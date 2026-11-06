from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import BAD, GOOD, HURDLE, PART, SPY_C, TREND_C, VT_C, fit_right, load


class Calendar(VoiceoverScene):
    def construct(self):
        c = load("calendar")
        self.card()
        self.tom(c)
        self.tom_why()
        self.night(c)
        self.night_why(c)
        self.halloween(c)
        self.fomc(c)
        self.events()
        self.mining()
        self.question()

    def card(self):
        c = chapter_card(8, r"Calendars, nights and events", r"Do returns arrive at predictable times?", part=PART)
        with self.voiceover("Chapter eight. Some premia are not about which asset to hold, but when. The calendar, the "
                            "clock and corporate events all leave traces in returns."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def tom(self, c):
        hx = [-4.0, -1.4, 1.0, 3.4, 5.6]
        head = VGroup(label(r"years", font_size=17, color=GREY_B), label(r"turn of month, bp a day", font_size=17,
                                                                         color=GOOD),
                      label(r"other days, bp a day", font_size=17, color=GREY_B), label(r"share of days", font_size=17,
                                                                                       color=GREY_B),
                      label(r"share of return", font_size=17, color=GOOD))
        tab = VGroup(head)
        for k, r in c["tom"].items():
            tab.add(VGroup(label(k.replace("-", "--"), font_size=20), MathTex(f"{r['tom']:.1f}", font_size=26, color=GOOD),
                           MathTex(f"{r['rest']:.1f}", font_size=26), MathTex(rf"{100 * r['share_days']:.0f}\%", font_size=26),
                           MathTex(rf"{100 * r['share_return']:.0f}\%", font_size=26, color=GOOD)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.85 * j, 0])
        foot = wrapped_label(r"US market excess return, Kenneth French's daily file; the turn of the month: the last trading "
                             r"day and the first three of the next; a share above 100\% means the other days lost money",
                             11.6, 16, GREY_A).to_edge(DOWN, buff=0.4)
        a, b, cc = (c["tom"][k] for k in c["tom"])
        with self.voiceover(
            "The turn of the month. <bookmark mark='a'/> Take the last trading day of each month and the first three of "
            "the next: about a fifth of all days. <bookmark mark='b'/> From 1926 to 1962 they earned "
            f"{100 * a['share_return']:.0f} percent of the market's whole excess return; from 1963 to 1990, more than all "
            f"of it, {100 * b['share_return']:.0f} percent, because the other days lost money on average. "
            f"<bookmark mark='c'/> Since 1991 the effect has shrunk: {100 * cc['share_return']:.0f} percent of the return "
            f"on {100 * cc['share_days']:.0f} percent of the days. Still there, but much less."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:3]], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(tab[3]))
        self.wait(0.4)
        self.clear_scene()

    def tom_why(self):
        cards = VGroup(
            desk_question(r"the finding", r"Ariel (1987) and Lakonishok and Smidt (1988): a monthly effect over ninety "
                          r"years of the Dow, concentrated around the turn of the month", width=12.4, font_size=19),
            desk_question(r"a flow story", r"wages, pension contributions and fund inflows arrive at the month end and are "
                          r"invested in the days after (Ogden 1990): a predictable buyer", width=12.4, font_size=19),
            desk_question(r"why it shrank", r"a known calendar effect is cheap to exploit with index futures: traders "
                          r"buying before the flows arrive move the effect earlier and make it smaller", width=12.4,
                          font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "The literature. <bookmark mark='a'/> Robert Ariel found it in 1987, and Josef Lakonishok and Seymour Smidt "
            "confirmed it over ninety years of the Dow. <bookmark mark='b'/> The usual explanation is a flow: wages, "
            "pension contributions and fund inflows arrive at the month end and are invested in the days after. A "
            "predictable buyer. <bookmark mark='c'/> And a predictable buyer is cheap to front-run with futures, which "
            "is one reason the effect has shrunk."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def night(self, c):
        d = np.asarray(c["cum"]["dates"], float)
        x = d // 10000 + ((d // 100) % 100 - 0.5) / 12
        yo = 100 * np.asarray(c["cum"]["over"], float)
        yi = 100 * np.asarray(c["cum"]["intra"], float)
        hi = float(np.ceil(max(yo.max(), yi.max()) / 200) * 200)
        lo = float(np.floor(min(yo.min(), yi.min()) / 50) * 50)
        g = axes([x[0], x[-1]], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"1993--2020",
                 ylabel=r"cumulative return in SPY, \%", xticks=[1995, 2005, 2015], yticks=[0, hi / 2, hi],
                 xfmt=lambda u: f"{u:.0f}", yfmt=lambda u: f"{u:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        l1 = curve(ax, x, yo, VT_C, stroke_width=3)
        l2 = curve(ax, x, yi, SPY_C, stroke_width=3)
        leg = legend([(VT_C, r"overnight: close to next open"), (SPY_C, r"intraday: open to close")], font_size=16)
        leg.to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        fit_right(leg)
        o, i = c["over"], c["intra"]
        st = VGroup(label(rf"overnight: {100 * o['mean']:.1f}\% a year, Sharpe {o['sharpe']:.2f}", font_size=16, color=VT_C),
                    label(rf"intraday: {100 * i['mean']:.1f}\% a year, Sharpe {i['sharpe']:.2f}", font_size=16, color=SPY_C))
        st.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(leg, DOWN, buff=0.4).align_to(leg, LEFT)
        fit_right(st)
        with self.voiceover(
            "The night. Split each day of the S&P 500 fund into two parts: from the close to the next morning's open, "
            "and from the open to the close. <bookmark mark='a'/> Since 1993, almost all of the fund's return was earned "
            f"overnight: {100 * o['mean']:.1f} percent a year, against {100 * i['mean']:.1f} percent during trading hours, "
            "when nearly all the trading and all the news conferences happen. <bookmark mark='b'/> The overnight line "
            "also had the smaller volatility."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(l1), Create(l2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(st))
        self.wait(0.4)
        self.clear_scene()

    def night_why(self, c):
        cards = VGroup(
            desk_question(r"a tug of war", r"Lou, Polk and Skouras (2019): momentum profits accrue overnight, and most "
                          r"other anomalies' profits intraday, consistent with different clienteles trading at the open "
                          r"and through the day", width=12.4, font_size=19),
            desk_question(r"risk", r"news that breaks while markets are closed cannot be traded on: holding overnight may "
                          r"be paid for bearing the gap", width=12.4, font_size=19),
            desk_question(r"why it is not free money", r"buying at every close and selling at every open is two trades a "
                          r"day: at even a few basis points each, about 10\% a year of costs, and the opening auction is "
                          r"not the price a large order gets", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Explanations. <bookmark mark='a'/> Dong Lou, Christopher Polk and Spyros Skouras found that momentum's "
            "profits accrue overnight while most other anomalies earn intraday, as if different clienteles trade at the "
            "open and through the day. <bookmark mark='b'/> There may be a premium for bearing the overnight gap, when "
            "news cannot be traded on. <bookmark mark='c'/> And it is not free money: holding only the nights takes two "
            "trades a day, about five hundred a year, and at a few basis points each the cost swallows most of the "
            "return."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def events(self):
        cards = VGroup(
            desk_question(r"merger arbitrage", r"buy the target after a deal is announced, short the acquirer: Mitchell "
                          r"and Pulvino (2001) find returns like selling index puts, steady in calm and rising markets, "
                          r"correlated with the market in sharp declines, when deals break", width=12.4, font_size=19),
            desk_question(r"index changes", r"stocks added to an index are bought by every index fund on the same day: "
                          r"the inclusion effect, large in the 1990s and much smaller since, as traders positioned "
                          r"ahead of the announced date", width=12.4, font_size=19),
            desk_question(r"earnings drift", r"prices keep moving in the direction of an earnings surprise for weeks "
                          r"(Bernard and Thomas 1989): Part 28 read the same delay in text", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        head = label(r"Event-driven strategies: flows around corporate events", font_size=28).to_edge(UP, buff=0.4)
        if cards.height > 6.0:
            cards.scale_to_fit_height(6.0)
        cards.next_to(head, DOWN, buff=0.3)
        with self.voiceover(
            "Event-driven strategies harvest similar flows around corporate events. <bookmark mark='a'/> Merger "
            "arbitrage buys a takeover target after the deal is announced and earns the spread if it closes. Mark "
            "Mitchell and Todd Pulvino found that its returns look like selling index puts: steady in calm markets, and "
            "correlated with the market when it falls sharply, because that is when deals break. "
            "<bookmark mark='b'/> Index changes force every index fund to buy the same stock on the same day; the "
            "effect has shrunk as traders learned to position ahead of it. <bookmark mark='c'/> And prices drift after "
            "earnings surprises for weeks, a delay Part twenty-eight read in text."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def mining(self):
        rows = [cmath(r"\#\ \text{calendar rules}", r"\approx", r"\text{thousands}", font_size=36),
                cmath(r"p_{\text{best}}", r"\ll", r"p_{\text{corrected}}", font_size=36, colors={r"p_{\text{best}}": BAD}),
                cmath(r"\text{the turn of the month}", r":", r"\text{a reason, and a decline after publication}",
                      font_size=30, colors={r"\text{the turn of the month}": GOOD})]
        whys = [why(r"days of the week, of the month, holidays, half-months, seasons: Sullivan, Timmermann and White (2001) "
                    r"counted the rules a researcher could have tried"),
                why(r"judged by White's reality check (Part 26) against that universe, most calendar effects in the Dow "
                    r"were no longer significant"),
                why(r"the effects that deserve belief come with a mechanism, a predictable flow, which also predicts "
                    r"their decay")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.3, buff=0.55, edge=6.9)
        with self.voiceover(
            "A warning comes with all of these. <bookmark mark='a'/> There are thousands of calendar rules a researcher "
            "could try: days of the week, of the month, holidays, seasons. Ryan Sullivan, Allan Timmermann and Halbert "
            "White counted them. <bookmark mark='b'/> Judged against that universe with White's reality check from Part "
            "twenty-six, most calendar effects in a century of the Dow were no longer significant. "
            "<bookmark mark='c'/> The ones worth believing come with a mechanism, a predictable flow, and the mechanism "
            "also predicts their decline. The turn of the month has one; the pre-announcement drift has a candidate; "
            "the Halloween effect is still looking for one. The House treats the first as a premium, the second as a "
            "question, and the third as a trial."
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


    def halloween(self, c):
        h = c["halloween"]
        hx = [-3.6, -0.6, 2.0, 4.6]
        head = VGroup(label(r"years", font_size=18, color=GREY_B), label(r"November--April", font_size=18, color=GOOD),
                      label(r"May--October", font_size=18, color=BAD), label(r"$t$ of the gap", font_size=18,
                                                                              color=GREY_B))
        tab = VGroup(head)
        for k, r in h.items():
            tab.add(VGroup(label(k.replace("-", "--"), font_size=20), MathTex(rf"{100 * r['winter']:.1f}\%", font_size=26),
                           MathTex(rf"{100 * r['summer']:.1f}\%", font_size=26), MathTex(f"{r['t']:.1f}", font_size=26)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.6 - 0.85 * j, 0])
        foot = wrapped_label(r"the US market's monthly excess return, annualised, in the two halves of the year; Bouman and "
                             r"Jacobsen (2002) found the gap in 36 of 37 markets", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.6)
        a, b, cc = (h[k] for k in h)
        bw, bs, bt, ct = 100 * b["winter"], 100 * b["summer"], b["t"], cc["t"]
        with self.voiceover(
            "One more calendar effect, with an old proverb: sell in May and go away. <bookmark mark='a'/> Split each year "
            "into November to April and May to October. Before 1963 the halves were close. From 1963 to 1990 the winter "
            f"half earned {bw:.0f} percent a year and the summer half {bs:.0f}, a gap with a t-statistic of {bt:.1f}. "
            f"Since 1991 the gap is smaller and weaker, {ct:.1f}. Sven Bouman and Ben Jacobsen found it in thirty-six of "
            "thirty-seven markets. It has no agreed explanation, which is exactly why the warning of the next slide "
            "applies to it."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()


    def fomc(self, c):
        f = c["fomc"]
        bars = VGroup()
        mx = max(f["on"], f["off"])
        for j, (nm, v, col) in enumerate(((r"FOMC statement days", f["on"], GOOD), (r"all other days", f["off"], GREY_B))):
            r = Rectangle(width=8.0 * v / mx, height=0.6, fill_color=col, fill_opacity=0.85, stroke_width=0)
            r.move_to([-3.0, 0.9 - 1.3 * j, 0], aligned_edge=LEFT)
            bars.add(VGroup(label(nm, font_size=22, color=col).next_to(r, UP, buff=0.12).align_to(r, LEFT), r,
                            MathTex(rf"{v:.1f}\ \text{{bp}}", font_size=28).next_to(r, RIGHT, buff=0.2)))
        foot = wrapped_label(rf"the US market's average daily excess return, 1994--2020, on the {f['days']} days with an "
                             rf"FOMC statement (Part 28's archive) against the rest; $t$ = {f['t']:.1f}", 11.4, 17,
                             GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "A newer clock: the Federal Reserve's. <bookmark mark='a'/> On the "
            f"{f['days']} days since 1994 with a statement from the Federal Open Market Committee, the American market "
            f"earned {f['on']:.0f} basis points over bills on average, against {f['off']:.0f} on other days. "
            f"<bookmark mark='b'/> Fewer than three percent of the days, and {100 * f['share']:.0f} percent of the "
            "market's whole excess return. David Lucca and Emanuel Moench found that most of this drift arrives in the "
            "hours before the announcement, not after it, which no standard model of risk explains."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"an overnight strategy earns 10\% a year before costs and trades 504 times a year. At what cost "
                       r"per trade does it break even?")
        with self.voiceover(
            "Pause and predict. An overnight strategy earns ten percent a year before costs and trades five hundred and "
            "four times a year. At what cost per trade does it break even?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
