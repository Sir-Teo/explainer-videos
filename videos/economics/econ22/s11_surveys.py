from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403


class Surveys(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Your answer, \ the surveys \ and the lottery", r"What do people say they would do with a "
             r"windfall, \ and what do winners do?", "Chapter nine. Your answer, the surveys and the lottery.",
             lit={2014: r"Jappelli and Pistaferri", 2021: r"Fuster, Kaplan, Zafar; Fagereng, Holm, Natvik"},
             scale=("household",), horizon=("a year",))
        self.ask()
        self.fkz()
        self.lottery()

    def ask(self):
        j = tables.MPC_STUDIES.data
        x0, x1 = -5.6, 5.6

        def X(v):
            return x0 + (x1 - x0) * v

        y0 = -0.4
        axis = Line([x0, y0, 0], [x1, y0, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(v), y0 - 0.07, 0], [X(v), y0 + 0.07, 0], color=GREY_C),
                                MathTex(f"{int(100 * v)}\\%", font_size=24, color=GREY_B).move_to([X(v), y0 - 0.35, 0]))
                         for v in (0, 0.25, 0.5, 0.75, 1.0)])
        m = load("mpc")
        marks = [
            (load("pih")["share_year"], r"permanent income: \\ 3\% a year", INCOME, 1),
            (m["mean_mpc"], r"the Island's \\ buffer stock: \ 23\%", SPEND, -1),
            (j["jp"]["value"], r"Italians asked, \ 2010: \\ 48\% on average", SAVE, 1),
        ]
        objs = VGroup()
        for v, txt, col, side in marks:
            tri = Triangle(color=col, fill_color=col, fill_opacity=1).scale(0.12).rotate(PI if side > 0 else 0)
            tri.move_to([X(v), y0 + 0.25 * side, 0])
            lb = label(txt, font_size=20, color=col).next_to(tri, UP if side > 0 else DOWN, buff=0.15)
            objs.add(VGroup(tri, lb))
        head = label(r"share of an unexpected windfall spent \ (within the year)", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.8)
        you = label(r"and your number, \ from chapter 1?", font_size=24, color=YOU).next_to(axis, DOWN, buff=1.6)
        tag = published_tag(r"Jappelli and Pistaferri, AEJ: Macro 6(4) (2014), \ abstract", corner=DR, font_size=12)
        with self.voiceover(
            "In chapter one you wrote down how much of a month's income, arriving unexpectedly, you would spend. "
            "Here is a scale to put it on. <bookmark mark='a'/> The permanent-income household: about three percent "
            "a year. <bookmark mark='b'/> The Island's buffer-stock households: twenty-three percent within the "
            "year. <bookmark mark='c'/> In 2010 the Bank of Italy's household survey asked thousands of Italians "
            "directly what share of an unexpected gain equal to a month's income they would spend. Tullio Jappelli "
            "and Luigi Pistaferri found an average of forty-eight percent, and much higher among households with "
            "little cash on hand. <bookmark mark='d'/> Where does your number sit?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(ticks), FadeIn(tag))
            for mk, o in zip("abc", objs):
                vo.wait_until(mk)
                self.play(FadeIn(o))
            vo.wait_until("d")
            self.play(FadeIn(you))
        self.wait(2.0)
        self.clear_scene()

    def fkz(self):
        f = tables.MPC_STUDIES.data["fkz"]["findings"]
        rows = VGroup(
            label(r"Andreas Fuster, \ Greg Kaplan and Basit Zafar, \ 2021: \ \emph{What Would You Do with \$500?}",
                  font_size=24, color=E.ACCENT),
            label(rf"gains: \ {f[0]}", font_size=22, color=SPEND),
            label(rf"losses: \ {f[1]}", font_size=22, color=HOLD),
            label(rf"news: \ {f[2]}", font_size=22, color=INCOME),
            label(rf"loans: \ {f[3]}", font_size=22, color=CASH),
            label(r"so not borrowing limits alone: \ also the bother of changing plans, \ and a few short of cash",
                  font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Fuster, Kaplan and Zafar, REStud 88(4) (2021): \ 1760--1795, \ abstract", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Surveys can also ask what no experiment could. In a survey of Americans, Andreas Fuster, Greg Kaplan "
            "and Basit Zafar asked what people would do with gains, losses, news and loans. <bookmark mark='a'/> "
            "With an unexpected gain, many would spend nothing at all, and others a large share. "
            "<bookmark mark='b'/> After a loss, cuts were larger and more common than the increases after a gain. "
            "<bookmark mark='c'/> Told of a gain that would only come later, very few would spend anything "
            "now, even among those who would spend a windfall in hand. <bookmark mark='d'/> And offered a loan for a "
            "year at no interest, almost no one would spend it. <bookmark mark='e'/> So it is not simply that "
            "people cannot borrow. The authors' model needs two things: a cost of changing one's spending plans, "
            "and a sizeable group of households with very little wealth."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def lottery(self):
        f = tables.MPC_STUDIES.data["fhn"]
        sc = study_card(r"MPC Heterogeneity and Household Balance Sheets", r"Andreas Fagereng, \ Martin Holm \ and "
                        r"Gisle Natvik, \ AEJ: Macroeconomics, \ 2021", [
                            (r"what varied", r"the size of a lottery prize, \ and when it was won: \ luck"),
                            (r"the data", r"Norway's tax records: \ every winner's income, \ wealth and spending, "
                                          r"year by year"),
                            (r"small prizes", rf"{f['small_prize']}, \ to winners with little liquid wealth: \ spent "
                                              r"in full within the year"),
                            (r"large prizes", r"to winners with ample liquid wealth: \ slightly below one-half"),
                            (r"after", r"spending peaks in the year of winning, \ and is back to normal within five "
                                       r"years"),
                        ], design="RCT", width=12.4, font_size=21).move_to(UP * 0.1)
        with self.voiceover(
            "And the best natural experiment of all is luck. <bookmark mark='a'/> In Norway, tax records show every "
            "household's income and wealth, and from them its spending, year by year. Andreas Fagereng, Martin Holm "
            "and Gisle Natvik followed people who won lottery prizes. <bookmark mark='b'/> Winners of the smallest "
            "prizes, about fifteen hundred dollars, who had little liquid wealth, spent all of it within the year. "
            "<bookmark mark='c'/> Winners of large prizes who already had plenty of liquid wealth spent slightly "
            "below half. <bookmark mark='d'/> Spending peaked in the year of the win and was back to normal within "
            "five years. Liquid wealth and the size of the windfall matter most, just as the buffer stock says, but "
            "the level of spending out of every windfall is higher than the model's."
        ) as vo:
            self.play(FadeIn(sc.card), FadeIn(sc[1][0]), FadeIn(sc[2]), FadeIn(sc.body[0]))
            vo.wait_until("a")
            self.play(FadeIn(sc.body[1]))
            vo.wait_until("b")
            self.play(FadeIn(sc.body[2]))
            vo.wait_until("c")
            self.play(FadeIn(sc.body[3]))
            vo.wait_until("d")
            self.play(FadeIn(sc.body[4]))
        self.clear_scene()
