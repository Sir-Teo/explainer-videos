from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import termstructure as TS
from videos.quant.quant19.common import CIRC, PART, VAS, ZERO, ask, house_lab, illustration, load, surf3d_axes


class Affine(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("shortrate")
        self.card()
        self.derive()
        self.shapes(s)
        self.surface(s)
        self.lab(s)

    def card(self):
        c = chapter_card(2, r"Affine term structures", r"How does a short-rate model price a bond?", part=PART)
        with self.voiceover("Chapter two. From a short rate to a whole curve: affine term structures."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"P(t, T)", r"=", r"\mathbb{E}^{\mathbb{Q}}_t\Big[e^{-\int_t^T r_s\,ds}\Big]", font_size=42,
                      colors={r"P(t, T)": ZERO}),
                cmath(r"\partial_t P + \mu(r)\,\partial_r P + \tfrac12 \sigma^2(r)\,\partial_{rr} P", r"=", r"r P",
                      font_size=38, colors={r"=": WHITE}),
                cmath(r"P", r"=", r"e^{A(\tau) - B(\tau)\,r},\quad \tau = T - t", font_size=42, colors={r"P": ZERO}),
                cmath(r"B'", r"=", r"1 - aB - \tfrac{\beta}{2}B^2,\qquad A' = -ab\,B + \tfrac{\alpha}{2}B^2", font_size=38,
                      colors={r"B'": VAS})]
        whys = [why(r"a bond pays 1 at $T$; under the pricing measure, discount it along every path of the short rate"),
                why(r"Feynman--Kac (Part 5): the expectation solves this equation, with $P(T, T) = 1$"),
                why(r"guess an exponential that is affine in $r$ (Duffie and Kan 1996): it works when the drift and the "
                    r"variance $\alpha + \beta r$ are affine too"),
                why(r"matching the terms in $r$ and the constants leaves two ordinary differential equations (Riccati). "
                    r"Vasicek: $\beta = 0$, so $B = (1 - e^{-a\tau})/a$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-1.6, buff=0.55, edge=6.9)
        with self.voiceover(
            "A bond pays one dollar at T. Its price is the expected discount along every path the short rate might "
            "take, under the pricing measure of Part four. <bookmark mark='a'/> By Feynman and Kac, that expectation "
            "solves a partial differential equation in the short rate. <bookmark mark='b'/> Guess that the price is an "
            "exponential of something linear in r. Darrell Duffie and Rui Kan showed in 1996 that the guess works "
            "exactly when the drift and the variance of r are themselves linear. <bookmark mark='c'/> Then matching "
            "terms turns the partial differential equation into two ordinary ones, of Riccati type. For Vasicek, B is "
            "one minus e to the minus a tau, over a: the sensitivity of a tau-year bond to today's short rate."
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

    def shapes(self, s):
        T = np.asarray(s["T"])
        g = axes([0, 30], [0, 9], x_length=8.0, y_length=4.6, xlabel=r"maturity, years", ylabel=r"zero yield, \%",
                 xticks=[0, 5, 10, 20, 30], yticks=[0, 2, 4, 6, 8], font_size=14).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        lines = VGroup()
        for k, sh in s["shapes"].items():
            lines.add(VGroup(curve(ax, T, 100 * np.asarray(sh["vas"]), VAS, stroke_width=3),
                             DashedVMobject(curve(ax, T, 100 * np.asarray(sh["cir"]), CIRC, stroke_width=3),
                                            num_dashes=40)))
        v = s["vas"]
        y_inf = 100 * (v["b"] - v["sigma"] ** 2 / (2 * v["a"] ** 2))
        lim = DashedLine(ax.c2p(0, y_inf), ax.c2p(30, y_inf), color=GREY_B, stroke_width=1.5)
        leg = legend([(VAS, r"Vasicek"), (CIRC, r"CIR (dashed)")], font_size=18).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        side = VGroup(
            label(r"short rate today: 0.5\%, 3\%, 8\%", font_size=20, color=GREY_A),
            MathTex(rf"y_\infty = b - \frac{{\sigma^2}}{{2a^2}} = {y_inf:.2f}\%", font_size=28, color=VAS),
            wrapped_label(r"every curve heads to the same long yield: with one factor, today's short rate is "
                          r"forgotten at long maturities, and convexity pulls the long end below $b$", 3.8, 18, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(leg, DOWN, buff=0.4, aligned_edge=LEFT)
        side.shift(LEFT * max(0.0, side.get_right()[0] - 6.75))
        with self.voiceover(
            "With the parameters fitted to the bill rate, here are the curves each model draws from three short rates "
            "today. <bookmark mark='a'/> From half a percent, the curve slopes up. From three and from eight percent it "
            f"slopes down, toward {y_inf:.1f} percent, because the fitted long-run level is so low. CIR's, dashed, are "
            "close to Vasicek's. <bookmark mark='b'/> And all of them "
            "head to the same long yield: the short rate's influence decays with maturity, and the long end sits a "
            "little below the long-run level b, because averaging over random paths makes long bonds worth more, a "
            "convexity effect."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.5, run_time=4))
            vo.wait_until("b")
            self.play(Create(lim), FadeIn(side[1]), FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, s):
        v = s["vas"]
        ax = surf3d_axes([0, 0.1, 0.02], [0, 30, 10], [0, 0.1, 0.02], x_length=6.0, y_length=5.0, z_length=3.2)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)

        def y(r, T):
            T = max(T, 0.1)
            return float(-np.log(TS.vasicek_zcb(r, v["a"], v["b"], v["sigma"], T)) / T)
        surf = Surface(lambda u, w: ax.c2p(u, w, y(u, w)), u_range=(0.0, 0.1), v_range=(0.1, 30), resolution=(20, 24),
                       fill_opacity=0.8, stroke_width=0.4, stroke_color=GREY_D, checkerboard_colors=False)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.SPOT, 0.0), (QC.DELTA, 0.05), (QC.LOSS, 0.1)], axis=2)
        key = VGroup(label(r"short rate (across), maturity (back), zero yield (up): Vasicek", font_size=19, color=GREY_A)
                     ).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "All those curves at once: the yield surface over today's short rate and maturity. At the front edge, "
            "maturity near zero, the yield is the short rate itself, a straight diagonal. <bookmark mark='a'/> Toward "
            "the back the surface flattens out: at long maturities the short rate hardly matters. Every curve the "
            "model can ever produce is a slice of this sheet, which is its great limitation."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(Create(surf), run_time=2.5)
            vo.wait_until("a")
            self.move_camera(theta=-120 * DEGREES, run_time=5)
        self.wait(0.3)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)

    def lab(self, s):
        card = house_lab(r"the Riccati equations, solved", TS.affine_zcb, "def f(t, y):", 7, width=7.4)
        card.to_edge(LEFT, buff=0.4).to_edge(UP, buff=0.5)
        v, c = s["vas"], s["cir"]
        T = np.array([2.0, 10.0, 30.0])
        num = TS.affine_zcb(0.03, v["a"], v["b"], v["sigma"] ** 2, 0.0, T)
        cf = TS.vasicek_zcb(0.03, v["a"], v["b"], v["sigma"], T)
        numc = TS.affine_zcb(0.03, c["kappa"], c["theta"], 0.0, c["sigma"] ** 2, T)
        cfc = TS.cir_zcb(0.03, c["kappa"], c["theta"], c["sigma"], T)
        out = [rf"Vasicek P(0,2,10,30): ODE {num[0]:.6f} {num[1]:.6f} {num[2]:.6f}",
               rf"                 closed {cf[0]:.6f} {cf[1]:.6f} {cf[2]:.6f}",
               rf"CIR     P(0,2,10,30): ODE {numc[0]:.6f} {numc[1]:.6f} {numc[2]:.6f}",
               rf"                 closed {cfc[0]:.6f} {cfc[1]:.6f} {cfc[2]:.6f}"]
        with self.voiceover(
            "The House solves the Riccati equations numerically for any member of the family, with Vasicek and CIR as "
            "special cases. <bookmark mark='a'/> Run it, and the numerical solutions match both closed forms to six "
            "decimals."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, out)
        q = ask(r"in a one-factor model the 2-year and 10-year yields always move in the same direction. Why, and which "
                r"chapter of Part 18 says that is wrong?")
        with self.voiceover("In a one-factor model, the two-year and ten-year yields always move the same way. Why? And "
                            "which chapter of Part eighteen says the curve does not behave like that?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
