"""The Island (videos/economics/SYLLABUS.md, section 2.2): Agora run as one seeded world that persists across the
series.

The Island grows as the series does: one castaway in Part 1, a fish market in Part 2, a village and its firms, a
bank in Part 26, a second island in Part 34, a hundred thousand households by Part 52.  In the real economy the
truth is hidden; on the Island it is known, so a method can be graded against it.  Everything drawn from the Island
is labelled ``simulated``.

:data:`CAST` is the cast, one glyph colour and one name each for the whole series; :data:`TRUTHS` the planted
parameters, part by part.  A part's ``compute.py`` reads its truths from here, so a later part that reuses the
Island's past (the recession of Part 27, the inflation of Part 28) works from the same numbers.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Islander:
    key: str
    name: str
    role: str
    color: str
    arrives: int  # the part in which they first appear


CAST = {
    "crusoe": Islander("crusoe", "Crusoe", "the castaway: fisher, gatherer, later the boatyard's owner", "#E8C07D", 1),
    "friday": Islander("friday", "Friday", "the second islander: gatherer, later the coconut grove", "#7FD1B9", 1),
    # the village of Part 2, in the order they come ashore
    "ana": Islander("ana", "Ana", "fishes; sells at the market", "#F29E8E", 2),
    "bo": Islander("bo", "Bo", "buys fish; runs the ferry", "#9FB8F2", 2),
    "chidi": Islander("chidi", "Chidi", "gathers coconuts", "#C8E07A", 2),
    "dara": Islander("dara", "Dara", "buys; later keeps the books and the bank", "#D6A6F2", 2),
}

TRUTHS = {
    # Part 1: the technologies of the two first islanders (agora.crusoe)
    1: {
        "crusoe_alone": {"hours": 10.0, "a": 3.0, "alpha": 0.5, "b": 4.0, "beta": 0.5, "theta": 0.6},
        "two": {"hours_per_fish": (1.0, 2.0), "hours_per_coconut": (2.0, 2.5), "hours": (12.0, 12.0),
                "theta": 0.6},
        # the pit market of the opening chapter: ten buyers' values and ten sellers' costs, in dollars
        "pit": {"values": (3.40, 3.10, 2.90, 2.70, 2.50, 2.30, 2.10, 1.90, 1.70, 1.50),
                "costs": (1.20, 1.40, 1.60, 1.80, 2.00, 2.20, 2.40, 2.60, 2.80, 3.00),
                "viewer": 3},  # the card the film hands to you: the buyer with the 2.70 card
    },
    # Part 2: the village's fish market opens (the Tableau's goods pipe), and the pit is run again with a tax and
    # with price controls
    2: {
        # Each market day the village's 400 buyers draw their values for a fish afresh, uniform between 0 and the
        # choke price (so demand is the straight line Q = 400 (1 - p / 6)); the 400 boats' costs are fixed, uniform
        # between 0.50 and 5.00 (supply Q = 400 (p - 0.5) / 4.5).  A storm keeps a share of the boats ashore, at
        # random.  The day's catch is sold at the price that clears that day's cards (Agora's competitive outcome).
        "fish": {"buyers": 400, "boats": 400, "choke": 6.0, "lowest_cost": 0.5, "highest_cost": 5.0,
                 "days": 120, "storm_prob": 0.15, "storm_ashore": 0.35, "seed": 1890},
        # the Play-it market: Smith's worry that convergence was "an accident of symmetry"; a design in which the
        # sellers' surplus is far larger than the buyers' (nearly flat demand, steep supply)
        "lopsided": {"values": (2.60, 2.55, 2.50, 2.45, 2.40, 2.35, 2.30, 2.25, 2.20, 2.15),
                     "costs": (0.60, 0.85, 1.10, 1.35, 1.60, 1.85, 2.10, 2.35, 2.60, 2.85)},
        # two more asymmetric designs for the zero-intelligence test (Cliff and Bruten 1997)
        "flat_supply": {"values": (3.40, 3.10, 2.90, 2.70, 2.50, 2.30, 2.10, 1.90, 1.70, 1.50),
                        "costs": (2.00,) * 10},
        "flat_demand": {"values": (2.60,) * 10,
                        "costs": (1.20, 1.40, 1.60, 1.80, 2.00, 2.20, 2.40, 2.60, 2.80, 3.00)},
        # the wedges and controls applied to Part 1's pit
        "tax": 0.40, "cap": 2.00, "minimum": 2.60,
    },
    # Part 3: a year of the Island's national accounts (thousands of island dollars), as an input-output table
    # (agora.accounts.IOTable).  Four industries; the council taxes production and buys ferry trips and coconuts;
    # passing ships buy fish and coconuts and sell nets, nails, fuel and cloth.  Constructed so that output, income
    # and expenditure each give a GDP of 740, and households save 100 while the boats bought cost 120 (the rest is
    # borrowed from abroad: exports 120 against imports 140).
    3: {
        "accounts": {
            "industries": ("fishing", "coconut grove", "boatyard", "ferry"),
            # Z[i][j]: what industry j bought from industry i and used up
            "Z": ((0, 0, 0, 0),
                  (20, 0, 30, 0),     # coconut fibre for nets, coconut wood for hulls
                  (40, 0, 0, 25),     # boat repairs for the fishing company and the ferry
                  (15, 10, 5, 0)),    # carrying fish, coconuts and timber
            "final": {"C": (300, 200, 0, 60), "I": (0, 0, 120, 0), "G": (0, 10, 0, 20), "X": (80, 40, 0, 0)},
            "imports_used": (30, 0, 40, 20),       # nets, nails, fuel
            "imports_final": {"C": 50},            # cloth bought by households
            "wages": (160, 180, 70, 40), "profits": (95, 100, 35, 20), "taxes": (20, 10, 5, 5),
        },
        # what the accounts leave out (chapter 3): a year of the islanders' unpaid work, valued at the fishing wage
        "unpaid": {"cooking and cleaning": 120, "childcare": 70, "Crusoe's garden": 25, "mending nets at home": 15},
        # Bo's household (chapters 4-5): $100 a week, half on fish and half on coconuts (Cobb-Douglas tastes), in a
        # calm year and a stormy one; the storms come and go for twelve seasons in the chain-drift example
        "basket": {"income": 100.0, "shares": (0.5, 0.5), "calm": (2.0, 1.0), "storm": (4.0, 1.0), "seasons": 12},
        # the boatyard's boats (chapter 6): price = A * length^B * (1 + inflation)^year * noise; this year's boats
        # are longer, so the average price rises much more than the price of a boat of given length
        "boats": {"n": 30, "length": ((5.0, 0.6), (5.6, 0.6)), "A": 2.0, "B": 1.6, "inflation": 0.03,
                  "noise": 0.06, "seed": 1996},
        # Dara's labour survey (chapter 8): the Island's 100 adults, each in exactly one box
        "survey": {"employed full time or by choice part time": 58, "employed part time, wanting full time": 4,
                   "unemployed 15 weeks or more": 2, "unemployed, lost a job in the last 15 weeks": 3,
                   "discouraged": 2, "marginally attached, other reasons": 2, "not in the labour force": 29},
        # who gets the income (chapter 9): 40 households; wages (450) spread lognormally over 38 of them, profits
        # (250): 100 to Friday (the grove), 85 to Crusoe (the boatyard and half the fishing company), 65 in shares to
        # eight others; taxes (40) to the council
        "households": {"n": 40, "wage_sigma": 0.45, "friday": 100.0, "crusoe": 85.0, "small_owners": (8, 65.0),
                       "seed": 1934},
    },
    4: {
        # a season of the fish market (chapters 0-3): straight lines as in Part 2, but now both move.  Feast days
        # shift demand out by 70 fish at every price; storms shift supply in by 80; each day also has small shocks
        # to both.  The day's price and quantity are where the day's two lines cross.
        "season": {"days": 240, "a": 400.0, "b": 400.0 / 6, "c": -400.0 * 0.5 / 4.5, "d": 400.0 / 4.5,
                   "feast": (0.25, 70.0), "storm": (0.15, 80.0), "noise": (12.0, 12.0), "seed": 1927},
        # the Island's school records (chapter 5): 1,200 islanders; ability raises both schooling and wages; the
        # school built on the east side in year 20 adds schooling for those born near it, and nothing else
        "schooling": {"n": 1200, "base": 9.0, "ability_on_school": 1.5, "near_school": 2.0, "school_noise": 1.5,
                      "return": 0.08, "ability_on_wage": 0.10, "wage_noise": 0.35, "seed": 1991},
        # Lucas's islands (chapter 9): output rises only with surprise inflation, y = y* + b (pi - E pi) + e;
        # expectations adapt (E pi moves a share lam of the way to last year's inflation).  For 30 years the
        # council's inflation is noise around 2%; then it tries to keep output high with 8% a year
        "lucas": {"ystar": 100.0, "b": 0.8, "noise": 0.4, "lam": 0.5, "pi_calm": (2.0, 2.0), "pi_push": 8.0,
                  "years": (30, 20), "seed": 1976},
        # the apprenticeship (Part 4, chapter 8): a year with the boatwrights raises log earnings by 0.10.  Left to
        # choose, the islanders with the poorest prospects sign up (P = logistic(-select * ability)); a lottery
        # instead takes half at random.  Ability moves earnings by 0.25 per standard deviation and is never seen
        "apprentice": {"n": 1600, "effect": 0.10, "select": 1.4, "ability_on_wage": 0.25, "base": 2.0,
                       "wage_noise": 0.30, "seed": 2019},
        # the apprenticeship scaled up (Part 4, the frontier): 100 villages of 40 young islanders; each village's
        # share offered a place is drawn from 0, 25, 50, 75 or 100% (as Crepon et al. 2013 drew theirs).  A place
        # raises its holder's log earnings by 0.10; every apprentice in a village takes a little of the boatwrights'
        # work from the others, lowering everyone's log earnings by 0.08 times the village's share
        "villages": {"villages": 100, "per_village": 40, "saturations": (0.0, 0.25, 0.5, 0.75, 1.0), "direct": 0.10,
                     "spill": -0.08, "ability_on_wage": 0.25, "base": 2.0, "wage_noise": 0.30, "village_noise": 0.04,
                     "seed": 2013},
    },
    # Part 5: what the islanders want (agora.consumer)
    5: {
        # the eleven budget lines of Play it, as (most fish, most coconuts) each one affords, in the order shown;
        # chosen so that the lines cross often: a chooser who picks at random violates GARP on 97% of tries
        "budgets": {"lines": ((6, 6), (12, 3), (4, 9), (9, 4), (3, 12), (7, 5), (5, 7), (11, 4), (4, 8), (10, 6),
                              (6, 7))},
        # four islanders choose on the same lines: Bo (Cobb-Douglas, 60% on fish, with a small tremble), Ana (fish
        # and coconuts one for one, perfect complements), Chidi (perfect substitutes, a coconut worth 1.2 fish), and
        # Dara on a distracted day (a point at random on each line)
        "choosers": {"bo": {"kind": "cobb-douglas", "a": 0.6, "tremble": 0.12},
                     "ana": {"kind": "complements", "a": 1.0, "b": 1.0, "tremble": 0.0},
                     "chidi": {"kind": "substitutes", "a": 1.0, "b": 1.2, "tremble": 0.0},
                     "dara": {"kind": "random"}, "seed": 1938},
        # the money pump: a trader whose tastes go round in a circle (fish over coconut, coconut over cloth, cloth
        # over fish) pays a coconut-shell coin for each swap up the circle
        "pump": {"goods": ("fish", "coconut", "cloth"), "fee": 1, "rounds": 12},
        # the coconut seller's bulk price: $2 each for the first 6, $1 each after; fish cost $2; Bo's income varies
        "bulk": {"fish": 2.0, "first": 6, "price_first": 2.0, "price_after": 1.0},
        # a village of 4,000 earners facing the EITC's 2008 schedule for one child (Saez 2010, table 1):
        # potential earnings lognormal (median $12,000, sigma 0.6), quasilinear isoelastic effort cost; two
        # elasticities of reported earnings, 0 (wage earners) and 1 (the self-employed)
        "credit": {"people": 4000, "median": 12000.0, "sigma": 0.6, "elasticities": (0.0, 0.25, 1.0), "seed": 2010},
        # Becker's 2,000 islanders who split $12 between fish and coconuts at random, whatever the price
        "becker": {"people": 2000, "income": 12.0, "prices": (1.0, 1.5, 2.0, 3.0, 4.0, 6.0), "seed": 1962},
        # the ferry survey (chapter 12): 2,000 trips, each a choice between the slow ferry and a faster one that saves
        # 10, 20 or 30 minutes for an extra fare drawn between $0 and $15; travellers value time at $15 an hour, with
        # logistic taste shocks (scale: 0.5 per dollar)
        "ferry": {"trips": 2000, "saves": (10, 20, 30), "max_extra": 15.0, "value_of_time": 15.0, "scale": 0.5,
                  "seed": 1974},
    },
    # Part 6: when prices move (agora.demand)
    6: {
        # Bo again (Part 5's Cobb-Douglas, 60% of his $60 on fish): fish falls from $10 to $6, coconuts stay at $6
        "bo": {"a": 0.6, "income": 60.0, "fish": (10.0, 6.0), "coconut": 6.0},
        # the Island's poorest households must eat 14,000 calories a week (2,000 a day).  A coconut brings 1,400
        # calories, a fish 700 but far more taste; 12% of the budget goes on oil and greens (600 calories a dollar).
        # Taste is Stone-Geary with 3 coconuts committed and a sixth of the rest on coconuts.  Coconuts are 4 times
        # as many calories a dollar as fish at the prices below, so in the subsistence zone the planted price
        # elasticity of coconuts is r / (1 - r) = +0.43 (r = 0.30)
        "diet": {"coconut_kcal": 1400.0, "fish_kcal": 700.0, "need": 14000.0, "beta": 1 / 6, "s0": 3.0,
                 "other_share": 0.12, "other_kcal": 600.0},
        # Play it: a week's food money of $21, the two foods only; coconuts go from $1.20 to $1.50, fish stay at $2
        "playit": {"budget": 21.0, "coconut": (1.20, 1.50), "fish": 2.00},
        # the voucher experiment, on Jensen and Miller's design (2008): 1,300 households in 11 villages, a control
        # group and vouchers worth 10, 20 or 30 cents off a $1.20 coconut, three survey rounds; weekly food money
        # lognormal (median $17, sigma 0.3), calorie needs vary by 10%, consumption reported with 12% error
        "vouchers": {"households": 1300, "villages": 11, "cuts": (0.10, 0.20, 0.30), "coconut": 1.20, "fish": 2.00,
                     "median": 17.0, "sigma": 0.3, "need_sd": 0.10, "report_sd": 0.12, "income_sd": 0.05,
                     "seed": 2006},
        # the household survey (chapter 10): 20 villages x 12 months of prices, 25 households a cell, spending on
        # fish, coconuts and cloth from a planted AIDS (alpha0 = log 300, the median monthly spending)
        "survey": {"goods": ("fish", "coconuts", "cloth"), "alpha": (0.35, 0.40, 0.25), "beta": (-0.04, -0.08, 0.12),
                   "gamma": ((-0.0525, -0.0075, 0.06), (-0.0075, 0.08, -0.0725), (0.06, -0.0725, 0.0125)),
                   "median": 300.0, "villages": 20, "months": 12, "per_cell": 25, "price_sd": 0.15, "m_sigma": 0.5,
                   "share_sd": 0.03, "seed": 1980},
        # a tax on coconuts (chapter 8): weekly demand x = -4 p + 0.1 m + 6 at $1.20 and $60 a week
        "tax": {"alpha": -4.0, "delta": 0.1, "c": 6.0, "price": 1.20, "income": 60.0, "taxes": (0.30, 0.60, 0.90)},
        # integrability (chapter 6): budget shares w = alpha + gamma log p over fish, coconuts and cloth, one gamma
        # symmetric and one that goes round in a circle; a loop of radius 0.4 in log prices
        "loop": {"alpha": (0.40, 0.35, 0.25),
                 "symmetric": ((-0.10, 0.05, 0.05), (0.05, -0.10, 0.05), (0.05, 0.05, -0.10)),
                 "circular": ((-0.10, 0.08, 0.02), (0.02, -0.10, 0.08), (0.08, 0.02, -0.10)), "radius": 0.4},
        # Hamilton's method on the Island (chapter 7): six surveys four years apart, 1,500 households each; food's
        # share w = 0.60 - 0.10 log(real income / 300) + 0.05 log(food's relative price) + noise; real income grows
        # 1.5% a year; food's relative price differs across 10 regions and years; the official price index
        # overstates the rise in the cost of living by 1% a year
        "hamilton": {"years": (0, 4, 8, 12, 16, 20), "households": 1500, "regions": 10, "median": 300.0,
                     "sigma": 0.5, "growth": 0.015, "bias": 0.010, "a": 0.60, "b": -0.10, "g": 0.05, "noise": 0.04,
                     "food_price_sd": 0.08, "seed": 2001},
    },
    7: {
        # the St Petersburg game as Bernoulli posed it (1738): $1 for heads on the first toss, doubling after; a million
        # simulated games, and the prices Bernoulli's log utility puts on it at three levels of wealth
        "stpete": {"first": 1.0, "games": 1_000_000, "seed": 1738, "wealths": (100.0, 1000.0, 1_000_000.0)},
        # Fisher's two periods (chapter 1): Chidi's harvest is worth $120 this season and $40 the next (the dry
        # season); Dara lends and borrows at 10% a season; Chidi's utility is CRRA with gamma 2 (an EIS of 1/2) and
        # beta 0.9.  The comparison choosers have EIS 2, 1/2 and 1/8
        "chidi": {"income": (120.0, 40.0), "rate": 0.10, "rates": (0.0, 0.10, 0.20, 0.30, 0.40), "beta": 0.90,
                  "gamma": 2.0, "gammas": (0.5, 2.0, 8.0)},
        # discounting (chapter 2): $100 thirty years away at 3% and at 10%
        "discount": {"rates": (0.03, 0.10), "years": 30, "prize": 100.0},
        # risk aversion (chapter 5): Ana has $40 and a day's fishing: the reef pays $60 for sure, the open sea $20 or
        # $140, 50-50
        "ana": {"wealth": 40.0, "reef": 60.0, "sea": (20.0, 140.0), "gammas": (0.0, 1.0, 2.0, 4.0)},
        # insurance (chapter 6): Ana's wealth is $300, $150 of it her boat; a storm wrecks it with chance 10%; cover
        # sold at the expected payout times 1 + loading; her gamma is 2
        "boat": {"wealth": 300.0, "boat": 150.0, "storm": 0.10, "loadings": (0.0, 0.2, 0.5), "gamma": 2.0},
        # deductibles at an American household's scale (illustrative): wealth $100,000, a claim in 5% of years,
        # deductibles of $500 or $1,000, the lower one costing $30, $50 or $100 a year more (its expected saving is
        # $25)
        "deductible": {"wealth": 100_000.0, "claim": 0.05, "deductibles": (500.0, 1000.0),
                       "extra": (30.0, 50.0, 100.0)},
        # the risky asset (chapter 6): Dara's venture returns 8% on average, 28% or -12% with equal chance (sd 20%),
        # against a safe 2%
        "venture": {"safe": 0.02, "outcomes": (1.28, 0.88), "gammas": (1.0, 2.0, 4.0, 10.0)},
        # stochastic dominance (chapter 7): three nets' daily catches (fish, with chances)
        "nets": {"old": ((2, 6, 10), (0.25, 0.5, 0.25)), "better": ((4, 6, 10), (0.25, 0.5, 0.25)),
                 "spread": ((0, 6, 12), (0.25, 0.5, 0.25))},
        # fanning out (chapter 8): Chew's weighted utility on $0, $1M, $5M with u = (0, 0.85, 1) and weights
        # (6, 1, 2), illustrative values that produce Allais's pattern
        "fanning": {"u": (0.0, 0.85, 1.0), "w": (6.0, 1.0, 2.0)},
        # Epstein-Zin (chapter 10): consumption 1 today and next season, then 0.8 or 1.2 with equal chance, learnt
        # next season or only when it comes; beta 0.95; Bansal and Yaron's calibration (gamma 10, psi 1.5) against
        # expected utility with gamma 2
        "ez": {"c": (1.0, 1.0), "c2": (0.8, 1.2), "beta": 0.95, "calibrations": ((10.0, 1.5), (2.0, 0.5),
                                                                              (5.0, 0.5), (0.5, 0.5))},
        # present bias (chapter 11): Chidi's dry-season store of 300 coconuts, to last six weeks; beta 0.7, delta 1
        "present": {"store": 300.0, "weeks": 6, "beta": 0.7, "delta": 1.0},
        # Holt and Laury's menu run on 400 islanders (chapter 12): CRRA gammas drawn normal (mean 0.35, sd 0.35),
        # choices noisy, logit in certainty-equivalent dollars with scale $0.20
        "hl": {"people": 400, "gamma_mean": 0.35, "gamma_sd": 0.35, "noise": 0.20, "seed": 2002},
    },
    8: {
        # Crusoe's boatyard: boats a month from slipways K and shipwrights L, q = 2 K^0.25 L^0.5 (decreasing returns,
        # 0.75); a shipwright costs $1,000 a month, a slipway $400; a boat sells for $1,200
        "yard": {"A": 2.0, "a": 0.25, "b": 0.5, "wage": 1000.0, "rent": 400.0, "price": 1200.0, "slipways": 4.0},
        # the technologies compared in chapter 2: CES with capital's weight 0.3 and sigma 0 (Leontief) to infinity
        "techs": {"share": 0.3, "sigmas": (0.0, 0.5, 1.0, 2.0)},
        # an industry of boatyards (chapter 8): each with total cost F + c q + d q^2 a month; boats demanded
        # Q = 400 - 0.2 p; with free entry and identical yards, and with fixed costs spread over $2,000-$8,000
        "industry": {"F": 4000.0, "c": 200.0, "d": 50.0, "demand": (400.0, 0.2), "fixed_range": (2000.0, 8000.0),
                     "entrants": 200},
        # rules of thumb under selection (chapter 9): 200 yards price at cost times (1 + markup), markups drawn
        # uniform 0-100%; each faces demand with elasticity -3, so the profit-maximizing markup is 50%; a yard whose
        # profit falls below zero three months running closes and is replaced by a copy of a survivor, slightly
        # varied
        "selection": {"yards": 200, "months": 120, "elasticity": -3.0, "noise": 0.15, "mutation": 0.03,
                      "seed": 1950},
        # hold-up (chapter 11): a body maker's specific investment i is worth 2 V sqrt(i) to the car maker, V = 10;
        # at arm's length it gets half the surplus after investing
        "holdup": {"V": 10.0, "theta": 0.5},
        # Grossman-Hart-Moore (chapter 12): A's investment matters four times as much as B's; the asset's owner keeps
        # 80% of its own investment's value outside the relationship
        "ghm": {"va": 4.0, "vb": 1.0, "outside": 0.8},
    },
    9: {
        # the box (chapters 1-5): Ana has 8 fish and 1.5 bundles of coconuts, Bo 2 fish and 8.5; Cobb-Douglas
        # tastes, Ana spending 40% on fish, Bo 60%; replicated 1, 2, 3, 5, 10 and 20 times for the core
        "box": {"ana": {"a": 0.4, "e": (8.0, 1.5)}, "bo": {"a": 0.6, "e": (2.0, 8.5)},
                "replicas": (1, 2, 3, 5, 10, 20)},
        # the second welfare theorem (chapter 6): the efficient allocation that gives Ana 5 fish
        "target_fish": 5.0,
        # three goods (chapters 8-9): Ana owns 2 fish, Bo 1 bundle of coconuts, Friday 1.5 cords of timber, each
        # with Cobb-Douglas weights on (fish, coconuts, timber)
        "three": {"traders": (("Ana", (0.5, 0.3, 0.2), (2.0, 0.0, 0.0)), ("Bo", (0.1, 0.6, 0.3), (0.0, 1.0, 0.0)),
                              ("Friday", (0.3, 0.2, 0.5), (0.0, 0.0, 1.5))),
                  "grids": (6, 12, 48), "starts": ((0.8, 0.15, 0.4), (0.2, 0.9, 0.2), (0.3, 0.3, 0.85))},
        # Scarf's economy (chapter 9): the auctioneer starts from these prices
        "scarf_start": (0.22, 0.85, 0.5),
        # the whole Island cleared at once (chapter 10): 5 goods, 12 islanders, CES tastes (elasticities 0.5-2),
        # endowments and weights drawn with this seed
        "island": {"goods": ("fish", "coconuts", "timber", "cloth", "salt"), "people": 12, "seed": 1954,
                   "sigma": (0.5, 2.0)},
        # Crusoe as consumer, worker and firm (chapter 11): 12 hours a day, coconuts c = 2 L^0.5, utility
        # 0.6 log c + 0.4 log leisure
        "crusoe": {"A": 2.0, "alpha": 0.5, "hours": 12.0, "b": 0.6},
        # time and uncertainty (chapter 13): Ana fishes (80 in calm weather, 20 in a storm), Chidi gathers coconuts
        # (storms bring them down: 20 calm, 80 storm); 50 each today; even odds; patience 0.95; risk aversion 2
        "risk": {"e0": (50.0, 50.0), "E": ((80.0, 20.0), (20.0, 80.0)), "probs": (0.5, 0.5), "beta": 0.95,
                 "gamma": (2.0, 2.0)},
        # the planner (chapter 14): four of the yard's machines make planks and masts at these rates a day; a
        # boat's set is 2 planks and 1 mast
        "plan": {"machines": ("saw", "adze", "lathe", "press"), "parts": ("planks", "masts"),
                 "rates": ((6.0, 1.0), (4.0, 2.0), (2.0, 2.0), (1.0, 3.0)), "kit": (2.0, 1.0)},
        # misallocation (chapter 15): 100,000 plants, productivity spread 0.2 in logs, revenue productivity spread
        # as in Hsieh and Klenow's United States (1997) and China (2005)
        "plants": {"n": 100_000, "sd_A": 0.2, "seed": 2009},
        # the housing market (chapter 17): six islanders, each with a hut, rank the huts
        "huts": {"names": ("Ana", "Bo", "Chidi", "Dara", "Crusoe", "Friday"),
                 "prefs": ((2, 3, 0, 1, 4, 5), (0, 2, 1, 3, 5, 4), (1, 0, 2, 4, 3, 5), (0, 4, 3, 2, 1, 5),
                           (2, 3, 4, 0, 5, 1), (3, 0, 5, 1, 2, 4))},
    },
    10: {
        # Bo's ferry (chapters 1-3): a hundred islanders who would cross, each with a value of the crossing drawn
        # uniform on $0-$10; an extra passenger costs Bo nothing; the fares of Play it
        "ferry": {"people": 100, "top": 10.0, "seed": 1844, "fares": (2.0, 4.0, 5.0, 6.0, 8.0)},
        # the same market as a demand curve: crossings a day Q = 100 - 10 p, marginal cost c (for pass-through)
        "demand": {"a": 100.0, "b": 10.0, "c": 2.0, "eps": 3.0},
        # third degree (chapter 5): students (Q = 60 - 10 p) and townsfolk (Q = 100 - 5 p); a crossing costs $1
        "groups": {"students": (60.0, 10.0), "town": (100.0, 5.0), "c": 1.0},
        # second degree (chapter 6): deck and cabin; a share 0.3 of passengers value comfort at 2 per unit, the
        # rest at 1; comfort q costs q^2 / 2 to provide
        "screen": {"lo": 1.0, "hi": 2.0, "share_hi": 0.3},
        # two-part tariffs (chapter 7): Oi's park on the Island, rides demanded 10 - p by two visitors in three and
        # 16 - p by the keen third; a ride costs $2
        "rides": {"small": (10.0, 1.0), "big": (16.0, 1.0), "mix": (2, 1), "c": 2.0},
        # bundling (chapter 8): 400 visitors' values for the crossing and the reef tour, negatively and positively
        # correlated
        "bundle": {"people": 400, "top": 10.0, "noise": 0.5, "seed": 1976},
        # a durable good (chapter 9): Crusoe's boats; buyers' values uniform on [0, 1] (in thousands); the market
        # discounts at 10% a year; a thirty-year horizon; price changes 1, 4, 12, 52 and 365 times a year
        "durable": {"r": 0.10, "years": 30, "per_year": (1, 4, 12, 52, 365)},
        # natural monopoly (chapter 10): the Island's waterworks sells to households (elasticity 1.5) and boatyards
        # (4), marginal cost 1, and must cover a fixed cost of 40
        "ramsey": {"A": (100.0, 100.0), "eps": (1.5, 4.0), "c": (1.0, 1.0), "F": 40.0},
        # regulation (chapter 11): the waterworks, q = 2 K^0.3 L^0.4 at price 10, wage 1, cost of capital 1, an
        # allowed return of 1.4
        "aj": {"A": 2.0, "a": 0.3, "b": 0.4, "p": 10.0, "w": 1.0, "r": 1.0, "s": 1.4},
        # monopsony (chapter 12): Crusoe's yard as the only employer: labour supply w = 5 + 0.1 L, each shipwright
        # adds $25 a day, and a minimum wage of $18
        "monopsony": {"w0": 5.0, "slope": 0.1, "mrp": 25.0, "min_wage": 18.0},
    },
    11: {
        # the guessing game (chapters 1, 2, 12): two-thirds of the average, 0-100; an Island crowd of 67 (the size of
        # Nagel's four 2/3 sessions) drawn from the cognitive hierarchy, with each level's choice blurred by noise
        "guess": {"p": 2 / 3, "crowd": 67, "noise": 6.0, "seed": 1995},
        # the prisoner's dilemma with Axelrod's payoffs (chapters 0, 8, 9): temptation, reward, punishment, sucker
        "pd": {"T": 5.0, "R": 3.0, "P": 1.0, "S": 0.0},
        # the grammar of 2x2 games (chapter 4): row payoff, column payoff for each cell (row strategy first)
        "grammar": {
            "coordination": ((2, 2), (0, 0), (0, 0), (1, 1)),     # both use the harbour's east or west quay
            "battle": ((2, 1), (0, 0), (0, 0), (1, 2)),           # Ana prefers the regatta, Bo the market
            "chicken": ((0, 0), (7, 2), (2, 7), (6, 6)),          # dare, chicken; Aumann's (1974) numbers
            "stag": ((4, 4), (0, 3), (3, 0), (3, 3)),             # hunt the stag together, or a hare alone
        },
        # mixed strategies (chapter 5): a penalty kick; the kicker's chance of scoring by (kick, dive), left first
        "penalty": {"score": ((0.58, 0.95), (0.93, 0.70))},
        # extensive form (chapter 6): Dara's boatyard considers entering Crusoe's trade; payoffs (entrant, incumbent)
        "entry": {"fight": (-1, -1), "accommodate": (1, 1), "stay_out": (0, 4)},
        # the centipede (chapter 7): McKelvey and Palfrey's four-move game, 0.40 and 0.10 doubling each move
        "centipede": {"moves": 4, "start": (0.4, 0.1), "grow": 2.0},
        # repeated games (chapter 8): discount factors to show
        "repeated": {"deltas": (0.3, 0.5, 0.7, 0.9)},
        # Axelrod's tournament (chapter 9): the field, 200 rounds a match, five repeats, and a noisy rerun
        "tournament": {"field": ("ALLC", "ALLD", "TFT", "GRIM", "TF2T", "WSLS", "GTFT", "RANDOM", "JOSS"),
                       "rounds": 200, "repeats": 5, "noise": 0.05, "seed": 1980},
        # evolution (chapter 11): hawk and dove with a prize of 2 and a cost of fighting of 4
        "hawkdove": {"V": 2.0, "C": 4.0},
        # incomplete information (chapter 13): Ana is tough with probability 0.3; if Bo enters her fishing ground,
        # a tough Ana fights and a weak one shares, and fighting an empty sea wastes effort; payoffs ((Ana fights,
        # shares) x (Bo enters, stays out))
        "bayes": {"prior_tough": 0.3,
                  "tough": ((3, 1.5), (1, 2)), "weak": ((0, 1), (1, 2)),
                  "bo_vs_tough": ((-2, 0), (2, 0)), "bo_vs_weak": ((-2, 0), (2, 0))},
        # bargaining (chapter 15): Rubinstein's alternating offers, patience 0.9 a round
        "bargain": {"delta": 0.9},
    },
    12: {
        # the boat market (chapters 1-3, 7, 11): Crusoe's yard and Dara's, inverse demand P = 100 - Q boats a year,
        # each boat costs 10 to build
        "boats": {"a": 100.0, "b": 1.0, "c": 10.0, "n_max": 20},
        # Play it (chapter 3): Crusoe asks $40 for a boat repair that costs either yard $10; the fares on offer
        "playit": {"rival": 40.0, "cost": 10.0, "prices": (45.0, 40.0, 39.0, 25.0, 10.0)},
        # differentiated boats (chapter 4): q_i = 90 - 2 p_i + p_j, cost 10
        "diff": {"alpha": 90.0, "beta": 2.0, "gamma": 1.0, "c": 10.0},
        # the beach (chapter 5): ice sellers on a line of length 1, transport cost 1; the coast as a circle with an
        # entry cost of 0.01
        "beach": {"t": 1.0, "c": 0.0, "F": 0.01},
        # monopolistic competition (chapter 6): elasticity of substitution 4, fixed cost 1, marginal cost 1, 100
        # workers
        "variety": {"sigma": 4.0, "f": 1.0, "c": 1.0, "L": 100.0},
        # entry deterrence (chapter 7): a boat's capacity costs 30 to build, running it 10 more; the entrant's fixed
        # cost 144 (it deters at 36 boats, a profit of 864 against 450 from sharing)
        "deter": {"a": 100.0, "b": 1.0, "c": 10.0, "r": 30.0, "F": 144.0},
        # collusion (chapters 8-9): numbers of firms; Green and Porter's price wars
        "collusion": {"ns": (2, 3, 4, 5, 6, 8, 10), "periods": 300, "seed": 1984},
        # leniency (chapter 9): a fine of 100, a 20% chance the authorities find the cartel unaided
        "leniency": {"fine": 100.0, "caught": 0.2},
        # mergers (chapter 11): three symmetric Cournot yards; Williamson's trade-off with demand elasticity 2
        "merger": {"n": 3, "eps": 2.0, "dp": 0.10},
        # common ownership (chapter 15): two airlines with half the market each; four funds own 7% of each, and the
        # rest of each airline is held either by one owner or by a thousand small ones
        "common": {"shares": (0.5, 0.5), "funds": 4, "stake": 0.07, "small": 1000},
    },
    13: {
        # used boats (chapters 1-2): a boat's quality, what it is worth to its owner, is uniform from $0 to $100; any
        # buyer values it at that plus $30; Play it's offers
        "boats": {"lo": 0.0, "hi": 100.0, "premium": 30.0, "offers": (80.0, 60.0, 40.0, 30.0, 20.0)},
        # a guarantee (chapter 3): good boats worth $90, bad $30, half good; a repair costs $100; a good boat breaks
        # with chance 0.1, a bad one with 0.7
        "warranty": {"good": 90.0, "bad": 30.0, "share_good": 0.5, "fix": 100.0, "break_good": 0.1,
                     "break_bad": 0.7},
        # signalling (chapter 4): fishers of two kinds, landing 1 or 2 baskets a day; a season of schooling costs a
        # weak fisher 1 basket a day and a strong one 0.5; half are strong
        "spence": {"theta_low": 1.0, "theta_high": 2.0, "cost_low": 1.0, "cost_high": 0.5, "share_high": 0.5},
        # screening (chapter 6): wealth 100, a storm that costs 60; careful boat owners lose with chance 0.1,
        # careless ones with 0.4; 30% are careless
        "screen": {"W": 100.0, "d": 60.0, "p_low": 0.1, "p_high": 0.4, "share_high": 0.3},
        # the death spiral (chapter 7)
        "spiral": {"n": 20000, "years": 5, "mean_extra": 300.0, "sd": 1.4, "value_mult": 1.5, "taste_mean": -600.0,
                   "taste_sd": 800.0, "base_charge": 450.0, "seed": 1995},
        # testing for private information (chapter 9): simulated drivers
        "drivers": {"n": 20000, "seed": 2000},
        # credit (chapter 10): two kinds of borrower and the bank's cost of chasing a failed loan
        "credit": {"s_safe": 0.9, "y_safe": 160.0, "s_risky": 0.5, "y_risky": 130.0, "share_safe": 0.5,
                   "collection_cost": 60.0},
        # reputation (chapter 12): a new seller, honest with prior 0.6; honest sales go well 95% of the time, a
        # cheat's 60%; three good reviews, one bad, then twelve good
        "reputation": {"prior": 0.6, "honest_good": 0.95, "cheat_good": 0.6, "value_honest": 100.0,
                       "value_cheat": 40.0, "feedback": (1,) * 3 + (0,) + (1,) * 12},
    },
    14: {
        # the team (chapter 1): eighteen households sharing a commune's harvest equally; effort cost c e^2/2, output a
        # per unit of effort
        "team": {"ns": (1, 2, 3, 6, 10, 18), "a": 1.0, "c": 1.0},
        # Play it (chapter 1): Crusoe hires Friday for the grove; a day's harvest is Friday's effort plus luck (sd 5
        # baskets); Friday is risk averse (CARA, r = 0.2 a basket) and effort e costs 0.1 e^2 / 2 baskets; the shares
        # Crusoe can offer, the fixed pay set so that Friday just accepts
        "playit": {"r": 0.2, "c": 0.1, "sigma": 5.0, "shares": (0.0, 1 / 3, 2 / 3, 1.0)},
        # the discrete model (chapter 3): hard work makes a good harvest (100) likelier, 0.8 against 0.4 (else 40);
        # it costs 0.3 utils; Friday's other work is worth 2 utils; log utility
        "discrete": {"p_high": 0.8, "p_low": 0.4, "y_high": 100.0, "y_low": 40.0, "cost": 0.3, "reservation": 2.0},
        # the trade-off (chapter 4): noise and risk aversion
        "tradeoff": {"sigmas": (0.0, 10.0), "rs": (0.05, 0.2, 0.8), "c": 0.1},
        # informativeness (chapter 5): a common shock (the weather on the whole island) and Friday's own luck
        "rpe": {"r": 0.2, "c": 0.1, "common": 4.0, "own": 3.0},
        # multitask (chapter 7): two tasks, half-substitutes in effort, pride worth 1 a unit on each
        "multitask": {"s": 0.5, "c": 1.0, "base": 1.0},
        # tournaments (chapter 8): prize spreads, noise sd 1
        "tournament": {"spreads": (0.0, 4.0), "sigma": 1.0, "c": 1.0},
        # the ratchet (chapter 9)
        "ratchet": {"delta": 0.9, "bonus": 1.0, "c": 1.0},
        # Holmström's career concerns: ability's variance a quarter of a year's noise; a thirty-year career
        "careers": {"years": 30, "var_ability": 0.25, "var_noise": 1.0, "c": 1.0, "delta": 0.9, "rc_sigma2": 0.5},
        # a relational bonus for Friday, at the Play it's cost of effort
        "relational": {"c": 0.1},
        # efficiency wages (chapter 10)
        "shirking": {"effort_cost": 1.0, "detect": 0.5, "quit_rate": 0.1, "discount": 0.05, "labour": 100.0,
                     "demand_a": 6.0, "demand_b": 0.04},
        # sharecropping (chapter 11): output 10 per unit of effort, noise sd 8, risk aversion 1
        "sharecrop": {"a": 10.0, "c": 1.0, "r": 1.0, "sigma": 8.0},
    },
    15: {
        # Play it (chapter 1): four islanders, twenty shells each; the pot is multiplied by 1.6 and shared (MPCR 0.4)
        "playit": {"n": 4, "endowment": 20.0, "mpcr": 0.4, "gives": (0, 5, 10, 20)},
        # the smoke of Dara's kiln (chapters 2-3): demand for pots, private cost, and the damage to the village
        "kiln": {"a": 100.0, "b": 1.0, "c": 10.0, "e": 1.0, "d": 0.5},
        # Coase's cattle (chapter 4): what each steer is worth to the cattle-raiser (Agora's numbers; Coase gives none)
        "coase": {"values": (5.0, 4.0, 1.5, -1.0), "transaction_costs": (0.0, 1.0, 2.0)},
        # a lighthouse for the island (chapter 6): four ship-owners' values theta ln(1 + G), a unit cost of 1
        "lighthouse": {"thetas": (4.0, 3.0, 2.0, 1.0), "mc": 1.0},
        # typed players (chapter 7): groups of four, ten rounds
        "vcm": {"groups": 400, "rounds": 10, "n": 4, "endowment": 20.0, "mpcr": 0.4, "seed": 2000},
        # the lagoon's fish (chapter 8)
        "fishery": {"K": 1.0, "r": 0.5, "q": 0.01, "p": 100.0, "c": 0.3},
        # prices or quantities (chapter 10): flat benefits and steep costs, then the reverse
        "weitzman": {"cases": ((0.5, 2.0), (2.0, 0.5)), "sigma": 1.0},
        # standards and lock-in (chapter 12): Arthur's adopters
        "lockin": {"runs": 12, "adopters": 800, "taste": 1.0, "network": 0.1, "seed": 1989},
        # the causeway into town (chapter 11)
        "bottleneck": {"N": 6000.0, "s": 4000.0, "alpha": 20.0, "beta": 10.0, "gamma": 40.0, "t_star": 9.0},
    },
    16: {
        # Play it (chapter 1): Crusoe's old canoe; you value it at 70 shells; three rivals' values uniform on 0-100
        "playit": {"value": 70.0, "rivals": 3, "top": 100.0},
        # the auction house (chapters 2-5): four bidders, values uniform on [0, 1] (in hundreds of shells)
        "formats": {"n": 4, "draws": 60000, "seed": 1961},
        # one sale run on the clocks (chapter 2): four islanders' values for the canoe, in shells
        "clock": {"values": (31.0, 84.0, 57.0, 72.0), "names": ("ana", "bo", "dara", "friday")},
        # Myerson (chapter 7): two bidders, and Bulow and Klemperer's extra one
        "myerson": {"n": 2},
        # risk aversion (chapter 6): utility x^alpha
        "risk": {"alpha": 0.5},
        # the jar (chapter 8): a common value of 10 shells, each bidder's estimate within 3 of it
        "curse": {"ns": (2, 4, 8, 16, 32), "value": 10.0, "noise": 3.0, "seed": 1971},
        # the fishing rights (chapter 9): a national bidder and two locals
        "exposure": {"both": 10.0, "alone": 1.0, "rivals": ((4.0, 4.0), (2.0, 9.0))},
        # the island's notice board (chapter 11): four advertisers, three slots
        "gsp": {"values": (10.0, 8.0, 6.0, 4.0), "ctrs": (200.0, 120.0, 60.0)},
        # the harbour's bonds (chapter 12): two bonds; a big buyer wants both, a small one wants one
        "bonds": {"supply": 2, "big": (10.0, 10.0), "small": 6.0},
    },
    17: {
        # Play it (chapter 1): four children, three workshops' places; one lottery breaks every tie
        "playit": {"students": {"you": ("boatyard", "kiln", "loft"), "ana": ("boatyard", "kiln", "loft"),
                                "bo": ("loft", "kiln", "boatyard"), "dara": ("kiln", "boatyard", "loft")},
                   "lottery": ("ana", "bo", "you", "dara"), "capacity": {"boatyard": 1, "kiln": 1, "loft": 2}},
        # the apprentices' board (chapters 5-6): four apprentices, four workshops (found by search: six rounds, three
        # stable matchings)
        "board": {"apprentices": {"ana": ("boatyard", "kiln", "loft", "grove"), "bo": ("kiln", "grove", "boatyard", "loft"),
                                  "chidi": ("loft", "boatyard", "kiln", "grove"),
                                  "dara": ("boatyard", "kiln", "grove", "loft")},
                  "workshops": {"boatyard": ("bo", "dara", "ana", "chidi"), "grove": ("ana", "dara", "chidi", "bo"),
                                "kiln": ("chidi", "dara", "bo", "ana"), "loft": ("bo", "dara", "ana", "chidi")}},
        # a footbridge (chapter 3): four islanders' values, a cost shared equally
        "bridge": {"values": (60.0, 10.0, 10.0, 40.0), "cost": 100.0},
        # two boats and two buyers (chapter 11): what each pair creates together
        "assignment": {"values": ((5.0, 8.0), (7.0, 9.0))},
        # huts (chapter 9): each islander's ranking of the four huts, named by owner
        "huts": {"ana": ("bo", "chidi", "ana", "dara"), "bo": ("ana", "dara", "bo", "chidi"),
                 "chidi": ("dara", "ana", "chidi", "bo"), "dara": ("ana", "chidi", "dara", "bo")},
        # the kidney pool (chapter 9): which pair's donor can give to which pair's patient (found by search)
        "kidneys": {"compat": {"P1": ("P6", "P7"), "P2": (), "P3": ("P2", "P6"), "P4": ("P5",), "P5": ("P3", "P6"),
                               "P6": ("P1", "P4"), "P7": ("P8",), "P8": ("P1", "P2")},
                    "altruists": {"altruist": ("P1", "P3")}, "max_cycle": 3, "max_chain": 5},
        # what a lottery reveals (chapter 12): one oversubscribed school
        "lottery": {"students": 20000, "effect": 0.4, "seats": 3000, "sibling_share": 0.25, "always_takers": 0.3,
                    "seed": 2017, "reps": 200},
    },
    18: {
        # Play it (chapter 1): 38 islanders rank five plans for the harvest feast (found by search: five rules, five
        # winners, no ties)
        "playit": {"profile": ((12, ("A", "E", "D", "B", "C")), (11, ("B", "D", "E", "C", "A")),
                               (8, ("C", "E", "D", "B", "A")), (7, ("D", "C", "B", "E", "A")))},
        # the median voter (chapter 4): five islanders' ideal sizes for the new granary, on a line
        "peaks": {"peaks": (1.0, 2.0, 3.0, 7.0, 9.0), "options": tuple(float(x) for x in range(1, 10))},
        # Arrow's pivot (chapter 3): five voters, a dictator at the third
        "arrow": {"n_voters": 5, "dictator": 2},
        # welfare (chapters 7-8): five islanders' incomes, and two societies behind the veil
        "incomes": (5.0, 10.0, 20.0, 40.0, 80.0),
        "veil": {"A": (20.0, 20.0, 20.0, 20.0, 20.0), "B": (8.0, 30.0, 30.0, 30.0, 30.0)},
        # the value of a statistical life (chapter 11): a job with more risk, and the pay that goes with it
        "vsl": {"extra_risk": 1e-4, "extra_pay": 1000.0},
        # discounting (chapter 12): a benefit 100 years away, at three rates
        "discount": {"years": 100, "amount": 1e6, "rates": (0.014, 0.03, 0.045)},
    },
    19: {
        # Play it (chapter 1): five candidate years for the start of England's climb in income per head
        "playit": {"options": (1350, 1500, 1650, 1800, 1900)},
        # the Malthusian island (chapters 2-4): income per head A (X / L)^beta, population growing at
        # lam ln(y / ybar); a plague in year 100 kills 45% (England lost about that share, 1348-51); a better
        # plough in year 250 raises A by half
        "malthus": {"beta": 0.6, "lam": 0.02, "ybar": 1.0, "years": 400, "plague": (100, 0.45),
                    "invention": (250, 0.5)},
        # England's labour demand curve (chapter 3): the spans fitted
        "elasticity": {"before": (1270, 1640), "after": (1600, 1800)},
        # unified growth (chapter 9): one generation per step from the year 1000
        "unified": {"phi": 0.065, "generations": 42},
        # persistence and spatial noise (chapter 13): 300 places, two independent smooth fields
        "noise": {"n_sites": 300, "length": 0.25, "reps": 400},
    },
    20: {
        # the island gets capital (chapters 3-5, 11): boats, nets and granaries; capital's share alpha, population
        # growth n, technology growth g, depreciation delta, all a year
        "solow": {"alpha": 1 / 3, "n": 0.01, "g": 0.02, "delta": 0.05, "s0": 0.15},
        # Play it (chapter 4): five saving rates to choose for a century; and a jump from 15% to 30% in year 10
        "playit": {"options": (0.10, 0.20, 0.33, 0.50, 0.70), "years": 100, "jump": (10, 0.15, 0.30)},
        # Ramsey (chapter 11): patience rho and the curvature theta
        "ramsey": {"rho": 0.03, "theta": 2.0, "k0_share": 0.5},
        # the cross-country work (chapters 6, 9, 10): spans and the share alpha
        "convergence": {"spans": ((1960, 1990), (1960, 2019), (2000, 2019)), "gd": 0.05, "min_pop": 1.0},
        "development": {"year": 2019, "alpha": 1 / 3},
        "lucas": {"poor": "IND", "rich": "USA", "year": 2019, "alpha": 0.4},
    },
    21: {
        # Play it (chapter 1): hours of work for 1,000 lumen-hours in 1992, given 5.37 in 1800 (Nordhaus)
        "playit": {"options": (1.0, 0.1, 0.01, 0.001, 0.0001)},
        # Romer's economy (chapter 4): idea productivity delta, the markup's alpha, patience and curvature
        "romer": {"L": 1.0, "delta": 0.10, "alpha": 0.5, "rho": 0.02, "theta": 1.0, "sizes": (0.5, 1.0, 1.5, 2.0)},
        # Aghion and Howitt's ladder (chapter 5)
        "ah": {"lam": 0.1, "alpha": 0.6, "rho": 0.05, "L": 1.0, "gamma": 1.5, "n": 0.25, "years": 120, "sectors": 200,
               "seed": 21},
        # semi-endogenous growth (chapter 6): researchers grow 4.3% a year; beta = 1 - phi = 3
        "semi": {"lam": 1.0, "phi": -2.0, "n": 0.043, "theta": 0.05, "years": 200},
        # the Island's plants (chapter 8): physical productivity and wedges, two economies
        "plants": {"n": 4000, "sd_logA": 0.6, "sd_wedge": (0.35, 0.65), "sigma": 3.0, "seed": 21},
        # directed technical change (chapter 12)
        "directed": {"sigmas": (1.4, 3.0)},
    },
    # Part 22: households get a horizon.  The named cast now sits inside a population of 10,000 households
    22: {
        # Play it (chapter 1): a windfall of a month's income; what share is spent within the quarter?
        "playit": {"options": (0.02, 0.25, 0.50, 0.90)},
        # the population (chapters 2, 8): log permanent income N(0, 0.5^2) and transitory income N(0, 0.3^2) a year;
        # every household consumes 0.9 of its permanent income; permanent incomes grow 2% a year for 60 years
        "population": {"n": 10_000, "sd_perm": 0.5, "sd_tran": 0.3, "share": 0.9, "growth": 0.02, "years": 60,
                       "seed": 22},
        # the permanent-income household (chapter 3): the interest rate, and a life of 40 working and 20 retired years
        "pih": {"r": 0.03, "work": 40, "retire": 20, "R": 1.02, "gamma": 2.0},
        # Campbell and Mankiw's economy (chapter 5): a share 0.4 of income goes to hand-to-mouth households
        "rule_of_thumb": {"lam": 0.4, "T": 240, "seed": 22},
        # the buffer-stock household (chapter 6), a year a period, normalized by permanent income (Carroll 1997)
        "buffer": {"beta": 0.96, "R": 1.03, "gamma": 2.0, "G": 1.02, "perm_sd": 0.1, "tran_sd": 0.1, "p_zero": 0.005},
        "mpc": {"n": 20_000, "windfall": 1 / 12, "seed": 22},
        # the wealthy hand-to-mouth (chapter 8): 60% of households hold illiquid wealth (houses, pensions), lognormal
        # around three years of income, earning 7% against cash's 3%; short of cash means under three months' income
        "illiquid": {"own": 0.6, "median": 3.0, "sd": 0.6, "R_h": 1.07, "short": 0.25, "seed": 22},
        # Ricardian equivalence (chapter 10): a tax cut of a month's income now, repaid with interest in 20 years
        "ricardo": {"cut": 1 / 12, "years": 20, "r": 0.03},
        # Diamond's economy (chapter 11): 30-year periods; population growth 40% a generation (1.1% a year)
        "olg": {"alpha": 0.3, "n": 0.4, "A": 10.0, "betas": (0.9, 0.3), "pensions": (0.0, 0.1, 0.2, 0.3, 0.4, 0.5,
                                                                                     0.6, 0.7, 0.8)},
    },
    # Part 23: what a claim on the future is worth
    23: {
        # Play it (chapter 5): a coconut tree pays 20 in a good year and 0 in a bad one (each half the time); the
        # Island's stochastic discount factor is 0.8 in good years and 1.2 in bad (a safe coconut costs 1)
        "playit": {"pay_good": 20.0, "pay_bad": 0.0, "m_good": 0.8, "m_bad": 1.2, "options": (6.0, 8.0, 10.0, 12.0)},
        # the Gordon formula (chapter 1): dividends of 4 growing 3% a year, discounted at 7%
        "gordon": {"D1": 4.0, "r": 0.07, "g": 0.03},
        # the investing firm (chapter 2): adjustment-cost parameter, capital's share, interest, depreciation; productivity
        # rises 20% (equivalently, the user cost falls)
        "firm": {"phi": 4.0, "alpha": 0.33, "r": 0.05, "delta": 0.08, "A0": 1.0, "A1": 1.2, "years": 40},
        # the option to wait (chapter 3)
        "option": {"r": 0.04, "mu": 0.0, "sigmas": (0.1, 0.2, 0.3, 0.4)},
        # Mehra and Prescott's economy (chapter 8): their two-state chain, and the grid of patience and risk aversion
        "mp": {"mu": 0.018, "delta": 0.036, "phi": 0.43, "gamma_max": 10.0, "beta_min": 0.80, "rf_max": 0.04},
        # rare disasters (chapter 9): Barro's 1.7% a year with sizes averaging about 29%; patience 3%, growth 2.5%
        "disasters": {"p": 0.017, "sizes": (0.15, 0.25, 0.35, 0.50, 0.65), "weights": (0.35, 0.25, 0.20, 0.12, 0.08),
                      "rho": 0.03, "g": 0.025, "sd": 0.02, "gammas": (1, 2, 3, 3.5, 4)},
        # habits (chapter 9): Campbell and Cochrane's annual calibration
        "habit": {"gamma": 2.0, "phi": 0.87, "g": 0.0189, "sd": 0.015, "years": 100, "seed": 23},
        # the stylized laboratory market (chapter 11)
        "ssw": {"periods": 15, "dividends": (0.0, 0.08, 0.28, 0.60), "share_trend": 0.7, "n": 12, "seed": 0},
    },
    # Part 24: the Island's labour market gets frictions (a month a period)
    24: {
        # Play it (chapter 2): wage offers drawn uniformly between 50 and 150 coconuts a week, one a week; a benefit
        # of 40 while searching; weekly patience 0.95; ten offers in the game, the same for every viewer
        "playit": {"low": 50.0, "high": 150.0, "b": 40.0, "beta": 0.95, "offers": (88, 71, 104, 63, 97, 121, 79, 135,
                                                                                  92, 110)},
        # Diamond's coconuts (chapter 0): the chance of meeting a trading partner rises with the number climbing
        "diamond": {"cost_max": 1.0, "gain": 1.2, "contact": 0.9, "grid": 200},
        # the DMP economy (chapters 6-9), monthly: productivity 1, benefit 0.4, matching elasticity and bargaining share
        # 0.5, matching efficiency 0.6, separations 3%, interest 0.4%, vacancy cost 0.3
        "dmp": {"p": 1.0, "b": 0.4, "beta": 0.5, "eta": 0.5, "A": 0.6, "s": 0.03, "r": 0.004, "c": 0.3},
        # Shimer's quarterly calibration and Hagedorn and Manovskii's small surplus, each with the vacancy cost set so
        # that tightness is one in the steady state
        "shimer": {"b": 0.4, "beta": 0.72, "eta": 0.72, "s": 0.10, "r": 0.012, "f": 1.355},
        "hm": {"b": 0.955, "beta": 0.052, "eta": 0.45, "s": 0.10, "r": 0.012, "f": 1.355},
        # the job ladder (chapter 11): offers arrive five times as often as jobs end
        "ladder": {"p": 1.0, "b": 0.4, "lam": 0.1, "delta": 0.02},
    },
    25: {
        # Play it and Kiyotaki-Wright (chapters 2-3): three goods, salt, coconuts and fish, costing 0.1, 0.2 and 0.6 a
        # period to keep (fish spoils); Ana eats salt and makes coconuts, Bo eats coconuts and makes fish, Dara eats
        # fish and makes salt; eating is worth 1; patience 0.9 a period; 300 of each kind, 400 periods of meetings.
        # In chapter 3 fish is smoked, so it keeps better: 0.25 a period
        "kw": {"goods": ("salt", "coconuts", "fish"), "names": ("Ana", "Bo", "Dara"), "c": (0.1, 0.2, 0.6),
               "c3_smoked": 0.25, "u": 1.0, "beta": 0.9, "n": 300, "periods": 400, "seed": 0},
        # Cagan's money demand (chapters 6-8): a semi-elasticity of 5 months, so seigniorage peaks at 20% a month;
        # a deficit of 4% of the real balances held at zero inflation, financed by printing; expectations that adapt
        # slowly (10% of the gap a month) or fast (50%)
        "cagan": {"alpha": 5.0, "deficit": 0.04, "lam_slow": 0.1, "lam_fast": 0.5, "months": 60},
        # Baumol-Tobin (chapter 9): a month's income of 3,000 coconuts, a trip to the bank costs 2
        "baumol": {"Y": 3000.0, "b": 2.0},
        # cash in advance (chapters 11-12): yearly patience 0.96, disutility of work 1
        "cia": {"beta": 0.96, "a": 1.0},
    },
    26: {
        # the Island's bank (chapters 1-4): a quarter of depositors turn out to need their money early; the bank's
        # investment pays 1.5 if held to the end and 1 if cut short; depositors' risk aversion 2; 1,000 depositors
        "dd": {"R": 1.5, "gamma": 2.0, "t": 0.25, "n": 1000, "seed": 0},
        # Play it (chapter 2): half of the other depositors say they will withdraw tomorrow
        "playit": {"share_saying": 0.5, "options": ("stay", "withdraw")},
        # the balance sheet (chapters 1, 8): reserves 10, loans 60, ten-year bonds 30 bought at 1.5%; deposits 90,
        # equity 10; then yields rise 3 points
        "sheet": {"reserves": 10.0, "loans": 60.0, "bonds": 30.0, "deposits": 90.0, "equity": 10.0, "coupon": 0.015,
                  "years": 10, "y0": 0.015, "y1": 0.045, "weights": {"reserves": 0.0, "loans": 1.0, "bonds": 0.0}},
        # Bagehot (chapter 6): withdrawals of 30; loans sell at 60% of face in a hurry; the lender's haircut 20%,
        # penalty rate 5%
        "llr": {"liquid": 10.0, "loans": 90.0, "deposits": 90.0, "equity": 10.0, "withdraw": 30.0, "fire_price": 0.6,
                "haircut": 0.2, "penalty": 0.05},
        # deposit insurance as a put (chapter 7): assets 100, deposits 90, a year, asset volatility from 5% to 25%
        "merton": {"V": 100.0, "D": 90.0, "sigmas": (0.05, 0.10, 0.15, 0.20, 0.25)},
        # the global game (chapter 10): a withdrawer gets 1, a stayer 2 if the bank survives; noise 0.05; 2,000
        # depositors; a more generous deposit pays withdrawers 1.2
        "gg": {"c": 1.0, "R": 2.0, "sigma": 0.05, "n": 2000, "c_generous": 1.2, "seed": 0},
        # the repo run (chapter 9): a dealer with securities of 100 and equity of 4 funds the rest by repo; the
        # haircut rises from 4% to 20%
        "repo": {"assets": 100.0, "equity": 4.0, "haircut_from": 0.04, "haircut_to": 0.20},
        # delegated monitoring (chapter 12): each borrower repays 1.3 with probability 0.9, nothing otherwise; the
        # bank promises depositors 1 per loan; monitoring a borrower costs 0.02
        "monitor": {"p": 0.9, "R": 1.3, "D": 1.0, "cost": 0.02, "ns": (1, 10, 100, 1000), "depositors": 1000},
    },
    27: {
        # the Island's babysitting co-op (chapters 0, 3): 150 couples, each wanting a reserve of 10 coupons; each week a
        # couple at its reserve wants to go out with probability 0.3; the co-op starts with 4 coupons a couple and the
        # board raises it to 9 in week 100
        "coop": {"n": 150, "target": 10.0, "p": 0.3, "start": 4.0, "print_to": 9.0, "print_at": 100, "weeks": 200,
                 "seed": 3},
        # Play it (chapter 2): you hold 3 coupons and want a reserve of 10 before the busy season
        "playit": {"held": 3, "target": 10, "options": ("spend", "hoard")},
        # the Island's spending (chapters 4-6): autonomous consumption 200, marginal propensity to consume 0.6, taxes
        # 100, investment 300 (falling by 1 per point of the interest rate times 25), government purchases 200;
        # money demand 0.5 Y - 50 i
        "cross": {"a": 200.0, "b": 0.6, "T": 100.0, "I": 300.0, "G": 200.0, "dG": 100.0},
        "thrift": {"a": 200.0, "b": 0.6, "I": 300.0, "da": 50.0, "h": 0.1},
        "islm": {"a": 200.0, "b": 0.6, "T": 100.0, "I0": 300.0, "d": 25.0, "k": 0.5, "h": 50.0, "G": 200.0,
                 "M": 600.0, "dG": 50.0, "dM": 100.0, "slump": 150.0},
        # Phillips's machine (chapter 8): spending 0.6 of disposable income, taxes 20%, investment 150, government 200,
        # which rises by 50
        "moniac": {"b": 0.6, "tax": 0.2, "I": 150.0, "G": 200.0, "dG": 50.0, "speed": 0.25, "steps": 60,
                   "shock_at": 8},
        # pay (chapter 9): notional changes averaging +1% with a 4% spread; four in five cuts are not made
        "wages": {"n": 20000, "mean": 0.01, "sd": 0.04, "rigid": 0.8, "seed": 2},
        # AS-AD (chapter 10): potential output 1450, expected price level 1, wages sticky (slope 300)
        "asad": {"Ystar": 1450.0, "Pe": 1.0, "kappa": 300.0, "dM": -100.0, "cost": 0.15},
    },
    28: {
        # the Island's council holds unemployment a point below its natural rate of 5% (chapter 3); inflation responds
        # half a point per point of unemployment; expectations are last year's inflation, or adapt more slowly
        "accelerate": {"years": 15, "ustar": 5.0, "u_target": 4.0, "beta": 0.5, "lam": 1.0, "lam_slow": 0.3,
                       "pi0": 2.0},
        # Play it (chapter 2): the viewer forecasts 1973's inflation from 1960-1972
        "playit": {"history": (1960, 1972), "target": 1973, "options": (3.0, 6.0, 11.0)},
        # adaptive expectations (chapter 5): weights on last year's surprise
        "adaptive": {"lams": (0.2, 0.5, 1.0)},
        # Lucas's islands (chapter 7): relative-price noise 1; calm and volatile money
        "islands": {"sigma_z": 1.0, "sigma_m_calm": 0.5, "sigma_m_wild": 3.0, "b": 1.0, "n_islands": 200,
                    "years": 60, "seed": 4},
        # the Lucas critique (chapter 8): output responds 2 to an inflation surprise; the council moves its rule from
        # 2% to 6% inflation
        "critique": {"ystar": 100.0, "b": 2.0, "pibar_old": 2.0, "pibar_new": 6.0, "sd": 1.5, "years": 40,
                     "seed": 5},
        # Barro-Gordon and Rogoff (chapter 9): society weights output 1; it wants output 2 above the natural level;
        # supply shocks of standard deviation 2
        "bg": {"lam": 1.0, "k": 2.0, "b": 1.0, "sigma": 2.0},
    },
    29: {
        # the cake (chapters 3-4): patience 0.9, a cake of 1 on a grid of 1,001 sizes
        "cake": {"beta": 0.9, "w_max": 1.0, "n": 1001, "iters": 400, "keep": (0, 1, 2, 5, 10, 30, 100)},
        # Brock and Mirman (chapter 5): capital's share 0.36, patience 0.96, TFP with persistence 0.9 and shocks 2%
        "bm": {"alpha": 0.36, "beta": 0.96, "rho": 0.9, "sigma": 0.02, "T": 200, "seed": 7},
        "growth": {"alpha": 0.36, "beta": 0.96, "delta": 0.1, "rho": 0.9, "sigma": 0.02, "nk": 151, "nz": 5},
        # the Island's real business cycle (chapters 6-10): quarterly; capital's share 0.36, patience 0.99,
        # depreciation 2.5% a quarter, TFP persistence 0.95 with shocks of 0.7%, a third of time at work
        "rbc": {"alpha": 0.36, "beta": 0.99, "delta": 0.025, "rho": 0.95, "sigma": 0.007, "n_ss": 1 / 3,
                "T": 20000, "seed": 11, "frisch_grid": (0.25, 0.5, 1.0, 2.0, 4.0)},
        # Markov chains (chapter 5): seven states
        "chains": {"n": 7, "rho": 0.95, "sigma": 0.007, "rho_high": 0.995},
    },
    30: {
        # Bo's ferry fare, painted on the board by the pier (chapter 3): demand elasticity 6, so a markup of 20%
        "menu": {"eps": 6.0, "gaps": (0.01, 0.02, 0.05, 0.10)},
        # the Island's New Keynesian economy (chapters 5-13): Gali's (2015) quarterly baseline
        "nk": {"beta": 0.99, "sigma": 1.0, "phi": 1.0, "alpha": 1 / 3, "eps": 6.0, "theta": 2 / 3, "phi_pi": 1.5,
               "phi_x": 0.125, "rho_shock": 0.5, "size": 1.0, "thetas": (0.25, 0.5, 2 / 3, 0.75, 0.85)},
        # the zero lower bound (chapter 12): the natural rate at -2% (annualized) for six quarters
        "zlb": {"T": 6, "rn_low": -2.0, "extras": (0, 1, 2, 3), "fg_horizons": (1, 2, 4, 6, 8, 10, 12)},
        # habits, indexation and smoothing (chapter 13)
        "hybrid": {"habit": 0.9, "index": 0.9, "smooth": 0.8},
        # a population of price setters (chapter 11): 10% change each month; targets drift 4% a month
        "setters": {"n": 20000, "freq": 0.1, "shock": 0.05, "sigma_a": 0.04, "months": 24, "seed": 3},
    },
    31: {
        # the Island's monetary history (chapters 4-5): recursive timing, the bank's private news about next quarter's
        # cost and demand shocks, and a true policy shock of 0.25 points a quarter (agora.cb.DEFAULT)
        "history": {"a": 0.8, "b": 0.25, "c": 0.08, "rho": 0.7, "phi_pi": 1.5, "phi_y": 0.5, "phi_ns": 1.5,
                    "phi_nd": 1.0, "sd_d": 0.5, "sd_s": 0.3, "sd_v": 0.25, "sd_ns": 0.3, "sd_nd": 0.4},
        # four methods scored on 300 histories of 60 years each; the announcement reveals 60% of the bank's demand
        # news (the information effect); the commodity proxy measures cost news with noise 0.15
        "mc": {"reps": 300, "T": 240, "h": 16, "info": 0.6, "proxy_noise": 0.15, "seed": 31},
        # the market for reserves (chapter 1): deposit rate 1%, lending rate 3%, banks need about 50 units
        "reserves": {"floor": 1.0, "ceiling": 3.0, "need": 50.0, "spread": 15.0},
        # Taylor's rule (chapters 2 and 7): r* 2%, target 2%, half on inflation's gap, half on output's
        "taylor": {"rstar": 2.0, "target": 2.0, "a_pi": 0.5, "a_y": 0.5},
        # the natural rate drifts (chapter 11): a random walk with s.d. 0.12 a quarter, estimated by the filter
        "rstar": {"T": 200, "seed": 4, "a": 0.8, "b": 0.3, "sd_y": 0.6, "sd_r": 0.12, "r0": 3.0, "phi_y": 0.6},
        # a eurozone country's debt (chapter 12): debt 120% of GDP, a safe rate of 2%; the fiscal capacity is
        # chosen so that the good equilibrium is 2.5% and the unstable one 6%; the backstop caps yields at 3.5%
        "debt": {"debt": 1.2, "rf": 0.02, "r_good": 0.025, "r_bad": 0.06, "cap": 0.035},
    },
    32: {
        # the Island's treasury (chapters 1-2): debt equal to a year's output, a 3% interest rate, 2% growth and a
        # primary deficit of 2% of output
        "budget": {"debt": 1.0, "r": 0.03, "g": 0.02, "deficit": 0.02, "years": 40},
        # the multiplier in the Part 30 economy (chapter 3): spending raises potential by half its size (gamma)
        "nk": {"gamma": 0.5, "gy": 0.2, "rhos": (0.0, 0.3, 0.5, 0.6, 0.7)},
        # a currency union of 48 regions over 40 years (chapter 4): local multiplier 1.5, national 0.6
        "regions": {"R": 48, "T": 40, "m_local": 1.5, "m_agg": 0.6, "seed": 32},
        # a war (chapter 9): spending of 20% of output, 50% for five years
        "war": {"before": 10, "length": 5, "after": 35, "normal": 0.2, "war": 0.5, "r": 0.03},
        # unpleasant arithmetic (chapter 10): a primary deficit of 1% of output, a money base of 15%
        "unpleasant": {"deficit": 0.01, "b0": 0.5, "r": 0.03, "g": 0.02, "base": 0.15, "mu_tight": 0.0,
                       "T_tight": 12, "years": 30},
        # the fiscal theory (chapter 10): nominal debt 100, a real rate of 2%, a surplus of 2 that falls to 1.5
        "ftpl": {"B": 100.0, "r": 0.02, "surplus": 2.0, "surplus_low": 1.5},
    },
    33: {
        # Minsky's borrowers (chapter 2): debt grows 10% a year against cash flow's 2% while credit is cheap at 3%,
        # then the rate doubles to 6% over the last three years
        "minsky": {"n": 4000, "years": 12, "rate0": 0.03, "rate_end": 0.06, "growth": 0.10, "seed": 33},
        # the Island's lenders (chapter 4): project returns lognormal with a log standard deviation of 0.35,
        # monitoring costs 15% of a failed project; firms borrow until capital's return meets the premium
        "bgg": {"sigma": 0.35, "mu": 0.15, "K_star": 2.0, "theta": 0.3, "N_fall": 0.10},
        # the Island's farmers and gatherers (chapter 5): R = 1.1 a period, an elasticity of land supply of 2, and a
        # fall of 1% in the farmers' output
        "km": {"R": 1.1, "eta": 2.0, "a": 1.0, "c": 0.5, "shock": 0.01, "T": 30},
        # the leverage cycle (chapter 6): the asset pays 1, or 0.2 after bad news twice
        "leverage": {"d": 0.2},
        # the Island's 400 counties (chapter 8): an MPC out of housing wealth of 2 cents plus 6 cents per unit of
        # leverage, house prices falling about a quarter
        "counties": {"n": 400, "seed": 33, "mpc_base": 0.02, "mpc_slope": 0.06, "price_drop": 0.25},
    },
    34: {
        # the governor's choice (chapter 2): abandoning the peg costs 1 (in squared units of slack); an expected
        # devaluation of 0.5 adds gamma * 0.5 to the slack a defence must bear; the Island's slack is 0.75
        "playit": {"cost": 1.0, "gamma": 1.0, "delta": 0.5, "u_island": 0.75},
        # overshooting (chapter 7): money up 10%; money demand's interest semi-elasticity 4 (years); prices close
        # half the gap in about 1.4 years (theta = 0.5)
        "dornbusch": {"dm": 0.10, "lam": 4.0, "theta": 0.5, "T": 8.0},
        # a first-generation attack (chapter 8): a peg of 100, domestic credit of 60 growing 2 a year, money
        # demand's semi-elasticity 5
        "krugman": {"peg": 100.0, "d0": 60.0, "mu": 2.0, "alpha": 5.0, "T": 25.0},
    },
    35: {
        # the Play-it trade (chapter 1): hours per unit of fish and of cloth on the Island and in the Archipelago,
        # which is better at both; the Island has twice the hours; half of spending goes on each good
        "playit": {"island": (3.0, 6.0), "arch": (1.0, 4.0), "L_island": 1200.0, "L_arch": 600.0, "beta": 0.5},
        # Ricardo's numbers (chapter 2), with England a quarter larger than Portugal in workers
        "ricardo": {"L_england": 1.25, "L_portugal": 1.0, "beta": 0.5},
        # the chain and the continuum (chapter 3): the Island's edge A(z) = a*(z)/a(z) = level exp(k (1 - 2 z)) over
        # 200 goods (below one in most: the Archipelago is the more productive), equal spending shares, the
        # Archipelago's labour force twice the Island's; shipping keeps 85% of a cargo
        "dfs": {"n": 200, "k": 1.5, "level": 0.4, "L": 1.0, "Lf": 2.0, "g": 0.85, "growth": 1.5},
        # Heckscher-Ohlin (chapter 5): cloth uses labour (share 0.7), machines capital (labour share 0.3); the Island
        # is labour-abundant, the Archipelago capital-abundant
        "ho": {"alphas": (0.7, 0.3), "island": (120.0, 50.0), "arch": (80.0, 130.0), "beta": 0.5},
        # specific factors (chapter 8): 100 workers, capital in manufacturing, land in agriculture, labour share 0.5
        "specific": {"pM": 1.0, "pA": 1.0, "L": 100.0, "K": 100.0, "T": 100.0, "theta": 0.5, "dpA": 0.10},
        # tariffs (chapter 9): the Island's cloth market, D = 100 - 10 p, S = 10 p - 20, world price 4; the
        # Archipelago's export supply when the Island is large, X* = 40 p* - 120 (free trade still at 4)
        "tariff": {"a": 100.0, "b": 10.0, "c": -20.0, "d": 10.0, "pw": 4.0, "t": 1.0, "e": -120.0, "f": 40.0},
        # protection for sale (chapter 10): ten industries, four organized; welfare weighs 50 times contributions
        "gh": {"n": 10, "organized": (1, 1, 0, 1, 0, 0, 1, 0, 0, 0), "a": 50.0, "alpha_L": 0.05, "seed": 35},
        # the tariff war (chapter 11): two mirror-image economies
        "war": {"A": 10.0, "b_lo": 0.5, "b_hi": 2.0},
    },
    36: {
        # Krugman (chapter 2): workers, fixed cost, elasticity of substitution; and the home-market effect's freeness
        "krugman": {"L": 1000.0, "f": 1.0, "sigma": 4.0, "phi": 0.3},
        # Melitz (chapter 6): Pareto shape 4.25, fixed costs of producing (1), exporting (1.5) and entering (2),
        # shipping 1.3, exit rate 0.1; 4,000 potential firms
        "melitz": {"sigma": 4.0, "k": 4.25, "f": 1.0, "fx": 1.5, "fe": 2.0, "tau": 1.3, "delta": 0.1, "n": 4000,
                   "seed": 41},
        # Eaton and Kortum (chapter 7): three islands' technology levels and shipping costs
        "ek": {"T": (1.0, 2.0, 0.5), "d": ((1.0, 1.5, 2.0), (1.5, 1.0, 1.8), (2.0, 1.8, 1.0)), "theta": 4.0,
               "goods": 20000, "seed": 7},
        # a value chain (chapter 11): the Island designs, the Archipelago makes components, the Far Isle assembles;
        # A[i, j] is the Island-dollars of i's output in a dollar of j's; the Far Isle sells $100 of phones
        "chain": {"A": ((0.0, 0.15, 0.10), (0.0, 0.0, 0.60), (0.0, 0.0, 0.0)), "exports": (0.0, 0.0, 100.0)},
        # the frontier (chapter 14): the share of traded intermediate inputs in costs
        "intermediates": 0.5,
        # the China shock on the Island's 400 local labour markets (chapter 10): the planted effect of a unit of
        # import exposure on the manufacturing share
        "shock": {"n_zones": 400, "n_ind": 30, "beta": -0.6, "seed": 36},
        # the hat-algebra counterfactual (chapter 9): trade costs between America and China up 25%, theta 4
        "hat": {"theta": 4.0, "rise": 1.25, "n_top": 15},
    },
    37: {
        # Schelling's board (the hook and chapter 1): 40 by 40, a tenth empty, content with a third alike
        "schelling": {"n": 40, "empty": 0.1, "threshold": 1 / 3, "seed": 3},
        # von Thuenen's crops around the Island's market town (chapter 2): yield per hectare, price and cost per ton
        # at market, freight per ton-kilometre; the rings run 0-3, 3-10, 10-35 and 35-100 km
        "thunen": ({"name": "vegetables and milk", "yield": 20.0, "price": 100.0, "cost": 53.2, "freight": 10.4},
                   {"name": "firewood", "yield": 12.0, "price": 40.0, "cost": 7.5, "freight": 26.0 / 12.0},
                   {"name": "grain", "yield": 2.6, "price": 150.0, "cost": 90.0, "freight": 1.0},
                   {"name": "cattle", "yield": 0.5, "price": 320.0, "cost": 120.0, "freight": 2.0}),
        # the monocentric town (chapter 3): a million households with $60,000, commuting at $1,000 a kilometre a
        # year; the car halves the cost, the lift makes height 40% cheaper
        "mono": {"N": 1.0e6, "y": 60.0, "t": 1.0, "alpha": 0.25, "theta": 0.25, "i": 0.06, "car": 0.5, "lift": 0.6},
        # agglomeration (chapter 4): the planted elasticity of productivity to density, and abler workers' taste for
        # dense towns
        "agglo": {"gamma": 0.03, "sort": 0.3, "seed": 37},
        # Gibrat with a floor (chapter 5)
        "gibrat": {"n": 20000, "T": 3000, "sigma": 0.2, "floor": 0.05, "seed": 37},
        # Krugman's core and periphery (chapter 6): manufacturing's share of spending and the elasticity
        "cp": {"mu": 0.4, "sigma": 5.0},
        # the Island's six towns (chapters 7, 8 and 13): productivity, amenity (log utility), housing supply
        "towns": {"names": ("Harbour", "Boatyard", "Market", "Grove", "Ridge", "Lagoon"),
                  "a": (0.30, 0.20, 0.10, 0.00, -0.10, 0.00), "q": (0.00, -0.05, 0.00, 0.05, -0.10, 0.15),
                  "eta": (0.6, 1.5, 2.5, 3.0, 2.0, 0.8), "b": 0.3, "alpha": 0.3},
        # the line city divided by a wall (chapter 11)
        "berlin": {"J": 61, "half": 6.0, "cbd": 1.5, "sub": -3.5},
    },
    38: {
        # labour supply (chapter 2): non-labour income, curvature of consumption utility, Frisch elasticity
        "supply": {"y": 5.0, "gamma": 2.0, "phi": 0.5, "psi": 1.0, "res_median": 12.0, "res_sd": 0.5},
        # a competitive market (chapter 4): demand A w^-0.5, supply B w
        "market": {"A": 100.0, "eps_d": 0.5, "B": 4.0, "eps_s": 1.0},
        # one employer (chapter 7): marginal product 30 L^-0.3, labour supply elasticity 3 (a 25% markdown)
        "monopsony": {"a": 30.0, "b": 0.3, "eta": 3.0, "B": 1.0},
        # the border experiment on the Island (chapter 8): the same 331 and 79 stores, the same rise
        "border": {"n_treat": 331, "n_ctrl": 79, "m0": 4.25, "m1": 5.05, "eps_d": 0.5, "eta": 3.0, "trend": -0.06,
                   "noise": 0.25, "seeds": 200},
        # Roy's two occupations (chapter 11): fishing and the boatyard
        "roy": {"n": 20000, "mu": (2.6, 2.5), "sd": (0.4, 0.6), "rho": 0.3, "cost_sd": 0.3, "seed": 38},
    },
    39: {
        # the task model (chapter 4): three skills, productivity exp(beta i); machines take the band (0.40, 0.60)
        "tasks": {"L": 1.0, "M": 1.0, "H": 1.0, "beta": (0.0, 1.0, 2.0), "auto": (0.40, 0.60)},
        # robots (chapter 5): 300 commuting zones; the planted effect is Acemoglu and Restrepo's -0.2 points per
        # robot per thousand workers, and manufacturing declines for other reasons too
        "robots": {"n_zones": 300, "beta": -0.20, "manuf_trend": -3.0, "noise": 0.4, "seed": 39},
        # the worker-firm economy (chapter 6): worker and firm effects, sorting, mobility
        "firms": {"n_workers": 20000, "n_firms": 400, "years": 6, "sd_alpha": 0.40, "sd_psi": 0.15, "sort": 0.3,
                  "move": 0.10, "sd_e": 0.12, "seed": 39},
        # superstars (chapter 7): talent's spread, and the reach of three technologies
        "stars": {"n": 100000, "sd_talent": 0.10, "reach": (1.0, 3.0, 8.0), "seed": 39},
        # compensating differentials (chapter 9): sixty jobs
        "hedonic": {"n": 60, "seed": 39},
        # discrimination (chapter 10): an eighth of workers in the minority; Phelps's two noise levels
        "becker": {"share_minority": 0.125, "d_scale": 0.15},
        "phelps": {"sd_q": 1.0, "sd_noise": (0.5, 1.0)},
        # the child penalty (chapter 12): mothers' earnings in years 0, 1, 2, 5 and 10 after the first child
        "child": {"n": 4000, "penalty": (0.0, -0.30, -0.25, -0.22, -0.20), "seed": 39},
    },
    40: {
        # the Island's incomes (chapters 2 and 15): careers under random growth, sampled for the measures
        "sample": {"n": 2000, "years": 400, "nu": 0.0, "sigma": 0.12, "delta": 0.025, "seed": 40},
        # random growth (chapter 4): log income drifts at nu with volatility sigma; careers end at rate delta and
        # restart at 1; sigma rises from sigma0 to sigma1 (the top 1% share from about 7% to 20%)
        "growth": {"nu": 0.0, "sigma0": 0.0894, "sigma1": 0.144, "delta": 0.025, "floor": -1.0, "n": 50000,
                   "seed": 40},
        # type dependence (chapter 5): a share q_h of newcomers grow fast (nu_h), until they turn ordinary at rate
        # psi; the fast types' growth rises from nu_h0 to nu_h1
        "types": {"nu_l": -0.03, "sigma": 0.10, "psi": 0.2, "q_h": 0.15, "nu_h0": 0.085, "nu_h1": 0.16},
        # wealth (chapter 6): dynasties consume c of their wealth a year, returns are risky, dynasties end or split
        "wealth": {"c": 0.03, "sigma": 0.15, "delta": 0.02, "r_minus_g": (0.0, 0.01, 0.02, 0.03, 0.04)},
        # Kuznets's dual economy (chapter 7)
        "kuznets": {"gap": 1.0, "sd_a": 0.4, "sd_m": 0.7, "n": 40000, "seed": 40},
        # generations (chapter 8): the planted elasticity, permanent and transitory spreads, fifteen years of
        # parents' incomes
        "generations": {"n": 6000, "beta": 0.45, "sd_perm": 0.6, "sd_trans": 0.55, "years": 15, "seed": 40},
        # the Gatsby curve's mechanism (chapter 8): economies differing only in the return to inherited skill
        "gatsby": {"lam": 0.5, "sd_h": 1.0, "sd_u": 0.5, "returns": (0.2, 0.35, 0.5, 0.65, 0.8, 0.95, 1.1),
                   "n": 20000, "seed": 40},
        # a flat tax with an equal transfer (chapter 15)
        "policy": {"tax": 0.2},
    },
    41: {
        # the napkin (chapter 0): two elasticities of the tax base
        "laffer": {"e": (0.25, 1.0)},
        # the corporate tax (chapter 1): capital's share of output, the tax, and capital's mobility
        "harberger": {"alpha": 0.3, "tau": 0.2, "eta": (0.0, 0.5, 1.0, 2.0, 5.0, 20.0)},
        # the Harberger triangle (chapter 2): the Island's market for fuel
        "triangle": {"eps_d": 0.5, "eps_s": 1.0},
        # Ramsey (chapter 4): bread, clothes and travel, and the revenue to raise (per unit of spending at cost)
        "ramsey": {"goods": ("bread", "clothes", "travel"), "eps": (0.2, 1.0, 2.0), "revenue": 0.3},
        # Mirrlees (chapters 5 and 7): skills lognormal with a Pareto tail; welfare weights falling with skill
        "mirrlees": {"e": 0.25, "nu": 1.0, "mu": 0.0, "sigma": 0.5, "alpha": 2.0, "tail": 0.97},
        # the top rate (chapters 3 and 6): the Pareto parameter is read from the tax data; these elasticities
        "top": {"e": (0.1, 0.25, 0.5, 1.0), "g": (0.0, 0.25)},
        # bunching (chapter 9): 200,000 taxpayers; the rate rises from 20% to 40% at 50 (thousand)
        "bunching": {"n": 200000, "e": 0.25, "z_star": 50.0, "t0": 0.2, "t1": 0.4, "friction": 0.01, "seed": 41},
        # evasion (chapter 13): a 30% tax, a fine equal to the evaded tax, relative risk aversion 2
        "evasion": {"t": 0.3, "theta": 1.0, "rho": 2.0},
    },
    42: {
        # pooling (chapter 1): a 3% chance of losing one's job in a normal year, 9% in a recession (one year in seven)
        "pooling": {"p_low": 0.03, "p_high": 0.09, "q": 0.15},
        # unemployment insurance, the static model (chapters 2 to 4): resources A besides the wage, risk aversion 2;
        # search costs calibrated so that, at a benefit of half the wage, 80% find work and the elasticity of
        # staying unemployed (holding the tax fixed) is one half
        "baily": {"gamma": 2.0, "w": 1.0, "A": 3.0, "theta": 0.3856, "kappa": 11.81},
        # week by week (chapter 4): half the wage for 26 weeks, then a fifth; no savings
        "weekly": {"b": 0.5, "K": 26, "floor": 0.2, "gamma": 2.0, "beta": 0.999, "theta": 240.0, "kappa": 0.5},
        # health insurance (chapter 6): illness lognormal (median 5% of income, sigma 1.3, capped at 70%), seven in
        # ten fall ill in a year; free care costs 1/0.7 times as much as a 95% coinsurance plan (RAND's ratio)
        "health": {"gamma": 3.0, "p_sick": 0.7, "median": 0.05, "sigma": 1.3, "cap": 0.7, "k": 0.316},
        # the lottery (chapter 7): 75,000 on the list, 40% drawn; coverage effects planted
        "lottery": {"n": 75000, "drawn": 0.4, "take_up": 0.3, "other": 0.14, "runs": 200, "seed": 42},
        # defaults (chapter 9): employees act on their choice about once in twenty-two months
        "defaults": {"attention": 0.045, "want": 0.75, "default": 0.03, "seed": 42},
        # disability examiners (chapter 10)
        "examiners": {"n": 60000, "j": 200, "spread": 0.12, "seed": 42},
        # tagging (chapter 11): a fifth are needy; the tag catches 70% of them and 10% of the rest
        "tagging": {"needy": 0.2, "catch": 0.7, "false_tag": 0.1},
        # a basic income (chapter 12): 20,000 incomes, lognormal around $50,000; elasticity of the base 0.25
        "ubi": {"n": 20000, "median": 50000.0, "sigma": 0.7, "e": 0.25, "seed": 42},
    },
    43: {
        # structure and performance (chapter 1): 300 industries alike in demand and all playing Cournot, five firms
        # each, whose costs differ by a spread drawn for each industry
        "scp": {"n_ind": 300, "n_firms": 5, "a": 10.0, "b": 1.0, "c0": 4.0, "max_spread": 0.6, "seed": 43},
        # the merger game (chapter 2): five brands of cereal in three nests (sweet, nutty, bran), each owned by a
        # different firm; nested logit with nesting parameter 0.6 and price coefficient 1
        "playit": {"names": ("Sun Flakes", "Honey Puffs", "Nut Clusters", "Bran Buds", "Bran Twigs"),
                   "nests": (0, 0, 1, 2, 2), "quality": (0.8, 0.0, 1.0, -0.5, -0.5), "mc": (1.5, 1.2, 1.6, 1.0, 1.0),
                   "sigma": 0.6, "alpha": 1.0, "x": (3, 4), "y": (0, 2)},
        # the car market (chapters 6 and 7): 40 years of 24 models from six firms; buyers' price sensitivity varies
        # around 0.6 with spread 0.15; costs shifted by an observed input price; 40 Islands for the Monte Carlo
        "cars": {"T": 40, "firms": 6, "per_firm": 4, "alpha": 0.6, "sigma": 0.15, "seed": 0, "runs": 40},
        # the cereal aisle (chapters 0 and 8): twelve brands from four firms (four, four, two, two); price
        # sensitivity 1.6 with spread 0.4 (random coefficient on price); 500 simulated shoppers
        "cereal": {"owner": (0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3), "base_mean": 1.0, "base_sd": 0.5,
                   "mc_median": 1.2, "mc_sd": 0.15, "alpha": 1.6, "sigma": 0.4, "ns": 500, "seed": 43,
                   "merge": (8, 10)},
        # plants (chapter 10): value added y = 0.6 l + 0.3 k + omega + eps; productivity persistent (rho 0.8) with
        # innovations 0.15, which makes the 90/10 productivity ratio about two
        "plants": {"n": 1500, "T": 10, "bl": 0.6, "bk": 0.3, "rho": 0.8, "sd_eta": 0.15, "sd_lerr": 0.3,
                   "seed": 43},
        # markups from production data (chapter 11): plants' true markups lognormal around 1.3
        "dlw": {"median": 1.3, "sd": 0.15, "n": 2000, "seed": 43},
        # towns (chapter 12): 400 isolated towns (populations in thousands); the market's margin per head falls
        # from 1 with one firm to 0.6 with two, 0.48 with three, then hardly at all; fixed cost 1
        "towns": {"n": 400, "F": 1.0, "sd": 0.25, "margins": (1.0, 0.6, 0.48, 0.46, 0.45), "seed": 43},
    },
    44: {
        # the game (chapter 1): an Island bus line rebuilds engines for $4,000; upkeep costs $6 a month for every
        # 5,000 miles on the engine; monthly mileage as in Rust's data; four rules to choose from (miles)
        "playit": {"RC": 4000.0, "per_bin": 6.0, "options": (50000, 150000, 250000, 350000)},
        # Rust's model (chapters 2 and 3): his groups 1 to 4, bins of 5,000 miles, 90 states; discount factors
        "rust": {"groups": (1, 2, 3, 4), "bin": 5000.0, "n": 90, "beta": 0.9999,
                 "betas": (0.0, 0.9, 0.99, 0.995, 0.999, 0.9995, 0.9999)},
        # simulated fleets for NFXP against CCP (chapter 3): ten years of monthly decisions
        "fleets": {"sizes": (104, 1000), "months": 120, "seed": 44},
        # dynamic duopoly (chapter 4): eight quality steps, market size 5, investment efficiency 1.5,
        # depreciation 0.3, discount factor 0.925
        "duopoly": {"K": 8, "M": 5.0, "a": 1.5, "delta": 0.3, "beta": 0.925, "T": 4000, "seed": 44},
        # vertical (chapter 5): demand P = 10 - Q, the manufacturer's cost 2
        "vertical": {"a": 10.0, "c": 2.0},
        # the platform (chapter 6): both sides' stand-alone appeal 1; side 1 values side 2 at 0.2
        "platform": {"a1": 1.0, "a2": 1.0, "alpha1": 0.2},
        # lock-in (chapter 7): B is better by 0.3 on average (tastes sd 1); A came first with 20 adopters
        "lockin": {"quality": 0.3, "adopters": 600, "runs": 300, "seed": 44},
        # innovation (chapter 8): the leader's profit 1, interest 5%, imitation 0.1 a year
        "innovation": {"pi1": 1.0, "r": 0.05, "h": 0.1, "a": 10.0, "c": 4.0, "c_new": 2.0},
        # killer acquisitions (chapter 9)
        "killer": {"pi_one": 100.0, "pi_two": 110.0, "pi_duo": 40.0, "cost": 30.0},
        # algorithms (chapter 10): Calvano et al.'s logit duopoly, fifteen prices, alpha 0.15, beta 4e-6, delta 0.95
        "qlearn": {"sessions": 12, "max_iter": 3000000, "stable": 100000, "seed": 44},
        # regulation (chapter 12): demand P = 10 - q, unit cost 2 or 4 with equal chances, profits weighted 0.6
        "regulation": {"a": 10.0, "c_lo": 2.0, "c_hi": 4.0, "nu": 0.5, "weight": 0.6},
    },
}


def truths(part: int) -> dict:
    return TRUTHS[part]
