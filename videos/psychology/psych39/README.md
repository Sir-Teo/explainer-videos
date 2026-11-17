# Psychology, Built: Part 39, What Is a Disorder?

The first part of Act X opens with the care card: this is education, not diagnosis or treatment, and here is where
help is found. In 1973 *Science* published a study in which eight healthy people faked one symptom, were admitted to
psychiatric hospitals and were never detected. It helped force a revolution in diagnosis: explicit criteria, checked
for agreement between clinicians. Decades later a journalist looked for the eight and found serious reason to doubt
the study. Reliability was won; validity is still open; and the alternatives to categories are mathematical.

The hook is Rosenhan's study and what the archive showed; the viewer works out what a positive screen means and
predicts four numbers. Then a short history from moral treatment to DSM-III; four candidate definitions of disorder,
Wakefield's harmful dysfunction, and the 1973 removal of homosexuality from the manual and the 1974 vote; Engel's
biopsychosocial model and its critique, and the diathesis-stress frame from Meehl to Zubin and Spring; Cohen's
kappa derived, the DSM-5 field trials' kappas, and a simulation in which reliability caps validity (computed);
Robins and Guze's validators, the 227 symptom combinations that meet one diagnosis (counted), and 1,030 profiles
among 3,703 patients; categories against dimensions and the taxometric evidence; comorbidity, a positive manifold
(computed) and the p factor; a symptom network with hysteresis and an episode that starts suddenly and ends slowly
(computed); prevalence and age of onset; a map of the manual (DSM-5-TR and ICD-11) marking which parts treat each
group; the eating disorders (prevalence, mortality, treatments with trials) and the personality disorders (ICD-11's
severity model, Zanarini's ten-year follow-up); the treatment gap and the treatment-prevalence paradox; Meehl's formulas against
clinical judgment, with a simulation of why (computed); and idioms of distress, stigma, and the diathesis-stress
frame. The practice chapter is diagnosis, screening and risk tools; the frontier is network, latent and common-cause
models, idiographic networks and what a biological classification would require.

## Where the numbers come from

| What | Source |
|---|---|
| A positive screen: 1% prevalence, 90% sensitivity, 91% specificity: of 10,000 people, 90 true and 891 false positives, so about 9% of positives have the condition | computed (`clinic.screen`), item `screen` |
| Two clinicians, 2,000 patients, 20% true cases, each seeing severity with noise: at noise 1 SD their kappa is 0.30 and each one's kappa with the truth 0.46 (20 samples per level) | Psyche (`clinic.two_clinicians`), item `kappa` |
| Five or more of nine symptoms, including one of two core symptoms: 227 combinations; two of them can share a single symptom | counted, item `combos` |
| Nine diagnoses from a general factor (loading 0.55) and three domains (0.45), each with 12% prevalence, in 20,000 people: all correlations positive, the first principal component 26% of the variance, and 55% of people with any diagnosis having two or more | Psyche (`clinic.comorbidity`), item `comorbid` |
| A nine-symptom network: with strong connections (c = 1) the way down stays up to 5.4 symptoms higher than the way up at the same stress; with weak ones (c = 0.2), 0.5 (30 runs) | Psyche (`clinic.sweep`), item `sweep` |
| The strong network under everyday stress with a stressful spell: 22 steps to recover after the stress ends, against 1 for the weak one (median of 21 runs by recovery time) | Psyche (`clinic.episode` rule in `compute.py`), item `episode` |
| A five-cue outcome, on new cases: true weights r = 0.71, fitted weights 0.71, equal weights 0.68, a clinician whose weights wander 0.60 (50 samples) | Psyche (`clinic.clinician_vs_formula`), item `meehl` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

Schematic panels (the profile-coverage curve, the taxon and dimension curves, the diathesis-stress line) are
labelled as schematic on screen and carry no data.

## Built in this part

* `explainer/psychology/psyche/clinic.py`: Cohen's kappa; two clinicians observing a latent severity with noise; a
  symptom network with Glauber dynamics, a stress sweep and an episode; diagnoses from a general factor and domains;
  natural frequencies for a screen; a formula against a clinician whose weights wander. Tested in
  `tests/psychology/test_clinic.py`.
* `care_card` in `explainer/psychology/viz.py`: the card that opens the parts about suffering (Parts 39 to 42, 57,
  59), with where help is found.
* The Ledger gains five rows.
* The course's interactive is a positive screen: six cases, each placed in a range for the chance that a positive
  means the condition, then counted out in natural frequencies.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Healthy people who faked one symptom were admitted to psychiatric hospitals and never detected | Rosenhan 1973 | contested |
| Combining information by a fixed formula predicts at least as well as an expert, often better | Meehl 1954 | replicated |
| Most mental disorders are continua with conventional cut-offs rather than categories | Haslam, Holland and Kuppens 2012 | replicated |
| A single general factor, p, accounts for much of the covariation among disorders, and means a shared liability | Caspi and colleagues 2014 | contested |
| A laboratory test can diagnose a mental disorder | Carroll and colleagues 1981 | failed |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Cahalan's investigation (in the
Rosenhan row); Wakefield; the APA's 1973 decision and 1974 vote; Regier and colleagues' field trials; Robins and
Guze; Fried and Nesse; Kessler and colleagues; Kohn and colleagues and Jorm and colleagues; Cramer and colleagues and
Borsboom; Nichter and Kaiser and colleagues; Kruis and Maris.

