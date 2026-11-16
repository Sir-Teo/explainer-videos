"""Psychology, Built as a course: Parts 51 to 57 (Act XII, psychology at work)."""

from videos.coursekit import Part

PARTS = [
    Part(
        n=51, level="U", widget="watchclock", prereq=(10, 12, 18, 25),
        question="When a person makes a fatal error with a machine, whose error is it?",
        story="In 1947 Paul Fitts and Richard Jones collected 460 reports of pilot error and found the same few again "
              "and again: in some aircraft the flap and landing-gear levers sat side by side and felt the same, and "
              "Alphonse Chapanis fixed it with a wheel-shaped knob and a flap-shaped one. Human factors begins with "
              "the idea that error is designed in. The part fits Fitts's and Hick's laws, sorts slips, lapses and "
              "mistakes, reads Three Mile Island, measures workload, watches Psyche's vigilance decline over two "
              "hours and its criterion rise for rare targets, models Bainbridge's ironies of automation and an "
              "alarm's two criteria, stacks correlated slices of Swiss cheese, and puts fatigue on the scale of "
              "blood alcohol.",
        handoff="Part 52 turns Fitts's and Hick's laws into an engineering model of the interface; Part 56 treats a "
                "line-up as a detection task; humans supervising learning machines return in Part 60.",
        outside="Part 12's signal detection, Part 18's attention, Part 10's clocks and Part 25's confidence; "
                "logarithms and the normal distribution.",
        objectives={
            "U": ["Explain why many errors are designed in, and sort an error as a slip, a lapse, a mistake or a "
                  "violation.",
                  "Describe the vigilance decrement and the prevalence effect, and why rare targets are missed."],
            "M": ["Fit Fitts's law and compute d' and c block by block for a long watch.",
                  "Model an alarm's hit rate, positive predictive value and the share of events answered when "
                  "operators match their response to its reliability."],
            "D": ["State an open problem in supervising learning-based automation and design a study of it."],
            "I": ["Write the human-factors section of a safety case: tasks, likely errors, evidence and residual "
                  "risk.",
                  "Design a takeover request and the simulator test that would show it works."],
        },
        results=[
            ("Fitts's law", r"MT = a + b\log_2(D/W + 1)"),
            ("Hick-Hyman law", r"RT = a + b\log_2(N + 1)"),
            ("An alarm's positive predictive value", r"\mathrm{PPV} = \frac{pH}{pH + (1-p)F}"),
            ("Independent defences", r"P(\text{accident}) = \prod_k h_k"),
        ],
        U=(0, 1, 2, 3, 4, 6, 7), D=(15,), I=(9, 10, 11, 14),
        also=(("Psyche's work module", "explainer/psychology/psyche/work.py"),
              ("Its tests", "tests/psychology/test_work.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=52, level="U", widget="pointer", prereq=(1, 11, 18, 51),
        question="Can you predict how long a person will take to use something before it is built?",
        story="In the late 1980s a telephone company was about to buy operator workstations expected to save time on "
              "every call. Wayne Gray, Bonnie John and Michael Atwood modelled the operators' perception, cognition "
              "and keystrokes on paper and predicted the new design would be slower; the field trial agreed. The "
              "part builds the Model Human Processor and the keystroke-level model, measures pointing as throughput, "
              "steers through tunnels, sets menu depth against breadth, follows an information forager by the "
              "marginal value theorem, shows why five users find less than promised, ranks chart encodings, computes "
              "contrast, and asks how long a habit takes.",
        handoff="Part 53 turns from the interface to the people (selection and training); Part 55 scales defaults "
                "and nudges; Part 60 returns to minds and machines.",
        outside="Part 1's mental chronometry, Part 11's power law, Part 18's search and Part 51's human factors; "
                "logarithms and a little probability.",
        objectives={
            "U": ["Predict a skilled user's task time with the keystroke-level model.",
                  "Explain why position and length are read more accurately than angle and area."],
            "M": ["Measure pointing throughput with the effective width, and fit Fitts's and the steering law.",
                  "Derive the problem-discovery curve and show how unequal detectability lowers it."],
            "D": ["Design a study of whether a simulated user's verdict on an interface can be trusted."],
            "I": ["Compare two designs by keystroke-level analysis before testing, and choose the right test for the "
                  "remaining questions.",
                  "Audit an interface for contrast, target size and dark patterns."],
        },
        results=[
            ("Keystroke-level model", r"T = \sum_i n_i t_i + R"),
            ("Throughput", r"TP = \frac{\log_2(D/W_e + 1)}{MT}, \quad W_e = 4.133\,\sigma"),
            ("Problem discovery", r"P(\text{found}) = 1 - (1 - p)^n"),
            ("Contrast ratio", r"\frac{L_1 + 0.05}{L_2 + 0.05}"),
        ],
        U=(0, 1, 2, 3, 7, 9, 10), D=(15,), I=(8, 11, 14),
        also=(("Psyche's work module", "explainer/psychology/psyche/work.py"),
              ("Its tests", "tests/psychology/test_work.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
