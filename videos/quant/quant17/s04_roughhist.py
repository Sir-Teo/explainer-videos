from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, DELTA, GOOD, IV, NET, PART, REF, ask, illustration, load


def _t(day):
    d = date.fromisoformat(day)
    return d.year + (d.timetuple().tm_yday - 1) / 365


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
        g1 = axes([2024, 2026], [0, 0.5], x_length=9.0, y_length=2.4, ylabel=r"Hurst exponent $H$",
                  xticks=[2024, 2025, 2026], xfmt=lambda v: f"{v:.0f}", yticks=[0, 0.25, 0.5], font_size=14)
        g2 = axes([2024, 2026], [-1, 0.7], x_length=9.0, y_length=2.0, ylabel=r"correlation $\rho$",
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
                             r"the short-dated skew asks for something rougher still. Fresh Monte Carlo at those parameters "
                             r"confirms the fits; the weekend rhythm of Part 14 reads as extra roughness. The correlation "
                             r"changes sign with the market, as Heston's did in Part 13", 3.6, 18, GREY_A).to_edge(RIGHT, buff=0.4)
        src = illustration(r"Deribit BTC options, Wednesdays 2024--2025 (Part 13's weekly surfaces), expiries to 200 days")
        with self.voiceover(
            "Part fourteen measured roughness on one day. Is it a property of the market or an accident of that day? "
            "With the network, calibrating rough Bergomi to every weekly surface of 2024 and 2025 takes minutes. "
            f"<bookmark mark='a'/> Here is the Hurst exponent, week by week. In {100 * at_floor:.0f} percent of weeks "
            "it sits at 0.02, the lowest value the network was trained on: the market's short-dated skew asks for "
            "something rougher still. Fresh simulation at those parameters confirms the fits, so this is the market, "
            "not the network; and Part fourteen showed that bitcoin's quiet weekends read as extra roughness. A "
            "production version would widen the training box. This is exactly the check of chapter seventeen: know "
            "where your network has been. <bookmark mark='b'/> Below it, the correlation between price and volatility, which "
            "changes sign with the market, as it did for Heston in Part thirteen."
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
        rng = np.random.default_rng(1)
        jit = rng.uniform(0, 0.006, len(H))

        def make():
            k = int(tr.get_value())
            return VGroup(*[Dot(ax.c2p(H[i] + jit[i], eta[i]), radius=0.045, color=NET, fill_opacity=0.8)
                            for i in range(k)])
        pts = always_redraw(make)
        cnt = always_redraw(lambda: label(rf"week {int(tr.get_value())} of {len(rows)}", font_size=20,
                                          color=NET).next_to(g, UP, buff=0.1).align_to(g, LEFT))
        days = {r["day"]: i for i, r in enumerate(rows)}
        ck = h["checks"]
        gaps = [abs(c["mc_rmse"] - c["net_rmse"]) for c in ck]
        agree = sum(gp < 0.5 for gp in gaps)
        rings = VGroup(*[Circle(radius=0.12, stroke_color=GOOD if gp < 0.5 else BAD, stroke_width=3).move_to(
            ax.c2p(H[days[c["day"]]] + jit[days[c["day"]]], eta[days[c["day"]]])) for c, gp in zip(ck, gaps)])
        at = int(np.sum(H < 0.021))
        side = VGroup(legend([(GREY_B, r"the training box"), (BAD, r"its wall, $H = 0.02$"),
                              (NET, r"one week's calibrated $(H, \eta)$"),
                              (GOOD, r"re-checked by fresh Monte Carlo: agrees within 0.5 vol points")], font_size=17),
                      wrapped_label(rf"{at} of {len(rows)} weeks end on the wall. {agree} of {len(ck)} Monte Carlo "
                                    r"checks agree with the network's fit to within half a vol point", 4.4, 19, GREY_A)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Look at the same fits another way: each week as a point in the plane of the Hurst exponent and the "
            "volatility of volatility, inside the box the network was trained on. <bookmark mark='a'/> Week by week "
            f"they drop in, and they pile up against the left wall, H equal to 0.02: {at} of {len(rows)} weeks end "
            "there. This is the vanishing gradient of chapter four, seen in the data. <bookmark mark='b'/> Are those "
            "fits real? Every tenth week was re-priced by fresh Monte Carlo at the network's parameters, never touching "
            f"the network. {agree} of {len(ck)} agree to within half a vol point. The fits are honest fits; they are "
            "simply the best the box allows."
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
                cmath(r"\hat\vartheta", r"=", r"\arg\min_{\vartheta \in \text{box}} L(\vartheta)\ \ne\ "
                      r"\arg\min_{\vartheta} L(\vartheta)", font_size=40, colors={r"\hat\vartheta": BAD})]
        whys = [why(r"rough Bergomi's at-the-money skew explodes like $T^{H - 1/2}$ as the expiry shortens (Part 14); "
                    r"bitcoin's short-dated skew is steep, so the fit pushes $H$ toward zero"),
                why(r"at the wall the answer is the best fit inside the box, not the market's $H$; the Monte Carlo checks "
                    r"confirm a fit, they cannot reveal what lies outside. A wider box needs a new hour of simulation")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.4, buff=1.0, edge=6.9)
        with self.voiceover(
            "Why the wall? In rough Bergomi the at-the-money skew grows like the expiry to the power H minus one half "
            "as expiries shorten. Bitcoin's short-dated skew is steep, and the only way the model can steepen it is to "
            "lower H. <bookmark mark='a'/> So at the wall, the answer is the best fit inside the box, not the market's "
            "H. The Monte Carlo checks confirm that the fit is a fit; they cannot see what lies outside the box."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        q = ask(r"retrain with $H$ down to 0.005. Do the weekly $H$'s move, and does the fit improve?")
        with self.voiceover(
            "Would they move if the box were wider? That needs another hour of simulation, so it is left as a problem."
        ):
            self.play(FadeIn(q))
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
        def roll(x, w=5):
            return np.array([np.median(x[max(0, i - w // 2): i + w // 2 + 1]) for i in range(len(x))])
        l_he = VGroup(curve(ax, t, np.minimum(he, top), GREY_B, stroke_width=1).set_stroke(opacity=0.35),
                      curve(ax, t, np.minimum(roll(he), top), GREY_B, stroke_width=3.5))
        l_rb = VGroup(curve(ax, t, np.minimum(rb, top), NET, stroke_width=1).set_stroke(opacity=0.35),
                      curve(ax, t, np.minimum(roll(rb), top), NET, stroke_width=3.5))
        leg = legend([(GREY_B, r"Heston, refitted to the same quotes"), (NET, r"rough Bergomi, through the network"),
                      (GREY_D, r"bold: 5-week rolling median; faint: each week")], font_size=17)
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
            "And the fit, week by week, against Heston refitted to the same quotes. "
            f"<bookmark mark='a'/> The medians are {h['rmse_median']:.2f} and {h['heston_rmse_median']:.2f} vol points, "
            f"and rough Bergomi is ahead in {100 * better:.0f} percent of weeks. On the single day of Part fourteen the "
            "rough model won clearly; over two years, with the same number of parameters, it is close to a tie. One "
            "good day is not a model, and only a fast calibrator could show it."
        ) as vo:
            self.play(FadeIn(g), Create(l_he), FadeIn(leg[0]), FadeIn(leg[2]))
            vo.wait_until("a")
            self.play(Create(l_rb), FadeIn(leg[1]), FadeIn(side))
        self.wait(0.5)
        self.clear_scene()
