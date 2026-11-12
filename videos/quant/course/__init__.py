"""Quant, Built as a course: the table the course site is built from (``tools/course_site.py``).

For every part: where it sits (act, prerequisites, the level it starts at), its story (the question it opens
with, the arc, what it hands to the next part), what a student can do afterwards at each of four levels, its key
results, and which chapters belong to which track.  The films stay the source of the chapters themselves
(``manifest.py``), the READMEs of the worked solutions, and ``READING.md`` of the papers; this table adds only
what none of them says.

The four tracks (``TRACKS``):

* ``U``, undergraduate: a first course.  Calculus, linear algebra and a first probability course are enough.
* ``M``, master's: the derivations, the models and the numerical methods of a financial-engineering degree.
* ``D``, doctoral: the research chapter of each part, its frontier chapter, proofs and open problems.
* ``I``, industry: how the idea is used, what it cost when it failed, the House's rule, the desk questions.

Each chapter has one home tier.  A track watches its own tier and those it builds on (``TRACK_TIERS``).

    from videos.quant.course import PARTS, chapters
    PARTS[10].question
    chapters(10)        # [(index, number, title, tier), ...] in the film's order
"""

from __future__ import annotations

import importlib
import re
from dataclasses import dataclass, field

N_PARTS = 43

TRACKS = {
    "U": ("Undergraduate", "A first course in quantitative finance: the ideas, the pictures, the arithmetic."),
    "M": ("Master's", "The derivations, models and numerical methods of a financial-engineering degree."),
    "D": ("PhD", "Each part's theorem in the literature's generality, its frontier, and open problems."),
    "I": ("Industry", "How desks and funds use it, what it cost when it failed, and the interview questions."),
}
# the tiers each track watches
TRACK_TIERS = {"U": "U", "M": "UMI", "D": "UMDI", "I": "UI"}

ACTS = [
    ("I", "Markets and Money", (1, 3),
     "What a price is, how a trade is made and settled, and what a share is a claim on."),
    ("II", "The Mathematical Toolkit", (4, 8),
     "Martingales and measure, stochastic calculus, econometrics, time series and control: the language of the rest."),
    ("III", "Derivatives (Q)", (9, 22),
     "Pricing by replication: from one-period arbitrage to the volatility surface, rates, credit and XVA."),
    ("IV", "Return Premia (P)", (23, 29),
     "What risk is paid, which factors are real, and how not to fool yourself with a backtest or a model."),
    ("V", "Portfolios, Strategies and the Firm", (30, 34),
     "Turning forecasts into positions, positions into a book, and a book into a business."),
    ("VI", "Market Microstructure", (35, 39),
     "Who trades with whom, the order book, impact and execution, market making, and crypto's market design."),
    ("VII", "The System", (40, 42),
     "Measuring risk, how leverage and liquidity turn losses into crises, and markets full of machines."),
    ("Finale", "Can You Beat the Market?", (43, 43),
     "The evidence, the arithmetic, and what the series built."),
]


@dataclass(frozen=True)
class Part:
    """One part's course entry.  Chapter lists hold the numbers shown in the film's chapter titles; 0 is the
    cold open.  Numbered chapters in none of ``U``, ``D``, ``I`` are master's; the research chapter is doctoral;
    the recap belongs to every track."""

    n: int
    level: str  # the tier at which the part can first be followed: "U", "M" or "D"
    question: str  # the question the part opens with
    story: str  # the arc, in a paragraph
    handoff: str  # what it leaves for later parts
    objectives: dict  # tier -> list of things you can do afterwards
    results: list  # [(name, TeX)], the part's key results
    prereq: tuple = ()  # parts to watch first
    outside: str = ""  # what you need from outside the series
    U: tuple = ()
    D: tuple = ()
    I: tuple = ()
    widget: str = ""  # the interactive on the part's page (site/quant/widgets.js)
    also: tuple = field(default_factory=tuple)  # [(label, repo path)], companion films in this repository


def _load() -> dict:
    parts = {}
    for name in ("act1", "act2", "act3a", "act3b", "act4", "act5", "act6", "act7"):
        for p in importlib.import_module(f"videos.quant.course.{name}").PARTS:
            assert p.n not in parts, f"Part {p.n} listed twice"
            parts[p.n] = p
    return parts


PARTS = _load()

_NUMBERED = re.compile(r"^(\d+)\.\s+(.*)$")


def manifest(n: int):
    """(film title, [(module, class, chapter title)]) of Part ``n``, from its manifest."""
    m = importlib.import_module(f"videos.quant.quant{n}.manifest")
    return m.TITLE, list(m.SCENES)


def chapters(n: int) -> list:
    """Part ``n``'s chapters in the film's order: (index, number or None, title, tier).  Tiers: ``U``, ``M``,
    ``D``, ``I``, or ``*`` for the recap, which every track watches."""
    part = PARTS[n]
    out = []
    scenes = manifest(n)[1]
    for i, (_, _, title) in enumerate(scenes):
        m = _NUMBERED.match(title)
        number = int(m.group(1)) if m else (0 if i == 0 else None)
        text = m.group(2) if m else title
        if i == len(scenes) - 1:
            tier = "*"
        elif number is None:
            tier = "D" if title.lower().startswith("for the researcher") else "I"
        elif number in part.U:
            tier = "U"
        elif number in part.D:
            tier = "D"
        elif number in part.I:
            tier = "I"
        else:
            tier = "U" if number == 0 else "M"
        out.append((i, number, text, tier))
    return out


def act_of(n: int):
    for act in ACTS:
        if act[2][0] <= n <= act[2][1]:
            return act
    raise KeyError(n)


def title(n: int) -> str:
    """The part's title, without the series prefix."""
    return manifest(n)[0].split(",", 2)[-1].strip()


def track_parts(track: str) -> list:
    """The parts a track should watch in order: every part that has a chapter of the track's own tier (for the
    undergraduate track, only parts that start at that level)."""
    out = []
    for n in range(1, N_PARTS + 1):
        tiers = {t for _, _, _, t in chapters(n)}
        if track == "U" and PARTS[n].level != "U":
            continue
        if track in tiers or track == "M":
            out.append(n)
    return out
