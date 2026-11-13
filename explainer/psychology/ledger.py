"""The Replication Ledger of *Psychology, Built* (videos/psychology/SYLLABUS.md, §2.5).

One record per finding the series presents: the claim; the original study; what happened when it was run again;
a status; the sources; and the date the record was last checked against them.  The Ledger is the series' honesty
device, so a row is entered only from primary sources (or a named secondary source), in the part's frontier sweep,
and every row carries its date.

    from explainer.psychology import ledger
    ledger.get("donders_ordering").status          # "replicated"
    ledger.rows(part=1)                            # the rows Part 1 enters

Rows live in :data:`LEDGER`, added with :func:`add` below, grouped by the part that enters them.  The drawing of a
row (``ledger_card``) and of the whole board (``ledger_board``) is in :mod:`explainer.psychology.viz`.

Nothing here imports manim.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["STATUSES", "Study", "Finding", "LEDGER", "add", "get", "rows", "counts"]

# status -> what it means (SYLLABUS.md, §2.5)
STATUSES = {
    "replicated": "direct replications find it at a similar size",
    "replicated, smaller": "it is there, at a fraction of the original size",
    "contested": "replications or meta-analyses disagree",
    "failed": "large preregistered replications find nothing",
    "not directly tested": "the classic has never been directly replicated",
    "retracted": "withdrawn for error or fraud",
    "story and record": "the finding stands, but the textbook account of the study is wrong",
}


@dataclass(frozen=True)
class Study:
    """One study: who, when, how many, and what it found.  ``effect`` is a number on the scale named by ``unit``
    (``"d"``, ``"r"``, ``"ms"``, ...) or ``None`` when the report is not a single effect size; ``lo`` and ``hi``
    bound it where an interval was reported."""

    who: str
    year: int
    n: str = ""  # sample, in words ("1 (Donders himself)", "1,469 adults")
    design: str = ""
    effect: float | None = None
    unit: str = ""
    lo: float | None = None
    hi: float | None = None
    found: str = ""  # one line: what it reported


@dataclass(frozen=True)
class Finding:
    key: str
    part: int  # the part that enters the row
    title: str  # a short name for the board (TeX)
    claim: str  # the finding, in one sentence
    original: Study
    status: str
    record: tuple = ()  # later studies, replications, meta-analyses
    note: str = ""  # what the status needs said about it
    sources: tuple = ()  # full references
    checked: str = ""  # ISO date the row was last checked against its sources

    def __post_init__(self):
        if self.status not in STATUSES:
            raise ValueError(f"{self.key}: unknown status {self.status!r}")
        if not self.sources or not self.checked:
            raise ValueError(f"{self.key}: a Ledger row needs its sources and the date they were checked")


LEDGER: dict = {}


def add(f: Finding) -> Finding:
    if f.key in LEDGER:
        raise ValueError(f"duplicate Ledger row {f.key!r}")
    LEDGER[f.key] = f
    return f


def get(key: str) -> Finding:
    return LEDGER[key]


def rows(part: int | None = None, upto: int | None = None) -> list:
    """The rows entered by ``part``, or by every part up to ``upto``, in the order they were added."""
    out = list(LEDGER.values())
    if part is not None:
        out = [f for f in out if f.part == part]
    if upto is not None:
        out = [f for f in out if f.part <= upto]
    return out


def counts(upto: int | None = None) -> dict:
    """How many rows have each status (statuses with no rows included, as 0)."""
    out = {s: 0 for s in STATUSES}
    for f in rows(upto=upto):
        out[f.status] += 1
    return out


# ---------------------------------------------------------------------------
# Part 1 · Kant's Wager
# ---------------------------------------------------------------------------
_ROELOFS = ("A. Roelofs, One hundred fifty years after Donders: insights from unpublished data, a replication, and "
            "modeling of his reaction times, Acta Psychologica 191 (2018) 228-233")
_DONDERS = ("F. C. Donders, Over de snelheid van psychische processen (1868); transl. W. G. Koster, On the speed of "
            "mental processes, Acta Psychologica 30 (1969) 412-431")
_SCHMIDGEN = ("H. Schmidgen, Of frogs and men: the origins of psychophysiological time experiments, 1850-1865, "
              "Endeavour 26 (2002) 142-148")

add(Finding(
    key="nerve_speed", part=1, title=r"The speed of the nerve signal",
    claim="The nerve signal travels at a finite, measurable speed, tens of metres per second.",
    original=Study("Helmholtz", 1850, n="frog nerve-muscle preparations",
                   design="stimulate the nerve at two distances from the muscle; time the twitch",
                   effect=None, unit="m/s", lo=25.0, hi=43.0,
                   found="0.0014 to 0.0020 s over 50 to 60 mm of nerve: 25 to 43 m/s (frogs kept at 2-6 C)"),
    status="replicated",
    record=(
        Study("Helmholtz", 1850, n="human subjects", design="reaction to a shock at the toe against the sacrum",
              effect=60.0, unit="m/s", found="about 60 m/s in human sensory nerves"),
        Study("Hirsch", 1862, n="human subjects", effect=34.0, unit="m/s", found="about 34 m/s"),
        Study("Donders and de Jaager", 1865, n="human subjects", effect=26.0, unit="m/s", found="26.00 to 26.09 m/s"),
        Study("Helmholtz and Baxt", 1867, n="human subjects", effect=33.9, unit="m/s",
              found="33.9 m/s; later, in midsummer 1869, 64.6 m/s: the speed rises with temperature"),
    ),
    note="The first measurement was also psychology's first replication dispute: others found half Helmholtz's "
         "human value, he suspected he had dropped a factor of two, and the cause turned out to be temperature.",
    sources=(_SCHMIDGEN,
             "H. Helmholtz, Vorlaeufiger Bericht ueber die Fortpflanzungsgeschwindigkeit der Nervenreizung, "
             "Archiv fuer Anatomie, Physiologie und wissenschaftliche Medicin (1850) 71-73"),
    checked="2026-11-13",
))

add(Finding(
    key="donders_ordering", part=1, title=r"Mental operations take time",
    claim="Mental operations take measurable time: simple reactions are faster than go/no-go, which are faster "
          "than choice.",
    original=Study("Donders", 1868, n="1 (Donders himself)", design="speech repetition by methods a, b and c",
                   effect=83.0, unit="ms", found="means 201 (a), 237 (c) and 284 (b) ms"),
    status="replicated",
    record=(Study("Roelofs", 2018, n="1, with Donders' original lists", design="direct replication",
                  found="the same ordering: simple fastest, then go/no-go, then choice, with choice and go/no-go close"),),
    note="The ordering is one of the most reproduced facts in psychology; Hick's law is its quantitative form.",
    sources=(_DONDERS, _ROELOFS),
    checked="2026-11-13",
))

add(Finding(
    key="donders_insertion", part=1, title=r"Subtraction gives pure stages",
    claim="The differences are the durations of pure stages: go/no-go minus simple is discrimination (36 ms), "
          "choice minus go/no-go is choice (47 ms).",
    original=Study("Donders", 1868, n="1 (Donders himself)", design="subtraction of mean reaction times",
                   effect=47.0, unit="ms", found="discrimination 36 ms, choice 47 ms"),
    status="contested",
    record=(
        Study("Wundt", 1880, design="critique", found="method c also contains a choice: whether to respond"),
        Study("Roelofs", 2018, n="Donders' students, from his unpublished laboratory notebook",
              design="reanalysis", found="no difference between choice and go/no-go for his students"),
    ),
    note="Subtraction needs pure insertion: adding a stage must leave the others unchanged. Three means cannot "
         "test that. Sternberg's additive-factor method (1969) was built to do without it.",
    sources=(_DONDERS, _ROELOFS,
             "S. Sternberg, The discovery of processing stages: extensions of Donders' method, Acta Psychologica "
             "30 (1969) 276-315"),
    checked="2026-11-13",
))

add(Finding(
    key="hick_law", part=1, title=r"Hick's law",
    claim="Choice reaction time grows with the logarithm of the number of equally likely alternatives.",
    original=Study("Hick", 1952, n="2 (Hick and R. L. Gregory)", design="ten lamps, ten keys, 2 to 10 alternatives",
                   found="RT = b log(n + 1), fitted to his own data and to Merkel's of 1885"),
    status="replicated",
    record=(Study("Hyman", 1953, n="4", design="uncertainty varied by number, probability and sequence",
                  found="RT linear in the information of the stimulus"),),
    note="A preview: Part 25 derives it. The slope falls toward zero with highly practised or highly compatible "
         "mappings.",
    sources=("W. E. Hick, On the rate of gain of information, Quarterly Journal of Experimental Psychology 4 (1952) "
             "11-26",
             "R. Hyman, Stimulus information as a determinant of reaction time, Journal of Experimental Psychology "
             "45 (1953) 188-196",
             "R. W. Proctor and D. W. Schneider, Hick's law for choice reaction time: a review, Quarterly Journal "
             "of Experimental Psychology 71 (2018) 1281-1299"),
    checked="2026-11-13",
))

add(Finding(
    key="victorians_faster", part=1, title=r"Reaction times have slowed since 1889",
    claim="Simple reaction times have slowed since the Victorian era, by tens of milliseconds.",
    original=Study("Woodley, te Nijenhuis and Murphy", 2013, n="a meta-analysis of studies since Galton",
                   design="simple visual RT across studies from 1889 to 2004",
                   found="a slowing of simple RT across the century, read as a decline in general intelligence"),
    status="contested",
    record=(Study("Woods, Wyma, Yund, Herron and Reed", 2015, n="1,469 adults aged 18 to 65",
                  design="simple visual RT with calibrated hardware", effect=213.0, unit="ms",
                  found="mean 231 ms, 213 ms after correcting for hardware delays: as fast as Galton's subjects"),),
    note="The instruments changed: computer displays and keyboards add delays that Galton's apparatus did not "
         "have. A difference between eras, laboratories or devices is first a fact about the apparatus.",
    sources=("M. A. Woodley, J. te Nijenhuis and R. Murphy, Were the Victorians cleverer than us? The decline in "
             "general intelligence estimated from a meta-analysis of the slowing of simple reaction time, "
             "Intelligence 41 (2013) 843-850",
             "D. L. Woods, J. M. Wyma, E. W. Yund, T. J. Herron and B. Reed, Factors influencing the latency of "
             "simple reaction time, Frontiers in Human Neuroscience 9 (2015) 131"),
    checked="2026-11-13",
))
