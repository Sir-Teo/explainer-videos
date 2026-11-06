from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import GAIN, GAM, IMP, LOSS, OPT, PART, SPOT, computed, load

C_ = {r"\Gamma": GAM, r"\sigma^2": IMP, r"\sigma^4": IMP, r"Z^2 - 1": SPOT, r"\Delta t": SPOT}


class Discrete(VoiceoverScene):
    def construct(self):
        d = load("discrete")
        self.card()
        self.derive()
        self.measure(d, load("discrete_seeds"))
        self.shape(load("discrete_seeds"))
        self.jumps(load("jump_floor"))

    def card(self):
        c = chapter_card(9, r"Hedging in steps", r"How often should you hedge?", lit=(1980,), part=PART)
        with self.voiceover("Chapter nine. Hedging in steps."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\text{error}_k", r"\approx", r"\tfrac12", r"\Gamma", r"S^2", r"\sigma^2", r"\Delta t", r"\,(", r"Z^2 - 1",
                  r")", font_size=40, colors=C_),
            cmath(r"\operatorname{Var}(\text{error}_k\mid\mathcal F_{t_k})", r"\approx", r"\tfrac12", r"\Gamma^2", r"S^4", r"\sigma^4",
                  r"\Delta t^2", font_size=40, colors={**C_, r"\Gamma^2": GAM, r"\Delta t^2": SPOT}),
            cmath(r"\operatorname{sd}(\text{P\&L})", r"\sim", r"\sigma^2", r"\sqrt{\tfrac12\,\Delta t\int_0^T "
                  r"\mathbb E\big[\Gamma_t^2 S_t^4\big]\,dt}", r"\;\propto\;", r"\tfrac{1}{\sqrt N}", font_size=40,
                  colors=C_),
        ]
        whys = [why(r"one step: the squared move $\sigma^2 S^2 Z^2\Delta t$ against its average"),
                why(r"$\operatorname{Var}(Z^2) = 2$"),
                why(r"leading martingale differences: variances add; weights are path dependent")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.2, buff=0.75, edge=6.9)
        hist = note(r"Boyle and Emanuel (1980); Derman and Kamal (Goldman Sachs, 1998): $\operatorname{sd} \approx "
                    r"\sqrt{\pi/4}\;\text{vega}\;\sigma/\sqrt N$ at the money, $\sqrt{\pi/4} = 0.886$",
                    font_size=24).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            """At zero rates under driftless GBM, freeze gamma and spot over one short step. Its leading error is half gamma S squared sigma squared delta t, times Z squared minus one. <bookmark mark='a'/> Conditional on the starting information, the variance is half gamma squared S to the fourth sigma to the fourth delta t squared. <bookmark mark='b'/> The leading centered increments are martingale differences. Their variances add even though their gamma weights depend on previous moves. With the usual moment and convergence conditions, total standard deviation is asymptotically proportional to the square root of the step. Boyle and Emanuel, 1980; the ATM approximation below is Derman and Kamal's rule of thumb."""
        ) as vo:
            step(0, run_time=0.15)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            self.play(FadeIn(hist))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measure(self, d, ds):
        N = np.asarray(d["N"], float)
        th, km = (np.asarray(d[k], float) for k in ("theory", "kamal"))
        sd5 = np.asarray(ds["sd"], float)
        g = axes([0.5, 3.1], [-1.1, 0.4], x_length=7.6, y_length=4.4, xlabel=r"hedges over three months",
                 ylabel=r"standard deviation of the hedged P\&L", xticks=[1, 2, 3], yticks=[-1, 0],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", font_size=20)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        lx = np.log10(N)
        th_line = curve(ax, lx, np.log10(th), GAM, stroke_width=3)
        km_line = DashedVMobject(curve(ax, lx, np.log10(km), GREY_B, stroke_width=2), num_dashes=40)
        k = ValueTracker(lx[0])

        def grown():
            j = max(int(np.searchsorted(lx, k.get_value() + 1e-9, side="right")), 2)
            return seed_band(ax, lx[:j], np.log10(sd5[:, :j]), OPT, stroke_width=3, opacity=0.35)

        band_ = always_redraw(grown)
        leg = legend([(OPT, r"simulated: 5 seeds of 10,000 paths"), (GAM, r"derived: $\propto \sqrt{\Delta t}$"),
                      (GREY_B, r"rule of thumb")], font_size=22).move_to(ax.c2p(2.3, 0.2))
        marks = VGroup()
        for n, name in ((13, r"weekly"), (63, r"daily"), (252, r"four a day")):
            x = np.log10(n)
            marks.add(VGroup(DashedLine(ax.c2p(x, -1.1), ax.c2p(x, -0.95), color=GREY_C, stroke_width=1),
                             label(name, font_size=18, color=GREY_B).next_to(ax.c2p(x, -0.95), UP, buff=0.05)))
        sl = np.asarray(ds["slopes"], float)
        right = VGroup(
            label(r"fitted slope, 5 seeds", font_size=26, color=GREY_A),
            MathTex(rf"{sl.min():.3f}\ \text{{to}}\ {sl.max():.3f}", font_size=40, color=OPT),
            label(r"the theory says $-0.5$", font_size=24, color=GREY_B),
            label(rf"premium: {d['premium_bs']:.2f}", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.6)
        with self.voiceover(
            "Here it is measured. A three-month at-the-money call, sold at the true volatility of twenty percent, "
            "hedged four times, eight, sixteen, up to a thousand and twenty-four times over the quarter. Five "
            "independent seeds of ten thousand paths each, drawn as a band as the frequency rises. The pink line "
            "is the formula we just derived, the dashed grey line the rule of thumb. <bookmark mark='a'/> The band "
            f"is so thin it looks like a line: the five seeds never differ by more than "
            f"{100 * ds['spread_max']:.1f} percent, and their slopes on these log scales lie between "
            f"{sl.min():.3f} and {sl.max():.3f}: the square-root law. Hedging weekly leaves an error of about "
            f"{d['sd'][2]:.2f} on a premium of {d['premium_bs']:.2f}; four times a day, about {d['sd'][6]:.2f}."
        ) as vo:
            self.play(FadeIn(g), Create(th_line), Create(km_line), FadeIn(leg), FadeIn(marks))
            self.add(band_)
            self.play(k.animate.set_value(lx[-1]), run_time=max(vo.until("a") - 1.0, 3.0), rate_func=linear)
            band_.clear_updaters()
            self.play(FadeIn(right, shift=LEFT * 0.2), FadeIn(computed()))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shape(self, ds):
        lo, hi = -3.5, 2.6  # 99.5% of the 13-hedge outcomes; the rest are left out, not piled into the end bins
        panels = VGroup()
        for N, col in ((13, LOSS), (252, OPT)):
            pnl = np.asarray(ds[f"pnl_{N}"], float)
            g = axes([lo, hi], [0, 1.05], x_length=5.0, y_length=2.6, xlabel=r"hedged P\&L, short the call",
                     xticks=[-3, -2, -1, 0, 1, 2], font_size=18)
            hh, e = np.histogram(pnl, bins=60, range=(lo, hi))
            hh = hh / hh.max()
            bars = VGroup(*[Rectangle(width=g.ax.x_length / 60 * 0.95, height=max(g.ax.y_length * v, 0.002),
                                      stroke_width=0, fill_color=col, fill_opacity=0.85)
                            .move_to(g.ax.c2p((e[i] + e[i + 1]) / 2, 0), aligned_edge=DOWN) for i, v in enumerate(hh)])
            head = label(rf"{N} hedges", font_size=26, color=col).next_to(g, UP, buff=0.12)
            stat = MathTex(rf"\text{{sd}}\ {ds[f'sd_{N}']:.2f},\ \text{{skewness}}\ {ds[f'skew_{N}']:+.2f}", font_size=26,
                           color=col).next_to(g, DOWN, buff=0.12)
            panels.add(VGroup(g, bars, head, stat))
        panels.arrange(RIGHT, buff=0.8).shift(UP * 0.2)
        neg = ds["skew_13"] < 0
        skew_line = (f"Hedged weekly, the seller's distribution leans left, skewness {ds['skew_13']:.2f}; hedged four "
                     f"times a day, {ds['skew_252']:.2f}: more steps, each smaller, and the sum looks more normal."
                     if neg else
                     f"Here the skewness is {ds['skew_13']:+.2f} weekly and {ds['skew_252']:+.2f} four times a day.")
        with self.voiceover(
            "The spread is not the whole story; look at its shape. Each step's error is Z squared minus one, "
            "which is lopsided: small gains most of the time, an occasional large loss when the stock jumps "
            f"across a step. <bookmark mark='a'/> {skew_line}"
        ) as vo:
            self.play(FadeIn(panels[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(panels[1], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def jumps(self, jf):
        N = np.asarray(jf["N"], float)
        J, G = np.asarray(jf["jump"], float), np.asarray(jf["gbm"], float)
        lx = np.log10(N)
        g = axes([1.1, 3.1], [-1.2, 0.5], x_length=7.4, y_length=4.2, xlabel=r"hedges over three months",
                 ylabel=r"sd of the hedged P\&L", xticks=[2, 3], yticks=[-1, 0],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", font_size=20)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        bj = seed_band(ax, lx, np.log10(J), LOSS, stroke_width=3.5, opacity=0.3)
        bg = seed_band(ax, lx, np.log10(G), SPOT, stroke_width=3.5, opacity=0.3)
        floor = DashedLine(ax.c2p(1.1, np.log10(jf["floor"])), ax.c2p(3.1, np.log10(jf["floor"])), color=LOSS,
                           stroke_width=1.5)
        leg = legend([(SPOT, r"GBM: matched log-return variance rate"), (LOSS, r"Merton jumps: 2 a year, mean log jump $-5\%$"),
                      (LOSS, rf"dashed: lognormal-proxy jump reference, {jf['floor']:.2f}")], font_size=22)
        if leg.width > 5.0:
            leg.scale_to_fit_width(5.0)
        leg.next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        C = {r"\Gamma": GAM, r"J": LOSS}
        eq = VGroup(
            cmath(r"R_J", r"=", r"V(Se^J)-V(S)-\Delta S(e^J-1)", font_size=25, colors=C),
            cmath(r"R_J", r"\approx", r"\tfrac12\Gamma S^2J^2", font_size=32, colors=C),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        if eq.width > 5.0:
            eq.scale_to_fit_width(5.0)
        eq.next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        eqn = wrapped_label(r"a jump is not made smaller by hedging more often", 5.0, 22, GREY_A)
        eqn.next_to(eq, DOWN, buff=0.15).align_to(eq, LEFT)
        holds = jf["ratio_jump"] < 2
        floor_phrase = "The measured curve flattens," if holds else "The measured curve keeps falling slowly,"
        with self.voiceover(
            f"""Add Poisson log-price jumps, twice a year with a minus five percent mean log jump. Compare with GBM at the same log-return variance rate. A single Black volatility does not complete this jump market. Without jumps, frequent hedging reduces the error. <bookmark mark='a'/> With jumps, its measured standard deviation falls from {J.mean(0)[0]:.2f} to {J.mean(0)[-1]:.2f}. {floor_phrase} A jump leaves the exact nonlinear remainder shown on screen; half gamma S squared J squared is only its small-log-jump approximation. The dashed {jf['floor']:.2f} is a quadrature reference for jump-remainder risk using a lognormal spot proxy. It is not a proved variance floor for these simulated Merton paths. Increasing frequency cannot eliminate unspanned jump risk."""
        ) as vo:
            self.play(FadeIn(g), FadeIn(bg), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(FadeIn(bj), FadeIn(leg[1]))
            self.play(Create(floor), FadeIn(leg[2]), Write(eq), FadeIn(eqn))
        self.wait(0.4)
        self.clear_scene()
