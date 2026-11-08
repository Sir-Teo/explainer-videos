from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403


def square(side, unit, color, center, fill=0.15):
    return Square(side * unit, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=fill).move_to(center)


class Meno(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Meno's paradox and the slave boy", r"How can you look for what you do not know?",
                            lit=(-380,), part=PART)
        with self.voiceover("Chapter five. Meno's paradox and the slave boy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.paradox()
        self.squares()
        self.irrational()
        self.recollection()

    def paradox(self):
        q = quote_card(r"How will you look for it, Socrates, when you do not know at all what it is?",
                       r"Meno, \textit{Meno} 80d", r"trans.\ Grube", width=9.0, font_size=30).to_edge(UP, buff=0.5)
        horns = VGroup(
            VGroup(label(r"if you know it", font_size=30, color=P.CLAIM),
                   label(r"you need not inquire", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(label(r"if you do not know it", font_size=30, color=P.AGENT),
                   label(r"you cannot recognize it when you find it", font_size=26, color=GREY_A)).arrange(DOWN,
                                                                                                    buff=0.12),
        ).arrange(RIGHT, buff=1.6).move_to([0, -0.6, 0])
        concl = label(r"so inquiry is either pointless or impossible", font_size=30, color=BAD).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In Plato's Meno, Socrates and Meno try to define virtue, and fail. Meno, frustrated, turns the "
            "failure into a paradox. <bookmark mark='a'/>How will you look for something when you do not know at all "
            "what it is? <bookmark mark='b'/>Either you know it, and then you need not inquire; <bookmark mark='c'/>or "
            "you don't, and then you won't recognize it even if you stumble on it. <bookmark mark='d'/>So inquiry is "
            "either pointless or impossible. It is a real problem, and it returns, as the paradox of analysis, "
            "whenever philosophers try to define a concept they already use."
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(Indicate(q, color=HIST))
            vo.wait_until("b")
            self.play(FadeIn(horns[0]))
            vo.wait_until("c")
            self.play(FadeIn(horns[1]))
            vo.wait_until("d")
            self.play(FadeIn(concl))
        self.clear_scene()

    def squares(self):
        d = load("meno")
        u = 0.7
        base = square(2, u, P.CLAIM, [-4.4, 0.2, 0])
        bl = label(r"side 2, \ area 4", font_size=24, color=P.CLAIM).next_to(base, DOWN, buff=0.2)
        task = label(r"Find the square with twice the area: \ 8", font_size=30, color=GOAL).to_edge(UP, buff=0.4)
        g4 = square(4, u, BAD, [0.2, 0.2, 0], fill=0.08)
        g4l = label(r"side 4: \ area 16, \ too big", font_size=24, color=BAD).next_to(g4, DOWN, buff=0.2)
        g3 = square(3, u, P.AGENT, [0.2, 0.2, 0], fill=0.08)
        g3l = label(r"side 3: \ area 9, \ still too big", font_size=24, color=P.AGENT).next_to(g3, DOWN, buff=0.2)
        assert [t["area"] for t in d["tries"]] == [16, 9, 8]
        # Socrates' figure: four copies of the base square, and the square on their inner diagonals
        c = np.array([4.2, 0.2, 0])
        quads = VGroup(*[square(2, u, P.CLAIM, c + np.array([dx, dy, 0]) * u, fill=0.06)
                         for dx in (-1, 1) for dy in (-1, 1)])
        diam = Polygon(c + np.array([0, 2, 0]) * u, c + np.array([2, 0, 0]) * u, c + np.array([0, -2, 0]) * u,
                       c + np.array([-2, 0, 0]) * u, stroke_color=OK, stroke_width=4, fill_color=OK, fill_opacity=0.25)
        halves = label(r"4 halves of the area-4 square: \ area 8", font_size=24, color=OK).next_to(quads, DOWN,
                                                                                               buff=0.2)
        side = MathTex(r"\text{side} = \sqrt{8} = 2\sqrt2", font_size=32, color=OK).next_to(halves, DOWN, buff=0.2)
        with self.voiceover(
            "Socrates' answer is a demonstration. He calls over a slave boy who has never studied geometry, draws a "
            "square with sides two feet long, area four, <bookmark mark='a'/>and asks for the square with twice the "
            "area, eight. <bookmark mark='b'/>The boy confidently doubles the side. But a side of four gives area "
            "sixteen, four times too much. <bookmark mark='c'/>So he tries three: area nine, still too big. Now he "
            "is confused, and Socrates points out that being confused is progress: at least he no longer thinks he "
            "knows."
        ) as vo:
            self.play(FadeIn(base), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(task))
            vo.wait_until("b")
            self.play(Create(g4), FadeIn(g4l))
            vo.wait_until("c")
            self.play(ReplacementTransform(g4, g3), ReplacementTransform(g4l, g3l))
        with self.voiceover(
            "Then Socrates draws four copies of the original square, and asks only questions. <bookmark mark='a'/>The "
            "lines across their corners, the diagonals, cut each copy in half, and the four halves make a new square. "
            "<bookmark mark='b'/>Four halves of four is eight. The square on the diagonal is the doubled square. Its "
            "side is no whole number of feet: it is the square root of eight, a quantity the Greeks had discovered "
            "cannot be a ratio of whole numbers."
        ) as vo:
            self.play(FadeOut(g3), FadeOut(g3l), FadeIn(quads))
            vo.wait_until("a")
            self.play(Create(diam), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(halves), Write(side))
        self.clear_scene()

    def recollection(self):
        thesis = definition_card(r"Recollection (\textit{anamnēsis})", r"the soul knew these truths before birth; "
                                 r"inquiry is remembering", width=6.4, font_size=24, color=HIST)
        thesis.to_corner(UL, buff=0.4)
        later = VGroup(
            label(r"Plato: \ innate knowledge, recollected", font_size=26),
            label(r"Descartes, Leibniz: \ innate ideas (Part 10)", font_size=26),
            label(r"Chomsky: \ an innate grammar", font_size=26),
            label(r"a learning system: \ an inductive bias (Part 15)", font_size=26, color=GOAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([1.6, -0.9, 0])
        with self.voiceover(
            "Plato's conclusion is startling. The boy was never taught the answer, yet he produced it under "
            "questioning; so, says Socrates, he must have known it already, before he was born, and inquiry is "
            "recollection. <bookmark mark='a'/>Few philosophers since have believed in recollection. But the "
            "underlying idea, that learning is impossible unless the learner brings something to it, runs through "
            "the history of philosophy: <bookmark mark='b'/>innate ideas in Descartes and Leibniz, an innate "
            "grammar in Chomsky, and, in Part 15, the inductive bias without which no machine can learn anything at "
            "all."
        ) as vo:
            self.play(FadeIn(thesis))
            vo.wait_until("a")
            self.play(FadeIn(later[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in later[1:]], lag_ratio=0.4))
        self.clear_scene()

    def irrational(self):
        rows = [MathTex(r"\sqrt{2}", r"=", r"p/q", r"\text{ in lowest terms}", font_size=40),
                MathTex(r"2q^2", r"=", r"p^2", font_size=40),
                MathTex(r"p", r"=", r"2r", r"\text{ (so } p \text{ is even)}", font_size=40),
                MathTex(r"q^2", r"=", r"2r^2", r"\text{ (so } q \text{ is even too)}", font_size=40)]
        whys = [why(r"suppose it were a fraction"), why(r"square both sides"), why(r"an odd square is odd"),
                why(r"divide by 2: \ contradiction, \ $p/q$ was in lowest terms")]
        step = ladder(self, rows, whys, keep=4, top=2.2, x=-1.6, edge=6.8)
        leg = note(r"the discovery is credited by legend to Hippasus, a Pythagorean").to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Why can't the side be a fraction? Here is the classic proof, probably known to Plato's circle. "
            "<bookmark mark='a'/>Suppose the square root of two were a fraction p over q, in lowest terms. "
            "<bookmark mark='b'/>Then two q squared equals p squared, so p squared is even. <bookmark mark='c'/>The "
            "square of an odd number is odd, so p itself is even: p is two r. <bookmark mark='d'/>Substitute and "
            "divide by two: q squared is two r squared, so q is even too. But then the fraction was not in lowest "
            "terms. The supposition refutes itself. A reductio, and the side of the doubled square is a new kind of "
            "number."
        ) as vo:
            step(0)
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                if k == 0:
                    self.play(Indicate(rows[0], color=GOAL))
                else:
                    step(k)
            self.play(FadeIn(leg))
        self.clear_scene()
