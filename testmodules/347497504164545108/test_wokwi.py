'''

7-seg display testbench
WOKWI_PROJECT_ID: 347497504164545108


SPDX-FileCopyrightText: © 2023 Pat Deegan, https://psychogenic.com
SPDX-License-Identifier: Apache2.0
'''

import os
import cocotb
import test.common.truthtable as truthtable

@cocotb.test()
async def truthTableCompare(parentDUT):
    usermodule = parentDUT.dut
    i_bus = parentDUT.io_in
    o_bus = parentDUT.io_out
    tt = truthtable.loadSimpleTruthTable('test/truthtable.txt')
    await tt.testAll(i_bus, o_bus, usermodule._log)
