# Computer Science, Built — Part 20: Randomness as a Resource

Part 20 of the [61-part course](../README.md) develops randomized algorithms through proofs, worked visual
examples and reproducible experiments. The instruments are [randomized.py](../../../explainer/cs/algo/randomized.py)
and [job3.py](../../../explainer/cs/algo/job3.py); producers live in `compute.py`, independent references in
`measurements.py`, and regression checks in `tests/test_cs20_randomized.py`.

The opening compares the exact word table with a Count-Min sketch retaining 32 candidate words. For this corpus
and fixed seed, all top-20 words and counts agree. The 18,588-byte figure is the compiled program's global-data
block, including candidates and indices; it is not the Python process footprint. In a separate sweep of 20 fixed
hash multipliers, only 5/20 configurations at the program's shape have the completely exact answer. All true top
words survive among the candidates in those 20 runs. Neither observation is a universal guarantee.

The chapters cover:

- Las Vegas versus bounded-time Monte Carlo algorithms; independent amplification, with false acceptance
  distinguished from a posterior probability of error after acceptance.
- Freivalds' three matrix-vector products and deferred-decisions proof. The theorem requires exact arithmetic.
  The instrument accepts integer matrices, prevents overflow and rejects fractional input. The float64 benchmark
  uses bounded integers with exact intermediates; a full integer product reference checks every timed result.
  The leading FLOP counts at size 2,000 are 16 billion versus 24 million. Wall times are host observations.
- Schwartz–Zippel over a field with independent uniform substitutions, a false identity, a Vandermonde check,
  and Tutte's perfect-matching test. Whole-field sampling gives the coarse degree-n bound n/p. The former
  nonzero-element sampler also admitted this coarse bound through its degree-n/2 Pfaffian; no defect is claimed
  for that original displayed inequality. The teaching API uses odd prime fields. A sentinel byte makes the
  integer file encoding injective; prime-count asymptotics are labeled heuristics, not finite error certificates.
- Karger's contraction and telescoping success lower bound, the ten-cycle's 45 minimum cuts, and Karger–Stein.
  Both graph fixtures have independent deterministic Stoer–Wagner certificates. Success shares are finite trials.
- Fermat and Carmichael numbers; Miller–Rabin's fixed-composite false-acceptance bound. The finite liar inventory
  below 20,000 uses exact trial division. Large generated values are probable primes: 40 screening rounds plus
  an independent 64-round rescreen do not constitute primality certificates.
- Papadimitriou's 2-SAT walk and Schöning's restarted 3-SAT search. Final permitted flips are checked, and attempts
  are counted directly, including initially solved restarts. The experiment uses small uniquely satisfying
  formulas checked exhaustively; it does not identify universally hardest instances or prove a runtime lower bound.
- One versus two random bin choices, finite histograms and asymptotic maximum-load scales.
- Bloom membership with a packed byte array, checked for every inserted word. The familiar false-positive formula
  assumes ideal independent placements and uses an occupancy approximation; the concrete double hash is empirical.
- Reservoir sampling, deterministic Misra–Gries, and insertion-only Count-Min. The standard error theorem is for
  each fixed query with suitable collision control and independent row hashes. It does not automatically certify
  every vocabulary item, a double-hash implementation or the retained top-word candidates.
- The complete Pebble Job execution, separately from processor and cache projections. Every corpus instruction
  is emulated and the entire output is checked. IPC comes from three short passages; cache accesses come from a
  150,000-byte passage. Projected cycles assume that sampled working-set behavior extends to the whole corpus.
- HyperLogLog and KMV. The 1.04/√m expression is a leading standard-error scale, not a confidence interval.
  The six-bit packed register model needs 3 KiB at m=4,096; the actual uint64 NumPy registers need 32 KiB,
  excluding corpus, hash arrays and interpreter. Scalar references check all registers for the displayed runs.
- AMS: a six-arrival signed-counter trace, the exact eight-sign expectation, variance, and median of means.
  Unsquared compatible counters merge linearly; their squared estimates do not simply add.
- MinHash's exact identity for ideal uniform minwise permutations and its affine-hash approximation. One hundred
  independent ideal rows have worst standard error 0.05, not a guaranteed ±0.05 interval. Whole-token shingle IDs
  are collision-free. The reference includes all inverted-index postings, including common shingles, and every
  positive-intersection pair. There are seven pairs with J≥0.2; observed recall is 3/7 at 0.2, 2/2 at 0.5 and
  1/1 at 0.8. The ideal banding curve is smooth and requires independent minwise rows.
