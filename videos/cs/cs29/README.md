# Computer Science, Built — Part 29: Secrets

Part 29 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth part of Act V, *Limits and Secrets*. For two thousand years ciphers were
broken by counting letters. Shannon proved in 1949 that perfect secrecy needs a key as long as the message. Modern
cryptography gets around his theorem by limiting the attacker's computing power, and builds pseudorandomness, block
ciphers and hash functions on that assumption. The attacks in this part show how much care it takes. Every cipher and
attack here is built from scratch and run; **the code is for learning, never for real use**, as the video says on
screen.

The instrument is `explainer/cs/algo/crypto.py`. It holds:
* classical ciphers and their breaks:
  - Caesar, substitution and Vigenère;
  - a quadgram language model with hill climbing from al-Kindi's frequency-matched start;
  - the index of coincidence, and χ² shift recovery;
* an Enigma I simulator (rotors I–V, reflector B, plugboard, double stepping), cycle decomposition and Rejewski's
  characteristic;
* the one-time pad and crib dragging; LFSRs, and Berlekamp–Massey over GF(2);
* ChaCha20 (RFC 8439);
* AES-128 from scratch:
  - the S-box built from inversion in GF(2⁸) mod x⁸ + x⁴ + x³ + x + 1 and the affine map;
  - the key schedule, encryption with a per-step trace, and decryption;
* ECB, CBC and CTR modes; PKCS#7 padding and Vaudenay's padding-oracle attack;
* SHA-256 (Merkle–Damgård) and the length-extension attack; HMAC; CBC-MAC; GHASH and AES-GCM; Keccak-f[1600] and
  SHA3-256;
* birthday collision search; Merkle trees and inclusion proofs;
* Heys' 16-bit SPN, its difference table and a differential attack on the last round; a 16-bit toy cipher and the
  meet-in-the-middle attack on its double encryption;
* early-exit and constant-time comparison; a PID-seeded key generator.

It is tested in `tests/test_cs29_crypto.py`, against published vectors where they exist:
* AES-128 against FIPS-197 Appendices B and C.1, and S(0x53) = 0xED;
* ChaCha20 against the RFC 8439 quarter-round and block vectors;
* AES-GCM against the NIST test cases 1 and 2;
* SHA-256, SHA3-256 and HMAC-SHA256 against `hashlib` and `hmac`;
* the Enigma test vector (AAAAA → BDZGO with rotors I, II, III at AAA); its involution property; and the invariance of
  the characteristic under the plugboard.

The attacks are also tested: length extension, the padding oracle, Berlekamp–Massey, the SPN differential attack,
Vigenère round trips, Merkle proofs and both comparisons.

* **Two thousand years of secrets.** Hook.
  - Our 128 × 96 logo under AES: in ECB, 85 distinct blocks out of 768 and the logo is visible; in CBC, 768 distinct
    blocks.
  - A timeline from Caesar to AES; Shannon's theorem; the bounded attacker.
* **1. Substitution and frequency analysis.**
  - 26! ≈ 4 × 10²⁶ keys, 13 billion years at a billion keys a second.
  - Letter counts of 600 letters of *Moby-Dick* under a random key against English: W (12.8%) is E (12.7%).
  - Hill climbing on quadgram scores, from six million letters of other novels: one restart stuck at −3647, five reach
    −2488. The whole text is recovered, 100% correct, in 5.5 s.
* **2. Vigenère and the index of coincidence.**
  - The keyword BABBAGE; five plaintext E's enciphered as K, E, F, E, K.
  - The index of coincidence: plaintext 0.062, ciphertext 0.045, random 0.038; by key length, peaks at 7 (0.065) and
    14.
  - Column-by-column χ² recovers BABBAGE; all 600 letters decrypt.
* **3. Enigma.**
  - Rotors as permutations; the reflector; no letter enciphers to itself; 150,738,274,937,250 plugboard settings and
    1.59 × 10²⁰ daily keys.
  - Rejewski's theorem: two 13-cycles with and without ten plugboard cables. The characteristic
    (13,13; 12,12,1,1; 13,13) is unchanged, because conjugation preserves cycle type; another setting gives
    (8,8,3,3,2,2; …).
  - Cribs: WETTERBERICHT rules out 9 of 15 positions; the Bombe; Colossus.
