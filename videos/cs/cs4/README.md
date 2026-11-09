# Computer Science, Built — Part 4: Arithmetic

Part 4 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)). A machine has only finitely many bits, so its integers live on a clock and its reals
on a sparse, uneven ruler. The carry chain that makes addition slow turns, seen the right way, into a parallel prefix
computation; multipliers become trees of adders; division hides a table that cost Intel $475 million; and floating
point is carefully engineered, yet a wrong number can still bring down a rocket. Every circuit here is a netlist in
`explainer/cs/pebble/blocks.py`, checked against Python's integers (exhaustively where the inputs are few) and timed
gate by gate with `Circuit.settle` (unit delays, which sees through false paths); every number is computed in
`compute.py`.

* **Numbers that run out.** YouTube's 32-bit view counter (2014), the Boeing 787's 248-day generator bug (2015),
  `0.1 + 0.2`; integers on a clock and reals on an uneven ruler; objectives.
* **1. Bits as numbers.** Positional notation; Leibniz (1679); why two levels (noise, drawn); decimal to binary by
  halving; hexadecimal.
* **2. Integers on a clock.** Arithmetic mod 2ⁿ on a 4-bit wheel; two's complement as a relabelling (von Neumann,
  1945): one adder for signed and unsigned; negation = invert + 1, proved; sign extension; −(−128) = −128; overflow:
  unsigned is the carry out, signed is carry-in ≠ carry-out of the top bit; what C, Java, Go, Rust and Python do.
* **3. Adding, one bit at a time.** Binary addition by hand; half and full adders (five gates); the ripple-carry
  adder and subtraction as a + b̄ + 1; correctness by induction on the bits; the carry rippling, simulated
  (2n + 1 gate delays; 129 at 64 bits).
* **4. Carries in parallel.** Generate, propagate, kill; carry lookahead unrolled; a block as a function of its
  carry-in (kill, propagate, generate), so the carry operator (g, p) ∘ (g′, p′) = (g + pg′, pp′) is function
  composition and associative; the ripple chain, Kogge–Stone (1973), Brent–Kung (1982) and Sklansky (1960) drawn on
  16 positions (15/49/26/32 combines, depth 15/4/7/4, fan-out 2/2/2/9); Snir's size + depth ≥ 2n − 2 (1986).
* **5. The adders, raced.** Carry-select (O(√n)); carry-skip, whose deepest path (81 gates at 32 bits) is false and
  whose largest observed delay in these test vectors is 29; delay and gates for six designs from 4 to 64 bits; 64 bits: ripple 320 gates / 129
  delays, Kogge–Stone 1,094 / 15.
* **6. Multiplication.** Shift and add; the array multiplier (O(n)); carry-save addition as 3:2 compression; the
  Wallace tree (1964) compressing 8 → 6 → 4 → 3 → 2, and Dadda's (1965); Booth recoding (1951; radix 4, MacSorley
  1961) of 118 as 2·4³ − 4² + 2·4 − 2; measured at 16 bits: array 88 delays, Wallace 28, Dadda 25.
* **7. Division, and a famous bug.** Restoring division of 200 by 13, traced; non-restoring; radix-4 SRT (Sweeney,
  Robertson, Tocher, 1958) with redundant digits −2…2; our quotient-digit table (1,056 cells, each checked) drawn as a
  map; random divisions never visit 208 of its cells; the Pentium FDIV bug (Nicely, 1994: five of 1,066 entries
  missing, 4195835/3145727, about 1 in 9 billion divisions, $475 million) and a toy version: five emptied cells,
  18,603 of 2,000,000 divisions wrong; Newton–Raphson reciprocals with quadratic convergence (derived), Goldschmidt.
* **8. Pebble's ALU.** Adder/subtractor, logic, barrel shifter (left, right, arithmetic) and comparisons from one
  Kogge–Stone adder (sltu from the borrow, slt from the sign corrected by overflow); verified on all 655,360 cases at 8
  bits and on 20,000 random and worst-case inputs at 32 bits against the emulator's semantics; 1,900 gates, measured
  delay 29 (78 with a ripple adder).
* **9. Fixed point.** Q formats; money in integer cents; 0.1 = 0.0(0011)₂; dynamic range: Q16.16 covers 9 decades,
  float32 normal values span about 76 decades (subnormals extend the range with reduced precision).
