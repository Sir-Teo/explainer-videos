from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, load, real_data


def _yr(days):
    return 1970 + np.asarray(days, float) / 365.2425


class PDV(VoiceoverScene):
    def construct(self):
        p = load("pdv")
        self.card()
        self.model(p)
        self.fit(p)

    def card(self):
        c = chapter_card(8, r"Volatility is (mostly) path-dependent", r"How much of volatility is just the past?",
                         part=PART)
        with self.voiceover("Chapter eight. Volatility is mostly path-dependent."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def model(self, p):
        rows = [cmath(r"\sigma_t", r"=", r"\beta_0 + \beta_1 R_{1,t} + \beta_2\sqrt{R_{2,t}}", font_size=40,
                      colors={r"\sigma_t": IV}),
                cmath(r"R_{1,t}", r"=", r"\sum_{t_i \le t} K_1(t - t_i)\,r_{t_i},\qquad R_{2,t} = \sum_{t_i \le t} "
                      r"K_2(t - t_i)\,r_{t_i}^2", font_size=34, colors={r"R_{1,t}": OPT}),
                cmath(r"K(\tau)", r"\propto", r"(\tau + \delta)^{-\alpha}", font_size=38, colors={r"K(\tau)": VAR})]
        whys = [why(r"Guyon and Lekeufack (2023): implied volatility as a function of the price path alone, no hidden "
                    r"random factor"),
                why(r"a trend (weighted past returns) and an activity (weighted past squared returns)"),
                why(r"time-shifted power-law kernels: memory that fades slowly, the same shape as rough volatility's "
                    r"kernel")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.0, buff=0.85, edge=6.9)
        with self.voiceover(
            "There is another way to read the same facts. In 2023 Julien Guyon and Jordan Lekeufack asked how much of "
            "volatility is simply a function of the path the price has already taken. Their answer: most of it. "
            "Write implied volatility as a constant, plus a trend term, plus the square root of an activity term. "
            "<bookmark mark='a'/> The trend is a weighted sum of past returns; the activity, of past squared returns. "
            "<bookmark mark='b'/> The weights fade with time like a shifted power law, slowly, the same shape as a "
            "rough kernel. For the S&P 500 and the VIX, they found this explains most of the variation in implied "
            "volatility, and that a model built on it fits options on both."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def fit(self, p):
        t = _yr(p["days"])
        vol = np.asarray(p["vol"], float)
        pred = np.asarray(p["pred"], float)
        base = np.asarray(p["base"], float)
        split = _yr(p["split_day"])
        g = axes([2021.25, 2026], [0.2, 1.4], x_length=8.0, y_length=4.2, ylabel=r"bitcoin's 30-day implied volatility",
                 xticks=[2022, 2023, 2024, 2025], yticks=[0.4, 0.8, 1.2], yfmt=lambda u: f"{100 * u:.0f}\\%",
                 font_size=16).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        ok = np.isfinite(vol)
        l_v = curve(ax, t[ok], np.clip(vol[ok], 0.2, 1.4), IV, stroke_width=2.4)
        l_p = curve(ax, t[ok], np.clip(pred[ok], 0.2, 1.4), MODEL_COL["PDV"], stroke_width=2.0)
        l_b = curve(ax, t[ok], np.clip(base[ok], 0.2, 1.4), GREY_B, stroke_width=1.6)
        cut = DashedLine(ax.c2p(split, 0.2), ax.c2p(split, 1.4), stroke_color=GREY_A, stroke_width=1.5)
        cl = label(r"fitted up to here; after it, out of sample", font_size=16, color=GREY_A).next_to(ax.c2p(split, 1.4),
                                                                                                    RIGHT, buff=0.1)
        leg = legend([(IV, r"DVOL"), (MODEL_COL["PDV"], r"path-dependent volatility, from bitcoin's returns only"),
                      (GREY_B, r"baseline: a line in the past 30 days' realized vol")], font_size=16).next_to(
            g, UP, buff=0.1).align_to(g, LEFT)
        b = p["beta"]
        side = VGroup(
            MathTex(rf"R^2:\ {p['r2_train']:.2f}\ \text{{(in)}},\ \ {p['r2_test']:.2f}\ \text{{(out)}}", font_size=28,
                    color=MODEL_COL["PDV"]),
            MathTex(rf"\text{{baseline: }} {p['r2_base_train']:.2f},\ \ {p['r2_base_test']:.2f}", font_size=26, color=GREY_B),
            MathTex(rf"\beta_2 = {b[2]:.2f}", font_size=28, color=WHITE),
            wrapped_label(rf"activity does almost all the work: its term moves implied vol by {100 * p['contrib']['activity']:.0f} "
                          rf"points (one s.d.), the trend by {100 * p['contrib']['trend']:.1f}. For the S\&P 500 the trend "
                          r"term matters (falls raise volatility); bitcoin's implied vol cares about how much it moved, "
                          r"hardly which way", 3.9, 18, GREY_A),
            wrapped_label(rf"activity's memory: a power law shifted by {365 * p['delta2']:.0f} days, exponent "
                          rf"{p['alpha2']:.2f}", 3.9, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        src = real_data(r"Deribit DVOL daily; Binance BTCUSDT daily returns since 2018 (kernels need 1{,}000 days of past)")
        with self.voiceover(
            "Fit it to Bitcoin. The inputs are only Bitcoin's own daily returns, going back to 2018; the target is "
            "DVOL, the market's thirty-day implied volatility. The model is fitted on 2021 to 2023, and then frozen. "
            f"<bookmark mark='a'/> In sample it explains {100 * p['r2_train']:.0f} percent of DVOL's variation. "
            f"<bookmark mark='b'/> Out of sample, in 2024 and 2025, {100 * p['r2_test']:.0f} percent, where a simple "
            "line in the last month's realized volatility, fitted the same way, does worse than a constant. "
            "<bookmark mark='c'/> And look at what does the work. In the S&P 500 the trend term matters: falls raise "
            "volatility. In Bitcoin it barely registers. Bitcoin's implied volatility cares how much the price has "
            "moved, with a memory that fades like a power law, and hardly which way."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), Create(l_v), run_time=2.5)
            vo.wait_until("a")
            self.play(Create(cut), FadeIn(cl), Create(l_p), FadeIn(leg[1]), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(l_b), FadeIn(leg[2]), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()
