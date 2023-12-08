'''**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************'''
import sys
import logging


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

def fp32_bin (n):
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
 
    # convert the binary to hexadecimal 
    hstr = '0x%0*X' %((len(final) + 3) // 4, int(final, 2)) 
    return final

def convert_cfloat152_fp32(cfloat152_in,bias,bin_ret):
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
    
    if (bin_ret == 1 and CHECK_RES):
        print(fp32_bin(cfloat152_in))
    else:
        sys.exit(1)

def main():
    cfloat_in = 2.0
    bias = 0

    convert_cfloat152_fp32(cfloat_in,bias,1)

main()