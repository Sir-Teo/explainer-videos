from __future__ import annotations

from videos.economics.econ3.common import *  # noqa: F403

CAT_COLOR = {
    "employed full time or by choice part time": E.HOUSEHOLDS,
    "employed part time, wanting full time": "#2E9C93",
    "unemployed 15 weeks or more": E.MISS,
    "unemployed, lost a job in the last 15 weeks": "#F59A8F",
    "discouraged": "#C9A0FF",
    "marginally attached, other reasons": "#9D7CE0",
    "not in the labour force": GREY_C,
}
CAT_NAME = {
    "employed full time or by choice part time": r"working",
    "employed part time, wanting full time": r"part time, \ want full time",
    "unemployed 15 weeks or more": r"unemployed 15+ weeks",
    "unemployed, lost a job in the last 15 weeks": r"unemployed, \ recently",
    "discouraged": r"discouraged: \ want work, \ stopped looking",
    "marginally attached, other reasons": r"want work, \ not looking \ (other reasons)",
    "not in the labour force": r"not in the labour force",
}
RATE_DEF = {
    "U-1": r"unemployed 15+ weeks",
    "U-2": r"job losers",
    "U-3": r"all unemployed \ (the official rate)",
    "U-4": r"+ discouraged workers",
    "U-5": r"+ others who want work",
    "U-6": r"+ part time, want full time",
}


