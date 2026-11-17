# Psychology, Built: Part 33, Personality

In 1936 Gordon Allport and Henry Odbert read Webster's New International Dictionary for people and copied out
17,953 words that describe how one person differs from another. Fifty years of factor analysis reduced them to
five dimensions. In between, in 1968, Walter Mischel nearly ended the field by showing how weakly a trait predicts
any single act. The answer turned out to be a lesson in measurement, and the story ends with personality read from a
trail of clicks.

From the dictionary to Cattell's sixteen factors, Tupes and Christal's five, the NEO and the six-factor HEXACO; the
SAPA project's 25 public-domain items answered by 2,800 people, recomputed: parallel analysis, five ML factors with
varimax, alpha, the scales' correlations; the viewer predicts four numbers; types against traits, with the median
split's information loss and the arcsine law for retests; Hartshorne and May's honest and dishonest children and
Mischel's .30, rebuilt in a simulated world of people and situations; Epstein's aggregation and the Spearman-Brown
curve, Funder and Ozer's situational effects, Fleeson's distributions of states and if-then signatures; rank-order
stability, mean-level change and changing on purpose; heritability; temperament, from Kagan's high-reactive infants to
the Dunedin cohort and Clauss and Blackford's meta-analysis; Eysenck and Gray, and a multitrait-multimethod
table from real data; what traits predict and Soto's 78 replications, with the binomial effect-size display; Freud
under Part 3's standards; women and men in one dimension and in many; personality from footprints, Cambridge
Analytica and psychological targeting. The practice chapter is hiring, faking and personality products; the frontier
is traits as networks, language models that read people, and open questions.

## Where the numbers come from

