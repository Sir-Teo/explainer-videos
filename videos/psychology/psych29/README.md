# Psychology, Built: Part 29, Emotion

In 1884 William James asked whether we run from a bear because we are afraid, or are afraid because we run, and
answered: the second. This part follows the argument about the order of events, from the body and the label to
faces, appraisals and fear circuits, and on to forecasting, money and a famous number. It recomputes a map of
feelings from data collected in 1962, and a facial-feedback meta-analysis from its open table.

James and Lange's body first, and Cannon's objections with Cannon–Bard; Marañón's "as if" emotions and Schachter and
Singer's adrenaline, written as Bayesian attribution of unexplained arousal; the Capilano bridge; Darwin, Ekman and
Friesen in New Guinea, forced choice and free sorting; Abelson and Sermat's thirteen faces rescaled by classical MDS
into a pleasantness–tension map, then a simulated observer's same-or-different judgments of ten schematic faces
recovered by MDS and Procrustes; constructed emotion and core affect; the pen in the teeth, seventeen laboratories,
the camera, and 286 effects pooled from the open data, with groups by manipulation and publication and the
precision-effect test; an appraisal model that labels six scenarios; LeDoux's two roads and a stick-or-snake
circuit; S.M.; stress, the process model, reappraisal against suppression; the impact bias, an adaptation model and
lottery winners; the 2010 plateau and the 2021 no-plateau reconciled in a simulated world and by the 2023
adversarial collaboration, and the Easterlin paradox across people, countries and years, with Deaton's and
Stevenson and Wolfers's replies and Easterlin's; and the critical positivity ratio, the Lorenz equations and how they were taken apart.
The practice chapter is emotion-recognition software, well-being statistics and reappraisal in therapy; the
frontier is interoceptive inference, emotion in animals, and affect in machines.

## Where the numbers come from

| What | Source |
|---|---|
| Attribution: arousal 1.2 (σ = 0.5, exponential prior of mean 0.3 on the situation's share); attributed to the situation 0.56 with no explanation, 0.24 when an injection of size 1 is explained, 0.25 for a placebo's arousal 0.3 | Psyche (`emotion.attribution`), item `attribution` |
| Abelson and Sermat's 13 faces: classical MDS of the 13 × 13 dissimilarities; two dimensions carry 84% of the positive eigenvalues (the first 52%); the rated scales fit the map with R = 0.94 (pleasantness), 0.94 (tension) and 0.81 (attention–rejection) | `opendata.faces_1962` (smacof's `FaceExp` and `FaceScale`), item `faces` |
| Ten schematic faces, 45 pairs judged "different" with probability logistic((distance − 0.9)/0.35): the MDS map matches the true plane with r = 0.68 (each pair once), 0.82 (three times), 0.98 (ten times) | Psyche (`emotion.pairs_map`, seed 29), item `pairs` |
| Facial feedback: 286 effects from 138 studies, pooled within study first; random-effects d = 0.199 [0.143, 0.254], τ² = 0.078, I² = 81%; precision-effect intercept 0.196 (SE 0.059); posing an expression 0.45 (58 effects), suppressing one 0.15 (151), exaggerating one 0.05 (36), unobtrusive manipulations 0.19 (88); published 0.25 (229), unpublished 0.14 (57) | Coles, Larsen and Lench (2019) (`opendata.coles_2019`, psymetadata 1.0.1), item `feedback` |
| Strack, Martin and Stepper: 0.82 points; the Registered Replication Report: 17 laboratories, 0.03 [−0.11, 0.16] | Wagenmakers et al. (2016) |
| Many Smiles: 3,878 people in 19 countries | Coles et al. (2022) |
| Appraisal: six scenarios on six dimensions; labels anger 0.95, fear 0.81, pride 0.86, sadness 0.95, hope 0.87, guilt 0.91 (prototypes after Smith and Ellsworth and Scherer, values illustrative) | Psyche (`emotion.appraise`, β = 3), item `appraisal` |
| Two roads: thalamic drive at 15 ms, cortical identification at 60 ms (illustrative); stick and snake both reach 0.54 before the cortex reports; the snake settles at 1.4, the stick at 0, no amygdala gives nothing | Psyche (`emotion.two_roads`), item `fear` |
| Forecasting: impact 3, experienced τ = 20 days, forecast τ = 150 days (illustrative); at day 60 the experience is 0.15 and the forecast 2.01 | Psyche (`emotion.forecast`), item `forecast` |
| Brickman, Coates and Janoff-Bulman: present happiness 4.00 (22 lottery winners), 3.82 (22 controls), 2.96 (29 people paralysed in accidents) | Brickman, Coates and Janoff-Bulman (1978) |
| Income: 200,000 simulated people, log income normal around $60,000; happiness rises 0.35 per doubling for most; a fifth gain only up to $100,000 and sit 1.8 lower; the mean keeps rising while the 10th percentile flattens above about $118,000 | Psyche (`emotion.income_world`), item `income` |
| Kahneman and Deaton: about 450,000 Gallup responses, a plateau near $75,000; Killingsworth: 1,725,994 reports from 33,391 employed adults; the 2023 reanalysis: a plateau above about $100,000 for the least happy 20% only | Kahneman and Deaton (2010); Killingsworth (2021); Killingsworth, Kahneman and Mellers (2023) |
| The Lorenz attractor: σ = 10, ρ = 28, β = 8/3, 30 time units by RK4 | Psyche (`emotion.lorenz`), item `lorenz` |
| The positivity ratio: 2.9013 and about 11.6; 188 people's daily reports over 28 days | Fredrickson and Losada (2005) |

