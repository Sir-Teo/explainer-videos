# Psychology, Built: Part 60, Minds and Machines

In 1958 a learning machine, the Perceptron, was published in *Psychological Review* by a psychologist. For decades
artificial intelligence borrowed from psychology; now the debt runs both ways. Language models are given
psychology's tests, proposed as models of the mind, used as advisers, helpers and stand-in participants. Each of
those uses is a psychological claim, and this part tests each one with the tools of the previous fifty-nine.

The viewer reads six sentences about the mind (three by William James, three written for the film by a language
model in his manner) and predicts four numbers. Then networks as models of vision and language, and why behaviour
matched is not mechanism shared; machine psychology and its three traps (contamination, prompt sensitivity, one
model as a sample of one), simulated with the truth known; theory of mind in machines; a benchmark treated as a
test, with item response theory and the number of items needed to separate two models; algorithm aversion and
appreciation, with aversion as a learning rule; mind perception; a dialogue that reduced conspiracy belief, and
sycophancy; chatbots in care by Part 42's standards; silicon samples that match means and erase spread and
minorities; the screens-and-well-being dispute with each side's best case and a specification curve; what machines
lack; and a science of machine behaviour.

No language model is run in this part: Psyche's `machines` module simulates each method problem with the truth
known.

## Where the numbers come from

| What | Source |
|---|---|
| Contamination: 200 four-option items; a memorizer that saw 80% of them, a reasoner right 56% of the time; mean of 20 runs: 85% and 56% on the published items, 25% and 54% on reworded twins | Psyche (`machines.contamination`), item `contam` |
| Prompts: one model (rate drawn around 0.6, between-model SD 0.15) asked in 100 phrasings (SD 0.08): estimate 0.42, interval 0.41 to 0.44 treating phrasings as subjects, 0.13 to 0.72 for a claim about models | Psyche (`machines.prompt_sample`), item `prompts` |
| A 300-item benchmark under the two-parameter model (discriminations 0.2 to 2.5, difficulties SD 1.5), twelve models with abilities -1.5 to 1.5: the most informative fifth of the items carries 47% of the information | Psyche (`machines.benchmark_irt`), item `irt` |
| Items to separate models at 70% and 73% (5% two-sided, 80% power): about 3,700 independent, about 1,800 paired with item-score correlation 0.5 | Psyche (`machines.items_to_separate`), item `separate` |
| Silicon samples: 5,000 respondents in five groups (45%, 30%, 15%, 7%, 3%), within-group SD 1.6; silicon spread shrunk to 35% and small groups pulled toward the overall mean: means 5.13 and 5.13, SDs 1.68 and 0.68, the 3% group off by +0.9 | Psyche (`machines.silicon`), item `silicon` |
| Aversion: 2,000 people, an aid right 80% and own judgment 70%; reliance halved after a seen error of the aid, regained 0.03 a trial: reliance 0.70 to 0.47, accuracy 0.75 against 0.80 | Psyche (`machines.aversion`), item `reliance` |
| A specification curve: 10,000 simulated teenagers, a true effect of -0.03 SD, four confounders; 288 analyses: every coefficient negative, from -0.15 to -0.01, 95% significant, median variance explained 1.1% | Psyche (`machines.specification_curve`), item `spec` |
| The six sentences: three from William James, *The Principles of Psychology* (1890), public domain; three written for this film by a language model in his manner | as stated on screen |
| Every published number on screen | the studies listed under Sources, quoted as reported |

## Built in this part

* `explainer/psychology/psyche/machines.py`: contamination, prompt samples, a benchmark under item response theory
  with leaderboard stability, items to separate two models, silicon samples, reliance and algorithm aversion, and a
  specification curve. Tested in `tests/psychology/test_machines.py`.
* The Ledger gains five rows.
* The course's interactive: human or machine? Six sentences, then a slider for how much you rely on an aid, with
  your accuracy.

## The Ledger

| Finding | Original | Status |
|---|---|---|
| Large language models given psychology's classic judgment problems show the same biases people do. | Binz and Schulz 2023 | contested |
| Large language models solve false-belief tasks in a way that shows a robust theory of mind. | Kosinski 2023 | contested |
| After seeing an algorithm err, people avoid it in favour of human judgment, even when the algorithm is more accurate. | Dietvorst, Simmons and Massey 2015 | contested |
| A short conversation with a language model that answers a person's own evidence durably reduces their belief in a conspiracy theory. | Costello, Pennycook and Rand 2024 | not directly tested |
| The spread of smartphones and social media caused a large rise in depressive symptoms among adolescents. | Twenge and colleagues 2018 | contested |

