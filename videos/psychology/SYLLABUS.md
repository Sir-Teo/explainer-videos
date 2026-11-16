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
part's `tests/psychology/test_*.py`, and **(Psy)** the Ledger gate, `tools/check_ledger.py psychN`: every study a
part shows (each Archive dataset its scenes and computations use, each author and year in a source tag) has a
Ledger row with its sources and the date they were checked, or a `ledger.shown` declaration that says why it has
none and, where a row is due later, which part enters it. A deferred row fails the gate once that part is built.

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
| `brain` | 7 | a lesionable box-and-arrow architecture; patients under one resource and two; cortical magnification; lesion-symptom mapping |
| `imaging` | 8 | a tuned cell; a lead-field toy for EEG; ERP averaging; the haemodynamic response and the GLM; a synthetic brain under each threshold; circular selection; reverse inference |
| `genes` | 9 | many loci; twin, adoption and family simulators with each assumption switchable; Falconer and ACE fits; a genome-wide scan and polygenic scores; the sibling design; embryo selection |
| `body` | 10 | a light-driven clock (free running, entrainment, phase response, jet lag); the two-process model of sleep and an alertness curve; lapses under short sleep; a hormone loop with feedback; receptor occupancy, blockers and half-lives; an opponent process; tolerance tied to a place; chronotype |
| `body` | 10 | a circadian oscillator; the two-process model; an HPA feedback loop; receptor occupancy and tolerance |
| `psychophysics` | 11 | an observer with floor, Weber and photon noise; psychometric functions; constant stimuli, limits and adjustment; staircases and QUEST; ML fits with bootstrap intervals and goodness of fit; Fechner's count; Stevens's power law and cross-modality matching; the triangle test; Thurstone's Case V |
| `sdt` | 12 | equal- and unequal-variance observers; d′, c and β; yes–no, rating, 2AFC and m-AFC; ROCs and zROCs fitted by maximum likelihood; the ideal observer under base rates and payoffs; high-threshold and dual-process rivals; predictive value; prevalence |
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
| 2 | Two-alternative threshold (a brightness increment over a standard of 100; built in Part 11) | 11 | a psychometric function; Weber's fraction |
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

### Part 3 · The Measure (~56)
*Question:* what does a number attached to a mind mean?
*Story:* in 1940 a committee of physicists and psychologists reports that it cannot agree whether sensation can be
measured at all. Stevens answers by asking what operations a number survives. Spearman has already asked the other
question, how much of a score is error. The two answers, scale type and reliability, plus the hardest question,
validity, decide what every later number in the series is worth.
0. Hook: the British Association's committee, 1932 to 1940. The physicists' objection: no addition, no
   measurement. Kant's first objection returns in a sharper form. Three questions for any number.
1. Stevens's four scales (1946) as groups of permissible transformations; the test of a meaningful statement. The
   quarrel over averaging ratings, computed: the order of two means can be reversed by respacing the scale
   exactly when the two groups' answers cross; sums of many items are forgiving.
2. From an order to a scale: conjoint measurement in one picture (three people, three questions), and a table
   that fails (paid off in Part 46).
3. On you: the Forer reading. Everyone gets the same sketch. Forer's class of 39 rated it 4.26 out of 5 (1949). A
   measure has to tell people apart.
4. True score and error: X = T + E, one person tested 300 times; reliability as a variance ratio, derived; the
   correlation of parallel forms.
5. Spearman 1904: attenuation and its correction (derived; checked on the Pool across test lengths), and what
   the correction costs in studies of 60 people.
6. Longer tests are better tests: Spearman-Brown derived; Cronbach's alpha, what it assumes and what it is not
   (unidimensionality); error from the day (retest) and from the judge (kappa); the measurement library.
7. Validity: content, criterion, construct. Cronbach and Meehl's nomological network (1955); the
   multitrait-multimethod matrix (Campbell and Fiske 1959), computed with method variance planted.
8. Jingle and jangle: one name for two things, two names for one. Grit and conscientiousness (0.84).
9. What is a construct? A hidden cause, and a network of mutual causes, imply the same correlations: a preview of
   Parts 32, 39 and 44.
10. Asking people: what introspection can deliver (Nisbett and Wilson 1977; choice blindness, Johansson et al.
    2005).
11. The reliability paradox, first statement: the tasks that give the most robust effects make the worst tests of
    individuals (Hedge, Powell and Sumner 2018; paid off in Parts 47 and 59).
12. The Ledger. 13. In practice: every score is a measurement; five questions for any score. 14. Frontier.

