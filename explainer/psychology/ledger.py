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

A row names the Archive datasets it rests on (``data``).  A study that a part shows without entering a row is
declared with :func:`shown`, with the reason and, where a row is due later, the part that will enter it.  The gate
``tools/check_ledger.py psychN`` reads both: every study a part shows has a row, or a stated reason for having none.

Nothing here imports manim.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["STATUSES", "Study", "Finding", "Shown", "LEDGER", "SHOWN", "add", "shown", "get", "rows", "counts"]

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
    data: tuple = ()  # the Archive datasets the row rests on, by name ("PFUNGST_1907")

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


@dataclass(frozen=True)
class Shown:
    """A study a part shows without entering a Ledger row for it.  ``name`` is an Archive dataset
    (``"KANT_1786"``) or the source line of a tag as the scene writes it; ``why`` says why there is no row;
    ``row_in`` is the later part that will enter one, when one is due."""

    part: int
    name: str
    why: str
    row_in: int | None = None

    def __post_init__(self):
        if not self.why.strip():
            raise ValueError(f"Part {self.part}, {self.name}: say why it has no Ledger row")
        if self.row_in is not None and self.row_in <= self.part:
            raise ValueError(f"Part {self.part}, {self.name}: a row due in Part {self.row_in} is not later")


SHOWN: list = []


def shown(part: int, name: str, why: str, row_in: int | None = None) -> Shown:
    if any(s.part == part and s.name == name for s in SHOWN):
        raise ValueError(f"Part {part}: {name!r} is declared twice")
    SHOWN.append(Shown(part, name, why, row_in))
    return SHOWN[-1]


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
    data=("HELMHOLTZ_1850",),
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
    data=("DONDERS_1868",),
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
    data=("DONDERS_1868",),
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
    data=("WOODS_2015",),
))


shown(1, "KANT_1786", "an argument, quoted from its source; not an empirical finding")
shown(1, "EBBINGHAUS_1885", "the first forgetting curve, shown as a historical first; the curve and its "
      "replication are entered with memory", row_in=20)

# ---------------------------------------------------------------------------
# Part 2 · The Experiment
# ---------------------------------------------------------------------------
_PFUNGST = ("O. Pfungst, Clever Hans (The Horse of Mr. von Osten): A Contribution to Experimental Animal and Human "
            "Psychology, transl. C. L. Rahn (1911; German original 1907)")
_LIT = ("L. Lit, J. B. Schweitzer and A. M. Oberbauer, Handler beliefs affect scent detection dog outcomes, Animal "
        "Cognition 14 (2011) 387-394")

add(Finding(
    key="clever_hans", part=2, title=r"An animal reads its handler",
    claim="An animal's apparent answers can be produced by cues its handler gives without knowing it.",
    original=Study("Pfungst", 1907, n="one horse, some hundreds of tests",
                   design="the questioner knows the answer or not; the horse can see him or not",
                   found="98% right when the questioner knew the answer, 8% when he did not; 89% when the horse "
                         "could see him, 6% when it could not"),
    status="replicated",
    record=(Study("Lit, Schweitzer and Oberbauer", 2011, n="18 certified detection-dog teams",
                  design="searches with no target scent anywhere; handlers told where the scent was",
                  found="225 alerts, more of them at the places the handlers believed held the scent"),),
    note="Pfungst then took the horse's place: 23 of 25 people gave him the cue without knowing it. The remedy he "
         "invented, a questioner who does not know the answer, is the blind.",
    sources=(_PFUNGST, _LIT),
    checked="2026-11-13",
    data=("PFUNGST_1907", "LIT_2011"),
))

add(Finding(
    key="bright_rats", part=2, title=r"``Bright'' rats learn faster",
    claim="Rats labelled maze-bright at random learn a maze faster than rats labelled maze-dull, because of what "
          "their experimenters expect.",
    original=Study("Rosenthal and Fode", 1963, n="12 student experimenters, 60 rats",
                   design="five rats each, ten runs a day for five days, labels assigned at random",
                   effect=0.78, unit="correct runs per rat per day",
                   found="2.32 correct runs a day for the 'bright' rats against 1.54 for the 'dull' (one-tailed "
                         "p = .01)"),
    status="not directly tested",
    record=(Study("Rosenthal and Lawson", 1964, design="the same laboratory, Skinner boxes in place of the maze",
                  found="reported by its authors as essentially the same result"),),
    note="One small study with one-tailed tests, repeated in its own laboratory; we know of no independent direct "
         "replication. That handlers' beliefs reach animals is separately established (the row above).",
    sources=("R. Rosenthal and K. L. Fode, The effect of experimenter bias on the performance of the albino rat, "
             "Behavioral Science 8 (1963) 183-189",
             "R. Rosenthal, On the social psychology of the psychological experiment: the experimenter's hypothesis "
             "as unintended determinant of experimental results, American Scientist 51 (1963) 268-283"),
    checked="2026-11-13",
    data=("ROSENTHAL_FODE_1963",),
))

add(Finding(
    key="pygmalion", part=2, title=r"Teachers' expectations raise IQ",
    claim="Telling teachers that certain pupils, chosen at random, are about to bloom raises those pupils' IQ "
          "scores.",
    original=Study("Rosenthal and Jacobson", 1968, n="one elementary school",
                   design="about a fifth of the pupils named to their teachers as likely to bloom",
                   found="larger IQ gains for the named pupils, concentrated in the first two grades"),
    status="replicated, smaller",
    record=(Study("Raudenbush", 1984, n="18 experiments", design="meta-analysis by weeks of prior contact",
                  effect=0.32, unit="d",
                  found="0.32 when teachers had not yet met the pupils, 0.26 after one week, -0.04 after more than "
                        "two weeks"),),
    note="The effect is there when teachers do not yet know their pupils, and gone once they do: a teacher "
         "believes her own two weeks of evidence over a researcher's list.",
    sources=("R. Rosenthal and L. Jacobson, Pygmalion in the Classroom (1968)",
             "S. W. Raudenbush, Magnitude of teacher expectancy effects on pupil IQ as a function of the "
             "credibility of expectancy induction: a synthesis of findings from 18 experiments, Journal of "
             "Educational Psychology 76 (1984) 85-97"),
    checked="2026-11-13",
    data=("RAUDENBUSH_1984",),
))

add(Finding(
    key="demand", part=2, title=r"Subjects do what they think is wanted",
    claim="Participants shift their behaviour toward what they take the experimenter's hypothesis to be.",
    original=Study("Orne", 1962, design="observations and argument: the 'demand characteristics' of an experiment",
                   found="subjects treat an experiment as a problem to solve and try to be good subjects"),
    status="replicated",
    record=(Study("de Quidt, Haushofer and Roth", 2018, n="about 19,000 participants, 11 standard tasks",
                  design="the hypothesis is signalled, or compliance is asked for outright", effect=0.13, unit="SD",
                  found="about 0.13 SD on average when the hypothesis is only signalled; 0.25 to 1 SD when "
                        "participants are asked to go along with it"),),
    note="Real and measurable, and usually modest: the size depends on how plainly the hypothesis shows.",
    sources=("M. T. Orne, On the social psychology of the psychological experiment: with particular reference to "
             "demand characteristics and their implications, American Psychologist 17 (1962) 776-783",
             "J. de Quidt, J. Haushofer and C. Roth, Measuring and bounding experimenter demand, American Economic "
             "Review 108 (2018) 3266-3302"),
    checked="2026-11-13",
    data=("DE_QUIDT_2018",),
))

add(Finding(
    key="not_random", part=2, title=r"People cannot be random",
    claim="People asked to produce a random sequence switch between the alternatives too often and avoid long "
          "runs.",
    original=Study("Wagenaar", 1972, n="a review of earlier studies", design="sequences produced on request",
                   found="systematic departures from randomness, most often too many alternations"),
    status="replicated",
    record=(Study("Falk and Konold", 1997, n="a review of generation and judgment studies",
                  found="sequences that alternate about 60% of the time are the ones produced, and judged most "
                        "random"),),
    note="Why assignment and order are left to a shuffled deck and never to the experimenter's sense of what is "
         "random.",
    sources=("W. A. Wagenaar, Generation of random sequences by human subjects: a critical survey of literature, "
             "Psychological Bulletin 77 (1972) 65-72",
             "R. Falk and C. Konold, Making sense of randomness: implicit encoding as a basis for judgment, "
             "Psychological Review 104 (1997) 301-318"),
    checked="2026-11-13",
))

shown(2, "PEIRCE_JASTROW_1884", "shown for its method, the shuffled deck; its result is not presented")
shown(2, "MITCHELL_2021", "shown for the authors' own count of who guessed their arm, which they call anecdotal; "
      "the trial's result is not presented", row_in=42)
shown(2, r"Arnett (2008); \ Henrich, Heine \& Norenzayan (2010)", "a count of who is sampled, shown to pose "
      "the question of external validity", row_in=38)

# ---------------------------------------------------------------------------
# Part 3 · The Measure
# ---------------------------------------------------------------------------
_JOHANSSON = ("P. Johansson, L. Hall, S. Sikstrom and A. Olsson, Failure to detect mismatches between intention and "
              "outcome in a simple decision task, Science 310 (2005) 116-119")

add(Finding(
    key="barnum", part=3, title=r"A general sketch feels personal",
    claim="People accept a personality description made of general statements as an accurate description of "
          "themselves in particular.",
    original=Study("Forer", 1949, n="39 students", design="one sketch of thirteen statements, given to every "
                   "student as the result of their own test; rated from 0 to 5", effect=4.26, unit="of 5",
                   found="mean rating 4.26 of 5; nobody below 2, five below 4"),
    status="replicated",
    record=(Study("Dickson and Kelly", 1985, n="a review of the studies since 1949",
                  found="general sketches are accepted as accurate throughout; more so the more general and the "
                        "more favourable they are, and depending on the kind of assessment they claim to rest on"),),
    note="Why a reader's agreement that a description fits is no evidence that the test behind it measures "
         "anything: the sketch would have fitted anyone.",
    sources=("B. R. Forer, The fallacy of personal validation: a classroom demonstration of gullibility, Journal of "
             "Abnormal and Social Psychology 44 (1949) 118-123",
             "D. H. Dickson and I. W. Kelly, The 'Barnum effect' in personality assessment: a review of the "
             "literature, Psychological Reports 57 (1985) 367-382"),
    checked="2026-11-13",
    data=("FORER_1949",),
))

add(Finding(
    key="telling_more", part=3, title=r"Telling more than we can know",
    claim="People's reports of why they acted are often inferences from plausible theories, and not observations "
          "of the process that produced the act.",
    original=Study("Nisbett and Wilson", 1977, n="a review of experiments",
                   design="a cause of behaviour is manipulated, and people are asked why they acted",
                   found="people often fail to report causes that moved them, report ones that did not, and give "
                         "the reasons an outside observer would guess"),
    status="replicated",
    record=(Study("Johansson, Hall, Sikstrom and Olsson", 2005, n="120 participants",
                  design="the outcome of a choice is covertly swapped, so a report can be checked against it",
                  found="reasons are given as readily for a choice that was not made as for one that was"),),
    note="The limit matters as much as the finding: it concerns reports of causes. It does not show that people "
         "cannot report what they currently see, feel or intend, and how far it reaches is still argued.",
    sources=("R. E. Nisbett and T. D. Wilson, Telling more than we can know: verbal reports on mental processes, "
             "Psychological Review 84 (1977) 231-259", _JOHANSSON),
    checked="2026-11-13",
))

