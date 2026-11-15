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
]
