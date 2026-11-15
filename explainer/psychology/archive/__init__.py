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
           "XIE_2013", "PHOENIX_1959", "TEIGEN_1994", "ROENNEBERG_2004",
           "WEBER_1834", "FECHNER_1860", "STEVENS_1957", "POULTON_1968", "LEVITT_1971", "WATSON_PELLI_1983",
           "WICHMANN_HILL_2001", "MCGILL_GOLDBERG_1968", "HALBERDA_2008", "GIBBON_1977", "LESMES_2010",
           "DEVRIES_ROSE", "BERNOULLI_1738", "PLATEAU_1872", "THURSTONE_1927",
           "MACKWORTH_1948", "PETERSON_1954", "TANNER_SWETS_1954", "WOLFE_2005", "FLECK_MITROFF_2007", "GIGERENZER_HOFFRAGE_1995", "RATCLIFF_1992", "YONELINAS_1994", "SEE_1995", "SWETS_2000", "SWETS_1961", "MANISCALCO_LAU_2012", "MICKES_2012",
           "HECHT_1942", "BAYLOR_1979", "TINSLEY_2016", "KUFFLER_1953", "CAMPBELL_ROBSON_1968", "BLAKEMORE_CAMPBELL_1969", "LAFER_SOUSA_2015", "MILNER_1991", "JORDAN_2010", "COLOUR_TABLES", "OKABE_ITO",
           "ADELSON_1995", "ERNST_BANKS_2002", "ALAIS_BURR_2004", "RAHNEV_DENISON_2018", "WEISS_2002", "THOMPSON_1982", "ADAMS_2004", "SEGALL_1966", "AMIR_FIRESTONE_2025", "GAUTHIER_1999", "YIN_1969", "YAMINS_2014", "GEIRHOS_2019", "VONG_2024", "WHEATSTONE_1838",
           "BEKESY_1960", "KEMP_1978", "LIBERMAN_1957", "MCMURRAY_2002", "MCGURK_1976", "MALLICK_2015", "BOTVINICK_COHEN_1998", "LUSH_2020", "MELZACK_WALL_1965", "LEVINE_1978", "HANIG_1901", "BUSHDID_2014", "MCDERMOTT_2016", "KUJAWA_LIBERMAN_2009",
           "PAVLOV_1927", "THORNDIKE_1898", "WATSON_RAYNER_1920", "HARRIS_1979", "FERSTER_SKINNER_1957", "RESCORLA_1968", "WASSERMAN_1993", "KAMIN_1969", "MAES_2016", "RESCORLA_WAGNER_1972", "LUBOW_MOORE_1959", "BOUTON_BOLLES_1979", "MACKINTOSH_PEARCE_HALL", "GALLISTEL_GIBBON_2000", "HERRNSTEIN_1961", "GARCIA_KOELLING_1966", "BRELAND_1961", "BANDURA_1961", "PRENDERGAST_2006", "ZENDLE_CAIRNS_2018", "GERSHMAN_2010", "MITCHELL_2009", "SCHILLER_2010",
           "SCHULTZ_1997", "STEINBERG_2013", "FRANK_2004", "WILSON_2014", "TOLMAN_HONZIK_1930", "TOLMAN_1948", "HAFTING_2005", "ADAMS_DICKINSON_1981", "DAW_2011", "FEHER_DA_SILVA_2020", "MOMENNEJAD_2017", "HOWE_2013", "DABNEY_2020", "REDISH_2004", "LI_2010", "WEINTRAUB_2010", "WANG_2018",
           "SIMONS_CHABRIS_1999", "RENSINK_1997", "CHERRY_1953", "BROADBENT_1958", "MORAY_1959", "TREISMAN_1960", "LAVIE_1995", "POSNER_1980", "TREISMAN_GELADE_1980", "WOLFE_2021", "ITTI_KOCH_1998", "DREW_2013", "RAYMOND_1992", "PASHLER_1994", "STROOP_1935", "ERIKSEN_1974", "BOTVINICK_2001", "ROGERS_MONSELL_1995", "MORAN_DESIMONE_1985", "REYNOLDS_HEEGER_2009", "BUNDESEN_1990", "STRAYER_2001", "OPHIR_2009", "ANDERSON_2011", "AWH_2012",
           "MILLER_1956", "SPERLING_1960", "PETERSON_1959", "KEPPEL_UNDERWOOD_1962", "BADDELEY_HITCH_1974", "BADDELEY_1975", "SHALLICE_WARRINGTON_1970", "STERNBERG_1966", "LUCK_VOGEL_1997", "COWAN_2001", "ZHANG_LUCK_2008", "BAYS_2009", "VANDENBERG_2012", "FUNAHASHI_1989", "WIMMER_2014", "MONGILLO_2008", "DANEMAN_CARPENTER_1980", "KANE_2005", "JAEGGI_2008", "REDICK_2013", "MELBY_LERVAG_2016", "SIMONS_2016", "FTC_LUMOSITY_2016",
           "PEERS_FREE_RECALL", "CRAIK_TULVING_1975", "BERTSCH_2007", "DRESLER_2017", "GODDEN_BADDELEY_1975", "MURRE_2021", "KOHNKEN_1999",
           "SAVINGS_REPLICATIONS", "ROEDIGER_KARPICKE_2006", "SCHOOLER_1990", "ALOGNA_2014", "LOFTUS_PALMER_1974", "ROEDIGER_MCDERMOTT_1995", "CEPEDA_2008", "LOFTUS_PICKRELL_1995", "TALARICO_RUBIN_2003", "HARDWICKE_2016", "PATIHIS_2013", "WIXTED_WELLS_2017", "DUNLOSKY_2013"]


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

# ---------------------------------------------------------------------------------------------------------------
# Part 11: the threshold
# ---------------------------------------------------------------------------------------------------------------
_P11 = "through a web search, 2026-11-14; the original was not read"

WEBER_1834 = Dataset(
    key="weber_1834",
    title="Weber's lifted weights and the constant fraction",
    source="E. H. Weber, De Pulsu, Resorptione, Auditu et Tactu: Annotationes Anatomicae et Physiologicae (1834); "
           "Der Tastsinn und das Gemeingefuehl (1846)",
    cite=r"Weber (1834)",
    checked="encyclopaedia entries and textbook accounts " + _P11 + ". The Latin title differs between sources and "
            "so does the fraction for weights (1/30 and 1/40 are both quoted): the films give no single figure",
    licence="facts only",
    data={"year": 1834, "german": 1846},
)

FECHNER_1860 = Dataset(
    key="fechner_1860",
    title="Fechner's Elements of Psychophysics",
    source="G. T. Fechner, Elemente der Psychophysik, 2 vols (Leipzig, 1860); E. G. Boring, Fechner: inadvertent "
           "founder of psychophysics, Psychometrika 26 (1961) 3-8",
    cite=r"Fechner (1860)",
    checked="Wozniak's introduction to the Classics in the History of Psychology edition, encyclopaedia entries and "
            "Boring (1961) " + _P11 + ". The number of judgments he made is not given",
    licence="facts only",
    data={"year": 1860, "volumes": 2, "insight": "22 October 1850",
          "methods": ("just noticeable differences", "right and wrong cases", "average error")},
)

STEVENS_1957 = Dataset(
    key="stevens_1957",
    title="Stevens's power law and his table of exponents",
    source="S. S. Stevens, On the psychophysical law, Psychological Review 64 (1957) 153-181; S. S. Stevens, "
           "Psychophysics (1975)",
    cite=r"Stevens (1957)",
    checked="the citation and the table of exponents as reproduced in textbooks " + _P11,
    licence="facts only",
    data={"exponents": (("brightness", 0.33), ("loudness", 0.67), ("vibration", 0.95), ("visual length", 1.0),
                        ("heaviness", 1.45), ("electric shock", 3.5))},
)

POULTON_1968 = Dataset(
    key="poulton_1968",
    title="Range and sequence effects in magnitude estimation",
    source="E. C. Poulton, The new psychophysics: six models for magnitude estimation, Psychological Bulletin 69 "
           "(1968) 1-19; R. Teghtsoonian, On the exponents in Stevens's law and the constant in Ekman's law, "
           "Psychological Review 78 (1971) 71-80",
    cite=r"Poulton (1968)",
    checked="citations and later reviews of the dispute " + _P11,
    licence="facts only",
    data={},
)

LEVITT_1971 = Dataset(
    key="levitt_1971",
    title="Transformed up-down staircases",
    source="H. Levitt, Transformed up-down methods in psychoacoustics, Journal of the Acoustical Society of America "
           "49 (1971) 467-477",
    cite=r"Levitt (1971)",
    checked="the paper's equilibrium points as tabulated by later papers " + _P11,
    licence="facts only",
    data={"targets": ((1, 0.5), (2, 0.7071), (3, 0.7937), (4, 0.8409))},
)

WATSON_PELLI_1983 = Dataset(
    key="watson_pelli_1983",
    title="QUEST: a Bayesian adaptive psychometric method",
    source="A. B. Watson and D. G. Pelli, QUEST: a Bayesian adaptive psychometric method, Perception & "
           "Psychophysics 33 (1983) 113-120",
    cite=r"Watson \& Pelli (1983)",
    checked="descriptions in later papers " + _P11 + "; the page numbers are from memory",
    licence="facts only",
    data={},
)

WICHMANN_HILL_2001 = Dataset(
    key="wichmann_hill_2001",
    title="Fitting the psychometric function, and bootstrap intervals",
    source="F. A. Wichmann and N. J. Hill, The psychometric function: I. Fitting, sampling, and goodness of fit; II. "
           "Bootstrap-based confidence intervals and sampling, Perception & Psychophysics 63 (2001) 1293-1313, "
           "1314-1329",
    cite=r"Wichmann \& Hill (2001)",
    checked="the citations and summaries " + _P11,
    licence="facts only",
    data={},
)

MCGILL_GOLDBERG_1968 = Dataset(
    key="mcgill_goldberg_1968",
    title="The near miss to Weber's law for the intensity of tones",
    source="W. J. McGill and J. P. Goldberg, A study of the near-miss involving Weber's law and pure-tone intensity "
           "discrimination, Perception & Psychophysics 4 (1968) 105-109",
    cite=r"McGill \& Goldberg (1968)",
    checked="the citation and later papers' summaries (a slope of about 0.9 instead of 1) " + _P11,
    licence="facts only",
    data={"slope": 0.9},
)

HALBERDA_2008 = Dataset(
    key="halberda_2008",
    title="Weber's law for number",
    source="J. Halberda, M. M. M. Mazzocco and L. Feigenson, Individual differences in non-verbal number acuity "
           "correlate with maths achievement, Nature 455 (2008) 665-668; J. Halberda and L. Feigenson, Developmental "
           "change in the acuity of the number sense, Developmental Psychology 44 (2008) 1457-1465",
    cite=r"Halberda et al.\ (2008)",
    checked="the papers' summaries " + _P11,
    licence="facts only",
    data={"adult_w": 0.11, "age3_ratio": "3:4", "age6_ratio": "5:6"},
)

GIBBON_1977 = Dataset(
    key="gibbon_1977",
    title="Weber's law for time: scalar timing",
    source="J. Gibbon, Scalar expectancy theory and Weber's law in animal timing, Psychological Review 84 (1977) "
           "279-325",
    cite=r"Gibbon (1977)",
    checked="the paper's opening pages and later reviews " + _P11,
    licence="facts only",
    data={},
)

LESMES_2010 = Dataset(
    key="lesmes_2010",
    title="The quick CSF: four parameters in fifty trials",
    source="L. A. Lesmes, Z.-L. Lu, J. Baek and T. D. Albright, Bayesian adaptive estimation of the contrast "
           "sensitivity function: the quick CSF method, Journal of Vision 10(3):17 (2010) 1-21",
    cite=r"Lesmes et al.\ (2010)",
    checked="the abstract and later papers' descriptions " + _P11,
    licence="facts only",
    data={"parameters": 4, "trials": 50},
)

DEVRIES_ROSE = Dataset(
    key="devries_rose",
    title="The square-root law: photon noise sets the threshold in dim light",
    source="Hl. de Vries, The quantum character of light and its bearing upon threshold of vision, the differential "
           "sensitivity and visual acuity of the eye, Physica 10 (1943) 553-564; A. Rose, The sensitivity performance "
           "of the human eye on an absolute scale, Journal of the Optical Society of America 38 (1948) 196-208",
    cite=r"de Vries (1943); \ Rose (1948)",
    checked="encyclopaedia entries and later papers' accounts " + _P11 + "; the page numbers are from memory",
    licence="facts only",
    data={"slopes": (("dark light", 0.0), ("square root", 0.5), ("Weber", 1.0))},
)

BERNOULLI_1738 = Dataset(
    key="bernoulli_1738",
    title="Bernoulli's measure of risk: the value of a gain falls in proportion to wealth",
    source="D. Bernoulli, Specimen theoriae novae de mensura sortis, Commentarii Academiae Scientiarum Imperialis "
           "Petropolitanae 5 (1738) 175-192; translated by L. Sommer as Exposition of a new theory on the measurement "
           "of risk, Econometrica 22 (1954) 23-36",
    cite=r"Bernoulli (1738)",
    checked="the 1954 translation's section 10 as quoted in later accounts " + _P11 + "; the volume and pages of the "
            "1738 original are from memory",
    licence="public domain",
    data={"year": 1738, "rule": "the utility of a small gain is inversely proportional to the wealth already held"},
)

PLATEAU_1872 = Dataset(
    key="plateau_1872",
    title="Plateau's painters: a grey midway between black and white, and the first power law",
    source="J. Plateau, Sur la mesure des sensations physiques, et sur la loi qui lie l'intensite de ces sensations a "
           "l'intensite de la cause excitante, Bulletins de l'Academie Royale de Belgique 33 (1872) 376-388",
    cite=r"Plateau (1872)",
    checked="later papers' accounts of the bisection experiment and of Delboeuf's replication " + _P11 + "; the "
            "number of painters and Plateau's own figures are not given; the volume and pages are from memory",
    licence="public domain",
    data={"year": 1872},
)

THURSTONE_1927 = Dataset(
    key="thurstone_1927",
    title="Thurstone's law of comparative judgment, and a scale of the seriousness of crimes",
    source="L. L. Thurstone, A law of comparative judgment, Psychological Review 34 (1927) 273-286; L. L. Thurstone, "
           "The method of paired comparisons for social values, Journal of Abnormal and Social Psychology 21 (1927) "
           "384-400",
    cite=r"Thurstone (1927)",
    checked="the citations, an encyclopaedia entry and a replication's account (19 offences) " + _P11,
    licence="facts only",
    data={"offences": 19},
)