add(Finding(
    key="choice_blindness", part=3, title=r"Choice blindness",
    claim="People often fail to notice that the outcome of a choice has been swapped, and then give reasons for "
          "the choice they did not make.",
    original=Study("Johansson, Hall, Sikstrom and Olsson", 2005, n="120 participants, 15 choices each",
                   design="choose the more attractive of two faces; on 3 trials the photographs are exchanged",
                   effect=0.26, unit="detected, at most",
                   found="no more than 26% of the swaps were detected, counting every sign of detection"),
    status="replicated",
    record=(Study("Hall, Johansson, Tarning, Sikstrom and Deutgen", 2010, n="shoppers at a supermarket stall",
                  design="taste two jams or smell two teas, choose, then sample the choice again, swapped",
                  found="no more than a third of the swaps were detected"),),
    note="Of those who noticed nothing in the first study, 84% said they would have noticed such a swap.",
    sources=(_JOHANSSON,
             "P. Johansson, Choice Blindness: The Incongruence of Intention, Action and Introspection (doctoral "
             "thesis, Lund University, 2006)",
             "L. Hall, P. Johansson, B. Tarning, S. Sikstrom and T. Deutgen, Magic at the marketplace: choice "
             "blindness for the taste of jam and the smell of tea, Cognition 117 (2010) 54-61"),
    checked="2026-11-13",
    data=("JOHANSSON_2005",),
))

shown(3, "STEVENS_1946", "a committee's disagreement and a classification of scales: an argument, not an empirical "
      "finding")
shown(3, "CREDE_2017", "shown as the example of two names for nearly one thing; whether grit adds anything to "
      "conscientiousness is entered with motivation", row_in=28)
shown(3, "HEDGE_2018", "the reliability paradox is stated here and paid off with its record later", row_in=59)
shown(3, "FLAKE_FRIED_2020", "counts of how measures are reported in journals: a description of practice, not a "
      "finding about minds")

# ---------------------------------------------------------------------------
# Part 4 · The Evidence
# ---------------------------------------------------------------------------
_ML1 = ("R. A. Klein et al., Investigating variation in replicability: a 'Many Labs' replication project, Social "
        "Psychology 45 (2014) 142-152")
_OSC = "Open Science Collaboration, Estimating the reproducibility of psychological science, Science 349 (2015) aac4716"

add(Finding(
    key="precognition", part=4, title=r"Feeling the future",
    claim="People's responses are influenced by events that have not yet happened.",
    original=Study("Bem", 2011, n="more than 1,000 participants in 9 experiments",
                   design="well-known effects run backwards in time, the cause coming after the response",
                   effect=0.22, unit="d", found="mean d = 0.22; 8 of the 9 experiments significant"),
    status="failed",
    record=(Study("Ritchie, Wiseman and French", 2012, n="150 in three preregistered attempts",
                  design="exact replications of the recall experiment", found="no effect (combined p = .83)"),
            Study("Galak, LeBoeuf, Nelson and Simmons", 2012, n="3,289 in seven experiments",
                  design="the recall experiments again, and a meta-analysis of every attempt", effect=0.04, unit="d",
                  found="no effect; across all replication attempts d = 0.04")),
    note="The methods were the field's ordinary methods, which is why the result mattered: it showed what those "
         "methods could produce.",
    sources=("D. J. Bem, Feeling the future: experimental evidence for anomalous retroactive influences on cognition "
             "and affect, Journal of Personality and Social Psychology 100 (2011) 407-425",
             "S. J. Ritchie, R. Wiseman and C. C. French, Failing the future: three unsuccessful attempts to "
             "replicate Bem's 'retroactive facilitation of recall' effect, PLoS ONE 7 (2012) e33423",
             "J. Galak, R. A. LeBoeuf, L. D. Nelson and J. P. Simmons, Correcting the past: failures to replicate "
             "psi, Journal of Personality and Social Psychology 103 (2012) 933-948"),
    checked="2026-11-13",
    data=("BEM_2011",),
))

add(Finding(
    key="low_power", part=4, title=r"Published studies are underpowered",
    claim="The typical published study in psychology has had about an even chance, or less, of detecting a "
          "medium-sized effect.",
    original=Study("Cohen", 1962, n="a year of one journal", design="the power of each study's tests, computed "
                   "for small, medium and large effects", effect=0.48, unit="power",
                   found="mean power 0.48 for a medium effect"),
    status="replicated",
    record=(Study("Sedlmeier and Gigerenzer", 1989, n="the same journal, 24 years later",
                  found="power for a medium effect had not risen (0.37)"),),
    note="Known for sixty years, and the root of two later rows: small studies that reach significance overstate "
         "the effect, and so shrink when repeated.",
    sources=("J. Cohen, The statistical power of abnormal-social psychological research: a review, Journal of "
             "Abnormal and Social Psychology 65 (1962) 145-153",
             "P. Sedlmeier and G. Gigerenzer, Do studies of statistical power have an effect on the power of "
             "studies?, Psychological Bulletin 105 (1989) 309-316"),
    checked="2026-11-13",
    data=("COHEN_1962",),
))

add(Finding(
    key="effects_shrink", part=4, title=r"Published effects shrink when repeated",
    claim="When published findings are repeated with larger samples, fewer are significant and the effects are "
          "about half as large.",
    original=Study("Open Science Collaboration", 2015, n="100 studies from three journals",
                   design="one high-powered replication of each", effect=0.36, unit="share significant",
                   found="97% of originals significant, 36% of replications; effects half the size"),
    status="replicated",
    record=(Study("Camerer and 23 others", 2018, n="21 experiments from Nature and Science",
                  found="13 of 21 (62%) significant; effects about half the size"),
            Study("Klein and 185 others (Many Labs 2)", 2018, n="28 findings, 15,305 participants",
                  found="15 of 28 (54%) significant; median d 0.15 against 0.60")),
    note="How low the rate 'really' is was disputed in 2016, and depends on the definition of success. That "
         "published effects are overstated is not in dispute.",
    sources=(_OSC,
             "C. F. Camerer et al., Evaluating the replicability of social science experiments in Nature and "
             "Science between 2010 and 2015, Nature Human Behaviour 2 (2018) 637-644",
             "R. A. Klein et al., Many Labs 2: investigating variation in replicability across samples and "
             "settings, Advances in Methods and Practices in Psychological Science 1 (2018) 443-490"),
    checked="2026-11-13",
    data=("OSC_2015", "MANY_LABS", "CAMERER_2018"),
))

add(Finding(
    key="flag_priming", part=4, title=r"A flag shifts political views",
    claim="A brief exposure to a national flag shifts people's political attitudes.",
    original=Study("Carter, Ferguson and Hassin", 2011, design="a small flag shown, or not, during a survey",
                   found="a shift toward conservative positions, reported to last for months"),
    status="failed",
    record=(Study("Klein and 50 others (Many Labs 1)", 2014, n="36 samples, 6,344 participants",
                  found="did not replicate"),),
    sources=("T. J. Carter, M. J. Ferguson and R. R. Hassin, A single exposure to the American flag shifts support "
             "toward Republicanism up to 8 months later, Psychological Science 22 (2011) 1011-1018", _ML1),
    checked="2026-11-13",
    data=("MANY_LABS",),
))

add(Finding(
    key="currency_priming", part=4, title=r"Money primes a belief in the system",
    claim="A brief exposure to an image of money increases support for the existing social system.",
    original=Study("Caruso, Vohs, Baxter and Waytz", 2013, design="a banknote in the background of the screen, "
                   "or not", found="more endorsement of free markets and of social inequality"),
    status="failed",
    record=(Study("Klein and 50 others (Many Labs 1)", 2014, n="36 samples, 6,344 participants",
                  found="did not replicate"),),
    sources=("E. M. Caruso, K. D. Vohs, B. Baxter and A. Waytz, Mere exposure to money increases endorsement of "
             "free-market systems and social inequality, Journal of Experimental Psychology: General 142 (2013) "
             "301-306", _ML1),
    checked="2026-11-13",
    data=("MANY_LABS",),
))

add(Finding(
    key="imagined_contact", part=4, title=r"Imagined contact reduces prejudice",
    claim="Imagining a pleasant meeting with a member of another group reduces prejudice toward that group.",
    original=Study("Husnu and Crisp", 2010, design="an imagined conversation, against an imagined outdoor scene",
                   found="greater willingness to engage with the other group"),
    status="contested",
    record=(Study("Klein and 50 others (Many Labs 1)", 2014, n="36 samples, 6,344 participants",
                  found="weak support for replicability"),),
    note="Present in the pooled data, and much smaller than first reported.",
    sources=("S. Husnu and R. J. Crisp, Elaboration enhances the imagined contact effect, Journal of Experimental "
             "Social Psychology 46 (2010) 943-950", _ML1),
    checked="2026-11-13",
    data=("MANY_LABS",),
))

# ---------------------------------------------------------------------------
# Part 5
# ---------------------------------------------------------------------------
add(Finding(
    key="hodgkin_huxley", part=5, title=r"The Hodgkin--Huxley model",
    claim="Voltage-dependent sodium and potassium conductances, measured under voltage clamp, account for the "
          "action potential and its speed.",
    original=Study("Hodgkin and Huxley", 1952, n="squid giant axons",
                   design="currents measured with the voltage held fixed, fitted by four equations; the action "
                          "potential then computed from them",
                   effect=18.8, unit="m/s",
                   found="a computed conduction speed of 18.8 m/s against 21.2 measured, with the spike's shape, "
                         "threshold and refractory period"),
    status="replicated",
    record=(
        Study("this series", 2026, n="the published equations", design="integrated on a cable in Psyche's neuron",
              effect=18.7, unit="m/s", found="18.7 m/s recomputed"),
    ),
    note="The series' standard of quantitative success: measure, write equations, compute, compare. Cole and "
         "Curtis had shown in 1939 that the membrane's conductance rises during the impulse, which the model "
         "requires. It is a model of one membrane, and its gates were later identified with ion channels.",
    sources=("A. L. Hodgkin and A. F. Huxley, A quantitative description of membrane current and its application "
             "to conduction and excitation in nerve, Journal of Physiology 117 (1952) 500-544",
             "K. S. Cole and H. J. Curtis, Electric impedance of the squid giant axon during activity, Journal of "
             "General Physiology 22 (1939) 649-670"),
    checked="2026-11-13",
    data=("HODGKIN_HUXLEY_1952", "COLE_CURTIS_1939"),
))

shown(4, "SIMMONS_2011", "a simulation of what flexible analysis does to a null result, recomputed here: a "
      "demonstration, not an empirical finding")
shown(4, "SCHEEL_2021", "a comparison of two literatures; shown at the frontier as early evidence on a reform, "
      "before the meta-science part", row_in=50)
shown(4, "LEVELT_2012", "the findings of an inquiry into one case of fraud")
shown(4, "DREBER_2015", "prediction markets on replications: shown at the frontier, entered with meta-science",
      row_in=50)
shown(4, "PROTZKO_2023", "a retracted report about replication rates, shown at the frontier for what its "
      "retraction says about the reforms; entered with meta-science", row_in=50)

# ---------------------------------------------------------------------------
# Part 6
# ---------------------------------------------------------------------------
add(Finding(
    key="ltp", part=6, title=r"Long-term potentiation",
    claim="A brief burst of strong activity leaves a synapse stronger for a long time.",
    original=Study("Bliss and Lomo", 1973, n="anaesthetized rabbits",
                   design="brief trains of fast stimulation of the perforant path; single test pulses before and "
                          "after",
                   found="the response in the dentate gyrus stays enlarged long after the trains"),
    status="replicated",
    record=(
        Study("Bi and Poo", 1998, n="pairs of cultured hippocampal neurons",
              design="single input and output spikes paired at chosen intervals",
              found="strengthening when the input comes first, weakening when it comes after, within about 20 ms"),
    ),
    note="That synapses can be strengthened by use is not in doubt. Whether this is how memories are stored is a "
         "separate claim, argued in Part 20.",
    sources=("T. V. P. Bliss and T. Lomo, Long-lasting potentiation of synaptic transmission in the dentate area "
             "of the anaesthetized rabbit following stimulation of the perforant path, Journal of Physiology 232 "
             "(1973) 331-356",
             "G.-Q. Bi and M.-M. Poo, Synaptic modifications in cultured hippocampal neurons, Journal of "
             "Neuroscience 18 (1998) 10464-10472"),
    checked="2026-11-14",
    data=("BLISS_LOMO_1973", "BI_POO_1998"),
))

