"""Act IV, Learning and Memory (Parts 16-22)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=16, level="U", widget="contingency",
        question="What, exactly, is learned when a signal comes to mean food?",
        story="Pavlov's dogs salivate to a signal paired with food; the response fades in extinction and part of it "
              "returns the next day. Thorndike's cats escape a puzzle box faster and faster, gradually: the law of "
              "effect. Watson builds behaviourism on it and conditions one infant to fear a white rat, a "
              "demonstration that grew in the retelling. Skinner's chamber records every response: shaping by "
              "successive approximation, and four schedules of reinforcement, each with its signature. Then the "
              "turn: Rescorla's random control shows that pairing teaches nothing without contingency, and Kamin's "
              "blocking that a paired cue teaches nothing when the outcome is already predicted. Rescorla and Wagner "
              "write surprise as one line, gradient descent on a squared prediction error, which predicts blocking, "
              "inhibition and overexpectation, and whose asymptote is the contingency itself. Its failures, latent "
              "inhibition, recovery and renewal, show that extinction is new learning bound to context; attention, "
              "time and choice extend it, and the matching law follows from melioration. Biology sets limits: taste "
              "goes with sickness, animals drift back to instinct, children learn by watching.",
        handoff="Prediction errors in dopamine neurons and temporal-difference learning are Part 17, learned attention "
                "Part 18, memory rewritten in use Part 21, choices over time Part 26, fear and exposure Part 40, "
                "addiction Part 41, and products built around habits Part 52.",
        outside="Part 2's experimental designs, Part 12's detection theory and Part 14's latent causes. Derivatives "
                "and the idea of a gradient; a little probability.",
        objectives={
            "U": ["Describe acquisition, extinction, spontaneous recovery, generalization and the four schedules.",
                  "Explain why contingency, not pairing, drives learning, and what blocking shows.",
                  "Explain why extinguished fears return, and what that means for exposure therapy."],
            "M": ["Derive the Rescorla-Wagner rule as gradient descent and run it on the classic designs.",
                  "Prove that its asymptote with a context cue is the contingency, delta P.",
                  "Derive the matching law from melioration, and show where melioration is a trap."],
            "D": ["Weigh associative against propositional and latent-cause accounts of human conditioning.",
                  "Assess the reliability of blocking and the evidence for reconsolidation."],
            "I": ["Explain how exposure therapy, contingency management and animal training use conditioning.",
                  "Recognize variable-ratio schedules in product design, and what the evidence on loot boxes shows."],
        },
        results=[
            ("Contingency", r"\Delta P = P(\text{US}\mid\text{CS}) - P(\text{US}\mid\neg\text{CS})"),
            ("Rescorla-Wagner", r"\Delta V_X = \alpha_X\beta\,\big(\lambda - \textstyle\sum_i V_i\big)"),
            ("As gradient descent", r"\Delta V = -\eta\,\nabla_V\,\tfrac12\big(\lambda - x^\top V\big)^2"),
            ("Its asymptote", r"V_X^\ast = \Delta P"),
            ("The matching law", r"\frac{B_L}{B_L + B_R} = \frac{R_L}{R_L + R_R}"),
            ("The I/T law", r"n_{\text{acq}} \approx 300\,(I/T)^{-1}"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 8, 11, 12, 13), D=(7, 9, 10, 15), I=(14,),
        also=(("Psyche's conditioning module", "explainer/psychology/psyche/conditioning.py"),
              ("Its tests", "tests/psychology/test_conditioning.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
    Part(
        n=17, level="U", widget="bandit",
        question="How does a brain learn what to do when the reward comes later?",
        story="A monkey's dopamine neurons fire at unannounced juice; after training they fire at the cue instead, and "
              "fall silent when promised juice is withheld. In 1997 those recordings were matched to the "
              "temporal-difference error of reinforcement learning, derived here from the Bellman equation: learn "
              "each prediction from the next one. On a delay line the error moves from reward to cue, and an "
              "artificial dopamine error, made with light, teaches as a real one does. The same error drives action: "
              "actor and critic, Q-learning, and the basal ganglia's Go and NoGo, tested in patients with "
              "Parkinson's disease. A bandit's learning rate can be read from choices, if parameter recovery says it "
              "can; directed exploration beats greedy choice. Tolman's rats learned maps without reward, and the "
              "brain has place and grid cells. Habits and plans are told apart by devaluation, the two-step task "
              "and revaluation, with the successor representation between them and replay offline. Dopamine also "
              "ramps, signals movement and encodes a distribution; a drug can fake its error; and the same "
              "mathematics runs recommender systems and the side effects of a medicine.",
        handoff="Attention is Part 18, memory and replay Part 21, decisions and risk Part 26, motivation Part 28, "
                "addiction Part 41, products built around habits Part 52, and the predictive brain Part 58.",
        outside="Part 16's Rescorla-Wagner rule and Part 11's maximum likelihood. Expected values, geometric sums "
                "and a little linear algebra.",
        objectives={
            "U": ["Describe Schultz's three dopamine recordings and what a reward prediction error is.",
                  "Explain the explore-exploit dilemma, latent learning, and the difference between habits and plans.",
                  "Explain why a drug that raises dopamine directly could hijack learning."],
            "M": ["Derive the TD error from the Bellman equation and run TD learning on a conditioning task.",
                  "Fit a Q-learning model to choices by maximum likelihood, and check it by parameter recovery.",
                  "Compute a successor matrix and predict reward and transition revaluation."],
            "D": ["Weigh the evidence that dopamine signals prediction errors against ramps and salience accounts.",
                  "Assess what the two-step task's mixture weight measures."],
            "I": ["Explain how bandit algorithms run recommendations and A/B tests.",
                  "Explain why dopamine agonists can cause impulse-control disorders."],
        },
        results=[
            ("Value", r"V(s_t) = \mathbb{E}\big[\textstyle\sum_k \gamma^k r_{t+k}\big]"),
            ("The TD error", r"\delta_t = r_t + \gamma V(s_{t+1}) - V(s_t)"),
            ("Q-learning", r"Q(s,a) \leftarrow Q(s,a) + \alpha\,[r + \gamma \max_{a'} Q(s',a') - Q(s,a)]"),
            ("Softmax choice", r"P(a) \propto e^{\beta Q(a)}"),
            ("Successor representation", r"M = (I - \gamma T)^{-1},\ V = M r"),
        ],
        U=(0, 1, 3, 4, 5, 6, 7, 8, 11, 12), D=(2, 9, 10, 14), I=(13,),
        also=(("Psyche's rl module", "explainer/psychology/psyche/rl.py"),
              ("Its tests", "tests/psychology/test_rl.py"),
              ("The Archive's sources", "explainer/psychology/archive/SOURCES.md")),
    ),
]
