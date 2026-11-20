from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ39.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ skills, \ firms, \ call-backs", r"What do the numbers say?",
             "Chapter thirteen. The Dials: skills, firms, call-backs.",
             lit={1992: r"Katz and Murphy", 2013: r"Card, \ Heining and Kline"}, scale=("firm", "nation"),
             horizon=("a decade",))
        self.skills()
        self.firms()
        self.callbacks()

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

    def skills(self):
        self._show(dials.DIALS["skill_substitution"], r"college and high-school workers \ (new)", 0, 3.0,
                   [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0], r"elasticity of substitution, \ $\sigma$",
                   "The first dial is new: the elasticity of substitution between college and high-school workers. "
                   "Katz and Murphy's time series gives 1.41; <bookmark mark='a'/> Ciccone and Peri, using states and "
                   "schooling laws, about 1.5; <bookmark mark='b'/> Card and Lemieux, using cohorts, about 2.5. This "
                   "film's own attempt on recent national data failed, for the reason chapter two showed. "
                   "<bookmark mark='z'/> The status: settled within a range, from about one and a half to two and a "
                   "half. Either way, more graduates lower the premium, so education can race technology.", "ab")

    def firms(self):
        self._show(dials.DIALS["firm_premium_share"], r"the firm share of wage variance \ (new)", 0, 30,
                   [0, 5, 10, 15, 20, 25, 30], r"percent of the variance of log wages",
                   "The second, also new: how much of the variance of pay is where you work. In West Germany, Card, "
                   "Heining and Kline found about 18 percent in the late 1980s, <bookmark mark='a'/> rising to 21 in "
                   "the 2000s. <bookmark mark='b'/> On the Island, the estimate lands on the planted eleven percent "
                   "when a tenth of workers move each year. <bookmark mark='z'/> The status: depends on the setting, "
                   "and on correcting for too few movers.", "ab", fmt="{:.1f}")

    def callbacks(self):
        self._show(dials.DIALS["callback_gap"], r"the call-back gap \ (new)", 0, 100,
                   [0, 20, 40, 60, 80, 100], r"percent more call-backs for White applicants",
                   "The third: the call-back gap. Bertrand and Mullainathan's résumés, recomputed here, give fifty "
                   "percent, with an interval from about a quarter to four-fifths; <bookmark mark='a'/> the meta-"
                   "analysis of American field experiments since 1989, thirty-six. <bookmark mark='z'/> The status: "
                   "settled within a range, and not shrinking.", "a", fmt="{:.0f}")
