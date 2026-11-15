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
      "replication are Part 21's row (forgetting_curve)")

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
      "strengthened synapses are the memory is argued with the evidence in Part 20, which reports it as a "
      "neuroscience finding, not a behavioural effect")
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
      "in Part 20, with the hippocampus as an index")
shown(17, "FRANK_2004", "one study of learning from reward and punishment, described with Psyche's learner beside it; disorders are Part 39")
shown(17, "WILSON_2014", "a study of exploration, described without figures")
shown(17, "TOLMAN_1948", "a theoretical paper, told as history")
shown(17, "ADAMS_DICKINSON_1981", "the devaluation test, described; motivation is entered with Part 28", row_in=28)
shown(17, "MOMENNEJAD_2017", "a test of the successor representation, described with its partial result")
shown(17, "HOWE_2013", "dopamine ramps, described at the frontier of the dopamine story")
shown(17, "DABNEY_2020", "a distributional code, described; replicated in a second region since")
shown(17, "REDISH_2004", "a model, run on Psyche; addiction is entered in Part 41", row_in=41)
shown(17, "LI_2010", "an engineering result, cited as an application")
shown(17, "WEINTRAUB_2010", "a cross-sectional survey quoted for its rates")
shown(17, "WANG_2018", "a model at the frontier")
shown(18, "ANDERSON_2011", "value-driven capture, described")
shown(18, "RENSINK_1997", "change blindness, described and fitted by Psyche; the effect is robust and its row is the inattentional-blindness row's companion")
shown(18, "CHERRY_1953", "the origin of the shadowing method, told as history")
shown(18, "BROADBENT_1958", "a theory, told as history")
shown(18, "MORAY_1959", "the own-name effect, described with its 1995 replication")
shown(18, "TREISMAN_1960", "theories of selection, told as history and run on Psyche")
shown(18, "LAVIE_1995", "load theory, described with its critics")
shown(18, "TREISMAN_GELADE_1980", "feature integration theory, described with its slopes")
shown(18, "WOLFE_2021", "a model, run on Psyche")
shown(18, "ITTI_KOCH_1998", "a model, run on Psyche")
shown(18, "PASHLER_1994", "a review and a model, run on Psyche")
shown(18, "BOTVINICK_2001", "a model, run on Psyche")
shown(18, "ROGERS_MONSELL_1995", "task switching, described as a pattern with Psyche's numbers")
shown(18, "MORAN_DESIMONE_1985", "a single-unit study, described schematically")
shown(18, "REYNOLDS_HEEGER_2009", "a model, derived and run on Psyche")
shown(18, "BUNDESEN_1990", "a theory, run on Psyche")
shown(18, "MACKWORTH_1948", "the vigilance decrement, revisited from Part 12", row_in=51)
shown(18, "STRAYER_2001", "a simulator study, read in full and described; driving returns in Part 51")
shown(19, "MILLER_1956", "history and arithmetic: the spans and the recoding are described, not tested anew")
shown(19, "SHALLICE_WARRINGTON_1970", "a single case, described as the evidence against the modal model's gateway")
shown(19, "BADDELEY_HITCH_1974", "a model, the multicomponent framework; its word-length prediction has a row")
shown(19, "ZHANG_LUCK_2008", "a descriptive model fitted here to open data; the capacity it estimates has a row")
shown(19, "BAYS_2009", "open trial-level data, fitted on screen by four models; the capacity row cites the comparison")
shown(19, "FUNAHASHI_1989", "delay activity, described with a schematic; a neural finding, not a behavioural claim")
shown(19, "WIMMER_2014", "a model fitted to monkey recordings, described alongside Psyche's ring attractor")
shown(19, "MONGILLO_2008", "a model of activity-silent memory, described at the frontier")
shown(19, "DANEMAN_CARPENTER_1980", "a correlation across people, described; intelligence returns in Part 32")
shown(19, "KANE_2005", "a meta-analytic correlation, described; intelligence returns in Part 32")
shown(19, "SIMONS_2016", "a review of the training evidence; the training row rests on the trials it reviews")
shown(19, "FTC_LUMOSITY_2016", "a regulatory settlement, reported as a fact; not a psychological finding")
shown(20, "EBBINGHAUS_1885", "the first forgetting curve, refitted here; its shape and its replication are Part 21's "
      "row (forgetting_curve)")
shown(20, "DRESLER_2017", "a single training study, shown as an example of the method of loci; mnemonic training's record "
      "is reviewed in Part 54", row_in=54)
shown(20, "KOHNKEN_1999", "a meta-analysis of an interview method; eyewitness memory and the interview are entered in Part "
      "56", row_in=56)
shown(20, "LIU_2012", "the engram experiment, recalled from Part 5; a neuroscience finding reported, not a behavioural "
      "effect")
shown(20, "SCOVILLE_MILNER_1957", "a single case, recalled from Part 7; its lessons are argued, not replicated")
shown(20, r"Anderson \& Schooler (1991)", "an analysis of the statistics of the environment, not an experiment on "
      "people")
shown(20, r"Berry, \ Shanks \& Henson (2008)", "a model at the frontier; the dissociations it addresses are described "
      "with their caveats")
shown(20, r"Hopfield (1982); \ Hebb (1949)", "a model and a postulate, derived and computed here")
shown(20, r"Ji-An et al.\ (2024)", "a study of language models at the frontier")
shown(20, r"Loftus \& Marburger (1983)", "a survey method, described; telescoping and landmarks are a measurement "
      "practice")
shown(20, r"MacDonald et al.\ (2011); \ Manning et al.\ (2011)", "neuroscience findings reported as evidence for a "
      "model's claim; the contiguity row cites the second")
shown(20, r"Mandler (1980); \ Tulving (1985)", "an example and a method; the recognition ROC's row is Part 12's")
shown(20, r"Marr (1971); \ Teyler \& DiScenna (1986)", "theories of the hippocampus, described")
shown(20, r"Milner (1962)", "a single case, recalled from Part 7")
shown(20, r"Raaijmakers \& Shiffrin (1981)", "a model, simulated here")
shown(20, r"Tulving (1972); \ Squire (1992, \ 2004)", "a taxonomy, not a finding")
shown(20, r"Warrington \& Weiskrantz (1970); \ Graf, \ Squire \& Mandler (1984)", "dissociations in amnesia, described "
      "with the warning about single dissociations; the lifespan and clinical record is Part 31's and Part 57's")
shown(20, r"Yonelinas et al.\ (2002); \ Wixted (2007); \ Squire et al.\ (2007)", "an open argument about brain "
      "localisation, described from both sides")
shown(21, "TALARICO_RUBIN_2003", "flashbulb memories, shown as one study with a schematic of its pattern; eyewitness "
      "memory and confidence are entered in Part 56", row_in=56)
shown(21, "WIXTED_WELLS_2017", "a review of eyewitness confidence, with a model computed here; the eyewitness rows are "
      "Part 56's", row_in=56)
shown(21, "DUNLOSKY_2013", "a review rating study techniques; the spacing and testing rows are this part's, and the "
      "classroom record is Part 54's", row_in=54)
shown(21, r"Anderson, \ Bjork \& Bjork (1994); \ Murayama et al.\ (2014)", "retrieval-induced forgetting, described "
      "with its meta-analysis; the mechanism (inhibition or blocking) is the open question, not the effect")
shown(21, r"Bartlett (1932); \ Bergman \& Roediger (1999)", "a classic informal method and its replication, described "
      "with a caution about how far it generalises")
shown(21, r"Ebbinghaus (1885); \ Cepeda et al.\ (2006)", "the spacing effect's history and review; its row is this "
      "part's")
shown(21, r"Huttenlocher, \ Hedges \& Duncan (1991)", "a model of reconstruction, derived and computed here")
shown(21, r"Jenkins \& Dallenbach (1924)", "a historical experiment in the decay-or-interference debate; none of its "
      "numbers is shown")
shown(21, r"Johnson, \ Hashtroudi \& Lindsay (1993)", "a framework, not a finding")
shown(21, r"Kindt, \ Soeter \& Vervliet (2009); \ Brunet et al.\ (2018)", "frontier attempts to weaken fear memories, "
      "described as open; treatment is Part 40's")
shown(21, r"Kirkpatrick et al.\ (2017)", "a machine-learning method at the frontier")
shown(21, r"Kornell, \ Bjork \& Garcia (2011)", "a model, fitted here")
shown(21, r"Luria (1968), \ \emph{The Mind of a Mnemonist}", "a single case study, told as such")
shown(21, r"McCloskey \& Cohen (1989)", "a simulation result about networks, reproduced here in a small network")
shown(21, r"McClelland, \ McNaughton \& O'Reilly (1995)", "a theory, with its model reproduced here")
shown(21, r"M\"uller \& Pilzecker (1900); \ Ribot (1882)", "the history of consolidation and of the temporal gradient "
      "of amnesia; the clinical record is Part 57's")
shown(21, r"Pavlik \& Anderson (2005)", "a model, simulated here")
shown(21, r"Richards \& Frankland (2017)", "a theoretical argument")
shown(21, r"Ryan et al.\ (2015)", "an animal neuroscience finding at the frontier")
shown(21, r"Underwood (1957)", "a review of old experiments, shown as a schematic of its summary")
shown(21, r"Wells et al.\ (2020); \ Garry et al.\ (1996)", "procedural recommendations and a finding about imagination; "
      "the courtroom and therapy are Part 56's", row_in=56)
shown(21, r"Wilson \& McNaughton (1994); \ Rasch et al.\ (2007)", "neuroscience of replay, and a targeted-reactivation "
      "experiment, reported as evidence for consolidation in sleep")
shown(21, r"Wixted \& Mickes (2014)", "a model of line-ups, computed here")
shown(21, r"Nader, \ Schafe \& LeDoux (2000)", "the animal reconsolidation experiment; the human claim is this part's "
      "reconsolidation row")
shown(16, "LUBOW_MOORE_1959", "latent inhibition, described and modelled; its row is in Part 18")
shown(16, "PAVLOV_1927", "the method and its vocabulary, told as history; the curves shown are Psyche's")
shown(16, "FERSTER_SKINNER_1957", "schedules of reinforcement, whose signatures are drawn on Psyche, not from their records")
shown(16, "WASSERMAN_1993", "human contingency judgment, cited for its main result; judgment is entered with Part 26")
shown(16, "RESCORLA_1968", "a design reproduced on Psyche with the paper's schedule; the paper's figures are not drawn")
shown(16, "RESCORLA_WAGNER_1972", "a model, derived and run, not a finding")
shown(16, "MACKINTOSH_PEARCE_HALL", "models of attention, run on one history")
shown(16, "GALLISTEL_GIBBON_2000", "a theory, and a summary of acquisition data shown with its exceptions")
shown(16, "BRELAND_1961", "trainers' observations, told as the anecdotes they were")
shown(16, "BANDURA_1961", "the Bobo doll, described without figures and with the doubt about what it measures")
shown(16, "PRENDERGAST_2006", "a meta-analysis quoted for its effect sizes", row_in=42)
shown(16, "ZENDLE_CAIRNS_2018", "a survey, quoted with its limits; product design is Part 52")
shown(16, "MITCHELL_2009", "a theoretical review at the frontier")
shown(16, "GERSHMAN_2010", "a model at the frontier")
shown(16, "SCHILLER_2010", "reconsolidation update, at the frontier; it is in the record of Part 21's row on "
      "reconsolidation in people")
shown(7, "PENFIELD_BOLDREY_1937", "the body's map on the cortex: settled anatomy, told as history; its row is "
      "entered with the senses, in Part 15")
shown(7, "HORTON_HOYT_1991", "a measured map used as a formula; the part computes with it")
shown(7, "SCOVILLE_MILNER_1957", "one patient, told as the case it was; what it shows about memory is argued in "
      "Part 20, where it is again a single case")
shown(7, "AZEVEDO_2009", "a count, used as a number")
shown(7, "RAICHLE_2002", "a measurement of energy use, used as a number")
shown(7, "WEISKRANTZ_1974", "one patient, described without figures; blindsight's own row is in Part 27, with "
      "awareness")
shown(7, "MAH_2014", "a methods finding shown at the frontier, beside the series' own simulation")
shown(7, "WIESEL_HUBEL_1963", "the critical period for one eye's hold on the cortex: told as history; entered with "
      "development", row_in=30)
shown(7, "MERZENICH_1984", "remapping after the loss of a finger: told as history, without figures")
shown(7, "GAZZANIGA_1978", "the split-brain experiments: told as the cases they were, a handful of patients "
      "studied in depth; Part 27 discusses awareness without them")


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
shown(10, "HOBSON_1977", "two theories of dreaming, presented as an open dispute between theories, not as a "
      "finding to replicate")
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
shown(11, "BERNOULLI_1738", "a theory of value, a preview; choices under risk are entered in Part 26, whose "
      "rows are the violations of that theory")
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
shown(12, "GIGERENZER_HOFFRAGE_1995", "base-rate reasoning, a preview; Part 26 shows the frequency-format "
      "result beside its heuristics rows, as a method rather than a finding")
shown(12, "MANISCALCO_LAU_2012", "a method at the frontier, a measure rather than a finding; Part 25 uses it to "
      "frame confidence")
shown(12, "SWETS_2000", "a review of applications, not a finding")
shown(12, "MICKES_2012", "line-ups, a preview of a live dispute; eyewitness memory is entered in Part 56", row_in=56)

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
shown(13, "MILNER_1991", "a single patient, told as the case that founded a theory; vision without awareness has "
      "its row in Part 27, as blindsight")
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

add(Finding(
    key="dopamine_rpe", part=17, title=r"Dopamine as a prediction error",
    claim="Midbrain dopamine neurons signal reward prediction errors: they fire to unpredicted rewards and to cues "
          "that predict reward, and dip when a predicted reward is omitted.",
    original=Study("Schultz, Dayan and Montague", 1997, n="recordings in monkeys", design="single dopamine neurons "
                   "during cue-juice conditioning, compared with the temporal-difference error",
                   found="the error's three signatures: at unpredicted reward, at the cue, a dip at omission"),
    status="replicated",
    record=(Study("Steinberg and colleagues", 2013, n="groups of rats", design="optogenetic stimulation of dopamine "
                  "neurons at reward time in a blocking design",
                  found="the blocked cue was learned: an artificial error teaches"),),
    note="The error signature has been found across species and methods, and shown to be causal for learning. "
         "Whether it is all dopamine signals, given ramps, movement-related firing and salience responses, is argued.",
    sources=("W. Schultz, P. Dayan and P. R. Montague, A neural substrate of prediction and reward, Science 275 (1997) "
             "1593-1599",
             "E. E. Steinberg et al., A causal link between prediction errors, dopamine neurons and learning, Nature "
             "Neuroscience 16 (2013) 966-973"),
    checked="2026-11-14",
    data=("SCHULTZ_1997", "STEINBERG_2013"),
))

add(Finding(
    key="two_step", part=17, title=r"Model-based choice in the two-step task",
    claim="In the two-step task, people's repeat choices show both a model-free and a model-based signature.",
    original=Study("Daw, Gershman, Seymour, Dayan and Dolan", 2011, n="17 people",
                   design="a two-stage choice with common and rare transitions; striatal imaging",
                   found="a mixture of the two signatures, and both kinds of error in the striatum"),
    status="replicated",
    record=(Study("Feher da Silva and Hare", 2020, n="online and laboratory samples",
                  design="the task with careful instructions and a story",
                  found="choices almost entirely model-based"),),
    note="The pattern of stay probabilities replicates widely. What the mixture weight measures is contested: a "
         "model-free learner with richer states can mimic it, and some apparent habit may be misunderstanding of "
         "the task.",
    sources=("N. D. Daw et al., Model-based influences on humans' choices and striatal prediction errors, Neuron 69 "
             "(2011) 1204-1215",
             "C. Feher da Silva and T. A. Hare, Humans primarily use model-based inference in the two-stage task, "
             "Nature Human Behaviour 4 (2020) 1053-1066"),
    checked="2026-11-14",
    data=("DAW_2011", "FEHER_DA_SILVA_2020"),
))

