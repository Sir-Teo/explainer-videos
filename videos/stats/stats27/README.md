# Statistics, Built — Part 27: Bayesian Computation

Part 27 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the seventh part of Stage III, Master's. Part 26 integrated over one
hyperparameter on a grid. This part computes posteriors no grid can reach:
- importance sampling, Metropolis–Hastings, Gibbs, and Hamiltonian Monte Carlo with NUTS;
- the diagnostics that say whether a run worked, and the reparametrization that fixes Neal's funnel;
- particle methods, variational inference, Laplace and INLA, likelihood-free inference, and exact sampling.

Its centrepiece is `statkit.ppl`, a small probabilistic programming language built on *AI, Built*'s automatic
differentiation and checked against closed-form answers.

It opens with Metropolis, the Rosenbluths and the Tellers' hard disks (1953). Forty disks, uniform proposals, and
overlapping moves rejected: 36% of moves accepted, and the lattice melts. Then a random walk on a curved posterior
accepts 53% of its proposals.

From there the part covers:
- **Importance sampling.**
  - The self-normalized estimator; Kish's ESS. Estimating E x² = 1 under N(0, 1) from 2,000 draws:

    | Proposal | Estimate | ESS | k̂ |
    |---|---|---|---|
    | N(0, 0.5²) | 1.309 (1.194 after PSIS) | 62 | 0.93 |
    | N(0, 3²) | 1.005 | 912 | −1.59 |
    | t₃ | 1.003 | 1,831 | −1.67 |

  - The optimal proposal: P(X > 3) = 0.00135, with SD 0.00088 naively and 0.000054 from N(3.15, 1), 16 times smaller.
  - Reweighting draws for a new prior or leave-one-out; PSIS and k̂ (Vehtari et al. 2024).
- **Metropolis–Hastings.**
  - The Hastings ratio; detailed balance.
  - Traces at three step sizes in 20 dimensions: accepting 88%, 24% and 0.3%. ESS per iteration peaks near 23%
    acceptance, at about 0.0165 (Roberts, Gelman & Gilks 1997).
  - Scaling with dimension; MALA (0.574).
- **Gibbs.**
  - Full conditionals. The zigzag at ρ = 0.95 gives ESS 33 from 2,000 sweeps.
  - Albert & Chib's probit by data augmentation on Bliss's 481 beetles: slope 19.80 (SD 1.51) against the MLE 19.73 (SE 1.48).
    ESS 226 from 2,500.
  - Blocking, collapsing and reparametrizing; BUGS.
- **Diagnostics.**
  - ESS and MCSE; rank-normalized split R̂ (Vehtari et al. 2021).
  - A bimodal target: stuck chains give R̂ 1.53, ESS 7, mean −2.0. Mixing chains give R̂ 1.008, ESS 631.
  - Rank plots; warmup, thinning, MCSE.
- **Hamiltonian Monte Carlo.**
  - Hamilton's equations; leapfrog. On a spring, Euler's energy grows from 0.5 to 88 in 60 steps, while leapfrog's error
    stays below 0.011.
  - The puck on the surface: 25-step trajectories on a correlation-0.9 normal, all accepted.
  - Neal's 100-dimensional normal: 6.3 effective draws per 1,000 gradients against the random walk's 0.045 per 1,000
    evaluations, about 140 times better.
  - Tuning ε, L and the mass matrix; Riemannian HMC.
- **NUTS.**
  - The U-turn criterion. Three trajectories on a correlation-0.95 normal take 7, 15 and 7 leapfrog steps.
  - Stan's warmup (dual averaging; windowed diagonal metric).
  - The eight schools, non-centred: mostly depth 3, 8.4 steps on average, ε 0.59, R̂(log τ) 1.002, ESS 1,830, no
    divergences.
  - Divergences; discrete parameters marginalized.
