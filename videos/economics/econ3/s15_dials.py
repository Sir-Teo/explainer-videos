from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

COMP_COLOR = {"upper-level substitution": PAAS, "lower-level substitution": "#4F9FD0",
              "new products and quality": FISHER, "new outlets": E.GAIN, "weighting": GREY_B}
COMP_NAME = {"upper-level substitution": r"between goods", "lower-level substitution": r"within a good",
             "new products and quality": r"new products, quality", "new outlets": r"new shops",
             "weighting": r"weights"}


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ how biased is the price index?", r"After thirty years of repairs, how far off "
             r"is the CPI?", "Chapter thirteen. The Dials: how biased is the price index?", scale=("nation",),
             horizon=("a decade",))
        self.dial()
        self.audits()
        self.kaldor()

    # ------------------------------------------------------------------
    def dial(self):
        dial = dials.DIALS["cpi_bias"]
        rows_def = [(r"Boskin et al.\ (1996)", r"the CPI in 1995--96"),
                    (r"Lebow and Rudd (2003)", r"after the reforms"),
                    (r"Gordon (2006)", r"1995--96, revisited"),
                    (r"Gordon (2006)", r"the CPI in 2006"),
                    (r"Moulton (2018)", r"the CPI in 2017")]
        color = DIAL_STATUS.get(dial.status, GREY_C)
        head = VGroup(label(dial.name, font_size=30),
                      VGroup(RoundedRectangle(width=3.6, height=0.42, corner_radius=0.08, stroke_width=0,
                                              fill_color=color, fill_opacity=1),
                             label(dial.status, font_size=20, color=BACKGROUND))).arrange(RIGHT, buff=0.4)
        head[1][1].move_to(head[1][0])
        units = label(r"percentage points a year by which the CPI overstates the rise in the cost of living",
                      font_size=20, color=GREY_B)
        VGroup(head, units).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(UP, buff=0.4).to_edge(LEFT, buff=0.6)
        x0, x1 = -0.4, 6.2
        lo, hi = 0.0, 1.8

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)

        top_y = 1.55
        axis_y = top_y - 5 * 0.62 - 0.1
        axis = Line([x0, axis_y, 0], [x1, axis_y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), axis_y - 0.07, 0], [X(v), axis_y + 0.07, 0], color=GREY_C),
                                MathTex(f"{v:g}", font_size=22, color=GREY_B).move_to([X(v), axis_y - 0.32, 0]))
                         for v in (0, 0.3, 0.6, 0.9, 1.2, 1.5, 1.8)])
        grid = VGroup(*[DashedLine([X(v), axis_y, 0], [X(v), top_y + 0.35, 0], color=GREY_D, stroke_width=1)
                        for v in (0.3, 0.6, 0.9, 1.2, 1.5)])
        rows = VGroup()
        for k, (e, (who, what)) in enumerate(zip(dial.estimates, rows_def)):
            y = top_y - 0.62 * k
            c = DESIGN_COLOR.get(e.design, GREY_B)
            t = VGroup(label(who, font_size=22, color=WHITE), label(what, font_size=18, color=GREY_B)).arrange(
                DOWN, aligned_edge=RIGHT, buff=0.04).move_to([x0 - 0.4, y, 0], aligned_edge=RIGHT)
            bar = Line([X(e.lo if e.lo is not None else e.value), y, 0], [X(e.hi if e.hi is not None else e.value),
                                                                          y, 0], color=c, stroke_width=5)
            dot = Dot([X(e.value), y, 0], radius=0.1, color=c)
            val = label(f"{e.value:.2f}", font_size=20, color=c).next_to(dot, UP, buff=0.08)
            rows.add(VGroup(t, bar, dot, val))
        meaning = wrapped_label(dial.meaning, 12.0, 21, GREY_A).to_edge(DOWN, buff=0.45)
        src = published_tag(r"Boskin et al.\ (1996); \ Lebow and Rudd (2003); \ Gordon (2006); \ Moulton (2018): "
                            r"expert reviews", corner=DR, font_size=14).shift(UP * 0.0)
        e = dial.estimates
        with self.voiceover(
            "This part enters a new dial: how far the consumer price index overstates the rise in the cost of "
            "living, in percentage points a year. Its estimates come from expert reviews, which add up the bias "
            "source by source from many smaller studies. <bookmark mark='a'/> The Boskin Commission put it at "
            f"{e[0].value:.1f} points for the mid-1990s, plausibly from 0.8 to 1.6. <bookmark mark='b'/> After the "
            f"bureau's reforms, David Lebow and Jeremy Rudd put it at {e[1].value:.2f}, with a plausible range from "
            "0.3 to 1.4. <bookmark mark='c'/> Robert Gordon, one of the original commissioners, looked back in 2006: "
            "with what was known by then, the 1990s bias had been more like 1.2 or 1.3, and the bias of 2006 about "
            f"0.8. <bookmark mark='d'/> And Brent Moulton's audit for 2017 found {e[4].value:.2f}. "
            "<bookmark mark='e'/> The status is settled within a range: the index overstates inflation, by "
            "somewhere between a few tenths of a point and a point and a half a year, and the best single guess "
            "has stayed close to one. Over a decade that compounds, and every indexed payment drifts with it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(units), Create(axis), FadeIn(ticks), FadeIn(grid), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][0]), Create(rows[0][1]), FadeIn(rows[0][2], scale=0.6), FadeIn(rows[0][3]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1][0]), Create(rows[1][1]), FadeIn(rows[1][2], scale=0.6), FadeIn(rows[1][3]))
            vo.wait_until("c")
            for r in rows[2:4]:
                self.play(FadeIn(r[0]), Create(r[1]), FadeIn(r[2], scale=0.6), FadeIn(r[3]), run_time=0.8)
            vo.wait_until("d")
            self.play(FadeIn(rows[4][0]), Create(rows[4][1]), FadeIn(rows[4][2], scale=0.6), FadeIn(rows[4][3]))
            vo.wait_until("e")
            self.play(FadeIn(meaning))
        self.clear_scene()

    def audits(self):
        c = load("cpi")["audit"]
        comps = c["components"]
        k = 7.2
        x0 = -4.0
        studies = ((r"Boskin et al.\ (1996)", c["boskin_1996"]), (r"Lebow and Rudd (2003)", c["lebow_rudd_2003"]),
                   (r"Moulton (2018)", c["moulton_2018"]))
        rows = VGroup()
        for i, (nm, vals) in enumerate(studies):
            y = 1.5 - 1.25 * i
            t = label(nm, font_size=24, color=GREY_A).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            segs = VGroup()
            x = x0
            for comp, v in zip(comps, vals):
                if v <= 0:
                    continue
                r = Rectangle(width=v * k, height=0.7, stroke_color=BACKGROUND, stroke_width=1.5,
                              fill_color=COMP_COLOR[comp], fill_opacity=0.9).move_to([x + v * k / 2, y, 0])
                segs.add(VGroup(r, label(f"{v:.2f}", font_size=19, color=BACKGROUND).move_to(r)))
                x += v * k
            tot = label(f"{sum(vals):.2f}", font_size=26, color=FISHER).move_to([x + 0.45, y, 0])
            rows.add(VGroup(t, segs, tot))
        legend = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=COMP_COLOR[cm], fill_opacity=0.9),
                                 label(COMP_NAME[cm], font_size=21, color=COMP_COLOR[cm])).arrange(RIGHT, buff=0.1)
                          for cm in comps]).arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=1.0)
        head = label(r"The bias, \ source by source \ (points a year)", font_size=30).to_edge(UP, buff=0.4)
        lesson = label(r"the fixes worked within goods; \ substitution between goods and quality remain",
                       font_size=24, color=E.ACCENT).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"Moulton (2018), table 5", corner=DR, font_size=14).shift(UP * 0.35)
        with self.voiceover(
            "The sources tell you what the reforms fixed. <bookmark mark='a'/> In 1996: a quarter of a point from "
            "substitution within goods, six tenths from new products and quality, and the rest from switching "
            "between goods and between shops. <bookmark mark='b'/> By 2003 the geometric means had cut the bias "
            "within goods to a twentieth of a point, and better quality adjustment had cut the largest part by "
            "about a third. But the chained index revealed more substitution between goods than the commission "
            "had thought. <bookmark mark='c'/> Moulton's update keeps the same shape. <bookmark mark='d'/> What "
            "remains is mostly Bo's problem, switching between goods, which a fixed basket can't see, and the "
            "hardest problem of all: putting a price on things that are new."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), LaggedStart(*[GrowFromEdge(s[0], LEFT) for s in r[1]], lag_ratio=0.2),
                          *[FadeIn(s[1]) for s in r[1]], FadeIn(r[2]))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.clear_scene()

    def kaldor(self):
        k = load("kaldor")
        facts_list = VGroup(*[label(t, font_size=22) for t in (
            r"1. \ output per worker grows at a roughly steady rate",
            r"2. \ capital per worker grows too",
            r"3. \ the return on capital is roughly steady",
            r"4. \ so is the ratio of capital to output",
            r"5. \ the shares of labour and capital in income are roughly steady",
            r"6. \ growth rates differ widely across countries")]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        head = VGroup(label(r"Facts", font_size=22, color=E.ACCENT),
                      label(r"Nicholas Kaldor's stylized facts of growth (1961)", font_size=28)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        block = VGroup(head, facts_list).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL, buff=0.45)
        ax1 = year_axis([1870, 2023], [np.log10(2500), np.log10(80000)], x_length=5.6, y_length=2.6,
                        xticks=[1900, 1950, 2000], yticks=[np.log10(v) for v in (3000, 10000, 30000)], log_y=True,
                        ylabel=r"US GDP per head, \ 2011 dollars, \ log", font_size=17,
                        center=RIGHT * 3.4 + DOWN * 1.9)
        a1 = ax1.ax
        line1 = VMobject(stroke_color=E.DATA, stroke_width=2.5).set_points_as_corners(
            [a1.c2p(y, np.log10(v)) for y, v in zip(k["years"], k["gdppc"])])
        g1 = label(rf"trend: \ {100 * k['trend_growth']:.1f}\% a year", font_size=19, color=E.ACCENT)
        g1.next_to(a1.c2p(1880, np.log10(30000)), RIGHT, buff=0.1)
        ax2 = year_axis([1950, 2024], [0.5, 0.7], x_length=5.6, y_length=2.6, xticks=[1950, 1980, 2010],
                        yticks=[0.5, 0.6, 0.7], yfmt=lambda v: f"{100 * v:.0f}\\%",
                        ylabel=r"US labour share of GDP", font_size=17, center=LEFT * 3.4 + DOWN * 1.9)
        a2 = ax2.ax
        line2 = VMobject(stroke_color=WAGES, stroke_width=2.5).set_points_as_corners(
            [a2.c2p(y, v) for y, v in zip(k["ls_years"], k["labour_share"])])
        g2 = label(rf"{100 * k['ls_1950_79']:.0f}\% (1950--79) \ $\to$ \ {100 * k['ls_last']:.0f}\% "
                   rf"({k['ls_last_year']})", font_size=19, color=WAGES)
        g2.next_to(a2.c2p(1952, 0.53), RIGHT, buff=0.05)
        explained = label(r"shown here; \ explained in Part 20, \ and the labour share's fall in Part 39",
                          font_size=21, color=GREY_B).next_to(block, RIGHT, buff=0.4).align_to(block, UP).shift(DOWN * 0.6)
        if explained.width > 4.4:
            explained.width = 4.4
        tag = data_tag(rf"Maddison Project 2023; Penn World Table via FRED (LABSHPUSA156NRUG), "
                       rf"{data.fred_cite('LABSHPUSA156NRUG')}", corner=DL, font_size=13)
        with self.voiceover(
            "The accounts also produced the first facts of growth. <bookmark mark='a'/> In 1961 Nicholas Kaldor "
            "listed six that a theory of growth would have to explain, every one of them a reading of the national "
            "accounts. <bookmark mark='b'/> The first is in the data: American output per head, on a log scale, "
            f"has grown along a nearly straight line since 1870, about {100 * k['trend_growth']:.1f} percent a "
            "year, through depressions and wars. <bookmark mark='c'/> The fifth has held less well. The share of "
            f"income paid to labour stayed near {100 * k['ls_1950_79']:.0f} percent for decades and has fallen "
            f"since 2000, to {100 * k['ls_last']:.0f} percent by {k['ls_last_year']}. <bookmark mark='d'/> These "
            "facts are entered on the series' list here. Part 20 builds the model that explains Kaldor's facts, "
            "and Part 39 asks why labour's share fell."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(head), LaggedStart(*[FadeIn(f, shift=RIGHT * 0.1) for f in facts_list], lag_ratio=0.3),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(ax1), Create(line1), FadeIn(g1), Indicate(facts_list[0], color=E.ACCENT))
            vo.wait_until("c")
            self.play(FadeIn(ax2), Create(line2), FadeIn(g2), Indicate(facts_list[4], color=WAGES))
            vo.wait_until("d")
            self.play(FadeIn(explained))
        self.clear_scene()
