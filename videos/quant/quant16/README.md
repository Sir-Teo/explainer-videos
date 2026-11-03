# Quant, Built — Part 16: Computing Prices

Part 16 of a forty-three-part series on quantitative finance (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), in Act III, Derivatives. It is the numerical-analysis part: every method a desk uses
to turn a model into a price, with its error rate proved, its algorithm built in the House's code, and all of them
measured on one scoreboard. It covers:

* Monte Carlo's error bar, random numbers and reproducible parallel streams;
* variance reduction: control variates (Kemna–Vorst), antithetics, stratification and Latin hypercubes, importance
  sampling with the optimal shift learned by cross-entropy;
* quasi-Monte Carlo: discrepancy, Koksma–Hlawka, Sobol nets, scrambling; the Brownian bridge, principal components and
  effective dimension;
* multilevel Monte Carlo: Giles's complexity theorem, Euler against Milstein;
* American options: Longstaff–Schwartz run backward on real paths, the duality bound (Rogers; Haugh–Kogan;
  Andersen–Broadie), a proper Bermudan reference, and the five-asset max-call against Part 17's network;
* Greeks by bumps, pathwise and likelihood ratio (and Malliavin weights); adjoint differentiation and its cost;
* finite differences: θ-schemes, von Neumann stability, Lax; Crank–Nicolson's ringing and Rannacher; the American put
  as a linear complementarity problem (PSOR and the penalty method);
* ADI for Heston on non-uniform grids;
* Fourier pricing: Carr–Madan, Lewis, COS, and the race between every method;
* the industry's machines (overnight runs, SIMM and FRTB sensitivities, Danske Bank's AAD, JPMorgan's FPGAs,
  STAC-A2, QuantLib and ORE); quantum amplitude estimation built, simulated and costed; the 2023–2026 frontier.

