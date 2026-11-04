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
