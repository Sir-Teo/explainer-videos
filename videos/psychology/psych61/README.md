# Psychology, Built: Part 61, The Next Psychology

In 2020, 160 teams with thousands of variables on about four thousand families, free to use any method, tried to
predict six outcomes in the children's lives. The best models barely beat a regression on four variables. A field
that explains much and predicts little has to decide what it is for. This part gathers the proposals for a
psychology designed today: bigger teams, bigger and broader samples, experiments designed as spaces instead of
points, theories written as code, and a model of the research community itself, and ranks them by the evidence that
they work.

The viewer chooses one cell of a space of 1,024 experiments and sees the effect vary across the whole space, then
predicts four numbers. Then explanation against prediction; big team science and heterogeneity across forty labs;
experiments at the scale of millions and the bias that size does not remove; who is sampled, and English as the
default; integrative experiment design with a surrogate model; machine-assisted theory and adaptive design; theory
as code; Smaldino and McElreath's natural selection of bad science, rerun under two publication rules; digital
traces and the tweets-and-heart-disease result taken apart; automating research and what stays human; and the
reform proposals ranked by evidence.

## Where the numbers come from

| What | Source |
|---|---|
| A cohort of 4,000 with 400 variables (four with effects 0.25, 0.20, 0.15, 0.12 and the rest adding 0.06), true R-squared 0.20; 2,000 for training; 160 teams each choosing a variable subset (usually keeping the four obvious ones) and a ridge penalty: best held-out R-squared 0.13, median 0.07, four-variable least squares 0.13 | Psyche (`community.challenge`), item `challenge` |
| One effect (d = 0.3) in 40 labs of 100: no true variation gives estimates from -0.09 to 0.71 and I-squared 19% by chance; between-lab SD 0.2 gives I-squared 36% | Psyche (`community.many_labs`), item `labs` |
| A self-selected sample (log-odds of joining rise by 0.3 per SD of the score), true mean 0: at a million volunteers the estimate is 0.22 with an interval of plus or minus 0.002 | Psyche (`community.selected_sample`), item `selection` |
| A design space of ten binary choices (1,024 cells; main effects SD 0.1, pairwise interactions SD 0.05, base 0.3): true effects from -1.0 to 1.5, 28% negative; 120 cells run with SE 0.08; a ridge surrogate on 55 terms predicts the 904 others with correlation 0.99 | Psyche (`community.integrative`), item `space` |
| The natural selection of bad science: 100 labs, base rate 0.1, power 0.8, alpha = W/(1 + (1 - W)e), output 1 - 0.2 log10 e; 200 generations: effort falls from about 62 to 1, false share of published positives 88%; under registered reports (effort at least 50, every result published) effort stays near 65 and the false share is about 39% | Psyche (`community.bad_science`), item `science` |
| Adaptive design: recall tests at ten delays (1 to 60); power law 0.95(1 + t)^-0.45 against exponential 0.95e^(-0.08t), parameters fixed; 2,000 simulated people forget by the power law; to reach P(power law) of 0.95 the fixed design (shuffled cycles of the ten delays) needs a median of 25 tests and the adaptive design (most expected information before each test) 11, choosing the longest delay 97% of the time; after 80 tests 87% against over 99% of people are classified correctly | Psyche (`community.adaptive_design`), item `adaptive` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/community.py`: a simulated cohort and prediction challenge, many-labs heterogeneity,
  selected samples, a design space with a surrogate model, and Smaldino and McElreath's model. Tested in
  `tests/psychology/test_community.py`.
* The Ledger gains four rows.
* The course's interactive: choose a cell of the design space, then see the whole space; and run a research
  community under two publication rules.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Even with thousands of variables and any method, children's life outcomes are predicted little better than by a simple regression on a few variables. | Salganik and colleagues 2020 | not directly tested |
| When one protocol is run in many labs and countries, most effects vary little between samples beyond what sampling error produces. | Klein and colleagues (Many Labs 1) 2014 | replicated |
| Cognitive and perceptual experiments run online give results comparable to the same experiments run in the laboratory. | Germine and colleagues 2012 | replicated |
| The language of tweets from US counties predicts county deaths from heart disease better than demographic and health factors. | Eichstaedt and colleagues 2015 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Yarkoni and Westfall; Hofman and
colleagues; Moshontz and colleagues; Awad and colleagues; Thalmayer, Toscanelli and Arnett; Blasi and colleagues;
Almaatouq and colleagues; Peterson and colleagues; Borsboom and colleagues; Smaldino and McElreath.

## Build it

```bash
python -m videos.psychology.psych61.compute            # every number (seconds)
python tools/qa_scene.py psych61 Integrative           # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych61 -q l   # the whole part, silent preview
python tools/build.py psych61                          # 1080p30 with narration
python tools/qa_scene.py psych61 Selection --lang zh   # the Chinese edition of one chapter
python tools/make.py psych61                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 61                    # the lab: prediction ceilings, design spaces, incentives
python tools/check_ledger.py psych61                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's community module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A hundred and sixty teams | The Fragile Families Challenge, in Psyche; the question; objectives |
| 1 | On you: a space of experiments, and four numbers | Ten design choices; four predictions |
| 2 | Explanation and prediction | Two goals; having both |
| 3 | Big team science | Many labs, one protocol; forty labs, one effect |
| 4 | Millions of participants | Experiments at scale; noise shrinks, bias does not |
| 5 | Who is sampled | A decade after WEIRD; English as the default |
| 6 | Integrative experiment design | Beyond twenty questions; 120 cells run, 904 predicted |
| 7 | Machine-assisted theory | Ten thousand gambles; choosing the next experiment |
| 8 | Theory as code | Verbal theories and their problem; theory construction |
| 9 | The natural selection of bad science | Laboratories as organisms; two hundred generations, two rules |
| 10 | Digital traces | Tweets and the heart; what traces need |
| 11 | Automating research | Machines in research; what must stay human |
| 12 | Proposals, ranked by evidence | Seven reforms and their evidence |
| 13 | The Ledger | Four rows; what they have in common |
| 14 | In practice: commissioning research that holds up | Where this is a job; a checklist |
| 15 | Frontier: a science that studies itself | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 62 |

