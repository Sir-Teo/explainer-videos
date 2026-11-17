from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


class Csf(VoiceoverScene):
    def construct(self):
        self.card()
        self.chart()
        self.curve_()
        self.hybrid()

    def card(self):
        card = chapter_card(6, r"On you: \ your contrast sensitivity", r"Which patterns can you see at all?",
                            lit={1968: r"Campbell and Robson"}, part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter six. On you: your contrast sensitivity."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def chart(self):
        d = load("csf")
        head = heading(r"On you: \ where do the bars disappear?")
        img = picture(0.5 + 0.5 * d["chart"], 4.2, smooth=True).move_to([0, 0.0, 0])
        img.stretch_to_fit_width(9.2)
        fr = frame_box(img)
        xl = label(r"finer bars $\rightarrow$", font_size=24, color=GREY_A).next_to(img, DOWN, buff=0.15)
        yl = label(r"more contrast $\downarrow$", font_size=24, color=GREY_A).next_to(img, LEFT, buff=0.2).rotate(PI / 2)
        q = wrapped_label(r"follow, \ with your eye, \ the line where the bars fade into grey", 12.0, 30, YOU)
        q.to_edge(DOWN, buff=0.75)
        tag = note(r"the Campbell-Robson chart, \ computed; \ your screen and distance change it").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Time for an experiment on you. <bookmark mark='a'/> This is a Campbell-Robson chart. From left to right "
            "the bars get finer; from bottom to top their contrast falls, from black and white to almost uniform "
            "grey. Every column has the same range of contrast. <bookmark mark='b'/> Follow with your eye the line "
            "where the bars fade into the grey. It isn't flat. It rises to a hump somewhere in the middle and falls "
            "away on both sides: you need more contrast to see very coarse bars, and much more to see very fine "
            "ones. <bookmark mark='c'/> That boundary is your own contrast sensitivity function, drawn by your visual "
            "system on a picture that doesn't contain it. Its exact place depends on your screen and how far away "
            "you sit, so pause and try it nearer and farther if you like."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(img), Create(fr), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.1))
            vo.wait_until("c")
            self.wait(1.0)
        self.clear_scene()

    def curve_(self):
        d = load("csf")
        fit = d["fit"]
        head = heading(r"The contrast sensitivity function")
        A = axes([np.log10(0.25), np.log10(64)], [0, np.log10(400)], x_length=6.6, y_length=3.9,
                 xticks=[np.log10(v) for v in (0.5, 1, 2, 4, 8, 16, 32, 64)], yticks=[0, 1, 2],
                 xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{10 ** v:g}",
                 xlabel=r"spatial frequency (cycles per degree)", ylabel=r"sensitivity = 1 / threshold contrast",
                 center=[-2.8, -0.4, 0])
        ax = A.ax
        lf = np.log10(d["f"])
        truth = curve(ax, lf, np.log10(np.where(d["s"] >= 1, d["s"], np.nan)), GREY_B, stroke_width=3)
        pts = scatter(ax, np.log10(d["fq"]), np.log10(d["y"]), YOU, radius=0.08)
        fc = curve(ax, lf, np.log10(np.where(d["fit_curve"] >= 1, d["fit_curve"], np.nan)), MODEL, stroke_width=5)
        acu = Dot(ax.c2p(float(np.log10(d["acuity"])), 0), radius=0.08, color=LCONE)
        acl = label(rf"acuity: \ {d['acuity']:.0f} c/deg", font_size=21, color=LCONE).next_to(acu, UP + LEFT, buff=0.08)
        rows = rows_of([
            (r"sensitivity: \ one over the faintest contrast at which a grating is seen", WHITE),
            (rf"it peaks at a few cycles per degree (Campbell and Robson, \ 1968); \ in this model a contrast of "
             rf"{100 * d['peak_contrast']:.1f}\% is enough there", LIGHT),
            (r"falling at high frequencies: \ the optics and the mosaic; \ at low: \ the surround of chapter 4", GREY_A),
            (rf"four numbers describe it: \ peak sensitivity, \ peak frequency, \ width, \ and a low-frequency floor; "
             rf"\ fitted to eight thresholds: \ peak {fit['peak']:.1f} c/deg", MODEL),
            (r"where it meets full contrast is the finest grating you can see at all", LCONE),
        ], 4.8, 24, 0.27).move_to([4.2, -0.2, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(archive.CAMPBELL_ROBSON_1968.cite),
                      psyche_tag(r"simulated: \ one observer's thresholds, \ the median fit of 101"))
        with self.voiceover(
            "Measure that boundary properly, with gratings one at a time and a staircase from Part 11, and you get "
            "a curve. <bookmark mark='a'/> Sensitivity is one over the faintest contrast at which a grating can be "
            "seen. <bookmark mark='b'/> Fergus Campbell and John Robson measured it in 1968. It peaks at a few "
            "cycles per degree, where a good observer needs well under one percent of contrast. <bookmark mark='c'/> It falls at fine frequencies because of the optics and the mosaic, and "
            "at coarse ones because of the surround that cancels broad, even light. The retina's band-pass filter, "
            "seen from outside. <bookmark mark='d'/> Four numbers describe the curve: its peak sensitivity, the "
            "frequency of the peak, its width, and a floor at low frequencies. Here they're fitted to eight "
            "simulated thresholds. Lesmes and colleagues showed in 2010 that a computer choosing each trial well can "
            "estimate all four in about fifty trials, which is how it's now measured in eye clinics. "
            "<bookmark mark='e'/> Where the curve meets full contrast is the finest grating you can see at all: "
            "here, about fifty-six cycles per degree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(truth), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p, scale=1.5) for p in pts], lag_ratio=0.15), run_time=1.5)
            self.play(Create(fc), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(acu), FadeIn(acl), FadeIn(rows[4]))
        self.clear_scene()

    def hybrid(self):
        d = load("hybrid")
        head = heading(r"What your sensitivity hides: \ a hybrid image")
        h = picture(d["hybrid"], 3.0, smooth=True).move_to([-4.6, 0.9, 0])
        near = picture(d["near"], 3.0, smooth=True).move_to([0, 0.9, 0])
        far = picture(d["far"], 3.0, smooth=True).move_to([4.6, 0.9, 0])
        lh = label(r"the image", font_size=24, color=GREY_A).next_to(h, DOWN, buff=0.15)
        ln = label(r"through the CSF, \ 2$^\circ$ across", font_size=24, color=MODEL).next_to(near, DOWN, buff=0.15)
        lf = label(r"through the CSF, \ $\tfrac14^\circ$ across", font_size=24, color=MODEL).next_to(far, DOWN, buff=0.15)
        rows = rows_of([
            (r"a blurred A plus the fine edges of an E", WHITE),
            (r"up close the fine edges fall where the curve is high: \ you read E", MODEL),
            (r"from far away the same edges become finer than your acuity, \ and only the A is left: \ step back from "
             r"the screen and try it", YOU),
        ], 12.4, 26, 0.22).to_edge(DOWN, buff=0.8)
        tag = psyche_tag(r"computed: \ each frequency weighted by the CSF")
        with self.voiceover(
            "The curve also tells you what you can't see. <bookmark mark='a'/> This image is a hybrid: a heavily "
            "blurred letter A, added to only the fine edges of a letter E. <bookmark mark='b'/> Filter it through the "
            "contrast sensitivity function as it would fall on your retina up close, two degrees across, and the "
            "E's edges land near the peak of the curve. You read E. <bookmark mark='c'/> Now shrink it to a quarter "
            "of a degree, as if seen from across a room. The same edges are now finer than your acuity, the filter "
            "removes them, and only the A remains. Step back from your screen, and you can watch the E turn into an "
            "A. Nothing in the image changed. What changed is which part of it fell where you're sensitive."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h), FadeIn(lh), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(near), FadeIn(ln), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(far), FadeIn(lf), FadeIn(rows[2]))
        self.clear_scene()
