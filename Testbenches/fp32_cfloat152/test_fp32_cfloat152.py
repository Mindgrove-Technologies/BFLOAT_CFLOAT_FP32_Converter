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
import struct

sys.path.append("../../reference_model/")
import fp32_cfloat152 as fp_c



def conv_fp32_to_binary(float32_array):
    binary_list = []

    for value in float32_array:
        # Convert float32 to IEEE 754 binary representation
        binary_representation = struct.pack('>f', value)
        
        # Convert binary to a list of 32 bits (0s and 1s)
        bits = [format(byte, '08b') for byte in binary_representation]
        
        # Combine the bits into a single string
        binary_string = ''.join(bits)
        
        # Append the binary string to the list
        binary_list.append(binary_string)

    return binary_list


def generate_random_fp32 (size,low = 0.0,high = 1.0):
    random_float32_array = np.random.uniform(low, high, size=size).astype(np.float32)
    return random_float32_array


class TB: #defining Class TB 
    def __init__(self,dut):
        self.dut = dut
        self.dut._log.setLevel(_log.INFO)
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
        self.dut._log.debug("Providing input \n")
        self.dut.fp32_in_fp_in.value = int(fp32_in,2)
        self.dut.bias_in_bias.value  = bias 
        await RisingEdge(self.dut.CLK) 

    
    async def get_output (self):
        await RisingEdge(self.dut.CLK)
        await RisingEdge(self.dut.CLK)
        self.dut._log.debug("Probing output\n")
        dut_output = self.dut.cfloat152_out.value
        return dut_output

    async def reference_model (self,fp32_in,bias,neg_zero):
        output_rm = fp_c.convert_fp32_cfloat152(fp32_in,bias,neg_zero)
        return output_rm
    

    def compare (self,output_dut,output_rm,fp32_in,bias):
        self.dut._log.debug(f'Output_dut  {output_dut}')
        self.dut._log.debug(f'Output_rm   {str(output_rm)}')
        # print('\n')
        assert output_rm == str(output_dut) ,f"Test Failed, rm: {output_rm} and dut: {str(output_dut)} not matching for input: {fp32_in} and bias: {bias}"


# @cocotb.test()
async def test_single_num(dut):
    tb =TB(dut)

    neg_zero = 0
    bias = 0
    fp32_in = 0.00000719332956578000448644161224365234375
    # fp32_in = 0.02
    # fp32_in = 0.34375
    print(fp32_in)
    await tb.cycle_reset()
    bin_fp32 = conv_fp32_to_binary(fp32_in)
    print(bin_fp32)
    output_rm = await tb.reference_model(fp32_in,bias,neg_zero)
    await tb.input_dut (bin_fp32,bias)
    output_dut = await tb.get_output()
    tb.compare (output_dut, output_rm,fp32_in,bias)


    await tb.cycle_reset()
    await tb.cycle_wait(10)


@cocotb.test()
async def test_zero_for_all_bias(dut):
    tb =TB(dut)

    
    fp32_in = 0.0
    await tb.cycle_reset()
    # sign bit 0
    for bias in range(64):
        neg_zero = 0
        bin_fp32 = "0"*32
        output_rm = await tb.reference_model(fp32_in,bias,neg_zero)
        await tb.input_dut (bin_fp32,bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut, output_rm,fp32_in,bias)

    # sign bit 1
    for bias in range(64):
        neg_zero = 1
        bin_fp32 = "1" + "0"*31
        output_rm = await tb.reference_model(fp32_in,bias,neg_zero)
        await tb.input_dut (bin_fp32,bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut, output_rm,fp32_in,bias) 

    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_positive_overflow(dut):
    tb =TB(dut)

    neg_zero = 0
    bias = random.randint(0, 63)
    # bias = 36
    size = 1
    i= 0
    max_cfloat = (2**(31-bias)) * 1.75
    low_limit = max_cfloat+1
    high_limit = max_cfloat + 2

    print(f"[INFO] : Random Bias used is {bias}")
    np_fp32 = generate_random_fp32 (size,low_limit,high_limit)
    bin_fp32 = conv_fp32_to_binary(np_fp32)
    
    await tb.cycle_reset()
    output_rm = await tb.reference_model(np_fp32[i],bias,neg_zero)
    await tb.input_dut (bin_fp32[i],bias)
    output_dut = await tb.get_output()
    tb.compare (output_dut, output_rm,np_fp32[i],bias)


    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_negative_overflow(dut):
    tb =TB(dut)

    neg_zero = 0
    bias = random.randint(0, 63)
    # bias = 36
    size = 1
    i= 0
    max_cfloat = (2**(31-bias)) * 1.75
    low_limit = - (max_cfloat+1)
    high_limit = - (max_cfloat + 2)

    print(f"[INFO] : Random Bias used is {bias}")
    np_fp32 = generate_random_fp32 (size,low_limit,high_limit)
    bin_fp32 = conv_fp32_to_binary(np_fp32)

    await tb.cycle_reset()
    output_rm = await tb.reference_model(np_fp32[i],bias,neg_zero)
    await tb.input_dut (bin_fp32[i],bias)
    output_dut = await tb.get_output()
    tb.compare (output_dut, output_rm,np_fp32[i],bias)

