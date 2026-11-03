from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import CASH, GAIN, OPT, PART, SPOT, THE, computed, load


class American(VoiceoverScene, ThreeDScene):
    def construct(self):
        d = load("tree")
        self.card()
        self.calls()
        self.puts(d)
        a = load("american_more")
        self.premium3d(a)
        self.free_boundary(a)
        self.approximations(a)

    def card(self):
        c = chapter_card(14, r"Early exercise and the free boundary", r"When should you stop waiting?", lit=(1979,),
                         part=PART)
        with self.voiceover("Chapter fourteen. Early exercise and the free boundary."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def calls(self):
        rows = VGroup(
            MathTex(r"C_{\text{American}}", r"\;\ge\;", r"C_{\text{European}}", r"\;\ge\;", r"S - K e^{-rT}",
                    r"\;>\;", r"S - K", font_size=42),
            label(r"alive, a call is worth more than exercised: never exercise early (no dividends)",
                  font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.4).shift(UP * 1.3)
        rows[0][2].set_color(OPT)
        rows[0][4].set_color(CASH)
        rows[0][6].set_color(GAIN)
        put = VGroup(
            MathTex(r"P_{\text{American}} = \max\big(\,K - S,\ \text{value of waiting}\,\big)", font_size=40,
                    color=OPT),
            label(r"a deep put: exercise, take $K$ now, and earn interest on it", font_size=28, color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(rows, DOWN, buff=0.9)
        with self.voiceover(
            "European options are exercised only at expiry; most stock options are American, exercisable any day. "
            "For a call on a stock without dividends the right is worthless: parity bounds the call below by the "
            "stock minus the discounted strike, more than the stock minus the strike. Merton, 1973. "
            "<bookmark mark='a'/> A put is different: exercising a deep one hands you the strike now, to earn "
            "interest on. At some price stopping beats waiting: optimal stopping, Part eight's subject, with no "
            "closed form at finite maturity."
        ) as vo:
            self.play(Write(rows[0]), run_time=2)
            self.play(FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(put, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def puts(self, d):
        spots = np.asarray(d["spots"], float)
        am, eu = np.asarray(d["am_curve"], float), np.asarray(d["eu_curve"], float)
        g = axes([60, 140], [0, 42], x_length=7.6, y_length=4.4, xlabel=r"stock price $S$",
                 ylabel=r"put value, one year to expiry", xticks=[60, 80, 100, 120, 140], yticks=[0, 20, 40],
                 font_size=20).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        payoff = curve(ax, [60, 100, 140], [40, 0, 0], GREY_B, stroke_width=2.5)
        eu_l = curve(ax, spots, eu, THE, stroke_width=3.5)
        am_l = curve(ax, spots, am, OPT, stroke_width=4)
        prem = Polygon(*[ax.c2p(s, a) for s, a in zip(spots, am)], *[ax.c2p(s, e) for s, e in zip(spots[::-1],
                                                                                                eu[::-1])],
                       stroke_width=0, fill_color=OPT, fill_opacity=0.25)
        leg = legend([(OPT, r"American (tree, 600 steps)"), (THE, r"European (formula)"),
                      (GREY_B, r"exercise now: $K - S$")], font_size=22).next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        nums = VGroup(
            label(r"at $S = K = 100$:", font_size=26, color=GREY_A),
            MathTex(rf"\text{{American}}\ {d['american_put']:.4f}", font_size=32, color=OPT),
            MathTex(rf"\text{{European}}\ {d['european_put']:.4f}", font_size=32, color=THE),
            MathTex(rf"\text{{early-exercise premium}}\ {d['american_put'] - d['european_put']:.4f}", font_size=28,
                    color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(leg, DOWN, buff=0.6).align_to(leg, LEFT)
        params = note(r"$K = 100$, $T = 1$, $\sigma = 20\%$, $r = 5\%$", font_size=20).to_corner(DR, buff=0.3)
        with self.voiceover(
            "The tree of chapter five solves it, with its one extra line: each node is worth the larger of "
            "exercising now and waiting. A one-year put, five percent interest rate. The European put, in blue, "
            "dips below its payoff for deep prices: alive, it is worth less than exercised, because of the "
            "interest. <bookmark mark='a'/> The American put, in magenta, never does: it meets the payoff and runs "
            f"along it. At the money it is worth {d['american_put']:.4f} against the European "
            f"{d['european_put']:.4f}: an early-exercise premium of "
            f"{d['american_put'] - d['european_put']:.2f}, the shaded gap."
        ) as vo:
            self.play(FadeIn(g), Create(payoff), FadeIn(params), FadeIn(leg[2]))
            self.play(Create(eu_l), FadeIn(leg[1]))
            vo.wait_until("a")
            self.play(Create(am_l), FadeIn(leg[0]))
            self.play(FadeIn(prem), FadeIn(nums, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def premium3d(self, a):
        sp, ta, P = np.asarray(a["spots"], float), np.asarray(a["taus"], float), np.asarray(a["premium"], float)
        bt, bs_ = np.asarray(a["b_times"], float), np.asarray(a["b_smooth"], float)
        zmax = 6.0
        ax = ThreeDAxes(x_range=[60, 140, 20], y_range=[0, 1, 0.25], z_range=[0, zmax, 2], x_length=7.6, y_length=5.4,
                        z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.5 + RIGHT * 0.8)  # the axis key keeps the upper-left corner

        def f(s_, t_):
            col = np.array([np.interp(t_, ta, P[:, j]) for j in range(len(sp))])
            return float(min(max(np.interp(s_, sp, col), 0.0), zmax))

        surf = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=[60, 140], v_range=[ta[0], 1.0],
                       resolution=(32, 20))
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.Q, 0), (OPT, 1.5), (WHITE, zmax)], axis=2)
        surf.set_style(fill_opacity=0.65, stroke_width=0.3, stroke_color=GREY_D)
        ok = np.isfinite(bs_) & (bt > 0.002)
        tau_b = 1.0 - bt[ok]
        Sb = bs_[ok]
        sel = np.linspace(0, len(Sb) - 1, 80).astype(int)
        gold = VMobject(stroke_color=YELLOW, stroke_width=6).set_points_smoothly(
            [ax.c2p(Sb[i], tau_b[i], f(Sb[i], tau_b[i]) + 0.05) for i in sel if tau_b[i] >= ta[0]])
        hint = VGroup(label(r"stock price $S$", font_size=24, color=SPOT), label(r"time left $\tau$", font_size=24,
                                                                               color=THE),
                      label(r"early-exercise premium $P_A - P_E$", font_size=24, color=OPT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        foot = note(r"600-step trees at every point; gold: the free boundary $S^*(\tau)$", font_size=20)
        foot.to_corner(DR, buff=0.3)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-60 * DEGREES, zoom=0.85)
        for m in (hint, foot):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        with self.voiceover(
            "Here is the whole early-exercise premium, the American put minus the European, over the stock price "
            "and the time left, from a tree at every point. Far above the strike it is zero: no one exercises a "
            "put that is out of the money. <bookmark mark='a'/> It grows as the stock falls, and below a certain "
            "price it becomes exactly the gap between exercising now and the European value. The gold curve, where "
            "the shape changes, is the free boundary: the stock price at which exercise becomes optimal, for each "
            "time left. It rises to the strike as expiry approaches, and falls away from it the longer there is to "
            "wait."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), FadeIn(foot), run_time=1.5)
            self.play(FadeIn(surf), run_time=2)
            vo.wait_until("a")
            self.play(Create(gold), run_time=2)
            self.move_camera(theta=-25 * DEGREES, phi=60 * DEGREES, run_time=max(vo.remaining(1.0) - 0.5, 1.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)]))], run_time=1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def free_boundary(self, a):
        C = {r"P": OPT, r"S^*": GAIN, r"K": QC.STRIKE, r"r": CASH}
        rows = [
            cmath(r"P(t, S)", r"=", r"\sup_{\tau}\,\mathbb E^{\mathbb Q}\big[e^{-r(\tau - t)}(K - S_\tau)^+\big]",
                  font_size=32, colors=C),
            cmath(r"P_t + rSP_S + \tfrac12\sigma^2S^2P_{SS} - rP = 0\ \ (S > S^*),", r"\quad",
                  r"P = K - S\ \ (S \le S^*)", font_size=30, colors=C),
            cmath(r"P(t, S^*) = K - S^*,", r"\quad", r"P_S(t, S^*) = -1", font_size=32, colors=C),
            cmath(r"(\partial_t + \mathcal L - r)(K - S)", r"=", r"-rK", font_size=32, colors=C),
            cmath(r"P_A", r"=", r"P_E + \int_0^T rK e^{-rs}\,N\big(-d_2(S_0, S^*(s), s)\big)\,ds", font_size=32,
                  colors=C),
        ]
        whys = [why(r"optimal stopping (Part 8)"),
                why(r"wait: the equation holds; stop: the payoff holds"),
                why(r"value matching and smooth pasting (Part 8's smooth fit)"),
                why(r"in the stopping region the put loses the interest on the strike"),
                why(r"It\^o on $e^{-rt}P$: Kim (1990); Jacka (1991); Carr, Jarrow, Myneni (1992)")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-1.6, buff=0.6, edge=6.9)
        gap = a["kim"] - a["tree"]
        gap_line = ("within a hundredth." if abs(gap) < 0.01 else
                    f"a gap of {abs(gap):.3f}, the boundary's remaining error.")
        with self.voiceover(
            "In symbols: optimal stopping. <bookmark mark='a'/> Above the boundary the equation holds; below it, "
            "the payoff. <bookmark mark='b'/> Across it value and slope join: Part eight's smooth fit. "
            "<bookmark mark='c'/> Plug the payoff into the equation in the stopping region and out comes minus r "
            "K: the interest on the strike. <bookmark mark='d'/> Ito on the discounted put, take expectations, and "
            "the premium is that interest, earned whenever the put would sit exercised, weighted by the chance of "
            "being below the boundary: In-Joon Kim, 1990; Carr, Jarrow and Myneni, 1992. With the tree's boundary, "
            f"located between nodes, the integral gives {a['kim']:.4f} against the tree's {a['tree']:.4f}: "
            + f"{gap_line} Pause and predict: rates go to zero; where does the boundary go? To zero."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
            self.play(FadeIn(computed()))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def approximations(self, a):
        sp, bc = np.asarray(a["spots"], float), np.asarray(a["baw_curve"], float)
        cards = VGroup(
            history_card(1977, r"Brennan and Schwartz", r"the first finite-difference solution of the American put "
                         r"(Part 16 solves it as a complementarity problem)", width=4.2, font_size=22),
            history_card(1987, r"Barone-Adesi and Whaley", r"drop the early-exercise term's time derivative: a "
                         r"quadratic, solved at the critical price", width=4.2, font_size=22),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).to_edge(LEFT, buff=0.4).shift(UP * 0.5)
        nums = VGroup(
            label(r"one-year at-the-money put, $r = 5\%$, $\sigma = 20\%$:", font_size=24, color=GREY_A),
            MathTex(rf"\text{{tree}}\ {a['tree']:.4f}", font_size=30, color=OPT),
            MathTex(rf"\text{{Kim's integral}}\ {a['kim']:.4f}", font_size=30, color=OPT),
            MathTex(rf"\text{{Barone-Adesi--Whaley}}\ {a['baw']:.4f}", font_size=30, color=GAIN),
            MathTex(rf"\text{{critical price: BAW}}\ {a['baw_critical']:.1f},\ \text{{tree}}\ {a['smooth_critical']:.1f}",
                    font_size=28, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 1.0)
        dv = a["div"]
        div = wrapped_label(
            rf"An American call, strike {dv['K']:.0f}, with one dividend of {dv['D']:.0f} at {12 * dv['tD']:.1f} months: "
            rf"worth {dv['american']:.3f} against {dv['european']:.3f} European, and every exercise node in the tree "
            rf"sits in the last step before the dividend.", 6.0, 22, GREY_A)
        div.next_to(nums, DOWN, buff=0.4).align_to(nums, LEFT)
        before = (dv["last_t"] < dv["tD"]) and (dv["tD"] - dv["first_t"] < 0.01)
        div_line = ("With one cash dividend the tree exercises a call only in the instant before the stock goes "
                    "ex-dividend." if before else
                    "With one cash dividend the tree's call exercise nodes cluster before the dividend date.")
        with self.voiceover(
            "Desks once needed something quicker than a tree. Brennan and Schwartz solved the put by finite "
            "differences in 1977, Part sixteen's method. <bookmark mark='a'/> Barone-Adesi and Whaley, 1987, "
            "dropped the premium's time derivative and solved what was left in closed form: "
            f"{a['baw']:.4f} against the tree's {a['tree']:.4f}, critical price {a['baw_critical']:.1f} against "
            f"{a['smooth_critical']:.1f}. <bookmark mark='b'/> And dividends bring calls back. {div_line}"
            " The trade around it is Part eleven's."
            " Next: the formula against real Bitcoin, selling volatility."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2), FadeIn(nums, shift=LEFT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(div))
        self.wait(0.4)
        self.clear_scene()
