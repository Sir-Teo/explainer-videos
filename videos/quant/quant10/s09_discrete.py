from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant10.common import GAIN, GAM, IMP, LOSS, OPT, PART, SPOT, load

C_ = {r"\Gamma": GAM, r"\sigma^2": IMP, r"\sigma^4": IMP, r"Z^2 - 1": SPOT, r"\Delta t": SPOT}


class Discrete(VoiceoverScene):
    def construct(self):
        d = load("discrete")
        self.card()
        self.derive()
        self.measure(d)
        self.costs(d)

    def card(self):
        c = chapter_card(8, r"Hedging in steps, and paying for it", r"How often should you hedge?",
                         lit=(1985,), part=PART)
        with self.voiceover("Chapter eight. Hedging in steps, and paying for it."):
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
        hist = note(r"Boyle and Emanuel (1980); Kamal and Derman (1999): $\operatorname{sd} \approx "
                    r"\sqrt{\pi/4}\;\text{vega}\;\sigma/\sqrt N$ at the money", font_size=24).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Black-Scholes assumes the hedge is adjusted continuously. Real hedgers trade in steps: every hour, "
            "every day. Over one step the hedge leaves an error: half gamma S squared times the squared move, "
            "minus its average. The squared move is sigma squared S squared Z squared delta t, with Z a standard "
            "normal, so the error is proportional to Z squared minus one. <bookmark mark='a'/> Z squared has "
            "variance two, so each step's error has variance one half gamma squared S to the fourth sigma to the "
            "fourth delta t squared. <bookmark mark='b'/> The steps are independent, so the variances add: there "
            "are T over delta t of them, which leaves one power of delta t. The standard deviation of the hedging "
            "error shrinks like the square root of the step: halve the error, hedge four times as often. Phelim "
            "Boyle and David Emanuel worked this out in 1980; Emanuel Derman's team at Goldman Sachs later gave "
            "the at-the-money rule of thumb at the bottom."
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
    def measure(self, d):
        N = np.asarray(d["N"], float)
        sd, th, km = (np.asarray(d[k], float) for k in ("sd", "theory", "kamal"))
        g = axes([0.5, 3.1], [-1.1, 0.4], x_length=7.6, y_length=4.4, xlabel=r"hedges over three months",
                 ylabel=r"standard deviation of the hedged P\&L", xticks=[1, 2, 3], yticks=[-1, 0],
                 xfmt=lambda v: f"10^{{{int(v)}}}", yfmt=lambda v: f"10^{{{int(v)}}}", font_size=20)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        lx = np.log10(N)
        dots = VGroup(*[glow_dot(ax.c2p(a, b), color=OPT, radius=0.06) for a, b in zip(lx, np.log10(sd))])
        th_line = curve(ax, lx, np.log10(th), GAM, stroke_width=3)
        km_line = DashedVMobject(curve(ax, lx, np.log10(km), GREY_B, stroke_width=2), num_dashes=40)
        leg = legend([(OPT, r"simulated, 20,000 paths each"), (GAM, r"derived: $\propto \sqrt{\Delta t}$"),
                      (GREY_B, r"rule of thumb")], font_size=22).move_to(ax.c2p(2.35, 0.2))
        marks = VGroup()
        for n, name in ((13, r"weekly"), (63, r"daily"), (252, r"four a day")):
            x = np.log10(n)
            marks.add(VGroup(DashedLine(ax.c2p(x, -1.1), ax.c2p(x, -0.95), color=GREY_C, stroke_width=1),
                             label(name, font_size=18, color=GREY_B).next_to(ax.c2p(x, -0.95), UP, buff=0.05)))
        right = VGroup(
            label(r"fitted slope", font_size=26, color=GREY_A),
            MathTex(rf"{d['slope']:.2f}", font_size=44, color=OPT),
            label(r"the theory says $-0.5$", font_size=24, color=GREY_B),
            label(rf"premium: {d['premium_bs']:.2f}", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.8)
        with self.voiceover(
            "Here it is measured. A three-month at-the-money call, sold at the true volatility of twenty percent, "
            "hedged four times, eight, sixteen, up to a thousand and twenty-four times over the quarter, twenty "
            "thousand paths at each frequency. The pink line is the formula we just derived, with its integral "
            "computed exactly; the dashed grey line is the rule of thumb. <bookmark mark='a'/> The simulation sits "
            f"on the formula, and its slope on these log scales is {d['slope']:.2f}: the square-root law. Hedging "
            f"weekly leaves an error of about {d['sd'][2]:.2f} on a premium of {d['premium_bs']:.2f}; hedging four "
            f"times a day, about {d['sd'][6]:.2f}. Even a hedger with a perfect model is running a risk, unless "
            "she trades without limit."
        ) as vo:
            self.play(FadeIn(g), Create(th_line), Create(km_line), FadeIn(leg), FadeIn(marks))
            self.play(LaggedStart(*[FadeIn(x, scale=1.4) for x in dots], lag_ratio=0.15, run_time=2.5))
            vo.wait_until("a")
            self.play(FadeIn(right, shift=LEFT * 0.2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def costs(self, d):
        k = d["cost"]
        eq = cmath(r"\sigma_L^2", r"=", r"\sigma^2", r"\Big(1 + \sqrt{\tfrac{2}{\pi}}\,\frac{2k}{\sigma\sqrt{\Delta t}}\Big)",
                   font_size=42, colors={r"\sigma_L^2": IMP, r"\sigma^2": IMP}).to_edge(UP, buff=0.5)
        who = note(r"Leland (1985): sell, and hedge, at the volatility $\sigma_L$", font_size=24).next_to(eq, DOWN,
                                                                                                         buff=0.2)
        lo, hi = -4.5, 3.0
        panels = VGroup()
        for name, arr, mean, col in ((r"priced at $\sigma = 20\%$", d["pnl_naive"], d["naive_mean"], LOSS),
                                     (rf"priced at $\sigma_L = {100 * d['sigma_leland']:.1f}\%$", d["pnl_leland"],
                                      d["leland_mean"], GAIN)):
            g = axes([lo, hi], [0, 1.05], x_length=4.6, y_length=2.4, xlabel=r"P\&L at expiry, after costs",
                     xticks=[-4, -2, 0, 2], font_size=18)
            pnl = np.asarray(arr, float)
            h, e = np.histogram(np.clip(pnl, lo, hi), bins=60, range=(lo, hi))
            h = h / h.max()
            bars = VGroup(*[Rectangle(width=g.ax.x_length / 60 * 0.95, height=max(g.ax.y_length * v, 0.002),
                                      stroke_width=0, fill_color=col, fill_opacity=0.85)
                            .move_to(g.ax.c2p((e[i] + e[i + 1]) / 2, 0), aligned_edge=DOWN) for i, v in enumerate(h)])
            zero = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(0, 1.05), color=GREY_C, stroke_width=1.2)
            head = label(name, font_size=26, color=IMP).next_to(g, UP, buff=0.15)
            stat = MathTex(rf"\text{{mean}}\ {mean:+.2f}", font_size=30, color=col).next_to(g, DOWN, buff=0.15)
            panels.add(VGroup(g, bars, zero, head, stat))
        panels.arrange(RIGHT, buff=1.0).next_to(who, DOWN, buff=0.45)
        # the trade-off, schematically: hedging error falls like 1/sqrt(N), costs rise like sqrt(N)
        tg = axes([1, 60], [0, 4.2], x_length=6.4, y_length=3.0, xlabel=r"hedges per period $N$",
                  ylabel=r"risk and cost", font_size=20).next_to(who, DOWN, buff=0.6)
        xs = np.linspace(1, 60, 200)
        e_, c_ = 3.6 / np.sqrt(xs), 0.42 * np.sqrt(xs)
        err_l = curve(tg.ax, xs, e_, SPOT, stroke_width=3.5)
        cost_l = curve(tg.ax, xs, c_, LOSS, stroke_width=3.5)
        tot_l = curve(tg.ax, xs, e_ + c_, WHITE, stroke_width=4)
        best = xs[np.argmin(e_ + c_)]
        best_d = glow_dot(tg.ax.c2p(best, float(np.min(e_ + c_))), color=WHITE, radius=0.07)
        tlegend = legend([(SPOT, r"hedging error $\propto 1/\sqrt N$"), (LOSS, r"costs $\propto \sqrt N$"),
                          (WHITE, r"both")], font_size=22).next_to(tg, RIGHT, buff=0.4)
        sch = note(r"schematic", font_size=18).next_to(tg, DOWN, buff=0.1).align_to(tg, RIGHT)
        trade = VGroup(tg, err_l, cost_l, tot_l, best_d, tlegend, sch)
        foot = wrapped_label(
            rf"cost {100 * k:.2f}\% of each share traded, hedged weekly. Of the costs, {d['end_costs']:.2f} is "
            rf"the first hedge and the unwind, which Leland's formula leaves out; without them his book averages "
            rf"{d['leland_mid_mean']:+.2f}.", 12.5, 22, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And trading is not free. Every rebalance pays a cost, here a quarter of a percent of the value of the "
            "shares traded, and the costs grow with the number of trades, like the square root of the frequency, "
            "while the hedging error shrinks like its inverse. So there is a best frequency, and a price for the "
            "option that covers it. Hayne Leland's answer in 1985: hedge, and sell, at a higher volatility, "
            "inflated by the costs. <bookmark mark='a'/> Weekly hedging of our call: priced at twenty percent, "
            f"the seller loses {-d['naive_mean']:.2f} on average, all of it costs. Priced and hedged at Leland's "
            f"{100 * d['sigma_leland']:.1f} percent, the loss shrinks to {-d['leland_mean']:.2f}. <bookmark mark='b'/> "
            f"And what is left is exactly what the formula leaves out: {d['end_costs']:.2f} for buying the first "
            "hedge and unwinding the last. Charge for those too, and the book breaks even. Leland's rule is a "
            "first answer; the deep hedger of Part seventeen will learn the better one, a band in which it does "
            "not trade at all."
        ) as vo:
            self.play(FadeIn(tg), FadeIn(sch))
            self.play(Create(err_l), FadeIn(tlegend[0]))
            self.play(Create(cost_l), FadeIn(tlegend[1]))
            self.play(Create(tot_l), FadeIn(tlegend[2]), FadeIn(best_d, scale=1.5))
            self.play(Write(eq), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeOut(trade), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in panels], lag_ratio=0.5, run_time=2.5))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
