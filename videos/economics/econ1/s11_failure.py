from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403

Y29 = "#F2B84B"  # the Depression
Y08 = WHITE  # the financial crisis


class Failure(VoiceoverScene):
    def construct(self):
        card(self, 9, r"When the order fails", r"How badly can the whole system fail, \ and did anyone see it "
             r"coming?", "Chapter nine. When the order fails.", lit={1929: r"the crash", 2008: r"the financial crisis"},
             scale=("nation", "world"), horizon=("a year", "a decade"))
        self.four_charts()
        self.called_it()
        self.letter()

    # ------------------------------------------------------------------
    def panel_chart(self, title, x, ys, y_range, yticks, center, xmax=60, xlabel=r"months after the peak", yfmt=None):
        ax = axes([0, xmax], y_range, x_length=5.2, y_length=2.35, xticks=[0, xmax // 2, xmax], yticks=yticks,
                  xlabel=xlabel, font_size=16, center=center, yfmt=yfmt)
        t = label(title, font_size=22, color=GREY_A).next_to(ax.ax, UP, buff=0.1).align_to(ax.ax, LEFT)
        lines = VGroup(*[curve(ax.ax, x, y, col, 3.5) for y, col in zip(ys, (Y29, Y08))])
        g = VGroup(ax, t)
        g.lines, g.ax = lines, ax
        return g

    def four_charts(self):
        c = load("collapses")
        m = c["months"]
        ip = self.panel_chart(r"industrial production \ (peak $=100$)", m, (c["ip29"], c["ip07"]), [40, 110],
                              [40, 60, 80, 100], [-3.4, 1.55, 0])
        un = self.panel_chart(r"unemployment rate, \%", m, (c["u29"], c["u07"]), [0, 28], [0, 10, 20],
                              [3.4, 1.55, 0])
        cp = self.panel_chart(r"consumer prices \ (peak $=100$)", m, (c["cpi29"], c["cpi07"]), [70, 110],
                              [70, 80, 90, 100, 110], [-3.4, -2.05, 0])
        gd = self.panel_chart(r"real GDP \ (peak year $=100$)", c["gdp_years"], (c["gdp29"], c["gdp07"]), [70, 110],
                              [70, 80, 90, 100, 110], [3.4, -2.05, 0], xmax=7, xlabel=r"years after the peak year")
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=Y29, stroke_width=5),
                            label(r"from August 1929", font_size=20, color=Y29)).arrange(RIGHT, buff=0.12),
                     VGroup(Line(ORIGIN, RIGHT * 0.4, color=Y08, stroke_width=5),
                            label(r"from December 2007", font_size=20, color=Y08)).arrange(RIGHT, buff=0.12))
        leg.arrange(RIGHT, buff=0.8).to_corner(UR, buff=0.15)
        src = VGroup(note(r"data: FRED, retrieved 18 Nov 2026: Federal Reserve (IP), BLS (CPI;", font_size=14,
                          color=E.SOURCE),
                     note(r"unemployment from 1948), NBER m08292a (unemployment 1929-42), BEA (GDP)", font_size=14,
                          color=E.SOURCE)).arrange(DOWN, aligned_edge=LEFT, buff=0.04).to_corner(UL, buff=0.15)
        with self.voiceover(
            "Bastiat's order works well enough to feed a city every day. It doesn't always work. Here are the two "
            "worst failures of the last hundred years, side by side, each measured from the month the economy "
            "peaked. <bookmark mark='a'/> Industrial production: after August 1929, American factories cut their "
            f"output by {100 - c['ip29_min']:.0f} percent in less than three years. After December 2007, the fall "
            f"was {100 - c['ip07_min']:.0f} percent. <bookmark mark='b'/> Unemployment: by 1933, about one worker "
            f"in four, {c['u29_max']:.0f} percent at the peak. In 2009, {c['u07_max']:.0f} percent. "
            "<bookmark mark='c'/> Prices: in the Depression they fell by about a quarter, which made every debt "
            "heavier. In 2008 they never fell below where they started. <bookmark mark='d'/> And output: real GDP "
            f"fell {100 - c['gdp29_min']:.0f} percent between 1929 and 1933, and "
            f"{100 - c['gdp07_min']:.1f} percent between 2007 and 2009. <bookmark mark='e'/> The second crisis was "
            "far smaller than the first. Why it was smaller, and how much of the credit belongs to the policies "
            "chosen in 2008, is argued about in Parts thirty-one to thirty-three. But in both cases, almost "
            "nobody had seen it coming."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(src))
            for mark, p in zip("abcd", (ip, un, cp, gd)):
                vo.wait_until(mark)
                self.play(FadeIn(p), run_time=0.6)
                self.play(*[Create(ln) for ln in p.lines], run_time=2.0)
        self.clear_scene()

    def called_it(self):
        s = load("spf")
        said = VGroup(label(rf"2009: \ {pct(s['aug_2009'], 1, sign=True)}", font_size=34, color=E.PRED),
                      label(r"the median forecast for real GDP growth", font_size=18, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06)
        got = VGroup(label(rf"2009: \ {pct(s['actual_2009'], 1, sign=True)}", font_size=34, color=WHITE),
                     label(r"the largest fall in a year since 1946", font_size=18, color=GREY_B)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06)
        cc = call_card(r"the Survey of Professional Forecasters", r"August 2008",
                       r"real GDP in 2009 a little higher than in 2008", r"it fell", "wrong", width=11.6,
                       said_value=said, outcome_value=got).to_edge(UP, buff=0.45)
        more = VGroup(
            label(rf"after Lehman, in November 2008, they said {pct(s['nov_2009'], 1, sign=True)} for 2009", font_size=24,
                  color=GREY_A),
            label(rf"the last quarter of 2008: \ forecast {pct(s['aug_q4'], 1, sign=True)} a year, \ outcome "
                  rf"{pct(s['actual_q4'], 1, sign=True)} a year", font_size=24, color=GREY_A),
            label(rf"but in August they put the chance of a fall that quarter at {s['aug_recess_q4']:.0f}\%",
                  font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.22).next_to(cc, DOWN, buff=0.45)
        src = data_tag(r"Philadelphia Fed, Survey of Professional Forecasters (median); BEA via FRED", font_size=16)
        with self.voiceover(
            "This series keeps score of predictions. Here's the first one. <bookmark mark='a'/> In August 2008, "
            "the Federal Reserve Bank of Philadelphia asked its panel of professional forecasters, as it does every "
            f"quarter, how the economy would do. The median forecast for 2009 was growth of "
            f"{say_pct(s['aug_2009'])}. <bookmark mark='b'/> Real GDP fell by {say_pct(-s['actual_2009'])}, the "
            "largest fall in any year since 1946. <bookmark mark='c'/> Even in November, after the collapse of "
            f"Lehman Brothers, the median forecast for 2009 was {say_pct(s['nov_2009'])}. And for the last quarter "
            f"of 2008, the August forecast was growth at an annual rate of {say_pct(s['aug_q4'])}; it came in at "
            f"{say_pct(s['actual_q4'])}. <bookmark mark='d'/> To be fair to the forecasters: in that same August "
            f"survey, they put the chance of a fall in output that quarter at {s['aug_recess_q4']:.0f} percent. "
            "They saw the risk. What they didn't see was its size."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(cc.card), FadeIn(cc[1][0]), FadeIn(cc.left), FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(cc.right))
            self.play(FadeIn(cc.stamp, scale=1.4))
            vo.wait_until("c")
            self.play(FadeIn(more[0]))
            self.play(FadeIn(more[1]))
            vo.wait_until("d")
            self.play(FadeIn(more[2]))
        self.clear_scene()

    def letter(self):
        a = tables.BRITISH_ACADEMY_2009.data
        q1 = quote_card(a["foresaw"], r"Besley and Hennessy, letter to the Queen (2009)", width=12.0, font_size=28)
        q1.to_edge(UP, buff=0.6)
        two = VGroup(
            VGroup(label(r"an order nobody designed", font_size=28, color=E.ACCENT),
                   label(r"why it works: \ Parts 2, 9, 16, 17", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.1),
            VGroup(label(r"a failure nobody foresaw", font_size=28, color=E.MISS),
                   label(r"why it fails: \ Act IV, \ and Parts 26, 33, 57", font_size=22, color=GREY_A)).arrange(
                DOWN, buff=0.1),
        ).arrange(RIGHT, buff=1.6).next_to(q1, DOWN, buff=0.8)
        src = published_tag(tables.BRITISH_ACADEMY_2009.tag, corner=DR, font_size=17)
        with self.voiceover(
            "This is what the British Academy's letter to the Queen meant. Many people, it said, did foresee the "
            "crisis. But the exact form that it would take, and the timing of its onset and ferocity, were "
            "foreseen by nobody. <bookmark mark='a'/> So the series has two jobs. It has to explain why an order "
            "that nobody designed works as well as it does, which is the business of Parts two, nine, sixteen and "
            "seventeen. And it has to explain how the same order fails: market failures in Act four, banks and "
            "crises in Parts twenty-six and thirty-three, and what forecasters can and can't see in Part "
            "fifty-seven."
        ) as vo:
            self.play(FadeIn(q1, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(two[0], shift=UP * 0.1))
            self.play(FadeIn(two[1], shift=UP * 0.1))
        self.clear_scene()
