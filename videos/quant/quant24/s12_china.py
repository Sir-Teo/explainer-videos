from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, HML, MKT, PART, SMB, UMD, ask, fit_right, illustration, load


class China(VoiceoverScene):
    def construct(self):
        c = load("china")
        self.card()
        self.market()
        self.shell()
        self.ch4()
        self.table(c)
        self.paths(c)
        self.lesson()

    def card(self):
        c = chapter_card(11, r"China's factors", r"Do the American factors travel to a market of retail traders?",
                         lit=(2019,), part=PART)
        with self.voiceover("Chapter eleven. The world's second-largest stock market, and the factors it needs."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def market(self):
        cards = VGroup(
            desk_question(r"who trades", r"individual investors account for most of the trading volume in A-shares, far "
                          r"more than in the US, and turnover is several times higher", width=12.0, font_size=20),
            desk_question(r"how firms list", r"initial public offerings are approved by the regulator and the queue is "
                          r"long, so a listed company has value as a vehicle for a private firm to list by reverse merger",
                          width=12.0, font_size=20),
            desk_question(r"what that does to size", r"the smallest listed firms are priced partly as shells: their "
                          r"returns follow the odds of a takeover, not their businesses", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        foot = wrapped_label(r"Historical mechanisms: 2000--2020 sample; nationwide registration-based IPO reform in 2023", 12.0, 18, GREY_A).to_edge(DOWN, buff=0.35)
        self.add(foot)
        with self.voiceover(
            "The institutional discussion concerns the historical Chinese A-share sample, 2000 through 2020. <bookmark mark='a'/> Retail participation and turnover were high in the cited studies. <bookmark mark='b'/> Approval constraints made listing access valuable and encouraged some reverse mergers. <bookmark mark='c'/> Small listed firms could therefore carry shell value as well as business value. These historical mechanisms should not be presented as unchanged current rules; the nationwide registration-based IPO reform arrived in 2023."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def shell(self):
        rows = [cmath(r"P", r"=", r"P^{\text{business}} + \pi\,V^{\text{shell}}", font_size=46, colors={r"P": MKT})]
        whys = [why(r"Liu, Stambaugh and Yuan (2019), 'Size and value in China': a tiny firm's price includes the chance "
                    r"$\pi$ of a reverse merger times the value of its listing. Its book-to-market and earnings say little "
                    r"about its business. So they drop the smallest 30\% of stocks before building any factor")]
        step = ladder(self, rows, whys, keep=1, top=2.4, x=-0.4, buff=0.8, edge=6.9)
        with self.voiceover(
            "Jianan Liu, Robert Stambaugh and Yu Yuan wrote the price of a tiny Chinese firm as the value of its "
            "business plus the chance of a reverse merger times the value of its listing. For such a firm, size and "
            "valuation ratios measure the shell, not the company. So before building any factor they drop the "
            "smallest thirty percent of stocks. It is a lesson in itself: the same characteristic can mean different "
            "things in different institutions."
        ) as vo:
            step(0)
        self.wait(0.4)
        self.clear_scene()

    def ch4(self):
        cards = VGroup(
            desk_question(r"SMB", r"size, among the 70\% of stocks that remain, 2 x 3 as in the US", width=12.0,
                          font_size=20),
            desk_question(r"VMG: value minus growth", r"on earnings to price, not book to market: in China E/P captures "
                          r"value best, absorbing B/M, cash flow to price and the others", width=12.0, font_size=20),
            desk_question(r"PMO: pessimistic minus optimistic", r"on abnormal turnover: stocks traded far more than usual "
                          r"are those retail optimism has bid up, and they subsequently lag", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        with self.voiceover(
            "Their model, CH-four, has four factors. The market, and <bookmark mark='a'/> size, built as in America "
            "on the stocks that remain. <bookmark mark='b'/> Value, measured by earnings to price rather than book to "
            "market, because in China it absorbs all the other valuation ratios. <bookmark mark='c'/> And a turnover "
            "factor, pessimistic minus optimistic: stocks traded far more than usual are the ones retail enthusiasm "
            "has bid up, and they go on to lag. A sentiment factor, built for a market of individual traders."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def table(self, c):
        hx = [-4.4, -1.4, 1.2, 4.0]
        heads = [r"factor, 2000--2020", r"China: mean, Sharpe", r"US: mean, Sharpe", r""]
        tab = VGroup(VGroup(*[label(h_, font_size=17, color=GREY_A).move_to([x, 2.2, 0]) for h_, x in zip(heads, hx)]))
        rows = [("market", "mktrf", "mkt"), ("size", "SMB", "smb"), ("value", "VMG", "hml"), ("turnover (PMO)", "PMO", None)]
        for i, (nm, k, u) in enumerate(rows):
            s = c[k]
            y = 1.5 - 0.62 * i
            us = c["us"][u] if u else None
            tab.add(VGroup(label(nm, font_size=19).move_to([hx[0], y, 0]),
                           MathTex(rf"{100 * s['mean']:.1f}\%,\ {s['sharpe']:.2f}", font_size=24,
                                   color=GOOD if s["sharpe"] > 0.6 else WHITE).move_to([hx[1], y, 0]),
                           MathTex(rf"{100 * us['mean']:.1f}\%,\ {us['sharpe']:.2f}" if us else r"\text{---}", font_size=24,
                                   color=GREY_B).move_to([hx[2], y, 0])))
        foot = wrapped_label(r"Liu, Stambaugh and Yuan's CH-4 factors as Robert Stambaugh publishes them, monthly, January "
                             r"2000 to December 2020, beside the Fama--French US factors over the same months. Chinese "
                             rf"value earned {100 * c['VMG']['mean']:.0f}\% a year with a Sharpe ratio above one while US "
                             r"value earned almost nothing", 12.0, 16, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Compare the original Chinese and US factors over the same calendar months, 2000 through 2020. <bookmark mark='a'/> The universes and constructions differ; equal dates do not make them identical controlled portfolios. <bookmark mark='b'/> Chinese earnings-price value has a high sample Sharpe and turnover a positive mean. US HML uses book-to-market and a different universe. These associations do not prove retail trading caused the difference, or establish implementable premia after costs and shorting constraints."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(tab[1]), FadeIn(tab[2]))
            vo.wait_until("a")
            self.play(Indicate(tab[1][1]))
            vo.wait_until("b")
            self.play(FadeIn(tab[3]), FadeIn(tab[4]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def paths(self, c):
        d = np.asarray(c["date"])
        t = d // 100 + (d % 100 - 0.5) / 12
        g = axes([2000, 2021], [-0.1, 1.3], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel='research index, $\\log_{10}$; start 1',
                 xticks=[2000, 2005, 2010, 2015, 2020], yticks=[0, 0.5, 1.0], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        cols = {"SMB": SMB, "VMG": HML, "PMO": UMD}
        lines = VGroup(*[curve(ax, t, np.log10(np.asarray(c["cum"][k])), cols[k], stroke_width=2.6) for k in cols])
        side = VGroup(
            legend([(SMB, r"size"), (HML, r"value (E/P)"), (UMD, r"turnover")], font_size=17),
            MathTex(rf"\rho(\text{{size}}, \text{{value}}) = {np.asarray(c['corr'])[1, 2]:.2f}", font_size=22),
            wrapped_label('size and value are strongly negatively correlated in China, more than in the US: small Chinese firms are expensive. Displayed calculations end in December 2020; the public CH4 source also contains 2021 observations', 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The paths, twenty-one years. <bookmark mark='a'/> Value climbs almost steadily, and turnover too; "
            "size is weaker and lumpier. And size and value are strongly negatively "
            "correlated, about minus six tenths: in China, the small firms are the expensive ones, a trace of the shell "
            "premium even after the smallest are removed."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(side[1]), FadeIn(side[2]),
                      run_time=3)
        self.add(illustration(r"Robert Stambaugh's website: CH-4 factors, monthly, to 2021"))
        self.wait(0.4)
        self.clear_scene()

    def lesson(self):
        cards = VGroup(
            desk_question(r"institutions shape factors", 'listing constraints and retail trading motivate market-specific hypotheses; return associations alone do not identify causal premia',
                          width=12.0, font_size=20),
            desk_question(r"and they change", r"when the regulator tightened the rules on reverse mergers in 2016, and "
                          r"as quantitative funds grew in China, the premia were exposed to the same crowding as "
                          r"America's: Part 29's A-share drawdown of February 2024", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Two lessons. <bookmark mark='a'/> Institutional mechanisms motivate market-specific definitions, but return associations alone do not establish that listing rules or retail enthusiasm caused a premium. <bookmark mark='b'/> Institutions change: reverse-merger rules tightened, registration-based IPO reform expanded, and trading technology and crowding evolved. The 2000-to-2020 factor history is not a certificate of a stable current or future opportunity."
        ) as vo:
            for i, mk in enumerate(("a", "b")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"Chinese value earned a Sharpe ratio above one in 2000--2020, while American value earned almost "
                r"nothing. Would you expect it to continue? What would make it stop?")
        with self.voiceover("Chinese value earned a Sharpe ratio above one from 2000 to 2020, while American value earned "
                            "almost nothing. Would you expect it to continue, and what would make it stop?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