class Unemployment(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Unemployment is a survey", r"Who counts as unemployed, and who decides?",
             "Chapter eight. Unemployment is a survey.", lit=("households",), scale=("person", "nation"),
             horizon=("a month",))
        self.questions()
        self.island()
        self.six()
        self.america()
        self.missing()

    # ------------------------------------------------------------------
    def questions(self):
        q1 = label(r"Last week, did you do any work for pay, \ even an hour?", font_size=28)
        yes = label(r"employed", font_size=28, color=E.HOUSEHOLDS)
        q2 = label(r"In the last four weeks, have you looked for work, \\ and could you start?", font_size=28)
        unemp = label(r"unemployed", font_size=28, color=E.MISS)
        nilf = label(r"not in the labour force", font_size=28, color=GREY_B)
        q1.move_to(UP * 2.3 + LEFT * 1.2)
        yes.next_to(q1, RIGHT, buff=1.4)
        q2.move_to(UP * 0.4 + LEFT * 1.2)
        unemp.next_to(q2, RIGHT, buff=1.0)
        nilf.move_to(DOWN * 1.4 + LEFT * 1.2)
        arrows = VGroup(
            Arrow(q1.get_right(), yes.get_left(), buff=0.15, color=E.HOUSEHOLDS, stroke_width=3),
            Arrow(q1.get_bottom(), q2.get_top(), buff=0.15, color=GREY_B, stroke_width=3),
            Arrow(q2.get_right(), unemp.get_left(), buff=0.15, color=E.MISS, stroke_width=3),
            Arrow(q2.get_bottom(), nilf.get_top(), buff=0.15, color=GREY_B, stroke_width=3),
        )
        yn = VGroup(label(r"yes", font_size=20, color=E.HOUSEHOLDS).next_to(arrows[0], UP, buff=0.05),
                    label(r"no", font_size=20, color=GREY_B).next_to(arrows[1], LEFT, buff=0.1),
                    label(r"yes", font_size=20, color=E.MISS).next_to(arrows[2], UP, buff=0.05),
                    label(r"no", font_size=20, color=GREY_B).next_to(arrows[3], LEFT, buff=0.1))
        rate = MathTex(r"\text{unemployment rate} = \frac{\text{unemployed}}{\text{employed} + \text{unemployed}}",
                       font_size=36).to_edge(DOWN, buff=0.5)
        ui = label(r"unemployment insurance plays no part", font_size=22, color=GREY_A).next_to(rate, UP, buff=0.3)
        tag = published_tag(r"BLS, Current Population Survey: concepts and definitions", corner=DR, font_size=16)
        cps = study_card(r"The Current Population Survey", r"Census Bureau, for the Bureau of Labor Statistics",
                         [(r"who", r"about 60,000 households, every month"), (r"how", r"interviews, in person and "
                                                                                   r"by phone"),
                          (r"when", r"the week that includes the 12th of the month")],
                         design="survey", width=8.0, font_size=26).move_to(UP * 0.2)
        with self.voiceover(
            "The unemployment rate isn't counted from claims for benefits. It comes from a survey. Every month "
            "the Census Bureau interviews about sixty thousand American households for the Bureau of Labor "
            "Statistics, and sorts every adult with two questions. <bookmark mark='a'/> Last week, did you do any "
            "work for pay, even an hour? If yes, you're employed. <bookmark mark='b'/> If not: in the last four "
            "weeks, have you looked for work, and could you start? If yes, you're unemployed. <bookmark mark='c'/> "
            "If not, you're not in the labour force at all: retired, studying, caring for family, or simply not "
            "looking. <bookmark mark='d'/> The unemployment rate is the unemployed as a share of everyone working "
            "or looking. Whether you claim unemployment insurance plays no part."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cps, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(cps))
            self.play(FadeIn(q1), GrowArrow(arrows[0]), FadeIn(yn[0]), FadeIn(yes))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), FadeIn(yn[1]), FadeIn(q2))
            self.play(GrowArrow(arrows[2]), FadeIn(yn[2]), FadeIn(unemp))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[3]), FadeIn(yn[3]), FadeIn(nilf))
            vo.wait_until("d")
            self.play(Write(rate), FadeIn(ui))
        self.clear_scene()

    def island(self):
        d = load("unemployment")
        cats = d["survey"]
        people = VGroup()
        colors = []
        for name, n in cats:
            colors += [CAT_COLOR[name]] * n
        rng = np.random.default_rng(3)
        order = rng.permutation(len(colors))
        for k in range(len(colors)):
            people.add(person(0.38, color=GREY_B))
        people.arrange_in_grid(5, 20, buff=(0.16, 0.18)).move_to(UP * 1.3)
        dara = islander("dara", 0.9, name=True).to_corner(UL, buff=0.4)
        head = label(r"Dara asks the Island's 100 adults the same questions", font_size=26, color=DARA)
        head.next_to(dara, RIGHT, buff=0.3)
        legend = VGroup()
        for name, n in cats:
            legend.add(VGroup(Square(0.2, stroke_width=0, fill_color=CAT_COLOR[name], fill_opacity=1),
                              label(rf"{CAT_NAME[name]}: \ {n}", font_size=19, color=CAT_COLOR[name])).arrange(
                RIGHT, buff=0.1))
        legend.arrange_in_grid(4, 2, buff=(0.5, 0.14), col_alignments="ll").to_edge(DOWN, buff=1.5)
        sums = VGroup(
            label(rf"employed {d['employed']}, \ unemployed {d['unemployed']}: \ labour force {d['labour_force']}",
                  font_size=24),
            label(rf"U-3 $= {d['unemployed']}/{d['labour_force']} =$ {pct(d['island']['U-3'], 1)} \qquad "
                  rf"participation {pct(d['participation'], 0)} \qquad employed {pct(d['employment_ratio'], 0)} of "
                  r"adults", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.35)
        tag = island_tag(r"simulated: the Island, year 3", corner=DR, font_size=15).shift(UP * 0.9)
        with self.voiceover(
            "On the Island, Dara runs the same survey, on all hundred adults. <bookmark mark='a'/> Here they "
            "are. <bookmark mark='b'/> Sixty-two worked last week, four of them part time though they wanted full "
            "time. Five looked for work and found none, two of them for more than fifteen weeks. Four more "
            "wanted work but weren't looking: two because they'd given up, two for other reasons. And twenty-nine "
            "didn't want a job: the old, the young in school, people caring for family. <bookmark mark='c'/> "
            f"Sixty-two employed and five unemployed make a labour force of sixty-seven, and the unemployment "
            f"rate is five out of sixty-seven: {say_pct(d['island']['U-3'])}."
        ) as vo:
            self.play(FadeIn(dara), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=0.6) for p in people], lag_ratio=0.01), run_time=1.6)
            vo.wait_until("b")
            self.play(*[p.animate.set_color(colors[order[k]]) for k, p in enumerate(people)], run_time=1.5)
            self.play(LaggedStart(*[FadeIn(l) for l in legend], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(sums, shift=UP * 0.1))
        self.clear_scene()

    def _ladder(self, rates, x, title, color, scale, fmt):
        g = VGroup()
        head = label(title, font_size=26, color=color)
        g.add(head)
        bars = VGroup()
        for i, k in enumerate(("U-1", "U-2", "U-3", "U-4", "U-5", "U-6")):
            v = rates[k]
            r = Rectangle(width=max(v * scale, 0.02), height=0.42, stroke_width=0,
                          fill_color=E.ACCENT if k == "U-3" else color, fill_opacity=0.85)
            r.move_to([x + v * scale / 2, 1.9 - 0.7 * i, 0])
            t = label(fmt(v), font_size=22).next_to(r, RIGHT, buff=0.1)
            bars.add(VGroup(r, t))
        head.move_to([x + 1.2, 2.7, 0])
        g.add(bars)
        g.bars = bars
        return g

    def six(self):
        d = load("unemployment")
        isl = self._ladder(d["island"], -1.6, r"the Island", E.ISLAND, 24.0, lambda v: pct(v, 1))
        names = VGroup()
        for i, k in enumerate(("U-1", "U-2", "U-3", "U-4", "U-5", "U-6")):
            t = VGroup(label(k, font_size=24, color=E.ACCENT if k == "U-3" else WHITE),
                       label(RATE_DEF[k], font_size=19, color=GREY_A)).arrange(RIGHT, buff=0.2)
            t.move_to([-2.0, 1.9 - 0.7 * i, 0], aligned_edge=RIGHT)
            names.add(t)
        tag = island_tag(r"simulated: the Island, year 3; BLS's definitions", corner=DR, font_size=15)
        with self.voiceover(
            "But which people count as unemployed is a choice, so the Bureau of Labor Statistics publishes six "
            "rates, from narrow to broad. Here they are for the Island. <bookmark mark='a'/> U-1 counts only the "
            "long-term unemployed: three percent. U-2, only people who lost a job. <bookmark mark='b'/> U-3 is the "
            f"official rate, {say_pct(d['island']['U-3'])}. <bookmark mark='c'/> U-4 adds the "
            "discouraged, who want work but have given up looking. U-5 adds everyone else who wants a job and "
            "isn't looking. <bookmark mark='d'/> And U-6 adds the people working part time who want full time. "
            f"On the Island it's {say_pct(d['island']['U-6'])}: same people, same week, and a rate more than twice "
            "as high."
        ) as vo:
            self.play(FadeIn(isl[0]), FadeIn(tag))
            vo.wait_until("a")
            for i in (0, 1):
                self.play(FadeIn(names[i]), GrowFromEdge(isl.bars[i][0], LEFT), FadeIn(isl.bars[i][1]))
            vo.wait_until("b")
            self.play(FadeIn(names[2]), GrowFromEdge(isl.bars[2][0], LEFT), FadeIn(isl.bars[2][1]))
            vo.wait_until("c")
            for i in (3, 4):
                self.play(FadeIn(names[i]), GrowFromEdge(isl.bars[i][0], LEFT), FadeIn(isl.bars[i][1]))
            vo.wait_until("d")
            self.play(FadeIn(names[5]), GrowFromEdge(isl.bars[5][0], LEFT), FadeIn(isl.bars[5][1]))
        self.clear_scene()

    def america(self):
        d = load("unemployment")
        us = d["us"]
        h = d["history"]
        rates = VGroup()
        for i, k in enumerate(("U-1", "U-2", "U-3", "U-4", "U-5", "U-6")):
            rates.add(VGroup(label(k, font_size=22, color=E.ACCENT if k == "U-3" else GREY_A),
                             label(rf"{us[k]:.1f}\%", font_size=24)).arrange(RIGHT, buff=0.2))
        rates.arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_corner(UR, buff=0.5).shift(DOWN * 0.4)
        rh = label(r"October 2026", font_size=24, color=E.ACCENT).next_to(rates, UP, buff=0.25)
        xs = [int(m[:4]) + (int(m[5:7]) - 0.5) / 12 for m in h["months"]]
        ax = year_axis([1994, 2027], [0, 24], x_length=8.8, y_length=4.6, xticks=list(range(1995, 2030, 5)),
                       yticks=[0, 5, 10, 15, 20], yfmt=lambda v: f"{v:.0f}\\%", ylabel=r"percent",
                       center=LEFT * 1.8 + DOWN * 0.4)
        a = ax.ax

        def series(vals, col):
            pts = [a.c2p(x, v) for x, v in zip(xs, vals) if np.isfinite(v)]
            return VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts)

        u3 = series(h["u3"], E.ACCENT)
        u6 = series(h["u6"], "#C9A0FF")
        l3 = label(r"U-3", font_size=22, color=E.ACCENT).next_to(a.c2p(2026.8, h["u3"][-1]), RIGHT, buff=0.1)
        l6 = label(r"U-6", font_size=22, color="#C9A0FF").next_to(a.c2p(2026.8, h["u6"][-1]), RIGHT, buff=0.1)
        part = label(rf"participation: \\ {d['CIVPART']['last']:.1f}\% \\ (peak {d['CIVPART']['peak']:.1f}\%, "
                     rf"{d['CIVPART']['peak_month'][:4]})", font_size=22, color=GREY_A)
        part.next_to(rates, DOWN, buff=0.6).align_to(rates, LEFT)
        tag = data_tag(rf"BLS, Current Population Survey (U1RATE ... U6RATE, UNRATE, CIVPART), "
                       rf"{data.fred_cite('U6RATE')}", corner=DL, font_size=14)
        with self.voiceover(
            "In the United States, in October 2026, the six rates ran from <bookmark mark='a'/> "
            f"{us['U-1']:.1f} percent, for U-1, to {us['U-6']:.1f} percent for U-6, with the official rate at "
            f"{us['U-3']:.1f}. <bookmark mark='b'/> Since 1994, when the broad rates begin, U-3 and U-6 have moved "
            "together, the broad one roughly double the narrow one, both soaring in 2009 and in the spring of "
            "2020. <bookmark mark='c'/> One more number keeps them honest: the share of adults in the labour "
            f"force at all. It peaked at {d['CIVPART']['peak']:.1f} percent in {d['CIVPART']['peak_month'][:4]} and "
            f"is {d['CIVPART']['last']:.1f} now, partly because the population is older. The unemployment rate "
            "can fall because people find jobs, or because they stop looking."
        ) as vo:
            self.play(FadeIn(rh), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in rates], lag_ratio=0.15))
            vo.wait_until("b")
            self.play(FadeIn(ax))
            self.play(Create(u6, rate_func=linear), Create(u3, rate_func=linear), run_time=3.0)
            self.play(FadeIn(l3), FadeIn(l6))
            vo.wait_until("c")
            self.play(FadeIn(part))
        self.clear_scene()

    def missing(self):
        d = load("unemployment")
        n = d["months_total"]
        grid = VGroup(*[Square(0.128, stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.75) for _ in range(n)])
        grid.arrange_in_grid(rows=12, buff=0.03, flow_order="dr")
        grid.move_to(UP * 0.5)
        years = VGroup(*[label(str(1948 + c), font_size=19, color=GREY_B).next_to(grid[12 * c], UP, buff=0.12)
                         for c in range(0, 79, 12)])
        mlab = VGroup(label(r"Jan", font_size=17, color=GREY_B).next_to(grid[0], LEFT, buff=0.12),
                      label(r"Dec", font_size=17, color=GREY_B).next_to(grid[11], LEFT, buff=0.12))
        miss_i = d["months_total"] - 13          # October 2025: thirteen months before October 2026
        hole = grid[miss_i]
        ring = Circle(radius=0.32, stroke_color=E.MISS, stroke_width=4).move_to(hole)
        pointer = Arrow(hole.get_center() + DOWN * 1.6 + LEFT * 1.2, hole.get_center() + DOWN * 0.3 + LEFT * 0.2,
                        buff=0.05, color=E.MISS, stroke_width=3, max_tip_length_to_length_ratio=0.15)
        head = label(rf"every month since January 1948: \ {n} squares", font_size=28).to_edge(UP, buff=0.4)
        cap = label(r"October 2025: \ the household survey was not conducted \\ during the federal government "
                    r"shutdown. \ The rate for that month does not exist.", font_size=24, color=E.MISS)
        cap.to_edge(DOWN, buff=0.6)
        tag = data_tag(rf"BLS via FRED (UNRATE), {data.fred_cite('UNRATE')}", corner=DL, font_size=15)
        with self.voiceover(
            "A survey has to be taken to exist. <bookmark mark='a'/> Here is every month since January 1948, a "
            f"square each: {n} of them, and every one has an unemployment rate, <bookmark mark='b'/> except one. "
            "In October 2025, during a shutdown of the federal government, the household survey wasn't carried "
            "out. There is no unemployment rate for that month, and there never will be. <bookmark mark='c'/> The "
            "number we treat as a fact of nature is the work of interviewers knocking on doors, and when they "
            "stop, it stops."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.0015), FadeIn(years), FadeIn(mlab),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(hole.animate.set_fill(BACKGROUND, opacity=1), Create(ring), GrowArrow(pointer))
            self.play(FadeIn(cap))
            vo.wait_until("c")
            self.play(Indicate(ring, color=E.MISS, scale_factor=1.4))
        self.clear_scene()
