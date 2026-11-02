# Part 16 · Computing Prices: expansion plan (19.0 → ~57.5 min)

Planning document only; nothing in the repo was changed. Sources read: `CLAUDE.md`; `videos/quant/SYLLABUS.md` §1 and
§6 Part 16 (and Parts 5, 13, 14, 15, 17 for overlap); `READING.md` §1 (numerical-methods spine), §2 (Glasserman map),
§4 Part 16; `videos/ai/LECTURE_GUIDE.md`; every file in `videos/quant/quant16/` (manifest, common, compute, the 12
scenes, README); the cached results in `.cache/quant16/`; `explainer/quant/house/engine.py` (all of it),
`stochvol.py` (`cos_price`, `heston_cf`, `heston_qe`), `trees.py`, `sim.py`; `explainer/quant/viz.py` (`lab_card`,
`lab_run`, `seed_band`, `TrainingReplay`); `explainer/ai/autodiff.py`; the plans `quant5.md` (format, and its MLMC,
importance-sampling and industry items) and `quant8.md`; `videos/quant/quant17/` (deep stopping on the same
max-call, `.cache/quant17/stopping.json`). Probe scripts (not in the repo):
`/tmp/claude-0/-home-user-explainer-videos/e79d9910-3070-5b5d-804d-ed98af9b99fd/scratchpad/q16probe/p1.py … p6.py`
(about 3 CPU-minutes in all, run at `nice 10`, one thread, on a loaded machine).

**Cadence.** Hook + 19 chapters + outro = 21 scenes, **about 57 minutes** (≈ 7,900 spoken words at 139 wpm). A chapter
is 2.6–3.2 min (360–450 words). Every one of the eleven syllabus items gets at least one full chapter; five items get two.

**What Part 16 is not.** Part 5 (plan) builds Brownian motion, Euler/Milstein orders, a first MLMC cost table and
importance sampling as Girsanov; Part 10 has the binomial tree and the early-exercise premium; Part 13 owns Heston's
characteristic function, QE and COS as a *model* tool; Part 15 owns barrier closed forms and the BGK correction;
Part 17 owns differential ML, deep BSDE and deep optimal stopping. Part 16 is the **numerical analysis**: proofs of
the error rates, the algorithms built line by line, every method measured on one scoreboard, and the industry that
runs them. Where Part 5's plan introduces MLMC and IS, Part 16 states and proves the complexity theorem and the
optimal-shift theory, and says "Part 5 showed the idea; here is why it works" in one line.

---

## 1. Current state (`python tools/lecture_length.py quant16`: 19.0 min)

