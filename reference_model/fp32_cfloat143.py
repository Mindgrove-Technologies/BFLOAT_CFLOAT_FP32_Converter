'''**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************'''
import sys
import logging


###################
def cfloat_bin(sign,exponent, mantissa):
    bin_sign = str(sign)
    bin_exponent = bin(exponent)[2:].zfill(4)
    if (mantissa == 0):
        bin_mantissa = "000"
    elif (mantissa == 1):
        bin_mantissa = "001"
    elif (mantissa == 2):
        bin_mantissa = "010"
    elif (mantissa == 3):
        bin_mantissa = "011"
    elif (mantissa == 4):
        bin_mantissa = "100"
    elif (mantissa == 5):
        bin_mantissa = "101"
    elif (mantissa == 6):
        bin_mantissa = "110"
    else:
        bin_mantissa = "111"

    bin_cfloat = bin_sign + bin_exponent + bin_mantissa
    return bin_cfloat



def convert_fp32_cfloat143(fp32_in, bias , neg_zero):
    dict_n = {}
    dict_d = {}
    target_exponent = 0
    inside_list = 0
    before=0
    after=0
    output=0
    CONV_DONE=False
    flags_zero = 0
    flags_denormal = 0
    sign = 0

    
    #################################

    logging.info("Initiallizing the dictionary with all normal numbers possible for the given bias")
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
            

    logging.debug(f"[NORMAL],{dict_n}")
    logging.debug(f"[DENORMAL],{dict_d}")
    logging.info("Checking if the given fp32 is within limits of the cfloat143")
    if (fp32_in < 0 or (fp32_in == 0 and neg_zero == 1)):
        sign = 1
        fp32_in = -(fp32_in)
    else:
        sign = 0
    #Zero Conditon
    if (fp32_in == 0):
        flags_zero = 1
        CONV_DONE = True
    # Overflow condition
    elif (fp32_in > dict_n[15][-1]):
        CONV_DONE = True
        target_exponent = 15
        output = -1
        logging.warning("Overflow Detected")
    elif (fp32_in < dict_n[1][0]):
        logging.warning("Underflow Detected")
        if (fp32_in < dict_d[1]):
            DIFF = dict_d[1] - 0
            if (fp32_in >= (DIFF/2)):
                flags_denormal = 1
                target_denormal = 1
            else:
                flags_zero = 1
        elif (dict_d [1] <= fp32_in < dict_d[2]):
            DIFF = dict_d[2] - dict_d[1]
            flags_denormal = 1
            if (fp32_in >= dict_d[1] + (DIFF/2)):
                target_denormal = 2
            else:
                target_denormal = 1
        elif (dict_d [2] <= fp32_in < dict_d[3]):
            DIFF = dict_d[3] - dict_d[2]
            flags_denormal = 1
            if (fp32_in >= dict_d[2] + (DIFF/2)):
                target_denormal = 3
            else:
                target_denormal = 2
        elif (dict_d [3] <= fp32_in < dict_d[4]):
            DIFF = dict_d[4] - dict_d[3]
            flags_denormal = 1
            if (fp32_in >= dict_d[3] + (DIFF/2)):
                target_denormal = 4
            else:
                target_denormal = 3
        elif (dict_d [4] <= fp32_in < dict_d[5]):
            DIFF = dict_d[5] - dict_d[4]
            flags_denormal = 1
            if (fp32_in >= dict_d[4] + (DIFF/2)):
                target_denormal = 5
            else:
                target_denormal = 4
        elif (dict_d [5] <= fp32_in < dict_d[6]):
            DIFF = dict_d[6] - dict_d[5]
            flags_denormal = 1
            if (fp32_in >= dict_d[5] + (DIFF/2)):
                target_denormal = 6
            else:
                target_denormal = 5
        elif (dict_d [6] <= fp32_in < dict_d[7]):
            DIFF = dict_d[7] - dict_d[6]
            flags_denormal = 1
            if (fp32_in >= dict_d[6] + (DIFF/2)):
                target_denormal = 7
            else:
                target_denormal = 6
        elif (dict_d [7] <= fp32_in < dict_n[1][0]):
            DIFF = dict_n[1][0] - dict_d[7]
            if (fp32_in >= dict_d[7] + (DIFF/2)):
                target_exponent = 1
                output = 0
            else:
                flags_denormal = 1
                target_denormal = 7
        else:
            logging.error ("NOT POSSIBLE CONDITION")
        CONV_DONE = True
    else:
        # Normal Numbers
        for e in range(1,16):
            if (dict_n[e][0] <= fp32_in <= dict_n[e][-1]):
                target_exponent = e
                inside_list = 1
            elif (dict_n[e][-1] < fp32_in < dict_n[e+1][0]):
                target_exponent = e
                inside_list = 0



        # print("[DEBUG]",dict_n[target_exponent])
        if (inside_list):
            for i in range(8):
                if (fp32_in > dict_n[target_exponent][i]):
                    before = i
                elif (fp32_in < dict_n[target_exponent][i]):
                    after=i
                    break
                else:
                    logging.info("Found the match")
                    CONV_DONE = True
                    output=i
                    break

            if(not CONV_DONE):
                logging.info("Performing Rounding")
                DIFF = dict_n[target_exponent][after] - dict_n[target_exponent][before]
                # print(dict_n[target_exponent][before] + (DIFF/2))
                if (fp32_in >= (dict_n[target_exponent][before] + (DIFF/2))):
                    logging.debug("Rounding Needed")
                    output = after
                else:
                    logging.debug("No Rounding Needed")
                    output = before
                CONV_DONE = True

        else:
            DIFF = dict_n[target_exponent+1][0] - dict_n[target_exponent][-1]
            if fp32_in >= dict_n[target_exponent][-1] + (DIFF/2):
                target_exponent += 1
                output = 0
            else:
                output = -1
            CONV_DONE = True


    if(CONV_DONE):
        logging.info("Generating Answer")
        if (flags_zero == 1):
            CFLOAT143 = 0
        elif (flags_denormal == 1):
            CFLOAT143 = dict_d[target_denormal]
        else:
            CFLOAT143 = dict_n[target_exponent][output]
        if (sign == 1):
            CFLOAT143 = (-CFLOAT143)
    else:
        logging.error("Conversion is not done")
        sys.exit()

    # print("ANSWER =",CFLOAT143)
    if (flags_zero == 1):
        bin_out = cfloat_bin(sign, 0, 0)
    elif (flags_denormal == 1):
        bin_out = cfloat_bin(sign, 0, target_denormal)
    else:
        bin_out = cfloat_bin(sign,target_exponent,output)
    return bin_out

def main():
    logging.basicConfig(level=logging.INFO)
    fp32_in = -128.250
    bias = 0
    print(convert_fp32_cfloat143(fp32_in, bias,1))
        
main()
        
# print("[DEBUG]: exponent",target_exponent)
# print("[DEBUG]: before",before)
# print("[DEBUG]: after",after)
 
            
        
