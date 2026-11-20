from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ34.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ pass-through and PPP", r"How far do exchange rates reach prices, and how fast "
             r"do they return?", "Chapter thirteen. The Dials: pass-through and purchasing power parity.",
             lit={1996: r"Rogoff", 2010: r"Gopinath, Itskhoki and Rigobon"}, scale=("market", "world"),
             horizon=("a year", "a decade"))
        self.passthrough()
        self.halflife()

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

    def passthrough(self):
        Dl = load("dollar")
        self._show(dials.DIALS["passthrough"], r"exchange-rate pass-through \ (first rows)", 0, 1,
                   [0, 0.25, 0.5, 0.75, 1], r"share of the exchange rate's move in import prices",
                   "The first dial has been waiting since the plan was written: pass-through, which Parts thirty-six "
                   "and sixty-six will use for tariffs. <bookmark mark='a'/> Gopinath, Itskhoki and Rigobon: a "
                   "quarter, for American imports priced in dollars; <bookmark mark='b'/> nearly all of it for those "
                   "priced in other currencies. <bookmark mark='c'/> This part's estimate for American imports "
                   f"excluding fuel: {abs(Dl['pt']['long_run']):.2f} after a year. <bookmark mark='z'/> The status: "
                   "depends on the setting, above all on the currency the goods are priced in.", "abc")

    def halflife(self):
        Q = load("ppp")
        self._show(dials.DIALS["ppp_halflife"], r"the half-life of PPP deviations \ (new)", 0, 8, [0, 2, 4, 6, 8],
                   r"years", "The second is new: how long deviations from purchasing power parity last. "
                   "<bookmark mark='a'/> Rogoff's consensus: three to five years. <bookmark mark='b'/> This part, "
                   f"over a hundred and fifty years and eighteen countries: {Q['full']['halflife']:.1f}. "
                   f"<bookmark mark='c'/> In the floating era alone: {Q['floating']['halflife']:.1f}. "
                   "<bookmark mark='z'/> The status: settled within a range. Real exchange rates come back, slowly; "
                   "why so slowly is the puzzle.", "abc", fmt="{:.1f}")
