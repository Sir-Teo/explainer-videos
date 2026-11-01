from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import GAIN, GAM, IMP, OPT, PART, REA, SPOT, load


class WrongVol(VoiceoverScene):
    def construct(self):
        w = load("wrong_vol")
        self.card()
        self.formula()
        self.two_paths(w)
        self.heston(w)

    def card(self):
        c = chapter_card(7, r"Hedging with the wrong volatility", r"Does it matter when the moves happen?",
                         lit=(1993,), part=PART)
        with self.voiceover("Chapter seven. Hedging with the wrong volatility."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def formula(self):
        eq = cmath(r"\text{P\&L}", r"=", r"\tfrac12", r"\int_0^T", r"\Gamma_t\,S_t^2", r"\big(", r"\sigma_i^2", r"-",
                   r"\sigma_{r,t}^2", r"\big)\,dt", font_size=50,
                   colors={r"\Gamma_t\,S_t^2": GAM, r"\sigma_i^2": IMP, r"\sigma_{r,t}^2": REA})
        eq.shift(UP * 1.2)
        who = note(r"El Karoui, Jeanblanc and Shreve (1998); the trader's version: Derman, Kani; Carr and Madan",
                   font_size=22).next_to(eq, DOWN, buff=0.4)
        pts = VGroup(
            label(r"the realized variance is weighted by dollar gamma, $\Gamma S^2$", font_size=30, color=GAM),
            label(r"so the same realized volatility can make or lose money", font_size=30, color=GREY_A),
            label(r"and if $\sigma_r \le \sigma_i$ everywhere, the seller cannot lose (the robustness result)",
                  font_size=26, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(who, DOWN, buff=0.6)
        with self.voiceover(
            "Add up the last chapter's formula over the life of the option, and let the realized volatility change "
            "from moment to moment. The seller's profit is one half the integral of gamma S squared times the "
            "difference of the variances. Nicole El Karoui, Monique Jeanblanc and Steven Shreve made this precise "
            "in 1998, and traders had used it long before. <bookmark mark='a'/> Two things follow. The realized "
            "variance does not enter as a plain average: it is weighted by dollar gamma, which is large near the "
            "strike and near expiry, and small elsewhere. So the same realized volatility can make or lose money, "
            "depending on when and where the moves happen. <bookmark mark='b'/> And if the realized volatility "
            "never exceeds the implied, every term is positive: the seller cannot lose, whatever the model, "
            "whatever the path. That is why Black-Scholes is robust enough to run a desk even though its "
            "assumptions are false."
        ) as vo:
            self.play(Write(eq), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]))
            self.play(Indicate(eq[4], color=GAM, scale_factor=1.3))
            self.play(FadeIn(pts[1]))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def two_paths(self, w):
        t = np.asarray(w["t"], float) * 252
        K, T, sig_i = w["K"], w["T"], w["sigma_i"]
        g = axes([0, 63], [92, 132], x_length=7.6, y_length=4.4, xlabel=r"trading days", ylabel=r"the stock",
                 xticks=[0, 21, 42, 63], yticks=[100, 115, 130], font_size=20).to_edge(LEFT, buff=0.6)
        ax = g.ax
        # dollar gamma as a heat strip behind the paths: where gamma is large
        tt = np.linspace(0, 62.5, 60)
        ss = np.linspace(92, 132, 40)
        Gm = np.array([[float(bs.greeks(s, K, max(T - x / 252, 1e-4), sig_i)["gamma"]) * s * s for x in tt]
                       for s in ss])
        vmax = np.percentile(Gm, 99)
        cells = VGroup()
        dx, dy = ax.x_length / len(tt), ax.y_length / len(ss)
        for i, s in enumerate(ss):
            for jx, x in enumerate(tt):
                a = float(np.clip(Gm[i, jx] / vmax, 0, 1))
                if a < 0.03:
                    continue
                cells.add(Rectangle(width=dx * 1.02, height=dy * 1.02, stroke_width=0, fill_color=GAM,
                                    fill_opacity=0.5 * a ** 0.8).move_to(ax.c2p(x, s)))
        kline = DashedLine(ax.c2p(0, K), ax.c2p(63, K), color=QC.STRIKE, stroke_width=1.2)
        near = series_line(ax, t, w["S_near"], SPOT, stroke_width=3)
        far = series_line(ax, t, w["S_far"], REA, stroke_width=3)
        heat_lab = label(r"pink: dollar gamma $\Gamma S^2$", font_size=22, color=GAM).next_to(g, UP, buff=0.1)
        heat_lab.align_to(g, RIGHT)
        tab = VGroup(
            label(r"sold and hedged at $\sigma_i = 25\%$", font_size=26, color=IMP),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=SPOT, stroke_width=5),
                   label(rf"near the strike: realized {100 * w['rv_near']:.1f}\%", font_size=24, color=SPOT))
            .arrange(RIGHT, buff=0.15),
            MathTex(rf"\text{{P\&L}} = {w['pnl_near']:+.2f}", font_size=36, color=GAIN),
            VGroup(Line(ORIGIN, RIGHT * 0.5, color=REA, stroke_width=5),
                   label(rf"away from it: realized {100 * w['rv_far']:.1f}\%", font_size=24, color=REA))
            .arrange(RIGHT, buff=0.15),
            MathTex(rf"\text{{P\&L}} = {w['pnl_far']:+.2f}", font_size=36, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.5)
        why_ = wrapped_label(rf"dollar gamma along the paths: {w['dg_near']:.0f} against {w['dg_far']:.0f}, so "
                             r"the same five-point edge in volatility pays very different amounts", 4.3, 22, GREY_A)
        why_.next_to(tab, DOWN, buff=0.4).align_to(tab, LEFT)
        keep_in_frame(why_, margin=0.25)
        with self.voiceover(
            f"Here is the effect on two paths. Both realize almost exactly twenty percent; the option was sold "
            f"and is hedged at twenty-five, so the seller has a five-point edge on both. Behind them, in pink, "
            "dollar gamma: it is concentrated near the strike and grows as expiry approaches. <bookmark mark='a'/> "
            f"The blue path spends the quarter close to the strike, where gamma is large, and the seller makes "
            f"{w['pnl_near']:.2f}. <bookmark mark='b'/> The green one drifts away early, into a region where the "
            f"option barely needs hedging, and the same edge earns only {w['pnl_far']:.2f}. Same realized "
            f"volatility, {w['pnl_near'] / w['pnl_far']:.0f} times the profit. A trader who sells options is not betting on volatility in "
            "general, but on volatility where her gamma is."
        ) as vo:
            self.play(FadeIn(g), FadeIn(cells), FadeIn(heat_lab), Create(kline), FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(Create(near), run_time=2.5)
            self.play(FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("b")
            self.play(Create(far), run_time=2.5)
            self.play(FadeIn(tab[3]), FadeIn(tab[4]))
            self.play(FadeIn(why_))
        self.wait(0.3)
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
            "In a world where volatility itself moves, this is not a curiosity, it is the main effect. Here are "
            f"{len(rv):,} paths of the Heston model, in which the variance wanders on its own, all sold and hedged "
            "at twenty-five percent. On the left, each path's profit against its realized volatility. The relation "
            f"is there, correlation {w['corr_rv']:.2f}, but loose: a path realizing twenty percent can make "
            "three or lose one. <bookmark mark='a'/> On the right, the same profits against the gamma-weighted "
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
