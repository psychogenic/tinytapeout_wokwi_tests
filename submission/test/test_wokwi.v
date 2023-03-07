// SPDX-License-Identifier: Apache2.0

`timescale 1ns / 1ps
`default_nettype none
module test_wokwi ();
  wire [7:0] io_out;
  wire [7:0] io_in;

  user_module_XXXWOKWI_IDXXX dut (
  `ifdef GL_TEST
      .vccd1( 1'b1),
      .vssd1( 1'b0),
  `endif
      .io_in (io_in),
      .io_out(io_out)
  );

  initial begin
    $dumpfile("wokwi_tb.vcd");
    $dumpvars(0, test_wokwi);
  end
endmodule
