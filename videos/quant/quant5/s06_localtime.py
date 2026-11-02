from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, load

K = 100.0


class LocalTime(VoiceoverScene):
    def construct(self):
        s = load("stoploss")
        self.card()
        self.tanaka()
        self.accumulate(s)
        self.scatter(s)

    def card(self):
        c = chapter_card(5, r"Local time: the paradox resolved", r"Where did the eight dollars go?", lit=(1990,),
                         part=PART)
        with self.voiceover("Chapter five. Local time, and the paradox resolved."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def tanaka(self):
        rows = [cmath(r"(S_T - K)^+", r"=", r"(S_0 - K)^+", r"+", r"\int_0^T \mathbf{1}_{\{S_t > K\}}\,dS_t", r"+",
                      r"\tfrac12 L_T^K", font_size=40,
                      colors={r"\int_0^T \mathbf{1}_{\{S_t > K\}}\,dS_t": DRIFT, r"\tfrac12 L_T^K": JUMP}),
                cmath(r"L_T^K", r"=", r"\lim_{\varepsilon \to 0} \frac{1}{2\varepsilon} \int_0^T \mathbf{1}_{\{|S_t - K| < \varepsilon\}}"
                      r"\,d\langle S\rangle_t", font_size=40, colors={r"L_T^K": JUMP}),
                cmath(r"\mathbb{E}_Q\big[\tfrac12 L_T^K\big]", r"=", r"C_0 - (S_0 - K)^+", font_size=40,
                      colors={r"\mathbb{E}_Q\big[\tfrac12 L_T^K\big]": JUMP})]
        whys = [why(r"Tanaka (1963): It\^o's lemma for the kink $x \mapsto (x - K)^+$; the stop-loss hedge earns the green "
                    r"term"),
                why(r"local time: how long the path lingered at $K$, measured in quadratic variation"),
                why(r"take expectations: the missing term is worth exactly the option's time value (Carr and Jarrow 1990)")]
        step = ladder(self, rows, whys, keep=3, top=2.5, x=-1.0, buff=1.0, edge=6.9)
        with self.voiceover(
            "Itô's lemma needs a smooth function, and a call's payoff has a kink at the strike. Hiroshi Tanaka worked "
            "out what happens at a kink. The payoff equals its starting value, plus the gains from holding one share "
            "whenever the stock is above the strike, which is exactly the stop-loss hedge, plus one more term. "
            "<bookmark mark='a'/> That term is the local time at the strike: how long the path spent within a hair "
            "of K, measured in quadratic variation, and rescaled by the hair's width. For a smooth path it would be "
            "zero. A Brownian path that touches K touches it infinitely often, and the local time is positive. "
            "<bookmark mark='b'/> Take expectations. The missing term is worth the call's price minus its intrinsic "
            "value: its time value. Peter Carr and Robert Jarrow published this resolution in 1990. The hedge is "
            "free only on paths that never come near the strike."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def accumulate(self, s):
        S = np.asarray(s["one"]["S"])
        L = np.asarray(s["one"]["half_L"])
        n = len(S) - 1
        t = np.linspace(0, 1, n + 1)
        g1 = axes([0, 1], [70, 140], x_length=8.0, y_length=2.6, ylabel=r"$S_t$", xticks=[], yticks=[80, 100, 120],
                  font_size=16)
        g2 = axes([0, 1], [0, max(L[-1] * 1.2, 1)], x_length=8.0, y_length=2.0, xlabel=r"time (years)",
                  ylabel=r"$\tfrac12 L_t^K$", xticks=[0, 0.5, 1], yticks=[0, round(L[-1])], font_size=16)
        VGroup(g1, g2).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        a1, a2 = g1.ax, g2.ax
        step = 4
        p = curve(a1, t[::step], S[::step], BM, stroke_width=2.5)
        band = Rectangle(width=a1.c2p(1, 0)[0] - a1.c2p(0, 0)[0], height=a1.c2p(0, 100.5)[1] - a1.c2p(0, 99.5)[1],
                         stroke_width=0, fill_color=JUMP, fill_opacity=0.6).move_to(a1.c2p(0.5, K))
        lt = curve(a2, t[::step], L[::step], JUMP, stroke_width=3)
        side = VGroup(
            wrapped_label(r"the clock of local time runs only while the path is inside the band around $K$", 4.4, 22,
                          GREY_A),
            MathTex(rf"\tfrac12 L_T^K = {L[-1]:.2f}", font_size=34, color=JUMP),
            wrapped_label(r"each crossing buys a share a little above $K$ and sells it a little below; on a Brownian path "
                          r"the crossings never end, and the little losses add up to this", 4.4, 22, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Watch it accumulate on one path. The red band is a narrow strip around the strike. "
            "<bookmark mark='a'/> Local time grows only while the price is inside the band, and stands still while "
            "it is away. <bookmark mark='b'/> In trading terms: each time the price crosses the strike, the hedger "
            "buys a share a little above it and sells a little below. A Brownian path crosses infinitely often near "
            "each crossing, so making the hedge finer doesn't help: the little losses add up to the local time."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(band), Create(p), run_time=2)
            vo.wait_until("a")
            self.play(Create(lt), FadeIn(side[0]), run_time=3)
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, s):
        sc = s["scatter"]
        e, L = np.asarray(sc["err"]), np.asarray(sc["half_L"])
        hi = float(np.percentile(np.concatenate([e, L]), 99))
        g = axes([0, hi], [0, hi], x_length=5.4, y_length=5.0, xlabel=r"$\tfrac12 L_T^K$ on the path",
                 ylabel=r"the stop-loss hedge's shortfall", xticks=[0, 10, 20], yticks=[0, 10, 20], font_size=18)
        g.to_edge(LEFT, buff=0.9).shift(DOWN * 0.1)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(min(a, hi), min(b, hi)), radius=0.03, color=JUMP, fill_opacity=0.6) for a, b in zip(L, e)])
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(hi, hi), color=GREY_B, stroke_width=2)
        rows = s["rows"]
        tab = VGroup(*[MathTex(rf"{r['n']:,}\text{{ trades: }} {r['mean_err']:.2f} \pm {r['sd_err']:.2f}".replace(",", "{,}"),
                               font_size=26, color=GREY_A) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        side = VGroup(
            label(r"average shortfall, by rebalancing frequency:", font_size=22, color=GREY_A), tab,
            MathTex(rf"\text{{the call's time value: }} {s['call']:.2f}", font_size=30, color=WHITE),
            MathTex(rf"\text{{correlation, path by path: }} {sc['corr']:.2f}", font_size=30, color=JUMP),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Now all four thousand paths. On each one, compare the stop-loss hedge's shortfall with half the local "
            "time at the strike. <bookmark mark='a'/> They line up, with a correlation of zero point nine seven. "
            "Paths that never came near the strike cost nothing to hedge; paths that lingered there cost a lot. "
            "<bookmark mark='b'/> On average the shortfall is the call's whole time value, about eight dollars, at "
            "every rebalancing frequency. Local time is real money. It is the reason a delta hedge is needed, and "
            "the reason options near the strike close to expiry, where the price lingers by the kink, are the "
            "hardest to hedge."
        ) as vo:
            self.play(FadeIn(g), Create(diag))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002, run_time=3))
            vo.wait_until("a")
            self.play(FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()
