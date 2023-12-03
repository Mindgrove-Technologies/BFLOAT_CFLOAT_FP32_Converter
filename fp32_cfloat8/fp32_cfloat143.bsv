/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/

package fp32_cfloat143;

// Project Imports
import fp32_cfloat8_types::*;

// Interface Declarations

(*always_ready, always_enabled*)
interface Ifc_fpu_convert_fp32_cfloat143;
    method Action convert_fp32_cfloat143(FP32_t fp32_in, Bit#(6) bias);
    method CFLOAT143_t get_cfloat143();
endinterface: Ifc_fpu_convert_fp32_cfloat143

(*always_ready, always_enabled*)
interface Ifc_fpu_convert_cfloat143_fp32;
    method Action convert_cfloat143_fp32(CFLOAT143_t cfloat143_in, Bit#(6) bias);
    method FP32_t get_fp32();
endinterface: Ifc_fpu_convert_cfloat143_fp32

// Module to convert IEEE-754 FP32 to Tesla's CFLOAT8_143.
module mk_fp32_cfloat143(Ifc_fpu_convert_fp32_cfloat143);

    // Register Declarations
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

    Reg#(Bit#(6)) rg_bias <- mkReg(0);

    rule rl_convert_fp32_cfloat8;
        rg_cfloat143.sign <= rg_fp32.sign;
    endrule

    method Action convert_fp32_cfloat143(FP32_t fp32_in, Bit#(6) bias);
        rg_fp32 <= fp32_in;
        rg_bias <= bias;
    endmethod

    method CFLOAT143_t get_cfloat143();
        return rg_cfloat143;
    endmethod

endmodule: mk_fp32_cfloat143

// Module to convert Tesla's CFLOAT8_143 to IEEE-754 FP32.
module mk_cfloat143_fp32(Ifc_fpu_convert_cfloat143_fp32);

    // Register Declarations
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

    method Action convert_cfloat143_fp32(CFLOAT143_t cfloat143_in, Bit#(6) bias);
        rg_cfloat143 <= cfloat143_in;
    endmethod

    method FP32_t get_fp32();
        return rg_fp32;
    endmethod

endmodule: mk_cfloat143_fp32

endpackage: fp32_cfloat143