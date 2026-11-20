from __future__ import annotations

from videos.economics.econ42.common import *  # noqa: F403


class Measure(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Measuring both sides", r"How much do benefits lengthen unemployment, and smooth consumption?",
             "Chapter four. Measuring both sides.", lit={1990: r"Meyer", 1997: r"Gruber",
                                                        2007: r"Card, \ Chetty and Weber",
                                                        2019: r"Ganong and Noel"},
             scale=("person", "nation"), horizon=("a week", "a year"))
        self.hazard()
        self.studies()
        self.consumption()
        self.verdict()

    def hazard(self):
        W = load("weekly")
        h = np.array(W["hazard"])
        wk = np.arange(len(h))
        ax = plane([0, 60], [0, 0.16], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 10, 20, 26, 40, 50, 60], yticks=[0, 0.04, 0.08, 0.12, 0.16],
                   xlabel=r"weeks of unemployment", ylabel=r"chance of finding a job this week",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, wk, h, HAZARD, 3.4, smooth=False)
        ex = vline(ax, W["K"], 0, 0.16, UNEMP)
        exl = label(rf"benefits end: \ week {W['K']}", font_size=16, color=UNEMP).next_to(ax.ax.c2p(W["K"], 0.16),
                                                                                       RIGHT, buff=0.1)
        side = VGroup(
            label(rf"the Island: \ half the wage \\ for {W['K']} weeks, \ then a fifth; \\ no savings", font_size=17,
                  color=GREY_A),
            label(rf"week 1: \ {100 * W['h0']:.1f}\%; \\ the last week and after: \\ {100 * W['h_after']:.1f}\%",
                  font_size=18, color=HAZARD),
            label(rf"average spell: \ {W['duration']:.1f} weeks", font_size=18, color=WHITE),
            label(rf"a 10\% higher benefit: \\ spells {100 * W['ten_pct']:.1f}\% longer \\ (elasticity "
                  rf"{W['level']:.2f})", font_size=18, color=COST),
            label(rf"30 weeks instead of 20: \\ {100 * -W['ccw']:.0f}\% fewer find work \\ in the first 20",
                  font_size=18, color=COST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "First, the cost side: how much do benefits lengthen unemployment? Watch a worker on the Island, week "
            f"by week. <bookmark mark='a'/> Benefits pay half the wage for {W['K']} weeks, then only a floor. "
            "<bookmark mark='b'/> In the first week the chance of finding a job is "
            f"{say_pct(W['h0'], 1)}. As the end of benefits approaches, the worker searches harder, and in the last "
            f"week and after it is {say_pct(W['h_after'], 1)}. Bruce Meyer saw this in American data in 1990: the "
            "chance of leaving unemployment jumps when benefits are about to lapse. "
            f"<bookmark mark='c'/> The average spell lasts {W['duration']:.1f} weeks. <bookmark mark='d'/> Raise "
            f"the benefit by ten percent, and spells lengthen by {say_pct(W['ten_pct'], 1)}: an elasticity of "
            f"{W['level']:.2f}. <bookmark mark='e'/> Pay benefits for thirty weeks instead of twenty, and "
            f"{say_pct(-W['ccw'], 0)} fewer find work in the first twenty weeks."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(ex), FadeIn(exl), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(side[1]), run_time=2.5)
            for mk, k in zip("cde", range(2, 5)):
                vo.wait_until(mk)
                self.play(FadeIn(side[k]))
        self.clear_scene()

    def studies(self):
        U = tables.UI_EVIDENCE.data
        rows = [(r"Meyer (1990), \ United States", rf"a 10\% higher benefit: \ spells {U['meyer_lo'] * 10:.0f}--"
                                                  rf"{U['meyer_hi'] * 10:.0f}\% longer", COST),
                (r"Card, \ Chetty and Weber (2007), \ Austria", rf"30 weeks instead of 20: \ job finding "
                                                               rf"{U['ccw_ext_lo']}--{U['ccw_ext_hi']}\% lower",
                 COST),
                (r"the same study", rf"severance of two months' pay: \ job finding {U['ccw_severance_lo']}--"
                                    rf"{U['ccw_severance_hi']}\% lower", LIQ),
                (r"Schmieder, \ von Wachter and Bender (2012), \ Germany", r"age thresholds for longer benefits: "
                                                                          r"\ effects at most \\ somewhat smaller "
                                                                          r"in recessions", COST)]
        tbl = VGroup(*[VGroup(label(a, font_size=20, color=WHITE), label(b, font_size=20, color=c)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1) for a, b, c in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        tbl.move_to(DOWN * 0.1)
        head = label(r"the cost side, \ measured", font_size=28, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(tables.UI_EVIDENCE.tag, corner=DR, font_size=10)
        with self.voiceover(
            "In real economies the same numbers have been measured many ways. <bookmark mark='a'/> In America, "
            "comparing workers in states and years with different benefits, a ten percent higher benefit "
            "lengthens spells by four to eight percent. <bookmark mark='b'/> In Austria, David Card, Raj Chetty and "
            "Andrea Weber compared workers just either side of the work record that entitled them to thirty weeks of "
            "benefits rather than twenty: job finding in the first twenty weeks was five to nine percent lower. "
            "<bookmark mark='c'/> The same design, at three years in a job, the cutoff for severance pay, found that a "
            "lump sum of two "
            "months' earnings lowered job finding by eight to twelve percent. A lump sum does not reward staying "
            "unemployed; that finding matters in chapter five. <bookmark mark='d'/> In Germany, Johannes Schmieder, "
            "Till von Wachter and Stefan Bender used the ages at which longer benefits begin, year after year, and "
            "found the effects at most somewhat smaller in recessions, when extensions also reach more people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tbl[0]))
            for mk, r_ in zip("bcd", tbl[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def consumption(self):
        U = tables.UI_EVIDENCE.data
        items = [(r"Gruber (1997): \ on losing a job", -U["gruber_drop"], SMOOTH),
                 (r"Gruber: \ without benefits \ (over 3 times)", -3 * U["gruber_drop"], LOSS),
                 (r"Ganong and Noel (2019): \ at the start", -U["gn_onset"], SMOOTH),
                 (r"Ganong and Noel: \ when benefits run out", -U["gn_exhaust"], LOSS)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(items):
            y = 1.5 - 1.05 * k
            w = abs(v) * 0.22
            r = Rectangle(width=w, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([0.6 - w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=19, color=WHITE).next_to(np.array([0.6 - w - 0.1, y, 0]), LEFT,
                                                                          buff=0.1),
                            r, label(rf"$-${abs(v):g}\%" if k != 1 else r"over $-$21\%", font_size=20,
                                     color=col).next_to(np.array([0.7, y, 0]), RIGHT, buff=0.1)))
        head = label(r"the gain side: \ how far consumption falls", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                  buff=0.5)
        foot = label(rf"each 10 points of replacement: \ a fall {U['gruber_slope']}\% smaller \ (Gruber)",
                     font_size=19, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.UI_EVIDENCE.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Now the gain side: how far does consumption fall? <bookmark mark='a'/> In 1997 Jonathan Gruber used "
            "food spending in the Panel Study of Income Dynamics: on losing a job, families cut it by about seven "
            "percent on average, <bookmark mark='b'/> and without unemployment benefits the fall would have been "
            "more than three times as large. Each ten points of replacement made the fall about 2.7 percent smaller. "
            "<bookmark mark='c'/> In 2019 Peter Ganong and Pascal Noel used bank accounts, which record all "
            "spending month by month: about six percent at the start of unemployment, <bookmark mark='d'/> and then "
            "about twelve percent more in the month benefits run out, a larger drop than in all the months before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(bars[0]), FadeIn(foot))
            for mk, b_ in zip("bcd", bars[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(b_[0]), GrowFromEdge(b_[1], RIGHT), FadeIn(b_[2]))
        self.clear_scene()

    def verdict(self):
        F = load("formula")
        g, ex = F["need"]["gruber"], F["need"]["exhaust"]
        rows = VGroup(
            MathTex(r"\gamma \;=\; \frac{\varepsilon}{\Delta c / c}", font_size=44),
            label(rf"with Gruber's 7\% drop and $\varepsilon$ from 0.4 to 0.8: \ risk aversion of "
                  rf"{g[0]:.1f} to {g[1]:.1f}", font_size=22, color=SMOOTH),
            label(r"most estimates of risk aversion are far lower \ (Part 7): \ by this measure, \ benefit levels "
                  r"look high enough", font_size=21, color=GREY_A),
            label(rf"with the 12\% drop at exhaustion: \ {ex[0]:.1f} to {ex[1]:.1f}: \ the case for "
                  r"longer benefits is stronger", font_size=22, color=LOSS),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.2)
        head = label(r"what risk aversion would justify the benefits?", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        tag = published_tag(tables.UI_EVIDENCE.tag, corner=DR, font_size=10)
        with self.voiceover(
            "Put the numbers in the formula, rearranged to ask what risk aversion would make today's benefits "
            "right. <bookmark mark='a'/> With a seven percent drop and an elasticity between 0.4 and 0.8, the answer "
            f"is a risk aversion of {g[0]:.1f} to {g[1]:.1f}. <bookmark mark='b'/> That is high: most estimates "
            "are lower. Gruber drew the same conclusion: the benefit levels of his time were justified only at "
            "fairly high risk aversion. <bookmark mark='c'/> But the drop at exhaustion is larger, about twelve "
            f"percent, which needs only {ex[0]:.1f} to {ex[1]:.1f}. Ganong and Noel concluded that the gains from "
            "paying benefits for longer are several times the gains from paying more each week. And there is a "
            "deeper objection to the whole calculation, the subject of the next chapter."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(rows[0]))
            for mk, r_ in zip("abc", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
