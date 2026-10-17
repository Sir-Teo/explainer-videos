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
        # frequency: how many times a second the air wobbles; a slow and a fast wobble side by side
        fq = VGroup()
        for i, (cyc, txt) in enumerate([(2, r"slow wobble: \ a low sound"), (7, r"fast wobble: \ a high sound")]):
            fa = Axes(x_range=[0, 1, 1], y_range=[-1, 1, 1], x_length=4.2, y_length=1.1, tips=False,
                      axis_config={"stroke_color": GREY_D, "stroke_width": 1, "include_ticks": False})
            fc = fa.plot(lambda t, c=cyc: np.sin(2 * PI * c * t), color=SND_C, stroke_width=3)
            fq.add(VGroup(fa, fc, label(txt, font_size=22, color=GREY_A).next_to(fa, DOWN, buff=0.15)))
        fq.arrange(RIGHT, buff=1.2).move_to(DOWN * 0.7)
        ft = label(r"frequency: \ how many times a second the air wobbles", font_size=26, color=SND_C).next_to(fq, UP, buff=0.4)
        with self.voiceover(
            "Sound is a wave: air pressure, sampled sixteen thousand times a second. Here's a synthetic voice saying "
            "five vowels. <bookmark mark='f'/> How many times a second the air wobbles is its frequency: slow wobbles "
            "sound low, fast ones sound high, and a voice mixes many at once. <bookmark mark='a'/> A wave is hard to "
            "read, so cut it into short frames, ten milliseconds apart, and measure how much of each frequency each "
            "frame has: a spectrogram. <bookmark mark='b'/> Now the vowels are visible: each has its own bright bands, "
            "the formants, which is how your ear tells a from e."
        ) as vo:
            self.play(Create(wl), FadeIn(tag), run_time=2.0)
            vo.wait_until("f")
            self.play(FadeIn(ft), Create(fq[0][0]), Create(fq[1][0]))
            self.play(Create(fq[0][1]), Create(fq[1][1]), FadeIn(fq[0][2]), FadeIn(fq[1][2]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(fq), FadeOut(ft), run_time=0.5)
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
        # a neural codec, schematic: wave -> encoder -> a few integers -> decoder (the vocoder) -> wave
        w = np.asarray(s["wave"], float)
        seg = w[1500:1590] / np.abs(w[1500:1590]).max()

        def wave_m(y, color, width=2.0, opacity=1.0):
            return VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity).set_points_as_corners(
                [[-1.0 + 2.0 * i / (len(y) - 1), 0.55 * float(v), 0] for i, v in enumerate(y)])

        def cbox(text, sub=None):
            b_ = RoundedRectangle(width=1.7, height=0.8, corner_radius=0.12, stroke_color=SND_C, stroke_width=2)
            t_ = label(text, font_size=22, color=SND_C).move_to(b_)
            return VGroup(b_, t_) if sub is None else VGroup(b_, t_, label(sub, font_size=18, color=GREY_A).next_to(b_, DOWN, buff=0.12))

        rebuilt = 0.85 * np.convolve(seg, [0.25, 0.5, 0.25], mode="same")
        w_in = wave_m(seg, GREY_A)
        enc_b, dec_b = cbox(r"encoder"), cbox(r"decoder", r"(the vocoder)")
        ints = VGroup(*[MathTex(str(int(c)), font_size=30, color=TOKEN_COLORS[int(c) % 8]) for c in codes[:6]]).arrange(RIGHT, buff=0.18)
        w_out = VGroup(wave_m(seg, GREY_D, 2.0), wave_m(rebuilt, SND_C, 2.5))
        pipe = Group(w_in, enc_b, ints, dec_b, w_out).arrange(RIGHT, buff=0.75).move_to(DOWN * 0.2)
        if pipe.width > 12.6:
            pipe.scale_to_fit_width(12.6)
        dec_b.shift(UP * (enc_b[0].get_y() - dec_b[0].get_y()))
        arrs = VGroup(*[Arrow(a_.get_right(), b_.get_left(), buff=0.08, stroke_width=2.5, color=GREY_B, max_tip_length_to_length_ratio=0.3)
                        for a_, b_ in zip([w_in, enc_b[0], ints, dec_b[0]], [enc_b[0], ints, dec_b[0], w_out])])
        pl = VGroup(label(r"sound", font_size=20, color=GREY_A).next_to(w_in, DOWN, buff=0.25),
                    label(r"a few small integers", font_size=20, color=GREY_A).next_to(ints, DOWN, buff=0.25),
                    label(r"rebuilt, \ over the original", font_size=20, color=GREY_A).next_to(w_out, DOWN, buff=0.25))
        ct = label(r"a neural codec: \ a coder and a decoder, \ trained together", font_size=26, color=SND_C).to_edge(UP, buff=1.0)
        ctag = note(r"schematic").to_corner(DR, buff=0.25)
        with self.voiceover(
            "Then the same trick as for pictures. <bookmark mark='a'/> Each frame becomes a few code numbers, from "
            "residual quantization in four stages. <bookmark mark='b'/> From those codes alone, the spectrogram comes "
            "back nearly intact. <bookmark mark='c'/> Real speech models use a neural codec trained for this: a coder "
            "and a decoder. The encoder half turns sound into a short list of codes; the decoder half, often called "
            "a vocoder, turns codes back into a wave. In the end, a voice is a stream of small integers, a few dozen "
            "a second per stage, that a transformer can predict like text."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in strip], lag_ratio=0.005), FadeIn(sl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bot), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeOut(Group(top, tl, strip, sl, bot, bl)), run_time=0.6)
            self.play(FadeIn(ct), Create(w_in), FadeIn(pl[0]), FadeIn(ctag))
            self.play(GrowArrow(arrs[0]), FadeIn(enc_b), GrowArrow(arrs[1]), LaggedStart(*[FadeIn(m_, scale=0.6) for m_ in ints], lag_ratio=0.15),
                      FadeIn(pl[1]), run_time=1.6)
            self.play(GrowArrow(arrs[2]), FadeIn(dec_b), GrowArrow(arrs[3]), Create(w_out), FadeIn(pl[2]), run_time=1.6)
        self.wait(0.3)
        self.clear_scene()
