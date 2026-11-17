from __future__ import annotations

import numpy as np
from scipy import stats

from videos.psychology.psych12.common import *  # noqa: F403


class Choice(VoiceoverScene):
    def construct(self):
        self.card()
        self.difference()
        self.curves()

    def card(self):
        card = chapter_card(7, r"Forced choice", r"Why does asking ``which one?'' take the caution out?",
                            lit=(), part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover(
            "Chapter seven. Forced choice."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def difference(self):
        d = load("afc")
        head = heading(r"Two intervals: \ compare, \ don't decide")
        A = axes([-4, 6], [0, 0.45], x_length=5.6, y_length=2.3, xticks=[-2, 0, 2, 4], yticks=[], xfmt=lambda v: f"{v:g}",
                 xlabel=r"evidence in each interval", ylabel=r"", center=[-3.9, 1.25, 0])
        g = gauss_pair(A.ax, 1.0, x0=-4, x1=6)
        B = axes([-4, 6], [0, 0.45], x_length=5.6, y_length=2.3, xticks=[-2, 0, 2, 4], yticks=[], xfmt=lambda v: f"{v:g}",
                 xlabel=r"signal interval minus blank interval", ylabel=r"", center=[-3.9, -1.7, 0])
        x = np.linspace(-4, 6, 300)
        y = stats.norm.pdf(x, 1.0, np.sqrt(2))
        diff = curve(B.ax, x, y, MODEL, stroke_width=4)
        right = area_under(B.ax, x, y, 0.0, 6.0, HIT, 0.4)
        zero = DashedLine(B.ax.c2p(0, 0), B.ax.c2p(0, 0.42), color=GREY_B, stroke_width=3)
        eqs = VGroup(
            MathTex(r"x_s - x_n \sim N\!\left(d',\; 2\right)", font_size=34, color=MODEL),
            MathTex(r"P(\text{correct}) = P(x_s - x_n > 0) = \Phi\!\left(\frac{d'}{\sqrt2}\right)", font_size=34, color=HIT),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows = rows_of([
            (r"no criterion: \ pick the interval with more evidence", WHITE),
            (r"the difference of two noisy numbers has twice the variance", MODEL),
            (rf"$d' = 1$: \ {pct(d['pc_at_1'])} correct, \ against {pct(d['yn_at_1'])} for an unbiased yes-no observer",
             HIT),
            (rf"and back: \ 75\% correct means $d' = \sqrt2\,z_{{0.75}} = {d['d_from_75']:.2f}$ \ (Part 11's JND)", THRESH),
        ], 5.6, 25, 0.24)
        side = VGroup(eqs, rows).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([3.5, -0.1, 0])
        keep_in_frame(side)
        tag = psyche_tag(r"computed: \ $d' = 1$")
        with self.voiceover(
            "Part eleven asked which of two intervals was brighter, and claimed that this question has no yes to be "
            "cautious about. Here's the reason in the theory. <bookmark mark='a'/> On each trial the observer gets "
            "two pieces of evidence, one from the signal interval and one from the blank, and simply picks the "
            "larger. There's no line to place. <bookmark mark='b'/> It's right whenever the difference between the "
            "two is positive. And the difference of two noisy numbers has twice the variance of either: its "
            "standard deviation is root two. <bookmark mark='c'/> So the chance of being right is the normal "
            "probability of d prime over root two. For d prime one, that's "
            f"{100 * d['pc_at_1']:.0f} percent, a little better than an unbiased yes-no observer's "
            f"{100 * d['yn_at_1']:.0f}, because the comparison uses two looks. <bookmark mark='d'/> Run it "
            "backwards and seventy-five percent correct means d prime of root two times the seventy-five percent "
            "quantile: point nine five. That's where the factor in Part 11's second problem came from."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(B), Create(diff), Create(zero), FadeIn(eqs[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(right), Write(eqs[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def curves(self):
        d = load("afc")
        head = heading(r"More alternatives, \ a lower floor")
        A = axes([0, 3], [0, 1], x_length=6.4, y_length=4.2, xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5, 0.75, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"$d'$", ylabel=r"share correct",
                 center=[-3.0, -0.2, 0])
        ax = A.ax
        cs = VGroup(curve(ax, d["ds"], d["two"], HIT, stroke_width=4), curve(ax, d["ds"], d["m4"], ROCC, stroke_width=4),
                    curve(ax, d["ds"], d["m8"], SIGNALC, stroke_width=4),
                    DashedLine(ax.c2p(0, 0.5), ax.c2p(3, 0.5), color=GREY_C, stroke_width=2))
        lg = legend([(HIT, r"2 alternatives"), (ROCC, r"4"), (SIGNALC, r"8")], font_size=23).move_to(ax.c2p(2.3, 0.3))
        rows = rows_of([
            (r"$m$ alternatives: \ right when the signal beats all $m - 1$ blanks", WHITE),
            (r"guessing gives $1/m$: \ the floor drops, \ the curve stretches", ROCC),
            (r"Part 11's eye chart is a choice among many letters, \ so its guess rate is small", GREY_A),
            (r"forced choice measures $d'$ without asking the observer to set a criterion; \ it trades that for "
             r"more trials", THRESH),
        ], 5.0, 26, 0.28).move_to([3.9, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ numerical integration")
        with self.voiceover(
            "Give the observer more alternatives, one signal hidden among several blanks. <bookmark mark='a'/> It's "
            "right when the signal's evidence beats every blank's, an integral the computer does in a moment. "
            "<bookmark mark='b'/> Guessing now succeeds one time in m, so the floor drops: a half for two "
            "alternatives, a quarter for four, an eighth for eight. <bookmark mark='c'/> That's why an eye chart, a "
            "choice among many letters, has a small guess rate. <bookmark mark='d'/> Forced choice buys a "
            "measurement of d prime that doesn't depend on the observer's caution, at the price of more trials. "
            "Yes-no and ratings buy the criterion as well, which matters whenever the criterion is what you're "
            "studying."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(cs[0]), Create(cs[3]))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs[1]), Create(cs[2]), FadeIn(lg), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
