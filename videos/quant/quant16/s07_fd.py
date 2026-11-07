from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, fixed, illustration, load, loglog, polyline, predict, axes, data_range, pause_card, flat_camera


def signed_log(values):
    values = np.asarray(values, float)
    return np.sign(values) * np.log10(1 + np.abs(values))


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
        Sx = S
        zr = data_range(*[signed_log(r["slices"]) for r in fl["runs"].values()])
        ax = ThreeDAxes(x_range=[float(S.min()), float(S.max()), 100], y_range=[0, 1, 0.25], z_range=[*zr, (zr[1] - zr[0]) / 4], x_length=7.0, y_length=5.0,
                        z_length=3.2, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def slices(run, every=1, bad_after=None):
            sl = np.asarray(run["slices"])
            taus = run["tau"]
            g = VGroup()
            for k in range(0, len(sl), every):
                bad = bad_after is not None and k >= bad_after
                z = signed_log(sl[k])
                col = interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.OPTION), k / max(len(sl) - 1, 1))
                g.add(VMobject(stroke_color=BAD if bad else col, stroke_width=2.5).set_points_as_corners(
                    [ax.c2p(s, taus[k], v) for s, v in zip(Sx, z)]))
            return g

        good = slices(fl["runs"]["2000"])
        fb = fl["runs"]["200"]["first_bad"]
        badl = slices(fl["runs"]["200"], bad_after=fb if fb is not None else 10 ** 6)
        hint = VGroup(label(r"across: spot $S$", font_size=21, color=GREY_A),
                      label(r"back: time to expiry $\tau$", font_size=21, color=GREY_A),
                      label(r"up: signed log value $\mathrm{sgn}(V)\log_{10}(1+|V|)$", font_size=21, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        t1 = label(rf"explicit, 2{{,}}000 steps: {f['explicit']['2000']:.3f}", font_size=24, color=GOOD).to_corner(UR, buff=0.4)
        t2 = label(rf"explicit, 200 steps; diffusion CFL estimate {f['explicit_nt_min']:.0f}", font_size=24, color=BAD)
        t2.to_corner(UR, buff=0.4)
        lam = MathTex(rf"\lambda_{{\max}} = \sigma^2 S_{{\max}}^2\,\Delta\tau/\Delta S^2 = {fl['lambda_max_200']:.1f}"
                      rf"\ \ (\text{{diffusion threshold}} \le 1)", font_size=26, color=BAD).to_corner(DR, buff=0.4)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-62 * DEGREES, zoom=0.85)
        fixed(self, hint, t1, t2, lam)
        with self.voiceover(
            f"A finite-difference method evolves the pricing equation on a stock-and-time grid. Start at the call payoff and move through time to expiry. Height here is explicitly signed logarithmic value, retaining the full stock domain and all saved slice values. It is a display transform, not a price rescaling. <bookmark mark='a'/> With two thousand time steps the recorded explicit solution stays smooth on this grid. <bookmark mark='b'/> With two hundred, the high-stock region becomes unstable. The signed-log scale exposes the growing oscillations instead of clipping them. The saved spot price is {f['explicit']['200']:.3g}. The displayed diffusion number is sigma squared S-max squared delta-time over delta-S squared, whose diffusion threshold is one, not one half. Drift, reaction and boundary conditions require additional stability or monotonicity checks."
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
        flat_camera(self)

    def proof(self, f):
        rows = [
            cmath(r"\partial_\tau V", r"=", r"\mathcal{L}V = \tfrac12\sigma^2S^2\,\partial_{SS}V + rS\,\partial_S V - rV",
                  font_size=34, colors={r"\partial_\tau V": OPT}),
            cmath(r"\partial_{SS}V", r"\approx", r"\frac{V_{j+1} - 2V_j + V_{j-1}}{\Delta S^2} + O(\Delta S^2)", font_size=34),
            cmath(r"\frac{V^{n+1} - V^n}{\Delta\tau}", r"=", r"\theta\,L_hV^{n+1} + (1 - \theta)\,L_hV^n", font_size=34),
            cmath(r"V_j^n = g^n e^{ikj\Delta x}", r"\Rightarrow", r"g_{\text{exp}} = 1 - 4\lambda s,\ \ g_{\text{imp}} = "
                  r"\frac{1}{1 + 4\lambda s},\ \ g_{\text{CN}} = \frac{1 - 2\lambda s}{1 + 2\lambda s}", font_size=26,
                  colors={r"\Rightarrow": BAD}),
            cmath(r"\text{consistent} + \text{stable}", r"\Leftrightarrow", r"\text{convergent}", font_size=34,
                  colors={r"\Leftrightarrow": GOOD}),
            cmath(r"\Delta\tau", r"\le", rf"\frac{{\Delta S^2}}{{\sigma^2 S_{{\max}}^2}}\ \Rightarrow\ "
                  rf"N_\tau \ge {f['explicit_nt_min']:.0f}", font_size=34, colors={r"\Delta\tau": BAD}),
        ]
        whys = [why(r"Part 10's equation, in time to expiry $\tau$"),
                why(r"Taylor: central differences are second-order accurate in the price step"),
                why(r"theta scheme: explicit (0), implicit (1), Crank--Nicolson ($\frac12$); global time orders one, one, two "
                    r"under suitable regularity and stability; nonsmooth payoffs need care"),
                why(r"von Neumann (on $u_\tau = a u_{xx}$, $\lambda = a\Delta\tau/\Delta x^2$, $s = \sin^2\frac{k\Delta x}{2}$): "
                    r"substitute one Fourier mode; explicit is stable iff $\lambda \le \tfrac12$"),
                why(r"Lax's equivalence theorem (Lax and Richtmyer 1956), for consistent approximations to well-posed linear initial-value problems"),
                why(r"diffusion-only CFL estimate using $a=\frac12\sigma^2S^2$; drift/reaction, boundaries and monotonicity are additional conditions")]
        step = ladder(self, rows, whys, keep=3, top=3.0, x=0.0, align_index=None, buff=0.45, edge=6.6)
        with self.voiceover(
            f"The Black–Scholes operator contains diffusion, drift and discounting. <bookmark mark='a'/> Central space differences have second-order consistency for a sufficiently smooth solution. <bookmark mark='b'/> The theta scheme is explicit at zero, implicit at one, and Crank–Nicolson at one half. Its familiar global time orders require regularity and stability. <bookmark mark='c'/> For constant-coefficient heat diffusion, Fourier analysis uses lambda equal to diffusion coefficient times time step over space step squared. Explicit stability requires lambda at most one half. Implicit and Crank–Nicolson factors stay between minus one and one; Crank–Nicolson can be negative. <bookmark mark='d'/> Lax equivalence connects stability and convergence for consistent approximations to a well-posed linear initial-value problem. <bookmark mark='e'/> In Black–Scholes the diffusion coefficient is one half sigma squared S squared. This gives the displayed diffusion-only estimate of {f['explicit_nt_min']:.0f} steps. It does not alone certify the complete drift, reaction and boundary discretization."
        ) as vo:
            for i, mk in enumerate("abcde"):
                step(i)
                vo.wait_until(mk)
            step(5)
        self.wait(0.4)
        self.clear_scene()

    def neumann(self):
        g = axes([0, np.pi], [-2.05, 0.4], x_length=7.2, y_length=4.2, xlabel=r"frequency $k\Delta x$",
                 ylabel=r"signed log growth: $\mathrm{sgn}(g)\log_{10}(1+|g|)$", xticks=[0, np.pi / 2, np.pi], xfmt=lambda v: {0: "0", 1: r"\pi/2"}.get(
                     int(round(2 * v / np.pi)), r"\pi"), yticks=list(signed_log([-79, -10, -1, 0, 1])),
                 yfmt=lambda v: f"{int(round(np.sign(v) * (10 ** abs(v) - 1)))}", font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        band_ = Rectangle(width=ax.c2p(np.pi, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, np.log10(2))[1] - ax.c2p(0, -np.log10(2))[1],
                          stroke_width=0, fill_color=GOOD, fill_opacity=0.08).move_to(ax.c2p(np.pi / 2, 0))
        k = np.linspace(0, np.pi, 120)
        lam = ValueTracker(0.2)
        exp_c = always_redraw(lambda: curve(ax, k, signed_log(1 - 4 * lam.get_value() * np.sin(k / 2) ** 2),
                                            BAD, stroke_width=3))
        cn_c = always_redraw(lambda: curve(ax, k, signed_log((1 - 2 * lam.get_value() * np.sin(k / 2) ** 2) /
                                           (1 + 2 * lam.get_value() * np.sin(k / 2) ** 2)), GOOD, stroke_width=3))
        rd = readout(r"\lambda =", lambda: lam.get_value(), digits=2, font_size=34, color=OPT)
        rd.next_to(g, UP, buff=0.1).align_to(g, RIGHT)
        leg = legend([(BAD, r"explicit heat scheme"),
                      (GOOD, r"Crank--Nicolson"), (GREY_B, r"stable: $|g| \le 1$ (shaded)")], font_size=17)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.5)
        side = wrapped_label(r"explicit leaves the band at $\lambda = \tfrac12$, at the highest frequency first: that "
                             r"mode flips sign and grows each step, the sawtooth. Crank--Nicolson never leaves it, but for "
                             r"large $\lambda$ its high frequencies sit near $-1$: they flip sign and barely decay "
                             r"(chapter 13)", 4.5, 20, GREY_A).next_to(leg, DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The vertical axis is a signed logarithm, with ticks labelled by the actual growth factor. Both curves receive the same transform. The shaded band still means absolute growth no greater than one. <bookmark mark='a'/> At heat-equation lambda one half, the highest-frequency explicit factor reaches minus one. Beyond that it flips and grows; by lambda twenty its factor is minus seventy-nine, fully shown. <bookmark mark='b'/> Crank–Nicolson remains between minus one and one for nonnegative lambda, but its highest frequencies approach minus one and decay slowly. This is diffusion-mode analysis, with the complete pricing discretization requiring its own boundary and operator checks."
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
        yr = data_range(*[np.log10(f["errors"][k]) for k in ("implicit", "cn", "cn+rannacher")])
        g = loglog(*data_range(grids), *yr, r"grid points in price and in time", r"error in the call price", xt=[2], yt=[-3, -2, -1, 0])
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        cols = {"implicit": BAD, "cn": OPT, "cn+rannacher": GOOD}
        # Crank--Nicolson and its Rannacher start agree on the price to 3 digits: draw plain CN last, dashed, on top
        pl = [polyline(ax, grids, np.log10(f["errors"][k]), cols[k])
              for k in ("implicit", "cn+rannacher", "cn")]
        lines = VGroup(pl[0], pl[1], VGroup(DashedVMobject(pl[2][0], num_dashes=30), *pl[2][1:]))
        leg = legend([(BAD, r"fully implicit: first order"), (OPT, r"Crank--Nicolson"),
                      (GOOD, r"Crank--Nicolson after two implicit half-steps (Rannacher)")], font_size=16)
        leg.next_to(g, UP, buff=0.1).align_to(g, LEFT)
        ri = f["errors"]["implicit"][-2] / f["errors"]["implicit"][-1]
        rc = f["errors"]["cn"][-2] / f["errors"]["cn"][-1]
        side = wrapped_label(rf"at the finest grids, doubling cuts the implicit error {ri:.1f} times and Crank--Nicolson's "
                             rf"{rc:.1f} times, the mark of second order; the implicit ratio is falling toward 2 as its "
                             r"first-order time error takes over. On the price the Rannacher start changes almost "
                             r"nothing; it is for the Greeks (chapter 13). Finite elements (Seydel's textbook) are the other "
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
            " Next: what goes wrong at the kink, and how a grid prices an American put."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lines[0]), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(lines[1]), FadeIn(leg[1]), Create(lines[2]), FadeIn(leg[2]), FadeIn(side), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
