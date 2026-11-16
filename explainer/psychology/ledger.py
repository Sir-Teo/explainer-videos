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
      "the trial's result is not presented; Part 42's frontier discusses the unblinding problem in such trials")
shown(2, r"Arnett (2008); \ Henrich, Heine \& Norenzayan (2010)", "a count of who is sampled, shown to pose "
      "the question of external validity; its row (weird samples) is entered in Part 38")

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
shown(3, "CREDE_2017", "shown as the example of two names for nearly one thing; grit has its own row in Part "
      "28")
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
shown(4, "SCHEEL_2021", "a comparison of two literatures; shown at the frontier as early evidence on a reform; its "
      "row (registered_reports) is entered in Part 43")
shown(4, "LEVELT_2012", "the findings of an inquiry into one case of fraud")
shown(4, "DREBER_2015", "prediction markets on replications: shown at the frontier; the row "
      "(replication_prediction) is entered in Part 50")
shown(4, "PROTZKO_2023", "a retracted report about replication rates, shown at the frontier for what its "
      "retraction says about the reforms; the row (rigour_replicability) is entered in Part 50")

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
      "Part 4's file drawer in an industry; Part 42 uses it as the record behind its row on the published size of "
      "therapy's effect")

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
shown(17, "ADAMS_DICKINSON_1981", "the devaluation test, described as a method for telling habits from goals")
shown(17, "MOMENNEJAD_2017", "a test of the successor representation, described with its partial result")
shown(17, "HOWE_2013", "dopamine ramps, described at the frontier of the dopamine story")
shown(17, "DABNEY_2020", "a distributional code, described; replicated in a second region since")
shown(17, "REDISH_2004", "a model, run on Psyche; the findings on addiction are entered in Part 41")
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
shown(18, "MACKWORTH_1948", "the vigilance decrement, revisited from Part 12; its row (vigilance_decrement) is "
      "entered in Part 51")
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
shown(16, "PRENDERGAST_2006", "a meta-analysis quoted for its effect sizes; its row (contingency management) is "
      "entered in Part 41")
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
shown(7, "WIESEL_HUBEL_1963", "the critical period for one eye's hold on the cortex: told as history of "
      "physiology, in animals")
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
shown(8, "MAREK_2022", "a methods result at the frontier, disputed in its details; the small-sample brain-behaviour "
      "row is entered in Part 49, with its own simulation")
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
shown(9, "TURKHEIMER_2003", "one study shown as the example of a heritability that depends on the environment; its "
                            "row, with its record, is entered with intelligence in Part 32")
shown(9, "HAWORTH_2010", "a description of how an estimate changes with age; its row is entered with intelligence in "
                         "Part 32")
shown(9, "NCD_RISC_2016", "a description of populations")
shown(9, "HERITABILITY_TABLE", "meta-analytic values; the evidence is the row on twin heritability")
shown(9, "KONG_2018", "a methods result at the frontier")
shown(9, "HOWE_2022", "a methods result at the frontier")
shown(9, "YENGO_2022", "a result about height, set beside the twin estimate")
shown(9, "MARTIN_2019", "a methods result at the frontier")
shown(9, "KARAVANI_2019", "a simulation study, set beside the series' own formula")
shown(9, "BUSS_1989", "the example of a cross-cultural test; its row (mate preferences) is entered in "
      "Part 37")
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
shown(10, "SOLOMON_CORBIT_1974", "a theory, shown as a model; the findings on addiction are entered in Part 41")
shown(10, "DUNSTER_2018", "a before-and-after comparison in two schools, described as that")
shown(10, "TRAUER_2015", "a meta-analysis of a treatment; Part 42 enters the evidence on psychotherapy in general")
shown(10, "XIE_2013", "a finding in mice and its dispute, at the frontier")
shown(10, "PHOENIX_1959", "animal physiology; the human evidence is indirect and is said to be")
shown(10, "TEIGEN_1994", "a history of a textbook law, told again in Part 28: a history, not a finding")
shown(10, "ROENNEBERG_2004", "a description from a survey of sleep times; its row, on the curve "
      "through life, is entered with the lifespan in Part 31")


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
shown(11, "HALBERDA_2008", "Weber's law for number, a preview; number sense and mathematics has its row in "
      "Part 30")
shown(11, "GIBBON_1977", "Weber's law for time, shown as a pattern; the series does not study interval timing")
shown(11, "LESMES_2010", "a method at the frontier; its row (csf_channels) is entered in Part 13")
shown(11, "DEVRIES_ROSE", "a theory of the threshold, run on Psyche; its row (few_quanta) is entered in Part 13")
shown(11, "BERNOULLI_1738", "a theory of value, a preview; choices under risk are entered in Part 26, whose "
      "rows are the violations of that theory")
shown(11, "PLATEAU_1872", "a historical proposal; the power law's row is Stevens's")
shown(11, "THURSTONE_1927", "a method, run on simulated judges; Part 46 fits it to Guilford's data, also as a method "
      "without a row")

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

shown(12, "MACKWORTH_1948", "the vigilance decrement, told as the story that started the field; its row "
      "(vigilance_decrement) is entered in Part 51")
shown(12, "SEE_1995", "a meta-analysis shown for its conclusion about the watch; the vigilance row is entered "
      "in Part 51")
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
shown(14, "VONG_2024", "a modelling result at the frontier, described again in Part 30's frontier")
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

# ---------------------------------------------------------------------------
# Part 28 · Motivation
# ---------------------------------------------------------------------------
add(Finding(
    key="brain_stimulation_reward", part=28, title=r"Brain-stimulation reward",
    claim="Animals will work to receive electrical stimulation of certain brain sites, often in preference to food.",
    original=Study("Olds and Milner", 1954, n="rats", design="electrodes near the septal area; brief current in one "
                   "corner of a box, then for pressing a lever",
                   found="rats returned to the place of stimulation and pressed a lever for it again and again"),
    status="replicated",
    record=(Study("Olds", 1958, n="rats", design="many electrode sites mapped",
                  found="high press rates at some sites, none at others: a map of reward"),
            Study("Routtenberg and Lindy", 1965, n="rats", design="a short daily session with a food lever and a "
                  "stimulation lever", found="some rats chose stimulation, stopped eating and lost weight"),
            Study("Carlezon and Chartoff", 2007, n="a protocol", design="intracranial self-stimulation in rodents",
                  found="a standard laboratory method, used to measure the rewarding effects of drugs")),
    note="Among the most reproduced findings in behavioural neuroscience; what it reveals, pleasure or wanting, is the "
         "part that changed.",
    sources=("J. Olds and P. Milner, Positive reinforcement produced by electrical stimulation of septal area and "
             "other regions of rat brain, Journal of Comparative and Physiological Psychology 47 (1954) 419-427",
             "J. Olds, Self-stimulation of the brain, Science 127 (1958) 315-324",
             "A. Routtenberg and J. Lindy, Effects of the availability of rewarding septal and hypothalamic "
             "stimulation on bar pressing for food under conditions of deprivation, Journal of Comparative and "
             "Physiological Psychology 60 (1965) 158-161",
             "W. A. Carlezon and E. H. Chartoff, Intracranial self-stimulation (ICSS) in rodents to study the "
             "neurobiology of motivation, Nature Protocols 2 (2007) 2987-2995"),
    checked="2026-11-15",
))

add(Finding(
    key="overjustification", part=28, title=r"Overjustification",
    claim="An expected, tangible reward for an activity people already enjoy reduces how much they choose to do it "
          "later.",
    original=Study("Lepper, Greene and Nisbett", 1973, n="preschool children who liked drawing",
                   design="an expected award, an unexpected award, or none, for drawing; free play observed one to "
                   "two weeks later", found="the expected-award group drew about half as much as the others"),
    status="replicated",
    record=(Study("Cameron and Pierce (meta-analysis)", 1994, n="many experiments",
                  found="little overall harm from rewards"),
            Study("Deci, Koestner and Ryan (meta-analysis)", 1999, n="128 experiments",
                  found="expected, tangible, task-contingent rewards reduce free-choice interest; praise raises it"),
            Study("Cerasoli, Nicklin and Ford (meta-analysis)", 2014, n="schools and workplaces",
                  found="incentives predict the quantity of performance, intrinsic motivation its quality")),
    note="Reliable in the laboratory under the conditions the meta-analyses specify; how much it matters in schools "
         "and workplaces is contested.",
    sources=("M. R. Lepper, D. Greene and R. E. Nisbett, Undermining children's intrinsic interest with extrinsic "
             "reward: a test of the overjustification hypothesis, Journal of Personality and Social Psychology 28 "
             "(1973) 129-137",
             "E. L. Deci, Effects of externally mediated rewards on intrinsic motivation, Journal of Personality and "
             "Social Psychology 18 (1971) 105-115",
             "J. Cameron and W. D. Pierce, Reinforcement, reward, and intrinsic motivation: a meta-analysis, Review "
             "of Educational Research 64 (1994) 363-423",
             "E. L. Deci, R. Koestner and R. M. Ryan, A meta-analytic review of experiments examining the effects of "
             "extrinsic rewards on intrinsic motivation, Psychological Bulletin 125 (1999) 627-668",
             "C. P. Cerasoli, J. M. Nicklin and M. T. Ford, Intrinsic motivation and extrinsic incentives jointly "
             "predict performance: a 40-year meta-analysis, Psychological Bulletin 140 (2014) 980-1008",
             "R. M. Ryan and E. L. Deci, Self-determination theory and the facilitation of intrinsic motivation, "
             "social development, and well-being, American Psychologist 55 (2000) 68-78"),
    checked="2026-11-15",
))

add(Finding(
    key="goal_setting", part=28, title=r"Specific, difficult goals",
    claim="Specific, difficult goals lead to higher performance than vague goals such as 'do your best'.",
    original=Study("Locke", 1968, n="laboratory studies", design="specific hard goals against do-your-best",
                   found="higher performance with specific, difficult goals"),
    status="replicated",
    record=(Study("Mento, Steel and Karren (meta-analysis)", 1987, n="studies from 1966 to 1984",
                  found="a consistent advantage for specific, difficult goals"),
            Study("Locke and Latham (review)", 2002, n="hundreds of studies, laboratory and field",
                  found="the effect holds with commitment, feedback and ability; learning goals help on new, "
                  "complex tasks"),
            Study("Ordonez, Schweitzer, Galinsky and Bazerman", 2009, n="a review of cases",
                  found="narrow, hard goals can crowd out other aims and invite cheating"),
            Study("Gollwitzer and Sheeran (meta-analysis)", 2006, n="many studies of if-then plans",
                  found="implementation intentions help people reach goals")),
    note="Robust in laboratory and field; smaller for complex new tasks, and with costs when goals are narrow.",
    sources=("E. A. Locke, Toward a theory of task motivation and incentives, Organizational Behavior and Human "
             "Performance 3 (1968) 157-189",
             "A. J. Mento, R. P. Steel and R. J. Karren, A meta-analytic study of the effects of goal setting on task "
             "performance: 1966-1984, Organizational Behavior and Human Decision Processes 39 (1987) 52-83",
             "E. A. Locke and G. P. Latham, Building a practically useful theory of goal setting and task "
             "motivation: a 35-year odyssey, American Psychologist 57 (2002) 705-717",
             "L. D. Ordonez, M. E. Schweitzer, A. D. Galinsky and M. H. Bazerman, Goals gone wild: the systematic "
             "side effects of overprescribing goal setting, Academy of Management Perspectives 23 (2009) 6-16",
             "P. M. Gollwitzer, Implementation intentions: strong effects of simple plans, American Psychologist 54 "
             "(1999) 493-503",
             "P. M. Gollwitzer and P. Sheeran, Implementation intentions and goal achievement: a meta-analysis of "
             "effects and processes, Advances in Experimental Social Psychology 38 (2006) 69-119"),
    checked="2026-11-15",
))

add(Finding(
    key="ego_depletion", part=28, title=r"Ego depletion",
    claim="Exerting self-control on one task impairs self-control on the next, as if a limited resource were used "
          "up.",
    original=Study("Baumeister, Bratslavsky, Muraven and Tice", 1998, n="undergraduates",
                   design="resist chocolate cookies and eat radishes, or eat the cookies; then unsolvable puzzles",
                   found="the radish eaters gave up much sooner"),
    status="failed",
    record=(Study("Hagger, Wood, Stiff and Chatzisarantis (meta-analysis)", 2010, n="198 tests", effect=0.62,
                  unit="d", found="a medium-to-large, consistent average effect"),
            Study("Carter, Kofler, Forster and McCullough", 2015, n="the published and unpublished literature",
                  design="corrections for small-study bias", found="corrected estimates near zero"),
            Study("Hagger, Chatzisarantis et al. (registered, multisite)", 2016, n="23 laboratories, 2,141 people",
                  effect=0.04, unit="d", lo=-0.07, hi=0.15, found="d = 0.04, 95% CI -0.07 to 0.15"),
            Study("Vohs et al. (registered, multisite)", 2021, n="36 laboratories, 3,531 people", effect=0.06,
                  unit="d", design="tasks chosen with the theory's proponents",
                  found="d = 0.06, not significant; the data favoured no effect")),
    note="Failed in its sequential-task form in two registered multisite tests; fatigue after effort is real, a "
         "limited resource is not supported.",
    sources=("R. F. Baumeister, E. Bratslavsky, M. Muraven and D. M. Tice, Ego depletion: is the active self a "
             "limited resource?, Journal of Personality and Social Psychology 74 (1998) 1252-1265",
             "M. T. Gailliot et al., Self-control relies on glucose as a limited energy source: willpower is more "
             "than a metaphor, Journal of Personality and Social Psychology 92 (2007) 325-336",
             "R. Kurzban, Does the brain consume additional glucose during self-control tasks?, Evolutionary "
             "Psychology 8 (2010) 244-259",
             "M. S. Hagger, C. Wood, C. Stiff and N. L. D. Chatzisarantis, Ego depletion and the strength model of "
             "self-control: a meta-analysis, Psychological Bulletin 136 (2010) 495-525",
             "E. C. Carter, L. M. Kofler, D. E. Forster and M. E. McCullough, A series of meta-analytic tests of the "
             "depletion effect: self-control does not seem to rely on a limited resource, Journal of Experimental "
             "Psychology: General 144 (2015) 796-815",
             "C. Sripada, D. Kessler and J. Jonides, Methylphenidate blocks effort-induced depletion of regulatory "
             "control in healthy volunteers, Psychological Science 25 (2014) 1227-1234",
             "M. S. Hagger, N. L. D. Chatzisarantis et al., A multilab preregistered replication of the "
             "ego-depletion effect, Perspectives on Psychological Science 11 (2016) 546-573",
             "R. F. Baumeister and K. D. Vohs, Misguided effort with elusive implications, Perspectives on "
             "Psychological Science 11 (2016) 574-575",
             "K. D. Vohs et al., A multisite preregistered paradigmatic test of the ego-depletion effect, "
             "Psychological Science 32 (2021) 1566-1581"),
    checked="2026-11-15",
    data=("EGO_DEPLETION_RRR",),
))

add(Finding(
    key="delay_of_gratification", part=28, title=r"Delay of gratification predicts outcomes",
    claim="How long a preschooler waits for a larger treat predicts achievement years later.",
    original=Study("Shoda, Mischel and Peake", 1990, n="a few dozen children from Stanford's nursery school",
                   design="waiting at four; test scores in adolescence",
                   found="children who waited longer had higher scores"),
    status="replicated, smaller",
    record=(Study("Kidd, Palmeri and Aslin", 2013, n="young children", design="a reliable or an unreliable "
                  "experimenter before the test", found="children waited far longer after a reliable adult"),
            Study("McGuire and Kable", 2013, n="adults", design="waiting when the delay's distribution varies",
                  found="persistence adjusted to the timing statistics, as a rational account predicts"),
            Study("Watts, Duncan and Quan", 2018, n="about 900 children from many backgrounds",
                  design="a conceptual replication with controls",
                  found="about half the original association; about two-thirds smaller again with background "
                  "controlled")),
    note="The association exists but is small and largely shared with family background and early ability; "
         "waiting also reflects how trustworthy the world seems.",
    sources=("W. Mischel, E. B. Ebbesen and A. R. Zeiss, Cognitive and attentional mechanisms in delay of "
             "gratification, Journal of Personality and Social Psychology 21 (1972) 204-218",
             "Y. Shoda, W. Mischel and P. K. Peake, Predicting adolescent cognitive and self-regulatory competencies "
             "from preschool delay of gratification: identifying diagnostic conditions, Developmental Psychology 26 "
             "(1990) 978-986",
             "W. Mischel, Y. Shoda and M. L. Rodriguez, Delay of gratification in children, Science 244 (1989) "
             "933-938",
             "C. Kidd, H. Palmeri and R. N. Aslin, Rational snacking: young children's decision-making on the "
             "marshmallow task is moderated by beliefs about environmental reliability, Cognition 126 (2013) 109-114",
             "J. T. McGuire and J. W. Kable, Rational temporal predictions can underlie apparent failures to delay "
             "gratification, Psychological Review 120 (2013) 395-410",
             "T. W. Watts, G. J. Duncan and H. Quan, Revisiting the marshmallow test: a conceptual replication "
             "investigating links between early delay of gratification and later outcomes, Psychological Science 29 "
             "(2018) 1159-1177"),
    checked="2026-11-15",
))

add(Finding(
    key="grit", part=28, title=r"Grit beyond conscientiousness",
    claim="Grit, perseverance and passion for long-term goals, predicts achievement beyond conscientiousness.",
    original=Study("Duckworth, Peterson, Matthews and Kelly", 2007, n="several samples, including West Point cadets "
                   "and spelling-bee finalists", design="a short grit questionnaire",
                   found="grit predicted retention and progress"),
    status="contested",
    record=(Study("Rimfeld, Kovas, Dale and Plomin", 2016, n="a UK twin sample",
                  found="grit added little to the prediction of exam results beyond the Big Five"),
            Study("Crede, Tynan and Harms (meta-analysis)", 2017, n="88 samples, 66,807 people",
                  found="grit and performance rho = .18; grit and conscientiousness rho = .84")),
    note="Grit predicts modestly and is nearly conscientiousness; whether it adds anything beyond it is contested.",
    sources=("A. L. Duckworth, C. Peterson, M. D. Matthews and D. R. Kelly, Grit: perseverance and passion for "
             "long-term goals, Journal of Personality and Social Psychology 92 (2007) 1087-1101",
             "K. Rimfeld, Y. Kovas, P. S. Dale and R. Plomin, True grit and genetics: predicting academic achievement "
             "from personality, Journal of Personality and Social Psychology 111 (2016) 780-789",
             "M. Crede, M. C. Tynan and P. D. Harms, Much ado about grit: a meta-analytic synthesis of the grit "
             "literature, Journal of Personality and Social Psychology 113 (2017) 492-511"),
    checked="2026-11-15",
    data=("CREDE_2017",),
))

# ---------------------------------------------------------------------------
# Part 29 · Emotion
# ---------------------------------------------------------------------------
add(Finding(
    key="schachter_singer", part=29, title=r"Arousal plus a label",
    claim="Unexplained physiological arousal is felt as whatever emotion the situation suggests.",
    original=Study("Schachter and Singer", 1962, n="185 men", design="adrenaline or placebo, informed or not about "
                   "its effects, with a euphoric or an angry confederate",
                   found="uninformed participants tended to take on the confederate's mood; the effects were weak and "
                   "mixed"),
    status="contested",
    record=(Study("Marshall and Zimbardo", 1979, n="students", design="the euphoria conditions repeated",
                  found="adrenaline did not make people more euphoric"),
            Study("Maslach", 1979, n="students", design="arousal by hypnotic suggestion, left unexplained",
                  found="unexplained arousal was felt as negative, whatever the confederate did"),
            Study("Reisenzein (review)", 1983, n="a review", design="the two-factor literature",
                  found="little evidence that arousal is necessary for emotion; misattribution of arousal occurs, "
                  "within limits")),
    note="Arousal can be misattributed, but the strong claim, that emotion is arousal plus a label, did not survive.",
    sources=("S. Schachter and J. E. Singer, Cognitive, social, and physiological determinants of emotional state, "
             "Psychological Review 69 (1962) 379-399",
             "G. D. Marshall and P. G. Zimbardo, Affective consequences of inadequately explained physiological "
             "arousal, Journal of Personality and Social Psychology 37 (1979) 970-988",
             "C. Maslach, Negative emotional biasing of unexplained arousal, Journal of Personality and Social "
             "Psychology 37 (1979) 953-969",
             "R. Reisenzein, The Schachter theory of emotion: two decades later, Psychological Bulletin 94 (1983) "
             "239-264"),
    checked="2026-11-15",
))

add(Finding(
    key="bridge_misattribution", part=29, title=r"The fear bridge",
    claim="Men who met a woman on a frightening bridge were more attracted to her, mistaking fear for attraction.",
    original=Study("Dutton and Aron", 1974, n="men crossing two bridges in North Vancouver",
                   design="an interviewer on a swaying suspension bridge or a low, solid one; who later phoned her",
                   found="more men called from the high bridge (9 of 18 who took her number, against 2 of 16)"),
    status="not directly tested",
    record=(Study("Foster, Witcher, Campbell and Green (meta-analysis)", 1998, n="the laboratory experiments",
                  design="arousal and attraction in the laboratory",
                  found="arousal increased attraction, though not only through misattribution"),),
    note="The bridge itself has not been directly replicated at scale; arousal-attraction effects in the "
         "laboratory are real, and their mechanism is argued.",
    sources=("D. G. Dutton and A. P. Aron, Some evidence for heightened sexual attraction under conditions of high "
             "anxiety, Journal of Personality and Social Psychology 30 (1974) 510-517",
             "C. A. Foster, B. S. Witcher, W. K. Campbell and J. D. Green, Arousal and attraction: evidence for "
             "automatic and controlled processes, Journal of Personality and Social Psychology 74 (1998) 86-101"),
    checked="2026-11-15",
))

add(Finding(
    key="universal_expressions", part=29, title=r"Six universally recognized expressions",
    claim="People in every culture recognize the same six emotions from the same facial expressions.",
    original=Study("Ekman and Friesen", 1971, n="Fore villagers in New Guinea",
                   design="a short story and three photographs; choose the face that fits",
                   found="matching far above chance for most emotions; fear and surprise were confused"),
    status="contested",
    record=(Study("Russell (review)", 1994, n="a review", design="the cross-cultural method",
                  found="forced choice among a few labels inflates agreement; agreement falls without it"),
            Study("Gendron, Roberson, van der Vyver and Barrett", 2014, n="Himba and US participants",
                  design="free sorting of 36 faces, with and without emotion words",
                  found="Himba sorted without the six piles; closer with words supplied"),
            Study("Barrett, Adolphs, Marsella, Martinez and Pollak (review)", 2019, n="a review",
                  design="reliability, specificity, generalizability and validity",
                  found="the faces are neither reliable nor specific signals; people scowl in anger about a quarter "
                  "of the time")),
    note="With forced choice the classic pattern replicates widely; with free responses and in small-scale "
         "societies it weakens, and what faces signal is contested.",
    sources=("P. Ekman and W. V. Friesen, Constants across cultures in the face and emotion, Journal of "
             "Personality and Social Psychology 17 (1971) 124-129",
             "J. A. Russell, Is there universal recognition of emotion from facial expression? A review of the "
             "cross-cultural studies, Psychological Bulletin 115 (1994) 102-141",
             "M. Gendron, D. Roberson, J. M. van der Vyver and L. F. Barrett, Perceptions of emotion from facial "
             "expressions are not culturally universal: evidence from a remote culture, Emotion 14 (2014) 251-262",
             "L. F. Barrett, R. Adolphs, S. Marsella, A. M. Martinez and S. D. Pollak, Emotional expressions "
             "reconsidered: challenges to inferring emotion from human facial movements, Psychological Science in "
             "the Public Interest 20 (2019) 1-68"),
    checked="2026-11-15",
))

