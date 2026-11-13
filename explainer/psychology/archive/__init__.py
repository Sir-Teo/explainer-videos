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
           "LIT_2011", "MITCHELL_2021", "STEVENS_1946", "FORER_1949", "JOHANSSON_2005", "CREDE_2017", "HEDGE_2018",
           "FLAKE_FRIED_2020", "BEM_2011", "COHEN_1962", "SIMMONS_2011", "OSC_2015", "MANY_LABS", "CAMERER_2018",
           "SCHEEL_2021", "LEVELT_2012", "DREBER_2015"]


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

# ---------------------------------------------------------------------------
# Part 3
# ---------------------------------------------------------------------------
STEVENS_1946 = Dataset(
    key="stevens_1946",
    title="The committee that could not agree whether sensation can be measured, and Stevens's four scales",
    source="S. S. Stevens, On the theory of scales of measurement, Science 103 (1946) 677-680; its account of the "
           "British Association's committee (appointed 1932; interim report 1938; final report 1940, 'Quantitative "
           "estimates of sensory events')",
    cite=r"Stevens (1946)",
    checked="the opening section and Table 1 read from a scan of the article, 2026-11-13; the committee's own "
            "reports were not read",
    licence="facts and a short quotation",
    data={
        "appointed": 1932, "interim_report": 1938, "final_report": 1940, "members": 19,
        "sections": ("A, Mathematical and Physical Sciences", "J, Psychology"),
        "question": "the possibility of quantitative estimates of sensory events",
        "example": "the sone scale of loudness (Stevens and Davis, 1938)",
        "quote": "any law purporting to express a quantitative relation between sensation intensity and stimulus "
                 "intensity is not merely false but is in fact meaningless unless and until a meaning can be given "
                 "to the concept of addition as applied to sensation",
        "quote_by": "one member, in the final report (as quoted by Stevens)",
        "definition": "the assignment of numerals to objects or events according to rules",
        # scale -> (what must be determined, the transformations that leave the scale's form unchanged,
        #           the statistics that keep their meaning; each scale also keeps those above it)
        "scales": {
            "nominal": ("equality", "any one-to-one relabelling", "number of cases, mode"),
            "ordinal": ("greater or less", "any increasing function", "median, percentiles"),
            "interval": ("equality of differences", "x' = ax + b", "mean, standard deviation, correlation"),
            "ratio": ("equality of ratios", "x' = ax", "coefficient of variation"),
        },
    },
)

FORER_1949 = Dataset(
    key="forer_1949",
    title="Forer's classroom demonstration: one personality sketch for everyone",
    source="B. R. Forer, The fallacy of personal validation: a classroom demonstration of gullibility, Journal of "
           "Abnormal and Social Psychology 44 (1949) 118-123; as described by D. H. Dickson and I. W. Kelly, "
           "Psychological Reports 57 (1985) 367-382",
    cite=r"Forer (1949)",
    checked="the design and results read from Dickson and Kelly's review (39 students; ratings from 0 to 5; mean "
            "given as 4.3; nobody below 2, five below 4), 2026-11-13; the mean to two places, 4.26, and the "
            "statements are as reproduced in secondary sources and were not read in the 1949 article",
    licence="facts and short quotations",
    data={
        "n": 39, "scale": (0, 5), "mean": 4.26, "below_4": 5, "lowest": 2, "statements": 13,
        "test": "the Diagnostic Interest Blank",
        "origin": "taken largely from a newsstand astrology book",
        # six of the thirteen statements
        "sample": (
            "You have a great need for other people to like and admire you.",
            "You have a tendency to be critical of yourself.",
            "You have a great deal of unused capacity which you have not turned to your advantage.",
            "Disciplined and self-controlled outside, you tend to be worrisome and insecure inside.",
            "At times you have serious doubts as to whether you have made the right decision or done the right "
            "thing.",
            "At times you are extroverted, affable, sociable, while at other times you are introverted, wary, "
            "reserved.",
        ),
    },
)