*Psyche:* no new faculty. The measurement library (`explainer/psychology/measure.py`) and a block of the Pool:
three traits, grit, a response style per method, rating-scale items, a conflict task. Reliability against test
length, attenuation and its correction, alpha under violated assumptions, an MTMM matrix with planted method
variance, a factor model against a network.
*On you:* the Forer effect (in the film, and as the part's interactive).
*Ledger:* the Barnum/Forer effect (`replicated`); telling more than we can know (`replicated`, for reports of
causes); choice blindness (`replicated`). Deferred with reasons: grit beyond conscientiousness (Part 28), the
reliability paradox (Part 59).
*In practice:* every hiring test, survey scale, clinical questionnaire and product metric is a measurement with a
reliability and a validity argument, or without one.
*Frontier:* is psychological measurement quantitative at all (Michell)? Generalizability theory; measurement
schmeasurement (Flake & Fried 2020): how measures are reported and altered.
*Reading:* Stevens 1946; Spearman 1904a; Lord & Novick 1968; Cronbach 1951; Cronbach & Meehl 1955; Campbell &
Fiske 1959; Luce & Tukey 1964; Michell 1999; Borsboom 2005; Hedge, Powell & Sumner 2018; Flake & Fried 2020.

### Part 4 · The Evidence (~48)
*Question:* when should a finding be believed?
*Story:* in 2011 a leading journal publishes nine experiments showing that people can feel the future. The methods
are the field's standard methods. Either precognition is real or the standard methods can prove anything. Within
four years the field has shown which, by rerunning a hundred of its own studies, and has begun to rebuild its
rules. Act I ends, and from here every part closes with its Ledger rows.
0. Hook: Bem, "Feeling the Future" (2011): nine experiments, more than a thousand participants, ordinary methods.
   Kant's third objection in its last form: the scientist as the observer who disturbs.
1. Effect sizes and their pictures: d as overlap and as the chance one person beats another; d = 0.2, 0.5 and 0.8
   drawn; the same effect as a correlation and as variance explained; a tiny effect made "significant" by sample
   size alone.
2. The p-value, exactly (one study against 20,000 shuffles), and the six things it is not (link to *Statistics,
   Built* Part 10).
3. Power: Cohen's 1962 survey of a year of a journal, and no rise 24 years later. Two thousand small studies of a
   real effect: three in four miss it, and the rest report twice the truth. The share of significant findings
   that are true.
4. On you: forking paths. One null dataset, four defensible choices, sixteen analyses; 5% becomes 18% (computed).
   Simmons, Nelson and Simonsohn's 61% (2011), recomputed with `statkit.multiple`.
5. The file drawer: a literature of a thousand laboratories on a true d = 0 and on a true d = 0.2 (computed), the
   funnel's missing corner, the winner's curse against study size, and three p-curves.
6. Honest people, wrong results: optional stopping (5% becomes 20% with ten looks), HARKing, and the garden of
   forking paths when only one analysis is run. Why the remedy has to be a procedure.
7. Meehl's warning (1967): in people everything correlates a little with everything, so rejecting a null is a
   weak test of a theory; physics and psychology; why the series builds models that predict numbers.
8. Fraud is the smaller problem: Stapel (2011), and what distinguished fabrication from flexibility.
9. The Reproducibility Project (2015): 97% of originals significant, 36% of replications, effects about half the
   size; the 2016 exchange; a simulated literature in which most findings are true and most replications fail,
   and what a replication rate can and cannot measure.
10. The repairs: preregistration and registered reports (96% against 44% positive results), Many Labs 1 and 2,
    and equivalence tests and Bayes factors for claiming an absence.
11. What survives: "will it replicate?" on six findings from the Ledger so far; what the survivors have in common;
    what predicted success (the strength of the original evidence; peers' bets).
12. The Ledger. 13. In practice: twenty metrics on a dashboard. 14. Frontier: have the reforms worked?

*Psyche:* no new faculty. The false-positive lab (`explainer/psychology/evidence.py`): effect sizes, power,
optional stopping, the four forks, a literature with a publication filter, p-curves, replications planned from the
printed effect, equivalence tests and a Bayes factor (reusing `statkit.multiple`'s p-hacking simulator).
*On you:* the forking-paths exercise (in the film, and as the part's interactive); six findings to bet on.
*Ledger:* Bem's precognition (`failed`); published studies are underpowered (`replicated`); published effects
shrink when repeated (`replicated`); flag priming and currency priming (`failed`); imagined contact (`contested`).
The plan called for the Ledger's first twenty rows from the Reproducibility Project and Many Labs here. Six were
entered, each with its sources read and a date; the other findings of those projects get their rows in the parts
that present them. Shown without rows, with reasons: the Simmons simulation, the Stapel inquiry, and three pieces
of meta-science due in Part 50 (registered reports, prediction markets, the retracted report of 2023).
*In practice:* the same arithmetic governs product experiments, biomarker claims and any dashboard with many
metrics; the four repairs carry over one for one.
*Frontier:* the best journals are not exempt (Camerer et al. 2018); the field can price its own findings (Dreber
et al. 2015); whether findings made under the new rules are more often true is open, and a 2023 report that they
are was retracted in 2024. Research problem: a study that could show whether registered reports give truer
findings, and not merely fewer positive ones.
*Reading:* Bem 2011; Cohen 1962; Meehl 1967, 1978; Rosenthal 1979; Kerr 1998; Simmons, Nelson & Simonsohn 2011;
Gelman & Loken 2013; Open Science Collaboration 2015; Klein et al. 2014, 2018; Camerer et al. 2018; Scheel,
Schijen & Lakens 2021; Chambers 2017; Ritchie 2020.

---

## Act II · The Wet Machine

### Part 5 · The Neuron (~58)
*Question:* what is the mind's smallest moving part, and what does it compute?
*Story:* Helmholtz showed the nerve signal is slow. A century later Hodgkin and Huxley, with a squid axon and a
hand calculator, wrote four equations that reproduce it to the millisecond. It is psychology's best model of
anything, and the template for every model in the series: measure, write equations, simulate, compare.
0. Hook: Galvani's frog and Volta's objection; Helmholtz's speed against a wire's; four equations and a speed
   they were never fitted to (18.8 m/s computed, 21.2 measured).
1. Cajal against Golgi: the neuron doctrine. Anatomy of a neuron, drawn, with its direction.
2. Ions and the membrane: diffusion against electrical force. The Nernst potential; two batteries; Goldman's
   equation as a dial between them.
3. The membrane as a circuit: capacitance, leak, the time constant (the RC curve on screen). A membrane adds up a
   few milliseconds and forgets the rest.
4. The squid giant axon, the overshoot of 1939 and the voltage clamp (Cole; Hodgkin, Huxley and Katz): the loop
   between voltage and channels, how the clamp breaks it, and the two conductances it showed.
5. The model: why a fourth power gives a delay; the gates m, h and n, their steady values and speeds; four
   equations, fitted only to clamp data.
6. The action potential, computed: one spike with its conductances; threshold and all-or-none; the absolute and
   relative refractory periods, each traced to a gate.
7. Propagation: passive spread and the length constant; the travelling spike on the 1952 axon (18.7 m/s
   recomputed); speed against radius, and myelin. Helmholtz's speed recovered.
8. Reduction: FitzHugh-Nagumo; the phase plane, where threshold, size and dead time are geometry; two ways to
   start firing (Hodgkin's classes).
9. Integrate-and-fire: what is kept and lost. The f-I curve in closed form, checked against simulation.
10. On you: reading a spike train. Adrian and Zotterman's rate code (1926); three trains to rank; Poisson
    variability, the Fano factor, and why a brain pools many cells.
11. What one neuron can compute: a threshold unit and the table it cannot produce; coincidence detection;
    dendrites as a two-layer network.
12. The Ledger. 13. In practice: talking to nerves. 14. Frontier: how much is one neuron?

*Psyche:* `neuron` (`explainer/psychology/psyche/neuron.py`): Nernst and Goldman; the RC membrane;
Hodgkin-Huxley with the clamp, threshold, refractory period and firing rate; the cable, with the 1952 conduction
speed as a test; FitzHugh-Nagumo; LIF with its closed-form f-I curve; Poisson trains and the Fano factor; a
neuron with thresholding branches, and an exact test of whether a point neuron can match a table.
*On you:* three spike trains to rank in the film. The interactive is the same task as an experiment: which of
two recordings came from the stronger stimulus, at recording lengths from 50 ms to a second, set against a
reader who counts; each pair can also be heard as clicks, as Adrian heard his.
*Ledger:* the Hodgkin-Huxley model (`replicated`; the standard of quantitative success). Shown without rows,
with reasons: the rate code (due in Part 11), the neuron doctrine, the dendritic spikes of 2020.
*In practice:* cochlear implants, local anaesthetics and deep-brain stimulators act on these mechanisms;
neuromorphic chips implement the reductions. What the membrane tells an engineer, and what it cannot.
*Frontier:* graded dendritic spikes in human cortical neurons (Gidon et al. 2020, from secondary accounts); how
many parameters a single-neuron model needs; rate against timing; glia; whether the mind needs this level.
*Reading:* Hodgkin & Huxley 1952; Kandel et al. chs. on membrane and action potential; Dayan & Abbott chs. 5-6;
Izhikevich, *Dynamical Systems in Neuroscience*; Koch, *Biophysics of Computation*; Finger, *Minds Behind the
Brain*.

### Part 6 · Synapses and Circuits (~62)
*Question:* how do neurons talk, and how does talking change them?
*Story:* on the night before Easter Sunday 1921 Otto Loewi wakes with an experiment: two frog hearts and a
transfer of fluid. The synapse is chemical. That makes it adjustable, and Hebb guesses the rule. Small circuits
built on one motif, mutual inhibition, already sharpen edges, hold a decision and keep a rhythm.
0. Hook: the gap; sparks against soups; Loewi's two hearts; why a chemical step can be adjusted (Eccles gives up
   in 1951).
1. The chemical synapse in six steps; transmitter released in packets by chance (Katz), strength as n p q; two
   kinds of receptor, and the direction a channel pulls.
2. Seven transmitters in two groups, the wiring and the broadcast; agonist and antagonist; six places where a
   drug can act, on one diagram (used again in Parts 10 and 40-42).
3. Adding up: one EPSP against the threshold; summation in time (within about 10 ms); many inputs add to less
   than their sum; shunting inhibition as division.
4. Hebb's postulate (1949), local and unstable (run until it diverges); Oja's rule derived; a cell that finds the
   first principal component.
5. Long-term potentiation (Bliss and Lømo 1973, as a sketch of the design); the NMDA receptor as an AND; spike
   timing (Bi and Poo 1998); a sliding threshold (BCM) and a cell that becomes selective, settling where the
   rule says.
6. Lateral inhibition: Hartline's horseshoe crab; a row of units shown an edge (a ratio of 2 becomes 4.3);
   Mach's bands on the viewer and in the model.
7. On you: the Hermann grid; the receptive-field account, computed; Geier's curved grid, where the account still
   predicts spots and none are seen.
8. A circuit that decides: two rivals, winner-take-all, a choice held after the evidence has gone, and harder
   choices taking longer (returns in Parts 19, 25).
9. A circuit that keeps time: Graham Brown's cats (1911); mutual inhibition with fatigue; what sets the tempo and
   what stops the rhythm; one motif, three behaviours.
10. Populations: Berger's rhythm; Wilson and Cowan's two equations; rest, rhythm and saturation as the drive
    rises (paid off in Part 8).
11. Knobs: the neuromodulators as gain and as learning rate; a three-factor rule (a preview of Part 17).
12. The Ledger. 13. In practice: drugs at the synapse. 14. Frontier: where is a memory?

*Psyche:* `circuits` (`explainer/psychology/psyche/circuits.py`): conductance synapses on a passive membrane;
Hebb's, Oja's and the BCM rule and a spike-timing window; a row of units with lateral inhibition; a
centre-surround filter and the Hermann grid, straight and curved; a winner-take-all pair; a half-centre
oscillator; Wilson and Cowan's populations.
*On you:* Mach's bands and the Hermann grid in the film, each predicted by the model first. The interactive is
the grid as an experiment: the reader judges grids with straight and wavy streets, and their reports collect
beside what the receptive-field account predicts.
*Ledger:* long-term potentiation (`replicated`, with the link to memory argued in Part 20); lateral inhibition
(`replicated`); the Hermann grid's textbook explanation (`story and record`). Shown without rows, with reasons:
Loewi, Katz's packets, Hebb's postulate, the tagged memory of 2012 (due in Part 20), and the registered and
published antidepressant trials (due in Part 42).
*In practice:* receptor occupancy and the shift a competitive antagonist makes; SSRIs, benzodiazepines,
stimulants and antipsychotics at the synapse, each with its catch; Turner et al.'s registered against published
trials (51% positive against 94%).
*Frontier:* a memory switched on with light (Liu et al. 2012, from the abstract); whether the memory is in the
synapses or the cells; whether spike timing is the rule in a living brain; credit assignment (Part 58).
*Reading:* Loewi 1921; del Castillo & Katz 1954; Hebb 1949; Oja 1982; Bienenstock, Cooper & Munro 1982; Bliss &
Lømo 1973; Bi & Poo 1998; Hartline & Ratliff 1957; Geier et al. 2008; Graham Brown 1911; Wilson & Cowan 1972;
Liu et al. 2012; Turner et al. 2008; Dayan & Abbott chs. 7-8; Valenstein, *The War of the Soups and the Sparks*.

### Part 7 · The Brain (~63)
*Question:* is the mind in one place or everywhere?
*Story:* an iron rod passes through Phineas Gage's head in 1848 and he lives; the record of what changed in him
is a few sentences. A patient who can say only "tan" gives Broca a place for speech. A surgeon removes Henry
Molaison's hippocampi and the making of new memories stops while everything else stays. Damage is psychology's
oldest experiment, and its logic, the double dissociation, is how a box-and-arrow model gets tested, and how it
gets fooled.
0. Hook: Gage. The story against the record; one place or everywhere; damage as an experiment nobody chose.
1. A tour: four numbers (86 billion neurons, 19% in the cortex, 2% of weight, 20% of energy); four lobes, the
   cerebellum and the brainstem from the side; six structures on the inner face; each line too simple.
2. Gall's good idea (parts with jobs) and bad method (no way to fail). Flourens's removals. Lashley's mass
   action, reproduced in a model cortex where every job has a place and the task can be done six ways.
3. Broca (1861) and Wernicke (1874): two aphasias; the diagram as a model, lesioned, and the third syndrome it
   predicted; Broca's own specimens scanned in 2007 (Dronkers et al.).
4. The logic of dissociation: one resource gives a single dissociation; a double one rules it out; with noisy
   tests a screen of 100 one-resource patients shows both patterns half the time; four rules.
5. Maps: Penfield's strip (126 patients); cortical magnification, M = 17.3/(E + 0.75) mm per degree; 46% of the
   map within ten degrees of the centre of gaze; letters that each take the same length of cortex.
6. On you: the blind spot of the right eye found on screen; a gap in a line that is not seen; the geometry.
7. H.M. (1953): what was removed, what was lost, what was spared; mirror tracing learned without the memory of
   learning it; what one patient can and cannot carry.
8. The split brain: one word, two answers; the interpreter; left-brained and right-brained "types" against
   what local lateralization predicts (Nielsen et al. 2013).
9. Things that break alone: neglect, visual agnosia, prosopagnosia, blindsight (returning in Parts 14, 18, 27),
   read with chapter 4's rules.
10. A brain that rewires: the critical period (Wiesel and Hubel), a map redrawn in an adult (Merzenich), the
    taxi drivers before and after training (Maguire).
11. One place, or everywhere? Specialized, connected, redundant: the unit is a network. The ten-percent myth
    against the energy bill.
12. The Ledger. 13. In practice: one patient, one question. 14. Frontier: mapping damage in thousands.

*Psyche:* `brain` (`explainer/psychology/psyche/brain.py`): a box-and-arrow architecture whose modules can be
lesioned (the language diagram, a memory architecture); Lashley's maze in a model cortex; patients under one
resource and under two, with noisy tests; the single-case t test; cortical magnification and the blind spot's
geometry; lesion-symptom mapping on a sheet fed by one artery.
*On you:* the blind spot and filling-in, in the film. The interactive measures it: a dot sweeps outward and
inward while the reader fixes a cross and presses when it vanishes and when it returns; the two directions
cancel the reaction time, and the page reports the hole's width as a share of its distance out.
*Ledger:* Gage's personality change (`story and record`); Broca's area and speech (`replicated`, refined: the
lesions were larger than the area); the taxi drivers' hippocampus (`replicated`); left-brained and right-brained
"types" (`failed`). Shown without rows, with reasons: Wernicke and the diagram, Lashley, Penfield, the
magnification formula, H.M. (due in Part 20), the split brain and blindsight (due in Part 27), the neuron count
and the energy share, the critical period (due in Part 30), the remapped hand, and the bias in lesion maps.
*In practice:* clinical neuropsychology as one comparison done carefully: a patient's score against eight
controls by z (1 in 700) and by the single-case t test (1 in 76); the chance that a healthy person fails at
least one of 10 or 20 tests (40%, 64%); what goes in the report.
*Frontier:* lesion-symptom mapping in thousands of patients; the displacement an artery puts in the map, shown
in a simulation (2.4 voxels against 1.1) and in 581 real strokes (Mah et al. 2014); disconnection; the
cerebellum's part in cognition; whether cortical "areas" are the right unit.
*Reading:* Macmillan, *An Odd Kind of Fame*; Harlow 1868; Broca 1861; Dronkers et al. 2007; Wernicke 1874;
Lichtheim 1885; Lashley 1929; Penfield & Boldrey 1937; Horton & Hoyt 1991; Scoville & Milner 1957; Corkin,
*Permanent Present Tense*; Gazzaniga & LeDoux 1978; Nielsen et al. 2013; Weiskrantz et al. 1974; Wiesel & Hubel
1963; Merzenich et al. 1984; Maguire et al. 2000; Woollett & Maguire 2011; Crawford & Howell 1998; Mah et al.
2014; Shallice, *From Neuropsychology to Mental Structure*; Kolb & Whishaw.

### Part 8 · Reading the Brain (~60)
*Question:* what can a brain scan tell you about a mind?
*Story:* in 2009 a team puts a dead Atlantic salmon in an MRI scanner, shows it photographs of people, and finds
"activity". The fish is a statistics lesson. This part walks the chain from a neuron to a coloured map, so that
each link's assumption is visible, shows the three ways a map misleads (the threshold, choosing voxels by the
answer, reading it backwards), and then lists what the maps have and have not delivered.
0. Hook: the salmon (Bennett et al. 2009). A test at one in a thousand, a thousand times: a 63% chance of at
   least one false alarm. The chain from a neuron to a statement about a mind.
1. Listening to one neuron: Hubel and Wiesel's line (1959); a model cell's tuning curve (40, 14 and 2 impulses
   a second); the standard every other instrument is measured against, and its cost.
2. Voltages on the scalp: Berger (recorded 1924, published 1929); why only aligned, synchronous cells add (N
   against root N: about 1,100 times at a million sources); the inverse problem on a toy head, two source
   patterns with identical scalp readings.
3. Averaging out the noise: a 5 microvolt wave in 20 of noise; the noise left falls as one over root n (400
   trials for 1 microvolt); the N400 (Kutas and Hillyard 1980).
4. MRI in five minutes: protons in a field, two relaxations and contrast, gradients and k-space as a Fourier
   transform (link to *Analysis, Built*), an image rebuilt from part of its transform.
5. Blood, and a slow echo: Ogawa (1990); the haemodynamic response (peak at 5 s); the working assumption that
   responses add, a convolution (Boynton et al. 1996); what the signal follows (Logothetis et al. 2001).
6. The linear model of an experiment: a regressor, a weight and a t in one voxel (0.21, t = 5.3, against none);
   a map as 1,600 separate regressions; subtraction and pure insertion return from Part 1; rest is not nothing.
7. A hundred thousand tests: empty brains show something 44% of the time uncorrected, and 2.9%, 3.9% and 6.5%
   under Bonferroni, the false discovery rate and clusters; what each rule finds of 78 true voxels (61 to 77);
   the cluster rule against long-tailed noise (5.7% against 15.9%) and Eklund et al. (2016).
8. Choosing voxels by the answer: Vul et al. (2009); 16 people, 10,000 voxels of noise, r = .74 in the chosen
   voxels and zero in fresh data; the same .74 whether or not anything is there; Kriegeskorte et al.'s count.
9. On you: three reported correlations, two reliabilities; the ceiling, root of 0.5 times 0.8, is .63.
10. Reading a mind backwards: reverse inference as Bayes' rule (Poldrack 2006: 0.5 becomes 0.69; 0.2 becomes
    0.37); the honest version, a model tested on new data.
11. From watching to intervening: damage, the magnetic pulse (Barker et al. 1985), stimulation in surgery,
    light in animals; necessary and sufficient; what thirty years of scanning settled and what it did not.
12. The Ledger. 13. In practice: what is sold, and what works. 14. Frontier: how many people does a brain study
    need?

*Psyche:* `imaging` (`explainer/psychology/psyche/imaging.py`): a tuned cell and its spike counts; dipole sums;
a lead-field toy head with a silent source; ERP trials and averaging; relaxation curves and k-space; the
haemodynamic response, convolution and the general linear model; a synthetic brain of smooth noise with known
active patches, thresholded by each rule, with family-wise rates over a thousand null brains; cluster
calibration under two kinds of noise; circular selection; reverse inference; the reliability ceiling; the
small-study simulator and sample sizes.
*On you:* three scatter plots of the kind imaging papers report, in the film. The interactive deals reported
correlations with the two measures' reliabilities; the reader judges each as possible or impossible, and the
page plots the answers against the ceiling.
*Ledger:* the N400 (`replicated`); brain-training transfer (`failed`); lie detection by fMRI (`not directly
tested`). Shown without rows, with reasons: the salmon, Hubel and Wiesel (due in Part 13), Berger, Ogawa,
Logothetis, Boynton, Eklund, Vul, Poldrack, the face area (due in Part 14), Barker, Marek, Elliott and Tang.
*In practice:* where the instruments are everyday tools (epilepsy, sleep, mapping before surgery, structural
scans) and what those uses share; a lie detector that is right nine times in ten flags as many truthful people
as liars at a base rate of one in ten, and a rehearsed toe movement took detection from 100% to 33% (Ganis et
al. 2011); brain training on 11,430 adults (Owen et al. 2010); six questions for any claim with a brain picture.
*Frontier:* brain-wide association studies (Marek et al. 2022): at 25 people and a true r of 0.06, 6% of
studies are significant and those report .47; 194, about 2,200 and about 78,000 people for r of 0.2, 0.06 and
0.01; the test-retest reliability of task fMRI (Elliott et al. 2020); the reply from multivariate models;
decoding the gist of a story (Tang et al. 2023) and its limits. Analysis methods at depth are Part 49.
*Reading:* Bennett et al. 2009; Hubel & Wiesel 1959; Berger 1929; Kutas & Hillyard 1980; Kutas & Federmeier
2011; Ogawa et al. 1990; Boynton et al. 1996; Logothetis et al. 2001; Eklund, Nichols & Knutsson 2016; Vul et
al. 2009; Kriegeskorte et al. 2009; Poldrack 2006; Barker et al. 1985; Owen et al. 2010; Ganis et al. 2011;
Elliott et al. 2020; Marek et al. 2022; Tang et al. 2023; Luck, *An Introduction to the Event-Related Potential
Technique*; Poldrack, Mumford & Nichols; Huettel, Song & McCarthy; Poldrack, *The New Mind Readers*.

### Part 9 · Genes and Evolution (~60)
*Question:* how much of who you are did you inherit, and what does that question mean?
*Story:* identical twins separated as babies meet at thirty-nine and find the same habits. The anecdote is worth
nothing; the design behind it is one of psychology's most replicated. This part derives what a twin study
estimates, shows on the Pool when it is right and wrong, lists what heritability is not, and follows the search
for the genes themselves, including a decade of findings that were not there.
0. Hook: the "Jim twins" (1979) and the Minnesota study. Two strangers compared on 200 things share about ten;
   anecdote against design; about 70% of IQ variance in twins reared apart (Bouchard et al. 1990).
1. Nature and nurture: Galton's families (1869) and the confound; two simulated worlds with the same
   parent-child correlation, told apart only by adoption; eugenics named, and deferred to Part 32.
2. From peas to bell curves: Mendel against the bell curve; 1, 2, 5 and 50 loci (Fisher 1918); a score as A + C +
   E and heritability as a share of variance; regression to the mean, whose slope is the heritability.
3. The logic of twins: two kinds of twins; Falconer's formula in four lines (0.50, 0.20, 0.30 recovered on the
   registry); the ACE model as a path diagram (the first in the series; returns in Part 44); 111 studies of
   test scores (Bouchard and McGue 1981).
4. On the Pool: 2,000 studies at each of four sizes (50 pairs: 95% of estimates between −0.05 and 1.07); one
   study fitted by maximum likelihood with bootstrap intervals; four assumptions switched off (equal
   environments 0.75, assortative mating 0.48, dominance 0.80 with a negative home, gene-environment
   correlation a home of 0.35); adoptive siblings, parent and child apart, and twins apart as checks.
5. On you: six traits, guessed and then revealed (language 0, schooling .40, personality .47, cognitive ability
   at seventeen .66, ADHD .74, schizophrenia .81; 49% across 17,804 traits).
6. What heritability is not: not fixed (height rose 20 cm in a century), not about groups (seed from one sack
   in two fields), not about a person (the rectangle), not a constant (the spread of environments; Turkheimer et
   al. 2003; Haworth et al. 2010).
7. Three laws and a puzzle: Turkheimer (2000) and Polderman et al. (2015); the shared home that counts for
   little; what is in the remainder; two cautions.
8. The candidate-gene decade: the serotonin transporter (Caspi et al. 2003); a variant explaining 0.02% needs
   39,237 people and a thousand give a 7% chance; a null gene analysed 18 ways is "significant" 38% of the time;
   the tests of 2009, 2012 and 2019 (Border et al.).
9. A million tests: the line at 5 × 10⁻⁸; a miniature genome at 2,000, 6,000 and 20,000 people (4, 57 and 179
   hits of 500, none false; the first hits 1.5 times too large); schooling: 3 positions, then 1,271, then 3,952.
10. What a polygenic score can say: built and tested out of sample (39%, against a formula's 38%); a score
    predicting 14% puts 76% of its top tenth above the median; smaller between siblings (0.30 against 0.50) and
    genetic nurture (Kong et al. 2018); missing heritability; epigenetics in two careful minutes.
11. Evolution as a source of hypotheses: the second "why"; 37 cultures (Buss 1989); just-so stories and what a
    testable claim needs; Betty the crow and her later qualification.
12. The Ledger. 13. In practice: what a genetic test can deliver. 14. Frontier: inside the family.

*Psyche:* `genes` (`explainer/psychology/psyche/genes.py`): the sum of L loci; families under the infinitesimal
model with switches for unequal environments, assortative mating, dominance and gene-environment correlation;
Falconer's estimates and a maximum-likelihood ACE fit; adoption and parent-offspring designs; two fields; power
for one variant and a flexibly analysed null gene; a genome-wide scan and polygenic scores; the sibling design
with genetic nurture and stratification; the gain from choosing among embryos.
*On you:* guess the heritability of six traits, in the film. The interactive shows the same trait in forty
identical and forty fraternal pairs; the reader decides from the two correlations whether genes or the shared
home account for more, and the page plots each trait against the lines "all genes" and "all home".
*Ledger:* twins and the heritability of psychological traits (`replicated`); candidate genes for behaviour
(`failed`); a polygenic score for years of schooling (`replicated`, about 40% smaller within families). Shown
without rows, with reasons: the Jim twins, Galton, Fisher, the three laws, the heritability that depends on wealth
and on age (due in Part 32), a century of height, the table of heritabilities, genetic nurture, the within-sibship
scan, height's variants, portability, the embryo simulation, mate preferences (due in Part 37), the famine and
methylation, and the crow.
*In practice:* genetic counselling for single-gene conditions against polygenic scores; a consumer score that
predicts 10% leaves a 67% chance of being above average for its top tenth and ±28 IQ points; choosing the best of
ten embryos gains about 3 points (2.5 in Karavani et al. 2019) and of a hundred about 5; six questions for any
claim about genes and behaviour.
*Frontier:* stratification (the chopsticks gene, simulated); within-sibship genome-wide studies (Howe et al.
2022); whose genomes (Martin et al. 2019); the missing heritability, how genetic nurture works, the path from a
variant to a behaviour, and what a score should be used for.
*Reading:* Knopik et al., *Behavioral Genetics*; Falconer & Mackay; Harden, *The Genetic Lottery*; Kevles, *In
the Name of Eugenics*; Galton 1875; Fisher 1918; Bouchard et al. 1990; Bouchard & McGue 1981; Polderman et al.
2015; Turkheimer 2000; Turkheimer et al. 2003; Haworth et al. 2010; Caspi et al. 2003; Risch et al. 2009; Chabris
et al. 2012; Border et al. 2019; Rietveld et al. 2013; Lee et al. 2018; Okbay et al. 2022; Kong et al. 2018; Howe
et al. 2022; Yengo et al. 2022; Martin et al. 2019; Karavani et al. 2019; Buss 1989; Gould & Lewontin 1979;
Heijmans et al. 2008; Weir et al. 2002.

### Part 10 · Chemistry and Clocks (~60)
*Question:* why is the same mind so different at four in the afternoon and at four in the morning?
*Story:* in 1938 Nathaniel Kleitman and a student live for a month in Mammoth Cave on a twenty-eight-hour day to
see whether the body would follow. The student's temperature rhythm stretches; Kleitman's keeps to twenty-four
hours with no sun to copy. The brain lives in a body with a clock, a pressure to sleep, hormones and drugs, and
each of these is a small model that can be written down and checked.
0. Hook: the cave (Kleitman 1939); two temperature rhythms, drawn; four things in the body that change the mind.
1. A clock inside: 24.18 hours in 24 people on a 28-hour day (Czeisler et al. 1999), and why earlier estimates
   said 25; Psyche's clock (a light-driven van der Pol oscillator) runs at 24.15; the suprachiasmatic nucleus and
   the loop of genes in each cell; on a 24-hour day the model locks, with its low point at 4:20; it follows days
   of 23 to 25 hours and not 22 or 26 to 28, so on the cave's day it does what Kleitman did.
2. Light sets the clock: the retina's third kind of light cell and melatonin; a phase response curve, computed
   (delays of up to 1.2 hours before the low point, advances of up to 0.8 after); a flight of six time zones
   takes 4 to 7 days to make up, with a caution that the model's direction is not the travellers'.
3. Sleep, found in the laboratory: 20 dream reports in 27 awakenings (Aserinsky and Kleitman 1953); four stages,
   drawn; a night's architecture in ninety-minute cycles.
4. Two processes (Borbély 1982): a pressure rising over 18.2 hours and falling over 4.2; thresholds moved by the
   clock; an eight-hour night; after 40 hours awake a recovery sleep of 8.6 hours, not sixteen; alertness lowest
   at 5:22 and higher the next afternoon without any sleep.
5. On you: chronotype as the midpoint of sleep on free days, and social jetlag; three example sleepers (45
   minutes, 1 h 30, 3 h 15); chronotype latest at about twenty (Roenneberg et al. 2004).
6. What sleep loss does: 8, 6 or 4 hours in bed for two weeks, by lot (Van Dongen et al. 2003); lapses add up
   with every hour awake beyond 15.84; ratings of sleepiness level off while lapses climb.
7. What sleep is for: an odour in slow-wave sleep and its four controls (Rasch et al. 2007); 91 experiments, g =
   0.29 (Hu et al. 2020); dreams: activation-synthesis (1977) against Solms (2000), a double dissociation.
8. The stress loop: a synapse against a hormone; hypothalamus, pituitary, adrenal and the brake; cortisol's day;
   a one-hour stressor is gone in 3.4 hours, and with the brake at 30% it is larger, slower, and the daily
   level 19% higher; organizing against activating (Phoenix et al. 1959); the Yerkes-Dodson curve's thin
   beginning (Teigen 1994; Part 28).
9. Four ways to change a synapse: mimic, block, hold, amplify (nicotine, caffeine, the reuptake blockers,
   alcohol); caffeine covers the gauge of sleep pressure; where a drug starts is not where it ends.
10. Dose and response: occupancy D/(D + K) from mass action; a blocker shifts the curve tenfold; three sites
    steepen it (4.3-fold against 81-fold); half-lives against alcohol's constant rate, from the same formula;
    three coffees leave 0.84 of a cup at 23:00.
11. Tolerance and withdrawal: the opponent process (Solomon and Corbit 1974); ten doses (the effect felt falls
    from 0.84 to 0.24, the low afterwards deepens to 1.07); the same dose in a different room (Siegel et al.
    1982: 32%, 64%, 96%).
12. The Ledger. 13. In practice: schedules, schools and insomnia. 14. Frontier: why do we sleep?

*Psyche:* `body` (`explainer/psychology/psyche/body.py`): the clock (free running, entrained, a phase response
curve, re-entrainment after a shift); the two-process model with forced waking and an alertness curve; lapses
under short sleep; a three-stage hormone loop with feedback; receptor occupancy with a blocker and a Hill
coefficient; first- and zero-order elimination and repeated dosing; an opponent process; tolerance tied to a
place; midsleep and social jetlag. The clock and the two-process model use published constants and are not
fitted here; the model makes no claim about an afternoon dip or about the direction of jet lag.
*On you:* four sleep times give a chronotype and a social jetlag, in the film. The interactive is a vigilance
task (watch for a light, respond, lapses counted) set beside the reader's own rating of how alert they feel,
block by block.
*Ledger:* REM sleep and dreaming (`replicated`); sleep loss and sustained attention (`replicated`); cueing a
memory in slow-wave sleep (`replicated, smaller`); short sleep and an early death (`contested`). Shown without
rows, with reasons: the cave, the clock's period, the two-process model, the two accounts of dreaming (due in
Part 27), chronotype across life (Part 31), the guinea pigs, the Yerkes-Dodson history (Part 28), the opponent
process (Part 41), Siegel's rats (Part 16), the Seattle schools, the insomnia trials (Part 42) and the two mouse
studies of clearance.
*In practice:* Seattle's later school start (34 minutes more sleep; a before-and-after comparison); behavioural
therapy for insomnia read as the two processes plus conditioning (20 trials: asleep 19 minutes sooner, 26 minutes
less awake); rosters built on descendants of the two-process model; caffeine arithmetic.
*Frontier:* why animals sleep at all (memory, synaptic downscaling, clearance, energy); does sleep wash the brain
(Xie et al. 2013 against Miao et al. 2024); who is hit hardest by sleep loss; what the pressure is made of;
whether REM sleep is for anything.
*Reading:* Kleitman, *Sleep and Wakefulness*; Miller, *Mapping the Darkness*; Roenneberg, *Internal Time*;
Borbély 1982; Daan, Beersma & Borbély 1984; Van Dongen et al. 2003; Solomon & Corbit 1974; Siegel et al. 1982;
Meyer & Quenzer, *Psychopharmacology*.

---

## Act III · Sensing

### Part 11 · The Threshold (~50)
*Question:* what is the smallest difference you can notice, and is there a law to it?
*Story:* on the morning of 22 October 1850 Fechner, in bed in Leipzig, sees how to measure the mind: count the
just noticeable steps between two stimuli. Weber had found that the step is a constant fraction; Fechner turns the
fraction into a logarithm, the first quantitative law of the mind. A century later Stevens asks people for numbers
and gets a power law. The quarrel is about what a step is worth, and the answer to what a threshold is, a curve
and not a point, sets up signal detection.
0. Hook: Fechner's morning (Fechner 1860, as told by Boring 1961); Kant's first objection, unanswered after ten
   parts; two pairs of grey patches, 24% and 2%.
1. Weber's fraction (1834): ΔI = kI, illustrated without a historical number; on Psyche (noise with a floor and a
   proportional part) a fraction of 0.076 over the middle, 0.48 near the floor; the near miss (McGill and
   Goldberg 1968).
