from __future__ import annotations

from videos.quant.quant20.common import lesson_cards

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, PART, RISKY, SAFE, ask, fit_right, illustration, load


class Vasicek(VoiceoverScene):
    def construct(self):
        v = load("vasicek")
        self.card()
        self.derive()
        self.pdfs(v)
        self.finite(load("finite"))
        self.basel(v)
        self.feedback()

    def card(self):
        c = chapter_card(10, r"The large pool and bank capital", r"How much capital does a loan book need?", part=PART)
        with self.voiceover("Chapter ten. From one borrower to thousands: the large pool, and the formula behind bank "
                            "capital."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def derive(self):
        rows = [cmath(r"X_i", r"=", r"\sqrt\rho\,M + \sqrt{1 - \rho}\,Z_i,\quad \text{default if } X_i < N^{-1}(p)",
                      font_size=36, colors={r"X_i": RISKY}),
                cmath(r"p(M)", r"=", r"N\Big(\frac{N^{-1}(p) - \sqrt\rho\,M}{\sqrt{1 - \rho}}\Big)", font_size=40,
                      colors={r"p(M)": BAD}),
                cmath(r"\mathbb{P}(L \le x)", r"=", r"N\Big(\frac{\sqrt{1 - \rho}\,N^{-1}(x) - N^{-1}(p)}{\sqrt\rho}\Big)",
                      font_size=38, colors={r"\mathbb{P}(L \le x)": BAD})]
        whys = [why(r"each borrower's fate depends on one common factor $M$, the economy, and its own $Z_i$; $\rho$ is "
                    r"how much they share. A one-factor version of Merton (Vasicek, 1987 and 2002)"),
                why('conditional independence and vanishing exposures give a large-pool limit: the default fraction converges to $p(M)$. Finite pools retain idiosyncratic noise'),
                why(r"so the pool's loss distribution is that of a function of one normal variable, in closed form")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.7, edge=6.9)
        with self.voiceover(
            "Assume homogeneous obligors with the same marginal default probability, a single Gaussian factor, independent idiosyncratic normals conditional on that factor, and equal vanishingly small exposures. <bookmark mark='a'/> Conditional on the common factor, the law of large numbers makes the default fraction converge to its conditional probability. That is a limit result, not exact equality for a finite book. <bookmark mark='b'/> The remaining uncertainty is the common factor. Transforming its normal distribution gives Vasicek's closed-form distribution of the default fraction. The displayed loss variable assumes full loss given default; fixed fractional loss would rescale it. Sector concentrations, heterogeneous exposures, changing recoveries and other factors require extensions."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.wait(0.4)
        self.clear_scene()

    def pdfs(self, v):
        x = np.asarray(v["x"]) * 100
        cols = {"0.0001": SAFE, "0.05": QC.SPOT, "0.15": QC.IMPLIED, "0.3": BAD}
        g = axes([0, 20], [0, 25], x_length=7.6, y_length=4.4, xlabel=r"fraction of the pool defaulting in a year, \%",
                 ylabel=r"density", xticks=[0, 2, 5, 10, 15, 20], yticks=[], font_size=14).to_edge(LEFT, buff=0.6).shift(
            DOWN * 0.3)
        ax = g.ax
        lines = VGroup()
        for k, c_ in cols.items():
            y = np.clip(np.asarray(v["pdf"][k]) / 100, 0, 25)
            lines.add(curve(ax, x, y, c_, stroke_width=3))
        mean = DashedLine(ax.c2p(2, 0), ax.c2p(2, 25), color=WHITE, stroke_width=1.5)
        q = v["q999"]
        side = VGroup(
            legend([(SAFE, r"$\rho \approx 0$"), (QC.SPOT, r"$\rho = 0.05$"), (QC.IMPLIED, r"$\rho = 0.15$"),
                    (BAD, r"$\rho = 0.30$")], font_size=17),
            label(r"all with an average default rate of 2\%", font_size=18, color=GREY_A),
            MathTex(rf"\text{{99.9th percentile: }} {100 * q['0.05']:.1f}\%,\ {100 * q['0.15']:.1f}\%,\ "
                    rf"{100 * q['0.3']:.1f}\%", font_size=24, color=BAD),
            wrapped_label('fixed marginal PD keeps the model mean unchanged while dependence changes the tail. Density shown over 0--20\\%; quantiles use the full model. Neither is a calendar forecast or complete capital requirement', 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            f"This model holds each name's marginal default probability at two percent. <bookmark mark='a'/> With vanishing common-factor loading and an infinite homogeneous pool, the default fraction approaches that mean. <bookmark mark='b'/> Higher dependence changes the distribution, including its tail, while leaving the mean fixed. The density view stops at twenty percent; the displayed quantiles use the full model. <bookmark mark='c'/> At correlation point one five the model ninety-nine point nine percent default-fraction quantile is {100 * q['0.15']:.1f} percent; at point three it is {100 * q['0.3']:.1f} percent. A quantile under fixed parameters is not a forecast of one particular year in a thousand, or a complete capital requirement."
        ) as vo:
            self.play(FadeIn(g), Create(mean), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l_) for l_ in lines[1:]], lag_ratio=0.4, run_time=3))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def finite(self, f):
        names = ["50", "200", "1000"]
        vals = [f["q999"][n] * 100 for n in names] + [f["lhp"] * 100]
        labs = [r"50 loans", r"200 loans", r"1{,}000 loans", r"the large pool"]
        g = axes([0.4, 4.6], [0, 25], x_length=6.4, y_length=4.2, xlabel=r"", ylabel=r"99.9th percentile default rate, \%",
                 xticks=[], yticks=[0, 5, 10, 15, 20, 25], font_size=14).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, (v_, l_) in enumerate(zip(vals, labs)):
            b_ = Rectangle(width=0.7, height=max(ax.c2p(0, v_)[1] - ax.c2p(0, 0)[1], 0.01), stroke_width=0,
                           fill_color=BAD if i < 3 else QC.IMPLIED, fill_opacity=0.8).move_to(
                [ax.c2p(i + 1, 0)[0], (ax.c2p(0, v_)[1] + ax.c2p(0, 0)[1]) / 2, 0])
            bars.add(VGroup(b_, MathTex(rf"{v_:.1f}\%", font_size=24).next_to(b_, UP, buff=0.1),
                            label(l_, font_size=17).next_to(ax.c2p(i + 1, 0), DOWN, buff=0.2)))
        side = wrapped_label('PD 2\\%, $\\rho=0.15$; 100{,}000 simulated years per pool. Finite-pool quantiles have a loss lattice and sampling uncertainty. The stylized IRB formula omits name concentration, which needs separate assessment', 3.8, 18,
                             GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            f"The large-pool expression ignores finite-name idiosyncratic risk. The displayed fixed-seed simulation compares pools of fifty, two hundred and one thousand loans. <bookmark mark='a'/> Their estimated ninety-nine point nine percent default fractions are {vals[0]:.0f}, {vals[1]:.1f} and {vals[2]:.1f} percent, against the large-pool value {vals[3]:.1f}. These are discrete loss quantiles from a finite simulation; tail sampling uncertainty matters. A larger number of names does not eliminate common-factor risk. Granularity approximations can estimate finite-name corrections under regularity and small-exposure conditions, but a concentrated book may require a more direct calculation."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def basel(self, v):
        pds, K = np.asarray(v["pds"]) * 100, np.asarray(v["K"]) * 100
        rows = [cmath(r"K", r"=", r"\Big[\text{LGD}\cdot N\Big(\frac{N^{-1}(\text{PD}) + \sqrt\rho\,N^{-1}(0.999)}{\sqrt{1 - \rho}}"
                      r"\Big) - \text{PD}\cdot\text{LGD}\Big]\times\frac{1 + (M - 2.5)\,b}{1 - 1.5\,b}", font_size=28,
                      colors={r"K": BAD})]
        hdr = rows[0].to_edge(UP, buff=0.5)
        g = axes([np.log10(0.03), np.log10(20)], [0, 25], x_length=7.0, y_length=3.8, xlabel=r"PD, \% (log scale)",
                 ylabel=r"capital, \% of exposure", xticks=[], yticks=[0, 5, 10, 15, 20, 25], font_size=14
                 ).to_edge(LEFT, buff=0.6).shift(DOWN * 0.8)
        ax = g.ax
        tx = VGroup(*[MathTex(f"{x_:g}", font_size=20).next_to(ax.c2p(np.log10(x_), 0), DOWN, buff=0.12)
                      for x_ in (0.03, 0.1, 1, 10)])
        line = curve(ax, np.log10(pds), K, BAD, stroke_width=3.5)
        dot = Dot(ax.c2p(0, 12.5 * 0 + 100 * v["rw_1pct"] / 12.5), color=WHITE)
        side = VGroup(
            MathTex(rf"\text{{PD}} = 1\%:\ \ K = {100 * v['rw_1pct'] / 12.5:.2f}\%,\ \text{{risk weight}}\ "
                    rf"{100 * v['rw_1pct']:.2f}\%", font_size=24),
            wrapped_label('stylized corporate IRB: a 99.9\\% loss construction less expected loss, with maturity adjustment. The prescribed PD--correlation relation is a rule, not an estimated causal law; provisions and current regime details are separate', 3.8, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.6)
        fit_right(side)
        with self.voiceover(
            f"This is the stylized Basel corporate internal-ratings formula, not a complete statement of current capital requirements. It uses a ninety-nine point nine percent one-year loss construction, subtracts expected loss and applies a maturity adjustment, with prescribed correlations and other assumptions. Actual requirements also involve exposure classes, floors, supervisory rules and the treatment of provisions. <bookmark mark='a'/> Its risk weights depend on the prescribed relation between PD and asset correlation. <bookmark mark='b'/> At one percent PD, forty-five percent loss given default and the displayed maturity, this implementation gives a risk weight of {100 * v['rw_1pct']:.2f} percent. The associated capital is {100 * v['rw_1pct'] / 12.5:.1f} cents per dollar of exposure. For a billion dollars that is about {1000 * v['rw_1pct'] / 12.5:.0f} million dollars. Expected loss is another four point five million, but its regulatory coverage and shortfall treatment cannot be reduced to an automatic identical provision in every bank."
        ) as vo:
            self.play(FadeIn(hdr), FadeIn(g), FadeIn(tx))
            vo.wait_until("a")
            self.play(Create(line), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(dot, scale=1.5), FadeIn(side))
        q = ask(r"Basel's formula assumes one common factor. A bank lends to every hotel in one city. What does the "
                r"formula miss?")
        with self.voiceover("Basel's formula assumes a single common factor. A bank lends to every hotel in one city. "
                            "What does the formula miss?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def feedback(self):
        title = wrapped_label('Answer: one city adds concentration beyond a generic factor', 12.4, 32, QC.IDEA).to_edge(UP, buff=.6)
        answer = wrapped_label('Hotels in one city share sector, location and local-demand shocks. A generic corporate correlation can miss these exposures and finite-name concentration.', 11.8, 27, GREY_A).move_to(ORIGIN)
        with self.voiceover('A portfolio of hotels in one city shares sector, location and local-demand risks. A generic prescribed corporate factor may miss those concentrations even when the book has many loans. Finite-name exposure sizes matter too. Model relevant factors and stresses, and assess concentration in addition to the stylized internal-ratings formula.') as vo:
            self.play(FadeIn(title), FadeIn(answer))
        self.wait(.5)
        self.clear_scene()
