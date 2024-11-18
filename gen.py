import random

output_file = "testcases/output_1.txt"
instruction_file = "testcases/instruction_1.txt"

# Clear the content of the output files before starting
with open(output_file, "w") as outfile:
    outfile.write("")
with open(instruction_file, "w") as instr_file:
    instr_file.write("")

# Initialize registers, PC, and instruction list
registers = [0] * 32
pc = 0
instructions = []

# Define the instruction formats
R_format = ['and', 'xor', 'sll', 'add', 'sub', 'mul']
I_format = ['addi', 'srai']

# Define the funct7, funct3, opcode for each instruction
instruction_set = {
    'and':  {'funct7': '0000000', 'funct3': '111', 'opcode': '0110011'},
    'xor':  {'funct7': '0000000', 'funct3': '100', 'opcode': '0110011'},
    'sll':  {'funct7': '0000000', 'funct3': '001', 'opcode': '0110011'},
    'add':  {'funct7': '0000000', 'funct3': '000', 'opcode': '0110011'},
    'sub':  {'funct7': '0100000', 'funct3': '000', 'opcode': '0110011'},
    'mul':  {'funct7': '0000001', 'funct3': '000', 'opcode': '0110011'},
    'addi': {'funct7': '',        'funct3': '000', 'opcode': '0010011'},
    'srai': {'funct7': '0100000', 'funct3': '101', 'opcode': '0010011'}
}

# Generate 12-bit immediate for addi
def generate_imm_12bit():
    return random.randint(-2048, 2047)

# Generate 5-bit non-negative immediate for srai
def generate_imm_5bit():
    return random.randint(0, 15)

# Ensure rs2 is non-negative for sll
def choose_rs2_non_negative():
    non_negative_regs = [i for i in range(32) if registers[i] >= 0]
    if not non_negative_regs:
        return None  # fallback to other instructions if all are negative
    return random.choice(non_negative_regs)

def sign_check_and_fix(A):
    # 判斷最高位
    A &= 0xFFFFFFFF
    if (A & 0x80000000) == 0:
        return A
    else:
        return A - 0x100000000

def sll(A, shift):
    shifted_value = (A << shift) & 0xFFFFFFFF
    return sign_check_and_fix(shifted_value)
    

def srai(A, shift):
    # 先將 A 轉換為 64 位，並進行右移
    # 右移時需要根據最高位填充
    if A < 0:
        # 如果 A 是負數，使用算術右移
        shifted_value = (A >> shift) | (0xFFFFFFFF << (64 - shift))
    else:
        # 如果 A 是正數，使用邏輯右移
        shifted_value = (A >> shift) & 0xFFFFFFFF
    
    return shifted_value

