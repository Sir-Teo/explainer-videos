from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant8.common import ALT, KELLY, OVER, PART, UNDER, VALUE, illustration, load


class Stopping(VoiceoverScene):
    def construct(self):
        self.card()
        self.secretary(load("secretary"))
        self.snell(load("american"))

    def card(self):
        c = chapter_card(7, r"Optimal stopping", r"When should you stop and take what you have?", part=PART)
        with self.voiceover("Chapter seven. Optimal stopping."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def secretary(self, q):
        k = np.asarray(q["k"])
        g = axes([0, 100], [0, 0.45], x_length=6.6, y_length=4.2, xlabel=r"candidates rejected before choosing",
                 ylabel=r"chance of choosing the best of 100", xticks=[0, 20, 37, 60, 80, 100],
                 yticks=[0, 0.1, 0.2, 0.3, 0.4], yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        exact = curve(ax, k, np.asarray(q["exact"]), VALUE, stroke_width=4)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.045, color=WHITE) for x, y in zip(k[::2], np.asarray(q["sim"])[::2])])
        top = DashedLine(ax.c2p(q["best_k"], 0), ax.c2p(q["best_k"], q["best_p"]), color=KELLY, stroke_width=2)
        tl = MathTex(rf"k = {q['best_k']}:\ {100 * q['best_p']:.1f}\%", font_size=26, color=KELLY).next_to(ax.c2p(q["best_k"], q["best_p"]),
                                                                                         UP, buff=0.1)
        side = VGroup(
            wrapped_label(r"100 candidates arrive in random order; you can rank each against those seen, must accept or "
                          r"reject on the spot, and win only with the best", 4.4, 21, GREY_A),
            wrapped_label(r"rule: reject the first $k$, then take the first who beats them all; the best $k \approx "
                          r"n/e$ wins with probability $\to 1/e \approx 37\%$, however large $n$", 4.4, 21, VALUE),
            wrapped_label(r"line: exact; dots: 20{,}000 simulated searches each. Dynkin (1963) and others; the "
                          r"general theory is the Snell envelope", 4.4, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Some decisions are not how much, but when. The classic is the secretary problem. A hundred candidates "
            "arrive in random order. You can rank each one against those you have already seen, but you must accept "
            "or reject on the spot, and you win only if you pick the very best. <bookmark mark='a'/> The best rule "
            "is to reject a fixed number, then take the first candidate better than all of them. Reject about "
            f"{q['best_k']}, a hundred divided by e, and you choose the best with a probability of "
            f"{100 * q['best_p']:.0f} percent: one over e, however many candidates there are. The white dots are "
            "simulated searches; the line is exact."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(exact), LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.05), run_time=2.5)
            self.play(Create(top), FadeIn(tl), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def snell(self, a):
        t = np.asarray(a["t"])
        b = np.asarray(a["boundary"])
        ok = np.isfinite(b)
        # the tree's boundary is a staircase of node spots; a running mean over 25 steps draws the curve it samples
        bs = b.copy()
        idx = np.where(ok)[0]
        bs[idx] = np.convolve(np.pad(b[idx], 12, mode="edge"), np.ones(25) / 25, mode="valid")
        b = bs
        rows = [cmath(r"U_n", r"=", r"\max\big(\,g(S_n),\ \mathbb{E}[\,U_{n+1} \mid \mathcal{F}_n]\,\big)", font_size=34,
                      colors={r"U_n": VALUE})]
        whys = [why(r"the Snell envelope (1952): the value of the right to stop is the larger of stopping now and "
                    r"the value of waiting; stop the first time they are equal")]
        step = ladder(self, rows, whys, keep=1, top=3.0, x=0, buff=0.7, edge=6.9)
        g = axes([0, 1], [60, 100], x_length=6.6, y_length=3.6, xlabel=r"time (years)", ylabel=r"stock price",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[60, 70, 80, 90, 100], font_size=17)
        g.to_edge(LEFT, buff=0.7).to_edge(DOWN, buff=0.6)
        ax = g.ax
        bl = curve(ax, t[ok], b[ok], OVER, stroke_width=4)
        region = Polygon(*[ax.c2p(x, 60) for x in (t[ok][0],)], *[ax.c2p(x, y) for x, y in zip(t[ok], b[ok])],
                         ax.c2p(t[ok][-1], 60), stroke_width=0, fill_color=OVER, fill_opacity=0.18)
        kl = DashedLine(ax.c2p(0, 100), ax.c2p(1, 100), color=GREY_B, stroke_width=1.5)
        ex = label(r"exercise", font_size=22, color=OVER).move_to(ax.c2p(0.55, 66))
        wt = label(r"wait", font_size=22, color=UNDER).move_to(ax.c2p(0.3, 92))
        side = VGroup(
            label(r"an American put: $K = 100$, $\sigma = 30\%$, $r = 5\%$, one year", font_size=21, color=GREY_A),
            MathTex(rf"\text{{American: }} {a['american']:.2f}", font_size=30, color=VALUE),
            MathTex(rf"\text{{European: }} {a['european']:.2f}", font_size=30, color=GREY_B),
            wrapped_label(r"the boundary rises to the strike at expiry; the early-exercise premium is the value of "
                          r"stopping at the right time. Part 10 prices it; Part 16 does it by simulation "
                          r"(Longstaff and Schwartz 2001)", 4.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4).to_edge(DOWN, buff=0.6)
        src = illustration(r"a 500-step CRR tree (the House's \texttt{trees})")
        with self.voiceover(
            "The general theory is the Snell envelope, from 1952. At each moment, the value of the right to stop is "
            "the larger of what you get by stopping now and the expected value of waiting; you stop the first time "
            "they are equal. <bookmark mark='a'/> The most important example in finance is an American put, the "
            "right to sell a stock at a hundred at any time within a year. Below the red boundary, exercising now "
            "beats waiting; above it, wait. The boundary rises toward the strike as expiry nears. "
            f"<bookmark mark='b'/> The right to choose when is worth {a['american'] - a['european']:.2f} here: the "
            f"American put costs {a['american']:.2f}, the European {a['european']:.2f}. Part ten prices it on a tree; "
            "Part sixteen does it by simulation."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(src), Create(kl), FadeIn(side[0]))
            self.play(Create(bl), FadeIn(region), FadeIn(ex), FadeIn(wt), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