2. Fechner's step: 90 just noticeable steps from 1 to 1,000, 30 a decade; the logarithm in four lines; the one
   assumption it rests on.
3. Three classical methods on Psyche: limits (14.1; descending 23.8, ascending 4.4), adjustment (PSE 102.2, a JND
   of 7.6 from the settings' spread), constant stimuli (8 × 40 trials); three willingnesses to say yes give 10.4,
   14.9 and 19.8 with the same eyes.
4. The threshold is a curve: four numbers (guess, threshold, spread, lapse); Gaussian, logistic and Weibull.
5. On you: eight pairs of patches, answered against an observer with a 7.6% JND.
6. Fitting: the binomial likelihood and its surface; a 75% threshold of 8.6 [6.3, 11.4] against a truth of 8.2
   (Wichmann and Hill 2001); goodness of fit by the bootstrap's deviance, which an observer whose threshold drifts
   between blocks passes as often as a steady one; one slip without a lapse rate moves the threshold from 8.1 to
   10.1.
7. Staircases and QUEST: p^k = 1/2 derived (Levitt 1971; a three-down median of 9.75 against 10.01); coarse steps
   sit low; QUEST (Watson and Pelli 1983); errors after 32 trials of 0.92, 0.75 and 0.36 log units.
8. Stevens (1957): magnitude estimation, straight lines on log-log axes, six exponents from 0.33 to 3.5,
   cross-modality matching (a predicted slope of 0.49).
9. Fechner against Stevens: one Weber's law and two assumptions (Ekman's form); hard to tell apart; Plateau's
   painters and the middle grey (1872: 44%, 27% or 18%; CIE lightness puts it at 18%); the range effect (1.34, 0.84,
   0.67 from one observer; Poulton 1968).
10. Where Weber's law comes from: growing noise or a compressed code, thresholds within 4%; the slope of threshold
    against background (0, 1/2, 1: dark light, the de Vries-Rose law, Weber).
11. Weber's law elsewhere: number (adults about 0.11; 3:4 at three, 5:6 at six; Halberda et al. 2008), time
    (scalar timing, Gibbon 1977), money (Bernoulli's logarithm of 1738; ten ducats worth 70 times more at ten
    than at a thousand).
12. The Ledger. 13. In practice: the audiometer's staircase (Hughson-Westlake), the eye chart, codecs, and the
    triangle test (15 of 30 to find a difference; 40 tasters for 80% power when 30% can taste it, 325 when 10%
    can). 14. Frontier: what the numbers measure; Thurstone's scale with no ruler (1927); the quick CSF (Lesmes et
    al. 2010).

*Psyche:* `psychophysics` (`explainer/psychology/psyche/psychophysics.py`): an observer with a noise floor, Weber
noise, photon noise, a lapse rate and a near miss; exact two-interval probabilities; psychometric functions in
three forms with guess and lapse rates; maximum-likelihood fits with a bounded lapse rate, the parametric
bootstrap and its goodness of fit; the three classical methods (limits with a criterion); k-down staircases and
their targets; a QUEST-style placement; Fechner's count; Stevens's power law, magnitude estimates and
cross-modality matching; the triangle test's critical counts and power; paired comparisons and Thurstone's Case V.
*On you:* eight pairs of patches in the film. The interactive is Battery task 2 on the reader's own screen: a
two-interval brightness task run by a 2-down 1-up staircase over 50 trials, with the reader's psychometric curve
fitted at the end.
*Ledger:* Weber's law (`replicated`, with its failures at the edges); Stevens's power law (`replicated`, for the
power form; the exponents move with the experiment). Shown without rows, with reasons: Levitt, QUEST and Wichmann
and Hill (methods), number sense (due in Part 30), scalar timing, the quick CSF and the square-root law (Part 13),
Bernoulli (Part 26), Plateau, and Thurstone (Part 46).
*In practice:* audiometry, eye charts, codecs measured in JNDs, the triangle test and its power.
*Frontier:* what is solid and what is argued in measuring sensation; scaling without a physical stimulus; adaptive
methods for whole curves; why the near miss; what the exponents measure.
*Reading:* Fechner 1860; Stevens 1957, 1975; Gescheider, *Psychophysics*; Kingdom & Prins, *Psychophysics: A
Practical Introduction*; Levitt 1971; Watson & Pelli 1983; Wichmann & Hill 2001; Poulton 1968; Thurstone 1927.

### Part 12 · Signal and Noise (~50)
*Question:* when you say "yes, I saw it", how much of that is seeing and how much is willingness to say yes?
*Story:* wartime radar observers miss real contacts, more as the watch wears on, and report ghosts. Mackworth's
Clock Test (1948) reproduces the decline, but a hit rate cannot tell an unseen target from an unspoken one.
Engineers at Michigan and then Tanner and Swets (1954) turn the trade-off into a theory with two numbers, one for
seeing and one for saying. It is the third objection's day in Kant's wager.
0. Hook: the radar screen; Mackworth's Clock Test; the third objection; objectives.
1. Four outcomes, two free numbers; one observer under five reward schemes (hits 97% to 37%, d′ 1.5 throughout);
   the correction for guessing slides from 0.87 to 0.29 with d′ fixed.
2. Two distributions and a line: d′ = z(H) − z(F) and c derived; two knobs; chapter 1 in the two numbers.
3. The ROC traced by sliding the criterion; the family by d′ and its area (0.856 = Φ(d′/√2)); two tests with the
   same area that cross (56% against 29% hits at 2% false alarms); a whole ROC from confidence ratings.
4. On you: twelve words studied, twenty-four tested; d′ from a table with the log-linear correction.
5. The ideal observer: the likelihood ratio and Neyman–Pearson; base rates and payoffs set β (1, 4, 19); at 5%
   prevalence the best line gets 95.2% and "always no" 95%.
6. Fitting: zROCs and slope 1/σ; a rating study fitted by maximum likelihood (slope 0.81, χ² = 5.5); recognition's
   slope of about 0.8 (Ratcliff, Sheu & Gronlund 1992).
7. Forced choice: Φ(d′/√2) derived; m alternatives and a lower floor.
8. Rivals: the high-threshold line against curved data; Yonelinas's recollection plus familiarity fits as well.
9. Base rates: the mammogram (8 of 103; Gigerenzer & Hoffrage 1995); Bayes's rule in odds (a second positive:
   41%); the same test at 1% and 10% prevalence.
10. The prevalence effect (Wolfe et al. 2005: 11%, 25%, 52%); a criterion that follows the base rate; Fleck and
    Mitroff's correctable search; threat-image projection.
11. The watch revisited: two watchers with one hit rate and opposite false alarms; See et al. (1995).
12. The Ledger. 13. In practice: signal, noise and criterion across fields; double reading (√2 if independent);
    police line-ups and the diagnosticity ratio (Mickes, Flowe & Wixted 2012); ROC against precision and recall.
    14. Frontier: what is solid and argued; confidence's own ROC and meta-d′ (Maniscalco & Lau 2012).

*Psyche:* `sdt` (`explainer/psychology/psyche/sdt.py`): equal- and unequal-variance observers; d′, c and β from
rates with the log-linear correction; ROCs, zROCs and their area; rating ROCs simulated and fitted by maximum
likelihood; the likelihood ratio and the ideal criterion under base rates and payoffs; two- and m-alternative
choice; high-threshold and dual-process ROCs; natural frequencies and predictive value; criteria that follow
prevalence.
*On you:* the in-film old/new test. The interactive is a recognition test with a six-point confidence scale that
draws the reader's ROC and gives d′, c and the area.
*Ledger:* the criterion moves while sensitivity stays (`replicated`); the prevalence effect (`replicated`);
recognition's zROC slope below one (`replicated`). Shown without rows, with reasons: Mackworth and See et al.
(Part 51), the mammogram (Part 26), meta-d′ (Part 25), Swets, Dawes & Monahan, and the line-up study (Part 21).
*In practice:* radiology and double reading, airport screening, alarms, line-ups, classifier ROC and
precision-recall.
*Frontier:* metacognition and meta-d′; whether the evidence is one-dimensional; criterion learning.
*Reading:* Tanner & Swets 1954; Swets, Tanner & Birdsall 1961; Green & Swets 1966; Macmillan & Creelman,
*Detection Theory*; Wickens, *Elementary Signal Detection Theory*; Swets, Dawes & Monahan 2000; Gigerenzer &
Hoffrage 1995; Wolfe et al. 2005; Mickes et al. 2012.

### Part 13 · The Eye and the Code (~55)
*Question:* what does the eye tell the brain?
*Story:* in 1942 Hecht, Shlaer and Pirenne sit in a dark room at Columbia and find that a flash is seen when five
to fourteen quanta are absorbed, spread over about 500 rods: a rod must answer a single quantum. But the eye does
not send pictures. It sends differences, across space, time and wavelength, and each stage can be written as a
filter. Colour turns out to be linear algebra. For Kant's first objection this is the strongest reply so far.
0. Hook: the dark room; from the cornea to the rods (54 to 148 quanta, 4% reflected, half absorbed, at most a fifth
   caught: 5 to 14); the eye sends differences; objectives.
1. Counting quanta: Poisson arrivals; the curve's steepness depends on k alone (0.80, 2.20, 2.71 for k = 1, 6, 9),
   and a loss only slides it; Psyche in the dark room (k = 6 recovered; within one of the truth 80% of the time);
   Baylor, Lamb & Yau's single rods (1 pA); Tinsley et al. (2016: 51.6%, P = 0.0545); photon noise and the
   square-root law.
2. Optics and the mosaic: the MTF and the diffraction limit (94 c/deg at 3 mm); cones 0.5 arcmin apart, Nyquist at
   60, an 80 c/deg grating aliased to 40; 20/20 as 30 c/deg.
3. Ten billion to one: the range of light; the Naka-Rushton curve that slides; gain control gives a Weber fraction
   of 4.1% over ten log units, a fixed gain saturates.
4. The retina sends differences: Adrian and Zotterman's rate code (the Ledger row deferred from Part 5); Kuffler's
   centre and surround; Rodieck's difference of Gaussians and its band-pass response; Mach bands computed; a 1/f
   texture's correlation two pixels apart, 0.60 before the filter and 0.11 after.
5. Edges in the cortex: Hubel and Wiesel's bar; the Gabor field (half-width 22°); simple and complex cells and the
   energy model; Reid and Alonso's paired recordings.
6. On you: the Campbell-Robson chart; the CSF and its four numbers (acuity 56 c/deg in the model); a hybrid image
   that reads E up close and A from across a room.
7. Channels and normalization: a bank of one-octave channels; Blakemore and Campbell's adaptation (up to fivefold);
   Heeger's divisive normalization, saturation and cross-orientation masking.
8. Three numbers for a spectrum: Newton, Young, Maxwell and Helmholtz; Stockman and Sharpe's cone fundamentals (570,
   545, 445 nm; rods 505); univariance; 79 numbers projected to three.
9. Colour matching as linear algebra: the 3-by-3 solve and negative weights; derived matching functions against
   Stiles and Burch's 1955 matches (r ≥ 0.9994); a null-space metamer that breaks under a warm lamp; the 1931
   diagram and a screen's gamut.
10. Opponent colours and colour blindness: Hering's puzzle; L − M, S − (L + M); colour deficiency (8% of men) as a
    lost dimension; a rainbow palette collapses (ΔE 39 to 7), Okabe and Ito's does not.
11. Constancy and the dress: von Kries; a stand-in swatch read under a warm and a cool light; Lafer-Sousa, Hermann &
    Conway (57%, 30%, 11%) and Wallisch (2017).