# ---------------------------------------------------------------------------------- Part 12: signal and noise
_P12 = "through a web search, 2026-11-14; the original was not read"

MACKWORTH_1948 = Dataset(
    key="mackworth_1948",
    title="The breakdown of vigilance: radar observers and the Clock Test",
    source="N. H. Mackworth, The breakdown of vigilance during prolonged visual search, Quarterly Journal of "
           "Experimental Psychology 1 (1948) 6-21",
    cite=r"Mackworth (1948)",
    checked="encyclopaedia entries and reviews " + _P12 + "; the detection rates are not given",
    licence="facts only",
    data={"session_hours": 2},
)

PETERSON_1954 = Dataset(
    key="peterson_1954",
    title="The theory of signal detectability, from Michigan",
    source="W. W. Peterson, T. G. Birdsall and W. C. Fox, The theory of signal detectability, Transactions of the "
           "IRE Professional Group on Information Theory 4(4) (1954) 171-212",
    cite=r"Peterson, Birdsall \& Fox (1954)",
    checked="the library record and later accounts " + _P12,
    licence="facts only",
    data={},
)

TANNER_SWETS_1954 = Dataset(
    key="tanner_swets_1954",
    title="A decision-making theory of visual detection",
    source="W. P. Tanner Jr. and J. A. Swets, A decision-making theory of visual detection, Psychological Review 61 "
           "(1954) 401-409; D. M. Green and J. A. Swets, Signal Detection Theory and Psychophysics (1966)",
    cite=r"Tanner \& Swets (1954)",
    checked="citations " + _P12 + "; the pages are from memory",
    licence="facts only",
    data={},
)

WOLFE_2005 = Dataset(
    key="wolfe_2005",
    title="Rare items often missed in visual searches",
    source="J. M. Wolfe, T. S. Horowitz and N. M. Kenner, Rare items often missed in visual searches, Nature 435 "
           "(2005) 439-440",
    cite=r"Wolfe et al.\ (2005)",
    checked="the paper's text as reproduced in a public copy " + _P12,
    licence="facts only",
    data={"prevalence": (0.5, 0.1, 0.01), "miss": (0.11, 0.25, 0.52)},
)

FLECK_MITROFF_2007 = Dataset(
    key="fleck_mitroff_2007",
    title="Rare targets are rarely missed in correctable search",
    source="M. S. Fleck and S. R. Mitroff, Rare targets are rarely missed in correctable search, Psychological "
           "Science 18 (2007) 943-947",
    cite=r"Fleck \& Mitroff (2007)",
    checked="later papers' summaries " + _P12 + "; the volume and pages are from memory",
    licence="facts only",
    data={},
)

GIGERENZER_HOFFRAGE_1995 = Dataset(
    key="gigerenzer_hoffrage_1995",
    title="The mammogram problem in probabilities and in natural frequencies",
    source="G. Gigerenzer and U. Hoffrage, How to improve Bayesian reasoning without instruction: frequency formats, "
           "Psychological Review 102 (1995) 684-704; D. M. Eddy, Probabilistic reasoning in clinical medicine (1982)",
    cite=r"Gigerenzer \& Hoffrage (1995)",
    checked="later papers quoting the problem and the result " + _P12,
    licence="facts only",
    data={"prevalence": 0.01, "sensitivity": 0.8, "false_positive": 0.096, "correct_prob": 0.16, "correct_freq": 0.46},
)

RATCLIFF_1992 = Dataset(
    key="ratcliff_1992",
    title="Recognition memory's zROC slope of about 0.8",
    source="R. Ratcliff, C.-F. Sheu and S. D. Gronlund, Testing global memory models using ROC curves, "
           "Psychological Review 99 (1992) 518-535",
    cite=r"Ratcliff et al.\ (1992)",
    checked="reviews that cite the slope " + _P12 + "; the title and pages are from memory",
    licence="facts only",
    data={"slope": 0.8},
)

YONELINAS_1994 = Dataset(
    key="yonelinas_1994",
    title="A dual-process account of recognition ROCs",
    source="A. P. Yonelinas, Receiver-operating characteristics in recognition memory: evidence for a dual-process "
           "model, Journal of Experimental Psychology: Learning, Memory, and Cognition 20 (1994) 1341-1354",
    cite=r"Yonelinas (1994)",
    checked="the author's posted copy, by its first page " + _P12,
    licence="facts only",
    data={},
)

SEE_1995 = Dataset(
    key="see_1995",
    title="A meta-analysis of the sensitivity decrement in vigilance",
    source="J. E. See, S. R. Howe, J. S. Warm and W. N. Dember, A meta-analysis of the sensitivity decrement in "
           "vigilance, Psychological Bulletin 117 (1995) 230-249",
    cite=r"See et al.\ (1995)",
    checked="the abstract as quoted " + _P12,
    licence="facts only",
    data={"studies": 42},
)

SWETS_2000 = Dataset(
    key="swets_2000",
    title="Psychological science can improve diagnostic decisions",
    source="J. A. Swets, R. M. Dawes and J. Monahan, Psychological science can improve diagnostic decisions, "
           "Psychological Science in the Public Interest 1 (2000) 1-26",
    cite=r"Swets, Dawes \& Monahan (2000)",
    checked="the abstract " + _P12,
    licence="facts only",
    data={},
)

SWETS_1961 = Dataset(
    key="swets_1961",
    title="Decision processes in perception",
    source="J. A. Swets, W. P. Tanner Jr. and T. G. Birdsall, Decision processes in perception, Psychological "
           "Review 68 (1961) 301-340",
    cite=r"Swets, Tanner \& Birdsall (1961)",
    checked="later reviews describing it " + _P12 + "; the pages are from memory",
    licence="facts only",
    data={},
)

MANISCALCO_LAU_2012 = Dataset(
    key="maniscalco_lau_2012",
    title="Meta-d': how much of the evidence confidence can use",
    source="B. Maniscalco and H. Lau, A signal detection theoretic approach for estimating metacognitive sensitivity "
           "from confidence ratings, Consciousness and Cognition 21 (2012) 422-430",
    cite=r"Maniscalco \& Lau (2012)",
    checked="the abstract " + _P12,
    licence="facts only",
    data={},
)

MICKES_2012 = Dataset(
    key="mickes_2012",
    title="ROC analysis of police line-ups: simultaneous against sequential",
    source="L. Mickes, H. D. Flowe and J. T. Wixted, Receiver operating characteristic analysis of eyewitness "
           "memory: comparing the diagnostic accuracy of simultaneous versus sequential lineups, Journal of "
           "Experimental Psychology: Applied 18 (2012) 361-376",
    cite=r"Mickes, Flowe \& Wixted (2012)",
    checked="the paper's posted copy, by its summary and one table as quoted " + _P12,
    licence="facts only",
    data={"sequential": (0.44, 0.15), "simultaneous": (0.52, 0.28)},
)


# ---------------------------------------------------------------------------
# Part 13
# ---------------------------------------------------------------------------
_P13 = "through a web search, 2026-11-14"

HECHT_1942 = Dataset(
    key="hecht_1942",
    title="Energy, quanta and vision: how few quanta a dark-adapted eye can see",
    source="S. Hecht, S. Shlaer and M. H. Pirenne, Energy, quanta, and vision, Journal of General Physiology 25 (1942) "
           "819-840 (Laboratory of Biophysics, Columbia University)",
    cite=r"Hecht, Shlaer \& Pirenne (1942)",
    checked="the abstract (PMC2142545) as quoted, " + _P13 + ": 2.1-5.7 x 10^-10 erg, 54-148 quanta at "
            "the cornea, the three corrections, 5-14 absorbed, about 500 rods, 5-8 from the statistics",
    licence="facts from a published article",
    data={"wavelength_nm": 510, "erg": (2.1e-10, 5.7e-10), "cornea": (54, 148), "reflection": 0.04, "media": 0.50,
          "retina_absorbed": 0.20, "absorbed": (5, 14), "rods": 500, "statistical": (5, 8), "dark_minutes": 40},
)

BAYLOR_1979 = Dataset(
    key="baylor_1979",
    title="Single rods respond to single photons",
    source="D. A. Baylor, T. D. Lamb and K.-W. Yau, Responses of retinal rods to single photons, Journal of Physiology "
           "288 (1979) 613-634",
    cite=r"Baylor, Lamb \& Yau (1979)",
    checked="the abstract, " + _P13,
    licence="facts from a published article",
    data={"species": "toad", "event_pA": 1.0, "event_sd_pA": 0.2, "dark_current_share": 0.05, "quantum_efficiency": 0.5},
)

TINSLEY_2016 = Dataset(
    key="tinsley_2016",
    title="Direct detection of a single photon by humans",
    source="J. N. Tinsley, M. I. Molodtsov, R. Prevedel, D. Wartmann, J. Espigule-Pons, M. Lauwers and A. Vaziri, "
           "Direct detection of a single photon by humans, Nature Communications 7 (2016) 12172",
    cite=r"Tinsley et al.\ (2016)",
    checked="the open-access article's numbers as quoted in summaries and in van der Reep et al. (2022), " + _P13,
    licence="facts from an open-access article (CC BY)",
    data={"trials": 30767, "single_photon_events": 2420, "p_correct": 0.516, "se": 0.010, "p_value": 0.0545,
          "high_confidence": 0.60},
)

KUFFLER_1953 = Dataset(
    key="kuffler_1953",
    title="Centre and surround in the cat's retinal ganglion cells",
    source="S. W. Kuffler, Discharge patterns and functional organization of mammalian retina, Journal of "
           "Neurophysiology 16 (1953) 37-68",
    cite=r"Kuffler (1953)",
    checked="the citation and later summaries, " + _P13,
    licence="facts only",
    data={"species": "cat", "types": ("on-centre", "off-centre")},
)

CAMPBELL_ROBSON_1968 = Dataset(
    key="campbell_robson_1968",
    title="Fourier analysis and the visibility of gratings",
    source="F. W. Campbell and J. G. Robson, Application of Fourier analysis to the visibility of gratings, Journal of "
           "Physiology 197 (1968) 551-566",
    cite=r"Campbell \& Robson (1968)",
    checked="secondary accounts of the band-pass CSF peaking near 3-5 cycles per degree, " + _P13,
    licence="facts only",
    data={"peak_cpd": (3.0, 5.0)},
)

BLAKEMORE_CAMPBELL_1969 = Dataset(
    key="blakemore_campbell_1969",
    title="Adapting to a grating raises the threshold for similar gratings",
    source="C. Blakemore and F. W. Campbell, On the existence of neurones in the human visual system selectively "
           "sensitive to the orientation and size of retinal images, Journal of Physiology 203 (1969) 237-260",
    cite=r"Blakemore \& Campbell (1969)",
    checked="the abstract (PMC1351526), " + _P13,
    licence="facts only",
    data={"max_elevation": 5.0},
)

LAFER_SOUSA_2015 = Dataset(
    key="lafer_sousa_2015",
    title="The dress: one photograph, different colours",
    source="R. Lafer-Sousa, K. L. Hermann and B. R. Conway, Striking individual differences in color perception "
           "uncovered by 'the dress' photograph, Current Biology 25 (2015) R545-R546",
    cite=r"Lafer-Sousa, Hermann \& Conway (2015)",
    checked="the authors' university's release and later summaries, " + _P13,
    licence="facts only (the photograph itself is not reproduced)",
    data={"n": 1400, "naive": 300, "blue_black": 0.57, "white_gold": 0.30, "blue_brown": 0.11, "other": 0.02},
)

MILNER_1991 = Dataset(
    key="milner_1991",
    title="Patient D.F.: posting without perceiving",
    source="A. D. Milner, D. I. Perrett, R. S. Johnston, P. J. Benson, T. R. Jordan, D. W. Heeley, D. Bettucci, "
           "F. Mortara, R. Mutani, E. Terazzi and D. L. W. Davidson, Perception and action in 'visual form agnosia', "
           "Brain 114 (1991) 405-428; M. A. Goodale, A. D. Milner, L. S. Jakobson and D. P. Carey, A neurological "
           "dissociation between perceiving objects and grasping them, Nature 349 (1991) 154-156",
    cite=r"Milner et al.\ (1991); \ Goodale et al.\ (1991)",
    checked="reviews' accounts of the slot task, " + _P13 + "; author lists from memory",
    licence="facts only",
    data={"cause": "carbon monoxide poisoning"},
)

JORDAN_2010 = Dataset(
    key="jordan_2010",
    title="A tetrachromat among carriers of anomalous trichromacy",
    source="G. Jordan, S. S. Deeb, J. M. Bosten and J. D. Mollon, The dimensionality of color vision in carriers of "
           "anomalous trichromacy, Journal of Vision 10(8) (2010) 12",
    cite=r"Jordan et al.\ (2010)",
    checked="the abstract and methods, " + _P13,
    licence="facts only",
    data={"carriers": 24, "tetrachromats": 1, "separation_nm": 12},
)

COLOUR_TABLES = Dataset(
    key="colour_tables",
    title="Colour-matching functions and cone fundamentals",
    source="CIE 1931 2-degree colour-matching functions; W. S. Stiles and J. M. Burch, Interim report to the CIE "
           "(1955) 2-degree pilot colour-matching functions (10 observers); A. Stockman and L. T. Sharpe, The spectral "
           "sensitivities of the middle- and long-wavelength-sensitive cones, Vision Research 40 (2000) 1711-1737 "
           "(2-degree fundamentals); CIE 1951 scotopic luminous efficiency.  All as tabulated by the Colour & Vision "
           "Research Laboratory, cvrl.org",
    cite=r"CIE (1931); \ Stiles \& Burch (1955); \ Stockman \& Sharpe (2000); \ via cvrl.org",
    checked="downloaded from cvrl.org at 5 nm and transcribed by script into archive/_colour_tables.py, 2026-11-14; "
            "peaks checked (L 570, M 545, S 445 nm; rods 505 nm)",
    licence="published standard tables, freely distributed by CVRL",
    data={"primaries_nm": (645.2, 526.3, 444.4), "observers": 10},
)

OKABE_ITO = Dataset(
    key="okabe_ito",
    title="A palette for colour-blind readers",
    source="M. Okabe and K. Ito, Color Universal Design (CUD): how to make figures and presentations that are friendly "
           "to colorblind people (J*Fly, 2002; revised 2008)",
    cite=r"Okabe \& Ito (2008)",
    checked="hex values as widely reproduced; from memory, 2026-11-14",
    licence="facts only",
    data={"hex": ("#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7", "#000000")},
)


