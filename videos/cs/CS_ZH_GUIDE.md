# Chinese edition of *Computer Science, Built* (计算机科学，从零搭建)

Translations live in each part's `zh_lines.py` (templates for lines computed from data) and
`videos/cs/csN/narration_zh.json` (keyed by the English line); check them with
`python tools/translate_narration.py csN --check` and `python tools/zh_lines.py csN --verify`.

- Spoken Mandarin, short sentences; same content and order as the English.
- Keep every `<bookmark mark='x'/>`, in order, before the words it times.
- Full-width punctuation; numbers as digits (47,176,870 步 → 4717万6870步 in speech is fine, digits on screen);
  Latin letters stay Latin (M, U, ⟨M⟩, BB(5), λ, NAND).
- Code, machine encodings, tape symbols and rule tables are data and never translated (`chip`, `TapeView` and
  `RuleTable` in `explainer.cs.viz` draw them verbatim). Comments and captions around them are translated.
- Names of people stay in their usual Chinese forms on first mention with the original after it where it helps
  (图灵 Turing, 丘奇 Church, 希尔伯特 Hilbert, 哥德尔 Gödel, 康托尔 Cantor, 巴贝奇 Babbage, 洛夫莱斯 Lovelace).
- On-screen text lives in `videos/cs/cs_text_zh.json` (exact `strings`, `phrases` inside `\text{}`, regex
  `patterns`); `python tools/collect_text.py --check csN` lists what is still English, and
  `python tools/collect_text.py --lang zh csN` dry-runs the Chinese build.

## Glossary

Extended by every part. Where the mainland textbook term and the industry term differ, the textbook term comes first
and the industry term follows in parentheses on first use.