add(Finding(
    key="latent_learning", part=17, title=r"Latent learning",
    claim="Rats that explore a maze without reward learn its layout, and show it as soon as a reward is introduced.",
    original=Study("Tolman and Honzik", 1930, n="three groups of rats", design="daily maze runs; food every day, "
                   "never, or from day 11",
                   found="the day after food appeared, the late group ran about as well as rats fed all along"),
    status="replicated",
    record=(Study("Thistlethwaite", 1951, n="a review", design="the latent-learning experiments to date",
                  found="found in most, with failures in some designs"),),
    note="Latent learning is robust where animals can explore freely. It was the founding evidence for cognitive "
         "maps, which place and grid cells later made literal.",
    sources=("E. C. Tolman and C. H. Honzik, Introduction and removal of reward, and maze performance in rats, "
             "University of California Publications in Psychology 4 (1930) 257-275",
             "D. Thistlethwaite, A critical review of latent learning and related experiments, Psychological "
             "Bulletin 48 (1951) 97-129"),
    checked="2026-11-14",
    data=("TOLMAN_HONZIK_1930",),
))

add(Finding(
    key="grid_cells", part=17, title=r"Grid cells",
    claim="Neurons in the entorhinal cortex fire at many locations arranged on a triangular lattice as an animal "
          "moves through space.",
    original=Study("Hafting, Fyhn, Molden, Moser and Moser", 2005, n="rats", design="recordings in medial "
                   "entorhinal cortex during free foraging", found="firing fields on a regular triangular grid"),
    status="replicated",
    record=(Study("Doeller, Barry and Burgess", 2010, n="people", design="functional imaging during virtual "
                  "navigation", found="a six-fold, grid-like signal"),),
    note="Grid cells have been found in mice, bats and monkeys, and grid-like signals in human imaging. The cells "
         "are secure; what grid-like codes do in human thought is newer work.",
    sources=("T. Hafting et al., Microstructure of a spatial map in the entorhinal cortex, Nature 436 (2005) 801-806",
             "C. F. Doeller, C. Barry and N. Burgess, Evidence for grid cells in a human memory network, Nature 463 "
             "(2010) 657-661"),
    checked="2026-11-14",
    data=("HAFTING_2005",),
))

add(Finding(
    key="latent_inhibition", part=18, title=r"Latent inhibition",
    claim="A stimulus that has been presented many times without consequence is later learned about more slowly.",
    original=Study("Lubow and Moore", 1959, n="sheep and goats",
                   design="pre-exposure to a conditional stimulus, then conditioning of leg flexion",
                   found="pre-exposed stimuli conditioned more slowly than novel ones"),
    status="replicated",
    record=(Study("Lubow (review)", 1989, n="decades of studies in many species",
                  design="pre-exposure with many procedures, in animals, children and adults",
                  found="robust in animals and young children; in adults usually only with a masking task"),),
    note="Robust across mammals. In adults it appears mostly when a masking task keeps them from noticing the "
         "pre-exposed stimulus, and whether it lowers attention to the cue or only its expression is argued.",
    sources=("R. E. Lubow and A. U. Moore, Latent inhibition, Journal of Comparative and Physiological Psychology 52 "
             "(1959) 415-419",
             "R. E. Lubow, Latent Inhibition and Conditioned Attention Theory, Cambridge University Press (1989)"),
    checked="2026-11-14",
    data=("LUBOW_MOORE_1959",),
))

add(Finding(
    key="stroop", part=18, title=r"The Stroop effect",
    claim="Naming the ink colour of a colour word is slower when the word names a different colour; reading the word "
          "is barely affected by the ink.",
    original=Study("Stroop", 1935, n="college students; cards of 100 items",
                   design="naming the inks of incongruent colour words against coloured squares; reading words",
                   found="about 47 s longer per card, 74% more time; reading barely slowed"),
    status="replicated",
    record=(Study("MacLeod (review)", 1991, n="over 700 studies",
                  design="half a century of variants",
                  found="interference in every variant; asymmetric; larger than facilitation"),),
    note="Among the most reliable effects in psychology, used as a check that an online sample is paying attention. "
         "What it measures, automatic reading or a failure of control, is the argued part.",
    sources=("J. R. Stroop, Studies of interference in serial verbal reactions, Journal of Experimental Psychology 18 "
             "(1935) 643-662",
             "C. M. MacLeod, Half a century of research on the Stroop effect, Psychological Bulletin 109 (1991) "
             "163-203"),
    checked="2026-11-14",
    data=("STROOP_1935",),
))

add(Finding(
    key="inattentional_blindness", part=18, title=r"Inattentional blindness",
    claim="People engaged in a demanding task often fail to notice an unexpected, clearly visible object.",
    original=Study("Simons and Chabris", 1999, n="192 observers",
                   design="counting passes in a video while a gorilla or a woman with an umbrella walks through",
                   found="46% did not notice; fewer noticed under a harder task"),
    status="replicated",
    record=(Study("Most and colleagues", 2001, n="students in several experiments",
                  design="unexpected shapes of varied colour against the attended set",
                  found="noticing rises with similarity to the attended items"),
            Study("Drew, V\\~o and Wolfe", 2013, n="24 radiologists",
                  design="a gorilla 48 times a nodule's size inserted in a lung CT",
                  found="20 of 24 did not report it; most looked at it")),
    note="The basic effect replicates widely and in experts. How large it is depends on the task's load, the "
         "object's similarity to what is attended, and what observers are asked to report.",
    sources=("D. J. Simons and C. F. Chabris, Gorillas in our midst, Perception 28 (1999) 1059-1074",
             "S. B. Most et al., How not to be seen, Psychological Science 12 (2001) 9-17",
             "T. Drew, M. L.-H. Vo and J. M. Wolfe, The invisible gorilla strikes again, Psychological Science 24 "
             "(2013) 1848-1853"),
    checked="2026-11-14",
    data=("SIMONS_CHABRIS_1999", "DREW_2013"),
))

add(Finding(
    key="posner_cueing", part=18, title=r"Spatial cueing",
    claim="A cue to a location speeds responses to targets there and slows them elsewhere, without eye movements; "
          "an uninformative flash is later followed by inhibition of return.",
    original=Study("Posner", 1980, n="small groups of trained observers",
                   design="central arrows, 80% valid, with fixation checked",
                   found="benefits at the cued place and costs elsewhere"),
    status="replicated",
    record=(Study("Posner and Cohen", 1984, n="small groups",
                  design="uninformative peripheral flashes at several intervals",
                  found="facilitation early, inhibition of return after about 300 ms"),),
    note="Reproduced in essentially every laboratory that has run it; the effects are tens of milliseconds and very "
         "reliable within people.",
    sources=("M. I. Posner, Orienting of attention, Quarterly Journal of Experimental Psychology 32 (1980) 3-25",
             "M. I. Posner and Y. Cohen, Components of visual orienting, Attention and Performance X (1984) 531-556"),
    checked="2026-11-14",
    data=("POSNER_1980",),
))

add(Finding(
    key="attentional_blink", part=18, title=r"The attentional blink",
    claim="When two targets appear in a rapid stream, the second is often missed if it comes 200 to 500 ms after the "
          "first, but not if it comes immediately after.",
    original=Study("Raymond, Shapiro and Arnell", 1992, n="small groups",
                   design="a rapid letter stream with a coloured target and a later probe X",
                   found="probe detection impaired from about 180 to 450 ms after the target"),
    status="replicated",
    record=(Study("Dux and Marois (review)", 2009, n="hundreds of studies",
                  design="variants with letters, digits, words, faces and sounds",
                  found="the blink and lag-1 sparing in nearly all"),),
    note="The effect is robust; its explanation, a capacity limit or a lapse of control, is still argued. "
         "Individual differences are large, and a few people show almost no blink.",
    sources=("J. E. Raymond, K. L. Shapiro and K. M. Arnell, Temporary suppression of visual processing in an RSVP "
             "task, Journal of Experimental Psychology: Human Perception and Performance 18 (1992) 849-860",
             "P. E. Dux and R. Marois, The attentional blink: a review of data and theory, Attention, Perception, & "
             "Psychophysics 71 (2009) 1683-1700"),
    checked="2026-11-14",
    data=("RAYMOND_1992",),
))

add(Finding(
    key="media_multitasking", part=18, title=r"Media multitasking and attention",
    claim="People who multitask heavily with media are worse at filtering out distraction.",
    original=Study("Ophir, Nass and Wagner", 2009, n="heavy and light media multitaskers among students",
                   design="filtering, task-switching and memory tasks",
                   found="heavy multitaskers worse at ignoring distractors"),
    status="contested",
    record=(Study("Wiradhany and Nieuwenstein", 2017, n="two replications; a meta-analysis of 12 studies",
                  design="the original tasks with adequate power; pooled tests",
                  found="5 of 14 tests in the predicted direction; d = 0.17, near zero after bias correction"),),
    note="A small original study with a large effect; later work finds at most a small association, and a "
         "correlation cannot show that multitasking causes the deficit.",
    sources=("E. Ophir, C. Nass and A. D. Wagner, Cognitive control in media multitaskers, PNAS 106 (2009) "
             "15583-15587",
             "R. Wiradhany and M. R. Nieuwenstein, Cognitive control in media multitaskers: two replication studies "
             "and a meta-analysis, Attention, Perception, & Psychophysics 79 (2017) 2620-2641"),
    checked="2026-11-14",
    data=("OPHIR_2009",),
))

add(Finding(
    key="partial_report", part=19, title=r"Partial-report superiority",
    claim="Immediately after a brief display, a cued part of it can be reported far better than whole report implies; "
          "the advantage fades within about a second.",
    original=Study("Sperling", 1960, n="a few observers, thousands of trials",
                   design="3 x 4 letter arrays for 50 ms; whole report against a tone cueing one row",
                   found="about 9 of 12 letters available at once, against about 4.5 by whole report"),
    status="replicated",
    record=(Study("Coltheart (review)", 1980, n="two decades of studies",
                  design="partial report with many cues, displays and masks",
                  found="a large, brief, maskable store; the advantage is for location cues, not category cues"),),
    note="One of the most reproducible results in cognitive psychology. What the store contains, a picture or "
         "already-recognized items, and how much of it reaches awareness, is argued.",
    sources=("G. Sperling, The information available in brief visual presentations, Psychological Monographs 74 "
             "(1960) no. 11",
             "M. Coltheart, Iconic memory and visible persistence, Perception & Psychophysics 27 (1980) 183-228"),
    checked="2026-11-15",
    data=("SPERLING_1960",),
))

add(Finding(
    key="brown_peterson", part=19, title=r"Forgetting in eighteen seconds",
    claim="Without rehearsal, three consonants are mostly forgotten within eighteen seconds, because their trace "
          "decays with time.",
    original=Study("Peterson and Peterson", 1959, n="24 students",
                   design="a consonant trigram, then counting backwards by threes for 3 to 18 s",
                   found="about 80% recalled after 3 s, about 10% after 18 s"),
    status="story and record",
    record=(Study("Keppel and Underwood", 1962, n="students, trial by trial",
                  design="the same task, analysed by position in the session",
                  found="almost no forgetting on the first trial; forgetting grows over the next few"),),
    note="The forgetting is real and reproduces. The textbook cause, decay with time, does not survive the first "
         "trial: the loss comes mostly from proactive interference by the earlier trials' items.",
    sources=("L. R. Peterson and M. J. Peterson, Short-term retention of individual verbal items, Journal of "
             "Experimental Psychology 58 (1959) 193-198",
             "G. Keppel and B. J. Underwood, Proactive inhibition in short-term retention of single items, Journal "
             "of Verbal Learning and Verbal Behavior 1 (1962) 153-161"),
    checked="2026-11-15",
    data=("PETERSON_1959", "KEPPEL_UNDERWOOD_1962"),
))

add(Finding(
    key="word_length", part=19, title=r"The word-length effect",
    claim="Memory span is shorter for words that take longer to say, and articulatory suppression removes the "
          "difference.",
    original=Study("Baddeley, Thomson and Buchanan", 1975, n="students in several experiments",
                   design="serial recall of short and long words, some matched for syllables",
                   found="fewer long words recalled; span about what can be said in two seconds"),
    status="replicated",
    record=(Study("Lovatt, Avons and Masterson", 2000, n="students",
                  design="disyllables differing only in spoken duration, with other word sets",
                  found="no reliable duration effect for some sets: the classic sets confounded other properties"),),
    note="The effect of word length on span reproduces readily. Whether spoken duration itself is the cause, as the "
         "phonological loop says, or a correlated property of the words, is argued.",
    sources=("A. D. Baddeley, N. Thomson and M. Buchanan, Word length and the structure of short-term memory, Journal "
             "of Verbal Learning and Verbal Behavior 14 (1975) 575-589",
             "P. Lovatt, S. E. Avons and J. Masterson, The word-length effect and disyllabic words, Quarterly Journal "
             "of Experimental Psychology 53A (2000) 1-22"),
    checked="2026-11-15",
    data=("BADDELEY_1975",),
))

add(Finding(
    key="sternberg", part=19, title=r"Memory scanning is linear",
    claim="The time to decide whether a probe is in a short memorized list rises linearly with the list's length, "
          "with the same slope for yes and no.",
    original=Study("Sternberg", 1966, n="students",
                   design="memory sets of 1 to 6 digits, then a probe; yes or no",
                   found="about 38 ms per item from about 397 ms; equal slopes for yes and no"),
    status="replicated",
    record=(Study("Sternberg (review)", 1975, n="many replications",
                  design="digits, letters, words, faces; many laboratories",
                  found="linear set-size functions throughout; slopes vary with the material"),),
    note="The linear function reproduces. Its interpretation as serial exhaustive search does not follow: limited-"
         "capacity parallel models make the same predictions (Townsend 1972), and serial-position effects in the "
         "RTs trouble the simple serial model.",
    sources=("S. Sternberg, High-speed scanning in human memory, Science 153 (1966) 652-654",
             "S. Sternberg, Memory scanning: new findings and current controversies, Quarterly Journal of "
             "Experimental Psychology 27 (1975) 1-32"),
    checked="2026-11-15",
    data=("STERNBERG_1966",),
))

add(Finding(
    key="capacity_four", part=19, title=r"Capacity near four",
    claim="Without rehearsal or chunking, people hold about three to four items in working memory.",
    original=Study("Luck and Vogel", 1997, n="students",
                   design="change detection with coloured squares and with four-feature objects",
                   found="accuracy falls beyond 3 to 4 items; objects held as well as single features"),
    status="replicated",
    record=(Study("Cowan (review)", 2001, n="many tasks and laboratories",
                  design="change detection, running span, recency, enumeration",
                  found="estimates cluster at 3 to 5 chunks"),
            Study("van den Berg, Awh and Ma", 2014, n="10 datasets, 6 laboratories",
                  design="32 models of continuous report",
                  found="precision falls continuously with load; fixed slots alone fit worse"),),
    note="The number reproduces in every laboratory that blocks rehearsal. Whether it counts slots, or is a summary "
         "of a resource that is spread thinner, is the open question; the objects-not-features claim held only in "
         "part.",
    sources=("S. J. Luck and E. K. Vogel, The capacity of visual working memory for features and conjunctions, "
             "Nature 390 (1997) 279-281",
             "N. Cowan, The magical number 4 in short-term memory, Behavioral and Brain Sciences 24 (2001) 87-185",
             "R. van den Berg, E. Awh and W. J. Ma, Factorial comparison of working memory models, Psychological "
             "Review 121 (2014) 124-149"),
    checked="2026-11-15",
    data=("LUCK_VOGEL_1997", "COWAN_2001", "VANDENBERG_2012"),
))

add(Finding(
    key="wm_training", part=19, title=r"Working-memory training raises intelligence",
    claim="Training on working-memory tasks such as dual n-back improves fluid intelligence.",
    original=Study("Jaeggi, Buschkuehl, Jonides and Perrig", 2008, n="young adults in small groups",
                   design="8 to 19 days of dual n-back against a no-contact control",
                   found="gains on fluid reasoning that grew with days of training"),
    status="failed",
    record=(Study("Redick and colleagues", 2013, n="young adults, three groups",
                  design="20 sessions of dual n-back against adaptive visual search and no contact",
                  found="practice gains; no transfer to reasoning, memory capacity or speed"),
            Study("Melby-Lervag, Redick and Hulme (meta-analysis)", 2016, n="87 publications, 145 comparisons",
                  design="working-memory training against treated and untreated controls",
                  found="near transfer only; no reliable far transfer against active controls"),),
    note="Practice improves the practised task and its close relatives. Against placebo training, the far transfer "
         "that would matter, to reasoning and everyday cognition, is not found.",
    sources=("S. M. Jaeggi et al., Improving fluid intelligence with training on working memory, PNAS 105 (2008) "
             "6829-6833",
             "T. S. Redick et al., No evidence of intelligence improvement after working memory training, Journal of "
             "Experimental Psychology: General 142 (2013) 359-379",
             "M. Melby-Lervag, T. S. Redick and C. Hulme, Working memory training does not improve performance on "
             "measures of intelligence or other measures of far transfer, Perspectives on Psychological Science 11 "
             "(2016) 512-534"),
    checked="2026-11-15",
    data=("JAEGGI_2008", "REDICK_2013", "MELBY_LERVAG_2016"),
))

