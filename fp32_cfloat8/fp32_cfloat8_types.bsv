package fp32_cfloat8_types;


// Struct for fp32 format
typedef struct{
  Bit#(1) sign;
  Bit#(8) exponent;
  Bit#(23) mantissa;
}FP32_t deriving(Bits,Eq);

// Struct for cfloat8_152 format
typedef struct{
  Bit#(1) sign;
  Bit#(5) exponent;
  Bit#(2) mantissa;
}CFLOAT152_t deriving(Bits,Eq);

// Struct for cfloat8_143 format
typedef struct{
  Bit#(1) sign;
  Bit#(4) exponent;
  Bit#(3) mantissa;
}CFLOAT143_t deriving(Bits,Eq);

typedef struct{
  Bit#(1) zero;
  Bit#(1) invalid;
  Bit#(1) denormal;
  Bit#(1) overflow;
  Bit#(1) underflow;
}CFLOAT_FLAGS_t deriving(Bits,Eq);

typedef struct{
  Bit#(1) denormal;
  Bit#(1) zero;
  Bit#(1) qNaN;
  Bit#(1) infinity;
  Bit#(1) sNaN;
}FP32_FLAGS_t deriving(Bits,Eq);


endpackage: fp32_cfloat8_types
