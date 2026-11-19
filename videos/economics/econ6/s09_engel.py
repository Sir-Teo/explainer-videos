from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


class Engel(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Engel curves", r"How does what people buy change as they get richer?",
             "Chapter seven. Engel curves.", horizon=("a century",), scale=("household", "nation"))
        self.engel()
        self.america()
        self.quintiles()
        self.hamilton()
        self.called()

    def engel(self):
        t = tables.ENGEL_1857.data
        h = history_card(r"1857", r"Ernst Engel, director of the Saxon statistical bureau",
                         r"from the budgets of Belgian working families collected by Ducpétiaux, and Saxony's own",
                         color=E.ACCENT, width=9.6, font_size=24).to_edge(UP, buff=0.5)
        q = quote_card(t["engel"], r"Engel (1857), in C.\ C.\ Zimmerman's translation (1932)", width=11.0,
                       font_size=27, color=E.ACCENT).next_to(h, DOWN, buff=0.45)
        hk = label(r"``Engel's law, formulated in 1857, is confirmed by all surveys.'' \ --- Houthakker (1957)",
                   font_size=24, color=GREY_A).next_to(q, DOWN, buff=0.45)
        tag = published_tag(r"Zimmerman, QJE (1932); Houthakker, Econometrica (1957); both via Anker (2011)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "The curves that show how purchases change with income are named after a statistician. "
            "<bookmark mark='a'/> In 1857 Ernst Engel, who ran the statistical bureau of the Kingdom of Saxony, "
            "studied the budgets of Belgian working families and found a regularity. <bookmark mark='b'/> The poorer "
            "a family, he wrote, the greater the proportion of its spending that must go on food. And he went "
            "further: the share spent on food, other things equal, is the best measure of a population's material "
            "standard of living. <bookmark mark='c'/> A hundred years later, Hendrik Houthakker compared about forty "
            "household surveys from thirty countries and wrote that Engel's law is confirmed by all of them."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(hk))
        self.clear_scene()

    def america(self):
        e = load("engel")
        from explainer.ai.viz import axes

        years = list(e["years"])
        real = np.log10(np.array(e["real"]))
        food = 100 * np.array(e["food_share"])

        def p10(v):
            return f"{10 ** v:,.0f}".replace(",", "{,}")

        ax = axes([3.7, 4.75], [0, 26], x_length=7.2, y_length=5.0,
                  xticks=[np.log10(5000), np.log10(10000), np.log10(20000), np.log10(40000)],
                  yticks=[0, 5, 10, 15, 20, 25], xlabel=r"real spending per head \ (2017 \$, log scale)",
                  ylabel=r"share spent on food at home (\%)", font_size=17, xfmt=p10, yfmt=lambda v: f"{v:.0f}",
                  center=LEFT * 2.0 + DOWN * 0.3)
        a = ax.ax
        path = VMobject(stroke_color=E.ACCENT, stroke_width=4).set_points_as_corners(
            [a.c2p(x, y) for x, y in zip(real, food)])
        marks = VGroup()
        for yr in (1929, 1945, 1970, 2000, 2025):
            i = years.index(yr)
            d = Dot(a.c2p(real[i], food[i]), radius=0.07, color=WHITE)
            marks.add(VGroup(d, label(str(yr), font_size=17, color=GREY_A).next_to(d, UR, buff=0.05)))
        side = VGroup(
            label(rf"food at home: \ {food[0]:.0f}\% $\to$ {food[-1]:.1f}\% of spending", font_size=24),
            label(rf"real spending per head \ $\times${e['real_ratio']:.1f}", font_size=24, color=E.ACCENT),
            label(rf"food bought per head \ $\times${e['food_q_ratio']:.1f}", font_size=24, color=COCO),
            label(rf"food's relative price \ $\times${e['food_rel_ratio']:.2f}: \\ almost unchanged", font_size=22,
                  color=GREY_A),
            label(rf"so the century's income elasticity \\ of food: \ about {e['century_el']:.2f}", font_size=25,
                  color=HICKS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        foot = label(r"a necessity: \ more is bought as income grows, \ but less than in proportion", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.2)
        tag = data_tag(r"BEA, personal consumption expenditures by type of product (FRED)", corner=UL, font_size=13)
        with self.voiceover(
            "Here is Engel's law in America over almost a century. <bookmark mark='a'/> Across, real spending per "
            "person; up, the share of it spent on food bought to eat at home. As Americans got richer, the share "
            "fell, from about a fifth in 1929 to seven and a half percent in 2025. <bookmark mark='b'/> Real "
            "spending per head rose about six and a half times. Americans did buy more food, about two and a half "
            "times as much, but far less than in proportion. <bookmark mark='c'/> And food's price relative to "
            "everything else ended the century almost where it began, so the change is mostly an income effect: "
            "food's income elasticity across the century comes out at about nought point four seven. "
            "<bookmark mark='d'/> Below one: food is a necessity. Part of the fall, to be fair, is food that moved "
            "from home kitchens to restaurants."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(path), run_time=3.0)
            self.play(LaggedStart(*[FadeIn(m_) for m_ in marks], lag_ratio=0.3), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def quintiles(self):
        e = load("engel")
        from explainer.ai.viz import axes

        groups = ("lowest", "middle", "highest")
        names = {"lowest": r"poorest fifth", "middle": r"middle fifth", "highest": r"richest fifth"}
        ax = axes([0, 3], [0, 36], x_length=5.6, y_length=4.6, xticks=None, yticks=[0, 10, 20, 30],
                  ylabel=r"food, \% of income", font_size=18, yfmt=lambda v: f"{v:.0f}",
                  center=LEFT * 3.4 + DOWN * 0.2)
        a = ax.ax
        bars = VGroup()
        for k, g in enumerate(groups):
            sh = 100 * e["quintile_share"][g]
            r = Polygon(a.c2p(k + 0.2, 0), a.c2p(k + 0.8, 0), a.c2p(k + 0.8, sh), a.c2p(k + 0.2, sh),
                        stroke_width=0, fill_color=COCO, fill_opacity=0.85)
            t = VGroup(label(rf"{sh:.1f}\%", font_size=22, color=WHITE),
                       label(rf"\${e['quintile_food'][g]:,.0f}".replace(",", "{,}"), font_size=18,
                             color=GREY_A)).arrange(DOWN, buff=0.05).next_to(r, UP, buff=0.08)
            n = label(names[g], font_size=19, color=GREY_A).next_to(a.c2p(k + 0.5, 0), DOWN, buff=0.15)
            bars.add(VGroup(r, t, n))
        inc = e["quintile_income"]
        side = VGroup(
            label(r"food spending, \ 2024, \ by income fifth", font_size=26, color=COCO),
            label(rf"incomes about \${inc['lowest'] / 1000:.0f}k, \ \${inc['middle'] / 1000:.0f}k, "
                  rf"\${inc['highest'] / 1000:.0f}k", font_size=22, color=GREY_A),
            label(rf"the richest spend {e['quintile_food']['highest'] / e['quintile_food']['lowest']:.1f} times as "
                  rf"much on food, \\ with {inc['highest'] / inc['lowest']:.0f} times the income", font_size=24),
            label(rf"elasticity, \ poorest to middle: \ {e['el_bottom_middle']:.2f}", font_size=24, color=HICKS),
            label(rf"elasticity, \ middle to richest: \ {e['el_middle_top']:.2f}", font_size=24, color=HICKS),
            label(r"(more eating out, \ dearer food: \ quality rises too)", font_size=21, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        tag = data_tag(r"USDA ERS (2026), from the BLS Consumer Expenditure Survey, 2024", corner=DR, font_size=13)
        with self.voiceover(
            "The same law holds across households at one moment. <bookmark mark='a'/> In 2024 the poorest fifth of "
            "American households spent a third of their income on food; the middle fifth, twelve percent; the "
            "richest fifth, six percent. <bookmark mark='b'/> The richest households spent about three times as "
            "much on food as the poorest, with about sixteen times the income. Read as an elasticity, that's about "
            "a third between the poorest and the middle, and a half between the middle and the richest, where "
            "money goes on restaurants and dearer food rather than more calories. <bookmark mark='c'/> An Engel "
            "curve is a demand curve for income instead of price, and its slope sorts goods into necessities, "
            "luxuries, and the inferior goods of chapter four."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.4), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeIn(side[3]), FadeIn(side[4]), FadeIn(side[5]))
            vo.wait_until("c")
            self.play(Indicate(bars[0][0], color=E.ACCENT))
        self.clear_scene()

    def hamilton(self):
        h = load("hamilton")
        from explainer.ai.viz import axes

        ax = axes([np.log10(120), np.log10(800)], [0.48, 0.76], x_length=6.0, y_length=4.8,
                  xticks=[np.log10(150), np.log10(300), np.log10(600)], yticks=[0.5, 0.6, 0.7],
                  xlabel=r"real income, \ as the official index measures it", ylabel=r"share spent on food",
                  font_size=17, xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:.2f}",
                  center=LEFT * 3.2 + DOWN * 0.35)
        a = ax.ax
        cols = [interpolate_color(ManimColor(IC), ManimColor(GIFF), k / (len(h["curves"]) - 1))
                for k in range(len(h["curves"]))]
        curves = VGroup()
        for k, (c, col) in enumerate(zip(h["curves"], cols)):
            pts = [a.c2p(np.log10(m), w) for m, w in zip(c["grid"], c["fit"])]
            ln = Line(pts[0], pts[-1], color=col, stroke_width=3.5)
            dots_ = VGroup(*[Dot(a.c2p(np.log10(m), w), radius=0.035, color=col, fill_opacity=0.7)
                             for m, w in zip(c["m"], c["w"]) if 120 <= m <= 800 and 0.48 <= w <= 0.76])
            tag_ = (label(rf"year {c['year']}", font_size=17, color=col).next_to(pts[-1], RIGHT, buff=0.08)
                    if k in (0, len(h["curves"]) - 1) else VectorizedPoint(pts[-1]))
            curves.add(VGroup(ln, dots_, tag_))
        rec = h["recovered"]
        rows = VGroup(*[label(rf"year {y}: \ planted {100 * h['bias'] * y:.0f}\%, \ recovered {100 * r:.1f}\%",
                              font_size=21, color=c_) for y, r, c_ in zip(h["years"][1:], rec[1:], cols[1:])]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.14)
        idea = VGroup(
            label(r"Hamilton's idea (2001)", font_size=27, color=HICKS),
            label(r"if the price index rises too fast, \ measured \\ real income understates true income:",
                  font_size=22),
            label(r"later households at the same measured income \\ are really richer, \ and spend less on food",
                  font_size=22, color=GREY_A),
            label(r"the Engel curve drifts down; \ the drift \\ divided by its slope is the index's error", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.35).to_edge(UP, buff=0.6)
        rows.next_to(idea, DOWN, buff=0.35).align_to(idea, LEFT)
        res = label(rf"per year: \ planted {100 * h['bias']:.1f}\%, \ recovered {100 * h['per_year']:.2f}\%",
                    font_size=24, color=HICKS).next_to(rows, DOWN, buff=0.25).align_to(idea, LEFT)
        tag = island_tag(r"simulated: six island surveys", corner=DR, font_size=13)
        with self.voiceover(
            "Engel's second sentence, that the food share measures the standard of living, became a tool for "
            "checking price indices in 2001. <bookmark mark='a'/> Bruce Hamilton's idea: if the official price "
            "index rises faster than the true cost of living, then real incomes deflated by it understate how rich "
            "people really are, more so every year. A household in a later year with the same measured real income "
            "is truly richer, so by Engel's law it spends a smaller share on food. <bookmark mark='b'/> So the Engel "
            "curve, drawn against measured income, drifts down from one survey to the next, and the drift divided "
            "by the curve's slope is the error in the index. <bookmark mark='c'/> On the Island we planted an index "
            "that overstates the cost of living by one percent a year, and drew six surveys four years apart. The "
            f"method recovers the error survey by survey, and {100 * h['per_year']:.2f} percent a year in all. "
            "<bookmark mark='d'/> On American data, Hamilton found the CPI overstating by about two point seven "
            "percent a year from 1974 to 1982 and nought point six from 1982 to 1991; Dora Costa, with the same "
            "idea, carried the estimates back to 1888. Ingvild Almås turned it on countries in 2012 and found that "
            "the price comparisons behind international incomes make poor countries look richer than they are."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(idea[0]))
            vo.wait_until("a")
            self.play(FadeIn(idea[1]), FadeIn(idea[2]), Create(curves[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c_) for c_ in curves[1:]], lag_ratio=0.4), FadeIn(idea[3]), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3), FadeIn(res), run_time=2.5)
            vo.wait_until("d")
            self.play(Indicate(res, color=E.ACCENT))
        self.clear_scene()
        self.costa()

    def costa(self):
        c = tables.COSTA_2001.data["bias_per_year"]
        hm = tables.COSTA_2001.data["hamilton_2001"]
        periods = [("1888--1919", c["1888-1919"], "Costa"), ("1919--1935", c["1919-1935"], "Costa"),
                   ("1960--1972", c["1960-1972"], "Costa"), ("1972--1982", c["1972-1982"], "Costa"),
                   ("1982--1994", c["1982-1994"], "Costa"), ("1974--1982", hm["1974-1982"], "Hamilton"),
                   ("1982--1991", hm["1982-1991"], "Hamilton")]
        from explainer.ai.viz import axes

        ax = axes([0, len(periods)], [-0.5, 3.0], x_length=10.0, y_length=4.2, xticks=None,
                  yticks=[0, 1, 2, 3], ylabel=r"CPI bias, \ points a year", font_size=18,
                  yfmt=lambda v: f"{v:.0f}", center=DOWN * 0.4)
        a = ax.ax
        bars = VGroup()
        for k, (lab, v, who) in enumerate(periods):
            col = HICKS if who == "Costa" else E.ACCENT
            r = Polygon(a.c2p(k + 0.15, 0), a.c2p(k + 0.85, 0), a.c2p(k + 0.85, v), a.c2p(k + 0.15, v),
                        stroke_width=0, fill_color=col, fill_opacity=0.85)
            t = label(rf"{v:+.1f}", font_size=20).next_to(r, UP if v >= 0 else DOWN, buff=0.06)
            n = VGroup(label(lab, font_size=16, color=GREY_A), label(who, font_size=15, color=col)).arrange(
                DOWN, buff=0.03).next_to(a.c2p(k + 0.5, -0.5), DOWN, buff=0.08)
            bars.add(VGroup(r, t, n))
        zero = Line(a.c2p(0, 0), a.c2p(len(periods), 0), color=GREY_B, stroke_width=1.5)
        head = label(r"How much the CPI overstated the cost of living, \ read from Engel curves", font_size=28).to_edge(
            UP, buff=0.45)
        tag = published_tag(r"Costa, JPE (2001); Hamilton, AER (2001), as Costa reports it", corner=DR, font_size=13)
        with self.voiceover(
            "Here are their estimates side by side. <bookmark mark='a'/> Almost no bias before 1919, some in the "
            "1920s and 30s, little in the 1960s, then a large overstatement in the inflation of the 1970s, in both "
            "studies the same two point seven points a year, and much less after. The Boskin Commission's 1996 "
            "range, from a completely different method, was nought point eight to one point six."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars], lag_ratio=0.3), run_time=4)
        self.clear_scene()

    def called(self):
        c = calls.CALLS["engel_1857"]
        e = load("engel")
        food = 100 * np.array(e["food_share"])
        cc = call_card(r"Ernst Engel", c.when,
                       r"the poorer a family, the larger the share of its spending that goes on food; that share "
                       r"measures a population's standard of living",
                       rf"America, 1929 to 2025: \ food at home {food[0]:.0f}\% $\to$ {food[-1]:.1f}\% of spending "
                       rf"as real spending per head grew {e['real_ratio']:.1f}-fold; \ 2024: \ poorest fifth "
                       rf"{100 * e['quintile_share']['lowest']:.0f}\% of income, \ richest "
                       rf"{100 * e['quintile_share']['highest']:.1f}\%", c.verdict, width=12.0,
                       font_size=25).move_to(UP * 0.4)
        foot = label(r"the oldest regularity in empirical economics, \ and still true", font_size=26,
                     color=E.ACCENT).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Engel (1857) via Zimmerman (1932); BEA via FRED; USDA ERS", corner=DR, font_size=13)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1857 Engel said that poorer families spend a larger share on food, "
            "and that the share measures a population's standard of living. <bookmark mark='b'/> A century and a "
            "half later, both halves hold: across American households in 2024, and across a century of American "
            "growth. <bookmark mark='c'/> It may be the oldest regularity in empirical economics, and it's still "
            "true."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(cc.stamp, scale=1.3))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()
