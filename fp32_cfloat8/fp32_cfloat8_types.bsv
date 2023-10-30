/**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************/

package fp32_cfloat8_types;


// Struct for fp32 format
typedef struct{
   Bit#(1) sign;
   Bit#(8) exponent;
   Bit#(23) mantissa;
}FP32 deriving(Bits,Eq,Fshow);

// Struct for cfloat8_152 format
typedef struct{
   Bit#(1) sign;
   Bit#(5) exponent;
   Bit#(2) mantissa;
}CFLOAT152 deriving(Bits,Eq,Fshow);

// Struct for cfloat8_143 format
typedef struct{
   Bit#(1) sign;
   Bit#(4) exponent;
   Bit#(3) mantissa;
}CFLOAT143 deriving(Bits,Eq,Fshow);


endpackage: fp32_cfloat8_types
