from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
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
        c = chapter_card(1, r"The fact: an exploding skew", r"How fast does the skew grow as expiry nears?", part=PART)
        with self.voiceover("Chapter one. The fact: an exploding skew."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def loom(self, w):
        weeks = w["weeks"]
        nw = len(weeks)
        lo_T = np.log10(2 / 365)
        ax = ThreeDAxes(x_range=[lo_T, 0, 1], y_range=[0, nw, 20], z_range=[-1.6, 0.8, 0.8], x_length=6.4,
                        y_length=6.0, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.3)
        crisis = next((i for i, x in enumerate(weeks) if x["day"] == "2024-08-07"), None)
        rows, fits = VGroup(), VGroup()
        for i, x in enumerate(weeks):
            T = np.asarray(x["T"])
            y = np.log10(np.clip(np.abs(np.asarray(x["skew"])), 10 ** -1.6, 10 ** 0.8))
            col = BAD if i == crisis else interpolate_color(ManimColor(IV), ManimColor(OPT), i / max(nw - 1, 1))
            pts = [ax.c2p(np.log10(t), i, v) for t, v in zip(T, y)]
            rows.add(VMobject(stroke_color=col, stroke_width=2.4 if i == crisis else 1.4).set_points_as_corners(pts))
            Tf = np.array([max(T.min(), 2 / 365), T.max()])
            yf = np.clip(np.log10(x["c"] * Tf ** (-x["a"])), -1.6, 0.8)
            fits.add(Line(ax.c2p(np.log10(Tf[0]), i, yf[0]), ax.c2p(np.log10(Tf[1]), i, yf[1]),
                          stroke_color=WHITE if i != crisis else BAD, stroke_width=1.0, stroke_opacity=0.6))
        hint = VGroup(label(r"left to right: time to expiry, 2 days to 1 year (log)", font_size=20, color=GREY_A),
                      label(r"front to back: the week, January 2024 to December 2025", font_size=20, color=GREY_A),
                      label(r"height: the at-the-money skew (log)", font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.3)
        a = np.array([x["a"] for x in weeks])
        hist_ax = axes([0, 1.2], [0, 30], x_length=3.6, y_length=2.2, xlabel=r"power-law exponent $a$ ($\psi \propto T^{-a}$)",
                       xticks=[0, 0.5, 1.0], yticks=[0, 15, 30], font_size=14).to_corner(DR, buff=0.4).shift(UP * 0.6)
        cnt, edges = np.histogram(np.clip(a, 0, 1.199), bins=12, range=(0, 1.2))
        bars = VGroup(*[Rectangle(width=hist_ax.ax.c2p(0.1, 0)[0] - hist_ax.ax.c2p(0, 0)[0] - 0.03,
                                  height=max(hist_ax.ax.c2p(0, c_)[1] - hist_ax.ax.c2p(0, 0)[1], 0.001),
                                  stroke_width=0, fill_color=IV, fill_opacity=0.85).move_to(
            hist_ax.ax.c2p(e + 0.05, c_ / 2)) for c_, e in zip(cnt, edges[:-1])])
        med = DashedLine(hist_ax.ax.c2p(w["a_median"], 0), hist_ax.ax.c2p(w["a_median"], 30), stroke_color=YELLOW)
        medl = MathTex(rf"\text{{median}}\ a = {w['a_median']:.2f}", font_size=24, color=YELLOW).next_to(hist_ax, UP, buff=0.1)
        src = real_data(rf"Deribit option trades, {nw} weekly days, 2024--2025; SVI per expiry, $|k| < 0.3$", corner=DL)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint, src)
        self.remove(hint, src)
        with self.voiceover(
            "Here is the fact, measured not on one day but on every week for two years. Each thread is one week of "
            "bitcoin options: the at-the-money skew, how steeply implied volatility falls as the strike rises, "
            "at every expiry from two days to a year, both on log scales. The weeks are woven in one by one, like "
            "cloth on a loom. <bookmark mark='a'/> Every week has the same shape: short expiries far steeper than "
            "long ones. Through each, a straight line: a power law. <bookmark mark='b'/> Now turn the loom so we "
            "look along the weeks. All the lines stack into one fan. Their slopes, the exponents of the power law, "
            f"pile up on the right. The median exponent is {w['a_median']:.2f}; half the weeks lie between "
            f"{w['a_q'][0]:.2f} and {w['a_q'][1]:.2f}. The red thread is the week of the seventh of August 2024, two "
            "days after the crash we will meet in chapter fourteen."
        ) as vo:
            self.play(FadeIn(hint), FadeIn(src), Create(ax), run_time=1.5)
            self.play(LaggedStart(*[Create(r_) for r_ in rows], lag_ratio=0.08, run_time=8))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(f) for f in fits], lag_ratio=0.02, run_time=3))
            vo.wait_until("b")
            self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.85, run_time=4)
            self.add_fixed_in_frame_mobjects(hist_ax, bars, med, medl)
            self.remove(hist_ax, bars, med, medl)
            self.play(FadeIn(hist_ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                      Create(med), FadeIn(medl))
            if crisis is not None:
                self.play(Indicate(rows[crisis], color=BAD), run_time=1.5)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, rows, fits)), FadeOut(hint), FadeOut(src),
                                      FadeOut(VGroup(hist_ax, bars, med, medl))], run_time=1.5)
        self.clear_scene()

    def law(self, s, w):
        T = np.asarray(s["T"])
        y = np.asarray(s["skew"])
        Tg = np.asarray(s["grid"])
        g = loglog_skew_axes().to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(np.log10(a), np.log10(b)), radius=0.07, color=WHITE) for a, b in zip(T, y) if b > 0.02])
        pw = curve(ax, np.log10(Tg), np.clip(np.log10(np.asarray(s["power_fit"])), -1.6, 0.6), MODEL_COL["power"],
                   stroke_width=2.5)
        sh = curve(ax, np.log10(Tg), np.clip(np.log10(np.asarray(s["shifted_fit"])), -1.6, 0.6), MODEL_COL["shifted"],
                   stroke_width=2.5)
        p, q = s["power"], s["shifted"]
        leg = legend([(WHITE, r"the Surface, 10 December 2025"), (MODEL_COL["power"], rf"power law: $T^{{-{p['a']:.2f}}}$"),
                      (MODEL_COL["shifted"], rf"bounded: $(T + {365 * q['eps']:.0f}\text{{d}})^{{-{q['a']:.2f}}}$")],
                     font_size=17).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        side = VGroup(
            wrapped_label(rf"this day: log error {p['rmse_log']:.2f} for the power law, {q['rmse_log']:.2f} for a skew "
                          rf"that stops growing below about {365 * q['eps']:.0f} days", 4.0, 19, GREY_A),
            wrapped_label(rf"all {w['n_weeks']} weeks: the bounded form beats the power law by more than 0.01 in "
                          rf"{100 * w['bounded_share']:.0f}\% of them; median shift "
                          rf"{w['eps_median_days']:.0f} days", 4.0, 19, GREY_A),
            wrapped_label(r"Guyon and El Amrani (Risk, 2023): on S\&P 500, Euro Stoxx 50 and DAX skews of 2020--21, a "
                          r"two-parameter power law fails once the shortest expiries are included", 4.0, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.35).align_to(leg, LEFT)
        src = real_data(r"the Surface (Part 13): SVI skew at each expiry")
        verdict = ("in most weeks the straight line is as good as anything" if w["bounded_share"] < 0.5 else
                   "in most weeks the bending form fits better")
        with self.voiceover(
            "Now one day up close: the Surface of Part thirteen, the tenth of December 2025. <bookmark mark='a'/> "
            f"A straight line fits it, a power law with exponent {p['a']:.2f}. <bookmark mark='b'/> But a skew that "
            f"stops growing below about {365 * q['eps']:.0f} days fits these points a little better. Julien Guyon and "
            "Mehdi El Amrani made this objection in 2023, on the S&P 500, the Euro Stoxx and the DAX: once the "
            "shortest expiries are included, a two-parameter power law fails. <bookmark mark='c'/> Across all our "
            f"weeks, the bounded form wins by a clear margin in {100 * w['bounded_share']:.0f} percent of them, so "
            + verdict + ". The fact is real; its exact form at the very short end is disputed, and chapter twelve "
            "returns to it."
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
                cmath(r"\psi(T)", r"=", r"c\,T^{-a},\qquad a = \tfrac12 - H", font_size=40, colors={r"\psi(T)": IV}),
                cmath(r"\psi(T)", r"=", r"c\,(T + \varepsilon)^{-a}", font_size=40, colors={r"\psi(T)": IV})]
        whys = [why(r"the at-the-money skew: the slope of the smile in log-moneyness $k = \log K/F$"),
                why(r"the power law; read as roughness, the exponent gives a Hurst exponent $H$ (chapter 2 says why)"),
                why(r"the bounded rival: finite as $T \to 0$, a power law only beyond $\varepsilon$")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-2.2, buff=0.7, edge=6.9)
        verdict = ("A rough reading, as the time series of chapter three will find." if w["H_median"] > 0 else
                   "That is below zero, which no rough model allows: something besides roughness steepens bitcoin's "
                   "short end, and the next chapter's computed jump skews show one candidate.")
        q = pause(r"If $H = 0.1$, by what factor is a 1-day option's skew steeper than a 1-month option's?",
                  width=7.0).to_edge(DOWN, buff=0.4)
        ans = MathTex(r"30^{\,0.4} \approx 3.9", font_size=40, color=YELLOW).next_to(q, UP, buff=0.25)
        with self.voiceover(
            "The definitions. The skew psi of T is the slope of implied volatility in log-moneyness, at the money. "
            "<bookmark mark='a'/> The power law says psi is a constant times T to the minus a. Read as roughness, "
            f"a equals one half minus H, and our median exponent of {w['a_median']:.2f} gives H of "
            f"{w['H_median']:.2f}. " + verdict + " "
            "<bookmark mark='b'/> The bounded rival shifts maturity by epsilon, so the skew "
            "stays finite as expiry nears. <bookmark mark='c'/> Pause and predict. If H is a tenth, how much steeper "
            "is a one-day option's skew than a one-month option's? <bookmark mark='d'/> Thirty days to one is a "
            "factor of thirty, raised to the power four-tenths: about three point nine."
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