add(Finding(
    key="lateral_inhibition", part=6, title=r"Lateral inhibition",
    claim="Neighbouring receptors in an eye inhibit one another, in proportion to how active each one is.",
    original=Study("Hartline and Ratliff", 1957, n="single optic nerve fibres of the horseshoe crab",
                   design="two receptor units lit together and apart, each fibre's impulses counted",
                   found="the inhibition on each unit is a linear function of the other's activity"),
    status="replicated",
    record=(
        Study("Hartline and Ratliff", 1958, n="several units lit", found="the inhibitory influences add"),
    ),
    note="The equations of the eye of one animal. They predict the bands Mach described in 1865 at an edge of "
         "light, and the series recomputes them.",
    sources=("H. K. Hartline and F. Ratliff, Inhibitory interaction of receptor units in the eye of Limulus, "
             "Journal of General Physiology 40 (1957) 357-376",),
    checked="2026-11-14",
    data=("HARTLINE_RATLIFF_1957",),
))

add(Finding(
    key="hermann_grid", part=6, title=r"The Hermann grid, explained by receptive fields",
    claim="The grey spots at the crossings of the Hermann grid are produced by centre-surround receptive fields.",
    original=Study("Baumgartner", 1960, n="", design="an argument from the receptive fields of retinal cells",
                   found="a cell centred on a crossing has more of its surround lit, and so responds less"),
    status="story and record",
    record=(
        Study("Geier, Bernath, Hudak and Sera", 2008, n="observers of altered grids",
              design="the streets given a slight curve, the receptive-field account's conditions unchanged",
              found="the spots vanish"),
    ),
    note="The textbook explanation predicts spots where none are seen. Lateral inhibition is real; this "
         "application of it is at best incomplete, and the mechanism is still disputed.",
    sources=("J. Geier, L. Bernath, M. Hudak and L. Sera, Straightness as the main factor of the Hermann grid "
             "illusion, Perception 37 (2008) 651-665",
             "G. Baumgartner, Indirekte Groessenbestimmung der rezeptiven Felder der Retina beim Menschen mittels "
             "der Hermannschen Gittertaeuschung, Pfluegers Archiv 272 (1960) 21-22"),
    checked="2026-11-14",
    data=("GEIER_2008",),
))

shown(5, "ADRIAN_1926", "the rate code of a single sensory fibre: told here as the discovery it was, with schematic "
      "trains; its row (rate_code) is entered in Part 13")
shown(5, "GOLGI_CAJAL_1906", "the neuron doctrine: a settled piece of anatomy, told as history")
shown(5, "GIDON_2020", "one laboratory's report of graded dendritic spikes in human cortex, shown at the frontier "
      "and not yet repeated elsewhere")

shown(6, "LOEWI_1921", "chemical transmission at a synapse: settled physiology, told as the history it is (the dream "
      "is Loewi's own later account, and the part says so)")
shown(6, "HEBB_1949", "a postulate, quoted; it is a hypothesis about a rule, and the finding that bears on it is the "
      "row on long-term potentiation")
shown(6, "DEL_CASTILLO_KATZ_1954", "release in packets: settled physiology, told as history; the histogram on "
      "screen is a model synapse's and is tagged as computed")
shown(6, "LIU_2012", "one laboratory's reactivation of a tagged memory in mice, shown at the frontier; whether "
      "strengthened synapses are the memory is argued with the evidence in Part 20", row_in=20)
shown(6, "TURNER_2008", "the registered and the published record of one class of drug trials, shown as a case of "
      "Part 4's file drawer in an industry; entered with the evidence on treatments", row_in=42)

# ---------------------------------------------------------------------------------------------------------------
# Part 7: the brain
# ---------------------------------------------------------------------------------------------------------------
add(Finding(
    key="gage", part=7, title=r"Phineas Gage",
    claim="Damage to the frontal lobes changed a careful, capable man into an impulsive and unreliable one.",
    original=Study("Harlow", 1868, n="one patient", design="his doctor's account, written twenty years after the "
                                                              "accident",
                   found="'no longer Gage', in the words of his friends"),
    status="story and record",
    record=(Study("Macmillan", 2000, n="the surviving documents", design="a history of the case",
                  found="the record of a change is a few sentences; he later held a demanding job for years"),),
    note="He survived, and something changed. How much, for how long, and whether he recovered are not in the "
         "record; most of what textbooks add is not in it either.",
    sources=("J. M. Harlow, Recovery from the passage of an iron bar through the head, Publications of the "
             "Massachusetts Medical Society 2 (1868) 327-347",
             "M. Macmillan, An Odd Kind of Fame: Stories of Phineas Gage (MIT Press, 2000)"),
    checked="2026-11-14",
    data=("HARLOW_1868",),
))

add(Finding(
    key="broca_area", part=7, title=r"Broca's area and speech",
    claim="Damage to the lower rear part of the left frontal lobe takes away fluent speech and spares understanding.",
    original=Study("Broca", 1861, n="one patient, then more", design="speech in life, the brain after death",
                   found="a lesion of the left frontal lobe in a man who could say one syllable"),
    status="replicated",
    record=(Study("Dronkers, Plaisant, Iba-Zizen and Cabanis", 2007, n="Broca's two preserved brains",
                  design="magnetic resonance imaging", found="the damage ran far beyond the area that carries "
                                                             "his name, into deep tissue and a long fibre tract"),),
    note="Replicated, and refined: the left frontal lobe matters for speech, and the lasting syndrome needs more "
         "damage than the area on the textbook's diagram.",
    sources=("P. Broca, Bulletin de la Societe d'Anthropologie 2 (1861) 235-238",
             "N. F. Dronkers et al., Paul Broca's historic cases, Brain 130 (2007) 1432-1441"),
    checked="2026-11-14",
    data=("BROCA_1861", "DRONKERS_2007"),
))

add(Finding(
    key="taxi_hippocampus", part=7, title=r"The taxi drivers' hippocampus",
    claim="Years of navigating London enlarge the back of the hippocampus.",
    original=Study("Maguire and colleagues", 2000, n="16 drivers and matched controls",
                   design="brain scans compared, and related to years of driving",
                   found="more grey matter at the back of the hippocampus, more with more years"),
    status="replicated",
    record=(Study("Woollett and Maguire", 2011, n="79 trainees and 31 controls", design="scanned before and after "
                                                                                       "years of training",
                  found="growth in the 39 who qualified, none in the 20 who failed or in controls"),),
    note="The first study could not say which came first. The second followed people through the training. It "
         "is one laboratory and one skill.",
    sources=("E. A. Maguire et al., Navigation-related structural change in the hippocampi of taxi drivers, PNAS "
             "97 (2000) 4398-4403",
             "K. Woollett and E. A. Maguire, Current Biology 21 (2011) 2109-2114"),
    checked="2026-11-14",
    data=("MAGUIRE_2000",),
))

add(Finding(
    key="brain_types", part=7, title=r"Left-brained and right-brained people",
    claim="People differ in which hemisphere dominates, and that makes them logical or creative.",
    original=Study("Pines, in a magazine article", 1973, n="", design="an extrapolation from patients whose "
                                                                         "hemispheres had been separated",
                   found="'We are left-brained or right-brained'"),
    status="failed",
    record=(Study("Nielsen and colleagues", 2013, n="1,011 people", design="lateralization of 7,266 regions' "
                                                                           "connections at rest",
                  found="lateralization is local: not consistent with a whole-brain type"),),
    note="The hemispheres do differ in what they do. The claim that fails is that a person is one or the other.",
    sources=("M. Pines, We are left-brained or right-brained, New York Times Magazine, 9 September 1973; R. E. "
             "Ornstein, The Psychology of Consciousness (1972)",
             "J. A. Nielsen et al., An evaluation of the left-brain vs. right-brain hypothesis with resting state "
             "functional connectivity magnetic resonance imaging, PLoS ONE 8 (2013) e71275"),
    checked="2026-11-14",
    data=("NIELSEN_2013",),
))

shown(7, "WERNICKE_1874", "a diagram and the syndrome it predicted: told as the history of a model; the finding "
      "it organizes is the row on Broca's area")
shown(7, "LASHLEY_1929", "a famous negative result, told as history with its critics; memory's location is argued "
      "in Part 20", row_in=20)
shown(16, "PAVLOV_1927", "the method and its vocabulary, told as history; the curves shown are Psyche's")
shown(16, "FERSTER_SKINNER_1957", "schedules of reinforcement, whose signatures are drawn on Psyche, not from their records")
shown(16, "WASSERMAN_1993", "human contingency judgment, cited for its main result; judgment is entered with Part 26")
shown(16, "RESCORLA_1968", "a design reproduced on Psyche with the paper's schedule; the paper's figures are not drawn")
shown(16, "RESCORLA_WAGNER_1972", "a model, derived and run, not a finding")
shown(16, "LUBOW_MOORE_1959", "latent inhibition, described and modelled", row_in=18)
shown(16, "MACKINTOSH_PEARCE_HALL", "models of attention, run on one history")
shown(16, "GALLISTEL_GIBBON_2000", "a theory, and a summary of acquisition data shown with its exceptions")
shown(16, "BRELAND_1961", "trainers' observations, told as the anecdotes they were")
shown(16, "BANDURA_1961", "the Bobo doll, described without figures and with the doubt about what it measures")
shown(16, "PRENDERGAST_2006", "a meta-analysis quoted for its effect sizes", row_in=42)
shown(16, "ZENDLE_CAIRNS_2018", "a survey, quoted with its limits; product design is Part 52")
shown(16, "MITCHELL_2009", "a theoretical review at the frontier")
shown(16, "GERSHMAN_2010", "a model at the frontier")
shown(16, "SCHILLER_2010", "reconsolidation update, at the frontier", row_in=21)
shown(7, "PENFIELD_BOLDREY_1937", "the body's map on the cortex: settled anatomy, told as history; its row is "
      "entered with the senses, in Part 15")
shown(7, "HORTON_HOYT_1991", "a measured map used as a formula; the part computes with it")
shown(7, "SCOVILLE_MILNER_1957", "one patient, told as the case it was; what it shows about memory is argued in "
      "Part 20", row_in=20)
shown(7, "AZEVEDO_2009", "a count, used as a number")
shown(7, "RAICHLE_2002", "a measurement of energy use, used as a number")
shown(7, "WEISKRANTZ_1974", "one patient, described without figures; blindsight is entered with awareness",
      row_in=27)
shown(7, "MAH_2014", "a methods finding shown at the frontier, beside the series' own simulation")
shown(7, "WIESEL_HUBEL_1963", "the critical period for one eye's hold on the cortex: told as history; entered with "
      "development", row_in=30)
shown(7, "MERZENICH_1984", "remapping after the loss of a finger: told as history, without figures")
shown(7, "GAZZANIGA_1978", "the split-brain experiments: told as the cases they were; what they show about "
      "awareness is entered in Part 27", row_in=27)


# ---------------------------------------------------------------------------------------------------------------
# Part 8: reading the brain
# ---------------------------------------------------------------------------------------------------------------