* **10. Floating point.** IEEE 754 (1985, Kahan): sign, biased exponent, hidden bit; 0.1 as stored; every value of a
  6-bit float, bands doubling in spacing, subnormals; ulp and machine epsilon, the relative-spacing sawtooth;
  2²⁴ + 1 is not a float32; ±0, ±∞, NaN, gradual underflow; correctly rounded operations, ties to even.
* **11. Rounding error.** fl(x ∘ y) = (x ∘ y)(1 + δ); catastrophic cancellation in (1 − cos x)/x² and its stable
  rewrite; naive, pairwise and Kahan summation of a million float32 numbers, with their error bounds; the Patriot
  clock (1991: 0.34 s after 100 hours) and Ariane 5 (1996: a 64-bit float into a 16-bit integer).
* **12. Conditioning and stability.** Condition number against backward stability, error ≲ κu; Wilkinson's
  polynomial with the x¹⁹ coefficient moved by 2⁻²³, roots animated from 60-digit computations (16.73 ± 2.81i, …);
  root sensitivity k¹⁹/∏|k − j| (2.4 × 10⁹ for root 16); what numerical software learned.
* **13. Beyond IEEE.** binary64 to FP8, side by side; bfloat16 against binary16 and why machine learning chose range;
  FP8 (2022); interval arithmetic and the dependency problem; posits (2017); bignums.
* **14. Computing sin, exp and log.** Range reduction (Payne–Hanek for huge arguments); a Remez minimax polynomial
  for eˣ against Taylor's (17× smaller error, equioscillating); CORDIC (Volder, 1959) rotating by arctan 2⁻ⁱ with
  shifts and adds, run for 16 steps; the HP-35.
* **15. Frontier: arithmetic's open questions.** Multiplication measured on this machine: CPython's integers
  (Karatsuba) against `decimal`'s number-theoretic transform, faster at a million digits (the measured ratio and
  slopes are on screen and vary by machine and run). The race to n log n: Karatsuba (1960), Toom–Cook,
  Schönhage–Strassen (1971), Fürer (2007), Harvey and van der Hoeven (2019). The galactic crossover
  2^(1729¹²) is an illustrative asymptotic estimate, not a measured threshold. An unconditional linear lower bound
  is known; the network-coding conjecture implies Ω(n log n) **size for constant-degree Boolean circuits**
  (Afshani, Freksen, Kamma and Larsen, 2019), rather than an unconditional runtime bound.
  NumPy's float32 `exp` disagrees with a float64-then-float32 reference on about 39% of 10 million sampled inputs
  on this machine (by 1 ulp, rarely 2); 200 disagreements are rechecked at 200 bits. This does not certify all
  reference values. The table-maker's dilemma; structured worst-case searches; CORE-MATH's existing binary32
  and many binary64 routines, proofs for several binary64 functions, and the project's November 2026 report of
  seven binary64 functions integrated into glibc 2.43. Complete certified coverage, speed and adoption remain active work.
* **Recap, where this comes back, in practice, problems.**

## Build

```bash
python -m videos.cs.cs4.compute            # every number in the part (about a minute)
python tools/build.py cs4 -q l             # a 480p preview
python tools/build.py cs4                  # 1080p
```

## Problems, with solutions

1. **Two's complement.** Write −37 in 8 bits, and show that x ↦ x̄ + 1 fixes only 0 and −128.

   *Solution.* 37 = 00100101; inverted, 11011010; plus one, **11011011**. A fixed point satisfies x = −x mod 2⁸, so
   2x ≡ 0 (mod 256), x ≡ 0 (mod 128): x = 0 or x = 128, whose signed reading is −128. So −128 has no positive partner.

2. **Signed overflow.** Prove that a signed n-bit addition overflows exactly when the carry into the top bit differs
   from the carry out of it.

   *Solution.* Let the top bits be a, b, the carry into the top position c, the carry out c′, and the top sum bit
   s = a ⊕ b ⊕ c. Overflow means both operands have the same sign but the result has the other: a = b ≠ s. If
   a = b = 0, then c′ = 0 and s = c, so overflow ⇔ c = 1 ⇔ c ≠ c′. If a = b = 1, then c′ = 1 and s = c, so overflow
   ⇔ c = 0 ⇔ c ≠ c′. If a ≠ b, overflow is impossible, and c′ = c (the column propagates). So overflow ⇔ c ≠ c′, which
   one XOR gate detects.

