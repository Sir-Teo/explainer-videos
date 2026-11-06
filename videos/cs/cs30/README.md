# Computer Science, Built — Part 30: Public Keys

Part 30 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the last part of Act V, *Limits and Secrets*. Two strangers can agree on a secret while
everyone listens. That took Diffie and Hellman (1976), RSA (1977) and the number theory of groups. Elliptic curves made
it compact, and lattices may keep it safe against a quantum computer. Two of our machines end the part by running a
TLS 1.3-style handshake. Everything is built from scratch and run; **the code is for learning, never for real use**.

The instrument is `explainer/cs/algo/pubkey.py`. It holds:
* number theory: extended Euclid with a trace, inverses, square-and-multiply with a trace, the CRT, Miller–Rabin,
  generators and orders;
* Merkle's puzzles; Diffie–Hellman and its man in the middle;
* RSA:
  - key generation, CRT decryption;
  - OAEP with MGF1-SHA-256, and hash-and-sign;
  - PKCS #1 v1.5 padding, and Bleichenbacher's attack with a trace of the shrinking interval;
* factoring: Brent's variant of Pollard's rho, the rho walk itself, and a quadratic sieve (Tonelli–Shanks roots, log
  sieving, linear algebra over GF(2));
* discrete logs: baby-step giant-step, Pollard's rho in a prime-order subgroup, Pohlig–Hellman, and a toy index
  calculus;
* elliptic curves:
  - affine arithmetic, P-256, a toy curve over GF(97);
  - ECDSA with RFC 6979 nonces, and nonce-reuse key recovery;
  - X25519 (RFC 7748's Montgomery ladder);
* ECDSA certificates and chain verification; HKDF and TLS 1.3's labelled expansion; a TLS 1.3-shaped handshake
  (X25519, a certificate chain, CertificateVerify, Finished MACs and AES-128-GCM from Part 29);
* lattices:
  - Gauss reduction with every step, and exact LLL;
  - a Merkle–Hellman knapsack and the Lagarias–Odlyzko attack;
  - Regev's LWE encryption;
  - ML-KEM's ring arithmetic (FIPS 203's NTT, base multiplication and centred binomial noise), and a K-PKE with
    ML-KEM-512's parameters, using our own sampling instead of SHAKE and no byte encodings;
* Lamport one-time signatures; Schnorr signatures with Fiat–Shamir; Shamir secret sharing.

It is tested in `tests/test_cs30_pubkey.py`:
* X25519 against RFC 7748;
* HKDF against RFC 5869's first test case;
* P-256 ECDSA against RFC 6979 A.2.5 (the public key, and r and s for "sample"; n·G = O);
* Euclid, the CRT, Miller–Rabin (including the Carmichael number 561), generators;
* BSGS, Pohlig–Hellman and index calculus; rho and the sieve on a 20-digit semiprime;
* RSA with and without CRT, OAEP, signatures, and Bleichenbacher's attack on a 256-bit key;
* nonce-reuse recovery, and every check of the handshake;
* Gauss reduction (same covolume), the knapsack attack, the NTT against schoolbook multiplication, K-PKE and LWE
  round trips;
* Lamport, Schnorr and Shamir.

Outside the tests, the `cryptography` library (version 50) cross-checked our code:
* it decrypted our RSA-OAEP ciphertexts, and we decrypted its;
* it verified our ECDSA signatures;
* its X25519 agreed with ours.

* **Two strangers, one secret.** Hook.
  - Diffie–Hellman with p = 23 and g = 5: A = 8, B = 19, shared secret 2.
  - The same exchange in RFC 3526's 2048-bit group: 27 ms in Python.
* **1. Key distribution and Merkle's puzzles.**
  - n(n−1)/2 keys.
  - Merkle's puzzles at n = 100, 1,000 and 10,000: Bob took 60, 178 and 2,110 tries, against Eve's n²/4.
  - GCHQ's earlier discoveries.
