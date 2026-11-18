from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono, words)


class Hook(WatchScene):
    def construct(self):
        self.three()
        self.title(PART)

    def pic_bits(self):
        sq = VGroup(*[Square(side_length=0.17, stroke_color=GREY_D, stroke_width=0.5,
                             fill_color=DATA if (i * 37 + 11) % 5 < 2 else BG, fill_opacity=0.9)
                      for i in range(96)]).arrange_in_grid(rows=4, cols=24, buff=0.02)
        marks = VGroup(*[SurroundingRectangle(sq[i], color=HEAD, buff=0.02, stroke_width=2.5) for i in (5, 42, 77)])
        return VGroup(sq, marks).scale_to_fit_width(3.6)

    def pic_talk(self):
        pv = label(r"prover", font_size=18, color=HEAD)
        vf = label(r"verifier", font_size=18, color=DATA).next_to(pv, RIGHT, buff=1.6)
        arrows = VGroup()
        for i in range(3):
            y = -0.25 * i
            a = Arrow(pv.get_right() + RIGHT * 0.1 + UP * (y + 0.05), vf.get_left() + LEFT * 0.1 + UP * (y + 0.05),
                      buff=0, stroke_width=2, color=HEAD, max_tip_length_to_length_ratio=0.12)
            b = Arrow(vf.get_left() + LEFT * 0.1 + UP * (y - 0.07), pv.get_right() + RIGHT * 0.1 + UP * (y - 0.07),
                      buff=0, stroke_width=2, color=DATA, max_tip_length_to_length_ratio=0.12)
            arrows.add(a, b)
        return VGroup(pv, vf, arrows).scale(1.25)

    def pic_zk(self):
        pts = [UP * 0.55, DOWN * 0.4 + LEFT * 0.75, DOWN * 0.4 + RIGHT * 0.75, UP * 0.05 + RIGHT * 1.5,
               UP * 0.05 + LEFT * 1.5]
        E = [(0, 1), (0, 2), (1, 2), (2, 3), (0, 3), (1, 4), (0, 4)]
        edges = VGroup(*[Line(pts[a], pts[b], color=GREY_B, stroke_width=2) for a, b in E])
        edges[2].set_color(WHITE).set_stroke(width=4)
        cols = {1: YES, 2: NO}
        dots = VGroup(*[Dot(p, radius=0.13, color=cols.get(i, GREY_D)) for i, p in enumerate(pts)])
        return VGroup(edges, dots)

    def three(self):
        head = label(r"Three ways to be convinced", font_size=34).to_edge(UP, buff=0.3)
        z = load("zk")
        s = load("sumcheck")
        cards = VGroup()
        items = [
            (r"\textbf{1. A proof you check by sampling}", r"read a few random bits \\ of a long proof; \\ a wrong "
             r"proof is caught \\ with high probability", DATA),
            (r"\textbf{2. A proof by conversation}", rf"claims {s['true']} satisfying assignments; \\ sampled cheating survival: \\ "
             rf"{round(s['cheat_survive'] * s['trials'])} of {s['trials']:,} mod {s['p']}; \\ "
             rf"{round(s['cheat_survive_big'] * 300)} of 300 mod {s['big_p']:,}", HEAD),
            (r"\textbf{3. A proof that reveals nothing}", rf"a graph is 3-colourable, \\ yet no colouring is shown; "
             rf"\\ a cheater survives {z['rounds_for_1e9']} rounds \\ with probability below $10^{{-9}}$", YES),
        ]
        pics = [self.pic_bits(), self.pic_talk(), self.pic_zk()]
        for (t, d, col), pic in zip(items, pics):
            box_ = RoundedRectangle(width=4.2, height=4.7, corner_radius=0.15, stroke_color=col, fill_color=BG,
                                    fill_opacity=1)
            tt = label(t, font_size=21, color=col).move_to(box_.get_top() + DOWN * 0.42)
            if tt.width > 3.9:
                tt.scale_to_fit_width(3.9)
            dd = label(d, font_size=20, color=WHITE).next_to(tt, DOWN, buff=0.3)
            pic.move_to(box_.get_bottom() + UP * 1.0)
            cards.add(VGroup(box_, tt, dd, pic))
        cards.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.4)
        moral = label(r"each trades certainty for a probability of error that can be made as small as you like",
                      font_size=23, color=LAM).next_to(cards, DOWN, buff=0.35)
        with self.voiceover(
            "I can convince you that a statement is true while you read only a handful of bits of my proof. "
            "<bookmark mark='a'/> Write the proof in a robust code, and a wrong proof is wrong almost everywhere. A few random spot checks catch it. "
            f"<bookmark mark='b'/> Or we can talk. I claim a formula has {s['true']} satisfying assignments. You ask me random questions about polynomials, and a liar gets caught. "
            "<bookmark mark='c'/> Or I can convince you that a graph is three-colourable, and show you nothing about the colouring. "
            "<bookmark mark='d'/> Each one trades certainty for an error you can make as small as you like. How can that possibly work?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(GrowFromEdge(c, DOWN), run_time=0.9)
            vo.wait_until("d")
            self.play(Write(moral))
        self.wait(0.3)
        self.clear_scene()