## Built in this part

* `explainer/psychology/psyche/emotion.py`: classical (Torgerson) scaling, scale fitting and Procrustes; ten
  schematic faces on a valence–arousal plane and a same-or-different observer; arousal attribution on a grid; an
  appraisal model with nine emotion prototypes on six dimensions; LeDoux's two roads as a leaky integrator; hedonic
  adaptation and a forecaster; a simulated population for income and happiness; the Lorenz system by RK4. Tested in
  `tests/psychology/test_emotion.py`.
* `explainer/psychology/rdata.py` reads ALTREP objects (compact sequences, wrappers, deferred strings), which newer
  R versions write into package data; any other ALTREP class is refused, and nothing is evaluated.
* `explainer/psychology/opendata.py` fetches smacof 2.1-7 (`FaceExp`, `FaceScale`) and psymetadata 1.0.1
  (`coles2019`) from CRAN and checks both the archives and the data members by SHA-256 (`faces_1962`,
  `coles_2019`); the Archive registers them (`FACES_1962`, `COLES_2019`).
* The Ledger gains six rows.
* The course's interactive is the face-pair task on you: 45 pairs of ten schematic faces, same feeling or
  different, then the map your judgments make, rotated onto the true plane, with its correlation.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Unexplained arousal is felt as whatever emotion the situation suggests | Schachter and Singer 1962 | contested |
| Men who met a woman on a frightening bridge were more attracted to her | Dutton and Aron 1974 | not directly tested |
| People in every culture recognize the same six emotions from the same faces | Ekman and Friesen 1971 | contested (replicated with forced choice) |
| Moving the face into an expression changes the emotion felt | Strack, Martin and Stepper 1988 | replicated, smaller |
| Emotional well-being rises with income, but stops rising above a moderate income | Kahneman and Deaton 2010 | replicated (its scope resolved) |
| People flourish when their ratio of positive to negative emotions exceeds 2.9013 | Fredrickson and Losada 2005 | retracted (the modelling) |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: the history of emotion theory
(James, Lange, Cannon, Bard, Marañón, Darwin), interoception theories (Craig, Damasio), basic-emotion and
construction theories (Ekman, Russell, Barrett), the meta-analyses of physiology and brain imaging (Siegel et al.,
Lindquist et al.), appraisal theory, LeDoux's anatomy and later argument, the S.M. case study, stress and coping,
Gross's regulation studies, the impact bias, the lottery study (with its limits stated) and Lucas's review, the
1962 face data (a method demonstration), and the frontier's theories and studies.