Every number is computed by the series' own code ([`compute.py`](compute.py), and the House's
[`engine`](../../../explainer/quant/house/engine.py), tested in `tests/test_quant_house.py`) on one CPU core. No market
data are used: the products are textbook cases (Black–Scholes with 20% volatility and 5% rates; Heston with
v₀ = θ = 0.04, κ = 1.5, ξ = 0.5, ρ = −0.7; Broadie–Glasserman's five-asset max-call), so every method can be checked
against an exact or near-exact price.

*An education in methods, not investment advice. Firms and episodes are described from the public record; figures
that come from a firm's or vendor's own account are labelled as such.*

## Chapters (about 59 minutes)

* **One price, many machines** (2.8 min). Four engines race on one Heston call, drawn as the wall clock reaches each
  run; the history from Crank–Nicolson (1947) and Metropolis–Ulam (1949) to quantum resource estimates (2021, 2024);
  the plan; the House's pricing engine.
* **1. Monte Carlo: an average with an error bar** (2.3). Three seeds' running estimates to a million paths with the
  95% funnel; the strong law, the CLT and Slutsky; n(ε) = (1.96σ/ε)²; efficiency = 1/(variance × cost). The payoff's
  standard deviation is 14.7, so ±1 cent at 95% needs about 8.3 million paths; the band covers the true price in 94.4%
  of 1,000 runs. Berry–Esseen. Predict: twice the noise at a quarter of the cost is a draw.
* **2. Random numbers and sample paths** (2.9). Inverse transform drawn live; Box–Muller; the Cholesky shear to
  ρ = −0.7; W = LZ with LLᵀ = min(tᵢ, tⱼ). **Lab:** `brownian_bridge` reproduces the covariance to 6 × 10⁻¹⁷.
  Counter-based streams (Philox): 1,000 paths in shuffled order are bit-identical; KS tests on 10⁶ draws; a Python loop
  is about 740 times slower than numpy.
* **3. Variance reduction: controls, mirrors and strata** (3.1). The regression line rotates and the histogram
  collapses: Kemna–Vorst's geometric control has ρ = 0.9996 and divides the variance by about 1,300 (the stock: 2.8).
  b* and 1 − ρ²; antithetics (call ρ = −0.50; straddle +0.64, worse); stratification (16 strata ÷24, 256 ÷504); Latin
  hypercube on 64 dimensions ÷3.3. **Lab:** `mc_call`'s antithetic and control branches.
* **4. Variance reduction: importance sampling** (2.4). The sampling density slides from θ = 0 to 7 above the
  variance-ratio curve: strike-centred θ = 2.20 gives ÷98, the optimum near 2.75 gives ÷133, θ = 5 only ÷4.6 and
  beyond ~6 worse than nothing (weight degeneracy, ESS). The zero-variance density, the convex second moment,
  cross-entropy (two steps from 0 land between 2.80 and 2.91, then 2.86–2.87), Glasserman–Heidelberger–Shahabuddin.
* **5. Quasi-Monte Carlo: filling space evenly** (3.4). Sixteen Sobol points light every elementary box (a (0,4,2)-net);
  random points leave 4 empty and 4 crowded of 16. Discrepancy, Koksma–Hlawka, (log n)^d/n, van der Corput's digit
  reversal, Joe–Kuo. L2-star discrepancy: slope −0.96 for Sobol in 2D; in 16D at these n neither Sobol nor Halton beats
  random yet. Halton's coordinates 29–30 stripe. Scrambling gives error bars; dropping the first point multiplies the
  error by 3.5 at n = 64 and 45 at n = 4,096 (Owen 2022).
* **6. QMC on paths: the Brownian bridge and effective dimension** (2.9). 3D: what each normal adds to the path,
  step / bridge / PCA; first-normal share of the average's variance 4.6% / 75.6% / 98.6%. The bridge crystallising.
  ANOVA, truncation dimension, Karhunen–Loève. On the 64-fixing Asian at 16,384 paths, spread: pseudo-random 0.049,
  Sobol 0.0127 (stalled), bridge 0.0016, PCA 0.00018 (270× less than random). Paskov–Traub (1995), CMO (1997).
* **7. Multilevel Monte Carlo** (3.6). Coupled fine and coarse paths; the level bars; the complexity theorem proved
  (telescoping, MSE split, Lagrange, the geometric series). **Replay:** the adaptive loop pass by pass at ε = 0.01 (10
  levels; four seeds' costs within 0.3%). **Lab:** `_mlmc_level` (V₀ = 161 → V₁₀ = 0.0018). Cost: 4×, 11× and 26×
  cheaper than standard at ε = 0.04, 0.02, 0.01. European call: β = 0.99 (Euler) against 1.96 (Milstein); ε²·cost from
  ε = 0.04 to 0.005 rises 1,160 → 1,773 for Euler and falls 1,048 → 592 for Milstein. Rhee–Glynn's unbiased version.
* **8. American options I: Longstaff–Schwartz on real paths** (2.8). The regression run backward date by date on the
  House's paths, the boundary traced and compared with the tree's. Snell envelope, L² projection, cash flow not value,
  lower bound. **Replay:** degree 1–5 × 10³–10⁵ fitting paths, 5 seeds: a line plateaus at 5.98; cubics reach the
  Bermudan reference 6.067; with 10³ paths degree 2 is best. On 400,000 fresh paths 6.071 ± 0.011; Tsitsiklis–Van Roy's
  value regression is 6.097 in sample (above the truth).
* **9. American options II: the dual bound, and five assets** (3.4). One outer path with its inner fans and the policy's
  martingale; the duality bound derived; AB's bound falls from 6.41 (50 inner) to 6.075 (1,600); the 5,000-step
  Bermudan tree, 6.067, sits inside [6.061, 6.075]. **Lab:** `andersen_broadie_put`'s outer loop. Five-asset max-call:
  LSM on 2,000,000 fresh paths 25.878 / 26.074 / 26.103 ± 0.014 with 2k / 20k / 200k fitting paths; Part 17's deep
  stopping 26.107 ± 0.020: a statistical tie; Becker–Cheridito–Jentzen's published bounds [26.156, 26.162].
* **10. Greeks three ways** (2.7). 3D: the bump's error over (h, n): a valley with independent numbers (11 at h = 0.01,
  best 0.017), flat 7.5 × 10⁻³ with common numbers. Bump bias–variance, pathwise, likelihood ratio, Malliavin (Fournié et
  al. 1999). Call and digital table; the digital's LR standard error is 3.3 times smaller than the bump's.
* **11. Adjoint differentiation** (2.8). A one-path call's tape forward and backward with real numbers (the series'
  autodiff); Jacobian products, the adjoint recursion, the cheap-gradient principle, Giles–Glasserman, Capriotti.
  **Lab:** `aad_greeks` (five Greeks for 2.2 prices against 7.4 by bumping). Scaling on a basket, 2–128 inputs:
  wall clock (best of several runs, shared machine; at 128 inputs AAD 1.5 prices, central bumps 380) and operation
  counts (backward/forward ≈ 1.2 at every size, so AAD ≈ 2.2 prices). Check-pointing.
