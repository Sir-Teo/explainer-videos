from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.two_scorecards()
        self.question()
        self.title()
        self.objectives()

    def two_scorecards(self):
        sam = history_card(1966, r"Paul Samuelson, \ in \emph{Newsweek}", r"`Wall Street indexes predicted nine out "
                           r"of the last five recessions'", color=NOW, width=6.0, font_size=21)
        sam.to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.5)
        alarms = VGroup(*[Circle(radius=0.18, stroke_color=NOW, stroke_width=2.5, fill_color=NOW,
                                 fill_opacity=0.25 if k >= 5 else 0.9) for k in range(9)]).arrange(RIGHT, buff=0.12)
        alarms.next_to(sam, DOWN, buff=0.4)
        al_l = label(r"nine alarms; \ five recessions", font_size=19, color=NOW).next_to(alarms, DOWN, buff=0.15)
        # 153 recessions: lit as forecasters saw them coming
        cells = VGroup(*[Square(side_length=0.2, stroke_width=0.8, stroke_color=GREY_D, fill_color=GREY_D,
                                fill_opacity=0.25) for _ in range(153)]).arrange_in_grid(9, 17, buff=0.06)
        cells.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.6)
        ajl = history_card(2018, r"An, \ Jalles and Loungani", r"153 recessions in 63 countries, \ 1992--2014: \ how "
                           r"many did forecasters see coming?", color=SPF, width=6.0, font_size=21)
        ajl.to_edge(UP, buff=0.5).to_edge(RIGHT, buff=0.5)
        cells.next_to(ajl, DOWN, buff=0.45)
        lab_a = label(r"by April of the year before: \ 5", font_size=20, color=EST).next_to(cells, DOWN, buff=0.25)
        lab_b = label(r"by October of the year itself: \ 118", font_size=20, color=SPF).next_to(lab_a, DOWN,
                                                                                               buff=0.15)
        tag = published_tag(r"Samuelson, \ Newsweek, \ 19 September 1966; \ An, \ Jalles and Loungani, \ "
                            r"International Finance 21(2) (2018)", corner=DL, font_size=12)
        with self.voiceover(
            "Two scorecards. <bookmark mark='a'/> In 1966 Paul Samuelson joked that the stock market had predicted "
            "nine of the last five recessions: too many alarms. <bookmark mark='b'/> Economists err the other way. "
            "Zidong An, João Tovar Jalles and Prakash Loungani took the forecasts made for 63 countries between "
            "1992 and 2014, and found 153 recessions, years in which output fell. <bookmark mark='c'/> In April of "
            "the year before, forecasters expected a fall in five of them. <bookmark mark='d'/> By October of the "
            "recession year itself, with the year nearly over, in 118. Recessions are mostly recognized, not "
            "forecast. This part is about how anyone reads an economy in real time: how its numbers are made and "
            "revised, how to see the present before the statistics arrive, and how to score a guess about the "
            "future."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(sam, shift=UP * 0.1))
            self.play(LaggedStart(*[FadeIn(a_) for a_ in alarms], lag_ratio=0.15), FadeIn(al_l), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeIn(ajl, shift=UP * 0.1), FadeIn(cells), run_time=1.5)
            vo.wait_until("c")
            self.play(*[cells[k].animate.set_fill(EST, opacity=0.95) for k in range(5)], FadeIn(lab_a))
            vo.wait_until("d")
            self.play(LaggedStart(*[cells[k].animate.set_fill(SPF, opacity=0.8) for k in range(5, 118)],
                                  lag_ratio=0.02), FadeIn(lab_b), run_time=3.0)
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how is a number like GDP made, \ and how much does it change later?", font_size=26, color=FIRST),
            label(r"how can anyone see this quarter before the statistics are out?", font_size=26, color=NOW),
            label(r"which signals warn of a recession, \ and how often do they cry wolf?", font_size=26, color=GB),
            label(r"and how should a forecast be scored, \ and its uncertainty told?", font_size=26, color=SPF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: what is the economy doing right now, and how good is anyone's guess about next year? "
            "<bookmark mark='a'/> How is a number like GDP made, and how much does it change later? <bookmark "
            "mark='b'/> How can anyone see this quarter before the statistics are out? <bookmark mark='c'/> Which "
            "signals warn of a recession, and how often do they cry wolf? <bookmark mark='d'/> And how should a "
            "forecast be scored, and its uncertainty told?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([F["t"][0], F["t"][-1]], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["p"])
        v = (v - np.nanmin(v)) / (np.nanmax(v) - np.nanmin(v))
        logo = path(mini, F["t"], v, NOW, 2.2, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 57 \ $\cdot$ \ Reading the Economy in Real Time", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part fifty-seven: reading the economy in real time."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XI \ $\cdot$ \ Economics at Work", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"how GDP and payrolls are made, \ revised and seasonally adjusted",
            r"nowcasting: \ bridge equations and a factor model with the Kalman filter",
            r"recession signals: \ the yield curve, \ the Sahm rule, \ and their false alarms",
            r"scoring forecasts: \ bias, \ errors by horizon, \ Diebold and Mariano, \ combinations",
            r"new data, \ text as data, \ and how to tell people about uncertainty",
        ], color=E.ACCENT, font_size=29, width=13.0)
        with self.voiceover(
            "The last act of the series is economics at work, and it starts where most economists' days start: "
            "with the data. By the end of this part you will know <bookmark mark='a'/> how GDP and payroll numbers "
            "are made, revised and seasonally adjusted; <bookmark mark='b'/> how nowcasts are built, from bridge "
            "equations to a factor model run through the Kalman filter; <bookmark mark='c'/> which signals warn of "
            "recessions, and how often they cry wolf; <bookmark mark='d'/> how to score a forecast, and when one "
            "forecaster really beats another; <bookmark mark='e'/> and what new data, text, and honest talk about "
            "uncertainty add."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