3. **Kogge–Stone's size.** Show that a Kogge–Stone network on n = 2ᵏ positions has nk − n + 1 combines.

   *Solution.* At level l (reach d = 2ˡ) every position i ≥ d combines, n − 2ˡ of them. Summing over l = 0 … k − 1:
   nk − (2ᵏ − 1) = **nk − n + 1**. For n = 16: 64 − 16 + 1 = 49, as drawn in chapter 4 (and depth k = log₂ n).

4. **Carry-save.** Show that, bit by bit, x + y + z = (x ⊕ y ⊕ z) + 2·maj(x, y, z).

   *Solution.* In each column, the three bits xᵢ, yᵢ, zᵢ add up to a number from 0 to 3, which is sᵢ + 2cᵢ with sᵢ
   the parity (XOR) and cᵢ the majority — the full adder's truth table. Multiply column i by 2ⁱ and sum over i: the
   left side is x + y + z, the right side is the word of parities plus twice the word of majorities. No carry moves
   between columns, so the step takes one full-adder delay for any n.

5. **Floats.** How many float32 values lie in [1, 2)? In Python binary64, why is 0.5 + 0.25 = 0.75 exact, but 0.1 + 0.2 ≠ 0.3?

   *Solution.* In [1, 2) the exponent is fixed and the 23 fraction bits are free: **2²³ = 8,388,608** values (the same
   number in every binade [2ᵉ, 2ᵉ⁺¹) of normal numbers). 0.5, 0.25 and 0.75 are dyadic (denominators powers of two),
   exactly representable, and so is their exact sum, so correct rounding returns it unchanged. 0.1, 0.2 and 0.3 have
   infinite binary expansions; each is stored rounded, and the rounded 0.1 plus the rounded 0.2 is a different double
   from the rounded 0.3 (0.30000000000000004 against 0.29999999999999998…). This inequality is format-dependent: the corresponding float32 additions compare equal.

6. **Build: a carry-select adder.** With `explainer/cs/pebble/blocks.py`, build an 8-bit carry-select adder with
   blocks of 2, 3 and 3 bits; verify it on all inputs; compare it with ripple and Kogge–Stone.

   *Solution.* `carry_select_adder(8, [2, 3, 3])`, simulated on all 2¹⁷ inputs with `hdl.simulate`, matches a + b + c
   everywhere. Measured: **94 gates, settling in 12 gate delays**, against the ripple adder's 40 gates and 17 delays
   and Kogge–Stone's 70 gates and 9 delays (the default block sizes 1, 2, 3, 2 give 105 gates and also 12).

7. **★ Research: hard float32 exponential inputs.** Screen float32 inputs in [−87.33, 88.72] for eˣ
   close to a rounding midpoint. Recheck the candidates at high precision. What would certify that none was missed?

   *Experiment, and its limits.* `compute_hardround` screens 2,237,667,740 bit patterns in this interval using
   NumPy float64 `exp` (endpoints rounded to float32), then re-measures 200 candidates at 300 bits with mpmath. The count includes both signed
   zeros. It does not cover the entire float32 domain, including inputs whose exponentials are subnormal.
   No rigorous error bound for the float64 screen is established here, so its shortlist is an experiment,
   not a proof of the global hardest case.

   The closest shortlisted candidate is **x = −14.56709003448486328125**, with eˣ only **2.36 × 10⁻⁹ float32
   ulp** from a midpoint. The metric `24 − log₂(distance)` is about **52.7 bits**, a useful indication of the
   accuracy budget rather than an exact minimum precision theorem. The next candidates are −0.0073526 (51.7)
   and 1.5199 × 10⁻⁵ (51.6). At the first candidate the midpoint is about **1.265 binary64 ulps** away;
   correctly rounding eˣ to binary64 and then float32 gives the correct float32 result. Thus this candidate
   does **not** establish that binary64 precision is insufficient. A particular fast approximation still needs
   a certified total error bound; an interval enclosing a midpoint must trigger refinement or a fallback.

   To turn the experiment into a certificate, bound the screening error and candidate-selection margin,
   cover excluded domains and special cases, and validate high-precision rounding with error enclosures.
   Structured searches and lattice methods can prune enormous ranges; evaluating every input individually
   is not the only method. CORE-MATH already supplies many correctly rounded binary64 routines. Extending
   certified coverage and improving performance and adoption remain active work.

## 习题与解答

