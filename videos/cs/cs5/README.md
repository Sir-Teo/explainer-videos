# Computer Science, Built — Part 5: Memory and Time

Part 5 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). Connect a circuit's output back to its input and it can remember. Memory brings time
into the design, and a cost that never quite vanishes: a flip-flop can balance between 0 and 1 for an unbounded time.
The same machines that remember turn out to be the first rung of a theory of languages. Circuits with feedback are
simulated gate by gate with unit delays (`Loop` in `explainer/cs/pebble/seq.py`), clocked circuits cycle by cycle
(`Seq`); every number is computed in `compute.py`.

* **A circuit that remembers.** Combinational circuits forget; two NANDs in a loop hold a bit; a ball between two
  valleys and on the ridge; objectives.
* **1. Feedback.** The SR latch, wire by wire (set, reset, hold, the forbidden input); tick-by-tick waveforms,
  including the symmetric release that oscillates forever in the unit-delay model; the ring oscillator (period 2k in the binary unit-delay model, with physical oscillation requiring gain and delay).
* **2. Two wells and a saddle.** The cross-coupled inverters as τv̇₁ = f(v₂) − v₁, τv̇₂ = f(v₁) − v₂; the phase
  portrait (vector field, nullclines, trajectories) with two stable states and a saddle on the diagonal; the Jacobian
  at the saddle, RC-normalized eigenvalues −4 and +2, and t_resolve ≈ (τ/λ) ln(Δ/|δ|).
* **3. Latches, flip-flops and the clock.** The D latch (transparent and closed, simulated); the master–slave
  edge-triggered flip-flop (Q takes D at the rising edge); registers; the synchronous picture (state, logic, next
  state).
* **4. How fast can the clock go?** Setup, hold, clock-to-Q on a waveform; f_max = 1/(t_cq + t_logic + t_setup) on a
  budget bar; an assumed 290 ps worst-case logic budget (≈ 2.8 GHz with the stated register delays); clock skew, and why a hold violation cannot be fixed by
  slowing the clock.
* **5. Metastability.** A D change at the edge makes the simulated master oscillate; 40,000 random arrivals
  integrated through the latch equations: a histogram with an exponential tail, P(t > T) ∝ e^{−λT}; MTBF =
  e^{t_r/τ}/(T₀ f_clk f_data): illustrative constants yield about 10 hours versus 6 × 10¹⁸ years. The finite sample illustrates a tail,
  not an astronomical reliability certificate; single-bit synchronizers do not solve bus coherence or pulse capture.
