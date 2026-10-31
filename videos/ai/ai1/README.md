# AI, Built — Part 1: The Guessing Game

Part 1 of a thirty-one-part series on how modern AI works and how it came to be (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)). It starts where Claude Shannon did, with a game: guess the next letter of an
English text. From that game it builds information theory as a working tool: probability and the chain rule,
surprise and entropy (and why entropy is the only consistent measure of uncertainty), codes and the limits of
compression, cross-entropy and the KL divergence, arithmetic coding, learning by counting and by gradient descent,
mutual information, and the series' scoreboard, where large language models turn out to be the best compressors of
text we have. A hook, fifteen chapters and an outro:

* **Shannon's guessing game.** Shannon's 1951 experiment, played on his own sentence by a counting program; how we
  got here (Morse code, Hartley 1928, Shannon 1948 and 1951, Huffman, arithmetic coding, Bengio 2003, GPT-2, Qwen3);
  GPT-2 (2019) and Qwen3-4B (2025) playing the same game on the next token; tokens; the series map; the objectives; the scoreboard and its passage.
* **1. Probability and the chain rule.** Letter frequencies of 22.8 million symbols from thirty novels; a distribution
  as one unit of belief shared out; the 27 × 27 table of P(next | previous) and the mosaic of joint probabilities,
  P(u | q) = 0.9985; the chain rule, derived, and drawn as nested slivers (“he said” → *the*).
* **2. How surprised to be.** Shannon's requirements for surprise and the derivation that they leave only
  log₂(1/p) (g(x + y) = g(x) + g(y), integers, fractions, continuity); the surprise of Shannon's
  sentence, letter by letter: 182 bits for 101 symbols.
* **3. Entropy, and why it is unique.** The average surprise, term by term; entropy as an area (slivers of width
  p and height log₂ 1/p): 4.08 bits for letters; the coin; Shannon's three requirements (1948) and the grouping rule, checked on his
  example and on the letters (space / vowel / consonant: 1.48 + 0.307 × 2.20 + 0.502 × 3.85 = 4.08); his Theorem 2,
  sketched (A(sᵐ) = m A(s), A(n) = K log n, blocks of equal outcomes); H ≤ log₂ K by Jensen on the entropy dome
  (log₂ 27 = 4.75; the gap is redundancy);
  conditional entropy as a mosaic: 3.33 bits given the previous letter.
* **4. Prefix codes and the Kraft–McMillan inequality.** Fixed-length codes; prefix-free codes as trees, decoding;
  Kraft's inequality proved on the full binary tree (codewords claim 16 + 8 + 4 + 2 + 1 + 1 of 32 leaves); the converse
  (the canonical code: Shannon's lengths for the letters sum to 0.70); McMillan (1956): a decodable code that is not
  prefix-free ({0, 01, 011, 0111}, sum 15/16), one that cannot be decoded ({0, 1, 01}, sum 5/4), the k-th power
  argument, and (5/4)ᵏ overtaking 2k at k = 16.
* **5. The best code: Huffman, and why it is optimal.** L ≥ H by Jensen and Kraft; Shannon's rounded code (4.62
  bits); Huffman's 1951 term paper and his algorithm, merge by merge on the 27 letters (4.127 bits, *the falcon* in 43
  bits instead of 50); optimality by exchange arguments (swapping e's and z's codewords costs 0.596 bits per letter;
  the deepest leaves come in pairs; z and q are siblings) and induction (L = L′ + p_x + p_y); checked: the merged
  weights sum to L, an exhaustive search over tree shapes finds the same 4.127, and 400 random alphabets (211 also
  against every length assignment) all agree.
