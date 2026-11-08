from __future__ import annotations

from videos.philosophy.philosophy24.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.film()
        self.questions()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"An intelligence which could comprehend all the forces by which nature is animated "
                       r"\dots\ for it, \ nothing would be uncertain, \ and the future, \ as the past, \ would be "
                       r"present to its eyes.", r"Pierre-Simon Laplace",
                       r"\textit{A Philosophical Essay on Probabilities} \ (1814)", width=10.0, font_size=25).next_to(
            t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 23 asked whether the world needs a cause outside itself. This part asks what holds it together from "
            "inside. <bookmark mark='a'/>In 1814 Pierre-Simon Laplace imagined an intelligence that knew every force "
            "in nature and the position of every particle. For such a mind, he wrote, nothing would be uncertain, "
            "and the future, like the past, would be present to its eyes. <bookmark mark='b'/>Laplace's demon "
            "packs three philosophical ideas into one sentence: that there are laws, that the laws fix everything, "
            "and that the future and the past are on the same footing. Each of the three is in trouble, and this "
            "part builds the trouble."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=LAW, scale_factor=1.03))
        self.clear_scene()

    def film(self):
        head = label(r"A film that runs both ways", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        box = (-3.0, 3.0, -2.2, 1.8)
        frame = Rectangle(width=6.0, height=4.0, color=GREY_B, stroke_width=2).move_to([-2.6, -0.2, 0])
        p0, v0 = gas(n=46, box=box, corner=0.2, seed=1876, speed=1.1)
        t = ValueTracker(0.0)

        def draw():  # the box's coordinates, shifted to the frame
            q = gas_at(p0, v0, t.get_value(), box)
            return VGroup(*[Dot([x - 2.6, y, 0], radius=0.07, color=ENT) for x, y in q])

        dots = always_redraw(draw)
        clock = always_redraw(lambda: label(rf"$t = {t.get_value():.1f}$", font_size=22, color=TIME).next_to(
            frame, DOWN, buff=0.2))
        side = stack([(r"each molecule obeys Newton's laws, \ which run equally well backwards", LAW),
                      (r"forwards: \ the gas spreads out", ENT),
                      (r"backwards: \ it gathers into a corner, \ obeying the same laws", ENT),
                      (r"only one direction looks like our world: \ why?", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=5.2).move_to([3.9, -0.2, 0])
        with self.voiceover(
            "Here is the trouble with the third idea. <bookmark mark='a'/>Forty-six molecules in a box, each moving in "
            "a straight line and bouncing off the walls, exactly as Newton's laws say. Those laws run equally well "
            "backwards: reverse every velocity and the motion retraces itself. <bookmark mark='b'/>Run the film "
            "forwards and the gas spreads out from its corner, as gas does. <bookmark mark='c'/>Now run it "
            "backwards. Every frame still obeys the laws of motion, and the gas gathers itself back into the corner, "
            "which no gas has ever been seen to do. <bookmark mark='d'/>Only one direction looks like our world. "
            "If the laws do not care which way the film runs, where does the difference come from? That question, "
            "Loschmidt's, is this part's brick in the Wall."
        ) as vo:
            self.play(FadeIn(head), Create(frame), FadeIn(dots), FadeIn(clock))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), t.animate.set_value(8.0), run_time=6, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), t.animate.set_value(0.0), run_time=6, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        dots.clear_updaters()
        clock.clear_updaters()
        self.clear_scene()

    def questions(self):
        head = label(r"Three questions, \ and a fourth", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"what is a law?", r"a regularity in the mosaic of facts, \ a relation between properties, \ a power "
                                r"in things, \ or something primitive?", LAW),
            (r"what is chance?", r"if the laws fix everything, \ how can a coin toss have a chance of one half? \ and "
                                 r"what makes a chance true?", CHANCE),
            (r"why does time have a direction?", r"the laws of motion run both ways; \ eggs break and gases spread "
                                                r"only one way", TIME),
            (r"and the cost of knowing", r"Maxwell's demon: \ is information physical? \ Landauer: \ erasing a bit "
                                        r"costs heat", DATA),
        ]
        g = rows_table(rows, top=1.7, gap=0.5, width=8.0, x_text=-1.8, label_size=22, text_size=21)
        with self.voiceover(
            "So this part asks three questions, and a fourth that grows out of them. <bookmark mark='a'/>What is a "
            "law of nature? A regularity in the pattern of facts, a relation between properties, a power in things, "
            "or something that cannot be analyzed at all? <bookmark mark='b'/>What is chance? If the laws fix "
            "everything, how can a coin have a chance of one half of landing heads; and what in the world makes a "
            "statement of chance true? <bookmark mark='c'/>Why does time have a direction, when the laws of motion "
            "run both ways? <bookmark mark='d'/>And the fourth: Maxwell's demon, a creature that seems to beat the "
            "second law of thermodynamics by knowing where the molecules are. Its exorcism shows that information "
            "is physical, and that forgetting has a price in heat, a price that today's computer chips pay many "
            "times over."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"laws as regularities, \ and the best-system account built: \ simplicity against strength, \ in bits",
            r"laws as relations between universals; \ powers; \ primitivism",
            r"Humean chance and the Principal Principle; \ undermining futures and the big bad bug, \ computed",
            r"determinism defined; \ Norton's dome, \ solved and animated",
            r"chaos: \ the Lorenz attractor and its Lyapunov exponent, \ computed",
            r"Boltzmann's entropy; \ Loschmidt and Zermelo; \ the Kac ring, \ built \ (the Wall)",
            r"the Past Hypothesis, \ Boltzmann brains, \ and a Price List for the arrow of time",
            r"Maxwell's demon, \ Szilard's engine and Landauer's bound; \ reversible computing",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>First, laws as regularities, and David Lewis's best-system account, built "
            "as a contest between simplicity and strength measured in bits. <bookmark mark='b'/>Then the rivals: "
            "laws as relations between universals, as powers, or as primitive. <bookmark mark='c'/>Chance, Lewis's "
            "Principal Principle, and the bug that nearly killed his account, computed. <bookmark mark='d'/>What "
            "determinism means, and a dome on which Newton's laws fail to fix the future. <bookmark mark='e'/>Chaos, "
            "and why unpredictable is not the same as undetermined. <bookmark mark='f'/>Entropy, the objections of "
            "Loschmidt and Zermelo, and a toy universe that answers them, this part's brick in the Wall. "
            "<bookmark mark='g'/>The special beginning that the arrow of time seems to need, and the Boltzmann "
            "brains that haunt the alternative. <bookmark mark='h'/>And the thermodynamics of information, from "
            "Maxwell's demon to reversible computers."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
