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
    Part(
        n=35, level="U", widget="goals",
        question="How do you read a mind, including your own?",
        story="In 1959 students paid one dollar to call a dull task interesting came to like it more than students "
              "paid twenty. Festinger called it dissonance; Bem said people read their own attitudes from their "
              "behaviour as an observer would. The part follows that reading: Kelley's cube as an analysis of "
              "variance, the Castro essays and a rational observer of them, the 2024 test of dissonance in 39 "
              "laboratories that found no effect of choice, LaPiere's road trip and when attitudes predict, the "
              "self's flattering illusions and a Dunning-Kruger graph rebuilt from regression to the mean, faces "
              "judged in a tenth of a second, and two famous collapses, behavioural priming and power posing, with "
              "the winner's curse that explains them. Then the false-belief localizer, inverse planning (a goal "
              "read from a path by Bayes' rule with a planner inside), Nisbett and Wilson's stockings and choice "
              "blindness, and theory of mind in language models.",
        handoff="Groups, stereotypes and bias scores are Part 36; cooperation and trust Part 37; attribution across "
                "cultures Part 38; interviews and performance reviews Part 53; theory of mind in machines Part 60.",
        outside="Part 3's measurement, Part 4's false positives and power, Part 17's planner, and Part 30's "
                "false-belief tasks. Bayes' rule, analysis of variance, the bivariate normal and the truncated normal.",
        objectives={
            "U": ["Describe attribution, the correspondence bias, dissonance and self-perception, and what the "
                  "2024 multi-laboratory test found.",
                  "Explain when attitudes predict behaviour, and describe the better-than-average, false-consensus "
                  "and Dunning-Kruger effects.",
                  "Describe the elderly-priming and power-posing studies, their replications, and which kinds of "
                  "priming are solid."],
            "M": ["Decompose Kelley's cube as an analysis of variance, and infer an attitude from a forced essay by "
                  "Bayes' rule.",
                  "Derive the Dunning-Kruger graph from regression to the mean, and the winner's curse from a "
                  "truncated normal.",
                  "Infer an agent's goal from its path with an inverse planner, step by step."],
            "D": ["Evaluate claims that language models have a theory of mind, and design controls that separate "
                  "reasoning about minds from familiarity with the tasks.",
                  "Explain why a brain region that responds to a task is not yet a region for that task."],
            "I": ["Design interviews, reviews and user research that guard against snap impressions, the "
                  "correspondence bias and people's theories about their own behaviour."],
        },
        results=[
            ("Rational observer", r"P(\text{pro} \mid \text{pro essay}) = \frac{1}{1 + \pi}"),
            ("Regression to the mean", r"E[Y \mid X] = 50 + s + \rho\,(X - 50)"),
            ("Inverse planning", r"P(g \mid a_{1:t}) \propto P(g) \prod_k \frac{e^{-\beta Q_g(s_k, a_k)}}{\sum_a e^{-\beta Q_g(s_k, a)}}"),
            ("Winner's curse", r"E[\hat d \mid \hat d > c\sigma] = d + \sigma \frac{\varphi(a)}{1 - \Phi(a)},\ a = c - d/\sigma"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's social module", "explainer/psychology/psyche/social.py"),
              ("Its tests", "tests/psychology/test_social.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=36, level="U", widget="minimal",
        question="How little does it take to make a group, and what does a bias score mean?",
        story="Henri Tajfel, who survived the war as a prisoner, divided Bristol schoolboys by a trivial test, and they "
              "favoured their own group at once, often giving up points to stay ahead. The part follows social "
              "identity, Robbers Cave as run and as staged, stereotypes as categories and an illusory correlation, "
              "then three ways of measuring prejudice: asking (with a list experiment that reveals no one's answer), "
              "timing (the Implicit Association Test, its retest reliability near .5, its small correlations with "
              "behaviour, and 492 studies in which changing the score did not change behaviour), and behaviour "
              "itself (identical resumes, 50% more callbacks for white-sounding names, and no change in 25 years). "
              "Then stereotype threat and its registered test, contact and the 27 randomized studies, a radio drama "
              "in Rwanda, diversity training, a faked canvassing study and the real one that followed, and a ladder "
              "on which small biases compound.",
        handoff="Cooperation, trust and punishment are Part 37; culture and which findings travel Part 38; "
                "structured selection Part 53; field experiments and nudges Part 55; bias in machines Part 60.",
        outside="Part 3's reliability and attenuation, Part 4's power and filtered literatures, Part 22's categories "
                "and Part 25's diffusion model. Proportions, the normal distribution and conditional expectation.",
        objectives={
            "U": ["Describe the minimal-group studies, social identity theory and Robbers Cave, with what Perry's "
                  "archive changed.",
                  "Explain stereotypes as categories, the stereotype content model and illusory correlation.",
                  "Describe the IAT, audit studies, stereotype threat, contact and what prejudice-reduction "
                  "experiments have and have not shown."],
            "M": ["Read Tajfel's matrices and separate joint profit, ingroup profit and maximum difference.",
                  "Derive the list experiment's estimator and its variance, and size an audit study by power.",
                  "Model an IAT as diffusion decisions and show how reliability bounds prediction, and compute "
                  "how small biases compound on a promotion ladder."],
            "D": ["Evaluate whether implicit measures describe persons or situations, and design a test between the "
                  "accounts.",
                  "Judge a prejudice-reduction claim by its design: randomization, outcome, delay and setting."],
            "I": ["Design a hiring or promotion process that measures and reduces discrimination, and an evaluation "
                  "of a training."],
        },
        results=[
            ("List experiment", r"\hat\pi = \bar Y_{\text{treat}} - \bar Y_{\text{control}}"),
            ("Attenuation", r"r_{\text{obs}} \le r\sqrt{\rho_{xx}}"),
            ("Two-proportion sample size", r"n = \frac{(z_{\alpha/2} + z_{\beta})^2 [p_1(1-p_1) + p_2(1-p_2)]}{(p_1 - p_2)^2}"),
            ("Ladder", r"(1 - s)\,\bar\Phi(c - \delta) + s\,\bar\Phi(c) = k,\quad s' = s\,\bar\Phi(c) / k"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12), D=(14,), I=(13,),
        also=(("Psyche's social module", "explainer/psychology/psyche/social.py"),
              ("Its tests", "tests/psychology/test_social.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=37, level="U", widget="ultimatum",
        question="Why do people cooperate with strangers, and can a relationship be predicted?",
        story="Offer someone one coin out of ten, take it or both get nothing: a selfish responder accepts, yet "
              "proposers offer about 40% and low offers are rejected at a cost. The part follows cooperation from "
              "five economic games to its four routes (kin, reciprocity, reputation, punishment), a tournament of "
              "strategies, public goods that decay without punishment and hold up with it (unless cooperators are "
              "punished too), inequity aversion as a utility function, and the same game in fifteen small "
              "societies, where offers ran from 26% to 58%. Then the closest bargains: proximity and mere exposure, "
              "stated preferences that do not predict desire, machine learning that cannot predict the chemistry of "
              "a pair, 11,196 couples whose own perceptions predict their satisfaction, a divorce model that is "
              "90% accurate only on the couples it was fitted to, mate preferences in 45 countries, and the link "
              "between relationships and survival.",
        handoff="Culture and morals are Part 38; therapy's evidence Part 42; teams and incentives at work Part 53; "
                "games with machines Part 60.",
        outside="Part 17's reinforcement learning, Part 26's utility, and the game theory of Philosophy, Built Part "
                "34. Expected value, logistic and least-squares fitting, cross-validation and odds ratios.",
        objectives={
            "U": ["Describe the dictator, ultimatum, trust, prisoner's dilemma and public-goods games, what selfish "
                  "play predicts and what people do.",
                  "Explain kin selection, reciprocity, reputation and punishment, and what Fehr and Gachter and the "
                  "fifteen-society study found.",
                  "Describe the findings on proximity, mere exposure, stated preferences and relationship "
                  "prediction, and the association between social ties and survival."],
            "M": ["Derive an inequity-averse responder's threshold and a proposer's best offer against a population "
                  "of responders.",
                  "Simulate a public-goods game with and without punishment, and a tournament of repeated "
                  "prisoner's dilemma strategies.",
                  "Show why in-sample accuracy overstates prediction, and estimate accuracy by cross-validation."],
            "D": ["Separate actor, partner and relationship variance in dyadic data, and say what each can and cannot "
                  "predict.",
                  "Evaluate causal claims about social connection and health from observational data."],
            "I": ["Design a reputation system, a team incentive or a dating product's claim with the evidence in "
                  "view."],
        },
        results=[
            ("Inequity aversion", r"U_i = x_i - \alpha (x_j - x_i)^+ - \beta (x_i - x_j)^+"),
            ("Responder threshold", r"s^\* = \frac{\alpha}{1 + 2\alpha}"),
            ("Hamilton's rule", r"rB > C"),
            ("Proposer's problem", r"\max_s\, (1 - s)\, P(s \ge s^\*)"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12), D=(14,), I=(13,),
        also=(("Psyche's social module", "explainer/psychology/psyche/social.py"),
              ("Its tests", "tests/psychology/test_social.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
