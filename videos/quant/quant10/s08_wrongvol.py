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
            row(r"d(V^h - V^h_S S)", r"=", r"\tfrac12", r"\Gamma^h", r"S^2", r"\big(", r"\sigma_t^2", r"-",
                r"\sigma_h^2", r"\big)\,dt"),
            row(r"\text{P\&L}_T", r"=", r"\tfrac12\int_0^T", r"\Gamma^h", r"S^2", r"\big(", r"\sigma_h^2", r"-",
                r"\sigma_t^2", r"\big)\,dt", fs=40),
            row(r"\sigma_t \le \sigma_h,\ ", r"\Gamma^h", r"\ge 0", r"\ \Rightarrow\ ", r"\text{P\&L}_T \ge 0"),
        ]
        whys = [why(r"the price at the hedge volatility $\sigma_h$ solves Black--Scholes ($r = 0$)"),
                why(r"It\^o under the true dynamics: the stock's variance is $\sigma_t^2$, whatever it is"),
                why(r"substitute the PDE; holding $V^h_S$ shares cancels the $dS$ term"),
                why(r"short the option at $\sigma_h$ and integrate: the payoff is $V^h_T$"),
                why(r"a convex payoff: El Karoui, Jeanblanc and Shreve (1998)")]
        step = ladder(self, rows, whys, keep=4, top=3.0, x=-2.2, buff=0.6, edge=6.9)
        with self.voiceover(
            "Chapter seven assumed the world's volatility was a constant. Drop that, and prove what the hedger "
            "earns. Sell the option, priced and hedged at a volatility sigma h, which solves the Black-Scholes "
            "equation at that volatility. <bookmark mark='a'/> The stock, meanwhile, moves with whatever "
            "volatility the world delivers, sigma t, changing as it likes; Ito's lemma uses that one. "
            "<bookmark mark='b'/> Substitute the equation, and the hedged position changes by half gamma S "
            "squared times the gap between the two variances: nothing else. <bookmark mark='c'/> Integrate over "
            "the option's life: the seller's profit is half the integral of dollar gamma times the variance gap. "
            "<bookmark mark='d'/> And if the world's volatility never exceeds sigma h, and the payoff is convex, "
            "every term is positive: the seller cannot lose, whatever the model, whatever the path. Nicole El "
            "Karoui, Monique Jeanblanc and Steven Shreve proved it in 1998. It is why a false model can run a desk."
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

    # ------------------------------------------------------------------
    def mountain(self, w, g3):
        tg, Sg, G = np.asarray(g3["t"], float), np.asarray(g3["S"], float), np.asarray(g3["G"], float)
        K, T = g3["K"], g3["T"]
        zmax = 150.0
        ax = ThreeDAxes(x_range=[0, T, T / 4], y_range=[88, 132, 11], z_range=[0, zmax, 50], x_length=7.6,
                        y_length=6.0, z_length=3.4, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False, "stroke_width": 2})
        ax.shift(DOWN * 0.5)
        surf = Surface(lambda u, v: ax.c2p(u, v, min(float(np.interp(v, Sg, [np.interp(u, tg, G[:, j])
                                                                              for j in range(len(Sg))])), zmax)),
                       u_range=[0, tg[-1]], v_range=[Sg[0], Sg[-1]], resolution=(24, 20))
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.Q, 0), (GAM, 60), (WHITE, zmax)], axis=2)
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
                    [ax.c2p(a, b, 0) for a, b in zip(t[:i + 1], np.clip(Pth[name][:i + 1], 88, 132))])
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
        fixed = [hint, base, ctitle, res]
        for m in fixed:
            self.add_fixed_in_frame_mobjects(m)
            self.remove(m)
        with self.voiceover(
            "Here is the weight in that integral, as a landscape: dollar gamma over time and stock price, for a "
            "three-month call sold at twenty-five percent. A ridge runs along the strike and climbs into a spike "
            "at expiry. <bookmark mark='a'/> Now two paths walk across the floor. Both realize almost exactly "
            "twenty percent, so the seller has a five-point edge on both. The blue one stays near the strike, "
            "under the ridge; the green one drifts away early, into the plain. On the right, each path's column "
            "fills with the dollar gamma it has collected. <bookmark mark='b'/> The blue column ends "
            f"{cols['near'][-1] / cols['far'][-1]:.0f} times taller, and so does the profit: "
            f"{w['pnl_near']:.2f} against {w['pnl_far']:.2f}. Same realized volatility; a trader who sells "
            "options is betting on volatility where her gamma is."
        ) as vo:
            self.play(FadeIn(hint), Create(ax), run_time=1.5)
            self.play(FadeIn(surf), run_time=2)
            self.move_camera(theta=-40 * DEGREES, run_time=max(vo.until("a") - 0.5, 1.0))
            self.add(track("near"), track("far"), c_near, c_far)
            self.play(FadeIn(base), FadeIn(ctitle))
            self.play(k.animate.set_value(n), run_time=max(vo.until("b") - 0.5, 4.0), rate_func=linear)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(Group(*self.mobjects))], run_time=1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def choice(self, h):
        s30, s25 = h["stats_30"], h["stats_25"]
        lo, hi = -1.5, 5.5
        panels = VGroup()
        for name, arr, col, st in ((r"hedged at implied, 20\%", h["imp_30"], IMP, (s30["imp_mean"], s30["imp_sd"])),
                                   (r"hedged at actual, 30\%", h["act_30"], REA, (s30["act_mean"], s30["act_sd"]))):
            g = axes([lo, hi], [0, 1.05], x_length=5.2, y_length=2.3, xlabel=r"P\&L at expiry, per 100 of stock",
                     xticks=[0, 2, 4], font_size=18)
            pnl = np.asarray(arr, float)
            hh, e = np.histogram(np.clip(pnl, lo, hi), bins=56, range=(lo, hi))
            hh = hh / hh.max()
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
            "Now the other side of the trade, and a choice. You bought a call at twenty percent and you are "
            "sure the stock will realize thirty. Which volatility do you hedge with? Paul Wilmott and Riaz Ahmad "
            "asked this in 2005. Pause and predict which gives the smoother outcome. <bookmark mark='a'/> Hedge "
            "at the volatility you believe, thirty, and the final profit is nearly the same on every path: the "
            f"price difference, {s30['locked']:.2f}, locked in at the start, with a spread of {s30['act_sd']:.2f} "
            "that is only the noise of hedging in steps. <bookmark mark='b'/> Hedge at the market's twenty, and "
            f"the average is the same, {s30['imp_mean']:.2f}, but it depends on the path, sd {s30['imp_sd']:.2f}: "
            "the integral of dollar gamma again. The price of certainty at expiry is a bumpy ride before it, "
            "since the actual-volatility hedge is marked by a market that still says twenty. "
            f"<bookmark mark='c'/> And if the world realizes only twenty-five, {loss_more} is the one with more "
            "losing paths. Neither choice is free."
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
        left = axes([0.04, 0.44], [-3.5, 5], x_length=5.4, y_length=4.0, xlabel=r"realized volatility",
                    ylabel=r"the seller's P\&L", xticks=[0.1, 0.25, 0.4], yticks=[-2, 0, 2, 4],
                    xfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20)
        right = axes([-3.5, 5], [-3.5, 5], x_length=4.4, y_length=4.0,
                     xlabel=r"$\tfrac12\int \Gamma S^2(\sigma_i^2 - v_t)\,dt$", ylabel=r"the seller's P\&L",
                     xticks=[-2, 0, 2, 4], yticks=[-2, 0, 2, 4], font_size=20)
        VGroup(left, right).arrange(RIGHT, buff=1.1).shift(DOWN * 0.3)
        d1 = VGroup(*[Dot(left.ax.c2p(a, b), radius=0.022, color=REA, fill_opacity=0.6) for a, b in
                      zip(rv[:n], np.clip(pnl[:n], -3.4, 4.9))])
        d2 = VGroup(*[Dot(right.ax.c2p(a, b), radius=0.022, color=GAM, fill_opacity=0.6) for a, b in
                      zip(np.clip(pred[:n], -3.4, 4.9), np.clip(pnl[:n], -3.4, 4.9))])
        diag = DashedLine(right.ax.c2p(-3.4, -3.4), right.ax.c2p(4.9, 4.9), color=GREY_B, stroke_width=1.5)
        be = DashedLine(left.ax.c2p(0.25, -3.5), left.ax.c2p(0.25, 5), color=IMP, stroke_width=1.5)
        c1 = MathTex(rf"\rho = {w['corr_rv']:.2f}", font_size=34, color=REA).next_to(left, UP, buff=0.2)
        c2 = MathTex(rf"\rho = {w['corr_pred']:.2f}", font_size=34, color=GAM).next_to(right, UP, buff=0.2)
        hp = w["heston"]
        params = note(rf"{len(rv):,} Heston paths (volatility of volatility {hp['xi']}, correlation {hp['rho']}); "
                      r"sold and hedged at 25\%".replace(",", "{,}", 1), font_size=20).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In a world where volatility itself moves, the gamma weighting is the main effect. Here are "
            f"{len(rv):,} paths of the Heston model, in which the variance wanders on its own, all sold and hedged "
            "at twenty-five percent. On the left, each path's profit against its realized volatility. The relation "
            f"is there, correlation {w['corr_rv']:.2f}, but loose: paths with the same realized volatility land "
            "a point or more apart. <bookmark mark='a'/> On the right, the same profits against the gamma-weighted "
            "formula, computed from each path's own variance. They fall on the diagonal, correlation "
            f"{w['corr_pred']:.2f}. The formula is the hedger's accounting identity: it explains essentially "
            "every dollar, and it says the realized volatility that matters is the one weighted by gamma. That "
            "observation is the seed of variance swaps, which pay plain realized variance with no gamma weight, "
            "and of Part twelve."
        ) as vo:
            self.play(FadeIn(left), Create(be), FadeIn(params))
            self.play(LaggedStart(*[FadeIn(d) for d in d1], lag_ratio=0.001, run_time=2.5), FadeIn(c1))
            vo.wait_until("a")
            self.play(FadeIn(right), Create(diag))
            self.play(LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.001, run_time=2.5), FadeIn(c2))
        self.wait(0.4)
        self.clear_scene()