* **2. Modular arithmetic.**
  - The clock. Extended Euclid on (240, 46): 240·(−9) + 46·47 = 2.
  - 17⁻¹ mod 3120 = 2753.
  - 3²¹⁸ mod 1000 = 489 by eight squarings and five multiplications.
* **3. Groups and the discrete logarithm.**
  - Powers of 5 mod 23 visit all 22 elements. The orders are 1, 2, 11 and 22 (Lagrange); Fermat and Euler.
  - 2ˣ mod 1019 as a scatter.
* **4. Diffie–Hellman.** Paint; the mathematics; CDH and DDH; Mallory's two keys (15 and 8).
* **5. RSA.**
  - p = 61, q = 53, e = 17, d = 2753: 65 → 2790 → 65.
  - The proof via Euler and the CRT.
  - A 2048-bit key: the prime searches took 354, 99 and 360 candidates against the 355 expected, and the key 0.7 s.
    Decryption takes 29 ms, or 8.9 ms with the CRT.
  - Textbook malleability; OAEP; signing.
* **6. Bleichenbacher's oracle.**
  - PKCS #1 v1.5 and the oracle.
  - 33,392 queries for a 256-bit key and 128,789 for a 384-bit one, with the uncertainty curve. ROBOT; TLS 1.3.
* **7. Factoring.**
  - The rho walk mod 1009: a tail of 7 and a cycle of 14; gcd = 1009.
  - Rho against our sieve from 10 to 34 digits.
  - A smooth relation and a GF(2) dependency of 46 relations on a 20-digit n.
  - The NFS and the factoring records.
* **8. Discrete logarithms.**
  - BSGS from 24 to 40 bits.
  - Pohlig–Hellman on an 84-bit prime with smooth p − 1, solved in 0.6 ms, against a safe prime.
  - Index calculus on a 30-bit prime: 22 primes, 37 relations. Logjam.
* **9. Elliptic curves.**
  - Over ℝ: (−1, 1) + (0, 1) = (1, −1), and 2·(−1, 1) = (3, −5).
  - Over GF(97): 99 points and 𝒪, and a generator of order 50.
  - P-256 scalar multiplication in 21 ms; key sizes; X25519 against RFC 7748.
* **10. Signatures.**
  - ECDSA, and RFC 6979's vector.
  - Two signatures with one nonce: k and d recovered, and a forged signature that verifies; the PS3.
* **11. Certificates and trust.**
  - A three-certificate chain verifies; a tampered leaf and a self-signed impostor are rejected.
  - DigiNotar; Certificate Transparency; Let's Encrypt.
* **12. TLS 1.3.**
  - The handshake between two of our machines, with message sizes; every check passes.
  - The key schedule; forward secrecy.
* **13. Shor's threat.**
  - Periods of 7 mod 15 (r = 4 → 3·5), of 2 mod 21 and of 2 mod 35.
  - Harvest now, decrypt later; FIPS 203–205; hybrids.
* **14. Lattices.**
  - Gauss reduction from (90, 123), (56, 76) to (−6, 3), (−2, −7).
  - LLL recovers all 20 bits of a knapsack.
  - LWE decryptions: 400 of 400 correct, with their noise.
  - The NTT is about 12× faster than schoolbook. Our ML-KEM-512 arithmetic decrypts 25,600 bits with no errors.
    Lamport; SLH-DSA.
* **15. Zero knowledge, sharing and computing on secrets.**
  - Schnorr identification and Fiat–Shamir.
  - Shamir sharing over GF(2⁶¹ − 1): any three of five shares give 31337, two give garbage.
  - MPC and FHE.
* **16. Frontier: post-quantum and beyond.**
  - Rainbow and SIKE broken; HQC.
  - The 2024 quantum-LWE claim and its retraction.
  - Open problems. Outro.

## Build

```bash
python -m videos.cs.cs30.compute           # every number in the part (about five minutes)
python tools/build.py cs30 -q l            # a 480p preview
python tools/build.py cs30                 # 1080p
```

## Problems, with solutions

