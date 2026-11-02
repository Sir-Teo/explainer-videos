from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, OPT, PART, ROUGH, RV, VAR, illustration, load, pause, real_data


class Rough(VoiceoverScene):
    def construct(self):
        r = load("roughness")
        a = load("artefact")
        r18 = load("roughness_2018")
        self.card()
        self.paths(r)
        self.derive()
        self.lab(r, a, r18)
        self.scaling(r, a)
        self.eras(r, a, r18)

    def card(self):
        c = chapter_card(3, r"Volatility is rough, re-measured", r"How jagged is volatility, measured?", lit=(2018,),
                         part=PART)
        with self.voiceover("Chapter three. Volatility is rough, re-measured."):
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
        tr = ValueTracker(0.0)
        lines = VGroup()
        for z, col, txt in rows:
            g = axes([0, n], [lo, hi], x_length=10.6, y_length=1.55, xticks=[], yticks=[], font_size=14)
            t = label(txt, font_size=19, color=col).next_to(g, UP, buff=0.05).align_to(g, LEFT)
            panels.add(VGroup(g, t))
            lines.add(tracing(g.ax, x, np.clip(z, lo, hi), tr, col, stroke_width=1.6))
        panels.arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        src = real_data(rf"Binance BTCUSDT, 5-minute returns, {n} complete days, January 2024 -- November 2025")
        with self.voiceover(
            "In 2014, Jim Gatheral, Thibault Jaisson and Mathieu Rosenbaum looked at volatility itself, measured every "
            "day from high-frequency returns, and found it rough. Here is Bitcoin's, for two years: the logarithm of "
            "each day's realized variance, from five-minute returns, drawn day by day. <bookmark mark='a'/> Below "
            f"it, a fractional Brownian motion with H of {float(keys[0]):.2f}, and a Brownian motion, H one half, "
            "scaled to the same day-to-day variability. <bookmark mark='b'/> The Brownian path wanders in long slow "
            "swings. Bitcoin's volatility, like the rough path, is jagged at every scale and keeps returning to its "
            "level."
        ) as vo:
            self.play(FadeIn(panels), FadeIn(src), FadeIn(lines))
            self.play(tr.animate.set_value(n - 1), run_time=max(vo.remaining(0.0) - 1.0, 4), rate_func=linear)
            vo.wait_until("b")
        lines.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        rows = [cmath(r"\log\sigma^2_{t + \Delta} - \log\sigma^2_t", r"\overset{d}{=}", r"\nu\,\Delta^H Z", font_size=38,
                      colors={r"\log\sigma^2_{t + \Delta} - \log\sigma^2_t": RV}),
                cmath(r"m(q, \Delta)", r"=", r"\mathbb{E}\big|\log\sigma^2_{t + \Delta} - \log\sigma^2_t\big|^q = \nu^q\,"
                      r"\mathbb{E}|Z|^q\,\Delta^{qH}", font_size=36, colors={r"m(q, \Delta)": IV}),
                cmath(r"\log m(q, \Delta)", r"=", r"\zeta_q\log\Delta + c_q,\qquad \zeta_q = qH", font_size=38,
                      colors={r"\log m(q, \Delta)": IV}),
                cmath(r"\widehat{\sigma^2_t}", r"=", r"\sum_i r_{t, i}^2 = \int_t^{t + 1}\sigma^2_s\,ds + \varepsilon_t",
                      font_size=38, colors={r"\widehat{\sigma^2_t}": RV})]
        whys = [why(r"if log variance is a fractional Brownian motion: stationary, self-similar increments"),
                why(r"take the $q$-th absolute moment: the scale pulls out as $\Delta^{qH}$"),
                why(r"on log scales, a straight line in the lag for every $q$; the slopes are linear in $q$ (monofractal)"),
                why(r"but we observe realized variance: the integral over a day, plus measurement error (chapter 11)")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-1.2, buff=0.75, edge=6.9)
        with self.voiceover(
            "Their measurement rests on one property. If log variance behaves like a fractional Brownian motion, "
            "its change over a lag delta has the same distribution as a constant times delta to the power H times a "
            "standard normal. <bookmark mark='a'/> Take the q-th absolute moment, and the scale pulls out: delta to "
            "the q H. <bookmark mark='b'/> On log scales, a straight line in the lag for every q, and the slopes, "
            "zeta of q, are proportional to q. The ratio is H. <bookmark mark='c'/> One caveat to carry forward. We "
            "never observe spot variance. We observe realized variance: the sum of squared five-minute returns, an "
            "estimate of the variance integrated over a day, with error. Chapter eleven shows how much that matters."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, r, a, r18):
        card = lab_card(r"the roughness estimator", [
            "def log_rv_scaling(log_v, lags=(1, 2, 3, 4, 5, 7, 10, 15, 20, 30, 50),",
            "                   qs=(0.5, 1.0, 1.5, 2.0, 3.0)):",
            "    x = np.asarray(log_v, float)",
            "    zeta = []",
            "    for q in qs:",
            "        m = np.array([np.mean(np.abs(x[L:] - x[:-L]) ** q)",
            "                      for L in lags])",
            "        zeta.append(np.polyfit(np.log(lags), np.log(m), 1)[0])",
            "    H = np.polyfit(np.asarray(qs), np.array(zeta), 1)[0]",
            "    return {\"zeta\": zeta, \"H\": H}",
        ], source="explainer/quant/house/rough.py", width=8.4).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.4)
        chk = r["checks"]
        outs = ["fBm with known H:  " + "   ".join(f"{c['H']:g} -> {c['est']:.2f}" for c in chk),
                f"bitcoin 2024-25:   H = {r['H']:.2f}   (weekdays evened out: {a['btc_deseasonalized']:.2f})",
                f"bitcoin 2018-20:   H = {r18['H']:.2f}   (weekdays evened out: {r18['H_deseasonalized']:.2f})"]
        with self.voiceover(
            "Here is the House's estimator, all of it. For each power q, average the absolute change in log "
            "variance over each lag, raised to q, and fit a line on log scales: that is zeta of q. Then regress the "
            "zetas on q: the slope is H. <bookmark mark='a'/> Run it. First on fractional Brownian motions whose H "
            f"we chose: it reads a tenth as {chk[1]['est']:.2f}, three-tenths as {chk[2]['est']:.2f}, a half as "
            f"{chk[3]['est']:.2f}, but the very roughest, 0.05, as {chk[0]['est']:.2f}: biased low at the extreme. "
            f"Then on Bitcoin: {r['H']:.2f} for 2024 and 2025, and {r18['H']:.2f} for 2018 to 2020, from one-minute "
            "bars resampled to five minutes. Two eras, two very different markets, both rough."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=4)
        self.wait(0.5)
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
        dots, fits = VGroup(), VGroup()
        for q, c in zip(qs, cols):
            m = np.log10(np.asarray(r["m"][f"{q}"]))
            dots.add(VGroup(*[Dot(g.ax.c2p(np.log10(L), v), radius=0.045, color=c) for L, v in zip(lags, m)]))
            b = np.polyfit(np.log10(lags), m, 1)
            fits.add(Line(g.ax.c2p(0, b[1]), g.ax.c2p(np.log10(60), b[1] + b[0] * np.log10(60)), stroke_color=c,
                          stroke_width=2))
        leg = legend([(c, rf"$q = {q:g}$") for q, c in zip(qs, cols)], font_size=16)
        leg.arrange(RIGHT, buff=0.3).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        g2 = axes([0, 3.2], [0, 0.3], x_length=3.4, y_length=2.6, xlabel=r"$q$", ylabel=r"slope $\zeta_q$",
                  xticks=[0, 1, 2, 3], yticks=[0, 0.1, 0.2, 0.3], font_size=14)
        g2.next_to(g, RIGHT, buff=1.0).align_to(g, UP)
        zd = VGroup(*[Dot(g2.ax.c2p(q, z), radius=0.06, color=c) for q, z, c in zip(qs, zeta, cols)])
        zl = Line(g2.ax.c2p(0, 0), g2.ax.c2p(3.2, 3.2 * r["H"]), stroke_color=WHITE, stroke_width=2)
        Hl = MathTex(rf"H = {r['H']:.2f}", font_size=34, color=ROUGH).next_to(g2, DOWN, buff=0.35)
        q = pause(r"If the $q = 2$ line had slope 1, what would $H$ be?", width=5.0, font_size=22).next_to(Hl, DOWN, buff=0.3)
        with self.voiceover(
            "Watch the measurement build on Bitcoin. For each lag, from one day to fifty, and each power q, one "
            "point. <bookmark mark='a'/> Fit a line through each colour. They are straight, to the eye at least: "
            "a scaling law. <bookmark mark='b'/> Now plot the slopes against q. They line up through the origin, "
            f"and the slope of that line is H: {r['H']:.2f}. <bookmark mark='c'/> Pause and predict: if the q equals "
            "two line had slope one, what would H be? <bookmark mark='d'/> One half: the second moment of a "
            "Brownian increment grows linearly in the lag. Bitcoin's grows like the lag to the power "
            f"{2 * r['H']:.2f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            self.play(LaggedStart(*[LaggedStart(*[FadeIn(d, scale=0.5) for d in row], lag_ratio=0.15) for row in dots],
                                  lag_ratio=0.3, run_time=4))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromCenter(f) for f in fits], lag_ratio=0.2, run_time=2))
            vo.wait_until("b")
            self.play(FadeIn(g2), LaggedStart(*[TransformFromCopy(fits[i], zd[i]) for i in range(len(zd))],
                                              lag_ratio=0.3, run_time=2.5))
            self.play(Create(zl), FadeIn(Hl))
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(Indicate(fits[3], color=YELLOW))
        self.wait(0.4)
        self.clear_scene()

    def eras(self, r, a, r18):
        items = [(r"2018--2020", r18["H"], r18["H_deseasonalized"]), (r"2024--2025", r["H"], a["btc_deseasonalized"])]
        g = axes([-0.6, 1.6], [0, 0.2], x_length=5.0, y_length=3.6, xticks=[0, 1],
                 xfmt=lambda u: [r"2018\text{--}2020", r"2024\text{--}2025"][int(round(u))], ylabel=r"estimated $H$",
                 yticks=[0, 0.05, 0.1, 0.15, 0.2], font_size=16).to_edge(LEFT, buff=0.9).shift(DOWN * 0.2)
        bars = VGroup()
        for i, (_, h, hd) in enumerate(items):
            for j, (v, c) in enumerate(((h, RV), (hd, ROUGH))):
                bars.add(Rectangle(width=0.45, height=max(g.ax.c2p(0, v)[1] - g.ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                                   fill_color=c, fill_opacity=0.85).move_to(g.ax.c2p(i - 0.13 + 0.26 * j, v / 2)))
        leg = legend([(RV, r"as measured"), (ROUGH, r"weekday pattern removed")], font_size=17).next_to(g, UP, buff=0.15)
        side = VGroup(
            wrapped_label(r"Gatheral, Jaisson and Rosenbaum (2018) found $H$ of order 0.1 for the S\&P 500 and other "
                          r"indices, from realized variance; bitcoin, in two eras, agrees", 5.4, 20, GREY_A),
            wrapped_label(r"\textit{Rough Volatility} (SIAM 2023), chapter 1 is their paper; the estimator, its scaling "
                          r"law and the forecast of chapter 4 are all there", 5.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Two eras side by side. In 2018 to 2020, a younger and wilder market, H comes out at "
            f"{r18['H']:.2f}; in 2024 and 2025, {r['H']:.2f}. Bitcoin's calm weekends add a weekly rhythm that pulls "
            f"the estimate down; remove each weekday's average, and the two eras read {r18['H_deseasonalized']:.2f} "
            f"and {a['btc_deseasonalized']:.2f}. <bookmark mark='a'/> Gatheral, Jaisson and Rosenbaum found H of "
            "order a tenth for the S&P 500 and other equity indices. Bitcoin agrees. Whether the estimator can be "
            "trusted is another matter, and chapter eleven will try hard to fool it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25))
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