# ---------------------------------------------------------------------------
# Part 14
# ---------------------------------------------------------------------------
_P14 = "through a web search, 2026-11-14"

ADELSON_1995 = Dataset(
    key="adelson_1995",
    title="The checker-shadow illusion",
    source="E. H. Adelson, Checkershadow illusion (MIT, 1995); E. H. Adelson, Lightness perception and lightness "
           "illusions, in M. Gazzaniga (ed.), The New Cognitive Neurosciences, 2nd ed. (MIT Press, 2000) 339-351",
    cite=r"Adelson (1995)",
    checked="demonstration pages and later accounts, " + _P14 + "; the image is not reproduced (the film draws its own)",
    licence="facts only",
    data={"finding": "two squares of equal luminance, one in a cast shadow, look very different"},
)

ERNST_BANKS_2002 = Dataset(
    key="ernst_banks_2002",
    title="Visual and haptic cues combined as an optimal observer would",
    source="M. O. Ernst and M. S. Banks, Humans integrate visual and haptic information in a statistically optimal "
           "fashion, Nature 415 (2002) 429-433",
    cite=r"Ernst \& Banks (2002)",
    checked="the abstract and later accounts, " + _P14,
    licence="facts only",
    data={"task": "height of a ridge, seen and felt", "noise": "visual noise added to shift the weights"},
)

ALAIS_BURR_2004 = Dataset(
    key="alais_burr_2004",
    title="The ventriloquist effect as near-optimal combination",
    source="D. Alais and D. Burr, The ventriloquist effect results from near-optimal bimodal integration, Current "
           "Biology 14 (2004) 257-262",
    cite=r"Alais \& Burr (2004)",
    checked="the abstract, " + _P14 + "; pages from memory",
    licence="facts only",
    data={},
)

RAHNEV_DENISON_2018 = Dataset(
    key="rahnev_denison_2018",
    title="Suboptimality in perceptual decision making",
    source="D. Rahnev and R. N. Denison, Suboptimality in perceptual decision making, Behavioral and Brain Sciences 41 "
           "(2018) e223",
    cite=r"Rahnev \& Denison (2018)",
    checked="the abstract, " + _P14,
    licence="facts only",
    data={"classes": 8},
)

WEISS_2002 = Dataset(
    key="weiss_2002",
    title="Motion illusions as optimal percepts",
    source="Y. Weiss, E. P. Simoncelli and E. H. Adelson, Motion illusions as optimal percepts, Nature Neuroscience 5 "
           "(2002) 598-604",
    cite=r"Weiss, Simoncelli \& Adelson (2002)",
    checked="the authors' abstract pages and a commentary, " + _P14,
    licence="facts only",
    data={"assumptions": ("noisy measurements, worse at low contrast", "a prior favouring slow speeds")},
)

THOMPSON_1982 = Dataset(
    key="thompson_1982",
    title="Low-contrast motion looks slower",
    source="P. Thompson, Perceived rate of movement depends on contrast, Vision Research 22 (1982) 377-380",
    cite=r"Thompson (1982)",
    checked="later papers' accounts, " + _P14,
    licence="facts only",
    data={"reversal_hz": 8},
)

ADAMS_2004 = Dataset(
    key="adams_2004",
    title="Experience can change the light-from-above prior",
    source="W. J. Adams, E. W. Graf and M. O. Ernst, Experience can change the 'light-from-above' prior, Nature "
           "Neuroscience 7 (2004) 1057-1058",
    cite=r"Adams, Graf \& Ernst (2004)",
    checked="the abstract and a conference abstract, " + _P14,
    licence="facts only",
    data={},
)

SEGALL_1966 = Dataset(
    key="segall_1966",
    title="The Müller-Lyer illusion across societies",
    source="M. H. Segall, D. T. Campbell and M. J. Herskovits, The Influence of Culture on Visual Perception "
           "(Bobbs-Merrill, 1966); and Cultural differences in the perception of geometric illusions, Science 139 "
           "(1963) 769-771",
    cite=r"Segall, Campbell \& Herskovits (1966)",
    checked="secondary accounts, " + _P14 + "; Science pages from memory",
    licence="facts only",
    data={"least": "San foragers of the Kalahari", "most": "the European-derived samples"},
)

AMIR_FIRESTONE_2025 = Dataset(
    key="amir_firestone_2025",
    title="Is visual perception WEIRD?",
    source="D. Amir and C. Firestone, Is visual perception WEIRD? The Müller-Lyer illusion and the cultural byproduct "
           "hypothesis, Psychological Review (2025)",
    cite=r"Amir \& Firestone (2025)",
    checked="the authors' posted copy's summary and press coverage, " + _P14,
    licence="facts only",
    data={},
)

GAUTHIER_1999 = Dataset(
    key="gauthier_1999",
    title="Expertise with greebles recruits the face area",
    source="I. Gauthier, M. J. Tarr, A. W. Anderson, P. Skudlarski and J. C. Gore, Activation of the middle fusiform "
           "'face area' increases with expertise in recognizing novel objects, Nature Neuroscience 2 (1999) 568-573",
    cite=r"Gauthier et al.\ (1999)",
    checked="later accounts of the debate, " + _P14 + "; author list and pages from memory",
    licence="facts only",
    data={},
)

YIN_1969 = Dataset(
    key="yin_1969",
    title="Looking at upside-down faces",
    source="R. K. Yin, Looking at upside-down faces, Journal of Experimental Psychology 81 (1969) 141-145",
    cite=r"Yin (1969)",
    checked="later accounts, " + _P14,
    licence="facts only",
    data={},
)

YAMINS_2014 = Dataset(
    key="yamins_2014",
    title="Performance-optimized networks predict IT responses",
    source="D. L. K. Yamins, H. Hong, C. F. Cadieu, E. A. Solomon, D. Seibert and J. J. DiCarlo, Performance-optimized "
           "hierarchical models predict neural responses in higher visual cortex, PNAS 111 (2014) 8619-8624",
    cite=r"Yamins et al.\ (2014)",
    checked="the abstract, " + _P14,
    licence="facts only",
    data={"it_neurons": 168},
)

GEIRHOS_2019 = Dataset(
    key="geirhos_2019",
    title="ImageNet-trained networks are biased towards texture",
    source="R. Geirhos, P. Rubisch, C. Michaelis, M. Bethge, F. A. Wichmann and W. Brendel, ImageNet-trained CNNs are "
           "biased towards texture; increasing shape bias improves accuracy and robustness, ICLR (2019)",
    cite=r"Geirhos et al.\ (2019)",
    checked="the preprint's abstract, " + _P14,
    licence="facts only",
    data={},
)

VONG_2024 = Dataset(
    key="vong_2024",
    title="Learning words through one child's eyes and ears",
    source="W. K. Vong, W. Wang, A. E. Orhan and B. M. Lake, Grounded language acquisition through the eyes and ears "
           "of a single child, Science 383 (2024) 504-511; A. E. Orhan, V. V. Gupta and B. M. Lake, Self-supervised "
           "learning through the eyes of a child, NeurIPS (2020)",
    cite=r"Vong et al.\ (2024); \ Orhan et al.\ (2020)",
    checked="the abstracts and press releases, " + _P14,
    licence="facts only",
    data={"hours": 61, "ages_months": (6, 25)},
)

WHEATSTONE_1838 = Dataset(
    key="wheatstone_1838",
    title="The stereoscope",
    source="C. Wheatstone, Contributions to the physiology of vision. Part the first. On some remarkable, and hitherto "
           "unobserved, phenomena of binocular vision, Philosophical Transactions of the Royal Society 128 (1838) "
           "371-394; B. Julesz, Binocular depth perception of computer-generated patterns, Bell System Technical "
           "Journal 39 (1960) 1125-1162",
    cite=r"Wheatstone (1838); \ Julesz (1960)",
    checked="historical accounts, " + _P14 + "; Julesz's date is given as 1959 or 1960 in different sources",
    licence="public domain (Wheatstone); facts only",
    data={},
)


# ---------------------------------------------------------------------------
# Part 15
# ---------------------------------------------------------------------------
_P15 = "through a web search, 2026-11-14"

BEKESY_1960 = Dataset(
    key="bekesy_1960",
    title="The travelling wave on the basilar membrane",
    source="G. von Békésy, Experiments in Hearing (McGraw-Hill, 1960); Nobel Prize in Physiology or Medicine, 1961",
    cite=r"von Békésy (1960)",
    checked="reviews and the Nobel record, " + _P15 + "; cadaver cochleae, stroboscopic light, silver particles",
    licence="facts only",
    data={"preparation": "human temporal bones from cadavers", "finding": "a wave from base to apex, peaking at a "
          "place that depends on frequency"},
)

KEMP_1978 = Dataset(
    key="kemp_1978",
    title="Sound emitted by the ear",
    source="D. T. Kemp, Stimulated acoustic emissions from within the human auditory system, Journal of the "
           "Acoustical Society of America 64 (1978) 1386-1391",
    cite=r"Kemp (1978)",
    checked="reference lists and reviews, " + _P15,
    licence="facts only",
    data={"finding": "the cochlea emits sound: evidence for an active amplifier"},
)

LIBERMAN_1957 = Dataset(
    key="liberman_1957",
    title="Discrimination peaks at the phoneme boundary",
    source="A. M. Liberman, K. S. Harris, H. S. Hoffman and B. C. Griffith, The discrimination of speech sounds within "
           "and across phoneme boundaries, Journal of Experimental Psychology 54 (1957) 358-368",
    cite=r"Liberman et al.\ (1957)",
    checked="bibliographic records and later accounts, " + _P15,
    licence="facts only",
    data={"continuum": "synthetic syllables from /b/ through /d/ to /g/", "method": "identification and ABX"},
)

MCMURRAY_2002 = Dataset(
    key="mcmurray_2002",
    title="Gradient sensitivity within phoneme categories",
    source="B. McMurray, M. K. Tanenhaus and R. N. Aslin, Gradient effects of within-category phonetic variation on "
           "lexical access, Cognition 86 (2002) B33-B42",
    cite=r"McMurray et al.\ (2002)",
    checked="the abstract, " + _P15,
    licence="facts only",
    data={"continuum": "voice onset time, 0 to 40 ms", "measure": "fixations to pictures"},
)

MCGURK_1976 = Dataset(
    key="mcgurk_1976",
    title="Hearing lips and seeing voices",
    source="H. McGurk and J. MacDonald, Hearing lips and seeing voices, Nature 264 (1976) 746-748",
    cite=r"McGurk \& MacDonald (1976)",
    checked="later accounts, " + _P15 + "; the 98% for adults as widely reported",
    licence="facts only",
    data={"stimulus": "a voice saying ba dubbed onto lips saying ga", "adults_fused": 0.98},
)

MALLICK_2015 = Dataset(
    key="mallick_2015",
    title="Individual differences in the McGurk effect",
    source="D. B. Mallick, J. F. Magnotti and M. S. Beauchamp, Variability and stability in the McGurk effect: "
           "contributions of participants, stimuli, time, and response type, Psychonomic Bulletin & Review 22 (2015) "
           "1299-1307",
    cite=r"Mallick et al.\ (2015)",
    checked="the abstract and full text summary, " + _P15,
    licence="facts only",
    data={"range": "0% to 100% across people", "retest_r": 0.91},
)

BOTVINICK_COHEN_1998 = Dataset(
    key="botvinick_cohen_1998",
    title="The rubber hand illusion",
    source="M. Botvinick and J. Cohen, Rubber hands 'feel' touch that eyes see, Nature 391 (1998) 756",
    cite=r"Botvinick \& Cohen (1998)",
    checked="later accounts, " + _P15,
    licence="facts only",
    data={"procedure": "a hidden real hand and a visible rubber hand stroked together"},
)

LUSH_2020 = Dataset(
    key="lush_2020",
    title="Phenomenological control and the rubber hand",
    source="P. Lush, V. Botan, R. B. Scott, A. K. Seth, J. Ward and Z. Dienes, Trait phenomenological control predicts "
           "experience of mirror synaesthesia and the rubber hand illusion, Nature Communications 11 (2020) 4853",
    cite=r"Lush et al.\ (2020)",
    checked="the abstract and the authors' summaries, " + _P15,
    licence="facts only",
    data={"n": 353},
)

MELZACK_WALL_1965 = Dataset(
    key="melzack_wall_1965",
    title="The gate control theory of pain",
    source="R. Melzack and P. D. Wall, Pain mechanisms: a new theory, Science 150 (1965) 971-979",
    cite=r"Melzack \& Wall (1965)",
    checked="later accounts, " + _P15,
    licence="facts only",
    data={},
)

LEVINE_1978 = Dataset(
    key="levine_1978",
    title="Naloxone and placebo analgesia",
    source="J. D. Levine, N. C. Gordon and H. L. Fields, The mechanism of placebo analgesia, Lancet 2 (1978) 654-657",
    cite=r"Levine, Gordon \& Fields (1978)",
    checked="the abstract, " + _P15,
    licence="facts only",
    data={"setting": "after extraction of impacted wisdom teeth", "finding": "naloxone raised pain in placebo responders"},
)

HANIG_1901 = Dataset(
    key="hanig_1901",
    title="Taste sensitivity across the tongue, and the map it became",
    source="D. P. Hänig, Zur Psychophysik des Geschmackssinnes, Philosophische Studien 17 (1901) 576-623; E. G. "
           "Boring, Sensation and Perception in the History of Experimental Psychology (1942); V. B. Collings, Human "
           "taste response as a function of locus of stimulation on the tongue and soft palate, Perception & "
           "Psychophysics 16 (1974) 169-174",
    cite=r"Hänig (1901); \ Collings (1974)",
    checked="later accounts, " + _P15 + "; journal pages from memory",
    licence="facts only",
    data={},
)

BUSHDID_2014 = Dataset(
    key="bushdid_2014",
    title="A trillion odours, and the reanalyses",
    source="C. Bushdid, M. O. Magnasco, L. B. Vosshall and A. Keller, Humans can discriminate more than 1 trillion "
           "olfactory stimuli, Science 343 (2014) 1370-1372; R. C. Gerkin and J. B. Castro, The number of olfactory "
           "stimuli that humans can discriminate is still unknown, eLife 4 (2015) e08127; M. Meister, On the "
           "dimensionality of odor space, eLife 4 (2015) e07865",
    cite=r"Bushdid et al.\ (2014); \ Gerkin \& Castro (2015); \ Meister (2015)",
    checked="the abstracts, " + _P15,
    licence="facts only",
    data={"mixtures": "of 10, 20 or 30 from 128 odorants", "claim": 1.72e12},
)

