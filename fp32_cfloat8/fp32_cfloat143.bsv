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
(* synthesize *)
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

    Reg#(FLAGS_t) rg_flags <- mkReg(FLAGS_t {zero    : 0,
        invalid  : 0,
        denormal : 0,
        overflow : 0,
        underflow: 0
    });

    /* doc: rule: */
    rule rl_convert_fp32_cfloat8;

        /* doc: local: cfloat sign,exponent & mantissa local variables */
        Bit#(1)  lv_sign;
        Bit#(4)  lv_exponent;
        Bit#(3)  lv_mantissa;

        Bit#(8) exponent_overflow_limit = ((rg_bias <= 6'd15) ? (8'd127 + zeroExtend(6'd15 - rg_bias)) : (8'd127 - zeroExtend(rg_bias - 6'd15)));
        $display("Exponent Overflow Limit: %d", exponent_overflow_limit);

        rg_flags <= FLAGS_t {   zero     : pack((|rg_fp32.exponent == 1'b0) && (|rg_fp32.mantissa == 1'b0)),
                                invalid  : pack((&rg_fp32.exponent == 1'b1)),
                                denormal : pack((&rg_fp32.exponent == 1'b0) && ((rg_fp32.mantissa[22] == 1'b0))),
                                overflow : pack((rg_fp32.exponent > pack(exponent_overflow_limit)) && (rg_fp32.mantissa[22:19] == 4'b1111))
                                };

        // rg_cfloat143 <= CFLOAT143_t{sign: lv_sign, exponent: lv_exponent, mantissa: lv_mantissa};
    
    endrule: rl_convert_fp32_cfloat8

    method Action convert_fp32_cfloat143(FP32_t fp32_in, Bit#(6) bias);
        rg_fp32 <= fp32_in;
        rg_bias <= bias;
    endmethod: convert_fp32_cfloat143

    method CFLOAT143_t get_cfloat143();
        return rg_cfloat143;
    endmethod: get_cfloat143

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

    Reg#(Bit#(6)) rg_bias <- mkReg(0);

    Reg#(FLAGS_t) rg_flags <- mkReg(FLAGS_t {zero    : 0,
        invalid  : 0,
        denormal : 0,
        overflow : 0,
        underflow: 0
    });

    rule rl_convert_cfloat8_fp32;
        rg_fp32.sign <= rg_cfloat143.sign;
    endrule: rl_convert_cfloat8_fp32

    method Action convert_cfloat143_fp32(CFLOAT143_t cfloat143_in, Bit#(6) bias);
        rg_cfloat143 <= cfloat143_in;
    endmethod: convert_cfloat143_fp32

    method FP32_t get_fp32();
        return rg_fp32;
    endmethod: get_fp32

endmodule: mk_cfloat143_fp32

endpackage: fp32_cfloat143