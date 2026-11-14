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
           "SCHEEL_2021", "LEVELT_2012", "DREBER_2015", "PROTZKO_2023", "HODGKIN_HUXLEY_1952", "COLE_CURTIS_1939",
           "ADRIAN_1926", "GOLGI_CAJAL_1906", "GIDON_2020", "LOEWI_1921", "HEBB_1949", "BLISS_LOMO_1973", "BI_POO_1998",
           "HARTLINE_RATLIFF_1957", "GEIER_2008", "DEL_CASTILLO_KATZ_1954", "LIU_2012", "TURNER_2008",
           "HARLOW_1868", "BROCA_1861", "DRONKERS_2007", "WERNICKE_1874", "LASHLEY_1929", "PENFIELD_BOLDREY_1937", "HORTON_HOYT_1991",
           "SCOVILLE_MILNER_1957", "NIELSEN_2013", "MAGUIRE_2000", "AZEVEDO_2009", "RAICHLE_2002", "WEISKRANTZ_1974", "MAH_2014", "WIESEL_HUBEL_1963", "MERZENICH_1984", "GAZZANIGA_1978",
           "BENNETT_2009", "HUBEL_WIESEL_1959", "BERGER_1929", "KUTAS_HILLYARD_1980", "OGAWA_1990",
           "LOGOTHETIS_2001", "BOYNTON_1996", "EKLUND_2016", "VUL_2009", "POLDRACK_2006",
           "MAREK_2022", "ELLIOTT_2020", "TANG_2023", "OWEN_2010", "KANWISHER_1997",
           "GANIS_2011", "BARKER_1985",
           "BOUCHARD_1990", "GALTON_1875", "FISHER_1918", "BOUCHARD_MCGUE_1981", "POLDERMAN_2015", "TURKHEIMER_2000",
           "TURKHEIMER_2003", "HAWORTH_2010", "NCD_RISC_2016", "HERITABILITY_TABLE", "CASPI_2003", "BORDER_2019",
           "CHABRIS_2012", "RIETVELD_2013", "LEE_2018", "KONG_2018", "HOWE_2022", "YENGO_2022", "MARTIN_2019",
           "KARAVANI_2019", "BUSS_1989", "HEIJMANS_2008", "WEIR_2002",
           "KLEITMAN_1938", "CZEISLER_1999", "ASERINSKY_1953", "BORBELY_1982", "VAN_DONGEN_2003", "RASCH_2007",
           "HOBSON_1977", "CAPPUCCIO_2010", "SIEGEL_1982", "SOLOMON_CORBIT_1974", "DUNSTER_2018", "TRAUER_2015",
           "XIE_2013", "PHOENIX_1959", "TEIGEN_1994", "ROENNEBERG_2004"]


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

PROTZKO_2023 = Dataset(
    key="protzko_2023",
    title="A claim that reformed practices give highly replicable findings, and its retraction",
    source="J. Protzko et al., High replicability of newly discovered social-behavioural findings is achievable, "
           "Nature Human Behaviour 8 (2024) 311-319 (published online 2023); Retraction Note, Nature Human "
           "Behaviour 8 (2024) 2067 (24 September 2024)",
    cite=r"Protzko et al.\ (2023); \ retraction note (2024)",
    checked="the retraction note as summarized from PubMed Central (PMC11493675) by a web search, 2026-11-13; "
            "neither the article nor the note was read in full",
    licence="facts only",
    data={"published": 2023, "retracted": 2024,
          "reasons": "several measures and analyses had not been preregistered as the article stated, and the "
                     "hypotheses the study was designed to test were misstated",
          "authors": "all authors agreed to the retraction, for the incorrect statements about preregistration"},
)

# ---------------------------------------------------------------------------
# Part 5
# ---------------------------------------------------------------------------
HODGKIN_HUXLEY_1952 = Dataset(
    key="hodgkin_huxley_1952",
    title="Hodgkin and Huxley's model of the squid giant axon, and its computed action potential",
    source="A. L. Hodgkin and A. F. Huxley, A quantitative description of membrane current and its application to "
           "conduction and excitation in nerve, Journal of Physiology 117 (1952) 500-544; A. L. Hodgkin and "
           "A. F. Huxley, Action potentials recorded from inside a nerve fibre, Nature 144 (1939) 710-712; "
           "A. F. Huxley, From overshoot to voltage clamp, Trends in Neurosciences 25 (2002) 553-558",
    cite=r"Hodgkin \& Huxley (1952)",
    checked="the computed speed (18.8 m/s at 18.5 C) from a textbook figure adapted from the 1952 paper (Sterratt "
            "et al., Principles of Computational Modelling in Neuroscience, ch. 3) and the 1939 voltages from "
            "Huxley's retrospective, both through a web search, 2026-11-13; the conductances and rate functions "
            "are the standard ones, as every text prints them; the measured speed (21.2 m/s), the axon's radius "
            "and its axoplasm resistivity are from memory of the paper, which was not read",
    licence="facts and published equations; no data file is redistributed",
    data={
        "g_na": 120.0, "g_k": 36.0, "g_l": 0.3, "c": 1.0,  # mS/cm^2 and uF/cm^2
        "e_na_rel": 115.0, "e_k_rel": -12.0, "e_l_rel": 10.6,  # mV from rest, depolarization positive
        "temp_c": 6.3,  # the temperature the rate constants are given for
        "velocity_computed": 18.8, "velocity_temp_c": 18.5,  # m/s, computed by hand
        "velocity_observed": 21.2,  # m/s (unverified here)
        "radius_um": 238.0, "resistivity_ohm_cm": 35.4,  # the axon of the propagated action potential (unverified)
        "rest_1939_mv": -45.0, "peak_1939_mv": 40.0,  # as Huxley recalls the first intracellular records
        "nobel": 1963,
    },
)

COLE_CURTIS_1939 = Dataset(
    key="cole_curtis_1939",
    title="The membrane's conductance rises during the action potential; its capacitance does not",
    source="K. S. Cole and H. J. Curtis, Electric impedance of the squid giant axon during activity, Journal of "
           "General Physiology 22 (1939) 649-670; the giant axon: J. Z. Young (1936)",
    cite=r"Cole \& Curtis (1939)",
    checked="from the Marine Biological Laboratory's history pages and Cole's National Academy memoir, through a "
            "web search, 2026-11-13; the paper was not read",
    licence="facts only",
    data={"finding": "an increase in membrane conductance without an accompanying change in capacitance",
          "summer": 1938, "giant_axon": 1936},
)

ADRIAN_1926 = Dataset(
    key="adrian_1926",
    title="One sensory fibre: impulses of constant size, more frequent with more stretch",
    source="E. D. Adrian and Y. Zotterman, The impulses produced by sensory nerve-endings. Part II. The response "
           "of a single end-organ, Journal of Physiology 61 (1926) 151-171",
    cite=r"Adrian \& Zotterman (1926)",
    checked="from secondary accounts through a web search, 2026-11-13: the preparation (the nerve to a frog's "
            "sternocutaneous muscle) and the finding; the paper and its records were not read, so no rates are "
            "quoted",
    licence="facts only",
    data={"preparation": "the nerve to the sternocutaneous muscle of a frog",
          "finding": "discrete impulses of similar amplitude and duration; only their frequency changes with "
                     "stretch"},
)

GOLGI_CAJAL_1906 = Dataset(
    key="golgi_cajal_1906",
    title="One net or many cells: Golgi and Cajal",
    source="The Nobel Prize in Physiology or Medicine 1906 (C. Golgi and S. Ramon y Cajal); nobelprize.org, How "
           "Golgi shared the 1906 Nobel Prize in Physiology or Medicine with Cajal",
    cite=r"Nobel Prize in Physiology or Medicine (1906)",
    checked="from the Nobel Foundation's article and encyclopedic accounts through a web search, 2026-11-13",
    licence="facts only",
    data={"year": 1906, "golgi": "the reticular theory: one continuous network",
          "cajal": "the neuron doctrine: separate cells", "stain": "Cajal's evidence came from Golgi's own stain",
          "settled": "by electron microscopy, in the 1950s"},
)

GIDON_2020 = Dataset(
    key="gidon_2020",
    title="Graded dendritic spikes in human cortical neurons",
    source="A. Gidon, T. A. Zolnik, P. Fidzinski, F. Bolduan, A. Papoutsi, P. Poirazi, M. Holtkamp, I. Vida and "
           "M. E. Larkum, Dendritic action potentials and computation in human layer 2/3 cortical neurons, "
           "Science 367 (2020) 83-87",
    cite=r"Gidon et al.\ (2020)",
    checked="from the authors' laboratory pages, the deposited manuscript's record and press accounts through a "
            "web search, 2026-11-13; the article was not read",
    licence="facts only",
    data={"tissue": "slices of human cortex removed in surgery for epilepsy or tumours",
          "finding": "calcium-mediated dendritic spikes whose amplitude is largest for inputs at threshold and "
                     "smaller for stronger ones",
          "claim": "in the authors' models, one such dendrite computes exclusive-or",
          "limit": "ex vivo tissue; whether other species have the same spikes is not known"},
)