1. **RSA is always correct.** Prove that RSA decryption is correct for every m in ℤ_n, including those sharing a
   factor with n, using the CRT.

   *Solution.* Write ed = 1 + k(p − 1)(q − 1), and work modulo p first.
   - If p ∤ m, Fermat gives m^{p−1} ≡ 1. So m^{ed} = m·(m^{p−1})^{k(q−1)} ≡ m.
   - If p | m, both sides are 0 mod p.

   Either way m^{ed} ≡ m (mod p), and the same holds mod q. Since p and q are distinct primes, the CRT says the two
   congruences determine m^{ed} mod n = pq, so m^{ed} ≡ m (mod n).

2. **Knowing too much factors n.** Show that knowing φ(n) for n = pq factors n. Show also that knowing e and d
   factors n with high probability.

   *Solution.* From φ(n) = n − (p + q) + 1 we get p + q = n − φ(n) + 1. Since pq = n, p and q are the roots of
   x² − (n − φ + 1)x + n.

   From e and d: ed − 1 is a multiple of λ(n). Write ed − 1 = 2ᵗr with r odd. Pick a random a and compute
   a^r, a^{2r}, …. The sequence reaches 1, and the value just before is a square root of 1. With probability at least
   ½ over a, this root is not ±1, as in Miller–Rabin. Then x² ≡ 1 with x ≢ ±1, so gcd(x − 1, n) is p or q.

   So publishing d is as bad as publishing the factors. A server that loses d must change n, not only d.

3. **Pohlig–Hellman's cost.** Show that Pohlig–Hellman takes O(∑ eᵢ(log n + √qᵢ)) group operations in a group of
   order n = ∏ qᵢ^{eᵢ}.

   *Solution.* For each prime power qᵉ:
   - Raise g and h to the power n/qᵉ, which takes O(log n) operations. This moves them into the subgroup of order qᵉ.
   - Find the log there one base-q digit at a time. Digit j needs one exponentiation to strip the digits already
     found, O(log n) operations, and one discrete log in the subgroup of order q, O(√qᵢ) by BSGS.

   That makes eᵢ digits, each O(log n + √qᵢ), plus O(log n) for the projection. Summing over i, and adding a
   negligible CRT, gives the bound. The cost is governed by the largest prime factor of the group order, which is why
   groups must have one of at least 2²⁵⁶.

4. **ECDSA's fragility.** Derive the nonce-reuse recovery. Then show that knowing k for a single signature
   reveals d.

   *Solution.* A signature satisfies s ≡ k⁻¹(z + rd) (mod n). With the same k (hence the same r) for messages with
   hashes z₁ and z₂:
   - s₁ − s₂ ≡ k⁻¹(z₁ − z₂), so k ≡ (z₁ − z₂)(s₁ − s₂)⁻¹ (when s₁ ≠ s₂).
   - Then d ≡ (s₁k − z₁)r⁻¹.

   The second line needs only k, so a single signature whose nonce leaks, by reuse, a weak generator or a side
   channel, gives d. Chapter 10 recovered both on P-256.

5. **Build: a hybrid handshake.** Extend the TLS-like handshake to a hybrid, X25519 plus this part's K-PKE, and check
   that both sides derive the same keys.

   *Solution.*
   1. The client adds a K-PKE public key to its ClientHello, next to its X25519 share.
   2. The server picks a random 32-byte secret m, encrypts its 256 bits under that public key, and returns the
      ciphertext with its X25519 share.
   3. Both sides compute IKM = X25519 secret ‖ m and feed it to HKDF-Extract in place of the X25519 secret alone. The
      client gets m by decrypting.
   4. Put both the public key and the ciphertext in the transcript, so the Finished MACs and the signature cover
      them.

   The derived keys match whenever decryption succeeds; chapter 14 measured no failures in 25,600 bits. The
   combination is secure if either component is: X25519 against classical attackers, K-PKE against quantum ones.

   One caveat: our K-PKE is only CPA-secure. ML-KEM wraps it in a Fujisaki–Okamoto transform. It re-encrypts the
   decrypted message and compares with the ciphertext, and on a mismatch it returns a pseudorandom "implicit
   rejection" key. That makes it safe against chosen ciphertexts, and it is what a real hybrid uses (X25519MLKEM768
   in TLS today).

