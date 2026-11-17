# Psychology, Built: Part 31, The Lifespan

In 2000, with too few foster homes for the children in Bucharest's institutions, a lottery decided which of 136
children would be placed in foster families. It made one of the very few randomized experiments on early care, and
the children have been followed ever since. Most questions about development cannot be randomized, and this part is
about the designs that try to answer them anyway: three clocks that no data can separate, three designs that each
get ageing wrong in their own way, simulated where the truth is known, and the growth model that describes every
child at once.

The Bucharest Early Intervention Project and its result at eighteen; age, period and cohort, the Lexis diagram, and
the identity that leaves only two of three slopes identified; cross-sectional, longitudinal and cohort-sequential
designs on a simulated population with a true ageing curve and a cohort drift, and the Schaie–Salthouse debate; the
viewer sorts three graphs by clock; growth curves as a linear mixed model fitted by EM, with BLUPs shrunk toward the
fan; sensitive periods in vision, grammar and care; adolescence: peers and risk, the dual-systems curves and the late
chronotype; Baumrind's parenting styles on Maccoby and Martin's two axes, with Lamborn's survey and the
question of direction; parents, shared environment and adoptive siblings, the nurture assumption, and birth order; Bronfenbrenner's nested systems; Perry
Preschool, Abecedarian and the multiplicity of outcomes, and the word gap with its measurement problem; Kohlberg's
stages, Gilligan's critique and its record, and Erikson; fluid and crystallized abilities, processing speed and the
positivity effect; dementia, cognitive reserve, attributable fractions and the FINGER trial, and adult neurogenesis;
the Flynn effect, old norms and the reversal within families. The practice chapter is relative age and diagnosis,
adolescents in court, and screening, driving and work in later life; the frontier is large cohorts, causes from
cohort data, and ageing clocks.

## Where the numbers come from