- Ramsey's expectation argument and the variable-model local lemma. Moser–Tardos now starts from exactly the
  assignment used in the initial-failure column. Dependency degree is an upper bound. Its expected-work theorem
  is separate from each observed resampling count; exhausting an execution budget does not establish UNSAT.
- Conditional expectations, with a five-edge graph and both branch values at each choice; pairwise-independent
  seed enumeration; RANDU's planes; simulation generators versus cryptographic generators and physical entropy.
- BPP as a decision class, explicit PRG seed/circuit quantifiers, the E-hardness premise of Impagliazzo–Wigderson,
  and the specific integer-PIT lower-bound implication. Bipartite matching in quasi-NC² still has
  quasi-polynomial size. Streaming bounds state their universe, update model and fixed success probability.

## Reproduce measurements and previews

```bash
source /workspace/environment/activate.sh
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 .venv/bin/python -m unittest tests.test_cs20_randomized -v
PYTHONPATH=. OPENBLAS_NUM_THREADS=1 .venv/bin/python -m videos.cs.cs20.compute --force
PYTHONPATH=. .venv/bin/python tools/build.py cs20 -q l
```

The `--force` rebuild matters when replacing older payloads. All 16 producers use schema 2. Payloads preserve
seeds, raw timing samples, the actual platform/NumPy build and queried BLAS thread configuration. Validation runs
after timers stop. Minimum-of-repeated, single-run and arithmetic-mean statistics are identified separately.
The 2,048-bit generation observation has one repetition; smaller generation sizes have three. AMS applies random signs to a retained exact frequency vector; its counter budget excludes that input. The MinHash timed
signature output has a full shape/range check and an independent scalar check of all 100 rows for 32 sampled
paragraphs, not a full independent signature certificate. Candidate band matches and the whole exact similarity
inventory are separate checks. Measurements on a shared host do not isolate a causal hardware improvement.

## Problems with worked arguments

1. **Freivalds with q values.** In exact arithmetic, let each coordinate of r be independent and uniform on q
   distinct field elements. Prove false acceptance ≤1/q for any fixed C≠AB, and show tightness when 0 is available.

   Let D=AB−C and choose dᵢⱼ≠0. Fix every coordinate except rⱼ. The necessary equation
   dᵢⱼrⱼ+Σₖ≠ⱼdᵢₖrₖ=0 has at most one solution in the q-element set. Averaging over the fixed coordinates gives
   the bound. With D having a single nonzero entry, acceptance is exactly rⱼ=0, of probability 1/q. For integer
   choices 0,…,q−1 in a finite field, require distinct residues; otherwise this argument's q-value premise fails.

2. **Near-minimum cuts.** For fixed α≥1 and a graph with positive minimum cut k, show that the number of cuts
   of size at most αk is Oα(n²α). Count an unordered bipartition once.

   Fix such a cut C, put β=2α and t=⌈β⌉. When i>t supervertices remain and C survives, at least ik/2 edges remain.
   Its next-step destruction probability is at most β/i. Contract to t vertices and choose a nontrivial remaining
   bipartition uniformly. The survival lower bound is

   `∏(1−β/i), i=t+1,…,n = Γ(n+1−β) Γ(t+1) / [Γ(t+1−β) Γ(n+1)] = Θα(n^−β)`.

   The final random choice adds the constant factor 1/(2ᵗ⁻¹−1). Distinct output cuts are disjoint outcomes,
   so there can be only Oα(nᵝ). The finitely many n≤t cases can be absorbed into the α-dependent constant.
   For integer β=t the product is 1/C(n,t); the argument can give nᵗ. The noninteger proof here claims an
   α-dependent constant, not an unproved leading constant of one. At α=1 the sharper chapter argument gives C(n,2).

3. **Bloom sizing in the ideal approximation.** Minimize f(k)=(1−exp(−kn/m))ᵏ over positive real k. Write
   p=exp(−kn/m), so log f=−(m/n) log p log(1−p). The symmetric product is maximized at p=1/2; differentiating
   gives a positive derivative before 1/2 and negative after. Thus k=(m/n)ln2 and
   f≈exp(−(m/n)(ln2)²). A target ε gives m≈n log₂(1/ε)/ln2. In a finite implementation choose a feasible
   integer k, round storage to bytes, and check hash behavior. This continuous optimum is not an exact finite
   double-hash false-positive theorem.

