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
    Part(
        n=40, level="U", widget="dotprobe",
        question="How do fear and sadness go wrong, and what do the treatments act on?",
        story="In 1967 dogs given shocks they could not escape later lay down and took shocks they could escape; "
              "fifty years later the authors reversed the explanation: passivity is the default, and what is learned "
              "is control. The part builds anxiety and depression from the learning models of earlier acts: Mowrer's "
              "two factors and an avoidance loop that never unlearns, extinction as context-bound learning and the "
              "return of fear, the anxiety disorders and the panic spiral, attention to threat and the failed "
              "bias-modification trials, depression's cognitive accounts, helplessness as a belief about control, and "
              "a model of momentary mood fitted to a gambling task. Then the serotonin story and the 2022 review, "
              "Kirsch's analysis and the 522-trial network meta-analysis, life events and the gene-by-stress finding "
              "that did not survive large samples, lithium, and why suicide cannot be predicted well for individuals.",
        handoff="Psychosis, addiction and development are Part 41, the evidence for therapy Part 42, symptoms tracked "
                "day by day Part 47 and computational psychiatry Part 59.",
        outside="Part 16's Rescorla-Wagner model, Part 17's prediction errors, Part 29's emotion and Part 39's base "
                "rates; logarithms, geometric series and least squares.",
        objectives={
            "U": ["Explain Mowrer's two factors, why avoidance preserves fear, and why exposure works.",
                  "Describe the cognitive, helplessness and reward accounts of depression and the evidence on each.",
                  "Interpret the drug-placebo difference as an effect size and a number needed to treat, and explain "
                  "why suicide risk cannot be predicted well for individuals."],
            "M": ["Simulate avoidance and response prevention on a Rescorla-Wagner learner, and renewal after "
                  "context-bound extinction.",
                  "Model the triadic design as a Beta belief about control.",
                  "Fit Rutledge and colleagues' model of momentary mood and show what blunted prediction errors do."],
            "D": ["Design a study that separates liking, learning and effort in anhedonia, with the parameter each "
                  "hypothesis predicts will differ."],
            "I": ["Map a treatment onto the model it acts on, and judge a claimed effect by its size and the base rate."],
        },
        results=[
            ("Rescorla-Wagner extinction", r"V_{t+1} = V_t + \alpha\,(0 - V_t)"),
            ("Renewal", r"\text{fear}_A = E, \quad \text{fear}_B = E - I"),
            ("Momentary mood", r"H_t = w_0 + w_1 \textstyle\sum_j \gamma^{t-j} CR_j + w_2 \sum_j \gamma^{t-j} EV_j "
                               r"+ w_3 \sum_j \gamma^{t-j} \delta_j"),
            ("Number needed to treat", r"\text{NNT} = \frac{1}{p_{\text{drug}} - p_{\text{placebo}}}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13), D=(15,), I=(14,),
        also=(("Psyche's clinic module", "explainer/psychology/psyche/clinic.py"),
              ("Its tests", "tests/psychology/test_clinic.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
