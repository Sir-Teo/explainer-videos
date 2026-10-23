from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, K, PART, Q, curve, load

RAW = C.SURPRISE


def saturating_softmax() -> VGroup:
    """The softmax of the same five scores, scaled up: the weights pile onto one key until they barely move."""
    s = np.array([1.0, 0.7, 0.4, 0.1, -0.2])
    panels = VGroup()
    for k in (1, 4, 16):
        p = np.exp(k * s) / np.exp(k * s).sum()
        bars = VGroup(*[Rectangle(width=0.26, height=1.6 * float(v) + 0.02, stroke_width=0, fill_color=A,
                                  fill_opacity=0.9) for v in p]).arrange(RIGHT, buff=0.07, aligned_edge=DOWN)
        base = Line(bars.get_corner(DL) + LEFT * 0.05, bars.get_corner(DR) + RIGHT * 0.05, color=GREY_C, stroke_width=1.5)
        lab = label(rf"scores $\times{k}$", font_size=22, color=GREY_B).next_to(base, DOWN, buff=0.1)
        panels.add(VGroup(bars, base, lab))
    panels.arrange(RIGHT, buff=0.6, aligned_edge=DOWN)
    arrows = VGroup(*[Arrow(a[1].get_right() + UP * 0.4, b[1].get_left() + UP * 0.4, buff=0.1, color=GREY_B,
                            stroke_width=2, max_tip_length_to_length_ratio=0.3) for a, b in zip(panels[:-1], panels[1:])])
    return VGroup(panels, arrows)


