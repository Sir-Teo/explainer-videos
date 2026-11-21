from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ55.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The Dials: \ what a rate rise and a dollar of spending do", r"How large are the two effects "
             r"macro most wants to know?", "Chapter twelve. The Dials: what a rate rise and a dollar of spending do.",
             lit={2004: r"Romer and Romer", 2012: r"Coibion", 2018: r"Ramey and Zubairy"}, scale=("nation",),
             horizon=("a year", "a decade"))
        self._show(dials.DIALS["monetary_shock"], r"a 100-basis-point tightening \ (two rows added)", -5, 0,
                   [-5, -4, -3, -2, -1, 0], r"industrial production at its lowest, \ \%",
                   "The first dial is Part thirty-one's: the effect of a one-point tightening on output at its "
                   "lowest. <bookmark mark='a'/> A standard recursive autoregression: about minus seven tenths of a "
                   "percent. <bookmark mark='b'/> The Romers' narrative shocks: minus four point three. <bookmark "
                   "mark='c'/> Olivier Coibion's reconciliation: two to three. <bookmark mark='d'/> Part thirty-one's "
                   "autoregression with commodity prices, to 2007: about minus one and a third. <bookmark mark='e'/> "
                   "This part adds two rows: the hook's autoregression to 1995, minus eight tenths without commodity "
                   "prices <bookmark mark='f'/> and minus one point one with them. <bookmark mark='z'/> The status "
                   "stays contested. Every method agrees on the sign and the delay; the size moves with the "
                   "assumption, and the assumption is what this part has been about.",
                   "abcdef", fmt="{:.1f}", step=0.5)
        self._show(dials.DIALS["multipliers"], r"the spending multiplier \ (from Part 32)", 0, 2.2,
                   [0, 0.5, 1, 1.5, 2], r"dollars of output per dollar of purchases",
                   "The second dial is Part thirty-two's spending multiplier, which Chapter nine explained. <bookmark "
                   "mark='a'/> National estimates from military news: two thirds of a dollar per dollar. <bookmark "
                   "mark='b'/> With timing assumptions instead: about four tenths. <bookmark mark='c'/> Across "
                   "states: one and a half. <bookmark mark='d'/> A survey of regional studies: one point eight. "
                   "<bookmark mark='z'/> It depends on the setting, and the missing intercept is why the regional "
                   "and national rows differ.", "abcd")

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}", step=0.62):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=step, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-21", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip(marks, rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()
