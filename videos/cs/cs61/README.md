# Computer Science, Built — Part 61: Doing Research

Part 61 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the sixth and last part of Act XI, *The Research Frontier*, and the coda of the
series. The series has quoted a thousand results; this part asks where they come from, and how you would make one.
We reproduce a famous measurement-bias experiment on this machine and find that, with the stack already placed at
random on every run, noise alone explains what we see; then we time the Job rigorously, watch benchmarks and analyses
fail, settle small cases of conjectures by computer, and practise reading, reviewing, choosing a problem and writing.
It ends on the open problems the series met, gathered on one map, on the bridges to *AI, Built* and *Analysis, Built*,
and on the tower one last time.

The instrument is in `explainer/cs/research/` (tested in `tests/test_cs61_research.py`):
* `method.py`: the measurement-bias experiment after Mytkowicz et al. (a word-counting C kernel in the Job's style,
  a hash-mixing function and a driver that fills 16 MiB with pseudo-random letters and spaces and times four passes;
  built once with `gcc -O2`, linked in three orders, and run with an unused environment variable padded from 0 to
  4,096 bytes in steps of 128: five interleaved rounds over the sizes, then fifteen rounds over the link orders with
  the variable empty); percentile bootstrap intervals; the Job in plain Python on the thirty novels, timed 30 times,
  with intervals after 3, 5, 10, 20 and 30 runs; arithmetic against geometric means of two illustrative speedups;
  Goldbach's conjecture checked to 2,000,000 by a sieve and a strike-out pass per prime, with its records; the
  Collatz conjecture below 1,000,000, each path followed only until it drops below its start, with the record
  stopping times; and the eleven open problems the series met, with their records and parts.

The scenes also read other parts' caches: Part 1's piles, Part 2's Ramsey check, Part 7's predictors and Amdahl
limit, Part 54's proof kernel, Part 60's Job, and the final ledger (from Part 60, or Part 55 before it).

## Chapters

* **Hook.** One C program, compiled once, timed on this machine while only an unused environment variable grows
  from nothing to 4 KiB: the median time moves by up to 7%. Mytkowicz, Diwan, Hauswirth and Sweeney (2009) showed
  that such changes move where the stack begins, and with it the alignment of hot data; but with the stack
  randomized on every run, is our spread that effect or only noise? Where results come from: a question, a method,
  evidence, a paper. The plan.
* **1. What research is.** A vague question ("does the environment affect speed?") sharpened until it could come out
  wrong; hypothesis, prediction, test, and Popper's falsifiability (1934). Three kinds of evidence: proof (Turing
  1936, Part 25; proof assistants, Part 54), experiment (Mytkowicz et al.), construction (Ritchie and Thompson's Unix
  paper, 1974, Part 31). The shape of a paper and the three questions it answers: does it matter, is it right, is it
  new. Conferences (SOSP since 1967, STOC 1969, POPL 1973) against journals (*JACM*, 1954) and arXiv (1991);
  Fortnow (2009). This part's own experiment written as a paper: 33 sizes × 5 runs and 3 link orders × 15 runs;
  medians spread 6.7% across sizes and 0.9% across link orders, both within the noise; the threats to validity; no
  effect shown, which is not the same as no effect.
* **2. Measurement bias.** Linux copies the environment strings to the top of the new stack, so every byte added moves
  every frame down: a hot local's address is 16⌊(T − e − c)/16⌋ + k, one of four places in a 64-byte cache line (Part
  9) and 256 in a 4 KiB page; a line split (illustrative) and 4K aliasing. Experiment one: 33 sizes in 128-byte steps,
  5 interleaved runs each; the medians spread 6.7%, the fastest of each five 5.3%, while 15 more runs of the one
  unchanged setting range over 22%, three times the medians' spread. Experiment two: three link orders, 15 runs each
  with the environment empty; the medians differ by 0.9%, far inside the scatter. What the 2009 paper found (bias on
  every processor and both compilers tried, in most of SPEC CPU2006's C programs; enough to change whether `-O3`
  looked faster than `-O2`; none of the hundred-odd papers it surveyed adequately accounted for it), its remedies
  (setup randomization, causal analysis), and Curtsinger and Berger's Stabilizer (2013). The verdict: 4,000 noise-only
  experiments, each drawing 33 medians of 5 from the 45 runs with an empty environment, typically spread 10%, and 89%
  of them exceed our 6.7%. Shown: the medians moved. Not shown: that the environment moved them; with address
  randomization on, Linux starts the stack at a different 16-byte step on every run, a setup randomization done for
  us.