JOHANSSON_2005 = Dataset(
    key="johansson_2005",
    title="Choice blindness: people explain a choice they did not make",
    source="P. Johansson, L. Hall, S. Sikstrom and A. Olsson, Failure to detect mismatches between intention and "
           "outcome in a simple decision task, Science 310 (2005) 116-119; summarized by its first author in "
           "P. Johansson, Choice Blindness (doctoral thesis, Lund University, 2006)",
    cite=r"Johansson et al.\ (2005)",
    checked="the author's summary of the paper read from the thesis (Lund University research portal), 2026-11-13",
    licence="facts only",
    data={
        "n": 120, "trials": 15, "manipulated": 3,
        "detected_at_most": 0.26,  # "counting all forms of detection ... no more than 26% of the manipulated trials"
        "would_have_noticed": 0.84,  # of those who detected nothing, the share sure they would have noticed
        "task": "choose the more attractive of two faces; the photographs are covertly exchanged; explain the choice",
    },
)

CREDE_2017 = Dataset(
    key="crede_2017",
    title="Grit and conscientiousness: a meta-analysis",
    source="M. Crede, M. C. Tynan and P. D. Harms, Much ado about grit: a meta-analytic synthesis of the grit "
           "literature, Journal of Personality and Social Psychology 113 (2017) 492-511",
    cite=r"Cred\'e, Tynan \& Harms (2017)",
    checked="the abstract and the Results read from a copy of the article, 2026-11-13",
    licence="facts only",
    data={
        "samples": 88, "people": 66_807,
        "grit_conscientiousness": {"rho": 0.84, "k": 22, "n": 18_826},  # corrected for unreliability
        "perseverance_conscientiousness": {"rho": 0.83, "k": 8, "n": 4_967},
        "consistency_conscientiousness": {"rho": 0.61, "k": 8, "n": 4_967},
        "grit_academic_performance": {"rho": 0.18, "k": 39, "n": 13_141},
    },
)

HEDGE_2018 = Dataset(
    key="hedge_2018",
    title="The reliability paradox: robust tasks, unreliable individual differences",
    source="C. Hedge, G. Powell and P. Sumner, The reliability paradox: why robust cognitive tasks do not produce "
           "reliable individual differences, Behavior Research Methods 50 (2018) 1166-1186",
    cite=r"Hedge, Powell \& Sumner (2018)",
    checked="the abstract, Method and the text on Table 1 read from the open-access article, 2026-11-13",
    licence="CC BY (summary statistics only are used)",
    data={
        "tasks": ("flanker", "Stroop", "stop-signal", "go/no-go", "Posner cueing", "Navon", "SNARC"),
        "retest_weeks": 3, "n": (50, 62, 42),  # Studies 1 to 3, before a few missed second sessions
        "icc_range": (0.0, 0.82),
        "stroop_rt_cost": (0.60, 0.66),  # Studies 1 and 2
        "flanker_rt_cost": 0.40,  # Study 1 ...
        "flanker_components": (0.74, 0.66),  # ... while congruent and incongruent RTs themselves are reliable
        "flanker_sem_ms": 15,
        "gonogo_commission": 0.76,
        "many_labs_3_stroop_replicated": 1.0,  # Ebersole et al. (2016), as cited there
    },
)

FLAKE_FRIED_2020 = Dataset(
    key="flake_fried_2020",
    title="How measures are reported and altered in published psychology",
    source="J. K. Flake and E. I. Fried, Measurement schmeasurement: questionable measurement practices and how to "
           "avoid them, Advances in Methods and Practices in Psychological Science 3 (2020) 456-465, and the "
           "surveys it reports (Flake, Pek and Hehman 2017; Weidman, Steckler and Tracy 2017; Elson et al. 2014; "
           "Santor, Gregus and Welch 2006)",
    cite=r"Flake \& Fried (2020)",
    checked="read from a copy of the article, 2026-11-13; the surveys it cites were not read",
    licence="facts only",
    data={
        "scales_reviewed": 433,  # a random sample of studies in JPSP, 2014 (Flake, Pek & Hehman 2017)
        "no_source": 0.40, "no_item_count": 0.19, "no_response_scale": 0.09,
        "emotion_instances": 356, "emotion_no_development": 0.69,  # Weidman et al. (2017)
        "crtt_ways": 150, "crtt_publications": 130,  # one aggression task, scored in over 150 ways
        "depression_scales": 280,
    },
)

