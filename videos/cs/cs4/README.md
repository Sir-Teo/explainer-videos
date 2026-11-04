# Computer Science, Built — Part 4: Arithmetic

Part 4 of a fifty-five-part course in computer science (see [the series plan](../README.md) and
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
  whose measured delay is 29; delay and gates for six designs from 4 to 64 bits; 64 bits: ripple 320 gates / 129
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
  float32 76.
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

5. **Floats.** How many float32 values lie in [1, 2)? Why is 0.5 + 0.25 = 0.75 exact, but 0.1 + 0.2 ≠ 0.3?

   *Solution.* In [1, 2) the exponent is fixed and the 23 fraction bits are free: **2²³ = 8,388,608** values (the same
   number in every binade [2ᵉ, 2ᵉ⁺¹) of normal numbers). 0.5, 0.25 and 0.75 are dyadic (denominators powers of two),
   exactly representable, and so is their exact sum, so correct rounding returns it unchanged. 0.1, 0.2 and 0.3 have
   infinite binary expansions; each is stored rounded, and the rounded 0.1 plus the rounded 0.2 is a different double
   from the rounded 0.3 (0.30000000000000004 against 0.29999999999999998…).

6. **Build: a carry-select adder.** With `explainer/cs/pebble/blocks.py`, build an 8-bit carry-select adder with
   blocks of 2, 3 and 3 bits; verify it on all inputs; compare it with ripple and Kogge–Stone.

   *Solution.* `carry_select_adder(8, [2, 3, 3])`, simulated on all 2¹⁷ inputs with `hdl.simulate`, matches a + b + c
   everywhere. Measured: **94 gates, settling in 12 gate delays**, against the ripple adder's 40 gates and 17 delays
   and Kogge–Stone's 70 gates and 9 delays (the default block sizes 1, 2, 3, 2 give 105 gates and also 12).

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

5. **浮点数。** [1, 2) 中有多少个 float32 值？为什么 0.5 + 0.25 = 0.75 是精确的，而 0.1 + 0.2 ≠ 0.3？

   *解答。* 在 [1, 2) 中指数固定，23 个小数位任取：共 **2²³ = 8,388,608** 个值（每个规格化的区间 [2ᵉ, 2ᵉ⁺¹) 都一样多）。
   0.5、0.25 和 0.75 都是二进分数（分母是 2 的幂），可以精确表示，它们的精确和也可以，所以正确舍入原样返回。0.1、0.2 和 0.3
   的二进制展开都是无限的；各自舍入后存储，舍入后的 0.1 加舍入后的 0.2，是一个与舍入后的 0.3 不同的双精度数
   （0.30000000000000004 对 0.29999999999999998…）。

6. **动手：进位选择加法器。** 用 `explainer/cs/pebble/blocks.py` 搭一个 8 位进位选择加法器，块大小为 2、3、3 位；在所有输入上
   验证；并与行波加法器和 Kogge–Stone 比较。

   *解答。* `carry_select_adder(8, [2, 3, 3])`，用 `hdl.simulate` 在全部 2¹⁷ 个输入上模拟，处处等于 a + b + c。测得：**94 个
   门，12 个门延迟后稳定**；行波加法器为 40 个门、17 个延迟，Kogge–Stone 为 70 个门、9 个延迟（默认块大小 1、2、3、2 为 105 个
   门，也是 12 个延迟）。

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