* **4. Perfect secrecy.**
  - Vernam's pad; Shannon's definition and the proof for the pad; the 2-bit Latin square.
  - |K| ≥ |M|, proved.
  - A two-time pad broken by dragging " THE ": hits at offsets 4, 17 and 22. VENONA.
* **5. What secure means.**
  - Kerckhoffs; polynomial-time attackers; negligible advantage.
  - Work on a log scale: 2⁵⁶ (Deep Crack), 2⁶⁴, 2⁹⁴ (a year of Bitcoin mining), 2¹²⁸.
  - IND-CPA as a game; why encryption must be randomised; proof by reduction.
* **6. Pseudorandom generators.**
  - The definition and the stream cipher's reduction; Yao's next-bit test; PRGs from any one-way function.
  - A 17-bit LFSR (period 131,071) predicted completely from 34 bits by Berlekamp–Massey.
  - ChaCha20: the state, the quarter-round, column and diagonal rounds; RFC 8439 vectors; 677 KB/s in Python.
* **7. Pseudorandom functions and permutations.**
  - The GGM tree with SHA-256 as the generator: F(101) = 415c14be….
  - Feistel networks: the 2-round distinguisher fires in 100% of 2,000 trials for 1 and 2 rounds, 0% for 3.
    Luby–Rackoff.
  - The PRP/PRF switching lemma and Sweet32.
* **8. AES.**
  - DES against AES, and the contest.
  - One round on FIPS-197's example: SubBytes (S(0x53): inverse 0xCA, output 0xED), ShiftRows, MixColumns,
    AddRoundKey.
  - Ten rounds give 69c4e0d86a7b0430d8cdb78070b4c55a, as in the standard.
* **9. The avalanche.**
  - One flipped bit after rounds 0–4: 1, 17, 62, 64 and 71 bits differ (1, 4 and then all 16 bytes).
  - 400 trials: means of 1, 16.1 and 64.4 bits after rounds 0–2. After ten rounds, mean 63.6 and s.d. 5.45, against
    Binomial(128, ½).
  - Why ten rounds: seven-round attacks; the biclique attack at 2¹²⁶·¹.
* **10. Modes of operation.**
  - The logo under ECB, CBC and CTR.
  - The padding oracle explained, then run: "PIN=4921; transfer approved by the bank" recovered with 6,412 queries
    (134 a byte) in 2 s.
* **11. Integrity.**
  - CTR malleability: $0010 becomes $9910 without the key.
  - CBC-MAC's splice forgery, verified; HMAC.
  - Encrypt-then-MAC; GCM's GHASH as polynomial evaluation (NIST vectors match); nonce reuse; ChaCha20-Poly1305.
* **12. Hash functions.**
  - Birthday collisions on SHA-256 cut to 16–32 bits, against √(π/2) · 2ⁿᐟ².
  - MD5 and SHA-1 broken.
  - Merkle–Damgård and a length-extension forgery that verifies.
  - The SHA-3 sponge; ours matches `hashlib`.
* **13. Hashes at work.**
  - A Merkle tree over eight commits; a 3-hash inclusion proof; tampering detected.
  - Coin flipping by telephone with a commitment.
  - Password hashing measured: SHA-256 (0.45 µs), PBKDF2 × 100,000 and × 600,000, and scrypt (48 ms, 16 MB), with
    the time to try every 8-letter lowercase password.
* **14. Cryptanalysis.**
  - Heys' SPN and its difference table; a three-round trail of probability 27/1024.
  - The last-round attack on 5,000 pairs: the right key gets 146 counts and the best wrong guess 80. DES's S-boxes;
    linear cryptanalysis; AES's wide-trail bound.
  - Meet in the middle on double encryption: 131,072 cipher calls instead of 2³²; two candidates survive two pairs.