MCDERMOTT_2016 = Dataset(
    key="mcdermott_2016",
    title="Indifference to dissonance among the Tsimane'",
    source="J. H. McDermott, A. F. Schultz, E. A. Undurraga and R. A. Godoy, Indifference to dissonance in native "
           "Amazonians reveals cultural variation in music perception, Nature 535 (2016) 547-550",
    cite=r"McDermott et al.\ (2016)",
    checked="the abstract and press accounts, " + _P15,
    licence="facts only",
    data={"finding": "consonant and dissonant chords rated equally pleasant; roughness still disliked"},
)

KUJAWA_LIBERMAN_2009 = Dataset(
    key="kujawa_liberman_2009",
    title="Hidden hearing loss in mice",
    source="S. G. Kujawa and M. C. Liberman, Adding insult to injury: cochlear nerve degeneration after 'temporary' "
           "noise-induced hearing loss, Journal of Neuroscience 29 (2009) 14077-14085",
    cite=r"Kujawa \& Liberman (2009)",
    checked="reviews by the authors, " + _P15,
    licence="facts only",
    data={"exposure": "2 h of 8-16 kHz noise at 100 dB SPL", "finding": "thresholds recover; synapses do not"},
)

_P16 = "through a web search, 2026-11-14"

PAVLOV_1927 = Dataset(
    key="pavlov_1927",
    title="Conditioned reflexes in Pavlov's laboratory",
    source='I. P. Pavlov, Conditioned Reflexes: An Investigation of the Physiological Activity of the Cerebral Cortex, trans. G. V. Anrep (Oxford University Press, 1927); D. P. Todes, Ivan Pavlov: A Russian Life in Science (Oxford University Press, 2014)',
    cite=r"Pavlov (1927)",
    checked="Todes's biography as summarized by its publisher and reviewers, " + _P16,
    licence="public domain (Pavlov's text); facts only",
    data={"nobel": 1904, "stimuli": "metronomes, buzzers, harmoniums, lights, touches; a bell rarely", "measure": "drops of saliva through a fistula"},
)

THORNDIKE_1898 = Dataset(
    key="thorndike_1898",
    title='Cats in puzzle boxes and the law of effect',
    source='E. L. Thorndike, Animal intelligence: an experimental study of the associative processes in animals, Psychological Review Monograph Supplements 2(4) (1898)',
    cite=r"Thorndike (1898)",
    checked='historical accounts, ' + _P16,
    licence='public domain',
    data={"animals": "cats, dogs and chicks", "measure": "seconds to escape, trial by trial"},
)

WATSON_RAYNER_1920 = Dataset(
    key="watson_rayner_1920",
    title='Little Albert',
    source='J. B. Watson and R. Rayner, Conditioned emotional reactions, Journal of Experimental Psychology 3 (1920) 1-14',
    cite=r"Watson \& Rayner (1920)",
    checked='the full text at Classics in the History of Psychology (York University), read 2026-11-14; ' + _P16,
    licence='public domain',
    data={"baseline": "about nine months (loud sound tested at 8 months 26 days)", "first_pairings": "11 months 3 days: two", "total_pairings": 7, "transfer_test": "11 months 15 days: rabbit, dog, seal fur coat, cotton wool, Santa Claus mask", "last_test": "1 year 21 days", "deconditioning": "none: Albert was taken from the hospital the day of the last tests"},
)

HARRIS_1979 = Dataset(
    key="harris_1979",
    title='How Little Albert was retold',
    source="B. Harris, Whatever happened to Little Albert?, American Psychologist 34 (1979) 151-160; R. A. Powell, N. Digdon, B. Harris and C. Smithson, Correcting the record on Watson, Rayner, and Little Albert: Albert Barger as 'psychology's lost boy', American Psychologist 69 (2014) 600-611",
    cite=r"Harris (1979); \ Powell et al.\ (2014)",
    checked='bibliographic records and summaries, ' + _P16,
    licence='facts only',
    data={"identity": "Douglas Merritte (Beck et al. 2009) or Albert Barger (Powell et al. 2014): disputed"},
)

FERSTER_SKINNER_1957 = Dataset(
    key="ferster_skinner_1957",
    title='Schedules of reinforcement',
    source='B. F. Skinner, The Behavior of Organisms (Appleton-Century, 1938); C. B. Ferster and B. F. Skinner, Schedules of Reinforcement (Appleton-Century-Crofts, 1957)',
    cite=r"Skinner (1938); \ Ferster \& Skinner (1957)",
    checked='from memory and textbook accounts, ' + _P16,
    licence='facts only',
    data={"schedules": "FR, VR, FI, VI"},
)

RESCORLA_1968 = Dataset(
    key="rescorla_1968",
    title='Contingency, not pairing',
    source='R. A. Rescorla, Probability of shock in the presence and absence of CS in fear conditioning, Journal of Comparative and Physiological Psychology 66 (1968) 1-5',
    cite=r"Rescorla (1968)",
    checked='the full text (a course copy), read 2026-11-14; ' + _P16,
    licence='facts only',
    data={"exp1_rats": 24, "exp2_rats": 80, "exp2_groups": 10, "tones_per_session": 12, "tone_s": 120, "mean_gap_min": 8, "sessions": 5, "shock": "0.5 s, 0.9 mA", "groups": [[0.4,0.4],[0.2,0.2],[0.1,0.1],[0.0,0.0],[0.4,0.2],[0.4,0.1],[0.4,0.0],[0.2,0.1],[0.2,0.0],[0.1,0.0]], "measure": "suppression ratio A/(A+B)"},
)

WASSERMAN_1993 = Dataset(
    key="wasserman_1993",
    title='Ratings of causal relations follow the contingency',
    source='E. A. Wasserman, S. M. Elek, D. L. Chatlosh and A. G. Baker, Rating causal relations: role of probability in judgments of response-outcome contingency, Journal of Experimental Psychology: Learning, Memory, and Cognition 19 (1993) 174-188',
    cite=r"Wasserman et al.\ (1993)",
    checked='the abstract, ' + _P16,
    licence='facts only',
    data={"people": 150, "experiments": 3, "task": "tapping a telegraph key, a light that may flash"},
)

KAMIN_1969 = Dataset(
    key="kamin_1969",
    title='Blocking',
    source='L. J. Kamin, Predictability, surprise, attention, and conditioning, in B. A. Campbell and R. M. Church (eds), Punishment and Aversive Behavior (Appleton-Century-Crofts, 1969) 279-296',
    cite=r"Kamin (1969)",
    checked='later accounts of the design, ' + _P16,
    licence='facts only',
    data={"design": "noise+shock, then noise-and-light+shock; test the light", "measure": "suppression ratio"},
)

MAES_2016 = Dataset(
    key="maes_2016",
    title='Fifteen failures to find blocking',
    source="T. Maes, Y. Boddez, J. M. Alfei, A.-M. Krypotos, R. D'Hooge, J. De Houwer and T. Beckers, The elusive nature of the blocking effect: 15 failures to replicate, Journal of Experimental Psychology: General 145 (2016) e49-e71",
    cite=r"Maes et al.\ (2016)",
    checked='the abstract, the comment by Soto and the reply, ' + _P16,
    licence='facts only',
    data={"experiments": 15},
)

RESCORLA_WAGNER_1972 = Dataset(
    key="rescorla_wagner_1972",
    title='The Rescorla-Wagner model',
    source='R. A. Rescorla and A. R. Wagner, A theory of Pavlovian conditioning: variations in the effectiveness of reinforcement and nonreinforcement, in A. H. Black and W. F. Prokasy (eds), Classical Conditioning II (Appleton-Century-Crofts, 1972) 64-99',
    cite=r"Rescorla \& Wagner (1972)",
    checked='from memory and textbook accounts, ' + _P16,
    licence='facts only',
    data={"rule": "dV = alpha beta (lambda - sum V)"},
)

LUBOW_MOORE_1959 = Dataset(
    key="lubow_moore_1959",
    title='Latent inhibition',
    source='R. E. Lubow and A. U. Moore, Latent inhibition: the effect of nonreinforced pre-exposure to the conditional stimulus, Journal of Comparative and Physiological Psychology 52 (1959) 415-419',
    cite=r"Lubow \& Moore (1959)",
    checked="a review's account of the design, " + _P16,
    licence='facts only',
    data={"animals": "sheep and goats", "response": "leg flexion"},
)

BOUTON_BOLLES_1979 = Dataset(
    key="bouton_bolles_1979",
    title='Renewal: extinction is bound to its context',
    source='M. E. Bouton and R. C. Bolles, Contextual control of the extinction of conditioned fear, Learning and Motivation 10 (1979) 445-466; B. Vervliet, M. G. Craske and D. Hermans, Fear extinction and relapse: state of the art, Annual Review of Clinical Psychology 9 (2013) 215-248',
    cite=r"Bouton \& Bolles (1979)",
    checked='the abstract and later reviews, ' + _P16,
    licence='facts only',
    data={"design": "conditioning in A, extinction in B, test in A"},
)

MACKINTOSH_PEARCE_HALL = Dataset(
    key="mackintosh_pearce_hall",
    title='Two theories of attention in learning',
    source='N. J. Mackintosh, A theory of attention: variations in the associability of stimuli with reinforcement, Psychological Review 82 (1975) 276-298; J. M. Pearce and G. Hall, A model for Pavlovian learning: variations in the effectiveness of conditioned but not of unconditioned stimuli, Psychological Review 87 (1980) 532-552; M. E. Le Pelley, The role of associative history in models of associative learning, Quarterly Journal of Experimental Psychology 57B (2004) 193-243',
    cite=r"Mackintosh (1975); \ Pearce \& Hall (1980)",
    checked='from memory and textbook accounts, ' + _P16,
    licence='facts only',
    data={},
)

GALLISTEL_GIBBON_2000 = Dataset(
    key="gallistel_gibbon_2000",
    title='Time, rate and conditioning',
    source='C. R. Gallistel and J. Gibbon, Time, rate, and conditioning, Psychological Review 107 (2000) 289-344; J. Gibbon and P. Balsam, Spreading associations in time, in C. M. Locurto, H. S. Terrace and J. Gibbon (eds), Autoshaping and Conditioning Theory (Academic Press, 1981)',
    cite=r"Gallistel \& Gibbon (2000)",
    checked='accounts of the result by Kakade and Dayan and later papers, ' + _P16,
    licence='facts only',
    data={"rule": "reinforcements to acquisition about 300 (I/T)^-1"},
)

HERRNSTEIN_1961 = Dataset(
    key="herrnstein_1961",
    title='The matching law',
    source='R. J. Herrnstein, Relative and absolute strength of response as a function of frequency of reinforcement, Journal of the Experimental Analysis of Behavior 4 (1961) 267-272; W. M. Baum, Matching, undermatching, and overmatching in studies of choice, Journal of the Experimental Analysis of Behavior 32 (1979) 269-281; R. J. Herrnstein and D. Prelec, Melioration: a theory of distributed choice, Journal of Economic Perspectives 5 (1991) 137-156',
    cite=r"Herrnstein (1961); \ Baum (1979)",
    checked='bibliographic records and later reviews, ' + _P16,
    licence='facts only',
    data={"baum_datasets": 103, "baum_studies": 23},
)

GARCIA_KOELLING_1966 = Dataset(
    key="garcia_koelling_1966",
    title='Taste aversion: cue to consequence, and long delays',
    source='J. Garcia and R. A. Koelling, Relation of cue to consequence in avoidance learning, Psychonomic Science 4 (1966) 123-124; J. Garcia, F. R. Ervin and R. A. Koelling, Learning with prolonged delay of reinforcement, Psychonomic Science 5 (1966) 121-122; M. Domjan and N. E. Wilson, Specificity of cue to consequence in aversion learning in the rat, Psychonomic Science 26 (1972) 143-145',
    cite=r"Garcia \& Koelling (1966)",
    checked="the publisher's record and later accounts, " + _P16,
    licence='facts only',
    data={"design": "bright-noisy-tasty water; shock or illness (X-rays, lithium chloride)"},
)

BRELAND_1961 = Dataset(
    key="breland_1961",
    title='The misbehavior of organisms',
    source='K. Breland and M. Breland, The misbehavior of organisms, American Psychologist 16 (1961) 681-684',
    cite=r"Breland \& Breland (1961)",
    checked='later accounts and excerpts, ' + _P16,
    licence='facts only',
    data={"cases": "a raccoon rubbing coins, pigs rooting tokens"},
)

BANDURA_1961 = Dataset(
    key="bandura_1961",
    title='Learning by watching: the Bobo doll',
    source='A. Bandura, D. Ross and S. A. Ross, Transmission of aggression through imitation of aggressive models, Journal of Abnormal and Social Psychology 63 (1961) 575-582',
    cite=r"Bandura, Ross \& Ross (1961)",
    checked="the paper's first page and later accounts, " + _P16,
    licence='facts only',
    data={"children": 72, "boys": 36, "girls": 36, "school": "Stanford University nursery school"},
)

PRENDERGAST_2006 = Dataset(
    key="prendergast_2006",
    title='Contingency management for drug use',
    source='M. Prendergast, D. Podus, J. Finney, L. Greenwell and J. Roll, Contingency management for treatment of substance use disorders: a meta-analysis, Addiction 101 (2006) 1546-1560; L. A. Benishek et al., Prize-based contingency management for the treatment of substance abusers: a meta-analysis, Addiction 109 (2014) 1426-1436',
    cite=r"Prendergast et al.\ (2006)",
    checked='the abstracts, ' + _P16,
    licence='facts only',
    data={"comparisons": 47, "d": 0.42, "d_opiates": 0.65, "d_cocaine": 0.66, "prize_end": 0.46, "prize_3mo": 0.33},
)

ZENDLE_CAIRNS_2018 = Dataset(
    key="zendle_cairns_2018",
    title='Loot boxes and problem gambling',
    source='D. Zendle and P. Cairns, Video game loot boxes are linked to problem gambling: results of a large-scale survey, PLoS ONE 13 (2018) e0206767; D. Zendle and P. Cairns, Loot boxes are again linked to problem gambling, PLoS ONE 14 (2019) e0213194',
    cite=r"Zendle \& Cairns (2018)",
    checked="the abstract and the university's release, " + _P16,
    licence='facts only (CC BY article)',
    data={"gamers": 7422, "eta2_loot": 0.054, "eta2_other": 0.004},
)

