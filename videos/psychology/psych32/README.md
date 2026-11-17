# Psychology, Built: Part 32, Intelligence

In 1904, working separately, two men put a number on the mind. In England Charles Spearman found that
schoolchildren's marks in every subject, and their skill at telling two tones apart, correlated positively with one
another, proposed one general factor, and invented factor analysis to measure it. In Paris Alfred Binet was asked by
the Ministry of Public Instruction for a way to find the children who would need help at school, and built a scale of
tasks of rising difficulty. Within twenty years, in the United States, test scores were being used to justify
sterilizing people. This part keeps all three facts in view: the mathematics, the predictions and the harm.

The positive manifold in Spearman's own table and in Holzinger and Swineford's 301 children, recomputed; the
one-factor model derived, with Spearman's tetrad differences and maximum-likelihood loadings; one factor rejected in
the real battery, three accepted, and the hierarchy above them (Thurstone, Carroll); the viewer solves three matrix
items; three simulated worlds, a common cause, Thomson's sampling and van der Maas's mutualism, that a one-factor test
cannot tell apart, and the experiment that can; ratio and deviation IQs and the error band around every score; what
scores predict, range restriction and Thorndike's correction, and health; what matrix items rest on, after
Carpenter, Just and Shell, with Psyche's rule-tracking solver; heritability by age, a year of school, and the Flynn
effect; group differences through overlap, measurement invariance and Lewontin's two fields, and stereotype threat's
record; the history of harm, Burt's fraud and a critic checked; multiple and emotional intelligences and the Mozart
effect. The practice chapter is cutoffs, the DSM-5 definition of intellectual disability, Brogden's value of a test,
and adverse impact; the frontier is network models, polygenic scores within families, and intelligence in machines.

## Where the numbers come from

