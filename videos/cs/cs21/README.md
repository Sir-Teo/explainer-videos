# Computer Science, Built — Part 21: Strings

Part 21 of the [series](../README.md) connects matching, indexing, compression, alignment and synchronization.
The instrument is [strings.py](../../../explainer/cs/algo/strings.py); [compute.py](compute.py) builds 17 guarded
schema-2 payloads. [measurement_references.py](measurement_references.py) supplies independent references, and
[stream_horspool.py](stream_horspool.py) supplies the tested streaming prototype used in exercise 5.

## What the pictures establish

- Slide a pattern, count comparisons, and derive the exact finite-prefix identity. Rolling hashes distinguish
  fixed-base observations from a randomized-base theorem. KMP's borders and automaton explain its linear bound.
  Boyer–Moore's shifts and the `ANPANMAN` example explain safe skipping; the measured implementation omits
  Galil's refinement and can still take O(nm). Aho–Corasick adds failure links and inherited outputs to a trie.
- Draw a small suffix tree built from SA/LCP, then illustrate Ukkonen's online construction separately. Sort all
  suffixes of the corpus by prefix doubling. Follow the BWT rotation matrix and LF mapping, then backward
  search for `ana`. A separate two-lane diagram distinguishes count work from locating selected occurrences.
- Show LZ back-references as arcs and LZ78 dictionary growth as phrase boxes. Separate token bit-cost models
  from emitted zlib/bzip2/xz files. Trace finite rANS states; context-entropy bars explain why the model matters.
- Fill global/local alignment grids, illustrate affine scoring, and follow Myers' furthest-reaching paths on
  the edit graph. Compare fixed blocks, rolling checksums and content-defined chunks after a 24-byte insertion.
  Draw periods, borders and Lyndon factorizations; scope the palindrome query to its exact normalization/filter.
- Compare full BWT run counts for equal-length texts. Explain dated repetitive-index results without asserting
  that a historical open question is still open. Explicit witness bars show two equal 428-byte intervals and
  the first unequal byte, alongside the complete-search certificate needed to establish a maximum.

## Measurements and limits

The matching corpus has **24,971,555 bytes** from thirty novels. Offsets and comparisons in these instruments
refer to bytes. The suffix/BWT/FM corpus adds one unique smallest `\0` terminator; user queries exclude it.
The compression producer's separate literal concatenation has 24,971,526 bytes (29 inter-book separators fewer).
Chapter-level BWT experiments also include their terminator. These are distinct, explicitly sized inputs.

- `Queequeg` has **253 occurrences**. Naive, KMP and Boyer–Moore make 24,974,844, 24,972,212 and 3,500,231
  character comparisons. Grep uses `-a -o -F` and its complete occurrence output is checked. A warm FM count
  uses 16 rank requests; locating the first five matching rows adds 69 rank requests. These are different units
  of work. The build is excluded from query timing; positions are checked against full native-match references.
- The longest exact repeat is **428 bytes**, at offsets **13,188,812** and **13,188,303**. The following bytes
  are 66 and 67. The old greedy block extension stopped at 383 after skipping residual matches. The replacement
  extends every adjacent suffix pair through its first mismatch. An independent native Kasai scan agrees.
- Moby-Dick has **741,383,838,433 distinct nonempty substrings of its original bytes**. The artificial terminal
  is excluded from n. The former terminal-inclusive result counted an extra 1,217,698 substrings. An independent
  native LCP sum checks the corrected value and the 102-byte longest repeat.
- The cached int32 suffix array occupies 99,886,224 array bytes; the `.npy` header, original text and construction
  temporaries are separate. Prefix doubling uses O(log n) sorting rounds; its total cost depends on the integer
  sort used. The small tree is not an executed Ukkonen implementation.
- The teaching FM-index keeps 24,971,556 BWT bytes, 229,426,428 occurrence-checkpoint bytes and a **modeled**
  3,121,448 bytes of four-byte suffix samples. Python dictionaries and container overhead, input text, the full
  construction suffix array and temporaries are excluded. The 7,093,132-byte bzip2 file of the BWT is a file-size
  reference, not the size of a searchable index. Samples are selected by **text offset** divisible by 32;
  reaching one takes at most 31 LF steps. Locate timing averages at most the first five matching rows, not all hits.