## Build it

```bash
python -m videos.psychology.psych29.compute            # every number (under a minute; fetches two CRAN packages once)
python tools/qa_scene.py psych29 Feedback              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych29 -q l   # the whole part, silent preview
python tools/build.py psych29                          # 1080p30 with narration
python tools/qa_scene.py psych29 Map --lang zh         # the Chinese edition of one chapter
python tools/make.py psych29                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 29                    # the lab: scaling, Procrustes, the meta-analysis, appraisal
python tools/check_ledger.py psych29                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's emotion module, rdata, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | James's bear | James and Lange; two orders of events; the questions; objectives |
| 1 | Body first? | Cannon's objections and Cannon–Bard; Marañón's injections; interoception and somatic markers |
| 2 | Two factors | Schachter and Singer; attribution as inference, derived; the replications; the Capilano bridge |
| 3 | Faces | Darwin; Ekman and Friesen in New Guinea; forced choice and free sorting; the 2019 review |
| 4 | On you: the map of feelings | Abelson and Sermat's faces; classical scaling derived; the map and its scales; the face-pair task on you and Psyche |
| 5 | Constructed emotion | Core affect; variation within categories; the best case for each side |
| 6 | Facial feedback | The pen; seventeen laboratories; the camera; the meta-analysis recomputed; Many Smiles |
| 7 | Appraisal | Lazarus; Smith and Ellsworth's dimensions; an appraisal model on six scenarios |
| 8 | Fear in the brain | LeDoux's two roads; a stick or a snake; S.M.; defence or fear |
| 9 | Stress and regulation | Selye's loop and Lazarus and Folkman's appraisal; Gross's process model; reappraisal against suppression |
| 10 | Affective forecasting | A forecast on you; the impact bias; adaptation derived; lottery winners and accident victims |
| 11 | Happiness and income | The 2010 plateau and the 2021 no-plateau; one world with both; the adversarial collaboration |
| 12 | The critical positivity ratio | 2.9013; the Lorenz equations; the 2013 critique and withdrawal |
| 13 | The Ledger | Two factors; the bridge; six faces; facial feedback; money; the ratio |
| 14 | In practice: machines that read faces, well-being, therapy | Emotion recognition by machine; well-being statistics; reappraisal taught |
| 15 | Frontier: the body, animals and machines | Interoceptive inference; emotion in animals; affect in machines; open problems |
| | Recap, problems, and the road ahead | Your forecast checked; ten lines; Kant's three objections; payoffs; problems; references; Part 30 |

## Sources

Body and label: W. James, What is an emotion?, Mind 9 (1884) 188-205; C. Lange, *Om Sindsbevægelser* (1885);
W. B. Cannon, The James-Lange theory of emotions: a critical examination and an alternative theory, American
Journal of Psychology 39 (1927) 106-124; P. Bard, A diencephalic mechanism for the expression of rage, American
Journal of Physiology 84 (1928) 490-515; G. Marañón, Contribution à l'étude de l'action émotive de l'adrénaline,
Revue Française d'Endocrinologie 2 (1924) 301-325; A. D. Craig, How do you feel -- now? The anterior insula and human
awareness, Nature Reviews Neuroscience 10 (2009) 59-70; A. R. Damasio, *Descartes' Error* (1994); the two-factor and
bridge rows' references in the Ledger.

Faces and construction: C. Darwin, *The Expression of the Emotions in Man and Animals* (1872); P. Ekman, An argument
for basic emotions, Cognition and Emotion 6 (1992) 169-200; J. A. Russell, A circumplex model of affect, Journal of
Personality and Social Psychology 39 (1980) 1161-1178; J. A. Russell, Core affect and the psychological
construction of emotion, Psychological Review 110 (2003) 145-172; L. F. Barrett, *How Emotions Are Made* (2017);
E. H. Siegel et al., Emotion fingerprints or emotion populations? A meta-analytic investigation of autonomic features
of emotion categories, Psychological Bulletin 144 (2018) 343-393; K. A. Lindquist, T. D. Wager, H. Kober,
E. Bliss-Moreau and L. F. Barrett, The brain basis of emotion: a meta-analytic review, Behavioral and Brain Sciences
35 (2012) 121-143; the universal-expressions row's references in the Ledger.

Scaling: R. P. Abelson and V. Sermat, Multidimensional scaling of facial expressions, Journal of Experimental
Psychology 63 (1962) 546-554; W. S. Torgerson, Multidimensional scaling: I. Theory and method, Psychometrika 17
(1952) 401-419; P. H. Schönemann, A generalized solution of the orthogonal Procrustes problem, Psychometrika 31
(1966) 1-10.

Facial feedback: the facial-feedback row's references in the Ledger.

Appraisal, fear and regulation: R. S. Lazarus, *Psychological Stress and the Coping Process* (1966); C. A. Smith and
P. C. Ellsworth, Patterns of cognitive appraisal in emotion, Journal of Personality and Social Psychology 48 (1985)
813-838; K. R. Scherer, Appraisal considered as a process of multilevel sequential checking, in *Appraisal Processes
in Emotion* (2001); J. E. LeDoux, *The Emotional Brain* (1996); J. E. LeDoux, *Anxious* (2015); J. S. Feinstein,
R. Adolphs, A. Damasio and D. Tranel, The human amygdala and the induction and experience of fear, Current Biology 21
(2011) 34-38; J. S. Feinstein et al., Fear and panic in humans with bilateral amygdala damage, Nature Neuroscience 16
(2013) 270-272; H. Selye, *The Stress of Life* (1956); R. S. Lazarus and S. Folkman, *Stress, Appraisal, and Coping*
(1984); J. J. Gross, Antecedent- and response-focused emotion regulation, Journal of Personality and Social
Psychology 74 (1998) 224-237; J. J. Gross and O. P. John, Individual differences in two emotion regulation
processes, Journal of Personality and Social Psychology 85 (2003) 348-362.

Forecasting and well-being: D. T. Gilbert, E. C. Pinel, T. D. Wilson, S. J. Blumberg and T. P. Wheatley, Immune
neglect: a source of durability bias in affective forecasting, Journal of Personality and Social Psychology 75
(1998) 617-638; T. D. Wilson and D. T. Gilbert, Affective forecasting: knowing what to want, Current Directions in
Psychological Science 14 (2005) 131-134; P. Brickman, D. Coates and R. Janoff-Bulman, Lottery winners and accident
victims: is happiness relative?, Journal of Personality and Social Psychology 36 (1978) 917-927; R. E. Lucas,
Adaptation and the set-point model of subjective well-being, Current Directions in Psychological Science 16 (2007)
75-79; the money and positivity-ratio rows' references in the Ledger; E. N. Lorenz, Deterministic nonperiodic flow,
Journal of the Atmospheric Sciences 20 (1963) 130-141.

Practice and frontier: Regulation (EU) 2024/1689 (the AI Act), Article 5(1)(f); Office for National Statistics,
Personal well-being user guidance; A. K. Seth, Interoceptive inference, emotion, and the embodied self, Trends in
Cognitive Sciences 17 (2013) 565-573; L. F. Barrett and W. K. Simmons, Interoceptive predictions in the brain, Nature
Reviews Neuroscience 16 (2015) 419-429; R. Schandry, Heart beat perception and emotional experience,
Psychophysiology 18 (1981) 483-488; G. Zamariola, P. Maurage, O. Luminet and O. Corneille, Interoceptive accuracy
scores from the heartbeat counting task are problematic: evidence from simple bivariate correlations, Biological
Psychology 137 (2018) 12-17; J. Panksepp and J. Burgdorf, "Laughing" rats and the evolutionary antecedents of human
joy?, Physiology and Behavior 79 (2003) 533-547; D. J. Anderson and R. Adolphs, A framework for studying emotions
across species, Cell 157 (2014) 187-200; W. T. Gibson et al., Behavioral responses to a repetitive visual threat
stimulus express a persistent state of defensive arousal in Drosophila, Current Biology 25 (2015);
R. W. Picard, *Affective Computing* (1997).

Data: smacof 2.1-7 (`FaceExp`, `FaceScale`, GPL-3) and psymetadata 1.0.1 (`coles2019`, GPL-3), from CRAN, fetched
and never redistributed.

## Problems and solutions

1. **Classical scaling.** Show that double-centring the squared distances, $B = -\tfrac12 J D^{(2)} J$ with $J = I - \tfrac1n \mathbf{1}\mathbf{1}^\top$, gives $B = X X^\top$ for centred points $X$. Why are its top eigenvectors the best $k$-dimensional map?

   *Solution.* With centred points, D⁽²⁾ᵢⱼ = |xᵢ|² + |xⱼ|² − 2xᵢ·xⱼ. The first two terms are constant
   along a column or a row, so double-centring removes them, and the mean of xᵢ·xⱼ over i or j is zero because X is
   centred. So −½ J D⁽²⁾ J = X Xᵀ. The best rank-k approximation of B in squared error (Eckart–Young) keeps its top k
   eigenpairs, and the map is V_k Λ_k^(1/2).
2. **Procrustes.** Show that the rotation $R$ maximizing $\mathrm{tr}(R^\top X^\top Y)$ is $U V^\top$, where $X^\top Y = U \Sigma V^\top$.

   *Solution.* tr(RᵀXᵀY) = tr(RᵀUΣVᵀ) = tr(ΣVᵀRᵀU) = Σᵢ σᵢ zᵢᵢ, with Z = VᵀRᵀU orthogonal, so |zᵢᵢ| ≤ 1.
   The sum is largest when Z = I, that is R = UVᵀ.
3. **Attribution.** In the attribution model, arousal $a \sim N(s + c, \sigma^2)$ with an exponential prior of mean $m$ on $s \geq 0$. Show that the posterior of $s$ is a normal with mean $a - c - \sigma^2/m$, truncated at 0.

   *Solution.* The posterior is proportional to exp(−s/m) exp(−(a − c − s)²/2σ²). Completing the square,
   −(a − c − s)²/2σ² − s/m = −(s − (a − c − σ²/m))²/2σ² + const, so on s ≥ 0 it is a normal with mean
   a − c − σ²/m truncated at 0. An explanation c moves arousal away from the situation one for one, until the
   truncation takes over: the informed subjects feel little.
4. **The forecaster.** For $h(t) = I e^{-t/\tau}$, show that a forecaster with time constant $\tau_p$ overstates the total extra happiness by the factor $\tau_p / \tau$, and find when the forecast is twice the experience.

   *Solution.* The total extra happiness is ∫₀^∞ I e^(−t/τ) dt = Iτ, and the forecast's is Iτ_p, so the
   forecast overstates it by τ_p/τ. The ratio at time t is e^(t(1/τ − 1/τ_p)), which is 2 at t = ln 2 · ττ_p/(τ_p −
   τ): 16 days for τ = 20 and τ_p = 150.
5. **The meta-analysis.** With the meta-analysis table (`opendata.coles\_2019`), recompute $\hat\tau^2$, $I^2$ and the PET intercept. What does PET assume about small studies?

   *Solution.* Pooled within study first, τ² = 0.078, I² = 81% and the precision-effect intercept 0.196
   (SE 0.059), against a random-effects 0.199. PET regresses effects on their standard errors and reads the
   intercept as the effect of an infinitely precise study; it assumes that any small-study asymmetry comes from
   selection and is linear in the standard error. Here the intercept matches the pool, so the funnel shows little
   asymmetry at the study level, although unpublished effects (0.14) are smaller than published ones (0.25).
6. **The hidden plateau.** In a world where a share $q$ of people stop gaining above $x^*$ (and sit below the rest), show that the mean's slope above $x^*$ falls to $(1 - q)$ of its value, and that the 10th percentile flattens only if $q > 0.1$.

   *Solution.* Above x*, the mean is (1 − q)(b log x + c₁) + q c₂, with slope (1 − q)b. If the capped
   group sits below everyone else, the p-th percentile lies inside it whenever p < q, so the 10th percentile goes
   flat above x* only if q > 0.1; for q = 0.2 the 10th flattens and the mean keeps rising.
7. ★ **Construction against basic emotions.** Design a study that the constructed-emotion account and the basic-emotion account predict differently, and say what each predicts.

   *Solution.* The basic-emotion account predicts a pattern (in the face, the body or
   the brain) for each emotion that holds across situations and cultures; the constructed account predicts patterns
   that classify within a situation and fail to transfer, and perception that depends on emotion concepts. For
   example: induce fear, anger and sadness in several different situations each, measure autonomic and facial
   responses, train a classifier on some situations and test it on new ones; and, separately, make emotion words
   temporarily less available (by repetition) before people judge faces. Transfer across situations, unaffected by
   the words, favours basic emotions; classification that holds only within a situation, and judgments that shift
   with the words, favour construction.

## Open checks

Checked against the articles, their abstracts or official pages (2026-11-15): Brickman et al.'s 4.00, 3.82 and
2.96 (73 people); Killingsworth's 1,725,994 reports from 33,391 adults; the 2023 plateau for the least happy 20%;
Schachter and Singer's 185 men and Suproxin; Wagenmakers et al.'s 17 laboratories and 0.03 [−0.11, 0.16] against
0.82; Many Smiles' 3,878 people in 19 countries; Coles et al.'s 286 effects from 138 studies; Barrett et al.'s
scowling in about a quarter of anger; Gendron et al.'s Himba and 36 photographs; S.M. in 2011 and the carbon dioxide
study in 2013; Gross's 120 people and the disgust film; Gilbert et al.'s tenure study; Dutton and Aron's 50% and
12.5% (9 of 18 and 2 of 16) of the men who took the number; Fredrickson and Losada's 188 people over 28 days and
the 2.9013 and 11.6 thresholds; Nick Brown as a graduate student at the University of East London; the journal's
withdrawal of the modelling; Siegel et al.'s 202 studies and no one-to-one autonomic mapping; Lindquist et al.'s
"little evidence" for localization; HireVue's removal of facial analysis in 2020, announced in January 2021; the
AI Act's prohibition of emotion recognition in workplaces and schools from 2 February 2025, with medical and safety
exceptions (law-firm summaries; the Official Journal text not read); the ONS's four questions on a 0 to 10 scale
since April 2011, about a minute and a half to ask, and higher ratings by phone; Panksepp and Burgdorf's 50 kHz
chirps; Gibson et al.'s persistent, scalable state in flies; Zamariola et al.'s critique of the heartbeat counting
task and the 2020 replies.

Still to recheck against the full texts before the final cut:

* The Capilano bridge's height, "about seventy metres" (230 feet in secondary sources; the paper gives 450 feet long
  and five feet wide).
* Lindquist et al. (2012): the amygdala's responses to novel or relevant stimuli, as summarized on screen.
* Marañón (1924): the "as if" reports and the article's citation, from secondary sources.
* Lucas (2007): disability and long unemployment as lasting changes; Gross and John (2003): habitual reappraisers'
  and suppressors' well-being.
* Craig (2009) and Damasio (1994) are summarized, not quoted; Panksepp's seven systems are named as in his later
  books.
* Kahneman and Deaton's "about 450,000" responses, quoted from the abstract.
