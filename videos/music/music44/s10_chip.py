from __future__ import annotations

import numpy as np

from videos.music.music44.common import *  # noqa: F403


class Chip(SoundScene):
    def construct(self):
        chapter(self, 9, r"Music under hardware limits", r"What can you play with three voices and a noise?")
        self.chips()
        self.duty()
        self.noise()
        self.quiz()
        self.tune()
        self.fm()
        self.style()

    # ------------------------------------------------------------------
    def chips(self):
        items = [
            (r"General Instrument's AY-3-8910 \ (1978) \ and Texas Instruments' SN76489: \ three square-wave tones and a noise", WHITE),
            (r"Nintendo's console chip \ (1983): \ two pulse waves, \ a triangle, \ a noise, \ and short samples", WHITE),
            (r"the Commodore 64's SID \ (1982): \ three oscillators with a real filter", WHITE),
            (r"a few voices, \ crude waveforms, \ volumes in 16 steps, \ registers changed 50 or 60 times a second", TUNE),
            (r"our chip, \ in their manner: \ two pulses, \ a 4-bit triangle, \ an LFSR noise, \ updated 60 times a second", GREY_A),
        ]
        rows_scene(self, r"sound chips", items,
                   "The first game music came from chips. <bookmark mark='b'/> General Instrument's AY-3-8910 of 1978 and Texas "
                   "Instruments' SN76489 each gave three square-wave tones and a noise channel. <bookmark mark='c'/> Nintendo's "
                   "console chip of 1983 had two pulse waves, a triangle, a noise channel and short samples, "
                   "<bookmark mark='d'/> and the Commodore 64's SID of 1982 had three oscillators with a real filter. "
                   "<bookmark mark='e'/> A few voices, crude waveforms, volumes in sixteen steps, registers changed fifty or sixty "
                   "times a second. <bookmark mark='f'/> Our chip works in their manner: two pulse channels, a four-bit triangle, "
                   "a noise channel from a shift register, updated sixty times a second.", marks="bcdef")

    # ------------------------------------------------------------------
    def duty(self):
        d = load("duty")
        c = clip("duty.three")
        cells = VGroup()
        for k, du in zip(("50", "25", "12.5"), d["duties"]):
            wave = VMobject(color=TUNE, stroke_width=3)
            pts = []
            for cyc in range(2):
                x = 1.4 * cyc
                pts += [[x, 0.5, 0], [x + 1.4 * du, 0.5, 0], [x + 1.4 * du, -0.5, 0], [x + 1.4, -0.5, 0], [x + 1.4, 0.5, 0]]
            wave.set_points_as_corners(pts)
            h = np.array(d["harmonics"][str(du)])
            bars = VGroup(Line([0, 0, 0], [2.8, 0, 0], color=GREY_D))
            for i, a in enumerate(h):
                bars.add(Rectangle(width=0.14, height=max(1.2 * a, 0.01), stroke_width=0, fill_color=EAR if a < 0.01 else BLUE, fill_opacity=0.9).move_to([2.8 * (i + 0.5) / len(h), 0.6 * a, 0]))
            gone = [i + 1 for i, a in enumerate(h) if a < 1e-6]
            cells.add(VGroup(label(rf"duty {k}\%", font_size=21, color=WHITE), wave, bars,
                             label(r"missing: \ harmonics " + r", \ ".join(str(x) for x in gone), font_size=14, color=GREY_A)).arrange(DOWN, buff=0.25))
        cells.arrange(RIGHT, buff=0.9).move_to(UP * 0.1)
        head = label(r"one pulse channel, \ three duty cycles", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The pulse channel's one timbre control is its duty cycle, the share of each cycle spent high. Hear A four at "
            "fifty, twenty-five and twelve and a half per cent. The harmonics follow a simple law: the k-th harmonic's "
            "strength is the sine of pi k times the duty, over k. At fifty per cent every even harmonic is missing, the "
            "hollow square wave; at twenty-five every fourth; at twelve and a half every eighth. Narrower pulses sound "
            "thinner and nasal."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three duty cycles", kind="synthesized", detail=r"our chip", corner=DL, tag_corner=DR)
            for i, k in enumerate(("50", "25", "12.5")):
                pulse(snd, cells[i], st[k], st[k] + 1.2, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("arp")
        c = clip("arp.quiz")
        card = listen_card(r"Two C major chords on the chip. \ One uses three channels at once; \ "
                           r"the other uses only one. \ Which uses one?", width=10.4)
        with self.voiceover(
            "A question for your ears. Two C major chords on our chip. One uses three channels sounding at once; the other "
            "uses a single channel. Which one uses only one?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.0, height=1.3, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(DOWN, buff=-0.85)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.5).move_to(UP * 1.0)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two chords", kind="synthesized", detail=r"our chip", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.3, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        # the arpeggio drawn: one channel stepping through C, E, G every frame
        steps = VGroup()
        for i in range(18):
            m = (60, 64, 67)[i % 3]
            steps.add(Rectangle(width=0.32, height=0.14, stroke_width=0, fill_color=TUNE, fill_opacity=0.9).move_to([-3.0 + 0.34 * i, -1.3 + 0.12 * (m - 60), 0]))
        cap = VGroup(label(r"the second: \ one channel stepping C, \ E, \ G every sixtieth of a second", font_size=20, color=TUNE),
                     label(r"too fast to hear as notes, \ too slow to fuse cleanly: \ the buzzing chiptune chord", font_size=17, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            f"The second. One channel steps through C, E and G, changing note {say(d['rate'])} times a second, once every "
            "frame of the console's display. That is too fast to hear as separate notes and too slow to fuse into a clean "
            "chord, and the buzz it makes became one of the signature sounds of chip music: a chord from a single voice, "
            "leaving the other channels free."
        ):
            self.play(FadeIn(steps), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tune(self):
        d = load("chip")
        c = clip("chip.tune")
        rows_ = VGroup(*[VGroup(label(n, font_size=20, color=col), label(w, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.4)
                         for n, w, col in ((r"pulse 1, \ 50\%", r"the melody", TUNE), (r"pulse 2, \ 25\%", r"the chords, \ as arpeggios", BLUE),
                                           (r"triangle", r"the bass", "#A3E635"), (r"noise", r"a short hit every other note", EAR))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(UP * 0.4)
        head = label(r"the Tune on the chip", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is the Tune's first two phrases on the chip, with every channel used: the melody on one pulse, the chords "
            "as arpeggios on the other, the bass on the triangle, and a short noise hit as a drum."
        ):
            self.play(FadeIn(head), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ chip", kind="synthesized", detail=r"our chip", corner=DL, tag_corner=DR)
            for i in range(4):
                pulse(snd, rows_[i], 0.0, c.duration, buff=0.06, rate=8.0 + 3 * i)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def style(self):
        items = [
            (r"limits became a style: \ fast arpeggios, \ echo made by repeating a note softer, \ drums from noise", WHITE),
            (r"Koji Kondo's \textit{Super Mario Bros.} \ (1985) \ fitted a whole score into three tones and a noise", WHITE),
            (r"melodies had to carry alone: \ few voices make strong tunes \ (Part 14's arches and steps)", WHITE),
            (r"chiptune is now a genre of its own, \ played on the old machines and on new ones", TUNE),
            (r"Part 51 builds oscillators and filters from scratch", GREY_A),
        ]
        rows_scene(self, r"limits as a style", items,
                   "The limits became a style. <bookmark mark='b'/> Fast arpeggios for chords, echo made by repeating a note "
                   "softer a moment later, drums from noise. <bookmark mark='c'/> Koji Kondo's score for Super Mario Bros., in "
                   "1985, fitted everything into the console's few channels. <bookmark mark='d'/> Melodies had to carry alone, "
                   "and few voices make strong tunes. <bookmark mark='e'/> Chiptune is now a genre of its own, played on the old "
                   "machines and new ones. <bookmark mark='f'/> Part 51 builds oscillators and filters from scratch.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def fm(self):
        items = [
            (r"from the late 1980s, \ FM chips from Yamaha gave consoles and PCs several voices with rich, \ changing timbres", WHITE),
            (r"FM: \ one oscillator bends another's frequency, \ making many partials from two sine waves \ (Part 52)", WHITE),
            (r"then sample playback, \ then streamed recordings: \ by the 2000s a game could carry an orchestra", WHITE),
            (r"the limit moved from the sound to the structure: \ how the music adapts", TUNE),
            (r"chapter 10: \ scores that compose themselves", GREY_A),
        ]
        rows_scene(self, r"after the chips", items,
                   "The chips grew. <bookmark mark='b'/> From the late 1980s, FM chips from Yamaha gave consoles and personal "
                   "computers several voices with rich, changing timbres. <bookmark mark='c'/> FM, frequency modulation, lets "
                   "one oscillator bend another's frequency and so makes many partials from two sine waves, as Part 52 will "
                   "show. <bookmark mark='d'/> Then came sample playback, and then streamed recordings: by the 2000s a game could "
                   "carry a recorded orchestra. <bookmark mark='e'/> The limit moved from the sound to the structure, to how the "
                   "music adapts. <bookmark mark='f'/> Chapter ten looks at scores that compose themselves.", marks="bcdef")

    # ------------------------------------------------------------------
    def noise(self):
        c = clip("noise.three")
        d = load("noise")
        reg = VGroup(*[Square(0.38, stroke_color=GREY_B, stroke_width=2).move_to([-2.7 + 0.4 * i, 1.4, 0]) for i in range(15)])
        bits = VGroup(*[label(b, font_size=16, color=WHITE).move_to(reg[i]) for i, b in enumerate("100110101110001")])
        xor = VGroup(Circle(radius=0.2, color=TUNE), label(r"$\oplus$", font_size=22, color=TUNE)).move_to([-2.7 + 0.4 * 15 + 0.5, 0.6, 0])
        arrows = VGroup(Arrow(reg[0].get_bottom(), xor.get_left() + LEFT * 0.1 + DOWN * 0.0, buff=0.05, color=GREY_B, stroke_width=2),
                        Arrow(reg[1].get_bottom(), xor.get_left(), buff=0.05, color=GREY_B, stroke_width=2),
                        Arrow(xor.get_top(), reg[14].get_right() + RIGHT * 0.05, buff=0.05, color=TUNE, stroke_width=2))
        side = VGroup(label(r"a 15-bit shift register: \ each step, \ two bits are combined and fed back in", font_size=19, color=WHITE),
                      label(r"long mode: \ 32,767 steps before it repeats \ --- \ hiss", font_size=19, color=WHITE),
                      label(r"short mode: \ a shorter loop \ --- \ a metallic, \ pitched buzz", font_size=19, color=WHITE),
                      label(r"a fast clock and a short decay make a hi-hat; \ a slow one, \ a snare or an explosion", font_size=19, color=TUNE)).arrange(DOWN, buff=0.28).move_to(DOWN * 1.4)
        head = label(r"the noise channel", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The noise channel is not random at all. A fifteen-bit shift register combines two of its bits at each step and "
            "feeds the result back in. In its long mode it runs thirty-two thousand seven hundred and sixty-seven steps before "
            "repeating, and sounds like hiss; in its short mode the loop is short enough to have a pitch, a metallic buzz. "
            "Clocked fast with a short decay it is a hi-hat; slowly, a snare or an explosion. Hear the long mode, the short "
            "mode, and three noise drums."
        ):
            self.play(FadeIn(head), FadeIn(reg), FadeIn(bits), FadeIn(xor), FadeIn(arrows), FadeIn(side))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"noise, \ long and short", kind="synthesized", detail=r"our chip", corner=DL, tag_corner=DR)
            pulse(snd, side[1], st["long"], st["short"] - 0.3, buff=0.08)
            pulse(snd, side[2], st["short"], st["drums"] - 0.3, buff=0.08)
            pulse(snd, side[3], st["drums"], c.duration, buff=0.08)
        self.wait(0.3)
        self.clear_scene()
