"""Psychology, Built as a course: Parts 44 to 50 (Act XI, the graduate toolkit)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=44, level="M", widget="diagrams", prereq=(3, 32, 43),
        question="How do you model something you cannot observe, and how do you know the model is not a fiction?",
        story="In 1921 Sewall Wright drew arrows between variables and showed how correlations follow from them; in "
              "1969 Karl Jöreskog joined his paths to Spearman's factors, and the structural equation model became "
              "psychology's way to state a theory about unobservables. The part derives the tracing rule, builds and "
              "identifies the factor model, fits Holzinger and Swineford's nine tests by maximum likelihood (checked "
              "against lavaan), judges fit and shows fixed cut-offs passing a wrong model, undoes attenuation, tests "
              "invariance across two schools, finds a significant indirect effect that is not there, shows that "
              "equivalent diagrams fit identically, that a cross-lagged panel confuses stable people with change, and "
              "that a factor and a network can imply the same covariances, and ends with eight questions for reading "
              "an SEM paper.",
        handoff="Item response theory is Part 45; within-person models over time Part 47; models of behaviour Part 48; "
                "the weight of evidence Part 50.",
        outside="Part 3's reliability, Part 32's factor analysis and Part 43's workflow; matrices, the normal "
                "likelihood and least squares.",
        objectives={
            "U": ["Read a path diagram: latent and observed variables, loadings, errors, and what an arrow claims.",
                  "Explain why a good fit does not show that the arrows point the right way."],
            "M": ["Derive model-implied correlations by the tracing rule and as Σ = ΛΦΛᵀ + Θ; count parameters to check "
                  "identification, and fit a confirmatory factor model by maximum likelihood.",
                  "Compute χ², RMSEA, CFI and SRMR, and test configural, metric and scalar invariance.",
                  "Simulate a confounded mediator and show the product-of-coefficients estimate is biased."],
            "D": ["Say what causal discovery can orient from conditional independences, and what its assumptions "
                  "demand of psychological data."],
            "I": ["Audit a survey or people-analytics model by asking which equivalent diagram fits as well, and "
                  "whether the score is comparable across groups."],
        },
        results=[
            ("Tracing rule", r"\rho_{XY} = \sum_{\text{paths}} \prod \text{path coefficients}"),
            ("Factor model", r"\Sigma = \Lambda \Phi \Lambda^\top + \Theta"),
            ("ML discrepancy", r"F = \log|\Sigma| + \operatorname{tr}(S\Sigma^{-1}) - \log|S| - p, \quad T = nF"),
            ("RMSEA", r"\sqrt{\max(T - df, 0)/(df\, n)}"),
            ("Attenuation", r"r_{\text{true}} = r_{xy}/\sqrt{r_{xx} r_{yy}}"),
        ],
        U=(0, 1, 9, 12), D=(15,), I=(14,),
        also=(("Psyche's sem module", "explainer/psychology/psyche/sem.py"),
              ("Its tests", "tests/psychology/test_sem.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=45, level="M", widget="adaptive", prereq=(3, 12, 44),
        question="How can two people who took different questions be put on the same scale?",
        story="In the 1950s the Danish mathematician Georg Rasch was asked to compare reading across tests that share "
              "no items. Classical scores cannot do it: difficulty depends on the sample and scores on the test. Rasch "
              "modelled the single encounter of one person with one item, and person and item separate. The part "
              "derives the model's specific objectivity and the sufficiency of the sum score, adds discrimination and "
              "guessing, measures information, fits the Law School Admission Test's items by marginal maximum "
              "likelihood (matching the published fits), builds an adaptive test that needs about half the items of "
              "the best fixed form, fits graded responses to attitude items, separates bias from impact with "
              "Mantel and Haenszel, links two forms through anchors, shows why national surveys report plausible "
              "values drawn from a conditioning model, and tracks learning with knowledge tracing and Elo.",
        handoff="What happens between a question and its answer is Part 46; ability and learning over time Part 47; "
                "response-time models Part 48; the weight of evidence Part 50.",
        outside="Part 3's classical test theory, Part 12's logistic functions and Part 44's latent variables; the "
                "logistic function, likelihood and Fisher information.",
        objectives={
            "U": ["Explain why a classical score depends on the test and an item's difficulty on the sample.",
                  "Read an item characteristic curve: difficulty, discrimination and guessing.",
                  "Say why a group gap on an item is not by itself evidence that the item is unfair."],
            "M": ["Derive the sufficiency of the sum score in the Rasch model and fit it by conditional ML.",
                  "Fit Rasch and two-parameter models by marginal ML with EM; compute item and test information, and "
                  "build an adaptive test.",
                  "Run a Mantel-Haenszel DIF analysis, a mean-sigma linking and a plausible-value analysis."],
            "D": ["Argue how response times, generated items or learning test-takers change what a calibrated scale "
                  "can claim."],
            "I": ["Plan an adaptive questionnaire: bank, stopping rule, exposure control and a DIF check."],
        },
        results=[
            ("Rasch model", r"P(X_{pi} = 1) = \frac{e^{\theta_p - b_i}}{1 + e^{\theta_p - b_i}}"),
            ("Sufficiency", r"P(\mathbf{x} \mid r) = e^{-\sum_i x_i b_i} / \gamma_r(e^{-b_1}, \dots, e^{-b_k})"),
            ("Item information", r"I_i(\theta) = a_i^2 P_i(\theta)(1 - P_i(\theta))"),
            ("Mantel-Haenszel", r"\hat\alpha_{MH} = \frac{\sum_s A_s D_s/N_s}{\sum_s B_s C_s/N_s}, \ \Delta = -2.35 \ln \hat\alpha_{MH}"),
            ("Mean-sigma linking", r"A = \mathrm{SD}(b^{old})/\mathrm{SD}(b^{new}), \ B = \bar b^{old} - A \bar b^{new}"),
        ],
        U=(0, 1, 2, 3, 9), D=(15,), I=(14,),
        also=(("Psyche's irt module", "explainer/psychology/psyche/irt.py"),
              ("Its tests", "tests/psychology/test_irt.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
