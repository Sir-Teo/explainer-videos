"""Acts III and IV, Knowledge and Science: credence, revision, induction, statistics, cause, theories (Parts 13-18)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=13, level="U", widget="dutchbrier", prereq=(11, 12),
        question="What laws must degrees of belief obey, and why those laws rather than others?",
        story="The part opens on a forecast of seventy percent rain: not knowledge, not plain belief, but a degree "
              "of confidence. Ramsey and de Finetti measure it by betting prices, Kolmogorov's axioms turn credences "
              "into points on a simplex, and two arguments say why a credence must lie there. A bookie, found by a "
              "linear program, takes a sure profit from any point off the simplex; Joyce's accuracy argument shows "
              "that the nearest point on the simplex is closer to the truth in every world. Proper scoring rules "
              "make honest reports pay, conditionalization and Jeffrey's rule say how credences move, and the "
              "problem of the priors asks where they start. There the part turns: Bertrand's three ways of drawing a "
              "random chord give 1/3, 1/2 and 1/4, so indifference is not well defined, and this is the Wall's "
              "thirteenth brick. It ends with what the framework strains to hold: chance, imprecise credences and "
              "dilation, the lottery and the preface, Sleeping Beauty, the Doomsday argument, and the cost of exact "
              "Bayesian inference.",
        handoff="The probability of conditionals and Lewis's triviality theorem follow in Part 14, confirmation and "
                "induction in Part 15, Bayesian against frequentist statistics in Part 16, chance and the big bad "
                "bug in Part 24, decisions under uncertainty and Ellsberg again in Part 33, and calibrated, fair "
                "machines in Parts 41 and 42.",
        outside="School algebra and fractions; the idea of a fair bet. The linear program and the separating "
                "hyperplane are drawn, not assumed.",
        objectives={
            "U": ["Build a Dutch book against credences that break the addition law, and compute the sure loss.",
                  "Update a credence by Bayes' rule on a positive test and explain the role of the base rate.",
                  "Explain why Bertrand's three chord ensembles give three answers to one question."],
            "M": ["Prove that a strictly proper scoring rule is minimized in expectation by reporting one's own "
                  "credence, for the Brier and logarithmic rules.",
                  "Compute the projection of an incoherent credence onto the simplex and verify that it has a "
                  "smaller Brier score in every world.",
                  "Apply Jeffrey's rule when the evidence shifts a partition without making any cell certain."],
            "D": ["State the Dutch book theorem with its converse as a separating hyperplane result, and say which "
                  "step of the accuracy argument needs the scoring rule to be strictly proper.",
                  "Compute the dilation of a precise credence across a credal set, and set out Elga's objection "
                  "and the replies."],
            "I": ["Score a set of probability forecasts with the Brier and log rules, bin them for calibration, "
                  "and say what each number rewards.",
                  "Explain why exact inference in a Bayesian network grows with the size of the joint table."],
        },
        results=[
            ("Dutch book theorem and converse",
             r"c \text{ admits a book with a sure loss} \iff c \text{ violates the probability axioms}"),
            ("Accuracy dominance (Brier score; pi projects onto the simplex)",
             r"c \notin \Delta \ \Longrightarrow\ \lVert \pi(c) - v_w \rVert^2 < \lVert c - v_w \rVert^2 "
             r"\ \text{ for every world } w"),
            ("Strict propriety of the Brier rule",
             r"\arg\min_q \bigl[\, p\,(1-q)^2 + (1-p)\,q^2 \,\bigr] = p"),
            ("Conditionalization", r"P_{\text{new}}(H) = P(H \mid E) = \frac{P(E \mid H)\,P(H)}{P(E)}"),
            ("Jeffrey's rule", r"P_{\text{new}}(A) = \sum_i P(A \mid E_i)\,P_{\text{new}}(E_i)"),
            ("Bertrand's chords",
             r"P(\text{chord} > \sqrt{3}) = \tfrac13 \ (\text{endpoints}),\quad \tfrac12 \ (\text{radius}),\quad "
             r"\tfrac14 \ (\text{midpoint})"),
        ],
        U=(0, 1, 2, 5, 7, 11), I=(4, 13), D=(9, 12),
        also=(("The Reasoner's credence laboratory", "explainer/philosophy/reasoner/credence.py"),),
    ),
    Part(
        n=14, level="U", widget="grovespheres", prereq=(2, 4, 13),
        question="When a new fact contradicts what you believe, which beliefs should you give up?",
        story="You believe that all swans are white, that this bird is a swan and that your eyes are reliable; then "
              "you see that the bird is black. Logic says something must go and does not say what. The part builds "
              "the logic of that choice: expansion, revision and contraction, the AGM postulates checked "
              "exhaustively by the Reasoner for four operators, and Grove's spheres, in which revising by A means "
              "moving to the most plausible A-worlds. Spohn's ranks carry the spheres through repeated change, and "
              "an operator that forgets them loses a red bird's flight. Then the part turns to the sentences that "
              "guide change. The Ramsey test ties conditionals to revision, and Gärdenfors's theorem shows the two "
              "cannot coexist; Lewis's triviality theorem shows that the probability of a conditional is not the "
              "probability of any proposition. Together they are the Wall's fourteenth brick. The rest is reasoning "
              "that can be withdrawn: McGee's counterexample to modus ponens, Reiter's defaults and Tweety, System P "
              "and System Z, Dung's arguments that attack each other, and machines, from truth maintenance to "
              "knowledge editing in language models.",
        handoff="Induction and confirmation follow in Part 15; counterfactuals carry causation in Part 17; theory "
                "change in science is Part 18; laws and chance return in Part 24; causal decision theory, which "
                "chooses by imaging, is in Part 33; machines that reason, revise and argue return in the finale.",
        outside="Truth tables (Part 2) and the idea of a possible world (Part 4). Conditional probability for "
                "Chapter 8, as in Part 13.",
        objectives={
            "U": ["Carry out an expansion, a revision and a contraction on a small system of spheres and say what "
                  "is believed afterwards.",
                  "Evaluate a counterfactual on a model of closest worlds, and show why strengthening the "
                  "antecedent fails.",
                  "Compute the grounded extension of a small argumentation framework and label each argument in, "
                  "out or undecided."],
            "M": ["Check the AGM postulates for a given revision operator and produce a counterexample where one "
                  "fails, as for Satoh's operator and subexpansion.",
                  "Derive revision from contraction by the Levi identity and contraction from revision by the "
                  "Harper identity.",
                  "Test four iterated revision operators against the Darwiche-Pearl postulates on a ranking."],
            "D": ["Prove Gärdenfors's impossibility theorem on three pairwise incompatible propositions, and "
                  "Lewis's triviality theorem for a class of credences closed under conditioning.",
                  "State System P and rational monotonicity, and explain what System Z's ranking adds and where it "
                  "drowns."],
            "I": ["Compare AGM revision with a local edit of one stored fact, and say which consequences each "
                  "leaves stale.",
                  "Compute the certain answers of a query over the repairs of an inconsistent database."],
        },
        results=[
            ("Grove's spheres", r"\lVert K * A \rVert = \min\nolimits_{\le}\, \lVert A \rVert"
                                r"\quad\text{(the most plausible } A\text{-worlds)}"),
            ("Levi and Harper identities", r"K * A = (K \div \lnot A) + A,\qquad K \div A = K \cap (K * \lnot A)"),
            ("Gärdenfors's theorem (Ramsey test: A > C in K iff C in K * A)",
             r"\text{Ramsey test} + \text{preservation} \ \Longrightarrow\ \text{no consistent } H * (B \lor C)"),
            ("Lewis's truth condition",
             r"w \models A \mathrel{\Box\!\!\to} C \iff C \text{ holds at every closest } A\text{-world to } w"),
            ("Lewis's triviality (for a class of credences closed under conditioning)",
             r"\forall P \in \mathcal{C}:\ P(A \to C) = P(C \mid A) \ \Longrightarrow\ P(C \mid A) = P(C)"),
            ("Dung's grounded extension",
             r"G = \bigcup_n F^n(\varnothing),\qquad F(S) = \{a : S \text{ attacks every attacker of } a\}"),
        ],
        U=(0, 1, 5, 7, 10, 12), I=(13,), D=(6, 8, 11),
        also=(("The Reasoner: revision", "explainer/philosophy/reasoner/revision.py"),
              ("The Reasoner: conditionals", "explainer/philosophy/reasoner/cond.py"),
              ("The Reasoner: defeasible reasoning and argumentation", "explainer/philosophy/reasoner/argue.py")),
    ),
    Part(
        n=15, level="U", widget="mergingpriors", prereq=(13, 14),
        question="Can the evidence of the past tell us anything at all about the future?",
        story="Russell's chicken expects breakfast every morning, with growing confidence, until the morning the "
              "farmer comes with a knife. Hume's argument says no past regularity entails anything about the "
              "future, and that any defence of induction by its record runs in a circle. The part collects the "
              "answers. Laplace's rule of succession and Carnap's continuum put the problem into a prior; Dignāga's "
              "wheel of reasons and the Cārvāka skeptic met it a thousand years earlier. Three paradoxes of "
              "confirmation follow: Hempel's ravens, measures that rank the same evidence oppositely, and Goodman's "
              "grue, reproduced in eight small neural networks that agree on the data and disagree after T. Popper, "
              "inference to the best explanation and the merging of opinions each help and each fall short. Then "
              "the question changes from justification to reliability: learning in the limit, Gold's adversary, "
              "Kelly's justification of Ockham's razor, Solomonoff's universal prior and MDL. The turn is Wolpert's "
              "no free lunch theorem, proved on all 256 worlds over three bits, the Wall's fifteenth brick: every "
              "learner bets on a kind of world. It ends with Reichenbach's pragmatic vindication and Schurz's "
              "meta-induction, whose regret bound holds for every sequence.",
        handoff="Significance tests, likelihoods and Bayes factors follow in Part 16; learning causes from data in "
                "Part 17; underdetermination and realism in Part 18; laws and chance in Part 24; inductive bias in "
                "learning machines in Parts 41 and 42, and goal misgeneralization, an agent that learned grue when "
                "we meant green, in the finale.",
        outside="Bayes' rule as in Part 13. One integral (the Beta integral behind Laplace's rule) is stated and "
                "left as a problem.",
        objectives={
            "U": ["State Hume's argument and show where an inductive justification of induction is circular.",
                  "Compute a prediction with Laplace's rule of succession and say what its prior assumes.",
                  "Prove no free lunch for one training set by counting the worlds that agree with the labels seen."],
            "M": ["Compute the Bayes factors of a black raven and of a white shoe for 'all ravens are black', and "
                  "say which premise of the paradox the Bayesian gives up.",
                  "Evaluate two pieces of evidence on six confirmation measures and exhibit a reversal of their "
                  "ranking.",
                  "Simulate two Bayesians with opposed priors merging, and one whose prior rules out the truth."],
            "D": ["Prove Gold's theorem by constructing the adversary, and Putnam's diagonal sequence against a "
                  "computable predictor.",
                  "State Kelly's Ockham efficiency theorem and Solomonoff's error bound, and say what each does "
                  "and does not claim about simplicity and truth."],
            "I": ["Choose a polynomial degree by two-part MDL and relate the code length to prediction error.",
                  "Name the inductive bias of a given learner and describe a world in which that bet loses."],
        },
        results=[
            ("Rule of succession and Carnap's continuum",
             r"P(X_{n+1} = 1 \mid s \text{ of } n) = \frac{s+1}{n+2},\qquad "
             r"c_\lambda = \frac{s + \lambda/2}{n + \lambda}"),
            ("The Bayesian ravens",
             r"\frac{P(\text{black raven} \mid H)}{P(\text{black raven} \mid H')} \approx 1.0101,\qquad "
             r"\frac{P(\text{white shoe} \mid H)}{P(\text{white shoe} \mid H')} \approx 1.0000011"),
            ("Merging of opinions (Blackwell-Dubins)",
             r"P \ll Q \ \Longrightarrow\ \sup_A \bigl|P(A \mid x_1 \dots x_n) - Q(A \mid x_1 \dots x_n)\bigr| \to 0"
             r"\quad Q\text{-almost surely}"),
            ("Gold's theorem",
             r"\text{no learner identifies in the limit, from positive data, } "
             r"\{\text{all finite sets}\} \cup \{\mathbb{N}\}"),
            ("No free lunch",
             r"\frac{1}{2^{|X|}} \sum_{f : X \to \{0,1\}} \operatorname{acc}_{\text{off-training}}(L, f) = \tfrac12"
             r"\quad\text{for every learner } L"),
            ("Meta-induction's regret", r"L_T - \min_{i \le N} L_{i,T} \le \sqrt{\tfrac{T}{2} \ln N}"
                                        r"\quad\text{for every sequence}"),
        ],
        U=(0, 1, 2, 4, 6, 7, 14), I=(13,), D=(10, 11, 12),
        also=(("The Reasoner: induction", "explainer/philosophy/reasoner/induction.py"),),
    ),
    Part(
        n=16, level="U", widget="peekbet", prereq=(13, 15),
        question="When the numbers come in, how much do they tell us, and is a significant result real?",
        story="In 2015 the Open Science Collaboration repeated a hundred psychology studies: ninety-seven originals "
              "had been significant, thirty-six replications were. To ask whether the method, its use or its "
              "reading is at fault, the part first says what the numbers mean. Fisher, Neyman and Pearson, and "
              "Jeffreys give three verdicts on one coin with 60 heads in 100. A p-value is defined and six "
              "misreadings are refuted by simulation; base rates, Ioannidis's positive predictive value, the garden "
              "of forking paths and optional stopping show how noise becomes discovery. Then the part turns to "
              "principle. Two experimenters with the same nine heads and three tails get p = 0.073 and p = 0.033, "
              "and Birnbaum's theorem shows that sufficiency and conditionality together force the likelihood "
              "principle, under which the sampling plan cannot matter: the Wall's sixteenth brick. Lindley's "
              "paradox, Mayo's severity, Simpson's paradox at Berkeley and the reference class problem mark how far "
              "apart the schools land. It ends in practice and at the frontier: A/B tests ruined by peeking, "
              "testing by betting with Ville's inequality, and AIC against BIC.",
        handoff="Simpson's paradox, randomized trials and causal graphs follow in Part 17; underdetermination and "
                "the choice between truth and prediction in Part 18; frequencies and propensities in Part 24; "
                "tests as decisions in Part 33; reference classes and fair risk scores in Part 41; the statistics "
                "of evaluating machines in the finale.",
        outside="Bayes' rule and credences as in Part 13; the normal curve and a sample mean from a first "
                "statistics course help but are shown.",
        objectives={
            "U": ["State what a p-value is, and refute by a simulation or a count the reading 'the probability "
                  "that the null hypothesis is true'.",
                  "Compute the chance that a positive result is a true one from the base rate, the power and the "
                  "false positive rate, in natural frequencies.",
                  "Exhibit Simpson's reversal in a two-by-two-by-two table and say which comparison answers which "
                  "question."],
            "M": ["Simulate optional stopping and show the false rejection rate rising with the number of looks.",
                  "Compute a Bayes factor for a point null against a normal alternative and reproduce Lindley's "
                  "paradox at fixed z as n grows.",
                  "Draw a severity curve for a significant and a non-significant result and name the fallacy each "
                  "one blocks."],
            "D": ["Prove Birnbaum's theorem on the mixture experiment, and locate the step that Durbin, "
                  "Kalbfleisch and Mayo each reject.",
                  "Prove Ville's inequality for a nonnegative martingale and derive the Kelly stake that maximizes "
                  "an e-process's growth rate."],
            "I": ["Run an A/B test with a rule that stays valid under peeking, and say what a fixed-horizon "
                  "p-value means after ten looks.",
                  "Report a result with its design: the stopping rule, the number of analyses tried, and an "
                  "interval, and say which of these a p-value alone hides."],
        },
        results=[
            ("The p-value, and its law under the null",
             r"p = P(T \ge t_{\text{obs}} \mid H_0),\qquad P(p \le \alpha \mid H_0) = \alpha"),
            ("Positive predictive value (Ioannidis)",
             r"\mathrm{PPV} = \frac{(1-\beta)\,R}{(1-\beta)\,R + \alpha},\qquad R = \text{pre-study odds}"),
            ("Birnbaum: sufficiency (S) and conditionality (C) give the likelihood principle",
             r"\text{S} + \text{C} \ \Longrightarrow\ \bigl[\, L_1 \propto L_2 \ \Rightarrow\ "
             r"\operatorname{Ev}(E_1, x_1) = \operatorname{Ev}(E_2, x_2) \,\bigr]"),
            ("Lindley's paradox",
             r"B_{01} = \sqrt{1 + \tfrac{n\tau^2}{\sigma^2}}\ \exp\Bigl(-\tfrac{z^2}{2}\,"
             r"\tfrac{n\tau^2}{\sigma^2 + n\tau^2}\Bigr) \to \infty \quad (n \to \infty,\ z \text{ fixed})"),
            ("Ville's inequality",
             r"W_t \ge 0 \text{ a martingale under } H_0,\ W_0 = 1 \ \Longrightarrow\ "
             r"P\bigl(\sup_t W_t \ge 1/\alpha\bigr) \le \alpha"),
            ("Kelly's stake", r"g(\lambda) = p \ln(1+\lambda) + (1-p)\ln(1-\lambda),\qquad "
                              r"\arg\max_\lambda g = 2p - 1"),
        ],
        U=(0, 1, 2, 3, 4, 9), I=(11,), D=(6, 12),
        also=(("The Reasoner: stats", "explainer/philosophy/reasoner/stats.py"),),
    ),
    Part(
        n=17, level="U", widget="seeingdoing", prereq=(13, 14, 16),
        question="What does it mean for one thing to cause another, and how can data ever show it?",
        story="Doll and Hill find that heavy smokers get lung cancer many times as often as non-smokers; Fisher "
              "answers that a gene might cause both, and Cornfield replies with an inequality. To say what was "
              "shown, the part first tries the classical analyses: Hume's two definitions and al-Ghazālī's cotton, "
              "Mill's methods and Mackie's INUS conditions, Lewis's counterfactual dependence, which Suzy and "
              "Billy's rocks break, and probability-raising, which Hesslow's pills break. Russell's challenge and "
              "Woodward's interventions lead to the turn: a structural causal model, in which doing is surgery on "
              "a graph and differs from seeing. The back-door and front-door formulas recover the effect of an "
              "intervention from observation, and Pearl's do-calculus says exactly when that is possible. On the "
              "ladder of causation counterfactuals sit one rung higher; Halpern and Pearl's definition of actual "
              "causation is run on six classic cases. Discovery has a limit, the Wall's seventeenth brick: graphs "
              "with the same skeleton and colliders imply the same independences, so observation alone cannot "
              "choose among them. The part ends with potential outcomes, causal inference in industry, and Kim's "
              "exclusion argument about the mind.",
        handoff="Causal explanation and underdetermination follow in Part 18; laws, chance and the direction of "
                "causation in Part 24; Bell's correlations in Part 26; mental causation in Part 30; determinism "
                "and free will in Part 32; causal decision theory and Newcomb's problem in Part 33; counterfactual "
                "fairness and responsibility in Part 41.",
        outside="Conditional probability and Bayes' rule as in Part 13; Simpson's paradox from Part 16. No "
                "statistics beyond proportions is assumed.",
        objectives={
            "U": ["Apply the but-for test to a case of late preemption and say why counterfactual dependence is "
                  "not necessary for causation.",
                  "Compute the effect of an intervention in a small structural model and contrast it with the "
                  "conditional probability that was observed.",
                  "Answer one question about a firing squad on each rung: association, intervention, "
                  "counterfactual."],
            "M": ["Decide d-separation queries on a graph, and use the back-door criterion to choose an adjustment "
                  "set.",
                  "Apply the front-door formula when the confounder is hidden, and check it against the model's "
                  "interventional truth.",
                  "Test a candidate cause against the Halpern-Pearl definition, and list a graph's Markov "
                  "equivalence class."],
            "D": ["State the three rules of the do-calculus with their graphical side conditions and derive the "
                  "front-door formula from them.",
                  "State the causal Markov and faithfulness conditions, and explain how Bell's correlations and "
                  "exact cancellations violate each."],
            "I": ["Estimate an effect from an experiment with a pre-period covariate (CUPED) and say what the "
                  "adjustment buys.",
                  "Distinguish targeting by predicted response from targeting by uplift, and say which design "
                  "licenses a causal claim."],
        },
        results=[
            ("Causal Markov factorization", r"P(v_1, \dots, v_n) = \prod_i P\bigl(v_i \mid \mathrm{pa}_i\bigr)"),
            ("Intervention as surgery",
             r"P\bigl(v \mid do(X = x)\bigr) = \prod_{i\,:\,V_i \ne X} P\bigl(v_i \mid \mathrm{pa}_i\bigr)"
             r"\Big|_{X = x}"),
            ("Back-door adjustment", r"P\bigl(y \mid do(x)\bigr) = \sum_z P(y \mid x, z)\,P(z)"),
            ("Front-door adjustment",
             r"P\bigl(y \mid do(x)\bigr) = \sum_m P(m \mid x) \sum_{x'} P(y \mid m, x')\,P(x')"),
            ("Do-calculus, rule 2 (action and observation exchange)",
             r"P(y \mid do(x), do(z), w) = P(y \mid do(x), z, w)\quad\text{if } "
             r"(Y \perp Z \mid X, W)_{G_{\overline{X}\,\underline{Z}}}"),
            ("Markov equivalence (Verma and Pearl)",
             r"G_1 \sim G_2 \iff \text{same skeleton and same v-structures } a \to c \leftarrow b"),
        ],
        U=(0, 1, 2, 3, 5, 7, 9), I=(14,), D=(8, 11),
        also=(("The Reasoner: causal", "explainer/philosophy/reasoner/causal.py"),),
    ),
    Part(
        n=18, level="U", widget="blockspins", prereq=(15, 16, 17),
        question="Does evidence fix theory, and do our best theories tell us what the world is really like?",
        story="In 1897 Thomson watches a glowing beam bend and infers the electron, which no one has ever seen; "
              "Putnam says realism is the only philosophy that does not make the success of science a miracle. The "
              "part tests that sentence. It starts with what makes a statement scientific and what makes it "
              "explain: the Vienna Circle's verification principle, trivialized by Church in one paragraph, "
              "Hempel's laws and Bromberger's flagpole, unification with Newton's moon test, and mechanisms. Then "
              "how science changes: Kuhn's revolutions, with the Copernican one computed, Lakatos, Feyerabend and "
              "Laudan. The turn is the realism debate. Two Newtonian worlds and a loose cable at OPERA show that "
              "evidence underdetermines theory; the no-miracles argument depends on a base rate nobody knows; and "
              "Laudan's list of successful, rejected theories turns history against the inference from success to "
              "truth: the Wall's eighteenth brick. Structural realism, with Fresnel's equations surviving the "
              "aether, and constructive empiricism are the two middle ways. The part ends with reduction and "
              "emergence, where an Ising model is coarse-grained to its fixed point, and with models, "
              "demarcation, values in science and machines that discover.",
        handoff="Mechanisms and explanation in biology follow in Part 19; laws of nature and chance in Part 24; "
                "absolute space and symmetry in Part 25; realism about quantum theory in Part 26; multiple "
                "realizability in Part 30; inductive risk and fair algorithms in Part 41; machines that do science "
                "in the finale.",
        outside="Bayes' rule with base rates (Parts 13 and 16). School physics helps for the moon test, the "
                "pendulum and Fresnel's equations, which are computed on screen.",
        objectives={
            "U": ["State the deductive-nomological model and use the flagpole to show that derivation from a law "
                  "is not sufficient for explanation.",
                  "Compute the probability that a successful theory is true for a given base rate, and say what "
                  "the no-miracles argument leaves out.",
                  "Set out the realism trilemma and say which claim the anti-realist, the selective realist and "
                  "Fahrbach each give up."],
            "M": ["Reproduce Church's trivialization of Ayer's 1946 criterion and check each entailment.",
                  "Show that two Newtonian worlds differing by a uniform velocity agree on every relative quantity, "
                  "and say what follows for underdetermination.",
                  "Explain what Fresnel's equations carry from the elastic aether into Maxwell's theory, and state "
                  "Newman's objection to structural realism."],
            "D": ["Coarse-grain a sampled Ising lattice by block spins and identify from the flow of the neighbour "
                  "correlation whether it is below, at or above the critical temperature.",
                  "Assess Batterman's claim that universality needs an explanation that discards detail, against "
                  "Butterfield's reply that emergence and reduction are compatible."],
            "I": ["Choose a decision threshold under stated costs of false positives and false negatives, and say "
                  "where the value judgment enters (inductive risk).",
                  "Evaluate a claim of automated discovery: what was searched, what was given, and what would "
                  "count as an explanation."],
        },
        results=[
            ("Deductive-nomological explanation (laws L, conditions C, explanandum E)",
             r"L_1, \dots, L_k,\ C_1, \dots, C_r \vdash E"),
            ("Newton's moon test",
             r"a_{\text{Moon}} = \frac{4\pi^2 r}{T^2} \approx \frac{g}{60^2}\qquad (r \approx 60\,R_{\text{Earth}})"),
            ("No miracles, with the base rate",
             r"P(\text{true} \mid \text{success}) = \frac{0.95\,b}{0.95\,b + 0.05\,(1-b)} = 0.16"
             r"\ \text{ at base rate } b = 0.01"),
            ("The realism trilemma",
             r"\text{success shows truth};\ \ \text{past successes were false};\ \ "
             r"\text{we are no better placed}\ \vdash \bot"),
            ("Brewster's angle (Fresnel, kept by Maxwell)",
             r"R_p(\theta_B) = 0,\qquad \tan\theta_B = \frac{n_2}{n_1}\qquad (56.3^\circ \text{ for } n_2/n_1 = 1.5)"),
            ("Onsager and Yang's magnetization",
             r"m(T) = \bigl(1 - \sinh^{-4}(2/T)\bigr)^{1/8}\ \ (T < T_c),\qquad T_c = \frac{2}{\ln(1+\sqrt2)} \approx 2.269"),
        ],
        U=(0, 1, 2, 4, 7, 8), I=(15, 16), D=(12,),
        also=(("The Reasoner: science", "explainer/philosophy/reasoner/science.py"),),
    ),
]
