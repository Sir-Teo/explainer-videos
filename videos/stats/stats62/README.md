# Statistics, Built — Part 62: Frontiers of Causal Inference

Part 62 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), and the seventh part of Stage V, the research frontier.

It opens with the HIV-CAUSAL Collaboration (Cain et al., *Ann. Intern. Med.* 2011). The question was when to start
combined antiretroviral therapy: as soon as the CD4 count falls below 500, below 350, or below 200? It was answered
from observational data on 20,971 people.
- **The emulation.** Against starting at 500, the hazard ratios for death were 1.01 (0.84–1.22) for 350 and 1.20
  (0.97–1.48) for 200. For AIDS or death they were 1.38 (1.23–1.56) and 1.90 (1.67–2.15).
- **The trial.** INSIGHT START (*NEJM* 2015) randomized 4,685 people with CD4 > 500 to immediate or deferred therapy.
  It was stopped early, with HR 0.43 for serious AIDS and non-AIDS events.

The part asks what can be identified and estimated when the textbook assumptions fail:
- identification theory:
  - clone, censor and weight for regimes;
  - the front door (Pearl 1995) on a simulation, the bow graph's non-identification, and the napkin;
  - the do-calculus and its completeness (Huang & Valtorta; Shpitser & Pearl 2006), the ID algorithm and hedges;
  - Balke–Pearl bounds, and efficient front-door estimation (Fulcher et al. 2020);
- sensitivity and partial identification:
  - Manski's bounds;
  - Tan's (2006) marginal sensitivity model with Zhao, Small & Bhattacharya's (2019) sharp bounds, on LaLonde's NSW
    data against PSID controls, with the bootstrap and benchmarking;
  - Rosenbaum, E-values, Cinelli–Hazlett, and Dorn & Guo;
- proximal causal inference (Miao, Geng & Tchetgen Tchetgen 2018; Tchetgen Tchetgen et al. 2020):
  - the bridge function, proximal 2SLS, and negative controls (Lipsitch et al. 2010);
  - weak proxies, and doubly robust and nonparametric versions (Cui et al. 2023);
- interference (Aronow & Samii 2017):
  - SUTVA's two halves, and exposure mappings on a random geometric network, shown in the new exposure map;
  - vaccine trials' direct and indirect effects (Halloran & Struchiner);
  - cluster and saturation designs, and approximate neighbourhood interference (Leung 2022);
- policy learning (Kitagawa & Tetenov 2018; Athey & Wager 2021):
  - EWM with AIPW scores, and the winner's curse of the in-sample value, with sample splitting as the fix;
  - inference on winners (Andrews, Kitagawa & McCloskey 2024), off-policy evaluation, and policy trees;
- dynamic treatment regimes:
  - the g-formula (Robins 1986), Q-learning on a two-stage SMART (Murphy 2003), and g- and A-learning;
  - target-trial emulation (Hernán & Robins);
- causal discovery:
  - PC (Spirtes & Glymour 1991), Markov equivalence, faithfulness and its fragility (Uhler et al. 2013);
  - LiNGAM, additive noise and equal variances, and interventions (Hauser & Bühlmann 2012);
  - NOTEARS (Zheng et al. 2018) and varsortability (Reisach, Seiler & Weichwald 2021);
- transportability (Bareinboim & Pearl 2016):
  - selection diagrams, inverse-odds and doubly robust transport (Dahabreh et al. 2019), and data fusion;
  - causally interpretable meta-analysis, and Meager's (2019) microcredit sites;
- surrogates:
  - the surrogate paradox (VanderWeele 2013) and CAST, and principal surrogates (Frangakis & Rubin 2002);
  - the surrogate index (Athey, Chetty, Imbens & Kang 2019), valid and with a bypass;
- five open problems.

It keeps two promises:
- **Part 36** assumed every confounder was measured. Chapters 2–3 bound the effect without that assumption and
  replace it with proxies.
- **Part 61** moved distributions without a causal model. Chapter 8 says when an effect itself can be transported.

