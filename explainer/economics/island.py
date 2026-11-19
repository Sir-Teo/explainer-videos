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
    },
}


def truths(part: int) -> dict:
    return TRUTHS[part]
