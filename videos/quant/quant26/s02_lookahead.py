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
            f"Plant a timing error deliberately in the moving-average rule. A position determined with today's close can earn only a return starting after that information is available. <bookmark mark='a'/> With the original lag convention, the two-hundred-day rule has Sharpe {a['ma200']['sr_honest']:.2f} during 1990 to 2020. Market buy-and-hold is {a['sr_bh']:.2f}. <bookmark mark='b'/> Letting that position earn the already-observed same-day return raises its ratio to {a['ma200']['sr_bug']:.2f}. <bookmark mark='c'/> The five-day version reaches {a['ma5']['sr_bug']:.2f}. This isolates a planted index error in a gross calculation; the lagged result is still not a fully implemented tradable strategy."
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
                if k:
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
            f"The public Philadelphia archive preserves revisions to 2008 quarter-four growth. <bookmark mark='a'/> In the first finite monthly vintage the annualised estimate is {ys[0]:.1f} percent. <bookmark mark='b'/> The saved path changes as later vintages arrive and ends at {ys[-1]:.1f} percent in December 2020. <bookmark mark='c'/> A monthly vintage is useful availability information, but it is not an exact release timestamp or a full intraday replay. The reader also accesses later published archive bytes before selecting its research window; that is separate from opening a sealed strategy experiment."
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
        g = axes([-12, 18], [-12, 18], x_length=4.6, y_length=4.6, xlabel=r"first published, \% a year",
                 ylabel=r"as of December 2020, \% a year", xticks=[-10, 0, 10], yticks=[-10, 0, 10],
                 font_size=13).to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        ax = g.ax
        diag = DashedLine(ax.c2p(-12, -12), ax.c2p(18, 18), color=GREY_C, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.035,
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
            f"The saved comparison contains {g_['n']} quarters from 1966 through 2019. <bookmark mark='a'/> First finite vintages and December 2020 estimates differ by an average absolute {g_['mean_abs_rev']:.2f} percentage points. {100*g_['sign_changes']:.1f} percent change sign; their correlation is {g_['corr']:.2f}. Revisions need not bias every strategy in the same direction. An available-time replay must use release dates, vintage definitions and realistic execution timing."
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
            f"A period date can be mistaken for an availability date. <bookmark mark='a'/> A quarter labelled October first was not fully known on that day. Merging revised quarterly data by the period can leak both later observations and revisions. <bookmark mark='b'/> In this original monthly-vintage illustration, the lagged-vintage timing ratio is {t['sr_realtime']:.2f}, versus {t['sr_naive']:.2f} for the naive period merge. It is not a timestamp-complete real-time trading replay. <bookmark mark='c'/> A plausible-looking difference can still come from unavailable information. Neither its small size nor a visually reasonable chart validates the protocol."
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
