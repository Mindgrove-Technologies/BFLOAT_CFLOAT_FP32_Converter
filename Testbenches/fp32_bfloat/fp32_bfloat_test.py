'''**********************************************
 Author: Rohit Srinivas R G, M Kapil Shyam
 Email: CS23Z002@smail.iitm.ac.in, CS23Z064@smail.iitm.ac.in
**********************************************'''

import torch
import sys
sys.path.append('../../reference_model')
import fp32_bfloat16 as f_b

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
	async def input_fp32 (self,fp32_input): 
		await RisingEdge(self.dut.CLK)
		self.dut.fp32_in_fp_in.value = int(fp32_input,2)

	async def get_bfloat (self): 
		await RisingEdge(self.dut.CLK)
		await RisingEdge(self.dut.CLK)
		await RisingEdge(self.dut.CLK)
		bfloat_output = self.dut.bfloat16_out.value
		await RisingEdge(self.dut.CLK)
		await RisingEdge(self.dut.CLK)

		return bfloat_output


#Reference model with only encryption 
	async def model (self,fp32_input, neg_zero):
		bfloat_value = f_b.convert_fp32_bfloat16(fp32_input,neg_zero)
		return bfloat_value


	def compare(self,input,output_dut,output_rm): #function to compare the outputs recieved from Reference model and DUT
		print ('Input       ',input)
		print ('Output_dut  ',output_dut)
		print ('Output_rm   ', output_rm)
		print('\n')
		assert output_rm == str(output_dut) ,"Test Failed, rm and dut not matching"

# Driver Code
@cocotb.test()
async def custom_numbers_test(dut):
	tb=TB(dut)

	elemns = 1
	# fp32_inp = torch.rand(elemns, dtype=torch.float32)*24*7*953*(-1)

	# fp32_inp = -36603.7578125
	fp32_inp = -154112.0
	fp32_inp = fp32_inp + torch.Tensor([0])
	fp32_inp.to(torch.float32)

	fp32_input = fp32_inp.float()
	print(fp32_input)
	
	float_list = fp32_inp.tolist()
	float_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		fp32_binary = f_b.IEEE754(float_list[i])
		float_list_binary.append(f_b.IEEE754(float_list[i]))
		
	# print(fp32_binary)
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_inp[i]
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def normal_numbers_test(dut):
	tb=TB(dut)

	elemns = 10
	fp32_inp = torch.rand(elemns, dtype=torch.float32)*24*7*998

	fp32_input = fp32_inp.float()
	print(fp32_input)
	
	float_list = fp32_inp.tolist()
	float_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		fp32_binary = f_b.IEEE754(float_list[i])
		float_list_binary.append(f_b.IEEE754(float_list[i]))
		
	# print(fp32_binary)
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_inp[i]
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()

@cocotb.test()
async def negative_numbers_test(dut):
	tb=TB(dut)

	elemns = 10
	fp32_inp = torch.rand(elemns, dtype=torch.float32)*24*7*953*(-1)

	fp32_input = fp32_inp.float()
	print(fp32_input)
	
	float_list = fp32_inp.tolist()
	float_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		fp32_binary = f_b.IEEE754(float_list[i])
		float_list_binary.append(f_b.IEEE754(float_list[i]))
		
	# print(fp32_binary)
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_inp[i]
		output_rm = await tb.model(temp,1)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def overflow_numbers_test(dut):
	tb=TB(dut)

	elemns = 1
	# fp32_inp = torch.rand(elemns, dtype=torch.float32)*24*7*953*19999999999

	fp32_bin = '01111111011111111111111111111111'

	fp32_inp = f_b.convert_ieee_to_real(fp32_bin)
	fp32_inp = fp32_inp + torch.Tensor([0])
	fp32_inp.to(torch.float32)

	fp32_input = fp32_inp.float()
	print(fp32_input)
	
	float_list = fp32_inp.tolist()
	float_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		fp32_binary = f_b.IEEE754(float_list[i])
		float_list_binary.append(fp32_bin)
		
	# print(fp32_binary)
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_input
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def underflow_numbers_test(dut):
	tb=TB(dut)

	start_bin = '00000000000000000000000000000001'
	end_bin = '00000000000000000111111111111111'

	start_dec = int(start_bin, 2)  # Convert binary string to decimal
	end_dec = int(end_bin, 2)  # Convert binary string to decimal

	float_list_binary = []
	count = 0

	# Iterate through the range of decimal numbers and print their binary equivalents
	for i in range(start_dec, end_dec + 1):
		binary = format(i, '032b')  # Convert decimal to 32-bit binary string
		# print(binary)
		fp32_bin = binary		
		fp32_inp = f_b.convert_ieee_to_real(fp32_bin)
		fp32_inp = fp32_inp + torch.Tensor([0])
		fp32_inp.to(torch.float32)
		float_list_binary.append(fp32_bin)
		count = count + 1

	# elemns = count
	elemns = 1

	fp32_input = fp32_inp.float()
	# print(fp32_input)
	
	float_list = fp32_inp.tolist()
		
	# print(fp32_binary)
	# print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_inp
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()

