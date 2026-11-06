# Computer Science, Built — Part 21: Strings

Part 21 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth part of Act IV, *Algorithms*. Text is the oldest data. Searching it
efficiently led to automata built from patterns, then to indexes of every suffix, then to a reversible transform
that sorts a book into compressible runs and lets you search the compressed result. Each `git diff` runs a
shortest-path algorithm on a grid. The instrument is `explainer/cs/algo/strings.py`. Its matchers count their
comparisons: naive (with a numpy version for megabytes), Rabin–Karp, KMP and its automaton, Horspool, Boyer–Moore
with the good-suffix rule, and Aho–Corasick. It also has suffix arrays by prefix doubling in numpy (fast enough for
the 25 MB corpus), Kasai's LCP array, suffix-array search, small suffix trees, the BWT and its inverse, an FM-index
with backward search and locate, move-to-front, LZ77 with hash chains, DEFLATE's code lengths, LZW, a byte-wise
rANS coder, Needleman–Wunsch, Smith–Waterman, Myers' O(ND) diff with traceback, patience anchors, rsync's rolling
checksum, gear-hash content-defined chunking, Manacher, periods and Duval's Lyndon factorization. It is tested
against brute force in `tests/test_cs21_strings.py`. Every number is computed in `compute.py`; timings are taken on
this machine.

* **Queequeg, four ways.** 253 occurrences in 25 MB. Naive search makes 24,974,844 comparisons and KMP 24,972,212.
  Boyer–Moore makes 3,500,231 (3,444,788 windows). The FM-index needs 16 rank queries (0.07 ms); grep takes
  19 ms. Search, compress, compare, synchronize.
* **1. Matching, the obvious way.** The sliding window, animated. On the corpus, the naive method makes 1.000–1.088
  comparisons per character. The cost predicted from prefix frequencies, 1 + f(p₁) + f(p₁p₂) + …, matches the
  measurement to the fourth decimal. The worst case aⁿ against a^{m−1}b costs exactly (n − m + 1)m: 99 million
  comparisons at n = 10⁵, m = 10³.
* **2. Rolling hashes.** Karp and Rabin (1987); the rolling update; collision probability by Schwartz–Zippel (Part
  20). Queequeg in *Moby-Dick*: 12,042 false alarms modulo 101, against 12,056 expected (n/p); 1,201 modulo 1,009;
  none modulo 10⁶ and above.
* **3. Knuth, Morris and Pratt.** Borders and the failure function of `ababaca`; the automaton (Part 12), traced on
  a text. ≤ 2n comparisons, proved by amortization: the worst case of chapter 1 costs 199,901 instead of ten
  million. On the corpus, 1.00–1.07 per character.
* **4. Boyer and Moore.** Right-to-left comparison and the bad-character shift, animated; the good-suffix rule on
  `ANPANMAN` (shift 6); Galil's rule; Horspool. On *Moby-Dick*, comparisons per character are 0.54, 0.31, 0.17,
  0.10, 0.075 and 0.049 for patterns of 2 to 64 characters, with Horspool on top of Boyer–Moore. Haertel's account
  of why grep is fast.
* **5. Many patterns at once.** Aho and Corasick's trie for he, she, his, hers, with failure links and inherited
  outputs; building the links breadth-first. 45 character names: a 231-state automaton, one 25-million-step pass
  against 1.1 billion characters read separately.
* **6. Suffix trees.** The tree of `banana$`; Ukkonen's online construction with suffix links and open leaves;
  longest repeats (*Moby-Dick*: 102 characters, a chapter title printed twice), longest common substrings,
  741 billion distinct substrings; 10–20 bytes per character.
* **7. Suffix arrays.** Manber and Myers (1990). The sorted suffixes of *it was the best of times*. Prefix doubling;
  SA-IS; Kasai's LCP array. The whole corpus took 105 s and 100 MB; Queequeg was found with 167 character
  comparisons. The corpus's longest repeat is 383 characters of chapter headings overlapping themselves.
* **8. The Burrows–Wheeler transform.** The rotation matrix of `banana$`, sorted; the LF mapping, animated, inverting
  the transform (and all of *Moby-Dick*). Contexts: L groups characters by what follows (in *Moby-Dick*, 72% of the
  characters before `he` are `t`), so it compresses to about nH_k for every k (Manzini 2001). *Moby-Dick*'s transform has 578,682 runs for 1.2 million characters. Move-to-front
  takes the entropy from 4.44 to 2.68 bits, and bzip2 makes 363 KB against zlib's 483 KB.