# ---------------------------------------------------------------------------
# Part 6
# ---------------------------------------------------------------------------
LOEWI_1921 = Dataset(
    key="loewi_1921",
    title="Two frog hearts and a shared fluid: the nerve's effect on the heart is carried by a chemical",
    source="O. Loewi, Ueber humorale Uebertragbarkeit der Herznervenwirkung, Pfluegers Archiv 189 (1921) 239-242",
    cite=r"Loewi (1921)",
    checked="the reference, the design and the result from encyclopedic and historical accounts through a web search, "
            "2026-11-14; the paper was not read; the dream is Loewi's own later account, and historians note that "
            "how much of it is accurate is unclear",
    licence="facts only",
    data={"year": 1921, "design": "two beating frog hearts, one with its vagus nerve; fluid from the first is moved "
                                  "to the second",
          "result": "stimulating the vagus slows the first heart, and the fluid then slows the second",
          "substance": "Vagusstoff, later identified as acetylcholine",
          "dream": "by his own account the idea came in a dream on the night before Easter Sunday; he wrote it down, "
                   "could not read the note in the morning, and it returned the next night"},
)

HEBB_1949 = Dataset(
    key="hebb_1949",
    title="Hebb's postulate",
    source="D. O. Hebb, The Organization of Behavior (Wiley, 1949), p. 62",
    cite=r"Hebb (1949)",
    checked="the postulate as it is quoted in every textbook, from memory, 2026-11-14; the book was not opened",
    licence="a short quotation",
    data={"postulate": "When an axon of cell A is near enough to excite a cell B and repeatedly or persistently "
                       "takes part in firing it, some growth process or metabolic change takes place in one or "
                       "both cells such that A's efficiency, as one of the cells firing B, is increased."},
)

BLISS_LOMO_1973 = Dataset(
    key="bliss_lomo_1973",
    title="Long-lasting potentiation of a synapse after a burst of stimulation",
    source="T. V. P. Bliss and T. Lomo, Long-lasting potentiation of synaptic transmission in the dentate area of "
           "the anaesthetized rabbit following stimulation of the perforant path, Journal of Physiology 232 (1973) "
           "331-356",
    cite=r"Bliss \& L\o mo (1973)",
    checked="the title, the preparation and the journal reference from later reviews through a web search, "
            "2026-11-14; the paper was not read, so no size or duration of the effect is quoted",
    licence="facts only",
    data={"animal": "anaesthetized rabbit", "pathway": "perforant path to the dentate gyrus of the hippocampus",
          "finding": "after brief trains of high-frequency stimulation the response to a single test pulse stays "
                     "enlarged for a long time"},
)

BI_POO_1998 = Dataset(
    key="bi_poo_1998",
    title="The sign of a synaptic change depends on the order of two spikes",
    source="G.-Q. Bi and M.-M. Poo, Synaptic modifications in cultured hippocampal neurons: dependence on spike "
           "timing, synaptic strength, and postsynaptic cell type, Journal of Neuroscience 18 (1998) 10464-10472",
    cite=r"Bi \& Poo (1998)",
    checked="the abstract as summarized by a web search, 2026-11-14: a window of about 20 ms; the paper was not read",
    licence="facts only",
    data={"window_ms": 20, "preparation": "pairs of cultured hippocampal neurons",
          "finding": "input before the output spike strengthens the synapse; input after it weakens the synapse"},
)

HARTLINE_RATLIFF_1957 = Dataset(
    key="hartline_ratliff_1957",
    title="Neighbouring receptors in the eye of the horseshoe crab inhibit one another",
    source="H. K. Hartline and F. Ratliff, Inhibitory interaction of receptor units in the eye of Limulus, Journal "
           "of General Physiology 40 (1957) 357-376; The Nobel Prize in Physiology or Medicine 1967",
    cite=r"Hartline \& Ratliff (1957)",
    checked="the abstract's statements as summarized from PubMed Central by a web search, 2026-11-14; the volume "
            "and pages from memory",
    licence="facts only",
    data={"animal": "the horseshoe crab, Limulus", "nobel": 1967,
          "finding": "with two receptor units lit, the inhibition on each is a linear function of the activity of "
                     "the other",
          "later": "the inhibitory influences of several units add (1958)"},
)

GEIER_2008 = Dataset(
    key="geier_2008",
    title="Curving the streets of the Hermann grid abolishes its spots",
    source="J. Geier, L. Bernath, M. Hudak and L. Sera, Straightness as the main factor of the Hermann grid "
           "illusion, Perception 37 (2008) 651-665; the account it challenges: G. Baumgartner (1960)",
    cite=r"Geier et al.\ (2008)",
    checked="from the first author's own pages and secondary summaries through a web search, 2026-11-14; the paper "
            "was not read; later authors (Bach 2008; Schiller and Carvey 2005) also find the classical account "
            "incomplete, and the mechanism is still disputed",
    licence="facts only",
    data={"classical": "the spots come from centre-surround receptive fields: more surround is lit at a crossing "
                       "(Baumgartner 1960)",
          "finding": "a slight curvature of the streets makes the spots vanish, although the classical account "
                     "predicts no change"},
)

DEL_CASTILLO_KATZ_1954 = Dataset(
    key="del_castillo_katz_1954",
    title="Transmitter is released in packets of one size",
    source="J. del Castillo and B. Katz, Quantal components of the end-plate potential, Journal of Physiology 124 "
           "(1954) 560-573; the spontaneous miniature potentials: P. Fatt and B. Katz, Journal of Physiology 117 "
           "(1952) 109-128",
    cite=r"del Castillo \& Katz (1954)",
    checked="the reference, the preparation and the conclusion from the PubMed Central record and a 2006 "
            "retrospective through a web search, 2026-11-14; the paper was not read, so the histogram the part "
            "shows is a model synapse's and no figure is quoted from the paper",
    licence="facts only",
    data={"preparation": "the frog's nerve-muscle junction, with calcium lowered and magnesium raised so that "
                         "little transmitter is released",
          "finding": "the response to a nerve impulse is built of whole numbers of a unit, and the unit is the "
                     "size of the miniature potentials that occur spontaneously",
          "nobel": 1970},
)

LIU_2012 = Dataset(
    key="liu_2012",
    title="Reactivating the cells that were active during learning brings back the memory",
    source="X. Liu, S. Ramirez, P. T. Pang, C. B. Puryear, A. Govindarajan, K. Deisseroth and S. Tonegawa, "
           "Optogenetic stimulation of a hippocampal engram activates fear memory recall, Nature 484 (2012) 381-385; "
           "the false memory: S. Ramirez et al., Science 341 (2013) 387-391",
    cite=r"Liu et al.\ (2012)",
    checked="the abstract's statements as summarized from the MIT repository and PubMed Central by a web search, "
            "2026-11-14; the paper was not read, so no freezing percentages are quoted; the 2013 reference from "
            "memory",
    licence="facts only",
    data={"animal": "mice", "where": "the dentate gyrus of the hippocampus",
          "design": "cells active during fear learning in one box are made to carry a light-sensitive channel; "
                    "later, in a different box, light is delivered to them",
          "finding": "the mice freeze when the light is on, and not otherwise",
          "controls": "no freezing with light in mice that were not fear conditioned, or whose tagged cells "
                      "carried no channel, or whose tagged cells came from a neutral box"},
)

TURNER_2008 = Dataset(
    key="turner_2008",
    title="Antidepressant trials as registered with the regulator, and as published",
    source="E. H. Turner, A. M. Matthews, E. Linardatos, R. A. Tell and R. Rosenthal, Selective publication of "
           "antidepressant trials and its influence on apparent efficacy, New England Journal of Medicine 358 "
           "(2008) 252-260",
    cite=r"Turner et al.\ (2008)",
    checked="the abstract's figures from the PubMed record and secondary summaries through a web search, "
            "2026-11-14; the paper was not read, and its effect-size comparison is not quoted",
    licence="facts only",
    data={"trials": 74, "drugs": 12, "patients": 12564, "positive_fda": 0.51, "positive_published": 0.94,
          "positive_trials": 38, "positive_published_count": 37},
)

HARLOW_1868 = Dataset(
    key="harlow_1868",
    title="Phineas Gage: an iron rod through the left frontal lobe, and what his doctor reported",
    source="J. M. Harlow, Passage of an iron rod through the head, Boston Medical and Surgical Journal 39 (1848) "
           "389-393; Recovery from the passage of an iron bar through the head, Publications of the Massachusetts "
           "Medical Society 2 (1868) 327-347; the critical history: M. Macmillan, An Odd Kind of Fame (MIT Press, 2000)",
    cite=r"Harlow (1848, 1868)",
    checked="the date, place and outline from encyclopedic accounts through a web search, 2026-11-14; neither "
            "report nor Macmillan's book was read; sources differ on the rod's dimensions and on the year of his "
            "death, so the part gives neither as exact",
    licence="facts only",
    data={"date": "13 September 1848", "place": "Cavendish, Vermont", "job": "railway construction foreman",
          "rod": "a tamping iron usually given as about 110 cm long, 3 cm across and 6 kg",
          "reported": "Harlow wrote in 1868 that to his friends he was 'no longer Gage'",
          "later": "worked with horses in New Hampshire, then for years as a stagecoach driver in Chile; died in "
                   "San Francisco about twelve years after the accident",
          "thin": "the change of character rests on a few sentences written twenty years later"},
)

