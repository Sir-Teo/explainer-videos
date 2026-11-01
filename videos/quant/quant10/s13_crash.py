from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import bs
from videos.quant.quant10.common import DEL, IMP, LOSS, OPT, PART, SPOT, load


def sci_tex(x: float) -> str:
    e = int(np.floor(np.log10(x)))
    m = x / 10 ** e
    return rf"{m:.1f}\times 10^{{{e}}}"


class Crash(VoiceoverScene):
    def construct(self):
        c = load("crash87")
        self.card()
        self.insurance()
        self.day(c)
        self.tails(c)
        self.after()

    def card(self):
        c = chapter_card(12, r"October 1987", r"What happens when everyone hedges the same way?", lit=(1987,),
                         part=PART)
        with self.voiceover("Chapter twelve. October 1987."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def insurance(self):
        xs = np.linspace(70, 130, 241)
        g = axes([70, 130], [0, 1.05], x_length=6.6, y_length=3.6, xlabel=r"index level",
                 ylabel=r"fraction of the portfolio held in stocks", xticks=[80, 100, 120], yticks=[0, 0.5, 1],
                 font_size=20).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        # a protective put struck at 95, a year out: stocks held = 1 + put delta, as a fraction of value
        frac = xs * (1 + bs.greeks(xs, 95.0, 1.0, 0.2, 0, 0, -1)["delta"]) / (xs + bs.price(xs, 95.0, 1.0, 0.2, 0, 0, -1))
        line = curve(ax, xs, np.clip(frac, 0, 1), DEL, stroke_width=4)
        arr = Arrow(ax.c2p(118, 0.95), ax.c2p(86, 0.55), buff=0, color=LOSS, stroke_width=4,
                    max_tip_length_to_length_ratio=0.12)
        arr_lab = label(r"prices fall $\Rightarrow$ sell", font_size=26, color=LOSS).next_to(arr.get_center(), DOWN + LEFT,
                                                                                        buff=0.1)
        card = history_card(1981, r"Leland, O'Brien and Rubinstein", r"portfolio insurance: a floor under a "
                            r"portfolio, built not from bought puts but by replicating them, Black--Scholes delta "
                            r"hedging with index futures", width=5.4, font_size=24).to_edge(RIGHT, buff=0.5).shift(UP * 0.9)
        size = label(r"by October 1987: some \$60--90 billion insured (Brady report)", font_size=24, color=GREY_A)
        size.next_to(card, DOWN, buff=0.4).align_to(card, LEFT)
        loop = label(r"a hedger who replicates a put sells as prices fall, and buys as they rise", font_size=24,
                     color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "By the mid-1980s the Black-Scholes hedge had become a product. Hayne Leland, John O'Brien and Mark "
            "Rubinstein sold portfolio insurance: a floor under a pension fund's portfolio, built not by buying puts, "
            "which were scarce, but by replicating them, with the delta hedge of this part, trading index futures. "
            "<bookmark mark='a'/> Replicating a put means holding less stock as prices fall. Here is the fraction "
            "of the portfolio held in stocks under a put struck five percent below the market: as the index drops, "
            "the hedge sells. <bookmark mark='b'/> By October 1987 the Brady Commission, which investigated the "
            "crash, put the assets under such strategies at sixty to ninety billion dollars. All of them followed "
            "the same rule. Sell when prices fall."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(g), Create(line))
            self.play(GrowArrow(arr), FadeIn(arr_lab))
            vo.wait_until("b")
            self.play(FadeIn(size), FadeIn(loop))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def day(self, c):
        dates = [str(int(x)) for x in c["window_dates"]]
        r = np.asarray(c["window_ret"], float)
        n = len(r)
        g = axes([0, n], [-0.19, 0.1], x_length=10.0, y_length=4.4, ylabel=r"daily return of the US stock market",
                 yticks=[-0.15, -0.1, -0.05, 0, 0.05], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20)
        g.shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, v in enumerate(r):
            y0, y1 = ax.c2p(i + 0.5, 0)[1], ax.c2p(i + 0.5, v)[1]
            bars.add(Rectangle(width=ax.x_length / n * 0.7, height=max(abs(y1 - y0), 0.003), stroke_width=0,
                               fill_color=LOSS if v < 0 else SPOT, fill_opacity=0.9)
                     .move_to([ax.c2p(i + 0.5, 0)[0], (y0 + y1) / 2, 0]))
        i0 = dates.index("19871019")
        lab = MathTex(rf"{100 * c['ret']:.1f}\%", font_size=40, color=LOSS).next_to(bars[i0], DOWN, buff=0.15)
        day = label(r"Monday 19 October 1987", font_size=26, color=LOSS).next_to(lab, RIGHT, buff=0.3)
        ticks = VGroup()
        for i, d_ in enumerate(dates):
            if d_[6:] in ("01", "02") or i == i0:
                pass
        src = note(r"Kenneth French's data library: the value-weighted US market (Mkt$-$RF $+$ RF), "
                   r"dividends included", font_size=18).to_corner(DR, buff=0.25)
        with self.voiceover(
            "In the week before the nineteenth of October the market fell several days running, and the insurers' "
            "rule told them to sell futures. Their selling pushed futures below the stocks; arbitrageurs bought "
            "futures and sold stocks; stocks fell; the rule said sell again. <bookmark mark='a'/> On Monday the "
            "nineteenth, the broad US market, in Kenneth French's data, fell "
            f"{-100 * c['ret']:.1f} percent in a day; the S and P five hundred, 20.5. It is still the largest "
            "one-day fall in the history of the American market. The hedge assumed that it could always trade, "
            "at a price near the last one, in any size. That day, it could not."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src))
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if r[i] < 0 else DOWN) for i, b_ in enumerate(bars) if i < i0],
                                  lag_ratio=0.05, run_time=3))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[i0], UP), run_time=1.5)
            self.play(FadeIn(lab), FadeIn(day))
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if r[i] < 0 else DOWN) for i, b_ in enumerate(bars) if i > i0],
                                  lag_ratio=0.05, run_time=2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tails(self, c):
        card = crisis_card(
            r"19 October 1987", r"Black Monday, measured",
            rf"against the market's own volatility over the year before ({100 * c['trailing_sd']:.2f}\% a day)",
            stats=[(rf"{c['z']:.1f}\,\sigma", r"the fall in standard deviations"),
                   (sci_tex(c['years_gauss']), r"years between such days, if returns were Gaussian"),
                   (rf"{c['years_tail']:.0f}", r"years between such days, under the fitted power-law tail")],
            width=10.4, font_size=28).to_edge(UP, buff=0.6)
        fit = label(rf"power-law tail fitted to the worst 2\% of days, 1926--1986: exponent "
                    rf"$\alpha = {c['alpha']:.2f}$ (Hill estimator)", font_size=24, color=GREY_A)
        fit.next_to(card, DOWN, buff=0.5)
        worst = label(rf"the worst day before it: {100 * c['worst_before']:.1f}\% (log), 29 October 1929",
                      font_size=24, color=GREY_A).next_to(fit, DOWN, buff=0.25)
        with self.voiceover(
            "How unlikely was it? Against the market's own volatility over the previous year, the fall was "
            f"{-c['z']:.1f} standard deviations. If daily returns were normal, as the lognormal model says, a day "
            f"like that would come once in about ten to the {int(np.floor(np.log10(c['years_gauss'])))} years: "
            "never, in any universe. <bookmark mark='a'/> But Part one measured the tails of real returns: they "
            "fall off like a power, not like a Gaussian. Fit a power law to the worst two percent of days from "
            f"1926 to 1986, and the exponent comes out {c['alpha']:.2f}, close to the inverse cubic law; under that "
            f"tail, a day like Black Monday comes about once every {c['years_tail']:.0f} years. Rare, but not "
            "impossible: the kind of event a long-lived institution should expect to meet."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(fit), FadeIn(worst))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def after(self):
        k = np.linspace(-0.3, 0.2, 101)
        before = 0.17 + 0.0 * k
        after = 0.17 - 0.45 * k + 0.6 * k ** 2
        g = axes([-0.3, 0.2], [0.08, 0.36], x_length=6.4, y_length=3.6, xlabel=r"log-moneyness",
                 ylabel=r"implied volatility, index options", xticks=[-0.2, -0.1, 0, 0.1],
                 yticks=[0.1, 0.2, 0.3], yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=20)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        ax = g.ax
        l0 = curve(ax, k, before, GREY_B, stroke_width=3)
        l1 = curve(ax, k, after, IMP, stroke_width=4)
        leg = legend([(GREY_B, r"before 1987: nearly flat"), (IMP, r"after: the skew")], font_size=22)
        leg.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        sch = note(r"schematic (Rubinstein 1994 documents the change in S\&P 500 options)", font_size=18)
        sch.next_to(g, DOWN, buff=0.1).align_to(g, LEFT)
        pts = VGroup(
            label(r"the formula's world broke, and the market priced the break:", font_size=26, color=GREY_A),
            label(r"crash protection has cost extra ever since", font_size=26, color=IMP),
            label(r"MacKenzie: the model shaped the market that seemed to fit it,", font_size=24, color=GREY_B),
            label(r"until the market stopped fitting it", font_size=24, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5)
        if pts.width > 6.2:
            pts.scale_to_fit_width(6.2).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "And then options changed. Before October 1987, index options traded on implied volatilities that "
            "barely depended on the strike: the market priced roughly the Black-Scholes world. After it, "
            "out-of-the-money puts, crash insurance, became permanently dearer than the formula's single volatility "
            "allows. Mark Rubinstein, one of the portfolio insurers, documented it in 1994. That is the skew of "
            "chapter nine, born here. <bookmark mark='a'/> The sociologist Donald MacKenzie read the episode as a "
            "case of performativity: for fourteen years the formula helped make the market look like the formula, "
            "and then, in one day, the market stopped looking like it. Part twelve is about that skew."
        ) as vo:
            self.play(FadeIn(g), Create(l0), FadeIn(leg[0]), FadeIn(sch))
            self.play(Create(l1), FadeIn(leg[1]))
            self.play(FadeIn(pts[:2]))
            vo.wait_until("a")
            self.play(FadeIn(pts[2:]))
        self.wait(0.4)
        self.clear_scene()