## Sources

* M. J. Salganik et al. (2020); M. J. Salganik, *Bit by Bit: Social Research in the Digital Age* (Princeton
  University Press, 2018).
* T. Yarkoni and J. Westfall, Choosing prediction over explanation in psychology: lessons from machine learning,
  *Perspectives on Psychological Science* 12 (2017) 1100-1122; J. M. Hofman et al., Integrating explanation and
  prediction in computational social science, *Nature* 595 (2021) 181-188.
* R. A. Klein et al. (2014, 2018); H. Moshontz et al., The Psychological Science Accelerator: advancing psychology
  through a distributed collaborative network, *Advances in Methods and Practices in Psychological Science* 1 (2018)
  501-515; M. C. Frank et al., A collaborative approach to infant research: promoting reproducibility, best
  practices, and theory-building, *Infancy* 22 (2017) 421-435; A. Olsson-Collentine et al. (2020).
* A. Coutrot et al., Global determinants of navigation ability, *Current Biology* 28 (2018) 2861-2866; E. Awad et
  al., The Moral Machine experiment, *Nature* 563 (2018) 59-64; J. K. Hartshorne, J. B. Tenenbaum and S. Pinker, A
  critical period for second language acquisition: evidence from 2/3 million English speakers, *Cognition* 177
  (2018) 263-277; L. Germine et al. (2012); M. J. C. Crump et al. (2013).
* J. Henrich, S. J. Heine and A. Norenzayan, The weirdest people in the world?, *Behavioral and Brain Sciences* 33
  (2010) 61-83; A. G. Thalmayer, C. Toscanelli and J. J. Arnett, The neglected 95% revisited: is American
  psychology becoming less American?, *American Psychologist* 76 (2021) 116-129; D. E. Blasi, J. Henrich, E.
  Adamou, D. Kemmerer and A. Majid, Over-reliance on English hinders cognitive science, *Trends in Cognitive
  Sciences* 26 (2022) 1153-1170.
* A. Almaatouq et al., Beyond playing 20 questions with nature: integrative experiment design in the social and
  behavioral sciences, *Behavioral and Brain Sciences* 47 (2024) e33; J. C. Peterson, D. D. Bourgin, M. Agrawal, D.
  Reichman and T. L. Griffiths, Using large-scale experiments and machine learning to discover theories of human
  decision-making, *Science* 372 (2021) 1209-1214; J. I. Myung and M. A. Pitt, Optimal experimental design for model
  discrimination, *Psychological Review* 116 (2009) 499-518.
