from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403

PROBLEMS = [
    r"With evidence $x \sim N(\pm d/2, 1)$ and ``seen'' when $|x| > c$, \ derive accuracy on unseen trials, \ and "
    r"show that it exceeds one half whenever $d > 0$.",
    r"Show that the same model's unseen accuracy rises toward the overall accuracy as $c$ grows. \ What does that "
    r"imply for claims of unconscious perception?",
    r"For a ring of $n$ nodes that each copy their neighbour, \ show that every bipartition into two arcs has "
    r"effective information 1 bit each way, \ so $\Phi = 2$.",
    r"Why does a network of two unconnected loops have $\Phi = 0$, \ however much information each loop "
    r"carries?",
    r"In Schurger's accumulator, \ show that the expected activity just before a crossing is higher than its "
    r"long-run mean, \ whatever the drift.",
    r"With \texttt{workspace.rivalry}: \ raise the noise and lower the adaptation. \ What happens to the shape of "
    r"the dominance distribution?",
    r"$\star$ \ Design a no-report experiment that could tell whether prefrontal cortex is needed for seeing a "
    r"face, \ and say what each theory predicts.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def recap(self):
        items = [
            (r"a digit for one frame: \ the same stimulus, \ seen or not", SEEN),
            (r"the contrastive method: \ hold the stimulus fixed, \ vary awareness", WHITE),
            (r"masking: \ above-chance guesses on unseen trials can be a strict criterion", UNSEEN),
            (r"blindsight: \ real, \ replicated, \ and maybe not entirely blind", LOST),
            (r"rivalry: \ inhibition plus adaptation; \ more neurons follow the percept further up the stream", GNW),
            (r"no-report: \ some frontal activity belongs to reporting, \ not seeing", HOT),
            (r"the workspace: \ graded early, \ all or none late", GNW),
            (r"integrated information: \ $\Phi$ computed, \ bold predictions, \ fierce critics", IIT),
            (r"the adversarial test: \ each theory lost something it had staked", MODEL),
            (r"Libet's ramp can be noise; \ hidden awareness is real; \ complexity measures it", RPT),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 27, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-seven in ten lines. <bookmark mark='a'/> A digit shown for a single frame showed the "
            "question: the same stimulus, seen or not. The contrastive method holds the stimulus fixed and varies "
            "awareness. Above-chance guessing on unseen trials can come from a strict criterion, not a second system. "
            "Blindsight is real and replicated, and maybe not entirely blind. Rivalry comes from inhibition and "
            "adaptation, and neurons follow the percept more closely further along the visual stream. No-report "
            "designs show that some frontal activity belongs to reporting, not to seeing. The workspace predicts "
            "graded early activity and all-or-none late activity. Integrated information can be computed for small "
            "networks, makes bold predictions, and has fierce critics. The adversarial test cost each theory "
            "something it had staked. And Libet's ramp can be accumulated noise, hidden awareness in unresponsive "
            "patients is real, and the complexity of the brain's echo can measure it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"signal detection, \ bifurcations and $\Phi$: \ the criterion problem and ignition computed",
             STATUS_COLOR["replicated"]),
            (r"the contrastive method, \ no-report designs, \ and an adversarial test agreed in advance",
             STATUS_COLOR["replicated"]),
            (r"here Kant's third objection bites hardest: \ every measure of awareness is a report, \ or stands in for "
             r"one", STATUS_COLOR["contested"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met "
            "signal detection, a bifurcation and integrated information, each computed. <bookmark mark='b'/> The "
            "second, that the mind can't be experimented on, met the contrastive method, no-report designs, and two "
            "rival theories agreeing in advance on how they could be proved wrong. <bookmark mark='c'/> But here the "
            "third objection, that looking inward disturbs what you look at, bites hardest. Every measure of "
            "awareness is a report, or stands in for one, and the criterion problem never quite goes away. Amber."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"motivation: \ why do anything at all?", [28]),
            (r"the infant mind: \ awareness before language", [30]),
            (r"the efficient, \ predictive brain: \ experience as the brain's best guess", [58]),
            (r"minds and machines: \ could a machine be conscious?", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Act Six begins next, with motivation. Awareness before "
            "language is in Part 30, on the infant mind. Experience as the brain's best guess is Part 58. And whether "
            "a machine could be conscious is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=8.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> Two work through the "
            "criterion problem in the masking model. Two compute integrated information for rings and for "
            "disconnected loops. One shows why averaging before threshold crossings produces a ramp. One explores "
            "the rivalry model. And the last, with the star, asks you to design a no-report experiment that could "
            "settle whether the front of the brain is needed to see a face. Pause here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"L. Weiskrantz, \emph{Blindsight: A Case Study and Implications} (1986)",
             r"S. Dehaene, \emph{Consciousness and the Brain} (2014)",
             r"A. K. Seth \& T. Bayne, \emph{Theories of consciousness}, \ Nature Reviews Neuroscience (2022)"],
            [r"L. Weiskrantz et al.\ (1974); \ A. Cowey \& P. Stoerig (1995); \ N. Persaud et al.\ (2007)",
             r"B. J. Baars (1988); \ F. Crick \& C. Koch (1990); \ D. J. Chalmers (1995); \ N. Block (1995)",
             r"S. Dehaene et al.\ (1998); \ C. Sergent et al.\ (2005); \ S. Dehaene \& J.-P. Changeux (2011)",
             r"G. Tononi (2004); \ G. Tononi et al.\ (2016); \ V. A. F. Lamme (2006); \ H. Lau \& D. Rosenthal (2011)",
             r"D. A. Leopold \& N. K. Logothetis (1996); \ F. Tong et al.\ (1998); \ S. Frässle et al.\ (2014)",
             r"B. Libet et al.\ (1983); \ A. Schurger, \ J. D. Sitt \& S. Dehaene (2012)",
             r"A. M. Owen et al.\ (2006); \ M. M. Monti et al.\ (2010); \ A. G. Casali et al.\ (2013)",
             r"L. Melloni et al.\ (2021); \ Cogitate Consortium (2025)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Weiskrantz's Blindsight is "
            "still the best account of D.B., Dehaene's Consciousness and the Brain makes the case for the workspace, "
            "and Anil Seth and Tim Bayne's review is the fairest short map of all the theories."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V \ complete: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 28", font_size=32, color=GREY_B), label(r"Motivation", font_size=40),
                     wrapped_label(r"A rat with a misplaced electrode, \ a lever, \ and thousands of presses an hour.",
                                   6.0, 28, GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "That completes Act Five, on thinking. <bookmark mark='a'/> Act Six is feeling and wanting, and it "
            "begins with a question so basic it's easy to skip: why do anything at all? <bookmark mark='b'/> In 1954 "
            "James Olds and Peter Milner noticed that a rat with a misplaced electrode kept returning to the corner "
            "of its box where the current had come on. Given a lever, rats pressed it thousands of times an hour and "
            "ignored food. What had they found? It's Part 28: motivation."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