* **6. Typical sequences and the source coding theorem.** Letters drawn independently: the surprise per letter of
  4,000 sampled texts concentrates at H as n goes 1 → 10,000 (spread 1.2 → 0.012 bits); the asymptotic equipartition
  property (Shannon 1948; McMillan 1953; Breiman 1957); the typical set and its size, derived; the typical set
  shrinking inside sequence space, exactly, for a coin with the books' space frequency (n = 4: 25% of the sequences,
  40% of the probability; n = 1000: 2⁻¹⁷³ of the sequences, all but one part in 87 million of the probability; the
  likeliest sequence is never typical); the source coding theorem, with Shannon's code on blocks closing in on H
  (0.882 → 0.7041 bits against 0.7036); real text as a vanishing corner of all strings.
* **7. Cross-entropy and KL.** A code as a set of bets (Huffman's lengths against the true p); coding with the wrong
  model as an area; H(p, q) = H(p) + D_KL(p‖q); Gibbs' inequality
  by Jensen (and H(Y | X) ≤ H(Y)); cross-entropy as the training loss of every language model, nats; forward against
  reverse KL, fitted by gradient descent to a two-peaked density, with the fits sliding (the wide fit scores 1.30 bits
  the other way, the narrow one 10.1).
* **8. Arithmetic coding.** Huffman's whole bits (and the 27¹⁰⁰-entry table blocks would need); the chain-rule slivers continued for *the falcon*, the binary
  expansions of the interval's ends agreeing digit by digit; the 29-bit codeword (information content 27.66 bits);
  the two-bit bound, proved; decoding; finite precision: the integer coder's own record, with 16-bit registers,
  narrowing and zooming (with pending bits) through *the falcon* (28 bits); prediction ⇔ compression. (`arithint`
  also runs the whole passage through a 32-bit coder: 41,089 bits against an information content of 41,087.6 with
  24-bit counts, 1,192 extra bits with 8-bit counts; the numbers are in the cache, not in the film.)
* **9. Learning by counting, and Laplace's rule.** Shannon's 1948 approximations, regenerated from the books; the
  counting rule; bits per letter against context length on the books (down to 0.27 at 14 letters) and on the Falcon
  passage (best 2.02 at 5 letters, worse than letter frequencies at 14); unseen contexts; Laplace's rule of succession
  (1814, the sunrise) derived from Euler's beta integral, add-one and add-α smoothing, swept over α at four context
  lengths (Laplace is best for one letter of context, and 0.35 bits worse at eight); generalization.
* **10. Shannon's 1951 experiment.** The identical-twin argument (guess counts are a code); our counting guesser's
  guess counts on 11,994 letters (first guess 58%); Shannon's upper and lower bounds (2.37 and 1.36 bits); his
  subjects (0.6–1.3 bits with 100 letters of context); Cover and King's 1978 estimate.
* **11. Likelihood, softmax and the gradient.** Maximum likelihood = minimum cross-entropy = minimum divergence; counting
  is maximum likelihood; the softmax, step by step; ∂(−ln q_y)/∂z_k = q_k − [k = y], derived: the model's guess
  minus the truth, the signal gradient descent follows.
* **12. Mutual information.** I(X; Y) = H(X) − H(X | Y), symmetric, a divergence; neighbouring letters share 0.75
  bits, two letters back 1.36 (the second alone 0.27); the data-processing inequality from the chain rule, checked on
  the books (the kind of the previous letter keeps 0.35 bits; noise drains the rest); the mutual information between
  letters d apart through 1,000 letters, with a matched shuffled control and finite-sample bias correction.
  A descriptive log-log fit summarizes the positive tail estimates; it does not establish a power law or
  extrapolate beyond the measured distances. Signed estimates and nonpositive control values remain in the data.
* **13. What it takes to guess well.** One paragraph's per-token surprise under GPT-2 and Qwen3-4B (Bull Durham
  tobacco; the telephone, 12.8 bits without the earlier paragraphs and 3.5 with them); knowledge probes; the ladder
  of knowledge.