# ---------------------------------------------------------------------------
# Part 4
# ---------------------------------------------------------------------------
BEM_2011 = Dataset(
    key="bem_2011",
    title="Nine experiments that appeared to show people responding to events that had not yet happened",
    source="D. J. Bem, Feeling the future: experimental evidence for anomalous retroactive influences on cognition "
           "and affect, Journal of Personality and Social Psychology 100 (2011) 407-425; with the replications of "
           "J. Galak, R. A. LeBoeuf, L. D. Nelson and J. P. Simmons, Correcting the past: failures to replicate psi, "
           "the same journal 103 (2012) 933-948, and S. J. Ritchie, R. Wiseman and C. C. French, Failing the future, "
           "PLoS ONE 7 (2012) e33423",
    cite=r"Bem (2011)",
    checked="the three abstracts read (Europe PMC), 2026-11-13; the experiments' procedures are as the abstracts "
            "describe them",
    licence="facts only",
    data={
        "experiments": 9, "participants_more_than": 1000, "mean_d": 0.22, "significant": 8,
        "effects": ("precognitive approach to erotic stimuli and avoidance of negative stimuli", "retroactive priming",
                    "retroactive habituation", "retroactive facilitation of recall"),
        "galak": {"experiments": 7, "n": 3289, "meta_d": 0.04},  # of Bem's Experiments 8 and 9
        "ritchie": {"attempts": 3, "n": 150, "p_one_tailed": 0.83},  # of the recall experiment; preregistered
    },
)

COHEN_1962 = Dataset(
    key="cohen_1962",
    title="The power of a year of published psychology",
    source="J. Cohen, The statistical power of abnormal-social psychological research: a review, Journal of Abnormal "
           "and Social Psychology 65 (1962) 145-153; P. Sedlmeier and G. Gigerenzer, Do studies of statistical power "
           "have an effect on the power of studies?, Psychological Bulletin 105 (1989) 309-316",
    cite=r"Cohen (1962); \ Sedlmeier \& Gigerenzer (1989)",
    checked="the figure for medium effects read from Cohen's own later account (A power primer, 1992), 2026-11-13; "
            "the figures for small and large effects and Sedlmeier and Gigerenzer's are from secondary summaries",
    licence="facts only",
    data={
        "journal_year": 1960, "power_medium": 0.48, "power_small": 0.18, "power_large": 0.83,
        "later_year": 1984, "later_power_medium": 0.37,
        "conclusion": "the power of studies in the same journal had not increased 24 years later",
    },
)

SIMMONS_2011 = Dataset(
    key="simmons_2011",
    title="How undisclosed flexibility raises the false-positive rate",
    source="J. P. Simmons, L. D. Nelson and U. Simonsohn, False-positive psychology: undisclosed flexibility in data "
           "collection and analysis allows presenting anything as significant, Psychological Science 22 (2011) "
           "1359-1366",
    cite=r"Simmons, Nelson \& Simonsohn (2011)",
    checked="the abstract read (Europe PMC), 2026-11-13; the combined figure of 60.7% confirmed from two secondary "
            "accounts; the paper's Table 1 was not read, so the film recomputes the rates and quotes only the total",
    licence="facts only",
    data={
        "nominal": 0.05, "combined": 0.607,
        "flexibilities": ("two dependent variables", "ten more observations per cell after a first look",
                          "a covariate, with or without its interaction", "dropping one of three conditions"),
        "requirements_for_authors": 6, "guidelines_for_reviewers": 4,
    },
)

OSC_2015 = Dataset(
    key="osc_2015",
    title="The Reproducibility Project: Psychology",
    source="Open Science Collaboration, Estimating the reproducibility of psychological science, Science 349 (2015) "
           "aac4716; D. T. Gilbert, G. King, S. Pettigrew and T. D. Wilson, Comment, Science 351 (2016) 1037; "
           "C. J. Anderson et al., Response, Science 351 (2016) 1037",
    cite=r"Open Science Collaboration (2015)",
    checked="the three abstracts read (Europe PMC), 2026-11-13",
    licence="facts only",
    data={
        "studies": 100, "journals": 3, "original_significant": 0.97, "replication_significant": 0.36,
        "original_in_replication_ci": 0.47, "rated_replicated": 0.39, "combined_significant": 0.68,
        "effect_ratio": 0.5,  # "replication effects were half the magnitude of original effects"
        "predictor": "the strength of the original evidence, more than characteristics of the teams",
        "comment": "three statistical errors alleged; 'the data are consistent with the opposite conclusion'",
        "response": "both optimistic and pessimistic conclusions are possible, and neither is yet warranted",
    },
)

