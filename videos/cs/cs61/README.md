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
* `method.py`: the measurement-bias experiment after Mytkowicz et al. (a word-counting C kernel in the Job's style, a
  hash-mixing function and a driver that fills 16 MiB with pseudo-random letters and spaces and times four passes;
  built once with `gcc -O2`, linked in three orders, and run with an unused environment variable padded from 0 to
  4,096 bytes in steps of 128: five interleaved rounds over the sizes, then fifteen rounds over the link orders with
  the variable empty); percentile bootstrap intervals; the Job in plain Python on the thirty novels, timed 30 times,
  with intervals after 3, 5, 10, 20 and 30 runs; arithmetic against geometric means of two illustrative speedups;
  Goldbach's conjecture checked to 2,000,000 by a sieve and a strike-out pass per prime, with its records; the Collatz
  conjecture below 1,000,000, each path followed only until it drops below its start, with the record stopping times;
  a probe that prints a local variable's address from 20 fresh runs of a C program, and counts the distinct addresses,
  their offsets in a cache line and a page, and the kernel's ASLR setting; and the eleven open problems the series
  met, with their records and parts.

The scenes also read other parts' caches: Part 1's piles, Part 2's Ramsey check, Part 7's predictors and Amdahl
limit, Part 54's proof kernel, Part 60's Job, and the final ledger (from Part 60, or Part 55 before it).

## Chapters

* **Hook.** One C program, compiled once, timed on this machine while only an unused environment variable grows from
  nothing to 4 KiB: the median time moves by up to 7%. Mytkowicz, Diwan, Hauswirth and Sweeney (2009) showed that such
  changes move where the stack begins, and with it the alignment of hot data, enough to decide which of two compiler
  settings looked faster; but with the stack randomized on every run, is our spread that effect or only noise? Where
  results come from: a question, a method, evidence, a paper. The plan.
* **1. What research is.** A vague question ("does the environment affect speed?") sharpened until it could come out
  wrong (which variable, which program, which machine, compared with what); hypothesis, prediction, test, and Popper's
  falsifiability (1934). Three kinds of evidence: proof (Turing 1936, Part 25; proof assistants, Part 54), experiment
  (Mytkowicz et al.), construction (Ritchie and Thompson's Unix paper, 1974, Part 31). The shape of a paper and the
  three questions it answers: does it matter, is it right, is it new. Conferences (SOSP since 1967, STOC 1969, POPL
  1973) against journals (*JACM*, 1954) and arXiv (1991); Fortnow (2009). This part's own experiment written as a
  paper: 33 sizes × 5 runs and 3 link orders × 15 runs; medians spread 6.7% across sizes and 0.9% across link orders,
  both within the noise; the threats to validity; no effect shown, which is not the same as no effect.
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
  randomization on, Linux starts the stack at a different 16-byte step on every run, a setup randomization done for us
  (the `stack` probe: 20 runs of a C program printing a local's address gave 20 distinct addresses, 4 offsets within a
  64-byte line and 20 within a page, with `randomize_va_space` = 2).
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
  faster on thirty novels). Finding what is not said, phrase by phrase: which texts; how many runs (our Job's 30 runs
  spread 11%); which baseline (an unused variable moved our medians 6.7%); how much is "little"; no limitations,
  threats or code. The third pass as this part's rebuild of the 2009 paper, which asked whether the stack starts at
  the same address on every run (here it does not) and so found the paper's own remedy, setup randomization, already
  switched on. Writing a review of the invented paper (summary, strengths, weaknesses, questions, verdict and
  confidence); Smith's "The task of the referee" (1990).
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
* **Outro.** Act XI in six lines; the series map, sixty-one parts; six problems, the series' last; the final reading
  list; thank you.

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

