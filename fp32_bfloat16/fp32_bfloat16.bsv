/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/
package fp32_bfloat16
// General Imports
import Clocks :: *;

// Project Imports
import fp32_cfloat8_types ::*;

(*always_ready, always_enabled*)

(*always_ready, always_enabled*)
interface Ifc_fp32_bfloat16;
  method Action fp32_in(FP32_t fp_in);
  method BFLOAT16_t bfloat16_out; 
endinterface: Ifc_fp32_cfloat152

module mk_fp32_bfloat16(Ifc_fp32_bfloat16);
  /* doc: reg: contains the fp32 representation */
  Reg#(FP32_t) rg_fp32 <- mkReg(FP32_t {sign     :0,
					                              exponent :0,
					                              mantissa :0});
  
  /* doc: reg: contains the bfloat16 representation */
  Reg#(BFLOAT16_t) rg_cfloat152 <- mkReg(BFLOAT16_t {sign     :0,
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
     
    rule rl_convert_fp32_bfloat16;
    BFLOAT16_t bfloat16 = BFLOAT16_t {sign     : 0,
                                      exponent : 0,
                                      mantissa : 0});
    FLAGS_t flags;

    /* Computing flags */
    
    
    
    /* Zero */
    
    



  endrule: rl_convert_fp32_bfloat16
endmodule: mk_fp32_bfloat16
  



(*always_ready, always_enabled*)
interface Ifc_bfloat16_fp32;
    method Action bfloat (BFLOAT16_t bfloat_in);
    method FP32_t fp32_out;
endinterface: Ifc_bfloat16_fp32

(* synthesize *)
module mk_bfloat16_fp32(Ifc_cfloat16_fp32);
 
  /* doc: reg: contains the fp32 representation */
  Reg#(FP32_t) rg_fp32 <- mkReg(FP32_t {sign     :0,
          exponent :0,
          mantissa :0});
  
  /* doc: reg: contains the bfloat16 representation */
  Reg#(BFLOAT16_t) rg_bfloat16 <- mkReg(BFLOAT16_t {sign     :0,
                                        exponent :0,
                                        mantissa :0});
  
  /* doc: reg: contains the flags */
  Reg#(FP32_FLAGS_t) rg_flags <- mkReg(FP32_FLAGS_t {denormal  : 0,
                                                     zero      : 0,
                                                     qNaN      : 0,
                                                     infinity  : 0,
                                                     sNaN      : 0});
  
  
  rule rl_convert_bfloat16_fp32;
    FP32_FLAGS_t fp32_flags = FP32_FLAGS_t {denormal  : 0,
                                            zero      : 0,
                                            qNaN      : 0,
                                            infinity  : 0,
                                            sNaN      : 0};
    
    FP32_t fp32 = FP32_t {sign     :0,
                          exponent :0,
                          mantissa :0};
    
    fp32.sign = rg_bfloat16.sign;

    if(rg_bfloat16.exponent == 8'b00000000 && rg_bfloat16.mantissa == 7'b0000000)
    begin
      fp32_flags.zero = 1;
      fp32.exponent = rg_bfloat16.exponent;
      fp32.mantissa[22:16] = rg_bfloat16.mantissa;
    end
    else if(rg_bfloat16.exponent == 8'b11111111)
    begin
      fp32.exponent = rg_bfloat16.exponent;
      fp32.mantissa[22:16] = rg_bfloat16.mantissa;
    end
    
    rg_fp32 <= FP32_t {sign     : fp32.sign,
                       exponent : fp32.exponent,
                       mantissa : fp32.mantissa};
    
    rg_flags <= FP32_FLAGS_t {denormal : fp32_flags.denormal,
                              zero     : fp32_flags.zero,
                              qNaN     : fp32_flags.qNaN,
                              infinity : fp32_flags.infinity,
                              sNaN     : fp32_flags.sNaN};
    
  endrule: rl_convert_bfloat16_fp32

  
  method Action cfloat152_in (CFLOAT152_t cfloat_in);
    rg_cfloat152 <= cfloat_in;
  endmethod: cfloat152_in
  
  method FP32_t fp32_out;
    return rg_fp32;
  endmethod: fp32_out
  
  
endmodule: mk_bfloat16_fp32

endpackage: fp32_bfloat16