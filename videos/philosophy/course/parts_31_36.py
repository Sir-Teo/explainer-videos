"""Act VI closes and Act VII, Value, opens: consciousness, free will, choice, games, ethics, population (Parts 31-36)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=31, level="U", widget="maskignite", prereq=(4, 22, 30),
        question="What is it like to be anything, and why does that seem to resist every physical explanation?",
        story="The part opens with Nagel's sentence of 1974: an organism is conscious if and only if there is "
              "something it is like to be that organism. Block's access and phenomenal consciousness and Chalmers's "
              "easy and hard problems set the question, and the hard problem is the Wall's thirty-first brick. Mary's "
              "room is built as an epistemic model in which three possibilities agree on every physical truth, and "
              "the zombie argument is run through Part 22's two-dimensional matrices and a modal check, then priced "
              "on a Price List. The part turns from the arguments to the science: a global workspace written as one "
              "recurrent equation that ignites and draws a masking curve, a higher-order observer that is 77% "
              "correct with confidence at chance, and a simplified integrated information computed by cutting a loop "
              "of three logic gates. Aaronson's XOR lattices and the unfolding argument are computed against that "
              "measure, and a T-maze agent minimizes expected free energy. It ends with the Cogitate adversarial "
              "collaboration, the declarations on animal consciousness, and the indicator properties for machines "
              "applied to the Reasoner's own toys.",
        handoff="Agents, causes and free will follow in Part 32, and minds that choose under uncertainty in Part 33. "
                "Whose welfare counts, and how much, returns in Parts 35 and 36; machines that decide about people "
                "in Part 41; and the moral status of aligned reasoners in Part 42.",
        outside="School mathematics and logarithms. The zombie chapter uses the modal logic of Part 4 and the "
                "two-dimensional semantics of Part 22; the free-energy chapter uses a Kullback-Leibler divergence.",
        objectives={
            "U": ["State the hard problem and say what separates it from the easy problems of explaining function "
                  "and report.",
                  "Set out the knowledge argument about Mary and the ability, acquaintance and phenomenal-concept "
                  "replies to it."],
            "M": ["Compute the two-dimensional matrix of a sentence on three scenarios and read off whether it is "
                  "a priori and whether it is necessary.",
                  "Compute the simplified phi of a three-gate network by finding the bipartition that loses the "
                  "least effective information.",
                  "Explain ignition in the workspace equation as bistability, and predict how the masking curve "
                  "moves with stimulus strength."],
            "D": ["Reconstruct the zombie argument in two-dimensional semantics and say which premise type-A "
                  "physicalism, type-B physicalism and Russellian monism each deny.",
                  "State the unfolding argument and Aaronson's objection, and explain why any measure that is zero "
                  "on feedforward networks faces the first."],
            "I": ["Apply the indicator properties of Butlin, Long and colleagues to a described system, and "
                  "explain why its self-reports are weak evidence.",
                  "Read an adversarial collaboration's preregistered predictions and say which results count "
                  "against which theory."],
        },
        results=[
            ("Nagel's criterion", r"X\text{ has conscious states}\iff\text{there is something it is like to be }X"),
            ("The zombie argument's modal core", r"\Box(P\rightarrow Q)\ \wedge\ \Diamond(P\wedge\neg Q)\ "
                                                 r"\text{ has no model},\qquad (P\rightarrow Q)\wedge\Diamond(P\wedge\neg Q)"
                                                 r"\text{ has one with two worlds}"),
            ("The workspace equation", r"\tau\,\dot w=-w+100\,\sigma\bigl(g\,(I+r\,w-\theta)\bigr),\qquad "
                                       r"\sigma(z)=\frac{1}{1+e^{-z}}"),
            ("Simplified integrated information", r"\operatorname{ei}(x;A|B)=D_{\mathrm{KL}}\bigl(p(X_0\mid x)\,\big\|\,"
                                                  r"p(A_0\mid x_A)\,p(B_0\mid x_B)\bigr),\qquad \Phi(x)="
                                                  r"\operatorname{ei}(x;\text{MIB}),\quad \text{MIB}=\arg\min_{A|B}"
                                                  r"\frac{\operatorname{ei}(x;A|B)}{\min(|A|,|B|)}"),
            ("Variational free energy", r"F(q)=\mathbb{E}_{q(s)}\bigl[\ln q(s)-\ln p(o,s)\bigr]=D_{\mathrm{KL}}"
                                        r"\bigl(q(s)\,\|\,p(s\mid o)\bigr)-\ln p(o)\ \ge\ -\ln p(o)"),
            ("Expected free energy of a policy", r"G(\pi)=-\mathbb{E}\bigl[\ln\tilde p(o)\bigr]-\mathbb{E}\bigl["
                                                 r"D_{\mathrm{KL}}\bigl(p(s\mid o)\,\|\,p(s)\bigr)\bigr],\qquad "
                                                 r"P(\pi)\propto e^{-G(\pi)}"),
        ],
        U=(0, 1, 2, 3, 7, 8), D=(6, 11), I=(13, 14, 15),
        also=(("The Reasoner's consciousness module", "explainer/philosophy/reasoner/consciousness.py"),),
    ),
    Part(
        n=32, level="U", widget="noisereadiness", prereq=(4, 24, 31),
        question="Could you have done otherwise, and is anything you do up to you?",
        story="The part opens with Schopenhauer's line that a man can do what he wills but cannot will what he "
              "wills, and with the dilemma: determined acts seem not up to us, undetermined ones seem luck. After "
              "Aristotle's sea battle and Chrysippus's answer to the lazy argument, van Inwagen's consequence "
              "argument is derived with the operator N and the rules alpha and beta. The Reasoner then models "
              "options as sets of worlds an action might lead to, and on McKay and Johnson's coin rule beta fails in "
              "two of sixty-four instances while the repaired rule fails in none: the Wall's thirty-second brick. "
              "Frankfurt's case is put on the same model, compatibilism gets its Price List, and van Inwagen's "
              "rollback is replayed a thousand times. The part turns to the science with Libet's readiness "
              "potential, rebuilt from a leaky accumulator fed nothing but noise, and with a diagonal agent that "
              "no predictor on a list gets right. It ends with the free will theorem, six careless drivers in ten "
              "thousand and their two ledgers of blame, and the responsibility gaps that learning machines open.",
        handoff="Newcomb's predictor returns as a decision problem in Part 33 and agents meet in games in Part 34. "
                "Desert and punishment return in Parts 35 and 38, machines that decide about people in Part 41, "
                "and the question of who answers for an aligned reasoner in Part 42.",
        outside="School mathematics. The consequence argument uses the box of Part 4's modal logic; determinism "
                "is defined as in Part 24.",
        objectives={
            "U": ["State the dilemma of determinism and luck, and say what compatibilists, libertarians and hard "
                  "incompatibilists each deny.",
                  "Describe a Frankfurt case and say what it is meant to show about alternative possibilities."],
            "M": ["Derive the consequence argument from rules alpha and beta, and evaluate N on a model of options.",
                  "Reproduce McKay and Johnson's countermodel and show that rule beta with alpha implies "
                  "agglomeration.",
                  "Explain how averaging a noisy accumulator backward from its threshold crossings produces a "
                  "ramp with no decision in the model."],
            "D": ["Prove that the repaired rule (from N p and the necessity of p implies q, infer N q) is valid "
                  "on every model of options, and say what stronger premise Finch and Warfield's argument then "
                  "needs.",
                  "State what the Conway-Kochen free will theorem assumes and what it does not show about "
                  "agency."],
            "I": ["Read a Libet-style result and say what a stochastic-accumulator account predicts differently "
                  "from an early-decision account.",
                  "Separate blame by outcome from blame by risk in a case of moral luck, and identify a "
                  "responsibility gap in a system that learns."],
        },
        results=[
            ("The operator N", r"N p\ :\ p,\ \text{and no one has, or ever had, any choice about whether }p"),
            ("Rules alpha and beta", r"\Box p\ \vdash\ N p\qquad\qquad N p,\ \ N(p\rightarrow q)\ \vdash\ N q"),
            ("The consequence argument", r"\Box\bigl((P_0\wedge L)\rightarrow P\bigr),\ \ N P_0,\ \ N L\ \ \vdash\ \ N P"),
            ("N on a model of options", r"N p\iff p\text{ is true and no available action }a\text{ has }"
                                        r"a\subseteq\neg p"),
            ("McKay and Johnson's coin", r"N(\neg H),\ \ N(\neg T),\ \ \text{but not }N(\neg H\wedge\neg T);"
                                         r"\qquad\text{the repaired rule } N p,\ \Box(p\rightarrow q)\vdash N q"
                                         r"\text{ is valid}"),
            ("The leaky stochastic accumulator", r"\dot x=I-k\,x+c\,\xi(t),\qquad\text{a movement when }x"
                                                 r"\text{ first reaches }\theta>I/k"),
        ],
        U=(0, 1, 2, 5, 9, 13), D=(4, 12), I=(10, 14),
        also=(("The Reasoner's free will module", "explainer/philosophy/reasoner/freewill.py"),),
    ),
    Part(
        n=33, level="U", widget="kellyfortunes", prereq=(13, 14, 32),
        question="What is it to choose well when the outcome is uncertain?",
        story="Act VII opens with Daniel Bernoulli in 1738: the value of an item is the utility it yields, not its "
              "price. Preferences come first, with a money pump that takes fifteen cents in fifteen trades, and the "
              "St Petersburg game is played a million times before Bernoulli's logarithm tames it. The von "
              "Neumann-Morgenstern theorem turns four axioms into a utility function whose indifference lines in "
              "the Marschak-Machina triangle are parallel. Then the theory is tested: Allais's common choices fit "
              "none of 201 utilities, and Ellsberg's fit no probability for any of 61 urns, which is half of the "
              "Wall's thirty-third brick. Risk-weighted utility and prospect theory are the rivals; the Kelly "
              "criterion shows a thousand simulated fortunes growing at the rate g(f) and ruined beyond it; the "
              "Pasadena game has an expectation that depends on the order of adding. The part turns on Newcomb's "
              "problem, where evidential and causal decision theory part ways and each has a counterexample: the "
              "other half of the brick. It ends with policies, Ulysses at the mast, Good's theorem on free "
              "information and the two envelopes.",
        handoff="Many choosers at once are Part 34's games; Harsanyi's theorem applies expected utility to a whole "
                "society in Part 35; tiny chances of vast stakes return as fanaticism in Part 36. Aggregating "
                "preferences leads to Arrow's theorem in Part 39, and predicted agents and the off-switch game "
                "return in Part 42.",
        outside="School algebra, logarithms and expected values. Credences and conditioning are those of Parts 13 "
                "and 14.",
        objectives={
            "U": ["Compute the expected value and expected utility of a lottery, and explain why the St "
                  "Petersburg game has no finite expected value.",
                  "State Allais's two choices and Newcomb's problem, and say why each is a puzzle for expected "
                  "utility."],
            "M": ["State the von Neumann-Morgenstern axioms and show that expected utility's indifference lines "
                  "in the triangle are parallel.",
                  "Prove that no utility function yields Allais's common choices, and derive the Kelly fraction "
                  "by maximizing g(f).",
                  "Compute evidential and causal expected utilities in Newcomb's problem and the smoking lesion."],
            "D": ["Explain why the Pasadena game has no expectation and what weak and relative expectations "
                  "offer in its place.",
                  "Set out the cases that separate evidential, causal and functional decision theory, and the "
                  "counterexample each one faces."],
            "I": ["Size a repeated bet by the Kelly criterion, and explain why practitioners stake a fraction of "
                  "it.",
                  "Recognise the fourfold pattern and a framing effect in a described choice, and say what "
                  "prospect theory predicts."],
        },
        results=[
            ("St Petersburg", r"\sum_{k\ge1}2^{-k}\cdot 2^{k}=\infty,\qquad \sum_{k\ge1}2^{-k}\log_2 2^{k}=2"
                              r"\ \ (\text{a certainty equivalent of }4\text{ ducats})"),
            ("Von Neumann-Morgenstern", r"\succsim\text{ complete, transitive, continuous, independent}\iff"
                                        r"\exists u:\ L\succsim M\Leftrightarrow\sum_i p_i\,u(x_i)\ge\sum_i q_i\,u(x_i),"
                                        r"\quad u\text{ unique up to }au+b,\ a>0"),
            ("Allais's identity", r"EU(1A)-EU(1B)=EU(2A)-EU(2B)=0.11\,u(1)-0.10\,u(5)-0.01\,u(0)"),
            ("The Kelly criterion", r"g(f)=p\ln(1+f)+(1-p)\ln(1-f),\qquad f^{*}=2p-1"),
            ("Newcomb's problem, evidentially", r"V(\text{one box})=10^{6}p,\qquad V(\text{two boxes})=10^{6}(1-p)"
                                                r"+10^{3},\qquad\text{equal at }p=0.5005"),
            ("Good's theorem", r"\mathbb{E}_e\Bigl[\max_a\mathbb{E}\bigl[u(a)\mid e\bigr]\Bigr]\ \ge\ "
                               r"\max_a\mathbb{E}\bigl[u(a)\bigr]"),
        ],
        U=(0, 1, 2, 4, 10, 13), D=(9, 12), I=(7, 8),
        also=(("The Reasoner's decision module", "explainer/philosophy/reasoner/decision.py"),),
    ),
    Part(
        n=34, level="U", widget="extortionline", prereq=(12, 19, 33),
        question="Why would self-interested people cooperate, and can the rules be designed so that they do?",
        story="The part opens with Hobbes's state of nature in 1651, where life is solitary, poor, nasty, brutish "
              "and short, and reads it as a game. Nash equilibrium is defined and found by support enumeration on "
              "five small games; the prisoner's dilemma and Hardin's commons show equilibrium leaving everyone "
              "worse off, and Ostrom's graduated sanctions hold contributions up. Rousseau's stag hunt separates "
              "payoff dominance from risk dominance, and the centipede's backward induction, which takes at once, "
              "is with the dilemma the Wall's thirty-fourth brick. Then come the ways out: a traffic light as a "
              "correlated equilibrium, the shadow of the future with its thresholds of patience, Axelrod's "
              "tournaments rerun with noise, and Press and Dyson's zero-determinant strategies, which fix a line "
              "between the two players' scores. Evolution in a finite population and Skyrms's demand game show "
              "cooperation and fair division arising without foresight. The part turns from playing games to "
              "designing them, with bargaining, the Shapley value, Vickrey's auction and deferred acceptance, and "
              "ends with the social contract's Price List.",
        handoff="Harsanyi's aggregation of welfare and its contractualist critics follow in Part 35, and fairness "
                "across generations in Part 36. Evolved norms return in Part 37, the original position in Part 38, "
                "voting as a mechanism in Part 39, and Shapley values and incentives in machines in Parts 41 and "
                "42.",
        outside="School algebra and probabilities. Expected utility is Part 33's; the replicator dynamics of Part "
                "19 and the common knowledge of Part 12 are recalled where used.",
        objectives={
            "U": ["Find the pure Nash equilibria of a two-by-two game, and explain why mutual defection is the "
                  "only one in the prisoner's dilemma.",
                  "Tell a stag hunt from a prisoner's dilemma, and say why tit for tat did well in Axelrod's "
                  "tournaments."],
            "M": ["Compute a mixed equilibrium from the indifference conditions, and the discount factor at which "
                  "grim trigger sustains cooperation.",
                  "Derive a zero-determinant strategy with a given extortion ratio, and check the line it "
                  "enforces from a stationary distribution.",
                  "Compute a Shapley value by orders of arrival, and run deferred acceptance by hand."],
            "D": ["Set out the paradox of backward induction and what Aumann's and Stalnaker's analyses assume "
                  "about rationality off the path of play.",
                  "Show that an extortioner scores only P against a copy of itself, and explain with Stewart "
                  "and Plotkin why it wins every match yet loses the tournament."],
            "I": ["Explain why a second-price auction makes truthful bidding optimal, and what changes in a "
                  "generalized second-price auction for ad slots.",
                  "Check a matching for blocking pairs, and say for whom deferred acceptance is strategy-proof."],
        },
        results=[
            ("Nash equilibrium", r"u_i(s_i^{*},s_{-i}^{*})\ \ge\ u_i(s_i,s_{-i}^{*})\quad\text{for every player }i"
                                 r"\text{ and every strategy }s_i"),
            ("The commons as a Cournot game", r"x_i^{*}=\frac{a-c}{n+1},\qquad\frac{\text{welfare at equilibrium}}"
                                              r"{\text{best welfare}}=\frac{4n}{(n+1)^{2}}"),
            ("The shadow of the future", r"\text{grim trigger sustains cooperation iff }\delta\ge\frac{T-R}{T-P},"
                                         r"\qquad\text{tit for tat iff }\delta\ge\max\Bigl(\frac{T-R}{T-P},"
                                         r"\frac{T-R}{R-S}\Bigr)"),
            ("Zero-determinant extortion", r"\tilde{\mathbf p}=\phi\bigl[(\mathbf S_X-P\mathbf 1)-\chi(\mathbf S_Y"
                                           r"-P\mathbf 1)\bigr]\ \Longrightarrow\ s_X-P=\chi\,(s_Y-P)"
                                           r"\quad\text{against every opponent}"),
            ("Bargaining", r"\text{Nash: }\max_{x}\,(u_1(x)-d_1)(u_2(x)-d_2),\qquad\text{Rubinstein: the first "
                           r"mover gets }\frac{1}{1+\delta}"),
            ("The Shapley value", r"\phi_i(v)=\sum_{S\subseteq N\setminus\{i\}}\frac{|S|!\,(n-|S|-1)!}{n!}"
                                  r"\bigl(v(S\cup\{i\})-v(S)\bigr)"),
        ],
        U=(0, 1, 2, 3, 6), D=(4, 7), I=(11, 12, 13),
        also=(("The Reasoner's games module", "explainer/philosophy/reasoner/games.py"),),
    ),
    Part(
        n=35, level="U", widget="monstershare", prereq=(33, 34),
        question="What makes an act right: its consequences, a law it falls under, or the character it shows?",
        story="The part opens with Kant's starry heavens above and moral law within, and with three questions: what "
              "is good, what is right, how should I be. Bentham's felicific calculus is kept as a ledger, and "
              "200,000 simulated promise cases show the noise at which calculating each act loses to a rule. "
              "Theories of welfare meet the experience machine; Harsanyi's theorem turns two mild axioms into a "
              "weighted sum, and two egalitarian rules break exactly as it predicts. Sums, priority and maximin are "
              "then set against each other on levelling down, Nozick's utility monster and Singer's pond. The film "
              "turns to Kant: a toy world of promises in which a universal lie collapses trust, the humanity "
              "formula as a consent test, and five maxims on which the universal-law test scores two hits, two "
              "false positives and a false negative. Constraints lead to the paradox of deontology, the Wall's "
              "thirty-fifth brick, and to the trolley problem's Price List. Contractualism, virtue and the holism "
              "of reasons, and care follow, and the part ends with what to do when unsure which theory is true.",
        handoff="Lives that may or may not exist, fanaticism and the far future are Part 36. What moral claims "
                "mean returns in Part 37, the difference principle in Part 38, aggregation by voting in Part 39, "
                "fairness criteria for algorithms in Part 41, and whose values to align a reasoner with in Part 42.",
        outside="School algebra and expected values. Harsanyi's theorem uses the expected utility of Part 33.",
        objectives={
            "U": ["State what consequentialism, deontology and virtue ethics each take to make an act right, with "
                  "a case each finds hard.",
                  "Apply the universal-law test to a maxim, and say why the lying promise fails it."],
            "M": ["State Harsanyi's aggregation theorem and show how the ex-ante and the ex-post egalitarian "
                  "rules each violate one of its premises.",
                  "Compute how the sum, a prioritarian sum and maximin divide a fixed stock between people of "
                  "unequal efficiency.",
                  "Compute expected choiceworthiness under raw, range and variance normalization, and show a "
                  "verdict that flips."],
            "D": ["State the paradox of deontology, and show that an agent-relative weight k on one's own "
                  "killings reproduces the constraint exactly when k exceeds the number saved.",
                  "Set out what Harsanyi's theorem does and does not establish about utilitarianism, given "
                  "Diamond's and Sen's objections."],
            "I": ["Compute Gini and Atkinson indices for an income distribution, and say which value judgement "
                  "the Atkinson parameter encodes.",
                  "Run a decision under moral uncertainty by expected choiceworthiness and by a parliament, and "
                  "report how the answer depends on the method."],
        },
        results=[
            ("Harsanyi's aggregation theorem", r"\text{individual and social preferences satisfy the vNM axioms, "
                                               r"and Pareto indifference holds}\ \Longrightarrow\ "
                                               r"W=\sum_i a_i\,u_i+b"),
            ("Three views of distribution", r"W_{\text{sum}}=\sum_i u_i,\qquad W_{\text{priority}}=\sum_i g(u_i)\ "
                                            r"(g\text{ increasing and strictly concave}),\qquad "
                                            r"W_{\text{maximin}}=\min_i u_i"),
            ("The utility monster under the sum", r"u_m=k\sqrt{x},\ \ u_i=\sqrt{x}\ \ (i=1,\dots,n)\ "
                                                  r"\Longrightarrow\ \text{the monster gets }\frac{k^{2}}{k^{2}+n}"
                                                  r"\text{ of the total}"),
            ("The formula of universal law", r"\text{Act only on that maxim through which you can at the same time "
                                             r"will that it become a universal law}"),
            ("Consequentializing a constraint", r"\text{weight one's own killings by }k:\quad\text{do not kill one "
                                                r"to prevent }n\text{ killings}\iff k>n"),
            ("Expected choiceworthiness", r"a^{*}=\arg\max_a\sum_t c(t)\,CW_t(a),\qquad\text{which depends on how "
                                          r"the }CW_t\text{ are normalized}"),
        ],
        U=(0, 1, 2, 5, 8, 10, 11), D=(3, 7), I=(4, 12),
        also=(("The Reasoner's ethics module", "explainer/philosophy/reasoner/ethics.py"),),
    ),
    Part(
        n=36, level="U", widget="repugnantladder", prereq=(33, 35),
        question="Which outcome is better when our choice decides who will exist, and how many?",
        story="The part opens with the sentence that ends Parfit's Reasons and Persons, on how much worse the "
              "destruction of mankind would be than most people think. The total, average, critical-level and "
              "variable-value views are each written as a formula and scored on Parfit's sequence from A to Z, and "
              "they pick four different best worlds. The repugnant conclusion and the mere addition paradox are "
              "walked step by step and priced on a Price List. The turn is Arrhenius's impossibility: the Reasoner "
              "searches small populations for violations of six conditions by five views and puts a cross in every "
              "row, which is the Wall's thirty-sixth brick. The asymmetry and the non-identity problem follow, "
              "where depletion harms no one who would otherwise exist. Then the far future: the Ramsey rule "
              "derived, Stern against Nordhaus by a factor of fifty-three, the value of a point of extinction risk "
              "under constant risk and under a time of perils, a chain of long shots that forces recklessness, "
              "timidity or intransitivity, and Basu and Mitra's theorem on infinite streams, proved. It ends in "
              "practice, with quality-adjusted life years and the value of a statistical life.",
        handoff="Whether intuitions about Z are evidence of anything is taken up in Part 37, and justice between "
                "generations with Rawls's just savings principle in Part 38. Arrow's theorem, the model for "
                "Arrhenius's, is built in Part 39; algorithms that allocate scarce care return in Part 41, and "
                "the long future of minds and machines in Part 42.",
        outside="School algebra, exponentials and geometric series. Fanaticism uses Part 33's expected utility; "
                "the views of distribution are Part 35's.",
        objectives={
            "U": ["Compute the total, average and critical-level value of a population, and state the repugnant "
                  "conclusion.",
                  "Explain the non-identity problem with the depletion case, and why no one is harmed in it."],
            "M": ["Walk the mere addition paradox from A to B and say which step each view rejects.",
                  "Derive the Ramsey rule and compute a present value under Stern's and under Nordhaus's "
                  "parameters.",
                  "Compute the value of reducing this century's extinction risk when later risk is constant and "
                  "when it falls."],
            "D": ["State the conditions of an Arrhenius-style impossibility theorem and exhibit, for each of the "
                  "five views, a small population that violates one.",
                  "Prove Basu and Mitra's theorem that no real-valued measure of infinite streams satisfies "
                  "strong Pareto and finite anonymity."],
            "I": ["Rank interventions by cost per quality-adjusted life year, and say what fair innings and "
                  "priority weights change.",
                  "Derive a value of a statistical life from a wage-risk trade-off and use it to find a "
                  "regulation's break-even point."],
        },
        results=[
            ("Four axiologies", r"V_{\text{total}}=\sum_i w_i,\qquad V_{\text{average}}=\frac1N\sum_i w_i,\qquad "
                                r"V_{\text{critical}}=\sum_i(w_i-c),\qquad V_{\text{variable}}=g(N)\,\bar w\ \ "
                                r"(g\text{ increasing, bounded})"),
            ("The repugnant conclusion", r"\text{on the total view, for every world }A\text{ there is a larger }Z"
                                         r"\text{ of lives barely worth living with }N_Z\,w_Z>N_A\,w_A"),
            ("Arrhenius's impossibility (2000)", r"\text{no ranking of populations avoids the repugnant and the "
                                                 r"sadistic conclusions and respects a weak form of mere addition}"),
            ("The Ramsey rule", r"r=\delta+\eta\,g,\qquad PV=\frac{X}{(1+r)^{t}}"),
            ("The value of reducing risk", r"V=\frac{v\,(1-r_1)}{r},\qquad \Delta V=\frac{v\,\Delta r_1}{r}"),
            ("Basu and Mitra (2003)", r"\text{no }W:\{0,1\}^{\mathbb N}\rightarrow\mathbb R\text{ satisfies both "
                                      r"strong Pareto and finite anonymity}"),
        ],
        U=(0, 1, 2, 3, 5), D=(4, 9), I=(6, 10, 11),
        also=(("The Reasoner's population module", "explainer/philosophy/reasoner/population.py"),),
    ),
]
