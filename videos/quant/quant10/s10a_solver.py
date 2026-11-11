from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import GAIN, IMP, LOSS, OPT, PART, SPOT, THE, computed, load


class Solver(VoiceoverScene, ThreeDScene):
    def construct(self):
        d = load("implied")
        r = load("solver_race")
        self.card()
        self.invert(d)
        self.sheet(r)
        self.lab(r)
        self.race(r)

    def card(self):
        c = chapter_card(11, r"Turning the formula inside out", r"What volatility is the market charging?",
                         lit=(1987,), part=PART)
        with self.voiceover("Chapter eleven. Turning the formula inside out: implied volatility."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def invert(self, d):
        F, K, T, target = d["solver_F"], d["solver_K"], d["solver_T"], d["solver_price"]
        sig = np.linspace(0.05, 1.2, 200)
        prices = bs.price(F, K, T, sig) / 1000
        g = axes([0, 1.2], [0, 17.5], x_length=6.6, y_length=4.2, xlabel=r"volatility $\sigma$",
                 ylabel=r"undiscounted Black forward value, thousands", xticks=[0.25, 0.5, 0.75, 1.0],
                 yticks=[0, 5, 10, 15], xfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, sig, prices, OPT, stroke_width=4)
        tgt = DashedLine(ax.c2p(0, target / 1000), ax.c2p(1.2, target / 1000), color=GREY_B, stroke_width=1.5)
        tgt_lab = MathTex(rf"\text{{model forward value}}\ \${target:,.0f}".replace(",", "{,}"), font_size=26, color=GREY_A)
        tgt_lab.next_to(ax.c2p(1.2, target / 1000), UP, buff=0.1).shift(LEFT * 1.2)
        its = np.asarray(d["solver_iters"], float)
        dot = glow_dot(ax.c2p(its[-1], target / 1000), color=IMP, radius=0.07)
        drop = DashedLine(ax.c2p(its[-1], target / 1000), ax.c2p(its[-1], 0), color=IMP, stroke_width=2)
        quote = VGroup(
            label(r"quote-IV repricing, 10 December 2025, 08:00 UTC", font_size=24, color=GREY_A),
            label(rf"a BTC call, strike \${K:,.0f}, {T * 365:.0f} days".replace(",", "{,}"), font_size=26),
            label(rf"forward \${F:,.0f} (from put--call parity)".replace(",", "{,}"), font_size=24, color=SPOT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.5)
        rows = VGroup(*[MathTex(rf"\sigma_{{{i}}} = {100 * v:.10f}\%", font_size=28,
                                color=IMP if i == len(its) - 1 else GREY_A) for i, v in enumerate(its)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(quote, DOWN, buff=0.5).align_to(quote, LEFT)
        rows_lab = VGroup(label(r"initial guess: Corrado--Miller", font_size=20, color=GREY_B),
                          label(r"then Newton steps, kept inside a bisection bracket", font_size=20, color=GREY_B))
        rows_lab.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(rows, DOWN, buff=0.3).align_to(rows, LEFT)
        with self.voiceover(
            f"""Traders invert a pricing model: given a price, find its implied volatility. Carry, discounting and settlement conventions are part of that conversion. <bookmark mark='a'/> Here we take one Bitcoin call's fitted forward and Surface IV reconstructed from mark prices from the tenth of December 2025, generate its undiscounted Black forward value, and invert that value. This checks numerical recovery of an input IV, rather than matching an independent execution price. <bookmark mark='b'/> From a Corrado-Miller approximation, guarded Newton steps recover {100 * its[-1]:.2f} percent. Numerical recovery does not establish market-price accuracy."""
        ) as vo:
            self.play(FadeIn(g), Create(line))
            vo.wait_until("a")
            self.play(FadeIn(quote), Create(tgt), FadeIn(tgt_lab))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), FadeIn(rows_lab[0]))
            for r in rows[1:]:
                self.play(FadeIn(r), run_time=0.6)
            self.play(FadeIn(rows_lab[1]), FadeIn(dot, scale=1.5), Create(drop))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sheet(self, r):
        xs, ss, B = np.asarray(r["bx"], float), np.asarray(r["bs_"], float), np.asarray(r["B"], float)
        ax = ThreeDAxes(x_range=[-1, 1, 0.5], y_range=[0, 1.2, 0.3], z_range=[0, 1.2, 0.4], x_length=7.6,
                        y_length=5.6, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.4)

        def bfun(a, s_):
            from scipy.special import ndtr
            s_ = max(s_, 1e-3)
            return float(np.exp(a / 2) * ndtr(a / s_ + s_ / 2) - np.exp(-a / 2) * ndtr(a / s_ - s_ / 2))

        surf = Surface(lambda u, v: ax.c2p(u, v, bfun(u, v)), u_range=[-1, 1], v_range=[0.02, 1.2],
                       resolution=(28, 24))
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.Q, 0), (OPT, 0.25), (WHITE, 1.2)], axis=2)
        surf.set_style(fill_opacity=0.65, stroke_width=0.3, stroke_color=GREY_D)
        beta = 0.12
        plane = Surface(lambda u, v: ax.c2p(u, v, beta), u_range=[-1, 1], v_range=[0.02, 1.2], resolution=(2, 2))
        plane.set_style(fill_color=IMP, fill_opacity=0.25, stroke_width=0)
        # where the sheet crosses the plane: the implied total volatility for each x
        from scipy.optimize import brentq
        cx = np.linspace(-0.9, 0.9, 37)
        cs = [brentq(lambda s_: bfun(a, s_) - beta, 1e-3, 1.2) if bfun(a, 1e-3) < beta < bfun(a, 1.2) else np.nan
              for a in cx]
        cross = VMobject(stroke_color=IMP, stroke_width=5).set_points_smoothly(
            [ax.c2p(a, s_, beta) for a, s_ in zip(cx, cs) if np.isfinite(s_)])
        corner = Dot3D(ax.c2p(-0.9, 0.08, bfun(-0.9, 0.08)), radius=0.1, color=LOSS)
        hint = VGroup(label(r"log-moneyness $x = \ln(F/K)$", font_size=24, color=SPOT),
                      label(r"total volatility $s = \sigma\sqrt T$", font_size=24, color=IMP),
                      label(r"normalized price $b = C / \sqrt{FK}$", font_size=24, color=OPT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        C = {r"b": OPT, r"s": IMP, r"x": SPOT}
        eqs = VGroup(
            cmath(r"b(x, s)", r"=", r"e^{x/2}N\!\left(\tfrac{x}{s} + \tfrac{s}{2}\right) - e^{-x/2}N\!\left("
                  r"\tfrac{x}{s} - \tfrac{s}{2}\right)", font_size=26, colors=C),
            cmath(r"\partial_s b", r"=", r"e^{x/2}\varphi(d_1) > 0", r"\Rightarrow", r"\text{one } s", font_size=26,
                  colors=C),
            cmath(r"b(0, s)", r"=", r"2N(s/2) - 1", r"\approx", r"0.3989\,s", font_size=26, colors=C),
            cmath(r"s_{n+1}", r"=", r"s_n - \frac{b(s_n) - \beta}{\partial_s b(s_n)}", font_size=26, colors=C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.35)
        whys_ = VGroup(*[note(t, font_size=17) for t in (
            r"divide by $\sqrt{FK}$: five inputs become two",
            r"vega is positive; between the no-arbitrage bounds, exactly one root",
            r"at the money: $C \approx 0.4\,F\sigma\sqrt T$ (Brenner--Subrahmanyam 1988)",
            r"Newton; where vega is tiny, bracket it, or start close (Corrado--Miller 1996; J\"ackel 2015)")])
        for e_, w_ in zip(eqs, whys_):
            w_.next_to(e_, DOWN, buff=0.04).align_to(e_, LEFT)
        eqs_all = VGroup(*[VGroup(e_, w_) for e_, w_ in zip(eqs, whys_)]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        eqs_all.to_corner(DR, buff=0.3)  # the lower right stays empty in every camera view
        for g_ in eqs_all:
            g_.add_to_back(BackgroundRectangle(g_, color=BACKGROUND, fill_opacity=1.0, buff=0.08))
        self.set_camera_orientation(phi=66 * DEGREES, theta=-62 * DEGREES, zoom=0.72)
        for m in (hint, eqs_all):
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        with self.voiceover(
            """When does a finite positive IV exist? With positive forward, strike and time, the price must lie strictly between intrinsic value and the upper bound, in the chosen discounted or forward units. At the boundaries the limits are zero or infinite volatility; inconsistent quotes have no such solution. Normalize by root forward times strike: price depends on log-moneyness x and total volatility s. <bookmark mark='a'/> Vega is positive, giving uniqueness inside those bounds. At the money the forward value is nearly point four s. <bookmark mark='b'/> Deep out of the money near expiry, vega is tiny: price errors amplify into large IV errors. Brackets protect Newton. Jaeckel's 2015 method uses careful transformations and high-order refinement for floating-point precision in its supported domain."""
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.5)
            self.play(FadeIn(surf), FadeIn(eqs_all[0]), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(plane), FadeIn(eqs_all[1]))
            self.play(Create(cross), FadeIn(eqs_all[2]), run_time=2)
            vo.wait_until("b")
            self.move_camera(phi=72 * DEGREES, theta=-100 * DEGREES, zoom=0.8, added_anims=[FadeIn(corner),
                                                                                          FadeIn(eqs_all[3])],
                             run_time=3)
            self.wait(max(vo.remaining(1.0) - 1.0, 0.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)]))], run_time=0.5)
        self.clear_scene(run_time=0.1)

    # ------------------------------------------------------------------
    def lab(self, r):
        card = lab_card(r"the House's implied-volatility solver", [
            "for _ in range(max_iter):",
            "    f = norm_price(s) - target",
            "    lo = np.where(f < 0, s, lo)        # the bracket",
            "    hi = np.where(f > 0, s, hi)",
            "    step = s - f / norm_vega(s)        # Newton",
            "    ok = np.isfinite(step) & (step > lo) & (step < hi)",
            "    s_new = np.where(ok, step, 0.5 * (lo + hi))",
            "    s_new = np.where(conv, s, s_new)   # freeze the done",
            "    conv |= abs(s_new - s) < tol * max(1, s)",
            "    s = s_new",
        ], source="explainer/quant/house/bs.py (implied_vol, abridged)", width=7.6).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The House's loop: tighten a bracket, try a Newton step, halve the bracket if the step lands outside. "
            "One line is new in this part: converged quotes are frozen while the others iterate; before, the "
            "fallback could knock a finished quote out of place. <bookmark mark='a'/> On all "
            f"{r['n']} quotes of the Surface: a median of {r['median']:.0f} iterations to ten decimals, "
            f"{r['p90']:.0f} for nine in ten, {r['max']} at worst, for a {r['worst_T_days']:.0f}-day call far "
            "out of the money."
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            lab_run(self, card, [f"implied_vol(prices, F, K, T, cp=cp)   # {r['n']} quotes",
                                 f"iterations to 1e-10: median {r['median']:.0f}, p90 {r['p90']:.0f}, max {r['max']}",
                                 f"slowest: {r['worst_T_days']:.0f} days, ln(K/F) = {r['worst_k']:+.2f}, "
                                 f"vol {100 * r['worst_iv']:.1f}%"])
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def race(self, r):
        k, iv = np.asarray(r["k"], float), np.asarray(r["iv"], float)
        H, Nv = np.asarray(r["house_paths"], float), np.asarray(r["naive_paths"], float)
        n_it = H.shape[0]
        keep = np.abs(k) <= 0.9
        left = axes([-0.9, 0.9], [0, 2.6], x_length=6.0, y_length=4.2, xlabel=r"log-moneyness $\ln(K/F)$",
                    ylabel=r"implied volatility", xticks=[-0.6, 0, 0.6], yticks=[0.5, 1, 2, 2.5],
                    yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=18).to_edge(LEFT, buff=0.5).shift(DOWN * 0.4)
        right = axes([0, n_it - 1], [-15, 27], x_length=5.2, y_length=4.2, xlabel=r"iteration",
                     ylabel=r"stored max error (log); invalid sentinel 9.99", xticks=[0, 4, 8, 12], yticks=[-15, -5, 5, 15, 25],
                     yfmt=lambda v: f"10^{{{int(v)}}}", font_size=18).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.4)
        it = ValueTracker(0)

        def dots(P, col):
            def f():
                i = min(int(round(it.get_value())), n_it - 1)
                y = P[i]
                return VGroup(*[Dot(left.ax.c2p(a, b), radius=0.03, color=col, fill_opacity=0.8)
                                for a, b in zip(k[keep], y[keep]) if np.isfinite(b)])
            return always_redraw(f)

        hm = np.log10(np.maximum(np.asarray(r["house_max"], float), 1e-15))
        nm = np.log10(np.maximum(np.asarray(r["naive_max"], float), 1e-15))
        its = np.arange(n_it)

        def err(line, col):
            def f():
                j = int(it.get_value()) + 1
                return curve(right.ax, its[:max(j, 2)], line[:max(j, 2)], col, stroke_width=3.5)
            return always_redraw(f)

        leg = legend([(IMP, r"the House: Corrado--Miller start, bracketed Newton"),
                      (LOSS, r"Newton: 50\% start; stored dots $0<\sigma<3$")], font_size=20).to_edge(UP, buff=0.4)
        truth = VGroup(*[Dot(left.ax.c2p(a, b), radius=0.022, color=GREY_B) for a, b in zip(k[keep], iv[keep])])
        cnt = always_redraw(lambda: MathTex(rf"\text{{iteration}}\ {int(it.get_value())}", font_size=28, color=IMP)
                            .next_to(left, UP, buff=0.1))
        with self.voiceover(
            f"Now all {r['n']} quotes solve at once. Left, grey: the true smile; each orange dot starts at the House's first guess and jumps onto it. Right: the worst error, on a log scale. <bookmark mark='a'/> By iteration {int(np.argmax(hm < -9))} the worst error is below ten to the minus nine. <bookmark mark='b'/> In red, plain Newton from a flat fifty percent: {r['naive_broke']} quotes are thrown to infinity or below zero, {r['naive_unfinished']} never return. Pause and predict: a far out-of-the-money quote one hundredth of a percent of the forward too high. How wrong is its volatility? On the slowest quote, {100 * r['tick_shift']:.0f} points. Next: the solver, run on a real smile. The dot panel shows absolute log-moneyness at most point nine and only stored positive IVs below three. Nonfinite stored iterates are omitted, not moved to an edge. The unchanged diagnostic substitutes nine point nine nine for a nonfinite error; its finite spikes are shown without an upper cap."
        ) as vo:
            self.play(FadeIn(left), FadeIn(right), FadeIn(truth), FadeIn(leg[0]))
            dh, eh = dots(H, IMP), err(hm, IMP)
            self.add(dh, eh, cnt)
            self.play(it.animate.set_value(n_it - 1), run_time=max(vo.until("a") - 0.5, 4.0), rate_func=linear)
            dh.clear_updaters()
            eh.clear_updaters()
            vo.wait_until("b")
            it.set_value(0)
            dn, en = dots(Nv, LOSS), err(nm, LOSS)
            self.play(FadeOut(dh), FadeIn(leg[1]))
            self.add(dn, en)
            self.play(it.animate.set_value(n_it - 1), run_time=5, rate_func=linear)
            dn.clear_updaters()
            en.clear_updaters()
            self.play(FadeIn(computed()))
        cnt.clear_updaters()
        self.wait(0.4)
        self.clear_scene()
