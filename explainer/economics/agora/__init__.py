"""Agora, the economy that *Economics, Built* builds (videos/economics/SYLLABUS.md, section 2.1).

*Agora* is Greek for the gathering place that became the market.  It is a small, tested library (numpy and scipy
only, no manim) that gains one mechanism in each part.  Every model is checked against something it did not compute
itself (a closed form, a second algorithm, a published table) in ``tests/economics/``.

Modules so far:

* :mod:`.market` (Part 1): traders with one unit each and a private limit price; the competitive prediction
  (quantity, price band, surplus); a continuous double auction run by zero-intelligence traders (Gode and Sunder
  1993) or by traders who adjust their margins (Cliff 1997); Smith's coefficient of convergence and the market's
  efficiency.
* :mod:`.crusoe` (Part 1): one person's production possibilities and choice at the margin; two people,
  comparative advantage, and the competitive equilibrium of their trade.
* :mod:`.signals` (Part 1): Hayek's tin market: many users who see only a price, a supply shock, the price that
  clears, and the cost of rationing the same cut without a price.

Conventions: a model is plain data plus functions; randomness comes from a ``numpy.random.Generator`` passed in or
from a ``seed``; results are dicts of floats and lists, so a part's ``compute.py`` can cache them as they are.
"""