- LZ77/Huffman and growing-width LZW columns are payload **cost models**, without full framing or codebooks.
  They are not complete DEFLATE/GIF files. LZ tokens round-trip and LZW passes an independent decoder. Actual
  zlib/bzip2/xz streams are decoded and checked. No universal compressor ranking follows from three novels.
  Classic universal-LZ asymptotic results do not promise universality for this fixed 32 KiB window/bounded search.
- rANS uses a quantized empirical model. Emitted state bytes are included; the frequency table and decoded
  length are external metadata and excluded. Both original and BWT/MTF streams round-trip. The skew experiment
  compares **empirical** H0 of each seeded 200,000-symbol sample with coding costs. A finite state step need not
  add exactly the symbol's information content. The BWT alone is a permutation and leaves H0 unchanged.
- Both full 300×300 local-alignment tables and the global example are checked against an independent list-DP
  implementation. The local score is 322. Affine-gap equations are an illustration, not a measured implementation;
  their convention charges o+eℓ for a gap of length ℓ. Conditional edit-distance lower bounds concern their stated
  unit-cost problem and worst-case assumptions, not all scoring systems or every structured input.
- The history snapshot contains **52 full commit IDs and content hashes**. Diff uses chronological adjacent
  pairs (51 scripts), each reconstructed and checked minimal by an independent LCS distance. Repetitiveness uses
  reverse-chronological git traversal, literal concatenation without separators, then one terminal. The resulting
  13,758,063-byte text has 150,581 BWT runs; the equal-length novel prefix has 5,800,029. Display strips are selected
  for near-average run density, not random samples. xz emits 117,040 bytes and is verified by decoding.
- Myers' D counts insertions and deletions; a substitution costs two. With N=n+m, O(N(D+1)) covers D=0 too.
  This implementation retains an O(D²) trace. A shortest script is a possible transformation, not causal edit
  history. A different git diff length does not imply corrupt output.
- The rsync instrument uses the rsync-style weak rolling checksum and exact byte equality in place of a strong
  hash. It is not zlib's Adler-32 convention. Of the edited bytes, 593×2,048 are reused and 3,257 are literal.
  All gear-hash chunk reuse decisions are checked with full byte chunks, independently of truncated 64-bit hashes.
  One new chunk has 14,006 bytes in this experiment; resynchronization is not an unconditional guarantee.
- The palindrome query keeps ASCII letters, lowercases them, and requires at least **four distinct letters**.
  Its maximum over 19,384,729 normalized letters is the 19-letter `ablewasiereisawelba`. Independent native odd/even
  scans check this filter and maximum. It is not an unrestricted longest-palindrome claim about original prose.

All timings are shared-host observations using `perf_counter`, with raw repetitions and min/single labels in
payloads. Expected references are prepared outside timed regions, and outputs are checked after timers stop.
They are not controlled before/after speedup estimates. Regression checks cover empty/long patterns, arbitrary
sentinel-like bytes, SA order, invalid BWT/FM input, bounded LF walks, entropy/rANS domains and malformed streams.

## Build and verify

```bash
source /workspace/environment/activate.sh
PYTHONPATH=. .venv/bin/python -m unittest discover -s tests -p test_cs21_strings.py -v
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python -m videos.cs.cs21.compute sa --force
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 .venv/bin/python -m videos.cs.cs21.compute --force
PYTHONPATH=. .venv/bin/python tools/build.py cs21 -q l
```

Preview QA records and numerical/native reference code live in the workspace evidence packet
`docs/qa/evidence/cs21-polish-20261110/`. Source/preview checks do not certify continuous narrated listening,
Chinese synthesized speech/listening, whole-video native production, or production runtime at the chosen pace.

## Six exercises with solutions or reproducible build guidance

1. **KMP's bound.** Prove O(m) failure preprocessing and at most 2n search comparisons.

   Let i be the text position, j the matched-prefix length and s=i−j the alignment start. Every comparison
   increases i or, on a nonzero fallback, s; both never decrease and are bounded by n. Hence at most 2n.
   Preprocessing uses the same monotonic accounting on the pattern. Correctness follows because every shorter
   candidate border is a border of the previous longest border, so the failure chain visits all candidates.

