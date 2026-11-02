"""The House: the series' own quant library, built part by part (videos/quant/SYLLABUS.md, "The House").

Each module is a desk's tools, tested in ``tests/test_quant_house.py``; scenes and compute modules import them
explicitly (``from explainer.quant.house import bs, hedge``).

* :mod:`pit` (Part 1, data & technology): the point-in-time rule and the sealed envelope (the hold-out from 2021);
* :mod:`stats` (Part 1): returns, autocorrelations, Lo–MacKinlay variance ratios, Hill tail exponents;
* :mod:`smile` (Parts 1, 12): raw SVI, the Breeden–Litzenberger density, Martin's SVIX;
* :mod:`funding` (Part 2, treasury & funding): margin accounts and liquidation, netting, auctions, fees, haircuts;
* :mod:`valuation` (Part 3): NPV, IRR, annuities, Gordon, DCF, WACC, Modigliani-Miller, Merton's equity;
* :mod:`fundamentals` (Part 3, data & technology): the bitemporal store of reported numbers, as of a filing date;
* :mod:`martingale` (Part 4, research): the doubling system, gambler's ruin, Doob's decomposition, likelihood
  ratios, stable-law fits, and the e-value monitor (testing by betting);
* :mod:`sim` (Part 5): the simulation library: Euler and Milstein with their orders, exact OU and CIR, Merton jumps,
  Hawkes processes, fractional Brownian motion, the Hurst exponent, path signatures;
* :mod:`econ` (Part 6, research): OLS with HAC and clustered errors, Fama-MacBeth, block bootstraps, Sharpe ratio
  errors, multiple testing, Stambaugh's bias, GMM, double machine learning, shrinkage;
* :mod:`vol` (Part 7): the volatility forecaster: realized measures, EWMA, GARCH/GJR/EGARCH, HAR(Q), QLIKE and
  Diebold-Mariano, ADF and Engle-Granger, Markov switching, the Kalman filter, DCC;
* :mod:`control` (Part 8, portfolio & risk): utility, Merton by dynamic programming, Kelly and realized growth, the
  secretary problem, BSDEs by regression (with two interest rates), PPO on Merton's problem;
* :mod:`arbitrage` (Part 9, research): the FTAP by linear programming, super-replication, static checks on a
  surface, martingale optimal transport bounds, Ross recovery;
* :mod:`bs` (Part 10, the volatility desk): Black–Scholes–Merton prices, Greeks, Black-76, implied volatility;
* :mod:`trees` (Part 10): Cox–Ross–Rubinstein trees, American exercise and its boundary;
* :mod:`paths` (Parts 5, 10, 13): GBM and Heston paths, realized volatility;
* :mod:`hedge` (Part 10): the delta-hedged book and its P&L decomposition;
* :mod:`surface` (Parts 1, 10, 12): the frozen options surface (the series' pricing scoreboard).
"""

from explainer.quant.house import arbitrage, bs, control, econ, fundamentals, funding, hedge, martingale, sim, vol, paths, pit, smile, stats, surface, trees, valuation  # noqa: F401