| What | Source |
|---|---|
| The APC identity: three slope sets, (0, 0.01, 0), (0.01, 0, 0.01) and (−0.01, 0.02, −0.01), predicting the same scores for a person born in 1950 (largest difference 4e-15) | Psyche (`lifespan.apc_equivalent`), item `apc` |
| The three graphs: Lexis tables made by a pure age effect (decline after 50), period effect (a rise after 1985) or cohort effect (later birth, higher score) | Psyche (`lifespan.lexis`), item `apc` |
| The designs: 40,000 people born 1900–1990; true ageing flat to 55, then falling; cohort drift 0.02 SD per year of birth; no period effect. Cross-section in 1990: −0.54 SD by 50 where the truth is 0. One cohort (born ~1930) followed every 7 years from 1956: survivors +0.37 SD at 54, 1,500 people falling to 552. Cohort-sequential (7 cohorts, no period effect assumed): drift 0.019 recovered, curve within 0.1 SD of the truth | Psyche (`lifespan.ability_world`, `cross_sectional`, `longitudinal`, `cohort_sequential`), item `designs` |
| Growth: 120 simulated children, 5 visits, 542 scores; fitted (true) β₀ 99.5 (100), β₁ 6.45 (6), σ₀ 8.3 (8), σ₁ 2.12 (2), ρ 0.32 (0.3), σ 4.9 (5); spread of growth: own lines 2.72, truth 2.04, BLUPs 1.76 | Psyche (`lifespan.growth_data`, `fit_growth`), item `growth` |
| Siblings: ACE correlations with h² = 0.4, c² = 0.3 in childhood (0.70, 0.50, 0.30) and h² = 0.6, c² = 0 in adulthood (0.60, 0.30, 0.00), with 300 simulated pairs each | Psyche (`lifespan.sibling_correlations`), item `parents` |
| One hour a month against a whole day: correlation of a family's estimated talk with the truth 0.81 against 0.98 (42 simulated families, a year) | Psyche (`lifespan.hour_sampling`), item `wordgap` |
| Familywise error: 40% with 10 independent outcomes, 79% with 30 | Psyche (`lifespan.familywise`), item `programmes` |
| Reserve: onset at 64, 70 and 78 for reserves 0.5, 1 and 2, with the same end; PAF 0.21 for p = 0.3 and RR = 1.9; 7, 7, 5 and 5% combine to 22%, not 24% | Psyche (`lifespan.reserve`, `paf`, `combined_paf`), item `reserve` |
| Old norms: an average person scored on 15-year-old norms gets about 104.5 at 3 points a decade | Psyche (`lifespan.flynn_norms`), item `flynn` |
| Illustrative curves, drawn to published shapes: the visual window (peak in weeks 4–5, gone by 3–4 months), grammar, fade-out, the dual-systems curves (peaks at 19, plateau 23–26), fluid and crystallized abilities, the Flynn rise (2.8 points a decade) | `compute.py` items `windows`, `adolescence`, `programmes`, `ageing`; scene `Flynn` |
| BEIP: 136 children aged 6–31 months, randomized; at 18, 135 participants, foster care about 9 IQ points (0.6 SD) higher | Nelson et al. (2007); Humphreys et al. (2022) |
| ERA: under 6 months in an institution, problems as rare as in UK adoptees; over 6 months, persistent problems into ages 22–25, emotional problems 3–4 times as common; IQ recovered; a fifth problem-free | Sonuga-Barke et al. (2017) |
| Grammar: Johnson and Newport's 46 speakers; Hartshorne et al.'s 669,498 people and a peak to about 17.4 | Johnson and Newport (1989); Hartshorne et al. (2018) |
| Steinberg et al.: more than 5,000 people aged 10–30 in 11 countries; sensation seeking peaks at 19; self-regulation plateaus at 23–26 | Steinberg et al. (2018) |
| Chronotype: about 25,000 people; latest at 19.5 (women) and about 21 (men); ATUS 2003–2014, latest near 19 | Roenneberg et al. (2004); Fischer et al. (2017) |
| Adoptive siblings' IQ: about 0.3 in childhood studies, −0.03 in the first post-adolescent study | Plomin and Daniels (1987) |
| Birth order: nearly 400,000 Dutch men; 241,310 Norwegian conscripts; more than 20,000 adults in three panels, first-born brighter in 6 pairs of 10; 377,000 students, r = 0.02 (personality) and 0.04 (IQ) | Belmont and Marolla (1973); Kristensen and Bjerkedal (2007); Rohrer et al. (2015); Damian and Roberts (2015) |
| Perry at 40: 123 children (58, 65); employed 76% against 62%; median earnings $20,800 against $15,300; 97% interviewed; social rate of return 7–10% | Schweinhart et al. (2005); Heckman et al. (2010) |
| Abecedarian at mid-30s: treated men's systolic pressure 126 against 143; metabolic syndrome in 1 in 4 control men, none treated | Campbell et al. (2014) |
| Word gap: 42 families, 30 million by age four (projected); 42 children in five communities; 3,213 day-long recordings | Hart and Risley (1995); Sperry et al. (2019); Gilkerson et al. (2017) |
| Moral orientation: 108 studies; care d = 0.28 (women), justice d = 0.19 (men) | Walker (1984); Jaffee and Hyde (2000) |
| Salthouse: about 2,000 adults aged 18–60; reasoning declining from the late twenties, vocabulary rising to 60 | Salthouse (2009) |
| Positivity: 144 people aged 18–80; 100 studies, 7,129 people | Charles et al. (2003); Reed et al. (2014) |
| Dementia: 14 factors, about 45% potentially preventable, hearing loss and LDL about 7% each; FINGER 1,260 people aged 60–77, test change 0.20 against 0.16 | Livingston et al. (2024); Ngandu et al. (2015) |
| Flynn: 271 samples, about 4 million people, 31 countries, 1909–2013, 2.8 points a decade; 736,808 Norwegian conscripts | Pietschnig and Voracek (2015); Bratsberg and Rogeberg (2018) |
| ADHD and school entry: 407,000 children; 85.1 against 63.6 per 10,000 | Layton et al. (2018) |
| ABCD: 11,880 children aged 9–10 at 21 sites | Casey et al. (2018) |

## Built in this part

