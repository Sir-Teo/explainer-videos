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
    Part(
        n=60, level="D", widget="humanormachine", prereq=(2, 3, 4, 26, 35, 45, 47),
        question="What can psychology and artificial intelligence now tell each other?",
        story="The Perceptron was published in Psychological Review in 1958, by a psychologist; now language models "
              "sit psychology's tests, are proposed as models of the mind, and are used as advisers, helpers and "
              "stand-in participants. The part judges networks as models of vision and language, simulates the "
              "traps of machine psychology (contamination, prompt sensitivity, one model as a sample of one), weighs "
              "machine theory of mind, treats a benchmark as a test, models algorithm aversion, reads a dialogue "
              "that reduced conspiracy belief and the evidence on chatbots in care, shows what silicon samples "
              "erase, sets out the screens-and-well-being dispute with a specification curve, and proposes a "
              "science of machine behaviour built on psychology's methods.",
        handoff="Part 61 uses language models as research assistants and simulated participants and writes theories "
                "as code; Part 62's dissertation is preregistered.",
        outside="Part 3's validity, Part 4's forking paths, Part 45's item response theory and Part 47's units of "
                "analysis; proportions, regression and power.",
        objectives={
            "U": ["Explain why a model matching people's behaviour need not share their mechanism.",
                  "Explain algorithm aversion and appreciation, and when each appears."],
            "M": ["Show by simulation how contamination and pseudo-replication mislead a machine evaluation.",
                  "Compute the items needed to separate two models, and run a specification curve."],
            "D": ["Design a valid test of a cognitive capacity in a machine, with new items and controls."],
            "I": ["Write an evaluation plan for a model, and judge a silicon-sample or chatbot-care claim."],
        },
        results=[
            ("Items to separate two accuracies", r"n \approx \frac{2p(1-p)(1-\rho)(z_{1-\alpha/2} + z_{1-\beta})^2}"
                                                 r"{\Delta^2}"),
            ("Accuracy with an aid", r"A = s\,a_{\text{aid}} + (1 - s)\,a_{\text{own}}"),
            ("A benchmark item, two-parameter logistic", r"P(\text{correct}\mid\theta) = \frac{1}{1 + e^{-a(\theta - b)}}"),
        ],
        U=(0, 1, 2, 6, 7, 10, 13), D=(4, 11, 12, 15), I=(5, 8, 9, 14),
        also=(("Psyche's machines module", "explainer/psychology/psyche/machines.py"),
              ("Its tests", "tests/psychology/test_machines.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=61, level="D", widget="designspace", prereq=(2, 4, 38, 48, 50, 58),
        question="What would psychology look like if it were designed today?",
        story="In 2020, 160 teams with thousands of variables tried to predict six outcomes in children's lives and "
              "barely beat a four-variable regression. The part separates explanation from prediction, reads "
              "many-labs heterogeneity, shows what samples of millions can and cannot fix, asks who is sampled, "
              "designs an experiment as a space with a surrogate model, follows machine-assisted theory and theory "
              "as code, reruns the natural selection of bad science under two publication rules, takes apart a "
              "digital-traces result, asks what research should automate, and ranks the reform proposals by "
              "evidence.",
        handoff="Part 62 carries one question through a registered report, then closes the series' accounts.",
        outside="Part 2's design, Part 4's power and forking paths, Part 38's samples, Part 48's model comparison "
                "and Part 50's meta-analysis; regression and simulation.",
        objectives={
            "U": ["Explain the difference between explanation and prediction, and what a predictability ceiling is.",
                  "Explain why a huge self-selected sample can be precisely wrong."],
            "M": ["Estimate heterogeneity across labs, and fit a surrogate model over a design space.",
                  "Run a model of a research community and compute false-discovery rates from base rates and "
                  "power."],
            "D": ["Propose a test of whether a reform (formal theory, integrative design) speeds discovery."],
            "I": ["Write a commissioning brief for research that will hold up."],
        },
        results=[
            ("False share of positives", r"\frac{(1-b)\alpha}{(1-b)\alpha + bW}"),
            ("Smaldino and McElreath's false-positive rate", r"\alpha(e) = \frac{W}{1 + (1 - W)e}"),
            ("Meng's identity", r"\bar y_n - \bar y_N = \rho_{R,Y}\sqrt{\frac{N - n}{n}}\,\sigma_Y"),
        ],
        U=(0, 1, 2, 4, 5, 12, 13), D=(6, 8, 9, 15), I=(3, 10, 11, 14),
        also=(("Psyche's community module", "explainer/psychology/psyche/community.py"),
              ("Its tests", "tests/psychology/test_community.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=62, level="D", widget="lastrotation", prereq=(1, 2, 3, 4, 24, 59, 61),
        question="Was Kant right that psychology could never become a science?",
        story="The series ends as a doctorate does. A question where Part 24 and Part 59 collide (is a robust "
              "effect, the mental-rotation slope, a reliable measure of a person?) is taken through a registered "
              "report: the plan written as code and hashed before the analysis, a design check on simulated "
              "people, reviews, Stage 2 on open data with one reported deviation, and a result reported as it fell "
              "(inconclusive for the paradox, leaning against it). Then Psyche sits the Battery, the complete "
              "Ledger is read by act, the Homunculus is drawn one last time, and Kant's three objections are "
              "answered, with a fourth he did not make.",
        handoff="The open problems of every part's frontier, gathered; the next row of the Ledger is the reader's.",
        outside="Every earlier part; Part 3's reliability, Part 4's registered reports and Part 59's paradox above "
                "all.",
        objectives={
            "U": ["Explain how a registered report protects a result, and what a reported deviation is.",
                  "Give the verdict on each of Kant's objections, with evidence from the series."],
            "M": ["Compute split-half reliability with a bootstrap interval, and a design check by simulation."],
            "D": ["Write a Stage 1 registered report for an open problem from any part's frontier."],
            "I": ["Choose a role and the parts that prepare for it, and commission research that will hold up."],
        },
        results=[
            ("Spearman-Brown for a split half", r"\rho_{\text{full}} = \frac{2r}{1 + r}"),
            ("The registered decision", r"\text{supported if } \mathrm{CI}_{95} < 0.70,\ \text{refuted if } "
                                        r"\mathrm{CI}_{95} > 0.70"),
            ("Attenuation", r"r_{\text{obs}} = r_{\text{true}}\sqrt{\rho_x\rho_y}"),
        ],
        U=(0, 1, 2, 3, 9, 10, 11), D=(4, 5, 6, 7, 15), I=(8, 12, 13, 14),
        also=(("Psyche's thesis module", "explainer/psychology/psyche/thesis.py"),
              ("Its tests", "tests/psychology/test_thesis.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