6. ★ **Research: where small lattice attacks stop.** For LWE with q = 3329 and small secrets, find the dimension at
   which LLL and BKZ stop recovering s, and compare with the lattice estimator.

   *Where to start.*
   1. Generate instances with n from 10 to 60, m ≈ 2n samples, and ternary secrets and errors.
   2. Build the primal attack's embedding lattice (Kannan's embedding of b into the q-ary lattice of A). Its unique
      shortest vector is (e, s, 1) up to sign.
   3. Reduce it with LLL. Ours works in exact rationals and is slow, so use a floating-point LLL, or `fpylll`'s.
      Then repeat with BKZ at block sizes β = 10, 20 and 30.
   4. Record the success rate against n for each method.
   5. Compare with the predictions of the Lattice Estimator (Albrecht, Player and Scott 2015, and its current
      open-source version). The 2016 "core-SVP" model of Alkim, Ducas, Pöppelmann and Schwabe predicts the β needed
      from n, q and the noise.

   How well do the predictions match at these small sizes, where the asymptotic heuristics are least trustworthy?
   Does the success curve have the sharp threshold the "2016 estimate" assumes? Published experiments (Albrecht et
   al., "Revisiting the expected cost of solving uSVP", 2017) are the place to begin. Extrapolating them is how every
   post-quantum key size is set.

## 习题与解答

1. **RSA 总是正确的。** 用中国剩余定理证明：对 ℤ_n 中的每个 m，包括与 n 有公因子的，RSA 解密都正确。

   *解答。* 写 ed = 1 + k(p − 1)(q − 1)。先模 p：若 p ∤ m，由费马小定理 m^{p−1} ≡ 1，于是 m^{ed} = m·(m^{p−1})^{k(q−1)} ≡ m；
   若 p | m，两边模 p 都是 0。所以 m^{ed} ≡ m (mod p)，同理模 q 也成立。p、q 是不同的素数，由中国剩余定理，这两个同余式确定
   m^{ed} 模 n = pq 的值，所以 m^{ed} ≡ m (mod n)。

2. **知道太多就能分解 n。** 证明对 n = pq，知道 φ(n) 就能分解 n；并证明知道 e 和 d 就能以很高的概率分解 n。

   *解答。* 由 φ(n) = n − (p + q) + 1 得 p + q = n − φ(n) + 1；又 pq = n，所以 p、q 是 x² − (n − φ + 1)x + n 的两个根。由 e
   和 d：ed − 1 是 λ(n) 的倍数。写 ed − 1 = 2ᵗr，r 为奇数。随机取 a，计算 a^r, a^{2r}, …。序列会到达 1，它前面的那个值是 1
   的平方根；与 Miller–Rabin 一样，对至少一半的 a，这个根不是 ±1。于是 x² ≡ 1 且 x ≢ ±1，gcd(x − 1, n) 就是 p 或 q。所以公开 d
   和公开因子一样糟：丢了 d 的服务器必须更换 n，而不只是 d。

3. **Pohlig–Hellman 的代价。** 证明在阶为 n = ∏ qᵢ^{eᵢ} 的群中，Pohlig–Hellman 需要 O(∑ eᵢ(log n + √qᵢ)) 次群运算。

   *解答。* 对每个素数幂 qᵉ：把 g 和 h 升到 n/qᵉ 次幂，花 O(log n) 次运算，把它们投到阶为 qᵉ 的子群；然后按 q 进制一位一位地求
   那里的对数。第 j 位需要一次乘幂来剥掉已求出的各位，O(log n)，以及一次阶为 q 的子群中的离散对数，用小步大步法 O(√qᵢ)。一共 eᵢ
   位，每位 O(log n + √qᵢ)，外加投影的 O(log n)。对 i 求和，再加上可以忽略的 CRT，就得到这个界。代价由群阶的最大素因子决定，
   所以群阶必须有一个至少 2²⁵⁶ 的素因子。