* `explainer/psychology/psyche/lifespan.py`: the APC identity and Lexis tables for a pure age, period or cohort
  effect; a simulated population with a true ageing curve and cohort drift, and cross-sectional, longitudinal (with
  practice and selective drop-out) and cohort-sequential designs on it; growth data and a linear mixed model with
  random intercepts and slopes fitted by EM, with BLUPs; a plasticity window; illustrative dual-systems and
  fluid/crystallized curves; ACE sibling correlations; a threshold model of cognitive reserve; Levin's attributable
  fraction and its combination; the sampling of talk by the hour or the day; fade-out; familywise error; old norms.
  Tested in `tests/psychology/test_lifespan.py`.
* The Ledger gains nine rows, and Part 10's deferred chronotype row is settled.
* The course's interactive is the three clocks: nine mystery worlds drawn as cross-sections in three years, each
  made by one clock, to be named by the reader; and a world whose age, period and cohort effects the reader sets,
  shown on a Lexis map with what a cross-section, one followed cohort and a same-age comparison would report.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Early institutional deprivation harms development, and early placement in a family helps | Nelson, Zeanah, Fox and colleagues 2007 | replicated |
| A preschool programme for poor three- and four-year-olds improved their lives as adults | Schweinhart and colleagues 2005 | replicated, smaller |
| By age four, children in poor families have heard about 30 million fewer words | Hart and Risley 1995 | contested |
| The adult human hippocampus keeps making new neurons into old age | Eriksson, Gage and colleagues 1998 | contested |
| Birth order shapes personality | Sulloway 1996 | failed |
| Firstborns score slightly higher on intelligence tests | Belmont and Marolla 1973 | replicated |
| Chronotype is latest at about age twenty | Roenneberg and colleagues 2004 | replicated |
| Kohlberg's stages score women's moral reasoning lower than men's | Gilligan 1982 | failed |
| Older adults favour positive over negative material | Charles, Mather and Carstensen 2003 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Hubel and Wiesel's sensitive
period, the Schaie–Salthouse debate, Gardner and Steinberg's peer study (its row waits for a registered
replication), the eleven-country survey, Harris's book, Colby et al.'s longitudinal study, Salthouse's speed theory,
the Lancet Commission's fractions, the FINGER trial, the ABCD design, relative age and ADHD (due a row with
development in Part 41), and the Flynn effect and its reversal (due with intelligence in Part 32).

## Build it

