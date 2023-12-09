import torch


# Python program to convert
# IEEE 754 floating point representation
# into real value

# Function to convert Binary
# of Mantissa to float value.
def convertToInt(mantissa_str):

	# variable to make a count
	# of negative power of 2.
	power_count = -1

	# variable to store
	# float value of mantissa.
	mantissa_int = 0

	# Iterations through binary
	# Number. Standard form of 
	# Mantissa is 1.M so we have 
	# 0.M therefore we are taking
	# negative powers on 2 for 
	# conversion.
	for i in mantissa_str:

		# Adding converted value of
		# Binary bits in every 
		# iteration to float mantissa.
		mantissa_int += (int(i) * pow(2, power_count))

		# count will decrease by 1
		# as we move toward right.
		power_count -= 1
		
	# returning mantissa in 1.M form.
	return (mantissa_int + 1)


# Function for converting decimal to binary
def float_bin(my_number, places = 3): 
	my_whole, my_dec = str(my_number).split(".")
	my_whole = int(my_whole)
	res = (str(bin(my_whole))+".").replace('0b','')

	for x in range(places):
		my_dec = str('0.')+str(my_dec)
		temp = '%1.20f' %(float(my_dec)*2)
		my_whole, my_dec = temp.split(".")
		res += my_whole
	return res



def IEEE754(n) : 
	# identifying whether the number
	# is positive or negative
	sign = 0
	if n < 0 : 
		sign = 1
		n = n * (-1) 
	p = 30
	# convert float to binary
	dec = float_bin (n, places = p)

	dotPlace = dec.find('.')
	onePlace = dec.find('1')
	# finding the mantissa
	if onePlace > dotPlace:
		dec = dec.replace(".","")
		onePlace -= 1
		dotPlace -= 1
	elif onePlace < dotPlace:
		dec = dec.replace(".","")
		dotPlace -= 1
	mantissa = dec[onePlace+1:]

	# calculating the exponent(E)
	exponent = dotPlace - onePlace
	exponent_bits = exponent + 127

	# converting the exponent from
	# decimal to binary
	exponent_bits = bin(exponent_bits).replace("0b",'') 

	mantissa = mantissa[0:23]

	# the IEEE754 notation in binary	 
	final = str(sign) + exponent_bits.zfill(8) + mantissa

	# # convert the binary to hexadecimal 
	# hstr = '0x%0*X' %((len(final) + 3) // 4, int(final, 2)) 
	return (final)


def convert_ieee_to_real(fp32_binary):
	# Floating Point Representation
	# to be converted into real 
	# value.
	ieee_32 = fp32_binary

	# First bit will be sign bit.
	sign_bit = int(ieee_32[0])

	# Next 8 bits will be 
	# Exponent Bits in Biased
	# form.
	exponent_bias = int(ieee_32[1 : 9], 2)

	# In 32 Bit format bias
	# value is 127 so to have
	# unbiased exponent
	# subtract 127.
	exponent_unbias = exponent_bias - 127

	# Next 23 Bits will be
	# Mantissa (1.M format)
	mantissa_str = ieee_32[9 : ]

	# Function call to convert
	# 23 binary bits into 
	# 1.M real no. form
	mantissa_int = convertToInt(mantissa_str)

	# The final real no. obtained
	# by sign bit, mantissa and
	# Exponent.
	real_no = pow(-1, sign_bit) * mantissa_int * pow(2, exponent_unbias)

	# Printing the obtained
	# Real value of floating
	# Point Representation.
	print("The float value of the given IEEE-754 representation is :",real_no)

	return real_no

import struct

def float_to_binary(num):
    # Convert the float number to IEEE 754 binary representation
    packed = struct.pack('>f', num)
    # Unpack the binary representation to get the bytes
    unpacked = struct.unpack('>I', packed)[0]
    # Convert the integer to its binary representation
    binary = bin(unpacked)[2:].zfill(32)  # 32 bits for single precision float
    return binary


def convert_bfloat16_fp32(bfloat_in,neg_zero):


	inf = 3.3895313892515355e+38
	neg_inf = -3.3895313892515355e+38
	qnan = 5.130820063729775e+38
	nqnan = -5.130820063729775e+38
	snan = 3.429408229125083e+38
	nsnan = -3.429408229125083e+38
	underflow = 1.17549435082e-38
	neg_underflow = -1.17549435082e-38

	if (bfloat_in != qnan and bfloat_in != snan and bfloat_in != nqnan and bfloat_in != nsnan):
		fp32_val = bfloat_in.float()
		fp32_list = fp32_val.tolist()

	float_list_binary = []

	# print("BFLOAT Val:")
	# print(fp32_list)
	# print("FP32_bin")
	# print(float_to_binary(fp32_list))
	for i in range(1):
		if(bfloat_in != (qnan) and bfloat_in != (snan) and bfloat_in < inf and bfloat_in != underflow and bfloat_in != neg_underflow and bfloat_in > neg_inf and bfloat_in != nqnan and bfloat_in != nsnan):
			if (fp32_list == 0.0 and neg_zero == 1):
				fp32_binary_temp = "1"+"0"*31
			elif (fp32_list == 0.0):
				fp32_binary_temp = "0"*32
			else:
				fp32_binary_temp = float_to_binary(fp32_list)
		elif(bfloat_in > inf and bfloat_in != qnan and bfloat_in != snan and bfloat_in != nqnan and bfloat_in != nsnan):
			fp32_binary_temp = "01111111100000000000000000000000"
		elif(bfloat_in < neg_inf and bfloat_in != qnan and bfloat_in != snan and bfloat_in != nqnan and bfloat_in != nsnan):
			fp32_binary_temp = "11111111100000000000000000000000"
		elif(bfloat_in == qnan):
			fp32_binary_temp = "01111111110000000000000000000001"
		elif(bfloat_in == snan):
			fp32_binary_temp = "01111111100000000000000000000001"
		elif(bfloat_in == nqnan):
			fp32_binary_temp = "11111111110000000000000000000001"
		elif(bfloat_in == nsnan):
			fp32_binary_temp = "11111111100000000000000000000001"
		elif(bfloat_in < underflow and bfloat_in > neg_underflow and bfloat_in != qnan and bfloat_in != snan and bfloat_in != nqnan and bfloat_in != nsnan):
			fp32_binary_temp = "00000000000000000000000000000000"
		elif(bfloat_in < neg_underflow and bfloat_in != qnan and bfloat_in != snan and bfloat_in != nqnan and bfloat_in != nsnan):
			fp32_binary_temp = "10000000000000000000000000000000"
		else:
			# fp32_binary = IEEE754(fp32_list)
			fp32_binary_temp = float_to_binary(fp32_list)
		
		if(bfloat_in != (qnan) and bfloat_in != (snan) and bfloat_in < inf and bfloat_in != underflow and bfloat_in != neg_underflow and bfloat_in > neg_inf and bfloat_in != nqnan and bfloat_in != nsnan):
			fp32_binary = fp32_binary_temp[0:16]+"0"*16
		else:
			fp32_binary = fp32_binary_temp

		float_list_binary.append(fp32_binary)

	# print("FP32 Binaries are: ")
	# print(float_list_binary)

	return float_list_binary[0]