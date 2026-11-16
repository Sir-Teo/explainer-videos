from __future__ import annotations

import numpy as np

from videos.music.music56.common import *  # noqa: F403

PCOL = {"near": TUNE, "middle": BLUE, "far": EAR}


class Depth(SoundScene):
    def construct(self):
        chapter(self, 9, r"Depth and width", r"How do two loudspeakers make a stage with a front and a back?")
        self.cues()
        self.places()
        self.heard()
        self.width_tools()
        self.haas_heard()

    # ------------------------------------------------------------------
    def cues(self):
        items = [
            (r"panning gives left and right; \ depth comes from Part 55's distance cues", WHITE),
            (r"level: \ further is quieter, \ 6 dB for each doubling of distance", WHITE),
            (r"treble: \ air and obstacles take the highs first", WHITE),
            (r"the ratio of direct sound to reverberation: \ the strongest cue of all", WHITE),
            (r"pre-delay: \ the gap before the reverberation; \ a long one keeps a source close in a big room", TUNE),
        ]
        rows_scene(self, r"cues for depth", items,
                   "Panning gives left and right. Depth comes from the distance cues of Part 55. <bookmark mark='b'/> Level: further "
                   "is quieter, about six decibels per doubling for a free-field point source, before room contributions. <bookmark mark='c'/> Treble: air and obstacles take the "
                   "highs first. <bookmark mark='d'/> The ratio of direct sound to reverberation, the strongest cue of all. "
                   "<bookmark mark='e'/> And pre-delay, the gap before the reverberation starts: a long one keeps a source close "
                   "even in a big room, a short one pushes it back.", marks="bcdef")

    # ------------------------------------------------------------------
    def places(self):
        d = load("depth")
        rows = VGroup(VGroup(label(r"place", font_size=17, color=GREY_A), label(r"fader", font_size=17, color=GREY_A), label(r"treble shelf", font_size=17, color=GREY_A),
                             label(r"reverb send", font_size=17, color=GREY_A), label(r"pre-delay", font_size=17, color=GREY_A), label(r"direct : reverb", font_size=17, color=GREY_A)))
        for k in ("near", "middle", "far"):
            v = d["places"][k]
            rows.add(VGroup(label(k, font_size=19, color=PCOL[k]), label(rf"{v['gain']:+.0f} dB", font_size=19, color=WHITE), label(rf"{v['shelf']:+.0f} dB", font_size=19, color=WHITE),
                            label(rf"{v['send']:+.0f} dB", font_size=19, color=WHITE), label(rf"{v['predelay_ms']:.0f} ms", font_size=19, color=WHITE),
                            label(rf"{d['dr_db'][k]:+.0f} dB", font_size=19, color=PCOL[k])))
        rows.arrange(DOWN, buff=0.35)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-5.4 + 2.15 * i)
        rows.move_to(UP * 0.5)
        stage = VGroup(Line([-3.5, -2.2, 0], [3.5, -2.2, 0], color=GREY_D, stroke_width=2))
        dots = VGroup(*[Dot([0, y, 0], radius=r, color=PCOL[k]) for k, y, r in (("near", -2.7, 0.18), ("middle", -2.05, 0.13), ("far", -1.55, 0.09))])
        sl = label(r"the band's line", font_size=14, color=GREY_A).next_to(stage, RIGHT, buff=0.1)
        head = label(r"one voice, \ three distances", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is our voice placed at three depths against the same band. <bookmark mark='a'/> Near: full level, full treble, "
            f"barely any reverberation, the direct sound {say(d['dr_db']['near'])} decibels above its echo. <bookmark mark='b'/> In the "
            "middle: five decibels down, the treble shelved four decibels, a send to the reverb and twelve milliseconds of "
            f"pre-delay; direct over reverberant, {say(d['dr_db']['middle'])} decibels. <bookmark mark='c'/> Far: ten decibels "
            f"down, nine decibels of treble gone, the reverb at full send: {say(d['dr_db']['far'])} decibels. Each step pushes "
            "the voice behind the band's line."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(stage), FadeIn(sl), FadeIn(ghost(VGroup(rows[1:], dots), 0.25)))
            for mark, i in zip("abc", range(3)):
                vo.wait_until(mark)
                self.play(FadeIn(rows[1 + i]), FadeIn(dots[i]), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("depth")
        c = clip("depth.three")
        boxes = choice_boxes([r"near", r"middle", r"far"], width=2.6, height=0.9, buff=0.9, size=22).move_to(UP * 0.4)
        head = label(r"three depths, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        note = label(r"headphones; \ the band stays where it is", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        with self.voiceover("Hear the three, with headphones; the band stays where it is."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"near, \ middle, \ far", kind="physical model", detail=r"our session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["near"], st["middle"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["middle"], st["far"] - 0.3, buff=0.08)
            pulse(snd, boxes[2], st["far"], c.duration, buff=0.08)
        with self.voiceover("The voice steps back each time: from in your face, to on the stage, to somewhere behind the band in a larger room."):
            self.play(Indicate(boxes[2], color=EAR, scale_factor=1.04))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def width_tools(self):
        d = load("depth")["width"]
        eq = MathTex(r"M = \frac{L + R}{2}, \quad S = \frac{L - R}{2}; \qquad L = M + S, \quad R = M - S", font_size=34, color=TUNE).move_to(UP * 1.6)
        items = [
            (r"mid-side: \ turn $S$ up to widen a stereo track, \ down to narrow it; \ at $S = 0$ it is mono", WHITE),
            (r"the Haas trick: \ the same mono track in both channels, \ one 12 ms late: \ wide, \ from one source", WHITE),
            (rf"its cost: \ the channels are unrelated \ (correlation {d['correlation']:.2f}), \ and in mono they comb: \ notches from {d['notch_hz']:.0f} Hz, \ every {d['spacing_hz']:.0f} Hz", WHITE),
            (r"a correlation meter on the master warns: \ near $+1$ is narrow and safe; \ near 0 is wide; \ below 0 cancels in mono", TUNE),
        ]
        rows = text_rows(items, font_size=20).move_to(DOWN * 0.8)
        head = label(r"width", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Width has tools of its own. <bookmark mark='a'/> Mid-side, Blumlein's again: the mid is the sum, the side the difference; turn the side up to widen a stereo track, down to narrow it, to nothing for mono. <bookmark mark='b'/> And the Haas trick: put the same mono track in both channels with one twelve milliseconds late. Depending on delay, signal and playback, precedence can bias localization toward the earlier channel while the sound may seem wider. <bookmark mark='c'/> Its cost: the two channels are nearly unrelated, a correlation of {say(d['correlation'], 2)}, and summed to mono they comb, with notches from {say(d['notch_hz'])} hertz and every {say(d['spacing_hz'])} hertz above. <bookmark mark='d'/> So a correlation meter sits on the master: positive correlation generally supports mono compatibility, while negative correlation warns of cancellation; one broadband number does not determine width or reveal all frequency-specific problems."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def haas_heard(self):
        d = load("depth")
        c = clip("depth.width")
        f = np.linspace(20, 1000, 400)
        tau = 0.012
        ax = frame_axes(width=8.0, height=1.8, xlo=20, xhi=1000, ylo=-30, yhi=8, center=DOWN * 1.6)
        comb = curve(f, np.clip(20 * np.log10(np.abs(1 + np.exp(-2j * np.pi * f * tau)) / 2 + 1e-9) + 0.0, -30, 8), ax.to, color=EAR, width=2)
        xt = VGroup(*[label(f"{v} Hz", font_size=13, color=GREY_A).next_to(ax.to(v, -30), DOWN, buff=0.08) for v in (20, 500, 1000)])
        cl = label(r"the mono sum's response: \ a comb", font_size=15, color=EAR).next_to(ax, UP, buff=0.1)
        boxes = choice_boxes([r"stereo, \ wide", r"summed to mono"], width=3.2, height=0.9, buff=1.2, size=20).move_to(UP * 1.0)
        head = label(r"a guitar made wide, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear our guitar widened by twelve milliseconds, then the same thing summed to mono."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(ax), FadeIn(xt), FadeIn(ghost(comb, 0.3)))
        st = d["starts_width"]
        with self.listen(c) as snd:
            window(snd, r"wide, \ then mono", kind="physical model", detail=r"Part 38's guitar", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["wide"], st["mono"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["mono"], c.duration, buff=0.08)
            pulse(snd, ax, st["mono"], c.duration, rate=5.0, color=GREY_B, buff=0.1)
        with self.voiceover("Wide and lush in stereo; in mono, hollow and phasey, as if played down a tube. Width bought with delay is paid for in mono."):
            self.play(Create(comb), FadeIn(cl), run_time=1.2)
        self.wait(0.4)
        self.clear_scene()
