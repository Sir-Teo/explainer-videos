from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ40.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ mobility and the tail of wealth", r"What do the numbers say?",
             "Chapter fourteen. The Dials: mobility and the tail of wealth.",
             lit={1992: r"Solon", 2006: r"Klass et al."}, scale=("household", "nation"), horizon=("a century",))
        self.ige()
        self.wealth()

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

    def ige(self):
        self._show(dials.DIALS["ige"], r"the intergenerational elasticity \ (new)", 0, 0.8,
                   [0, 0.2, 0.4, 0.6, 0.8], r"elasticity of children's income with respect to parents'",
                   "The first dial is new: the intergenerational elasticity of income in America. Solon's averages "
                   "of several years gave 0.4 or higher; <bookmark mark='a'/> Mazumder's long spells of Social "
                   "Security earnings, about 0.6; <bookmark mark='b'/> Chetty and coauthors' tax records, 0.344 in "
                   "logs; <bookmark mark='c'/> and this film's fit across their percentile means, 0.41. "
                   "<bookmark mark='z'/> The status: contested. The number depends on how long parents' income is "
                   "averaged, at what age children are observed, and how zero incomes are treated; that is why the "
                   "field has moved to ranks.", "abc")

    def wealth(self):
        self._show(dials.DIALS["pareto_wealth"], r"the Pareto exponent of top wealth \ (new)", 1.0, 2.2,
                   [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2], r"$\alpha$, \ lower is a fatter tail",
                   "The second, also new: the Pareto exponent of American wealth. From the Federal Reserve's shares "
                   "in 1989, 1.74; <bookmark mark='a'/> in 2026, 1.48; <bookmark mark='b'/> and the Forbes 400 from "
                   "1988 to 2003, 1.49. <bookmark mark='z'/> The status: depends on the setting, because the tail "
                   "moves with returns, growth and taxes, and fattened through these years.", "ab")
