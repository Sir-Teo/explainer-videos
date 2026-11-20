from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ27.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the propensity to spend, \ and Okun's coefficient", r"How big is $b$, \ and "
             r"how much unemployment does a lost point of output bring?", "Chapter thirteen. The Dials: the "
             "propensity to spend, and Okun's coefficient.", lit={1962: r"Okun", 2017: r"Ball, Leigh and Loungani"},
             scale=("household", "nation"), horizon=("a quarter", "a year"))
        self.mpc()
        self.okun()

    def mpc(self):
        dial = dials.DIALS["mpc_windfall"]
        head = status_head(dial, r"the propensity to spend a windfall \ (from Part 22)")
        frame, rows = dial_rows(dial, 0, 60, [0, 10, 20, 30, 40, 50, 60], r"percent spent", top=2.2, step=0.62,
                                fmt="{:.0f}")
        note_ = label(r"the cross's $b$ is the share of a lasting rise in income spent over a year: \ larger than "
                      r"these quarterly shares, \ smaller than the Island's 0.6 once taxes and imports leak",
                      font_size=17, color=GREY_A).to_edge(DOWN, buff=0.35)
        tag = published_tag(r"the dial's record: \ explainer/economics/dials.py", corner=DR, font_size=12)
        with self.voiceover(
            "Two dials. The first returns from Part twenty-two, because the multiplier is built on it: how much of "
            "an extra dollar people spend. <bookmark mark='a'/> When the American government mailed tax rebates in "
            "2001, with the week of each cheque set by the last digits of the taxpayer's Social Security number, "
            "households spent about thirty percent on nondurable goods within the quarter. "
            "<bookmark mark='b'/> The stimulus payments of 2008: about twenty percent on nondurables, and far more "
            "counting cars. <bookmark mark='c'/> The payments of 2020, when there was little to buy: about ten "
            "percent. <bookmark mark='d'/> Alaska's yearly oil dividend, in account data, about a quarter. "
            "<bookmark mark='e'/> Italians asked in a survey, about half. <bookmark mark='f'/> And the buffer-stock "
            "households of Part twenty-two, about a quarter within a year. <bookmark mark='g'/> These are shares "
            "of one-off windfalls in a quarter. The cross needs the share of a lasting rise in income spent over "
            "a year, which is larger, but once taxes and imports leak, the Island's six tenths is generous. Part "
            "thirty-two measures the multipliers themselves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("g")
            self.play(FadeIn(note_))
        self.clear_scene()

    def okun(self):
        dial = dials.DIALS["okun"]
        head = status_head(dial, r"Okun's coefficient \ (new)")
        frame, rows = dial_rows(dial, -1.0, 0.0, [-1.0, -0.75, -0.5, -0.25, 0.0], r"points of unemployment per "
                                r"point of output gap", top=2.0, step=0.68, fmt="{:.2f}")
        meaning = wrapped_label(tex_safe(dial.meaning), 12.0, 17, GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(r"Okun (1962); \ Ball, \ Leigh and Loungani, \ JMCB 49(7) (2017); \ this film",
                            corner=DR, font_size=12)
        o = load("okun")
        with self.voiceover(
            "The second dial is new: Okun's coefficient, how many points unemployment rises for each point output "
            "falls below its potential. <bookmark mark='a'/> Arthur Okun, in 1962, found about three points of "
            "output for each point of unemployment: a coefficient of a third. <bookmark mark='b'/> Laurence Ball, "
            "Daniel Leigh and Prakash Loungani, fifty years on, found about minus point four five for the United "
            "States, and a fit that has hardly changed since 1948. <bookmark mark='c'/> But in Japan, where firms "
            "keep workers through slumps, about minus point one five. <bookmark mark='d'/> And in Spain, where "
            "temporary contracts are cut first, about minus point eight five. <bookmark mark='e'/> This film's own "
            "estimate, against the Congressional Budget Office's measures of potential output and the natural "
            f"rate, is {o['beta']:.2f}. <bookmark mark='f'/> It depends on the setting: on how a country's firms "
            "adjust, by hours, by hiring, or by firing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("f")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
