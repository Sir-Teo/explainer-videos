from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, MKT, PART, TSM, UMD, ask, fit_right, illustration, load


class Momentum(VoiceoverScene):
    def construct(self):
        m = load("momentum")
        self.card()
        self.sort()
        self.deciles(m)
        self.skip()
        self.umd(m)
        self.tsmom()
        self.classes(m)
        self.smile(m)
        self.why()

    def card(self):
        c = chapter_card(3, r"Momentum, across stocks and through time", r"Do winners keep winning?", lit=(1993, 2012),
                         part=PART)
        with self.voiceover("Chapter three. Momentum: the strongest, and the strangest, of the classic factors."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def sort(self):
        rows = [cmath(r"s_{i,t}", r"=", r"\textstyle\prod_{k=2}^{12}(1 + r_{i,t-k}) - 1", font_size=42,
                      colors={r"s_{i,t}": UMD}),
                cmath(r"UMD_t", r"=", r"\tfrac12(\text{small up} + \text{big up}) - \tfrac12(\text{small down} + "
                      r"\text{big down})", font_size=34, colors={r"UMD_t": UMD})]
        whys = [why(r"Jegadeesh and Titman (1993): rank stocks on their return over the past year, skipping the most "
                    r"recent month; buy the winners, sell the losers, hold for a month, and repeat"),
                why(r"Carhart (1997), Fama and French's version: a 2 x 3 sort on size and prior return, top and bottom "
                    r"30\% by NYSE breakpoints, rebalanced monthly, so it trades far more than value")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Narasimhan Jegadeesh and Sheridan Titman's recipe, from 1993. Each month, rank stocks on their return over "
            "the past twelve months, leaving out the most recent one. Buy the winners, sell the losers, hold for a "
            "month, and repeat. <bookmark mark='a'/> The factor version, up minus down, is built like size and value, "
            "from a two by three sort on size and past return, but rebalanced every month instead of every year. It "
            "trades far more, which matters for costs, a theme of Part twenty-six."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def deciles(self, m):
        v = np.asarray(m["deciles"])
        g = axes([0.4, 10.6], [0, 0.16], x_length=7.6, y_length=4.4, xlabel=r"past-year return decile (losers to winners)",
                 ylabel=r"excess return, a year", xticks=list(range(1, 11)), yticks=[0, 0.04, 0.08, 0.12, 0.16],
                 font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        bars = VGroup()
        for i, x in enumerate(v):
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, x)[1]
            bars.add(Rectangle(width=0.55, height=max(y1 - y0, 0.01), stroke_width=0,
                               fill_color=interpolate_color(ManimColor(BAD), ManimColor(GOOD), i / 9),
                               fill_opacity=0.85).move_to([ax.c2p(i + 1, 0)[0], (y0 + y1) / 2, 0]))
        side = VGroup(
            MathTex(rf"\text{{winners}}:\ {100 * v[-1]:.1f}\%,\quad \text{{losers}}:\ {100 * v[0]:.1f}\%", font_size=24),
            wrapped_label(r"ten value-weighted portfolios on the past year's return (skipping a month), 1927--2020, "
                          r"above bills. Average returns rise almost monotonically: the losers barely beat cash", 3.6, 16,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Sort every American stock into ten portfolios on its past year's return, and track them for "
            "ninety-four years. <bookmark mark='a'/> The returns climb almost step by step: last year's losers earned "
            "about one percent a year above bills, last year's winners fifteen. No characteristic of a company, no "
            "accounting number, only its recent price. In an efficient market this should not happen, and Eugene Fama "
            "has called momentum the premier anomaly."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.1), FadeIn(side), run_time=3)
        self.add(illustration(r"Kenneth French's data library: 10 portfolios formed on prior (12--2) return"))
        self.wait(0.4)
        self.clear_scene()

    def skip(self):
        cards = VGroup(
            desk_question(r"one month: reversal", r"Jegadeesh (1990), Lehmann (1990): last month's winners tend to lose "
                          r"next month, partly bid--ask bounce and liquidity provision; the short-term reversal factor",
                          width=12.0, font_size=20),
            desk_question(r"two to twelve months: momentum", r"winners keep winning for about a year", width=12.0,
                          font_size=20),
            desk_question(r"three to five years: reversal again", r"De Bondt and Thaler (1985): long-run losers beat "
                          r"long-run winners, value's cousin", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Why skip the latest month? Because returns have three horizons that pull in different directions. "
            "<bookmark mark='a'/> Over a month, they reverse: last month's winners tend to lose a little next month, "
            "partly the bounce between bid and ask, partly the reward for providing liquidity. <bookmark mark='b'/> "
            "Over two to twelve months, they continue. <bookmark mark='c'/> Over three to five years, they reverse "
            "again, as Werner De Bondt and Richard Thaler found, a pattern close to value. Momentum lives in the middle "
            "horizon."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def umd(self, m):
        u = m["umd"]
        rows = [
            (r"mean, a year", rf"{100 * u['mean']:.1f}\%"), (r"volatility", rf"{100 * u['vol']:.1f}\%"),
            (r"Sharpe ratio", rf"{u['sharpe']:.2f} \pm {u['sharpe_se']:.2f}"), (r"$t$ of the mean", rf"{u['t']:.1f}"),
            (r"skewness", rf"{u['skew']:.2f}"), (r"worst month", rf"{100 * u['worst']:.1f}\%"),
            (r"worst drawdown", rf"{100 * u['maxdd']:.0f}\%"),
        ]
        tab = VGroup(*[VGroup(label(a, font_size=20, color=GREY_A).move_to([-1.8, 2.0 - 0.55 * i, 0]),
                              MathTex(b, font_size=28, color=BAD if i >= 4 else WHITE).move_to([2.2, 2.0 - 0.55 * i, 0]))
                       for i, (a, b) in enumerate(rows)])
        title = label(r"UMD, January 1927 to December 2020", font_size=26, color=UMD).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"the best Sharpe ratio of the classic US factors, with the worst skewness: a long right "
                             r"body and a few catastrophic months", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The momentum factor's record, ninety-four years. <bookmark mark='a'/> Seven and a half percent a year, a "
            "Sharpe ratio near a half, a t-statistic of four and a half: the strongest of the classic American "
            "factors. <bookmark mark='b'/> And a skewness of minus three, a worst month of minus fifty-three percent, "
            "a drawdown of seventy-eight. Momentum earns its premium in small steps and gives it back in a few "
            "terrible months."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[:4]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[4:]], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def tsmom(self):
        rows = [cmath(r"r^{TS}_{i,t+1}", r"=", r"\text{sign}\big(r_{i,t-12,t}\big)\,\frac{40\%}{\sigma_{i,t}}\,r_{i,t+1}",
                      font_size=40, colors={r"r^{TS}_{i,t+1}": TSM}),
                cmath(r"TSMOM_{t+1}", r"=", r"\frac{1}{N_t}\textstyle\sum_i r^{TS}_{i,t+1}", font_size=40,
                      colors={r"TSMOM_{t+1}": TSM})]
        whys = [why(r"Moskowitz, Ooi and Pedersen (2012): for each futures market on its own, go long if its own past "
                    r"year's excess return was positive and short if negative, sized to an ex ante volatility of 40\%"),
                why(r"average across 58 futures and forwards: equity indices, bonds, currencies, commodities. Not ranked "
                    r"against each other: the whole book can be net long, or net short, everything. Trend following, "
                    r"written down")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Momentum has a second form. Tobias Moskowitz, Yao Hua Ooi and Lasse Pedersen looked at each futures "
            "market on its own. If its own excess return over the past year was positive, go long; if negative, go "
            "short; size every position to the same expected volatility. <bookmark mark='a'/> Average that over "
            "fifty-eight markets, equity indices, bonds, currencies and commodities, and you have time-series momentum. "
            "Nothing is ranked against anything else, so the whole book can be long everything, or short everything. "
            "It is the trend following that managed-futures funds have run for decades, written down as a factor."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def classes(self, m):
        ts = m["ts"]
        names = [("TSMOM^EQ", r"equity indices"), ("TSMOM^FI", r"bonds"), ("TSMOM^FX", r"currencies"),
                 ("TSMOM^CM", r"commodities"), ("TSMOM", r"all, diversified")]
        g = axes([-0.6, 4.6], [0, 1.2], x_length=7.4, y_length=4.2, xlabel=r"", ylabel=r"Sharpe ratio", xticks=[],
                 yticks=[0, 0.4, 0.8, 1.2], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        bars, labs = VGroup(), VGroup()
        for i, (k, nm) in enumerate(names):
            v = ts[k]["sharpe"]
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            bars.add(VGroup(Rectangle(width=0.8, height=y1 - y0, stroke_width=0, fill_color=TSM if i < 4 else QC.HOUSE,
                                      fill_opacity=0.85).move_to([ax.c2p(i, 0)[0], (y0 + y1) / 2, 0]),
                            MathTex(f"{v:.2f}", font_size=22).next_to(ax.c2p(i, v), UP, buff=0.08)))
            labs.add(label(nm, font_size=14, color=GREY_A).next_to(ax.c2p(i, 0), DOWN, buff=0.15))
        side = VGroup(
            MathTex(rf"2008:\ TSMOM\ {100 * m['ts_2008']:+.0f}\%,\ \text{{market}}\ {100 * m['mkt_2008']:+.0f}\%",
                    font_size=22, color=TSM),
            MathTex(rf"\rho(TSMOM, UMD) = {m['corr_umd_ts']:.2f}", font_size=22),
            wrapped_label(rf"AQR's updated factors, {m['ts_start'] // 100}--2020, monthly, excess of cash. Each asset "
                          r"class alone has a Sharpe ratio near 0.6; together, above 1, because trends in different "
                          r"markets are nearly independent", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "AQR publishes the factor, updated, from 1985. <bookmark mark='a'/> Each asset class on its own has a "
            "Sharpe ratio around six tenths. Together, above one: trends in stock indices, bonds, currencies and "
            "commodities are nearly independent of one another, so the combination is far smoother than any of its "
            "parts. <bookmark mark='b'/> It is related to stock momentum, a correlation of about four tenths, but not "
            "the same thing. And in 2008, when the market fell thirty-eight percent, time-series momentum made "
            "twenty-five."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.25))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.add(illustration(r"AQR data set: Time Series Momentum, Factors, Monthly"))
        self.wait(0.4)
        self.clear_scene()

    def smile(self, m):
        x, y = np.asarray(m["smile"]["m"]), np.asarray(m["smile"]["t"])
        c2 = m["smile"]["fit"]
        g = axes([-0.3, 0.25], [-0.15, 0.3], x_length=7.0, y_length=4.4, xlabel=r"the market's quarterly excess return",
                 ylabel=r"TSMOM, the same quarter", xticks=[-0.2, -0.1, 0, 0.1, 0.2], yticks=[-0.1, 0, 0.1, 0.2, 0.3],
                 font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(a, min(b, 0.3)), radius=0.045, color=TSM, fill_opacity=0.8) for a, b in zip(x, y)])
        xs = np.linspace(-0.28, 0.23, 80)
        fit = curve(ax, xs, np.polyval(c2, xs), WHITE, stroke_width=3)
        side = VGroup(
            MathTex(rf"\hat y = {c2[2]:.3f} {c2[1]:+.2f}\,x {c2[0]:+.2f}\,x^2", font_size=24),
            wrapped_label(r"each dot a quarter, 1985--2020. The fitted curve is a smile: trend following does best when "
                          r"the market moves a lot in either direction, like a long straddle on the market", 3.6, 16,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Plot each quarter's time-series momentum return against the stock market's. <bookmark mark='a'/> The "
            "best-fitting curve is a smile. In big down quarters trend followers are already short and gain; in big up "
            "quarters they are long and gain; in quiet quarters they whipsaw and lose a little. That is the payoff of "
            "a long straddle on the market, from Part eleven, and it is why trend following is sold as crisis "
            "insurance. Insurance with a positive average return, so far."
        ) as vo:
            self.play(FadeIn(g), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.01))
            vo.wait_until("a")
            self.play(Create(fit), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def why(self):
        cards = VGroup(
            desk_question(r"underreaction", r"news spreads slowly (Hong and Stein, 1999); investors anchor on old "
                          r"beliefs (Barberis, Shleifer and Vishny, 1998): prices drift toward the news for months",
                          width=12.0, font_size=20),
            desk_question(r"the disposition effect", r"Grinblatt and Han (2005): investors sell winners too soon and hold "
                          r"losers too long (Part 23), so prices adjust to good and bad news only gradually", width=12.0,
                          font_size=20),
            desk_question(r"risk?", r"no convincing risk story: momentum is not riskier in bad times on average, but it "
                          r"has crash risk, and that is chapter four", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Why does it work? The leading explanations are behavioural. <bookmark mark='a'/> Underreaction: news "
            "spreads slowly through investors, and those who hear it anchor on their old beliefs, so prices drift "
            "toward the news for months. <bookmark mark='b'/> The disposition effect of Part twenty-three: investors "
            "sell winners too early and cling to losers, which slows the adjustment in both directions. "
            "<bookmark mark='c'/> A risk story has been hard to find. Momentum is not, on average, worse in bad times. "
            "But it has a particular, catastrophic kind of risk, and it is the next chapter."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"cross-sectional momentum is always long winners and short losers; time-series momentum can be short "
                r"everything. Which would you expect to do better in a market crash, and in the rebound after it?")
        with self.voiceover("Cross-sectional momentum is always long winners and short losers; time-series momentum can "
                            "be short everything. Which would you expect to do better in a crash, and in the rebound "
                            "after it?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
