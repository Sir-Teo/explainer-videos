from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import BAD, GOOD, NOISE, PART, RULE, ask, comma, fit_right, illustration, load


class Survivor(VoiceoverScene):
    def construct(self):
        s = load("survivor")
        self.card()
        self.tickers(s)
        self.delisting()
        self.simulate(s["sim"])
        self.byvol(s["sim"])
        self.forms()
        self.question()

    def card(self):
        c = chapter_card(2, r"Survivorship", r"Who is missing from the data?", lit=(2001, 2008), part=PART)
        with self.voiceover("Chapter two. Survivorship: the companies, funds and strategies that are missing from the "
                            "data because they failed."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def tickers(self, s):
        fl = s["floats"]
        bk = s["bank_by_year"]
        ys = list(range(2011, 2021))
        g = axes([2010.4, 2020.6], [0, 100], x_length=8.2, y_length=4.2, xlabel=r"year",
                 ylabel=r"still in the SEC's ticker file today, \%", xticks=[2011, 2013, 2015, 2017, 2019],
                 yticks=[0, 25, 50, 75, 100], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        pub, bad = VGroup(), VGroup()
        for y in ys:
            n, k = fl[str(y)]
            v = 100 * k / n
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
            pub.add(Rectangle(width=0.32, height=y1 - y0, stroke_width=0, fill_color=RULE, fill_opacity=0.85).move_to(
                [ax.c2p(y - 0.18, 0)[0], (y0 + y1) / 2, 0]))
            if str(y) in bk:
                n2, k2 = bk[str(y)]
                v2 = 100 * k2 / n2
                y2 = ax.c2p(0, v2)[1]
                bad.add(Rectangle(width=0.32, height=max(y2 - y0, 0.02), stroke_width=0, fill_color=BAD,
                                  fill_opacity=0.9).move_to([ax.c2p(y + 0.18, 0)[0], (y0 + y2) / 2, 0]))
        leg = legend([(RULE, r"public companies that year"), (BAD, r"companies that filed for bankruptcy that year")],
                     font_size=15).next_to(ax, UP, buff=0.15).align_to(ax, RIGHT)
        side = VGroup(
            MathTex(rf"{100 * s['float12_share']:.0f}\%\ \text{{of 2012's filers}}", font_size=26, color=RULE),
            MathTex(rf"{100 * s['bank_share']:.0f}\%\ \text{{of the bankrupt}}", font_size=26, color=BAD),
            wrapped_label(rf"EDGAR's filers with a public float in each year, and the {s['bank_n']} that reported a "
                          rf"bankruptcy (8-K item 1.03), 2009--2020, matched by CIK against the SEC's current ticker "
                          rf"file ({comma(s['n_tickers'])} companies). The others merged, were bought, went private or "
                          rf"failed", 3.5, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Suppose you build a stock universe the easy way, from today's list of tickers, and then download their "
            "price histories. Who is in it? <bookmark mark='a'/> Of the companies that had public shares in 2012, only "
            "about two in five are still in the SEC's ticker file today; the rest merged, were bought, went private, "
            "or failed. For 2020's companies, two in three remain. <bookmark mark='b'/> Now the companies that filed for "
            "bankruptcy. Of the nine hundred and seventy-seven that reported one between 2009 and 2020, sixty are still "
            "there: six percent. <bookmark mark='c'/> A universe drawn from today's list has quietly removed almost every "
            "company that went to zero. Its backtest never holds a stock on the way down to bankruptcy, because those "
            "stocks are not in the data."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in pub], lag_ratio=0.1), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bad], lag_ratio=0.1), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.add(illustration(r"EDGAR frames (dei:EntityPublicFloat), full-text search (8-K item 1.03), company\_tickers.json"))
        self.wait(0.4)
        self.clear_scene()

    def delisting(self):
        rows = [cmath(r"r_{\text{last month}}", r"=", r"\frac{P_{\text{last trade}} + D}{P_{\text{prev}}} - 1", font_size=36,
                      colors={r"r_{\text{last month}}": WHITE}),
                cmath(r"r_{\text{delisting}}", r"=", r"\frac{\text{what holders actually got}}{P_{\text{last trade}}} - 1",
                      font_size=36, colors={r"r_{\text{delisting}}": BAD}),
                cmath(r"r_{\text{missing}}", r"\approx", r"-30\%\ \ \text{(performance delistings, NYSE and AMEX)}",
                      font_size=34, colors={r"r_{\text{missing}}": BAD})]
        whys = [why(r"the last return a price file can compute: from the previous close to the last trade on the "
                    r"exchange"),
                why(r"what a holder received after the stock left the exchange: an over-the-counter price, a "
                    r"liquidation payment, often close to nothing"),
                why(r"Shumway (1997): the price file was missing most of these for stocks delisted for poor "
                    r"performance; on average they were large losses. Leave them out and the worst stocks' worst month "
                    r"disappears")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.6, buff=0.45, edge=6.9)
        with self.voiceover(
            "Even a careful database, one that keeps dead companies, can lose the moment they die. <bookmark mark='a'/> "
            "A price file computes returns from trade to trade, and the last one it can compute ends at the last "
            "trade on the exchange. <bookmark mark='b'/> But a holder's loss does not stop there: after delisting the "
            "stock trades over the counter, or is liquidated, often for close to nothing. That is the delisting "
            "return. <bookmark mark='c'/> In 1997 Tyler Shumway showed that the standard research file was missing "
            "most delisting returns for stocks removed for poor performance, and that these missing returns were on "
            "average large losses, around minus thirty percent. Any strategy that buys distressed stocks looked better "
            "than it was until the gap was filled; on Nasdaq, Shumway and Vincent Warther found in 1999 that filling it "
            "removed the size effect altogether."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.wait(0.1)
        self.wait(0.5)
        self.clear_scene()

    def simulate(self, sm):
        e = np.linspace(-30, 30, 41)
        c = (e[:-1] + e[1:]) / 2
        ha, hs = np.asarray(sm["hist_all"], float), np.asarray(sm["hist_alive"], float)
        top = float(max(ha.max(), hs.max()) * 1.1)
        g = axes([-30, 30], [0, top], x_length=7.6, y_length=4.0, xlabel=r"a manager's average return, \% a year",
                 ylabel=r"managers", xticks=[-30, -15, 0, 15, 30], yticks=[], font_size=14).to_edge(LEFT, buff=0.5)
        g.shift(DOWN * 0.3)
        ax = g.ax

        def bars(h, col, op):
            out = VGroup()
            for x, v in zip(c, h):
                if v <= 0:
                    continue
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                out.add(Rectangle(width=ax.c2p(1.4, 0)[0] - ax.c2p(0, 0)[0], height=y1 - y0, stroke_width=0,
                                  fill_color=col, fill_opacity=op).move_to([ax.c2p(x, 0)[0], (y0 + y1) / 2, 0]))
            return out
        ba, bs = bars(ha, NOISE, 0.45), bars(hs, GOOD, 0.75)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, top), color=GREY_C, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"\text{{all}}:\ {abs(100 * sm['mean_all']):.1f}\%", font_size=28, color=NOISE),
            MathTex(rf"\text{{survivors}}:\ {100 * sm['mean_alive']:+.1f}\%", font_size=28, color=GOOD),
            MathTex(rf"\text{{survived}}:\ {100 * sm['alive']:.0f}\%", font_size=24, color=GREY_A),
            wrapped_label(rf"{comma(sm['n'])} managers with no skill, volatilities from 5\% to 35\%, {sm['years']} years; a "
                          rf"manager whose cumulative return ever falls below $-30\%$ leaves the database, record and "
                          rf"all", 3.5, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Funds die too, and fund databases forget them. Stephen Brown, William Goetzmann, Roger Ibbotson and "
            "Stephen Ross showed in 1992 what that does to a performance study. Simulate it. <bookmark mark='a'/> Five "
            "thousand managers, none with any skill: their average returns centre on zero. <bookmark mark='b'/> Now let "
            "the database drop anyone whose cumulative return ever falls thirty percent below where they started, as "
            "investors leave and the fund closes. <bookmark mark='c'/> The survivors average three and a half percent a "
            "year. No one has any skill, and the industry that survives looks as if it does."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in ba], lag_ratio=0.02), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bs], lag_ratio=0.02), FadeIn(side[1]),
                      FadeIn(side[2]), run_time=2)
        self.add(illustration(r"simulated: the House's \texttt{backtest.survivorship}"))
        self.wait(0.4)
        self.clear_scene()

    def byvol(self, sm):
        vb = sm["by_vol"]
        g = axes([0.04, 0.36], [0, 100], x_length=6.0, y_length=3.6, xlabel=r"a manager's volatility, \% a year",
                 ylabel=r"survived, \%", xticks=[0.05, 0.15, 0.25, 0.35], xfmt=lambda v: f"{100 * v:.0f}",
                 yticks=[0, 50, 100], font_size=13).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        ax = g.ax
        g2 = axes([0.04, 0.36], [0, 10], x_length=5.0, y_length=3.6, xlabel=r"a manager's volatility, \% a year",
                  ylabel=r"survivors' average return, \%", xticks=[0.05, 0.15, 0.25, 0.35], xfmt=lambda v: f"{100 * v:.0f}",
                  yticks=[0, 5, 10], font_size=13).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        ax2 = g2.ax
        b1, b2 = VGroup(), VGroup()
        for v in vb:
            x = (v["lo"] + v["hi"]) / 2
            w = ax.c2p(0.04, 0)[0] - ax.c2p(0, 0)[0]
            y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, 100 * v["alive"])[1]
            b1.add(Rectangle(width=w, height=y1 - y0, stroke_width=0, fill_color=NOISE, fill_opacity=0.8).move_to(
                [ax.c2p(x, 0)[0], (y0 + y1) / 2, 0]))
            w2 = ax2.c2p(0.04, 0)[0] - ax2.c2p(0, 0)[0]
            z0, z1 = ax2.c2p(0, 0)[1], ax2.c2p(0, 100 * v["mean_alive"])[1]
            b2.add(Rectangle(width=w2, height=max(z1 - z0, 0.02), stroke_width=0, fill_color=GOOD, fill_opacity=0.85)
                   .move_to([ax2.c2p(x, 0)[0], (z0 + z1) / 2, 0]))
        foot = wrapped_label(r"the quiet managers almost all survive, with records near zero; the volatile ones mostly "
                             r"die, and the few who survive were the lucky ones. A database of survivors rewards risk-taking "
                             r"that did not, on average, pay", 12.2, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "And notice who survives. <bookmark mark='a'/> Quiet managers, with five or ten percent volatility, almost "
            "all survive, and their records stay near zero. Volatile ones mostly die. <bookmark mark='b'/> But the "
            "volatile ones who survive were the lucky ones, and their records are the best in the database: nearly "
            "nine percent a year for the boldest. Survivorship does not just inflate the average. It makes risk-taking "
            "look like skill."
        ) as vo:
            self.play(FadeIn(g), FadeIn(g2))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b1], lag_ratio=0.15), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in b2], lag_ratio=0.15), FadeIn(foot), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def forms(self):
        cards = VGroup(
            desk_question(r"index membership", r"backtesting today's index members over twenty years: every one of them "
                          r"was a success, by construction. Membership must be as of each date", width=12.2, font_size=19),
            desk_question(r"backfill", r"a fund joins a database after a good start, and brings its history with it: the "
                          r"first years in the database are its best", width=12.2, font_size=19),
            desk_question(r"the strategy graveyard", r"the same holds for a firm's own ideas: strategies that were "
                          r"switched off leave the report, and the survivors' track record looks like the firm's", width=12.2,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Survivorship takes other forms. <bookmark mark='a'/> Index membership: backtest today's S&P 500 members over "
            "twenty years and every one of them was a success, by construction; membership has to be taken as of each "
            "date. <bookmark mark='b'/> Backfill: a fund joins a database after a good start and brings its history "
            "along, so its first years in the database are its best. <bookmark mark='c'/> And the strategy graveyard: "
            "inside a firm, the strategies that were switched off leave the report, and the survivors' record starts "
            "to look like the firm's. The House keeps its dead strategies in the Track Record for exactly this reason."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                if k:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a backtest buys every stock in today's S\&P 500, equally weighted, from 2000 to 2020. Which way is "
                r"its bias, and roughly how would you measure it without a survivorship-free database?")
        with self.voiceover(
            "Pause and predict. A backtest buys every stock in today's S and P five hundred, equally weighted, from "
            "2000 to 2020. Which way is the bias, and how might you measure it without paying for a survivorship-free "
            "database?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