| What | Source |
|---|---|
| Spearman's six-by-six correlations (Classics, French, English, Mathematics, pitch, music); one-factor loadings 0.96, 0.87, 0.81, 0.74, 0.69, 0.65; RMSR of residuals 0.03; mean absolute tetrad difference 0.038; first factor 63% of the variance | Spearman (1904), the Archive's `SPEARMAN_1904`; Psyche (`traits.tetrads`, `one_factor`), item `spearman` |
| Holzinger and Swineford: 301 children, 9 tests (x1–x9); smallest correlation −0.076, mean 0.26, one negative pair of 36; one, two and three ML factors χ² 307 (27 df), 128 (19), 22.4 (12, p = 0.034); varimax factors visual, verbal and speed; the composites correlate 0.32, 0.28 and 0.23 | lavaan's copy of the data, fetched and checked by SHA-256 (`opendata.holzinger_1939`); `statkit.multi.factor_ml`, item `holzinger` |
| Three worlds of 300 people and 8 tests: one-factor p 0.69, 0.10 and 0.50; one-factor test rejects 5.5%, 8% and 4% of 200 samples; training one ability by 0.5 SD moves only it under a common cause, and the other seven by about 0.075 SD under mutualism | Psyche (`traits.common_cause`, `sampling`, `mutualism`, `train_one`), item `worlds` |
| Ratio IQ 125 for a mental age of 10 at 8, and 40 for a mental age of 16 at 40; deviation IQ 120 for a raw score of 42 against a mean of 34 and SD of 6; SEM 6.7, 4.7 and 3.4 points at reliability 0.80, 0.90 and 0.95 | Psyche (`traits.ratio_iq`, `deviation_iq`, `sem_interval`), item `scale` |
| Range restriction: 200,000 simulated applicants, validity 0.50; hiring the top 30% leaves 0.28, u = 0.51; Thorndike's correction gives 0.50 back | Psyche (`traits.restriction_corrected`), item `validity` |
| Matrix items with 1 to 3 rules; a solver that tracks 1 to 4 rules; a population mixing capacities gets 100%, 100%, 91%, 67% and 38% of items with 0 to 4 rules | Psyche (`traits.matrix_item`, `solve`, `solver_accuracy`), item `matrices` |
| Two distributions d = 0.2, 0.5 and 1.0 apart overlap 92%, 80% and 62%, with 42%, 31% and 16% of the lower group above the higher mean; a real latent gap of 0.4 SD moves every test (total 0.38 SD), one biased test moves only itself (total 0.15) | Psyche (`traits.overlap`, `invariance_demo`), item `groups` |
| Near a cutoff of 70: a true 72 scores below 70 28% of the time at reliability 0.95 and 38% at 0.80; a true 68 scores 70 or more 28% of the time; Kelley's estimate behind an observed 69 is 70.5 and 75.2 | Psyche (`traits.below_cut`, `kelley`), item `practice` |
| Brogden's gain: hiring the top tenth gives 0.90 SD at validity .51 and 0.54 at .31; hiring half, 0.41 and 0.25; two groups 0.5 SD apart give a selection-rate ratio of 0.37 at the top tenth and 0.62 at half | Psyche (`traits.selection_gain`, `impact_ratio`), item `practice` |
| Hierarchy: Classics, French, English, Mathematics averaging 0.77, 0.72, 0.70, 0.67 | Spearman (1904) |
| Thurstone: 56 tests, seven primary mental abilities | Thurstone (1938) |
| Carroll: more than 460 data sets, three strata | Carroll (1993) |
| Deary et al.: more than 70,000 English children; g at 11 and GCSE at 16 correlate 0.81 (latent); 58.6% of mathematics, 48% of English, 18.1% of art and design | Deary et al. (2007) |
| Strenze: 0.56 with education, 0.43 occupation, 0.20 income | Strenze (2007) |
| Job performance: about .5, revised to .31 | Schmidt and Hunter (1998); Sackett et al. (2022) |
| Calvin et al.: 16 studies; 1 SD higher early IQ, about 24% lower risk of death; adult socioeconomic position attenuates it by 34%, education by 54% | Calvin et al. (2011) |
| Carpenter et al.: the number of rules explains 57% of item difficulty; FAIRAVEN and BETTERAVEN | Carpenter, Just and Shell (1990) |
| Heritability 41% at 9, 55% at 12, 66% at 17, about 11,000 twin pairs; 11,500 pairs in a longitudinal meta-analysis; poverty and heritability: 319 pairs at 7, then 24,926 pairs in six countries | Haworth et al. (2010); Briley and Tucker-Drob (2013); Turkheimer et al. (2003); Tucker-Drob and Bates (2016) |
| Schooling: 142 effect sizes, 42 data sets, more than 600,000 people; 1.2 to 5.2 points a year by design, 3.4 on average | Ritchie and Tucker-Drob (2018) |
| Flynn: 13.8 points from 1932 to 1978; 5 to 25 points in a generation in 14 nations | Flynn (1984, 1987) |
| Stereotype threat: more than 2,000 Dutch students, no effect | Flore, Mulder and Wicherts (2018) |
| Burt's 0.771 | Kamin (1974); Hearnshaw (1979) |
| Morton's skulls: about 300 remeasured | Lewis et al. (2011) |
| Mozart: about 40 studies, more than 3,000 people, d = 0.37 against no stimulus | Pietschnig, Voracek and Formann (2010) |
| Polygenic scores: about 1.1 million people, 11–13% of education and 7–10% of cognitive performance; 178,000 siblings in 19 cohorts, about 47% shrinkage within families | Lee et al. (2018); Howe et al. (2022) |

## Built in this part

* `explainer/psychology/psyche/traits.py`: tetrad differences and a one-factor ML fit; three populations that make a
  positive manifold (a common cause, Thomson's sampling of bonds, van der Maas's mutualism) and an experiment that
  trains one ability in each; ratio and deviation IQs, the standard error of a score, Thorndike's correction for
  range restriction; matrix items generated from attribute rules and a solver that can track only so many rules;
  overlap of two distributions and a measurement-invariance demonstration; the chance of falling below a cutoff,
  Kelley's true-score estimate, Brogden's selection gain and the selection-rate ratio. Tested in
  `tests/psychology/test_traits.py`.
* `explainer/psychology/opendata.py` fetches Holzinger and Swineford's scores from lavaan's CRAN source package and
  reads its R data file with `rdata.py`; the Archive gains `SPEARMAN_1904` and `HOLZINGER_1939`.