**Built in this part:**
- **`statkit.frontier`** ([`explainer/stats/kit/frontier.py`](../../../explainer/stats/kit/frontier.py)), tested in
  `tests/test_stats_kit_frontier.py`:
  - the front-door formula and criterion (on statkit.causal's `DAG`);
  - marginal-sensitivity bounds by sorting, checked against brute force;
  - 2SLS with sandwich errors, proximal 2SLS, and the naive adjusted OLS;
  - Aronow–Samii exposures, simulated exposure probabilities, and Hájek contrasts;
  - AIPW scores, threshold EWM, and policy values;
  - two-stage Q-learning;
  - the PC skeleton with Fisher-z tests, random linear SEMs, and varsortability;
  - the surrogate index.
- **The exposure map** (`ExposureMap` in `explainer/stats/viz.py`), the part's instrument. It draws a network
  experiment, with units joined by their links and coloured by their four exposure conditions, so spillovers can be
  seen in the design.

**Data.**
- From the Museum: LaLonde's NSW data (the Dehejia–Wahba treated men, the experimental controls as a benchmark, and
  the PSID comparison group), and CAST's deaths.
- The HIV-CAUSAL and START numbers are quoted from the papers.
- The rest is seeded simulation.

The Coverage Board gains four rows:

| Method | Setting | Nominal | Achieved | Verdict |
|---|---|---|---|---|
| OLS adjusting for both proxies | hidden confounder, n = 1,000 | 95% | 0.0% | broken |
| Proximal 2SLS | hidden confounder, n = 1,000 | 95% | 95.3% | kept |
| Policy value, learned and evaluated in-sample | EWM, AIPW scores, n = 400 | 95% | 80.9% | broken |
| Policy value, learned on one half, evaluated on the other | EWM, AIPW scores, n = 400 | 95% | 95.3% | kept |

## Build it

