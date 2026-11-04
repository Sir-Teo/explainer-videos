from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, HML, MKT, PART, ask, fit_right, illustration, load


class ValueDecade(VoiceoverScene):
    def construct(self):
        v = load("valuedecade")
        self.card()
        self.drawdown(v)
        self.howbad(v)
        self.spread(v)
        self.identity()
        self.reasons()
        self.devil(v)
        self.verdict()

    def card(self):
        c = chapter_card(8, r"Value's lost decade", r"Is a factor that loses for fourteen years broken?", lit=(2020,),
                         part=PART)
        with self.voiceover("Chapter eight. Value's lost decade, measured, and what it does and does not prove."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def drawdown(self, v):
        d = np.asarray(v["date"])
        t = d // 100 + (d % 100 - 0.5) / 12
        w = np.asarray(v["cum"])
        g = axes([2007, 2021], [0.35, 1.1], x_length=8.2, y_length=4.4, xlabel=r"year", ylabel=r"\$1 in HML, January 2007",
                 xticks=[2008, 2010, 2012, 2014, 2016, 2018, 2020], yticks=[0.4, 0.6, 0.8, 1.0], font_size=14).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, t, w, HML, stroke_width=2.8)
        k = v["dd"]["trough"]
        dot = Dot(ax.c2p(t[k], w[k]), color=BAD, radius=0.08)
        s, p = v["stats_0720"], v["stats_2606"]
        side = VGroup(
            MathTex(rf"2007\text{{--}}2020:\ {100 * s['mean']:.1f}\%\ \text{{a year}},\ t = {s['t']:.1f}", font_size=24,
                    color=BAD),
            MathTex(rf"1926\text{{--}}2006:\ {100 * p['mean']:+.1f}\%\ \text{{a year}}", font_size=24, color=HML),
            MathTex(rf"\text{{trough}}\ (\text{{September 2020}}):\ {100 * v['dd']['max']:.0f}\%", font_size=24, color=BAD),
            wrapped_label(r"the Fama--French value factor, long cheap and short expensive stocks, from January 2007 to "
                          r"December 2020. Growth stocks, technology above all, rose; value stocks, banks and energy "
                          r"among them, fell behind every year but a few", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "From January 2007 to the autumn of 2020, value lost. <bookmark mark='a'/> A dollar in the value factor "
            "fell to forty-two cents, a drawdown of fifty-seven percent, the worst in its history. Over the fourteen "
            "years it averaged minus five percent a year, after eighty years of plus five and a half. "
            "<bookmark mark='b'/> Cheap stocks, banks and energy among them, kept getting cheaper; expensive stocks, "
            "technology above all, kept getting more expensive."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(line), run_time=2.5)
            self.play(FadeIn(dot), FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.add(illustration(r"Kenneth French's data library: HML"))
        self.wait(0.4)
        self.clear_scene()

    def howbad(self, v):
        s, p = v["stats_0720"], v["stats_2606"]
        z = (s["mean"] - p["mean"]) / (s["vol"] / np.sqrt(s["n"] / 12))
        rows = [cmath(r"z", r"=", rf"\frac{{\bar r_{{07\text{{--}}20}} - \mu_{{\text{{before}}}}}}{{\sigma/\sqrt{{14}}}} = "
                      rf"\frac{{{100 * s['mean']:.1f} - {100 * p['mean']:.1f}}}{{{100 * s['vol']:.1f}/\sqrt{{14}}}} "
                      rf"\approx {z:.1f}", font_size=38, colors={r"z": BAD}),
                cmath(r"T^*", r"=", rf"\Big(\frac{{2}}{{SR}}\Big)^2 = \Big(\frac{{2}}{{{p['sharpe']:.2f}}}\Big)^2 \approx "
                      rf"{(2 / p['sharpe']) ** 2:.0f}\ \text{{years}}", font_size=38)]
        whys = [why(r"if value's true premium were still its pre-2007 average, a fourteen-year average this low would be "
                    r"about four standard errors away: rare under normal returns, less rare with fat tails and regime "
                    r"shifts, but a genuine surprise"),
                why(r"and the flip side: with a Sharpe ratio near 0.45, it takes about twenty years for a true premium to "
                    r"reach $t = 2$ (Part 6). A decade proves little either way, which cuts both ways")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "How surprising was it? Suppose value's true premium had stayed at its old average. Then a fourteen-year "
            "average as low as this one sits about four standard errors away. <bookmark mark='a'/> That is rare under "
            "normal returns, though less rare with fat tails, and it is a genuine surprise. But turn the arithmetic "
            "around. With a Sharpe ratio of about a half, a true premium needs about twenty years of data to reach a "
            "t-statistic of two. A decade cannot prove a factor works, and it cannot prove it has stopped."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def spread(self, v):
        yr, sp = np.asarray(v["years"]), np.asarray(v["spread"])
        g = axes([1926, 2021], [1.0, 2.8], x_length=8.2, y_length=4.4, xlabel=r"year",
                 ylabel=r"$\ln(B/M_{\text{value}}) - \ln(B/M_{\text{growth}})$", xticks=[1930, 1950, 1970, 1990, 2010],
                 yticks=[1.0, 1.5, 2.0, 2.5], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = curve(ax, yr, sp, HML, stroke_width=2.8)
        med = DashedLine(ax.c2p(1926, np.median(sp)), ax.c2p(2021, np.median(sp)), color=GREY_B, stroke_width=1.5)
        side = VGroup(
            MathTex(rf"2020:\ {sp[-1]:.2f},\ \text{{above}}\ {100 * v['spread_pct']:.0f}\%\ \text{{of years}}", font_size=24,
                    color=BAD),
            MathTex(rf"\text{{median}}:\ {np.median(sp):.2f}", font_size=22),
            wrapped_label(r"the value spread: the aggregate book-to-market of the cheapest 30\% of stocks over that of the "
                          r"dearest 30\%, each June, in logs (Kenneth French's 'Sum of BE / Sum of ME'). By 2020 value "
                          r"stocks were cheaper relative to growth than at any time since the 1930s, close to the dot-com "
                          r"peak", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Much of the loss shows up in prices, not in businesses. The value spread compares the book-to-market of "
            "the cheapest thirty percent of stocks with that of the dearest thirty percent. <bookmark mark='a'/> Since "
            "1926 it has wandered around a median of about one and a half, in logs. By 2020 it was two point four, "
            "higher than in ninety-six percent of years, a level last seen in the 1930s and approached at the dot-com "
            "peak. Value stocks had become extraordinarily cheap relative to growth stocks."
        ) as vo:
            self.play(FadeIn(g), Create(med))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side), run_time=2.5)
        self.add(illustration(r"Kenneth French's data library: portfolios formed on BE/ME, annual book-to-market"))
        self.wait(0.4)
        self.clear_scene()

    def identity(self):
        rows = [cmath(r"r^{HML}", r"\approx", r"\underbrace{\Delta\,\text{spread}}_{\text{revaluation}} + "
                      r"\underbrace{(\text{profitability, migration})}_{\text{structural}}", font_size=38,
                      colors={r"r^{HML}": HML}),
                cmath(r"\text{spread}_t", r"\approx", r"\textstyle\sum_j \rho^j\big(r^V - r^G\big)_{t+j} - \sum_j \rho^j"
                      r"\big(\text{roe}^V - \text{roe}^G\big)_{t+j}", font_size=34)]
        whys = [why(r"Arnott, Harvey, Kalesnik and Linnainmaa (2021): split value's return into the change in the spread "
                    r"and everything else. Most of 2007--2020's loss was revaluation: growth stocks got dearer relative to "
                    r"value"),
                why(r"and by Part 23's Campbell--Shiller logic, a wide spread must mean either high future returns to "
                    r"value or worse future profitability of value firms. Which one, history will tell")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Rob Arnott, Campbell Harvey, Vitali Kalesnik and Juhani Linnainmaa split value's return into two parts: "
            "the change in the spread, which they called revaluation, and everything else. Most of the lost decade "
            "was revaluation: growth stocks simply became dearer relative to value. <bookmark mark='a'/> Apply Part "
            "twenty-three's Campbell-Shiller identity to the spread itself. A wide spread today must be followed "
            "either by high returns to value, as the spread closes, or by value firms' profits falling further behind. "
            "The identity cannot say which."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def reasons(self):
        cards = VGroup(
            desk_question(r"book value is stale", r"Eisfeldt, Kim and Papanikolaou (2022): book equity omits intangible "
                          r"capital (R\&D, brands, organisation); value built on 'intangible-adjusted' book did much "
                          r"better", width=12.0, font_size=20),
            desk_question(r"falling rates", r"long-duration growth stocks gain most when discount rates fall, and rates "
                          r"fell for the whole decade: value was short duration", width=12.0, font_size=20),
            desk_question(r"crowding and flows", r"growth benefited from passive and momentum flows (chapter 10 of Part "
                          r"23: inelastic markets)", width=12.0, font_size=20),
            desk_question(r"it was just bad luck", r"Israel, Laursen and Richardson (2021): the value spread widened, but "
                          r"cheap firms' fundamentals did not deteriorate more than usual", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.22)
        if cards.height > 6.8:
            cards.scale_to_fit_height(6.8)
        with self.voiceover(
            "Four explanations were offered. <bookmark mark='a'/> Book value is stale: Andrea Eisfeldt, Edward Kim and "
            "Dimitris Papanikolaou showed that accounting book equity leaves out intangible capital, research, brands, "
            "organisation, and a value factor that adds it back did much better. <bookmark mark='b'/> Falling interest "
            "rates: growth stocks are long-duration assets, their cash flows far in the future, and rates fell for the "
            "whole decade. <bookmark mark='c'/> Flows: passive and momentum money flowed toward growth, in markets that "
            "Part twenty-three found inelastic. <bookmark mark='d'/> Or bad luck: Ronen Israel, Kristoffer Laursen and "
            "Scott Richardson found the spread widened while cheap firms' fundamentals were no worse than usual."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c", "d")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def devil(self, v):
        dd, w = np.asarray(v["devil_date"]), np.asarray(v["devil_cum"])
        t = dd // 100 + (dd % 100 - 0.5) / 12
        d2 = np.asarray(v["date"])
        t2 = d2 // 100 + (d2 % 100 - 0.5) / 12
        g = axes([2007, 2021], [0.35, 1.3], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"\$1, January 2007",
                 xticks=[2008, 2012, 2016, 2020], yticks=[0.4, 0.6, 0.8, 1.0, 1.2], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        l1 = curve(ax, t2, np.asarray(v["cum"]), HML, stroke_width=2.4)
        l2 = curve(ax, t, w, GOOD, stroke_width=2.4)
        a, b = v["ff_0720_same"], v["devil_0720"]
        side = VGroup(
            legend([(HML, r"HML, Fama--French"), (GOOD, r"HML with current prices (AQR)")], font_size=16),
            MathTex(rf"{100 * a['mean']:.1f}\%\ \text{{vs}}\ {100 * b['mean']:.1f}\%\ \text{{a year}}", font_size=24),
            wrapped_label(r"Asness and Frazzini (2013), 'The devil in HML's details': Fama and French divide book by the "
                          r"market value of the previous December; using this month's price instead makes value a purer "
                          r"bet against expensive stocks. Same idea, different details, half the loss", 3.6, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Details matter, too. Fama and French compute book-to-market with the price of the previous December, up "
            "to eighteen months stale. Cliff Asness and Andrea Frazzini use the current price. <bookmark mark='a'/> "
            "Over the same fourteen years their version lost about two and a half percent a year instead of five. "
            "Same idea, different details, half the loss: a warning that 'the value factor' is a family of "
            "portfolios, not a single fact."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(l1), Create(l2), FadeIn(side[1]), FadeIn(side[2]), run_time=2.5)
        self.add(illustration(r"AQR data set: The Devil in HML's Details, Factors, Monthly"))
        self.wait(0.4)
        self.clear_scene()

    def verdict(self):
        cards = VGroup(
            desk_question(r"what the decade proves", r"that a factor with a Sharpe ratio of a half can lose for fourteen "
                          r"years, and that investors who hold it must be able to wait that long", width=12.0, font_size=20),
            desk_question(r"what it does not", r"that value is dead: the evidence for the premium was never strong enough "
                          r"for a decade to overturn, nor for one to confirm", width=12.0, font_size=20),
            desk_question(r"what came next", r"the research window ends in December 2020. What value did in 2021--2025 "
                          r"is sealed until chapter 13", width=12.0, font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "The verdict. <bookmark mark='a'/> The decade proves that a factor with a Sharpe ratio of a half can lose "
            "for fourteen years, and that anyone who holds it must be able to wait that long, and to explain the wait "
            "to their clients. <bookmark mark='b'/> It does not prove that value is dead; the evidence was never strong "
            "enough for a decade to overturn. <bookmark mark='c'/> And what happened next is sealed. This part's "
            "research ends in December 2020, at value's trough. Chapter thirteen opens the envelope."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                if i:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"it is December 2020 and the value spread is at its 96th percentile. What would you expect value to do "
                r"next, and how confident could you be?")
        with self.voiceover("It is December 2020, and the value spread is at its ninety-sixth percentile. What would you "
                            "expect value to do next, and how confident could you be?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