@cocotb.test()
async def test_positive_underflow(dut):
    tb =TB(dut)

    neg_zero = 0
    bias = random.randint(0, 63)

    size = 10000
    low_limit = 0.0
    high_limit = (2**(1-bias)) * 1
    np_fp32 = generate_random_fp32 (size,low_limit,high_limit)
    bin_fp32 = conv_fp32_to_binary(np_fp32)
    await tb.cycle_reset()
    for i in range(size):
        output_rm = await tb.reference_model(np_fp32[i],bias,neg_zero)
        await tb.input_dut (bin_fp32[i],bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut, output_rm,np_fp32[i],bias)

    print(f"[INFO] : Random Bias used is {bias}")
    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_negative_underflow(dut):
    tb =TB(dut)

    neg_zero = 0
    bias = random.randint(0, 63)


    size = 10
    low_limit = 0.0
    high_limit = -((2**(1-bias)) * 1)
    np_fp32 = generate_random_fp32 (size,low_limit,high_limit)
    bin_fp32 = conv_fp32_to_binary(np_fp32)
    await tb.cycle_reset()
    for i in range(size):
        output_rm = await tb.reference_model(np_fp32[i],bias,neg_zero)
        await tb.input_dut (bin_fp32[i],bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut, output_rm,np_fp32[i],bias)

    print(f"[INFO] : Random Bias used is {bias}")
    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_positive_normal_numbers_single_bias(dut):
    tb =TB(dut)

    neg_zero = 0
    bias = random.randint(0, 63)


    size = 10000
    low_limit = ((2 ** (1-bias)) * 1)
    high_limit = ((2**(31-bias)) * 1.75)
    np_fp32 = generate_random_fp32 (size,low_limit,high_limit)
    bin_fp32 = conv_fp32_to_binary(np_fp32)
    await tb.cycle_reset()
    for i in range(size):
        output_rm = await tb.reference_model(np_fp32[i],bias,neg_zero)
        await tb.input_dut (bin_fp32[i],bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut, output_rm,np_fp32[i],bias)

    print(f"[INFO] : Random Bias used is {bias}")
    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_positive_normal_numbers_all_bias(dut):
    tb =TB(dut)

    neg_zero = 0
    for bias in range(64):
        size = 10
        low_limit = ((2 ** (1-bias)) * 1)
        high_limit = ((2**(31-bias)) * 1.75)
        np_fp32 = generate_random_fp32 (size,low_limit,high_limit)
        bin_fp32 = conv_fp32_to_binary(np_fp32)
        await tb.cycle_reset()
        for i in range(size):
            output_rm = await tb.reference_model(np_fp32[i],bias,neg_zero)
            await tb.input_dut (bin_fp32[i],bias)
            output_dut = await tb.get_output()
            tb.compare (output_dut, output_rm,np_fp32[i],bias)

    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_negative_normal_numbers_single_bias(dut):
    tb =TB(dut)

    neg_zero = 0
    bias = random.randint(0, 63)


    size = 10000
    low_limit = - ((2 ** (1-bias)) * 1)
    high_limit = - ((2**(31-bias)) * 1.75)
    np_fp32 = generate_random_fp32 (size,low_limit,high_limit)
    bin_fp32 = conv_fp32_to_binary(np_fp32)
    await tb.cycle_reset()
    for i in range(size):
        output_rm = await tb.reference_model(np_fp32[i],bias,neg_zero)
        await tb.input_dut (bin_fp32[i],bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut, output_rm,np_fp32[i],bias)

    print(f"[INFO] : Random Bias used is {bias}")
    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_negative_normal_numbers_all_bias(dut):
    tb =TB(dut)

    neg_zero = 0
    for bias in range(64):
        size = 10
        low_limit = - ((2 ** (1-bias)) * 1)
        high_limit = - ((2**(31-bias)) * 1.75)
        np_fp32 = generate_random_fp32 (size,low_limit,high_limit)
        bin_fp32 = conv_fp32_to_binary(np_fp32)
        await tb.cycle_reset()
        for i in range(size):
            # print(np_fp32[i])
            output_rm = await tb.reference_model(np_fp32[i],bias,neg_zero)
            await tb.input_dut (bin_fp32[i],bias)
            output_dut = await tb.get_output()
            tb.compare (output_dut, output_rm,np_fp32[i],bias)

    await tb.cycle_reset()
    await tb.cycle_wait(10)






    

    


