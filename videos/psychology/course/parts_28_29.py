"""Act VI, Feeling and Wanting (Parts 28-29)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=28, level="U", widget="discount",
        question="Why does a rat, or a person, do anything at all, and what do needs, rewards and goals each add?",
        story="In 1954 a rat with a misplaced electrode keeps returning to the corner of its box where a current came "
              "on, and given a lever it presses until exhausted. Psyche's learner shows why: a reward that bypasses "
              "the body's needs wins. From there the part climbs from homeostasis, a thermostat derived with its "
              "steady error, to hunger as a defended loop that makes diets regain; from curiosity and the "
              "Yerkes-Dodson law that was a story about mice, to wanting split from liking, with a cue whose value "
              "flips with the body's state and no new learning. Expected rewards undermine interest, explained as "
              "Bayesian self-perception; specific goals work; and the viewer measures their own discount curve. Then "
              "self-control, where famous findings fell: ego depletion, built from hundreds of small studies, pooled "
              "to d = 0.04 by twenty-three laboratories, recomputed here from their open data; the marshmallow test "
              "shrunk by controls and explained as rational waiting; grit nearly conscientiousness. Effort ends as a "
              "cost the brain chooses to pay.",
        handoff="Emotion is Part 29; wanting without liking returns in addiction, Part 41; incentives and goals at "
                "work are Part 53; grit and mindset in schools are Part 54; what machines should want is Part 60.",
        outside="Part 4's file drawer, Part 17's learner and Part 26's discounting. First-order differential equations, "
                "Bayes's rule, regression and meta-analysis.",
        objectives={
            "U": ["Describe homeostasis, drive reduction and its limits, and the signals that control hunger.",
                  "Distinguish wanting from liking, and intrinsic from extrinsic motivation.",
                  "Describe the ego-depletion, marshmallow and grit findings and what happened to each."],
            "M": ["Solve a proportional control loop, find its steady error, and remove it with an integral term.",
                  "Model energy balance with a settling point and a defended set point, and compute a diet's course.",
                  "Recompute a multi-laboratory meta-analysis from open data, and correct a literature for "
                  "small-study bias."],
            "D": ["Derive when giving up is rational from the distribution of waiting times.",
                  "State the expected value of control and the opportunity-cost account of effort, and design a test "
                  "between effort accounts."],
            "I": ["Judge an incentive scheme, a weight-loss programme or a habit app against the evidence on "
                  "motivation."],
        },
        results=[
            ("Proportional control", r"\dot x = -k(x - s) + D \ \Rightarrow \ x_\infty = s + D/k"),
            ("Energy balance", r"\rho\,\dot W = I - E_0 - a(W - W_0), \quad \Delta W_\infty = c/a, \ \tau = \rho/a"),
            ("Incentive salience", r"\tilde V(\text{cue}) = \gamma\,\kappa\, r"),
            ("Hyperbolic discounting", r"V = A / (1 + kD)"),
            ("Expected remaining wait", r"\mathbb{E}[T - t \mid T > t] = \int_t^\infty S(u)\,du \,/\, S(t)"),
            ("Expected value of control", r"u^* = \arg\max_u \ P(\text{success} \mid u)\,R - c(u)"),
        ],
        U=(0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13), D=(2, 12, 15), I=(14,),
        also=(("Psyche's drive module", "explainer/psychology/psyche/drive.py"),
              ("Its tests", "tests/psychology/test_drive.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