4. **ECDSA 的脆弱。** 推导随机数复用时的恢复方法，并证明只要知道单个签名的 k 就能得出 d。

   *解答。* 签名满足 s ≡ k⁻¹(z + rd) (mod n)。对哈希为 z₁、z₂ 的两条消息使用同一个 k（因而 r 相同）：s₁ − s₂ ≡ k⁻¹(z₁ − z₂)，
   所以 k ≡ (z₁ − z₂)(s₁ − s₂)⁻¹（当 s₁ ≠ s₂ 时），然后 d ≡ (s₁k − z₁)r⁻¹。第二步只需要 k，所以只要有一个签名的随机数泄露，无论是
   因为复用、糟糕的生成器还是侧信道，都会交出 d。第 10 章在 P-256 上恢复出了两者。

5. **动手：混合握手。** 把 TLS 式握手扩展为混合方案，X25519 加本部分的 K-PKE，并检查双方得出相同的密钥。

   *解答。* 客户端在 ClientHello 中，在 X25519 份额旁边再加一个 K-PKE 公钥。服务器随机选一个 32 字节的秘密 m，用该公钥加密它的
   256 位，连同自己的 X25519 份额一起返回密文。双方计算 IKM = X25519 秘密 ‖ m（客户端解密得到 m），用它代替单独的 X25519 秘密送入
   HKDF-Extract。把公钥和密文都放进记录，让 Finished MAC 和签名覆盖它们。只要解密成功，派生出的密钥就一致；第 14 章在 25,600 位中
   测得没有失败。只要其中一个组成部分安全，组合就安全：X25519 对付经典攻击者，K-PKE 对付量子攻击者。一个提醒：我们的 K-PKE 只是
   CPA 安全的。ML-KEM 用 Fujisaki–Okamoto 变换包装它：重新加密解出的消息并与密文比较，不一致时返回一个伪随机的「隐式拒绝」密钥。
   这使它能抵御选择密文攻击，真正的混合方案（如今 TLS 中的 X25519MLKEM768）用的就是它。

6. ★ **研究：小规模格攻击在哪里失效。** 对 q = 3329、秘密很小的 LWE，找出 LLL 与 BKZ 不再能恢复 s 的维数，并与格估计器比较。

   *从哪里入手。* 生成 n 从 10 到 60、约 m ≈ 2n 个样本、秘密与误差取三值的实例。构造原始攻击的嵌入格（把 b 用 Kannan 嵌入法放进
   A 的 q 元格），它唯一的最短向量在正负号意义下是 (e, s, 1)。用 LLL 约化它（我们的 LLL 用精确有理数，很慢；改用浮点 LLL 或
   `fpylll` 的），再用块大小 β = 10、20、30 的 BKZ 重复，记录各方法的成功率随 n 的变化。再与格估计器（Albrecht、Player 与 Scott
   2015，以及它现在的开源版本）的预测比较：Alkim、Ducas、Pöppelmann 与 Schwabe 2016 年的「core-SVP」模型由 n、q 和噪声预测所需的
   β。在这些小规模下，渐近启发式最不可信，预测吻合得如何？成功率曲线是否有「2016 估计」所假设的那种陡峭阈值？已发表的实验
   （Albrecht 等，《Revisiting the expected cost of solving uSVP》，2017）是起点；把它们外推，正是每个后量子密钥长度的确定方式。

## Glossary additions

