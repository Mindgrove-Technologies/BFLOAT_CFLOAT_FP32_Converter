import numpy as np
import logging

logging.basicConfig(level=logging.WARNING)
fp32_in = 2.75
sign = 0

bias = 0
dict_n = {}
lst = []
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

logging.info(dict_n)
target_exponent = 0;
for e in range(1,32):
    if (fp32_in > dict_n[e][0] and fp32_in < dict_n[e][-1]):
        target_exponent = e;
    elif (fp32_in > dict_n[e][-1] and fp32_in < dict_n[e+1][0]):
        target_exponent = e;

before=0
after=0

# print("[DEBUG]",dict_n[target_exponent])
for i in range(4):
    if (fp32_in > dict_n[target_exponent][i]):
        # print("greater than",i)
        before = i
    elif (fp32_in < dict_n[target_exponent][i]):
        # print("less than",i)
        after=i
        break
    else:
        out=i
        
# print("[DEBUG]: exponent",target_exponent)
# print("[DEBUG]: before",before)
# print("[DEBUG]: after",after)
 
            
        