* **15. Side channels and bad randomness.**
  - Early-exit comparison: 208 to 524 ns over 0–16 correct bytes; constant time is flat at about 720 ns.
  - Cache attacks on AES T-tables; power analysis.
  - The Debian OpenSSL bug in miniature: a PID-seeded key found after 23,107 tries in 2 s. Dual_EC_DRBG.
* **16. Frontier: proofs, quanta and lightweight ciphers.**
  - Minicrypt; Liu–Pass.
  - Grover and Simon's attacks on modes.
  - Key-alternating ciphers (Even–Mansour; Chen–Steinberger); Ascon.
  - Open problems. Outro.

## Build

```bash
python -m videos.cs.cs29.compute           # every number in the part (about two minutes)
python tools/build.py cs29 -q l            # a 480p preview
python tools/build.py cs29                 # 1080p
```

## Problems, with solutions

1. **Shannon's theorem.** Prove that perfect secrecy implies |K| ≥ |M|, and that the one-time pad with a uniform key
   is perfectly secret.

   *Solution.* Let the message distribution give every message positive probability, and fix a ciphertext c with
   Pr[C = c] > 0. Decrypting c under every key gives the set D(c) = {Dec_k(c) : k ∈ K}, of size at most |K|. If
   |K| < |M|, some message m′ is not in D(c). Then no key turns m′ into c, so Pr[M = m′ | C = c] = 0, while
   Pr[M = m′] > 0. That contradicts perfect secrecy.

   For the pad on n bits, fix any m and c. Then Pr[C = c | M = m] = Pr[K = m ⊕ c] = 2⁻ⁿ, the same for every m. So
   Pr[C = c] = Σ_m Pr[C = c | M = m] Pr[M = m] = 2⁻ⁿ. Bayes' rule then gives Pr[M = m | C = c] = 2⁻ⁿ Pr[M = m] / 2⁻ⁿ
   = Pr[M = m].

2. **A stream cipher from a PRG.** Show that if G is a PRG, then c = m ⊕ G(k) is secure for one message, by a
   reduction. Then break it for two messages under one key.

   *Solution.* Suppose an adversary A, given m₀, m₁ of its choice and c = m_b ⊕ G(k), guesses b with probability
   ½ + ε. Build a distinguisher D for G. On input y, D runs A to get m₀, m₁, picks a random bit b, and gives A the
   value m_b ⊕ y. It outputs 1 if A guesses b.
   - If y = G(k), this is exactly A's game, so Pr[D = 1] = ½ + ε.
   - If y is uniform, m_b ⊕ y is uniform and independent of b, so Pr[D = 1] = ½.

   D's advantage is ε, so if G is a PRG, ε is negligible.

   With two messages under one key, c₁ ⊕ c₂ = m₁ ⊕ m₂. In the two-message game, the adversary submits
   (m, m) against (m, m′) with m ≠ m′. It outputs 0 exactly when c₁ = c₂. It is always right, so its advantage is ½.
   Chapter 4's crib dragging is the practical version.

3. **Feistel distinguishers.** Give a distinguisher with advantage near 1 for the 2-round Feistel network, and one
   for 3 rounds when decryption queries are allowed.

   *Solution.* Write a round as (L, R) ↦ (R, L ⊕ f(R)), with halves of h bits.

   Two rounds: (L, R) ↦ (L ⊕ f₁(R), R ⊕ f₂(L ⊕ f₁(R))). Query (L₁, R) and (L₂, R) with L₁ ≠ L₂, and output 1 if the
   left output halves XOR to L₁ ⊕ L₂. A 2-round network does this always. A random permutation does it with
   probability about 2⁻ʰ. The advantage is 1 − 2⁻ʰ, and chapter 7 measured 100% against 0%.

   Three rounds, with decryptions:
   1. Encrypt (L₁, R) to get (S₁, T₁).
   2. Encrypt (L₂, R) to get (S₂, T₂).
   3. Decrypt (S₂, T₂ ⊕ L₁ ⊕ L₂) to get (L₃, R₃).
   4. Output 1 if R₃ = S₁ ⊕ S₂ ⊕ R.

   Following the rounds:
   - The decryption's middle value becomes X₁ = L₁ ⊕ f₁(R).
   - Since S_i = R ⊕ f₂(X_i), we have R₃ = S₂ ⊕ f₂(X₁) = S₂ ⊕ S₁ ⊕ R, always.

   A random permutation satisfies it with probability about 2⁻ʰ. That is why Luby and Rackoff need four rounds for a
   *strong* PRP.

