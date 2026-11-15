"""Act VIII, How people differ (Parts 32-33)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=32, level="U", widget="matrices",
        question="Is there one thing that the word \"intelligence\" measures?",
        story="In 1904 Charles Spearman found every school mark, and the skill of telling two tones apart, "
              "correlated positively with every other, and invented factor analysis to explain it with one general "
              "factor; the same year Paris asked Alfred Binet for a test to find children who needed help. Within "
              "twenty years American courts were citing test scores to justify sterilization. The part recomputes "
              "the positive manifold from Spearman's table and Holzinger and Swineford's 301 children, derives the "
              "factor model and its tetrads, rejects one factor in the real battery and accepts three, with the "
              "hierarchy above them. Psyche builds a common cause, Thomson's sampling and van der Maas's mutualism, "
              "all of which a one-factor test accepts, and the training experiment that tells them apart. Then the "
              "IQ scale and its error band, validity and range restriction, matrix items as rules held at once, "
              "heritability, schooling and the Flynn effect, group differences through invariance and Lewontin's "
              "two fields, the history of harm, and other intelligences: multiple, emotional and Mozart's.",
        handoff="Factor analysis on personality is Part 33; stereotype threat's full record is Part 36; intellectual "
                "disability and development are Part 41; latent variables and measurement invariance are Part 44; "
                "item response theory and adaptive tests are Part 45; selection at work is Part 53; schools, courts "
                "and machines are Parts 54, 56 and 60.",
        outside="Part 3's reliability and validity, Part 9's heritability, Part 19's working memory and Part 31's "
                "cohorts. Linear algebra, correlation, maximum likelihood and the normal distribution.",
        objectives={
            "U": ["Explain the positive manifold, the general factor and the hierarchy of abilities, and what an IQ "
                  "score is and is not.",
                  "Describe what intelligence scores predict, how heritable and how changeable they are, and the "
                  "replication records of the Flynn effect, schooling, the Mozart effect and multiple "
                  "intelligences.",
                  "Explain why a difference between group averages says little about individuals, and nothing on "
                  "its own about causes."],
            "M": ["Derive the one-factor model's tetrad differences and fit loadings by maximum likelihood; test one "
                  "factor against three on a real battery.",
                  "Simulate a common cause, a sampling world and a mutualism world, and show that a factor fit "
                  "cannot tell them apart.",
                  "Derive the standard error of a score, Thorndike's correction for range restriction, Kelley's "
                  "true-score estimate and Brogden's selection gain."],
            "D": ["Design an experiment that separates a common cause from mutualism, and judge network models "
                  "against g.",
                  "Judge what a polygenic score, a benchmark for machines or a measurement-invariance test can show."],
            "I": ["Evaluate a cutoff, a diagnostic rule or a hiring test for error, validity and adverse impact."],
        },
        results=[
            ("The one-factor model and its tetrads",
             r"r_{ij} = \lambda_i \lambda_j, \quad r_{ik} r_{jl} - r_{il} r_{jk} = 0"),
            ("Standard error of measurement", r"\mathrm{SEM} = \sigma\sqrt{1 - \rho}"),
            ("Thorndike's correction", r"r_c = \frac{r/u}{\sqrt{1 - r^2 + r^2/u^2}}"),
            ("Brogden's selection gain", r"E[Y \mid X > z] = r\,\frac{\phi(z)}{1 - \Phi(z)}"),
        ],
        U=(0, 1, 4, 6, 7, 9, 10, 11, 12, 13), D=(15,), I=(14,),
        also=(("Psyche's traits module", "explainer/psychology/psyche/traits.py"),
              ("Its tests", "tests/psychology/test_traits.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
