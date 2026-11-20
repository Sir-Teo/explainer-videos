from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403

GROUND = -3.0
UNIT = 1.0 / HEIGHT   # screen units per metre: a person of average income is one unit tall


class Hook(VoiceoverScene):
    def construct(self):
        self.parade()
        self.giants()
        self.question()
        self.title()
        self.objectives()

    def _bars(self, P):
        h = np.array(P["height"])
        bars = VGroup()
        for k, v in enumerate(h):
            x = -6.3 + 0.122 * k
            hh = max(v * UNIT, 0.015)
            col = BOTTOM if k < 50 else (MIDDLE if k < 90 else TOP)
            bars.add(Rectangle(width=0.1, height=hh, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(
                np.array([x, GROUND + hh / 2, 0])))
        return bars

    def parade(self):
        P = load("parade")
        bars = self._bars(P)
        ground = Line(LEFT * 6.8 + UP * GROUND, RIGHT * 6.8 + UP * GROUND, color=GREY_B, stroke_width=2)
        avg = DashedLine(LEFT * 6.8 + UP * (GROUND + HEIGHT * UNIT), RIGHT * 6.8 + UP * (GROUND + HEIGHT * UNIT),
                         color=GREY_D, stroke_width=1.5)
        avg_l = label(r"average income: \ average height, \ 1.7 m", font_size=16, color=GREY_A).next_to(
            avg, UP, buff=0.06).to_edge(LEFT, buff=0.3)
        clock_t = ValueTracker(0.0)
        clock = always_redraw(lambda: label(rf"minute {int(clock_t.get_value()):02d} of 60", font_size=26,
                                            color=E.ACCENT).to_corner(UL, buff=0.4).shift(DOWN * 0.9))
        intro = VGroup(
            label(r"Jan Pen, \ 1971: \ everyone marches past in one hour", font_size=26, color=WHITE),
            label(r"each person as tall as their income", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.4)

        def note(txt, k, col, up=0.35):
            b = bars[k]
            return label(txt, font_size=16, color=col).next_to(b, UP, buff=up)
        n10 = note(rf"minute 6: \ {P['h_p10'] * 100:.0f} cm", 9, BOTTOM)
        n50 = note(rf"half past: \ the median, \ {P['h_median']:.2f} m", 49, BOTTOM)
        n70 = note(rf"minute {P['minute_mean']:.0f}: \ at last, \ average height", P["pct_mean"] - 1, MIDDLE, 0.6)
        n90 = note(rf"minute 54: \ {P['h_p90']:.1f} m", 89, TOP, 0.2)
        n99 = label(rf"the last 36 seconds: \ {P['h_p99']:.0f} m, \ then {P['h_p100']:.0f} m", font_size=18,
                    color=TOP).move_to(LEFT * 1.0 + UP * 1.6)
        who = label(r"one marcher for each percentile \\ of American families raising \\ children, \ around 2000",
                    font_size=20, color=GREY_A).move_to(LEFT * 2.6 + UP * 1.0)
        tag = data_tag(r"parents' family income by percentile, \ 1996--2000, \ 2012 dollars: \ Chetty et al. "
                       r"(2014), \ Opportunity Insights", corner=DR, font_size=11)
        with self.voiceover(
            "In 1971 the Dutch economist Jan Pen asked his readers to watch a parade. <bookmark mark='a'/> Everyone "
            "in the country marches past in exactly one hour, and each person is as tall as their income: someone "
            "with the average income is of average height. Here are American families raising children around the "
            "year 2000, one marcher for each percentile, from the tax records. <bookmark mark='b'/> For the first "
            f"minutes the marchers barely reach your ankles: at minute six they are {P['h_p10'] * 100:.0f} "
            "centimetres tall. <bookmark mark='c'/> At half past, the median family goes by, at "
            f"{P['h_median']:.2f} metres, well below average height. <bookmark mark='d'/> You wait until minute "
            f"{P['minute_mean']:.0f} before anyone of average height appears. <bookmark mark='e'/> Then the giants: "
            f"{P['h_p90']:.1f} metres at minute fifty-four, <bookmark mark='f'/> {P['h_p99']:.0f} metres in the last "
            f"minute, and in the final seconds the top percentile, {P['h_p100']:.0f} metres tall on average."
        ) as vo:
            self.add(clock)
            self.play(FadeIn(intro), Create(ground), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(avg), FadeIn(avg_l))
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[:3]], lag_ratio=0.5),
                      clock_t.animate.set_value(2), FadeIn(who), run_time=3.0, rate_func=linear)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[3:10]], lag_ratio=0.5),
                      clock_t.animate.set_value(6), FadeIn(n10), run_time=3.0, rate_func=linear)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[10:50]], lag_ratio=0.5),
                      clock_t.animate.set_value(30), FadeIn(n50), run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[50:P["pct_mean"]]], lag_ratio=0.5),
                      clock_t.animate.set_value(P["minute_mean"]), FadeIn(n70), run_time=3.0, rate_func=linear)
            vo.wait_until("e")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[P["pct_mean"]:90]], lag_ratio=0.5),
                      clock_t.animate.set_value(54), FadeIn(n90), FadeOut(who), run_time=3.0, rate_func=linear)
            vo.wait_until("f")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[90:]], lag_ratio=0.5),
                      clock_t.animate.set_value(60), FadeIn(n99), run_time=3.0, rate_func=linear)
        self.wait(0.5)
        self.clear_scene()

    def giants(self):
        P = load("parade")
        rows = [(r"the median family", P["h_median"], BOTTOM),
                (r"average height: \ the mean income", HEIGHT, MIDDLE),
                (r"the 99th percentile of families", P["h_p99"], TOP),
                (r"the top 1\% of tax units, \ 2022", P["h_top1"], TOP),
                (r"the top 0.1\%", P["h_top01"], TOP),
                (r"the top 0.01\%", P["h_top001"], LOSS)]
        ax = plane([-0.3, 3.2], [0, 7], center=RIGHT * 1.6 + DOWN * 0.2, x_length=7.4, y_length=5.6,
                   xticks=[0, 1, 2, 3], yticks=[], xlabel=r"height in metres \ (log scale)",
                   xfmt=lambda v: f"{10 ** v:g}", font_size=14)
        bars = VGroup()
        for k, (nm, h, col) in enumerate(rows):
            y = 6.3 - 1.05 * k
            x1 = np.log10(h)
            p0, p1 = ax.ax.c2p(-0.3, y - 0.32), ax.ax.c2p(x1, y + 0.32)
            r = Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            v = label(f"{h:.1f} m" if h < 10 else f"{h:.0f} m", font_size=18, color=WHITE).next_to(r, RIGHT,
                                                                                                buff=0.12)
            n = label(nm, font_size=18, color=col).next_to(ax.ax.c2p(-0.3, y), LEFT, buff=0.2)
            bars.add(VGroup(r, v, n))
        foot = label(rf"the top 0.01\%: \ {P['ratio_top001']:.0f} times the average income, \ about "
                     rf"\${P['inc_top001'] / 1e6:.0f} million a year", font_size=20, color=LOSS).to_edge(DOWN,
                                                                                                    buff=0.35)
        tag = data_tag(r"Opportunity Insights; \ Piketty and Saez, \ updated to 2022", corner=DR, font_size=11)
        with self.voiceover(
            "And Pen's parade does not end there, because the top percentile is itself unequal. Take the tax "
            "records for 2022 and put everyone on one scale. <bookmark mark='a'/> The median family is a little "
            "over a metre tall, and average height is one metre seventy. <bookmark mark='b'/> The richest one "
            f"percent of tax units average about {P['h_top1']:.0f} metres; <bookmark mark='c'/> the richest one in a "
            f"thousand, about {P['h_top01']:.0f} metres. <bookmark mark='d'/> And the richest one in ten thousand, "
            f"with {P['ratio_top001']:.0f} times the average income, about {P['inc_top001'] / 1e6:.0f} million "
            f"dollars a year, are over {round(P['h_top001'], -2):.0f} metres tall, taller than any building in "
            "America. Their heads are in the clouds."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(bars[0]), FadeIn(bars[1]), run_time=1.5)
            for mk, b_ in zip("bcd", bars[3:]):
                vo.wait_until(mk)
                if mk == "b":
                    self.play(FadeIn(bars[2]), FadeIn(b_))
                else:
                    self.play(FadeIn(b_))
            self.play(FadeIn(foot))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 38, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how should inequality be measured, \ and what does each measure hide?", font_size=26,
                  color=LORENZ),
            label(r"why do incomes and wealth have such long tails, \ and why did they grow?", font_size=26,
                  color=TOP),
            label(r"do children escape where they started, \ and where in America do they?", font_size=26,
                  color=CHILD),
            label(r"what has happened to the world's distribution, \ and does it matter?", font_size=26,
                  color=MIDDLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "This part asks how unequal incomes and wealth are, why, and whether children escape where they "
            "started. <bookmark mark='a'/> How should inequality be measured, and what does each measure hide? "
            "<bookmark mark='b'/> Why do incomes and wealth have such long tails, and why did the tails grow? "
            "<bookmark mark='c'/> Do children escape their parents' place in the parade, and in which parts of "
            "America do they? <bookmark mark='d'/> And what has happened to the distribution of the whole world, "
            "and does any of it matter?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1913, 2022], [5, 21], x_length=4.2, y_length=1.4)
        logo = path(mini, F["t"], F["v"], TOP, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 40 \ $\cdot$ \ Inequality and Mobility", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty: inequality and mobility."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VIII \ $\cdot$ \ Work and the State", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"a game; \ measures and their ethics; \ a century of top incomes",
            r"Pareto tails from random growth, \ and why they moved so fast",
            r"wealth and $r - g$; \ Kuznets's curve",
            r"mobility: \ the elasticity, \ forty million tax records, \ places",
            r"the world; \ does it matter; \ two dials; \ distributional tables; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> A game, then the measures and the ethics inside them, and a "
            "century of top incomes. <bookmark mark='b'/> Where Pareto's long tails come from, and why they moved so "
            "fast. <bookmark mark='c'/> Wealth, and Piketty's r against g; Kuznets's curve. <bookmark mark='d'/> "
            "Then mobility: the elasticity between generations, forty million tax records, and the places where "
            "children rise. <bookmark mark='e'/> Finally the world, whether inequality matters, two dials, the "
            "distributional tables that analysts build, and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
