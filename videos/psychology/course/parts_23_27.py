"""Act V continued, Thinking (Parts 23-27)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=23, level="U", widget="stream",
        question="How does a child who hears a finite number of sentences come to understand an infinite number?",
        story="In 1959 a thirty-year-old linguist reviews Skinner's book on verbal behaviour: almost every sentence is "
              "new, so reinforcement cannot explain it, and the argument over what is built in and what is learned "
              "from statistics begins. Language is productive at every level, as wugs show. Words follow Zipf's law, "
              "and so does a typing monkey. Common words are read faster, a spoken word narrows a cohort, and a "
              "network in which words feed back into letters explains why a letter is easier to see inside a word. "
              "Readers commit as they go, garden paths make them pay, and the surprisal of every word of ten stories, "
              "from a trigram model of thirty novels, predicts how long people spend on the next one. Infants find "
              "words in two minutes of a made-up language by transitional probabilities. A network learns the past "
              "tense in a U, and the rules-or-associations argument follows. Learning a grammar gets harder with "
              "age, late into the teens; language has its own network in the brain; and claims that a language "
              "reshapes colour vision or executive control mostly failed. Language models learn grammar from text, "
              "at thousands of times a child's input, and fit readers worse as they grow.",
        handoff="Reasoning is Part 24, the infant mind Part 30, model comparison Part 48, encoding models Part 49, "
                "readable design Part 52, teaching reading Part 54, and language models Part 60.",
        outside="Part 14's inference, Part 16's delta rule, Part 20's search and Part 22's size principle. "
                "Logarithms, conditional probability and least squares.",
        objectives={
            "U": ["Describe the levels of language, productivity, and the evidence from children's errors.",
                  "Explain word superiority, garden paths and the cohort model.",
                  "Describe statistical learning, critical periods and the language network."],
            "M": ["Fit Zipf's law and explain why a random typist obeys it too.",
                  "Run the interactive activation model and read out a forced choice.",
                  "Fit reading times to n-gram surprisal with length and frequency controlled."],
            "D": ["Derive surprisal as a change of belief, and Gold's learnability limit.",
                  "Build a past-tense learner and explain where its U-shaped curve comes from."],
            "I": ["Judge a readability formula against a reader-based measure.",
                  "Evaluate claims about bilingual advantages and linguistic relativity."],
        },
        results=[
            ("Zipf's law", r"f(r) \propto r^{-s}, \quad s \approx 1"),
            ("Surprisal", r"\text{cost}(w_t) \propto -\log P(w_t \mid w_{<t})"),
            ("Surprisal as belief change", r"-\log P(w_t \mid w_{<t}) = D_{\mathrm{KL}}\big(P(T \mid w_{\le t}) "
                                           r"\,\|\, P(T \mid w_{<t})\big)"),
            ("Transitional probability", r"P(y \mid x) = \#(x\,y) / \#(x)"),
            ("Interactive activation", r"\Delta a = n (M - a) - \theta (a - r) \ \ (n > 0)"),
            ("Kneser-Ney smoothing", r"P(w \mid v) = \frac{\max(c(v w) - d, 0)}{c(v)} + \lambda_v P_{\mathrm{cont}}(w)"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, 9, 10, 12), D=(5, 8, 11, 14), I=(13,),
        also=(("Psyche's language module", "explainer/psychology/psyche/language.py"),
              ("Its tests", "tests/psychology/test_language.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=24, level="U", widget="rotation",
        question="Are people logical, and if not, what are they instead?",
        story="Four cards and one rule defeat nine people in ten; the same rule about drinking ages defeats almost "
              "no one. Psyche finds every valid syllogism by brute force, and 139 people's answers to all 64 show "
              "what logic, mental models and shortcuts each get right. Under rarity, the 'wrong' cards are the "
              "informative ones. Newell and Simon turn problems into spaces of states: the Tower of Hanoi is drawn "
              "whole, a hill-climber wanders through it, and a goal stack predicts where people pause. The nine dots "
              "are proved unsolvable inside the box. Masters see chunks, practice matters but ten thousand hours is a "
              "story, analogy maps relations, and mental rotation runs at about 93 degrees a second in open data. "
              "Causal power, everyday priors and a mind that satisfices close the part.",
        handoff="Deciding in time is Part 25, judgement and bias Part 26, model comparison Part 48, usability Part 52, "
                "personnel selection Part 53, the science of learning Part 54, and reasoning machines Part 60.",
        outside="Part 16's contingency and Part 22's size principle. Sets, conditional probability, entropy and "
                "least squares.",
        objectives={
            "U": ["Describe the selection task, its content effects, and belief bias.",
                  "Explain problem solving as search, insight and functional fixedness.",
                  "Describe chunking, deliberate practice, analogy and mental rotation."],
            "M": ["Decide a syllogism's validity over set models, and score accounts of people's answers on data.",
                  "Compute each card's expected information gain under rarity.",
                  "Fit rotation rates person by person to open data."],
            "D": ["Derive causal power from a noisy-OR, and the posterior-median rule for everyday predictions.",
                  "Explain why no single account of syllogistic reasoning fits, and what would decide between them."],
            "I": ["Judge interview puzzles against validated selection methods.",
                  "Plan a usability test from the problem-discovery model, and say where it fails."],
        },
        results=[
            ("Validity", r"\text{valid} \iff \forall M:\ M \models P_1 \wedge P_2 \Rightarrow M \models C"),
            ("Expected information gain", r"\mathbb{E}[I(x)] = H(M) - \sum_y P(y \mid x)\, H(M \mid x, y)"),
            ("Tower of Hanoi", r"3^n \text{ states}, \quad 2^n - 1 \text{ moves}"),
            ("Mental rotation", r"\text{RT} = a + b\,\theta"),
            ("Causal power", r"q = \frac{\Delta P}{1 - P(e \mid \neg c)}"),
            ("Everyday prediction", r"t^{*} = \operatorname{median}\, p(t_{\text{total}} \mid t) \propto "
                                    r"\frac{p(t_{\text{total}})}{t_{\text{total}}}"),
        ],
        U=(0, 1, 3, 4, 6, 7, 8, 9, 12), D=(2, 5, 10, 11, 14), I=(13,),
        also=(("Psyche's reasoning module", "explainer/psychology/psyche/reason.py"),
              ("Its tests", "tests/psychology/test_reason.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=25, level="M", widget="dots",
        question="Why does a decision take the time it takes?",
        story="In 1943 the Navy asks whether a firing test can stop as soon as the answer is clear, and Abraham Wald "
              "answers: add up the evidence until it crosses a line, which needs about half the shots of a fixed "
              "test and, as he and Wolfowitz prove, no fewer are possible. Hick's and Fitts's laws put a constant "
              "price on each bit; seventeen people told to be careful are all slower and more accurate; and response "
              "times are skewed, so the mean misleads. Ratcliff's diffusion model gives accuracy and mean time in "
              "closed form and whole distributions by series, and its parameters mostly mean what they claim: speed "
              "instructions lower the bound in sixteen of seventeen people, though not only the bound. Variability "
              "explains fast and slow errors; neurons in LIP climb to a level, though single neurons may step; and "
              "races, stopping and confidence read the same accumulator three ways.",
        handoff="Judgement and choice is Part 26, the readiness potential Part 27, model fitting Part 48, interface "
                "design Part 52, individual differences Part 59, and machines that decide when to stop Part 60.",
        outside="Part 1's ex-Gaussian and Hick's law, Part 12's signal detection and meta-d', and Part 17's "
                "dopamine. Random walks, the normal distribution, logarithms and maximum likelihood.",
        objectives={
            "U": ["Describe Hick's and Fitts's laws and the speed-accuracy trade-off.",
                  "Explain why mean response times mislead, and what a response-time distribution looks like.",
                  "Describe accumulation in LIP and the stop-signal task."],
            "M": ["Run Wald's test and compute its average sample number against a fixed test.",
                  "Fit the diffusion model to speed and accuracy blocks, and compare models by AIC.",
                  "Estimate a stop-signal reaction time by the integration method."],
            "D": ["Derive the diffusion model's accuracy and mean decision time.",
                  "Derive Fitts's law from iterative corrections, and explain fast and slow errors by variability."],
            "I": ["Price an interface's targets and menus with Fitts and Hick.",
                  "Decide whether a slower group is less able or more careful."],
        },
        results=[
            ("Wald's bounds", r"A = \log\frac{1-\beta}{\alpha}, \quad B = \log\frac{\beta}{1-\alpha}"),
            ("Hick's law", r"\text{RT} = a + b \log_2 n"),
            ("Fitts's law", r"MT = a + b \log_2 \frac{2D}{W}"),
            ("Accuracy", r"P(\text{upper}) = \frac{1 - e^{-2vz/s^2}}{1 - e^{-2va/s^2}}"),
            ("Mean decision time", r"\mathbb{E}[T] = \frac{a\,P(\text{upper}) - z}{v}"),
            ("Stop-signal race", r"\text{SSRT} = F_{\text{go}}^{-1}\big(P(\text{respond})\big) - \text{SSD}"),
        ],
        U=(0, 1, 2, 3, 8, 10, 11, 12), D=(4, 5, 6, 7, 9, 14), I=(13,),
        also=(("Psyche's decision module", "explainer/psychology/psyche/decide.py"),
              ("Its tests", "tests/psychology/test_decide.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=26, level="U", widget="gambles",
        question="Why do the same people buy insurance and lottery tickets?",
        story="A disease threatens six hundred people. Described as lives saved, most people choose the sure "
              "programme; described as deaths, most choose the gamble, though the outcomes are identical. Bernoulli's "
              "utility explains insurance but not lottery tickets, and Allais's paradox breaks the independence "
              "axiom. Kahneman and Tversky's prospect theory measures outcomes from a reference point, with a kink at "
              "zero, and bends probabilities into an inverse S; its two curves compute the fourfold pattern, and on "
              "1,928 open choice problems it beats expected value out of sample, though loss aversion is near one at "
              "small stakes. Heuristics err systematically, while frequencies and simple rules often do well; the "
              "hot-hand fallacy turns out to be in the statistic; hyperbolic discounting reverses plans; experience "
              "underweights rare events; and values come partly from what we have sampled.",
        handoff="Consciousness is Part 27, risk preference as a trait Part 33, influence between people Part 34, "
                "fitting choice models Part 48, defaults and nudges Part 55, and value as efficient code Part 58.",
        outside="Part 14's illusions, Part 17's reward learning and Part 25's accumulators. Expected values, "
                "Bayes's rule, logarithms and least squares.",
        objectives={
            "U": ["Explain framing, the Allais paradox and the fourfold pattern with prospect theory's two curves.",
                  "Describe availability, representativeness and anchoring, and solve a base-rate problem with "
                  "natural frequencies.",
                  "Explain hyperbolic discounting and why it reverses preferences."],
            "M": ["Compute certainty equivalents under cumulative prospect theory.",
                  "Fit and cross-validate choice models on open data.",
                  "Compute the bias of the hot-hand statistic."],
            "D": ["Show that expected utility's indifference lines are parallel in the probability triangle.",
                  "Explain why prospect theory needed its cumulative form, and judge the evidence on loss aversion."],
            "I": ["Design a default or a framing of choices, and say what would show it worked.",
                  "Communicate a risk in absolute frequencies."],
        },
        results=[
            ("Expected utility", r"\mathrm{EU} = \sum_i p_i\,u(x_i)"),
            ("Value function", r"v(x) = x^{\alpha} \ (x \ge 0), \quad -\lambda(-x)^{\beta} \ (x < 0)"),
            ("Weighting function", r"w(p) = \frac{p^{\gamma}}{(p^{\gamma} + (1-p)^{\gamma})^{1/\gamma}}"),
            ("Decision weight", r"\pi_i = w\big(P(X \ge x_i)\big) - w\big(P(X > x_i)\big)"),
            ("Bayes's rule", r"P(H \mid D) = \frac{P(D \mid H)P(H)}{P(D \mid H)P(H) + P(D \mid \neg H)P(\neg H)}"),
            ("Hyperbolic discounting", r"V = \frac{A}{1 + kD}"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7, 8, 9, 13), D=(5, 10, 11, 12, 15), I=(14,),
        also=(("Psyche's choice module", "explainer/psychology/psyche/choice.py"),
              ("Its tests", "tests/psychology/test_choice.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=27, level="M", widget="masked",
        question="What is the difference between information the brain uses and information you experience?",
        story="A man with a damaged visual cortex insists he sees nothing in half his visual field, and when forced "
              "to guess, points to objects there almost perfectly. The contrastive method makes the question "
              "experimental: hold the stimulus fixed and vary awareness. A model of masking shows the trap in it, "
              "since a strict criterion for saying 'seen' manufactures unconscious perception from one "
              "representation. Rivalry alternates by inhibition and adaptation; no-report designs strip away activity "
              "that belongs to reporting; the workspace ignites all or none; integrated information can be computed "
              "for small networks; and the two theories, tested on terms their authors agreed in advance, each lost "
              "something. Libet's readiness potential can be accumulated noise, and some unresponsive patients "
              "follow commands with their brains.",
        handoff="Motivation begins Act VI in Part 28; awareness before language is Part 30; experience as the "
                "brain's best guess is Part 58; and machine consciousness is Part 60.",
        outside="Part 12's signal detection and meta-d', Part 18's attention, and Part 25's accumulators. "
                "Probability, mutual information and simple differential equations.",
        objectives={
            "U": ["Describe the contrastive method, blindsight and inattentional blindness.",
                  "Explain the global workspace and integrated information theories and one prediction of each.",
                  "Describe Libet's experiment and the accumulator reading of it."],
            "M": ["Compute accuracy on unseen trials in a signal-detection model of masking, and its dependence on "
                  "the criterion.",
                  "Simulate binocular rivalry and an ignition network, and read off their signatures.",
                  "Compute effective information and phi for a small Boolean network."],
            "D": ["Explain why above-chance guessing on unseen trials does not by itself show unconscious perception.",
                  "Design a no-report test that separates the theories' predictions."],
            "I": ["Explain what anaesthesia monitors and brain-based tests in disorders of consciousness can and "
                  "cannot show."],
        },
        results=[
            ("Unseen accuracy", r"P(\text{correct} \mid |x| < c) = \frac{\Phi(c - \mu) - \Phi(-\mu)}"
                                r"{\Phi(c - \mu) - \Phi(-c - \mu)}"),
            ("Effective information", r"\mathrm{EI}(A \to B) = I\big(A^{H_{\max}}_t ; B_{t+1}\big)"),
            ("Integrated information", r"\Phi = \mathrm{EI}(A \to B) + \mathrm{EI}(B \to A) \ \text{at the "
                                       r"minimum information bipartition}"),
            ("Leaky accumulator", r"dx = (I - kx)\,dt + c\,dW"),
            ("Complexity index", r"\mathrm{PCI} = \frac{c_{LZ}(S)\,\log_2 L}{L\,H(p)}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 11, 12, 13), D=(7, 8, 9, 10, 15), I=(14,),
        also=(("Psyche's workspace module", "explainer/psychology/psyche/workspace.py"),
              ("Its tests", "tests/psychology/test_workspace.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