1. **No effect, and a spread.** Thirty-three settings, five runs each, and no real effect: show why the spread of the
   33 medians grows with the number of settings, and estimate the runs per setting that bring it under 2%.

   *Solution.* With no effect, the 33 medians are independent draws from one distribution: that of a median of 5
   runs, with some standard deviation s. The spread is their range over the smallest. The expected range of k
   independent normal draws is d(k)·s, with d(2) = 1.13, d(5) = 2.33 and d(33) = 4.16. It grows without bound, roughly
   like 2√(2 ln k), because every extra setting is another chance of an extreme value. So the spread grows with the
   number of settings even though no setting differs. On chapter 2's data: the 45 runs with an empty environment
   have median 0.1391 s, and a median of 5 drawn from them has s = 3.1 ms. That predicts a spread of
   4.16 × 3.1 / 139 ≈ 9.5%, close to the 9.9% typical of chapter 2's 4,000 noise-only experiments. Two settings would
   typically spread only 1.5%. If s fell like 1/√r with r runs per setting, getting under 2% would take
   r ≈ 5 × (9.9 / 2)² ≈ 120. Resampling the pool directly gives a smaller answer. The typical spread is 2.3% at 30
   runs, 2.0% at 35 and 1.9% at 40 (95th percentile 2.9%), so about 40 runs a setting. The rule overestimates
   because a median of 5 is still pulled about by the pool's long right tail (runs up to 0.177 s), and a median of 40
   ignores it. The resampling can only reproduce the tail the 45 runs happened to show. At 33 × 40 runs of about
   0.14 s, the whole experiment takes about three minutes. Better still, compare settings with a test rather than
   the range (problem 5).

2. **Geometric means.** Prove that the geometric mean of speedups does not depend on the reference machine, and build
   two programs on which the arithmetic mean of ratios favours each machine in turn.

   *Solution.* Write G(a) = (∏ aᵢ)^{1/n}. G is multiplicative, G(aᵢbᵢ) = G(a)G(b), and G(1/a) = 1/G(a). Machine X's
   score against a reference R is G(t_{R,i}/t_{X,i}) = G(t_R)/G(t_X). The ratio of two scores is therefore
   G(t_Y)/G(t_X), from which t_R has cancelled: every reference gives the same ranking. For the arithmetic mean A,
   take chapter 3's two programs: X takes 1 s and 4 s, Y takes 2 s and 2 s, and a score is the mean of t_R/t (bigger
   is better). With X as the reference, X scores (1 + 1)/2 = 1 and Y scores (1/2 + 2)/2 = 1.25: Y is 25% "faster".
   With Y as the reference, X scores (2 + 1/2)/2 = 1.25 and Y scores 1: X is 25% "faster". The geometric mean scores
   them 1 and 1 under either reference (G(1, 4) = 2 = G(2, 2)). In general, Cauchy–Schwarz gives
   (Σ rᵢ)(Σ 1/rᵢ) ≥ n², so A(r)·A(1/r) ≥ 1, with equality only when all the ratios are equal. Whenever the ratios
   differ, at least one way of normalizing therefore makes the other machine look faster; here both do. For a fixed
   workload, the totals (5 s against 4 s) remain the honest summary.

3. **The bootstrap for a median.** Derive the bootstrap percentile interval for a median, and show its width falls
   like 1/√n; check it on chapter 3's thirty runs.

   *Solution.* Sort the sample, x₍₁₎ ≤ … ≤ x₍ₙ₎. A resample of n draws with replacement has a median below or at x₍ⱼ₎
   when at least (n + 1)/2 of its draws are among the j smallest values. For odd n,
   P(m* ≤ x₍ⱼ₎) = P(Bin(n, j/n) ≥ (n + 1)/2), so the bootstrap distribution can be computed exactly, without
   simulation. For even n, the median averages the two middle draws, and in practice one simulates B resamples. The
   percentile interval is the 2.5% and 97.5% quantiles of that distribution. For a density f that is continuous and
   positive at the median m, the sample median is asymptotically normal: √n(m̂ − m) → N(0, 1/(4f(m)²)). The bootstrap
   distribution reproduces that spread, so the interval's width is about 2 × 1.96 / (2f(m)√n) = 1.96/(f(m)√n), which
   falls like 1/√n. Check on the thirty runs (median 0.904 s): the bootstrap interval is 0.894 to 0.919 s, 25.0 ms
   wide. A normal density with the runs' standard deviation, 28.4 ms, has f(m) = 14.1 per second and predicts
   25.5 ms. A kernel density estimate gives f(m) = 12.3 and predicts 29.0 ms. Over the first 3, 5, 10, 20 and 30
   runs the median's interval is 62, 62, 41, 42 and 25 ms wide. Times √n, that is 108, 139, 131, 190 and 137:
   roughly constant, but lumpy, because a bootstrap median can only take the values of order statistics (or their
   midpoints). A distribution-free check: x₍₁₀₎ to x₍₂₁₎ covers the median with probability
   1 − 2P(Bin(30, ½) ≤ 9) = 95.7%. That gives 0.894 to 0.920 s, almost the bootstrap's interval.