1. **补码。** 用 8 位写出 −37，并证明映射 x ↦ x̄ + 1 只把 0 和 −128 映到自身。

   *解答。* 37 = 00100101；取反得 11011010；加一得 **11011011**。不动点满足 x ≡ −x (mod 2⁸)，即 2x ≡ 0 (mod 256)，
   x ≡ 0 (mod 128)：x = 0 或 x = 128，后者按有符号读作 −128。所以 −128 没有正的搭档。

2. **有符号溢出。** 证明 n 位有符号加法溢出，当且仅当进入最高位的进位不等于从最高位出去的进位。

   *解答。* 设最高位为 a、b，进入最高位的进位为 c，出去的进位为 c′，最高位的和 s = a ⊕ b ⊕ c。溢出指两个操作数同号而结果
   异号：a = b ≠ s。若 a = b = 0，则 c′ = 0 且 s = c，溢出 ⇔ c = 1 ⇔ c ≠ c′。若 a = b = 1，则 c′ = 1 且 s = c，溢出 ⇔ c = 0
   ⇔ c ≠ c′。若 a ≠ b，不可能溢出，且 c′ = c（这一列传递进位）。所以溢出 ⇔ c ≠ c′，一个异或门就能检测。

3. **Kogge–Stone 的规模。** 证明 n = 2ᵏ 个位置上的 Kogge–Stone 网络有 nk − n + 1 个合并。

   *解答。* 在第 l 层（跨度 d = 2ˡ），每个 i ≥ d 的位置都合并一次，共 n − 2ˡ 个。对 l = 0 … k − 1 求和：
   nk − (2ᵏ − 1) = **nk − n + 1**。n = 16 时为 64 − 16 + 1 = 49，与第4章的图一致（深度 k = log₂ n）。

4. **进位保留。** 证明逐位地有 x + y + z = (x ⊕ y ⊕ z) + 2·maj(x, y, z)。

   *解答。* 每一列的三个位 xᵢ、yᵢ、zᵢ 之和在 0 到 3 之间，等于 sᵢ + 2cᵢ，其中 sᵢ 是奇偶（异或），cᵢ 是多数——这正是全加器的
   真值表。把第 i 列乘以 2ⁱ 再对 i 求和：左边是 x + y + z，右边是奇偶组成的字加上两倍的多数组成的字。各列之间没有进位移动，所以
   这一步对任何 n 都只需一个全加器的延迟。

5. **浮点数。** [1, 2) 中有多少个 float32 值？在 Python 的 binary64 算术中，为什么 0.5 + 0.25 = 0.75 是精确的，而 0.1 + 0.2 ≠ 0.3？

   *解答。* 在 [1, 2) 中指数固定，23 个小数位任取：共 **2²³ = 8,388,608** 个值（每个规格化的区间 [2ᵉ, 2ᵉ⁺¹) 都一样多）。
   0.5、0.25 和 0.75 都是二进分数（分母是 2 的幂），可以精确表示，它们的精确和也可以，所以正确舍入原样返回。0.1、0.2 和 0.3
   的二进制展开都是无限的；各自舍入后存储，舍入后的 0.1 加舍入后的 0.2，是一个与舍入后的 0.3 不同的双精度数
   （0.30000000000000004 对 0.29999999999999998…）。这个不等式依赖格式：对应的 float32 加法结果与 float32 的 0.3 相等。

6. **动手：进位选择加法器。** 用 `explainer/cs/pebble/blocks.py` 搭一个 8 位进位选择加法器，块大小为 2、3、3 位；在所有输入上
   验证；并与行波加法器和 Kogge–Stone 比较。

   *解答。* `carry_select_adder(8, [2, 3, 3])`，用 `hdl.simulate` 在全部 2¹⁷ 个输入上模拟，处处等于 a + b + c。测得：**94 个
   门，12 个门延迟后稳定**；行波加法器为 40 个门、17 个延迟，Kogge–Stone 为 70 个门、9 个延迟（默认块大小 1、2、3、2 为 105 个
   门，也是 12 个延迟）。

