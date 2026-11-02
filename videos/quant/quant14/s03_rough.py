from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, VAR, illustration, load, real_data


class Rough(VoiceoverScene):
    def construct(self):
        r = load("roughness")
        a = load("artefact")
        self.card()
        self.paths(r)
        self.scaling(r, a)

    def card(self):
        c = chapter_card(2, r"Volatility is rough", r"How jagged is volatility, measured?", lit=(2018,), part=PART)
        with self.voiceover("Chapter two. Volatility is rough."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def paths(self, r):
        lv = np.log(np.asarray(r["rv"]))
        n = len(lv)
        x = np.arange(n)
        ps = r["paths"]
        keys = sorted(ps, key=float)
        rows = [(lv, RV, r"bitcoin: log of daily realized variance (5-minute returns)"),
                (np.asarray(ps[keys[0]]), ROUGH, rf"fractional Brownian motion, $H = {float(keys[0]):.2f}$"),
                (np.asarray(ps[keys[1]]), VAR, r"Brownian motion, $H = 0.5$ (the same day-to-day variability)")]
        lo, hi = min(np.percentile(z, 0.5) for z, _, _ in rows), max(np.percentile(z, 99.5) for z, _, _ in rows)
        panels = VGroup()
        for z, col, txt in rows:
            g = axes([0, n], [lo, hi], x_length=10.6, y_length=1.55, xticks=[], yticks=[], font_size=14)
            line = curve(g.ax, x, np.clip(z, lo, hi), col, stroke_width=1.6)
            t = label(txt, font_size=19, color=col).next_to(g, UP, buff=0.05).align_to(g, LEFT)
            panels.add(VGroup(g, line, t))
        panels.arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        src = real_data(rf"Binance BTCUSDT, 5-minute returns, {n} complete days, January 2024 -- November 2025")
        with self.voiceover(
            "In 2014, Jim Gatheral, Thibault Jaisson and Mathieu Rosenbaum looked at volatility itself, measured every "
            "day from high-frequency returns, and found it rough. Here is Bitcoin's, for two years: the logarithm of "
            "each day's realized variance, from five-minute returns. <bookmark mark='a'/> Below it, a fractional "
            f"Brownian motion with H of {float(keys[0]):.2f}. <bookmark mark='b'/> And a Brownian motion, H one half, "
            "scaled to the same day-to-day variability. The Brownian path wanders in long slow swings. Bitcoin's "
            "volatility, like the rough path, is jagged at every scale and keeps returning to its level."
        ) as vo:
            self.play(FadeIn(panels[0][0]), FadeIn(panels[0][2]), Create(panels[0][1]), FadeIn(src), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(panels[1][0]), FadeIn(panels[1][2]), Create(panels[1][1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(panels[2][0]), FadeIn(panels[2][2]), Create(panels[2][1]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def scaling(self, r, a):
        lags = np.asarray(r["lags"], float)
        qs = np.asarray(r["qs"], float)
        zeta = np.asarray(r["zeta"])
        g = axes([0, np.log10(60)], [-1.6, 1.2], x_length=5.4, y_length=4.0, xlabel=r"lag $\Delta$ (days, log scale)",
                 ylabel=r"$\log_{10} m(q, \Delta)$", xticks=[np.log10(v) for v in (1, 3, 10, 30)],
                 xfmt=lambda u: f"{10 ** u:.0f}", log_x=True, yticks=[-1, 0, 1], font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        cols = [VAR, RV, IV, OPT, ROUGH]
        lines = VGroup()
        for q, c in zip(qs, cols):
            m = np.log10(np.asarray(r["m"][f"{q}"]))
            lines.add(VGroup(*[Dot(g.ax.c2p(np.log10(L), v), radius=0.045, color=c) for L, v in zip(lags, m)]),
                      )
        leg = legend([(c, rf"$q = {q:g}$") for q, c in zip(qs, cols)], font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        leg.arrange(RIGHT, buff=0.3).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        g2 = axes([0, 3.2], [0, 0.3], x_length=3.4, y_length=2.6, xlabel=r"$q$", ylabel=r"slope $\zeta_q$",
                  xticks=[0, 1, 2, 3], yticks=[0, 0.1, 0.2, 0.3], font_size=14)
        g2.next_to(g, RIGHT, buff=1.0).align_to(g, UP)
        zd = VGroup(*[Dot(g2.ax.c2p(q, z), radius=0.06, color=c) for q, z, c in zip(qs, zeta, cols)])
        zl = Line(g2.ax.c2p(0, 0), g2.ax.c2p(3.2, 3.2 * r["H"]), stroke_color=WHITE, stroke_width=2)
        chk = r["checks"]
        side = VGroup(
            MathTex(r"m(q, \Delta) = \overline{|\log\sigma^2_{t + \Delta} - \log\sigma^2_t|^q} \propto \Delta^{\zeta_q},\ "
                    r"\zeta_q = qH", font_size=26),
            MathTex(rf"H = {r['H']:.2f}\ \ \text{{(without the weekend pattern: }}{a['btc_deseasonalized']:.2f})",
                    font_size=28, color=ROUGH),
            label(r"the estimator on fBm with known $H$: " + ", ".join(rf"${c['H']:g} \to {c['est']:.2f}$" for c in chk),
                  font_size=17, color=GREY_A),
            wrapped_label(r"Gatheral, Jaisson and Rosenbaum (2018) found $H$ of order 0.1 across the equity indices "
                          r"they measured; bitcoin agrees", 6.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(g2, DOWN, buff=0.35).align_to(g2, LEFT)
        if side.get_right()[0] > 6.9:
            side.shift(LEFT * (side.get_right()[0] - 6.9))
        with self.voiceover(
            "Their measurement is simple. For each lag, take the average of the absolute change in log variance, raised "
            "to a power q. On log scales, each power gives a straight line in the lag. <bookmark mark='a'/> The slopes "
            "grow in proportion to q, which is the signature of a self-similar process, and the ratio is H. For "
            f"Bitcoin, H is {r['H']:.2f}. Bitcoin's calm weekends add a weekly pattern that pulls the estimate down; "
            f"remove it and H is {a['btc_deseasonalized']:.2f}. <bookmark mark='b'/> The same estimator, run on "
            "fractional Brownian motions with known H, recovers a tenth, three-tenths and a half closely, and reads "
            "a true H of 0.05 as about 0.01: for the very roughest paths it is biased low. That is a check on the "
            "tool, not on the world. Gatheral, Jaisson and Rosenbaum found H of about a tenth across the equity indices they "
            "measured. "
            "Bitcoin agrees."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.2, run_time=2.5),
                      FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(g2), LaggedStart(*[FadeIn(d) for d in zd], lag_ratio=0.2), Create(zl), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
