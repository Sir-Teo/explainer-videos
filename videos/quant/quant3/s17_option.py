from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import valuation
from videos.quant.quant3.common import DEBT, EQUITY, PART, VALUE, load

F_, T_, SA, R_ = 80.0, 5.0, 0.25, 0.02


class EquityOption(VoiceoverScene, ThreeDScene):
    def construct(self):
        m = load("merton")
        self.card()
        self.payoff()
        self.surfaces(m)
        self.overhang(m)
        self.real_option()

    def card(self):
        c = chapter_card(12, r"Equity as a call", r"Who gains when the owners gamble?", lit=(1974,), part=PART)
        with self.voiceover("Chapter twelve. Equity as a call: debt overhang, risk-shifting, and real options."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def payoff(self):
        A = np.linspace(1, 200, 200)
        m = valuation.merton_equity(A, F_, T_, SA, R_)
        g = axes([0, 200], [0, 200], x_length=6.0, y_length=4.8, xlabel=r"value of the firm's assets $A$",
                 ylabel=r"value of the claim", xticks=[0, 80, 200], yticks=[0, 80, 200], font_size=18)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        pay = curve(ax, [0, F_, 200], [0, 0, 200 - F_], GREY_B, stroke_width=2.5)
        eq = curve(ax, A, m["equity"], EQUITY, stroke_width=4)
        dpay = curve(ax, [0, F_, 200], [0, F_, F_], GREY_C, stroke_width=2)
        dv = curve(ax, A, m["debt"], DEBT, stroke_width=3.5)
        leg = legend([(GREY_B, r"equity at the debt's maturity: $\max(A - F, 0)$"),
                      (EQUITY, r"equity now: a call on the assets"),
                      (DEBT, r"debt now: riskless debt minus a put")], font_size=21)
        rows = VGroup(
            cmath(r"E", r"=", r"A\,N(d_1) - F e^{-rT} N(d_2)", font_size=34, colors={r"E": EQUITY}),
            cmath(r"D", r"=", r"F e^{-rT} - \text{Put}(A, F)", font_size=34, colors={r"D": DEBT}),
            cmath(r"\frac{\partial E}{\partial \sigma_A}", r"=", r"\text{vega} > 0", font_size=34,
                  colors={r"\frac{\partial E}{\partial \sigma_A}": EQUITY}),
            label(rf"debt of {F_:.0f} due in {T_:.0f} years; asset volatility {100 * SA:.0f}\%", font_size=19,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        VGroup(leg, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "One more way to see a share. A firm has assets worth A and owes F, due in five years. When the debt comes "
            "due, the owners pay it if the assets are worth more and keep the rest; if not, they hand the firm to the "
            "lenders and walk away, because their liability is limited. <bookmark mark='a'/> That payoff is a call "
            "option on the firm's assets, struck at the debt. Before maturity, equity is worth what a call is worth: "
            "Black and Scholes noticed this in 1973, and Robert Merton built a theory of corporate debt on it in "
            "1974. Part ten derives the formula. <bookmark mark='b'/> And the debt is riskless debt minus a put: the "
            "lenders have sold the owners the right to default. <bookmark mark='c'/> One derivative carries the rest "
            "of this chapter: a call is worth more when volatility rises."
        ) as vo:
            self.play(FadeIn(g), Create(pay), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(eq), FadeIn(leg[1]), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(dpay), Create(dv), FadeIn(leg[2]), FadeIn(rows[1]), FadeIn(rows[3]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.wait(0.4)
        self.clear_scene()

    def surfaces(self, m):
        F, T, r = m["F"], m["T"], m["r"]
        ax = ThreeDAxes(x_range=[20, 200, 40], y_range=[0.1, 0.6, 0.1], z_range=[0, 180, 40], x_length=7.0,
                        y_length=4.6, z_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.6 + RIGHT * 0.4)

        def E(a, s):
            return float(valuation.merton_equity(a, F, T, s, r)["equity"])

        def D(a, s):
            return float(valuation.merton_equity(a, F, T, s, r)["debt"])

        se = Surface(lambda u, v: ax.c2p(u, v, E(u, v)), u_range=[20, 200], v_range=[0.1, 0.6], resolution=(18, 10),
                     fill_opacity=0.75, stroke_width=0.4, stroke_color=BLACK, checkerboard_colors=[EQUITY, EQUITY])
        sd = Surface(lambda u, v: ax.c2p(u, v, D(u, v)), u_range=[20, 200], v_range=[0.1, 0.6], resolution=(18, 10),
                     fill_opacity=0.6, stroke_width=0.4, stroke_color=BLACK, checkerboard_colors=[DEBT, DEBT])
        a0, s0 = m["a0"], m["s0"]
        s = ValueTracker(s0)
        ball_e = always_redraw(lambda: Dot3D(ax.c2p(a0, s.get_value(), E(a0, s.get_value())), radius=0.11,
                                             color=WHITE))
        ball_d = always_redraw(lambda: Dot3D(ax.c2p(a0, s.get_value(), D(a0, s.get_value())), radius=0.11,
                                             color=GREY_A))
        hint = VGroup(label(r"assets $A$: 20 to 200 (debt due 80 in a year)", font_size=21, color=VALUE),
                      label(r"asset volatility $\sigma_A$: 10\% to 60\%", font_size=21, color=QC.IMPLIED),
                      label(r"equity (magenta) and debt (blue)", font_size=21, color=GREY_A))
        hint.arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.4)
        rd = VGroup(MathTex(rf"\sigma_A\ {100 * s0:.0f}\% \to {200 * s0:.0f}\%:", font_size=28),
                    MathTex(rf"\text{{equity}}\ {m['e0']:.2f} \to {m['e_risky']:.2f}", font_size=28, color=EQUITY),
                    MathTex(rf"\text{{debt}}\ {m['d0']:.2f} \to {m['d_risky']:.2f}", font_size=28, color=DEBT),
                    MathTex(rf"\text{{total}}\ {m['e0'] + m['d0']:.2f} = {m['e_risky'] + m['d_risky']:.2f}",
                            font_size=28, color=QC.GAIN))
        rd.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.4)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-125 * DEGREES, zoom=0.8)
        self.add_fixed_in_frame_mobjects(hint, rd)
        self.remove(hint, rd)
        with self.voiceover(
            "Here are both claims as surfaces over two inputs: the value of the assets, and their volatility, with "
            "eighty of debt due in a year. Equity is the upper sheet, debt the lower one, and at every point they add "
            "up to the assets. <bookmark mark='a'/> Put a firm near default: assets of sixty against debt of eighty. "
            "<bookmark mark='b'/> Now let the owners gamble, doubling the volatility of the assets without changing "
            "their value. The firm's ball on the equity sheet climbs; the one on the debt sheet sinks by exactly the "
            f"same amount. Equity goes from {m['e0']:.2f} to {m['e_risky']:.2f}, debt from {m['d0']:.2f} to "
            f"{m['d_risky']:.2f}. <bookmark mark='c'/> Nothing was created: value moved from lenders to owners. This is "
            "risk-shifting, or asset substitution, which Jensen and Meckling described in 1976, and it is why loan "
            "agreements are full of covenants."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.5)
            self.play(Create(se), Create(sd), run_time=3)
            vo.wait_until("a")
            self.add(ball_e, ball_d)
            self.play(FadeIn(rd[0]))
            vo.wait_until("b")
            self.play(s.animate.set_value(2 * s0), run_time=4)
            self.play(FadeIn(rd[1:3]))
            vo.wait_until("c")
            self.play(FadeIn(rd[3]))
            self.move_camera(theta=-60 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.0))
        ball_e.clear_updaters()
        ball_d.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, se, sd, ball_e, ball_d)),
                                                                  FadeOut(hint), FadeOut(rd)], run_time=1.5)
        self.clear_scene()

    def overhang(self, m):
        rows = VGroup(
            label(rf"assets {m['a0']:.0f}, debt of {m['F']:.0f} due in a year, volatility {100 * m['s0']:.0f}\%",
                  font_size=24, color=GREY_A),
            label(rf"a project: the owners put in {m['cost']:.0f}, it adds {m['gain']:.0f} to the assets: "
                  rf"NPV $+{m['gain'] - m['cost']:.0f}$", font_size=24, color=GREY_A),
            MathTex(rf"\Delta E = {m['e1']:.2f} - {m['e0']:.2f} = {m['e1'] - m['e0']:.2f}\ <\ {m['cost']:.0f}",
                    font_size=34, color=EQUITY),
            MathTex(rf"\Delta D = {m['d1']:.2f} - {m['d0']:.2f} = {m['d1'] - m['d0']:.2f}", font_size=34, color=DEBT),
            wrapped_label(r"the owners pay the whole cost and the lenders collect most of the gain: a good project "
                          r"is refused (Myers 1977, debt overhang)", 10.0, 24, QC.LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.6)
        pp = desk_question(r"Pause and predict: near default, the owners can double the firm's volatility at no cost. "
                           r"Do they? Who pays?", width=10.0, font_size=22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The same arithmetic runs in reverse. Stewart Myers pointed out in 1977 that a firm burdened with debt "
            "can refuse good projects. The same firm, assets of sixty against eighty of debt, is offered a project: "
            f"the owners put in {m['cost']:.0f} and it adds {m['gain']:.0f} to the assets, a positive net present "
            f"value. <bookmark mark='a'/> But the equity, the call, rises by only {m['e1'] - m['e0']:.2f}. The owners "
            f"pay {m['cost']:.0f} and get {m['e1'] - m['e0']:.2f}; the lenders get {m['d1'] - m['d0']:.2f} for nothing. "
            "<bookmark mark='b'/> So the owners say no, and value that could have existed never does. That is debt "
            "overhang. Pause and predict the mirror image: if the same owners could double the volatility for free, "
            "would they? Yes, and the lenders would pay."
        ) as vo:
            self.play(FadeIn(rows[:2]))
            vo.wait_until("a")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[4]), FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()

    def real_option(self):
        V = np.linspace(40, 160, 121)
        K, T, s, r = 100.0, 2.0, 0.35, 0.03
        call = np.asarray(valuation.merton_equity(V, K, T, s, r)["equity"])
        npv = V - K
        g = axes([40, 160], [-60, 70], x_length=6.6, y_length=4.4, xlabel=r"value of the project today",
                 ylabel=r"value of the opportunity", xticks=[50, 100, 150], yticks=[-50, 0, 50], font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        l_npv = curve(ax, V, npv, GREY_B, stroke_width=3)
        l_opt = curve(ax, V, call, QC.OPTION, stroke_width=4)
        leg = legend([(GREY_B, r"invest now: NPV $= V - 100$"),
                      (QC.OPTION, r"the right to invest within two years: a call")], font_size=20)
        side = VGroup(leg,
                      wrapped_label(r"the option is worth more than investing now, so waiting has value; NPV alone "
                                    r"undervalues flexibility (Myers 1977; Dixit and Pindyck 1994)", 4.8, 21, GREY_A),
                      label(r"illustrative: cost 100, volatility 35\%, two years, rate 3\%", font_size=18,
                            color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The option view also works for good news. A project that can be delayed is a call on the project's "
            "value, struck at its cost. Investing today is exercising early, and earns only the grey line, value "
            "minus cost. <bookmark mark='a'/> The right to wait is the magenta curve, always above it, most of all "
            "near the money, when you are least sure. Myers called these real options; they are why NPV alone "
            "undervalues a firm's flexibility, and why a firm's equity can be worth more than its projects' plain "
            "present values."
        ) as vo:
            self.play(FadeIn(g), Create(l_npv), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(l_opt), FadeIn(leg[1]), run_time=2)
            self.play(FadeIn(side[1:]))
        self.wait(0.4)
        self.clear_scene()
