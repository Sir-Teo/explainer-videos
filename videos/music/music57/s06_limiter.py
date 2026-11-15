from __future__ import annotations

import numpy as np

from videos.music.music57.common import *  # noqa: F403


class Limiter(SoundScene):
    def construct(self):
        chapter(self, 5, r"Limiters and clippers", r"How do you make a record louder without letting a single peak through?")
        self.how()
        self.zoom()
        self.heard()
        self.clippers()

    # ------------------------------------------------------------------
    def how(self):
        items = [
            (r"a compressor with an infinite ratio and an instant attack: \ nothing passes the ceiling", WHITE),
            (r"but an instant gain change is itself a distortion: \ the gain must start falling before the peak arrives", WHITE),
            (r"look-ahead: \ at each moment, \ the least gain needed over the next 1.5 ms, \ glided down in time", WHITE),
            (r"the detector watches the true peak \ (4$\times$ oversampled), \ so no inter-sample over escapes", WHITE),
            (r"then a release of 80 ms lets the gain recover; \ a final clip at the ceiling catches what is left", TUNE),
        ]
        rows_scene(self, r"a look-ahead limiter", items,
                   "The tool that won the loudness war is the limiter. <bookmark mark='b'/> It is a compressor with an infinite "
                   "ratio and an instant attack: nothing passes the ceiling. <bookmark mark='c'/> But an instant change of gain is a "
                   "distortion in itself, so the gain must start falling before the peak arrives. <bookmark mark='d'/> Monochord's "
                   "limiter looks ahead: at each moment it takes the least gain needed over the next one and a half milliseconds, "
                   "and glides down to it. <bookmark mark='e'/> Its detector watches the true peak, oversampled four times, so no "
                   "inter-sample over escapes. <bookmark mark='f'/> Then a release of eighty milliseconds lets the gain recover, and "
                   "a final clip at the ceiling catches anything left.", marks="bcdef")

    # ------------------------------------------------------------------
    def zoom(self):
        d = load("limiter")
        z = d["zoom"]
        t = np.array(z["t"])
        a1 = frame_axes(width=10.4, height=2.2, xlo=t[0], xhi=t[-1], ylo=-1.6, yhi=1.6, center=UP * 0.8)
        cin = VMobject(stroke_color=GREY_D, stroke_width=1.5).set_points_as_corners([a1.to(x, v) for x, v in zip(t, np.clip(z["in"], -1.55, 1.55))])
        ccl = VMobject(stroke_color=EAR, stroke_width=2).set_points_as_corners([a1.to(x, v) for x, v in zip(t, z["clip"])])
        cli = VMobject(stroke_color=TUNE, stroke_width=2).set_points_as_corners([a1.to(x, v) for x, v in zip(t, z["lim"])])
        ceil = VGroup(DashedLine(a1.to(t[0], 0.891), a1.to(t[-1], 0.891), color=RED, stroke_width=1.5), DashedLine(a1.to(t[0], -0.891), a1.to(t[-1], -0.891), color=RED, stroke_width=1.5))
        a2 = frame_axes(width=10.4, height=1.4, xlo=t[0], xhi=t[-1], ylo=-10, yhi=0, center=DOWN * 1.9)
        gr = curve(t, np.clip(z["gain"], -10, 0), a2.to, color=TUNE, width=3)
        g2l = label(r"the limiter's gain, \ dB \ (0 to $-10$)", font_size=14, color=TUNE).next_to(a2, UP, buff=0.05).align_to(a2, LEFT)
        key = VGroup(label(r"pushed to $-8$ LUFS, \ before", font_size=15, color=GREY_B), label(r"clipped", font_size=15, color=EAR), label(r"limited", font_size=15, color=TUNE)).arrange(RIGHT, buff=0.6).next_to(a1, UP, buff=0.1)
        head = label(r"0.6 seconds, \ close up", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is six tenths of a second of our mix pushed to about minus eight LUFS, close up, with the ceiling at minus "
            "one. <bookmark mark='a'/> In grey, the signal before: its drum hits go far over. <bookmark mark='b'/> A clipper "
            "slices them off: flat tops, corners and all. <bookmark mark='c'/> The limiter turns the whole signal down around "
            f"each hit, by up to {say(d['gr_max'])} decibels, gliding down just before it and recovering after, so the "
            "waveform keeps its shape and only its size changes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a1), FadeIn(ceil), FadeIn(a2), FadeIn(g2l), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(Create(cin), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(ccl), FadeIn(key[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(cli), Create(gr), FadeIn(key[2]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("limiter")
        c = clip("limiter.two")
        boxes = choice_boxes([r"clipped", r"limited"], width=3.0, height=0.9, buff=1.4, size=22).move_to(UP * 0.6)
        res = label(rf"the same loudness; \ the clipped one's true peak {d['clip_tp']:+.1f} dBTP, \ the limited one's {d['lim_tp']:+.1f}", font_size=18, color=GREY_A).move_to(DOWN * 1.0)
        head = label(r"clipping and limiting, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear both at the same loudness: clipped, then limited. Listen to the drums."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(res))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"clipped, \ then limited", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["clipped"], st["limited"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["limited"], c.duration, buff=0.08)
        with self.voiceover(
            "The clipped drums crackle on every hit, a buzz riding on the snare; the limited ones are clean, though their snap "
            "is a little softened. At this loudness the limiter wins; push both harder and both lose."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def clippers(self):
        items = [
            (r"yet mastering engineers do clip, \ on purpose: \ a few tenths of a millisecond on a drum's spike are inaudible", WHITE),
            (r"a soft clipper rounds the corners \ (Part 50's tanh), \ trading a little distortion for a lot of level", WHITE),
            (r"multiband limiters split the spectrum and limit each band apart, \ so the kick does not pump the voice", WHITE),
            (r"the loud masters of the 2000s stacked all three: \ clippers, \ multiband, \ limiter, \ and then clipped the converter", TUNE),
        ]
        rows_scene(self, r"clippers, \ on purpose", items,
                   "And yet engineers clip on purpose. <bookmark mark='b'/> Clipping a few tenths of a millisecond off a drum's "
                   "spike is inaudible, and buys level. <bookmark mark='c'/> A soft clipper rounds the corners, Part 50's hyperbolic "
                   "tangent, trading a little distortion for a lot of loudness. <bookmark mark='d'/> Multiband limiters split the "
                   "spectrum and limit each band apart, so that the kick does not pump the voice. <bookmark mark='e'/> The loud "
                   "masters of the 2000s stacked all three, and then clipped the converter for the last decibel.", marks="bcde")