add(Finding(
    key="serial_position", part=20, title=r"Primacy and recency in free recall",
    claim="In free recall the first and the last few items of a list are recalled best, and recall usually starts "
          "with the last items.",
    original=Study("Murdock", 1962, n="students, six list conditions", design="free recall of lists of 10 to 40 "
                   "words at one or two seconds a word", found="a U-shaped serial-position curve; recency spans the "
                   "last seven or eight words whatever the length of the list"),
    status="replicated",
    record=(Study("Glanzer and Cunitz", 1966, n="students", design="30 s of counting before recall; slower "
                  "presentation", found="the delay removes recency and spares primacy; slower presentation helps "
                  "the early and middle words"),
            Study("Bjork and Whitten", 1974, n="students", design="a distractor after every word, the last "
                  "included", found="recency returns: long-term recency"),
            Study("Healey and Kahana (PEERS)", 2014, n="over a hundred people, thousands of lists",
                  design="immediate free recall of 16-word lists, analysed person by person",
                  found="the serial-position curve appears in almost every person; how recall starts varies"),),
    note="The shape is one of the most reproducible results in psychology. Its explanation is what changed: from a "
         "short-term buffer and rehearsal to a drifting context, because recency survives distraction.",
    sources=("B. B. Murdock, The serial position effect of free recall, Journal of Experimental Psychology 64 (1962) "
             "482-488",
             "M. Glanzer and A. R. Cunitz, Two storage mechanisms in free recall, Journal of Verbal Learning and Verbal "
             "Behavior 5 (1966) 351-360",
             "D. Rundus, Analysis of rehearsal processes in free recall, Journal of Experimental Psychology 89 (1971) "
             "63-77",
             "R. A. Bjork and W. B. Whitten, Recency-sensitive retrieval processes in long-term free recall, Cognitive "
             "Psychology 6 (1974) 173-189",
             "A. D. Baddeley and G. Hitch, Recency reexamined, in S. Dornic (ed.), Attention and Performance VI "
             "(1977) 647-667",
             "M. K. Healey and M. J. Kahana, Is memory search governed by universal principles or idiosyncratic "
             "strategies?, Journal of Experimental Psychology: General 143 (2014) 575-596"),
    checked="2026-11-15",
    data=("PEERS_FREE_RECALL",),
))

add(Finding(
    key="contiguity", part=20, title=r"Temporal contiguity in recall",
    claim="After recalling one item, people tend to recall next an item studied close to it in time, more often the "
          "one after it than the one before.",
    original=Study("Kahana", 1996, n="several free-recall datasets", design="the lag-conditional response "
                   "probability", found="a peak at lags of plus and minus one, higher in the forward direction"),
    status="replicated",
    record=(Study("Howard and Kahana", 1999, n="students", design="continual-distractor free recall",
                  found="contiguity persists when every word is followed by arithmetic"),
            Study("Healey and Kahana (PEERS)", 2014, n="over a hundred people", design="the lag-CRP person by person",
                  found="a recognisable contiguity curve in almost every person"),
            Study("Healey, Long and Kahana (review)", 2019, n="many datasets, new and archival",
                  design="benchmarks of contiguity across tasks, materials and time scales",
                  found="contiguity across designs and time scales, roughly scale-invariant"),),
    note="It is weaker in some people and some designs, and present almost everywhere. Models differ in how they "
         "produce it; the forward lean is what rules out symmetric associations alone.",
    sources=("M. J. Kahana, Associative retrieval processes in free recall, Memory & Cognition 24 (1996) 103-109",
             "M. W. Howard and M. J. Kahana, Contextual variability and serial position effects in free recall, "
             "Journal of Experimental Psychology: Learning, Memory, and Cognition 25 (1999) 923-941",
             "M. W. Howard and M. J. Kahana, A distributed representation of temporal context, Journal of "
             "Mathematical Psychology 46 (2002) 269-299",
             "S. M. Polyn, K. A. Norman and M. J. Kahana, A context maintenance and retrieval model of organizational "
             "processes in free recall, Psychological Review 116 (2009) 129-156",
             "M. K. Healey, N. M. Long and M. J. Kahana, Contiguity in episodic memory, Psychonomic Bulletin & Review "
             "26 (2019) 699-720",
             "M. G. Uitvlugt and M. K. Healey, Temporal proximity links unrelated news events in memory, "
             "Psychological Science 30 (2019)",
             "J. R. Manning, S. M. Polyn, G. H. Baltuch, B. Litt and M. J. Kahana, Oscillatory patterns in temporal "
             "lobe reveal context reinstatement during memory search, PNAS 108 (2011)"),
    checked="2026-11-15",
    data=("PEERS_FREE_RECALL",),
))

add(Finding(
    key="levels_of_processing", part=20, title=r"Levels of processing",
    claim="Words judged for their meaning at study are remembered better than words judged for their sound or "
          "their appearance, whether or not a test is expected.",
    original=Study("Craik and Tulving", 1975, n="ten experiments", design="case, rhyme or sentence questions about "
                   "each word, then a surprise or an expected test", found="recognition of about 15, 48 and 81 per "
                   "cent after case, rhyme and meaning questions"),
    status="replicated",
    record=(Study("Morris, Bransford and Franks", 1977, n="students", design="a rhyme recognition test after "
                  "rhyme or meaning study", found="rhyme study wins on a rhyme test: transfer-appropriate "
                  "processing"),),
    note="The effect is among the most robust in memory research. Depth as a theory was criticised for lacking an "
         "independent measure of depth; the match between study and test qualifies it.",
    sources=("F. I. M. Craik and R. S. Lockhart, Levels of processing: a framework for memory research, Journal of "
             "Verbal Learning and Verbal Behavior 11 (1972) 671-684",
             "F. I. M. Craik and E. Tulving, Depth of processing and the retention of words in episodic memory, "
             "Journal of Experimental Psychology: General 104 (1975) 268-294",
             "C. D. Morris, J. D. Bransford and J. J. Franks, Levels of processing versus transfer appropriate "
             "processing, Journal of Verbal Learning and Verbal Behavior 16 (1977) 519-533"),
    checked="2026-11-15",
    data=("CRAIK_TULVING_1975",),
))

add(Finding(
    key="generation_effect", part=20, title=r"The generation effect",
    claim="Words that people generate from a cue are remembered better than the same words read.",
    original=Study("Slamecka and Graf", 1978, n="five experiments", design="generate a word from a rule and a cue, "
                   "or read it", found="better recognition, cued and free recall for generated words"),
    status="replicated",
    record=(Study("Bertsch, Pesta, Wiscott and McDaniel (meta-analysis)", 2007, n="86 studies, 445 effect sizes",
                  design="generate against read", found="a mean effect of d = 0.40"),
            Study("McCurdy and colleagues (meta-analysis)", 2020, n="126 articles, 310 experiments",
                  design="generate against read, with generation constraint as a moderator",
                  found="a reliable effect, smallest in free recall"),),
    note="About half a standard deviation on average, varying a good deal with design; in free recall of mixed "
         "lists it can shrink or vanish.",
    sources=("N. J. Slamecka and P. Graf, The generation effect: delineation of a phenomenon, Journal of "
             "Experimental Psychology: Human Learning and Memory 4 (1978) 592-604",
             "S. Bertsch, B. J. Pesta, R. Wiscott and M. A. McDaniel, The generation effect: a meta-analytic review, "
             "Memory & Cognition 35 (2007) 201-210",
             "M. McCurdy and colleagues, Theories of the generation effect and the impact of generation "
             "constraint: a meta-analytic review, Psychonomic Bulletin & Review 27 (2020)"),
    checked="2026-11-15",
    data=("BERTSCH_2007",),
))

add(Finding(
    key="encoding_specificity", part=20, title=r"Encoding specificity",
    claim="A retrieval cue helps when it was part of what was encoded, so that a word can fail to be recognised and "
          "yet be recalled to a weak cue studied with it.",
    original=Study("Tulving and Thomson", 1973, n="several experiments", design="targets studied with weak "
                   "associates, then tested with strong associates and with the studied cues",
                   found="recognition failure of words recalled to their study cues"),
    status="replicated",
    record=(Study("Tulving and Wiseman", 1975, n="many published experiments", design="recognition of recallable "
                  "words across studies", found="recognition failure follows a lawful function of recognition"),),
    note="The phenomenon is robust. How general the principle is, and whether it can be tested without "
         "circularity, has been argued since.",
    sources=("E. Tulving and D. M. Thomson, Encoding specificity and retrieval processes in episodic memory, "
             "Psychological Review 80 (1973) 352-373",
             "E. Tulving and S. Wiseman, Relation between recognition and recognition failure of recallable words, "
             "Bulletin of the Psychonomic Society 6 (1975)",
             "D. W. Goodwin, B. Powell, D. Bremer, H. Hoine and J. Stern, Alcohol and recall: state-dependent "
             "effects in man, Science 163 (1969) 1358-1360",
             "J. E. Eich, The cue-dependent nature of state-dependent retrieval, Memory & Cognition 8 (1980) 157-173"),
    checked="2026-11-15",
))

add(Finding(
    key="underwater_context", part=20, title=r"Divers remember best where they learnt",
    claim="Divers recall words better in the environment where they learnt them, on land or under water.",
    original=Study("Godden and Baddeley", 1975, n="student divers", design="36 words learnt on a beach or about 7 m "
                   "under the sea, recalled 4 minutes later in the same or the other place", found="about 46 per "
                   "cent more recalled when the places matched"),
    status="contested",
    record=(Study("Smith and Vela (meta-analysis)", 2001, n="dozens of studies", design="incidental environmental "
                  "context and memory", found="a reliable, small effect (around d = 0.25), reduced by other cues and "
                  "by imagining the original context"),
            Study("Murre (direct replication)", 2021, n="16 divers", design="the same design in a heated pool 1.8 m "
                  "deep, all four conditions in one session", found="no context effect; if anything the reverse",
                  effect=-1.25, unit="words"),),
    note="Environmental context effects in general are real and small. The large underwater effect was not found "
         "again, in a replication that differed in setting and schedule; one replication cannot settle it either "
         "way.",
    sources=("D. R. Godden and A. D. Baddeley, Context-dependent memory in two natural environments: on land and "
             "underwater, British Journal of Psychology 66 (1975) 325-331",
             "S. M. Smith and E. Vela, Environmental context-dependent memory: a review and meta-analysis, "
             "Psychonomic Bulletin & Review 8 (2001) 203-220",
             "J. M. J. Murre, The Godden and Baddeley (1975) experiment on context-dependent memory on land and "
             "underwater: a replication, Royal Society Open Science 8 (2021) 200724"),
    checked="2026-11-15",
    data=("GODDEN_BADDELEY_1975", "MURRE_2021"),
))

add(Finding(
    key="forgetting_curve", part=21, title=r"The forgetting curve",
    claim="Memory, measured by savings in relearning, falls fast at first and then ever more slowly, roughly as a "
          "power of the time since learning.",
    original=Study("Ebbinghaus", 1885, n="1 (Ebbinghaus himself)", design="lists of 13 nonsense syllables learnt to "
                   "one errorless recitation and relearnt after 20 minutes to 31 days", found="savings of 58 per cent "
                   "after 20 minutes, 34 after a day, 21 after a month"),
    status="replicated",
    record=(Study("Heller, Mack and Seitz", 1991, n="2", design="Ebbinghaus's method and intervals",
                  found="the same shape at similar levels"),
            Study("Wixted and Ebbesen", 1991, n="students, several measures", design="recall and recognition over "
                  "intervals from seconds to weeks", found="forgetting well described by power functions"),
            Study("Murre and Dros", 2015, n="1 (about 70 hours)", design="a direct replication of the method and the "
                  "seven intervals", found="the same curve, with a likely jump upwards at one day"),),
    note="The shape replicates in every attempt. Which law describes a single memory is another matter: a power law "
         "in averaged data can arise from exponentials with different rates, and seven points do not separate the "
         "candidates.",
    sources=("H. Ebbinghaus, Uber das Gedachtnis (1885); transl. H. A. Ruger and C. E. Bussenius, Memory (1913)",
             "O. Heller, W. Mack and J. Seitz, Replikation der Ebbinghaus'schen Vergessenskurve mit der "
             "Ersparnismethode, Zeitschrift fur Psychologie 199 (1991) 3-18",
             "J. T. Wixted and E. B. Ebbesen, On the form of forgetting, Psychological Science 2 (1991) 409-415",
             "J. M. J. Murre and J. Dros, Replication and analysis of Ebbinghaus' forgetting curve, PLoS ONE 10 "
             "(2015) e0120644",
             "R. B. Anderson and R. D. Tweney, Artifactual power curves in forgetting, Memory & Cognition 25 (1997) "
             "724-730"),
    checked="2026-11-15",
    data=("EBBINGHAUS_1885", "SAVINGS_REPLICATIONS"),
))

add(Finding(
    key="spacing_effect", part=21, title=r"The spacing effect",
    claim="Study spread out over time is remembered better than the same amount of study massed together, and the "
          "best gap grows with how long the memory must last.",
    original=Study("Ebbinghaus", 1885, n="1", design="a list relearnt with massed or distributed repetitions",
                   found="38 repetitions over three days did as well as 68 in one"),
    status="replicated",
    record=(Study("Cepeda, Pashler, Vul, Wixted and Rohrer (meta-analysis)", 2006, n="hundreds of experiments",
                  design="verbal recall tasks with spaced and massed study", found="spacing beat massing almost "
                  "everywhere; the best gap depends on the retention interval"),
            Study("Cepeda, Vul, Rohrer, Wixted and Pashler", 2008, n="1,354 people online",
                  design="32 facts; gaps up to 105 days; retention intervals of 7 to 350 days",
                  found="an optimal gap for each interval, about 20 to 40 per cent of a week and 5 to 10 per cent "
                        "of a year"),),
    note="One of the most general effects in experimental psychology, for materials, ages and settings. Its "
         "mechanisms are argued; its use in schools is rare.",
    sources=("H. Ebbinghaus, Uber das Gedachtnis (1885)",
             "N. J. Cepeda, H. Pashler, E. Vul, J. T. Wixted and D. Rohrer, Distributed practice in verbal recall "
             "tasks: a review and quantitative synthesis, Psychological Bulletin 132 (2006) 354-380",
             "N. J. Cepeda, E. Vul, D. Rohrer, J. T. Wixted and H. Pashler, Spacing effects in learning: a temporal "
             "ridgeline of optimal retention, Psychological Science 19 (2008) 1095-1102",
             "P. I. Pavlik and J. R. Anderson, Practice and forgetting effects on vocabulary memory: an "
             "activation-based model of the spacing effect, Cognitive Science 29 (2005) 559-586"),
    checked="2026-11-15",
    data=("CEPEDA_2008",),
))

add(Finding(
    key="testing_effect", part=21, title=r"The testing effect",
    claim="Retrieving material from memory improves long-term retention more than studying it again for the same "
          "time.",
    original=Study("Roediger and Karpicke", 2006, n="120 students (Experiment 1)", design="a prose passage re-read "
                   "or recalled once without feedback; final test after 5 minutes, 2 days or a week",
                   found="re-reading better at 5 minutes; testing better by 14 points at 2 days and a week"),
    status="replicated",
    record=(Study("Rowland (meta-analysis)", 2014, n="many experiments", design="testing against restudy",
                  found="a reliable advantage for testing, about half a standard deviation, larger when the "
                        "practice test asks for recall rather than recognition"),
            Study("Adesope, Trevisan and Sundararajan (meta-analysis)", 2017, n="many studies, classroom and lab",
                  design="practice tests against other conditions", found="a reliable benefit in classrooms as "
                                                                           "well as the laboratory"),),
    note="Robust, and largest after a delay. How far it extends to complex material that must be understood "
         "rather than recalled is argued.",
    sources=("H. L. Roediger III and J. D. Karpicke, Test-enhanced learning: taking memory tests improves long-term "
             "retention, Psychological Science 17 (2006) 249-255",
             "A. I. Gates, Recitation as a factor in memorizing, Archives of Psychology 40 (1917)",
             "C. A. Rowland, The effect of testing versus restudy on retention: a meta-analytic review of the testing "
             "effect, Psychological Bulletin 140 (2014) 1432-1463",
             "O. O. Adesope, D. A. Trevisan and N. Sundararajan, Rethinking the use of tests: a meta-analysis of "
             "practice testing, Review of Educational Research 87 (2017) 659-701",
             "N. Kornell, R. A. Bjork and M. A. Garcia, Why tests appear to prevent forgetting: a distribution-based "
             "bifurcation model, Journal of Memory and Language 65 (2011) 85-97"),
    checked="2026-11-15",
    data=("ROEDIGER_KARPICKE_2006",),
))

