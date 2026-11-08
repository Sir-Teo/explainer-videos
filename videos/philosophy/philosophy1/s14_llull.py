from __future__ import annotations

import numpy as np

from videos.philosophy.philosophy1.common import *  # noqa: F403


class Llull(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Llull's wheels", r"Could a machine combine ideas?", lit=(1305, 1666), part=PART)
        with self.voiceover("Chapter thirteen. Llull's wheels."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.figure_a()
        self.wheels()
        self.legacy()
        self.swift()

    def figure_a(self):
        d = load("llull")
        letters = [p[0] for p in d["principles"]]
        R = 2.4
        c = np.array([-2.8, -0.3, 0])
        pts = [c + R * np.array([np.cos(PI / 2 - TAU * i / 9), np.sin(PI / 2 - TAU * i / 9), 0]) for i in range(9)]
        ring = Circle(radius=R, stroke_color=CONN, stroke_width=2).move_to(c)
        labs = VGroup(*[MathTex(rf"\mathrm{{{L}}}", font_size=34, color=GOAL).move_to(c + (p - c) * 1.13)
                        for L, p in zip(letters, pts)])
        chords = VGroup(*[Line(pts[i], pts[j], color=CONN, stroke_width=1.6, stroke_opacity=0.7)
                          for i in range(9) for j in range(i + 1, 9)])
        assert len(chords) == len(d["pairs"]) == 36
        hc = history_card(r"c.\ 1305", r"Ramon Llull (c.\ 1232--1316), of Majorca", r"the \textit{Ars magna}: a "
                          r"mechanical art of finding truths", width=5.6, color=HIST).to_corner(UR, buff=0.35)
        names = VGroup(*[label(rf"\textbf{{{L}}} \ {en}", font_size=22, color=GREY_A) for L, _, en in d["principles"]])
        names.arrange_in_grid(rows=3, cols=3, buff=(0.4, 0.15), cell_alignment=LEFT).next_to(hc, DOWN, buff=0.4)
        cnt = MathTex(r"\binom{9}{2} = 36 \text{ pairs}", font_size=36, color=CONN).next_to(names, DOWN, buff=0.4)
        with self.voiceover(
            "In the 1270s, on the island of Majorca, Ramon Llull had a vision of a machine for finding truth. "
            "<bookmark mark='a'/>His Ars magna, refined over decades, begins with nine principles, the attributes of "
            "God, each with a letter: goodness, greatness, eternity, power, wisdom, will, virtue, truth and glory. "
            "<bookmark mark='b'/>The first figure arranges them on a circle and joins every pair: thirty-six chords, "
            "one for each combination, such as 'goodness is great' or 'power is wise'. <bookmark mark='c'/>Nine "
            "things taken two at a time is thirty-six. Llull's point was that the combinations are generated "
            "mechanically, not chosen: the art lists them all, so nothing is missed."
        ) as vo:
            self.play(Create(ring), FadeIn(labs), FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(names))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(ch) for ch in chords], lag_ratio=0.05), run_time=3)
            vo.wait_until("c")
            self.play(Write(cnt))
        self.clear_scene()

    def wheels(self):
        d = load("llull")
        letters = [p[0] for p in d["principles"]]
        w1 = wheel(letters, radius=2.9, color=CONN, font_size=30, center=[-2.6, -0.3, 0])
        w2 = wheel(letters, radius=2.15, color=P.AGENT, font_size=28, center=[-2.6, -0.3, 0])
        w3 = wheel(letters, radius=1.4, color=P.TRUE, font_size=26, center=[-2.6, -0.3, 0])
        for w in (w2, w3):
            w[1].set_opacity(0)
        pointer = Arrow([-2.6, 3.0, 0], [-2.6, 2.4, 0], color=GOAL, buff=0)
        txt = VGroup(label(r"the fourth figure: \ three wheels", font_size=28, color=GOAL),
                     MathTex(r"9 \times 9 \times 9 = 729 \text{ settings}", font_size=34),
                     MathTex(r"\binom{9}{3} = 84 \text{ triples: Llull's Table}", font_size=34),
                     label(r"each setting is a question to be answered", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.2, 0])
        assert d["wheels"] == 729 and len(d["triples"]) == 84
        with self.voiceover(
            "Llull's fourth figure is a machine you can hold: three paper wheels, one inside another, each "
            "carrying the nine letters, and free to turn. <bookmark mark='a'/>Turn them, and read off three letters "
            "under a pointer. <bookmark mark='b'/>There are nine times nine times nine, seven hundred and twenty-nine "
            "settings; and Llull's Table lays out the eighty-four ways to choose three different letters. "
            "<bookmark mark='c'/>Each setting poses a question: whether goodness, greatness and eternity agree, and "
            "how. Llull, a missionary, meant the art to convince Muslims and Jews by demonstration rather than by "
            "authority: a calculation all parties could check."
        ) as vo:
            self.play(FadeIn(w1), FadeIn(w2), FadeIn(w3), FadeIn(pointer))
            vo.wait_until("a")
            for a1, a2, a3 in ((TAU / 9, -2 * TAU / 9, 3 * TAU / 9), (2 * TAU / 9, TAU / 9, -TAU / 9)):
                self.play(Rotate(w1, a1, about_point=w1.get_center()), Rotate(w2, a2, about_point=w2.get_center()),
                          Rotate(w3, a3, about_point=w3.get_center()), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(txt[:3]))
            vo.wait_until("c")
            self.play(FadeIn(txt[3]))
        self.clear_scene()

    def legacy(self):
        chain = VGroup(
            history_card(1305, r"Llull", r"\textit{Ars magna}: combinations of concepts", width=3.9, color=HIST,
                         font_size=19),
            history_card(1666, r"Leibniz, aged 19", r"\textit{Dissertatio de arte combinatoria}", width=3.9,
                         color=HIST, font_size=19),
            history_card(1679, r"Leibniz", r"concepts as numbers (next chapter)", width=3.9, color=HIST,
                         font_size=19)).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.6)
        q = quote_card(r"\dots\ a kind of alphabet of human thoughts, and \dots\ everything can be discovered and "
                       r"judged by a comparison of the letters of this alphabet and an analysis of the words made "
                       r"from them.", r"Leibniz, \textit{On the General Characteristic} (c.\ 1679)",
                       r"trans.\ Loemker", width=10.6, font_size=26).move_to([0, -1.4, 0])
        with self.voiceover(
            "Llull was mocked by later scholars, and his art is not a logic: it generates combinations, but cannot "
            "tell good ones from bad. <bookmark mark='a'/>Yet the idea reached a nineteen-year-old in Leipzig. In "
            "1666 Leibniz wrote a dissertation on the art of combinations, citing Llull. <bookmark mark='b'/>What if, "
            "he asked, there were an alphabet of human thoughts, so that every concept was a combination of simple "
            "ones, and reasoning could be done by combining and comparing the letters? Llull had the combinatorics. "
            "Leibniz wanted the arithmetic."
        ) as vo:
            self.play(FadeIn(chain[0]))
            vo.wait_until("a")
            self.play(FadeIn(chain[1]))
            vo.wait_until("b")
            self.play(FadeIn(chain[2]), FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def swift(self):
        q = quote_card(r"\dots\ the most ignorant person, at a reasonable charge, and with a little bodily labour, "
                       r"might write books in philosophy, poetry, politics, laws, mathematics, and theology, without "
                       r"the least assistance from genius or study.", r"Swift, \textit{Gulliver's Travels} (1726), "
                       r"III.5", width=10.6, font_size=27).move_to([0, 0.9, 0])
        frame = VGroup(*[Square(0.42, stroke_color=GREY_C, stroke_width=1.5) for _ in range(40)]).arrange_in_grid(
            rows=4, cols=10, buff=0.04).move_to([0, -2.2, 0])
        lab = label(r"the Lagado engine: \ words on blocks, turned by cranks", font_size=22, color=GREY_A).next_to(
            frame, RIGHT, buff=0.3)
        if lab.get_right()[0] > 6.9:
            lab.next_to(frame, UP, buff=0.15)
        with self.voiceover(
            "The combinatorial dream was famous enough to be mocked. <bookmark mark='a'/>In Gulliver's Travels, in "
            "1726, Jonathan Swift sent Gulliver to the academy of Lagado, where a professor's engine of words on "
            "turning blocks lets the most ignorant person, with a little bodily labour, write books in philosophy, "
            "poetry, politics, law, mathematics and theology, without the least assistance from genius or study. "
            "<bookmark mark='b'/>Swift's target was combination without judgement: an engine that produces every "
            "sentence, and cannot tell a true one from a false one. Llull's problem is the problem a logic must "
            "solve."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(q, color=HIST))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f) for f in frame], lag_ratio=0.02), FadeIn(lab))
        self.clear_scene()
