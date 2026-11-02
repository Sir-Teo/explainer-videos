from __future__ import annotations

from datetime import datetime, timezone

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant11.common import ALT, GAMMA, OPT, PART, SPOT, THETA, VEGA, load, real_data, tbar


def _year(ts):
    d = datetime.fromtimestamp(ts, tz=timezone.utc)
    return d.year + (d.timetuple().tm_yday - 1) / 365


class VRP(VoiceoverScene):
    def construct(self):
        e = load("edge")
        env = load("envelope")
        self.card()
        self.series(e)
        self.result(e, env)

    def card(self):
        c = chapter_card(3, r"Volatility trading, and a forecaster's edge", r"When is implied volatility too high?",
                         part=PART)
        with self.voiceover("Chapter three. Volatility trading, and a forecaster's edge."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def series(self, e):
        t = np.array([_year(x) for x in e["t"]])
        iv, fv, rv = (np.clip(np.asarray(e[k]), 0, 2.0) for k in ("iv", "fvol", "rv"))
        g = axes([2022, 2026], [0, 1.6], x_length=8.4, y_length=4.2, ylabel=r"bitcoin volatility, annualised",
                 xticks=[2022, 2023, 2024, 2025, 2026], xfmt=lambda u: f"{int(u)}", yticks=[0, 0.4, 0.8, 1.2, 1.6],
                 yfmt=lambda u: f"{100 * u:.0f}\\%", font_size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        li = curve(ax, t, iv, VEGA, stroke_width=3)
        lf = curve(ax, t, fv, ALT, stroke_width=2.5)
        lr = curve(ax, t, rv, GAMMA, stroke_width=1.5).set_stroke(opacity=0.7)
        leg = legend([(VEGA, r"implied: DVOL, the day it is sold"), (ALT, r"forecast: HAR on past realized variance"),
                      (GAMMA, r"realized over the next 30 days")], font_size=18).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        side = VGroup(
            wrapped_label(r"Part 10: selling a hedged one-month call every day earned the volatility risk premium, "
                          r"with a fat left tail", 3.8, 20, GREY_A),
            wrapped_label(r"Sinclair's rule: sell only when implied is above your own forecast of what will be "
                          r"realized", 3.8, 20, ALT),
            wrapped_label(r"the forecast is Part 7's HAR, refitted each week on the past only", 3.8, 20, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        src = real_data(r"Deribit DVOL and Binance BTCUSDT hourly, 2021--2025")
        with self.voiceover(
            "Part ten found that selling Bitcoin options and hedging them earned money on average: implied "
            "volatility tends to sit above the volatility that follows, the volatility risk premium, paid for "
            "carrying a fat left tail. <bookmark mark='a'/> A trader can try to do better. Euan Sinclair's rule is to "
            "sell only when implied volatility is above your own forecast. The forecast here is Part seven's HAR "
            "model, refitted every week on the past alone. <bookmark mark='b'/> And here is what was realized over "
            "each following month: mostly below implied, with spikes the forecast could not see coming."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(li), FadeIn(side[0]), FadeIn(leg[0]), run_time=2)
            vo.wait_until("a")
            self.play(Create(lf), FadeIn(leg[1]), FadeIn(side[1]), FadeIn(side[2]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lr), FadeIn(leg[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def result(self, e, env):
        g = axes([0, 2], [0, 2.5], x_length=4.6, y_length=4.0, ylabel=r"average P\&L of a month, per 100 of bitcoin",
                 xticks=[], yticks=[0, 0.5, 1, 1.5, 2, 2.5], font_size=17).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        ax = g.ax
        vals = [(e["nonoverlap_on"], e["se_on"], ALT, r"implied $>$ forecast", e["n_on"]),
                (e["nonoverlap_off"], e["se_off"], GREY_B, r"implied $\le$ forecast", e["n_off"])]
        objs = VGroup()
        for i, (m, se, c, lab, n) in enumerate(vals):
            b = tbar(ax, i + 0.5, m, c, width=0.55)
            err = Line(ax.c2p(i + 0.5, m - 2 * se), ax.c2p(i + 0.5, m + 2 * se), color=WHITE, stroke_width=2)
            txt = wrapped_label(lab + f" ({n} months)", 1.9, 18, GREY_A).next_to(ax.c2p(i + 0.5, 0), DOWN, buff=0.12)
            objs.add(VGroup(b, err, txt))
        diff = e["nonoverlap_on"] - e["nonoverlap_off"]
        se_d = float(np.hypot(e["se_on"], e["se_off"]))
        side = VGroup(
            label(r"selling only on the signal, separate months:", font_size=22, color=GREY_A),
            MathTex(rf"{e['nonoverlap_on']:.2f}\ \ \text{{vs}}\ \ {e['nonoverlap_off']:.2f}", font_size=34),
            MathTex(rf"\text{{difference }} {diff:.2f},\ \ t \approx {diff / se_d:.1f}", font_size=30, color=ALT),
            wrapped_label(rf"one test, registered before it was run: the trial counter reads {env['trials']}. A $t$ of "
                          r"two on a few dozen months is a reason to keep watching, not to lever up (Part 6)", 4.6, 20,
                          GREY_A),
            wrapped_label(r"the bars: two standard errors; months that overlap are dropped, so each is independent",
                          4.6, 19, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Did the forecast help? Take separate, non-overlapping months. When implied was above the forecast, the "
            f"hedged short call earned {e['nonoverlap_on']:.2f} per hundred of Bitcoin; when it was not, "
            f"{e['nonoverlap_off']:.2f}. <bookmark mark='a'/> The difference has a t-statistic of about "
            f"{diff / se_d:.1f}. The test was registered before it was run, so the trial counter reads "
            f"{env['trials']}. <bookmark mark='b'/> A t of two on a few dozen months is a reason to keep watching, "
            "not a reason to lever up: Part six's lesson about how little a few years of data can prove."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(o) for o in objs], lag_ratio=0.4), FadeIn(side[0]),
                      FadeIn(side[1]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[2]), FadeIn(side[4]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
