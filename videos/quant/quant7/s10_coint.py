from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant7.common import ALT, BAD, FC, GOOD, PART, RET, VOL, load, real_data


class Coint(VoiceoverScene, ThreeDScene):
    def construct(self):
        j = load("johansen")
        c = load("coint")
        self.card()
        self.walkers(j)
        self.basis(c)
        self.derive()
        self.yields(j)

    def card(self):
        c = chapter_card(3, r"Cointegration", r"When are two wanderers tied together?", lit=(2003,), part=PART)
        with self.voiceover("Chapter three. Cointegration."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def walkers(self, j):
        D, G, gap = np.asarray(j["drunk"]), np.asarray(j["dog"]), np.asarray(j["gap"])
        lo, hi = np.minimum(D.min(0), G.min(0)) - 0.5, np.maximum(D.max(0), G.max(0)) + 0.5
        g = axes([lo[0], hi[0]], [lo[1], hi[1]], x_length=7.0, y_length=6.0, xticks=[], yticks=[], font_size=14)
        g.to_edge(LEFT, buff=0.4).shift(DOWN * 0.2)
        ax = g.ax
        n = len(D)
        tr = ValueTracker(1)

        def trail(P, col):
            def mk():
                k = int(tr.get_value())
                pts = [ax.c2p(*p) for p in P[max(0, k - 120):k + 1]]
                return VMobject(stroke_width=2.5, stroke_color=col, stroke_opacity=0.7).set_points_as_corners(
                    pts if len(pts) > 1 else pts * 2)
            return always_redraw(mk)

        drunk = always_redraw(lambda: Dot(ax.c2p(*D[int(tr.get_value())]), radius=0.12, color=RET))
        dog = always_redraw(lambda: Dot(ax.c2p(*G[int(tr.get_value())]), radius=0.09, color=GOOD))
        leash = always_redraw(lambda: DashedLine(ax.c2p(*D[int(tr.get_value())]), ax.c2p(*G[int(tr.get_value())]),
                                                 color=GREY_B, stroke_width=2, dash_length=0.06))
        leg = legend([(RET, r"the drunk: a random walk"), (GOOD, r"her dog: a random walk, pulled toward her")],
                     font_size=19)
        gg = axes([0, n], [0, 3], x_length=5.0, y_length=1.8, xticks=[], yticks=[0, 1, 2, 3],
                  ylabel=r"leash length (stationary)", font_size=14)
        gx = axes([0, n], [lo[0], hi[0]], x_length=5.0, y_length=1.8, xticks=[], yticks=[],
                  ylabel=r"east--west position of each (each wanders)", font_size=14)
        side = VGroup(leg, gx, gg).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        lx1 = tracing(gx.ax, np.arange(n), D[:, 0], tr, RET, stroke_width=2)
        lx2 = tracing(gx.ax, np.arange(n), G[:, 0], tr, GOOD, stroke_width=2)
        lg = tracing(gg.ax, np.arange(n), np.minimum(gap, 3), tr, ALT, stroke_width=2)
        src = label(r"simulated; after Murray (1994), \textit{The American Statistician} 48(1)", font_size=16,
                    color=GREY_C).to_corner(DR, buff=0.2)
        with self.voiceover(
            "In 1994 Michael Murray explained cointegration with a drunk and her dog. The drunk wanders home: a "
            "random walk. Her dog wanders too. <bookmark mark='a'/> But the dog keeps trotting back toward her. Follow either one and it drifts anywhere: a unit root. "
            f"<bookmark mark='b'/> But the leash, the distance between them, stays short. On this simulation the "
            f"Dickey-Fuller test on her position gives {j['adf_drunk']:.1f}, a unit root; on the gap between them, "
            f"{j['adf_gap']:.1f}, decisively stationary. Two series with unit roots whose combination is stationary are "
            "cointegrated."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg), FadeIn(gx), FadeIn(gg), FadeIn(src))
            self.add(trail(D, RET), trail(G, GOOD), leash, drunk, dog, lx1, lx2, lg)
            vo.wait_until("a")
            self.play(tr.animate.set_value(n * 0.55), run_time=max(vo.until("b") - 0.2, 2), rate_func=linear)
            self.play(tr.animate.set_value(n - 1), run_time=max(vo.remaining(1.0) - 0.4, 3), rate_func=linear)
        self.wait(0.3)
        self.clear_scene()

    def basis(self, c):
        t, bp = np.asarray(c["t"]), np.asarray(c["basis_bp"])
        g = axes([2020, 2021], [-80, 40], x_length=6.0, y_length=4.0, ylabel=r"perpetual minus spot, basis points",
                 xticks=[2020, 2020.5, 2021], xfmt=lambda u: {2020: "Jan", 2020.5: "Jul", 2021: "Jan"}[round(u * 2) / 2],
                 yticks=[-80, -40, 0, 40], font_size=18).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        line = curve(ax, t, np.clip(bp, -80, 40), VOL, stroke_width=2.5)
        k = int(np.argmin(bp))
        crash = label(rf"{bp[k]:.0f} bp: 12 March", font_size=18, color=BAD).next_to(ax.c2p(t[k], -80), RIGHT, buff=0.1)
        rho = c["rho"]
        side = VGroup(
            MathTex(r"\log F_t = a + b \log S_t + u_t", font_size=32),
            MathTex(rf"\text{{ADF on each: }} t = {c['adf_spot_t']:.2f},\ {c['adf_fut_t']:.2f}", font_size=26, color=GREY_A),
            MathTex(rf"\text{{on the residual: }} t = {c['eg_t']:.1f} \ (5\%: -3.34)", font_size=28, color=GOOD),
            MathTex(rf"u_t = {rho:.2f}\,u_{{t-1}} + e_t:\ \text{{half-life }} {c['half_life_days']:.1f}\text{{ days}}",
                    font_size=28, color=VOL),
            label(rf"an independent walk against Bitcoin: $t = {c['fake_t']:.1f}$, not cointegrated", font_size=21,
                  color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.4)
        pc = pause_card(r"The basis is $-20$ bp today. What do you expect tomorrow?", width=5.6, font_size=22)
        pc.next_to(side, DOWN, buff=0.3).align_to(side, LEFT)
        src = real_data(r"Binance BTCUSDT spot and USD-M perpetual, daily closes, 2020")
        with self.voiceover(
            "A real leash. Bitcoin's spot price and its perpetual future each have a unit root. <bookmark mark='a'/> "
            "But the gap between them, the basis, does not wander: here it is through 2020, in basis points, snapping "
            "back toward zero even after the crash of the twelfth of March. Robert Engle and Clive Granger made this "
            "a test in 1987: regress one on the other, and test the residual for a unit root. It rejects decisively. "
            "<bookmark mark='b'/> Pause and predict: the basis is minus twenty basis points today. What do you expect "
            f"tomorrow? The fitted autoregression says {rho:.2f} times that, about {20 * rho:.0f} basis points: half "
            "the gap closes in about a day. The leash is arbitrage, and Part two's funding rate is the hand that pulls "
            "it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            self.play(FadeIn(crash), FadeIn(side[2]), FadeIn(side[4]))
            vo.wait_until("b")
            self.play(FadeIn(pc))
            self.play(FadeIn(side[3]))
        self.wait(0.3)
        self.clear_scene()

    def derive(self):
        rows = [
            cmath(r"y_t - \beta x_t", r"=", r"u_t \sim I(0),\quad x_t, y_t \sim I(1)", font_size=36),
            cmath(r"\Delta y_t", r"=", r"\alpha_y\,(y_{t-1} - \beta x_{t-1}) + \textstyle\sum\gamma_i\Delta x_{t-i} + e_t",
                  font_size=36),
            cmath(r"t_{EG}", r"<", r"-3.34 \quad(\text{not } -2.86)", font_size=36),
            cmath(r"\Delta X_t", r"=", r"\Pi X_{t-1} + \textstyle\sum_i\Gamma_i\Delta X_{t-i} + \varepsilon_t,\quad "
                  r"\Pi = \alpha\beta'", font_size=36),
            cmath(r"\lambda_{trace}(r)", r"=", r"-T\sum_{i>r}\ln(1 - \hat\lambda_i)", font_size=36),
        ]
        whys = [why(r"the definition: a combination of wanderers that does not wander"),
                why(r"Granger's representation theorem: cointegrated $\Leftrightarrow$ an error-correction model"),
                why(r"$\hat\beta$ was chosen to make $u$ look stationary, so the bar is higher (MacKinnon)"),
                why(r"many series: the levels enter through a matrix of reduced rank $r$ (Johansen 1991)"),
                why(r"$\hat\lambda_i$: squared canonical correlations of $\Delta X_t$ and $X_{t-1}$; test $r = 0, 1, \ldots$")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=-2.4, buff=0.55, edge=6.9)
        with self.voiceover(
            "The algebra. Two series are cointegrated when each has a unit root but some combination of them is "
            "stationary. <bookmark mark='a'/> Granger's representation theorem says that is the same as an error-"
            "correction model: each period, at least one series moves to close a fraction alpha of yesterday's gap. "
            "<bookmark mark='b'/> The residual test needs its own critical value, minus three point three four: beta "
            "was chosen to make the residual look stationary. <bookmark mark='c'/> With "
            "more than two series, Soren Johansen wrote the system in levels and differences: the levels enter only "
            "through a matrix pi of reduced rank. <bookmark mark='d'/> Its rank, the number of independent leashes, "
            "is read from the canonical correlations between the changes and the lagged levels, by the trace test."
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
        self.wait(0.3)
        self.clear_scene()

    def yields(self, j):
        X = np.asarray(j["X"])
        ax3 = ThreeDAxes(x_range=[0, 10, 2], y_range=[0, 10, 2], z_range=[0, 10, 2], x_length=4.2, y_length=4.2,
                         z_length=4.2, axis_config={"stroke_color": GREY_C, "include_ticks": False})
        cols = [interpolate_color(ManimColor(RET), ManimColor(BAD), f) for f in np.linspace(0, 1, len(X))]
        pts = VGroup(*[Dot(ax3.c2p(*p), radius=0.03, color=c_).set_opacity(0.8) for p, c_ in zip(X, cols)])
        V = np.asarray(j["pca_vec"])
        mu = np.asarray(j["mean"])
        sd = np.sqrt(np.asarray(j["pca_var"]))
        arrows = VGroup(*[Line(ax3.c2p(*(mu - L * v)), ax3.c2p(*(mu + L * v)), color=c_, stroke_width=5)
                          for v, L, c_ in zip(V.T, (4.5, 1.6, 1.0), (GOOD, ALT, BAD))])
        tr, cr = np.asarray(j["trace"]), np.asarray(j["crit5"])
        rows = VGroup(*[MathTex(rf"r \le {r_}:\ {tr[r_]:.1f}\ \ (5\%: {cr[r_]:.1f})", font_size=26,
                                color=BAD if tr[r_] > cr[r_] else GOOD) for r_ in range(3)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rank = j["rank"]
        b = np.asarray(j["beta"])[:, 0]
        b = b / np.abs(b).max()
        panel = VGroup(label(r"Johansen trace test, daily yields 1990--2020", font_size=20, color=GREY_A), rows,
                       label(rf"rank {rank}: {rank} leash" + ("" if rank == 1 else "es") + rf", {3 - rank} common trend"
                             + ("" if 3 - rank == 1 else "s"), font_size=22, color=VOL),
                       MathTex(rf"\beta' = ({b[0]:+.2f},\ {b[1]:+.2f},\ {b[2]:+.2f})", font_size=26, color=BAD),
                       label(rf"principal axes: {100 * j['pca_var'][0]:.1f}\%, {100 * j['pca_var'][1]:.1f}\%, "
                             rf"{100 * j['pca_var'][2]:.2f}\% of the variance", font_size=18, color=GREY_B))
        panel.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UL, buff=0.3)  # the axes swing into the upper right
        leg = legend([(GOOD, r"level: the common trend"), (ALT, r"slope"), (BAD, r"curvature: the thin direction")],
                     font_size=18).to_corner(DL, buff=0.3)
        src = real_data(r"FRED DTB3, DGS5, DGS10, daily 1990--2020 (every tenth day drawn)")
        alabs = VGroup(*[label(s_, font_size=18, color=GREY_B).move_to(ax3.c2p(*p_))
                         for s_, p_ in ((r"3-month", (11.4, 0, 0)), (r"5-year", (0, 11.4, 0)), (r"10-year", (0, 0, 11.0)))])
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES, zoom=0.78)
        self.add_fixed_in_frame_mobjects(panel, leg, src)
        self.add_fixed_orientation_mobjects(*alabs)
        for m in (*panel, leg, src, *alabs):
            m.set_opacity(0)
        slope = V[:, 1]
        phi_e = float(np.degrees(np.arccos(abs(slope[2]))))
        theta_e = float(np.degrees(np.arctan2(slope[1] * np.sign(slope[2]), slope[0] * np.sign(slope[2]))))
        hag = ("Our three yields share two common trends, the level and the slope, and one leash. "
               if rank == 1 else "Here the test finds a different structure from the classic one. ")
        with self.voiceover(
            f"Johansen's test, made visible. Every day from 1990 to 2020, the three-month, five-year and ten-year Treasury "
            f"yields as one point in three dimensions, blue to red through time. <bookmark mark='a'/> Each yield wanders: "
            f"the cloud stretches along one long direction, the level of rates, falling for thirty years. <bookmark mark='b'/> "
            f"Turn the camera until the cloud is seen edge-on. It is almost flat: a sheet, thin in one direction. The "
            f"thin direction is a combination of yields that does not wander, the curve's curvature, a leash. <bookmark "
            f"mark='c'/> The trace test agrees. {hag}In 1992 Hall, Anderson and Granger found Treasury bill yields of "
            f"different maturities cointegrated. Yield-curve factors return in Part nineteen, and pairs trading on cointegration "
            f"in Part thirty-three."
            " Some relations are not stable but switch. Next: hidden regimes."
        ) as vo:
            self.play(Create(ax3), *[m.animate.set_opacity(1) for m in alabs], run_time=1)
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.002, run_time=3), src.animate.set_opacity(1))
            vo.wait_until("a")
            self.play(Create(arrows[0]), leg[0].animate.set_opacity(1))
            self.move_camera(theta=-20 * DEGREES, run_time=2)
            vo.wait_until("b")
            self.move_camera(phi=phi_e * DEGREES, theta=theta_e * DEGREES, run_time=3)
            self.play(Create(arrows[1]), Create(arrows[2]), leg[1].animate.set_opacity(1), leg[2].animate.set_opacity(1))
            vo.wait_until("c")
            self.play(*[m.animate.set_opacity(1) for m in panel])
        self.wait(0.3)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)
