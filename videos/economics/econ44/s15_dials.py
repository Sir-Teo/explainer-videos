from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ44.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 13, r"The Dials: \ merger retrospectives, \ patience", r"What do the numbers say?",
             "Chapter thirteen. The Dials: merger retrospectives, and patience.",
             lit={2013: r"Kwoka", 2017: r"Miller and Weinberg"}, scale=("firm", "market"), horizon=("a year",))
        self.dial_mergers()
        self.dial_beta()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}", extra=None):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.55, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.45)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip(marks, rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            if extra is not None:
                vo.wait_until("y")
                self.play(FadeIn(extra[0]))
                vo.wait_until("x")
                self.play(FadeIn(extra[1]))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def dial_mergers(self):
        self._show(dials.DIALS["merger_retro"], r"merger price effects, \ measured after \ (new)", 0, 12,
                   [0, 2, 4, 6, 8, 10, 12], r"percent change in the merging firms' prices",
                   "The first dial is new: what mergers did to prices, measured after the fact. John Kwoka's 2013 "
                   "review of 46 American mergers with published retrospectives: 38 were followed by price rises, "
                   "averaging almost ten percent. <bookmark mark='a'/> In his 2015 book, mergers the agencies had "
                   "challenged were followed by rises of about 7.7 percent, as reviewers report it. <bookmark "
                   "mark='b'/> "
                   "MillerCoors: about two percent from concentration, offset at the mean by the savings. "
                   "<bookmark mark='c'/> And six to eight percent above competition, by Miller and Weinberg's "
                   "structural estimate. <bookmark mark='d'/> The Island's simulated cereal merger: 5.8 percent. "
                   "<bookmark mark='z'/> The status: contested. Critics reply that the mergers studied are not a "
                   "random sample, and that averaging different studies misleads.", "abcd", fmt="{:.1f}")

    def dial_beta(self):
        R = load("rust")
        prof = [r for r in R["profile"] if r["beta"] in (0.0, 0.9, 0.99, 0.999, 0.9999)]
        cols = [[r"monthly $\beta$", r"log likelihood", r"rebuild cost, \ $RC$", r"cost slope, \ $\theta$"]]
        for r in prof:
            b = f"{r['beta']:g}"
            cols.append([b, f"{r['loglik']:.1f}".replace("-", "$-$"), f"{r['RC']:.2f}", f"{r['theta1']:.2f}"])
        grid = VGroup()
        for j, col in enumerate(cols):
            c = VGroup(*[label(t, font_size=17, color=(GREY_A if j == 0 else (MYOPIC if j == 1 else PATIENT)))
                         for t in col]).arrange(DOWN, buff=0.28)
            grid.add(c)
        grid.arrange(RIGHT, buff=0.75, aligned_edge=UP).move_to(DOWN * 0.95)
        for c in grid:
            for k, t in enumerate(c):
                t.set_y(grid[0][k].get_y())
        top = VGroup(*[VGroup(*[c[k] for c in grid]) for k in range(2)])
        bottom = VGroup(*[VGroup(*[c[k] for c in grid]) for k in range(2, 4)])
        self._show(dials.DIALS["dynamic_beta"], r"the discount factor of a dynamic decision maker \ (new)", 0.98, 1.0,
                   [0.98, 0.985, 0.99, 0.995, 1.0], r"monthly discount factor",
                   "The second, also new: how patient was Zurcher? On his buses, the best of the values tried is "
                   f"0.9999 a month, with a log likelihood of {say_num(R['nfxp']['loglik'], 1)}, against "
                   f"{say_num(R['myopic']['loglik'], 1)} for a myopic superintendent. <bookmark mark='y'/> Read the "
                   "likelihood across the values: it climbs steeply from zero to 0.99, then barely moves; everything "
                   "from 0.99 to 0.9999 fits almost equally well. <bookmark mark='x'/> Yet the costs it implies do "
                   f"move: the rebuild cost goes from {prof[2]['RC']:.1f} to {prof[-1]['RC']:.1f} and the cost "
                   f"slope from {prof[2]['theta1']:.1f} to {prof[-1]['theta1']:.1f}. <bookmark mark='z'/> The status: "
                   "not identified. The data reject myopia, but the exact discount factor usually has to be "
                   "assumed, and the estimated costs depend on the assumption.", "", fmt="{:.4f}",
                   extra=(top, bottom))
