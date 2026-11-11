# Computer Science, Built — Part 28: Error-Correcting Codes

Part 28 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fourth part of Act V, *Limits and Secrets*. In 1947 Hamming's weekend jobs kept
dying on bad bits, so he taught the machine to fix them. Two years before Hamming published, Shannon had proved that
noise costs only a fixed fraction of a channel's rate. It took fifty years to build codes that reach his limit. This part builds
the codes from Hamming's to polar codes, runs every one of them, and scratches a QR code and reads it back.

The instrument is [`codes.py`](../../../explainer/cs/algo/codes.py). It holds:
* the binary symmetric channel, entropy and capacity;
* repetition codes; Hamming(7,4), general Hamming codes and SECDED;
* linear codes by enumeration; the [23,12,7] Golay code; the asymptotic bounds (Singleton, Hamming, Plotkin, MRRW, GV);
* GF(256) with exp/log tables (checked against carry-less multiplication); polynomials over it; irreducible and
  primitive polynomials by brute force;
* Reed–Solomon codes two ways:
  - the evaluation view over GF(p), with Lagrange interpolation for erasures and Berlekamp–Welch for errors;
  - the generator view over GF(256), with Berlekamp–Massey, Chien search and Forney's formula, errors and erasures
    together;
* a version-2 QR encoder (byte mode, all four error levels, mask selection by the standard's penalty rules) and a
  decoder that reads a damaged module matrix, with or without erasure information;
* CRCs as polynomial division; CRC-8 and CRC-32;
* random linear codes with maximum-likelihood syndrome decoding; the (7,5) convolutional code with Viterbi decoding;
* regular LDPC codes (Gallager's construction, with 4-cycles removed) under sum-product belief propagation, and BEC
  density evolution;
* polar codes: the transform, Bhattacharyya parameters and successive cancellation;
* LT fountain codes with the robust soliton and a peeling decoder; RAID-6 P+Q; the Hadamard code's two-query local
  decoder.

The rate–distance curves describe asymptotic binary code families; the short Hamming and Golay points can lie above
them. Finite codes obey finite-length bounds, including `k + d ≤ n + 1`. The perfect-code theorem restricts nontrivial
binary parameters, rather than identifying every nonlinear code with those parameters.

LDPC experiments stop when the receiver's parity checks pass, including when they pass for an incorrect codeword;
the sent word is used only to score the result. The (3,6) construction has design rate 1/2, and bounded swaps attempt
to remove four-cycles. Density-evolution thresholds are asymptotic numerical references. The polar experiment uses
a BEC-based frozen-set ordering and min-sum SC on the BSC; its finite results are not a capacity proof. Binary
two-query locally decodable codes require exponential length for constant noise and recovery guarantees; the
three-query length tradeoff remains open.

It is tested in `tests/test_cs28_codes.py`. The tests check:
* Hamming correcting every single error, and SECDED detecting doubles;
* the Golay weight distribution and perfection;
* the order of the bounds, including where the LP bound beats Hamming's;
* GF(256) inverses and tables;
* Reed–Solomon over GF(256) with errors and erasures together, up to 2e + f = 16;
* Lagrange and Berlekamp–Welch over GF(97);
* a QR round trip with 11 corrupted bytes;
* CRC-32 against `zlib.crc32`;
* Viterbi, LDPC and polar decoding on clean inputs, and BEC density evolution;
* RAID-6, LT and Hadamard local decoding.

Outside the tests, the QR encoder was compared module for module with the `qrcode` library (version 7.4.2, byte mode,
version 2, every mask and error level): identical in every case.

* **A scratched message.** Hook.
  - Hamming, the Model V and the two-out-of-five code.
  - Our QR code, "CS, Built: Part 28": a scratch over 56 modules corrupts 8 of its 44 bytes, and it still reads.
* **1. Noise and repetition.**
  - The BSC. Repetition at p = 0.1: 2.8% error at three copies, 1.6 × 10⁻⁷ at twenty-five, at 4% of the rate.
  - A 96 × 40 picture through BSC(0.05): 179 pixels wrong raw, 22 with three-fold repetition, 60 with Hamming(7,4).
* **2. Hamming distance.**
  - The 3-cube with the repetition code, and the 4-cube with the even-weight code.
  - d detects d − 1 errors and corrects ⌊(d − 1)/2⌋; erasures cost half.
* **3. Hamming(7,4).**
  - The Venn diagram: data 1011, a flip at position 5 located by circles A and C.
  - The parity-check matrix: the syndrome is 101 = 5. Perfection: 16 × 8 = 128.
  - The Hamming family up to (127,120), and SECDED (72,64).
  - Exact bit-error curves against repetition and no code, confirmed by simulation (8.7 × 10⁻⁴ at p = 0.01).
* **4. How good can a code be?**
  - The rate–distance plane: Singleton, Hamming, the LP bound (better than Hamming's above δ ≈ 0.12), and
    Gilbert–Varshamov.
  - The Golay code enumerated: 4,096 codewords; weights 7, 8, 11, 12, 15, 16 and 23 (253, 506, 1,288, 1,288, 506, 253,
    1); 4,096 × 2,048 = 2²³. Voyager; the Leech lattice.
* **5. Finite fields.**
  - Multiplication mod 7; why mod 8 fails.
  - GF(256) from x⁸ + x⁴ + x³ + x² + 1: the powers of α run through all 255 nonzero bytes; 0x57 × 0x83 = 0x31 by logs.
  - Of the 256 polynomials of degree 8, 30 are irreducible and 16 primitive. QR's 0x11d is primitive; AES's 0x11b is
    not.
* **6. Reed–Solomon.**
  - 2x² + 3x + 5 at x = 1, …, 9 (mod 1009). Three corrupted values are found and fixed by Berlekamp–Welch.
  - Six erased values are restored by Lagrange from the other three.
  - MDS; CDs, deep space, QR, RAID-6.
* **7. Our QR code.**
  - Anatomy: finders, timing, alignment, format, mask 0.
  - Where each of the 44 bytes lives; the decoder's trace on the scratch (22 syndromes, a locator of degree 8, Chien's 8
    roots equal to the 8 changed bytes).
  - Three damage cases:
    - scratch: 8 bytes wrong, read as errors;
    - blot: 15 wrong, 18 touched; fails as errors, read as erasures;
    - hole: 24 touched; fails both ways.
* **8. Cyclic codes and CRCs.**
  - Long division over GF(2) and the same division as a three-flip-flop shift register: remainder 100.
  - CRC-32 matches zlib.
  - CRC-8 on 64-byte messages: every burst of length ≤ 8 caught; bursts of 9 missed 0.75% (2⁻⁷); random damage missed
    0.39% (2⁻⁸).
* **9. Shannon's theorem.**
  - C = 1 − H(p).
  - Random [n, n/2] codes, decoded optimally for n = 8 to 28. At p = 0.05 the block error falls from 11% to 5%; at
    p = 0.15 it rises from 36% to 54%.
  - The random-coding argument and the converse.
* **10. Convolutional codes and Viterbi.**
  - The (7,5) trellis; Viterbi as dynamic programming.
  - 20,000 bits per point: 6.5 errors per 10,000 at 2% flips, none at 0.5%. Concatenation.
* **11. LDPC codes and belief propagation.**
  - The Tanner graph and message passing.
  - One block, round by round: 342 errors to 0 in 14 rounds at p = 0.07; stuck near 300 at 0.09.
  - The waterfall of a (3,6) code of length 4,800: zero failures in 100 trials up to p = 0.0725, almost none recovered
    past 0.09. The asymptotic BP reference is about 0.084 and Shannon's limit about 0.11.
  - BEC density evolution: a numerical threshold about 0.4294. History: Gallager, turbo codes, MacKay–Neal.
* **12. Polar codes.**
  - The N = 8 butterfly with its synthetic channels (erasure probability 0.004 to 0.996).
  - Polarization up to N = 1,024 (a third perfect, a third useless).
  - SC decoding at rate ½ for N = 256 and 1,024; 5G.
* **13. Codes for storage.**
  - RAID-6 rebuilding two lost disks.
  - Replication against RS(10,4) and Azure's LRC.
  - LT fountain overheads: 30%, 18% and 9% for 100, 1,000 and 10,000 blocks.
* **14. Frontier: capacity and locality.**
  - Reed–Muller codes achieve capacity (2016, 2023); list decoding and folded RS codes.
  - The Hadamard code's two-query decoder, measured against 1 − 2δ.
  - c³-LTCs and good quantum LDPC codes (2021).
  - Open problems. Outro.

## Build

```bash
python -m videos.cs.cs28.compute           # every number in the part (about a minute and a half)
python tools/build.py cs28 -q l            # a 480p preview
python tools/build.py cs28                 # 1080p
```

## Problems, with solutions

1. **Distance.** Prove that a code with minimum distance d detects d − 1 errors and corrects ⌊(d − 1)/2⌋, and that
   no code can do better.

   *Solution.* If at most d − 1 bits flip, the received word is within distance d − 1 of the codeword sent. It is
   therefore not another codeword, which would be at distance ≥ d, so the change is detected. Let t = ⌊(d − 1)/2⌋.
   If at most t bits flip, the received word y satisfies d(c, y) ≤ t. For any other codeword c′, the triangle
   inequality gives d(c′, y) ≥ d(c, c′) − d(c, y) ≥ d − t > t. So c is the unique nearest codeword.

   Optimality: take two codewords c, c′ at distance exactly d. Flipping d bits turns c into c′, which no decoder can
   detect. For correction, flip ⌈d/2⌉ of the positions where they differ, starting from c. The result is at distance
   ⌈d/2⌉ ≤ ⌊d/2⌋ + 1 from c, and ⌊d/2⌋ from c′. So when ⌈d/2⌉ = t + 1, nearest-codeword decoding picks c′ or ties.
   Since maximum likelihood on the BSC is nearest-codeword decoding, no decoder corrects all patterns of t + 1 errors.

2. **Reed–Solomon is MDS.** Show that with n distinct evaluation points and messages of degree < k, the distance is
   exactly n − k + 1.

   *Solution.* The code is linear, so its distance is the minimum weight of a nonzero codeword. A nonzero polynomial
   of degree < k has at most k − 1 roots, so its n values contain at most k − 1 zeros: the weight is at least
   n − k + 1. The polynomial (x − x₁)(x − x₂)⋯(x − x_{k−1}) has degree k − 1 and exactly k − 1 zeros among the
   points, so the weight n − k + 1 is attained. The Singleton bound says d ≤ n − k + 1 for every code, so RS codes
   meet it.

3. **CRC guarantees.** Prove that a CRC with generator g(x), g(0) = 1, deg g = r, detects every burst of length ≤ r,
   and every odd number of errors if (x + 1) divides g(x).

   *Solution.* An error goes undetected exactly when g(x) divides the error polynomial e(x). A burst of length
   ℓ ≤ r is e(x) = xⁱ b(x), with deg b = ℓ − 1 < r and b(0) = 1. Because g(0) = 1, g shares no factor with xⁱ. So
   g | xⁱ b would force g | b, impossible since deg b < deg g and b ≠ 0. For odd weight: if (x + 1) | g and g | e,
   then e(1) = 0 over GF(2). But e(1) is the parity of the number of error bits, which is 1 for an odd count. Chapter 8
   measured both properties for CRC-8 (whose generator x⁸ + x² + x + 1 = (x + 1)(x⁷ + x⁶ + x⁵ + x⁴ + x³ + x² + 1) contains x + 1).

4. **Density evolution.** Derive x ↦ ε(1 − (1 − x)⁵)² for the (3,6) code on BEC(ε), and find its threshold.

   *Solution.* Let x be the probability that a message from a bit to a check is "erased" (unknown), on a tree-like
   neighbourhood. A check can tell a bit its value only if all 5 of its other bits are known, which happens with
   probability (1 − x)⁵; so a check-to-bit message is erased with probability 1 − (1 − x)⁵. A bit stays erased if
   its channel value was erased (probability ε) and both of its other 2 checks are erased: x′ = ε(1 − (1 − x)⁵)².
   Decoding succeeds on long codes exactly when the iteration from x = ε goes to 0, that is, when
   x > ε(1 − (1 − x)⁵)² for all x in (0, ε]. Bisection, `codes.de_bec_threshold(3, 6)`, gives ε* ≈ 0.4294, against
   capacity's 0.5. The gap is the price of the regular (3,6) degree profile.

5. **Build: a version-1 QR code.** Encode a version-1 code (21 × 21) with this part's functions and check it against
   a phone.

   *Solution.* Version 1 drops the alignment pattern, and its dark module sits at (8, 13). Byte-mode capacities are
   17, 14, 11 and 7 characters for L, M, Q and H. The data codewords are 19, 16, 13 and 9, the check bytes 7, 10, 13
   and 17, in a single block. Changes to `codes.py`:
   - parametrize `QR_SIZE` to 21;
   - drop the alignment loop in `_qr_function_map`;
   - set the codeword counts;
   - keep everything else.

   The format bits, mask patterns, zigzag placement and `rs_encode` are unchanged. Check the result against
   `qrcode.QRCode(version=1, …)` with the same mask, as we did for version 2. Then display it with a quiet zone of four
   modules and scan it.

6. ★ **Research: short codes.** For block lengths 64 to 256 at rate ½ on the BSC, compare polar SC-list decoding,
   LDPC codes with BP, and the finite-length bound of Polyanskiy, Poor and Verdú.

   *Where to start.* Shannon's theorem is asymptotic. For short blocks, Polyanskiy, Poor and Verdú (2010) give the
   normal approximation log₂ M ≈ nC − √(nV) Q⁻¹(ε) + ½ log₂ n, where V is the channel dispersion. Coşkun et al.
   (2019) survey how today's codes compare with it at short lengths. Extend `codes.polar_sc` to a list decoder (keep
   the L best paths, CRC-aided; Tal and Vardy 2015), build short LDPC codes with progressive edge growth (Hu,
   Eleftheriou and Arnold 2005), and plot block error against p for each. Then ask how far each is from the bound at
   n = 128, and whether the gap shrinks as the list size grows. Nobody knows a practical decoder that reaches the
   bound at these lengths.

## 习题与解答

1. **距离。** 证明最小距离为 d 的码能检测 d − 1 个错误、纠正 ⌊(d − 1)/2⌋ 个错误，并且没有码能做得更好。

   *解答。* 若至多 d − 1 位翻转，收到的字与发送的码字距离至多 d − 1，因此不可能是另一个码字（那至少相距 d），所以变化会被检测到。设
   t = ⌊(d − 1)/2⌋。若至多 t 位翻转，收到的字 y 满足 d(c, y) ≤ t；对任何其他码字 c′，三角不等式给出 d(c′, y) ≥ d(c, c′) − d(c, y) ≥
   d − t > t，所以 c 是唯一最近的码字。最优性：取两个距离恰为 d 的码字 c、c′。翻转 d 位就把 c 变成 c′，任何解码器都无法察觉。至于纠错，
   从 c 出发，在它们不同的位置中翻转 ⌈d/2⌉ 个：结果与 c 相距 ⌈d/2⌉，与 c′ 相距 ⌊d/2⌋。所以当 ⌈d/2⌉ = t + 1 时，最近码字解码会选 c′
   或打平。由于在 BSC 上最大似然就是最近码字解码，没有解码器能纠正所有 t + 1 个错误的模式。

2. **Reed–Solomon 码是 MDS 码。** 证明用 n 个不同的求值点、次数 < k 的消息，距离恰为 n − k + 1。

   *解答。* 码是线性的，所以距离等于非零码字的最小重量。次数 < k 的非零多项式至多有 k − 1 个根，所以它的 n 个值中至多 k − 1 个为零：
   重量至少 n − k + 1。多项式 (x − x₁)(x − x₂)⋯(x − x_{k−1}) 次数为 k − 1，在这些点中恰有 k − 1 个零点，所以重量 n − k + 1 能达到。
   Singleton 界说对每个码都有 d ≤ n − k + 1，所以 RS 码达到了它。

3. **CRC 的保证。** 证明生成多项式 g(x) 满足 g(0) = 1、次数为 r 的 CRC 能检测每个长度 ≤ r 的突发错误；若 (x + 1) 整除 g(x)，还能
   检测每个奇数个错误。

   *解答。* 错误恰在 g(x) 整除错误多项式 e(x) 时漏检。长度 ℓ ≤ r 的突发是 e(x) = xⁱ b(x)，其中 deg b = ℓ − 1 < r 且 b(0) = 1。因为
   g(0) = 1，g 与 xⁱ 没有公因子，所以 g | xⁱ b 会推出 g | b，而 deg b < deg g 且 b ≠ 0，不可能。奇数重量：若 (x + 1) | g 且 g | e，则在
   GF(2) 上 e(1) = 0；但 e(1) 是错误位数的奇偶，奇数个时为 1。第 8 章对 CRC-8 测量了这两条性质（它的生成多项式 x⁸ + x² + x + 1 =
   (x + 1)(x⁷ + x⁶ + x⁵ + x⁴ + x³ + x² + 1) 含有因子 x + 1）。

4. **密度演化。** 推导 (3,6) 码在 BEC(ε) 上的递推 x ↦ ε(1 − (1 − x)⁵)²，并求出阈值。

   *解答。* 设 x 为在树状邻域上，从比特到校验的消息被「擦除」（未知）的概率。校验只有在它另外 5 个比特都已知时才能告诉一个比特它的值，
   概率为 (1 − x)⁵；所以校验到比特的消息被擦除的概率是 1 − (1 − x)⁵。一个比特保持被擦除，当且仅当它的信道值被擦除（概率 ε）且另外两个
   校验都被擦除：x′ = ε(1 − (1 − x)⁵)²。长码解码成功，恰好当从 x = ε 出发的迭代趋于 0，即对 (0, ε] 中所有 x 有 x > ε(1 − (1 − x)⁵)²。
   二分法，`codes.de_bec_threshold(3, 6)`，给出 ε* ≈ 0.4294，而容量是 0.5；差距是正则 (3,6) 度分布的代价。

5. **动手：版本 1 的二维码。** 用本部分的函数编码一个版本 1 的二维码（21 × 21），并用手机核对。

   *解答。* 版本 1 没有对齐图案；暗模块在 (8, 13)；字节模式容量为 L、M、Q、H 下 17、14、11、7 个字符；数据码字 19、16、13、9，校验字节
   7、10、13、17，都是单块。把 `QR_SIZE` 参数化为 21，去掉 `_qr_function_map` 里画对齐图案的循环，设置码字数，其余不变：格式位、掩码、
   之字形排布和 `rs_encode` 都一样。和我们对版本 2 做的一样，用相同掩码与 `qrcode.QRCode(version=1, …)` 对照，然后加上四个模块宽的静区
   显示出来并扫描。

6. ★ **研究：短码。** 在码长 64 到 256、码率 ½ 的 BSC 上，比较极化码的 SC 列表解码、用 BP 解码的 LDPC 码，以及 Polyanskiy、Poor 与
   Verdú 的有限长度界。

   *从哪里入手。* Shannon 定理是渐近的。对短块，Polyanskiy、Poor 与 Verdú（2010）给出正态近似 log₂ M ≈ nC − √(nV) Q⁻¹(ε) + ½ log₂ n，
   其中 V 是信道色散。Coşkun 等（2019）综述了当今的码在短码长下与它的比较。把 `codes.polar_sc` 扩展为列表解码器（保留 L 条最好的路径，
   用 CRC 辅助；Tal 与 Vardy 2015），用渐进边增长（Hu、Eleftheriou 与 Arnold 2005）构造短 LDPC 码，画出各自的块错误率对 p 的曲线。然后
   问：在 n = 128 时它们离这个界有多远，列表变大时差距是否缩小。在这些码长上，还没有人知道能达到这个界的实用解码器。

## Glossary additions

信道 channel · 二元对称信道 binary symmetric channel (BSC) · 擦除信道 erasure channel · 码率 rate · 重复码 repetition code ·
汉明距离 Hamming distance · 最小距离 minimum distance · 汉明码 Hamming code · 校验矩阵 parity-check matrix · 伴随式 syndrome ·
完美码 perfect code · SECDED 单纠错双检错 · Golay 码 Golay code · Singleton 界 Singleton bound · Gilbert–Varshamov 界 · 线性规划界
linear-programming bound · 有限域 finite field · 不可约多项式 irreducible polynomial · 本原多项式 primitive polynomial ·
Reed–Solomon 码 · 最大距离可分 MDS · 拉格朗日插值 Lagrange interpolation · 错误定位多项式 error-locator polynomial ·
擦除 erasure · 二维码 QR code · 循环冗余校验 CRC · 突发错误 burst error · 信道容量 channel capacity · 卷积码 convolutional code ·
网格图 trellis · Viterbi 算法 · 级联码 concatenated code · LDPC 码 low-density parity-check code · Tanner 图 · 置信传播 belief
propagation · 密度演化 density evolution · Turbo 码 · 极化码 polar code · 逐次消除 successive cancellation · 喷泉码 fountain code ·
纠删码 erasure code · 局部重构码 local reconstruction code · 局部可解码码 locally decodable code · 列表解码 list decoding ·
局部可测试码 locally testable code

## Sources

*Canon.* Books:
- MacKay, *Information Theory, Inference, and Learning Algorithms* (2003);
- Cover & Thomas, *Elements of Information Theory* (2nd ed., 2006), ch. 7;
- Guruswami, Rudra & Sudan, *Essential Coding Theory* (draft, 2023);
- MacWilliams & Sloane, *The Theory of Error-Correcting Codes* (1977);
- Roth, *Introduction to Coding Theory* (2006);
- Richardson & Urbanke, *Modern Coding Theory* (2008);
- Lin & Costello, *Error Control Coding* (2nd ed., 2004).

Papers:
- Foundations: Shannon (1948); Hamming (1950); Golay (1949); Gilbert (1952); Varshamov (1957); McEliece, Rodemich,
  Rumsey & Welch (1977); Tietäväinen (1973).
- Algebraic codes: Reed & Solomon (1960); Berlekamp (1968); Massey (1969); Welch & Berlekamp (1986); Chien (1964);
  Forney (1965, 1966); Peterson & Brown (1961); ISO/IEC 18004 (QR code).
- Probabilistic codes: Elias (1955); Viterbi (1967); Gallager (1962); Tanner (1981); Berrou, Glavieux & Thitimajshima
  (1993); MacKay & Neal (1996); Richardson & Urbanke (2001); Chung, Forney, Richardson & Urbanke (2001); Arıkan (2009);
  Tal & Vardy (2015).
- Storage: Patterson, Gibson & Katz (1988); Anvin, "The mathematics of RAID-6"; Luby (2002); Shokrollahi (2006);
  Huang et al. (2012); Muralidhar et al., "f4" (2014); Dimakis et al. (2010).
- Frontier: Kudekar et al. (2017); Abbe & Sandon (2023); Sudan (1997); Guruswami & Sudan (1999); Guruswami & Rudra
  (2008); Dinur, Evra, Livne, Lubotzky & Mozes (2022); Panteleev & Kalachev (2022); Polyanskiy, Poor & Verdú (2010);
  Coşkun et al. (2019).
