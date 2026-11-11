# Computer Science, Built — Part 27: Proofs and Randomness

Part 27 of the [61-part course](../README.md), Act V, *Limits and Secrets*.
See the [syllabus](../SYLLABUS.md). This part develops randomized decision classes,
interactive proofs, local testing and their connections to approximation, counting
and cryptographic assumptions.

The teaching instrument is [proofs.py](../../../explainer/cs/algo/proofs.py).
The producer module retains complete finite inputs, outputs and protocol records;
its independent references use exact rational arithmetic, Fourier identities,
native GMP subset dynamic programming and modular CRT determinants. Native Glucose
cross-checks resolved SAT queries. UNSAT agreement is not called a checked proof trace.

## Chapters and scope

| Chapter | Main construction and qualification |
| --- | --- |
| Hook | Sampling, interaction and zero knowledge have different completeness, soundness and security guarantees. |
| 1. Randomized classes | RP/coRP have bounded one-sided error; ZPP has zero error and expected polynomial time on every input. Amplification uses independent runs. |
| 2. Hardness and randomness | Quantitative Nisan–Wigderson / Impagliazzo–Wigderson implications; general arithmetic-circuit PIT is distinct from the known Vandermonde identity. |
| 3. Circuits | Nonuniform polynomial-size families, Karp–Lipton, random restrictions and exact finite decision-tree depth; circuit models and moduli remain fixed in the cited lower bounds. |
| 4. Communication | Equal-length private-coin fingerprints, exact bit accounting, rectangles/rank and one-pass streaming reductions. Insertion-only $F_1$ is a counter. |
| 5. Interaction | Complete GNI challenge records; completeness is existential over provers and soundness universal. Public/private-coin equivalence allows controlled round overhead. |
| 6. Sum-check | Field-valued Boolean-cube sums, individual-degree checks, complete transcripts and adaptive conditional soundness. A full QBF/IP theorem is cited, not implemented. |
| 7. Zero knowledge | Salted-hash commitments and openings are retained. Opened-colour histograms check only a marginal; full zero knowledge requires the complete simulator definition and assumptions. |
| 8. PCP | Perfect-completeness PCP versus the near-perfect-completeness three-query refinement; BLR arithmetic is over $\mathbb F_2$. |
| 9. Approximation | MAX-E3SAT's $7/8$ guarantee, near-satisfiable MAX-E3LIN hardness and problem-specific reduction gaps. Random-instance heuristic scores are not worst-case guarantees. |
| 10. Unique games | General permutation games versus planted cyclic shifts; planted value is a lower bound on optimum. UGC and related hardness promises remain distinct. |
| 11. Fine-grained | Explicit SETH/OV dimensions and machine models; full SAT-to-OV vectors and witnesses. Fixed 64-bit negative fixtures are timing examples. |
| 12. Parameterized | Complete covers and Buss kernels; FPT/W[1] qualifications and fixed-formula, fixed-treewidth Courcelle scope. |
| 13. Counting | Exact permanent versus determinant, full matrices and independent checks; arithmetic operations versus bit complexity, oracle counting and FPRAS scope. |
| 14. Average case | Complete planted graphs and factors; finite recovery rates do not establish a hardness threshold or a one-way function. Lattice reductions retain their parameters. |
| 15. Frontier | MIP* = RE with unbounded finite-dimensional provers; protocol-specific succinct-argument assumptions, setup and public-input costs. |
| Outro | Six worked exercises, connections to later parts and the distinction between finite verification and general theorems. |

## Computations

```bash
python -m unittest tests.test_cs27_proofs -v
python -m videos.cs.cs27.compute             # build every missing/current item
python -m videos.cs.cs27.compute --force zk  # explicit fresh run
python tools/build.py cs27 -q l              # preview
python tools/build.py cs27                   # native-resolution build
```

The 18 schema-2 producers include the 16 original experiments plus the two worked
exercise computations. Each retains a raw evidence artifact before validation and
a separately checked artifact afterwards, with source hashes and actual call times.
Validation failures retain their full objects and failure records.

Timing tables for vertex cover, permanent/determinant and OV/3SUM use thirty actual
calls per fixture, reporting medians. Multiplication uses five actual batches of
1,000 operations per size. PIT records every actual point evaluation. Serialization
and independent checking occur outside the reported teaching-call intervals. These
are measurements of the stated implementations on the current host.

