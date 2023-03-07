
import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


async def make_clock(dut, clock_mhz):
    clk_period_ns = round(1 / clock_mhz * 1000, 2)
    dut._log.info("input clock = %d MHz, period = %.2f ns" %
                  (clock_mhz, clk_period_ns))
    clock = Clock(dut.clk, clk_period_ns, units="ns")
    clock_sig = cocotb.fork(clock.start())
    return clock_sig


@cocotb.test()
async def test_wokwi(dut):
    print(str(dut))