add(Finding(
    key="n400", part=8, title=r"The N400",
    claim="A word that does not fit the meaning of its sentence is followed, about 400 ms later, by a negative "
          "brain potential.",
    original=Study("Kutas and Hillyard", 1980, n="a few readers, many sentences", design="potentials averaged over "
                                                                                      "the last words of sentences",
                   found="a negative wave near 400 ms to 'socks', none to 'butter'"),
    status="replicated",
    record=(Study("Kutas and Federmeier", 2011, n="thirty years of studies", design="a review",
                  found="found in reading, listening, signing and pictures; graded by how expected the word is"),),
    note="One of the most repeated effects in the field. What it measures (surprise, or the work of fitting a "
         "meaning in) is still argued.",
    sources=("M. Kutas and S. A. Hillyard, Reading senseless sentences: brain potentials reflect semantic "
             "incongruity, Science 207 (1980) 203-205",
             "M. Kutas and K. D. Federmeier, Thirty years and counting, Annual Review of Psychology 62 (2011) "
             "621-647"),
    checked="2026-11-14",
    data=("KUTAS_HILLYARD_1980",),
))

add(Finding(
    key="brain_training", part=8, title=r"Brain training",
    claim="Practising brain-training games improves abilities that were not practised.",
    original=Study("Jaeggi and colleagues", 2008, n="a few dozen students", design="training on one memory task, "
                                                                                   "tested on a reasoning test",
                   found="gains on the reasoning test that grew with the amount of training"),
    status="failed",
    record=(Study("Owen and colleagues", 2010, n="11,430 adults", design="six weeks of online training, randomized",
                  found="better at every trained task; no transfer to untrained ones"),
            Study("Simons and colleagues", 2016, n="132 cited articles", design="a review of the evidence the "
                                                                                "companies cite",
                  found="little evidence of broad transfer; weak controls and small samples")),
    note="People get better at what they practise. The claim that fails is that this carries over to memory, "
         "attention or intelligence in general.",
    sources=("S. M. Jaeggi et al., Improving fluid intelligence with training on working memory, PNAS 105 (2008) "
             "6829-6833",
             "A. M. Owen et al., Putting brain training to the test, Nature 465 (2010) 775-778",
             "D. J. Simons et al., Do 'brain-training' programs work?, Psychological Science in the Public "
             "Interest 17 (2016) 103-186"),
    checked="2026-11-14",
    data=("OWEN_2010",),
))

add(Finding(
    key="fmri_lie_detection", part=8, title=r"Lie detection by brain scan",
    claim="A brain scan can tell whether a particular person is lying.",
    original=Study("Kozel and colleagues", 2005, n="volunteers told to lie about a mock theft",
                   design="each person classified from their own scan",
                   found="most volunteers classified correctly, in the laboratory"),
    status="not directly tested",
    record=(Study("Ganis and colleagues", 2011, n="26 volunteers", design="the same kind of test, with and without "
                                                                          "a covert countermeasure",
                  found="100% detected without the countermeasure, 33% with it"),),
    note="Never tested where it would be used: on people with something at stake who do not want to be read. A "
         "United States court excluded it in 2010, and the appeal court agreed in 2012.",
    sources=("F. A. Kozel et al., Detecting deception using functional magnetic resonance imaging, Biological "
             "Psychiatry 58 (2005) 605-613",
             "G. Ganis et al., Lying in the scanner, NeuroImage 55 (2011) 312-319",
             "United States v. Semrau, 693 F.3d 510 (6th Cir. 2012)"),
    checked="2026-11-14",
    data=("GANIS_2011",),
))

shown(8, "BENNETT_2009", "a demonstration of a statistical error, not a claim about the mind")
shown(8, "HUBEL_WIESEL_1959", "told as the history of a method; orientation selectivity's row (orientation_cells) is "
      "entered in Part 13")
shown(8, "BERGER_1929", "the history of an instrument")
shown(8, "OGAWA_1990", "the physics of a measurement")
shown(8, "LOGOTHETIS_2001", "what a measurement follows; physiology, not a claim about the mind")
shown(8, "BOYNTON_1996", "a property of the measurement, used as a model")
shown(8, "EKLUND_2016", "a result about a statistical method")
shown(8, "VUL_2009", "a result about a method of analysis; the simulation beside it is the series' own")
shown(8, "POLDRACK_2006", "an argument about inference, with its own numbers shown")
shown(8, "KANWISHER_1997", "shown as the example of a robust activation with a disputed reading; its row "
      "(face_area) is entered in Part 14")
shown(8, "BARKER_1985", "the history of an instrument")
shown(8, "MAREK_2022", "a methods result at the frontier, disputed in its details", row_in=43)
shown(8, "ELLIOTT_2020", "a methods result at the frontier")
shown(8, "TANG_2023", "one laboratory's result at the frontier, described without figures")

# ---------------------------------------------------------------------------------------------------------------
# Part 9: genes and evolution
# ---------------------------------------------------------------------------------------------------------------
add(Finding(
    key="twin_heritability", part=9, title=r"Twins and the heritability of psychological traits",
    claim="On almost every psychological trait, identical twins are more alike than fraternal twins.",
    original=Study("Bouchard and McGue", 1981, n="111 studies, 113,942 pairings of relatives",
                   design="a review of correlations in intelligence-test scores",
                   found="identical twins raised together correlate .86, fraternal twins less"),
    status="replicated",
    record=(Study("Polderman and colleagues", 2015, n="14.5 million twin pairs, 17,804 traits",
                  design="a meta-analysis of fifty years of twin studies",
                  found="a mean heritability of 49%; almost no trait at zero"),),
    note="What repeats is the pattern of correlations. Reading it as a share for genes rests on the twin design's "
         "assumptions, and the share describes a population in its environments, not a person.",
    sources=("T. J. Bouchard and M. McGue, Familial studies of intelligence: a review, Science 212 (1981) 1055-1059",
             "T. J. C. Polderman et al., Meta-analysis of the heritability of human traits based on fifty years of "
             "twin studies, Nature Genetics 47 (2015) 702-709"),
    checked="2026-11-14",
    data=("BOUCHARD_MCGUE_1981", "POLDERMAN_2015"),
))

add(Finding(
    key="candidate_genes", part=9, title=r"Candidate genes for behaviour",
    claim="Common variants in a few named genes explain who becomes depressed after stress, or who scores higher "
          "on tests.",
    original=Study("Caspi and colleagues", 2003, n="a birth cohort in Dunedin, New Zealand",
                   design="a serotonin-transporter variant, stressful life events and depression",
                   found="more depression after stress in carriers of the short version"),
    status="failed",
    record=(Study("Risch and colleagues", 2009, n="14 studies, more than 14,000 people",
                  design="a meta-analysis of the same interaction",
                  found="no association, with or without stress"),
            Study("Chabris and colleagues", 2012, n="three samples, 9,771 people",
                  design="12 published variants for intelligence, retested",
                  found="1 of 32 tests significant; 10 to 15 expected if the effects were real"),
            Study("Border and colleagues", 2019, n="up to 443,264 people",
                  design="18 candidate genes for depression, preregistered",
                  found="no support for any of them, alone or with stress")),
    note="A 2011 meta-analysis of 54 studies found the interaction again; the large preregistered tests did not. "
         "Small samples, flexible analyses and selective publication: Part 4's mechanism.",
    sources=("A. Caspi et al., Influence of life stress on depression: moderation by a polymorphism in the 5-HTT "
             "gene, Science 301 (2003) 386-389",
             "N. Risch et al., Interaction between the serotonin transporter gene (5-HTTLPR), stressful life events, "
             "and risk of depression, JAMA 301 (2009) 2462-2471",
             "C. F. Chabris et al., Most reported genetic associations with general intelligence are probably false "
             "positives, Psychological Science 23 (2012) 1314-1323",
             "R. Border et al., No support for historical candidate gene or candidate gene-by-interaction hypotheses "
             "for major depression across multiple large samples, American Journal of Psychiatry 176 (2019) 376-387"),
    checked="2026-11-14",
    data=("CASPI_2003", "CHABRIS_2012", "BORDER_2019"),
))

add(Finding(
    key="education_polygenic_score", part=9, title=r"A polygenic score for years of schooling",
    claim="A score added up from many common gene variants predicts how far a person goes in school.",
    original=Study("Rietveld and colleagues", 2013, n="126,559 people", design="a genome-wide association study",
                   found="three variants; a score from all variants predicts about 2% of the variation"),
    status="replicated",
    record=(Study("Lee and colleagues", 2018, n="1.1 million people", design="a genome-wide association study",
                  found="1,271 variants; a score predicts 11 to 13%; effects about 40% smaller within families"),
            Study("Okbay and colleagues", 2022, n="3 million people", design="a genome-wide association study",
                  found="3,952 variants; a score predicts 12 to 16%")),
    note="It predicts the averages of groups far better than it predicts a person; part of it is the parents' genes "
         "acting through the home; and it predicts poorly in people whose ancestry differs from the samples it was "
         "built on.",
    sources=("C. A. Rietveld et al., GWAS of 126,559 individuals identifies genetic variants associated with "
             "educational attainment, Science 340 (2013) 1467-1471",
             "J. J. Lee et al., Gene discovery and polygenic prediction from a genome-wide association study of "
             "educational attainment in 1.1 million individuals, Nature Genetics 50 (2018) 1112-1121",
             "A. Okbay et al., Polygenic prediction of educational attainment within and between families from "
             "genome-wide association analyses in 3 million individuals, Nature Genetics 54 (2022) 437-449"),
    checked="2026-11-14",
    data=("RIETVELD_2013", "LEE_2018"),
))

shown(9, "BOUCHARD_1990", "an anecdote and the study it began; its figure is quoted as that study's own")
shown(9, "GALTON_1875", "the history of a question")
shown(9, "FISHER_1918", "theory, checked here by simulation")
shown(9, "TURKHEIMER_2000", "a summary of a literature; the evidence is the row on twin heritability")
shown(9, "TURKHEIMER_2003", "one study with mixed replications, shown as the example of a heritability that depends "
                            "on the environment", row_in=32)
shown(9, "HAWORTH_2010", "a description of how an estimate changes with age", row_in=32)
shown(9, "NCD_RISC_2016", "a description of populations")
shown(9, "HERITABILITY_TABLE", "meta-analytic values; the evidence is the row on twin heritability")
shown(9, "KONG_2018", "a methods result at the frontier")
shown(9, "HOWE_2022", "a methods result at the frontier")
shown(9, "YENGO_2022", "a result about height, set beside the twin estimate")
shown(9, "MARTIN_2019", "a methods result at the frontier")
shown(9, "KARAVANI_2019", "a simulation study, set beside the series' own formula")
shown(9, "BUSS_1989", "the example of a cross-cultural test; its claim is entered with mate preferences", row_in=37)
shown(9, "HEIJMANS_2008", "physiology, told with its limits")
shown(9, "WEIR_2002", "comparative cognition, told with its later qualification")

# ---------------------------------------------------------------------------------------------------------------
# Part 10: chemistry and clocks
# ---------------------------------------------------------------------------------------------------------------
add(Finding(
    key="rem_sleep", part=10, title=r"REM sleep and dreaming",
    claim="Sleep contains recurring periods of rapid eye movement, and people woken from them usually report a "
          "dream.",
    original=Study("Aserinsky and Kleitman", 1953, n="27 awakenings during eye movements",
                   design="sleepers woken during eye movements and during ocular quiet",
                   found="20 of 27 awakenings during eye movements gave detailed dream reports"),
    status="replicated",
    record=(Study("Sleep laboratories since", 1957, n="thousands of recorded nights",
                  design="all-night recordings of the EEG, eye movements and muscle tone",
                  found="the same stages, in cycles of about ninety minutes, in every laboratory"),),
    note="The stages are among the most repeated observations in psychology. That dreaming happens only in REM "
         "did not hold: dreams are also reported from other stages, less often and less vividly.",
    sources=("E. Aserinsky and N. Kleitman, Regularly occurring periods of eye motility, and concomitant phenomena, "
             "during sleep, Science 118 (1953) 273-274",
             "W. Dement and N. Kleitman, Cyclic variations in EEG during sleep and their relation to eye movements, "
             "body motility, and dreaming, Electroencephalography and Clinical Neurophysiology 9 (1957) 673-690"),
    checked="2026-11-14",
    data=("ASERINSKY_1953",),
))