* **14. Bits per character, bits per token.** Two tokenizers on the same paragraph and passage (GPT-2: 5,458 tokens,
  3.92 characters each; Qwen3: 5,217); total bits = tokens × bits per token = characters × bits per character; per
  token, the counting model looks better than GPT-2 (2.32 bits, perplexity 5.0, against 4.57 and 23.8), per character
  it is twice as bad; perplexity; bits per byte; Huang et al. (2024): bits per character on fresh text against the
  average of twelve benchmarks across 31 models, Pearson −0.93.
* **15. The scoreboard: language modeling is compression.** Bits per character on the passage as printed: plain text 8,
  uniform over its 61 symbols 5.93, letter frequencies 4.55, one character of context 3.58, gzip 3.31, xz 3.20,
  bzip2 2.92, the best counting model 2.32, GPT-2 small 1.17, GPT-2 XL 1.01, Qwen3-0.6B 1.02, Qwen3-4B 0.87; people
  0.6–1.3 (letters only); the gap from counting to under one bit is the series. GPT-2 small as a real compressor, round trip: the first 4,331 characters in 688 bytes
  (xz: 2,180), decoded back exactly by a second run of the model. The catch, the model's size (248 MB for GPT-2 small:
  11,572 times the passage); Delétang et al. (ICLR 2024) on enwik9 (Chinchilla 70B 8.3% against gzip 32.3% and LZMA2
  23.0%, 14,008% counting its weights); the Hutter Prize (2006; record of 24 July 2026: 100,424,672 bytes for enwik9,
  decompressor included, 0.80 bits per character). The rows later parts fill.
* **Recap** in eight computed pictures, where each idea comes back, six problems, Part 2's teaser, references.

Every number the narration states is computed in [`compute.py`](compute.py) (or cited), and the narration is written
over the data: it branches where a sentence depends on a result. Schematics are labeled `schematic`, made-up
examples `illustrative`.

## Build it

```bash
python tools/make.py ai1                  # everything: the computations, then the narrated cut in English and Chinese
python -m videos.ai.ai1.compute           # or just the numbers
python tools/build.py ai1 -q l            # a preview
python tools/build.py ai1 --lang zh       # the Chinese cut
```

`compute.py` downloads 31 Gutenberg books (~40 MB) and, for `lms`, `probes` and `context`, GPT-2, GPT-2 XL and
Qwen3-0.6B/1.7B/4B-Base (~19 GB); about 15 minutes on 4 cores, cached in `.cache/ai1`. The items added for the
expanded part are small: `groups`, `kraft`, `units`, `compress` and `dpi` take seconds; `huffopt` (400 exhaustive
searches) about 15 s; `typical` a second; `smoothing` and `arithint` under a minute; `lmzip` (GPT-2 small encodes and
decodes 1,023 tokens, one at a time, on one core) about 3 minutes. Every random choice is seeded (`compute.rng`), and
each item is saved the moment it finishes, so an interrupted run resumes; `lms` keeps each model's result as it goes.
`coder.py` is the finite-precision arithmetic coder (Witten, Neal & Cleary 1987) used by `arithint` and `lmzip`.

## Sources

Books: T. M. Cover & J. A. Thomas, *Elements of Information Theory*, 2nd ed. (2006), ch. 2, 3, 5, 13; D. J. C.
MacKay, *Information Theory, Inference, and Learning Algorithms* (2003), ch. 2, 4–6; C. M. Bishop & H. Bishop, *Deep
Learning: Foundations and Concepts* (2024), ch. 2.

