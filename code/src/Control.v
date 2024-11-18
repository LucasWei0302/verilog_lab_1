module Control
(
    opcode_i,
    alu_op_o,
    alu_src_o,
    reg_write_o
);

// Input
input [6:0] opcode_i;

// Outputs
output reg        alu_op_o;    // ALU operation type (0 is for R-Type, 1 is for I-type)
output reg        alu_src_o;  // ALU source (0 is for register, 1 is for immediate)
output reg        reg_write_o; // Register write enable

always @(*) begin
    case (opcode_i)
        7'b0110011: begin // R-type
            alu_op_o     <= 0;
            alu_src_o    <= 0;
            reg_write_o  <= 1;
        end
        7'b0010011: begin // I-type (addi, srai)
            alu_op_o     <= 1;
            alu_src_o    <= 1;
            reg_write_o  <= 1;
        end
        default: begin
            alu_op_o     <= 0;
            alu_src_o    <= 0;
            reg_write_o  <= 0;
        end
    endcase
end

endmodule