Shown without a row, with the reason recorded in `explainer/psychology/ledger.py`: Rosenblatt; Yamins and DiCarlo;
Heinz and colleagues; Argyle and colleagues; Lake and colleagues; Rahwan and colleagues.

## Build it

```bash
python -m videos.psychology.psych60.compute            # every number (seconds)
python tools/qa_scene.py psych60 Silicon               # one chapter, silent, at 480p, with a contact sheet
EXPLAINER_TTS=silent python tools/build.py psych60 -q l   # the whole part, silent preview
python tools/build.py psych60                          # 1080p30 with narration
python tools/qa_scene.py psych60 Trust --lang zh       # the Chinese edition of one chapter
python tools/make.py psych60                           # both editions, with the checks a long build needs
python -m videos.psychology.labs 60                    # the lab: contamination, benchmarks, silicon samples
python tools/check_ledger.py psych60                   # every study shown has its Ledger row, or a reason
python -m pytest tests/psychology                      # Psyche's machines module, the Ledger, the Archive
```

The Chinese edition is `zh_lines.py` (the narration, line by line) and the series table
`videos/psychology/psychology_text_zh.json` (the text on screen); the terms are in
[`PSYCHOLOGY_ZH_GUIDE.md`](../PSYCHOLOGY_ZH_GUIDE.md).

## Chapters

| # | Chapter | What it does |
|---|---|---|
| 0 | A psychologist's machine | Rosenblatt and ELIZA; the question; objectives |
| 1 | On you: human or machine, and four numbers | Six sentences; four predictions |
| 2 | Networks as models of the mind | Vision; language; behaviour matched is not mechanism shared |
| 3 | Machine psychology | The classic problems given to a model; contamination; prompts and one model |
| 4 | Theory of mind in machines | A claim, its perturbations and a comparison; what a valid test needs |
| 5 | Psychometrics for machines | A benchmark is a test; which items do the work; how many items |
| 6 | People trusting machines | Aversion and appreciation; what aversion costs; seeing a mind |
| 7 | Machines changing minds | A conversation about a conspiracy theory; machines that agree |
| 8 | Machines as helpers and companions | The trial evidence; Part 42's standards |
| 9 | Silicon samples | Out of one, many; five groups, human and silicon |
| 10 | Screens and well-being | A dispute with each side's best case; a specification curve; experiments |
| 11 | What machines lack, and have | Child-like learning; Part 27's question asked of machines |
| 12 | A science of machine behaviour | Machine behaviour; the toolkit, part by part |
| 13 | The Ledger | Five rows; what they have in common |
| 14 | In practice: evaluating a model | Where this is a job; a worked evaluation plan |
| 15 | Frontier: two sciences of minds | What is new; open problems |
| | Recap, problems, and the road ahead | Your numbers; twelve lines; payoffs; problems; references; Part 61 |

## Sources

* F. Rosenblatt, The perceptron: a probabilistic model for information storage and organization in the brain,
  *Psychological Review* 65 (1958) 386-408; J. Weizenbaum, ELIZA: a computer program for the study of natural
  language communication between man and machine, *Communications of the ACM* 9 (1966) 36-45; J. Weizenbaum,
  *Computer Power and Human Reason* (Freeman, 1976); W. James, *The Principles of Psychology* (Holt, 1890).
* D. L. K. Yamins and J. J. DiCarlo, Using goal-driven deep learning models to understand sensory cortex, *Nature
  Neuroscience* 19 (2016) 356-365; J. S. Bowers et al., Deep problems with neural network models of human vision,
  *Behavioral and Brain Sciences* 46 (2023) e385; K. Mahowald et al., Dissociating language and thought in large
  language models, *Trends in Cognitive Sciences* 28 (2024) 517-540.
* M. Binz and E. Schulz (2023); T. Hagendorff, S. Fabi and M. Kosinski (2023); M. Kosinski (2023, 2024); T. Ullman
  (2023); J. W. A. Strachan et al. (2024).
* B. J. Dietvorst, J. P. Simmons and C. Massey (2015, 2018); J. M. Logg, J. A. Minson and D. A. Moore (2019); H. M.
  Gray, K. Gray and D. M. Wegner, Dimensions of mind perception, *Science* 315 (2007) 619.
* T. H. Costello, G. Pennycook and D. G. Rand (2024); M. Sharma et al., Towards understanding sycophancy in language
  models, *International Conference on Learning Representations* (2024).
