# Statistics, Built — Part 13: Experiments by Design

Part 13 of a sixty-five-part course in statistics, from a first course to a PhD (see [the series plan](../README.md)
and [the syllabus](../SYLLABUS.md)), in Stage II, Bachelor's: Methods. Part 12 fitted relationships to data that
were already there. This part designs the data, so that the answer is unambiguous.

It opens at Rothamsted. Broadbalk has been sown with wheat since 1843, and in 1919 Fisher arrives to analyse
seventy-six years of records that can describe but not decide. A simulated uniformity trial shows the soil's own
variation, about 8% of the mean. Fisher's answer, in his own words (1926, 1938), is to design the experiment. From there
the part covers:
- the three principles on the field-trial simulator: a tidy systematic layout is biased 3.9-fold, randomization makes
  the estimate unbiased, replication follows σ√(2/n), and pairing halves the SD; Peirce & Jastrow (1884);
- randomization as inference: the sharp null, the exact distribution over all 184,756 labellings, balance of the
  World's unmeasured heights and incomes, and a doctor who chooses;
- one-way ANOVA as Pythagoras in R²⁴, the F-test, Fisher & Mackenzie's first table (1923), ANOVA as regression, and
  expected mean squares;
- orthogonal contrasts; the family-wise error of ten pairwise tests; Tukey, Dunnett, Bonferroni and Scheffé
  multipliers; the HSD grid;
- blocking on a steep gradient (power 74% vs 10%, relative efficiency 15), the RCBD model, Darwin's *Zea mays* and
  Fisher's 863 of 32,768, and incomplete blocks;