| What | Source |
|---|---|
| The 25 items: 2,436 complete answers of 2,800; eigenvalues 5.13, 2.75, 2.14, 1.85, 1.55, then 1.07, against random 1.21, 1.18, 1.15, 1.14, 1.12, 1.10: five kept; every item loads most on its own factor (0.36 to 0.84 in size); alpha 0.72, 0.74, 0.77, 0.82, 0.61 (A, C, E, N, O); agreeableness and extraversion correlate 0.46 | SAPA project (psychTools `bfi`, fetched and checked by SHA-256); Psyche (`personality.score`, `parallel`), `statkit.multi.factor_ml`, `varimax`, `measure.cronbach_alpha`; item `factors` |
| Types: extraversion's median 4.2; 34% of people within half an SD of it; same type on one dimension 75%, 80% and 86% at reliability 0.7, 0.8, 0.9, and on four dimensions 31%, 40% and 54%; a median split keeps 0.80 of a correlation | SAPA data; Psyche (`personality.type_agreement`, `dichotomy_loss`), item `types` |
| The act world: 4,000 people, 40 situations, each visited twice; variance of one act 27% person, 10% situation, 10% signature, 53% noise; one act against another 0.29, averages of 2, 4, 8, 16 against as many others 0.46, 0.63, 0.77, 0.87 (Spearman-Brown 0.45, 0.62, 0.77, 0.87); the same situation twice 0.41 | Psyche (`personality.act_world`, `aggregate_curve`), item `acts` |
| Ages: bands 16-19 to 50-65 (475 to 189 people); agreeableness 4.36 to 4.98, neuroticism 3.26 to 2.72 (a cross-section) | SAPA data, item `ages` |
| EPI and BFI in 231 people: extraversion 0.54, neuroticism 0.63; cross-trait -0.18 to 0.04 | psychTools `epi.bfi`, item `eysenck` |
| Binomial effect-size display for r = 0.1, 0.2, 0.3: 55/45, 60/40, 65/35 | Psyche (`personality.besd`), item `outcomes` |
| Sexes: 919 men, 1,881 women; d (women minus men) A 0.45, C 0.20, E 0.23, N 0.27, O -0.13; D 0.65 on five scales (overlap 74%), 0.89 on 25 items (66%); mean single-item \|d\| 0.18; D = 2.71 means about 18% overlap by 2Φ(-D/2) | SAPA data; Psyche (`personality.mahalanobis`, `d_by_dimensions`, `overlap_d`), item `sexes` |
| Likes: 6,000 simulated people, 2,000 likes, about 150 per person; accuracy 0.08 with 5 likes, 0.32 with 100, 0.48 with 300, 0.75 with 2,000 | Psyche (`personality.likes_world`, `likes_accuracy`), item `likes` |
| Faking: 30% of applicants add 0.8 SD; hiring the top tenth, they are 62% of hires; hires' mean performance 0.41 against 0.43 SD with honest answers | Psyche (`personality.faking`), item `faking` |
| 17,953 words from about 400,000 entries | Allport and Odbert (1936) |
| 171 clusters, 16 factors, the 16PF in 1949 | Cattell |
| Five factors in eight samples | Tupes and Christal (1961) |
| NEO PI 1985; NEO PI-R 1992, 240 items, 30 facets | Costa and McCrae |
| Six factors in lexical studies in seven languages | Ashton, Lee et al. (2004) |
| Correlations rarely above about .30 | Mischel (1968) |
| Situational effects .36 to .42 | Funder and Ozer (1983) |
| Rank-order stability about .3, .6, .7 (152 studies) | Roberts and DelVecchio (2000) |
| 92 samples of mean-level change | Roberts, Walton and Viechtbauer (2006) |
| Two 16-week studies of wanting to change | Hudson and Fraley (2015) |
| 1,523 people, d = 0.52 and -0.58 self-reported, 0.35 by observers | Stieger et al. (2021) |
| Heritability .40 (twins .47, family and adoption .22), 62 estimates, >100,000 people | Vukasović and Bratko (2015) |
| 78 links, median N 1,504, 87% replicated, 77% as large | Soto (2019) |
| 46 meta-analyses, 30% near zero and 48% small | Hyde (2005) |
| 26 cultures, 23,031 people | Costa, Terracciano and McCrae (2001) |
| 55 nations, larger differences in more developed nations | Schmitt et al. (2008) |
| 16PF in 10,261 Americans, D = 2.71, about 10% overlap | Del Giudice, Booth and Irwing (2012) |
| 58,466 volunteers | Kosinski, Stillwell and Graepel (2013) |
| 10, 70, 150 and 300 likes; .56 against .49 | Youyou, Kosinski and Stillwell (2015) |
| About .3 to .4 | Azucar, Marengo and Settanni (2018) |
| About 270,000 app users, up to 87 million affected | Facebook's 2018 statements |
| Over 3.5 million people; up to 40% more clicks and 50% more purchases | Matz et al. (2017) |
| Conscientiousness valid for every criterion and group; composite validity about .31 | Barrick and Mount (1991); Mount and Barrick (1995) |
| 33 studies of applicants against non-applicants | Birkeland et al. (2006) |
| Average r = .29 from status updates | Peters and Matz (2024) |

## Built in this part

* `explainer/psychology/psyche/personality.py`: scoring with reverse keys; Horn's parallel analysis; a world of
  people and situations (trait, situational pull, if-then signature, noise) with single-act and aggregated
  consistency and variance components; type agreement on retest and the median split's loss; univariate d,
  Mahalanobis D, overlap and D by number of variables; the binomial effect-size display; simulated likes and ridge
  predictions; faking in selection. Tested in `tests/psychology/test_personality.py`.
* `explainer/psychology/opendata.py` fetches the SAPA `bfi` and the `epi.bfi` samples from psychTools' CRAN source
  package; the Archive gains `SAPA_BFI_2010` and `EPI_BFI`.
* The Ledger gains seven rows.
* The course's interactive is the 25-item inventory: the reader answers the SAPA items and sees five positions
  against the 2,800 people, with the error band each short scale carries.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Ratings and self-reports of personality are summarized by five broad recurring factors | Tupes and Christal 1961 | replicated |