* **6. Finite-state machines.** A Moore detector for 1011, run on a stream; Mealy against Moore; binary, Gray and
  one-hot encodings synthesized with Quine–McCluskey (with don't-cares), built and simulated: 3/3/5 flip-flops,
  14/24/15 gates.
* **7. Machines and languages.** A six-state DFA for multiples of 3 (state = value mod 6); the Myhill–Nerode theorem
  (1958), proved; partition refinement merging it to 3 states; Hopcroft's n log n (1971); {0ⁿ1ⁿ} is not regular; the
  ladder to Parts 12, 25 and 1.
* **8. Counters and shift registers.** The counter; the shift register; a 4-bit LFSR running through all 15 non-zero
  states; LFSRs as multiplication by x modulo a monic polynomial with constant term 1 (a field only when irreducible);
  primitive polynomials and nonzero seeds give full period; every such feedback polynomial of degree 2–8,
  simulated: the maximal ones number φ(2ⁿ − 1)/n (16 at degree 8); CRCs, stream ciphers, scramblers, GPS, BIST.
* **9. Pebble's register file.** Sixteen 32-bit registers (r0 hard-wired to 0), a decoder for the write port, a
  multiplexer per bit to load or keep, two 16-to-1 multiplexer trees for the read ports: 480 flip-flops and 5,824
  gates in the chosen gate basis, verified against a Python model; what each extra port costs.
* **10. Static memory.** The 6T SRAM cell (cross-coupled inverters and two access transistors), bit lines, word
  lines and sense amplifiers; cells in a grid.
* **11. Dynamic memory.** Dennard's 1T1C idea (1966), destructive sensing and immediate restoration, Intel 1103's early 3T cell
  (1970); a common 64 ms refresh interval at normal temperature (device dependent); activate, read, precharge and
  row buffers. DDR4 defaults to burst length 8; DDR5 to 16. The 20× area comparison is an illustrative cell model.
* **12. When memory leaks.** Rowhammer (Kim et al., 2014: 110 of 129 DDR3 modules, as few as 139,000 activations);
  Project Zero's page-table exploit (2015), JavaScript and Android (2016), TRR and TRRespass (2020); leaky
  abstractions.
* **13. Clocks, and memory as logic.** The synchronous discipline and its cost; the Muller C-element and asynchronous
  handshakes; ROMs, PLAs and FPGAs as memory doing logic; microcode previewed.
* **14. Remembering, before chips.** Mercury delay lines (EDSAC), Williams tubes (the Manchester Baby), core memory
  (Forrester, Whirlwind 1953; coincident-current selection and destructive reads), the Intel 1103, flash.
* **15. Frontier: defending memory.** Historical thresholds: 139,000 toggles (2014); as few as 4,800 activations
  **per aggressor in a two-aggressor experiment** (2020), with mitigations disabled. A teaching model uses
  W = 1,383,783 activations per bank per 64 ms. Independent coins refresh all modeled victim neighbours.
  With N = ceil(seconds per year / t_RC), the union bound N(1 − p)^T ≤ 10⁻² covers overlapping runs:
  p ≈ 0.03%, 0.4%, 3.8% at T = 139,000, 10,000, 1,000. This all-neighbour variant differs from original PARA.
  Positive Misra–Gries counters are removed after immediate modeled refresh. In one aligned window the
  undercount is at most floor(W/(k + 1)); k ≥ 2W/T is sufficient, not a minimum or a physical DRAM guarantee.
  Four or 16 counters allow 60,739 unrefreshed activations on the chosen trace; 64 and 277 stay below T on that
  trace. Graphene (Park et al., 2020) uses additional spillover machinery. CoMeT (2024) never undercounts under
  its specified update/reset rules; collisions can cause extra refreshes. Half-Double, RowPress and PRAC expose
  further physical/model constraints. AutoPRAC (June 2026 preprint) reports a reset-policy flaw; this lesson
  attributes that finding without independently auditing the paper's proof.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs5.compute            # every number in the part (under a minute)
python tools/build.py cs5 -q l             # a 480p preview
python tools/build.py cs5                  # 1080p
```

## Problems, with solutions

1. **A NOR latch.** Build an SR latch from two NOR gates. Which input is forbidden now, and what do the outputs do?

   *Solution.* Q = NOR(R, Q̄), Q̄ = NOR(S, Q), with active-high inputs: S = 1 forces Q̄ = 0 and then Q = 1; R = 1 forces
   Q = 0; S = R = 0 holds. The forbidden input is **S = R = 1**, which forces **both outputs to 0**; an exactly symmetric analog release can remain at the unstable equilibrium; the binary unit-delay model
   can oscillate instead. Real mismatch and noise usually break the symmetry.

2. **The fastest clock.** t_cq = 50 ps, t_setup = 30 ps, slowest logic path 420 ps. What is f_max? What if the clock
   reaches the second register 20 ps late?

   *Solution.* T ≥ 50 + 420 + 30 = 500 ps, so **f_max = 2 GHz**. With 20 ps of skew in the capturing register's
   favour, the setup inequality becomes 500 ≤ T + 20, so T ≥ 480 ps and f_max ≈ **2.08 GHz**; but the hold check
   t_cq + t_logic,min ≥ t_hold + 20 ps is now 20 ps harder on the shortest path.

3. **Synchronizer design.** τ = 25 ps, T₀ = 20 ps, f_clk = 2 GHz, f_data = 50 MHz. How long must a synchronizer
   wait for an MTBF of 1000 years?

   *Solution.* T₀ f_clk f_data = 20·10⁻¹² · 2·10⁹ · 5·10⁷ = 2·10⁶ s⁻¹, and 1000 years ≈ 3.16·10¹⁰ s. So
   e^{t_r/τ} ≥ 6.3·10¹⁶, t_r ≥ 25 ps · ln(6.3·10¹⁶) ≈ 25 · 38.7 ps ≈ **0.97 ns**: about two 0.5 ns clock cycles, so
   three flip-flops in this idealized budget (two cycles of resolution time). Real paths must subtract register
   and routing delays and use characterized constants; this is not an implementation sign-off.

4. **A Moore machine.** Draw a Moore machine that outputs 1 when the number of 1s read so far is divisible by 3. Is it
   minimal?

   *Solution.* Three states c₀, c₁, c₂ (the count of 1s mod 3), start c₀, output 1 in c₀ only; a 1 moves cᵢ → cᵢ₊₁, a
   0 stays. It is **minimal**: the suffixes ε, 11 and 1 distinguish the three states pairwise (from c₀, ε is accepted;
   from c₁, "11" is; from c₂, "1" is), so there are three Myhill–Nerode classes.

5. **Palindromes are not regular.** Use Myhill–Nerode to show no finite automaton recognizes the palindromes over
   {0, 1}.

   *Solution.* Take the prefixes xᵢ = 0ⁱ1 for i = 0, 1, 2, …. For i ≠ j the suffix z = 0ⁱ gives xᵢz = 0ⁱ10ⁱ, a
   palindrome, but xⱼz = 0ʲ10ⁱ, which is not. So the xᵢ are pairwise inequivalent: **infinitely many classes**, and
   no finite automaton can recognize the language.

6. **Build: every 5-bit LFSR.** With `explainer/cs/pebble/seq.py`, find the period of every 5-bit LFSR, and check that
   exactly φ(31)/5 = 6 are maximal.

   *Solution.* Tap bit 4 (so the register really has length 5) plus any subset of bits 0–3: 16 registers. Run each
   with `lfsr(taps, 5)` from state 1 until it returns. The periods are **5, 6, 8, 12, 14, 14, 15, 15, 21, 21** and six
   times **31**; the maximal tap sets are {4, 1}, {4, 2}, {4, 0, 1, 2}, {4, 0, 1, 3}, {4, 0, 2, 3} and {4, 1, 2, 3}.
   31 is prime, so φ(31)/5 = 30/5 = **6**.

7. **★ Research: verify a bounded-window tracker.** Prove the undercount bound in the stated finite model.
   Test `[0,0] + [1]*20` with one counter and trigger 2. What must a physical guarantee also model?

   *Solution and starting point.* Every full-table decrement consumes k tracked events plus the incoming event,
   so there are at most floor(W/(k+1)) decrements. For each row, since its last immediate modeled victim refresh,
   the true count exceeds its estimate by at most this total. Triggering at T/2 therefore keeps the count at
   most T when floor(W/(k+1)) ≤ T/2. This is a sufficient bound inside one aligned window, not a universal
   counter lower bound. Delete a row's counter after refresh: retaining a zero can produce a negative ghost
   entry on the next full-table miss. The regression stream then gives maximum unrefreshed counts `{0:2,1:2}`;
   the defective version gives `{0:2,1:20}`. A physical proof must also account for multiple aggressors, window
   alignment, reset policies, refresh queues, row-open time and device assumptions. Compare Graphene's spillover
   table and CoMeT's count-min upper estimates; investigate formally checked guarantees and their implementation
   cost. AutoPRAC (Qu and Saileshwar, June 2026 preprint) is a dated reported example of reset-policy analysis.

## 习题与解答

1. **或非锁存器。** 用两个或非门搭一个 SR 锁存器。现在哪个输入是禁止的？输出会怎样？

   *解答。* Q = NOR(R, Q̄)，Q̄ = NOR(S, Q)，输入高电平有效：S = 1 迫使 Q̄ = 0，进而 Q = 1；R = 1 迫使 Q = 0；S = R = 0
   时保持。禁止的输入是 **S = R = 1**，它迫使**两个输出都为 0**；在理想模拟模型中完全对称地释放，可停在不稳定平衡点；二值单位延迟模型则可能振荡。实际失配与噪声通常会打破对称性。

2. **最快的时钟。** t_cq = 50 ps，t_setup = 30 ps，最慢的逻辑路径为 420 ps。f_max 是多少？如果时钟到达第二个寄存器晚了 20 ps
   呢？

   *解答。* T ≥ 50 + 420 + 30 = 500 ps，所以 **f_max = 2 GHz**。有 20 ps 对捕获寄存器有利的偏斜时，建立条件变为
   500 ≤ T + 20，于是 T ≥ 480 ps，f_max ≈ **2.08 GHz**；但保持检查 t_cq + t_logic,min ≥ t_hold + 20 ps 对最短路径变严了
   20 ps。

3. **设计同步器。** τ = 25 ps，T₀ = 20 ps，f_clk = 2 GHz，f_data = 50 MHz。要让平均故障间隔达到 1000 年，同步器要等多久？

   *解答。* T₀ f_clk f_data = 20·10⁻¹² · 2·10⁹ · 5·10⁷ = 2·10⁶ s⁻¹，1000 年 ≈ 3.16·10¹⁰ s。所以 e^{t_r/τ} ≥ 6.3·10¹⁶，
   t_r ≥ 25 ps · ln(6.3·10¹⁶) ≈ 25 · 38.7 ps ≈ **0.97 ns**：约两个 0.5 ns 的时钟周期，因此要用三个串联的触发器（两个周期的
   决断时间）。这是理想预算；实际路径还须扣除寄存器与布线延迟，使用实测常数，并验证实现。

4. **摩尔机。** 画一个摩尔机：当已读到的 1 的个数能被 3 整除时输出 1。它是最小的吗？

   *解答。* 三个状态 c₀、c₁、c₂（1 的个数模 3），初态 c₀，只在 c₀ 输出 1；读 1 使 cᵢ → cᵢ₊₁，读 0 不变。它是**最小的**：后缀
   ε、11 和 1 两两区分这三个状态（从 c₀ 出发 ε 被接受；从 c₁ 出发 "11" 被接受；从 c₂ 出发 "1" 被接受），所以有三个
   Myhill–Nerode 类。

5. **回文不是正则的。** 用 Myhill–Nerode 定理证明，没有有限自动机能识别 {0, 1} 上的回文。

   *解答。* 取前缀 xᵢ = 0ⁱ1，i = 0, 1, 2, …。对 i ≠ j，后缀 z = 0ⁱ 使 xᵢz = 0ⁱ10ⁱ 是回文，而 xⱼz = 0ʲ10ⁱ 不是。所以 xᵢ
   两两不等价：**有无穷多个类**，没有有限自动机能识别这个语言。

6. **动手：所有 5 位 LFSR。** 用 `explainer/cs/pebble/seq.py` 求出每个 5 位 LFSR 的周期，并验证恰有 φ(31)/5 = 6 个达到最大
   周期。

   *解答。* 抽头取第 4 位（这样寄存器长度确实为 5），再加第 0–3 位的任意子集：共 16 个寄存器。用 `lfsr(taps, 5)` 从状态 1
   运行到回到起点。周期为 **5、6、8、12、14、14、15、15、21、21**，以及六个 **31**；达到最大周期的抽头集合是 {4, 1}、
   {4, 2}、{4, 0, 1, 2}、{4, 0, 1, 3}、{4, 0, 2, 3} 和 {4, 1, 2, 3}。31 是素数，所以 φ(31)/5 = 30/5 = **6**。

7. **★ 研究题：验证有限窗口跟踪器。** 证明所述有限模型中的低估界。用一个计数器、触发值 2 测试
   `[0,0] + [1]*20`。物理保证还需建模哪些因素？

   *解答与起点。* 每次全表递减消耗 k 个已跟踪事件和当前输入事件，所以最多发生 floor(W/(k+1)) 次。
   自一行上次在模型中立即触发受害行刷新以来，它的实际计数与估计值之差不超过该总次数。因此，当
   floor(W/(k+1)) ≤ T/2 时，在 T/2 触发刷新可将实际计数限制在 T 内。这是一个对齐窗口内的充分条件，
   并非通用的计数器数量下界。刷新后必须删除该行计数器：若保留零项，下次表满且未命中时会产生负数幽灵项。
   回归序列中各行未刷新计数的最大值应为 `{0:2,1:2}`；有缺陷的版本得到 `{0:2,1:20}`。
   物理证明还需考虑多个攻击行、窗口对齐、重置策略、刷新队列、行开启时长和器件假设。比较 Graphene 的溢出表
   与 CoMeT 的 count-min 上估计，并研究形式化验证保证及其实现开销。Qu 与 Saileshwar 的 AutoPRAC
   （2026 年 6 月预印本）是报告重置策略分析的一个有明确日期的案例。

## Glossary additions

反馈 feedback · SR 锁存器 SR latch · D 锁存器 D latch · 触发器 flip-flop · 主从触发器 master–slave flip-flop · 时钟
clock · 寄存器 register · 建立时间 / 保持时间 setup / hold time · 时钟到输出延迟 clock-to-Q · 时钟偏斜 clock skew · 亚稳态
metastability · 同步器 synchronizer · 平均故障间隔 MTBF · 相图 phase portrait · 鞍点 saddle · 有限状态机 finite-state
machine · 摩尔机 / 米利机 Moore / Mealy machine · 独热码 one-hot · 格雷码 Gray code · 有限自动机 finite automaton · 正则语言
regular language · Myhill–Nerode 定理 · 状态最小化 state minimization · 计数器 counter · 移位寄存器 shift register · 线性
反馈移位寄存器 LFSR · 本原多项式 primitive polynomial · 寄存器堆 register file · 静态 / 动态随机存储器 SRAM / DRAM · 读出
放大器 sense amplifier · 字线 / 位线 word line / bit line · 刷新 refresh · 行缓冲 row buffer · 行锤攻击 Rowhammer · 异步
电路 asynchronous circuit · C 元件 C-element · 只读存储器 ROM · 可编程逻辑阵列 PLA · 微码 microcode · 磁芯存储器 core memory

## Sources

Books: Harris & Harris, *Digital Design and Computer Architecture*, ch. 3; Nisan & Schocken, *The Elements of
Computing Systems*, ch. 3; Sipser, *Introduction to the Theory of Computation*, ch. 1; Hopcroft, Motwani & Ullman,
ch. 4; Jacob, Ng & Wang, *Memory Systems: Cache, DRAM, Disk*; Golomb, *Shift Register Sequences*; Strogatz,
*Nonlinear Dynamics and Chaos*, ch. 6.

Papers: Mealy (1955); Moore, "Gedanken-experiments on sequential machines" (1956); Myhill (1957); Nerode, "Linear
automaton transformations" (1958); Muller & Bartky (1959); Hopcroft, "An n log n algorithm for minimizing states in a
finite automaton" (1971); Chaney & Molnar, "Anomalous behavior of synchronizer and arbiter circuits" (1973); Dennard,
DRAM patent (1968); Ginosar, "Metastability and synchronizers: a tutorial" (2011); Kim et al., "Flipping bits in
memory without accessing them" (2014); Seaborn & Dullien (2015); Frigo et al., "TRRespass" (2020).

Primary checks for this revision: [IBM DRAM history](https://www.ibm.com/history/dram);
[Micron DDR5 features](https://www.micron.com/content/dam/micron/global/public/products/white-paper/ddr5-new-features-white-paper.pdf);
[Lamport's dated manuscript](https://lamport.azurewebsites.net/pubs/buridan.pdf) (1984; published 2012);
[Kim et al. 2020](https://arxiv.org/abs/2005.13121);
[Graphene](https://microarch.org/micro53/papers/738300a001.pdf);
[CoMeT](https://arxiv.org/html/2402.18769v1);
[AutoPRAC](https://arxiv.org/abs/2606.23905) (submitted 22 June 2026; preprint attribution).