GERSHMAN_2010 = Dataset(
    key="gershman_2010",
    title='Latent causes and extinction',
    source='S. J. Gershman, D. M. Blei and Y. Niv, Context, learning, and extinction, Psychological Review 117 (2010) 197-209; C. J. Mitchell, J. De Houwer and P. F. Lovibond, The propositional nature of human associative learning, Behavioral and Brain Sciences 32 (2009) 183-198',
    cite=r"Gershman, Blei \& Niv (2010)",
    checked='the abstracts, ' + _P16,
    licence='facts only',
    data={},
)

MITCHELL_2009 = Dataset(
    key="mitchell_2009",
    title="Human associative learning as propositional reasoning",
    source="C. J. Mitchell, J. De Houwer and P. F. Lovibond, The propositional nature of human associative learning, "
           "Behavioral and Brain Sciences 32 (2009) 183-198",
    cite=r"Mitchell, \ De Houwer \& Lovibond (2009)",
    checked="the abstract and commentaries, " + _P16,
    licence="facts only",
    data={},
)

SCHILLER_2010 = Dataset(
    key="schiller_2010",
    title="Extinction during reconsolidation",
    source="D. Schiller, M.-H. Monfils, C. M. Raio, D. C. Johnson, J. E. LeDoux and E. A. Phelps, Preventing the return "
           "of fear in humans using reconsolidation update mechanisms, Nature 463 (2010) 49-53",
    cite=r"Schiller et al.\ (2010)",
    checked="from memory and later reviews, " + _P16,
    licence="facts only",
    data={"follow_up": "about a year, in a subset"},
)

_P17 = "through a web search, 2026-11-14"

SCHULTZ_1997 = Dataset(
    key="schultz_1997",
    title='Dopamine neurons and the temporal-difference error',
    source='W. Schultz, P. Dayan and P. R. Montague, A neural substrate of prediction and reward, Science 275 (1997) 1593-1599',
    cite=r"Schultz, Dayan \& Montague (1997)",
    checked='from memory and later reviews, ' + _P17,
    licence="facts only",
    data={},
)

STEINBERG_2013 = Dataset(
    key="steinberg_2013",
    title='An artificial prediction error teaches',
    source='E. E. Steinberg, R. Keiflin, J. R. Boivin, I. B. Witten, K. Deisseroth and P. H. Janak, A causal link between prediction errors, dopamine neurons and learning, Nature Neuroscience 16 (2013) 966-973',
    cite=r"Steinberg et al.\ (2013)",
    checked='the abstract and commentaries, ' + _P17,
    licence="facts only",
    data={"design": "blocking and extinction in rats, with optogenetic stimulation of dopamine neurons"},
)

FRANK_2004 = Dataset(
    key="frank_2004",
    title="Learning from reward and punishment in Parkinson's disease",
    source="M. J. Frank, L. C. Seeberger and R. C. O'Reilly, By carrot or by stick: cognitive reinforcement learning in parkinsonism, Science 306 (2004) 1940-1943",
    cite=r"Frank, Seeberger \& O'Reilly (2004)",
    checked='the abstract and later reviews, ' + _P17,
    licence="facts only",
    data={},
)

WILSON_2014 = Dataset(
    key="wilson_2014",
    title='Directed and random exploration',
    source='R. C. Wilson, A. Geana, J. M. White, E. A. Ludvig and J. D. Cohen, Humans use directed and random exploration to solve the explore-exploit dilemma, Journal of Experimental Psychology: General 143 (2014) 2074-2081',
    cite=r"Wilson et al.\ (2014)",
    checked='from memory and later reviews, ' + _P17,
    licence="facts only",
    data={"horizons": [1, 6]},
)

TOLMAN_HONZIK_1930 = Dataset(
    key="tolman_honzik_1930",
    title='Latent learning in the maze',
    source='E. C. Tolman and C. H. Honzik, Introduction and removal of reward, and maze performance in rats, University of California Publications in Psychology 4 (1930) 257-275; D. Thistlethwaite, A critical review of latent learning and related experiments, Psychological Bulletin 48 (1951) 97-129',
    cite=r"Tolman \& Honzik (1930)",
    checked='textbook accounts and a review of the design, ' + _P17,
    licence="facts only",
    data={"groups": "fed daily; never fed; fed from day 11"},
)

TOLMAN_1948 = Dataset(
    key="tolman_1948",
    title='Cognitive maps',
    source='E. C. Tolman, Cognitive maps in rats and men, Psychological Review 55 (1948) 189-208',
    cite=r"Tolman (1948)",
    checked='from memory, ' + _P17,
    licence="facts only",
    data={},
)

HAFTING_2005 = Dataset(
    key="hafting_2005",
    title='Place cells and grid cells',
    source="J. O'Keefe and J. Dostrovsky, The hippocampus as a spatial map, Brain Research 34 (1971) 171-175; T. Hafting, M. Fyhn, S. Molden, M.-B. Moser and E. I. Moser, Microstructure of a spatial map in the entorhinal cortex, Nature 436 (2005) 801-806; C. F. Doeller, C. Barry and N. Burgess, Evidence for grid cells in a human memory network, Nature 463 (2010) 657-661",
    cite=r"O'Keefe \& Dostrovsky (1971); \ Hafting et al.\ (2005)",
    checked='from memory and the Nobel record, ' + _P17,
    licence="facts only",
    data={"nobel": 2014},
)

ADAMS_DICKINSON_1981 = Dataset(
    key="adams_dickinson_1981",
    title='Devaluation, and habits after overtraining',
    source='C. D. Adams and A. Dickinson, Instrumental responding following reinforcer devaluation, Quarterly Journal of Experimental Psychology 33B (1981) 109-121; C. D. Adams, Variations in the sensitivity of instrumental responding to reinforcer devaluation, Quarterly Journal of Experimental Psychology 34B (1982) 77-98',
    cite=r"Adams \& Dickinson (1981); \ Adams (1982)",
    checked='reviews of the method, ' + _P17,
    licence="facts only",
    data={},
)

DAW_2011 = Dataset(
    key="daw_2011",
    title='The two-step task',
    source="N. D. Daw, S. J. Gershman, B. Seymour, P. Dayan and R. J. Dolan, Model-based influences on humans' choices and striatal prediction errors, Neuron 69 (2011) 1204-1215",
    cite=r"Daw et al.\ (2011)",
    checked='the abstract, ' + _P17,
    licence="facts only",
    data={"participants": 17, "common": 0.7},
)

FEHER_DA_SILVA_2020 = Dataset(
    key="feher_da_silva_2020",
    title='The two-step task, explained carefully',
    source='C. Feher da Silva and T. A. Hare, Humans primarily use model-based inference in the two-stage task, Nature Human Behaviour 4 (2020) 1053-1066; T. Akam, R. Costa and P. Dayan, Simple plans or sophisticated habits?, PLoS Computational Biology 11 (2015) e1004648',
    cite=r"Feher da Silva \& Hare (2020)",
    checked='from memory and later reviews, ' + _P17,
    licence="facts only",
    data={},
)

MOMENNEJAD_2017 = Dataset(
    key="momennejad_2017",
    title='The successor representation in people',
    source='I. Momennejad, E. M. Russek, J. H. Cheong, M. M. Botvinick, N. D. Daw and S. J. Gershman, The successor representation in human reinforcement learning, Nature Human Behaviour 1 (2017) 680-692; P. Dayan, Improving generalization for temporal difference learning: the successor representation, Neural Computation 5 (1993) 613-624',
    cite=r"Momennejad et al.\ (2017)",
    checked='the abstract and a later modelling paper, ' + _P17,
    licence="facts only",
    data={},
)

HOWE_2013 = Dataset(
    key="howe_2013",
    title='Dopamine ramps',
    source='M. W. Howe, P. L. Tierney, S. G. Sandberg, P. E. M. Phillips and A. M. Graybiel, Prolonged dopamine signalling in striatum signals proximity and value of distant rewards, Nature 500 (2013) 575-579',
    cite=r"Howe et al.\ (2013)",
    checked='from memory and later reviews, ' + _P17,
    licence="facts only",
    data={},
)

DABNEY_2020 = Dataset(
    key="dabney_2020",
    title='A distributional code in dopamine neurons',
    source='W. Dabney, Z. Kurth-Nelson, N. Uchida, C. K. Starkweather, D. Hassabis, R. Munos and M. Botvinick, A distributional code for value in dopamine-based reinforcement learning, Nature 577 (2020) 671-675',
    cite=r"Dabney et al.\ (2020)",
    checked='the abstract and later replications, ' + _P17,
    licence="facts only",
    data={},
)

REDISH_2004 = Dataset(
    key="redish_2004",
    title='Addiction as a computational process gone awry',
    source='A. D. Redish, Addiction as a computational process gone awry, Science 306 (2004) 1944-1947',
    cite=r"Redish (2004)",
    checked='from memory, ' + _P17,
    licence="facts only",
    data={},
)

LI_2010 = Dataset(
    key="li_2010",
    title='A contextual bandit for news',
    source='L. Li, W. Chu, J. Langford and R. E. Schapire, A contextual-bandit approach to personalized news article recommendation, Proceedings of WWW (2010) 661-670',
    cite=r"Li et al.\ (2010)",
    checked='from memory, ' + _P17,
    licence="facts only",
    data={},
)

WEINTRAUB_2010 = Dataset(
    key="weintraub_2010",
    title="Impulse-control disorders in Parkinson's disease",
    source='D. Weintraub et al., Impulse control disorders in Parkinson disease: a cross-sectional study of 3090 patients, Archives of Neurology 67 (2010) 589-595',
    cite=r"Weintraub et al.\ (2010)",
    checked='the record and secondary summaries, ' + _P17,
    licence="facts only",
    data={"patients": 3090, "any": 13.6, "agonist": 17.1, "levodopa": 6.9},
)

WANG_2018 = Dataset(
    key="wang_2018",
    title='Prefrontal cortex as a meta-reinforcement-learning system',
    source='J. X. Wang, Z. Kurth-Nelson, D. Kumaran, D. Tirumala, H. Soyer, J. Z. Leibo, D. Hassabis and M. Botvinick, Prefrontal cortex as a meta-reinforcement learning system, Nature Neuroscience 21 (2018) 860-868; H. F. Harlow, The formation of learning sets, Psychological Review 56 (1949) 51-65',
    cite=r"Wang et al.\ (2018)",
    checked='from memory, ' + _P17,
    licence="facts only",
    data={},
)


_P18 = "through a web search, 2026-11-14"

SIMONS_CHABRIS_1999 = Dataset(
    key="simons_chabris_1999",
    title='Gorillas in our midst',
    source='D. J. Simons and C. F. Chabris, Gorillas in our midst: sustained inattentional blindness for dynamic events, Perception 28 (1999) 1059-1074',
    cite=r"Simons \& Chabris (1999)",
    checked='secondary summaries' + ", " + _P18,
    licence="facts only",
    data={'observers': 192, 'missed': 0.46},
)

RENSINK_1997 = Dataset(
    key="rensink_1997",
    title='Change blindness in the flicker paradigm',
    source="R. A. Rensink, J. K. O'Regan and J. J. Clark, To see or not to see: the need for attention to perceive changes in scenes, Psychological Science 8 (1997) 368-373",
    cite=r"Rensink, O'Regan \& Clark (1997)",
    checked='the paper read in full' + ", " + _P18,
    licence="facts only",
    data={'observers': 10, 'scenes': 48, 'image_ms': 240, 'blank_ms': 80, 'mi_alternations': 17.1, 'mi_seconds': 10.9, 'ci_alternations': 7.3, 'ci_seconds': 4.7, 'no_blank_alternations': 1.4, 'no_blank_seconds': 0.9},
)

CHERRY_1953 = Dataset(
    key="cherry_1953",
    title='The cocktail party problem',
    source='E. C. Cherry, Some experiments on the recognition of speech, with one and with two ears, Journal of the Acoustical Society of America 25 (1953) 975-979',
    cite=r"Cherry (1953)",
    checked='from memory and reviews' + ", " + _P18,
    licence="facts only",
    data={},
)

BROADBENT_1958 = Dataset(
    key="broadbent_1958",
    title='The filter',
    source='D. E. Broadbent, Perception and Communication, Pergamon Press (1958)',
    cite=r"Broadbent (1958)",
    checked='from memory and reviews' + ", " + _P18,
    licence="facts only",
    data={},
)

MORAY_1959 = Dataset(
    key="moray_1959",
    title="One's own name in the unattended ear",
    source='N. Moray, Attention in dichotic listening: affective cues and the influence of instructions, Quarterly Journal of Experimental Psychology 11 (1959) 56-60; N. L. Wood and N. Cowan, The cocktail party phenomenon revisited, Journal of Experimental Psychology: Learning, Memory, and Cognition 21 (1995) 255-260',
    cite=r"Moray (1959)",
    checked='secondary summaries' + ", " + _P18,
    licence="facts only",
    data={'own_name_share': 0.33},
)

TREISMAN_1960 = Dataset(
    key="treisman_1960",
    title='Attenuation, and late selection',
    source='A. M. Treisman, Contextual cues in selective listening, Quarterly Journal of Experimental Psychology 12 (1960) 242-248; J. A. Deutsch and D. Deutsch, Attention: some theoretical considerations, Psychological Review 70 (1963) 80-90',
    cite=r"Treisman (1960); \ Deutsch \& Deutsch (1963)",
    checked='from memory and reviews' + ", " + _P18,
    licence="facts only",
    data={},
)

LAVIE_1995 = Dataset(
    key="lavie_1995",
    title='Perceptual load',
    source='N. Lavie, Perceptual load as a necessary condition for selective attention, Journal of Experimental Psychology: Human Perception and Performance 21 (1995) 451-468',
    cite=r"Lavie (1995)",
    checked='secondary summaries' + ", " + _P18,
    licence="facts only",
    data={},
)

POSNER_1980 = Dataset(
    key="posner_1980",
    title='Orienting of attention',
    source='M. I. Posner, Orienting of attention, Quarterly Journal of Experimental Psychology 32 (1980) 3-25; M. I. Posner and Y. Cohen, Components of visual orienting, in Attention and Performance X (1984) 531-556',
    cite=r"Posner (1980)",
    checked='secondary summaries' + ", " + _P18,
    licence="facts only",
    data={'valid_share': 0.8},
)

