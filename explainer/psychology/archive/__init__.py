"""The Archive of *Psychology, Built*: real data, transcribed from the original publication or a named secondary
source, each with its reference (videos/psychology/SYLLABUS.md, §1 "Numbers and claims").

    from explainer.psychology import archive
    archive.EBBINGHAUS_1885.data["saving"]          # the seven savings scores of Ebbinghaus's retention table
    archive.DONDERS_1868.cite                       # the line that goes on screen with it

Every entry is a :class:`Dataset`: what it is, where it comes from, how it was checked and on what date, and
the numbers.  ``SOURCES.md`` beside this file is the human-readable register, with the check that was made for
each entry; ``tests/psychology/test_archive.py`` checks the arithmetic the films rely on.

Nothing here imports manim.
"""

from __future__ import annotations

from dataclasses import dataclass, field

__all__ = ["Dataset", "ALL", "KANT_1786", "HELMHOLTZ_1850", "DONDERS_1868", "EBBINGHAUS_1885", "WOODS_2015",
           "PFUNGST_1907", "PEIRCE_JASTROW_1884", "ROSENTHAL_FODE_1963", "RAUDENBUSH_1984", "DE_QUIDT_2018",
           "LIT_2011", "MITCHELL_2021"]


@dataclass(frozen=True)
class Dataset:
    key: str
    title: str
    source: str  # the full reference
    cite: str  # the short source line shown on screen (TeX)
    checked: str  # how the transcription was checked, and the ISO date
    licence: str
    data: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Part 1
# ---------------------------------------------------------------------------
KANT_1786 = Dataset(
    key="kant_1786",
    title="Kant's three objections to a science of psychology",
    source="I. Kant, Metaphysische Anfangsgruende der Naturwissenschaft (1786), Preface (Akademie edition 4:471); "
           "English by E. B. Bax, Kant's Prolegomena and Metaphysical Foundations of Natural Science (1883), p. 141",
    cite=r"Kant (1786), Preface; \ transl.\ Bax (1883)",
    checked="read against the 1883 translation on Wikisource (page 141), 2026-11-13",
    licence="public domain",
    data={
        "mathematics": "mathematics is inapplicable to the phenomena of the internal sense and its laws",
        "experiment": "the manifold of internal observation is only separated in thought, but cannot be kept "
                      "separate and be connected again at pleasure",
        "observation": "even the observation itself, alters and distorts the state of the object observed",
        "verdict": "a natural description of the soul, but not a science of the soul",
    },
)

HELMHOLTZ_1850 = Dataset(
    key="helmholtz_1850",
    title="Helmholtz's first measurement of the speed of the nerve signal",
    source="H. Helmholtz, Vorlaeufiger Bericht ueber die Fortpflanzungsgeschwindigkeit der Nervenreizung, Archiv "
           "fuer Anatomie, Physiologie und wissenschaftliche Medicin (1850) 71-73, signed 15 January 1850; figures "
           "as translated and reported by H. Schmidgen, Endeavour 26 (2002) 142-148",
    cite=r"Helmholtz (1850); \ Schmidgen (2002)",
    checked="read in Schmidgen (2002), 2026-11-13: nerve lengths, delays, the 25-43 m/s range, the human values "
            "and the later measurements",
    licence="facts from a published article; no data file is redistributed",
    data={
        "length_mm": (50.0, 60.0),  # the nerves of large frogs
        "delay_s": (0.0014, 0.0020),  # the extra time when the stimulus is applied at the far end
        "frog_temp_c": (2.0, 6.0),
        "speed_frog": (25.0, 43.0),  # m/s, the range Schmidgen gives (50 mm / 0.0020 s to 60 mm / 0.0014 s)
        "speed_human_1850": 60.0,  # "circa 60 Meter (180 feet)": toe against sacrum 62.1, finger against neck 61.0
        "brain_time_s": 0.1,  # Helmholtz's estimate of the time "for the processes of perceiving and willing"
        "later": (("Hirsch", 1862, 34.0), ("Donders and de Jaager", 1865, 26.0),
                  ("Helmholtz and Baxt", 1867, 33.9), ("Helmholtz and Baxt, midsummer", 1869, 64.6)),
    },
)

