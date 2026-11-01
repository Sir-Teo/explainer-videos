"""The House: the series' own quant library, built part by part (videos/quant/SYLLABUS.md, "The House").

Each module is a desk's tools, tested in ``tests/test_quant_house.py``; scenes and compute modules import them
explicitly (``from explainer.quant.house import bs, hedge``).

* :mod:`bs` (Part 10, the volatility desk): Black–Scholes–Merton prices, Greeks, Black-76, implied volatility;
* :mod:`trees` (Part 10): Cox–Ross–Rubinstein trees, American exercise and its boundary;
* :mod:`paths` (Parts 5, 10, 13): GBM and Heston paths, realized volatility;
* :mod:`hedge` (Part 10): the delta-hedged book and its P&L decomposition;
* :mod:`surface` (Parts 1, 10, 12): the frozen options surface (the series' pricing scoreboard).
"""

from explainer.quant.house import bs, hedge, paths, surface, trees  # noqa: F401