12. Two streams: Ungerleider and Mishkin; Goodale and Milner; D.F.'s slot task (schematic).
13. The Ledger. 14. In practice: screens, cameras and codecs on the standard observer; chroma subsampling (half the
    data); colour-blind-safe design. 15. Frontier: what is solid and argued; how close we are to understanding V1
    (Olshausen & Field 2005); twenty retinal output types; a tetrachromat (Jordan et al. 2010).

*Psyche:* `vision` (`explainer/psychology/psyche/vision.py`, twelve tests): frequency of seeing and its fit; the
diffraction MTF, blur, Nyquist and aliasing; Naka-Rushton gain control; differences of Gaussians, Mach bands and a 2-D
DoG; gratings, Gabor fields, simple and complex cells, orientation tuning; normalization; a truncated log-parabola
CSF, its fit, the Campbell-Robson chart and CSF filtering; the CIE 1931, Stiles-Burch and Stockman-Sharpe tables
(`archive/_colour_tables.py`, from cvrl.org); cone excitations, matching, matching functions for any primaries,
null-space metamers, chromaticity, sRGB; opponent channels, dichromacy, Planck spectra and von Kries.
*On you:* the Campbell-Robson chart and the hybrid image in the film; the course's interactive measures the reader's
contrast sensitivity at four stripe widths by interleaved staircases and draws the curve.
*Ledger:* a handful of quanta (`replicated`, with the single photon noted as resting on one study at P = 0.0545); the
rate code of a single fibre (`replicated`; deferred from Part 5); orientation-tuned cells (`replicated`); the CSF and
its channels (`replicated`); the dress's illuminant account (`replicated`). Shown without rows, with reasons: D.F.
(Part 27), the tetrachromat, the colour tables and Okabe and Ito's palette.
*In practice:* displays, cameras and sRGB; codecs and chroma subsampling; colour-blind-safe design.
*Frontier:* what V1 does with natural scenes; the retina's many output types; tetrachromacy.
*Reading:* Hecht, Shlaer & Pirenne 1942; Baylor, Lamb & Yau 1979; Kuffler 1953; Hubel & Wiesel 1959, 1962;
Campbell & Robson 1968; Blakemore & Campbell 1969; Heeger 1992; Stockman & Sharpe 2000; Lafer-Sousa et al. 2015;
Wandell, *Foundations of Vision*; Rodieck, *The First Steps in Seeing*; Hubel, *Eye, Brain, and Vision*.

### Part 14 · Seeing as Inference (~55)
*Question:* if every image fits many worlds, how does seeing choose one?
*Story:* two squares on a checkerboard send identical light and look different. That is the visual system
working: the image underdetermines the world, so seeing must be a bet. Helmholtz called it unconscious inference.
The modern version says which bet is optimal, and people come remarkably close. For Kant's third objection: cue
weights read from choices, never from reports, and an illusion that knowing does not undo.
0. Hook: the checkerboard in shadow (Psyche's own board, after Adelson 1995): both squares send 0.40; seeing is a
   bet; objectives.
1. The inverse problem: one 2° image from every size and distance on a line; the Ames room from above.
2. Grouping and the Gestalt laws: proximity, similarity, continuation and closure read as priors (edge statistics
   in natural images); Kanizsa's triangle and V2's illusory-contour cells (1984); Rubin's vase and border ownership
   (2000).
3. Depth from two eyes: disparity derived, δ ≈ IΔd/d² (1 cm gives 8.49′ at 0.5 m, 0.54′ at 2 m, 0.022′ at 10 m;
   thresholds of a few seconds of arc); Wheatstone's stereoscope (1838); a random-dot stereogram to free-fuse
   (Julesz 1960); the cues for one eye.
4. Constancy, and illusions: size constancy; Ponzo; Müller-Lyer and Gregory's misapplied constancy (1963); Segall,
   Campbell & Herskovits (1966), newly sighted children (Gandhi et al. 2015) and Amir & Firestone's reopening (2025).
5. Bayes for perception: the rule; a normal prior (0, 1.5) and measurement (4, 1) give a posterior of 2.77, σ 0.83;
   completing the square (precisions add, means are precision-weighted, w = 0.692); shrinkage as noise grows; the
   biased posterior mean's error 0.69 against 1.
6. Combining cues: the weights and the combined variance derived; Ernst & Banks (2002); Psyche at the bench (weights
   predicted 0.88 to 0.31 and recovered from conflict trials; combined σ predicted and measured within 2%), with the
   caution that Psyche is optimal by construction; the ventriloquist reversed (Alais & Burr 2004); children (Gori et
   al. 2008); departures (Rahnev & Denison 2018); why an advance prediction makes it a test.
7. Priors made visible: bumps and dents (light from above, Ramachandran 1988), retrained by touch (Adams, Graf &
   Ernst 2004); low contrast looks slower (Thompson 1982) under a slow prior (0.92, 0.50, 0.10 of the speed in the
   model); fog in a simulator (1998) and fog that thickens with distance (2012); the aperture problem and the MAP
   velocity for two edges (8° and 30° off course, at 0.82 and 0.44 of the speed, toward the vector average).
8. The two squares, explained: light as surface times illumination; retinex (Land & McCann 1971) gives 0.50 and 0.96
   (true ratio 2, found 1.94); where edges are not enough (Gilchrist 1977; Knill & Kersten 1991).
9. Recognizing objects: pixel templates fail (a disc nearer a square than the square moved); Marr's stages; geons
   (Biederman 1987), and the rival of remembered views (Bülthoff & Edelman 1992); 150 ms (Thorpe et al. 1996).
10. Faces: inversion (Yin 1969) and the composite face; a schematic Thatcher illusion; the fusiform face area (12 of
    15), face patches (97%), prosopagnosia and super-recognizers; greebles and the expertise dispute.
11. Deep networks as models: IT predicted (Yamins et al. 2014); a one-layer network trained here learns texture
    (283 of 299 conflict answers), and shape when textures are shuffled (147 to 66). Continued in Part 60.
12. The Ledger. 13. In practice: the vergence-accommodation conflict (Hoffman et al. 2008); disruptive colouring and
    countershading (Cuthill et al. 2005); stickers on a stop sign (2018) and the human in the loop.
14. Frontier: what is solid and argued; priors as world statistics (Geisler 2001; Stocker & Simoncelli 2006);
    Molyneux's question answered (Held et al. 2011); one child's head camera (Vong et al. 2024); what "Bayesian"
    commits you to (Bowers & Davis 2012; Part 58); Gibson's affordances.

*Psyche:* `infer` (`explainer/psychology/psyche/infer.py`, six tests): the normal posterior and reliability-weighted
combination; a two-interval observer with one or two cues and a conflict, with a cumulative-normal fit; speed under a
slow prior; edge constraints, the MAP velocity and the vector average; the checkerboard in shadow and retinex;
disparity, random-dot stereograms and size-distance invariance; textured shapes and a one-layer convolutional network
in numpy, with its texture bias.
*On you:* the checkerboard; a random-dot stereogram; bumps and dents; the Thatcher illusion. The course's interactive
measures the reader's own Müller-Lyer illusion with two interleaved staircases and reports the point of equality.
*Ledger:* reliability-weighted cue combination (`replicated`, with documented departures); low contrast looks slower
(`replicated`, for slow and moderate speeds); the Müller-Lyer illusion's dependence on culture (`contested`); the
fusiform face area (`replicated`; what it is selective for is argued). Shown without rows, with reasons: Adelson's
checkerboard, Adams et al. (2004), Yin (1969), Yamins et al. (Part 60), Geirhos et al., Vong et al. (Part 30) and
Wheatstone's stereoscope.
*In practice:* headsets and the vergence-accommodation conflict, camouflage, machine vision and the human in the
loop.
*Frontier:* where priors come from; what "Bayesian" commits a model to (Part 58); learning from one child's
experience (Part 30); Gibson.
*Reading:* Helmholtz, *Handbuch der physiologischen Optik*; Marr 1982; Knill & Richards (eds.) 1996; Ernst & Banks
2002; Weiss, Simoncelli & Adelson 2002; Palmer, *Vision Science*; Frisby & Stone, *Seeing*; Kanwisher, McDermott &
Chun 1997; Yamins et al. 2014; Geirhos et al. 2019.

### Part 15 · The Other Senses (~55)
*Question:* how do pressure waves become a voice, and why does pain not follow the injury?
*Story:* a sound with no energy at 200 Hz is heard at 200 Hz, and the film plays it. Békésy watched a wave travel
along the membrane, peaking in a different place for each pitch: the ear is a frequency analyser. Then the surprises:
a pitch that is not in the sound, a face that changes what a voice says, a rubber hand that becomes yours, and pain
that is a decision the nervous system makes. Act III ends here.
0. Hook and On you: six harmonics of 200 Hz, then harmonics 3 to 6, then a pure 200 Hz tone, all played; the
   telephone's missing fundamental; objectives.
1. Sound, and the decibel: a pressure wave; the decibel as Fechner's law in engineering (130 dB is 3.2 million times
   the pressure); Terhardt's threshold in quiet (most sensitive near 3.3 kHz; 40 dB more at 50 Hz); the audiogram.
2. The cochlea: the middle ear's pressure gain; von Békésy's travelling wave (Nobel 1961), with the caution that dead
   cochleas tune broadly; Greenwood's map; Kemp's emissions (1978), outer hair cells and the cochlear amplifier;
   Psyche's 48 gammatone filters, resolved and unresolved harmonics.
3. Filters and masking: Fletcher's band-widening (1940) and the critical band (241 Hz at 2 kHz); upward spread; what
   masking is for.
4. Pitch: Seebeck, Ohm and Schouten's residue; phase locking; Licklider's summary autocorrelation, run in Psyche (200
   Hz for harmonics 1–6, 3–6 and 5–8; Meddis and Hewitt 1991); place and time together; individual differences.
5. Where is it?: Rayleigh's duplex theory; Woodworth's delays (up to 656 µs; thresholds near 10 µs); Jeffress's
   coincidence circuit (1948) and Psyche's array (275 µs for a true 261 µs); owls and gerbils (Brand et al. 2002);
   the outer ear's filtering.
6. Auditory scene analysis: Cherry's cocktail party; Bregman; streaming played (500/560 Hz, then 500/1000 Hz; van
   Noorden 1975); harmonicity, onset, similarity and location as priors.
7. Speech: no acoustic invariant (the /d/ of "di" and "du"); categorical perception (Liberman et al. 1957; ABX from
   labels peaks at 0.69), corrected by McMurray et al. (2002); the McGurk effect (98% in 1976) as cue combination
   (88% /d/ in Psyche); individual differences from 0% to 100% (Mallick et al. 2015) and causal inference.
8. Music: roughness within a filter (Plomp & Levelt 1965); dips at the simple ratios for harmonic tones; a fifth and a
   tritone played; the Tsimane' (McDermott et al. 2016).
9. Touch and the body: four mechanoreceptor channels; two-point thresholds (2–3 mm on a fingertip, about 39 mm on the
   back); proprioception and tendon vibration (1972); the rubber hand (1998) and phenomenological control (Lush et
   al. 2020).
10. Pain: Descartes's bell rope; Beecher's soldiers; Melzack and Wall's gate (1965) as Psyche's circuit (rubbing cuts T
    from 1.00 to 0.44); TENS; phantom limbs and the mirror box; naloxone and placebo (Levine et al. 1978).
11. Smell and taste: Buck and Axel's receptor family; a combinatorial code; flavour is mostly smell; the tongue map
    (Hänig 1901, Boring 1942, Collings 1974); a trillion smells (Bushdid et al. 2014) and the reanalyses; a count of
    mixtures that moves from 62 to 2.4 × 10^14 with one threshold.
12. Balance, and the senses together: canals and otoliths; the vestibulo-ocular reflex; sensory conflict and motion
    sickness (Reason & Brand 1975).
13. The Ledger. 14. In practice: hearing aids that compress; cochlear implants (about 737,000 by 2019); perceptual
    coding; haptics and pain clinics. 15. Frontier: what is solid and argued; hidden hearing loss (Kujawa & Liberman
    2009); chronic pain as learning; the mismatch negativity.

*Psyche:* `hearing` (`explainer/psychology/psyche/hearing.py`, ten tests): decibels and the threshold in quiet;
harmonic complexes; the ERB scale, Greenwood's map, gammatone filters, excitation patterns, a schematic travelling
wave; summary autocorrelation and pitch; the power-spectrum model of masking; Woodworth's delay, phase-locked spikes and
a Jeffress array; identification and the label model of ABX; the McGurk effect as cue combination; the gate as a
circuit; a combinatorial count of odour mixtures. `VoiceoverScene.sound` lets the film play its demonstrations.
*On you:* the missing fundamental, streaming and two intervals, played in the film; two-point thresholds with a friend.
The course's interactive plays pairs of tones whose fundamental and harmonics move in opposite directions and reports
which the reader follows.
*Ledger:* the McGurk effect (`replicated`, with wide individual differences); categorical perception (`story and
record`); the rubber hand (`contested`); the tongue map (`story and record`); a trillion smells (`contested`). Shown
without rows, with reasons: von Békésy, Kemp, Melzack and Wall, Levine et al. (Part 57), McDermott et al., and Kujawa
and Liberman.
*In practice:* hearing aids and cochlear implants, perceptual audio coding, haptics, pain clinics.
*Frontier:* hidden hearing loss; chronic pain as learning; predictive models of auditory cortex.
*Reading:* von Békésy 1960; Moore, *An Introduction to the Psychology of Hearing*; Bregman, *Auditory Scene
Analysis*; Liberman et al. 1957; McGurk & MacDonald 1976; Melzack & Wall 1965; Wolfe et al., *Sensation & Perception*.

---

## Act IV · Learning

### Part 16 · Conditioning (~55)
*Question:* what, exactly, is learned when a signal comes to mean food?
*Story:* Pavlov's dogs salivate to a signal; the response fades in extinction and part of it is back the next day.
Two dogs with the same forty pairings learn different things if food also comes, for one of them, without the signal.
In 1968–69 two experiments break the idea that pairing is enough: Rescorla's random control and Kamin's blocking.
Learning is driven by surprise; in 1972 Rescorla and Wagner write it as one line, which is gradient descent on a
squared prediction error and whose asymptote is the contingency. Its failures show that extinction is new learning
bound to context, which is why fears return. Act IV begins here.
0. Hook: Pavlov's laboratory (Nobel 1904; metronomes and buzzers, the bell mostly legend, after Todes); acquisition,
   extinction and next-day recovery on Psyche; the two dogs; objectives.
1. Pavlov's method: US, UR, CS, CR and "conditional"; a generalization gradient and discrimination; experimental
   neurosis; substitution against preparation (freezing, conditioned tolerance from Part 10; Rescorla 1988).
2. The law of effect: Thorndike's puzzle box with Psyche's law-of-effect cat (one cat and the median of 200);
   Watson's behaviourism; Little Albert from the paper's own notes (seven pairings; Albert taken from the hospital
   with the fear in place), and as retold (Harris 1979; the disputed identity).
3. Skinner's box: the chamber and the cumulative recorder; shaping (79% rewarded against 0.3% when waiting for the
   target); FR, VR, FI and VI records with their signatures; the partial reinforcement extinction effect.
4. Contingency, not pairing: On you, the fertilizer game (24 plants, ΔP = 0 with blooms common); ΔP and the
   outcome-density effect; Wasserman et al. (1993); Rescorla (1968) Experiment 2, its ten groups and three statements.
5. Blocking: Kamin's design (1969); surprise; unblocking.
6. The Rescorla–Wagner rule: the terms; the derivation as gradient descent (Widrow and Hoff's delta rule; *AI, Built*
   Part 9); acquisition and extinction; blocking on the error surface over (V_noise, V_light).
7. What the rule predicts: overshadowing, conditioned inhibition and overexpectation (Kremer 1978); with the context
   as a cue the asymptote is ΔP (Chapman and Robbins 1990); Rescorla's ten groups on Psyche.
8. What the rule gets wrong: latent inhibition (Lubow and Moore 1959); renewal (Bouton and Bolles 1979) with a
   two-memory model, which wrongly makes AAB as strong as ABC; spontaneous recovery as a drifting context.
9. Attention to cues: Mackintosh (1975) against Pearce and Hall (1980), run on one history with opposite results;
   evidence for both in people.
10. Time: the peak procedure and the scalar property; the I/T law (Gallistel and Gibbon 2000) against Rescorla–Wagner.
11. Choice: the matching law (Herrnstein 1961; Baum 1979) from melioration on Psyche; exclusive choice on two ratio
    keys; the melioration trap (Herrnstein and Prelec 1991).
12. Biology's limits: Garcia and Koelling (1966); the Brelands' raccoon and pigs; preparedness; the Bobo doll
    (Bandura, Ross and Ross 1961) and monkeys' observational fear of snakes.
13. The Ledger. 14. In practice: exposure therapy designed around renewal; clickers, shaping and token economies;
    contingency management (d = 0.42 over 47 comparisons; fading after the rewards stop); loot boxes as variable-ratio
    schedules (Zendle and Cairns 2018). 15. Frontier: what is solid and argued; propositional learning (Mitchell, De
    Houwer and Lovibond 2009); latent causes and gradual extinction (Gershman, Blei and Niv 2010); reconsolidation
    (Schiller et al. 2010).

