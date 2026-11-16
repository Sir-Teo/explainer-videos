from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.ravel()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"A phrase on a horn; \ then the same phrase again. \ "
                           r"The second time, \ how many instruments are playing: \ one, \ two, \ or four?", width=10.4)
        with self.voiceover(
            "A question for your ears. A short phrase on a horn, and then the same phrase again. The second time, how many "
            "instruments are playing: one, two, or four?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        mel = d["melody"]
        BOLERO_PARTS = d["parts"]
        roll = mroll(mel, width=10.0, height=1.6, lo=58, hi=72, color=TUNE, total=8, bar_h=0.16).move_to(UP * 0.6)
        stage = VGroup(label(r"first", font_size=22, color=GREY_A), label(r"second", font_size=22, color=GREY_A)).arrange(RIGHT, buff=2.0).to_edge(DOWN, buff=1.4)
        self.play(FadeOut(card), FadeIn(roll), FadeIn(stage))
        beat = d["beat"]
        with self.listen(c) as snd:
            window(snd, r"a phrase, \ twice", kind="synthesized", detail=r"additive instruments from measured spectra", corner=DL, tag_corner=DR)
            for k, t0 in enumerate((d["starts"]["horn"], d["starts"]["four"])):
                flash(snd, roll.notes, [t0 + a * beat for _, a, _ in mel], hot=WHITE, base=TUNE)
            pulse(snd, stage[0], d["starts"]["horn"], d["starts"]["four"] - 0.5, buff=0.08)
            pulse(snd, stage[1], d["starts"]["four"], c.duration, buff=0.08)
        parts = VGroup(*[label(t, font_size=19, color=col) for t, col in ((r"horn: \ the melody", TUNE), (r"celesta: \ two octaves up \ (4th harmonic)", BLUE),
                                                                          (r"piccolo: \ a twelfth up \ (3rd harmonic)", EAR), (r"piccolo: \ two octaves and a third up \ (5th harmonic)", "#A3E635"))]).arrange(DOWN, buff=0.18, aligned_edge=LEFT).to_edge(DOWN, buff=0.35)
        cols4 = [TUNE, BLUE, EAR, "#A3E635"]
        voices = [[[m + sh, a, dd] for m, a, dd in mel] for _, sh, _ in BOLERO_PARTS]
        stack = voices_roll(voices, width=10.0, height=3.1, colors=cols4, total=8, lo=58, hi=102, bar_h=0.13).move_to(UP * 1.0)
        with self.voiceover(
            "Four: a horn, <bookmark mark='a'/> a celesta two octaves up, <bookmark mark='b'/> and two piccolos, one a "
            "twelfth up <bookmark mark='c'/> and one two octaves and a major third up, all moving together. "
            "<bookmark mark='d'/> The combination can suggest one composite instrument, an organ-like colour no single player owns, "
            "because each added instrument sits on a harmonic of the horn's notes: the fourth, the third and the fifth. "
            "How completely they fuse depends on performance and listening context."
        ) as vo:
            self.play(FadeOut(stage), FadeOut(roll), FadeIn(stack.parts[0]), FadeIn(parts[0]))
            for mark, k in zip("abc", (1, 2, 3)):
                vo.wait_until(mark)
                self.play(FadeIn(stack.parts[k]), FadeIn(parts[k]))
            vo.wait_until("d")
            self.play(*[VGroup(*p_.notes).animate.set_opacity(0.55) for p_ in stack.parts[1:]], run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ravel(self):
        items = [
            (r"Maurice Ravel, \ \textit{Bol\'ero} \ (1928): \ one tune in two halves, \ stated eighteen times, \ over one snare-drum rhythm", WHITE),
            (r"Ravel called it `a piece for orchestra without music': \ orchestration, density and dynamics drive most of the change", WHITE),
            (r"in one statement he puts a horn, \ a celesta and two piccolos on the tune's harmonics", WHITE),
            (r"additive synthesis \ (Part 3), \ done with players instead of oscillators", TUNE),
            (r"this part is orchestration: \ which instruments play which notes, \ and why", GREY_A),
        ]
        rows_scene(self, r"Ravel's experiment", items,
                   "That combination is Maurice Ravel's, from Boléro of 1928: two alternating melodic strains, with eighteen statements over "
                   "one unchanging rhythm on the snare drum. <bookmark mark='b'/> Ravel called it a piece for orchestra without "
                   "music: orchestration, density and dynamics drive most of the change. <bookmark mark='c'/> In one statement he puts a horn, a celesta and two "
                   "piccolos on the tune's harmonics, <bookmark mark='d'/> which is Part 3's additive synthesis done with players "
                   "instead of oscillators. <bookmark mark='e'/> This part is about orchestration: which instruments play which "
                   "notes, and why. What you heard was our own phrase, on our own instruments, with Ravel's idea.", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"an orchestra built from the series' physical models",
            r"ranges, \ registers and transposing instruments",
            r"loudness and brightness; \ why a section is not one loud player",
            r"blend, \ doubling, \ balance and spacing",
            r"textures and the melody of timbres; \ Ravel's harmonics",
            r"orchestration as search: \ a solver that matches a vowel",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. An orchestra built from the series' own physical models. <bookmark mark='b'/> Ranges, "
            "registers, and instruments that read one note and sound another. <bookmark mark='c'/> Loudness and brightness, "
            "and why a section is not one loud player. <bookmark mark='d'/> Blend, doubling, balance and spacing. "
            "<bookmark mark='e'/> Textures, the melody of timbres, and Ravel's harmonics. <bookmark mark='f'/> And "
            "orchestration as search: a solver that matches a vowel with instruments."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