BROCA_1861 = Dataset(
    key="broca_1861",
    title="Leborgne ('Tan'): loss of speech with a lesion of the left frontal lobe",
    source="P. Broca, Perte de la parole, ramollissement chronique et destruction partielle du lobe anterieur "
           "gauche du cerveau, Bulletin de la Societe d'Anthropologie 2 (1861) 235-238",
    cite=r"Broca (1861)",
    checked="the reference and outline from historical accounts through a web search, 2026-11-14; the paper was "
            "not read",
    licence="facts only",
    data={"patient": "Leborgne, called Tan after the one syllable he could say", "died": "April 1861, at Bicetre",
          "lesion": "the lower rear part of the left frontal lobe"},
)

DRONKERS_2007 = Dataset(
    key="dronkers_2007",
    title="Broca's two preserved brains, scanned",
    source="N. F. Dronkers, O. Plaisant, M. T. Iba-Zizen and E. A. Cabanis, Paul Broca's historic cases: high "
           "resolution MR imaging of the brains of Leborgne and Lelong, Brain 130 (2007) 1432-1441",
    cite=r"Dronkers et al.\ (2007)",
    checked="the findings from the journal's abstract page, letters about the paper and a news report through a "
            "web search, 2026-11-14; the paper was not read",
    licence="facts only",
    data={"finding": "in both brains the damage ran well beyond the surface region Broca described, into deeper "
                     "tissue including a long fibre tract (the superior longitudinal fasciculus)",
          "area": "neither brain's damage covered the whole of what is now called Broca's area"},
)

WERNICKE_1874 = Dataset(
    key="wernicke_1874",
    title="A second aphasia, a connection between two centres, and a predicted third",
    source="C. Wernicke, Der aphasische Symptomencomplex (Breslau, 1874); L. Lichtheim, On aphasia, Brain 7 (1885) "
           "433-484",
    cite=r"Wernicke (1874); Lichtheim (1885)",
    checked="from reviews through a web search, 2026-11-14; neither work was read",
    licence="facts only",
    data={"sensory": "fluent speech with poor understanding, from damage further back, in the temporal lobe",
          "predicted": "conduction aphasia: damage to the connection alone, sparing both centres",
          "caveat": "the authors used their diagrams as aids to reasoning and did not claim they were anatomy"},
)

LASHLEY_1929 = Dataset(
    key="lashley_1929",
    title="The search for the engram: maze learning and the amount of cortex removed",
    source="K. S. Lashley, Brain Mechanisms and Intelligence (University of Chicago Press, 1929); In search of the "
           "engram, Symposia of the Society for Experimental Biology 4 (1950) 454-482",
    cite=r"Lashley (1929, 1950)",
    checked="the outline from encyclopedic accounts through a web search, 2026-11-14; neither work was read, and a "
            "sentence often quoted from the 1950 paper could not be confirmed, so it is not quoted",
    licence="facts only",
    data={"finding": "how badly a rat learned a maze depended on how much cortex was removed and hardly on where",
          "years": 30, "critics": "a maze can be solved by many senses, so removing any one region leaves others"},
)

PENFIELD_BOLDREY_1937 = Dataset(
    key="penfield_boldrey_1937",
    title="The body mapped on the cortex by electrical stimulation during surgery",
    source="W. Penfield and E. Boldrey, Somatic motor and sensory representation in the cerebral cortex of man as "
           "studied by electrical stimulation, Brain 60 (1937) 389-443",
    cite=r"Penfield \& Boldrey (1937)",
    checked="the number of patients and the dates from a review on PubMed Central through a web search, "
            "2026-11-14; the paper was not read; volume and pages from memory",
    licence="facts only",
    data={"patients": 126, "years": "1928 to 1936", "method": "patients awake under local anaesthesia, the "
                                                             "exposed cortex touched with a weak current"},
)

HORTON_HOYT_1991 = Dataset(
    key="horton_hoyt_1991",
    title="The map of the visual field on human primary visual cortex",
    source="J. C. Horton and W. F. Hoyt, The representation of the visual field in human striate cortex: a revision "
           "of the classic Holmes map, Archives of Ophthalmology 109 (1991) 816-824",
    cite=r"Horton \& Hoyt (1991)",
    checked="the reference from PubMed and the magnification formula from a paper that cites it, through a web "
            "search, 2026-11-14; the paper was not read",
    licence="facts only",
    data={"m0": 17.3, "e2": 0.75, "formula": "mm of cortex per degree = 17.3 / (eccentricity + 0.75)"},
)

SCOVILLE_MILNER_1957 = Dataset(
    key="scoville_milner_1957",
    title="H.M.: loss of new memories after removal of the inner temporal lobes on both sides",
    source="W. B. Scoville and B. Milner, Loss of recent memory after bilateral hippocampal lesions, Journal of "
           "Neurology, Neurosurgery and Psychiatry 20 (1957) 11-21; the skill: B. Milner (1962)",
    cite=r"Scoville \& Milner (1957)",
    checked="the outline, the year of the operation and the mirror-tracing result from PubMed Central and review "
            "articles through a web search, 2026-11-14; the paper was not read; sources give two dates in 1953 "
            "for the operation, so only the year is used",
    licence="facts only",
    data={"year": 1953, "patient": "Henry Molaison, known in print as H.M. until his death in 2008",
          "removed": "the inner part of both temporal lobes, including most of the hippocampus",
          "lost": "the ability to lay down new memories of facts and events",
          "skill": "over three days of mirror tracing his errors fell, with no memory of having done it before"},
)

NIELSEN_2013 = Dataset(
    key="nielsen_2013",
    title="Are people left-brained or right-brained?  Resting connectivity in 1,011 people",
    source="J. A. Nielsen, B. A. Zielinski, M. A. Ferguson, J. E. Lainhart and J. S. Anderson, An evaluation of the "
           "left-brain vs. right-brain hypothesis with resting state functional connectivity magnetic resonance "
           "imaging, PLoS ONE 8 (2013) e71275",
    cite=r"Nielsen et al.\ (2013)",
    checked="the abstract from PubMed Central through a web search, 2026-11-14; the paper was not read",
    licence="facts only; the article is open access",
    data={"people": 1011, "ages": "7 to 29", "regions": 7266,
          "finding": "lateralized connections were independent of one another across people; the data were 'not "
                     "consistent with a whole-brain phenotype' of stronger left or right networks"},
)

MAGUIRE_2000 = Dataset(
    key="maguire_2000",
    title="London taxi drivers and the back of the hippocampus",
    source="E. A. Maguire et al., Navigation-related structural change in the hippocampi of taxi drivers, PNAS 97 "
           "(2000) 4398-4403; K. Woollett and E. A. Maguire, Acquiring 'the Knowledge' of London's layout drives "
           "structural brain changes, Current Biology 21 (2011) 2109-2114",
    cite=r"Maguire et al.\ (2000)",
    checked="the samples and findings from secondary accounts, a funder's press release and the PubMed Central "
            "record of the 2011 paper through a web search, 2026-11-14; neither paper was read; the 2000 paper's "
            "title and pages from memory",
    licence="facts only",
    data={"drivers": 16, "years_driving": 14.3,
          "finding": "more grey matter at the back of the hippocampus than in matched controls, more with more "
                     "years of driving",
          "trainees": 79, "qualified": 39, "failed": 20, "controls": 31,
          "followup": "the back of the hippocampus grew in the trainees who qualified, and not in those who "
                      "failed or in controls"},
)

AZEVEDO_2009 = Dataset(
    key="azevedo_2009",
    title="How many neurons a human brain has",
    source="F. A. C. Azevedo et al., Equal numbers of neuronal and nonneuronal cells make the human brain an "
           "isometrically scaled-up primate brain, Journal of Comparative Neurology 513 (2009) 532-541",
    cite=r"Azevedo et al.\ (2009)",
    checked="the abstract's figures from PubMed through a web search, 2026-11-14; the paper was not read",
    licence="facts only",
    data={"neurons": 86.1e9, "neurons_sd": 8.1e9, "other_cells": 84.6e9, "cortex_share": 0.19},
)

RAICHLE_2002 = Dataset(
    key="raichle_2002",
    title="The brain's share of the body's mass and of its energy",
    source="M. E. Raichle and D. A. Gusnard, Appraising the brain's energy budget, PNAS 99 (2002) 10237-10239",
    cite=r"Raichle \& Gusnard (2002)",
    checked="the opening lines from PubMed Central through a web search, 2026-11-14",
    licence="facts only",
    data={"mass_share": 0.02, "energy_share": 0.20},
)

WEISKRANTZ_1974 = Dataset(
    key="weiskrantz_1974",
    title="Blindsight: responding to what one reports not seeing",
    source="L. Weiskrantz, E. K. Warrington, M. D. Sanders and J. Marshall, Visual capacity in the hemianopic field "
           "following a restricted occipital ablation, Brain 97 (1974) 709-728",
    cite=r"Weiskrantz et al.\ (1974)",
    checked="the reference from PubMed and the outline from review articles through a web search, 2026-11-14; "
            "the paper was not read, so no figures are quoted",
    licence="facts only",
    data={"patient": "D.B.", "finding": "he could point to and tell apart things shown in the part of the field "
                                         "where he said he saw nothing, and called his answers guesses"},
)

