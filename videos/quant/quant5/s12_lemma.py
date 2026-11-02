from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant5.common import BM, DRIFT, ITO, JUMP, PART, STRAT, load, pause


def f(t, x):
    return x ** 2 * np.exp(-t / 4)


class Lemma(VoiceoverScene, ThreeDScene):
    def construct(self):
        L = load("lemma_column")
        self.card()
        self.surface(L)
        self.misses(L)
        self.proof()
        self.consequences(L)

    def card(self):
        c = chapter_card(4, r"It\^o's lemma, proved", r"Where does the extra term come from?", part=PART)
        with self.voiceover("Chapter four. Itô's lemma, proved, and seen."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def surface(self, L):
        t = np.asarray(L["t"])
        W = np.clip(np.asarray(L["W"]), -1.5, 1.5)
        cm = np.asarray(L["cum_miss"])
        ax = ThreeDAxes(x_range=[0, 1, 0.5], y_range=[-1.5, 1.5, 0.5], z_range=[0, 2.4, 0.5], x_length=6.0,
                        y_length=5.4, z_length=3.2, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(LEFT * 1.2 + DOWN * 0.3)
        surf = loss_surface(ax, f, [0, 1], [-1.5, 1.5], resolution=(18, 30), z_lo=0, z_hi=2.3, opacity=0.55)
        pts = [ax.c2p(a, b, f(a, b)) + np.array([0, 0, 0.03]) for a, b in zip(t, W)]
        tk = ValueTracker(0)

        def lifted():
            i = int(np.clip(tk.get_value(), 1, len(pts) - 1))
            return VMobject(stroke_color=BM, stroke_width=4).set_points_as_corners(pts[:i + 1])

        def ball():
            i = int(np.clip(tk.get_value(), 0, len(pts) - 1))
            return Dot3D(pts[i], radius=0.08, color=YELLOW, resolution=(6, 6))

        def plane():
            i = int(np.clip(tk.get_value(), 0, len(t) - 2))
            a, b = t[i], W[i]
            ft, fx = -0.25 * b ** 2 * np.exp(-a / 4), 2 * b * np.exp(-a / 4)
            h, k = 0.12, 0.35
            corners = [(a + da, b + db) for da, db in ((-h, -k), (h, -k), (h, k), (-h, k))]
            return Polygon(*[ax.c2p(x, y, f(a, b) + ft * (x - a) + fx * (y - b)) for x, y in corners], stroke_width=1,
                           stroke_color=WHITE, fill_color=ITO, fill_opacity=0.45)
        base = ax.c2p(1.15, 1.5, 0)
        unit = (ax.c2p(0, 0, 1) - ax.c2p(0, 0, 0))[2]

        def column():
            i = int(np.clip(tk.get_value(), 0, len(cm) - 1))
            hgt = max(cm[i], 0.005)
            return Prism(dimensions=[0.18, 0.18, hgt * unit], fill_color=JUMP, fill_opacity=0.85,
                         stroke_width=0).move_to(base + np.array([0, 0, hgt * unit / 2]))
        ref = Line(base + np.array([-0.25, 0, L["theory"][-1] * unit]), base + np.array([0.25, 0, L["theory"][-1] * unit]),
                   color=WHITE, stroke_width=4)
        hint = VGroup(label(r"surface: $f(t, x) = x^2 e^{-t/4}$", font_size=22, color=GREY_A),
                      label(r"blue: a Brownian path lifted onto it", font_size=22, color=BM),
                      label(r"tangent plane: the first-order prediction", font_size=22, color=ITO),
                      label(r"red column: the misses, stacked", font_size=22, color=JUMP),
                      label(r"white bar: $\tfrac12\int_0^t f_{xx}\,ds$", font_size=22, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UR, buff=0.35)
        readout_ = VGroup(MathTex(r"\text{misses so far} =", font_size=28, color=JUMP),
                          DecimalNumber(0, num_decimal_places=3, font_size=28, color=JUMP)).arrange(RIGHT, buff=0.15)
        readout_.to_corner(DR, buff=0.4)
        readout_[1].add_updater(lambda m: m.set_value(cm[int(np.clip(tk.get_value(), 0, len(cm) - 1))]))
        self.set_camera_orientation(phi=65 * DEGREES, theta=-70 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        lp, bl, pl, co = always_redraw(lifted), always_redraw(ball), always_redraw(plane), always_redraw(column)
        with self.voiceover(
            "Here is the lemma as a picture: a surface, x squared times a decaying exponential, and a Brownian path "
            "lifted onto it. <bookmark mark='a'/> At each step, ordinary calculus predicts the next height from the "
            "tangent plane: the time slope times the time step, plus the space slope times the move. "
            "<bookmark mark='b'/> The surface curves upward, so the true height is always a little above the plane. "
            "Stack those misses in the red column. For a smooth path they would be of the order of the step squared, "
            "and the column would stay empty. Here it fills, steadily, toward the white bar: half the integral of the "
            "second derivative. <bookmark mark='c'/> The misses are not noise. They add up to a drift, and that drift "
            "is Itô's extra term."        ) as vo:
            self.play(Create(ax), FadeIn(surf), FadeIn(hint[:2]), run_time=2)
            self.add(lp, bl)
            vo.wait_until("a")
            self.add(pl)
            self.play(FadeIn(hint[2]), tk.animate.set_value(40), run_time=2, rate_func=linear)
            vo.wait_until("b")
            self.add(co)
            self.play(FadeIn(hint[3:]), Create(ref))
            self.play(tk.animate.set_value(len(t) - 1), run_time=max(vo.remaining(0.5) - 3.5, 4), rate_func=linear)
            self.move_camera(theta=-30 * DEGREES, phi=70 * DEGREES, run_time=3)
            vo.wait_until("c")
        for m in (lp, bl, pl, co):
            m.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, surf, lp, bl, pl, co, ref)), FadeOut(hint)],
                         run_time=1.5)
        self.clear_scene()

    def misses(self, L):
        t = np.asarray(L["t"])
        g1 = axes([0, 1], [0, 1.1], x_length=5.6, y_length=3.4, xlabel=r"time",
                  ylabel=r"stacked misses, $f = x^2 e^{-t/4}$", xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                  font_size=16)
        g2 = axes([0, 1], [-0.85, 0.1], x_length=5.6, y_length=3.4, xlabel=r"time",
                  ylabel=r"stacked misses, $f = xy$, $\rho = -0.7$", xticks=[0, 0.5, 1], yticks=[-0.7, 0],
                  font_size=16)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).shift(DOWN * 0.3)
        m1 = curve(g1.ax, t, L["cum_miss"], JUMP, stroke_width=3)
        th1 = curve(g1.ax, t, L["theory"], WHITE, stroke_width=2)
        m2 = curve(g2.ax, t, L["cum_miss2"], JUMP, stroke_width=3)
        th2 = curve(g2.ax, t, L["rho"] * t, WHITE, stroke_width=2)
        lab1 = MathTex(rf"{L['cum_miss'][-1]:.3f} \text{{ against }} \tfrac12\int_0^1 f_{{xx}}\,dt = {L['theory'][-1]:.3f}",
                       font_size=24).next_to(g1, UP, buff=0.2)
        lab2 = MathTex(rf"{L['cum_miss2'][-1]:.3f} \text{{ against }} \langle X, Y\rangle_1 = {L['rho']:.1f}",
                       font_size=24).next_to(g2, UP, buff=0.2)
        with self.voiceover(
            f"Flattened: the stacked misses end at {L['cum_miss'][-1]:.3f}, against {L['theory'][-1]:.3f}; the gap is "
            "the discretisation error of four hundred steps. <bookmark mark='a'/> With two Brownian motions "
            "correlated at minus point seven and the function x times y, the misses come from the cross term and pile "
            "up to the covariation: the product rule, seen happening."
        ) as vo:
            self.play(FadeIn(g1), Create(th1), Create(m1), FadeIn(lab1), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(th2), Create(m2), FadeIn(lab2), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        rows = [cmath(r"f(t_{k+1}, W_{k+1}) - f(t_k, W_k)", r"=", r"f_t\,\Delta t + f_x\,\Delta W + \tfrac12 f_{xx}(\Delta W)^2 + R_k",
                      font_size=32),
                cmath(r"\sum_k f_{xx}(t_k, W_k)\big[(\Delta W_k)^2 - \Delta t_k\big]", r"\to", r"0 \text{ in } L^2", font_size=32),
                cmath(r"\sum_k R_k", r"\to", r"0", font_size=32),
                cmath(r"df", r"=", r"f_t\,dt + f_x\,dW + \tfrac12 f_{xx}\,dt", font_size=36,
                      colors={r"\tfrac12 f_{xx}\,dt": JUMP}),
                cmath(r"df(X, Y)", r"=", r"f_x\,dX + f_y\,dY + \tfrac12 f_{xx}\,d\langle X\rangle + f_{xy}\,d\langle X, Y\rangle "
                      r"+ \tfrac12 f_{yy}\,d\langle Y\rangle", font_size=30),
                cmath(r"d(XY)", r"=", r"X\,dY + Y\,dX + d\langle X, Y\rangle", font_size=34)]
        whys = [why(r"Taylor to second order on each step"),
                why(r"a martingale sum: the terms are uncorrelated, each with variance $2 f_{xx}^2 \Delta t^2$, as in "
                    r"chapter 2"),
                why(r"the remainder is $o\big((\Delta W)^2\big)$ uniformly on compacts, and $\sum |\Delta W|^3 \to 0$"),
                why(r"the three sums converge: It\^o's lemma"),
                why(r"the same proof in two variables; for Brownian motions $d\langle W, B\rangle = \rho\,dt$"),
                why(r"take $f = xy$: the product rule, with its covariation term")]
        step = ladder(self, rows, whys, keep=4, top=3.2, x=-1.4, buff=0.55, edge=6.9)
        with self.voiceover(
            "Now the proof. On each step, expand the function to second order: the time slope times the time step, "
            "the space slope times the move, half the curvature times the move squared, and a remainder. "
            "<bookmark mark='a'/> Replace each squared move by its time step. The error is a sum of terms with mean "
            "zero, uncorrelated because the moves are independent, each with variance two times the curvature squared "
            "times the step squared: the same computation as for quadratic variation, so it vanishes in mean square. "
            "<bookmark mark='b'/> The remainder is smaller than the cube of the move, uniformly on bounded sets, and "
            "the sum of cubed moves goes to zero. <bookmark mark='c'/> What is left is Itô's lemma: the first-order "
            "terms, plus half the curvature times d t. <bookmark mark='d'/> With two processes, the same argument "
            "produces a cross term, the mixed derivative times the covariation, which for two Brownian motions is rho "
            "d t. <bookmark mark='e'/> And f equal to x times y gives the stochastic product rule, which solves the "
            "Ornstein-Uhlenbeck equation and proves Girsanov's theorem."
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
            vo.wait_until("e")
            step(5)
        self.wait(0.5)
        self.clear_scene()

    def consequences(self, L):
        rows = VGroup(
            MathTex(r"S_t = S_0 \exp\!\big((\mu - \tfrac12\sigma^2)t + \sigma W_t\big)", font_size=32, color=BM),
            label(rf"20{{,}}000 paths, $\mu = {L['mu']:.2f}$, $\sigma = {L['sigma']:.2f}$: "
                  rf"$\mathbb{{E}}\log S_1/S_0 = {L['mean_log']:.3f}$ against $\mu - \tfrac12\sigma^2 = "
                  rf"{L['drag_theory']:.3f}$; $\log \mathbb{{E}} S_1/S_0 = {L['log_mean']:.3f}$", font_size=22,
                  color=GREY_A),
            theorem_card(r"L\'evy's characterization", r"A continuous local martingale $M$ with $\langle M\rangle_t = t$ is "
                         r"a Brownian motion: by the lemma $e^{iuM_t + u^2 t/2}$ is a martingale, so the increments are "
                         r"Gaussian. Dambis, Dubins and Schwarz (1965): every continuous martingale is a Brownian motion "
                         r"run on the clock $\langle M\rangle_t$.", who=r"L\'evy (1948); Dambis (1965), Dubins and Schwarz "
                         r"(1965)", color=ITO, width=8.6, font_size=21),
        ).arrange(DOWN, buff=0.35).to_edge(UP, buff=0.4)
        pc, ans = pause(r"What is $\mathbb{E}[W_t^4]$?", rf"$3t^2$: $d(W^4) = 4W^3\,dW + 6W^2\,dt$, so "
                        rf"$\tfrac{{d}}{{dt}}\mathbb{{E}}W^4 = 6t$. Simulated at $t = 1$: {L['EW4']:.3f}.", width=6.4,
                        font_size=22)
        VGroup(pc, ans).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Consequences. The lemma solves geometric Brownian motion: its log grows at mu minus half sigma squared. "
            "<bookmark mark='a'/> On twenty thousand paths with ten percent drift and forty percent volatility, the "
            f"mean log return is {L['mean_log']:.3f}, the volatility drag, while the log of the mean return is "
            f"{L['log_mean']:.3f}. <bookmark mark='b'/> Paul Lévy's characterization: a continuous martingale whose "
            "quadratic variation is t is a Brownian motion. Dambis, Dubins and Schwarz: every continuous martingale "
            "is a Brownian motion running on the clock of its own quadratic variation. <bookmark mark='c'/> A desk "
            "classic: the expected fourth power of W at time t? <bookmark mark='d'/> Three t squared, by the lemma; "
            f"the simulation gives {L['EW4']:.3f} at t equals one."
            " The lemma solves a few equations exactly. Most must be simulated. Next."
        ) as vo:
            self.play(FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(pc))
            vo.wait_until("d")
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()
