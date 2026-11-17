# Psychology, Built: Part 38, Culture and Morals

In 2008 a count of six leading psychology journals found that 68% of the samples were American and 96% came from
Western industrialized countries, which hold about 12% of humanity. In 2010 a review named them WEIRD (Western,
educated, industrialized, rich, democratic) and showed that on many measures they sit at one end of the human range.
This part asks whose mind psychology has been describing: what varies across cultures, what causes the variation,
how to measure it without fooling yourself, and how culture is inherited. Morality is the test case: one trolley
judged in forty-two countries, and a puppet show for babies tested in thirty-seven laboratories.

The hook is Arnett's count and the WEIRD paper; the viewer judges three trolley cases and predicts four numbers.
Then the Müller-Lyer illusion across societies and the dispute about why it varies (Part 14's row); independent and
interdependent selves, analytic and holistic attention, and the weak scales behind national scores; three theories
of where differences come from (rice farming, relational mobility, kinship and the Church); four ways a cross-cultural
comparison fails and the reference-group effect (computed); culture as inheritance: conformist and prestige-biased
copying (computed), faithful overimitation, and Henrich's model in which small populations lose skills (computed,
with its critics); moral psychology from Kohlberg to the social intuitionist model, Greene's dual process and moral
foundations; the Moral Machine, 42 countries and 45 countries (with a model of shared case effects, computed); the
infant helper study and ManyBabies 4; what travels (Many Labs 2) and constraints on generality; and the state of
the sample a decade on. The practice chapter is products, surveys and machines; the frontier is cultural distance,
historical psychology and machines as participants.

## Where the numbers come from

| What | Source |
|---|---|
| Conformist transmission with D = 0.3 among 200 learners who each sample three models: a variant starting at 45% vanishes and one at 55% takes over within 40 generations (the run with the median final share of 21 per start) | Psyche (`culture.conformist_sim`, `conformist_path`), item `conform` |
| Prestige-biased copying of the most successful of five models: a useless marker carried by 10% of people, mostly the skilled, reaches 74% after 30 generations in the median run of 21, and passes half in 14 of the 21 | Psyche (`culture.prestige_sim`), item `prestige` |
| Henrich's model with alpha = 4.5 and beta = 1: the critical population is about 51; over 60 generations from a skill of 10, 20 learners lose it, 50 hold near it (8.7) and 200 build it to 92 (median runs of 21) | Psyche (`culture.skill_change`, `tasmania`), item `tasmania` |
| Two cultures 0.8 SD apart (0.83 in the sample) rating themselves 1 to 7 against their own culture: mean ratings 4.01 and 4.00, a gap of −0.01 SD; a noisy behavioural measure shows 0.57 SD | Psyche (`culture.reference_group`), item `refgroup` |
| 42 simulated countries, 600 people each, with case effects set so the averages fall near 81%, 72% and 51%: the order Switch > Loop > Footbridge holds in every country while Footbridge acceptance ranges from 36% to 70% | Psyche (`culture.trolley`, `fit_trolley`), item `trolley` |
| Every published number on screen | the studies listed under Sources, quoted as reported |

Schematic panels (the illusion sizes, relational mobility, the personal-force bars, Many Labs 2's effects, the
network of laboratories, the model's similarity to countries, the two groups for the fixation index) are labelled
as schematic on screen and carry no data.

## Built in this part

* `explainer/psychology/psyche/culture.py`: Boyd and Richerson's conformist transmission (expected step and finite
  learners); prestige-biased copying with a hitchhiking marker; Henrich's model of imperfect copying, its expected
  gain and critical population; the reference-group effect; an additive logistic model of trolley judgments across
  countries and its fit. Tested in `tests/psychology/test_culture.py`.
* The Ledger gains nine rows. Part 2's WEIRD declaration and Part 30's overimitation declaration now point to the
  rows entered here.
* The course's interactive is the trolley: three classic cases and three variants, judged yes or no, with the
  classic cases set against the 42-country averages.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Most participants in psychology's leading journals come from WEIRD societies | Arnett 2008 | replicated |
