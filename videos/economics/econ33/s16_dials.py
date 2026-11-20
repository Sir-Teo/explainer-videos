from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ33.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ crises", r"How costly are crises, and how well can they be foreseen?",
             "Chapter fourteen. The Dials: crises.", lit={2009: r"Reinhart and Rogoff",
                                                          2022: r"Greenwood, Hanson, Shleifer and S\o rensen"},
             scale=("nation", "world"), horizon=("a decade",))
        self.cost()
        self.warning()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.1f}", step=0.55):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.15, step=step, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag))
            for mk, r in zip(marks, rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def cost(self):
        R = load("recessions")
        self._show(dials.DIALS["crisis_cost"], r"the output cost of a banking crisis \ (two rows added)", 0, 20,
                   [0, 5, 10, 15, 20], r"percent of GDP",
                   "Part twenty-six opened the dial for the cost of a banking crisis; this part adds two rows. "
                   "<bookmark mark='a'/> Reinhart and Rogoff: output falls more than nine percent from peak to "
                   "trough after the typical systemic crisis. <bookmark mark='b'/> Cerra and Saxena, across a hundred "
                   "and ninety countries: a loss of about ten percent that does not go away. <bookmark mark='c'/> "
                   "Romer and Romer, for rich countries since 1967: about six percent at the worst, and highly "
                   "variable. <bookmark mark='d'/> America's own, peak to trough, <bookmark mark='e'/> and its gap "
                   "below the old trend a decade later. <bookmark mark='f'/> New: this part's comparison since 1948, "
                   f"{R['gap5_post']:.1f} points of GDP per head lost against a normal recession five years on, "
                   f"<bookmark mark='g'/> and {R['gap5_all']:.1f} since 1870. <bookmark mark='z'/> The status stays "
                   "contested: the measures differ, and averages mix the crisis with whatever caused it.",
                   "abcdefg")

    def warning(self):
        O = load("panel")["odds"]
        self._show(dials.DIALS["credit_warning"], r"the warning value of a credit boom \ (new)", 0, 50,
                   [0, 10, 20, 30, 40, 50], r"\% chance of a crisis within three years",
                   "The second dial is new: how much a credit boom tells you. <bookmark mark='a'/> Greenwood, Hanson, "
                   "Shleifer and Sorensen, forty-two countries since 1950: about forty percent after booms in credit "
                   "and asset prices. <bookmark mark='b'/> This part's count when loans and house prices both rose "
                   f"fastest: {100 * O['both']:.0f} percent. <bookmark mark='c'/> And for the fastest credit growth "
                   f"alone, {100 * O['by_quintile'][-1]:.0f} percent, against {100 * O['by_quintile'][0]:.0f} "
                   "for the slowest. <bookmark mark='z'/> The status: settled within a range. Booms raise the odds "
                   "of a crisis two to four times over, and higher with asset prices; most booms still end without "
                   "one, and the timing is hard to call.", "abc")
