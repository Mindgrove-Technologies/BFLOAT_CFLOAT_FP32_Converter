/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/
package fp32_bfloat16;
// General Imports
import Clocks :: *;

// Project Imports
import fp32_bfloat16_types ::*;

(*always_ready, always_enabled*)

(*always_ready, always_enabled*)
interface Ifc_fp32_bfloat16;
  method Action fp32_in(FP32_t fp_in);
  method BFLOAT16_t bfloat16_out; 
endinterface: Ifc_fp32_bfloat16

(* synthesize *)
module mk_fp32_bfloat16(Ifc_fp32_bfloat16);
  /* doc: reg: contains the fp32 representation */
  Reg#(FP32_t) rg_fp32 <- mkReg(FP32_t {sign     :0,
					                              exponent :0,
					                              mantissa :0});
  
  /* doc: reg: contains the bfloat16 representation */
  Reg#(BFLOAT16_t) rg_bfloat16 <- mkReg(BFLOAT16_t {sign     :0,
						                                        exponent :0,
						                                        mantissa :0});

  /* doc: reg: contains the flags for the conversion */
  Reg#(FLAGS_t) rg_flags <- mkReg(FLAGS_t {denormal  : 0,
                                           zero      : 0,
                                           qNaN      : 0,
                                           infinity  : 0,
                                           sNaN      : 0});


    /* doc: rule: rule to convert fp32 to bfloat16
     * Implicit cond: None
     * Explicit cond: None
     * Desc: conversion from fp32 to bfloat16 with round-to-nearest conversion strategy
     */
     
    rule rl_convert_fp32_bfloat16;
      
      BFLOAT16_t bfloat16 = BFLOAT16_t {sign     : 0,
                                        exponent : 0,
                                        mantissa : 0};
      FLAGS_t flags;
      
       
      /* Computing flags */
      flags.zero     = pack(|rg_fp32.exponent == 1'b0 && |rg_fp32.mantissa == 1'b0);
      flags.infinity = pack(&rg_fp32.exponent == 1'b1 && |rg_fp32.mantissa == 1'b0);
      flags.qNaN     = pack(&rg_fp32.exponent == 1'b1 && rg_fp32.mantissa[22] == 1'b1 && rg_fp32.mantissa[0] == 1'b1);
      flags.sNaN     = pack(&rg_fp32.exponent == 1'b1 && rg_fp32.mantissa[22] == 1'b0 && rg_fp32.mantissa[0] == 1'b1);
      flags.denormal = pack(|rg_fp32.exponent == 1'b0 && (flags.qNaN == 0) && (flags.sNaN == 0) && (flags.zero == 0));


      /* Zero */
      if(flags.zero == 1'b1) begin
        bfloat16.exponent = 8'd0;
        bfloat16.mantissa = 7'd0;
      end
      /* Infinity */
      else if (flags.infinity == 1'b1) begin
        bfloat16.exponent = 8'b11111111;
        bfloat16.mantissa = 7'd0;
      end
      //TODO Check the difference between qNaN and sNaN
      /* qNaN */
      else if(flags.qNaN == 1'b1) begin
        bfloat16.exponent = 8'b11111111;
        bfloat16.mantissa = 7'b1000001;
      end
      /* sNaN */
      else if(flags.sNaN == 1'b1) begin
        bfloat16.exponent = 8'b11111111;
        bfloat16.mantissa = 7'b0000001;
      end
      /* Normal Numbers*/
      else begin
        bfloat16.exponent = rg_fp32.exponent;
        Bit#(15) temp = {bfloat16.exponent,rg_fp32.mantissa[22:16]};
        if(rg_fp32.mantissa[16] == 1'b0 && rg_fp32.mantissa[15] == 1'b1)
          temp = temp;
        else if (rg_fp32.mantissa[15] == 1'b1) begin
          temp = temp + 15'd1;
        end
        bfloat16.exponent = temp[14:7];
        bfloat16.mantissa = temp[6:0];
      end
    
      rg_bfloat16 <= BFLOAT16_t{
                                sign: bfloat16.sign,
                                exponent: bfloat16.exponent,
                                mantissa: bfloat16.mantissa};

  endrule: rl_convert_fp32_bfloat16

  method Action fp32_in (FP32_t fp_in);
    rg_fp32 <= fp_in;
  endmethod: fp32_in
  
  method BFLOAT16_t bfloat16_out;
    return rg_bfloat16;
  endmethod: bfloat16_out

endmodule: mk_fp32_bfloat16


(*always_ready, always_enabled*)
interface Ifc_bfloat16_fp32;
    method Action bfloat16_in (BFLOAT16_t bfloat_in);
    method FP32_t fp32_out;
endinterface: Ifc_bfloat16_fp32

(* synthesize *)
module mk_bfloat16_fp32(Ifc_bfloat16_fp32);
 
  /* doc: reg: contains the fp32 representation */
  Reg#(FP32_t) rg_fp32 <- mkReg(FP32_t {sign     :0,
                                        exponent :0,
                                        mantissa :0});
  
  /* doc: reg: contains the bfloat16 representation */
  Reg#(BFLOAT16_t) rg_bfloat16 <- mkReg(BFLOAT16_t {sign     :0,
                                                    exponent :0,
                                                    mantissa :0});
  
  /* doc: reg: contains the flags */
  Reg#(FLAGS_t) rg_flags <- mkReg(FLAGS_t {denormal  : 0,
                                                     zero      : 0,
                                                     qNaN      : 0,
                                                     infinity  : 0,
                                                     sNaN      : 0});
  
  
  rule rl_convert_bfloat16_fp32;
    FLAGS_t fp32_flags = FLAGS_t {denormal  : 0,
                                            zero      : 0,
                                            qNaN      : 0,
                                            infinity  : 0,
                                            sNaN      : 0};
    
    FP32_t fp32 = FP32_t {sign     :0,
                          exponent :0,
                          mantissa :0};

    FLAGS_t bfloat_flags;
  
    bfloat_flags.zero     = pack(rg_bfloat16.exponent == 8'b00000000 && rg_bfloat16.mantissa == 7'b0000000);
    bfloat_flags.infinity = pack(rg_bfloat16.exponent == 8'b11111111 && rg_bfloat16.mantissa == 7'b0000000);
    bfloat_flags.qNaN     = pack(rg_bfloat16.exponent == 8'b11111111 && rg_bfloat16.mantissa[6] == 1'b1 && rg_bfloat16.mantissa[0] == 1'b1);
    bfloat_flags.sNaN     = pack(rg_bfloat16.exponent == 8'b11111111 && rg_bfloat16.mantissa[6] == 1'b0 && rg_bfloat16.mantissa[0] == 1'b1);
    bfloat_flags.denormal = pack(rg_bfloat16.exponent == 8'b00000000 && (bfloat_flags.qNaN == 0) && (bfloat_flags.sNaN == 0) && (bfloat_flags.zero == 0));
    
    fp32.sign = rg_bfloat16.sign;

    if(bfloat_flags.zero == 1)
    begin
      fp32_flags.zero = 1;
      fp32.exponent = rg_bfloat16.exponent;
      fp32.mantissa[22:16] = rg_bfloat16.mantissa;
    end
    else if(bfloat_flags.infinity == 1)
    begin
      fp32_flags.infinity = 1;
      fp32.exponent = rg_bfloat16.exponent;
      fp32.mantissa[22:16] = rg_bfloat16.mantissa;
    end
    else if(bfloat_flags.qNaN == 1)
    begin
      fp32_flags.qNaN = 1;
      fp32.exponent = rg_bfloat16.exponent;
      fp32.mantissa = 23'b10000000000000000000001;
    end
    else if(bfloat_flags.sNaN == 1)
    begin
      fp32_flags.sNaN = 1;
      fp32.exponent = rg_bfloat16.exponent;
      fp32.mantissa = 23'b00000000000000000000001;
    end
    else if(bfloat_flags.denormal == 1)
    begin
      fp32_flags.denormal = 1;
      fp32.exponent = rg_bfloat16.exponent;
      fp32.mantissa[22:16] = rg_bfloat16.mantissa;
    end
    else
    begin
      fp32.exponent = rg_bfloat16.exponent;
      fp32.mantissa[22:16] = rg_bfloat16.mantissa;
    end
    
    rg_fp32 <= FP32_t {sign     : fp32.sign,
                       exponent : fp32.exponent,
                       mantissa : fp32.mantissa};
    
    rg_flags <= FLAGS_t {denormal : fp32_flags.denormal,
                              zero     : fp32_flags.zero,
                              qNaN     : fp32_flags.qNaN,
                              infinity : fp32_flags.infinity,
                              sNaN     : fp32_flags.sNaN};
    
  endrule: rl_convert_bfloat16_fp32

  
  method Action bfloat16_in (BFLOAT16_t bfloat_in);
    rg_bfloat16 <= bfloat_in;
  endmethod: bfloat16_in
  
  method FP32_t fp32_out;
    return rg_fp32;
  endmethod: fp32_out
  
  
endmodule: mk_bfloat16_fp32

endpackage: fp32_bfloat16