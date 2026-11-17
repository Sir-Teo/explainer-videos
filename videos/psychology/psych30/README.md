# Psychology, Built: Part 30, The Infant Mind

A ten-month-old finds a toy under cup A, again and again; then she watches it hidden under cup B, and reaches for A.
This part asks what a baby knows and how anyone can find out, when the baby cannot answer. It builds the
instrument that replaced asking, looking time, then tests it at scale by recomputing ManyBabies 1 from its open
table, and ends by rebuilding Piaget's error as a dynamic neural field.

The A-not-B error and Piaget's theory: schemes, assimilation and accommodation, four stages, conservation; Fantz's
looking chamber; habituation with the laboratory criterion, simulated; violation of expectation and what a long
look can mean; the Goldilocks effect with an ideal learner's surprisal; ManyBabies 1, 108 lab-by-age estimates
from 65 laboratories, pooled and meta-regressed on age, method and language; the viewer predicts six infant
results; the drawbridge and its lean reading, and Spelke's core knowledge; Wynn's one plus one and its record,
number by ratio with Weber fractions by age, and number sense and mathematics; Xu and Garcia's box of balls and
three views of development; the A-not-B error as a dynamic field, with error against delay and number of A
trials; false belief at four and at fifteen months, and newborn imitation; Harlow, the Strange Situation and what
attachment predicts; temperament, Vygotsky, natural pedagogy and overimitation. The practice chapter is
developmental screening, early childhood programmes and media for babies; the frontier is infancy research at
scale, head cameras, and infants as a benchmark for machines.

## Where the numbers come from

| What | Source |
|---|---|
| Habituation: looks fall from about 12 s (mean of the first three) to the criterion (three looks under half that) at trial 7; a familiar test display 4.3 s, a new one 12.1 s | Psyche (`develop.habituation`, seed 3), item `habituation` |
| Goldilocks: look-away lowest near 1.1 bits of surprisal (by construction, after Kidd et al.); events watched before looking away: predictable 6.4, intermediate 6.8, random 5.5 | Psyche (`develop.goldilocks`, `surprisal_trace`), item `goldilocks` |
| ManyBabies 1: 108 estimates, 65 laboratories, 2,179 infants in the shared table; random-effects d = 0.35 [0.29, 0.42], I² = 12%; central fixation 0.29 (33), eye tracking 0.24 (41), head-turn preference 0.51 (34); by age group 0.17, 0.21, 0.42, 0.55; meta-regression age slope 0.047 per month (SE 0.010), head-turn preference +0.18 (SE 0.08); North American English stimuli 0.43 against 0.28 | ManyBabies Consortium (2020) (`opendata.manybabies_2020`, psymetadata 1.0.1), item `manybabies` |
| Number: Weber fractions 0.66 (6 months), 0.41 (9 months), 0.29 (3 years), 0.15 (adults), illustrative, chosen so that 2:1 and 3:2 are told apart three times in four at six and nine months; thresholds 1.99, 1.50, 1.32, 1.15 | Psyche (`develop.ans_correct`, `ratio_threshold`), item `number` |
| The box of balls: with 90% white (illustrative), four red and one white has probability 0.00045 (11.1 bits), four white and one red 0.33 (1.6 bits): 729 times less likely | Psyche (`develop.sample_surprise`), item `statistics` |
| The dynamic field: 300 simulated infants per point; younger field (h = −6) errs 0%, 9%, 96%, 87%, 67% at 0 to 4 s and returns to about 50% by 6 s; the older field (h = −3) never errs; at 3 s, error 52% after one A trial and 90% after six | Psyche (`develop.a_not_b`, `field_snapshot`), item `anotb` |
| Wynn's meta-analysis: 12 studies, 26 samples, 550 infants, d = 0.34 | Christodoulou, Lac and Moore (2017) |
| Wellman, Cross and Watson: 178 studies | Wellman, Cross and Watson (2001) |
| Oostenbroek et al.: 106 infants at 1, 3, 6 and 9 weeks, 11 models | Oostenbroek et al. (2016) |
| van IJzendoorn and Kroonenberg: 32 samples, 8 countries, 1,990 infants; Fearon et al.: 69 samples, nearly 6,000 children, d = 0.31 | van IJzendoorn and Kroonenberg (1988); Fearon et al. (2010) |
| Thomas and Chess: 40% easy, 10% difficult, 15% slow to warm up | Thomas and Chess (1977) |
| Vong et al.: 61 hours of one child's head-camera video, 6 to 25 months; Piloto et al.: as little as 28 hours of video, five concepts | Vong et al. (2024); Piloto et al. (2022) |

