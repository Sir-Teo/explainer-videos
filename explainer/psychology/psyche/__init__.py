"""Psyche, the model subject of *Psychology, Built* (videos/psychology/SYLLABUS.md, §2.1).

*Psyche* is Greek for breath, for the soul, and for a butterfly.  Here it is a library of small models, one faculty
per part of the series, each a few hundred lines of numpy whose docstring states its equations.  Three rules:

* **It runs the same tasks people do.**  A model produces trial-level data in the Battery's format
  (:mod:`explainer.psychology.battery`), so one plotting and fitting pipeline serves people, Psyche and the Pool.
* **It is checked.**  Every module has tests in ``tests/psychology/`` against an independent reference: a closed
  form, a published parameter set reproducing a published figure, or SciPy.
* **It is fitted, not tuned by eye.**  Parameters shown on screen come from a fit to named data.

Nothing in this package imports manim, so the labs and the tests use it on its own.

Modules so far, with the part that introduces each:

=================  ====  ===============================================================================
``chronometry``     1    serial stage models of reaction time: Donders' subtraction, pure insertion and
                         its distributional test, additive factors, Hick's logarithm, the ex-Gaussian
``cueing``          2    an observer who reads a questioner: Clever Hans as a psychometric function
``neuron``          5    Nernst and Goldman, the membrane as a circuit, Hodgkin and Huxley with the voltage
                         clamp and the cable, FitzHugh-Nagumo, integrate-and-fire, spike trains, dendrites
``circuits``        6    conductance synapses and shunting; Hebb, Oja, BCM and STDP; lateral inhibition and
                         a centre-surround filter; winner-take-all; a half-centre oscillator; Wilson-Cowan
``brain``           7    box-and-arrow architectures that can be lesioned; dissociations with noisy tests;
                         one patient against a small control sample; cortical magnification and the blind
                         spot; lesion-symptom mapping on a sheet fed by one artery
``imaging``         8    the measurement chain: a tuning curve; dipole sums and a toy lead field; averaging
                         and event-related potentials; the Fourier pair behind an MR image; the haemodynamic
                         response and the linear model; a synthetic brain under four thresholds; circular
                         selection; reverse inference, the reliability ceiling, small studies of small effects
``genes``           9    many loci make a bell curve; twin, adoption and family designs under the infinitesimal
                         model, with each assumption switchable; Falconer and a maximum-likelihood ACE fit;
                         a genome-wide association study and polygenic scores; within- and between-family
                         effects; stratification; the gain from choosing among embryos
``body``            10   a light-driven circadian oscillator (entrainment, phase response, jet lag); the
                         two-process model of sleep and an alertness curve; lapses under sleep restriction;
                         the stress axis as a feedback loop; the Hill equation, antagonists and elimination;
                         the opponent process and conditioned tolerance; chronotype
``psychophysics``   11   an observer whose noise grows with the signal (Weber's law and its failure near the
                         floor); the psychometric function and its maximum-likelihood fit with a bootstrap;
                         Fechner's three methods; staircases and a Bayesian placement rule; Fechner's and
                         Stevens's scales; magnitude estimation and cross-modality matching; photon noise;
                         the triangle test; paired comparisons and Thurstone's Case V
``sdt``             12   the equal- and unequal-variance observer; d' and c from rates; ROCs, zROCs and their
                         area; rating ROCs fitted by maximum likelihood; the ideal observer under base rates
                         and payoffs; forced choice; high-threshold and dual-process rivals; natural
                         frequencies; the prevalence effect
``vision``          13   frequency of seeing as a Poisson tail and its fit; diffraction, blur, Nyquist and
                         aliasing; gain control and Weber's law; differences of Gaussians and Mach bands;
                         Gabor fields, simple and complex cells; normalization; the CSF and its fit; cone
                         fundamentals, colour matching, metamers, chromaticity; opponent channels, dichromacy
                         and von Kries constancy
``infer``           14   the normal posterior and reliability-weighted combination; a two-interval observer
                         with one or two cues and a conflict; speed under a slow prior; edge constraints and
                         the MAP velocity; a checkerboard in shadow and retinex; disparity and random-dot
                         stereograms; textured shapes and a one-layer convolutional network with its texture
                         bias
``hearing``         15   decibels and the threshold in quiet; harmonic complexes; the ERB scale, Greenwood's
                         map and a gammatone filter bank; masking; pitch by summary autocorrelation;
                         interaural delays and a Jeffress array; the label model of categorical perception;
                         the McGurk effect as cue combination; the gate control of pain; odour mixtures
``conditioning``    16   Rescorla-Wagner for any design and its exact asymptote (ΔP); Mackintosh and
                         Pearce-Hall attention; extinction bound to context (renewal, spontaneous recovery);
                         Thorndike's box; shaping; the four schedules; melioration and matching; timing
``rl``              17   TD learning on a delay line (the dopamine error and its migration); second-order
                         conditioning; Q-learning bandits fitted by likelihood; exploration policies; a maze
                         with latent learning; the two-step task; the successor representation; a
                         distributional code; Redish's drug that cannot be predicted away
``attention``       18   the dichotic attenuator and load; cueing and inhibition of return; guided search,
                         saliency maps and scan paths; prevalence; the flicker paradigm; the attentional blink
                         and the PRP bottleneck; Stroop as a diffusion with conflict monitoring; the
                         normalization model of attention; Bundesen's race; vigilance
``wm``              19   absolute judgment as a channel; the phonological loop; partial report; SIMPLE's
                         temporal distinctiveness; memory scanning, serial and parallel; slots and the K
                         formulas; von Mises precision, mixture, swap and four process models fitted by
                         maximum likelihood; a ring attractor; training trials; a shared information budget
``memory``          20   forgetting laws fitted to Ebbinghaus; serial position, first recall and the lag-CRP;
                         SAM's buffer and search; the context maintenance and retrieval model, its exact
                         likelihood and a maximum-likelihood fit; a Hopfield network and its capacity; ACT-R's
                         activation; dual-process and unequal-variance ROCs; pattern separation
``memory``          21   four forgetting laws and AIC; Jost's law; the averaging artefact; associator
                         interference; two-store consolidation; the penguin in Rumelhart's network; Pavlik and
                         Anderson's spacing; the bifurcation model; category adjustment; DRM by global matching;
                         line-up confidence by signal detection; half-life regression
``concepts``        22   the generalized context model and the prototype model; the six problems with ALCOVE
                         and a delta-rule network; classical and non-metric scaling; Shepard's generalization
                         measure, law and consequential regions; Tversky's contrast model and asymmetry count;
                         category utility; spreading activation; the number game; PPMI word vectors; card sorts;
                         RSA
``language``        23   Zipf's law and the typing monkey; cohorts; the interactive activation model with a
                         14-segment font; transitional probabilities and segmentation; a past-tense learner;
                         a Kneser-Ney trigram and surprisal; the reading-time regression; Flesch's formula
``reason``          24   syllogisms by brute force over set models and four accounts scored; optimal data
                         selection; the Tower of Hanoi's state graph, a goal-stack production system and a
                         hill-climber; the nine dots; structure mapping; rotation fits; causal power; everyday
                         predictions by posterior medians
``decide``          25   Wald's sequential test and its operating characteristic; the diffusion model's closed
                         forms, first-passage densities (Navarro and Fuss) and fits by maximum likelihood and EZ;
                         the linear ballistic accumulator; Hick's race; the stop-signal race and SSRT;
                         balance-of-evidence confidence; urgency; the attentional drift diffusion model
``choice``          26   expected value and utility; St Petersburg; the probability triangle; cumulative prospect
                         theory, certainty equivalents and the fourfold pattern; choice models fitted and
                         cross-validated; natural frequencies; take-the-best; the hot-hand bias; discounting;
                         choices from samples; decision by sampling
``workspace``       27   masking as one signal read twice (the criterion problem); a rivalry oscillator; a
                         two-stage ignition network; effective information and Φ (Tononi 2004); Schurger's
                         accumulator; Lempel–Ziv complexity and the perturbational complexity index
``drive``           28   a thermostat with integral control; energy balance with a settling point and a
                         defended set point; a learner given a current; incentive value recomputed from
                         state; self-perception as Bayes; the expected value of control; rational waiting;
                         random-effects meta-analysis and the precision-effect test; discount titration
``emotion``         29   classical scaling, scale fitting and Procrustes; schematic faces and a
                         same-or-different observer; arousal attribution; an appraisal model; LeDoux's two
                         roads; hedonic adaptation and a forecaster; a hidden income plateau; Lorenz by RK4
``develop``         30   habituation; an ideal learner's surprisal and a Goldilocks observer; number by
                         ratio; the infant statistician; a dynamic neural field for A-not-B, run for
                         many infants at once; random-effects meta-regression
=================  ====  ===============================================================================
"""