# Generate a random instruction
def generate_instruction():
    global pc
    
    # instr_type = random.choice(R_format + I_format)
    instr_type = random.choice(['sll', 'mul'] + I_format)
    
    rs1 = random.randint(0, 31)
    rd = random.randint(0, 31)
    
    # Handle different instruction types
    if instr_type in R_format:
        rs2 = random.randint(0, 31)
        if instr_type == 'sll':  # Ensure non-negative rs2 for sll
            rs2 = choose_rs2_non_negative()
            if rs2 is None:  # If no non-negative rs2 found
                raise
        
        funct7 = instruction_set[instr_type]['funct7']
        funct3 = instruction_set[instr_type]['funct3']
        opcode = instruction_set[instr_type]['opcode']
        machine_code = f"{funct7}_{rs2:05b}_{rs1:05b}_{funct3}_{rd:05b}_{opcode}"
        instructions.append(f"{machine_code} // {instr_type} x{rd},x{rs1},x{rs2}")
    
    elif instr_type == 'addi':
        imm12 = generate_imm_12bit()
        imm12_bin = f"{imm12 & 0b111111111111:012b}" if imm12 >= 0 else f"{(4096 + imm12):012b}"
        funct3 = instruction_set[instr_type]['funct3']
        opcode = instruction_set[instr_type]['opcode']
        machine_code = f"{imm12_bin}_{rs1:05b}_{funct3}_{rd:05b}_{opcode}"
        instructions.append(f"{machine_code}  // {instr_type} x{rd},x{rs1},{imm12}")
    
    elif instr_type == 'srai':
        imm5 = generate_imm_5bit()
        funct7 = instruction_set[instr_type]['funct7']
        funct3 = instruction_set[instr_type]['funct3']
        opcode = instruction_set[instr_type]['opcode']
        machine_code = f"{funct7}_{imm5:05b}_{rs1:05b}_{funct3}_{rd:05b}_{opcode}"
        instructions.append(f"{machine_code} // {instr_type} x{rd},x{rs1},{imm5}")
    
    # Update the register file except for x0
    if rd != 0:
        if instr_type == 'addi':
            registers[rd] = registers[rs1] + imm12
        elif instr_type == 'srai':
            registers[rd] = registers[rs1] >> imm5 # ok
            # registers[rd] = srai(registers[rs1], imm5)
        elif instr_type == 'and':
            registers[rd] = registers[rs1] & registers[rs2]
        elif instr_type == 'xor':
            registers[rd] = registers[rs1] ^ registers[rs2]
        elif instr_type == 'sll':
            # registers[rd] = registers[rs1] << registers[rs2] # wrong
            registers[rd] = sll(registers[rs1], registers[rs2])
        elif instr_type == 'add':
            registers[rd] = registers[rs1] + registers[rs2]
        elif instr_type == 'sub':
            registers[rd] = registers[rs1] - registers[rs2]
        elif instr_type == 'mul':
            registers[rd] = registers[rs1] * registers[rs2]
        registers[rd] = sign_check_and_fix(registers[rd])
        
    # Increment PC by 4
    pc += 4

# Print the register file and PC
def print_register_state():
    regfile = f"PC = {pc:10}\nRegisters\n"
    regfile += f"x0     = {registers[0]:10}, x8(s0)  = {registers[8]:10}, x16(a6) = {registers[16]:10}, x24(s8)  = {registers[24]:10}\n"
    regfile += f"x1(ra) = {registers[1]:10}, x9(s1)  = {registers[9]:10}, x17(a7) = {registers[17]:10}, x25(s9)  = {registers[25]:10}\n"
    regfile += f"x2(sp) = {registers[2]:10}, x10(a0) = {registers[10]:10}, x18(s2) = {registers[18]:10}, x26(s10) = {registers[26]:10}\n"
    regfile += f"x3(gp) = {registers[3]:10}, x11(a1) = {registers[11]:10}, x19(s3) = {registers[19]:10}, x27(s11) = {registers[27]:10}\n"
    regfile += f"x4(tp) = {registers[4]:10}, x12(a2) = {registers[12]:10}, x20(s4) = {registers[20]:10}, x28(t3)  = {registers[28]:10}\n"
    regfile += f"x5(t0) = {registers[5]:10}, x13(a3) = {registers[13]:10}, x21(s5) = {registers[21]:10}, x29(t4)  = {registers[29]:10}\n"
    regfile += f"x6(t1) = {registers[6]:10}, x14(a4) = {registers[14]:10}, x22(s6) = {registers[22]:10}, x30(t5)  = {registers[30]:10}\n"
    regfile += f"x7(t2) = {registers[7]:10}, x15(a5) = {registers[15]:10}, x23(s7) = {registers[23]:10}, x31(t6)  = {registers[31]:10}\n\n"

    with open(output_file, "a") as outfile:
        outfile.write(regfile + '\n')

instr_num = 50

for _ in range(instr_num):
    # Print register states
    print_register_state()
    generate_instruction()
print_register_state()

# Save the generated instructions
with open(instruction_file, "w") as f:
    for instr in instructions:
        f.write(instr + "\n")
