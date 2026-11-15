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
    Part(
        n=33, level="U", widget="inventory",
        question="Is there a \"you\" that stays the same across situations and years?",
        story="In 1936 Allport and Odbert read a dictionary for people and found 17,953 words; Cattell's sixteen "
              "factors, Tupes and Christal's five and the NEO followed, and a sixth, honesty-humility, appeared in "
              "seven languages. The part recomputes the five in the SAPA project's 2,800 people: parallel analysis "
              "keeps five and every item finds its factor. Types cut one hump in two and change on retest by the "
              "arcsine law. Hartshorne and May's children and Mischel's .30 are rebuilt in a world of people and "
              "situations, and Epstein's aggregation turns .3 into .9 by Spearman-Brown; Funder and Ozer show "
              "situations are no larger, and Fleeson and Mischel and Shoda make traits distributions and if-then "
              "signatures. Then stability and change, heritability and Eysenck and Gray, Soto's 78 replications, "
              "Freud and the inkblots under Part 3's standards, sex differences in one dimension and many, and "
              "personality read from likes, Cambridge Analytica and psychological targeting.",
        handoff="Situations that move people are Part 34; disorders as continua are Part 39; latent variables "
                "against networks are Part 44; item response theory and faking are Part 45; personality at work is "
                "Part 53; minds and machines are Part 60.",
        outside="Part 3's reliability, validity and Spearman-Brown, Part 9's heritability and Part 32's factor "
                "analysis. Correlation, the normal distribution, eigenvalues and regression.",
        objectives={
            "U": ["Describe the five-factor model, where it came from, and its six-factor variant.",
                  "Explain the person-situation debate and how aggregation resolved it.",
                  "Describe stability and change, heritability, outcomes and sex differences in personality, with "
                  "their replication records."],
            "M": ["Score an inventory with reverse keys, choose factors by parallel analysis, and fit and rotate them.",
                  "Derive the Spearman-Brown aggregation curve, the arcsine law for type agreement and the median "
                  "split's loss.",
                  "Compute univariate d and Mahalanobis's D, and explain why D grows with the number of traits."],
            "D": ["Judge whether traits are latent causes or network summaries, and design a study that could tell.",
                  "Evaluate claims of universality and of persuasion by psychological targeting."],
            "I": ["Evaluate a hiring test, a type workshop, a matching product or a targeting campaign against the "
                  "evidence."],
        },
        results=[
            ("Aggregation", r"r_k = \frac{k\rho}{1 + (k - 1)\rho}"),
            ("Same type on retest", r"P = \tfrac12 + \frac{\arcsin r}{\pi}"),
            ("A median split keeps", r"\sqrt{2/\pi} \approx 0.80"),
            ("Mahalanobis distance", r"D^2 = \Delta\mu^{\top} \Sigma^{-1} \Delta\mu"),
        ],
        U=(0, 1, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13), D=(15,), I=(14,),
        also=(("Psyche's personality module", "explainer/psychology/psyche/personality.py"),
              ("Its tests", "tests/psychology/test_personality.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