| East Asians construe the self as interdependent and Westerners as independent, and questionnaires measure it | Markus and Kitayama 1991 | contested |
| Rice farming makes thinking more holistic and interdependent | Talhelm and colleagues 2014 | contested |
| Sacrificing one to save five is more acceptable by a switch than by personal force, in every country | Greene and colleagues 2001 | replicated |
| Five moral foundations, measured the same way across cultures | Graham, Haidt and Nosek 2009 | contested |
| Infants of six to ten months prefer a helper to a hinderer | Hamlin, Wynn and Bloom 2007 | failed |
| Larger populations accumulate skills and small isolated ones lose them | Henrich 2004 | contested |
| Children copy a demonstrator's useless actions, in every culture tested | Horner and Whiten 2005 | replicated |
| People keep moral judgments they cannot justify once every reason is ruled out | Haidt 2001 | contested |

Part 14's row on the Müller-Lyer illusion and culture (contested) is shown again in chapter 2. Shown without a row,
with the reason recorded in `explainer/psychology/ledger.py`: Masuda and Nisbett; Hofstede and Oyserman and
colleagues; Thomson and colleagues; Schulz and colleagues; the Moral Machine (2018); Many Labs 2; Simons, Shoda and
Lindsay; McGuire and colleagues' reanalysis; Atari and colleagues' preprint; Muthukrishna and colleagues' method.

## Build it

