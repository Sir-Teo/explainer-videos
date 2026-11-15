from __future__ import annotations

import numpy as np

from videos.music.music41.common import *  # noqa: F403


class Blend(SoundScene):
    def construct(self):
        chapter(self, 5, r"Doubling, \ blend and balance", r"What happens when two instruments play the same line?")
        self.hear()
        self.numbers()
        self.masking()
        self.octaves()
        self.hear_octave()
        self.blendstudies()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("blend")
        c = clip("blend.four")
        names = ["flute", "clarinet", "flute+clarinet", "flute+trumpet"]
        labels_ = {"flute": r"flute", "clarinet": r"clarinet", "flute+clarinet": r"flute and clarinet, \ unison", "flute+trumpet": r"flute and loud trumpet, \ unison"}
        cells = VGroup(*[label(labels_[n], font_size=20, color=WHITE) for n in names]).arrange_in_grid(rows=2, cols=2, buff=(1.5, 0.8)).move_to(UP * 0.3)
        cap = label(r"all on C5", font_size=19, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Doubling: two instruments on the same line. Hear one held C, on the flute, on the clarinet, on both in unison, "
            "and then on the flute with a trumpet playing six decibels louder, as a trumpet at forte would."
        ):
            self.play(FadeIn(cells), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"four doublings", kind="synthesized", detail=r"additive, \ from measured spectra", corner=DL, tag_corner=DR)
            st = d["starts"]
            for i, n in enumerate(names):
                pulse(snd, cells[i], st[n], st[n] + 1.7, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("blend")
        st = d["stats"]
        rows_ = VGroup(
            label(r"sound", font_size=19, color=GREY_A), label(r"brightness \ (centroid)", font_size=19, color=GREY_A), label(r"flute's share of the power", font_size=19, color=GREY_A),
            label(r"flute", font_size=19, color=WHITE), label(f"{round(st['flute']['centroid'])} Hz", font_size=19, color=WHITE), label(r"100\%", font_size=19, color=WHITE),
            label(r"clarinet", font_size=19, color=WHITE), label(f"{round(st['clarinet']['centroid'])} Hz", font_size=19, color=WHITE), label(r"--", font_size=19, color=WHITE),
            label(r"flute + clarinet", font_size=19, color=TUNE), label(f"{round(st['flute+clarinet']['centroid'])} Hz", font_size=19, color=TUNE), label(f"{round(100 * st['flute+clarinet']['flute_share'])}\\%", font_size=19, color=TUNE),
            label(r"flute + loud trumpet", font_size=19, color=EAR), label(f"{round(st['flute+trumpet']['centroid'])} Hz", font_size=19, color=EAR), label(f"{round(100 * st['flute+trumpet']['flute_share'])}\\%", font_size=19, color=EAR),
        ).arrange_in_grid(rows=5, cols=3, buff=(0.9, 0.35), col_alignments="lcc").move_to(UP * 0.2)
        notes = VGroup(label(r"a unison doubling is a new timbre: \ its spectrum is the sum, \ its brightness in between", font_size=19, color=TUNE),
                       label(r"a louder partner takes most of the power: \ the flute is covered, \ not blended", font_size=19, color=EAR)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        head = label(r"the doublings, \ measured", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Measure them. <bookmark mark='a'/> A unison doubling makes a new timbre: its spectrum is the sum of the two, so "
            "its brightness lies between theirs, and the flute and clarinet each carry half the power. <bookmark mark='b'/> "
            f"With the loud trumpet the flute carries only {say(round(100 * st['flute+trumpet']['flute_share']))} per cent of "
            "the power: it is not blended but covered. Blend and balance are different questions: does it fuse, and can "
            "every part be heard?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.2)))
            vo.wait_until("a")
            self.play(FadeIn(rows_), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def octaves(self):
        items = [
            (r"doubling at the octave adds even harmonics to the lower instrument: \ brighter, \ fuller", WHITE),
            (r"a flute an octave above violins is a classic colour: \ the flute sits on the violins' second harmonic", WHITE),
            (r"doubling at the fifth or twelfth builds Ravel's organ-like mixtures \ (chapter 8)", WHITE),
            (r"doublings in octaves make a melody carry over a full orchestra", TUNE),
            (r"the pipe organ's stops do exactly this, \ with pipes \ (Part 8)", GREY_A),
        ]
        rows_scene(self, r"octaves and mixtures", items,
                   "Doubling need not be at the unison. <bookmark mark='b'/> An octave above, an instrument adds even harmonics to "
                   "the lower one, so the line sounds brighter and fuller. <bookmark mark='c'/> A flute an octave above the "
                   "violins sits on their second harmonic, a classic colour. <bookmark mark='d'/> At the fifth or the twelfth it "
                   "builds Ravel's organ-like mixtures, chapter eight's subject. <bookmark mark='e'/> Doublings in octaves let a "
                   "melody carry over a full orchestra, <bookmark mark='f'/> and the pipe organ's stops do exactly this with "
                   "pipes, as Part 8 described.", marks="cdef")

    # ------------------------------------------------------------------
    def blendstudies(self):
        items = [
            (r"Gregory Sandell \ (1995): \ listeners rate which pairs of instruments blend in unison", WHITE),
            (r"blend was better when the pair's overall brightness was lower, \ and when the instruments began together", WHITE),
            (r"Sven-Amin Lembke and Stephen McAdams: \ players adjust their own brightness to blend with a partner", WHITE),
            (r"blend is partly in the sound, \ partly in the playing", TUNE),
            (r"chapter 6: \ how the notes of a chord are spaced", GREY_A),
        ]
        rows_scene(self, r"what blends?", items,
                   "What makes instruments blend? <bookmark mark='b'/> In 1995 Gregory Sandell had listeners rate pairs of "
                   "instruments playing in unison, <bookmark mark='c'/> and blend was rated higher when the pair's overall "
                   "brightness was lower, and when the instruments began together. <bookmark mark='d'/> Later, Sven-Amin Lembke "
                   "and Stephen McAdams found that players adjust their own brightness to blend with a partner. "
                   "<bookmark mark='e'/> So blend is partly in the sound and partly in the playing. <bookmark mark='f'/> Chapter "
                   "six turns to how the notes of a chord are spaced.", marks="cdef")

    # ------------------------------------------------------------------
    def hear_octave(self):
        d = load("octave")
        c = clip("octave.two")
        cells = VGroup(label(r"violin", font_size=22, color=BLUE), label(r"violin, \ with a flute an octave above", font_size=22, color=TUNE)).arrange(RIGHT, buff=1.5).move_to(UP * 0.3)
        with self.voiceover(
            "Hear an octave doubling: a phrase on the violin, then with a flute an octave above, a little quieter. The flute "
            "is hardly heard as a second instrument; the violin seems to grow brighter and more present."
        ):
            self.play(FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"alone, \ then doubled", kind="synthesized", detail=r"additive instruments", corner=DL, tag_corner=DR)
            pulse(snd, cells[0], d["starts"]["violin"], d["starts"]["octave"] - 0.3, buff=0.1)
            pulse(snd, cells[1], d["starts"]["octave"], c.duration, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def masking(self):
        items = [
            (r"Part 4's masking: \ a loud sound hides a softer one nearby in frequency", WHITE),
            (r"a melody is covered when the accompaniment's partials sit in the same critical bands", WHITE),
            (r"so orchestrators give the melody its own register, \ or thin the accompaniment around it", WHITE),
            (r"balance is a question of bands, \ not only of decibels", TUNE),
            (r"Part 56's mixing engineers solve the same problem with equalisers", GREY_A),
        ]
        rows_scene(self, r"masking", items,
                   "Why is a part covered? <bookmark mark='b'/> Part 4's masking: a loud sound hides a softer one near it in frequency. <bookmark mark='c'/> A melody is covered when the accompaniment's partials sit in the same critical bands. <bookmark mark='d'/> So orchestrators give the melody its own register, or thin the accompaniment around it. <bookmark mark='e'/> Balance is a question of bands, not only of decibels, <bookmark mark='f'/> and Part 56's mixing engineers solve the same problem with equalisers.", marks="cdef")
