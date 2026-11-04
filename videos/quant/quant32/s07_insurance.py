from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART, PUT_C, SPY_C, TREND_C, fit_right, load


class Insurance(VoiceoverScene):
    def construct(self):
        v = load("shortvol")
        self.card()
        self.index()
        self.paths(v)
        self.table(v)
        self.decompose(v)
        self.crisis()
        self.buyers()
        self.mirror()
        self.question()

    def card(self):
        c = chapter_card(7, r"Selling insurance", r"Is the volatility premium a premium, or a loan from the next crash?",
                         part=PART)
        with self.voiceover("Chapter seven. Parts eleven and twelve measured the variance risk premium: options are, on "
                            "average, more expensive than the volatility that follows. Here is what selling them "
                            "systematically feels like."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def index(self):
        rows = [cmath(r"\text{each month}", r":", r"\text{sell a one-month at-the-money S\&P 500 put}", font_size=32),
                cmath(r"\text{collateral}", r":", r"\text{the strike, held in Treasury bills}", font_size=32),
                cmath(r"r^{\text{PUT}}", r"=", r"r_f + \text{premium} - \max(K - S_T, 0)/K", font_size=34,
                      colors={r"\max(K - S_T, 0)/K": BAD})]
        whys = [why(r"Cboe's PUT index: a rule anyone could follow, published daily"),
                why(r"fully collateralised, so it never needs leverage or margin calls"),
                why(r"the seller keeps the premium unless the market falls below the strike, and then pays the shortfall")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "Cboe publishes a rule anyone could follow. <bookmark mark='a'/> Each month, sell a one-month put on the "
            "S&P 500 at the money. <bookmark mark='b'/> Keep the full strike in Treasury bills as collateral, so there is "
            "no leverage. <bookmark mark='c'/> Earn the bill rate and the premium, and pay the shortfall whenever the "
            "index ends the month below where it started."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def paths(self, v):
        md = np.asarray(v["months"], float)
        x = md // 100 + ((md % 100) - 0.5) / 12
        ys = {k: 100 * np.asarray(v["cum"][k], float) for k in ("put", "mkt")}
        lo = float(np.floor(min(y.min() for y in ys.values()) / 50) * 50)
        hi = float(np.ceil(max(y.max() for y in ys.values()) / 50) * 50)
        g = axes([x[0], x[-1]], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"2007--2020",
                 ylabel=r"cumulative total return, \%", xticks=[2008, 2012, 2016, 2020], yticks=[lo, 0, hi],
                 xfmt=lambda u: f"{u:.0f}", yfmt=lambda u: f"{u:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        l1 = curve(ax, x, ys["mkt"], SPY_C, stroke_width=3)
        l2 = curve(ax, x, ys["put"], PUT_C, stroke_width=3)
        leg = legend([(SPY_C, r"US stock market"), (PUT_C, r"selling puts (Cboe PUT)")], font_size=16)
        leg.to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            "Fourteen years. <bookmark mark='a'/> The market, with its two crashes. <bookmark mark='b'/> And the put "
            "seller: a smoother line that collects premium month after month, falls with the market in the crashes, and "
            "climbs back more slowly, because a put seller's upside is capped at the premium."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(l1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(l2), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    def table(self, v):
        hx = [-3.6, -0.6, 2.0, 4.6]
        head = VGroup(label(r"", font_size=18), label(r"US market", font_size=18, color=SPY_C),
                      label(r"selling puts", font_size=18, color=PUT_C), label(r"", font_size=18))
        p, m = v["put"], v["mkt"]
        lines = [(r"Sharpe ratio", f"{m['sharpe']:.2f}", f"{p['sharpe']:.2f}"),
                 (r"volatility", rf"{100 * m['vol']:.1f}\%", rf"{100 * p['vol']:.1f}\%"),
                 (r"worst fall", rf"{100 * m['maxdd']:.0f}\%", rf"{100 * p['maxdd']:.0f}\%"),
                 (r"skewness, monthly", f"{m['skew']:.2f}", f"{p['skew']:.2f}")]
        tab = VGroup(head)
        for nm, a, b in lines:
            tab.add(VGroup(label(nm, font_size=20), MathTex(a, font_size=26), MathTex(b, font_size=26), label("", font_size=10)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.75 * j, 0])
        foot = wrapped_label(r"monthly excess returns, February 2007 to December 2020; Cboe's PUT index against Kenneth "
                             r"French's market", 11.0, 16, GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The numbers. <bookmark mark='a'/> The put seller had about three quarters of the market's volatility and a smaller "
            f"worst fall, {abs(100 * p['maxdd']):.0f} percent against {abs(100 * m['maxdd']):.0f}. <bookmark mark='b'/> "
            f"But a lower Sharpe ratio, {p['sharpe']:.2f} against {m['sharpe']:.2f}, and a monthly skewness of "
            f"{p['skew']:.2f}, three times as negative as the market's: the signature of a seller of insurance."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(tab[4]))
        self.wait(0.4)
        self.clear_scene()

    def decompose(self, v):
        rows = [cmath(r"r^{\text{PUT}} - r_f", r"=", r"\alpha + \beta\,(r^{M} - r_f) + \varepsilon", font_size=36),
                cmath(r"\beta", r"=", rf"{v['beta']:.2f},\qquad \alpha = {100 * v['alpha']:+.1f}\%\ \text{{a year}}",
                      font_size=36, colors={r"\beta": HURDLE}),
                cmath(r"\text{covered call}", r"=", r"\text{equity beta} + \text{short volatility} + \text{short timing}",
                      font_size=30)]
        whys = [why(r"regress the put seller's excess return on the market's"),
                why(r"in these fourteen years selling puts was mostly market exposure at a lower beta, with no alpha left "
                    r"after it"),
                why(r"Israelov and Nielsen (2015): an option-selling strategy is equity beta, plus a short volatility "
                    r"position that earns the variance premium, plus an unintended bet against the market's recent "
                    r"direction")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "What was it, really? <bookmark mark='a'/> Regress the put seller on the market. "
            f"<bookmark mark='b'/> A beta of {v['beta']:.2f}, and an alpha of {100 * v['alpha']:+.1f} percent a year: in "
            "these years, selling puts was mostly a lower-beta way to own the market. Over longer samples the index has "
            "looked better; this sample had two crashes in fourteen years. "
            "<bookmark mark='c'/> Roni Israelov and Lars Nielsen split option selling into its parts: equity beta, a "
            "short volatility position that earns the variance premium, and an unintended short bet on the market's "
            "recent direction. Only the middle part is the premium."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def crisis(self):
        card = crisis_card(r"5 February 2018", r"Volmageddon",
                           r"the VIX index more than doubled in one day; exchange-traded notes that paid the inverse of VIX "
                           r"futures lost almost all their value overnight, and Credit Suisse's XIV was terminated; funds "
                           r"that sold volatility with leverage took losses that years of premium could not repay",
                           stats=((r"\times 2", r"the VIX in one day, as reported"),
                                  (r"> 90\%", r"of XIV's value lost overnight, as reported")), width=11.0,
                           font_size=22).move_to(UP * 0.2)
        with self.voiceover(
            "The crisis file. On the fifth of February 2018 the VIX index more than doubled in a day. Exchange-traded "
            "notes that paid the inverse of VIX futures, sold to the public as a steady income, lost almost all their "
            "value overnight, and Credit Suisse terminated its XIV note. It was the same trade as the PUT index, with "
            "leverage and a daily reset, and it shows the shape of the premium: years of small gains, repaid in a day."
        ):
            self.play(FadeIn(card))
            self.wait(1.0)
        self.clear_scene()

    def mirror(self):
        cards = VGroup(
            desk_question(r"selling insurance", r"many small gains, a few large losses: negative skew; it pays most of the "
                          r"time and loses in the crash", width=12.4, font_size=19),
            desk_question(r"trend following", r"many small losses, a few large gains: positive skew; it pays least of "
                          r"the time and gains in the slow crash", width=12.4, font_size=19),
            desk_question(r"together", r"Ilmanen (2012): markets tend to reward selling insurance and lottery tickets, "
                          r"and charge for buying them; a book that holds both is paid for one and insured by the other",
                          width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Put it next to trend following. <bookmark mark='a'/> Selling insurance: many small gains, a few large "
            "losses. <bookmark mark='b'/> Trend following: many small losses, a few large gains. One is short a "
            "straddle, the other long. <bookmark mark='c'/> Antti Ilmanen surveyed the evidence in 2012: markets tend "
            "to reward selling insurance and lottery tickets, and charge for buying them. A macro book that holds both "
            "is paid by one and insured by the other."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def buyers(self):
        cards = VGroup(
            desk_question(r"who buys", r"pension funds, insurers and structured-product desks that must hedge against "
                          r"falls, whatever the price of protection", width=12.4, font_size=19),
            desk_question(r"why it stays expensive", r"Garleanu, Pedersen and Poteshman (2009): dealers who absorb that "
                          r"demand cannot hedge perfectly, so options that are in demand, index puts above all, are priced "
                          r"above their expected payoff", width=12.4, font_size=19),
            desk_question(r"so it is structural", r"the premium should last as long as the hedging demand does; its "
                          r"size moves with dealers' capacity to bear the risk", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Who pays this premium? <bookmark mark='a'/> Pension funds, insurers and the desks behind structured "
            "products, who must hedge against falls at almost any price. <bookmark mark='b'/> Nicolae Garleanu, Lasse "
            "Pedersen and Allen Poteshman showed why the price stays high: dealers who absorb that demand cannot hedge "
            "perfectly, so the options most in demand, index puts above all, are priced above their expected payoff. "
            "<bookmark mark='c'/> So it is a structural premium, and it should last as long as the hedging demand does."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a put seller earns 1\% a month for 50 months, then loses 30\% in one. What was its average "
                       r"monthly return, and its skewness sign?")
        with self.voiceover(
            "Pause and predict. A put seller earns one percent a month for fifty months, then loses thirty percent in "
            "one. What was its average monthly return, and what sign is its skewness?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
