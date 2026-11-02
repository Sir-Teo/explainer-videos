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
        self.play(FadeOut(c))

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
                why(r"Gy\"ongy's theorem (Part 12): the model has local vol's marginals, so it reprices every vanilla "
                    r"exactly, when this holds", 20),
                why(r"so $L$ depends on the joint law of the model it drives: a McKean--Vlasov SDE, nonlinear in the "
                    r"sense of McKean", 20),
                why(r"Guyon and Henry-Labord\`ere (2012): estimate the conditional expectation across the simulated "
                    r"particles themselves, by kernel regression (Nadaraya--Watson), with Silverman's bandwidth", 20),
                why(r"kernel regression's trade-off: a wide window is biased, a narrow one noisy; balancing them gives "
                    r"the rate, as a heuristic", 20)]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.0, buff=0.8, edge=6.9)
        with self.voiceover(
            (
            "Local volatility fits today exactly and predicts the wrong future; stochastic volatility the reverse. "
            "Desks multiply them: Heston's variance, vol of vol scaled by a mixing fraction eta, times a leverage "
            "function. <bookmark mark='a'/> By Gyöngy, it reprices every vanilla when leverage squared times the "
            "expected variance given the price equals Dupire's local variance. <bookmark mark='b'/> But that "
            "expectation is under the model's own law, which depends on the leverage: a McKean–Vlasov equation. "
            "<bookmark mark='c'/> Guyon and Henry-Labordère's 2012 cut: simulate particles together, and at each "
            "step estimate the expectation across them by kernel regression. <bookmark mark='d'/> The window trades "
            "bias against noise, which suggests an error falling like N to the minus two fifths: a heuristic, "
            "measured below."
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
        self.clear_scene()

    def particles(self, sp):
        snaps = sp["snaps"]
        grid = np.asarray(sp["grid"])
        g = axes([-0.6, 0.6], [0, 1.6], x_length=7.0, y_length=4.2, xlabel=r"log-moneyness $x = \ln S/S_0$",
                 ylabel=r"variance $v$", xticks=[-0.5, -0.25, 0, 0.25, 0.5], yticks=[0, 0.4, 0.8, 1.2, 1.6], font_size=15)
        g.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        gl = axes([-0.6, 0.6], [0, 2.5], x_length=4.2, y_length=2.4, xlabel=r"$x$", ylabel=r"leverage $L(x, t)$",
                  xticks=[-0.5, 0, 0.5], yticks=[0, 1, 2], font_size=13).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)

        def frame(k):
            z = snaps[k]
            x, v = np.asarray(z["x"]), np.asarray(z["v"])
            ok = (np.abs(x) < 0.6) & (v < 1.6)
            cloud = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.022, color=VAR, fill_opacity=0.55) for a, b in zip(x[ok], v[ok])])
            ev = curve(g.ax, grid, np.clip(np.asarray(z["Ev"]), 0, 1.6), IV, stroke_width=4)
            L = curve(gl.ax, grid, np.clip(np.asarray(z["L"]), 0, 2.5), MODEL_COL["SLV"], stroke_width=3)
            day = MathTex(rf"\text{{day}}\ {z['day']}", font_size=30, color=WHITE).next_to(g, UP, buff=0.05).align_to(g, RIGHT)
            return VGroup(cloud, ev, L, day)

        cur = frame(0)
        leg = legend([(VAR, r"particles (900 of 8{,}000)"), (IV, r"$\mathbb{E}[v \mid x]$, kernel estimate")],
                     font_size=17).next_to(g, UP, buff=0.12).align_to(g, LEFT)
        note_ = wrapped_label(r"each step: estimate $\mathbb{E}[v \mid x]$ across the cloud, set $L = \sigma_{\text{loc}}/"
                              r"\sqrt{\mathbb{E}[v \mid x]}$, move every particle with that $L$", 4.2, 18, GREY_A)
        note_.next_to(gl, DOWN, buff=0.4).align_to(gl, LEFT)
        src = illustration(r"the House's particle method on the Surface's SSVI local vol; Heston from chapter 4, $\eta = \tfrac12$")
        with self.voiceover(
            (
            "Here it runs. Each dot is a particle, a log price and a variance, all starting together. "
            "<bookmark mark='a'/> At each step the gold curve is the kernel estimate of the expected variance given "
            "the price; right, the leverage it implies; then every particle steps with the leverage at its own price. "
            "<bookmark mark='b'/> The cloud fans out and tilts: with negative correlation, particles that fell carry "
            "high variance. Where the cloud is too wild for the market's local volatility the leverage dips below "
            "one; too calm, it lifts. The model calibrates while it simulates."
        )
        ) as vo:
            self.play(FadeIn(g), FadeIn(gl), FadeIn(leg), FadeIn(src), FadeIn(cur))
            vo.wait_until("a")
            self.play(FadeIn(note_))
            per = max((vo.remaining(1.5) - 0.5) / (len(snaps) - 1), 0.4)
            for k in range(1, len(snaps)):
                self.play(Transform(cur, frame(k)), run_time=per, rate_func=linear)
        self.wait(0.4)
        self.clear_scene()

    def surface3d(self, s):
        grid = np.asarray(s["grid"])
        Ls = s["L"]
        ts = np.array([z["t"] * 365 for z in Ls])
        m = np.abs(grid) <= 0.5
        xg = grid[m]
        Z = np.clip(np.array([np.asarray(z["L"])[m] for z in Ls]), 0.3, 2.2)
        ax = ThreeDAxes(x_range=[-0.5, 0.5, 0.25], y_range=[ts[0], ts[-1], 30], z_range=[0.3, 2.2, 0.5], x_length=6.4,
                        y_length=5.4, z_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.3)
        slices = VGroup(*[VMobject(stroke_color=MODEL_COL["SLV"], stroke_width=3).set_points_as_corners(
            [ax.c2p(x, t, z) for x, z in zip(xg, row)]) for t, row in zip(ts, Z)])

        def f(x, y):
            j = int(np.clip(np.searchsorted(ts, y) - 1, 0, len(ts) - 2))
            w = (y - ts[j]) / (ts[j + 1] - ts[j])
            return float(np.interp(x, xg, (1 - w) * Z[j] + w * Z[j + 1]))

        surf = price_surface(ax, f, [-0.5, 0.5], [ts[0], ts[-1]], resolution=(20, 12), z_lo=0.5, z_hi=1.8, opacity=0.6)
        one = Polygon(ax.c2p(-0.5, ts[0], 1), ax.c2p(0.5, ts[0], 1), ax.c2p(0.5, ts[-1], 1), ax.c2p(-0.5, ts[-1], 1),
                      stroke_width=0, fill_color=GREY_C, fill_opacity=0.2)
        hint = label(r"the leverage function $L(x, t)$ the particles found, over log-moneyness and 10 to 120 days; "
                     r"grey plane: $L = 1$", font_size=20, color=GREY_A).to_corner(UL, buff=0.35)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-120 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            (
            "Stack the leverage every ten days into a surface over price and time. <bookmark mark='a'/> Below one "
            "near the money, rising in the wings, steepest at short dates, and flattening toward one as the random "
            "variance carries more of the load."
        )
        ) as vo:
            self.play(Create(ax), FadeIn(one), FadeIn(hint), run_time=1.2)
            self.play(LaggedStart(*[Create(l_) for l_ in slices], lag_ratio=0.25), run_time=3)
            vo.wait_until("a")
            self.play(Create(surf), run_time=1.5)
            self.move_camera(theta=-55 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(1.0) - 0.3, 1.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, surf, slices, one)), FadeOut(hint)],
                         run_time=1.5)
        self.clear_scene()

    def lab(self, s):
        card = lab_card(r"the particle step", LAB_SLV, source="explainer/quant/house/stochvol.py: slv_paths", width=9.4)
        card.to_edge(UP, buff=0.35).to_edge(LEFT, buff=0.4)
        rep = s["reprice"]
        outs = ["slv_paths(lv, heston_x, 120, 40_000, mix=0.5)  # repricing error, 13 strikes"]
        outs += [f"  day {r['days']:>3}: {r['err']:.2f} vol points" for r in rep]
        with self.voiceover(
            (
            (
            "The step itself, eleven lines: a subsample, Silverman's bandwidth, kernel weights, one matrix product "
            "for the conditional variance, the leverage, and an Euler step for every particle. "
            "<bookmark mark='a'/> Forty thousand particles, a hundred and twenty days: the model reprices the "
            f"Surface's smile to {rep[0]['err']:.2f} vol points at thirty days and {rep[-1]['err']:.2f} at a hundred "
            "and twenty, the remainder being Monte Carlo noise and the finite differences in local volatility."
        )
        )
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, outs, run_time=3)
        self.wait(0.6)
        self.clear_scene()

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
        self.clear_scene()

    def cards(self):
        c1 = history_card(2007, r"Ren, Madan and Qian; Lipton (2002)",
                          r"The PDE route: solve the forward Kolmogorov equation for the joint density of $(S, v)$ on a "
                          r"grid, and read $\mathbb{E}[v \mid S]$ off it. Accurate in one factor, hard in more.",
                          color=QC.IDEA, width=5.6)
        c2 = history_card(2025, r"Reisinger and Tsianni (arXiv 2504.14343)",
                          r"For the calibrated Heston-type SLV particle system: well-posedness, propagation of chaos, and a "
                          r"strong convergence rate of one half.", color=QC.IDEA, width=5.6)
        G = VGroup(c1, c2).arrange(RIGHT, buff=0.4, aligned_edge=UP)
        pp = pause(r"Set the vol of vol to zero. What is $L$?", width=4.4).to_corner(DR, buff=0.3)
        with self.voiceover(
            (
            "The rival is the PDE route of Ren, Madan and Qian, and Lipton: solve for the joint density on a grid. "
            "<bookmark mark='a'/> The theory is recent: Reisinger and Tsianni proved in 2025 that this particle "
            "system converges, at rate one half. <bookmark mark='b'/> Pause: set the vol of vol to zero. The leverage "
            "is local vol over the deterministic root variance: local volatility. The next chapter turns that dial."
        )
        ) as vo:
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(pp))
        self.wait(0.4)
        self.clear_scene()