Examples include all 7,500 sampled DNF restrictions, 2,200 GNI rounds, 3,301 complete
sum-check protocol runs, 220 planted graphs and every fixed/variable-dimension OV
input. The random unique-game baseline draws independent labels from one generator
per trial; the original constant-label bug and its data remain in the QA history.
The experiments use seeded `random.Random`, not a cryptographic random generator.

## Problems, with solutions

1. **Amplification.** Reduce BPP error from $1/3$ to $2^{-k}$.

   Run the algorithm independently an odd number $t$ of times. If $X$ is the number
   of incorrect answers, then $\mathbb E X\le t/3$ and a wrong majority requires
   $X\ge t/2$. Hoeffding gives $\Pr[X\ge t/2]\le e^{-t/18}$. Choose an odd
   $t\ge18k\ln2$. Independence is necessary for this argument; the input is fixed.
   The producer checks numerical binomial tails against exact rational sums.

2. **Deterministic equality.** Prove an $n$-bit lower bound.

   Fix the deterministic communication model in which each transcript leaf has a
   monochromatic rectangle. The $2^n$ diagonal inputs $(x,x)$ require distinct
   accepting rectangles: a rectangle containing $(x,x)$ and $(y,y)$ would also
   contain the unequal input $(x,y)$. Thus depth is at least $n$. If the model
   requires a monochromatic output leaf for both parties, there is also a rejecting
   leaf and the usual worst-case bound is $n+1$ for $n\ge1$. If only Bob outputs,
   Alice can simply send $n$ bits. State which convention is being used.

   For randomized equal-length fingerprints, choose a prime $q$, view strings as
   polynomials of degree at most $n-1$, and send the evaluation point and value.
   This costs $2\lceil\log_2q\rceil$ bits and errs with probability at most
   $\min(1,(n-1)/q)$ on unequal strings. Public coins change the accounting.

3. **Sum-check soundness.** Show an upper bound $nd/p$.

   Assume a prime field of size $p$, individual degree at most $d<p$, and a fresh
   uniform verifier challenge after each prover message. While the current claim
   is false, any message passing the endpoint-sum check differs from the true
   univariate polynomial. Two distinct degree-at-most-$d$ polynomials agree at
   no more than $d$ points. Conditional on any prior transcript with a false claim,
   the probability of repairing that claim is therefore at most $d/p$. If no round
   repairs it, the final direct evaluation rejects. A union bound gives
   $\min(1,nd/p)$; sequential conditional probabilities also give
   $1-(1-d/p)^n$. The success events need not be independent.

   The verified quantity is a field-valued sum. Integer #SAT recovery needs a
   sufficiently large modulus or additional reconstruction. Repeated occurrences
   of a variable contribute to its individual degree; an empty formula still has
   a well-defined constant sum.

4. **Buss's kernel.** Bound the residual graph.

   Use a simple undirected graph and budget $k$. A vertex of degree greater than
   the remaining budget must be selected, because omitting it forces all its
   distinct neighbours. Delete it and decrement the budget. In the residual graph,
   degree is at most $k'\le k$. A cover of size $k'$ covers at most $k'^2$ edges;
   more edges imply failure. After deleting isolated vertices, at most $k'$ cover
   vertices and $k'^2$ neighbours remain. The algorithm must normalize duplicate
   edges before applying degree rules. The retained regression with three copies
   of each edge $(0,1)$ and $(1,2)$ has the one-vertex cover $\{1\}$; the original
   implementation incorrectly rejected it. Linear-time kernel implementations
   exist, but this teaching routine repeatedly scans its edges.

5. **Build: transcript-bound hash challenges.** Reproduce the structured
   20-variable example and its mutation checks.

   The formula has ten disjoint clauses $(x_1\lor x_2),\ldots,(x_{19}\lor x_{20})$,
   so its count is $3^{10}=59{,}049$. Work over $p=2^{61}-1$, with individual
   degree one. The honest prover exploits the disjoint-pair factorization to sum
   the Boolean suffixes; this particular counting instance is easy. Native code
   separately enumerates all $2^{20}$ assignments to check the count.

   Canonically serialize the statement, field, degree bound and claim, followed by
   the full message/challenge history. Prefix the bytes with the versioned domain
   `CS27-SUMCHECK-FS-TEACHING-v1` and a NUL byte. Derive each challenge using SHA-256
   with an encoded retry counter and rejection sampling into the field; include
   each accepted challenge in subsequent hash inputs. The verifier checks message
   length, endpoint sums and the final formula evaluation. Preserve the actual
   messages, hashes, challenges and six cases: honest proof, changed claim, changed
   message, changed formula, truncation and oversized message.

   These finite checks establish the behaviour of this demonstration. They do not
   prove generic Fiat–Shamir security, a random-oracle theorem for an arbitrary
   protocol, zero knowledge, succinctness or security of a deployed system.

