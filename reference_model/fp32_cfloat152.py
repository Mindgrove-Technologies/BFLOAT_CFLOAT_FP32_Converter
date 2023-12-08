import sys
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

# Temporary variables
# fp32_in = 3.75
fp32_in = 3758096385.0
bias = 1
###################

dict_n = {}
dict_d = {}
lst = []
target_exponent = 0
inside_list = 0
before=0
after=0
output=0
CONV_DONE=False
flags_zero = 0
flags_denormal = 0
#################################

logging.info("Initiallizing the dictionary with all normal numbers possible for the given bias")
for e in range(1,32):
    dict_n[e]=list();

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
        

logging.debug(f"[NORMAL],{dict_n}")
logging.debug(f"[DENORMAL],{dict_d}")
logging.info("Checking if the given fp32 is within limits of the cfloat152")
#Zero Conditon
if (fp32_in == 0):
    flags_zero = 1
    CONV_DONE = True
# Overflow condition
elif (fp32_in > dict_n[31][-1]):
    CONV_DONE = True
    target_exponent = 31
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
    else:
        if (fp32_in >= dict_d[1] and fp32_in ):
    
else:
    # Normal Numbers
    for e in range(1,32):
        if (dict_n[e][0] <= fp32_in <= dict_n[e][-1]):
            target_exponent = e
            inside_list = 1
        elif (dict_n[e][-1] < fp32_in < dict_n[e+1][0]):
            target_exponent = e
            inside_list = 0



    # print("[DEBUG]",dict_n[target_exponent])
    if (inside_list):
        for i in range(4):
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
            print(dict_n[target_exponent][before] + (DIFF/2))
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
        CFLOAT152 = 0
    elif (flags_denormal == 1):
        CFLOAT152 = dict_d[target_denormal]
    else:
        CFLOAT152 = dict_n[target_exponent][output]
else:
    logging.error("Conversion is not done")
    sys.exit()
    

print("ANSWER =",CFLOAT152)
        
        
        
        
# print("[DEBUG]: exponent",target_exponent)
# print("[DEBUG]: before",before)
# print("[DEBUG]: after",after)
 
            
        
