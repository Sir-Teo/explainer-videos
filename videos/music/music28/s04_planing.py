from __future__ import annotations

import numpy as np

from videos.music.music28.common import *  # noqa: F403


class Planing(SoundScene):
    def construct(self):
        chapter(self, 3, r"Chords that slide", r"What if a chord is a colour, \ not a function?", extra=((1910, r"\textit{La cathédrale engloutie}"),))
        self.idea()
        self.quiz()
        self.cathedral()
        self.jazz()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"in functional harmony each chord has a job: \ tonic, \ subdominant, \ dominant \ (Part 18)", WHITE),
            (r"voices move by the shortest way, \ and parallel fifths are forbidden \ (Part 17)", WHITE),
            (r"planing: \ one chord shape under every note of the melody, \ moving in parallel", TUNE),
            (r"the chord thickens the line: \ a colour, \ like an organ stop", WHITE),
            (r"the rule against parallels broken on purpose, \ and all the time", GREY_A),
        ]
        rows_scene(self, r"planing", items,
                   "The new scales came with a new way of using chords. <bookmark mark='b'/> In functional harmony every chord "
                   "has a job, tonic, subdominant, dominant, as Part 18 said, <bookmark mark='c'/> and the voices move by the "
                   "shortest way, with parallel fifths forbidden, as in Part 17. <bookmark mark='d'/> Planing puts one chord "
                   "shape under every note of a melody and slides it along in parallel. <bookmark mark='e'/> The chord no "
                   "longer has a job; it thickens the line, like an organ stop adding a colour. <bookmark mark='f'/> The rule "
                   "against parallels is broken on purpose, in every chord.", marks="cdef")

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("planing")
        c = clip("planing.quiz")
        card = listen_card(r"The Tune's first phrase twice. \ Once each note carries the same chord, \ sliding in parallel; \ "
                           r"once the chords change by function. \ Which is planed, \ A or B?", width=10.4)
        with self.voiceover(
            "Listen for it. The Tune's first phrase twice. In one, every melody note carries the same chord shape, a major "
            "triad, sliding along with it. In the other, the chords change by function, tonic and subdominant. Which is "
            "planed, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll([d["melody"]] + d["planed"], width=5.0, height=2.6, colors=[GREY_A] * 4, lo=50, hi=86, bar_h=0.1).move_to(LEFT * 3.3 + DOWN * 0.2)
        gB = voices_roll([d["melody"], d["functional"]], width=5.0, height=2.6, colors=[GREY_A] * 2, lo=50, hi=86, bar_h=0.1).move_to(RIGHT * 3.3 + DOWN * 0.2)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, [d["melody"]] + d["planed"], d["starts"]["A"], d["unit"], colors=[GREY_A] * 4)
            flash_voices(snd, gB, [d["melody"], d["functional"]], d["starts"]["B"], d["unit"], colors=[GREY_A] * 2)
            pulse(snd, la, d["starts"]["A"], d["starts"]["B"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["B"], c.duration, buff=0.1)
        ans = VGroup(label(r"A: \ planed: \ every line parallel to the tune", font_size=21, color=TUNE).next_to(gA, DOWN, buff=0.35),
                     label(r"B: \ functional: \ I, \ IV, \ IV, \ I", font_size=21, color=BLUE).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "A is planed: look at the picture, and every line moves exactly as the tune does. The major triads are not in "
            "one key: under C the chord is F major, under G it is C major, under A it is D major, with F sharp. B stays "
            "in C, its chords chosen for their jobs. A sounds like one thick voice; B sounds like harmony."
        ):
            self.play(FadeIn(ans), *[p.animate.set_color(TUNE) for p in gA.parts], gB.parts[1].animate.set_color(BLUE))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cathedral(self):
        items = [
            (r"Debussy, \ \textit{La cathédrale engloutie} \ (1910): \ a cathedral rising from the sea and sinking back", WHITE),
            (r"chords of open fifths and octaves, \ planed, \ like an organ in the distance", WHITE),
            (r"bells: \ the chords include their own overtones \ (Part 3)", WHITE),
            (r"the same technique becomes the sound of jazz piano and of film music", TUNE),
            (r"Debussy is in the public domain; \ the next chapters' composers mostly are not, \ so the film plays its own sketches", GREY_A),
        ]
        rows_scene(self, r"a sunken cathedral", items,
                   "Debussy's best-known planing is in La cathédrale engloutie, the sunken cathedral, of 1910, a church that "
                   "rises from the sea in a legend and sinks back. <bookmark mark='c'/> Its chords of open fifths and octaves "
                   "slide in parallel, like an organ heard from far away, <bookmark mark='d'/> and they ring like bells, "
                   "because a planed chord of fifths and octaves is close to the overtones of a single note, which Part 3 "
                   "drew. <bookmark mark='e'/> The technique went on to become a sound of jazz piano and of film. "
                   "<bookmark mark='f'/> One note on what you will hear: most of this era's music is still in copyright, so "
                   "the examples in this part are the film's own sketches, built on the Tune.", marks="cdef")

    # ------------------------------------------------------------------
    def jazz(self):
        items = [
            (r"jazz arrangers' `block chords': \ the melody doubled in a chord that moves with it", WHITE),
            (r"modal jazz \ (1959): \ chords in fourths, \ planed up and down a scale", WHITE),
            (r"film scores: \ planed triads for wonder, \ for distance, \ for ritual", WHITE),
            (r"diatonic planing \ (inside a key) \ against chromatic planing \ (exact shapes, \ any key)", TUNE),
            (r"the Variation at the end planes whole-tone chords: \ nothing in it is outside the scale", GREY_A),
        ]
        rows_scene(self, r"planing after Debussy", items,
                   "Planing outlived Debussy. <bookmark mark='b'/> Jazz arrangers double a melody in block chords that move with it. <bookmark mark='c'/> Modal jazz, from 1959, slides chords built in fourths up and down a scale. <bookmark mark='d'/> Film composers plane triads for wonder, distance and ritual. <bookmark mark='e'/> There are two kinds: diatonic planing, which keeps the chords inside a key and so changes their quality, and chromatic planing, which keeps the exact shape and leaves the key behind, as our quiz did. <bookmark mark='f'/> This part's Variation planes whole-tone chords along a whole-tone melody, so that nothing in it is outside the scale.", marks="cdef")