6. **Research: exact BLR minima.** Exhaust all four-bit Boolean functions.

   Use truth-table bit $x$ for $f(x)$ and compare against all linear parities,
   including zero and excluding constant-one offsets. For each of the 65,536
   functions, retain the exact Hamming distance numerator and the number of
   rejecting ordered pairs $(x,y)$ among 256 pairs. The producer uses Walsh
   coefficients; independent native code directly enumerates parities and pairs.

   | Distance numerator, out of 16 | Minimum rejecting pairs, out of 256 |
   | --- | --- |
   | 0 | 0 |
   | 1 | 42 |
   | 2 | 72 |
   | 3 | 90 |
   | 4 | 96 |
   | 5 | 90 |
   | 6 | 120 |
   | 7 | 166 |
   | 8 | 256 |

   Each minimum has a retained complete truth-table witness. Adding a linear
   parity and applying an invertible linear variable change preserve rejection
   and distance. They do not remove the need for a complete orbit argument when
   reducing a larger search. These exact finite minima do not prove a formula for
   every dimension.

## 习题与解答

1. **放大。** 对固定输入独立运行奇数次 $t$，以多数决定答案。每次错误率至多三分之一，
   错误多数需要比期望多至少 $t/6$ 次错误。Hoeffding 界为 $e^{-t/18}$；取不小于
   $18k\ln2$ 的奇数 $t$，便使错误率至多 $2^{-k}$。不能把相关重复当作独立重复。

2. **相等判定。** 在每个输出叶子对应单色矩形的确定性通信模型中，$2^n$ 个对角输入必须
   属于不同的接受矩形，否则会误收交叉的不等输入，因此至少需要 $n$ 位。双方都要由叶子
   知道答案的常见约定，对 $n\ge1$ 得到 $n+1$ 位；若只让 Bob 输出，Alice 发送 $n$ 位即可。
   私有随机指纹假设等长串和素数域，发送点与值，成本为 $2\lceil\log_2q\rceil$，误差至多
   $\min(1,(n-1)/q)$。公开随机模型的计费不同。

3. **Sum-check。** 假设素数域、逐变量次数界 $d<p$，且每轮先收消息，再独立均匀抽挑战。
   当前声称为假时，通过端点求和检查的多项式必须不同于真实多项式，因此至多在 $d$ 个点上
   一致。对任何此前的假声称对话条件，修复概率都至多 $d/p$。并集界给出 $nd/p$；逐步条件
   论证给出 $1-(1-d/p)^n$，不需要各轮成功事件独立。协议验证域上的和；整数计数还需足够大
   的模数或重建信息。重复出现的变量必须计入次数，空公式也有明确的常数和。

4. **Buss 核。** 先把边规范化成简单无向图。若顶点度数超过剩余预算，不选它就必须选入
   全部不同邻居，所以它被强制选入。剩余预算为 $k'$ 时，最大度数至多 $k'$，覆盖至多
   $k'$ 个顶点只能覆盖 $k'^2$ 条边。删除孤立顶点后，至多剩 $k'^2+k'$ 个顶点。重复边若被
   误计为不同邻居，可能错误拒绝实际可解的实例；保留的三重复边路径回归展示了这个旧错误。
   线性时间核化存在，但教学实现会重复扫描边。

5. **动手：哈希挑战。** 实际例子是十个互不相交的二变量或子句，计数为 $3^{10}$，并用
   独立本地程序枚举全部 $2^{20}$ 个赋值核对。在 $2^{61}-1$ 域上，证明者利用该实例的可分解
   结构生成逐变量一次消息。哈希输入包括规范化语句、域、次数、声称和完整消息挑战历史，
   带版本域分离与 NUL 字节，并用拒绝采样得到均匀域元素。保留真实消息、摘要、挑战以及
   改动声称、消息、公式、截断和超次数等检查。教学演示不等于一般 Fiat–Shamir 安全证明，
   也不自动得到零知识、简洁性或实际部署安全。

