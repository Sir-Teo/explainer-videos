from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import PART, VALUE, load, real_data

ASOF_CODE = [
    "def history(self, entity, concept, t):",
    "    last = {}                      # each period's latest value filed by t",
    "    for f in self.known(entity, concept, t):     # f.filed <= t",
    "        if f.period_end not in last or f.filed >= last[f.period_end].filed:",
    "            last[f.period_end] = f",
    "    return [last[k] for k in sorted(last)]",
    "",
    "def asof(self, entity, concept, t):",
    "    h = self.history(entity, concept, t)",
    "    return h[-1].value if h else None",
]


def _yr(n: int) -> float:
    d = date(n // 10000, n // 100 % 100, n % 100)
    return d.year + (d.timetuple().tm_yday - 1) / 365.25


class House(VoiceoverScene):
    def construct(self):
        p = load("pit")
        self.card()
        self.xbrl()
        self.plane(p)
        self.lab(p)
        self.audit(p)

    def card(self):
        c = chapter_card(5, r"XBRL and the point-in-time store", r"When could the market have known?", part=PART)
        with self.voiceover("Chapter five. XBRL, and the point-in-time store."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def xbrl(self):
        fact = VGroup(
            label(r"one fact in a filing", font_size=24, color=GREY_B),
            MathTex(r"\texttt{us-gaap:NetIncomeLoss}", font_size=34, color=VALUE),
            MathTex(r"\text{value, unit USD, period: the fiscal year}", font_size=30),
            MathTex(r"\text{filed: the day the 10-K reached the SEC}", font_size=30, color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        box = SurroundingRectangle(fact, buff=0.35, color=GREY_C, corner_radius=0.12)
        card_ = VGroup(box, fact).to_edge(UP, buff=0.6)
        rules = VGroup(
            wrapped_label(r"SEC Release 33-9002 (2009): XBRL from fiscal periods ending after 15 June 2009 for large "
                          r"accelerated filers with a float above \$5 billion; other large accelerated filers from June "
                          r"2010; everyone else from June 2011.", 11.4, 23, GREY_A),
            wrapped_label(r"The 10-K is due 60 days after the year ends for large accelerated filers, 75 for "
                          r"accelerated filers, 90 for the rest; numbers can be restated or recast years later.", 11.4,
                          23, QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(card_, DOWN, buff=0.5)
        with self.voiceover(
            "Since 2009 the SEC has required filings in machine-readable XBRL, phased in from the largest filers to all by 2011. "
            "<bookmark mark='a'/> Each number is a tagged fact: concept, value, unit, period, filing. <bookmark mark='b'/> The "
            "10-K is due sixty to ninety days after the year ends, and numbers are restated or recast later. Every number has two "
            "dates: the period it describes and the day it became public."
        ) as vo:
            self.play(Create(box), FadeIn(fact[0]), FadeIn(rules[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in fact[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]), Indicate(fact[3], color=QC.HOUSE))
        self.wait(0.4)
        self.clear_scene()

    def plane(self, p):
        F = np.asarray(p["planes"]["General Electric revenue"], float)
        ends, filed, vals = F[:, 0].astype(int), F[:, 1].astype(int), F[:, 2] / 1e9
        X = np.array([_yr(e) for e in ends])
        Y = np.array([_yr(f) for f in filed])
        g = axes([2008.5, 2021.2], [2009.5, 2022.0], x_length=5.6, y_length=5.0, xlabel=r"fiscal year described",
                 ylabel=r"filing date", xticks=[2010, 2014, 2018], yticks=[2010, 2014, 2018, 2022],
                 xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{int(v)}", font_size=17).to_edge(LEFT, buff=0.5)
        g.shift(DOWN * 0.2)
        ax = g.ax
        diag = DashedLine(ax.c2p(2009.5, 2009.5), ax.c2p(2021.2, 2021.2), color=GREY_D, stroke_width=1.5)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.055, color=GREY_B, fill_opacity=0.6) for x, y in zip(X, Y)])
        t = ValueTracker(2009.6)
        h = axes([2008.5, 2021.2], [90, 190], x_length=5.4, y_length=3.6, xlabel=r"fiscal year",
                 ylabel=r"GE revenue, \$ billion, as the store answers", xticks=[2010, 2014, 2018],
                 yticks=[100, 150], xfmt=lambda v: f"{int(v)}", font_size=17).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
        hx = h.ax

        def lit():
            tt = t.get_value()
            out = VGroup()
            line = Line(ax.c2p(2008.5, tt), ax.c2p(2021.2, tt), color=QC.HOUSE, stroke_width=3)
            out.add(line, label(rf"as of {tt:.1f}", font_size=20, color=QC.HOUSE).next_to(line, RIGHT, buff=0.1))
            xs, ys = [], []
            for e in np.unique(X):
                m = (X == e) & (Y <= tt)
                if not m.any():
                    continue
                j = np.flatnonzero(m)[np.argmax(Y[m])]
                out.add(Dot(ax.c2p(X[j], Y[j]), radius=0.08, color=VALUE))
                xs.append(e)
                ys.append(vals[j])
            if len(xs) > 1:
                out.add(VMobject(stroke_width=3, stroke_color=VALUE).set_points_as_corners(
                    [hx.c2p(a, np.clip(b, 90, 190)) for a, b in zip(xs, ys)]))
            out.add(*[Dot(hx.c2p(a, np.clip(b, 90, 190)), radius=0.05, color=VALUE) for a, b in zip(xs, ys)])
            return out

        lv = always_redraw(lit)
        cap = wrapped_label(r"each dot: one filed value of one year's revenue; the store's answer for each year is the "
                            r"highest dot below the line", 5.6, 18, GREY_B).next_to(h, DOWN, buff=0.35)
        src = real_data(r"SEC EDGAR company facts: General Electric, 10-K revenue, FY2008--2020")
        with self.voiceover(
            "Here is that idea as a plane. Across, the fiscal year a number describes; up, the day it was filed. Every dot is one "
            "value of General Electric's annual revenue as some 10-K reported it, and all sit above the diagonal: a number is "
            "filed after its year ends. <bookmark mark='a'/> Sweep an as-of line upwards. For each year, the store answers with "
            "the highest dot below the line, the latest value anyone could have seen that day; the history it returns is on the "
            "right. <bookmark mark='b'/> Watch it change. Each time GE sold a business, its 10-K recast the past years without it. "
            "A database that keeps only the latest number hands a 2012 backtest a GE that did not yet exist."
        ) as vo:
            self.play(FadeIn(g), Create(diag), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.02, run_time=2.5))
            vo.wait_until("a")
            self.play(FadeIn(h), FadeIn(cap))
            self.add(lv)
            self.play(t.animate.set_value(2014.0), run_time=5, rate_func=linear)
            vo.wait_until("b")
            self.play(t.animate.set_value(2021.9), run_time=8, rate_func=linear)
        lv.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def lab(self, p):
        card = lab_card(r"the as-of query", ASOF_CODE, source="explainer/quant/house/fundamentals.py", width=7.6,
                        font_size=17).to_corner(UL, buff=0.3)
        v1, v2 = p["khc_views"]["20180630"], p["khc_views"]["20200630"]

        def fmt(v):
            return "  ".join(f"FY{int(e) // 10000 if int(e) % 10000 > 600 else int(e) // 10000 - 1}: "
                             f"{x / 1e6:,.0f}" for e, x, _ in v if 20161231 <= int(e) <= 20171231)

        rest = p["khc_restatements"]
        sec = firm_card(r"Kraft Heinz, 2015--2019",
                        r"The SEC found an expense-management misconduct scheme: about \$208 million of improperly "
                        r"recognised cost savings from late 2015 to 2018, corrected in a restatement in June 2019. "
                        r"Settled in 2021 without admitting or denying the findings.",
                        numbers=[(r"\$62\text{m}", r"civil penalty"), (r"\$208\text{m}", r"cost savings restated")],
                        source=r"SEC press release 2021-174", width=5.4, font_size=20).to_corner(UR, buff=0.3)
        with self.voiceover(
            "The House's code for that query is short: for each period, keep the latest fact filed by the day you ask; the "
            "answer is the last of them, or nothing if nothing was filed. <bookmark mark='a'/> Run it on Kraft Heinz. In 2021 the "
            "SEC settled charges that the company had improperly booked about two hundred and eight million dollars of cost "
            "savings from late 2015 to 2018, corrected in a restatement in June 2019. <bookmark mark='b'/> Ask for net income as "
            "of mid-2018 and the store returns the numbers as first reported; as of mid-2020, 2016 and 2017 are lower. Both "
            "answers are right for their day: a restatement is a new fact, never an edit of the old one."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(sec))
            vo.wait_until("b")
            lab_run(self, card, ["store.history('KHC', 'NetIncomeLoss', 20180630)   # $ million",
                                 fmt(v1),
                                 "store.history('KHC', 'NetIncomeLoss', 20200630)",
                                 fmt(v2) + f"   (restated {rest[0][3] // 10000}-{rest[0][3] // 100 % 100:02d})"])
        self.wait(0.4)
        self.clear_scene()

    def audit(self, p):
        firms = p["firms"]
        head = VGroup(*[label(t, font_size=19, color=GREY_B) for t in
                        (r"firm (10-K, FY2009--2020)", r"net income changed", r"revenue changed",
                         r"median days to 10-K")])
        rows = []
        for f in firms:
            ni, sa = f["net_income"], f["sales"]
            rows.append([label(f["name"], font_size=19),
                         MathTex(rf"{ni[1]}/{ni[0]}", font_size=24, color=QC.LOSS if ni[1] else GREY_A),
                         MathTex(rf"{sa[1]}/{sa[0]}" if sa[0] else r"\text{--}", font_size=24,
                                 color=QC.LOSS if sa[1] else GREY_A),
                         MathTex(rf"{f['median_lag']:.0f}" if f["median_lag"] is not None else "--", font_size=24,
                                 color=QC.HOUSE)])
        tab = VGroup(head, *[VGroup(*r) for r in rows])
        xs = [-6.2, -2.5, -0.6, 1.3]
        for k_, r in enumerate(tab):
            for c, m in enumerate(r):
                m.move_to([xs[c] + m.width / 2 if c == 0 else xs[c] + 0.9, 2.6 - 0.48 * k_, 0])
        lags = np.asarray(p["lags"])
        g = axes([0, 100], [0, 0.5], x_length=3.8, y_length=3.0, xlabel=r"days from year end to the 10-K",
                 xticks=[0, 60, 90], yticks=[], font_size=16).move_to(RIGHT * 5.0 + UP * 0.6)
        ax = g.ax
        hist, edges = np.histogram(np.clip(lags, 0, 99), bins=20, range=(0, 100))
        hist = hist / hist.sum()
        bars = VGroup(*[Rectangle(width=(ax.c2p(5, 0)[0] - ax.c2p(0, 0)[0]) * 0.9,
                                  height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 0.002), stroke_width=0,
                                  fill_color=QC.HOUSE, fill_opacity=0.8).move_to(ax.c2p(e + 2.5, 0), aligned_edge=DOWN)
                        for e, v in zip(edges[:-1], hist)])
        rules = VGroup(*[DashedLine(ax.c2p(d, 0), ax.c2p(d, 0.5), color=c, stroke_width=2)
                         for d, c in ((60, QC.LOSS), (75, GREY_B), (90, GREY_B))])
        note_ = wrapped_label(rf"median {np.median(lags):.0f} days: a backtest that uses December's earnings on 1 "
                              r"January has read about two months of the future", 4.2, 19, GREY_A).next_to(g, DOWN, buff=0.3)
        pp = desk_question(r"Pause and predict: how many of GE's annual revenue figures did a later 10-K show "
                           r"differently?", width=6.4, font_size=21).to_edge(DOWN, buff=0.3).to_edge(LEFT, buff=0.4)
        src = real_data(r"SEC EDGAR company facts, filings through October 2026; changes include restatements and recasts")
        ge = next(f for f in firms if f["name"] == "General Electric")
        with self.voiceover(
            "An audit of the cached filings: how many years' net income and revenue a later 10-K showed differently. "
            f"<bookmark mark='a'/> Pause and predict: General Electric's revenue? <bookmark mark='b'/> {ge['sales'][1]} of "
            f"{ge['sales'][0]}, mostly recasts, not frauds. <bookmark mark='c'/> And the median 10-K arrived {np.median(lags):.0f} "
            "days after year end: a backtest using December's earnings on the first of January reads two months of the future."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(src))
            self.play(LaggedStart(*[FadeIn(VGroup(*r[:1])) for r in tab[1:]], lag_ratio=0.1))
            self.play(FadeIn(VGroup(*[r[1] for r in tab[1:]])))
            vo.wait_until("a")
            self.play(FadeIn(pp))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[r[2] for r in tab[1:]])), FadeOut(pp))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*[r[3] for r in tab[1:]])), FadeIn(g), FadeIn(bars), Create(rules))
            self.play(FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()
