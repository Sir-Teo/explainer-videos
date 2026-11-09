# Computer Science, Built — Part 6: The Stored-Program Computer

Part 6 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the end of Act I. ENIAC was initially programmed with cables; the EDVAC report described
instructions in memory beside data, drawing on the team’s discussions. This part builds that machine, Pebble, from the gates, adders and registers of
Parts 3–5: an instruction set designed bit by bit, a single-cycle datapath and its control unit, an assembler, and
programs. The gate-level CPU is one netlist (`explainer/cs/pebble/cpu.py`), compiled to C (`fast.py`) and checked
against the instruction-level emulator (`emu.py`) on random programs. It runs Euclid, bounded Turing-machine examples, and the Job,
version 0, whose exact cycle count for thirty novels is the first row of the ledger. Every number is computed in
`compute.py`.

* **A machine that reads its own instructions.** Five parts of pieces; the program as numbers in memory and the
  program counter walking Part 1's Euclid; what the part builds; objectives.
* **1. Cables, then memory.** ENIAC (1945: 17,468 tubes, 5,000 additions a second, programmed by plugging cables)
  and its six programmers; von Neumann's *First Draft* (June 1945) and the credit dispute; the Manchester Baby's first
  program (21 June 1948: the largest proper factor of 2¹⁸, 52 minutes, about 3.5 million instructions); EDSAC (6 May
  1949), the Wheeler jump and the initial orders.
* **2. Instructions are data.** Fetch, decode, execute, next; a five-instruction program stepped register by
  register; the instruction set as a contract above single-cycle, pipelined and out-of-order machines.
* **3. Designing an instruction set.** Sixteen registers (r0 = 0), byte-addressed little-endian memory, the program
  counter; the R, I, S and J formats bit by bit; 34 instructions, one opcode each, and the design rules; Pebble-32
  beside RV32I.
* **4. The datapath, one instruction at a time.** Fetch (pc, instruction memory, +4); R format through the register
  file and ALU; immediates and the operand multiplexer; loads and stores through data memory and write-back; branch
  target adder and the next-pc multiplexer; jal's link; 8,224 gates and 512 flip-flops.
