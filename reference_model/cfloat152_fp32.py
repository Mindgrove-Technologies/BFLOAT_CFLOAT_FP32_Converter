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

def convert_cfloat152_fp32(cfloat152_in,bias):
    dict_n     = {}
    dict_d     = {}
    CHECK_RES  = False
    ####################
    logging.info("Checking if the given cfloat number is a valid")
    for e in range(1,32):
        dict_n[e]=list()

    for e in range(1,32):
        value= 2**(e-bias)
        for m in range(4):
            if(m == 0):
                dict_n[e].append(value*1)
            elif(m == 1):
                dict_n[e].append(value*1.25)
            elif(m == 2):
                dict_n[e].append(value*1.5)
            else:
                dict_n[e].append(value*1.75)

    for m in range(1,4):
        value = 2**(-bias)
        if (m == 1):
            dict_d[m] = value*0.25
        elif (m==2):
            dict_d[m] = value*0.5
        else:
            dict_d[m] = value*0.75

    for e in range(1,32):
        for m in range(4):
            if (cfloat152_in == dict_n[e][m]):
                CHECK_RES = True
                break
            else:
                continue
    
    for m in range(1,4):
        if (cfloat152_in == dict_d[m]):
            CHECK_RES = True
            break
        else:
            continue

    if (CHECK_RES == True):
        print(f"ANS = {cfloat152_in}")
        logging.info("The given cfloat is a valid number")
    else:
        logging.error("The given cfloat number is not a valid input")
    
    if (CHECK_RES):
        bin_fp32 = fp32_bin(cfloat152_in)
        return bin_fp32
    else:
        sys.exit(1)

def main():
    cfloat_in = 2.0
    bias = 0

    convert_cfloat152_fp32(cfloat_in,bias,1)

main()