*Psyche:* `conditioning`: Rescorla–Wagner for any design and its exact asymptote, Mackintosh, Pearce–Hall, a
two-memory model of extinction, Thorndike's box, shaping, the four schedules, concurrent schedules chosen by
melioration, a melioration trap, scalar timing and the I/T law; each run on the classic designs.
*On you:* the gardener's game: four batches of plants, predictions that reveal the contingency learned.
*Ledger:* blocking (`replicated, smaller`: Maes et al. 2016); taste aversion (`replicated`); conditioned tolerance
(`replicated`, deferred from Part 10); Little Albert (`story and record`); the matching law (`replicated`); renewal
(`replicated`). Shown without rows, with reasons: Pavlov, Ferster and Skinner, Wasserman et al., Rescorla (1968),
Rescorla and Wagner, Lubow and Moore (Part 18), Mackintosh and Pearce–Hall, Gallistel and Gibbon, the Brelands,
Bandura et al., Prendergast et al. (Part 42), Zendle and Cairns, Mitchell et al., Gershman et al., Schiller et al.
(Part 21).
*In practice:* exposure therapy, animal training, token economies, contingency management for addiction; loot boxes
and variable rewards (Part 52).
*Frontier:* is learning associative or propositional in humans? Latent-cause models of extinction; reconsolidation.
*Reading:* Pavlov 1927; Rescorla 1968, 1988 ("It's not what you think it is"); Kamin 1969; Rescorla & Wagner
1972; Bouton, *Learning and Behavior*; Herrnstein 1961; Garcia & Koelling 1966; Gallistel & Gibbon 2000.

### Part 17 · Reward and Prediction (~55)
*Question:* how does a brain learn what to do when the reward comes later?
*Story:* a monkey gets juice and its dopamine neurons fire. After training they fire at the cue instead, and when
promised juice is withheld they fall silent at the moment it was due. In 1997 that recording is laid beside an
equation from computer science and they match; in 2013 light on dopamine neurons teaches a blocked cue. The same error
chooses actions, and can be read back from a person's choices. Then the cracks: rats that know a maze they were never
rewarded in, habits that ignore a devalued goal, people who plan, and dopamine that ramps, moves and encodes a whole
distribution.
0. Hook: Schultz's three recordings drawn on Psyche's TD learner (rasters and rates, not his figures); the 1997
   equation; the questions; objectives.
1. Credit over time: the problem Rescorla–Wagner cannot solve; Samuel's checkers; second-order conditioning on Psyche.
2. Temporal-difference learning: value as discounted future reward; the Bellman equation; the TD error derived (Sutton
   1988); TD-Gammon and *AI, Built* Part 26; a tapped delay line.
3. The error moves to the cue: the migration over 120 trials, computed; the error within one trial (first, trained,
   omitted) beside each case of the equation; probability and size scaling; Steinberg et al. (2013) as four bars from
   Rescorla–Wagner with the light added to the error.
4. From prediction to action: actor and critic; Q-learning and the softmax (Watkins 1989; DQN 2015); Go and NoGo;
   Frank, Seeberger and O'Reilly (2004), with Psyche's opponent learner, which reproduces the avoid-B side only.
5. A bandit, and your learning rate: a reversal bandit; α and β read back by likelihood (α 0.50 against a true 0.3);
   parameter recovery over 40 players (r = 0.90 for α, 0.70 for β).
6. Explore or exploit: five policies over 5,000 plays (Thompson 40, ε-greedy 83, UCB1 162, greedy 308); directed and
   random exploration with the horizon (Wilson et al. 2014), as a hand-set choice model.
7. Tolman's maps: latent learning on Psyche's planner against a learner without a map; cognitive maps and a shortcut;
   place cells (O'Keefe 1971) and grid cells (Hafting et al. 2005).
8. Habits and plans: devaluation after moderate and extensive training (Adams and Dickinson 1981); the two-step task
   (Daw et al. 2011) with three agents' stay probabilities; what the mixture weight means (Feher da Silva and Hare
   2020).
9. Between habit and plan: the successor representation, M = (I − γT)⁻¹; reward and transition revaluation for three
   learners (Momennejad et al. 2017); replay, forward and backward.
10. Is dopamine only an error? Ramps (Howe et al. 2013), movement and salience; a distributional code of expectile
    learners (Dabney et al. 2020).
11. When the signal is hijacked: Redish (2004), a drug that cannot be predicted away; continued in Part 41.
12. The Ledger. 13. In practice: contextual bandits (Li et al. 2010) and a bandit test against an even split;
    impulse-control disorders on dopamine agonists (Weintraub et al. 2010: 13.6%, 17.1% against 6.9%); habits by
    design. 14. Frontier: what is solid and argued; Harlow's learning sets and meta-reinforcement learning (Wang et al.
    2018); open questions.

*Psyche:* `rl`: TD(0) with a complete serial compound and second-order conditioning; Q-learning bandits, their
likelihood and fit; five exploration policies with regret; a maze with a planner and a model-free learner; the two-step
task with model-free, model-based and hybrid agents; the successor matrix and both revaluations; distributional TD;
Redish's model.
*On you:* two slot machines: eighty pulls, a swap after forty, and your α and β fitted on the page.
*Ledger:* dopamine reward-prediction errors (`replicated`; scope argued); the two-step model-based signature
(`replicated`; the weight's meaning contested); latent learning (`replicated`); grid cells (`replicated`). Shown
without rows, with reasons: Frank et al., Wilson et al., Tolman (1948), Adams and Dickinson (row due in Part 28),
Momennejad et al., Howe et al., Dabney et al., Redish (row due in Part 41), Li et al., Weintraub et al., Wang et al.
*In practice:* recommender systems and bandit tests are this mathematics; impulse-control disorders on agonists;
habits, made and broken.
*Frontier:* what dopamine ramps mean; whether humans are ever purely model-free; meta-reinforcement learning in
prefrontal cortex (Part 58).
*Reading:* Schultz, Dayan & Montague 1997; Sutton & Barto, *Reinforcement Learning* (ch. 14–15 on psychology and
neuroscience); Tolman 1948; Daw et al. 2011; Niv 2009; Dabney et al. 2020; Dayan & Daw 2008.

---

## Act V · Thinking

### Part 18 · Attention (~55)
*Question:* why do you miss a gorilla, and what is the thing you were doing instead?
*Story:* half of the observers counting basketball passes fail to see a person in a gorilla suit walk through, and a
large change in a flickering photograph takes seconds to find. Attention was psychology's first reason to draw a box
inside the head (Broadbent's filter, 1958). Sixty years of experiments moved the filter, split it and finally replaced
it with something a circuit can do: competition, and a gain that multiplies before a division. Act V begins here.
0. Hook: Simons and Chabris (1999; 46% of 192 missed the visitor); Rensink, O'Regan and Clark's flicker (1997: 0.9 s
   without blanks, 4.7 s and 10.9 s with them); the questions; objectives.
1. Cherry's cocktail party (1953) and shadowing; Broadbent's split span; the filter as the first information-flow
   diagram.
2. Your own name gets through (Moray 1959; Wood and Cowan 1995); Treisman's attenuator (1960) run on Psyche as signal
   and noise against word thresholds; late selection (Deutsch and Deutsch 1963); Lavie's load (1995) and its critics.
3. Posner's cueing (1980): benefits and costs on Psyche; endogenous against exogenous cues; inhibition of return
   (Posner and Cohen 1984).
4. On you: a feature and a conjunction display; set-size functions; Treisman and Gelade's slopes (about 29 and 67 ms).
5. Feature integration theory and illusory conjunctions; guided search on Psyche (slopes 0/3, 12/35 and 23/47 ms an
   item for feature, conjunction and T-among-L searches); a computed saliency map with a scan path (Itti, Koch and
   Niebur 1998); selection history (latent inhibition from Part 16; Anderson, Laurent and Yantis 2011; Awh et al.
   2012).
6. Change blindness fitted on Psyche to Rensink's means; attentional set (Most et al. 2001); radiologists and the
   gorilla (Drew, Võ and Wolfe 2013: 20 of 24).
7. The attentional blink (Raymond, Shapiro and Arnell 1992) as a two-stage model; the psychological refractory period
   and its slope of −1 under a central bottleneck (Pashler 1994), with Part 1's stages.
8. Stroop (1935; 74% more time) on you and as a two-pathway diffusion with its asymmetry and delta plot; flankers
   (Eriksen and Eriksen 1974), conflict monitoring and the sequence effect (Botvinick et al. 2001; Gratton et al.
   1992); task switching (Rogers and Monsell 1995).
9. Moran and Desimone's V4 (1985) and biased competition; the normalization model of attention (Reynolds and Heeger
   2009) derived, with contrast gain and response gain from the sizes of stimulus and attention field (Herrmann et al.
   2010).
10. Bundesen's theory of visual attention (1990) and whole report.
11. Mackworth's clock revisited as attention; the prevalence effect refitted to Wolfe et al.'s three points (d′ 2.48,
    a criterion moved 69% of the ideal way); Fleck and Mitroff's correctable search.
12. Phones and driving (Strayer and Johnston 2001: misses more than doubled, hands-free no better); media multitasking
    (Ophir et al. 2009) and its replications (Wiradhany and Nieuwenstein 2017).
13. The Ledger. 14. In practice: professional search, satisfaction of search and test-image insertion; alarm fatigue;
    driving law and in-car screens; ad viewability. 15. Frontier: what is solid and argued; rhythmic sampling
    (Landau and Fries 2012, contested); attention in transformers (Part 60).

*Psyche:* `attention`: the dichotic attenuator and load; cue effects with inhibition of return; guided search with a
quitting threshold; a centre-surround saliency map and scan path; prevalence as a criterion shift; the flicker
paradigm; the attentional blink; the PRP; a diffusion simulator, the Stroop task as two pathways and conflict
monitoring; the normalization model of attention; Bundesen's whole report; a vigilance watch.
*On you:* Battery tasks 3 (Stroop) and 4 (visual search) run on Psyche; the interactive is visual search, with the
reader's set-size functions and slopes.
*Ledger:* latent inhibition (`replicated`, deferred from Part 16); the Stroop effect (`replicated`); inattentional
blindness (`replicated`); Posner cueing (`replicated`); the attentional blink (`replicated`); media multitasking harms
attention (`contested`). Shown without rows, with reasons: Rensink et al., Cherry, Broadbent, Moray, Treisman, Lavie,
Treisman and Gelade, Wolfe, Itti and Koch, Anderson et al., Pashler, Botvinick et al., Rogers and Monsell, Moran and
Desimone, Reynolds and Heeger, Bundesen, Mackworth (row due in Part 51), Strayer and Johnston.
*In practice:* professional search and screening, alarm design, distracted-driving law, attention metrics in
advertising.
*Frontier:* is attention one thing? Rhythmic sampling; attention in networks against attention in brains (the shared
word, Part 60).
*Reading:* Broadbent 1958; Treisman & Gelade 1980; Posner 1980; Stroop 1935; Desimone & Duncan 1995; Reynolds &
Heeger 2009; Wolfe 2021 (Guided Search 6.0); Carrasco 2011; Simons & Chabris 1999; Pashler 1998.

### Part 19 · Working Memory (~50)
*Question:* how much can you hold in mind at once, and what is the limit made of?
*Story:* George Miller is "persecuted by an integer". Seven turns out to be closer to four, then turns out not to
be an integer at all: is the limit a number of slots or a resource that is spread thinner? The argument is
settled, as far as it is, by fitting models to the errors people make, here to an open dataset of 7,271 trials.
Then an industry promises to raise the limit.
0. Hook: digit span on you (5, 7 and 9 digits); Miller's confession; the questions; objectives.
1. Absolute judgment as a channel, computed (a noisy percept labelled by the nearest category levels off near 2.7
   bits, about six categories); span counts chunks, not bits (about 9 binary digits, 7 decimal, 5 words); recoding
   performed (eighteen binary digits as six octal ones; Smith's 40); chess and chunks.
2. Sperling (1960): whole report about 4.5 letters, partial report about 9 of 12; the icon fading on Psyche (i =
   0.62, τ = 250 ms); Neisser's iconic memory.
3. Brown, and Peterson and Peterson (1959): about 80% at 3 s, 10% at 18 s; Keppel and Underwood (1962): no forgetting
   on the first trial; release from proactive interference (Wickens); SIMPLE's temporal distinctiveness derived
   (Brown, Neath and Chater 2007) and run trial by trial.
4. The modal model (Atkinson and Shiffrin 1968) and patient K.F. (a span of about two, normal learning); Baddeley and
   Hitch (1974): dual-task logic, the loop, the sketchpad, the executive, the episodic buffer (2000); the word-length
   effect (Baddeley, Thomson and Buchanan 1975) and articulatory suppression on Psyche's loop (spans 6.2 and 3.0,
   2.4 under suppression); span against speech rate, and digit spans across languages.
5. Sternberg's memory scanning (1966: 37.9 ms per item from 397 ms); exhaustive against self-terminating search; an
   unlimited parallel search curves, and a limited-capacity parallel search reproduces the serial line and its
   distribution exactly (Townsend 1972), derived.
6. Four, not seven: change detection (Luck and Vogel 1997); Cowan's and Pashler's K derived and recovered on Psyche
   (K = 3.5); Cowan (2001), 4 ± 1; subitizing.
7. Slots or resources on Bays, Catalao and Husain's open data (2009; 12 observers, set sizes 1 to 6): error spreads
   of 16 to 63 degrees; the mixture model (Zhang and Luck 2008: g from 0.01 to 0.44, s.d. 14 to 22 degrees, levelling
   off); swap errors (27% at six squares); slots, slots plus averaging, equal and variable precision fitted to every
   observer (variable precision best for 11 of 12; van den Berg et al. 2012, 2014); a variable-precision observer who
   never guesses yields g = 0.49 and K ≈ 3.05 from the mixture.
8. Delay activity (Funahashi, Bruce and Goldman-Rakic 1989); a ring attractor computed: a bump that holds and diffuses,
   s.d. 5 to 14 degrees over 0.5 to 4 s, variance linear in delay (Wimmer et al. 2014); activity-silent memory
   (Mongillo, Barak and Tsodyks 2008; Rose et al. 2016).
9. Complex span (Daneman and Carpenter 1980; r about 0.41 with comprehension); working memory and fluid intelligence
   (about 0.72 latent, about 0.45 between tasks; Kane et al. 2005), with Part 3's attenuation.
10. Dual n-back (Jaeggi et al. 2008); an active control (Redick et al. 2013); the meta-analysis (Melby-Lervåg et al.
    2016: 87 publications, 145 comparisons); Psyche's 400 trials against two controls; the 2014 consensus and reply;
    Simons et al. (2016); the FTC and Lumosity ($2 million, $50 million suspended).
11. The Ledger. 12. In practice: chunked codes, forms and interruptions; read-backs and checklists; span as a clinical
    measure. 13. Frontier: settled and open; a shared information budget fitted to the open data (2.3 bits; Sims et al.
    2012; van den Berg and Ma 2018; Part 58); the focus of attention, Oberauer's benchmarks, small workspaces and large
    contexts (Part 60).

*Psyche:* `wm`: absolute judgment as a channel; the phonological loop with suppression; partial report; SIMPLE;
memory scanning, serial and parallel; slots and the K formulas; von Mises precision, the mixture and swap models and
four process models fitted by maximum likelihood; a ring attractor; brain-training trials; a shared information
budget. `opendata`: Bays et al. (2009), fetched on first use and checked by SHA-256.
*On you:* digit span in the film; Battery task 5 (change detection) runs on Psyche; the interactive is change
detection, with the reader's K at four set sizes.
*Ledger:* partial-report superiority (`replicated`); forgetting in eighteen seconds by decay (`story and record`);
the word-length effect (`replicated`); linear memory scanning (`replicated`); capacity near four (`replicated`);
working-memory training raises intelligence (`failed`). Shown without rows, with reasons: Miller, Shallice and
Warrington, Baddeley and Hitch, Zhang and Luck, Bays et al., Funahashi et al., Wimmer et al., Mongillo et al., Daneman
and Carpenter, Kane et al., Simons et al., the FTC.
*In practice:* chunked codes and forms, interruptions, read-backs and checklists, cognitive assessment; the
brain-training market as a case study in evidence.
*Frontier:* slots against resources is not closed; persistent against silent codes; whether capacity limits are a
bug or an optimal trade (Part 58).
*Reading:* Miller 1956; Sperling 1960; Baddeley & Hitch 1974; Cowan 2001; Luck & Vogel 1997; Zhang & Luck 2008;
Bays, Catalao & Husain 2009; van den Berg et al. 2012; Ma, Husain & Bays 2014; Oberauer et al. 2018 (benchmarks);
Simons et al. 2016.

### Part 20 · Memory I: Storing and Finding (~55)
*Question:* when you remember, what is being searched, and with what?
*Story:* in 1885 Hermann Ebbinghaus publishes the first experiments on memory, with one subject, himself, and
2,300 invented syllables. The next century finds lawful curves in what people recall and in what order. The best
account is a search: you remember with a cue, and the most important cue is the slowly drifting context of your
own mind. Fitted to 3,528 open lists, that account predicts each next word far better than position alone, and
fails one test that shows what it lacks.
0. Hook: Ebbinghaus's method and savings; free recall of a sixteen-word list on you; the questions; objectives.
1. Ebbinghaus's seven savings with three laws fitted (his formula k = 1.82, c = 1.21; a power law; an exponential
   that cannot bend both ways); ACT-R's base-level activation (one, three and ten uses); Anderson and Schooler
   (1991): forgetting tracks the odds of need.
2. Scoring your sheet; serial position and first recall on PEERS (126 people, 3,528 lists: 82%, about 57%, 92%; 45%
   of recalls start at the last word); Murdock (1962); Glanzer and Cunitz (1966) and Rundus (1971): two stores.