2. **LF is reversible.** Assume one unique smallest terminal. Prove that occurrence ranks in L and F align.

   Sort the rotations after each occurrence of c. In F, the corresponding rows start with c and are ordered
   by the following rotation. In L, they end with c and have the same relative order because the following
   rotations have the same prefixes through their first difference. Thus the k-th c of L corresponds to the
   k-th c of F: LF(i)=C[c]+rank_c(L,i), using exclusive rank. LF moves the row's start one byte backward cyclically.
   The unique terminal identifies the original row; n LF steps visit the cycle and emit the reversed text.
   Without the unique terminal or a valid single cycle, this instrument rejects the input.

3. **Count distinct substrings without counting the terminal.** Derive n(n+1)/2−ΣLCP.

   Suffix SA[i] contributes n−SA[i] prefixes. Its first LCP[i] prefixes already occur on the preceding suffix.
   Any earlier suffix sharing a longer prefix would force that same prefix on every intervening sorted suffix,
   including the predecessor. The longer prefixes are therefore new, giving the formula. If the SA includes
   a unique smallest terminal, use n equal to the **original** length: terminal-containing common prefixes are
   zero, and the terminal-only suffix contributes nothing. Moby-Dick gives 741,383,838,433. `banana` gives 21−6=15;
   counting `banana\0` as seven original symbols would instead give 22, seven too many.

4. **Fine–Wilf and tightness.** If n≥p+q−gcd(p,q), prove gcd(p,q) is a period.

   Induct on p+q, with p>q and g=gcd(p,q). If q divides p, q is already a period. Otherwise the prefix u of
   length n−q has periods q and p−q: for i<n−p, s[i]=s[i+p]=s[i+p−q]. Its length is at least p−g, the induction
   threshold for those periods, so u has period g. Since p≥q+g, n≥2q; every omitted suffix position has a q-step
   predecessor in u. As q is a multiple of g, this extends the g-period to the entire string. At length 11,
   `abaababaaba` has periods 5 and 8 but not 1; the threshold is 12. A universal threshold cannot be reduced by one.

5. **Build streaming Horspool, then port it to Pebble.** Count `Queequeg`, including overlapping matches.

   The completed Python prototype is [stream_horspool.py](stream_horspool.py). Precompute shift[c]=m−1−last(c)
   over pattern positions before the last, default m. Keep m bytes in a ring, compare right to left, then consume
   the indicated number of bytes through the ring. The search skips comparisons but still reads every input byte.
   Exhaustive binary strings/patterns at three input chunk sizes agree with brute force and the array instrument.
   The full corpus returns all 253 exact positions after reading 24,971,555 bytes, with 3,500,231 comparisons.
   For a Pebble port, use a 256-entry table, ring, head and total-read counters; handle the final partial refill
   without searching an incomplete window. Compare complete positions/counts before timing the emulator. **No
   Pebble port or emulator instruction count is supplied or claimed here.** Instructions per byte must be measured,
   including all `getc`, ring maintenance and output operations, rather than inferred from comparison savings.

6. **Research: reproduce an index tradeoff and audit its model.** Use growing prefixes of the captured history
   and novels; pin ordering, separator and end-marker conventions. Measure allocated bytes, construction,
   count and locate separately; verify every returned occurrence. Compare your teaching FM layout with a named
   published repetitive index, and record that paper's word size, alphabet, randomization and query assumptions.

   A worked starting point is the equal-length 13,758,063-byte experiment: r=150,581 for history and 5,800,029 for
   novels, or about 91 and 2.37 bytes per run. These are full counts. The 117,040-byte xz stream shows compressibility
   but provides no rank/locate operation. The teaching FM buffers above exceed the text before Python overhead;
   their BWT bzip2 file is not a searchable-index measurement. A faithful study reports these distinctions instead
   of drawing a speed/space conclusion from unlike objects. Extend the size series and add a real index build;
   do not label a current question open without a dated primary-source review.

## 习题与解答

1. **KMP。** 令文本位置为 i、已匹配前缀长度为 j，起点 s=i−j。每次比较增加 i，或在失配回退时增加 s；
   两者单调且至多 n，因此比较至多 2n 次。失配预处理用相同的单调记账，耗时 O(m)。所有较短候选边界必为
   上一个最长边界的边界，因此沿失配链不会漏掉候选。
