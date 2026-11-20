from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ37.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 14, r"The Dials: \ agglomeration and housing supply", r"What do the numbers say?",
             "Chapter fourteen. The Dials: agglomeration and housing supply.",
             lit={2010: r"Saiz; \ Combes et al.", 2015: r"Ahlfeldt et al."}, scale=("city", "nation"),
             horizon=("a decade",))
        self.agglomeration()
        self.housing()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}"):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.55, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip(marks, rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def agglomeration(self):
        self._show(dials.DIALS["agglomeration"], r"the agglomeration elasticity \ (new)", 0, 9, [0, 2, 4, 6, 8],
                   r"percent more productive per doubling of density",
                   "The first dial is new: how much more productive a worker is where work is twice as dense. "
                   "Antonio Ciccone and Robert Hall, across American states, found five or six percent. "
                   "<bookmark mark='a'/> Combes and his coauthors' raw French estimate is about three and a half; "
                   "<bookmark mark='b'/> following the same workers, with instruments from history and geology, "
                   "brings it to between one and two. <bookmark mark='c'/> Within Berlin, holding commutes fixed, "
                   "about five. <bookmark mark='d'/> Stuart Rosenthal and William Strange's survey spans three to "
                   "eight. <bookmark mark='e'/> On the Island, the movers recover the planted two. "
                   "<bookmark mark='z'/> The status: settled within a range. Small for a worker, large summed over a "
                   "city of millions.", "abcde", fmt="{:.1f}")

    def housing(self):
        self._show(dials.DIALS["housing_supply"], r"the elasticity of housing supply \ (new)", 0, 6,
                   [0, 1, 2, 3, 4, 5, 6], r"percent more housing for a 1\% higher price",
                   "The second, also new: the elasticity of housing supply. Albert Saiz's estimates run from Miami, "
                   "<bookmark mark='a'/> and San Francisco, below one, <bookmark mark='b'/> through one elasticity "
                   "for all cities, one and a half, <bookmark mark='c'/> and the population-weighted average, "
                   "<bookmark mark='d'/> to Houston, <bookmark mark='e'/> and Wichita above five. "
                   "<bookmark mark='z'/> The status: depends on the setting. Where it is low, a boom becomes rent; "
                   "where it is high, more homes and more people.", "abcde", fmt="{:.2f}")
