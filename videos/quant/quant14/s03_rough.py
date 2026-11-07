from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import axes, data_range, skew_range
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
        c = chapter_card(3, 'Measuring roughness in realized variance', r"How jagged is volatility, measured?", lit=(2018,),
                         part=PART)
        with self.voiceover("""Chapter three. Measuring roughness in realized variance."""):
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
        lo, hi = data_range(*[z for z, _, _ in rows])
        panels = VGroup()
        tr = ValueTracker(0.0)
        lines = VGroup()
        for z, col, txt in rows:
            g = axes([0, n], [lo, hi], x_length=10.6, y_length=1.55, xticks=[], yticks=[], font_size=14)
            t = label(txt, font_size=19, color=col).next_to(g, UP, buff=0.05).align_to(g, LEFT)
            panels.add(VGroup(g, t))
            lines.add(tracing(g.ax, x, z, tr, col, stroke_width=1.6))
        panels.arrange(DOWN, buff=0.35).move_to(DOWN * 0.1)
        src = real_data(rf"Binance BTCUSDT, 5-minute returns, {n} complete days, January 2024 -- November 2025")
        with self.voiceover(
            f"""Gatheral, Jaisson and Rosenbaum studied realized-volatility proxies computed from high-frequency returns. Here is the logarithm of Bitcoin's daily realized variance, measured from five-minute returns. <bookmark mark='a'/> Below it are a simulated fractional Brownian path with H of {float(keys[0]):.2f}, and a Brownian path, scaled to comparable daily variability. <bookmark mark='b'/> The low-H benchmark has negatively correlated increments. It is not a stationary mean-reverting process, and visual resemblance does not identify the latent variance law. Aggregation and measurement error will matter in the later debate."""
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
            "zeta of q, are proportional to q. The ratio is H. <bookmark mark='c'/> One caveat: we observe realized "
            "variance, a day's integrated variance with error. Chapter eleven shows how much that matters."
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
            f"""The estimator fits a log-moment slope for each q, then regresses those slopes on q with a free intercept. The resulting slope is the reported H estimate. <bookmark mark='a'/> On one fixed simulated path per chosen H, it returns {chk[1]['est']:.2f}, {chk[2]['est']:.2f} and {chk[3]['est']:.2f} for H of one tenth, three tenths and one half. For H of point zero five it returns {chk[0]['est']:.2f}. One path per value diagnoses a possible problem; it cannot establish statistical bias. Bitcoin's two era estimates are {r['H']:.2f} and {r18['H']:.2f}. They summarize finite-lag realized-variance proxies, not a direct observation of instantaneous variance or an option-pricing H."""
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
        allm = np.concatenate([np.log10(np.asarray(r["m"][f"{q}"])) for q in qs])
        ylo, yhi = float(np.floor(allm.min() * 10) / 10 - 0.05), float(np.ceil(allm.max() * 10) / 10 + 0.05)
        g = axes([0, np.log10(60)], [ylo, yhi], x_length=5.6, y_length=4.4, xlabel=r"lag $\Delta$ (days, log scale)",
                 ylabel=r"$\log_{10} m(q, \Delta)$", xticks=[np.log10(v) for v in (1, 3, 10, 30)],
                 xfmt=lambda u: f"{10 ** u:.0f}", log_x=True, yticks=[round(ylo + 0.05, 1), round((ylo + yhi) / 2, 1),
                                                                     round(yhi - 0.05, 1)], font_size=15)
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
        intercept = float(np.polyfit(qs, zeta, 1)[1])
        zrange = data_range(zeta, [intercept, 3.2 * r["H"] + intercept], zero=True)
        g2 = axes([0, 3.2], list(zrange), x_length=3.4, y_length=2.6, xlabel=r"$q$", ylabel=r"slope $\zeta_q$",
                  xticks=[0, 1, 2, 3], yticks=[0, 0.1, 0.2, 0.3], font_size=14)
        g2.next_to(g, RIGHT, buff=1.0).align_to(g, UP)
        zd = VGroup(*[Dot(g2.ax.c2p(q, z), radius=0.06, color=c) for q, z, c in zip(qs, zeta, cols)])
        zl = Line(g2.ax.c2p(0, intercept), g2.ax.c2p(3.2, 3.2 * r["H"] + intercept), stroke_color=WHITE, stroke_width=2)
        Hl = MathTex(rf"H = {r['H']:.2f}", font_size=34, color=ROUGH).next_to(g2, DOWN, buff=0.35)
        q = pause(r"If the $q = 2$ line had slope 1, what would $H$ be?", width=5.0, font_size=22).next_to(Hl, DOWN, buff=0.3)
        with self.voiceover(
            f"""For each lag from one to fifty days and each q, plot an empirical moment. <bookmark mark='a'/> Fit a log-log line to each color; deviations from a line remain part of the evidence. <bookmark mark='b'/> Regress the resulting slopes on q. The actual free-intercept line is shown, with slope {r['H']:.2f}. The ideal fractional Brownian benchmark instead has exactly zeta q equal to q H. <bookmark mark='c'/> Under that benchmark, if the q equals two slope were one, what would H be? <bookmark mark='d'/> One half. That one moment exponent alone does not establish Brownian motion."""
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
            answer = MathTex(r"H=\zeta_2/2=1/2", font_size=30, color=YELLOW).next_to(q, DOWN, buff=.18)
            self.play(Indicate(fits[3], color=YELLOW), Write(answer))
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
            wrapped_label('Low finite-lag exponents appear in both bitcoin eras and in the cited equity-index studies; this agreement does not identify latent volatility regularity.', 5.4, 20, GREY_A),
            wrapped_label(r"\textit{Rough Volatility} (SIAM 2023), chapter 1 is their paper; the estimator, its scaling "
                          r"law and the forecast of chapter 4 are all there", 5.4, 20, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            f"""Two era estimates: {r18['H']:.2f} and {r['H']:.2f}; after removing each full sample's weekday means, {r18['H_deseasonalized']:.2f} and {a['btc_deseasonalized']:.2f}. <bookmark mark='a'/> Low finite-lag exponents also appear in the cited equity-index studies. Agreement between proxies does not identify instantaneous variance regularity. Later chapters compare sampling, noise and mean-reversion explanations. Next: the rough predictor."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25))
            vo.wait_until("a")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()