* D. Borsboom, H. L. J. van der Maas, J. Dalege, R. A. Kievit and B. D. Haig, Theory construction methodology: a
  practical framework for building theories in psychology, *Perspectives on Psychological Science* 16 (2021)
  756-766; I. van Rooij and G. Baggio, Theory before the test: how to build high-verisimilitude explanatory
  theories in psychological science, *Perspectives on Psychological Science* 16 (2021) 682-697.
* P. E. Smaldino and R. McElreath, The natural selection of bad science, *Royal Society Open Science* 3 (2016)
  160384; A. M. Scheel, M. R. M. J. Schijen and D. Lakens, An excess of positive results: comparing the standard
  psychology literature with registered reports, *Advances in Methods and Practices in Psychological Science* 4
  (2021); C. K. Soderberg et al., Initial evidence of research quality of registered reports compared with the
  standard publishing model, *Nature Human Behaviour* 5 (2021) 990-997.
* J. C. Eichstaedt et al. (2015); N. J. L. Brown and J. C. Coyne (2018); M. B. Nuijten et al., The prevalence of
  statistical reporting errors in psychology (1985-2013), *Behavior Research Methods* 48 (2016) 1205-1226.

## Problems and solutions

1. **A ceiling.** With reliability 0.6, at most 60% of the outcome's variance is systematic, so no model can
   exceed R-squared 0.6, and a sum of many small causes, most unmeasured, puts the practical ceiling far lower.
2. **Many labs.** Each lab's SE is about sqrt(4/100 + 0.09/200) = 0.20, so with no true variation the estimates
   have SD about 0.20 and a 95% range of roughly 0.3 +/- 0.4.
3. **A biased million.** 0.22 +/- 1.96/sqrt(1,000,000) = 0.22 +/- 0.002. The interval says nothing about the
   bias; you need to know how people came to take part (and a benchmark from a probability sample) to correct it.
4. **A design space.** 2^10 = 1,024 cells; 1 + 10 + 45 = 56 parameters with an intercept, main effects and all
   pairwise interactions.
5. **Smaldino's arithmetic.** alpha = 0.8/(1 + 0.2 x 1) = 0.67 at effort 1, and 0.8/(1 + 0.2 x 75) = 0.05 at 75.
6. **False positives.** True positives 0.1 x 0.8 = 0.08; false 0.9 x 0.05 = 0.045; the false share 0.045/0.125 =
   0.36.
7. **A commissioning brief.** The decision and the smallest effect that would change it; a registered plan with
   power, primary outcome and analysis code; payment independent of the result; the sample described; data and
   code delivered; a replication if the stakes are high.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
the Fragile Families Challenge's 160 teams, about 4,000 families, six outcomes and the best R-squared values;
Yarkoni and Westfall (2017); Hofman et al. (2021); Many Labs 1's samples and Many Labs 2's 28 effects, about 125
samples and 36 countries; the Accelerator's founding; ManyBabies; Olsson-Collentine et al. (2020); Sea Hero Quest's
numbers; the Moral Machine's 40 million decisions and 233 countries and territories; Hartshorne et al.'s 670,000;
Germine et al. (2012); Crump et al. (2013); Thalmayer et al. (2021); Blasi et al. (2022); Almaatouq et al. (2024);
Peterson et al. (2021)'s nearly 10,000 problems; Myung and Pitt (2009); that Cavagnaro, Myung and Pitt's early demonstrations of adaptive design optimization used the power and exponential retention models (Cavagnaro et al., 2010); Borsboom et al. (2021); van Rooij and Baggio
(2021); Smaldino and McElreath (2016)'s model and power review; Scheel et al. (2021); Soderberg et al. (2021);
Eichstaedt et al. (2015)'s counties; Brown and Coyne (2018); Nuijten et al. (2016); Meng (2018)'s identity;
Simons, Shoda and Lindsay (2017) on constraints on generality; the audits of computational reproducibility in
journals with data policies; and every page range in Sources. The overfitting curve, the worked Meng example
(an illustrative correlation of 0.005) and the county simulation are Psyche's, with the truth known.