* **3. Measuring rigorously.** Thirty runs of the Job in plain Python on the same 25 million characters: best
  0.865 s, worst 0.962 s (11% slower), mean 0.907 s; Georges, Buytaert and Eeckhout (2007) on single-number
  reporting. Start-up against steady state for a JIT-compiled runtime (Part 15; illustrative), and our runs in order:
  no trend, the slowest is run 18. The bootstrap (Efron 1979) derived and run: a 95% interval for the mean from
  0.897 to 0.917 s. More runs, narrower intervals: 62 ms wide after 3 runs, then 41, 29 and 26, and 20 ms after 30,
  beside the prediction ±1.96 s/√n (four times the runs for half the width); the centre drifts from 913 ms to
  907 ms. Averaging speedups (illustrative times: A takes 1 s and 4 s, B 2 s and 2 s): the arithmetic mean of the
  ratios says each is a quarter slower than the other, the geometric mean says 1 either way round (Fleming and
  Wallace 1986), and for a fixed workload the totals, 5 s against 4 s, are the honest summary.
* **4. Benchmarks and reproducibility.** Dhrystone (Weicker 1984); the SPEC suites from 1989 to 2017, with matrix300
  and libquantum dropped. Goodhart's law (1975, in Strathern's 1997 phrasing), the loop from measure to target, a
  score drifting from the real programs (illustrative), and benchmark-detecting phones (2013) and Volkswagen's
  diesels (2015). How SPEC keeps score: ratios to a reference machine, their geometric mean, and why the reference
  cancels; base and peak, disclosure, review, retirement. The garden of forking paths (Simmons, Nelson and
  Simonsohn 2011; Gelman and Loken 2013): 1 − 0.95²⁰ ≈ 0.64; in our data, the fastest environment size against the
  slowest is a 6.7% "speedup". Repeatable, reproducible and replicable in the ACM's terms; Collberg and Proebsting
  (2016); artifact evaluation since 2011; this series' compute, cache and load pipeline.
* **5. Proof as research.** The life of a conjecture: Goldbach (1742; checked to 4 × 10¹⁸ by 2014), Euler's sums of
  powers (1769; refuted 1966), four colours (1852; Kempe's failed proof, 1879; Appel and Haken by computer, 1976,
  Part 18; Gonthier in Coq, 2005). What a search proves: every even number from 4 to 2,000,000 is a sum of two primes,
  a theorem; the hardest case, 1,077,422 = 601 + 1,076,821, needs only the 110th prime. The Collatz check as strong
  induction (Part 2): the path from 7 climbs to 52 and falls to 5, and every start below 1,000,000 reaches 1. Euler
  refuted by Lander and Parkin: 27⁵ + 84⁵ + 110⁵ + 133⁵ = 144⁵ = 61,917,364,224; Elkies (1988) and Frye's
  95800⁴ + 217519⁴ + 414560⁴ = 422481⁴, both checked in exact integers. When the evidence misleads: Liouville's λ for
  n ≤ 20, its running sum touching zero at 2, 4, 6, 10 and 16; Pólya's conjecture, Haselgrove (1958), Tanaka's first
  failure at 906,150,257 (1980). What a proof asks you to trust: Part 2's pigeonhole argument; Part 2's check of all
  2¹⁵ = 32,768 colourings (0 escape), the four colour theorem, Hales on Kepler (1998) and Part 26's 200-terabyte
  Pythagorean-triples proof (2016); a kernel (Coq's four colours, 2005; Flyspeck, 2014; Part 54's 69 lines and 11
  rules).