* K. K. Fitzpatrick, A. Darcy and M. Vierhile, Delivering cognitive behavior therapy to young adults with symptoms
  of depression and anxiety using a fully automated conversational agent (Woebot), *JMIR Mental Health* 4 (2017)
  e19; M. V. Heinz et al., Randomized trial of a generative AI chatbot for mental health treatment, *NEJM AI* 2
  (2025).
* L. P. Argyle et al., Out of one, many: using language models to simulate human samples, *Political Analysis* 31
  (2023) 337-351.
* J. M. Twenge et al. (2018); A. Orben and A. K. Przybylski (2019); H. Allcott, L. Braghieri, S. Eichmeyer and M.
  Gentzkow (2020).
* B. M. Lake, T. D. Ullman, J. B. Tenenbaum and S. J. Gershman, Building machines that learn and think like people,
  *Behavioral and Brain Sciences* 40 (2017) e253; P. Butlin et al., Consciousness in artificial intelligence:
  insights from the science of consciousness, arXiv preprint 2308.08708 (2023); I. Rahwan et al., Machine
  behaviour, *Nature* 568 (2019) 477-486; M. Jakesch, J. T. Hancock and M. Naaman, Human heuristics for
  AI-generated language are flawed, *PNAS* 120 (2023) e2208839120.

## Problems and solutions

1. **Contamination.** A model scores 85% on published items and 26% on reworded twins with four options each. What do you conclude?

   *Solution.* 26% with four options is chance: the 85% came from remembering the published items, not
   from solving the problems. Test on new items.
2. **The sample size.** Twelve models, each tested with 100 phrasings. What is the sample size for a claim about models?

   *Solution.* Twelve: for a claim about models the model is the unit; the 100 phrasings per model
   estimate each model's rate precisely but add no models.
3. **Two models.** Two models at 70% and 73%, 1,000 shared items, item scores correlated 0.5. Can you tell them apart?

   *Solution.* The paired standard error is sqrt(2 x 0.21 x 0.5 / 1000) = 0.0145; the difference is 2.1
   standard errors, so power is only about 54%: the comparison may or may not come out significant, and 1,800 items
   would be needed for 80% power.
4. **Reliance.** An aid is right 80% of the time, you 70%. Your accuracy if you follow it half the time, at random?

   *Solution.* 0.5 x 0.8 + 0.5 x 0.7 = 0.75; following the aid always gives 0.80.
5. **Silicon samples.** Silicon respondents match a survey's mean but have half its SD. Which conclusions survive?

   *Solution.* Claims about averages may survive; claims about variability, polarization, correlations
   between answers (attenuated by the shrunk spread) and small groups do not, and every claim must be checked on
   people.
6. **A tiny association.** Screen time explains 0.4% of the variance in well-being. Could it still matter? For whom?

   *Solution.* Yes: a small average can hide large effects for a few people, or effects of specific
   uses (at night, on particular content), and small effects summed over a population matter for policy. That is a
   reason to measure who is affected, not to assume large average harm.
7. ★ **A trial.** Design a randomized trial of a mental-health chatbot that would meet Part 42's standards.

   *Solution.* Randomize adults with depressive symptoms to the chatbot or to an active comparison (guided
   self-help, or a human-delivered brief therapy), with a preregistered primary outcome assessed blind at three and
   six months; count harms (adverse events, worsening, how urgent-help situations are handled); analyse everyone
   randomized; and report engagement from logs.

## Open checks

The web-search budget for this session was spent on earlier parts, so the facts in this part come from the
standard literature and were not re-checked online today; each is listed here to be checked against its source:
the three James quotations, word for word; Rosenblatt (1958); ELIZA's date and Weizenbaum's reaction; Yamins and
DiCarlo (2016); Bowers et al. (2023); Mahowald et al. (2024); Binz and Schulz (2023)'s tasks; Hagendorff, Fabi and
Kosinski (2023); Kosinski (2023, 2024); Ullman (2023)'s alterations; Strachan et al. (2024)'s 1,907 participants
and results; Dietvorst et al. (2015, 2018); Logg et al. (2019); Gray, Gray and Wegner (2007); Costello et al.'s
sample, three rounds, about 20% and two months; Sharma et al. on sycophancy; the Woebot trial; Heinz et al.
(2025)'s sample, control and outcomes; Argyle et al. (2023); Twenge et al. (2018); Orben and Przybylski (2019)'s
0.4% and the glasses-and-potatoes comparison; Allcott et al. (2020)'s four weeks and results; Lake et al. (2017);
Butlin et al. (2023); Rahwan et al. (2019); Jakesch et al. (2023); Ullman (2023)'s transparent-container
perturbation; Frank (2023) on the data gap between children and language models; and every page range in Sources.
