from __future__ import annotations

from videos.music.music58.common import *  # noqa: F403


class Stereo(SoundScene):
    def construct(self):
        chapter(self, 6, r"Stereo coding", r"Why code two channels when most of the music is in both?")
        self.ms()
        self.numbers()
        self.heard()
        self.tricks()

    # ------------------------------------------------------------------
    def ms(self):
        d = load("stereo")
        eq = MathTex(r"M = \frac{L + R}{2}, \qquad S = \frac{L - R}{2}", font_size=40, color=TUNE).move_to(UP * 1.5)
        items = [
            (r"left and right share most of a mix: \ the voice, \ bass and drums sit in the centre, \ in both", WHITE),
            (rf"so code the sum and the difference instead: \ here the side carries {-d['side_share_db']:.0f} dB less energy than the mid", WHITE),
            (r"the quiet side needs far fewer bits; \ the mid gets the rest", WHITE),
            (r"Blumlein's mid-side of 1931 \ (Part 56), \ used to save bits", TUNE),
        ]
        rows = text_rows(items, font_size=22).move_to(DOWN * 0.9)
        head = label(r"mid and side", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Stereo doubles the data, but not the information. <bookmark mark='a'/> Left and right share most of a mix: the "
            "voice, bass and drums sit in the centre, in both. <bookmark mark='b'/> So code their sum and difference instead, "
            f"the mid and the side. In our mix the side carries {say(-d['side_share_db'])} decibels less energy than the mid. "
            "<bookmark mark='c'/> The quiet side needs far fewer bits, and the mid gets the rest. <bookmark mark='d'/> It is "
            "Blumlein's mid-side of 1931, from Part 56, put to work saving bits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("stereo")
        rows = VGroup(VGroup(label(r"64 kbit/s in all", font_size=17, color=GREY_A), label(r"bits", font_size=17, color=GREY_A), label(r"left: \ SNR", font_size=17, color=GREY_A),
                             label(r"right: \ SNR", font_size=17, color=GREY_A)))
        rows.add(VGroup(label(r"left and right apart", font_size=19, color=EAR), label(r"32 + 32", font_size=19, color=WHITE), label(f"{d['lr']['snr_l']:.1f} dB", font_size=19, color=WHITE),
                        label(f"{d['lr']['snr_r']:.1f} dB", font_size=19, color=WHITE)))
        rows.add(VGroup(label(r"mid and side", font_size=19, color=TUNE), label(rf"{d['total'] - d['side_kbps']:.0f} + {d['side_kbps']:.0f}", font_size=19, color=WHITE),
                        label(f"{d['ms']['snr_l']:.1f} dB", font_size=19, color=TUNE), label(f"{d['ms']['snr_r']:.1f} dB", font_size=19, color=TUNE)))
        rows.arrange(DOWN, buff=0.45)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-4.4 + 3.0 * i)
        rows.move_to(UP * 0.3)
        note = label(r"the same bits, \ about 4 dB better in each channel", font_size=19, color=TUNE).to_edge(DOWN, buff=0.7)
        head = label(r"the same bits, \ spent two ways", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is our stereo mix at sixty-four kilobits in all. <bookmark mark='a'/> Coded as two channels of thirty-two, "
            f"each comes back with a signal-to-noise ratio near {say(d['lr']['snr_l'])} decibels. <bookmark mark='b'/> Coded as "
            f"a mid of {say(d['total'] - d['side_kbps'])} kilobits and a side of {say(d['side_kbps'])}, each channel comes back "
            "about four decibels better, from the same number of bits."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("stereo")
        c = clip("stereo.two")
        boxes = choice_boxes([r"left and right", r"mid and side"], width=3.2, height=0.9, buff=1.2, size=20).move_to(UP * 0.4)
        note = label(r"headphones; \ 64 kbit/s in all", font_size=18, color=GREY_A).next_to(boxes, DOWN, buff=0.5)
        head = label(r"two ways, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear both, with headphones: left and right coded apart, then mid and side."):
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(note))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"L/R, \ then M/S", kind="physical model", detail=r"Part 56's mix, \ Monochord's coder", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["lr"], st["ms"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["ms"], c.duration, buff=0.08)
        with self.voiceover(
            "The first is rough, and the noise in its two channels is unrelated, so it spreads around the head away from the "
            "music. The second is cleaner, its noise sitting in the centre with the voice that masks it."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tricks(self):
        items = [
            (r"switch per band and per frame: \ mid-side where the channels agree, \ left-right where they do not", WHITE),
            (r"intensity stereo: \ above a few kilohertz, \ send one channel and a level ratio per band; \ the ear locates highs by level", WHITE),
            (r"parametric stereo \ (HE-AAC v2, \ 2006): \ one channel plus a few kilobits of cues: \ level and time differences, \ coherence", WHITE),
            (r"Part 55's two cues, \ sent as numbers instead of as sound", TUNE),
        ]
        rows_scene(self, r"more stereo tricks", items,
                   "Coders go further. <bookmark mark='b'/> They switch per band and per frame: mid-side where the channels agree, "
                   "left-right where they do not. <bookmark mark='c'/> Intensity stereo sends a single channel above a few "
                   "kilohertz, with a level ratio per band, since the ear locates high sounds by level. <bookmark mark='d'/> And "
                   "parametric stereo, in HE-AAC version two of 2006, sends one channel plus a few kilobits of cues: level and time "
                   "differences and how alike the channels are. <bookmark mark='e'/> They are Part 55's two cues, sent as numbers "
                   "instead of as sound.", marks="bcde")
