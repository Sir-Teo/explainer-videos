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

shown(5, "ADRIAN_1926", "the rate code of a single sensory fibre: told here as the discovery it was, with schematic "
      "trains; entered with the senses", row_in=11)
shown(5, "GOLGI_CAJAL_1906", "the neuron doctrine: a settled piece of anatomy, told as history")
shown(5, "GIDON_2020", "one laboratory's report of graded dendritic spikes in human cortex, shown at the frontier "
      "and not yet repeated elsewhere")
