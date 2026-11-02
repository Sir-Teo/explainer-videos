from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, fixed, illustration, load, loglog, polyline, predict


class FD(VoiceoverScene, ThreeDScene):
    def construct(self):
        f = load("fd")
        fl = load("fd_live")
        self.card()
        self.march(fl, f)
        self.proof(f)
        self.neumann()
        self.convergence(f)

    def card(self):
        c = chapter_card(12, r"Finite differences I: theta schemes and stability", r"How do you solve the pricing "
                         r"equation on a grid?", lit=(1947,), part=PART)
        with self.voiceover("Chapter twelve. Finite differences, part one: theta schemes and stability."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def march(self, fl, f):
        S = np.asarray(fl["S"])
        m = S <= 200
        Sx = S[m]
        ax = ThreeDAxes(x_range=[0, 200, 50], y_range=[0, 1, 0.25], z_range=[-20, 110, 20], x_length=7.0, y_length=5.0,
                        z_length=3.2, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def slices(run, every=1, bad_after=None):
            sl = np.asarray(run["slices"])[:, m]
            taus = run["tau"]
            g = VGroup()
            for k in range(0, len(sl), every):
                bad = bad_after is not None and k >= bad_after
                z = np.clip(sl[k], -20, 110)
                col = interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.OPTION), k / max(len(sl) - 1, 1))
                g.add(VMobject(stroke_color=BAD if bad else col, stroke_width=2.5).set_points_as_corners(
                    [ax.c2p(s, taus[k], v) for s, v in zip(Sx, z)]))
            return g

        good = slices(fl["runs"]["2000"])
        fb = fl["runs"]["200"]["first_bad"]
        badl = slices(fl["runs"]["200"], bad_after=fb if fb is not None else 10 ** 6)
        hint = VGroup(label(r"across: spot $S$", font_size=21, color=GREY_A),
                      label(r"back: time to expiry $\tau$", font_size=21, color=GREY_A),
                      label(r"up: the call's value on the grid", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        t1 = label(rf"explicit, 2{{,}}000 steps: {f['explicit']['2000']:.3f}", font_size=24, color=GOOD).to_corner(UR, buff=0.4)
        t2 = label(rf"explicit, 200 steps: the bound asks for {f['explicit_nt_min']:.0f}", font_size=24, color=BAD)
        t2.to_corner(UR, buff=0.4)
        lam = MathTex(rf"\lambda_{{\max}} = \sigma^2 S_{{\max}}^2\,\Delta\tau/\Delta S^2 = {fl['lambda_max_200']:.1f}"
                      rf"\ \ (\text{{stable only if}} \le \tfrac12)", font_size=26, color=BAD).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-62 * DEGREES, zoom=0.85)
        fixed(self, hint, t1, t2, lam)
        with self.voiceover(
            "The other family of methods solves the pricing equation itself, on a grid of prices and times. Eduardo "
            "Schwartz did it first in finance, for warrants, in 1977. Start from the payoff at expiry, here a call's "
            "hockey stick, and march backward in time to expiry, slice by slice. <bookmark mark='a'/> The explicit "
            "scheme computes each new value from three neighbours on the previous slice. With two thousand time "
            "steps on a hundred price points, the surface rolls smoothly back to today. <bookmark mark='b'/> With two "
            "hundred steps, the same scheme on the same grid. For a few slices nothing looks wrong. Then a sawtooth "
            "appears at high prices, doubles every step, and the surface explodes off the axes: the price comes out "
            f"near minus {abs(f['explicit']['200']) / 1e9:.0f} billion."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), run_time=1.5)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(x) for x in good], lag_ratio=0.15, run_time=5), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeOut(good), FadeOut(t1), FadeIn(t2))
            self.play(LaggedStart(*[Create(x) for x in badl], lag_ratio=0.2, run_time=max(vo.remaining(0.5) - 1, 3)),
                      FadeIn(lam))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, badl)), FadeOut(hint), FadeOut(t2),
                                                                  FadeOut(lam)], run_time=1.5)
        self.clear_scene()

    def proof(self, f):
        rows = [
            cmath(r"\partial_\tau V", r"=", r"\mathcal{L}V = \tfrac12\sigma^2S^2\,\partial_{SS}V + rS\,\partial_S V - rV",
                  font_size=34, colors={r"\partial_\tau V": OPT}),
            cmath(r"\partial_{SS}V", r"\approx", r"\frac{V_{j+1} - 2V_j + V_{j-1}}{\Delta S^2} + O(\Delta S^2)", font_size=34),
            cmath(r"\frac{V^{n+1} - V^n}{\Delta\tau}", r"=", r"\theta\,L_hV^{n+1} + (1 - \theta)\,L_hV^n", font_size=34),
            cmath(r"V_j^n = g^n e^{ikj\Delta x}", r"\Rightarrow", r"g_{\text{exp}} = 1 - 4\lambda s,\ \ g_{\text{imp}} = "
                  r"\frac{1}{1 + 4\lambda s},\ \ g_{\text{CN}} = \frac{1 - 2\lambda s}{1 + 2\lambda s}", font_size=30,
                  colors={r"\Rightarrow": BAD}),
            cmath(r"\text{consistent} + \text{stable}", r"\Leftrightarrow", r"\text{convergent}", font_size=34,
                  colors={r"\Leftrightarrow": GOOD}),
            cmath(r"\Delta\tau", r"\le", rf"\frac{{\Delta S^2}}{{\sigma^2 S_{{\max}}^2}}\ \Rightarrow\ "
                  rf"N_\tau \ge {f['explicit_nt_min']:.0f}", font_size=34, colors={r"\Delta\tau": BAD}),
        ]
        whys = [why(r"Part 10's equation, in time to expiry $\tau$"),
                why(r"Taylor: central differences are second-order accurate in the price step"),
                why(r"the theta scheme: explicit ($\theta = 0$), implicit (1), Crank--Nicolson ($\tfrac12$); local error "
                    r"$O(\Delta\tau)$, or $O(\Delta\tau^2)$ at $\tfrac12$ (expand about the midpoint)"),
                why(r"von Neumann (on $u_\tau = a u_{xx}$, $\lambda = a\Delta\tau/\Delta x^2$, $s = \sin^2\frac{k\Delta x}{2}$): "
                    r"substitute one Fourier mode; explicit is stable iff $\lambda \le \tfrac12$"),
                why(r"Lax's equivalence theorem (Lax and Richtmyer 1956), for linear problems"),
                why(r"Black--Scholes: $a = \tfrac12\sigma^2S^2$ is largest at $S_{\max}$; 100 price points up to $4K$")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.55, edge=6.9)
        with self.voiceover(
            "In symbols. Part ten's equation, written in time to expiry. <bookmark mark='a'/> Replace the second "
            "derivative by a central difference: second-order accurate in the price step. <bookmark mark='b'/> Then "
            "step in time with the theta scheme: theta zero is explicit, one is fully implicit, and one half is Crank "
            "and Nicolson's scheme from 1947, second order in time. <bookmark mark='c'/> Stability: put a single "
            "Fourier mode into the scheme and see how much it grows per step. The explicit factor dips below minus "
            "one once lambda passes a half; the others never leave the unit interval. <bookmark mark='d'/> Peter Lax's theorem then says that a consistent scheme "
            "converges exactly when it is stable. <bookmark mark='e'/> For Black–Scholes the binding point is the top "
            f"of the grid: on our hundred-point grid the explicit scheme needs at least {f['explicit_nt_min']:.0f} "
            "steps, which is why two hundred exploded."
        ) as vo:
            for i, mk in enumerate("abcde"):
                step(i)
                vo.wait_until(mk)
            step(5)
        self.wait(0.4)
        self.clear_scene()

    def neumann(self):
        g = axes([0, np.pi], [-3.2, 1.2], x_length=7.2, y_length=4.2, xlabel=r"frequency $k\Delta x$",
                 ylabel=r"growth per step $g(k)$", xticks=[0, np.pi / 2, np.pi], xfmt=lambda v: {0: "0", 1: r"\pi/2"}.get(
                     int(round(2 * v / np.pi)), r"\pi"), yticks=[-3, -2, -1, 0, 1], font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        band_ = Rectangle(width=ax.c2p(np.pi, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 1)[1] - ax.c2p(0, -1)[1],
                          stroke_width=0, fill_color=GOOD, fill_opacity=0.08).move_to(ax.c2p(np.pi / 2, 0))
        k = np.linspace(0, np.pi, 120)
        lam = ValueTracker(0.2)
        exp_c = always_redraw(lambda: curve(ax, k, np.clip(1 - 4 * lam.get_value() * np.sin(k / 2) ** 2, -3.2, 1.2),
                                            BAD, stroke_width=3))
        cn_c = always_redraw(lambda: curve(ax, k, (1 - 2 * lam.get_value() * np.sin(k / 2) ** 2) /
                                           (1 + 2 * lam.get_value() * np.sin(k / 2) ** 2), GOOD, stroke_width=3))
        rd = readout(r"\lambda =", lambda: lam.get_value(), digits=2, font_size=34, color=OPT)
        rd.next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        leg = legend([(BAD, r"explicit: $1 - 4\lambda\sin^2(k\Delta x/2)$"),
                      (GOOD, r"Crank--Nicolson"), (GREY_B, r"stable: $|g| \le 1$ (shaded)")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.5)
        side = wrapped_label(r"explicit leaves the band at $\lambda = \tfrac12$, at the highest frequency first: that "
                             r"mode flips sign and grows each step, the sawtooth. Crank--Nicolson never leaves it, but for "
                             r"large $\lambda$ its high frequencies sit near $-1$: they flip sign and barely decay "
                             r"(chapter 13)", 4.4, 18, GREY_A).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        with self.voiceover(
            "Here is the von Neumann picture, live. The growth factor of each frequency for the explicit scheme, red, "
            "and Crank–Nicolson, green; stability means staying in the shaded band. <bookmark mark='a'/> Raise "
            "lambda, the time step over the price step squared. At one half, the explicit curve touches minus one at "
            "the highest frequency, and beyond it that mode grows, flipping sign each step: the sawtooth you watched. "
            "<bookmark mark='b'/> Crank–Nicolson stays inside for any lambda. But look where its highest frequencies "
            "go as lambda grows: toward minus one. Stable, but hardly damped. That is the seed of the next chapter."
        ) as vo:
            self.play(FadeIn(g), FadeIn(band_), FadeIn(exp_c), FadeIn(cn_c), FadeIn(rd), FadeIn(leg))
            vo.wait_until("a")
            self.play(lam.animate.set_value(0.8), run_time=4)
            vo.wait_until("b")
            self.play(lam.animate.set_value(20.0), run_time=4, rate_func=rate_functions.ease_in_quad)
            self.play(FadeIn(side))
        for x in (exp_c, cn_c, rd):
            x.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def convergence(self, f):
        grids = np.log10(np.asarray(f["grids"], float))
        g = loglog(1.2, 2.8, -3, 0, r"grid points in price and in time", r"error in the call price", xt=[2], yt=[-3, -2, -1, 0])
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        cols = {"implicit": BAD, "cn": OPT, "cn+rannacher": GOOD}
        lines = VGroup(*[polyline(ax, grids, np.clip(np.log10(np.maximum(np.asarray(f["errors"][k]), 1e-7)), -3, 0), cols[k])
                         for k in ("implicit", "cn", "cn+rannacher")])
        leg = legend([(BAD, r"fully implicit: first order"), (OPT, r"Crank--Nicolson"),
                      (GOOD, r"Crank--Nicolson after two implicit half-steps (Rannacher)")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        ri = f["errors"]["implicit"][-2] / f["errors"]["implicit"][-1]
        rc = f["errors"]["cn"][-2] / f["errors"]["cn"][-1]
        side = wrapped_label(rf"at the finest grids, doubling cuts the implicit error {ri:.1f} times and Crank--Nicolson's "
                             rf"{rc:.1f} times, the mark of second order; the implicit ratio is falling toward 2 as its "
                             r"first-order time error takes over. Finite elements (Seydel's textbook) are the other "
                             r"family; desks rarely use them for vanillas", 4.4, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        q = predict(r"Double the price points of a stable explicit grid. How many more time steps?", width=4.4,
                    font_size=20).to_corner(DR, buff=0.3)
        src = illustration(r"one-year at-the-money call; uniform grid to four times the strike", corner=DL)
        with self.voiceover(
            "And measured. Each stable scheme's error as the grid is refined in price and time together. The fully "
            "implicit scheme is only first order in time. <bookmark mark='a'/> Crank–Nicolson is second order: on "
            f"the finest grids, doubling the grid cuts its error {rc:.1f} times. <bookmark mark='b'/> Pause and "
            "predict: double the price points of a stable explicit grid. The bound has the price step squared in "
            "it, so you need four times the time steps, and eight times the work."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lines[0]), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lines[1]), FadeIn(leg[1]), Create(lines[2]), FadeIn(leg[2]), FadeIn(side), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