MAH_2014 = Dataset(
    key="mah_2014",
    title="Lesion-deficit maps are displaced by the way strokes spread",
    source="Y.-H. Mah, M. Husain, G. Rees and P. Nachev, Human brain lesion-deficit inference remapped, Brain 137 "
           "(2014) 2522-2531",
    cite=r"Mah et al.\ (2014)",
    checked="the abstract from PubMed Central and a later paper's summary through a web search, 2026-11-14; the "
            "paper was not read, so no displacement in millimetres is quoted",
    licence="facts only",
    data={"patients": 581, "finding": "testing each point of the brain separately mislocalizes a function, "
                                      "because damage at one point goes with damage at others; the error "
                                      "follows the territories of the arteries"},
)

WIESEL_HUBEL_1963 = Dataset(
    key="wiesel_hubel_1963",
    title="An eye closed early in life loses its hold on the visual cortex",
    source="T. N. Wiesel and D. H. Hubel, Single-cell responses in striate cortex of kittens deprived of vision in "
           "one eye, Journal of Neurophysiology 26 (1963) 1003-1017; D. H. Hubel and T. N. Wiesel, The period of "
           "susceptibility to the physiological effects of unilateral eye closure in kittens, Journal of Physiology "
           "206 (1970) 419-436",
    cite=r"Wiesel \& Hubel (1963)",
    checked="the references from PubMed Central and the outline from a history of the work through a web search, "
            "2026-11-14; neither paper was read; that the same closure in an adult cat has little effect is from "
            "the secondary account",
    licence="facts only",
    data={"finding": "in kittens with one eye closed from soon after birth, cortical cells came to respond to "
                     "the open eye only",
          "adults": "the same closure in adult cats, even for a year, gave a very different result"},
)

MERZENICH_1984 = Dataset(
    key="merzenich_1984",
    title="The map of the hand on the cortex is redrawn after a finger is lost",
    source="M. M. Merzenich et al., Somatosensory cortical map changes following digit amputation in adult monkeys, "
           "Journal of Comparative Neurology 224 (1984) 591-605; V. S. Ramachandran, D. Rogers-Ramachandran and "
           "M. Stewart, Perceptual correlates of massive cortical reorganization, Science 258 (1992) 1159-1160",
    cite=r"Merzenich et al.\ (1984)",
    checked="the abstracts as summarized by a web search, 2026-11-14; neither paper was read",
    licence="facts only",
    data={"animals": "adult owl monkeys", "months": "2 to 8",
          "finding": "the cortex that had served the lost finger came to respond to the neighbouring fingers and "
                     "the palm",
          "people": "in people who have lost an arm, touching the face can be felt in the missing hand"},
)

GAZZANIGA_1978 = Dataset(
    key="gazzaniga_1978",
    title="The split brain: what each hemisphere can report, and the interpreter",
    source="M. S. Gazzaniga, The split brain in man, Scientific American 217(2) (1967) 24-29; M. S. Gazzaniga and "
           "J. E. LeDoux, The Integrated Mind (Plenum, 1978); M. S. Gazzaniga, Forty-five years of split-brain "
           "research and still going strong, Nature Reviews Neuroscience 6 (2005) 653-659",
    cite=r"Gazzaniga \& LeDoux (1978)",
    checked="the experiments from secondary accounts through a web search, 2026-11-14; none of the three was "
            "read, and the references and the patient's sentence are from memory",
    licence="facts only",
    data={"where": "the California Institute of Technology, in Roger Sperry's laboratory, from the 1960s",
          "finding": "a word shown to the right hemisphere cannot be named, and the left hand can still pick out "
                     "the object",
          "interpreter": "shown a chicken's claw (left hemisphere) and a snow scene (right), the patient explains "
                         "the left hand's choice of a shovel by the chicken"},
)


# ---------------------------------------------------------------------------------------------------------------
# Part 8: reading the brain
# ---------------------------------------------------------------------------------------------------------------

BENNETT_2009 = Dataset(
    key="bennett_2009",
    title="A dead salmon in a scanner: uncorrected thresholds find activity where there is none",
    source="C. M. Bennett, A. A. Baird, M. B. Miller and G. L. Wolford, Neural correlates of interspecies perspective "
           "taking in the post-mortem Atlantic salmon: an argument for multiple comparisons correction, poster, "
           "Human Brain Mapping 2009; Journal of Serendipitous and Unexpected Results 1 (2010) 1-5",
    cite=r"Bennett et al.\ (2009)",
    checked="the design and result from the authors' own commentary and several summaries through a web search, "
            "2026-11-14; the poster was not read, so no voxel count is quoted",
    licence="facts only",
    data={"task": "photographs of people in social situations; the salmon was asked what each person was feeling",
          "threshold": "p < 0.001 at each voxel, uncorrected",
          "finding": "a cluster of active voxels in the brain cavity and the spinal column; none after correction "
                     "for the number of tests",
          "prize": "Ig Nobel, 2012"},
)

HUBEL_WIESEL_1959 = Dataset(
    key="hubel_wiesel_1959",
    title="Cells of the cat's visual cortex respond to a line at one orientation",
    source="D. H. Hubel and T. N. Wiesel, Receptive fields of single neurones in the cat's striate cortex, Journal of "
           "Physiology 148 (1959) 574-591",
    cite=r"Hubel \& Wiesel (1959)",
    checked="the abstract and later accounts through a web search, 2026-11-14; the paper was not read. The story of "
            "the slide's edge is from Wiesel's and Hubel's later recollections, not from the paper",
    licence="facts only",
    data={"finding": "to drive a cell, a stimulus had to have a particular form, size, position and orientation"},
)

BERGER_1929 = Dataset(
    key="berger_1929",
    title="The first recordings of the human brain's electrical rhythm through the skull",
    source="H. Berger, Ueber das Elektrenkephalogramm des Menschen, Archiv fuer Psychiatrie und Nervenkrankheiten 87 "
           "(1929) 527-570",
    cite=r"Berger (1929)",
    checked="the reference and the history from encyclopedia entries and centenary articles through a web search, "
            "2026-11-14; the paper was not read",
    licence="facts only",
    data={"first_recording": 1924, "published": 1929, "alpha_hz": "about 8 to 12",
          "confirmed": "by Adrian and Matthews in 1934"},
)

KUTAS_HILLYARD_1980 = Dataset(
    key="kutas_hillyard_1980",
    title="A word that does not fit its sentence: a negative potential near 400 ms",
    source="M. Kutas and S. A. Hillyard, Reading senseless sentences: brain potentials reflect semantic incongruity, "
           "Science 207 (1980) 203-205; M. Kutas and K. D. Federmeier, Thirty years and counting: finding meaning in "
           "the N400 component of the event-related brain potential, Annual Review of Psychology 62 (2011) 621-647",
    cite=r"Kutas \& Hillyard (1980)",
    checked="the reference, the example sentence and the latency from lecture notes and reviews through a web "
            "search, 2026-11-14; neither paper was read",
    licence="facts only",
    data={"sentence": "He spread the warm bread with socks.", "latency_ms": 400,
          "note": "they had expected the positive wave that follows a surprising stimulus"},
)

OGAWA_1990 = Dataset(
    key="ogawa_1990",
    title="A magnetic resonance signal that depends on the oxygen in the blood",
    source="S. Ogawa, T. M. Lee, A. R. Kay and D. W. Tank, Brain magnetic resonance imaging with contrast dependent "
           "on blood oxygenation, PNAS 87 (1990) 9868-9872; K. K. Kwong et al., Dynamic magnetic resonance imaging "
           "of human brain activity during primary sensory stimulation, PNAS 89 (1992) 5675-5679",
    cite=r"Ogawa et al.\ (1990)",
    checked="the references and the history from textbooks' accounts through a web search, 2026-11-14; neither "
            "paper was read",
    licence="facts only",
    data={"finding": "blood without oxygen lowers the signal around it; in 1992 two groups used the effect to watch "
                     "the human brain respond"},
)

LOGOTHETIS_2001 = Dataset(
    key="logothetis_2001",
    title="What the BOLD signal follows: the cortex's input and local processing more than its spikes",
    source="N. K. Logothetis, J. Pauls, M. Augath, T. Trinath and A. Oeltermann, Neurophysiological investigation of "
           "the basis of the fMRI signal, Nature 412 (2001) 150-157",
    cite=r"Logothetis et al.\ (2001)",
    checked="the abstract through a web search, 2026-11-14; the paper was not read",
    licence="facts only",
    data={"finding": "in the monkey's visual cortex, local field potentials predicted the BOLD response better than "
                     "the firing of the cells did"},
)

BOYNTON_1996 = Dataset(
    key="boynton_1996",
    title="The fMRI response is close to a linear, time-invariant transform of neural activity",
    source="G. M. Boynton, S. A. Engel, G. H. Glover and D. J. Heeger, Linear systems analysis of functional magnetic "
           "resonance imaging in human V1, Journal of Neuroscience 16 (1996) 4207-4221",
    cite=r"Boynton et al.\ (1996)",
    checked="the abstract and the first author's later review through a web search, 2026-11-14; the paper was not "
            "read. The peak near 5 s is the textbook's canonical response, not a figure from this paper",
    licence="facts only",
    data={"finding": "the response to a long stimulus is predicted by adding shifted copies of the response to a "
                     "short one; very brief stimuli give somewhat more than the rule predicts"},
)

