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
import cfloat152_fp32 as fp_c

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
        self.dut.cfloat152_in_cfloat_in.value = int(cfloat_in,2)
        self.dut.bias_in_bias.value  = bias 
        await RisingEdge(self.dut.CLK) 

    
    async def get_output (self):
        await RisingEdge(self.dut.CLK)
        await RisingEdge(self.dut.CLK)
        self.dut._log.debug("Probing output\n")
        dut_output = self.dut.fp32_out.value
        return dut_output

    async def reference_model (self,cfloat_in,bias):
        output_rm = fp_c.convert_cfloat152_fp32(cfloat_in,bias)
        return output_rm
    

    def compare (self,output_dut,output_rm,cfloat_in,bias):
        self.dut._log.debug(f'Output_dut  {output_dut}')
        self.dut._log.debug(f'Output_rm   {str(output_rm)}')
        # print('\n')
        assert output_rm == str(output_dut) ,f"Test Failed, rm: {output_rm} and dut: {str(output_dut)} not matching for input: {cfloat_in} and bias: {bias}"

