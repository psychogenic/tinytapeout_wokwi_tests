'''
	TruthTable testing
	Copyright (C) 2023 Pat Deegan, https://psychogenic.com

	A simple system to take truth table data from yosys, like

		 \io_in | \io_out
	 ---------- | -----------
	 8'11111000 | 8'xxxxxxx0
	 8'11111001 | 8'xxxxxxx1
	 8'11111010 | 8'xxxxxxx0
	 ...

	and run it through cocotb harness.

    SAMPLE USAGE:

	@cocotb.test()
	async def truthTableCompare(dut):
		i_bus = dut.io_in
		o_bus = dut.io_out
		tt = truthtable.loadSimpleTruthTable('test/truthtable.txt')
		await tt.testAll(i_bus, o_bus, dut._log)
		

   SPDX-FileCopyrightText: © 2023 Pat Deegan, https://psychogenic.com
   SPDX-License-Identifier: Apache2.0
'''
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer
from cocotb.binary import BinaryValue
import re

class SaneBinaryValue(BinaryValue):
	def __init__(self, vstr:str):
		super().__init__(vstr, n_bits=len(vstr), bigEndian=False)
		numbits = len(vstr)
		self.careBit = [True]*numbits
		for i in range(numbits):
			c = vstr[i]
			if c != '1' and c != '0':
				self.careBit[(numbits - 1) - i] = False

class TruthMapping:
	def __init__(self, resultingValue:str):
		self.result = SaneBinaryValue(resultingValue)
		
		
class TruthTable:
	def __init__(self):
		self.mappings = []
		
	def addMapping(self, relationship:TruthMapping):
		self.mappings.append(relationship)
		
	def getMapping(self, idx:int) -> TruthMapping:
		if idx >= len(self.mappings):
			raise IndexError('out of bounds on mapping')
			
		return self.mappings[idx]
		
	def numMappings(self):
		return len(self.mappings)
		
	def __len__(self):
		return self.numMappings()
		
	def __getitem__(self, idx:int):
		return self.getMapping(idx)
		
		
	async def testAll(self, i_bus, o_bus, logger=None):	
		for i in range(len(self)):
			i_bus.value = self[i].state
			await Timer(10, units="ns")  # wait a tad
			expectedResult = self[i].result
			if logger is not None:
				logger.info(f'State {i}, setting input to {self[i].state}, expecting {expectedResult} (got {o_bus})')
				
			# this is so stupid that it's probably wrong... there _must_ be
			# a good way to do this, otherwise _what_ is the point of having
			# unknown and don't care... but anyway, 
			# will die if o_bus[n] is some defined value
			# but we expect a don't know (x) or even a don't care (-), ugh
			# manual style
			for bit in range(len(o_bus)):
				if expectedResult.careBit[bit]:
					# ok, safe to compare, duh
					# logger.info(f'Doing bit {bit}: {o_bus[bit]} == {expectedResult[bit]}')
					assert o_bus[bit] == expectedResult[bit]
		
		
class OneToOneTruthMapping(TruthMapping):
	def __init__(self, state:str, output:str):
		super().__init__(output)
		self.state = SaneBinaryValue(state)
		

def parseSimpleTable(contents:str):
	tt = TruthTable()
	m = re.compile(r'''^\s*\d'(\d+)\s*\|\s*\d'([zZxX\d]+)''', re.M)
	for match in m.findall(contents):
		if match[1] != 'x':
			# we skip anything where all results are don't care
			# result = match[1].replace('x', '-') # now using the BinaryValue override
			result = match[1]
			tt.addMapping(OneToOneTruthMapping(match[0],result))
		
	return tt
	
def loadSimpleTruthTable(filepath:str):
	with open(filepath, 'r') as f:
		contents = f.read()
		return parseSimpleTable(contents)
	
	return None
	
	

		 

TruthTableExample = '''
     \\io_in | \\io_out
 ---------- | -----------
 8'11111000 | 8'xxxxxxx0
 8'11111001 | 8'xxxxxxx1
 8'11111010 | 8'xxxxxxx0
 8'11111011 | 8'xxxxxxx1
 8'11111100 | 8'xxxxxxx0
 8'11111101 | 8'xxxxxxx1
 8'11111110 | 8'xxxxxxx1
 8'11111111 | 8'xxxxxxx0

'''

if __name__ == "__main__":
	tt = parseSimpleTable(TruthTableExample)
	print(f'with state {tt[0].state} you get {tt[0].result}')