| # | Scene | Min | What it covers, how deep, what is computed |
|---|---|---|---|
| — | `s01_hook` Hook | 1.3 | Title; a 4-row table (MC/ADI/Carr–Madan/COS on one Heston call: error and time from `race`); objectives (7 lines); House card. No history segment, no moving visual. |
| 1 | `s02_mc` | 2.1 | Boyle's estimator as one ladder row; rmse-vs-paths log–log for plain/antithetic/control/Sobol (`mc`: 0.0259, 0.0156, 0.0094, 3.4e-5 at 262,144); IS for K = 160 (se 0.0059 → 0.00059). **No CLT derivation, no running estimate, no optimal-b proof, no antithetic variance formula, no stratification, no IS theory.** Three syllabus-item-2 tricks in 40 s. |
| 2 | `s03_qmc` | 1.4 | 256 random vs Sobol points (static); Asian 64 fixings: pseudo/Sobol/Sobol+bridge spread (0.049/0.0127/0.0016 at 16,384, 31×). **No discrepancy, no Koksma–Hlawka, no construction of Sobol, no randomization, no effective dimension (syllabus item), no PCA.** Note: Sobol without bridge stalls (0.0132 → 0.0127 from 4,096 to 16,384), which the narration does not mention. |
| 3 | `s04_mlmc` | 1.6 | Two-row ladder (telescoping, N_l); cost vs ε (4.4×, 11.5×, 25.7× at ε = 0.04/0.02/0.01); level variances. **No complexity theorem, no proof, no Milstein (β = 2), no replay of the adaptive algorithm.** |
| 4 | `s05_american` | 1.7 | LSM explained on a **schematic** scatter (fake data); the AB upper bound vs inner paths (6.414 → 6.075), LSM 6.061, tree 6.090, PSOR 6.085. **No backward-induction animation on real paths, no exercise boundary, no Snell envelope, no convergence/bias discussion, no many-asset case. Dual stated, not derived.** |
| 5 | `s06_greeks` | 2.2 | Three-ways table (call and digital delta); AAD tape cartoon (static arrows); AAD cost 2.2× vs 7.4× bump (5 inputs). **No derivation of pathwise/LR, no bump bias-variance, no Malliavin, no scaling experiment (the point of AAD), no lab.** |
| 6 | `s07_fd` | 1.7 | θ-scheme ladder; explicit blow-up stated (−7.5 × 10¹⁰); convergence plot; CN gamma ringing vs Rannacher. **No von Neumann derivation on screen (it is problem 4), no grid animation, no LCP chapter (syllabus item 8 lists it), PSOR only quoted.** |
| 7 | `s08_adi` | 1.4 | Splitting ladder; error vs grid (Douglas, CS). **No picture of the sweeps, no stability, no non-uniform-grid demonstration, no surface.** |
| 8 | `s09_fourier` | 1.5 | Carr–Madan formula; COS vs CM table; the race (log–log error vs time). **Lewis (syllabus) absent; no COS derivation; no density reconstruction.** |
| 9 | `s10_hardware` | 1.2 | Four history cards: overnight run, JPMorgan–Maxeler 2011, Chakrabarti et al. 2021, "algorithms first" (COS ≈ 14,000× faster than MC's best). **No GPUs/RNG streams, no QAE mechanism, nothing computed except the speed ratio.** |
| 10 | `s11_house` | 0.8 | Function table; Rule 16; counter 73. |
| — | `s12_outro` | 2.2 | 8-line recap, 3 desk questions, 5 problems, payoffs, references, next part. |

Overall: correct, honest numbers and a good race, but every chapter is a summary (1.2–2.2 min), there is **no 3D, no
live simulation, no lab, no replay, no industry or frontier chapter, no history segment, no firm or crisis file**,
and Lewis, effective dimension, stratification, the LCP, the complexity theorem and Malliavin Greeks are missing.

Bug-level findings in the existing material (fix during implementation):
1. `american.bermudan_tree25 = 6.146` is a 25-step CRR tree, not a Bermudan reference: its discretisation error puts
   it *above* the AB upper bound 6.075. Not shown on screen today; do not use it. Add a proper Bermudan reference
   (`bermudan_ref`, §3 ch 9).
2. The hardware card says "about 7,500 logical qubits". The *Quantum* abstract (Chakrabarti et al. 2021, checked
   this session) says **"8k logical qubits"** and T-depth 54 million. Check the body's table; say "about 8,000"
   unless the table says 7.5k for the specific case quoted.
3. `race`'s Monte Carlo point at 80,000 paths has actual error 0.067 against se 0.032 (2.1 se). Fine statistically,
   but the narration should say the plotted MC error is the standard error, as the code comment does.

---

## 2. Audit

### (a) Syllabus items → chapters (new numbering of §3)

| Item | Now | Plan |
|---|---|---|
| 1 Monte Carlo at 1/√n | ch1, 40 s | ch1 (estimator, CLT, cost), ch2 (random numbers, sample paths) |
| 2 Variance reduction: antithetics, CV, IS | ch1, 80 s | ch3 (antithetic, control, stratified, LHS, moment matching), ch4 (IS theory, optimal shift, cross-entropy) |
| 3 QMC: Sobol, Brownian bridge, effective dimension | ch2, 1.4 min | ch5 (discrepancy, Koksma–Hlawka, digital nets, scrambling), ch6 (bridge, PCA, effective dimension) |
| 4 MLMC | ch3 | ch7 (theorem, proof, Euler vs Milstein, replay, unbiased randomized MLMC) |
| 5 LSM; duality | ch4 | ch8 (LSM on real paths, boundary, convergence), ch9 (duality derived, AB, max-call on five assets) |
| 6 Greeks: bump, pathwise, LR | ch5 part | ch10 (all three derived; bump bias–variance in 3D; Malliavin weights) |
| 7 AAD | ch5 part | ch11 (tape replay, cheap-gradient theorem, scaling experiment, checkpointing) |
| 8 FD: explicit/implicit/CN/Rannacher; American LCP | ch6 | ch12 (θ-schemes, von Neumann, Lax), ch13 (CN ringing, Rannacher, LCP: PSOR and penalty, free boundary in 3D) |
| 9 ADI for Heston | ch7 | ch14 (splitting derived, sweeps animated, non-uniform grids measured, the solution surface) |
| 10 Fourier: Carr–Madan, Lewis, COS | ch8 | ch15 (Carr–Madan and Lewis derived), ch16 (COS derived, density reconstruction live, the race) |
| 11 Hardware; quantum AE | ch9 | ch17 (industry: overnight run, GPUs, RNG streams, AAD at banks, FPGAs, STAC-A2, SIMM/FRTB), ch18 (QAE built and simulated; resource estimates) |
| (standard) frontier | — | ch19 (2023–2026: signature stopping, RQMC median-of-means, COS term bounds, Chebyshev/tensor pricers, quantum QSP) |

### (b) Textbook sections → chapter

Chapter titles of Glasserman (2003) confirmed this session against a library catalogue record (9 chapters + appendix);
section numbers below are from memory and marked *(verify)* where they matter. Andersen–Piterbarg vol. I: Part I order
(arbitrage theory, **FD methods, MC methods**, rates fundamentals, instruments) confirmed from a retailer listing;
chapter numbers 2–3 *(verify)*. Savine: ch. 13 "Check-Pointing and Calibration" confirmed (British Library listing);
other chapter numbers *(verify)*. Duffy, Seydel and Oosterlee–Grzelak are mapped by topic; chapter numbers *(verify)*.

| Book · section | Chapter / elsewhere |
|---|---|
| Glasserman 1 Foundations (principles, efficiency = variance × work, Hammersley–Handscomb) | 1 |
| Glasserman 2 Random numbers and random variables (LCGs, combined generators; inverse transform, acceptance–rejection; normals: Box–Muller, Marsaglia polar, Beasley–Springer–Moro; Cholesky) | 2 |
| Glasserman 3 Sample paths: 3.1 BM (random walk, **Brownian bridge, PCA**), 3.2 GBM, 3.3–3.4 Gaussian and square-root short rates, 3.5 jumps, 3.6–3.7 HJM/LMM | 2, 6; 3.3–3.4 → Part 19 (CIR exact also Part 5); 3.5 → Parts 5, 13; 3.6–3.7 → Part 19 |
| Glasserman 4 Variance reduction: 4.1 control variates, 4.2 antithetic, 4.3 stratified, 4.4 Latin hypercube, 4.5 moment matching, 4.6 importance sampling *(verify numbering)* | 3, 4 |
| Glasserman 5 QMC: discrepancy and Koksma–Hlawka; Van der Corput, Halton, Faure, Sobol, Niederreiter nets; lattice rules; randomized QMC; finance applications and effective dimension | 5, 6 (lattice rules named, one line) |
| Glasserman 6 Discretization: Euler, second-order schemes, extensions, **extremes and barrier crossings**, changing variables | Part 5 (orders); 7 (MLMC uses them); barrier crossings → Part 15 (BGK) |
| Glasserman 7 Sensitivities: finite differences, pathwise, likelihood ratio | 10 (and AAD in 11) |
| Glasserman 8 American options: parametric, **random trees**, state-space partitioning, **stochastic mesh**, regression, **duality** | 8, 9 (random tree and mesh: one card in 9) |
| Glasserman 9 Risk management (VaR by delta–gamma, IS for tails, credit) | Part 40 (one forward line in ch4) |
| Savine Part I (modern/parallel C++, thread pools) | 17 (what parallel simulation needs: independent streams, no shared state) |
| Savine Part II (simulation library: models, products, serial and parallel implementation) | 1–2, 17; the House engine is the miniature |
| Savine Part III (manual adjoints, AAD tape, memory, **check-pointing (ch. 13)**, multiple differentiation, expression templates) | 11 |
| Andersen–Piterbarg I, FD chapter (θ-schemes, stability, non-uniform grids, boundary conditions, ADI/splitting) | 12, 13, 14 |
| Andersen–Piterbarg I, MC chapter (RNG, QMC, variance reduction, Greeks, American by regression) | 1–11 |
| Duffy: PDE theory; θ-schemes; CN's spurious oscillations and fixes; exponential fitting; free boundaries; ADI and splitting; Soviet splitting (Yanenko) | 12, 13 (exponential fitting: one line in 13), 14 |
| Seydel: random numbers; MC for SDEs; FD for standard options; **finite elements**; exotic options; American as free boundary | 2, 1, 12–13; finite elements → **README note** ("not used by desks for vanillas; named in ch12") |
| Oosterlee–Grzelak: COS method chapter; Monte Carlo for SDEs (QE, Heston) chapter | 16 (COS derived); QE → Part 13 |
| Hull OFOD "Numerical procedures" chapter (trees, MC, FD) | 1, 12 (Part 10 holds trees) |

### (c) Papers on the Part 16 list in READING.md

| Paper | Now | Plan |
|---|---|---|
| Crank–Nicolson 1947 | on screen | ch12 card; hook timeline |
| Boyle 1977 | on screen | ch1 card; hook timeline |
| Schwartz 1977 (warrants, FD) | **absent** | ch12 history line ("first FD option pricer in finance") |
| Brennan–Schwartz 1978 | **absent** (engine docstring says "1977") | ch13 (LCP history; note the docstring year) |
| Rannacher 1984 | on screen | ch13 |
| Craig–Sneyd 1988 | on screen | ch14 |
| Paskov–Traub 1995 | **absent** | ch6 card (CMO, 360 dimensions; QMC beat MC on a Goldman Sachs CMO) |
| Broadie–Glasserman 1996 | on screen | ch10 |
| Caflisch–Morokoff–Owen 1997 | on screen | ch6 (effective dimension defined) |
| Fournié et al. 1999 | **absent** | ch10 (Malliavin weight for the digital) |
| Carr–Madan 1999 | on screen | ch15 |
| Longstaff–Schwartz 2001 | on screen | ch8 |
| Tsitsiklis–Van Roy 2001 | **absent** | ch8 (regress the value, not the cash flow: the high-biased variant, measured) |
| Lewis 2001 | **absent** | ch15 (derived and computed: agrees with COS to 8 × 10⁻¹³) |
| Rogers 2002; Haugh–Kogan 2004 | on screen | ch9 derivation |
| Andersen–Broadie 2004 | on screen | ch9 |
| Giles–Glasserman 2006 | on screen | ch11 |
| Giles 2008 | on screen | ch7 |
| Fang–Oosterlee 2008 | on screen | ch16 |
| Joe–Kuo 2008 | **absent** | ch5 (direction numbers: what scipy's Sobol uses) |
| in 't Hout–Foulon 2010 | on screen | ch14 |
| Capriotti 2011 | **absent** | ch11 card |
| Rebentrost–Gupt–Bromley 2018 | **absent** | ch18 |
| Stamatopoulos et al. 2020 | **absent** | ch18 |
| Chakrabarti et al. 2021 | on screen | ch18 (with the corrected 8k figure) |

Proposed additions to READING.md Part 16 (classic): Metropolis–Ulam (1949) "The Monte Carlo method" *JASA*; Hammersley–
Handscomb (1964) *Monte Carlo Methods*; Sobol' (1967) *USSR Comp. Math. & Math. Phys.*; Halton (1960); Koksma (1942)/
Hlawka (1961); Courant–Friedrichs–Lewy (1928); Lax–Richtmyer (1956) "Survey of the stability of linear finite difference
equations" *CPAM*; Cryer (1971) "The solution of a quadratic programming problem using systematic overrelaxation" *SIAM
J. Control*; Peaceman–Rachford (1955); Douglas–Rachford (1956); Kemna–Vorst (1990) "A pricing method for options based
on average asset values" *J. Banking & Finance*; Owen (1995/1997) scrambled nets; Broadie–Glasserman (1997) "Pricing
American-style securities using simulation" *JEDC* (random tree); Broadie–Glasserman (2004) stochastic mesh *J. Comp.
Finance*; Glasserman–Heidelberger–Shahabuddin (1999) "Asymptotically optimal importance sampling and stratification
for pricing path-dependent options" *Math. Finance*; Clément–Lamberton–Protter (2002) "An analysis of a least squares
regression method for American option pricing" *Finance & Stochastics*; Forsyth–Vetzal (2002) "Quadratic convergence for
valuing American options using a penalty method" *SIAM J. Sci. Comput.*; Griewank–Walther (2008) *Evaluating
Derivatives* (2nd ed., SIAM); Giles (2008b) "Improved multilevel Monte Carlo convergence using the Milstein scheme"
*MCQMC 2006*; Rhee–Glynn (2015) "Unbiased estimation with square root convergence for SDE models" *Operations Research*;
Giles (2015) "Multilevel Monte Carlo methods" *Acta Numerica*; Salmon–Moraes–Dror–Shaw (2011) "Parallel random numbers:
as easy as 1, 2, 3" *SC'11* (D. E. Shaw Research; Philox); Montanaro (2015) "Quantum speedup of Monte Carlo methods"
*Proc. R. Soc. A*; Suzuki et al. (2020) "Amplitude estimation without phase estimation" *Quantum Inf. Process.*;
Gaß–Glau–Mahlstedt–Mair (2018) "Chebyshev interpolation for parametric option pricing" *Finance & Stochastics*;
Glau–Kressner–Statti (2020) "Low-rank tensor approximation for Chebyshev interpolation in parametric option pricing"
*SIAM J. Financial Math.* Frontier (2023–2026) in §4. Venues from memory are *(verify)* for the implementer unless
listed in §4 as checked.

---

## 3. The chapter list (21 scenes, about 57 min)

Conventions as in `quant5.md`: **Visual** is the signature picture, built before the formula; **Live** is a simulation
drawn as it runs (ValueTracker or step-by-step `play`); **Lab** is `lab_card` (≤ 12 lines of real House code, file and
line range given) + `lab_run` printing cached results; **Replay** is `TrainingReplay` or a ValueTracker scrub with seeds
as `seed_band`; **Compute** names the `compute.py` item and its CPU estimate (one core). "Planning run" numbers come from
the probes and must be recomputed by `compute.py`; narration branches where a result could go either way. Existing
modules and Scene classes are kept for kept chapters (caches are keyed by them); new chapters get new modules, ordered by
the manifest.

### H · Hook: "One price, many machines" (2.8 min) · `s01_hook` (deepened)
- Goal: the puzzle (same price, costs 10⁴ apart), the era, the map.
- Beats: (1) **Live race teaser**: four "engines" start together on one Heston call; each draws its error-vs-time trace
  in real time-scaled playback (ValueTracker over log time): COS reaches 10⁻⁶ before MC has drawn its first dot. Keep the
  existing table as the end frame. (2) **How we got here (≈60 s)**, timeline lit: 1947 Crank–Nicolson; 1949
  Metropolis–Ulam name "Monte Carlo"; 1967 Sobol; 1977 Boyle (MC) and Schwartz (FD) in the same JFE year; 1979 trees;
  1996 Broadie–Glasserman; 1999 Carr–Madan; 2001 Longstaff–Schwartz; 2006 smoking adjoints; 2008 MLMC and COS; 2011
  JPMorgan's FPGAs (firm, blue); 2021 quantum threshold; 2024 QSP. (3) Objectives (11 items + industry + frontier).
  (4) House card: the pricing engine; Rule 16 previewed.
- Pause-and-predict: "Ten times the accuracy from Monte Carlo costs how many times the work?" (100.)
- Compute: `race` (exists, 0.5 min). Timeline: append 1947, 1949, 2011 (append-only, `explainer/quant/__init__.py`).

### 1 · Monte Carlo: an average with an error bar (2.8) · item 1 · `s02_mc` (reshaped: the rate only)
- Goal: the estimator, its error proved, the cost of a digit; "efficiency = 1/(variance × work)".
- Beats: **Live**: GBM paths shoot out one batch at a time (path_fan); each terminal payoff drops as a dot onto a
  running-mean plot; around the running mean a ±1.96 se **funnel** narrows like 1/√n (3 seeds as thin lines, the true
  price 10.4506 dashed). The funnel's width is read off at n = 10², 10⁴, 10⁶. Then the ladder. Then "one cent costs 3.5
  million paths". Then the efficiency card: two estimators, one twice as noisy and four times cheaper, which wins.
- Derivation:
  - $V = e^{-rT}\mathbb E^Q f(S_T)$ (Part 9: the price is an expectation).
  - $\hat V_n = \frac1n\sum_i Y_i \to V$ a.s. (strong law; $Y_i$ i.i.d., $\mathbb E|Y|<\infty$).
  - $\sqrt n(\hat V_n - V) \Rightarrow N(0,\sigma_Y^2)$ (CLT, $\sigma_Y^2<\infty$), so $\hat V_n \pm 1.96\,s_n/\sqrt n$ is a
    95% interval (Slutsky: $s_n\to\sigma_Y$).
  - $n(\varepsilon) = (1.96\,\sigma_Y/\varepsilon)^2$ (solve for the half-width); dimension does not appear.
  - Work-normalised error: with cost $c$ per sample and budget $C$, error $\approx \sigma_Y\sqrt{c/C}$, so compare
    estimators by $\sigma_Y^2 c$ (Hammersley–Handscomb; Glasserman 1.1).
  - Berry–Esseen (one line): the interval's coverage error is $O(\mathbb E|Y|^3/(\sigma^3\sqrt n))$, which is why deep
    out-of-the-money estimates need care (link to ch4).
- Experiment: `mc` (exists: plain rmse 0.580 → 0.0259 over 1,024…262,144); `mc_live` (new: running means and se for 3
  seeds to n = 10⁶, stored at 200 log-spaced checkpoints; check coverage of the 95% interval over 1,000 seeds at n = 10⁴:
  expected ≈ 0.95, computed).
- Pause-and-predict: "Two estimators: A has twice B's standard deviation and costs a quarter as much per path. Which?"
  (Equal: σ²c is the same.)
- Compute: `mc` (0.5), `mc_live` (0.3).

### 2 · Random numbers and sample paths (2.7) · item 1 · `s02a_paths` (new)
- Goal: where the uniforms come from, how they become normals and correlated paths; reproducible parallel streams.
- Beats: **Visual**: a uniform u on a vertical axis is mapped through Φ⁻¹ to a normal on the horizontal (inverse
  transform), dots raining and stacking into a bell; then Box–Muller as a 2D picture (radius from −2 log u₁, angle 2πu₂:
  dots sprayed in a disc pattern that becomes an isotropic Gaussian cloud). Then **Cholesky live**: a cloud of
  independent (Z₁, Z₂) is sheared by L into correlation ρ = −0.7 (Heston's), the ellipse rotating. Then three ways to
  build the same Brownian path from the same 64 normals (step-by-step, bridge, PCA) — introduced here, measured in ch6.
  Last, **streams**: numpy's PCG64 (sequential state) vs counter-based Philox (Salmon et al. 2011, D. E. Shaw Research):
  the k-th random number is a pure function of (key, k), so 10,000 GPU threads or a rerun of one trade's paths get the
  same numbers. A grid of "path tiles" each coloured by its (key, counter), recomputed in a different order with
  identical output.
- Derivation: $U\sim U(0,1)\Rightarrow F^{-1}(U)\sim F$ ($P(F^{-1}(U)\le x) = P(U\le F(x)) = F(x)$); Box–Muller: the
  Jacobian of $(r,\phi)\mapsto(x,y)$ gives density $\frac1{2\pi}e^{-r^2/2}r$, and $r^2/2\sim$ Exp(1) $=-\log U_1$;
  $X = \mu + LZ$, $LL^\top = \Sigma$ ⇒ $\operatorname{Cov}X = L\,I\,L^\top$; a random walk path $W_{t_k} = \sum_{j\le k}\sqrt{\Delta t}Z_j$
  is $W = L_{\text{step}}Z$ with $L_{\text{step}}L_{\text{step}}^\top = C$, $C_{ij} = \min(t_i,t_j)$ — any $L$ with
  $LL^\top = C$ gives the same law (the hinge for ch6).
- **Lab 1**: `engine.brownian_bridge` (`explainer/quant/house/engine.py` lines 65–80, 12 lines after trimming the
  docstring): run on `np.eye(8)` columns, print that $LL^\top$ equals $\min(t_i,t_j)$ to 6 × 10⁻¹⁷ (planning run:
  max deviation 5.6 × 10⁻¹⁷ for 64 steps).
- Experiment: `rng` (new): KS statistics of inverse-transform and Box–Muller normals (10⁶); Philox streams reproduced
  out of order (bitwise equal: a check, not a result); vectorised vs per-path Python loop on 10⁵ payoffs (planning run:
  12× under load; recompute, best of 5).
- Pause-and-predict: "Two correlated assets, ρ = 0.9. Cholesky's second row?" ((0.9, √0.19) = (0.9, 0.436).)
- Compute: `rng` (0.2).

### 3 · Variance reduction I: antithetics, control variates, stratification (3.0) · item 2 · `s02b_control` (new)
- Goal: shrink the constant; prove the optimal control coefficient; show a 1,000× control variate.
- Beats: **Visual (the scatter that rotates)**: 2,000 simulated (C, Y) pairs for an arithmetic Asian (Y) against the
  geometric Asian (C, known in closed form, Kemna–Vorst 1990); a regression line rotates from slope 0 to b* while the
  marginal histogram of Y − b(C − EC) on the right **collapses** from a wide bell to a needle (ρ = 0.9996). Then the same
  with the stock as control (ρ small; histogram barely moves: 2.8×). Antithetics: pair each path with its mirror, the
  pair-averages histogram narrows; the derivation shows why only monotone payoffs gain. **Stratification live**: the
  unit interval split into 16 strata, one uniform per stratum drops in; the estimator's histogram over 500 repeats is
  drawn beside plain MC's; Latin hypercube in 2D (one point per row and column) and moment matching as one-line cards.
- Derivation:
  - $\operatorname{Var}(Y - b(C-\mathbb EC)) = \sigma_Y^2 - 2b\sigma_{YC} + b^2\sigma_C^2$ (expand), minimised at
    $b^* = \sigma_{YC}/\sigma_C^2$ (set the derivative to 0), giving $\sigma_Y^2(1-\rho^2)$ (substitute).
  - Estimating $b^*$ from the same sample adds $O(1/n)$ bias (a regression estimator; negligible for $n\gg1$).
  - Antithetic: $\operatorname{Var}\frac{Y+Y'}2 = \frac{\sigma^2}{2}(1+\rho)$, $\rho = \operatorname{corr}(f(Z),f(-Z))$;
    for monotone $f$, $\rho\le0$ (Chebyshev's association inequality), so at equal work the gain is $1/(1+\rho)$.
  - Stratified with proportional allocation: $\operatorname{Var} = \frac1n\sum_k p_k\sigma_k^2 \le \frac1n\sigma^2$
    (law of total variance drops the between-strata term $\sum p_k(\mu_k-\mu)^2$).
- **Lab 2**: `engine.mc_call` control branch (lines 44–50, 7 lines) and antithetic branch (lines 31–36): run → prints
  the cached rmse at 262,144 (plain 0.0259, antithetic 0.0156, control 0.0094).
- Experiment: `mc` (exists); `control` (new): Kemna–Vorst control on 64 fixings, 20,000 paths × 5 seeds. **Planning run:
  ρ = 0.9996, variance ratio ≈ 1,340 (geometric control) vs 2.8 (stock control); antithetic ρ = −0.50 for the ATM
  call** (so 2× at equal work); stratified (16 and 256 strata on the terminal normal) and LHS ratios (computed).
- Pause-and-predict: "Antithetics for a straddle |S_T − K|?" (Little or none: the payoff is not monotone; ρ ≈ +.)
- Compute: `control` (0.5).

### 4 · Variance reduction II: importance sampling and rare events (2.8) · item 2 · `s02c_importance` (new)
- Goal: the theory of the shift (zero-variance measure, optimal exponential tilt), how to find it by learning, how it
  fails.
- Beats: **Visual**: the N(0,1) density with the payoff region x > 2.2 shaded (1.4% of mass); a ValueTracker slides the
  sampling density's centre θ from 0 to 7; underneath, the **variance-ratio curve** draws itself (rises to ≈ 130× near
  θ ≈ 2.75, falls back past 5, below 1 beyond, computed), and a weights histogram on the right goes from
  "almost all zero" to "well spread" to "a few giant weights" (effective sample size printed). Then **Replay (learning the
  measure)**: cross-entropy iterations θ₀ = 0 → θ₁ → … drawn on the same curve as hops, 5 seeds as a band — the
  estimator "trains" its sampling law in two steps. Card: path-dependent IS (Glasserman–Heidelberger–Shahabuddin
  1999: the optimal drift path from a saddlepoint, plus stratification along it). Forward: Part 40 tail risk; Part 5
  did the Girsanov version.
- Derivation:
  - $\mathbb E_p f = \mathbb E_q[f\,p/q]$ (change of measure, $q>0$ where $fp\ne0$).
  - $\operatorname{Var}_q = \mathbb E_p[f^2p/q] - (\mathbb E_pf)^2$, minimised by $q^*\propto|f|p$ (Cauchy–Schwarz);
    zero variance if $f\ge0$ — useless directly (needs the answer) but it says *where* to sample.
  - Normal shift: $p/q = e^{-\theta z+\theta^2/2}$ (ratio of Gaussians); second moment
    $m(\theta) = \mathbb E[f(Z)^2e^{-\theta Z+\theta^2/2}]$ is convex in θ (log-convexity), so the optimum is unique.
  - Cross-entropy: $\theta_{k+1} = \arg\max_\theta\mathbb E_{\theta_k}[f\,w\log q_\theta] = \frac{\mathbb E_{\theta_k}[fwZ]}{\mathbb E_{\theta_k}[fw]}$
    (for a normal family the maximiser is a weighted mean).
  - Weight degeneracy: ESS $=(\sum w)^2/\sum w^2$; for a shift θ, $\mathbb E_q w^2 = e^{\theta^2}$, so ESS/n ≈ $e^{-\theta^2}$
    for a payoff-blind check (the "too far" failure).
- Experiment: `mc.deep` (exists: se 0.0059 → 0.00059); `is_sweep` (new): 400,000 normals, θ ∈ [0, 7]. **Planning run:
  strike-centred θ = 2.20 (the House's choice) gives ≈ 103×; the minimum is near θ ≈ 2.75 at ≈ 133×; θ = 5 gives 4.6×;
  cross-entropy reaches θ = 2.80 after one step and 2.86 after two** (CE minimises a KL criterion, not the variance, so
  it lands slightly past the variance optimum: say so).
- Pause-and-predict: "Shift the normal far beyond the strike. What happens to the error?" (It grows: few huge weights.)
- Compute: `is_sweep` (0.3).

### 5 · Quasi-Monte Carlo: filling space evenly (3.0) · item 3 · `s03_qmc` (deepened: the points)
- Goal: discrepancy, Koksma–Hlawka, how Sobol points are built, and randomisation for error bars.
- Beats: **Live (the net property)**: Sobol points appear one by one in the unit square; at n = 16, 64, 256 the square is
  re-tiled by every dyadic box shape of area 1/n (1×16, 2×8, 4×4, 8×2, 16×1 …) and each box lights green when it holds
  exactly one point — all light (a (0, m, 2)-net); random points leave red empties and doubles. **Van der Corput built
  digit by digit**: n in binary, bits reversed after the point (1 → 0.1, 2 → 0.01, 3 → 0.11 …), each new point landing in
  the largest gap. Then the star-discrepancy plot (log–log) for random (slope −½), Halton and Sobol (≈ −1), and the
  **Halton failure**: the 2D projection of Halton dimensions 29 and 30 at n = 1,000 (stripes), against Sobol's with
  Joe–Kuo (2008) direction numbers. Then Owen scrambling: 10 scrambled copies give independent unbiased estimates, so QMC
  gets an error bar. Keep the existing 256-point comparison as the opener.
- Derivation:
  - $D_n^* = \sup_{a\in[0,1]^d}\big|\frac{\#\{x_i\in[0,a)\}}{n} - \prod a_j\big|$ (definition).
  - Koksma–Hlawka: $\big|\frac1n\sum f(x_i) - \int f\big| \le V_{HK}(f)\,D_n^*$ (Hardy–Krause variation × discrepancy;
    stated, the 1D proof by integration by parts: $\frac1n\sum f(x_i)-\int f = -\int_0^1 (F_n(x)-x)f'(x)dx$).
  - Sobol/Halton: $D_n^* = O((\log n)^d/n)$, against $O(\sqrt{\log\log n/n})$ for random (law of the iterated
    logarithm) — better for fixed $d$, but $(\log n)^d/n$ only wins once $n \gg e^d$ (why dimension hurts).
  - Van der Corput: $\phi_2(n) = \sum_k a_k2^{-k-1}$ for $n = \sum_k a_k2^k$ (radical inverse).
  - Scrambled nets: $\mathbb E\hat I = I$, and for smooth $f$, $\operatorname{Var} = O(n^{-3}(\log n)^{d-1})$ (Owen 1997;
    stated).
- Experiment: `qmc` (exists, the 256 points); `discrepancy` (new): L2-star discrepancy (Warnock's closed form) for
  random/Halton/Sobol at n = 2⁶ … 2¹⁴ in d = 2 and d = 16; the box-occupancy counts for the animation; Halton (29, 30)
  projection.
- Pause-and-predict: "Drop the first Sobol point (the origin) to avoid Φ⁻¹(0) = −∞. Harmless?" (No: it breaks the net
  property and the rate; Owen's "On dropping the first Sobol' point" — README reading guide *(verify year/venue)*.)
- Compute: `discrepancy` (0.3).

### 6 · QMC on paths: the Brownian bridge and effective dimension (2.8) · item 3 · `s03a_bridge` (new; reuses `qmc`)
- Goal: why ordering the coordinates matters; effective dimension measured; Paskov–Traub's CMO.
- Beats: **Visual (3D)**: a `ThreeDScene` "coordinate staircase": axes (time t, coordinate index k, contribution); for
  step-by-step construction every coordinate adds a small equal ramp (a flat field of 64 short columns); for the bridge
  the first column (W_T) is a tower, the next two (midpoint, quarter points) shorter, then a fast decay; PCA steeper
  still. The camera swings from front to side to show the decay profiles. Then the **bridge drawn live**: the same path
  crystallising from endpoint to midpoints (8, 16, 64 points), the Sobol coordinate number written on each new point.
  Then the existing spread plot (pseudo/Sobol/Sobol+bridge) plus **PCA** as a fourth line, and the variance-captured bars.
  Card: Paskov and Traub (1995) priced a 360-dimensional CMO with Sobol/Halton faster than MC, which started the field;
  Caflisch–Morokoff–Owen (1997) explained it by effective dimension.
- Derivation:
  - ANOVA: $f = \sum_{u\subseteq\{1..d\}}f_u$, $\sigma^2 = \sum_u\sigma_u^2$ (orthogonal decomposition).
  - Truncation dimension $d_T$: smallest $s$ with $\sum_{u\subseteq\{1..s\}}\sigma_u^2\ge0.99\sigma^2$; superposition
    dimension $d_S$: smallest $s$ with $\sum_{|u|\le s}\sigma_u^2\ge0.99\sigma^2$ (definitions, CMO 1997).
  - For a linear functional $a^\top W = a^\top LZ$: variance captured by the first $k$ coordinates is
    $\sum_{j\le k}(a^\top L)_j^2/\|a^\top L\|^2$ (each $Z_j$ independent): the bar heights of the 3D picture.
  - PCA: $L = V\Lambda^{1/2}$ from $C = V\Lambda V^\top$, $\lambda_j = \frac{T^2}{(j-\frac12)^2\pi^2}$ in the
    continuous limit (Karhunen–Loève), so it front-loads the most variance among all $L$ (Eckart–Young).
- Experiment: `effdim` (new). **Planning run, average of W over 64 fixings: share of variance in the first coordinate
  — step 4.6%, bridge 75.6%, PCA 98.6%; first four — 17.5%, 98.5%, 100%.** Add PCA to the `qmc` spread (64 fixings,
  20 scrambles; expected near the bridge, computed). Caveat on screen: PCA costs O(d²) per path and needs a fixed grid;
  desks use the bridge (QuantLib's Sobol-Brownian generator; ch17).
- Pause-and-predict: "Feed Sobol points step by step into a 64-step path. Why did the spread stall between 4,096 and
  16,384?" (The late, poorly distributed coordinates carry 95% of the variance; existing `qmc`: 0.0132 → 0.0127.)
- Compute: `effdim` (0.5).

### 7 · Multilevel Monte Carlo (3.2) · item 4 · `s04_mlmc` (deepened)
- Goal: the complexity theorem with proof; β = 1 vs β = 2 measured; the adaptive algorithm replayed.
- Beats: **Visual (the telescope)**: a stack of horizontal bars, one per level, width ∝ N_l (paths) and height ∝ C_l
  (cost per path); fine paths (gold) and coarse paths (grey) sharing Brownian increments are drawn superimposed for one
  sample at levels 1–4, the difference P_l − P_{l−1} shown as a shrinking red sliver. **Replay (the estimator
  learning its levels)**: the adaptive loop of `engine.mlmc` scrubbed iteration by iteration: pilot samples per level,
  V_l dots appearing on a log plot, N_l bars growing to the optimum, a new level added when the bias test fails, until it
  passes (10 levels at ε = 0.01); 4 seeds as a band on the total-cost readout. Then the existing cost-vs-ε plot, now with
  a **Milstein** line, and the level-variance plot with two slopes.
- Derivation:
  - $\mathbb E P_L = \mathbb E P_0 + \sum_{l=1}^L\mathbb E(P_l - P_{l-1})$ (telescoping); estimate each term
    independently with $N_l$ samples (unbiased for $\mathbb E P_L$).
  - MSE $= \sum_l V_l/N_l + (\mathbb E P_L - \mathbb E P)^2$ (variance + bias²); split $\varepsilon^2/2$ each.
  - Minimise $\sum N_lC_l$ s.t. $\sum V_l/N_l = \varepsilon^2/2$ (Lagrange): $N_l = 2\varepsilon^{-2}\sqrt{V_l/C_l}\sum_k\sqrt{V_kC_k}$,
    total cost $2\varepsilon^{-2}(\sum_l\sqrt{V_lC_l})^2$.
  - With $|\mathbb E(P_l-P)|\le c_1M^{-\alpha l}$, $V_l\le c_2M^{-\beta l}$, $C_l\le c_3M^{\gamma l}$ (assumptions):
    $\sum\sqrt{V_lC_l}\sim\sum M^{(\gamma-\beta)l/2}$, a geometric series, giving cost $O(\varepsilon^{-2})$ if $\beta>\gamma$,
    $O(\varepsilon^{-2}(\log\varepsilon)^2)$ if $\beta=\gamma$, $O(\varepsilon^{-2-(\gamma-\beta)/\alpha})$ if $\beta<\gamma$ (Giles's theorem).
  - Euler: $\alpha = 1$, $\beta = 1$ (strong order ½ squared, Lipschitz payoff), $\gamma = 1$ ⇒ $\varepsilon^{-2}(\log\varepsilon)^2$;
    Milstein: $\beta = 2 > \gamma$ ⇒ $\varepsilon^{-2}$, the cost of one unbiased sample stream. Standard MC: $\varepsilon^{-3}$.
  - Randomised MLMC (Rhee–Glynn 2015): pick the level at random with probabilities $p_l$, weight by $1/p_l$; unbiased for
    $\mathbb E P$ itself when $\beta>\gamma$ (one card).
- **Lab 3**: `engine._mlmc_level` (lines 99–112, 12 lines: the fine loop and `dW.reshape(n, nc, M).sum(axis=2)`, the
  coupling): run → prints level variances V₀…V₉ from cache (161 → 0.0086 at ε = 0.01).
- Experiment: `mlmc` (exists: 4.4×, 11.5×, 25.7×; levels 8/9/10); `mlmc_trace` (new: the iteration log of `mlmc` at
  ε = 0.01 for 4 seeds — requires a `trace=True` option, see §6); `mlmc_milstein` (new). **Planning run, European call
  under GBM: level variances fall with β = 0.99 (Euler: 2.4 → 0.022 over levels 1–8) and β = 1.96 (Milstein: 0.16 →
  1.4 × 10⁻⁵).** Cost vs ε for Milstein-MLMC on the same Asian (expected flatter ε²·cost, computed and branched).
- Pause-and-predict: "Milstein makes V_l fall four times per level instead of two. What happens to ε²·cost as ε → 0?"
  (It stops growing.)
- Compute: `mlmc` (2), `mlmc_trace` (1), `mlmc_milstein` (3).

### 8 · American options I: Longstaff–Schwartz on real paths (3.0) · item 5 · `s05_american` (deepened; schematic replaced)
- Goal: dynamic programming by regression, run on screen; the exercise boundary emerging; why it is a lower bound and
  how biased it is.
- Beats: **Live (backward induction as a replay)**: 2,000 of the actual `lsm_put` paths fanned over 25 dates. A vertical
  cursor walks **backward** from T: at each date the in-the-money points (S_t, realised discounted cash flow) appear as
  a scatter (real data, replacing the schematic), the cubic fit draws itself, the crossing of the fit with K − S marks
  that date's exercise boundary point, and the paths that now exercise turn gold from that date on. The boundary
  traces a curve back to t = 0; the 2,000-step tree's continuous boundary (`trees.crr(..., boundary=True)`) is drawn
  dashed for comparison. **Replay over the basis**: degree 1 → 5 and fit paths 10³ → 10⁵; out-of-sample lower bound with
  ±2 se, 5 seeds as a band, the duality bound of ch9 as the ceiling.
- Derivation:
  - Snell envelope: $V_{t_N} = h_{t_N}$, $V_{t_i} = \max\big(h_{t_i}, \mathbb E[e^{-r\Delta t}V_{t_{i+1}}\mid S_{t_i}]\big)$
    (dynamic programming; Part 8's optimal stopping).
  - $\mathbb E[Y\mid S] = \arg\min_{g}\mathbb E(Y-g(S))^2$ (conditional expectation is the $L^2$ projection), so regress
    $Y$ on $\psi_1(S),\dots,\psi_K(S)$: $\hat\beta = (\Psi^\top\Psi)^{-1}\Psi^\top Y$ (least squares).
  - LS regress the **realised cash flow along the policy** (not the estimated value — Tsitsiklis–Van Roy's choice, which
    is high-biased); the regression only *decides*, the payoff is realised (why LS is less biased).
  - Lower bound: any stopping rule $\tau$ gives $\mathbb E[e^{-r\tau}h_\tau]\le V_0$ (definition of the sup); evaluate it on
    **independent** paths to remove foresight bias.
  - Convergence (Clément–Lamberton–Protter 2002): as $K\to\infty$ and then $n\to\infty$, the price converges; the rate
    in $n$ is $1/\sqrt n$ for fixed $K$ (stated).
- Experiment: `american` (exists: LSM 6.061, European 5.574, tree 6.090, PSOR 6.085); `lsm_live` (new): stored
  scatter, fit and boundary for each of 25 dates (2,000 paths for display; the regression on the full 200,000), tree
  boundary; degree × paths grid, 5 seeds; the Tsitsiklis–Van Roy variant's in-sample value (expected above the
  true price; computed and branched).
- Pause-and-predict: "Why regress only on in-the-money paths?" (Out-of-the-money paths never exercise there; including
  them wastes the basis on the wrong region.)
- Compute: `american` (2, exists), `lsm_live` (2).

### 9 · American options II: the dual bound, and five assets (3.0) · item 5 · `s05a_dual` (new; takes the bounds from `s05_american`)
- Goal: derive the duality upper bound; Andersen–Broadie by nested simulation; the method in five dimensions, where
  grids die, compared with Part 17's network.
- Beats: **Live (one outer path)**: a path S_t with its payoff h_t (red) and the martingale π_t built from the LSM policy
  (blue, nested inner simulations shown as tiny fans sprouting at each date); the gap h_t − π_t is drawn, its running
  max ticks up; average over 400 outer paths → the upper bound. Then the existing bound-vs-inner-paths plot, now with a
  **proper Bermudan reference** line between the bounds. Then the **max-call on five assets** (Broadie–Glasserman's
  benchmark; S₀ = K = 100, r = 5%, δ = 10%, σ = 20%, T = 3, 9 dates): the 5D state cannot be gridded (100⁵ nodes); LSM
  with 15 basis functions (sorted prices, squares, payoff); the price bar chart: LSM (this part), deep stopping (Part 17,
  loaded from its cache), and the published bounds. Card: random trees and stochastic mesh (Broadie–Glasserman 1997,
  2004) as the other two classical simulation methods (Glasserman ch. 8).
- Derivation:
  - For any martingale $M$, $M_0 = 0$: $\mathbb E[h_\tau] = \mathbb E[h_\tau - M_\tau]\le\mathbb E\max_t(h_t - M_t)$ (optional
    stopping, then bound the stopped value by the max).
  - So $V_0\le\inf_M\mathbb E\max_t(h_t-M_t)$ (Rogers 2002; Haugh–Kogan 2004), with equality at $M^*$ = the martingale
    part of the Snell envelope (Doob–Meyer: $V = V_0 + M^* - A$, $A$ increasing, $h\le V$).
  - AB: $\pi_{t_{i+1}} = \pi_{t_i} + L_{t_{i+1}} - \mathbb E_{t_i}L_{t_{i+1}}$ with $L$ the policy value, the conditional
    expectation by inner paths; inner noise $\varepsilon$ inflates the bound by $\mathbb E\max(\cdot+\varepsilon)\ge\max\mathbb E$
    (Jensen) — why it falls as the inner paths grow.
  - Duality gap = upper − lower measures the policy's suboptimality (a desk's error bar on an American price).
- **Lab 4**: `engine.andersen_broadie_put` outer loop (lines 248–259, 12 lines): run → prints the four (inner, upper,
  se) rows from cache.
- Experiment: `american.ab` (exists: 6.414/6.146/6.079/6.075); `bermudan_ref` (new: a 2,500-step CRR tree that may
  exercise only on the 25 dates; expected inside [6.061, 6.075], computed and branched; replaces the misleading
  `bermudan_tree25`); `maxcall` (new). **Planning run: LSM lower bound 25.918 ± 0.031 (2,000 fit paths), 26.113 (20,000),
  26.146 ± 0.031 (200,000; 400,000 independent evaluation paths); Part 17's deep stopping 26.107 ± 0.020; the reference
  bounds stored in `house/deep.py` are [26.156, 26.162]** (source of those bounds: verify which paper — Becker et al. 2019
  quote Andersen–Broadie-type bounds; *(verify)*). Narration must branch: on this benchmark classical LSM with a good
  basis is *not* beaten by the network (planning run); say so, and say what the network buys (no hand-made basis).
- Pause-and-predict: "Your upper bound is 0.5 above your lower bound. Is the policy bad, or the inner simulation small?"
  (Rerun with more inner paths: if the gap shrinks, it was noise.)
- Compute: `bermudan_ref` (0.5), `maxcall` (3), `dual_path` (0.5, one traced outer path).

### 10 · Greeks three ways (3.0) · item 6 · `s06_greeks` (deepened: `three` kept, tape and cost moved to ch11)
- Goal: derive bump, pathwise and likelihood-ratio estimators; the bias–variance trade-off of bumping in 3D; Malliavin
  weights for discontinuous payoffs.
- Beats: **Visual (3D)**: `ThreeDScene`, axes (log h, log n, log RMSE) for the central-difference delta: with independent
  random numbers the surface is a valley (variance ∝ 1/(nh²) wall at small h, bias ∝ h² wall at large h), its floor
  sloping down with n; with common random numbers the small-h wall **collapses** (the surface morphs) and only the bias
  wall remains. Camera orbits 50°. Then the derivations on one ladder, then the existing table (call and digital), then
  the **digital's pathwise failure drawn**: the payoff's step and its derivative (a spike pathwise misses), the LR score
  weight z/(S₀σ√T) multiplying the payoff instead.
- Derivation:
  - Bump: $\frac{\hat V(\theta+h)-\hat V(\theta-h)}{2h}$: bias $\frac{h^2}6V'''$ (Taylor), variance $\frac{\operatorname{Var}(Y(\theta+h)-Y(\theta-h))}{4nh^2}$;
    independent draws: $O(1/(nh^2))$ ⇒ optimal $h\sim n^{-1/6}$, RMSE $\sim n^{-1/3}$; CRN with Lipschitz payoff:
    $\operatorname{Var}=O(h^2)/h^2 = O(1)$ ⇒ RMSE $\sim n^{-1/2}$ (h free).
  - Pathwise: $\frac{\partial}{\partial S_0}\mathbb E[e^{-rT}(S_T-K)^+] = \mathbb E[e^{-rT}\mathbf 1_{S_T>K}\frac{S_T}{S_0}]$
    (interchange: payoff Lipschitz, $\partial S_T/\partial S_0 = S_T/S_0$, dominated convergence).
  - LR: $\frac{\partial}{\partial\theta}\int f(x)p_\theta(x)dx = \mathbb E[f(X)\,\partial_\theta\log p_\theta(X)]$; for
    log-normal $S_T$: $\partial_{S_0}\log p = \frac{Z}{S_0\sigma\sqrt T}$, $\partial_\sigma\log p = \frac{Z^2-1}{\sigma}-Z\sqrt T$
    (differentiate the density, not the payoff).
  - Malliavin (Fournié et al. 1999): delta $= \mathbb E[e^{-rT}f(S_T)\,\pi]$ with weight $\pi = \frac{W_T}{S_0\sigma T}$ — the
    LR weight recovered by integration by parts on Wiener space; works for path-dependent payoffs where densities are
    unknown (one card).
  - Gamma: pathwise fails twice for a call (the indicator's derivative is a delta function); mix: pathwise once, then LR
    (stated; problem 6).
- Experiment: `greeks` (exists: call delta 0.6374 ± 0.0013 (bump), 0.6377 ± 0.0013 (pathwise), 0.6379 ± 0.0033 (LR),
  exact 0.6368; digital LR se 6.2 × 10⁻⁵ vs bump 2.1 × 10⁻⁴); `bump_h` (new). **Planning run, 10,000 paths, 30 seeds:
  CRN RMSE flat at 7.5 × 10⁻³ for h from 0.01 to 3 and 0.055 at h = 30; independent draws 11 at h = 0.01, minimum
  0.017 near h = 10** (the 3D surface adds n = 10³…10⁵).
- Pause-and-predict: "Bump with h = 0.0001 and fresh random numbers. What do you get?" (Noise: the error ∝ 1/h.)
- Compute: `greeks` (0.5), `bump_h` (1).

### 11 · Adjoint differentiation: every Greek for the price of a few (3.0) · item 7 · `s06a_aad` (new; tape and cost from `s06_greeks`)
- Goal: reverse mode explained as the chain rule in the other order; its cost theorem; measured scaling; memory and
  checkpointing; what desks do with it.
- Beats: **Live (the tape runs)**: the forward pass of a 3-step Asian pricing is drawn node by node as a computation
  graph (inputs S₀, σ, r, K, T on the left; log, mul, exp, add, relu, mean nodes), each node recorded onto a horizontal
  **tape** strip; then the backward sweep starts at V̄ = 1 and walks the tape right to left, each node lighting and its
  adjoint value written in, edges carrying ∂(child)/∂(parent) × adjoint; the five input adjoints land at once. Then the
  matrix picture: $J_f J_g J_h$ multiplied right-to-left (forward mode: an n-column block grows) vs left-to-right
  (reverse: a single row). **Measured scaling**: a basket option with d assets (2d inputs: spots and vols), cost of AAD /
  price and bump / price against the number of inputs, log–log: AAD flat, bumping a line of slope 1. Memory: the tape
  length grows with steps × paths; checkpointing (store every k-th state, recompute in between: √-memory trade-off;
  Savine ch. 13).
- Derivation:
  - $y = f(g(h(x)))$, $\nabla y^\top = \bar y\,J_fJ_gJ_h$ (chain rule).
  - Forward: $J_f(J_g(J_h\dot x))$ costs one pass per input direction ⇒ $n$ passes; reverse: $((\bar yJ_f)J_g)J_h$ costs one
    pass for all inputs (associativity).
  - Adjoint recursion: $\bar v_i = \sum_{j:\,i\to j}\bar v_j\,\partial v_j/\partial v_i$ (each node visited once, one
    multiply–add per edge).
  - Cheap gradient principle: $\text{cost}(\nabla f)\le\omega\cdot\text{cost}(f)$, $\omega\approx3$–$5$ (Griewank–Walther),
    independent of $n$.
  - Pathwise + adjoint = Giles–Glasserman: differentiate each path's payoff in reverse (needs Lipschitz payoffs; digitals
    need smoothing or LR — the link to ch10).
- **Lab 5**: `engine.aad_greeks` tape section (lines 320–333, 12 lines after removing timing): run → prints the five AAD
  and bump values from cache (delta 0.5941 vs 0.5932, vega 22.232 vs 22.232 …) and the ratios 2.2× vs 7.4×.
- Experiment: `greeks.aad` (exists); `aad_scale` (new): basket of d = 1…64 assets (2…128 inputs), 4,000 paths, 12
  steps, series autodiff, best of 5 timings, plus a deterministic proxy (tape length and flop count, so the plot does not
  depend on machine load). **Planning run (noisy, machine under load): AAD 1.8–5.6× a price for 8–128 inputs; bumping
  36–126×, growing with the inputs; max delta disagreement 1 × 10⁻⁵ at d = 64.** Recompute when the machine is quiet.
- Pause-and-predict: "A swap book has 2,000 curve points. Bumping costs 4,000 prices. AAD costs about?" (A handful.)
- Compute: `aad_scale` (3).

### 12 · Finite differences I: θ-schemes and stability (3.0) · item 8 · `s07_fd` (deepened: schemes + convergence)
- Goal: discretise the Black–Scholes PDE; prove stability by von Neumann; Lax's theorem; convergence orders measured.
- Beats: **Visual (3D)**: `ThreeDScene` with axes (S, τ, V); the payoff on the τ = 0 edge, the explicit scheme marches
  the surface backward in time-to-expiry, slice by slice (the stencil — three points at one level feeding one at the
  next — highlighted as it moves). At 2,000 steps the surface is smooth; at 200 steps a sawtooth appears at high S and
  grows each slice until the surface explodes off the axes (clipped, red). **Live von Neumann**: the amplification
  factor g(k) plotted against frequency k for λ = aΔt/ΔS² sliding from 0.2 to 0.8: the curve dips below −1 at high k once
  λ > ½ (red region); CN's curve stays in [−1, 1] for all λ but hugs −1 at high k for large λ (setting up ch13). Then the
  existing convergence plot.
- Derivation:
  - $\partial_\tau V = \mathcal LV$, $\mathcal L = \frac12\sigma^2S^2\partial_{SS}+rS\partial_S-r$ (Part 10's PDE in time to expiry).
  - Central differences: $\partial_{SS}V\approx\frac{V_{j+1}-2V_j+V_{j-1}}{\Delta S^2}$, error $O(\Delta S^2)$ (Taylor).
  - θ-scheme: $\frac{V^{n+1}-V^n}{\Delta\tau} = \theta L_hV^{n+1}+(1-\theta)L_hV^n$; local truncation $O(\Delta\tau)$ for θ ≠ ½,
    $O(\Delta\tau^2)$ for θ = ½ (expand about the midpoint).
  - Von Neumann on $u_\tau = au_{xx}$: $V_j^n = g^ne^{ikj\Delta x}$ ⇒ explicit $g = 1-4\lambda\sin^2\frac{k\Delta x}2$, $|g|\le1\iff\lambda\le\frac12$;
    implicit $g = \frac1{1+4\lambda s}$; CN $g = \frac{1-2\lambda s}{1+2\lambda s}$, $s = \sin^2\frac{k\Delta x}2$ (substitute).
  - Lax equivalence: consistent + stable ⇔ convergent (linear problems; stated).
  - For Black–Scholes $a = \frac12\sigma^2S^2$ is largest at $S_{\max}$: $\Delta\tau\le\Delta S^2/(\sigma^2S_{\max}^2)$ (the 400-step
    bound on the 100-point grid).
- Experiment: `fd` (exists: explicit 10.411 at 2,000 steps, −7.5 × 10¹⁰ at 200; bound 400; CN error ratio 4.0, implicit
  3.0); `fd_live` (new: explicit-scheme slices at 2,000 and 200 steps for the 3D march; amplification curves are
  analytic).
- Pause-and-predict: "Double the price points of a stable explicit grid. How many more time steps?" (Four times.)
- Compute: `fd` (0.3), `fd_live` (0.1).

### 13 · Finite differences II: Crank–Nicolson's ringing, and the American put as a complementarity problem (3.0) · item 8 · `s07a_lcp` (new; the ringing moves here from `s07_fd`)
- Goal: why CN rings and Rannacher's cure; the American put as an LCP, solved two ways; the free boundary in 3D.
- Beats: the existing gamma-ringing plot (exact / CN / Rannacher), now preceded by **CN's amplification at −1 drawn** as
  a high-frequency mode on the grid flipping sign every step (a little red zigzag at the strike that does not decay),
  then two implicit half-steps flattening it. **Visual (3D)**: the American put's value surface V(S, τ) with the region
  where V = K − S lit as a "floor" (stopping region) and the free boundary S*(τ) as a gold curve along its edge, rising
  from K at expiry; the European surface fades in beneath for comparison (the gap is the early-exercise premium). Then
  the LCP and two solvers: **PSOR live** (sweeps over the grid, the projection max(payoff, ·) clipping points onto the
  floor, residual dropping) and the **penalty method** (Forsyth–Vetzal 2002: a large penalty where V < payoff, one or
  two Newton solves per step). Card: Brennan–Schwartz (1978) solved it first; Cryer (1971) the PSOR algorithm.
- Derivation:
  - CN: $g\to-1$ as $\lambda s\to\infty$ (the formula of ch12), so the payoff's high-frequency content survives with
    alternating sign; a few implicit steps ($g\to0$) damp it, and keep second order globally (Rannacher 1984).
  - American put: $V\ge h$, $\partial_\tau V-\mathcal LV\ge0$, $(V-h)(\partial_\tau V-\mathcal LV) = 0$ (hold or stop:
    one of the two inequalities is an equality; Part 8's variational inequality).
  - Discrete LCP: $Ax\ge b$, $x\ge g$, $(x-g)^\top(Ax-b) = 0$ (θ-scheme matrix $A = I-\theta\Delta\tau L_h$).
  - PSOR: $x_j\leftarrow\max\big(g_j, x_j+\omega(\tilde x_j-x_j)\big)$, $\tilde x_j$ the Gauss–Seidel update (converges for
    $A$ an M-matrix, $0<\omega<2$; Cryer).
  - Penalty: $(A+P(x))x = b+P(x)g$, $P_{jj} = \rho\mathbf 1_{x_j<g_j}$ (penalise violations); Newton on the active set
    converges in finitely many steps.
- **Lab 6**: `engine.fd_american_put` PSOR inner loop (lines 423–431, 9 lines): run → prints the PDE price 6.085 and the
  tree 6.090.
- Experiment: `fd.gamma` (exists); `lcp` (new): American put by PSOR and by a new penalty solver (§6); iterations per
  step; free boundary from FD vs the tree's boundary; the value surface for 3D (61 × 41). **Planning run: penalty with
  Rannacher start, 400 × 400 grid: 6.0873, two Newton iterations per step, 1.5 s; PSOR 200 × 200: 6.0789 in 0.95 s**
  (tree 6.0900).
- Pause-and-predict: "Where on the surface is the PDE ∂_τV = 𝓛V *not* satisfied?" (In the stopping region, where
  V = K − S.)
- Compute: `fd` (shared), `lcp` (1).

### 14 · ADI for Heston: two dimensions, one direction at a time (3.0) · item 9 · `s08_adi` (deepened)
- Goal: the splitting derived; why the mixed term is explicit and how Craig–Sneyd corrects it; non-uniform grids
  measured; the solution surface and its Greeks.
- Beats: **Visual (3D)**: the Heston price surface u(S, v) on the non-uniform grid, marching in τ; each ADI step shown
  as two sweeps — rows of the grid (fixed v) light up one after another (tridiagonal solves along S), then columns
  (fixed S, along v), then the CS correction flashes the mixed-derivative stencil (a 3 × 3 cross pattern). The camera
  orbits from above (grid visible: points crowded at S ≈ K and v ≈ 0) to the side (the smile of the surface in v).
  **Measured**: uniform vs non-uniform grids, a bar pair per grid size (error 2.66 vs 0.045 at 40 price points: a
  60-fold effect). Then the existing error-vs-grid lines. Then "Greeks for free": delta, gamma and vega read off the
  grid by finite differences, drawn as surfaces beside the price.
- Derivation:
  - $\partial_\tau u = \frac12vS^2u_{SS}+\rho\xi vSu_{Sv}+\frac12\xi^2vu_{vv}+rSu_S+\kappa(\theta-v)u_v-ru$ (Heston's PDE,
    Feynman–Kac on the 2D state; Part 13).
  - $A = A_0+A_1+A_2$ (mixed, S-direction, v-direction parts).
  - Douglas: $Y_0 = U^{n}+\Delta\tau AU^{n}$; $(I-\vartheta\Delta\tau A_j)Y_j = Y_{j-1}-\vartheta\Delta\tau A_jU^n$, $j=1,2$
    (each a set of tridiagonal systems: $O(N)$ per step against $O(N^{3/2})$ for a sparse 2D solve).
  - CS: $\hat Y_0 = Y_0+\frac12\Delta\tau(A_0Y_2-A_0U^n)$, then the two implicit corrections again (second order with the
    mixed term, ϑ = ½; Craig–Sneyd 1988; in 't Hout–Foulon 2010 also MCS and HV).
  - Non-uniform grid: $S_i = K+c\sinh\xi_i$ (uniform $\xi$): spacing $\propto\cosh\xi$, smallest at $K$; three-point weights
    for $u_S, u_{SS}$ on uneven spacing (second order if the map is smooth).
- **Lab 7** (optional, if time): `engine.heston_adi` step (lines 517–526, 10 lines): run → the 160 × 80 price 7.0224 vs
  COS 7.0243.
- Experiment: `adi` (exists: CS 160 × 80 error 0.0019 in 0.82 s; Douglas slightly ahead here); `adi_grid` (new).
  **Planning run: uniform grids error 2.66 (40 × 20) and 1.47 (80 × 40); non-uniform 0.045 and 0.0094.** Plus the
  surfaces (price, delta, gamma, vega) on 41 × 21 for 3D.
- Pause-and-predict: "Why crowd the variance grid near v = 0?" (The solution changes fastest there; Feller's condition
  is broken, so the variance spends time near 0.)
- Compute: `adi` (0.5), `adi_grid` (1).

### 15 · Fourier I: Carr–Madan and Lewis (2.8) · item 10 · `s09_fourier` (deepened: methods)
- Goal: price from the characteristic function; derive Carr–Madan's damping and Lewis's single integral; the FFT grid
  trade-off.
- Beats: **Visual**: the call price as a function of log-strike k (rising to S₀ as k → −∞: not integrable); multiply by
  e^{αk} (ValueTracker on α from 0 to 1.5): the curve becomes a hump that decays both ways — now it has a transform. Its
  transform ψ(u) drawn as real and imaginary parts, oscillating and decaying. Then the FFT grid: two rulers, η on the
  u-axis and λ on the k-axis, with **λη = 2π/N** — shrinking η stretches λ (a slider shows the strike spacing becoming
  useless). Then Lewis: the contour moved to Im u = −½, the integrand smooth and fast-decaying; one quadrature gives the
  price to 8 × 10⁻¹³ of COS.
- Derivation:
  - $c_T(k) = e^{-\alpha k}c^\alpha(k)$, $\psi(u) = \int e^{iuk}e^{\alpha k}c_T(k)dk = \frac{e^{-rT}\varphi(u-(\alpha+1)i)}{\alpha^2+\alpha-u^2+i(2\alpha+1)u}$
    (Fubini; integrate the payoff against $e^{(\alpha+iu)k}$).
  - $c_T(k) = \frac{e^{-\alpha k}}\pi\int_0^\infty e^{-iuk}\psi(u)du$ (inverse transform; real-valued price, so half-line).
  - Discretise: $u_j = j\eta$, $k_m = -b+m\lambda$, $\lambda\eta = 2\pi/N$ (to match the DFT kernel $e^{-2\pi ijm/N}$); Simpson
    weights (the code's `w`).
  - Condition on α: $\mathbb E[S_T^{\alpha+1}]<\infty$ (the moment must exist; for Heston it fails beyond a critical α at
    long maturities — Andersen–Piterbarg's moment explosions, one line).
  - Lewis (2001): $C = S_0-\frac{\sqrt{S_0K}}\pi\int_0^\infty\operatorname{Re}\big[e^{iuk}\varphi(u-\tfrac i2)\big]\frac{du}{u^2+\frac14}$,
    $k = \log(S_0/K)$ (Parseval with the payoff's transform on the strip, contour at Im = −½).
- Experiment: `fourier` (exists: CM errors 0.039 → 2.5 × 10⁻⁵ for N = 512 → 16,384); `lewis` (new). **Planning run: Lewis
  by adaptive quadrature 7.024291416814 vs COS reference 7.024291416815 (difference −7.8 × 10⁻¹³).** CM error vs α
  (0.5 … 3) at N = 4,096 (computed: a U-shape expected).
- Pause-and-predict: "N doubles with η fixed. What happens to the strike spacing?" (It halves: λ = 2π/(Nη).)
- Compute: `fourier` (0.1), `lewis` (0.1).

### 16 · Fourier II: the COS method, and the race (3.0) · item 10 · `s09a_cos` (new; the race moves here from `s09_fourier`)
- Goal: derive COS; watch a density rebuilt by cosines; truncation and the term count; then the scoreboard of the whole
  part.
- Beats: **Live**: the Heston log-return density (true, from a fine COS) in grey; the cosine series is added term by term
  (N = 2, 4, 8, 16, 32, 64) in gold, the residual shaded red shrinking to nothing; a side panel shows |coefficient| on a
  log scale falling in a straight line (exponential decay). Then truncation: the window [a, b] from cumulants
  (c₁ ± L√c₂) slides narrower until the left tail is cut off and the error floor appears (why the code uses L = 16 for
  ρ = −0.7). Then **the race** (existing plot, now drawn as a live race: points appear in order of wall-clock time on a
  log axis, as if all methods started together) with a new MC line using the best variance reduction of ch3 (control
  variate) — the honest MC frontier. Bermudans by COS (Fang–Oosterlee 2009) named.
- Derivation:
  - $V = e^{-rT}\int_{\mathbb R}v(y)f(y)dy\approx e^{-rT}\int_a^bv(y)f(y)dy$ (truncate; tails small).
  - $f(y) = \sum_{k\ge0}{}'A_k\cos\big(k\pi\frac{y-a}{b-a}\big)$, $A_k = \frac2{b-a}\int_a^bf(y)\cos(k\pi\frac{y-a}{b-a})dy$ (cosine
    series on $[a,b]$).
  - $A_k\approx\frac2{b-a}\operatorname{Re}\big[\varphi\big(\frac{k\pi}{b-a}\big)e^{-ik\pi\frac a{b-a}}\big]$ (extend the integral to
    $\mathbb R$: the definition of $\varphi$).
  - $V\approx e^{-rT}\sum_{k<N}{}'\operatorname{Re}\big[\varphi(\tfrac{k\pi}{b-a})e^{ik\pi\frac{x-a}{b-a}}\big]V_k$, $V_k$ the payoff's
    cosine coefficients in closed form ($\chi_k,\psi_k$: the code's `chi`, `psi`).
  - Error: truncation + $O(e^{-\nu N})$ for densities analytic in a strip (exponential convergence); Junike (2024) gives
    an explicit N for a target error (frontier, ch19).
- Experiment: `fourier` (exists: COS 128 terms 1.4 × 10⁻⁶, 256 terms 4.8 × 10⁻⁸); `cos_density` (new: reconstructions and
  coefficients; L sweep 4…40 with error); `race` (exists; add an MC-with-control line, 4 sizes, computed).
- Pause-and-predict: "Why can COS not price a barrier directly?" (A barrier needs the path, not just the terminal
  density: use a grid or simulation, or COS with monitoring dates.)
- Compute: `cos_density` (0.1), `race` (1).

### 17 · Industry: the overnight run, GPUs, and adjoints at banks (3.0) · item 11 · `s10_hardware` (reshaped as the industry chapter)
- Goal: how desks, clearing houses and regulators actually compute, from the public record; firm file; crisis file.
- Beats (each a card or a live object, source on screen):
  1. **The overnight run** (live): a bank's book as a grid of trades × scenarios filling cell by cell (thousands of
     scenarios for XVA (Part 21), risk limits, capital). Why sensitivities: ISDA SIMM margin is computed from delta,
     vega and curvature sensitivities (ISDA SIMM methodology), and Basel's FRTB standardised approach uses a
     sensitivities-based method (BCBS d457, 2019) — so banks need thousands of Greeks a day, which is AAD's market.
  2. **Firm file: Danske Bank** — Risk.net In-House System of the Year 2015 for AAD-based risk: CVA sensitivities in
     about 10 seconds on standard hardware (Risk.net, as reported; Savine, then at Danske, wrote the 2018 textbook).
  3. **Firm file: JPMorgan and Maxeler (2011)** — as reported by insideHPC and Computer Weekly (July 2011): the credit
     portfolio's end-of-day risk run, eight hours (HPCwire: 8–12 h) on thousands of x86 cores, cut to about 238 s with
     12 s on FPGAs; Maxeler engineers ported the copula and convolution kernels. Figures are the bank's and vendor's
     own presentations (say so).
  4. **GPUs and the benchmark**: STAC-A2, designed by bank quants with STAC, times Heston Monte Carlo Greeks (delta, gamma,
     cross-gamma, model vega, correlation vega, theta, rho) of a multi-asset path-dependent option with early exercise —
     ch2's streams, ch3–6's estimators, ch9's early exercise and ch11's Greeks in one benchmark. Vendor results
     (NVIDIA, Intel, Oracle) are vendor-run; no figures quoted unless re-checked against a report.
  5. **Clearing houses**: OCC's STANS margin uses large-scale Monte Carlo (OCC, SEC filing; verified in the Part 5
     plan). Open source: QuantLib's Sobol + Brownian-bridge path generators (ch6), ORE (Open Source Risk Engine) built
     on it.
  6. **Measured on this machine (live)**: the same 10⁶-path pricing run as a Python loop, vectorised numpy, numpy
     float32, and split across 1/2/4 processes (the speed-up bars grow as they finish). Honest result: vectorisation
     ≫ cores here; "algorithms first" (COS ≈ 14,000× faster than MC's best from the existing `race`).
  7. **Crisis file (one card, cross-referenced to Part 20)**: the London Whale's VaR spreadsheet — JPMorgan's 2013 Task
     Force report found a modeling spreadsheet that divided by the sum of two rates instead of their average, muting
     the measured volatility; the computation, not the market, was wrong (verify the report's wording and page before it
     goes on screen; Part 20 keeps the full file). Lesson for the House: Rule 16's independent second method.
  8. **Validation**: the House's test table (old `s11_house`) shown as the nightly validation report: every engine
     function, its reference, its tolerance.
- Experiment: `parallel` (new): loop / numpy / float32 / ProcessPool(1, 2, 4) on one pricing, best of 3; run when the
  machine is quiet, label "this machine, <date>". `race` (exists) for the 14,000×.
- Pause-and-predict: "Monte Carlo is embarrassingly parallel. Is an American LSM pricing?" (Not fully: the backward
  regression is a reduction across paths at every date.)
- Compute: `parallel` (1).

### 18 · Quantum amplitude estimation: the real speedup (2.8) · item 11 · `s10a_quantum` (new)
- Goal: what quantum computers would speed up (the 1/ε² of ch1), built from the rotation picture, simulated, and
  costed honestly.
- Beats: **Visual (the rotation)**: a 2D plane spanned by |good⟩ and |bad⟩; the state sits at angle θ with sin²θ = a =
  the price (normalised). Grover's operator Q is drawn as two reflections whose product rotates the state by 2θ;
  applying Q^m moves it to angle (2m+1)θ, the measurement probability sin²((2m+1)θ) oscillating faster with m.
  **Replay (the estimate learning a)**: maximum-likelihood amplitude estimation (Suzuki et al. 2020, no phase estimation):
  shots at m = 0, 1, 2, 4, …; after each batch the likelihood curve over θ is redrawn — first broad, then multi-peaked,
  then a needle — 40 repetitions as a band on the error-vs-oracle-calls log–log plot, slope −1 against MC's −½.
  Then the resource cards.
- Derivation:
  - $\mathcal A|0\rangle = \sqrt{1-a}\,|\psi_0\rangle|0\rangle+\sqrt a\,|\psi_1\rangle|1\rangle$, $a = \mathbb E[\tilde f(X)]\in[0,1]$ (load
    the distribution, rotate an ancilla by the payoff).
  - $Q = -\mathcal AS_0\mathcal A^{-1}S_\chi$ is a rotation by $2\theta$ in span{good, bad}, $a = \sin^2\theta$ (product of two
    reflections is a rotation by twice the angle between them).
  - $P(\text{good after }Q^m) = \sin^2((2m+1)\theta)$ (apply the rotation $m$ times).
  - Heisenberg scaling: with $N$ oracle calls, error $O(1/N)$, against $O(1/\sqrt N)$ classically (Brassard–Høyer–Mosca–
    Tapp 2002; Montanaro 2015): quadratic speedup, **in samples, not in seconds**.
  - What it costs: Chakrabarti et al. (*Quantum* 2021, Goldman Sachs and IBM authors): advantage on autocallables/TARFs
    needs ≈ 8,000 logical qubits, T-depth 54 million, run in about a second; Stamatopoulos–Zeng (*Quantum* 2024, QSP):
    ≈ 4.7k logical qubits and 10⁹ T-gates at a 45 MHz logical clock. Classical: COS prices a vanilla in 0.2 ms here.
- Experiment: `qae` (new; noise-free simulation of the measurement law, not a circuit). **Planning run, a = 0.3, 50 shots
  per power, 40 repetitions: RMSE 2.2 × 10⁻² at 450 oracle calls (equal to MC), 2.2 × 10⁻⁵ at 410,150 calls against
  MC's 7.2 × 10⁻⁴ — about 32× better, slope ≈ −1.0.** (Use a local grid refinement around the MLE: a 200,001-point θ grid
  limits precision near 10⁻⁵.)
- Pause-and-predict: "A quantum computer with a quadratic speedup in samples, running each sample 10,000 times slower
  than a CPU. When does it win?" (Only once 1/ε exceeds ~10,000: the clock-rate argument of the resource papers.)
- Compute: `qae` (1).

### 19 · Frontier: pricing faster, 2023–2026 (2.8) · `s10b_frontier` (new)
- Goal: where computational pricing research is now, with one method trained and one measured on screen.
- Beats: **Replay (train a pricer, then use it)**: Chebyshev tensor interpolation of the Heston call over (S₀, v₀)
  (Gaß, Glau, Mahlstedt, Mair 2018): `ThreeDScene` surface of the max error over the box, nodes doubling 4 → 32 per axis
  (the node lattice drawn on the floor, Chebyshev-clustered at the edges), the error surface collapsing from 10⁻¹ to
  10⁻⁶ as the replay runs; then a **speed card**: one interpolant evaluation vs one COS price vs one MC price. Low-rank
  tensor formats (Glau–Kressner–Statti 2020) extend it to many parameters; neural surrogates (Part 17) are the
  learned version. **Measured: RQMC median-of-means** — mean of 11 scrambled Sobol estimates vs their median on a smooth
  integrand, log–log against n: the mean follows n^{−3/2}, the median dives faster (Pan–Owen, *Math. Comp.* 2023). Cards:
  - Pan, Owen (2023), "Super-polynomial accuracy of one dimensional randomized nets using the median-of-means", *Math.
    Comp.* 92(340); multivariate follow-up arXiv 2208.05078.
  - Junike (2024), "On the number of terms in the COS method for European option pricing", *Numerische Mathematik*
    156:533–564; Junike–Pankrashkin (2022), truncation range (*Applied Math. & Computation* *(verify)*).
  - Bayer, Pelizzari, Schoenmakers (2023/2025), "Primal and dual optimal stopping with signatures", arXiv 2312.03444:
    Longstaff–Schwartz with signature features for non-Markovian (rough) models, and a signature dual — ch8–9
    generalised (journal version *(verify)*).
  - Stamatopoulos, Zeng (2024), "Derivative pricing using quantum signal processing", *Quantum* 8, 1322 (ch18).
  - Dalzell et al. (2023/2025), "Quantum algorithms: a survey of applications and end-to-end complexities", arXiv
    2310.03011: the finance section's sober accounting (book version *(verify)*).
  - Context: Giles (2015) *Acta Numerica* MLMC survey; Gaß et al. (2018); Glau et al. (2020).
- Experiment: `cheb` (new). **Planning run: max error over (S₀, v₀) ∈ [70, 130] × [0.01, 0.09], 200 random test points:
  n = 8 → 4.1 × 10⁻², 16 → 1.3 × 10⁻³, 24 → 7.7 × 10⁻⁵, 32 → 3.7 × 10⁻⁶ (1,024 COS calls to build).**
  `rqmc_median` (new). **Planning run, ∫e^u on [0,1], 11 scrambles, 30 repeats: at n = 2¹⁰ the mean's RMSE is 1.9 × 10⁻⁶
  and the median's 8.9 × 10⁻¹⁰ (at the floating-point floor by 2¹²).**
- Pause-and-predict: "The Chebyshev pricer needs 1,024 COS prices to build. When does it pay?" (After about a thousand
  queries — e.g. a calibration or an XVA scenario run.)
- Compute: `cheb` (1), `rqmc_median` (0.5).

### O · The pricing engine, recap, desk questions, problems (2.8) · `s12_outro` (absorbs `s11_house`)
- House card: the pricing engine, org chart lit; Rule 16 (every price leaves with its error; every method checked
  nightly against an independent one); trial counter (no strategy tested: unchanged).
- Recap in 11 lines (one per item, each with its computed headline number).
- Desk questions (README solutions): keep "How many paths for a price to 1 bp?" and "Why is AAD's cost independent of
  the number of Greeks?"; keep the CN-gamma question; add **"Your LSM price is 6.06 and your dual bound 6.41. What do you
  do?"** (more inner paths; check the gap shrinks; then improve the basis).
- Problems (≈ 90 s): existing 5, plus (6) "a mixed pathwise–LR estimator of a call's gamma", (7) "the MLMC cost when
  β = γ: show Σ√(V_lC_l) grows like L ∼ log ε⁻¹", (8) "show λη = 2π/N is forced by the DFT".
- Payoff card: Parts 17 (networks trained on this engine's prices and AAD Greeks), 19 (rates by lattice and MC), 21
  (XVA scenario runs), 40 (IS for tails).
- References card (textbooks + the paper list).
- Retire `s11_house` from the manifest (its table moves to ch17, its rule here). Chapter numbers on cards and in the
  manifest must agree after renumbering.

### Minutes (targets; the per-chapter figures in the headings above are upper limits)

| Scene | Min | Scene | Min |
|---|---|---|---|
| Hook | 2.6 | 10 Greeks three ways | 2.7 |
| 1 Monte Carlo | 2.7 | 11 AAD | 2.8 |
| 2 Random numbers, paths | 2.6 | 12 FD I | 2.7 |
| 3 Control, antithetic, strata | 2.8 | 13 FD II, LCP | 2.8 |
| 4 Importance sampling | 2.7 | 14 ADI | 2.9 |
| 5 QMC points | 2.8 | 15 Carr–Madan, Lewis | 2.6 |
| 6 Bridge, effective dim. | 2.7 | 16 COS, race | 2.8 |
| 7 MLMC | 3.0 | 17 Industry | 2.8 |
| 8 LSM | 2.8 | 18 Quantum AE | 2.6 |
| 9 Dual, max-call | 2.9 | 19 Frontier | 2.6 |
| | | Outro | 2.6 |
| | | **Total** | **≈ 57.5** |

About 7,900 words at 139 wpm. The heading figures (2.7–3.2) sum to about 61, over the ceiling, so write to the targets
(≈ 360–400 words a chapter). Measure with `lecture_length.py quant16 --floor 50`; if the total exceeds 60, trim ch2 and
ch17 first (both have card material that can go to the README); if under 52, ch9 and ch14 take the slack.

---

## 3b. Hands-on summary

**Labs (`lab_card` ≤ 12 lines of real House code, then `lab_run` printing cached results):**
1. ch2 `engine.brownian_bridge` — `explainer/quant/house/engine.py` 65–80 (trim to 12) → LLᵀ = min(tᵢ, tⱼ) to 10⁻¹⁶.
2. ch3 `engine.mc_call` control and antithetic branches — 31–36 and 44–50 → the three rmse values.
3. ch7 `engine._mlmc_level` — 99–112 → V₀ … V₉.
4. ch9 `engine.andersen_broadie_put` — 248–259 → (inner, upper, se) rows.
5. ch11 `engine.aad_greeks` tape — 320–333 → five AAD vs bump values; 2.2× vs 7.4×.
6. ch13 `engine.fd_american_put` PSOR — 423–431 → 6.085 vs tree 6.090.
7. (optional) ch14 `engine.heston_adi` step — 517–526; ch16 `stochvol.cos_price` core — `explainer/quant/house/stochvol.py`
   91–100 → COS errors by N.
Line numbers are as of this session; re-read before quoting.

**Replays (ValueTracker / `TrainingReplay`, seeds as `seed_band`):**
- ch4 cross-entropy learning the IS shift (5 seeds; baseline: the strike-centred θ, dashed).
- ch7 the MLMC adaptive algorithm adding levels and samples (4 seeds on the cost readout; baseline: standard MC cost).
- ch8 LSM backward induction date by date (boundary vs the tree's); basis × paths sweep (5 seeds; ceiling: the dual).
- ch18 MLAE likelihood sharpening; error vs oracle calls (40 repetitions as a band; baseline: MC at equal calls).
- ch19 Chebyshev pricer "training" by node doubling (error surface; baseline: COS cost per query).

**Live simulations:** the CI funnel (ch1); inverse transform, Box–Muller, Cholesky shear (ch2); the rotating regression
and collapsing histogram, strata filling (ch3); the sliding IS density and weight histogram (ch4); the net's boxes
lighting (ch5); the bridge crystallising (ch6); fine/coarse coupled paths (ch7); the outer path and its martingale
(ch9); the bump RMSE surface morph (ch10); the AAD tape (ch11); the explicit march exploding, the g(k) curve (ch12);
CN's sign-flipping mode, PSOR sweeps (ch13); ADI row/column sweeps (ch14); the α-damping slider (ch15); the density
rebuilt by cosines, the live race (ch16); the trades × scenarios grid, speed-up bars (ch17); the Grover rotation (ch18).

**3D scenes (`ThreeDScene`):** ch6 coordinate staircase; ch10 bump RMSE over (h, n); ch12 explicit march over (S, τ);
ch13 American value surface with the stopping floor and free boundary; ch14 Heston surface u(S, v) with sweeps and
Greeks; ch19 Chebyshev error over (S₀, v₀).

**Compute budget (seeded; ≈ 35 CPU-minutes of 120):**

| Item | Min | Item | Min | Item | Min |
|---|---|---|---|---|---|
| race* | 1 | mlmc* | 2 | fd_live | 0.1 |
| mc* | 0.5 | mlmc_trace | 1 | lcp | 1 |
| mc_live | 0.3 | mlmc_milstein | 3 | adi* | 0.5 |
| rng | 0.2 | american* | 2 | adi_grid | 1 |
| control | 0.5 | lsm_live | 2 | fourier* | 0.1 |
| is_sweep | 0.3 | bermudan_ref | 0.5 | lewis | 0.1 |
| qmc* | 1 | maxcall | 3 | cos_density | 0.1 |
| discrepancy | 0.3 | dual_path | 0.5 | parallel | 1 |
| effdim | 0.5 | greeks* | 0.5 | qae | 1 |
| fd* | 0.3 | bump_h | 1 | cheb | 1 |
| envelope* | 0 | aad_scale | 3 | rqmc_median | 0.5 |

(* exists.) Everything is numpy/scipy; no torch training (the max-call comparison loads Part 17's cached result through
`videos.quant.quant17.compute.load`, the documented cross-part route). Long items (`maxcall`, `aad_scale`,
`mlmc_milstein`) use `CACHE.partial` per sub-run. One command rebuilds the part: `python -m videos.quant.quant16.compute`.
Timing items (`aad_scale`, `parallel`, `race`) report best-of-N and a machine-independent proxy where possible.

---

## 4. Industry and frontier: sources

Checked this session (2 November 2026) unless marked:

| Fact | Source |
|---|---|
| Chakrabarti, Krishnakumar, Mazzola, Stamatopoulos, Woerner, Zeng, "A threshold for quantum advantage in derivative pricing", *Quantum* 5, 463 (2021): "8k logical qubits", T-depth 54 million, run "on the order of a second" (abstract). The current video says 7,500: check the body. | https://arxiv.org/abs/2012.03819 |
| Stamatopoulos, Zeng, "Derivative pricing using quantum signal processing", *Quantum* 8, 1322 (2024): ~16× fewer T-gates, ~4× fewer logical qubits; advantage needs ≈ 4.7k logical qubits and 10⁹ T-gates at 45 MHz | https://arxiv.org/abs/2307.14310 |
| JPMorgan–Maxeler FPGA risk run (2011): 8 h → ≈ 238 s (12 s on FPGAs), credit/CDO portfolio; HPCwire: 8–12 h on thousands of x86 cores; copula and convolution kernels ported in ≈ 3 months (bank and vendor presentations, as reported) | https://insidehpc.com/2011/07/jp-morgan-supercomputer-risk-analysis-in-near-real-time/ ; https://www.computerweekly.com/news/2240112723/JP-Morgan-gies-live-with-FPGA-supercommuter ; https://www.hpcwire.com/2011/03/10/maxeler_carves_high-end_niche_with_hpc_acceleration_business/ |
| STAC-A2: Heston MC sensitivities (theta, rho, delta, gamma, cross-gamma, model vega, correlation vega) for a multi-asset path-dependent option with early exercise; designed with bank quants; vendor-run reports | https://docs.stacresearch.com/node/46089 ; https://stacresearch.com/system/files/resource/files/STAC_Intel_Webinar_27sep13-final_0.pdf |
| ISDA SIMM: initial margin per risk class = delta + vega + curvature margin, computed from sensitivities (v2.8 current) | https://www.isda.org/a/hhkiE/ISDA-SIMM_v2.82512_PUBLIC.pdf |
| Glasserman (2003) chapter titles (1 Foundations … 9 Risk Management) | library record via search; Springer page https://link.springer.com/book/10.1007/978-0-387-21617-1 |
| Andersen–Piterbarg vol. I Part I order: arbitrage theory, FD methods, MC methods, rates fundamentals, instruments | https://imusic.fi/books/9780984422104 (retailer listing) |
| Savine (2018) ch. 13 "Check-Pointing and Calibration" | https://eld.bl.uk/catalog/019129058 |
| Pan, Owen, *Math. Comp.* 92(340) (2023), median-of-means for randomized nets; multivariate arXiv 2208.05078 | https://arxiv.org/abs/2111.12676 ; https://arxiv.org/abs/2208.05078 |
| Junike, *Numerische Mathematik* 156:533–564 (2024), number of COS terms; builds on Junike–Pankrashkin (2022) truncation range | https://link.springer.com/article/10.1007/s00211-024-01402-1 ; https://arxiv.org/abs/2303.16012 |
| Bayer, Pelizzari, Schoenmakers, "Primal and dual optimal stopping with signatures", arXiv 2312.03444 (v2 Feb 2025; no journal ref on arXiv) | https://arxiv.org/abs/2312.03444 |
| Dalzell et al., quantum algorithms survey (finance section) | https://arxiv.org/abs/2310.03011 |
| JPMorgan 2013 Task Force: VaR spreadsheet divided by the sum instead of the average (secondary sources quoting the report; Bloomberg 16 Jan 2013) | https://www.bloomberg.com/news/articles/2013-01-16/jpmorgan-halves-dimon-pay-says-ceo-responsible-for-lapses-1- ; primary report to be fetched *(verify wording, page)* |
| From the Part 5 plan (verified there): Giles–Glasserman "Smoking adjoints" (*Risk* 2006); Danske Bank Risk In-House System of the Year 2015 (AAD, CVA in ~10 s); OCC STANS Monte Carlo; QuantLib Sobol–Brownian-bridge generators | https://www.risk.net/1500261 ; https://www.risk.net/derivatives/2387869/house-system-year-danske-bank ; https://www.theocc.com/Risk-Management/Margin-Methodology ; https://rkapl123.github.io/QLAnnotatedSource/d3/dd6/class_quant_lib_1_1_sobol_brownian_generator_base.html |

**Unverified (keep the marks or drop):** BCBS d457 (FRTB, 2019) sensitivities-based method wording (https://www.bis.org/bcbs/publ/d457.htm,
not fetched); Salmon et al. SC'11 bibliographic details (well known; DOI not fetched); the source of the max-call bounds
[26.156, 26.162] stored in `house/deep.py`; Junike–Pankrashkin venue; Owen's "On dropping the first Sobol' point"
venue/year; Gaß et al. 2018 and Glau et al. 2020 volumes/pages; Chakrabarti et al.'s 7.5k vs 8k figure in the body;
the affiliations of Stamatopoulos and Zeng (Goldman Sachs at the time of the 2021 paper; check the 2024 paper); any
STAC-A2 headline numbers (none quoted); ORE's description (fetch its site before quoting).

---

## 5. Revised SYLLABUS.md §6 entry (paste-ready)

```markdown
### Part 16 · Computing Prices (~57)
1. Monte Carlo: the estimator, the CLT error bar, efficiency (variance × work); random numbers (inverse transform,
   Box–Muller, Cholesky) and reproducible parallel streams (counter-based generators).
2. Variance reduction: antithetics, control variates (the optimal coefficient; Kemna–Vorst's geometric control),
   stratification and Latin hypercubes; importance sampling (the zero-variance measure, the optimal shift learned by
   cross-entropy, weight degeneracy).
3. Quasi-Monte Carlo: discrepancy and Koksma–Hlawka, Sobol nets (Joe–Kuo), scrambling for error bars; the Brownian
   bridge and PCA; effective dimension (Caflisch–Morokoff–Owen 1997; Paskov–Traub 1995).
4. Multilevel Monte Carlo (Giles 2008): the complexity theorem proved; Euler (β = 1) against Milstein (β = 2);
   randomised MLMC (Rhee–Glynn 2015).
5. American options by simulation: Longstaff–Schwartz run backward on real paths; the duality bound derived
   (Rogers; Haugh–Kogan) and computed (Andersen–Broadie); the five-asset max-call, against Part 17's network.
6. Greeks: bumps (bias–variance, common random numbers), pathwise, likelihood ratio, Malliavin weights
   (Broadie–Glasserman 1996; Fournié et al. 1999).
7. AAD (Giles–Glasserman 2006): reverse mode, the cheap-gradient principle, cost against the number of inputs,
   check-pointing.
8. Finite differences: θ-schemes, von Neumann stability and Lax's theorem; Crank–Nicolson's ringing and Rannacher; the
   American put as a complementarity problem (PSOR; the penalty method).
9. ADI for Heston (Douglas; Craig–Sneyd; in 't Hout–Foulon), on non-uniform grids.
10. Fourier: Carr–Madan and Lewis derived; COS (Fang–Oosterlee 2008) and its truncation; the race between every method.
11. Hardware: the overnight run, GPUs and FPGAs, sensitivities for SIMM and FRTB; quantum amplitude estimation built,
    simulated and costed.

*Textbooks:* Glasserman ch. 1–5, 7–8 (6 → Part 5, 9 → Part 40); Savine Parts II–III; Andersen–Piterbarg vol. I (FD and
MC chapters); Duffy; Seydel (finite elements: README note); Oosterlee–Grzelak (COS chapter).
*Computed:* the CI funnel; Kemna–Vorst control (variance ÷ ~1,300); the IS variance curve and cross-entropy; star
discrepancy; effective dimension (step/bridge/PCA); MLMC Euler vs Milstein; LSM boundary, duality gap, Bermudan
reference, five-asset max-call; bump RMSE surface; AAD cost against inputs; explicit blow-up; PSOR vs penalty; uniform
vs non-uniform ADI; Lewis vs COS; the race; QAE vs MC at equal oracle calls; a Chebyshev pricer; RQMC median-of-means.
*Visuals:* the net's boxes lighting; the bridge's coordinate staircase (3D); the MLMC telescope; LSM run backward;
the bump-error valley (3D); the AAD tape running backward; the explicit march exploding (3D); the American surface with
its free boundary (3D); ADI sweeps on the Heston surface (3D); a density rebuilt by cosines; the Grover rotation.
*Labs:* `brownian_bridge`, `mc_call`, `_mlmc_level`, `andersen_broadie_put`, `aad_greeks`, `fd_american_put`.
*Industry:* the overnight run; SIMM and FRTB sensitivities; Danske Bank's AAD; JPMorgan's FPGAs (2011); STAC-A2;
OCC's Monte Carlo margin; QuantLib. *Frontier:* QSP derivative pricing (2024); median-of-means RQMC (2023); COS term
bounds (2024); signature stopping (2023–25); Chebyshev and tensor pricers.
*Crisis:* the London Whale's VaR spreadsheet (2012; full file in Part 20). *Firms:* Danske Bank; JPMorgan; bank quant
libraries and overnight risk runs.
*Desk:* "How many paths for a price to 1 bp?"; "Why is AAD's cost independent of the number of Greeks?";
"Crank–Nicolson's gamma oscillates: why, and the fix?"; "LSM 6.06, dual 6.41: what next?"
*House:* the pricing engine; Rule 16 (every price with its error, every method checked against another).
```

---

## 6. Implementation notes

**Manifest (21 scenes; new modules marked +):** `s01_hook`, `s02_mc`, +`s02a_paths`, +`s02b_control`,
+`s02c_importance`, `s03_qmc`, +`s03a_bridge`, `s04_mlmc`, `s05_american`, +`s05a_dual`, `s06_greeks`, +`s06a_aad`,
`s07_fd`, +`s07a_lcp`, `s08_adi`, `s09_fourier`, +`s09a_cos`, `s10_hardware` (chapter 17, "Industry: the overnight run"),
+`s10a_quantum`, +`s10b_frontier`, `s12_outro`. `s11_house` leaves the manifest (keep the file or delete it; its
narration cache becomes unused). Existing chapter cards are renumbered (`s02_mc` stays 1; `s03_qmc` becomes 5;
`s04_mlmc` 7; `s05_american` 8; `s06_greeks` 10; `s07_fd` 12; `s08_adi` 14; `s09_fourier` 15; `s10_hardware` 17).
Material moved between kept modules (IS and the variance-reduction plot out of `s02_mc`; the race out of
`s09_fourier`; the tape and cost out of `s06_greeks`; the ringing out of `s07_fd`) changes their narration, so those
narration caches regenerate anyway.

**New House functions** (append to `explainer/quant/house/engine.py`; tests appended to `tests/test_quant_house.py`):
- `geometric_asian_call(S0, K, T, sigma, r, n_fix)` — closed form for the discrete geometric Asian. Test: matches a
  200,000-path MC within 3 se.
- `asian_control(S0, K, T, sigma, r, n_paths, n_fix, seed)` — Kemna–Vorst control-variate estimator returning
  (price, se, ρ). Test: variance ratio > 100 and price within 3 se of a long plain run.
- `stratified_call(..., n_strata)` — proportional stratification of the terminal normal. Test: unbiased; variance ≤ plain.
- `is_cross_entropy(f, theta0, n, iters, seed)` — CE iterates for a normal shift. Test: on the K = 160 call converges
  to within 0.2 of the variance-optimal shift found by a grid.
- `path_matrix(n_steps, T, kind)` — L for 'step', 'bridge', 'pca' with LLᵀ = C. Test: all three reproduce C to 1e-12;
  `variance_captured(a, L)` — Test: PCA's first share ≥ bridge's ≥ step's.
- `l2_star_discrepancy(x)` (Warnock's formula). Test: the 1-point set {0.5} in 1D gives the known value; Sobol < random
  at n = 1,024, d = 2.
- `mlmc(..., scheme="euler"|"milstein", payoff="asian"|"call", trace=False)` — extend the existing function with keyword
  arguments whose defaults keep current behaviour (so the cached `mlmc` item is unchanged); `trace=True` returns the
  per-iteration (L, N_l, V_l) log for the replay. Test: Milstein V_l slope ≥ 1.7 over levels 3–8; estimate within 3 se
  of Black–Scholes for the call.
- `lsm_trace(...)` — the per-date scatter, fit and boundary (or a `trace=True` on `lsm_put`). Test: boundary below K
  and increasing in t; out-of-sample lower bound ≤ tree price + 3 se.
- `bermudan_tree(S0, K, T, sigma, r, n_dates, n_steps)` — CRR with exercise only on the dates. Test: European ≤
  Bermudan ≤ American (2,000-step) for the put.
- `lsm_max_call(p, n_fit, n_eval, seed)` — the five-asset LSM with the sorted-asset basis (reuse `deep.max_call_paths`).
  Test: d = 2 case within 0.1 of the 13.902 binomial reference stored in Part 17.
- `aad_basket(d, n_paths, n_steps, seed)` — AAD vs bump for 2d inputs; returns times and tape length. Test: AAD deltas
  equal bump deltas to 1e-3.
- `fd_american_penalty(S0, K, T, sigma, r, nS, nt, rho=1e8, rannacher=2)` — Forsyth–Vetzal. Test: within 0.01 of the
  2,000-step tree; returns the free boundary.
- `lewis_call(cf, S0, K, T)` — Lewis's integral. Test: equals COS for Heston to 1e-8.
- `mlae(a, powers, shots, seed)` — simulated maximum-likelihood amplitude estimation with local grid refinement. Test:
  RMSE at the largest schedule below MC's at equal calls.
- `chebyshev2d(f, box, n)` and its evaluator. Test: reproduces a bivariate polynomial of degree < n exactly.
Optional: `parallel_price(n_workers)` lives in `compute.py`, not the House (machine-specific).

**Data:** none needed. All products are textbook cases with exact or near-exact references; no `data/manifest.json`
change. The only cross-part read is Part 17's `stopping` result.

**3D scenes:** `ThreeDScene` with `VoiceoverScene` as in `quant12/s01_hook.py`; text via `add_fixed_in_frame_mobjects`;
reset the camera after each block; surfaces via `price_surface` in `explainer/quant/viz.py`.

**Branches the narration must compute, not assume:** the 95% coverage (ch1); the stratified/LHS ratios (ch3); CE vs
variance optimum (ch4); PCA vs bridge in the QMC spread (ch6); Milstein-MLMC cost slope (ch7); TvR's bias sign and the
basis sweep's plateau (ch8); Bermudan reference inside the bounds; LSM vs Part 17's network on the max-call (ch9 —
planning run says LSM ≥ network); AAD/bump ratios (ch11, machine-dependent: quote the proxy too); PSOR vs penalty speed
(ch13); CM error vs α (ch15); MC-with-control in the race (ch16); speed-up bars (ch17); QAE slope (ch18).

**Chinese:** new terms for `QUANT_ZH_GUIDE.md`: 控制变量 (control variate), 对偶变量 (antithetic variates), 分层抽样
(stratified sampling), 拉丁超立方 (Latin hypercube), 交叉熵法 (cross-entropy method), 有效样本量 (effective sample size),
差异度 (discrepancy), 有效维数 (effective dimension), 布朗桥 (Brownian bridge), 多层蒙特卡洛 (MLMC), 对偶上界 (dual
upper bound), 伴随算法微分 (AAD), 检查点 (checkpointing), 线性互补问题 (LCP), 罚函数法 (penalty method), 交替方向隐式
(ADI), 余弦展开法 (COS method), 振幅估计 (amplitude estimation), 逻辑量子比特 (logical qubit), 切比雪夫插值 (Chebyshev
interpolation).

**README:** chapter list with minutes; the textbook-audit table of §2(b); the full paper list (READING.md Part 16 plus
the additions of §2(c) and §4); 4 desk questions and 8 problems with solutions in English and Chinese; the
build command; a note that wall-clock numbers are machine-specific.

**Risks:**
- Length: the plan's chapters sum above 60 at 3 min each; write to 2.7. If short, ch17 and ch19 absorb cards.
- Timing experiments (`aad_scale`, `parallel`, `race`) on a shared, loaded 4-core machine are noisy (the planning AAD
  run varied 2–10× between adjacent sizes). Use best-of-N, a quiet window, and a deterministic proxy; never narrate a
  single noisy ratio.
- The PSOR in `fd_american_put` is a pure-Python double loop; at 400 × 400 it is slow (minutes). Keep 200–300 for
  display, or switch the displayed number to the penalty solver.
- `maxcall` evaluation with 400,000 paths × 9 dates × 5 assets needs ≈ 150 MB; chunk it.
- The London Whale card must quote the Task Force report itself, not secondary sources; if not fetched, drop the
  quote and keep a one-line pointer to Part 20.
- Overlap with Part 5 (MLMC, IS) and Part 17 (stopping): keep Part 16's angle (theorem, optimal shift, LSM baseline)
  and say "Part 5 showed…/Part 17 trains…" in one line each.
- `quant16` is cited in `IMPLEMENT.md` as an exemplar of a rich finished part; once expanded it should stay one.

## 7. Lead's decisions (2 Nov 2026)

1. Accepted: `s11_house` leaves the manifest (its table becomes the industry chapter's validation report, its rule moves to the outro); new modules slot in between kept ones.
2. London Whale as a one-card crisis pointing to Part 20 — only if the JPMorgan Task Force report (2013) itself is fetched and quoted; otherwise drop it.
3. Split confirmed: Part 16 owns the MLMC complexity proof, optimal-shift theory, Milstein comparison, and the industry chapter (AAD, Danske, STAC-A2, QuantLib, OCC margin engine); Part 5 keeps importance sampling only as a Girsanov application and points forward.
4. The max-call comparison branches on the cached numbers: Longstaff–Schwartz is not beaten by the network on this benchmark; say so.
5. Accepted: 15 new `engine.py` functions with tests; `mlmc` gains options whose defaults keep cached results.
6. Accepted. Timings: measure in a quiet window and pair with a machine-independent proxy (operation counts).
Also: replace the 25-step "Bermudan" tree number with a proper reference; check the quantum paper body for the 7,500 vs ~8,000 logical-qubit figure and quote what it says.
