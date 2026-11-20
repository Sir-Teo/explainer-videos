from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ42.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ durations, \ medical prices, \ the MVPF", r"What do the numbers say?",
             "Chapter fourteen. The Dials: durations, medical prices, the value of public funds.",
             lit={1987: r"Manning et al.", 1990: r"Meyer", 2020: r"Hendren and Sprung-Keyser"},
             scale=("person", "nation"), horizon=("a year",))
        self.duration()
        self.medical()
        self.mvpf()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}"):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.55, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip(marks, rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def duration(self):
        self._show(dials.DIALS["ui_duration"], r"the duration elasticity of unemployment benefits \ (filled)", 0,
                   1.0, [0, 0.25, 0.5, 0.75, 1.0], r"percent longer unemployment per 1\% higher benefit",
                   "The first dial picks up a promise from Part twenty-four: how much longer unemployment lasts when "
                   "benefits are one percent higher. Meyer's American estimates: four to eight tenths. "
                   "<bookmark mark='a'/> The Island's weekly model: 0.41. <bookmark mark='z'/> The status: settled "
                   "within a range, and at that range today's benefit levels need high risk aversion to be right, "
                   "unless liquidity, not moral hazard, drives most of the response.", "a")

    def medical(self):
        self._show(dials.DIALS["med_price"], r"the price elasticity of medical spending \ (new)", -0.5, 0,
                   [-0.5, -0.4, -0.3, -0.2, -0.1, 0], r"percent change in spending per 1\% higher out-of-pocket price",
                   "The second, new: how much medical spending falls when patients pay more. The RAND experiment's "
                   "summary: minus 0.2. <bookmark mark='a'/> The Island, matched to RAND's ratio between free care and "
                   "ninety-five percent coinsurance: minus 0.23. <bookmark mark='z'/> The status: contested, not "
                   "because the experiment was flawed but because plans with deductibles and caps have no single "
                   "price, so one number summarizes them badly.", "a")

    def mvpf(self):
        self._show(dials.DIALS["mvpf"], r"the marginal value of public funds \ (new)", 0, 2.5,
                   [0, 0.5, 1.0, 1.5, 2.0, 2.5], r"dollars of value per net dollar of public money",
                   "The third, new: the marginal value of public funds. Hendren and Sprung-Keyser: most policies for "
                   "adults between a half and two. <bookmark mark='a'/> The Island's unemployment insurance at its "
                   "best benefit: one. <bookmark mark='b'/> The Island's tax credit: 1.06. <bookmark mark='z'/> The "
                   "status: depends on the setting, because the value of a programme depends on whom it reaches and "
                   "how they respond.", "ab")