TREISMAN_GELADE_1980 = Dataset(
    key="treisman_gelade_1980",
    title='Feature integration theory',
    source='A. M. Treisman and G. Gelade, A feature-integration theory of attention, Cognitive Psychology 12 (1980) 97-136; H. Pashler, Detecting conjunctions of color and form, Perception & Psychophysics 41 (1987) 191-201',
    cite=r"Treisman \& Gelade (1980)",
    checked="a lecture reproduction of Experiment 1's slopes" + ", " + _P18,
    licence="facts only",
    data={'conjunction_present_ms_per_item': 29, 'conjunction_absent_ms_per_item': 67},
)

WOLFE_2021 = Dataset(
    key="wolfe_2021",
    title='Guided search',
    source='J. M. Wolfe, K. R. Cave and S. L. Franzel, Guided search, Journal of Experimental Psychology: Human Perception and Performance 15 (1989) 419-433; J. M. Wolfe, Guided Search 6.0, Psychonomic Bulletin & Review 28 (2021) 1060-1092',
    cite=r"Wolfe (1989, 2021)",
    checked='from memory and reviews' + ", " + _P18,
    licence="facts only",
    data={},
)

ITTI_KOCH_1998 = Dataset(
    key="itti_koch_1998",
    title='A saliency map',
    source='L. Itti, C. Koch and E. Niebur, A model of saliency-based visual attention for rapid scene analysis, IEEE Transactions on Pattern Analysis and Machine Intelligence 20 (1998) 1254-1259',
    cite=r"Itti, Koch \& Niebur (1998)",
    checked='from memory' + ", " + _P18,
    licence="facts only",
    data={},
)

DREW_2013 = Dataset(
    key="drew_2013",
    title='Radiologists and the gorilla',
    source='T. Drew, M. L.-H. Vo and J. M. Wolfe, The invisible gorilla strikes again: sustained inattentional blindness in expert observers, Psychological Science 24 (2013) 1848-1853',
    cite=r"Drew, V\~o \& Wolfe (2013)",
    checked='press coverage and the abstract' + ", " + _P18,
    licence="facts only",
    data={'radiologists': 24, 'missed': 20, 'size_vs_nodule': 48},
)

RAYMOND_1992 = Dataset(
    key="raymond_1992",
    title='The attentional blink',
    source='J. E. Raymond, K. L. Shapiro and K. M. Arnell, Temporary suppression of visual processing in an RSVP task: an attentional blink?, Journal of Experimental Psychology: Human Perception and Performance 18 (1992) 849-860',
    cite=r"Raymond, Shapiro \& Arnell (1992)",
    checked='the abstract and secondary summaries' + ", " + _P18,
    licence="facts only",
    data={'window_start_ms': 180, 'window_end_ms': 450},
)

PASHLER_1994 = Dataset(
    key="pashler_1994",
    title='The psychological refractory period',
    source='H. Pashler, Dual-task interference in simple tasks: data and theory, Psychological Bulletin 116 (1994) 220-244',
    cite=r"Pashler (1994)",
    checked='secondary summaries' + ", " + _P18,
    licence="facts only",
    data={},
)

STROOP_1935 = Dataset(
    key="stroop_1935",
    title='The Stroop effect',
    source='J. R. Stroop, Studies of interference in serial verbal reactions, Journal of Experimental Psychology 18 (1935) 643-662; C. M. MacLeod, Half a century of research on the Stroop effect: an integrative review, Psychological Bulletin 109 (1991) 163-203',
    cite=r"Stroop (1935)",
    checked="secondary summaries and MacLeod's review" + ", " + _P18,
    licence="facts only",
    data={'items': 100, 'extra_seconds': 47.0, 'extra_percent': 74.3},
)

ERIKSEN_1974 = Dataset(
    key="eriksen_1974",
    title='The flanker task',
    source='B. A. Eriksen and C. W. Eriksen, Effects of noise letters upon the identification of a target letter in a nonsearch task, Perception & Psychophysics 16 (1974) 143-149',
    cite=r"Eriksen \& Eriksen (1974)",
    checked='from memory' + ", " + _P18,
    licence="facts only",
    data={},
)

BOTVINICK_2001 = Dataset(
    key="botvinick_2001",
    title='Conflict monitoring',
    source='M. M. Botvinick, T. S. Braver, D. M. Barch, C. S. Carter and J. D. Cohen, Conflict monitoring and cognitive control, Psychological Review 108 (2001) 624-652; G. Gratton, M. G. H. Coles and E. Donchin, Optimizing the use of information, Journal of Experimental Psychology: General 121 (1992) 480-506',
    cite=r"Botvinick et al.\ (2001)",
    checked='from memory' + ", " + _P18,
    licence="facts only",
    data={},
)

ROGERS_MONSELL_1995 = Dataset(
    key="rogers_monsell_1995",
    title='Task switching',
    source='R. D. Rogers and S. Monsell, Costs of a predictable switch between simple cognitive tasks, Journal of Experimental Psychology: General 124 (1995) 207-231',
    cite=r"Rogers \& Monsell (1995)",
    checked='secondary summaries' + ", " + _P18,
    licence="facts only",
    data={},
)

MORAN_DESIMONE_1985 = Dataset(
    key="moran_desimone_1985",
    title='Attention gates V4',
    source='J. Moran and R. Desimone, Selective attention gates visual processing in the extrastriate cortex, Science 229 (1985) 782-784; R. Desimone and J. Duncan, Neural mechanisms of selective visual attention, Annual Review of Neuroscience 18 (1995) 193-222',
    cite=r"Moran \& Desimone (1985)",
    checked='secondary summaries' + ", " + _P18,
    licence="facts only",
    data={},
)

REYNOLDS_HEEGER_2009 = Dataset(
    key="reynolds_heeger_2009",
    title='The normalization model of attention',
    source='J. H. Reynolds and D. J. Heeger, The normalization model of attention, Neuron 61 (2009) 168-185; K. Herrmann, L. Montaser-Kouhsari, M. Carrasco and D. J. Heeger, When size matters: attention affects performance by contrast or response gain, Nature Neuroscience 13 (2010) 1554-1559',
    cite=r"Reynolds \& Heeger (2009)",
    checked="the model from the paper's equations; the test from its abstract" + ", " + _P18,
    licence="facts only",
    data={},
)

BUNDESEN_1990 = Dataset(
    key="bundesen_1990",
    title='A theory of visual attention',
    source='C. Bundesen, A theory of visual attention, Psychological Review 97 (1990) 523-547',
    cite=r"Bundesen (1990)",
    checked='from memory' + ", " + _P18,
    licence="facts only",
    data={},
)

STRAYER_2001 = Dataset(
    key="strayer_2001",
    title='Driving and talking on a phone',
    source='D. L. Strayer and W. A. Johnston, Driven to distraction: dual-task studies of simulated driving and conversing on a cellular telephone, Psychological Science 12 (2001) 462-466',
    cite=r"Strayer \& Johnston (2001)",
    checked='the paper read in full' + ", " + _P18,
    licence="facts only",
    data={'participants': 48},
)

OPHIR_2009 = Dataset(
    key="ophir_2009",
    title='Media multitasking',
    source='E. Ophir, C. Nass and A. D. Wagner, Cognitive control in media multitaskers, PNAS 106 (2009) 15583-15587; R. Wiradhany and M. R. Nieuwenstein, Cognitive control in media multitaskers: two replication studies and a meta-analysis, Attention, Perception, & Psychophysics 79 (2017) 2620-2641',
    cite=r"Ophir, Nass \& Wagner (2009)",
    checked="the replication's abstract and secondary summaries" + ", " + _P18,
    licence="facts only",
    data={'replication_tests': 14, 'replication_significant': 5, 'meta_tests': 39, 'meta_studies': 12, 'meta_d': 0.17},
)

ANDERSON_2011 = Dataset(
    key="anderson_2011",
    title='Value-driven attentional capture',
    source='B. A. Anderson, P. A. Laurent and S. Yantis, Value-driven attentional capture, PNAS 108 (2011) 10367-10371',
    cite=r"Anderson, Laurent \& Yantis (2011)",
    checked='the abstract and the record' + ", " + _P18,
    licence="facts only",
    data={},
)

AWH_2012 = Dataset(
    key="awh_2012",
    title='Selection history',
    source='E. Awh, A. V. Belopolsky and J. Theeuwes, Top-down versus bottom-up attentional control: a failed theoretical dichotomy, Trends in Cognitive Sciences 16 (2012) 437-443',
    cite=r"Awh, Belopolsky \& Theeuwes (2012)",
    checked='from memory' + ", " + _P18,
    licence="facts only",
    data={},
)

_P19 = "through a web search, 2026-11-15"

MILLER_1956 = Dataset(
    key="miller_1956",
    title='The magical number seven',
    source='G. A. Miller, The magical number seven, plus or minus two: some limits on our capacity for processing information, Psychological Review 63 (1956) 81-97',
    cite=r"Miller (1956)",
    checked='secondary summaries and quotations of the paper' + ", " + _P19,
    licence='facts only',
    data={'binary_span': 9, 'word_span': 5, 'smith_binary_recoded': 40, 'absolute_judgment_bits': 2.6},
)

SPERLING_1960 = Dataset(
    key="sperling_1960",
    title='Partial report',
    source='G. Sperling, The information available in brief visual presentations, Psychological Monographs 74 (1960) no. 11, whole no. 498',
    cite=r"Sperling (1960)",
    checked="secondary summaries (the monograph's tables not read: about 9 of 12 is the commonly quoted figure)" + ", " + _P19,
    licence='facts only',
    data={'letters': 12, 'whole_report': 4.5, 'partial_available_immediate': 9.0},
)

PETERSON_1959 = Dataset(
    key="peterson_1959",
    title='Short-term forgetting in eighteen seconds',
    source='L. R. Peterson and M. J. Peterson, Short-term retention of individual verbal items, Journal of Experimental Psychology 58 (1959) 193-198; J. Brown, Some tests of the decay theory of immediate memory, Quarterly Journal of Experimental Psychology 10 (1958) 12-21',
    cite=r"Peterson \& Peterson (1959)",
    checked='secondary summaries (about 80% at 3 s and about 10% at 18 s)' + ", " + _P19,
    licence='facts only',
    data={'delays_s': [3, 6, 9, 12, 15, 18], 'recall_3s': 0.8, 'recall_18s': 0.1},
)

KEPPEL_UNDERWOOD_1962 = Dataset(
    key="keppel_underwood_1962",
    title='Proactive interference in short-term retention',
    source='G. Keppel and B. J. Underwood, Proactive inhibition in short-term retention of single items, Journal of Verbal Learning and Verbal Behavior 1 (1962) 153-161',
    cite=r"Keppel \& Underwood (1962)",
    checked='from memory and reviews' + ", " + _P19,
    licence='facts only',
    data={},
)

BADDELEY_HITCH_1974 = Dataset(
    key="baddeley_hitch_1974",
    title='Working memory',
    source='A. D. Baddeley and G. Hitch, Working memory, in G. H. Bower (ed.), The Psychology of Learning and Motivation 8 (1974) 47-89; R. C. Atkinson and R. M. Shiffrin, Human memory: a proposed system and its control processes, ibid. 2 (1968) 89-195',
    cite=r"Baddeley \& Hitch (1974)",
    checked='from memory and reviews' + ", " + _P19,
    licence='facts only',
    data={},
)

BADDELEY_1975 = Dataset(
    key="baddeley_1975",
    title='The word-length effect',
    source='A. D. Baddeley, N. Thomson and M. Buchanan, Word length and the structure of short-term memory, Journal of Verbal Learning and Verbal Behavior 14 (1975) 575-589',
    cite=r"Baddeley, Thomson \& Buchanan (1975)",
    checked='secondary summaries (span is about what can be said in two seconds)' + ", " + _P19,
    licence='facts only',
    data={'seconds_of_speech': 2.0},
)

SHALLICE_WARRINGTON_1970 = Dataset(
    key="shallice_warrington_1970",
    title='Patient K.F.',
    source='E. K. Warrington and T. Shallice, The selective impairment of auditory verbal short-term memory, Brain 92 (1969) 885-896; T. Shallice and E. K. Warrington, Independent functioning of verbal memory stores: a neuropsychological study, Quarterly Journal of Experimental Psychology 22 (1970) 261-273',
    cite=r"Warrington \& Shallice (1969); \ Shallice \& Warrington (1970)",
    checked='secondary summaries' + ", " + _P19,
    licence='facts only',
    data={'kf_digit_span': 2},
)

STERNBERG_1966 = Dataset(
    key="sternberg_1966",
    title='High-speed scanning in human memory',
    source='S. Sternberg, High-speed scanning in human memory, Science 153 (1966) 652-654',
    cite=r"Sternberg (1966)",
    checked='a hosted copy of the paper' + ", " + _P19,
    licence='facts only',
    data={'slope_ms': 37.9, 'intercept_ms': 397.2, 'r2': 0.994},
)

LUCK_VOGEL_1997 = Dataset(
    key="luck_vogel_1997",
    title='Four objects',
    source='S. J. Luck and E. K. Vogel, The capacity of visual working memory for features and conjunctions, Nature 390 (1997) 279-281',
    cite=r"Luck \& Vogel (1997)",
    checked='the abstract' + ", " + _P19,
    licence='facts only',
    data={'capacity': 4},
)

COWAN_2001 = Dataset(
    key="cowan_2001",
    title='Four, plus or minus one',
    source='N. Cowan, The magical number 4 in short-term memory: a reconsideration of mental storage capacity, Behavioral and Brain Sciences 24 (2001) 87-185; H. Pashler, Familiarity and visual change detection, Perception & Psychophysics 44 (1988) 369-378',
    cite=r"Cowan (2001)",
    checked='from memory and reviews' + ", " + _P19,
    licence='facts only',
    data={'capacity': 4},
)

ZHANG_LUCK_2008 = Dataset(
    key="zhang_luck_2008",
    title='Discrete fixed-resolution representations',
    source='W. Zhang and S. J. Luck, Discrete fixed-resolution representations in visual working memory, Nature 453 (2008) 233-235',
    cite=r"Zhang \& Luck (2008)",
    checked='the abstract and summaries' + ", " + _P19,
    licence='facts only',
    data={},
)

BAYS_2009 = Dataset(
    key="bays_2009",
    title='Continuous report of colour, trial by trial (open data)',
    source='P. M. Bays, R. F. G. Catalao and M. Husain, The precision of visual working memory is set by allocation of a shared resource, Journal of Vision 9(10):7 (2009); data shared by P. M. Bays at osf.io/c2yx5 (Exp_data.mat)',
    cite=r"Bays, Catalao \& Husain (2009)",
    checked='the data file itself, fetched by explainer.psychology.opendata and checked by SHA-256' + ", " + _P19,
    licence='data fetched, not redistributed',
    data={'trials': 7271, 'observers': 12, 'set_sizes': [1, 2, 4, 6], 'durations_ms': [100, 500, 2000]},
)

