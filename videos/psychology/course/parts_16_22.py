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
]