## Built in this part

* `explainer/psychology/psyche/develop.py`: habituation with the laboratory criterion; a Dirichlet-multinomial
  ideal learner's surprisal and an observer with a U-shaped look-away rule; the approximate number system's
  accuracy and ratio thresholds, with illustrative Weber fractions by age; the box-of-balls probabilities; a
  one-dimensional dynamic neural field with a memory trace, run for many simulated infants at once, that makes and
  outgrows the A-not-B error; random-effects meta-regression. Tested in `tests/psychology/test_develop.py`.
* `explainer/psychology/opendata.py` reads ManyBabies 1's lab-level table from psymetadata 1.0.1, checked by
  SHA-256 (`manybabies_2020`); the Archive registers it (`MANYBABIES_2020`).
* The Ledger gains eight rows, and four earlier declarations that pointed here are settled.
* The course's interactive is the prediction game on you: six published infant results, where did infants look
  longer, and what happened to each when it was checked.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Infants of about eight to twelve months search at A after seeing a toy hidden at B | Piaget 1937 | replicated |
| Infants of three to five months know that a hidden object still exists | Baillargeon, Spelke and Wasserman 1985 | contested |
| Five-month-olds expect one plus one to make two | Wynn 1992 | contested |
| The acuity of the approximate number system predicts mathematics | Halberda, Mazzocco and Feigenson 2008 | replicated, smaller |
| Children begin to pass explicit false-belief tasks at about four | Wimmer and Perner 1983 | replicated |
| Infants of about fifteen months expect people to act on false beliefs | Onishi and Baillargeon 2005 | contested |
| Newborns imitate facial gestures | Meltzoff and Moore 1977 | contested |
| Infants prefer infant-directed speech | Fernald 1985 | replicated |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Piaget's theory and the
conservation task, Fantz's method, core knowledge and the three theoretical positions, Xu and Garcia's study,
the dynamic field model, Harlow's experiments, the Strange Situation and its cross-cultural pooling, the
attachment meta-analysis quoted for its size, temperament, Vygotsky and natural pedagogy, overimitation (due a
row with culture in Part 38), the programme evaluations (due with education in Part 54), the baby-media trial,
and the frontier's models (machines are Part 60's).

## Build it

