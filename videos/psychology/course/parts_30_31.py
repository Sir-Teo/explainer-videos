"""Act VII, Growing (Parts 30-31)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=30, level="U", widget="infant",
        question="What does a baby know, and how can anyone find out when the baby cannot answer?",
        story="A ten-month-old finds a toy under cup A, again and again; then she watches it hidden under cup B, and "
              "reaches for A. Piaget saw his own children do it and concluded that infants do not yet know objects "
              "exist on their own. Checking him needed an instrument: Fantz noticed that infants can look, and "
              "looking can be timed. Habituation, violation of expectation and the Goldilocks effect follow, and "
              "then the instrument tested at scale: ManyBabies' sixty-five laboratories, recomputed here, find the "
              "preference for infant-directed speech real, smaller than believed, and dependent on age, method and "
              "language. The viewer predicts six famous infant results; then objects, arithmetic, number by ratio "
              "and infants as statisticians are weighed, core knowledge against construction. The A-not-B error is "
              "rebuilt as a dynamic neural field that makes and outgrows it. False belief at four is robust and at "
              "fifteen months contested; newborn imitation is contested; attachment, temperament and copying make "
              "modest predictions.",
        handoff="Development across the life is Part 31; temperament grown up is personality, Part 33; autism and "
                "development are Part 41; the replication capstone is Part 43; learning in schools is Part 54; "
                "machines tested like infants are Part 60.",
        outside="Part 3's measurement, Part 4's meta-analysis, Part 6's circuits, Part 11's Weber's law and Part "
                "14's inference. Probability, differential equations and weighted regression.",
        objectives={
            "U": ["Describe Piaget's stages and the A-not-B error, and what looking-time methods can and cannot show.",
                  "Describe the findings on objects, number, false belief, imitation and attachment, with their "
                  "replication records.",
                  "Explain why multi-laboratory studies changed infancy research."],
            "M": ["Recompute a multi-laboratory meta-analysis and its meta-regression on age and method.",
                  "Derive the approximate number system's accuracy from Weber's law, and an ideal learner's "
                  "surprisal.",
                  "Simulate a dynamic neural field and explain the A-not-B error's dependence on delay."],
            "D": ["Design a study that core knowledge and rational constructivism predict differently.",
                  "Judge what a surprise signal shows, in an infant or a machine."],
            "I": ["Evaluate a developmental screen, an early-childhood programme or a product for babies against "
                  "the evidence."],
        },
        results=[
            ("Ideal learner's surprisal", r"-\log_2 \frac{c + \alpha}{n + k\alpha}"),
            ("Number by ratio", r"P(\text{correct}) = \Phi\!\left(\frac{|n_1 - n_2|}{w\sqrt{n_1^2 + n_2^2}}\right)"),
            ("A dynamic neural field",
             r"\tau\,\dot u = -u + h + S + c\,m + \int w(x - x')\,\sigma(u(x'))\,dx'"),
            ("Random-effects meta-regression", r"y_i = X_i\beta + u_i + e_i, \quad u_i \sim N(0, \tau^2)"),
        ],
        U=(0, 1, 2, 3, 4, 5, 6, 9, 10, 11, 12), D=(7, 8, 14), I=(13,),
        also=(("Psyche's develop module", "explainer/psychology/psyche/develop.py"),
              ("Its tests", "tests/psychology/test_develop.py"),
              ("The open data, fetched and checked", "explainer/psychology/opendata.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