* **9. The FM-index.** Ferragina and Manzini (2000). Backward search for `ana`, row ranges drawn; wavelet trees and
  Jacobson's rank. On the corpus, counts take a fraction of a millisecond and locates use suffix-array samples
  every 32 rows. Our teaching version is larger than the text, while a compressed one would be near the 7.1 MB
  bzip2 size of the BWT. BWA and Bowtie.
* **10. Compression, I: Lempel and Ziv.** LZ77's back-references as arcs over *A Tale of Two Cities*; inside DEFLATE;
  an LZ78 parse drawn, and LZW; Ziv and Lempel's optimality for stationary ergodic sources. Our LZ77 + Huffman comes within 6% of `zlib -9` on
  three novels (*Moby-Dick*: 505 KB against 483; bzip2 363, xz 391). DEFLATE's buckets and extra bits, per-block
  codes and lazy matching come first.
* **11. Compression, II: coding the symbols.** Huffman's whole bits against rANS on a skewed source: at p = 0.95
  the entropy is 0.286 bits, Huffman spends 1 and rANS 0.287. On *Moby-Dick*'s bytes the gap is under 1%. Duda's
  ANS, derived. The model is everything: H₀ = 4.44, H₁ = 3.48, H₂ = 2.81 bits; PPM, context mixing, language
  models; zstd.
