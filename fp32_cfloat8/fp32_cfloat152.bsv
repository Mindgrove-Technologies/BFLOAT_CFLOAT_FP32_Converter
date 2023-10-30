/*************************************
 AUTHOR: Rohit Srinivas R G
 EMAIL: CS23Z002@smail.iitm.ac.in
 ************************************/

package fp32_cfloat152

// General Imports
import Clocks::*;

// Project Imports
import fp32_cfloat8_types::*;


// Interface declaration
(*always_ready, always_enabled*)
interface Ifc_fp32_cfloat152;
  method Action fp32_in(FP32_t fp_in);
  method Action bias_in(Bit#(6));
  method CFLOAT152_t cfloat152_out; 
endinterface: Ifc_fp32_cfloat152


module mk_fp32_cfloat15(Ifc_fp32_cfloat152);
  // Register Instantiation
  Reg#(FP32_t) fp32 <- mkReg(FP32_t {sign     :0,
				     exponent :0,
				     mantissa :0});
  
  Reg#(CFLOAT152_t) cfloat152 <- mkReg(CFLOAT152_t {sign     :0,
						    exponent :0,
						    mantissa :0});
  
  
  
  
  rule rl_sample;
    $display("Hello");
  endrule

  interface Ifc_fp32_cfloat152;
    method
  
endmodule: mk_fp32_cfloat15

endpackage: fp32_cfloat152