DONDERS_1868 = Dataset(
    key="donders_1868",
    title="Donders' reaction times by the a-, b- and c-methods",
    source="F. C. Donders, Over de snelheid van psychische processen, Onderzoekingen gedaan in het Physiologisch "
           "Laboratorium der Utrechtsche Hoogeschool, Tweede reeks II (1868) 92-120; transl. W. G. Koster, Acta "
           "Psychologica 30 (1969) 412-431; means as given by A. Roelofs, Acta Psychologica 191 (2018) 228-233",
    cite=r"Donders (1868); \ Roelofs (2018)",
    checked="means 201, 284 and 237 ms and the differences 36 and 47 ms confirmed from Roelofs (2018) by search "
            "summary and abstract, 2026-11-13; the paper itself was not retrievable (to be read before the "
            "narrated master)",
    licence="facts from published articles; no data file is redistributed",
    data={
        "task": "speech repetition: the experimenter says a syllable, the subject repeats it",
        "a": 201.0,  # ms: the syllable is known in advance
        "b": 284.0,  # ms: one of five syllables, repeat whichever is said
        "c": 237.0,  # ms: one of five syllables, repeat only the agreed one
        "alternatives": 5,
        "subject": "Donders himself",
        "students": "no b - c difference in the unpublished notebook data of his students (Roelofs 2018)",
    },
)

EBBINGHAUS_1885 = Dataset(
    key="ebbinghaus_1885",
    title="Ebbinghaus's retention table: savings in relearning after seven intervals",
    source="H. Ebbinghaus, Ueber das Gedaechtnis (1885); transl. H. A. Ruger and C. E. Bussenius, Memory: A "
           "Contribution to Experimental Psychology (1913), ch. VII, sections 27-29",
    cite=r"Ebbinghaus (1885), ch.~VII",
    checked="transcribed from the tables of the 1913 translation at psychclassics.yorku.ca (table images of ch. "
            "VII), 2026-11-13",
    licence="public domain",
    data={
        "hours": (0.33, 1.0, 8.8, 24.0, 48.0, 144.0, 744.0),
        "minutes": (20.0, 64.0, 526.0, 1440.0, 2880.0, 8640.0, 44640.0),  # the t of his formula
        "saving": (58.2, 44.2, 35.8, 33.7, 27.8, 25.4, 21.1),  # per cent of the original learning time saved
        "probable_error": (1.0, 1.0, 1.0, 1.2, 1.4, 1.3, 0.8),
        "formula": "b = 100 k / ((log10 t)^c + k), t in minutes, k = 1.84, c = 1.25",
        "k": 1.84,
        "c": 1.25,
        "calculated": (57.0, 46.7, 34.5, 30.4, 28.1, 24.9, 21.2),  # his own column of fitted values
        "syllables_created": 2300,
    },
)

WOODS_2015 = Dataset(
    key="woods_2015",
    title="Simple visual reaction time in a community sample, with calibrated hardware",
    source="D. L. Woods, J. M. Wyma, E. W. Yund, T. J. Herron and B. Reed, Factors influencing the latency of "
           "simple reaction time, Frontiers in Human Neuroscience 9 (2015) 131",
    cite=r"Woods et al.\ (2015)",
    checked="read from the article's abstract (Europe PMC, PMC4374455), 2026-11-13",
    licence="CC BY (summary statistics only are used)",
    data={
        "n": 1469,
        "ages": (18, 65),
        "mean_raw_ms": 231.0,
        "mean_corrected_ms": 213.0,  # after subtracting measured hardware delays
        "age_slope_ms_per_year": 0.55,
        "detection_ms": 131.0,  # stimulus detection time: simple RT minus movement initiation time
        "galton_ms": 190.0,  # "below 190 ms in young subjects" (Galton, as cited by Woods et al.)
    },
)

