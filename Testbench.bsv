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

(* synthesize *)
module mkTestbench (Ifc_Testbench);
    Ifc_fpu_convert_fp32_cfloat143 cfloat8_143_test <- mk_fp32_cfloat143;
    
    Bit#(6) bias = 6'b000100;

    rule rl_convert;

      cfloat8_143_test.convert_fp32_cfloat143(FP32_t {sign: 1'b0,
                          exponent: 8'b00000111,
                          mantissa: 23'b11100000000000000011111}, bias);
    endrule

    rule rl_get_result;

      let result = cfloat8_143_test.get_cfloat143();
      // $display("Result: %8b", result);
    endrule
  
endmodule

// ================================================================

endpackage
           