Papers: R. V. L. Hartley, *Transmission of Information* (1928); C. E. Shannon, *A Mathematical Theory of
Communication* (1948; Theorem 2, the uniqueness of entropy; Theorem 3, the AEP) and *Prediction and Entropy of
Printed English* (1951); L. G. Kraft (MIT thesis, 1949); D. A. Huffman, *A Method for the Construction of
Minimum-Redundancy Codes* (1952), and G. Stix, *Profile: David A. Huffman*, Scientific American (1991); A. A.
Sardinas & G. W. Patterson (1953); B. McMillan, *The Basic Theorems of Information Theory* (1953) and *Two
Inequalities Implied by Unique Decipherability* (1956); L. Breiman, *The Individual Ergodic Theorem of Information
Theory* (1957); S. Kullback & R. A. Leibler, *On Information and Sufficiency* (1951); P.-S. Laplace, *Essai
philosophique sur les probabilités* (1814); R. A. Fisher, *On the Mathematical Foundations of Theoretical Statistics*
(1922); J. Rissanen, *Generalized Kraft Inequality and Arithmetic Coding* (1976); R. Pasco (Stanford thesis, 1976);
I. H. Witten, R. M. Neal & J. G. Cleary, *Arithmetic Coding for Data Compression* (1987); T. M. Cover & R. C. King,
*A Convergent Gambling Estimate of the Entropy of English* (1978); H. W. Lin & M. Tegmark, *Critical Behavior in
Physics and Probabilistic Formal Languages* (2017); G. Delétang et al., *Language Modeling Is Compression* (ICLR
2024; Table 1 for enwik9); Y. Huang, J. Zhang, Z. Shan & J. He, *Compression Represents Intelligence Linearly* (COLM
2024); the Hutter Prize, hutter1.net (records table, consulted October 2026); A. Radford et al., *Language Models are
Unsupervised Multitask Learners* (2019); Qwen Team, *Qwen3 Technical Report* (2025).

Data: Project Gutenberg (thirty novels, listed in `compute.BOOKS`; *The Maltese Falcon*, eBook #77600, released
1 January 2026).

## Problems, with solutions

**1. The grouping rule.** From H = −Σ pᵢ log₂ pᵢ, show H(p₁, p₂, p₃, …) = H(p₁ + p₂, p₃, …) + (p₁ + p₂) H(p₁/(p₁ + p₂),
p₂/(p₁ + p₂)).

*Solution.* Write s = p₁ + p₂. The two sides share every term from p₃ on. What is left on the left is −p₁ log p₁ −
p₂ log p₂; on the right, −s log s + s H(p₁/s, p₂/s) = −s log s − p₁ log(p₁/s) − p₂ log(p₂/s) = −s log s − p₁ log p₁ −
p₂ log p₂ + (p₁ + p₂) log s, which is the same.

**2. A budget overspent.** Can a prefix code have codeword lengths 1, 2, 3, 3, 3? Can any uniquely decodable code?

*Solution.* Σ 2^(−l) = 1/2 + 1/4 + 3/8 = 9/8 > 1. Kraft's inequality rules out a prefix code, and McMillan's
extends the verdict to every uniquely decodable code: with these lengths, some message would always have two readings.

**3. Two optimal codes.** Build a Huffman code for (0.4, 0.2, 0.2, 0.1, 0.1). Find two optimal codes with different
lengths, and compare their average with H.

*Solution.* Merge 0.1 + 0.1 = 0.2. Four weights of 0.4, 0.2, 0.2, 0.2 remain, and the tie decides the shape: merging
the new 0.2 with an old one gives lengths (2, 2, 2, 3, 3); merging the two old 0.2's gives (1, 2, 3, 4, 4). Both
average 2.2 bits (0.8 + 0.8 + 0.6, and 0.4 + 0.4 + 0.6 + 0.8), both are optimal, and H = 0.4 × 1.322 + 0.4 × 2.322 +
0.2 × 3.322 = 2.122 bits: within 0.08 bits of the bound. The first code has the smaller spread of lengths, which
matters for buffering, not for the average.

**4. Typical, but not likely.** A coin lands heads with probability 0.1; toss it 100 times. About how many typical
sequences are there, how likely is each, and how does that compare with the likeliest single sequence?