EKLUND_2016 = Dataset(
    key="eklund_2016",
    title="Cluster inference with common settings gave far more false positives than the nominal 5%",
    source="A. Eklund, T. E. Nichols and H. Knutsson, Cluster failure: why fMRI inferences for spatial extent have "
           "inflated false-positive rates, PNAS 113 (2016) 7900-7905",
    cite=r"Eklund et al.\ (2016)",
    checked="the abstract and the discussion that followed through a web search, 2026-11-14; the paper was not "
            "read. The authors withdrew the paper's estimate of how many published studies were affected",
    licence="facts only",
    data={"controls": 499, "analyses": 3_000_000, "worst": 0.70, "nominal": 0.05,
          "cause": "the noise's spatial autocorrelation is not Gaussian: it has a long tail",
          "meaning": "the share of null analyses with at least one false cluster, not the share of findings that "
                     "are false"},
)

VUL_2009 = Dataset(
    key="vul_2009",
    title="Correlations between brain activity and personality that are too high to be true",
    source="E. Vul, C. Harris, P. Winkielman and H. Pashler, Puzzlingly high correlations in fMRI studies of emotion, "
           "personality, and social cognition, Perspectives on Psychological Science 4 (2009) 274-290; N. "
           "Kriegeskorte, W. K. Simmons, P. S. F. Bellgowan and C. I. Baker, Circular analysis in systems "
           "neuroscience: the dangers of double dipping, Nature Neuroscience 12 (2009) 535-540",
    cite=r"Vul et al.\ (2009)",
    checked="the abstracts and news reports through a web search, 2026-11-14; neither paper was read",
    licence="facts only",
    data={"share_vul": "more than half of the studies surveyed", "papers": 134, "circular": 57, "share": 0.42,
          "finding": "voxels were selected by the correlation that was then reported"},
)

POLDRACK_2006 = Dataset(
    key="poldrack_2006",
    title="Reverse inference: how much an activation says about a mental process",
    source="R. A. Poldrack, Can cognitive processes be inferred from neuroimaging data?, Trends in Cognitive Sciences "
           "10 (2006) 59-63; R. A. Poldrack, Inferring mental states from neuroimaging data: from reverse inference "
           "to large-scale decoding, Neuron 72 (2011) 692-697",
    cite=r"Poldrack (2006)",
    checked="the abstract of the first and the author's own summary of its numbers in the second, through a web "
            "search, 2026-11-14; neither was read in full",
    licence="facts only",
    data={"prior": 0.5, "posterior": 0.69, "bayes_factor": 2.3, "region": "Broca's area", "process": "language"},
)

MAREK_2022 = Dataset(
    key="marek_2022",
    title="Associations between brain measures and behaviour are small, and need thousands of people",
    source="S. Marek et al., Reproducible brain-wide association studies require thousands of individuals, Nature 603 "
           "(2022) 654-660",
    cite=r"Marek et al.\ (2022)",
    checked="the abstract and the university's summary through a web search, 2026-11-14; the paper was not read. A "
            "reply (Spisak et al. 2023) argues that cross-validated multivariate models need fewer people",
    licence="facts only",
    data={"people": 50_000, "median_n": 25, "median_r": 0.01},
)

ELLIOTT_2020 = Dataset(
    key="elliott_2020",
    title="The test-retest reliability of common task-fMRI measures is poor",
    source="M. L. Elliott et al., What is the test-retest reliability of common task-functional MRI measures? New "
           "empirical evidence and a meta-analysis, Psychological Science 31 (2020) 792-806",
    cite=r"Elliott et al.\ (2020)",
    checked="the abstract through a web search, 2026-11-14; the paper was not read",
    licence="facts only",
    data={"experiments": 90, "n": 1008, "icc": 0.397, "own_low": 0.067, "own_high": 0.485},
)

TANG_2023 = Dataset(
    key="tang_2023",
    title="The gist of continuous language decoded from fMRI",
    source="J. Tang, A. LeBel, S. Jain and A. G. Huth, Semantic reconstruction of continuous language from "
           "non-invasive brain recordings, Nature Neuroscience 26 (2023) 858-866",
    cite=r"Tang et al.\ (2023)",
    checked="the abstract and the funder's summary through a web search, 2026-11-14; the paper was not read. Three "
            "participants and about sixteen hours of listening each are from a newspaper report",
    licence="facts only",
    data={"participants": 3, "hours": 16,
          "finding": "the decoder recovers the meaning of what was heard or imagined, not the words, and only with "
                     "the person's cooperation"},
)

OWEN_2010 = Dataset(
    key="owen_2010",
    title="Brain training in 11,430 people: better at the trained tasks, no transfer",
    source="A. M. Owen et al., Putting brain training to the test, Nature 465 (2010) 775-778; D. J. Simons et al., Do "
           "'brain-training' programs work?, Psychological Science in the Public Interest 17 (2016) 103-186; S. M. "
           "Jaeggi, M. Buschkuehl, J. Jonides and W. J. Perrig, Improving fluid intelligence with training on "
           "working memory, PNAS 105 (2008) 6829-6833",
    cite=r"Owen et al.\ (2010)",
    checked="the abstract of Owen et al. from PubMed Central and the press summary of Simons et al. through a web "
            "search, 2026-11-14; none was read, and the reference to Jaeggi et al. is from memory",
    licence="facts only",
    data={"registered": 52_617, "completed": 11_430, "weeks": 6, "sessions": 24, "reviewed": 132,
          "settlement_usd": 2_000_000, "settlement_year": 2016},
)

KANWISHER_1997 = Dataset(
    key="kanwisher_1997",
    title="A region of the fusiform gyrus that responds more to faces than to other things",
    source="N. Kanwisher, J. McDermott and M. M. Chun, The fusiform face area: a module in human extrastriate cortex "
           "specialized for face perception, Journal of Neuroscience 17 (1997) 4302-4311",
    cite=r"Kanwisher et al.\ (1997)",
    checked="reviews by both sides of the dispute through a web search, 2026-11-14; the paper was not read",
    licence="facts only",
    data={"finding": "found in most people in the same place; whether it is for faces or for anything one is expert "
                     "at is still argued"},
)

GANIS_2011 = Dataset(
    key="ganis_2011",
    title="fMRI lie detection: perfect in the laboratory, a third with a covert countermeasure",
    source="G. Ganis, J. P. Rosenfeld, J. Meixner, R. A. Kievit and H. E. Schendan, Lying in the scanner: covert "
           "countermeasures disrupt deception detection by functional magnetic resonance imaging, NeuroImage 55 "
           "(2011) 312-319; United States v. Semrau, 693 F.3d 510 (6th Cir. 2012); F. A. Kozel et al., Detecting "
           "deception using functional magnetic resonance imaging, Biological Psychiatry 58 (2005) 605-613",
    cite=r"Ganis et al.\ (2011)",
    checked="the abstract and case summaries through a web search, 2026-11-14; none was read, and the reference to "
            "Kozel et al. is from memory",
    licence="facts only",
    data={"participants": 26, "without": 1.00, "with": 0.33,
          "court": "a United States court excluded an fMRI lie-detection report in 2010; the appeal court agreed "
                   "in 2012"},
)

BARKER_1985 = Dataset(
    key="barker_1985",
    title="A magnetic pulse through the scalp makes the opposite hand twitch",
    source="A. T. Barker, R. Jalinous and I. L. Freeston, Non-invasive magnetic stimulation of human motor cortex, "
           "Lancet 325 (1985) 1106-1107",
    cite=r"Barker et al.\ (1985)",
    checked="the PubMed record and an encyclopedia entry through a web search, 2026-11-14",
    licence="facts only",
    data={"finding": "the first transcranial magnetic stimulation of the human motor cortex"},
)


# ---------------------------------------------------------------------------------------------------------------
# Part 9: genes and evolution
# ---------------------------------------------------------------------------------------------------------------
_P9 = "through a web search, 2026-11-14; the paper was not read"

BOUCHARD_1990 = Dataset(
    key="bouchard_1990",
    title="The Minnesota Study of Twins Reared Apart, and the 'Jim twins' who began it",
    source="T. J. Bouchard, D. T. Lykken, M. McGue, N. L. Segal and A. Tellegen, Sources of human psychological "
           "differences: the Minnesota Study of Twins Reared Apart, Science 250 (1990) 223-228",
    cite=r"Bouchard et al.\ (1990)",
    checked="summaries of the paper and press accounts of the Jim twins " + _P9 + ". Secondary sources disagree on "
            "the number of pairs (48 or 56 reared-apart identical pairs), so none is given; the twins' coincidences "
            "are as the newspapers told them",
    licence="facts only",
    data={"reunited": 1979, "age": 39, "iq_variance_genetic": 0.70, "names": ("Jim Lewis", "Jim Springer"),
          "coincidences": ("both named James by their adoptive parents", "first wives both called Linda",
                           "second wives both called Betty", "sons called James Alan and James Allan",
                           "each had a dog called Toy")},
)

GALTON_1875 = Dataset(
    key="galton_1875",
    title="Galton's 'nature and nurture', and his questionnaire on twins",
    source="F. Galton, The history of twins, as a criterion of the relative powers of nature and nurture, Fraser's "
           "Magazine 12 (1875) 566-576; Hereditary Genius (1869); Inquiries into Human Faculty (1883), where the "
           "word 'eugenics' is coined",
    cite=r"Galton (1875)",
    checked="histories of the twin method " + _P9 + ". Galton did not compare identical with fraternal twins as "
            "the later method does; that comparison dates from the 1920s",
    licence="facts only",
    data={"hereditary_genius": 1869, "twins": 1875, "eugenics_coined": 1883},
)

