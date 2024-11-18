#!/bin/bash

# Step 1: Create a backup directory if it doesn't exist
mkdir -p backup

# Step 2: Check if instruction_1.txt exists in the backup directory, if not, copy it
if [ ! -f backup/instruction_1.txt ]; then
    cp testcases/instruction_1.txt backup/instruction_1.txt
fi

# Step 3: Check if output_1.txt exists in the backup directory, if not, copy it
if [ ! -f backup/output_1.txt ]; then
    cp testcases/output_1.txt backup/output_1.txt
fi

# Step 4: Check if testbench.v exists in the backup directory, if not, copy it
if [ ! -f backup/testbench.v ]; then
    cp code/supplied/testbench.v backup/testbench.v
fi

# Step 5: Loop until diff shows a difference
while true; do

    # Step 7: Generate a random integer
    instruction_count=$(((RANDOM % 255) + 1))

    # Step 8: Update gen.py with the generated instruction count (instruction_count - 1)
    sed -i "s/instr_num = .*/instr_num = $((instruction_count - 1))/" gen.py

    # Step 9: Update testbench.v with the same generated number
    sed -i "s/if(counter == [0-9]*).*/if(counter == $instruction_count) /" code/supplied/testbench.v

    # Step 10: Execute gen.py to generate instruction_1.txt and output_1.txt
    python3 gen.py

    # Step 11: Simulate execution using docker-compose
    docker-compose up

    # Step 12: Compare the output files
    if diff testcases/output_1.txt log/output_1.txt; then
        echo "Outputs are the same, continuing..."
    else
        echo "Outputs are different. Stopping execution."
        break
    fi
done
