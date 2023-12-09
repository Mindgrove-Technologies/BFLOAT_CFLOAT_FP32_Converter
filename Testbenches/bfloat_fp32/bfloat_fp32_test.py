import torch
import sys
sys.path.append('../../reference_model')
import bfloat16_fp32 as b_f

from pydoc import allmethods
import sys
from time import clock_getres
import cocotb
import random
import os

from cocotb.binary import BinaryValue
import logging as _log
from cocotb.clock import Clock
from cocotb.decorators import coroutine
from cocotb.triggers import Timer, RisingEdge, ReadOnly, FallingEdge
# from cocotb_bus.monitors import Monitor
# from cocotb_bus.drivers import BitDriver
from cocotb.binary import BinaryValue
from cocotb.regression import TestFactory
# from cocotb_bus.scoreboard import Scoreboard
from cocotb.result import TestFailure, TestSuccess

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

#function to initialize the inputs to mme
	async def input_bfloat (self,bfloat_input): 
		await RisingEdge(self.dut.CLK)
		self.dut.bfloat16_in_bfloat_in.value = int(bfloat_input,2)

	async def get_float (self): 
		await RisingEdge(self.dut.CLK)
		await RisingEdge(self.dut.CLK)
		await RisingEdge(self.dut.CLK)
		bfloat_output = self.dut.fp32_out.value
		await RisingEdge(self.dut.CLK)
		await RisingEdge(self.dut.CLK)

		return bfloat_output


#Reference model with only encryption 
	async def model (self,bfloat_input,neg_zero):
		float_value = b_f.convert_bfloat16_fp32(bfloat_input,neg_zero)
		return float_value


	def compare(self,input,output_dut,output_rm): #function to compare the outputs recieved from Reference model and DUT
		print ('Input       ',input)
		print ('Output_dut  ',output_dut)
		print ('Output_rm   ', output_rm)
		print('\n')
		assert (output_rm == str(output_dut)) ,"Test Failed, rm and dut not matching"

# Driver Code
@cocotb.test()
async def custom_numbers_test(dut):
	tb=TB(dut)

	elemns = 1
	# bfloat_inp = torch.rand(elemns, dtype=torch.bfloat16)*24*7*193*(-1)

	bfloat_inp = -154112.0
	bfloat_inp = bfloat_inp + torch.Tensor([0])
	bfloat_inp.to(torch.bfloat16)

	bfloat_input = bfloat_inp.bfloat16()
	print(bfloat_input)
	
	bfloat_list = bfloat_inp.tolist()
	bfloat_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		bfloat_binary_temp = b_f.IEEE754(bfloat_list[i])
		bfloat_binary = bfloat_binary_temp[0:16]
		bfloat_list_binary.append(bfloat_binary)
		
	# print(bfloat_binary)
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		temp = bfloat_inp[i]
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()

@cocotb.test()
async def normal_numbers_test(dut):
	tb=TB(dut)

	elemns = 100000
	bfloat_inp = torch.rand(elemns, dtype=torch.bfloat16)*24*7*536
	bfloat_input = bfloat_inp.bfloat16()
	print(bfloat_input)
	
	bfloat_list = bfloat_inp.tolist()
	bfloat_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		bfloat_binary_temp = b_f.float_to_binary(bfloat_list[i])
		bfloat_binary = bfloat_binary_temp[0:16]
		bfloat_list_binary.append(bfloat_binary)
		
	# print(bfloat_binary)
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		temp = bfloat_inp[i]
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()

@cocotb.test()
async def negative_numbers_test(dut):
	tb=TB(dut)

	elemns = 100000
	bfloat_inp = torch.rand(elemns, dtype=torch.bfloat16)*24*7*193*(-1)
	bfloat_input = bfloat_inp.bfloat16()
	print(bfloat_input)
	
	bfloat_list = bfloat_inp.tolist()
	bfloat_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		bfloat_binary_temp = b_f.float_to_binary(bfloat_list[i])
		bfloat_binary = bfloat_binary_temp[0:16]
		bfloat_list_binary.append(bfloat_binary)
		
	# print(bfloat_binary)
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		temp = bfloat_inp[i]
		output_rm = await tb.model(temp,1)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()
		

