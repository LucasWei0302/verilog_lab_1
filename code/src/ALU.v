module ALU(

    operand1_i, 
    operand2_i,
    alu_ctrl_i,
    result_o

);

input [31:0]    operand1_i;
input [31:0]    operand2_i;
input [3:0]     alu_ctrl_i; //ALU control signal

output reg [31:0] result_o;

always @(*) begin
    case (alu_ctrl_i)
        4'b0010: result_o <= operand1_i + operand2_i;
        4'b0110: result_o <= operand1_i - operand2_i;
        4'b0000: result_o <= operand1_i & operand2_i;
        4'b0001: result_o <= operand1_i ^ operand2_i;
        4'b0011: result_o <= operand1_i << operand2_i[4:0];
        4'b1000: result_o <= operand1_i * operand2_i;
        4'b0111: result_o <= $signed(operand1_i) >>> operand2_i[4:0];
        default: result_o <= 32'b0;
    endcase
end

endmodule

