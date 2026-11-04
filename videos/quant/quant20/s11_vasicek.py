from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, PART, RISKY, SAFE, ask, fit_right, illustration, load


class Vasicek(VoiceoverScene):
    def construct(self):
        v = load("vasicek")
        self.card()
        self.derive()
        self.pdfs(v)
        self.basel(v)

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
                why(r"given the economy, defaults are independent, so in a large pool the default fraction is exactly "
                    r"the conditional probability $p(M)$: all idiosyncratic risk diversifies away"),
                why(r"so the pool's loss distribution is that of a function of one normal variable, in closed form")]
        step = ladder(self, rows, whys, keep=3, top=2.8, x=-1.0, buff=0.7, edge=6.9)
        with self.voiceover(
            "A bank lends to thousands of borrowers. Each defaults if its own Merton variable falls below a "
            "threshold, and each variable is one part the economy, shared by all, and one part its own luck. Oldrich "
            "Vasicek worked out what follows. <bookmark mark='a'/> Given the state of the economy, defaults are "
            "independent; in a large enough pool the fraction that defaults is simply the conditional probability. "
            "Individual luck diversifies away completely. <bookmark mark='b'/> What remains is one random variable, "
            "the economy, and the pool's loss distribution is a closed formula."
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
            wrapped_label(r"the mean never moves; correlation moves the tail. A bank that lends to borrowers who fail "
                          r"together needs capital for the year they all do", 3.6, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is what correlation does. Every pool defaults two percent a year on average. <bookmark mark='a'/> "
            "With no shared factor, the default rate is two percent almost every year. <bookmark mark='b'/> As the "
            "borrowers share more of their fate, the typical year gets better and the bad years much worse. "
            f"<bookmark mark='c'/> In the worst year in a thousand, a pool with correlation 0.15 loses "
            f"{100 * q['0.15']:.0f} percent of its borrowers, and one with 0.3 loses {100 * q['0.3']:.0f}. The average "
            "is the same; the capital needed is not."
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
            wrapped_label(r"Basel II's internal-ratings formula (2004), founded by Gordy (2003): Vasicek's 99.9th "
                          r"percentile less the expected loss, which provisions cover; $\rho$ falls from 0.24 to 0.12 as "
                          r"PD rises (big safe firms move with the economy), LGD 45\%, maturity $M$ = 2.5 years", 3.8, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.6)
        fit_right(side)
        with self.voiceover(
            "That is exactly how bank capital is set. Basel II's internal-ratings formula takes the loss in the "
            "worst year in a thousand of Vasicek's pool, subtracts the expected loss, which provisions already cover, "
            "and adjusts for maturity. Michael Gordy showed in 2003 that only a one-factor model makes each loan's "
            "capital add up, independent of the rest of the portfolio. <bookmark mark='a'/> The curve rises steeply "
            "for safe loans and flattens for risky ones, because the formula assumes risky borrowers depend less on "
            f"the economy. <bookmark mark='b'/> At a one percent PD it asks for {100 * v['rw_1pct'] / 12.5:.1f} cents "
            f"of capital per dollar lent: a risk weight of {100 * v['rw_1pct']:.2f} percent, the number in the Basel "
            "Committee's own tables."
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