* **5. The control unit.** The 34 × 20 truth table; built as a PLA (one product term per opcode, 307 gates) and as
  minimized logic (Quine–McCluskey with the 30 illegal opcodes as don't-cares, 205 gates), both verified; microcode
  (Wilkes, 1951), System/360, patchable x86 microcode.
* **6. The assembler.** Mnemonics and labels (Kathleen Booth, 1947; EDSAC's initial orders); pass 1 and the symbol
  table; pass 2 and PC-relative offsets; pseudo-instructions and why the zero register makes half of them possible.
* **7. First programs, gate by gate.** 1 + … + 10 traced on the gate-level machine; Euclid's registers as a
  staircase over 60 cycles; 300 random programs, both control units, all final registers, memory bytes, program counters and step counts equal to the emulator. This checks completed program states, not each instruction boundary or all possible programs.
* **8. What a program costs.** The iron law (instructions × CPI × cycle time); a load's path through the cycle, the
  the netlist's structural depth of 59 and sampled maximum of 56 unit gate delays (4,096 inputs), neither a certified silicon clock nor a worst-case delay proof; an explicit teaching timing budget including memory; the Job's instruction mix.
* **9. Talking to the world.** Memory-mapped devices (console, tape, cycle counter) and the PDP-11; printing a
  string; polling, and why device addresses must not be cached.
* **10. The Job, version 0.** Linear search in an unsorted table, animated; the inner loop in assembly (6
  instructions per entry); a paragraph at gate level (613 bytes, 53,665 cycles) and chapter 1 on the emulator
  (827,576); an exact cycle formula, checked on 20 random passages; thirty novels: 1.069 × 10¹¹ cycles, 4,279 per
  byte, 99.7% of them in the search; rate analogies of 640 years at 5.3 operations/s and 8 months at 5,000/s, not actual ports to Z3 or ENIAC; 4.7 minutes at an assumed 380 MHz Pebble clock, not measured silicon; ledger row 0.
* **11. Pebble and the Turing machine.** A Turing-machine interpreter in Pebble assembly runs the 3-state busy beaver
  (21 steps, 5 ones) and the 4-state one (107, 13); the converse simulation argument. Fixed 32-bit Pebble is finite-state; universality requires an ideal family with unbounded effective storage and addressing. These examples do not prove the Church–Turing thesis. Only the 2- and 3-state examples are gate-checked; the 4-state case uses the emulator.
* **12. Code is data.** Summing an array EDSAC-style by rewriting a load's offset field; index registers (the
  Manchester Mark 1's B-lines, 1949), stale prefetched instructions, write-xor-execute, and JIT compilers.
* **13. When the world interrupts.** Polling against interrupts (DYSEAC, 1954); exceptions: illegal instructions,
  divide by zero, page faults, system calls.
* **14. The whole machine, counted.** Gates by block (the register file's read ports are the biggest); a synthetic estimate of ≈ 90,000 transistors (NAND equivalents × 4 plus flip-flops × 24), excluding memory, I/O, clocks, buffers and layout, against the 6502, 8086, 80386 and the whole 16-billion-transistor Apple M1 system on a chip (2020), with different counting scopes rather than an area comparison; a trip down the tower,
  datapath to transistors, and back.
* **15. Frontier: is the processor right?** A separate mutation study using the random generator with multiply/divide enabled (the gate CPU implements the base ISA): nine bugs planted
  one at a time in a copy of the emulator, each run against 2,000 random programs. A store that also writes the next
  byte is caught by 67% of them and shifts that read 4 bits of their amount by 54%; a byte load that forgets its sign
  by 0.25%, a branch wrong only for two zeros by 2.7%; dividing −2³¹ by −1 by 0 of these 2,000 programs. This does not establish zero hit probability. Independent uniform 32-bit operands would give 2⁻⁶⁴ for that pair; a uniform dividend with divisor fixed at −1 gives 2⁻³². Neither is the evolving generator’s distribution. Detection
  budgets, 1 − (1 − r)^N, require independent tests and a fixed true per-test rate; empirical rates are illustrations. A directed boundary test distinguishes the mutant in one run. CPU fuzzing (DifuzzRTL, 2021; Cascade, 2024:
  37 new bugs in 5 of 6 RISC-V CPUs). Sail, an executable formal reference for supported RISC-V features, not by itself a proof of a core; verified designs (Kami, 2017; Silver + CakeML,
  2019). Abstract out-of-order proofs and selected industrial verification exist; scaling complete correctness and security arguments to complex implementations remains difficult.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs6.compute            # every number in the part (a few minutes: the CPU compiles once)
python tools/build.py cs6 -q l             # a 480p preview
python tools/build.py cs6                  # 1080p
```

The Job's corpus is *AI, Built* Part 1's thirty Gutenberg novels (downloaded into `.cache/ai1/books`). Ledger row 0 is
written to `.cache/cs6/ledger.json`.

## Problems, with solutions

1. **Encode by hand.** Encode `sub t0, a1, a2` and `sw t0, -8(sp)` in hexadecimal, field by field.

   *Solution.* `sub` is opcode 2, R format: rd = t0 = 9, rs1 = a1 = 4, rs2 = a2 = 5, so the word is
   2·2²⁶ + 9·2²² + 4·2¹⁸ + 5·2¹⁴ = **0x0A514000**. `sw` is opcode 23, S format: rs1 = sp = 2 in bits 25–22, rs2 = t0 = 9
   in bits 21–18, and −8 as an 18-bit two's complement immediate, 0x3FFF8: 23·2²⁶ + 2·2²² + 9·2¹⁸ + 0x3FFF8 =
   **0x5CA7FFF8**.

2. **A control word.** Which of the 20 control signals does `jalr ra, 4(t1)` set?

   *Solution.* **rw** (write a register), **imm** (the immediate is the ALU's second operand), **wb1** with wb0 = 0
   (write back the link, pc + 4) and **jalr** (take the next pc from the ALU). The ALU operation is add (all four aop
   bits 0), and every other signal is 0: no memory access, no branch.

3. **The single-cycle clock.** Assume a worst-case teaching budget: instruction and data memory take 1 ns each; logic takes 56 gate delays of 10 ps,
   plus 70 ps of flip-flop overhead. What is f_max? How much faster could a machine run that never touched data
   memory?

   *Solution.* The period must hold both memory accesses and the logic: 1 + 1 + 0.56 + 0.07 = 2.63 ns, so
   **f_max ≈ 380 MHz within this assumed model**. The sampled netlist maximum does not certify this budget for physical hardware. Without the data memory the period is 1.63 ns, **613 MHz, 1.61 times faster**: the single-cycle
   design makes every add pay for the loads. Part 7's pipeline instead gives each stage its own cycle.

4. **Reverse a string.** Write a Pebble program that reverses a zero-terminated string in place. How many instructions
   does it run for n letters?

   *Solution.*

   ```
           la   a0, str          # a0: the first letter
           mv   a1, a0
   find:   lbu  t0, 0(a1)        # a1: walk to the terminating zero
           beqz t0, found
           addi a1, a1, 1
           j    find
   found:  addi a1, a1, -1       # a1: the last letter
   swap:   bgeu a0, a1, done     # the pointers have met
           lbu  t0, 0(a0)
           lbu  t1, 0(a1)
           sb   t1, 0(a0)
           sb   t0, 0(a1)
           addi a0, a0, 1
           addi a1, a1, -1
           j    swap
   done:   halt
   ```

   Counting (la is two instructions): 3 to start, 4 per letter to find the end, 3 more to leave the loop and step
   back, 8 per swap, and 2 to finish: **8 + 4n + 8⌊n/2⌋**. On the emulator, "stressed" (n = 8) becomes "desserts" in
   72 instructions, and "pebble" (n = 6) becomes "elbbep" in 56.

5. **Rewrite a branch.** Write a program that turns one of its own `beq` instructions into a `bne`. Why does it work on
   single-cycle Pebble, and why might it fail on a pipeline?

   *Solution.* beq is opcode 25 and bne 26, and the opcode is the top six bits, so adding 2²⁶ to the word changes one
   into the other:

   ```
           la   s0, test
           lw   t0, 0(s0)        # the beq, as a word
           li   t1, 0x04000000   # 1 << 26
           add  t0, t0, t1
           sw   t0, 0(s0)        # now it is bne
           li   a0, 0
   test:   beq  a0, zero, skip   # as written: taken; rewritten: not taken
           li   a1, 1
           halt
   skip:   li   a1, 2
           halt
   ```

   It ends with **a1 = 1**: the rewritten branch is not taken. Single-cycle Pebble fetches every instruction from
   memory in the cycle it runs, so it always sees the newest word. A pipeline fetches several instructions ahead, and
   a cache may hold an old copy of the instruction, so without an explicit flush the processor can run the **stale**
   beq.

6. **Build: move the found word up.** Change `JOB_V0` so that a word that is found swaps places with the entry above it.
   Run both versions on chapter 1 with the emulator: how many instructions does the change save?

   *Solution.* At `found`, after adding one to the count, if the entry is not first, copy the entry above down one
   place (three loads and stores) and store this word's pointer, length and count above it (three stores). Frequent
   words drift towards the top, where the linear search finds them sooner. On chapter 1 of *Pride and Prejudice* the
   count drops from 827,576 to **822,271 instructions (0.6%)**; on the first 60 kB of the novel, from 27.45 to 26.53
   million (**3.4%**). The printed top twenty is identical. A small idea buys a little; Part 17's hash table removes the
   search altogether.

7. **★ Research: define what a generator covers.** Add boundary-value generation to `random_program`, then rerun all nine planted mutants on 2,000 fixed seeds. Define the operand classes your generator is intended to cover and report the evidence, including misses.

   *Starting point.* Include 0, 1, −1, 2³¹−1, −2³¹, 0x7F, 0x80 and 0xFF. Initializing a register does not ensure a later instruction consumes that value: instructions overwrite registers and the current generator forces division’s divisor odd. Instrument the values actually consumed by each opcode. Enumerate a finite set of ordered operand classes and check that each appears. A separate directed program with `li a0, 0x80000000; li a1, -1; div a2, a0, a1; halt` already distinguishes the overflow mutant: the reference returns 0x80000000 and the mutant returns 0. Do not label this directed example as a random-generator success.

   Independent per-operand sampling would give a pair probability equal to the product of the two marginal probabilities; it does not give that probability for correlated evolving registers. Coverage-guided testing can help exploration, but does not imply discovery within a fixed time. Finite coverage guarantees and proof-guided test generation exist; scaling useful guarantees to realistic processor state spaces is the research challenge. Report the precise class coverage you established and the properties still unproved.

## 习题与解答

1. **手工编码。** 把 `sub t0, a1, a2` 和 `sw t0, -8(sp)` 逐字段编码成十六进制。

   *解答。* `sub` 的操作码是 2，R 格式：rd = t0 = 9，rs1 = a1 = 4，rs2 = a2 = 5，所以这个字是
   2·2²⁶ + 9·2²² + 4·2¹⁸ + 5·2¹⁴ = **0x0A514000**。`sw` 的操作码是 23，S 格式：rs1 = sp = 2 放在第 25–22 位，
   rs2 = t0 = 9 放在第 21–18 位，−8 写成 18 位补码立即数 0x3FFF8：23·2²⁶ + 2·2²² + 9·2¹⁸ + 0x3FFF8 = **0x5CA7FFF8**。

2. **一个控制字。** `jalr ra, 4(t1)` 会置位 20 个控制信号中的哪些？

   *解答。* **rw**（写寄存器）、**imm**（立即数作为算术逻辑单元的第二个操作数）、**wb1**（wb0 = 0，写回链接地址 pc + 4），以及
   **jalr**（下一个 pc 取自算术逻辑单元）。运算是加法（四个 aop 位全为 0），其余信号都为 0：不访问存储器，也不是分支。

3. **单周期时钟。** 假设一个最坏情况教学预算：两次存储器访问各需 1 ns，逻辑为 56 个 10 ps 的门延迟，另加 70 ps 的触发器开销。f_max 是多少？
   一台从不访问数据存储器的机器能快多少？

   *解答。* 一个周期要容下两次存储器访问和逻辑：1 + 1 + 0.56 + 0.07 = 2.63 ns，所以**在此假设模型中 f_max ≈ 380 MHz**。抽样网表最大值并不能验证真实芯片的这项预算。去掉数据存储器，周期为
   1.63 ns，即 **613 MHz，快 1.61 倍**：单周期设计让每一条加法都为取数指令买单。第 7 部分的流水线则让每一级各有自己的周期。

4. **反转字符串。** 写一个 Pebble 程序，原地反转一个以零结尾的字符串。对 n 个字母它要执行多少条指令？

   *解答。* 程序见上文英文部分。计数（la 是两条指令）：开头 3 条，找结尾时每个字母 4 条，离开循环并退回一步再 3 条，每次交换
   8 条，结束 2 条：**8 + 4n + 8⌊n/2⌋**。在模拟器上，"stressed"（n = 8）用 72 条指令变成 "desserts"，"pebble"（n = 6）用 56 条
   变成 "elbbep"。

5. **改写一条分支。** 写一个程序，把它自己的一条 `beq` 改成 `bne`。为什么它在单周期 Pebble 上可行？为什么在流水线上可能失败？

   *解答。* beq 的操作码是 25，bne 是 26，而操作码是最高的六位，所以给这个字加上 2²⁶ 就把前者变成后者（程序见上文）。它结束时
   **a1 = 1**：改写后的分支没有跳转。单周期 Pebble 在每条指令执行的那个周期才从存储器取它，所以总能看到最新的字。流水线会提前取
   好几条指令，缓存也可能保留指令的旧副本，因此如果不显式刷新，处理器可能执行那条**过时的** beq。

6. **动手：把找到的词往上移。** 修改 `JOB_V0`，让找到的词与它上面的条目交换位置。用模拟器在第 1 章上运行两个版本：这一改动省了多少
   条指令？

   *解答。* 在 `found` 处把计数加一之后，如果这个条目不在最前面，就把上面的条目下移一格（三次取数和存数），再把这个词的指针、长度
   和计数存到上面（三次存数）。常用词会逐渐漂到前面，线性查找就能更早找到它们。在《傲慢与偏见》第 1 章上，指令数从 827,576 降到
   **822,271（0.6%）**；在小说的前 60 kB 上，从 2745 万降到 2653 万（**3.4%**）。打印出的前二十个词完全相同。小主意只换来一点点；
   第 17 部分的哈希表则彻底去掉了查找。

7. **★ 研究题：定义生成器覆盖了什么。** 在 `random_program` 中加入边界值生成，用两千个固定种子重跑全部九个变异体。定义预期覆盖的操作数类别，报告证据和仍然漏掉的情况。

   *起点。* 可加入 0、1、−1、2³¹−1、−2³¹、0x7F、0x80、0xFF。但寄存器的初值不等于后来指令真正读到的值：中间指令会覆盖它，当前生成器还把除数强制变成奇数。因此要记录每种操作真正消耗的值，枚举有限的有序操作数类别，并检查是否全部出现。另一个定向程序 `li a0, 0x80000000; li a1, -1; div a2, a0, a1; halt` 能直接区分溢出变异体：参考实现返回 0x80000000，变异体返回 0。不要把它算成随机生成器已经发现了错误。

   只有独立抽样，才能把两个边缘概率相乘；不能把这种计算套到相互关联、不断变化的寄存器上。覆盖率引导能帮助探索，但不保证固定时间内发现错误。有限覆盖保证和证明引导测试已经存在；研究难点在于把有用保证扩展到现实处理器状态空间。应明确已确立的类别覆盖，以及仍未证明的性质。

## Glossary additions

存储程序计算机 stored-program computer · 冯·诺依曼体系结构 von Neumann architecture · 程序计数器 program counter · 取指、译码、
执行 fetch, decode, execute · 指令集体系结构 instruction set architecture · 操作码 opcode · 立即数 immediate · 符号扩展 sign
extension · 小端序 little-endian · 数据通路 datapath · 控制单元 control unit · 控制字 control word · 多路选择器 multiplexer ·
可编程逻辑阵列 PLA · 微码 / 控制存储器 microcode / control store · 汇编器 assembler · 标号 label · 符号表 symbol table · 伪指令
pseudo-instruction · 相对 pc 的偏移 PC-relative offset · 每条指令周期数 CPI · 铁律 the iron law · 关键路径 critical path ·
内存映射输入输出 memory-mapped I/O · 轮询 polling · 中断 interrupt · 异常 / 陷阱 exception / trap · 系统调用 system call · 自修改
代码 self-modifying code · 变址寄存器 index register · 写异或执行 write xor execute · 即时编译 JIT · 协同仿真 co-simulation

## Sources

Books: Patterson & Hennessy, *Computer Organization and Design, RISC-V Edition*, ch. 2 and 4; Harris & Harris, *Digital
Design and Computer Architecture*, ch. 6–7; Nisan & Schocken, *The Elements of Computing Systems*, ch. 4–6; Haigh,
Priestley & Rope, *ENIAC in Action* (2016); Waterman & Asanović (eds.), *The RISC-V Instruction Set Manual*, Volume I.

Papers and reports: von Neumann, *First Draft of a Report on the EDVAC* (1945); Booth & Booth, "Coding for A.R.C."
(1947); Williams & Kilburn, "Electronic digital computers", *Nature* 162 (1948); Wilkes, "The best way to design an
automatic calculating machine" (1951); Wilkes, Wheeler & Gill, *The Preparation of Programs for an Electronic Digital
Computer* (1951); Patterson & Ditzel, "The case for the reduced instruction set computer" (1980).


Primary references for the verification chapter:

- Solt, Ceesay-Seitz & Razavi, *Cascade: CPU Fuzzing via Intricate Program Generation*, USENIX Security 2024 ([paper](https://comsec.ethz.ch/wp-content/files/cascade_sec24.pdf)). The paper reports 37 new bugs in 5 of 6 tested CPUs; Cascade’s program-construction approach is distinct from a generic coverage-feedback loop.
- Hur et al., *DifuzzRTL: Differential Fuzz Testing to Find CPU Bugs*, NDSS 2021, cited and compared in Cascade.
- Lööw et al., *Verified Compilation on a Verified Processor*, PLDI 2019 ([paper](https://cakeml.org/pldi19.pdf)); Silver is a proof-of-concept processor, with explicit initialization/environment assumptions.
- [Kami project](https://github.com/mit-plv/kami), [RISC-V Sail model](https://github.com/riscv/sail-riscv), and [RISC-V integer divide semantics](https://github.com/riscv/riscv-isa-manual/blob/main/src/unpriv/m-st-ext.adoc). RISC-V division by zero defines results; Pebble’s stop is a local design choice.
- [Cambridge EDSAC history](https://www.cl.cam.ac.uk/events/EDSAC99/history.html): first logged squares program, 6 May 1949, initial orders and subroutine work.
