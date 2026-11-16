from __future__ import annotations

import numpy as np

from explainer.music.viz import heat_image
from videos.music.music59.common import *  # noqa: F403


class Speech(SoundScene):
    def construct(self):
        chapter(self, 9, r"Speech in big rooms", r"Why can't you understand the announcement at the station?")
        self.mtf()
        self.grid()
        self.quiz()
        self.remedies()

    # ------------------------------------------------------------------
    def mtf(self):
        lines = VGroup(
            label(r"speech is a carrier whose loudness swings 0.6 to 12.5 times a second: \ syllables", font_size=20, color=WHITE),
            MathTex(r"m(F) = \underbrace{\frac{1}{\sqrt{1 + \left(2\pi F\,T/13.8\right)^2}}}_{\text{reverberation fills the dips}}"
                    r"\;\cdot\; \underbrace{\frac{1}{1 + 10^{-\mathrm{SNR}/10}}}_{\text{noise lifts the floor}}", font_size=34, color=TUNE),
            MathTex(r"\mathrm{SNR}_{\text{app}} = 10\log_{10}\frac{m}{1-m}, \quad \text{clipped to } \pm 15\ \text{dB}, \quad \mathrm{STI} = \frac{\overline{\mathrm{SNR}_{\text{app}}} + 15}{30}", font_size=30),
            label(r"14 modulation frequencies \ $\times$ \ 7 octave bands, \ weighted \ (IEC 60268-16): \ 0 is nothing, \ 1 is perfect", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.5).move_to(DOWN * 0.1)
        head = label(r"the speech transmission index", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Music forgives a reverberant room; speech does not. Houtgast and Steeneken, in the 1970s, found a way to measure why. <bookmark mark='a'/> Speech is a carrier whose loudness swings with the syllables, between about half a time and twelve times a second. Understanding depends on hearing those swings. <bookmark mark='b'/> Reverberation fills in the quiet between syllables, more for faster swings and longer reverberation times; noise lifts the floor under all of them. Their product is how much of each swing survives. <bookmark mark='c'/> Each surviving depth is turned into an apparent signal-to-noise ratio, clipped to fifteen decibels either way, and averaged onto a scale from nought to one. <bookmark mark='d'/> The full IEC speech transmission index uses fourteen modulation rates and seven octave bands with additional corrections. Our illustration uses one decay and SNR in all bands and omits those details, so it is not a compliance measurement."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grid(self):
        d = load("sti")
        g = np.array(d["grid"])  # rows T, columns SNR
        T, snr = d["T"], d["snr"]
        nr, nc = g.shape
        w, h = 6.6, 4.2
        pic = Group(heat_image(g, 0.0, 0.75, w, h, smooth=False), Rectangle(width=w, height=h, stroke_color=GREY_D, stroke_width=1.2)).move_to(LEFT * 0.4 + DOWN * 0.25)
        cw, ch = w / nc, h / nr
        x0, y0 = pic.get_left()[0], pic.get_top()[1]
        nums = VGroup(*[label(f"{g[i, j]:.2f}", font_size=13, color=WHITE if g[i, j] < 0.5 else BLACK).move_to([x0 + cw * (j + 0.5), y0 - ch * (i + 0.5), 0]) for i in range(nr) for j in range(nc)])
        cl = VGroup(*[label(f"{v:g}", font_size=14, color=GREY_A).move_to([x0 + cw * (j + 0.5), y0 + 0.2, 0]) for j, v in enumerate(snr)])
        rl = VGroup(*[label(f"{v:g} s", font_size=14, color=GREY_A).move_to([x0 - 0.35, y0 - ch * (i + 0.5), 0]) for i, v in enumerate(T)])
        cx = label(r"signal to noise, \ dB", font_size=15, color=GREY_A).next_to(cl, UP, buff=0.1)
        rx = label(r"reverberation time", font_size=15, color=GREY_A).rotate(PI / 2).next_to(rl, LEFT, buff=0.15)
        scale = VGroup(
            label(r"$\geq 0.60$ \ good", font_size=16, color=TUNE),
            label(r"0.45 to 0.60 \ fair", font_size=16, color=WHITE),
            label(r"0.30 to 0.45 \ poor", font_size=16, color=EAR),
            label(r"$< 0.30$ \ bad", font_size=16, color=EAR),
            label(r"illustrative model; \\ not a compliance test", font_size=15, color=GREY_A),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(pic, RIGHT, buff=0.5)
        head = label(r"simplified STI illustration", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Here is the index computed by Monochord for every pair of reverberation time and signal-to-noise ratio. "
            "<bookmark mark='a'/> A dry room with the voice well above the noise, top right, scores over seven tenths. "
            "<bookmark mark='b'/> Down the columns, reverberation takes its share: at six seconds, a stone station hall, "
            "even a voice with no noise at all scores under a quarter. <bookmark mark='c'/> Along the rows, noise takes its "
            "share. Neither can be fixed by turning the voice up: louder speech raises the reverberation with it, and only beats "
            "the noise. <bookmark mark='d'/> Required intelligibility thresholds depend on the applicable standard, jurisdiction, coverage statistic and project; this illustration is not a compliance test."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pic), FadeIn(cl), FadeIn(rl), FadeIn(cx), FadeIn(rx))
            vo.wait_until("a")
            self.play(FadeIn(nums), run_time=1.2)
            self.play(Indicate(nums[nc - 1], color=TUNE, scale_factor=1.5))
            vo.wait_until("b")
            self.play(Indicate(nums[(nr - 1) * nc + nc - 1], color=EAR, scale_factor=1.5))
            vo.wait_until("c")
            self.play(FadeIn(scale[:4]))
            vo.wait_until("d")
            self.play(FadeIn(scale[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("sti")
        c = clip("sti.three")
        cd = d["conds"]
        card = listen_card(r"The same announcement in three rooms: \ a dry studio, \ a reverberant hall, \ a noisy, \ "
                           r"echoing station. \ Count how many words you catch in each.", width=10.0)
        with self.voiceover("Your turn. The same announcement in three rooms. Count how many words you catch in each."):
            self.play(FadeIn(card))
        self.wait(0.8)
        names = [("good", r"first"), ("fair", r"second"), ("bad", r"third")]
        boxes = choice_boxes([n[1] for n in names], width=2.6, height=0.9, buff=0.9, size=22).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three rooms", kind="physical model", detail=r"Part 8's voice, \ reverberation and noise", corner=DL, tag_corner=DR)
            for i, (k, _) in enumerate(names):
                end = st[names[i + 1][0]] - 0.4 if i + 1 < len(names) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.08)
        res = VGroup(*[label(rf"T = {cd[k]['T']:g} s, \ SNR {cd[k]['snr']:g} dB: \ STI {cd[k]['sti']:.2f}", font_size=16,
                             color=(TUNE, WHITE, EAR)[i]).next_to(boxes[i], DOWN, buff=0.35) for i, (k, _) in enumerate(names)])
        with self.voiceover(
            f"The first was the studio, index {say(cd['good']['sti'], 2)}: every word. The second the hall, "
            f"{say(cd['fair']['sti'], 2)}: the words smear into each other. The third the station, {say(cd['bad']['sti'], 2)}: a "
            "voice, but hardly a word of it."
        ):
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.4), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def remedies(self):
        items = [
            (r"put the loudspeaker near the listener: \ more direct sound, \ less of the room", WHITE),
            (r"aim it at the audience and away from the walls: \ steerable columns", WHITE),
            (r"many small loudspeakers, \ each quiet, \ each close, \ delayed to the talker", WHITE),
            (r"absorb the room where you can; \ speak slower where you cannot", WHITE),
            (r"automatic gain from a noise microphone: \ louder announcements when the train arrives", TUNE),
        ]
        rows_scene(self, r"what helps", items,
                   "What helps? <bookmark mark='b'/> Put the loudspeaker near the listener: more direct sound and less of the room. "
                   "<bookmark mark='c'/> Aim it at the audience and away from the hard walls, which "
                   "is what steerable columns are for. <bookmark mark='d'/> Use many small loudspeakers, each quiet and close, "
                   "delayed to the talker. <bookmark mark='e'/> Absorb the room where you can, and speak slower where you cannot. "
                   "<bookmark mark='f'/> And measure the noise with a microphone, so announcements grow louder only when the train "
                   "arrives.", marks="bcdef")
