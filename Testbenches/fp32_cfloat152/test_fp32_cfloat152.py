from pydoc import allmethods
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes 
import sys
from time import clock_getres
import cocotb
import random
import os
import logging as _log
from cocotb.binary import BinaryValue
from cocotb.clock import Clock
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, ReadOnly, FallingEdge
# from cocotb_bus.monitors import Monitor
# from cocotb_bus.drivers import BitDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
# from cocotb_bus.scoreboard import Scoreboard
from cocotb.result import TestFailure, TestSuccess
import numpy as np

sys.path.append("../../reference_model/")
import fp32_cfloat152 as fp_c


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

def conv_fp32_to_binary(n) : 
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

def generate_random_fp32 (size,low = 0.0,high = 1.0):
    random_float32_array = np.random.uniform(low, high, size=size).astype(np.float32)
    return random_float32_array


class TB: #defining Class TB 
    def __init__(self,dut):
        self.dut = dut

        cocotb.start_soon(Clock(dut.CLK,1,"ns").start()) #starting Clock to run concurrently to the tests

#Function to reset the DUT
    async def cycle_reset (self): 
        self.dut.RST_N.setimmediatevalue(0)
        await RisingEdge(self.dut.CLK)
        self.dut.RST_N.value = 0
        await RisingEdge(self.dut.CLK)
        self.dut.RST_N.value = 1
        await RisingEdge(self.dut.CLK)

#function to wait specified number of cycles
    async def cycle_wait (self,cycle): 
        for i in range(1,cycle):
            await RisingEdge(self.dut.CLK)

    async def input_dut (self,fp32_in,bias):
        self.dut._log.info("Providing input \n")
        self.dut.fp32_in_fp_in.value = int(fp32_in,2)
        self.dut.bias_in_bias.value  = bias 
        await RisingEdge(self.dut.CLK) 

    
    async def get_output (self):
        await RisingEdge(self.dut.CLK)
        await RisingEdge(self.dut.CLK)
        self.dut._log.info("Probing output\n")
        dut_output = self.dut.cfloat152_out.value
        return dut_output

    async def reference_model (self,fp32_in,bias):
        output_rm = fp_c.convert_fp32_cfloat152(fp32_in,bias)
        return output_rm
    

    def compare (self,output_dut,output_rm):
        print ('Output_dut  ',output_dut)
        print ('Output_rm   ',str(output_rm))
        print('\n')
        assert output_rm == str(output_dut) ,"Test Failed, rm and dut not matching"


@cocotb.test()
async def test_random_numbers_once(dut):
    tb=TB(dut)
    bias = 0


    size = 3

    # This particular configuration will cause a fail because the rounding was not taken
    # care when the number is less than the least denormal number
    low_limit = 0
    high_limit = 0.25
    np_fp32 = generate_random_fp32 (size,low_limit,high_limit)
    bin_fp32 = []
    fp32_in = []
    for i in range(size):
        
        bin_fp32.append(conv_fp32_to_binary(np_fp32[i].item()))
        fp32_in.append(np_fp32[i].item())
    # for i in range(size):
    #     print(fp32_in[i])
    #     output_rm = await tb.reference_model(fp32_in[i],bias)
    #     await tb.input_dut(bin_fp32[i],bias)
    #     output_dut = await tb.get_output()
    print(fp32_in[0])
    await tb.cycle_reset()
    output_rm = await tb.reference_model(fp32_in[0],bias)
    await tb.input_dut(bin_fp32[0],bias)
    output_dut = await tb.get_output()
    tb.compare(output_dut, output_rm) 




    

    


