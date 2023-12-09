/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/

package fp32_cfloat152; 

// General Imports
import Clocks :: *;

// Project Imports
import fp32_cfloat8_types ::*;

// Preject defines
// `define verbose


// Interface declaration
(*always_ready, always_enabled*)
interface Ifc_fp32_cfloat152;
  method Action fp32_in(FP32_t fp_in);
  method Action bias_in(Bit#(6) bias);
  method CFLOAT152_t cfloat152_out; 
endinterface: Ifc_fp32_cfloat152

(* synthesize *)
module mk_fp32_cfloat152(Ifc_fp32_cfloat152);
  /* doc: reg: contains the fp32 representation */
  Reg#(FP32_t) rg_fp32 <- mkReg(FP32_t {sign     :0,
          exponent :0,
          mantissa :0});
  
  /* doc: reg: contains the cfloat152 representation */
  Reg#(CFLOAT152_t) rg_cfloat152 <- mkReg(CFLOAT152_t {sign     :0,
                                                       exponent :0,
                                                       mantissa :0});
  
  /* doc: reg: contains the configurable bias */
  Reg#(Bit#(6)) rg_bias <- mkReg(0);
  
  /* doc: reg: contains the flags */
  Reg#(CFLOAT_FLAGS_t) rg_flags <- mkReg(CFLOAT_FLAGS_t {zero     : 0,
                                                         invalid  : 0,
                                                         denormal : 0,
                                                         overflow : 0,
                                                         underflow: 0});
  
  /* doc: rule: */
  rule rl_convert_fp32_cfloat152;
    /* doc: local: cfloat sign,exponent & mantissa local variables */
    // Bit#(1) cfloat_sign;
    // Bit#(5) cfloat_exponent;
    // Bit#(2) cfloat_mantissa;
    CFLOAT152_t cfloat152 = CFLOAT152_t {sign     : 0,
                                         exponent : 0,
                                         mantissa : 0};

    /* doc: local: limit used to determine if the overflow flag is to be set
     * if the max_exponent <= rg_bias,then
     * limit = 127 + (max_exponent - bias)
     * else
     * limit = 127 - (rg_bias-max_exponent)
     * where bias of fp32 = 127
     */
    Bit#(8) exponent_overflow_limit  = ((rg_bias <= 6'd31) ? 
                                        (8'd127+zeroExtend((6'd31 - rg_bias)))
                                      : (8'd127-zeroExtend((rg_bias - 6'd31))));
    
    Bit#(8) exponent_underflow_limit = 8'd128 - zeroExtend(rg_bias);
    
    CFLOAT_FLAGS_t flags;
    
    flags.zero      = pack(((|rg_fp32.exponent == 1'b0) && (|rg_fp32.mantissa == 1'b0)) || (rg_fp32.exponent < exponent_underflow_limit - 8'd4) );
    flags.invalid   = pack((&rg_fp32.exponent == 1'b1));
    flags.overflow  = pack(((rg_fp32.exponent == exponent_overflow_limit) 
                       && (rg_fp32.mantissa[22:21] == 2'b11)) || rg_fp32.exponent > exponent_overflow_limit);
    flags.underflow = pack(rg_fp32.exponent < exponent_underflow_limit); 
    flags.denormal = 1'd0;


  `ifdef verbose
    $display($time," overflow %d",flags.overflow);
    $display($time," fp32_exponent %d",rg_fp32.exponent);
    $display("Limit %d",exponent_underflow_limit);
  `endif
    cfloat152.sign     = rg_fp32.sign;
    /* doc: Conversion to zero*/
    if(flags.zero == 1'b1) begin
    `ifdef verbose 
      $display($time,"Zero");
    `endif
      cfloat152.exponent = 5'd0;
      cfloat152.mantissa = 2'd0;
    end
    /* doc: Overflow */
    else if((flags.invalid == 1'b1 ) || (flags.overflow == 1'b1)) begin
    `ifdef verbose 
      $display($time,"Overflow");
    `endif
      // cfloat152.sign     = rg_fp32.sign;
      cfloat152.exponent = 5'b11111;
      cfloat152.mantissa = 2'b11;
    end
    /* doc: Underflow */
    else if(flags.underflow == 1'b1) begin
    `ifdef verbose
      $display($time, "Underflow");
    `endif
      if (rg_fp32.exponent < exponent_underflow_limit - 8'd4) begin
        cfloat152.exponent = 5'd0;
        cfloat152.mantissa = 2'd0;
      end
      else if (rg_fp32.exponent == exponent_underflow_limit - 8'd4) begin
        cfloat152.exponent = 5'd0;
        flags.denormal = 1'd1;
        cfloat152.mantissa = 2'b01;
      end
      else if (rg_fp32.exponent == exponent_underflow_limit - 8'd3) begin
        cfloat152.exponent = 5'd0;
        flags.denormal = 1'd1;
        if (rg_fp32.mantissa[22:21] == 2'b00 || rg_fp32.mantissa[22:21] == 2'b01) 
          cfloat152.mantissa = 2'b01;
        else
          cfloat152.mantissa = 2'b10;
      end
      else if (rg_fp32.exponent == exponent_underflow_limit - 8'd2) begin
        cfloat152.exponent = 5'd0;
        flags.denormal = 1'd1;
        if (rg_fp32.mantissa[22:21] == 2'b00) 
          cfloat152.mantissa = 2'b10;
        else
          cfloat152.mantissa = 2'b11;
      end
      else if (rg_fp32.exponent == exponent_underflow_limit - 8'd1) begin
        cfloat152.exponent = 5'd0;
        if (rg_fp32.mantissa[22:21] == 2'b00 ) begin
          flags.denormal = 1'd1;
          cfloat152.mantissa = 2'b11;
        end
        else if (rg_fp32.mantissa[22:21] == 2'b01 && (rg_fp32.mantissa[20]) == 1'b0) begin
          flags.denormal = 1'd1;
          cfloat152.mantissa = 2'b11;
        end
        else begin
          cfloat152.exponent = 5'd1;
          cfloat152.mantissa = 2'b00;
        end
      end
    end
    /* Normal Numbers 
     * REVIEW: Check if there is an overflow or underflow possibility when rounding up or
     * rounding down the numbers
     * 
     */
    else begin
    `ifdef verbose
      $display($time,"Normal %d",flags.overflow);
    `endif
      cfloat152.exponent = truncate(rg_fp32.exponent - 8'd127 + zeroExtend(rg_bias));
      Bit#(7) temp = {cfloat152.exponent,rg_fp32.mantissa[22:21]};
      if (rg_fp32.mantissa[20] == 1'b1) begin
        temp = temp + 7'd1;
        if (temp == 7'd0) 
          flags.overflow = 1'd1;
      end
      cfloat152.exponent = temp[6:2];
      cfloat152.mantissa = temp[1:0];
    end
    
    rg_cfloat152 <= CFLOAT152_t {sign     : cfloat152.sign,
                                 exponent : cfloat152.exponent,
                                 mantissa : cfloat152.mantissa};
 
    rg_flags <= CFLOAT_FLAGS_t {zero        : flags.zero,
                                invalid     : flags.invalid,
                                overflow    : flags.overflow,
                                underflow   : flags.underflow,
                                denormal    : flags.denormal};

  endrule: rl_convert_fp32_cfloat152
 
  /* doc: method: FP32 Input
   * Argument: 32-bit number converted to FP32 Format
   */
  method Action fp32_in(FP32_t fp_in);
    rg_fp32 <= fp_in;
  endmethod: fp32_in
  
  /* doc: method: bias_in
   * Argument: 6-bit bias number
   */
  method Action bias_in(Bit#(6) bias);
    rg_bias <= bias;
  endmethod: bias_in

  /* doc: method: Output CFLOAT8 1_5_2 number
   * return: 8-bit value in the CFLOAT 1_5_2 format
   */
  method CFLOAT152_t cfloat152_out;
    return rg_cfloat152;
  endmethod: cfloat152_out
    
  
endmodule: mk_fp32_cfloat152

(*always_ready, always_enabled*)
interface Ifc_cfloat152_fp32;
  method Action cfloat152_in (CFLOAT152_t cfloat_in);
  method Action bias_in (Bit#(6) bias);
  method FP32_t fp32_out;
endinterface: Ifc_cfloat152_fp32

(* synthesize *)
module mk_cfloat152_fp32(Ifc_cfloat152_fp32); 
  /* doc: reg: contains the fp32 representation */
  Reg#(FP32_t) rg_fp32 <- mkReg(FP32_t {sign     :0,
          exponent :0,
          mantissa :0});
  
  /* doc: reg: contains the cfloat152 representation */
  Reg#(CFLOAT152_t) rg_cfloat152 <- mkReg(CFLOAT152_t {sign     :0,
                   exponent :0,
                   mantissa :0});
  
  /* doc: reg: contains the configurable bias */
  Reg#(Bit#(6)) rg_bias <- mkReg(0);
  
  /* doc: reg: contains the flags */
  Reg#(FP32_FLAGS_t) rg_flags <- mkReg(FP32_FLAGS_t {denormal  : 0,
                                                     zero      : 0,
                                                     qNaN      : 0,
                                                     infinity  : 0,
                                                     sNaN      : 0});
  
  
  rule rl_convert_cfloat152_fp32;
    FP32_FLAGS_t fp32_flags = FP32_FLAGS_t {denormal  : 0,
                                            zero      : 0,
                                            qNaN      : 0,
                                            infinity  : 0,
                                            sNaN      : 0};
    
    FP32_t fp32 = FP32_t {sign     :0,
                          exponent :0,
                          mantissa :0};
    
    /* Zero */
    fp32.sign = rg_cfloat152.sign;
    if (|rg_cfloat152.exponent == 1'b0 && |rg_cfloat152.mantissa == 1'b0) begin
      fp32.exponent = 8'd0;
      fp32.mantissa = 23'd0;
      fp32_flags.zero = 1'b1;
    end
    /* cfloat Denormal Numbers */
    else if (|rg_cfloat152.exponent == 1'b0 && |rg_cfloat152.mantissa != 1'b0) begin
      fp32.mantissa  = 23'd0;
      if (rg_cfloat152.mantissa == 2'b01)
        fp32.exponent = 8'd128 - 8'd3 - zeroExtend(rg_bias);
      else if (rg_cfloat152.mantissa == 2'b10)
        fp32.exponent = 8'd128 - 8'd2 - zeroExtend(rg_bias);
      else begin
        fp32.exponent     = 8'd128 - 8'd2 - zeroExtend(rg_bias);
        fp32.mantissa[22] = 1'b1;
      end
    end
    /* Normal Numbers */
    else begin
      fp32.mantissa[22:21] = rg_cfloat152.mantissa;
      fp32.exponent        = zeroExtend(rg_cfloat152.exponent) - zeroExtend(rg_bias) + 8'd127;
    end
    
    rg_fp32 <= FP32_t {sign     : fp32.sign,
                       exponent : fp32.exponent,
                       mantissa : fp32.mantissa};
    
    rg_flags <= FP32_FLAGS_t {denormal : fp32_flags.denormal,
                              zero     : fp32_flags.zero,
                              qNaN     : fp32_flags.qNaN,
                              infinity : fp32_flags.infinity,
                              sNaN     : fp32_flags.sNaN};
    
  endrule: rl_convert_cfloat152_fp32
  
  method Action cfloat152_in (CFLOAT152_t cfloat_in);
    rg_cfloat152 <= cfloat_in;
  endmethod: cfloat152_in
  
  method Action bias_in (Bit#(6) bias);
    rg_bias <= bias;
  endmethod: bias_in
  
  method FP32_t fp32_out;
    return rg_fp32;
  endmethod: fp32_out
  
  
endmodule: mk_cfloat152_fp32


endpackage: fp32_cfloat152
