VSIM ?= iverilog

# ================================================================
# You should not have to change anything below this line

TOPFILE   ?= Testbench.bsv
TOPMODULE ?= mkTestbench

BSC_COMP_FLAGS = -elab -keep-fires -aggressive-conditions -no-warn-action-shadowing
BSC_LINK_FLAGS = -keep-fires
BSC_PATHS = -p %/Prelude:%/Libraries:./fp32_cfloat8/
# BSC_PATHS = -p %/Prelude:%/Libraries:/media/kapil/Kapil-Drive/xspi/
# BSC_PATHS = -p %/Prelude:%/Libraries:/home/kapil/Shakti-Software-Development/Mindgrove/devices-xspi/xspi/

BSIM_DIRS = -simdir build_bsim -bdir build_bsim -info-dir build_bsim
BSIM_EXE = $(TOPMODULE)_bsim

.PHONY: all_bsim
all_bsim: full_clean  compile  link    simulate

build_bsim:
	mkdir  build_bsim

.PHONY: compile
compile: build_bsim
	@echo Compiling for Bluesim ...
	bsc -u -sim $(BSIM_DIRS) $(BSC_COMP_FLAGS) $(BSC_PATHS) -g $(TOPMODULE)  $(TOPFILE) 
	@echo Compiling for Bluesim finished

.PHONY: link
link:
	@echo Linking for Bluesim ...
	bsc -e $(TOPMODULE) -sim -o $(BSIM_EXE) $(BSIM_DIRS) $(BSC_LINK_FLAGS) $(BSC_PATHS)
	@echo Linking for Bluesim finished

.PHONY: simulate
simulate:
	@echo Bluesim simulation ...
	./$(BSIM_EXE)  -V
	@echo Bluesim simulation finished

.PHONY: clean
clean:
	rm -f  build_bsim/*  build_v/*    *~

.PHONY: full_clean
full_clean:
	rm -r -f  build_bsim  build_v  verilog_dir  *~
	rm -f  *$(TOPMODULE)*  *.vcd

V_DIRS = -vdir verilog_dir -bdir build_v -info-dir build_v
VSIM_EXE = $(TOPMODULE)_vsim

.PHONY: all_vsim
all_vsim: full_clean  verilog  v_link  v_simulate

build_v:
	mkdir  build_v
verilog_dir:
	mkdir  verilog_dir

.PHONY: verilog
verilog: build_v  verilog_dir
	@echo Compiling for Verilog ...
	bsc -u -verilog $(V_DIRS) $(BSC_COMP_FLAGS) $(BSC_PATHS) -g $(TOPMODULE)  $(TOPFILE)
	@echo Compiling for Verilog finished

.PHONY: v_link
v_link:  build_v  verilog_dir
	@echo Linking for Verilog sim ...
	bsc -e $(TOPMODULE) -verilog -o ./$(VSIM_EXE) $(V_DIRS) -vsim $(VSIM)  verilog_dir/$(TOPMODULE).v
	@echo Linking for Verilog sim finished

.PHONY: v_simulate
v_simulate:
	@echo Verilog simulation...
	./$(VSIM_EXE)  +bscvcd
	@echo Verilog simulation finished