@cocotb.test()
async def overflow_numbers_test(dut):
	tb=TB(dut)

	elemns = 1
	# bfloat_inp = torch.rand(elemns, dtype=torch.bfloat16)*24*7*193*199999999999

	bfloat_bin = '0111111101111111'

	bfloat_inp = b_f.convert_ieee_to_real(bfloat_bin+"0"*16)
	bfloat_inp = bfloat_inp + torch.Tensor([0])

	bfloat_input = bfloat_inp.bfloat16()
	print(bfloat_input)
	
	bfloat_list = bfloat_inp.tolist()
	bfloat_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		bfloat_binary_temp = b_f.IEEE754(bfloat_list[i])
		bfloat_binary = bfloat_binary_temp[0:16]
		bfloat_list_binary.append(bfloat_bin)
		
	# print(bfloat_binary)
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		temp = bfloat_inp[i]
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def underflow_numbers_test(dut):
	tb=TB(dut)

	elemns = 1
	bfloat_bin = "0000000010000000"
	
	bfloat_inp = b_f.convert_ieee_to_real(bfloat_bin+"0"*16)
	bfloat_inp = bfloat_inp + torch.Tensor([0])

	bfloat_input = bfloat_inp.bfloat16()
	print(bfloat_input)
	
	bfloat_list = bfloat_inp.tolist()
	bfloat_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		bfloat_binary_temp = b_f.IEEE754(bfloat_list[i])
		bfloat_binary = bfloat_binary_temp[0:16]
		bfloat_list_binary.append(bfloat_bin)
		
	# print(bfloat_binary)
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		temp = bfloat_inp[i]
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def qnan_test(dut):
	tb=TB(dut)

	elemns = 1

	bfloat_bin = '0111111111000001'

	bfloat_inp = b_f.convert_ieee_to_real(bfloat_bin)

	print(bfloat_inp)
	
	bfloat_list_binary = []
	
	for i in range(elemns):
		bfloat_list_binary.append(bfloat_bin)
		
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		output_rm = await tb.model(bfloat_inp,0)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def snan_test(dut):
	tb=TB(dut)

	elemns = 1

	bfloat_bin = '0111111110000001'

	bfloat_inp = b_f.convert_ieee_to_real(bfloat_bin)
	print(bfloat_inp)
	
	bfloat_list_binary = []
	
	for i in range(elemns):
		bfloat_list_binary.append(bfloat_bin)
		
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		temp = bfloat_inp
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def negative_qnan_test(dut):
	tb=TB(dut)

	elemns = 1

	bfloat_bin = '1111111111000001'

	bfloat_inp = b_f.convert_ieee_to_real(bfloat_bin)

	print(bfloat_inp)
	
	bfloat_list_binary = []
	
	for i in range(elemns):
		bfloat_list_binary.append(bfloat_bin)
		
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		output_rm = await tb.model(bfloat_inp,0)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def negative_snan_test(dut):
	tb=TB(dut)

	elemns = 1

	bfloat_bin = '1111111110000001'

	bfloat_inp = b_f.convert_ieee_to_real(bfloat_bin)
	print(bfloat_inp)
	
	bfloat_list_binary = []
	
	for i in range(elemns):
		bfloat_list_binary.append(bfloat_bin)
		
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		temp = bfloat_inp
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()



@cocotb.test()
async def zero_test(dut):
	tb=TB(dut)

	elemns = 10
	bfloat_inp = torch.rand(elemns, dtype=torch.bfloat16)*0
	bfloat_input = bfloat_inp.bfloat16()
	print(bfloat_input)
	
	bfloat_list = bfloat_inp.tolist()
	bfloat_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		bfloat_binary_temp = "0"*32
		bfloat_binary = bfloat_binary_temp[0:16]
		bfloat_list_binary.append(bfloat_binary)
		
	# print(bfloat_binary)
	print(bfloat_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_bfloat(bfloat_list_binary[i])
		temp = bfloat_inp[i]
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_float()

		tb.compare(bfloat_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()