4. **Twenty comparisons.** Twenty independent comparisons are each tested at α = 0.05. Derive the chance of at least
   one false positive, and the Bonferroni threshold that keeps it under 5%.

   *Solution.* With no real effect, each test stays quiet with probability 0.95, and independent tests all stay quiet
   with probability 0.95²⁰. So P(at least one) = 1 − 0.95²⁰ = 0.642. Bonferroni uses the union bound,
   P(A₁ ∪ … ∪ A₂₀) ≤ Σ P(Aᵢ) = 20α′, so testing each comparison at α′ = 0.05/20 = 0.0025 keeps the familywise rate
   at or below 5% whether or not the tests are independent. Under independence the exact rate is
   1 − 0.9975²⁰ = 0.0488, and the exact threshold (Šidák) is 1 − 0.95^{1/20} = 0.00256, barely larger. Bonferroni is
   conservative, but it needs no assumption about how the tests depend on one another.

5. **Build.** Rerun chapter 2's experiment with stack randomization turned off, more runs per setting, and a
   permutation test: does environment size move the time on this machine?

   *Solution notes.*
   - **Turn ASLR off for the child only.** Give `_time` in `explainer/cs/research/method.py` a flag that prefixes the
     command with `setarch -R`, which sets the ADDR_NO_RANDOMIZE personality for the child alone and needs no root.
     Check it with the `stack_randomization` probe. Here, under `setarch -R`, three runs of the probe printed the
     same address, and growing `PAD` by 16 or 128 bytes moved it down by exactly 16 or 128 bytes. Without it, 20 runs
     give 20 addresses (`stack.json`).
   - **Use 16-byte steps.** With the stack fixed, 128-byte steps leave the address modulo 64 unchanged, so chapter 2's
     grid tests only the 32 positions in a page and never the cache-line offset.
   - **Permutation test.** Keep the interleaved rounds. As the statistic, take the spread of the medians, or the
     one-way F statistic on log times. Shuffle the setting labels within each round (the rounds are blocks, so drift
     cancels), recompute the statistic, say 5,000 times, and report p = (count + 1)/(5,001).
   - **What a good run shows.** If the environment matters, p is small and the medians follow the address: they
     depend on it modulo 64 or 4,096, and repeat with that period, which is the causal check. If it does not, p is
     roughly uniform and the line-offset groups agree.
   - **Our run (on 7 November 2026).** One caveat first. The program ran about 35% slower than when the cache was
     measured (medians 0.186 to 0.213 s against 0.133 to 0.142 s), so the machine was not in the same state. The
     results:

     | Design | Spread of medians | p (spread) | p (F) |
     |---|---|---|---|
     | ASLR off; 33 sizes in 128-byte steps × 15 runs | 10.0% | 0.26 | 0.28 |
     | ASLR off; 64 sizes from 0 to 1,008 bytes in 16-byte steps × 8 runs | 14.4% | 0.52 | 0.99 |
     | ASLR on; the first design repeated | 11.2% | 0.24 | 0.25 |

     In the 16-byte design, the medians of the four cache-line offsets were 0.1909, 0.1908, 0.1931 and 0.1924 s,
     within 1.2% of one another.
   - **Conclusion.** No detectable effect of environment size on this machine, for this kernel, with ASLR off or on.
     That is plausible from the code: at `-O2`, `count` keeps its state in registers (four pushes at entry, none in
     the loop), so the only stack traffic in the hot loop is the return address of each call to `mix`. A kernel with
     hot locals spilled to the stack, or with stores that can alias them in their low twelve bits, is where to look
     next.

