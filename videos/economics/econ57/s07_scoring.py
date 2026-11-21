from __future__ import annotations

from videos.economics.econ57.common import *  # noqa: F403


class Scoring(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Scoring forecasts", r"When does one forecaster really beat another?",
             "Chapter six. Scoring forecasts.", lit={1969: r"Bates and Granger", 1995: r"Diebold and Mariano"},
             scale=("nation",), horizon=("a year",))
        self.rules()
        self.by_horizon()

    def rules(self):
        rows = VGroup(
            MathTex(r"e_t = f_t - a_t", font_size=36, color=WHITE),
            MathTex(r"\text{bias} = \bar e, \qquad \text{RMSE} = \sqrt{\tfrac1n \textstyle\sum e_t^2}", font_size=36,
                    color=SPF),
            MathTex(r"d_t = e_{A,t}^2 - e_{B,t}^2, \qquad \text{DM} = \frac{\bar d}{\widehat{\text{se}}_{\text{HAC}}"
                    r"(\bar d)} \ \approx\ N(0, 1)", font_size=36, color=GB),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.8)
        notes = VGroup(
            label(r"score against what was knowable: \ the first estimate, \ not today's", font_size=21,
                  color=FIRST),
            label(r"forecasts $h$ quarters ahead overlap: \ their errors are correlated, \ so the standard error "
                  r"must allow for it", font_size=21, color=GREY_A),
            label(r"and always against a benchmark: \ the past average, \ or the last number", font_size=21,
                  color=BENCH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(rows, DOWN, buff=0.55)
        with self.voiceover(
            "How should a forecast be scored? <bookmark mark='a'/> The error is the forecast minus what happened. "
            "<bookmark mark='b'/> Its average is the bias; the square root of its average square, the root mean "
            "squared error, is the usual score. <bookmark mark='c'/> To ask whether one forecaster really beats "
            "another, Francis Diebold and Roberto Mariano took the difference in their squared errors and asked "
            "whether its mean is zero, with a standard error that allows for the errors' correlation over time. "
            "<bookmark mark='d'/> Three rules make the scoring fair. Score against what could be known: the first "
            "estimate of the outcome, not today's revised one, which no forecaster could have aimed at. <bookmark "
            "mark='e'/> Forecasts a year ahead made each quarter overlap, so their errors are correlated. "
            "<bookmark mark='f'/> And always compare with a benchmark that takes no skill."
        ) as vo:
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=UP * 0.1))
            for k, mk in enumerate("def"):
                vo.wait_until(mk)
                self.play(FadeIn(notes[k], shift=RIGHT * 0.1))
        self.clear_scene()

    def by_horizon(self):
        S, A = load("score"), load("score_all")
        rows = S["rows"]
        h = np.array([r["h"] for r in rows])
        ax = plane([-0.3, 4.3], [0, 6], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4], yticks=[0, 2, 4, 6], xlabel=r"quarters ahead",
                   ylabel=r"error, \ points of growth \ (root mean square)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        spf = path(ax, h, [r["rmse"] for r in rows], SPF, 3.2, smooth=False)
        mean = path(ax, h, [r["rmse_mean"] for r in rows], BENCH, 2.6, smooth=False)
        rw = path(ax, h, [r["rmse_rw"] for r in rows], FIRST, 2.6, smooth=False)
        dots = VGroup(*[dot(ax, r["h"], r["rmse"], SPF if r["dm_p"] < 0.05 else GREY_C, 0.09) for r in rows])
        stars = VGroup(*[label(r"$\ast$", font_size=30, color=SPF).next_to(ax.ax.c2p(r["h"], r["rmse"]), DOWN,
                                                                            buff=0.08) for r in rows
                         if r["dm_p"] < 0.05])
        n_sig = len(stars)
        r4 = rows[-1]
        side = VGroup(
            label(rf"blue: \ the professional forecasters \\ ({rows[0]['n']} surveys, \ "
                  rf"{S['rows'][0]['target'][0][:4]}--{S['rows'][0]['target'][-1][:4]})", font_size=18, color=SPF),
            label(r"grey: \ the average of the last \\ ten years' first estimates", font_size=18, color=BENCH),
            label(r"orange: \ last quarter's first estimate", font_size=18, color=FIRST),
            label(r"$\ast$: \ better than the average, \\ Diebold--Mariano, \ 5\%", font_size=18, color=SPF),
            label(rf"bias a year ahead: \ ${r4['bias']:+.2f}$ points", font_size=18, color=ERR),
            label(rf"with 2020Q2--Q3 kept: \ {A['rows'][0]['rmse']:.1f} to {A['rows'][-1]['rmse']:.1f}",
                  font_size=16, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Philadelphia Fed: \ SPF medians; \ real-time first estimates", corner=DR, font_size=12)
        with self.voiceover(
            "Here are America's professional forecasters, scored that way: every median forecast of real GDP growth "
            "since 1968, for the current quarter and up to four quarters ahead, against the first published "
            "number. The two quarters of the pandemic, with swings of thirty points, are left out. <bookmark "
            f"mark='a'/> For the current quarter their error is {rows[0]['rmse']:.2f} points, <bookmark mark='b'/> "
            f"rising to {rows[2]['rmse']:.2f} two quarters ahead and {r4['rmse']:.2f} a year ahead. <bookmark "
            "mark='c'/> The benchmark that takes no skill, the average growth of the last ten years, misses by "
            f"about {rows[0]['rmse_mean']:.1f} at every horizon. <bookmark mark='d'/> Repeating last quarter's "
            f"number does worse still. <bookmark mark='e'/> So the forecasters beat the average, by Diebold and "
            f"Mariano's test, for the current quarter and the next {n_sig - 1} quarters. Beyond that, their "
            "forecasts are "
            "no better than the average of the past. <bookmark mark='f'/> And they lean optimistic: a year ahead "
            f"the average error is {say_num(r4['bias'], 2)} points. The honest summary is that economists can "
            "read the present, and a little of the next six months; beyond that, the forecast is mostly the "
            "average."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(dots[0]))
            vo.wait_until("b")
            self.play(Create(spf), FadeIn(dots[1:]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(mean), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(Create(rw), FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(stars), FadeIn(side[3]))
            vo.wait_until("f")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.clear_scene()