* **12. Finite differences I: θ-schemes and stability** (2.7). 3D: the explicit march, stable with 2,000 steps (10.411)
  and exploding with 200 (λ = 2). The θ-scheme, von Neumann's amplification factors live, Lax, the 400-step bound;
  convergence (CN ratio 4.0). Schwartz (1977).
* **13. Finite differences II: ringing, and the American put** (3.1). CN's g → −1 mode flipping sign; the digital's
  gamma ringing and Rannacher's cure. 3D: the American surface with its stopping region and free boundary (S* ≈ 81 a
  year out) over the European. The LCP; PSOR (Cryer 1971) traced sweep by sweep; the penalty method (Forsyth–Vetzal
  2002): 6.0873 on 400 × 400 with two Newton iterations per step; PSOR 200 × 200 6.0789; tree 6.0900. **Lab:**
  `fd_american_put`.
* **14. ADI for Heston** (2.4). 3D: row and column sweeps on the sinh grid, the price surface and its delta, gamma and
  variance sensitivity. Douglas, Craig–Sneyd, in 't Hout–Foulon. Uniform against sinh grids: 2.66 against 0.045 at
  40 × 20 (59×), 0.59 against 0.0019 at 160 × 80.
* **15. Fourier I: Carr–Madan and Lewis** (2.4). The α-damping slider; the transform; the derivation; λη = 2π/N as two
  rulers; Lewis's integral agrees with COS to 12 decimals; CM's error against α plateaus at 1.1 × 10⁻³ (the strike grid).
* **16. Fourier II: the COS method, and the race** (2.8). Heston's density rebuilt by 2 … 128 cosines, coefficients
  decaying exponentially; the derivation; the truncation range (L = 4: 0.12; L = 16: 5 × 10⁻⁸). **Lab:** `cos_price`.
  The race again, with Monte Carlo plus a control variate (variance ÷2.7: the line shifts, the slope stays).
* **17. Industry: the overnight run, GPUs and adjoints** (2.8). Trades × scenarios; SIMM and FRTB sensitivities; Danske
  Bank (Risk.net In-House System of the Year 2015, as reported); JPMorgan and Maxeler (eight hours to under four
  minutes, the bank's and vendor's account; Weston et al. 2012); STAC-A2; QuantLib, ORE, the OCC's STANS. This machine
  (shared, load ≈ 50 on 4 cores): 10⁶ payoffs by a Python loop 3.6 s, numpy 19 ms, float32 2.3 ms; 4 processes no faster
  than one. COS beat Monte Carlo's best accuracy about 14,000 times faster. The nightly validation report.
* **18. Quantum amplitude estimation** (2.9). The Grover rotation in the good/bad plane; the derivation (Rebentrost et al.
  2018, Stamatopoulos et al. 2020, Brassard et al. 2002, Montanaro 2015, Suzuki et al. 2020). **Replay:** the MLAE
  likelihood sharpening; 40 runs: slope −0.94 against −0.5, 33× smaller error than MC at 410,150 calls. Costs:
  Chakrabarti et al. (2021): 8k logical qubits, T-depth 54 million, ~1 s (10 MHz T-gates against ~10 kHz logical clocks
  then estimated); Stamatopoulos–Zeng (2024): 4.7k qubits, 10⁹ T-gates at 45 MHz.
* **19. Frontier: pricing faster, 2023–2026** (2.4). **Replay (3D):** a Chebyshev pricer for Heston over (S₀, v₀),
  error 4 × 10⁻² → 3.7 × 10⁻⁶ from 8 to 32 nodes per axis (1,024 COS calls); a query 0.11 ms against 0.35 ms for COS.
  RQMC median-of-means (Pan–Owen 2023): 2,000× more accurate than the mean at 1,024 points. Junike (2024),
  Bayer–Pelizzari–Schoenmakers (2023), Stamatopoulos–Zeng (2024), Dalzell et al. (2023), Glau–Kressner–Statti (2020).
* **The pricing engine, recap, desk questions, problems** (2.5). Rule 16; the trial counter stays at 310.

## Hands-on

* Labs (real House code, output from the cache): `brownian_bridge` (ch. 2), `mc_call` (3), `_mlmc_level` (7),
  `andersen_broadie_put` (9), `aad_greeks` (11), `fd_american_put` (13), `stochvol.cos_price` (16).
* Replays: cross-entropy learning the IS shift (4), the MLMC adaptive loop (7), LSM backward and the basis × paths sweep
  with seed bands (8), MLAE's likelihood (18), the Chebyshev pricer by node doubling (19).
* 3D: the bridge's coordinates (6), the bump-error valley (10), the explicit march (12), the American surface (13), the
  Heston surface and Greeks (14), the Chebyshev error surface (19).
