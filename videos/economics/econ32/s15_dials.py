from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ32.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the multipliers", r"How much output does a dollar of spending or taxes move?",
             "Chapter thirteen. The Dials: the multipliers.",
             lit={2010: r"Romer and Romer", 2018: r"Ramey and Zubairy"}, scale=("nation", "city"),
             horizon=("two years",))
        self.spending()
        self.taxes()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}", step=0.62):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=step, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip(marks, rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def spending(self):
        self._show(dials.DIALS["multipliers"], r"the spending multiplier \ (new)", 0, 2.2, [0, 0.5, 1, 1.5, 2],
                   r"dollars of output per dollar of purchases",
                   "The first new dial is the government-spending multiplier. <bookmark mark='a'/> Ramey and Zubairy "
                   "with military news: zero point six seven over two years. <bookmark mark='b'/> With Blanchard and "
                   "Perotti's timing, zero point four one. <bookmark mark='c'/> Across American states, Nakamura and "
                   "Steinsson: about one and a half. <bookmark mark='d'/> Chodorow-Reich's survey of regional "
                   "studies: one point eight. <bookmark mark='z'/> The status: depends on the setting. National "
                   "multipliers in normal times sit below one; regional ones, with monetary policy held fixed, above "
                   "it; and theory says a slump at the zero bound can push the national one above one as well.",
                   "abcd")

    def taxes(self):
        self._show(dials.DIALS["tax_multiplier"], r"the tax multiplier \ (new)", 0, 4, [0, 1, 2, 3, 4],
                   r"percent fall in GDP after a tax rise of 1\% of GDP",
                   "The second: the tax multiplier. <bookmark mark='a'/> The Romers: nearly three percent of output "
                   "over three years for a tax increase of one percent of GDP. <bookmark mark='b'/> This film's "
                   "projections on their record: two point two at the trough. <bookmark mark='z'/> The status: "
                   "contested. Narrative estimates are large and consistent; why taxes should matter more than "
                   "spending, and whether deficit-cutting tax rises cost less, are not settled.", "ab", fmt="{:.1f}")
