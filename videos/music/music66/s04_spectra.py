from __future__ import annotations

import numpy as np

from videos.music.music66.common import *  # noqa: F403


class Spectra(SoundScene):
    def construct(self):
        chapter(self, 3, r"Spectrograms and vocoders", r"Can sound be made from a picture of sound?")
        self.picture_()
        self.heard()
        self.bands()
        self.vocoders()

    # ------------------------------------------------------------------
    def picture_(self):
        d = load("vocoder")
        M = np.array(d["mel"])
        pic = heat_image(M[::-1], M.max() - 4, M.max(), width=10.0, height=3.2).move_to(DOWN * 0.3)
        lab = label(rf"a bowed phrase as a mel spectrogram: \ 64 bands, \ {d['values_per_second_mel']:,.0f} numbers a second instead of 16,000 samples", font_size=17, color=GREY_A).next_to(pic, DOWN, buff=0.25)
        ly = VGroup(label(r"7.6 kHz", font_size=13, color=GREY_A).next_to(pic, LEFT, buff=0.12).align_to(pic, UP),
                    label(r"40 Hz", font_size=13, color=GREY_A).next_to(pic, LEFT, buff=0.12).align_to(pic, DOWN))
        head = label(r"a picture of sound", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The first split is the spectrogram. Here is a bowed phrase as a mel spectrogram: the energy in sixty-four bands "
            "spaced as the ear spaces pitch, sixty-two times a second. <bookmark mark='a'/> The phrase's notes, their "
            "harmonics and their attacks are all visible, and there are four thousand numbers a second instead of sixteen "
            "thousand samples. What is gone is the phase, the exact timing of every wave, and the fine detail between bands."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pic), FadeIn(ly))
            vo.wait_until("a")
            self.play(FadeIn(lab))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("vocoder")
        c = clip("vocoder.two")
        boxes = choice_boxes([r"the phrase", r"rebuilt from its mel spectrogram"], width=4.4, height=0.9, buff=0.8, size=18).move_to(UP * 0.6)
        res = label(rf"{d['dist_mel']:.1f} dB from the original, \ spectrum against spectrum \ (the true spectrum with Griffin-Lim's phase alone: \ {d['dist_gl']:.1f} dB)", font_size=17, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"back from the picture", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Can the picture be turned back into sound? Spread each band back over its frequencies, and invent a phase by Griffin and Lim's method from Part 64. Hear the phrase, then the phrase rebuilt from its mel spectrogram."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"original, \ then rebuilt", kind="synthesized", detail=r"Part 9's string; \ mel and Griffin-Lim", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["original"], st["mel"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["mel"], c.duration, buff=0.08)
        with self.voiceover(
            f"The tune survives; the sound is smeared and a little metallic, {say(d['dist_mel'], 1)} decibels from the original "
            f"by spectrum. Most of that is lost detail between the bands: with the full spectrum and only the phase invented, the "
            f"distance is {say(d['dist_gl'], 1)}."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vocoders(self):
        items = [
            (r"a vocoder: \ a network that turns a mel spectrogram into sound, \ trained on pairs of spectrogram and sound", WHITE),
            (r"WaveNet as a vocoder \ (2017), \ then fast ones: \ WaveGlow, \ MelGAN, \ HiFi-GAN \ (2020)", WHITE),
            (r"so a generator can work on pictures: \ draw a spectrogram, \ then let a vocoder make it sound", WHITE),
            (r"text-to-speech has worked this way since about 2018; \ much music generation too", TUNE),
        ]
        rows_scene(self, r"vocoders", items,
                   "The fix is to learn the way back. <bookmark mark='b'/> A vocoder is a network that turns a mel spectrogram "
                   "into sound, trained on many pairs of spectrogram and sound. <bookmark mark='c'/> WaveNet itself served as one "
                   "from 2017, and then faster ones: WaveGlow, MelGAN, and HiFi-GAN in 2020, quicker than real time. "
                   "<bookmark mark='d'/> So a generator can work on pictures: draw a spectrogram, then let a vocoder make it sound. "
                   "<bookmark mark='e'/> Text-to-speech has worked this way since about 2018, and much music generation too.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def bands(self):
        d = load("melbands")
        c = clip("melbands.three")
        boxes = choice_boxes([r"16 bands", r"64 bands", r"256 bands"], width=3.2, height=0.9, buff=0.5, size=19).move_to(UP * 0.6)
        dist = d["dist"]
        res = label(rf"spectral distance: \ {dist['16']:.1f}, \ {dist['64']:.1f} and {dist['256']:.1f} dB", font_size=19, color=TUNE).next_to(boxes, DOWN, buff=0.6)
        head = label(r"how many bands?", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("How much does the picture need? Hear the phrase rebuilt from sixteen bands, sixty-four, and two hundred and fifty-six."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        ks = ["b16", "b64", "b256"]
        with self.listen(c) as snd:
            window(snd, r"16, \ 64, \ 256 bands", kind="synthesized", detail=r"Part 9's string; \ Griffin-Lim", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            f"With sixteen bands the harmonics blur into a hum, {say(dist['16'], 1)} decibels away; with two hundred and "
            f"fifty-six the string returns, {say(dist['256'], 1)}. More bands, more numbers to generate: every representation "
            "in this part is a trade between what is easy to model and what is needed to hear."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()