| English | 中文 |
|---|---|
| computation, to compute | 计算 |
| algorithm | 算法 |
| mechanical procedure | 机械的程序（能行的过程） |
| decision problem (Entscheidungsproblem) | 判定问题 |
| decidable / undecidable | 可判定 / 不可判定 |
| Turing machine | 图灵机 |
| tape, cell, head | 纸带，格子，读写头 |
| state, halting state | 状态，停机状态 |
| transition table, rule | 转移表，规则 |
| blank symbol | 空白符号 |
| configuration | 格局 |
| step | 步 |
| halts / runs forever | 停机 / 永远运行下去 |
| the halting problem | 停机问题 |
| universal Turing machine | 通用图灵机 |
| description (encoding) of a machine ⟨M⟩ | 机器的描述（编码）⟨M⟩ |
| simulate, simulation | 模拟 |
| multitape machine | 多带图灵机 |
| nondeterministic | 非确定性的 |
| lambda calculus, λ-term | λ演算，λ项 |
| β-reduction, normal form | β归约，范式 |
| Church numeral | 丘奇数 |
| recursive function | 递归函数 |
| counter machine | 计数器机 |
| cellular automaton | 元胞自动机 |
| Church–Turing thesis | 丘奇–图灵论题 |
| extended Church–Turing thesis | 扩展的丘奇–图灵论题 |
| countable / uncountable | 可数 / 不可数 |
| diagonal argument | 对角线论证 |
| reduction | 归约 |
| busy beaver | 忙碌海狸 |
| computable function | 可计算函数 |
| Difference Engine / Analytical Engine | 差分机 / 分析机 |
| method of finite differences | 有限差分法 |
| the tower (of abstractions) | 抽象之塔 |
| layer | 层 |
| the Job | 那项任务（数词频） |
| ledger | 账本 |
| Pebble | Pebble（石子机） |
| in practice | 实践中 |
| invariant | 不变量 |
| a quantity that shrinks (variant) | 递减量（变式） |
| greatest common divisor | 最大公约数 |
| space-time diagram | 时空图 |
| palindrome | 回文 |
| lower bound | 下界 |
| communication complexity | 通信复杂性 |
| crossing sequence | 穿越序列 |
| decider / recognizer | 判定器 / 识别器 |
| Rice's theorem | 莱斯定理 |
| Rule 110, glider | 规则110，滑翔机 |
| Game of Life, glider gun | 生命游戏，滑翔机枪 |
| Gödel numbering | 哥德尔编码 |
| unary | 一进制 |
| stored-program computer | 存储程序计算机 |
| interpreter, emulator, virtual machine | 解释器，模拟器，虚拟机 |
| proof assistant | 证明助手 |
| tetration (10↑↑15) | 迭代幂（10↑↑15） |
| two's complement, sign extension | 补码，符号扩展 |
| overflow (signed / unsigned) | 溢出（有符号 / 无符号） |
| half adder, full adder | 半加器，全加器 |
| ripple-carry adder | 行波进位加法器 |
| generate, propagate, kill | 生成，传递，消除 |
| carry lookahead | 超前进位 |
| parallel prefix (Kogge–Stone, Brent–Kung, Sklansky) | 并行前缀（Kogge–Stone、Brent–Kung、Sklansky） |
| carry-select, carry-skip adder | 进位选择加法器，进位跳跃加法器 |
| false path | 伪路径 |
| carry-save addition, 3:2 compressor | 进位保留加法，三到二压缩器 |
| Wallace tree, Dadda tree | 华莱士树，达达树 |
| Booth recoding | 布斯编码 |
| restoring / non-restoring division, SRT | 恢复余数 / 不恢复余数除法，SRT 除法 |
| ALU | 算术逻辑单元 |
| fixed point, Q format | 定点数，Q 格式 |
| floating point, significand, biased exponent | 浮点数，有效数，偏置指数 |
| subnormal, gradual underflow | 次正规数，渐进下溢 |
| ulp, machine epsilon, unit roundoff u | 末位单位（ulp），机器精度，单位舍入误差 u |
| correctly rounded, ties to even | 正确舍入，平局取偶 |
| catastrophic cancellation | 灾难性抵消 |
| compensated (Kahan) summation | 补偿（卡亨）求和 |
| condition number, backward stable | 条件数，向后稳定 |
| interval arithmetic | 区间算术 |
| minimax polynomial, equioscillation | 最佳一致逼近多项式，等振荡 |
| range reduction | 自变量约化 |
| feedback, latch (SR, D), flip-flop (edge-triggered, master–slave) | 反馈，锁存器（SR、D），触发器（边沿触发、主从） |
| ring oscillator | 环形振荡器 |
| saddle point, eigenvalue, basin of attraction | 鞍点，特征值，吸引域 |
| setup time, hold time, clock-to-Q delay | 建立时间，保持时间，时钟到输出延迟 |
| clock skew, clock tree, clock gating, clock domain | 时钟偏斜，时钟树，时钟门控，时钟域 |
| metastability, synchronizer, MTBF | 亚稳态，同步器，平均故障间隔时间 |
| Buridan's principle | 布里丹原理 |
| finite-state machine (Moore, Mealy), state encoding (binary, Gray, one-hot) | 有限状态机（摩尔、米利），状态编码（二进制、格雷码、独热码） |
| finite automaton, regular language, Myhill–Nerode theorem, minimization | 有限自动机，正则语言，Myhill–Nerode 定理，最小化 |
| linear-feedback shift register (Fibonacci, Galois), primitive polynomial | 线性反馈移位寄存器（斐波那契、伽罗瓦接法），本原多项式 |
| register file, read port, write port, bypass (forwarding) | 寄存器堆，读端口，写端口，旁路（转发） |
| SRAM, DRAM, sense amplifier, bit line, word line | 静态随机存储器，动态随机存储器，读出放大器，位线，字线 |
| refresh, row buffer, bank, activate / precharge, row hit / conflict | 刷新，行缓冲，存储体，激活 / 预充电，行命中 / 行冲突 |
| Rowhammer, aggressor / victim row, TRR | 行锤攻击，攻击行 / 受害行，目标行刷新（TRR） |
| C-element, asynchronous circuit, arbiter | C 元件，异步电路，仲裁器 |
| ROM, PLA, microcode | 只读存储器，可编程逻辑阵列，微码 |
| delay line, Williams tube, core memory, core rope | 延迟线，威廉姆斯管，磁芯存储器，磁芯绳存储器 |
| stored-program computer, von Neumann architecture, von Neumann bottleneck | 存储程序计算机，冯·诺依曼体系结构，冯·诺依曼瓶颈 |
| program counter (pc), fetch / decode / execute | 程序计数器（pc），取指 / 译码 / 执行 |
| instruction set architecture (ISA), opcode, format (R, I, S, J) | 指令集体系结构，操作码，格式（R、I、S、J） |
| immediate, sign extension, little-endian | 立即数，符号扩展，小端序 |
| datapath, control unit, control word, control signal | 数据通路，控制单元，控制字，控制信号 |
| single-cycle, critical path, CPI, the iron law | 单周期，关键路径，每条指令周期数（CPI），性能铁律 |
| microcode, control store, microinstruction | 微码，控制存储器，微指令 |
| assembler, label, symbol table, pseudo-instruction, two-pass | 汇编器，标号，符号表，伪指令，两遍扫描 |
| object file, linker, relocation, loader | 目标文件，链接器，重定位，装入程序 |
| jump-and-link (jal), return address, Wheeler jump | 跳转并链接（jal），返回地址，惠勒跳转 |
| memory-mapped I/O, polling, interrupt, handler | 内存映射输入输出，轮询，中断，处理程序 |
| exception, trap, precise interrupt, system call, exception program counter | 异常，陷阱，精确中断，系统调用，异常程序计数器 |
| self-modifying code, index register (B-line), write xor execute, JIT | 自修改代码，变址寄存器（B 线），写异或执行，即时编译 |
| emulator, co-simulation, random program testing | 模拟器，协同仿真，随机程序测试 |
| the Job, the ledger | 任务，账本 |
| pipeline, stage, pipeline register, pipeline chart | 流水线，流水级，流水线寄存器，流水线图 |
| throughput, latency, the iron law, MIPS | 吞吐量，延迟，性能铁律，每秒百万条指令（MIPS） |
| hazard (structural, data, control), stall, bubble, flush | 冒险（结构、数据、控制），停顿，气泡，冲刷 |
| read-after-write, forwarding (bypass), load-use hazard, hazard unit | 写后读，转发（旁路），取数—使用冒险，冒险检测单元 |
| delay slot, branch penalty, misprediction | 延迟槽，分支代价，预测错误 |
| branch prediction (static, 1-bit, 2-bit saturating counter), global history, gshare, tournament, TAGE, perceptron predictor | 分支预测（静态、一位、两位饱和计数器），全局历史，gshare，锦标赛预测器，TAGE，感知机预测器 |
| branch target buffer (BTB), return-address stack (RAS) | 分支目标缓冲器（BTB），返回地址栈 |
| precise exception, commit | 精确异常，提交 |
| power wall, Dennard scaling, Amdahl's law, Gustafson's law | 功耗墙，登纳德缩放，阿姆达尔定律，古斯塔夫森定律 |
| branch-free code, conditional move | 无分支代码，条件传送 |
| limit study, prediction by partial matching (PPM), linearly separable, entropy rate | 极限研究，部分匹配预测（PPM），线性可分，熵率 |
| Frontier (chapter), research problem | 前沿（章），研究题 |
