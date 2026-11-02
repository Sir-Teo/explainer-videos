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
        self.derive()
        self.theta_identity()
        self.vega_one_bump()

    def card(self):
        c = chapter_card(6, r"The Greeks as geometry", r"What are the slopes of a price?", lit=(1973,), part=PART)
        with self.voiceover("Chapter six. The Greeks as geometry."):
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
            "Every risk an options trader manages is a slope or a curve of one surface: the option's value over "
            "the stock price and the time left. At expiry, the front edge, it is the payoff. "
            "<bookmark mark='a'/> Further back the surface rises and smooths: chapter three's melting kink. "
            "<bookmark mark='b'/> The Greek letters name its slopes. Delta is the slope along the stock axis, "
            "gamma the curvature along it, theta the slope along time, and vega, not a Greek letter at all, how "
            "the whole surface lifts when volatility rises. Take the slice three months out, in yellow."
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
            "Laid flat: on top the value, above its payoff; in the middle its slope, delta, the shares in the "
            "hedge, none far below the strike and one far above. <bookmark mark='a'/> At the bottom the curvature, "
            "gamma: how fast delta changes, so how often the hedger must trade. It lives near the strike. "
            "<bookmark mark='b'/> Let time pass: the value presses onto its payoff, delta steepens into a step, "
            "gamma sharpens into a spike. At the money near expiry, a small move flips the hedge from nothing to "
            "a full share."
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
    def derive(self):
        C = {r"\Delta": DEL, r"\Gamma": GAM, r"\Theta": THE, r"\mathcal V": VEG, r"S": SPOT, r"V": OPT}
        rows = [
            cmath(r"S\,\varphi(d_1)", r"=", r"K e^{-rT}\,\varphi(d_2)", font_size=40, colors=C),
            cmath(r"\Delta", r"=", r"N(d_1)", font_size=40, colors=C),
            cmath(r"\Gamma", r"=", r"\frac{\varphi(d_1)}{S\sigma\sqrt T},\qquad", r"\mathcal V", r"=",
                  r"S\varphi(d_1)\sqrt T", r"=", r"\sigma T S^2", r"\Gamma", font_size=38, colors=C),
            cmath(r"\Theta", r"+", r"r S", r"\Delta", r"+", r"\tfrac12\sigma^2 S^2", r"\Gamma", r"=", r"r", r"V",
                  font_size=40, colors=C),
        ]
        whys = [why(r"$d_1^2 - d_2^2 = 2\ln(S/K) + 2rT$: the identity that makes the Greeks short"),
                why(r"differentiate the formula; the two $\varphi$ terms cancel by the identity"),
                why(r"differentiate again; vega in units of gamma"),
                why(r"the PDE, read as a ledger")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-1.6, buff=0.75, edge=6.9)
        with self.voiceover(
            "Each slope takes two lines, thanks to one identity: S times the normal density at d one equals the "
            "discounted strike times the density at d two. <bookmark mark='a'/> Differentiate the formula in S: "
            "the terms where d one and d two move cancel by it, and delta is just N of d one. "
            "<bookmark mark='b'/> Once more for gamma; vega, the derivative in sigma, comes out as sigma T S "
            "squared gamma. <bookmark mark='c'/> And the equation itself ties three of them together. Pause and "
            "predict: at the money, with no rates, as the maturity grows without limit, what happens to the "
            "call's delta? It goes to one, because d one is half sigma root T."
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
            "Theta is the slope along time: what the option loses each day if the stock stands still. With no "
            "interest rate the equation has two terms, <bookmark mark='a'/> and says theta is minus half sigma "
            "squared S squared gamma. <bookmark mark='b'/> Computed from the formula three months out: what gamma "
            "earns per year, solid pink, and what time costs, dashed blue, lie exactly on top of each other. You "
            "cannot own curvature without paying for it in time. The only question is whether the stock moves "
            "enough to pay the bill: the next chapter."
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
            "Last, vega: how much the value rises with volatility. Another bump at the strike, growing with the "
            "time left, the opposite of gamma. <bookmark mark='a'/> For Black-Scholes it is sigma times time left "
            "times S squared gamma: gamma, theta and vega are one bump seen three ways. Long an option is long "
            "gamma, short theta, long vega; the second-order Greeks, vanna and volga, come with the smile in Part "
            "eleven."
        ) as vo:
            self.play(FadeIn(pv), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.4), FadeIn(tl))
            vo.wait_until("a")
            self.play(Write(eq))
            self.play(FadeIn(table, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()
