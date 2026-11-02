"""The House: the series' own quant library, built part by part (videos/quant/SYLLABUS.md, "The House").

Each module is a desk's tools, tested in ``tests/test_quant_house.py``; scenes and compute modules import them
explicitly (``from explainer.quant.house import bs, hedge``).

* :mod:`pit` (Part 1, data & technology): the point-in-time rule and the sealed envelope (the hold-out from 2021);
* :mod:`stats` (Part 1): returns, autocorrelations, Lo–MacKinlay variance ratios, Hill tail exponents;
* :mod:`smile` (Parts 1, 12): raw SVI, the Breeden–Litzenberger density, Martin's SVIX;
* :mod:`funding` (Part 2, treasury & funding): margin accounts and liquidation, netting, auctions, fees, haircuts;
* :mod:`valuation` (Part 3): NPV, IRR, annuities, Gordon, DCF, WACC, Modigliani-Miller, Merton's equity;
* :mod:`bs` (Part 10, the volatility desk): Black–Scholes–Merton prices, Greeks, Black-76, implied volatility;
* :mod:`trees` (Part 10): Cox–Ross–Rubinstein trees, American exercise and its boundary;
* :mod:`paths` (Parts 5, 10, 13): GBM and Heston paths, realized volatility;
* :mod:`hedge` (Part 10): the delta-hedged book and its P&L decomposition;
* :mod:`surface` (Parts 1, 10, 12): the frozen options surface (the series' pricing scoreboard).
"""

from explainer.quant.house import bs, funding, hedge, paths, pit, smile, stats, surface, trees, valuation  # noqa: F401