class Scale(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.collapse()
        self.saturate()

    def card(self):
        card = chapter_card(3, r"Why divide by $\sqrt{d}$", r"What goes wrong when the vectors get longer?",
                            lit=(2017,), part=PART)
        with self.voiceover("Chapter three. Why divide by the square root of d."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def derive(self):
        d = load("dotscale")
        ds = [int(v) for v in d["ds"]]
        sd = np.asarray(d["sd"])
        sds = np.asarray(d["sd_scaled"])
        colors = {r"q": Q, r"k": K, r"q_i": Q, r"k_i": K}
        rows = [
            cmath(r"q \cdot k", r"=", r"\textstyle\sum_{i=1}^{d}\, q_i\, k_i", font_size=36, colors=colors),
            cmath(r"\operatorname{E}[q_i k_i]", r"=", r"\operatorname{E}[q_i]\operatorname{E}[k_i] = 0", font_size=36),
            cmath(r"\operatorname{Var}(q_i k_i)", r"=", r"\operatorname{E}[q_i^2]\operatorname{E}[k_i^2] = 1", font_size=36),
            cmath(r"\operatorname{Var}(q \cdot k)", r"=", r"\textstyle\sum_{i=1}^{d} \operatorname{Var}(q_i k_i) = d",
                  font_size=36),
            cmath(r"\operatorname{Var}\big(q \cdot k / \sqrt{d}\,\big)", r"=", r"d / d = 1", font_size=36),
        ]
        whys = [why(r"$d$ products, added"), why(r"independent, \ mean $0$"), why(r"independent, \ variance $1$"),
                why(r"independent terms: \ variances add"), why(r"dividing by $c$ divides the variance by $c^2$")]
        step = ladder(self, rows, whys, keep=5, top=3.1, x=-1.6, buff=0.5, edge=6.9)
        xs_ = [-0.6 + 1.45 * j for j in range(len(ds))]

        def row(head, vals, col, y):
            g_ = VGroup(label(head, font_size=22, color=col).move_to([-1.6, y, 0], aligned_edge=RIGHT))
            g_.add(*[MathTex(v, font_size=26, color=col).move_to([x_, y, 0]) for x_, v in zip(xs_, vals)])
            return g_

        grid = VGroup(row(r"$d$", [str(v) for v in ds], GREY_A, -2.35),
                      row(r"spread of $q\cdot k$", [f"{v:.1f}" for v in sd], RAW, -2.85),
                      row(r"spread of $q\cdot k/\sqrt{d}$", [f"{v:.2f}" for v in sds], Q, -3.35))
        grid.set_x(0)
        cap = note(rf"computed: \ $2{{,}}000$ random queries, ${int(d['n'])}$ random keys each").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Take a query and a key whose d numbers are independent, with mean zero and variance one, roughly what "
            f"a freshly initialized network makes. <bookmark mark='a'/> Measure how far their dot product spreads: "
            f"{sd[0]:.1f} at d of {ds[0]}, {sd[-1]:.0f} at {ds[-1]}. It grows with the size of the vectors. Why? "
            "<bookmark mark='b'/> The dot product is a sum of d products. <bookmark mark='c'/> Each product has mean "
            "zero, since its two factors are independent. <bookmark mark='d'/> And variance one: the expected square "
            "of a product of independent numbers is the product of their expected squares. <bookmark mark='e'/> "
            "Independent terms add their variances, so the dot product has variance d: its spread grows like the "
            "square root of d. <bookmark mark='f'/> Divide by the square root of d and the variance is back to one, "
            f"whatever the size: measured, {sds.min():.2f} to {sds.max():.2f}."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(grid[0]), FadeIn(grid[1]), FadeIn(cap))
            vo.wait_until("b")
            self.play(Indicate(rows[0][2], color=Q, scale_factor=1.05))
            vo.wait_until("c")
            step(1)
            vo.wait_until("d")
            step(2)
            vo.wait_until("e")
            step(3)
            vo.wait_until("f")
            step(4)
            self.play(FadeIn(grid[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def collapse(self):
        d = load("dotscale")
        ds = [int(v) for v in d["ds"]]
        raw, scl = np.asarray(d["raw_ent"]), np.asarray(d["scaled_ent"])
        n = int(d["n"])
        mx = float(d["max_ent"])
        lx = np.log2(ds)
        ax = Axes(x_range=[0.5, 9.5, 1], y_range=[0, 6.5, 1], x_length=6.2, y_length=4.0, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-3.3, -0.5, 0])
        xt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(math.log2(v), 0), DOWN, buff=0.1) for v in ds])
        yt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(0.5, v), LEFT, buff=0.1) for v in (0, 2, 4, 6)])
        xn = label(r"$d$, \ the numbers in each vector", font_size=24, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yn = label(rf"how spread the weights are \ (entropy over ${n}$ keys, bits)", font_size=22, color=GREY_A)
        yn.next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        top = DashedLine(ax.c2p(0.5, mx), ax.c2p(9.5, mx), color=GREY_B, stroke_width=1.5)
        topl = MathTex(rf"\log_2 {n} = {mx:.0f}", font_size=20, color=GREY_B).next_to(ax.c2p(9.5, mx), UP, buff=0.08)
        topl.align_to(ax.c2p(9.5, mx), RIGHT)
        c_raw = VGroup(curve(ax, lx, raw, RAW, 4), *[Dot(ax.c2p(a, b), radius=0.06, color=RAW) for a, b in zip(lx, raw)])
        c_scl = VGroup(curve(ax, lx, scl, Q, 4), *[Dot(ax.c2p(a, b), radius=0.06, color=Q) for a, b in zip(lx, scl)])
        l_raw = label(r"$q \cdot k$", font_size=28, color=RAW).next_to(ax.c2p(lx[-1], raw[-1]), UP, buff=0.2)
        l_scl = label(r"$q \cdot k / \sqrt{d}$", font_size=28, color=Q).next_to(ax.c2p(lx[-1], scl[-1]), DOWN, buff=0.25)
        g = np.random.default_rng(5)  # one draw at the largest d, for the strips (illustrating the computed curves)
        qv, kv = g.normal(size=ds[-1]), g.normal(size=(n, ds[-1]))
        s = kv @ qv

        def sm(z):
            e = np.exp(z - z.max())
            return e / e.sum()

        def strip(w, color, y):
            bw_ = 5.2 / n
            return VGroup(*[Rectangle(width=bw_ * 0.8, height=max(1.5 * v / max(w.max(), 0.3), 0.005), stroke_width=0,
                                      fill_color=color, fill_opacity=0.9).move_to([1.4 + (i + 0.5) * bw_, y + 0.75 * v / max(w.max(), 0.3), 0])
                            for i, v in enumerate(w)])

        s_raw, s_scl = strip(sm(s), RAW, 0.6), strip(sm(s / math.sqrt(ds[-1])), Q, -2.0)
        t_raw = label(rf"$d = {ds[-1]}$, \ no division: \ one key takes it all", font_size=22, color=RAW)
        t_raw.next_to(s_raw, UP, buff=0.15).set_x(4.0)
        t_scl = label(r"divided by $\sqrt{d}$: \ spread out", font_size=22, color=Q).next_to(s_scl, UP, buff=0.15).set_x(4.0)
        tag = note(r"one random query, \ illustration").next_to(s_scl, DOWN, buff=0.15).set_x(4.0)
        with self.voiceover(
            "Why does the spread matter? Because the softmax turns differences of scores into ratios of weights, "
            "exponentially. <bookmark mark='a'/> Feed it scores that spread like the square root of d and it stops "
            f"averaging: it picks one key and ignores the rest. Over {n} keys, the entropy of the weights, a "
            f"measure of how many keys share them, falls from {raw[0]:.1f} bits at d of {ds[0]} to {raw[-1]:.2f} "
            f"at {ds[-1]}. <bookmark mark='b'/> Divided by the square root of d, the weights stay spread out, "
            f"{scl.min():.1f} bits at every size, just under the {mx:.0f} bits of a perfectly even share."
        ) as vo:
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(top), FadeIn(topl))
            vo.wait_until("a")
            self.play(Create(c_raw), FadeIn(l_raw), run_time=1.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in s_raw], lag_ratio=0.01), FadeIn(t_raw))
            vo.wait_until("b")
            self.play(Create(c_scl), FadeIn(l_scl), run_time=1.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in s_scl], lag_ratio=0.01), FadeIn(t_scl), FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def saturate(self):
        d = load("dotscale")
        sig, jac = np.asarray(d["sig"]), np.asarray(d["jac_by_sig"])
        ds = [int(v) for v in d["ds"]]
        sd = np.asarray(d["sd"])
        rows = [
            cmath(r"p_i", r"=", r"\frac{e^{s_i}}{\sum_j e^{s_j}}", font_size=34, colors={r"p_i": A}),
            cmath(r"\frac{\partial p_i}{\partial s_j}", r"=", r"p_i\,(\delta_{ij} - p_j)", font_size=34),
            cmath(r"p \to (1, 0, \dots, 0)", r"\;\Rightarrow\;", r"\frac{\partial p}{\partial s} \to 0", font_size=34),
        ]
        whys = [why(r"the softmax", font_size=20), why(r"quotient rule", font_size=20),
                why(r"every term has a factor \\ that is $0$ or $1 - 1$", font_size=20)]
        step = ladder(self, rows, whys, keep=3, top=3.05, x=-4.0, buff=0.5, edge=6.9)
        g = axes([-1, math.log10(sig[-1]), 1], [0, 0.35, 0.1], x_length=6.0, y_length=3.0,
                 xlabel=r"spread of the scores", ylabel=r"how much the weights respond \ ($\|\partial p/\partial s\|$)",
                 xticks=[], yticks=[0, 0.1, 0.2, 0.3], center=[3.2, -1.45, 0])
        ax = g.ax
        for e in (-1, 0, 1, 2):
            g.add(MathTex(f"10^{{{e}}}" if e not in (0, 1) else ("1" if e == 0 else "10"), font_size=20,
                          color=GREY_B).next_to(ax.c2p(e, 0), DOWN, buff=0.12))
        c_ = curve(ax, np.log10(sig), jac, A, 3.5)
        pk = int(np.argmax(jac))
        mk = VGroup()
        for v, col, txt in ((1.0, Q, r"$\div\sqrt{d}$"), (sd[-1], RAW, rf"$d = {ds[-1]}$, raw")):
            x = math.log10(v)
            y = float(np.interp(x, np.log10(sig), jac))
            dt = Dot(ax.c2p(x, y), radius=0.08, color=col)
            mk.add(VGroup(dt, label(txt, font_size=20, color=col).next_to(dt, UP, buff=0.12)))
        demo = saturating_softmax().move_to([3.4, -1.0, 0])
        demo_t = note(r"the same five scores, multiplied: \ illustration").next_to(demo, DOWN, buff=0.2)
        sat = gloss(r"saturated", r"one weight near $1$: \ small changes to the scores \\ no longer move the weights, "
                    r"so no gradient flows", width=5.2, color=RAW).to_corner(DL, buff=0.35)
        jr = float(np.interp(math.log10(sd[-1]), np.log10(sig), jac))
        j1 = float(np.interp(0.0, np.log10(sig), jac))
        cite_ = cite(r"A.~Vaswani et al.\ (2017), \S3.2.1; \ G.~Yang et al., $\mu$P (2022)", corner=UR)
        with self.voiceover(
            "There is a second cost, and it is worse. Training moves the scores by gradients, and those pass through "
            "the softmax's derivative. <bookmark mark='a'/> The derivative of weight i with respect to score j is p i "
            "times delta i j minus p j. <bookmark mark='b'/> When one weight is near one and the rest near zero, "
            "every term has a factor near zero: the softmax is saturated, and the scores stop learning. "
            f"<bookmark mark='c'/> How much the weights respond peaks when the scores spread by about "
            f"{sig[pk]:.0f}, and falls away on both sides. <bookmark mark='d'/> Scaled scores, with a spread of one, "
            f"respond at {j1:.2f}. Unscaled at d of {ds[-1]}, the response is {jr:.2f}, and it keeps falling as the "
            "vectors grow. That is the reason Vaswani and colleagues gave in 2017 for the square root. Later work on "
            "very wide networks, Greg Yang's mu P, argues for one over d once training has lined queries up with "
            "their keys; we will meet runaway scores again in chapter thirteen."
        ) as vo:
            step(0)
            self.play(FadeIn(demo), FadeIn(demo_t))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(sat, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeOut(demo), FadeOut(demo_t))
            self.play(FadeIn(g), Create(c_), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(mk[0]), FadeIn(mk[1]), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()
