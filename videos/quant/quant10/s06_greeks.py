from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import DEL, GAM, OPT, PART, SPOT, THE, VEG

K, SIG = 100.0, 0.25


def V(S, tau):
    return bs.price(S, K, np.maximum(tau, 1e-4), SIG)


def G(S, tau):
    return bs.greeks(S, K, np.maximum(tau, 1e-4), SIG)


class Greeks(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.card()
        self.surface()
        self.delta_gamma()
        self.theta_identity()
        self.vega_one_bump()

    def card(self):
        c = chapter_card(5, r"The Greeks as geometry", r"What are the slopes of a price?", lit=(1973,), part=PART)
        with self.voiceover("Chapter five. The Greeks as geometry."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def surface(self):
        ax = ThreeDAxes(x_range=[60, 140, 20], y_range=[0, 1, 0.25], z_range=[0, 45, 15], x_length=8.0,
                        y_length=5.0, z_length=4.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.6)
        surf = price_surface(ax, lambda s, t: float(V(s, t)), (60, 140), (0.0, 1.0), resolution=(40, 30),
                             z_lo=0, z_hi=40)
        payoff = VMobject(stroke_color=WHITE, stroke_width=4).set_points_as_corners(
            [ax.c2p(s, 0, max(s - K, 0)) for s in np.linspace(60, 140, 81)])
        xl = label(r"stock price $S$", font_size=26, color=SPOT)
        yl = label(r"time to expiry", font_size=26, color=THE)
        zl = label(r"option value $V$", font_size=26, color=OPT)
        hint = VGroup(xl, yl, zl).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4)
        params = note(r"a call: $K = 100$, $\sigma = 25\%$, $r = 0$", font_size=20).to_corner(DR, buff=0.3)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-58 * DEGREES, zoom=0.92)
        self.add_fixed_in_frame_mobjects(hint, params)
        self.remove(hint, params)
        # a slice at three months to expiry, drawn on the surface: the next panel's value curve
        slice_ = VMobject(stroke_color=YELLOW, stroke_width=5).set_points_as_corners(
            [ax.c2p(x, 0.25, float(V(x, 0.25))) + OUT * 0.03 for x in np.linspace(60, 140, 81)])
        with self.voiceover(
            "Every risk an options trader manages is a slope or a curve of one surface: the option's value, "
            "over the stock price and the time left. Here it is for a call. Along the front edge, at expiry, it "
            "is the payoff, the white hockey stick. <bookmark mark='a'/> Further back, with more time left, the "
            "surface rises and smooths, the heat-equation picture of chapter two, now in three dimensions. "
            "<bookmark mark='b'/> The Greek letters are the names of its slopes. Delta is the slope along the "
            "stock axis. Gamma is the curvature along it. Theta is the slope along the time axis. And vega, which "
            "is not a Greek letter at all, is how the whole surface lifts when volatility rises. Take the slice three "
            "months from expiry, in yellow, and lay it flat."
        ) as vo:
            self.play(FadeIn(hint), FadeIn(params), Create(ax), Create(payoff), run_time=2)
            vo.wait_until("a")
            self.play(Create(surf), run_time=3)
            self.move_camera(theta=-44 * DEGREES, phi=64 * DEGREES, run_time=vo.until("b"))
            self.play(Create(slice_), run_time=1.5)
            self.move_camera(theta=-36 * DEGREES, run_time=max(vo.remaining(1.0) - 1.0, 1.0))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, payoff, slice_)),
                                                                  FadeOut(hint), FadeOut(params)], run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def panel(self, y_range, ylabel, yticks, y_len=1.85):
        g = axes([60, 140], y_range, x_length=6.2, y_length=y_len, ylabel=ylabel, yticks=yticks, font_size=18)
        return g

    def delta_gamma(self):
        tau = ValueTracker(1.0)
        xs = np.linspace(60, 140, 321)
        pv = self.panel([0, 45], r"value $V$", [0, 20, 40])
        pd = self.panel([0, 1.05], r"delta $\Delta = \partial_S V$", [0, 0.5, 1])
        pg = self.panel([0, 0.17], r"gamma $\Gamma = \partial_{SS} V$", [0, 0.08, 0.16])
        stack = VGroup(pv, pd, pg).arrange(DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        for p in (pv, pd, pg):
            p.add(MathTex(r"S", font_size=22, color=SPOT).next_to(p.ax.c2p(140, p.ax.y_range[0]), RIGHT, buff=0.1))
        payoff = curve(pv.ax, [60, 100, 140], [0, 0, 40], GREY_C, stroke_width=2)
        lines = VGroup(
            always_redraw(lambda: curve(pv.ax, xs, V(xs, tau.get_value()), OPT, stroke_width=3.5)),
            always_redraw(lambda: curve(pd.ax, xs, G(xs, tau.get_value())["delta"], DEL, stroke_width=3.5)),
            always_redraw(lambda: curve(pg.ax, xs, np.minimum(G(xs, tau.get_value())["gamma"], 0.17), GAM,
                                        stroke_width=3.5)),
        )
        tlab = always_redraw(lambda: MathTex(rf"T - t = {tau.get_value():.2f}\ \text{{years}}", font_size=34,
                                             color=THE).to_corner(UR, buff=0.6))
        notes = VGroup(
            wrapped_label(r"\textbf{Delta}: shares to hold. Far below the strike, none; far above, one share.",
                          5.4, 26, DEL),
            wrapped_label(r"\textbf{Gamma}: how fast delta changes, so how often the hedge must be traded. It "
                          r"lives near the strike, and it sharpens into a spike as expiry nears.", 5.4, 26, GAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        with self.voiceover(
            "Slice the surface at one time to expiry and look along the stock axis. On top, the value curve, "
            "above its payoff. In the middle, its slope: delta, the number of shares in the hedge. Far below the "
            "strike the call is almost surely worthless and needs no shares; far above it is almost surely "
            "exercised and needs one. <bookmark mark='a'/> At the bottom, the curvature: gamma, the rate at which "
            "delta changes as the stock moves, and so the rate at which the hedger must trade. Gamma lives near "
            "the strike, where the hockey stick bends. <bookmark mark='b'/> Now let time pass. As expiry "
            "approaches, the value curve presses down onto its payoff, delta steepens into a step, and gamma "
            "sharpens into a spike at the strike. An at-the-money option close to expiry is the most violent "
            "thing to hedge: a small move flips it from worthless to one full share."
        ) as vo:
            self.play(FadeIn(stack), Create(payoff), FadeIn(tlab))
            self.add(lines[0])
            self.play(FadeIn(lines[0]))
            self.add(lines[1])
            self.play(FadeIn(notes[0]))
            vo.wait_until("a")
            self.add(lines[2])
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(tau.animate.set_value(0.02), run_time=max(vo.remaining(1.0) - 1.5, 5.0), rate_func=smooth)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theta_identity(self):
        rows = [
            cmath(r"\partial_t V", r"+", r"r S\,\partial_S V", r"+", r"\tfrac12\sigma^2 S^2", r"\partial_{SS} V",
                  r"-", r"r V", r"=", r"0", font_size=40,
                  colors={r"\partial_t V": THE, r"\partial_{SS} V": GAM, r"\tfrac12\sigma^2 S^2": GAM}),
            cmath(r"\Theta", r"=", r"-", r"\tfrac12\sigma^2 S^2", r"\,\Gamma", r"\qquad (r = 0)", font_size=46,
                  colors={r"\Theta": THE, r"\,\Gamma": GAM, r"\tfrac12\sigma^2 S^2": GAM}),
        ]
        g = VGroup(*rows).arrange(DOWN, buff=0.45).to_edge(UP, buff=0.4)
        xs = np.linspace(60, 140, 321)
        tau = 0.25
        gr = G(xs, tau)
        pg = axes([60, 140], [0, 9], x_length=8.4, y_length=3.0, xlabel=r"stock price $S$",
                  ylabel=r"per year, in dollars", xticks=[60, 100, 140], yticks=[0, 4, 8], font_size=20)
        pg.next_to(g, DOWN, buff=0.35)
        dg = curve(pg.ax, xs, 0.5 * SIG ** 2 * xs ** 2 * gr["gamma"], GAM, stroke_width=14).set_stroke(opacity=0.55)
        th = DashedVMobject(curve(pg.ax, xs, -gr["theta"], THE, stroke_width=5), num_dashes=60)
        leg = legend([(GAM, r"$\tfrac12\sigma^2 S^2\,\Gamma$: what gamma earns"),
                      (THE, r"$-\Theta$: what time costs")], font_size=24)
        leg.arrange(RIGHT, buff=0.8).next_to(pg, DOWN, buff=0.25)
        with self.voiceover(
            "Theta is the slope along time: how much value the option loses each day if the stock stands still. "
            "Look again at the Black-Scholes equation. With no interest rate it has just two terms, <bookmark "
            "mark='a'/> and it says theta equals minus one half sigma squared S squared times gamma. Time decay "
            "and curvature are the same quantity with opposite signs. <bookmark mark='b'/> Here they are as "
            "computed from the formula, three months from expiry: the solid pink curve is what gamma earns per "
            "year, the dashed blue one is what time costs per year. They lie exactly on top of each other. This "
            "is the most important identity on an options desk: you cannot own curvature without paying for it in "
            "time, and you cannot collect time decay without being short curvature. The only question is whether "
            "the stock will move enough to pay the bill, which is the next chapter."
        ) as vo:
            self.play(Write(rows[0]))
            vo.wait_until("a")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(pg), Create(dg), FadeIn(leg[0]))
            self.play(Create(th), FadeIn(leg[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vega_one_bump(self):
        xs = np.linspace(60, 140, 321)
        taus = (1.0, 0.25, 0.05)
        cols = (VEG, interpolate_color(ManimColor(VEG), ManimColor(WHITE), 0.35),
                interpolate_color(ManimColor(VEG), ManimColor(WHITE), 0.7))
        pv = axes([60, 140], [0, 42], x_length=7.0, y_length=3.6, xlabel=r"stock price $S$",
                  ylabel=r"vega, per 1.00 of volatility", xticks=[60, 100, 140], yticks=[0, 20, 40], font_size=20)
        pv.to_edge(LEFT, buff=0.8).shift(DOWN * 0.6)
        lines = VGroup(*[curve(pv.ax, xs, G(xs, t)["vega"], c, stroke_width=4) for t, c in zip(taus, cols)])
        tl = VGroup(*[MathTex(rf"T - t = {t:g}", font_size=24, color=c).next_to(pv.ax.c2p(100, float(G(100, t)['vega'])),
                                                                                  UP, buff=0.08)
                      for t, c in zip(taus, cols)])
        eq = cmath(r"\text{vega}", r"=", r"\sigma\,(T - t)\,S^2", r"\,\Gamma", font_size=44,
                   colors={r"\text{vega}": VEG, r"\,\Gamma": GAM}).to_edge(UP, buff=0.6)
        table = VGroup(
            label(r"long an option:", font_size=28, color=GREY_A),
            label(r"long gamma \ $\Leftrightarrow$ \ short theta \ $\Leftrightarrow$ \ long vega", font_size=28),
            label(r"short an option: all three signs flip", font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
        if table.width > 5.6:
            table.scale_to_fit_width(5.6)
        with self.voiceover(
            "Last, vega: how much the value rises if volatility rises by one unit. It is a bump too, centred at "
            "the strike, and it grows with the time left, the opposite of gamma, because volatility has longer to "
            "work. <bookmark mark='a'/> In fact for Black-Scholes, vega is sigma times the time left times S "
            "squared gamma. So gamma, theta and vega are one bump seen three ways: a trader long an option is long "
            "gamma, short theta and long vega at once, and the short side is the mirror image. Second-order "
            "Greeks like vanna and volga, the slopes of delta and vega with respect to volatility, matter once "
            "volatility itself moves; they come back with the smile in Parts eleven and twelve."
        ) as vo:
            self.play(FadeIn(pv), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.4), FadeIn(tl))
            vo.wait_until("a")
            self.play(Write(eq))
            self.play(FadeIn(table, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()
