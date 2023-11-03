/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/

package Testbench;

// ================================================================
// Project imports

import fp32_cfloat8_types ::*;
import fp32_cfloat143 ::*;

// ================================================================

interface Ifc_Testbench;
  
endinterface

// (* synthesize *)
// module mkTestbench (Ifc_Testbench);

(* synthesize *)
module mkTestbench (Empty);
    Ifc_fpu_convert_fp32_cfloat143 mod <- mk_fp32_cfloat143;
    
    Bit#(6) bias = 6'b000011;

    rule rl_sample;
      mod.convert_fp32_cfloat143(FP32_t {sign: 1'b0,
                          exponent: 8'h5,
                          mantissa: 23'h0A}, bias);
    endrule
   
endmodule

// ================================================================

endpackage
           