add(Finding(
    key="facial_feedback", part=29, title=r"Facial feedback",
    claim="Moving the face into an expression changes the emotion felt.",
    original=Study("Strack, Martin and Stepper", 1988, n="undergraduates",
                   design="a pen held in the teeth (a smile) or the lips (a pout) while rating cartoons",
                   effect=0.82, unit="points on a 10-point scale", found="cartoons rated 0.82 points funnier with "
                   "the pen in the teeth"),
    status="replicated, smaller",
    record=(Study("Wagenmakers et al. (registered, 17 laboratories)", 2016, n="17 laboratories", effect=0.03,
                  unit="points on a 10-point scale", lo=-0.11, hi=0.16, found="0.03 points, 95% CI -0.11 to 0.16"),
            Study("Noah, Schul and Mayo", 2018, n="students", design="with and without a camera",
                  found="the effect appeared without a camera and vanished when participants were filmed"),
            Study("Coles, Larsen and Lench (meta-analysis)", 2019, n="286 effects from 138 studies",
                  effect=0.20, unit="d", found="small and variable, about d = 0.2"),
            Study("Coles et al. (Many Smiles Collaboration)", 2022, n="3,878 people in 19 countries",
                  design="mimicry, voluntary posing and the pen, preregistered",
                  found="posed and mimicked smiles raised happiness; the pen gave inconclusive results")),
    note="Deliberate expressions change feelings a little; the unobtrusive pen manipulation is unreliable, and the "
         "effect depends on the task.",
    sources=("F. Strack, L. L. Martin and S. Stepper, Inhibiting and facilitating conditions of the human smile: a "
             "nonobtrusive test of the facial feedback hypothesis, Journal of Personality and Social Psychology 54 "
             "(1988) 768-777",
             "E.-J. Wagenmakers et al., Registered Replication Report: Strack, Martin, & Stepper (1988), "
             "Perspectives on Psychological Science 11 (2016) 917-928",
             "T. Noah, Y. Schul and R. Mayo, When both the original study and its failed replication are correct: "
             "feeling observed eliminates the facial-feedback effect, Journal of Personality and Social Psychology "
             "114 (2018) 657-664",
             "N. A. Coles, J. T. Larsen and H. C. Lench, A meta-analysis of the facial feedback literature, "
             "Psychological Bulletin 145 (2019) 610-651",
             "N. A. Coles et al., A multi-lab test of the facial feedback hypothesis by the Many Smiles "
             "Collaboration, Nature Human Behaviour 6 (2022) 1731-1742"),
    checked="2026-11-15",
    data=("COLES_2019",),
))

add(Finding(
    key="money_wellbeing", part=29, title=r"Money and well-being",
    claim="Emotional well-being rises with income, but stops rising above a moderate income.",
    original=Study("Kahneman and Deaton", 2010, n="about 450,000 Gallup responses",
                   design="yesterday's emotions and life evaluation against household income",
                   found="emotional well-being levelled off above about 75,000 dollars a year; life evaluation kept rising"),
    status="replicated",
    record=(Study("Killingsworth", 2021, n="1,725,994 reports from 33,391 employed US adults",
                  design="experience sampling by smartphone",
                  found="experienced well-being rose with log income, with no plateau above 75,000 dollars"),
            Study("Killingsworth, Kahneman and Mellers (adversarial collaboration)", 2023, n="the 2021 data",
                  design="happiness percentiles against income",
                  found="a plateau above about 100,000 dollars only for the least happy fifth; for others it kept rising")),
    note="Well-being rises with log income for most people; the 2010 plateau described the unhappiest, and an "
         "adversarial collaboration reconciled the two findings.",
    sources=("D. Kahneman and A. Deaton, High income improves evaluation of life but not emotional well-being, "
             "Proceedings of the National Academy of Sciences 107 (2010) 16489-16493",
             "M. A. Killingsworth, Experienced well-being rises with income, even above $75,000 per year, "
             "Proceedings of the National Academy of Sciences 118 (2021) e2016976118",
             "M. A. Killingsworth, D. Kahneman and B. Mellers, Income and emotional well-being: a conflict "
             "resolved, Proceedings of the National Academy of Sciences 120 (2023) e2208661120"),
    checked="2026-11-15",
))

add(Finding(
    key="positivity_ratio", part=29, title=r"The critical positivity ratio",
    claim="People flourish when their ratio of positive to negative emotions exceeds 2.9013.",
    original=Study("Fredrickson and Losada", 2005, n="188 people",
                   design="emotion diaries, with a ratio derived from Losada's Lorenz-equation model of teams",
                   found="flourishers above 2.9, others below"),
    status="retracted",
    record=(Study("Brown, Sokal and Friedman", 2013, n="a reanalysis", design="the model's mathematics",
                  found="the equations' use was unfounded; the 2.9013 threshold has no basis"),
            Study("American Psychologist (correction)", 2013, n="the journal",
                  design="formal withdrawal", found="the modelling and its predictions withdrawn; the rest of the "
                  "paper stands")),
    note="The number was withdrawn; that more positive emotion goes with better mental health, within limits, was "
         "not.",
    sources=("B. L. Fredrickson and M. F. Losada, Positive affect and the complex dynamics of human flourishing, "
             "American Psychologist 60 (2005) 678-686",
             "N. J. L. Brown, A. D. Sokal and H. L. Friedman, The complex dynamics of wishful thinking: the critical "
             "positivity ratio, American Psychologist 68 (2013) 801-813",
             "B. L. Fredrickson, Updated thinking on positivity ratios, American Psychologist 68 (2013) 814-822"),
    checked="2026-11-15",
))

# ---------------------------------------------------------------------------
# Part 30 · The Infant Mind
# ---------------------------------------------------------------------------
add(Finding(
    key="a_not_b", part=30, title=r"The A-not-B error",
    claim="Infants of about eight to twelve months, having found a toy at A, search at A after seeing it hidden at B.",
    original=Study("Piaget", 1937, n="his own three children", design="hiding games, observed and described",
                   found="search returned to the place of earlier success"),
    status="replicated",
    record=(Study("Diamond", 1985, n="infants followed monthly", design="A-not-B with delays",
                  found="the delay needed to produce the error grew with age"),
            Study("Wellman, Cross and Bartsch (meta-analysis)", 1987, n="the published studies",
                  design="A-not-B studies pooled", found="the error is reliable and depends on delay and number of "
                  "locations"),
            Study("Smith, Thelen, Titzer and McLin", 1999, n="infants", design="manipulations of the task and posture",
                  found="the error appears without any hidden toy and disappears when posture changes")),
    note="One of the most reliable findings in infancy; what it shows, a missing concept or the dynamics of reaching "
         "and memory, is argued.",
    sources=("J. Piaget, La construction du reel chez l'enfant (1937); The Construction of Reality in the Child (1954)",
             "A. Diamond, Development of the ability to use recall to guide action, as indicated by infants' "
             "performance on AB, Child Development 56 (1985) 868-883",
             "H. M. Wellman, D. Cross and K. Bartsch, Infant search and object permanence: a meta-analysis of the "
             "A-not-B error, Monographs of the Society for Research in Child Development 51 (1987)",
             "L. B. Smith, E. Thelen, R. Titzer and D. McLin, Knowing in the context of acting: the task dynamics of "
             "the A-not-B error, Psychological Review 106 (1999) 235-260"),
    checked="2026-11-15",
))

add(Finding(
    key="infant_object_permanence", part=30, title=r"Object permanence by looking",
    claim="Infants of three to five months know that a hidden object still exists and cannot be passed through.",
    original=Study("Baillargeon, Spelke and Wasserman", 1985, n="5-month-olds",
                   design="a screen rotating like a drawbridge toward a hidden box",
                   found="longer looks at the screen rotating through the box's space"),
    status="contested",
    record=(Study("Baillargeon", 1987, n="3.5- and 4.5-month-olds", design="the same design with controls",
                  found="4.5-month-olds, and fast-habituating 3.5-month-olds, looked longer at the impossible event"),
            Study("Bogartz, Shinskey and Schilling", 2000, n="5.5-month-olds",
                  design="familiarization varied", found="preferences followed familiarization; the authors concluded "
                  "the design does not show object permanence")),
    note="The looking pattern replicates in its laboratory; reading it as knowledge of hidden objects, rather than "
         "familiarity and motion, is contested.",
    sources=("R. Baillargeon, E. S. Spelke and S. Wasserman, Object permanence in five-month-old infants, Cognition 20 "
             "(1985) 191-208",
             "R. Baillargeon, Object permanence in 3 1/2- and 4 1/2-month-old infants, Developmental Psychology 23 "
             "(1987) 655-664",
             "R. S. Bogartz, J. L. Shinskey and T. H. Schilling, Object permanence in five-and-a-half-month-old "
             "infants?, Infancy 1 (2000) 403-428"),
    checked="2026-11-15",
))

add(Finding(
    key="infant_arithmetic", part=30, title=r"Infant arithmetic",
    claim="Five-month-olds expect one object plus one object to make two.",
    original=Study("Wynn", 1992, n="5-month-olds", design="dolls added or removed behind a screen",
                   found="longer looks at impossible outcomes"),
    status="contested",
    record=(Study("Wakeley, Rivera and Langer", 2000, n="5-month-olds", design="a careful repetition",
                  found="no reliable effect"),
            Study("Christodoulou, Lac and Moore (meta-analysis)", 2017, n="12 studies, 26 samples, 550 infants",
                  effect=0.34, unit="d", found="d = 0.34; publication bias suggested by some tests and not others")),
    note="The looking pattern is probably real and smaller than first reported; whether it reflects arithmetic, "
         "rather than familiarity, is contested.",
    sources=("K. Wynn, Addition and subtraction by human infants, Nature 358 (1992) 749-750",
             "Wakeley, S. Rivera and J. Langer, Can young infants add and subtract?, Child Development 71 (2000) "
             "1525-1534",
             "J. Christodoulou, A. Lac and D. S. Moore, Babies and math: a meta-analysis of infants' simple arithmetic "
             "competence, Developmental Psychology 53 (2017) 1405-1417"),
    checked="2026-11-15",
))

add(Finding(
    key="ans_math", part=30, title=r"Number sense and mathematics",
    claim="The acuity of the approximate number system predicts mathematics achievement.",
    original=Study("Halberda, Mazzocco and Feigenson", 2008, n="14-year-olds",
                   design="dot-array comparison against past mathematics scores",
                   found="acuity correlated with mathematics scores back to kindergarten"),
    status="replicated, smaller",
    record=(Study("Chen and Li (meta-analysis)", 2014, n="the published studies", effect=0.20, unit="r",
                  found="a small positive correlation, about 0.2"),
            Study("Schneider et al. (meta-analysis)", 2017, n="45 articles, 284 effects",
                  found="non-symbolic relations present but weak, especially beyond age six")),
    note="A real, small correlation, partly shared with general ability; training the system has not reliably "
         "improved mathematics.",
    sources=("J. Halberda, M. M. M. Mazzocco and L. Feigenson, Individual differences in non-verbal number acuity "
             "correlate with maths achievement, Nature 455 (2008) 665-668",
             "Q. Chen and J. Li, Association between individual differences in non-symbolic number acuity and math "
             "performance: a meta-analysis, Acta Psychologica 148 (2014) 163-172",
             "M. Schneider et al., Associations of non-symbolic and symbolic numerical magnitude processing with "
             "mathematical competence: a meta-analysis, Developmental Science 20 (2017) e12372"),
    checked="2026-11-15",
))

add(Finding(
    key="false_belief_explicit", part=30, title=r"False belief at four",
    claim="Children begin to pass explicit false-belief tasks at about four years.",
    original=Study("Wimmer and Perner", 1983, n="children aged 3 to 9", design="Maxi and the chocolate",
                   found="most younger children answered where the chocolate was; older children, where Maxi left it"),
    status="replicated",
    record=(Study("Baron-Cohen, Leslie and Frith", 1985, n="typical, Down syndrome and autistic children",
                  design="the Sally-Anne task", found="most typical 4-year-olds passed"),
            Study("Wellman, Cross and Watson (meta-analysis)", 2001, n="178 studies",
                  design="false-belief tasks pooled", found="a consistent shift with age across countries and "
                  "task versions")),
    note="One of developmental psychology's most robust findings; its interpretation as a new concept, against new "
         "processing abilities, is argued.",
    sources=("H. Wimmer and J. Perner, Beliefs about beliefs, Cognition 13 (1983) 103-128",
             "S. Baron-Cohen, A. M. Leslie and U. Frith, Does the autistic child have a 'theory of mind'?, Cognition "
             "21 (1985) 37-46",
             "H. M. Wellman, D. Cross and J. Watson, Meta-analysis of theory-of-mind development: the truth about "
             "false belief, Child Development 72 (2001) 655-684"),
    checked="2026-11-15",
))

add(Finding(
    key="false_belief_implicit", part=30, title=r"False belief in infants",
    claim="Infants of about fifteen months expect people to act on false beliefs, shown by looking.",
    original=Study("Onishi and Baillargeon", 2005, n="15-month-olds", design="violation of expectation",
                   found="longer looks when the actor searched where the toy really was"),
    status="contested",
    record=(Study("Kulke, von Duhn, Schneider and Rakoczy (preregistered)", 2018, n="four anticipatory-looking tasks",
                  design="systematic replication", found="one task replicated, and not once confounds were removed"),
            Study("Powell, Hobbs, Bardis, Carey and Saxe", 2018, n="infants", design="looking-time and helping "
                  "tasks", found="the looking-time tasks failed to replicate")),
    note="Several preregistered replications of implicit tasks failed; multi-laboratory tests are under way.",
    sources=("K. H. Onishi and R. Baillargeon, Do 15-month-old infants understand false beliefs?, Science 308 (2005) "
             "255-258",
             "L. Kulke, B. von Duhn, D. Schneider and H. Rakoczy, Is implicit theory of mind a real and robust "
             "phenomenon? Results from a systematic replication study, Psychological Science 29 (2018)",
             "L. J. Powell, K. Hobbs, A. Bardis, S. Carey and R. Saxe, Replications of implicit theory of mind tasks "
             "with varying representational demands, Cognitive Development 46 (2018) 40-50"),
    checked="2026-11-15",
))

add(Finding(
    key="neonatal_imitation", part=30, title=r"Newborn imitation",
    claim="Newborns imitate facial gestures such as tongue protrusion.",
    original=Study("Meltzoff and Moore", 1977, n="infants 12 to 21 days old",
                   design="an adult models tongue protrusion, mouth opening and lip protrusion",
                   found="infants produced the modelled gesture more often"),
    status="contested",
    record=(Study("Oostenbroek et al. (longitudinal)", 2016, n="106 infants at 1, 3, 6 and 9 weeks",
                  design="eleven gestures, matching against control models",
                  found="gestures as frequent after control models as after matching ones"),
            Study("Meltzoff et al. (reanalysis)", 2018, n="the 2016 data", design="tongue protrusion alone",
                  found="tongue protrusion matched")),
    note="The largest longitudinal study found no imitation; tongue protrusion, the one disputed gesture, is also "
         "a general response to arousal.",
    sources=("A. N. Meltzoff and M. K. Moore, Imitation of facial and manual gestures by human neonates, Science 198 "
             "(1977) 75-78",
             "J. Oostenbroek et al., Comprehensive longitudinal study challenges the existence of neonatal imitation "
             "in humans, Current Biology 26 (2016) 1334-1338",
             "A. N. Meltzoff et al., Re-examination of Oostenbroek et al. (2016): evidence for neonatal imitation of "
             "tongue protrusion, Developmental Science 21 (2018) e12609"),
    checked="2026-11-15",
))

add(Finding(
    key="ids_preference", part=30, title=r"Infant-directed speech",
    claim="Infants prefer to listen to infant-directed speech over adult-directed speech.",
    original=Study("Fernald", 1985, n="4-month-olds", design="head turns produced recordings of either kind",
                   found="infants turned more often to produce infant-directed speech"),
    status="replicated",
    record=(Study("ManyBabies Consortium (registered, multi-laboratory)", 2020, n="65 laboratories, 2,179 infants in "
                  "the shared table", effect=0.35, unit="d", lo=0.29, hi=0.42,
                  found="d = 0.35, larger with age, with head-turn preference, and with native-language stimuli"),),
    note="Replicated at scale, smaller than earlier estimates, and dependent on method, age and language.",
    sources=("A. Fernald, Four-month-old infants prefer to listen to motherese, Infant Behavior and Development 8 "
             "(1985) 181-195",
             "ManyBabies Consortium, Quantifying sources of variability in infancy research using the "
             "infant-directed-speech preference, Advances in Methods and Practices in Psychological Science 3 (2020) "
             "24-52"),
    checked="2026-11-15",
    data=("MANYBABIES_2020",),
))

add(Finding(
    key="deprivation_foster_care", part=31, title=r"Early deprivation, and early placement",
    claim="Early institutional deprivation harms development, and placement in a family early in life helps.",
    original=Study("Nelson, Zeanah, Fox and colleagues (randomized)", 2007, n="136 children in Bucharest's "
                   "institutions, aged 6 to 31 months", design="a lottery assigned foster care or care as usual",
                   found="foster care raised IQ, most for the children placed youngest"),
    status="replicated",
    record=(Study("Sonuga-Barke and colleagues (English and Romanian Adoptees)", 2017, n="Romanian adoptees in "
                  "British families, followed to ages 22 to 25", found="more than six months of deprivation: "
                  "problems persisting into adulthood; IQ recovered"),
            Study("Humphreys and colleagues (the randomized trial at 18)", 2022, n="135 participants", effect=9.0,
                  unit="IQ points", found="about 9 IQ points (0.6 SD) higher with foster care, partly through "
                  "caregiving and attachment"),),
    note="A randomized trial and a natural experiment agree; the trial is one city, and its IQ effect at 18 sits near "
         "the edge of significance.",
    sources=("C. A. Nelson, C. H. Zeanah, N. A. Fox, P. J. Marshall, A. T. Smyke and D. Guthrie, Cognitive recovery "
             "in socially deprived young children: the Bucharest Early Intervention Project, Science 318 (2007) "
             "1937-1940",
             "E. J. S. Sonuga-Barke et al., Child-to-adult neurodevelopmental and mental health trajectories after "
             "early life deprivation: the young adult follow-up of the longitudinal English and Romanian Adoptees "
             "study, Lancet 389 (2017) 1539-1548",
             "K. L. Humphreys et al., Foster care leads to sustained cognitive gains following severe early "
             "deprivation, PNAS 119 (2022)"),
    checked="2026-11-15",
))

add(Finding(
    key="perry_long_run", part=31, title=r"Preschool's effects in adulthood",
    claim="A preschool programme for poor three- and four-year-olds improved their lives as adults, decades later.",
    original=Study("Schweinhart and colleagues (Perry Preschool, age 40)", 2005, n="123 children, 58 in the "
                   "programme", design="assignment by a near-random procedure, 1962 to 1967",
                   found="at 40: more employed (76% against 62%), higher earnings, fewer arrests"),
    status="replicated, smaller",
    record=(Study("Anderson (reanalysis for many outcomes)", 2008, n="Perry, Abecedarian and Early Training",
                  found="substantial gains for girls; no significant long-term benefits for boys"),
            Study("Heckman and colleagues (reanalysis)", 2010, n="the Perry sample", design="the compromised "
                  "assignment modelled", found="a social rate of return of about 7 to 10% a year"),
            Study("Campbell and colleagues (Abecedarian, randomized)", 2014, n="the participants in their "
                  "mid-thirties", found="better cardiovascular and metabolic health in treated men"),),
    note="Long-run effects survive reanalysis, smaller and narrower than first claimed; each trial is small.",
    sources=("L. J. Schweinhart, J. Montie, Z. Xiang, W. S. Barnett, C. R. Belfield and M. Nores, Lifetime Effects: "
             "The High/Scope Perry Preschool Study Through Age 40 (High/Scope Press, 2005)",
             "M. L. Anderson, Multiple inference and gender differences in the effects of early intervention, "
             "Journal of the American Statistical Association 103 (2008) 1481-1495",
             "J. J. Heckman, S. H. Moon, R. Pinto, P. A. Savelyev and A. Yavitz, The rate of return to the HighScope "
             "Perry Preschool Program, Journal of Public Economics 94 (2010) 114-128",
             "F. Campbell et al., Early childhood investments substantially boost adult health, Science 343 (2014) "
             "1478-1485"),
    checked="2026-11-15",
))

add(Finding(
    key="word_gap", part=31, title=r"The thirty-million-word gap",
    claim="By age four, children in poor families have heard about 30 million fewer words than children in "
          "professional families.",
    original=Study("Hart and Risley", 1995, n="42 Kansas families", design="one hour recorded each month",
                   found="a projected gap of about 30 million words by age four"),
    status="contested",
    record=(Study("Gilkerson and colleagues", 2017, n="3,213 day-long automated recordings",
                  found="fewer adult words in lower-income homes, with wide variation in every group"),
            Study("Sperry, Sperry and Miller", 2019, n="42 children in five communities",
                  found="counting overheard speech too, no gap by income"),),
    note="Children who hear more talk directed at them learn more words; the size, the cause and the measurement "
         "of the gap are disputed.",
    sources=("B. Hart and T. R. Risley, Meaningful Differences in the Everyday Experience of Young American Children "
             "(Brookes, 1995)",
             "J. Gilkerson et al., Mapping the early language environment using all-day recordings and automated "
             "analysis, American Journal of Speech-Language Pathology 26 (2017) 248-265",
             "D. E. Sperry, L. L. Sperry and P. J. Miller, Reexamining the verbal environments of children from "
             "different socioeconomic backgrounds, Child Development 90 (2019) 1303-1318"),
    checked="2026-11-15",
))

add(Finding(
    key="adult_neurogenesis", part=31, title=r"New neurons in the adult human brain",
    claim="The adult human hippocampus keeps making new neurons into old age.",
    original=Study("Eriksson, Gage and colleagues", 1998, n="5 cancer patients given a marker of dividing cells",
                   found="new neurons in the hippocampus after death"),
    status="contested",
    record=(Study("Sorrells and colleagues", 2018, n="post-mortem and surgical tissue",
                  found="new neurons fell steeply through childhood; none detectable in adults"),
            Study("Boldrini and colleagues", 2018, n="post-mortem brains, ages 14 to 79",
                  found="immature neurons throughout adulthood"),
            Study("Moreno-Jimenez and colleagues", 2019, n="post-mortem brains, with tightly controlled fixation",
                  found="immature neurons into old age, fewer in Alzheimer's disease"),),
    note="The disagreement is largely about tissue handling and markers; neither side's result is settled.",
    sources=("P. S. Eriksson et al., Neurogenesis in the adult human hippocampus, Nature Medicine 4 (1998) 1313-1317",
             "S. F. Sorrells et al., Human hippocampal neurogenesis drops sharply in children to undetectable levels "
             "in adults, Nature 555 (2018) 377-381",
             "M. Boldrini et al., Human hippocampal neurogenesis persists throughout aging, Cell Stem Cell 22 (2018) "
             "589-599",
             "E. P. Moreno-Jimenez et al., Adult hippocampal neurogenesis is abundant in neurologically healthy "
             "subjects and drops sharply in patients with Alzheimer's disease, Nature Medicine 25 (2019) 554-560"),
    checked="2026-11-15",
))

add(Finding(
    key="birth_order_personality", part=31, title=r"Birth order and personality",
    claim="Birth order shapes personality: firstborns are more conscientious, later-borns more open.",
    original=Study("Sulloway", 1996, n="historical figures and published studies", design="a book-length synthesis",
                   found="later-borns more open to new ideas, firstborns more dominant and conscientious"),
    status="failed",
    record=(Study("Rohrer, Egloff and Schmukle (within and between families)", 2015, n="more than 20,000 adults in "
                  "three national panels", found="no birth-order effects on the Big Five"),
            Study("Damian and Roberts", 2015, n="377,000 American high-school students", effect=0.02, unit="r",
                  found="an average correlation of 0.02 with personality traits"),),
    note="Large samples, compared within families, find nothing of practical size.",
    sources=("F. J. Sulloway, Born to Rebel: Birth Order, Family Dynamics, and Creative Lives (Pantheon, 1996)",
             "J. M. Rohrer, B. Egloff and S. C. Schmukle, Examining the effects of birth order on personality, PNAS "
             "112 (2015) 14224-14229",
             "R. I. Damian and B. W. Roberts, The associations of birth order with personality and intelligence in a "
             "representative sample of U.S. high school students, Journal of Research in Personality 58 (2015)"),
    checked="2026-11-15",
))