3. The lag-CRP derived with its denominators (a worked sequence); contiguity on PEERS (+1 0.45, −1 0.26); person by
   person (89% lean forward, 98% show recency; Healey and Kahana 2014); long-term recency (Bjork and Whitten 1974;
   Baddeley and Hitch's rugby players; Howard and Kahana 1999).
4. Levels of processing (Craik and Lockhart 1972; Craik and Tulving 1975: about 15, 48 and 81% recognised); transfer-
   appropriate processing (Morris, Bransford and Franks 1977); the generation effect (Slamecka and Graf 1978;
   Bertsch et al. 2007, d = 0.40); the method of loci (Dresler et al. 2017).
5. Encoding specificity (Tulving and Thomson 1973); the divers (Godden and Baddeley 1975: 13.5, 8.4, 8.6, 11.4) and
   Murre's replication from his open data (2021: per-diver effect −1.25 words, exact sign-flip p = 0.055; a warm
   pool, one session); Smith and Vela (2001); state dependence (Goodwin et al. 1969; Eich 1980).
6. SAM (Raaijmakers and Shiffrin 1981): the rehearsal buffer, sampling, recovery, stopping, simulated; symmetric
   contiguity and no long-term recency.
7. The temporal context model derived (Howard and Kahana 2002; CMR, Polyn, Norman and Kahana 2009): the drift and
   ρ = √(1 − β²); context similarity ρ^|i−j|; recency from a choice rule and the ratio argument; contiguity's forward
   lean from reinstated context.
8. CMR fitted by maximum likelihood to every other PEERS list (nine parameters; ρ = 0.31, γ = 0.10); checked on the
   other half (2.67 bits per recall against 3.23 for serial position alone and 3.30 for chance); tested on two other
   designs: it reproduces Glanzer and Cunitz and fails Bjork and Whitten (Sederberg, Howard and Kahana 2008 pass).
9. Memories as attractors: the Hopfield network (1982), its energy argument, a ring recovered from a corrupted cue,
   capacity derived from crosstalk and computed (0.138 N; Amit, Gutfreund and Sompolinsky 1985); modern Hopfield
   networks and attention (*AI, Built*).
10. Memory systems: H.M. again (Scoville and Milner 1957; Milner 1962); episodic and semantic (Tulving 1972); Squire's
    taxonomy; priming in amnesia (Warrington and Weiskrantz 1970; Graf, Squire and Mandler 1984); what dissociations
    can show (Part 7).
11. Recognition: the butcher on the bus (Mandler 1980), remember and know (Tulving 1985); dual-process and unequal-
    variance ROCs and z-ROCs (Yonelinas 1994; Part 12); where the two processes are (Yonelinas et al. 2002; Wixted
    2007; Squire et al. 2007).
12. The hippocampus as an index (Marr 1971; Teyler and DiScenna 1986); pattern separation computed (inputs sharing
    80% give codes sharing 38%; Leutgeb et al. 2007); time cells (MacDonald et al. 2011), context reinstatement in
    the brain (Manning et al. 2011), engrams (Part 5).
13. The Ledger. 14. In practice: the cognitive interview (Köhnken et al. 1999: d = 0.87, 85% against 82% accurate);
    telescoping and landmarks in surveys (Loftus and Marburger 1983); word-list tests in the clinic. 15. Frontier: one
    system or many (Berry, Shanks and Henson 2008); from lists to lives (Uitvlugt and Healey 2019); induction heads
    that behave like CMR (Ji-An et al. 2024).

*Psyche:* `memory`: forgetting laws; the serial-position curve, first recall and the lag-CRP; SAM; CMR with distractor
drift, its exact likelihood and a maximum-likelihood fit, against a serial-position baseline; a Hopfield network and
its capacity; ACT-R's activation; dual-process and unequal-variance ROCs; pattern separation. `opendata`: PEERS free
recall (from the psifr wheel) and Murre's divers (from his OSF workbook), fetched on first use and checked by SHA-256.
*On you:* free recall of a sixteen-word list in the film; the interactive is free recall (three lists of ten), with
the reader's serial-position and lag-CRP curves.
*Ledger:* serial position (`replicated`); contiguity (`replicated`); levels of processing (`replicated`); the
generation effect (`replicated`); encoding specificity (`replicated`); underwater context dependence (`contested`).
Shown without rows, with reasons: Ebbinghaus (Part 21), Anderson and Schooler, SAM and Hopfield (models), H.M., the
systems taxonomy and priming dissociations, recognition's two processes, indexing theory, time cells and the engram,
Dresler et al. (Part 54), Köhnken et al. (Part 56), Loftus and Marburger, Berry et al., Ji-An et al.
*In practice:* the cognitive interview, survey recall and landmarks, memory assessment in the clinic.
*Frontier:* one memory system or many; whether context models scale from lists to lives; context models inside
language models.
*Reading:* Ebbinghaus 1885; Murdock 1962; Tulving & Thomson 1973; Raaijmakers & Shiffrin 1981; Howard & Kahana
2002; Polyn, Norman & Kahana 2009; Hopfield 1982; Kahana, *Foundations of Human Memory*; Baddeley, Eysenck &
Anderson, *Memory*.

### Part 21 · Memory II: Forgetting and Inventing (~55)
*Question:* why do we forget, and why do we remember things that never happened?
*Story:* Elizabeth Loftus shows people a film of a car crash and changes one word in the question. A week later
those asked about cars that "smashed" remember broken glass. There was none. Memory loses what it had and gains what
it never had, and both come from one design: a memory that keeps the gist, rewrites itself when used, and has to
infer where its contents came from. The same mechanisms say how to study, and how not to run a line-up.
0. Hook: Loftus and Palmer (1974: speeds of 40.8 to 31.8 mph by the verb; broken glass 16, 7 and 6 of 50); the DRM
   SLEEP list and a remember/know test on you; the questions; objectives.
1. The shape of forgetting: savings for Ebbinghaus, Mack and Seitz (Heller et al. 1991) and Dros (Murre and Dros
   2015) with a possible jump at a day; four laws compared by AIC (the power law best for three of four, the
   logarithm for Dros, the exponential never); Jost's law from the power law's hazard b/t; the averaging artefact
   derived (a gamma mixture of exponentials is (1 + θt)^−k; Anderson and Tweney 1997).
2. Why: decay or interference (Jenkins and Dallenbach 1924); proactive interference (Underwood 1957: about 75% to
   25%); retroactive interference in a linear associator against cue overlap; retrieval-induced forgetting (Anderson,
   Bjork and Bjork 1994; Murayama et al. 2014).
3. Consolidation: Müller and Pilzecker (1900), Ribot's gradient, H.M.; a two-store model solved in closed form
   (after Alvarez and Squire 1994); replay in sleep (Wilson and McNaughton 1994) and targeted memory reactivation
   (Rasch et al. 2007); reconsolidation (Nader, Schafe and LeDoux 2000) and its record in people (Hardwicke, Taqi and
   Shanks 2016).
4. Two ways to learn: catastrophic interference (McCloskey and Cohen 1989); Rumelhart's semantic network taught the
   penguin, focused (a robin now flies 0.36 and swims 0.35) or interleaved (it still flies 0.84); complementary
   learning systems (McClelland, McNaughton and O'Reilly 1995) and replay buffers.
5. Spacing: Ebbinghaus's 38 against 68 repetitions; Cepeda et al. (2006, 2008: 1,354 people, 26 gap-by-interval
   cells, optimal gaps of about 3, 8, 12 and 27 days); Pavlik and Anderson's activation-dependent decay derived and
   run: the model's best gaps (48, 18, 12 and 6% of the interval) match the timing, and its gains are far too small.
6. Testing: Roediger and Karpicke (2006: restudy wins at 5 minutes, testing by 14 points at 2 days and a week;
   SSSS against STTT, 40 against 61% a week later, with the opposite predictions); the bifurcation model (Kornell,
   Bjork and Garcia 2011) derived and fitted (a recall adds 1.3 times what a re-reading adds; 75% predicted on the
   first test, about 70% observed).
7. Remembering as rebuilding: Bartlett's War of the Ghosts (1932) and its replication (Bergman and Roediger 1999);
   Huttenlocher, Hedges and Duncan's dots (1991); the category adjustment model derived as a posterior mean, and
   computed (bias toward the prototype; error 15.4° instead of 19.9° for the noisiest trace).
8. Words that were never there: the viewer's test scored; Roediger and McDermott (1995: lure recall .40 and .55,
   recognised .84 against .86, 72% "remembered"); global matching derived (after Arndt and Hirshman 1998) and
   computed; activation-monitoring and fuzzy-trace accounts.
9. Suggestion: misinformation (Loftus, Miller and Burns 1978); source monitoring (Johnson, Hashtroudi and Lindsay
   1993); lost in the mall (Loftus and Pickrell 1995; Scoboria et al. 2017: 30% of 423; Murphy et al. 2023: 35%) and
   what it does not show; verbal overshadowing (Schooler and Engstler-Schooler 1990: −25 points) and the first
   Registered Replication Report from its open data (Alogna et al. 2014: −16 points in 22 labs, −4 in 31).
10. Confidence and accuracy: flashbulb memories (Brown and Kulik 1977; Neisser and Harsch; Talarico and Rubin 2003);
    Jennifer Thompson and Ronald Cotton; Wixted and Wells (2017); a line-up by signal detection with the max rule
    and the confidence-accuracy characteristic computed (Wixted and Mickes 2014).
11. Remembering too much: S. (Luria 1968); highly superior autobiographical memory (Parker, Cahill and McGaugh 2006)
    and its false memories (Patihis et al. 2013); why a good memory forgets (Richards and Frankland 2017).
12. The Ledger. 13. In practice: Dunlosky et al.'s ten techniques (2013); Leitner's boxes, SuperMemo and half-life
    regression (Settles and Meeder 2016) fitted to simulated learners and checked on held-out practice; line-up
    procedures (Wells et al. 2020), interviews, imagination inflation in therapy (Garry et al. 1996). 14. Frontier:
    weakening fear by reconsolidation (Kindt, Soeter and Vervliet 2009; Brunet et al. 2018); silent engrams (Ryan et
    al. 2015); elastic weight consolidation, replay and unlearning in machines (Kirkpatrick et al. 2017).

*Psyche:* `memory` (Part 21's half): four forgetting laws with AIC, Jost's law and the gamma mixture; associator
interference; a two-store consolidation model; Rumelhart's semantic network and the penguin; Pavlik and Anderson's
spacing model and ridge; the bifurcation model and its fit; category adjustment; DRM by global matching; line-ups
by signal detection with the CAC; half-life regression. `opendata`: the two verbal-overshadowing workbooks
(osf.io/ybeur), fetched on first use and checked by SHA-256.
*On you:* the DRM list and a remember/know test in the film; the interactive is a DRM experiment (four lists, each
built around a word it leaves out, with remember, know or new).
*Ledger:* the forgetting curve (`replicated`; Part 20's deferred row); the spacing effect (`replicated`); the
testing effect (`replicated`); DRM false memory (`replicated`); the misinformation effect (`replicated`); implanted
memories (`replicated`); reconsolidation updating in people (`contested`); verbal overshadowing (`replicated,
smaller`). Shown without rows, with reasons: the interference and consolidation history, retrieval-induced
forgetting, the models (Pavlik and Anderson, Kornell et al., Huttenlocher et al., McClelland et al., Wixted and
Mickes), Bartlett, source monitoring, Luria's S., flashbulb memories and eyewitness confidence (Part 56), the
study-techniques review (Part 54), and the frontier.
*In practice:* study techniques, spaced-repetition software with half-life regression, line-ups, interviews and
therapy.
*Frontier:* weakening memories by reconsolidation; silent engrams and whether forgetting is lost storage or lost
access; continual learning and unlearning in machines.
*Reading:* Loftus & Palmer 1974; Murre & Dros 2015; Wixted & Ebbesen 1991; Underwood 1957; McClelland, McNaughton &
O'Reilly 1995; Cepeda et al. 2008; Roediger & Karpicke 2006; Bartlett 1932; Roediger & McDermott 1995; Alogna et al.
2014; Wixted & Wells 2017; Schacter, *The Seven Sins of Memory*; Brown, Roediger & McDaniel, *Make It Stick*.

### Part 22 · Concepts and Categories (~60)
*Question:* what do you know when you know what a bird is?
*Story:* Aristotle said a concept is a definition. Wittgenstein asked for the definition of "game", and Eleanor
Rosch showed that people agree a robin is a better bird than a penguin. If concepts are not definitions, are they
averages or remembered examples? The two answers become two equations, six small problems show that attention has
to learn, and Roger Shepard finds a law of generalization he argues should hold for any mind anywhere. Then
similarity itself is questioned: by Tversky's asymmetries, by networks of knowledge, by theories that override
resemblance, by a learner that needs three examples, and by meaning read from the company words keep.
0. Hook: true or false, as fast as you can (a robin, a penguin, a bat is a bird); Rosch's typicality ratings as a
   ladder; McCloskey and Glucksberg's borderline items; the questions; objectives.
1. No definition: the classical view; Wittgenstein's games; family resemblance computed on Psyche's bird table
   (Rosch and Mervis 1975); fuzzy boundaries (McCloskey and Glucksberg 1978; Hampton 1998, as a schematic).
2. The average member: Posner and Keele's dot patterns (1968, 1970); Homa and Vosburgh (1976) from catlearn's open
   data (prototypes .92 to .99, rising with category size); the prototype model as four equations.
3. Every member remembered: the context model (Medin and Schaffer 1978); the generalized context model derived
   (Nosofsky 1986); the 5-4 structure, where A2 beats A1 for exemplars and loses for the prototype; the debate
   (Medin and Schwanenflugel 1981; Smith and Minda 2000; mimicry, Part 48).
4. Six problems, and attention that learns: Shepard, Hovland and Jenkins (1961) as cubes; Nosofsky et al. (1994)
   from the open data; a delta-rule network that cannot learn II and VI and an equal-attention exemplar model that
   orders II wrongly; ALCOVE derived (Kruschke 1992) and fitted (SSE .209 against .335 without attention learning),
   with VI still too easy at the fitted values, said so.
5. A map of similarity: classical scaling derived (Torgerson's double centring) and non-metric scaling (Shepard,
   Kruskal); Ekman's 14 colours close into Newton's circle (stress .029); Rothkopf's 36 Morse signals map by length
   and rhythm (stress .19).
6. A universal law: Shepard (1987); his bias-free measure from confusions (1957, after Luce); the law tested on the
   Morse map (exponential R² .71 in log g, a Gaussian −.12); consequential regions derived (an Erlang prior gives
   exactly e^−d; a nearly known size gives a shoulder).
7. Similarity is not distance: the metric axioms and three failures (Rothkopf's diagonal 97% for E, 83% for P; 66 of
   69 for "North Korea is similar to Red China"; Jamaica, Cuba, Russia); the contrast model derived; Tversky's count
   of Morse asymmetries rerun on the open table (336, 182, 37 against his 336, 181, 38).
8. Knowledge as a network: Collins and Quillian (1969); its failures (typicality; levels reversed; Conrad 1972);
   spreading activation with a fan (Collins and Loftus 1975; Anderson 1974); semantic priming (Meyer and
   Schvaneveldt 1971) and the Semantic Priming Project (Hutchison et al. 2013: about 19 ms; first associates 26 and
   20 ms against 42 and 60 earlier).
9. Concepts as theories: the basic level (Rosch et al. 1976; Tanaka and Taylor 1991); category utility derived
   (Corter and Gluck 1992), with the basic level winning only while superordinates are loose; Rips's pizza (1989),
   Barsalou's goals (1983), Murphy and Medin (1985); Keil's raccoon (1989), Gelman and Markman's blackbird (1986),
   psychological essentialism.
10. Learning from a few examples: the number game and the size principle derived (Tenenbaum 1999); the model after
    one and four examples (powers of 4 at 28%; powers of 2; a range); Xu and Tenenbaum's feps (2007); Shepard's law
    as Bayesian inference (Tenenbaum and Griffiths 2001).
11. Meaning from company: Harris (1954), Firth (1957), the tezgüino example; PPMI and the SVD derived; Jane Austen's
    six novels (729,322 words) with neighbours, a map in which *unhappy* sits among the happy words, analogies (one
    right, one wrong); LSA on the TOEFL (64.4% against 64.5%); Caliskan et al.'s biases; grounding (Harnad 1990).
12. The Ledger. 13. In practice: 227 symptom sets for one DSM-5 diagnosis, and Fried and Nesse's 1,030 profiles;
    HiTOP; a card sort of twelve groceries by 40 simulated people, clustered; recommendation, search and ImageNet's
    person categories. 14. Frontier: RSA on Ekman's colours (hue angle .83, wavelength .77, cones .65);
    language models' similarity ratings (Marjieh et al. 2024: colour .89 from hex codes); one-shot learning (Lake et
    al. 2015), reweighted network features (Peterson et al. 2018), compositional learning (Lake and Baroni 2023);
    semantic maps (Huth et al. 2016) and open questions.

*Psyche:* `concepts`: the GCM and the prototype model; ALCOVE with attention learning fitted to the six problems and
a delta-rule network; classical and non-metric MDS; Shepard's measure, law and consequential regions; the contrast
model and the asymmetry count; category utility; spreading activation; the number game; PPMI word vectors and
analogies; RSA and hue angles; the polythetic count and a card sort. `rdata`: a data-only reader for R's XDR files.
`opendata`: catlearn, smacof and janeaustenr from CRAN, one member read from each tarball, checked by SHA-256.
*On you:* true or false at speed in the film; the interactive is the number game (three rounds, the reader's
judgements against the model's).
*Ledger:* typicality (`replicated`); the basic level (`replicated`); the prototype effect (`replicated`, with its
interpretation contested); the six-problem ordering (`replicated`, Type II's place depending on the task); Shepard's
law (`replicated`); asymmetric similarity (`replicated, smaller`); the hierarchical network (`failed`); semantic
priming (`replicated, smaller`).
*In practice:* diagnosis by polythetic criteria, card sorting for navigation, recommendation by similarity, search
by vectors, the categories in dataset labels.
*Frontier:* representational similarity analysis; what language models know about perception; one-shot and
compositional learning; where concepts are in the brain; grounding.
*Reading:* Rosch 1975; Medin & Schaffer 1978; Nosofsky 1986; Shepard 1987; Tversky 1977; Kruschke 1992; Murphy,
*The Big Book of Concepts*; Tenenbaum & Griffiths 2001; Landauer & Dumais 1997.

### Part 23 · Language (~55)
*Question:* how does a child who hears a finite number of sentences come to understand an infinite number?
*Story:* in 1959 a thirty-year-old linguist reviews B. F. Skinner's book on verbal behaviour and argues that no
theory of reinforcement can explain a sentence never heard before. The review helps start cognitive science. The
argument it began, how much is built in and how much is learned from statistics, has now run for seventy years, and
it now has numbers: reading times, a model's probabilities, two minutes of a made-up language, a network that says
*goed*, and two-thirds of a million grammar quizzes. Machines that learn language from text alone have joined it.
0. Hook: Skinner (1957) and Chomsky's review (1959); "Colorless green ideas sleep furiously" and its reverse; a
   syllable stream on you, with the question held until Chapter 6; the questions; objectives.
1. Levels and productivity: sounds, words, sentences, meaning and use, productive at each level; the wug test (Berko
   1958); Zipf's law on thirty novels (exponent 1.20, R² .994) and on Miller's typing monkey (1.20, a staircase), a
   warning about what a law shows.
2. The mental lexicon: frequency and length against reading time in the Natural Stories corpus (Futrell et al.
   2021; 369 to 327 ms across eighths of frequency); a spoken word's cohort as it arrives (Marslen-Wilson 1987;
   *trespass*: 1,547, 346, 54, 4, 2).
3. Recognizing a word: Reicher's paradigm (1969); the interactive activation model derived (McClelland and Rumelhart
   1981) with a fourteen-segment font, and run: K after WORK .534 against K alone .418, an effect smaller than
   people's, said so.
4. Sentences in real time: garden paths (Bever 1970); eye movements at the breaking word (Frazier and Rayner 1982,
   as a schematic); a trigram model's surprisal word by word, *fell* at 13 bits with and without *that was*: two
   words of context cannot see the syntax (Hale 2001 can).
5. The cost of a surprising word: surprisal derived as a change of belief (Levy 2008); a story word by word; the fit
   to 10,256 words (a Kneser-Ney trigram of the novels, perplexity 405): 324 to 361 ms across tenths, 1.18 ms per bit
   on the next word and none on the word itself, with length and frequency held fixed (Smith and Levy 2013).
6. Finding the words: Saffran, Aslin and Newport (1996); transitional probabilities derived (1 inside words, 1/3
   across); segmentation by dips, perfect after 20 words; golabu against labubi answered; Black and Bergmann's
   meta-analysis (2017).
7. How children learn a language: milestones; the poverty of the stimulus as a learnability claim, Gold's theorem
   (1967) and its answers (Horning 1969; Chater and Vitányi 2007); fast mapping (Carey and Bartlett 1978), Part
   22's size principle, and the input (Hart and Risley 1995, with its dispute).
8. Rules or associations? The U-shaped curve and Marcus et al.'s 4.2% (1992); a past-tense network (Rumelhart and
   McClelland 1986) run on Psyche's 65 irregulars and 125 regulars (.94, dip to .83, .92; over-regularization peaking
   at .12) and the vocabulary flood behind it; Pinker and Prince (1988); words and rules.