4. **CBC-MAC and lengths.** Show that CBC-MAC is insecure for messages of different lengths, and that prefixing the
   length defeats the splice.

   *Solution.* Let one-block messages m₁ and m₂ have tags t₁ = E_k(m₁) and t₂ = E_k(m₂). For the two-block message
   m₁ ‖ (m₂ ⊕ t₁), the chain computes E_k(E_k(m₁) ⊕ m₂ ⊕ t₁) = E_k(m₂) = t₂. That is a valid tag for a message never
   queried.

   Now prefix a block holding the length. The tag of a one-block message is then E_k(E_k(1) ⊕ m₁). The forger needs
   the chain's state after "2 blocks, m₁", which is E_k(E_k(2) ⊕ m₁). That value is unrelated to any tag it has seen.

   More generally, with a length prefix no message's encoding is a proper prefix of another's. On such prefix-free
   sets, CBC-MAC is a secure PRF when E is a PRP (Bellare, Kilian and Rogaway; Petrank and Rackoff). CMAC achieves
   the same result by masking the last block with a derived subkey.

5. **Build: attack your own server, then fix it.** Write a padding-oracle server with this part's AES-CBC, recover a
   message and count queries. Then fix it with encrypt-then-MAC.

   *Solution.* The server is a function `oracle(iv, c)` that runs `pkcs7_unpad(cbc_decrypt(aes, iv, c))` and returns
   whether it raised. `crypto.padding_oracle_attack(iv, c, oracle)` recovers each block from right to left, with at
   most 256 queries a byte and about 128 on average. Chapter 10 measured 134.

   The fix:
   - Compute `t = hmac_sha256(k_mac, iv + c)` at encryption.
   - At decryption, check t with `constant_time_equal` *before* decrypting.
   - Return one error for every failure.

   The oracle now answers "invalid" for every doctored ciphertext, because the attacker cannot produce a valid tag,
   and the attack learns nothing. Use separate keys for encryption and the MAC. Better still, use an AEAD mode.

6. ★ **Research: how much do trails cluster?** For Heys' SPN with 3 to 6 rounds, compute the exact expected
   probability of the best differential over all trails. Compare it with the best single trail.

   *Where to start.* With independent uniform round keys the cipher is a Markov cipher (Lai, Massey and Murphy,
   1991). The expected probability that input difference α becomes β after r rounds is then an entry of Mʳ, where M
   is the 2¹⁶ × 2¹⁶ difference-transition matrix of one round: the S-box layer, then the permutation.

   M is sparse. Each row's support is the product of the S-boxes' nonzero table entries for the active nibbles. So
   for a fixed α, propagate a vector of 2¹⁶ probabilities r times. Maximise over α by symmetry and pruning, since
   only low-weight α are plausible.

   Compare max_β EDP(α, β) with the best single trail, found by a branch-and-bound search over trails (Matsui's
   algorithm). Then ask how fast the ratio grows with r. Background:
   - Keliher and Sui (2007) computed such exact values for two rounds of AES.
   - Daemen and Rijmen (2007) discussed "plateau trails".
   - Ankele and Kölbl (2018), "Mind the gap", measured clustering in modern lightweight ciphers.

   Nobody can compute these sums for full-size ciphers, which is why designers bound single trails instead.

## 习题与解答