* **6. Reading and reviewing.** Keshav's three passes (2007). The five Cs on an invented abstract ("Skim", 2.1 times
  faster on thirty novels). Finding what is not said, phrase by phrase: which texts; how many runs (our Job's 30
  runs spread 11%); which baseline (an unused variable moved our medians 6.7%); how much is "little"; no
  limitations, threats or code. The third pass as this part's rebuild of the 2009 paper, which found the paper's own
  remedy, setup randomization, already switched on. Writing a review of the invented paper (summary, strengths,
  weaknesses, questions, verdict and confidence); Smith's "The task of the referee" (1990).
* **7. Finding problems.** Hamming's "You and Your Research" (1986): the lunch questions, important means it would
  matter and you have an attack, ten to twenty problems in mind. Compound interest taken literally (illustrative):
  1.1ⁿ = 2 at n = ln 2 / ln 1.1 ≈ 7.3 years. Pólya's *How to Solve It* (1945): six quarts from a 4- and a 9-quart pail,
  worked backwards (6 = 9 − 3; the 4 takes 3 if it holds 1; 1 = 9 − 4 − 4), against Part 2's search of every state.
  Limit studies: the Job's branches on Part 7's predictors, 8.8% mispredicted by 2-bit counters, 5.7% by TAGE at
  9 KB, 2.5% with no storage limit; Amdahl's law with 1 − p = 0.002854, so S ≤ 350; the ledger's 58 s in Part 13
  against 0.81 s with Part 17's hash table, about 72 times. Working backwards from the ideal: Belady (1966) for
  caches (Parts 9, 32); for the Job, Part 17's hash table at about 29 cycles a byte against one byte a cycle, 31 ms
  (Part 60).
* **8. Writing.** Toulmin's argument (1958) on this part's result: claim, data (6.7% across 33 sizes, 5 runs each),
  warrant, backing (the 4,000 simulated experiments), qualifier, rebuttal (unless address randomization hides a real
  effect). Every claim and its evidence, on the invented paper. Figures that carry the claim, from chapter 2's link
  orders: medians only on an axis cut at 0.138 s, the tallest bar 7.6 times the shortest, against all 45 runs, where
  the medians differ by under 1% and each order's runs spread 18% to 35%; Tufte (1983). How a computed number
  travels, from `method.py` through `compute.py` and `bias.json` to `load("bias")` and the spoken 7%. Three kinds of
  number, three labels (computed here, published, illustrative); Hamming on writing; Zobel.
* **9. Frontier: the open-problems map.** The eleven open problems the series met, as a sky over the tower, each with
  the year it was asked and its parts: P versus NP (1971; Part 26), one-way functions (1976; Parts 29, 30), the
  exponent of matrix multiplication (1969; ω < 2.372 in 2024; Parts 19, 52), BB(6) (1962; BB(5) = 47,176,870 proved in
  2024; Part 25), dynamic optimality (1985; Tango trees, 2004; Part 17), the unique games conjecture (2002; the 2-to-2
  theorem, 2018; Parts 23, 56), BPP = P? (1980; PRIMES in P, 2004; Parts 20, 27), circuit lower bounds (1949; about
  3.1n gates, 2022; Parts 3, 26), a memory model for C (2011; out-of-thin-air; Part 33), practical quantum advantage
  (1994; error correction below threshold, 2024; Part 53), verified software at scale (1969; seL4 and CompCert;
  Part 54). Start with the small cases: Goldbach to 2,000,000 (22 records of the smallest prime needed, the last
  1,077,422 with 601), Collatz below 1,000,000 (the longest, 837,799, takes 524 steps). Choosing a problem: important
  and attackable; a special case first; a new tool for an old problem; measure the headroom. The ★ research problem.
