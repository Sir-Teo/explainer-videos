from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403

NN = ["C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]
MODE = {"Cmaj7": r"ionian", "C7": r"mixolydian", "Cm7": r"dorian", "Cm7b5": r"locrian", "Cdim7": r"whole-half"}


class Scales(SoundScene):
    def construct(self):
        chapter(self, 4, r"Chord scales", r"Which notes may a soloist play over a chord?")
        self.idea()
        self.table()
        self.hear()
        self.quiz()
        self.russell()
        self.critique()

    # ------------------------------------------------------------------
    def idea(self):
        items = [
            (r"chord-scale theory: \ each chord implies a seven- or eight-note scale to improvise with", WHITE),
            (r"the chord's notes, \ plus `tensions' \ (ninths, \ elevenths, \ thirteenths) \ that colour it", WHITE),
            (r"the modes of Part 12, \ chosen by the chord's quality: \ dorian for minor seventh, \ mixolydian for dominant", WHITE),
            (r"some scale notes clash when held: \ the \textit{avoid notes}, \ a semitone above a chord tone", TUNE),
            (r"a simple rule, \ computed for five chords", GREY_A),
        ]
        rows_scene(self, r"chord scales", items,
                   "Jazz teaching since the 1950s has answered with chord-scale theory: each chord implies a scale of seven or "
                   "eight notes to improvise with. <bookmark mark='b'/> The chord's own notes, plus tensions, ninths, elevenths "
                   "and thirteenths, that colour it. <bookmark mark='c'/> The scales are the modes of Part 12, chosen by the "
                   "chord's quality: dorian for a minor seventh, mixolydian for a dominant. <bookmark mark='d'/> Some scale "
                   "notes clash when they are held: the avoid notes, a semitone above a chord tone. <bookmark mark='e'/> A simple "
                   "rule, computed here for five chords.", marks="bcde")

    # ------------------------------------------------------------------
    def table(self):
        d = load("avoid")
        rows_ = VGroup()
        for s, info in d["table"].items():
            notes = VGroup()
            for p in info["scale"]:
                col = TUNE if p in info["chord"] else (RED if p in info["avoid"] else WHITE)
                notes.add(label(NN[p], font_size=19, color=col))
            notes.arrange(RIGHT, buff=0.3)
            rows_.add(VGroup(label(sym(s), font_size=22, color=WHITE), label(MODE[s], font_size=18, color=GREY_A), notes))
        for i, r in enumerate(rows_):
            y = 1.6 - 0.8 * i
            r[0].move_to([-5.4, y, 0], aligned_edge=LEFT)
            r[1].move_to([-3.6, y, 0], aligned_edge=LEFT)
            r[2].move_to([-1.2, y, 0], aligned_edge=LEFT)
        key = label(r"gold: \ chord tones; \ white: \ tensions; \ red: \ avoid notes \ (a semitone above a chord tone)", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.7)
        head = label(r"five chords on C, \ their scales and avoid notes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is the rule run on five chords built on C. <bookmark mark='a'/> Over C major seven, the ionian scale, and "
            "its F is an avoid note: it sits a semitone above E, the chord's third. Over C seven, the mixolydian, with the "
            "same F. Over C minor seven, the dorian: no avoid notes at all, which is one reason modal players loved it. Over "
            "the half-diminished chord, the locrian, whose D flat sits a semitone above the root. And over the diminished "
            "seventh, an eight-note scale alternating whole and half steps, with no avoid notes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.35), run_time=4.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("scales")
        c = clip("scales.five")
        cells = VGroup(*[VGroup(label(sym(s), font_size=24, color=WHITE), label(MODE[s], font_size=18, color=GREY_A)).arrange(DOWN, buff=0.15) for s in d["order"]]).arrange(RIGHT, buff=0.8).move_to(UP * 0.3)
        head = label(r"each chord held, \ its scale played over it", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the five: each chord held on the piano while its scale runs up over it, from C to C. Listen for the colour "
            "each scale gives its chord, and for the moment the avoid notes pass."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"five chords, \ five scales", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            ks = d["order"]
            for i, k in enumerate(ks):
                end = d["starts"][ks[i + 1]] - 0.3 if i < len(ks) - 1 else c.duration
                pulse(snd, cells[i], d["starts"][k], end, buff=0.1)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("avoid")
        c = clip("avoid.two")
        card = listen_card(r"A C major seventh chord, \ twice, \ with a saxophone holding a note above it: \ "
                           r"first one note, \ then another. \ Which held note clashes with the chord?", width=10.4)
        with self.voiceover(
            "A question for your ears. A C major seventh chord, twice, with a saxophone holding a note above it, first one "
            "note and then another. Which held note clashes with the chord, the first or the second?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=3.2, height=1.6, corner_radius=0.15, stroke_color=GREY_B), label(t, font_size=24, color=WHITE)).arrange(DOWN, buff=-1.0)
                         for t in (r"first", r"second")]).arrange(RIGHT, buff=1.5).move_to(UP * 0.3)
        self.play(FadeOut(card), FadeIn(boxes))
        with self.listen(c) as snd:
            window(snd, r"two held notes over Cmaj7", kind="synthesized", detail=r"an additive saxophone over Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], d["times"][0], d["times"][1] - 0.2, buff=0.08)
            pulse(snd, boxes[1], d["times"][1], c.duration, buff=0.08)
        ans = label(r"the first: \ F, \ a semitone above the chord's E; \ the second is E itself", font_size=22, color=TUNE).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "The first. It is F, held a semitone above the chord's E, and the two grind against each other. The second is E "
            "itself, the chord's third. In a fast line the F passes unnoticed; held, it is the avoid note."
        ):
            self.play(FadeIn(ans), boxes[0][0].animate.set_stroke(RED, 4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def russell(self):
        items = [
            (r"George Russell's \textit{Lydian Chromatic Concept of Tonal Organization} \ (1953): \ the first theory written from jazz", WHITE),
            (r"Russell made the lydian, \ not the major scale, \ the most stable: \ it avoids the avoid note", WHITE),
            (r"the Berklee school in Boston taught chord scales to generations of players from the 1950s", WHITE),
            (r"chord scales made improvising teachable, \ chord by chord", TUNE),
            (r"Miles Davis credited Russell's ideas as a source of modal jazz \ (chapter 5)", GREY_A),
        ]
        rows_scene(self, r"Russell and Berklee", items,
                   "Where did the theory come from? <bookmark mark='b'/> George Russell's Lydian Chromatic Concept of Tonal "
                   "Organization, from 1953, was the first theory written from jazz itself. <bookmark mark='c'/> Russell made the "
                   "lydian scale, not the major scale, the most stable; with its sharp fourth, it has no avoid note. "
                   "<bookmark mark='d'/> And the Berklee school in Boston taught chord scales to generations of players from the "
                   "1950s, <bookmark mark='e'/> making improvising teachable, chord by chord. <bookmark mark='f'/> Miles Davis "
                   "credited Russell's ideas as one source of modal jazz, the next chapter.", marks="cdef")

    # ------------------------------------------------------------------
    def critique(self):
        items = [
            (r"critics: \ thinking scale by scale makes lines that run up and down without going anywhere", WHITE),
            (r"the bebop masters thought in lines and targets \ (chapters 2 and 3), \ not in scales", WHITE),
            (r"a chord scale says which notes are safe, \ not which order to play them in", WHITE),
            (r"Part 22's analysts would say: \ a vocabulary is not a grammar", TUNE),
            (r"chapter 8 builds a grammar", GREY_A),
        ]
        rows_scene(self, r"a critique", items,
                   "Chord-scale theory has critics. <bookmark mark='b'/> Thinking scale by scale, they say, makes lines that "
                   "run up and down without going anywhere. <bookmark mark='c'/> The bebop masters thought in lines and targets, "
                   "as chapters two and three showed, not in scales. <bookmark mark='d'/> A chord scale says which notes are "
                   "safe, not in which order to play them. <bookmark mark='e'/> Part 22's analysts would put it this way: a "
                   "vocabulary is not a grammar. <bookmark mark='f'/> Chapter eight builds a grammar.", marks="cdef")