1. **Shannon 定理。** 证明完美保密蕴含 |K| ≥ |M|，并证明密钥均匀的一次一密是完美保密的。

   *解答。* 设消息分布给每个消息正概率，固定一个 Pr[C = c] > 0 的密文 c。在每个密钥下解密 c，得到集合 D(c) = {Dec_k(c) : k ∈ K}，
   其大小至多 |K|。若 |K| < |M|，就有某个消息 m′ 不在 D(c) 中：没有密钥把 m′ 变成 c，所以 Pr[M = m′ | C = c] = 0，而 Pr[M = m′] > 0，
   与完美保密矛盾。对 n 位的一次一密，任取 m 与 c，Pr[C = c | M = m] = Pr[K = m ⊕ c] = 2⁻ⁿ，对每个 m 都一样；所以 Pr[C = c] =
   Σ_m Pr[C = c | M = m] Pr[M = m] = 2⁻ⁿ，再由 Bayes 公式，Pr[M = m | C = c] = 2⁻ⁿ Pr[M = m] / 2⁻ⁿ = Pr[M = m]。

2. **由 PRG 构造流密码。** 证明若 G 是 PRG，则 c = m ⊕ G(k) 对一条消息是安全的（用归约）；再对同一密钥下的两条消息攻破它。

   *解答。* 设敌手 A 拿到自己选的 m₀、m₁ 与 c = m_b ⊕ G(k)，以 ½ + ε 的概率猜中 b。构造 G 的区分器 D：输入 y 时，D 运行 A 得到 m₀、m₁，
   随机取一位 b，把 m_b ⊕ y 交给 A，A 猜中 b 就输出 1。若 y = G(k)，这正是 A 的游戏，Pr[D = 1] = ½ + ε；若 y 均匀，m_b ⊕ y 均匀且与 b
   独立，Pr[D = 1] = ½。所以 D 的优势是 ε；G 是 PRG，ε 就可忽略。同一密钥下两条消息：c₁ ⊕ c₂ = m₁ ⊕ m₂。在两消息游戏中，敌手提交
   (m, m) 对 (m, m′)（m ≠ m′），当且仅当 c₁ = c₂ 时输出 0：它总是对的，优势为 ½。第 4 章的拖曳猜词就是它的实战版。

3. **Feistel 区分器。** 对 2 轮 Feistel 网络给出优势接近 1 的区分器；对 3 轮、允许解密查询的情形也给出一个。

   *解答。* 把一轮写成 (L, R) ↦ (R, L ⊕ f(R))，每半 h 位。两轮：(L, R) ↦ (L ⊕ f₁(R), R ⊕ f₂(L ⊕ f₁(R)))。查询 (L₁, R) 与 (L₂, R)
   （L₁ ≠ L₂），若两个输出的左半异或等于 L₁ ⊕ L₂ 就输出 1：2 轮网络总是如此，随机置换的概率约为 2⁻ʰ；优势 1 − 2⁻ʰ（第 7 章测得 100% 对
   0%）。三轮且允许解密：加密 (L₁, R) 得 (S₁, T₁)，加密 (L₂, R) 得 (S₂, T₂)，解密 (S₂, T₂ ⊕ L₁ ⊕ L₂) 得 (L₃, R₃)，若 R₃ = S₁ ⊕ S₂ ⊕ R
   就输出 1。逐轮推演：解密时的中间值变为 X₁ = L₁ ⊕ f₁(R)；又因 S_i = R ⊕ f₂(X_i)，得 R₃ = S₂ ⊕ f₂(X₁) = S₂ ⊕ S₁ ⊕ R，恒成立。随机置换
   满足它的概率约 2⁻ʰ。这就是 Luby 与 Rackoff 要四轮才能得到*强* PRP 的原因。