@cocotb.test()
async def negative_overflow_numbers_test(dut):
	tb=TB(dut)

	elemns = 1
	# fp32_inp = torch.rand(elemns, dtype=torch.float32)*24*7*953*19999999999

	fp32_bin = '11111111011111111111111111111111'

	fp32_inp = f_b.convert_ieee_to_real(fp32_bin)
	fp32_inp = fp32_inp + torch.Tensor([0])
	fp32_inp.to(torch.float32)

	fp32_input = fp32_inp.float()
	print(fp32_input)
	
	float_list = fp32_input.tolist()
	float_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		fp32_binary = f_b.IEEE754(float_list[i])
		float_list_binary.append(fp32_bin)
		
	# print(fp32_binary)
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_inp[i]
		output_rm = await tb.model(temp,1)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def negative_underflow_numbers_test(dut):
	tb=TB(dut)

	start_bin = '10000000000000000000000000000001'
	end_bin = '10000000000000000111111111111111'

	start_dec = int(start_bin, 2)  # Convert binary string to decimal
	end_dec = int(end_bin, 2)  # Convert binary string to decimal

	float_list_binary = []
	count = 0

	# Iterate through the range of decimal numbers and print their binary equivalents
	for i in range(start_dec, end_dec + 1):
		binary = format(i, '032b')  # Convert decimal to 32-bit binary string
		# print(binary)
		fp32_bin = binary		
		fp32_inp = f_b.convert_ieee_to_real(fp32_bin)
		fp32_inp = fp32_inp + torch.Tensor([0])
		fp32_inp.to(torch.float32)
		float_list_binary.append(fp32_bin)
		count = count + 1

	# elemns = count
	elemns = 1

	fp32_input = fp32_inp.float()
	print(fp32_input)
	
	float_list = fp32_inp.tolist()
		
	# print(fp32_binary)
	# print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_inp
		output_rm = await tb.model(temp,1)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def qnan_test(dut):
	tb=TB(dut)

	elemns = 1

	fp32_bin = '01111111110000000000000000000001'

	fp32_inp = f_b.convert_ieee_to_real(fp32_bin)

	print(fp32_inp)
	
	float_list_binary = []
	
	for i in range(elemns):
		float_list_binary.append(fp32_bin)
		
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		output_rm = await tb.model(fp32_inp,0)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def snan_test(dut):
	tb=TB(dut)

	elemns = 1

	fp32_bin = '01111111100000000000000000000001'

	fp32_inp = f_b.convert_ieee_to_real(fp32_bin)
	print(fp32_inp)
	
	float_list_binary = []
	
	for i in range(elemns):
		float_list_binary.append(fp32_bin)
		
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_inp
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def negative_qnan_test(dut):
	tb=TB(dut)

	elemns = 1

	fp32_bin = '11111111110000000000000000000001'

	fp32_inp = f_b.convert_ieee_to_real(fp32_bin)

	print(fp32_inp)
	
	float_list_binary = []
	
	for i in range(elemns):
		float_list_binary.append(fp32_bin)
		
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		output_rm = await tb.model(fp32_inp,1)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def negative_snan_test(dut):
	tb=TB(dut)

	elemns = 1

	fp32_bin = '11111111100000000000000000000001'

	fp32_inp = f_b.convert_ieee_to_real(fp32_bin)
	print(fp32_inp)
	
	float_list_binary = []
	
	for i in range(elemns):
		float_list_binary.append(fp32_bin)
		
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_inp
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()


@cocotb.test()
async def zero_test(dut):
	tb=TB(dut)

	elemns = 10
	fp32_inp = torch.rand(elemns, dtype=torch.float32)*0

	fp32_input = fp32_inp.float()
	print(fp32_input)
	
	float_list = fp32_inp.tolist()
	float_list_binary = []
	
		# print(float_list)
	for i in range(elemns):
		fp32_binary = "0"*32
		float_list_binary.append(fp32_binary)
		
	# print(fp32_binary)
	print(float_list_binary)

	for i in range(elemns):
		await tb.cycle_reset()
		await tb.input_fp32(float_list_binary[i])
		temp = fp32_input[i]
		output_rm = await tb.model(temp,0)
		output_dut = await tb.get_bfloat()

		tb.compare(float_list_binary[i],output_dut,output_rm)
		await tb.cycle_wait(5)
		await tb.cycle_reset()