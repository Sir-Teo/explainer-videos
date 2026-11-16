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
    Part(
        n=53, level="U", widget="hiring", prereq=(2, 3, 28, 32),
        question="How well can anyone predict who will be good at a job?",
        story="The Hawthorne lighting studies became the founding story of work psychology, though their data barely "
              "show the effect. The useful history is a correlation: how well a hiring method predicts later "
              "performance. The part simulates 200,000 applicants to show how selection and unreliable ratings hide "
              "validity and how corrections restore it or overshoot, sets Schmidt and Hunter's 1998 summary beside "
              "Sackett and colleagues' 2022 revision, models why unstructured interviews feel informative, turns "
              "validity into money with Taylor-Russell tables and the Brogden-Cronbach-Gleser formula, computes "
              "adverse impact and the validity-diversity frontier, and ends with goals, incentives, crowding out, "
              "teams and a randomized trial of working from home.",
        handoff="Part 54 takes learning and training into the classroom; Part 55 scales incentives and defaults; Part "
                "56 takes tests and judgement into court; Part 60 returns to fairness in algorithms.",
        outside="Part 3's reliability, Part 32's ability testing and Part 28's motivation; correlation, the normal "
                "distribution and a little algebra.",
        objectives={
            "U": ["Explain why a test can look weak among the people it selected, and why structured interviews beat "
                  "unstructured ones.",
                  "Apply the four-fifths rule and say what it does and does not establish."],
            "M": ["Correct an observed validity for criterion unreliability and range restriction, in order, and show "
                  "how a wrong correction overshoots.",
                  "Compute Taylor-Russell success rates and Brogden-Cronbach-Gleser utility."],
            "D": ["Evaluate the 2022 revision of selection validities and design a study that would settle it."],
            "I": ["Design a selection system with its utility, adverse-impact analysis and validation plan.",
                  "Audit an algorithmic hiring tool for validity and impact."],
        },
        results=[
            ("Case II correction", r"r_c = \frac{r\,u}{\sqrt{1 + r^2 (u^2 - 1)}}"),
            ("Utility", r"\Delta U = N_s T r\, SD_y\, \bar z_x - C"),
            ("Mean score of those selected", r"\bar z_x = \phi(z_c) / SR"),
            ("Impact ratio", r"SR_{\text{focal}} / SR_{\text{reference}} \ge 0.8"),
        ],
        U=(0, 1, 2, 3, 6, 10, 11, 12), D=(15,), I=(7, 8, 9, 14),
        also=(("Psyche's work module", "explainer/psychology/psyche/work.py"),
              ("Its tests", "tests/psychology/test_work.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
    Part(
        n=54, level="U", widget="spacedlists", prereq=(20, 21, 45),
        question="What is the most effective way to learn something, and why do learners choose the opposite?",
        story="In 1984 Benjamin Bloom reported that tutored pupils scored two standard deviations above a class, and "
              "challenged education to match it; later reviews put tutoring near 0.8 and school trials near 0.4. The "
              "part turns memory research into engineering: the testing effect in classrooms, the spacing "
              "ridgeline as a design rule, interleaving, learning against performance with Psyche cramming and "
              "spacing, ten techniques ranked, cognitive load, the learning-styles crossover that never appears, "
              "tutoring systems, four review schedules raced at equal study, the simple view of reading, "
              "growth-mindset lessons at national scale, and feedback that makes things worse.",
        handoff="Part 55 scales interventions from classrooms to countries; Part 56 takes memory to court; Part 62's "
                "dissertation can test a learning intervention.",
        outside="Parts 20 and 21's memory models, Part 45's knowledge tracing and Part 47's heterogeneity; "
                "logarithms and effect sizes.",
        objectives={
            "U": ["Choose study methods by evidence (retrieval, spacing, interleaving) and explain why they feel "
                  "worse.",
                  "Explain why learning styles fail the crossover test."],
            "M": ["Compare review schedules under a memory model at equal study time.",
                  "Compute the sample a small educational effect needs, and read heterogeneity."],
            "D": ["Design a study of transfer, or of an AI tutor, that separates performance from learning."],
            "I": ["Redesign a course or training programme with retrieval, spacing, interleaving and faded examples, "
                  "and plan its evaluation."],
        },
        results=[
            ("Simple view of reading", r"RC = D \times LC"),
            ("Bayesian knowledge tracing", r"P(K \mid \text{wrong}) = \frac{P(K)\,s}{P(K)\,s + (1 - P(K))(1 - g)}"),
            ("Sample per arm", r"n = 2 (z_{1-\alpha/2} + z_{1-\beta})^2 / d^2"),
        ],
        U=(0, 1, 2, 3, 4, 5, 7, 10), D=(15,), I=(6, 9, 14),
        also=(("Psyche's work module", "explainer/psychology/psyche/work.py"),
              ("Part 21's memory model", "explainer/psychology/psyche/memory.py"),
              ("The Ledger", "explainer/psychology/ledger.py")),
    ),
]