9. A critical period? Genie (Curtiss 1977) and late first languages (Mayberry, Lock and Kazmi 2002); Johnson and
   Newport (1989); Hakuta, Bialystok and Wiley (2003); Hartshorne, Tenenbaum and Pinker (2018): 669,498 people,
   ability near its peak until about 17.4.
10. Language in the brain: Broca (1861) and Wernicke (1874); the language network, localized in each person
    (Fedorenko, Behr and Kanwisher 2011); the N400 (Kutas and Hillyard 1980) and the P600 (Osterhout and Holcomb
    1992).
11. Language and thought: Whorf; Berlin and Kay (1969); Russian blues (Winawer et al. 2007) and their contested
    record; Pirahã numbers (Frank et al. 2008); the bilingual advantage and its meta-analysis (Lehtonen et al.
    2018).
12. The Ledger. 13. In practice: Flesch's formula computed (about 75 for two stories and a chapter of *The Maltese
    Falcon*) and why surprisal is better; the National Reading Panel (2000) and phonics; intensive aphasia therapy
    (Breitenstein et al. 2017); second languages. 14. Frontier: language models' input against a child's
    (BLiMP, Warstadt et al. 2020; BabyLM); one child's 61 hours (Vong et al. 2024); larger models' surprisal fitting
    readers worse (Oh and Schuler 2023).

*Psyche:* `language`: Zipf's law and the typing monkey; cohorts and Flesch; the interactive activation model with a
fourteen-segment font; Saffran streams, transitional probabilities and segmentation; a past-tense learner whose
vocabulary grows; an interpolated Kneser-Ney trigram and its surprisal; the reading-time regression with spillover.
`opendata`: Natural Stories' per-word reading times, pinned to a commit and checked by SHA-256.
*On you:* a syllable stream in the film; the interactive is a made-up language (watch the stream, then pick its
words out of eight pairs; you against chance and Psyche).
*Ledger:* word superiority (`replicated`); infant statistical segmentation (`replicated, smaller`); surprisal and
reading time (`replicated`); a sharp critical period (`contested`); linguistic relativity for colour
discrimination (`contested`); a bilingual advantage in executive control (`failed`).
*In practice:* readability, reading instruction (Part 54), aphasia therapy, second-language teaching.
*Frontier:* what language models' success shows about learnability; child-scale input; whether surprisal from
larger models fits reading times worse.
*Reading:* Chomsky 1959; Saffran, Aslin & Newport 1996; McClelland & Rumelhart 1981; Levy 2008; Pinker, *The
Language Instinct* and *Words and Rules*; Rumelhart & McClelland 1986; Hartshorne et al. 2018; Traxler,
*Introduction to Psycholinguistics*; Christiansen & Chater, *The Language Game*.

### Part 24 · Reasoning and Problem Solving (~55)
*Question:* are people logical, and if not, what are they instead?
*Story:* four cards, one rule, and nine in ten university students choose wrongly. Change the cards to drinks and
ages and nearly everyone is right. Reasoning is not the application of logic to content; content is the engine.
Meanwhile Newell and Simon write a program that solves problems as people do, by searching, and the expert turns
out to be someone who no longer needs to.
0. Hook and On you: Wason's selection task (1966, 1968), abstract, then as a drinking-age rule (Griggs and Cox
   1982: about three in four right); the questions; objectives.
1. Deduction: the 64 syllogisms and nine answers; validity by brute force over the 256 models of three sets (27
   valid with existential presupposition, 22 without); 139 people's answers to all 64 (Ragni 2016, open data via
   CCOBRA: 41% right, "no valid conclusion" 28% of answers; EA1 right 4%); belief bias (Evans, Barston and Pollard
   1983: 89, 56, 71, 10).
2. Rules, models and shortcuts: mental models and the search for counterexamples (Johnson-Laird 1983); atmosphere,
   matching, the probability heuristics; all four scored on the data (atmosphere best where a conclusion follows,
   only logic where none does); Khemlani and Johnson-Laird's meta-analysis (2012).
3. Why content helps: pragmatic schemas (Cheng and Holyoak 1985), cheater detection (Cosmides 1989); optimal data
   selection derived (Oaksford and Chater 1994) and computed (p .61, q .15, not-q .05, not-p .01 bits) against their
   Table 2 (13 studies, 845 people: 89, 62, 25, 16%).
4. Problem solving as search: Newell, Shaw and Simon; states, operators, means-ends analysis; the Tower of Hanoi's
   27 states drawn as a Sierpinski triangle; the 7-move path against a hill-climber (median 14 of 101 runs).
5. Production systems: three rules for the tower; ACT-R in outline; a goal stack's pauses before moves 1, 9, 5 and
   13 (Anderson and Douglass 2001); thinking aloud as data (Ericsson and Simon 1980, 1993).
6. Insight: Duncker's candle (1945), functional fixedness (Adamson 1952); the nine dots by brute force (no drawing
   inside the square, 16 outside); Weisberg and Alba's hint (1981); warmth ratings (Metcalfe and Wiebe 1987) and
   progress monitoring (MacGregor, Ormerod and Chronicle 2001).
7. Expertise: de Groot (1946); Chase and Simon (1973), game and random positions, Gobet and Simon (1996); chunks;
   deliberate practice (Ericsson et al. 1993), the 10,000-hour story, Macnamara et al. (2014: 26, 21, 18, 4, <1%) and
   the 2019 replication.
8. Analogy: the radiation problem and the fortress (Gick and Holyoak 1980: about 10, 30, 75%); structure mapping
   (Gentner 1983) computed: army to rays, fortress to tumour, general to doctor.
9. Mental imagery: Shepard and Metzler (1971); Ganis and Kievit's open data (2015: 54 people; 1.56 to 3.34 s from 0
   to 150 degrees; 53 of 54 slopes rising; median 93 degrees a second) and a constant-rate model that fits the trend
   but not the bend; Kosslyn against Pylyshyn; aphantasia (Zeman et al. 2015).
10. Reasoning about causes: delta P (Part 16) to causal power derived (Cheng 1997); seeing against doing (Waldmann
    and Hagmayer 2005; *Statistics, Built* Part 36).
11. Everyday predictions and bounded rationality: the posterior median derived (Griffiths and Tenenbaum 2006);
    power-law, Erlang and normal priors give multiplicative, additive and regressive rules; Mozer, Pashler and
    Homaei's critique (2008); Simon's satisficing (1955), and the argument Part 26 continues.
12. The Ledger. 13. In practice: interview puzzles against validated selection methods (Schmidt and Hunter 1998;
    Sackett et al. 2022); worked examples (Sweller and Cooper 1985); usability testing as protocol analysis,
    Nielsen and Landauer's curve computed (five users, 84%). 14. Frontier: ARC (Chollet 2019; H-ARC, LeGris et al.
    2024: 64%), program induction (DreamCoder, Ellis et al. 2021), large reasoning models; analogy in language
    models (Webb, Holyoak and Lu 2023) and counterfactual critiques (Lewis and Mitchell 2024).

