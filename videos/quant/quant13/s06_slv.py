from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant13.common import BAD, IV, MODEL_COL, OPT, PART, RV, SPOT, VAR, illustration, load, pause

LAB_SLV = [
    "sub = g.choice(n_paths, n_sub, replace=False)",
    "bw = 1.06 * np.std(x[sub]) * n_sub ** (-0.2)      # Silverman",
    "Wk = np.exp(-0.5 * ((grid[:, None] - x[None, sub]) / bw) ** 2)",
    "Ev = (Wk @ v[sub]) / Wk.sum(axis=1)               # E[v | x]",
    "Lg = lv_fn(grid, t) / np.sqrt(np.maximum(Ev, 1e-6))  # leverage",
    "Lx = np.interp(x, grid, Lg)",
    "z1 = g.standard_normal(n_paths)",
    "z2 = rho * z1 + np.sqrt(1 - rho**2) * g.standard_normal(n_paths)",
    "vp = np.maximum(v, 0)",
    "x = x - 0.5 * Lx**2 * vp * h + Lx * np.sqrt(vp * h) * z1",
    "v = v + kappa * (theta - vp) * h + xi * np.sqrt(vp * h) * z2",
]


class SLV(VoiceoverScene, ThreeDScene):
    def construct(self):
        s = load("slv")
        sp = load("slv_particles")
        self.card()
        self.model()
        self.particles(sp)
        self.surface3d(s)
        self.lab(s)
        self.convergence(sp)
        self.cards()

    def card(self):
        c = chapter_card(11, r"Stochastic local volatility: the particle method",
                         r"Can one model fit today's smile and keep tomorrow's?", part=PART)
        with self.voiceover("Chapter eleven. Stochastic local volatility, and the particle method."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c), run_time=0.35)

    def model(self):
        rows = [cmath(r"\frac{dS}{S}", r"=", r"L(S, t)\,\sqrt{v_t}\,dW^1_t,\qquad dv_t = \kappa(\theta - v_t)\,dt + "
                      r"\eta\,\xi\sqrt{v_t}\,dW^2_t", font_size=34, colors={r"\frac{dS}{S}": SPOT}),
                cmath(r"\sigma^2_{\text{loc}}(S, t)", r"=", r"L^2(S, t)\ \mathbb{E}\big[v_t \mid S_t = S\big]", font_size=36,
                      colors={r"\sigma^2_{\text{loc}}(S, t)": MODEL_COL["LV"]}),
                cmath(r"L(S, t)", r"=", r"\frac{\sigma_{\text{loc}}(S, t)}{\sqrt{\mathbb{E}\big[v_t \mid S_t = S\big]}}\ "
                      r"\ \text{depends on the law of}\ (S_t, v_t)", font_size=32, colors={r"L(S, t)": MODEL_COL["SLV"]}),
                cmath(r"\mathbb{E}\big[v \mid S\big]", r"\approx", r"\frac{\sum_i v^i\,K_h(S^i - S)}{\sum_i K_h(S^i - S)},\quad "
                      r"h = 1.06\,\hat\sigma\,N^{-1/5}", font_size=32, colors={r"\mathbb{E}\big[v \mid S\big]": VAR}),
                cmath(r"\text{error}", r"\sim", r"\underbrace{O(h^2)}_{\text{bias}} + \underbrace{O\big((Nh)^{-1/2}\big)}"
                      r"_{\text{noise}}\ \Rightarrow\ h \propto N^{-1/5},\ \ \text{error} \propto N^{-2/5}", font_size=30,
                      colors={r"\text{error}": BAD})]
        whys = [why(r"Heston's variance, its vol of vol scaled by the mixing fraction $\eta$, times a leverage function "
                    r"$L$ of the price and the date", 20),
                why('Ideal marginal projection under existence and regularity assumptions; finite particles do not reprice exactly.', 20),
                why(r"so $L$ depends on the joint law of the model it drives: a McKean--Vlasov SDE, nonlinear in the "
                    r"sense of McKean", 20),
                why(r"Guyon and Henry-Labord\`ere (2012): estimate the conditional expectation across the simulated "
                    r"particles themselves, by kernel regression (Nadaraya--Watson), with Silverman's bandwidth", 20),
                why(r"kernel regression's trade-off: a wide window is biased, a narrow one noisy; balancing them gives "
                    r"the rate, as a heuristic", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.8, edge=6.9)
        with self.voiceover(
            (
            """Local volatility targets today's marginals; stochastic volatility supplies another source of smile dynamics. SLV combines them: Heston variance, with vol of vol scaled by eta, and a leverage function. <bookmark mark='a'/> Under suitable existence and regularity conditions, matching leverage squared times conditional variance to Dupire variance gives the same one-date marginals and vanilla prices. This is an ideal identity. <bookmark mark='b'/> The conditional expectation uses the model's own law, which depends on leverage: a McKean–Vlasov equation. <bookmark mark='c'/> Guyon and Henry-Labordère's particle method estimates it across simulated particles by kernel regression. <bookmark mark='d'/> The displayed bias–noise balance is an independent-sample kernel heuristic. Interacting particles, time stepping, boundaries and sparse wings add errors; this is not a convergence theorem for our implementation."""
        )
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
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def particles(self, sp):
        snaps = sp["snaps"]
        grid = np.asarray(sp["grid"])
        g = axes([-1.5, 0.75], [-0.05, 1.8], x_length=7.0, y_length=4.2, xlabel=r"log-moneyness $x = \ln S/S_0$",
                 ylabel=r"variance $v$", xticks=[-1.5, -0.75, 0, 0.75], yticks=[0, 0.6, 1.2, 1.8], font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        gl = axes([-0.6, 0.6], [-0.2, 3.5], x_length=4.2, y_length=2.4, xlabel=r"$x$", ylabel=r"leverage $L(x,t)$, log scale",
                  xticks=[-0.5, 0, 0.5], yticks=[0, 1, 2, 3], yfmt=lambda u: f"10^{{{u:.0f}}}", font_size=13).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)

        def frame(k):
            z = snaps[k]
            x, v = np.asarray(z["x"]), np.asarray(z["v"])
            ok = np.isfinite(x) & np.isfinite(v)
            cloud = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.022, color=VAR, fill_opacity=0.55) for a, b in zip(x[ok], v[ok])])
            ev = curve(g.ax, grid, np.asarray(z["Ev"]), IV, stroke_width=4)
            L = curve(gl.ax, grid, np.log10(np.asarray(z["L"])), MODEL_COL["SLV"], stroke_width=3)
            day = MathTex(rf"\text{{day}}\ {z['day']}", font_size=30, color=WHITE).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
            return VGroup(cloud, ev, L, day)

        cur = frame(0)
        leg = legend([(VAR, r"particles (900 of 8{,}000)"), (IV, r"$\mathbb{E}[v \mid x]$, kernel estimate")],
                     font_size=17).next_to(g, UP, buff=0.12).align_to(g, LEFT)
        note_ = wrapped_label('Raw kernel estimates; variance floor $10^{-6}$. Sparse wings can give very large $L$. No leverage cap in the original algorithm.', 4.2, 18, GREY_A)
        note_.next_to(gl, DOWN, buff=0.4).align_to(gl, LEFT)
        src = illustration(r"the House's particle method on the Surface's SSVI local vol; Heston from chapter 4, $\eta = \tfrac12$")
        with self.voiceover(
            (
            """Each dot is a saved log-price and Euler variance particle. This view includes all saved particles, including small negative Euler variances; the spot step uses their positive parts. <bookmark mark='a'/> Gold is the raw kernel estimate. On the right, leverage is shown on a base-ten logarithmic scale, retaining its large early wing estimates. <bookmark mark='b'/> Initially the particles occupy almost one point. In unsupported grid wings the kernel denominator can underflow, and the conditional-variance floor can produce leverage above a thousand. Those values are numerical estimates, not evidence for an economic leverage spike. The original algorithm interpolates this grid without a leverage cap. More central and later estimates are much smaller. The particle calculation calibrates as it simulates, with measurable repricing error."""
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(gl), FadeIn(leg), FadeIn(src), FadeIn(cur))
            vo.wait_until("a")
            self.play(FadeIn(note_))
            per = max((vo.remaining(1.5) - 0.5) / (len(snaps) - 1), 0.4)
            for k in range(1, len(snaps)):
                self.play(Transform(cur, frame(k)), run_time=per, rate_func=linear)
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def surface3d(self, s):
        grid = np.asarray(s["grid"])
        Ls = s["L"]
        ts = np.array([z["t"] * 365 for z in Ls])
        m = np.ones_like(grid, dtype=bool)
        xg = grid[m]
        Z = np.log10(np.array([np.asarray(z["L"])[m] for z in Ls]))
        ax = ThreeDAxes(x_range=[-1, 1, 0.5], y_range=[ts[0], ts[-1], 30], z_range=[-0.2, 3.2, 1], x_length=6.4,
                        y_length=5.4, z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.3)
        slices = VGroup(*[VMobject(stroke_color=MODEL_COL["SLV"], stroke_width=3).set_points_as_corners(
            [ax.c2p(x, t, z) for x, z in zip(xg, row)]) for t, row in zip(ts, Z)])

        def f(x, y):
            j = int(np.clip(np.searchsorted(ts, y) - 1, 0, len(ts) - 2))
            w = (y - ts[j]) / (ts[j + 1] - ts[j])
            return float(np.interp(x, xg, (1 - w) * Z[j] + w * Z[j + 1]))

        surf = price_surface(ax, f, [-1, 1], [ts[0], ts[-1]], resolution=(20, 12), z_lo=-0.2, z_hi=3.2, opacity=0.6)
        one = Polygon(ax.c2p(-1, ts[0], 0), ax.c2p(1, ts[0], 0), ax.c2p(1, ts[-1], 0), ax.c2p(-1, ts[-1], 0),
                      stroke_width=0, fill_color=GREY_C, fill_opacity=0.2)
        hint = label('Raw leverage grids, 10--120 days: height $log_{10} L$; grey plane $L=1$. Sparse wings are numerically sensitive.', font_size=20, color=GREY_A).to_corner(UL, buff=0.35)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-120 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            (
            """Stack the saved leverage grids from ten to a hundred and twenty days. The height is log ten of leverage; the grey plane is leverage one. <bookmark mark='a'/> This preserves the raw wing estimates instead of flattening them at a display cap. Early unsupported wings and the variance floor can dominate the height. Around the money, leverage is near one or below it in this fit. These grids illustrate the numerical particle method; they are not a smooth, uniquely identified market leverage surface."""
        )
        ) as vo:
            self.play(Create(ax), FadeIn(one), FadeIn(hint), run_time=1.2)
            self.play(LaggedStart(*[Create(l_) for l_ in slices], lag_ratio=0.25), run_time=3)
            vo.wait_until("a")
            self.play(Create(surf), run_time=1.5)
            self.move_camera(theta=-55 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(1.0) - 0.3, 1.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, slices, one)), FadeOut(hint)],
                         run_time=0.8)
        self.clear_scene(run_time=0.35)

    def lab(self, s):
        card = lab_card(r"the particle step", LAB_SLV, source="explainer/quant/house/stochvol.py: slv_paths", width=9.4)
        card.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.4)
        rep = s["reprice"]
        outs = ["slv_paths(lv, heston_x, 120, 40_000, mix=0.5)  # repricing error, 13 strikes"]
        outs += [f"  day {r['days']:>3}: {r['err']:.2f} vol points" for r in rep]
        with self.voiceover(
            (
            (
            f"""The code uses a subsample, Silverman's bandwidth, kernel weights, and a matrix product for conditional variance, then interpolates leverage and takes Euler steps. The implementation protects the weight denominator and floors the estimated variance. <bookmark mark='a'/> With forty thousand particles over a hundred and twenty days, repricing error is {rep[0]['err']:.2f} vol points at thirty days and {rep[-1]['err']:.2f} at a hundred and twenty. This includes simulation error, time stepping, kernel bias, subsampling, interpolation, floors and the local-volatility approximation. It cannot all be assigned to Monte Carlo noise."""
        )
        )
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=3)
        self.wait(0.6)
        self.clear_scene(run_time=0.35)

    def convergence(self, sp):
        E = sp["err"]
        Ns = sp["Ns"]
        seeds = sp["seeds"]
        g = axes([np.log10(1500), np.log10(55000)], [0, 2.4], x_length=6.2, y_length=4.0, xlabel=r"particles $N$ (log scale)",
                 ylabel=r"repricing error, vol points (mean of 4 dates)", xticks=[np.log10(n) for n in Ns],
                 xfmt=lambda u: f"{10 ** u:,.0f}".replace(",", "{,}"), yticks=[0, 0.5, 1.0, 1.5, 2.0], log_x=True,
                 font_size=15).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        lx = np.log10(np.asarray(Ns, float))
        runs = np.array([[np.mean(E[f"{n}_{s_}"]) for n in Ns] for s_ in seeds])
        bandm = seed_band(g.ax, lx, np.clip(runs, 0, 2.4), MODEL_COL["SLV"])
        dots = VGroup(*[Dot(g.ax.c2p(x, min(y, 2.4)), radius=0.05, color=GREY_B) for row in runs for x, y in zip(lx, row)])
        ref = runs.mean(0)[0] * (np.asarray(Ns, float) / Ns[0]) ** (-0.4)
        refl = DashedLine(g.ax.c2p(lx[0], ref[0]), g.ax.c2p(lx[-1], ref[-1]), stroke_color=GREY_C, stroke_width=2)
        bw = {b: np.mean([np.mean(E[f"bw{b:g}_{s_}"]) for s_ in seeds]) for b in sp["bws"]}
        mid = np.mean(runs[:, 1])
        slope = float(np.polyfit(lx, np.log10(runs.mean(0)), 1)[0])
        side = VGroup(
            MathTex(rf"\text{{slope}}\ {slope:.2f}\ \ (\text{{heuristic}}\ {-0.4:.1f})", font_size=30, color=MODEL_COL["SLV"]),
            wrapped_label(r"three seeds per $N$: the band is their spread; the error includes the Monte Carlo noise of the "
                          r"repricing itself", 4.4, 18, GREY_A),
            MathTex(rf"N = 8{{,}}000:\ \ h \times \tfrac12: {bw[0.5]:.2f},\ \ h: {mid:.2f},\ \ h \times 2: {bw[2.0]:.2f}",
                    font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        falls = runs.mean(0)[-1] < runs.mean(0)[0]
        v1 = (f"The error falls from {runs.mean(0)[0]:.2f} vol points with two thousand particles to "
              f"{runs.mean(0)[-1]:.2f} with forty thousand, a slope of {slope:.2f} on log scales, against the "
              "heuristic's minus zero point four." if falls else
              f"The error does not fall with N here: {runs.mean(0)[0]:.2f} at two thousand, {runs.mean(0)[-1]:.2f} at "
              "forty thousand; the time step and the local volatility's own error dominate.")
        best_bw = min(bw.items(), key=lambda kv: kv[1])
        v2 = (f"Halving the window gives {bw[0.5]:.2f}, doubling it {bw[2.0]:.2f}, against {mid:.2f} for Silverman's "
              "choice: the trade-off is real, and shallow.")
        src = illustration(r"repricing the Surface's smile at 30, 60, 90 and 120 days, 13 strikes")
        with self.voiceover(
            (
            "How many particles are enough? Two thousand, eight thousand and forty thousand, three seeds each. "
            f"<bookmark mark='a'/> {v1} <bookmark mark='b'/> At small N the seed band is wide: the leverage and the "
            f"repricing check are both noisy. <bookmark mark='c'/> And the bandwidth, at eight thousand: {v2}"
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(bandm), Create(refl), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)

    def cards(self):
        c1 = history_card(2007, r"Ren, Madan and Qian; Lipton (2002)",
                          r"The PDE route: solve the forward Kolmogorov equation for the joint density of $(S, v)$ on a "
                          r"grid, and read $\mathbb{E}[v \mid S]$ off it. Accurate in one factor, hard in more.",
                          color=QC.IDEA, width=5.6)
        c2 = history_card(2025, r"Reisinger and Tsianni (arXiv 2504.14343)",
                          'Fixed-bandwidth regularized SLV: particle convergence and Euler time convergence require distinct Feller and regularity conditions.', color=QC.IDEA, width=5.6)
        G = VGroup(c1, c2).arrange(RIGHT, buff=0.4, aligned_edge=UP)
        pp = pause(r"Set the vol of vol to zero. What is $L$?", width=4.4).to_corner(DR, buff=0.3)
        with self.voiceover(
            (
            """The PDE route solves for the joint density on a grid. <bookmark mark='a'/> Reisinger and Tsianni's 2025 work studies a regularized, fixed-bandwidth Heston-type particle system. Its propagation-of-chaos result uses a Feller ratio at least one and a critical-time restriction. A separate Euler time-discretization result approaches order one half, up to logarithms, under the stronger Feller condition above two plus root three. These are different limits. Our default eta of one half raises the effective Feller ratio to about one point four eight: above one but below that time-step threshold. The remaining regularity and algorithm conditions have not been verified here. <bookmark mark='b'/> Set vol of vol to zero: leverage is local volatility divided by deterministic root variance. This gives the local-volatility diffusion, in the ideal identity."""
        )
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene(run_time=0.35)