add(Finding(
    key="birth_order_iq", part=31, title=r"Birth order and IQ",
    claim="Firstborns score slightly higher on intelligence tests than their younger siblings.",
    original=Study("Belmont and Marolla", 1973, n="nearly 400,000 Dutch 19-year-old men",
                   design="Raven's matrices at military induction",
                   found="scores fell with each later birth and with family size"),
    status="replicated",
    record=(Study("Kristensen and Bjerkedal", 2007, n="241,310 Norwegian conscripts",
                  found="eldest sons about 2 points higher; second sons raised as eldest scored like firstborns"),
            Study("Rohrer, Egloff and Schmukle (within families)", 2015, n="more than 20,000 adults",
                  found="a small decline with birth order"),
            Study("Damian and Roberts", 2015, n="377,000 students", effect=0.04, unit="r",
                  found="about one IQ point"),),
    note="Small, one to three points, and about the rank in which a child is raised; it predicts little about any "
         "one family.",
    sources=("L. Belmont and F. A. Marolla, Birth order, family size, and intelligence, Science 182 (1973) 1096-1101",
             "P. Kristensen and T. Bjerkedal, Explaining the relation between birth order and intelligence, Science "
             "316 (2007) 1717",
             "J. M. Rohrer, B. Egloff and S. C. Schmukle, Examining the effects of birth order on personality, PNAS "
             "112 (2015) 14224-14229"),
    checked="2026-11-15",
))

add(Finding(
    key="chronotype_age", part=31, title=r"The latest sleepers are about twenty",
    claim="Chronotype grows later through adolescence, is latest at about age twenty, and grows earlier after.",
    original=Study("Roenneberg and colleagues", 2004, n="about 25,000 people aged 8 to 90",
                   design="the Munich Chronotype Questionnaire", found="latest at about 19.5 in women and 21 in men"),
    status="replicated",
    record=(Study("Fischer, Lombardi, Marucci-Wellman and Roenneberg", 2017, n="twelve years of the American Time "
                  "Use Survey", found="latest at about 19; men later than women before 40"),),
    note="The curve replicates; whether its turning point marks the biological end of adolescence is a proposal.",
    sources=("T. Roenneberg et al., A marker for the end of adolescence, Current Biology 14 (2004) R1038-R1039",
             "D. Fischer, D. A. Lombardi, H. Marucci-Wellman and T. Roenneberg, Chronotypes in the US: influence of "
             "age and sex, PLoS ONE 12 (2017) e0178782"),
    checked="2026-11-15",
    data=("ROENNEBERG_2004",),
))

add(Finding(
    key="moral_stage_sex", part=31, title=r"Kohlberg's scale and women",
    claim="Kohlberg's stages score women's moral reasoning lower than men's.",
    original=Study("Gilligan", 1982, n="interview studies, including women deciding about abortion",
                   design="a critique of the scale", found="an ethic of care, heard more in women, scored as lower"),
    status="failed",
    record=(Study("Walker (review)", 1984, n="108 studies", found="sex differences in stage were rare"),
            Study("Jaffee and Hyde (meta-analysis)", 2000, n="published studies of moral orientation", effect=0.28, unit="d",
                  found="care reasoning slightly more in women (d = 0.28), justice in men (d = 0.19)"),),
    note="Stage scores show few sex differences; the orientations differ slightly, and more by dilemma than by sex.",
    sources=("C. Gilligan, In a Different Voice (Harvard University Press, 1982)",
             "L. J. Walker, Sex differences in the development of moral reasoning: a critical review, Child "
             "Development 55 (1984) 677-691",
             "S. Jaffee and J. S. Hyde, Gender differences in moral orientation: a meta-analysis, Psychological "
             "Bulletin 126 (2000) 703-726"),
    checked="2026-11-15",
))

add(Finding(
    key="positivity_effect", part=31, title=r"The positivity effect in later life",
    claim="Compared with younger adults, older adults attend to and remember positive material more than negative.",
    original=Study("Charles, Mather and Carstensen", 2003, n="144 people aged 18 to 80",
                   design="recall and recognition of positive, negative and neutral pictures",
                   found="the oldest recalled fewer negative pictures; the bias grew with age"),
    status="replicated",
    record=(Study("Reed, Chan and Mikels (meta-analysis)", 2014, n="100 studies, 7,129 people",
                  found="reliable; larger when processing is unconstrained and the age gap wider"),),
    note="Reliable on average and moderated by method; whether it reflects goals, as the theory says, or reduced "
         "processing of negative material is argued.",
    sources=("S. T. Charles, M. Mather and L. L. Carstensen, Aging and emotional memory: the forgettable nature of "
             "negative images for older adults, Journal of Experimental Psychology: General 132 (2003) 310-324",
             "A. E. Reed, L. Chan and J. A. Mikels, Meta-analysis of the age-related positivity effect: age "
             "differences in preferences for positive over negative information, Psychology and Aging 29 (2014) 1-15"),
    checked="2026-11-15",
))

add(Finding(
    key="positive_manifold", part=32, title=r"The positive manifold",
    claim="Scores on different kinds of mental test correlate positively with one another.",
    original=Study("Spearman", 1904, n="boys at a preparatory school", design="examination marks, pitch "
                   "discrimination and musical talent", found="every correlation positive, in a hierarchy"),
    status="replicated",
    record=(Study("Holzinger and Swineford (recomputed here)", 1939, n="301 children, nine tests",
                  found="35 of 36 correlations positive, mean 0.26; one factor too few, three adequate"),
            Study("Carroll (reanalysis)", 1993, n="more than 460 data sets",
                  found="a general factor at the top of a hierarchy of broad and narrow abilities"),
            Study("Visser, Ashton and Vernon", 2006, n="tests of Gardner's eight domains",
                  found="a positive manifold and a large general factor even here"),),
    note="Among the most replicated findings in psychology; what causes it, one ability or many interacting ones, is "
         "a separate and open question.",
    sources=("C. Spearman, \"General intelligence,\" objectively determined and measured, American Journal of "
             "Psychology 15 (1904) 201-292",
             "K. J. Holzinger and F. Swineford, A study in factor analysis: the stability of a bi-factor solution, "
             "Supplementary Educational Monographs 48 (University of Chicago, 1939)",
             "J. B. Carroll, Human Cognitive Abilities: A Survey of Factor-Analytic Studies (Cambridge University "
             "Press, 1993)",
             "B. A. Visser, M. C. Ashton and P. A. Vernon, Beyond g: putting multiple intelligences theory to the "
             "test, Intelligence 34 (2006) 487-502"),
    checked="2026-11-15",
    data=("SPEARMAN_1904", "HOLZINGER_1939"),
))

add(Finding(
    key="gma_job_validity", part=32, title=r"Intelligence and job performance",
    claim="General mental ability predicts job performance with a validity of about .5, better than any other "
          "single selection method.",
    original=Study("Schmidt and Hunter (meta-analysis)", 1998, n="85 years of studies of 19 selection methods",
                   found="general mental ability the strongest single predictor"),
    status="replicated, smaller",
    record=(Study("Sackett, Zhang, Berry and Lievens (reanalysis)", 2022, n="the same literatures, corrections "
                  "for range restriction revisited", effect=0.31, unit="r",
                  found="about .31; no longer the clear best single predictor"),),
    note="A real and useful predictor; the classic figure rested on corrections for range restriction that were "
         "too large.",
    sources=("F. L. Schmidt and J. E. Hunter, The validity and utility of selection methods in personnel psychology, "
             "Psychological Bulletin 124 (1998) 262-274",
             "P. R. Sackett, C. Zhang, C. M. Berry and F. Lievens, Revisiting meta-analytic estimates of validity in "
             "personnel selection: addressing systematic overcorrection for restriction of range, Journal of Applied "
             "Psychology 107 (2022) 2040-2068"),
    checked="2026-11-15",
))

add(Finding(
    key="flynn_effect", part=32, title=r"The Flynn effect",
    claim="Average scores on intelligence tests rose by about three points a decade through the twentieth century.",
    original=Study("Flynn", 1984, n="American norming samples, 1932 to 1978",
                   found="13.8 points in 46 years"),
    status="replicated",
    record=(Study("Flynn", 1987, n="14 nations", found="5 to 25 points in a generation, largest on reasoning tests"),
            Study("Wicherts and colleagues", 2004, n="several test batteries across cohorts",
                  found="the gains are not measurement-invariant"),
            Study("Pietschnig and Voracek (meta-analysis)", 2015, n="271 samples, about 4 million people, 31 "
                  "countries", found="about 2.8 points a decade"),
            Study("Bratsberg and Rogeberg (within families)", 2018, n="736,808 Norwegian conscripts",
                  found="a reversal for men born from the mid-1970s, within families"),),
    note="The rise is real and large; what it is a rise in is unclear, since the tests are not invariant across "
         "cohorts, and in several countries it has reversed.",
    sources=("J. R. Flynn, The mean IQ of Americans: massive gains 1932 to 1978, Psychological Bulletin 95 (1984) "
             "29-51",
             "J. R. Flynn, Massive IQ gains in 14 nations, Psychological Bulletin 101 (1987) 171-191",
             "J. M. Wicherts et al., Are intelligence tests measurement invariant over time? Investigating the "
             "nature of the Flynn effect, Intelligence 32 (2004) 509-537",
             "J. Pietschnig and M. Voracek, One century of global IQ gains, Perspectives on Psychological Science 10 "
             "(2015) 282-306",
             "B. Bratsberg and O. Rogeberg, Flynn effect and its reversal are both environmentally caused, PNAS 115 "
             "(2018) 6674-6678"),
    checked="2026-11-15",
))

add(Finding(
    key="schooling_iq", part=32, title=r"Schooling raises scores",
    claim="An additional year of schooling raises scores on intelligence tests.",
    original=Study("Ceci (review)", 1991, n="many studies of schooling and test scores",
                   found="schooling raises IQ scores"),
    status="replicated",
    record=(Study("Ritchie and Tucker-Drob (meta-analysis)", 2018, n="142 effects, 42 data sets, more than 600,000 "
                  "people", found="about 1 to 5 points a year, 3.4 on average, lasting into later life"),),
    note="Robust across three quasi-experimental designs; whether schooling raises g or the skills tests sample is "
         "open.",
    sources=("S. J. Ceci, How much does schooling influence general intelligence and its cognitive components? A "
             "reassessment of the evidence, Developmental Psychology 27 (1991) 703-722",
             "S. J. Ritchie and E. M. Tucker-Drob, How much does education improve intelligence? A meta-analysis, "
             "Psychological Science 29 (2018) 1358-1369"),
    checked="2026-11-15",
))

add(Finding(
    key="heritability_age", part=32, title=r"Heritability of intelligence rises with age",
    claim="The heritability of general cognitive ability rises from childhood to young adulthood.",
    original=Study("Haworth and colleagues", 2010, n="about 11,000 twin pairs, six studies, four countries",
                   found="41% at 9, 55% at 12, 66% at 17"),
    status="replicated",
    record=(Study("Briley and Tucker-Drob (meta-analysis)", 2013, n="11,500 twin and sibling pairs, longitudinal",
                  found="heritability rises after about age 8, mostly by amplification of earlier genetic "
                        "influences"),),
    note="A robust developmental pattern; one reading is that children increasingly select environments that suit "
         "them (Part 9's gene-environment correlation).",
    sources=("C. M. A. Haworth et al., Molecular Psychiatry 15 (2010) 1112-1120",
             "D. A. Briley and E. M. Tucker-Drob, Explaining the increasing heritability of cognitive ability across "
             "development, Psychological Science 24 (2013) 1704-1713"),
    checked="2026-11-15",
    data=("HAWORTH_2010",),
))

add(Finding(
    key="ses_heritability", part=32, title=r"Poverty and the heritability of IQ",
    claim="Among children raised in poverty, the heritability of IQ is close to zero.",
    original=Study("Turkheimer, Haley, Waldron, D'Onofrio and Gottesman", 2003, n="319 twin pairs aged 7",
                   found="in poor families shared environment large and heritability near zero; the reverse in "
                         "affluent families"),
    status="contested",
    record=(Study("Tucker-Drob and Bates (meta-analysis)", 2016, n="24,926 twin and sibling pairs, six countries",
                  found="the interaction in US samples; none in Western Europe or Australia"),),
    note="A heritability that depends on the environment, as Part 9 argued it can; whether it does depends on the "
         "country.",
    sources=("E. Turkheimer et al., Socioeconomic status modifies heritability of IQ in young children, Psychological "
             "Science 14 (2003) 623-628",
             "E. M. Tucker-Drob and T. C. Bates, Large cross-national differences in gene x socioeconomic status "
             "interaction on intelligence, Psychological Science 27 (2016) 138-149"),
    checked="2026-11-15",
    data=("TURKHEIMER_2003",),
))

add(Finding(
    key="mozart_effect", part=32, title=r"The Mozart effect",
    claim="Listening to Mozart improves spatial reasoning.",
    original=Study("Rauscher, Shaw and Ky", 1993, n="college students", design="a Mozart sonata, relaxation "
                   "instructions or silence, then spatial tasks", found="better spatial reasoning for a short time"),
    status="failed",
    record=(Study("Pietschnig, Voracek and Formann (meta-analysis)", 2010, n="about 40 studies, more than 3,000 "
                  "people", effect=0.37, unit="d", lo=0.23, hi=0.52,
                  found="a small effect against no stimulus, varying by laboratory; nothing specific to Mozart"),),
    note="A small arousal or mood effect of music in general, if anything; the specific Mozart effect was not "
         "confirmed, and general intelligence was never claimed by the authors.",
    sources=("F. H. Rauscher, G. L. Shaw and K. N. Ky, Music and spatial task performance, Nature 365 (1993) 611",
             "J. Pietschnig, M. Voracek and A. K. Formann, Mozart effect-Shmozart effect: a meta-analysis, "
             "Intelligence 38 (2010) 314-323"),
    checked="2026-11-15",
))

add(Finding(
    key="multiple_intelligences", part=32, title=r"Multiple intelligences",
    claim="Human abilities form several independent intelligences rather than one general factor.",
    original=Study("Gardner", 1983, n="a synthesis of neuropsychology, development and special talents",
                   design="Frames of Mind", found="seven intelligences, later eight"),
    status="failed",
    record=(Study("Visser, Ashton and Vernon", 2006, n="tests of the eight domains",
                  found="a positive manifold and a large general factor; cognitive domains loaded most"),),
    note="A useful list of talents; the claim of independence is contradicted by the domains' own correlations.",
    sources=("H. Gardner, Frames of Mind: The Theory of Multiple Intelligences (Basic Books, 1983)",
             "B. A. Visser, M. C. Ashton and P. A. Vernon, Beyond g: putting multiple intelligences theory to the "
             "test, Intelligence 34 (2006) 487-502"),
    checked="2026-11-15",
))

add(Finding(
    key="big_five_structure", part=33, title=r"Five broad factors of personality",
    claim="Ratings and self-reports of personality are summarized by five broad recurring factors.",
    original=Study("Tupes and Christal", 1961, n="trait ratings from eight samples (US Air Force report)",
                   found="the same five factors in each"),
    status="replicated",
    record=(Study("Norman", 1963, n="peer ratings", found="the five again"),
            Study("McCrae and Costa", 1997, n="the NEO-PI-R in six translations",
                  found="similar five-factor structures in German, Portuguese, Hebrew, Chinese, Korean and Japanese"),
            Study("SAPA sample (recomputed here)", 2010, n="2,800 people, 25 IPIP items",
                  found="parallel analysis keeps five; every item loads most on its own factor"),),
    note="Robust in literate, mostly Western and Asian samples; a lexical sixth factor (honesty-humility) recurs too.",
    sources=("E. C. Tupes and R. E. Christal, Recurrent personality factors based on trait ratings, USAF ASD Technical "
             "Report 61-97 (1961)",
             "W. T. Norman, Toward an adequate taxonomy of personality attributes, Journal of Abnormal and Social "
             "Psychology 66 (1963)",
             "R. R. McCrae and P. T. Costa, Personality trait structure as a human universal, American Psychologist 52 "
             "(1997) 509-516",
             "M. C. Ashton et al., A six-factor structure of personality-descriptive adjectives, Journal of "
             "Personality and Social Psychology 86 (2004)"),
    checked="2026-11-15",
    data=("SAPA_BFI_2010",),
))

add(Finding(
    key="big_five_universal", part=33, title=r"The five factors as a human universal",
    claim="The same five factors describe personality in every human population.",
    original=Study("McCrae and Costa", 1997, n="six translations of one inventory",
                   found="five language families, one structure"),
    status="contested",
    record=(Study("Gurven and colleagues", 2013, n="632 Tsimane forager-horticulturalists in Bolivia",
                  found="no robust five-factor structure; two broad factors instead"),
            Study("Laajaj and colleagues", 2019, n="94,751 respondents, 23 low- and middle-income countries",
                  found="face-to-face Big Five surveys of low validity; internet samples from the same countries "
                        "looked like Western ones"),),
    note="Whether the five are universal or partly a product of literacy, schooling and questionnaire habits is "
         "unresolved.",
    sources=("R. R. McCrae and P. T. Costa, American Psychologist 52 (1997) 509-516",
             "M. Gurven et al., How universal is the Big Five? Journal of Personality and Social Psychology 104 "
             "(2013) 354-370",
             "R. Laajaj et al., Challenges to capture the big five personality traits in non-WEIRD populations, "
             "Science Advances 5 (2019)"),
    checked="2026-11-15",
))

add(Finding(
    key="trait_outcomes", part=33, title=r"Traits predict life outcomes",
    claim="Personality traits predict consequential outcomes such as health, relationships and work.",
    original=Study("Roberts, Kuncel, Shiner, Caspi and Goldberg (review)", 2007, n="prospective studies",
                   found="mortality, divorce and attainment, about as well as socioeconomic status and cognitive "
                         "ability"),
    status="replicated, smaller",
    record=(Study("Soto (LOOPR)", 2019, n="78 trait-outcome links, median N 1,504, preregistered",
                  found="87% replicated; effects typically 77% as large"),),
    note="A strong record by Part 4's standards; the replications were cross-sectional self-report panels.",
    sources=("B. W. Roberts et al., The power of personality, Perspectives on Psychological Science 2 (2007) 313-345",
             "C. J. Soto, How replicable are links between personality traits and consequential life outcomes? "
             "Psychological Science 30 (2019)"),
    checked="2026-11-15",
))

add(Finding(
    key="person_situation", part=33, title=r"Traits barely predict behaviour",
    claim="Traits predict behaviour only up to about .30, so behaviour is mostly determined by situations.",
    original=Study("Mischel", 1968, n="a review", design="Personality and Assessment",
                   found="trait-behaviour and cross-situational correlations rarely above about .30"),
    status="story and record",
    record=(Study("Epstein", 1979, n="daily records over weeks", found="aggregated behaviour highly stable"),
            Study("Funder and Ozer", 1983, n="classic situational experiments",
                  found="situational effects about .36 to .42 as correlations"),
            Study("Fleeson", 2001, n="experience sampling over weeks",
                  found="large within-person variation, highly stable averages"),),
    note="The .30 was real for single acts; the story that personality does not exist was not: aggregated, traits "
         "predict well, and situations are no larger.",
    sources=("W. Mischel, Personality and Assessment (Wiley, 1968)",
             "S. Epstein, The stability of behavior, Journal of Personality and Social Psychology 37 (1979)",
             "D. C. Funder and D. J. Ozer, Behavior as a function of the situation, Journal of Personality and Social "
             "Psychology 44 (1983) 107-112",
             "W. Fleeson, Toward a structure- and process-integrated view of personality, Journal of Personality and "
             "Social Psychology 80 (2001) 1011-1027"),
    checked="2026-11-15",
))

add(Finding(
    key="mbti_types", part=33, title=r"Personality types",
    claim="People fall into distinct personality types that a questionnaire identifies reliably.",
    original=Study("Myers and Briggs", 1962, n="the indicator's first manual", found="sixteen types"),
    status="failed",
    record=(Study("Pittenger (review)", 1993, n="studies of the indicator",
                  found="weak evidence that the types are distinct; type often changes on retest"),
            Study("SAPA sample (recomputed here)", 2010, n="2,800 people",
                  found="extraversion has one hump, not two"),),
    note="Trait scores are continuous; cutting them at the middle makes types that are unstable near the cut and "
         "discard information.",
    sources=("I. B. Myers, The Myers-Briggs Type Indicator manual (Educational Testing Service, 1962)",
             "D. J. Pittenger, The utility of the Myers-Briggs Type Indicator, Review of Educational Research 63 "
             "(1993) 467-488"),
    checked="2026-11-15",
    data=("SAPA_BFI_2010",),
))

add(Finding(
    key="likes_prediction", part=33, title=r"Personality from digital footprints",
    claim="Personality traits can be estimated from digital records such as likes.",
    original=Study("Kosinski, Stillwell and Graepel", 2013, n="58,466 US volunteers",
                   found="openness about as accurate as the test's retest; other traits less"),
    status="replicated",
    record=(Study("Youyou, Kosinski and Stillwell", 2015, n="Facebook volunteers",
                  found="computer .56 against friends .49; beat a spouse with 300 likes"),
            Study("Azucar, Marengo and Settanni (meta-analysis)", 2018, n="social-media studies",
                  found="about .3 to .4"),
            Study("Peters and Matz", 2024, n="1,000 users' status updates",
                  found="a language model without task-specific training: about .29"),),
    note="Moderate accuracy, repeatedly; the privacy questions are larger than the effect sizes.",
    sources=("M. Kosinski, D. Stillwell and T. Graepel, PNAS 110 (2013) 5802-5805",
             "W. Youyou, M. Kosinski and D. Stillwell, PNAS 112 (2015) 1036-1040",
             "D. Azucar, D. Marengo and M. Settanni, Personality and Individual Differences 124 (2018) 150-159",
             "H. Peters and S. C. Matz, Large language models can infer psychological dispositions of social media "
             "users, PNAS Nexus (2024)"),
    checked="2026-11-15",
))