FISHER_1918 = Dataset(
    key="fisher_1918",
    title="Many Mendelian factors of small effect give continuous variation and the correlations between relatives",
    source="R. A. Fisher, The correlation between relatives on the supposition of Mendelian inheritance, "
           "Transactions of the Royal Society of Edinburgh 52 (1918) 399-433",
    cite=r"Fisher (1918)",
    checked="histories of quantitative genetics " + _P9,
    licence="facts only",
    data={"year": 1918},
)

BOUCHARD_MCGUE_1981 = Dataset(
    key="bouchard_mcgue_1981",
    title="A review of 111 studies of familial resemblance in measured intelligence",
    source="T. J. Bouchard and M. McGue, Familial studies of intelligence: a review, Science 212 (1981) 1055-1059",
    cite=r"Bouchard \& McGue (1981)",
    checked="the abstract " + _P9 + ". The correlation of .86 for identical twins reared together is confirmed by a "
            "later paper that cites it; the .60 for fraternal twins is from memory of the paper's figure and is an "
            "open check",
    licence="facts only",
    data={"studies": 111, "correlations": 526, "pairings": 113_942, "r_mz": 0.86, "r_dz": 0.60},
)

POLDERMAN_2015 = Dataset(
    key="polderman_2015",
    title="Fifty years of twin studies: 17,804 traits",
    source="T. J. C. Polderman et al., Meta-analysis of the heritability of human traits based on fifty years of twin "
           "studies, Nature Genetics 47 (2015) 702-709",
    cite=r"Polderman et al.\ (2015)",
    checked="the abstract " + _P9,
    licence="facts only",
    data={"traits": 17_804, "publications": 2_748, "pairs": 14_558_903, "h2": 0.49, "additive_share": 0.69,
          "years": (1958, 2012)},
)

TURKHEIMER_2000 = Dataset(
    key="turkheimer_2000",
    title="Three laws of behaviour genetics",
    source="E. Turkheimer, Three laws of behavior genetics and what they mean, Current Directions in Psychological "
           "Science 9 (2000) 160-164; C. F. Chabris et al., The fourth law of behavior genetics, Current Directions "
           "in Psychological Science 24 (2015) 304-312",
    cite=r"Turkheimer (2000)",
    checked="the abstract and later commentary " + _P9,
    licence="facts only",
    data={"laws": ("All human behavioural traits are heritable.",
                   "The effect of being raised in the same family is smaller than the effect of genes.",
                   "A substantial part of the variation is accounted for by neither genes nor families."),
          "fourth": "A typical trait is associated with very many genetic variants, each of very small effect."},
)

TURKHEIMER_2003 = Dataset(
    key="turkheimer_2003",
    title="Among poor families the heritability of children's IQ was near zero",
    source="E. Turkheimer, A. Haley, M. Waldron, B. D'Onofrio and I. I. Gottesman, Socioeconomic status modifies "
           "heritability of IQ in young children, Psychological Science 14 (2003) 623-628",
    cite=r"Turkheimer et al.\ (2003)",
    checked="the abstract " + _P9 + ". Later samples are mixed: the pattern has been found again in the United "
            "States and not in several European samples",
    licence="facts only",
    data={"pairs": 319, "mz_pairs": 114, "age": 7, "poor_shared": 0.60, "poor_genes": "close to zero",
          "affluent": "almost exactly the reverse"},
)

HAWORTH_2010 = Dataset(
    key="haworth_2010",
    title="The heritability of general cognitive ability rises from childhood to young adulthood",
    source="C. M. A. Haworth et al., The heritability of general cognitive ability increases linearly from childhood "
           "to young adulthood, Molecular Psychiatry 15 (2010) 1112-1120",
    cite=r"Haworth et al.\ (2010)",
    checked="the abstract " + _P9,
    licence="facts only",
    data={"pairs": 11_000, "countries": 4, "ages": (9, 12, 17), "h2": (0.41, 0.55, 0.66)},
)

NCD_RISC_2016 = Dataset(
    key="ncd_risc_2016",
    title="A century of change in adult height",
    source="NCD Risk Factor Collaboration, A century of trends in adult human height, eLife 5 (2016) e13410",
    cite=r"NCD-RisC (2016)",
    checked="the abstract " + _P9,
    licence="facts only (CC BY article)",
    data={"studies": 1_472, "people": 18_600_000, "born": (1896, 1996), "korean_women_cm": 20.2,
          "iranian_men_cm": 16.5, "dutch_men_cm": 182.5},
)

HERITABILITY_TABLE = Dataset(
    key="heritability_table",
    title="Twin-study heritabilities of six traits, from meta-analyses",
    source="P. F. Sullivan, K. S. Kendler and M. C. Neale, Schizophrenia as a complex trait, Archives of General "
           "Psychiatry 60 (2003) 1187-1192; S. V. Faraone and H. Larsson, Genetics of attention deficit hyperactivity "
           "disorder, Molecular Psychiatry 24 (2019) 562-575; B. Tick et al., Heritability of autism spectrum "
           "disorders, Journal of Child Psychology and Psychiatry 57 (2016) 585-595; A. R. Branigan, K. J. McCallum "
           "and J. Freese, Variation in the heritability of educational attainment, Social Forces 92 (2013) 109-140; "
           "T. Vukasovic and D. Bratko, Heritability of personality, Psychological Bulletin 141 (2015) 769-785; "
           "Haworth et al. (2010)",
    cite=r"meta-analyses of twin studies, 2003--2019",
    checked="each abstract or a summary of it " + _P9 + ". These are twin estimates and rest on the twin design's "
            "assumptions",
    licence="facts only",
    data={"traits": (("which language you speak", 0.0, "by construction: nobody inherits a language"),
                     ("years of schooling", 0.40, "Branigan et al. 2013"),
                     ("personality traits", 0.47, "Vukasovic & Bratko 2015, twin studies"),
                     ("cognitive ability at 17", 0.66, "Haworth et al. 2010"),
                     ("ADHD", 0.74, "Faraone & Larsson 2019"),
                     ("schizophrenia", 0.81, "Sullivan et al. 2003")),
          "autism_range": (0.64, 0.91), "cognitive_at_9": 0.41, "personality_family_studies": 0.22},
)

CASPI_2003 = Dataset(
    key="caspi_2003",
    title="A serotonin-transporter variant, stressful life events and depression: the claim and its tests",
    source="A. Caspi et al., Influence of life stress on depression: moderation by a polymorphism in the 5-HTT gene, "
           "Science 301 (2003) 386-389; N. Risch et al., Interaction between the serotonin transporter gene "
           "(5-HTTLPR), stressful life events, and risk of depression: a meta-analysis, JAMA 301 (2009) 2462-2471",
    cite=r"Caspi et al.\ (2003)",
    checked="summaries of both papers " + _P9 + ". A 2011 meta-analysis of 54 studies found the interaction again; "
            "the large preregistered analysis of 2019 did not",
    licence="facts only",
    data={"cohort": "Dunedin, New Zealand", "risch_studies": 14, "risch_people": 14_000},
)

BORDER_2019 = Dataset(
    key="border_2019",
    title="Eighteen candidate genes for depression, tested in samples of up to 443,264",
    source="R. Border et al., No support for historical candidate gene or candidate gene-by-interaction hypotheses "
           "for major depression across multiple large samples, American Journal of Psychiatry 176 (2019) 376-387",
    cite=r"Border et al.\ (2019)",
    checked="the abstract " + _P9,
    licence="facts only",
    data={"genes": 18, "n_min": 62_138, "n_max": 443_264, "studied_at_least": 10},
)

CHABRIS_2012 = Dataset(
    key="chabris_2012",
    title="Twelve published genetic associations with intelligence, retested",
    source="C. F. Chabris et al., Most reported genetic associations with general intelligence are probably false "
           "positives, Psychological Science 23 (2012) 1314-1323",
    cite=r"Chabris et al.\ (2012)",
    checked="the abstract " + _P9,
    licence="facts only",
    data={"variants": 12, "samples": (5_571, 1_759, 2_441), "tests": 32, "significant": 1, "expected": (10, 15)},
)

RIETVELD_2013 = Dataset(
    key="rietveld_2013",
    title="The first genome-wide association study of educational attainment",
    source="C. A. Rietveld et al., GWAS of 126,559 individuals identifies genetic variants associated with "
           "educational attainment, Science 340 (2013) 1467-1471",
    cite=r"Rietveld et al.\ (2013)",
    checked="the abstract " + _P9,
    licence="facts only",
    data={"n": 126_559, "discovery": 101_069, "replication": 25_490, "snps": 3, "r2_per_snp": 0.0002,
          "months_per_allele": 1, "score_r2": 0.02},
)

LEE_2018 = Dataset(
    key="lee_2018",
    title="Educational attainment in 1.1 million people, and in 3 million",
    source="J. J. Lee et al., Gene discovery and polygenic prediction from a genome-wide association study of "
           "educational attainment in 1.1 million individuals, Nature Genetics 50 (2018) 1112-1121; A. Okbay et al., "
           "Polygenic prediction of educational attainment within and between families from genome-wide association "
           "analyses in 3 million individuals, Nature Genetics 54 (2022) 437-449",
    cite=r"Lee et al.\ (2018)",
    checked="both abstracts " + _P9,
    licence="facts only",
    data={"n": 1_100_000, "snps": 1_271, "score_r2": (0.11, 0.13), "cognitive_r2": (0.07, 0.10),
          "within_family_smaller": 0.40,
          "okbay_n": 3_000_000, "okbay_snps": 3_952, "okbay_r2": (0.12, 0.16)},
)

