from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


class Channels(VoiceoverScene):
    def construct(self):
        self.card()
        self.bank()
        self.adapt()
        self.normalize()

    def card(self):
        card = chapter_card(7, r"Channels and normalization", r"Is the CSF one filter, or many?",
                            lit={1969: r"Blakemore and Campbell", 1992: r"Heeger"}, part=PART, scale=("circuit", "mind"),
                            marr=("how",))
        with self.voiceover("Chapter seven. Channels, and normalization."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _axes(self, center):
        return axes([np.log10(0.5), np.log10(40)], [0, np.log10(300)], x_length=6.4, y_length=3.6,
                    xticks=[np.log10(v) for v in (0.5, 1, 2, 4, 8, 16, 32)], yticks=[0, 1, 2],
                    xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{10 ** v:g}",
                    xlabel=r"spatial frequency (cycles per degree)", ylabel=r"sensitivity", center=center)

    def bank(self):
        d = load("channels")
        head = heading(r"Many narrow filters under one curve")
        A = self._axes([-2.8, -0.3, 0])
        ax = A.ax
        lf = np.log10(d["f"])
        chans = VGroup(*[curve(ax, lf, np.log10(np.where(b >= 1.0, b, np.nan)),
                               interpolate_color(ManimColor(SURROUND), ManimColor(CENTRE), i / (len(d["bank"]) - 1)),
                               stroke_width=2.5) for i, b in enumerate(d["bank"])])
        env = curve(ax, lf, np.log10(np.maximum(d["before"], 1.0)), WHITE, stroke_width=5)
        rows = rows_of([
            (r"the hypothesis: \ the CSF is not one filter but the envelope of many, \ each tuned to a band of "
             r"frequencies about an octave wide", WHITE),
            (r"like the cortex's cells, \ each prefers a size of pattern, \ as well as an orientation", CELL),
            (r"how could you test it from outside, \ with nothing but a person and some gratings?", YOU),
        ], 5.0, 26, 0.32).move_to([4.1, -0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ a bank of channels, \ one octave wide")
        with self.voiceover(
            "Is the contrast sensitivity function one filter, or many? <bookmark mark='a'/> The hypothesis in the "
            "late nineteen-sixties was that it's the upper edge, the envelope, of many narrower filters, called "
            "channels, each tuned to a band of frequencies about an octave wide. <bookmark mark='b'/> That's what "
            "you'd expect if it were built from cells like Hubel and Wiesel's, each preferring one size of pattern "
            "as well as one orientation. <bookmark mark='c'/> But how would you test it, from the outside, with "
            "nothing but a person and some gratings?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in chans], lag_ratio=0.1), FadeIn(rows[0]), run_time=2.5)
            self.play(Create(env))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def adapt(self):
        d = load("channels")
        head = heading(r"Tire one channel, \ and look")
        A = self._axes([-2.8, -0.3, 0])
        ax = A.ax
        lf = np.log10(d["f"])
        before = curve(ax, lf, np.log10(np.maximum(d["before"], 1.0)), WHITE, stroke_width=4)
        after = curve(ax, lf, np.log10(np.maximum(d["after"], 1.0)), CENTRE, stroke_width=5)
        mark = DashedLine(ax.c2p(np.log10(d["adapter"]), 0), ax.c2p(np.log10(d["adapter"]), np.log10(300)), color=LIGHT,
                          stroke_width=2.5)
        ml = label(rf"adapter: \ {d['adapter']:g} c/deg", font_size=22, color=LIGHT).next_to(mark.get_top(), RIGHT, buff=0.1)
        rows = rows_of([
            (r"Blakemore and Campbell, \ 1969: \ stare for a minute at a high-contrast grating", LIGHT),
            (r"then measure the CSF again: \ a notch, \ thresholds up to five times higher near the adapting "
             r"frequency, \ and little change far from it", CENTRE),
            (r"one filter would have dimmed everywhere; \ a dent means separate channels", WHITE),
            (r"the same for orientation: \ adapt to vertical, \ and horizontal is spared", GREY_A),
        ], 5.0, 26, 0.32).move_to([4.1, -0.2, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(archive.BLAKEMORE_CAMPBELL_1969.cite),
                      psyche_tag(r"computed: \ the channel bank, \ one channel's gain cut"))
        with self.voiceover(
            "Colin Blakemore and Fergus Campbell found a way in 1969. <bookmark mark='a'/> Look for a minute or so "
            "at a high-contrast grating of one fineness, and the neurons that respond to it tire. "
            "<bookmark mark='b'/> Then measure the curve again. Thresholds near the adapting frequency rose as much "
            "as fivefold, but gratings much coarser or finer were barely affected. The curve gets a notch. "
            "<bookmark mark='c'/> A single filter would have dimmed everywhere at once. A notch means there are "
            "separate channels, and you tired one. <bookmark mark='d'/> The same works for orientation: tire the "
            "vertical channels, and horizontal gratings are spared. The channels are, very probably, populations of "
            "cells like the ones in chapter five."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tags), Create(before))
            vo.wait_until("a")
            self.play(Create(mark), FadeIn(ml), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(after), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def normalize(self):
        d = load("channels")
        head = heading(r"Divide by the neighbourhood: \ normalization")
        A = axes([-2, 0], [0, 1], x_length=5.6, y_length=3.4, xticks=[-2, -1, 0], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{100 * 10 ** v:g}\\%", xlabel=r"contrast of the preferred grating",
                 ylabel=r"response", center=[-3.6, 0.3, 0])
        ax = A.ax
        lc = np.log10(d["c"])
        crf = curve(ax, lc, d["crf"], CELL, stroke_width=5)
        mask = curve(ax, lc, d["crf_mask"], SURROUND, stroke_width=4)
        lg = legend([(CELL, r"alone"), (SURROUND, r"with a crossed grating on top")], font_size=21).move_to(ax.c2p(-1.45, 0.85))
        eq = MathTex(r"R_i = \frac{d_i^{\,n}}{\sigma^n + \sum_j d_j^{\,n}}", font_size=42).move_to([3.4, 2.0, 0])
        rows = rows_of([
            (r"each cell's drive, \ divided by the summed drive of its neighbours (Heeger, \ 1992)", WHITE),
            (r"responses saturate at high contrast, \ like the adaptation curve of chapter 3", CELL),
            (r"a grating the cell ignores still divides its response: \ cross-orientation masking", SURROUND),
            (r"double every input and the pattern of responses barely changes: \ what is kept is the pattern, \ not "
             r"the overall strength", GREY_A),
            (r"the same division turns up in smell, \ in attention, \ in value: \ a candidate canonical computation",
             LIGHT),
        ], 5.6, 24, 0.27).move_to([3.4, -1.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ divisive normalization")
        with self.voiceover(
            "One more operation, and it may be the most general. <bookmark mark='a'/> In 1992 David Heeger proposed "
            "that each cortical cell's drive is divided by the summed activity of its neighbours. "
            "<bookmark mark='b'/> It explains why responses saturate at high contrast: as the cell's own drive "
            "grows, so does the pool it's divided by. It's the gain control of chapter three, again. "
            "<bookmark mark='c'/> It explains something stranger: a grating the cell ignores entirely, laid across its "
            "preferred one, still suppresses its response, because it feeds the pool. <bookmark mark='d'/> And it "
            "means that doubling every input leaves the pattern of responses nearly unchanged: what's kept is the "
            "pattern, not the overall strength. <bookmark mark='e'/> The same division turns up in smell, in "
            "attention, in how the brain codes value. Matteo Carandini and Heeger called it a canonical neural "
            "computation. Part 58 asks why a brain would compute this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(crf), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(mask), FadeIn(lg), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
