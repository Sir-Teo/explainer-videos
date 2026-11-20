from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ41.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ the elasticity, \ the top rate, \ who pays", r"What do the numbers say?",
             "Chapter fourteen. The Dials: the elasticity, the top rate, who pays.",
             lit={1995: r"Feldstein", 2011: r"Diamond and Saez", 2018: r"Fuest, \ Peichl and Siegloch"},
             scale=("person", "nation"), horizon=("a year",))
        self.eti()
        self.toprate()
        self.incidence()

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

    def eti(self):
        self._show(dials.DIALS["eti"], r"the elasticity of taxable income \ (new)", 0, 1.2,
                   [0, 0.25, 0.5, 0.75, 1.0], r"elasticity with respect to the share kept, \ $1 - t$",
                   "The first dial is new: the elasticity of taxable income. Feldstein's panel around the 1986 reform "
                   "gave at least one; <bookmark mark='a'/> Gruber and Saez, with more reforms, about 0.4; "
                   "<bookmark mark='b'/> and Diamond and Saez take a quarter as the middle of the range. "
                   "<bookmark mark='z'/> The status: depends on the setting, because the elasticity depends on what "
                   "the tax law lets people relabel, defer or hide.", "ab")

    def toprate(self):
        self._show(dials.DIALS["top_rate"], r"the revenue-maximizing top rate \ (new)", 0, 100,
                   [0, 20, 40, 60, 80, 100], r"percent, \ all taxes on top income",
                   "The second, also new: the revenue-maximizing top rate. Diamond and Saez: seventy-three percent. "
                   "<bookmark mark='a'/> This film, with the Pareto parameter from the 2022 tax data and the same "
                   "elasticity: seventy-two; <bookmark mark='b'/> with Feldstein's elasticity of one: thirty-nine. "
                   "<bookmark mark='z'/> The status: contested, and the dispute is almost entirely about the "
                   "elasticity.", "ab", fmt="{:.0f}")

    def incidence(self):
        self._show(dials.DIALS["corp_incidence"], r"corporate tax incidence on wages \ (new)", 0, 100,
                   [0, 25, 50, 75, 100], r"percent of the burden borne by workers",
                   "The third: who pays the corporate tax. In German towns, workers bore about fifty-one percent. "
                   "<bookmark mark='a'/> On the Island, closed to capital flows, none; <bookmark mark='b'/> open, all "
                   "of it. <bookmark mark='z'/> The status: depends on the setting, on how mobile capital and profits "
                   "are, and on the time horizon.", "ab", fmt="{:.0f}")
