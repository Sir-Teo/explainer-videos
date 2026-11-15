from __future__ import annotations

import numpy as np

from videos.music.music49.common import *  # noqa: F403


class Phase(SoundScene):
    def construct(self):
        chapter(self, 4, r"Phase", r"Does it matter when each frequency arrives?")
        self.delay()
        self.quiz()
        self.groupdelay()
        self.linear()

    # ------------------------------------------------------------------
    def delay(self):
        items = [
            (r"a filter changes each frequency's level, \ and also its timing: \ the phase response", WHITE),
            (r"group delay: \ how late each frequency's energy arrives, \ the slope of the phase", WHITE),
            (r"an all-pass filter changes no level at all, \ only the timing", WHITE),
            (r"for a steady tone, \ a phase shift is almost inaudible \ (Part 4)", TUNE),
            (r"for a sharp attack, \ where every frequency must arrive together, \ it can be heard", GREY_A),
        ]
        rows_scene(self, r"timing, \ frequency by frequency", items,
                   "A filter does two things to each frequency. <bookmark mark='b'/> It changes its level, and also its timing: "
                   "the phase response. <bookmark mark='c'/> The group delay says how late each frequency's energy arrives; it is "
                   "the slope of the phase. <bookmark mark='d'/> An all-pass filter changes no level at all, only the timing. "
                   "<bookmark mark='e'/> For a steady tone a phase shift is almost inaudible, as Part 4 found. "
                   "<bookmark mark='f'/> For a sharp attack, where every frequency must arrive together, it can be heard.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("phase")
        c = clip("phase.two")
        card = listen_card(r"A snare, \ twice dry and twice through a filter that changes no frequency's level, \ in some order. \ Which was filtered?", width=9.6)
        with self.voiceover("Hear it. A snare struck twice dry, and twice through a filter that changes no frequency's level, in some order. Which was filtered?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.1, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(ORIGIN)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.6).move_to(UP * 1.4)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"a snare, \ twice", detail=r"Part 40's snare", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        n = len(d["dry"])
        a1 = frame_axes(width=5.2, height=1.8, xlo=0, xhi=n, ylo=-1, yhi=1, center=LEFT * 3.2 + DOWN * 1.2)
        a2 = frame_axes(width=5.2, height=1.8, xlo=0, xhi=n, ylo=-1, yhi=1, center=RIGHT * 3.2 + DOWN * 1.2)
        k = np.arange(n)
        dr = np.array(d["dry"]) / max(np.abs(d["dry"]))
        we = np.array(d["wet"]) / max(np.abs(d["wet"]))
        g1 = VGroup(a1, curve(k, dr, a1.to, color=GREY_A, width=1.5), label(r"dry: \ 120 ms", font_size=16, color=GREY_A).next_to(a1, UP, buff=0.1))
        g2 = VGroup(a2, curve(k, we, a2.to, color=TUNE, width=1.5), label(rf"through {d['stages']} all-passes", font_size=16, color=TUNE).next_to(a2, UP, buff=0.1))
        with self.voiceover(
            f"The second. Sixty first-order all-passes in a row delay the low frequencies more than the high ones: the snare's "
            "crack is smeared into a downward chirp, a zap. <bookmark mark='a'/> The waveforms show it: the dry hit is "
            "compact; the filtered one starts with its highest frequencies and ends with its lowest. And yet its spectrum's "
            "levels are the same as the dry hit's everywhere, to within a millionth of a decibel."
        ) as vo:
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
            vo.wait_until("a")
            self.play(FadeIn(g1), FadeIn(g2))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def groupdelay(self):
        d = load("phase")
        ax = logf_axes(width=9.0, height=3.2, flo=30, fhi=20000, ylo=0, yhi=max(d["group_delay_ms"]) * 1.1, center=DOWN * 0.3, ticks=(100, 1000, 10000))
        cv = curve(d["f"], d["group_delay_ms"], ax.to, color=TUNE, width=3)
        yl = label(r"delay, \ ms", font_size=16, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        g0 = max(d["group_delay_ms"])
        g1 = min(d["group_delay_ms"])
        head = label(rf"the group delay of {d['stages']} all-passes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Here is the delay the sixty all-passes give each frequency. <bookmark mark='a'/> The lowest frequencies are held "
            f"back about {say(g0)} milliseconds; the highest pass in {say(g1, 1)}. Spread a click's frequencies over twenty "
            "milliseconds like that, and the ear hears the order they arrive in: high first, then low, a falling chirp."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(cv), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linear(self):
        items = [
            (r"a symmetric FIR filter delays every frequency equally: \ linear phase, \ no smearing", WHITE),
            (r"but its delay is half its length, \ and its ringing comes before the attack as well as after: \ pre-echo", WHITE),
            (r"a minimum-phase filter puts all its energy as early as possible: \ no pre-echo, \ some phase distortion", WHITE),
            (r"analogue filters, \ and the biquads modelled on them, \ are minimum phase", TUNE),
            (r"mastering engineers choose between them by ear, \ case by case", GREY_A),
        ]
        rows_scene(self, r"linear phase and minimum phase", items,
                   "Can a filter avoid smearing? <bookmark mark='b'/> A symmetric FIR filter delays every frequency equally: linear "
                   "phase, no smearing. <bookmark mark='c'/> But its delay is half its length, and its ringing comes before the "
                   "attack as well as after: pre-echo. <bookmark mark='d'/> A minimum-phase filter puts all its energy as early "
                   "as it can: no pre-echo, but some phase distortion. <bookmark mark='e'/> Analogue filters, and the biquads "
                   "modelled on them, are minimum phase. <bookmark mark='f'/> Mastering engineers choose between the two by ear, "
                   "case by case.", marks="bcdef")
