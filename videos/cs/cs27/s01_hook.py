from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs27.common import (BG, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.three()
        self.plan()

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
            "A proof can be more than a document read from beginning to end. This part studies three precise alternatives. <bookmark mark='a'/> A probabilistically checkable proof uses a robust encoding. True statements have an accepting proof; every proof of a false statement is rejected with bounded probability. <bookmark mark='b'/> Sum-check turns a claimed exponential sum into a conversation about low-degree polynomials over a finite field. Our small experiment checks complete transcripts; its sample frequencies do not establish the theorem. <bookmark mark='c'/> A zero-knowledge protocol can convince a verifier without revealing additional efficiently usable information about a secret colouring, under its stated definition and commitment assumptions. The graph and statement remain public. <bookmark mark='d'/> We will distinguish perfect completeness, soundness error, computational assumptions and actual finite measurements throughout."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Proofs and Randomness", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"randomized classes, \ amplification, \ and hardness against randomness",
            r"circuit lower bounds: \ the switching lemma, \ measured; \ communication complexity",
            r"interactive proofs: \ graph non-isomorphism, \ sum-check, \ IP = PSPACE",
            r"zero knowledge, \ the PCP theorem, \ and why approximation is hard",
            r"the Unique Games Conjecture; \ fine-grained and parameterized complexity",
            r"counting and the permanent; \ average case; \ MIP* = RE",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 27 of Computer Science, Built: Proofs and Randomness. <bookmark mark='a'/> In this part: the "
            "complexity classes of randomized algorithms, and why randomness may not add power after all; lower "
            "bounds for circuits, including the switching lemma, which we measure; communication between two "
            "parties; interactive proofs, from graph non-isomorphism to the sum-check protocol and IP equals PSPACE; "
            "zero knowledge; the PCP theorem, and why it makes approximation hard; the Unique Games Conjecture; "
            "fine-grained and parameterized complexity; counting; and a 2020 result connecting proofs with quantum "
            "entanglement and the halting problem."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