add(Finding(
    key="sleep_loss_vigilance", part=10, title=r"Sleep loss and attention",
    claim="Too little sleep, night after night, impairs sustained attention, and the impairment accumulates.",
    original=Study("Van Dongen and colleagues", 2003, n="adults kept in a laboratory for two weeks",
                   design="8, 6 or 4 hours in bed for 14 days, or none for 3, assigned at random",
                   found="lapses grew day by day; 6 hours for two weeks matched up to two nights without sleep"),
    status="replicated",
    record=(Study("Belenky and colleagues", 2003, n="66 adults", design="3, 5, 7 or 9 hours in bed for a week",
                  found="a graded decline in a vigilance task; on 5 and 7 hours it levelled off at a lower level"),),
    note="People rated themselves only slightly sleepy while their performance kept falling: the loss is not "
         "noticed by the person who has it.",
    sources=("H. P. A. Van Dongen, G. Maislin, J. M. Mullington and D. F. Dinges, The cumulative cost of additional "
             "wakefulness, Sleep 26 (2003) 117-126",
             "G. Belenky et al., Patterns of performance degradation and restoration during sleep restriction and "
             "subsequent recovery, Journal of Sleep Research 12 (2003) 1-12"),
    checked="2026-11-14",
    data=("VAN_DONGEN_2003",),
))

add(Finding(
    key="sleep_memory", part=10, title=r"Sleep and the consolidation of memory",
    claim="Reactivating a memory during slow-wave sleep strengthens it.",
    original=Study("Rasch and colleagues", 2007, n="a few dozen volunteers",
                   design="an odour present while learning card locations, given again in slow-wave sleep",
                   found="better memory the next morning; not when given in REM sleep or while awake"),
    status="replicated, smaller",
    record=(Study("Hu and colleagues", 2020, n="91 experiments, 2,004 people", design="a meta-analysis of cueing in sleep",
                  found="a small effect in non-REM sleep (g = 0.29); none in REM sleep or waking"),),
    note="The effect is there and small. For a neighbouring method, sounds timed to slow waves, reported effects "
         "have shrunk year by year.",
    sources=("B. Rasch, C. Buchel, S. Gais and J. Born, Odor cues during slow-wave sleep prompt declarative memory "
             "consolidation, Science 315 (2007) 1426-1429",
             "X. Hu, L. Y. Cheng, M. H. Chiu and K. A. Paller, Promoting memory consolidation during sleep: a "
             "meta-analysis of targeted memory reactivation, Psychological Bulletin 146 (2020) 218-244"),
    checked="2026-11-14",
    data=("RASCH_2007",),
))

add(Finding(
    key="short_sleep_mortality", part=10, title=r"Short sleep and an early death",
    claim="Sleeping too little shortens your life.",
    original=Study("Cappuccio and colleagues", 2010, n="16 studies, 1.4 million people",
                   design="a meta-analysis of cohorts who reported their usual sleep and were followed for years",
                   found="short sleepers 12% more likely to die in the follow-up; long sleepers 30% more likely"),
    status="contested",
    record=(),
    note="The association is real and the causal reading is not established. Sleep was self-reported, illness "
         "changes sleep before it kills, and long sleep predicts death more strongly than short sleep, which a "
         "simple story about sleep loss does not expect.",
    sources=("F. P. Cappuccio, L. D'Elia, P. Strazzullo and M. A. Miller, Sleep duration and all-cause mortality: a "
             "systematic review and meta-analysis of prospective studies, Sleep 33 (2010) 585-592",),
    checked="2026-11-14",
    data=("CAPPUCCIO_2010",),
))

shown(10, "KLEITMAN_1938", "an experiment on two people, told as history; the clock's period is the next entry")
shown(10, "CZEISLER_1999", "physiology: a property of the body's clock, not a claim about the mind")
shown(10, "BORBELY_1982", "a model, tested here against its own predictions")
shown(10, "HOBSON_1977", "two theories of dreaming, presented as an open dispute", row_in=27)
shown(10, "SIEGEL_1982", "an animal experiment on tolerance; its row is entered with conditioning, in Part 16")
shown(10, "SOLOMON_CORBIT_1974", "a theory, shown as a model", row_in=41)
shown(10, "DUNSTER_2018", "a before-and-after comparison in two schools, described as that")
shown(10, "TRAUER_2015", "a meta-analysis of a treatment; therapies are entered in Part 42", row_in=42)
shown(10, "XIE_2013", "a finding in mice and its dispute, at the frontier")
shown(10, "PHOENIX_1959", "animal physiology; the human evidence is indirect and is said to be")
shown(10, "TEIGEN_1994", "a history of a textbook law; the law itself is examined in Part 28", row_in=28)
shown(10, "ROENNEBERG_2004", "a description from a survey of sleep times; the lifespan is Part 31", row_in=31)


# ---------------------------------------------------------------------------------------------------------------
# Part 11: the threshold
# ---------------------------------------------------------------------------------------------------------------
add(Finding(
    key="weber_law", part=11, title=r"Weber's law",
    claim="The smallest noticeable change in a stimulus is a constant fraction of its size.",
    original=Study("Weber", 1834, n="Weber and a few colleagues", design="lifted weights, touch and line length, "
                   "compared in pairs", found="the noticeable difference grew in proportion to the standard"),
    status="replicated",
    record=(Study("Fechner", 1860, n="years of his own judgments", design="lifted weights, brightness and distances, "
                  "by three methods", found="a roughly constant fraction over the middle of each range"),
            Study("McGill and Goldberg", 1968, n="a few listeners", design="intensity discrimination of pure tones",
                  found="a near miss: the fraction falls slowly as the tone gets louder")),
    note="It holds over the middle of most ranges and fails at the edges: near the absolute threshold the fraction "
         "grows, and for loud tones it shrinks a little. The fraction differs from sense to sense.",
    sources=("E. H. Weber, De Pulsu, Resorptione, Auditu et Tactu (1834); Der Tastsinn und das Gemeingefuehl (1846)",
             "G. T. Fechner, Elemente der Psychophysik (1860)",
             "W. J. McGill and J. P. Goldberg, A study of the near-miss involving Weber's law and pure-tone intensity "
             "discrimination, Perception & Psychophysics 4 (1968) 105-109"),
    checked="2026-11-14",
    data=("WEBER_1834", "FECHNER_1860", "MCGILL_GOLDBERG_1968"),
))

add(Finding(
    key="stevens_power_law", part=11, title=r"Stevens's power law",
    claim="Judged magnitude grows as a power of stimulus intensity.",
    original=Study("Stevens", 1957, n="many small groups of observers", design="magnitude estimation: say a number "
                   "for each stimulus", found="straight lines on log-log axes, exponents from 0.33 to 3.5"),
    status="replicated",
    record=(Study("Poulton", 1968, n="a review of magnitude-estimation studies", design="the same continua under "
                  "different ranges, standards and orders", found="the power form repeats; the exponent moves with "
                  "the range and the order of the stimuli"),),
    note="The power form is among the most repeated results in psychophysics. The exponents are not constants of "
         "the senses: they shift with the range presented, the first stimulus and the numbers people like to use.",
    sources=("S. S. Stevens, On the psychophysical law, Psychological Review 64 (1957) 153-181",
             "E. C. Poulton, The new psychophysics: six models for magnitude estimation, Psychological Bulletin 69 "
             "(1968) 1-19"),
    checked="2026-11-14",
    data=("STEVENS_1957", "POULTON_1968"),
))

shown(11, "LEVITT_1971", "a method, derived and checked on Psyche")
shown(11, "WATSON_PELLI_1983", "a method, run on Psyche")
shown(11, "WICHMANN_HILL_2001", "a method, applied to simulated data")
shown(11, "HALBERDA_2008", "Weber's law for number, a preview; number sense is entered in Part 30", row_in=30)
shown(11, "GIBBON_1977", "Weber's law for time, shown as a pattern; the series does not study interval timing")
shown(11, "LESMES_2010", "a method at the frontier; its row (csf_channels) is entered in Part 13")
shown(11, "DEVRIES_ROSE", "a theory of the threshold, run on Psyche; its row (few_quanta) is entered in Part 13")
shown(11, "BERNOULLI_1738", "a theory of value, a preview; choices under risk are entered in Part 26", row_in=26)
shown(11, "PLATEAU_1872", "a historical proposal; the power law's row is Stevens's")
shown(11, "THURSTONE_1927", "a method, run on simulated judges; scaling judgments is entered in Part 46", row_in=46)

# ------------------------------------------------------------------------------------------- Part 12: signal and noise
add(Finding(
    key="criterion_shift", part=12, title=r"The criterion moves; the sensitivity stays",
    claim="Changing the payoffs or the base rate of signals moves where an observer says yes, while the observer's "
          "sensitivity stays the same.",
    original=Study("Tanner and Swets", 1954, n="a few trained observers", design="visual detection of a faint "
                   "spot under different instructions and probabilities", found="the yes rate for signals and for "
                   "blanks moved together along one curve, as a decision model predicts"),
    status="replicated",
    record=(Study("Swets, Tanner and Birdsall", 1961, n="trained observers", design="payoffs and a priori "
                  "probabilities varied, and confidence ratings", found="points from payoffs, probabilities and "
                  "ratings fall on one ROC"),
            Study("Green and Swets", 1966, n="a review of many laboratories", design="detection in vision and "
                  "hearing", found="the separation of sensitivity and criterion holds across senses and tasks")),
    note="The separation is the foundation of detection theory and holds wherever it has been tested in the "
         "laboratory. Observers do move their criterion, but usually not as far as an ideal observer would.",
    sources=("W. P. Tanner Jr. and J. A. Swets, A decision-making theory of visual detection, Psychological Review "
             "61 (1954) 401-409",
             "J. A. Swets, W. P. Tanner Jr. and T. G. Birdsall, Decision processes in perception, Psychological "
             "Review 68 (1961) 301-340",
             "D. M. Green and J. A. Swets, Signal Detection Theory and Psychophysics (1966)"),
    checked="2026-11-14",
    data=("TANNER_SWETS_1954", "SWETS_1961"),
))

add(Finding(
    key="prevalence_effect", part=12, title=r"The prevalence effect",
    claim="When targets are rare, searchers miss more of them.",
    original=Study("Wolfe, Horowitz and Kenner", 2005, n="observers in a laboratory search", design="a tool hidden "
                   "among overlapping objects, like a baggage X-ray, present on 50%, 10% or 1% of displays", found="misses rose from 11% to 25% "
                   "to 52% as targets grew rare; false alarms stayed rare"),
    status="replicated",
    record=(Study("Fleck and Mitroff", 2007, n="observers in the same kind of search", design="observers allowed "
                  "to correct a response they had just made", found="most of the extra misses disappeared: they "
                  "were responses given too quickly, not targets unseen"),),
    note="Rare targets are missed more often in laboratory search after laboratory search. Why is argued: "
         "a criterion that moves toward 'absent', searches that end too soon, and responses given too fast all "
         "contribute.",
    sources=("J. M. Wolfe, T. S. Horowitz and N. M. Kenner, Rare items often missed in visual searches, Nature 435 "
             "(2005) 439-440",
             "M. S. Fleck and S. R. Mitroff, Rare targets are rarely missed in correctable search, Psychological "
             "Science 18 (2007) 943-947"),
    checked="2026-11-14",
    data=("WOLFE_2005", "FLECK_MITROFF_2007"),
))