# ---------------------------------------------------------------------------
# Part 2
# ---------------------------------------------------------------------------
PFUNGST_1907 = Dataset(
    key="pfungst_1907",
    title="Pfungst's experiments on Clever Hans, and the report of the Hans Commission",
    source="O. Pfungst, Das Pferd des Herrn von Osten (Der Kluge Hans) (1907); transl. C. L. Rahn, Clever Hans (The "
           "Horse of Mr. von Osten): A Contribution to Experimental Animal and Human Psychology (1911), ch. II and "
           "IV and Supplements II and IV",
    cite=r"Pfungst (1907; transl.\ 1911)",
    checked="read from the 1911 translation, Project Gutenberg ebook 33936, 2026-11-13: the counts and percentages "
            "of ch. II, the laboratory tests of ch. IV and the signatures of the report of 12 September 1904",
    licence="public domain",
    data={
        "commission_date": "1904-09-12",
        "commission_members": 13,
        "commission_verdict": "tricks (intentional signs) are out of the question; unintentional signs of the kind "
                              "at present familiar are likewise excluded; worthy of a serious investigation",
        "report_date": "1904-12-09",  # Stumpf's report of Pfungst's experiments
        # reading numerals from cards: was the answer known to the questioner?
        "numerals": {"without_knowledge": {"n": 49, "correct": 0.08}, "with_knowledge": {"n": 42, "correct": 0.98}},
        # words on placards
        "placards": {"without_knowledge": {"n": 12, "correct": 0.0}, "with_knowledge": {"n": 14, "correct": 1.0}},
        # large blinders: could the horse see the questioner while tapping?
        "blinders": {"not_seen": {"n": 35, "correct": 0.06}, "seen": {"n": 56, "correct": 0.89},
                     "undecided": {"n": 11, "correct": 0.18}},
        # distance of the questioner (70 tests): accurate to 3.5 m, none correct beyond 4.5 m
        "distance_m": {"accurate_to": 3.5, "one_third_correct": (4.0, 4.5), "none_beyond": 4.5, "n": 70},
        # Pfungst as the horse: 25 naive people think of a number while he taps
        "laboratory": {"people": 25, "made_the_movement": 23,
                       "size": "seldom as much as one millimetre; one or two in a very few cases"},
        "cue": "a slight forward bend of the questioner as the tapping starts, and a slight upward jerk of the "
               "head when the right count is reached",
    },
)

PEIRCE_JASTROW_1884 = Dataset(
    key="peirce_jastrow_1884",
    title="Peirce and Jastrow's randomized experiment on small differences of pressure",
    source="C. S. Peirce and J. Jastrow, On small differences in sensation, Memoirs of the National Academy of "
           "Sciences 3 (1885) 73-83 (read 17 October 1884)",
    cite=r"Peirce \& Jastrow (1884)",
    checked="read from the text at psychclassics.yorku.ca (Classics in the History of Psychology), 2026-11-13",
    licence="public domain",
    data={
        "randomizer": "a pack of 25 playing cards, 12 red and 13 black or the reverse, shuffled; the colour of each "
                      "card fixed whether the weight was first increased or first decreased",
        "trials_per_pack": 25,
        "trials_per_sitting": 150,
        "confidence_scale": (0, 1, 2, 3),
        "base_pressure": "a kilogram on the pan (a quarter of it on the finger)",
        "differences_per_thousand": (60, 30, 15, 20, 10, 5),
        "blind": "a screen served to prevent the subject from having any indications whatever of the movements "
                 "of the operator",
        "why": "any possible psychological guessing of what change the operator was likely to select was avoided",
    },
)

ROSENTHAL_FODE_1963 = Dataset(
    key="rosenthal_fode_1963",
    title="Rosenthal and Fode's 'maze-bright' and 'maze-dull' rats",
    source="R. Rosenthal and K. L. Fode, The effect of experimenter bias on the performance of the albino rat, "
           "Behavioral Science 8 (1963) 183-189, Table 1",
    cite=r"Rosenthal \& Fode (1963)",
    checked="Table 1 and the Method read from a scan of the article, 2026-11-13",
    licence="facts from a published article; no data file is redistributed",
    data={
        "experimenters": 12,  # six told 'maze-bright', six told 'maze-dull'; labels assigned at random
        "rats_per_experimenter": 5,
        "trials_per_rat_per_day": 10,
        "days": 5,
        "maze": "an elevated T maze; the darker arm was always reinforced",
        "bright": (1.33, 1.60, 2.60, 2.83, 3.26),  # correct responses per rat per day
        "dull": (0.73, 1.10, 2.23, 1.83, 1.83),
        "mean_bright": 2.32,
        "mean_dull": 1.54,
        "t": 4.01,
        "p_one_tailed": 0.01,
    },
)

