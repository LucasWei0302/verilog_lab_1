module ALU_Control(

    alu_op_i,
    func3_i,
    func7_i,
    alu_ctrl_o

);

input           alu_op_i; //0 is for R-type, 1 is for I-type
input [2:0]     func3_i; //Function code for operation
input [6:0]     func7_i; //More function code for R-type operation

output reg [3:0] alu_ctrl_o; //to determine control signal for alu operation

always @(*) begin
    case (alu_op_i)
        1'b0: begin //R-type
            case ({func7_i, func3_i})
                10'b0000000000: alu_ctrl_o <= 4'b0010; // add
                10'b0100000000: alu_ctrl_o <= 4'b0110; // sub
                10'b0000000111: alu_ctrl_o <= 4'b0000; // and
                10'b0000000100: alu_ctrl_o <= 4'b0001; // xor
                10'b0000000001: alu_ctrl_o <= 4'b0011; // sll
                10'b0000001000: alu_ctrl_o <= 4'b1000; // mul 
                default:        alu_ctrl_o <= 4'b1111; 
            endcase
        end
        1'b1: begin
            case (func3_i)
                3'b000: alu_ctrl_o <= 4'b0010; // addi
                3'b101: alu_ctrl_o <= 4'b0111; // srai
                default: alu_ctrl_o <= 4'b1111; // undefined operation
            endcase
        end
        default: alu_ctrl_o <= 4'b1111; // undefined operation
    endcase
end

endmodule



