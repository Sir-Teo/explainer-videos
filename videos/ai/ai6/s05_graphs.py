from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import HIDDEN

SEEN = C.TRUE_P


def node(tex, pos, hidden=True, r=0.36):
    c = Circle(radius=r, color=HIDDEN if hidden else SEEN, stroke_width=3,
               fill_color=BACKGROUND if hidden else SEEN, fill_opacity=1 if hidden else 0.35).move_to(pos)
    return VGroup(c, MathTex(tex, font_size=30).move_to(pos))


def edge(a, b):
    d = b[0].get_center() - a[0].get_center()
    d = d / np.linalg.norm(d)
    return Arrow(a[0].get_center() + d * a[0].width / 2, b[0].get_center() - d * b[0].width / 2, buff=0.04,
                 color=GREY_B, stroke_width=3, max_tip_length_to_length_ratio=0.25)


class Graphs(VoiceoverScene):
    def construct(self):
        self.card()
        self.pictures()

    def card(self):
        card = chapter_card(4, r"Models as pictures", r"What depends on what?", part=6)
        with self.voiceover("Chapter four. Models as pictures."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def pictures(self):
        # the mixture: a hidden source, then a page (a plate of n pages)
        z = node(r"z", [-4.6, 1.6, 0])
        x = node(r"x", [-4.6, -0.2, 0], hidden=False)
        plate = SurroundingRectangle(VGroup(z, x), color=GREY_C, buff=0.35, corner_radius=0.12)
        pn = MathTex(r"n", font_size=28, color=GREY_B).next_to(plate.get_corner(DR), UL, buff=0.1)
        mix = VGroup(z, x, edge(z, x), plate, pn)
        mix_l = label(r"a mixture: \\ hidden source $\to$ page", font_size=24, color=GREY_A).next_to(plate, DOWN, buff=0.25)
        # the hidden Markov model
        zs = [node(rf"z_{k}", [-1.6 + 1.5 * k, 1.6, 0]) for k in range(1, 5)]
        xs = [node(rf"x_{k}", [-1.6 + 1.5 * k, -0.2, 0], hidden=False) for k in range(1, 5)]
        hmm = VGroup(*zs, *xs, *[edge(zs[k], zs[k + 1]) for k in range(3)], *[edge(zs[k], xs[k]) for k in range(4)])
        hmm_l = label(r"a hidden Markov model: \\ a chain of hidden states, \ each emitting a letter", font_size=24,
                      color=GREY_A).next_to(VGroup(*xs), DOWN, buff=0.6)
        key = VGroup(VGroup(Circle(radius=0.14, color=HIDDEN, stroke_width=3), label(r"hidden", font_size=22, color=HIDDEN)).arrange(RIGHT, buff=0.12),
                     VGroup(Circle(radius=0.14, color=SEEN, stroke_width=3, fill_color=SEEN, fill_opacity=0.35),
                            label(r"observed", font_size=22, color=SEEN)).arrange(RIGHT, buff=0.12))
        key.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.35)
        colors = {r"\mathrm{parents}(v)": HIDDEN}
        f = cmath(r"p(\text{everything})", "=", r"\prod_{v}", r"\,p\big(v \mid", r"\mathrm{parents}(v)", r"\big)",
                  colors=colors, font_size=40).to_edge(DOWN, buff=1.15)
        fn = label(r"$\prod$: \ multiply one probability per circle, \ each given the circles that point into it",
                   font_size=24, color=GREY_A)
        fn.next_to(f, DOWN, buff=0.15)
        cite_ = cite(r"J.~Pearl, \textit{Probabilistic Reasoning in Intelligent Systems} (1988)", corner=DR)
        # a language model: every earlier letter points at every later one
        lm = [node(rf"x_{k}", [-1.6 + 1.5 * k, 0.6, 0], hidden=False) for k in range(1, 5)]
        lm_e = VGroup(*[CurvedArrow(lm[a][0].get_top() + UP * 0.02, lm[b][0].get_top() + UP * 0.02, angle=-0.6 - 0.25 * (b - a),
                                    color=GREY_B, stroke_width=2.5, tip_length=0.14)
                        for a in range(4) for b in range(a + 1, 4)])
        lm_l = label(r"a language model: \ every earlier letter points at every later one", font_size=24,
                     color=GREY_A).next_to(VGroup(*lm), DOWN, buff=0.5)
        # the drawing rules, built big as they're named, then shrunk into the mixture's own z -> x
        dz, dx = node(r"z", [0, 1.5, 0], r=0.62), node(r"x", [0, -1.2, 0], r=0.62)
        for d_ in (dz, dx):
            d_[0].set_stroke(GREY_B).set_fill(BACKGROUND, opacity=1)
            d_[1].scale(1.5)
        dzh = node(r"z", [0, 1.5, 0], r=0.62)
        dzh[1].scale(1.5)
        dxo = node(r"x", [0, -1.2, 0], hidden=False, r=0.62)
        dxo[1].scale(1.5)
        d_e = edge(dz, dx)
        tq = label(r"one circle per quantity", font_size=28, color=GREY_A).next_to(VGroup(dz, dx), LEFT, buff=0.8)
        to = label(r"shaded: \ observed", font_size=28, color=SEEN).next_to(dx, RIGHT, buff=0.6)
        th = label(r"empty: \ hidden", font_size=28, color=HIDDEN).next_to(dz, RIGHT, buff=0.6)
        ta = label(r"arrow: \ depends directly on", font_size=28, color=GREY_B).next_to(d_e, LEFT, buff=0.5)
        with self.voiceover(
            "Every model in this part can be drawn the same way: <bookmark mark='q'/> a circle for each quantity, "
            "<bookmark mark='o'/> shaded if we observe it, <bookmark mark='h'/> empty if it's hidden, "
            "<bookmark mark='r'/> and an arrow wherever one depends directly on another. "
            "<bookmark mark='a'/> The mixture: a hidden choice of source, then a page, repeated for every page. "
            "<bookmark mark='b'/> The hidden Markov model: a chain of hidden states, each emitting a letter. "
            "<bookmark mark='c'/> The picture is a formula. The probability of everything is a product, the big "
            "pi: multiply one probability per circle, each given only the circles that point into it, its parents. "
            "That's a Bayesian network, Judea "
            "Pearl's language for reasoning under uncertainty."
        ) as vo:
            vo.wait_until("q")
            self.play(Create(dz[0]), Create(dx[0]), FadeIn(dz[1]), FadeIn(dx[1]), FadeIn(tq))
            vo.wait_until("o")
            self.play(Transform(dx, dxo), FadeIn(to))
            vo.wait_until("h")
            self.play(Transform(dz, dzh), FadeIn(th))
            vo.wait_until("r")
            self.play(GrowArrow(d_e), FadeOut(tq), FadeIn(ta))
            vo.wait_until("a")
            self.play(FadeOut(VGroup(to, th, ta)), ReplacementTransform(dz, mix[0]), ReplacementTransform(dx, mix[1]),
                      ReplacementTransform(d_e, mix[2]), FadeIn(key), run_time=1.2)
            self.play(FadeIn(mix[3:]), FadeIn(mix_l))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in hmm], lag_ratio=0.05), FadeIn(hmm_l), run_time=2.0)
            vo.wait_until("c")
            self.play(Write(f), FadeIn(fn), FadeIn(cite_))
        self.wait(0.3)
        self.play(FadeOut(VGroup(mix, mix_l, hmm, hmm_l)))
        with self.voiceover(
            "Part one's language models fit the same picture, with an arrow from every earlier letter to every later "
            "one. <bookmark mark='a'/> Nothing is hidden, but nothing is simplified either: each factor is a "
            "prediction from the whole past. Counting can't fill in factors like that. A network, from part eight "
            "on, can."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m) for m in lm], lag_ratio=0.1), FadeIn(lm_l))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(e) for e in lm_e], lag_ratio=0.15), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()