VANDENBERG_2012 = Dataset(
    key="vandenberg_2012",
    title='Variable precision',
    source='R. van den Berg, H. Shin, W.-C. Chou, R. George and W. J. Ma, Variability in encoding precision accounts for visual short-term memory limitations, PNAS 109 (2012) 8780-8785; R. van den Berg, E. Awh and W. J. Ma, Factorial comparison of working memory models, Psychological Review 121 (2014) 124-149',
    cite=r"van den Berg et al.\ (2012)",
    checked='the abstracts' + ", " + _P19,
    licence='facts only',
    data={},
)

FUNAHASHI_1989 = Dataset(
    key="funahashi_1989",
    title='Delay activity in prefrontal cortex',
    source="S. Funahashi, C. J. Bruce and P. S. Goldman-Rakic, Mnemonic coding of visual space in the monkey's dorsolateral prefrontal cortex, Journal of Neurophysiology 61 (1989) 331-349",
    cite=r"Funahashi, Bruce \& Goldman-Rakic (1989)",
    checked='secondary summaries' + ", " + _P19,
    licence='facts only',
    data={},
)

WIMMER_2014 = Dataset(
    key="wimmer_2014",
    title='A diffusing bump',
    source='K. Wimmer, D. Q. Nykamp, C. Constantinidis and A. Compte, Bump attractor dynamics in prefrontal cortex explains behavioral precision in spatial working memory, Nature Neuroscience 17 (2014) 431-439',
    cite=r"Wimmer et al.\ (2014)",
    checked='the abstract' + ", " + _P19,
    licence='facts only',
    data={},
)

MONGILLO_2008 = Dataset(
    key="mongillo_2008",
    title='Activity-silent working memory',
    source='G. Mongillo, O. Barak and M. Tsodyks, Synaptic theory of working memory, Science 319 (2008) 1543-1546; N. S. Rose et al., Reactivation of latent working memories with transcranial magnetic stimulation, Science 354 (2016) 1136-1139',
    cite=r"Mongillo, Barak \& Tsodyks (2008)",
    checked='from memory and reviews' + ", " + _P19,
    licence='facts only',
    data={},
)

DANEMAN_CARPENTER_1980 = Dataset(
    key="daneman_carpenter_1980",
    title='Complex span',
    source='M. Daneman and P. A. Carpenter, Individual differences in working memory and reading, Journal of Verbal Learning and Verbal Behavior 19 (1980) 450-466; M. Daneman and P. M. Merikle, Working memory and language comprehension: a meta-analysis, Psychonomic Bulletin & Review 3 (1996) 422-433',
    cite=r"Daneman \& Carpenter (1980)",
    checked='secondary summaries' + ", " + _P19,
    licence='facts only',
    data={'meta_r_reading_span_comprehension': 0.41},
)

KANE_2005 = Dataset(
    key="kane_2005",
    title='Working memory and fluid intelligence',
    source='M. J. Kane, D. Z. Hambrick and A. R. A. Conway, Working memory capacity and fluid intelligence are strongly related constructs, Psychological Bulletin 131 (2005) 66-71; P. L. Ackerman, M. E. Beier and M. O. Boyle, ibid. 30-60',
    cite=r"Kane, Hambrick \& Conway (2005)",
    checked='a later review quoting both' + ", " + _P19,
    licence='facts only',
    data={'latent_r': 0.72, 'task_r': 0.45},
)

JAEGGI_2008 = Dataset(
    key="jaeggi_2008",
    title='Dual n-back training',
    source='S. M. Jaeggi, M. Buschkuehl, J. Jonides and W. J. Perrig, Improving fluid intelligence with training on working memory, PNAS 105 (2008) 6829-6833',
    cite=r"Jaeggi et al.\ (2008)",
    checked="the paper's design and secondary summaries" + ", " + _P19,
    licence='facts only',
    data={'training_days': [8, 12, 17, 19]},
)

REDICK_2013 = Dataset(
    key="redick_2013",
    title='An active control',
    source='T. S. Redick et al., No evidence of intelligence improvement after working memory training: a randomized, placebo-controlled study, Journal of Experimental Psychology: General 142 (2013) 359-379',
    cite=r"Redick et al.\ (2013)",
    checked='the abstract' + ", " + _P19,
    licence='facts only',
    data={'sessions': 20},
)

MELBY_LERVAG_2016 = Dataset(
    key="melby_lervag_2016",
    title='Working memory training, meta-analysed',
    source='M. Melby-Lervag, T. S. Redick and C. Hulme, Working memory training does not improve performance on measures of intelligence or other measures of far transfer, Perspectives on Psychological Science 11 (2016) 512-534',
    cite=r"Melby-Lerv\aa{}g, Redick \& Hulme (2016)",
    checked='the abstract' + ", " + _P19,
    licence='facts only',
    data={'publications': 87, 'comparisons': 145},
)

SIMONS_2016 = Dataset(
    key="simons_2016",
    title='Do brain-training programs work?',
    source='D. J. Simons et al., Do "brain-training" programs work?, Psychological Science in the Public Interest 17 (2016) 103-186; Stanford Center on Longevity and Max Planck Institute for Human Development, A consensus on the brain training industry from the scientific community (2014)',
    cite=r"Simons et al.\ (2016)",
    checked="the abstract and the consensus statement's page" + ", " + _P19,
    licence='facts only',
    data={'consensus_signatories': 70},
)

FTC_LUMOSITY_2016 = Dataset(
    key="ftc_lumosity_2016",
    title='The FTC and Lumosity',
    source='Federal Trade Commission, Lumosity to pay $2 million to settle FTC deceptive advertising charges for its brain training program, press release, 5 January 2016',
    cite=r"FTC (2016)",
    checked="the FTC's press release and press coverage" + ", " + _P19,
    licence='facts only',
    data={'redress_usd': 2000000, 'judgment_usd': 50000000},
)

_P20 = "through a web search, 2026-11-15"

PEERS_FREE_RECALL = Dataset(
    key="peers_free_recall",
    title='Immediate free recall of 16-word lists (open data)',
    source='Penn Electrophysiology of Encoding and Retrieval Study (PEERS), Kahana Computational Memory Lab, University of Pennsylvania; the immediate free-recall lists without an encoding task as packaged with psifr 0.10.1 (N. W. Morton, Psifr: analysis and visualization of free recall data, Journal of Open Source Software (2020)); M. K. Healey and M. J. Kahana, Is memory search governed by universal principles or idiosyncratic strategies?, Journal of Experimental Psychology: General 143 (2014) 575-596',
    cite=r"PEERS (Kahana lab), \ via psifr",
    checked='the data file itself, fetched from PyPI by explainer.psychology.opendata and checked by SHA-256 (the wheel and the CSV inside it); the 2014 abstract from PubMed' + ", " + _P20,
    licence='data fetched, not redistributed',
    data={'subjects': 126, 'lists': 3528, 'list_length': 16},
)

CRAIK_TULVING_1975 = Dataset(
    key="craik_tulving_1975",
    title='Depth of processing and recognition',
    source='F. I. M. Craik and E. Tulving, Depth of processing and the retention of words in episodic memory, Journal of Experimental Psychology: General 104 (1975) 268-294; F. I. M. Craik and R. S. Lockhart, Levels of processing: a framework for memory research, Journal of Verbal Learning and Verbal Behavior 11 (1972) 671-684',
    cite=r"Craik \& Tulving (1975)",
    checked='the proportions recognised (Experiment 2, incidental; Experiment 9, intentional) as quoted in a review' + ", " + _P20,
    licence='facts only',
    data={'questions': ['case', 'rhyme', 'category'], 'incidental': [0.15, 0.48, 0.81], 'intentional': [0.23, 0.59, 0.81]},
)

BERTSCH_2007 = Dataset(
    key="bertsch_2007",
    title='The generation effect, meta-analysed',
    source='S. Bertsch, B. J. Pesta, R. Wiscott and M. A. McDaniel, The generation effect: a meta-analytic review, Memory & Cognition 35 (2007) 201-210; N. J. Slamecka and P. Graf, The generation effect: delineation of a phenomenon, Journal of Experimental Psychology: Human Learning and Memory 4 (1978) 592-604',
    cite=r"Bertsch et al.\ (2007)",
    checked='the abstract from PubMed' + ", " + _P20,
    licence='facts only',
    data={'studies': 86, 'effects': 445, 'd': 0.4},
)

DRESLER_2017 = Dataset(
    key="dresler_2017",
    title='Memory athletes, and novices trained in the method of loci',
    source='M. Dresler, W. R. Shirer, B. N. Konrad, N. C. J. Muller, I. C. Wagner, G. Fernandez, M. Czisch and M. D. Greicius, Mnemonic training reshapes brain networks to support superior memory, Neuron 93 (2017) 1227-1235',
    cite=r"Dresler et al.\ (2017)",
    checked="the paper's text at PubMed Central" + ", " + _P20,
    licence='facts only',
    data={'athletes_n': 23, 'athletes': 70.8, 'controls': 39.9, 'words': 72, 'trained_n': 51, 'sessions': 40, 'minutes': 30},
)

GODDEN_BADDELEY_1975 = Dataset(
    key="godden_baddeley_1975",
    title='Divers on land and under water',
    source='D. R. Godden and A. D. Baddeley, Context-dependent memory in two natural environments: on land and underwater, British Journal of Psychology 66 (1975) 325-331',
    cite=r"Godden \& Baddeley (1975)",
    checked="the four means as transcribed by J. M. J. Murre in the data workbook of his 2021 replication (sheet 'Godden and Baddeley (1975)'), and the procedure as his paper describes it; the 1975 paper was not read" + ", " + _P20,
    licence='facts only',
    data={'conditions': ['DD', 'DW', 'WD', 'WW'], 'means': [13.5, 8.4, 8.6, 11.4], 'words': 36, 'delay_min': 4, 'depth_m': 7},
)

MURRE_2021 = Dataset(
    key="murre_2021",
    title='The divers again: a direct replication (open data)',
    source='J. M. J. Murre, The Godden and Baddeley (1975) experiment on context-dependent memory on land and underwater: a replication, Royal Society Open Science 8 (2021) 200724; data at osf.io/q2vjk; S. M. Smith and E. Vela, Environmental context-dependent memory: a review and meta-analysis, Psychonomic Bulletin & Review 8 (2001) 203-220',
    cite=r"Murre (2021)",
    checked='the paper at PubMed Central, and the data workbook itself, fetched by explainer.psychology.opendata and checked by SHA-256' + ", " + _P20,
    licence='data fetched, not redistributed',
    data={'divers': 16, 'words': 36, 'delay_min': 4, 'pool_depth_m': 1.8, 'interaction_F': 2.0, 'interaction_p': 0.163},
)

KOHNKEN_1999 = Dataset(
    key="kohnken_1999",
    title='The cognitive interview, meta-analysed',
    source='G. Kohnken, R. Milne, A. Memon and R. Bull, The cognitive interview: a meta-analysis, Psychology, Crime & Law 5 (1999) 3-27; R. P. Fisher and R. E. Geiselman, Memory-Enhancing Techniques for Investigative Interviewing: The Cognitive Interview (1992)',
    cite=r"K\"ohnken et al.\ (1999)",
    checked='the abstract and summaries' + ", " + _P20,
    licence='facts only',
    data={'studies': 42, 'comparisons': 55, 'people': 2500, 'd_correct': 0.87, 'd_incorrect': 0.24, 'accuracy_ci': 85, 'accuracy_si': 82},
)

_P21 = "through a web search, 2026-11-15"

SAVINGS_REPLICATIONS = Dataset(
    key="savings_replications",
    title="Ebbinghaus's savings curve and three replications",
    source="J. M. J. Murre and J. Dros, Replication and analysis of Ebbinghaus' forgetting curve, PLoS ONE 10 (2015) e0120644 (Table 3: savings of Ebbinghaus, of Mack and Seitz, and of Dros); O. Heller, W. Mack and J. Seitz, Replikation der Ebbinghaus'schen Vergessenskurve mit der Ersparnismethode, Zeitschrift fur Psychologie 199 (1991) 3-18; H. Ebbinghaus, Uber das Gedachtnis (1885)",
    cite=r"Murre \& Dros (2015)",
    checked="the paper at PLoS ONE (CC BY): its Table 3, the replication's procedure, and its fits of a jump at 24 hours" + ", " + _P21,
    licence='facts only',
    data={'intervals': ['20 min', '1 h', '9 h', '1 d', '2 d', '6 d', '31 d'], 'minutes': [20, 64, 526, 1440, 2880, 8640, 44640], 'ebbinghaus': [0.582, 0.442, 0.358, 0.337, 0.278, 0.254, 0.211], 'mack': [0.544, 0.432, 0.285, 0.316, 0.365, 0.309, 0.258], 'seitz': [0.442, 0.325, 0.27, 0.27, 0.286, 0.205, 0.201], 'dros': [0.472, 0.373, 0.276, 0.317, 0.23, 0.168, 0.041], 'dros_hours': 70},
)

ROEDIGER_KARPICKE_2006 = Dataset(
    key="roediger_karpicke_2006",
    title='Test-enhanced learning',
    source='H. L. Roediger III and J. D. Karpicke, Test-enhanced learning: taking memory tests improves long-term retention, Psychological Science 17 (2006) 249-255',
    cite=r"Roediger \& Karpicke (2006)",
    checked='the paper' + ", " + _P21,
    licence='facts only',
    data={'exp1_n': 120, 'exp1_delays_days': [0.003472222222222222, 2.0, 7.0], 'exp1_restudy': [0.81, 0.54, 0.42], 'exp1_test': [0.75, 0.68, 0.56], 'exp2_n': 180, 'exp2_conditions': ['SSSS', 'SSST', 'STTT'], 'exp2_5min': [0.83, 0.78, 0.71], 'exp2_week': [0.4, 0.56, 0.61], 'exp2_predicted': [4.8, 4.2, 4.0], 'exp2_reads': [14.2, 10.3, 3.4]},
)

