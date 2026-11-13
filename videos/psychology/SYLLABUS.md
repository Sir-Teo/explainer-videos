# Psychology, Built: the syllabus (plan of record, draft 1)

Goal: a university education in psychology on video, from the first lecture of an introductory course to the level
of a doctoral qualifying exam, followed by the curriculum that industry and the clinic work from. It aims to be
**as comprehensive as the textbooks, as technical as a graduate methods sequence, as practical as a working
practitioner's knowledge, and as honest about its evidence as the field has learned to be**. It is told as one
story, Kant's wager ([README](README.md)). Each part runs **30–60 minutes**, most at 45–55, and its content decides
where in that range it lands. Sixty-two parts come to about **52 hours**: a degree in forty-three, a graduate
toolkit in seven, the practice in seven and a research tier in five.

The plan has the shape of a degree plus a career:

- **Act I** is research methods, measurement and statistics for psychology (Shadish, Cook & Campbell; Cronbach;
  Cohen; Chambers).
- **Act II** is biological psychology and behavioural neuroscience (Kandel; Bear, Connors & Paradiso; Dayan &
  Abbott; Plomin).
- **Act III** is sensation and perception (Wolfe; Green & Swets; Wandell; Marr; Moore).
- **Act IV** is learning (Bouton; Sutton & Barto).
- **Act V** is cognitive psychology and cognitive science, the largest act (Anderson; Kahana; Luce; Kahneman;
  Griffiths, Chater & Tenenbaum).
- **Acts VI–VIII** are motivation and emotion, developmental psychology, and individual differences (Reeve; Siegler;
  Deary; Funder).
- **Act IX** is social psychology (Aronson; Fiske & Taylor; Henrich).
- **Act X** is psychopathology and treatment, and ends on the degree's capstone (Barlow; Kring; Wampold).
- **Act XI is the graduate toolkit**: quantitative and mathematical psychology (Bollen; Embretson & Reise; Train;
  Farrell & Lewandowsky; Poldrack, Mumford & Nichols; Borenstein).
- **Act XII is the practice**: human factors, HCI, industrial and organizational psychology, education, behavioural
  science in policy and business, psychology and law, health psychology and the delivery of care.
- **The research tier** runs through the whole series and ends in its own act. Every part closes with a *Frontier*
  chapter (§1.1). **Act XIII** then covers theory at research level, computational psychiatry, psychology's
  exchange with AI, the field's own reform, and how research is done.

Each part's **Reading** line names the textbooks, the classic papers and the recent papers it follows. Each part's
**In practice** line names the jobs, products and decisions it maps to. §2.6 maps the series onto a degree and
onto the roles graduates fill.

## 1. The standard every part meets

The standard is *AI, Built*'s ([`../ai/SYLLABUS.md`](../ai/SYLLABUS.md) §1 and
[`../ai/LECTURE_GUIDE.md`](../ai/LECTURE_GUIDE.md)), with *Computer Science, Built*'s research tier and *In practice*
cards, plus the rules specific to psychology, marked **(Psy)**.

**A part is one story.** It opens on a hook that a person off the street would stop for: a horse that does
arithmetic, a man who cannot form a memory, a line of lengths that eight people call wrong. It then:

1. shows the phenomenon and **runs it on the viewer**;
2. tells how it was found (the people, the year, the apparatus, the dead ends);
3. builds the mechanism: definitions, the model derived step by step, and the code that runs it;
4. confronts the model with data, and shows where it fits and where it fails;
5. enters the findings in **the Ledger**: how big, how sure, and what happened on replication;
6. closes with *In practice*, the *Frontier*, and the question the next part takes up.

A chapter that does not serve the part's story is cut, or moved to the part it serves.

**A chapter is a lecture segment of 3–4 minutes,** twelve to sixteen to a part. It runs in this order:

1. A motivating question, demonstration or historical moment, drawn.
2. A definition card, in words and then in symbols.
3. The derivation or the experimental logic on screen, every step, each with a margin reason ("random assignment",
   "Bayes' rule", "the likelihood ratio is monotone", "regression to the mean").
4. A computed experiment: Psyche run on the task, a fit to Archive data, or a study replayed on the Pool.
5. A *pause-and-predict* question. **(Psy)** Predictions are about data: "which bar is taller?", "does it
   replicate?".
6. The takeaway, with a forward link (a payoff card).

**Per part:**
- An objectives card.
- Definition, model, theorem, study and history cards. **(Psy)** A *study card* always shows design, N, the effect
  size with its interval, and the Ledger status.
- **(Psy)** At least one **On you** segment (§2.4): a demonstration or Battery task the viewer performs, with the
  published result revealed afterwards.
- **(Psy)** One or more rows of **the Ledger** (§2.5), and where the textbook story is wrong, a *story and record*
  card.
- A problem set: 5–6 problems, about 90 s on screen, with full solutions in the part's README. The mix: a
  derivation, a model computation with Psyche, a design critique ("find the confound"), a data problem on the
  Archive or the Pool, and one research problem (★, §1.1). Practice-facing parts add one problem in that style
  ("design the selection system for…").
- A reference card: textbooks, the classic papers, recent papers.
- An *In practice* card in the outro.
- A *Frontier* chapter before the outro (§1.1).

**The history thread.** Every part opens with its era (2–3 min), lit on the timeline strip (1850–2030). Every idea
is credited with its people and year, its dead ends included: phrenology, introspection's stalemate, radical
behaviourism's ban on the mind, the lobotomy, the refrigerator mother, facilitated communication, the recovered-
memory epidemic. **(Psy)** The history of who was studied and who was excluded is part of it (§1.2).

**Numbers and claims.**
- Computed numbers come from the part's `compute.py`, cached under `.cache/psychN/`. Narration that states a result
  is an f-string over the cached data, and branches on it when the verdict depends on the outcome (a model wins a
  comparison, a simulated replication fails).
- **(Psy)** Published results are cited on screen with N and effect size. A standardized effect is always shown
  with a picture of what it means (two overlapping distributions, or a common-language probability), never as a
  bare d or r.
- **(Psy)** Archive data are transcribed from the original publication, or loaded from the authors' open
  repository, with licence and source recorded in `explainer/psychology/archive/SOURCES.md`. A dataset whose
  licence does not allow redistribution is cited and summarized, not stored.
- **(Psy)** Pool results are labelled `simulated`. A simulation shows what a method can and cannot recover; it is
  never offered as evidence about people.
- Schematics are labelled `schematic` and made-up examples `illustrative`.
- `assert`s in `compute.py` are for invariants: the Hodgkin–Huxley integrator conserves what it should, the
  diffusion simulator matches its closed-form accuracy, the factor analyser recovers planted loadings.
- CPU budget: at most 1 h per part by default, seeded and resumable. Named exceptions (hierarchical Bayesian fits in
  Parts 25, 48 and 59, sparse coding in Part 58, the agent-based models of Parts 34 and 61) get up to 6 h.

**Frontier sweep.** Before a part is written, its literature is checked against primary sources up to the writing
date: the *Annual Review of Psychology*, *Psychological Bulletin*, *Psychological Review*, *Perspectives on
Psychological Science*, *AMPPS*, *Nature Human Behaviour*, *Behavioral and Brain Sciences*, the field's own journals,
PsyArXiv, and the registries of replication projects. Results the plan relies on that are recent or disputed are
marked **(verify)** below and must be checked against their primary sources before they go on screen. **(Psy)**
Because Ledger statuses change, each Ledger row carries the date it was last checked.

**Bilingual standard (as *AI, Built*).** Every narration line has its entry in `narration_zh.json`, or in the
part's `zh_lines.py` template when the line is computed. Every on-screen string is in `psychology_text_zh.json`,
and `tools/collect_text.py --check psychN` is clean. `PSYCHOLOGY_ZH_GUIDE.md` is the glossary and follows the
standard terms of Chinese psychology (信号检测论, 工作记忆, 经典条件作用, 认知失调, 效应量, 可重复性危机, 项目反应理论).
**(Psy)** Demonstrations that depend on language (Stroop, the DRM lists, garden-path sentences, the lexical
personality items) are rebuilt in Chinese with Chinese materials and Chinese norms where they exist, not
translated.

**Gates per part:** `tools/lecture_length.py` (floor 30 min; a part that would pass 60 is split or trimmed),
`contact_sheet.py`, `dead_air.py`, `collect_text.py --check`, `check_narration.py`, `zh_lines.py --verify`, the
part's `tests/psychology/test_*.py`, and **(Psy)** a Ledger check, to be written in Phase 0: every study card on
screen has a Ledger row with a source and a date.

### 1.1 The research tier

Every part ends its content with a **Frontier** chapter (4–7 minutes), written for a PhD student. It does four
things:

1. **What is not known**, stated precisely: the competing models and the data that would separate them.
2. **The best current evidence**, with dates: the largest replication, the most recent meta-analysis and what its
   bias corrections do to the estimate, the adversarial collaboration if there is one.
3. **Two or three recent papers** and what each changed, checked in the frontier sweep.
4. **A research problem (★)** in the problem set: open-ended, possibly open. The README says what is known, how a
   researcher would attack it, and which Psyche module or Archive dataset is the place to start.

### 1.2 Care **(Psy)**

Psychology's subject matter is people, and some of it is painful. These rules bind every part.

- **Not advice.** Parts 39–42, 57 and 59 open with a card: this is education, not diagnosis or treatment, and here
  is where help is found. Suicide and self-harm are covered under safe-messaging guidelines: no method detail, no
  framing as a solution, help resources on screen.
- **No scoring of viewers.** On-you demonstrations show the viewer a phenomenon. They never return an IQ, a
  clinical score, a personality type or a percentile for an ability. The matrix puzzles of Parts 32 and 45 are
  demonstrations of an adaptive test's mechanics and say so.
- **No harm in demonstrations.** No flicker faster than 3 Hz, no startling audio, a colour-vision note where it
  matters, and nothing that deceives the viewer for longer than the demonstration.
- **Disorders are described in people-first, non-stigmatizing language,** with prevalence and the range of
  outcomes, and with the voices of people who live with them where a published first-person source exists.
- **Named patients are people.** Henry Molaison, Phineas Gage, Louis Leborgne, Genie, the Genain sisters: the
  record of what was done to and for them is part of the story.
- **Group comparisons** (sex, race and ethnicity, class, culture) are shown only with the full distributions, the
  measurement-invariance evidence, the size of within-group variation and the history of how such comparisons
  were abused. The narration states what the data cannot show.
- **The history of harm is told plainly:** eugenics and the testing movement, forced sterilization, lobotomy,
  conversion therapy, the Tuskegee study, the Monster study, psychologists and interrogation. Each appears in the
  part whose science it distorted.
