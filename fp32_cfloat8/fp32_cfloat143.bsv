/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/

package fp32_cfloat143;

import fp32_cfloat8_types::*;

interface Ifc_fpu_convert_fp32_cfloat8_143;
    method ActionValue#(CFLOAT143) convert_fp32_cfloat8;
    method ActionValue#(FP32) convert_cfloat8_fp32;
endinterface

module fp32_to_cfloat143(Empty);

    Reg#(FP32) rg_fp32 <- mkReg(FP32{
        sign : 0,
        exponent : 0,
        mantissa : 'h0
    });

    Reg#(CFLOAT143) rg_cfloat143 <-mkReg(CFLOAT143{
        sign : 0,
        exponent : 0,
        mantissa : 'h0
    });

endmodule: fp32_to_cfloat143

endpackage: fp32_cfloat143