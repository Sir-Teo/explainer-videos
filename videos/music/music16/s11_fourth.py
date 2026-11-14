from __future__ import annotations

import numpy as np

from videos.music.music16.common import *  # noqa: F403
from videos.music.music16.s09_second import species_scene


class Fourth(SoundScene):
    def construct(self):
        chapter(self, 10, r"Held over", r"What is a suspension?")
        self.how()
        self.quiz()
        self.hear()

    def how(self):
        steps = [(r"1. \ prepare", r"D over F: \ a sixth, \ consonant", WHITE), (r"2. \ hold", r"the cantus moves to E: \ D over E is a seventh", EAR),
                 (r"3. \ resolve", r"D falls a step to C: \ a sixth", TUNE)]
        g = duet([[(74, 2, 4), (72, 6, 2)], [(65, 0, 4), (64, 4, 4)]], width=6.0, height=2.6, lo=60, hi=78, thick=0.17, bar=4.0).move_to(LEFT * 2.8 + DOWN * 0.3)
        tie = label(r"held", font_size=22, color=EAR).next_to(g.notes[0][0], UP, buff=0.2)
        txt = VGroup(*[VGroup(label(a, font_size=28, color=c), label(b, font_size=22, color=GREY_A)).arrange(DOWN, buff=0.1, aligned_edge=LEFT) for a, b, c in steps]).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to(RIGHT * 3.6 + DOWN * 0.2)
        head = label(r"syncopation: \ the new voice moves while the cantus holds, \ and holds while it moves", font_size=26, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Fourth species shifts the new voice by half a bar. Each of its notes begins in the middle "
            "of a cantus note and is held over into the next. When the cantus moves underneath a held "
            "note, the interval can become a dissonance on the strong beat, where it is most exposed. "
            "<bookmark mark='a'/> The note must first be consonant when it arrives: the preparation. "
            "<bookmark mark='b'/> Then the cantus moves, and the held note becomes a dissonance: the "
            "suspension. <bookmark mark='c'/> And then it must fall by step to a consonance: the "
            "resolution. A seven falling to a six, a four falling to a three."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(tie))
            for mark, t in zip("abc", txt):
                vo.wait_until(mark)
                self.play(FadeIn(t))
        cap = label(r"dissonance as delay: \ the voice that should have moved has not, \ yet", font_size=28, color=TUNE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A suspension is a dissonance of a different kind from a passing note. It is not on the "
            "way between two consonances. It is a consonance that has stayed too long: the note that "
            "should have moved when the cantus did has not moved yet. You hear the delay, and then you "
            "hear it paid off. A great deal of expressive music, from Palestrina to the slow movements "
            "of Mozart, lives in that delay."
        ):
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def quiz(self):
        d = load("more")["suspension"]
        c = clip("more.suspension")
        cf = [(p, 4.0 * k, 4.0) for k, p in enumerate(d["cf"])]
        gA = duet([[tuple(e) for e in d["A"]], cf], width=5.4, height=2.6, lo=58, hi=79, thick=0.15, bar=4.0).move_to(LEFT * 3.3 + UP * 0.1)
        gB = duet([[tuple(e) for e in d["B"]], cf], width=5.4, height=2.6, lo=58, hi=79, thick=0.15, bar=4.0).move_to(RIGHT * 3.3 + UP * 0.1)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        card = listen_card(r"The same five notes over a falling cantus, \ twice: \ once moving with it, \ once held over. \ In which do you hear a clash on the strong beats: \ A or B?", width=10.0)
        with self.voiceover(
            "Hear it before seeing it. The same five notes in the upper voice, over a falling cantus, "
            "twice: once moving with the cantus, once held over. In which do you hear a clash on the "
            "strong beats, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            sing_voice(snd, gA.notes[0], d["times"]["A"][0], base=UP_C)
            sing_voice(snd, gA.notes[1], d["times"]["A"][1], base=CF_C)
            sing_voice(snd, gB.notes[0], d["times"]["B"][0], base=UP_C)
            sing_voice(snd, gB.notes[1], d["times"]["B"][1], base=CF_C)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        sus = {(int(p), float(a)) for p, a, iv in d["suspensions"]}
        marks = [k for k, e in enumerate(d["B"]) if (int(e[0]), float(e[1])) in sus]
        ansA = label(r"parallel sixths: \ consonant all the way", font_size=24, color=GREY_A).next_to(gA, DOWN, buff=0.35)
        ansB = label(r"three sevenths, \ each falling to a sixth", font_size=24, color=EAR).next_to(gB, DOWN, buff=0.35)
        with self.voiceover(
            "B. In A the upper voice moves with the cantus in parallel sixths: pleasant, and a little "
            "bland. In B each note arrives half a bar late and is still sounding when the cantus moves: "
            "three sevenths on the strong beats, each falling a step to a sixth. A chain of seven-six "
            "suspensions. The notes are the same; only the timing makes the dissonance, and the timing "
            "is also what keeps the voices apart."
        ):
            self.play(FadeIn(ansA), FadeIn(ansB), *[gB.notes[0][k].animate.set_fill(EAR) for k in marks])
        self.wait(0.4)
        self.clear_scene()

    def hear(self):
        d = load("species")["4"]
        species_scene(self, 4,
                      "Here is a fourth-species line over Fux's cantus. The pink notes are the suspensions.",
                      f"{len(d['suspensions'])} suspensions, each a seventh resolving to a sixth, and a "
                      "chain of syncopations that never lets the two voices start together until the "
                      "last note: one note in twenty begins with the cantus. Of all the species, this one "
                      "keeps the voices most apart in time.",
                      r"pink: \ suspensions")
