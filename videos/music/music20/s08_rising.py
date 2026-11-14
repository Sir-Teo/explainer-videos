from __future__ import annotations

import numpy as np

from videos.music.music20.common import *  # noqa: F403

PCS = ["C", "C♯", "D", "D♯", "E", "F", "F♯", "G", "G♯", "A", "A♯", "B"]


class Rising(SoundScene):
    def construct(self):
        chapter(self, 7, r"A canon that never arrives", r"Can music rise for ever?")
        self.per_tonos()
        self.hear()
        self.loop()

    # ------------------------------------------------------------------
    def per_tonos(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"\textit{Canon per tonos}: \ it ends a tone higher than it began", WHITE),
            (r"played six times round, \ it rises through six keys and ends an octave up", WHITE),
            (r"`as the modulation rises, \ so may the glory of the King'", TUNE),
            (r"Part 4's Shepard tones: \ every note an octave stack under a fixed envelope", WHITE),
            (r"rising a tone each time, \ the canon can go round for ever", EAR))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"the endlessly rising canon", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The other famous canon of the Musical Offering is the canon through the keys. <bookmark mark='a'/> It is "
            "written so that it ends a whole tone higher than it began, ready to start again there. "
            "<bookmark mark='b'/> Played six times round, it climbs through six keys and arrives where it began, an "
            "octave higher. <bookmark mark='c'/> Bach's inscription: as the modulation rises, so may the glory of the "
            "King. <bookmark mark='d'/> Part 4 built a sound that makes the climb endless, the Shepard tone: each note "
            "a stack of octaves under a fixed bell of loudness, so that twelve semitones up is the same sound. "
            "<bookmark mark='e'/> Play a rising canon in Shepard tones, and it can climb for ever without getting "
            "anywhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("rising")
        c = clip("rising.shepard")
        g = voices_roll([d["leader"], d["follower"]], width=5.4, height=2.6, lo=48, hi=76, total=d["lap_beats"]).move_to(LEFT * 3.4 + DOWN * 0.2)
        t = label(r"one lap: \ a canon from the solver, \ at the fifth below", font_size=22, color=GREY_A).next_to(g, UP, buff=0.3)
        R = 1.9
        centre = RIGHT * 3.6 + DOWN * 0.2
        ring = Circle(radius=R, color=DIM, stroke_width=2).move_to(centre)
        labs = VGroup(*[label(tex(PCS[k]), font_size=20, color=GREY_B).move_to(centre + (R + 0.35) * np.array([np.sin(2 * np.pi * k / 12), np.cos(2 * np.pi * k / 12), 0])) for k in range(12)])
        laps = VGroup(*[Dot(centre + R * np.array([np.sin(2 * np.pi * 2 * L / 12), np.cos(2 * np.pi * 2 * L / 12), 0]), radius=0.13, color=TUNE) for L in range(7)])
        key_lab = label(r"the key of each lap", font_size=22, color=GREY_A).next_to(ring, UP, buff=0.55)
        with self.voiceover(
            "Here is a two-voice canon the solver found, at the fifth below, eight notes long. It is played seven "
            "times, each lap a whole tone higher than the last, every note a Shepard tone. On the right, the key of "
            "each lap goes round the clock of Part 12; after six laps it is back where it started. Listen to whether "
            "the music ever comes home."
        ):
            self.play(FadeIn(g), FadeIn(t), Create(ring), FadeIn(labs), FadeIn(key_lab), FadeIn(laps))
        with self.listen(c) as snd:
            window(snd, r"the canon, \ a tone higher each lap, \ in Shepard tones", detail=r"synthesized", corner=DL, tag_corner=DR)
            lap_s = d["lap_beats"] * d["beat"]
            for L in range(7):
                sing_voices(snd, g, [d["leader"], d["follower"]], start=L * lap_s, beat=d["beat"])
            flash(snd, list(laps), [L * lap_s for L in range(7)], hot=WHITE, base=TUNE, hold=lap_s * 0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def loop(self):
        rows_ = VGroup(*[label(t, font_size=26, color=c_) for t, c_ in (
            (r"each lap sounds higher than the last", WHITE),
            (r"the seventh lap is the first lap, \ note for note", WHITE),
            (r"pitch has two parts: \ height, \ and where you are in the octave \ (Part 4)", WHITE),
            (r"Shepard tones keep the second and hide the first", TUNE),
            (r"Hofstadter's word for it: \ a strange loop", GREY_A))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"a strange loop", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "Most listeners hear every lap as higher than the one before. <bookmark mark='a'/> <bookmark mark='b'/> "
            "Yet the seventh lap is the first lap, sample for sample. <bookmark mark='c'/> Part 4 explained why: pitch "
            "has two parts, height, and where a note sits within the octave, its chroma. <bookmark mark='d'/> Shepard "
            "tones keep the chroma and hide the height, so each step up is heard as up, and the steps add up to "
            "nothing. <bookmark mark='e'/> Hofstadter called this a strange loop, a hierarchy that, climbed far enough, "
            "returns to its start, and he took Bach's rising canon as his first example."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
