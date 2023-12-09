'''**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************'''
import sys
import logging


import struct

def fp32_bin(value):
    # Use struct.pack to convert the float to IEEE 754 binary representation
    binary_representation = struct.pack('>f', value)

    # Convert binary to a list of 32 bits (0s and 1s)
    bits = [format(byte, '08b') for byte in binary_representation]

    # Combine the bits into a single string
    binary_string = ''.join(bits)

    return binary_string

def convert_cfloat143_fp32(cfloat143_in,bias,neg_zero):
    dict_n     = {}
    dict_d     = {}
    CHECK_RES  = False
    sign = 0
    if(cfloat152_in < 0):
        cfloat152_in = -cfloat152_in
        sign = 1
    ####################
    logging.info("Checking if the given cfloat number is a valid")
    for e in range(1,16):
        dict_n[e]=list()

    for e in range(1,16):
        value= 2**(e-bias)
        for m in range(8):
            if(m == 0):
                dict_n[e].append(value*1)
            elif(m == 1):
                dict_n[e].append(value*1.125)
            elif(m == 2):
                dict_n[e].append(value*1.25)
            elif(m == 3):
                dict_n[e].append(value*1.375)
            elif(m == 4):
                dict_n[e].append(value*1.500)
            elif(m == 5):
                dict_n[e].append(value*1.625)
            elif(m == 6):
                dict_n[e].append(value*1.750)
            else:
                dict_n[e].append(value*1.875)

    for m in range(1,8):
        value = 2**(-bias)
        if (m == 1):
            dict_d[m] = value*0.125
        elif (m == 2):
            dict_d[m] = value*0.250
        elif (m == 3):
            dict_d[m] = value*0.375
        elif (m == 4):
            dict_d[m] = value*0.500
        elif (m == 5):
            dict_d[m] = value*0.625
        elif (m == 6):
            dict_d[m] = value*0.750
        else:
            dict_d[m] = value*0.875


    for e in range(1,16):
        for m in range(8):
            if (cfloat143_in == dict_n[e][m]):
                CHECK_RES = True
                break
            else:
                continue
    
    for m in range(1,8):
        if (cfloat143_in == dict_d[m]):
            CHECK_RES = True
            break
        else:
            continue

    if (cfloat152_in == 0.0):
        CHECK_RES = True


    if (CHECK_RES == True):
        # print(f"ANS = {cfloat143_in}")
        logging.info("The given cfloat is a valid number")
    else:
        logging.error("The given cfloat number is not a valid input")
     
    if (sign == 1):
        cfloat152_in = -cfloat152_in
        
    if (CHECK_RES and not neg_zero):
        bin_fp32 = fp32_bin(cfloat152_in)
        return bin_fp32
    elif (CHECK_RES and neg_zero):
        bin_fp32 = fp32_bin(-0.0)
        return bin_fp32
    else:
        sys.exit(1)
def main():
    cfloat_in = 3.75
    bias = 0

    print(convert_cfloat143_fp32(cfloat_in,bias))

main()