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
}


def truths(part: int) -> dict:
    return TRUTHS[part]
