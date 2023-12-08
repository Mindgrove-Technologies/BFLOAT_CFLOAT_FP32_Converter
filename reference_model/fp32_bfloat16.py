import torch


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


# Driver Code
if __name__ == "__main__" :
	elemns = 1
	a = torch.rand(elemns, dtype=torch.float32)
	b = a.float()
	c = b.bfloat16()

	float_list = b.tolist()
	float_list_binary = []

	# print(float_list)
	for i in range(elemns):
		fp32_binary = IEEE754(float_list[i])
		float_list_binary.append(IEEE754(float_list[i]))
		# print (fp32_binary)
		
	print("FP32 Binaries are: ")
	print(float_list_binary)
	
	bfloat_list = c.tolist()

	bfloat_list_binary = []

	# print(bfloat_list)
	for i in range(elemns):
		bfloat_binary_temp = IEEE754(bfloat_list[i])
		bfloat_binary = bfloat_binary_temp[0:16]
		bfloat_list_binary.append(bfloat_binary)
		# print (bfloat_binary)

	print("BFLOAT16 Binaries are: ")
	print(bfloat_list_binary)