RAUDENBUSH_1984 = Dataset(
    key="raudenbush_1984",
    title="Teacher expectancy and pupil IQ: 18 experiments, by how long the teacher had known the pupils",
    source="S. W. Raudenbush, Magnitude of teacher expectancy effects on pupil IQ as a function of the credibility "
           "of expectancy induction: a synthesis of findings from 18 experiments, Journal of Educational Psychology "
           "76 (1984) 85-97",
    cite=r"Raudenbush (1984)",
    checked="abstract and Results read from a scan of the article, 2026-11-13",
    licence="facts from a published article; no data file is redistributed",
    data={
        "experiments": 18,
        "effect_no_prior_contact": 0.32,  # mean standardized effect, four experiments
        "n_no_prior_contact": 4,
        "effect_one_week": 0.26,  # three experiments
        "n_one_week": 3,
        "effect_more_than_two_weeks": -0.04,  # eight experiments
        "n_more_than_two_weeks": 8,
    },
)

DE_QUIDT_2018 = Dataset(
    key="de_quidt_2018",
    title="Experimenter demand, measured: deliberately signalling the hypothesis in eleven standard tasks",
    source="J. de Quidt, J. Haushofer and C. Roth, Measuring and bounding experimenter demand, American Economic "
           "Review 108 (2018) 3266-3302 (NBER working paper 23470)",
    cite=r"de Quidt, Haushofer \& Roth (2018)",
    checked="introduction of the working paper read, 2026-11-13; the published abstract gives an average of 0.13 "
            "standard deviations for the weak treatments",
    licence="facts from a published article; no data file is redistributed",
    data={
        "experiments": 7,
        "participants": 19000,  # approximately
        "tasks": 11,
        "strong_demand_sd": (0.25, 1.0),  # 'you will do us a favour if...': positive minus negative, by task
        "weak_demand_sd": (0.1, 0.3),  # 'we expect that participants will...': the range of the bounds
        "weak_demand_mean_sd": 0.13,
    },
)

LIT_2011 = Dataset(
    key="lit_2011",
    title="Handlers' beliefs and the alerts of scent-detection dogs",
    source="L. Lit, J. B. Schweitzer and A. M. Oberbauer, Handler beliefs affect scent detection dog outcomes, "
           "Animal Cognition 14 (2011) 387-394",
    cite=r"Lit, Schweitzer \& Oberbauer (2011)",
    checked="abstract and Methods read from the open-access text (Europe PMC, PMC3078300), 2026-11-13",
    licence="open access (summary statistics only are used)",
    data={
        "teams": 18,  # certified handler and dog teams: 13 drug, 3 explosives, 2 both
        "target_scent_present": 0,  # no search area held any drug or explosive scent
        "incorrect_alerts": 225,
        "manipulation": "handlers were told, falsely, that a piece of paper marked the place of the scent in two of "
                        "the four conditions",
        "finding": "handlers reported more alerts at the marked places; human more than dog influences affected "
                   "where the alerts fell",
    },
)

MITCHELL_2021 = Dataset(
    key="mitchell_2021",
    title="A double-blind drug trial in which most participants could tell their arm",
    source="J. M. Mitchell et al., MDMA-assisted therapy for severe PTSD: a randomized, double-blind, "
           "placebo-controlled phase 3 study, Nature Medicine 27 (2021) 1025-1033",
    cite=r"Mitchell et al.\ (2021)",
    checked="the passage on blinding read from the open-access text (Europe PMC, PMC8205851), 2026-11-13",
    licence="CC BY (summary statistics only are used)",
    data={
        "n": 90,
        "n_drug": 46,
        "n_placebo": 44,
        "placebo_believed_drug_at_least": 7,  # "at least 7 of 44 (15.9%)"
        "drug_believed_placebo_at_least": 2,  # "at least 2 of 46 (4.3%)"
        "note": "blinding was not formally assessed; the figures were gathered when participants were told their "
                "assignment, and the authors call them anecdotal",
    },
)

ALL = {d.key: d for d in (KANT_1786, HELMHOLTZ_1850, DONDERS_1868, EBBINGHAUS_1885, WOODS_2015, PFUNGST_1907,
                          PEIRCE_JASTROW_1884, ROSENTHAL_FODE_1963, RAUDENBUSH_1984, DE_QUIDT_2018, LIT_2011,
                          MITCHELL_2021)}
