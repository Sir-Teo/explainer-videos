from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant32.common import (BAD, BOND_C, GOOD, HURDLE, OOS_C, PART, RP_C, SIXTY_C, SPY_C, TREND_C, comma,
                                         fit_right, load)

BCOL = {"trend": TREND_C, "rp": RP_C, "spy": SPY_C, "6040": SIXTY_C}
BNAME = {"trend": r"trend book", "rp": r"risk parity", "spy": r"US stocks", "6040": r"60/40"}
GCOL = {"equities": QC.SPOT, "bonds": QC.DELTA, "credit": QC.OPTION, "commodities": QC.P, "currencies": QC.REALIZED}


class Envelope(VoiceoverScene):
    def construct(self):
        e = load("envelope")
        self.card()
        self.register(e)
        self.opened(e)
        self.table(e)
        self.y2022(e)
        self.by_class(e)
        self.flip(e)
        self.reading(e)
        self.blend(e)
        self.next_steps()
        self.question()

    def card(self):
        c = chapter_card(9, r"The trend and risk-parity books, registered and opened", r"Did the macro books do in "
                         r"2021--25 what they are sold to do?", part=PART)
        with self.voiceover("Chapter nine. Two books from this part, registered before the envelope was opened, and "
                            "judged once on 2021 to 2025: years that included the worst bond market in a generation."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def register(self, e):
        nt, nr = e["n_trials"]["trend"], e["n_trials"]["rp"]
        cards = VGroup(
            firm_card(r"The trend book", r"23 ETFs; long or short each on the sign of its past 252 days' excess return; "
                      r"40\% volatility per position, the book at 10\%; monthly", numbers=((rf"{nt}", r"trials: the "
                                                                                             r"lookbacks and sizings of "
                                                                                             r"Chapter 1"),),
                      kind=r"Registered", width=6.2, font_size=20),
            firm_card(r"The risk-parity book", r"10 ETFs in four classes; inverse volatility within a class, equal risk "
                      r"across, levered to 10\% on the trailing year, capped at 4; monthly",
                      numbers=((rf"{nr}", r"trials: risk parity and its 60/40 comparison"),), kind=r"Registered",
                      width=6.2, font_size=20),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 0.4)
        n_now = int(e["trials"])
        ctr = MathTex(rf"\text{{the counter}}:\ {comma(n_now - nt - nr)}\ \to\ {comma(n_now)}", font_size=30,
                      color=QC.HOUSE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The registrations. <bookmark mark='a'/> The trend book exactly as Chapter one built it, charged with the "
            f"{nt} lookbacks and sizings compared. The risk-parity book of Chapter four, charged with {nr}. Both before "
            f"costs, over Treasury bills. <bookmark mark='b'/> The counter moves to {n_now:,}."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cards))
            vo.wait_until("b")
            self.play(FadeIn(ctr))
        self.wait(0.4)
        self.clear_scene()

    def opened(self, e):
        b = e["books"]
        md = np.asarray(b["trend"]["hold_months"], float)
        x = md // 100 + ((md % 100) - 0.5) / 12
        ys = {k: 100 * np.asarray(b[k]["cum_hold"], float) for k in ("spy", "6040", "rp", "trend")}
        lo = float(np.floor(min(y.min() for y in ys.values()) / 10) * 10)
        hi = float(np.ceil(max(y.max() for y in ys.values()) / 10) * 10)
        g = axes([x[0], x[-1]], [lo, hi], x_length=7.4, y_length=4.4, xlabel=r"2021--2025, sealed until now",
                 ylabel=r"cumulative excess return, \%", xticks=[2021, 2023, 2025], yticks=[lo, 0, hi],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15).move_to(LEFT * 1.8 + DOWN * 0.2)
        ax = g.ax
        band = Rectangle(width=ax.c2p(2023, 0)[0] - ax.c2p(2022, 0)[0], height=4.4, fill_color=BAD, fill_opacity=0.12,
                         stroke_width=0).move_to(ax.c2p(2022.5, (lo + hi) / 2))
        lines = VGroup(*[curve(ax, x, ys[k], BCOL[k], stroke_width=3) for k in ys])
        leg = legend([(BCOL[k], BNAME[k]) for k in ("trend", "rp", "6040", "spy")], font_size=16).to_edge(RIGHT, buff=0.4)
        leg.shift(UP * 1.6)
        fit_right(leg)
        with self.voiceover(
            "The envelope. <bookmark mark='a'/> Five years: the boom of 2021; 2022, shaded, when inflation reached its "
            "highest in forty years and the Federal Reserve raised rates faster than at any time since the early 1980s; "
            "and the recovery after. <bookmark mark='b'/> Stocks finished far ahead. The trend book rose in 2022 while "
            "everything else fell. Risk parity fell furthest of all in 2022, and never recovered its research-years pace."
        ) as vo:
            self.play(FadeIn(g), FadeIn(leg))
            vo.wait_until("a")
            self.play(FadeIn(band))
            vo.wait_until("b")
            self.play(*[Create(l_) for l_ in lines], run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    def table(self, e):
        b = e["books"]
        hx = [-4.2, -1.6, 0.9, 3.2, 5.4]
        head = VGroup(label(r"book", font_size=17, color=GREY_B), label(r"Sharpe, 2007--20", font_size=17, color=GREY_B),
                      label(r"Sharpe, 2021--25", font_size=17, color=OOS_C), label(r"volatility", font_size=17, color=OOS_C),
                      label(r"worst fall", font_size=17, color=OOS_C))
        tab = VGroup(head)
        for k in ("trend", "rp", "6040", "spy"):
            r, h = b[k]["res"], b[k]["hold"]
            se = b[k]["row"]["holdout"]["sharpe_se"] if "row" in b[k] else None
            hs = rf"{h['sharpe']:.2f} \pm {se:.2f}" if se is not None else f"{h['sharpe']:.2f}"
            tab.add(VGroup(label(BNAME[k], font_size=20, color=BCOL[k]), MathTex(f"{r['sharpe']:.2f}", font_size=24),
                           MathTex(hs, font_size=24), MathTex(rf"{100 * h['vol']:.1f}\%", font_size=24),
                           MathTex(rf"{100 * h['maxdd']:.0f}\%", font_size=24)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.8 - 0.8 * j, 0])
        foot = wrapped_label(r"daily excess returns, annualised; standard errors from the 59 monthly returns in the Track "
                             r"Record; before costs", 11.4, 16, GREY_A).to_edge(DOWN, buff=0.6)
        t, r = b["trend"], b["rp"]
        with self.voiceover(
            "The numbers. <bookmark mark='a'/> On the research years the four books had similar Sharpe ratios. "
            f"<bookmark mark='b'/> On the sealed years, stocks earned {b['spy']['hold']['sharpe']:.2f}. The trend book, "
            f"{t['hold']['sharpe']:.2f}, with a standard error of {t['row']['holdout']['sharpe_se']:.2f}: positive, and "
            f"indistinguishable from its research value or from zero. Risk parity, {r['hold']['sharpe']:.2f}. Five years "
            "cannot rank these books on their Sharpe ratios. They can test what each book is for."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(r_[0], r_[1])) for r_ in tab[1:]], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(*r_[2:])) for r_ in tab[1:]], lag_ratio=0.2))
        self.wait(0.4)
        self.clear_scene()

    def y2022(self, e):
        b = e["books"]
        keys = ["spy", "6040", "rp", "trend"]
        bars = VGroup()
        for j, k in enumerate(keys):
            v = b[k]["y2022"]
            r = Rectangle(width=abs(v) * 14, height=0.55, fill_color=BCOL[k], fill_opacity=0.85, stroke_width=0)
            r.move_to([0.8, 1.6 - 1.0 * j, 0], aligned_edge=LEFT if v > 0 else RIGHT)
            bars.add(VGroup(label(BNAME[k], font_size=22, color=BCOL[k]).move_to([-4.4, 1.6 - 1.0 * j, 0]), r,
                            MathTex(rf"{100 * v:+.1f}\%", font_size=28).next_to(r, RIGHT if v > 0 else LEFT, buff=0.2)))
        axis = Line([0.8, 2.2, 0], [0.8, -2.0, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"2022, the calendar year", font_size=30).to_edge(UP, buff=0.5)
        with self.voiceover(
            "2022. <bookmark mark='a'/> Stocks lost "
            f"{abs(100 * b['spy']['y2022']):.0f} percent over bills, and sixty-forty {abs(100 * b['6040']['y2022']):.0f}, "
            f"because its bonds fell too. Risk parity, levered on those bonds, lost {abs(100 * b['rp']['y2022']):.0f}. "
            f"<bookmark mark='b'/> The trend book made {100 * b['trend']['y2022']:.0f} percent. Crisis alpha, in a crisis "
            "that unfolded over a whole year: exactly the kind of crisis Chapter two said it needs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in bars[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(bars[3]))
        self.wait(0.4)
        self.clear_scene()

    def by_class(self, e):
        by = e["trend_2022_by_class"]
        keys = sorted(by, key=by.get, reverse=True)
        mx = max(abs(by[k]) for k in keys)
        bars = VGroup()
        for j, k in enumerate(keys):
            v = by[k]
            r = Rectangle(width=max(abs(v) * 6.0 / mx, 0.03), height=0.5, fill_color=GCOL[k], fill_opacity=0.85,
                          stroke_width=0).move_to([0.0, 1.8 - 0.9 * j, 0], aligned_edge=LEFT if v > 0 else RIGHT)
            bars.add(VGroup(label(k, font_size=22, color=GCOL[k]).move_to([-4.2, 1.8 - 0.9 * j, 0]), r,
                            MathTex(rf"{100 * v:+.1f}\%", font_size=26).next_to(r, RIGHT if v > 0 else LEFT, buff=0.2)))
        axis = Line([0, 2.3, 0], [0, -2.2, 0], color=GREY_C, stroke_width=1.5)
        head = label(r"The trend book in 2022, each class's sub-book at 10\% volatility", font_size=26).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Where it came from. <bookmark mark='a'/> Short bonds, as yields rose all year: "
            f"{100 * by['bonds']:+.0f} percent. Currencies, riding the dollar's rise. Credit, which fell with the bonds. "
            "<bookmark mark='b'/> Commodities added little, and equities, which fell in fits and rallies, cost a "
            "little. The book made money by being short the assets that a balanced "
            "portfolio owns."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bars[3:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()

    def flip(self, e):
        sb = e["sb_corr"]
        yrs = sb["years"]
        g = axes([2020.4, 2025.6], [-0.6, 0.4], x_length=7.4, y_length=4.0, xlabel=r"calendar year",
                 ylabel=r"daily correlation, SPY and TLT", xticks=[2021, 2022, 2023, 2024, 2025], yticks=[-0.4, 0, 0.4],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.1f}", font_size=15).move_to(LEFT * 1.4 + DOWN * 0.2)
        ax = g.ax
        zero = DashedLine(ax.c2p(2020.4, 0), ax.c2p(2025.6, 0), color=GREY_C, stroke_width=1.5)
        res = DashedLine(ax.c2p(2020.4, sb["research"]), ax.c2p(2025.6, sb["research"]), color=BOND_C, stroke_width=1.5)
        rl = label(rf"2007--2020: {sb['research']:+.2f}", font_size=16, color=BOND_C).next_to(ax.c2p(2025.6,
                                                                                                  sb["research"]), UP,
                                                                                         buff=0.08).shift(LEFT * 1.2)
        dots = VGroup()
        for y, v in yrs.items():
            h = abs(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1])
            dots.add(Rectangle(width=0.5, height=max(h, 0.02), fill_color=BAD if v > 0 else BOND_C, fill_opacity=0.85,
                               stroke_width=0).move_to(ax.c2p(int(y), v / 2)))
        lev = e["rp_lev_hold"]
        txt = wrapped_label(rf"risk parity's leverage in these years averaged {lev['mean']:.2f}: the rule de-levered as "
                            r"bond volatility rose, but only after the losses", 3.6, 16, GREY_A).to_edge(RIGHT, buff=0.3)
        fit_right(txt)
        with self.voiceover(
            "And the reason risk parity failed. <bookmark mark='a'/> Over the research years, American stocks and "
            f"long Treasuries had a daily correlation of {sb['research']:+.2f}. <bookmark mark='b'/> From 2022 it was "
            f"positive every year: {yrs['2022']:+.2f}, {yrs['2023']:+.2f}, {yrs['2024']:+.2f}, {yrs['2025']:+.2f}. The "
            "sign of the 1970s, 80s and 90s came back with inflation, as Chapter four's history said it could. "
            f"<bookmark mark='c'/> The rule de-levered as bond volatility rose, to an average of {lev['mean']:.2f} times, "
            "but only after the losses had been taken."
        ) as vo:
            self.play(FadeIn(g), Create(zero))
            vo.wait_until("a")
            self.play(Create(res), FadeIn(rl))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(d_, DOWN) for d_ in dots], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(txt))
        self.wait(0.4)
        self.clear_scene()

    def reading(self, e):
        cards = VGroup(
            desk_question(r"what the trend book promised", r"to make money in a slow crisis and to be uncorrelated "
                          r"otherwise; it did both, and its Sharpe ratio over five years says nothing more", width=12.4,
                          font_size=19),
            desk_question(r"what risk parity assumed", r"that bonds hedge stocks; for twenty years they had, and in 2022 "
                          r"they did not; a levered book cannot survive the one regime it is not built for", width=12.4,
                          font_size=19),
            desk_question(r"what the Track Record keeps", r"two rows, each with a standard error larger than its value; "
                          r"the finale weighs them with the rest of the series", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "How to read it. <bookmark mark='a'/> The trend book promised to make money in a slow crisis and to be "
            "uncorrelated otherwise. It did both. <bookmark mark='b'/> Risk parity assumed that bonds hedge stocks. For "
            "twenty years they had; in 2022 they did not, and a levered book has no defence against the one regime it "
            "is not built for. <bookmark mark='c'/> The Track Record keeps two rows whose standard errors exceed their "
            "values. The finale weighs them with everything else."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()


    def blend(self, e):
        b = e["books"]
        rt = np.asarray(b["trend"]["hold_m"], float)
        r6 = np.asarray(b["6040"]["hold_m"], float)
        hm = np.asarray(b["trend"]["hold_months"])
        rows = []
        for k in (0.0, 0.2):
            r = (1 - k) * r6 + k * rt
            g = np.cumprod(1 + r)
            rows.append((k, r.mean() / r.std() * np.sqrt(12), float(np.min(g / np.maximum.accumulate(g) - 1)),
                         float(np.prod(1 + r[hm // 100 == 2022]) - 1)))
        hx = [-3.6, -0.8, 1.8, 4.4]
        head = VGroup(label(r"share in trend", font_size=18, color=TREND_C), label(r"Sharpe, 2021--25", font_size=18,
                                                                                  color=OOS_C),
                      label(r"worst fall", font_size=18, color=OOS_C), label(r"2022", font_size=18, color=OOS_C))
        tab = VGroup(head)
        for k, sr, dd, y22 in rows:
            tab.add(VGroup(MathTex(rf"{100 * k:.0f}\%", font_size=28), MathTex(f"{sr:.2f}", font_size=28),
                           MathTex(rf"{100 * dd:.0f}\%", font_size=28), MathTex(rf"{100 * y22:+.0f}\%", font_size=28)))
        for j, row in enumerate(tab):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.2 - 0.9 * j, 0])
        foot = wrapped_label(r"60/40 with a fifth of its capital in the registered trend book, on the sealed years; the same "
                             r"blend as Chapter 2, not a new strategy", 11.0, 17, GREY_A).to_edge(DOWN, buff=0.7)
        y0, y1 = abs(100 * rows[0][3]), abs(100 * rows[1][3])
        d0, d1 = abs(100 * rows[0][2]), abs(100 * rows[1][2])
        s0, s1 = rows[0][1], rows[1][1]
        with self.voiceover(
            "And the use Chapter two proposed, on the sealed years. <bookmark mark='a'/> A sixty-forty portfolio with a "
            f"fifth moved into the trend book: its 2022 loss shrinks from {y0:.0f} percent to {y1:.0f}, its worst fall "
            f"from {d0:.0f} to {d1:.0f}, and its Sharpe ratio moves from {s0:.2f} to {s1:.2f}. The diversifier did its "
            "job in the one year it was needed."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3))
        self.wait(0.4)
        self.clear_scene()


    def next_steps(self):
        cards = VGroup(
            desk_question(r"for the trend book", r"more markets, futures instead of funds, and a blend of lookbacks; each "
                          r"is a new trial, judged on data that did not exist when it was chosen", width=12.4, font_size=19),
            desk_question(r"for risk parity", r"stress the book under a positive stock--bond correlation before sizing "
                          r"its leverage, and add assets that hedge inflation, such as commodities and inflation-linked "
                          r"bonds, at their own risk budgets", width=12.4, font_size=19),
            desk_question(r"for both", r"report the crisis years first: a premium book is held for what it does in the "
                          r"years an investor fears", width=12.4, font_size=19),
        ).arrange(DOWN, buff=0.25)
        with self.voiceover(
            "What the macro desk would do next. <bookmark mark='a'/> For the trend book: more markets, futures in place "
            "of funds, a blend of lookbacks; each change a new trial, judged on new data. <bookmark mark='b'/> For risk "
            "parity: stress the book under a positive stock-bond correlation before sizing its leverage, and give assets "
            "that hedge inflation their own risk budget. <bookmark mark='c'/> And for both: report the crisis years "
            "first, because that is what these books are held for."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = pause_card(r"a trend book earned a Sharpe ratio of 0.27 over five years. How many years would a true Sharpe "
                       r"of 0.3 need to be two standard errors from zero?")
        with self.voiceover(
            "Pause and predict. A trend book earned a Sharpe ratio of point two seven over five years. If its true "
            "Sharpe ratio is point three, how many years would it take to be two standard errors from zero?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
