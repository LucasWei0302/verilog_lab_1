This judge is for unix-like os.

把gen.py跟judge.sh丟到lab1/
在lab1/執行sudo bash judge.sh

原本助教給的testcases/output_1.txt跟testcases/instruction_1.txt備份到backup/裡面
code/supplied/testbench.v也會備份過去

judge.sh做的事情如下
gen.py會生成新的testcases/output_1.txt(標準答案)和testcases/instruction_1.txt(測資) 覆蓋掉原本的
然後我直接call Makefile 他會把instruction餵進去testbench.v 得到執行結果 放在log/output_1.txt(你的答案)
然後去diff 標準答案跟你的答案 如果一樣 那就會循環執行
直到答案不一樣 那就會停下來
你可以去testcases/裡面把測資拿出來看

值得注意的是 因為judge.sh每次生成instruction的數量是隨機的 我會在gen.py跟testbench.v裡面修改這個數字

根據code/supplied/Instruction_Memory.v instruction的數量只有到256個 如果想要測更多就要改Instruction_Memory.v