module CPU
(
    clk_i, 
    rst_i,
);

// Ports
input               clk_i;
input               rst_i;

wire [31:0] pc_i, pc_o, instr, imm_ext, read_data1, read_data2, alu_result;
wire [4:0] rs1, rs2, rd;
wire [2:0] func3;
wire [6:0] opcode, func7;
wire alu_src, reg_write, alu_op;
wire [3:0] alu_ctrl;
wire [31:0] mux_out;

PC PC(
    .clk_i(clk_i),
    .rst_i(rst_i),
    .pc_i(pc_i),
    .pc_o(pc_o)
);

Instruction_Memory Instruction_Memory(
    .addr_i(pc_o), 
    .instr_o(instr)
);

assign opcode = instr[6:0];
assign rd = instr[11:7];
assign func3 = instr[14:12];
assign rs1 = instr[19:15];
assign rs2 = instr[24:20];
assign func7 = instr[31:25];


Control Control(
    .opcode_i(opcode),
    .alu_op_o(alu_op),
    .alu_src_o(alu_src),
    .reg_write_o(reg_write)
);


Registers Registers(
    .rst_i(rst_i),
    .clk_i(clk_i),
    .RS1addr_i(rs1),
    .RS2addr_i(rs2),
    .RDaddr_i(rd), 
    .RDdata_i(alu_result),
    .RegWrite_i(reg_write), 
    .RS1data_o(read_data1), 
    .RS2data_o(read_data2) 
);

Sign_Extend Sign_Extend(
    .instr_i(instr[31:20]),
    .data_o(imm_ext)
);


Adder Add_PC(
    .data0_i(pc_o),
    .data1_i(32'd4),
    .result_o(pc_i)
);


MUX32 MUX_ALUSrc(
    .data0_i(read_data2),
    .data1_i(imm_ext),
    .select_i(alu_src),
    .data_o(mux_out)
);

ALU_Control ALU_Control(
    .alu_op_i(alu_op),
    .func3_i(func3),
    .func7_i(func7),
    .alu_ctrl_o(alu_ctrl)

);

ALU ALU(
    .operand1_i(read_data1), 
    .operand2_i(mux_out),
    .alu_ctrl_i(alu_ctrl),
    .result_o(alu_result)
);


endmodule

