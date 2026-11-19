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
}


def truths(part: int) -> dict:
    return TRUTHS[part]
