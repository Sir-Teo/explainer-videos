from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAIN, GAUSS, LOSS, PART, REAL, VOL, bars, load, real_data

C_ = {r"R": REAL, r"r": REAL, r"\mu": QC.IDEA, r"m": QC.IDEA, r"\sigma^2": VOL, r"\tfrac12\sigma^2": VOL,
      r"\tfrac12 s^2": VOL, r"s^2": VOL, r"L": QC.HOUSE}


def row(*parts, fs=40):
    return cmath(*parts, colors=C_, font_size=fs)


class Returns(VoiceoverScene):
    def construct(self):
        d = load("drag")
        self.card()
        self.definitions()
        self.updown()
        self.annual(d)
        self.derive(d)
        self.leverage(d)

    def card(self):
        c = chapter_card(2, r"Prices, returns and the drag", r"Why does the average return overstate what you earn?",
                         part=PART)
        with self.voiceover("Chapter two. Prices, returns and the drag."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def definitions(self):
        d1 = definition_card(r"Simple return", MathTex(r"R_t = \frac{P_t}{P_{t-1}} - 1", font_size=40, color=REAL),
                             width=5.6, color=REAL)
        d2 = definition_card(r"Log return", MathTex(r"r_t = \ln\frac{P_t}{P_{t-1}} = \ln(1 + R_t)", font_size=40,
                                                    color=REAL), width=5.6, color=REAL)
        top = VGroup(d1, d2).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.5)
        multi = VGroup(
            MathTex(r"1 + R_{0\to T} = (1 + R_1)(1 + R_2)\cdots(1 + R_T)", font_size=36),
            MathTex(r"r_{0\to T} = r_1 + r_2 + \cdots + r_T", font_size=36),
        ).arrange(DOWN, buff=0.35).next_to(top, DOWN, buff=0.6)
        w1 = why(r"simple returns compound: they multiply")
        w2 = why(r"log returns add: sums, so averages and the central limit theorem apply")
        w1.next_to(multi[0], DOWN, buff=0.08)
        multi[1].next_to(w1, DOWN, buff=0.3)
        w2.next_to(multi[1], DOWN, buff=0.08)
        small = MathTex(r"r = R - \tfrac12 R^2 + \tfrac13 R^3 - \cdots", font_size=34, color=GREY_A)
        small.next_to(w2, DOWN, buff=0.5)
        sw = why(r"for small moves, the two are nearly the same; for big ones they are not")
        sw.next_to(small, DOWN, buff=0.1)
        with self.voiceover(
            "Two ways to measure a move. The simple return: today's price over yesterday's, minus one. That is what "
            "you earn. The log return: the logarithm of the same ratio. <bookmark mark='a'/> The difference shows up "
            "over many periods. Simple returns compound: you multiply one plus each return. Log returns just add. A "
            "sum is what statistics knows how to handle: averages, variances, and the central limit theorem all "
            "work on sums. <bookmark mark='b'/> For small moves the two are almost equal, since the log of one plus "
            "R is R minus half R squared and so on. For large moves they part ways, and that half R squared is "
            "where the rest of this chapter lives."
        ) as vo:
            self.play(FadeIn(d1, shift=UP * 0.2))
            self.play(FadeIn(d2, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Write(multi[0]), FadeIn(w1))
            self.play(Write(multi[1]), FadeIn(w2))
            vo.wait_until("b")
            self.play(Write(small), FadeIn(sw))
        self.wait(0.3)
        self.clear_scene()

    def updown(self):
        g = axes([-0.5, 2.5], [0, 170], x_length=5.6, y_length=4.0, ylabel=r"wealth", yticks=[0, 50, 100, 150],
                 font_size=20).to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        ax = g.ax
        vals = [100, 150, 75]
        cols = [GREY_B, GAIN, LOSS]
        bs = VGroup(*[Rectangle(width=0.9, height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=c,
                                fill_opacity=0.85).move_to(ax.c2p(i, v / 2)) for i, (v, c) in enumerate(zip(vals, cols))])
        tops_ = VGroup(*[MathTex(str(v), font_size=34).next_to(b, UP, buff=0.1) for v, b in zip(vals, bs)])
        steps = VGroup(MathTex(r"+50\%", font_size=34, color=GAIN).move_to(ax.c2p(0.5, 160)),
                       MathTex(r"-50\%", font_size=34, color=LOSS).move_to(ax.c2p(1.5, 160)))
        right = VGroup(
            MathTex(r"\text{average return} = \tfrac12(+50\%) + \tfrac12(-50\%) = 0", font_size=34),
            MathTex(r"\text{what you have} = 1.5 \times 0.5 = 0.75", font_size=34, color=LOSS),
            MathTex(r"\text{average log return} = \tfrac12(\ln 1.5 + \ln 0.5) = -14\%", font_size=34, color=REAL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.5).shift(UP * 0.4)
        if right.width > 7.2:
            right.scale_to_fit_width(7.2).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "The smallest example. You have a hundred dollars. It rises fifty percent, to one hundred and fifty, then "
            "falls fifty percent, to seventy-five. <bookmark mark='a'/> The average of the two returns is zero. But "
            "you lost a quarter of your money. The log returns tell the truth: their average is minus fourteen "
            "percent a period. Repeat the coin flip, up fifty or down fifty, forever, and the average outcome stays "
            "at a hundred, because a few lucky paths get enormous, while the typical path goes to zero."
        ) as vo:
            self.play(FadeIn(g), GrowFromEdge(bs[0], DOWN), FadeIn(tops_[0]))
            self.play(GrowFromEdge(bs[1], DOWN), FadeIn(tops_[1]), FadeIn(steps[0]))
            self.play(GrowFromEdge(bs[2], DOWN), FadeIn(tops_[2]), FadeIn(steps[1]))
            vo.wait_until("a")
            for r_ in right:
                self.play(FadeIn(r_, shift=LEFT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def annual(self, d):
        ys, a = np.asarray(d["years"]), np.asarray(d["annual"])
        g = axes([1926, 2021], [-0.5, 0.6], x_length=10.6, y_length=3.9, ylabel=r"the market's return, each calendar year",
                 xticks=[1930, 1950, 1970, 1990, 2010], yticks=[-0.4, 0, 0.4], xfmt=lambda v: f"{int(v)}",
                 yfmt=lambda v: f"{100 * v:+.0f}\\%" if v else "0", font_size=18).shift(UP * 0.9)
        ax = g.ax
        bb = bars(ax, ys, a, ax.x_length / 95 * 0.75, GAIN, LOSS)
        mean_l = DashedLine(ax.c2p(1926, d["arith"]), ax.c2p(2021, d["arith"]), color=QC.IDEA, stroke_width=2.5)
        geo_l = DashedLine(ax.c2p(1926, d["geo"]), ax.c2p(2021, d["geo"]), color=REAL, stroke_width=2.5)
        stats_ = VGroup(
            MathTex(rf"\text{{arithmetic mean}}\ {100 * d['arith']:.2f}\%", font_size=32, color=QC.IDEA),
            MathTex(rf"\text{{geometric mean (what \$1 grew at)}}\ {100 * d['geo']:.2f}\%", font_size=32, color=REAL),
            MathTex(rf"\text{{gap}}\ {100 * (d['arith'] - d['geo']):.2f}\%", font_size=32),
            MathTex(rf"\tfrac12\sigma^2 = \tfrac12({100 * d['sd']:.1f}\%)^2 = {100 * d['half_var']:.2f}\%", font_size=32,
                    color=VOL),
        ).arrange_in_grid(2, 2, buff=(0.8, 0.2), flow_order="dr", col_alignments="ll").next_to(g, DOWN, buff=0.35).set_x(0)
        src = real_data(r"calendar-year returns, 1927--2020, compounded from Ken French's daily market returns")
        with self.voiceover(
            "Now ninety-four real years. Each bar is a calendar year of the American market, dividends included. "
            f"<bookmark mark='a'/> The arithmetic average of these returns is {100 * d['arith']:.2f} percent. But a "
            f"dollar invested in 1927 grew at {100 * d['geo']:.2f} percent a year: the geometric mean. "
            f"<bookmark mark='b'/> The gap is {100 * (d['arith'] - d['geo']):.2f} points. And half the variance of the "
            f"annual returns, with a standard deviation of {100 * d['sd']:.1f} percent, is {100 * d['half_var']:.2f}. "
            "Almost the same number. That is not a coincidence."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN if v >= 0 else UP) for b, v in zip(bb, a)], lag_ratio=0.03,
                                  run_time=4))
            vo.wait_until("a")
            self.play(Create(mean_l), FadeIn(stats_[0]))
            self.play(Create(geo_l), FadeIn(stats_[1]))
            vo.wait_until("b")
            self.play(FadeIn(stats_[2]))
            self.play(FadeIn(stats_[3]))
        self.wait(0.4)
        self.clear_scene()

    def derive(self, d):
        rows = [
            row(r"\mathbb E[1 + R]", r"=", r"\mathbb E\big[e^{r}\big]", fs=40),
            row(r"\mathbb E[1 + R]", r"=", r"e^{\,m + \tfrac12 s^2}", fs=40),
            row(r"\text{arithmetic}", r"\approx", r"m", r"+", r"\tfrac12 s^2", fs=40),
            row(r"\text{geometric}", r"=", r"e^{m} - 1", r"\approx", r"m", fs=40),
            row(r"\text{arithmetic} - \text{geometric}", r"\approx", r"\tfrac12 s^2", fs=40),
        ]
        whys = [why(r"$1 + R = e^r$"), why(r"if $r \sim N(m, s^2)$: the lognormal mean"),
                why(r"expand for small $m$ and $s^2$"),
                why(r"a dollar grows like $e^{\sum r}$: at rate $m$"),
                why(r"volatility drag: variance lowers growth, not the average")]
        step = ladder(self, rows, whys, keep=5, top=3.0, x=-1.0, buff=0.55, edge=6.9)
        with self.voiceover(
            "Here is why. One plus the simple return is e to the log return. <bookmark mark='a'/> If the log return "
            "is normal with mean m and variance s squared, the average of e to the r is e to the m plus half s "
            "squared: the mean of a lognormal. <bookmark mark='b'/> So the arithmetic average return is about m "
            "plus half s squared. <bookmark mark='c'/> But a dollar grows like e to the sum of the log returns, at "
            "rate m. That is the geometric return. <bookmark mark='d'/> The difference is half the variance: "
            "volatility drag. Variance does not change the average return. It lowers the growth that a single "
            "investor, living through one path, actually gets."
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
        self.wait(0.6)
        self.clear_scene()

    def leverage(self, d):
        t = np.asarray(d["t"])
        g = axes([1926, 2021], [-2.2, 5.7], x_length=7.0, y_length=4.6, ylabel=r"\$1 invested in July 1926 (log scale)",
                 xticks=[1930, 1960, 1990, 2020], yticks=[-2, 0, 2, 4], xfmt=lambda v: f"{int(v)}",
                 yfmt=lambda v: (rf"\${10 ** v:,.0f}".replace(",", "{,}") if v >= 0 else rf"\${10 ** v:.2f}"),
                 font_size=18)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        cols = {1: REAL, 2: QC.IDEA, 3: LOSS}
        lines = {L: curve(ax, t, np.log10(np.maximum(np.asarray(d[f"w{L}"]), 1e-6)).clip(-2.19, 5.69), cols[L],
                          stroke_width=2.5) for L in (1, 2, 3)}
        ends = VGroup(*[MathTex(rf"{L}\times:\ \${d['final'][str(L)]:,.0f}".replace(",", "{,}"), font_size=24,
                                color=cols[L]) for L in (1, 2, 3)])
        ends.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.c2p(1930, 5.0), aligned_edge=UL)
        # growth against leverage: the parabola
        mu = d["growth_theory"]
        g2 = axes([0, 5], [-0.05, 0.16], x_length=4.6, y_length=3.4, xlabel=r"leverage $L$",
                  ylabel=r"growth per year", xticks=[0, 1, 2, 3, 4, 5], yticks=[0, 0.05, 0.1, 0.15],
                  yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=18).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        a2 = g2.ax
        # g(L) = r + L (mu - r) - L^2 sigma^2 / 2, fitted through the three computed points
        Ls = np.array([1.0, 2.0, 3.0])
        gs = np.array([mu["1"], mu["2"], mu["3"]])
        cfit = np.polyfit(Ls, gs, 2)
        xx = np.linspace(0, 5, 101)
        par = curve(a2, xx, np.clip(np.polyval(cfit, xx), -0.05, 0.16), GREY_B, stroke_width=2.5)
        pts = VGroup(*[Dot(a2.c2p(L, d["growth"][str(int(L))]), radius=0.08, color=cols[int(L)]) for L in Ls])
        kel = d["kelly"]
        kl = DashedLine(a2.c2p(kel, -0.05), a2.c2p(kel, float(np.polyval(cfit, kel))), color=QC.IDEA, stroke_width=2)
        klab = MathTex(rf"L^* = \frac{{\mu - r}}{{\sigma^2}} = {kel:.1f}", font_size=26, color=QC.IDEA)
        klab.move_to(a2.c2p(kel + 0.15, 0.0), aligned_edge=LEFT)
        fees = note(r"daily rebalancing, borrowing at the Treasury bill rate, no fees: an idealized fund", font_size=18)
        fees.to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The drag has a famous consequence. Here is a dollar invested in the market in 1926, and in two funds "
            "that hold two and three times the market each day, borrowing the rest at the Treasury bill rate, "
            f"with no fees. <bookmark mark='a'/> The plain market turned a dollar into {d['final']['1']:,.0f}. "
            f"Twice the market made {d['final']['2']:,.0f}. Three times the market made only "
            f"{d['final']['3']:,.0f}: three times the risk for barely more money, and on the way, by the summer of "
            f"1932, it had lost {100 * (1 - d['low']['3']):.1f} percent. <bookmark mark='b'/> Growth is "
            "the average minus half the variance, and leverage multiplies the average by L but the variance by L "
            "squared. So growth is a parabola in leverage. It peaks at the excess return over the variance, about "
            f"{kel:.1f} times, for this market and this century, and beyond that, more leverage grows more slowly, "
            "and eventually ruins you. That peak is the Kelly criterion, the subject of Part eight, and a lesson "
            "every leveraged fund in this series will relearn."
            " If prices drift, and their spread grows like the square root of time, what kind of path are they? Next: the random walk."
        ) as vo:
            self.play(FadeIn(g), FadeIn(fees))
            self.play(*[Create(lines[L]) for L in (1, 2, 3)], run_time=5, rate_func=linear)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e) for e in ends], lag_ratio=0.6, run_time=4))
            vo.wait_until("b")
            self.play(FadeIn(g2), Create(par))
            self.play(LaggedStart(*[GrowFromCenter(p) for p in pts], lag_ratio=0.3))
            self.play(Create(kl), FadeIn(klab))
        self.wait(0.5)
        self.clear_scene()
