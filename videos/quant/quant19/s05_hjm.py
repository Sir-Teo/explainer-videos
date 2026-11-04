from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant19.common import (CURV, FWD, LEVEL, PART, SLOPE, ask, fit_right, grid_fn, illustration, load,
                                         surf3d_axes)


class HJM(VoiceoverScene, ThreeDScene):
    def construct(self):
        j = load("hjm")
        self.card()
        self.derive()
        self.vols(j)
        self.surface(j)
        self.check(j)

    def card(self):
        c = chapter_card(4, r"Heath--Jarrow--Morton: the drift condition", r"What if you model the whole curve at once?",
                         lit=(1992,), part=PART)
        with self.voiceover("Chapter four. Heath, Jarrow and Morton: modelling the whole forward curve at once."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"df(t, T)", r"=", r"\alpha(t, T)\,dt + \sigma(t, T)\cdot dW_t", font_size=42,
                      colors={r"df(t, T)": FWD}),
                cmath(r"\frac{dP(t,T)}{P(t,T)}", r"=", r"r_t\,dt - \Big(\int_t^T \alpha\Big)dt + \tfrac12\Big|\int_t^T "
                      r"\sigma\Big|^2 dt - \Big(\int_t^T \sigma\Big)\cdot dW", font_size=34,
                      colors={r"\frac{dP(t,T)}{P(t,T)}": WHITE}),
                cmath(r"\int_t^T \alpha(t, u)\,du", r"=", r"\tfrac12\Big|\int_t^T \sigma(t, u)\,du\Big|^2", font_size=40,
                      colors={r"=": WHITE}),
                cmath(r"\alpha(t, T)", r"=", r"\sigma(t, T)\cdot\int_t^T \sigma(t, u)\,du", font_size=44,
                      colors={r"\alpha(t, T)": FWD})]
        whys = [why(r"Heath, Jarrow and Morton (1992): every forward rate moves, driven by a few shared Brownian motions"),
                why(r"$P = e^{-\int_t^T f}$; Itô's formula for the bond. Under the pricing measure its expected return "
                    r"must be the short rate $r_t$"),
                why(r"so the drift terms must cancel, for every $T$"),
                why(r"differentiate in $T$: the drift of each forward is fixed by the volatilities. Choose the vols; the "
                    r"model is determined")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.4, buff=0.55, edge=6.9)
        with self.voiceover(
            "Short-rate models start from one rate and derive the curve. David Heath, Robert Jarrow and Andrew Morton, "
            "in 1992, started from the whole forward curve instead: every forward rate moves, driven by a few shared "
            "random shocks. <bookmark mark='a'/> A bond is the exponential of minus the integral of the forwards; "
            "apply Itô's formula. Under the pricing measure, a bond's expected return must be the short rate, like any "
            "traded asset. <bookmark mark='b'/> So the extra terms must cancel, for every maturity. "
            "<bookmark mark='c'/> Differentiate, and the drift of every forward rate is fixed by the volatilities: the "
            "volatility times its own integral. You choose how the curve wiggles; no arbitrage chooses how it drifts."
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

    def vols(self, j):
        tau = np.asarray(j["tau"])
        V = np.asarray(j["vols"]) * 1e4
        dr = np.asarray(j["drift"]) * 1e4
        g = axes([0, 30], [-120, 160], x_length=7.4, y_length=4.4, xlabel=r"time to maturity, years",
                 ylabel=r"forward-rate volatility, bp a year", xticks=[0, 5, 10, 20, 30], yticks=[-100, 0, 100],
                 font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lines = VGroup(*[curve(ax, tau, np.clip(V[k], -120, 160), c_, stroke_width=3) for k, c_ in
                         enumerate((LEVEL, SLOPE, CURV))])
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(30, 0), color=GREY_D, stroke_width=1.5)
        g2 = axes([0, 30], [0, float(dr.max()) * 1.1], x_length=4.0, y_length=2.4, xlabel=r"years",
                  ylabel=r"drift, bp a year", xticks=[0, 15, 30], yticks=[0, round(float(dr.max()))], font_size=12)
        g2.to_edge(RIGHT, buff=0.5).shift(DOWN * 1.4)
        ld = curve(g2.ax, tau, dr, FWD, stroke_width=3)
        leg = legend([(LEVEL, r"level"), (SLOPE, r"slope"), (CURV, r"curvature")], font_size=18).to_edge(
            RIGHT, buff=0.8).shift(UP * 1.8)
        with self.voiceover(
            "Which volatilities? The ones Part eighteen measured: the three principal components of the curve's daily "
            "moves, turned into volatilities for each forward rate and annualized. Level moves every forward; slope "
            "moves the short and long ends against each other; curvature bends the middle. <bookmark mark='a'/> And "
            "the drift that no arbitrage then forces on the forwards, small, a few basis points a year, but growing "
            "with maturity."
        ) as vo:
            self.play(FadeIn(g), Create(zero), Create(lines), FadeIn(leg), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(ld))
        self.add(illustration(r"volatilities: Part 18's factors (GSW daily changes, 1985--2025); forward-rate form by "
                              r"differentiating $\tau\,\sigma_y(\tau)$"))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, j):
        tau = np.asarray(j["tau"])
        P = np.asarray(j["paths"])  # time x paths x tau
        tt = np.linspace(0, 5, P.shape[0])
        Z = P[:, 0, :] * 100
        f = grid_fn(tau, tt, Z)
        ax = surf3d_axes([0, 5, 1], [0, 30, 10], [2, 9, 1], x_length=5.8, y_length=5.2, z_length=3.4)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)
        surf = Surface(lambda u, w: ax.c2p(u, w, np.clip(f(w, u), 2, 9)), u_range=(0, 5), v_range=(0, 30),
                       resolution=(20, 30), fill_opacity=0.8, stroke_width=0.3, stroke_color=GREY_D,
                       checkerboard_colors=False)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.SPOT, 2), (QC.DELTA, 5), (QC.LOSS, 8)], axis=2)
        key = VGroup(label(r"calendar time (across), maturity ahead (back), forward rate (up): one simulated path",
                           font_size=18, color=GREY_A)).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "One simulated future: five years of forward curves, starting from today's at the front edge. Each slice "
            "across the back is a whole curve on one date. <bookmark mark='a'/> It shifts, tilts and bends, exactly "
            "the three ways Part eighteen measured, and nothing else: a three-factor model can only move in three "
            "directions at once."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(Create(surf), run_time=3)
            vo.wait_until("a")
            self.move_camera(theta=-125 * DEGREES, run_time=5)
        self.wait(0.3)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)

    def check(self, j):
        tau = np.asarray(j["tau"])
        q = np.asarray(j["q_T"]) * 100
        f0 = np.asarray(j["f0"]) * 100
        g = axes([0, 30], [0, 10], x_length=7.4, y_length=4.4, xlabel=r"maturity, years", ylabel=r"forward rate, \%",
                 xticks=[0, 5, 10, 20, 30], yticks=[0, 2, 4, 6, 8, 10], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        band = Polygon(*[ax.c2p(a, b) for a, b in zip(tau, np.clip(q[0], 0, 10))],
                       *[ax.c2p(a, b) for a, b in zip(tau[::-1], np.clip(q[2][::-1], 0, 10))], stroke_width=0,
                       fill_color=FWD, fill_opacity=0.18)
        l0 = curve(ax, tau, f0, WHITE, stroke_width=3)
        lm = curve(ax, tau, q[1], FWD, stroke_width=3)
        rows = VGroup(label(r"the martingale test: $\mathbb{E}[P(5, 5 + m)/\beta_5] / P(0, 5 + m)$", font_size=20),
                      *[MathTex(rf"m = {c_['m']}:\ \ {c_['ratio']:.4f}", font_size=26) for c_ in j["check"]],
                      wrapped_label(r"1 if the drift is right; the gaps are Monte Carlo noise and the time step", 3.8,
                                    17, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4)
        fit_right(rows)
        leg = legend([(WHITE, r"today's forwards"), (FWD, r"in five years: median and 5--95\%")], font_size=17).next_to(
            g, UP, buff=0.05)
        with self.voiceover(
            "Four thousand such futures, five years on: the median forward curve, and the range that contains ninety "
            "percent of them. <bookmark mark='a'/> And the test that the drift is right: a bond maturing m years after "
            "year five, discounted by the money-market account, must on average be worth today's price. It is, to "
            "within a fraction of a percent for short bonds and about one percent at twenty years, the residue of a "
            "finite time step and finite paths."
        ) as vo:
            self.play(FadeIn(g), FadeIn(band), Create(l0), Create(lm), FadeIn(leg), run_time=2.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3))
        q_ = ask(r"the volatilities decide the drift. What goes wrong if a trader sets the forwards' drift to their own "
                 r"forecast instead?")
        with self.voiceover("The volatilities decide the drift. What goes wrong if a trader puts in a drift from their "
                            "own forecast instead?"):
            self.play(FadeIn(q_))
        self.wait(0.5)
        self.clear_scene()