- Latin squares (Knut Vik, randomized squares, Euler's 36 officers), crossovers and carryover;
- factorials: one-factor-at-a-time on the bakery's diagonal ridge, the 2² square and its interaction, the NPK cube,
  Yates's algorithm, the interaction plot, Daniel's half-normal plot, hidden replication;
- fractional factorials: the half cube, aliasing and the defining relation, resolution, 2⁷⁻⁴, Plackett–Burman;
- response surfaces on the island bakery: a first-order design, steepest ascent, a central composite design, the
  fitted quadratic's canonical analysis (Box & Wilson 1951);
- split plots and their two error strata, with the classic mistake on the Board;
- optimal design: the line's end points, Kirstine Smith (1918), D-optimality, thirds at −1, 0, 1, and the
  Kiefer–Wolfowitz equivalence theorem;
- power, the minimum detectable effect, Cohen's conventions, and the winner's curse (type M and S errors);
- online experiments: Bing's headline, the anatomy of an A/B test, CUPED as regression adjustment, sample-ratio
  mismatch, the old pitfalls at scale.

Every number on screen is computed in [`compute.py`](compute.py) or inline in a scene:
- the hidden-covariate check uses the World's adults (seed 1662);
- Darwin's differences come from the Museum;
- the field trials run on `statkit.design.Field`, and the bakery on `statkit.design.Bakery`;
- everything else is a seeded simulation.

**Built in this part:**
- **`statkit.design`** ([`explainer/stats/kit/design.py`](../../../explainer/stats/kit/design.py)):
  - `Field`, the field-trial simulator: a hidden fertility surface plus plot noise;
  - `Bakery`, a hidden response surface;
  - one-way, RCBD and Latin-square ANOVAs;
  - random Latin squares;
  - 2ᵏ designs, factorial effects and Yates's algorithm;
  - fractional factorials and aliases;
  - Tukey's HSD and Scheffé's multiplier;
  - the D-criterion, the minimum detectable effect, CUPED and the sample-ratio test.

  The analyses are checked against SciPy and statsmodels in `tests/test_stats_kit_design.py`.
- **The field plot** (`FieldPlot` in `explainer/stats/viz.py`): a field from above, painted by fertility or yield, with
  treatment letters and block frames.

The Coverage Board gains seven rows, all tests at a nominal 5%, R = 10,000:

| Method | Setting | Achieved | Verdict |
|---|---|---|---|
| randomization test | 10 + 10 plots, skewed errors | 5.19% | kept |
| t-test, systematic layout | west vs east, fertility gradient | 100% | broken |
| pairwise t-tests, unadjusted | 5 groups, any of 10 pairs | 26.6% | broken |
| Tukey's HSD | 5 groups, any of 10 pairs | 4.95% | kept |
| split plot analysed as a CRD | whole-plot factor, 4 blocks | 25.6% | broken |
| split plot, whole-plot error | whole-plot factor, 4 blocks | 5.01% | kept |
| CUPED z-test | A/A, 2,000 users | 5.21% | kept |

## Build it

```bash
python -m videos.stats.stats13.compute         # once (a few minutes; cached in .cache/stats13)
python tools/build.py stats13 -q l             # fast 480p preview
python tools/build.py stats13                  # 1080p30 -> renders/stats13.mp4
python tools/qa_scene.py stats13 SplitPlot
python tools/lecture_length.py stats13 --floor 50
```

## Chapters

| # | Chapter | Numbers |
|---|---|---|
| 0 | Rothamsted, 1919 | uniformity trial: yields 41–60, CV 8% |
| 1 | Three principles | true gain 2: systematic 7.8 (swapped −4.3); 4,000 random layouts mean 1.99, SD 0.71; n = 1 → 6.1, n = 72 → 0.70; pairs SD 0.36 |
| 2 | Randomization as inference | 20 plots: difference 2.71; 6,322 of 184,756 labellings, p = 0.034 (t: 0.031); height-gap SD 1.32 cm, 4.8% beyond 2 SD; a chooser's gap 16.1 cm |
| 3 | One-way ANOVA | SST 107.8 = 46.6 + 61.2; F = 5.07 on (3, 20), p = 0.009; R² = 0.432 |
| 4 | Contrasts | 37.09 + 1.04 + 8.45 = 46.59; FWER 26.6% vs Tukey 4.95%; multipliers t 2.06, Dunnett 2.61, Tukey 2.94, Bonferroni 3.08, Scheffé 3.32; HSD 3.50 |
| 5 | Blocking | ignoring blocks F = 0.21, p = 0.89; RCBD F = 4.94, p = 0.014; power 10% vs 74%; MSE 33.4 vs 2.25; Darwin t = 2.15, 863/32,768, p = 0.053 |
| 6 | Latin squares | F = 17.8 vs 0.88 one-way; power 96% vs 20%; 161,280 squares of order 5 |
| 7 | Factorials | OFAT ends at 225 °C, 26.5 min, quality 79.6 vs 85; 2² effects 14.3, 19.0, −15.0; NPK: N 6.21, P 2.95, NP 1.34, SE 0.53 |
| 8 | Fractional factorials | half fraction A 4.21 (full 4.51), AB + CD 1.68; Plackett–Burman XᵀX = 12I |
| 9 | Response surfaces | first-order fit 43.9 + 12.6x₁ + 15.6x₂; best on the path 85.3; stationary point 203.0 °C, 31.7 min, predicted 85.2 (truth 84.9); 29 bakes |
| 10 | Split plots | wrong F = 22.3 on (1, 24), p = 8 × 10⁻⁵; right F = 6.79 on (1, 3), p = 0.08; null rejection 25.6% vs 5.01% |
| 11 | Optimal design | slope SE 0.495σ (even) vs 0.316σ (ends); det M 4/27 = 0.148 vs 0.039; max d(x) = 3 vs 7.5 |
| 12 | Power | n for 80%: 42 (σ = 4) vs 12 (σ = 2); MDE 3.54 at n = 20, 1.77 at n = 80; Cohen 393 / 63 / 25; exaggeration 2.41× at n = 5, 1.12× at n = 42 |
| 13 | Online experiments | ρ = 0.80; SE 0.056 → 0.034; p 0.065 → 3.9 × 10⁻⁵; worth 2.8× the users; SRM 50,000 vs 50,820, p = 0.0098 |
| 14 | Outro | — |

## Sources

- **Rothamsted and Fisher.**
  - R. A. Fisher, "Studies in crop variation I", *J. Agric. Sci.* 11 (1921); with W. A. Mackenzie, II, *J. Agric. Sci.*
    13 (1923).
  - R. A. Fisher, "The arrangement of field experiments", *J. Ministry of Agriculture* 33 (1926); *The Design of
    Experiments* (1935).
  - W. B. Mercer & A. D. Hall, *J. Agric. Sci.* 4 (1911).
  - C. S. Peirce & J. Jastrow, *Memoirs of the National Academy of Sciences* 3 (1884).
  - J. Neyman (1923), trans. *Statist. Sci.* 5 (1990).
- **Design and analysis.**
  - F. Yates, *The Design and Analysis of Factorial Experiments* (1937); "Incomplete randomized blocks", *Ann.
    Eugenics* 7 (1936).
  - D. J. Finney, *Ann. Eugenics* 12 (1945); R. Plackett & J. P. Burman, *Biometrika* 33 (1946).
  - G. Box & K. B. Wilson, *JRSS B* 13 (1951); G. Box & J. S. Hunter, *Technometrics* 3 (1961); G. Box & N. Draper, *JASA*
    54 (1959).
  - C. Daniel, *Technometrics* 1 (1959); E. J. Williams, *Aust. J. Sci. Res.* 2 (1949).
  - R. C. Bose, S. S. Shrikhande & E. T. Parker, *Canad. J. Math.* 12 (1960).
- **Multiple comparisons.** J. Tukey, "The problem of multiple comparisons" (1953); H. Scheffé, *Biometrika* 40 (1953);
  C. Dunnett, *JASA* 50 (1955).
- **Optimal design.** K. Smith, *Biometrika* 12 (1918); J. Kiefer & J. Wolfowitz, *Canad. J. Math.* 12 (1960).
- **Power.**
  - J. Cohen, *J. Abnormal and Social Psychology* 65 (1962); *Statistical Power Analysis for the Behavioral Sciences*
    (2nd ed., 1988).
  - A. Gelman & J. Carlin, *Perspectives on Psychological Science* 9 (2014).
- **Online experiments.**
  - R. Kohavi, D. Tang & Y. Xu, *Trustworthy Online Controlled Experiments* (2020).
  - A. Deng, Y. Xu, R. Kohavi & T. Walker, *WSDM* (2013).
  - D. Freedman, *Adv. Appl. Math.* 40 (2008); W. Lin, *Ann. Appl. Stat.* 7 (2013).
- **Textbooks.**
  - G. Box, J. S. Hunter & W. G. Hunter, *Statistics for Experimenters* (2nd ed., 2005).
  - D. Montgomery, *Design and Analysis of Experiments* (10th ed., 2019).
  - W. Cochran & G. Cox, *Experimental Designs* (2nd ed., 1957).
  - R. Bailey, *Design of Comparative Experiments* (2008).

## Problems and solutions

**1. An exact randomization test.**

*Solution.* The six yields total 84. If the new variety's three plots sum to S, the difference in means is
(S − (84 − S))/3 = (2S − 84)/3.

The observed S is 14 + 16 + 18 = 48, a difference of 4. |difference| ≥ 4 means S ≥ 48 or S ≤ 36. Of the
C(6, 3) = 20 equally likely sets of three:
- only {14, 16, 18} (48) and {15, 16, 18} (49) reach 48;
- by complements, two sets have S ≤ 36.

So p = 4/20 = 0.20. Six plots cannot give strong evidence: the smallest possible two-sided p is 2/20 = 0.10.

**2. The ANOVA identity.**

*Solution.* Write yᵢⱼ − ȳ = (ȳᵢ − ȳ) + (yᵢⱼ − ȳᵢ) and square. The cross term is
2Σᵢ(ȳᵢ − ȳ)Σⱼ(yᵢⱼ − ȳᵢ). Each inner sum is zero, because deviations from a group's own mean sum to zero. So
SST = Σᵢnᵢ(ȳᵢ − ȳ)² + ΣᵢΣⱼ(yᵢⱼ − ȳᵢ)² = SSB + SSW.

**3. Yates's algorithm on a 2².**

*Solution.* In standard order the yields are 20, 30, 24, 40.
- **Pass 1:** sums 50, 64; differences 10, 16.
- **Pass 2:** sums 114, 26; differences 14, 6.

The column [114, 26, 14, 6] is the total and the contrasts for A, B and AB. Divide the contrasts by 2^(k−1) = 2:
A = 13, B = 7, AB = 3. Check A directly: (30 + 40)/2 − (20 + 24)/2 = 35 − 22 = 13.

**4. A half fraction of a 2⁵.**

*Solution.* E = ABCD gives I = ABCDE. The shortest (only) word has five letters, so the design has resolution V.
- A × ABCDE = BCDE, so A is aliased with a four-factor interaction.
- AB × ABCDE = CDE, so AB is aliased with a three-factor interaction.

Main effects and two-factor interactions are all clear of each other.

**5. D-optimality for a line.**

*Solution.* With f(x) = (1, x),
M = [[1, x̄], [x̄, mean(x²)]]
under the design ξ, so det M = mean(x²) − x̄² = Var_ξ(x).

On [−1, 1], Var(x) ≤ mean(x²) ≤ 1, with equality only if every point is at ±1 and x̄ = 0. So the D-optimal design
puts half the observations at each end, with det M = 1.

**6. A sample size.**

*Solution.* n = 2(1.960 + 0.842)² σ²/δ² = 2 × 7.85 × (4/2.5)² = 40.2, so 41 plots per variety. The exact
calculation with the noncentral t gives 42, the value in chapter 12.

## Where it comes back

| Idea | Returns in |
|---|---|
| GLMs for counts and binary outcomes | 14, 24 |
| rank and permutation tests in general | 16 |
| survey design: strata and clusters | 18 |
| the linear model in depth, estimability | 23 |
| mixed models: split plots and clustering | 25 |
| the false discovery rate | 33 |
| potential outcomes, interference, two-stage designs | 35, 62 |
| sequential and adaptive experiments | 58 |
| the Coverage Board | every part; 65 |