add(Finding(
    key="zroc_slope", part=12, title=r"Recognition's zROC slope",
    claim="In recognition memory the z-transformed ROC has a slope below one, about 0.8: the evidence for studied "
          "items varies more than the evidence for new ones.",
    original=Study("Ratcliff, Sheu and Gronlund", 1992, n="several experiments", design="old-new recognition with "
                   "confidence ratings", found="zROC slopes near 0.8, fairly constant across conditions"),
    status="replicated",
    record=(Study("Yonelinas", 1994, n="three experiments", design="recognition ROCs fitted by rival models",
                  found="the curved, asymmetric ROC is also fitted by a mixture of recollection and familiarity"),),
    note="The slope below one repeats in study after study. What it means is argued: unequal variances, or a "
         "threshold-like recollection added to graded familiarity. The slope also falls as memory gets stronger.",
    sources=("R. Ratcliff, C.-F. Sheu and S. D. Gronlund, Testing global memory models using ROC curves, "
             "Psychological Review 99 (1992) 518-535",
             "A. P. Yonelinas, Receiver-operating characteristics in recognition memory: evidence for a dual-process "
             "model, Journal of Experimental Psychology: Learning, Memory, and Cognition 20 (1994) 1341-1354"),
    checked="2026-11-14",
    data=("RATCLIFF_1992", "YONELINAS_1994"),
))

shown(12, "MACKWORTH_1948", "the vigilance decrement, told as the story that started the field; vigilance is entered "
      "in Part 51", row_in=51)
shown(12, "SEE_1995", "a meta-analysis shown for its conclusion about the watch; vigilance is entered in Part 51",
      row_in=51)
shown(12, "GIGERENZER_HOFFRAGE_1995", "base-rate reasoning, a preview; judgment under uncertainty is entered in "
      "Part 26", row_in=26)
shown(12, "MANISCALCO_LAU_2012", "a method at the frontier; confidence is entered in Part 25", row_in=25)
shown(12, "SWETS_2000", "a review of applications, not a finding")
shown(12, "MICKES_2012", "line-ups, a preview of a live dispute; eyewitness memory is entered in Part 21", row_in=21)

# ---------------------------------------------------------------------------------------------------------------
# Part 13: The Eye and the Code
# ---------------------------------------------------------------------------------------------------------------
add(Finding(
    key="few_quanta", part=13, title=r"A handful of quanta",
    claim="A fully dark-adapted eye sees a dim flash when only a handful of quanta, roughly five to fourteen, are "
          "absorbed by its rods, spread so thinly that a rod must respond to a single quantum.",
    original=Study("Hecht, Shlaer and Pirenne", 1942, n="a few trained observers, mostly the authors",
                   design="frequency of seeing for brief flashes of 510 nm light after 40 minutes in the dark",
                   found="54 to 148 quanta at the cornea, 5 to 14 absorbed; the curves' slopes gave 5 to 8"),
    status="replicated",
    record=(Study("Baylor, Lamb and Yau", 1979, n="toad rods", design="suction-electrode recordings from single rods",
                  found="one absorbed photon gives a current of about 1 pA, 5% of the dark current"),
            Study("Tinsley et al.", 2016, n="a few observers, 30,767 trials", design="single photons from a quantum "
                  "source; two-interval forced choice with confidence",
                  found="51.6% correct on single-photon trials (P = 0.0545); 60% on high-confidence trials")),
    note="That a few absorbed quanta suffice, and that a rod responds to one, is settled physiology and has been "
         "repeated many times. Whether a person can report a single photon rests on one study whose overall result "
         "was at the edge of significance; it has not been directly repeated.",
    sources=("S. Hecht, S. Shlaer and M. H. Pirenne, Energy, quanta, and vision, Journal of General Physiology 25 "
             "(1942) 819-840",
             "D. A. Baylor, T. D. Lamb and K.-W. Yau, Responses of retinal rods to single photons, Journal of "
             "Physiology 288 (1979) 613-634",
             "J. N. Tinsley et al., Direct detection of a single photon by humans, Nature Communications 7 (2016) "
             "12172"),
    checked="2026-11-14",
    data=("HECHT_1942", "BAYLOR_1979", "TINSLEY_2016", "DEVRIES_ROSE"),
))

add(Finding(
    key="rate_code", part=13, title=r"Intensity as a rate",
    claim="A single sensory fibre signals the strength of a stimulus by how often it fires, not by the size of its "
          "impulses, and its rate falls during a steady stimulus.",
    original=Study("Adrian and Zotterman", 1926, n="frog muscle preparations", design="one stretch receptor isolated "
                   "by cutting the muscle down; weights hung from it",
                   found="impulses of fixed size whose frequency rose with the load and fell as the load stayed on"),
    status="replicated",
    record=(Study("Hartline and Graham", 1932, n="Limulus", design="a single optic nerve fibre from one ommatidium",
                  found="brighter light, a faster rate; the size of the impulses unchanged"),),
    note="Rate coding and adaptation have been found in every sense since. Rate is not the only code: the timing of "
         "the first spike and the pattern across many fibres carry information too.",
    sources=("E. D. Adrian and Y. Zotterman, The impulses produced by sensory nerve-endings. Part II. The response of "
             "a single end-organ, Journal of Physiology 61 (1926) 151-171",
             "H. K. Hartline and C. H. Graham, Nerve impulses from single receptors in the eye, Journal of Cellular "
             "and Comparative Physiology 1 (1932) 277-295"),
    checked="2026-11-14",
    data=("ADRIAN_1926",),
))

add(Finding(
    key="orientation_cells", part=13, title=r"Cells tuned to orientation",
    claim="Neurons in primary visual cortex respond best to an edge or bar at one orientation, and simple cells' "
          "fields are built from aligned centre-surround inputs.",
    original=Study("Hubel and Wiesel", 1959, n="cats", design="single cells in striate cortex, stimulated with spots "
                   "and slits of light", found="cells driven only by a line at a particular orientation and position"),
    status="replicated",
    record=(Study("Hubel and Wiesel", 1968, n="monkeys", design="single cells in striate cortex",
                  found="orientation tuning, simple and complex cells, as in the cat"),
            Study("Reid and Alonso", 1995, n="cats", design="paired recordings from thalamus and cortex",
                  found="thalamic cells connect to simple cells whose subregions they overlap, of the same sign")),
    note="Orientation tuning has been confirmed in every mammal with a visual cortex that has been studied. The "
         "hierarchy (centre-surround, simple, complex) holds as a first approximation; much of what these cells do "
         "with natural scenes is not yet explained by it.",
    sources=("D. H. Hubel and T. N. Wiesel, Receptive fields of single neurones in the cat's striate cortex, Journal "
             "of Physiology 148 (1959) 574-591",
             "D. H. Hubel and T. N. Wiesel, Receptive fields and functional architecture of monkey striate cortex, "
             "Journal of Physiology 195 (1968) 215-243",
             "S. W. Kuffler, Discharge patterns and functional organization of mammalian retina, Journal of "
             "Neurophysiology 16 (1953) 37-68",
             "R. C. Reid and J.-M. Alonso, Specificity of monosynaptic connections from thalamus to visual cortex, "
             "Nature 378 (1995) 281-284"),
    checked="2026-11-14",
    data=("HUBEL_WIESEL_1959", "KUFFLER_1953"),
))

add(Finding(
    key="csf_channels", part=13, title=r"The CSF and its channels",
    claim="Sensitivity to contrast is band-pass, peaking at a few cycles per degree, and adapting to one grating "
          "lowers sensitivity mainly near its own frequency and orientation.",
    original=Study("Campbell and Robson", 1968, n="a few observers", design="contrast thresholds for sine and square "
                   "gratings", found="a band-pass contrast sensitivity function; thresholds predicted from Fourier "
                   "components"),
    status="replicated",
    record=(Study("Blakemore and Campbell", 1969, n="2 observers", design="thresholds after adapting to a "
                  "high-contrast grating", found="up to a fivefold rise in threshold near the adapting frequency"),
            Study("Lesmes et al.", 2010, n="observers and simulations", design="a four-parameter CSF estimated "
                  "adaptively", found="the band-pass shape recovered in about fifty trials")),
    note="The shape is one of the best-replicated curves in vision and is used to test eyes in clinics. Whether the "
         "'channels' are separate mechanisms or a convenient description of a continuum is still discussed.",
    sources=("F. W. Campbell and J. G. Robson, Application of Fourier analysis to the visibility of gratings, Journal "
             "of Physiology 197 (1968) 551-566",
             "C. Blakemore and F. W. Campbell, On the existence of neurones in the human visual system selectively "
             "sensitive to the orientation and size of retinal images, Journal of Physiology 203 (1969) 237-260",
             "L. A. Lesmes, Z.-L. Lu, J. Baek and T. D. Albright, Bayesian adaptive estimation of the contrast "
             "sensitivity function: the quick CSF method, Journal of Vision 10(3) (2010) 17"),
    checked="2026-11-14",
    data=("CAMPBELL_ROBSON_1968", "BLAKEMORE_CAMPBELL_1969", "LESMES_2010"),
))

add(Finding(
    key="dress_illuminant", part=13, title=r"The dress",
    claim="People who see the dress as white and gold, rather than blue and black, are assuming that it is lit by "
          "bluish light, and discount it.",
    original=Study("Lafer-Sousa, Hermann and Conway", 2015, n="about 1,400 online", design="a survey with colour "
                   "matching; the image shown at several sizes",
                   found="57% blue-black, 30% white-gold, 11% blue-brown; reports followed assumed illumination"),
    status="replicated",
    record=(Study("Wallisch", 2017, n="8,084 and 5,333 online", design="two surveys asking what people saw and "
                  "how they thought the dress was lit", found="those who assumed shade saw white and gold more often"),
            Study("Witzel, Racey and O'Regan", 2017, n="online and laboratory samples", design="colour reports "
                  "against assumed illumination", found="perceived colour moved opposite to the assumed light along "
                  "the daylight axis")),
    note="Three groups, using different methods, tie the split to assumptions about the light. Why people differ "
         "in those assumptions (age, time spent in daylight) is less settled, and the effects found are modest.",
    sources=("R. Lafer-Sousa, K. L. Hermann and B. R. Conway, Striking individual differences in color perception "
             "uncovered by 'the dress' photograph, Current Biology 25 (2015) R545-R546",
             "P. Wallisch, Illumination assumptions account for individual differences in the perceptual "
             "interpretation of a profoundly ambiguous stimulus in the color domain: 'The dress', Journal of Vision "
             "17(4) (2017) 5",
             "C. Witzel, C. Racey and J. K. O'Regan, The most reasonable explanation of 'the dress': implicit "
             "assumptions about illumination, Journal of Vision 17(2) (2017) 1"),
    checked="2026-11-14",
    data=("LAFER_SOUSA_2015",),
))

shown(13, "JORDAN_2010", "one exceptional observer, shown at the frontier as a possibility, not a general finding")
shown(13, "MILNER_1991", "a single patient, told as the case that founded a theory; vision without awareness, with "
      "blindsight, is entered in Part 27", row_in=27)
shown(13, "COLOUR_TABLES", "standard tables, the measurements on which colour science is built, not a finding")
shown(13, "OKABE_ITO", "a design recommendation, not a finding")

