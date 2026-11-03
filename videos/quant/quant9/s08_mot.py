from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant9.common import (ALT, ARB, CALL, FWD, HEDGE, PART, PUT, Q_C, answer_under, load, pause_at,
                                        real_data)


class MOT(VoiceoverScene, ThreeDScene):
    def construct(self):
        m, du, cl = load("mot"), load("mot_dual"), load("mot_claims")
        self.card()
        self.problem(m)
        self.dual()
        self.hedge3d(du)
        self.bounds(m, cl)
        self.predict(cl)

    def card(self):
        c = chapter_card(15, r"Bounds without a model", r"What do vanilla prices alone imply for exotic ones?",
                         lit=(1998,), part=PART)
        with self.voiceover("Chapter fifteen. Bounds without a model."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def problem(self, m):
        x, mu, y, nu = (np.asarray(m[k]) for k in ("x", "mu", "y", "nu"))
        ks = np.linspace(0.4, 1.8, 141)
        c1 = np.array([np.dot(mu, np.maximum(x - k, 0)) for k in ks])
        c2 = np.array([np.dot(nu, np.maximum(y - k, 0)) for k in ks])
        g = axes([0.4, 1.8], [0, 0.62], x_length=5.6, y_length=3.8, xlabel=r"strike, over the forward",
                 ylabel=r"call price, over the forward", xticks=[0.5, 1.0, 1.5], yticks=[0, 0.2, 0.4, 0.6],
                 font_size=15)
        g.to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        ax = g.ax
        k1 = curve(ax, ks, c1, ALT, stroke_width=4)
        k2 = curve(ax, ks, c2, Q_C, stroke_width=4)
        lg = legend([(ALT, rf"first expiry, {m['T1'] * 365:.0f} days"), (Q_C, rf"second expiry, {m['T2'] * 365:.0f} days")],
                    font_size=17).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        rows = [cmath(r"\sup_\pi / \inf_\pi", r"\ ", r"\sum_{i,j}\pi_{ij}\, c(x_i, y_j)", font_size=32,
                      colors={r"\sup_\pi / \inf_\pi": ALT}),
                cmath(r"\sum_j \pi_{ij} = \mu_i,\ \sum_i \pi_{ij} = \nu_j", r",", r"\sum_j \pi_{ij}(y_j - x_i) = 0",
                      font_size=30, colors={r"\sum_j \pi_{ij}(y_j - x_i) = 0": Q_C}),
                cmath(r"\text{feasible}", r"\iff", r"\mu \le_{cx} \nu", font_size=30, colors={r"\text{feasible}": Q_C})]
        whys = [side_why_(r"a claim on the prices at two dates; its price depends on how the two are joined"),
                side_why_(r"every joining must match both marginals, which the vanilla options fix (chapter 12), and be "
                          r"a martingale (no arbitrage)"),
                side_why_(r"a martingale with these marginals exists exactly when the later call curve lies above the "
                          r"earlier one at every strike: $\int (y - k)^+ d\nu \ge \int (x - k)^+ d\mu$ for all $k$ "
                          r"(Strassen 1965)")]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=3.6, buff=0.55, edge=6.95)
        with self.voiceover(
            "A claim on the price at two dates depends on how they are joined, which vanilla prices "
            "don't reveal. Here are the call curves at the Surface's two expiries. <bookmark "
            "mark='a'/> Over all joinings, the claim's price has a highest and lowest value. "
            "<bookmark mark='b'/> A joining must match both densities and be a martingale. <bookmark "
            "mark='c'/> One exists exactly when the later call curve lies above the earlier, "
            "Strassen's theorem of 1965, as here. The rest is a linear program: martingale optimal "
            "transport."
            f" Here the earlier marginal has {len(x)} atoms and the later {len(y)}, so the program has "
            f"{len(x) * len(y):,} unknowns."
        ) as vo:
            self.play(FadeIn(g), Create(k1), Create(k2), FadeIn(lg))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            self.play(Indicate(k2, color=Q_C, scale_factor=1.0))
        self.wait(0.3)
        self.clear_scene()

    def dual(self):
        rows = [cmath(r"\inf_{u,v,h}\ ", r"\ ", r"\sum_i u_i\mu_i + \sum_j v_j\nu_j", font_size=34,
                      colors={r"\inf_{u,v,h}\ ": HEDGE}),
                cmath(r"u(x) + v(y) + h(x)(y - x)", r"\ge", r"c(x, y)\quad \forall x, y", font_size=34,
                      colors={r"u(x) + v(y) + h(x)(y - x)": HEDGE}),
                cmath(r"\sum \pi\, c", r"\le", r"\sum \pi\,(u + v + h\,(y - x)) = \sum u\mu + \sum v\nu", font_size=32),
                cmath(r"\sup_\pi \sum \pi\, c", r"=", r"\inf_{u,v,h} \Big(\sum u\mu + \sum v\nu\Big)", font_size=34,
                      colors={r"\inf_{u,v,h} \Big(\sum u\mu + \sum v\nu\Big)": HEDGE})]
        whys = [why(r"a multiplier for each constraint: $u_i$ for the first marginal, $v_j$ the second, $h_i$ the "
                    r"martingale condition", 21),
                why(r"read as trades: a static portfolio of first-expiry vanillas $u$, second-expiry vanillas $v$, and "
                    r"$h(S_1)$ units of the underlying held from the first date to the second", 21),
                why(r"weak duality: integrate the inequality against any feasible $\pi$; the $h$ term vanishes by the "
                    r"martingale constraint", 21),
                why(r"strong duality (Beiglb\"ock, Henry-Labord\`ere and Penkner 2013): the bound is the price of the "
                    r"cheapest model-free super-hedge", 21)]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-0.4, buff=0.6, edge=6.9)  # leaves the corner for the card
        t = history_card(2014, r"Galichon, Henry-Labord\`ere and Touzi", r"in continuous time the dual is a stochastic "
                         r"control problem: the hedger chooses the delta through time", width=5.6, font_size=19)
        t.to_corner(DR, buff=0.3)
        with self.voiceover(
            "Its dual is a trading strategy. Multipliers: u for the first density, v for the second, "
            "h for the martingale condition. <bookmark mark='a'/> As trades: options on the first "
            "date paying u, on the second paying v, and h of the underlying held in between, at least "
            "the claim whatever happens. <bookmark mark='b'/> Weak duality: integrate against any "
            "joining; the trading term averages to zero. <bookmark mark='c'/> Strong duality, "
            "Beiglböck, Henry-Labordère and Penkner, 2013: the highest model price is the cheapest "
            "model-free super-hedge. Galichon, Henry-Labordère and Touzi made the dual a control "
            "problem in continuous time."
            " So any static portfolio of options that dominates the claim, plus any delta, costs at "
            "least the price under every martingale model."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            self.play(FadeIn(t))
        self.wait(0.3)
        self.clear_scene()

    def hedge3d(self, du):
        x, y = np.asarray(du["x"]), np.asarray(du["y"])
        up = du["up"]
        u, v, h = (np.asarray(up[k]) for k in ("u", "v", "h"))
        pi = np.asarray(up["pi"])
        X0, X1, Y0, Y1 = 0.7, 1.4, 0.5, 1.8
        Z1 = 1.0

        def pay(a, b):
            return abs(b / a - 1)

        def hedge(a, b):
            return float(np.interp(a, x, u) + np.interp(b, y, v) + np.interp(a, x, h) * (b - a))

        ax = ThreeDAxes(x_range=[X0, X1, 0.1], y_range=[Y0, Y1, 0.2], z_range=[0, Z1, 0.25], x_length=6.0,
                        y_length=7.0, z_length=2.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.3)
        lift = ValueTracker(0.6)
        P = Surface(lambda a, b: ax.c2p(a, b, min(pay(a, b), Z1)), u_range=[X0, X1], v_range=[Y0, Y1],
                    resolution=(18, 22), fill_opacity=0.55, checkerboard_colors=[PUT, interpolate_color(
                        ManimColor(PUT), ManimColor(BACKGROUND), 0.3)], stroke_width=0.3, stroke_color=PUT)

        def hsurf():
            dz = lift.get_value()
            return Surface(lambda a, b: ax.c2p(a, b, float(np.clip(hedge(a, b) + dz, 0, Z1 + 0.6))),
                           u_range=[X0, X1], v_range=[Y0, Y1], resolution=(14, 16), fill_opacity=0.35,
                           checkerboard_colors=[HEDGE, interpolate_color(ManimColor(HEDGE), ManimColor(BACKGROUND), 0.4)],
                           stroke_width=0.3, stroke_color=HEDGE)

        H = always_redraw(hsurf)
        cont = VGroup(*[Dot3D(ax.c2p(x[i], y[j], min(pay(x[i], y[j]), Z1)), radius=0.05, color=Q_C, resolution=(4, 4))
                        for i in range(len(x)) for j in range(len(y)) if pi[i, j] > 1e-4 and X0 <= x[i] <= X1
                        and Y0 <= y[j] <= Y1])
        floor = VGroup(*[Dot(ax.c2p(x[i], y[j], 0), radius=0.03 + 0.12 * np.sqrt(pi[i, j] / pi.max()), color=Q_C)
                         .set_opacity(0.7) for i in range(len(x)) for j in range(len(y))
                         if pi[i, j] > 1e-4 and X0 <= x[i] <= X1 and Y0 <= y[j] <= Y1])
        names = VGroup(label(r"red: the claim $|S_2/S_1 - 1|$", font_size=22, color=PUT),
                       label(r"gold: the hedge $u(S_1) + v(S_2) + h(S_1)(S_2 - S_1)$", font_size=22, color=HEDGE),
                       label(r"purple: where the dearest model puts its mass", font_size=22, color=Q_C)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.3)
        axn = label(r"axes: $S_1/F_1$ across, $S_2/F_2$ deep, payoff up", font_size=19, color=GREY_B).to_corner(DL,
                                                                                                         buff=0.3)
        val = MathTex(rf"\text{{hedge cost }} = \sum u\mu + \sum v\nu = {up['dual_value']:.4f}", font_size=30,
                      color=HEDGE).to_corner(UR, buff=0.35)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-130 * DEGREES, zoom=0.68)  # the hedge rises well above the claim
        self.add_fixed_in_frame_mobjects(names, axn, val)
        self.remove(names, axn, val)
        with self.voiceover(
            "The dual in three dimensions. The floor is every pair of prices; the red surface is the "
            "claim, a valley along the diagonal. <bookmark mark='a'/> The gold surface is the optimal "
            "hedge from the program's dual, starting high. <bookmark mark='b'/> Lower it: it rests on "
            "the claim without crossing. Its cost is the upper bound. <bookmark mark='c'/> And the "
            "purple dots, where the most expensive model puts its mass, sit exactly where it touches: "
            "complementary slackness, seen."
            " Off the contact set the hedge is strictly above the claim: money left on the table in "
            "states the extreme model never visits."
        ) as vo:
            self.play(Create(ax), FadeIn(names[0]), FadeIn(axn), run_time=1.5)
            self.play(Create(P), run_time=2.5)
            vo.wait_until("a")
            self.add(H)
            self.play(FadeIn(names[1]))
            self.begin_ambient_camera_rotation(rate=0.08)
            vo.wait_until("b")
            self.play(lift.animate.set_value(0.0), run_time=3.0, rate_func=smooth)
            H.clear_updaters()
            self.play(FadeIn(val))
            vo.wait_until("c")
            self.play(FadeIn(cont), FadeIn(floor), FadeIn(names[2]))
        self.stop_ambient_camera_rotation()
        H.clear_updaters()
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0,
                         added_anims=[FadeOut(VGroup(ax, P, H, cont, floor)), FadeOut(names), FadeOut(axn),
                                      FadeOut(val)], run_time=1.5)
        self.clear_scene()

    def bounds(self, m, cl):
        lo, up, model = m["lower"], m["upper"], m["model"]
        g = axes([0.10, 0.24], [0, 1], x_length=6.4, y_length=1.2, xlabel=r"forward-start straddle, as a fraction of "
                 r"the price at the first expiry", xticks=[0.10, 0.14, 0.18, 0.22], yticks=[], font_size=16)
        g.to_edge(UP, buff=0.7).to_edge(LEFT, buff=0.8)
        ax = g.ax
        band_ = Rectangle(width=ax.c2p(up, 0)[0] - ax.c2p(lo, 0)[0], height=0.5, stroke_width=0, fill_color=ALT,
                          fill_opacity=0.5).move_to((ax.c2p(lo, 0.5) + ax.c2p(up, 0.5)) / 2)
        bl = MathTex(f"{lo:.3f}", font_size=26, color=ALT).next_to(ax.c2p(lo, 0.5), UP, buff=0.35)
        bu = MathTex(f"{up:.3f}", font_size=26, color=ALT).next_to(ax.c2p(up, 0.5), UP, buff=0.35)
        md = Line(ax.c2p(model, 0.15), ax.c2p(model, 0.85), color=CALL, stroke_width=5)
        ml = MathTex(rf"\text{{log-normal: }} {model:.3f}", font_size=24, color=CALL).next_to(md, UP, buff=0.12)  # above the band, between its two end values
        tab = VGroup(*[VGroup(label(n, font_size=21, color=c), MathTex(t, font_size=26, color=c)).arrange(RIGHT, buff=0.3)
                       for n, t, c in (
                           (r"forward-start straddle $|R - 1|$", rf"[{cl['straddle']['lower']:.4f},\ "
                                                                 rf"{cl['straddle']['upper']:.4f}]", ALT),
                           (r"forward-start call $(R - 1)^+$", rf"[{cl['fwd_call']['lower']:.4f},\ "
                                                               rf"{cl['fwd_call']['upper']:.4f}]", CALL),
                           (r"$(S_2 - S_1)^2$", rf"[{cl['sq']['lower']:.5f},\ {cl['sq']['upper']:.5f}]", Q_C),
                           (r"$(\ln S_2/S_1)^2$", rf"[{cl['logsq']['lower']:.4f},\ {cl['logsq']['upper']:.4f}]", FWD))])
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(g, DOWN, buff=1.0).align_to(g, LEFT)
        side = VGroup(
            wrapped_label(r"the forward-start call's band is exactly half the straddle's: $(R - 1)^+ = \tfrac12(|R - 1| "
                          r"+ (R - 1))$ and $R - 1$ has mean zero given $S_1$", 4.6, 19, CALL),
            wrapped_label(r"Hobson (1998) solved the first case of this kind, the lookback, by the Az\'ema--Yor "
                          r"embedding; Part 15 prices exotics inside such bands", 4.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.6)
        src = real_data(r"densities from the Surface, 25 and 81 atoms; the House's \texttt{mot\_bounds} (HiGHS)")
        with self.voiceover(
            f"The numbers. The forward-start straddle lies between {lo:.3f} and {up:.3f} of the first "
            f"price. <bookmark mark='a'/> Independent log-normal returns say {model:.3f}: inside, as "
            "they must be. <bookmark mark='b'/> The forward-start call's band is exactly half the "
            "straddle's, and the squared change has a band of zero width. <bookmark mark='c'/> Hobson "
            "found the first bound of this kind in 1998, for the lookback."
            f" The squared log return is different: its band, {cl['logsq']['lower']:.4f} to "
            f"{cl['logsq']['upper']:.4f}, is open, because it is not a difference of moments."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(band_), FadeIn(bl), FadeIn(bu))
            vo.wait_until("a")
            self.play(Create(md), FadeIn(ml))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab], lag_ratio=0.3), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.wait(0.3)
        self.clear_scene()

    def predict(self, cl):
        card = pause_at(r"Why is the band for $(S_2 - S_1)^2$ a single number?")
        with self.voiceover(
            "Pause and predict. Why is the squared change a single number? <bookmark mark='a'/> For "
            "any martingale its value is the difference of the two second moments, and the vanillas "
            "fix both."
            " So the square's band has width zero, and any dealer quoting a different price can be "
            "arbitraged with vanillas alone."
            " Next: those bounds, computed on real data."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(answer_under(card, rf"$\mathbb{{E}}[(S_2 - S_1)^2] = \mathbb{{E}}[S_2^2] - \mathbb{{E}}[S_1^2]$ for "
                                                rf"any martingale: both marginals fix it ({cl['sq_exact']:.5f})")))
        self.wait(0.4)
        self.clear_scene()


def side_why_(text):
    return wrapped_label(text, 5.8, 18, GREY_B)