```bash
OMP_NUM_THREADS=1 python -m videos.stats.stats62.compute   # once (under a minute)
python tools/build.py stats62 -q l                         # fast 480p preview
python tools/build.py stats62                              # 1080p30 -> renders/stats62.mp4
python tools/qa_scene.py stats62 Sensitivity
python tools/lecture_length.py stats62 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | When to start | HIV-CAUSAL: HR (vs 500) 1.01, 1.20 for death; 1.38, 1.90 for AIDS or death; START: HR 0.43 |
| 1 | Identification | 20,000 units, hidden binary U: naive 2.83, front door 1.01, truth 1 |
| 2 | Sensitivity | NSW: experiment 1,794; 185 treated vs 429 PSID: raw −635, IPW −342; sharp bounds (−1,302, 643) at Λ = 1.25, (−2,060, 1,474) at 1.5, (−2,679, 2,195) at 1.75; zero reached at Λ ≈ 1.09, the experiment at Λ ≈ 1.61 |
| 3 | Proximal | 600 samples of 1,000: naive mean 1.81, 95% coverage 0%; proximal mean 1.02 (sd 0.18), coverage 95.3% |
| 4 | Interference | 400 units, mean degree 4.3, p = 0.3, 300 assignments: direct 1.98 ± 0.30 (truth 2), spillover 1.01 ± 0.19 (truth 1), naive 2.00 ± 0.14 |
| 5 | Policy | τ(x) = 0.25x − 0.1, n = 400, 800 samples: best gain 0.0225; in-sample bias +0.073, coverage 80.9%; split coverage 95.3%, bias −0.0001 |
| 6 | Regimes | two-stage SMART, n = 1,000: values never 0.00, always −0.21, stage 2 only 0.35, Q-learning 0.87, true thresholds 0.89 |
| 7 | Discovery | 30 random 10-node SEMs: PC recall 0.81, precision 0.85; varsortability 0.97 raw, 0.47 standardized; cancelling paths: corr −0.011 |
| 8 | Transport | 200 trials, mean age 34 vs target 50: trial 0.69 (sd 0.09), transported 1.51 (sd 0.20; ESS ≈ 203 of 743), truth 1.49 |
| 9 | Surrogates | valid: index 1.64 ± 0.12 vs truth 1.55; bypass: 1.58 ± 0.12 vs truth 0.55 |
| 10 | Open problems | — |
| 11 | Outro | — |

## Sources

- **The hook.** HIV-CAUSAL Collaboration (L. Cain et al.), *Ann. Intern. Med.* 154 (2011); INSIGHT START Study Group,
  *NEJM* 373 (2015).
- **Identification.**
  - J. Pearl, *Biometrika* 82 (1995); J. Tian & J. Pearl, AAAI (2002);
  - Y. Huang & M. Valtorta, AAAI (2006); I. Shpitser & J. Pearl, AAAI (2006);
  - A. Balke & J. Pearl, *JASA* 92 (1997);
  - I. Fulcher, I. Shpitser, S. Marealle & E. Tchetgen Tchetgen, *JRSS B* 82 (2020);
  - J. Pearl & D. Mackenzie, *The Book of Why* (2018).
- **Sensitivity.**
  - C. Manski (1990); Z. Tan, *JASA* 101 (2006); Q. Zhao, D. Small & B. Bhattacharya, *JRSS B* 81 (2019);
  - J. Dorn & K. Guo, *JASA* 118 (2023); C. Cinelli & C. Hazlett, *JRSS B* 82 (2020);
  - T. VanderWeele & P. Ding, *Ann. Intern. Med.* 167 (2017);
  - R. LaLonde, *AER* 76 (1986); R. Dehejia & S. Wahba, *JASA* 94 (1999).
- **Proximal.**
  - W. Miao, Z. Geng & E. Tchetgen Tchetgen, *Biometrika* 105 (2018);
  - E. Tchetgen Tchetgen, A. Ying, Y. Cui, X. Shi & W. Miao, arXiv:2009.10982 (2020);
  - Y. Cui, H. Pu, X. Shi, W. Miao & E. Tchetgen Tchetgen, *JASA* (2023);
  - M. Lipsitch, E. Tchetgen Tchetgen & T. Cohen, *Epidemiology* 21 (2010).
- **Interference.**
  - P. Aronow & C. Samii, *Ann. Appl. Stat.* 11 (2017); M. Leung, *Econometrica* 90 (2022);
  - M. E. Halloran & C. Struchiner, *Epidemiology* (1991, 1995); M. Hudgens & M. E. Halloran, *JASA* 103 (2008);
  - J. Ugander et al., KDD (2013); S. Baird et al., *REStat* 100 (2018); M. Ali et al., *Lancet* 366 (2005).
- **Policy learning.**
  - T. Kitagawa & A. Tetenov, *Econometrica* 86 (2018); S. Athey & S. Wager, *Econometrica* 89 (2021);
  - I. Andrews, T. Kitagawa & A. McCloskey, *QJE* 139 (2024); M. Dudík, J. Langford & L. Li, ICML (2011).
- **Regimes.**
  - J. Robins, *Math. Modelling* 7 (1986) and (2004); S. Murphy, *JRSS B* 65 (2003) and *Stat. Med.* 24 (2005);
  - M. Hernán & J. Robins, *Am. J. Epidemiol.* 183 (2016).
- **Discovery.**
  - P. Spirtes & C. Glymour, *Soc. Sci. Comput. Rev.* 9 (1991); T. Verma & J. Pearl (1990);
  - C. Uhler, G. Raskutti, P. Bühlmann & B. Yu, *Ann. Stat.* 41 (2013);
  - S. Shimizu et al., *JMLR* 7 (2006); P. Hoyer et al., NeurIPS (2009); J. Peters & P. Bühlmann, *Biometrika* 101 (2014);
  - A. Hauser & P. Bühlmann, *JMLR* 13 (2012); X. Zheng et al., NeurIPS (2018);
  - A. Reisach, C. Seiler & S. Weichwald, NeurIPS (2021); J. Robins et al., *Biometrika* 90 (2003).
- **Transport.**
  - J. Pearl & E. Bareinboim, AAAI (2011); E. Bareinboim & J. Pearl, *PNAS* 113 (2016);
  - I. Dahabreh et al., *Biometrics* 75 (2019) and *Stat. Med.* (2020); D. Westreich et al., *Am. J. Epidemiol.* (2017);
  - N. Kallus, A. Puli & U. Shalit, NeurIPS (2018); R. Meager, *AEJ: Applied* 11 (2019).
- **Surrogates.**
  - R. Prentice, *Stat. Med.* 8 (1989); T. VanderWeele, *Biometrics* 69 (2013);
  - C. Frangakis & D. Rubin, *Biometrics* 58 (2002);
  - S. Athey, R. Chetty, G. Imbens & H. Kang, NBER Working Paper 26463 (2019);
  - D. Echt et al., *NEJM* 324 (1991).
- **Open problems.** V. Veitch, D. Sridhar & D. Blei, UAI (2020); B. Schölkopf et al., *Proc. IEEE* 109 (2021).

## Problems and solutions

1. **The front door from two back doors.**
   - A → M is unconfounded, so P(m | do(a)) = P(m | a).
   - For M → Y, A blocks the back door M ← A ← U → Y, so P(y | do(m)) = Σ_{a′} P(y | m, a′)P(a′).
   - Since M intercepts every directed path, P(y | do(a)) = Σ_m P(m | do(a)) P(y | do(m)), which gives the formula.
2. **The weight box.**
   - Write the true weight as 1/e(x, u) = 1 + (1 − e(x, u))/e(x, u), that is, one plus the odds against treatment.
   - The model bounds those odds between Λ⁻¹ and Λ times (1 − e(x))/e(x), so the weight lies in
     [1 + (1/e − 1)/Λ, 1 + (1/e − 1)Λ].
3. **Proximal 2SLS.**
   - With Y = b₀ + b_A A + γU + ε and W = U + η, write Y = b₀ + b_A A + γW + (ε − γη).
   - The instruments (1, A, Z) are uncorrelated with ε − γη, because Z and A are independent of η given U, and of ε.
   - They are correlated with W through U. So the moment conditions hold and 2SLS is consistent for (b₀, b_A, γ).
4. **Naive difference under Bernoulli assignment.**
   - E[Y | z_i = 1] − E[Y | z_i = 0] = 2 + (P(nb treated | z_i = 1) − P(nb treated | z_i = 0)) × 1.
   - Under independent assignment the two probabilities are equal, so the naive difference estimates the direct effect
     2 and is silent about the spillover.
5. **The winner's curse.**
   - For every π, V̂(π) ≤ max_{π′} V̂(π′). Take expectations: V(π) = E V̂(π) ≤ E max V̂.
   - Maximizing over π gives max V ≤ E max V̂. The gap E[V̂(π̂)] − V(π̂) is positive whenever estimation noise
     affects which π wins.
6. **Inverse odds.**
   - With p(x) = P(trial | x), the trial density is f_T(x) ∝ p(x)f(x) and the target density is f_G(x) ∝ (1 − p(x))f(x).
   - So f_G/f_T ∝ (1 − p)/p, and weighting trial units by the odds reproduces the target's covariate law.

## Glossary

- **Identification.** Identification; back door; front door; do-calculus; completeness; ID algorithm; c-component;
  hedge; bow graph; napkin.
- **Bounds and proxies.**
  - Partial identification; Manski bounds; Balke–Pearl bounds.
  - Marginal sensitivity model; Λ; benchmarking.
  - Proximal inference; bridge function; negative control.
- **Beyond SUTVA.** Interference; exposure mapping; direct and spillover effects; versions of treatment; saturation
  design.
- **Decisions.**
  - Policy; value; regret; EWM; winner's curse; off-policy evaluation.
  - Dynamic regime; g-formula; Q-learning; g-estimation; SMART; target trial; clone–censor–weight.
- **Graphs and populations.**
  - PC algorithm; Markov equivalence; faithfulness; LiNGAM; NOTEARS; varsortability.
  - Selection diagram; transportability; data fusion.
  - Surrogate; surrogate paradox; principal surrogate; surrogate index.

## Where it comes back

- **Part 63**: fair treatment rules and counterfactual fairness.
- **Part 64**: causal questions about AI systems; learned adjustment sets.
- **Part 65**: the dissertation's causal chapter.
