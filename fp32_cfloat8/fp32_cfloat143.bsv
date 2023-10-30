/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/

package fp32_cfloat143;

import fp32_cfloat8_types::*;

interface Ifc_fpu_convert_fp32_cfloat8_143;
    method ActionValue#(CFLOAT143_t) convert_fp32_cfloat143;
    method ActionValue#(FP32_t) convert_cfloat143_fp32;
endinterface: Ifc_fpu_convert_fp32_cfloat8_143

module fp32_to_cfloat143(Ifc_fpu_convert_fp32_cfloat8_143);

    Reg#(FP32_t) rg_fp32 <- mkReg(FP32_t {
        sign : 0,
        exponent : 0,
        mantissa : 'h0
    });

    Reg#(CFLOAT143_t) rg_cfloat143 <-mkReg(CFLOAT143_t {
        sign : 0,
        exponent : 0,
        mantissa : 'h0
    });

endmodule: fp32_to_cfloat143

endpackage: fp32_cfloat143