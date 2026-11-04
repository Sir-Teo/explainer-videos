from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import backtest as BT
from videos.quant.quant26.common import (BAD, BUG, COST, ENGINE, GOOD, HONEST, MKT, PART, RULE, ask, comma, fit_right,
                                         house_lab, illustration, load)


def _years(ym):
    ym = np.asarray(ym)
    return ym // 100 + (ym % 100 - 0.5) / 12


def _d2y(d):
    d = np.asarray(d)
    return d // 10000 + ((d // 100) % 100 - 1) / 12 + (d % 100) / 365


class Engine(VoiceoverScene):
    def construct(self):
        e = load("engine")
        self.card()
        self.loop()
        self.vector()
        self.race(e)
        self.overnight(e)
        self.costs(e)
        self.split(e["split"])
        self.dividends(e["div"])
        self.borrow()
        self.lab()
        self.question()

    def card(self):
        c = chapter_card(4, r"The event-driven backtester", r"What would a broker actually have filled?", lit=(2010,),
                         part=PART)
        with self.voiceover("Chapter four. The backtester itself: a machine that replays history one event at a time "
                            "and fills orders as a broker would."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def loop(self):
        steps = [(r"bar $t$ arrives", r"open, high, low, close, volume"),
                 (r"corporate actions", r"splits change the share count; dividends pay longs, charge shorts"),
                 (r"fills", r"orders due now, at the open or close, less spread, impact, commission"),
                 (r"mark and borrow", r"value the book at the close; charge borrow on shorts"),
                 (r"the strategy", r"sees bars $0, \dots, t$ only, returns a target"),
                 (r"orders", r"the difference, due at $t + L$ (latency)")]
        n = len(steps)
        R = 2.55
        boxes = VGroup()
        for k, (a, b) in enumerate(steps):
            ang = PI / 2 - 2 * PI * k / n
            c = np.array([R * 1.55 * np.cos(ang), R * np.sin(ang) - 0.2, 0])
            box = RoundedRectangle(width=3.6, height=1.05, corner_radius=0.12, stroke_color=ENGINE, stroke_width=2,
                                   fill_color="#141a26", fill_opacity=1).move_to(c)
            t1 = label(a, font_size=20, color=ENGINE)
            t2 = wrapped_label(b, 3.3, 13, GREY_A)
            txt = VGroup(t1, t2).arrange(DOWN, buff=0.06).move_to(box)
            if txt.width > 3.4:
                txt.scale_to_fit_width(3.4)
            boxes.add(VGroup(box, txt))
        arrows = VGroup(*[CurvedArrow(boxes[k][0].get_center() * 0.62 + boxes[(k + 1) % n][0].get_center() * 0.38,
                                      boxes[(k + 1) % n][0].get_center() * 0.62 + boxes[k][0].get_center() * 0.38,
                                      angle=-0.35, color=GREY_C, stroke_width=2, tip_length=0.15) for k in range(n)])
        centre = VGroup(label(r"one loop per bar", font_size=22, color=WHITE),
                        label(r"the future is never handed over", font_size=16, color=GREY_B)).arrange(DOWN, buff=0.1).move_to(
            DOWN * 0.2)
        token = Dot(boxes[0][0].get_center(), color=HONEST, radius=0.1)
        with self.voiceover(
            "An event-driven backtester is a loop, run once for every bar of history. <bookmark mark='a'/> A bar "
            "arrives: the day's open, high, low, close and volume. First the corporate actions: a split changes the "
            "share count, a dividend pays the longs and charges the shorts. Then the fills: orders that are due now "
            "execute at the open or the close, paying half the spread, a price impact that grows with the order's size, "
            "and a commission. Then the book is marked at the close, and short positions pay their borrow fee. "
            "<bookmark mark='b'/> Only then is the strategy called, and it is handed the bars up to this one and no "
            "further. It returns a target position; the difference becomes an order, due after a latency. "
            "<bookmark mark='c'/> The point of the design is not speed. It is that the future is never handed to the "
            "strategy, so it cannot use it, however the code is written."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.15), FadeIn(centre))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a_) for a_ in arrows], lag_ratio=0.15), FadeIn(token))
            for k in range(1, 4):
                self.play(token.animate.move_to(boxes[k][0].get_center()), run_time=0.9)
            vo.wait_until("b")
            for k in (4, 5, 0):
                self.play(token.animate.move_to(boxes[k][0].get_center()), run_time=0.9)
            vo.wait_until("c")
            self.play(Indicate(boxes[4], color=HONEST, scale_factor=1.04), Indicate(centre[1], color=HONEST))
        self.wait(0.4)
        self.clear_scene()

    def vector(self):
        rows = [cmath(r"r^{\text{vec}}_{t+1}", r"=", r"w_t\, r_{t+1} - c\,|w_t - w_{t-1}|", font_size=38,
                      colors={r"r^{\text{vec}}_{t+1}": RULE}),
                cmath(r"\text{assumes}", r":", r"\ \text{fill at } C_t,\ \text{no latency, fixed cost, no corporate actions}",
                      font_size=32, colors={r"\text{assumes}": BUG}),
                cmath(r"\text{gains}", r":", r"\ \text{one line, a thousand times faster; right when the assumptions are}",
                      font_size=32, colors={r"\text{gains}": GOOD})]
        whys = [why(r"the vectorised backtest: a weight decided at today's close earns the next close-to-close return, "
                    r"less a cost on each change of weight"),
                why(r"it trades at the very close it computed the signal from, instantly, at a cost that does not depend "
                    r"on size or volatility, in prices already adjusted for splits and dividends"),
                why(r"so the House uses it to search, and the event-driven engine to decide: a strategy is judged on the "
                    r"engine's numbers")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.5, buff=0.45, edge=6.9)
        with self.voiceover(
            "The alternative is a single line of array arithmetic. <bookmark mark='a'/> The weight decided at today's "
            "close earns the next close-to-close return, less a cost on each change. <bookmark mark='b'/> It assumes a "
            "great deal: a fill at the very close the signal came from, with no latency, at a cost that does not depend "
            "on size or volatility, in prices someone has already adjusted for splits and dividends. <bookmark "
            "mark='c'/> It is also a thousand times faster, and right whenever its assumptions are. So the House "
            "searches with the vectorised backtest, and decides with the event-driven one."
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

    def race(self, e):
        v, R = e["vector"], e["runs"]
        series = [(r"vectorised, close to close", v["ym"], v["eq"], v["sr"], RULE),
                  (r"engine, filled at that close", R["close_now"]["ym"], R["close_now"]["eq"], R["close_now"]["sr"], ENGINE),
                  (r"engine, next open", R["open_next"]["ym"], R["open_next"]["eq"], R["open_next"]["sr"], MKT),
                  (r"next open, 1 bp half-spread", R["spread"]["ym"], R["spread"]["eq"], R["spread"]["sr"], BUG),
                  (r"next open, all costs", R["all"]["ym"], R["all"]["eq"], R["all"]["sr"], COST)]
        ys = [np.log10(np.asarray(s[2])) for s in series]
        lo, hi = float(np.floor(min(y.min() for y in ys) * 4) / 4), float(np.ceil(max(y.max() for y in ys) * 4) / 4)
        g = axes([2010, 2021], [lo, hi], x_length=7.4, y_length=4.2, xlabel=r"year",
                 ylabel=r"growth of \$1, $\log_{10}$", xticks=[2010, 2013, 2016, 2019],
                 yticks=[t for t in (-1, -0.5, 0, 0.5, 1) if lo <= t <= hi], font_size=14).to_edge(LEFT, buff=0.45)
        g.shift(DOWN * 0.3)
        ax = g.ax
        lines = [curve(ax, _years(s[1]), y, s[4], stroke_width=3 if k < 2 else 2.5) for k, (s, y) in
                 enumerate(zip(series, ys))]
        tags = VGroup(*[VGroup(Line(ORIGIN, RIGHT * 0.35, color=s[4], stroke_width=5),
                               label(s[0], font_size=15, color=s[4]),
                               MathTex(f"{s[3]:+.2f}", font_size=22, color=s[4])).arrange(RIGHT, buff=0.15)
                        for s in series]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        side = VGroup(label(r"Sharpe ratio", font_size=18, color=GREY_A), tags,
                      wrapped_label(r"EEM, the emerging-markets ETF, 2010--2020: short after an up day, long after a "
                                    r"down day. Costs: 1 bp half-spread, square-root impact, \$0.005 a share, 30 bp a "
                                    r"year to borrow", 3.7, 14, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(
            RIGHT, buff=0.25)
        fit_right(side, 6.85)
        with self.voiceover(
            "Watch the two disagree. The strategy is a one-day reversal on EEM, the emerging-markets exchange-traded "
            "fund: short after an up day, long after a down day. <bookmark mark='a'/> The vectorised backtest gives it a "
            "Sharpe ratio of point four three from 2010 to 2020. <bookmark mark='b'/> The engine, told to fill at the "
            "very close the signal came from, agrees: point four five. The machinery is right; the difference is in the "
            "assumptions. <bookmark mark='c'/> Now fill at the next morning's open, which is what an order placed after "
            "the close would get. The Sharpe ratio becomes minus point one eight. <bookmark mark='d'/> Add one basis "
            "point of half-spread: minus point three. Add impact, commissions and borrow: minus half. A strategy that "
            "looked like a modest edge is a way to lose more than ten percent a year."
        ) as vo:
            self.play(FadeIn(g), FadeIn(side[0]), FadeIn(side[2]))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(tags[0]), run_time=2)
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(tags[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(tags[2]), run_time=2)
            vo.wait_until("d")
            self.play(Create(lines[3]), FadeIn(tags[3]), Create(lines[4]), FadeIn(tags[4]), run_time=2.5)
        self.add(illustration(r"Yahoo Finance daily bars and dividends; the House's \texttt{backtest.Backtester}"))
        self.wait(0.4)
        self.clear_scene()

    def overnight(self, e):
        v = e["vector"]
        rows = [cmath(r"\frac{C_{t+1}}{C_t}", r"=", r"\underbrace{\frac{O_{t+1}}{C_t}}_{\text{overnight}}\;"
                      r"\underbrace{\frac{C_{t+1}}{O_{t+1}}}_{\text{the day}}", font_size=40,
                      colors={r"\frac{C_{t+1}}{C_t}": RULE})]
        rows[0].to_edge(UP, buff=0.7)
        bars = [(r"the whole return", v["sr"], RULE), (r"overnight only", v["sr_overnight"], HONEST),
                (r"the day only", v["sr_intraday"], BUG)]
        g = VGroup()
        for i, (nm, val, c) in enumerate(bars):
            b = Rectangle(width=abs(val) * 5.0, height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([val * 2.5, -0.5 - 0.75 * i, 0])
            g.add(VGroup(label(nm, font_size=20, color=c).move_to([-4.6, -0.5 - 0.75 * i, 0]), b,
                         MathTex(f"{val:+.2f}", font_size=24).next_to(b, RIGHT if val > 0 else LEFT, buff=0.15)))
        axis = Line([0, 0.0, 0], [0, -2.4, 0], color=GREY_C, stroke_width=1.5)
        foot = wrapped_label(r"the reversal's Sharpe ratio from each piece of the next day's return. EEM holds stocks that "
                             r"trade in Asian and Latin American hours; New York's close and the next open straddle their "
                             r"sessions. The edge sits in the gap that an order placed after the close cannot reach",
                             12.2, 18, GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where did the edge go? Split each day's return into two pieces: from the close to the next open, "
            "overnight, and from the open to the close. <bookmark mark='a'/> The reversal's whole edge is overnight, "
            "with a Sharpe ratio near point eight, and during the day it loses. EEM holds stocks that trade in Asian "
            "and Latin American hours, so New York's close and the next open straddle their sessions. The reversal is "
            "real, but it lives in a gap that an order placed after the close cannot reach. A vectorised backtest "
            "never asks."
        ) as vo:
            self.play(FadeIn(rows[0]), Create(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in g], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def costs(self, e):
        c = e["runs"]["all"]["costs"]
        items = [(r"spread", c["spread"]), (r"impact", c["impact"]), (r"commission", c["commission"]),
                 (r"borrow", c["borrow"])]
        tot = sum(v for _, v in items)
        g = VGroup()
        for i, (nm, v) in enumerate(items):
            b = Rectangle(width=v / tot * 8.0, height=0.5, stroke_width=0, fill_color=COST,
                          fill_opacity=0.45 + 0.12 * i)
            b.move_to([-3.6 + v / tot * 4.0, 1.2 - 0.8 * i, 0])
            g.add(VGroup(label(nm, font_size=21, color=COST).next_to([-3.7, 1.2 - 0.8 * i, 0], LEFT, buff=0.2), b,
                         MathTex(rf"\${comma(v)}", font_size=24).next_to(b, RIGHT, buff=0.15)))
        head = label(r"what \$1 million paid to trade the reversal, 2010--2020", font_size=28).to_edge(UP, buff=0.5)
        foot = wrapped_label(rf"{comma(e['runs']['all']['trades'])} trades, turning the book over about "
                             rf"{e['turnover']:.0f} times a year. At that pace a cost of one basis point a trade is about "
                             r"2.5\% a year: a high-turnover strategy is a bet that its edge per trade beats its cost per "
                             r"trade", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "What the costs were. <bookmark mark='a'/> Over eleven years a million dollars paid about a hundred and "
            "thirty thousand in spread, nearly forty thousand in impact, a hundred and sixty thousand in commissions at half "
            "a cent a share, and a little borrow. <bookmark mark='b'/> The strategy turns its book over more than two "
            "hundred and fifty times a year. At that pace one basis point a trade is two and a half percent a year. "
            "Every high-turnover strategy is a bet that its edge per trade beats its cost per trade, and the "
            "vectorised backtest, with its one fixed cost, cannot tell you whether it does."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in g], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def split(self, s):
        x = _d2y(s["date"])
        raw, adj = np.asarray(s["raw"]), np.asarray(s["adj"])
        g = axes([2019.9, 2021.0], [0, 520], x_length=6.0, y_length=3.6, xlabel=r"2020",
                 ylabel=r"AAPL, dollars a share", xticks=[], yticks=[0, 100, 200, 300, 400, 500], font_size=13).to_edge(
            LEFT, buff=0.5).shift(DOWN * 0.2)
        ax = g.ax
        l_raw = curve(ax, x, raw, BUG, stroke_width=2.5)
        l_adj = curve(ax, x, adj, HONEST, stroke_width=2.5)
        k = s["k"]
        mark = Dot(ax.c2p(x[k], raw[k]), color=BUG, radius=0.07)
        g2 = axes([2019.9, 2021.0], [0, 2.2], x_length=5.0, y_length=3.6, xlabel=r"2020",
                  ylabel=r"a holder's \$1, by the engine", xticks=[], yticks=[0, 1, 2], font_size=13).to_edge(
            RIGHT, buff=0.5).shift(DOWN * 0.2)
        ax2 = g2.ax
        ok, bad = np.asarray(s["ok"]), np.asarray(s["bad"])
        l_ok, l_bad = curve(ax2, x, ok, HONEST, stroke_width=2.5), curve(ax2, x, bad, BUG, stroke_width=2.5)
        leg = legend([(BUG, r"as traded, split ignored"), (HONEST, r"adjusted, or the split applied")], font_size=15).to_edge(
            UP, buff=0.35)
        foot = wrapped_label(rf"Apple split 4 for 1 on 31 August 2020: the price fell from about \$500 to \$125 and every "
                             rf"holder got four shares for one. A file of prices as traded shows a {100 * s['fake_return']:.0f}\% "
                             rf"day; a 20-day momentum signal read from it is wrong for {s['mom_raw_flat_days']} days",
                             12.4, 17, GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Corporate actions are the next trap. <bookmark mark='a'/> On the thirty-first of August 2020 Apple split "
            "its stock four for one. The price fell from about five hundred dollars to a hundred and twenty-five, and "
            "every holder got four shares for each one. In a file of prices as traded, that is a seventy-four percent "
            "crash. <bookmark mark='b'/> An engine that applies the split keeps the holder whole. One that ignores it "
            "books a loss of three quarters overnight, and a momentum signal read from those prices turns bearish on "
            "Apple for ten days. The fix is either prices adjusted backwards for every split, or an engine that applies "
            "each action on its date, and never a mixture of the two."
        ) as vo:
            self.play(FadeIn(g), FadeIn(g2), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(l_raw), Create(l_adj), FadeIn(mark), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(l_ok), Create(l_bad), FadeIn(foot), run_time=2.5)
        self.add(illustration(r"Yahoo Finance, split-adjusted bars un-adjusted before 2020-08-31", corner=UR))
        self.wait(0.4)
        self.clear_scene()

    def dividends(self, d):
        rows = VGroup(
            MathTex(rf"\text{{SPY, price only}}:\ {100 * d['price_cagr']:.1f}\%\ \text{{a year}}", font_size=34, color=BUG),
            MathTex(rf"\text{{SPY, with dividends}}:\ {100 * d['total_cagr']:.1f}\%\ \text{{a year}}", font_size=34,
                    color=HONEST),
            MathTex(rf"\text{{{d['n_div']} quarterly dividends}},\ \${d['dividends']:.2f}\ \text{{a share}}", font_size=28,
                    color=GREY_A),
        ).arrange(DOWN, buff=0.35).shift(UP * 0.6)
        foot = wrapped_label(r"2010--2020. A backtest on price alone loses two points a year from a buy-and-hold "
                             r"benchmark, and misstates any strategy that is long or short around ex-dividend dates: a short "
                             r"pays the dividend, a long receives it", 12.0, 20, GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Dividends are quieter. <bookmark mark='a'/> The S and P five hundred fund SPY returned eleven and a half "
            "percent a year in price from 2010 to 2020, and thirteen point seven with its forty-four quarterly "
            "dividends. A backtest on prices alone loses two points a year from its benchmark, and misstates any "
            "strategy that is short across an ex-dividend date, because the short pays the dividend."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.2) for r_ in rows], lag_ratio=0.4), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def borrow(self):
        cards = VGroup(
            desk_question(r"borrow", r"a short sale borrows the stock and pays a fee: a few tenths of a percent a year "
                          r"for most large stocks, and for crowded, hard-to-borrow ones many percent, or none to be had "
                          r"at all", width=12.2, font_size=19),
            desk_question(r"fills", r"a limit order fills only if the market trades through it, and then mostly when you "
                          r"would rather it had not; a backtest that fills every limit order touched is selling itself "
                          r"options for free", width=12.2, font_size=19),
            desk_question(r"capacity", r"impact grows with size: a strategy that works with \$1 million may not with "
                          r"\$1 billion, and the engine's impact model is where that is learned", width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "Three more things the engine models and the vectorised line does not. <bookmark mark='a'/> Borrow: a "
            "short sale borrows the stock and pays a fee, a few tenths of a percent a year for most large companies, "
            "many percent for crowded ones, and sometimes there is none to borrow. <bookmark mark='b'/> Fills: a limit "
            "order fills only if the market trades through it, and mostly when you would rather it had not. A backtest "
            "that fills every limit order it touches is giving itself options for free. <bookmark mark='c'/> And "
            "capacity: impact grows with size, so a strategy that works with a million dollars may not work with a "
            "billion. Parts thirty-five to thirty-seven build these models properly."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def lab(self):
        card = house_lab(r"The loop, in the House", BT.Backtester.run, "# 1. corporate actions", 12,
                         extra=((BT.Backtester.run, "# 4. the strategy sees", 4),), width=10.6)
        card.move_to(ORIGIN)
        if card.height > 7.2:
            card.scale_to_fit_height(7.2)
        with self.voiceover(
            "Here is the loop as the House wrote it. Corporate actions first, then the fills that are due, then the "
            "mark and the borrow. And the line that matters most: the strategy is handed a view of the bars up to and "
            "including t, a slice that ends today. There is no index it could mistype to reach tomorrow, because "
            "tomorrow is not in what it was given."
        ):
            self.play(FadeIn(card))
            self.wait(1.5)
        self.clear_scene()

    def question(self):
        q = ask(r"a strategy trades 200 times a year with an average gross profit of 4 basis points a trade. Your "
                r"cost estimate is 3 basis points. How confident must you be in that estimate before trading it?")
        with self.voiceover(
            "Pause and predict. A strategy trades two hundred times a year and makes four basis points a trade before "
            "costs. Your estimate of its costs is three. How confident must you be in that three before you trade it?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