MANY_LABS = Dataset(
    key="many_labs",
    title="Many Labs 1 and 2: the same protocols run in many laboratories at once",
    source="R. A. Klein et al., Investigating variation in replicability: a 'Many Labs' replication project, Social "
           "Psychology 45 (2014) 142-152; R. A. Klein et al., Many Labs 2: investigating variation in replicability "
           "across samples and settings, Advances in Methods and Practices in Psychological Science 1 (2018) 443-490",
    cite=r"Klein et al.\ (2014, 2018)",
    checked="the abstract of the first read (Europe PMC); the figures of the second read from its abstract as "
            "reproduced by institutional repositories, 2026-11-13",
    licence="facts only",
    data={
        "ml1": {"effects": 13, "samples": 36, "participants": 6344, "replicated": 10, "weak": 1, "failed": 2},
        "ml2": {"effects": 28, "samples": 125, "participants": 15305, "countries": 36, "replicated": 15,
                "replicated_strict": 14, "median_d_original": 0.60, "median_d_replication": 0.15,
                "smaller_than_original": 21},
        "finding": "replicability depended on the effect, and hardly at all on the sample or the setting",
    },
)

CAMERER_2018 = Dataset(
    key="camerer_2018",
    title="Replications of 21 social-science experiments published in Nature and Science",
    source="C. F. Camerer et al., Evaluating the replicability of social science experiments in Nature and Science "
           "between 2010 and 2015, Nature Human Behaviour 2 (2018) 637-644",
    cite=r"Camerer et al.\ (2018)",
    checked="the abstract read (Europe PMC), 2026-11-13",
    licence="facts only",
    data={"studies": 21, "replicated": 13, "share": 0.62, "effect_ratio": 0.5, "sample_ratio": 5,
          "peers": "peer beliefs of replicability were strongly related to replicability"},
)

SCHEEL_2021 = Dataset(
    key="scheel_2021",
    title="Positive results in the standard literature and in Registered Reports",
    source="A. M. Scheel, M. R. M. J. Schijen and D. Lakens, An excess of positive results: comparing the standard "
           "psychology literature with Registered Reports, Advances in Methods and Practices in Psychological "
           "Science 4 (2021) 1-12",
    cite=r"Scheel, Schijen \& Lakens (2021)",
    checked="the abstract read (Europe PMC, preprint record), 2026-11-13",
    licence="facts only",
    data={"standard_n": 152, "standard_positive": 0.96, "registered_n": 71, "registered_positive": 0.44},
)

LEVELT_2012 = Dataset(
    key="levelt_2012",
    title="The Stapel affair: what three committees found",
    source="Levelt, Noort and Drenth Committees, Flawed Science: the fraudulent research practices of social "
           "psychologist Diederik Stapel (Tilburg, 28 November 2012)",
    cite=r"Levelt, Noort \& Drenth Committees (2012)",
    checked="the count and the committees' conclusions read from university news reports of the final report, "
            "2026-11-13; the report itself was not read",
    licence="facts only",
    data={"publications_with_fraud": 55, "exposed": 2011,
          "culture": "a general culture of careless, selective and uncritical handling of research and data",
          "coauthors": "no co-author or doctoral student was found to have taken part in the fraud"},
)

DREBER_2015 = Dataset(
    key="dreber_2015",
    title="Prediction markets on which studies would replicate",
    source="A. Dreber et al., Using prediction markets to estimate the reproducibility of scientific research, "
           "Proceedings of the National Academy of Sciences 112 (2015) 15343-15347",
    cite=r"Dreber et al.\ (2015)",
    checked="the abstract read (Europe PMC, PMC4687569), 2026-11-13",
    licence="open access (summary statistics)",
    data={"studies": 44, "median_prior": 0.09,
          "finding": "the markets predicted the outcomes of the replications well, and better than a survey of the "
                     "same participants"},
)

ALL = {d.key: d for d in (KANT_1786, HELMHOLTZ_1850, DONDERS_1868, EBBINGHAUS_1885, WOODS_2015, PFUNGST_1907,
                          PEIRCE_JASTROW_1884, ROSENTHAL_FODE_1963, RAUDENBUSH_1984, DE_QUIDT_2018, LIT_2011,
                          MITCHELL_2021, STEVENS_1946, FORER_1949, JOHANSSON_2005, CREDE_2017, HEDGE_2018,
                          FLAKE_FRIED_2020, BEM_2011, COHEN_1962, SIMMONS_2011, OSC_2015, MANY_LABS, CAMERER_2018,
                          SCHEEL_2021, LEVELT_2012, DREBER_2015)}