- **Tests and criteria.** Commercial tests (Wechsler scales, Raven's matrices, the MMPI) and the DSM's text are
  copyrighted and, for tests, secure. They are described and cited, never reproduced. The series uses
  public-domain instruments (the IPIP items) and items it generates itself.
- **Each side's best case** on open questions, in its defenders' words where possible, and the narration says that
  the question is open.

## 2. The devices

### 2.1 Psyche, the model subject

`explainer/psychology/psyche/` is a library of small models, one faculty per part, each a few hundred lines of
numpy with a docstring that states the equations. Three rules:

- **It runs the same tasks people do.** Every module exposes `run(task, params, seed)` and returns trial-level
  data in the Battery's format, so one plotting and fitting pipeline serves people, Psyche and the Pool.
- **It is checked.** Each module has tests in `tests/psychology/` against an independent reference: a closed form
  (diffusion-model accuracy and mean RT, the Rescorla–Wagner asymptote, the Rasch likelihood), a published
  parameter set reproducing a published figure, SciPy, or statkit.
- **It is fitted, not tuned by eye.** From Part 11 on, parameters shown on screen come from a fit to named data,
  and from Part 48 on every fit shows its parameter-recovery check.

Modules, with the part that introduces each:

| Module | Part | What it holds |
|---|---|---|
| `chronometry` | 1 | additive stage models of reaction time; Donders' subtraction; Sternberg's additive factors |
| `neuron` | 5 | Nernst and GHK; the passive membrane; Hodgkin–Huxley; FitzHugh–Nagumo; LIF and adaptive LIF; the cable equation |
| `circuits` | 6 | conductance synapses; Hebbian, BCM and STDP rules; lateral inhibition; winner-take-all; half-centre oscillators; Wilson–Cowan |
| `brain` | 7, 8 | a lesionable box-and-arrow architecture; neural mass to BOLD (the haemodynamic response); a lead-field toy for EEG |
| `genes` | 9 | the Pool's additive genomes; twin, adoption and family simulators; ACE fits; GWAS and polygenic scores |
| `body` | 10 | a circadian oscillator; the two-process model; an HPA feedback loop; receptor occupancy and tolerance |
| `psychophysics` | 11 | psychometric functions; constant stimuli, limits and adjustment; staircases and QUEST; ML fits with intervals |
| `sdt` | 12 | equal- and unequal-variance observers; yes–no, rating and 2AFC; ROC and d′; ideal observers |
| `vision` | 13 | an optical point spread; cone fundamentals and colour matching; centre–surround and Gabor banks; contrast normalization |
| `infer` | 14 | Bayesian observers; cue combination; the motion prior; a small recognition network with a behavioural readout |
| `hearing` | 15 | a gammatone filter bank; autocorrelation pitch; a Jeffress coincidence array; a gate-control circuit |
| `conditioning` | 16 | Rescorla–Wagner; Mackintosh and Pearce–Hall; the comparator hypothesis; an operant chamber with schedules; matching |
| `rl` | 17 | TD(λ); actor–critic; Q-learning; model-based planning; the two-step task; the successor representation; bandit policies |
| `attention` | 18 | a saliency map; guided search; the normalization model; a theory-of-visual-attention race; Stroop conflict |
| `wm` | 19 | slot, resource and mixture models; a ring attractor; an interference model of span |
| `memory` | 20, 21 | SAM; the temporal context model; a Hopfield network; ACT-R base-level activation; complementary learning systems; a schema-driven false-memory model |
| `concepts` | 22 | prototype and exemplar models; the generalized context model; ALCOVE; Bayesian generalization; MDS |
| `language` | 23 | the interactive activation model; a cohort and TRACE-style recognizer; transitional-probability segmentation; a past-tense network; surprisal from *AI, Built*'s novels model |
| `reason` | 24 | a production system with goal stack; mental-model enumeration; problem-space search; a rotation model; causal power and causal Bayes nets |
| `decide` | 25 | random walks and the SPRT; drift–diffusion with across-trial variability; the LBA; leaky competing accumulators; the stop-signal race; meta-d′ |
| `choice` | 26 | expected utility; cumulative prospect theory; discounting models; the heuristics toolbox; decision by sampling |
| `workspace` | 27 | a global-workspace ignition network; rivalry by adaptation and inhibition |
| `drive` | 28 | homeostatic control; incentive salience; the expected value of control |
| `emotion` | 29 | an appraisal model; a core-affect space; a fear-learning circuit |
| `develop` | 30, 31 | habituation and the Goldilocks model; a dynamic neural field; growth and ageing curves |
| `traits` | 32, 33 | the Pool's generative models for abilities and traits; factor analysis; mutualism dynamics |
| `social` | 34–38 | threshold cascades; DeGroot and bounded-confidence opinion dynamics; Schelling; inverse planning; repeated-game players; cultural transmission chains |
| `clinic` | 39–42 | Ising symptom networks; a helplessness learner; an avoidance loop; strong- and weak-prior perceivers; a therapy-trial simulator |
| `sem`, `irt`, `scaling` | 44–46 | path models and CFA by ML; Rasch to 3PL and graded response, CAT; Thurstone, Bradley–Terry–Luce, conjoint, MaxDiff |
| `fit` | 48 | likelihoods for every model above; optimizers; hierarchical Bayes on statkit's probabilistic programming language; parameter and model recovery |
| `neurodata` | 49 | a synthetic brain with ground truth; GLM, cluster inference, decoding, RSA, encoding models, ERP averaging |
| `meta` | 50 | fixed and random effects; bias detection and correction; GRIM and related checks; a literature simulator |
| `work` | 51–57 | Fitts and KLM predictors; a vigilance operator; selection utility; a review scheduler; a megastudy; a line-up; stepped care |
| `efficient` | 58 | whitening; sparse coding; predictive coding; rate–distortion |

### 2.2 The Homunculus

`homunculus_map` is the series map. Part 1 draws the explanation that explains nothing: a little person in the
head watching a screen and pulling levers. Each part redraws one of its powers as mechanism (its eye becomes Part
13's filter bank, its notebook Part 20's memory search, its hand on the lever Part 25's accumulator), following
Dennett's rule that a homunculus is discharged when it is replaced by simpler ones that can be built. The map
appears on every part's opening and closing card. Part 62 shows what is still drawn as a person.

### 2.3 The Pool

`explainer.psychology.pool` is a seeded population of 100,000 simulated people. Each is a Psyche with its own
parameters, drawn from a generative model that is itself part of the syllabus:

- additive genetic and environmental components, in families with twins, siblings and adoptees (Part 9);
- ages from birth to ninety, with growth and decline in parameters, and cohort effects (Parts 30, 31);
- a hierarchical ability structure and five traits (Parts 32, 33);
- membership of groups and a social network (Parts 34–38);
- liabilities to disorder with comorbidity, and a response to treatment that differs between people (Parts 39–42);
- for methods parts, the things a real pool has: careless responders, dropouts, practice effects, demand effects.

What it is for: grading methods against a known truth. A twin study recovers the heritability that was set, or
does not when its assumptions are broken. A thousand laboratories study a true effect of d = 0.2 with n = 20 per
cell, and the published literature that results is drawn. An adaptive test is scored against the abilities it was
built to find. **It is never evidence about people,** and every frame that shows it is labelled `simulated`.

### 2.4 The Battery, and "On you"

Twelve tasks and one questionnaire, implemented once (`explainer.psychology.battery` for the films and Psyche,
`videos/psychology/course/site/widgets/` for the browser) and used throughout.

| # | Task | First used | Signature a model must reproduce |
|---|---|---|---|
| 1 | Simple and choice reaction time | 1 | the right-skewed RT distribution; Hick's logarithm |
| 2 | Two-alternative threshold (contrast or length) | 11 | a psychometric function; Weber's fraction |
| 3 | Stroop colour naming | 18 | interference larger than facilitation; the delta plot |
| 4 | Visual search | 18 | flat and sloped set-size functions; target-absent slopes about twice target-present |
| 5 | Change detection | 19 | capacity near three to four items; precision falling with load |
| 6 | Free recall of a word list | 20 | primacy, recency, contiguity |
| 7 | Random-dot motion | 25 | accuracy and RT against coherence; fast and slow errors |
| 8 | Two-armed bandit and the two-step task | 17 | win-stay lose-shift; model-based and model-free signatures |
| 9 | Risky and delayed choices | 26 | the fourfold pattern; framing; hyperbolic discounting |
| 10 | Mental rotation | 24 | RT linear in angle |
| 11 | Lexical decision and self-paced reading | 23 | frequency and surprisal effects |
| 12 | Matrix reasoning (generated items) | 32 | item difficulty ordered by rule count |
| Q | A 50-item public-domain Big Five inventory (IPIP) | 33 | five factors |

Each task has a human benchmark from open data (named in the part), Psyche's result, and the viewer's. In the
films, On-you segments use a framed stage, a countdown and a pause. On the course site, each part's interactive
(`course/site/widgets/*.js`) is an experiment that runs in the browser with honest timing caveats, draws the
reader's data against the benchmark and the model, and **stores nothing and sends nothing**. `tools/check_course.py`
already drives every interactive; for this series it also plays each task with a scripted participant.

### 2.5 The Replication Ledger

`explainer.psychology.ledger` holds one record per finding: the claim; the original study (authors, year, N,
design, effect size); the replication record (direct replications, multi-site projects, meta-analyses with and
without bias correction); a status; sources; the date checked. Statuses:

| Status | Meaning |
|---|---|
| `replicated` | direct replications find it at a similar size |
| `replicated, smaller` | it is there, at a fraction of the original size |
| `contested` | replications or meta-analyses disagree, and the disagreement is described |
| `failed` | large preregistered replications find nothing |
| `not directly tested` | the classic has never been directly replicated (often it could not be, ethically) |
| `retracted` | withdrawn for error or fraud |
| `story and record` | the finding stands, but the textbook account of the study is wrong |

On screen a Ledger row is a card (`ledger_card`): hollow marker for the original estimate, filled markers for
replications, on one effect-size axis. The whole Ledger (`ledger_board`) is shown at the end of each act. It is
audited in Part 50 with the tools taught there, and shown complete in Part 62. Planned rows are listed under each
part below; the frontier sweep fixes each status before it goes on screen.

### 2.6 The degree and the practice

| Tier | Parts | Comparable courses |
|---|---|---|
| Introductory | the opening chapters of 1–42 | Psych 101 (the scope of MIT 9.00, Yale PSYC 110, and the AP and IB syllabuses) |
| The major | 1–43 | research methods and statistics; biological psychology; sensation and perception; learning; cognition; developmental; personality; social; abnormal; a capstone project |
| Graduate | the model chapters of every part; 44–50 | quantitative methods sequences (SEM, IRT, multilevel models, meta-analysis); mathematical psychology; computational cognitive modelling; neuroimaging methods |
| Research | the Frontier chapters; 58–62 | topics seminars and reading groups; the dissertation |
| Practice | the In practice chapters; 51–57 | human factors; HCI; I/O psychology; educational psychology; behavioural science; forensic and health psychology |

| Role | Parts that serve it |
|---|---|
| UX researcher, quantitative UXR | 2–4, 11–12, 18, 25, 46, 51, 52 |
| Behavioural scientist (policy, product, marketing) | 2–4, 26, 28, 34–36, 46, 50, 55 |
| Psychometrician, assessment scientist | 3, 32, 33, 44–46, 53 |
| People analytics, I/O consultant | 3, 32, 33, 44, 46, 47, 53 |
| Learning scientist, edtech | 16, 20, 21, 45, 54 |
| Human factors engineer | 11–15, 18, 25, 51, 52 |
| Clinical scientist and practitioner (alongside licensed training, which this is not) | 16, 39–42, 47, 57, 59 |
| Cognitive and computational neuroscientist | 5–8, 13–17, 25, 48, 49, 58 |
| Data scientist working with human data | 2–4, 44–50 |
| AI researcher (evaluation, alignment, human–AI interaction) | 17, 22–27, 35, 45, 48, 60 |

## 3. Visual instruments

The base is `explainer/ai/viz.py` and `explainer/ai/lecture.py`: continuity over cuts, in-place derivations,
colour as meaning, a narrating camera, live quantities. New instruments, in `explainer/psychology/viz.py`:

| Instrument | What it shows |
|---|---|
| `TrialStrip` | one trial as a film strip (fixation, stimulus, response window, feedback) with its timing; the standard opening of every study card |
| `DemoStage` | the On-you frame: border, countdown, stimulus, response prompt, then the reveal against published data |
| `StudyCard` / `LedgerCard` / `LedgerBoard` | design, N, effect with interval; original (hollow) and replications (filled) on one axis; the whole Ledger |
| `HomunculusMap` | the series map: the little person, part by part replaced by mechanism |
| `LevelsStrip` | the scale ladder (molecule to culture) and Marr's level, lit per chapter |
| `PoolCloud` | the Pool as a field of dots; a sample drawn; a thousand laboratories as a grid of small studies |
| `EffectPicture` | two distributions sliding apart as d changes, with overlap and the common-language probability live |
| `SpikeScope` | membrane voltage with the m, h and n gates beneath it; rasters; the phase plane with nullclines |
| `BrainTour` | a 3D brain the camera flies through; regions light, lesions darken, tracts draw |
| `BoldTrace` | neural events convolved into a BOLD curve; a design matrix assembling column by column |
| `PsychometricCurve` | responses accumulating as dots, the fitted sigmoid, threshold and slope as live trackers; a staircase homing in |
| `SDTView` | two distributions and a sliding criterion, the four outcome areas, and the ROC point tracing its curve |
| `ReceptiveField` | a stimulus over a patch of retina, the filter, the response; a bank of Gabors tiling space and frequency |
| `BayesBars` | prior, likelihood and posterior, with cue weights that follow reliability |
| `AssocNet` | cues and outcomes with weights as bars; the prediction error as a red pulse that shrinks with learning |
| `ValueWorld` | a gridworld or state chain with values as heat and the dopamine trace under it |
| `SearchDisplay` | search arrays with a saliency or priority map and a moving spotlight |
| `MemoryTheatre` | items as cards entering a store; a drifting context vector; recall transitions drawing the contiguity curve |
| `Landscape` | an energy landscape with a settling ball: Hopfield memories, ring attractors, bistable percepts, symptom networks with hysteresis |
| `ConceptSpace` | stimuli in a psychological space; generalization gradients; MDS unfolding a distance table |
| `ReadingTrace` | a sentence read word by word with surprisal bars and a gaze trace |
| `DiffusionRace` | evidence paths to two bounds with the RT histograms growing on the bounds |
| `ValueCurve` | the value and weighting functions, and the probability triangle with indifference curves |
| `GrowthFan` | individual trajectories over age; cross-sectional and longitudinal slices of the same fan |
| `PathDiagram` | latent circles and observed squares; a correlation matrix morphing into the diagram that implies it |
| `ItemCurves` | item characteristic and information curves; an adaptive test narrowing its interval |
| `SocialNet` | agents on a network: cascades, opinion flows, a Schelling grid |
| `SymptomNet` | symptoms as nodes with weighted edges, activation spreading |
| `ForestFunnel` | a forest plot stacking study by study; the same studies falling into a funnel with its missing corner |
| `MultiverseGrid` | every defensible analysis as a cell, coloured by its result |

**Colour is meaning.** Human data white; Psyche orange; the Pool grey-blue. Stimulus white, response blue. Signal
teal, noise grey. Prediction purple, prediction error red, reward gold. Excitation warm, inhibition cool. Prior
purple, likelihood green, posterior orange (as *Statistics, Built*). Original study hollow, replication filled.
Treated coral, control sky blue.

**Stimuli.** All stimuli are generated in code (gratings, dot fields, search arrays, word lists from public-domain
norms, schematic faces). No photographs of people. The brain mesh for `BrainTour` needs a licence check (the
candidates and the fallback, a drawn schematic, are in §8).

## 4. Part by part

Lengths are targets; the content decides. Each part lists its **question** and **story**, then its content
chapters. Every part also has, after the numbered chapters and not listed again each time: the **Ledger** chapter,
the **In practice** chapter, the **Frontier** chapter, and the outro (recap, problems, payoff cards, the
Homunculus redrawn). The italic lines give their content. *Psyche:* is what the part builds and computes; *On
you:* is the demonstration.

---

## Act I · Asking a Mind a Question

### Part 1 · Kant's Wager (~46)
*Question:* can a mind be measured?
*Story:* Kant gives three reasons why psychology can never be a science. Helmholtz, Donders, Fechner and Ebbinghaus
answer the first by timing and scaling the mind. A century of schools argues over what the measurements are of. The
series takes the modern answer: explain a capacity by building something that has it.
0. Hook: Kant, 1786. Three objections on screen. The series will keep score against them.
1. On you: simple reaction time, then a choice. Your two numbers differ. Why?
2. Helmholtz times the nerve impulse (1850): the apparatus, the arithmetic, 25 to 43 metres a second in the frog
   from his own distances and delays. Thought takes time, so it can be measured.
3. Donders' subtraction method (1868): simple, go/no-go and choice reaction times; stages as additive durations.
   Psyche's first module runs his three tasks.
4. What subtraction assumes: pure insertion. Two worlds with the same three means; the variances tell them apart.
   Sternberg's additive-factors repair (1969).
5. Fechner's morning (1850) and the *Elements* (1860): measuring sensation in just-noticeable steps (paid off in
   Part 11).
6. Wundt's laboratory (1879), Ebbinghaus (1885, his own savings table), James's *Principles* (1890): what an
   experiment on the mind looked like, and why introspection stalled (the imageless-thought dispute).
7. Behaviourism: Watson 1913, Skinner. What banning the mind bought, and what it could not explain (Lashley on
   serial order, 1951; Tolman's maps).
8. The cognitive revolution: 1956 (Miller, Newell and Simon, Chomsky), the computer as a licence to talk about
   inner states; Hick's law as a stage model's prediction.
9. Marr's three levels (1982) with one worked example, the cash register, then reaction time itself.
10. The Homunculus: why "a part of you decides" explains nothing, and the rule for discharging it. The map of
    twenty faculties.
11. The devices: Psyche, the Pool, the Battery, the Archive, and the map of the series.
12. The Ledger opens: the anatomy of a row, the seven verdicts, the first five rows.
13. In practice: reaction time on the road, on a screen, in the clinic, on the track.
14. Frontier: what is a reaction time measuring? Stages against cascades; the group mean that describes no one;
    whether the Victorians were faster; what a browser's clock can be trusted with.

*Psyche:* `chronometry`: a serial-stage simulator; Donders' three tasks reproduced; a rival with the same means
and different variances; additive factors shown as parallel lines; Hick's law; the ex-Gaussian fit.
*On you:* simple and choice reaction time; the published norm revealed (Woods et al. 2015, 1,469 adults).
*Ledger:* nerve conduction speed (replicated); the ordering of Donders' three tasks (replicated); his differences
as pure stages (contested); Hick's law, a preview (replicated); "the Victorians were faster" (contested).
*In practice:* reaction time is still the workhorse measure of UX latency budgets, road design, sports timing and
cognitive screening.
*Frontier:* is there a single "mental speed"? Stage models against cascade and accumulator models; what
millisecond timing can and cannot be trusted to in a browser.
*Reading:* Kant, *Metaphysical Foundations of Natural Science*, Preface; Boring, *A History of Experimental
Psychology*; Donders 1868/1969; Sternberg 1969; Marr 1982 ch. 1; Miller 2003; Danziger 1990; Dennett 1978;
Roelofs 2018.

### Part 2 · The Experiment (~56)
*Question:* how do you ask a mind a question without telling it the answer?
*Story:* a horse does arithmetic and a commission of experts finds no trick. One young psychologist varies who
knows the answer, and the ability vanishes. Every design rule in psychology is in that story: the comparison, the
control, the blind, and randomization, which psychologists used first.
0. Hook: Clever Hans in Berlin, 1904. The commission of thirteen and its report of 12 September.
1. Pfungst's experiments: the questioner knows or does not (98% against 8%); blinders (89% against 6%); the cue,
   a movement of the head; the questioner moved away, with the cue-reading model; Pfungst plays the horse, and 23
   of 25 people give him the signal.
2. On you: Chevreul's pendulum (ideomotor action); be a coin, and why a program can guess you.
3. Compared with what? Variables, operational definitions, and why one group is never enough: a useless game
   "works" in a group tested twice, and a control group shows why.
4. Six ways to fool yourself: testing, history, maturation, regression, selection, attrition, each run on the Pool
   with the truth zero. Regression to the mean, drawn. The confound. The randomized experiment, 500 times.
5. Shuffling the cards: Peirce and Jastrow's deck (1884), the first randomized experiment; what a shuffle balances,
   measured or not, and by how much (computed); the randomization test.
6. Between and within designs: what pairing buys (computed), carry-over, counterbalancing, Latin and Williams
   squares.
7. Expectancy and demand: Rosenthal and Fode's rats, Pygmalion and its record, detection dogs (Lit et al. 2011),
   Orne's demand characteristics measured (de Quidt et al. 2018), the placebo, single, double and triple blinds.
8. Factorial designs and interactions, drawn. Why "it depends" is a finding. Scale dependence of interactions
   (computed).
9. Validity, four kinds (Shadish, Cook and Campbell). The WEIRD sample problem as external validity (paid off in
   Part 38). Quasi-experiments for when randomization is impossible (link to *Statistics, Built* Parts 35–37).
10. Ethics as design: deception, Milgram, Tuskegee, the Belmont Report (1979), consent and debriefing, the ethics
    board; the rules for this series' own experiments.
11. The experiment runner: a design is a small program; the Pool runs it. Hans as four numbers.
12. The Ledger.
13. In practice: A/B tests, clinical trials, user studies; five questions for any study.
14. Frontier: blinds that cannot be kept (Mitchell et al. 2021), the balanced placebo design and its price,
    demand measured directly, who gets studied.

*Psyche:* `cueing` (Clever Hans as a cue reader, fitted to Pfungst's counts); the Pool's sessions; and
`explainer.psychology.lab`: assignment, counterbalancing, the comparison and its test, power, and each threat to
validity simulated with the truth known.
*On you:* an ideomotor demonstration (a pendulum that answers your own thought); try to be random, against a
program that guesses your next key press.
*Ledger:* an animal reads its handler (`replicated`); the "bright" rats (`not directly tested`); teacher
expectancy and IQ (`replicated, smaller`); demand effects (`replicated`); people cannot be random (`replicated`).
The Hawthorne effect is left to Part 53.
*In practice:* A/B tests, clinical trials and user studies are these designs; "who is blind?" is the first question
to ask of any of them.
*Frontier:* demand effects measured directly (de Quidt, Haushofer & Roth 2018); when a blind cannot be kept
(psychotherapy, psychedelics), and what designs do about it; whether findings hold beyond the samples studied.
*Reading:* Pfungst 1907/1911; Peirce & Jastrow 1884; Shadish, Cook & Campbell 2002; Rosenthal 1966; Orne 1962;
Campbell & Stanley 1963; the Belmont Report.

### Part 3 · The Measure (~50)
*Question:* what does a number attached to a mind mean?
*Story:* in 1940 a committee of physicists and psychologists reports that it cannot agree whether sensation can be
measured at all. Stevens answers by asking what operations a number survives. Spearman has already asked the other
question, how much of a score is error. The two answers, scale type and reliability, plus the hardest question,
validity, decide what every later number in the series is worth.
1. Hook: the Ferguson Committee's final report, 1940. Campbell's objection: no addition, no measurement.
2. Stevens's four scales (1946) as groups of permissible transformations; what statistics survive each. The
   century-long quarrel over Likert means, and when it matters (computed).
3. Representational measurement: from an ordering to a scale; conjoint measurement in one picture (paid off in
   Part 46).
4. On you: the Forer reading. Everyone gets the same paragraph. Forer's class rated it 4.26 out of 5 (1949).
5. True score and error: X = T + E. Reliability as a variance ratio, derived.
6. Spearman 1904: attenuation. The correlation between two noisy measures, and the correction (derived; checked
   on the Pool).
7. Longer tests are better tests: Spearman–Brown derived; Cronbach's α derived, what it assumes and what it is
   not (unidimensionality); test–retest, parallel forms, inter-rater agreement and kappa.
8. Validity: content, criterion, construct. Cronbach and Meehl's nomological network (1955); the
   multitrait–multimethod matrix (Campbell and Fiske 1959), drawn and computed.
9. Jingle and jangle: one name for two things, two names for one. Grit and conscientiousness as the example.
10. Constructs as latent variables, and the alternative (a network of causes): a preview of Parts 32, 39 and 44.
11. Measuring in milliseconds and in self-report: what introspection can deliver (Nisbett and Wilson 1977; choice
    blindness, Johansson et al. 2005).
12. The reliability paradox, first statement: the tasks that give the most robust effects make the worst tests of
    individuals (paid off in Parts 47 and 59).

*Psyche:* a classical-test-theory simulator on the Pool: reliability against test length, attenuation and its
correction, α under violated assumptions, an MTMM matrix with planted method variance.
*On you:* the Forer effect.
*Ledger:* the Barnum/Forer effect (`replicated`); telling more than we can know (`replicated`, with limits);
choice blindness (`replicated`).
*In practice:* every hiring test, survey scale, clinical questionnaire and product metric is a measurement with a
reliability and a validity argument, or without one.
*Frontier:* is psychological measurement quantitative at all (Michell)? Generalizability theory; measurement
schmeasurement (Flake & Fried 2020): how often scales are altered and unvalidated.
*Reading:* Stevens 1946; Spearman 1904a; Lord & Novick 1968; Cronbach 1951; Cronbach & Meehl 1955; Campbell &
Fiske 1959; Michell 1999; Borsboom 2005; Flake & Fried 2020.

### Part 4 · The Evidence (~55)
*Question:* when should a finding be believed?
*Story:* in 2011 a leading journal publishes nine experiments showing that people can feel the future. The methods
are the field's standard methods. Either precognition is real or the standard methods can prove anything. Within
four years the field has shown which, by rerunning a hundred of its own studies, and has begun to rebuild its
rules. The Ledger opens here.
1. Hook: Bem, "Feeling the Future" (2011). The reactions: the methods are ordinary.
2. Effect sizes and their pictures: d, r, odds ratios; what d = 0.2, 0.5 and 0.8 look like; why "significant"
   says so little.
3. The p-value, exactly, and the six things it is not (link to *Statistics, Built* Part 10).
4. Power: Cohen's 1962 survey of a year of a journal, and how little changed in fifty years. What an underpowered
   literature looks like (computed on the Pool).
5. On you: forking paths. One null dataset, four innocent choices; make it significant. Simmons, Nelson and
   Simonsohn's 61% (2011), recomputed.
6. Publication bias: the file drawer, the funnel plot's missing corner, the winner's curse. A literature of a
   thousand laboratories on a true d = 0 and on a true d = 0.2 (computed).
7. HARKing, optional stopping and the garden of forking paths; why honesty is not enough.
8. Meehl's warning (1967, 1978): in soft psychology everything correlates with everything, so rejecting a null is
   a weak test of a theory.
9. Fraud is the smaller problem: Stapel (2011) and what distinguished fabrication from flexibility.
10. The Reproducibility Project (2015): one hundred studies; 97% of originals significant, 36% of replications;
    effects about half the size. What it showed and what it did not (the 2016 exchange).
11. The repairs: preregistration, registered reports, multi-site replications (Many Labs), open data, larger
    samples, and Bayes factors and equivalence tests for claiming an absence.
12. What survived. The Ledger's first board: robust classics beside fallen ones, and the pattern in which is which.

*Psyche:* the false-positive lab: a literature simulator on the Pool with knobs for sample size, flexibility and
publication filter; p-curves and funnel plots drawn from it (reusing `statkit.multiple`'s p-hacking simulator).
*On you:* the forking-paths exercise; "will it replicate?" on six one-line findings.
*Ledger:* Bem's precognition (`failed`); the Ledger's schema and its first twenty rows from the Reproducibility
Project and Many Labs.
*In practice:* the same arithmetic governs product experiments, biomarker claims and any dashboard with many
metrics.
*Frontier:* have the reforms worked? Registered reports' rate of null results; replication rates since 2015;
prediction markets for replicability; the claim that some subfields were hit and others spared.
*Reading:* Bem 2011; Simmons, Nelson & Simonsohn 2011; Cohen 1962, 1994; Meehl 1967, 1978; Open Science
Collaboration 2015; Klein et al. 2014, 2018; Nosek et al. 2018; Chambers 2017; Ritchie 2020.

---

## Act II · The Wet Machine

### Part 5 · The Neuron (~55)
*Question:* what is the mind's smallest moving part, and what does it compute?
*Story:* Helmholtz showed the nerve signal is slow. A century later Hodgkin and Huxley, with a squid axon and a
hand calculator, wrote four equations that reproduce it to the millisecond. It is psychology's best model of
anything, and the template for every model in the series: measure, write equations, simulate, compare.
1. Hook: Galvani's frog, Helmholtz's timing, and the question of what moves.
2. Cajal against Golgi: the neuron doctrine. Anatomy of a neuron, drawn.
3. Ions and the membrane: diffusion against electrical force. The Nernst potential derived; Goldman's equation.
4. The membrane as a circuit: capacitance, leak, the time constant (derived; the RC curve on screen).
5. The squid giant axon and the voltage clamp (Cole; Hodgkin and Huxley 1939–52). What they measured.
6. The model: sodium and potassium conductances, the gates m, h and n, their rates fitted to clamp data. Four
   equations.
7. The action potential, computed: threshold, all-or-none, the refractory period, each traced to a gate.
8. Propagation: the cable equation, the length constant, myelin and saltatory conduction. Helmholtz's speed
   recovered.
9. Reduction: the phase plane, nullclines, FitzHugh–Nagumo; two ways to start firing (Hodgkin's classes as
   bifurcations).
10. Integrate-and-fire: what is kept and lost. The f–I curve.
11. Codes: rate, timing, Poisson variability, the Fano factor; Adrian's stretch receptor (1926).
12. What one neuron can compute: thresholds, coincidence detection, dendrites as a two-layer network.

*Psyche:* `neuron`: Hodgkin–Huxley integrated and checked against the 1952 figures; the cable; FHN; LIF with its
closed-form f–I curve; a spike-train generator.
*On you:* spikes as sound: hear a rate code, then guess the stimulus.
*Ledger:* the Hodgkin–Huxley model (`replicated`; the standard of quantitative success).
*In practice:* cochlear implants, deep-brain stimulators and anaesthetics act on these mechanisms; neuromorphic
chips implement the reductions.
*Frontier:* dendritic computation in human cortical neurons (Gidon et al. 2020 **(verify)**); how many parameters
a single-neuron model needs; glia.
*Reading:* Hodgkin & Huxley 1952; Kandel et al. chs. on membrane and action potential; Dayan & Abbott chs. 5–6;
Izhikevich, *Dynamical Systems in Neuroscience*; Koch, *Biophysics of Computation*; Finger, *Minds Behind the
Brain*.

### Part 6 · Synapses and Circuits (~50)
*Question:* how do neurons talk, and how does talking change them?
*Story:* on Easter Saturday 1921 Otto Loewi wakes from a dream with an experiment: two frog hearts and a shared
bath. The synapse is chemical. That makes it adjustable, and Hebb guesses the rule. Small circuits built from
adjustable synapses already sharpen edges, hold a decision and keep a rhythm.
1. Hook: Loewi's dream and the two hearts. Soup against sparks (Eccles and Dale).
2. The chemical synapse step by step: vesicles, quanta (Katz), receptors, reuptake. Ionotropic and metabotropic.
3. The transmitters and where the drugs act: glutamate, GABA, dopamine, serotonin, noradrenaline, acetylcholine,
   opioids. Agonists and antagonists on one diagram (used again in Parts 10 and 40–42).
4. Synaptic integration: EPSPs and IPSPs summing in time and space (computed on Part 5's neuron); shunting
   inhibition as division.
5. Hebb's postulate (1949) and its instability; Oja's rule finds a principal component (derived, computed).
6. LTP found (Bliss and Lømo 1973); the NMDA receptor as a coincidence detector; spike-timing-dependent
   plasticity (Bi and Poo 1998).
7. Lateral inhibition: Hartline's horseshoe crab; Mach bands computed; the Hermann grid.
8. Recurrent excitation and inhibition: winner-take-all, a circuit that holds a choice (returns in Parts 19, 25).
9. Rhythm: half-centre oscillators and central pattern generators; the lamprey's swim.
10. Populations: Wilson–Cowan equations, the excitation–inhibition balance, oscillations and what the EEG's
    rhythms are (paid off in Part 8).
11. Neuromodulators as gain and learning-rate knobs (a preview of Part 17's dopamine).

*Psyche:* `circuits`: conductance synapses; Hebb, Oja, BCM and STDP rules with their fixed points; a lateral-
inhibition sheet; a winner-take-all pair; a half-centre oscillator; Wilson–Cowan.
*On you:* Mach bands and the Hermann grid, predicted by the model before you look.
*Ledger:* LTP as a memory mechanism (`replicated`, with the causal link argued in Part 20); the Hermann grid's
textbook explanation (`story and record`: the curved-grid variant breaks the receptive-field account).
*In practice:* psychopharmacology; why SSRIs, benzodiazepines, stimulants and antipsychotics do what they do at
the synapse.
*Frontier:* the engram (optogenetic tagging and reactivation of memories in mice); whether STDP is the rule in
vivo; backpropagation and the brain (taken up in Part 58).
*Reading:* Loewi 1921; Hebb 1949; Bliss & Lømo 1973; Bi & Poo 1998; Hartline & Ratliff 1957; Dayan & Abbott chs.
7–8; Marder & Bucher 2001; Valenstein, *The War of the Soups and the Sparks*.

### Part 7 · The Brain (~55)
*Question:* is the mind in one place or everywhere?
*Story:* an iron bar passes through Phineas Gage's skull in 1848 and he walks to the doctor. A patient who can
say only "tan" gives Broca a place for speech. A surgeon removes Henry Molaison's hippocampi and memory formation
stops while everything else stays. Damage is psychology's oldest experiment, and its logic, the double
dissociation, is how a box-and-arrow model gets tested.
1. Hook: Gage. What the record supports and what a century of retelling added.
2. A tour in 3D: brainstem, cerebellum, thalamus, basal ganglia, limbic structures, the four lobes, white matter.
   What each is for, in one line each, with the caveat that the line is too simple.
3. Phrenology: Gall's good idea (localization) and bad method. Flourens's pigeons. Lashley's search for the
   engram and "mass action".
4. Broca (1861) and Wernicke (1874): two aphasias and the first circuit diagram of a function.
5. The logic of dissociation: single, double, and what each licenses (drawn as crossed lesion diagrams; simulated
   in a lesionable architecture, where a single-system model can fake a dissociation).
6. Maps: Penfield's homunculus, retinotopy, tonotopy. Cortical magnification computed.
7. H.M. (1953): what was removed, what was lost, what was spared (mirror tracing). Memory is not one thing.
8. The split brain (Sperry and Gazzaniga): what each hemisphere can report; the interpreter. The left-brain,
   right-brain myth against the lateralization data.
9. Neglect, agnosia, prosopagnosia, blindsight (returns in Parts 14, 27): the catalogue of things that can break
   alone.
10. Plasticity: remapping after amputation, critical periods (Hubel and Wiesel), London taxi drivers, recovery
    after stroke.
11. Localization against distribution today: networks, hubs, degeneracy. The 10% myth, with the metabolic
    arithmetic.

*Psyche:* `brain`: a box-and-arrow architecture whose parts can be lesioned, run on Battery tasks; dissociation
logic tested against single- and multi-system models; a magnification-factor fit.
*On you:* find your blind spot and measure its size; a pointing demonstration of filling-in.
*Ledger:* Gage's personality change (`story and record`); Broca's area and speech (`replicated, refined`: the
lesions were larger than the area); the taxi-driver hippocampus (`replicated`); left-brain and right-brain
"types" (`failed`).
*In practice:* clinical neuropsychology: the assessment after stroke, injury and in dementia is dissociation logic
applied to one person.
*Frontier:* lesion–symptom mapping with thousands of patients; the cerebellum's role in cognition; whether
cortical "areas" are the right unit.
*Reading:* Macmillan, *An Odd Kind of Fame*; Scoville & Milner 1957; Corkin, *Permanent Present Tense*; Gazzaniga
2005; Shallice, *From Neuropsychology to Mental Structure*; Kandel et al.; Dronkers et al. 2007.

### Part 8 · Reading the Brain (~55)
*Question:* what can a brain scan tell you about a mind?
*Story:* in 2009 a team puts a dead Atlantic salmon in an MRI scanner, shows it photographs of people, and finds
"activity". The fish is a statistics lesson. This part builds the measurement chain from a neuron to a coloured
blob, so that each link's assumptions are visible, and then lists what the blobs have and have not delivered.
1. Hook: the salmon (Bennett et al. 2009). An uncorrected threshold across 130,000 voxels.
2. Recording from neurons: single units, Hubel and Wiesel's method, what a tuning curve is.
3. EEG: Berger's recordings (1920s); why scalp potentials are summed postsynaptic currents from aligned pyramidal
   cells; volume conduction; the inverse problem has no unique solution (drawn).
4. Event-related potentials: averaging pulls a signal out of noise at a rate of root n (computed); the P300, the
   N400 (Kutas and Hillyard 1980), mismatch negativity.
5. MRI in five minutes: spins, relaxation, gradients, k-space as a Fourier transform (link to *Analysis, Built*).
6. BOLD: neurovascular coupling, the haemodynamic response, and the linear model: a response is the events
   convolved with a kernel (derived, computed).
7. The general linear model of an experiment: design matrix, contrasts, a t-map. Subtraction logic returns from
   Part 1 with its pure-insertion problem.
8. A hundred thousand tests: family-wise error, random fields, false discovery rate, cluster inference, and the
   2016 finding that common cluster settings gave far too many false positives.
9. Circular analysis: "voodoo correlations" (Vul et al. 2009). Selecting voxels by the correlation you then
   report (simulated on a synthetic brain: r = 0.8 from nothing).
10. Reverse inference (Poldrack 2006): from activation to mental state by Bayes' rule, with real base rates.
11. Causal tools: lesions, TMS, direct stimulation, optogenetics in animals. What "necessary" and "sufficient"
    mean here.
12. What imaging settled and what it did not: a short, honest list.

*Psyche:* `brain`: a forward model from simulated neural events to BOLD and to scalp EEG; a synthetic brain with
known active regions analysed with each threshold method; ERP averaging.
*On you:* three scatter plots from brain-imaging papers: which one is impossible given the measures'
reliabilities?
*Ledger:* the N400 (`replicated`); the fusiform face area (`replicated`, interpretation `contested`, in Part
14); brain-training transfer and "neuromarketing" claims (`failed` or `not directly tested`).
*In practice:* clinical EEG and presurgical mapping are established uses; lie detection and consumer "neuro"
products are not.
*Frontier:* brain-wide association studies need thousands of people (Marek et al. 2022); test–retest reliability
of task fMRI; decoding continuous language from fMRI (Tang et al. 2023 **(verify)**). Analysis methods at depth
are Part 49.
*Reading:* Bennett et al. 2009; Vul et al. 2009; Kriegeskorte et al. 2009; Poldrack 2006; Eklund, Nichols &
Knutsson 2016; Logothetis 2008; Luck 2014; Poldrack, Mumford & Nichols 2011; Huettel, Song & McCarthy.

### Part 9 · Genes and Evolution (~55)
*Question:* how much of who you are did you inherit, and what does that question mean?
*Story:* twins separated in infancy meet at thirty-nine and find the same habits. The anecdote is worth nothing;
the design behind it is one of psychology's most replicated. This part derives what a twin study estimates, shows
on the Pool when it is right and wrong, and follows the search for the genes themselves, including a decade of
findings that were not there.
1. Hook: the "Jim twins" and the Minnesota study (1979–). Anecdote against design.
2. Galton's "nature and nurture" (1869–75), and where his programme led: eugenics, named here and told in Part
   32.
3. Mendel to Fisher (1918): many small genes make a continuous trait; variance components.
4. Twin logic: identical and fraternal correlations; Falconer's formula derived; the ACE model as a path diagram
   (the first one in the series; returns in Part 44).
5. On the Pool: the design recovers the planted heritability, and then fails as the equal-environments assumption,
   assortative mating or gene–environment correlation are switched on (computed).
6. What heritability is not: not fixedness, not about an individual, not about group differences, not constant
   across environments (the height-in-two-fields picture; Turkheimer et al. 2003 on socioeconomic status).
7. The three laws of behaviour genetics (Turkheimer 2000) and the large twin meta-analysis (Polderman et al.
   2015). The puzzle of the shared environment.
8. Finding the genes: candidate-gene studies and their collapse (5-HTTLPR and depression; Border et al. 2019).
   Why: small effects, small samples, flexible analysis. Part 4 again.
9. GWAS: a million tests, the 5 × 10⁻⁸ line, Manhattan plots; polygenic scores, what they predict within and
   between families, and missing heritability.
10. Gene–environment interplay; epigenetics in two careful minutes.
11. Evolutionary psychology: adaptation as a hypothesis generator; the cheater-detection claim (Part 24), mate
    preferences (Part 37); the just-so-story critique and what a testable version looks like.
12. Comparative cognition in brief: what crows, apes and octopuses tell us about which solutions are forced.

*Psyche:* `genes`: additive genomes for the Pool; twin, adoption and sibling designs with ACE fits by maximum
likelihood; a GWAS on a simulated trait; polygenic prediction within and between families.
*On you:* guess the heritability of ten traits, then see the meta-analytic values.
*Ledger:* the heritability of psychological traits (`replicated`); 5-HTTLPR × stress (`failed`); candidate genes
for cognition generally (`failed`); educational-attainment polygenic scores (`replicated`; within-family effects
about half as large **(verify)**).
*In practice:* genetic counselling; direct-to-consumer "behavioural" genetics and embryo screening claims, with
the arithmetic of what a polygenic score can deliver.
*Frontier:* within-family GWAS and genetic nurture; ancestry and portability of scores; rare variants; what a
causal account from variant to behaviour would need.
*Reading:* Plomin et al., *Behavioral Genetics*; Falconer & Mackay; Turkheimer 2000; Polderman et al. 2015; Border
et al. 2019; Visscher et al. 2017; Harden, *The Genetic Lottery*; Kevles, *In the Name of Eugenics*.

### Part 10 · Chemistry and Clocks (~50)
*Question:* why does the same mind differ at four in the afternoon and four in the morning?
*Story:* in 1938 Nathaniel Kleitman and a student live for a month in Mammoth Cave on a twenty-eight-hour day to
see whether the body would follow. One of them adapts; the body's clock is real and stubborn. The mind sits in a
body with rhythms, hormones and drugs, and each of these is a control loop that can be written down.
1. Hook: the cave. Free-running rhythms; Aschoff's bunker; a period slightly longer than a day.
2. The clock: a molecular feedback loop as a limit-cycle oscillator; entrainment by light; phase-response curves;
   jet lag computed.
3. Sleep discovered in the laboratory: Aserinsky and Kleitman find REM (1953); the stages and the hypnogram.
4. The two-process model (Borbély 1982): a homeostatic pressure and a circadian threshold. The model, its
   predictions for deprivation and naps, and its fit.
5. What sleep is for: deprivation studies, memory consolidation (a preview of Part 21), synaptic homeostasis.
   What is solid and what was oversold.
6. Dreams: activation–synthesis against continuity theories; what can be measured.
7. Hormones as slow signals: the stress axis as a negative-feedback loop (Selye; the cortisol curve computed);
   allostasis. Stress and performance (the Yerkes–Dodson curve and its thin original basis, Part 28).
8. Sex hormones and behaviour: organizational and activational effects; what the human evidence supports.
9. Drugs: dose–response, receptor occupancy and the Hill equation; agonists, antagonists, half-lives.
10. Tolerance and withdrawal as opponent processes (Solomon and Corbit 1974; Siegel's conditioned tolerance).
    Returns in Part 41.
11. Caffeine, alcohol, nicotine, cannabis, in the same four numbers each.

*Psyche:* `body`: a van der Pol-style circadian oscillator with light input; the two-process model fitted to
published sleep-timing data; an HPA loop; occupancy and opponent-process tolerance.
*On you:* your chronotype from two questions, placed on the model's phase axis; predict your own afternoon dip.
*Ledger:* REM and the stages (`replicated`); sleep deprivation impairs vigilance (`replicated`); sleep and
declarative memory consolidation (`replicated, smaller` **(verify)**); specific popular claims about sleep loss and
mortality (`contested`).
*In practice:* shift scheduling, aviation duty limits, school start times, CBT for insomnia (Part 57).
*Frontier:* why we sleep is still open; the glymphatic hypothesis and its disputes; individual differences in
vulnerability to sleep loss.
*Reading:* Kleitman, *Sleep and Wakefulness*; Borbély 1982; Daan, Beersma & Borbély 1984; Sapolsky, *Why Zebras
Don't Get Ulcers*; Solomon & Corbit 1974; Siegel 1975; Julien, *A Primer of Drug Action*.

---

## Act III · Sensing

### Part 11 · The Threshold (~50)
*Question:* what is the smallest difference you can notice, and is there a law to it?
*Story:* Weber lifts weights and finds that the noticeable difference is a constant fraction. Fechner turns the
fraction into a scale of sensation, and the first quantitative law of the mind is a logarithm. A century later
Stevens asks people for numbers directly and gets a power law. The quarrel is about what a threshold is, and the
answer, a curve and not a point, sets up signal detection theory.
1. Hook and On you: two patches, which is brighter? A hundred trials in ninety seconds of screen time.
2. Weber (1834): ΔI = kI. Weber fractions for weight, brightness, loudness, line length.
3. Fechner's step: integrate the fraction. S = k log I derived, with its assumption that every JND is one equal
   unit.
4. The three classical methods (limits, adjustment, constant stimuli), each drawn as its trial strip.
5. The threshold is not a step: the psychometric function. Cumulative Gaussian, logistic and Weibull forms;
   threshold, slope, guess and lapse rates.
6. Fitting it: the binomial likelihood, maximum likelihood, bootstrap intervals (your data from chapter 1,
   fitted).
7. Efficient measurement: staircases and what they converge to (the 70.7% rule derived), and QUEST's Bayesian
   placement of the next trial (Watson and Pelli 1983).
8. Stevens's direct scaling (1957): magnitude estimation, the power law, exponents from 0.33 (brightness) to 3.5
   (electric shock); cross-modality matching as a check.
9. Fechner against Stevens: what each assumes; why both can describe their data.
10. Where Weber's law comes from: noise that grows with the signal, or a compressive code. A preview of Parts 12
    and 58.
11. Weber's law elsewhere: number sense (Part 30), time, prices (Part 26).

*Psyche:* `psychophysics`: the observer, the three methods, staircases and QUEST, ML fits with intervals; Weber
fractions recovered from simulated and open data.
*On you:* Battery task 2. Your psychometric function, fitted on the site.
*Ledger:* Weber's law (`replicated`, with the known failures at the extremes); Stevens's exponents
(`replicated`).
*In practice:* audiometry and optometry are psychophysics; display and codec engineering (JND-based compression,
the decibel) rest on it; "just noticeable" price and design changes.
*Frontier:* why near-miss to Weber's law; adaptive methods for many-parameter functions; what magnitude estimates
measure.
*Reading:* Fechner 1860; Stevens 1957, 1975; Gescheider, *Psychophysics*; Kingdom & Prins, *Psychophysics: A
Practical Introduction*; Wichmann & Hill 2001; Watson & Pelli 1983.

### Part 12 · Signal and Noise (~50)
*Question:* when you say "yes, I saw it", how much of that is seeing and how much is willingness to say yes?
*Story:* wartime radar operators miss targets and report ghosts, and it turns out no instruction can fix one
error without causing the other. Engineers and psychologists at Michigan turn that trade-off into a theory with
two numbers: how well you can tell, and where you draw the line. It is the most exported idea in psychology.
1. Hook: the radar screen. Hits, misses, false alarms, correct rejections.
2. Why the threshold idea fails: change the payoff or the base rate and the "threshold" moves (computed).
3. The model: two overlapping distributions and a criterion. d′ and c derived from hit and false-alarm rates.
4. The ROC curve: sweep the criterion; the area under it; rating-scale ROCs from confidence.
5. On you: an old/new judgment with confidence. Your ROC, drawn.
6. The ideal observer: the likelihood ratio is the best decision variable (Neyman–Pearson; link to *Statistics,
   Built* Part 10). The optimal criterion from payoffs and base rates.
7. Two-alternative forced choice: why it removes bias and why d′ gains a factor of root two (derived).
8. Unequal variances and curved zROCs: recognition memory's slope of about 0.8 (returns in Part 21).
9. Rival models: high-threshold and mixture models, and how ROC shape separates them.
10. Base rates: a rare target and a good detector still give mostly false alarms (the mammogram arithmetic;
    natural frequencies).
11. The prevalence effect: when targets are rare, observers miss more (Wolfe et al. 2005). Returns in Part 51.
12. The same picture everywhere: diagnosis, line-ups, spam filters, hiring. A table of what plays the role of
    signal, noise and criterion in each.

*Psyche:* `sdt`: equal- and unequal-variance observers for yes–no, rating and 2AFC; ROC fitting by maximum
likelihood; the ideal observer under payoffs.
*On you:* the confidence-rating recognition test; the mammogram problem.
*Ledger:* criterion shifts with payoffs and base rates (`replicated`); the prevalence effect (`replicated`);
subliminal perception claims that relied on thresholds without SDT (`contested`).
*In practice:* radiology, airport screening, quality inspection, alarm design, classifier evaluation (the ROC
entered machine learning from here).
*Frontier:* confidence and metacognition (meta-d′, Part 25); whether the decision variable is one-dimensional;
criterion setting as learning.
*Reading:* Tanner & Swets 1954; Green & Swets 1966; Macmillan & Creelman, *Detection Theory*; Swets, Dawes &
Monahan 2000; Wixted 2020; Gigerenzer & Hoffrage 1995.

### Part 13 · The Eye and the Code (~55)
*Question:* what does the eye tell the brain?
*Story:* in 1942 three researchers sit in a dark room and find that a flash delivering five to seven photons to
the retina can be seen: the eye is as sensitive as physics allows. But the eye does not send pictures. It sends
differences, across space, time and wavelength, and each stage can be written as a filter. Colour turns out to be
linear algebra.
1. Hook: Hecht, Shlaer and Pirenne (1942). Counting quanta; the Poisson argument from the frequency-of-seeing
   curve.
2. Optics: the eye's point spread function and why acuity stops near sixty cycles per degree; the cone mosaic.
3. Rods, cones and adaptation: nine orders of magnitude of light on a limited response range; gain control.
4. Ganglion cells: Kuffler's centre–surround (1953) as a difference of Gaussians; why code differences (a first
   look at redundancy, Part 58).
5. To cortex: Hubel and Wiesel's bar (1959); orientation tuning; simple and complex cells; the Gabor model.
6. Vision as Fourier analysis: gratings, the contrast sensitivity function (Campbell and Robson 1968), channels
   and adaptation; an image filtered by your own CSF.
7. Contrast normalization: responses divided by the neighbourhood (a canonical computation, Part 58).
8. Colour I: Newton's prism; Young and Helmholtz; three cone types. A light is a spectrum, a sensation is three
   numbers.
9. Colour matching as linear algebra: metamers are the null space; the 1931 standard observer; why three
   primaries suffice.
10. Colour II: Hering's opponent colours; Hurvich and Jameson's cancellation; cone-opponent cells. Colour
    deficiency as a lost dimension (about 8% of men).
11. Colour constancy and the dress (2015): one image, two assumed illuminants.
12. Two streams (Ungerleider and Mishkin; Milner and Goodale), and patient D.F.

*Psyche:* `vision`: a point-spread and sampling model; cone fundamentals and colour matching (metamers
constructed); difference-of-Gaussians and Gabor banks applied to images; a CSF fit; divisive normalization.
*On you:* the dress, then a metameric match; Mach bands return, now computed from the filter.
*Ledger:* single-photon sensitivity (`replicated`; rods respond to single photons, and people can report them
above chance, Tinsley et al. 2016 **(verify)**); the Hubel–Wiesel hierarchy (`replicated`, as a first
approximation); the dress's illuminant account (`replicated`).
*In practice:* every display, camera, image codec and colour standard is built on the standard observer and the
CSF; colour-blind-safe design.
*Frontier:* what V1 does with natural scenes (models explain a minority of the variance); the functions of the
many retinal ganglion cell types; tetrachromacy.
*Reading:* Hecht, Shlaer & Pirenne 1942; Kuffler 1953; Hubel & Wiesel 1959, 1962; Campbell & Robson 1968; Wandell,
*Foundations of Vision*; Rodieck, *The First Steps in Seeing*; Hubel, *Eye, Brain, and Vision*.

### Part 14 · Seeing as Inference (~55)
*Question:* why does a grey square look white, and how can a flat image yield a solid world?
*Story:* two squares on Adelson's checkerboard send identical light and look different. That is the visual system
working: the image underdetermines the world, so seeing must be a bet. Helmholtz called it unconscious inference.
The modern version says which bet is optimal, and people come remarkably close.
1. Hook and On you: the checker shadow. Measure it; the squares are the same.
2. The inverse problem: infinitely many scenes for one image (the Ames room, drawn from above).
3. Gestalt psychology: grouping laws, figure and ground, Kanizsa's triangle. Laws as descriptions waiting for an
   explanation.
4. Depth: binocular disparity (Wheatstone 1838; Julesz's random-dot stereograms), motion parallax, pictorial
   cues. The geometry derived.
5. Constancies of size, shape and lightness; the Müller-Lyer and Ponzo illusions as constancy misapplied (and
   the cross-cultural data, Part 38).
6. Bayes for perception: likelihood from the image, prior from the world, posterior as the percept (derived with
   Gaussians).
7. Cue combination: two noisy cues should be weighted by their reliabilities. Ernst and Banks (2002): vision and
   touch combined as predicted, with the predicted reduction in variance.
8. Priors made visible: light from above; the slow-motion prior explains the aperture problem and why low-contrast
   things seem slower (Weiss, Simoncelli and Adelson 2002).
9. Recognizing objects: Marr's stages; templates, features and parts; invariance as the hard problem.
10. Faces: inversion, the Thatcher illusion, prosopagnosia, the fusiform face area and the expertise dispute.
11. Deep networks as models of the ventral stream: what they predict (Yamins et al. 2014) and where they differ
    from people (texture bias, adversarial images). Continued in Part 60.
12. Perception and action (Gibson's affordances), and predictive coding in one picture (Part 58).

*Psyche:* `infer`: Gaussian cue combination with fitted weights; a lightness model that reproduces the checker
shadow; the motion prior; a small convolutional network with a behavioural readout compared on error patterns.
*On you:* six illusions, each predicted by the model before it is shown; a stereogram.
*Ledger:* optimal cue combination (`replicated`, with documented exceptions); the Müller-Lyer illusion
(`replicated`; size varies across societies); the FFA's selectivity (`replicated`; what it is selective for,
`contested`).
*In practice:* VR and stereo displays (cue conflicts and discomfort), camouflage, medical image reading, computer
vision evaluation against human error patterns.
*Frontier:* where the priors come from; what "Bayesian" commits a model to (Part 58); whether networks trained on
a child's visual input learn child-like recognition **(verify)**.
*Reading:* Helmholtz, *Treatise on Physiological Optics* vol. 3; Marr 1982; Knill & Richards (eds.) 1996; Ernst &
Banks 2002; Weiss, Simoncelli & Adelson 2002; Palmer, *Vision Science*; Kanwisher, McDermott & Chun 1997; Yamins
& DiCarlo 2016.

### Part 15 · The Other Senses (~55)
*Question:* how do pressure waves become a voice, and why does pain not follow the injury?
*Story:* Békésy opens the cochleas of cadavers and watches a wave travel along the membrane, peaking in a
different place for each pitch: the ear is a frequency analyser. Then the surprises begin. You hear a pitch that
is not in the sound, your eyes change what you hear, a rubber hand becomes yours, and pain turns out to be a
decision the nervous system makes.
1. Hook and On you: the missing fundamental. The pitch you hear is absent from the spectrum.
2. Sound: pressure, frequency, the decibel as Fechner's law in engineering (Part 11); the audiogram; equal-
   loudness contours.
3. The cochlea: Békésy's travelling wave (Nobel 1961), tonotopy, hair cells, the active amplifier; critical
   bands and masking.
4. Pitch: place against timing; the autocorrelation model explains the missing fundamental (computed).
5. Where is it? Interaural time and level differences (the duplex theory); Jeffress's coincidence detectors
   (1948), and what owls and mammals actually do.
6. Scene analysis: the cocktail party as grouping (Bregman); streaming demonstrations.
7. Speech: no invariant acoustic cue for a phoneme; categorical perception (Liberman et al. 1957); the McGurk
   effect (1976) as cue combination (Part 14's rule again).
8. Music: consonance and roughness, octave equivalence, expectation and surprise (links to *Philosophy, Built*
   Part 40).
9. Touch and the body: receptors, two-point thresholds and cortical magnification; proprioception; the rubber
   hand (Botvinick and Cohen 1998).
10. Pain: specificity against pattern; gate control (Melzack and Wall 1965) as a circuit; phantom limbs; placebo
    analgesia and its opioid mechanism (returns in Part 57).
11. Smell and taste: a combinatorial code; flavour is mostly smell; the tongue-map myth.
12. The vestibular sense, and how the senses are weighted when they disagree.

*Psyche:* `hearing`: a gammatone filter bank; autocorrelation pitch; a Jeffress array; a gate-control circuit;
audio-visual fusion by reliability weighting.
*On you:* the missing fundamental, streaming, the McGurk effect (with the warning that some viewers do not get
it, and the rates).
*Ledger:* the McGurk effect (`replicated`; large individual and cross-language variation); categorical perception
(`replicated, refined`); the rubber-hand illusion (`replicated`; demand effects `contested`); the tongue map
(`failed`; a mistranslation); gate control (`replicated` in outline, revised in detail).
*In practice:* hearing aids and cochlear implants, audio codecs (MP3 is a masking model), haptics, pain clinics.
*Frontier:* hidden hearing loss; predictive models of auditory cortex; chronic pain as learning.
*Reading:* von Békésy 1960; Moore, *An Introduction to the Psychology of Hearing*; Bregman, *Auditory Scene
Analysis*; Liberman et al. 1957, 1967; McGurk & MacDonald 1976; Melzack & Wall 1965; Wolfe et al., *Sensation &
Perception*.

---

## Act IV · Learning

### Part 16 · Conditioning (~55)
*Question:* what, exactly, is learned when a bell comes to mean food?
*Story:* Pavlov thought pairing was enough. In 1968–69 two experiments break that idea: Rescorla shows that
pairing without contingency teaches nothing, and Kamin shows that a perfectly paired cue is ignored if the
outcome was already predicted. Learning is driven by surprise. In 1972 Rescorla and Wagner write surprise as one
line of algebra, and the line still runs half of computational psychology.
1. Hook: Pavlov's laboratory (the bell is mostly legend; the method was not). Acquisition, extinction,
   spontaneous recovery, generalization.
2. Thorndike's puzzle box (1898) and the law of effect; Watson and "Little Albert" (1920), as run and as retold.
3. Skinner: the operant chamber, shaping, the cumulative record; schedules of reinforcement and their signatures
   (the scallop, the post-reinforcement pause), simulated.
4. On you: a two-minute contingency-learning game. Your ratings track ΔP.
5. Contiguity is not enough: Rescorla's truly random control (1968). Contingency as P(US|CS) − P(US|no CS).
6. Kamin's blocking (1969): the experiment, the result, the idea of surprise.
7. Rescorla–Wagner (1972): ΔV = αβ(λ − ΣV), derived as gradient descent on squared error (the delta rule; link to
   *AI, Built* Part 9). Acquisition, extinction, blocking, overshadowing, conditioned inhibition and
   overexpectation, each computed.
8. What the model gets wrong: latent inhibition, spontaneous recovery, renewal. Extinction is new learning
   (Bouton), not erasure. This is why fears return (Part 40).
9. Attention to cues: Mackintosh (1975) and Pearce–Hall (1980), and the hybrid.
10. Timing: the conditioned response is timed; rate-estimation theory as a rival to associations.
11. Choice: Herrnstein's matching law (1961) derived and simulated; melioration against maximizing.
12. Constraints: taste aversion in one trial across hours (Garcia and Koelling 1966); the misbehaviour of
    organisms (Breland and Breland 1961); preparedness; learning by watching (Bandura's Bobo doll, 1961).

*Psyche:* `conditioning`: Rescorla–Wagner, Mackintosh, Pearce–Hall, a context-dependent extinction model, an
operant chamber with the four basic schedules, matching; each run on the classic designs.
*On you:* the contingency game.
*Ledger:* blocking (`replicated`; smaller and less universal than textbooks say, Maes et al. 2016); taste
aversion (`replicated`); Little Albert (`story and record`: one infant, weak data, no deconditioning); the
matching law (`replicated`); renewal (`replicated`).
*In practice:* exposure therapy, animal training, token economies, contingency management for addiction; the
design of loot boxes and variable rewards (Part 52).
*Frontier:* is learning associative or propositional in humans? Latent-cause models of extinction; one-shot
learning.
*Reading:* Pavlov 1927; Rescorla 1968, 1988 ("It's not what you think it is"); Kamin 1969; Rescorla & Wagner
1972; Bouton, *Learning and Behavior*; Herrnstein 1961; Garcia & Koelling 1966; Gallistel & Gibbon 2000.

### Part 17 · Reward and Prediction (~55)
*Question:* how does a brain learn what to do when the reward comes later?
*Story:* a monkey gets juice and its dopamine neurons fire. After training they fire at the cue instead, and when
promised juice is withheld they fall silent at the moment it was due. In 1997 that recording is laid beside an
equation from computer science and they match. Then the cracks: rats that know a maze they were never rewarded
in, and people who plan.
1. Hook: Schultz's three recordings (unpredicted reward, predicted reward, omitted reward).
2. The problem Rescorla–Wagner cannot solve: credit over time. Second-order conditioning.
3. Temporal-difference learning: value as expected discounted future reward; the TD error δ = r + γV′ − V;
   derived from the Bellman equation (link to *AI, Built* Part 26, where the same algorithm plays games).
4. TD on Pavlov's task: the error moves from reward to cue, and dips at omission (computed). Schultz, Dayan and
   Montague (1997).
5. From prediction to action: actor–critic and the basal ganglia; Q-learning; the direct and indirect pathways as
   Go and NoGo; Parkinson's patients on and off medication (Frank et al. 2004).
6. On you: a two-armed bandit. Win-stay, lose-shift; your learning rate, fitted on the site.
7. Explore or exploit: softmax, uncertainty bonuses, Thompson sampling; what people do.
8. Tolman's rats (1930, 1948): latent learning and cognitive maps. Place cells (O'Keefe 1971) and grid cells
   (the Mosers, 2005).
9. Two controllers: model-free habits and model-based plans; devaluation experiments; the two-step task (Daw et
   al. 2011) and what its stay probabilities show.
10. Between the two: the successor representation; replay and planning in the hippocampus.
11. Is dopamine a prediction error? Ramps, movement signals, salience, and distributional codes (Dabney et al.
    2020).
12. When the signal is hijacked: a first model of addiction (Redish 2004), continued in Part 41.

*Psyche:* `rl`: TD(λ) with a simulated dopamine trace; actor–critic; Q-learning; a model-based planner; the
two-step task; the successor representation; bandit policies fitted to open data.
*On you:* Battery task 8.
*Ledger:* dopamine reward-prediction errors (`replicated`; scope `contested`); the two-step model-based signature
(`replicated`; interpretation `contested`); latent learning (`replicated`); grid cells (`replicated`).
*In practice:* recommender systems and bandit optimization are this mathematics; medication effects in
Parkinson's; behavioural addictions.
*Frontier:* what dopamine ramps mean; whether humans are ever purely model-free; meta-reinforcement learning in
prefrontal cortex (Part 58).
*Reading:* Schultz, Dayan & Montague 1997; Sutton & Barto, *Reinforcement Learning* (ch. 14–15 on psychology and
neuroscience); Tolman 1948; Daw et al. 2011; Niv 2009; Dabney et al. 2020; Dayan & Daw 2008.

---

## Act V · Thinking

### Part 18 · Attention (~55)
*Question:* why do you miss a gorilla, and what is the thing you were doing instead?
*Story:* half of viewers counting basketball passes fail to see a person in a gorilla suit walk through. Attention
was psychology's first reason to draw a box inside the head (Broadbent's filter, 1958). Sixty years of
experiments moved the filter, split it and finally replaced it with something a circuit can do: competition, and
a gain that multiplies.
1. Hook: Simons and Chabris (1999). Change blindness in a flicker display.
2. Cherry's cocktail party (1953) and dichotic listening; Broadbent's filter: the first information-flow diagram
   in psychology.
3. Your own name gets through (Moray): attenuation (Treisman) against late selection (Deutsch and Deutsch); load
   theory as the reconciliation (Lavie).
4. Attention in space without moving the eyes: Posner's cueing (1980). Benefits, costs, inhibition of return.
5. On you: visual search. A red target pops out; a conjunction does not.
6. Feature integration theory (Treisman and Gelade 1980): maps, a spotlight, illusory conjunctions. Guided search
   (Wolfe) and saliency maps (Itti and Koch) as its computational descendants.
7. Attention in time: the attentional blink; the psychological refractory period and the central bottleneck
   (computed with Part 1's stage model).
8. Control and conflict: the Stroop effect (1935), the flanker task, conflict monitoring; task switching and its
   cost.
9. What attention does to neurons: gain, biased competition (Desimone and Duncan 1995), and the normalization
   model (Reynolds and Heeger 2009), which reconciles the recordings (derived, computed).
10. Capacity as a race: Bundesen's theory of visual attention in outline.
11. Vigilance: Mackworth's clock (1948) and the decrement (returns in Part 51).
12. Multitasking: what the driving and media data show.

*Psyche:* `attention`: a saliency map on search displays; guided search reproducing flat and steep slopes; the
normalization model reproducing contrast-gain and response-gain effects; a Stroop conflict model.
*On you:* Battery tasks 3 and 4; the flicker paradigm.
*Ledger:* the Stroop effect (`replicated`; among the largest effects in psychology); inattentional blindness
(`replicated`); Posner cueing (`replicated`); the attentional blink (`replicated`); media multitasking harms
attention (`contested`).
*In practice:* interface and alarm design, distracted driving law, radiological search, attention metrics in
advertising.
*Frontier:* is attention one thing? Rhythmic sampling; attention in networks against attention in brains (the
shared word, Part 60).
*Reading:* Broadbent 1958; Treisman & Gelade 1980; Posner 1980; Stroop 1935; Desimone & Duncan 1995; Reynolds &
Heeger 2009; Wolfe 2021 (Guided Search 6.0); Carrasco 2011; Simons & Chabris 1999.

### Part 19 · Working Memory (~50)
*Question:* how much can you hold in mind at once, and what is the limit made of?
*Story:* George Miller is "persecuted by an integer". Seven turns out to be closer to four, then turns out not to
be an integer at all: is the limit a number of slots or a resource that is spread thinner? The argument is
settled, as far as it is, by fitting models to the errors people make. Then an industry promises to raise the
limit.
1. Hook and On you: digit span, live.
2. Miller's "magical number" (1956): span, chunks, recoding (the binary-to-octal trick, performed).
3. Sperling (1960): partial report shows a large, fast-fading sensory store.
4. Brown, and Peterson and Peterson (1959): forgetting in eighteen seconds. Decay or interference? (Keppel and
   Underwood 1962.)
5. The modal model (Atkinson and Shiffrin 1968) and its trouble; Baddeley and Hitch (1974): a phonological loop
   (word-length and similarity effects), a sketchpad, an executive. Dual-task logic.
6. Sternberg's memory scanning (1966): reaction time linear in set size, same slope for yes and no; serial
   exhaustive search, and the parallel models that mimic it.
7. Four, not seven: change detection (Luck and Vogel 1997), Cowan's review (2001), the K formula derived.
8. Slots or resources: continuous report; the mixture model (Zhang and Luck 2008) against variable precision
   (Bays and Husain 2008; van den Berg et al. 2012). The fits, and what each predicts.
9. How neurons hold a thought: delay activity (Funahashi et al. 1989); the ring attractor (computed; the bump
   drifts, and drift predicts the errors); activity-silent alternatives.
10. Working memory and intelligence: complex span, the correlation with fluid reasoning (Part 32).
11. Can you train it? Jaeggi et al. (2008), the replications and meta-analyses, the 2016 consensus review, and
    the FTC's settlement with Lumosity.

*Psyche:* `wm`: slot, resource and mixture models with ML fits to open continuous-report data; a ring attractor
whose diffusion predicts precision against delay; an interference model of span.
*On you:* Battery task 5; digit span forwards and with articulatory suppression.
*Ledger:* capacity near four chunks (`replicated`); Sternberg's linear scanning (`replicated`); far transfer from
working-memory training (`failed`); the word-length effect (`replicated, refined`).
*In practice:* interface and form design, checklists and read-backs, cognitive assessment; the brain-training
market as a case study in evidence.
*Frontier:* slots against resources is not closed; persistent against silent codes; whether capacity limits are a
bug or an optimal trade (Part 58).
*Reading:* Miller 1956; Sperling 1960; Baddeley & Hitch 1974; Cowan 2001; Luck & Vogel 1997; Zhang & Luck 2008;
Ma, Husain & Bays 2014; Oberauer et al. 2018 (benchmarks); Simons et al. 2016.

### Part 20 · Memory I: Storing and Finding (~55)
*Question:* when you remember, what is being searched, and with what?
*Story:* in 1885 Hermann Ebbinghaus publishes the first experiments on memory, with one subject, himself, and
2,300 invented syllables. The next century finds lawful curves in what people recall and in what order. The best
account is a search: you remember with a cue, and the most important cue is the slowly drifting context of your
own mind.
1. Hook: Ebbinghaus's method. Savings; the first forgetting curve.
2. On you: free recall of a fifteen-word list.
3. The serial position curve (Murdock 1962): primacy and recency; what a delay and a distractor do to each.
4. The order of recall: contiguity. After recalling a word you recall its neighbour, forward more than backward
   (Kahana 1996). The lag-CRP curve of your own recall.
5. Encoding: levels of processing (Craik and Lockhart 1972); the generation effect; imagery and the method of
   loci.
6. Cues: encoding specificity (Tulving and Thomson 1973); context-dependent memory under water (Godden and
   Baddeley 1975) and its replication record; state dependence.
7. Search of associative memory (Raaijmakers and Shiffrin 1981): sampling by cue strength, recovery, stopping.
   The model run on the list.
8. Context that drifts: the temporal context model (Howard and Kahana 2002). Recency and contiguity from one
   mechanism (derived, computed).
9. Memories as attractors: the Hopfield network (1982). Storage by Hebb's rule, recall by settling, capacity near
   0.14 N (computed; link to *AI, Built* Part 20).
10. Memory systems: H.M. again; episodic and semantic (Tulving); declarative and procedural; priming. One system
    or several, and what dissociations can show (Part 7).
11. Recognition against recall: familiarity and recollection, and the SDT account (Part 12).
12. The hippocampus as index: pattern separation and completion; time cells.

*Psyche:* `memory`: SAM and a temporal-context model fitted to open free-recall data (serial position and lag-CRP
together); a Hopfield network with its capacity curve; ACT-R's activation equation.
*On you:* Battery task 6: your serial-position and contiguity curves.
*Ledger:* serial position and contiguity (`replicated`); levels of processing (`replicated`); the testing effect
(preview, `replicated`); underwater context dependence (`contested`: a 2021 replication did not find it
**(verify)**).
*In practice:* mnemonic techniques, interview and survey design (what cues recall), memory assessment in the
clinic.
*Frontier:* one memory system or many; whether context models scale from lists to lives; the engram and the
model's "context".
*Reading:* Ebbinghaus 1885; Murdock 1962; Tulving & Thomson 1973; Raaijmakers & Shiffrin 1981; Howard & Kahana
2002; Hopfield 1982; Kahana, *Foundations of Human Memory*; Baddeley, Eysenck & Anderson, *Memory*.

### Part 21 · Memory II: Forgetting and Inventing (~55)
*Question:* why do we forget, and why do we remember things that never happened?
*Story:* Elizabeth Loftus shows people a film of a car crash and changes one word in the question. A week later
those asked about cars that "smashed" remember broken glass. There was none. Memory is reconstruction, which
explains its efficiency and its errors, and the same mechanisms tell you how to study and how not to run a
police interview.
1. Hook: Loftus and Palmer (1974).
2. The shape of forgetting: exponential or power? Jost's law; Wixted's analysis; Ebbinghaus's curve replicated in
   2015.
3. Why: decay against interference (Jenkins and Dallenbach's sleepers, 1924); proactive and retroactive
   interference; retrieval-induced forgetting.
4. Consolidation: retrograde amnesia's gradient; sleep and replay; reconsolidation (Nader et al. 2000) and its
   limits in people.
5. Complementary learning systems (McClelland, McNaughton and O'Reilly 1995): why a fast and a slow learner;
   catastrophic interference shown in a small network, and interleaving as the cure (link to *AI, Built*).
6. Spacing: Ebbinghaus onward; the optimal gap grows with the retention interval (Cepeda et al. 2008).
7. Testing: retrieval practice beats restudy after a delay, and students predict the opposite (Roediger and
   Karpicke 2006). Returns in Part 54.
8. Bartlett's "War of the Ghosts" (1932): schemas and reconstruction.
9. On you: the DRM lists (Roediger and McDermott 1995). You will remember a word that was not there.
10. Misinformation and implantation: "lost in the mall" (1995), its replication, and how implantation rates
    depend on scoring.
11. Confidence, flashbulb memories (vivid, confident, and no more accurate), and eyewitnesses (taken to court in
    Part 56).
12. Exceptional memories: mnemonists, highly superior autobiographical memory, and what they do not show.

*Psyche:* `memory`: forgetting functions fitted to Ebbinghaus's and modern data; a complementary-learning-systems
pair of networks; a spacing model that reproduces the optimal-gap ridge; a schema model that produces the DRM
lure.
*On you:* the DRM lists; a retention-interval prediction.
*Ledger:* the misinformation effect (`replicated`); DRM false recall (`replicated`); the testing effect
(`replicated`); the spacing effect (`replicated`); reconsolidation-based erasure in humans (`contested`);
repressed and recovered memories (`contested`; told in Part 56).
*In practice:* study methods, spaced-repetition software (Part 54), cognitive interviewing, the courtroom.
*Frontier:* what sleep replay does in humans; whether forgetting is adaptive (rational analysis, Part 58);
editing memories.
*Reading:* Loftus & Palmer 1974; Bartlett 1932; McClelland, McNaughton & O'Reilly 1995; Roediger & Karpicke 2006;
Roediger & McDermott 1995; Cepeda et al. 2008; Wixted 2004; Schacter, *The Seven Sins of Memory*; Murre & Dros
2015.

### Part 22 · Concepts and Categories (~50)
*Question:* what do you know when you know what a bird is?
*Story:* Aristotle said a concept is a definition. Wittgenstein asked for the definition of "game", and Eleanor
Rosch showed that people agree a robin is a better bird than a penguin. If concepts are not definitions, are they
averages or remembered examples? The two answers become two equations, and Roger Shepard finds a law of
generalization he argues should hold for any mind anywhere.
1. Hook: is a penguin a bird, is a tomato a fruit, how fast do you say yes? Typicality in reaction times.
2. The classical view and its failure: no definitions, graded membership, unclear cases (Rosch 1975; family
   resemblance).
3. Prototypes: a category as a central tendency; the prototype is "recognized" though never seen (Posner and
   Keele 1968).
4. Exemplars: the context model (Medin and Schaffer 1978) and Nosofsky's generalized context model (1986):
   similarity, attention weights, choice. Derived.
5. On you: learn a two-dimensional category in forty trials. Prototype and exemplar models fitted to your
   responses.
6. Shepard, Hovland and Jenkins's six problems (1961): the difficulty order that models must reproduce; ALCOVE as
   exemplars plus error-driven attention (Parts 16 and 18 meeting).
7. Psychological space: multidimensional scaling turns a table of confusions into a map (derived; link to
   `statkit.multi`).
8. Shepard's universal law (1987): generalization falls exponentially with distance in that space; his argument
   from consequential regions.
9. Similarity is not distance: Tversky's contrast model (1977) and the asymmetries.
10. Knowledge in a network: Collins and Quillian's hierarchy (1969), spreading activation, semantic priming.
11. Concepts as theories: essentialism in children, causal knowledge; Bayesian concept learning and the number
    game (Tenenbaum).
12. Meaning from co-occurrence: latent semantic analysis (1997) to word embeddings as models of semantic memory.

*Psyche:* `concepts`: prototype, GCM and ALCOVE fitted to the six problems and to open category-learning data; MDS
on a classic confusion matrix; the number game's hypothesis averaging.
*On you:* the category-learning task; the number game.
*Ledger:* typicality effects (`replicated`); the six-problem ordering (`replicated`, with a known exception for
Type II); the universal law (`replicated` across species and modalities); the hierarchical network's strict
predictions (`failed`, superseded).
*In practice:* taxonomy and navigation design, diagnosis by resemblance, recommendation by similarity, embeddings.
*Frontier:* prototypes against exemplars is a question about representation that behaviour may not settle (model
mimicry, Part 48); few-shot concept learning; whether embeddings have human-like geometry (Part 60).
*Reading:* Rosch 1975; Medin & Schaffer 1978; Nosofsky 1986; Shepard 1987; Tversky 1977; Kruschke 1992; Murphy,
*The Big Book of Concepts*; Tenenbaum & Griffiths 2001; Landauer & Dumais 1997.

### Part 23 · Language (~55)
*Question:* how does a child who hears a finite number of sentences come to understand an infinite number?
*Story:* in 1959 a thirty-year-old linguist reviews B. F. Skinner's book on verbal behaviour and argues that no
theory of reinforcement can explain a sentence never heard before. The review helps start cognitive science. The
argument it began, how much is built in and how much is learned from statistics, has now run for seventy years,
and machines that learn language from text alone have joined it.
1. Hook: Chomsky's review. "Colorless green ideas sleep furiously."
2. The levels: phonemes, morphemes, words, syntax, meaning, use. Productivity at each (the wug test, Berko 1958).
3. The mental lexicon: frequency, neighbourhoods, lexical decision. Zipf's law.
4. Recognizing a word: the word-superiority effect; the interactive activation model (McClelland and Rumelhart
   1981): letters, words, feedback (computed); spoken words in time (the cohort model and TRACE).
5. Sentences in real time: ambiguity and the garden path; eye movements in reading.
6. Surprisal: processing difficulty is the negative log probability of the word in context (Hale 2001; Levy
   2008); reading time is close to linear in it. Computed with the language model of *AI, Built*.
7. On you: sixty seconds of an alien language. You will find the words (Saffran, Aslin and Newport 1996).
8. Acquisition: babbling to grammar; the poverty-of-the-stimulus argument stated as a learnability claim (link to
   *Philosophy, Built* Part 15); word learning as inference.
9. The past-tense debate: a network that learns "goed" and then "went" (Rumelhart and McClelland 1986) against
   words and rules (Pinker and Prince 1988).
10. A critical period? Genie; late signers; Johnson and Newport (1989); two-thirds of a million learners
    (Hartshorne, Tenenbaum and Pinker 2018).
11. Language in the brain: Broca, Wernicke, and the modern network; the N400 and P600; aphasia.
12. Language and thought: Whorf's claim, strong and weak; colour terms; Russian blues (Winawer et al. 2007);
    numbers without number words.

*Psyche:* `language`: interactive activation reproducing the word-superiority effect; a segmenter driven by
transitional probabilities; a past-tense network with its U-shaped curve; surprisal from the series' own language
model regressed on open reading-time data.
*On you:* statistical segmentation; a garden path; Battery task 11.
*Ledger:* infant statistical learning (`replicated`); surprisal and reading time (`replicated`); a sharp critical
period (`contested`); linguistic relativity for colour discrimination (`replicated, smaller`); a bilingual
advantage in executive control (`contested`, leaning `failed`).
*In practice:* speech recognition and reading instruction (Part 54), aphasia therapy, readability, second-
language teaching.
*Frontier:* what language models' success shows about learnability; child-scale input (training on one child's
recordings **(verify)**); whether surprisal from larger models fits reading times worse.
*Reading:* Chomsky 1959; Saffran, Aslin & Newport 1996; McClelland & Rumelhart 1981; Levy 2008; Pinker, *The
Language Instinct* and *Words and Rules*; Rumelhart & McClelland 1986; Hartshorne et al. 2018; Traxler,
*Introduction to Psycholinguistics*.

### Part 24 · Reasoning and Problem Solving (~55)
*Question:* are people logical, and if not, what are they instead?
*Story:* four cards, one rule, and nine in ten university students choose wrongly. Change the cards to drinks and
ages and nearly everyone is right. Reasoning is not the application of logic to content; content is the engine.
Meanwhile Newell and Simon write a program that solves problems as people do, by searching, and the expert turns
out to be someone who no longer needs to.
1. Hook and On you: Wason's selection task (1966), abstract, then as a drinking-age rule.
2. Deduction: syllogisms, belief bias (Evans et al. 1983); mental rules against mental models (Johnson-Laird).
3. Why content helps: pragmatic schemas, cheater detection (Cosmides 1989), and the probabilistic account
   (Oaksford and Chater 1994): the "wrong" cards are the informative ones.
4. Problem solving as search: Newell and Simon; states, operators, means–ends analysis; the Tower of Hanoi's
   state space drawn, and human move sequences on it.
5. Protocols and production systems: thinking aloud as data; rules that fire; ACT-R in outline.
6. Insight: Duncker's candle, the nine dots, functional fixedness; is insight special? (Metcalfe's warmth
   ratings.)
7. Expertise: de Groot and Chase and Simon (1973), chess positions real and random; chunks; deliberate practice
   (Ericsson 1993) and how much it explains (Macnamara et al. 2014).
8. Analogy: Gick and Holyoak's radiation problem (1980); structure mapping (Gentner).
9. Imagery: mental rotation, reaction time linear in angle (Shepard and Metzler 1971); the imagery debate
   (Kosslyn against Pylyshyn); aphantasia.
10. Causal reasoning: from ΔP (Part 16) to causal power (Cheng 1997) and interventions on causal graphs (link to
    *Statistics, Built* Part 36).
11. Everyday prediction as Bayesian inference (Griffiths and Tenenbaum 2006): people's guesses about life spans
    and movie grosses match the right priors.
12. Rational, irrational, or bounded: Simon's satisficing, and the argument Part 26 continues.

*Psyche:* `reason`: a small production system solving the Tower of Hanoi with human-like move latencies; mental-
model enumeration for syllogisms against difficulty data; a rotation model; causal power.
*On you:* the selection task; Battery task 10; the candle problem.
*Ledger:* the selection task's content effect (`replicated`); mental rotation (`replicated`); belief bias
(`replicated`); chess chunking (`replicated`); the 10,000-hour rule (`story and record`); optimal everyday
predictions (`replicated`; individual-level interpretation `contested`).
*In practice:* interview puzzles and what they do not measure, training design, decision support, protocol
analysis in UX.
*Frontier:* program induction as a model of thinking; whether language models reason by analogy (Part 60);
cognitive architectures against end-to-end learning.
*Reading:* Wason 1966; Newell & Simon 1972; Chase & Simon 1973; Shepard & Metzler 1971; Gick & Holyoak 1980;
Johnson-Laird 1983; Oaksford & Chater 2007; Anderson 2007; Holyoak & Morrison (eds.), *The Oxford Handbook of
Thinking and Reasoning*.

### Part 25 · Deciding in Time (~55)
*Question:* why do decisions take the time they take?
*Story:* during the war Abraham Wald worked out the fastest reliable way to decide between two hypotheses: add up
evidence until it crosses a line. In 1978 Roger Ratcliff proposes that this is what a person does in half a
second, and the proposal accounts for accuracy, speed, and the full shape of reaction-time distributions at
once. Twenty years later neurons in monkey parietal cortex are seen climbing to a bound.
1. Hook and On you: moving dots. Which way? Now faster.
2. Two old laws: Hick (1952), reaction time grows with the logarithm of the number of alternatives; Fitts
   (1954), movement time with the logarithm of distance over width. Information theory in the 1950s laboratory.
3. The speed–accuracy trade-off, drawn. Any model of choice must produce it.
4. What a reaction-time distribution looks like: the skew, the ex-Gaussian, why means mislead.
5. A random walk between two bounds: the sequential probability ratio test, and Wald's result that it is optimal.
6. The drift–diffusion model (Ratcliff 1978): drift, bound, start point, non-decision time. Accuracy and mean RT
   in closed form (derived); the distributions (computed).
7. Each parameter is a psychological claim: difficulty moves drift, instructions move the bound, payoffs move the
   start. The selective-influence experiments.
8. Fast errors and slow errors: across-trial variability.
9. The brain: Shadlen and Newsome's recordings in LIP; ramping to a bound; the stepping-against-ramping dispute.
10. Relatives: the linear ballistic accumulator, leaky competing accumulators, urgency signals; many alternatives
    and Hick's law recovered.
11. Stopping: the stop-signal task as a race (Logan and Cowan 1984); the stop-signal reaction time, derived.
12. Confidence: reading the losing accumulator; meta-d′ (Part 12 continued).

*Psyche:* `decide`: the SPRT; the diffusion model with its closed forms and a fast simulator; hierarchical fits to
open random-dot data; the LBA; the stop-signal race.
*On you:* Battery task 7 under speed and accuracy instructions; your two fitted bounds.
*Ledger:* Hick's and Fitts's laws (`replicated`); selective influence in the diffusion model (`replicated`, with
exceptions); the readiness potential as accumulation (Part 27); ramping in LIP (`contested` at the single-trial
level).
*In practice:* interface latency and menu design (Part 52), driver reaction models, cognitive screening by RT
decomposition, drift rates as trial outcome measures.
*Frontier:* collapsing bounds; decisions between values and attention-weighted accumulation; whether parameters
are stable traits (Part 59).
*Reading:* Wald 1947; Hick 1952; Fitts 1954; Ratcliff 1978; Ratcliff & McKoon 2008; Bogacz et al. 2006; Gold &
Shadlen 2007; Brown & Heathcote 2008; Logan & Cowan 1984; Luce, *Response Times*.

### Part 26 · Judgment and Choice (~55)
*Question:* why do the same people buy insurance and lottery tickets?
*Story:* a disease threatens six hundred people. Described as lives saved, most people choose the sure thing;
described as deaths, most gamble. The outcomes are identical. Kahneman and Tversky turn such reversals into a
theory with a kinked value curve and bent probabilities, and win economics' attention. Their critics ask whether
the "biases" are errors at all. Unlike much else from its era, most of this replicates.
1. Hook and On you: the disease problem (1981), and five more, answered before the reveal.
2. The standard: expected value, the St Petersburg game, Bernoulli's utility, the von Neumann–Morgenstern axioms
   in one slide (link to *Philosophy, Built* Part 33).
3. The violations: Allais's paradox, drawn in the probability triangle; preference reversals.
4. Prospect theory (1979): reference dependence, loss aversion, diminishing sensitivity, probability weighting.
   The value and weighting functions derived from the choices; the 1992 parameters.
5. The fourfold pattern of risk attitudes, computed from those two curves. Insurance and lotteries.
6. Heuristics and biases (1974): availability, representativeness (Linda), anchoring; base-rate neglect.
7. The reply: frequency formats, ecological rationality, fast and frugal heuristics that beat regression out of
   sample (Gigerenzer; take-the-best, computed).
8. Choice over time: exponential discounting and its consistency; hyperbolic discounting and preference reversal;
   the β–δ model.
9. Decisions from experience: rare events are underweighted when learned, overweighted when described.
10. Two systems? The dual-process story, its evidence and its critics.
11. Where preferences come from: sampling and range–frequency accounts; value as efficient code (Part 58).
12. What replicated: the 2014 and 2018 Many Labs results for framing, anchoring and sunk cost; prospect theory in
    nineteen countries (Ruggeri et al. 2020); the dispute over loss aversion.

*Psyche:* `choice`: cumulative prospect theory fitted to open choice data; the heuristics toolbox against
regression in cross-validation; discounting models; decision by sampling.
*On you:* Battery task 9; the classic problems with the published splits.
*Ledger:* framing (`replicated`); anchoring (`replicated`); the Allais pattern (`replicated`); the conjunction
fallacy (`replicated`; interpretation `contested`); loss aversion (`replicated` for large stakes, `contested` for
small); the hot hand "fallacy" (`story and record`: the original analysis was biased, Miller & Sanjurjo 2018).
*In practice:* pricing, insurance and pension design, medical risk communication, product defaults (Part 55).
*Frontier:* large-scale choice datasets and machine-learned theories (Peterson et al. 2021); resource-rational
accounts of biases; whether risk preference is one trait.
*Reading:* Kahneman & Tversky 1979; Tversky & Kahneman 1974, 1981, 1992; Gigerenzer, Todd & the ABC Group 1999;
Laibson 1997; Hertwig et al. 2004; Kahneman, *Thinking, Fast and Slow* (with its own errata); Ruggeri et al. 2020.

### Part 27 · Consciousness (~55)
*Question:* what is the difference between information the brain uses and information you experience?
*Story:* a man with a damaged visual cortex insists he sees nothing in half his visual field, and when forced to
guess, points to objects there almost perfectly. Blindsight makes the question experimental: hold the stimulus
constant, vary awareness, and look for what changes. Rival theories now make different predictions, and for the
first time their authors have agreed in advance on experiments that could embarrass them.
1. Hook: patient D.B. (Weiskrantz 1974). Seeing without knowing it.
2. On you: masking. The same word, seen and unseen, by changing forty milliseconds.
3. The contrastive method: masking, binocular rivalry, inattention, neglect and extinction. What unconscious
   processing can do (priming) and the measurement problem (Part 12: is it a criterion effect?).
4. The easy problems and the hard one, in two minutes (the philosophy is *Philosophy, Built* Part 31).
5. Correlates: front or back of the brain? Report against experience; no-report paradigms.
6. The global workspace (Baars; Dehaene): ignition, the P3b, the all-or-none signature (a network that ignites,
   computed).
7. Integrated information theory: Φ in outline, its predictions and the 2023 open letter calling it
   pseudoscience.
8. Recurrent processing and higher-order theories, each in one diagram with one prediction.
9. Adversarial collaboration: preregistered tests of workspace against integrated-information predictions (the
   Cogitate results **(verify)**): what each theory got wrong.
10. Volition: Libet's clock (1983); the readiness potential as accumulated noise (Schurger et al. 2012; Part
    25's model).
11. Losing consciousness: sleep (Part 10), anaesthesia, disorders of consciousness; detecting awareness in
    unresponsive patients (Owen et al. 2006) and the perturbational complexity index.
12. Attention is not consciousness; metacognition; what would count as progress.

*Psyche:* `workspace`: an ignition network with a bifurcation between subliminal and conscious regimes; a rivalry
oscillator (adaptation plus inhibition) with its dominance-time distribution.
*On you:* masking; binocular rivalry with red–cyan glasses or free fusion.
*Ledger:* blindsight (`replicated`; whether it is degraded conscious vision, `contested`); unconscious semantic
priming (`replicated, smaller`); Libet's timing (`replicated`; interpretation `contested`); covert awareness in
unresponsive patients (`replicated`).
*In practice:* anaesthesia monitoring, diagnosis after brain injury, the question of machine consciousness (Part
60).
*Frontier:* the whole part is a frontier; the chapter gives the current scorecard of theories and the next
adversarial collaborations.
*Reading:* Weiskrantz 1986; Dehaene, *Consciousness and the Brain*; Tononi et al. 2016; Lamme 2006; Seth & Bayne
2022; Libet et al. 1983; Schurger, Sitt & Dehaene 2012; Owen et al. 2006; Cogitate Consortium **(verify)**.

---

## Act VI · Feeling and Wanting

### Part 28 · Motivation (~50)
*Question:* why do anything?
*Story:* in 1954 a rat with a misplaced electrode keeps returning to the corner of the box where the current came
on. Given a lever, rats press it thousands of times an hour and ignore food. Olds and Milner had found something,
but not pleasure: later work splits wanting from liking. From there the part follows motivation upward, from
hunger as a control loop to goals and self-control, where some of psychology's most famous findings did not
survive.
1. Hook: Olds and Milner's rat.
2. Drives and homeostasis: Cannon; Hull's drive reduction; a thermostat as a negative-feedback loop (derived).
3. Hunger as control: glucose, leptin and ghrelin, the hypothalamus; set points and settling points; why diets
   regain (the loop, computed).
4. Beyond drives: curiosity and play; Harlow's monkeys solving puzzles for nothing; optimal arousal (the
   Yerkes–Dodson "law", and what the 1908 mice showed).
5. Wanting is not liking (Berridge and Robinson): dopamine and incentive salience; opioid hedonic hotspots.
   Returns in Part 41.
6. Intrinsic and extrinsic: the overjustification effect (Lepper, Greene and Nisbett 1973); the meta-analyses;
   self-determination theory's three needs.
7. Goals: goal-setting theory (Locke and Latham); implementation intentions; expectancy times value.
8. On you: sooner-smaller or later-larger. Your discount curve (Part 26's model).
9. Self-control as a resource: ego depletion (Baumeister et al. 1998), hundreds of studies, a meta-analysis, then
   the 2016 registered replication across twenty-three laboratories with an effect near zero.
10. The marshmallow test (Mischel): the original follow-ups, and the 2018 conceptual replication in which the
    association shrinks by about two-thirds with family background controlled.
11. Grit and mindset: what the large studies find (small effects, concentrated in some students). Continued in
    Part 54.
12. Effort as a cost: the expected value of control; why mental effort feels like something.

*Psyche:* `drive`: a homeostatic controller with a defended set point; an incentive-salience term added to Part
17's learner; the expected-value-of-control model choosing how hard to try.
*On you:* a delay-discounting titration.
*Ledger:* brain-stimulation reward (`replicated`); overjustification (`replicated`; scope `contested`); ego
depletion (`failed` in its sequential-task form); delay of gratification predicting life outcomes (`replicated,
smaller`); grit beyond conscientiousness (`contested`); goal-setting effects (`replicated`).
*In practice:* incentive design at work (Part 53), gamification, weight-loss programmes, habit apps.
*Frontier:* what, if anything, is depleted; computational accounts of effort and boredom; motivation in
artificial agents.
*Reading:* Olds & Milner 1954; Berridge & Robinson 1998; Deci, Koestner & Ryan 1999; Baumeister et al. 1998;
Hagger et al. 2016; Mischel, Shoda & Rodriguez 1989; Watts, Duncan & Quan 2018; Shenhav, Botvinick & Cohen 2013;
Locke & Latham 2002.

### Part 29 · Emotion (~55)
*Question:* do we run because we are afraid, or are we afraid because we run?
*Story:* William James says the second, in 1884, and psychology has argued about the order of events ever since.
The modern form of the argument is whether anger, fear and joy are natural kinds with fixed faces and circuits,
or categories a brain constructs from two simpler ingredients. Along the way: a pen held in the teeth, a rickety
bridge, lottery winners, and what money does for happiness.
1. Hook: James's bear. The James–Lange theory; Cannon's five objections; Cannon–Bard.
2. Two factors: Schachter and Singer's adrenaline study (1962) and its replication record; misattribution on the
   bridge (Dutton and Aron 1974).
3. Faces: Darwin (1872); Ekman and Friesen in New Guinea; six basic emotions; the forced-choice method and what
   happens without it.
4. On you: sort twenty schematic faces. The solution has two dimensions: valence and arousal (Russell's
   circumplex 1980).
5. Constructed emotion (Barrett): variability within a category, the 2019 review of faces, core affect and
   interoception. The best case for each side.
6. Facial feedback: the pen-in-mouth study (Strack et al. 1988), the seventeen-laboratory null (2016), and the
   Many Smiles collaboration (2022): a small effect, depending on the task.
7. Appraisal: Lazarus; emotions as evaluations of events against goals; an appraisal model that outputs emotion
   labels from scenarios (computed).
8. Fear in the brain: LeDoux's two roads, fear conditioning (Part 16) and the amygdala; patient S.M.; what
   "fear circuit" does and does not mean.
9. Stress and coping (Part 10's loop); emotion regulation: reappraisal against suppression (Gross).
10. Affective forecasting: we mispredict how long feelings last (Gilbert and Wilson); hedonic adaptation;
    lottery winners and accident victims (Brickman et al. 1978), as measured.
11. Happiness and income: the 2010 plateau, the 2021 no-plateau, and the 2023 adversarial collaboration that
    reconciled them.
12. The critical positivity ratio: a chaos-theory formula for flourishing, cited thousands of times, taken apart
    by a part-time graduate student and a physicist (2013).

*Psyche:* `emotion`: MDS of open emotion-rating data recovering the circumplex; an appraisal model; a fear-
learning circuit built from Parts 6 and 16.
*On you:* the face-sorting task; a forecast of your own reaction, checked at the end of the part.
*Ledger:* facial feedback (`replicated, smaller`, conditional); Schachter–Singer (`contested`); universal
recognition of six expressions (`replicated` with forced choice, `contested` without); the bridge study (`not
directly tested` at scale); the positivity ratio (`retracted` in part); money and well-being (`replicated`; shape
resolved by adversarial collaboration).
*In practice:* emotion-recognition software and why its premise is disputed; well-being measurement in policy;
emotion regulation in therapy.
*Frontier:* emotion as inference about the body; whether animals' defensive states are "emotions"; affect in
language models.
*Reading:* James 1884; Schachter & Singer 1962; Ekman 1992; Russell 1980; Barrett 2017; Barrett et al. 2019; Coles
et al. 2022; LeDoux 1996; Gross 2015; Killingsworth, Kahneman & Mellers 2023; Brown, Sokal & Friedman 2013.

---

## Act VII · Growing

### Part 30 · The Infant Mind (~55)
*Question:* what does a baby know, and how can you find out?
*Story:* Piaget watches his own three children and concludes that an infant does not know a hidden object still
exists. The obstacle to checking him is that infants cannot answer questions. Then Robert Fantz notices that they
can look, and that looking can be timed. Looking time becomes developmental psychology's instrument, with all of
Part 3's questions about what an instrument measures.
1. Hook: Piaget's A-not-B error. The infant watches the toy go under B and reaches to A.
2. Piaget's theory: schemes, assimilation and accommodation, four stages; conservation tasks.
3. The method: Fantz's looking chamber (1961); habituation and dishabituation; violation of expectation. A trial
   strip, and a model of looking as information seeking (the Goldilocks effect, Kidd et al. 2012).
4. On you: six infant experiments. Predict where the baby looks longer.
5. Objects: Baillargeon's drawbridge (1985, 1987); Spelke's core principles (cohesion, continuity, contact).
6. Number: Wynn's 1 + 1 (1992); the approximate number system and its Weber fraction sharpening with age (Part
   11).
7. Core knowledge against constructivism against rational constructivism (infants as statisticians, Xu and Garcia
   2008). The best case for each.
8. A-not-B as dynamics: a neural field with memory and input (Thelen, Smith and colleagues 2001) reproduces the
   error and its dependence on delay (computed). Knowledge is not a yes-or-no possession.
9. Other minds: the false-belief task (Wimmer and Perner 1983); passing at four; implicit tests at fifteen months
   (Onishi and Baillargeon 2005) and their troubled replications.
10. Attachment: Harlow's cloth and wire mothers (1958); Bowlby; Ainsworth's Strange Situation; what early
    attachment predicts (modestly).
11. Temperament, and the first look at how children shape their own environments (Part 9's gene–environment
    correlation).
12. Vygotsky: the zone of proximal development; learning from others (natural pedagogy; overimitation).

*Psyche:* `develop`: a habituation model whose looking times follow surprise non-monotonically; a dynamic neural
field that makes and then outgrows the A-not-B error; an approximate-number observer with age-dependent Weber
fraction.
*On you:* the predict-the-infant quiz.
*Ledger:* A-not-B (`replicated`); violation-of-expectation object knowledge (`replicated`; rich interpretation
`contested`); Wynn's arithmetic (`replicated`; interpretation `contested`); explicit false belief near four
(`replicated`); implicit false belief in infants (`contested`, multi-laboratory failures); neonatal imitation
(`contested`: a large longitudinal study found none); infant-directed speech preference (`replicated`,
ManyBabies).
*In practice:* developmental screening, early-childhood programmes, design of children's media and toys.
*Frontier:* large-scale infant science (ManyBabies) and what replicates; head-camera corpora; infants as a
benchmark for machine common sense.
*Reading:* Piaget 1954; Fantz 1961; Baillargeon 1987; Spelke & Kinzler 2007; Wynn 1992; Thelen et al. 2001;
Wimmer & Perner 1983; Ainsworth et al. 1978; Gopnik, Meltzoff & Kuhl, *The Scientist in the Crib*; ManyBabies
Consortium 2020.

### Part 31 · The Lifespan (~50)
*Question:* what, in a life, is set early, and what stays open?
*Story:* in 2000 researchers in Bucharest do something almost never possible: with too few foster homes for the
children in the city's institutions, placement is decided by lottery. A randomized experiment on the effect of
early care follows the children for two decades. Most questions about development cannot be randomized, and this
part is about the designs that try to answer them anyway.
1. Hook: the Bucharest Early Intervention Project. IQ and attachment by age of placement.
2. Three clocks: age, period, cohort, and why they cannot be separated without assumptions (drawn; the identity
   age = period − cohort).
3. Cross-sectional against longitudinal: the same ability "declines from twenty" or "holds to sixty" depending on
   design (Schaie's Seattle study). Attrition and practice effects, on the Pool.
4. Growth curves: every child a line, the population a fan; a first look at multilevel models (Part 47).
5. Sensitive periods: Hubel and Wiesel's kittens; language (Part 23); what closes a window.
6. Adolescence: the brain's late-maturing control systems; risk taking with peers present; what "the teenage
   brain" explains and excuses.
7. Parents: the correlations, and the behaviour-genetic challenge (Part 9): adoptive siblings grow up no more
   alike. What parenting demonstrably does.
8. Early intervention: Perry Preschool and Abecedarian (small randomized trials, long follow-up); fade-out and
   re-emergence; Head Start's evidence; the "thirty-million-word gap" and its replication.
9. Moral and identity development: Kohlberg's stages and Gilligan's critique; Erikson, briefly.
10. Adulthood and ageing: fluid and crystallized abilities; processing speed (Salthouse); what stays and
    improves (vocabulary, emotional regulation; socioemotional selectivity).
11. Dementia: what is normal ageing and what is not; reserve; the modifiable risk factors and the strength of
    their evidence.
12. Cohorts change: the Flynn effect as a lifespan fact (Part 32).

*Psyche:* `develop`: growing and ageing parameters for the Pool; a cohort-sequential design that recovers what
cross-sectional and longitudinal designs each get wrong; growth-curve fits.
*On you:* three graphs: age, period or cohort?
*Ledger:* institutional deprivation harms and early placement helps (`replicated`; randomized); Perry Preschool's
long-run effects (`replicated` within the trial; small N); the word gap's size (`contested`); adult
neurogenesis in humans (`contested`); birth-order effects on personality (`failed`; a small effect on IQ
`replicated`).
*In practice:* family policy, schooling ages, juvenile justice, retirement and driving assessments, cognitive
screening.
*Frontier:* the ABCD cohort and what large longitudinal imaging can show; causal inference from cohort data;
ageing interventions.
*Reading:* Nelson, Fox & Zeanah, *Romania's Abandoned Children*; Schaie 2005; Baltes 1987; Steinberg 2008;
Harris, *The Nurture Assumption*; Heckman 2006; Salthouse 2010; Siegler et al., *How Children Develop*.

---

## Act VIII · Differing

### Part 32 · Intelligence (~60)
*Question:* is there one thing that the word "intelligence" measures?
*Story:* in 1904 Charles Spearman notices that schoolchildren good at one thing tend to be good at everything,
and invents factor analysis to explain it with a single general factor. In the same year the French government
asks Alfred Binet for a practical test, and he builds one while warning against treating its score as a fixed
quantity. The mathematics is beautiful, the test predicts, and within twenty years it is being used to sterilize
people. All three facts are in this part.
1. Hook: Spearman's correlation table and Binet's commission. Two men, two attitudes to the same number.
2. The positive manifold: every ability test correlates positively with every other. An Archive matrix, drawn as
   a heat map.
3. Factor analysis derived: a correlation matrix as loadings times loadings plus uniqueness; Spearman's tetrad
   differences; extraction and rotation (link to `statkit.multi`).
4. One factor or many: Thurstone's primary abilities; the hierarchical compromise (Carroll's three strata; CHC).
5. What g is not shown to be: the same manifold from a single cause, from sampling of many bonds (Thomson 1916),
   and from abilities that help each other grow (mutualism, van der Maas et al. 2006). Two worlds on the Pool,
   indistinguishable by factor analysis.
6. The scale: mental age, Stern's quotient, Wechsler's deviation IQ; norming; reliability and the standard error
   of a score (Part 3).
7. What it predicts: school, job performance (Part 53), health and mortality. Effect sizes, with pictures.
8. What it rests on: working memory (Part 19), speed, brain measures. Raven-style items solved by a rule-finding
   model (Carpenter, Just and Shell 1990).
9. Heritability rising with age; schooling raises scores (one to five points a year, Ritchie and Tucker-Drob
   2018); the Flynn effect and its reversal in some countries.
10. Group differences, with care: what a mean difference does and does not imply; measurement invariance as the
    technical question; the within-group heritability fallacy (Part 9's two fields); stereotype threat's record
    (Part 36). What the data cannot show.
11. The history of harm: Goddard at Ellis Island, the Army tests and the 1924 Immigration Act, *Buck v. Bell*
    (1927), Burt's data. Gould's critique and its own errors.
12. Other intelligences: multiple intelligences and emotional intelligence, judged by Part 3's standards.

*Psyche:* `traits`: a factor analyser checked on planted loadings and run on Archive matrices; a mutualism
simulation and a common-cause simulation with the same manifold; a matrix-item generator and a rule-induction
solver.
*On you:* generated matrix puzzles, as a demonstration of the item type, unscored.
*Ledger:* the positive manifold (`replicated`; among the most replicated findings in psychology); predictive
validity (`replicated`); the Flynn effect (`replicated`); schooling effects (`replicated`); the "Mozart effect"
(`failed`); multiple intelligences as separable abilities (`failed`).
*In practice:* educational placement, clinical and forensic assessment (Part 56), selection (Part 53); what a
score may and may not be used for.
*Frontier:* network against factor models; what polygenic scores for attainment mean; measuring intelligence in
machines (Part 60).
*Reading:* Spearman 1904b; Binet & Simon 1905; Carroll 1993; Deary, *Intelligence: A Very Short Introduction*;
Neisser et al. 1996; Nisbett et al. 2012; van der Maas et al. 2006; Ritchie & Tucker-Drob 2018; Gould 1981, with
Lewis et al. 2011; Kevles 1985.

### Part 33 · Personality (~55)
*Question:* is there a "you" that stays the same across situations and years?
*Story:* in 1936 Gordon Allport and Henry Odbert go through an unabridged dictionary and copy out 17,953 words
that describe people. Fifty years of factor analysis reduce them to five dimensions. In between, Walter Mischel
nearly ends the field by showing how weakly traits predict any single act. The resolution is a lesson in
aggregation, and it ends with what your phone can infer about you.
1. Hook: the dictionary. The lexical hypothesis: differences that matter get a word.
2. From 17,953 words to five factors: Cattell's sixteen, Tupes and Christal, Goldberg, Costa and McCrae.
   Extraversion, agreeableness, conscientiousness, neuroticism, openness; the six-factor HEXACO variant.
3. On you: a fifty-item public-domain inventory. Your answers stay in the browser, and the result is a profile
   on five continua, not a type.
4. Types against traits: why the Myers–Briggs sorts a bell curve into two bins, and what that does to retest
   agreement (computed).
5. Mischel (1968): cross-situational consistency near r = 0.3. Hartshorne and May's honest and dishonest
   children.
6. The reply: aggregate over occasions and the correlations rise (Epstein 1979; the Spearman–Brown logic of Part
   3); situational effects are no larger (Funder and Ozer 1983); if-then signatures.
7. Stability and change: rank-order stability rising with age; mean-level change (people become more agreeable
   and conscientious); can you change on purpose?
8. Where traits come from: heritability near 0.4, little shared environment (Part 9); biological theories
   (Eysenck; Gray).
9. What traits predict: mortality, divorce, occupational success, at sizes comparable to socioeconomic status
   and IQ (Roberts et al. 2007); the 2019 replication of seventy-eight trait–outcome links.
10. Freud and the psychodynamic tradition: the claims, the influence, the evidential record; what survived (much
    of mental life is not conscious) and what did not. Projective tests under Part 3's standards.
11. Differences between women and men: the gender-similarities evidence, where the larger differences are, and
    the univariate against multivariate dispute.
12. Personality from digital footprints: likes predicting traits (Kosinski et al. 2013); the Cambridge Analytica
    story against the measured effect of psychological targeting.

*Psyche:* `traits`: five traits for the Pool; factor analysis of open IPIP responses; aggregation raising
predictive correlations; a dichotomized type's retest reliability.
*On you:* Battery questionnaire Q.
*Ledger:* the five-factor structure in Western, educated samples (`replicated`; cross-cultural generality
`contested`); trait–outcome associations (`replicated`, 87% in the 2019 project, at smaller sizes); the
person–situation correlation ceiling (`story and record`); Myers–Briggs types (`failed` as types); personality
prediction from likes (`replicated`); large persuasion effects of psychographic targeting (`contested`).
*In practice:* selection (conscientiousness; Part 53), clinical assessment, marketing segmentation, dating and
team "fit" products judged against the evidence.
*Frontier:* whether five factors are causes or summaries (networks, Part 44); personality change interventions;
traits inferred by language models.
*Reading:* Allport & Odbert 1936; Goldberg 1990; McCrae & Costa 1987; Mischel 1968; Epstein 1979; Funder & Ozer
1983; Roberts et al. 2007; Soto 2019; Hyde 2005; Kosinski, Stillwell & Graepel 2013; Funder, *The Personality
Puzzle*.

---

## Act IX · Other People

### Part 34 · Social Influence (~60)
*Question:* how much of what you do is decided by who is in the room?
*Story:* in 1961, in a basement at Yale, ordinary people are told by an experimenter in a grey coat to give
another person electric shocks. Most continue to the end of the board. Milgram's study, Asch's lines and
Zimbardo's prison became the public face of psychology. This part tells each as it was run, as it was retold, and
as the archives now show it, and then builds the mathematics of influence that the famous studies never had.
1. Hook: the shock generator. The procedure as a trial strip.
2. Sherif's moving light (1935): norms form and persist. Asch's lines (1951): what happened (about a third of
   critical trials conformed; a quarter of participants never did), and one ally cuts it sharply.
3. On you: Asch's lines with five recorded answers before yours.
4. Milgram: 65% at the baseline; the variations as a dose–response curve (proximity, legitimacy, peers who
   refuse); the partial replication of 2009; the archives (prods, disbelief, coaching) and the "engaged
   followership" reading.
5. The Stanford prison experiment (1971): the textbook version; the recordings of guards being instructed; the
   BBC Prison Study's different result.
6. Bystanders: the murder of Kitty Genovese and the thirty-eight witnesses who were not; Darley and Latané's
   smoke-filled room; diffusion of responsibility; real street-camera footage showing intervention in nine of ten
   conflicts (2020).
7. The presence of others: Triplett's reels (1898), Zajonc's drive theory and the cockroaches; social loafing.
8. Groups deciding: polarization, groupthink (and its thin evidence), minority influence.
9. Persuasion: the Yale programme; central and peripheral routes; Cialdini's principles and what field
   experiments find (Part 55).
10. Thresholds: Granovetter's riot model (1978). Two crowds, one person different, opposite outcomes (computed).
11. Opinion dynamics: DeGroot averaging and consensus; bounded confidence and polarization; simple against
    complex contagion (Centola 2010).
12. The wisdom of crowds: Galton's ox (1907), the error decomposition, and how social influence destroys it
    (Lorenz et al. 2011); the Music Lab's unpredictable hits (2006).

*Psyche:* `social`: threshold cascades; DeGroot and bounded-confidence dynamics on networks; a crowd-estimation
model with and without influence; a cumulative-advantage market.
*On you:* the Asch lines; estimate a quantity before and after seeing others' guesses.
*Ledger:* Asch conformity (`replicated`; smaller in later and individualist samples); Milgram obedience (`not
directly tested` in full; `replicated` in milder forms; interpretation `contested`); the Stanford prison
experiment (`story and record`: not an experiment and coached); the Genovese account (`story and record`); the
bystander effect (`replicated`, reversed in dangerous emergencies); groupthink (`contested`).
*In practice:* compliance and safety culture, jury and committee design, online review and rating systems,
viral marketing.
*Frontier:* influence measured in networks of millions; identifying contagion apart from homophily; algorithmic
amplification.
*Reading:* Asch 1956; Milgram 1974; Perry, *Behind the Shock Machine*; Haslam & Reicher 2012; Le Texier 2019;
Darley & Latané 1968; Manning, Levine & Collins 2007; Philpot et al. 2020; Granovetter 1978; DeGroot 1974; Lorenz
et al. 2011; Salganik, Dodds & Watts 2006.

### Part 35 · Social Cognition (~55)
*Question:* how do you read a mind, including your own?
*Story:* students who are paid one dollar to tell a lie come to believe it more than students paid twenty. Leon
Festinger says they are reducing dissonance; Daryl Bem says they are simply observing themselves the way they
would observe anyone. People explain behaviour with theories about hidden causes, their own included, and the
part ends by writing that theory down as inference. In the middle is the area of psychology hit hardest by the
replication crisis.
1. Hook: Festinger and Carlsmith (1959). The prophecy that failed (1956).
2. On you: Heider and Simmel's animation (1944). Two triangles and a circle; you will see a bully.
3. Attribution: Heider; Kelley's covariation cube as an analysis of variance; the correspondence bias (Jones and
   Harris 1967) and its cultural variation (Part 38).
4. Dissonance against self-perception: the predictions that separate them; the 2024 multi-laboratory replication
   of induced compliance **(verify)**.
5. Attitudes and behaviour: LaPiere's road trip (1934); when attitudes predict (specificity, strength); planned
   behaviour.
6. The self's illusions: better-than-average, self-serving attributions, false consensus. The Dunning–Kruger
   effect, and how much of its famous graph noise alone produces (computed).
7. First impressions: a tenth of a second (Willis and Todorov 2006); faces predicting elections; the validity of
   thin slices.
8. Automatic social behaviour: the elderly-walking study (Bargh et al. 1996), the 2012 failure, Kahneman's
   "train wreck" letter. What kinds of priming are solid (semantic, Part 22) and what were not.
9. Power posing: the 2010 paper, the larger replication, a co-author's public reversal.
10. Thinking about thinking: theory of mind in adults; the mentalizing network (Saxe).
11. Mind reading as inverse planning: a rational agent in a gridworld; infer its goal from its path by Bayes'
    rule (Baker, Saxe and Tenenbaum 2009). The model's ratings against people's.
12. Knowing others' minds better than our own? Introspection's limits revisited (Part 3).

*Psyche:* `social`: an inverse planner (Part 17's planner run backwards); Kelley's cube; a simulation of the
Dunning–Kruger plot from regression to the mean plus a better-than-average shift.
*On you:* the Heider–Simmel film; goal inference trials.
*Ledger:* correspondence bias (`replicated`; culturally variable); induced-compliance dissonance (`contested`);
false consensus (`replicated`); Dunning–Kruger (`replicated` as a pattern; explanation `contested`); behavioural
priming of the elderly-walking kind (`failed`); power posing's hormonal and behavioural effects (`failed`; a
small effect on self-reported feeling remains); inverse-planning accounts of goal inference (`replicated`).
*In practice:* interviewing and performance review biases (Part 53), user research ("what people say against what
they do"), negotiation, AI systems that model users.
*Frontier:* what survives of social priming; theory of mind in language models (Part 60); computational models of
the self.
*Reading:* Festinger & Carlsmith 1959; Bem 1967; Heider 1958; Kelley 1973; Jones & Harris 1967; Kruger & Dunning
1999; Bargh, Chen & Burrows 1996; Doyen et al. 2012; Baker, Saxe & Tenenbaum 2009; Fiske & Taylor, *Social
Cognition*; Nisbett & Wilson 1977.

### Part 36 · Us and Them (~55)
*Question:* how little does it take to make a group, and what does a bias score mean?
*Story:* Henri Tajfel, who survived the war as a prisoner by concealing that he was a Polish Jew, wants to find
the minimum conditions for discrimination. He divides schoolboys by a meaningless preference between two
painters, and they favour their own group at once. From there the part asks how prejudice is measured, by
questionnaire, by reaction time, by sending out thousands of identical résumés, and which interventions change
behaviour, as opposed to scores.
1. Hook: Klee or Kandinsky (Tajfel et al. 1971). The allocation matrices.
2. On you: a minimal-group allocation.
3. Social identity and self-categorization; realistic conflict: the Robbers Cave camp (1954), as run and as
   staged, with its superordinate goals.
4. Stereotypes as categories (Part 22) with social consequences; the stereotype content model (warmth and
   competence); illusory correlation.
5. Measuring prejudice by asking: the decline in expressed prejudice; social desirability; list experiments.
6. Measuring it by speed: the Implicit Association Test (1998). What it is, its retest reliability near 0.5, its
   small correlations with behaviour, and the finding that changing the score does not change behaviour (2019).
   The best case for and against.
7. Measuring it in the field: audit studies. Identical résumés, different names (Bertrand and Mullainathan
   2004); the meta-analysis of thirty years of hiring audits. This is discrimination measured as behaviour.
8. Stereotype threat (Steele and Aronson 1995): the original finding and its covariate adjustment; publication
   bias; the large registered replication.
9. Contact: Allport's hypothesis; the meta-analysis; what randomized contact experiments show.
10. Reducing prejudice: what was tried and how little was tested in the field (Paluck and Green's reviews); the
    Rwandan radio experiment; diversity training's evidence.
11. Deep canvassing: a faked study exposed by the two students who tried to extend it (2015), who then ran the
    real experiment and found a durable effect (2016).
12. From bias to system: how small individual biases compound (computed), and the limits of individual-level
    explanation.

*Psyche:* `social`: group identity for the agents; an IAT model (a diffusion account of the D score) with planted
associations, showing what reliability does to prediction; a compounding-bias simulation.
*On you:* the minimal-group matrices.
*Ledger:* minimal-group favouritism (`replicated`); the IAT's group-level effects (`replicated`) and its use to
predict individuals (`failed`); hiring discrimination in audits (`replicated`; little decline for Black
applicants in the United States over twenty-five years); stereotype threat (`contested`, leaning `failed` in
registered tests); intergroup contact (`replicated`; causal evidence thinner); deep canvassing (`replicated`
after a `retracted` first report); Robbers Cave (`story and record`).
*In practice:* hiring audits and structured selection (Part 53), bias training and what to buy instead, fair-
lending and housing tests, algorithmic audits.
*Frontier:* what implicit measures measure (the bias-of-crowds account); field experiments at scale; measuring
structural effects.
*Reading:* Tajfel et al. 1971; Sherif et al. 1961; Greenwald, McGhee & Schwartz 1998; Oswald et al. 2013;
Forscher et al. 2019; Bertrand & Mullainathan 2004; Quillian et al. 2017; Steele & Aronson 1995; Pettigrew & Tropp
2006; Paluck, Green & Green 2019; Broockman & Kalla 2016.

### Part 37 · Bonds and Bargains (~50)
*Question:* why do people cooperate with strangers, and can a relationship be predicted?
*Story:* offer someone one dollar out of ten, take it or both get nothing. A rational recipient accepts. Most
people refuse, at a cost to themselves, and proposers know it. The part follows cooperation from two-person
bargains to groups, and then turns to the closest bonds, where a science of attraction meets machine learning
and finds how little can be predicted in advance.
1. Hook and On you: the ultimatum game (Güth et al. 1982).
2. Games as experiments: dictator, ultimatum, trust, prisoner's dilemma, public goods. What "rational" predicts
   and what people do (the theory is in *Philosophy, Built* Part 34).
3. Why cooperate: kin selection, reciprocity, reputation, punishment. Axelrod's tournament in one minute.
4. Public goods decay, and punishment sustains them (Fehr and Gächter 2002); antisocial punishment across
   societies.
5. Social preferences: inequity aversion as a utility function, fitted to game data; where it fails.
6. The same games in fifteen small-scale societies (Henrich et al. 2001): offers track market integration. A
   bridge to Part 38.
7. Attraction: proximity, familiarity (mere exposure), similarity, reciprocity. The matching hypothesis.
8. What people say they want against whom they choose: speed-dating studies (Eastwick and Finkel 2008).
9. Predicting relationships: machine learning on dozens of couples datasets; one's own perceptions predict,
   partner traits barely, and compatibility of a specific pair almost not at all (Joel et al. 2017, 2020).
10. Adult attachment; the investment model of commitment; what the "divorce prediction" studies did not do
    (out-of-sample testing).
11. Mate preferences across cultures: the thirty-seven-culture study (1989) and its forty-five-country
    replication; evolutionary and social-role readings.
12. Loneliness and health: the mortality meta-analyses, and the causal question.

*Psyche:* `social`: repeated-game players with inequity-averse utilities fitted to open game data; a public-goods
simulation with and without punishment; a cross-validated relationship predictor on simulated couples showing
why in-sample accuracy misleads.
*On you:* ultimatum offers and responses; a public-goods round against recorded players.
*Ledger:* ultimatum rejections (`replicated`); punishment sustaining cooperation (`replicated`); mere exposure
(`replicated`); stated-preference prediction of attraction (`failed`); high-accuracy divorce prediction
(`contested`: not cross-validated); sex differences in stated mate preferences (`replicated`); social isolation
and mortality (`replicated` association).
*In practice:* marketplace and reputation-system design, team incentives, dating products' claims, couple
therapy's evidence.
*Frontier:* partner-specific compatibility; cooperation with and among machines; causal effects of social
connection.
*Reading:* Güth, Schmittberger & Schwarze 1982; Fehr & Gächter 2002; Fehr & Schmidt 1999; Henrich et al. 2001;
Camerer, *Behavioral Game Theory*; Finkel et al. 2012; Joel et al. 2020; Buss 1989; Holt-Lunstad et al. 2010.

### Part 38 · Culture and Morals (~55)
*Question:* whose mind has psychology been describing?
*Story:* in 2010 three researchers count who takes part in psychology's experiments: overwhelmingly people from
Western, educated, industrialized, rich and democratic societies, who on many measures are outliers among
humans. Even the Müller-Lyer illusion varies. If the mind is partly made by culture, culture needs a theory, and
there is one, with equations. Morality is the test case: millions of people, hundreds of countries, one trolley.
1. Hook: the WEIRD paper (Henrich, Heine and Norenzayan 2010) and the count behind it (Arnett 2008).
2. A basic illusion varies: the Müller-Lyer across societies (Segall et al. 1966), and the dispute over why.
3. Independent and interdependent selves (Markus and Kitayama 1991); analytic and holistic attention (Nisbett);
   Hofstede's dimensions. How good are the measures (Part 3)?
4. Explanations: ecology and subsistence (the rice theory), relational mobility, kinship and institutions.
5. Method: translation, measurement invariance across cultures (Part 44), reference-group effects, samples of
   convenience.
6. Cultural evolution: culture as inheritance; biased transmission; the mathematics of conformity and prestige
   (Boyd and Richerson); cumulative culture and the transmission chain (computed).
7. On you: six trolley and footbridge cases.
8. Moral psychology: Kohlberg's reasoning; Haidt's dumbfounding and the intuitionist model; Greene's dual
   process and the scanner; moral foundations and their measurement.
9. Moral judgment at scale: the trolley in forty-two countries; the Moral Machine's forty million decisions;
   what is universal and what varies.
10. The origins of morality in infants: the helper and hinderer (2007) and its multi-laboratory replication
    **(verify)**.
11. Universals: what does hold across cultures (psychophysics, basic learning, much of memory), and how to
    report a finding's population.
12. A psychology of everyone: multi-site consortia across dozens of countries, and what they have found so far.

*Psyche:* `social`: cultural learners with conformist and prestige biases; a transmission chain that accumulates
or loses a skill with population size; a simple moral-judgment model fitted to open cross-cultural data.
*On you:* the trolley cases, then the published splits by country.
*Ledger:* WEIRD sampling (`replicated`; still true a decade on); cross-cultural variation in the Müller-Lyer
(`replicated`; cause `contested`); self-construal differences (`contested`: measures unreliable); the rice theory
(`contested`); the switch–footbridge difference (`replicated` across countries); moral foundations' factor
structure across cultures (`contested`); infant helper preference (`contested`).
*In practice:* localization of products and tests, global survey research, cross-cultural teams, value alignment
of AI systems.
*Frontier:* cultural distance as a measurable quantity; historical psychology from texts; whether language models
are WEIRD.
*Reading:* Henrich, Heine & Norenzayan 2010; Henrich, *The WEIRDest People in the World*; Markus & Kitayama 1991;
Nisbett 2003; Boyd & Richerson 1985; Haidt 2001; Greene et al. 2001; Awad et al. 2018, 2020; Segall, Campbell &
Herskovits 1966.

---

## Act X · When Minds Suffer

Each part of this act opens with the care card (§1.2).

### Part 39 · What Is a Disorder? (~55)
*Question:* where is the line between suffering and illness, and who draws it?
*Story:* in 1973 *Science* publishes a study in which eight healthy people report hearing a voice, are admitted
to psychiatric hospitals, and are never detected as sane. It helps force a revolution in diagnosis: explicit
criteria, checked for agreement between clinicians. Decades later a journalist looks for the eight and finds
reason to doubt the study. Reliability was won. Validity is still open, and the alternatives are mathematical.
1. Hook: "On Being Sane in Insane Places", and what the 2019 investigation found.
2. A short history: asylums, moral treatment, Kraepelin's two psychoses, Freud's neuroses, the anti-psychiatry
   critique.
3. Defining disorder: statistical rarity, distress, dysfunction, harm; Wakefield's harmful dysfunction;
   homosexuality's removal from the manual (1973) as a case of the definition at work.
4. Reliability: two clinicians, one patient. Cohen's kappa derived. The DSM-III (1980) and its criteria; the
   DSM-5 field trials' kappas, including major depression near 0.28.
5. Reliable is not valid: Robins and Guze's validators; heterogeneity (hundreds of symptom combinations meet one
   diagnosis); the scales that share few symptoms.
6. Categories or dimensions: taxometric evidence; most problems are continua with thresholds chosen by
   convention.
7. Comorbidity is the rule: internalizing and externalizing; the p factor (Part 32's mathematics again, with the
   same question about what a general factor is); HiTOP; the research domain criteria.
8. Disorders as networks: symptoms that cause each other (insomnia, fatigue, concentration, mood). An Ising
   model with hysteresis: why episodes start suddenly and end slowly (computed).
9. Epidemiology: prevalence, incidence, lifetime risk, the treatment gap; are rates rising?
10. On you: a screening test with 90% sensitivity for a 1% condition. The base-rate arithmetic (Part 12).
11. Clinical against statistical prediction: Meehl's "disturbing little book" (1954), the meta-analysis, and why
    simple formulas beat expert judgment (Dawes 1979).
12. Stigma, culture and idioms of distress; diathesis and stress as the frame for the next three parts.

*Psyche:* `clinic`: an Ising symptom network with a tipping point and hysteresis; a kappa simulator showing how
unreliable criteria cap validity; a comorbidity structure for the Pool.
*On you:* the base-rate problem in probabilities, then in natural frequencies.
*Ledger:* Rosenhan's study (`story and record`: serious doubts about the data); statistical beating clinical
prediction (`replicated`); the p factor (`replicated` statistically; meaning `contested`); candidate biomarkers
for diagnosis (`failed` so far).
*In practice:* diagnosis in clinics and insurance, screening programmes, risk tools; why a checklist score is not
a diagnosis.
*Frontier:* network against latent models (they can be statistically equivalent); idiographic networks from
experience sampling (Part 47); what a validated biological classification would require.
*Reading:* Rosenhan 1973; Cahalan, *The Great Pretender*; Kendell & Jablensky 2003; Regier et al. 2013; Caspi et
al. 2014; Kotov et al. 2017; Borsboom 2017; Meehl 1954; Dawes 1979; Wakefield 1992; Kendler's papers on
psychiatric nosology.

### Part 40 · Fear and Sadness (~55)
*Question:* what are anxiety and depression made of, and what do the treatments act on?
*Story:* dogs that received shocks they could not escape later lie down and take shocks they could escape. The
finding becomes a theory of depression, and fifty years later its own authors reverse it: passivity is the
default, and what is learned is control. The part builds anxiety and depression out of the learning and choice
models of Acts IV and V, and weighs what trials say about the drugs.
1. Hook: Seligman and Maier (1967), and the 2016 revision.
2. Anxiety as learning: fear conditioning (Part 16); Mowrer's two factors: fear is acquired by pairing and
   maintained by avoidance, which prevents extinction (computed: the loop that never unlearns).
3. Exposure: extinction as new learning explains relapse (renewal, reinstatement); inhibitory-learning
   principles for making exposure last.
4. The anxiety disorders in one frame: phobia, panic (catastrophic misinterpretation of bodily signals), social
   anxiety, generalized worry, OCD (compulsions as avoidance; goals and habits, Part 17), PTSD (memory, Part 21).
5. On you: a dot-probe trial. Attentional bias to threat, and why this task's scores are too unreliable to
   diagnose anyone (Part 3).
6. Depression: the symptoms; one disorder or many (Part 39).
7. Cognitive theory: Beck's triad; attributional style; rumination. Learned helplessness as a reinforcement
   learner with a low estimate of control (computed).
8. Reward: anhedonia as blunted prediction error or reduced effort; momentary mood as a running average of
   reward prediction errors (Rutledge et al. 2014), fitted.
9. The chemical story: reserpine, iproniazid, the monoamine hypothesis; what the 2022 umbrella review of
   serotonin did and did not show; that a drug works does not show the deficit.
10. Do antidepressants work? Kirsch's meta-analyses; the 2018 network meta-analysis of 522 trials (a real and
    modest average effect); the debate over who benefits.
11. Stress, life events and genes: Brown and Harris; diathesis–stress; the fallen gene-by-environment finding
    (Part 9).
12. Bipolar disorder and lithium (Cade 1949); suicide: what is known about risk, and why prediction of individual
    attempts is barely better than chance (told under §1.2).

*Psyche:* `clinic`: an avoidance loop on Part 16's learner; extinction with renewal; a helplessness learner; the
mood model fitted to open data.
*On you:* a dot-probe demonstration (unscored).
*Ledger:* exposure therapy's efficacy (`replicated`); renewal of extinguished fear (`replicated`); learned
helplessness (`replicated`; explanation revised); attentional-bias modification as treatment (`failed`); the
serotonin-deficit account (`failed` as stated); antidepressants beating placebo on average (`replicated`, small);
5-HTTLPR × stress (`failed`); suicide prediction from risk factors (`failed` at useful accuracy).
*In practice:* how exposure, behavioural activation and cognitive therapy map onto these models; prescribing
decisions; screening.
*Frontier:* depression subtypes; fast-acting treatments and what they imply about mechanism; computational
phenotyping (Part 59).
*Reading:* Maier & Seligman 2016; Mowrer 1947; Bouton 2002; Craske et al. 2014; Beck 1967; Clark 1986; Rutledge et
al. 2014; Cipriani et al. 2018; Moncrieff et al. 2022; Franklin et al. 2017; Barlow, Durand & Hofmann.

### Part 41 · Psychosis, Addiction and Development (~55)
*Question:* what happens when the machinery of inference and learning is set wrongly?
*Story:* a hollow mask of a face, seen from behind, looks convex to almost everyone: a prior strong enough to
overrule the eyes. Many people with schizophrenia see it as hollow. The part uses the series' own models as a
language for three kinds of condition: perception and belief with mis-weighted priors, learning systems captured
by a drug, and brains that develop along a different path.
1. Hook and On you: the hollow mask.
2. Schizophrenia: positive, negative and cognitive symptoms; course and outcome; the Genain quadruplets.
3. Dopamine: chlorpromazine (1952), the receptor-binding correlation with clinical dose, the revised dopamine
   hypothesis.
4. Aberrant salience (Kapur 2003): prediction errors firing at the irrelevant (Part 17), and delusion as the
   explanation a person builds.
5. Hallucination as inference: strong priors (Part 14) produce perception without input; conditioned
   hallucinations in voice hearers and non-hearers (Powers, Mathys and Corlett 2017). The model, and its critics.
6. Causes: heritability near 0.8; hundreds of common variants of tiny effect; complement gene C4 and synaptic
   pruning; cannabis, urbanicity and migration as risks; the "schizophrenogenic mother", a harm done by theory.
7. Addiction: from use to compulsion. Tolerance and withdrawal (Part 10); the reward system; incentive
   sensitization (Part 28); habits (Part 17); steep delay discounting.
8. Addiction as reinforcement learning gone wrong: a drug that produces a prediction error that cannot be
   learned away (Redish 2004), computed.
9. Environment: Rat Park and its uneven replications; the Vietnam veterans who stopped (Robins 1974);
   contingency management as operant conditioning that works.
10. Autism: Kanner and Asperger and their histories; the "refrigerator mother"; the fraudulent vaccine paper
    (1998, retracted 2010); theory of mind (Part 30), and perception with weaker priors (Pellicano and Burr
    2012); rising prevalence and what explains it; neurodiversity.
11. ADHD: what it is, heritability, stimulant medication's short-term efficacy and the long-term follow-up of the
    largest trial.
12. The transdiagnostic view: the same parameters (priors, learning rates, discounting) across diagnoses.

*Psyche:* `clinic`: Part 14's Bayesian observer with prior precision as a dial, run on the hollow mask and on a
conditioned-hallucination task; Part 17's agent with a non-compensable drug reward; a salience-misattribution
simulation.
*On you:* the rotating hollow mask.
*Ledger:* reduced hollow-mask illusion in schizophrenia (`replicated` in small samples); antipsychotic efficacy
for positive symptoms (`replicated`); strong-prior hallucinations (`contested`); Rat Park (`contested`);
contingency management (`replicated`); vaccines and autism (`retracted`; no association in studies of millions);
facilitated communication (`failed`).
*In practice:* early-intervention services, medication and its trade-offs, harm reduction, school and workplace
supports.
*Frontier:* whether "precision" accounts make distinct predictions; polygenic risk in practice; new mechanisms
for antipsychotics **(verify)**.
*Reading:* Kapur 2003; Howes & Kapur 2009; Powers, Mathys & Corlett 2017; Sterzer et al. 2018; Redish 2004;
Robinson & Berridge 1993; Robins 1974; Pellicano & Burr 2012; Frith, *Autism: Explaining the Enigma*; MTA
Cooperative Group 1999.

### Part 42 · Does Therapy Work? (~55)
*Question:* how would you know that talking to someone helped?
*Story:* in 1952 Hans Eysenck surveys the outcome studies and concludes that two-thirds of neurotic patients
recover with or without psychotherapy. The claim is infuriating and nearly impossible to answer without a method
for adding up studies. In 1977 Smith and Glass invent that method's use in psychology, meta-analysis, and answer
him. Then come the harder questions: compared with what, by which ingredient, and how much of the published
effect is real.
1. Hook: Eysenck's challenge.
2. On you: clients enter therapy at their worst and improve. Two graphs; which one shows the therapy working?
   Regression to the mean and natural recovery (computed on the Pool).
3. The trial: randomization, and the control problem. Waiting lists (which may make people worse), placebo
   therapy, treatment as usual; no blinding of the patient; researcher allegiance.
4. Meta-analysis is born: Glass (1976); Smith and Glass's 375 studies and an average effect of 0.68. A forest
   plot built study by study (the mathematics is Part 50).
5. The dodo bird: "everybody has won" (Rosenzweig 1936; Luborsky 1975). Common factors, the therapeutic alliance
   and its correlation near 0.28 with outcome; the case for specific ingredients (exposure for anxiety).
6. The therapies: behavioural methods (Part 40); cognitive therapy (Beck); the third wave; psychodynamic therapy
   and its trial evidence; DBT for self-harm (Linehan 1991).
7. Medication against therapy against both; relapse after stopping.
8. How big is it really? Publication bias in antidepressant trials (94% positive in journals, 51% at the
   regulator); the same correction applied to psychotherapy trials; effects against waiting list, against
   placebo, against usual care.
9. Clinical significance: the reliable change index and the recovered proportion (Jacobson and Truax 1991),
   derived.
10. Treatments that harm: critical-incident debriefing, "scared straight", recovered-memory techniques, conversion
    therapy.
11. The history of the body treatments: lobotomy and a Nobel Prize (1949); ECT then and now.
12. The dose–response curve of sessions; who does not respond; the treatment gap (to Part 57).

*Psyche:* `clinic`: a therapy-trial simulator on the Pool (natural recovery, regression to the mean, control-
condition choice, allegiance, publication filter); a random-effects meta-analysis by hand; the reliable change
index.
*On you:* the two-graphs problem.
*Ledger:* psychotherapy beats no treatment (`replicated`); the published effect size (`replicated, smaller` after
bias correction); equivalence of bona fide therapies (`contested`); the alliance–outcome correlation
(`replicated`; causal direction `contested`); debriefing after trauma (`failed`, possibly harmful).
*In practice:* how treatment guidelines are written; choosing a therapy; outcome monitoring.
*Frontier:* mechanisms of change; personalized treatment selection (Part 59); psychedelic-assisted therapy and
the unblinding problem.
*Reading:* Eysenck 1952; Smith & Glass 1977; Wampold & Imel, *The Great Psychotherapy Debate*; Cuijpers et al.
2010, 2019; Turner et al. 2008; Jacobson & Truax 1991; Lilienfeld 2007; Linehan et al. 1991; Flückiger et al.
2018; Valenstein, *Great and Desperate Cures*.

### Part 43 · The Replication (the capstone, ~50)
*Question:* can you run a study that deserves to be believed?
*Story:* the degree ends as a degree does, with a project. The part takes one classic effect from the Ledger and
replicates it properly, on screen, from the choice of target to the report. The viewer is a participant. Nothing
about the result is known when the script is written: the narration is templated over the data, and the plan
commits in advance to what each outcome would mean.
1. Hook: a row of the Ledger marked `not directly tested`. Choosing a target: importance, uncertainty,
   feasibility. Two targets are run: one expected to hold (a Stroop variant) and one in doubt.
2. What counts as the same study: direct and conceptual replication; contacting the original authors; materials.
3. The smallest effect of interest; power analysis; the "small telescopes" rule; the sample size, justified.
4. Preregistration, written on screen: hypotheses, exclusion rules, the analysis script run on simulated data
   from the Pool before any real data exist.
5. Building the experiment: the trial strip, counterbalancing, attention checks, browser timing validation.
6. Ethics and consent; what participants are told.
7. Data collection: the viewer takes part on the site; the film uses an open multi-site dataset for the same
   paradigm so that its numbers are real and fixed.
8. The confirmatory analysis, exactly as registered. Effect size and interval.
9. Was it a replication? Three criteria (significance, the original inside the interval, small telescopes) can
   disagree; a replication Bayes factor.
10. Exploratory analysis, labelled; robustness (a small multiverse).
11. The report: a registered-report layout; open data and code.
12. The degree: the Ledger so far, the Homunculus so far, and the entry points to Acts XI, XII and XIII.

*Psyche:* the capstone pipeline: preregistration as code, a simulated run on the Pool, the frozen analysis
applied to open multi-site data; the report generated from the result.
*On you:* take part in the replication on the site.
*Ledger:* the two target effects, with this part's estimate added to their rows.
*In practice:* this is the workflow of a product experiment or a clinical trial: decide the analysis before the
data.
*Frontier:* what a failed replication licenses; hidden moderators; replication at scale by many small labs.
*Reading:* Simonsohn 2015; Brandt et al. 2014 (the replication recipe); Lakens 2022 (sample size justification);
Nosek & Errington 2020; Chambers & Tzavella 2022; Zwaan et al. 2018.

---

## Act XI · The Graduate Toolkit

These seven parts are the quantitative sequence of a psychology PhD. They assume calculus, linear algebra and
probability, and lean on *Statistics, Built* (named per part) for the general theory; what is taught here is the
psychological use and the psychological trap. Every method is graded on the Pool.

### Part 44 · Latent Variables (~55)
*Question:* how do you model something you cannot observe, and how do you know the model is not a fiction?
*Story:* in 1921 the geneticist Sewall Wright draws arrows between variables and shows how correlations follow
from the arrows. Half a century later Karl Jöreskog joins Wright's paths to Spearman's factors, and the
structural equation model becomes psychology's standard way to state a theory about unobservables. Its standard
abuse is to forget that very different diagrams fit the same data.
1. Hook: one correlation matrix, three diagrams that fit it equally (returned to at the end).
2. Path analysis: Wright's tracing rules derived; a correlation as a sum over paths.
3. From exploratory to confirmatory factor analysis: the model Σ = ΛΦΛᵀ + Θ; identification (scaling, the
   three-indicator rule, counting parameters).
4. Estimation: the maximum-likelihood discrepancy function, derived and minimized with the series' autodiff;
   Holzinger and Swineford's 1939 scores fitted.
5. Fit: the χ² test and why it "always rejects"; RMSEA, CFI, SRMR; where the conventional cut-offs came from and
   why fixed cut-offs mislead (dynamic cut-offs).
6. The full model: measurement plus structure; latent regressions corrected for unreliability (Part 3's
   attenuation, done properly).
7. Measurement invariance: configural, metric, scalar. What must hold before two groups' means can be compared
   (owed since Parts 32 and 38).
8. Mediation: Baron and Kenny (1986), the product of coefficients, bootstrapped intervals; and why a mediation
   analysis of an experiment is still a correlational claim about the mediator (sequential ignorability; link to
   *Statistics, Built* Part 36).
9. Equivalent models: the diagrams of chapter 1; rules for generating them; why fit cannot choose.
10. Longitudinal models: latent growth curves; the cross-lagged panel model and its repair (to Part 47).
11. Factors against networks: a one-factor model and a fully connected network can imply the same covariances.
    What would distinguish them (interventions, time).
12. Reporting standards, and a checklist for reading an SEM paper.

*Psyche:* `psyche.sem`: path models, CFA and SEM by ML on the series' autodiff, checked against a reference
implementation on the Holzinger–Swineford data; fit indices; invariance tests; equivalent-model generation;
everything run on Pool data with a known generating model.
*On you:* three data-generating stories and one matrix: draw a model that fits as well as the "true" one.
*Ledger:* famous mediation claims whose mediators failed when manipulated; statistical equivalence of factor and
network models (`replicated` as mathematics).
*In practice:* survey analytics, test validation, people analytics, marketing mix and attitude models; the
question to ask: what alternative diagram fits equally?
*Frontier:* causal discovery from psychological data and its assumptions; Bayesian SEM and small-sample
behaviour; dynamic fit.
*Reading:* Wright 1921; Jöreskog 1969; Bollen 1989; Kline, *Principles and Practice of Structural Equation
Modeling*; Hu & Bentler 1999, with McNeish & Wolf 2023; MacCallum et al. 1993; Meredith 1993; Bullock, Green & Ha
2010; Rohrer 2018; *Statistics, Built* Parts 31 and 36.

### Part 45 · Item Response Theory (~55)
*Question:* how can two people who took different questions be put on the same scale?
*Story:* in the 1950s the Danish mathematician Georg Rasch is asked to compare reading ability across tests that
share no items. Classical test theory cannot: a score depends on which test was taken. Rasch models the single
encounter of one person with one item, and the person and the item separate. From that model come adaptive tests
that ask each person different questions, a statistical definition of an unfair item, and a way to track what a
student knows.
1. Hook and On you: a ten-item adaptive test picks each next item from your last answer, and stops when it is
   sure enough (a demonstration, unscored).
2. What classical theory cannot do (Part 3): sample-dependent difficulty, test-dependent scores, one standard
   error for everyone.
3. The Rasch model: P(correct) as a logistic function of ability minus difficulty; specific objectivity; the sum
   score is sufficient (derived).
4. Two and three parameters: discrimination, guessing (Birnbaum; Lord). Item characteristic curves.
5. Information: each item informs most near its own difficulty; test information; the standard error as a
   function of ability (derived as Fisher information; link to *Statistics, Built* Part 9).
6. Estimation: joint, conditional and marginal maximum likelihood by EM; Bayesian ability estimates.
7. Adaptive testing: choose the most informative item, update, stop. The same precision in half the items
   (computed on the Pool); exposure control and item pools.
8. Polytomous items: the graded response and partial credit models for rating scales (Part 46).
9. Fairness as a statistic: differential item functioning. Matching on ability; Mantel–Haenszel and likelihood-
   ratio DIF; the difference between item bias and group difference.
10. Linking and equating: putting this year's test on last year's scale.
11. Large-scale assessment: matrix sampling and plausible values (why a national survey does not give each
    student a score).
12. Tracking learning: Bayesian knowledge tracing (Corbett and Anderson 1995) as a hidden Markov model; Elo for
    learners and items; deep knowledge tracing against the simple model.

*Psyche:* `psyche.irt`: Rasch to 3PL and graded response; marginal ML by EM (reusing `statkit.evals`' 2PL where it
fits); information functions; a CAT engine; DIF tests; knowledge tracing. Graded on Pool abilities.
*On you:* the adaptive test on generated matrix items; watch your interval narrow.
*Ledger:* adaptive tests matching fixed-form precision with fewer items (`replicated`); deep knowledge tracing's
large gains over simple models (`replicated, smaller` once baselines were tuned).
*In practice:* admissions and licensing exams, language tests, clinical short forms, adaptive learning
platforms; evaluating AI systems with IRT (*Statistics, Built* Part 64).
*Frontier:* response-time IRT joining Part 25's models to testing; items generated by language models and their
calibration; measurement of rapidly learning systems.
*Reading:* Rasch 1960; Lord 1980; Lord & Novick 1968 (Birnbaum's chapters); Embretson & Reise 2000; van der
Linden (ed.), *Handbook of Item Response Theory*; Holland & Wainer (eds.), *Differential Item Functioning*; Corbett
& Anderson 1995; Mislevy 1991.

### Part 46 · Scaling, Surveys and Choice (~55)
*Question:* how do you turn "I prefer this one" into a number, and what happens between a question and its
answer?
*Story:* in 1927 Louis Thurstone asks students which of two crimes is more serious, for every pair, and derives a
scale of seriousness from the inconsistencies. R. Duncan Luce later replaces Thurstone's normal curves with a
single axiom. From those two men comes the logit model that prices products and predicts commutes, and the
discovery that preferences bend with the menu.
1. Hook: Thurstone's crimes. On you: twelve paired comparisons.
2. The law of comparative judgment (Case V): discriminal processes, choice proportions to scale values (derived;
   it is signal detection, Part 12, between two stimuli).
3. Luce's choice axiom (1959): independence from irrelevant alternatives implies a ratio scale. Bradley–Terry–
   Luce, fitted by the MM algorithm (link to `statkit.optim`).
4. Random utility: Gumbel noise gives the logit (derived); McFadden's conditional logit and the BART forecast.
5. Where the axiom fails: red bus and blue bus; similarity, attraction (the decoy) and compromise effects. On
   you: the decoy.
6. Models of context effects: elimination by aspects; sequential-sampling accounts (Part 25's accumulators with
   several options).
7. Conjoint analysis: decomposing a product into attributes; designs, part-worths, willingness to pay, market
   simulation; MaxDiff.
8. The survey response process (Tourangeau): comprehend, retrieve, judge, report. A model of each failure.
9. Question effects: wording, order, scale anchors; acquiescence; social desirability; satisficing (Krosnick).
10. Rating scales: Likert's method (1932); the number of points; response styles, and separating style from
    trait (Part 45's graded model).
11. Data quality online: careless responding, bots, panel conditioning; attention checks and their side effects.
12. One number to rule them all: the net promoter score against its evidence.

*Psyche:* `psyche.scaling`: Thurstone Case V; BTL; multinomial and mixed logit; a conjoint designer and
estimator with recovery of planted part-worths on the Pool; a response-process simulator with satisficing and
acquiescence.
*On you:* your own scale from paired comparisons; the decoy effect.
*Ledger:* the attraction (decoy) effect (`replicated` with numerical attributes; weaker with realistic stimuli);
question-order and wording effects (`replicated`); acquiescence (`replicated`); the net promoter score as the best
predictor of growth (`failed`).
*In practice:* pricing and product research, survey design, public-opinion polling (with *Statistics, Built* Part
18 for sampling), rating systems and leaderboards.
*Frontier:* conjoint for causal questions in political science; preference learning in recommender systems;
language models as survey respondents (Part 60).
*Reading:* Thurstone 1927; Luce 1959; McFadden 1974; Tversky 1972; Huber, Payne & Puto 1982; Train, *Discrete
Choice Methods with Simulation*; Green & Srinivasan 1990; Tourangeau, Rips & Rasinski 2000; Krosnick 1991; Likert
1932.

### Part 47 · People over Time (~55)
*Question:* when is a finding about people a finding about a person?
*Story:* in 1973 Herbert Clark points out that a generation of psycholinguistics has tested whether effects
generalize to new people but not to new words. The fix, treating both as samples, took thirty years to become
routine. The deeper version of his point is the hardest in the series: a relation that holds across people need
not hold within any one of them, and psychology's theories are mostly about the second.
1. Hook: the language-as-fixed-effect fallacy. A simulated priming study with twenty items and a false-positive
   rate several times the nominal 5% (computed).
2. Repeated measures: why averaging over trials throws away the structure; the multilevel model as regressions
   within regressions.
3. Random intercepts and slopes; partial pooling and shrinkage (link to *Statistics, Built* Part 25,
   `statkit.mixed`).
4. Crossed random effects for participants and stimuli; "keep it maximal" against parsimony; what convergence
   failures mean.
5. Stimuli are a sample too: generalizing beyond the twenty faces or the twelve vignettes (Judd, Westfall and
   Kenny; the generalizability crisis).
6. Growth: individual trajectories (Part 31) as a multilevel model; time-varying predictors.
7. On you: one cloud of points with a positive slope overall and a negative slope within every person. Simpson's
   paradox inside psychology.
8. Within against between: person-mean centring; the ecological fallacy at the scale of one mind.
9. Ergodicity (Molenaar 2004): when group statistics equal individual statistics, and how rarely the conditions
   hold; the empirical gap between group and individual variation (Fisher et al. 2018).
10. Intensive longitudinal data: experience sampling; autoregression and inertia; person-specific networks.
11. Cause over time: the cross-lagged panel model's artefacts and the random-intercept repair (Hamaker et al.
    2015).
12. Tipping points: critical slowing down as an early warning before a transition into depression; the single-
    case evidence and its limits (Part 39's network, now in time).

*Psyche:* mixed models on the Pool with `statkit.mixed`: false-positive rates with and without item effects;
shrinkage of individual slopes; a population built to be non-ergodic; cross-lagged artefacts reproduced and
repaired.
*On you:* the within-and-between plot; guess the sign for one person.
*Ledger:* item-as-fixed-effect inflation (`replicated` as arithmetic); findings that reverse within persons
(examples from the frontier sweep); early-warning signals before depression (`contested`).
*In practice:* user-level against aggregate product metrics, personalized health and learning, any dashboard that
reads individual advice off a cross-section.
*Frontier:* idiographic science at scale; how many stimuli and occasions a claim needs; combining wearable
streams with models.
*Reading:* Clark 1973; Baayen, Davidson & Bates 2008; Barr et al. 2013; Judd, Westfall & Kenny 2012; Yarkoni
2022; Molenaar 2004; Fisher, Medaglia & Jeronimus 2018; Hamaker, Kuiper & Grasman 2015; Kievit et al. 2013; Bolger
& Laurenceau, *Intensive Longitudinal Methods*.

### Part 48 · Modelling Behaviour (~60)
*Question:* when is a computational model of the mind more than a curve fit?
*Story:* in 1956 William Estes shows that a smooth, gradual learning curve can be the average of animals who each
learned in a single jump. The average describes no one. Models of behaviour are fitted to data from many people,
many trials and many possible mechanisms, and this part is the craft of not fooling yourself with them. It
rebuilds the fitting harness that every earlier part used, in the open.
1. Hook: Estes's curves. The power law of practice as an averaging artefact.
2. What a cognitive model is: a generative program from parameters to trial-level data. The series' models,
   listed with their likelihoods.
3. Fitting: maximum likelihood; local minima; when to simulate instead (likelihood-free methods).
4. Parameter recovery: simulate, fit, compare. The heat map every modelling paper should show (done here for
   Parts 16, 17, 25 and 26's models).
5. On you: your bandit data from Part 17, fitted, with the recovery plot beside it. How much should you trust
   your learning rate?
6. Identifiability and sloppiness: parameters that trade off (learning rate and inverse temperature).
7. Model comparison: likelihood ratios, AIC and BIC, cross-validation, Bayes factors, random-effects model
   selection over a group; model recovery and the confusion matrix (link to *Statistics, Built* Part 28).
8. A good fit can be bad: flexibility and what a model rules out (Roberts and Pashler 2000); falsification by
   posterior prediction: does the winning model produce the qualitative effect?
9. Hierarchical Bayes: people as draws from a population; shrinkage of individual parameters; a hierarchical
   diffusion model fitted with the series' own sampler (`statkit.ppl`).
10. Levels again: rational analysis (Anderson 1990: derive behaviour from the problem) and resource-rational
    analysis (optimal use of limited computation).
11. Connectionism: PDP (1986); what networks added (graded, learned representations) and what they cost
    (interpretability; catastrophic interference, Part 21).
12. Language models as cognitive models: giving a model the Battery; fine-tuned "foundation models of cognition"
    **(verify)** and the argument over whether prediction is explanation (to Parts 60 and 61).

*Psyche:* `psyche.fit`: likelihoods for the series' models; optimizers with restarts; parameter- and model-
recovery harnesses; hierarchical Bayesian fits; posterior predictive checks; the model zoo's confusion matrix.
*On you:* the fit to your own data.
*Ledger:* model-based parameters as stable traits (`contested`: low retest reliability, parameters that do not
generalize across tasks); the power law of practice at the individual level (`failed`: exponential fits better).
*In practice:* computational phenotyping, user modelling, simulation-based product testing, cognitive models
inside tutoring systems.
*Frontier:* amortized inference; automated model discovery; what a foundation model of behaviour would need to
show.
*Reading:* Estes 1956; Heathcote, Brown & Mewhort 2000; Farrell & Lewandowsky 2018; Wilson & Collins 2019; Lee &
Wagenmakers 2013; Roberts & Pashler 2000; Pitt & Myung 2002; Palminteri, Wyart & Koechlin 2017; Anderson 1990;
Lieder & Griffiths 2020; Rumelhart, McClelland & the PDP Group 1986.

### Part 49 · Modelling the Brain's Data (~55)
*Question:* what must be true for a brain map to be evidence?
*Story:* in 2020 seventy research teams are given the same brain-imaging dataset and the same nine hypotheses. No
two teams choose the same analysis pipeline, and for several hypotheses their yes-or-no answers split. Part 8
built the measurement chain. This part builds the analysis chain on a synthetic brain where the truth is known,
and then asks the question that reorganized the field: how many people does a brain–behaviour correlation need?
1. Hook: the seventy teams (NARPS). On you: count the forks in a standard pipeline.
2. Preprocessing: motion, slice timing, registration, smoothing. Head motion as a confound that created
   findings.
3. The mass-univariate model at depth: first and second levels; random effects; contrasts.
4. Thresholds at depth: Gaussian random fields, cluster-extent inference and its failure, permutation tests,
   FDR (link to *Statistics, Built* Part 33).
5. Patterns: multivariate decoding (Haxby et al. 2001); cross-validation and the ways to leak; what decodability
   does and does not show.
6. Geometry: representational similarity analysis; comparing a brain region, a model and behaviour through
   their distance matrices (Part 22's psychological space, in neurons).
7. Encoding models: predict voxels from features of the stimulus; noise ceilings; semantic maps of cortex.
8. Connectivity: resting-state networks and the default mode; graph measures; what correlation between regions
   can mean.
9. EEG and MEG analysis: ERPs at depth, time–frequency, source estimation; "double dipping" in time windows.
10. Populations of neurons: the population vector, dimensionality reduction, neural manifolds and dynamics.
11. Reading out: brain–computer interfaces from cursor control to speech decoding **(verify)**; what they decode
    (motor intention) and what they do not (thoughts at large).
12. The sample-size reckoning: brain-wide association studies need thousands; task-fMRI reliability; and the
    parable of the microprocessor analysed with neuroscience's methods (Jonas and Kording 2017).

*Psyche:* `psyche.neurodata`: a synthetic brain with planted effects; the pipeline with switchable choices
(a multiverse of several hundred paths); decoding with and without leakage; RSA and encoding models against a
known representation; a brain–behaviour correlation's sampling variability at n = 25 and n = 2,500.
*On you:* the fork count.
*Ledger:* analytic variability changing conclusions (`replicated`); the default-mode network (`replicated`);
small-sample brain–behaviour correlations (`failed` at scale); cluster inference at lenient thresholds
(`failed`); category decoding from ventral cortex (`replicated`).
*In practice:* clinical imaging pipelines, BCI engineering, neurotechnology claims and how to audit them.
*Frontier:* foundation models of brain activity; naturalistic stimuli; individual-specific mapping with hours of
data per person.
*Reading:* Botvinik-Nezer et al. 2020; Poldrack, Mumford & Nichols 2011; Haxby et al. 2001; Kriegeskorte, Mur &
Bandettini 2008; Naselaris et al. 2011; Huth et al. 2016; Marek et al. 2022; Elliott et al. 2020; Jonas & Kording
2017; Luck 2014.

### Part 50 · The Weight of Evidence (~60)
*Question:* what does a whole literature say, and can it be trusted to say it?
*Story:* a regulator holds the registered results of seventy-four antidepressant trials. About half are positive.
In the journals, nearly all are. Part 4 told the crisis as a story; this part is the mathematics of reading a
literature that has been filtered, the forensic tools that caught the impossible numbers, and the argument that
the deepest problem was never statistics but theory. The Ledger is audited with its own tools.
1. Hook: the two piles of trials (Turner et al. 2008).
2. Combining studies: fixed and random effects, inverse-variance weights, heterogeneity (τ², I², prediction
   intervals), derived (link to *Statistics, Built* Part 25, `statkit.shrink`).
3. Moderators and meta-regression, and their low power.
4. Seeing the filter: funnel plots and Egger's test; what else makes a funnel asymmetric.
5. Correcting for it: trim-and-fill, PET-PEESE, selection models, p-curve, z-curve. Each run on simulated
   literatures from the Pool with a known truth: none works everywhere.
6. Meta-analyses against registered multi-site replications of the same effects: the meta-analytic estimates
   were about three times larger (Kvarven et al. 2020).
7. Designs that remove the filter: registered reports (about 44% positive results against 96% in the standard
   literature); multi-site protocols; sequential and Bayesian stopping rules.
8. On you: GRIM. Given n = 28 and integer answers, can the mean be 5.19? Forensic statistics: GRIM, SPRITE,
   statcheck (about half of papers had at least one inconsistent p-value), and what they found.
9. Fraud cases as method: how fabricated data were detected in spreadsheets (the dishonesty studies, 2021–23
   **(verify)**).
10. Many analysts, one dataset: twenty-nine teams and the red cards; multiverse and specification-curve analysis.
11. The theory crisis: Meehl again; weak theories make weak tests; formal theory, strong inference, and the
    generalizability critique.
12. The Ledger audited: its rows by subfield, original against replication effect sizes, and what predicted
    survival (sample size, effect size, surprise).

*Psyche:* `psyche.meta`: random-effects meta-analysis; every bias-correction method graded on simulated
literatures (reusing `statkit.multiple`'s p-curve and Egger/PET tools); GRIM and SPRITE; a specification-curve
engine; the Ledger's own summary statistics.
*On you:* the GRIM test on five reported means.
*Ledger:* audited as a whole; replication-rate estimates by project; the high-replicability claim of 2023 that was
itself retracted **(verify)**.
*In practice:* evidence reviews for policy and medicine, due diligence on vendor claims, internal experiment
archives and their own file drawers.
*Frontier:* whether replication rates have risen; automated error detection; incentives modelled as evolution
(to Part 61).
*Reading:* Borenstein et al., *Introduction to Meta-Analysis*; Turner et al. 2008; Carter et al. 2019; Kvarven,
Strømland & Johannesson 2020; Scheel, Schijen & Lakens 2021; Brown & Heathers 2017; Nuijten et al. 2016;
Silberzahn et al. 2018; Steegen et al. 2016; Meehl 1978, 1990; Oberauer & Lewandowsky 2019; Yarkoni 2022.

---

## Act XII · Psychology at Work

Each part of this act is organized around decisions a practitioner makes, opens with a failure or a success in
the field, and ends with a worked case in the style of that profession. Facts about products, laws and prices are
dated on screen ("as of …").

### Part 51 · Human Factors (~55)
*Question:* when a person makes a fatal error with a machine, whose error is it?
*Story:* in 1947 Paul Fitts and Richard Jones collect 460 "pilot errors" and find the same ones again and again:
in some aircraft the flap and landing-gear levers sit side by side and feel identical. Alphonse Chapanis has
already fixed it with a wheel-shaped knob and a flap-shaped knob. Human factors begins with the idea that error
is designed in, and it now has to deal with machines that fly themselves until they cannot.
1. Hook: the B-17 and the shape-coded knob.
2. Design-induced error: stimulus–response compatibility, population stereotypes, coding of controls and
   displays.
3. Slips, lapses and mistakes (Norman; Reason); skills, rules and knowledge (Rasmussen).
4. Three Mile Island (1979): an indicator that showed the command and not the valve.
5. Attention at work: multiple resources (Wickens); workload and how to measure it (NASA-TLX, secondary tasks,
   physiology).
6. On you: Mackworth's clock for ninety seconds. Vigilance falls within minutes; the SDT account (Part 12):
   sensitivity or criterion?
7. Rare targets: the prevalence effect in baggage and cancer screening; a gorilla in a lung scan missed by most
   radiologists.
8. Situation awareness (Endsley's three levels) and how it is measured.
9. Automation: levels of automation; the ironies of automation (Bainbridge 1983): the more reliable the system,
   the less practised the human who must take over. Mode confusion; Air France 447.
10. Trust in automation: calibration, misuse and disuse; alarm fatigue as a criterion placed by an engineer.
11. Systems: the Swiss cheese model; the checklist and its trial evidence in surgery and intensive care; crew
    resource management after Tenerife.
12. Fatigue (Part 10) as a quantified risk: hours awake against blood-alcohol equivalents.

*Psyche:* `psyche.work`: an operator model built from Parts 12, 18 and 25 (vigilance decrement, prevalence-driven
criterion shift, takeover reaction time after automation); an alarm-threshold optimizer.
*On you:* the vigilance clock.
*Ledger:* the vigilance decrement (`replicated`); the prevalence effect (`replicated`); surgical checklists
reducing complications (`replicated` in the original multi-site study; smaller or absent under mandate,
`contested`); automation complacency (`replicated`).
*In practice:* aviation, medical devices, control rooms, vehicle automation; the human-factors section of a
safety case; a worked takeover-request design.
*Frontier:* supervising learning-based automation; driver monitoring; human factors of AI assistants in
high-stakes work.
*Reading:* Fitts & Jones 1947; Chapanis, Garner & Morgan 1949; Wickens et al., *Engineering Psychology and Human
Performance*; Reason, *Human Error*; Bainbridge 1983; Endsley 1995; Parasuraman, Sheridan & Wickens 2000; Wolfe et
al. 2005; Haynes et al. 2009; Dekker, *The Field Guide to Understanding Human Error*.

### Part 52 · Designing for Minds (~55)
*Question:* can you predict how long a person will take to use something before it is built?
*Story:* in the late 1980s a telephone company is about to buy new operator workstations expected to save two
seconds a call. A team models the operator's perception, cognition and keystrokes on paper and predicts that the
new design will be slower. The field trial agrees with the model. Project Ernestine is the claim of this part:
enough psychology is quantitative to do engineering with.
1. Hook: Project Ernestine (Gray, John and Atwood 1993).
2. The Model Human Processor (Card, Moran and Newell 1983): three processors with cycle times, drawn from Acts
   III and V.
3. GOMS and the keystroke-level model: operators with durations; predicting a task's time by adding them.
4. On you: point and click at targets of different sizes and distances. Your Fitts's law line; throughput in
   bits per second.
5. Fitts and Hick in the interface: edges and corners, menu depth against breadth; where Hick's law does not
   apply.
6. Information foraging: users as foragers following scent (Pirolli and Card 1999; the marginal value theorem).
7. Gulfs of execution and evaluation; affordances and signifiers (Norman).
8. Usability testing: five users and the 1 − (1 − p)ⁿ curve, its assumptions and its critics; standard
   questionnaires; when to run an experiment instead (link to *Computer Science, Built* Part 44).
9. Seeing data: graphical perception (Cleveland and McGill 1984): position beats length beats angle beats area;
   Stevens's exponents (Part 11) for area and volume; preattentive features (Part 18).
10. Accessibility as psychophysics: contrast (Part 13), colour-vision deficiency, text size, motor tolerances.
11. Habit and attention by design: variable-ratio schedules (Part 16) in products; how habits form (a median of
    about sixty-six days in one study, with a wide range); dark patterns catalogued.
12. Conversational and AI interfaces: expectation, trust and repair (to Part 60).

*Psyche:* `psyche.work`: a keystroke-level predictor assembled from the Battery's fitted parameters; a Fitts and
steering-law pointing model; an information-foraging agent on a site graph.
*On you:* the pointing task; rank five chart types by your own estimation error.
*Ledger:* Fitts's law (`replicated`; one of the most robust quantitative laws in psychology); the graphical-
perception ranking (`replicated`, including online); "five users are enough" (`contested`); the twenty-one-day
habit claim (`failed`).
*In practice:* UX research and quantitative UXR, design systems, accessibility standards, data-visualization
practice; a worked keystroke-level analysis of a checkout form.
*Frontier:* computational models that simulate users end to end; reinforcement-learning users for design
optimization; evaluating interfaces to language models.
*Reading:* Card, Moran & Newell 1983; Gray, John & Atwood 1993; MacKenzie 1992; Pirolli & Card 1999; Norman,
*The Design of Everyday Things*; Nielsen & Landauer 1993; Cleveland & McGill 1984; Heer & Bostock 2010; Lally et
al. 2010; Mathur et al. 2019.

### Part 53 · People at Work (~60)
*Question:* how well can anyone predict who will be good at a job?
*Story:* in 1924 researchers at the Hawthorne plant raise the lighting and output rises; they lower it and output
rises again. The story of an effect of being observed outlived the data, which on reanalysis barely show it. The
real history of work psychology is less romantic and more useful: the correlation between a hiring method and
later performance, estimated across a century, revised sharply in 2022.
1. Hook: Hawthorne, as told and as reanalysed.
2. The 1917 Army tests and the birth of mass testing (Part 32's history); Münsterberg and scientific management.
3. Validity: correlating a predictor with performance. The criterion problem: what is job performance, and who
   rates it? Rater idiosyncrasy.
4. On you: two candidates, an interview impression and a test score. Whom do you hire? Then the base rates of
   being right.
5. Why observed validities understate and overstate: sampling error, unreliability (Part 3), range restriction
   (derived, simulated on the Pool).
6. A century of evidence: the 1998 summary (ability tests and work samples near 0.5) and the 2022 revision
   (structured interviews at the top near 0.4, ability near 0.3) after range-restriction corrections were
   rethought.
7. Interviews: why unstructured ones add noise and feel informative; structure as the fix.
8. Utility: from a validity coefficient to money. Taylor–Russell tables; the Brogden–Cronbach–Gleser formula
   (derived); selection ratio and base rate.
9. Fairness: adverse impact and the four-fifths rule; *Griggs* (1971); differential prediction; the validity–
   diversity trade-off as a Pareto frontier (computed).
10. Algorithms in hiring: résumé screens that learned the past; audits and bias-audit laws.
11. Motivation and pay (Part 28): goal setting; pay for performance (a glass-installation firm's 44% gain) and
    crowding out (a fine that increased late pick-ups).
12. Satisfaction, teams and leadership: satisfaction and performance correlate near 0.3; psychological safety;
    what randomized trials say about working from home.

*Psyche:* `psyche.work`: a selection simulator on the Pool (validity, range restriction, selection ratio, utility
in currency, adverse impact and the trade-off frontier); an interview-noise model.
*On you:* the hiring choice.
*Ledger:* the Hawthorne effect in the original data (`story and record`); validity of structured over
unstructured interviews (`replicated`); the size of ability-test validity (`contested` since 2022); goal-setting
effects (`replicated`); the crowding-out daycare result (`not directly tested` at scale).
*In practice:* talent assessment, people analytics, compensation design, engagement surveys (Part 46); a worked
selection-system design with its utility and adverse-impact analysis.
*Frontier:* validity of game-based and language-model-scored assessments; performance measurement without
ratings; remote and hybrid work evidence **(verify)**.
*Reading:* Roethlisberger & Dickson 1939, with Levitt & List 2011; Schmidt & Hunter 1998; Sackett et al. 2022;
Cronbach & Gleser 1965; Highhouse 2008; Dana, Dawes & Peterson 2013; Judge et al. 2001; Edmondson 1999; Lazear
2000; Gneezy & Rustichini 2000; Bloom et al. 2015.

### Part 54 · The Science of Learning (~55)
*Question:* what is the most effective way to learn something, and why do learners choose the opposite?
*Story:* in 1984 Benjamin Bloom reports that students tutored one to one perform two standard deviations above
those in a classroom, and challenges education to find group methods as good. Forty years on, the two sigma has
shrunk on replication, and the methods with the strongest evidence are ones students rate as less effective than
rereading. Memory research (Parts 20 and 21) becomes an engineering problem: schedule the next review.
1. Hook: Bloom's two sigma, and what later tutoring trials found.
2. On you: at the start of this part you studied two lists, one massed and one spaced. The test is now.
3. Retrieval practice: the testing effect in classrooms.
4. Spacing and interleaving: why mixed practice feels worse and works better.
5. Learning against performance (Bjork): desirable difficulties, and the illusion of fluency. Students in active
   classes learn more and feel they learned less.
6. Ten techniques ranked (Dunlosky et al. 2013): highlighting and rereading at the bottom.
7. Cognitive load: worked examples, split attention, the expertise reversal effect.
8. Myths: learning styles (the meshing hypothesis and its failed tests), left- and right-brained learners.
9. Tutoring: human tutoring's real effect; intelligent tutoring systems; knowledge tracing (Part 45) as the
   student model.
10. Scheduling reviews as control: from Leitner's boxes and SM-2 to models that estimate each memory's half-life
    and optimize the next interval. Part 21's memory model drives a scheduler, and it is raced against fixed
    schedules on the Pool.
11. Reading: the simple view; phonics and the evidence that settled the "reading wars".
12. Beliefs and feedback: growth-mindset interventions at national scale (small effects for some students);
    feedback that lowers performance a third of the time.

*Psyche:* `psyche.work`: a review scheduler on Part 21's memory model (fixed, expanding and model-based policies
compared at equal study time); a knowledge-tracing tutor on simulated students.
*On you:* the spaced-against-massed test; predict your own score first.
*Ledger:* the testing effect (`replicated`); spacing (`replicated`); interleaving (`replicated`); learning-styles
matching (`failed`); Bloom's two sigma (`replicated, smaller`); growth-mindset interventions (`replicated,
smaller`; heterogeneous); longhand beating laptops for notes (`contested`).
*In practice:* curriculum and course design, edtech products, corporate training, spaced-repetition software; a
worked redesign of a course's study plan.
*Frontier:* randomized trials of AI tutors **(verify)**; optimal scheduling with realistic memory models; what
transfers.
*Reading:* Bloom 1984; VanLehn 2011; Dunlosky et al. 2013; Roediger & Karpicke 2006; Bjork & Bjork 2011; Pashler
et al. 2008; Sweller 1988; Freeman et al. 2014; Deslauriers et al. 2019; Settles & Meeder 2016; Yeager et al.
2019; Castles, Rastle & Nation 2018.

### Part 55 · Behaviour Change at Scale (~55)
*Question:* how much can a small change in how a choice is presented change what millions of people do?
*Story:* in countries where people must opt in to organ donation, consent rates are low; where they must opt
out, nearly everyone is a donor. A change of default, one sentence on a form. The nudge becomes government
policy across the world. Then the accounting arrives: in published papers the average nudge moves behaviour by
almost nine percentage points; across everything two government units ran, by about one and a half.
1. Hook: the donation defaults (Johnson and Goldstein 2003), and what defaults do and do not change downstream.
2. Why defaults work: effort, implied endorsement, loss aversion (Part 26). Retirement enrolment from 37% to
   86%; Save More Tomorrow.
3. The toolbox: framing, salience, reminders, simplification, commitment devices, social norms (energy reports
   and a 2% reduction).
4. On you: five interventions to raise gym attendance. Rank them. Then the megastudy's results and the experts'
   forecasts.
5. The megastudy: dozens of interventions in one population (Milkman et al. 2021); why the winner's estimate is
   inflated and how shrinkage corrects it (link to *Statistics, Built* Part 25).
6. The reckoning: academic nudges against nudge-unit trials (DellaVigna and Linos 2022); the meta-analysis and
   its bias-corrected re-analysis.
7. Heterogeneity is the finding: effects depend on who and where (Bryan, Tipton and Yeager 2021).
8. Incentives: paying people to quit smoking or exercise; what persists.
9. When nudges backfire: highway fatality signs that increased crashes; norm messages that licensed the
   below-average.
10. Persuasion at scale: campaign contact's near-zero average effect in general elections; advertising returns
    that are almost impossible to measure; search-ad experiments.
11. Misinformation: accuracy prompts and inoculation; effect sizes in the field.
12. Ethics and limits: autonomy, transparency and sludge; individual-level fixes against changing the system.

*Psyche:* `psyche.work`: a megastudy simulator on the Pool (many arms, small true effects, winner's curse and
shrinkage); a publication filter that reproduces the academic–practice gap.
*On you:* the ranking exercise.
*Ledger:* default effects on enrolment (`replicated`); social-norm energy reports (`replicated`, small); the
average published nudge (`replicated, smaller` in practice); signing at the top for honesty (`retracted`; failed
replication, then fabricated data); choice overload from more options (`contested`: meta-analytic mean near
zero); accuracy prompts (`replicated, smaller`).
*In practice:* behavioural insights teams, product growth and retention, public-health campaigns; a worked trial
design with a preregistered primary outcome.
*Frontier:* predicting which interventions work where; forecasting tournaments; personalization against fairness.
*Reading:* Thaler & Sunstein 2008/2021; Johnson & Goldstein 2003; Madrian & Shea 2001; Milkman et al. 2021;
DellaVigna & Linos 2022; Mertens et al. 2022, with Maier et al. 2022; Bryan, Tipton & Yeager 2021; Allcott 2011;
Kalla & Broockman 2018; Lewis & Rao 2015; Hall & Madsen 2022; Chater & Loewenstein 2023.

### Part 56 · Psychology and Law (~55)
*Question:* how much should a court trust a memory, a confession or an expert?
*Story:* a witness picks a man from a line-up and is certain. Years later DNA shows it was someone else.
Mistaken identification figures in most of the first few hundred DNA exonerations. The psychology of the
courtroom is Parts 12 and 21 with a person's liberty attached, and for once the research changed the practice.
Then it changed its own mind about one of its reforms.
1. Hook and On you: a staged event, then a six-person line-up.
2. The line-up as signal detection (Part 12): culprit-present and culprit-absent line-ups; hits and false
   identifications of the innocent.
3. Simultaneous against sequential: the diagnosticity-ratio argument for sequential line-ups, and the ROC
   analysis that reversed it (sequential mostly shifts the criterion).
4. Confidence: once thought nearly useless; now, initial high confidence under clean procedures is highly
   diagnostic, and confidence inflates with feedback.
5. System variables against estimator variables; the reforms: double-blind administration (Part 2's horse),
   fair fillers, recorded confidence.
6. False confessions: the laboratory paradigm in which most innocent students sign; interrogation tactics and
   the false evidence ploy; documented cases.
7. Lie detection: people at 54%; the polygraph's record; why cue-based detection fails.
8. Experts are people: fingerprint examiners changing their own earlier conclusions when given context; the
   2009 and 2016 reviews of forensic science; linear sequential unmasking.
9. Children as witnesses and suggestibility; the day-care cases; implanted memories (Part 21) and the memory
   wars.
10. Juries: the story model; anchoring in sentencing; the "hungry judges" finding and its artefact.
11. Risk assessment: actuarial against clinical prediction (Part 39); a risk tool's error rates across groups and
    the impossibility result (link to *Statistics, Built* Part 63).
12. Numbers in court: the standard error of an IQ score becomes constitutional law (*Hall v. Florida*, 2014);
    the Flynn effect and capital cases.

*Psyche:* `psyche.work`: a line-up model on Part 12's observer and Part 21's memory (simultaneous and sequential
procedures, ROC and confidence–accuracy curves); an interrogation decision model.
*On you:* the line-up, with your confidence.
*Ledger:* sequential line-up superiority (`failed` on ROC analysis); high-confidence initial identifications
being accurate under good procedure (`replicated`); the laboratory false-confession effect (`replicated`);
human lie detection near chance (`replicated`); contextual bias in forensic examiners (`replicated`); the
hungry-judges effect (`contested`: case ordering explains much of it).
*In practice:* police procedure, expert testimony, forensic laboratories, forensic assessment; a worked
evaluation of an identification's evidentiary weight.
*Frontier:* machine face recognition beside human witnesses; interviewing methods that work; risk tools under
scrutiny.
*Reading:* Wells et al. 1998, 2020; Wixted & Wells 2017; Wixted & Mickes 2014; Kassin et al. 2010; Kassin &
Kiechel 1996; Bond & DePaulo 2006; Dror, Charlton & Péron 2006; National Research Council 2009, 2014; Ceci &
Bruck 1995; Garrett, *Convicting the Innocent*.

### Part 57 · Health and Care (~55)
*Question:* how does the mind get into the body, and how does help get to the people who need it?
*Story:* in 1991 volunteers are given nose drops containing a cold virus and quarantined. The more stress they
reported beforehand, the more of them catch the cold, in a dose–response line. The first half of this part is
the evidence that psychological states change physical health and that sugar pills change pain. The second half
is logistics: most people with a treatable condition get no treatment, and the solutions are systems.
1. Hook: the cold studies (Cohen, Tyrrell and Smith 1991).
2. Stress and illness: Part 10's loop over years; allostatic load; status and health in civil servants; adverse
   childhood experiences; the limits of the correlational evidence.
3. Placebo: the "powerful placebo" (1955) and the regression-to-the-mean critique (2001); what survives:
   placebo analgesia, blocked by an opioid antagonist (1978).
4. On you: an open-label placebo. People are told the pill is inert. Predict the result.
5. Expectation as a prior on bodily signals (Parts 14, 15); nocebo effects and side-effect warnings; sham
   surgery trials.
6. Pain: chronic pain as a learned state; fear-avoidance; psychological treatment's modest, real effects.
7. Behaviour is the treatment: adherence near half; the lifestyle trial that cut diabetes incidence by 58%; why
   weight returns (Part 28).
8. Sleep, treated: CBT for insomnia as first-line care (Part 10's model, applied).
9. Mindfulness: the clinical evidence, the school-based null, and the hype.
10. The treatment gap: prevalence against capacity; stepped care; a national programme that reports outcomes for
    every patient.
11. Measurement-based care: feedback to therapists improves outcomes for those off track.
12. Scale: lay-counsellor programmes (the Friendship Bench); digital therapeutics: trial evidence, engagement
    cliffs, a regulated product whose company failed, and privacy enforcement.

*Psyche:* `psyche.work`: a stepped-care simulator on the Pool (capacity, waiting, allocation rules, outcome
monitoring); an expectation model of placebo analgesia from Part 14's observer.
*On you:* the open-label placebo prediction.
*Ledger:* stress and susceptibility to infection (`replicated`); placebo analgesia (`replicated`); placebo
effects on objective outcomes (`failed`, mostly); open-label placebo (`replicated` in small trials; `contested`);
lifestyle intervention preventing diabetes (`replicated`); Type A personality and heart disease (`failed`;
hostility remains, weaker); hotel-maids mindset and health (`contested`).
*In practice:* health psychology, behavioural medicine, service design in mental health, digital health
evaluation; a worked stepped-care capacity plan.
*Frontier:* just-in-time adaptive interventions; chatbots in care (Part 60); causal evidence on stress and
disease.
*Reading:* Cohen, Tyrrell & Smith 1991; Beecher 1955, with Hróbjartsson & Gøtzsche 2001; Levine, Gordon & Fields
1978; Kaptchuk et al. 2010; Diabetes Prevention Program Research Group 2002; Engel 1977; Clark 2018; Chibanda et
al. 2016; Lambert et al. 2018; Sapolsky.

---

## Act XIII · The Frontier

These parts are research-level throughout. Their Frontier chapters are the open problems of their fields.

### Part 58 · The Efficient, Predictive Brain (~60)
*Question:* is there one principle from which the mind's mechanisms follow?
*Story:* in 1961 Horace Barlow proposes that sensory neurons exist to remove redundancy from their input. In 1996
two researchers ask a network to describe photographs of nature with as few active units as possible, and its
units turn into the receptive fields Hubel and Wiesel found in cortex. An optimization principle produced
biology. This part follows the most ambitious descendants of that result, up to a theory that claims to explain
everything a brain does, and asks what such a claim would have to risk.
1. Hook: sparse coding (Olshausen and Field 1996), run on screen: Gabor patches emerge from natural images.
2. Efficient coding: Attneave and Barlow; a fly's contrast code matching the histogram of its world (Laughlin
   1981); whitening and centre–surround (Part 13) derived.
3. Efficiency explains biases: resource-limited codes predict Weber's law (Part 11), capacity limits (Part 19)
   and "anti-Bayesian" repulsions; value coding in choice (Part 26).
4. Rate–distortion theory: the cheapest representation for a tolerated error; Shepard's law (Part 22) derived
   from it.
5. Normalization as a canonical computation: one equation in retina, cortex, attention (Part 18) and value.
6. Predictive coding (Rao and Ballard 1999): cortex as a hierarchy sending predictions down and errors up; what
   the physiological evidence does and does not support.
7. The free-energy principle: variational inference derived step by step (link to *AI, Built* Part 7); action as
   inference; what is a theorem, what is a model, and the charge of unfalsifiability.
8. On you: adaptation after-effects (tilt, motion, colour), each predicted by an efficient code.
9. The Bayesian brain and its critics: optimal against what, with which priors; "Bayesian just-so stories".
10. Resource rationality: heuristics (Part 26) as optimal use of limited computation.
11. Learning rules: backpropagation and the brain; predictive coding as an approximation to it; meta-learning in
    prefrontal cortex.
12. Unified architectures: Newell's "twenty questions" complaint (1973); ACT-R, Soar and the common model; large
    brain simulations; the scorecard against the Battery.

*Psyche:* `psyche.efficient`: whitening and sparse coding on a licensed natural-image set; a predictive-coding
network; a rate–distortion derivation of generalization gradients; an efficient-coding observer reproducing
adaptation effects.
*On you:* three after-effects with predicted direction and size.
*Ledger:* sparse coding yielding V1-like fields (`replicated`); efficient-coding predictions of perceptual bias
(`replicated` in several domains); prediction-error neurons as predictive coding requires (`contested`); the
free-energy principle (`not directly tested`: the question is whether it can be).
*In practice:* compression and perceptual codecs, neuromorphic design, representation learning in AI.
*Frontier:* the part's subject. Stated open problems: a normative account of capacity limits; which learning rule
cortex uses; whether any unified theory makes a risky prediction that the special theories do not.
*Reading:* Barlow 1961; Laughlin 1981; Olshausen & Field 1996; Simoncelli & Olshausen 2001; Carandini & Heeger
2012; Rao & Ballard 1999; Friston 2010; Bowers & Davis 2012; Jones & Love 2011; Wei & Stocker 2015; Sims 2018;
Lieder & Griffiths 2020; Lillicrap et al. 2020; Newell 1973.

### Part 59 · Computational Psychiatry (~55)
*Question:* can a model of the mind tell a clinician something a conversation cannot?
*Story:* the plan is elegant: give a patient a task from Acts IV and V, fit the model, read off the parameter
that has gone wrong, choose the treatment. The first obstacle is a paradox. The tasks psychology trusts most are
trusted because everyone shows the effect, which means they barely distinguish one person from another. This
part is about a young field's promise and the measurement discipline (Part 3) it is having to relearn.
1. Hook: the reliability paradox (Hedge, Powell and Sumner 2018). Robust effects, unreliable individual scores.
2. The programme: theory-driven models (parameters as mechanisms) and data-driven prediction; what each has
   delivered.
3. Worked case: compulsivity and reduced model-based control in fourteen hundred online participants (Gillan et
   al. 2016), with a transdiagnostic factor (Part 39).
4. Worked case: learning under uncertainty: volatility, learning rates and anxiety; hierarchical Gaussian
   filters in outline.
5. Mood as computation: momentum and reward prediction errors (Part 40) at smartphone scale.
6. On you: design a task. A slider trades reliability against sensitivity to the effect; you cannot have both
   without more trials (computed).
7. Fixing measurement: hierarchical models, more trials, task redesign; retest reliability of model parameters.
8. Biotypes: clustering patients by brain connectivity (2017), and what happened on replication.
9. Prediction that does not travel: treatment-outcome models that work in the trial they were trained on and
   fall to chance in the next (2024).
10. Treatment selection: the personalized advantage index; how large a trial a selection rule needs (computed).
11. New interventions: targeted brain stimulation; closed-loop stimulation in single patients; psychedelic
    trials, functional unblinding (Part 2) and a regulator's refusal **(verify)**.
12. Digital phenotyping: what phone sensors predict, and the ethics.

*Psyche:* a precision-psychiatry bench on the Pool: task designs scored for reliability and sensitivity; a
clustering pipeline that finds "biotypes" in structureless data; a prediction model trained on one simulated
trial and tested on another; power for treatment-selection trials.
*On you:* the task-design slider.
*Ledger:* the reliability paradox (`replicated`); model-based deficits in compulsivity (`replicated` online);
connectivity biotypes of depression (`contested`, replication failures); cross-trial generalization of
outcome prediction (`failed` so far); accelerated stimulation protocols **(verify)**.
*In practice:* digital mental-health products, trial design, biomarker claims and how to evaluate them.
*Frontier:* the part's subject. Open problems: a task battery with clinical-grade reliability; generalizable
prediction; mechanistic validation of a computational target.
*Reading:* Montague et al. 2012; Huys, Maia & Frank 2016; Hedge, Powell & Sumner 2018; Gillan et al. 2016;
Browning et al. 2015; Rutledge et al. 2014; Drysdale et al. 2017, with Dinga et al. 2019; Chekroud et al. 2024;
DeRubeis et al. 2014; Karvelis, Paulus & Diaconescu 2023.

### Part 60 · Minds and Machines (~60)
*Question:* what can psychology and artificial intelligence now tell each other?
*Story:* the Perceptron was published in *Psychological Review* in 1958, by a psychologist. Reinforcement
learning came from Pavlov and Thorndike. For decades AI borrowed from psychology. Now the debt runs both ways:
language models are given psychology's tests, proposed as models of the mind, used as therapists and persuaders,
and offered as substitutes for participants. Each of those uses is a psychological claim, and this part tests
each with the tools of the previous fifty-nine.
1. Hook: Rosenblatt's paper, and ELIZA's users confiding in a script (1966).
2. Networks as models of the brain: vision (Part 14) and language (Part 23); brain-score benchmarks; where the
   models' errors differ from people's, and why behaviour matched is not mechanism shared.
3. Machine psychology: running the Battery and the classic problems (Part 26) on language models. Method traps:
   training-data contamination, prompt sensitivity, one model is not a sample.
4. Theory of mind in machines: the 2023 claim, the perturbation failures, the comparison with 1,900 humans
   (2024). What a valid test would need (Part 30's lesson about infants).
5. On you: six short texts and six answers to a moral dilemma. Human or model?
6. Psychometrics for machines: construct validity of benchmarks (Part 3); IRT for evaluations (Part 45).
7. People trusting machines: automation bias (Part 51); algorithm aversion and appreciation; anthropomorphism
   and the two dimensions of mind perception.
8. Machines changing minds: a conversation that durably reduced conspiracy belief (2024); persuasion
   comparisons with humans **(verify)**; sycophancy.
9. Machines as therapists and companions: the trial evidence **(verify)**, the risks, and what Part 42's
   standards require of a control group.
10. Silicon samples: language models as stand-ins for survey respondents and participants; where they match
    aggregates and where they erase variance and minorities.
11. Screens and well-being: the correlational specification curves (tiny associations), the deactivation
    experiments, natural experiments, and an unresolved dispute presented with each side's best case.
12. What machines lack and have: developmental benchmarks; child-scale learning; and the question Part 27 left
    open, asked of machines.

*Psyche:* Psyche and open-weight language models sit the same Battery (through *AI, Built*'s tooling): error
patterns compared, not just accuracy; an IRT analysis of a benchmark; a silicon-sample study against real survey
data from the Archive.
*On you:* human or model?
*Ledger:* language models showing human-like biases on classic problems (`replicated`, with contamination
caveats); robust theory of mind in language models (`contested`); algorithm aversion (`contested`: task-
dependent); durable belief change from model dialogue (`replicated` **(verify)**); social-media use causing
adolescent harm at scale (`contested`).
*In practice:* AI evaluation, human–AI interaction design, safety and alignment research, mental-health
products, market research with synthetic respondents.
*Frontier:* the part's subject. Open problems: a science of machine behaviour with psychology's hard-won
methods; models of cognition that are also mechanistic; effects of pervasive AI on human learning and belief.
*Reading:* Rosenblatt 1958; Weizenbaum 1966; Lake et al. 2017; Yamins & DiCarlo 2016; Bowers et al. 2023; Binz &
Schulz 2023; Kosinski 2024, with Ullman 2023 and Strachan et al. 2024; Mahowald et al. 2024; Dietvorst, Simmons
& Massey 2015; Logg, Minson & Moore 2019; Costello, Pennycook & Rand 2024; Argyle et al. 2023; Orben & Przybylski
2019; Allcott et al. 2020; Rahwan et al. 2019.

### Part 61 · The Next Psychology (~55)
*Question:* what would psychology look like if it were designed today?
*Story:* in 2020, 160 teams with thousands of variables on four thousand families and any method they like try
to predict six outcomes in the children's lives. The best models barely beat four-variable regression. A field
that explains much and predicts little has to decide what it is for. This part gathers the proposals: bigger
teams, bigger samples, experiments designed as spaces instead of points, theories written as code, and a model of
the research community itself.
1. Hook: the Fragile Families Challenge (Salganik et al. 2020).
2. Explanation against prediction (Yarkoni and Westfall 2017): what each buys, and how to have both.
3. Big team science: Many Labs, the Psychological Science Accelerator, ManyBabies, ManyPrimates. Costs, credit
   and what they found.
4. Experiments at the scale of millions: a navigation game played by millions; the Moral Machine; language
   learners; what a sample of that size can and cannot fix.
5. Who is sampled (Part 38): a decade after WEIRD; English as the default language of cognitive science.
6. On you: an experiment has ten design choices. Pick one cell, as a standard study does, then watch the effect
   vary across the whole space.
7. Integrative experiment design (Almaatouq et al. 2024): sample the space of experiments, fit a surrogate
   model, and let theories compete to predict held-out cells.
8. Machine-assisted theory: ten thousand risky-choice problems and a learned theory that contains the classics
   (Peterson et al. 2021); adaptive design optimization.
9. Theory as code: formal models against verbal theories; theory construction methods; what counts as a
   derivation.
10. The natural selection of bad science (Smaldino and McElreath 2016): laboratories as agents, publications as
    fitness. The model run, and then run under registered reports.
11. Digital traces: phones, language, wearables; prediction of traits and states; consent and harm; a famous
    Twitter-and-heart-disease result taken apart.
12. Automation: language models as research assistants, simulated participants and reviewers; what must stay
    human.

*Psyche:* a model of a research community on the Pool (laboratories with strategies, a publication filter,
selection on output), under alternative incentive rules; an integrative design over a parameterized experiment
with a surrogate model.
*On you:* the design-space exercise.
*Ledger:* poor predictability of life outcomes (`replicated` across 160 teams); many-labs heterogeneity being
small for most effects (`replicated`); large-scale online cognitive data matching laboratory benchmarks
(`replicated`).
*In practice:* research operations in industry, experimentation platforms, forecasting; how to commission
research that will hold up.
*Frontier:* the part's subject, ending on a ranked list of proposals by the evidence that they work.
*Reading:* Salganik et al. 2020; Yarkoni & Westfall 2017; Hofman et al. 2021; Almaatouq et al. 2024; Peterson et
al. 2021; Moshontz et al. 2018; Coutrot et al. 2018; Thalmayer, Toscanelli & Arnett 2021; Blasi et al. 2022;
Smaldino & McElreath 2016; Borsboom et al. 2021; van Rooij & Baggio 2021; Muthukrishna & Henrich 2019.

### Part 62 · The Dissertation (~55)
*Question:* was Kant right?
*Story:* the series ends as a doctorate does. One question, left open by an earlier part, is taken through a
registered report: reviewed before the data exist, run, and reported whatever it shows. Then the accounts are
closed. Psyche sits the whole Battery. The Ledger is read from top to bottom. The Homunculus is drawn one last
time, and the parts of it that are still a little person are the syllabus of the next fifty years. Kant's three
objections are answered one at a time.
1. Hook: Kant's three objections, back on screen.
2. How research is done: finding a question worth asking; reading; the pilot; advisers and collaborators; what a
   contribution is.
3. Ethics as practice: Belmont's principles applied; data privacy; the profession's failures (psychologists and
   coercive interrogation) and its codes.
4. The registered report, Stage 1: theory as a model in Psyche that makes a risky prediction; design, power on
   the Pool, analysis code, the outcomes that would count against the theory.
5. Peer review, shown: three reviews (written for the film), the response, the revision.
6. Stage 2: data (an open dataset fixed in advance, plus the viewers' on the site), the registered analysis, the
   result. The narration follows the data.
7. Writing it: the paper's structure; figures that show the data; limits stated.
8. Psyche's scorecard: the whole Battery, model against human benchmarks, task by task. Where one model with one
   set of parameters does several tasks, and where it cannot.
9. The Ledger, complete: what replicated, by act; the pattern; the date on every row.
10. The Homunculus, last drawing: what is mechanism now, and what is still a person (consciousness, open-ended
    thought, a unified architecture, the individual case).
11. The verdict on Kant: mathematics applies; experiment is possible; observation does disturb, and the field
    learned to measure the disturbance. The fourth objection he did not make: the observer's incentives.
12. Where to go: reading by direction, the roles of §2.6, and the map of open problems from all sixty-two
    Frontier chapters.

*Psyche:* the thesis: a registered report executed end to end; the Battery scorecard; the final Ledger board and
Homunculus map generated from the series' data.
*On you:* the last experiment, and your Battery page on the site with every task you have taken.
*Ledger:* the complete board.
*In practice:* the careers map: academic research, clinical training routes (which this series is not), and the
industry roles, with what each asks for.
*Frontier:* the open-problems map.
*Reading:* Chambers & Tzavella 2022; the Belmont Report; Hoffman et al. 2015; Platt 1964; Hamming, "You and Your
Research"; Newell 1973; the reading lists of every act.

## 5. Threads that cross the parts

Ideas met more than once, each time sharper. Each return opens with an upgrade card (the earlier statement, what
it assumed, what is added).

| Thread | Appears in |
|---|---|
| Prediction error | 16 (Rescorla–Wagner), 17 (TD and dopamine), 28 (wanting), 40 (mood), 41 (salience, addiction), 58 (predictive coding) |
| Signal detection | 12, 21 (recognition), 25 (confidence), 39 (screening), 51 (vigilance), 56 (line-ups) |
| Bayesian inference | 14 (perception), 22 (concepts), 24 (prediction), 35 (mind reading), 41 (hallucination), 57 (placebo), 58 (critique) |
| Evidence accumulation | 1 (stages), 25 (diffusion), 27 (volition), 36 (the IAT), 45 (response-time IRT), 46 (context effects) |
| Attractors and tipping points | 6, 19 (ring), 20 (Hopfield), 27 (ignition), 39 (symptom networks), 47 (early warnings) |
| Latent variable or network? | 3, 32 (g and mutualism), 33, 39 (p and symptoms), 44 |
| Reliability and attenuation | 3, 8, 36 (the IAT), 47, 53 (range restriction), 59 (the paradox) |
| Regression to the mean | 2, 35 (Dunning–Kruger), 42 (therapy), 57 (placebo) |
| Group to individual | 9 (heritability), 32, 47 (ergodicity), 48 (Estes), 59 |
| The filtered literature | 4, 9 (candidate genes), 42, 50, 55 (nudges), 61 |
| Who was studied | 2, 38, 44 (invariance), 61 |

**Cross-series links.** *Statistics, Built*: Parts 10 (tests), 13 (design), 25 (shrinkage, meta-analysis), 28
(model choice), 31 (factor analysis, MDS), 33 (multiple testing, replication), 35–37 (causal inference), 63
(fairness), 64 (IRT for evaluation). *AI, Built*: Parts 7 (variational inference), 9 (the delta rule and
networks), 20 (Hopfield and Boltzmann), 26 (reinforcement learning), 30–31 (inside models, evaluation).
*Philosophy, Built*: Parts 13–16 (belief and evidence), 30–32 (mind, consciousness, free will), 33–34 (choice and
games), 37 (moral psychology). *Computer Science, Built*: Part 44 (people and products).

## 6. What the series is not

- Not self-help, and not clinical training. It explains the evidence for treatments; it does not treat.
- Not a tour of famous studies. A study appears when it carries the argument, with its record.
- Not a debunking series. Most of what the Ledger holds replicates, and the series says so with the same care.
- Not a neuroscience course. Act II and Parts 49 and 58 cover what psychology needs; a full neuroscience series
  would be its own.

## 7. Phases

0. **Infrastructure** (one or two sessions).
   - `explainer/psychology/`: ACTS/PARTS, `series_map` (the Homunculus), timeline and levels strips,
     `chapter_card`, payoff, reference, study, ledger and upgrade cards; `style.py`, `viz.py` (the first
     instruments: `TrialStrip`, `DemoStage`, `EffectPicture`, `PoolCloud`, `LedgerCard`); `pool.py`, `ledger.py`,
     `archive/` with `SOURCES.md`, `battery.py`, `psyche/`.
   - `videos/psychology/__init__.py`, `PSYCHOLOGY_ZH_GUIDE.md`, `psychology_text_zh.json`.
   - Tools: a `Course` entry for `psychology` (prefix `psych`) in `tools/series_site.py` with its test count in
     `tests/test_series_site.py`; `psychology` added to `videos/coursekit.SERIES` and, if bilingual, to `BILINGUAL`
     in `tools/make.py`; `--series psychology` for the QA and packaging tools; the Ledger gate.
   - The browser task kit for the Battery (`course/site/widgets/00_tasks.js`: trial loops, timing, local-only
     storage), since every part's interactive needs it, and a scripted participant for `tools/check_course.py`.
   - `tests/psychology/`: the Pool's planted truths are recoverable; the Ledger's schema; a silent smoke render.
1. **Pilots: Part 1, then Part 2** (The Experiment). The first draft of this plan named Part 12 as the second
   pilot; it is Part 2 instead, for two reasons found while building Part 1: the course tools and the site count a
   series' parts from 1 without gaps, so a part built out of order would not appear; and Part 1 ends on Part 2's
   hook. Part 2 still exercises what a typical part needs (an experiment on the viewer, a model fitted to
   historical data, designs run on the Pool, Ledger rows, an industry payoff), and Part 12 becomes the checkpoint
   for the methods standard when Act III is reached. Delivered with previews and contact sheets. **Review with
   the user**, then lock the standard.
2. **Act by act,** reviewing at each milestone:
   - Acts I–IV (Parts 2–17): method, brain, senses, learning. About 14 hours.
   - Acts V–VI (Parts 18–29): cognition, motivation, emotion.
   - Acts VII–X (Parts 30–43): development, differences, social, clinical. **The degree**, complete at Part 43.
   - Act XI (Parts 44–50): the graduate toolkit.
   - Act XII (Parts 51–57): the practice.
   - Act XIII (Parts 58–62): the frontier and the finale.

   Each part goes through: the frontier sweep and Ledger statuses with sources and dates; the Archive's licence
   checks; locking the chapter list; `compute.py` and its Psyche module with tests; English scenes and the QA
   gates; the course entry, lab and interactive (`videos/coursekit/AUTHORING.md`); the Chinese edition and its
   gates; commit and push.

## 8. Decisions, and open risks

**Decisions** (the default, listed first in each, was accepted on 2026-11-13):

1. **Sixty-two parts**, or a first season of 1–43 with the rest committed later. The acts are separable: XI, XII
   and XIII each stand on the degree and not on each other.
2. **30–60 minutes per part, most at 45–55.** Parts 32, 34, 48, 50, 53, 58 and 60 are planned at the top of the
   range; if one passes 60 it is split.
3. **`psych1` … `psych62` in `videos/psychology/`.**
4. **Bilingual from the start.** Language-dependent demonstrations need Chinese materials and norms (§1), which is
   real extra work in Parts 18, 21, 23 and 33.
5. **The viewer experiments and the browser Battery** as a core device, with nothing stored or sent. A later
   option, off by default and only with explicit consent, would be to let viewers contribute data to the
   capstone's replication.
6. **Methods first** (Act I), told as stories. Alternative: open with Act III and move Parts 2–4 after it.
7. **Names:** Psyche, the Pool, the Battery, the Ledger, the Homunculus.
8. **One part on consciousness and none on parapsychology, hypnosis or dreams as separate topics** (they appear
   inside Parts 4, 10 and 27). Sport, environmental and military psychology appear as cases in Act XII, not as
   parts. Sexuality and gender are treated inside Parts 10, 28, 31 and 33; a dedicated part is a possible
   addition.

**Open risks:**

- **Ledger accuracy.** A wrong replication status is the worst error this series can make. Mitigation: statuses
  are set only in the frontier sweep from primary sources, carry a date, and are reviewed again before each act
  is released. Every status and number in this draft is from memory of the literature and is to be treated as
  **(verify)** until its sweep, whether or not it is marked.
- **Licences.** Archive datasets, a natural-image set for Part 58, word norms, and a brain mesh for `BrainTour`
  (candidates: a FreeSurfer average surface, or a mesh derived from an openly licensed atlas; fallback: a drawn
  schematic). Checked per part before use.
- **Browser timing.** Reaction-time tasks in a browser have device-dependent latency. The Battery reports
  differences and slopes, which are robust to a constant delay, and says so.
- **Sensitive content.** §1.2 is the policy; Acts VIII, IX and X get an additional read against it before
  release.
- **Scope of Psyche.** Sixty small models can become sixty unrelated scripts. The rule that every module runs
  Battery tasks through one interface (§2.1) is what makes it one library; Part 48 is where that is tested.

## 9. Progress (updated as parts land)

| Part | State | Length |
|---|---|---|
| 0 | built: `explainer/psychology/` (Psyche's `chronometry`, the Pool, the Battery, the Ledger, the Archive, cards, maps and the first instruments), `tests/psychology/`, the course kit and site entries. The Chinese guide (`PSYCHOLOGY_ZH_GUIDE.md`) and text table are in place. Still to do: the Ledger gate tool, the shared browser task kit (Part 1's interactive carries its own trial loop) | |
| 1 | built, English and Chinese: 14 chapters, hook and outro; course entry, lab and interactive checked; narration table and on-screen text translated and dry-run. Open checks in its README | 46 min |
| 2 | built in English, the second pilot: 14 chapters, hook and outro; the laboratory (`lab.py`), the cue-reading model (`psyche/cueing.py`), five Ledger rows; course entry, lab and interactive checked. Chinese edition next. Open checks in its README | 56 min |
