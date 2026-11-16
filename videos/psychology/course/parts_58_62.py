"""Psychology, Built as a course: Parts 58 to 62 (Act XIII, the frontier)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=58, level="D", widget="aftereffect", prereq=(11, 13, 14, 22),
        question="Is there one principle from which the mind's mechanisms follow?",
        story="In 1961 Horace Barlow proposed that sensory neurons exist to remove redundancy; in 1996 a network asked "
              "to describe natural images with as few active units as possible grew the oriented receptive fields "
              "of visual cortex. The part runs that optimization on screen, derives a fly's contrast code and the "
              "retina's centre-surround from efficiency, predicts the tilt after-effect and repulsive biases from an "
              "efficient code, derives Shepard's law from rate-distortion theory, meets normalization's one "
              "equation, builds predictive coding and the free energy step by step, weighs the Bayesian brain, "
              "resource rationality and learning rules, and scores each principle by what it risked.",
        handoff="Part 59 takes priors, precision and learning rates to the clinic; Part 60 compares learning in "
                "context in machines; Part 62's dissertation can test a principle.",
        outside="Part 11's psychophysics, Part 13's receptive fields, Part 14's inference and Part 22's "
                "generalization; logarithms, probability and a little linear algebra.",
        objectives={
            "U": ["Explain the efficient coding hypothesis and give two of its successful predictions.",
                  "Explain why an adapted population code produces the tilt after-effect."],
            "M": ["Derive Laughlin's histogram-matching code and the whitening filter, and run sparse coding.",
                  "Derive the variational free energy as a divergence plus surprise, and compute it for a Gaussian "
                  "model."],
            "D": ["State what a unified theory of the mind would have to risk, and design an experiment that "
                  "separates predictive coding from adaptation."],
            "I": ["Explain how perceptual codecs and sensors spend bits where perception needs them."],
        },
        results=[
            ("Laughlin's code", r"r(c) = F_C(c)"),
            ("Sparse coding", r"\min_{D, a}\ \tfrac12\lVert x - Da\rVert^2 + \lambda\lVert a\rVert_1"),
            ("Normalization", r"R = \frac{c^n}{\sigma^n + c^n + m^n}"),
            ("Free energy", r"F(q) = \mathrm{KL}\big(q\,\|\,p(z\mid x)\big) - \log p(x)"),
        ],
        U=(0, 1, 2, 4, 7, 13), D=(8, 9, 12, 15), I=(14,),
        also=(("Psyche's efficient module", "explainer/psychology/psyche/efficient.py"),
              ("Its tests", "tests/psychology/test_efficient.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=59, level="D", widget="taskdesign", prereq=(3, 4, 17, 39, 48),
        question="Can a model of the mind tell a clinician something a conversation cannot?",
        story="Computational psychiatry plans to give a patient a task, fit a model and read off the parameter that "
              "has gone wrong. Its first obstacle is the reliability paradox: tasks with enormous group effects "
              "measure individuals poorly. The part sets out the theory-driven and data-driven routes, compulsivity "
              "and model-based control, anxiety and volatility, mood as an integral of prediction errors; buys "
              "reliability with trials, finds biotypes in data with none and exposes them by stability, scores a "
              "prediction model in sample, cross-validated and in a new trial, sizes a trial for choosing "
              "treatments, judges stimulation, psychedelics and phones by Part 2's standards, and sets five tests "
              "for a computational target. It opens with the care card.",
        handoff="Part 60 asks what models of machines can tell psychology; Part 61 takes up big-team science and "
                "registered models; Part 62's dissertation can measure individuals properly.",
        outside="Part 3's reliability and attenuation, Part 4's winner's curse, Part 17's learning models and Part "
                "48's model fitting; correlation, logistic regression and cross-validation.",
        objectives={
            "U": ["Explain the reliability paradox and why it limits tasks as clinical tests.",
                  "Explain why a model scored on its own data overstates how it will do in a new clinic."],
            "M": ["Compute the trials needed for a target reliability, and the attenuation of a correlation.",
                  "Run a clustering pipeline with a stability check, and cross-validate a prediction model "
                  "properly."],
            "D": ["Design a study that tests whether a computational parameter is a treatment target."],
            "I": ["Evaluate a biomarker or digital-health claim with six questions."],
        },
        results=[
            ("Difference-score reliability", r"\rho = \frac{\sigma_b^2}{\sigma_b^2 + 2\sigma_t^2/n}"),
            ("Spearman-Brown", r"\rho_k = \frac{k\rho}{1 + (k-1)\rho}"),
            ("Attenuation", r"r_{\text{obs}} = r_{\text{true}}\sqrt{\rho_x\rho_y}"),
            ("An interaction's sample", r"N_{\text{interaction}} \approx 4\,N_{\text{main}}"),
        ],
        U=(0, 1, 2, 3, 6, 8, 13), D=(5, 7, 12, 15), I=(9, 10, 11, 14),
        also=(("Psyche's precision module", "explainer/psychology/psyche/precision.py"),
              ("Its tests", "tests/psychology/test_precision.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