4. **CBC-MAC 与长度。** 证明 CBC-MAC 对不同长度的消息不安全，并证明前置长度能挫败拼接。

   *解答。* 设单块消息 m₁、m₂ 的标签为 t₁ = E_k(m₁)、t₂ = E_k(m₂)。对两块消息 m₁ ‖ (m₂ ⊕ t₁)，链计算 E_k(E_k(m₁) ⊕ m₂ ⊕ t₁) =
   E_k(m₂) = t₂：一个从未查询过的消息的有效标签。现在前置一个存放长度的块：单块消息的标签是 E_k(E_k(1) ⊕ m₁)，而伪造者需要的是
   「2 块，m₁」之后链的状态 E_k(E_k(2) ⊕ m₁)，它与见过的任何标签都无关。一般地，有了长度前缀，没有一个消息的编码是另一个的真前缀；在
   这种无前缀集合上，只要 E 是 PRP，CBC-MAC 就是安全的 PRF（Bellare、Kilian 与 Rogaway；Petrank 与 Rackoff）。CMAC 用派生子密钥掩盖
   最后一块，达到同样的效果。

5. **动手：攻击自己的服务器，再修好它。** 用本部分的 AES-CBC 写一个填充预言机服务器，恢复一条消息并数查询次数；然后用先加密后 MAC
   修好它。

   *解答。* 服务器就是一个函数 `oracle(iv, c)`：运行 `pkcs7_unpad(cbc_decrypt(aes, iv, c))`，返回是否抛出异常。
   `crypto.padding_oracle_attack(iv, c, oracle)` 从右到左恢复每一块，每字节至多 256 次、平均约 128 次查询（第 10 章测得 134）。修复：加密时
   计算 `t = hmac_sha256(k_mac, iv + c)`；解密时*先*用 `constant_time_equal` 检查 t，再解密；任何失败都返回同一个错误。现在预言机对每个
   篡改过的密文都答「无效」，因为攻击者造不出有效标签，攻击什么也学不到。加密与 MAC 用不同的密钥；更好的是直接用 AEAD 模式。

6. ★ **研究：差分路径聚集有多严重？** 对 3 到 6 轮的 Heys SPN，计算最佳差分在所有路径上求和的精确期望概率，并与最佳单条路径比较。

   *从哪里入手。* 轮密钥独立均匀时，这个密码是 Markov 密码（Lai、Massey 与 Murphy，1991），r 轮后输入差分 α 变成 β 的期望概率是 Mʳ 的
   一个元素，其中 M 是一轮（S 盒层再接置换）的 2¹⁶ × 2¹⁶ 差分转移矩阵。M 是稀疏的：每行的支撑是活跃半字节上各 S 盒非零表项之积。所以对
   固定的 α，把一个 2¹⁶ 维的概率向量传播 r 次；再利用对称性与剪枝对 α 取最大（只有低重量的 α 有希望）。把 max_β EDP(α, β) 与用分支定界
   （Matsui 算法）找到的最佳单条路径比较，问这个比值随 r 增长多快。Keliher 与 Sui（2007）对两轮 AES 算出了这样的精确值；Daemen 与 Rijmen
   （2007）讨论了「平台路径」；Ankele 与 Kölbl（2018，《Mind the gap》）测量了现代轻量级密码中的聚集。对全尺寸密码，没有人能算出这些和，
   所以设计者只能为单条路径定界。

## Glossary additions

密码学 cryptography · 密钥 key · 明文 plaintext · 密文 ciphertext · 替换密码 substitution cipher · 频率分析 frequency analysis ·
爬山法 hill climbing · 维吉尼亚密码 Vigenère cipher · 重合指数 index of coincidence · 转子 rotor · 反射器 reflector · 接线板
plugboard · 共轭 conjugation · 循环结构 cycle structure · 已知明文片段 crib · 一次一密 one-time pad · 完美保密 perfect secrecy ·
Kerckhoffs 原则 · 可忽略 negligible · 选择明文攻击下的不可区分性 IND-CPA · 语义安全 semantic security · 归约 reduction ·
伪随机生成器 pseudorandom generator (PRG) · 单向函数 one-way function · 流密码 stream cipher · 随机数 nonce · 伪随机函数
pseudorandom function (PRF) · 混合论证 hybrid argument · 伪随机置换 pseudorandom permutation (PRP) · Feistel 网络 · 分组密码
block cipher · 代换–置换网络 SPN · S 盒 S-box · 雪崩效应 avalanche effect · 工作模式 mode of operation · 填充预言机 padding
oracle · 可延展性 malleability · 消息认证码 MAC · 认证加密 authenticated encryption (AEAD) · 哈希函数 hash function · 抗碰撞性
collision resistance · 生日界 birthday bound · 长度扩展 length extension · 海绵结构 sponge · Merkle 树 Merkle tree · 承诺 commitment ·
盐 salt · 内存困难 memory-hard · 差分密码分析 differential cryptanalysis · 线性密码分析 linear cryptanalysis · 中间相遇 meet in the
middle · 侧信道 side channel · 常数时间 constant time · 迷你密码国 Minicrypt · 密钥交替密码 key-alternating cipher · 轻量级密码
lightweight cryptography