* New House functions (all in `explainer/quant/house/engine.py`, each tested): `geometric_asian_call`, `asian_control`,
  `stratified_call`, `is_cross_entropy`, `path_matrix`, `variance_captured`, `l2_star_discrepancy`, `mlmc_run`
  (Euler/Milstein, Asian/European, traced), `lsm_put_trace`, `lsm_put_eval`, `bermudan_tree`, `lsm_max_call`,
  `aad_basket`, `fd_american_penalty`, `lewis_call`, `mlae`, `chebyshev2d`/`chebyshev2d_eval`, `heston_adi_grid`.

## Textbook audit

| Book · section | Chapter |
|---|---|
| Glasserman (2003) ch. 1 Foundations (efficiency = variance × work) | 1 |
| Glasserman ch. 2 Generating random numbers and variables (inverse transform, Box–Muller, Cholesky) | 2 |
| Glasserman ch. 3 Sample paths (random walk, Brownian bridge, PCA) | 2, 6 (short rates, jumps, LMM: Parts 5, 13, 19) |
| Glasserman ch. 4 Variance reduction (controls, antithetics, stratification, Latin hypercube, moment matching, importance sampling) | 3, 4 |
| Glasserman ch. 5 Quasi-Monte Carlo (discrepancy, Koksma–Hlawka, van der Corput, Halton, Sobol, nets, randomized QMC, effective dimension) | 5, 6 |
| Glasserman ch. 6 Discretization methods | Part 5 (orders); 7 (MLMC uses them); barrier crossings Part 15 |
| Glasserman ch. 7 Estimating sensitivities (finite differences, pathwise, likelihood ratio) | 10, 11 |
| Glasserman ch. 8 Pricing American options (parametric, random trees, mesh, regression, duality) | 8, 9 |
| Glasserman ch. 9 Applications in risk management | Part 40 (forward line in ch. 4) |
| Savine (2018) Parts I–II (parallel simulation library) | 2, 17 |
| Savine Part III (AAD, tapes, check-pointing) | 11 |
| Andersen–Piterbarg vol. I, finite-difference chapters (θ-schemes, stability, non-uniform grids, ADI) | 12, 13, 14 |
| Andersen–Piterbarg vol. I, Monte Carlo chapter (RNG, QMC, variance reduction, Greeks, regression) | 1–11 |
| Duffy (2006): θ-schemes, CN's oscillations and their fixes, exponential fitting, free boundaries, ADI | 12, 13, 14 |
| Seydel: random numbers, MC for SDEs, FD for standard and American options | 2, 1, 12, 13 (finite elements: named in ch. 12; desks rarely use them for vanillas) |
| Oosterlee–Grzelak (2019): the COS method chapter | 16 |
| Hull, *Options, Futures and Other Derivatives*: numerical procedures (MC, FD; trees in Part 10) | 1, 12 |

## Papers (on screen)

Crank–Nicolson (1947); Metropolis–Ulam (1949); Box–Muller (1958); Sobol (1967); Cryer (1971); Boyle (1977);
Schwartz (1977); Brennan–Schwartz (1978); Rannacher (1984); Craig–Sneyd (1988); Kemna–Vorst (1990); Paskov–Traub
(1995); Broadie–Glasserman (1996; random trees 1997; stochastic mesh 2004); Caflisch–Morokoff–Owen (1997); Rubinstein
(1997, cross-entropy); Glasserman–Heidelberger–Shahabuddin (1999); Fournié–Lasry–Lebuchoux–Lions–Touzi (1999);
Carr–Madan (1999); Longstaff–Schwartz (2001); Tsitsiklis–Van Roy (2001); Lewis (2001); Rogers (2002);
Clément–Lamberton–Protter (2002); Forsyth–Vetzal (2002); Brassard–Høyer–Mosca–Tapp (2002); Andersen–Broadie (2004);
Haugh–Kogan (2004); Giles–Glasserman (2006); Giles (2008); Fang–Oosterlee (2008; Bermudan COS 2009); Joe–Kuo (2008);
Griewank–Walther (2008); in 't Hout–Foulon (2010); Capriotti (2011); Salmon–Moraes–Dror–Shaw (2011, Philox);
Weston–Spooner–Racanière–Mencer (2012); Montanaro (2015); Rhee–Glynn (2015); Gaß–Glau–Mahlstedt–Mair (2018);
Rebentrost–Gupt–Bromley (2018); Becker–Cheridito–Jentzen (2019); Stamatopoulos et al. (2020); Suzuki et al. (2020);
Glau–Kressner–Statti (2020); Chakrabarti et al. (2021); Owen (2022, dropping the first Sobol point); Junike–Pankrashkin
(2022); Pan–Owen (2023); Bayer–Pelizzari–Schoenmakers (2023); Dalzell et al. (2023); Junike (2024);
Stamatopoulos–Zeng (2024).