SCHOOLER_1990 = Dataset(
    key="schooler_1990",
    title='Verbal overshadowing of faces',
    source='J. W. Schooler and T. Y. Engstler-Schooler, Verbal overshadowing of visual memories: some things are better left unsaid, Cognitive Psychology 22 (1990) 36-71',
    cite=r"Schooler \& Engstler-Schooler (1990)",
    checked="the counts of Studies 1 and 4 as tabulated in the Registered Replication Report's data workbooks (Alogna et al. 2014)" + ", " + _P21,
    licence='facts only',
    data={'study1_verbal': [17, 44], 'study1_control': [28, 44], 'study4_verbal': [18, 37], 'study4_control': [27, 38]},
)

ALOGNA_2014 = Dataset(
    key="overshadowing_rrr",
    title='The verbal-overshadowing Registered Replication Report (open data)',
    source='V. K. Alogna, M. K. Attaya, P. Aucoin, S. Bahnik, S. Birch, A. R. Birt, ... and R. A. Zwaan, Registered replication report: Schooler and Engstler-Schooler (1990), Perspectives on Psychological Science 9 (2014) 556-578; data at osf.io/ybeur',
    cite=r"Alogna et al.\ (2014)",
    checked='the two data workbooks (Table1_updated, Table2_updated), fetched by explainer.psychology.opendata and checked by SHA-256' + ", " + _P21,
    licence='data fetched, not redistributed',
    data={'rrr1_labs': 31, 'rrr2_labs': 22, 'rrr1_diff': -0.04, 'rrr2_diff': -0.16},
)

LOFTUS_PALMER_1974 = Dataset(
    key="loftus_palmer_1974",
    title='Smashed or hit: the wording of a question',
    source='E. F. Loftus and J. C. Palmer, Reconstruction of automobile destruction: an example of the interaction between language and memory, Journal of Verbal Learning and Verbal Behavior 13 (1974) 585-589',
    cite=r"Loftus \& Palmer (1974)",
    checked="summaries of the paper's two experiments" + ", " + _P21,
    licence='facts only',
    data={'verbs': ['smashed', 'collided', 'bumped', 'hit', 'contacted'], 'mph': [40.8, 39.3, 38.1, 34.0, 31.8], 'exp1_n': 45, 'exp2_n': 150, 'glass_yes': {'smashed': 16, 'hit': 7, 'control': 6}, 'per_group': 50},
)

ROEDIGER_MCDERMOTT_1995 = Dataset(
    key="roediger_mcdermott_1995",
    title='False memories for words not presented (DRM)',
    source='H. L. Roediger III and K. B. McDermott, Creating false memories: remembering words not presented in lists, Journal of Experimental Psychology: Learning, Memory, and Cognition 21 (1995) 803-814; J. Deese, On the prediction of occurrence of particular verbal intrusions in immediate recall, Journal of Experimental Psychology 58 (1959) 17-22',
    cite=r"Roediger \& McDermott (1995)",
    checked='the paper' + ", " + _P21,
    licence='facts only',
    data={'exp1_n': 36, 'exp1_lists': 6, 'exp1_length': 12, 'exp1_studied_recall': 0.65, 'exp1_lure_recall': 0.4, 'exp1_hits': 0.86, 'exp1_lure_fa': 0.84, 'exp2_n': 30, 'exp2_lists': 24, 'exp2_length': 15, 'exp2_studied_recall': 0.62, 'exp2_lure_recall': 0.55, 'exp2_lure_remember': 0.72},
)

CEPEDA_2008 = Dataset(
    key="cepeda_2008",
    title='Spacing over a year: the temporal ridgeline',
    source='N. J. Cepeda, E. Vul, D. Rohrer, J. T. Wixted and H. Pashler, Spacing effects in learning: a temporal ridgeline of optimal retention, Psychological Science 19 (2008) 1095-1102',
    cite=r"Cepeda et al.\ (2008)",
    checked='the paper' + ", " + _P21,
    licence='facts only',
    data={'n': 1354, 'facts': 32, 'retention_days': [7, 35, 70, 350], 'gaps_days_max': 105, 'optimal_ratio_week': [0.2, 0.4], 'optimal_ratio_year': [0.05, 0.1],
          'optimal_gap_days': [3, 8, 12, 27], 'recall_gain': [0.10, 0.59, 1.11, 0.77]},  # interpolated optima; gain over a zero gap
)

LOFTUS_PICKRELL_1995 = Dataset(
    key="loftus_pickrell_1995",
    title='Lost in the mall: implanted childhood memories',
    source='E. F. Loftus and J. E. Pickrell, The formation of false memories, Psychiatric Annals 25 (1995) 720-725; A. Scoboria, K. A. Wade, D. S. Lindsay, T. Azad, D. Strange, J. Ost and I. E. Hyman, A mega-analysis of memory reports from eight peer-reviewed false memory implantation studies, Memory 25 (2017) 146-163; G. Murphy, C. A. Dawson, C. Huston, L. Ballantyne, E. Barrett, C. S. Cowman, C. Fitzsimons, J. Maher, K. M. Ryan and C. M. Greene, Lost in the mall again: a preregistered replication and extension of Loftus & Pickrell (1995), Memory 31 (2023) 711-724',
    cite=r"Loftus \& Pickrell (1995)",
    checked='the abstracts and summaries of the three papers' + ", " + _P21,
    licence='facts only',
    data={'original_n': 24, 'original_rate': 0.25, 'mega_studies': 8, 'mega_n': 423, 'mega_rate': 0.304, 'replication_n': 123, 'replication_rate': 0.35},
)

TALARICO_RUBIN_2003 = Dataset(
    key="talarico_rubin_2003",
    title='Flashbulb memories of September 11',
    source='J. M. Talarico and D. C. Rubin, Confidence, not consistency, characterizes flashbulb memories, Psychological Science 14 (2003) 455-461; U. Neisser and N. Harsch, Phantom flashbulbs: false recollections of hearing the news about Challenger, in E. Winograd and U. Neisser (eds), Affect and Accuracy in Recall (1992) 9-31',
    cite=r"Talarico \& Rubin (2003)",
    checked='the abstract' + ", " + _P21,
    licence='facts only',
    data={'n': 54, 'first_day': '2001-09-12', 'retest_weeks': [1, 6, 32]},
)

HARDWICKE_2016 = Dataset(
    key="hardwicke_2016",
    title='Reconsolidation of motor memory in people, tested again',
    source='T. E. Hardwicke, M. Taqi and D. R. Shanks, Postretrieval new learning does not reliably induce human memory updating via reconsolidation, Proceedings of the National Academy of Sciences 113 (2016) 5206-5211; K. Nader, G. E. Schafe and J. E. LeDoux, Fear memories require protein synthesis in the amygdala for reconsolidation after retrieval, Nature 406 (2000) 722-726; M. P. Walker, T. Brakefield, J. A. Hobson and R. Stickgold, Dissociable stages of human memory consolidation and reconsolidation, Nature 425 (2003) 616-620',
    cite=r"Hardwicke, \ Taqi \& Shanks (2016)",
    checked='the abstract' + ", " + _P21,
    licence='facts only',
    data={'experiments': 7, 'direct': 4},
)

PATIHIS_2013 = Dataset(
    key="patihis_2013",
    title='Superior autobiographical memory and false memory',
    source='L. Patihis, S. Y. Frenda, A. K. R. LePort, N. Petersen, R. M. Nichols, C. E. L. Stark, J. L. McGaugh and E. F. Loftus, False memories in highly superior autobiographical memory individuals, Proceedings of the National Academy of Sciences 110 (2013) 20947-20952; E. S. Parker, L. Cahill and J. L. McGaugh, A case of unusual autobiographical remembering, Neurocase 12 (2006) 35-49',
    cite=r"Patihis et al.\ (2013)",
    checked='the abstract' + ", " + _P21,
    licence='facts only',
    data={'hsam': 20, 'controls': 38},
)

WIXTED_WELLS_2017 = Dataset(
    key="wixted_wells_2017",
    title='Eyewitness confidence and accuracy',
    source='J. T. Wixted and G. L. Wells, The relationship between eyewitness confidence and identification accuracy: a new synthesis, Psychological Science in the Public Interest 18 (2017) 10-65; J. T. Wixted and L. Mickes, A signal-detection-based diagnostic-feature-detection model of eyewitness identification, Psychological Review 121 (2014) 262-276; L. Mickes, Receiver operating characteristic analysis and confidence-accuracy characteristic analysis in investigations of system variables and estimator variables that affect eyewitness memory, Journal of Applied Research in Memory and Cognition 4 (2015) 93-102; G. L. Wells et al., Policy and procedure recommendations for the collection and preservation of eyewitness identification evidence, Law and Human Behavior 44 (2020) 3-36',
    cite=r"Wixted \& Wells (2017)",
    checked='the abstracts' + ", " + _P21,
    licence='facts only',
    data={'procedures': ['one suspect per line-up', 'the suspect does not stand out', 'a warning that the culprit may be absent', 'double-blind administration', 'confidence recorded at once']},
)

DUNLOSKY_2013 = Dataset(
    key="dunlosky_2013",
    title='Ten study techniques, rated',
    source="J. Dunlosky, K. A. Rawson, E. J. Marsh, M. J. Nathan and D. T. Willingham, Improving students' learning with effective learning techniques, Psychological Science in the Public Interest 14 (2013) 4-58",
    cite=r"Dunlosky et al.\ (2013)",
    checked="the abstract and the paper's summary table" + ", " + _P21,
    licence='facts only',
    data={'high': ['practice testing', 'distributed practice'], 'moderate': ['elaborative interrogation', 'self-explanation', 'interleaved practice'], 'low': ['summarization', 'highlighting', 'keyword mnemonic', 'imagery for text', 'rereading']},
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
                          XIE_2013, PHOENIX_1959, TEIGEN_1994, ROENNEBERG_2004,
                          WEBER_1834, FECHNER_1860, STEVENS_1957, POULTON_1968, LEVITT_1971, WATSON_PELLI_1983,
                          WICHMANN_HILL_2001, MCGILL_GOLDBERG_1968, HALBERDA_2008, GIBBON_1977, LESMES_2010,
                          DEVRIES_ROSE, BERNOULLI_1738, PLATEAU_1872, THURSTONE_1927,
                          MACKWORTH_1948, PETERSON_1954, TANNER_SWETS_1954, WOLFE_2005, FLECK_MITROFF_2007, GIGERENZER_HOFFRAGE_1995, RATCLIFF_1992, YONELINAS_1994, SEE_1995, SWETS_2000, SWETS_1961, MANISCALCO_LAU_2012, MICKES_2012,
                          HECHT_1942, BAYLOR_1979, TINSLEY_2016, KUFFLER_1953, CAMPBELL_ROBSON_1968, BLAKEMORE_CAMPBELL_1969, LAFER_SOUSA_2015, MILNER_1991, JORDAN_2010, COLOUR_TABLES, OKABE_ITO,
                          ADELSON_1995, ERNST_BANKS_2002, ALAIS_BURR_2004, RAHNEV_DENISON_2018, WEISS_2002, THOMPSON_1982, ADAMS_2004, SEGALL_1966, AMIR_FIRESTONE_2025, GAUTHIER_1999, YIN_1969, YAMINS_2014, GEIRHOS_2019, VONG_2024, WHEATSTONE_1838,
                          BEKESY_1960, KEMP_1978, LIBERMAN_1957, MCMURRAY_2002, MCGURK_1976, MALLICK_2015, BOTVINICK_COHEN_1998, LUSH_2020, MELZACK_WALL_1965, LEVINE_1978, HANIG_1901, BUSHDID_2014, MCDERMOTT_2016, KUJAWA_LIBERMAN_2009,
                          PAVLOV_1927, THORNDIKE_1898, WATSON_RAYNER_1920, HARRIS_1979, FERSTER_SKINNER_1957, RESCORLA_1968, WASSERMAN_1993, KAMIN_1969, MAES_2016, RESCORLA_WAGNER_1972, LUBOW_MOORE_1959, BOUTON_BOLLES_1979, MACKINTOSH_PEARCE_HALL, GALLISTEL_GIBBON_2000, HERRNSTEIN_1961, GARCIA_KOELLING_1966, BRELAND_1961, BANDURA_1961, PRENDERGAST_2006, ZENDLE_CAIRNS_2018, GERSHMAN_2010, MITCHELL_2009, SCHILLER_2010,
                          SCHULTZ_1997, STEINBERG_2013, FRANK_2004, WILSON_2014, TOLMAN_HONZIK_1930, TOLMAN_1948, HAFTING_2005, ADAMS_DICKINSON_1981, DAW_2011, FEHER_DA_SILVA_2020, MOMENNEJAD_2017, HOWE_2013, DABNEY_2020, REDISH_2004, LI_2010, WEINTRAUB_2010, WANG_2018,
                          SIMONS_CHABRIS_1999, RENSINK_1997, CHERRY_1953, BROADBENT_1958, MORAY_1959, TREISMAN_1960, LAVIE_1995, POSNER_1980, TREISMAN_GELADE_1980, WOLFE_2021, ITTI_KOCH_1998, DREW_2013, RAYMOND_1992, PASHLER_1994, STROOP_1935, ERIKSEN_1974, BOTVINICK_2001, ROGERS_MONSELL_1995, MORAN_DESIMONE_1985, REYNOLDS_HEEGER_2009, BUNDESEN_1990, STRAYER_2001, OPHIR_2009, ANDERSON_2011, AWH_2012,
                          MILLER_1956, SPERLING_1960, PETERSON_1959, KEPPEL_UNDERWOOD_1962, BADDELEY_HITCH_1974, BADDELEY_1975, SHALLICE_WARRINGTON_1970, STERNBERG_1966, LUCK_VOGEL_1997, COWAN_2001, ZHANG_LUCK_2008, BAYS_2009, VANDENBERG_2012, FUNAHASHI_1989, WIMMER_2014, MONGILLO_2008, DANEMAN_CARPENTER_1980, KANE_2005, JAEGGI_2008, REDICK_2013, MELBY_LERVAG_2016, SIMONS_2016, FTC_LUMOSITY_2016,
                          PEERS_FREE_RECALL, CRAIK_TULVING_1975, BERTSCH_2007, DRESLER_2017, GODDEN_BADDELEY_1975, MURRE_2021, KOHNKEN_1999,
                          SAVINGS_REPLICATIONS, ROEDIGER_KARPICKE_2006, SCHOOLER_1990, ALOGNA_2014, LOFTUS_PALMER_1974, ROEDIGER_MCDERMOTT_1995, CEPEDA_2008, LOFTUS_PICKRELL_1995, TALARICO_RUBIN_2003, HARDWICKE_2016, PATIHIS_2013, WIXTED_WELLS_2017, DUNLOSKY_2013)}
