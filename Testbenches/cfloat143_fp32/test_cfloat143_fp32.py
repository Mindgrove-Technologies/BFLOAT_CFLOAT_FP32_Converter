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
import cfloat143_fp32 as fp_c

def conv_cfloat_to_binary(sign,exponent, mantissa):
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

def generate_cfloat_num (sign, exponent, mantissa,bias):
    if (exponent != 0):
        value = ((-1) ** sign) * (2** (exponent - bias))
        if mantissa == 0:
            return value * 1
        elif mantissa == 1:
            return value * 1.125
        elif mantissa == 2:
            return value * 1.25
        elif mantissa == 3:
            return value * 1.375
        elif mantissa == 4:
            return value * 1.5
        elif mantissa == 5:
            return value * 1.625
        elif mantissa == 6:
            return value * 1.75
        else:
            return value * 1.875
    else:
        value = 2 ** (-bias) * ((-1) ** sign)
        if mantissa == 1:
            return value * 0.125
        elif mantissa == 2:
            return value * 0.25
        elif mantissa == 3:
            return value * 0.375
        elif mantissa == 4:
            return value * 0.500
        elif mantissa == 5:
            return value * 0.625
        elif mantissa == 6:
            return value * 0.750
        else:
            return value * 0.875

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

    async def input_dut (self,cfloat_in,bias):
        self.dut._log.debug("Providing input \n")
        self.dut.convert_cfloat143_fp32_cfloat143_in.value = int(cfloat_in,2)
        self.dut.convert_cfloat143_fp32_bias.value  = bias 
        await RisingEdge(self.dut.CLK) 

    
    async def get_output (self):
        await RisingEdge(self.dut.CLK)
        await RisingEdge(self.dut.CLK)
        self.dut._log.debug("Probing output\n")
        dut_output = self.dut.get_fp32.value
        return dut_output

    async def reference_model (self,cfloat_in,bias,neg_zero):
        output_rm = fp_c.convert_cfloat143_fp32(cfloat_in,bias,neg_zero)
        return output_rm
    

    def compare (self,output_dut,output_rm,cfloat_in,bias):
        self.dut._log.debug(f'Output_dut  {output_dut}')
        self.dut._log.debug(f'Output_rm   {str(output_rm)}')
        # print('\n')
        assert output_rm == str(output_dut) ,f"Test Failed, rm: {output_rm} and dut: {str(output_dut)} not matching for input: {cfloat_in} and bias: {bias}"

# @cocotb.test()
async def test_single_number(dut):
    tb = TB(dut)

    cfloat_in = 2.0

@cocotb.test()
async def test_all_zero(dut):
    tb = TB(dut)

    cfloat_in = 0.0
    neg_zero = 0
    exponent = 0
    mantissa = 0
    await tb.cycle_reset()
    # positive zero
    for bias in range(64):
        bin_cfloat = conv_cfloat_to_binary(neg_zero,exponent,mantissa)
        output_rm = await tb.reference_model(cfloat_in,bias,neg_zero)
        await tb.input_dut(bin_cfloat,bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut,output_rm,cfloat_in,bias)

    neg_zero = 1
    # Negative zero
    for bias in range(64):
        bin_cfloat = conv_cfloat_to_binary(neg_zero,exponent,mantissa)
        output_rm = await tb.reference_model(cfloat_in,bias,neg_zero)
        await tb.input_dut(bin_cfloat,bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut,output_rm,cfloat_in,bias)
    
    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_positive_normal_numbers_single_bias(dut):
    tb = TB(dut)
    sign = 0
    neg_zero = 0

    await tb.cycle_reset()

    iteration = 100000
    for i in range(iteration):
        exponent = random.randint(1,15)
        mantissa = random.randint(0,7)
        bias = random.randint(0,63)

    
        tb.dut._log.info(f"bias: {bias} exponenet: {exponent} mantissa: {mantissa}")
        cfloat_in = generate_cfloat_num(sign, exponent, mantissa, bias)
        bin_cfloat = conv_cfloat_to_binary(sign,exponent,mantissa)
        output_rm = await tb.reference_model(cfloat_in,bias,neg_zero)
        await tb.input_dut(bin_cfloat,bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut,output_rm,cfloat_in,bias)
    
    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_negative_normal_numbers_single_bias(dut):
    tb = TB(dut)
    sign = 1
    neg_zero = 0

    await tb.cycle_reset()

    iteration = 10000
    for i in range(iteration):
        exponent = random.randint(1,15)
        mantissa = random.randint(0,7)
        bias = random.randint(0,63)

        tb.dut._log.info(f"bias: {bias} exponenet: {exponent} mantissa: {mantissa}")
        cfloat_in = generate_cfloat_num(sign, exponent, mantissa, bias)
        # print(cfloat_in)
        bin_cfloat = conv_cfloat_to_binary(sign,exponent,mantissa)
        output_rm = await tb.reference_model(cfloat_in,bias,neg_zero)
        await tb.input_dut(bin_cfloat,bias)
        output_dut = await tb.get_output()
        tb.compare (output_dut,output_rm,cfloat_in,bias)
    
    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_positive_denormal_numbers_single_bias(dut):
    tb = TB(dut)
    sign = 0        
    exponent = 0
    mantissa = 0

    neg_zero = 0

    await tb.cycle_reset()
    # bias = random.randint(0,63
    for bias in range(0,64):
        for mantissa in range(1,8):
            # bias = 1
        
            tb.dut._log.info(f"bias: {bias} exponenet: {exponent} mantissa: {mantissa}")
            cfloat_in = generate_cfloat_num(sign, exponent, mantissa, bias)
            bin_cfloat = conv_cfloat_to_binary(sign,exponent,mantissa)
            output_rm = await tb.reference_model(cfloat_in,bias,neg_zero)
            await tb.input_dut(bin_cfloat,bias)
            output_dut = await tb.get_output()
            tb.compare (output_dut,output_rm,cfloat_in,bias)
    
    await tb.cycle_reset()
    await tb.cycle_wait(10)

@cocotb.test()
async def test_negative_denormal_numbers_single_bias(dut):
    tb = TB(dut)
    sign = 1        
    exponent = 0
    mantissa = 0

    neg_zero = 0

    await tb.cycle_reset()
    # bias = random.randint(0,63)
    for bias in range(0,64):
        for mantissa in range(1,8):
        
            tb.dut._log.info(f"bias: {bias} exponenet: {exponent} mantissa: {mantissa}")
            cfloat_in = generate_cfloat_num(sign, exponent, mantissa, bias)
            bin_cfloat = conv_cfloat_to_binary(sign,exponent,mantissa)
            output_rm = await tb.reference_model(cfloat_in,bias,neg_zero)
            await tb.input_dut(bin_cfloat,bias)
            output_dut = await tb.get_output()
            tb.compare (output_dut,output_rm,cfloat_in,bias)
    
    await tb.cycle_reset()
    await tb.cycle_wait(10)