add(Finding(
    key="drm_false_memory", part=21, title=r"False memories for unpresented words",
    claim="After studying a list of associates of a word that is not presented, people often recall and recognise "
          "that word, and report remembering it.",
    original=Study("Roediger and McDermott", 1995, n="36 and 30 students", design="lists of 12 or 15 associates of a "
                   "missing word (after Deese, 1959); recall, recognition, remember/know",
                   found="the missing word recalled on 40 and 55 per cent of lists, recognised as often as studied "
                         "words, and often judged remembered"),
    status="replicated",
    record=(Study("Gallo (review)", 2010, n="hundreds of studies", design="15 years of the DRM illusion",
                  found="robust across materials, tests and populations; reduced but not removed by warnings"),
            Study("Patihis and colleagues", 2013, n="20 people with superior autobiographical memory, 38 controls",
                  design="DRM lists and misinformation", found="as susceptible as ordinary memories"),),
    note="One of the most reproducible results in memory research. Its accounts (global matching, activation and "
         "monitoring, fuzzy traces) differ, and how far it speaks to memories of real events is argued.",
    sources=("H. L. Roediger III and K. B. McDermott, Creating false memories: remembering words not presented in "
             "lists, Journal of Experimental Psychology: Learning, Memory, and Cognition 21 (1995) 803-814",
             "J. Deese, On the prediction of occurrence of particular verbal intrusions in immediate recall, Journal "
             "of Experimental Psychology 58 (1959) 17-22",
             "D. A. Gallo, False memories and fantastic beliefs: 15 years of the DRM illusion, Memory & Cognition "
             "38 (2010) 833-848",
             "L. Patihis et al., False memories in highly superior autobiographical memory individuals, Proceedings "
             "of the National Academy of Sciences 110 (2013) 20947-20952",
             "J. Arndt and E. Hirshman, True and false recognition in MINERVA2: explanations from a global matching "
             "perspective, Journal of Memory and Language 39 (1998) 371-391"),
    checked="2026-11-15",
    data=("ROEDIGER_MCDERMOTT_1995", "PATIHIS_2013"),
))

add(Finding(
    key="misinformation_effect", part=21, title=r"The misinformation effect",
    claim="Misleading information given after an event is often incorporated into people's reports of the event "
          "itself.",
    original=Study("Loftus and Palmer", 1974, n="150 students (Experiment 2)", design="a verb in a speed question; a "
                   "week later, 'did you see broken glass?'", found="16 of 50 after 'smashed', 7 after 'hit', 6 not "
                                                                     "asked; there was none"),
    status="replicated",
    record=(Study("Loftus, Miller and Burns", 1978, n="students", design="slides of an accident at a stop sign; a "
                  "question presupposing a yield sign; a forced choice between the two slides",
                  found="misled people more often chose the slide they had not seen"),
            Study("Loftus (review)", 2005, n="hundreds of studies", design="thirty years of the paradigm",
                  found="robust; larger when the suggestion is plausible, comes later, and goes unnoticed"),),
    note="The effect on reports is robust. Whether the original detail is overwritten or merely outcompeted at test "
         "is argued; warnings after the misinformation reduce it.",
    sources=("E. F. Loftus and J. C. Palmer, Reconstruction of automobile destruction: an example of the interaction "
             "between language and memory, Journal of Verbal Learning and Verbal Behavior 13 (1974) 585-589",
             "E. F. Loftus, D. G. Miller and H. J. Burns, Semantic integration of verbal information into a visual "
             "memory, Journal of Experimental Psychology: Human Learning and Memory 4 (1978) 19-31",
             "E. F. Loftus, Planting misinformation in the human mind: a 30-year investigation of the malleability "
             "of memory, Learning & Memory 12 (2005) 361-366",
             "M. K. Johnson, S. Hashtroudi and D. S. Lindsay, Source monitoring, Psychological Bulletin 114 (1993) "
             "3-28"),
    checked="2026-11-15",
    data=("LOFTUS_PALMER_1974",),
))

add(Finding(
    key="implanted_memories", part=21, title=r"Implanted memories of childhood events",
    claim="Repeatedly suggesting a false childhood event, said to come from a relative, leads a substantial "
          "minority of people to report remembering it.",
    original=Study("Loftus and Pickrell", 1995, n="24", design="three true events and one false one (lost in a "
                   "mall), written about and discussed in two interviews", found="about a quarter came to remember "
                                                                                    "the false event", effect=0.25,
                   unit="share"),
    status="replicated",
    record=(Study("Scoboria and colleagues (mega-analysis)", 2017, n="423 people in eight studies",
                  design="the reports recoded on one scheme", found="about 30 per cent false memories; more "
                                                                     "accepted the event to some degree", effect=0.304,
                  unit="share"),
            Study("Murphy and colleagues (preregistered replication)", 2023, n="123", design="the lost-in-the-mall "
                  "procedure, online and in interviews", found="about 35 per cent coded as false memories",
                  effect=0.35, unit="share"),),
    note="The rate depends on the procedure and on how a report is coded as a memory rather than a belief. It shows "
         "that detailed false memories can be created; it does not show that any particular memory is false.",
    sources=("E. F. Loftus and J. E. Pickrell, The formation of false memories, Psychiatric Annals 25 (1995) 720-725",
             "A. Scoboria, K. A. Wade, D. S. Lindsay, T. Azad, D. Strange, J. Ost and I. E. Hyman, A mega-analysis of "
             "memory reports from eight peer-reviewed false memory implantation studies, Memory 25 (2017) 146-163",
             "G. Murphy et al., Lost in the mall again: a preregistered replication and extension of Loftus & "
             "Pickrell (1995), Memory 31 (2023) 711-724"),
    checked="2026-11-15",
    data=("LOFTUS_PICKRELL_1995",),
))

add(Finding(
    key="reconsolidation_humans", part=21, title=r"Updating a human memory by reconsolidation",
    claim="Reactivating a consolidated memory in people makes it labile, so that new learning soon after a reminder "
          "changes it.",
    original=Study("Walker, Brakefield, Hobson and Stickgold", 2003, n="students", design="a finger-tapping "
                   "sequence, reactivated before a second sequence was learnt", found="the first sequence was "
                   "impaired only when it had been reactivated"),
    status="contested",
    record=(Study("Schiller, Monfils, Raio, Johnson, LeDoux and Phelps", 2010, n="students",
                  design="extinction within minutes of a reminder of a conditioned fear", found="the fear did not "
                  "return, in a subset followed for about a year"),
            Study("Kindt and Soeter", 2013, n="students", design="the same retrieval-then-extinction procedure, with "
                  "several measures of fear", found="no prevention of the return of fear"),
            Study("Hardwicke, Taqi and Shanks", 2016, n="seven experiments, four of them direct replications",
                  design="the motor-sequence procedure, and variants", found="no reconsolidation effect"),),
    note="Reconsolidation in animals, after Nader, Schafe and LeDoux (2000), is robust. The behavioural version in "
         "people has proved hard to reproduce, and the boundary conditions are argued.",
    sources=("M. P. Walker, T. Brakefield, J. A. Hobson and R. Stickgold, Dissociable stages of human memory "
             "consolidation and reconsolidation, Nature 425 (2003) 616-620",
             "D. Schiller, M.-H. Monfils, C. M. Raio, D. C. Johnson, J. E. LeDoux and E. A. Phelps, Preventing the "
             "return of fear in humans using reconsolidation update mechanisms, Nature 463 (2010) 49-53",
             "M. Kindt and M. Soeter, Reconsolidation in a human fear conditioning study: a test of extinction as "
             "updating mechanism, Biological Psychology 92 (2013) 43-50",
             "T. E. Hardwicke, M. Taqi and D. R. Shanks, Postretrieval new learning does not reliably induce human "
             "memory updating via reconsolidation, Proceedings of the National Academy of Sciences 113 (2016) "
             "5206-5211",
             "K. Nader, G. E. Schafe and J. E. LeDoux, Fear memories require protein synthesis in the amygdala for "
             "reconsolidation after retrieval, Nature 406 (2000) 722-726"),
    checked="2026-11-15",
    data=("HARDWICKE_2016", "SCHILLER_2010"),
))

add(Finding(
    key="verbal_overshadowing", part=21, title=r"Verbal overshadowing of faces",
    claim="Describing a face in words after seeing it makes people less accurate at picking it from a line-up.",
    original=Study("Schooler and Engstler-Schooler", 1990, n="88 (Study 1)", design="a robbery video; a 20-minute "
                   "filler; 5 minutes describing the robber or naming states; a line-up",
                   found="correct identifications 39 against 64 per cent", effect=-0.25, unit="share"),
    status="replicated, smaller",
    record=(Study("Meissner and Brigham (meta-analysis)", 2001, n="dozens of studies",
                  design="description and identification", found="a small overshadowing effect, dependent on the "
                                                                  "procedure"),
            Study("Alogna and colleagues (RRR 2)", 2014, n="22 labs, about 2,000 people", design="the original order: "
                  "filler, then description", found="16 points fewer correct identifications", effect=-0.16,
                  unit="share"),
            Study("Alogna and colleagues (RRR 1)", 2014, n="31 labs, about 3,700 people", design="the description "
                  "straight after the video", found="4 points fewer", effect=-0.04, unit="share"),),
    note="Real, smaller than first reported, and sensitive to the timing of the description. The first Registered "
         "Replication Report; its per-lab data are open.",
    sources=("J. W. Schooler and T. Y. Engstler-Schooler, Verbal overshadowing of visual memories: some things are "
             "better left unsaid, Cognitive Psychology 22 (1990) 36-71",
             "C. A. Meissner and J. C. Brigham, A meta-analysis of the verbal overshadowing effect in face "
             "identification, Applied Cognitive Psychology 15 (2001) 603-616",
             "V. K. Alogna et al., Registered replication report: Schooler and Engstler-Schooler (1990), Perspectives "
             "on Psychological Science 9 (2014) 556-578"),
    checked="2026-11-15",
    data=("SCHOOLER_1990", "ALOGNA_2014"),
))

add(Finding(
    key="typicality", part=22, title=r"Typicality",
    claim="Members of a category differ reliably in how typical they are, and typical members are classified faster.",
    original=Study("Rips, Shoben and Smith", 1973, n="students", design="true-false verification of sentences like "
                   "'a robin is a bird'", found="typical members verified faster; rated distance predicted the times"),
    status="replicated",
    record=(Study("Rosch", 1975, n="about 200 students", design="goodness-of-example ratings for about 50 members of "
                  "each of 10 categories", found="strong agreement on which members are typical"),
            Study("McCloskey and Glucksberg", 1978, n="students, tested twice", design="membership and typicality "
                  "judgements, weeks apart", found="typicality agreed on; membership of borderline items unstable"),),
    note="One of the most robust regularities in cognition; what explains it, prototypes or exemplars, is the "
         "argument of chapters two and three.",
    sources=("L. J. Rips, E. J. Shoben and E. E. Smith, Semantic distance and the verification of semantic relations, "
             "Journal of Verbal Learning and Verbal Behavior 12 (1973) 1-20",
             "E. Rosch, Cognitive representations of semantic categories, Journal of Experimental Psychology: General "
             "104 (1975) 192-233",
             "M. E. McCloskey and S. Glucksberg, Natural categories: well defined or fuzzy sets?, Memory & Cognition 6 "
             "(1978) 462-472",
             "J. A. Hampton, Similarity-based categorization and fuzziness of natural categories, Cognition 65 (1998) "
             "137-165",
             "L. Wittgenstein, Philosophical Investigations (1953), sections 66-67"),
    checked="2026-11-15",
))

add(Finding(
    key="basic_level", part=22, title=r"The basic level",
    claim="Objects are named, verified and first learned at a middle level of abstraction, the basic level.",
    original=Study("Rosch, Mervis, Gray, Johnson and Boyes-Braem", 1976, n="a series of experiments",
                   design="attribute listing, shape averaging, naming and verification at three levels",
                   found="the middle level carries most attributes and is fastest"),
    status="replicated",
    record=(Study("Murphy and Smith", 1982, n="students", design="artificial tool categories at three levels",
                  found="a basic-level advantage in categorization speed"),
            Study("Tanaka and Taylor", 1991, n="dog and bird experts", design="naming and verification in and out "
                  "of the domain of expertise", found="in their domain, experts as fast at the subordinate level"),),
    note="Robust, and it moves with expertise.",
    sources=("E. Rosch, C. B. Mervis, W. D. Gray, D. M. Johnson and P. Boyes-Braem, Basic objects in natural "
             "categories, Cognitive Psychology 8 (1976) 382-439",
             "G. L. Murphy and E. E. Smith, Basic-level superiority in picture categorization, Journal of Verbal "
             "Learning and Verbal Behavior 21 (1982) 1-20",
             "J. W. Tanaka and M. Taylor, Object categories and expertise: is the basic level in the eye of the "
             "beholder?, Cognitive Psychology 23 (1991) 457-482",
             "J. E. Corter and M. A. Gluck, Explaining basic categories: feature predictability and information, "
             "Psychological Bulletin 111 (1992) 291-303"),
    checked="2026-11-15",
))

add(Finding(
    key="prototype_effect", part=22, title=r"The prototype effect",
    claim="After learning distortions of a prototype, people classify the never-seen prototype as well as or better "
          "than the items they studied.",
    original=Study("Posner and Keele", 1968, n="students", design="dot patterns distorted from three prototypes",
                   found="the unseen prototype classified well, and forgotten more slowly"),
    status="replicated",
    record=(Study("Homa and Vosburgh", 1976, n="students", design="categories of 3, 6 or 9 distortions",
                  found="prototype classification rises with category size"),
            Study("Medin and Schaffer", 1978, n="students", design="the 5-4 structure, where the models disagree",
                  found="an exemplar model fits; a prototype model does not"),
            Study("Medin and Schwanenflugel", 1981, n="students", design="linearly separable and non-separable "
                  "categories", found="separable categories not easier, against prototypes"),),
    note="The effect is solid. That it shows an abstracted prototype is not: exemplar models predict it too.",
    sources=("M. I. Posner and S. W. Keele, On the genesis of abstract ideas, Journal of Experimental Psychology 77 "
             "(1968) 353-363",
             "M. I. Posner and S. W. Keele, Retention of abstract ideas, Journal of Experimental Psychology 83 (1970) "
             "304-308",
             "D. Homa and R. Vosburgh, Category breadth and the abstraction of prototypical information, Journal of "
             "Experimental Psychology: Human Learning and Memory 2 (1976) 322-330",
             "D. L. Medin and M. M. Schaffer, Context theory of classification learning, Psychological Review 85 "
             "(1978) 207-238",
             "D. L. Medin and P. J. Schwanenflugel, Linear separability in classification learning, Journal of "
             "Experimental Psychology: Human Learning and Memory 7 (1981) 355-368",
             "R. M. Nosofsky, Attention, similarity, and the identification-categorization relationship, Journal of "
             "Experimental Psychology: General 115 (1986) 39-57",
             "J. D. Smith and J. P. Minda, Thirty categorization results in search of a model, Journal of "
             "Experimental Psychology: Learning, Memory, and Cognition 26 (2000) 3-27"),
    checked="2026-11-15",
    data=("HOMA_1976",),
))

add(Finding(
    key="shj_ordering", part=22, title=r"The six problems' ordering",
    claim="Of the six ways to split eight three-feature objects four and four, Type I is learned fastest, then II, "
          "then III, IV and V, and VI slowest.",
    original=Study("Shepard, Hovland and Jenkins", 1961, n="students", design="the six problems, learned by trial "
                   "and error", found="fewest errors on I, then II, then III, IV and V, most on VI"),
    status="replicated",
    record=(Study("Nosofsky, Gluck, Palmeri, McKinley and Glauthier", 1994, n="40 learners per problem",
                  design="the six problems, 16 blocks of 16 trials", found="the same ordering"),
            Study("Kurtz, Levering, Stanton, Romero and Morris", 2013, n="several experiments",
                  design="varied instructions and stimuli", found="Type II's advantage over IV not always found"),),
    note="I first and VI last is robust; Type II's place depends on the instructions and the stimuli.",
    sources=("R. N. Shepard, C. I. Hovland and H. M. Jenkins, Learning and memorization of classifications, "
             "Psychological Monographs 75 (1961) no. 13",
             "R. M. Nosofsky, M. A. Gluck, T. J. Palmeri, S. C. McKinley and P. Glauthier, Comparing models of "
             "rule-based classification learning: a replication and extension of Shepard, Hovland, and Jenkins "
             "(1961), Memory & Cognition 22 (1994) 352-369",
             "K. J. Kurtz, K. R. Levering, R. D. Stanton, J. Romero and S. N. Morris, Human learning of elemental "
             "category structures, Journal of Experimental Psychology: Learning, Memory, and Cognition 39 (2013)",
             "J. K. Kruschke, ALCOVE: an exemplar-based connectionist model of category learning, Psychological "
             "Review 99 (1992) 22-44"),
    checked="2026-11-15",
    data=("NOSOFSKY_1994",),
))