*Solution.* H = h(0.1) = 0.469 bits, so there are about 2^46.9 ≈ 1.3 × 10¹⁴ typical sequences, each with probability
about 2^(−46.9) ≈ 7.7 × 10⁻¹⁵: together they hold nearly all the probability, though they are only a 2^(−53) sliver
of the 2¹⁰⁰ sequences. The likeliest sequence, all tails, has probability 0.9¹⁰⁰ ≈ 2.7 × 10⁻⁵, about 3.5 billion
times more than any typical one; but its surprise per toss is −log₂ 0.9 = 0.152 bits, far from 0.469. It is not
typical, and you will essentially never see it: there are just too many sequences with about ten heads.

**5. KL is not symmetric.** For p = (½, ½) and q = (¼, ¾), compute D_KL(p‖q) and D_KL(q‖p).

*Solution.* D_KL(p‖q) = ½ log₂(½/¼) + ½ log₂(½/¾) = 0.5 − 0.2925 = 0.2075 bits. D_KL(q‖p) = ¼ log₂(¼/½) + ¾ log₂(¾/½)
= −0.25 + 0.4387 = 0.1887 bits. Coding p's data with q's code wastes more than the other way round.

**6. Laplace's rule.** Derive (s + 1)/(n + 2) from ∫₀¹ θᵃ(1 − θ)ᵇ dθ = a! b!/(a + b + 1)!.

*Solution.* With every chance θ equally likely beforehand, after s successes in n trials the weight of θ is
proportional to θˢ(1 − θ)ⁿ⁻ˢ, and the chance of a success next is the average of θ under that weight:
∫ θˢ⁺¹(1 − θ)ⁿ⁻ˢ dθ / ∫ θˢ(1 − θ)ⁿ⁻ˢ dθ = [(s + 1)!(n − s)!/(n + 2)!] / [s!(n − s)!/(n + 1)!] = (s + 1)/(n + 2).

## 习题与解答

**1. 分组法则。** 由 H = −Σ pᵢ log₂ pᵢ 证明：H(p₁, p₂, p₃, …) = H(p₁ + p₂, p₃, …) + (p₁ + p₂) H(p₁/(p₁ + p₂), p₂/(p₁ + p₂))。

*解答。* 记 s = p₁ + p₂。两边从p₃起的各项相同。左边剩下 −p₁ log p₁ − p₂ log p₂；右边是
−s log s + s H(p₁/s, p₂/s) = −s log s − p₁ log(p₁/s) − p₂ log(p₂/s) = −s log s − p₁ log p₁ − p₂ log p₂ + (p₁ + p₂) log s，
两者相等。

**2. 超支的预算。** 能否有一个前缀码，码字长度为1, 2, 3, 3, 3？能否有任何一个唯一可解码的码？

*解答。* Σ 2^(−l) = 1/2 + 1/4 + 3/8 = 9/8 > 1。克拉夫特不等式排除了前缀码，麦克米兰不等式把这个结论推广到一切唯一可解码的码：
用这些长度，总有某条消息会有两种读法。

**3. 两个最优码。** 为 (0.4, 0.2, 0.2, 0.1, 0.1) 构造霍夫曼编码。找出两个码长不同的最优码，并把它们的平均码长与H比较。

*解答。* 先合并 0.1 + 0.1 = 0.2。剩下 0.4, 0.2, 0.2, 0.2 四个权重，平局决定了树的形状：把新的0.2和一个旧的合并，得到码长
(2, 2, 2, 3, 3)；把两个旧的0.2合并，得到 (1, 2, 3, 4, 4)。两者的平均码长都是2.2比特（0.8 + 0.8 + 0.6，以及
0.4 + 0.4 + 0.6 + 0.8），都是最优的；而 H = 0.4 × 1.322 + 0.4 × 2.322 + 0.2 × 3.322 = 2.122 比特，相差不到0.08比特。
第一个码的码长更整齐，这影响缓冲，不影响平均码长。

