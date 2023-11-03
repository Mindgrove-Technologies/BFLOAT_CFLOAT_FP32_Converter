/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/

package Testbench;

// ================================================================
// Project imports
import fp32_cfloat8_types ::*;
import fp32_cfloat152 ::*;

// ================================================================

(* synthesize *)
module mkTestbench (Empty);
  Ifc_fp32_cfloat152 mod <- mk_fp32_cfloat152;
  
  rule rl_sample;
    // mod.fp32_in(FP32_t {sign: 1'b0,
    //                     exponent: 8'h5,
    //                     mantissa: 23'h0A});
    mod.fp32_in(unpack(32'h251));
    
  endrule

   
endmodule

// ================================================================

endpackage
           
