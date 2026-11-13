from __future__ import annotations

import numpy as np

from videos.music.music3.common import *  # noqa: F403


class ConstantQ(SoundScene):
    def construct(self):
        chapter(self, 8, r"A ruler for music", r"Why should every bin be the same width?", lit=(1807,),
                extra=((1991, r"Brown's constant-Q transform"),))
        self.mismatch()
        self.pictures()

    # ------------------------------------------------------------------
    def mismatch(self):
        d = load("cq")
        x0, x1 = -6.0, 6.0
        fmax = 2100.0
        top = Line([x0, 1.6, 0], [x1, 1.6, 0], color=GREY_C, stroke_width=2)

        def X(f):
            return x0 + (x1 - x0) * f / fmax

        ticks = VGroup(*[Line([X(f), 1.5, 0], [X(f), 1.7, 0], color=GREY_C, stroke_width=1) for f in np.arange(0, fmax, 46.875)])
        cs = [65.41 * 2 ** k for k in range(6)]
        marks = VGroup(*[VGroup(Line([X(f), 1.6, 0], [X(f), 2.2, 0], color=TUNE, stroke_width=3),
                                label(rf"C{k + 2}", font_size=22, color=TUNE).move_to([X(f), 2.45, 0])) for k, f in enumerate(cs)])
        t1 = label(r"equal steps in hertz: \ the transform's bins", font_size=26, color=GREY_A).next_to(top, DOWN, buff=0.25)
        counts = VGroup(label(r"the octave C2 to C3: \ 65 Hz wide", font_size=26, color=BAD), label(r"the octave C6 to C7: \ 1{,}047 Hz wide", font_size=26, color=GOOD)
                        ).arrange(RIGHT, buff=1.0).next_to(t1, DOWN, buff=0.3)
        # the musical ruler: equal steps in ratio
        low = Line([x0, -1.9, 0], [x1, -1.9, 0], color=GREY_C, stroke_width=2)

        def XL(f):
            return x0 + (x1 - x0) * np.log2(f / 65.41) / 5.0

        ticks2 = VGroup(*[Line([XL(65.41 * 2 ** (k / 12)), -2.0, 0], [XL(65.41 * 2 ** (k / 12)), -1.8, 0], color=GREY_C, stroke_width=1) for k in range(61)])
        marks2 = VGroup(*[VGroup(Line([XL(f), -1.9, 0], [XL(f), -1.3, 0], color=TUNE, stroke_width=3),
                                 label(rf"C{k + 2}", font_size=22, color=TUNE).move_to([XL(f), -1.05, 0])) for k, f in enumerate(cs)])
        t2 = label(rf"equal steps in ratio: \ every bin the same musical width, \ $Q = f / \Delta f = {d['q']:.0f}$", font_size=26, color=GREY_A).next_to(low, DOWN, buff=0.25)
        with self.voiceover(
            "The transform has one more awkwardness, and this one is about music in particular. Its bins are "
            "equally spaced in hertz. Musical notes are not. <bookmark mark='a'/> Each octave is a doubling, so the "
            "octave from the lowest C here to the next is sixty-five hertz wide, and the octave four above it is a "
            "thousand hertz wide. Equal bins give the bottom octave almost nothing and waste hundreds on the top. "
            "<bookmark mark='b'/> The remedy is a ruler marked the way a keyboard is: equal steps in ratio. Make "
            "each bin a fixed fraction of its own frequency. That fraction is called Q, and a transform built this "
            "way is a constant-Q transform. <bookmark mark='c'/> It pays for its fine low bins with time, as Gabor "
            f"says it must: the lowest bin here listens for {say(d['window_low_ms'])} milliseconds, the highest for "
            f"{say(d['window_high_ms'])}."
        ) as vo:
            self.play(FadeIn(top), FadeIn(ticks), FadeIn(t1))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.2), FadeIn(counts), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(low), FadeIn(ticks2), LaggedStart(*[FadeIn(m) for m in marks2], lag_ratio=0.2), FadeIn(t2), run_time=2.0)
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pictures(self):
        d = load("cq")
        c = clip("stft.phrase")
        lin = picture(d["lin"], -55, 0, 5.9, 3.6)
        cq = picture(d["cq"], -55, 0, 5.9, 3.6)
        Group(lin, cq).arrange(RIGHT, buff=0.6).move_to(UP * 0.2)
        caps = VGroup(label(r"equal bins in hertz", font_size=26, color=GREY_A).next_to(lin, UP, buff=0.12),
                      label(r"constant Q: \ a quarter-tone per bin", font_size=26, color=TUNE).next_to(cq, UP, buff=0.12))
        with self.voiceover(
            "Here is the Tune's opening both ways. On the left, equal bins: the notes are crushed into the bottom "
            "of the picture, and the stack of stripes above each note is spaced differently for every pitch. "
            "<bookmark mark='a'/> On the right, constant Q. The notes step up and down by even amounts, like a "
            "piano roll. And every note now has the same pattern of stripes above it, only moved up or down."
        ) as vo:
            self.play(FadeIn(lin), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(FadeIn(cq), FadeIn(caps[1]))
        with self.listen(c) as snd:
            window(snd, r"the Tune's opening, \ on both rulers", corner=DL, tag_corner=UR)
            for p_ in (lin, cq):
                p_.playhead.set_opacity(1)
                snd.drive(p_.playhead, sweep(p_, d["seconds"]))
        lin.playhead.set_opacity(0), cq.playhead.set_opacity(0)
        facts = VGroup(label(rf"all {d['notes']} notes of the first phrase land in the bin of their pitch", font_size=24, color=GOOD),
                       label(r"a note moved in pitch is the same picture, \ shifted: \ what machines that read music rely on (Parts 61, 62)", font_size=24, color=GREY_A),
                       label(r"the ear's own analysis is closer to this ruler than to the other (Part 4)", font_size=24, color=EAR)
                       ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "That shifting is the point. On this ruler a melody moved to another key is the same picture, slid up "
            "or down, which is why nearly every machine that transcribes or recognises music starts here. "
            "<bookmark mark='a'/> It was worked out by Judith Brown in 1991, and the wavelets you may have heard of "
            "are the same idea. <bookmark mark='b'/> There is a much older instrument that uses a ruler like this "
            "one, and it is inside your head. That is the next part."
        ) as vo:
            self.play(Group(lin, cq, caps).animate.shift(UP * 0.35), FadeIn(facts[0]), FadeIn(facts[1]), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()
