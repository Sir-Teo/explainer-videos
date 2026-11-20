from __future__ import annotations

import dataclasses

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ38.common import *  # noqa: F403

SCHOOL_ROWS = ("Angrist and Krueger", "Card", "Harmon and Walker", "Duflo", "this film (Card's data)",
               "this film (wage2, with IQ)", "this film (Mincer, 1976 CPS)")


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ the minimum wage, \ schooling, \ labour supply", r"What do the numbers say?",
             "Chapter thirteen. The Dials: the minimum wage, schooling, labour supply.",
             lit={1994: r"Card and Krueger", 2019: r"Cengiz et al."}, scale=("person", "market"),
             horizon=("a year", "a decade"))
        self.minimum()
        self.schooling()
        self.supply()

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

    def minimum(self):
        self._show(dials.DIALS["minimum_wage"], r"the minimum wage \ (new)", -2.2, 2.2, [-2, -1, 0, 1, 2],
                   r"own-wage elasticity of employment",
                   "The first dial is new: the employment effect of the minimum wage, measured as the percent change "
                   "in low-wage jobs per percent rise in low-wage pay. Card and Krueger's restaurants, recomputed "
                   "here, give about one, with a wide interval. <bookmark mark='a'/> The bunching estimates across "
                   "138 state increases give 0.41, <bookmark mark='b'/> Seattle's high minimum minus a half to minus "
                   "two. <bookmark mark='c'/> On the Island, the same design recovers the competitive world's loss "
                   "<bookmark mark='d'/> and the monopsony world's gain. <bookmark mark='z'/> The status: contested. "
                   "Near zero for moderate minimums; losses where the minimum is high relative to local pay.",
                   "abcd", fmt="{:.2f}")

    def schooling(self):
        d = dials.DIALS["return_schooling"]
        keep = []
        for e in d.estimates:
            if e.who in SCHOOL_ROWS and e.design != "regression" or e.who.startswith("this film"):
                if e.who == "Angrist and Krueger" and "1930-39" not in e.sample:
                    continue
                keep.append(e)
        sub = dataclasses.replace(d, estimates=tuple(keep))
        self._show(sub, r"the return to a year of school \ (rows added)", 0, 0.26, [0, 0.05, 0.1, 0.15, 0.2, 0.25],
                   r"proportional rise in earnings per year of school",
                   "The return to schooling, a dial since Part four, shown here by its instrumental estimates: "
                   "Angrist and Krueger's quarter of birth, <bookmark mark='a'/> Card's college distance, "
                   "<bookmark mark='b'/> Britain's leaving age, "
                   "<bookmark mark='c'/> Indonesia's school-building programme. <bookmark mark='d'/> This part adds "
                   "three rows: Card's estimate recomputed from his data, <bookmark mark='e'/> least squares with IQ "
                   "held fixed, <bookmark mark='f'/> and Mincer's equation on the 1976 survey. <bookmark mark='z'/> "
                   "The status: settled within a range, about six to fifteen percent a year.", "abcdef", fmt="{:.3f}")

    def supply(self):
        self._show(dials.DIALS["labour_supply"], r"labour supply \ (new)", 0, 1.4, [0, 0.25, 0.5, 0.75, 1.0, 1.25],
                   r"elasticity of hours or participation to the wage",
                   "The third, also new: how much people work more when pay rises. Chetty and his coauthors' "
                   "synthesis gives a Hicksian elasticity of 0.3 for hours, <bookmark mark='a'/> 0.25 for "
                   "participation, <bookmark mark='b'/> and Frisch elasticities of 0.5 <bookmark mark='c'/> and 0.25. "
                   "<bookmark mark='d'/> Uber's drivers, with hours they choose minute by minute, give 1.2. "
                   "<bookmark mark='z'/> The status: depends on the setting, and on whether the change is permanent "
                   "or temporary. Part forty-one puts the permanent ones to work on taxes.", "abcd", fmt="{:.2f}")
