from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant20.common import BAD, GOOD, PART, RISKY, SAFE, ask, fit_right, illustration, load


def _t(d):
    d = np.asarray(d)
    return (d // 100 % 100 - 1) * 30.5 + d % 100  # day of the year, roughly


class March(VoiceoverScene):
    def construct(self):
        m = load("march2020")
        self.card()
        self.etfs(m)
        self.spread(m)
        self.facilities()
        self.factors()

    def card(self):
        c = chapter_card(15, r"Corporate bonds and March 2020", r"Can the safest corporate bonds stop trading?",
                         lit=(2020,), part=PART)
        with self.voiceover("Chapter fifteen. Corporate bond markets, and three weeks in March 2020."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def etfs(self, m):
        g = axes([0, 182], [60, 110], x_length=8.0, y_length=4.4, xlabel=r"2020",
                 ylabel=r"price, as \% of 20 February", xticks=[], yticks=[70, 80, 90, 100], font_size=14
                 ).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        months = VGroup(*[label(mn, font_size=16, color=GREY_B).next_to(ax.c2p(x, 60), DOWN, buff=0.15)
                          for mn, x in zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [15, 46, 75, 106, 136, 167])])
        lines = VGroup()
        for tk, c_ in (("LQD", SAFE), ("HYG", BAD)):
            d, p = np.asarray(m[tk]["date"]), np.asarray(m[tk]["close"])
            base = p[np.searchsorted(d, 20200220)]
            lines.add(curve(ax, _t(d), 100 * p / base, c_, stroke_width=2.8))
        ev = VGroup()
        for d, txt in ((20200323, r"23 Mar: the Fed's corporate credit facilities"), (20200409, r"9 Apr: expanded")):
            x = _t(d)
            ev.add(VGroup(DashedLine(ax.c2p(x, 60), ax.c2p(x, 110), color=GREY_B, stroke_width=1.5),
                          label(txt, font_size=15, color=GREY_A).next_to(ax.c2p(x, 108), RIGHT, buff=0.08)))
        ev[1][1].next_to(ax.c2p(_t(20200409), 104), RIGHT, buff=0.08)
        lq, hy = m["LQD"], m["HYG"]
        side = VGroup(
            legend([(SAFE, r"LQD: investment-grade bond ETF"), (BAD, r"HYG: high-yield bond ETF")], font_size=17),
            MathTex(rf"\text{{LQD}}: {100 * lq['drawdown']:.0f}\%\ \text{{by {lq['low']['date'] % 100} March}}", font_size=24,
                    color=SAFE),
            MathTex(rf"\text{{HYG}}: {100 * hy['drawdown']:.0f}\%\ \text{{by {hy['low']['date'] % 100} March}}", font_size=24,
                    color=BAD),
            wrapped_label(r"ETF shares kept trading when the bonds inside them barely did; for days the ETFs traded "
                          r"well below the value of their holdings, the market's real-time price of credit", 3.6, 17,
                          GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "In March 2020, as the pandemic closed economies, everyone wanted cash at once. Corporate bonds, even "
            "investment-grade ones, became hard to sell. <bookmark mark='a'/> The exchange-traded funds that hold "
            f"them kept trading, and fell: the investment-grade fund by {abs(100 * lq['drawdown']):.0f} percent and the "
            f"high-yield fund by {abs(100 * hy['drawdown']):.0f}, in less than a month. <bookmark mark='b'/> On the "
            "twenty-third of March the Federal Reserve announced it would buy corporate bonds and the funds that hold "
            "them; on the ninth of April it widened that to high yield. Prices turned on the first day, long before it had bought much. Valentin Haddad, Alan Moreira and Tyler "
            "Muir found that the announcement alone did most of the work."
        ) as vo:
            self.play(FadeIn(g), FadeIn(months), FadeIn(side[0]))
            self.play(Create(lines), run_time=3)
            vo.wait_until("a")
            self.play(FadeIn(side[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("b")
            self.play(FadeIn(ev))
        self.add(illustration(r"Yahoo Finance closes; Federal Reserve press releases, 23 March and 9 April 2020"))
        self.wait(0.4)
        self.clear_scene()

    def spread(self, m):
        d, v = np.asarray(m["baa"]["date"]), np.asarray(m["baa"]["v"])
        g = axes([0, 182], [1.5, 4.6], x_length=8.0, y_length=4.2, xlabel=r"2020", ylabel=r"Baa minus 10-year Treasury, \%",
                 xticks=[], yticks=[2, 3, 4], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        months = VGroup(*[label(mn, font_size=16, color=GREY_B).next_to(ax.c2p(x, 1.5), DOWN, buff=0.15)
                          for mn, x in zip(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], [15, 46, 75, 106, 136, 167])])
        line = curve(ax, _t(d), v, RISKY, stroke_width=3)
        k = int(np.argmax(v))
        k0 = int(np.searchsorted(d, 20200220))
        top = Dot(ax.c2p(_t(d[k]), v[k]), color=BAD)
        mark = DashedLine(ax.c2p(_t(20200323), 1.5), ax.c2p(_t(20200323), 4.6), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"{v[k0]:.2f}\% \to {v[k]:.2f}\%", font_size=30, color=BAD),
            label(rf"20 February to {d[k] % 100} March", font_size=18, color=GREY_A),
            MathTex(rf"\text{{30 June: }} {v[-1]:.2f}\%", font_size=26),
            wrapped_label(r"in a month the spread rose more than twice as much as in the whole of 2007; after the "
                          r"Fed's announcement it fell back almost as fast", 3.4, 17, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "The same three weeks in the spread of medium-grade bonds over Treasuries: "
            f"<bookmark mark='a'/> from {v[k0]:.2f} percent on the twentieth of February to {v[k]:.2f} on "
            f"{d[k] % 100} March, the day of the announcement. <bookmark mark='b'/> By the end of June it was "
            f"back to {v[-1]:.2f}. The spread had priced a wave of defaults; the backstop priced most of it away."
        ) as vo:
            self.play(FadeIn(g), FadeIn(months), Create(mark))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(top), FadeIn(side[0]), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def facilities(self):
        rows = [cmath(r"\text{PMCCF} + \text{SMCCF}", r"\to", r"\text{the Fed as buyer of last resort for corporate credit}",
                      font_size=32, colors={r"\text{PMCCF} + \text{SMCCF}": GOOD}),
                cmath(r"\Delta s", r"\approx", r"\text{announcement} \gg \text{purchases}", font_size=36,
                      colors={r"\Delta s": RISKY})]
        whys = [why(r"primary and secondary market corporate credit facilities: new issues and existing bonds, then "
                    r"ETFs and recent 'fallen angels'; the facilities bought a small fraction of the market"),
                why(r"Haddad, Moreira and Muir (2021): spreads fell most on announcement days, and for the bonds made "
                    r"eligible: the backstop priced the tail away. A lender of last resort is an option written to "
                    r"the market")]
        step = ladder(self, rows, whys, keep=2, top=2.4, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "The two facilities offered to buy new corporate bonds and existing ones, and then the funds holding them. "
            "In the end the secondary-market facility bought about fourteen billion dollars of bonds and funds, in a "
            "market of some ten trillion. <bookmark mark='a'/> But spreads fell most "
            "on the days of the announcements, and most for the bonds that became eligible. The promise of a buyer "
            "removed the tail, and the tail was what was being priced: a backstop is an option the central bank "
            "writes to the whole market."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def factors(self):
        cards = VGroup(
            desk_question(r"credit factors", r"Bai, Bali and Wen (2019): corporate bond returns load on downside risk, "
                          r"credit risk and illiquidity factors. Dickerson, Mueller and Robotti (2023): once bond data "
                          r"are cleaned, most such factors add little beyond the bond market itself", width=12.0,
                          font_size=21),
            desk_question(r"the distress puzzle", r"Campbell, Hilscher and Szilagyi (2008): stocks of the firms most "
                          r"likely to fail, by a model like chapter 9's, have earned low returns, not the high ones "
                          r"risk would demand; Part 25 returns to it among the anomalies", width=12.0, font_size=21),
        ).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Two debates the series returns to. Do corporate bonds have their own factors, as stocks do? Jennie Bai, "
            "Turan Bali and Quan Wen found several; Alexander Dickerson, Philippe Mueller and Cesare Robotti, after "
            "cleaning the bond data, found that most add little beyond the bond market as a whole. "
            "<bookmark mark='a'/> And the distress puzzle: John Campbell, Jens Hilscher and Jan Szilagyi found that "
            "the shares of the companies most likely to fail have earned less, not more, the opposite of what risk "
            "should pay. Part twenty-five takes it up among the anomalies."
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
        q = ask(r"an ETF trades 5\% below the value its sponsor reports for its bonds. Which price is wrong?")
        with self.voiceover("A bond fund trades five percent below the value its sponsor reports for its bonds. Which "
                            "price is wrong?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
