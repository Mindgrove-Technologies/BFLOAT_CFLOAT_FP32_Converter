TOPLEVEL_LANG ?= verilog
SIM = verilator

PWD=$(shell pwd)

#export PYTHONPATH := $(PWD)/../model:$(PYTHONPATH)

ifeq ($(TOPLEVEL_LANG),verilog)
  VERILOG_SOURCES =$(PWD)/../../verilog_dir/mk_fp32_bfloat16.v

else
  $(error "A valid value (verilog) was not provided for TOPLEVEL_LANG=$(TOPLEVEL_LANG)")
endif

EXTRA_ARGS += --trace-structs --trace-fst

TOPLEVEL := mk_fp32_bfloat16
MODULE   := fp32_bfloat_test

include $(shell cocotb-config --makefiles)/Makefile.sim