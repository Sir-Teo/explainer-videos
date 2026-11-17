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
    Part(
        n=29, level="U", widget="faces",
        question="Do we run because we are afraid, or are we afraid because we run, and what is an emotion made of?",
        story="In 1884 William James says the second: the feeling is the body's reaction, perceived. Cannon objects "
              "that the body is too slow and too much alike across emotions, and Schachter and Singer's adrenaline "
              "adds a label, here written as Bayesian attribution of unexplained arousal; a swaying bridge in North "
              "Vancouver becomes the famous case. Then faces: Ekman's six basic emotions in New Guinea, strong with a "
              "list to choose from and weaker without one, and a map of feelings recovered by classical scaling from "
              "judgments of faces made in 1962, then from the viewer's own. Constructed emotion argues the categories "
              "are built. A pen held in the teeth made cartoons funnier in 1988; seventeen laboratories found almost "
              "nothing; the meta-analysis of 286 effects, recomputed here, finds a small effect. Appraisal is "
              "computed, LeDoux's two roads to the amygdala are simulated, and patient S.M. fears nothing outside "
              "her body. Regulation, forecasting and money and happiness follow, the last reconciled by an "
              "adversarial collaboration, and the part ends with a ratio from fluid dynamics that a graduate student "
              "and a physicist took apart.",
        handoff="Act VII begins with the infant mind in Part 30; fear and sadness as disorders are Part 40; "
                "reappraisal as therapy is tested in Part 42; scaling returns in Part 46; emotion as prediction of "
                "the body in Part 58; machines that read feelings in Part 60.",
        outside="Part 3's measurement, Part 4's meta-analysis, Part 10's hormone loops, Part 14's inference and Part "
                "16's fear conditioning. Eigenvectors, the singular value decomposition, Bayes's rule and "
                "exponential decay.",
        objectives={
            "U": ["Compare the James-Lange, Cannon-Bard, two-factor, basic-emotion, appraisal and constructionist "
                  "accounts of emotion.",
                  "Describe the facial-feedback, bridge and universal-recognition findings and their replication "
                  "records.",
                  "Explain the impact bias, and how a plateau in emotional well-being can hold for some people "
                  "only."],
            "M": ["Derive classical scaling from a table of distances, and align two maps by Procrustes.",
                  "Recompute a random-effects meta-analysis from its open table, with groups and the "
                  "precision-effect test.",
                  "Write unexplained arousal as a Bayesian attribution, and compute an appraisal model's labels."],
            "D": ["Design a study that the basic-emotion and constructed-emotion accounts predict differently.",
                  "Judge when a mathematical model in a psychology paper is fitted to data and when it is only "
                  "borrowed."],
            "I": ["Evaluate an emotion-recognition product or a well-being survey against what the evidence "
                  "supports."],
        },
        results=[
            ("Classical scaling", r"B = -\tfrac12 J D^{(2)} J = X X^\top"),
            ("Orthogonal Procrustes", r"X^\top Y = U \Sigma V^\top \ \Rightarrow \ R^* = U V^\top"),
            ("Attribution of arousal",
             r"s \mid a \sim N\!\left(a - c - \sigma^2/m,\ \sigma^2\right) \text{ on } s \ge 0"),
            ("Random effects", r"\hat\mu = \frac{\sum_i w_i y_i}{\sum_i w_i}, \quad w_i = \frac{1}{v_i + \hat\tau^2}"),
            ("Hedonic adaptation", r"h(t) = h_0 + I\, e^{-t/\tau}"),
        ],
        U=(0, 1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13), D=(2, 4, 15), I=(14,),
        also=(("Psyche's emotion module", "explainer/psychology/psyche/emotion.py"),
              ("Its tests", "tests/psychology/test_emotion.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