KONG_2018 = Dataset(
    key="kong_2018",
    title="Genetic nurture: the alleles parents did not pass on still predict their children's schooling",
    source="A. Kong et al., The nature of nurture: effects of parental genotypes, Science 359 (2018) 424-428",
    cite=r"Kong et al.\ (2018)",
    checked="the abstract " + _P9,
    licence="facts only",
    data={"probands": 21_637, "share_of_transmitted": 0.299},
)

HOWE_2022 = Dataset(
    key="howe_2022",
    title="Genome-wide association within sibships",
    source="L. J. Howe et al., Within-sibship genome-wide association analyses decrease bias in estimates of direct "
           "genetic effects, Nature Genetics 54 (2022) 581-592",
    cite=r"Howe et al.\ (2022)",
    checked="the abstract " + _P9,
    licence="facts only",
    data={"siblings": 178_086, "cohorts": 19, "phenotypes": 25,
          "smaller_within": ("height", "educational attainment", "cognitive ability", "depressive symptoms",
                             "smoking")},
)

YENGO_2022 = Dataset(
    key="yengo_2022",
    title="Height in 5.4 million people: the common variants are nearly all found",
    source="L. Yengo et al., A saturated map of common genetic variants associated with human height, Nature 610 "
           "(2022) 704-712",
    cite=r"Yengo et al.\ (2022)",
    checked="the abstract " + _P9 + ". The twin heritability of height of about 0.8 set beside it is the textbook "
            "figure",
    licence="facts only",
    data={"n": 5_400_000, "snps": 12_111, "variance_european": 0.40, "variance_all_common": 0.45,
          "variance_other": (0.10, 0.20), "twin_h2": 0.8},
)

MARTIN_2019 = Dataset(
    key="martin_2019",
    title="Polygenic scores built in Europeans predict worse in everyone else",
    source="A. R. Martin et al., Clinical use of current polygenic risk scores may exacerbate health disparities, "
           "Nature Genetics 51 (2019) 584-591",
    cite=r"Martin et al.\ (2019)",
    checked="news summaries of the paper and its preprint " + _P9 + ". The preprint gives 'about 2- to 5-fold' for "
            "East Asian and African ancestries; the share of participants of European descent (79%) is from a "
            "truncated excerpt",
    licence="facts only",
    data={"fold_lower_african": 4.5, "fold_lower_east_asian": 2.0, "european_share": 0.79},
)

KARAVANI_2019 = Dataset(
    key="karavani_2019",
    title="What choosing among embryos by a polygenic score would gain",
    source="E. Karavani et al., Screening human embryos for polygenic traits has limited utility, Cell 179 (2019) "
           "1424-1435",
    cite=r"Karavani et al.\ (2019)",
    checked="summaries of the paper " + _P9,
    licence="facts only",
    data={"embryos": 10, "iq_points": 2.5, "height_cm": 2.5},
)

BUSS_1989 = Dataset(
    key="buss_1989",
    title="Mate preferences in 37 cultures",
    source="D. M. Buss, Sex differences in human mate preferences: evolutionary hypotheses tested in 37 cultures, "
           "Behavioral and Brain Sciences 12 (1989) 1-49",
    cite=r"Buss (1989)",
    checked="summaries of the paper " + _P9 + ". Most samples were urban, educated and from industrial countries, "
            "as the author notes",
    licence="facts only",
    data={"people": 10_047, "cultures": 37, "countries": 33, "financial_prospects": 36, "younger_mates": 37},
)

HEIJMANS_2008 = Dataset(
    key="heijmans_2008",
    title="Methylation of a growth gene six decades after the Dutch Hunger Winter",
    source="B. T. Heijmans et al., Persistent epigenetic differences associated with prenatal exposure to famine in "
           "humans, PNAS 105 (2008) 17046-17049; I. C. G. Weaver et al., Epigenetic programming by maternal "
           "behavior, Nature Neuroscience 7 (2004) 847-854",
    cite=r"Heijmans et al.\ (2008)",
    checked="both abstracts " + _P9,
    licence="facts only",
    data={"people": 60, "famine": (1944, 1945), "gene": "IGF2", "compared_with": "unexposed same-sex siblings"},
)

WEIR_2002 = Dataset(
    key="weir_2002",
    title="A crow bends a wire into a hook",
    source="A. A. S. Weir, J. Chappell and A. Kacelnik, Shaping of hooks in New Caledonian crows, Science 297 (2002) "
           "981; C. Rutz et al., Tool bending in New Caledonian crows, Royal Society Open Science 3 (2016) 160439",
    cite=r"Weir et al.\ (2002)",
    checked="accounts of both studies " + _P9 + "; the reference of the 2016 study is from memory",
    licence="facts only",
    data={"bird": "Betty", "later": "wild crows bend their twig tools as a matter of routine, so the feat was less of "
                                    "an invention than it looked"},
)


# ---------------------------------------------------------------------------------------------------------------
# Part 10: chemistry and clocks
# ---------------------------------------------------------------------------------------------------------------
_P10 = "through a web search, 2026-11-14; the paper was not read"

KLEITMAN_1938 = Dataset(
    key="kleitman_1938",
    title="Thirty-two days in Mammoth Cave on a 28-hour day",
    source="N. Kleitman, Sleep and Wakefulness (1939; revised 1963); contemporary report: Science: Cave Men, Time, "
           "18 July 1938; K. Miller, Mapping the Darkness (2023)",
    cite=r"Kleitman (1939)",
    checked="the 1938 magazine report, a National Park Service account and a book excerpt " + _P10 + ". Sources "
            "differ on the cave's depth, which is not given",
    licence="facts only",
    data={"year": 1938, "days": 32, "day_hours": 28, "student": "Bruce Richardson", "student_age": 25,
          "kleitman_age": 43, "adapted": "the student's temperature rhythm stretched toward 28 hours",
          "did_not": "Kleitman's kept its 24-hour course, and he grew sleepy at about ten each evening"},
)

CZEISLER_1999 = Dataset(
    key="czeisler_1999",
    title="The human clock's own period is close to 24 hours",
    source="C. A. Czeisler et al., Stability, precision, and near-24-hour period of the human circadian pacemaker, "
           "Science 284 (1999) 2177-2181",
    cite=r"Czeisler et al.\ (1999)",
    checked="the PubMed abstract and the university's report " + _P10,
    licence="facts only",
    data={"period_h": 24.18, "people": 24, "young": 11, "older": 13, "day_hours": 28, "days": (29, 38)},
)

ASERINSKY_1953 = Dataset(
    key="aserinsky_1953",
    title="Periods of rapid eye movement in sleep, and the dreams reported from them",
    source="E. Aserinsky and N. Kleitman, Regularly occurring periods of eye motility, and concomitant phenomena, "
           "during sleep, Science 118 (1953) 273-274",
    cite=r"Aserinsky \& Kleitman (1953)",
    checked="a reprint of the paper's text " + _P10 + ". Sources differ on the number of sleepers, which is not "
            "given",
    licence="facts only",
    data={"awakenings_rem": 27, "dreams_rem": 20},
)

BORBELY_1982 = Dataset(
    key="borbely_1982",
    title="The two-process model of sleep regulation",
    source="A. A. Borbely, A two process model of sleep regulation, Human Neurobiology 1 (1982) 195-204; S. Daan, "
           "D. G. M. Beersma and A. A. Borbely, Timing of human sleep: recovery process gated by a circadian "
           "pacemaker, American Journal of Physiology 246 (1984) R161-R178",
    cite=r"Borb\'ely (1982)",
    checked="the figure legend of the model's 2016 reappraisal (Journal of Sleep Research 25, 131-143) " + _P10,
    licence="facts only",
    data={"tau_rise_h": 18.18, "tau_fall_h": 4.2},
)

VAN_DONGEN_2003 = Dataset(
    key="van_dongen_2003",
    title="Two weeks of six hours' sleep impair attention as much as two nights without any",
    source="H. P. A. Van Dongen, G. Maislin, J. M. Mullington and D. F. Dinges, The cumulative cost of additional "
           "wakefulness, Sleep 26 (2003) 117-126",
    cite=r"Van Dongen et al.\ (2003)",
    checked="the abstract " + _P10,
    licence="facts only",
    data={"hours_in_bed": (8, 6, 4), "days": 14, "total_deprivation_days": 3, "threshold_awake_h": 15.84,
          "equivalent_nights": 2, "noticed": "sleepiness ratings levelled off while performance kept falling"},
)

RASCH_2007 = Dataset(
    key="rasch_2007",
    title="Cueing a memory during slow-wave sleep, and the pooled effect since",
    source="B. Rasch, C. Buchel, S. Gais and J. Born, Odor cues during slow-wave sleep prompt declarative memory "
           "consolidation, Science 315 (2007) 1426-1429; X. Hu, L. Y. Cheng, M. H. Chiu and K. A. Paller, Promoting "
           "memory consolidation during sleep: a meta-analysis of targeted memory reactivation, Psychological "
           "Bulletin 146 (2020) 218-244",
    cite=r"Rasch et al.\ (2007)",
    checked="both abstracts " + _P10,
    licence="facts only",
    data={"experiments": 91, "effects": 212, "people": 2_004, "g": 0.29, "g_lo": 0.21, "g_hi": 0.38},
)