## Build it

```bash
python -m videos.psychology.psych39.compute            # every number (about a minute)
python tools/qa_scene.py psych39 Networks              # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych39 -q l   # the whole part, silent preview
python tools/build.py psych39                          # 1080p30 with narration
python tools/qa_scene.py psych39 Kappa --lang zh       # the Chinese edition of one chapter
python tools/make.py psych39                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 39                    # the lab: kappa, combinations, screens, networks, formulas
python tools/check_ledger.py psych39                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's clinic module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 1973: sane in insane places | The care card; Rosenhan's study; what the archive showed; the question; objectives |
| 1 | On you: a positive screen, and four numbers | A positive screen; natural frequencies; four predictions |
| 2 | A short history of madness | Two centuries in seven steps |
| 3 | What makes it a disorder? | Four candidate criteria; harmful dysfunction; a definition at work |
| 4 | Two clinicians, one patient | Agreement beyond chance; the DSM-5 field trials; unreliable cannot be valid |
| 5 | Reliable is not valid | Validators; two people, one diagnosis; 1,030 profiles |
| 6 | Categories or dimensions? | A kind or a degree; mostly degrees |
| 7 | Comorbidity is the rule | Every diagnosis goes with every other; a p factor |
| 8 | Symptoms that cause each other | No hidden cause; stress up, stress down; an episode |
| 9 | How common? | Nearly half, starting young; the treatment gap, and a paradox |
| 10 | Clinical against statistical prediction | A disturbing little book; half a century later; why formulas win |
| 11 | Culture, stigma and idioms of distress | Idioms of distress; diathesis and stress |
| 12 | The Ledger | Five rows and the tally |
| 13 | In practice: diagnosis, screening and risk tools | What a diagnosis is used for; a checklist score is not a diagnosis |
| 14 | Frontier: networks, persons and biology | Same data, three stories; open questions |
| | Recap, problems, and the road ahead | Your numbers; eleven lines; Kant's three objections; payoffs; problems; references; Part 40 |

## Sources

* D. L. Rosenhan, On being sane in insane places, *Science* 179 (1973) 250-258; S. Cahalan, *The Great Pretender*
  (2019).
* E. Shorter, *A History of Psychiatry* (1997); T. S. Szasz, *The Myth of Mental Illness* (1961); American
  Psychiatric Association, *DSM-III* (1980).
* J. C. Wakefield, The concept of mental disorder: on the boundary between biological facts and social values,
  *American Psychologist* 47 (1992) 373-388.
* J. Cohen, A coefficient of agreement for nominal scales, *Educational and Psychological Measurement* 20 (1960)
  37-46; D. A. Regier et al., DSM-5 field trials in the United States and Canada, Part II, *American Journal of
  Psychiatry* 170 (2013) 59-70.
* E. Robins and S. B. Guze, *American Journal of Psychiatry* 126 (1970) 983-987; E. I. Fried and R. M. Nesse,
  Depression is not a consistent syndrome, *Journal of Affective Disorders* 172 (2015) 96-102.
* N. Haslam, E. Holland and P. Kuppens, *Psychological Medicine* 42 (2012); N. Haslam, M. J. McGrath, W. Viechtbauer
  and P. Kuppens, *Psychological Medicine* 50 (2020).
* A. Caspi et al., The p factor, *Clinical Psychological Science* 2(2) (2014) 119-137; R. Kotov et al., The
  Hierarchical Taxonomy of Psychopathology, *Journal of Abnormal Psychology* 126 (2017).
* A. O. J. Cramer et al., Major depression as a complex dynamic system, *PLoS ONE* 11(12) (2016) e0167490;
  D. Borsboom, A network theory of mental disorders, *World Psychiatry* 16 (2017); J. Kruis and G. Maris, Three
  representations of the Ising model, *Scientific Reports* 6 (2016) 34175.
* R. C. Kessler et al., *Archives of General Psychiatry* 62(6) (2005) 593-602; R. Kohn et al., *Bulletin of the
  World Health Organization* 82 (2004) 858-866; A. F. Jorm, S. B. Patten, T. S. Brugha and R. Mojtabai, *World
  Psychiatry* 16(1) (2017) 90-99.
* P. E. Meehl, *Clinical versus Statistical Prediction* (1954); R. M. Dawes, The robust beauty of improper linear
  models, *American Psychologist* 34 (1979) 571-582; W. M. Grove et al., *Psychological Assessment* 12 (2000) 19-30.
* B. J. Carroll et al., *Archives of General Psychiatry* 38 (1981) 15-22; S. Kapur, A. G. Phillips and T. R. Insel,
  *Molecular Psychiatry* 17 (2012).
* M. Nichter, Idioms of distress, *Culture, Medicine and Psychiatry* 5 (1981) 379-408; B. N. Kaiser et al.,
  "Thinking too much", *Social Science and Medicine* 147 (2015) 170-183.

## Problems and solutions

1. **Kappa by hand.** n = 200; agreement p_o = (30 + 130)/200 = 0.80. A says yes (30 + 25)/200 = 0.275, B says yes
   (30 + 15)/200 = 0.225; p_e = 0.275 × 0.225 + 0.725 × 0.775 = 0.0619 + 0.5619 = 0.6238. κ = (0.80 − 0.6238) /
   (1 − 0.6238) ≈ 0.47.
2. **Kappa and independence.** If the ratings are independent, P(both yes) = a b and P(both no) = (1 − a)(1 − b), so
   p_o = p_e and κ = 0. With base rates 0.1 and 0.3, agreement is greatest when every yes of the first is also a
   yes of the second: p_o = 0.1 + 0.7 = 0.8, p_e = 0.03 + 0.63 = 0.66, so κ_max = 0.14/0.34 ≈ 0.41. Different base
   rates cap kappa.
3. **Combinations.** Subsets of nine with at least five members: 126 + 84 + 36 + 9 + 1 = 256. Those containing
   neither symptom 1 nor 2 are subsets of the other seven with at least five: 21 + 7 + 1 = 29. So 256 − 29 = 227.
4. **Screens at three prevalences.** PPV = π·0.9 / (π·0.9 + (1 − π)·0.09): at 1%, 0.009/0.0981 ≈ 9%; at 10%,
   0.09/0.171 ≈ 53%; at 30%, 0.27/0.333 ≈ 81%. Screening makes sense where the condition is common enough, or as a
   first stage before a confirmatory assessment.
5. **Reliability caps validity.** Write each measure as a true score plus independent error: X = T_X + E_X, Y = T_Y +
   E_Y. Then cov(X, Y) = cov(T_X, T_Y) ≤ sd(T_X) sd(T_Y) = √(r_xx) sd(X) · √(r_yy) sd(Y), so |r_xy| ≤ √(r_xx r_yy).
6. **Two stable states.** In a mean-field approximation each symptom is on with probability m = σ(b + s + c(n − 1)m).
   The right side is an S-shaped function of m; when c(n − 1) is large enough, the line m and the curve cross three
   times: the outer two crossings are stable (well and ill) and the middle one unstable. As s changes, one of the
   stable states disappears at a fold, which is where the network jumps; coming back, the jump happens at a
   different s: hysteresis.
7. **Network or common cause?** Intervene on one symptom (for example, treat insomnia alone) and measure the others
   over time: a network predicts the others improve through their connections; a common cause predicts they do not,
   unless the cause itself changes. Repeated measures within people (Part 47) add the time order that
   cross-sectional data lack.

## Open checks

Checked against the articles, their abstracts or official pages, or named secondary summaries of them
(2026-11-16): Rosenhan's eight pseudopatients, twelve hospitals and "in remission"; Cahalan's findings (via reviews of
the book); the APA's December 1973 decision and the 1974 vote (58%); the field trials' kappas (major depression and
generalized anxiety via a news report and secondary summaries, which give slightly different values; autism 0.69,
major neurocognitive disorder 0.78); Fried and Nesse's 3,703 patients, 1,030 profiles, 501 single and 84% shared by
five or fewer; Haslam et al.'s 177 articles, 311 findings, 38.9%, 16.2% and 14%; Caspi et al.'s design and
correlates; Cramer et al.'s model; Kessler et al.'s 46.4%, onset ages and halves; Kohn et al.'s 56.3% and 78.1%;
Jorm et al.'s four countries and conclusion; Grove et al.'s 33-47% and 6-16%; Kapur, Phillips and Insel's argument;
Kruis and Maris's equivalence; Nichter's and Kaiser et al.'s papers. Not re-checked here: the voice's words
("empty", "hollow", "thud"); the history chapter's dates and attributions (Pinel, Tuke, Kraepelin's 1899 division,
DSM-I in 1952, Szasz in 1961); Robins and Guze's five phases as listed; the claim that prospective studies find
higher lifetime prevalence (Moffitt et al., 2010); Carroll et al.'s 1981 paper and the fate of the dexamethasone
suppression test; the page ranges of Haslam et al., Kotov et al., Fried and Nesse, Wakefield and Cohen.
