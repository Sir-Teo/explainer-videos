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
                         Stevens's scales; magnitude estimation and cross-modality matching
=================  ====  ===============================================================================
"""