*Psyche:* `reason`: syllogisms over set models and four accounts scored; optimal data selection; the Tower of
Hanoi's graph, layout, shortest path, goal stack and hill-climber; the nine dots by exhaustive search; structure
mapping; rotation fits and a rotation model; delta P and causal power; posterior-median predictions.
`opendata`: Ganis and Kievit's workbooks (figshare, CC BY 4.0) and Ragni's syllogisms (CCOBRA, MIT), both checked
by SHA-256.
*On you:* the selection task in the film; the interactive is mental rotation (same or mirror; your slope and rate
against the 54 people).
*Ledger:* the selection task's content effect (`replicated`); belief bias (`replicated`); mental rotation
(`replicated`); chess chunking (`replicated`); the 10,000-hour rule (`story and record`); optimal everyday
predictions (`replicated`, individual-level interpretation contested).
*In practice:* interview puzzles and what they do not measure, training design, protocol analysis in UX.
*Frontier:* program induction as a model of thinking; whether language models reason by analogy (Part 60);
cognitive architectures against end-to-end learning.
*Reading:* Wason 1966; Newell & Simon 1972; Chase & Simon 1973; Shepard & Metzler 1971; Gick & Holyoak 1980;
Johnson-Laird 1983 and *How We Reason*; Oaksford & Chater 1994; Anderson 1993; Holyoak & Morrison (eds.), *The Oxford
Handbook of Thinking and Reasoning*.

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
   - The browser task kit for the Battery (`course/site/widgets/00_tasks.js`: keys and taps, timing, the
     timed-trial loop; data kept in the page's memory only), since every part's interactive needs it, and a
     scripted participant for `tools/check_course.py`.
   - `tests/psychology/`: the Pool's planted truths are recoverable; the Ledger's schema; a silent smoke render.
1. **Pilots: Part 1, then Part 2** (The Experiment). The first draft of this plan named Part 12 as the second
   pilot; it is Part 2 instead, for two reasons found while building Part 1: the course tools and the site count a
   series' parts from 1 without gaps, so a part built out of order would not appear; and Part 1 ends on Part 2's
   hook. Part 2 still exercises what a typical part needs (an experiment on the viewer, a model fitted to
   historical data, designs run on the Pool, Ledger rows, an industry payoff), and Part 12 becomes the checkpoint
   for the methods standard when Act III is reached. Delivered with previews and contact sheets. **Reviewed
   with the user on 2026-11-13 and accepted as they stand; the standard of §1 is locked** and the parts now follow
   in order.
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
| 0 | built: `explainer/psychology/` (Psyche's `chronometry`, the Pool, the Battery, the Ledger, the Archive, cards, maps and the first instruments), `tests/psychology/`, the course kit and site entries. The Chinese guide (`PSYCHOLOGY_ZH_GUIDE.md`) and text table are in place, and the Ledger gate (`tools/check_ledger.py`, run by `tools/make.py`). The browser task kit (`course/site/widgets/00_tasks.js`: keys and taps, timing, the timed-trial loop; nothing stored or sent) carries the interactives of Parts 1 and 2, and `tools/check_widgets.js` plays a scripted participant against it. Phase 0 is complete | |
| 1 | built, English and Chinese: 14 chapters, hook and outro; course entry, lab and interactive checked; narration table and on-screen text translated and dry-run. Open checks in its README | 46 min |
| 2 | built, English and Chinese, the second pilot: 14 chapters, hook and outro; the laboratory (`lab.py`), the cue-reading model (`psyche/cueing.py`), five Ledger rows; course entry, lab and interactive checked; narration table and on-screen text translated and dry-run. Open checks in its README | 56 min |
| 3 | built, English and Chinese: 14 chapters, hook and outro; the measurement library (`measure.py`), the Pool's traits, methods and conflict task, three Ledger rows; course entry, lab and interactive (the Forer reading) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 56 min |
| 4 | built, English and Chinese: 14 chapters, hook and outro; the false-positive lab (`evidence.py`), six Ledger rows (the plan's twenty were cut to what could be sourced and dated), nine Archive datasets; course entry, lab and interactive (the forking paths) checked; narration table and on-screen text translated and dry-run. Act I is complete. Open checks in its README | 48 min |
| 5 | built, English and Chinese: 14 chapters, hook and outro; Psyche's neuron (`psyche/neuron.py`, eleven tests, the 1952 conduction speed recomputed), one Ledger row, five Archive datasets; course entry for Act II, lab and interactive (reading a spike train) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 58 min |
| 6 | built, English and Chinese: 14 chapters, hook and outro; Psyche's circuits (`psyche/circuits.py`, eleven tests), three Ledger rows, nine Archive datasets; course entry, lab and interactive (the Hermann grid with straight and wavy streets) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 62 min |
| 7 | built, English and Chinese: 14 chapters, hook and outro; Psyche's brain (`psyche/brain.py`, ten tests), four Ledger rows, seventeen Archive datasets; course entry, lab and interactive (the reader's own blind spot, measured with outward and inward sweeps) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 63 min |
| 8 | built, English and Chinese: 14 chapters, hook and outro; Psyche's imaging (`psyche/imaging.py`, thirteen tests), three Ledger rows, seventeen Archive datasets; course entry, lab and interactive (which reported correlation is impossible, given the two reliabilities) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 60 min |
| 9 | built, English and Chinese: 14 chapters, hook and outro; Psyche's genes (`psyche/genes.py`, sixteen tests), three Ledger rows, twenty-three Archive datasets; course entry, lab and interactive (genes or the shared home, read from two twin correlations) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 60 min |
| 10 | built, English and Chinese: 14 chapters, hook and outro; Psyche's body (`psyche/body.py`, fourteen tests), four Ledger rows, sixteen Archive datasets; course entry, lab and interactive (a vigilance task beside the reader's own rating of alertness) checked; narration table and on-screen text translated and dry-run. Act II is complete. Open checks in its README | 59 min |
| 11 | built, English and Chinese: 14 chapters, hook and outro; Psyche's psychophysics (`psyche/psychophysics.py`, twenty-four tests) and Battery task 2, two Ledger rows, fifteen Archive datasets; course entry, lab and interactive (the reader's own threshold, by staircase, with a fitted curve) checked; narration table and on-screen text translated and dry-run. Act III begins. Open checks in its README | 48 min |
| 12 | built, English and Chinese: 14 chapters, hook and outro; Psyche's sdt (`psyche/sdt.py`, eleven tests), three Ledger rows, thirteen Archive datasets; course entry, lab and interactive (a recognition test with confidence that draws the reader's ROC) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 44 min |
| 13 | built, English and Chinese: 15 chapters, hook and outro; Psyche's vision (`psyche/vision.py`, twelve tests) and the colour tables, five Ledger rows (one deferred from Part 5), eleven Archive datasets; course entry, lab and interactive (the reader's contrast sensitivity at four stripe widths) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 52 min |
| 14 | built, English and Chinese: 14 chapters, hook and outro; Psyche's inference (`psyche/infer.py`, six tests, with a one-layer convolutional network in numpy), four Ledger rows, fifteen Archive datasets; course entry, lab and interactive (the reader's own Müller-Lyer illusion, by two staircases) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 64 min |
| 15 | built, English and Chinese: 15 chapters, hook and outro, with demonstrations played in the film; Psyche's hearing (`psyche/hearing.py`, ten tests) and `VoiceoverScene.sound`, six Ledger rows (one deferred from Part 7), fourteen Archive datasets; course entry, lab and interactive (which way a missing fundamental moves, in Web Audio) checked; narration table and on-screen text translated and dry-run. Act III is complete. Open checks in its README | 55 min |
| 16 | built, English and Chinese: 15 chapters, hook and outro; Psyche's conditioning (`psyche/conditioning.py`, twelve tests), six Ledger rows (one deferred from Part 10), twenty-three Archive datasets; course entry, lab and interactive (the gardener's game: predictions that reveal the contingency learned) checked; narration table and on-screen text translated and dry-run. Act IV begins. Open checks in its README | 54 min |
| 17 | built, English and Chinese: 14 chapters, hook and outro; Psyche's reinforcement learning (`psyche/rl.py`, seven tests) with the part's own simulations of Steinberg's and Frank's designs and a bandit test, four Ledger rows, seventeen Archive datasets; course entry, lab and interactive (two slot machines: eighty pulls, the reader's α and β fitted on the page) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 42 min |
| 18 | built, English and Chinese: 15 chapters, hook and outro; Psyche's attention (`psyche/attention.py`, seventeen tests) with Battery tasks 3 and 4 (Stroop, visual search), six Ledger rows (one deferred from Part 16), twenty-five Archive datasets; course entry, lab and interactive (feature and conjunction search, the reader's slopes measured on the page) checked; narration table and on-screen text translated and dry-run. Act V begins. Open checks in its README | 51 min |
| 19 | built, English and Chinese: 13 chapters, hook and outro, with digit span played in the film; Psyche's working memory (`psyche/wm.py`, sixteen tests) with Battery task 5 (change detection) and the series' first open trial-level data (`opendata.py`: Bays, Catalao and Husain 2009, fetched and checked by SHA-256, four process models fitted to every observer), six Ledger rows, twenty-three Archive datasets; course entry, lab and interactive (change detection: the reader's K at four set sizes) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 52 min |
| 20 | built, English and Chinese: 15 chapters, hook and outro, with free recall played in the film; Psyche's memory (`psyche/memory.py`, fourteen tests) with the context model fitted by maximum likelihood to open free-recall data (PEERS) and checked on held-out lists, and Murre's divers from his open data (`opendata.py`), six Ledger rows, seven Archive datasets; course entry, lab and interactive (free recall: the reader's serial-position and lag-CRP curves) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 62 min |
| 21 | built, English and Chinese: 14 chapters, hook and outro, with the DRM illusion played in the film; Psyche's memory module gains forgetting and inventing (`psyche/memory.py`, thirteen more tests in `test_forget.py`): four forgetting laws, a two-store consolidation model, the penguin in a semantic network, the spacing and bifurcation models, category adjustment, global matching, line-ups by signal detection and half-life regression; the verbal-overshadowing Registered Replication Report from its open data (`opendata.py`), eight Ledger rows, thirteen Archive datasets; course entry, lab and interactive (the DRM lists with remember, know or new) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 66 min |
| 22 | built, English and Chinese: 14 chapters, hook and outro, with typicality at speed played in the film; Psyche's concepts module (`psyche/concepts.py`, seventeen tests): the GCM, the prototype model and ALCOVE fitted to the six problems, classical and non-metric scaling, Shepard's law and consequential regions, the contrast model, category utility, the number game, word vectors and RSA; three CRAN packages' data read without R (`rdata.py`, `opendata.py`), eight Ledger rows, eight Archive datasets; course entry, lab and interactive (the number game) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 59 min |
| 23 | built, English and Chinese: 14 chapters, hook and outro, with a syllable stream played in the film; Psyche's language module (`psyche/language.py`, twelve tests): Zipf fits and a typing monkey, cohorts, the interactive activation model with a fourteen-segment font, transitional probabilities and segmentation, a past-tense learner, a Kneser-Ney trigram and its surprisal fitted to reading times, Flesch's formula; the Natural Stories reading times (`opendata.py`, pinned to a commit), six Ledger rows, five Archive datasets; course entry, lab and interactive (a made-up language) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 42 min |
| 24 | built, English and Chinese: 14 chapters, hook and outro, with the four-card selection task played in the film; Psyche's reasoning module (`psyche/reason.py`, eight tests): syllogisms by brute force over set models with four accounts scored, optimal data selection, the Tower of Hanoi's state graph with a goal-stack production system and a hill-climber, the nine dots by exhaustive search, structure mapping, rotation fits, causal power and posterior-median predictions; Ragni's syllogism answers and Ganis and Kievit's mental rotation data (`opendata.py`, pinned and checked), six Ledger rows, five Archive datasets; course entry, lab and interactive (mental rotation) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 41 min |
| 25 | built, English and Chinese: 14 chapters, hook and outro, with moving dots played in the film; Psyche's decision module (`psyche/decide.py`, eleven tests): Wald's sequential test with its operating characteristic and average sample number, the diffusion model's closed forms and Navarro and Fuss's first-passage densities, fits by maximum likelihood and EZ, the linear ballistic accumulator, Hick's race, the stop-signal race with the integration estimate, balance-of-evidence confidence, collapsing bounds and the attentional drift diffusion model; Wagenmakers et al.'s speed-accuracy lexical decisions and Ratcliff and Rouder's brightness judgements (`opendata.py`, from the CRAN package rtdists, pinned and checked), five Ledger rows, two Archive datasets; course entry, lab and interactive (moving dots in careful and fast blocks) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 40 min |
| 26 | built, English and Chinese: 15 chapters, hook and outro, with the disease problem and the bat and the ball played in the film; Psyche's choice module (`psyche/choice.py`, thirteen tests) with Battery task 9 (risky and delayed choices): expected value and utility, the St Petersburg game, the probability triangle, cumulative prospect theory with certainty equivalents and the fourfold pattern, four choice models fitted and cross-validated, Bayes's rule in natural frequencies, take-the-best against regression, the hot-hand bias by exact enumeration, discounting and its reversals, choices from small samples, decision by sampling; choices13k (`opendata.py`, pinned and checked), six Ledger rows, one Archive dataset; course entry, lab and interactive (the disease problem and your own fourfold pattern) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 58 min |
| 27 | built, English and Chinese: 15 chapters, hook and outro, with a masked digit and binocular rivalry played in the film; Psyche's workspace module (`psyche/workspace.py`, seven tests): masking as one signal read twice with the criterion problem computed, a rivalry oscillator with gamma-like dominance durations, a two-stage ignition network, effective information and Φ in Tononi's 2004 form for small Boolean networks, Schurger's accumulator and its back-averaged ramp, Lempel–Ziv complexity and the perturbational complexity index; four Ledger rows; course entry, lab and interactive (masking with visibility reports) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 45 min |
| 28 | built, English and Chinese: 15 chapters, hook and outro, with a discount titration played in the film; Psyche's drive module (`psyche/drive.py`, nine tests): a thermostat with proportional and integral control, energy balance with a settling point and a defended set point, Part 17's learner given a stimulating current, an arousal sketch, the salt cue's cached and incentive values, self-perception as Bayes, Atkinson's tendency, the expected value of control, expected remaining waits, a confounded delay study, random effects and the precision-effect test, discount titration; the ego-depletion Registered Replication Report's table fetched from OSF and recomputed; six Ledger rows; course entry, lab and interactive (a discount titration) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 56 min |
| 29 | built, English and Chinese: 15 chapters, hook and outro, with the face-pair map and a forecast checked in the outro; Psyche's emotion module (`psyche/emotion.py`, twelve tests with the reader's ALTREP vectors): classical scaling, scale fitting and Procrustes, schematic faces and a same-or-different observer, arousal attribution, an appraisal model, LeDoux's two roads, adaptation and a forecaster, a hidden income plateau, the Lorenz system; Abelson and Sermat's 1962 faces (smacof) and Coles, Larsen and Lench's facial-feedback table (psymetadata) fetched from CRAN and recomputed; six Ledger rows; course entry, lab and interactive (the face-pair map) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 49 min |
| 30 | built, English and Chinese: 14 chapters, hook and outro, with six infant results predicted on you; Psyche's develop module (`psyche/develop.py`, seven tests): habituation with the laboratory criterion, a Dirichlet-multinomial learner's surprisal and a Goldilocks observer, number by ratio with Weber fractions by age, the box-of-balls probabilities, a dynamic neural field that makes and outgrows the A-not-B error, random-effects meta-regression; ManyBabies 1's lab-level table (psymetadata) fetched from CRAN and recomputed, with age, method and language; eight Ledger rows and four earlier deferrals settled; course entry, lab and interactive (predict the infant) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 42 min |
| 31 | built, English and Chinese: 15 chapters, hook and outro, with three graphs sorted by clock on you; Psyche's lifespan module (`psyche/lifespan.py`, six tests): the APC identity and Lexis tables, a population with a true ageing curve and cohort drift under cross-sectional, longitudinal (practice and drop-out) and cohort-sequential designs, a growth-curve mixed model fitted by EM with BLUPs, ACE sibling correlations, a threshold model of cognitive reserve, attributable fractions, the sampling of talk by the hour; nine Ledger rows and Part 10's chronotype deferral settled; course entry, lab and interactive (age, period or cohort?) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 54 min |
| 32 | built, English and Chinese: 15 chapters, hook and outro, with three matrix items on you; Psyche's traits module (`psyche/traits.py`, seven tests): tetrad differences and one-factor ML fits, a common-cause, a Thomson sampling and a mutualism world with a training experiment, ratio and deviation IQs, the SEM and Thorndike's correction, rule-built matrix items with a capacity-limited solver, overlap and a measurement-invariance demonstration, cutoffs, Kelley's estimate, Brogden's gain and the selection-rate ratio; Spearman's 1904 table in the Archive and Holzinger and Swineford's 301 children fetched from lavaan and checked by SHA-256; eight Ledger rows, with Part 31's Flynn deferrals and Part 9's two deferred rows settled; course entry, lab and interactive (a matrix test built from rules) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 45 min |
| 33 | built, English and Chinese: 15 chapters, hook and outro, with four numbers predicted on you; Psyche's personality module (`psyche/personality.py`, six tests): reverse-keyed scoring, parallel analysis, a world of people and situations with aggregation and variance components, the arcsine law for types, Mahalanobis D by number of traits, the binomial effect-size display, simulated likes, faking in selection; the SAPA project's 25 IPIP items for 2,800 people and the EPI/BFI sample fetched from psychTools and checked by SHA-256; seven Ledger rows; course entry, lab and interactive (the 25-item inventory against the SAPA norms) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 40 min |
| 34 | built, English and Chinese: 14 chapters, hook and outro, with four numbers predicted on you; Psyche's social module (`psyche/social.py`, nine tests, shared with Part 35): Granovetter's thresholds, DeGroot and bounded-confidence opinions, simple and complex contagion on rewired rings, the diversity identity and rounds of influence, a cumulative-advantage market, bystanders, drive and information sampling; ten Ledger rows, with Milgram not directly tested and two stories (the prison study, the 38 witnesses) set against their records; course entry, lab and interactive (Asch's lines, alone and after five scripted answers) checked; narration table and on-screen text translated and dry-run. The MusicLab data sit behind a browser challenge, so the market is simulated. Open checks in its README | 47 min |
| 35 | built, English and Chinese: 14 chapters, hook and outro, with three moving shapes and four numbers on you; Psyche's social module (Kelley's cube, the Dunning-Kruger plot from noise, the inverse planner): attribution as an analysis of variance, a rational observer of forced essays, the winner's curse, goal inference in a gridworld; eight Ledger rows, with induced-compliance dissonance, elderly priming and power posing failed and Dunning-Kruger's explanation contested; course entry, lab and interactive (goal inference against the inverse planner) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 36 min |
| 36 | built, English and Chinese: 14 chapters, hook and outro, with a minimal-group choice and four numbers on you; Psyche's social module (Tajfel's matrices, an IAT as diffusion decisions with trait and state, the list experiment, a promotion ladder, an illusory-correlation model): the IAT's reliability and what it does to prediction, an audit's power, a filtered stereotype-threat literature; eight Ledger rows, with the IAT as a guide to individuals failed, stereotype threat contested, deep canvassing replicated after a retracted first report and Robbers Cave set against Perry's archive; course entry, lab and interactive (a minimal group: share points in Tajfel-style matrices) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 34 min |
| 37 | built, English and Chinese: 14 chapters, hook and outro, with an ultimatum offer and four numbers on you; Psyche's social module gains Fehr and Schmidt's utility, the proposer's problem, a public-goods game with punishment, a noisy prisoner's dilemma tournament, a marriage market by deferred acceptance and a divorce classifier scored in and out of sample; seven Ledger rows, with stated preferences predicting desire failed and 90% divorce prediction contested; course entry, lab and interactive (the ultimatum game as the responder) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 28 min |
| 38 | built, English and Chinese: 14 chapters, hook and outro, with three trolley cases and four numbers on you; Psyche's new culture module (conformist and prestige-biased transmission, Henrich's model of population size and skill, the reference-group effect, an additive model of trolley judgments across countries): WEIRD sampling, the Müller-Lyer illusion, selves and their measures, rice, mobility and kinship, cultural evolution with overimitation, moral psychology, 42 and 45 countries, ManyBabies 4 and Many Labs 2; nine Ledger rows, with the infant helper preference failed and five contested, and Part 2's and Part 30's deferred rows entered; course entry, lab and interactive (three trolley cases and three variants) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 33 min |
| 39 | built, English and Chinese: 14 chapters, hook and outro, opening with the care card (a new shared `care_card`), with a positive screen and four numbers on you; Psyche's new clinic module (Cohen's kappa, two noisy clinicians, a symptom network with hysteresis and episodes, diagnoses from a general factor and domains, natural frequencies, a formula against a wandering clinician): Rosenhan and the archive, definitions, kappa and the field trials, 227 combinations, taxometrics, the p factor, prevalence and the treatment gap, Meehl, idioms of distress; five Ledger rows, with laboratory diagnosis failed and Rosenhan and the p factor contested, and Part 22's deferred row entered; course entry, lab and interactive (six positive screens) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 29 min |
| 40 | built, English and Chinese: 15 chapters, hook and outro, opening with the care card and following safe messaging on suicide (help lines on screen), with a dot-probe trial and four numbers on you; Psyche's clinic module gains Mowrer's avoidance loop, context-bound extinction and extinction across contexts, the triadic design as a belief about control, the behavioural-activation trap, and Rutledge and colleagues' model of momentary mood with its fit: helplessness and its reversal, exposure and renewal, the anxiety disorders, panic and compulsion as habit, attention bias, depression's cognitive accounts, anhedonia, the serotonin story, Kirsch and Cipriani, life events and 5-HTTLPR, lithium, and suicide's base rate in natural frequencies; eight Ledger rows, with four failed (attention training, serotonin deficit, the gene-by-stress interaction, suicide prediction); course entry, lab and interactive (an unscored dot-probe) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 29 min |
| 41 | built, English and Chinese: 15 chapters, hook and outro, opening with the care card, with shaded bumps and dents and four numbers on you; Psyche's clinic module gains the hollow mask on a Gaussian observer, the best strength of a prior, conditioned hallucinations, aberrant salience, Redish's non-compensable drug signal and hyperbolic discounting: schizophrenia and its course, chlorpromazine, D2 binding and dopamine version III, salience and the precision puzzle, genes, environments and the schizophrenogenic mother, addiction's mechanisms, Redish's model and the blocking test, Rat Park, the Vietnam veterans and contingency management, autism's histories, the vaccine fraud, weak priors, rising diagnoses and facilitated communication, ADHD, relative age and the MTA trial, and three transdiagnostic dials; eight Ledger rows (one retracted, one failed, two contested), and the deferred addiction declarations of Parts 10, 16 and 17 resolved; course entry, lab and interactive (sixteen shaded discs) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 34 min |
| 42 | built, English and Chinese: 14 chapters, hook and outro, opening with the care card, with the two-graphs problem and four numbers on you; Psyche's clinic module gains a therapy-trial simulator (regression to the mean, four arms), effects against each control, researcher allegiance, a publication filter, DerSimonian and Laird's random-effects meta-analysis, Jacobson and Truax's reliable change and cut-off, and the dose-response curve: Eysenck's challenge, Smith and Glass, the dodo bird and the alliance, the therapies and DBT, therapy against medication and relapse, Turner's two piles of trials and "Was Eysenck right after all?", clinical significance for four clients, treatments that harm, lobotomy and ECT, and the treatment gap; seven Ledger rows (two failed, debriefing and Scared Straight), and the deferred declarations of Parts 2, 6 and 10 resolved; course entry, lab and interactive (six study designs) checked; narration table and on-screen text translated and dry-run. Open checks in its README | 29 min |