add(Finding(
    key="shepard_law", part=22, title=r"Shepard's law of generalization",
    claim="Generalization falls off exponentially with distance in psychological space.",
    original=Study("Shepard", 1957, n="confusion data", design="a stochastic model relating generalization to "
                   "distance", found="an exponential gradient"),
    status="replicated",
    record=(Study("Nosofsky", 1986, n="well-practised observers", design="identification and categorization of "
                  "semicircles", found="Gaussian gradients fitted better for practised identification"),
            Study("Shepard", 1987, n="12 data sets, people and pigeons", design="generalization against "
                  "scaled distance", found="exponential in every case"),
            Study("Sims", 2018, n="published data sets", design="a derivation from efficient coding",
                  found="the exponential law follows; deviations predicted"),
            Study("this part, on Rothkopf's table", 2026, n="630 pairs of Morse signals",
                  design="non-metric scaling, then generalization against distance",
                  found="exponential explains 71% of log generalization; a Gaussian less than none"),),
    note="Exponential across many data sets, with Gaussian exceptions that the theory accounts for.",
    sources=("R. N. Shepard, Stimulus and response generalization: a stochastic model relating generalization to "
             "distance in psychological space, Psychometrika 22 (1957) 325-345",
             "R. N. Shepard, Toward a universal law of generalization for psychological science, Science 237 (1987) "
             "1317-1323",
             "R. D. Luce, Detection and recognition, in Handbook of Mathematical Psychology 1 (1963) 103-189",
             "C. R. Sims, Efficient coding explains the universal law of generalization in human perception, Science "
             "360 (2018) 652-656",
             "E. Z. Rothkopf, A measure of stimulus similarity and errors in some paired-associate learning tasks, "
             "Journal of Experimental Psychology 53 (1957) 94-101",
             "J. B. Tenenbaum and T. L. Griffiths, Generalization, similarity, and Bayesian inference, Behavioral and "
             "Brain Sciences 24 (2001) 629-640"),
    checked="2026-11-15",
    data=("ROTHKOPF_1957",),
))

add(Finding(
    key="similarity_asymmetry", part=22, title=r"Asymmetric similarity",
    claim="Similarity judgements are asymmetric: a less prominent thing is judged more similar to a prominent one than "
          "the reverse.",
    original=Study("Tversky", 1977, n="69 and 2 x 77 students", design="choice of phrase and ratings for 21 pairs "
                   "of countries; Rothkopf's Morse confusions", found="66 of 69 chose 'North Korea is similar to Red "
                   "China'; 336 of 555 Morse pairs asymmetric the predicted way"),
    status="replicated, smaller",
    record=(Study("Tversky and Gati", 1978, n="students", design="countries, figures and other stimuli",
                  found="asymmetries in the predicted direction"),
            Study("Aguilar and Medin", 1999, n="several experiments", design="the direction and framing of "
                  "comparisons", found="no reliable asymmetry in rated similarity at first; asymmetries only under circumscribed conditions"),
            Study("this part, on Rothkopf's open table", 2026, n="555 pairs of unequal length",
                  design="Tversky's sign count", found="336, 182 and 37; Tversky's 336, 181 and 38"),),
    note="Preferences for one phrasing are strong. Asymmetries in rated similarity are small and appear only under "
         "some conditions; the Morse asymmetry is reliable but about 3 points.",
    sources=("A. Tversky, Features of similarity, Psychological Review 84 (1977) 327-352",
             "A. Tversky and I. Gati, Studies of similarity, in E. Rosch and B. B. Lloyd (eds), Cognition and "
             "Categorization (1978) 79-98",
             "C. M. Aguilar and D. L. Medin, Asymmetries of comparison, Psychonomic Bulletin & Review 6 (1999) 328-337",
             "E. Z. Rothkopf, A measure of stimulus similarity and errors in some paired-associate learning tasks, "
             "Journal of Experimental Psychology 53 (1957) 94-101"),
    checked="2026-11-15",
    data=("TVERSKY_1977",),
))

add(Finding(
    key="hierarchical_network", part=22, title=r"The hierarchical network",
    claim="Knowledge is stored in a hierarchy of concepts with each property stored once, so checking a fact takes "
          "longer the more links it crosses.",
    original=Study("Collins and Quillian", 1969, n="a few subjects", design="true-false sentences needing 0, 1 or 2 "
                   "links", found="times rose with the number of links"),
    status="failed",
    record=(Study("Conrad", 1972, n="students", design="properties controlled for how often people name them",
                  found="times followed familiarity, not level"),
            Study("Rips, Shoben and Smith", 1973, n="students", design="verification across levels",
                  found="typicality effects; 'a bear is an animal' faster than 'a bear is a mammal'"),),
    note="The strict hierarchy and cognitive economy did not survive; networks with spreading activation did.",
    sources=("A. M. Collins and M. R. Quillian, Retrieval time from semantic memory, Journal of Verbal Learning and "
             "Verbal Behavior 8 (1969) 240-247",
             "M. R. Quillian, Semantic memory, in M. Minsky (ed.), Semantic Information Processing (1968) 227-270",
             "C. Conrad, Cognitive economy in semantic memory, Journal of Experimental Psychology 92 (1972) 149-154",
             "L. J. Rips, E. J. Shoben and E. E. Smith, Semantic distance and the verification of semantic relations, "
             "Journal of Verbal Learning and Verbal Behavior 12 (1973) 1-20",
             "A. M. Collins and E. F. Loftus, A spreading-activation theory of semantic processing, Psychological "
             "Review 82 (1975) 407-428"),
    checked="2026-11-15",
))

add(Finding(
    key="semantic_priming", part=22, title=r"Semantic priming",
    claim="A word is recognized faster after a related word than after an unrelated one.",
    original=Study("Meyer and Schvaneveldt", 1971, n="students", design="lexical decisions on pairs like "
                   "bread-butter", found="related pairs faster"),
    status="replicated, smaller",
    record=(Study("Lucas (meta-analysis)", 2000, n="dozens of experiments", design="priming by meaning without "
                  "word association", found="a reliable effect, smaller than with associated pairs"),
            Study("Hutchison and colleagues (the Semantic Priming Project)", 2013, n="768 people, 1,661 targets",
                  design="lexical decision and naming, 200 and 1,200 ms", found="about 19 ms in lexical decision, 6 "
                  "in naming; 26 and 20 for first associates against 42 and 60 earlier", effect=19.0, unit="ms"),),
    note="Real and very reliable, but smaller than the hand-picked pairs of earlier studies suggested.",
    sources=("D. E. Meyer and R. W. Schvaneveldt, Facilitation in recognizing pairs of words: evidence of a "
             "dependence between retrieval operations, Journal of Experimental Psychology 90 (1971) 227-234",
             "M. Lucas, Semantic priming without association: a meta-analytic review, Psychonomic Bulletin & Review 7 "
             "(2000) 618-630",
             "K. A. Hutchison et al., The semantic priming project, Behavior Research Methods 45 (2013) 1099-1114",
             "J. R. Anderson, Retrieval of propositional information from long-term memory, Cognitive Psychology 6 "
             "(1974) 451-474"),
    checked="2026-11-15",
    data=("HUTCHISON_2013",),
))

add(Finding(
    key="word_superiority", part=23, title=r"The word superiority effect",
    claim="A letter in a briefly shown, masked word is reported more accurately than the same letter shown alone.",
    original=Study("Reicher", 1969, n="students", design="a brief display, a mask, then a choice between two "
                   "letters that both make a word", found="letters in words reported more accurately"),
    status="replicated",
    record=(Study("Wheeler", 1970, n="students", design="the same paradigm, with controls for guessing",
                  found="the same advantage"),
            Study("Baron and Thurston", 1973, n="students", design="pronounceable non-words",
                  found="an advantage for pronounceable non-words too"),),
    note="Robust, and the founding data of interactive models of reading.",
    sources=("G. M. Reicher, Perceptual recognition as a function of meaningfulness of stimulus material, Journal of "
             "Experimental Psychology 81 (1969) 275-280",
             "D. D. Wheeler, Processes in word recognition, Cognitive Psychology 1 (1970) 59-85",
             "J. Baron and I. Thurston, An analysis of the word-superiority effect, Cognitive Psychology 4 (1973) "
             "207-228",
             "J. L. McClelland and D. E. Rumelhart, An interactive activation model of context effects in letter "
             "perception: Part 1, Psychological Review 88 (1981) 375-407"),
    checked="2026-11-15",
))

add(Finding(
    key="statistical_segmentation", part=23, title=r"Statistical word segmentation by infants",
    claim="Infants can find the words of a continuous syllable stream from the transitional probabilities between "
          "syllables alone.",
    original=Study("Saffran, Aslin and Newport", 1996, n="24 eight-month-olds", design="two minutes of a "
                   "monotone stream of four three-syllable words; test on words and part-words",
                   found="longer listening to part-words"),
    status="replicated, smaller",
    record=(Study("Black and Bergmann (meta-analysis)", 2017, n="infant studies from 4 to 11 months",
                  design="conceptual replications and other transitional-probability designs",
                  found="a small, reliable effect in close replications; none reliable across all designs"),),
    note="Real but small in infants, and moderated by the stimuli; the computation itself is easy for a learner.",
    sources=("J. R. Saffran, R. N. Aslin and E. L. Newport, Statistical learning by 8-month-old infants, Science 274 "
             "(1996) 1926-1928",
             "A. Black and C. Bergmann, Quantifying infants' statistical word segmentation: a meta-analysis, "
             "Proceedings of the 39th Annual Conference of the Cognitive Science Society (2017) 124-129"),
    checked="2026-11-15",
    data=("SAFFRAN_1996",),
))

add(Finding(
    key="surprisal_reading", part=23, title=r"Surprisal and reading time",
    claim="The time a reader spends on a word grows linearly with the word's surprisal.",
    original=Study("Smith and Levy", 2013, n="eye-tracking and self-paced reading corpora", design="reading times "
                   "against n-gram surprisal", found="a linear relation over six orders of magnitude of "
                   "probability"),
    status="replicated",
    record=(Study("Goodkind and Bicknell", 2018, n="reading-time corpora", design="many language models",
                  found="the better the model, the better its surprisal predicts reading times"),
            Study("this part, on the Natural Stories corpus", 2026, n="10,256 words, about 84 readers each",
                  design="a trigram model of thirty novels; length and frequency controlled",
                  found="about 1.2 ms per bit, on the following word", effect=1.2, unit="ms"),),
    note="Steady across corpora and methods; which language model best matches readers is open.",
    sources=("N. J. Smith and R. Levy, The effect of word predictability on reading time is logarithmic, Cognition "
             "128 (2013) 302-319",
             "J. Hale, A probabilistic Earley parser as a psycholinguistic model, Proceedings of NAACL (2001) 159-166",
             "R. Levy, Expectation-based syntactic comprehension, Cognition 106 (2008) 1126-1177",
             "A. Goodkind and K. Bicknell, Predictive power of word surprisal for reading times is a linear function "
             "of language model quality, Proceedings of CMCL (2018) 10-18",
             "R. Futrell et al., The Natural Stories corpus, Language Resources and Evaluation 55 (2021) 63-77"),
    checked="2026-11-15",
    data=("NATURAL_STORIES",),
))

add(Finding(
    key="critical_period", part=23, title=r"A sharp critical period for second-language grammar",
    claim="There is a sharp age after which a second language's grammar cannot be fully learned.",
    original=Study("Johnson and Newport", 1989, n="46 Chinese and Korean speakers", design="grammaticality "
                   "judgements by age of arrival, 3 to 39", found="scores fell with age of arrival"),
    status="contested",
    record=(Study("Hakuta, Bialystok and Wiley", 2003, n="census data, millions of immigrants",
                  design="self-rated English by age of arrival", found="a steady decline, no break at puberty"),
            Study("Hartshorne, Tenenbaum and Pinker", 2018, n="669,498 people", design="an online grammar quiz; "
                  "age, age of starting and experience separated", found="ability near its peak until about 17.4, "
                  "then declining"),),
    note="A decline with the age of starting is well supported; whether it is a sharp period, when, and why, is not.",
    sources=("J. S. Johnson and E. L. Newport, Critical period effects in second language learning, Cognitive "
             "Psychology 21 (1989) 60-99",
             "K. Hakuta, E. Bialystok and E. Wiley, Critical evidence: a test of the critical-period hypothesis for "
             "second-language acquisition, Psychological Science 14 (2003) 31-38",
             "J. K. Hartshorne, J. B. Tenenbaum and S. Pinker, A critical period for second language acquisition, "
             "Cognition 177 (2018) 263-277",
             "R. I. Mayberry, E. Lock and H. Kazmi, Linguistic ability and early language exposure, Nature 417 (2002) "
             "38"),
    checked="2026-11-15",
    data=("HARTSHORNE_2018",),
))

add(Finding(
    key="color_relativity", part=23, title=r"Colour words and colour discrimination",
    claim="Speakers discriminate colours faster across a boundary their language names than within it.",
    original=Study("Winawer and colleagues", 2007, n="Russian and English speakers", design="speeded matching of "
                   "blues, with verbal or spatial interference", found="a Russian category advantage, removed by "
                   "verbal interference"),
    status="contested",
    record=(Study("Witzel and Gegenfurtner", 2011, n="observers", design="category effects in colour "
                  "discrimination", found="no reliable lateralized category effect"),
            Study("Martinovic, Paramei and MacInnes", 2020, n="Russian speakers", design="speeded discrimination "
                  "across blue boundaries", found="mixed: sharper boundaries, shaped by stimulus biases"),),
    note="Effects appear under some conditions and stimuli and not others.",
    sources=("J. Winawer, N. Witthoft, M. C. Frank, L. Wu, A. R. Wade and L. Boroditsky, Russian blues reveal "
             "effects of language on color discrimination, PNAS 104 (2007) 7780-7785",
             "C. Witzel and K. R. Gegenfurtner, Is there a lateralized category effect for color?, Journal of Vision "
             "11 (2011) 16",
             "J. Martinovic, G. V. Paramei and W. J. MacInnes, Russian blues reveal the limits of language influencing "
             "colour discrimination, Cognition 201 (2020) 104281",
             "B. Berlin and P. Kay, Basic Color Terms (1969)"),
    checked="2026-11-15",
))

add(Finding(
    key="bilingual_advantage", part=23, title=r"The bilingual advantage in executive control",
    claim="Speaking two languages improves executive control.",
    original=Study("Bialystok, Craik, Klein and Viswanathan", 2004, n="bilingual and monolingual adults",
                   design="the Simon task", found="bilinguals faster, especially older ones"),
    status="failed",
    record=(Study("Paap and Greenberg", 2013, n="three studies, about 100 to 200 each", design="many executive "
                  "tasks", found="no bilingual advantage"),
            Study("Lehtonen and colleagues (meta-analysis)", 2018, n="891 effect sizes from 152 studies",
                  design="six executive domains", found="a very small advantage before correcting for publication "
                  "bias; none after"),),
    note="No advantage once small samples and selective publication are accounted for.",
    sources=("E. Bialystok, F. I. M. Craik, R. Klein and M. Viswanathan, Bilingualism, aging, and cognitive control: "
             "evidence from the Simon task, Psychology and Aging 19 (2004) 290-303",
             "K. R. Paap and Z. I. Greenberg, There is no coherent evidence for a bilingual advantage in executive "
             "processing, Cognitive Psychology 66 (2013) 232-258",
             "M. Lehtonen et al., Is bilingualism associated with enhanced executive functioning in adults? A "
             "meta-analytic review, Psychological Bulletin 144 (2018) 394-425"),
    checked="2026-11-15",
    data=("LEHTONEN_2018",),
))