```bash
python -m videos.psychology.psych31.compute            # every number (under a minute)
python tools/qa_scene.py psych31 Designs               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych31 -q l   # the whole part, silent preview
python tools/build.py psych31                          # 1080p30 with narration
python tools/qa_scene.py psych31 Growth --lang zh      # the Chinese edition of one chapter
python tools/make.py psych31                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 31                    # the lab: APC, three designs, growth curves, reserve
python tools/check_ledger.py psych31                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's lifespan module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The lottery in Bucharest | The trial; what it showed; the questions; objectives |
| 1 | Three clocks | Age, period and cohort; the Lexis diagram; the identity; the assumption every answer needs |
| 2 | Three designs, three answers | A known world; cross-sectional; longitudinal with practice and drop-out; cohort-sequential; the Schaie–Salthouse debate |
| 3 | On you: age, period or cohort? | Three graphs, three clocks, and the trap |
| 4 | Growth curves | Every child a line; the mixed model fitted by EM; shrinkage |
| 5 | Windows | Kittens and the visual window; grammar; care; what closes a window |
| 6 | Adolescence | Chicken with friends; two systems; the late clock; what "the teenage brain" explains |
| 7 | Parents | Two routes; siblings as children and adults; the nurture assumption; birth order |
| 8 | Early intervention | Fade-out; Perry at forty; many outcomes; Abecedarian; the word gap; one hour a month |
| 9 | Moral development and identity | Heinz; Kohlberg's stages; a different voice; Erikson |
| 10 | Adulthood and ageing | Fluid and crystallized; speed; socioemotional selectivity |
| 11 | Dementia and reserve | Normal ageing and dementia; reserve; attributable fractions; FINGER; adult neurogenesis |
| 12 | Cohorts change | The Flynn effect; old norms; the reversal within families |
| 13 | The Ledger | Nine rows: deprivation, Perry, the word gap, birth order twice, chronotype, moral stages, positivity, neurogenesis |
| 14 | In practice: ages and rules | Relative age and ADHD; adolescents in court; screening, driving and work |
| 15 | Frontier: cohorts, causes and ageing | ABCD; causes from cohorts; ageing clocks and prevention trials; open problems |
| | Recap, problems, and the road ahead | Your graphs; ten lines; Kant's three objections; payoffs; problems; references; Part 32 |

## Sources

* C. A. Nelson, C. H. Zeanah, N. A. Fox, P. J. Marshall, A. T. Smyke and D. Guthrie, Cognitive recovery in socially
  deprived young children: the Bucharest Early Intervention Project, *Science* 318 (2007) 1937–1940.
* K. L. Humphreys et al., Foster care leads to sustained cognitive gains following severe early deprivation, *PNAS*
  119 (2022).
* C. A. Nelson, N. A. Fox and C. H. Zeanah, *Romania's Abandoned Children* (Harvard University Press, 2014).
* E. J. S. Sonuga-Barke et al., Child-to-adult neurodevelopmental and mental health trajectories after early life
  deprivation, *Lancet* 389 (2017) 1539–1548.
* N. B. Ryder, The cohort as a concept in the study of social change, *American Sociological Review* 30 (1965).
* K. W. Schaie, *Developmental Influences on Adult Intelligence: The Seattle Longitudinal Study* (Oxford, 2005).
* T. A. Salthouse, When does age-related cognitive decline begin? *Neurobiology of Aging* 30 (2009); The
  processing-speed theory of adult age differences in cognition, *Psychological Review* 103 (1996).
* N. M. Laird and J. H. Ware, Random-effects models for longitudinal data, *Biometrics* 38 (1982).
* T. N. Wiesel and D. H. Hubel, Single-cell responses in striate cortex of kittens deprived of vision in one eye,
  *Journal of Neurophysiology* 26 (1963); D. H. Hubel and T. N. Wiesel, The period of susceptibility to the
  physiological effects of unilateral eye closure in kittens, *Journal of Physiology* 206 (1970).
* J. S. Johnson and E. L. Newport (1989); K. Hakuta, E. Bialystok and E. Wiley (2003); J. K. Hartshorne, J. B.
  Tenenbaum and S. Pinker, *Cognition* 177 (2018) 263–277.
* M. Gardner and L. Steinberg, Peer influence on risk taking, risk preference, and risky decision making in
  adolescence and adulthood, *Developmental Psychology* 41 (2005).
* L. Steinberg et al., Around the world, adolescence is a time of heightened sensation seeking and immature
  self-regulation, *Developmental Science* 21 (2018) e12532.
* T. Roenneberg et al., A marker for the end of adolescence, *Current Biology* 14 (2004) R1038–R1039; D. Fischer,
  D. A. Lombardi, H. Marucci-Wellman and T. Roenneberg, Chronotypes in the US, *PLoS ONE* 12 (2017) e0178782.
* American Academy of Pediatrics, School start times for adolescents, *Pediatrics* (2014).
* R. Plomin and D. Daniels, Why are children in the same family so different from one another? *Behavioral and
  Brain Sciences* 10 (1987); J. R. Harris, *The Nurture Assumption* (Free Press, 1998).
* L. Belmont and F. A. Marolla, *Science* 182 (1973) 1096–1101; P. Kristensen and T. Bjerkedal, *Science* 316
  (2007) 1717; J. M. Rohrer, B. Egloff and S. C. Schmukle, *PNAS* 112 (2015) 14224–14229; R. I. Damian and B. W.
  Roberts, *Journal of Research in Personality* 58 (2015); F. J. Sulloway, *Born to Rebel* (1996).
* L. J. Schweinhart et al., *Lifetime Effects: The High/Scope Perry Preschool Study Through Age 40* (2005); J. J.
  Heckman et al., *Journal of Public Economics* 94 (2010) 114–128; M. L. Anderson, *JASA* 103 (2008) 1481–1495;
  F. Campbell et al., *Science* 343 (2014).
* B. Hart and T. R. Risley, *Meaningful Differences* (1995); D. E. Sperry, L. L. Sperry and P. J. Miller, *Child
  Development* 90 (2019); J. Gilkerson et al., *American Journal of Speech-Language Pathology* 26 (2017).
* L. Kohlberg (1958 dissertation); A. Colby, L. Kohlberg, J. Gibbs and M. Lieberman, A longitudinal study of moral
  judgment, *Monographs of the SRCD* 48 (1983); C. Gilligan, *In a Different Voice* (1982); L. J. Walker, *Child
  Development* 55 (1984); S. Jaffee and J. S. Hyde, *Psychological Bulletin* 126 (2000); E. H. Erikson,
  *Childhood and Society* (1950).
* S. T. Charles, M. Mather and L. L. Carstensen, *Journal of Experimental Psychology: General* 132 (2003); A. E.
  Reed, L. Chan and J. A. Mikels, *Psychology and Aging* 29 (2014) 1–15.
* Y. Stern, Cognitive reserve in ageing and Alzheimer's disease, *Lancet Neurology* 11 (2012); G. Livingston et
  al., Dementia prevention, intervention, and care: 2024 report of the Lancet standing Commission, *Lancet* (2024);
  T. Ngandu et al., *Lancet* 385 (2015) 2255–2263.
* P. S. Eriksson et al., *Nature Medicine* 4 (1998) 1313–1317; S. F. Sorrells et al., *Nature* 555 (2018); M.
  Boldrini et al., *Cell Stem Cell* 22 (2018); E. P. Moreno-Jiménez et al., *Nature Medicine* 25 (2019).
* J. R. Flynn, Massive IQ gains in 14 nations, *Psychological Bulletin* 101 (1987); J. Pietschnig and M. Voracek,
  *Perspectives on Psychological Science* 10 (2015); B. Bratsberg and O. Rogeberg, *PNAS* 115 (2018).
* T. J. Layton, M. L. Barnett, T. R. Hicks and A. B. Jena, Attention deficit–hyperactivity disorder and month of
  school enrollment, *New England Journal of Medicine* 379 (2018).
* B. J. Casey et al., The Adolescent Brain Cognitive Development (ABCD) study, *Developmental Cognitive
  Neuroscience* 32 (2018) 43–54.
* P. B. Baltes, Theoretical propositions of life-span developmental psychology, *Developmental Psychology* 23
  (1987).

## Problems and solutions

1. **The identity.** With cohort c = period − age, a·Age + p·Period + c·Cohort = (a − c)·Age + (p + c)·Period.
   Adding k to a and c and subtracting k from p leaves a − c and p + c unchanged, so every prediction is the same.
   Only the two combinations are identified; a third constraint must come from outside the data.
2. **A cross-section invents ageing.** In year t, a person of age A was born in t − A, so a cohort gain g per year of
   birth gives a score g(t − A − t₀): an apparent ageing slope of −g per year of age, with no ageing at all. A
   longitudinal study of one cohort, in a world with no period effect, shows a flat line. Chapter two's cross-section
   (g = 0.02) shows −0.54 SD by 50 where the truth is flat: about −0.02 × 30 = −0.6, up to noise.
3. **Shrinkage.** With the intercept known, a child's least-squares slope b̂ᵢ has sampling variance σ²/Sₓₓ, where
   Sₓₓ = Σ(tⱼ − t̄)² over the child's visits. With bᵢ ~ N(β₁, σ₁²), the posterior mean is
   β₁ + λ(b̂ᵢ − β₁) with λ = σ₁² / (σ₁² + σ²/Sₓₓ). More noise (σ²) lowers λ, more shrinkage; more or more widely spread
   visits (Sₓₓ) raise it. A child who missed visits is shrunk more.
4. **ACE.** r_MZ = h² + c² and r_DZ = h²/2 + c², so r_MZ − r_DZ = h²/2, giving h² = 2(r_MZ − r_DZ), and
   c² = r_MZ − h² = 2r_DZ − r_MZ. Adoptive siblings share no genes by descent, so if placement is not selective their
   correlation is c² directly; that is why adoptive siblings' near-zero IQ correlation after adolescence is such
   direct evidence that the shared environment fades.
5. **Attributable fractions.** With exposure prevalence p and relative risk RR, P(D) = P(D | Ē)[(1 − p) + p·RR] =
   P(D | Ē)(1 + p(RR − 1)). The fraction removable by eliminating exposure is (P(D) − P(D | Ē))/P(D) =
   p(RR − 1)/(1 + p(RR − 1)). For independent factors acting multiplicatively, P(D)/P(D | none) = ∏(1 + pᵢ(RRᵢ − 1)) =
   ∏ 1/(1 − PAFᵢ), so the combined fraction is 1 − ∏(1 − PAFᵢ), less than the sum. Every step assumes the factor
   causes the disease and that removing it returns the risk to the unexposed level.
6. **Old norms.** Eighteen years at 2.8 points a decade is 5.04 points: the average person now scores about 105.0.
   Below 70 then requires z < (70 − 105.04)/15 = −2.34, about 1.0% of people, against 2.3% (z < −2) at norming. A
   cutoff of 70 on an old test identifies fewer than half as many people as it did when the test was new.
7. ★ **Retirement and decline.** A cohort-sequential panel gives age and cohort under no period effect, but people
   who retire early differ from those who do not (health, work, wealth), and declining people may retire because they
   decline. A design: use rules that move retirement for reasons unrelated to the person, such as pension
   eligibility ages that differ between countries or change between birth cohorts, as an instrument for retirement,
   in a panel with repeated cognitive tests. The cohort clock is used to define who faced which rule; the
   assumption is that the rule affects cognition only through retirement (no other change in the same cohorts) and
   that retest effects are equal across groups, which should be checked with refreshment samples.

## Open checks

Checked against the articles, their abstracts or official pages (2026-11-15): the BEIP design (136 children, 6 to 31
months) and the 2007 report's direction (gains largest for the youngest placed), and Humphreys et al.'s 135
participants and 9 points (0.6 SD) at 18; the ERA's six-month boundary, persistence to 22–25, threefold to fourfold
emotional problems, IQ recovery and the problem-free fifth; Hartshorne et al.'s 669,498 people and 17.4; Steinberg
et al.'s more than 5,000 people in 11 countries, 19 and 23–26; Roenneberg's 25,000 people; Fischer et al.'s ATUS
2003–2014 and a peak near 19; the AAP's 8:30 recommendation; Plomin and Daniels's 0.32 and −0.03; Belmont and
Marolla's nearly 400,000 Dutch men; Kristensen and Bjerkedal's 241,310 conscripts and the second sons raised as
eldest (102.9 against 103.2 for firstborns and 101.2 for other second-borns); Rohrer et al.'s three panels and the
60/40 split; Damian and Roberts's 377,000, 0.02 and 0.04; Perry's 123 (58, 65), 76% against 62%, $20,800 against
$15,300 and 97%; Heckman et al.'s 7–10%; Anderson's girls and boys; Campbell et al.'s 126 against 143 and the
metabolic syndrome; Hart and Risley's 42 families and 30 million by age four; Gilkerson et al.'s 3,213 recordings;
Colby et al.'s 58 boys aged 10, 13 and 16; Jaffee and Hyde's 0.28 and 0.19; Salthouse's 2,000 adults, the late
twenties and vocabulary to 60; Charles et al.'s 144 people; Reed et al.'s 100 studies and 7,129 people; the Lancet
Commission's 14 factors, 45%, and 7% for hearing loss and LDL; FINGER's 1,260 people aged 60–77 and 0.20 against
0.16; Eriksson et al.'s five patients; Sorrells, Boldrini and Moreno-Jiménez's findings; Pietschnig and Voracek's
271 samples, about four million people, 31 countries and 2.8 points; Bratsberg and Rogeberg's 736,808 conscripts;
Layton et al.'s 407,000 children and 85.1 against 63.6; ABCD's 11,880 children at 21 sites.

Still to recheck against the full texts before the final cut:

* Gardner and Steinberg (2005): the Chicken task's yellow light and wall, and the three age groups' means (shown as
  a schematic, not as values).
* Sperry, Sperry and Miller (2019): that counting overheard speech removed the gap by income in their five
  communities (from summaries).
* Walker (1984): the count of 108 studies (from a secondary summary).
* Kohlberg's stage 6 dropped from later scoring, and "most adults at stages 3 and 4" (standard textbook accounts).
* Pietschnig and Voracek (2015): larger gains for fluid than crystallized abilities (standard summary).
* The Lexis diagram's date and Wilhelm Lexis's priority (named without a date on screen).
