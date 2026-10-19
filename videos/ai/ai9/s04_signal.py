from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai9.common import NEURON, curve, load

SMALL, HE, BIG = "#7FD3FF", C.BITS, C.SURPRISE


class Signal(VoiceoverScene):
    def construct(self):
        self.card()
        self.layers()
        self.rule()

    def card(self):
        card = chapter_card(3, r"Signals through fifty layers", r"How should the weights start?", part=9)
        with self.voiceover("Chapter three. Keeping signals alive."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def layers(self):
        g = load("signal")
        L = int(g["L"])
        lo, hi = -9, 9
        ax = Axes(x_range=[0, L, 10], y_range=[0, hi - lo, 3], x_length=7.6, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.05}).move_to([-2.0, -0.5, 0])
        yl = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=22, color=GREY_B).next_to(ax.c2p(0, v - lo), LEFT, buff=0.1)
                      for v in range(lo, hi + 1, 3)])
        xl = label(r"layer", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yn = label(r"typical size of the signal", font_size=24, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        ls = np.arange(1, L + 1)

        def line(key, col, sw=4):
            v = np.clip(np.log10(np.maximum(np.asarray(g[key]), 1e-30)), lo, hi) - lo
            return curve(ax, ls, v, col, sw)

        c_small, c_he, c_big = line("sd_small", SMALL), line("sd_he", HE), line("sd_big", BIG)

        def ride(key, col):
            """A pulse travelling through the layers along the curve, as big as the signal it carries."""
            vals = np.asarray(g[key])
            pulse = glow_dot(ax.c2p(1, np.clip(np.log10(vals[0]), lo, hi) - lo), color=col, radius=0.1)

            def upd(m, alpha):
                k = alpha * (L - 1)
                v = float(vals[min(int(k), L - 1)])
                r = float(np.clip(0.1 * v ** 0.12, 0.012, 0.55))
                m.become(glow_dot(ax.c2p(k + 1, float(np.clip(np.log10(max(v, 1e-30)), lo, hi)) - lo), color=col, radius=r))

            return Succession(UpdateFromAlphaFunc(pulse, upd), FadeOut(pulse, run_time=0.01))
        names = VGroup(label(r"weights $0.7\times$ too small: \ vanishes", font_size=24, color=SMALL),
                       label(r"weights just right", font_size=24, color=HE),
                       label(r"weights $1.4\times$ too big: \ explodes", font_size=24, color=BIG))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.4, 0.6, 0])
        grad = label(r"gradients flowing back do the same, \\ so the first layers can't learn", font_size=24,
                     color=GREY_A).next_to(names, DOWN, buff=0.5).align_to(names, LEFT)
        head = label(r"$50$ layers of $256$ ReLU units, \ random weights", font_size=30).to_edge(UP, buff=0.35)
        # the three spreads of starting weights, as bells of equal area (sd 0.7, 1 and 1.4 times the right one)
        bells = VGroup()
        for k, (f, col) in enumerate(((0.7, SMALL), (1.0, HE), (1.4, BIG))):
            x0 = 3.0 + 1.35 * k
            base = Line([x0 - 0.6, 1.55, 0], [x0 + 0.6, 1.55, 0], color=GREY_C, stroke_width=1.5)
            bell = FunctionGraph(lambda t, f=f: 0.5 / f * np.exp(-0.5 * (t / (0.22 * f)) ** 2), x_range=[-0.6, 0.6],
                                 color=col, stroke_width=3).shift([x0, 1.55, 0])
            bells.add(VGroup(base, bell))
        bells = VGroup(bells[0], bells[2], bells[1])  # in the order the narration shows them
        spread = label(r"the spread of the random starting weights", font_size=22, color=GREY_A)
        spread.next_to(VGroup(*bells), UP, buff=0.2)
        shrink = float(g["sd_small"][0] / g["sd_small"][-1])
        grow = float(g["sd_big"][-1])
        assert 1e7 < shrink < 1e8 and 1e7 < grow < 1e8

        def millions(v):
            return f"{round(v / 1e7) * 10} million"

        with self.voiceover(
            "Before training, the weights are random. But random how? What matters is their spread: how far the "
            "random starting weights stray from zero. Send a signal through fifty layers and track "
            "its size. <bookmark mark='a'/> Draw the weights a little too small, and each layer shrinks the signal "
            f"by a fixed factor. After fifty layers, it's about {millions(shrink)} times smaller: gone. "
            f"<bookmark mark='b'/> A little too big, and it explodes, to about {millions(grow)}. <bookmark mark='c'/> "
            "Only one size keeps it steady, layer after layer. And gradients, flowing backwards, vanish or explode "
            "the same way, which is why deep networks once seemed impossible to train."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(yn), FadeIn(spread))
            vo.wait_until("a")
            self.play(Create(c_small), ride("sd_small", SMALL), FadeIn(names[0]), Create(bells[0]), run_time=3.0,
                      rate_func=linear)
            vo.wait_until("b")
            self.play(Create(c_big), ride("sd_big", BIG), FadeIn(names[2]), Create(bells[1]), run_time=3.0,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(Create(c_he), ride("sd_he", HE), FadeIn(names[1]), Create(bells[2]), run_time=3.0,
                      rate_func=linear)
            self.play(FadeIn(grad))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        g = load("signal")
        colors = {r"\tfrac{2}{n}": HE, r"\tfrac{1}{n}": NEURON}
        f1 = cmath(r"\operatorname{Var}(w)", "=", r"\tfrac{1}{n}", colors=colors, font_size=46)
        f2 = cmath(r"\operatorname{Var}(w)", "=", r"\tfrac{2}{n}", colors=colors, font_size=46)
        for f in (f1, f2):
            f.move_to(UP * 2.6)
        sumv = MathTex(r"\operatorname{Var}\Big(\sum_{i=1}^{n} w_i x_i\Big)", "=", r"n", r"\cdot\operatorname{Var}(w)",
                       r"\cdot\,\mathbb{E}[x^2]", font_size=36).next_to(f1, DOWN, buff=0.35)
        sumv[2].set_color(NEURON)
        why1 = label(r"$n$ inputs, each adding its share of variance: \ the sum keeps the size", font_size=26,
                     color=GREY_A).next_to(sumv, DOWN, buff=0.3)
        # what a layer's units receive, before the ReLU: computed, layer 25 of the steady network
        h = np.asarray(g["hist_he"])[24].astype(float)
        h = h / h.max()
        edges = np.linspace(-4, 4, len(h) + 1)
        bw = 5.6 / len(h)
        bars = VGroup(*[Rectangle(width=bw * 0.92, height=max(2.0 * v, 0.01), stroke_width=0, fill_color=HE,
                                  fill_opacity=0.85).move_to([-3.2 + (edges[i] + edges[i + 1]) / 2 * 0.7, -2.0 + v, 0])
                        for i, v in enumerate(h)])
        base = Line([-6.1, -2.0, 0], [-0.3, -2.0, 0], color=GREY_C, stroke_width=2)
        zero = DashedLine([-3.2, -2.05, 0], [-3.2, 0.1, 0], color=GREY_B, stroke_width=2)
        hl = label(r"what a unit receives, before the ReLU \\ (layer $25$, computed)", font_size=22, color=GREY_A)
        hl.next_to(base, DOWN, buff=0.15)
        neg = VGroup(*[b for b, e in zip(bars, edges[1:]) if e <= 0])
        why2 = label(r"a ReLU zeroes the negative half: \\ only half the variance survives, \\ so double it", font_size=26,
                     color=HE).move_to([3.6, -1.1, 0])
        cites = VGroup(label(r"X.~Glorot \& Y.~Bengio (2010): \ $1/n$, \ for tanh", font_size=22, color=GREY_B),
                       label(r"K.~He, X.~Zhang, S.~Ren \& J.~Sun (2015): \ $2/n$, \ for ReLU", font_size=22, color=GREY_B))
        cites.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.6, -2.9, 0])
        with self.voiceover(
            "The right size has a simple rule. A unit adds up n inputs, so to keep the sum the same size as each "
            "input, each weight's variance, its spread, should be one over n. That's Glorot and Bengio's rule, from "
            "2010, worked out for tanh, a smooth S-shaped bend. "
            "<bookmark mark='a'/> A ReLU throws away the negative half of its inputs, so for ReLU networks, double "
            "it: two over n. That's He initialization, and it's the steady line we just saw."
        ) as vo:
            self.play(Write(f1), FadeIn(sumv), FadeIn(cites[0]))
            self.play(FadeIn(why1), Create(base), FadeIn(hl),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03), run_time=1.6)
            vo.wait_until("a")
            self.play(Create(zero), neg.animate.set_fill(GREY_D, opacity=0.5), run_time=1.2)
            morph(self, f1, f2)
            self.play(FadeIn(why2), FadeIn(cites[1]))
        self.wait(0.3)
        self.clear_scene()