# ---------------------------------------------------------------------------------------------------------------
# Part 14: Seeing as Inference
# ---------------------------------------------------------------------------------------------------------------
add(Finding(
    key="cue_combination", part=14, title=r"Cues weighted by reliability",
    claim="When two senses report the same property, people combine them roughly as an optimal observer would: each "
          "cue weighted by its reliability, and the combined estimate less variable than either alone.",
    original=Study("Ernst and Banks", 2002, n="4 observers", design="the height of a ridge, seen and felt, with noise "
                   "added to the visual display", found="weights and combined thresholds close to the maximum-likelihood "
                   "prediction from each sense alone"),
    status="replicated",
    record=(Study("Alais and Burr", 2004, n="a few observers", design="locating flashes and clicks",
                  found="the ventriloquist effect follows near-optimal combination of vision and hearing"),
            Study("Rahnev and Denison", 2018, n="a review", design="the literature on optimality in perception",
                  found="many documented departures from optimality, cue combination included")),
    note="Reliability-weighted combination has been found across many pairs of senses and cues. It is not universal: "
         "children combine some cues later in development, and the review lists many conditions in which observers "
         "fall short of the optimal weights.",
    sources=("M. O. Ernst and M. S. Banks, Humans integrate visual and haptic information in a statistically optimal "
             "fashion, Nature 415 (2002) 429-433",
             "D. Alais and D. Burr, The ventriloquist effect results from near-optimal bimodal integration, Current "
             "Biology 14 (2004) 257-262",
             "D. Rahnev and R. N. Denison, Suboptimality in perceptual decision making, Behavioral and Brain Sciences "
             "41 (2018) e223"),
    checked="2026-11-14",
    data=("ERNST_BANKS_2002", "ALAIS_BURR_2004", "RAHNEV_DENISON_2018"),
))

add(Finding(
    key="contrast_speed", part=14, title=r"Low contrast looks slower",
    claim="A moving pattern of low contrast looks slower than the same pattern at high contrast.",
    original=Study("Thompson", 1982, n="a few observers", design="matching the speeds of gratings of different "
                   "contrast", found="lower contrast, lower perceived speed, at least below about 8 cycles a second"),
    status="replicated",
    record=(Study("Weiss, Simoncelli and Adelson", 2002, n="model and demonstrations", design="an ideal observer with a "
                  "prior favouring slow speeds", found="the slowing, and several other motion illusions, predicted"),),
    note="The slowing at low contrast is robust for slow and moderate speeds; at high temporal frequencies the results "
         "are mixed, and some studies find low contrast speeding things up.",
    sources=("P. Thompson, Perceived rate of movement depends on contrast, Vision Research 22 (1982) 377-380",
             "Y. Weiss, E. P. Simoncelli and E. H. Adelson, Motion illusions as optimal percepts, Nature Neuroscience "
             "5 (2002) 598-604",
             "P. Thompson, K. Brooks and S. T. Hammett, Speed can go up as well as down at low contrast, Vision "
             "Research 46 (2006) 782-786"),
    checked="2026-11-14",
    data=("THOMPSON_1982", "WEISS_2002"),
))

add(Finding(
    key="muller_lyer_culture", part=14, title=r"The Müller-Lyer illusion and culture",
    claim="The Müller-Lyer illusion is much weaker in people who grow up without rectangular buildings.",
    original=Study("Segall, Campbell and Herskovits", 1966, n="over a dozen societies", design="choosing which of two "
                   "lines looked longer", found="large differences; San foragers least susceptible, European-derived "
                   "samples most"),
    status="contested",
    record=(Study("Gandhi, Kalia, Ganesh and Sinha", 2015, n="newly sighted children aged 8 to 16",
                  design="the Ponzo and Müller-Lyer figures, within 48 hours of cataract surgery",
                  found="both illusions at once, without visual experience of corners"),
            Study("Amir and Firestone", 2025, n="a review", design="the cross-cultural and comparative evidence",
                  found="the original differences may reflect method; the illusion appears in many animals")),
    note="That the illusion itself is real is not in doubt. Whether its size depends on a carpentered environment is "
         "now disputed, and the original study has not been repeated with modern methods.",
    sources=("M. H. Segall, D. T. Campbell and M. J. Herskovits, The Influence of Culture on Visual Perception "
             "(Bobbs-Merrill, 1966)",
             "T. Gandhi, A. Kalia, S. Ganesh and P. Sinha, Immediate susceptibility to visual illusions after sight "
             "onset, Current Biology 25 (2015) R358-R359",
             "D. Amir and C. Firestone, Is visual perception WEIRD? The Müller-Lyer illusion and the cultural "
             "byproduct hypothesis, Psychological Review (2025)"),
    checked="2026-11-14",
    data=("SEGALL_1966", "AMIR_FIRESTONE_2025"),
))

add(Finding(
    key="face_area", part=14, title=r"The fusiform face area",
    claim="A region of the fusiform gyrus responds much more to faces than to other objects, in most people tested.",
    original=Study("Kanwisher, McDermott and Chun", 1997, n="15 people", design="fMRI to faces, objects, houses and "
                   "hands", found="a face-selective region in 12 of 15"),
    status="replicated",
    record=(Study("Gauthier et al.", 1999, n="a few observers", design="fMRI before and after training on novel "
                  "objects", found="the region's response to the trained objects rose with expertise"),),
    note="The region's face selectivity has been found in study after study. What it is selective for, faces as such "
         "or any category a person is expert in, is still argued.",
    sources=("N. Kanwisher, J. McDermott and M. M. Chun, The fusiform face area: a module in human extrastriate cortex "
             "specialized for face perception, Journal of Neuroscience 17 (1997) 4302-4311",
             "I. Gauthier, M. J. Tarr, A. W. Anderson, P. Skudlarski and J. C. Gore, Activation of the middle fusiform "
             "'face area' increases with expertise in recognizing novel objects, Nature Neuroscience 2 (1999) 568-573"),
    checked="2026-11-14",
    data=("KANWISHER_1997", "GAUTHIER_1999"),
))

shown(14, "ADELSON_1995", "a demonstration, redrawn and explained by a model; lightness is not a finding in dispute")
shown(14, "ADAMS_2004", "a single experiment showing that a prior can be retrained, told as an example")
shown(14, "YIN_1969", "a classic demonstration of the face inversion effect, told as history; faces are entered with the face area")
shown(14, "YAMINS_2014", "a modelling result at the frontier; deep networks as models are entered in Part 60", row_in=60)
shown(14, "GEIRHOS_2019", "a property of artificial networks, reproduced on a small one; not a finding about minds")
shown(14, "VONG_2024", "a modelling result at the frontier; learning from an infant's experience is entered in "
      "Part 30", row_in=30)
shown(14, "WHEATSTONE_1838", "the history of an instrument and a stimulus")

# ---------------------------------------------------------------------------------------------------------------
# Part 15: the other senses
# ---------------------------------------------------------------------------------------------------------------
add(Finding(
    key="mcgurk", part=15, title=r"The McGurk effect",
    claim="A voice saying one syllable, dubbed onto lips saying another, is often heard as a third syllable.",
    original=Study("McGurk and MacDonald", 1976, n="children and adults", design="a voice saying ba dubbed onto lips "
                   "saying ga", found="98% of adults reported hearing da or a blend"),
    status="replicated",
    record=(Study("Mallick, Magnotti and Beauchamp", 2015, n="hundreds of participants, many stimuli",
                  design="rates of the illusion across people, stimuli and a one-year retest",
                  found="from 0% to 100% across people, stable within a person"),),
    note="The illusion is easily reproduced, but its strength depends heavily on the person, the recording and the "
         "language: some people never experience it, and rates far below the original 98% are common.",
    sources=("H. McGurk and J. MacDonald, Hearing lips and seeing voices, Nature 264 (1976) 746-748",
             "D. B. Mallick, J. F. Magnotti and M. S. Beauchamp, Variability and stability in the McGurk effect, "
             "Psychonomic Bulletin & Review 22 (2015) 1299-1307"),
    checked="2026-11-14",
    data=("MCGURK_1976", "MALLICK_2015"),
))

add(Finding(
    key="categorical_speech", part=15, title=r"Categorical perception of speech",
    claim="Along a continuum of speech sounds, listeners discriminate pairs much better across a phoneme boundary than "
          "within a category.",
    original=Study("Liberman, Harris, Hoffman and Griffith", 1957, n="a few listeners", design="synthetic syllables from "
                   "b through d to g, identified and discriminated (ABX)", found="discrimination peaks at the "
                   "boundaries and is near chance within categories"),
    status="story and record",
    record=(Study("McMurray, Tanenhaus and Aslin", 2002, n="listeners' eye movements", design="a voice-onset-time "
                  "continuum and pictures of words", found="graded sensitivity to differences within a category"),),
    note="The peak at the boundary is robust. The textbook story, that listeners cannot hear differences within a "
         "category, is not: with sensitive measures, within-category differences are heard and used.",
    sources=("A. M. Liberman, K. S. Harris, H. S. Hoffman and B. C. Griffith, The discrimination of speech sounds within "
             "and across phoneme boundaries, Journal of Experimental Psychology 54 (1957) 358-368",
             "B. McMurray, M. K. Tanenhaus and R. N. Aslin, Gradient effects of within-category phonetic variation on "
             "lexical access, Cognition 86 (2002) B33-B42"),
    checked="2026-11-14",
    data=("LIBERMAN_1957", "MCMURRAY_2002"),
))

add(Finding(
    key="rubber_hand", part=15, title=r"The rubber hand illusion",
    claim="When a visible rubber hand and a person's hidden hand are stroked in synchrony, people feel the touch on the "
          "rubber hand and report that it feels like their own.",
    original=Study("Botvinick and Cohen", 1998, n="a small group", design="synchronous and asynchronous stroking of a "
                   "rubber hand and the hidden real hand", found="touch felt on the rubber hand; felt position drifts "
                   "toward it"),
    status="contested",
    record=(Study("Lush and colleagues", 2020, n="353 people", design="hypnotic suggestibility and illusion reports",
                  found="reports track a person's response to suggestion, raising the role of expectations"),),
    note="Synchronous stroking reliably produces higher ratings than asynchronous. Whether the ratings reflect a change "
         "in bodily experience, or partly what participants expect the experiment to produce, is now disputed.",
    sources=("M. Botvinick and J. Cohen, Rubber hands 'feel' touch that eyes see, Nature 391 (1998) 756",
             "P. Lush et al., Trait phenomenological control predicts experience of mirror synaesthesia and the rubber "
             "hand illusion, Nature Communications 11 (2020) 4853"),
    checked="2026-11-14",
    data=("BOTVINICK_COHEN_1998", "LUSH_2020"),
))

add(Finding(
    key="homunculus", part=15, title=r"The cortical homunculus",
    claim="The body is mapped in order along the strips of cortex either side of the central sulcus, with the hands, "
          "lips and tongue given far more cortex than the trunk.",
    original=Study("Penfield and Boldrey", 1937, n="126 patients", design="the exposed cortex stimulated with a weak "
                   "current in awake patients during surgery, 1928 to 1936",
                   found="tingling and movements in an orderly sequence of body parts; a distorted map"),
    status="replicated",
    record=(Study("Roux, Djidjeli and Durand", 2018, n="50 patients", design="stimulation of the postcentral gyrus during "
                  "surgery, sites placed in standard coordinates",
                  found="the medial-to-lateral order confirmed; some of Penfield's details, such as felt movement, not found"),
            Study("Gordon and colleagues", 2023, n="precision fMRI in several people, with large datasets",
                  design="the motor strip's functional connectivity",
                  found="the effector regions confirmed, interleaved with regions for whole-body action")),
    note="The ordered map and its magnification of the hands and face have held for ninety years, in stimulation and in "
         "imaging. The famous drawing is a summary, not a measurement, and finer studies keep revising its details.",
    sources=("W. Penfield and E. Boldrey, Somatic motor and sensory representation in the cerebral cortex of man as "
             "studied by electrical stimulation, Brain 60 (1937) 389-443",
             "F.-E. Roux, I. Djidjeli and J.-B. Durand, Functional architecture of the somatosensory homunculus detected "
             "by electrostimulation, Journal of Physiology 596 (2018) 941-956",
             "E. M. Gordon et al., A somato-cognitive action network alternates with effector regions in motor cortex, "
             "Nature 617 (2023) 351-359"),
    checked="2026-11-14",
    data=("PENFIELD_BOLDREY_1937",),
))

