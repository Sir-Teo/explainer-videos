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
=================  ====  ===============================================================================
"""
