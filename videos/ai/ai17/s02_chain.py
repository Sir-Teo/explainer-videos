from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai17.common import CHAIN, DIRECT, curve, load


def verdict(a: float) -> str:
    return "solved" if a > 0.95 else "shaky" if a > 0.65 else "a coin flip"


class Chain(VoiceoverScene):
    def construct(self):
        self.card()
        self.depth()
        self.results()

    def card(self):
        card = chapter_card(1, r"Thinking out loud is computing", r"Why does writing the steps help?", lit=(2024,), part=17)
        with self.voiceover("Chapter one. Thinking out loud is computing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def depth(self):
        L, P, W = 4, 5, 6  # layers, prompt tokens, tokens written
        T = P + W
        dx, dy = 1.0, 0.72
        x0, y0 = -5.4, -1.9

        def at(l, t):
            return np.array([x0 + t * dx, y0 + l * dy, 0])

        nodes = VGroup(*[Dot(at(l, t), radius=0.07, color=GREY_B if t < P else CHAIN).set_opacity(0.9 if l else 0.6)
                         for t in range(T) for l in range(L + 1)])
        ups = VGroup(*[Line(at(l, t), at(l + 1, t), stroke_width=1.5, color=GREY_D) for t in range(T) for l in range(L)])
        att = VGroup(*[Line(at(l, s), at(l + 1, t), stroke_width=0.8, color=GREY_D).set_stroke(opacity=0.45)
                       for t in range(T) for s in range(max(0, t - 2), t) for l in range(L)])
        toks = VGroup(*[label(r"$x_{%d}$" % (t + 1), font_size=20, color=GREY_B if t < P else CHAIN).next_to(at(0, t), DOWN, buff=0.15)
                        for t in range(T)])
        ll = VGroup(*[label(rf"layer ${l}$", font_size=18, color=GREY_C).next_to(at(l, 0), LEFT, buff=0.25) for l in range(1, L + 1)])
        back = VGroup(*[CurvedArrow(at(L, t) + UR * 0.06, at(0, t + 1) + LEFT * 0.12, angle=-PI / 3, stroke_width=2,
                                    color=CHAIN, tip_length=0.12) for t in range(P - 1, T - 1)])
        bl = label(r"each written token goes back in", font_size=22, color=CHAIN).next_to(at(L, P + 2), UP, buff=0.35)
        # the longest chain of steps done one after another
        one = [at(0, 0)] + [at(l, min(l, P - 1)) for l in range(1, L + 1)]
        one[-1] = at(L, P - 1)
        p1 = VMobject(stroke_width=6, color=DIRECT).set_points_as_corners(one)
        snake = [at(0, P - 1)]
        for t in range(P - 1, T):
            snake += [at(L, t)]
            if t < T - 1:
                snake += [at(0, t + 1)]
        p2 = VMobject(stroke_width=6, color=C.BITS).set_points_as_corners(snake)
        colors = {r"L": GREY_A, r"k": CHAIN}
        f1 = cmath(r"\text{at once:}\quad", r"L", r"\text{ steps in a row}", colors=colors, font_size=30)
        f2 = cmath(r"\text{with } ", r"k", r"\text{ tokens of thought:}\quad", r"L", r"\,(k+1)", colors=colors, font_size=30)
        fs = VGroup(f1, f2).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(UP, buff=0.35).shift(RIGHT * 1.0)
        cite_ = cite(r"W.~Merrill \& A.~Sabharwal, \textit{The Expressive Power of Transformers with Chain of Thought} (2024)", corner=DR)
        tag = note(r"schematic: \ $4$ layers").to_corner(DL, buff=0.25)
        with self.voiceover(
            "Why does writing help? Look at the computation. A transformer runs every token through the same fixed "
            "stack of layers. <bookmark mark='a'/> Answering at once, the longest chain of steps that happen one "
            "after another is as tall as the stack: L layers, however hard the question. <bookmark mark='b'/> But a "
            "token it writes goes back in as input. <bookmark mark='c'/> So the chain of steps can climb the stack, "
            "come back down, and climb again, once per token. With k tokens of thought, L times k plus one steps in a "
            "row. <bookmark mark='d'/> Theory backs this up: answering at once, a transformer is limited to shallow "
            "computations; given a long enough chain of thought, it can carry out any step-by-step procedure."
        ) as vo:
            self.play(FadeIn(nodes[: (L + 1) * P]), FadeIn(toks[:P]), FadeIn(ll), FadeIn(tag),
                      Create(VGroup(*[u for u in ups if u.get_start()[0] < x0 + P * dx - 0.5])),
                      Create(VGroup(*[a for a in att if a.get_end()[0] < x0 + P * dx - 0.5])), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(p1), Write(f1), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(nodes[(L + 1) * P:]), FadeIn(toks[P:]), FadeIn(VGroup(*[u for u in ups if u.get_start()[0] > x0 + P * dx - 0.5])),
                      FadeIn(VGroup(*[a for a in att if a.get_end()[0] > x0 + P * dx - 0.5])),
                      LaggedStart(*[Create(b) for b in back], lag_ratio=0.2), FadeIn(bl), run_time=2.0)
            vo.wait_until("c")
            dot = glow_dot(snake[0], color=C.BITS, radius=0.09)
            self.play(p1.animate.set_stroke(opacity=0.3), FadeIn(dot))
            self.play(Create(p2), MoveAlongPath(dot, p2.copy()), Write(f2), run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(cite_), Circumscribe(f2, color=C.BITS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def results(self):
        p = load("parity")
        ns = [int(n) for n in p["ns"]]
        d = [float(p[f"acc_direct{n}"]) for n in ns]
        c = [float(p[f"acc_cot{n}"]) for n in ns]
        ax = Axes(x_range=[0, 3, 1], y_range=[0, 1, 0.25], x_length=5.2, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.3, -0.5, 0])
        yt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 0.5, 1)])
        chance = DashedLine(ax.c2p(0, 0.5), ax.c2p(3, 0.5), color=GREY_D, stroke_width=1.5)
        cl = label(r"chance", font_size=18, color=GREY_C).next_to(ax.c2p(3, 0.5), RIGHT, buff=0.08)
        bw = 0.42
        bars_d = VGroup(*[Rectangle(width=bw, height=max(ax.y_length * v, 0.01), stroke_width=0, fill_color=DIRECT, fill_opacity=0.85)
                          .move_to(ax.c2p(i + 0.5, 0) + LEFT * bw * 0.55, aligned_edge=DOWN) for i, v in enumerate(d)])
        bars_c = VGroup(*[Rectangle(width=bw, height=max(ax.y_length * v, 0.01), stroke_width=0, fill_color=CHAIN, fill_opacity=0.85)
                          .move_to(ax.c2p(i + 0.5, 0) + RIGHT * bw * 0.55, aligned_edge=DOWN) for i, v in enumerate(c)])
        xt = VGroup(*[label(rf"$n = {n}$ bits", font_size=22, color=GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.15)
                      for i, n in enumerate(ns)])
        yn = label(r"right on new strings", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        key = VGroup(label(r"answer at once", font_size=22, color=DIRECT), label(r"running parity first", font_size=22, color=CHAIN))
        key.arrange(RIGHT, buff=0.5).next_to(xt, DOWN, buff=0.3)
        # training at n = 16
        cd, cc = np.asarray(p["curve_direct"]), np.asarray(p["curve_cot"])
        smax = float(max(cd[:, 0].max(), cc[:, 0].max()))
        bx = Axes(x_range=[0, smax, smax / 5], y_range=[0.4, 1, 0.1], x_length=5.0, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([3.5, -0.5, 0])
        bxt = VGroup(*[MathTex(f"{int(v):,}".replace(",", "{,}"), font_size=20, color=GREY_B).next_to(bx.c2p(v, 0.4), DOWN, buff=0.1)
                       for v in (0, smax / 2, smax)])
        byt = VGroup(*[MathTex(rf"{int(100 * v)}\%", font_size=20, color=GREY_B).next_to(bx.c2p(0, v), LEFT, buff=0.1) for v in (0.5, 1.0)])
        bxn = label(r"training steps", font_size=20, color=GREY_A).next_to(bxt, DOWN, buff=0.1)
        byn = label(r"learning, \ at $n = 16$", font_size=22, color=GREY_A).next_to(bx, UP, buff=0.15).align_to(bx, LEFT)
        ld = curve(bx, cd[:, 0], np.clip(cd[:, 1], 0.4, 1), DIRECT, 3)
        lc = curve(bx, cc[:, 0], np.clip(cc[:, 1], 0.4, 1), CHAIN, 3)
        hit = [s for s, a in cc if a > 0.95]
        first = int(hit[0]) if hit else None
        tag = note(r"two layers, \ $64$ numbers wide; \ same training for both").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Here are all our runs, on strings of four, eight and sixteen bits. <bookmark mark='a'/> Answering at "
            f"once is {verdict(d[0])} at four bits, {verdict(d[1])} at eight, and {verdict(d[2])} at sixteen: every "
            "bit flips the answer, and two layers can't learn to combine sixteen of them at once. "
            "<bookmark mark='b'/> With the running parity written first, that is, whether the count of ones so far "
            "is odd or even, all three are "
            f"{'solved' if min(c) > 0.95 else 'much better'}. <bookmark mark='c'/> And the chain is also easier to "
            "learn. " + (f"At sixteen bits it's reliable after about {first:,} steps; " if first else "")
            + "answering at once never gets off the ground."
        ) as vo:
            self.play(Create(ax), FadeIn(yt), Create(chance), FadeIn(cl), FadeIn(xt), FadeIn(yn), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_d], lag_ratio=0.3), FadeIn(key[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars_c], lag_ratio=0.3), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(Create(bx), FadeIn(bxt), FadeIn(byt), FadeIn(bxn), FadeIn(byn))
            self.play(Create(lc), Create(ld), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
