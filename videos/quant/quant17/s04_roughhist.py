from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, IV, NET, PART, REF, illustration, load


def _t(day):
    d = date.fromisoformat(day)
    return d.year + (d.timetuple().tm_yday - 1) / 365


class RoughHistory(VoiceoverScene):
    def construct(self):
        h = load("calib_hist")
        self.card()
        self.series(h)
        self.fit(h)

    def card(self):
        c = chapter_card(3, r"Rough volatility, week by week", r"Is the market's $H$ stable, or a one-day accident?",
                         part=PART)
        with self.voiceover("Chapter three. Rough volatility, week by week."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def series(self, h):
        rows = h["rows"]
        t = np.array([_t(r["day"]) for r in rows])
        H = np.array([r["H"] for r in rows])
        rho = np.array([r["rho"] for r in rows])
        g1 = axes([2024, 2026], [0, 0.5], x_length=9.0, y_length=2.4, ylabel=r"Hurst exponent $H$",
                  xticks=[2024, 2025, 2026], xfmt=lambda v: f"{v:.0f}", yticks=[0, 0.25, 0.5], font_size=14)
        g2 = axes([2024, 2026], [-1, 0.7], x_length=9.0, y_length=2.0, ylabel=r"correlation $\rho$",
                  xticks=[2024, 2025, 2026], xfmt=lambda v: f"{v:.0f}", yticks=[-1, 0, 0.5], font_size=14)
        VGroup(g1, g2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_edge(LEFT, buff=0.7).shift(DOWN * 0.15)
        d1 = VGroup(*[Dot(g1.ax.c2p(a, b), radius=0.04, color=NET) for a, b in zip(t, H)])
        d2 = VGroup(*[Dot(g2.ax.c2p(a, b), radius=0.04, color=DELTA) for a, b in zip(t, rho)])
        half = DashedLine(g1.ax.c2p(2024, 0.5), g1.ax.c2p(2026, 0.5), stroke_color=GREY_C, stroke_width=1.5)
        zero = DashedLine(g2.ax.c2p(2024, 0), g2.ax.c2p(2026, 0), stroke_color=GREY_C, stroke_width=1)
        q = h["H_q"]
        side = wrapped_label(rf"{len(rows)} weekly surfaces, each calibrated in about {h['seconds_median']:.0f} s. Median "
                             rf"$H$ = {h['H_median']:.2f}; half the weeks between {q[1]:.2f} and {q[2]:.2f}; "
                             rf"{100 * h['share_H_below_0_15']:.0f}\% below 0.15. The skew's correlation flips sign with the "
                             r"market, as Heston's did in Part 13", 3.6, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        src = illustration(r"Deribit BTC options, Wednesdays 2024--2025 (Part 13's weekly surfaces), expiries to 200 days")
        with self.voiceover(
            "Part fourteen measured roughness on one day. Is it a property of the market or an accident of that day? "
            "With the network, calibrating rough Bergomi to every weekly surface of 2024 and 2025 takes minutes. "
            f"<bookmark mark='a'/> Here is the Hurst exponent, week by week. Its median is {h['H_median']:.2f}, and in "
            f"{100 * h['share_H_below_0_15']:.0f} percent of weeks it is below 0.15: rough, far from the one half of "
            "a classical model. <bookmark mark='b'/> Below it, the correlation between price and volatility, which "
            "changes sign with the market, as it did for Heston in Part thirteen."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(src), Create(half))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in d1], lag_ratio=0.02, run_time=2.5), FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(zero), LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.02, run_time=2))
        self.wait(0.4)
        self.clear_scene()

    def fit(self, h):
        rows = h["rows"]
        t = np.array([_t(r["day"]) for r in rows])
        rb = np.array([r["rmse"] for r in rows])
        he = np.array([r["heston_rmse"] for r in rows])
        top = float(np.percentile(np.r_[rb, he], 97) * 1.15)
        g = axes([2024, 2026], [0, top], x_length=8.4, y_length=4.2, ylabel=r"fit error (vol points)",
                 xticks=[2024, 2025, 2026], xfmt=lambda v: f"{v:.0f}", yticks=[round(v) for v in np.linspace(0, top, 4)[1:]],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        l_he = curve(ax, t, np.minimum(he, top), GREY_B, stroke_width=2.5)
        l_rb = curve(ax, t, np.minimum(rb, top), NET, stroke_width=3)
        leg = legend([(GREY_B, r"Heston (Part 13)"), (NET, r"rough Bergomi, through the network")], font_size=17)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        better = float(np.mean(rb < he))
        ck = h["checks"]
        gap = float(np.median([abs(c["mc_rmse"] - c["net_rmse"]) for c in ck]))
        side = wrapped_label(rf"median error {h['rmse_median']:.2f} against Heston's {h['heston_rmse_median']:.2f}; rough "
                             rf"Bergomi fits better in {100 * better:.0f}\% of weeks, with the same number of parameters (five). Every tenth "
                             rf"week re-checked by Monte Carlo at the network's parameters: the two errors differ by a median "
                             rf"{gap:.2f} vol points", 4.2, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "And the fit, week by week, against Heston's weekly fits from Part thirteen. "
            f"<bookmark mark='a'/> Rough Bergomi's median error is {h['rmse_median']:.2f} vol points against Heston's "
            f"{h['heston_rmse_median']:.2f}, and it fits better in {100 * better:.0f} percent of weeks, with the same "
            "number of parameters. And the network is checked, not trusted: every tenth week is re-priced by fresh simulation "
            "at its parameters."
        ) as vo:
            self.play(FadeIn(g), Create(l_he), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(l_rb), FadeIn(leg[1]), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()
