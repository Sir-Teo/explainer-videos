from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Clocks(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.lexis_diagram()
        self.identity()
        self.assumptions()

    def card(self):
        card = chapter_card(1, r"Three clocks", r"Is it age, \ the year, \ or the generation?",
                            lit={1965: r"Ryder"}, part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter one. Three clocks."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def three(self):
        head = heading(r"Every score carries three times")
        clocks = VGroup(clock(r"age", AGE), clock(r"period", PERIOD), clock(r"cohort", COHORT)).arrange(RIGHT,
                                                                                                     buff=2.4)
        clocks.move_to([0, 1.3, 0])
        rows = rows_of([
            (r"age: \ how long you have lived; \ growing up and growing old", AGE),
            (r"period: \ the year you were tested; \ a recession, \ a pandemic, \ a new test form", PERIOD),
            (r"cohort: \ the year you were born; \ the schooling, \ food and medicine of your generation", COHORT),
            (r"a 70-year-old tested in 2020 was born in 1950: \ any two clocks fix the third", WHITE),
        ], 12.0, 25, 0.36).move_to([0, -1.5, 0])
        with self.voiceover(
            "A score from a person carries three times. <bookmark mark='a'/> Age: how long the person has lived. "
            "Growing up and growing old are age effects. <bookmark mark='b'/> Period: the year of the test. A "
            "recession, a pandemic, or a new edition of the test touches everyone tested that year, whatever their "
            "age. <bookmark mark='c'/> Cohort: the year of birth. A generation shares its schooling, its food and "
            "its medicine, and carries them through life. <bookmark mark='d'/> But a seventy-year-old tested in "
            "2020 was born in 1950. Any two of the clocks fix the third."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(c, scale=0.8) for c in clocks], lag_ratio=0.3))
            for m, r, c in zip("abc", rows, clocks):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15), Indicate(c[0], color=c[1].get_color()))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15))
        self.clear_scene()

    def lexis_diagram(self):
        head = heading(r"The Lexis diagram")
        A = axes([1950, 2020], [0, 70], x_length=6.6, y_length=5.0, xticks=[1950, 1970, 1990, 2010],
                 yticks=[0, 20, 40, 60], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                 xlabel=r"period: \ year of the test", ylabel=r"age", center=[-2.6, -0.4, 0], font_size=16)
        diag = VGroup()
        for c in range(1890, 2020, 10):
            x0, x1 = max(1950, c), min(2020, c + 70)
            if x1 <= x0:
                continue
            diag.add(Line(A.ax.c2p(x0, x0 - c), A.ax.c2p(x1, x1 - c), color=COHORT, stroke_width=1.5,
                          stroke_opacity=0.6))
        life = Line(A.ax.c2p(1955, 5), A.ax.c2p(2015, 65), color=COHORT, stroke_width=6)
        dot = Dot(A.ax.c2p(1955, 5), radius=0.1, color=WHITE)
        vline = DashedLine(A.ax.c2p(1990, 0), A.ax.c2p(1990, 70), color=PERIOD, stroke_width=3)
        hline = DashedLine(A.ax.c2p(1950, 40), A.ax.c2p(2020, 40), color=AGE, stroke_width=3)
        rows = rows_of([
            (r"one point: \ a test, \ at an age, \ in a year", WHITE),
            (r"a life runs up a diagonal: \ each diagonal is a cohort \ (here, \ born 1950)", COHORT),
            (r"a cross-sectional study reads a vertical line: \ many ages, \ one year", PERIOD),
            (r"following 40-year-olds over the years reads a horizontal line: \ one age, \ many cohorts", AGE),
            (r"every design reads some slice of this plane, \ and each slice mixes two clocks", GREY_A),
        ], 5.4, 22, 0.34).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "Demographers draw this as a plane, named the Lexis diagram after the nineteenth-century statistician "
            "Wilhelm Lexis. <bookmark mark='a'/> The horizontal axis is the year of the test, the vertical axis is "
            "age, and one point is one test. <bookmark mark='b'/> A life runs up a diagonal, one year older for each "
            "year that passes, so each diagonal is a cohort. This one was born in 1950. "
            "<bookmark mark='c'/> A cross-sectional study, many ages tested in one year, reads a vertical line. "
            "<bookmark mark='d'/> Following forty-year-olds year after year reads a horizontal line: one age, a "
            "different cohort each time. <bookmark mark='e'/> Every design reads some slice of this plane, and each "
            "slice mixes two of the clocks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(diag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(dot))
            vo.wait_until("b")
            self.play(Create(life), dot.animate.move_to(A.ax.c2p(2015, 65)), FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(vline), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(hline), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def identity(self):
        d = load("apc")
        head = heading(r"The identity, \ and what it costs")
        eq1 = label(r"$y = a\cdot\text{Age} + p\cdot\text{Period} + c\cdot\text{Cohort}$", font_size=34)
        eq2 = label(r"$\text{Cohort} = \text{Period} - \text{Age}$", font_size=34, color=COHORT)
        eq3 = label(r"$y = (a - c)\,\text{Age} + (p + c)\,\text{Period}$", font_size=34, color=YOU)
        eq4 = label(r"$(a, \ p, \ c)$ \ and \ $(a + k, \ p - k, \ c + k)$ \ predict the same $y$, \ for every $k$",
                    font_size=30, color=LOST)
        eqs = VGroup(eq1, eq2, eq3, eq4).arrange(DOWN, buff=0.42).move_to([0, 0.6, 0])
        A = axes([20, 80], [0, 0.65], x_length=4.6, y_length=1.9, xticks=[20, 40, 60, 80], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age, \ one person born in 1950", center=[-3.2, -2.55, 0],
                 font_size=14)
        sets = (("+0.00", PERIOD, r"$(0, \ 0.01, \ 0)$: \ all period"),
                ("+0.01", AGE, r"$(0.01, \ 0, \ 0.01)$: \ all ageing"),
                ("-0.01", COHORT, r"$(-0.01, \ 0.02, \ -0.01)$: \ decline, \ outpaced by the times"))
        lines = VGroup(*[curve(A.ax, d["ages"], d[f"y_{k}"], col, stroke_width=7 - 2 * i)
                         for i, (k, col, _) in enumerate(sets)])
        key = legend([(col, txt) for _, col, txt in sets], font_size=17).move_to([3.0, -2.3, 0])
        diff = max(d["diff_+0.01"], d["diff_-0.01"])
        note_ = label(rf"largest difference between them: \ {diff:.0e}", font_size=17, color=GREY_B)
        note_.next_to(key, DOWN, buff=0.2)
        tag = psyche_tag(r"\texttt{lifespan.apc\_equivalent}")
        with self.voiceover(
            "Now the algebra. <bookmark mark='a'/> Suppose a score is a straight-line function of the three clocks, "
            "with slopes a, p and c. <bookmark mark='b'/> But cohort is period minus age. "
            "<bookmark mark='c'/> Substitute, and only two combinations survive: a minus c, multiplying age, and p "
            "plus c, multiplying period. <bookmark mark='d'/> So add any number k to the age slope, subtract it "
            "from the period slope, add it to the cohort slope, and every prediction is unchanged. "
            "<bookmark mark='e'/> Here Psyche follows one person born in 1950 under three such sets of slopes. "
            "One says the rise is all period, one says it's all ageing, one says people decline but the times improve faster, "
            "and they draw one line. No amount of data can choose between them. Norman Ryder made the cohort a central idea of social science in "
            "1965; the identity is why it's so hard to measure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, e in zip("abcd", eqs):
                vo.wait_until(m)
                self.play(FadeIn(e, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(A), LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.5), FadeIn(key), FadeIn(note_))
        self.clear_scene()

    def assumptions(self):
        head = heading(r"Every answer needs an assumption")
        rows = rows_of([
            (r"assume one clock does nothing: \ no period effect, \ say \ (the cohort-sequential design of the "
             r"next chapter)", PERIOD),
            (r"assume a shape: \ two neighbouring cohorts are equal, \ or effects are smooth", COHORT),
            (r"replace a clock by its cause: \ years of schooling for cohort, \ unemployment for period", AGE),
            (r"or measure within people, \ under a randomization: \ the lottery in Bucharest", GOOD),
            (r"the data never choose: \ the assumption does, \ so it must be stated, \ and defended", YOU),
        ], 12.2, 26, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "So every answer to an age, period or cohort question rests on an assumption from outside the data. "
            "<bookmark mark='a'/> You can assume one clock does nothing, for instance that there's no period effect. "
            "That's the design of the next chapter. <bookmark mark='b'/> You can assume a shape: that two "
            "neighbouring cohorts are equal, or that effects change smoothly. <bookmark mark='c'/> You can replace a "
            "clock by a measured cause, years of schooling instead of cohort, or the unemployment rate instead of "
            "period. <bookmark mark='d'/> Or you can measure change inside people under a randomization, as the "
            "lottery did. <bookmark mark='e'/> The data never choose. The assumption does, so it has to be stated, "
            "and defended."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
