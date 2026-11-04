from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant26.common import (BUG, HONEST, HURDLE, MKT, PART, RULE, ask, fit_right, illustration, load)


def _years(ym):
    ym = np.asarray(ym)
    return ym // 100 + (ym % 100 - 0.5) / 12


def _vyear(v):
    y, m = v.split("M")
    return int(y) + (int(m) - 0.5) / 12


class LookAhead(VoiceoverScene):
    def construct(self):
        a = load("lookahead")
        self.card()
        self.planted(a)
        self.ways()
        self.vintages(a["gdp"])
        self.scatter(a["gdp"])
        self.stamp(a["gdp"])
        self.question()

    def card(self):
        c = chapter_card(1, r"Look-ahead and point in time", r"What did the strategy know, and when?", lit=(2008,),
                         part=PART)
        with self.voiceover("Chapter one. Look-ahead: a backtest that knew something its trader could not have known."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def planted(self, a):
        m = a["ma200"]
        yr = _years(m["ym"])
        series = [np.log10(np.asarray(m[k])) for k in ("honest", "bug", "bh")]
        top = float(np.ceil(max(s.max() for s in series) * 2) / 2)
        g = axes([1990, 2021], [-0.3, top], x_length=7.6, y_length=4.2, xlabel=r"year",
                 ylabel=r"growth of \$1, $\log_{10}$", xticks=[1990, 2000, 2010, 2020],
                 yticks=[0, 0.5, 1.0, 1.5] if top >= 1.5 else [0, 0.5, 1.0], font_size=14).to_edge(LEFT, buff=0.45)
        g.shift(DOWN * 0.5)
        ax = g.ax
        lines = [curve(ax, yr, s, c, stroke_width=3 if c != MKT else 2) for s, c in zip(series, (HONEST, BUG, MKT))]
        code = VGroup(
            MathTex(r"\text{honest}:\ \ r^{\text{rule}}_{t+1} = s_t\, r_{t+1}", font_size=28, color=HONEST),
            MathTex(r"\text{planted}:\ \ r^{\text{rule}}_{t} = s_t\, r_{t}", font_size=28, color=BUG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(UP, buff=0.35).shift(RIGHT * 2.6)
        side = VGroup(
            MathTex(rf"\text{{honest}}:\ {m['sr_honest']:.2f}", font_size=28, color=HONEST),
            MathTex(rf"\text{{planted}}:\ {m['sr_bug']:.2f}", font_size=28, color=BUG),
            MathTex(rf"\text{{buy and hold}}:\ {a['sr_bh']:.2f}", font_size=24, color=MKT),
            wrapped_label(r"Sharpe ratios, 1990--2020. The rule: long when the market closes above its 200-day "
                          r"average, short below. $s_t$ uses today's close; the planted line lets it earn today's "
                          r"return too", 3.5, 15, GREY_A),
            MathTex(rf"\text{{5-day average, planted}}:\ {a['ma5']['sr_bug']:.1f}", font_size=22, color=BUG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.5)
        fit_right(side)
        with self.voiceover(
            "Start with the error itself, planted on purpose. The rule: be long the market when it closes above its "
            "two-hundred-day average, short when it closes below. The position s t is decided at today's close, so "
            "it can only earn tomorrow's return. <bookmark mark='a'/> Done honestly, from 1990 to 2020, its Sharpe "
            "ratio was a modest two tenths, below simply holding the market. <bookmark mark='b'/> Now change one index: "
            "let the position earn today's return, the very return whose close decided it. The Sharpe ratio jumps to "
            "one point three, two and a half times the market's. <bookmark mark='c'/> With a five-day average the same "
            "slip manufactures a Sharpe ratio near nine. One subscript. The code runs, the chart is beautiful, and "
            "nothing about it says it is wrong; only the size of the number might."
        ) as vo:
            self.play(FadeIn(g), FadeIn(code[0]))
            vo.wait_until("a")
            self.play(Create(lines[2]), Create(lines[0]), FadeIn(side[0]), FadeIn(side[2]), FadeIn(side[3]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(code[1]), Create(lines[1]), FadeIn(side[1]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
        self.add(illustration(r"Ken French's daily market factor; the House's \texttt{RuleEngine}"))
        self.wait(0.4)
        self.clear_scene()

    def ways(self):
        cards = VGroup(
            desk_question(r"the same bar", r"a signal from today's close earns today's return; or it trades at the "
                          r"close it was computed from, which a real order reaches only approximately", width=12.2,
                          font_size=19),
            desk_question(r"the period, not the release", r"earnings for the year to December are filed in February or "
                          r"March; GDP for a quarter appears a month after it ends. Stamped by period, they arrive early",
                          width=12.2, font_size=19),
            desk_question(r"the revision", r"today's database holds today's best estimate of the past, not what anyone "
                          r"saw at the time: GDP, earnings restatements, index weights", width=12.2, font_size=19),
            desk_question(r"the whole sample", r"a z-score scaled by the full sample's mean, a parameter fitted on all of "
                          r"it, a universe chosen by what exists at the end: each leaks the future into every date",
                          width=12.2, font_size=19),
        ).arrange(DOWN, buff=0.2)
        if cards.height > 7.0:
            cards.scale_to_fit_height(7.0)
        with self.voiceover(
            "Look-ahead enters in four common ways. <bookmark mark='a'/> The same bar: the bug we just planted, or its "
            "milder cousin, trading at the very close a signal was computed from, which a real order can only "
            "approximate. <bookmark mark='b'/> The period instead of the release: a company's earnings for the year "
            "to December are filed in February or March; a quarter's GDP appears a month after the quarter ends. A "
            "database that stamps them by period hands them to the backtest early. <bookmark mark='c'/> The revision: "
            "today's database holds today's best estimate of the past, which is not what anyone saw at the time. "
            "<bookmark mark='d'/> And the whole sample: a z-score scaled by the full sample's mean, a parameter fitted "
            "on all the data, a universe chosen by what exists at the end. Each quietly leaks the future into every "
            "date."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c", "d")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def vintages(self, g_):
        p = g_["q08"]
        xs = np.array([_vyear(v) for v in p["vintage"]])
        ys = np.asarray(p["growth"])
        g = axes([2009, 2021], [-10, 0], x_length=8.0, y_length=4.2, xlabel=r"vintage: the month the estimate was "
                 r"published", ylabel=r"US real GDP growth in 2008 Q4, \% a year", xticks=[2009, 2011, 2013, 2015, 2017,
                                                                                         2019, 2021],
                 yticks=[-10, -8, -6, -4, -2, 0], font_size=14).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        ax = g.ax
        line = VMobject(color=RULE, stroke_width=3).set_points_as_corners(
            [ax.c2p(x, y) for x, y in zip(*_steps(xs, ys))])
        first = Dot(ax.c2p(xs[0], ys[0]), color=HURDLE, radius=0.07)
        j11 = int(np.argmin(ys))
        lo = Dot(ax.c2p(xs[j11], ys[j11]), color=BUG, radius=0.07)
        side = VGroup(
            MathTex(rf"\text{{first estimate, Jan 2009}}:\ {ys[0]:.1f}\%", font_size=26, color=HURDLE),
            MathTex(rf"\text{{lowest, {_month(p['vintage'][j11])}}}:\ {ys[j11]:.1f}\%", font_size=24, color=BUG),
            MathTex(rf"\text{{as of Dec 2020}}:\ {ys[-1]:.1f}\%", font_size=26, color=RULE),
            wrapped_label(r"the same quarter, re-estimated as late tax and survey data arrived, and again at each "
                          r"benchmark revision. A backtest that reads today's number in February 2009 knew the recession "
                          r"was more than twice as deep as anyone did", 3.6, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.3)
        fit_right(side)
        with self.voiceover(
            "Here is a revision you can see. The last quarter of 2008, the worst of the financial crisis. <bookmark "
            "mark='a'/> At the end of January 2009 the government's first estimate said the American economy had "
            "shrunk at an annual rate of three point eight percent. <bookmark mark='b'/> A month later it said six "
            "point two. In the annual revision of July 2011 it said almost nine. In the December 2020 vintage it is eight "
            "point four. <bookmark mark='c'/> A backtest that reads today's database in February 2009 knows the "
            "recession was more than twice as deep as anyone knew at the time. Every monthly vintage is kept by the "
            "Federal Reserve Bank of Philadelphia, precisely so that research can ask what was known when."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(first), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(lo), FadeIn(side[1]), FadeIn(side[2]), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.add(illustration(r"Federal Reserve Bank of Philadelphia, Real-Time Data Set for Macroeconomists (ROUTPUT)"))
        self.wait(0.4)
        self.clear_scene()

    def scatter(self, g_):
        f, z = np.asarray(g_["first"]), np.asarray(g_["final"])
        g = axes([-10, 10], [-10, 10], x_length=4.6, y_length=4.6, xlabel=r"first published, \% a year",
                 ylabel=r"as of December 2020, \% a year", xticks=[-10, -5, 0, 5, 10], yticks=[-10, -5, 0, 5, 10],
                 font_size=13).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        ax = g.ax
        diag = DashedLine(ax.c2p(-10, -10), ax.c2p(10, 10), color=GREY_C, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(np.clip(a, -10, 10), np.clip(b, -10, 10)), radius=0.035,
                            color=BUG if np.sign(a) != np.sign(b) else RULE, fill_opacity=0.8) for a, b in zip(f, z)])
        side = VGroup(
            MathTex(rf"{g_['n']}\ \text{{quarters, 1966--2019}}", font_size=26),
            MathTex(rf"\text{{mean revision}}:\ {g_['mean_abs_rev']:.1f}\ \text{{points}}", font_size=26, color=RULE),
            MathTex(rf"\text{{sign changed}}:\ {100 * g_['sign_changes']:.0f}\%", font_size=26, color=BUG),
            MathTex(rf"\text{{correlation}}:\ {g_['corr']:.2f}", font_size=24, color=GREY_A),
            wrapped_label(r"each quarter's growth as first published against the same quarter in the December 2020 "
                          r"vintage. Red: a quarter that was first reported as growth and later as contraction, or the "
                          r"reverse", 4.4, 15, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "Every quarter since 1966, first estimate against the 2020 vintage. <bookmark mark='a'/> On average a "
            "quarter's growth rate was revised by one and a half percentage points, more than half of a typical "
            "quarter's growth. One quarter in fourteen changed sign: reported as growth, later as contraction, or the "
            "reverse. The correlation between what was known and what is now believed is only about eight tenths. A "
            "signal built from macro data must be built from the vintages."
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.005, run_time=2.5),
                      FadeIn(side[1:]))
        self.add(illustration(r"Philadelphia Fed real-time data: first release against the 2020M12 vintage"))
        self.wait(0.4)
        self.clear_scene()

    def stamp(self, g_):
        t = g_["timing"]
        rows = VGroup(
            cmath(r"\text{real time}", r":", r"\ \text{the latest GDP published by month } m", font_size=30,
                  colors={r"\text{real time}": HONEST}),
            cmath(r"\text{naive}", r":", r"\ \text{the 2020 vintage, merged on FRED's date stamp}", font_size=30,
                  colors={r"\text{naive}": BUG}),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(UP, buff=0.7)
        sub = wrapped_label(r"FRED dates a quarter by its first day: 2008 Q4 is stamped 1 October 2008. Merged 'as of' "
                            r"the end of October, it hands the backtest the whole quarter, revised, three months before the "
                            r"first estimate existed", 12.0, 19, GREY_A).next_to(rows, DOWN, buff=0.35)
        bars = [(r"real time", t["sr_realtime"], HONEST), (r"naive", t["sr_naive"], BUG), (r"buy and hold", t["sr_bh"], MKT)]
        g = VGroup()
        for i, (nm, v, c) in enumerate(bars):
            b = Rectangle(width=v * 9.0, height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.85)
            b.move_to([-3.0 + v * 4.5, -1.2 - 0.7 * i, 0])
            g.add(VGroup(label(nm, font_size=20, color=c).next_to([-3.1, -1.2 - 0.7 * i, 0], LEFT, buff=0.15), b,
                         MathTex(f"{v:.2f}", font_size=24).next_to(b, RIGHT, buff=0.15)))
        foot = wrapped_label(rf"in the market next month only if the latest quarter grew; Sharpe ratios, "
                             rf"{t['first'] // 100}--{t['last'] // 100}. The two disagree in "
                             rf"{100 * t['disagree']:.0f}\% of months", 12.0, 17, GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "How does this reach a backtest? Usually through a date. <bookmark mark='a'/> FRED, the most used "
            "economic database, dates each quarter by its first day: the last quarter of 2008 is stamped the first of "
            "October 2008. Merge it as of the end of October and the backtest has the whole quarter, revised, three "
            "months before the first estimate existed. <bookmark mark='b'/> A rule that stays in the market only "
            "while the latest quarter grew earns a Sharpe ratio of point three eight in real time, and point four "
            "three with the naive merge, nudged above buy and hold. <bookmark mark='c'/> Notice how small that is. "
            "Not a Sharpe of nine: a few hundredths, the size of an honest improvement. That is the dangerous kind of "
            "bias, the kind nobody looks for, because the result is believable."
        ) as vo:
            self.play(FadeIn(rows))
            vo.wait_until("a")
            self.play(FadeIn(sub))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.2) for b_ in g], lag_ratio=0.4), FadeIn(foot))
            vo.wait_until("c")
            self.play(Indicate(g[1], color=BUG, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a backtest computes each stock's 'value' signal from book equity divided by price, using a database "
                r"of annual reports keyed by fiscal year end. What would you change, and which way is the bias?")
        with self.voiceover(
            "Pause and predict. A value signal divides each company's book equity by its price, from a database of "
            "annual reports keyed by fiscal year end. What would you change, and in which direction does the bias run?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()


def _month(v):
    y, m = v.split("M")
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][int(m) - 1] + f" {y}"


def _steps(xs, ys):
    """A step line through (xs, ys): each value held until the next."""
    X, Y = [], []
    for k in range(len(xs)):
        X += [xs[k], xs[k + 1] if k + 1 < len(xs) else xs[k] + 1 / 12]
        Y += [ys[k], ys[k]]
    return np.array(X), np.array(Y)