**4. 典型，却不是最可能的。** 一枚硬币正面朝上的概率是0.1，抛100次。典型序列大约有多少个？每个的概率是多少？和最可能的那一个序列相比如何？

*解答。* H = h(0.1) = 0.469比特，所以典型序列大约有 2^46.9 ≈ 1.3 × 10¹⁴ 个，每个的概率大约是 2^(−46.9) ≈ 7.7 × 10⁻¹⁵：
它们合起来几乎占据了全部概率，却只是 2¹⁰⁰ 个序列中 2^(−53) 的一小片。最可能的序列是全部反面，概率 0.9¹⁰⁰ ≈ 2.7 × 10⁻⁵，
是任何一个典型序列的大约35亿倍；但它每次抛掷的意外度是 −log₂ 0.9 = 0.152比特，离0.469很远。它不是典型的，你几乎永远不会见到它：
大约十次正面的序列实在太多了。

**5. KL散度不对称。** 对 p = (½, ½) 和 q = (¼, ¾)，计算 D_KL(p‖q) 和 D_KL(q‖p)。

*解答。* D_KL(p‖q) = ½ log₂(½/¼) + ½ log₂(½/¾) = 0.5 − 0.2925 = 0.2075比特。D_KL(q‖p) = ¼ log₂(¼/½) + ¾ log₂(¾/½)
= −0.25 + 0.4387 = 0.1887比特。用q的编码去编p的数据，比反过来浪费得多。

**6. 拉普拉斯法则。** 由 ∫₀¹ θᵃ(1 − θ)ᵇ dθ = a! b!/(a + b + 1)! 推出 (s + 1)/(n + 2)。

*解答。* 事先认为每个机会θ都同样可能；在n次试验中成功了s次之后，θ的权重正比于 θˢ(1 − θ)ⁿ⁻ˢ，而下一次成功的概率是θ在这个权重下的平均：
∫ θˢ⁺¹(1 − θ)ⁿ⁻ˢ dθ / ∫ θˢ(1 − θ)ⁿ⁻ˢ dθ = [(s + 1)!(n − s)!/(n + 2)!] / [s!(n − s)!/(n + 1)!] = (s + 1)/(n + 2)。

## Glossary (new terms in this part, beyond `AI_ZH_GUIDE.md`'s first section)

| English | 中文 |
|---|---|
| Shannon's three requirements; the grouping rule | 香农的三条要求；分组法则 |
| uniqueness of entropy (Shannon's Theorem 2) | 熵的唯一性（香农定理2） |
| Hartley's measure of information | 哈特利的信息度量 |
| uniquely decodable code | 唯一可解码的码 |
| Kraft–McMillan inequality | 克拉夫特–麦克米兰不等式 |
| canonical code | 规范码 |
| exchange argument; sibling (leaves) | 交换论证；兄弟（叶子） |
| optimal code | 最优码 |
| typical set, typical sequence | 典型集，典型序列 |
| asymptotic equipartition property (AEP) | 渐近均分性（AEP） |
| law of large numbers | 大数定律 |
| block code | 分组编码 |
| finite precision; register | 有限精度；寄存器 |
| zoom (renormalization); pending bit | 放大（重新归一化）；待定比特 |
| Laplace's rule of succession; the sunrise problem | 拉普拉斯接续法则；日出问题 |
| prior | 先验 |
| add-one (Laplace) smoothing | 加一（拉普拉斯）平滑 |
| data-processing inequality | 数据处理不等式 |
| chain rule for mutual information | 互信息的链式法则 |
| tokenizer, vocabulary | 分词器，词表 |
| bits per token, bits per byte | 每词元比特数，每字节比特数 |
| perplexity | 困惑度 |
| two-part code; adjusted compression rate | 两段式编码；调整后的压缩率 |
| Hutter Prize; context mixing | 赫特奖；上下文混合 |
| round trip (encode, then decode) | 往返（先编码，再解码） |
