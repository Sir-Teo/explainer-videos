"""Psychology, Built as a course: Parts 39 to 43 (Act X, when minds suffer, and the capstone)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=39, level="U", widget="screening",
        question="Where is the line between suffering and illness, and who draws it?",
        story="In 1973 a study reported that eight healthy people faked one symptom, were admitted to psychiatric "
              "hospitals and were never detected; it helped force explicit diagnostic criteria, and decades later "
              "its data fell into serious doubt. The part asks what a disorder is: rarity, distress, dysfunction and "
              "harm, Wakefield's harmful dysfunction, and a category removed by a vote. It derives Cohen's kappa, "
              "shows the field trials' kappas (depression near 0.3) and why reliability caps validity, counts 227 "
              "symptom combinations that make one diagnosis and 1,030 profiles among real patients, weighs categories "
              "against dimensions, finds comorbidity and a p factor, and builds a symptom network that tips suddenly "
              "and recovers slowly. Then epidemiology and the treatment gap, a positive screen in natural "
              "frequencies, Meehl's formulas against clinical judgment, and idioms of distress.",
        handoff="Anxiety and depression are Part 40, psychosis, addiction and development Part 41, the evidence for "
                "therapy Part 42; latent variables and networks Parts 44 and 47.",
        outside="Part 3's reliability, Part 12's base rates and Part 32's factor analysis; probability, logistic "
                "functions and simple linear regression.",
        objectives={
            "U": ["Explain the candidate definitions of a disorder and their problems, and the history from asylums "
                  "to DSM-III.",
                  "Compute and interpret Cohen's kappa, and explain why a reliable diagnosis need not be valid.",
                  "Work out what a positive screen means in natural frequencies, and describe prevalence and the "
                  "treatment gap."],
            "M": ["Show that reliability bounds validity, and simulate two clinicians to see it.",
                  "Count the symptom combinations a criterion allows, and compare categorical and dimensional "
                  "structure.",
                  "Build a symptom network and show bistability and hysteresis under changing stress."],
            "D": ["Explain why network, latent-variable and common-cause models can be statistically equivalent, and "
                  "design a study to tell them apart."],
            "I": ["Evaluate a screening programme or a risk tool by its predictive value at the real base rate."],
        },
        results=[
            ("Cohen's kappa", r"\kappa = \frac{p_o - p_e}{1 - p_e}"),
            ("Positive predictive value", r"\text{PPV} = \frac{\pi\,\text{sens}}{\pi\,\text{sens} + (1 - \pi)(1 - "
                                          r"\text{spec})}"),
            ("Reliability bounds validity", r"|r_{xy}| \le \sqrt{r_{xx}\, r_{yy}}"),
            ("Symptom network", r"P(x_i = 1) = \sigma\big(b + s + c \textstyle\sum_{j \ne i} x_j\big)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's clinic module", "explainer/psychology/psyche/clinic.py"),
              ("Its tests", "tests/psychology/test_clinic.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
