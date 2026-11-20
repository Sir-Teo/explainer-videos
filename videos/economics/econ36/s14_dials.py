from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ36.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The Dials: \ elasticities, \ pass-through, \ local jobs", r"What do the numbers say?",
             "Chapter twelve. The Dials: elasticities, pass-through, local jobs.",
             lit={2013: r"Autor, \ Dorn and Hanson", 2023: r"Boehm et al."}, scale=("nation", "world"),
             horizon=("a year", "a decade"))
        self.elasticity()
        self.passthrough()
        self.jobs()

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

    def elasticity(self):
        self._show(dials.DIALS["trade_elasticity"], r"the trade elasticity \ (new)", 0, 10, [0, 2, 4, 6, 8, 10],
                   r"absolute value", "The first dial is new: the trade elasticity, the number at the heart of the "
                   "gains formula. Gravity studies across countries put it between five and ten. "
                   "<bookmark mark='a'/> Christoph Boehm, Andrei Levchenko and Nitya Pandalai-Nayar traced tariff "
                   "changes over time instead: under one in the first year, <bookmark mark='b'/> about two after a "
                   "decade. <bookmark mark='z'/> The status: depends on the setting, and on the horizon. Since the "
                   "gains from trade rise as the elasticity falls, the long-run values imply larger gains.",
                   "ab", fmt="{:.2f}")

    def passthrough(self):
        self._show(dials.DIALS["passthrough"], r"pass-through \ (two rows added)", 0, 1.1, [0, 0.25, 0.5, 0.75, 1],
                   r"share reaching US import prices", "The pass-through dial, opened in Part thirty-four for "
                   "exchange rates, gains two rows for tariffs. <bookmark mark='a'/> <bookmark mark='b'/> "
                   "<bookmark mark='c'/> <bookmark mark='d'/> Amiti, Redding and Weinstein, and Fajgelbaum and "
                   "coauthors: for the tariffs of 2018 and 2019, complete. <bookmark mark='z'/> Exchange rates pass "
                   "through little because prices are set in dollars; tariffs pass through fully because they are "
                   "charged on the dollar price.", "abcd")

    def jobs(self):
        self._show(dials.DIALS["import_competition_jobs"], r"import competition and local jobs \ (new)", -0.8, 0.0,
                   [-0.8, -0.6, -0.4, -0.2, 0.0], r"points of employment per \$1,000 of exposure",
                   "The third is new: the local effect of import competition on manufacturing jobs. "
                   "<bookmark mark='a'/> Autor, Dorn and Hanson's least squares, minus 0.17, "
                   "<bookmark mark='b'/> and the Island's instrumented estimate, close to the planted minus 0.6. "
                   "<bookmark mark='z'/> The status: settled within a range for the China shock itself; how far it "
                   "generalizes to other shocks and places is open.", "ab", fmt="{:.2f}")