公钥 public key · 私钥 private key · 密钥分配 key distribution · Merkle 谜题 Merkle's puzzles · 模运算 modular arithmetic ·
扩展欧几里得算法 extended Euclidean algorithm · Bézout 等式 · 平方乘 square-and-multiply · 群 group · 生成元 generator · 阶
order · 拉格朗日定理 Lagrange's theorem · 费马小定理 Fermat's little theorem · 欧拉定理 Euler's theorem · 中国剩余定理 Chinese
remainder theorem · 离散对数 discrete logarithm · Diffie–Hellman 密钥交换 · 中间人 man in the middle · RSA · 填充 padding ·
OAEP · 因数分解 factoring · 光滑数 smooth number · 二次筛法 quadratic sieve · 数域筛法 number field sieve · 小步大步法
baby-step giant-step · 安全素数 safe prime · 指数演算 index calculus · 椭圆曲线 elliptic curve · 无穷远点 point at infinity ·
标量乘法 scalar multiplication · ECDSA · 随机数复用 nonce reuse · 证书 certificate · 证书颁发机构 certificate authority ·
证书链 certificate chain · 证书透明 Certificate Transparency · 握手 handshake · 密钥派生 key derivation · 前向保密 forward
secrecy · 周期寻找 period finding · 先收集后解密 harvest now, decrypt later · 格 lattice · 格基约化 lattice reduction ·
带误差学习 learning with errors · 数论变换 number-theoretic transform · 混合密钥交换 hybrid key exchange · 一次性签名 one-time
signature · 零知识 zero knowledge · 秘密共享 secret sharing · 多方计算 multiparty computation · 全同态加密 fully homomorphic
encryption

## Sources

*Canon.* Books:
- Katz & Lindell, *Introduction to Modern Cryptography* (3rd ed., 2020);
- Boneh & Shoup, *A Graduate Course in Applied Cryptography* (v0.6, 2023);
- Silverman, *The Arithmetic of Elliptic Curves* (2nd ed., 2009); Washington, *Elliptic Curves: Number Theory and
  Cryptography* (2nd ed., 2008);
- Crandall & Pomerance, *Prime Numbers: A Computational Perspective* (2nd ed., 2005);
- Galbraith, *Mathematics of Public Key Cryptography* (2012); Peikert, *A Decade of Lattice Cryptography* (2016).

Papers and standards:
- Key exchange and RSA: Merkle (1978); Diffie & Hellman (1976); Rivest, Shamir & Adleman (1978); Ellis (1970, 1987);
  Cocks (1973); Barak & Mahmoody-Ghidary (2009).
- Padding and attacks: Bellare & Rogaway (1994); Bleichenbacher (1998); Böck, Somorovsky & Young, "ROBOT" (2018).
- Factoring and logs:
  - Pollard (1974, 1975, 1978); Brent (1980); Pomerance (1982); Lenstra & Lenstra (eds.), *The Development of the
    Number Field Sieve* (1993);
  - Boudot et al., RSA-240 and RSA-250 (2020); Shanks (1971); Pohlig & Hellman (1978);
  - Adrian et al., "Imperfect Forward Secrecy" (Logjam, 2015).
- Curves and signatures: Miller (1985); Koblitz (1987); Bernstein, "Curve25519" (2006); RFC 7748; FIPS 186-5;
  RFC 6979; fail0verflow, "Console Hacking 2010" (27C3); Schnorr (1991); Fiat & Shamir (1986); Lamport (1979).
- PKI and TLS:
  - RFC 5280; RFC 6962 (Laurie, Langley & Kasper, Certificate Transparency);
  - Fox-IT's DigiNotar report (2012); Aas et al., "Let's Encrypt" (2019);
  - RFC 8446; Krawczyk, "Cryptographic Extraction and Key Derivation" (2010), RFC 5869.
- Quantum and lattices:
  - Shor (1994); Gidney (2025); Lenstra, Lenstra & Lovász (1982); Shamir (1982);
  - Lagarias & Odlyzko (1985); Regev (2005);
  - FIPS 203, 204, 205 (2024); Alkim, Ducas, Pöppelmann & Schwabe (2016); Albrecht, Player & Scott (2015);
  - Beullens (2022); Castryck & Decru (2023).
- Beyond: Shamir (1979); Yao (1986); Goldreich, Micali & Wigderson (1987); Bogetoft et al., "Secure multiparty
  computation goes live" (2009); Gentry (2009); Impagliazzo & Rudich (1989).