| The same five factors describe personality in every human population | McCrae and Costa 1997 | contested |
| Personality traits predict consequential outcomes such as health, relationships and work | Roberts, Kuncel, Shiner, Caspi and Goldberg 2007 | replicated, smaller |
| Traits predict behaviour only up to about .30, so behaviour is mostly determined by situations | Mischel 1968 | story and record |
| People fall into distinct personality types that a questionnaire identifies reliably | Myers and Briggs 1962 | failed |
| Personality traits can be estimated from digital records such as likes | Kosinski, Stillwell and Graepel 2013 | replicated |
| Ads matched to a person's personality are substantially more persuasive | Matz, Kosinski, Nave and Stillwell 2017 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Allport and Odbert's word list,
Goldberg's naming and the NEO, the HEXACO lexical studies, Jung and the type indicator's history, Hartshorne and
May, Roberts and DelVecchio, Roberts et al.'s mean-level change, Hudson and Fraley, Stieger et al., Vukasović and
Bratko, Eysenck and Gray, Westen and Kihlstrom, Rorschach and Lilienfeld et al., Hyde, Costa et al., Schmitt et al.,
Del Giudice et al., Barrick and Mount, Birkeland et al., Cramer et al., and Peters and Matz (also in the likes row).

## Build it

```bash
python -m videos.psychology.psych33.compute            # every number (about a minute; fetches psychTools once)
python tools/qa_scene.py psych33 Aggregation           # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych33 -q l   # the whole part, silent preview
python tools/build.py psych33                          # 1080p30 with narration
python tools/qa_scene.py psych33 Types --lang zh       # the Chinese edition of one chapter
python tools/make.py psych33                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 33                    # the lab: factors, aggregation, types, sex differences
python tools/check_ledger.py psych33                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's personality module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 1936: a dictionary, read for people | The word list; three turns; the question; objectives |
| 1 | From words to five | Cattell, Tupes and Christal, Norman, Goldberg; the five; the NEO; HEXACO |
| 2 | Five factors in 2,800 people | The items; parallel analysis; rotated loadings; scales, alpha and their correlations |
| 3 | On you: four numbers | Four predictions; the inventory |
| 4 | Types against traits | Jung, Briggs and Myers; one hump; the arcsine law on retest |
| 5 | The person and the situation | Studies in Deceit; Mischel's .30; Psyche's world of acts |
| 6 | Many acts | Aggregation and Spearman-Brown; Funder and Ozer; Fleeson and if-then signatures |
| 7 | Stability and change | Rank-order stability; mean-level change; changing on purpose |
| 8 | Where traits come from | Heritability; Eysenck and Gray; two tests, two traits |
| 9 | What traits predict | The power of personality; 78 replications; what a small correlation means |
| 10 | Freud, under Part 3's standards | The tradition; what survived; inkblots, measured |
| 11 | Women and men | Mostly similar; the SAPA differences; many dimensions at once; the dispute |
| 12 | Personality from footprints | Likes; who knows you best; from measuring to persuading |
| 13 | The Ledger | Seven rows: five factors, universality, outcomes, person and situation, types, likes, targeting |
| 14 | In practice: hiring, faking and fit | Personality at work; faking; products judged |
| 15 | Frontier: causes, change and machines | Networks against latent traits; language models; open questions |
| | Recap, problems, and the road ahead | Your numbers; ten lines; Kant's three objections; payoffs; problems; references; Part 34 |

## Sources

* G. W. Allport and H. S. Odbert, Trait-names: a psycho-lexical study, *Psychological Monographs* 47 (211) (1936).
* R. B. Cattell, the 16PF (1949); E. C. Tupes and R. E. Christal, Recurrent personality factors based on trait
  ratings, USAF technical report (1961); W. T. Norman (1963); L. R. Goldberg (1981, 1990); P. T. Costa and R. R.
  McCrae, NEO PI (1985) and NEO PI-R (1992); R. R. McCrae and P. T. Costa, *American Psychologist* 52 (1997)
  509–516; M. C. Ashton, K. Lee et al., *Journal of Personality and Social Psychology* 86 (2004).
* W. Revelle and colleagues, the SAPA project; the `bfi` and `epi.bfi` data in the R package psychTools 2.6.4 (CRAN,
  GPL); L. R. Goldberg's International Personality Item Pool (public domain).
* J. L. Horn, A rationale and test for the number of factors in factor analysis, *Psychometrika* 30 (1965).
* C. G. Jung, *Psychological Types* (1921); I. B. Myers, the MBTI manual (Educational Testing Service, 1962); D. J.
  Pittenger, *Review of Educational Research* 63 (1993) 467–488.
* H. Hartshorne and M. A. May, *Studies in Deceit* (Macmillan, 1928); W. Mischel, *Personality and Assessment*
  (1968); S. Epstein, *Journal of Personality and Social Psychology* 37 (1979); D. C. Funder and D. J. Ozer,
  *Journal of Personality and Social Psychology* 44 (1983) 107–112; W. Fleeson, *Journal of Personality and Social
  Psychology* 80 (2001) 1011–1027; W. Mischel and Y. Shoda, *Psychological Review* 102 (1995).
* B. W. Roberts and W. F. DelVecchio, *Psychological Bulletin* 126 (2000) 3–25; B. W. Roberts, K. E. Walton and W.
  Viechtbauer, *Psychological Bulletin* 132 (2006); N. W. Hudson and R. C. Fraley, *Journal of Personality and
  Social Psychology* (2015); M. Stieger et al., *PNAS* 118 (2021).
* T. Vukasović and D. Bratko, *Psychological Bulletin* 141 (2015) 769–785; J. A. Gray (1970); H. J. Eysenck.
* B. W. Roberts, N. R. Kuncel, R. Shiner, A. Caspi and L. R. Goldberg, *Perspectives on Psychological Science* 2
  (2007) 313–345; C. J. Soto, *Psychological Science* 30 (2019); R. Rosenthal and D. B. Rubin, the binomial
  effect-size display (1982).
* D. Westen, The scientific legacy of Sigmund Freud, *Psychological Bulletin* 124 (1998); J. F. Kihlstrom's
  critique; H. Rorschach, *Psychodiagnostik* (1921); S. O. Lilienfeld, J. M. Wood and H. N. Garb, *Psychological
  Science in the Public Interest* 1 (2000).
* J. S. Hyde, *American Psychologist* 60 (2005) 581–592; P. T. Costa, A. Terracciano and R. R. McCrae, *Journal of
  Personality and Social Psychology* 81 (2001) 322–331; D. P. Schmitt et al., *Journal of Personality and Social
  Psychology* 94 (2008); M. Del Giudice, T. Booth and P. Irwing, *PLoS ONE* 7 (2012) e29265.
* M. Kosinski, D. Stillwell and T. Graepel, *PNAS* 110 (2013) 5802–5805; W. Youyou, M. Kosinski and D. Stillwell,
  *PNAS* 112 (2015) 1036–1040; D. Azucar, D. Marengo and M. Settanni, *Personality and Individual Differences* 124
  (2018) 150–159; S. C. Matz et al., *PNAS* 114 (2017); D. Eckles, B. R. Gordon and G. A. Johnson, *PNAS* 115
  (2018); H. Peters and S. C. Matz, *PNAS Nexus* (2024).
* M. R. Barrick and M. K. Mount, *Personnel Psychology* 44 (1991) 1–26; S. A. Birkeland et al., *International
  Journal of Selection and Assessment* 14 (2006) 317–335.
* A. O. J. Cramer et al., Dimensions of normal personality as networks in search of equilibrium, *European Journal
  of Personality* 26 (2012) 414–431; M. Gurven et al., *Journal of Personality and Social Psychology* 104 (2013)
  354–370; R. Laajaj et al., *Science Advances* 5 (2019).
* D. C. Funder, *The Personality Puzzle* (Norton).

## Problems and solutions

1. **Aggregation.** The average of k situations is T + ū + ē, with Var(ū + ē) = σ_e²/k (the situational parts and
   noise independent across situations). Two such averages over different situations share only T, so their
   correlation is σ_T² / (σ_T² + σ_e²/k) = kρ/(1 + (k − 1)ρ) with ρ = σ_T²/(σ_T² + σ_e²): the Spearman-Brown formula.
   With ρ = 0.29, k = 16 gives 0.87.
2. **The arcsine law.** For a standard bivariate normal with correlation r, P(X > 0, Y > 0) = 1/4 + arcsin(r)/(2π)
   (Sheppard's orthant probability), so P(same side) = 2 × that = 1/2 + arcsin(r)/π. At r = 0.8 this is 0.795, and
   for four independent dimensions 0.795⁴ = 0.40.
3. **The median split.** For X standard normal and D = sign(X), Cov(X, D) = E|X| = √(2/π) and Var(D) = 1, so the
   correlation is √(2/π) ≈ 0.80. Any correlation of X with Y passing through X alone shrinks by this factor.
4. **D in many dimensions.** With independent unit-variance traits the pooled covariance is the identity, so D² is
   the sum of the squared differences: D = d√p. For d = 0.2 and p = 25, D = 1.0 and the overlap is 2Φ(−0.5) = 0.62.
   (The SAPA items are correlated, which is why their D is 0.89 rather than 0.18 × 5.)
5. **Reverse keys.** On a 1-to-6 scale, x and 7 − x have the same distance from the midpoint 3.5 on opposite sides,
   so 7 − x reverses the item without changing its spread. Left unreversed, a reverse-keyed item correlates
   negatively with the others, lowering the sum's variance relative to the items' and so lowering alpha, which can
   even become negative.
6. **The effect-size display.** Two median splits with a 2 × 2 table of shares p, 1/2 − p, 1/2 − p, p have phi
   coefficient (p − 1/4)/(1/4) = 4p − 1 = r, so p = (1 + r)/4, and the success rate in the upper half is p/(1/2) =
   (1 + r)/2 = 50 + 50r percent.
7. ★ **Conscientiousness and longevity.** Observational data confound conscientiousness with income, education,
   health and childhood circumstances. A design: a prospective cohort measuring conscientiousness in childhood
   (before most adult confounders), with siblings compared to remove shared family factors; mediators measured over
   time (smoking, diet, adherence to treatment) to trace mechanisms; and, for causality, randomized trials of a
   conscientiousness intervention (like Stieger et al.'s) with health behaviours as outcomes. Each part removes a
   different confounder: timing removes adult reverse causation, siblings remove the family, randomization removes
   the rest, at the cost of measuring short-run behaviour rather than death.

## Open checks

Checked against the articles, their abstracts or official pages (2026-11-15): Allport and Odbert's 17,953 words and
the dictionary; Cattell's 171 terms and the 1949 16PF; Tupes and Christal's eight samples and the Air Force report;
Goldberg's naming; the NEO's history; Ashton et al.'s seven languages; McCrae and Costa's six translations; Gurven et
al.'s 632 Tsimane; Laajaj et al.'s 94,751 respondents in 23 countries; the psychTools files' hashes and the 6-point
scale; Jung 1921 and the indicator's history to the 1962 manual; Mischel's .30; Epstein's aggregation; Funder and
Ozer's .36 to .42; Fleeson's distributions; Roberts and DelVecchio's 152 studies and the rounded .3/.6/.7; Roberts,
Walton and Viechtbauer's 92 samples; Hudson and Fraley's two 16-week studies; Stieger et al.'s 1,523 people and the
effect sizes; Vukasović and Bratko's .40, .47 and .22; Roberts et al. 2007's comparison; Soto's 78, 1,504, 87% and
77%; Westen's propositions and Kihlstrom's reply; Rorschach's 1921 monograph; Lilienfeld, Wood and Garb's
conclusions; Hyde's 46 meta-analyses; Costa et al.'s 26 cultures; Schmitt et al.'s 55 nations; Del Giudice et al.'s
10,261 people and D = 2.71; Kosinski et al.'s 58,466; Youyou et al.'s thresholds and .56/.49; Azucar et al.'s range;
the 270,000 and 87 million; Matz et al.'s 3.5 million, 40% and 50%; Eckles et al.'s critique; Barrick and Mount;
Birkeland et al.'s 33 studies; Cramer et al.; Peters and Matz's .29.

Still to recheck against the full texts before the final cut (the web-search budget ran out while this part was
being written):

* Hartshorne and May (1928): the number of children and the size of the cross-test correlations (described without
  numbers).
* Pittenger (1993): the exact retest figures for type changes (the film computes its own instead).
* Roberts et al. (2007): the specific effect sizes (described only as comparable to SES and cognitive ability).
* Del Giudice et al. (2012): the number of 16PF factors in their model (not stated on screen).
* Fleeson (2001): the sampling schedule ("several times a day").
* The first names of Warren Norman, Kibeom Lee and Mirjam Stieger, and the honesty-humility descriptors.
* Eysenck's arousal account of extraversion, and the phrase "maturity principle" (standard textbook accounts).
* Milgram's procedure for the Part 34 teaser (kept to "in the early 1960s, at Yale").