add(Finding(
    key="psychographic_targeting", part=33, title=r"Persuasion matched to personality",
    claim="Ads matched to a person's personality are substantially more persuasive.",
    original=Study("Matz, Kosinski, Nave and Stillwell", 2017, n="field experiments reaching over 3.5 million people",
                   found="up to 40% more clicks and 50% more purchases"),
    status="contested",
    record=(Study("Eckles, Gordon and Johnson (letter)", 2018, n="a critique of the design",
                  found="no randomization of people to ads; ad delivery could produce the differences"),),
    note="Unresolved without randomized tests; the Cambridge Analytica story was never shown to rest on measured "
         "effects.",
    sources=("S. C. Matz, M. Kosinski, G. Nave and D. J. Stillwell, PNAS 114 (2017) 12714-12719",
             "D. Eckles, B. R. Gordon and G. A. Johnson, Field studies of psychologically targeted ads face threats "
             "to internal validity, PNAS 115 (2018)"),
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
      "qualitatively, as background to theories of concepts")
shown(22, r"Xu \& Tenenbaum (2007); \ Tenenbaum \& Griffiths (2001)", "a model and a word-learning study that tests "
      "it, described qualitatively; Bayesian word learning returns with language")
shown(22, r"Harris (1954); \ Firth (1957); \ the \emph{tezg\"{u}ino} example: \ Nida (1975), \ Lin (1998)", "the "
      "history of an idea")
shown(22, r"Landauer \& Dumais (1997); \ Caliskan et al. (2017); \ Harnad (1990)", "a model's benchmark, a "
      "measurement of text and a philosophical argument; not psychological findings to replicate")
shown(22, "LANDAUER_DUMAIS_1997", "a model's score on a test, not a finding about people")
shown(22, r"Fried \& Nesse (2015); \ Kotov et al. (2017); \ APA, \ DSM-5 (2013)", "a count of symptom profiles, a "
      "classification proposal and a manual's criteria; diagnosis as a category is entered in Part 39 (its rows "
      "dimensional structure and p factor)")
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
shown(23, r"Fedorenko, \ Behr \& Kanwisher (2011), \ \emph{PNAS}", "the language network, described; Part 49 "
      "teaches the encoding models used to map it, as methods")
shown(23, r"Kutas \& Hillyard (1980); \ Osterhout \& Holcomb (1992)", "ERP components described with schematics; "
      "the N400's row is Part 8's, and Part 49 teaches how ERP measures are analysed")
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
shown(26, r"Frey et al.\ (2017)", "a frontier study of how risk preference is measured, described; Part 33 "
      "covers the broad traits, not risk preference")
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

shown(28, r"Bernard (1865); \ Cannon (1932); \ Hull (1943)", "the history of homeostasis and drive theory")
shown(28, r"Sheffield \& Roby (1950); \ Olds \& Milner (1954)", "saccharin as a reward, told as history; "
      "brain-stimulation reward has its row")
shown(28, r"Hetherington \& Ranson (1940); \ Zhang et al.\ (1994); \ Kojima et al.\ (1999)", "the physiology of "
      "hunger: lesions, a gene and a hormone, described")
shown(28, r"Leibel, \ Rosenbaum \& Hirsch (1995); \ Hall et al.\ (2011); \ Fothergill et al.\ (2016)", "physiology "
      "of weight loss and a model of energy balance, described qualitatively; the loop is Psyche's")
shown(28, r"Harlow, \ Harlow \& Meyer (1950); \ Butler (1953)", "early animal studies of curiosity, told as history")
shown(28, r"Yerkes \& Dodson (1908); \ Teigen (1994)", "a 1908 experiment and the history of the law named after "
      "it: a history, not a finding tested here")
shown(28, r"Berlyne (1960); \ Loewenstein (1994); \ Kang et al.\ (2009)", "theories of curiosity and one study "
      "illustrating them")
shown(28, r"Berridge \& Robinson (1998); \ Pe\~cina et al.\ (2003)", "the wanting and liking dissociation; described "
      "again with addiction in Part 41, without a row of its own")
shown(28, r"Pe\~cina \& Berridge (2005); \ Berridge \& Kringelbach (2015)", "hedonic hotspots and a review, "
      "described; incentive salience returns in Part 41's chapter on addiction, without a row of its own")
shown(28, r"Robinson \& Berridge (2013)", "one experiment, modelled by Psyche; incentive salience returns in "
      "Part 41's chapter on addiction, without a row of its own")
shown(28, r"Kirby, \ Petry \& Bickel (1999); \ Myerson, \ Green \& Warusawitharana (2001)", "discounting's clinical "
      "correlates are described with addiction in Part 41, without a row; the area under the curve is a method")
shown(28, r"Locke \& Latham (2002); \ Ord\'o\~nez et al.\ (2009)", "goal-setting has its row; the review of its "
      "costs is cited in that row")
shown(28, r"Duckworth et al.\ (2007); \ Cred\'e, \ Tynan \& Harms (2017)", "grit has its row; this tag names it "
      "with accents the gate does not read")
shown(28, r"Dweck (2006); \ Sisk et al.\ (2018); \ Yeager et al.\ (2019)", "growth mindset, summarized from two "
      "meta-analyses and a national trial; entered with education", row_in=54)
shown(28, r"Kool et al.\ (2010); \ Westbrook, \ Kester \& Braver (2013)", "effort avoidance and its price, "
      "described as the starting point of a model")
shown(28, r"Kurzban et al.\ (2013); \ Inzlicht, \ Shenhav \& Olivola (2018)", "theories of effort, described")
shown(28, r"Gneezy \& Rustichini (2000)", "a field study told as an application of chapter five's finding")
shown(28, r"Hall et al.\ (2011)", "a model of energy balance used in practice, described")
shown(28, r"Lally, \ van Jaarsveld, \ Potts \& Wardle (2010)", "a study of habit formation, described as an "
      "application")
shown(28, r"Kurzban et al.\ (2013); \ Agrawal et al.\ (2022)", "theories at the frontier, described")
shown(28, r"Schmidhuber (1991); \ Pathak et al.\ (2017)", "machine-learning methods, described; machines are Part "
      "60's", row_in=60)

shown(29, r"James (1884)", "the James-Lange theory, told as history; its tests are Cannon's objections and the "
      "two-factor row")
shown(29, r"Cannon (1927); \ Bard (1928)", "Cannon's objections and the Cannon-Bard theory, told as history")
shown(29, r"Cannon (1927); \ Mara\~n\'on (1924)", "adrenaline injections that produced 'as if' emotions, told as "
      "history of the two-factor idea, whose row is Schachter and Singer")
shown(29, r"Craig (2009); \ Damasio (1994)", "theories of interoception and the body in feeling, described")
shown(29, r"Darwin (1872); \ Ekman (1992)", "the history and theory of basic emotions; universal recognition has "
      "its row")
shown(29, "FACES_1962", "the 1962 face-similarity data, rescaled on screen as a method demonstration; the map is a "
      "description of these judgments, not a finding about emotion")
shown(29, r"Russell (2003); \ Barrett (2017)", "theories of core affect and constructed emotion, described")
shown(29, r"Siegel et al.\ (2018); \ Lindquist et al.\ (2012)", "two meta-analyses describing variability within "
      "emotion categories, shown as the evidence for construction; not entered as single findings")
shown(29, r"Lazarus (1966); \ Smith \& Ellsworth (1985)", "appraisal theory, described; the model computed is "
      "Psyche's")
shown(29, r"LeDoux (1996)", "the two routes to the amygdala in rat fear conditioning, described as anatomy")
shown(29, r"Feinstein et al.\ (2011); \ Feinstein et al.\ (2013)", "a single patient, described as a case study")
shown(29, r"LeDoux (2015)", "a theoretical argument about circuits and feelings")
shown(29, r"Selye (1956); \ Lazarus \& Folkman (1984)", "theories of stress and coping, described")
shown(29, r"Gross (1998)", "the process model of regulation and one experiment, described; regulation's clinical "
      "use is tested in Part 42")
shown(29, r"Gross (1998); \ Gross \& John (2003)", "one experiment and a correlational study of habitual "
      "regulation, described")
shown(29, r"Gilbert et al.\ (1998); \ Wilson \& Gilbert (2005)", "the impact bias, described with one of its "
      "studies and a review")
shown(29, r"Brickman, \ Coates \& Janoff-Bulman (1978); \ Lucas (2007)", "a small 1978 study, shown with its "
      "limits stated, and a review of panel studies that qualifies it")
shown(29, r"Seth (2013); \ Barrett \& Simmons (2015); \ Zamariola et al.\ (2018)", "frontier theories of "
      "interoceptive inference and a dispute about the heartbeat counting measure")
shown(29, r"Panksepp \& Burgdorf (2003); \ Anderson \& Adolphs (2014); \ Gibson et al.\ (2015)", "frontier work "
      "on emotional states in animals, described")
shown(29, r"Picard (1997)", "a book that founded a field, described")

shown(30, r"Piaget (1936, \ 1937)", "Piaget's theory and observations, told as history; the A-not-B error has its row")
shown(30, r"Piaget \& Szeminska (1941)", "the conservation task, described; it replicates easily and its meaning is "
      "discussed qualitatively")
shown(30, r"Fantz (1961)", "the looking-preference method, told as history")
shown(30, r"Spelke \& Kinzler (2007)", "a theory of core knowledge, described")
shown(30, r"Xu \& Garcia (2008)", "a single study described as the case for infant statistics; not entered as a finding")
shown(30, r"Spelke \& Kinzler (2007); \ Xu \& Kushnir (2012)", "three theoretical positions, described")
shown(30, r"Diamond (1985); \ Thelen et al.\ (2001)", "the delay finding, entered in the A-not-B row, and a model, "
      "simulated by Psyche")
shown(30, r"Harlow (1958)", "animal experiments told as history, with their ethics")
shown(30, r"Ainsworth et al.\ (1978); \ van IJzendoorn \& Kroonenberg (1988)", "a method of assessment and a "
      "descriptive cross-cultural pooling, not a test of a claim")
shown(30, r"Fearon et al.\ (2010)", "a meta-analysis quoted for the size of an association, described as modest")
shown(30, r"Thomas \& Chess (1977)", "a descriptive longitudinal study of temperament")
shown(30, r"Vygotsky (1934); \ Csibra \& Gergely (2009)", "theories of learning from others, described")
shown(30, r"Horner \& Whiten (2005); \ Lyons, \ Young \& Keil (2007)", "overimitation, described from its first "
      "studies; its row (overimitation across cultures) is entered in Part 38")
shown(30, r"Schweinhart et al.\ (2005); \ Puma et al.\ (2012); \ Durkin et al.\ (2022)", "evaluations of programmes, "
      "described as applications; early intervention is taken up with education in Part 54", row_in=54)
shown(30, r"DeLoache et al.\ (2010)", "a single trial of a product, described as an application")
shown(30, r"Vong et al.\ (2024)", "a modelling result at the frontier, described")
shown(30, r"Piloto et al.\ (2022)", "a machine-learning model at the frontier, described; machines are Part 60's",
      row_in=60)

shown(31, r"Wiesel \& Hubel (1963); \ Hubel \& Wiesel (1970)", "the sensitive period in vision, told as history "
      "(Part 7); textbook physiology")
shown(31, r"Schaie (2005); \ Salthouse (2009)", "a methodological debate between two research programmes, "
      "described and simulated; no single finding to enter")
shown(31, r"Gardner \& Steinberg (2005)", "a single laboratory study of peer influence, described with a failed "
      "attempt to repeat it; its row waits for a registered replication")
shown(31, r"Steinberg et al.\ (2018)", "a descriptive cross-national survey of two age curves")
shown(31, r"Harris (1998); \ Humphreys et al.\ (2022)", "a book's argument, described; the trial has its row")
shown(31, r"Colby et al.\ (1983)", "the longitudinal study of Kohlberg's stages, described")
shown(31, r"Salthouse (1996)", "a theory of cognitive ageing, described with its limits")
shown(31, r"Livingston et al.\ (2024)", "a commission's estimate from attributable fractions, explained with its "
      "causal assumption")
shown(31, r"Ngandu et al.\ (2015)", "a single randomized trial, described with its small effect")
shown(31, r"Pietschnig \& Voracek (2015)", "the Flynn effect, described as a cohort effect; its row is entered with "
      "intelligence in Part 32")
shown(31, r"Bratsberg \& Rogeberg (2018)", "the reversal of the Flynn effect, described; entered with intelligence "
      "in Part 32")
shown(31, r"Layton et al.\ (2018)", "a single large natural experiment, described as an application; relative age and "
      "diagnosis are taken up again in Part 41's chapter on ADHD, without a row of its own")
shown(31, r"Casey et al.\ (2018)", "the design of a cohort study at the frontier, described")

shown(32, r"Spearman (1904); \ Binet \& Simon (1905)", "two founding studies told as history; the positive manifold has "
      "its row")
shown(32, r"\emph{Buck v. Bell} (1927)", "a court decision, told as history")
shown(32, r"Thurstone (1938)", "a factor-analytic study told as history; the hierarchy is in the positive-manifold row")
shown(32, r"Deary et al.\ (2007); \ Strenze (2007); \ Sackett et al.\ (2022)", "effect sizes quoted from a cohort "
      "study and meta-analyses; the job-performance figure has its row")
shown(32, r"Calvin et al.\ (2011)", "a meta-analysis quoted for the size of an association, with its confounding")
shown(32, r"Carpenter, \ Just \& Shell (1990)", "a process model of one test, described and rebuilt by Psyche")
shown(32, r"Flore \& Wicherts (2015); \ Flore et al.\ (2018)", "stereotype threat's record, previewed; its row "
      "(stereotype_threat) is entered in Part 36")
shown(32, r"Snyderman \& Herrnstein (1983)", "a historical dispute, described")
shown(32, r"Kamin (1974); \ Hearnshaw (1979)", "a case of fraud, told as history")
shown(32, r"Gould (1981); \ Lewis et al.\ (2011)", "a historical critique and its re-examination, described")
shown(32, r"Binet \& Simon (1905); \ Stern (1912)", "the history of the IQ scale, described")
shown(32, r"Wechsler (1939)", "the deviation IQ's history, described")
shown(32, r"Kan et al.\ (2019); \ McFarland (2020)", "a methodological dispute at the frontier, described as open")
shown(32, r"Lee et al.\ (2018); \ Howe et al.\ (2022)", "genome-wide estimates quoted at the frontier; heritability is "
      "Part 9's")
shown(32, r"Chollet (2019)", "a proposal for measuring machine intelligence, described")

shown(33, r"Allport \& Odbert (1936)", "a lexical study told as history; the five factors have their row")
shown(33, r"Mischel (1968)", "the person-situation debate; its row is person_situation")
shown(33, r"Allport \& Odbert (1936); \ Tupes \& Christal (1961)", "history of the five; they have their row")
shown(33, r"Goldberg (1981); \ Costa \& McCrae (1985, \ 1992)", "the naming of the five and the NEO, described")
shown(33, r"Ashton et al.\ (2004)", "the six-factor lexical result, described in the five-factor row's note")
shown(33, r"Jung (1921); \ Myers \& Briggs (1962)", "history of the type indicator; types have their row")
shown(33, r"Hartshorne \& May (1928)", "a historical study of honesty, described")
shown(33, r"Funder \& Ozer (1983)", "part of the person-situation row's record")
shown(33, r"Roberts \& DelVecchio (2000)", "a meta-analysis quoted for rank-order stability")
shown(33, r"Roberts et al.\ (2006); \ data: \ SAPA (2010)", "a meta-analysis of mean-level change, with a "
      "cross-section recomputed")
shown(33, r"Hudson \& Fraley (2015); \ Stieger et al.\ (2021)", "studies of volitional change, described; a "
      "frontier")
shown(33, r"Vukasovi\'c \& Bratko (2015)", "a pooled heritability estimate, described; heritability is Part 9's")
shown(33, r"Eysenck; \ Gray (1970)", "biological theories, described")
shown(33, r"Barrick \& Mount (1991)", "a meta-analysis of personality and job performance, described; work is Part 53's")
shown(33, r"Cramer et al.\ (2012)", "a theoretical proposal (traits as networks), described; Part 44 tests it")
shown(33, r"Roberts et al.\ (2007)", "the trait-outcome row's original")
shown(33, r"Soto (2019)", "the trait-outcome row's record")
shown(33, r"Westen (1998); \ Kihlstrom", "an evaluation of psychoanalysis and its critique, described")
shown(33, r"Rorschach (1921); \ Lilienfeld, \ Wood \& Garb (2000)", "projective tests and a review of them, "
      "described")
shown(33, r"Hyde (2005); \ Costa et al.\ (2001); \ Schmitt et al.\ (2008)", "reviews and cross-cultural surveys "
      "of sex differences, described")
shown(33, r"Del Giudice et al.\ (2012); \ Hyde", "a disputed multivariate estimate, described with its critique")
shown(33, r"Kosinski et al.\ (2013); \ simulated: \ \texttt{personality.likes\_accuracy}", "the likes row's "
      "original, with a simulation")
shown(33, r"Youyou et al.\ (2015); \ Azucar et al.\ (2018)", "the likes row's record")
shown(33, r"Matz et al.\ (2017); \ Eckles et al.\ (2018)", "the targeting row")


# ---------------------------------------------------------------- Part 34: social influence

add(Finding(
    key="asch_conformity", part=34, title=r"Conformity to a unanimous majority",
    claim="People often give an answer they can see is wrong when a unanimous group gives it first.",
    original=Study("Asch", 1956, n="123 men, three universities", design="12 critical line-judgment trials",
                   found="36.8% of critical answers went with the wrong majority; a quarter never conformed"),
    status="replicated, smaller",
    record=(Study("Bond and Smith (meta-analysis)", 1996, n="133 studies, 17 countries",
                  found="higher in collectivist cultures; declining in the US since the 1950s"),
            Study("Franzen and Mader", 2023, n="210 students, five confederates",
                  found="33% of critical answers wrong; 25% when correct answers were paid"),),
    note="Robust and durable, though smaller in later and individualist samples; one dissenting ally removes most of "
         "it.",
    sources=("S. E. Asch, Opinions and social pressure, Scientific American 193(5) (1955) 31-35",
             "S. E. Asch, Studies of independence and conformity: I. A minority of one against a unanimous majority, "
             "Psychological Monographs 70(9) (1956)",
             "R. Bond and P. B. Smith, Culture and conformity: a meta-analysis of studies using Asch's line judgment "
             "task, Psychological Bulletin (1996)",
             "A. Franzen and S. Mader, The power of social influence: a replication and extension of the Asch "
             "experiment, PLOS ONE 18 (2023) e0294325"),
    checked="2026-11-16",
))

add(Finding(
    key="milgram_obedience", part=34, title=r"Obedience to a destructive authority",
    claim="Most ordinary people will give apparently dangerous shocks to another person when an experimenter tells "
          "them to.",
    original=Study("Milgram", 1963, n="40 men, New Haven", design="the remote-feedback condition",
                   found="26 of 40 (65%) went to the 450-volt switch"),
    status="not directly tested",
    record=(Study("Burger", 2009, n="70 adults", design="stopped at 150 volts",
                  found="70% went past 150 volts, against 82.5% in Milgram's matching condition"),
            Study("Haslam, Loughnan and Perry (synthesis)", 2014, n="21 conditions, 740 people",
                  found="43.6% obeyed to the end overall, from 0% to 92.5% by condition"),
            Study("Perry et al. (archive reanalysis)", 2020, n="656 post-experiment questionnaires",
                  found="only about half fully believed the shocks were real"),),
    note="Never run in full again; milder versions replicate the willingness to go on, while the reading of it "
         "(blind obedience, or engaged followership amid doubt) is contested.",
    sources=("S. Milgram, Behavioral study of obedience, Journal of Abnormal and Social Psychology 67 (1963) 371-378",
             "S. Milgram, Obedience to Authority (1974)",
             "J. M. Burger, Replicating Milgram: would people still obey today?, American Psychologist 64 (2009)",
             "N. Haslam, S. Loughnan and G. Perry, Meta-Milgram: an empirical synthesis of the obedience experiments, "
             "PLOS ONE 9 (2014) e93927",
             "G. Perry, Behind the Shock Machine (2012)",
             "G. Perry, A. Brannigan, R. A. Wanner and H. Stam, Credibility and incredulity in Milgram's obedience "
             "experiments: a reanalysis of an unpublished test, Social Psychology Quarterly 83 (2020) 88-106",
             "S. A. Haslam, S. D. Reicher and K. Millard, Shock treatment: using immersive digital realism to restage and "
             "re-examine Milgram's obedience to authority research, PLOS ONE (2015)"),
    checked="2026-11-16",
))

add(Finding(
    key="stanford_prison", part=34, title=r"The Stanford prison experiment",
    claim="Randomly assigned to be guards, ordinary students spontaneously became abusive: a role takes over the "
          "person.",
    original=Study("Zimbardo and colleagues", 1971, n="24 male students", design="a mock prison, stopped on day six",
                   found="abusive guards and distressed prisoners"),
    status="story and record",
    record=(Study("Reicher and Haslam (BBC prison study)", 2006, n="men randomly assigned, eight days",
                  found="guards did not identify with the role; the prisoners became a group and overcame them"),
            Study("Le Texier (archives and interviews)", 2019, n="the archives and 15 participants",
                  found="guards were given precise instructions and were not told they were subjects"),),
    note="Not an experiment on what a role does by itself: the guards were coached toward the result.",
    sources=("C. Haney, C. Banks and P. Zimbardo, Interpersonal dynamics in a simulated prison, International Journal "
             "of Criminology and Penology 1 (1973)",
             "S. Reicher and S. A. Haslam, Rethinking the psychology of tyranny: the BBC prison study, British Journal "
             "of Social Psychology 45 (2006) 1-40",
             "T. Le Texier, Debunking the Stanford Prison Experiment, American Psychologist 74 (2019) 823-839"),
    checked="2026-11-16",
))

add(Finding(
    key="genovese_witnesses", part=34, title=r"The 38 witnesses",
    claim="Thirty-eight neighbours watched Kitty Genovese's murder and none called the police.",
    original=Study("Gansberg (The New York Times)", 1964, n="one murder, Queens", design="a news report",
                   found="38 witnesses who did nothing"),
    status="story and record",
    record=(Study("Manning, Levine and Collins", 2007, n="the trial and police record",
                  found="about a dozen heard or saw parts of the attack; at least one called the police"),),
    note="The bystander effect it inspired is real (next row); the story that launched it was not.",
    sources=("M. Gansberg, 37 who saw murder didn't call the police, The New York Times (27 March 1964)",
             "R. Manning, M. Levine and A. Collins, The Kitty Genovese murder and the social psychology of helping: "
             "the parable of the 38 witnesses, American Psychologist 62 (2007) 555-562"),
    checked="2026-11-16",
))

add(Finding(
    key="bystander_effect", part=34, title=r"The bystander effect",
    claim="The more bystanders there are, the less likely each one is to help.",
    original=Study("Darley and Latané", 1968, n="students over an intercom", design="an apparent seizure",
                   found="85% helped alone, 31% with four others"),
    status="replicated",
    record=(Study("Fischer et al. (meta-analysis)", 2011, n="105 effects, more than 7,700 people",
                  found="g = -0.35; weaker in dangerous emergencies"),
            Study("Philpot et al.", 2020, n="219 filmed public conflicts, three countries",
                  found="someone intervened in about nine in ten; more bystanders, more help"),),
    note="True of each individual in the laboratory; in real public conflicts, a larger crowd still makes help from "
         "someone more likely.",
    sources=("J. M. Darley and B. Latané, Bystander intervention in emergencies: diffusion of responsibility, Journal "
             "of Personality and Social Psychology 8 (1968) 377-383",
             "B. Latané and J. M. Darley, Group inhibition of bystander intervention in emergencies, Journal of "
             "Personality and Social Psychology 10 (1968) 215-221",
             "P. Fischer et al., The bystander-effect, Psychological Bulletin 137 (2011) 517-537",
             "R. Philpot, L. S. Liebst, M. Levine, W. Bernasco and M. R. Lindegaard, Would I be helped?, American "
             "Psychologist 75 (2020) 66-75"),
    checked="2026-11-16",
))

add(Finding(
    key="social_facilitation", part=34, title=r"An audience helps easy tasks and hurts hard ones",
    claim="The presence of others improves performance on simple tasks and impairs it on complex ones.",
    original=Study("Zajonc, Heingartner and Herman", 1969, n="cockroaches", design="runway and maze, with or without "
                   "an audience", found="faster on the runway, slower in the maze, with an audience"),
    status="contested",
    record=(Study("Halfmann, Bredehöft and Häusser (preregistered)", 2020, n="cockroaches, direct replication",
                  found="an audience slowed them on both tasks; no interaction"),),
    note="Social inhibition replicates; the facilitation half of the famous interaction did not.",
    sources=("R. B. Zajonc, Social facilitation, Science 149 (1965) 269-274",
             "R. B. Zajonc, A. Heingartner and E. M. Herman, Social enhancement and impairment of performance in the "
             "cockroach, Journal of Personality and Social Psychology 13 (1969)",
             "E. Halfmann, J. Bredehöft and J. A. Häusser, Replicating roaches: a preregistered direct replication of "
             "Zajonc, Heingartner, and Herman's (1969) social-facilitation study, Psychological Science 31 (2020) "
             "332-337",
             "W. Stroebe, The truth about Triplett (1898), but nobody seems to care, Perspectives on Psychological "
             "Science 7 (2012) 54-57"),
    checked="2026-11-16",
))

add(Finding(
    key="social_loafing", part=34, title=r"Social loafing",
    claim="People exert less effort on a collective task than when working alone.",
    original=Study("Latané, Williams and Harkins", 1979, n="students shouting and clapping",
                   found="82% of solo effort with one other, 74% with five"),
    status="replicated",
    record=(Study("Karau and Williams (meta-analysis)", 1993, n="78 studies",
                  found="moderate and general; smaller when effort is identifiable or the task matters"),),
    note="One of the steadier group effects; the collective effort model predicts when it shrinks.",
    sources=("B. Latané, K. Williams and S. Harkins, Many hands make light the work, Journal of Personality and Social "
             "Psychology 37 (1979)",
             "S. J. Karau and K. D. Williams, Social loafing: a meta-analytic review and theoretical integration, "
             "Journal of Personality and Social Psychology 65 (1993) 681-706"),
    checked="2026-11-16",
))

add(Finding(
    key="groupthink", part=34, title=r"Groupthink",
    claim="Cohesive, insulated groups under directive leaders seek consensus and make defective decisions.",
    original=Study("Janis", 1972, n="historical case studies", design="American foreign-policy fiascos",
                   found="a syndrome of concurrence-seeking"),
    status="contested",
    record=(Study("Fuller and Aldag (review)", 1998, n="25 years of research",
                  found="virtually devoid of support"),
),
    note="Case studies fit it; experiments rarely confirm its causal model.",
    sources=("I. L. Janis, Victims of Groupthink (1972)",
             "S. R. Fuller and R. J. Aldag, Organizational Tonypandy: lessons from a quarter century of the "
             "groupthink phenomenon, Organizational Behavior and Human Decision Processes 73 (1998) 163-184"),

    checked="2026-11-16",
))

add(Finding(
    key="hotel_towel_norms", part=34, title=r"Descriptive norms on a hotel card",
    claim="Telling guests that most guests reuse their towels increases towel reuse more than an environmental "
          "appeal.",
    original=Study("Goldstein, Cialdini and Griskevicius", 2008, n="1,058 opportunities, one US hotel",
                   found="44.1% against 35.1%; the same-room norm did best"),
    status="contested",
    record=(Study("Bohner and Schlüter", 2014, n="two German hotels (724 and 204)",
                  found="both messages beat no message; the norm no better than the standard appeal"),),
    note="Norm messages help, but their edge over ordinary appeals depends on the setting.",
    sources=("N. J. Goldstein, R. B. Cialdini and V. Griskevicius, A room with a viewpoint, Journal of Consumer "
             "Research 35 (2008) 472-482",
             "G. Bohner and L. E. Schlüter, A room with a viewpoint revisited, PLOS ONE 9 (2014) e104086"),
    checked="2026-11-16",
))

add(Finding(
    key="crowd_influence", part=34, title=r"Social influence undermines the wisdom of crowds",
    claim="Seeing others' estimates reduces a crowd's diversity without making it more accurate.",
    original=Study("Lorenz, Rauhut, Schweitzer and Helbing", 2011, n="144 people, factual estimates",
                   found="less diversity, no gain in accuracy, more confidence"),
    status="contested",
    record=(Study("Becker, Brackbill and Centola", 2017, n="networked estimation experiments",
                  found="in decentralized networks, influence improved accuracy; in centralized ones it could hurt"),),
    note="Whether influence helps or harms a crowd depends on who is listened to: the network decides.",
    sources=("J. Lorenz, H. Rauhut, F. Schweitzer and D. Helbing, How social influence can undermine the wisdom of "
             "crowd effect, PNAS 108 (2011) 9020-9025",
             "J. Becker, D. Brackbill and D. Centola, Network dynamics of social influence in the wisdom of crowds, "
             "PNAS 114 (2017) E5070-E5076",
             "F. Galton, Vox populi, Nature (7 March 1907)"),
    checked="2026-11-16",
))

shown(34, r"Asch (1951, \ 1955, \ 1956)", "Asch's procedure, described; the conformity row is asch_conformity")
shown(34, r"Sherif (1935); \ Jacobs \& Campbell (1961)", "the founding norm studies, described, with an illustration of "
      "the design")
shown(34, r"Haslam \& Reicher (2012); \ Haslam, \ Reicher \& Millard (2015)", "readings of Milgram, part of the "
      "milgram_obedience row's record")
shown(34, r"the Stanford prison experiment (1971)", "the study as taught; its row is stanford_prison")
shown(34, r"Darley \& Latan\'e (1968); \ Latan\'e \& Darley (1968)", "the intercom and smoke studies; the row is "
      "bystander_effect")
shown(34, r"Latan\'e, \ Williams \& Harkins (1979); \ Karau \& Williams (1993)", "the social_loafing row")
shown(34, r"Stoner (1961); \ Moscovici \& Zavalloni (1969)", "the history of group polarization, described")
shown(34, r"Janis (1972); \ Fuller \& Aldag (1998); \ Baron (2005)", "the groupthink row and a later review")
shown(34, r"Moscovici, \ Lage \& Naffrechoux (1969)", "minority influence, described with its reported figures")
shown(34, r"Hovland \& Weiss (1951); \ Hovland, \ Janis \& Kelley (1953)", "the Yale programme and the sleeper "
      "effect, described with the later meta-analysis")
shown(34, r"Petty, \ Cacioppo \& Goldman (1981)", "the elaboration likelihood model's founding study, drawn "
      "schematically")
shown(34, r"Cialdini (1984)", "a book of principles from field observation, described; Part 55 tests nudges")
shown(34, r"Galton (1907); \ Wallis (2014)", "a historical demonstration and its reanalysis; the crowd row is "
      "crowd_influence")
shown(34, r"Muchnik, \ Aral \& Taylor (2013)", "a randomized field experiment on ratings, described in practice")
shown(34, r"Bond et al.\ (2012)", "a randomized field experiment on voting, described in practice")
shown(34, r"Husz\'ar et al.\ (2022)", "a randomized platform audit, described in the frontier")

# --- Part 35: Social Cognition ---------------------------------------------------------------------------------------

add(Finding(
    key="correspondence_bias", part=35, title=r"The correspondence bias",
    claim="Observers infer a person's attitude from what they say or do even when the situation forced it.",
    original=Study("Jones and Harris", 1967, n="Duke students", design="essays on Castro, writer chose or was assigned",
                   found="a pro-Castro essay read as a pro-Castro writer even when the topic was assigned by coin toss"),
    status="replicated",
    record=(Study("Gilbert and Malone (review)", 1995, found="a robust bias, with four mechanisms behind it"),
            Study("Nalipay and colleagues", 2017, n="Filipino students", design="the essay paradigm, political attitude",
                  found="the attribution to the writer reappeared"),
            Study("Walker, Smith and Vul", 2022, found="much of it is what a rational observer unsure of the constraint "
                                                      "would infer")),
    note="The effect reproduces; whether it is an error depends on how sure the observer can be about the situation.",
    sources=("E. E. Jones and V. A. Harris, The attribution of attitudes, Journal of Experimental Social Psychology "
             "3 (1967) 1-24",
             "D. T. Gilbert and P. S. Malone, The correspondence bias, Psychological Bulletin 117(1) (1995) 21-38",
             "Philippine Journal of Psychology (2017), a replication of Jones and Harris with a political attitude",
             "D. E. Walker, K. A. Smith and E. Vul, The fundamental attribution error is rational in an uncertain "
             "world, Decision (2022)"),
    checked="2026-11-16",
))

add(Finding(
    key="induced_compliance", part=35, title=r"Induced-compliance dissonance",
    claim="Freely choosing to argue against your own view moves your attitude toward what you argued, more than "
          "being told to.",
    original=Study("Festinger and Carlsmith", 1959, n="71 men", design="paid one dollar or twenty to call a dull task interesting",
                   found="the one-dollar group rated the task more enjoyable"),
    status="failed",
    record=(Study("Vaidis and colleagues (multi-site)", 2024, n="4,898 people, 39 labs, 19 countries",
                  design="high against low choice to write a counterattitudinal essay",
                  found="no difference between high and low choice; writing the essay itself shifted attitudes"),),
    note="The core prediction of the choice manipulation did not replicate; other dissonance paradigms are untested "
         "here.",
    sources=("L. Festinger and J. M. Carlsmith, Cognitive consequences of forced compliance, Journal of Abnormal and "
             "Social Psychology 58(2) (1959) 203-210",
             "D. C. Vaidis et al., A multilab replication of the induced-compliance paradigm of cognitive dissonance, "
             "Advances in Methods and Practices in Psychological Science 7(1) (2024)"),
    checked="2026-11-16",
))

add(Finding(
    key="false_consensus", part=35, title=r"The false-consensus effect",
    claim="People overestimate how many others share their own choices and opinions.",
    original=Study("Ross, Greene and House", 1977, n="Stanford students", design="wear a sandwich board, or refuse",
                   found="each group thought most others would choose as they did"),
    status="replicated",
    record=(Study("Mullen and colleagues (meta-analysis)", 1985, n="115 hypothesis tests", effect=0.3, unit="r",
                  found="a reliable effect of moderate size"),),
    note="Reliable and moderate; some of it is reasonable inference from a sample of one.",
    sources=("L. Ross, D. Greene and P. House, The false consensus effect, Journal of Experimental Social Psychology "
             "13 (1977) 279-301",
             "B. Mullen et al., The false consensus effect: a meta-analysis of 115 hypothesis tests, Journal of "
             "Experimental Social Psychology 21 (1985) 262-283"),
    checked="2026-11-16",
))

add(Finding(
    key="dunning_kruger", part=35, title=r"The Dunning-Kruger pattern",
    claim="The least skilled overestimate their standing the most, because they lack the skill to see their errors.",
    original=Study("Kruger and Dunning", 1999, n="four studies", design="humour, grammar and logic",
                   found="the bottom quarter scored near the 12th percentile and placed themselves near the 62nd"),
    status="contested",
    record=(Study("Nuhfer and colleagues", 2016, found="random numbers reproduce much of the famous graph"),
            Study("McIntosh and colleagues", 2019, found="evidence for the metacognitive explanation weaker than "
                                                          "claimed")),
    note="The graph replicates easily; how much of it is a metacognitive deficit, rather than regression and a "
         "better-than-average shift, is argued.",
    sources=("J. Kruger and D. Dunning, Unskilled and unaware of it, Journal of Personality and Social Psychology "
             "77(6) (1999) 1121-1134",
             "E. Nuhfer et al., Random number simulations reveal how random noise affects the measurements and "
             "graphical portrayals of self-assessed competency, Numeracy 9(1) (2016)",
             "R. D. McIntosh et al., Wise up: clarifying the role of metacognition in the Dunning-Kruger effect, "
             "Journal of Experimental Psychology: General (2019)"),
    checked="2026-11-16",
))

add(Finding(
    key="better_than_average", part=35, title=r"The better-than-average effect",
    claim="Most people rate themselves above the median on desirable traits and skills.",
    original=Study("Svenson", 1981, n="US and Swedish students", design="driving skill against the group",
                   found="93% of the US sample placed themselves above the median"),
    status="replicated",
    record=(Study("Koppel and colleagues (preregistered)", 2023, n="1,203 people",
                  found="the effect replicated"),),
    note="Robust; part of it reflects vague traits each person can define in their own favour.",
    sources=("O. Svenson, Are we all less risky and more skillful than our fellow drivers?, Acta Psychologica 47(2) "
             "(1981) 143-148",
             "L. Koppel et al., a preregistered replication of Svenson (1981), Meta-Psychology (2023)"),
    checked="2026-11-16",
))

add(Finding(
    key="elderly_priming", part=35, title=r"Behavioural priming by the elderly stereotype",
    claim="Reading words about old age makes people walk more slowly afterwards.",
    original=Study("Bargh, Chen and Burrows", 1996, design="scrambled sentences, then a timed walk to the elevator",
                   found="primed students walked more slowly"),
    status="failed",
    record=(Study("Doyen, Klein, Pichon and Cleeremans", 2012, design="walking timed by infrared sensors",
                  found="no effect; slowing appeared only when experimenters expected it"),),
    note="The likely source of the original effect is the experimenters; semantic priming inside a task is a "
         "different and solid finding.",
    sources=("J. A. Bargh, M. Chen and L. Burrows, Automaticity of social behavior, Journal of Personality and Social "
             "Psychology 71(2) (1996) 230-244",
             "S. Doyen, O. Klein, C.-L. Pichon and A. Cleeremans, Behavioral priming: it's all in the mind, but whose "
             "mind?, PLOS ONE 7(1) (2012) e29081"),
    checked="2026-11-16",
))

add(Finding(
    key="power_posing", part=35, title=r"Power posing",
    claim="Holding an expansive pose for two minutes raises testosterone, lowers cortisol and increases risk-taking.",
    original=Study("Carney, Cuddy and Yap", 2010, n="42 people", design="expansive or contracted poses",
                   found="hormone changes and more risk-taking in expansive posers"),
    status="failed",
    record=(Study("Ranehill and colleagues", 2015, n="200 people",
                  found="more self-reported power; no effect on hormones or behaviour"),
            Study("Carney (public statement)", 2016, found="the first author no longer believed the effects real")),
    note="The hormonal and behavioural claims failed; a small effect on how powerful people say they feel remains.",
    sources=("D. R. Carney, A. J. C. Cuddy and A. J. Yap, Power posing, Psychological Science 21(10) (2010) 1363-1368",
             "E. Ranehill et al., Assessing the robustness of power posing, Psychological Science 26(5) (2015) 653-656",
             "D. R. Carney, My position on power poses (2016)"),
    checked="2026-11-16",
))

add(Finding(
    key="inverse_planning", part=35, title=r"Goal inference as inverse planning",
    claim="People infer an agent's goal from its movement as a Bayesian observer of a roughly rational planner would.",
    original=Study("Baker, Saxe and Tenenbaum", 2009, design="three experiments, agents moving in mazes",
                   found="the model's goal inferences tracked people's (r = .96 in the 2007 version)"),
    status="replicated",
    record=(Study("Baker, Jara-Ettinger, Saxe and Tenenbaum", 2017, design="food trucks",
                  found="beliefs, desires and percepts inferred jointly, again close to the model"),),
    note="Replicated within the research programme and extended; independent tests of the same stimuli are fewer.",
    sources=("C. L. Baker, R. Saxe and J. B. Tenenbaum, Action understanding as inverse planning, Cognition 113(3) "
             "(2009) 329-349",
             "C. L. Baker, J. Jara-Ettinger, R. Saxe and J. B. Tenenbaum, Rational quantitative attribution of "
             "beliefs, desires and percepts in human mentalizing, Nature Human Behaviour 1 (2017) 0064"),
    checked="2026-11-16",
))

shown(35, r"Ajzen (1991); \ Glasman \& Albarrac\'in (2006)", "a theory and a meta-analysis of when attitudes predict, "
      "described without effect sizes")
shown(35, r"Ambady \& Rosenthal (1993)", "thin slices, described qualitatively; Part 53 weighs interviews")
shown(35, r"Bem (1967); \ Fazio, \ Zanna \& Cooper (1977)", "the rival theory to dissonance, described; the "
      "induced_compliance row carries the test")
shown(35, r"Festinger, \ Riecken \& Schachter (1956)", "an observational case study, told with its later criticism")
shown(35, r"Heider \& Simmel (1944)", "a demonstration the viewer takes part in; no effect size is claimed")
shown(35, r"Kosinski (2024)", "a contested result about language models, described in the frontier; Part 60 returns")
shown(35, r"LaPiere (1934)", "a historical field study, described with its known flaw")
shown(35, r"Mitchell (2008)", "an imaging comparison, described in the mentalizing chapter")
shown(35, r"Ng \& Russell (2000)", "an algorithm, described in practice")
shown(35, r"Saxe \& Kanwisher (2003)", "an imaging localizer, described; its specificity is discussed with Mitchell "
      "(2008)")
shown(35, r"Svenson (1981); \ Mezulis et al.\ (2004)", "the better_than_average row, and a meta-analysis of "
      "self-serving attributions shown with its effect size")
shown(35, r"Todorov et al.\ (2005)", "a correlational election study, described with its published figure")
shown(35, r"Ullman (2023)", "a critique of a language-model result, described in the frontier")
shown(35, r"Willis \& Todorov (2006)", "a judgment-agreement study, described; agreement is not accuracy")

# --- Part 36: Us and Them -------------------------------------------------------------------------------------------

add(Finding(
    key="minimal_group", part=36, title=r"Favouritism in minimal groups",
    claim="Assigning people to groups by a trivial criterion is enough for them to favour their own group.",
    original=Study("Tajfel, Billig, Bundy and Flament", 1971, n="Bristol schoolboys aged 14-15",
                   design="dot estimation or Klee against Kandinsky; points allocated by matrices",
                   found="the boys favoured their own group, often at the cost of its absolute gain"),
    status="replicated",
    record=(Study("Balliet, Wu and De Dreu (meta-analysis)", 2014, n="212 studies",
                  found="d = 0.19 where groups are only labels; 0.42 where outcomes are interdependent"),),
    note="Robust but modest when groups are mere labels; mostly more warmth for the ingroup, not hostility to the "
         "outgroup.",
    sources=("H. Tajfel, M. G. Billig, R. P. Bundy and C. Flament, Social categorization and intergroup behaviour, "
             "European Journal of Social Psychology 1(2) (1971) 149-178",
             "D. Balliet, J. Wu and C. K. W. De Dreu, Ingroup favoritism in cooperation: a meta-analysis, "
             "Psychological Bulletin 140(6) (2014) 1556-1581"),
    checked="2026-11-16",
))

add(Finding(
    key="iat_group", part=36, title=r"Implicit associations, on average",
    claim="On average, people sort faster when categories and attributes are paired as common associations pair "
          "them.",
    original=Study("Greenwald, McGhee and Schwartz", 1998, n="three experiments",
                   design="the Implicit Association Test",
                   found="large differences between compatible and incompatible pairings"),
    status="replicated",
    record=(Study("Greenwald and Lai (review)", 2020, found="internal consistency about .8; test-retest about .5"),),
    note="The average effect is robust across samples; what it means for any one person is the next row.",
    sources=("A. G. Greenwald, D. E. McGhee and J. L. K. Schwartz, Measuring individual differences in implicit "
             "cognition: the implicit association test, Journal of Personality and Social Psychology 74(6) (1998)",
             "A. G. Greenwald and C. K. Lai, Implicit social cognition, Annual Review of Psychology 71 (2020)"),
    checked="2026-11-16",
))

add(Finding(
    key="iat_individual", part=36, title=r"IAT scores predicting a person's behaviour",
    claim="A person's IAT score predicts their discriminatory behaviour well enough to judge or select "
          "individuals, and changing it changes behaviour.",
    original=Study("Greenwald and colleagues (meta-analysis)", 2009, effect=0.24, unit="r",
                   found="IAT scores predicted racially discriminatory behaviour at r = .24, self-reports at .12"),
    status="failed",
    record=(Study("Oswald, Mitchell, Blanton, Jaccard and Tetlock", 2013,
                  found="poor prediction of most criteria, no better than explicit measures"),
            Study("Forscher and colleagues (meta-analysis)", 2019, n="492 studies, 87,418 people",
                  found="implicit scores can be changed; the changes did not carry through to behaviour")),
    note="With retest reliability near .5 and correlations near .1 to .2, the score is a weak guide to one person; "
         "changing it is not a way to change behaviour.",
    sources=("A. G. Greenwald et al., Understanding and using the Implicit Association Test III: meta-analysis of "
             "predictive validity, Journal of Personality and Social Psychology 97(1) (2009)",
             "F. L. Oswald, G. Mitchell, H. Blanton, J. Jaccard and P. E. Tetlock, Predicting ethnic and racial "
             "discrimination: a meta-analysis of IAT criterion studies, Journal of Personality and Social "
             "Psychology 105(2) (2013)",
             "P. S. Forscher et al., A meta-analysis of procedures to change implicit measures, Journal of "
             "Personality and Social Psychology 117(3) (2019) 522-559"),
    checked="2026-11-16",
))

add(Finding(
    key="hiring_audits", part=36, title=r"Discrimination in hiring audits",
    claim="Identical applications receive fewer callbacks when the name signals a Black applicant.",
    original=Study("Bertrand and Mullainathan", 2004, design="fictitious resumes to Boston and Chicago ads",
                   found="white-sounding names received 50% more callbacks"),
    status="replicated",
    record=(Study("Quillian, Pager, Hexel and Midtboen (meta-analysis)", 2017, n="28 studies, 55,842 applications",
                  found="36% more callbacks for white applicants; no change from 1989 to 2015"),),
    note="One of the most consistent findings in the part, measured as behaviour, with no decline in a quarter "
         "century against African Americans.",
    sources=("M. Bertrand and S. Mullainathan, Are Emily and Greg more employable than Lakisha and Jamal?, "
             "American Economic Review 94(4) (2004) 991-1013",
             "L. Quillian, D. Pager, O. Hexel and A. H. Midtboen, Meta-analysis of field experiments shows no change "
             "in racial discrimination in hiring over time, PNAS 114(41) (2017)"),
    checked="2026-11-16",
))

add(Finding(
    key="stereotype_threat", part=36, title=r"Stereotype threat",
    claim="Reminding people of a negative stereotype about their group lowers their test performance.",
    original=Study("Steele and Aronson", 1995, n="Black and white Stanford students",
                   design="a verbal test described as diagnostic or not",
                   found="Black students did worse when the test was called diagnostic (SAT-adjusted scores)"),
    status="contested",
    record=(Study("Sackett, Hardison and Cullen", 2004, found="the adjustment hid the gap; widely misreported"),
            Study("Flore and Wicherts (meta-analysis)", 2015, design="schoolgirls in mathematics and science",
                  found="signs of publication bias"),
            Study("Flore, Mulder and Wicherts (registered)", 2018, n="2,064 Dutch pupils",
                  found="no effect on girls' maths scores, and no moderation")),
    note="Signs of publication bias and null registered tests; the effect may exist in some settings, but its size "
         "and reach are unsettled.",
    sources=("C. M. Steele and J. Aronson, Stereotype threat and the intellectual test performance of African "
             "Americans, Journal of Personality and Social Psychology 69(5) (1995)",
             "P. R. Sackett, C. M. Hardison and M. J. Cullen, On interpreting stereotype threat as accounting for "
             "African American-White differences on cognitive tests, American Psychologist 59(1) (2004)",
             "P. C. Flore and J. M. Wicherts, Does stereotype threat influence performance of girls in stereotyped "
             "domains? A meta-analysis, Journal of School Psychology (2015)",
             "P. C. Flore, J. Mulder and J. M. Wicherts, The influence of gender stereotype threat on mathematics "
             "test scores of Dutch high school students: a registered report, Comprehensive Results in Social "
             "Psychology 3(2) (2018; issue dated 2019) 140-174"),
    checked="2026-11-16",
))

add(Finding(
    key="intergroup_contact", part=36, title=r"Intergroup contact",
    claim="Contact between members of different groups reduces prejudice.",
    original=Study("Pettigrew and Tropp (meta-analysis)", 2006, n="more than 500 studies",
                   found="contact associated with less prejudice; Allport's conditions helpful, not necessary"),
    status="replicated",
    record=(Study("Paluck, Green and Green", 2019, n="27 randomized studies with delayed outcomes",
                  found="consistent with reduced prejudice; weaker for ethnic and racial prejudice"),),
    note="The average holds in experiments too, but the causal evidence is thin where it matters most.",
    sources=("G. W. Allport, The Nature of Prejudice (1954)",
             "T. F. Pettigrew and L. R. Tropp, A meta-analytic test of intergroup contact theory, Journal of "
             "Personality and Social Psychology 90(5) (2006)",
             "E. L. Paluck, S. A. Green and D. P. Green, The contact hypothesis re-evaluated, Behavioural Public "
             "Policy 3(2) (2019) 129-158"),
    checked="2026-11-16",
))

add(Finding(
    key="deep_canvassing", part=36, title=r"Deep canvassing",
    claim="A single conversation at the door can durably reduce prejudice.",
    original=Study("LaCour and Green", 2014, design="canvassing on same-sex marriage",
                   found="large, lasting effects; the data were fabricated and the paper retracted in 2015"),
    status="replicated",
    record=(Study("Broockman and Kalla", 2016, n="Miami-Dade voters", design="randomized, about 10 minutes",
                  found="about 10 points warmer toward transgender people, lasting months"),),
    note="Replicated in a real experiment by the people who exposed the fake one; the first report remains "
         "retracted.",
    sources=("M. J. LaCour and D. P. Green, When contact changes minds, Science 346 (2014), retracted 2015",
             "D. Broockman and J. Kalla, Durably reducing transphobia: a field experiment on door-to-door "
             "canvassing, Science 352 (2016) 220-224"),
    checked="2026-11-16",
))

add(Finding(
    key="robbers_cave", part=36, title=r"Robbers Cave",
    claim="Competition between groups of boys at a summer camp produced hostility, and shared goals removed it.",
    original=Study("Sherif and colleagues", 1954, n="22 boys, Oklahoma", design="bonding, contests, shared goals",
                   found="hostility under competition, reduced by superordinate goals"),
    status="story and record",
    record=(Study("Perry", 2018, design="Sherif's archives",
                  found="an earlier 1953 run in which the boys would not turn on each other, and staff provocation"),),
    note="A demonstration with the conditions arranged, after a failed first attempt left out of the report.",
    sources=("M. Sherif, O. J. Harvey, B. J. White, W. R. Hood and C. W. Sherif, Intergroup Conflict and "
             "Cooperation: The Robbers Cave Experiment (1961)",
             "G. Perry, The Lost Boys: Inside Muzafer Sherif's Robbers Cave Experiment (2018)"),
    checked="2026-11-16",
))

shown(36, r"Chang et al.\ (2019)", "a randomized field evaluation of a diversity training, described in its own terms")
shown(36, r"Fiske, \ Cuddy, \ Glick \& Xu (2002)", "a descriptive model of stereotype content, shown without effect sizes")
shown(36, r"Hamilton \& Gifford (1976)", "the illusory-correlation design, described; the judged rates on screen are "
      "Psyche's model")
shown(36, r"Paluck (2009)", "a randomized field experiment, described qualitatively")
shown(36, r"Paluck, \ Porat, \ Clark \& Green (2021)", "a review of the field's evidence, described")
shown(36, r"Payne, \ Vuletich \& Lundberg (2017); \ Connor \& Evers (2020)", "a theoretical debate, described in the "
      "frontier")
shown(36, r"Tajfel \& Turner (1979); \ Turner et al.\ (1987)", "theories, described; the minimal_group row carries the "
      "evidence")

# --- Part 37: Bonds and Bargains -------------------------------------------------------------------------------------

add(Finding(
    key="ultimatum_rejection", part=37, title=r"Fair offers and costly rejections",
    claim="In the ultimatum game proposers offer far more than the minimum, and responders reject low offers at a cost "
          "to themselves.",
    original=Study("Guth, Schmittberger and Schwarze", 1982, design="the first ultimatum experiments",
                   found="average offers near 37% of the sum; low offers rejected"),
    status="replicated",
    record=(Study("Oosterbeek, Sloof and van de Kuilen (meta-analysis)", 2004, n="37 papers, 75 results",
                  found="average offer 40%"),
            Study("Henrich and colleagues", 2001, n="15 small-scale societies",
                  found="no society matched the selfish prediction; mean offers 26% to 58%")),
    note="One of the most reproducible results in experimental economics; its size varies with culture and stakes.",
    sources=("W. Guth, R. Schmittberger and B. Schwarze, An experimental analysis of ultimatum bargaining, Journal of "
             "Economic Behavior and Organization 3 (1982) 367-388",
             "H. Oosterbeek, R. Sloof and G. van de Kuilen, Cultural differences in ultimatum game experiments, "
             "Experimental Economics 7 (2004) 171-188",
             "J. Henrich et al., In search of homo economicus, American Economic Review 91 (2001) 73-78"),
    checked="2026-11-16",
))

add(Finding(
    key="punishment_cooperation", part=37, title=r"Punishment sustaining cooperation",
    claim="When group members can punish free riders at a cost to themselves, contributions to a public good hold "
          "up instead of decaying.",
    original=Study("Fehr and Gachter", 2002, design="public-goods games with and without costly punishment",
                   found="cooperation flourished with punishment and broke down without it"),
    status="replicated",
    record=(Study("Herrmann, Thoni and Gachter", 2008, n="16 participant pools",
                  found="antisocial punishment of cooperators removed the benefit in some societies"),),
    note="Robust where punishment targets free riders; where cooperators are punished too, the benefit can vanish.",
    sources=("E. Fehr and S. Gachter, Altruistic punishment in humans, Nature 415 (2002) 137-140",
             "B. Herrmann, C. Thoni and S. Gachter, Antisocial punishment across societies, Science 319 (2008) "
             "1362-1367"),
    checked="2026-11-16",
))

add(Finding(
    key="mere_exposure", part=37, title=r"Mere exposure",
    claim="Repeated exposure to a stimulus increases liking for it.",
    original=Study("Zajonc", 1968, design="repeated exposure to unfamiliar stimuli", found="liking rose with exposure"),
    status="replicated",
    record=(Study("Bornstein (meta-analysis)", 1989, n="208 experiments", effect=0.26, unit="r",
                  found="a reliable effect"),
            Study("Montoya and colleagues (meta-analysis)", 2017, n="268 curves, 81 articles",
                  found="an inverted U: liking rises, then falls with many exposures")),
    note="Reliable, with limits: the effect peaks and declines with many exposures.",
    sources=("R. B. Zajonc, Attitudinal effects of mere exposure, Journal of Personality and Social Psychology "
             "Monograph 9(2) (1968)",
             "R. F. Bornstein, Exposure and affect: overview and meta-analysis of research, 1968-1987, Psychological "
             "Bulletin 106(2) (1989)",
             "R. M. Montoya et al., A re-examination of the mere exposure effect, Psychological Bulletin (2017)"),
    checked="2026-11-16",
))

add(Finding(
    key="stated_preferences", part=37, title=r"Stated preferences predicting desire",
    claim="The partner qualities people say they want, and the sex differences in them, predict whom they come to "
          "desire when they meet.",
    original=Study("Buss", 1989, n="10,047 people, 37 cultures", design="ratings of an ideal partner",
                   found="men weighted attractiveness, women earning prospects, more"),
    status="failed",
    record=(Study("Eastwick and Finkel", 2008, design="speed dating and follow-up",
                  found="the sex differences in stated preferences did not appear in actual desire"),
            Study("Joel, Eastwick and Finkel", 2017, n="two speed-dating studies, 100+ measures",
                  found="desire unique to a pair was not predictable at all")),
    note="Stated preferences replicate as statements (the next row but one); as predictions of desire in person they "
         "fail.",
    sources=("D. M. Buss, Sex differences in human mate preferences, Behavioral and Brain Sciences 12 (1989) 1-49",
             "P. W. Eastwick and E. J. Finkel, Sex differences in mate preferences revisited, Journal of Personality "
             "and Social Psychology 94(2) (2008)",
             "S. Joel, P. W. Eastwick and E. J. Finkel, Is romantic desire predictable?, Psychological Science 28 "
             "(2017)"),
    checked="2026-11-16",
))

add(Finding(
    key="divorce_prediction", part=37, title=r"Divorce predicted with 90\% accuracy",
    claim="Observing how a couple argues predicts which couples will divorce with about 90% accuracy.",
    original=Study("Gottman and colleagues", 1998, n="newlywed couples",
                   found="a model fitted the outcomes with about 90% accuracy"),
    status="contested",
    record=(Study("Heyman and Slep", 2001, found="the figures were in-sample fits; accuracy falls under "
                                                  "cross-validation, and base rates matter"),
            Study("Joel and colleagues", 2020, n="11,196 couples",
                  found="change in relationship quality largely unpredictable")),
    note="Process findings about conflict may hold; the headline accuracy was never shown on new couples.",
    sources=("J. M. Gottman, J. Coan, S. Carrere and C. Swanson, Predicting marital happiness and stability from "
             "newlywed interactions, Journal of Marriage and the Family 60 (1998)",
             "R. E. Heyman and A. M. Smith Slep, The hazards of predicting divorce without crossvalidation, Journal of "
             "Marriage and Family 63 (2001)",
             "S. Joel et al., Machine learning uncovers the most robust self-report predictors of relationship "
             "quality across 43 longitudinal couples studies, PNAS 117(32) (2020)"),
    checked="2026-11-16",
))

add(Finding(
    key="mate_preferences", part=37, title=r"Sex differences in stated mate preferences",
    claim="Across cultures, men say they value physical attractiveness and youth in a partner more than women do, "
          "and women value earning prospects more.",
    original=Study("Buss", 1989, n="10,047 people, 37 cultures", found="the differences in most cultures"),
    status="replicated",
    record=(Study("Walter and colleagues", 2020, n="14,399 people, 45 countries",
                  found="the same differences; not robustly predicted by gender equality or pathogens"),),
    note="Replicated as stated preferences; what they mean for actual choice is two rows up.",
    sources=("D. M. Buss, Sex differences in human mate preferences, Behavioral and Brain Sciences 12 (1989) 1-49",
             "K. V. Walter et al., Sex differences in mate preferences across 45 countries: a large-scale "
             "replication, Psychological Science 31(4) (2020)"),
    checked="2026-11-16",
))

add(Finding(
    key="isolation_mortality", part=37, title=r"Social relationships and survival",
    claim="People with stronger social relationships are more likely to survive over follow-up periods.",
    original=Study("Holt-Lunstad, Smith and Layton (meta-analysis)", 2010, n="148 studies, 308,849 people",
                   effect=1.50, unit="OR", lo=1.42, hi=1.59, found="odds of survival 1.5 times higher"),
    status="replicated",
    record=(Study("Holt-Lunstad and colleagues (meta-analysis)", 2015,
                  found="isolation OR 1.29, loneliness 1.26, living alone 1.32 for mortality"),),
    note="A robust association; whether connection causes survival is not established by these observational data.",
    sources=("J. Holt-Lunstad, T. B. Smith and J. B. Layton, Social relationships and mortality risk: a "
             "meta-analytic review, PLoS Medicine 7(7) (2010) e1000316",
             "J. Holt-Lunstad et al., Loneliness and social isolation as risk factors for mortality, Perspectives on "
             "Psychological Science 10(2) (2015)"),
    checked="2026-11-16",
))

shown(37, r"Festinger, \ Schachter \& Back (1950)", "a field study of friendship and proximity, described without its "
      "percentages")
shown(37, r"Hazan \& Shaver (1987); \ Rusbult (1980)", "a self-selected survey and a theory of commitment, described")

# --- Part 38: Culture and Morals -------------------------------------------------------------------------------------

add(Finding(
    key="weird_samples", part=38, title=r"Psychology's WEIRD samples",
    claim="Most participants in psychology's leading journals come from Western, educated, industrialized, rich and "
          "democratic societies, which hold a small share of humanity.",
    original=Study("Arnett", 2008, n="six APA journals, 2003 to 2007", design="a count of sample origins",
                   found="68% of samples from the United States, 96% from Western industrialized countries"),
    status="replicated",
    record=(Study("Henrich, Heine and Norenzayan (review)", 2010, found="these samples are often outliers on "
                  "perception, fairness, cooperation, reasoning and the self"),
            Study("Rad, Martingano and Ginges", 2018, n="Psychological Science, 2014",
                  found="about half the samples American; generalization rarely justified"),
            Study("Thalmayer, Toscanelli and Arnett", 2021, n="the same six journals, 2014 to 2018",
                  found="a little over 60% American; majority-world samples about 4 to 5%")),
    note="Still true a decade on; the share from other Western countries grew, not the share from the majority world.",
    sources=("J. J. Arnett, The neglected 95%: why American psychology needs to become less American, American "
             "Psychologist 63 (2008) 602-614",
             "J. Henrich, S. J. Heine and A. Norenzayan, The weirdest people in the world?, Behavioral and Brain "
             "Sciences 33 (2010) 61-83",
             "M. S. Rad, A. J. Martingano and J. Ginges, Toward a psychology of Homo sapiens, PNAS 115 (2018)",
             "A. G. Thalmayer, C. Toscanelli and J. J. Arnett, The neglected 95% revisited, American Psychologist 76 "
             "(2021) 116-129"),
    checked="2026-11-16",
))

add(Finding(
    key="self_construal", part=38, title=r"Independent and interdependent selves",
    claim="People in East Asian cultures construe the self as interdependent and people in Western cultures as "
          "independent, and questionnaires measure the difference.",
    original=Study("Markus and Kitayama", 1991, design="a theory with supporting studies",
                   found="two construals of the self shaping cognition, emotion and motivation"),
    status="contested",
    record=(Study("Oyserman, Coon and Kemmelmeier (meta-analysis)", 2002, n="individualism and collectivism scales",
                  found="European Americans more individualistic and less collectivistic, with differences smaller "
                        "and less consistent than assumed and dependent on the scale"),
            Study("Heine, Lehman, Peng and Greenholtz", 2002, design="self-reports against expert judgments",
                  found="reference-group effects can hide expected differences on Likert scales")),
    note="Behavioural and attentional differences replicate better than self-report scales; the measures, not the "
         "idea, are the weak point.",
    sources=("H. R. Markus and S. Kitayama, Culture and the self, Psychological Review 98 (1991) 224-253",
             "D. Oyserman, H. M. Coon and M. Kemmelmeier, Rethinking individualism and collectivism, Psychological "
             "Bulletin 128 (2002) 3-72",
             "S. J. Heine, D. R. Lehman, K. Peng and J. Greenholtz, What's wrong with cross-cultural comparisons of "
             "subjective Likert scales?, Journal of Personality and Social Psychology 82 (2002) 903-918"),
    checked="2026-11-16",
))

add(Finding(
    key="rice_theory", part=38, title=r"The rice theory",
    claim="People from rice-farming regions think more holistically and interdependently than people from "
          "wheat-farming regions.",
    original=Study("Talhelm and colleagues", 2014, n="1,162 Han Chinese students from six sites",
                   found="southern rice regions more holistic and interdependent than northern wheat regions"),
    status="contested",
    record=(Study("Ruan, Xie and Zhang", 2014, design="a reanalysis with other crop and survey data",
                  found="weaker and different patterns; corn and other crops grouped with wheat"),
            Study("Thomson and colleagues", 2018, n="nearly 17,000 people in 39 societies",
                  found="lower relational mobility where farming was settled and threat high")),
    note="A bold ecological account with supportive and critical analyses; no independent test has settled it.",
    sources=("T. Talhelm et al., Large-scale psychological differences within China explained by rice versus wheat "
             "agriculture, Science 344 (2014) 603-608",
             "J. Ruan, Z. Xie and X. Zhang, a reanalysis of the rice theory, IFPRI discussion paper (2014)",
             "R. Thomson et al., Relational mobility predicts social behaviors in 39 countries and is tied to "
             "historical farming and threat, PNAS 115 (2018) 7521-7526"),
    checked="2026-11-16",
))

add(Finding(
    key="trolley_universal", part=38, title=r"Switch, loop and footbridge across countries",
    claim="People everywhere find sacrificing one to save five more acceptable by a switch than by personal force.",
    original=Study("Greene and colleagues", 2001, design="personal and impersonal dilemmas",
                   found="personal dilemmas such as the footbridge judged less acceptable"),
    status="replicated",
    record=(Study("Awad and colleagues", 2020, n="70,000 people in 42 countries",
                  found="Switch 81%, Loop 72%, Footbridge 51% on average; the order held in every country"),
            Study("Bago and colleagues", 2022, n="45 countries",
                  found="the personal-force effect in every cultural cluster; its interaction with intention "
                        "inconclusive outside the West")),
    note="The order is universal in these samples; the level of approval varies, lower in Eastern countries.",
    sources=("J. D. Greene et al., An fMRI investigation of emotional engagement in moral judgment, Science 293 "
             "(2001) 2105-2108",
             "E. Awad, S. Dsouza, A. Shariff, I. Rahwan and J.-F. Bonnefon, Universals and variations in moral "
             "decisions made in 42 countries by 70,000 participants, PNAS 117 (2020) 2332-2337",
             "B. Bago et al., Situational factors shape moral judgements in the trolley dilemma in Eastern, Southern "
             "and Western countries in a culturally diverse sample, Nature Human Behaviour 6 (2022) 880-895"),
    checked="2026-11-16",
))

add(Finding(
    key="moral_foundations_structure", part=38, title=r"Five moral foundations across cultures",
    claim="Moral intuitions fall into five foundations (care, fairness, loyalty, authority, purity) that the Moral "
          "Foundations Questionnaire measures the same way across cultures.",
    original=Study("Graham, Haidt and Nosek", 2009, design="questionnaires of moral relevance and judgment",
                   found="liberals weight care and fairness most; conservatives weight all five more evenly"),
    status="contested",
    record=(Study("Iurino and Saucier", 2020, n="the short questionnaire in 27 countries",
                  found="the five-factor model did not fit or converge well across countries"),),
    note="The liberal-conservative pattern is often found; the five-factor structure does not travel cleanly.",
    sources=("J. Graham, J. Haidt and B. A. Nosek, Liberals and conservatives rely on different sets of moral "
             "foundations, Journal of Personality and Social Psychology 96 (2009) 1029-1046",
             "K. Iurino and G. Saucier, Testing measurement invariance of the Moral Foundations Questionnaire across "
             "27 countries, Assessment 27 (2020) 365-372"),
    checked="2026-11-16",
))

add(Finding(
    key="infant_helper", part=38, title=r"Infants preferring helpers",
    claim="Infants of six to ten months prefer a character who helps another to one who hinders it.",
    original=Study("Hamlin, Wynn and Bloom", 2007, n="12 six-month-olds and 16 ten-month-olds",
                   design="the hill paradigm with puppets", found="12 of 12 and 14 of 16 reached for the helper"),
    status="failed",
    record=(Study("Lucca and colleagues (ManyBabies 4)", 2025, n="1,018 infants tested, 567 included, 37 labs",
                  design="a registered multi-laboratory replication", effect=0.4934, unit="share choosing the helper",
                  found="49.3% chose the helper; neither condition differed from chance"),),
    note="The authors conclude the effect is weaker than thought, absent, or develops later.",
    sources=("J. K. Hamlin, K. Wynn and P. Bloom, Social evaluation by preverbal infants, Nature 450 (2007) "
             "557-559",
             "K. Lucca et al., Infants' social evaluation of helpers and hinderers: a large-scale, multi-lab, "
             "coordinated replication study, Developmental Science 28 (2025) e13581"),
    checked="2026-11-16",
))

add(Finding(
    key="population_complexity", part=38, title=r"Population size and cumulative culture",
    claim="Larger, better-connected populations accumulate more complex technology, and small isolated ones lose "
          "skills.",
    original=Study("Henrich", 2004, design="a model of imperfect copying, applied to Tasmania",
                   found="below a critical population, skills decay"),
    status="contested",
    record=(Study("Vaesen, Collard, Cosgrove and Roebroeks", 2016, design="a critique of the models and the data",
                  found="the effect needs restrictive assumptions; hunter-gatherer toolkits track environment "
                        "better"),),
    note="Laboratory transmission chains often show the effect; whether it explains the archaeological record is "
         "argued.",
    sources=("J. Henrich, Demography and cultural evolution, American Antiquity 69 (2004) 197-214",
             "K. Vaesen, M. Collard, R. Cosgrove and W. Roebroeks, Population size does not explain past changes "
             "in cultural complexity, PNAS 113 (2016) E2241-E2247"),
    checked="2026-11-16",
))

add(Finding(
    key="overimitation_culture", part=38, title=r"Overimitation across cultures",
    claim="Children copy a demonstrator's causally unnecessary actions, in every culture tested.",
    original=Study("Horner and Whiten", 2005, n="young chimpanzees and children", design="a puzzle box, opaque or "
                   "transparent, opened after unnecessary actions",
                   found="with a transparent box, chimpanzees skipped the useless actions and children copied them"),
    status="replicated",
    record=(Study("Nielsen and Tomaselli", 2010, n="San children in the Kalahari and Australian children",
                  found="overimitation in both"),
            Study("Berl and Hewlett", 2015, n="Aka and Ngandu children and Aka adults, Congo Basin",
                  found="Aka children overimitated at one of the lowest rates recorded"),
            Study("Stengelin, Hepach and Haun", 2020, design="children in several societies",
                  found="variation in how much, but not whether, children overimitate")),
    note="Found wherever it has been tested; how much children do it varies with culture.",
    sources=("V. Horner and A. Whiten, Causal knowledge and imitation/emulation switching in chimpanzees and "
             "children, Animal Cognition 8 (2005) 164-181",
             "M. Nielsen and K. Tomaselli, Overimitation in Kalahari Bushman children and the origins of human "
             "cultural cognition, Psychological Science 21 (2010) 729-736",
             "M. Berl and B. S. Hewlett, Cultural variation in the use of overimitation by the Aka and Ngandu of the "
             "Congo Basin, PLoS ONE 10 (2015)",
             "R. Stengelin, R. Hepach and D. B. M. Haun, Cross-cultural variation in how much, but not whether, "
             "children overimitate, Journal of Experimental Child Psychology (2020)"),
    checked="2026-11-16",
))

add(Finding(
    key="moral_dumbfounding", part=38, title=r"Moral dumbfounding",
    claim="People keep moral judgments they cannot justify once every reason is ruled out: intuition leads and "
          "reasoning follows.",
    original=Study("Haidt", 2001, design="the social intuitionist model, with harmless-taboo vignettes such as "
                   "consensual sibling incest", found="people condemned the acts and some could give no reason"),
    status="contested",
    record=(Study("Royzman, Kim and Leeman", 2015, design="the sibling vignette with checks on beliefs about harm",
                  found="many rejected the story's harmlessness; beliefs about harm predicted condemnation; true "
                        "dumbfounding rare"),),
    note="Intuitions clearly shape moral judgments; how often people are truly dumbfounded is disputed.",
    sources=("J. Haidt, The emotional dog and its rational tail: a social intuitionist approach to moral judgment, "
             "Psychological Review 108 (2001) 814-834",
             "E. B. Royzman, K. Kim and R. F. Leeman, The curious tale of Julie and Mark: unraveling the moral "
             "dumbfounding effect, Judgment and Decision Making 10 (2015) 296-313"),
    checked="2026-11-16",
))

shown(38, r"Masuda \& Nisbett (2001)", "an attention study described as an example of the theory; the "
      "self_construal row carries the evidence")
shown(38, r"Hofstede (1980); \ Oyserman, \ Coon \& Kemmelmeier (2002)", "measures described; the self_construal row "
      "carries the evidence")
shown(38, r"Thomson et al.\ (2018)", "a cross-national survey described with the rice theory; see its row")
shown(38, r"Schulz et al.\ (2019)", "a historical correlational argument, described with its limits")
shown(38, r"Awad et al.\ (2018)", "a self-selected online sample described; the trolley row carries the classic "
      "cases")
shown(38, r"Klein et al.\ (2018), \ Many Labs 2", "each of its 28 findings belongs to its own topic; described for "
      "its heterogeneity result")
shown(38, r"Simons, \ Shoda \& Lindsay (2017)", "a reporting proposal, not a finding")
shown(38, r"Greene et al.\ (2001); \ McGuire et al.\ (2009)", "a reanalysis of the original response times; the "
      "trolley row carries the personal-force result")
shown(38, r"Atari et al.\ (2023), \ preprint", "a preprint, described as an example in the practice chapter")
shown(38, r"Muthukrishna et al.\ (2020)", "a method for measuring cultural distance, described")

# --- Part 39: What Is a Disorder? ------------------------------------------------------------------------------------

add(Finding(
    key="rosenhan_pseudopatients", part=39, title=r"Sane in insane places",
    claim="Healthy people who faked one symptom were admitted to psychiatric hospitals and never detected: "
          "psychiatric diagnosis cannot tell the sane from the insane.",
    original=Study("Rosenhan", 1973, n="8 pseudopatients, 12 hospitals", design="feigned voices at admission, "
                   "then normal behaviour", found="none detected by staff; most discharged with schizophrenia in "
                   "remission"),
    status="contested",
    record=(Study("Cahalan (an investigation)", 2019, design="a search of Rosenhan's papers and the participants",
                  found="only two other pseudopatients identified; one with a positive experience left out; notes "
                        "that do not match the paper"),),
    note="Never replicated, and the data are in serious doubt; its critique of unreliable diagnosis was taken up by "
         "DSM-III's criteria.",
    sources=("D. L. Rosenhan, On being sane in insane places, Science 179 (1973) 250-258",
             "S. Cahalan, The Great Pretender (Grand Central, 2019)"),
    checked="2026-11-16",
))

add(Finding(
    key="clinical_vs_statistical", part=39, title=r"Formulas beating clinical judgment",
    claim="Combining information by a fixed formula predicts health and behaviour at least as well as an expert's "
          "judgment, and often better.",
    original=Study("Meehl", 1954, design="a review of comparisons between clinical and statistical prediction",
                   found="the formula as good or better in nearly every study"),
    status="replicated",
    record=(Study("Dawes", 1979, design="improper (equal-weight) linear models against expert judges",
                  found="equal weights outperformed the experts"),
            Study("Grove and colleagues (meta-analysis)", 2000, n="studies of human health and behaviour",
                  found="formula clearly better in 33 to 47% of studies, clinician in 6 to 16%")),
    note="One of the most consistent findings in applied psychology; the gap is larger when clinicians add "
         "interview impressions.",
    sources=("P. E. Meehl, Clinical versus Statistical Prediction (University of Minnesota Press, 1954)",
             "R. M. Dawes, The robust beauty of improper linear models in decision making, American Psychologist "
             "34 (1979) 571-582",
             "W. M. Grove, D. H. Zald, B. S. Lebow, B. E. Snitz and C. Nelson, Clinical versus mechanical "
             "prediction: a meta-analysis, Psychological Assessment 12 (2000) 19-30"),
    checked="2026-11-16",
))

add(Finding(
    key="dimensional_structure", part=39, title=r"Disorders as dimensions",
    claim="Most mental disorders are continua with conventional cut-offs rather than distinct categories.",
    original=Study("Haslam, Holland and Kuppens (review)", 2012, n="177 articles, 311 taxometric findings",
                   found="39% reported taxonic, an estimated 14% after correcting for method"),
    status="replicated",
    record=(Study("Haslam, McGrath, Viechtbauer and Kuppens (meta-analysis)", 2020,
                  found="the great majority of latent variables continuous, psychopathology included"),),
    note="A few conditions may be taxonic; for most, where to draw the line is a decision, not a discovery.",
    sources=("N. Haslam, E. Holland and P. Kuppens, Categories versus dimensions in personality and "
             "psychopathology: a quantitative review of taxometric research, Psychological Medicine 42 (2012) "
             "903-920",
             "N. Haslam, M. J. McGrath, W. Viechtbauer and P. Kuppens, Dimensions over categories: a meta-analysis "
             "of taxometric research, Psychological Medicine 50 (2020) 1418-1432"),
    checked="2026-11-16",
))

add(Finding(
    key="p_factor", part=39, title=r"A general factor of psychopathology",
    claim="A single general factor, p, accounts for much of the covariation among mental disorders, and it means "
          "something: a shared liability.",
    original=Study("Caspi and colleagues", 2014, n="the Dunedin cohort, ages 18 to 38",
                   found="one general dimension fitted better than three correlated domains"),
    status="contested",
    record=(Study("Kotov and colleagues (HiTOP)", 2017, design="a consortium's hierarchical model from data",
                  found="spectra under broader dimensions; a general factor as a provisional top level"),),
    note="The statistical pattern is found in many samples; whether p is a cause or a summary is argued, as with g.",
    sources=("A. Caspi et al., The p factor: one general psychopathology factor in the structure of psychiatric "
             "disorders?, Clinical Psychological Science 2 (2014) 119-137",
             "R. Kotov et al., The Hierarchical Taxonomy of Psychopathology (HiTOP), Journal of Abnormal Psychology "
             "126 (2017) 454-477"),
    checked="2026-11-16",
))

add(Finding(
    key="diagnostic_biomarkers", part=39, title=r"Biological tests for diagnosis",
    claim="A laboratory test can diagnose a mental disorder, as the dexamethasone suppression test was claimed to "
          "diagnose melancholic depression.",
    original=Study("Carroll and colleagues", 1981, design="the dexamethasone suppression test",
                   found="reported as a specific test for melancholia"),
    status="failed",
    record=(Study("Kapur, Phillips and Insel (review)", 2012, design="why biological psychiatry lacks clinical "
                  "tests", found="no biomarker has reached routine diagnostic use; candidate tests fail on "
                  "replication and specificity"),),
    note="No laboratory test is used to diagnose a common mental disorder; candidates have not replicated or were "
         "not specific.",
    sources=("B. J. Carroll et al., A specific laboratory test for the diagnosis of melancholia, Archives of "
             "General Psychiatry 38 (1981) 15-22",
             "S. Kapur, A. G. Phillips and T. R. Insel, Why has it taken so long for biological psychiatry to "
             "develop clinical tests and what to do about it?, Molecular Psychiatry 17 (2012) 1174-1179"),
    checked="2026-11-16",
))

shown(39, r"Cahalan, \ \emph{The Great Pretender} (2019)", "an investigation; the rosenhan pseudopatients row "
      "carries it")
shown(39, r"Wakefield (1992)", "a definition, described with its criticism")
shown(39, r"APA (1973, \ 1974)", "a historical decision and its vote, told as history")
shown(39, r"Regier et al.\ (2013)", "field-trial reliabilities quoted as reported, with the caveat about design")
shown(39, r"Robins \& Guze (1970)", "a set of criteria for validity, described")
shown(39, r"Fried \& Nesse (2015)", "a descriptive analysis of one trial's symptoms, quoted for its counts")
shown(39, r"Kessler et al.\ (2005)", "an epidemiological survey, quoted for its estimates")
shown(39, r"Kohn et al.\ (2004); \ Jorm et al.\ (2017)", "epidemiological reviews, quoted for their estimates")
shown(39, r"Cramer et al.\ (2016); \ Borsboom (2017)", "a model and a theory, run on Psyche")
shown(39, r"Nichter (1981); \ Kaiser et al.\ (2015)", "an anthropological concept and a systematic review, "
      "described")
shown(39, r"Kruis \& Maris (2016)", "a mathematical result about models, described")

# --- Part 40: Fear and Sadness ---------------------------------------------------------------------------------------

add(Finding(
    key="exposure_efficacy", part=40, title=r"Exposure therapy for anxiety",
    claim="Treatments built on exposure to what is feared reduce anxiety more than control conditions.",
    original=Study("Wolpe", 1958, design="systematic desensitization: graded imagined exposure with relaxation",
                   found="most phobic patients improved"),
    status="replicated",
    record=(Study("Carpenter and colleagues (meta-analysis)", 2018, n="placebo-controlled trials of cognitive "
                  "behavioural therapy for anxiety disorders", found="moderate benefits over placebo"),
            Study("Craske and colleagues (review)", 2014, found="exposure works; how to make it last is the open "
                  "question")),
    note="Among the best-supported treatments in psychology; relapse after it is common, as the renewal row predicts.",
    sources=("J. Wolpe, Psychotherapy by Reciprocal Inhibition (Stanford University Press, 1958)",
             "J. K. Carpenter et al., Cognitive behavioral therapy for anxiety and related disorders: a meta-analysis "
             "of randomized placebo-controlled trials, Depression and Anxiety 35 (2018) 502-514",
             "M. G. Craske et al., Maximizing exposure therapy: an inhibitory learning approach, Behaviour Research "
             "and Therapy 58 (2014) 10-23"),
    checked="2026-11-16",
))

add(Finding(
    key="fear_renewal", part=40, title=r"The return of extinguished fear",
    claim="Fear removed by extinction returns when the context changes (renewal), with time, or after a reminder.",
    original=Study("Bouton and Bolles", 1979, n="rats", design="conditioning in one context, extinction in another",
                   found="fear returned when tested back in the first context"),
    status="replicated",
    record=(Study("Vervliet, Craske and Hermans (review)", 2013, design="animal and human studies",
                  found="renewal, spontaneous recovery and reinstatement in many species and procedures"),),
    note="Extinction is new, context-bound learning; relapse after exposure therapy fits the pattern.",
    sources=("M. E. Bouton and R. C. Bolles, Contextual control of the extinction of conditioned fear, Learning and "
             "Motivation 10 (1979) 445-466",
             "B. Vervliet, M. G. Craske and D. Hermans, Fear extinction and relapse: state of the art, Annual Review "
             "of Clinical Psychology 9 (2013) 215-248"),
    checked="2026-11-16",
))

add(Finding(
    key="learned_helplessness", part=40, title=r"Learned helplessness",
    claim="Animals exposed to uncontrollable shock later fail to escape when escape is possible, because they have "
          "learned that responding does not matter.",
    original=Study("Seligman and Maier", 1967, n="dogs in three groups", design="escapable, yoked inescapable and "
                   "no shock, then a shuttle box", found="the inescapable group mostly failed to escape"),
    status="replicated",
    record=(Study("Maier and Seligman (review)", 2016, design="decades of neuroscience in rats",
                  found="passivity is the default response to prolonged shock; what is learned is control"),),
    note="The effect replicates; its explanation was reversed by its own authors.",
    sources=("M. E. P. Seligman and S. F. Maier, Failure to escape traumatic shock, Journal of Experimental "
             "Psychology 74 (1967) 1-9",
             "S. F. Maier and M. E. P. Seligman, Learned helplessness at fifty: insights from neuroscience, "
             "Psychological Review 123 (2016) 349-367"),
    checked="2026-11-16",
))

add(Finding(
    key="attention_bias_modification", part=40, title=r"Training attention away from threat",
    claim="Training attention away from threat in a dot-probe task reduces anxiety.",
    original=Study("MacLeod and colleagues", 2002, design="attention training in the dot-probe task",
                   found="trained attention changed, and so did reactions to stress"),
    status="failed",
    record=(Study("Cristea, Kok and Cuijpers (meta-analysis)", 2015, n="randomized trials of bias modification",
                  found="small effects that disappeared after correcting for publication bias"),),
    note="The dot-probe bias score is also too unreliable to measure one person.",
    sources=("C. MacLeod et al., Selective attention and emotional vulnerability, Journal of Abnormal Psychology "
             "111 (2002) 107-123",
             "I. A. Cristea, R. N. Kok and P. Cuijpers, Efficacy of cognitive bias modification interventions in "
             "anxiety and depression: meta-analysis, British Journal of Psychiatry 206 (2015) 7-16"),
    checked="2026-11-16",
))

add(Finding(
    key="serotonin_deficit", part=40, title=r"Depression as low serotonin",
    claim="Depression is caused by a shortage of serotonin, which antidepressants correct.",
    original=Study("Schildkraut and the monoamine hypothesis", 1965, design="inferences from reserpine and "
                   "early antidepressants", found="a monoamine shortage proposed"),
    status="failed",
    record=(Study("Moncrieff and colleagues (umbrella review)", 2022, design="reviews of serotonin and depression",
                  found="no consistent evidence of an association or a cause"),),
    note="Failed as stated; serotonin may matter for some people, and the drugs' effect does not depend on the story.",
    sources=("J. J. Schildkraut, The catecholamine hypothesis of affective disorders, American Journal of "
             "Psychiatry 122 (1965) 509-522",
             "J. Moncrieff et al., The serotonin theory of depression: a systematic umbrella review of the evidence, "
             "Molecular Psychiatry (2022)"),
    checked="2026-11-16",
))

add(Finding(
    key="antidepressants_placebo", part=40, title=r"Antidepressants against placebo",
    claim="Antidepressants relieve depression more than placebo.",
    original=Study("Kirsch and colleagues", 2008, design="trials submitted to the US regulator",
                   found="about 1.8 points on the 52-point Hamilton scale; larger in severe depression"),
    status="replicated, smaller",
    record=(Study("Cipriani and colleagues (network meta-analysis)", 2018, n="522 trials, 116,477 people",
                  found="all 21 drugs more effective than placebo; odds ratios about 1.4 to 2.1"),),
    note="A real and modest average effect over about eight weeks; who benefits most is debated.",
    sources=("I. Kirsch et al., Initial severity and antidepressant benefits, PLoS Medicine 5 (2008) e45",
             "A. Cipriani et al., Comparative efficacy and acceptability of 21 antidepressant drugs, Lancet 391 "
             "(2018) 1357-1366"),
    checked="2026-11-16",
))

add(Finding(
    key="httlpr_stress", part=40, title=r"A serotonin gene and stress",
    claim="Stressful life events cause depression more often in carriers of the short 5-HTTLPR allele.",
    original=Study("Caspi and colleagues", 2003, n="the Dunedin cohort", found="a gene-by-environment interaction"),
    status="failed",
    record=(Study("Culverhouse and colleagues (collaborative meta-analysis)", 2018, n="over 38,000 people",
                  found="no interaction"),
            Study("Border and colleagues", 2019, design="candidate genes in large samples",
                  found="no support for the candidate genes or their interactions")),
    note="Depression is highly polygenic; candidate genes of large effect did not survive large samples (Part 9).",
    sources=("A. Caspi et al., Influence of life stress on depression: moderation by a polymorphism in the 5-HTT "
             "gene, Science 301 (2003) 386-389",
             "R. C. Culverhouse et al., Collaborative meta-analysis finds no evidence of a strong interaction between "
             "stress and 5-HTTLPR genotype, Molecular Psychiatry 23 (2018) 133-142",
             "R. Border et al., No support for historical candidate gene or candidate gene-by-interaction hypotheses "
             "for major depression across multiple large samples, American Journal of Psychiatry 176 (2019) 376-387"),
    checked="2026-11-16",
))

add(Finding(
    key="suicide_prediction", part=40, title=r"Predicting suicidal behaviour",
    claim="Known risk factors predict which individuals will make a suicide attempt with useful accuracy.",
    original=Study("Pokorny", 1983, n="about 4,800 psychiatric inpatients", design="risk factors recorded at "
                   "admission, then follow-up", found="the factors flagged far more people than died, and missed many "
                   "who did"),
    status="failed",
    record=(Study("Franklin and colleagues (meta-analysis)", 2017, n="365 studies",
                  found="prediction only slightly better than chance, and no better over fifty years"),),
    note="Associations are real; individual prediction is poor, largely because of the low base rate.",
    sources=("A. D. Pokorny, Prediction of suicide in psychiatric patients, Archives of General Psychiatry 40 (1983) "
             "249-257",
             "J. C. Franklin et al., Risk factors for suicidal thoughts and behaviors: a meta-analysis of 50 years of "
             "research, Psychological Bulletin 143 (2017) 187-232"),
    checked="2026-11-16",
))

shown(40, r"Mowrer (1947)", "a theory, run on Psyche; the exposure row carries the evidence")
shown(40, r"Craske et al.\ (2014)", "a review of principles; cited in the exposure row")
shown(40, r"Clark (1986)", "a cognitive model of panic, described")
shown(40, r"Beck (1967); \ Abramson, \ Seligman \& Teasdale (1978)", "theories of depression, described")
shown(40, r"Schildkraut (1965)", "the monoamine hypothesis; the serotonin row carries the evidence")
shown(40, r"Brown \& Harris (1978)", "a community interview study, described")
shown(40, r"Cade (1949)", "the discovery of lithium, told as history")
shown(40, r"Gillan et al.\ (2011); \ Gillan et al.\ (2016)", "studies of habit and compulsivity, described; "
      "computational psychiatry is Part 59's")

# --- Part 41: Psychosis, Addiction and Development ---------------------------------------------------------------------

add(Finding(
    key="hollow_mask_schizophrenia", part=41, title=r"The hollow-mask illusion in schizophrenia",
    claim="People with schizophrenia are less often fooled by the hollow-mask illusion than other people.",
    original=Study("Emrich", 1989, design="binocular depth inversion of hollow faces in patients and controls",
                   found="patients saw the hollow face as hollow more often"),
    status="replicated",
    record=(Study("Schneider and colleagues", 2002, design="binocular depth inversion in patients and controls",
                  found="reduced depth inversion in patients"),
            Study("Dima and colleagues", 2009, design="hollow masks during brain imaging, with a model of "
                  "connectivity", found="patients were not fooled; top-down connections differed")),
    note="Replicated in small samples; a large preregistered test is still missing.",
    sources=("H. M. Emrich, A three-component-system hypothesis of psychosis, British Journal of Psychiatry 155 "
             "(suppl. 5) (1989) 37-39",
             "U. Schneider et al., Reduced binocular depth inversion in schizophrenic patients, Schizophrenia "
             "Research 53 (2002) 101-108",
             "D. Dima et al., Understanding why patients with schizophrenia do not perceive the hollow-mask illusion "
             "using dynamic causal modelling, NeuroImage 46 (2009) 1180-1186"),
    checked="2026-11-16",
))

add(Finding(
    key="antipsychotic_efficacy", part=41, title=r"Antipsychotics for positive symptoms",
    claim="Antipsychotic drugs reduce the positive symptoms of schizophrenia and prevent relapse better than "
          "placebo.",
    original=Study("Delay and Deniker", 1952, design="chlorpromazine given to agitated psychotic patients",
                   found="marked calming and reduction of psychotic symptoms"),
    status="replicated",
    record=(Study("Leucht and colleagues (meta-analysis)", 2012, design="relapse-prevention trials against placebo",
                  found="far fewer relapses within a year on the drug"),
            Study("Leucht and colleagues (meta-analysis)", 2017, design="sixty years of placebo-controlled trials in "
                  "acute schizophrenia", found="a moderate average benefit, smaller in recent trials")),
    note="A real effect with real costs: movement disorders, weight gain and metabolic harm, varying by drug.",
    sources=("J. Delay, P. Deniker and J. M. Harl, Utilisation en thérapeutique psychiatrique d'une phénothiazine "
             "d'action centrale élective (4560 RP), Annales médico-psychologiques 110 (1952) 112-117",
             "S. Leucht et al., Antipsychotic drugs versus placebo for relapse prevention in schizophrenia: a "
             "systematic review and meta-analysis, Lancet 379 (2012) 2063-2071",
             "S. Leucht et al., Sixty years of placebo-controlled antipsychotic drug trials in acute schizophrenia, "
             "American Journal of Psychiatry 174 (2017) 927-942"),
    checked="2026-11-16",
))

add(Finding(
    key="strong_prior_hallucinations", part=41, title=r"Hallucinations as strong priors",
    claim="People who hear voices weight prior expectations more heavily, and so are more prone to hallucinations "
          "conditioned in the laboratory.",
    original=Study("Powers, Mathys and Corlett", 2017, n="four groups: voice hearers and non-hearers, with and "
                   "without a psychotic diagnosis", design="tones at threshold paired with a light, then made rarer",
                   found="voice hearers reported more tones that were not there, and fitted models gave their priors "
                   "more weight"),
    status="contested",
    record=(Study("Kafadar and colleagues", 2022, design="the same task, repeated over time",
                  found="the effect tracked current hallucination severity"),),
    note="An influential account with few independent tests; critics ask whether precision models make predictions "
         "that other accounts do not.",
    sources=("A. R. Powers, C. Mathys and P. R. Corlett, Pavlovian conditioning-induced hallucinations result from "
             "overweighting of perceptual priors, Science 357 (2017) 596-600",
             "E. Kafadar et al., Conditioned hallucinations and prior overweighting are state-sensitive markers of "
             "hallucination susceptibility, Biological Psychiatry 92 (2022) 772-780",
             "P. Sterzer et al., The predictive coding account of psychosis, Biological Psychiatry 84 (2018) "
             "634-643"),
    checked="2026-11-16",
))

add(Finding(
    key="rat_park", part=41, title=r"Rat Park",
    claim="Rats housed in a large, social, enriched colony drink far less morphine than rats housed alone.",
    original=Study("Alexander, Coambs and Hadaway", 1978, n="rats", design="isolated cages against a large "
                   "colony, with morphine solution available", found="colony rats drank much less morphine"),
    status="contested",
    record=(Study("Petrie", 1996, n="rats", design="a replication of the housing comparison",
                  found="housing made little difference"),),
    note="Enrichment and social housing often reduce drug-taking in later animal studies, but not always; Rat Park "
         "itself is more often told than tested.",
    sources=("B. K. Alexander, R. B. Coambs and P. F. Hadaway, The effect of housing and gender on morphine "
             "self-administration in rats, Psychopharmacology 58 (1978) 175-179",
             "B. F. Petrie, Environment is not the most important variable in determining oral morphine consumption "
             "in Wistar rats, Psychological Reports 78 (1996) 391-400"),
    checked="2026-11-16",
))

add(Finding(
    key="contingency_management", part=41, title=r"Contingency management",
    claim="Paying people, in vouchers or prizes, for drug-free urine samples increases abstinence during "
          "treatment.",
    original=Study("Higgins and colleagues", 1991, n="cocaine users in outpatient treatment",
                   design="vouchers for cocaine-free samples against standard counselling",
                   found="more patients stayed in treatment and stayed abstinent"),
    status="replicated",
    record=(Study("Prendergast and colleagues (meta-analysis)", 2006, design="trials of contingency management",
                  found="a moderate effect on abstinence during treatment"),),
    note="Operant conditioning that works; effects fade after the incentives stop.",
    sources=("S. T. Higgins et al., A behavioral approach to achieving initial cocaine abstinence, American Journal "
             "of Psychiatry 148 (1991) 1218-1224",
             "M. Prendergast et al., Contingency management for treatment of substance use disorders: a "
             "meta-analysis, Addiction 101 (2006) 1546-1560"),
    checked="2026-11-16",
))

add(Finding(
    key="vaccines_autism", part=41, title=r"Vaccines and autism",
    claim="The measles, mumps and rubella vaccine causes autism.",
    original=Study("Wakefield and colleagues", 1998, n="12 children", design="a case series",
                   found="bowel disease and regression said to follow vaccination"),
    status="retracted",
    record=(Study("The Lancet's retraction", 2010, found="the paper withdrawn after findings of misconduct"),
            Study("Hviid and colleagues", 2019, n="657,461 Danish children", design="a national cohort",
                  found="no increase in autism after vaccination")),
    note="Retracted for misconduct; no association in studies of millions of children; vaccination fell and measles "
         "returned.",
    sources=("A. J. Wakefield et al., Ileal-lymphoid-nodular hyperplasia, non-specific colitis, and pervasive "
             "developmental disorder in children, Lancet 351 (1998) 637-641 (retracted, 2010)",
             "A. Hviid et al., Measles, mumps, rubella vaccination and autism: a nationwide cohort study, Annals of "
             "Internal Medicine 170 (2019) 513-520"),
    checked="2026-11-16",
))

add(Finding(
    key="facilitated_communication", part=41, title=r"Facilitated communication",
    claim="Non-speaking autistic people can communicate fluent thoughts by typing with a facilitator steadying "
          "their hand.",
    original=Study("Biklen", 1990, design="observations of facilitated typing", found="fluent messages reported"),
    status="failed",
    record=(Study("Wheeler and colleagues", 1993, design="facilitator and typist shown different pictures",
                  found="the messages matched what the facilitator saw"),
            Study("Jacobson, Mulick and Schwartz (review)", 1995, design="controlled tests",
                  found="the messages came from the facilitators")),
    note="The ideomotor effect: facilitators moved the hands without knowing it; false allegations of abuse followed.",
    sources=("D. Biklen, Communication unbound: autism and praxis, Harvard Educational Review 60 (1990) 291-314",
             "D. L. Wheeler et al., An experimental assessment of facilitated communication, Mental Retardation 31 "
             "(1993) 49-60",
             "J. W. Jacobson, J. A. Mulick and A. A. Schwartz, A history of facilitated communication: science, "
             "pseudoscience, and antiscience, American Psychologist 50 (1995) 750-765"),
    checked="2026-11-16",
))

add(Finding(
    key="adhd_stimulants", part=41, title=r"Stimulants for ADHD",
    claim="Stimulant medication reduces the symptoms of ADHD in children more than behavioural treatment alone.",
    original=Study("MTA Cooperative Group", 1999, n="579 children", design="medication, behavioural treatment, both, "
                   "or community care, for 14 months", found="medication management reduced symptoms most"),
    status="replicated, smaller",
    record=(Study("Jensen and colleagues", 2007, design="the same children at three years",
                  found="the groups no longer differed"),
            Study("Cortese and colleagues (network meta-analysis)", 2018, design="short-term trials",
                  found="stimulants reduced symptoms in the short term")),
    note="Short-term benefit replicates; the advantage faded in long-term follow-up of the largest trial.",
    sources=("MTA Cooperative Group, A 14-month randomized clinical trial of treatment strategies for "
             "attention-deficit/hyperactivity disorder, Archives of General Psychiatry 56 (1999) 1073-1086",
             "P. S. Jensen et al., 3-year follow-up of the NIMH MTA study, Journal of the American Academy of Child "
             "and Adolescent Psychiatry 46 (2007) 989-1002",
             "S. Cortese et al., Comparative efficacy and tolerability of medications for attention-deficit "
             "hyperactivity disorder in children, adolescents, and adults, Lancet Psychiatry 5 (2018) 727-738"),
    checked="2026-11-16",
))

shown(41, r"Gregory (1970)", "the hollow mask as a demonstration of perception as inference")
shown(41, r"Rosenthal (1963)", "the Genain quadruplets, a case study told as history")
shown(41, r"Seeman et al.\ (1976); \ Creese, \ Burt \& Snyder (1976)", "a pharmacological correlation; the "
      "antipsychotic row carries the evidence")
shown(41, r"Howes \& Kapur (2009)", "a theory, described")
shown(41, r"Kapur (2003)", "a theory, run on Psyche")
shown(41, r"Sullivan, \ Kendler \& Neale (2003); \ Trubetskoy et al.\ (2022); \ Sekar et al.\ (2016)",
      "a twin meta-analysis, a genome-wide association study and a genetic mechanism, quoted; Part 9 entered "
      "heritability and the candidate-gene record")
shown(41, r"Panlilio et al.\ (2007)", "a test of Redish's model in rats, described as the model's failed prediction")
shown(41, r"Faraone \& Larsson (2019)", "a review of twin studies, quoted for its estimate")
shown(41, r"Layton et al.\ (2018)", "a natural experiment from insurance records, described")
shown(41, r"Marconi et al.\ (2016)", "an observational meta-analysis, quoted; whether cannabis causes psychosis is "
      "debated")
shown(41, r"Fromm-Reichmann (1948)", "a theory that did harm, told as history")
shown(41, r"Robinson \& Berridge (1993)", "a theory, recalled from Part 28")
shown(41, r"Redish (2004)", "a model, run on Psyche")
shown(41, r"Robins (1974)", "a follow-up of a cohort, described; it has not been repeated in a comparable cohort")
shown(41, r"Kanner (1943); \ Asperger (1944)", "the first descriptions, told as history")
shown(41, r"Pellicano \& Burr (2012)", "a theory, run on Psyche")
shown(41, r"CDC ADDM (2023)", "surveillance figures, quoted")

# --- Part 42: Does Therapy Work? --------------------------------------------------------------------------------------

add(Finding(
    key="psychotherapy_vs_none", part=42, title=r"Psychotherapy against no treatment",
    claim="People who receive psychotherapy end better off than comparable people who receive none.",
    original=Study("Smith and Glass (meta-analysis)", 1977, n="375 controlled studies",
                   design="every outcome expressed as a standardized difference", found="an average effect of 0.68"),
    status="replicated",
    record=(Study("Cuijpers and colleagues (meta-analysis)", 2019, design="trials of psychotherapy for adult "
                  "depression", found="clear benefits over control conditions, smaller in the best trials"),),
    note="The answer to Eysenck's challenge; how large the benefit is depends on the control condition and the trial's "
         "quality.",
    sources=("M. L. Smith and G. V. Glass, Meta-analysis of psychotherapy outcome studies, American Psychologist 32 "
             "(1977) 752-760",
             "H. J. Eysenck, The effects of psychotherapy: an evaluation, Journal of Consulting Psychology 16 (1952) "
             "319-324",
             "P. Cuijpers et al., Was Eysenck right after all? A reassessment of the effects of psychotherapy for "
             "adult depression, Epidemiology and Psychiatric Sciences 28 (2019) 21-30"),
    checked="2026-11-16",
))

add(Finding(
    key="published_effect_size", part=42, title=r"The published size of therapy's effect",
    claim="Psychotherapy for adult depression has a large effect, near g = 0.7 against control conditions, as the "
          "whole published literature suggests.",
    original=Study("Cuijpers and colleagues (all trials)", 2019, design="every randomized trial against a control",
                   found="an average near 0.7"),
    status="replicated, smaller",
    record=(Study("Cuijpers and colleagues (low risk of bias)", 2019, design="trials at low risk of bias, without "
                  "waiting-list controls, adjusted for publication bias", found="considerably smaller"),),
    note="Real, but smaller once waiting lists, weak trials and unpublished results are accounted for; Driessen and "
         "colleagues (2015) found a quarter of funded trials unpublished, and the effect smaller once they were added.",
    sources=("E. Driessen et al., Does publication bias inflate the apparent efficacy of psychological treatment for "
             "major depressive disorder? PLoS ONE 10 (2015) e0137864",
             "P. Cuijpers et al., Was Eysenck right after all? Epidemiology and Psychiatric Sciences 28 (2019) 21-30"),
    checked="2026-11-16",
))

add(Finding(
    key="dodo_equivalence", part=42, title=r"The dodo bird verdict",
    claim="All bona fide psychotherapies are about equally effective.",
    original=Study("Luborsky, Singer and Luborsky", 1975, design="a review of comparisons between therapies",
                   found="\"everyone has won and all must have prizes\""),
    status="contested",
    record=(Study("Wampold and colleagues (meta-analysis)", 1997, design="direct comparisons of bona fide therapies",
                  found="differences near zero"),
            Study("Tolin (meta-analysis)", 2010, design="cognitive behavioural therapy against other therapies",
                  found="a small advantage for anxiety and depression")),
    note="Near-equivalence on average for many conditions; specific ingredients matter for some, such as exposure "
         "for anxiety.",
    sources=("L. Luborsky, B. Singer and L. Luborsky, Comparative studies of psychotherapies: is it true that "
             "\"everyone has won and all must have prizes\"? Archives of General Psychiatry 32 (1975) 995-1008",
             "B. E. Wampold et al., A meta-analysis of outcome studies comparing bona fide psychotherapies, "
             "Psychological Bulletin 122 (1997) 203-215",
             "D. F. Tolin, Is cognitive-behavioral therapy more effective than other therapies? Clinical Psychology "
             "Review 30 (2010) 710-720"),
    checked="2026-11-16",
))

add(Finding(
    key="alliance_outcome", part=42, title=r"The alliance and outcome",
    claim="The quality of the working alliance between client and therapist correlates with how well therapy goes.",
    original=Study("Horvath and Symonds (meta-analysis)", 1991, design="studies relating alliance to outcome",
                   found="a correlation near 0.26"),
    status="replicated",
    record=(Study("Flückiger and colleagues (meta-analysis)", 2018, n="295 studies", found="a correlation near "
                  "0.28"),),
    note="The correlation replicates; whether the alliance causes improvement, or early improvement builds the "
         "alliance, is contested.",
    sources=("A. O. Horvath and B. D. Symonds, Relation between working alliance and outcome in psychotherapy: a "
             "meta-analysis, Journal of Counseling Psychology 38 (1991) 139-149",
             "C. Flückiger et al., The alliance in adult psychotherapy: a meta-analytic synthesis, Psychotherapy 55 "
             "(2018) 316-340"),
    checked="2026-11-16",
))

add(Finding(
    key="dbt_self_harm", part=42, title=r"Dialectical behaviour therapy and self-harm",
    claim="Dialectical behaviour therapy reduces self-harm in people with borderline personality disorder.",
    original=Study("Linehan and colleagues", 1991, n="44 women", design="DBT against treatment as usual for a year",
                   found="fewer and less severe acts of self-harm"),
    status="replicated",
    record=(Study("Linehan and colleagues", 2006, n="101 women", design="DBT against treatment by community experts",
                  found="about half the rate of suicide attempts"),
            Study("DeCou, Comtois and Landes (meta-analysis)", 2019, found="a small reduction in self-directed "
                  "violence")),
    note="Replicated, with smaller effects in later and independent trials.",
    sources=("M. M. Linehan et al., Cognitive-behavioral treatment of chronically parasuicidal borderline patients, "
             "Archives of General Psychiatry 48 (1991) 1060-1064",
             "M. M. Linehan et al., Two-year randomized controlled trial and follow-up of dialectical behavior "
             "therapy, Archives of General Psychiatry 63 (2006) 757-766",
             "C. R. DeCou, K. A. Comtois and S. J. Landes, Dialectical behavior therapy is effective for the treatment "
             "of suicidal behavior: a meta-analysis, Behavior Therapy 50 (2019) 60-72"),
    checked="2026-11-16",
))

add(Finding(
    key="debriefing", part=42, title=r"Debriefing after trauma",
    claim="A single session of psychological debriefing soon after a trauma prevents post-traumatic stress.",
    original=Study("Mitchell", 1983, design="critical incident stress debriefing for emergency workers",
                   found="proposed and widely adopted on clinical experience"),
    status="failed",
    record=(Study("Rose, Bisson, Churchill and Wessely (Cochrane review)", 2002, design="randomized trials",
                  found="no prevention of PTSD; some trials found more symptoms"),
            Study("Mayou, Ehlers and Hobbs", 2000, design="road-accident victims followed for three years",
                  found="those debriefed did worse")),
    note="Possibly harmful; guidelines advise against routine single-session debriefing.",
    sources=("J. T. Mitchell, When disaster strikes: the critical incident stress debriefing process, Journal of "
             "Emergency Medical Services 8 (1983) 36-39",
             "S. Rose, J. Bisson, R. Churchill and S. Wessely, Psychological debriefing for preventing post traumatic "
             "stress disorder, Cochrane Database of Systematic Reviews (2002) CD000560",
             "R. A. Mayou, A. Ehlers and M. Hobbs, Psychological debriefing for road traffic accident victims: "
             "three-year follow-up, British Journal of Psychiatry 176 (2000) 589-593"),
    checked="2026-11-16",
))

add(Finding(
    key="scared_straight", part=42, title=r"Scared Straight",
    claim="Taking young offenders to visit prisons, to be confronted by inmates, deters them from crime.",
    original=Study("Scared Straight!, the programme and the documentary", 1978,
                   found="dramatic claims of success"),
    status="failed",
    record=(Study("Petrosino and colleagues (Campbell review)", 2013, design="randomized trials",
                  found="more offending among those who took part"),),
    note="Harmful: the programmes increased offending.",
    sources=("A. Petrosino et al., 'Scared Straight' and other juvenile awareness programs for preventing juvenile "
             "delinquency, Campbell Systematic Reviews 9 (2013)",
             "S. O. Lilienfeld, Psychological treatments that cause harm, Perspectives on Psychological Science 2 "
             "(2007) 53-70"),
    checked="2026-11-16",
))

shown(42, r"Eysenck (1952)", "the challenge, told as history; the row on therapy against no treatment answers it")
shown(42, r"Driessen et al.\ (2015); \ Cuijpers et al.\ (2019)", "the evidence behind the row on the published size of "
      "therapy's effect")
shown(42, r"Hollon et al.\ (2005)", "a single relapse trial, described with its limits")
shown(42, r"Turner et al.\ (2008)", "the registered and published record of antidepressant trials, described as the "
      "file drawer at work")
shown(42, r"Moniz (1936)", "the history of lobotomy, told as history")
shown(42, r"Cerletti \& Bini (1938)", "the history of ECT, told as history")
shown(42, r"Howard et al.\ (1986)", "a summary of the dose-response curve, quoted and drawn")

# --- Part 43: The Replication ----------------------------------------------------------------------------------------

add(Finding(
    key="registered_reports", part=43, title=r"Registered reports and positive results",
    claim="Studies accepted for publication before their results are known report positive results far less often "
          "than standard articles do.",
    original=Study("Allen and Mehler", 2019, design="hypotheses tested in published registered reports",
                   found="most were not supported, against a large majority supported in the standard literature"),
    status="replicated",
    record=(Study("Scheel, Schijen and Lakens", 2021, design="hypothesis tests in psychology's registered reports "
                  "and a random sample of standard articles", found="44% positive against 96%"),),
    note="The gap is what publication bias and flexible analysis predict; registered reports may also test riskier "
         "hypotheses.",
    sources=("C. Allen and D. M. A. Mehler, Open science challenges, benefits and tips in early career and beyond, "
             "PLoS Biology 17 (2019) e3000246",
             "A. M. Scheel, M. R. M. J. Schijen and D. Lakens, An excess of positive results: comparing the standard "
             "psychology literature with registered reports, Advances in Methods and Practices in Psychological "
             "Science 4 (2021)",
             "C. D. Chambers and L. Tzavella, The past, present and future of Registered Reports, Nature Human "
             "Behaviour 6 (2022) 29-42"),
    checked="2026-11-16",
))

add(Finding(
    key="hidden_moderators", part=43, title=r"Hidden moderators",
    claim="Replications often fail because of hidden moderators: effects depend strongly on the setting and the "
          "sample.",
    original=Study("Van Bavel and colleagues", 2016, design="the Reproducibility Project's 100 studies, rated for "
                   "how sensitive to context their topics were", found="more context-sensitive effects replicated "
                   "less often"),
    status="contested",
    record=(Study("Klein and colleagues (Many Labs 2)", 2018, n="28 effects, about 15,000 people in 36 countries",
                  found="little variation across samples and settings for most effects"),
            Study("Olsson-Collentine, Wicherts and van Assen", 2020, design="heterogeneity across direct "
                  "replications", found="mostly small, and largest where effects were large")),
    note="Some effects vary with setting, but for most tested effects variation across labs is small; a failed "
         "replication is rarely explained by place alone.",
    sources=("J. J. Van Bavel, P. Mende-Siedlecki, W. J. Brady and D. A. Reinero, Contextual sensitivity in "
             "scientific reproducibility, Proceedings of the National Academy of Sciences 113 (2016) 6454-6459",
             "R. A. Klein et al., Many Labs 2: investigating variation in replicability across samples and settings, "
             "Advances in Methods and Practices in Psychological Science 1 (2018) 443-490",
             "A. Olsson-Collentine, J. M. Wicherts and M. A. L. M. van Assen, Heterogeneity in direct replications in "
             "psychology and its association with effect size, Psychological Bulletin 146 (2020) 922-940"),
    checked="2026-11-16",
))

shown(43, r"Brandt et al.\ (2014); \ Zwaan et al.\ (2018)", "methods papers on how to replicate, described")
shown(43, r"Nosek \& Errington (2020); \ Van Bavel et al.\ (2016)", "a definition of replication, and the moderator "
      "argument whose record is the hidden-moderators row")
shown(43, r"Simonsohn (2015)", "a method, computed")
shown(43, r"Verhagen \& Wagenmakers (2014)", "a method, computed")

# --- Part 44: Latent Variables ---------------------------------------------------------------------------------------

add(Finding(
    key="glucose_self_control", part=44, title=r"Glucose as the mediator of self-control",
    claim="Self-control draws on blood glucose: depletion lowers it, and a sugary drink restores self-control.",
    original=Study("Gailliot and colleagues", 2007, design="mediation of depletion by measured blood glucose, and "
                   "glucose drinks", found="glucose fell after self-control and a sugary drink restored performance"),
    status="failed",
    record=(Study("Lange and Eggert", 2014, design="a preregistered test of a glucose drink",
                  found="no effect on self-control"),
            Study("Vadillo, Gold and Osman (meta-analysis)", 2016, design="the glucose literature",
                  found="signs of publication bias; little evidence once it is accounted for")),
    note="A mediator chosen from a correlation failed when manipulated; the parent effect, ego depletion, failed "
         "too (Part 28).",
    sources=("M. T. Gailliot et al., Self-control relies on glucose as a limited energy source: willpower is more "
             "than a metaphor, Journal of Personality and Social Psychology 92 (2007) 325-336",
             "F. Lange and F. Eggert, Sweet delusion: glucose drinks fail to counteract ego depletion, Appetite 75 "
             "(2014) 54-63",
             "M. A. Vadillo, N. Gold and M. Osman, The bitter truth about sugar and willpower, Psychological Science "
             "27 (2016) 1207-1214"),
    checked="2026-11-16",
))

add(Finding(
    key="factor_network_equivalence", part=44, title=r"Factors and networks fit the same data",
    claim="A latent-factor model and a network model of direct interactions can imply exactly the same distribution "
          "of observed responses.",
    original=Study("Kruis and Maris", 2016, design="a mathematical proof for binary data",
                   found="the Ising network, a latent-variable model and a common-cause model are equivalent"),
    status="replicated",
    record=(Study("Marsman and colleagues", 2018, design="the network and item-response models related formally",
                  found="the equivalence holds in general for these model families"),),
    note="A theorem, not an experiment: fit cannot decide between a hidden cause and a system of mutual causes; "
         "interventions and time can.",
    sources=("J. Kruis and G. Maris, Three representations of the Ising model, Scientific Reports 6 (2016) 34175",
             "M. Marsman et al., An introduction to network psychometrics: relating Ising network models to item "
             "response theory models, Multivariate Behavioral Research 53 (2018) 15-35"),
    checked="2026-11-16",
))

add(Finding(
    key="fit_cutoffs", part=44, title=r"Universal cut-offs for model fit",
    claim="Fixed cut-offs for fit indices, such as CFI of at least 0.95 and RMSEA of at most 0.06, separate good "
          "models from bad ones in general.",
    original=Study("Hu and Bentler", 1999, design="simulations of a few model types",
                   found="cut-offs that balanced the errors in those conditions"),
    status="failed",
    record=(Study("Marsh, Hau and Wen", 2004, design="a critique with simulations", found="the cut-offs do not "
                  "generalize beyond the conditions studied"),
            Study("McNeish and Wolf", 2023, design="dynamic fit-index cut-offs", found="the right cut-off depends on "
                  "the model, the loadings and the sample, and is often far from the conventional one")),
    note="Useful in the conditions they came from; as general rules, misleading.",
    sources=("L. Hu and P. M. Bentler, Cutoff criteria for fit indexes in covariance structure analysis, Structural "
             "Equation Modeling 6 (1999) 1-55",
             "H. W. Marsh, K.-T. Hau and Z. Wen, In search of golden rules, Structural Equation Modeling 11 (2004) "
             "320-341",
             "D. McNeish and M. G. Wolf, Dynamic fit index cutoffs for confirmatory factor analysis models, "
             "Psychological Methods 28 (2023) 61-88"),
    checked="2026-11-16",
))

shown(44, r"Wright (1921); \ Jöreskog (1969)", "the origins of path analysis and confirmatory factor analysis, told as "
                                                  "history and derived")
shown(44, r"Holzinger \& Swineford (1939)", "a classic dataset, fitted and checked against lavaan")
shown(44, r"Baron \& Kenny (1986)", "a method, described with its critique")
shown(44, r"Bullock, Green \& Ha (2010)", "a methods critique, described")
shown(44, r"MacCallum et al. (1993)", "a methods result on equivalent models, described")
shown(44, r"Meredith (1993)", "the invariance ladder, described and computed")
shown(44, r"Hamaker, Kuiper \& Grasman (2015)", "a methods result, reproduced in simulation")
shown(44, r"Borsboom \& Cramer (2013)", "a theory of disorder, described (Part 39 shows its network)")
shown(44, r"Spirtes, Glymour \& Scheines (2000)", "a method, described")
shown(44, r"Muthén \& Asparouhov (2012); McNeish \& Wolf (2023)", "methods, described")

# --- Part 45: Item Response Theory -----------------------------------------------------------------------------------

add(Finding(
    key="cat_efficiency", part=45, title=r"Adaptive tests need fewer items",
    claim="An adaptive test reaches the precision of a fixed test with far fewer items, often about half.",
    original=Study("Weiss", 1982, design="computerized adaptive tests of ability compared with conventional tests, "
                   "in simulation and live testing", found="equal or better precision with substantially fewer items"),
    status="replicated",
    record=(Study("Wainer and colleagues (review)", 2000, design="the adaptive testing programmes of the 1980s and "
                  "1990s, collected in Computerized Adaptive Testing: A Primer",
                  found="large savings in test length at equal precision; item exposure and security as the costs"),
            Study("Cella and colleagues (PROMIS)", 2010, design="adaptive tests of patient-reported symptoms against "
                  "the full item banks", found="close agreement with the full banks from a handful of items")),
    note="The saving depends on the bank: items spread across the abilities being measured, and well calibrated. "
         "The first items are given to everyone, so exposure must be controlled.",
    sources=("D. J. Weiss, Improving measurement quality and efficiency with adaptive testing, Applied "
             "Psychological Measurement 6 (1982) 473-492",
             "H. Wainer (ed.), Computerized Adaptive Testing: A Primer (2nd edition, Erlbaum, 2000)",
             "D. Cella et al., The Patient-Reported Outcomes Measurement Information System (PROMIS) developed and "
             "tested its first wave of adult self-reported health outcome item banks: 2005-2008, Journal of Clinical "
             "Epidemiology 63 (2010) 1179-1194"),
    checked="2026-11-16",
))

add(Finding(
    key="deep_knowledge_tracing", part=45, title=r"Deep knowledge tracing's large gains",
    claim="A recurrent neural network predicts students' answers far better than Bayesian knowledge tracing.",
    original=Study("Piech and colleagues", 2015, design="deep knowledge tracing on tutoring-system logs",
                   found="an area under the curve near 0.86, against 0.67 for Bayesian knowledge tracing"),
    status="replicated, smaller",
    record=(Study("Khajah, Lindsey and Mozer", 2016, design="Bayesian knowledge tracing extended with forgetting, "
                  "student abilities and skill discovery", found="matched deep knowledge tracing on the same data"),
            Study("Xiong and colleagues", 2016, design="the benchmark data re-examined",
                  found="duplicated records had inflated the gain; much smaller once removed")),
    note="Neural models do predict somewhat better on large logs, but much of the first gap came from a weak baseline "
         "and a data artefact; the simple model's parameters are also interpretable.",
    sources=("C. Piech et al., Deep knowledge tracing, Advances in Neural Information Processing Systems 28 (2015)",
             "M. Khajah, R. V. Lindsey and M. C. Mozer, How deep is knowledge tracing?, Proceedings of Educational "
             "Data Mining (2016)",
             "X. Xiong, S. Zhao, E. G. Van Inwegen and J. E. Beck, Going deeper with deep knowledge tracing, "
             "Proceedings of Educational Data Mining (2016)"),
    checked="2026-11-16",
))
shown(45, r"Rasch (1960)", "the origin of the model, told as history")
shown(45, r"Lord \& Novick (1968); \ Lord (1980)", "the two- and three-parameter models, described")
shown(45, r"Holland \& Thayer (1988)", "a method, computed")
shown(45, r"van der Linden (2007)", "a model, described")