- **Neal's funnel and the eight schools.**
  - The funnel. Centred NUTS never enters the neck: the 5% point of v is −2.12 against the true −4.93, with one
    divergence. Non-centred gives −4.98.
  - The eight schools, τ ~ half-Cauchy(5), μ ~ N(0, 5²), against the exact grid (5% point 0.24, median 2.74):

    | Form | Divergences | R̂ | ESS | 5% point of τ | Gradients |
    |---|---|---|---|---|---|
    | centred, δ = 0.8 | 47 | 1.049 | 60 | 0.90 | 154,706 |
    | centred, δ = 0.99 | 4 | 1.056 | 75 | 0.55 | 496,566 |
    | non-centred | 0 | 1.003 | 1,909 | 0.25 | 78,473 |

  - QR and scale reparametrizations; centring vs non-centring by data strength (Papaspiliopoulos, Roberts & Sköld
    2007).
- **A probabilistic programming language.**
  - Models as log densities; autodiff; transforms and Jacobians.
  - The twelve-line eight schools model. Checks against closed forms: a normal mean, a proportion, a Poisson rate, and
    the eight schools' median τ and E θ_A, each within Monte Carlo error.
  - Debugging; Stan, PyMC, NumPyro, Turing.
- **Sequential Monte Carlo.**
  - The bootstrap particle filter tracks the Kalman filter on a 60-step local-level series.
  - Log-likelihood estimates: SD 1.20, 0.66 and 0.21 for 50, 200 and 1,000 particles (exact −110.41).
  - Degeneracy; particle MCMC.
  - Tempered SMC evidence for polynomial degrees 1–4 within 0.15 of the exact values, in 5–7 rungs.
- **Variational inference.**
  - The ELBO; reverse KL.
  - Mean-field on a correlation-0.9 normal: SDs 0.41 and 0.37 against 1.
  - CAVI for a normal sample: SD(μ) 0.276 against the exact 0.289.
  - ADVI on the eight schools: τ's 90% interval [0.65, 6.66] against NUTS's [0.26, 10.3]; k̂ 0.62.
  - Full-rank, flows, EP.
- **Laplace and INLA.**
  - A logistic slope with n = 20: the 95% point is 5.55 by NUTS and 4.77 by Laplace. At n = 400 they agree (2.18,
    2.14).
  - Laplace for the evidence; INLA (Rue, Martino & Chopin 2009); a guide to every method.
- **Likelihood-free.**
  - Rejection ABC for a Poisson rate (exact posterior mean 2.56, SD 0.40). With the sufficient mean, ε = 0.05 gives
    2.58 (SD 0.41), keeping 1 simulation in 79. With the median, it gives 2.10 (SD 0.49): shifted, not just wider.
  - ABC-MCMC and ABC-SMC; regression ABC, synthetic likelihood, neural posterior estimation.
  - The Board.