## Build it

```bash
python -m videos.quant.quant16.compute                    # every number (the longest items take a few minutes each)
EXPLAINER_TTS=silent python tools/qa_scene.py quant16 COS  # one chapter, silent, with a contact sheet
python tools/make.py quant16 --cpu-voice -q m             # English and Chinese, narrated on the CPU
```

## Desk questions, with solutions

1. **How many paths for a price to one basis point?**
   * The 95% half-width is 1.96 σ_Y/√n, so n ≈ (1.96 σ_Y/ε)².
   * For the one-year at-the-money call σ_Y ≈ 14.7, so ±1 cent at 95% needs about 8.3 million plain paths (2.2 million
     for a one-standard-error cent).
   * A control variate with a closed-form twin, stratification or Sobol points with a bridge cut that by one to three
     orders of magnitude. Quote the error with the price.
2. **Why is AAD's cost independent of the number of Greeks?**
   * The price is a composition of elementary operations; reverse mode carries the adjoint ∂V/∂(intermediate) backward
     through the recorded tape, one multiply–add per edge.
   * One sweep yields ∂V/∂x for every input at once: a small constant (here 2.2) times one pricing, for five inputs or
     five thousand. Bumping needs one or two extra pricings per input.
   * The cost is memory: the tape stores the forward pass, so long simulations check-point.
3. **Crank–Nicolson gives the right price for a digital, but the gamma oscillates. Why, and the fix?**
   * CN's amplification factor (1 − 2λs)/(1 + 2λs) tends to −1 for high frequencies when λ is large: those modes flip
     sign each step and barely decay. A payoff with a jump is full of them; differentiating twice magnifies them.
   * Rannacher: start with a few fully implicit (half-)steps (factor 1/(1 + 4λs) → 0), then switch to CN; the scheme
     stays second order.
4. **LSM says 6.06, the dual bound 6.41. What next?**
   * The gap is policy suboptimality plus the inner simulation's upward bias (Jensen: E max(· + noise) ≥ max E).
   * Rerun the dual with more inner paths: here the bound fell from 6.41 (50 inner) to 6.075 (1,600). If the gap
     does not shrink, improve the regression basis (or the fitting paths), and evaluate the policy on fresh paths.

## Problems, with solutions

1. **The optimal control variate.** Var(Y − b(C − EC)) = Var Y − 2b Cov(Y, C) + b² Var C, minimised at
   b* = Cov(Y, C)/Var C; substituting gives Var Y − Cov²/Var C = Var Y (1 − ρ²).
2. **Importance sampling's shift.** Under Z ~ N(θ, 1) the likelihood ratio is φ(z)/φ(z − θ) = exp(−θz + θ²/2), so
   E[f(Z)] = E_θ[f(Z) e^{−θZ + θ²/2}]. Centring on the strike: S₀ exp((r − σ²/2)T + σ√T θ) = K, so
   θ = (ln(K/S₀) − (r − σ²/2)T)/(σ√T) (2.20 for K = 160).
3. **The duality bound.** For a stopping time τ, optional stopping gives E[M_τ] = M₀ = 0, so
   E[h_τ] = E[h_τ − M_τ] ≤ E[max_t (h_t − M_t)]; take the supremum over τ. Equality holds for the martingale part of
   the Snell envelope.
4. **Stability of the explicit scheme.** For u_t = a u_xx, u_j^{n+1} = u_j^n + λ(u_{j+1}^n − 2u_j^n + u_{j−1}^n),
   λ = aΔt/Δx². Substituting u_j^n = g^n e^{ijkΔx}: g = 1 − 4λ sin²(kΔx/2), and |g| ≤ 1 for all k iff λ ≤ ½. For
   Black–Scholes a = σ²S²/2 is largest at S_max: Δt ≤ ΔS²/(σ²S_max²).