HOBSON_1977 = Dataset(
    key="hobson_1977",
    title="Two accounts of dreaming",
    source="J. A. Hobson and R. W. McCarley, The brain as a dream state generator: an activation-synthesis hypothesis "
           "of the dream process, American Journal of Psychiatry 134 (1977) 1335-1348; M. Solms, Dreaming and REM "
           "sleep are controlled by different brain mechanisms, Behavioral and Brain Sciences 23 (2000) 843-850",
    cite=r"Hobson \& McCarley (1977)",
    checked="reference lists and summaries " + _P10,
    licence="facts only",
    data={},
)

CAPPUCCIO_2010 = Dataset(
    key="cappuccio_2010",
    title="Sleep duration and death in 1.4 million people",
    source="F. P. Cappuccio, L. D'Elia, P. Strazzullo and M. A. Miller, Sleep duration and all-cause mortality: a "
           "systematic review and meta-analysis of prospective studies, Sleep 33 (2010) 585-592",
    cite=r"Cappuccio et al.\ (2010)",
    checked="the abstract and full-text summary " + _P10,
    licence="facts only",
    data={"studies": 16, "people": 1_382_999, "deaths": 112_566, "rr_short": 1.12, "rr_long": 1.30},
)

SIEGEL_1982 = Dataset(
    key="siegel_1982",
    title="A dose of heroin kills more rats in an unfamiliar place",
    source="S. Siegel, R. E. Hinson, M. D. Krank and J. McCully, Heroin 'overdose' death: contribution of "
           "drug-associated environmental cues, Science 216 (1982) 436-437",
    cite=r"Siegel et al.\ (1982)",
    checked="the paper's table as quoted " + _P10,
    licence="facts only",
    data={"dose_mg_kg": 15, "usual_place": 0.324, "new_place": 0.643, "no_history": 0.964, "n": (37, 42, 28)},
)

SOLOMON_CORBIT_1974 = Dataset(
    key="solomon_corbit_1974",
    title="The opponent-process theory",
    source="R. L. Solomon and J. D. Corbit, An opponent-process theory of motivation: I. Temporal dynamics of "
           "affect, Psychological Review 81 (1974) 119-145",
    cite=r"Solomon \& Corbit (1974)",
    checked="the PubMed record and summaries " + _P10,
    licence="facts only",
    data={},
)

DUNSTER_2018 = Dataset(
    key="dunster_2018",
    title="Seattle moves its high schools' start 55 minutes later",
    source="G. P. Dunster et al., Sleepmore in Seattle: later school start times are associated with more sleep and "
           "better performance in high school students, Science Advances 4 (2018) eaau6200",
    cite=r"Dunster et al.\ (2018)",
    checked="the university's summary and news reports " + _P10 + ". A before-and-after comparison, not a "
            "randomized trial",
    licence="facts only",
    data={"shift_min": 55, "from": "7:50", "to": "8:45", "more_sleep_min": 34, "grades_pct": 4.5},
)

TRAUER_2015 = Dataset(
    key="trauer_2015",
    title="Cognitive behavioural therapy for chronic insomnia: twenty trials",
    source="J. M. Trauer et al., Cognitive behavioral therapy for chronic insomnia: a systematic review and "
           "meta-analysis, Annals of Internal Medicine 163 (2015) 191-204",
    cite=r"Trauer et al.\ (2015)",
    checked="the abstract " + _P10,
    licence="facts only",
    data={"trials": 20, "people": 1_162, "onset_min": 19, "awake_min": 26, "efficiency_points": 9.9},
)

XIE_2013 = Dataset(
    key="xie_2013",
    title="Does sleep wash the brain? A finding and its dispute",
    source="L. Xie et al., Sleep drives metabolite clearance from the adult brain, Science 342 (2013) 373-377; A. "
           "Miao et al., Brain clearance is reduced during sleep and anesthesia, Nature Neuroscience 27 (2024) "
           "1046-1050",
    cite=r"Xie et al.\ (2013)",
    checked="both abstracts and commentary on the dispute " + _P10 + "; mice in both",
    licence="facts only",
    data={"space_increase": 0.60},
)

PHOENIX_1959 = Dataset(
    key="phoenix_1959",
    title="Hormones before birth organize; hormones in adulthood activate",
    source="C. H. Phoenix, R. W. Goy, A. A. Gerall and W. C. Young, Organizing action of prenatally administered "
           "testosterone propionate on the tissues mediating mating behavior in the female guinea pig, Endocrinology "
           "65 (1959) 369-382",
    cite=r"Phoenix et al.\ (1959)",
    checked="reviews " + _P10,
    licence="facts only",
    data={},
)

TEIGEN_1994 = Dataset(
    key="teigen_1994",
    title="The Yerkes-Dodson law and its thin beginning",
    source="R. M. Yerkes and J. D. Dodson, The relation of strength of stimulus to rapidity of habit-formation, "
           "Journal of Comparative Neurology and Psychology 18 (1908) 459-482; K. H. Teigen, Yerkes-Dodson: a law "
           "for all seasons, Theory & Psychology 4 (1994) 525-547",
    cite=r"Teigen (1994)",
    checked="summaries of both " + _P10,
    licence="facts only",
    data={},
)

ROENNEBERG_2004 = Dataset(
    key="roenneberg_2004",
    title="Chronotype through life: latest at about twenty",
    source="T. Roenneberg et al., A marker for the end of adolescence, Current Biology 14 (2004) R1038-R1039; M. "
           "Wittmann, J. Dinich, M. Merrow and T. Roenneberg, Social jetlag: misalignment of biological and social "
           "time, Chronobiology International 23 (2006) 497-509",
    cite=r"Roenneberg et al.\ (2004)",
    checked="summaries of the survey, and the PubMed record of the second paper, " + _P10,
    licence="facts only",
    data={"latest_women": 19.5, "latest_men": 21.0},
)


ALL = {d.key: d for d in (KANT_1786, HELMHOLTZ_1850, DONDERS_1868, EBBINGHAUS_1885, WOODS_2015, PFUNGST_1907,
                          PEIRCE_JASTROW_1884, ROSENTHAL_FODE_1963, RAUDENBUSH_1984, DE_QUIDT_2018, LIT_2011,
                          MITCHELL_2021, STEVENS_1946, FORER_1949, JOHANSSON_2005, CREDE_2017, HEDGE_2018,
                          FLAKE_FRIED_2020, BEM_2011, COHEN_1962, SIMMONS_2011, OSC_2015, MANY_LABS, CAMERER_2018,
                          SCHEEL_2021, LEVELT_2012, DREBER_2015, PROTZKO_2023, HODGKIN_HUXLEY_1952,
                          COLE_CURTIS_1939, ADRIAN_1926, GOLGI_CAJAL_1906, GIDON_2020, LOEWI_1921, HEBB_1949,
                          BLISS_LOMO_1973, BI_POO_1998, HARTLINE_RATLIFF_1957, GEIER_2008,
                          DEL_CASTILLO_KATZ_1954, LIU_2012, TURNER_2008,
                          HARLOW_1868, BROCA_1861, DRONKERS_2007, WERNICKE_1874, LASHLEY_1929, PENFIELD_BOLDREY_1937,
                          HORTON_HOYT_1991, SCOVILLE_MILNER_1957, NIELSEN_2013, MAGUIRE_2000, AZEVEDO_2009,
                          RAICHLE_2002, WEISKRANTZ_1974, MAH_2014,
                          WIESEL_HUBEL_1963, MERZENICH_1984, GAZZANIGA_1978,
                          BENNETT_2009, HUBEL_WIESEL_1959, BERGER_1929, KUTAS_HILLYARD_1980, OGAWA_1990,
                          LOGOTHETIS_2001, BOYNTON_1996, EKLUND_2016, VUL_2009, POLDRACK_2006,
                          MAREK_2022, ELLIOTT_2020, TANG_2023, OWEN_2010, KANWISHER_1997,
                          GANIS_2011, BARKER_1985,
                          BOUCHARD_1990, GALTON_1875, FISHER_1918, BOUCHARD_MCGUE_1981, POLDERMAN_2015,
                          TURKHEIMER_2000, TURKHEIMER_2003, HAWORTH_2010, NCD_RISC_2016, HERITABILITY_TABLE,
                          CASPI_2003, BORDER_2019, CHABRIS_2012, RIETVELD_2013, LEE_2018, KONG_2018, HOWE_2022,
                          YENGO_2022, MARTIN_2019, KARAVANI_2019, BUSS_1989, HEIJMANS_2008, WEIR_2002,
                          KLEITMAN_1938, CZEISLER_1999, ASERINSKY_1953, BORBELY_1982, VAN_DONGEN_2003, RASCH_2007,
                          HOBSON_1977, CAPPUCCIO_2010, SIEGEL_1982, SOLOMON_CORBIT_1974, DUNSTER_2018, TRAUER_2015,
                          XIE_2013, PHOENIX_1959, TEIGEN_1994, ROENNEBERG_2004)}
