module Sign_Extend(

    instr_i,
    data_o
);

input [11:0]    instr_i;
output [31:0]   data_o;

assign data_o = {{20{instr_i[11]}},instr_i};

endmodule