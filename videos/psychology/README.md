# Psychology, Built (心理学，从零搭建)

**Status (2026-11-15): the plan is accepted, the shared code is in place, and Parts 1 to 44 are built in English
and Chinese.** Act I (Parts 1 to 4) is the method; Act II (Parts 5 to 10) is the biology, from *The Neuron* to
*Chemistry and Clocks*; Act III (Parts 11 to 15) is the senses, from *The Threshold* to *The Other Senses*; Act IV
(Parts 16 and 17) is learning, *Conditioning* and *Reward and Prediction*; and Act V, thinking, is complete:
*Attention*, *Working Memory*, *Memory I: Storing and Finding*, *Memory II: Forgetting and Inventing*, *Concepts
and Categories*, *Language*, *Reasoning and Problem Solving*, *Deciding in Time*, *Judgment and Choice* and *Consciousness* (Parts 18 to 27); and Act VI, feeling and wanting, is complete: *Motivation* and *Emotion* (Parts 28 and 29); and Act VII, growing, is complete: *The Infant Mind* and *The Lifespan* (Parts 30 and 31); and Act VIII, how people differ, is complete: *Intelligence* and *Personality* (Parts 32 and 33); and Act IX, other people, is complete: *Social Influence*, *Social Cognition*, *Us and Them*, *Bonds and Bargains* and *Culture and Morals* (Parts 34 to 38); and Act X, when minds suffer, is complete: *What Is a Disorder?*, *Fear and Sadness*, *Psychosis, Addiction and Development* and *Does Therapy Work?* (Parts 39 to 42); and the degree ends with its capstone, *The Replication* (Part 43). Act XI, the graduate toolkit, has begun with *Latent Variables* (Part 44). This file is the plan;
the standard every part meets, the devices and all sixty-two parts chapter by chapter are in
[`SYLLABUS.md`](SYLLABUS.md), with the progress table in its §9.

This is a sixty-two-part course in psychology on video: **an undergraduate degree, the graduate methods sequence,
the practice industry runs on, and a research tier**. It covers the brain and the senses, learning, memory, language,
thought and decision, emotion, development, intelligence and personality, social life, and mental disorder and its
treatment. Then it covers the quantitative toolkit of a PhD (latent variables, item response theory, multilevel
data, computational modelling, neuroimaging analysis, meta-analysis), the places psychology is a job (human factors,
UX, hiring, education, behaviour change, the courtroom, the clinic) and the research frontier. The videos will be
`psych1` … `psych62`, in `videos/psychology/psychN/`.

Each part is a **30–60 minute lecture** (most will land at 45–55) in the manner of 3Blue1Brown, and it is technical
on purpose. Psychology is usually filmed as a string of anecdotes. Here every central idea is a model that is
derived on screen, built in code, run, and compared with human data: a neuron from Hodgkin and Huxley's equations,
a threshold from signal detection theory, a habit from a prediction error, a reaction-time distribution from a
random walk, a forgetting curve from a memory search, an IQ score from a factor model. Every part is also one
story, and every part runs at least one experiment on the viewer.

## The story: Kant's wager

In 1786 Immanuel Kant wrote that psychology could never be a proper natural science. His reasons were good ones.
Mathematics, he said, cannot be applied to the phenomena of the inner sense; the mind cannot be taken apart and
recombined at will like a chemical; and the act of observing a mental state changes the state observed.

On the morning of 22 October 1850, lying in bed in Leipzig, Gustav Fechner saw how to take the wager. If you cannot
measure a sensation directly, measure the smallest change in the world that a person can notice, and count
sensation in those steps. Ten years later he published a book of measurements. The series is the story of that
reply, 175 years long, and it puts three questions to every topic:

1. **What happens?** The phenomenon, measured, and first measured on you: your threshold, your Stroop cost, your
   serial-position curve, your answer to Tversky and Kahneman's disease problem.
2. **What would produce it?** A mechanism, written as mathematics and built as running code. A model earns its place
   by reproducing the data, including the errors, the illusions and the shape of the reaction-time distribution.
3. **How do we know?** Kant's third objection never went away: the investigator is a mind studying minds, and the
   easiest person to fool. So every finding the series presents is entered in a ledger with its design, its size
   and what happened when someone ran it again.

The series tells three stories at once.

* **Building a mind.** The order of the parts is the order of construction: how to ask a mind a question, then the
  neuron, the brain, the senses, learning, memory, language, thought, choice, feeling, growth, the ways people
  differ, other people, and what happens when minds suffer and what helps. Then the tools, the work and the frontier.
* **The history of the field, 1850 to now.** Fechner, Helmholtz and Wundt's laboratory; James and Ebbinghaus; Pavlov
  and the behaviourists; the cognitive revolution of 1956; the brain scanner; the replication crisis of 2011 and
  the reforms that followed. Each part opens in its era, and the dead ends are told too.
* **A science learning to check itself.** It starts with a horse. In 1904 Clever Hans appeared to do arithmetic, and
  a commission of experts found no trick; Oskar Pfungst then showed (in a book of 1907) that the horse was reading
  its questioners.
  The methods invented because of Hans, and their failures a century later, run through the whole series.

## The devices that hold it together

