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
            cmath(r"\text{error}_k", r"=", r"\tfrac12", r"\Gamma", r"S^2", r"\sigma^2", r"\Delta t", r"\,(", r"Z^2 - 1",
                  r")", font_size=40, colors=C_),
            cmath(r"\operatorname{Var}(\text{error}_k)", r"=", r"\tfrac12", r"\Gamma^2", r"S^4", r"\sigma^4",
                  r"\Delta t^2", font_size=40, colors={**C_, r"\Gamma^2": GAM, r"\Delta t^2": SPOT}),
            cmath(r"\operatorname{sd}(\text{P\&L})", r"=", r"\sigma^2", r"\sqrt{\tfrac12\,\Delta t\int_0^T "
                  r"\mathbb E\big[\Gamma_t^2 S_t^4\big]\,dt}", r"\;\propto\;", r"\tfrac{1}{\sqrt N}", font_size=40,
                  colors=C_),
        ]
        whys = [why(r"one step: the squared move $\sigma^2 S^2 Z^2\Delta t$ against its average"),
                why(r"$\operatorname{Var}(Z^2) = 2$"),
                why(r"steps are independent: add the variances")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-1.2, buff=0.75, edge=6.9)
        hist = note(r"Boyle and Emanuel (1980); Derman and Kamal (Goldman Sachs, 1998): $\operatorname{sd} \approx "
                    r"\sqrt{\pi/4}\;\text{vega}\;\sigma/\sqrt N$ at the money, $\sqrt{\pi/4} = 0.886$",
                    font_size=24).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Real hedgers trade in steps. Over one step the hedge leaves half gamma S squared times the squared "
            "move minus its average: sigma squared S squared delta t times Z squared minus one. "
            "<bookmark mark='a'/> Z squared has variance two, so each step's error has variance half gamma squared "
            "S to the fourth sigma to the fourth delta t squared. <bookmark mark='b'/> The steps are independent, "
            "T over delta t of them, so one power of delta t is left: the error shrinks like the square root of the "
            "step. Phelim Boyle and David Emanuel, 1980; Emanuel Derman and Michael Kamal at Goldman Sachs gave "
            "the rule of thumb at the bottom, with its root pi over four."
        ) as vo:
            step(0)
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
        lo, hi = -3.0, 1.6
        panels = VGroup()
        for N, col in ((13, LOSS), (252, OPT)):
            pnl = np.asarray(ds[f"pnl_{N}"], float)
            g = axes([lo, hi], [0, 1.05], x_length=5.0, y_length=2.6, xlabel=r"hedged P\&L, short the call",
                     xticks=[-2, -1, 0, 1], font_size=18)
            hh, e = np.histogram(np.clip(pnl, lo, hi), bins=60, range=(lo, hi))
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
        leg = legend([(SPOT, r"no jumps: GBM, same total volatility"), (LOSS, r"Merton jumps: 2 a year, mean $-5\%$"),
                      (LOSS, rf"dashed: the jump term alone, {jf['floor']:.2f}")], font_size=22)
        leg.next_to(g, RIGHT, buff=0.3).align_to(g, UP)
        C = {r"\Gamma": GAM, r"J": LOSS}
        eq = cmath(r"V(Se^J) - V(S) - \Delta S(e^J - 1)", r"\approx", r"\tfrac12", r"\Gamma", r"S^2", r"J", r"^2",
                   font_size=32, colors=C).next_to(leg, DOWN, buff=0.5).align_to(leg, LEFT)
        eqn = label(r"a jump is not made smaller by hedging more often", font_size=22, color=GREY_A)
        eqn.next_to(eq, DOWN, buff=0.15).align_to(eq, LEFT)
        holds = jf["ratio_jump"] < 2
        floor_phrase = "It hits a floor," if holds else "It falls, but slowly, towards a floor,"
        with self.voiceover(
            "And here is where the law stops. Emanuel Derman and Nassim Taleb's point, in 2005: dynamic "
            "replication assumes the price moves continuously. Give the stock jumps, twice a year on average, "
            "about five percent down, and hedge at the right total volatility. In blue, the same stock without "
            "jumps: its error keeps halving every time the hedging quadruples. <bookmark mark='a'/> In red, with "
            f"jumps: from sixteen hedges to a thousand and twenty-four, the error falls only from "
            f"{J.mean(0)[0]:.2f} to {J.mean(0)[-1]:.2f}. "
            + f"{floor_phrase} and the floor is the jump term: a jump of size J costs half gamma S squared J squared however "
            f"often you rebalance, which by itself leaves {jf['floor']:.2f}. Hedging frequency buys you nothing "
            "against a gap. Part eleven measures it on Bitcoin's real jumps; Part thirteen prices them."
        ) as vo:
            self.play(FadeIn(g), FadeIn(bg), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(FadeIn(bj), FadeIn(leg[1]))
            self.play(Create(floor), FadeIn(leg[2]), Write(eq), FadeIn(eqn))
        self.wait(0.4)
        self.clear_scene()