5. **Why reverse mode is cheap.** The Jacobian of f(g(h(x))) is J_f J_g J_h. Forward mode multiplies from the right
   carrying n columns (n passes); reverse mode starts from the 1 × m row of a scalar output, so every product is a row:
   a constant multiple of one evaluation (Griewank's cheap gradient principle).
6. **A mixed gamma estimator.** Pathwise delta is Δ = E[g(S_T)] with g(s) = e^{−rT} 1{s > K} s/S₀. Differentiating
   g again would need the derivative of an indicator (a delta function), so differentiate the density of S_T instead
   (score Z/(S₀σ√T)) and keep the explicit 1/S₀: Γ = E[g Z/(S₀σ√T)] − E[g]/S₀
   = E[e^{−rT} 1{S_T > K} (S_T/S₀²)(Z/(σ√T) − 1)].
7. **Multilevel cost when β = γ.** With V_l ∝ M^{−βl} and C_l ∝ M^{γl}, √(V_l C_l) is constant, so
   Σ_{l ≤ L} √(V_l C_l) ∝ L. The bias M^{−αL} ≤ ε/√2 needs L ≈ log(1/ε)/(α log M), so the cost
   2ε^{−2}(Σ√(V_lC_l))² = O(ε^{−2}(log ε)²).
8. **λη = 2π/N.** The FFT computes Σ_j e^{−2πijm/N} x_j. The Carr–Madan sum is Σ_j e^{−iu_jk_m} ψ(u_j)η with
   u_j = jη, k_m = −b + mλ, so e^{−iu_jk_m} = e^{ijηb} e^{−ijmηλ}: matching the kernel needs ηλ = 2π/N.

## Data and reproducibility

* No market data: all products are textbook cases with exact or near-exact references (Black–Scholes formulas,
  Kemna–Vorst's geometric Asian, 2,000-step and 5,000-step trees, COS with 4,096 terms on a wide range).
* Wall-clock times (`race`, `race_cv`, `aad_scale`, `parallel`, `lcp`, `cheb`) are best-of-N on one core of a shared
  build machine, under load; they will differ on other hardware. Where the narration compares costs it also shows
  machine-independent counts (tape operations, pricings, oracle calls).
* Monte Carlo errors are reported as standard errors or root-mean-square errors over repeated seeds.
* `american.bermudan_tree25` (a 25-step tree, 6.146) is no Bermudan reference and is not shown; `bermudan_ref` is.
* Part 17's deep-stopping result is read from `.cache/quant17/stopping.json`, not recomputed.
* No strategy was tested; the trial counter is unchanged at 310.

---

# 量化金融，从零搭建 — 第16部分：计算价格

这是本系列第三幕“衍生品”中讲数值分析的一部分：交易台把模型变成价格的每一种方法，证明它的误差阶，用我们公司的代码搭出算法，
再把所有方法放在同一张记分牌上比较。本部分讲：

* 蒙特卡洛的误差棒、随机数与可复现的并行随机数流；
* 方差缩减：控制变量（Kemna–Vorst）、对偶变量、分层抽样与拉丁超立方、用交叉熵学出最优平移的重要性抽样；
* 拟蒙特卡洛：差异度、Koksma–Hlawka不等式、Sobol网、扰乱；布朗桥、主成分与有效维数；
* 多层蒙特卡洛：Giles的复杂度定理，欧拉格式对米尔斯坦格式；
* 美式期权：在真实路径上倒着运行Longstaff–Schwartz、对偶上界（Rogers；Haugh–Kogan；Andersen–Broadie）、真正的百慕大参考值，
  以及五资产最大值看涨期权与第17部分神经网络的比较；
* 扰动法、路径法与似然比法（以及Malliavin权重）计算希腊字母；伴随算法微分及其成本；
* 有限差分：θ格式、冯·诺依曼稳定性、拉克斯定理；克兰克-尼科尔森的振荡与Rannacher起步；作为线性互补问题的美式看跌期权（PSOR与罚函数法）；
* 非均匀网格上赫斯顿模型的ADI；
* 傅里叶定价：Carr–Madan、Lewis、COS，以及所有方法之间的竞赛；
* 业界的机器（隔夜计算、SIMM与FRTB敏感度、丹斯克银行的AAD、摩根大通的FPGA、STAC-A2、QuantLib与ORE）；量子振幅估计的构造、模拟与成本；2023–2026年的前沿。

所有数字都由本系列自己的代码在一个CPU核上算出。不使用市场数据：产品都是教科书案例，因此每种方法都能与精确或近乎精确的价格核对。

*讲的是方法，不构成投资建议。涉及的公司与事件均依据公开记录；来自公司或供应商自述的数字均已注明。*

## 各章（约59分钟）

* **一个价格，多台机器。** 四台引擎为同一个赫斯顿看涨期权竞赛；从克兰克-尼科尔森（1947）、梅特罗波利斯-乌拉姆（1949）到量子资源估算（2021、2024）的历史；本部分安排；我们公司的定价引擎。
* **1. 蒙特卡洛：带误差棒的平均。** 三个随机种子到一百万条路径的运行估计与95%漏斗；强大数定律、中心极限定理、Slutsky；收益标准差14.7，95%下正负一分钱约需830万条路径；误差带在1000次运行中覆盖真价94.4%。
* **2. 随机数与样本路径。** 逆变换、Box–Muller、Cholesky剪切；**实验**：`brownian_bridge`把协方差复现到6 × 10⁻¹⁷；Philox计数器流乱序计算逐位相同；Python循环比numpy慢约740倍。
* **3. 方差缩减：控制变量、镜像与分层。** Kemna–Vorst几何控制变量ρ = 0.9996，方差缩小约1300倍（股票仅2.8倍）；看涨期权对偶相关−0.50，跨式+0.64；16层÷24，256层÷504；拉丁超立方÷3.3。**实验**：`mc_call`。
* **4. 方差缩减：重要性抽样。** 以行权价为中心÷98，最优约θ = 2.75时÷133，θ = 5仅÷4.6；交叉熵两步学出平移量。
* **5. 拟蒙特卡洛：均匀地填满空间。** 数字网的格子检验；差异度与Koksma–Hlawka；van der Corput；二维中Sobol斜率−0.96；十六维中尚未胜过随机点；Halton第29–30维的条纹；丢掉第一个点使误差在64点时大3.5倍、4096点时大45倍。
* **6. 路径上的拟蒙特卡洛：布朗桥与有效维数。** 第一个正态数的方差份额：逐步4.6%、布朗桥75.6%、主成分98.6%；64维亚式期权上主成分比随机路径离散程度小270倍。
* **7. 多层蒙特卡洛。** 复杂度定理的证明；自适应循环回放（10层，四个种子成本相差0.3%）；**实验**：`_mlmc_level`；ε = 0.01时便宜26倍；欧式看涨期权β：欧拉0.99、米尔斯坦1.96。
* **8. 美式期权（上）。** 倒着运行的回归与边界；基函数次数×路径数扫描；新路径上6.071 ± 0.011；百慕大参考值6.067；TvR样本内6.097偏高。
* **9. 美式期权（下）。** 对偶上界的推导与一条外层路径；上界从6.41降到6.075；五千步百慕大树6.067落在区间内；**实验**：`andersen_broadie_put`；五资产最大值看涨期权：LSM 26.103 ± 0.014，深度停时26.107 ± 0.020，统计上平局。
* **10. 三种方法算希腊字母。** 扰动误差的三维山谷；路径法、似然比法、Malliavin；数字期权上似然比法的标准误差小3.3倍。
* **11. 伴随算法微分。** 一条路径看涨期权的计算带前向与反向；廉价梯度原理；**实验**：`aad_greeks`（2.2次定价对扰动法7.4次）；按输入数的缩放：128个输入时AAD 1.5次定价，中心扰动380次；运算计数显示反向约为前向的1.2倍。
* **12. 有限差分（上）。** 显式格式的三维推进与爆炸；冯·诺依曼放大因子；拉克斯定理；收敛阶。
* **13. 有限差分（下）。** 克兰克-尼科尔森的振荡与Rannacher；美式看跌期权的三维曲面与自由边界；PSOR与罚函数法（6.0873，每步两次牛顿迭代）；**实验**：`fd_american_put`。
* **14. 赫斯顿模型的ADI。** 行列扫描、价格曲面与希腊字母；均匀网格与sinh网格：40 × 20时2.66对0.045。
* **15. 傅里叶方法（上）。** α阻尼滑块；λη = 2π/N；Lewis积分与COS一致到小数点后12位。
* **16. 傅里叶方法（下）。** 余弦重建密度；截断区间；**实验**：`cos_price`；带控制变量的蒙特卡洛重新参赛。
* **17. 业界。** 交易×情景；SIMM与FRTB；丹斯克银行（据Risk.net报道）；摩根大通与Maxeler（据银行与供应商自述，八小时降到四分钟以内）；STAC-A2；QuantLib、ORE、OCC；本机实测（Python循环3.6秒、numpy 19毫秒、float32 2.3毫秒，四个进程并不更快）；夜间验证报告。
* **18. 量子振幅估计。** Grover旋转；最大似然振幅估计回放：斜率−0.94对−0.5；资源估算：8000逻辑量子比特、T深度5400万（2021），4700逻辑量子比特、10⁹个T门、45 MHz（2024）。
* **19. 前沿。** 切比雪夫定价器（32×32节点误差3.7 × 10⁻⁶）；随机化拟蒙特卡洛的中位数（Pan–Owen 2023）；阅读清单。
* **定价引擎、回顾、交易台问题与习题。** 第16条规矩；试验计数器仍为310。

## 交易台问题与解答

1. **要把价格算到一个基点，需要多少条路径？** 95%半宽是1.96 σ_Y/√n，所以n ≈ (1.96 σ_Y/ε)²。一年期平值看涨期权σ_Y ≈ 14.7，正负一分钱约需830万条普通路径（一个标准误差为一分钱时约220万条）。带闭式孪生的控制变量、分层或带布朗桥的Sobol点能把它减少一到三个数量级。报价时要同时报误差。
2. **为什么AAD的成本与希腊字母的个数无关？** 价格是基本运算的复合；反向模式沿记录的计算带把伴随量向后传，每条边一次乘加。一次扫描同时得到对所有输入的导数：一次定价的一个小常数倍（这里2.2倍），无论输入有五个还是五千个。扰动法每个输入要多定价一到两次。代价是内存，长模拟要设检查点。
3. **克兰克-尼科尔森给出数字期权的正确价格，但Gamma振荡。为什么？怎么修？** λ大时，放大因子(1 − 2λs)/(1 + 2λs)对高频趋于−1：这些模式每步变号、几乎不衰减。带跳跃的收益充满这类模式，求两次导数又放大它们。Rannacher：先走几个完全隐式（半）步（因子1/(1 + 4λs)趋于0），再换成克兰克-尼科尔森，格式仍是二阶。
4. **LSM给出6.06，对偶上界6.41。下一步做什么？** 差距是策略的次优性加上内层模拟的向上偏差（Jensen）。先用更多内层路径重算对偶界：这里从6.41（50条）降到6.075（1600条）。如果差距不缩小，再改进回归基函数或拟合路径，并在新路径上评估策略。

## 习题与解答

1. **最优控制变量。** Var(Y − b(C − EC)) = Var Y − 2b Cov(Y, C) + b² Var C，在b* = Cov(Y, C)/Var C处最小；代入得Var Y (1 − ρ²)。
2. **重要性抽样的平移。** Z ~ N(θ, 1)时似然比为exp(−θz + θ²/2)。以行权价为中心：θ = (ln(K/S₀) − (r − σ²/2)T)/(σ√T)（K = 160时为2.20）。
3. **对偶上界。** 由可选停时定理E[M_τ] = 0，所以E[h_τ] = E[h_τ − M_τ] ≤ E[max_t (h_t − M_t)]，再对τ取上确界；取Snell包络的鞅部分时等号成立。
4. **显式格式的稳定性。** 代入u_j^n = g^n e^{ijkΔx}得g = 1 − 4λ sin²(kΔx/2)，对所有k有|g| ≤ 1当且仅当λ ≤ ½；对布莱克-斯科尔斯得Δt ≤ ΔS²/(σ²S_max²)。
5. **为什么反向模式便宜。** 雅可比矩阵J_f J_g J_h：前向模式从右乘，携带n列（n轮）；反向模式从标量输出的行向量开始从左乘，每次乘积都是行向量，成本是一次求值的常数倍。
6. **混合Gamma估计量。** 路径法Delta为e^{−rT} 1{S_T > K} S_T/S₀；它对S₀的导数含有δ函数，所以对剩下的显式依赖改用似然比：Γ = E[e^{−rT} 1{S_T > K} (S_T/S₀²)(Z/(σ√T) − 1)]。
7. **β = γ时多层方法的成本。** √(V_l C_l)为常数，所以和与L成正比；偏差要求L ≈ log(1/ε)/(α log M)，于是成本为O(ε^{−2}(log ε)²)。
8. **λη = 2π/N。** FFT计算Σ_j e^{−2πijm/N} x_j；Carr–Madan的核为e^{−iu_jk_m} = e^{ijηb} e^{−ijmηλ}，要与之匹配必须ηλ = 2π/N。

## 数据与可复现性

* 不使用市场数据；所有产品都有精确或近乎精确的参考价格。
* 墙钟时间在共享且繁忙的构建机器上取多次运行中的最好值，换一台机器会不同；叙述比较成本时同时给出与机器无关的计数。
* `american.bermudan_tree25`（25步二叉树，6.146）不是百慕大参考值，不在画面上使用；`bermudan_ref`才是。
* 第17部分的深度停时结果读取自其缓存，不重新计算。
* 本部分没有测试任何策略；试验计数器仍为310。
