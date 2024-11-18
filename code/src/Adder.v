module Adder(

    data0_i,
    data1_i,
    result_o
);

input [31:0]    data0_i;
input [31:0]    data1_i;

output [31:0]   result_o;

assign result_o = data0_i + data1_i;

endmodule