* The Ledger gains eight rows; Part 31's two Flynn declarations and Part 9's two deferred rows (heritability by age and by family income) are settled.
* The course's interactive is a matrix test: items generated fresh from one to four rules, with keys F and J for the
  two candidate answers, and a running chart of accuracy by number of rules.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Scores on different kinds of mental test correlate positively | Spearman 1904 | replicated |
| General mental ability predicts job performance at about .5, better than any other single method | Schmidt and Hunter 1998 | replicated, smaller |
| Average test scores rose about three points a decade through the twentieth century | Flynn 1984 | replicated |
| An extra year of schooling raises intelligence-test scores | Ceci 1991 | replicated |
| The heritability of general cognitive ability rises from childhood to young adulthood | Haworth and colleagues 2010 | replicated |
| Among children raised in poverty, the heritability of IQ is close to zero | Turkheimer, Haley, Waldron, D'Onofrio and Gottesman 2003 | contested |
| Listening to Mozart improves spatial reasoning | Rauscher, Shaw and Ky 1993 | failed |
| Human abilities form several independent intelligences | Gardner 1983 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Binet and Simon's scale and
Stern's quotient, Wechsler's deviation IQ, *Buck v. Bell*, Thurstone's primary abilities, Deary et al.'s cohort,
Strenze's meta-analysis, Calvin et al.'s mortality meta-analysis, Carpenter, Just and Shell's process model,
Snyderman and Herrnstein's history, the Burt case, Gould and Lewis et al., the
network-model dispute, polygenic scores within families, Chollet's proposal, and stereotype threat (due a row with
prejudice in Part 36).

## Build it

