# Psychology, Built: Part 44, Latent Variables

In 1921 the geneticist Sewall Wright drew arrows between variables and showed how their correlations follow from
the arrows. Spearman had already explained correlations by an unseen common factor. In 1969 Karl Jöreskog joined the
two, and the structural equation model became psychology's standard way to state a theory about things nobody
observes. Its standard abuse is to forget that very different diagrams fit the same data.

The viewer meets one correlation matrix and three diagrams that fit it equally well, draws a model for three
stories, and predicts four numbers. Then Wright's tracing rule, derived and written as a matrix; the confirmatory
factor model, identified by counting; maximum likelihood, fitted to Holzinger and Swineford's nine tests and checked
against lavaan; fit, from the chi-square test to the indices and the fixed cut-offs that pass a wrong model
(computed); the full model, which undoes Part 3's attenuation and gives reliability from the loadings; measurement invariance across the two schools;
mediation, and a significant indirect effect that is not there (computed); equivalent models; growth curves and the
cross-lagged panel's confusion of stable people with change (computed); factors against networks (computed); and
eight questions for reading a paper with a path diagram. This part starts Act XI, the graduate toolkit.

## Where the numbers come from

| What | Source |
|---|---|
| The hook and chapter 9: 1,000 simulated people from the chain X → M → Y (paths 0.5 and 0.6); correlations 0.51, 0.56 and 0.28; the chain, its reverse and the fork each give χ² = 0.32 on 1 df; the collider gives 79.3 | Psyche (`sem.markov_equivalent`, the item's own regression), item `equivalent` |
| Holzinger and Swineford's nine tests for 301 children: the three-factor model gives χ² = 85.31 on 24 df, CFI 0.931, TLI 0.896, RMSEA 0.092, SRMR 0.065 (baseline 918.85 on 36); standardized loadings 0.42 to 0.86; factor correlations 0.46, 0.47 and 0.28; one factor: χ² = 312 on 27 df, CFI 0.677, RMSEA 0.187 | `opendata.holzinger_1939` (fetched from CRAN and SHA-256 checked); Psyche (`sem.fit_cfa`), item `hs`; every value matches lavaan's |
| Fixed cut-offs: 200 samples of 301 from the fitted model, and 200 from a model in which x9 also loads 0.4 on the visual factor, each fitted by the three-factor model: the wrong model passes RMSEA at most 0.06 in 91% of samples and CFI at least 0.95 in all of them | Psyche (`sem.fit_cfa`), item `cutoffs` |
| Attenuation: two traits correlated 0.5, three items each with loadings 0.6, 500 simulated people: alpha 0.63, sum scores correlate 0.32, the two-factor model recovers 0.49 | Psyche (`sem.fit_cfa`), item `attenuation` |
| Reliability from the loadings: omega 0.63, 0.89 and 0.69 for the three factors' sums, alpha 0.63, 0.88 and 0.69; four standardized loadings 0.9, 0.8, 0.3 and 0.2: alpha 0.60, omega 0.67 | Psyche (`sem.fit_cfa`), item `omega` |
| Invariance across the two schools (Pasteur 156, Grant-White 145): configural χ² = 115.85 on 48 df, metric 124.04 on 54, scalar 164.10 on 60; Grant-White's verbal mean 0.58 higher if scalar invariance is assumed | Psyche (`sem.fit_multigroup`), item `invariance`; every value matches lavaan's |
| Mediation: 500 simulated people, X randomized, a = 0.5, no effect of M on Y, an unmeasured U (0.6) behind M and Y: indirect effect 0.17, bootstrap 95% interval 0.10 to 0.25 (1,000 resamples) | Psyche (`sem.mediation`), item `mediation` |
| The cross-lagged panel: 2,000 simulated people, 4 waves, stable traits correlated 0.6, within-person autoregression 0.3, no cross effects: the pooled cross-lagged regression gives 0.117 (SE 0.010); on the within-person deviations, -0.015 (SE 0.012) | the item's own regressions in `compute.py`, item `panel` |
| Factors and networks: one factor with loadings 0.8, 0.7, 0.6 and 0.5; the network of partial correlations (0.10 to 0.40) reproduces the correlations to 3e-16 | Psyche (`sem.factor_as_network`), item `network` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

The diagrams in chapters 6, 10 and 11 (two layers, a growth model, a cross-lagged panel, two pictures of a disorder)
are schematic, and the abstract in chapter 12 is invented for practice and labelled so on screen.

## Built in this part

* `explainer/psychology/psyche/sem.py`: model-implied covariances for path and factor models, the maximum-likelihood
  discrepancy, confirmatory factor analysis with marker-variable scaling and the χ², RMSEA, CFI, TLI and SRMR,
  multi-group models with configural, metric and scalar constraints and latent means, Markov-equivalent diagrams,
  the network implied by a factor model, and a mediation simulator with a bootstrap. Checked against lavaan on
  Holzinger and Swineford's data; tested in `tests/psychology/test_sem.py`.
* The Ledger gains three rows.
* The course's interactive: three variables and a correlation matrix; the reader draws diagrams and sees which fit
  as well as the true one.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Self-control draws on blood glucose: depletion lowers it, and a sugary drink restores self-control. | Gailliot and colleagues 2007 | failed |
| A latent-factor model and a network model of direct interactions can imply exactly the same distribution of observed responses. | Kruis and Maris 2016 | replicated |
| Fixed cut-offs for fit indices, such as CFI of at least 0.95 and RMSEA of at most 0.06, separate good models from bad ones in general. | Hu and Bentler 1999 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Wright and Jöreskog; Holzinger and
Swineford; Baron and Kenny; Bullock, Green and Ha; MacCallum and colleagues; Meredith; Hamaker, Kuiper and Grasman;
Borsboom and Cramer; Spirtes, Glymour and Scheines; Muthén and Asparouhov, and McNeish and Wolf.

## Build it

```bash
python -m videos.psychology.psych44.compute            # every number (about a minute; fetches the data once)
python tools/qa_scene.py psych44 Fit                   # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych44 -q l   # the whole part, silent preview
python tools/build.py psych44                          # 1080p30 with narration
python tools/qa_scene.py psych44 Mediation --lang zh   # the Chinese edition of one chapter
python tools/make.py psych44                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 44                    # the lab: paths, a CFA by hand, fit, invariance, mediation
python tools/check_ledger.py psych44                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's sem module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | One matrix, three diagrams | Three diagrams that fit equally; Wright's arrows and Spearman's factors; the question; objectives |
| 1 | On you: draw a model, and four numbers | Three stories as diagrams; four predictions |
| 2 | Wright's paths | The tracing rule; in matrix form |
| 3 | The factor model, confirmed | Nine tests, three factors; identification by counting |
| 4 | Estimation by maximum likelihood | The discrepancy function; Holzinger and Swineford, fitted |
| 5 | Does it fit? | The chi-square test; approximate fit; cut-offs that depend on the model |
| 6 | Measurement and structure | Two layers; attenuation, undone; reliability from the loadings |
| 7 | Measurement invariance | Three rungs; two schools |
| 8 | Mediation | The recipe; a mechanism that is not there; what would show a mechanism |
| 9 | Equivalent models | Four diagrams, one matrix; what fit cannot tell you |
| 10 | Latent variables over time | Growth curves; the cross-lagged panel; between people or within? |
| 11 | Factors or networks? | Two pictures of a disorder; the same covariances; what could decide |
| 12 | Reading an SEM paper | An invented abstract; eight questions |
| 13 | The Ledger | Three rows; what they have in common |
| 14 | In practice: surveys, tests and people analytics | Where the models work; the question to ask |
| 15 | Frontier: causal discovery, Bayes and dynamic fit | What discovery can orient; small samples and fit for this model |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; Kant's three objections; payoffs; problems; references; Part 45 |

## Sources

* S. Wright, Correlation and causation, *Journal of Agricultural Research* 20 (1921) 557-585; K. G. Jöreskog, A
  general approach to confirmatory maximum likelihood factor analysis, *Psychometrika* 34 (1969) 183-202; K. A.
  Bollen, *Structural Equations with Latent Variables* (Wiley, 1989); R. B. Kline, *Principles and Practice of
  Structural Equation Modeling* (Guilford).
* K. J. Holzinger and F. F. Swineford, *A Study in Factor Analysis: The Stability of a Bi-Factor Solution*
  (University of Chicago, 1939); Y. Rosseel, lavaan: an R package for structural equation modeling, *Journal of
  Statistical Software* 48 (2012).
* L. Hu and P. M. Bentler, Cutoff criteria for fit indexes in covariance structure analysis, *Structural Equation
  Modeling* 6 (1999) 1-55; H. W. Marsh, K.-T. Hau and Z. Wen (2004); D. McNeish and M. G. Wolf, Dynamic fit index
  cutoffs for confirmatory factor analysis models, *Psychological Methods* 28 (2023).
* W. Meredith, Measurement invariance, factor analysis and factorial invariance, *Psychometrika* 58 (1993) 525-543.
* R. M. Baron and D. A. Kenny, The moderator-mediator variable distinction, *Journal of Personality and Social
  Psychology* 51 (1986) 1173-1182; J. G. Bullock, D. P. Green and S. E. Ha, Yes, but what's the mechanism? (don't
  expect an easy answer), *Journal of Personality and Social Psychology* 98 (2010) 550-558.
* M. T. Gailliot et al. (2007); F. Lange and F. Eggert (2014); M. A. Vadillo, N. Gold and M. Osman (2016).
* R. C. MacCallum, D. T. Wegener, B. N. Uchino and L. R. Fabrigar, The problem of equivalent models in applications
  of covariance structure analysis, *Psychological Bulletin* 114 (1993) 185-199.
* E. L. Hamaker, R. M. Kuiper and R. P. P. P. Grasman, A critique of the cross-lagged panel model, *Psychological
  Methods* 20 (2015) 102-116.
* D. Borsboom and A. O. J. Cramer, Network analysis: an integrative approach to the structure of psychopathology,
  *Annual Review of Clinical Psychology* 9 (2013) 91-121; J. Kruis and G. Maris (2016); M. Marsman et al. (2018).
* P. Spirtes, C. Glymour and R. Scheines, *Causation, Prediction, and Search* (2nd edition, MIT Press, 2000); B.
  Muthén and T. Asparouhov, Bayesian structural equation modeling, *Psychological Methods* 17 (2012) 313-335; J. M.
  Rohrer, Thinking clearly about correlations and causation, *Advances in Methods and Practices in Psychological
  Science* 1 (2018) 27-42.

## Problems and solutions

1. **Tracing.** The only path from X to Y runs through M, so r(X, Y) = 0.5 × 0.6 = 0.30.
2. **Counting.** Free parameters: 9 loadings less 3 markers = 6, plus 3 factor variances and 3 covariances, plus 9
   residual variances: 21. Moments: 9 × 10/2 = 45. Degrees of freedom: 45 - 21 = 24.
3. **RMSEA.** √((85.3 - 24)/(24 × 301)) = √(61.3/7224) = √0.00849 = 0.092.
4. **Attenuation.** 0.32/√(0.63 × 0.63) = 0.32/0.63 = 0.51, close to the true 0.5.
5. **Intercepts.** Δχ² = 164.1 - 124.0 = 40.1 on 60 - 54 = 6 df; the 5% critical value is 12.6 (p ≈ 4 × 10⁻⁷).
   Scalar invariance is rejected, so the schools' means are not comparable as they stand.
6. **Equivalence.** X → M → Y, Y → M → X and X ← M → Y all imply that X and Y are independent given M and nothing
   else, so they fit identically, always. X → M ← Y implies that X and Y are independent, a different constraint.
7. **The abstract.** Burnout → workload perceptions → turnover intention, or turnover intention → burnout →
   workload perceptions, fit as well as the authors' chain. A study that tells them apart: randomize a reduction in
   workload (for instance, staffing) across teams, measure burnout and intention monthly, and preregister that
   burnout should fall before intention does; a second arm that targets burnout without changing workload tests
   the mediator directly.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
Wright's 1921 paper and its guinea-pig examples; McDonald's omega (McDonald, *Test Theory*, 1999); Jöreskog's 1969 paper; Holzinger and Swineford's 1939 monograph and
the two schools; Hu and Bentler's cut-offs (CFI 0.95, RMSEA 0.06, SRMR 0.08) and their simulation conditions;
McNeish and Wolf's dynamic cut-offs (2023); Meredith (1993); Baron and Kenny's citation count ("tens of
thousands"); Bullock, Green and Ha's title and argument; Gailliot et al. (2007), Lange and Eggert (2014) and Vadillo,
Gold and Osman (2016); MacCallum et al.'s survey (53 published applications, and how few acknowledged equivalent
models); Hamaker, Kuiper and Grasman (2015); Borsboom and Cramer (2013); Kruis and Maris (2016) and Marsman et al.
(2018); Spirtes, Glymour and Scheines's PC algorithm; Muthén and Asparouhov (2012); Rohrer (2018); and every page
range in Sources.
