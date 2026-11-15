from __future__ import annotations

import numpy as np

from videos.music.music64.common import *  # noqa: F403


class Phase(SoundScene):
    def construct(self):
        chapter(self, 7, r"The phase problem", r"Is a spectrogram's magnitude enough to rebuild a sound?")
        self.problem()
        self.heard()
        self.convergence()
        self.gap()
        self.waveform()

    # ------------------------------------------------------------------
    def problem(self):
        items = [
            (r"a mask scales magnitudes, \ and keeps the mixture's phase in every bin", WHITE),
            (r"where sources overlap, \ the mixture's phase is neither source's: \ the error that no mask can remove", WHITE),
            (r"Griffin and Lim \ (1984): \ a phase for a magnitude, \ by going back and forth between a spectrogram and a signal", WHITE),
            (r"it finds a consistent phase, \ not the true one", TUNE),
        ]
        rows_scene(self, r"phase", items,
                   "Masks have a blind spot. <bookmark mark='b'/> A mask scales magnitudes and keeps the mixture's phase in every "
                   "bin. <bookmark mark='c'/> Where sources overlap, the mixture's phase is neither source's, and that error no mask "
                   "can remove. <bookmark mark='d'/> Could the phase be rebuilt from the magnitude? Daniel Griffin and Jae Lim's "
                   "method of 1984 goes back and forth between a spectrogram and a signal, keeping the magnitude each time. "
                   "<bookmark mark='e'/> It finds a phase that is consistent, not the true one.", marks="bcde")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("phase")
        c = clip("phase.two")
        s = d["sdr"]
        boxes = choice_boxes([r"Griffin-Lim's phase", r"the mixture's phase"], width=3.8, height=0.9, buff=0.9, size=19).move_to(UP * 0.5)
        res = VGroup(label(rf"the true magnitude with the mixture's phase: \ {s['mixture_phase']:.1f} dB", font_size=18, color=TUNE),
                     label(rf"with Griffin-Lim's: \ {s['griffin_lim']:.1f} dB \ (scale-invariant: \ {s['si_griffin']:.1f})", font_size=18, color=EAR),
                     label(r"a phase that sounds right can still be far from the truth, \ sample by sample", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.25).next_to(boxes, DOWN, buff=0.5)
        head = label(r"the vocals' true magnitude, \ two phases", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Here is the vocals' true magnitude, first with a phase invented by Griffin and Lim's method, then with the mixture's phase."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two phases", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["griffin"], st["mixphase"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["mixphase"], c.duration, buff=0.08)
        with self.voiceover(
            "Griffin and Lim's sounds a little phasey and hollow, and by the waveform measure it is far from the truth, "
            f"{say(s['griffin_lim'], 1)} decibels: its phases are consistent but not the voice's own. The mixture's phase, wrong "
            f"only where the sources overlap, scores {say(s['mixture_phase'], 1)}. Phase is why masks have ceilings."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def waveform(self):
        items = [
            (r"so separate in the waveform itself: \ no spectrogram, \ no phase to lose", WHITE),
            (r"Wave-U-Net \ (2018), \ Demucs \ (Défossez et al., \ 2019): \ networks from samples to samples", WHITE),
            (r"later Demucs versions combine both: \ a spectrogram branch and a waveform branch, \ and a transformer between them", WHITE),
            (r"on MUSDB18, \ vocals have improved from a few dB SDR in 2015 to around 9 or more \ (verify the latest)", TUNE),
        ]
        rows_scene(self, r"separating waveforms", items,
                   "One answer is to avoid the spectrogram altogether. <bookmark mark='b'/> Separate in the waveform itself, with no "
                   "phase to lose. <bookmark mark='c'/> Wave-U-Net in 2018 and Demucs, from Alexandre Défossez and colleagues in "
                   "2019, are networks from samples to samples. <bookmark mark='d'/> Later Demucs versions combine both, a "
                   "spectrogram branch and a waveform branch with a transformer between them. <bookmark mark='e'/> On the MUSDB18 "
                   "benchmark, vocal separation improved from a few decibels around 2015 to about nine or more; check the latest.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def convergence(self):
        d = load("glcurve")
        it = np.array(d["iters"], float)
        inc, sd = np.array(d["inconsistency_db"]), np.array(d["sdr"])
        ax = frame_axes(width=8.5, height=3.2, xlo=0, xhi=100, ylo=-22, yhi=2, center=DOWN * 0.5 + LEFT * 0.6)
        c1 = curve(it, inc, ax.to, color=TUNE, width=3)
        c2 = curve(it, sd, ax.to, color=EAR, width=3)
        xl = label(r"iterations", font_size=14, color=GREY_A).next_to(ax, DOWN, buff=0.2)
        yl = label(r"dB", font_size=14, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        k1 = label(r"inconsistency: \ how far the signal's spectrogram is from the target magnitude", font_size=15, color=TUNE).move_to(ax.to(50, -18) + UP * 0.0).shift(UP * 0.0)
        k2 = label(r"SDR against the true vocals", font_size=15, color=EAR).move_to(ax.to(60, 0) + UP * 0.3)
        k1.next_to(ax.to(100, inc[-1]), LEFT, buff=0.2).shift(DOWN * 0.35)
        head = label(r"consistent is not correct", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Watch Griffin and Lim's method work. <bookmark mark='a'/> Iteration by iteration, the signal's spectrogram comes "
            f"closer to the target magnitude: from {say(-inc[0], 0)} decibels off to {say(-inc[-1], 0)} after a hundred rounds. "
            "<bookmark mark='b'/> And its distance from the true vocals does not move at all; the SDR stays near minus three. It "
            "finds a signal with the right spectrogram, and there are many, nearly all of them different from the voice "
            "sample by sample."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(k1), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(k2), run_time=1.4)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def gap(self):
        d = load("truephase")
        c = clip("truephase.two")
        card = listen_card(r"The vocals through the ideal ratio mask, \ twice: \ once with the mixture's phase, \ once with the voice's own. \ Which had the voice's own?", width=9.4)
        with self.voiceover("Your turn. How much does phase matter to the ear? Here are the vocals through the ideal ratio mask twice, once with the mixture's phase and once with the voice's own. Which had the voice's own?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"], width=3.2, height=0.9, buff=1.2, size=19).move_to(UP * 0.5)
        self.play(FadeOut(card), FadeIn(boxes))
        res = label(rf"{d['sdr_mix']:.1f} dB, \ then {d['sdr_true']:.1f} dB: \ the gap that better magnitudes alone cannot close", font_size=18, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"the phase gap, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        self.play(FadeIn(head))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two phases", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["mixphase"], st["truephase"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["truephase"], c.duration, buff=0.08)
        with self.voiceover(
            f"The second had the voice's own phase. By SDR, {say(d['sdr_mix'], 1)} decibels, then {say(d['sdr_true'], 1)}. Listen again where the band and the voice "
            "share a harmonic: that is where the two differ. Whether three decibels of SDR sound like much is a question for "
            "the ear, not the formula, and Chapter 9 takes it up."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
