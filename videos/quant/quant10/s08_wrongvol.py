from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import GAIN, GAM, IMP, LOSS, OPT, PART, REA, SPOT, THE, computed, load

C_ = {r"\Gamma^h": GAM, r"\sigma_h^2": IMP, r"\sigma_t^2": REA, r"\sigma_h": IMP, r"\sigma_t": REA, r"V^h": OPT,
      r"S": SPOT, r"S^2": SPOT}


def row(*parts, fs=34):
    return cmath(*parts, colors=C_, font_size=fs)


class WrongVol(VoiceoverScene, ThreeDScene):
    def construct(self):
        w = load("wrong_vol")
        self.card()
        self.proof()
        self.mountain(w, load("dgamma3d"))
        self.choice(load("hedge_choice"))
        self.heston(w)

    def card(self):
        c = chapter_card(8, r"Hedging with the wrong volatility", r"Does it matter when the moves happen?",
                         lit=(1993,), part=PART)
        with self.voiceover("Chapter eight. Hedging with the wrong volatility."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def proof(self):
        rows = [
            row(r"V^h_t", r"+", r"\tfrac12", r"\sigma_h^2", r"S^2", r"V^h_{SS}", r"=", r"0"),
            row(r"dV^h", r"=", r"V^h_t\,dt", r"+", r"V^h_S\,dS", r"+", r"\tfrac12", r"V^h_{SS}", r"\,", r"\sigma_t^2",
                r"S^2", r"\,dt"),
            row(r"dV^h - V^h_S\,dS", r"=", r"\tfrac12", r"\Gamma^h", r"S^2", r"\big(", r"\sigma_t^2", r"-",
                r"\sigma_h^2", r"\big)\,dt"),
            row(r"\text{P\&L}_T", r"=", r"\tfrac12\int_0^T", r"\Gamma^h", r"S^2", r"\big(", r"\sigma_h^2", r"-",
                r"\sigma_t^2", r"\big)\,dt", fs=40),
            row(r"\sigma_t \le \sigma_h,\ ", r"\Gamma^h", r"\ge 0", r"\ \Rightarrow\ ", r"\text{P\&L}_T \ge 0"),
        ]
        whys = [why(r"the price at the hedge volatility $\sigma_h$ solves Black--Scholes ($r = 0$)"),
                why(r"It\^o under the true dynamics: the stock's variance is $\sigma_t^2$, whatever it is"),
                why(r"self-financing gains: $dV^h - V^h_S\,dS$; include cash when rebalancing"),
                why(r"short the option at $\sigma_h$ and integrate: the payoff is $V^h_T$"),
                why(r"a convex payoff: El Karoui, Jeanblanc and Shreve (1998)")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-2.2, buff=0.6, edge=6.9)
        with self.voiceover(
            """Let the true instantaneous volatility vary with time and the path, while the call is priced and hedged at a fixed sigma h. Assume a continuous stock diffusion, zero rates, no costs, continuous self-financing trading, and sufficient regularity and integrability. <bookmark mark='a'/> Ito uses the true variance sigma t squared. <bookmark mark='b'/> Subtract delta times the stock gain from the option's differential. This is not the differential of option minus delta times stock, which would include changes in delta. <bookmark mark='c'/> Integrating gives the short seller's variance-gap P and L. <bookmark mark='d'/> For a convex payoff, gamma is nonnegative. If true instantaneous volatility stays below sigma h almost surely, the continuous hedge super-replicates under these assumptions. El Karoui, Jeanblanc and Shreve, 1998. Jumps, discrete trading and costs fall outside this conclusion."""
        ) as vo:
            step(0, run_time=0.15)
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

    # ------------------------------------------------------------------
    def mountain(self, w, g3):
        tg, Sg, G = np.asarray(g3["t"], float), np.asarray(g3["S"], float), np.asarray(g3["G"], float)
        K, T = g3["K"], g3["T"]
        zmax = 500.0  # typical dollar gamma is about 200; only the spike in the last days before expiry is capped
        ax = ThreeDAxes(x_range=[0, T, T / 4], y_range=[88, 132, 11], z_range=[0, zmax, 100], x_length=7.6,
                        y_length=6.0, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.5)
        surf = Surface(lambda u, v: ax.c2p(u, v, min(float(np.interp(v, Sg, [np.interp(u, tg, G[:, j])
                                                                              for j in range(len(Sg))])), zmax)),
                       u_range=[0, tg[-1]], v_range=[Sg[0], Sg[-1]], resolution=(24, 20))
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.Q, 0), (GAM, 200), (WHITE, zmax)], axis=2)
        surf.set_style(fill_opacity=0.55, stroke_width=0.3, stroke_color=GREY_D)
        t = np.asarray(w["t"], float)
        k = ValueTracker(0)
        n = len(t) - 1
        cols = {"near": np.asarray(g3["col_near"], float), "far": np.asarray(g3["col_far"], float)}
        colour = {"near": SPOT, "far": REA}
        Pth = {"near": np.asarray(w["S_near"], float), "far": np.asarray(w["S_far"], float)}
        cscale = 2.6 / max(cols["near"][-1], cols["far"][-1])

        def track(name):
            def f():
                i = max(int(k.get_value()), 1)
                return VMobject(stroke_color=colour[name], stroke_width=3).set_points_as_corners(
                    [ax.c2p(a, b, 0) for a, b in zip(t[:i + 1], Pth[name][:i + 1])])
            return always_redraw(f)

        def column(name, x_off):
            def f():
                i = int(k.get_value())
                h = max(cols[name][i] * cscale, 0.02)
                return Rectangle(width=0.35, height=h, stroke_width=0, fill_color=colour[name], fill_opacity=0.9) \
                    .move_to([5.2 + x_off, -2.6 + h / 2, 0])
            return always_redraw(f)

        hint = VGroup(label(r"time", font_size=24, color=THE), label(r"stock price", font_size=24, color=SPOT),
                      label(r"dollar gamma $\tfrac12\Gamma S^2$", font_size=24, color=GAM)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        base = Line([4.7, -2.6, 0], [6.4, -2.6, 0], color=GREY_C)
        ctitle = label(r"$\int \tfrac12\Gamma S^2\,dt$", font_size=24, color=GAM).move_to([5.55, 0.6, 0])
        c_near, c_far = column("near", 0), column("far", 0.6)
        res = VGroup(MathTex(rf"\text{{P\&L}}\ {w['pnl_near']:+.2f}", font_size=26, color=SPOT),
                     MathTex(rf"\text{{P\&L}}\ {w['pnl_far']:+.2f}", font_size=26, color=REA)).arrange(DOWN, buff=0.1)
        res.next_to(base, DOWN, buff=0.15)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-65 * DEGREES, zoom=0.85)
        fixed = [hint, base, ctitle, res, c_near, c_far]
        for m in fixed:
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        with self.voiceover(
            f"""Dollar gamma is a landscape over time and spot. The displayed near-expiry spike is capped at five hundred. <bookmark mark='a'/> From twenty thousand simulated paths, select the largest and smallest integrated gamma among {w['n_band']:,} paths with realized volatility near twenty percent. This deliberately chosen pair illustrates path weighting; it is not a typical-path comparison. The paths and cumulative weights are shown together. <bookmark mark='b'/> The integrated-gamma ratio is {cols['near'][-1] / cols['far'][-1]:.1f}. Finite-step profits are {w['pnl_near']:.2f} and {w['pnl_far']:.2f}; their ratio also reflects discrete hedging and the small difference in realized variance."""
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.5)
            self.play(FadeIn(surf), run_time=2)
            self.move_camera(theta=-40 * DEGREES, run_time=max(vo.until("a") - 0.5, 1.0))
            self.add(track("near"), track("far"), c_near, c_far)
            self.play(FadeIn(base), FadeIn(ctitle))
            self.play(k.animate.set_value(n), run_time=max(vo.until("b") - 0.5, 4.0), rate_func=linear)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(Group(*[m for m in self.mobjects if not isinstance(m, ValueTracker)]))], run_time=0.5)
        self.clear_scene(run_time=0.1)

    # ------------------------------------------------------------------
    def choice(self, h):
        s30, s25 = h["stats_30"], h["stats_25"]
        lo, hi = -1.5, 6.5
        panels = VGroup()
        hist_peak = max(np.histogram(np.asarray(h[key]), bins=56, range=(lo, hi))[0].max()
                        for key in ("imp_30", "act_30"))
        for name, arr, col, st in ((r"hedged at implied, 20\%", h["imp_30"], IMP, (s30["imp_mean"], s30["imp_sd"])),
                                   (r"hedged at actual, 30\%", h["act_30"], REA, (s30["act_mean"], s30["act_sd"]))):
            g = axes([lo, hi], [0, 1.05], x_length=5.2, y_length=2.3, xlabel=r"P\&L at expiry, per 100 of stock",
                     xticks=[0, 2, 4], font_size=18)
            pnl = np.asarray(arr, float)
            hh, e = np.histogram(pnl, bins=56, range=(lo, hi))
            hh = hh / hist_peak
            bars = VGroup(*[Rectangle(width=g.ax.x_length / 56 * 0.95, height=max(g.ax.y_length * v, 0.002),
                                      stroke_width=0, fill_color=col, fill_opacity=0.85)
                            .move_to(g.ax.c2p((e[i] + e[i + 1]) / 2, 0), aligned_edge=DOWN) for i, v in enumerate(hh)])
            lock = DashedLine(g.ax.c2p(s30["locked"], 0), g.ax.c2p(s30["locked"], 1.05), color=OPT, stroke_width=1.5)
            head = label(name, font_size=24, color=col).next_to(g, UP, buff=0.12)
            stat = MathTex(rf"\text{{mean}}\ {st[0]:+.2f},\ \text{{sd}}\ {st[1]:.2f}", font_size=26, color=col)
            stat.next_to(g, DOWN, buff=0.12)
            panels.add(VGroup(g, bars, lock, head, stat))
        panels.arrange(RIGHT, buff=0.7).shift(UP * 0.5)
        top = label(r"long a 3-month call bought at 20\%; the stock realizes 30\% (20,000 paths, 252 hedges)",
                    font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        lockl = label(rf"dashed: $V(30\%) - V(20\%) = {s30['locked']:.2f}$", font_size=22, color=OPT)
        lockl.to_edge(DOWN, buff=0.75)
        mark = VGroup(*[MathTex(rf"\sigma_r = 25\%:\ \text{{sd}}\ {s25['imp_sd']:.2f}\ \text{{vs}}\ {s25['act_sd']:.2f};"
                                rf"\ \text{{losing paths}}\ {100 * s25['imp_loss']:.2f}\%\ \text{{vs}}\ "
                                rf"{100 * s25['act_loss']:.2f}\%", font_size=24, color=GREY_B)]).to_edge(DOWN, buff=0.3)
        loss_more = "the actual-volatility hedge" if s25["act_loss"] > s25["imp_loss"] else "the implied-volatility hedge"
        with self.voiceover(
            f"""Buy a call at twenty percent, then compare hedges on twenty thousand GBM paths with constant thirty-percent volatility and ten-percent annual drift. Zero rates and costs. Pause: which hedge has less terminal dispersion? <bookmark mark='a'/> Hedging at the known true volatility would lock in {s30['locked']:.2f} continuously; in steps its standard deviation is {s30['act_sd']:.2f}. <bookmark mark='b'/> Hedging at twenty gives a sample mean of {s30['imp_mean']:.2f} and standard deviation {s30['imp_sd']:.2f}. The displayed histograms share bins and a count scale. Similar sample means here are not a general equality under arbitrary physical dynamics. <bookmark mark='c'/> On the separate twenty-five-percent-volatility paths, {loss_more} has more losing paths. Knowing future constant volatility is an assumption, not an available forecast."""
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(panels[1], shift=UP * 0.2), FadeIn(lockl))
            vo.wait_until("b")
            self.play(FadeIn(panels[0], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(mark), FadeIn(computed(corner=DR).shift(UP * 0.5)))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heston(self, w):
        rv = np.asarray(w["heston_rv"], float)
        pnl = np.asarray(w["heston_pnl"], float)
        pred = np.asarray(w["heston_pred"], float)
        n = 1500
        left = axes([0.04, 0.6], [-7, 5], x_length=5.4, y_length=4.0, xlabel=r"realized volatility",
                    ylabel=r"the seller's P\&L", xticks=[0.1, 0.3, 0.5], yticks=[-6, -3, 0, 3],
                    xfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20)
        right = axes([-7, 5], [-7, 5], x_length=4.4, y_length=4.0,
                     xlabel=r"$\tfrac12\int \Gamma S^2(\sigma_i^2 - v_t)\,dt$", ylabel=r"the seller's P\&L",
                     xticks=[-6, -3, 0, 3], yticks=[-6, -3, 0, 3], font_size=20)
        VGroup(left, right).arrange(RIGHT, buff=1.1).shift(DOWN * 0.3)
        d1 = VGroup(*[Dot(left.ax.c2p(a, b), radius=0.022, color=REA, fill_opacity=0.6) for a, b in
                      zip(rv[:n], pnl[:n])])
        d2 = VGroup(*[Dot(right.ax.c2p(a, b), radius=0.022, color=GAM, fill_opacity=0.6) for a, b in
                      zip(pred[:n], pnl[:n])])
        diag = DashedLine(right.ax.c2p(-7, -7), right.ax.c2p(5, 5), color=GREY_B, stroke_width=1.5)
        be = DashedLine(left.ax.c2p(0.25, -3.5), left.ax.c2p(0.25, 5), color=IMP, stroke_width=1.5)
        c1 = MathTex(rf"\rho = {w['corr_rv']:.2f}", font_size=34, color=REA).next_to(left, UP, buff=0.2)
        c2 = MathTex(rf"\rho = {w['corr_pred']:.2f}", font_size=34, color=GAM).next_to(right, UP, buff=0.2)
        hp = w["heston"]
        params = note(rf"{len(rv):,} Heston paths (volatility of volatility {hp['xi']}, correlation {hp['rho']}); "
                      r"sold and hedged at 25\%".replace(",", "{,}", 1), font_size=20).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            f"""Across {len(rv):,} Heston paths, profit and realized volatility have correlation {w['corr_rv']:.2f}. The panels show the first fifteen hundred paths; reported correlations use all four thousand. <bookmark mark='a'/> Against each path's gamma-weighted variance-gap integral, correlation is {w['corr_pred']:.2f}. The close relation is an approximation with discrete-hedging residuals, not exact replication of stochastic volatility. A variance swap instead weights realized variance without option gamma."""
        ) as vo:
            self.play(FadeIn(left), Create(be), FadeIn(params))
            self.play(LaggedStart(*[FadeIn(d) for d in d1], lag_ratio=0.001, run_time=2.5), FadeIn(c1))
            vo.wait_until("a")
            self.play(FadeIn(right), Create(diag))
            self.play(LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.001, run_time=2.5), FadeIn(c2))
        self.wait(0.4)
        self.clear_scene()