## Sources

*Canon.* Books:
- Katz & Lindell, *Introduction to Modern Cryptography* (3rd ed., 2020);
- Boneh & Shoup, *A Graduate Course in Applied Cryptography* (v0.6, 2023);
- Goldreich, *Foundations of Cryptography* I–II (2001, 2004);
- Menezes, van Oorschot & Vanstone, *Handbook of Applied Cryptography* (1996);
- Daemen & Rijmen, *The Design of Rijndael* (2nd ed., 2020);
- Ferguson, Schneier & Kohno, *Cryptography Engineering* (2010);
- Kahn, *The Codebreakers* (1967, rev. 1996); Singh, *The Code Book* (1999).

Papers and standards:
- Classical: al-Kindi, *Risāla fī istikhrāj al-muʿammā* (9th c.); Kasiski (1863); Friedman, *The Index of
  Coincidence* (1922); Rejewski, "How Polish mathematicians deciphered the Enigma" (1981).
- Foundations: Shannon (1949); Kerckhoffs (1883); Goldwasser & Micali (1984); Yao (1982); Blum & Micali (1984);
  Goldreich & Levin (1989); Håstad, Impagliazzo, Levin & Luby (1999); Goldreich, Goldwasser & Micali (1986);
  Luby & Rackoff (1988); Impagliazzo (1995); Liu & Pass (2020).
- Ciphers and modes: FIPS 46 (DES); FIPS 197 (AES); Bernstein, "ChaCha" (2008), RFC 8439; Ehrsam, Meyer, Smith &
  Tuchman (CBC, 1976); Vaudenay (2002); Bhargavan & Leurent, "Sweet32" (2016); Bogdanov, Khovratovich & Rechberger
  (2011).
- Integrity and hashes: Bellare, Kilian & Rogaway (1994); Bellare, Canetti & Krawczyk (1996); Bellare & Namprempre
  (2000); McGrew & Viega, GCM (2004), SP 800-38D; Joux (2006); Böck et al., "Nonce-disrespecting adversaries" (2016);
  Merkle (1979, 1989); Damgård (1989); Wang & Yu (2005); Stevens et al., "SHAttered" (2017); Leurent & Peyrin (2020);
  Bertoni, Daemen, Peeters & Van Assche, Keccak (2011), FIPS 202; Percival, scrypt (2009); Biryukov, Dinu &
  Khovratovich, Argon2 (2016).
- Attacks: Biham & Shamir (1991); Matsui (1993); Coppersmith (1994); Heys, "A tutorial on linear and differential
  cryptanalysis" (2002); Diffie & Hellman (1977); Kocher (1996); Kocher, Jaffe & Jun (1999); Bernstein (2005); Osvik,
  Shamir & Tromer (2006); Debian Security Advisory DSA-1571 (2008); Shumow & Ferguson (2007).
- Frontier: Grover (1996); Simon (1994); Kuwakado & Morii (2010, 2012); Kaplan, Leurent, Leverrier & Naya-Plasencia
  (2016); Even & Mansour (1991); Chen & Steinberger (2014); Dobraunig, Eichlseder, Mendel & Schläffer, Ascon (2021);
  Jain, Lin & Sahai (2021); Lai, Massey & Murphy (1991); Keliher & Sui (2007); Ankele & Kölbl (2018).