```bash
python -m videos.psychology.psych30.compute            # every number (a few minutes: the field runs 7,000 infants)
python tools/qa_scene.py psych30 Field                 # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych30 -q l   # the whole part, silent preview
python tools/build.py psych30                          # 1080p30 with narration
python tools/qa_scene.py psych30 ManyBabies --lang zh  # the Chinese edition of one chapter
python tools/make.py psych30                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 30                    # the lab: surprisal, ManyBabies, number, the field
python tools/check_ledger.py psych30                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's develop module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | The toy under the cloth | The A-not-B error; the problem of a subject who cannot answer; the questions; objectives |
| 1 | Piaget's infant | Schemes, assimilation and accommodation; four stages; conservation |
| 2 | Looking as an instrument | Fantz's chamber; habituation simulated; violation of expectation; the Goldilocks effect |
| 3 | One effect, sixty-five laboratories | Why infant studies are fragile; ManyBabies 1 recomputed; age, method and language |
| 4 | On you: predict the infant | Six experiments, six guesses, and what was reported |
| 5 | Objects | The drawbridge; the lean reading; core knowledge |
| 6 | Number | One plus one; its record; number by ratio; number sense and mathematics |
| 7 | Born knowing, or built? | The box of balls; three views of development |
| 8 | A-not-B as dynamics | What the error depends on; the field derived; one infant's field; error against delay and A trials |
| 9 | Other minds | False belief at four; at fifteen months; newborn imitation |
| 10 | Attachment | Cloth and wire; the Strange Situation; what attachment predicts |
| 11 | Temperament and learning from others | Temperament; the zone of proximal development and natural pedagogy; overimitation |
| 12 | The Ledger | Eight rows: A-not-B, object permanence, arithmetic, number sense, false belief twice, imitation, infant-directed speech |
| 13 | In practice: screening, programmes and media | Developmental screening; early childhood programmes; media for babies |
| 14 | Frontier: many babies, head cameras and machines | Infancy research at scale; one child's view; infants as a benchmark for machines; open problems |
| | Recap, problems, and the road ahead | Your guesses; ten lines; Kant's three objections; payoffs; problems; references; Part 31 |

## Sources

Piaget and looking: J. Piaget, *La naissance de l'intelligence chez l'enfant* (1936) and *La construction du réel
chez l'enfant* (1937; *The Construction of Reality in the Child*, 1954); J. Piaget and A. Szeminska, *La genèse du
nombre chez l'enfant* (1941); R. L. Fantz, The origin of form perception, Scientific American 204 (May 1961) 66-72;
C. Kidd, S. T. Piantadosi and R. N. Aslin, The Goldilocks effect: human infants allocate attention to visual
sequences that are neither too simple nor too complex, PLoS ONE 7 (2012) e36399; the infant-directed speech row's
references in the Ledger.

Objects, number and statistics: the object-permanence, arithmetic and number-sense rows' references in the Ledger;
F. Xu and E. S. Spelke, Large number discrimination in 6-month-old infants, Cognition 74 (2000) B1-B11; J. S.
Lipton and E. S. Spelke, Origins of number sense: large-number discrimination in human infants, Psychological
Science 14 (2003) 396-401; F. Xu and V. Garcia, Intuitive statistics by 8-month-old infants, Proceedings of the
National Academy of Sciences 105 (2008) 5012-5015; E. S. Spelke and K. D. Kinzler, Core knowledge, Developmental
Science 10 (2007) 89-96; F. Xu and T. Kushnir, eds., *Rational Constructivism in Cognitive Development* (2012).

The field: E. Thelen, G. Schöner, C. Scheier and L. B. Smith, The dynamics of embodiment: a field theory of infant
perseverative reaching, Behavioral and Brain Sciences 24 (2001) 1-86; the A-not-B row's references in the Ledger.

Minds, attachment and others: the false-belief and imitation rows' references in the Ledger; H. F. Harlow, The
nature of love, American Psychologist 13 (1958) 673-685; J. Bowlby, *Attachment* (1969); M. D. S. Ainsworth,
M. C. Blehar, E. Waters and S. Wall, *Patterns of Attachment* (1978); M. H. van IJzendoorn and P. M. Kroonenberg,
Cross-cultural patterns of attachment: a meta-analysis of the Strange Situation, Child Development 59 (1988)
147-156; R. M. P. Fearon et al., The significance of insecure attachment and disorganization in the development of
children's externalizing behavior, Child Development 81 (2010) 435-456; A. Thomas and S. Chess, *Temperament and
Development* (1977); L. S. Vygotsky, *Thinking and Speech* (1934); G. Csibra and G. Gergely, Natural pedagogy,
Trends in Cognitive Sciences 13 (2009) 148-153; V. Horner and A. Whiten, Causal knowledge and imitation/emulation
switching in chimpanzees and children, Animal Cognition 8 (2005) 164-181; D. E. Lyons, A. G. Young and F. C. Keil,
The hidden structure of overimitation, Proceedings of the National Academy of Sciences 104 (2007) 19751-19756.

Practice and frontier: American Academy of Pediatrics guidance on developmental surveillance and screening;
L. J. Schweinhart et al., *Lifetime Effects: The High/Scope Perry Preschool Study Through Age 40* (2005);
M. Puma et al., *Third Grade Follow-up to the Head Start Impact Study* (2012); K. Durkin, M. W. Lipsey,
D. C. Farran and S. E. Wiesen, Effects of a statewide pre-kindergarten program on children's achievement and
behavior through sixth grade, Developmental Psychology 58 (2022) 470-484; J. S. DeLoache et al., Do babies learn
from baby media?, Psychological Science 21 (2010) 1570-1574; W. K. Vong, W. Wang, A. E. Orhan and B. M. Lake,
Grounded language acquisition through the eyes and ears of a single child, Science 383 (2024) 504-511; L. S.
Piloto, A. Weinstein, P. Battaglia and M. Botvinick, Intuitive physics learning in a deep-learning model inspired
by developmental psychology, Nature Human Behaviour 6 (2022) 1257-1267.

Data: ManyBabies 1's lab-level table, github.com/manybabies/mb1-analysis-public, as manybabies2020 in psymetadata
1.0.1 (GPL >= 2), fetched from CRAN and never redistributed.

## Problems and solutions

1. **The ideal learner.** For a Dirichlet$(\alpha)$-multinomial learner with $k$ outcomes, show that the predictive probability of an outcome seen $c$ times in $n$ events is $(c + \alpha)/(n + k\alpha)$, and give its surprisal in bits.

   *Solution.* With a Dirichlet(α) prior over k outcomes and counts c₁…c_k after n events, the
   posterior is Dirichlet(α + c), whose mean for outcome j is (c_j + α)/(n + kα): the predictive probability of the
   next event. Its surprisal is −log₂((c_j + α)/(n + kα)) bits. With α = 1 and k = 3 the first event always
   carries log₂ 3 = 1.58 bits.
2. **Number by ratio.** If a number $n$ is represented as a normal with mean $n$ and standard deviation $w n$, show that $P(\text{correct}) = \Phi\big(|n_1 - n_2| / (w\sqrt{n_1^2 + n_2^2})\big)$, and that it depends only on the ratio.

   *Solution.* The difference of the two representations is normal with mean n₁ − n₂ and variance
   w²(n₁² + n₂²). The judgment is right when the difference has the sign of n₁ − n₂, with probability
   Φ(|n₁ − n₂| / (w√(n₁² + n₂²))). Replacing (n₁, n₂) by (λn₁, λn₂) cancels λ, so with r = n₁/n₂ it is
   Φ(|r − 1| / (w√(r² + 1))): a function of the ratio only.
3. **The box of balls.** From a box with a share $p$ of white balls, show that four red and one white is $\big(p/(1 - p)\big)^3$ times less probable than four white and one red.

   *Solution.* P(4 red, 1 white) = 5(1 − p)⁴p and P(1 red, 4 white) = 5(1 − p)p⁴; their ratio is
   (p/(1 − p))³, which is 729 for p = 0.9.
4. **ManyBabies with age alone.** With the ManyBabies table (`opendata.manybabies\_2020`), refit the meta-regression with age alone. How much does the age slope change, and why?

   *Solution.* The age slope is 0.050 per month (SE 0.010), against 0.047 with method held
   fixed, because age and method are nearly uncorrelated across laboratories (r = 0.10). Age alone also takes τ²
   from 0.014 to zero: the little heterogeneity there was is mostly age.
5. **When memory wins.** In a field with no interactions, a cue of strength $A$ at B decays as $A e^{-t/\tau}$ while a memory trace $c\,m$ sits at A. Show that the reach goes to A after $t^* = \tau \ln(A / c\,m)$.

   *Solution.* Without interactions the field at B after the cue is h + s + A e^(−t/τ) and at A is
   h + s + c m. The reach goes to A once A e^(−t/τ) < c m, that is t > τ ln(A/(c m)). Stronger memories (more A
   trials) and faster decay (smaller τ, a less cooperative field) make the error come sooner.
6. **Familiarity.** Infants who have seen too little of a display prefer the familiar one. Show how a familiarity preference could produce longer looks at the 180-degree drawbridge without any knowledge of the box.

   *Solution.* Infants who have had little exposure to a display prefer it; with more, they prefer novelty.
   After a short habituation to a 180-degree rotation, the impossible event, which repeats that rotation, can win a
   familiarity preference with no knowledge of the box. The test: vary familiarization and see whether the
   preference flips, as Bogartz, Shinskey and Schilling did.
7. ★ **Core knowledge against rational constructivism.**

   *Solution.* Core knowledge predicts expectations that appear without
   relevant experience and resist short exposure to contrary evidence; rational constructivism predicts
   expectations calibrated to the statistics of experience and updated by them. For example: give infants a short,
   controlled exposure to a display world in which some regularity is reversed (objects that pass through barriers
   on a screen), then test with violation of expectation. Unchanged surprise favours core knowledge; surprise that
   shifts with the exposure, in proportion to its amount, favours rational constructivism. Controlled-rearing
   studies in animals test the other half.

## Open checks

Checked against the articles, their abstracts or official pages (2026-11-15): ManyBabies 1's 67 laboratories,
2,329 infants (65 laboratories and 2,179 infants in the shared lab-level table) and its moderators (age, the
head-turn procedure, native-language stimuli); the pooled d = 0.35 recomputed; Kidd et al.'s 7- and 8-month-olds and
U-shaped look-away; Wynn's 5-month-olds, Wakeley et al.'s failure and Christodoulou et al.'s 12 studies, 26 samples,
550 infants and d = 0.34; Oostenbroek et al.'s 106 infants at 1, 3, 6 and 9 weeks and 11 models; Wellman et al.'s
178 studies; Baillargeon (1987) with 3.5- and 4.5-month-olds and Bogartz et al. (2000) with 5.5-month-olds; Xu and
Spelke's 8 against 16 and 12; Xu and Garcia's 8-month-olds; Onishi and Baillargeon's green and yellow boxes; Kulke et
al.'s four tasks; Meltzoff and Moore's 12- to 21-day-olds; van IJzendoorn and Kroonenberg's 32 samples, 8 countries
and 1,990 infants; Fearon et al.'s d = 0.31; Harlow's cloth and wire surrogates; Thomas and Chess's 40, 10 and 15
percent; Horner and Whiten's opaque and transparent boxes; DeLoache et al.'s 12- to 18-month-olds; Perry
Preschool's 123 children; the AAP's screening ages; Vong et al.'s 61 hours from 6 to 25 months; Piloto et al.'s five
concepts and 28 hours.

Still to recheck against the full texts before the final cut:

* Baillargeon, Spelke and Wasserman: the screen stopping at about 112 degrees.
* Tennessee pre-kindergarten: children who attended doing slightly worse by sixth grade (Durkin et al. 2022; the
  abstract was not read in full).
* Diamond (1985): the delay effect "month by month", described qualitatively.
* Meltzoff et al.'s reanalysis: its year (2017 online, 2018 in print) and journal.
* Kulke et al.: the Psychological Science paper's page numbers; and the companion paper in Cognitive Development.
* Halberda, Mazzocco and Feigenson (2008): the size of the 14-year-old sample, not quoted.
* Wimmer and Perner's age bands, described as "most three-year-olds" and "by about four or five".
