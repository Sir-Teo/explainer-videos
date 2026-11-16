from __future__ import annotations

import numpy as np

from videos.music.music63.common import *  # noqa: F403


class Constellation(SoundScene):
    def construct(self):
        chapter(self, 1, r"A constellation of peaks", r"What part of a recording survives a noisy bar?")
        self.why()
        self.peaks()
        self.heard()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"a fingerprint must survive noise, \ a phone's microphone, \ a codec and a room", WHITE),
            (r"most of a spectrogram does not: \ quiet detail is buried first", WHITE),
            (r"what survives is the loudest point in each neighbourhood: \ a local peak", WHITE),
            (r"keep only the peaks' positions, \ time and frequency, \ and forget their heights: \ a constellation", TUNE),
        ]
        rows_scene(self, r"what survives", items,
                   "What part of a recording survives a noisy bar? <bookmark mark='b'/> A fingerprint must survive noise, a phone's "
                   "microphone, a codec and a room. <bookmark mark='c'/> Most of a spectrogram does not: the quiet detail is buried "
                   "first. <bookmark mark='d'/> What survives is the loudest point in each neighbourhood of time and frequency, a "
                   "local peak, because noise has to be louder than the music there to move it. <bookmark mark='e'/> So keep only "
                   "the peaks' positions, and forget their heights: Wang called the result a constellation.", marks="bcde")

    # ------------------------------------------------------------------
    def peaks(self):
        d = load("constellation")
        S = np.array(d["S"])
        top = S.max()
        w, h = 10.5, 3.6
        pic = picture(np.clip(S - top, -70, 0), -70, 0, w, h).move_to(DOWN * 0.3)
        x0, y0 = pic.get_left()[0], pic.get_bottom()[1]
        nf, nt = S.shape
        dots = VGroup(*[Dot([x0 + w * (t / 2 + 0.5) / nt, y0 + h * (b / 2 + 0.5) / nf, 0], radius=0.045, color=TUNE)
                        for t, b in d["peaks"] if b < 2 * nf and t < 2 * nt])
        note = label(rf"8 seconds of {d['name'].split('/')[1]}: \ about {d['per_second']:.0f} peaks a second \ (0 to 2 kHz shown)", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"a spectrogram, \ and its peaks", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here are eight seconds of a Variation, resampled to eight kilohertz for this fingerprint implementation. <bookmark mark='a'/> And its "
            f"constellation: about {say(d['per_second'])} peaks a second, each the loudest point in its neighbourhood. That is "
            "all the fingerprinter keeps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pic), FadeIn(note))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dd) for dd in dots], lag_ratio=0.005), run_time=2.0)
            self.play(pic.animate.set_opacity(0.25))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("constellation")
        c = clip("constellation.two")
        boxes = choice_boxes([r"the recording", r"only its peaks"], width=3.4, height=0.9, buff=1.0, size=20).move_to(UP * 0.5)
        note = label(r"each peak played as a short sine at its frequency: \ what the fingerprinter hears", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"the constellation, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the recording, and then only its peaks, each played as a short sine at its frequency: the song as the fingerprinter hears it."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"full, \ then peaks", kind="synthesized", detail=r"a Variation's fingerprint", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["full"], st["peaks"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["peaks"], c.duration, buff=0.08)
        with self.voiceover("A sparkle of beeps, in which the melody can just be followed. Little enough to search fast; enough to distinguish many recordings when sufficient peaks survive."):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