```bash
python -m videos.psychology.psych38.compute            # every number (a few seconds)
python tools/qa_scene.py psych38 Evolution             # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych38 -q l   # the whole part, silent preview
python tools/build.py psych38                          # 1080p30 with narration
python tools/qa_scene.py psych38 Trolley --lang zh     # the Chinese edition of one chapter
python tools/make.py psych38                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 38                    # the lab: conformity, Henrich's model, reference groups, trolleys
python tools/check_ledger.py psych38                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's culture module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | 2010: the weirdest people in the world | Who is in the experiments; WEIRD; the question; objectives |
| 1 | On you: three tracks, and four numbers | Switch, Loop and Footbridge; four predictions |
| 2 | Even an illusion varies | Two equal lines; why it varies is still argued |
| 3 | Independent and interdependent selves | Two construals; what is in the picture; how good are the measures |
| 4 | Where differences come from | The rice theory; relational mobility; cousins and the Church |
| 5 | Measuring across cultures | Four ways a comparison fails; the reference-group effect |
| 6 | Culture as inheritance | Copy the majority; copy the successful; copy faithfully; population size and lost skills |
| 7 | Moral psychology | The emotional dog; two processes in the scanner; moral foundations |
| 8 | One trolley, forty-two countries | The Moral Machine; same order, different levels; personal force in 45 countries |
| 9 | Do babies judge? | Helper and hinderer; thirty-seven laboratories |
| 10 | What travels | Twenty-eight findings in thirty-six countries; what holds, and how to say so |
| 11 | A psychology of everyone | A decade later; science by network |
| 12 | The Ledger | Nine rows and the tally |
| 13 | In practice: products, surveys and machines | Taking a test or a product abroad; aligning machines to whom? |
| 14 | Frontier: distance, history and machines | Cultural distance as a number; open questions |
| | Recap, problems, and the road ahead | Your numbers; eleven lines; Kant's three objections; payoffs; problems; references; Part 39 |

## Sources

* J. J. Arnett, The neglected 95%: why American psychology needs to become less American, *American Psychologist*
  63(7) (2008) 602-614; A. G. Thalmayer, C. Toscanelli and J. J. Arnett, The neglected 95% revisited, *American
  Psychologist* 76(1) (2021) 116-129; M. S. Rad, A. J. Martingano and J. Ginges, Toward a psychology of Homo
  sapiens, *PNAS* 115 (2018).
* J. Henrich, S. J. Heine and A. Norenzayan, The weirdest people in the world?, *Behavioral and Brain Sciences* 33
  (2010) 61-83; J. Henrich, *The WEIRDest People in the World* (2020).
* M. H. Segall, D. T. Campbell and M. J. Herskovits, *The Influence of Culture on Visual Perception* (1966); T. Gandhi,
  A. Kalia, S. Ganesh and P. Sinha, *Current Biology* 25 (2015); D. Amir and C. Firestone, *Psychological Review*
  (2025).
* H. R. Markus and S. Kitayama, Culture and the self, *Psychological Review* 98 (1991) 224-253; T. Masuda and R. E.
  Nisbett, Attending holistically versus analytically, *Journal of Personality and Social Psychology* 81 (2001);
  G. Hofstede, *Culture's Consequences* (1980); D. Oyserman, H. M. Coon and M. Kemmelmeier, *Psychological Bulletin*
  128 (2002) 3-72; R. E. Nisbett, *The Geography of Thought* (2003).
* T. Talhelm et al., *Science* 344 (2014) 603-608; R. Thomson et al., *PNAS* 115 (2018) 7521-7526; J. F. Schulz,
  D. Bahrami-Rad, J. P. Beauchamp and J. Henrich, The Church, intensive kinship, and global psychological variation,
  *Science* 366 (2019).
* S. J. Heine, D. R. Lehman, K. Peng and J. Greenholtz, What's wrong with cross-cultural comparisons of subjective
  Likert scales?, *Journal of Personality and Social Psychology* 82(6) (2002) 903-918.
* R. Boyd and P. J. Richerson, *Culture and the Evolutionary Process* (1985); J. Henrich, Demography and cultural
  evolution, *American Antiquity* 69 (2004) 197-214; K. Vaesen, M. Collard, R. Cosgrove and W. Roebroeks, *PNAS* 113
  (2016) E2241-E2247; V. Horner and A. Whiten, *Animal Cognition* 8 (2005); M. Nielsen and K. Tomaselli,
  *Psychological Science* 21 (2010); M. Berl and B. S. Hewlett, *PLoS ONE* (2015); R. Stengelin, R. Hepach and
  D. B. M. Haun (2020).
* J. Haidt, The emotional dog and its rational tail, *Psychological Review* 108 (2001) 814-834; E. B. Royzman, K. Kim
  and R. F. Leeman, *Judgment and Decision Making* 10 (2015) 296-313; J. D. Greene et al., *Science* 293 (2001)
  2105-2108; C. McGuire, R. Langdon, M. Coltheart and C. Mackenzie, *Journal of Experimental Social Psychology* 45
  (2009); J. Graham, J. Haidt and B. A. Nosek, *Journal of Personality and Social Psychology* 96 (2009); K. Iurino and
  G. Saucier, *Assessment* 27(2) (2020) 365-372.
* E. Awad et al., The Moral Machine experiment, *Nature* 563 (2018) 59-64; E. Awad, S. Dsouza, A. Shariff, I. Rahwan
  and J.-F. Bonnefon, *PNAS* 117 (2020) 2332-2337; B. Bago et al., *Nature Human Behaviour* 6 (2022) 880-895.
* J. K. Hamlin, K. Wynn and P. Bloom, Social evaluation by preverbal infants, *Nature* 450 (2007) 557-559; K. Lucca
  et al., Infants' social evaluation of helpers and hinderers (ManyBabies 4), *Developmental Science* 28 (2025)
  e13581.
* R. A. Klein et al., Many Labs 2, *Advances in Methods and Practices in Psychological Science* 1 (2018); D. J.
  Simons, Y. Shoda and D. S. Lindsay, Constraints on generality (COG), *Perspectives on Psychological Science* 12
  (2017); M. Muthukrishna et al., Beyond WEIRD psychology, *Psychological Science* 31(6) (2020) 678-701;
  M. Atari, M. J. Xue, P. S. Park, D. E. Blasi and J. Henrich, Which humans? (preprint, 2023).

## Problems and solutions

1. **Conformist transmission.** With k carriers among three models (binomial, p), the adoption chance is 0,
   1/3 − D/3, 2/3 + D/3, 1. The expected share is 3p(1 − p)²(1/3 − D/3) + 3p²(1 − p)(2/3 + D/3) + p³. Without D this
   is p(1 − p)² + 2p²(1 − p) + p³ = p. The D terms add D p(1 − p)[p − (1 − p)] = D p(1 − p)(2p − 1). Fixed points:
   p = 0, 1/2, 1. The derivative of the step at p is 1 + D(−6p² + 6p − 1); at 0 and 1 it is 1 − D < 1 (stable for
   0 < D < 2), at 1/2 it is 1 + D/2 > 1 (unstable).
2. **Henrich's critical population.** The best of N copies gains β(γ + ln N) − α. Setting it to zero gives
   N* = exp(α/β − γ) = exp(4.5 − 0.5772) ≈ 50.5.
3. **The reference-group effect.** If each person reports a fixed function of their own z-score within their culture,
   the expected rating is the same in both cultures, so the expected difference is 0, whatever the true gap. Designs
   that recover it: an absolute behavioural measure (time worked, punctuality), anchoring vignettes that put everyone
   on the same reference, or ratings of the same targets by judges from both cultures.
4. **The trolley model keeps the order.** For a country with level ℓ, the acceptance of case k is σ(c_k + ℓ). The
   logistic function is strictly increasing, so c₁ > c₂ > c₃ implies σ(c₁ + ℓ) > σ(c₂ + ℓ) > σ(c₃ + ℓ) for every ℓ.
   Sampling noise can swap two close cases in a small sample, which is why Psyche uses 600 people per country.
5. **How surprising was ManyBabies 4?** With a true preference of 0.6 and n = 567, the share chosen has mean 0.6 and
   SD √(0.6 × 0.4/567) ≈ 0.0206. Observing 0.493 or less is (0.6 − 0.493)/0.0206 ≈ 5.2 SDs below the mean: chance of
   about 1 in 10 million. Even a modest true preference is very hard to square with the result.
6. **Arnett's over-representation.** Per head, the WEIRD countries supply 96/12 = 8 samples per percent of
   population and the rest 4/88 ≈ 0.045, so a person in those countries is about 8/0.045 ≈ 176 times as likely to be
   in a sample.
7. **A constraints-on-generality statement.** For example, the Switch–Footbridge order: "We expect the order to hold
   in adults in any society with the concept of personal force, for these three cases as worded; we do not expect
   the levels to be constant; the 42-country and 45-country studies support this; the samples were online or
   student volunteers, so we do not claim it for people without schooling." The smallest test: the three cases with
   a pre-registered within-person comparison, in a population unlike those studied (for example, a rural community
   sampled door to door), with enough people to detect a ten-point difference between Switch and Footbridge.

## Open checks

Checked against the articles, their abstracts or official pages, or named secondary summaries of them
(2026-11-16): Arnett's 68% and 96% and the 12% of the world's population; Thalmayer, Toscanelli and Arnett's "a little
over 60%" and 4 to 5%; Rad, Martingano and Ginges's "about half" (from the authors' summary); the WEIRD paper's
claims; Segall, Campbell and Herskovits's design (more than a dozen societies; the San result via the WEIRD paper's
figure); Gandhi et al.'s 48 hours; Talhelm et al.'s 1,162 students and six sites and the critiques' points;
Thomson et al.'s 39 societies, nearly 17,000 people and correlates; Schulz et al.'s 24 outcomes; Heine et al.'s
findings; Oyserman, Coon and Kemmelmeier's conclusion (the "smaller and less consistent" wording summarizes the
abstract and Kitayama's commentary); Royzman, Kim and Leeman's harm finding; McGuire et al.'s reanalysis; Iurino
and Saucier's 27 countries; the Moral Machine's 40 million decisions, ten languages, 2.3 million people and 233
countries and territories; Awad et al.'s 70,000 people, 42 countries, 81%, 72% and 51%; Bago et al.'s 45 countries
and results; Hamlin, Wynn and Bloom's 12 of 12 and 14 of 16 (via a secondary source); ManyBabies 4's 1,018, 567,
37 labs, 49.34% and 55.85%; Many Labs 2's 28 findings, 125 samples, 15,305 people, 36 countries and territories,
medians 0.60 and 0.15 and 15 significant; Vaesen et al.'s argument; Berl and Hewlett's Aka result; Muthukrishna et
al.'s method; Atari et al.'s result (preprint). Not re-checked here: Masuda and Nisbett's details (the focal fish
and the recognition test), Hofstede's survey design (described only as dozens of countries), the first names
Robert Thomson and Kathryn Iurino, and the exact volume or article numbers for Nielsen and Tomaselli, Berl and
Hewlett, and Stengelin et al.