* **10. Where the series meet.** The thirty novels of *AI, Built* Part 1 (*Pride and Prejudice* … *Ulysses*), on
  which that series trains and scores its models (held-out passage: *The Maltese Falcon*, chapter 2), and which this
  series' Job counts: 24,971,526 bytes, 4,609,954 words. Seven bridges between the towers: Part 23 and *AI, Built* 11
  (gradient descent), 57 and 8 (generalization), 60 and 17 (the roofline), 28 and 1 (typical sets); Part 1 and
  *Analysis, Built* 1 (computable numbers and Cantor's diagonal), 19 and 9 (Fourier), 52 and 2 (convergence). One
  step on three towers: Taylor's theorem gives f(x − f′(x)/L) ≤ f(x) − f′(x)²/2L when f″ ≤ L, run on log cosh x with
  L = 1, and the 2/L ceiling on the learning rate. More crossings, dashed: Part 18 and *AI, Built* 5 (PageRank, Markov
  chains), 20 and 3 (Johnson–Lindenstrauss), 54 and 25 (Lean).
* **11. The pebble, the last time.** Part 1's piles, 24 and 18 to 6 and 6, gcd 6; Hilbert and Ackermann (1928) and
  Turing (1936). The tower the series built, floor by floor, with its two columns and Part 55's question of trust.
  The ledger, all 22 rows on a log scale: Part 6's single-cycle Pebble 281 s, Part 15's λ-core 2.4 hours, Part 60's
  word-counting unit 31.5 ms; 3 rows timed natively. First row against last: 281.04 s / 0.031464 s ≈ 8,932, a product
  of 21 steps, 9 of them slower; the largest step forward ×1,699 (Part 15 to 16), the largest back ÷149 (Part 13 to
  15); the geometric mean, 1.54 per step (chapter 3's rule). The sky above the top floor, and *calculus*, a small
  stone.
* **Outro.** Act XI in six lines; the series map, sixty-one parts; the final reading list; thank you.

## Build

```bash
python -m videos.cs.cs61.compute
python -m unittest tests.test_cs61_research
python tools/build.py cs61
```

The `ledger` item copies the final ledger from Part 60's cache (or Part 55's), so run that part's compute first. The
`bias` and `timing` items measure this machine, so a machine that is busy while they run will give other numbers,
and the narration will follow them.

## Problems, with solutions

This part sets one problem: the ★ research problem that closes chapter 9.

1. **★ Research.** Pick one star from the series, find its smallest open special case, and settle it.

   *Discussion.* Open by design: the problem asks you to choose an open question and cut it down until it is small
   enough to finish. Each star on the map is open because it has resisted every known method, and the obstacles do not
   vanish in special cases: Part 26's barriers (relativization, natural proofs, algebrization) rule out whole families
   of techniques, so a special case is worth having only if you can say which known obstacle it avoids. Three of the
   series' earlier ★ problems show the shape of a good cut. BB(6) shrinks to single six-state machines whose halting is
   unknown, such as Antihydra (Part 1's ★), whose fate is a Collatz-like question about the parities of
   ⌊3h/2⌋-iterates. Circuit lower bounds shrink to exact minimum circuits for every function of a few inputs (computed
   to four inputs in Part 3's ★, with the last five-input cases closed by SAT solvers) and to the Minimum Circuit Size
   Problem, and the Ramsey frontier to the clique numbers of Paley graphs (Part 2's ★). A good partial answer (1)
   states the special case precisely, with a parameter that measures its size; (2) shows that it is open, from the
   literature, and that the cases below it are settled, by citation or by computation; (3) settles it, or settles a
   smaller case and says exactly what blocks the next one, which is itself a result; and (4) writes it up as chapter 8
   asks, with every claim matched to its evidence and the threats to validity stated. A search proves a finite
   statement exactly and can find a counterexample; it never proves the infinite one, so the write-up must say which
   kind of result it is. Where to start in the repository: `goldbach` and `collatz` in
   `explainer/cs/research/method.py` show the pattern of a search that proves a finite statement and keeps the records
   that show where a proof would have to work hardest; Part 26's SAT solver is the tool for finite combinatorial
   cases; and Part 54's kernel is the place to check a proof once you have one.

## 习题与解答

本讲只有一道题：第 9 章结尾的 ★ 研究题。

1. **★ 研究。** 从本系列中挑一颗星，找出它最小的、尚未解决的特殊情形，并解决它。

   *讨论。* 这道题本身就是开放的：它要求你选一个未解决的问题，把它切小，直到小得可以做完。地图上的每颗星之所以未解决，是因为它抵挡住了
   所有已知的方法，而这些障碍在特殊情形中并不会消失：第 26 讲的几道壁垒（相对化、自然证明、代数化）排除了整类的技术，
   所以一个特殊情形只有在你能说明它绕开了哪一道已知障碍时才值得做。本系列前面的三道 ★ 题已经给出了好的切法。BB(6) 可以缩小为一台台停机与否
   尚不清楚的六状态机器，比如反九头蛇（第 1 讲的 ★），它的命运是关于 ⌊3h/2⌋ 迭代奇偶性的一个类似 Collatz 的问题。电路下界可以缩小为少数
   几个输入的每个函数的精确最小电路（第 3 讲的 ★ 算到四个输入，五个输入的最后几种情形由 SAT 求解器解决），以及最小电路规模问题（MCSP）；
   Ramsey 前沿则可以缩小为 Paley 图的团数（第 2 讲的 ★）。好的部分结果应当：（1）精确地陈述这个特殊情形，并给出衡量其大小的参数；（2）根据文献说明它尚未解决，并通过引用或计算
   说明比它小的情形都已解决；（3）解决它，或者解决一个更小的情形并准确说明是什么挡住了下一个，这本身就是一个结果；（4）按第 8 章的要求写出来，
   每个论断都对应它的证据，并写明对有效性的威胁。搜索能精确地证明一个有限的命题，也能找到反例，但永远证明不了无限的命题，所以文章必须说清楚
   结果属于哪一种。在本仓库里从哪里开始：`explainer/cs/research/method.py` 中的 `goldbach` 和 `collatz` 展示了这种模式：搜索证明一个有限的
   命题，并记录下那些显示证明在哪里最费力的纪录；第 26 讲的 SAT 求解器是处理有限组合情形的工具；有了证明之后，第 54 讲的内核是检查它的地方。

## Glossary additions

* **falsifiability, hypothesis, prediction** — a claim some observation could refute; what it predicts; the test.
* **measurement bias, setup randomization, causal analysis** — a systematic error from an innocuous-looking part of
  the setup; measuring over many random setups; changing one suspected cause alone and checking that the effect
  follows.
* **address-space layout randomization (ASLR)** — the operating system placing the stack (and other regions) at a
  random address on every run.
* **threats to validity** — the ways an experiment's conclusion could be wrong, stated by its authors.
* **start-up and steady-state performance, warm-up** — the time of the first iterations against the time after a
  runtime has settled.
* **bootstrap, resample, confidence interval** — drawing n values from the sample with replacement, many times, and
  reading an interval from the spread of the statistic.
* **geometric mean** — the n-th root of a product; a mean of ratios that gives the same verdict whichever way round
  they are taken, and whichever reference they are normalized to.
* **benchmark, synthetic benchmark, Goodhart's law** — a program whose speed stands for others'; one written to be
  representative; a measure that becomes a target stops being a good measure.
* **base and peak results** — one set of compiler flags for every benchmark in a language; flags tuned per benchmark.
* **garden of forking paths, p-hacking, false alarm** — the many analysis choices between data and claim; choosing
  among them until a test passes; a significant result with nothing behind it.
* **repeatable, reproducible, replicable; artifact evaluation** — the same team and setup; another team with the
  authors' artifacts; another team with its own setup; a committee running a paper's code and data.
* **conjecture, counterexample, computer-assisted proof, trusted base** — a statement believed and unproved; a case
  that refutes it; a proof with a program in it; what a proof asks you to trust.
* **Liouville's λ, Pólya's conjecture** — (−1) to the number of prime factors counted with repetition; the claim that
  its running sum never rises above zero, false first at 906,150,257.
* **three-pass reading, the five Cs, referee report** — Keshav's method; category, context, correctness,
  contributions, clarity; a review's summary, strengths, weaknesses, questions and verdict.
* **limit study, headroom** — the best possible, measured before the work; the gap between it and today.
* **Toulmin model: claim, data, warrant, backing, qualifier, rebuttal** — the parts of an argument.

## Sources

* T. Mytkowicz, A. Diwan, M. Hauswirth and P. Sweeney, "Producing wrong data without doing anything obviously
  wrong!", ASPLOS 2009; C. Curtsinger and E. Berger, "Stabilizer: statistically sound performance evaluation",
  ASPLOS 2013.
* A. Georges, D. Buytaert and L. Eeckhout, "Statistically rigorous Java performance evaluation", OOPSLA 2007;
  R. Jain, *The Art of Computer Systems Performance Analysis* (Wiley, 1991); B. Efron, "Bootstrap methods: another
  look at the jackknife", Annals of Statistics 7(1), 1979; P. Fleming and J. Wallace, "How not to lie with
  statistics: the correct way to summarize benchmark results", Communications of the ACM 29(3), 1986.
* R. Weicker, "Dhrystone: a synthetic systems programming benchmark", Communications of the ACM 27(10), 1984;
  J. Hennessy and D. Patterson, *Computer Architecture: A Quantitative Approach* (on SPEC and matrix300);
  M. Strathern, "'Improving ratings': audit in the British university system", European Review 5(3), 1997.
* J. Simmons, L. Nelson and U. Simonsohn, "False-positive psychology", Psychological Science 22(11), 2011;
  A. Gelman and E. Loken, "The garden of forking paths" (2013); C. Collberg and T. Proebsting, "Repeatability in
  computer systems research", Communications of the ACM 59(3), 2016; ACM, "Artifact review and badging".
* K. Popper, *Logik der Forschung* (1934; *The Logic of Scientific Discovery*, 1959); L. Fortnow, "Time for computer
  science to grow up", Communications of the ACM 52(8), 2009.
* L. Lander and T. Parkin, "Counterexample to Euler's conjecture on sums of like powers", Bulletin of the AMS 72,
  1966; N. Elkies, "On A⁴ + B⁴ + C⁴ = D⁴", Mathematics of Computation 51, 1988; C. B. Haselgrove, "A disproof of a
  conjecture of Pólya", Mathematika 5, 1958; T. Oliveira e Silva, S. Herzog and S. Pardi, "Empirical verification of
  the even Goldbach conjecture and computation of prime gaps up to 4·10¹⁸", Mathematics of Computation 83, 2014.
* G. Gonthier, "Formal proof — the four-color theorem", Notices of the AMS 55(11), 2008; T. Hales et al., "A formal
  proof of the Kepler conjecture", Forum of Mathematics, Pi 5, 2017; M. Heule, O. Kullmann and V. Marek, "Solving and
  verifying the Boolean Pythagorean triples problem via cube-and-conquer", SAT 2016.
* S. Keshav, "How to read a paper", ACM SIGCOMM Computer Communication Review 37(3), 2007; A. J. Smith, "The task of
  the referee", IEEE Computer 23(4), 1990.
* R. Hamming, "You and your research", a talk at Bellcore, 1986; G. Pólya, *How to Solve It* (Princeton, 1945);
  L. Belady, "A study of replacement algorithms for a virtual-storage computer", IBM Systems Journal 5(2), 1966;
  D. Wall, "Limits of instruction-level parallelism", ASPLOS 1991.
* S. Toulmin, *The Uses of Argument* (Cambridge, 1958); E. Tufte, *The Visual Display of Quantitative Information*
  (Graphics Press, 1983); J. Zobel, *Writing for Computer Science* (3rd ed., Springer, 2014).
* S. Aaronson, "P =? NP", in *Open Problems in Mathematics* (Springer, 2016); the records on the open-problems map
  are cited in the parts that met them.

## The end of the series

This is the last part of *Computer Science, Built*: sixty-one parts in eleven acts, from two piles of pebbles and a
rule to the open problems on chapter 9's map. One program, the Job, kept score the whole way, and its ledger runs from
Part 6's 281 s on a single-cycle Pebble to Part 60's 31.5 ms in a circuit. Every measured number in the series is
recomputed by its parts' `compute.py`; the [series plan](../README.md) lists every part, and the sibling series are
*AI, Built* ([`../../ai/`](../../ai/README.md)) and *Analysis, Built*
([`../../analysis/`](../../analysis/analysis1/README.md)).
