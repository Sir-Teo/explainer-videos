from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import SND_C, TOKEN_COLORS, heat, load


class Sound(VoiceoverScene):
    def construct(self):
        self.card()
        self.wave()
        self.codes()

    def card(self):
        card = chapter_card(3, r"Sound as tokens", r"How does a voice become a sequence?", part=16)
        with self.voiceover("Chapter three. Sound as tokens."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def wave(self):
        s = load("sound")
        w = np.asarray(s["wave"])
        spec = np.asarray(s["spec"])
        vow = [str(x) for x in s["vowels"]]
        ax = Axes(x_range=[0, len(w), len(w) / 5], y_range=[-1.1, 1.1, 1], x_length=11.0, y_length=1.6, tips=False,
                  axis_config={"stroke_width": 0}).move_to(UP * 2.2)
        wn = w / np.abs(w).max()
        wl = VMobject(color=SND_C, stroke_width=1).set_points_as_corners([ax.c2p(i, float(wn[i])) for i in range(0, len(w), 2)])
        img = heat(spec[::-1], 11.0, 3.2, color=SND_C).move_to(DOWN * 0.6)
        frame = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.5)
        vl = VGroup(*[label(rf"``{v}''", font_size=26, color=WHITE).move_to(img.get_corner(UL) + RIGHT * 11.0 * (i + 0.5) / 5 + UP * 0.3)
                      for i, v in enumerate(vow)])
        fl = label(r"frequency $\uparrow$", font_size=20, color=GREY_B).rotate(PI / 2).next_to(img, LEFT, buff=0.1)
        tl = label(rf"time $\to$: \ one column every ${float(s['frame_ms']):.0f}$ ms", font_size=20, color=GREY_B).next_to(img, DOWN, buff=0.12)
        tag = note(r"a synthesized voice: \ a pulse train through each vowel's formant resonances").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Sound is a wave: air pressure, sampled sixteen thousand times a second. Here's a synthetic voice saying "
            "five vowels. <bookmark mark='a'/> A wave is hard to read, so cut it into short frames, ten milliseconds "
            "apart, and measure how much of each frequency each frame has: a spectrogram. <bookmark mark='b'/> Now "
            "the vowels are visible: each has its own bright bands, the formants, which is how your ear tells a from "
            "e."
        ) as vo:
            self.play(Create(wl), FadeIn(tag), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(img), Create(frame), FadeIn(fl), FadeIn(tl), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(vl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def codes(self):
        s = load("sound")
        spec, rec = np.asarray(s["spec"]), np.asarray(s["rec4"])
        codes = np.asarray(s["codes1"])
        errs = [float(e) for e in s["rec_errs"]]
        top = heat(spec[::-1], 11.0, 1.8, color=SND_C).move_to(UP * 2.0)
        bot = heat(rec[::-1], 11.0, 1.8, color=SND_C).move_to(DOWN * 1.5)
        n = len(codes)
        cw = 11.0 / n
        strip = VGroup(*[Rectangle(width=cw, height=0.42, stroke_width=0, fill_color=TOKEN_COLORS[int(c) % 8],
                                   fill_opacity=0.35 + 0.6 * (int(c) % 4) / 3).move_to([-5.5 + cw * (i + 0.5), 0.25, 0])
                         for i, c in enumerate(codes)])
        tl = label(r"the frames", font_size=22, color=GREY_A).next_to(top, UP, buff=0.08).align_to(top, LEFT)
        sl = label(r"each frame's code, \ stage $1$ of $4$ \ ($32$ codes)", font_size=22, color=GREY_A).next_to(strip, UP, buff=0.06)
        sl.align_to(top, LEFT)
        bl = label(rf"rebuilt from $4$ codes a frame: \ error ${errs[-1]:.3f}$ \ (one stage: \ ${errs[0]:.3f}$)", font_size=22,
                   color=GREY_A).next_to(bot, DOWN, buff=0.1).align_to(bot, LEFT)
        with self.voiceover(
            "Then the same trick as for pictures. <bookmark mark='a'/> Each frame becomes a few code numbers, from "
            "residual quantization in four stages. <bookmark mark='b'/> From those codes alone, the spectrogram comes "
            "back nearly intact. Real speech models use a neural codec trained for this, and a vocoder to turn the "
            "result back into a wave; but in the end, a voice is a stream of small integers, a few dozen a second "
            "per stage, that a transformer can predict like text."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in strip], lag_ratio=0.005), FadeIn(sl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bot), FadeIn(bl))
        self.wait(0.3)
        self.clear_scene()
