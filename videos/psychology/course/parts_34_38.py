"""Act IX, Other people (Parts 34-38)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=34, level="U", widget="lines",
        question="How much of what you do is decided by who is in the room?",
        story="In the summer of 1961, in a basement at Yale, an experimenter in a grey coat told ordinary men to give "
              "another man electric shocks, and 26 of 40 went to the last switch. The part tells the famous studies "
              "as they were run, as they were retold and as the record now shows them: Sherif's moving light and "
              "Asch's lines, with Bond and Smith's 133 studies and a 2023 replication at 33%; Milgram's variations "
              "as a dose-response curve from 0% to 92.5%, Burger's partial replication and Perry's archives, where "
              "only about half fully believed; the prison study's coaching and the BBC study's different result; "
              "the 38 witnesses as a parable, the bystander effect in the laboratory, and cameras showing help in "
              "nine of ten street fights. Then audiences, loafing, polarization, groupthink, a consistent minority, "
              "the hidden profile and persuasion's two routes. Psyche computes what the famous studies never had: "
              "Granovetter's thresholds, DeGroot's consensus, bounded confidence, simple and complex contagion, the "
              "diversity identity behind Galton's ox, and a music market where social information makes hits "
              "unequal and unpredictable.",
        handoff="Reading minds, including your own, is Part 35; groups against groups are Part 36; cooperation and "
                "punishment are Part 37; culture as social learning is Part 38; field experiments and nudges are "
                "Part 55; minds and machines are Part 60.",
        outside="Part 2's experiments, Part 4's replication record and Part 17's reinforcement learning. Probability, "
                "matrices and eigenvectors, and the binomial distribution.",
        objectives={
            "U": ["Describe Asch's, Milgram's and Darley and Latané's studies, what later work found, and what the "
                  "archives changed.",
                  "Explain why the Stanford prison experiment and the 38 witnesses are stories that outran their "
                  "records.",
                  "Describe social facilitation, social loafing, group polarization, minority influence and the two "
                  "routes to persuasion."],
            "M": ["Solve Granovetter's threshold model and show how one changed threshold flips a crowd.",
                  "Derive DeGroot's consensus as a left-eigenvector average, and simulate bounded confidence and "
                  "simple and complex contagion on networks.",
                  "Prove the diversity prediction identity, and compute the bystander and information-sampling "
                  "formulas."],
            "D": ["Explain why influence and homophily are confounded in observational network data, and design a "
                  "study that separates them.",
                  "Evaluate claims about algorithmic amplification and experiments on millions of users."],
            "I": ["Design a committee, rating system or seeding campaign that uses, or guards against, social "
                  "influence."],
        },
        results=[
            ("Granovetter's equilibrium", r"n^\* = \min\{k : F(k) = k\}"),
            ("DeGroot consensus", r"x_\infty = \pi^{\top} x_0,\quad \pi^{\top} W = \pi^{\top}"),
            ("Diversity prediction", r"(\bar x - \theta)^2 = \overline{(x_i - \theta)^2} - \overline{(x_i - \bar x)^2}"),
            ("Someone helps", r"1 - (1 - p_N)^N"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's social module", "explainer/psychology/psyche/social.py"),
              ("Its tests", "tests/psychology/test_social.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
