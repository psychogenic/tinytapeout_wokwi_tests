## SPDX-FileCopyrightText: © 2021 Uri Shaked <uri@wokwi.com>
## SPDX-License-Identifier: MIT
# See https://docs.cocotb.org/en/stable/quickstart.html for more info

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

export COCOTB_REDUCED_LOG_FMT=1

# WOKWI_PROJECT_ID : MUST be set in calling parent/env

ifneq ($(GATELEVEL),yes)
# normal simulation
VERILOG_SOURCES +=  $(wildcard src/*.v) test/test_wokwi.v
else
# gate level simulation requires some extra setup
COMPILE_ARGS    += -DGL_TEST
COMPILE_ARGS    += -DFUNCTIONAL
COMPILE_ARGS    += -DUSE_POWER_PINS
COMPILE_ARGS    += -DSIM
COMPILE_ARGS    += -DUNIT_DELAY=#1
VERILOG_SOURCES += $(PDK_ROOT)/sky130B/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/sky130B/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v

# the github action copies the gatelevel verilog from /runs/wokwi/results/final/verilog/gl/ 
VERILOG_SOURCES += $(wildcard src/*.v) $(PWD)/src/user_module.gl.v
endif

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
TOPLEVEL = test_wokwi

# MODULE is the basename of the Python test file
MODULE = test.test_wokwi

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim

