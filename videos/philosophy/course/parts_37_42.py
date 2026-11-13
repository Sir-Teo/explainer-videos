"""Act VII, Value, concluded, and the Finale, The Reasoners We Build (Parts 37-42)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=37, level="U", widget="maxsatethics", prereq=(2, 6, 35),
        question="When we say that cruelty is wrong, are we stating a fact, expressing an attitude, or making a "
                 "mistake?",
        story="The part opens with Mackie's five words of 1977, 'there are no objective values', and four questions "
              "about logic, metaphysics, meaning and knowledge. Hume's paragraph of 1739 becomes Hume's law, Prior's "
              "tea inference of 1960 breaks its naive form, and the Reasoner builds a logic of ought on serial "
              "Kripke models and checks eight inferences on every model of three worlds: each valid inference from "
              "is-only premises to an ought is a logical truth or has an idle ought, which is Schurz's pattern and "
              "the Wall's thirty-seventh brick. Moore's open question, realism in its two forms, Mackie's error "
              "theory and expressivism are then set out as answers, with a Price List for Mackie's triad. The part "
              "turns on the Frege-Geach problem: if 'lying is wrong' only expresses disapproval, modus ponens "
              "through a conditional equivocates, and Gibbard's norm-world pairs are built to make it valid again "
              "(eight pairs, two left by the premises). Relativism, constructivism, Street's Darwinian dilemma run "
              "as an analogy, moral psychology, and Mencius against Xunzi follow. It ends with reflective "
              "equilibrium as weighted MaxSAT on six trolley commitments, where double effect and three judgments "
              "survive until Greene's reweighting leaves only welfare and the switch.",
        handoff="Constructivism returns as the original position in Part 38, attitudes are aggregated by voting in "
                "Part 39, and the question whether a judgment states a fact or expresses a feeling is asked of "
                "beauty in Part 40. Hume's law returns as the no-free-lunch theorem for learning preferences in "
                "Part 42, where reflective equilibrium is also proposed as a process for choosing a machine's "
                "values.",
        outside="Nothing beyond the series: truth tables from Part 2 and possible worlds from Part 6 are enough.",
        objectives={
            "U": ["State Hume's law, give Prior's counterexample to its naive form, and say what makes the ought "
                  "in it idle.",
                  "Sort a metaethical view as realist, error-theoretic or expressivist by which claim of Mackie's "
                  "triad it denies."],
            "M": ["Evaluate Op and Pp on a serial Kripke model and build a two-world countermodel to an invalid "
                  "inference.",
                  "Compute the pairs a judgment leaves open in Gibbard's semantics and check an argument's "
                  "validity by inclusion.",
                  "Find the heaviest consistent set of weighted commitments and say how it moves when one weight "
                  "changes."],
            "D": ["State the special Hume thesis for KD and prove it by grafting a new root onto a countermodel.",
                  "Set out the negation problem for expressivism (Unwin, Schroeder) and what Gibbard's hyperplans "
                  "and Schroeder's 'being for' each pay to solve it."],
            "I": ["Read a dumbfounding or trolley study and say what it does and does not show about the "
                  "reliability of a moral intuition.",
                  "Encode a set of principles and case judgments as weighted MaxSAT and report which weights the "
                  "verdict depends on."],
        },
        results=[
            ("Ought and may on serial models (KD)", r"w\vDash O\varphi\iff\forall v\,(wRv\Rightarrow v\vDash\varphi),"
                                                   r"\qquad w\vDash P\varphi\iff\exists v\,(wRv\wedge v\vDash\varphi),"
                                                   r"\qquad\forall w\,\exists v\;wRv"),
            ("Prior's tea, and what fails", r"p\vDash p\vee Oq,\qquad p\nvDash Op,\qquad Op\nvDash p,"
                                            r"\qquad Op\vDash Pp"),
            ("Hume's law in Schurz's form", r"\text{if no premise in }\Gamma\text{ contains }O\text{ or }P\text{ and }"
                                            r"\Gamma\vDash\varphi,\text{ then }\vDash\varphi\text{ or the oughts in }"
                                            r"\varphi\text{ are idle: }\Gamma\vDash\varphi[\,s/O\psi\,]"
                                            r"\text{ for a fresh atom }s"),
            ("Mackie's triad", r"\text{Not all three: moral claims purport to state objective facts; there are no "
                               r"objective moral facts; some moral claims are true.}"),
            ("Validity in norm-world semantics", r"[\![\varphi]\!]\subseteq W\times N,\qquad \varphi_1,\dots,"
                                                 r"\varphi_k\vDash\chi\iff[\![\varphi_1]\!]\cap\dots\cap"
                                                 r"[\![\varphi_k]\!]\subseteq[\![\chi]\!]"),
            ("Reflective equilibrium as weighted MaxSAT", r"\max_{K\subseteq C}\ \sum_{c\in K}w_c\quad"
                                                          r"\text{subject to }K\cup L\text{ being satisfiable}"),
        ],
        U=(0, 1, 2, 4, 5, 10), D=(6,), I=(9,),
        also=(("The Reasoner's metaethics module", "explainer/philosophy/reasoner/metaethics.py"),),
    ),
    Part(
        n=38, level="U", widget="veilchooser", prereq=(34, 35, 37),
        question="What does a society owe its members, and who gets the flute?",
        story="The part opens with Rawls's first sentence of 1971 and Sen's flute, and scores three toy societies by "
              "total, least income and Gini: each principle picks a different one. Thrasymachus, the ring of Gyges "
              "and the social contract of Hobbes, Locke and Rousseau lead to Rawls's original position, the two "
              "principles and the difference principle drawn on an incentive frontier, where (8, 6) beats both "
              "equality at (5, 5) and the utilitarian point (12.5, 3.75). Harsanyi's reply is computed on two "
              "hundred random societies: the average picks one, maximin another, and a chooser with constant "
              "relative risk aversion moves from the first to the second as eta grows. Nozick's entitlement "
              "theory is run as the Wilt Chamberlain economy with a Price List, and Dworkin's auction is built as a "
              "competitive equilibrium from equal incomes with envy checked. The part turns on Sen's liberal "
              "paradox: every assignment of two rights is searched and each is forced into a cycle with the Pareto "
              "principle, the Wall's thirty-eighth brick. Liberty, then fair division by procedure (cut and "
              "choose, Selfridge-Conway, envy-free rents, deferred acceptance), follow, and the part ends with "
              "communitarian and Confucian critics and justice beyond borders.",
        handoff="Sen's paradox is the first of the aggregation impossibilities: Arrow's theorem follows in Part 39. "
                "Equality of opportunity and the choice among fairness criteria return for machines in Part 41, "
                "and the veil of ignorance returns in Part 42 as a way to choose a machine's principles.",
        outside="School algebra. Part 34's games and Part 35's utilitarianism are recalled where they are used.",
        objectives={
            "U": ["State Rawls's two principles and their priority, and find the point the difference principle "
                  "picks on a frontier.",
                  "Set out the Wilt Chamberlain argument as an inconsistent set and say which claim each side "
                  "denies."],
            "M": ["Compute the choice behind the veil under the average, maximin and CRRA expected utility, and "
                  "say which risk attitude each assumes.",
                  "Run Selfridge-Conway on given valuations and verify that no one envies another.",
                  "Check a competitive equilibrium from equal incomes, or a vector of rents, for envy."],
            "D": ["Prove Sen's theorem that no social decision function with unrestricted domain satisfies weak "
                  "Pareto and minimal liberalism.",
                  "Explain how Gibbard's alienable rights and the game-form account each escape the paradox, and "
                  "at what cost."],
            "I": ["Divide a rent or a set of goods with an envy-free rule and state what is maximized among the "
                  "envy-free solutions.",
                  "Run deferred acceptance for a school-choice problem and say for which side the result is "
                  "best."],
        },
        results=[
            ("The difference principle on the film's frontier", r"\max_t\,u_L(t),\qquad u_A=5+3t,\ u_L=5+2t-t^2"
                                                                r"\ \Longrightarrow\ t=1,\ (u_A,u_L)=(8,6)"),
            ("Choice behind the veil", r"\max_s\ \frac1n\sum_{i=1}^n u_\eta(w_{s,i}),\qquad u_\eta(w)="
                                       r"\frac{w^{1-\eta}-1}{1-\eta};\qquad \eta=0\text{: the average},\quad "
                                       r"\eta\to\infty\text{: }\max_s\min_i w_{s,i}"),
            ("The Gini coefficient", r"G=\frac{\sum_{i}\sum_{j}|x_i-x_j|}{2n^2\,\bar x}"),
            ("Sen's liberal paradox", r"\text{No social decision function on all profiles satisfies both weak "
                                      r"Pareto and minimal liberalism (two people each decisive over one pair).}"),
            ("Envy-freeness", r"v_i(A_i)\ \ge\ v_i(A_j)\quad\text{for all }i,j"),
            ("Envy-free rents", r"v_{i\sigma(i)}-p_{\sigma(i)}\ \ge\ v_{ir}-p_r\ \text{ for all }i,r,\qquad"
                                r"\sum_r p_r=R"),
        ],
        U=(0, 1, 2, 3, 5), D=(7,), I=(9,),
        also=(("The Reasoner's justice module", "explainer/philosophy/reasoner/justice.py"),),
    ),
    Part(
        n=39, level="U", widget="fivewinners", prereq=(2, 34, 38),
        question="Can a crowd have a will, and can any way of counting ballots find it?",
        story="The part opens with Rousseau's general will and one election of 55 voters that five standard rules "
              "give to five different candidates. Condorcet's paradox of 1785 shows a majority cycling among three "
              "options; its probability under impartial culture is computed exactly (1/18 with three voters) up "
              "to Guilbaud's limit of 8.77%. The rules are then compared on the same ballots, with agenda control "
              "and a search that finds instant runoff punishing a candidate for gaining support. May's theorem "
              "is proved by searching all 59,049 anonymous rules for two alternatives, and the part turns on "
              "Arrow's theorem: the Borda count is shown breaking independence, Geanakoplos's pivotal voter is "
              "drawn, and the case of two voters and three alternatives is encoded in 108 variables and 992 "
              "clauses and found unsatisfiable, the Wall's thirty-ninth brick. Gibbard-Satterthwaite follows by "
              "searching every profile for manipulations, and Black's median voter gives the escape by restricting "
              "the domain. The later chapters go beyond rankings, compute the jury theorem and its failure under "
              "an opinion leader, rebuild Hong and Page, and aggregate judgments and seats. It ends with "
              "deliberation, sortition and what a model trained on human comparisons aggregates.",
        handoff="Part 40 asks whether a panel of critics converges as a jury does. Part 41 meets fairness criteria "
                "that cannot hold together, an impossibility in Arrow's style, and Part 42 uses the Borda lesson "
                "for learning from human feedback and asks whose values a machine should aggregate.",
        outside="Counting and school probability (the binomial distribution). Part 2's SAT solver is used, not "
                "re-derived.",
        objectives={
            "U": ["Count a set of ranked ballots by plurality, runoff, instant runoff and Borda, and find the "
                  "Condorcet winner or the cycle.",
                  "Compute the probability that a majority of n independent voters is right, and say what "
                  "happens when the voters copy one another."],
            "M": ["State May's theorem and Arrow's theorem with every condition, and show the Borda count "
                  "violating independence of irrelevant alternatives.",
                  "Find a profitable misreport under a given rule, and state the Gibbard-Satterthwaite theorem.",
                  "Prove that single-peaked preferences make the median voter's peak a Condorcet winner."],
            "D": ["Prove Arrow's theorem by the pivotal-voter argument.",
                  "State List and Pettit's impossibility for judgment aggregation and relate the "
                  "premise-based and conclusion-based procedures to it."],
            "I": ["Encode a small social-choice impossibility as SAT and read its correction sets as the list "
                  "of escapes.",
                  "Say what a Bradley-Terry fit to pooled human comparisons aggregates, and when it disagrees "
                  "with the majority."],
        },
        results=[
            ("Condorcet's paradox under impartial culture", r"P_3(\text{no Condorcet winner})=\tfrac1{18},\qquad "
                                                            r"\lim_{n\to\infty}P_n=\tfrac14-\tfrac{3}{2\pi}"
                                                            r"\arcsin\tfrac13\approx 0.0877"),
            ("May's theorem", r"\text{For two alternatives, majority rule is the only rule that is anonymous, "
                              r"neutral and positively responsive.}"),
            ("Arrow's theorem", r"\text{With three or more alternatives, a social welfare function on all "
                                r"profiles that satisfies Pareto and IIA is a dictatorship.}"),
            ("Gibbard-Satterthwaite", r"\text{A strategy-proof rule that can elect each of three or more "
                                      r"candidates is a dictatorship.}"),
            ("Black's median voter theorem", r"\text{single-peaked preferences, } n \text{ odd}\ \Longrightarrow\ "
                                             r"\text{the median peak beats every alternative by majority}"),
            ("Condorcet's jury theorem", r"P_n=\sum_{k>n/2}\binom nk p^k(1-p)^{n-k}\ \longrightarrow\ 1"
                                         r"\quad\text{as } n\to\infty,\ \text{if } p>\tfrac12"),
        ],
        U=(0, 1, 2, 9), D=(10,), I=(5, 11),
        also=(("The Reasoner's social choice module", "explainer/philosophy/reasoner/vote.py"),),
    ),
    Part(
        n=40, level="U", widget="roughnessdips", prereq=(37, 39),
        question="Is beauty in the eye of the beholder, or is there something in the object to be right about?",
        story="The part opens with Hume's remark of 1757 that beauty exists 'in the mind which contemplates', and "
              "asks how far a calculation can go against it. After Plato's ladder and Aristotle's mimesis, the "
              "Pythagorean ratios are stacked into a spiral of fifths that misses by the comma 531441/524288, and "
              "equal temperament is measured against the just intervals. Plomp and Levelt's roughness is then "
              "built into a dissonance curve whose dips fall exactly on 6:5, 5:4, 4:3, 3:2, 5:3 and 2:1, and move "
              "when the timbre's partials are stretched: consonance belongs to the sound, not to the numbers "
              "alone. All seventeen wallpaper groups are generated and classified, and order is measured by "
              "Birkhoff's ratio and by compression, which shrinks rule 90 and cannot touch rule 30. The golden "
              "ratio fails a look-elsewhere test. The part turns on Hume's standard of taste: no formula settles "
              "beauty, yet some judgments are better, which is the Wall's fortieth brick, and a simulated panel "
              "of true judges converges where a shared prejudice stalls. Kant, the definitions of art, forgery "
              "and machine-made images follow, and it ends with mathematical beauty and the Chinese tradition "
              "from Xie He to Cook Ding.",
        handoff="Act VII ends here. The independence that Hume's judges need, like Condorcet's jurors in Part 39, "
                "returns as the question of whose judgments a machine is trained on in Parts 41 and 42, and "
                "Part 42's Wall files this brick with the others where a rule gives way to trained judgment.",
        outside="School arithmetic with ratios and logarithms. No music theory is assumed.",
        objectives={
            "U": ["Compute the Pythagorean comma and say why no stack of pure fifths closes on an octave.",
                  "State the paradox of taste as three claims that cannot all hold, and say which one Hume and "
                  "Kant each give up."],
            "M": ["Compute the roughness of two complex tones from their partials and predict where the "
                  "dissonance curve dips.",
                  "Classify a wallpaper pattern by the flowchart: smallest rotation, mirrors, glides, centres "
                  "on mirrors.",
                  "Run a look-elsewhere test on a claimed golden ratio."],
            "D": ["Explain why Kolmogorov complexity is uncomputable and why it ranks noise highest, and what "
                  "logical depth and effective complexity change.",
                  "Assess compression progress as a theory of interest against Berlyne's inverted U and "
                  "the evidence for it."],
            "I": ["Tune a scale to a timbre with non-harmonic partials using the dissonance curve.",
                  "Set out what current guidance and case law say about authorship of machine-made images, and "
                  "what a trained aesthetic predictor does and does not measure."],
        },
        results=[
            ("The Pythagorean comma", r"\frac{(3/2)^{12}}{2^{7}}=\frac{3^{12}}{2^{19}}=\frac{531441}{524288},\qquad "
                                      r"1200\log_2\frac{3^{12}}{2^{19}}\approx 23.46\text{ cents}"),
            ("Equal temperament", r"\text{semitone}=2^{1/12},\qquad 1200\log_2\frac{2^{7/12}}{3/2}\approx-1.96"
                                  r"\text{ cents}"),
            ("Roughness of two partials (Plomp-Levelt, Sethares)", r"d=\min(a_1,a_2)\bigl(e^{-3.5\,s\,\Delta f}-"
                                                                  r"e^{-5.75\,s\,\Delta f}\bigr),\qquad "
                                                                  r"s=\frac{0.24}{0.0207\,f_{\min}+18.96}"),
            ("Where the curve dips", r"n f_1=m f_2\ \Longrightarrow\ \frac{f_2}{f_1}=\frac nm;\qquad"
                                     r"\text{with partials at }k^{\log_2 S}\text{ the dips move to }"
                                     r"\Bigl(\frac nm\Bigr)^{\log_2 S}"),
            ("The wallpaper groups", r"\text{There are exactly seventeen symmetry groups of patterns that repeat "
                                     r"in two independent directions (Fedorov 1891).}"),
            ("Birkhoff's aesthetic measure", r"M=\frac{O}{C}\qquad(\text{order over complexity})"),
        ],
        U=(0, 1, 2, 6, 7, 9), D=(5,), I=(10,),
        also=(("The Reasoner's aesthetics module", "explainer/philosophy/reasoner/aesthetics.py"),),
    ),
    Part(
        n=41, level="U", widget="groupthresholds", prereq=(17, 34, 38, 39),
        question="Can a machine that decides about people be fair, and fair by whose measure?",
        story="The finale's first part opens with the COMPAS dispute of 2016: ProPublica found unequal error rates "
              "between Black and white defendants, Northpointe answered that the score was equally calibrated, "
              "and both had their numbers right. The three families of criteria are stated as independence, "
              "separation and sufficiency, and the Reasoner builds two populations with base rates of 30% and "
              "50% and a perfectly calibrated score: at a threshold of 0.5 the false-positive rates are about "
              "10% and 30%. The part turns on the impossibility. Chouldechova's identity is derived from the "
              "confusion table, Kleinberg, Mullainathan and Raghavan's theorem is proved in four lines and "
              "checked on the population, and a Price List sets out what each escape costs: the Wall's "
              "forty-first brick. Group thresholds are then searched and four policies entered in a ledger of "
              "errors. The middle chapters ask which fairness is owed, what individual and counterfactual "
              "fairness add, and what makes discrimination wrong, with fairness through unawareness tested and "
              "failing. Differential privacy is built from the Laplace mechanism, randomized response, "
              "composition and a reconstruction attack, and set against contextual integrity. It ends with "
              "Shapley and counterfactual explanations for a toy credit model, and with opacity and the "
              "responsibility gap.",
        handoff="Part 42 takes the same question from a classifier to an agent: what to specify, how values are "
                "learned from feedback, and whose values count. The trilemma is filed in Part 42's complete Wall "
                "with Arrow's and Sen's theorems, under aggregation.",
        outside="Fractions and conditional probability at school level. The causal models of Part 17 and the "
                "Shapley value of Part 34 are recalled where they are used.",
        objectives={
            "U": ["Compute a false-positive rate, a false-negative rate and a precision from a confusion table, "
                  "and say which of them each side of the COMPAS dispute compared.",
                  "State independence, separation and sufficiency in words and give a decision rule that meets "
                  "one and breaks another."],
            "M": ["Derive Chouldechova's identity and prove the Kleinberg-Mullainathan-Raghavan theorem for a "
                  "calibrated score.",
                  "Calibrate Laplace noise to a query's sensitivity and add up the privacy loss of k queries.",
                  "Compute exact Shapley values for a small model and check that they sum to the prediction's "
                  "distance from the baseline."],
            "D": ["State counterfactual fairness on a structural causal model, and set out the objection that a "
                  "causal effect of race is not well defined and the path-specific reply.",
                  "Explain why auditing every intersection of groups is hard, statistically and "
                  "computationally."],
            "I": ["Audit a deployed score: report calibration, error rates and selection rates by group, and "
                  "the cost in errors of each threshold policy.",
                  "Write the fairness and privacy parts of a model card, naming the criterion chosen and what "
                  "was given up for it."],
        },
        results=[
            ("Three criteria", r"\text{independence: }R\perp A,\qquad\text{separation: }R\perp A\mid Y,\qquad"
                               r"\text{sufficiency: }Y\perp A\mid R"),
            ("Chouldechova's identity", r"\mathrm{FPR}=\frac{p}{1-p}\cdot\frac{1-\mathrm{PPV}}{\mathrm{PPV}}\cdot"
                                        r"(1-\mathrm{FNR})"),
            ("Calibration against balance", r"p\,x+(1-p)\,y=p\ \Longrightarrow\ \frac{p}{1-p}=\frac{y}{1-x},"
                                            r"\qquad x=\mathbb{E}[s\mid Y=1],\ y=\mathbb{E}[s\mid Y=0]"),
            ("Differential privacy and the Laplace mechanism", r"P\bigl(M(D)\in S\bigr)\le e^{\varepsilon}\,"
                                                               r"P\bigl(M(D')\in S\bigr),\qquad M(D)=f(D)+"
                                                               r"\operatorname{Lap}\bigl(\Delta f/\varepsilon\bigr)"),
            ("Composition", r"k\text{ queries: }\varepsilon_{\text{total}}\le k\varepsilon,\quad\text{or }"
                            r"\sqrt{2k\ln(1/\delta)}\,\varepsilon+k\varepsilon(e^{\varepsilon}-1)"
                            r"\text{ with probability }1-\delta"),
            ("Shapley values", r"\phi_i=\sum_{S\subseteq N\setminus\{i\}}\frac{|S|!\,(n-|S|-1)!}{n!}"
                               r"\bigl(v(S\cup\{i\})-v(S)\bigr),\qquad\sum_i\phi_i=f(x)-f(x_0)"),
        ],
        U=(0, 1, 2, 5, 7), D=(6,), I=(4, 10, 11),
        also=(("The Reasoner's fairness module", "explainer/philosophy/reasoner/fairness.py"),),
    ),
    Part(
        n=42, level="U", widget="offswitchdefer", prereq=(7, 37, 39, 41),
        question="We have built reasoners that calculate: what do we want them to calculate, and can we say it?",
        story="The finale opens with Wiener's warning of 1960 and King Midas, and four questions: specification, "
              "learning, control and legitimacy. Goodhart's law is computed as best-of-N selection on a noisy "
              "proxy: with Gaussian error the pick's true value keeps rising, with heavy tails it peaks at N = 8 "
              "and falls back to nothing while the proxy climbs, and a quantilizer keeps most of the gain. "
              "After the catalogue of specification gaming, value learning meets its limit: four planner-reward "
              "pairs reproduce one behaviour exactly, Armstrong and Mindermann's no free lunch for preferences "
              "and Hume's law for learning machines. The off-switch game is solved: a robot unsure of our utility "
              "gains E[max(u, 0)] by waiting, 0.70 against 0.50 for acting, and a noisy human reverses the "
              "incentive. Power-seeking is counted on a small MDP, and Löb's axiom is checked on every frame of "
              "up to four worlds before FairBot cooperates with itself in modal combat. The part turns from "
              "computation to judgment with whose values, honesty and the moral status of the machines "
              "themselves. It ends by laying all forty-two bricks of the Wall, sorting them by what they force, "
              "and returning to Leibniz's 'calculemus' with the Reasoner counted by the numbers.",
        handoff="This is the last part: nothing is handed forward. Its last chapters send each brick of the Wall "
                "back to the part that laid it, Parts 1 to 41, and list what to read next.",
        outside="The normal distribution and expected values at school level. Löb's theorem is recalled from "
                "Part 7, social choice from Part 39 and Hume's law from Part 37.",
        objectives={
            "U": ["Explain Goodhart's law with the best-of-N experiment, and say why the shape of the proxy's "
                  "error decides whether more optimization helps.",
                  "Give two different planner-reward pairs that explain the same behaviour, and say why "
                  "behaviour alone cannot separate them."],
            "M": ["Solve the off-switch game: compute the value of acting, switching off and waiting, and find "
                  "when a noisy human removes the incentive to defer.",
                  "Compute the share of reward functions whose optimal policy avoids shutdown in a small MDP, "
                  "and explain the limit k/(k + 1).",
                  "Check Löb's axiom on a finite frame and say which frames validate it."],
            "D": ["Derive Gödel's second theorem from Löb's theorem, state the Löbian obstacle for an agent "
                  "that must trust its successor, and prove that FairBot cooperates with FairBot.",
                  "State the no-free-lunch theorem for preferences and the assumptions that current value "
                  "learning adds to escape it."],
            "I": ["Recognise specification gaming and reward-model overoptimization in a training run, and "
                  "choose a mitigation such as a quantilizer or a penalty for leaving the reference policy.",
                  "Say what evidence would show that a model believes what it reports, and what probes and "
                  "behavioural tests do not establish."],
        },
        results=[
            ("Regressional Goodhart, Gaussian case", r"V\sim N(0,1),\ U=V+E,\ E\sim N(0,1)\ \Longrightarrow\ "
                                                     r"\mathbb{E}[V\mid U]=\tfrac12U"),
            ("No free lunch for preferences", r"\pi(a)\propto e^{\beta R(a)}\quad\text{is unchanged under}\quad"
                                              r"(\beta,R)\mapsto(2\beta,\tfrac12R)\ \text{and}\ (\beta,R)\mapsto"
                                              r"(-\beta,-R)"),
            ("The off-switch game", r"u\sim N(\mu,\sigma^2):\quad\mathbb{E}[\max(u,0)]=\mu\,\Phi\bigl(\tfrac{\mu}"
                                    r"{\sigma}\bigr)+\sigma\,\varphi\bigl(\tfrac{\mu}{\sigma}\bigr)\ \ge\ "
                                    r"\max(\mu,0)"),
            ("Power-seeking with k options behind the hub", r"P(\text{the optimal policy avoids shutdown})\to"
                                                            r"\frac{k}{k+1}\quad\text{as }\gamma\to1"),
            ("Löb's theorem", r"\text{if }\mathrm{PA}\vdash\Box P\to P\text{ then }\mathrm{PA}\vdash P;\qquad"
                              r"\Box(\Box p\to p)\to\Box p"),
            ("Löb's axiom on finite frames", r"\Box(\Box p\to p)\to\Box p\text{ is valid on a finite frame iff "
                                             r"its relation is transitive and irreflexive}"),
        ],
        U=(0, 1, 2, 7, 9, 11), D=(6,), I=(8,),
        also=(("The Reasoner's alignment module", "explainer/philosophy/reasoner/alignment.py"),),
    ),
]
