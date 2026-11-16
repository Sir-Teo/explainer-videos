from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403


class Mix(SoundScene):
    def construct(self):
        chapter(self, 6, r"Music under dialogue", r"How does a score stay out of the actors' way?")
        self.problem()
        self.hear()
        self.drawn()
        self.loudness()
        self.craft()

    # ------------------------------------------------------------------
    def problem(self):
        items = [
            (r"dialogue comes first: \ if a line is not understood, \ the scene fails", WHITE),
            (r"speech intelligibility lives mostly between 1 and 4 kHz: \ consonants and the upper formants \ (Part 8)", WHITE),
            (r"music in that band, \ at that moment, \ masks the words \ (Part 4's masking)", WHITE),
            (r"the mixer lowers the music under every line: \ `ducking', \ the sidechain of Part 40", TUNE),
            (r"our dialogue is Part 17's model voice babbling vowels: \ it has a voice's spectrum, \ not words", GREY_A),
        ]
        rows_scene(self, r"the voice comes first", items,
                   "On screen, the voice comes first: if a line is not understood, the scene fails. <bookmark mark='b'/> Speech "
                   "intelligibility lives mostly between one and four kilohertz, in the consonants and upper formants of Part 8. "
                   "<bookmark mark='c'/> Music in that band, at that moment, masks the words, as Part 4 showed. "
                   "<bookmark mark='d'/> So the mixer lowers the music under every line: ducking, the sidechain of Part 40. "
                   "<bookmark mark='e'/> Our dialogue is Part 17's model voice babbling vowels, which has a voice's spectrum but "
                   "no words.", marks="bcde")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("mix")
        c = clip("mix.two")
        boxes = VGroup(*[VGroup(RoundedRectangle(width=4.0, height=1.3, corner_radius=0.15, stroke_color=GREY_B),
                                label(t, font_size=22, color=WHITE)).arrange(ORIGIN) for t in (r"music at full level", r"music ducked 10 dB under the voice")]).arrange(RIGHT, buff=1.0).move_to(UP * 0.8)
        nums = VGroup(label(rf"voice against music, \ 1 to 4 kHz: \ {d['ratio_before_db']:+.1f} dB", font_size=19, color=GREY_A).next_to(boxes[0], DOWN, buff=0.3),
                      label(rf"voice against music, \ 1 to 4 kHz: \ {d['ratio_after_db']:+.1f} dB", font_size=19, color=TUNE).next_to(boxes[1], DOWN, buff=0.3))
        with self.voiceover(
            "Hear a passage of strings and horn with the voice over it, first at full level, then with the music ducked by "
            "up to ten decibels whenever the voice speaks."
        ):
            self.play(FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"before, \ then after", kind="synthesized", detail=r"a model voice, \ the additive orchestra", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["before"], st["after"] - 0.4, buff=0.1)
            pulse(snd, boxes[1], st["after"], c.duration, buff=0.1)
        with self.voiceover(
            "Measure the voice against the music in the speech band. Before ducking the voice is "
            f"{say(-d['ratio_before_db'], 1)} decibels below the music there; after, {say(-d['ratio_after_db'], 1)}. The "
            "ten-decibel duck bought about six decibels over the whole passage, because the music comes back up in every "
            "pause."
        ):
            self.play(FadeIn(nums))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def drawn(self):
        d = load("mix")
        env = np.array(d["dialogue_env"])
        g = np.array(d["gain_db"])
        n = len(env)
        x0, W = -5.6, 11.2
        e_line = VMobject(color=BLUE, stroke_width=3).set_points_as_corners([[x0 + W * i / (n - 1), 0.4 + 1.4 * v, 0] for i, v in enumerate(env)])
        g_line = VMobject(color=TUNE, stroke_width=3).set_points_as_corners([[x0 + W * i / (n - 1), -1.2 + 0.12 * v, 0] for i, v in enumerate(g)])
        axes = VGroup(Line([x0, 0.4, 0], [x0 + W, 0.4, 0], color=GREY_D), Line([x0, -1.2, 0], [x0 + W, -1.2, 0], color=GREY_D),
                      DashedLine([x0, -1.2 - 1.2, 0], [x0 + W, -1.2 - 1.2, 0], color=GREY_D))
        labs = VGroup(label(r"the voice's envelope", font_size=17, color=BLUE).move_to([x0 + 1.4, 2.1, 0]),
                      label(r"the music's gain: \ 0 dB, \ down to $-$10 dB", font_size=17, color=TUNE).move_to([x0 + 2.2, -0.75, 0]),
                      label(r"$-$10 dB", font_size=14, color=GREY_A).move_to([x0 - 0.45, -2.4, 0]))
        head = label(r"the duck, \ drawn", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"7 seconds; \ the gain follows the voice with a fast attack and a quarter-second release", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is the duck. <bookmark mark='a'/> In blue, the voice's envelope, phrase by phrase. <bookmark mark='b'/> In "
            "gold, the music's gain: down by ten decibels as each phrase starts, and back up a quarter of a second after it "
            "ends. A good mix makes this inaudible: the music seems to make room by itself."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axes), FadeIn(cap))
            vo.wait_until("a")
            self.play(Create(e_line), FadeIn(labs[0]))
            vo.wait_until("b")
            self.play(Create(g_line), FadeIn(labs[1:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def craft(self):
        items = [
            (r"composers write around dialogue: \ thin textures, \ low or high registers, \ careful register and texture around the voice, without a universal ban on melody in its range", WHITE),
            (r"a solo clarinet under a tenor's line competes; \ sustained low strings may compete less, depending on levels and spectra", WHITE),
            (r"the final mix balances three stems: \ dialogue, \ music, \ effects", WHITE),
            (r"cinema mixes aim dialogue at a steady loudness; \ Part 57 measures it", TUNE),
            (r"chapter 7: \ games, \ where nobody knows what happens next", GREY_A),
        ]
        rows_scene(self, r"writing for the mix", items,
                   "Good scores make the mixer's job easy. <bookmark mark='b'/> Composers write around dialogue: thin textures, "
                   "low or high registers, careful register and texture around the voice, without a universal ban on melody in its range. <bookmark mark='c'/> A solo clarinet under a tenor's "
                   "line competes; sustained low strings may compete less, depending on levels and spectra. <bookmark mark='d'/> The final mix balances three stems, "
                   "dialogue, music and effects, <bookmark mark='e'/> and cinema mixes aim the dialogue at a steady loudness, "
                   "which Part 57 measures. <bookmark mark='f'/> Chapter seven turns to games, where nobody knows what happens "
                   "next.", marks="bcdef")

    # ------------------------------------------------------------------
    def loudness(self):
        items = [
            (r"broadcasters normalise programmes to a target loudness \ (EBU R 128: \ $-$23 LUFS)", WHITE),
            (r"R 128 measures integrated programme loudness; \\ dialogue-gated targets belong to other specifications", WHITE),
            (r"music and effects then get the room the dialogue leaves", WHITE),
            (r"cinema mixes keep a wide range: \ quiet dialogue, \ very loud action; \ home versions compress it", TUNE),
            (r"Part 57 builds the loudness meter itself", GREY_A),
        ]
        rows_scene(self, r"loudness standards", items,
                   "There are also rules for the whole programme. <bookmark mark='b'/> European broadcasters normalise to a target loudness, minus twenty-three LUFS under EBU R 128. <bookmark mark='c'/> EBU R 128 normally uses integrated programme loudness; dialogue-gated measurements belong to particular other delivery specifications, <bookmark mark='d'/> and music and effects get the room the dialogue leaves. <bookmark mark='e'/> Cinema mixes keep a wide range, quiet dialogue and very loud action, and home versions compress it. <bookmark mark='f'/> Part 57 builds the loudness meter itself.", marks="bcdef")
