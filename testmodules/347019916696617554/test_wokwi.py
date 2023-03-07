'''

padlock puzzle testbench
(C) 2023 Pat Deegan, https://psychogenic.com

WOKWI_PROJECT_ID: 347019916696617554

SPDX-FileCopyrightText: © 2023 Pat Deegan, https://psychogenic.com
SPDX-License-Identifier: Apache2.0

'''

import os
import cocotb
from cocotb.triggers import Timer

class PadLock:
    '''
		Simple class to give access to padlock-type functionality
    '''
    def __init__(self, usermodule,i_bus, o_bus):
        self.dut = usermodule 
        self.i_bus = i_bus 
        self.o_bus = o_bus
        self.lockedLED = usermodule.flipflop1.q
        self.unlockedLED = usermodule.flipflop2.q
		
    async def hitButton(self):
        self.i_bus[0].value = 1 
        await Timer(20, units='ns') # take effect
        self.i_bus[0].value = 0
        await Timer(20, units='ns') # take effect
        
    async def setCombo(self, a,b,c):
        self.i_bus[2].value = a
        self.i_bus[3].value = b
        self.i_bus[4].value = c
        await Timer(20, units='ns') # take effect  
        
    async def reset(self):
        self.i_bus[1].value = 1
        await Timer(20, units='ns') # take effect
        await self.hitButton()
        self.i_bus[1].value = 0
        await Timer(20, units='ns') # take effect
        
    def confirmLocked(self):
        assert self.lockedLED.value == 1
        assert self.unlockedLED.value == 0
        self.dut._log.debug(f'segment display says {self.o_bus.value}, i.e.{self.o_bus.value.integer} ')
        assert self.o_bus.value == 249 # zz11100z, with z's as 1
        
    def confirmUnLocked(self):
        assert self.lockedLED.value == 0
        assert self.unlockedLED.value == 1
        self.dut._log.debug(f'segment display says {self.o_bus.value}, i.e.{self.o_bus.value.integer} ')
        assert self.o_bus.value == 255 # zz11111z, with z's as 1
        
@cocotb.test()
async def playWithPadlock(parentDUT):
    usermodule = parentDUT.dut
    i_bus = parentDUT.io_in
    o_bus = parentDUT.io_out
    padlock = PadLock(usermodule, i_bus, o_bus)
    
    i_bus.value = 0 
    await Timer(20, units='ns') # settle
    
    # after reset, should be locked 
    await padlock.reset()
    padlock.confirmLocked()
    
    
    # fail combo 1
    await padlock.setCombo(1,1,1)
    await padlock.hitButton()
    padlock.confirmLocked()
    
    # fail combo 1
    await padlock.setCombo(0,0,1)
    await padlock.hitButton()
    padlock.confirmLocked()
    
    # valid combo
    await padlock.setCombo(0,1,1)
    await padlock.hitButton()
    padlock.confirmUnLocked()
    
    # reset device
    await padlock.reset()
    padlock.confirmLocked()
