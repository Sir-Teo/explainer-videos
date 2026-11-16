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
]