1. **Psyche** (`explainer/psychology/psyche/`). *Psyche* is Greek for breath, for the soul, and for a butterfly.
   It is the model subject the series builds: a small, tested Python library that gains one faculty in each part,
   from a psychophysical observer and a Hodgkin–Huxley neuron to a memory search, a diffusion decision maker, a
   reinforcement learner, a Bayesian mind-reader and a network of symptoms. Later parts reuse earlier modules on
   screen: the signal detection observer of Part 12 judges a police line-up in Part 56. Each module is checked
   against an independent reference (an analytic solution, a published parameter set reproducing its published
   curve, SciPy, or *Statistics, Built*'s statkit).
2. **The Homunculus** (`homunculus_map`). The oldest bad explanation in psychology is the little person inside the
   head who does the seeing and deciding. The series map is that little person. Each part replaces one of its
   powers with a mechanism that runs, and the figure is redrawn with that part mechanical. What is still drawn as a
   person at the end is the list of open problems.
3. **The Pool** (`explainer.psychology.pool`). A seeded, simulated participant pool: a hundred thousand Psyches
   whose parameters differ (thresholds, learning rates, memory capacity, drift rates, traits), born into families
   and twin pairs, growing older, living in groups. In a real study the truth is hidden. In the Pool it is known,
   so a method can be graded: whether a twin design recovers the heritability that was built in, whether an
   adaptive test finds the ability, how often a literature of small studies gets the sign right. Always labelled
   `simulated`.
4. **The Battery.** Twelve classic tasks and one questionnaire, fixed for the whole series (reaction time, a 2AFC
   threshold, Stroop, visual search, change detection, free recall, moving dots, a bandit, risky choices, mental
   rotation, reading, matrix reasoning, and a public-domain personality inventory). Each has three columns: the
   published human benchmark, Psyche's result, and **yours**. In the films the task runs on the viewer with a
   pause; on the course site each part's interactive is the experiment itself, run in the browser, with the data
   never leaving it. In the last part Psyche sits the whole Battery, and the scorecard shows what the built mind
   can and cannot yet do.
5. **The Replication Ledger** (`explainer.psychology.ledger`). The series' scoreboard, one row for every classic
   finding the series presents: the original claim, year, sample and effect size; then what the record shows
   (`replicated`, `replicated, smaller`, `contested`, `failed`, `not directly tested`, `retracted`), with the
   citation. It includes the findings that grew (the Stroop effect, anchoring, the testing effect) and the ones
   that shrank or fell (ego depletion, power posing, the facial feedback effect as first reported), and it
   includes the stories that textbooks told wrongly (Kitty Genovese's thirty-eight witnesses, Little Albert, the
   Stanford prison). It plays the role of *Statistics, Built*'s Coverage Board and *Philosophy, Built*'s Wall.
6. **The Archive** (`explainer.psychology.archive`). Real data, transcribed from the original publication or taken
   from open repositories, with the source on screen: Ebbinghaus's savings (1885), Spearman's correlations (1904),
   Stroop's times (1935), Murdock's recall curves (1962), Sternberg's scanning times (1966), Shepard and Metzler's
   rotations (1971), Holzinger and Swineford's test scores (1939), the Many Labs files, the Open Science
   Collaboration's hundred replications (2015).
7. **On every chapter card:** the timeline strip (1850–2030); the **levels strip**, which lights the scale the
   chapter works at (molecule, neuron, circuit, brain, mind, person, group, culture) and which of Marr's three
   levels it answers (what is computed, by what algorithm, in what tissue); and payoff cards ("where this comes
   back"). Each part closes with an *In practice* card (the jobs, products and decisions the idea serves) and a
   *Frontier* chapter (what is open). Cross-series links point to *Statistics, Built*, *AI, Built*, *Philosophy,
   Built* and *Computer Science, Built* instead of repeating them.

## Four ways through it

Every part is written so that its chapters climb. The opening chapters are the introductory course: the phenomenon,
the classic experiment, the demonstration on you. The middle chapters are the major and the graduate course: the
model, derived and fitted. The closing chapters are the Ledger, *In practice* and the *Frontier*. The course site's
four tracks follow from that (the tiers of `videos/coursekit`):

| Track | Who it is for | What it is |
|---|---|---|
| **U** · Psych 101 and the major | anyone; no mathematics beyond school algebra at the start | the opening chapters of Parts 1–43: a complete introductory course, then the major |
| **M** · The graduate course | a psychology graduate, or anyone with calculus, linear algebra and probability | the model chapters of every part, and Act XI (Parts 44–50) |
| **D** · The research tier | a PhD student | every part's Frontier chapter, and Act XIII (Parts 58–62) |
| **I** · Practice | UX researchers, behavioural scientists, psychometricians, I/O and clinical practitioners, data scientists | every part's In practice chapter, and Act XII (Parts 51–57) |

Milestones mark the degree: Part 43 is the capstone (a registered replication, run from preregistration to
report), Part 50 closes the graduate methods sequence, and Part 62 is the dissertation.

## The acts

| Act | Parts | Question |
|---|---|---|
| **I. Asking a Mind a Question** | 1–4 | Can the mind be measured, and how do we avoid fooling ourselves? |
| **II. The Wet Machine** | 5–10 | What is the mind made of? (neurons, circuits, the brain and how we read it, genes, the body's chemistry and clocks) |
| **III. Sensing** | 11–15 | How does a world get in? (thresholds, signal and noise, the eye, perception as inference, the other senses) |
| **IV. Learning** | 16–17 | How does experience change behaviour? (conditioning, reward and prediction) |
| **V. Thinking** | 18–27 | What happens between the stimulus and the response? (attention, memory, concepts, language, reasoning, decision, consciousness) |
| **VI. Feeling and Wanting** | 28–29 | Why do we act at all, and what are emotions for? |
| **VII. Growing** | 30–31 | Where does a mind come from, and how does it change over a life? |
| **VIII. Differing** | 32–33 | How do people differ, and what do the numbers mean? (intelligence, personality) |
| **IX. Other People** | 34–38 | What do minds do to each other? (influence, social cognition, groups and prejudice, bonds and bargains, culture and morals) |
| **X. When Minds Suffer** | 39–43 | What is a mental disorder, what causes it, and what helps? Then the capstone. |
| **XI. The Graduate Toolkit** | 44–50 | How is a claim about the mind made rigorous? (latent variables, IRT, scaling and choice, people over time, modelling behaviour, modelling brain data, the weight of evidence) |
| **XII. Psychology at Work** | 51–57 | Where is psychology a job? (human factors, design, hiring and work, education, behaviour change, law, health and care) |
| **XIII. The Frontier** | 58–62 | Where does the field stop knowing, and how do you push it? (the efficient brain, computational psychiatry, minds and machines, the next psychology, the dissertation) |

## How it looks

The series draws in the manner of 3Blue1Brown with the instruments of `explainer/ai/viz.py` and
`explainer/ai/lecture.py`, plus its own in `explainer/psychology/viz.py` (list in the syllabus, §3).

* **The experiment is on screen.** Every study is drawn as its trial strip (fixation, stimulus, response, feedback)
  before its result is shown, so the viewer knows exactly what the participant saw and did.
* **Then it is run on you.** A framed stage, a countdown, the stimulus, a pause to answer, and then the reveal:
  the published distribution, with a marker where most viewers fall.
* **Models are machines you can watch.** Ion-channel gates opening under a voltage trace; evidence wandering to a
  bound while the reaction-time histogram grows on the bound; a context vector drifting as a list is studied; a
  ball settling in an attractor landscape; prediction errors firing in red down a chain of states.
* **Model against data, always in the same colours.** Human data are white, Psyche is orange. An original study is a
  hollow marker and its replication a filled one. Signal is teal and noise grey; a prediction is purple and its
  error red; reward is gold; excitation is warm and inhibition cool.
* **The camera travels the levels.** From a face in a crowd to the fusiform gyrus, to a column, to one neuron, to a
  channel, and back out.
* **Real numbers.** Everything plotted is `computed` (the part's `compute.py`), `historical data` (the Archive,
  with source), `published` (cited), `simulated` (the Pool), `illustrative` or `schematic`, and tagged as such.

## The parts

| # | Part | Hook | Ideas, models and mathematics | Psyche gains | On you |
|---|---|---|---|---|---|
| **I** | **Asking a Mind a Question** | | | | |
| 1 | Kant's Wager | Kant 1786; Fechner's morning, 1850 | mental chronometry, Donders' subtraction, Helmholtz's nerve speed, Wundt, Ebbinghaus, James, behaviourism, the cognitive revolution, Marr's levels | a reaction-time stage model; the Homunculus, whole | simple and choice reaction time |
| 2 | The Experiment | Clever Hans, 1904–07 | confounds, random assignment (Peirce and Jastrow 1884), within and between designs, counterbalancing, blinding, placebo, demand, expectancy, ethics | the Pool; an experiment runner | a cueing demonstration: are you Hans? |
| 3 | The Measure | the committee that ruled sensation unmeasurable, 1940 | Stevens's scales, classical test theory, reliability and attenuation, Cronbach's α, validity and the nomological net, MTMM | a test-score simulator | the Forer personality reading |
| 4 | The Evidence | "Feeling the Future", 2011 | effect sizes, power, what a p-value is, flexible analysis, publication bias, the 2015 replication project, preregistration and registered reports | the Replication Ledger; a false-positive lab | forking paths: make a null result significant |
| **II** | **The Wet Machine** | | | | |
| 5 | The Neuron | Helmholtz times a frog's nerve; the squid's giant axon | Nernst and Goldman, the RC membrane, Hodgkin–Huxley derived, phase planes and bifurcations, cable theory, integrate-and-fire | a Hodgkin–Huxley neuron and its reductions | hear a spike train |
| 6 | Synapses and Circuits | Loewi's two frog hearts, 1921 | packets and receptors, synaptic integration and shunting, Hebb and Oja, LTP and spike timing, lateral inhibition, winner-take-all, half-centre oscillators, Wilson and Cowan's populations, where drugs act | plastic synapses; three small circuits; populations | Mach bands and the Hermann grid, straight and curved |
| 7 | The Brain | Phineas Gage, 1848; Tan; H.M. | a tour of the parts, Gall to Lashley, two aphasias and a diagram, single and double dissociation, cortical maps and magnification, H.M., the split brain, selective losses, plasticity, networks, the ten-percent myth | a lesionable architecture; lesion maps | find your blind spot, and measure it |
| 8 | Reading the Brain | a dead salmon in a scanner, 2009 | one neuron's tuning curve, EEG and the inverse problem, averaging and the N400, MRI in five minutes, the BOLD signal as a convolution, the GLM, a hundred thousand tests, circular analysis, reverse inference, intervention, how many people a study needs | a tuned cell, a toy head, a synthetic brain under each threshold | which reported correlation is impossible? |
| 9 | Genes and Evolution | two twins called Jim, 1979 | the family confound, many loci and a bell curve, Falconer's formula and the ACE path diagram, the twin design on the Pool and four ways it fails, what heritability is not, three laws, the candidate-gene decade, genome-wide association, polygenic scores within and between families, evolution as a source of hypotheses | twin, adoption and sibling simulators; a miniature genome | genes or the shared home, from two twin correlations |
| 10 | Chemistry and Clocks | Kleitman in Mammoth Cave, 1938 | the clock inside and what light does to it, sleep's stages, the two-process model and a night without sleep, chronotype, sleep loss that goes unnoticed, sleep and memory, dreams, the stress loop, four ways to change a synapse, dose and response, half-lives, tolerance and withdrawal as one process | a body: a clock, a sleep pressure, a stress loop, a dose | a vigilance task beside your own rating of alertness |
| **III** | **Sensing** | | | | |
| 11 | The Threshold | Fechner's morning, 22 October 1850 | Weber's fraction and where it fails, Fechner's logarithm, the three classical methods, the psychometric function fitted by maximum likelihood with a bootstrap interval and a goodness-of-fit check, staircases and QUEST, Stevens's power law and the range effect, Plateau's middle grey, the noise behind Weber's law and the square-root regime, Weber's law for number, time and money, the triangle test, Thurstone's scale | a psychophysical observer | measure your own threshold, by staircase, with a fitted curve |
| 12 | Signal and Noise | Radar observers and Mackworth's Clock Test, 1948 | four outcomes, d′ and c, the ROC and its area, the ideal observer and the accuracy trap, rating ROCs fitted by maximum likelihood, forced choice, threshold and dual-process rivals, base rates and natural frequencies, the prevalence effect, the vigilance decrement as caution or fatigue, double reading, line-ups, ROC against precision and recall, meta-d′ | a detection observer | an old/new test with confidence, and your own ROC |
| 13 | The Eye and the Code | A dark room at Columbia, 1942: a flash seen when five to fourteen quanta are absorbed | counting quanta from a curve's shape, optics, the mosaic and aliasing, gain control and Weber's law, the rate code, centre–surround and the difference of Gaussians, Mach bands, Gabor cells, the CSF and a hybrid image, channels and normalization, cone fundamentals, colour matching as linear algebra against the 1955 data, metamers, opponent colours, colour blindness, constancy and the dress, two streams | a retina, a V1 filter bank and the colour machinery | your contrast sensitivity at four stripe widths |
| 14 | Seeing as Inference | Two squares on a checkerboard send identical light and look different | the inverse problem, Gestalt laws as priors, disparity derived and a random-dot stereogram, constancy and its illusions, the normal posterior and shrinkage, cue combination predicted and tested, light from above and the slow prior, the aperture problem, retinex, objects and invariance, faces, a small network that learns texture | a Bayesian observer, a cue combiner, retinex and a convolutional network | your own Müller-Lyer illusion, by two staircases |
| 15 | The Other Senses | A note heard at 200 Hz in a sound with nothing at 200 Hz | the decibel as Fechner's law, the cochlea as a filter bank, masking, pitch by autocorrelation, interaural delays and Jeffress's circuit, scene analysis, categorical speech and the McGurk effect, roughness and consonance, touch and the rubber hand, the gate control of pain, smell's code and the trillion smells, balance | a cochlea, a pitch model, a Jeffress array and a gate | which way a missing fundamental moves |
| **IV** | **Learning** | | | | |
| 16 | Conditioning | Pavlov's dogs; Kamin's blocked rats | classical and operant conditioning, contingency, blocking, Rescorla–Wagner derived, attention models, schedules, the matching law, extinction and its return, preparedness | an associative learner, an operant chamber and a meliorating chooser | the gardener's game: predict the plants, reveal your ΔP |
| 17 | Reward and Prediction | Schultz's monkeys, 1997 | temporal-difference learning derived, the error's migration and Steinberg's unblocking, actor–critic, Q-learning and Go/NoGo, a bandit fitted and parameter recovery, exploration policies, latent learning, place and grid cells, devaluation and the two-step task, the successor representation and replay, ramps and a distributional code, Redish's drug | a TD learner, Q-learning bandits, a maze planner, two-step agents and a successor learner | two slot machines: your α and β fitted |
| **V** | **Thinking** | | | | |
| 18 | Attention | the gorilla nobody saw | filters, attenuation and load, spatial cueing and inhibition of return, feature integration, guided search, saliency and selection history, change and inattentional blindness, the blink and the PRP bottleneck, Stroop and conflict monitoring, the normalization model derived, Bundesen's race, vigilance and prevalence, phones and media | an attenuator, guided search, a saliency map, a Stroop diffusion and the normalization model | visual search: your set-size functions |
| 19 | Working Memory | the magical number seven | span and chunks, absolute judgment as a channel, partial report, Brown-Peterson forgetting and temporal distinctiveness, the multicomponent model and the word-length effect, memory scanning and parallel mimicry, change detection and K derived, slots against resources fitted to open data, ring attractors and silent synapses, working memory and reasoning, brain training | a phonological loop, SIMPLE, scanning models, mixture, swap and four process models, a ring attractor | change detection: your K |
| 20 | Memory I: Storing and Finding | Ebbinghaus alone with his syllables, 1885 | savings and forgetting laws, ACT-R activation, serial position and contiguity measured on open data, levels of processing and generation, encoding specificity and the divers replicated from open data, SAM, the temporal context model derived and fitted by maximum likelihood, Hopfield networks and capacity, memory systems and H.M., familiarity and recollection, the hippocampus as an index | SAM, a context model fitted to 3,528 lists, a Hopfield network, ACT-R activation, ROCs, pattern separation | free recall: your serial-position and lag-CRP curves |
| 21 | Memory II: Forgetting and Inventing | "smashed" or "hit"? | four forgetting laws fitted to Ebbinghaus and three replications, Jost's law and the averaging artefact, interference and retrieval-induced forgetting, consolidation in two stores, replay and reconsolidation, complementary learning systems and the penguin, spacing and testing with models fitted, schemas and the category adjustment model, the DRM illusion by global matching, misinformation and implanted memories, verbal overshadowing pooled from 53 replications' open data, flashbulb memories and line-up confidence by signal detection, half-life regression | forgetting laws, an associator, two stores, a semantic network, a spacing model, the bifurcation model, category adjustment, global matching, a line-up, half-life regression | the DRM lists: remember, know or new |
| 22 | Concepts and Categories | is a penguin a bird? | definitions and family resemblance, prototypes and the generalized context model with the 5-4 structure, the six problems and ALCOVE fitted to open data, multidimensional scaling of colours and Morse code, Shepard's universal law tested and derived, Tversky's contrast model and his asymmetry count rerun, semantic networks and priming at scale, the basic level and category utility, concepts as theories, the number game and the size principle, word vectors from Jane Austen, RSA and language models | the GCM, a prototype model, ALCOVE, non-metric MDS, consequential regions, the contrast model, category utility, a Bayesian concept learner, PPMI word vectors | the number game |
| 23 | Language | Chomsky reviews Skinner, 1959 | levels and productivity, Zipf's law and a typing monkey, the mental lexicon and the cohort, interactive activation, garden paths, surprisal fitted to the Natural Stories reading times, statistical segmentation, the past-tense debate, critical periods, the language network and the N400, language and thought | Zipf fits, interactive activation, a Kneser-Ney surprisal reader, a transitional-probability segmenter, a past-tense learner | find the words of a made-up language |
| 24 | Reasoning and Problem Solving | Wason's four cards | deduction and its biases, mental models, problem spaces and search, insight, expertise and chunking, analogy, imagery and mental rotation, causal learning, production systems | a production system; a mental rotator | the selection task; mental rotation |
| 25 | Deciding in Time | a walk to a boundary | Hick and Fitts, the speed–accuracy trade-off, random walks, the drift–diffusion model, optimality (the SPRT), accumulators in the brain, the stop signal, confidence | a diffusion decision maker | moving dots, fast and then careful |
| 26 | Judgment and Choice | the disease problem, 1981 | expected utility and its violations, prospect theory derived, heuristics and biases, fast and frugal heuristics, discounting, dual-process accounts and their critics | a prospect-theory chooser; a heuristics toolbox | the classic problems, with the published splits |
| 27 | Consciousness | the patient who saw without seeing | blindsight, neglect, rivalry and masking, the search for correlates, the global workspace, integrated information, adversarial collaborations, volition, sleep and anaesthesia | a workspace that ignites | masking: what did you see? |
| **VI** | **Feeling and Wanting** | | | | |
| 28 | Motivation | the rat that would not stop pressing | drives and homeostasis as control, hunger, incentive salience, wanting and liking, intrinsic motivation, goals, self-control and the depletion story, delay of gratification | a homeostat with wants | discount your own delays |
| 29 | Emotion | James's bear | James–Lange to appraisal, basic emotions against construction, the facial-feedback saga, fear and the amygdala, stress, regulation, affective forecasting, happiness and income | an appraisal model; an affect space | place faces in the circumplex |
| **VII** | **Growing** | | | | |
| 30 | The Infant Mind | how do you ask a baby? | looking-time and habituation, Piaget, object permanence, core knowledge, number sense, the A-not-B error as dynamics, theory of mind, attachment | a habituating infant; a dynamic field | predict the infant |
| 31 | The Lifespan | the orphanages of Bucharest | cross-sectional against longitudinal designs, growth curves, sensitive periods, adolescence, parenting and behaviour genetics, early intervention, cognitive ageing | growing and ageing Psyches | age, period or cohort? |
| **VIII** | **Differing** | | | | |
| 32 | Intelligence | Binet's commission, 1904; Spearman's matrix | the positive manifold, factor analysis derived, g and its rivals, the mutualism model, IQ scaling, heritability, the Flynn effect, group comparisons and measurement invariance, the eugenic history | a factor analyser; two worlds with one manifold | matrix puzzles (unscored) |
| 33 | Personality | 17,953 words | the lexical hypothesis, the Big Five, the person–situation debate, stability and change, prediction of life outcomes, types against traits, the Barnum effect, Freud's legacy, digital footprints | traits for the Pool | a public-domain Big Five inventory |
| **IX** | **Other People** | | | | |
| 34 | Social Influence | the shock generator, 1961 | conformity, obedience, bystanders, the prison study and its record, facilitation and loafing, persuasion, thresholds and cascades, opinion dynamics, the wisdom of crowds | agents on a network | Asch's lines; a crowd estimate |
| 35 | Social Cognition | one dollar or twenty | attribution, dissonance and self-perception, attitudes and behaviour, the self and its illusions, first impressions, priming and its collapse, Bayesian theory of mind | an inverse planner | Heider and Simmel's triangles |
| 36 | Us and Them | Klee or Kandinsky | minimal groups, social identity, Robbers Cave, stereotypes, implicit measures and what they predict, stereotype threat, contact, audit studies, prejudice reduction in the field | groups for the agents | a minimal-group allocation |
| 37 | Bonds and Bargains | the ultimatum | attraction and what predicts it, attachment in adults, relationship science and its limits, cooperation, reciprocity and punishment, trust, loneliness and health | players of repeated games | the ultimatum and public goods games |
| 38 | Culture and Morals | the WEIRDest people | whose psychology?, individualism and collectivism, illusions across cultures, cultural evolution, moral intuition and reasoning, the trolley and the Moral Machine | cultural learners | trolley cases, against forty-two countries |
| **X** | **When Minds Suffer** | | | | |
| 39 | What Is a Disorder? | "On Being Sane in Insane Places" | the history of diagnosis, reliability and kappa, categories against dimensions, comorbidity and the p factor, symptom networks, epidemiology, clinical against statistical prediction | a symptom network with hysteresis | a base-rate diagnosis problem |
| 40 | Fear and Sadness | dogs that did not jump | anxiety as learning, extinction and exposure, learned helplessness revised, the cognitive model, the monoamine story, antidepressant trials, trauma, OCD, bipolar disorder, suicide prediction | a helpless learner; an avoidance loop | an attentional-bias probe |
| 41 | Psychosis, Addiction and Development | a mask that will not look hollow | schizophrenia and dopamine, aberrant salience, hallucination as inference, genetics, addiction as hijacked learning, autism, ADHD | priors too strong and too weak | the hollow mask |
| 42 | Does Therapy Work? | Eysenck's challenge, 1952 | the therapy trial and its controls, regression to the mean, meta-analysis born, the dodo bird, CBT and exposure, medication, placebo, publication bias, clinical significance | a therapy trial simulator | spot the regression to the mean |
| 43 | **The Replication** (capstone) | one classic effect, run again | a registered replication from choice of target to report: power, preregistration, materials, exclusion rules, analysis, the write-up | the capstone report | take part in the replication |
| **XI** | **The Graduate Toolkit** | | | | |
| 44 | Latent Variables | Wright's guinea pigs; the 1939 test battery | path analysis, confirmatory factor analysis, structural equation models, identification, fit, invariance, mediation and its limits, equivalent models, networks against factors | `psyche.sem` | draw the model that fits as well |
| 45 | Item Response Theory | Rasch's reading tests | Rasch, 2PL and 3PL, information, estimation, adaptive testing, differential item functioning, equating, plausible values, knowledge tracing | `psyche.irt`; an adaptive test | a ten-item adaptive test (unscored) |
| 46 | Scaling, Surveys and Choice | Thurstone asks which crime is worse | comparative judgment, Luce's axiom, Bradley–Terry, random utility and the logit, conjoint and MaxDiff, context effects, the survey response process, Likert scales and response styles | `psyche.scaling`; a conjoint engine | the decoy effect; a paired-comparison scale |
| 47 | People over Time | the language-as-fixed-effect fallacy, 1973 | repeated measures, crossed random effects, growth models, experience sampling, within against between persons, ergodicity, cross-lagged panels, early-warning signals | mixed models on the Pool | Simpson's paradox inside one person |
| 48 | Modelling Behaviour | learning curves that no one has | likelihoods for behaviour, fitting, parameter and model recovery, model comparison, hierarchical Bayes, falsification by simulation, rational and resource-rational analysis, networks and language models as cognitive models | `psyche.fit`: the modelling harness | fit a model to your own bandit data |
| 49 | Modelling the Brain's Data | seventy teams, one dataset | the fMRI pipeline, random fields and clusters, decoding, representational similarity, encoding models, connectivity, ERP analysis, population codes, brain–computer interfaces, the sample-size problem | `psyche.neurodata` on a synthetic brain | how many analysis paths? |
| 50 | The Weight of Evidence | 94% positive, 51% registered | meta-analysis, heterogeneity, bias detection and correction, registered reports, multi-site replications, forensic statistics, the multiverse, many analysts, the theory crisis | `psyche.meta`; the Ledger audited | GRIM: catch an impossible mean |
| **XII** | **Psychology at Work** | | | | |
| 51 | Human Factors | the B-17's two identical levers | design-induced error, displays and controls, workload, vigilance, situation awareness, automation and its ironies, the Swiss cheese model, checklists, screening and prevalence | an operator model | a vigilance clock |
| 52 | Designing for Minds | Project Ernestine | the Model Human Processor, GOMS and the keystroke-level model, Fitts in the interface, information foraging, usability testing and its sample sizes, graphical perception, accessibility, dark patterns, habit | a keystroke-level predictor | your Fitts' law slope; rank the charts |
| 53 | People at Work | the Hawthorne plant | selection and validity, range restriction, utility analysis, adverse impact and the trade-off frontier, interviews, performance ratings, motivation and incentives, teams, remote work, hiring algorithms | a selection simulator | interview or test: who gets hired? |
| 54 | The Science of Learning | Bloom's two sigma | retrieval practice, spacing and interleaving, desirable difficulties, cognitive load, learning-styles and other myths, tutoring, intelligent tutors, review scheduling as optimal control, reading instruction, mindset at scale | a review scheduler on the memory model | spaced against massed, on you |
| 55 | Behaviour Change at Scale | the default that made donors | defaults and nudges, megastudies, the gap between papers and nudge units, heterogeneity, incentives, norms, persuasion and its small effects, advertising measurement, misinformation, the ethics of steering | a megastudy simulator | choose the winning nudge |
| 56 | Psychology and Law | the line-up | eyewitness identification as signal detection, confidence and accuracy, false confessions, lie detection, expert bias in forensics, juries, risk assessment, memory wars, the standard error in the Supreme Court | a line-up ROC | pick from a line-up |
| 57 | Health and Care | stress and the common cold | stress and illness, placebo and nocebo, pain, adherence, lifestyle trials, sleep treatment, stepped care, measurement-based care, digital therapeutics, task sharing | a stepped-care simulator | open-label placebo: what would you predict? |
| **XIII** | **The Frontier** | | | | |
| 58 | The Efficient, Predictive Brain | Barlow's redundancy, 1961 | efficient coding, sparse coding and the emergence of receptive fields, normalization, predictive coding, the free-energy principle derived and criticized, resource rationality, unified architectures | sparse coding on natural images | adaptation after-effects, predicted |
| 59 | Computational Psychiatry | a task score that will not hold still | models as assays, the reliability paradox, biotypes and their replication, treatment selection, prediction that fails to transfer, neuromodulation, psychedelic trials and unblinding | a precision-psychiatry trial bench | reliable or sensitive: pick one |
| 60 | Minds and Machines | the Perceptron was a psychologist's | networks as models of vision and language, machine psychology, theory-of-mind tests and their critics, people trusting and distrusting algorithms, chatbots as therapists and persuaders, silicon samples, screens and well-being | Psyche against language models on the Battery | human or model? |
| 61 | The Next Psychology | 160 teams fail to predict a life | big team science, experiments at the scale of millions, integrative experiment design, prediction against explanation, who is sampled, the natural selection of bad science, theory building, automated discovery | a model of a research community | design the experiment space |
| 62 | **The Dissertation** | back to Kant | how research is done: ethics, a question, a registered report from Stage 1 to Stage 2, the final Ledger, Psyche's Battery scorecard, the Homunculus's remaining parts, the open problems | the thesis | the last experiment |

## What it follows

The series reads like the reading lists of a strong department. The spines (each part's reference card names its
own, and the syllabus lists them):

| Tier | Main texts |
|---|---|
| Introductory | Gleitman, Gross & Reisberg; Myers & DeWall; Gray & Bjorklund; Schacter, Gilbert, Nock & Wegner; James, *The Principles of Psychology* |
| The major | Kandel et al., *Principles of Neural Science*; Bear, Connors & Paradiso; Wolfe et al., *Sensation & Perception*; Bouton, *Learning and Behavior*; Baddeley, Eysenck & Anderson, *Memory*; Anderson, *Cognitive Psychology and Its Implications*; Siegler et al., *How Children Develop*; Aronson, Wilson & Sommers; Funder, *The Personality Puzzle*; Barlow, Durand & Hofmann; Shadish, Cook & Campbell |
| Graduate and mathematical | Dayan & Abbott, *Theoretical Neuroscience*; Green & Swets; Macmillan & Creelman; Kingdom & Prins; Sutton & Barto; Kahana, *Foundations of Human Memory*; Luce, *Response Times*; Farrell & Lewandowsky, *Computational Modeling of Cognition and Behavior*; Lee & Wagenmakers; Griffiths, Chater & Tenenbaum, *Bayesian Models of Cognition*; Bollen; Embretson & Reise; Lord & Novick; Train, *Discrete Choice Methods*; Poldrack, Mumford & Nichols; Luck, *An Introduction to the Event-Related Potential Technique*; Borenstein et al., *Introduction to Meta-Analysis* |
| Practice | Wickens et al., *Engineering Psychology and Human Performance*; Card, Moran & Newell; Norman; Schmitt (ed.), *The Oxford Handbook of Personnel Assessment and Selection*; Dunlosky et al. (2013); Thaler & Sunstein; Wells and Wixted's reviews; Barlow (ed.), *Clinical Handbook of Psychological Disorders* |
| History and metascience | Boring; Hunt, *The Story of Psychology*; Danziger, *Constructing the Subject*; Chambers, *The Seven Deadly Sins of Psychology*; Ritchie, *Science Fictions*; Meehl's papers |

## Standards (as *AI, Built* and *Philosophy, Built*, plus psychology's own)

* **Every number is real.** Computed in the part's `compute.py` and cached in `.cache/psychN/`, transcribed into
  the Archive with its source, or cited. Pool results are labelled `simulated`.
* **Every empirical claim carries its evidence.** Sample size, effect size with an interval, and its Ledger status.
  "Significant" is never the whole report. Where the famous version of a story differs from the record, both are
  shown.
* **Every model is run against data.** A model on screen is fitted or simulated against the human benchmark, and
  the screen shows where it fits and where it fails.
* **Each side gets its best case.** On open controversies (nature and nurture, modularity, what IQ measures, what
  implicit measures measure, whether social media harms, what consciousness is) the strongest version of each
  position is presented with its evidence, and the narration says that the question is open.
* **Care.** Clinical material is education, not advice, and says so. The demonstrations never diagnose or score a
  viewer: there is no IQ, no clinical cut-off, no personality type. Suicide and self-harm are covered under
  safe-messaging guidelines. The history of harm (eugenics, lobotomy, unethical experiments) is told plainly. Named
  patients are treated as people. Copyrighted tests and diagnostic criteria are described, not reproduced; the
  series uses public-domain instruments and generates its own items.
* **Bilingual.** English and Chinese, as the other series: `narration_zh.json`, `psychology_text_zh.json`,
  `PSYCHOLOGY_ZH_GUIDE.md`.

## Shared code

`explainer/psychology/` holds what every part shares:

| Module | What it is |
|---|---|
| `psyche/` | Psyche, the model subject: one module per faculty. So far `chronometry` (serial stages, Donders' subtraction, the insertion test, additive factors, Hick's law, the ex-Gaussian) `cueing` (Clever Hans as a reader of an involuntary cue), `neuron` (Nernst and Goldman, Hodgkin-Huxley with the clamp and the cable, FitzHugh-Nagumo, integrate-and-fire, spike trains, dendritic branches) and `circuits` (synapses on a membrane, Hebb's, Oja's and the BCM rule, lateral inhibition and the Hermann grid, winner-take-all, a half-centre oscillator, Wilson and Cowan's populations) and `brain` (a box-and-arrow architecture that can be lesioned, Lashley's maze in a model cortex, one resource against two with noisy tests, the single-case t test, cortical magnification, the blind spot, lesion-symptom mapping on a sheet fed by one artery) and `imaging` (a tuned cell, dipole sums and a toy head with a silent source, ERP averaging, relaxation and k-space, the haemodynamic response and the general linear model, a synthetic brain thresholded by each rule, cluster calibration, circular selection, reverse inference, the reliability ceiling, the small-study simulator) and `genes` (many loci, twin and adoption designs with each assumption switchable, Falconer and a maximum-likelihood ACE fit, a genome-wide scan and polygenic scores, the sibling design, the gain from choosing among embryos) and `body` (a clock that light sets, the two-process model of sleep, lapses under short sleep, a hormone loop with a brake, receptor occupancy and half-lives, an opponent process, tolerance tied to a place, chronotype) and `psychophysics` (an observer with floor, Weber and photon noise, psychometric functions and their maximum-likelihood fits with bootstrap intervals, the classical methods, staircases and QUEST, Fechner's count, Stevens's power law, the triangle test, Thurstone's Case V) and `sdt` (the equal- and unequal-variance observer, d′ and c, ROCs and their fits, the ideal observer under base rates and payoffs, forced choice, threshold and dual-process rivals, predictive value) and `vision` (frequency of seeing, optics and sampling, gain control, differences of Gaussians, Gabor cells, normalization, the CSF, colour matching, metamers, opponent channels, dichromacy, constancy) and `infer` (the normal posterior, reliability-weighted cue combination and a two-interval observer, the slow prior and the MAP velocity, retinex on a checkerboard in shadow, disparity and stereograms, a one-layer convolutional network and its texture bias) and `hearing` (decibels and the threshold in quiet, a gammatone filter bank and Greenwood's map, masking, pitch by summary autocorrelation, interaural delays and a Jeffress array, the label model of categorical perception, the McGurk effect as cue combination, the gate control of pain, a count of odour mixtures) |
| `lab.py` | the laboratory: assignment by shuffle, counterbalancing, the comparison and its randomization test, power, and the sound and unsound designs run on the Pool with the truth known |
| `measure.py` | measurement: Stevens's scale types, reliability, Spearman-Brown, alpha, the correction for attenuation, kappa, the intraclass correlation, the multitrait-multimethod matrix, a factor model against a network, the cancellation conditions |
| `evidence.py` | the false-positive lab: effect sizes, power, optional stopping, the four forks, a literature with a publication filter, p-curves, replications planned from the printed effect, equivalence tests, a Bayes factor |
| `pool.py` | the Pool: 100,000 simulated people with planted truths, always tagged *simulated* on screen |
| `battery.py` | the Battery: the tasks, and one `run(task, model)` interface that Psyche, the Pool and the browser share |
| `ledger.py` | the Replication Ledger: one validated row per finding, with sources and the date checked; `tools/check_ledger.py psychN` is its gate (every study a part shows has a row, or a stated reason) |
| `archive/` | the Archive: historical and published numbers, each with its source in `archive/SOURCES.md` |
| `__init__.py`, `viz.py`, `style.py` | chapter cards with the timeline and levels strips, the series map, the Homunculus map, the demo stage, stage bars, ledger cards and boards, the palette |

Tests are in `tests/psychology/`. The code reuses `explainer.stats.kit` (mixed models, shrinkage and meta-analysis,
factor analysis and MDS, IRT, the probabilistic programming language for hierarchical fits) and
`explainer.ai.autodiff`, and will use the language model of *AI, Built* for reading-time predictions. The course
material follows `videos/coursekit` (a course entry, a lab and an interactive per part); for this series the
interactive is the part's experiment on the reader, built on the task kit
(`course/site/widgets/00_tasks.js`); it keeps its data in the page and sends nothing.

## Decisions taken

The defaults below were accepted on 2026-11-13 and the series is being built to them. Details in the syllabus, §8.

1. **Scope: sixty-two parts, about 52 hours.** The alternative is a first season of Parts 1–43 (the degree, about
   36 hours) with Acts XI–XIII committed to later.
2. **Length: 30–60 minutes, most at 45–55**, as asked. The other series run 50–60; `tools/lecture_length.py`
   already defaults to a 30-minute floor.
3. **Video names `psych1` … `psych62`** in `videos/psychology/` (shorter than `psychology1`, and no clash with the
   existing names).
4. **Bilingual from the start**, like the recent series, or English first like *Statistics, Built*.
5. **The experiments on the viewer** are a core device. On the site they run in the browser and store nothing.
6. **The order.** Methods come first (Act I) because the Ledger needs them, but they are told as stories (a horse,
   a committee, a paper on precognition). The alternative is to open with the senses and move Act I's parts later.