- **Exact sampling.**
  - Coupling from the past (Propp & Wilson 1996) for a 16 × 16 Ising model: coalescence from T = 32 at β = 0.3, and
    T = 128 at β = 0.42, near the critical point.
  - Unbiased MCMC with couplings (Jacob, O'Leary & Atchadé 2020).

Every number on screen is computed in [`compute.py`](compute.py):
- the eight schools and Bliss's beetles are the Museum's;
- the doctor-visit and polynomial data reuse Parts 24 and 26;
- the rest are seeded simulations.

**Built in this part:**
- **`statkit.ppl`** ([`explainer/stats/kit/ppl.py`](../../../explainer/stats/kit/ppl.py)), checked in
  `tests/test_stats_kit_ppl.py`:
  - **Models:** `Model` (real/positive/unit supports with Jacobians), with log densities on autodiff Tensors.
  - **Samplers:**
    - leapfrog, HMC, and NUTS with Stan-style warmup;
    - random-walk Metropolis;
    - Albert–Chib Gibbs.
  - **Diagnostics:** rank-normalized split R̂; bulk, tail and basic ESS; PSIS with k̂.
  - **Approximations:** mean-field ADVI with its PSIS check; tempered SMC; the bootstrap particle filter and the Kalman
    filter; rejection ABC.
  - **Exact sampling:** coupling from the past for the Ising model.
- **`statkit.bayes`**: `hier_normal` now takes a normal prior on μ.
- **The puck on the surface** (`PuckSurface` in `explainer/stats/viz.py`): an oblique wireframe of −log π, with
  trajectories drawn on it.

The Coverage Board gains four rows: simulation-based coverage of 90% intervals for the eight schools' effects. Truths
are drawn from the prior (μ ~ N(0, 5²), τ ~ half-Cauchy(5)), 100 simulated data sets, 8 schools each.

| Method | Setting | Reps | Achieved | Verdict |
|---|---|---|---|---|
| exact grid draws | eight schools, truths from the prior | 800 | 90.5% | kept |
| NUTS, non-centred | eight schools, truths from the prior | 800 | 90.9% | kept |
| NUTS, centred | eight schools, truths from the prior | 800 | 91.0% | kept |
| mean-field ADVI | eight schools, truths from the prior | 800 | 87.5% | kept (short, within the margin) |

Calibration averaged over the prior can pass while a particular data set's answer is biased. The centred sampler's
error at small τ (chapter seven) barely moves the schools' coverage.

## Build it

```bash
python -m videos.stats.stats27.compute         # once (about an hour: the Board runs NUTS 200 times)
python tools/build.py stats27 -q l             # fast 480p preview
python tools/build.py stats27                  # 1080p30 -> renders/stats27.mp4
python tools/qa_scene.py stats27 Funnel
python tools/lecture_length.py stats27 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Hard disks, 1953 | 36% of moves accepted; 53% on the banana |
| 1 | Importance sampling | 1.309 with k̂ 0.93; tail SD 16× smaller |
| 2 | Metropolis–Hastings | 88 / 24 / 0.3% acceptance; peak near 0.23 |
| 3 | Gibbs sampling | ESS 33 of 2,000; probit slope 19.80 vs 19.73 |
| 4 | Diagnostics | R̂ 1.53 (stuck) vs 1.008 |
| 5 | Hamiltonian Monte Carlo | Euler 0.5 → 88; leapfrog ±0.011; 140× in 100-D |
| 6 | NUTS | 7 / 15 / 7 steps; ε 0.59; ESS 1,830 |
| 7 | Neal's funnel and the eight schools | v: −2.12 vs −4.93; τ 5%: 0.90 / 0.55 / 0.25 vs 0.24 |
| 8 | A probabilistic programming language | all checks within Monte Carlo error |
| 9 | Sequential Monte Carlo | log-lik SD 1.20 / 0.66 / 0.21; evidence within 0.15 |
| 10 | Variational inference | SD 0.41 vs 1; τ [0.65, 6.66] vs [0.26, 10.3]; k̂ 0.62 |
| 11 | Laplace and INLA | 95% point 5.55 vs 4.77 (n = 20); 2.18 vs 2.14 (n = 400) |
| 12 | Likelihood-free inference | mean summary 2.58; median summary 2.10 vs exact 2.56 |
| 13 | Exact sampling | T = 32 (β 0.3), 128 (β 0.42) |
| 14 | Outro | — |

## Sources

- **History.**
  - N. Metropolis, A. Rosenbluth, M. Rosenbluth, A. Teller & E. Teller, *J. Chem. Phys.* 21 (1953).
  - W. Hastings, *Biometrika* 57 (1970).
  - S. Geman & D. Geman, *IEEE PAMI* 6 (1984); A. Gelfand & A. Smith, *JASA* 85 (1990).
  - S. Duane, A. Kennedy, B. Pendleton & D. Roweth, *Physics Letters B* 195 (1987).
- **Sampling.**
  - G. Roberts, A. Gelman & W. Gilks, *Ann. Appl. Prob.* 7 (1997); G. Roberts & J. Rosenthal, *JRSS B* 60 (1998).
  - J. Albert & S. Chib, *JASA* 88 (1993); M. Tanner & W. Wong, *JASA* 82 (1987); J. Liu, *JASA* 89 (1994).
  - R. Neal, *Ann. Stat.* 31 (2003) and in the *Handbook of MCMC* (2011); M. Hoffman & A. Gelman, *JMLR* 15 (2014).
  - M. Girolami & B. Calderhead, *JRSS B* 73 (2011); O. Papaspiliopoulos, G. Roberts & M. Sköld, *Stat. Sci.* 22 (2007).
- **Diagnostics.**
  - A. Gelman & D. Rubin, *Stat. Sci.* 7 (1992).
  - A. Vehtari, A. Gelman, D. Simpson, B. Carpenter & P.-C. Bürkner, *Bayesian Analysis* 16 (2021).
  - A. Vehtari, D. Simpson, A. Gelman, Y. Yao & J. Gabry, *JMLR* 25 (2024).
  - J. Zhang & M. Stephens, *Technometrics* 51 (2009); W. Link & M. Eaton, *Methods Ecol. Evol.* 3 (2012).
- **SMC.**
  - N. Gordon, D. Salmond & A. Smith, *IEE Proc. F* 140 (1993); P. Del Moral, A. Doucet & A. Jasra, *JRSS B* 68 (2006).
  - C. Andrieu & G. Roberts, *Ann. Stat.* 37 (2009); C. Andrieu, A. Doucet & R. Holenstein, *JRSS B* 72 (2010).
  - T. Bengtsson, P. Bickel & B. Li (2008).
- **Approximations.**
  - M. Jordan, Z. Ghahramani, T. Jaakkola & L. Saul, *Machine Learning* 37 (1999); D. Blei, A. Kucukelbir &
    J. McAuliffe, *JASA* 112 (2017).
  - A. Kucukelbir, D. Tran, R. Ranganath, A. Gelman & D. Blei, *JMLR* 18 (2017); Y. Yao, A. Vehtari, D. Simpson &
    A. Gelman, *ICML* (2018).
  - D. Rezende & S. Mohamed, *ICML* (2015); T. Minka, *UAI* (2001).
  - H. Rue, S. Martino & N. Chopin, *JRSS B* 71 (2009).
- **Likelihood-free.**
  - J. Pritchard et al., *Mol. Biol. Evol.* 16 (1999); M. Beaumont, W. Zhang & D. Balding, *Genetics* 162 (2002).
  - P. Marjoram et al., *PNAS* 100 (2003); S. Sisson, Y. Fan & M. Tanaka, *PNAS* 104 (2007); S. Wood, *Nature* 466
    (2010).
- **Exact sampling.** J. Propp & D. Wilson, *Random Structures & Algorithms* 9 (1996); P. Jacob, J. O'Leary &
  Y. Atchadé, *JRSS B* 82 (2020).
- **Software.** B. Carpenter et al., *J. Stat. Software* 76 (2017).
- **Books.**
  - C. Robert & G. Casella, *Monte Carlo Statistical Methods* (2nd ed., 2004).
  - S. Brooks, A. Gelman, G. Jones & X.-L. Meng (eds.), *Handbook of Markov Chain Monte Carlo* (2011).
  - A. Doucet, N. de Freitas & N. Gordon (eds.), *Sequential Monte Carlo Methods in Practice* (2001).
  - C. Bishop, *Pattern Recognition and Machine Learning* (2006), chapter 10.

## Problems and solutions

**1. Detailed balance for Metropolis–Hastings.**

*Solution.* For x′ ≠ x the kernel density is K(x → x′) = q(x′ | x) α(x, x′). Then
π(x) q(x′ | x) α(x, x′) = min{π(x) q(x′ | x), π(x′) q(x | x′)}. This is symmetric in (x, x′), so it equals
π(x′) K(x′ → x). The rejection mass sits at x′ = x, where balance is trivial. Integrating over x gives
∫ π(x) K(x → x′) dx = π(x′): π is stationary.

**2. Self-normalized importance sampling.**

*Solution.* By the law of large numbers, (1/n)Σ w_s f(x_s) → E_q(wf) = c E_π f and (1/n)Σ w_s → E_q w = c, where c is
π's unknown normalizing constant. The ratio therefore converges to E_π f (Slutsky). If q = π up to the constant, every
w_s is equal, and (Σ w)²/Σ w² = n.

**3. Gibbs on a correlated normal.**

*Solution.* x₁ | x₂ ~ N(ρx₂, 1 − ρ²) and x₂ | x₁ ~ N(ρx₁, 1 − ρ²). Over one sweep,
x₁^{(t+1)} = ρ x₂^{(t)} + e and x₂^{(t)} = ρ x₁^{(t)} + e′, so x₁^{(t+1)} = ρ² x₁^{(t)} + (noise). That is an AR(1) with
φ = ρ², whose ESS per draw is (1 − φ)/(1 + φ) = (1 − ρ²)/(1 + ρ²). For ρ = 0.95 this is 0.051, about 100 from 2,000,
the right order for the 33 seen (the chain starts far out).

**4. Leapfrog preserves volume and is reversible.**

*Solution.* Each of the three substeps is a shear: (q, p) ↦ (q, p − (ε/2)∇U(q)) changes p by a function of q only, so its
Jacobian is unit triangular with determinant 1; likewise q ↦ q + εM⁻¹p. A composition of shears preserves volume.
Reversibility: apply a step from (q′, p′) with momentum negated. The first half-kick undoes the last, the drift undoes
the drift, and the final half-kick undoes the first. You arrive at (q, −p).

**5. The ELBO identity.**

*Solution.* log p(y) = E_q log p(y) = E_q log{p(y, θ)/p(θ | y)}. Write
log p(y, θ)/p(θ | y) = log{p(y, θ)/q(θ)} + log{q(θ)/p(θ | y)}, and take expectations under q. The result is
ELBO + KL(q ‖ p(θ | y)). Since KL ≥ 0, the ELBO is a lower bound, tight when q is the posterior.

**6. The log transform's Jacobian.**

*Solution.* For u = log τ, P(U ≤ u) = P(τ ≤ e^u), and differentiating gives p_U(u) = p_τ(e^u) e^u. So on the
unconstrained scale the log density gains the term log|dτ/du| = u. That is exactly what `Model` adds for a "positive"
parameter.

## Glossary

- **Monte Carlo; ergodic theorem; MCSE**: averages of draws; their convergence for Markov chains; the error of a
  Monte Carlo average.
- **Importance sampling; self-normalized; Kish's ESS; PSIS; k̂**:
  - weighted draws from a proposal;
  - normalized by the weights' sum;
  - (Σw)²/Σw²;
  - Pareto smoothing of the largest weights;
  - the fitted tail shape, unreliable above 0.7.
- **Markov chain Monte Carlo; Metropolis–Hastings; detailed balance; acceptance rate; MALA**:
  - chains whose limit is the posterior;
  - propose and accept by the Hastings ratio;
  - balanced flows;
  - tuned near 0.234 (RWM) or 0.574 (MALA);
  - Langevin proposals.
- **Gibbs sampling; full conditional; data augmentation; blocking; collapsing**:
  - coordinate-wise exact draws;
  - a parameter's distribution given all others;
  - latent variables that make conditionals easy;
  - updating together;
  - integrating out.
- **R̂; split, rank-normalized; bulk and tail ESS; rank plot; warmup; thinning**: the multi-chain convergence
  diagnostic and its modern form, and the routine of a run.
- **Hamiltonian Monte Carlo; leapfrog; symplectic; mass matrix; divergence**:
  - momentum-driven proposals;
  - the half-kick, drift, half-kick integrator;
  - volume- and structure-preserving;
  - the preconditioner;
  - an exploding energy error.
- **NUTS; U-turn; dual averaging; tree depth**: self-tuning HMC and its parts.
- **Neal's funnel; centred and non-centred parametrizations**: hierarchical geometry, and θ = μ + τz.
- **Probabilistic programming language; automatic differentiation; transform; Jacobian**: models as code, gradients
  by reverse mode, and constrained parameters mapped to ℝ.
- **Particle filter; resampling; degeneracy; pseudo-marginal MCMC; tempered SMC**: sequential importance sampling and
  its uses for likelihoods and evidences.
- **Variational inference; ELBO; KL(q ‖ p); mean field; CAVI; ADVI; normalizing flow; EP**: optimization-based
  approximations and their families.
- **Laplace approximation; INLA**: a normal at the mode; nested Laplace for latent Gaussian models.
- **ABC; summary statistic; tolerance; synthetic likelihood; neural posterior estimation**: likelihood-free
  inference.
- **Coupling from the past; monotone coupling; unbiased MCMC**: exact draws; order-preserving couplings; coupled
  chains for finite-sample unbiasedness.
- **Simulation-based calibration**: rank checks that a computation reproduces the prior on average.

## Where it comes back

| Idea | Returns in |
|---|---|
| PSIS-LOO and WAIC | 28 |
| shrinkage priors by NUTS | 32 |
| Kalman filters and state-space models | 38 |
| Gaussian processes, INLA | 39 |
| multiple imputation by MCMC | 41 |
| Markov chains, mixing times | 44 |
| stochastic approximation | 50 |
| BvM and posterior contraction | 53 |
| the Coverage Board | every part; 65 |
