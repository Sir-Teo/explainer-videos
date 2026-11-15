from __future__ import annotations

import numpy as np

from videos.music.music58.common import *  # noqa: F403


class Masking(SoundScene):
    def construct(self):
        chapter(self, 2, r"What the ear cannot hear", r"How much noise can a piece of music hide?")
        self.model()
        self.spreading()
        self.frame()
        self.quiz()
        self.time()

    # ------------------------------------------------------------------
    def model(self):
        items = [
            (r"Part 4: \ a sound raises the threshold for others in its critical band, \ and a little beyond", WHITE),
            (r"so in every band of every frame there is a level of noise the music will hide: \ the masking threshold", WHITE),
            (r"a coder may put its errors anywhere below that level, \ and nowhere above it", WHITE),
            (r"the model needs four ingredients: \ critical bands, \ spreading, \ tonality, \ and the threshold in quiet", TUNE),
        ]
        rows_scene(self, r"a masking model", items,
                   "A perceptual coder rests on Part 4. <bookmark mark='b'/> A sound raises the threshold for other sounds in its "
                   "critical band, and a little beyond. <bookmark mark='c'/> So in every band of every frame there is a level of "
                   "noise the music will hide: the masking threshold. <bookmark mark='d'/> A coder may put its errors anywhere below "
                   "that level, and nowhere above it. <bookmark mark='e'/> The model needs four ingredients: critical bands, how "
                   "masking spreads across them, whether the masker is a tone or noise, and the threshold in quiet.", marks="bcde")

    # ------------------------------------------------------------------
    def spreading(self):
        dz = np.linspace(-4, 8, 200)
        S = 15.81 + 7.5 * (dz + 0.474) - 17.5 * np.sqrt(1 + (dz + 0.474) ** 2)
        ax = frame_axes(width=8.4, height=3.0, xlo=-4, xhi=8, ylo=-80, yhi=5, center=DOWN * 0.4 + LEFT * 0.8)
        cv = curve(dz, S, ax.to, color=TUNE, width=3)
        xt = VGroup(*[label(f"{v:+d}" if v else "0", font_size=14, color=GREY_A).next_to(ax.to(v, -80), DOWN, buff=0.1) for v in (-4, 0, 4, 8)])
        xl = label(r"distance from the masker, \ Bark \ (critical bands)", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        yt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(-4, v), LEFT, buff=0.1) for v in (0, -40, -80)])
        side = text_rows([(r"Schroeder's spreading function \ (1979)", TUNE), (r"steep below the masker: \ about 25 dB a Bark", WHITE),
                          (r"shallow above: \ about 10 dB a Bark; \ low sounds mask high ones", WHITE),
                          (r"then lowered by an offset: \ 14.5 + $z$ dB below a tone, \ 5.5 dB below noise \ (Johnston, \ 1988)", WHITE),
                          (r"and never below the threshold in quiet", GREY_A)], font_size=17, width=4.4).next_to(ax, RIGHT, buff=0.4)
        head = label(r"how far masking reaches", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "How far does masking reach? <bookmark mark='a'/> On the Bark scale, where each unit is one critical band, "
            "Manfred Schroeder fitted this curve in 1979: steep below the masker, about twenty-five decibels a band, shallow "
            "above it, about ten, so low sounds mask high ones much more than the reverse. <bookmark mark='b'/> James "
            "Johnston's model of 1988 then lowers it by an offset: a tone hides noise poorly, so the threshold sits fourteen "
            "and a half plus the band number decibels below a tone, but only five and a half below noise. Our coder judges how "
            "tonal each frame is from its spectral flatness, and blends the two. And no threshold goes below the threshold in "
            "quiet, Part 4's curve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(xl), FadeIn(yt), FadeIn(ghost(cv, 0.3)))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(side[:3]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(side[3:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frame(self):
        d = load("masking")
        f = np.array(d["f"])
        k = (f >= 30) & (f <= 20000)
        p = np.array(d["power_db"])
        ref = np.max(p)
        ax = logf_axes(width=10.0, height=3.4, flo=30, fhi=20000, ylo=-100, yhi=0, center=DOWN * 0.4, ticks=(100, 1000, 10000))
        spec = VMobject(stroke_color=GREY_B, stroke_width=1.2).set_points_as_corners([ax.to(x, max(v - ref, -100)) for x, v in zip(f[k], p[k])])
        al = curve(f[k], np.clip(np.array(d["allowed_db"])[k] - ref, -100, 0), ax.to, color=TUNE, width=3)
        q = curve(f[k], np.clip(np.array(d["quiet_db"])[k] - ref, -100, 0), ax.to, color=BLUE, width=2)
        key = VGroup(label(r"one frame of our mix, \ MDCT power", font_size=16, color=GREY_B), label(r"the allowed noise", font_size=16, color=TUNE),
                     label(r"the threshold in quiet", font_size=16, color=BLUE)).arrange(RIGHT, buff=0.6).to_edge(UP, buff=1.0)
        yt = VGroup(*[label(f"{v} dB", font_size=14, color=GREY_A).next_to(ax.to(30, v), LEFT, buff=0.1) for v in (0, -50, -100)])
        note = label(r"everything between the grey spectrum and the gold line is noise the coder may add unheard; \ a band whose signal lies under the gold line need not be sent at all", font_size=16, color=WHITE).to_edge(DOWN, buff=0.3)
        note.scale_to_fit_width(min(note.width, 13.0))
        head = label(r"one frame's mask", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the model at work on twenty-one milliseconds of our mix. <bookmark mark='a'/> In grey, the frame's "
            "spectrum. <bookmark mark='b'/> In gold, the noise allowed in each critical band: the band energies spread, lowered "
            "by the tonality offset. <bookmark mark='c'/> In blue, the threshold in quiet, which takes over at the top. "
            "Everything between the grey and the gold is room for noise the music will hide; and any band whose music lies "
            "entirely under the gold line need not be sent at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(yt), FadeIn(ghost(VGroup(spec, al, q), 0.25)))
            vo.wait_until("a")
            self.play(Create(spec), FadeIn(key[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(Create(al), FadeIn(key[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(Create(q), FadeIn(key[2]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("masking")
        c = clip("masking.two")
        card = listen_card(r"Our mix, \ twice, \ with the same amount of noise added each time: \ once plain white noise, \ once "
                           r"noise shaped by the masking model. \ In which can you hear the noise?", width=10.0)
        with self.voiceover(
            "Your turn. Our mix twice, with exactly the same amount of noise added each time: once plain white noise, once "
            "noise shaped band by band to the masking threshold. In which can you hear the noise?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"the same noise power, \ twice", kind="physical model", detail=r"Part 56's mix, \ Monochord's model", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        res = label(rf"the first: \ white noise is plain to hear; \ the shaped noise, \ only {d['noise_snr_db']:.0f} dB below the music, \ hides inside it", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            f"The first, the white noise, hisses over everything. The shaped noise has the same power, only "
            f"{say(d['noise_snr_db'])} decibels below the music, and yet it is very hard to hear, because every band of it "
            "hides behind the music in that band. A perceptual coder's errors are noise of the second kind."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def time(self):
        items = [
            (r"masking also reaches across time: \ a loud sound hides quieter ones after it for up to about 100 ms", WHITE),
            (r"and, \ oddly, \ before it: \ for only a few milliseconds \ (pre-masking)", WHITE),
            (r"a coder's frames last tens of milliseconds, \ so noise spread through a frame can land before an attack, \ where nothing hides it", WHITE),
            (r"that is pre-echo, \ the subject of Chapter 5", TUNE),
        ]
        rows_scene(self, r"masking in time", items,
                   "Masking reaches across time as well. <bookmark mark='b'/> A loud sound hides quieter ones after it for up to "
                   "about a hundred milliseconds. <bookmark mark='c'/> And, oddly, before it, but only for a few milliseconds. "
                   "<bookmark mark='d'/> A coder's frames last tens of milliseconds, so noise spread through a frame can land before "
                   "an attack, where nothing hides it. <bookmark mark='e'/> That is pre-echo, the subject of Chapter 5.", marks="bcde")