```bash
python -m videos.psychology.psych32.compute            # every number (about a minute; fetches lavaan once)
python tools/qa_scene.py psych32 Factor                # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych32 -q l   # the whole part, silent preview
python tools/build.py psych32                          # 1080p30 with narration
python tools/qa_scene.py psych32 Worlds --lang zh      # the Chinese edition of one chapter
python tools/make.py psych32                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 32                    # the lab: tetrads, factors, three worlds, range restriction
python tools/check_ledger.py psych32                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's traits module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 1904: two men, one number | Spearman and Binet; three facts that belong together; the question; objectives |
| 1 | The positive manifold | Spearman's table; the hierarchy; Holzinger and Swineford's 301 children |
| 2 | One factor, derived | The model; the tetrad difference; fitting the loadings; one factor is not enough |
| 3 | One factor or many | Thurstone's seven; three factors in the real battery; Carroll's hierarchy |
| 4 | On you: three matrices | Three items with one, two and three rules, and the answers |
| 5 | What g is not shown to be | A common cause, sampling and mutualism; the same correlations; the experiment that tells them apart |
| 6 | The scale | Mental age and the quotient; Wechsler's deviation IQ; the error bar; *Hall v. Florida* |
| 7 | What it predicts | School, work and income; range restriction; health |
| 8 | What it rests on | Carpenter, Just and Shell; Psyche's solver; working memory, speed and the brain |
| 9 | Genes, schools and generations | Heritability by age; a year of school; the Flynn effect and invariance |
| 10 | Group differences, with care | Overlap; measurement invariance; two fields; stereotype threat's record |
| 11 | The history of harm | Goddard, the Army tests and 1924; *Buck v. Bell*; Burt's twins; the critic, checked |
| 12 | Other intelligences | Multiple intelligences; emotional intelligence; the Mozart effect |
| 13 | The Ledger | Eight rows: the manifold, job validity, the Flynn effect, schooling, heritability by age and by income, Mozart, multiple intelligences |
| 14 | In practice: cutoffs, clinics and hiring | Error near a cutoff and Kelley's estimate; DSM-5; Brogden's gain; *Griggs* and the four-fifths rule |
| 15 | Frontier: networks, genes and machines | Network models against g; polygenic scores within families; Chollet and ARC; open problems |
| | Recap, problems, and the road ahead | Your matrices; ten lines; Kant's three objections; payoffs; problems; references; Part 33 |

## Sources

* C. Spearman, "General intelligence," objectively determined and measured, *American Journal of Psychology* 15
  (1904) 201–292; G. H. Thomson, A hierarchy without a general factor, *British Journal of Psychology* 8 (1916)
  271–281.
* A. Binet and T. Simon, *L'Année Psychologique* 11 (1905); A. Binet, *Les idées modernes sur les enfants* (1909);
  W. Stern (1912); L. M. Terman, *The Measurement of Intelligence* (1916); D. Wechsler, *The Measurement of Adult
  Intelligence* (1939).
* K. J. Holzinger and F. Swineford, *A study in factor analysis: the stability of a bi-factor solution*,
  Supplementary Educational Monographs 48 (University of Chicago, 1939); the data as distributed with lavaan (CRAN,
  GPL).
* L. L. Thurstone, *Primary Mental Abilities* (1938); J. B. Carroll, *Human Cognitive Abilities: A Survey of
  Factor-Analytic Studies* (Cambridge University Press, 1993).
* H. L. J. van der Maas et al., A dynamical model of general intelligence: the positive manifold of intelligence by
  mutualism, *Psychological Review* 113 (2006) 842–861.
* I. J. Deary, S. Strand, P. Smith and C. Fernandes, Intelligence and educational achievement, *Intelligence* 35
  (2007) 13–21; T. Strenze, Intelligence and socioeconomic success, *Intelligence* 35 (2007) 401–426.
* F. L. Schmidt and J. E. Hunter, *Psychological Bulletin* 124 (1998) 262–274; P. R. Sackett, C. Zhang, C. M. Berry
  and F. Lievens, *Journal of Applied Psychology* 107 (2022) 2040–2068.
* C. M. Calvin et al., Intelligence in youth and all-cause-mortality, *International Journal of Epidemiology* 40
  (2011).
* P. A. Carpenter, M. A. Just and P. Shell, What one intelligence test measures, *Psychological Review* 97 (1990)
  404–431.
* C. M. A. Haworth et al., The heritability of general cognitive ability increases linearly from childhood to young
  adulthood, *Molecular Psychiatry* 15 (2010) 1112–1120; D. A. Briley and E. M. Tucker-Drob, *Psychological Science* 24 (2013)
  1704–1713; E. Turkheimer et al., Socioeconomic status modifies heritability of IQ in young children,
  *Psychological Science* 14 (2003) 623–628; E. M. Tucker-Drob and T. C. Bates, *Psychological Science* 27 (2016)
  138–149.
* S. J. Ceci, *Developmental Psychology* 27 (1991) 703–722; S. J. Ritchie and E. M. Tucker-Drob, How much does
  education improve intelligence? *Psychological Science* 29 (2018) 1358–1369.
* J. R. Flynn, *Psychological Bulletin* 95 (1984) 29–51 and 101 (1987) 171–191; J. M. Wicherts et al.,
  *Intelligence* 32 (2004) 509–537; J. R. Flynn, *What Is Intelligence?* (Cambridge University Press, 2007).
* R. C. Lewontin, Race and intelligence, *Bulletin of the Atomic Scientists* (1970); P. C. Flore and J. M.
  Wicherts, *Journal of School Psychology* (2015); P. C. Flore, J. Mulder and J. M. Wicherts, *Comprehensive Results
  in Social Psychology* (2018).
* M. Snyderman and R. J. Herrnstein, Intelligence tests and the Immigration Act of 1924, *American Psychologist* 38
  (1983); *Buck v. Bell*, 274 U.S. 200 (1927); *Skinner v. Oklahoma*, 316 U.S. 535 (1942).
* L. J. Kamin, *The Science and Politics of I.Q.* (1974); L. S. Hearnshaw, *Cyril Burt, Psychologist* (1979).
* S. J. Gould, *The Mismeasure of Man* (1981); J. E. Lewis et al., The mismeasure of science, *PLoS Biology* 9
  (2011) e1001071.
* H. Gardner, *Frames of Mind* (1983) and *Intelligence Reframed* (1999); B. A. Visser, M. C. Ashton and P. A.
  Vernon, *Intelligence* 34 (2006) 487–502; M. A. Brackett and J. D. Mayer, *Personality and Social Psychology
  Bulletin* 29 (2003).
* F. H. Rauscher, G. L. Shaw and K. N. Ky, Music and spatial task performance, *Nature* 365 (1993) 611; J.
  Pietschnig, M. Voracek and A. K. Formann, *Intelligence* 38 (2010) 314–323.
* T. L. Kelley, *Interpretation of Educational Measurements* (1927); H. E. Brogden, When testing pays off,
  *Personnel Psychology* 2 (1949) 171–183; *Griggs v. Duke Power Co.*, 401 U.S. 424 (1971); Uniform Guidelines on
  Employee Selection Procedures, 29 CFR 1607 (1978); American Psychiatric Association, *DSM-5* (2013); *Hall v.
  Florida*, 572 U.S. 701 (2014).
* K.-J. Kan, H. L. J. van der Maas and S. Levine, *Intelligence* 73 (2019) 52–62; D. McFarland, *Journal of
  Intelligence* (2020); K.-J. Kan et al., How to compare psychometric factor and network models, *Journal of
  Intelligence* 8 (2020).
* J. Lee et al., *Nature Genetics* (2018); L. Howe et al., *Nature Genetics* (2022).
* F. Chollet, On the measure of intelligence, arXiv:1911.01547 (2019).
* I. J. Deary, *Intelligence: A Very Short Introduction* (2nd ed., Oxford University Press, 2020).

## Problems and solutions

1. **Tetrads.** Under one factor, $r_{ij} = \lambda_i \lambda_j$ for $i \neq j$. Show that every tetrad difference $r_{ik} r_{jl} - r_{il} r_{jk}$ is zero, and that $\lambda_i^2 = r_{ij} r_{ik} / r_{jk}$.

   *Solution.* With r_ij = λ_iλ_j, r_ik r_jl − r_il r_jk = λ_iλ_kλ_jλ_l − λ_iλ_lλ_jλ_k = 0. And
   r_ij r_ik / r_jk = λ_i²λ_jλ_k / (λ_jλ_k) = λ_i².
2. **Three of Spearman's correlations.** From Spearman's table, $r_{CF} = .83$, $r_{CE} = .78$ and $r_{FE} = .67$. Estimate the loadings of Classics, French and English, and say why three tests give one answer but four test the model.

   *Solution.* λ_C² = .83 × .78 / .67 = 0.966, λ_C = 0.98; λ_F² = .83 × .67 / .78 = 0.713,
   λ_F = 0.84; λ_E² = .78 × .67 / .83 = 0.630, λ_E = 0.79. Three tests give three correlations and three loadings, so
   the model fits exactly whatever the data; with four there are six correlations and four loadings, and the two
   independent tetrads must vanish, which is a test. (The full six-test ML fit gives 0.96, 0.87 and 0.81, close.)
3. **Thorndike's case II.** Derive Thorndike's correction for direct range restriction, $r_c = (r/u) / \sqrt{1 - r^2 + r^2/u^2}$, and apply it to $r = .28$, $u = .51$.

   *Solution.* Selection on X alone leaves the regression of Y on X unchanged: slope b = r s_Y/s_X is the
   same in both groups, and so is the residual variance s_Y²(1 − r²). Write s_x = u s_X for the restricted SD. In the
   full group, r_c² = b²s_X² / (b²s_X² + e²) with e² the residual variance; substitute b = r s_y/s_x and
   e² = s_y²(1 − r²) from the restricted group and divide by s_y² to get r_c = (r/u) / √(1 − r² + r²/u²). With
   r = .28 and u = .51: (0.549) / √(0.9216 + 0.3014) = 0.50, the validity before selection.
4. **Ratio IQs.** Why does a ratio IQ give a 40-year-old with a mental age of 16 a score of 40? Give the deviation IQ of a raw score of 42 when the age group's mean is 34 and its SD is 6.

   *Solution.* 100 × 16/40 = 40: mental age stops rising in the late teens, while chronological age keeps rising,
   so the quotient falls for every adult. A deviation IQ compares a person with their own age group:
   100 + 15 × (42 − 34)/6 = 120.
5. **Kelley's estimate.** With true scores normal and $X = T + E$, show that $E[T \mid X] = \mu + \rho\,(X - \mu)$, with $\rho$ the reliability. Estimate the true score behind 130 at $\rho = 0.9$.

   *Solution.* With T ~ N(μ, σ_T²) and E ~ N(0, σ_E²) independent, (T, X) is bivariate normal and
   E[T | X] = μ + (Cov(T, X)/Var X)(X − μ) = μ + (σ_T² / (σ_T² + σ_E²))(X − μ) = μ + ρ(X − μ). At 130 and ρ = 0.9:
   100 + 0.9 × 30 = 127. The posterior mean minimizes expected squared error.
6. **Brogden.** For a standard normal test $X$ and criterion $Y$ with correlation $r$, show that $E[Y \mid X > z] = r\,\phi(z) / (1 - \Phi(z))$. What do the top 20% average at $r = 0.4$?

   *Solution.* Y = rX + √(1 − r²)Z with Z independent of X, so E[Y | X > z] = r E[X | X > z] = r φ(z)/(1 − Φ(z)).
   For the top 20%, z = 0.842 and φ(z) = 0.280, so the gain is 0.4 × 0.280/0.2 = 0.56 SD.
7. ★ **Common cause against mutualism.** Design an experiment that could tell a common cause from mutualism, and say what each world predicts for every test when one ability is trained.

   *Solution.* Train one ability (for example, with practice on one test's skill) in a
   randomized group, and test every ability before, just after and months later. Under a common cause with no
   causal links, training a specific skill moves that test only (unless it moves g, in which case every test moves
   in proportion to its loading at once). Under mutualism, the trained ability moves first and the others follow,
   over time, in proportion to their couplings with it, and the effect spreads more to strongly linked abilities
   than to weakly linked ones. Under sampling, tests that share more bonds with the trained one move more. The
   design needs enough power to detect small transfer (chapter five's 0.075 SD needs thousands of people per arm),
   a delayed test, and an active control.

## Open checks

Checked against the articles, their abstracts or official pages (2026-11-15): Spearman's averages, pitch and music
correlations; Holzinger and Swineford's 301 children and the lavaan files' hashes; Thurstone's 56 tests and seven
factors; Thomson's 1916 dice; Carroll's more than 460 data sets; van der Maas et al.'s mutualism; Deary et al.'s
70,000 children, 0.81, 58.6%, 48% and 18.1%; Strenze's 0.56, 0.43 and 0.20; Sackett et al.'s .31; Calvin et al.'s
16 studies, 24%, 34% and 54%; Carpenter et al.'s 57%, FAIRAVEN and BETTERAVEN; Haworth et al.'s 11,000 pairs and
41/55/66%; Briley and Tucker-Drob's 11,500 pairs; Tucker-Drob and Bates's 24,926 pairs and the US-only interaction; Ritchie and Tucker-Drob's 142, 42, 600,000, 1.197–5.229 and 3.4; Ceci's 1991 review; Flynn's 13.8 points
and 14 nations; Wicherts et al.'s invariance result; Flore et al.'s 2,000 students; *Buck v. Bell*'s 8–1 and Holmes's
sentence; the Army Alpha and Beta; Snyderman and Herrnstein; Kamin's 0.771 and Hearnshaw's conclusion; Lewis et
al.'s 300 skulls; Gardner's 1983 seven and 1999 naturalist; Visser et al.'s positive manifold; Brackett and Mayer's
two kinds of measure; Rauscher, Shaw and Ky (Katherine N. Ky) and Pietschnig et al.'s 40 studies, 3,000 people and
d = 0.37; *Hall v. Florida*; DSM-5's three criteria; *Griggs* and the four-fifths rule; Kan et al. 2019, McFarland
2020 and the reply; Lee et al.'s 1.1 million and percentages; Howe et al.'s 178,000 siblings, 19 cohorts and 47%;
Chollet's definition and ARC.

Still to recheck against the full texts before the final cut:

* Schmidt and Hunter (1998): the single-predictor validity .51 (from two secondary sources; the ledger says "about
  .5").
* Spearman (1904): the subject block (.83 C–F, .78 C–E, .70 C–M, .67 F–E, .67 F–M, .64 E–M) as the widely
  reproduced table; it reproduces his stated averages exactly.
* Binet (1909): the "brutal pessimism" wording, p. 141 (from translations quoted in textbooks).
* Kelley (1927) and Brogden (1949): the formulas as attributed in secondary sources (they are derived in the
  problems).
* Goddard at Ellis Island: "small, selected groups" and the discrediting of the percentages (from historical
  summaries).
* Visser et al. (2006): the number of participants (not stated on screen).
* The number of Army recruits tested (sources give 1.5 to about 2 million; shown as "well over a million").