6. **研究：BLR 最小值。** 穷举全部四位布尔函数，保留每个函数的精确距离与拒绝有序对数量。
   Python 用 Walsh 谱计算，独立本地程序直接枚举所有奇偶函数和全部 256 对输入。上表的每个
   最小值都附有完整真值表见证。这里的线性函数包含零函数，不包含常数一偏移。加上线性
   函数和可逆线性换元保持距离与拒绝率；把它用于更大搜索时，仍须证明轨道覆盖完整。
   有限穷举没有证明所有维数的一般公式。

## Sources and reading scope

- Arora & Barak, *Computational Complexity* (2009), especially randomized classes,
  circuit complexity, interaction, PCPs and counting; Goldreich, *Computational
  Complexity* (2008); Wigderson, *Mathematics and Computation* (2019).
- Thaler, [*Proofs, Arguments, and Zero-Knowledge*](https://people.cs.georgetown.edu/jthaler/ProofsArgsAndZK.pdf):
  inspected sum-check's degree/message checks and the random-oracle / Fiat–Shamir
  discussion, including the additional soundness conditions for many rounds.
- Håstad, [*Some Optimal Inapproximability Results*](https://www.csc.kth.se/~johanh/optimalinap.pdf),
  JACM 2001; inspected the downloaded February 2002 manuscript's introduction and
  three-query linear-equation test, including its near-perfect completeness.
- Kabanets–Impagliazzo, [ECCC TR02-055 and revision](https://eccc.weizmann.ac.il/report/2002/055/):
  inspected the abstract's integer arithmetic-circuit hypothesis, Boolean/arithmetic
  lower-bound disjunction and partial formula-PIT converse. An attempted author-PDF
  retrieval failed and is not claimed as a downloaded proof.
- Gill; Adleman; Sipser–Gács–Lautemann; Nisan–Wigderson; Impagliazzo–Wigderson;
  Schwartz–Zippel; AKS: the definitions, quantitative hypotheses and representations
  matter, rather than an unqualified statement that all randomness is removable.
- Goldwasser–Micali–Rackoff; Babai; Goldwasser–Sipser; LFKN; Shamir;
  Goldreich–Micali–Wigderson; Fiat–Shamir: distinguish information-theoretic proofs,
  computational commitments, honest-verifier marginals and full zero knowledge.
- Arora–Safra; Arora–Lund–Motwani–Sudan–Szegedy; Dinur; Blum–Luby–Rubinfeld;
  Bellare–Coppersmith–Håstad–Kiwi–Sudan; Kaufman–Litsyn–Xie: finite local tests and
  their extremal bounds are distinct from a complete PCP construction.
- Khot; Khot–Regev; Khot–Kindler–Mossel–O'Donnell; Raghavendra;
  Charikar–Makarychev–Makarychev; Arora–Barak–Steurer; the 2018 Grassmann / games
  results: retain promise, alphabet and completeness parameters. The attempted
  ECCC Grassmann-page retrieval returned HTTP 503; no proof reading is claimed.
- Williams; Grønlund–Pettie; Downey–Fellows; Buss–Goldsmith; Chen–Kanj–Xia;
  Courcelle: hypotheses, word/bit cost, parameter dependence and dated bounds matter.
- Valiant; Toda; Valiant–Vazirani; Stockmeyer; Jerrum–Sinclair–Vigoda;
  Kasteleyn / Temperley–Fisher: exact, oracle-assisted and randomized approximate
  counting are different guarantees. The matching count uses the permanent of a
  bipartite adjacency matrix, not an arbitrary graph adjacency matrix.
- Levin; Håstad–Impagliazzo–Levin–Luby; Ajtai; Regev; Feigenbaum–Fortnow;
  Bogdanov–Trevisan; Kučera; Alon–Krivelevich–Sudakov; Pollard; Brent: average-case
  distribution, negligible success and lattice approximation/noise conditions remain explicit.
- Ji–Natarajan–Vidick–Wright–Yuen, [*MIP⋆ = RE*](https://arxiv.org/abs/2001.04383),
  first announced 2020: inspected the abstract and stated consequences of arXiv v4,
  16 October 2026. The finite-dimensional tensor-product/commuting-operator distinction
  and unbounded prover resources do not produce a halting decider.
- Kilian; Micali; Goldwasser–Kalai–Rothblum; Groth16; Zerocash; transparent argument
  systems: proof size, setup, zero knowledge, public input and verifier work depend on
  the particular construction. No production security audit is claimed here.

English/Chinese source and sampled-preview verification are separate from continuous
narrated listening, synthesized Chinese speech/listening, whole-video native review
and runtime approval at the chosen narration pace. Those production gates remain open.