add(Finding(
    key="tongue_map", part=15, title=r"The tongue map",
    claim="Different parts of the tongue are sensitive to different tastes: sweet at the tip, bitter at the back.",
    original=Study("Hänig", 1901, n="a few observers", design="thresholds for tastes at points around the tongue's edge",
                   found="small differences in sensitivity from place to place"),
    status="story and record",
    record=(Study("Collings", 1974, n="a few observers", design="thresholds at loci on the tongue and soft palate",
                  found="real but small differences; every region with taste buds detects every taste"),),
    note="Hänig's small differences were redrawn in a 1942 history as a map, and textbooks turned the map into zones. "
         "Every part of the tongue with taste buds detects every basic taste.",
    sources=("D. P. Hänig, Zur Psychophysik des Geschmackssinnes, Philosophische Studien 17 (1901) 576-623",
             "V. B. Collings, Human taste response as a function of locus of stimulation on the tongue and soft palate, "
             "Perception & Psychophysics 16 (1974) 169-174"),
    checked="2026-11-14",
    data=("HANIG_1901",),
))

add(Finding(
    key="trillion_odours", part=15, title=r"A trillion odours",
    claim="People can discriminate more than a trillion different smells.",
    original=Study("Bushdid, Magnasco, Vosshall and Keller", 2014, n="26 people", design="telling apart mixtures of 10, 20 "
                   "or 30 odorants from 128", found="an extrapolated lower bound of 1.72 trillion"),
    status="contested",
    record=(Study("Gerkin and Castro", 2015, n="a reanalysis", design="the original data and estimator",
                  found="the estimate is fragile and could have given almost any number"),
            Study("Meister", 2015, n="an analysis", design="the same method applied to models and to colour",
                  found="the data fit ten discriminable odours as well as a trillion")),
    note="The experiments themselves are not in question. The number is: the extrapolation from pairs of mixtures to a "
         "count of all smells rests on assumptions that the reanalyses reject, and the true count is unknown.",
    sources=("C. Bushdid, M. O. Magnasco, L. B. Vosshall and A. Keller, Humans can discriminate more than 1 trillion "
             "olfactory stimuli, Science 343 (2014) 1370-1372",
             "R. C. Gerkin and J. B. Castro, The number of olfactory stimuli that humans can discriminate is still "
             "unknown, eLife 4 (2015) e08127",
             "M. Meister, On the dimensionality of odor space, eLife 4 (2015) e07865"),
    checked="2026-11-14",
    data=("BUSHDID_2014",),
))

add(Finding(
    key="blocking", part=16, title=r"Blocking",
    claim="A cue paired with an outcome that another cue already predicts acquires little or no association.",
    original=Study("Kamin", 1969, n="groups of rats", design="noise paired with shock, then noise and light together "
                   "paired with shock; fear of the light tested alone",
                   found="little fear of the light, against strong fear in rats without the noise training"),
    status="replicated, smaller",
    record=(Study("Maes and colleagues", 2016, n="15 experiments, in people and in rodents",
                  design="procedures similar or identical to published demonstrations",
                  found="no blocking in any of the fifteen"),),
    note="Blocking has been shown in many species and procedures and is built into most theories of learning, but "
         "it is weaker and less reliable than textbooks imply: careful standard procedures can fail to produce it, "
         "and its size depends on details such as whether the two cues share a sense.",
    sources=("L. J. Kamin, Predictability, surprise, attention, and conditioning, in B. A. Campbell and R. M. Church "
             "(eds), Punishment and Aversive Behavior (1969) 279-296",
             "T. Maes et al., The elusive nature of the blocking effect: 15 failures to replicate, Journal of "
             "Experimental Psychology: General 145 (2016) e49-e71"),
    checked="2026-11-14",
    data=("KAMIN_1969", "MAES_2016"),
))

add(Finding(
    key="taste_aversion", part=16, title=r"Taste aversion",
    claim="Rats readily learn to avoid a taste followed by illness, even hours later, and a light or sound followed "
          "by shock, but not the reverse pairings.",
    original=Study("Garcia and Koelling", 1966, n="groups of rats", design="water that was bright, noisy and tasty; "
                   "then shock, or illness from X-rays or lithium",
                   found="taste avoided after illness, lights and sounds after shock"),
    status="replicated",
    record=(Study("Domjan and Wilson", 1972, n="groups of rats", design="saccharin or a buzzer, then shock or illness",
                  found="the same selectivity, with the cues delivered in the same way"),),
    note="One-trial taste aversions across long delays are among the most robust findings in learning, in animals "
         "and in people after chemotherapy or food poisoning. They ended the idea that any cue can be linked to any "
         "outcome equally well.",
    sources=("J. Garcia and R. A. Koelling, Relation of cue to consequence in avoidance learning, Psychonomic Science 4 "
             "(1966) 123-124",
             "M. Domjan and N. E. Wilson, Specificity of cue to consequence in aversion learning in the rat, "
             "Psychonomic Science 26 (1972) 143-145"),
    checked="2026-11-14",
    data=("GARCIA_KOELLING_1966",),
))

add(Finding(
    key="conditioned_tolerance", part=16, title=r"Conditioned tolerance",
    claim="Tolerance to a drug is partly a conditioned response to the cues that usually come with it, so the same "
          "dose is more dangerous in an unfamiliar place.",
    original=Study("Siegel, Hinson, Krank and McCully", 1982, n="rats in three groups (37, 42, 28)",
                   design="heroin in a familiar room, then a large dose in the usual room or a new one",
                   found="32% died in the usual room, 64% in a new one, 96% with no history of the drug"),
    status="replicated",
    record=(Study("Siegel and Ramos", 2002, n="a review", design="animal experiments and human reports",
                  found="tolerance tied to drug cues across many drugs and species; overdoses often in unusual settings"),),
    note="The animal result has been repeated with many drugs. In people the evidence is from reports by overdose "
         "survivors and from cue-reactivity studies: consistent, but observational.",
    sources=("S. Siegel, R. E. Hinson, M. D. Krank and J. McCully, Heroin 'overdose' death: contribution of "
             "drug-associated environmental cues, Science 216 (1982) 436-437",
             "S. Siegel and B. M. C. Ramos, Applying laboratory research: drug anticipation and the treatment of drug "
             "addiction, Experimental and Clinical Psychopharmacology 10 (2002) 162-183"),
    checked="2026-11-14",
    data=("SIEGEL_1982",),
))

add(Finding(
    key="little_albert", part=16, title=r"Little Albert",
    claim="An infant was conditioned to fear a white rat, the fear spread to furry things, and it showed how phobias "
          "are learned.",
    original=Study("Watson and Rayner", 1920, n="1 infant", design="seven pairings of a white rat with a loud noise; "
                   "tests over the next month",
                   found="fear of the rat, and of a rabbit, a dog, a fur coat and a Santa Claus mask"),
    status="story and record",
    record=(Study("Harris", 1979, n="a review of the retellings", design="the paper against later textbooks",
                  found="the result grew in the retelling, and the fear was never removed"),
            Study("Powell, Digdon, Harris and Smithson", 2014, n="a historical search",
                  design="hospital records and census data",
                  found="who Albert was is disputed; the case cannot be followed up")),
    note="One infant, few trials, records kept as notes and a film, and no attempt to remove the fear before he left "
         "the hospital. It is a demonstration, and an ethical lesson, not evidence for a theory of phobias.",
    sources=("J. B. Watson and R. Rayner, Conditioned emotional reactions, Journal of Experimental Psychology 3 (1920) "
             "1-14",
             "B. Harris, Whatever happened to Little Albert?, American Psychologist 34 (1979) 151-160",
             "R. A. Powell, N. Digdon, B. Harris and C. Smithson, Correcting the record on Watson, Rayner, and Little "
             "Albert, American Psychologist 69 (2014) 600-611"),
    checked="2026-11-14",
    data=("WATSON_RAYNER_1920", "HARRIS_1979"),
))

add(Finding(
    key="matching_law", part=16, title=r"The matching law",
    claim="Given two sources of reward, animals divide their responses in proportion to the rewards each provides.",
    original=Study("Herrnstein", 1961, n="pigeons", design="two keys on concurrent variable-interval schedules",
                   found="the share of pecks on a key matched its share of reinforcers"),
    status="replicated",
    record=(Study("Baum", 1979, n="103 data sets from 23 studies", design="the generalized matching law fitted",
                  found="matching on average, with undermatching common"),),
    note="The relation holds across species, including people, and reinforcers. Fitted exactly, sensitivity is often "
         "a little below one (undermatching), and the law describes choice under concurrent interval schedules "
         "rather than every choice.",
    sources=("R. J. Herrnstein, Relative and absolute strength of response as a function of frequency of "
             "reinforcement, Journal of the Experimental Analysis of Behavior 4 (1961) 267-272",
             "W. M. Baum, Matching, undermatching, and overmatching in studies of choice, Journal of the Experimental "
             "Analysis of Behavior 32 (1979) 269-281"),
    checked="2026-11-14",
    data=("HERRNSTEIN_1961",),
))

add(Finding(
    key="renewal", part=16, title=r"Renewal after extinction",
    claim="A fear extinguished in one context returns when the cue is met in the context where the fear was learned.",
    original=Study("Bouton and Bolles", 1979, n="groups of rats", design="fear conditioned in one box, extinguished in "
                   "another, tested in the first",
                   found="fear back at the level of rats never extinguished"),
    status="replicated",
    record=(Study("Vervliet, Craske and Hermans", 2013, n="a review", design="renewal and relapse in animals and people",
                  found="renewal found across species, including in human fear conditioning and after exposure therapy"),),
    note="Extinction does not erase the first learning; it adds new learning tied to its context. The return of fear "
         "is why relapse after therapy is common, and why therapists vary the settings of exposure.",
    sources=("M. E. Bouton and R. C. Bolles, Contextual control of the extinction of conditioned fear, Learning and "
             "Motivation 10 (1979) 445-466",
             "B. Vervliet, M. G. Craske and D. Hermans, Fear extinction and relapse: state of the art, Annual Review of "
             "Clinical Psychology 9 (2013) 215-248"),
    checked="2026-11-14",
    data=("BOUTON_BOLLES_1979",),
))

shown(15, "BEKESY_1960", "the history of a measurement; the travelling wave is textbook physiology, not a finding in "
      "dispute")
shown(15, "KEMP_1978", "the discovery of an effect told as history; otoacoustic emissions are a clinical test")
shown(15, "MELZACK_WALL_1965", "a theory told as history and modelled; its circuit is revised in detail")
shown(15, "LEVINE_1978", "a single experiment at the start of a literature; placebo analgesia is entered in Part 57",
      row_in=57)
shown(15, "MCDERMOTT_2016", "a single cross-cultural study at the frontier of music perception, described with its "
      "limits")
shown(15, "KUJAWA_LIBERMAN_2009", "an animal result at the frontier; its human counterpart is unsettled")