2. **LF。** 假设只有一个唯一最小结束标记。对字符 c 的各次出现，F 中以 c 开头的行按其后旋转排序；L 中
   以 c 结束的对应行有相同相对顺序。因此第 k 个 c 对应第 k 个 c，LF(i)=C[c]+rank_c(L,i)，rank 不含位置 i。
   LF 把起点循环向前移一字节；唯一结束标记确定原始行，走 n 步输出逆序文本。无唯一标记或不是有效单环的输入会被拒绝。
3. **不同子串。** 后缀 SA[i] 有 n−SA[i] 个前缀，其中前 LCP[i] 个已经出现。若更早后缀共享更长前缀，排序区间
   中间的后缀也必须共享它，与 LCP 定义矛盾。求和得 n(n+1)/2−ΣLCP。n 应为原文长度，不含人工结束标记；
   `banana` 有 15 个不同非空子串。《白鲸》为 741,383,838,433。把人工标记当原文字节会多算。
4. **Fine–Wilf。** 对 p+q 归纳，p>q，g=gcd(p,q)。若 q 整除 p 则已成立；否则长度 n−q 的前缀同时有周期 q 和
   p−q，因为 s[i]=s[i+p]=s[i+p−q]。前缀长度达到归纳门槛 p−g，故有周期 g。又因 n≥2q，余下每个位置均有
   前缀内的 q 步前驱，而 g 整除 q，周期 g 可延伸到整串。长度 11 的 `abaababaaba` 有周期 5、8，却无周期 1；门槛是 12。
5. **构建。** 已完成的 Python 原型保留 m 字节环形缓冲与 256 项位移表，右到左比较，再读入位移数量的新字节。
   跳过比较不等于跳过输入。小例子穷举与三种输入分块通过；完整语料读入 24,971,555 字节，找回全部 253 个位置。
   Pebble 移植须处理不完整末窗，并先核验完整输出，再实测模拟器指令数。本部分没有提供或声称已执行 Pebble 移植，
   不能从比较次数直接预测每字节指令数。
6. **研究。** 固定输入族、顺序、分隔符与结束标记，分别测实际空间、构造、计数、定位，并核验完整输出。
   等长实验中历史与小说的 r 分别是 150,581 与 5,800,029；xz 的 117,040 字节输出不是可搜索索引。
   阅读有日期的一手论文，记录字长、字母表、随机性与查询假设，再扩展规模系列并构建真正索引。
   声称问题尚未解决之前，必须检查更新工作。

## Primary research references and scope

- Gagie, Navarro and Prezza, [Fully-Functional Suffix Trees and Optimal Text Searching in BWT-runs Bounded Space](https://arxiv.org/abs/1809.02792),
  2018 preprint / JACM 2020. The O(r)-word locating result includes additional structures and a word-RAM model;
  search cost and per-occurrence cost are separate. This part does not implement the r-index.
- Kempa and Kociumaka, [Resolution of the Burrows–Wheeler Transform Conjecture](https://arxiv.org/abs/1910.10631),
  FOCS 2020: r=O(z log²n), for the paper's LZ parsing convention. Our bounded-window parser is a different object.
- Kociumaka, Navarro and Prezza, [Towards a Definitive Compressibility Measure for Repetitive Sequences](https://arxiv.org/abs/1910.02151),
  and Navarro's [DCC 2022 keynote](https://datacompressionconference.org/Keynotes/DCC2022KeynoteSlides-Navarro.pdf).
  δ≤γ≤b≤z is one hierarchy. **r and z are incomparable**; the old universal z≤r ladder was false.
- Andoni and Nosatzki, [Edit Distance in Near-Linear Time: it's a Constant Factor](https://arxiv.org/abs/2005.07678),
  2020 / revised 2022: randomized constant-factor approximation in n^(1+η) for any fixed η>0; the constant depends
  on η. It is not an n·polylog n theorem. The chapter presents selected dated results, not a complete 2026 survey.

The packet preserves actual abstract/metadata and keynote reads. These support the scoped statements above;
no full-proof verification or exhaustive current open-problem survey is claimed.
