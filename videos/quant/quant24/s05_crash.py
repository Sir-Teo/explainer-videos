from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant24.common import BAD, GOOD, MKT, PART, UMD, ask, fit_right, illustration, load


class Crash(VoiceoverScene):
    def construct(self):
        c = load("crash")
        self.card()
        self.months(c)
        self.y1932(c)
        self.worst(c)
        self.mechanism()
        self.betas(c)
        self.option()
        self.scaling(c)
        self.caution()

    def card(self):
        c = chapter_card(4, r"Momentum crashes", r"Why does momentum fail exactly when the market recovers?", lit=(2009,),
                         part=PART)
        with self.voiceover("Chapter four. The momentum crash: when it happens, why, and what can be done about it."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def months(self, c):
        w = c["w2009_full"]
        d, u, mk = np.asarray(w["date"]), np.asarray(w["umd"]), np.asarray(w["mkt"])
        g = axes([-0.6, len(d) - 0.4], [-0.4, 0.15], x_length=8.6, y_length=4.4, xlabel=r"", ylabel=r"monthly return",
                 xticks=[], yticks=[-0.3, -0.2, -0.1, 0, 0.1], font_size=13).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        bars = VGroup()
        for i, (a, b) in enumerate(zip(u, mk)):
            for off, v, col in ((-0.2, b, MKT), (0.2, a, UMD)):
                y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, max(v, -0.4))[1]
                bars.add(Rectangle(width=0.36, height=max(abs(y1 - y0), 0.01), stroke_width=0, fill_color=col,
                                   fill_opacity=0.85).move_to([ax.c2p(i + off, 0)[0], (y0 + y1) / 2, 0]))
        labs = VGroup(*[label(t_, font_size=14, color=GREY_A).next_to(ax.c2p(i, -0.4), DOWN, buff=0.1)
                        for i, t_ in ((0, r"Jan 2008"), (8, r"Sep"), (14, r"Mar 2009"), (16, r"May"), (23, r"Dec"))])
        hl = Rectangle(width=ax.c2p(16.5, 0)[0] - ax.c2p(13.5, 0)[0], height=4.4, stroke_color=BAD, stroke_width=2,
                       fill_opacity=0).move_to([(ax.c2p(13.5, 0)[0] + ax.c2p(16.5, 0)[0]) / 2, ax.c2p(0, -0.125)[1], 0])
        side = VGroup(
            legend([(MKT, r"the market, less bills"), (UMD, r"momentum, UMD")], font_size=17),
            MathTex(rf"\text{{Mar--May 2009}}:\ UMD\ {100 * c['w2009']['cum_umd']:.0f}\%", font_size=24, color=BAD),
            MathTex(rf"\text{{market}}\ {100 * c['w2009']['cum_mkt']:+.0f}\%", font_size=24, color=MKT),
            wrapped_label(r"through 2008 momentum did well while the market fell: it was short the banks. In April 2009 "
                          r"alone it lost 34\%", 3.6, 16, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here are the two years month by month, the market in blue and momentum in pink. <bookmark mark='a'/> "
            "Through 2008, as the market fell, momentum did well: its short side was full of banks and cyclical "
            "companies, the year's biggest losers. <bookmark mark='b'/> Then the market turned in March 2009. The "
            "losers, priced for bankruptcy, rebounded hardest. Momentum lost twelve percent in March, thirty-four in "
            "April and thirteen in May: about half its value in three months, while the market rose by a quarter."
        ) as vo:
            self.play(FadeIn(g), FadeIn(labs), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if b_.get_center()[1] < ax.c2p(0, 0)[1] else DOWN)
                                    for b_ in bars[:28]], lag_ratio=0.03), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, UP if b_.get_center()[1] < ax.c2p(0, 0)[1] else DOWN)
                                    for b_ in bars[28:]], lag_ratio=0.03), Create(hl), FadeIn(side[1:]), run_time=2)
        self.add(illustration(r"Kenneth French's data library: Mkt-RF and the momentum factor"))
        self.wait(0.4)
        self.clear_scene()

    def y1932(self, c):
        w = c["w1932"]
        cc = crisis_card(r"July--August 1932", r"The first momentum crash",
                         r"the Dow bottomed on 8 July 1932 after losing about 89\% from its 1929 peak. In the next two "
                         r"months the market nearly doubled, led by the most beaten-down stocks: momentum, short exactly "
                         r"those, had its two worst months ever",
                         stats=[(rf"{100 * w['cum_umd']:.0f}\%", r"momentum, July and August 1932"),
                                (rf"+{100 * w['cum_mkt']:.0f}\%", r"the market, the same two months")], width=8.6,
                         font_size=20)
        with self.voiceover(
            "It had happened before. In July 1932 the Dow Jones bottomed, eighty-nine percent below its 1929 peak. "
            "<bookmark mark='a'/> In July and August the market rose more than eighty percent, led by the stocks that "
            "had fallen furthest. Momentum lost seventy-four percent in two months, its two worst months on record. "
            "The pattern is the same: a long bear market, a short side full of crushed stocks, and a sudden rebound."
        ) as vo:
            self.play(FadeIn(cc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(cc, color=BAD, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    def worst(self, c):
        ws = c["worst"][:6]
        context = {193208: r"after the 1932 low", 193207: r"after the 1932 low", 200904: r"after the 2009 low",
                   193909: r"war in Europe; the market jumps", 200101: r"the Nasdaq's January rally",
                   193806: r"a sharp rally in June 1938"}
        tab = VGroup()
        for i, w in enumerate(ws):
            y = 2.0 - 0.62 * i
            dt = f"{w['date'] // 100}-{w['date'] % 100:02d}"
            tab.add(VGroup(MathTex(dt, font_size=26).move_to([-4.0, y, 0]),
                           MathTex(rf"{100 * w['r']:.1f}\%", font_size=28, color=BAD).move_to([-1.2, y, 0]),
                           label(context.get(w["date"], r""), font_size=18, color=GREY_A).move_to([3.0, y, 0])))
        title = label(r"Momentum's six worst months, 1927--2020", font_size=26).to_edge(UP, buff=0.5)
        foot = wrapped_label(r"every one came in a sharp market rebound, five of them after a long decline", 12.0, 17,
                             GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The six worst months in ninety-four years. <bookmark mark='a'/> Two in the summer of 1932; April 2009; "
            "September 1939, when war in Europe sent the market sharply up; January 2001, the Nasdaq's rally; and June "
            "1938. Every one came in a sharp market rebound. Momentum crashes are not random. They are predictable in "
            "kind, if not in date."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tab], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def mechanism(self):
        rows = [cmath(r"\beta_{\text{UMD},t}", r"=", r"\beta_{\text{winners},t} - \beta_{\text{losers},t}", font_size=42,
                      colors={r"\beta_{\text{UMD},t}": UMD}),
                cmath(r"\text{after a bear market}:", r"\ ", r"\beta_{\text{losers}} \gg 1 > \beta_{\text{winners}}\ "
                      r"\Rightarrow\ \beta_{\text{UMD}} \ll 0", font_size=36)]
        whys = [why(r"Daniel and Moskowitz (2016): momentum's market beta is not fixed; it is the beta of whatever won "
                    r"less the beta of whatever lost over the past year"),
                why(r"after a long fall, the losers are the stocks that fell most with the market: the highest-beta, most "
                    r"leveraged firms. Momentum is then short a high-beta portfolio, a large bet against a rebound it does "
                    r"not know it is making")]
        step = ladder(self, rows, whys, keep=2, top=2.5, x=-0.6, buff=0.8, edge=6.9)
        with self.voiceover(
            "Kent Daniel and Tobias Moskowitz explained the mechanism. Momentum's market beta is not fixed. It is the "
            "beta of whatever won over the past year less the beta of whatever lost. <bookmark mark='a'/> After a long "
            "bear market, the losers are the stocks that fell hardest with the market: the most leveraged, highest-beta "
            "firms. So momentum ends up short a very high-beta portfolio, a large bet against a market rebound that "
            "nobody chose to make."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
        self.wait(0.4)
        self.clear_scene()

    def betas(self, c):
        cd = c["cond"]
        hx = [-4.2, -1.4, 1.0, 3.6]
        heads = [r"months", r"how many", r"beta on the market", r"momentum, a year"]
        tab = VGroup(VGroup(*[label(h_, font_size=18, color=GREY_A).move_to([x, 2.1, 0]) for h_, x in zip(heads, hx)]))
        for i, k in enumerate(("normal", "bear, market down", "bear, market up")):
            v = cd[k]
            y = 1.4 - 0.65 * i
            tab.add(VGroup(label({"normal": r"normal", "bear, market down": r"bear market, market falls",
                                  "bear, market up": r"bear market, market rises"}[k], font_size=19).move_to([hx[0], y, 0]),
                           MathTex(str(v["n"]), font_size=26).move_to([hx[1], y, 0]),
                           MathTex(f"{v['beta']:+.2f}", font_size=26, color=BAD if v["beta"] < -0.3 else WHITE).move_to(
                               [hx[2], y, 0]),
                           MathTex(rf"{100 * v['mean']:+.0f}\%", font_size=26,
                                   color=BAD if v["mean"] < 0 else GOOD).move_to([hx[3], y, 0])))
        foot = wrapped_label(r"1927--2020. A bear market: the market's return over the previous 24 months is negative. In "
                             r"those months momentum's beta turns sharply negative, and when the market then rises it "
                             r"loses at a rate of almost 50\% a year", 12.0, 17, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Measure it. Split the months by whether the market had fallen over the previous two years. "
            "<bookmark mark='a'/> In normal times momentum's beta is about zero, and it earns about eleven percent a "
            "year. <bookmark mark='b'/> In bear markets its beta falls to minus a half, and when the market keeps "
            "falling it does well. <bookmark mark='c'/> But in bear-market months when the market rises, its beta is "
            "about minus one, and it loses at a rate of nearly fifty percent a year. The crashes live in those hundred "
            "months."
        ) as vo:
            self.play(FadeIn(tab[0]))
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(tab[i + 1], shift=RIGHT * 0.2))
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def option(self):
        g = axes([-0.3, 0.3], [-0.3, 0.15], x_length=6.4, y_length=4.2, xlabel=r"the market's return",
                 ylabel=r"momentum's return, in a bear market", xticks=[-0.2, 0, 0.2], yticks=[-0.2, -0.1, 0, 0.1],
                 font_size=13).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        ax = g.ax
        xs = np.linspace(-0.3, 0.3, 61)
        ys = np.where(xs < 0, -0.5 * xs, -1.0 * xs) * 0.5
        pay = curve(ax, xs, ys, UMD, stroke_width=3.5)
        side = VGroup(
            wrapped_label(r"in a bear market, momentum gains a little when the market falls and loses a lot when it "
                          r"rises: the payoff of a short call on the market. Daniel and Moskowitz price it so, and the "
                          r"option is cheapest to sell exactly when the market's volatility is highest", 3.8, 17, GREY_A),
            wrapped_label(r"illustrative slopes from the betas above", 3.8, 15, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        fit_right(side)
        with self.voiceover(
            "Draw it as a payoff. In a bear market, momentum gains a little if the market falls further, and loses a "
            "lot if it rises. <bookmark mark='a'/> That is the shape of a short call on the market, from Part ten. "
            "Momentum investors are, without meaning to, selling options on a rebound, and those options are worth "
            "most just when volatility is highest, after a crash. The premium is real, and so is the occasional bill."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(Create(pay), FadeIn(side), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def scaling(self, c):
        d = np.asarray(c["date"])
        t = d // 100 + (d % 100 - 0.5) / 12
        raw = np.log10(np.asarray(c["cum"]))
        vs = np.asarray(c["vs"], float)
        sc = np.log10(np.cumprod(1 + np.nan_to_num(vs)))
        g = axes([1927, 2021], [-0.5, 5.0], x_length=8.0, y_length=4.4, xlabel=r"year", ylabel=r"\$1 in 1927, $\log_{10}$",
                 xticks=[1930, 1950, 1970, 1990, 2010], yticks=[0, 1, 2, 3, 4, 5], font_size=14).to_edge(LEFT, buff=0.5).shift(
            DOWN * 0.3)
        ax = g.ax
        l1 = curve(ax, t, raw, UMD, stroke_width=2.4)
        l2 = curve(ax, t, sc, GOOD, stroke_width=2.4)
        r_, s_ = c["raw"], c["scaled"]
        hx = [0.0, 1.5, 2.8]
        tab = VGroup(VGroup(*[label(h_, font_size=15, color=GREY_A).move_to([x, 0, 0]) for h_, x in
                              zip((r"", r"raw", r"scaled"), hx)]))
        for i, (nm, a, b) in enumerate(((r"Sharpe", f"{r_['sharpe']:.2f}", f"{s_['sharpe']:.2f}"),
                                         (r"skew", f"{r_['skew']:.2f}", f"{s_['skew']:.2f}"),
                                         (r"worst drawdown", rf"{100 * r_['maxdd']:.0f}\%", rf"{100 * s_['maxdd']:.0f}\%"),
                                         (r"Mar--May 2009", rf"{100 * c['raw_2009']:.0f}\%", rf"{100 * c['scaled_2009']:.0f}\%"))):
            y = -0.45 * (i + 1)
            tab.add(VGroup(label(nm, font_size=15).move_to([hx[0], y, 0]), MathTex(a, font_size=20, color=UMD).move_to(
                [hx[1], y, 0]), MathTex(b, font_size=20, color=GOOD).move_to([hx[2], y, 0])))
        side = VGroup(legend([(UMD, r"UMD"), (GOOD, r"scaled to 12\% expected volatility")], font_size=15), tab,
                      wrapped_label(r"Barroso and Santa-Clara (2015): hold 12\% / (last six months' realised volatility) "
                                    r"of the factor, capped at 3. Point in time", 3.6, 15, GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "One repair is simple. Momentum's crashes come when its volatility is already high, so hold less of it "
            "then. Pedro Barroso and Pedro Santa-Clara scale the factor each month to a constant expected volatility, "
            "using only the past six months. <bookmark mark='a'/> On ninety-four years the Sharpe ratio rises from "
            "about a half to three quarters; the skewness from minus three to minus eight tenths; the worst drawdown "
            "from seventy-eight percent to forty-six. The 2009 crash is halved. <bookmark mark='b'/> Daniel and "
            "Moskowitz's own version goes further, forecasting the mean as well as the variance, and leaning out of "
            "momentum in bear markets."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(l1), Create(l2), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[2]))
        self.wait(0.4)
        self.clear_scene()

    def caution(self):
        cards = VGroup(
            desk_question(r"in sample?", r"no: the scaling uses only past returns. But which window, which target and "
                          r"which cap were chosen after seeing the data, and Part 26 counts those choices", width=12.0,
                          font_size=20),
            desk_question(r"everywhere?", r"Cederburg, O'Doherty, Wang and Yan (2020): volatility management helps "
                          r"momentum but not most other factors once implemented in real time", width=12.0, font_size=20),
            desk_question(r"the crowd", r"in a crash, every momentum fund is short the same stocks; the faster the "
                          r"rebound, the more of them buy at once. Crowding is a thread of Parts 33 and 41", width=12.0,
                          font_size=20),
        ).arrange(DOWN, buff=0.3)
        if cards.height > 6.6:
            cards.scale_to_fit_height(6.6)
        with self.voiceover(
            "Three cautions. <bookmark mark='a'/> The scaling uses only past data, so it is not look-ahead. But the "
            "window, the target and the cap were chosen by researchers who knew the history, and Part twenty-six "
            "counts such choices. <bookmark mark='b'/> It does not generalise well: Scott Cederburg and colleagues "
            "found volatility management helps momentum but not most other factors, implemented in real time. "
            "<bookmark mark='c'/> And in a crash every momentum fund is short the same stocks. When they rebound, all "
            "must buy at once. That is crowding, a thread that runs through the rest of the series."
        ) as vo:
            for i, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[i], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()
        q = ask(r"the market has fallen 40\% over two years and has just risen 10\% in a month. Momentum's beta is about "
                r"$-1$. What would you do with a momentum position, and what does it cost you if you are wrong?")
        with self.voiceover("The market has fallen forty percent over two years and has just risen ten percent in a "
                            "month. Momentum's beta is about minus one. What would you do with a momentum position, and "
                            "what does it cost you if you are wrong?"):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