4. **Weighted sampling without replacement.** Let all weights wᵢ be positive and uᵢ independent uniform on (0,1).
   Keep the k largest uᵢ^(1/wᵢ). Define Tᵢ=−log(uᵢ)/wᵢ. These are independent exponential clocks with rates wᵢ.
   The first clock is i with probability wᵢ/Σⱼwⱼ. The memoryless property leaves independent exponential clocks
   for the unchosen items after each arrival, so the next item is proportional to remaining weight. This proves
   the ordered sequential sampling law. For k>1, an item's marginal inclusion probability is generally not
   k wᵢ/Σⱼwⱼ. Keep a max-heap of the k smallest times; use stable log computations and define finite-RNG tie rules.

5. **Design sketch: HyperLogLog on Pebble.** Design 256 registers with ranks found by repeated halving. This is
   an unexecuted sketch, not a compiled solution or a measured program.

   Tokenize a word and compute a repeatable integer hash h. Select register h mod 256; let q=⌊h/256⌋ and compute
   one plus the trailing-zero count of q. Preserve the maximum for that register. If h has only 24 effective bits,
   q has only 16: cap the all-zero suffix consistently at rank 17. A rank loop cannot manufacture extra random
   bits. The proposed polynomial hash modulo 16,777,213 is neither uniform 24-bit randomness nor a proved
   independent family. Hash collisions, suffix saturation and correlation therefore need tests.

   Combine registers with the HLL harmonic estimate and the appropriate small-range correction. A fixed-point
   implementation must prove its intermediate bounds and quantify rounding; a floating formula alone does not
   do that. Before reporting accuracy or instructions, compile the complete implementation, compare every
   register against an independent reference, run several seeds and corpora, and retain actual measurements.
   The ideal leading 1.04/√256≈6.5% standard error is a comparison scale, not a guarantee for this hash sketch.

6. **★ Research: general deterministic polynomial identity testing.** Decide whether an arithmetic circuit
   computes the zero formal polynomial in deterministic polynomial time. The general problem remains open.
   Specify the field, coefficient encoding, degree and whether the circuit is given explicitly or as an oracle.
   Kabanets–Impagliazzo's integer-PIT implication supplies a starting point. Restricted circuit classes and
   quasi-polynomial hitting sets do not settle the general question. A successful substitution on 20–40 vertex
   Tutte matrices is an experiment, not a universal deterministic matching construction.

## Selected primary sources and scope

These sources were checked at the abstract/introduction or metadata level for the stated claims; this is not
an independent proof verification or a comprehensive current-record survey.

- [Henzinger, Li, Rao and Wang, deterministic weighted minimum cut (2024)](https://arxiv.org/abs/2401.05627).
- [Fenner, Gurjar and Thierauf, bipartite perfect matching in quasi-NC (2016)](https://arxiv.org/abs/1601.06319).
- [Impagliazzo and Wigderson, E circuit hardness implies P=BPP (1997)](https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/IW97/proc.pdf).
- [Kabanets and Impagliazzo, PIT and circuit lower bounds (2004)](https://www.cs.sfu.ca/~kabanets/Research/poly.html).
- [Kane, Nelson and Woodruff, optimal distinct elements (2010)](https://www.cs.cmu.edu/afs/cs/user/dwoodruf/www/knw10b.pdf):
  insertion-only universe [n], fixed constant success, O(ε⁻²+log n) bits; amplification costs are separate.
- [Campos, Griffiths, Morris and Sahasrabudhe (submitted 2023, revised 2025)](https://arxiv.org/abs/2303.09521):
  a diagonal Ramsey upper-bound base below four.
- [Gupta, Ndiaye, Norin and Wei (submitted 2024, revised August 2026)](https://arxiv.org/abs/2407.19026):
  selected reported upper bound 3.8^(k+o(k)).

Preview evidence belongs to the sequential QA ledger. Sampled layout, decoded motion and speech-signal checks
remain distinct from continuous listening, Chinese speech synthesis and complete native-production approval.
