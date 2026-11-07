from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant14.common import axes, data_range, skew_range
from videos.quant.quant14.common import (BAD, IV, MODEL_COL, OPT, PART, ROUGH, RV, VAR, load, loglog_skew_axes, pause,
                                         real_data)


class Fact(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("skew")
        w = load("skew_weekly")
        self.card()
        self.loom(w)
        self.law(s, w)
        self.definitions(w)

    def card(self):
        c = chapter_card(1, 'Finite-maturity skew magnitudes', r"How fast does the skew grow as expiry nears?", part=PART)
        with self.voiceover("""Chapter one. Finite-maturity skew magnitudes."""):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def loom(self, w):
        weeks = w["weeks"]
        nw = len(weeks)
        lo_T = np.log10(min(min(x["T"]) for x in weeks))
        yr = skew_range(*[x["skew"] for x in weeks],
                        *[x["c"] * np.asarray(x["T"]) ** (-x["a"]) for x in weeks])
        ax = ThreeDAxes(x_range=[lo_T, 0, 1], y_range=[0, nw, 20], z_range=[*yr, 1], x_length=6.4,
                        y_length=6.0, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.3)
        crisis = next((i for i, x in enumerate(weeks) if x["day"] == "2024-08-07"), None)
        rows, fits = VGroup(), VGroup()
        for i, x in enumerate(weeks):
            T = np.asarray(x["T"])
            y = np.log10(np.abs(np.asarray(x["skew"])))
            col = BAD if i == crisis else interpolate_color(ManimColor(IV), ManimColor(OPT), i / max(nw - 1, 1))
            pts = [ax.c2p(np.log10(t), i, v) for t, v in zip(T, y)]
            rows.add(VMobject(stroke_color=col, stroke_width=2.4 if i == crisis else 1.4).set_points_as_corners(pts))
            Tf = np.array([max(T.min(), 2 / 365), T.max()])
            yf = np.log10(x["c"] * Tf ** (-x["a"]))
            fits.add(Line(ax.c2p(np.log10(Tf[0]), i, yf[0]), ax.c2p(np.log10(Tf[1]), i, yf[1]),
                          stroke_color=WHITE if i != crisis else BAD, stroke_width=1.0, stroke_opacity=0.6))
        hint = VGroup(label(r"left to right: time to expiry, 2 days to 1 year (log)", font_size=20, color=GREY_A),
                      label(r"front to back: the week, January 2024 to December 2025", font_size=20, color=GREY_A),
                      label(r"height: the at-the-money skew (log)", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.3)
        a = np.array([x["a"] for x in weeks])
        bounds = (np.floor(4 * min(a.min(), 0)) / 4, np.ceil(4 * max(a.max(), 1)) / 4)
        cnt, edges = np.histogram(a, bins=18, range=bounds)
        count_top = max(5, int(cnt.max()) + 2)
        hist_ax = axes(list(bounds), [0, count_top], x_length=3.6, y_length=2.2, xlabel=r"power-law exponent $a$ ($\psi \propto T^{-a}$)",
                       xticks=[-1, -0.5, 0, 0.5, 1.0], yticks=[0, count_top], font_size=14).to_corner(DR, buff=0.4).shift(UP * 0.6)
        bars = VGroup(*[Rectangle(width=hist_ax.ax.c2p(edges[1] - edges[0], 0)[0] - hist_ax.ax.c2p(0, 0)[0] - 0.03,
                                  height=max(hist_ax.ax.c2p(0, c_)[1] - hist_ax.ax.c2p(0, 0)[1], 0.001),
                                  stroke_width=0, fill_color=IV, fill_opacity=0.85).move_to(
            hist_ax.ax.c2p(e + (edges[1] - edges[0]) / 2, c_ / 2)) for c_, e in zip(cnt, edges[:-1])])
        med = DashedLine(hist_ax.ax.c2p(w["a_median"], 0), hist_ax.ax.c2p(w["a_median"], count_top), stroke_color=YELLOW)
        medl = MathTex(rf"\text{{median}}\ a = {w['a_median']:.2f}", font_size=24, color=YELLOW).next_to(hist_ax, UP, buff=0.1)
        src = real_data('Deribit pooled option marks; original 102 manifest dates (101 Wednesdays, 1 Thursday); SVI finite differences', corner=DL)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, src)
        self.remove(hint, src)
        with self.voiceover(
            f"""Here are the original one hundred and two dates in the frozen 2024 to 2025 data manifest. Each thread shows the magnitude of a finite-difference, near-at-the-money SVI skew, by expiry, on log scales. The source is pooled option marks; neither simultaneous executable quotes nor a continuous limit at expiry. <bookmark mark='a'/> Many dates have steeper short-maturity magnitudes, but eight fitted exponents are negative. Signed skews also change direction, so absolute values hide information. Each white line is a descriptive power fit. <bookmark mark='b'/> The histogram preserves every exponent, including those below zero. Its median is {w['a_median']:.2f}, with quartiles {w['a_q'][0]:.2f} and {w['a_q'][1]:.2f}. These are finite-window summaries, not proof of an exploding skew. Red marks the seventh of August 2024, two days after the crisis discussed later."""
        ) as vo:
            self.play(FadeIn(hint), FadeIn(src), Create(ax), run_time=1.5)
            self.play(LaggedStart(*[Create(r_) for r_ in rows], lag_ratio=0.08, run_time=8))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(f) for f in fits], lag_ratio=0.02, run_time=3))
            vo.wait_until("b")
            self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.72, frame_center=RIGHT * 2.4, run_time=4)
            # the strands move left and shrink, leaving the right side to the histogram
            self.add_fixed_in_frame_mobjects(hist_ax, bars, med, medl)
            self.remove(hist_ax, bars, med, medl)
            self.play(FadeIn(hist_ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                      Create(med), FadeIn(medl))
            if crisis is not None:
                self.play(Indicate(rows[crisis], color=BAD), run_time=1.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, frame_center=ORIGIN,
                         added_anims=[FadeOut(VGroup(ax, rows, fits)), FadeOut(hint), FadeOut(src),
                                      FadeOut(VGroup(hist_ax, bars, med, medl))], run_time=1.5)
        self.clear_scene(run_time=0.1)

    def law(self, s, w):
        T = np.asarray(s["T"])
        y = np.asarray(s["skew"])
        Tg = np.asarray(s["grid"])
        yr = skew_range(y, s["power_fit"], s["shifted_fit"])
        g = loglog_skew_axes(y_range=yr).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(abs(b))), radius=0.07, color=WHITE) for a, b in zip(T, y) if np.isfinite(b) and abs(b) > 0])
        pw = curve(ax, np.log10(Tg), np.log10(np.asarray(s["power_fit"])), MODEL_COL["power"],
                   stroke_width=2.5)
        sh = curve(ax, np.log10(Tg), np.log10(np.asarray(s["shifted_fit"])), MODEL_COL["shifted"],
                   stroke_width=2.5)
        p, q = s["power"], s["shifted"]
        leg = legend([(WHITE, r"the Surface, 10 December 2025"), (MODEL_COL["power"], rf"power law: $T^{{-{p['a']:.2f}}}$"),
                      (MODEL_COL["shifted"], rf"bounded: $(T + {365 * q['eps']:.0f}\text{{d}})^{{-{q['a']:.2f}}}$")],
                     font_size=17).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        side = VGroup(
            wrapped_label('single-date fits summarize observed curvature; a positive shift bounds the fitted form, without observing the zero-maturity limit', 4.0, 19, GREY_A),
            wrapped_label('weekly comparison: weighted fitting objective, unweighted reported log RMSE; differing exponent bounds; 0.01 is a descriptive threshold', 4.0, 19, GREY_A),
            wrapped_label(r"Guyon and El Amrani (Risk, 2023): on S\&P 500, Euro Stoxx 50 and DAX skews of 2020--21, a "
                          r"two-parameter power law fails once the shortest expiries are included", 4.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        src = real_data(r"the Surface (Part 13): SVI skew at each expiry")
        verdict = ("in most weeks the straight line is as good as anything" if w["bounded_share"] < 0.5 else
                   "in most weeks the bending form fits better")
        with self.voiceover(
            f"""One date up close: the tenth of December 2025 Surface. <bookmark mark='a'/> The power fit has exponent {p['a']:.2f}. <bookmark mark='b'/> A shifted power law fits these points a little better, with a shift of {365 * q['eps']:.0f} days. A positive shift makes this fitted functional form bounded at zero maturity; it does not observe that limit. <bookmark mark='c'/> Across the original dates, the shifted form reduces reported log root mean squared error by more than point zero one in {100 * w['bounded_share']:.0f} percent. Weekly optimization weights use quote counts, while this reported error is unweighted. The exponent constraints also differ between the two fits. The threshold is a descriptive in-sample convention, not a significance test or a validated choice of model."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots],
                                                                         lag_ratio=0.1, run_time=2))
            vo.wait_until("a")
            self.play(Create(pw), FadeIn(leg[1]))
            vo.wait_until("b")
            self.play(Create(sh), FadeIn(leg[2]), FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()

    def definitions(self, w):
        rows = [cmath(r"\psi(T)", r"=", r"\big|\partial_k\sigma_{\rm imp}(k, T)\big|_{k = 0}", font_size=40,
                      colors={r"\psi(T)": IV}),
                cmath(r"\psi(T)", r"=", r"c\,T^{-a}\quad\text{(fitted over finite maturities)}", font_size=40, colors={r"\psi(T)": IV}),
                cmath(r"\psi(T)", r"=", r"c\,(T + \varepsilon)^{-a}", font_size=40, colors={r"\psi(T)": IV})]
        whys = [why(r"the at-the-money skew: the slope of the smile in log-moneyness $k = \log K/F$"),
                why('a descriptive power fit; $a=1/2-H$ needs a specified model and an asymptotic regime'),
                why(r"the bounded rival: finite as $T \to 0$, a power law only beyond $\varepsilon$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-2.2, buff=0.7, edge=6.9)
        verdict = ("A rough reading, as the time series of chapter three will find." if w["H_median"] > 0 else
                   "That is below zero, which no rough model allows: something besides roughness steepens bitcoin's "
                   "short end, and the next chapter's computed jump skews show one candidate.")
        q = pause(r"If $H = 0.1$, by what factor is a 1-day option's skew steeper than a 1-month option's?",
                  width=6.4).to_corner(DL, buff=0.35)
        ans = MathTex(r"30^{\,0.4} \approx 3.9", font_size=40, color=YELLOW).next_to(q, RIGHT, buff=0.7)  # beside the card
        with self.voiceover(
            f"""Define psi as the magnitude of the implied-volatility slope in log-moneyness at the money. The observations use finite differences, an approximation to that derivative. <bookmark mark='a'/> A power law writes psi as c times T to the minus a. Only under a suitable rough-model short-maturity expansion does a equal one half minus H. Substituting our finite-window median {w['a_median']:.2f} would give {w['H_median']:.2f}. This does not identify a Hurst exponent. The usual square-integrable Brownian Volterra kernel requires positive H; broader hyper-rough constructions are a different class. <bookmark mark='b'/> The shifted rival is bounded when its fitted shift is positive. <bookmark mark='c'/> Suppose H is a tenth and the power approximation holds from one day to one month. What is the ratio of skew magnitudes? <bookmark mark='d'/> Thirty to the power four tenths: about three point nine. This ratio says nothing by itself about a position's total volatility risk."""
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(Write(ans))
        self.wait(0.4)
        self.clear_scene()