add(Finding(
    key="selection_content", part=24, title=r"Content effects in the selection task",
    claim="The selection task is solved far more often when the rule is a familiar permission, such as a drinking "
          "age, than when it is abstract.",
    original=Study("Griggs and Cox", 1982, n="students", design="the abstract task and the drinking-age version",
                   found="about three in four right on the drinking-age version, very few on the abstract one"),
    status="replicated",
    record=(Study("Cheng and Holyoak", 1985, n="students", design="permission rules with arbitrary content",
                  found="permission rules help without familiar content"),
            Study("Cosmides", 1989, n="students", design="unfamiliar rules framed as social contracts or "
                  "descriptions", found="social contracts solved, descriptions not"),),
    note="The effect is robust; whether it reflects permission schemas, cheater detection or information gain is "
         "argued.",
    sources=("P. C. Wason, Reasoning about a rule, Quarterly Journal of Experimental Psychology 20 (1968) 273-281",
             "R. A. Griggs and J. R. Cox, The elusive thematic-materials effect in Wason's selection task, British "
             "Journal of Psychology 73 (1982) 407-420",
             "P. W. Cheng and K. J. Holyoak, Pragmatic reasoning schemas, Cognitive Psychology 17 (1985) 391-416",
             "L. Cosmides, The logic of social exchange, Cognition 31 (1989) 187-276"),
    checked="2026-11-15",
))

add(Finding(
    key="belief_bias", part=24, title=r"Belief bias in syllogistic reasoning",
    claim="People accept believable conclusions more often than unbelievable ones with the same logical form, most "
          "of all when the conclusions do not follow.",
    original=Study("Evans, Barston and Pollard", 1983, n="students", design="valid and invalid syllogisms with "
                   "believable and unbelievable conclusions", found="acceptance 89, 56, 71 and 10 percent"),
    status="replicated",
    record=(Study("Klauer, Musch and Naumer", 2000, n="eight experiments", design="a multinomial model of the "
                  "effect", found="the effect, larger for invalid syllogisms"),
            Study("Dube, Rotello and Heit", 2010, n="experiments and reanalyses", design="receiver operating "
                  "characteristics", found="the effect, read as a shift in response bias"),),
    note="The effect is one of the most reliable in reasoning; whether belief changes reasoning or only the "
         "threshold for saying yes is argued.",
    sources=("J. St B. T. Evans, J. L. Barston and P. Pollard, On the conflict between logic and belief in "
             "syllogistic reasoning, Memory & Cognition 11 (1983) 295-306",
             "K. C. Klauer, J. Musch and B. Naumer, On belief bias in syllogistic reasoning, Psychological Review "
             "107 (2000) 852-884",
             "C. Dube, C. M. Rotello and E. Heit, Assessing the belief bias effect with ROCs: it's a response bias "
             "effect, Psychological Review 117 (2010) 831-863"),
    checked="2026-11-15",
))

add(Finding(
    key="mental_rotation", part=24, title=r"Mental rotation",
    claim="The time to judge whether two figures are the same object grows linearly with the angle between them.",
    original=Study("Shepard and Metzler", 1971, n="8 adults", design="pairs of block figures, 0 to 180 degrees "
                   "apart", found="about one second per 60 degrees, linear"),
    status="replicated",
    record=(Study("Cooper and Shepard", 1973, n="adults", design="rotated letters, normal or mirrored",
                  found="the same linear growth"),
            Study("Ganis and Kievit", 2015, n="54 adults", design="new 3-D figures at 0, 50, 100 and 150 degrees, "
                  "open data", found="times rising with angle; about 93 degrees a second for the median person"),),
    note="One of the most reliable effects in cognition; a constant rate fits the trend, not every detail.",
    sources=("R. N. Shepard and J. Metzler, Mental rotation of three-dimensional objects, Science 171 (1971) "
             "701-703",
             "L. A. Cooper and R. N. Shepard, Chronometric studies of the rotation of mental images, in Visual "
             "Information Processing (1973)",
             "G. Ganis and R. Kievit, A new set of three-dimensional shapes for investigating mental rotation "
             "processes: validation data and stimulus set, Journal of Open Psychology Data 3 (2015) e3"),
    checked="2026-11-15",
    data=("GANIS_KIEVIT_2015",),
))

add(Finding(
    key="chess_chunking", part=24, title=r"Chess experts' memory for positions",
    claim="Chess experts recall briefly seen positions from real games far better than novices, but not random "
          "ones.",
    original=Study("Chase and Simon", 1973, n="a master, a class A player and a beginner", design="positions "
                   "seen for five seconds, from games or random", found="recall rose with skill for games, not for "
                   "random positions"),
    status="replicated",
    record=(Study("Gobet and Simon", 1996, n="players of many strengths", design="random positions, brief "
                  "exposure", found="a small skill advantage on random positions too"),
            Study("Sala and Gobet (meta-analysis)", 2017, n="studies of chess, music, sport and other fields",
                  design="experts against novices on random material", found="a small but reliable expert edge, "
                  "as chunks that occur by chance predict"),),
    note="De Groot's earlier exposures (1946, in English 1965) found near-perfect recall by masters. "
         "Replicated many times; the small edge on random boards fits chunks that occur by chance.",
    sources=("W. G. Chase and H. A. Simon, Perception in chess, Cognitive Psychology 4 (1973) 55-81",
             "A. D. de Groot, Thought and Choice in Chess (1965; Dutch original 1946)",
             "F. Gobet and H. A. Simon, Recall of rapidly presented random chess positions is a function of skill, "
             "Psychonomic Bulletin & Review 3 (1996) 159-163",
             "G. Sala and F. Gobet, Experts' memory superiority for domain-specific random material generalizes "
             "across fields of expertise: a meta-analysis, Memory & Cognition 45 (2017) 183-193",
             "H. A. Simon and K. Gilmartin, A simulation of memory for chess positions, Cognitive Psychology 5 "
             "(1973) 29-46"),
    checked="2026-11-15",
))

add(Finding(
    key="ten_thousand_hours", part=24, title=r"The 10,000-hour rule",
    claim="Expert performance is mainly the product of about 10,000 hours of deliberate practice.",
    original=Study("Ericsson, Krampe and Tesch-Romer", 1993, n="violinists and pianists in Berlin",
                   design="retrospective estimates of practice", found="the best violinists had practised most, "
                   "an estimated 10,000 hours by twenty"),
    status="story and record",
    record=(Study("Macnamara, Hambrick and Oswald (meta-analysis)", 2014, n="88 studies, 11,135 people",
                  design="practice and performance across domains", found="practice explains 26% of differences "
                  "in games, 21% in music, 18% in sports, 4% in education, under 1% in professions"),
            Study("Macnamara and Maitra", 2019, n="violinists", design="a replication of the 1993 study",
                  found="the best and the good had practised about equally"),),
    note="Practice matters; the rule, popularized by Gladwell in 2008, is not what the study found and not what "
         "the record supports.",
    sources=("K. A. Ericsson, R. T. Krampe and C. Tesch-Romer, The role of deliberate practice in the acquisition "
             "of expert performance, Psychological Review 100 (1993) 363-406",
             "B. N. Macnamara, D. Z. Hambrick and F. L. Oswald, Deliberate practice and performance in music, "
             "games, sports, education, and professions: a meta-analysis, Psychological Science 25 (2014) "
             "1608-1618",
             "B. N. Macnamara and M. Maitra, The role of deliberate practice in expert performance: revisiting "
             "Ericsson, Krampe & Tesch-Romer (1993), Royal Society Open Science 6 (2019) 190327",
             "M. Gladwell, Outliers: The Story of Success, Little, Brown, New York (2008)"),
    checked="2026-11-15",
    data=("MACNAMARA_2014",),
))

add(Finding(
    key="everyday_prediction", part=24, title=r"Optimal predictions in everyday cognition",
    claim="People's predictions about everyday quantities match the Bayesian predictions under each domain's real "
          "distribution.",
    original=Study("Griffiths and Tenenbaum", 2006, n="students", design="predicting totals from one "
                   "observation, in several domains", found="median predictions close to the optimal curves"),
    status="replicated",
    record=(Study("Mozer, Pashler and Homaei", 2008, n="simulations and data", design="a model in which each person "
                  "recalls a few examples", found="group medians as good from very little individual knowledge"),
            Study("Lewandowsky, Griffiths and Kalish", 2009, n="individuals in chains", design="iterated learning",
                  found="individuals' predictions converge on good priors"),),
    note="The group-level match is robust; how much of the distribution each person holds is contested.",
    sources=("T. L. Griffiths and J. B. Tenenbaum, Optimal predictions in everyday cognition, Psychological "
             "Science 17 (2006) 767-773",
             "M. C. Mozer, H. Pashler and H. Homaei, Optimal predictions in everyday cognition: the wisdom of "
             "individuals or crowds?, Cognitive Science 32 (2008) 1133-1147",
             "S. Lewandowsky, T. L. Griffiths and M. L. Kalish, The wisdom of individuals: exploring people's "
             "knowledge about everyday events using iterated learning, Cognitive Science 33 (2009) 969-998"),
    checked="2026-11-15",
))

add(Finding(
    key="fitts_law", part=25, title=r"Fitts's law",
    claim="The time of an aimed movement grows linearly with the logarithm of twice the distance over the width of "
          "the target.",
    original=Study("Fitts", 1954, n="16 men", design="tapping between two plates, distances and widths varied",
                   found="movement time linear in log2(2D/W)"),
    status="replicated",
    record=(Study("Fitts and Peterson", 1964, n="adults", design="single, discrete aimed movements",
                  found="the same law"),
            Study("MacKenzie (review)", 1992, n="pointing studies", design="mice, styluses, joysticks, fingers",
                  found="the law holds across devices and limbs"),
            Study("Soukoreff and MacKenzie", 2004, n="studies under ISO 9241-9", design="a standard method for "
                  "testing pointing devices", found="the law as a measurement standard"),),
    note="Among the most reliable laws in psychology, and a standard for evaluating pointing devices.",
    sources=("P. M. Fitts, The information capacity of the human motor system in controlling the amplitude of "
             "movement, Journal of Experimental Psychology 47 (1954) 381-391",
             "P. M. Fitts and J. R. Peterson, Information capacity of discrete motor responses, Journal of "
             "Experimental Psychology 67 (1964) 103-112",
             "I. S. MacKenzie, Fitts' law as a research and design tool in human-computer interaction, "
             "Human-Computer Interaction 7 (1992) 91-139",
             "R. W. Soukoreff and I. S. MacKenzie, Towards a standard for pointing device evaluation, International "
             "Journal of Human-Computer Studies 61 (2004) 751-789"),
    checked="2026-11-15",
))

add(Finding(
    key="speed_bound", part=25, title=r"Speed instructions move the bound",
    claim="Instructions to be fast or accurate act on the diffusion model's boundary separation.",
    original=Study("Ratcliff and Rouder", 1998, n="3 practised observers", design="brightness judgements in speed "
                   "and accuracy blocks", found="the bound about twice as wide when accuracy is stressed"),
    status="replicated",
    record=(Study("Voss, Rothermund and Voss", 2004, n="students", design="four manipulations, one per parameter",
                  found="each manipulation moved mainly its own parameter"),
            Study("Wagenmakers, Ratcliff, Gomez and McKoon", 2008, n="17 adults (with Heathcote and Love 2012)",
                  design="lexical decision in speed and accuracy blocks; refitted in Part 25",
                  found="a lower bound under speed for 16 of 17; t0, and for some drift, changed too"),
            Study("Rae, Heathcote, Donkin, Averell and Brown", 2014, n="adults", design="speed emphasis",
                  found="the drift falls under speed emphasis as well as the bound"),),
    note="The bound moves every time; it is not the only thing that moves.",
    sources=("R. Ratcliff and J. N. Rouder, Modeling response times for two-choice decisions, Psychological Science "
             "9 (1998) 347-356",
             "A. Voss, K. Rothermund and J. Voss, Interpreting the parameters of the diffusion model: an empirical "
             "validation, Memory & Cognition 32 (2004) 1206-1220",
             "E.-J. Wagenmakers, R. Ratcliff, P. Gomez and G. McKoon, A diffusion model account of criterion shifts "
             "in the lexical decision task, Journal of Memory and Language 58 (2008) 140-159",
             "B. Rae, A. Heathcote, C. Donkin, L. Averell and S. Brown, The hare and the tortoise: emphasizing speed "
             "can change the evidence used to make decisions, Journal of Experimental Psychology: Learning, Memory, "
             "and Cognition 40 (2014) 1226-1243",
             "G. Dutilh and colleagues, The quality of response time data inference: a blinded, collaborative "
             "assessment of the validity of cognitive models, Psychonomic Bulletin & Review 26 (2019) 1051-1069"),
    checked="2026-11-15",
    data=("SPEED_ACC_2008", "RR98"),
))

add(Finding(
    key="fast_slow_errors", part=25, title=r"Fast errors under speed, slow errors under accuracy",
    claim="Errors are faster than correct responses when speed is stressed, and slower when accuracy is stressed.",
    original=Study("Ratcliff and Rouder", 1998, n="3 practised observers", design="brightness judgements in speed "
                   "and accuracy blocks", found="fast errors under speed, slow errors under accuracy, fitted by "
                   "variability in start and in drift"),
    status="replicated",
    record=(Study("Wagenmakers, Ratcliff, Gomez and McKoon", 2008, n="17 adults (with Heathcote and Love 2012)",
                  design="lexical decision in speed and accuracy blocks; refitted in Part 25",
                  found="median errors faster for 13 of 17 under speed, slower for 14 of 17 under accuracy"),
            Study("Ratcliff and McKoon (review)", 2008, n="studies of two-choice tasks", design="a review",
                  found="the pattern is common, and the full diffusion model fits it"),),
    note="A regular pattern that the four-parameter model cannot produce and the full model can.",
    sources=("R. Ratcliff and J. N. Rouder, Modeling response times for two-choice decisions, Psychological Science "
             "9 (1998) 347-356",
             "E.-J. Wagenmakers, R. Ratcliff, P. Gomez and G. McKoon, A diffusion model account of criterion shifts "
             "in the lexical decision task, Journal of Memory and Language 58 (2008) 140-159",
             "R. Ratcliff and G. McKoon, The diffusion decision model: theory and data for two-choice decision "
             "tasks, Neural Computation 20 (2008) 873-922"),
    checked="2026-11-15",
    data=("SPEED_ACC_2008", "RR98"),
))

add(Finding(
    key="lip_ramping", part=25, title=r"LIP neurons ramp to a bound",
    claim="Single neurons in the lateral intraparietal area accumulate evidence for a choice, ramping to a bound.",
    original=Study("Roitman and Shadlen", 2002, n="2 monkeys", design="random-dot motion, reaction-time "
                   "version", found="rises steeper for stronger motion; answers at a common level"),
    status="contested",
    record=(Study("Latimer, Yates, Meister, Huk and Pillow", 2015, n="2 monkeys", design="single-trial models of "
                  "LIP spike trains", found="about three quarters of neurons better described as stepping"),
            Study("Shadlen and colleagues (comment)", 2016, n="the same data and others", design="a reanalysis",
                  found="the data do not show one-time steps"),
            Study("Steinemann and colleagues", 2024, n="up to 203 neurons at once", design="population recordings "
                  "in LIP", found="a population signal that drifts and diffuses within single decisions"),),
    note="The population looks like diffusion; whether single neurons ramp or step is unsettled.",
    sources=("J. D. Roitman and M. N. Shadlen, Response of neurons in the lateral intraparietal area during a "
             "combined visual discrimination reaction time task, Journal of Neuroscience 22 (2002) 9475-9489",
             "K. W. Latimer, J. L. Yates, M. L. R. Meister, A. C. Huk and J. W. Pillow, Single-trial spike trains in "
             "parietal cortex reveal discrete steps during decision-making, Science 349 (2015) 184-187",
             "M. N. Shadlen, R. Kiani, W. T. Newsome and colleagues, Comment on single-trial spike trains in "
             "parietal cortex reveal discrete steps during decision-making, Science 351 (2016) 1406",
             "N. A. Steinemann, G. M. Stine, E. M. Trautmann, A. Zylberberg, D. M. Wolpert and M. N. Shadlen, "
             "Direct observation of the neural computations underlying a single decision, eLife 12 (2024) RP90859"),
    checked="2026-11-15",
))