* **12. Alignment.** Needleman–Wunsch on *intention*/*execution*; Smith–Waterman on two versions of the anonymous
  letter in *The Count of Monte Cristo* (90,000 cells, score 322); Gotoh's affine gaps in three tables; BLAST's
  seeds; edit distance and SETH.
* **13. Myers' diff.** The edit graph of Myers' own example (D = 5), with diagonals and the path. The O(ND) greedy
  algorithm, its furthest-reaching D-paths drawn for D = 0 … 5; patience diff; three-way merge. On the 27 versions of this
  course's syllabus, the first rewrite took 1,475 edits in 0.6 s and most commits took milliseconds. Every D was
  verified minimal against the quadratic LCS; `git diff --minimal` was 2–4 lines longer on 8 of 26.
* **14. rsync and chunking.** 24 bytes inserted into *Moby-Dick*: only 297 of 595 fixed blocks survive. rsync's
  rolling checksum finds 593 blocks and sends 3,257 literal bytes. Gear-hash content-defined chunks: 120 chunks
  averaging 10 KB, and after the edit exactly 1 new chunk (14 KB). LBFS, restic, Borg.
* **15. Periods, palindromes and Lyndon words.** Periods from borders; Fine and Wilf (1965), tight at
  `abaababaaba`; the two-way algorithm. Manacher (1975) over all 19.4 million letters of the novels finds Lenehan's
  *Able was I ere I saw Elba* in *Ulysses*. Lyndon words and the Chen–Fox–Lyndon factorization; Duval; the runs
  theorem.
* **16. Frontier: indexes as small as the information.** Repetitive collections: 27 versions of the syllabus have
  48 characters per BWT run against 2.3 for novels, and xz compresses them 63×. The r-index (Gagie, Navarro and
  Prezza, 2018); move structures; r = O(z log² n) (Kempa and Kociumaka, 2020); the ladder δ ≤ γ ≤ z ≤ r. The
  quadratic wall and its escapes; open problems. Outro.

## Build

```bash
python -m videos.cs.cs21.compute           # every number in the part (about ten minutes; the suffix array is two)
python tools/build.py cs21 -q l            # a 480p preview
python tools/build.py cs21                 # 1080p
```

## Problems, with solutions

1. **KMP is linear.** Prove that the failure function of a pattern of length m is computed in O(m) time, and that
   the search makes at most 2n comparisons.

   *Solution.* In the search, let i be the text position and j the number of matched pattern characters, so the
   pattern's current start is s = i − j. Every comparison either matches, so i increases (and j with it), or
   fails. A failure with j > 0 replaces j by fail[j − 1] < j, so s increases; a failure with j = 0 advances i.
   So every comparison increases i or s. Both lie in [0, n] and never decrease, hence there are at most 2n
   comparisons. The failure function is the same search run on the pattern against itself, with k playing the
   role of j. Each step either increases j, or decreases k, which increases j − k. Both are bounded by m, so the
   work is O(m). Correctness: when p[j] ≠ p[k], the next candidate border of p[0..j] must be a border of p[0..k−1]
   extended by p[j]. The borders of a string are exactly its longest border, the longest border of that, and so
   on, which is why following fail visits all candidates in decreasing order.

2. **The LF property.** Prove that the k-th occurrence of a character c in L and the k-th occurrence of c in F are
   the same character of the text, and deduce that inverting the BWT is correct.

   *Solution.* Consider the rows whose rotations begin with c, in sorted (F) order. Each is c followed by some
   rotation R, and since they all begin with c they are sorted by R. Now consider the rows that end with c, in
   sorted order. Each is a rotation R′ whose last character is c, and these rows are sorted by R′ itself. The
   character c at the end of R′ is the same text character as the c at the start of the rotation cR′. So both
   lists consist of the same occurrences of c, each sorted by the rotation that follows that c, and hence in the
   same order. The k-th c of L is therefore the k-th c of F. LF(i) = C[L[i]] + rank_{L[i]}(L, i) is that position
   in F, and the row at F-position LF(i) is the rotation that starts with L[i]: one step back in the text.
   Starting from the row equal to the text (the one ending in the unique sentinel) and applying LF n times visits
   the text's rotations in reverse order, emitting each one's last character. That is the text read backwards.

3. **Distinct substrings.** Show that a text of length n has exactly n(n+1)/2 − Σ LCP[i] distinct substrings.

   *Solution.* Every substring is a prefix of some suffix. In sorted order, the suffix SA[i] has n − SA[i]
   prefixes. Among them, those of length at most LCP[i] are prefixes of the previous suffix SA[i − 1] too. Those
   longer than LCP[i] are new: any earlier suffix sharing such a prefix would also share it with SA[i − 1],
   because the common prefix of a sorted block of strings is shared by all neighbours inside it. So each distinct
   substring is counted exactly once, at the first suffix in sorted order that has it as a prefix. The total is
   Σ (n − SA[i] − LCP[i]) = n(n+1)/2 − Σ LCP[i]. For *Moby-Dick* this is 741,385,056,131.

4. **Fine and Wilf.** Prove that a string with periods p and q and length n ≥ p + q − gcd(p, q) has period
   gcd(p, q), and that the bound cannot be lowered.

   *Solution.* By induction on p + q, with p > q. If q divides p we are done. Otherwise consider the prefix u of
   length n − q. For i < n − p we have s_i = s_{i+p} = s_{i+p−q}, using period p and then period q backwards (the
   index i + p − q is at least 0). So u has period p − q, and it also has period q. Its length is
   n − q ≥ (p − q) + q − gcd(p − q, q), since gcd(p − q, q) = gcd(p, q). By induction, u has period
   g = gcd(p, q). Since q is a multiple of g and every position of s is within q of a position of u, g is also a
   period of s. For tightness, take the Fibonacci-like strings. `abaababaaba`, of length 11 = 5 + 8 − 2, has
   periods 5 and 8 but not period 1. In general, the central words of the Fibonacci sequence have length
   p + q − 2 with coprime periods p and q.

5. **Build: Horspool on Pebble.** Write Horspool's algorithm in the Pebble language. Count `Queequeg` in the corpus
   on the emulator, and compare its instructions per byte with Part 17's Job.

   *Solution sketch.* The text arrives as a stream of `getc` calls and doesn't fit in Pebble's 1 MiB, so keep a
   ring buffer of the last m = 8 characters. Precompute a 256-entry shift table: shift[c] = m − 1 − (last index of
   c in pattern[0..m−2]), or m. At each window, compare from the right inside the ring buffer. Then read shift[c]
   new characters, where c is the window's last character. Here is the lesson: Boyer–Moore skips comparisons, but
   a stream still has to deliver every byte, so the getc loop (about four instructions per byte: call, test,
   store, advance) sets the floor. Expect roughly 6–8 instructions per byte in all, against the Job v2's 39 and
   the v3's 43, and against about 10 for KMP on the same stream. With the whole text in memory (a 1 MiB passage),
   Horspool's advantage reappears: about 0.14 comparisons per byte for m = 8, as measured in chapter 4. Check the
   count, 253, against `grep -o Queequeg | wc -l`.

6. **★ Research: an index in LZ77 space.** Give a text index in O(z) words, z the number of LZ77 phrases, that
   counts the occurrences of any pattern in O(m polylog n) time, or prove that none exists.

   *Where to start.* Navarro's survey "Indexing highly repetitive string collections" (ACM Computing Surveys,
   2021, two parts) lays out the measures δ ≤ γ ≤ b ≤ z ≤ r and the indexes for each. Known results:
   - the r-index counts and locates in O(r) space (Gagie, Navarro and Prezza, JACM 2020);
   - LZ-based and grammar-based indexes locate in O(z log(n/z)) or O(γ log(n/γ)) space, but counting there needs
     extra machinery (Christiansen, Ettienne, Kociumaka, Navarro and Prezza, "Optimal-time dictionary-compressed
     indexes", 2021);
   - Kociumaka, Navarro and Prezza, "Toward a definitive compressibility measure for repetitive sequences" (2023)
     shows O(δ log(n/δ)) space suffices for access and pattern matching;
   - Kempa and Kociumaka (2020) bound r by O(z log² n).

   Open:
   - (a) counting in O(z) or O(δ) space, rather than with a log(n/z) factor;
   - (b) lower bounds separating what each measure can support;
   - (c) here, measure: z, r and the bzip2 and xz sizes of growing prefixes of the syllabus history and of
     concatenated novels, and plot how each scales.

## 习题与解答

1. **KMP 是线性的。** 证明长度为 m 的模式的失配函数可以在 O(m) 时间内算出，且搜索至多做 2n 次比较。

   *解答。* 搜索中令 i 为文本位置，j 为已匹配的模式字符数，于是模式当前的起点 s = i − j。每次比较要么匹配，i 增加（j 随之增加）；
   要么失败。j > 0 时失败会把 j 换成 fail[j − 1] < j，于是 s 增加；j = 0 时失败则 i 前进。所以每次比较都会增加 i 或 s。两者都在
   [0, n] 中且从不减少，因此至多有 2n 次比较。失配函数就是模式对自身做同样的搜索，k 扮演 j 的角色。每一步要么增加 j，要么减小
   k，从而增加 j − k。两者都不超过 m，所以工作量是 O(m)。正确性：当 p[j] ≠ p[k] 时，p[0..j] 的下一个候选边界必定是 p[0..k−1] 的
   某个边界再接上 p[j]。一个字符串的全部边界恰好是它的最长边界、最长边界的最长边界，依此类推，所以沿 fail 走会按递减顺序访问所有
   候选。

2. **LF 性质。** 证明 L 中字符 c 的第 k 次出现与 F 中 c 的第 k 次出现是文本中的同一个字符，并由此推出 BWT 的逆变换是正确的。

   *解答。* 考虑旋转以 c 开头的那些行，按排序（F）顺序。每一行都是 c 后接某个旋转 R，由于都以 c 开头，它们按 R 排序。再考虑以 c
   结尾的那些行，按排序顺序。每一行都是一个以 c 结尾的旋转 R′，这些行就按 R′ 本身排序。R′ 末尾的 c 与旋转 cR′ 开头的 c 是文本中的
   同一个字符。所以两张表由同样的那些 c 组成，都按紧跟在该 c 之后的旋转排序，因而顺序相同。于是 L 中第 k 个 c 就是 F 中第 k 个 c。
   LF(i) = C[L[i]] + rank_{L[i]}(L, i) 正是它在 F 中的位置，而 F 位置 LF(i) 处的行就是以 L[i] 开头的旋转：在文本中退后一步。从等于
   文本本身的那一行（以唯一的哨兵结尾的那一行）出发，应用 LF n 次，会按逆序访问文本的所有旋转，并依次输出每个旋转的最后一个字符。
   这正是倒着读出的文本。

3. **不同子串的个数。** 证明长度为 n 的文本恰好有 n(n+1)/2 − Σ LCP[i] 个不同的子串。

   *解答。* 每个子串都是某个后缀的前缀。按排序顺序，后缀 SA[i] 有 n − SA[i] 个前缀。其中长度不超过 LCP[i] 的，也是前一个后缀
   SA[i − 1] 的前缀。更长的则是新的：任何更早的后缀若共享这样的前缀，也必定与 SA[i − 1] 共享，因为一组已排序字符串的公共前缀被
   其中所有相邻者共享。所以每个不同的子串恰好被计数一次，计在排序后第一个以它为前缀的后缀上。总数为
   Σ (n − SA[i] − LCP[i]) = n(n+1)/2 − Σ LCP[i]。对《白鲸》，这是 741,385,056,131。

4. **Fine–Wilf 定理。** 证明有周期 p 和 q、长度 n ≥ p + q − gcd(p, q) 的字符串有周期 gcd(p, q)，并且这个界不能降低。

   *解答。* 对 p + q 归纳，设 p > q。若 q 整除 p，则已得证。否则考虑长度为 n − q 的前缀 u。对 i < n − p，有
   s_i = s_{i+p} = s_{i+p−q}：先用周期 p，再向后用周期 q（下标 i + p − q 至少为 0）。所以 u 有周期 p − q，也有周期 q。它的长度
   n − q ≥ (p − q) + q − gcd(p − q, q)，因为 gcd(p − q, q) = gcd(p, q)。由归纳假设，u 有周期 g = gcd(p, q)。由于 q 是 g 的倍数，
   而 s 的每个位置都与 u 的某个位置相距 q 以内，g 也是 s 的周期。紧性：取类斐波那契字符串。`abaababaaba` 长度为
   11 = 5 + 8 − 2，有周期 5 和 8，却没有周期 1。一般地，斐波那契序列的中心词长度为 p + q − 2，且有互素的周期 p 和 q。

5. **动手：Pebble 上的 Horspool。** 用 Pebble 语言写 Horspool 算法，在模拟器上统计语料中 `Queequeg` 的次数，并把它每字节的指令数
   与第17部分的作业比较。

   *解答要点。* 文本以一连串 `getc` 调用到达，放不进 Pebble 的 1 MiB 内存，所以用环形缓冲区保存最后 m = 8 个字符。预先算出一张 256
   项的移动表：shift[c] = m − 1 − （c 在 pattern[0..m−2] 中最后出现的下标），若不出现则为 m。在每个窗口上，在环形缓冲区内从右向左
   比较。然后读入 shift[c] 个新字符，c 是窗口的最后一个字符。要点在于：Boyer–Moore 省掉了比较，但数据流仍然必须送来每一个字节，
   所以 getc 循环（每字节大约四条指令：调用、测试、存储、前进）决定了下限。预计总共每字节约 6–8 条指令，作业 v2 是 39 条、v3 是
   43 条，同一数据流上的 KMP 约为 10 条。当整个文本在内存中时（一段 1 MiB 的文字），Horspool 的优势又出现了：m = 8 时每字节约 0.14
   次比较，正如第4章所测。用 `grep -o Queequeg | wc -l` 核对计数 253。

6. **★ 研究问题：LZ77 空间的索引。** 给出一个占 O(z) 个字（z 为 LZ77 短语数）的文本索引，能在 O(m polylog n) 时间内统计任意模式
   的出现次数，或者证明不存在这样的索引。

   *从哪里开始。* Navarro 的综述《Indexing highly repetitive string collections》（ACM Computing Surveys，2021，分两部分）梳理了
   各种度量 δ ≤ γ ≤ b ≤ z ≤ r 以及对应的索引。已知结果：
   - r-index 在 O(r) 空间内计数和定位（Gagie、Navarro 与 Prezza，JACM 2020）；
   - 基于 LZ 和基于文法的索引在 O(z log(n/z)) 或 O(γ log(n/γ)) 空间内定位，但在那里计数需要额外的机制（Christiansen、Ettienne、
     Kociumaka、Navarro 与 Prezza，《Optimal-time dictionary-compressed indexes》，2021）；
   - Kociumaka、Navarro 与 Prezza 的《Toward a definitive compressibility measure for repetitive sequences》（2023）表明 O(δ log(n/δ))
     空间足以支持访问和模式匹配；
   - Kempa 与 Kociumaka（2020）证明 r 至多为 O(z log² n)。

   未解决：
   - （a）在 O(z) 或 O(δ) 空间内计数，而不带 log(n/z) 因子；
   - （b）区分各个度量能支持什么的下界；
   - （c）在这里动手测量：对教学大纲历史和拼接起来的小说的不断增长的前缀，测量 z、r 以及 bzip2 和 xz 的大小，画出它们各自如何
     增长。

## Glossary additions

模式匹配 pattern matching · 滚动哈希 rolling hash · 边界 border · 失配函数 failure function · KMP 算法 Knuth–Morris–Pratt
algorithm · 坏字符规则 bad-character rule · 好后缀规则 good-suffix rule · 字典树 trie · 失配链接 failure link · 后缀树 suffix
tree · 后缀链接 suffix link · 后缀数组 suffix array · 倍增 prefix doubling · 最长公共前缀数组 LCP array · BWT 变换
Burrows–Wheeler transform · LF 映射 LF mapping · 前移编码 move-to-front · FM 索引 FM-index · 反向搜索 backward search · 小波树
wavelet tree · 秩查询 rank query · 回指 back-reference · 滑动窗口 sliding window · 熵编码 entropy coding · 非对称数字系统
asymmetric numeral systems · 上下文模型 context model · 全局比对 global alignment · 局部比对 local alignment · 仿射空位罚分 affine
gap penalty · 编辑图 edit graph · 蛇形路径 snake · 三方合并 three-way merge · 内容定义分块 content-defined chunking · 去重
deduplication · 周期 period · 回文 palindrome · Lyndon 词 Lyndon word · 重复性度量 measure of repetitiveness · r 索引 r-index

## Sources

*Canon.* Books: Gusfield, *Algorithms on Strings, Trees, and Sequences* (1997); Crochemore, Hancart & Lecroq,
*Algorithms on Strings* (2007); Navarro, *Compact Data Structures* (2016); Mäkinen, Belazzougui, Cunial & Tomescu,
*Genome-Scale Algorithm Design* (2015); Salomon & Motta, *Handbook of Data Compression* (2010); Knuth, *The Art of
Computer Programming*, volume 3; Cover & Thomas, *Elements of Information Theory*, chapter 13.

Papers: Fine & Wilf (1965); Needleman & Wunsch (1970); Weiner (1973); Aho & Corasick (1975); Manacher (1975);
McCreight (1976); Knuth, Morris & Pratt, "Fast pattern matching in strings" (1977); Boyer & Moore, "A fast string
searching algorithm" (1977); Ziv & Lempel (1977, 1978); Galil (1979); Horspool (1980); Smith & Waterman (1981);
Gotoh (1982); Duval (1983); Welch (1984); Myers, "An O(ND) difference algorithm and its variations" (1986); Karp &
Rabin, "Efficient randomized pattern-matching algorithms" (1987); Landau & Vishkin (1988); Jacobson (1989); Manber &
Myers, "Suffix arrays" (1990); Altschul et al., "Basic local alignment search tool" (1990); Crochemore & Perrin,
"Two-way string-matching" (1991); Burrows & Wheeler, "A block-sorting lossless data compression algorithm" (1994);
Ukkonen, "On-line construction of suffix trees" (1995); RFC 1951 (1996); Tridgell & Mackerras, "The rsync
algorithm" (1996); Ferragina & Manzini, "Opportunistic data structures with applications" (2000); Manzini, "An
analysis of the Burrows–Wheeler transform" (2001); Kasai et al. (2001); Muthitacharoen, Chen & Mazières, "A
low-bandwidth network file system" (2001); Crochemore, Landau & Ziv-Ukelson (2003); Nong, Zhang & Chan, "Linear
suffix array construction by almost pure induced-sorting" (2009); Haertel, "why GNU grep is fast" (2010); Duda,
"Asymmetric numeral systems" (2009, 2013); Xia et al., "FastCDC" (2016); Bannai et al., "The runs theorem" (2017).

*Frontier.* Backurs & Indyk (2015); Gagie, Navarro & Prezza, "Fully functional suffix trees and optimal text
searching in BWT-runs bounded space" (2018, JACM 2020); Andoni & Nosatzki (2020); Kempa & Kociumaka, "Resolution of
the Burrows–Wheeler transform conjecture" (2020); Nishimoto & Tabei, "Optimal-time queries on BWT-runs compressed
indexes" (2021); Navarro, "Indexing highly repetitive string collections" (2021); Christiansen, Ettienne, Kociumaka,
Navarro & Prezza (2021); Kociumaka, Navarro & Prezza (2023).
