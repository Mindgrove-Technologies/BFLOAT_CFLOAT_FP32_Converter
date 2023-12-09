/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/

package Testbench;

// ================================================================
// Project imports
// ================================================================


import fp32_cfloat8_types ::*;
import fp32_bfloat16_types ::*;
import fp32_cfloat152 ::*;
import fp32_cfloat143 ::*;
import fp32_bfloat16 ::*;

// ================================================================

// ================================================================
// Project Defines
// ================================================================

`define simulate_bfloat 1

// ================================================================

interface Ifc_Testbench;
  
endinterface

// (* synthesize *)
// module mkTestbench (Ifc_Testbench);

(* synthesize *)
module mkTestbench (Empty);

`ifdef simulate_cfloat_152
  Ifc_fp32_cfloat152 mod <- mk_fp32_cfloat152;
  Reg#(Bit#(32)) rg_counter <- mkReg(0);
  
  rule rl_count;
    rg_counter <= rg_counter + 1;
  endrule
  
  // rule rl_sample_1 (rg_counter <= 32'd1000);
  rule rl_sample_1 ;
    // mod.fp32_in(FP32_t {sign: 1'b0,
    //                     exponent: 8'h5,
    //                     mantissa: 23'h0A});
    mod.fp32_in(unpack(32'b01000000011100000000000000000000));
    mod.bias_in(6'd0);
  endrule

  // rule rl_sample_2 (rg_counter >= 32'd1000);
  //   // mod.fp32_in(unpack(32'b01100001111111111111111111111111));
  //   mod.fp32_in(unpack(32'b01000000000000000000000000000000));
  //   mod.bias_in(6'd0);
  // endrule
`endif

`ifdef simulate_cfloat_143
  // Ifc_fpu_convert_fp32_cfloat143 mod <- mk_fp32_cfloat143;
  Ifc_fpu_convert_cfloat143_fp32 sm_bi <- mk_cfloat143_fp32;

  
  Reg#(Bit#(32)) rg_counter <- mkReg(0);
  Bit#(6) bias = 0;

  rule rl_count;
    rg_counter <= rg_counter + 1;
  endrule

  // doc: rule: This rule is to check conversion of FP32 to CFLOAT8_143.
  // rule rl_sample_1 ;
  //   mod.convert_fp32_cfloat143(unpack(32'b01000000011110000000000000000000), bias);
  // endrule

  // doc: rule: This rule is to check conversion of CFLOAT8_143 to FP32.
  rule rl_sample_2;
    sm_bi.convert_cfloat143_fp32(unpack(8'b00000011), bias);
  endrule

  // CFLOAT143_t lv_cfloat_val = mod.get_cfloat143();

  FP32_t lv_fp32_val = sm_bi.get_fp32();

  // $display("Cfloat 8 value: %8b", pack(lv_cfloat_val));

  // $display("FP32 value: %32b", pack(lv_fp32_val));


  `endif

  `ifdef simulate_bfloat
  
    Ifc_fp32_bfloat16 mod <- mk_fp32_bfloat16;

    // doc: rule: This rule is to check conversion of FP32 to CFLOAT8_143.
    rule rl_sample_1 ;
      mod.fp32_in(unpack(32'b01000000011110011000000000000000));
    endrule

    BFLOAT16_t lv_bfloat_val = mod.bfloat16_out;

  `endif
   
endmodule

// ================================================================

endpackage
           