add(Finding(
    key="stop_race", part=25, title=r"The stop-signal race",
    claim="Stopping is a race between independent go and stop processes, from which the stop-signal reaction time "
          "can be estimated.",
    original=Study("Logan and Cowan", 1984, n="a model with experiments", design="stop signals at varied delays",
                   found="the inhibition function and the stop time follow from an independent race"),
    status="contested",
    record=(Study("Verbruggen and colleagues (consensus)", 2019, n="many laboratories", design="a consensus guide "
                  "to running and analysing the task", found="estimates depend on design choices; recommended "
                  "practice"),
            Study("Bissett, Jones, Poldrack and Logan", 2021, n="several large datasets", design="tests of "
                  "independence", found="severe violations at short delays, across tasks and responses"),),
    note="The race predicts the inhibition function well; its independence assumption fails at short delays, "
         "which biases estimates that rely on them.",
    sources=("G. D. Logan and W. B. Cowan, On the ability to inhibit thought and action: a theory of an act of "
             "control, Psychological Review 91 (1984) 295-327",
             "F. Verbruggen and colleagues, A consensus guide to capturing the ability to inhibit actions and "
             "impulsive behaviors in the stop-signal task, eLife 8 (2019) e46323",
             "P. G. Bissett, H. M. Jones, R. A. Poldrack and G. D. Logan, Severe violations of independence in "
             "response inhibition tasks, Science Advances 7 (2021) eabf4355"),
    checked="2026-11-15",
))

add(Finding(
    key="framing_disease", part=26, title=r"Risky-choice framing",
    claim="Described as lives saved, most people choose a sure programme; described as deaths, the same outcomes "
          "lead most to choose the gamble.",
    original=Study("Tversky and Kahneman", 1981, n="152 and 155 respondents",
                   design="the disease problem in a lives-saved and a deaths frame",
                   found="72% chose the sure programme framed as lives saved; 78% chose the gamble framed as deaths"),
    status="replicated",
    record=(Study("Kuhberger (meta-analysis)", 1998, n="many studies", design="framing studies of many kinds",
                  found="risky-choice framing reliable, of moderate size, larger with problems like the original"),
            Study("Klein et al. (Many Labs 1)", 2014, n="36 samples", design="the disease problem, preregistered",
                  found="a clear framing effect in the pooled data")),
    note="One of the most reliable results in the field; its size depends on the wording.",
    sources=("A. Tversky and D. Kahneman, The framing of decisions and the psychology of choice, Science 211 (1981) "
             "453-458",
             "A. Kuhberger, The influence of framing on risky decisions: a meta-analysis, Organizational Behavior and "
             "Human Decision Processes 75 (1998) 23-55",
             "R. A. Klein et al., Investigating variation in replicability: a 'Many Labs' replication project, Social "
             "Psychology 45 (2014) 142-152"),
    checked="2026-11-15",
))

add(Finding(
    key="anchoring", part=26, title=r"Anchoring",
    claim="An arbitrary number considered before an estimate pulls the estimate toward it.",
    original=Study("Tversky and Kahneman", 1974, n="students", design="a wheel of fortune stopping at 10 or 65, "
                   "then the share of African countries in the UN",
                   found="median estimates of 25% and 45%"),
    status="replicated",
    record=(Study("Jacowitz and Kahneman", 1995, n="students", design="anchors set at percentiles of others' "
                  "estimates", found="large anchoring, stronger for high anchors"),
            Study("Klein et al. (Many Labs 1)", 2014, n="36 samples", design="four anchoring questions",
                  found="large effects in the pooled data"),
            Study("Maniadis, Tufano and List", 2014, n="students", design="anchors from incidental numbers, with "
                  "real valuations", found="much weaker effects than with a plainly comparative question")),
    note="Robust when the anchor is posed as a comparison; anchors from incidental numbers are weaker and less "
         "reliable.",
    sources=("A. Tversky and D. Kahneman, Judgment under uncertainty: heuristics and biases, Science 185 (1974) "
             "1124-1131",
             "K. E. Jacowitz and D. Kahneman, Measures of anchoring in estimation tasks, Personality and Social "
             "Psychology Bulletin 21 (1995) 1161-1166",
             "R. A. Klein et al., Investigating variation in replicability: a 'Many Labs' replication project, Social "
             "Psychology 45 (2014) 142-152",
             "Z. Maniadis, F. Tufano and J. A. List, One swallow doesn't make a summer: new evidence on anchoring "
             "effects, American Economic Review 104 (2014) 277-290"),
    checked="2026-11-15",
))

add(Finding(
    key="allais", part=26, title=r"The Allais pattern",
    claim="People prefer a sure gain to a slightly better risky one, yet reverse the choice when a common chance of "
          "the sure amount is removed from both options, violating independence.",
    original=Study("Kahneman and Tversky", 1979, n="72 respondents", design="Allais's common-consequence problems, "
                   "hypothetical prizes in Israeli pounds",
                   found="82% chose the sure 2,400; 83% chose the 0.33 chance of 2,500"),
    status="replicated",
    record=(Study("Huck and Muller", 2012, n="a large representative Dutch panel",
                  design="the paradox with hypothetical and real stakes",
                  found="frequent violations, most with high hypothetical stakes, fewer with small real ones"),
            Study("Ruggeri et al.", 2020, n="4,098 people in 19 countries", design="the 1979 problems",
                  found="most of the 1979 patterns found again, the certainty effect among them")),
    note="Robust with large, hypothetical prizes as in the original; with small real stakes it is weaker and "
         "depends on the design.",
    sources=("M. Allais, Le comportement de l'homme rationnel devant le risque, Econometrica 21 (1953) 503-546",
             "D. Kahneman and A. Tversky, Prospect theory: an analysis of decision under risk, Econometrica 47 "
             "(1979) 263-291",
             "S. Huck and W. Muller, Allais for all: revisiting the paradox in a large representative sample, "
             "Journal of Risk and Uncertainty 44 (2012) 261-293",
             "K. Ruggeri et al., Replicating patterns of prospect theory for decision under risk, Nature Human "
             "Behaviour 4 (2020) 622-633"),
    checked="2026-11-15",
))

add(Finding(
    key="conjunction_fallacy", part=26, title=r"The conjunction fallacy",
    claim="People judge a conjunction, such as feminist bank teller, more probable than one of its parts.",
    original=Study("Tversky and Kahneman", 1983, n="142 students", design="the Linda problem with two options",
                   found="85% chose the conjunction"),
    status="replicated",
    record=(Study("Fiedler", 1988, n="students", design="the same problems asked as frequencies",
                  found="far fewer conjunction errors"),
            Study("Hertwig and Gigerenzer", 1999, n="students", design="what people take 'probable' to mean",
                  found="many read it as plausible, not as mathematical probability"),
            Study("Mellers, Hertwig and Kahneman", 2001, n="students", design="an adversarial collaboration on "
                  "frequency formats", found="frequencies reduced the effect but did not remove it")),
    note="The error replicates; what it means, a failure of probability or a reasonable reading of the words, is "
         "still contested.",
    sources=("A. Tversky and D. Kahneman, Extensional versus intuitive reasoning: the conjunction fallacy in "
             "probability judgment, Psychological Review 90 (1983) 293-315",
             "K. Fiedler, The dependence of the conjunction fallacy on subtle linguistic factors, Psychological "
             "Research 50 (1988) 123-129",
             "R. Hertwig and G. Gigerenzer, The 'conjunction fallacy' revisited: how intelligent inferences look like "
             "reasoning errors, Journal of Behavioral Decision Making 12 (1999) 275-305",
             "B. Mellers, R. Hertwig and D. Kahneman, Do frequency representations eliminate conjunction effects? An "
             "exercise in adversarial collaboration, Psychological Science 12 (2001) 269-275"),
    checked="2026-11-15",
))

add(Finding(
    key="loss_aversion", part=26, title=r"Loss aversion",
    claim="Losses weigh more than equal gains, by a factor of about two.",
    original=Study("Kahneman and Tversky", 1979, n="students", design="mixed gambles and reflected problems",
                   found="symmetric 50-50 bets are unattractive; losses loom larger than gains"),
    status="contested",
    record=(Study("Tversky and Kahneman", 1992, n="graduate students", design="certainty equivalents",
                  found="a loss-aversion coefficient of 2.25"),
            Study("Walasek and Stewart", 2015, n="online participants", design="the ranges of gains and losses "
                  "offered varied", found="loss aversion appeared, vanished or reversed with the ranges"),
            Study("Gal and Rucker", 2018, n="a review", design="the evidence for loss aversion re-examined",
                  found="many effects attributed to it have other explanations"),
            Study("Mrkva, Johnson, Gachter and Herrmann", 2020, n="several large samples",
                  design="loss aversion and its moderators", found="robust, larger for larger stakes"),
            Study("This part (choices13k)", 2021, n="1,928 described problems", design="prospect theory fitted",
                  found="loss aversion of 1.13 at small stakes")),
    note="Present and robust for larger stakes; at small stakes and in some contexts it is weak, absent or "
         "reversed.",
    sources=("D. Kahneman and A. Tversky, Prospect theory: an analysis of decision under risk, Econometrica 47 "
             "(1979) 263-291",
             "A. Tversky and D. Kahneman, Advances in prospect theory: cumulative representation of uncertainty, "
             "Journal of Risk and Uncertainty 5 (1992) 297-323",
             "L. Walasek and N. Stewart, How to make loss aversion disappear and reverse: tests of the decision by "
             "sampling origin of loss aversion, Journal of Experimental Psychology: General 144 (2015) 7-11",
             "D. Gal and D. D. Rucker, The loss of loss aversion: will it loom larger than its gain?, Journal of "
             "Consumer Psychology 28 (2018) 497-516",
             "K. Mrkva, E. J. Johnson, S. Gachter and A. Herrmann, Moderating loss aversion: loss aversion has "
             "moderators, but reports of its death are greatly exaggerated, Journal of Consumer Psychology 30 (2020) "
             "407-428",
             "J. C. Peterson, D. D. Bourgin, M. Agrawal, D. Reichman and T. L. Griffiths, Using large-scale "
             "experiments and machine learning to discover theories of human decision-making, Science 372 (2021) "
             "1209-1214"),
    checked="2026-11-15",
    data=("CHOICES13K",),
))

add(Finding(
    key="hot_hand", part=26, title=r"The hot-hand fallacy",
    claim="Belief in the hot hand in basketball is a cognitive illusion: a player's chance of a hit does not rise "
          "after a run of hits.",
    original=Study("Gilovich, Vallone and Tversky", 1985, n="the 76ers, free throws, 26 Cornell players",
                   design="hit rates after streaks of hits and of misses",
                   found="no difference; the hot hand called an illusion"),
    status="story and record",
    record=(Study("Miller and Sanjurjo", 2018, n="the same Cornell shots, reanalysed",
                  design="the streak statistic's bias in finite sequences corrected",
                  found="a hot hand of several percentage points in the original data"),),
    note="The original test was biased toward finding nothing; corrected, the data show a hot hand. Whether people "
         "overestimate it is a separate question.",
    sources=("T. Gilovich, R. Vallone and A. Tversky, The hot hand in basketball: on the misperception of random "
             "sequences, Cognitive Psychology 17 (1985) 295-314",
             "J. B. Miller and A. Sanjurjo, Surprised by the hot hand fallacy? A truth in the law of "
             "small numbers, Econometrica 86 (2018) 2019-2047"),
    checked="2026-11-15",
))

add(Finding(
    key="blindsight", part=27, title=r"Blindsight",
    claim="After damage to primary visual cortex, people can locate and discriminate stimuli in the blind field "
          "that they say they do not see.",
    original=Study("Weiskrantz, Warrington, Sanders and Marshall", 1974, n="1 patient (D.B.)",
                   design="forced-choice localization and discrimination in the blind half-field",
                   found="far above chance, with no reported seeing"),
    status="replicated",
    record=(Study("Campion, Latto and Smith", 1983, n="a review", design="scattered light and spared cortex as "
                  "explanations", found="some results explicable by light scattered into the seeing field"),
            Study("Cowey and Stoerig", 1995, n="monkeys with V1 lesions", design="forced choice against detection",
                  found="targets located but classified as blank"),
            Study("Persaud, McLeod and Cowey", 2007, n="1 patient (G.Y.)", design="post-decision wagering",
                  found="accurate guesses, wagers that did not follow them"),
            Study("Overgaard, Fehl, Mouridsen, Bergholt and Cleeremans", 2008, n="1 patient",
                  design="a graded awareness scale", found="faint glimpses reported on trials a yes or no called "
                  "unseen"),
            Study("Schmid et al.", 2010, n="monkeys with V1 lesions", design="the LGN silenced",
                  found="blindsight abolished")),
    note="The effect replicates in patients and monkeys; whether it is degraded conscious vision rather than none "
         "is contested.",
    sources=("L. Weiskrantz, E. K. Warrington, M. D. Sanders and J. Marshall, Visual capacity in the hemianopic "
             "field following a restricted occipital ablation, Brain 97 (1974) 709-728",
             "J. Campion, R. Latto and Y. M. Smith, Is blindsight an effect of scattered light, spared cortex, and "
             "near-threshold vision?, Behavioral and Brain Sciences 6 (1983) 423-448",
             "A. Cowey and P. Stoerig, Blindsight in monkeys, Nature 373 (1995) 247-249",
             "N. Persaud, P. McLeod and A. Cowey, Post-decision wagering objectively measures awareness, Nature "
             "Neuroscience 10 (2007) 257-261",
             "M. Overgaard, K. Fehl, K. Mouridsen, B. Bergholt and A. Cleeremans, Seeing without seeing? Degraded "
             "conscious vision in a blindsight patient, PLoS ONE 3 (2008) e3028",
             "M. C. Schmid et al., Blindsight depends on the lateral geniculate nucleus, Nature 466 (2010) 373-377"),
    checked="2026-11-15",
))

add(Finding(
    key="masked_semantic_priming", part=27, title=r"Unconscious semantic priming",
    claim="A masked word or number that cannot be reported still speeds responses to a related target.",
    original=Study("Dehaene et al.", 1998, n="volunteers, with fMRI and ERPs", design="masked number primes, 43 ms",
                   found="congruent primes speed responses and prepare a motor response"),
    status="replicated, smaller",
    record=(Study("Van den Bussche, Van den Noortgate and Reynvoet (meta-analysis)", 2009, n="many studies",
                  design="masked priming of words and numbers", found="a reliable effect, smaller than early "
                  "reports"),
            Study("Vadillo, Konstantinidis and Shanks", 2016, n="a review", design="the awareness tests used",
                  found="often too weak to show that primes were unseen")),
    note="Priming by masked stimuli is real; how large it is, and how sure we are that the primes were unseen, is "
         "smaller than first claimed.",
    sources=("S. Dehaene et al., Imaging unconscious semantic priming, Nature 395 (1998) 597-600",
             "E. Van den Bussche, W. Van den Noortgate and B. Reynvoet, Mechanisms of masked priming: a "
             "meta-analysis, Psychological Bulletin 135 (2009) 452-477",
             "M. A. Vadillo, E. Konstantinidis and D. R. Shanks, Underpowered samples, false negatives, and "
             "unconscious learning, Psychonomic Bulletin & Review 23 (2016) 87-102"),
    checked="2026-11-15",
))

add(Finding(
    key="libet_timing", part=27, title=r"Libet's timing",
    claim="The readiness potential begins several hundred milliseconds before people report the urge to move.",
    original=Study("Libet, Gleason, Wright and Pearl", 1983, n="volunteers", design="spontaneous wrist flexions "
                   "timed on a clock", found="urge reported about 200 ms before movement; potential from about "
                   "550 ms"),
    status="replicated",
    record=(Study("Haggard and Eimer", 1999, n="volunteers", design="the lateralized readiness potential",
                  found="the timing found again, with a closer link to the lateralized potential"),
            Study("Soon, Brass, Heinze and Haynes", 2008, n="volunteers, fMRI", design="free choice of hand",
                  found="the choice decoded seconds early, at about 60% accuracy"),
            Study("Trevena and Miller", 2010, n="volunteers", design="cued decisions to move or not",
                  found="a similar potential before deciding not to move"),
            Study("Schurger, Sitt and Dehaene", 2012, n="a model and volunteers", design="accumulated noise to a "
                  "threshold", found="the ramp arises from averaging; interruptions answered faster at high "
                  "activity")),
    note="The timing replicates; that it shows an unconscious decision is contested, and the accumulator account "
         "explains the ramp without one.",
    sources=("B. Libet, C. A. Gleason, E. W. Wright and D. K. Pearl, Time of conscious intention to act in relation "
             "to onset of cerebral activity (readiness-potential), Brain 106 (1983) 623-642",
             "P. Haggard and M. Eimer, On the relation between brain potentials and the awareness of voluntary "
             "movements, Experimental Brain Research 126 (1999) 128-133",
             "C. S. Soon, M. Brass, H.-J. Heinze and J.-D. Haynes, Unconscious determinants of free decisions in the "
             "human brain, Nature Neuroscience 11 (2008) 543-545",
             "J. Trevena and J. Miller, Brain preparation before a voluntary action: evidence against unconscious "
             "movement initiation, Consciousness and Cognition 19 (2010) 447-456",
             "A. Schurger, J. D. Sitt and S. Dehaene, An accumulator model for spontaneous neural activity prior to "
             "self-initiated movement, PNAS 109 (2012) E2904-E2913"),
    checked="2026-11-15",
))

