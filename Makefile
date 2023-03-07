# Automated wokwi project testing helper makefile
# Copyright (C) 2023 Pat Deegan
#
# 
# You need only
#  
#   WOKWI_PROJECT_ID=ABC123 make runtest
#
# and the project will be downloaded, configured and testbench run
# 
# Assumes
#	- some PROCESSING_DIR to work in (proj/ by default)
#	- a PROJ_TPLDIR to use as a template for wokwi projects
#	- a TESTMODULES_DIR with cocotb testbench code in
#		 TESTMODULES_DIR/WOKWI_PROJECT_ID sub-directories
# 
# Useful targets include
#    
#    make yosys_shell
#    make show_module
#    make show_truthtable
#
# 
# SPDX-FileCopyrightText: © 2023 Pat Deegan, https://psychogenic.com
# SPDX-License-Identifier: Apache2.0


WOKWI_PROJECT_ID ?= 347497504164545108
PROJ_TPLDIR ?= tt03-submission-template-main

PROCESSING_DIR := proj
PROJ_DIR := $(PROCESSING_DIR)/$(WOKWI_PROJECT_ID)
TESTMODULES_DIR := testmodules


# test modules stashed in TESTMODULES_DIR/WOKWI_PROJECT_ID...
HAVE_TESTS=$(wildcard $(TESTMODULES_DIR)/$(WOKWI_PROJECT_ID)/*)

# gen'ed user config file
USER_CONFIG := $(PROJ_DIR)/src/user_config.tcl

USERMODULE_NAME := user_module_$(WOKWI_PROJECT_ID)


export COCOTB_RESOLVE_X=ONES


$(PROJ_TPLDIR):
	git clone https://github.com/TinyTapeout/tt03-submission-template.git $(PROJ_TPLDIR)
	perl -pi -e 's/wokwi_id:\s*0/wokwi_id: XXXWOKWI_IDXXX/smg' $(PROJ_TPLDIR)/info.yaml
	cp submission/Makefile $(PROJ_TPLDIR)
	mkdir -p $(PROJ_TPLDIR)/test 
	cp -R submission/test/* $(PROJ_TPLDIR)/test 


tt:
	git clone https://github.com/TinyTapeout/tt-support-tools.git tt
	pip install -r tt/requirements.txt

	


$(PROJ_DIR): tt $(PROJ_TPLDIR)
	mkdir -p $(PROCESSING_DIR)

	cp -Ra $(PROJ_TPLDIR) $(PROJ_DIR)
	
	perl -pi -e "s|XXXWOKWI_IDXXX|$(WOKWI_PROJECT_ID)|smg" \
	     $(PROJ_DIR)/info.yaml $(PROJ_DIR)/test/test_wokwi.v
	cp -Ra tt $(PROJ_DIR)


copytests: 
	@if [ "x$(HAVE_TESTS)" = "x" ]; then echo "no tests..?"; \
		else cp $(HAVE_TESTS) $(PROJ_DIR)/test/; \
		cp -R $(TESTMODULES_DIR)/common $(PROJ_DIR)/test/ ;\
	fi
	

$(USER_CONFIG): $(PROJ_DIR)
	cd $(PROJ_DIR) && (./tt/tt_tool.py --create-user-config)



init: $(USER_CONFIG) 
	
runtest: init copytests
	cd $(PROJ_DIR) && $(MAKE) sim
	


YSYS_TRUTHTABLE_SHOW ?= io_out

YSYS_READVLOG := read_verilog src/cells.v; read_verilog src/$(USERMODULE_NAME).v; hierarchy; proc
YSYS_SHOW_MODULE := show -colors 3 $(USERMODULE_NAME)
YSYS_SHOW_INPATH := show -colors 3 n:io_in %co*
YSYS_TTABLE_EVAL := eval -set-undef -table io_in -show $(YSYS_TRUTHTABLE_SHOW) $(USERMODULE_NAME)

yosys_shell: init 
	cd $(PROJ_DIR) && yosys -p '$(YSYS_READVLOG); shell'

show_module: init
	cd $(PROJ_DIR) && yosys -p '$(YSYS_READVLOG); $(YSYS_SHOW_MODULE); shell'

show_ioin: init
	cd $(PROJ_DIR) && yosys -p '$(YSYS_READVLOG); $(YSYS_SHOW_INPATH); shell'

show_truthtable: init
	cd $(PROJ_DIR) && yosys -p '$(YSYS_READVLOG); opt; flatten; $(YSYS_TTABLE_EVAL)'
	
