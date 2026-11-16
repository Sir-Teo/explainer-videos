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
]