add(Finding(
    key="covert_awareness", part=27, title=r"Covert awareness",
    claim="Some patients who show no sign of awareness at the bedside follow commands by modulating their brain "
          "activity.",
    original=Study("Owen et al.", 2006, n="1 patient in a vegetative state", design="imagining tennis and moving "
                   "through a house, in fMRI", found="the same areas as healthy volunteers"),
    status="replicated",
    record=(Study("Monti et al.", 2010, n="54 patients", design="the same imagery tasks",
                  found="5 could modulate activity; one answered yes-or-no questions"),
            Study("Bodien et al.", 2024, n="353 patients in several countries", design="fMRI and EEG command "
                  "following", found="about a quarter of those without bedside command following did so")),
    note="Found again in larger and multicentre samples; how often, and with which method, still varies.",
    sources=("A. M. Owen et al., Detecting awareness in the vegetative state, Science 313 (2006) 1402",
             "M. M. Monti et al., Willful modulation of brain activity in disorders of consciousness, New England "
             "Journal of Medicine 362 (2010) 579-589",
             "Y. G. Bodien et al., Cognitive motor dissociation in disorders of consciousness, New England Journal "
             "of Medicine 391 (2024)"),
    checked="2026-11-15",
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

shown(22, r"Kruschke (1992)", "a model, fitted here to the open data; the ordering row is its test")
shown(22, r"Rips (1989); \ Barsalou (1983); \ Murphy \& Medin (1985)", "three single studies and a theoretical "
      "paper, told as the case for theories; described without effect sizes")
shown(22, r"Keil (1989); \ Gelman \& Markman (1986); \ Medin \& Ortony (1989)", "developmental studies described "
      "qualitatively; essentialism in children is entered with the infant mind in Part 30", row_in=30)
shown(22, r"Xu \& Tenenbaum (2007); \ Tenenbaum \& Griffiths (2001)", "a model and a word-learning study that tests "
      "it, described qualitatively; Bayesian word learning returns with language")
shown(22, r"Harris (1954); \ Firth (1957); \ the \emph{tezg\"{u}ino} example: \ Nida (1975), \ Lin (1998)", "the "
      "history of an idea")
shown(22, r"Landauer \& Dumais (1997); \ Caliskan et al. (2017); \ Harnad (1990)", "a model's benchmark, a "
      "measurement of text and a philosophical argument; not psychological findings to replicate")
shown(22, "LANDAUER_DUMAIS_1997", "a model's score on a test, not a finding about people")
shown(22, r"Fried \& Nesse (2015); \ Kotov et al. (2017); \ APA, \ DSM-5 (2013)", "a count of symptom profiles, a "
      "classification proposal and a manual's criteria; diagnosis as a category is entered in Part 39", row_in=39)
shown(22, r"Yang et al. (2020), \ the ImageNet person subtree", "a dataset's audit, described; not a finding about "
      "people")
shown(22, r"Marjieh, \ Sucholutsky, \ van Rijn, \ Jacoby \& Griffiths (2024)", "a study of language models at the "
      "frontier, with its numbers; machine representations are Part 60's", row_in=60)
shown(22, r"Lake et al. (2015); \ Peterson et al. (2018); \ Lake \& Baroni (2023)", "models at the frontier, "
      "described with their benchmarks; Part 60's")
shown(22, r"Huth, \ de Heer, \ Griffiths, \ Theunissen \& Gallant (2016)", "a mapping study at the frontier, "
      "described; semantic maps return with Part 49's encoding models")

shown(23, r"Skinner (1957); \ Chomsky (1959), \ \emph{Language} 35", "the history of a debate, told as the part's "
      "opening")
shown(23, r"Chomsky (1957), \ \emph{Syntactic Structures}", "a linguist's example sentence, not a finding")
shown(23, r"Berko (1958), \ \emph{Word} 14", "a classic demonstration of productivity, described; its generality "
      "is not in dispute")
shown(23, r"Bever (1970)", "garden-path sentences as a demonstration; the cost of reanalysis is measured in the "
      "surprisal row")
shown(23, r"Frazier \& Rayner (1982)", "an eye-tracking study described with a schematic; reanalysis costs are "
      "textbook")
shown(23, r"Gold (1967); \ Horning (1969); \ Chater \& Vit\'anyi (2007)", "theorems about learnability, not "
      "experiments")
shown(23, r"Carey \& Bartlett (1978); \ Hart \& Risley (1995)", "a word-learning study and a disputed estimate of "
      "input; the input gap is entered with the science of learning", row_in=54)
shown(23, r"Marcus et al. (1992)", "a corpus count reported as the size of an effect; the rules-or-associations "
      "dispute is about mechanism")
shown(23, r"Rumelhart \& McClelland (1986); \ Pinker \& Prince (1988)", "models and a critique of a model")
shown(23, r"Curtiss (1977); \ Mayberry, \ Lock \& Kazmi (2002)", "a single case and a study of first-language "
      "deprivation, described with their limits; the second-language row is this part's")
shown(23, r"Broca (1861); \ Wernicke (1874)", "the history of localization")
shown(23, r"Fedorenko, \ Behr \& Kanwisher (2011), \ \emph{PNAS}", "the language network, described; encoding "
      "models of language are Part 49's", row_in=49)
shown(23, r"Kutas \& Hillyard (1980); \ Osterhout \& Holcomb (1992)", "ERP components described with schematics; "
      "their use as measures is Part 49's", row_in=49)
shown(23, r"Whorf (1956, \ collected); \ Berlin \& Kay (1969)", "the history of the relativity question")
shown(23, r"Frank, \ Everett, \ Fedorenko \& Gibson (2008)", "one field study, described with its design")
shown(23, r"National Reading Panel (2000); \ Breitenstein et al. (2017), \ \emph{Lancet}", "a review and a trial "
      "in practice; reading instruction is entered in Part 54", row_in=54)
shown(23, r"Warstadt et al. (2020); \ Brown et al. (2020)", "machine benchmarks at the frontier; Part 60's")
shown(23, r"Vong, \ Wang, \ Orhan \& Lake (2024), \ \emph{Science}", "a model trained on one child's input, at "
      "the frontier; Part 60's")
shown(23, r"Oh \& Schuler (2023), \ \emph{TACL}", "a model-comparison result at the frontier; in the surprisal "
      "row's background")

shown(24, r"Wason (1966, \ 1968)", "the selection task's history; its content effect is this part's row")
shown(24, r"Johnson-Laird (1983); \ Johnson-Laird \& Bara (1984)", "a theory, described with a worked example")
shown(24, r"Cheng \& Holyoak (1985); \ Cosmides (1989)", "in the content-effect row's record")
shown(24, r"Oaksford \& Chater (1994), \ \emph{Psychological Review}", "a model, computed; its meta-analysis is "
      "quoted from its table")
shown(24, r"Newell, \ Shaw \& Simon (1958); \ Newell \& Simon (1972)", "the history of problem solving as "
      "search")
shown(24, r"Newell \& Simon (1972); \ Anderson (1993)", "theories of the mind as production systems")
shown(24, r"Ericsson \& Simon (1980, \ 1993)", "a method, described")
shown(24, r"Duncker (1945); \ Adamson (1952)", "classic demonstrations of functional fixedness, described")
shown(24, r"Metcalfe \& Wiebe (1987); \ MacGregor, \ Ormerod \& Chronicle (2001)", "a study and a model of "
      "insight, described with a schematic")
shown(24, r"Duncker (1945); \ Gick \& Holyoak (1980)", "a problem and a study of analogical transfer; its "
      "numbers are summaries, given as rough shares")
shown(24, r"Kosslyn, \ Ball \& Reiser (1978); \ Pylyshyn (1981); \ Zeman et al. (2015)", "the imagery debate "
      "and a recent finding, described")
shown(24, r"Waldmann \& Hagmayer (2005); \ Pearl (2000)", "causal reasoning, described; the mathematics is "
      "Statistics, Built Part 36")
shown(24, r"Evans, \ Barston \& Pollard (1983), \ as tabulated by Evans et al. (2001)", "the original "
      "study's table, as reprinted; the finding has its row, belief_bias")
shown(24, r"Simon (1955, \ 1956)", "a theory: bounded rationality")
shown(24, r"Schmidt \& Hunter (1998); \ Sackett et al. (2022); \ Sweller \& Cooper (1985)", "selection and "
      "instruction research, described; personnel selection is Part 53's",
      row_in=53)
shown(24, r"Ellis et al. (2021); \ Chollet (2019); \ LeGris et al. (2024)", "programs and benchmarks at the "
      "frontier; Part 60's", row_in=60)
shown(24, r"Webb, \ Holyoak \& Lu (2023), \ \emph{Nature Human Behaviour}", "machine analogy at the frontier; "
      "Part 60's", row_in=60)

shown(25, r"Wallis (1980); \ Wald (1945, \ 1947); \ Ratcliff (1978); \ Roitman \& Shadlen (2002)", "the history "
      "the part tells; LIP ramping has its row")
shown(25, r"Stone (1960); \ Laming (1968); \ Ratcliff (1978)", "the sequential-sampling tradition, described")
shown(25, r"Ratcliff (1978); \ Voss, \ Rothermund \& Voss (2004)", "the model's claims; selective influence has its "
      "row (speed_bound), with Voss et al. in its record")
shown(25, r"Shadlen \& Newsome (1996, \ 2001); \ Roitman \& Shadlen (2002)", "the recordings behind the LIP row "
      "(lip_ramping)")
shown(25, r"Usher \& McClelland (2001); \ Bogacz et al. (2006)", "models, described")
shown(25, r"Vickers (1979); \ Kiani \& Shadlen (2009); \ Pleskac \& Busemeyer (2010)", "accounts of confidence, "
      "described; metacognition's measures were Part 12's")
shown(25, r"Green (2000); \ AASHTO stopping sight distance", "applied figures, described")
shown(25, r"Ratcliff, \ Thapar \& McKoon (2001)", "ageing studies, described; individual differences are Part 59's",
      row_in=59)
shown(26, r"Bernoulli (1738); \ Allais (1953); \ Kahneman \& Tversky (1979)", "the history of the idea; the "
      "Allais pattern has its row")
shown(26, r"Pascal--Fermat letters (1654); \ Huygens (1657)", "the history of probability, described")
shown(26, r"von Neumann \& Morgenstern (1944, \ 1947); \ Savage (1954)", "axioms and theorems, not findings")
shown(26, r"Lichtenstein \& Slovic (1971); \ Grether \& Plott (1979); \ Tversky, \ Slovic \& Kahneman (1990)",
      "preference reversals, described with the replication by Grether and Plott that the film names")
shown(26, r"Tversky \& Kahneman (1992); \ Quiggin (1982)", "the cumulative form of the theory, derived; its "
      "parameters are tested on choices13k in the film")
shown(26, r"Tversky \& Kahneman (1992); \ Friedman \& Savage (1948)", "the fourfold pattern, computed from the "
      "theory; Friedman and Savage's is a theory, described")
shown(26, r"Tversky \& Kahneman (1973, \ 1974)", "the heuristics, introduced; anchoring and the conjunction "
      "fallacy have their rows")
shown(26, r"Gigerenzer \& Goldstein (1996)", "a decision rule, tested out of sample in Psyche's simulated worlds")
shown(26, r"Hertwig, \ Barron, \ Weber \& Erev (2004)", "the description-experience gap, described with its "
      "meta-analysis (Wulff et al. 2018) and checked in choices13k in the film")
shown(26, r"Stanovich \& West (2000); \ Evans \& Stanovich (2013); \ Kruglanski \& Gigerenzer (2011)", "theories "
      "of two systems and their critics, described")
shown(26, r"Parducci (1965); \ Walasek \& Stewart (2015)", "range-frequency theory, described; Walasek and "
      "Stewart's result is in the loss-aversion row")
shown(26, r"Johnson \& Goldstein (2003); \ Levin \& Gaeth (1988)", "applications of defaults and framing, "
      "described; defaults get their row with behaviour change at scale", row_in=55)
shown(26, r"Thaler \& Benartzi (2004)", "an applied programme, described as uncontrolled; its row is due with "
      "behaviour change at scale", row_in=55)
shown(26, r"Gigerenzer et al.\ (2007); \ Furedi (1999)", "risk communication, applied and described")
shown(26, r"Peterson et al.\ (2021); \ Erev et al.\ (2017)", "methods for finding theories, described; the "
      "choices13k data are fitted in the film")
shown(26, r"Frey et al.\ (2017)", "the measurement of risk preference, described; traits are Part 33's",
      row_in=33)
shown(27, r"Baars (1988); \ Crick \& Koch (1990)", "the founding programmes of the field, described")
shown(27, r"Baars (1988); \ Dehaene, \ Kerszberg \& Changeux (1998)", "the global workspace theory, described; its "
      "predictions are modelled by Psyche")
shown(27, r"Dehaene \& Changeux (2011)", "a review of the workspace's signatures, described with their challenges")
shown(27, r"Eriksen (1960); \ Ramsøy \& Overgaard (2004); \ Del Cul, \ Baillet \& Dehaene (2007)", "methods for "
      "measuring awareness, described; the criterion problem is computed by Psyche")
shown(27, r"Fleming, \ Weil, \ Nagy, \ Dolan \& Rees (2010); \ Fleming \& Dolan (2012)", "metacognition's neural "
      "correlates, described; its measurement was Part 12's")
shown(27, r"Frässle et al.\ (2014); \ Tsuchiya et al.\ (2015)", "the no-report method, described")
shown(27, r"Koch \& Tsuchiya (2007)", "an argument from dissociations, described; attention was Part 18's")
shown(27, r"Kornhuber \& Deecke (1965); \ Libet, \ Gleason, \ Wright \& Pearl (1983)", "the readiness potential's "
      "discovery; Libet's timing has its row")
shown(27, r"Lamme (2006)", "a theory, described")
shown(27, r"Lau \& Passingham (2006); \ Lau \& Rosenthal (2011); \ Brown, \ Lau \& LeDoux (2019)", "higher-order "
      "theories and one study in their support, described")
shown(27, r"Laureys (2005)", "a clinical framework, described")
shown(27, r"Leopold \& Logothetis (1996); \ Tong et al.\ (1998)", "rivalry's neural correlates, described "
      "schematically; the rivalry model is Psyche's")
shown(27, r"Melloni et al.\ (2021); \ Cogitate Consortium (2025)", "a single preregistered adversarial study, too "
      "recent to have a record of its own")
shown(27, r"Cogitate Consortium (2025)", "a single preregistered adversarial study, too recent to have a record of "
      "its own")
shown(27, r"Seth \& Bayne (2022)", "a review of theories")
shown(27, r"Seth \& Bayne (2022); \ Cogitate Consortium (2025)", "a review, and the adversarial study above; the "
      "scorecard is a judgement, marked as such")
shown(27, r"Myles et al.\ (2004); \ Avidan et al.\ (2008); \ Pandit et al.\ (2014)", "clinical trials and an "
      "audit in anaesthesia, described as applications")
shown(27, r"Schnakers et al.\ (2009); \ Giacino et al.\ (2018); \ Kondziella et al.\ (2020)", "clinical diagnosis "
      "and guidelines, described as applications")
shown(27, r"Butlin, \ Long et al.\ (2023)", "a proposal for assessing machines, described; machines are Part 60's",
      row_in=60)
shown(27, r"Nagel (1974); \ Chalmers (1995); \ Block (1995)", "philosophical distinctions, not findings")
shown(27, r"the Koch--Chalmers wager (1998, \ settled 2023)", "a wager, told as history")
shown(27, r"Tononi (2004); \ Oizumi, \ Albantakis \& Tononi (2014); \ Tononi et al.\ (2016)", "integrated "
      "information theory, described; its 2004 measure is computed by Psyche")
shown(27, r"Tononi et al.\ (2016); \ Aaronson (2014); \ Fleming et al.\ (2023)", "the theory's predictions and its "
      "critics, described")
shown(27, r"Weiskrantz, \ Warrington, \ Sanders \& Marshall (1974); \ Weiskrantz (1986)", "the history of the "
      "case; blindsight has its row")