6. **★ Research.** Pick one star from chapter 9's map, find its smallest open special case, and settle it.

   *Discussion.* Open by design: the problem asks you to choose an open question and cut it down until it is small
   enough to finish. Each star on the map is open because it has resisted every known method, and the obstacles do not
   vanish in special cases: Part 26's barriers (relativization, natural proofs, algebrization) rule out whole families
   of techniques, so a special case is worth having only if you can say which known obstacle it avoids. Two of the
   series' earlier ★ problems show the shape of a good cut. BB(6) shrinks to single six-state machines whose halting
   is unknown, such as Antihydra (Part 1's ★), whose fate is a Collatz-like question about the parities of
   ⌊3h/2⌋-iterates. Circuit lower bounds shrink to exact minimum circuits for every function of a few inputs (computed
   to four inputs in Part 3's ★, with the last five-input cases closed by SAT solvers) and to the Minimum Circuit Size
   Problem. A good partial answer (1) states the special case precisely, with a parameter that measures its size; (2)
   shows that it is open, from the literature, and that the cases below it are settled, by citation or by computation;
   (3) settles it, or settles a smaller case and says exactly what blocks the next one, which is itself a result; and
   (4) writes it up as chapter 8 asks, with every claim matched to its evidence and the threats to validity stated. A
   search proves a finite statement exactly and can find a counterexample; it never proves the infinite one, so the
   write-up must say which kind of result it is. Where to start in the repository: `goldbach` and `collatz` in
   `explainer/cs/research/method.py` show the pattern of a search that proves a finite statement and keeps the records
   that show where a proof would have to work hardest; Part 26's SAT solver is the tool for finite combinatorial
   cases; and Part 54's kernel is the place to check a proof once you have one.

## 习题与解答

1. **没有效应，却有离散。** 33 种设置，每种运行 5 次，而且并没有真实的效应：说明为什么 33 个中位数的离散度随设置的数目增大，并估计每种设置需要
   运行多少次才能使它降到 2% 以下。

   *解答。* 没有效应时，33 个中位数是从同一个分布中独立抽取的：即 5 次运行的中位数的分布，设其标准差为 s。离散度是它们的极差除以最小值。k 个
   独立正态值的极差的期望是 d(k)·s，其中 d(2) = 1.13，d(5) = 2.33，d(33) = 4.16。它无界地增长，大约像 2√(2 ln k)，因为每多一种设置就多一次
   出现极端值的机会。所以即使没有任何一种设置真的不同，离散度也随设置的数目增大。用第 2 章的数据：环境变量为空的 45 次运行的中位数是 0.1391 秒，
   从中抽取的 5 次运行的中位数的标准差 s = 3.1 毫秒。由此预测离散度为 4.16 × 3.1 / 139 ≈ 9.5%，接近第 2 章 4000 次纯噪声实验的典型值 9.9%。
   只有两种设置时，典型离散度只有 1.5%。如果 s 随每种设置的运行次数 r 按 1/√r 下降，要降到 2% 以下需要 r ≈ 5 × (9.9 / 2)² ≈ 120。直接对这些
   运行重抽样，得到的答案更小：30 次时典型离散度为 2.3%，35 次时 2.0%，40 次时 1.9%（第 95 百分位为 2.9%），所以每种设置大约 40 次。这条规则
   高估了，因为 5 次运行的中位数仍会被这批运行的右侧长尾（最慢的达 0.177 秒）拉动，而 40 次的中位数不理会它。重抽样只能再现这 45 次运行恰好
   显示出的尾部。33 × 40 次、每次约 0.14 秒，整个实验大约三分钟。更好的做法是用检验而不是极差来比较各种设置（第 5 题）。

2. **几何平均。** 证明加速比的几何平均与参考机器无关，并构造两个程序，使比值的算术平均依次偏向每一台机器。

   *解答。* 记 G(a) = (∏ aᵢ)^{1/n}。G 是可乘的：G(aᵢbᵢ) = G(a)G(b)，且 G(1/a) = 1/G(a)。机器 X 相对参考机器 R 的得分是
   G(t_{R,i}/t_{X,i}) = G(t_R)/G(t_X)。因此两个得分之比为 G(t_Y)/G(t_X)，t_R 已经消去：无论选哪台参考机器，排名都一样。对算术平均 A，取第 3 章
   的两个程序：X 用 1 秒和 4 秒，Y 用 2 秒和 2 秒，得分是 t_R/t 的平均（越大越好）。以 X 为参考，X 得 (1 + 1)/2 = 1，Y 得 (1/2 + 2)/2 = 1.25：
   Y “快” 25%。以 Y 为参考，X 得 (2 + 1/2)/2 = 1.25，Y 得 1：X “快” 25%。几何平均在两种参考下都给出 1 和 1（G(1, 4) = 2 = G(2, 2)）。一般地，
   由柯西–施瓦茨不等式，(Σ rᵢ)(Σ 1/rᵢ) ≥ n²，所以 A(r)·A(1/r) ≥ 1，当且仅当所有比值相等时取等号。因此只要比值不全相等，至少有一种归一化方式会
   让另一台机器显得更快；这里两种都会。对于固定的工作量，总时间（5 秒对 4 秒）才是诚实的概括。

3. **中位数的自助法。** 推导中位数的自助法百分位区间，证明它的宽度按 1/√n 下降，并用第 3 章的 30 次运行检验。

   *解答。* 把样本排序，x₍₁₎ ≤ … ≤ x₍ₙ₎。有放回地抽取 n 个值的重抽样，其中位数不超过 x₍ⱼ₎，当且仅当至少 (n + 1)/2 个抽取值落在最小的 j 个值中。
   n 为奇数时，P(m* ≤ x₍ⱼ₎) = P(Bin(n, j/n) ≥ (n + 1)/2)，所以自助分布可以精确算出，无需模拟。n 为偶数时，中位数是中间两个抽取值的平均，实践中
   模拟 B 次重抽样。百分位区间就是这个分布的 2.5% 和 97.5% 分位数。若密度 f 在中位数 m 处连续且为正，样本中位数渐近正态：
   √n(m̂ − m) → N(0, 1/(4f(m)²))。自助分布再现了这个离散程度，所以区间宽度约为 2 × 1.96 / (2f(m)√n) = 1.96/(f(m)√n)，按 1/√n 下降。在 30 次运行上
   检验（中位数 0.904 秒）：自助区间为 0.894 到 0.919 秒，宽 25.0 毫秒。以这些运行的标准差 28.4 毫秒为参数的正态密度，f(m) = 每秒 14.1，预测
   宽度 25.5 毫秒。核密度估计给出 f(m) = 12.3，预测 29.0 毫秒。取前 3、5、10、20、30 次运行，中位数区间的宽度依次为 62、62、41、42、25 毫秒。
   乘以 √n 后为 108、139、131、190、137：大致恒定，但有起伏，因为自助中位数只能取次序统计量（或它们的中点）的值。一个不依赖分布的检验：x₍₁₀₎ 到
   x₍₂₁₎ 覆盖中位数的概率是 1 − 2P(Bin(30, ½) ≤ 9) = 95.7%。它给出 0.894 到 0.920 秒，几乎就是自助法的区间。

4. **二十次比较。** 二十次独立的比较，各以 α = 0.05 检验。推导至少出现一次假阳性的概率，以及使它保持在 5% 以下的 Bonferroni 阈值。

   *解答。* 没有真实效应时，每次检验以 0.95 的概率不报警，独立的检验全都不报警的概率是 0.95²⁰。所以 P(至少一次) = 1 − 0.95²⁰ = 0.642。
   Bonferroni 用的是并集上界：P(A₁ ∪ … ∪ A₂₀) ≤ Σ P(Aᵢ) = 20α′。所以每次比较都以 α′ = 0.05/20 = 0.0025 检验，无论检验之间是否独立，整族的错误率都
   不超过 5%。在独立的假设下，精确的错误率是 1 − 0.9975²⁰ = 0.0488，精确的阈值（Šidák）是 1 − 0.95^{1/20} = 0.00256，只大一点点。Bonferroni
   偏保守，但它不需要对检验之间的相关性作任何假设。

5. **动手。** 关闭栈随机化，每种设置多运行几次，再加一个置换检验，重做第 2 章的实验：在这台机器上，环境的大小会改变运行时间吗？

   *解答要点。*
   - **只对子进程关闭 ASLR。** 给 `explainer/cs/research/method.py` 中的 `_time` 加一个开关，在命令前加上 `setarch -R`。它只为子进程设置
     ADDR_NO_RANDOMIZE，不需要 root 权限。用 `stack_randomization` 探针检查。在这里，用 `setarch -R` 运行三次探针，打印出的地址相同；把 `PAD`
     加长 16 或 128 字节，地址恰好下移 16 或 128 字节。不用它时，20 次运行给出 20 个地址（`stack.json`）。
   - **用 16 字节的步长。** 栈固定以后，128 字节的步长不改变地址模 64 的值，所以第 2 章的网格只检验了页内的 32 个位置，从未检验缓存行内的偏移。
   - **置换检验。** 保留交错的轮次。统计量取各中位数的离散度，或对数时间的单因素 F 统计量。在每一轮之内打乱设置的标签（轮次是区组，漂移因此抵消），
     重新计算统计量，比如 5000 次，报告 p = (计数 + 1)/5001。
   - **好的结果是什么样。** 如果环境有影响，p 会很小，而且中位数跟着地址走：它们取决于地址模 64 或模 4096 的值，并以这个周期重复，这就是因果检验。
     如果没有影响，p 大致均匀分布，各缓存行偏移组的结果一致。
   - **我们的运行（2026 年 11 月 7 日）。** 先说一个保留：程序比测量缓存时慢了约 35%（中位数 0.186 到 0.213 秒，缓存中是 0.133 到 0.142 秒），
     所以机器的状态并不相同。结果如下：

     | 设计 | 中位数的离散度 | p（离散度） | p（F） |
     |---|---|---|---|
     | 关闭 ASLR；33 种大小，步长 128 字节 × 15 次 | 10.0% | 0.26 | 0.28 |
     | 关闭 ASLR；0 到 1008 字节的 64 种大小，步长 16 字节 × 8 次 | 14.4% | 0.52 | 0.99 |
     | 开启 ASLR；重复第一种设计 | 11.2% | 0.24 | 0.25 |

     在 16 字节的设计中，四种缓存行偏移的中位数为 0.1909、0.1908、0.1931 和 0.1924 秒，彼此相差不到 1.2%。
   - **结论。** 在这台机器上、对这个内核，无论 ASLR 开或关，都检测不到环境大小的影响。从代码看这是合理的：在 `-O2` 下，`count` 把状态放在寄存器里
     （入口处四次压栈，循环中没有），所以热循环里唯一的栈访问是每次调用 `mix` 的返回地址。下一步该看的是把热局部变量溢出到栈上的内核，或者带有
     低 12 位可能与它们混叠的存储操作的内核。

6. **★ 研究。** 从第 9 章的地图上挑一颗星，找出它最小的、尚未解决的特殊情形，并解决它。

   *讨论。* 这道题本身就是开放的：它要求你选一个未解决的问题，把它切小，直到小得可以做完。地图上的每颗星之所以未解决，是因为它抵挡住了所有已
   知的方法，而这些障碍在特殊情形中并不会消失：第 26 讲的几道壁垒（相对化、自然证明、代数化）排除了整类的技术，所以一个特殊情形只有在你能说明
   它绕开了哪一道已知障碍时才值得做。本系列前面的两道 ★ 题已经给出了好的切法。BB(6) 可以缩小为一台台停机与否尚不清楚的六状态机器，比如反
   九头蛇（第 1 讲的 ★），它的命运是关于 ⌊3h/2⌋ 迭代奇偶性的一个类似 Collatz 的问题。电路下界可以缩小为少数几个输入的每个函
   数的精确最小电路（第 3 讲的 ★ 算到四个输入，五个输入的最后几种情形由 SAT 求解器解决），以及最小电路规模问题（MCSP）。好的部分结
   果应当：（1）精确地陈述这个特殊情形，并给出衡量其大小的参数；（2）根据文献说明它尚未解决，并通过引用或计算说明比它小的情形都已解决；（3）解
   决它，或者解决一个更小的情形并准确说明是什么挡住了下一个，这本身就是一个结果；（4）按第 8 章的要求写出来，每个论断都对应它的证据，并写明对
   有效性的威胁。搜索能精确地证明一个有限的命题，也能找到反例，但永远证明不了无限的命题，所以文章必须说清楚结果属于哪一种。在本仓库里从哪里开始：
   `explainer/cs/research/method.py` 中的 `goldbach` 和 `collatz` 展示了这种模式：搜索证
   明一个有限的命题，并记录下那些显示证明在哪里最费力的纪录；第 26 讲的 SAT 求解器是处理有限组合情形的工具；有了证明之后，第 54 讲的
   内核是检查它的地方。

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
* **permutation test, Bonferroni correction** — a p-value from reshuffling the labels the null hypothesis says do not
  matter; testing each of k comparisons at α/k to keep the chance of any false alarm under α.
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
