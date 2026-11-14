from __future__ import annotations

import numpy as np

from videos.music.music12.common import *  # noqa: F403


class Minor(SoundScene):
    def construct(self):
        chapter(self, 5, r"Minor's three forms", r"Why does the minor scale keep changing?")
        self.three()
        self.leading()

    # ------------------------------------------------------------------
    def three(self):
        d = load("minor")
        c = clip("minor.three")
        forms = [("natural", r"natural: \ the Aeolian mode", ["A3", "B3", "C4", "D4", "E4", "F4", "G4", "A4"]),
                 ("harmonic", r"harmonic: \ the seventh raised", ["A3", "B3", "C4", "D4", "E4", "F4", "G#4", "A4"]),
                 ("melodic", r"melodic: \ the sixth and seventh raised, \ going up", ["A3", "B3", "C4", "D4", "E4", "F#4", "G#4", "A4"])]
        rows = VGroup()
        staves = {}
        for key, name, notes in forms:
            st = scale_staff(None, names=notes, width=6.4, space=0.17)
            staves[key] = st
            rows.add(VGroup(st, label(name, font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(UP * 0.3)
        gap = SurroundingRectangle(VGroup(staves["harmonic"].notes[5].head, staves["harmonic"].notes[6].head), color=BAD, buff=0.14, stroke_width=3)
        gl = label(r"3 semitones", font_size=22, color=BAD).next_to(gap, UP, buff=0.08)
        top = label(r"the minor scale, \ on A", font_size=30, color=GREY_A).to_edge(UP, buff=0.35)
        rows.shift(DOWN * 0.3)
        gap.shift(DOWN * 0.3)
        gl.shift(DOWN * 0.3)
        with self.voiceover(
            "The darker modes have a problem, and the way musicians solved it gave the minor scale three "
            "forms. <bookmark mark='a'/> The natural minor is the Aeolian mode: on A, all white keys. "
            "<bookmark mark='b'/> The harmonic minor raises the seventh note by a semitone, for a reason "
            "we will hear in a moment. But that leaves a step of three semitones between the sixth and "
            "the seventh, awkward to sing. <bookmark mark='c'/> So the melodic minor raises the sixth as "
            "well, on the way up, and puts both back on the way down, where the pull toward the top note "
            "is not needed."
        ) as vo:
            self.play(FadeIn(top))
            for mark, r in zip("abc", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.7)
                if mark == "b":
                    self.wait(4.0)
                    self.play(Create(gap), FadeIn(gl))
        with self.listen(c) as snd:
            window(snd, r"natural; \ harmonic; \ melodic, \ up and down", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, (key, _, _) in enumerate(forms):
                t0 = d["starts"][k]
                pulse(snd, rows[k][1], t0, t0 + (5.4 if key == "melodic" else 3.0), buff=0.08)
                flash(snd, [n.ink for n in staves[key].notes], d["note_times"][key], base=WHITE, hot=TUNE, fade=0.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def leading(self):
        c = clip("minor.leading")
        card = listen_card(r"Two endings on the same chord. \ Which sounds more final: \ A or B?", width=8.8)
        with self.voiceover("Why raise the seventh at all? Listen to two endings on the same chord. Which sounds more final: A or B?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        bx = boxes(("A", "B"), buff=1.2, width=2.4, height=1.2, font_size=48).move_to(UP * 1.4)
        self.play(FadeOut(card), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, bx[0], snd.time_of("A"), snd.time_of("B") - 0.9)
            pulse(snd, bx[1], snd.time_of("B"), c.duration)
        kb = keyboard(-5, 12, width=8.0, height=1.5).move_to(DOWN * 1.0)
        kb.light(-5, GREY_B)                                         # G: the natural seventh of A minor
        lead = kb.light(-4, TUNE)                                    # G sharp: the leading note
        kb.light(-3, GOOD)                                           # A: home
        ta = label(r"A: \ the natural seventh is a whole tone below home", font_size=26, color=GREY_A)
        tb = label(r"B: \ the raised seventh is a semitone below: \ a leading note", font_size=26, color=TUNE)
        VGroup(ta, tb).arrange(DOWN, buff=0.25).next_to(kb, DOWN, buff=0.4)
        with self.voiceover(
            "Most listeners choose B. The two differ in one note of the first chord. In A it is the "
            "natural seventh of the scale, a whole tone below the home note. <bookmark mark='a'/> In B "
            "it is raised, so that it lies a semitone below. A note a semitone below home pulls upward "
            "to it; musicians call it the leading note. The major scale has one built in. The minor "
            "modes do not, so composers borrowed it, and the harmonic minor scale is the natural minor "
            "with that one loan. A scale, it turns out, is not always a fixed set of notes. It can "
            "change with what the music is doing."
        ) as vo:
            self.play(FadeIn(kb), FadeIn(ta))
            vo.wait_until("a")
            self.play(FadeIn(tb), Indicate(lead, color=TUNE))
        self.wait(0.4)
        self.clear_scene()