7. **★ 研究题：难舍入的单精度指数输入。** 在 [−87.33, 88.72] 内筛查使 eˣ 接近舍入中点的 float32 输入，
   再用高精度复核候选。要证明没有遗漏，还需要什么？

   *实验与局限。* `compute_hardround` 用 NumPy float64 `exp` 筛查这个区间内的 2,237,667,740 个位模式，
   端点先舍入到 float32，包括正负两个零，再用 mpmath 以 300 位精度复核 200 个候选。它不覆盖整个 float32 定义域，包括指数结果为非规格化数的区域。
   这里没有建立 float64 筛查误差的严格界，所以候选表是实验结果，不是全域最难情形的证明。

   候选中最近的是 **x = −14.56709003448486328125**，eˣ 离中点只有 **2.36 × 10⁻⁹ 个 float32 ulp**。
   `24 − log₂(距离)` 约为 **52.7 位**，用于表示精度预算，不能当作最小精度的精确定理。其次为 −0.0073526（51.7）
   和 1.5199 × 10⁻⁵（51.6）。第一个候选的中点距离约为 **1.265 个 binary64 ulp**；先把精确指数正确舍入到 binary64，
   再舍入到 float32，会得到正确结果。因此，这个候选**不能证明双精度不足**。具体快速近似仍需严格的总误差界；
   如果误差区间跨过中点，就必须提高精度或走后备路径。

   要把实验变成证书，需证明筛查误差和候选选取裕量，覆盖遗漏区域与特殊值，并用误差包围验证高精度舍入。
   结构化搜索和格方法能排除大片范围，不必逐一计算每个输入。CORE-MATH 已提供许多正确舍入的 binary64 例程；
   扩展有证明的覆盖范围、提升性能和推广采用，仍是活跃工作。

## Glossary additions

补码 two's complement · 溢出 overflow · 符号扩展 sign extension · 半加器 / 全加器 half / full adder · 行波进位加法器
ripple-carry adder · 生成 / 传递 / 消除 generate / propagate / kill · 超前进位 carry lookahead · 并行前缀 parallel prefix ·
进位选择 / 进位跳跃 carry-select / carry-skip · 伪路径 false path · 进位保留 carry-save · 华莱士树 Wallace tree · 布斯编码
Booth recoding · SRT 除法 SRT division · 牛顿–拉弗森迭代 Newton–Raphson iteration · 算术逻辑单元 ALU · 定点数 fixed point ·
浮点数 floating point · 规格化数 / 次正规数 normal / subnormal number · 末位单位 ulp · 机器精度 machine epsilon · 正确舍入
correctly rounded · 灾难性抵消 catastrophic cancellation · 补偿求和 compensated summation · 条件数 condition number · 向后稳定
backward stable · 区间算术 interval arithmetic · 最佳一致逼近 minimax approximation · CORDIC

## Sources

Books: Harris & Harris, *Digital Design and Computer Architecture*, ch. 1 and 5; Parhami, *Computer Arithmetic*;
Koren, *Computer Arithmetic Algorithms*; Higham, *Accuracy and Stability of Numerical Algorithms*, ch. 1–4; Muller et
al., *Handbook of Floating-Point Arithmetic*; Overton, *Numerical Computing with IEEE Floating Point Arithmetic*;
Knuth, *TAOCP* vol. 2, §4.1–4.3.

Papers and reports: Booth (1951); Robertson (1958); Tocher (1958); Sklansky, "Conditional-sum addition logic" (1960);
MacSorley (1961); Bedrij, carry-select (1962); Wallace (1964); Dadda (1965); Kahan, compensated summation (1965);
Kogge & Stone (1973); Brent & Kung (1982); Payne & Hanek (1983); Wilkinson, *Rounding Errors in Algebraic Processes*
(1963) and "The perfidious polynomial" (1984); Snir (1986); Goldberg, "What every computer scientist should know about
floating-point arithmetic" (1991); GAO IMTEC-92-26 (1992); Lions et al., *Ariane 5 Flight 501 Failure* (1996);
Edelman, "The mathematics of the Pentium division bug" (1997); Gustafson & Yonemoto (2017); Micikevicius et al., "FP8
formats for deep learning" (2022); IEEE 754 (1985, 2008, 2019); Volder (1959).

Technical scope checked on 9 November 2026: the FAA's [2015 directive](https://public-inspection.federalregister.gov/2015-10066.pdf)
reports a 248-day internal GCU counter overflow but does not specify its width or units; the centisecond example is illustrative.
The conditional circuit bound is stated in the [ICALP 2019 paper](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2019.10).
Current function coverage and integration claims come from [CORE-MATH](https://core-math.gitlabpages.inria.fr/) and its
[FAQ](https://core-math.gitlabpages.inria.fr/faq.html), not an independent proof audit.
Python's [`math.fsum` documentation](https://docs.python.org/3.12/library/math.html#math.fsum) records the possible double-rounding exception.
