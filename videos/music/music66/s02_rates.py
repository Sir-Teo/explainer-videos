from __future__ import annotations

import numpy as np

from videos.music.music66.common import *  # noqa: F403


class Rates(SoundScene):
    def construct(self):
        chapter(self, 1, r"Why raw audio is hard", r"How many decisions is a second of sound?")
        self.zoom()
        self.numbers()
        self.mulaw()
        self.heard()

    # ------------------------------------------------------------------
    def numbers(self):
        rows_ = VGroup(
            label(r"a second of CD audio: \ 44,100 samples, \ 16 bits each, \ two channels: \ 1.4 million bits", font_size=20, color=WHITE),
            label(r"a model of raw sound must decide every sample: \ 16,000 a second even at a speech rate", font_size=20, color=WHITE),
            label(r"a three-minute song: \ about 2.88 million decisions at that rate, \ each depending on the ones before", font_size=20, color=WHITE),
            label(r"a phrase lasts seconds: \ to keep a melody in mind, \ a model must look back tens of thousands of samples", font_size=20, color=WHITE),
            label(r"compare a word: \ a few tokens a second of speech; \ the gap between text and sound is a factor of thousands", font_size=20, color=TUNE),
        ).arrange(DOWN, buff=0.38)
        head = label(r"the numbers", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Sound is a long sequence. <bookmark mark='a'/> A second of CD audio is 44,100 samples of 16 bits in each of two "
            "channels: one point four million bits. <bookmark mark='b'/> A model that writes raw sound must decide every "
            "sample, sixteen thousand a second at a sixteen-kilohertz mono sampling rate. <bookmark mark='c'/> A three-minute song "
            "is about 2.88 million decisions at that rate, each depending on the ones before. <bookmark mark='d'/> And a musical phrase "
            "lasts seconds, so to keep a melody in mind the model must look back tens of thousands of samples. "
            "<bookmark mark='e'/> A text model writes a few tokens for a second of speech; the gap is a factor of thousands."
        ) as vo:
            self.play(FadeIn(head))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mulaw(self):
        lines = VGroup(
            label(r"WaveNet's first step: \ fewer levels per sample, \ chosen to suit the ear", font_size=20, color=WHITE),
            MathTex(r"c = \operatorname{sign}(x)\,\frac{\ln(1 + \mu |x|)}{\ln(1 + \mu)}, \qquad \mu = 255", font_size=38, color=TUNE),
            label(r"then 256 equal steps of $c$: \ fine near silence, \ coarse when loud, \ as the telephone has done since the 1970s", font_size=19, color=WHITE),
            label(r"each sample becomes one of 256 classes: \ the network outputs a probability for each", font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.4)
        head = label(r"mu-law", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "WaveNet's first step was to make each decision smaller. <bookmark mark='a'/> Compand the sample: take a "
            "logarithm of its size, <bookmark mark='b'/> then cut the result into 256 equal steps. The steps are fine near "
            "silence and coarse when the sound is loud, where the ear forgives them; telephones have done this since the "
            "nineteen seventies. <bookmark mark='c'/> Each sample becomes one of 256 classes, and the network's job is to give "
            "a probability to each."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]))
            for mark, ln in zip("abc", lines[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("rates")
        c = clip("rates.two")
        boxes = choice_boxes([r"8 bits, \ equal steps", r"8 bits, \ mu-law"], width=3.8, height=0.9, buff=1.0, size=19).move_to(UP * 0.6)
        res = label(rf"signal to noise on the quiet phrase: \ {d['snr_linear']:.0f} dB, \ then {d['snr_mulaw']:.0f} dB", font_size=19, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"256 levels, \ two ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear a quiet bowed phrase with 256 equal levels, then with 256 mu-law levels, both turned up so you can hear the difference."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"equal, \ then mu-law", kind="synthesized", detail=r"Part 9's string, \ quietly", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["linear"], st["mulaw"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["mulaw"], c.duration, buff=0.08)
        with self.voiceover(
            f"Equal steps leave the quiet phrase {say(round(d['snr_linear']))} decibels above its own grit; mu-law, "
            f"{say(round(d['snr_mulaw']))}. The same 256 classes, spent where the ear needs them."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def zoom(self):
        d = load("zoom")
        def wave(ys, width, height, center, col, dots=False):
            ys = np.array(ys)
            ax = frame_axes(width=width, height=height, xlo=0, xhi=len(ys) - 1, ylo=-1, yhi=1, center=center)
            g = VGroup(ax, curve(np.arange(len(ys)), ys / (np.max(np.abs(ys)) + 1e-9), ax.to, color=col, width=2))
            if dots:
                g.add(*[Dot(ax.to(i, v / (np.max(np.abs(ys)) + 1e-9)), radius=0.05, color=WHITE) for i, v in enumerate(ys)])
            return g
        a = wave(d["second"], 11.0, 1.4, UP * 1.6, GREY_B)
        b = wave(d["note"], 11.0, 1.4, DOWN * 0.3, BLUE)
        c = wave(d["samples"], 11.0, 1.4, DOWN * 2.2, TUNE, dots=True)
        la = label(r"one second of a bowed phrase", font_size=15, color=GREY_B).next_to(a, UP, buff=0.05).align_to(a, LEFT)
        lb = label(r"50 ms of it: \ the string's waves", font_size=15, color=BLUE).next_to(b, UP, buff=0.05).align_to(b, LEFT)
        lc = label(r"2 ms: \ 32 samples, \ each a decision", font_size=15, color=TUNE).next_to(c, UP, buff=0.05).align_to(c, LEFT)
        with self.voiceover(
            "Look at a second of sound at three magnifications. <bookmark mark='a'/> The whole second: a phrase of a bowed "
            "string. <bookmark mark='b'/> Fifty milliseconds of it: the string's waves, repeating at the note's pitch. "
            "<bookmark mark='c'/> And two milliseconds: thirty-two samples, each a number. A generator that works on raw "
            "sound must choose every one of those numbers."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(la))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb))
            vo.wait_until("c")
            self.play(FadeIn(c), FadeIn(lc))
        self.wait(0.6)
        self.clear_scene()
