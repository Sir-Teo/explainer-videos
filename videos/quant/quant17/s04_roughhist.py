from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import axes, data_range
from videos.quant.quant17.common import BAD, DELTA, GOOD, IV, NET, PART, REF, ask, illustration, load


def _t(day):
    d = date.fromisoformat(day)
    return d.year + (d.timetuple().tm_yday - 1) / (date(d.year + 1, 1, 1) - date(d.year, 1, 1)).days


class RoughHistory(VoiceoverScene):
    def construct(self):
        h = load("calib_hist")
        self.card()
        self.series(h)
        self.box(h)
        self.wall()
        self.fit(h)

    def card(self):
        c = chapter_card(5, r"Rough volatility, week by week", r"Is the market's $H$ stable, or a one-day accident?",
                         part=PART)
        with self.voiceover("Chapter five. Rough volatility, week by week."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def series(self, h):
        rows = h["rows"]
        t = np.array([_t(r["day"]) for r in rows])
        H = np.array([r["H"] for r in rows])
        rho = np.array([r["rho"] for r in rows])
        g1 = axes([2024, 2026], [0, 0.5], x_length=8.3, y_length=2.4, ylabel=r"Hurst exponent $H$",
                  xticks=[2024, 2025, 2026], xfmt=lambda v: f"{v:.0f}", yticks=[0, 0.25, 0.5], font_size=14)
        g2 = axes([2024, 2026], [-1, 0.7], x_length=8.3, y_length=2.0, ylabel=r"correlation $\rho$",
                  xticks=[2024, 2025, 2026], xfmt=lambda v: f"{v:.0f}", yticks=[-1, 0, 0.5], font_size=14)
        VGroup(g1, g2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_edge(LEFT, buff=0.7).shift(DOWN * 0.15)
        d1 = VGroup(*[Dot(g1.ax.c2p(a, b), radius=0.04, color=NET) for a, b in zip(t, H)])
        d2 = VGroup(*[Dot(g2.ax.c2p(a, b), radius=0.04, color=DELTA) for a, b in zip(t, rho)])
        half = DashedLine(g1.ax.c2p(2024, 0.02), g1.ax.c2p(2026, 0.02), stroke_color=BAD, stroke_width=1.5)
        floor_lab = VGroup(DashedLine(ORIGIN, RIGHT * 0.4, stroke_color=BAD, stroke_width=1.5),
                           label(r"the lowest $H$ the network was trained on (0.02)", font_size=15, color=BAD)).arrange(
            RIGHT, buff=0.12).next_to(g1, UP, buff=0.05).align_to(g1, RIGHT)
        at_floor = float(np.mean(H < 0.021))
        zero = DashedLine(g2.ax.c2p(2024, 0), g2.ax.c2p(2026, 0), stroke_color=GREY_C, stroke_width=1)
        q = h["H_q"]
        side = wrapped_label(rf"{len(rows)} weekly surfaces, each calibrated in about {h['seconds_median']:.0f} s. In "
                             rf"{100 * at_floor:.0f}\% of weeks $H$ sits at 0.02, the edge of the network's training box: "
                             r"a boundary fit can reflect model misspecification, quote noise, surrogate error or optimization. Selected MC checks compare fit errors, not identification. The fitted correlation can change sign", 3.6, 18, GREY_A).to_edge(RIGHT, buff=0.4)
        src = illustration(r"Deribit BTC options, Wednesdays 2024--2025 (Part 13's weekly surfaces), expiries to 200 days")
        with self.voiceover(
            f"The saved weekly option surfaces cover 2024 and 2025; these are descriptive calibrations, not forecasts. <bookmark mark='a'/> In {100 * at_floor:.0f} percent of fitted weeks, H is below 0.021, within 0.001 of the training floor. This is a boundary diagnostic. It can reflect the model, calendar effects, quotes, surrogate error or optimization; it does not prove that a latent market H is smaller. <bookmark mark='b'/> The fitted price–volatility correlation also changes. Neither parameter series is a direct observation of the underlying process, and a good surface fit need not identify parameters uniquely."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(src), Create(half), FadeIn(floor_lab))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in d1], lag_ratio=0.02, run_time=2.5), FadeIn(side))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(zero), LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.02, run_time=2))
        self.wait(0.4)
        self.clear_scene()

    def box(self, h):
        rows = h["rows"]
        H = np.array([r["H"] for r in rows])
        eta = np.array([r["eta"] for r in rows])
        g = axes([0, 0.52], [0, 4.2], x_length=6.4, y_length=4.6, xlabel=r"Hurst exponent $H$",
                 ylabel=r"vol of vol $\eta$", xticks=[0.02, 0.25, 0.5], yticks=[0.3, 2, 4], font_size=15
                 ).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lo, hi = ax.c2p(0.02, 0.3), ax.c2p(0.5, 4.0)
        slab = Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_color=GREY_B, stroke_width=1.5,
                         fill_color=GREY_D, fill_opacity=0.15).move_to((lo + hi) / 2)
        wall = Line(ax.c2p(0.02, 0.3), ax.c2p(0.02, 4.0), stroke_color=BAD, stroke_width=4)
        tr = ValueTracker(0)

        def make():
            k = int(tr.get_value())
            return VGroup(*[Dot(ax.c2p(H[i], eta[i]), radius=0.045, color=NET, fill_opacity=0.8)
                            for i in range(k)])
        pts = always_redraw(make)
        cnt = always_redraw(lambda: label(rf"week {int(tr.get_value())} of {len(rows)}", font_size=20,
                                          color=NET).next_to(g, UP, buff=0.1).align_to(g, LEFT))
        days = {r["day"]: i for i, r in enumerate(rows)}
        ck = h["checks"]
        gaps = [abs(c["mc_rmse"] - c["net_rmse"]) for c in ck]
        agree = sum(gp < 0.5 for gp in gaps)
        rings = VGroup(*[Circle(radius=0.12, stroke_color=GOOD if gp < 0.5 else BAD, stroke_width=3).move_to(
            ax.c2p(H[days[c["day"]]], eta[days[c["day"]]])) for c, gp in zip(ck, gaps)])
        at = int(np.sum(H < 0.021))
        side = VGroup(legend([(GREY_B, r"the training box"), (BAD, r"its wall, $H = 0.02$"),
                              (NET, r"one week's calibrated $(H, \eta)$"),
                              (GOOD, r"re-checked by fresh Monte Carlo: agrees within 0.5 vol points")], font_size=17),
                      wrapped_label(rf"{at} of {len(rows)} weeks have $H < 0.021$, near the 0.02 floor. {agree} of {len(ck)} Monte Carlo "
                                    r"checks agree with the network's fit to within half a vol point", 4.4, 19, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"Plot the fitted H and volatility-of-volatility parameters at their actual coordinates, without jitter. <bookmark mark='a'/> Of {len(rows)} weeks, {at} have H below 0.021. Clustering near the boundary alone cannot distinguish a constrained optimum, a flat objective, surrogate error or optimizer saturation. <bookmark mark='b'/> Selected weeks, every tenth retained fit, were repriced with forty thousand Monte Carlo paths. In {agree} of {len(ck)} checks, the network and finite simulation fit errors differ by less than half a vol point. That is a chosen descriptive threshold, not a confidence level or proof that either fit is globally optimal."
        ) as vo:
            self.play(FadeIn(g), FadeIn(slab), Create(wall), FadeIn(side[0]))
            vo.wait_until("a")
            self.add(pts, cnt)
            self.play(tr.animate.set_value(len(rows)), run_time=7, rate_func=linear)
            pts.clear_updaters()
            cnt.clear_updaters()
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r_) for r_ in rings], lag_ratio=0.2), FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def wall(self):
        rows = [cmath(r"\psi(T)", r"\sim", r"T^{H - 1/2}", font_size=44, colors={r"\psi(T)": IV}),
                cmath(r"L(\hat\vartheta)", r"\ge", r"\inf_{\vartheta\in\mathrm{box}}L(\vartheta)\ \ge\ \inf_{\vartheta\in\mathrm{admissible}}L(\vartheta)", font_size=34, colors={r"\ge": BAD})]
        whys = [why(r"under the model's small-time ATM-skew assumptions, a nonzero leading coefficient scales as $T^{H-1/2}$; finite-expiry fitted H is not a direct roughness measurement"),
                why(r"a finite optimizer returns a feasible point, not a certified global minimizer; widening the admissible box cannot increase its theoretical infimum. Fresh training and independent validation would be needed")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.4, buff=1.0, edge=6.9)
        with self.voiceover(
            "Under the rough model's small-time assumptions and a nonzero leading coefficient, the at-the-money skew scales as maturity to the power H minus one half. That asymptotic statement does not identify H from a finite set of noisy expiries. <bookmark mark='a'/> A fitted point has loss at least the box's infimum; the box's infimum is at least the infimum over a larger admissible domain. A finite optimizer does not certify either infimum. Boundary fits invite coverage, identification and optimization checks rather than a literal claim about the market's roughness."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"retrain with $H$ down to 0.005. Do the weekly $H$'s move, and does the fit improve?")
        with self.voiceover(
            'A wider box requires new labels and independent validation. A lower permitted H alone does not guarantee a more accurate pricing model; identifying that distinction is the exercise.'
        ):
            self.play(FadeIn(q))
        self.wait(0.4)
        self.clear_scene()

    def fit(self, h):
        rows = h["rows"]
        t = np.array([_t(r["day"]) for r in rows])
        rb = np.array([r["rmse"] for r in rows])
        he = np.array([r["heston_rmse"] for r in rows])
        top = data_range(rb, he, zero=True)[1]
        g = axes([2024, 2026], [0, top], x_length=8.4, y_length=4.2, ylabel=r"fit error (vol points)",
                 xticks=[2024, 2025, 2026], xfmt=lambda v: f"{v:.0f}", yticks=[round(v) for v in np.linspace(0, top, 4)[1:]],
                 font_size=15).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        def roll(x, w=5):
            return np.array([np.median(x[max(0, i - w // 2): i + w // 2 + 1]) for i in range(len(x))])
        l_he = VGroup(curve(ax, t, he, GREY_B, stroke_width=1).set_stroke(opacity=0.35),
                      curve(ax, t, roll(he), GREY_B, stroke_width=3.5))
        l_rb = VGroup(curve(ax, t, rb, NET, stroke_width=1).set_stroke(opacity=0.35),
                      curve(ax, t, roll(rb), NET, stroke_width=3.5))
        leg = legend([(GREY_B, r"Heston, refitted to the same quotes"), (NET, r"rough Bergomi, through the network"),
                      (GREY_D, r"bold: centred 5-week median (descriptive); faint: each week")], font_size=17)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        better = float(np.mean(rb < he))
        ck = h["checks"]
        gap = float(np.median([abs(c["mc_rmse"] - c["net_rmse"]) for c in ck]))
        side = wrapped_label(rf"Heston refitted to the same quotes each week, starting from Part 13's fit. Median errors "
                             rf"{h['rmse_median']:.2f} and {h['heston_rmse_median']:.2f}; rough Bergomi ahead in "
                             rf"{100 * better:.0f}\% of weeks, with the same number of parameters (five). On the Surface's "
                             rf"single day the gap was wide (Part 14); over two years it is close to a tie. Every tenth week "
                             rf"re-checked by Monte Carlo: the two errors differ by a median {gap:.2f} vol points", 4.2, 18,
                             GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"Compare descriptive fits to the same weekly quotes. Faint lines retain every saved error; bold lines are centred five-week medians, using neighbouring future weeks for display. <bookmark mark='a'/> The median errors are {h['rmse_median']:.2f} and {h['heston_rmse_median']:.2f} vol points; the rough surrogate has the smaller recorded error in {100 * better:.0f} percent of weeks. Equal parameter counts do not mean equal flexibility or optimization budgets. Heston is refitted directly, while most rough-model errors use the surrogate; selected Monte Carlo checks remain noisy. This is a finite in-sample calibration comparison, not a statistical tie, a forecast contest or proof of the underlying model."
        ) as vo:
            self.play(FadeIn(g), Create(l_he), FadeIn(leg[0]), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(Create(l_rb), FadeIn(leg[1]), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()
