from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403
from explainer.music.monochord import blues as BL

NN = ["C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


class Modal(SoundScene):
    def construct(self):
        chapter(self, 5, r"Modal jazz and quartal voicings", r"What happens when the chords stop changing?")
        self.kind()
        self.form()
        self.voicing()
        self.hear()
        self.after()

    # ------------------------------------------------------------------
    def kind(self):
        items = [
            (r"1959: \ Miles Davis's \textit{Kind of Blue}, \ with John Coltrane, \ Cannonball Adderley and Bill Evans", WHITE),
            (r"few chords, \ held for many bars: \ a mode to explore instead of changes to navigate", WHITE),
            (r"Davis had found bebop's changes a cage; \ the new frame left room for melody", WHITE),
            (r"one of the best-selling jazz albums ever made", TUNE),
            (r"the same year as \textit{Giant Steps}: \ two opposite answers to bebop", GREY_A),
        ]
        rows_scene(self, r"Kind of Blue", items,
                   "In 1959 Miles Davis recorded Kind of Blue, with John Coltrane, Cannonball Adderley and Bill Evans. "
                   "<bookmark mark='b'/> Its tunes have few chords, held for many bars: a mode to explore instead of changes to "
                   "navigate. <bookmark mark='c'/> Davis had come to find bebop's dense changes confining, and the new frame left "
                   "room for melody. <bookmark mark='d'/> It became one of the best-selling jazz albums ever made. "
                   "<bookmark mark='e'/> And it was the same year as Giant Steps: two opposite answers to bebop, from the same "
                   "saxophonist.", marks="bcde")

    # ------------------------------------------------------------------
    def form(self):
        d = load("modal")
        n = d["so_what_bars"]
        blocks = VGroup()
        for name, bars, col in ((r"A: \ D dorian", 8, TUNE), (r"A: \ D dorian", 8, TUNE), (r"B: \ E$\flat$ dorian", 8, EAR), (r"A: \ D dorian", 8, TUNE)):
            r = Rectangle(width=2.8, height=0.9, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.2)
            blocks.add(VGroup(r, label(name, font_size=20, color=WHITE).move_to(r), label(rf"{bars} bars", font_size=16, color=GREY_A).next_to(r, DOWN, buff=0.12)))
        blocks.arrange(RIGHT, buff=0.15).move_to(UP * 0.6)
        notes = VGroup(label(r"the form of \textit{So What}: \ 32 bars, \ AABA, \ two chords in all", font_size=21, color=WHITE),
                       label(r"D dorian: \ D E F G A B C, \ the white keys from D; \ then up a semitone, \ and back", font_size=20, color=GREY_A),
                       label(r"against \textit{Giant Steps}' 26 chords in 16 bars", font_size=20, color=EAR)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.9)
        head = label(r"two chords, \ thirty-two bars", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The album's first track, So What, has the simplest form imaginable. <bookmark mark='a'/> Thirty-two bars in "
            "the song form A A B A, with two chords in all: sixteen bars of D dorian, eight of E flat dorian, a semitone up, "
            "and eight of D again. <bookmark mark='b'/> D dorian is the white keys from D. Compare Giant Steps, recorded weeks "
            "later: twenty-six chords in sixteen bars. Here the soloist has eight bars at a time on one mode, and must find "
            "the shape somewhere other than in the changes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(blocks.copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in blocks], lag_ratio=0.2), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def voicing(self):
        d = load("modal")
        q = d["quartal"]
        y0 = -1.6
        keys = VGroup()
        for i, m in enumerate(q):
            dot = Dot([-3.0, y0 + 0.16 * (m - q[0]), 0], radius=0.13, color=TUNE)
            keys.add(VGroup(dot, label(NN[m % 12], font_size=20, color=WHITE).next_to(dot, LEFT, buff=0.2)))
        ints = VGroup()
        for i in range(len(q) - 1):
            mid = (keys[i][0].get_center() + keys[i + 1][0].get_center()) / 2
            n = q[i + 1] - q[i]
            ints.add(label({5: r"a fourth", 4: r"a major third"}[n], font_size=17, color=GREY_A).move_to(mid + RIGHT * 1.0))
        tert = [50, 53, 57, 60, 64]
        keys2 = VGroup()
        for m in tert:
            dot = Dot([2.4, y0 + 0.16 * (m - q[0]), 0], radius=0.13, color=BLUE)
            keys2.add(VGroup(dot, label(NN[m % 12], font_size=20, color=WHITE).next_to(dot, LEFT, buff=0.2)))
        cap = VGroup(label(r"quartal: \ stacked fourths", font_size=20, color=TUNE).next_to(keys, DOWN, buff=0.5),
                     label(r"tertian: \ stacked thirds \ (Dm9)", font_size=20, color=BLUE).next_to(keys2, DOWN, buff=0.5))
        side = label(r"quartal spacing can leave the root implicit\\bass and context still establish mode", font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"a voicing in fourths", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Quartal voicings became one influential option for modal jazz, rather than a requirement of static harmony. <bookmark mark='a'/> Pianists stacked fourths instead of thirds: E, A, D, G, and a major third to B on top, the voicing heard on So What. <bookmark mark='b'/> Beside it, the same mode's chord in thirds, a D minor ninth. Quartal spacing can make the root less explicit; the collection can still contain thirds and take a clear modal quality from the bass and context, so they float over the mode instead of pinning it to a chord. McCoy Tyner, Coltrane's pianist from 1960, built a whole style on them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(keys.copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(k) for k in keys], lag_ratio=0.2), FadeIn(ints), FadeIn(cap[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(k) for k in keys2], lag_ratio=0.2), FadeIn(cap[1]), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("modal")
        c = clip("modal.vamp")
        line = [tuple(x) for x in d["line"]]
        g = line_over(line, d["form"], width=11.6, height=2.4, color=TUNE, size=12).move_to(DOWN * 0.3)
        head = label(r"a modal vamp of ours: \ 8 bars of D dorian, \ 4 of E$\flat$, \ 4 of D", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(rf"quartal piano chords, \ bass and ride; \ the program's line on top \ ({round(100 * d['judge']['on_beat_chord_tones'])}\% of beats on chord tones)", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Hear a modal vamp of our own: eight bars of D dorian, four of E flat dorian, four of D, with quartal chords on "
            "the piano and the improviser's line on top. With one chord for eight bars, the line has to make its own shape; "
            "notice how the move up a semitone, when it comes, sounds like a change of light."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(cap))
        beat = 60.0 / d["bpm"]
        with self.listen(c) as snd:
            window(snd, r"a modal vamp", kind="synthesized", detail=r"an additive saxophone, \ piano, \ string and cymbal", corner=DL, tag_corner=DR)
            flash(snd, g.roll.notes, list(BL.swing_times([e for _, e in line], d["bpm"])), hot=WHITE, base=TUNE)
            cursor(snd, g.roll, 0.0, beat / 2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def after(self):
        items = [
            (r"Coltrane's \textit{Impressions} \ (1961) \ reuses the form of \textit{So What}, \ at speed", WHITE),
            (r"Herbie Hancock's \textit{Maiden Voyage} \ (1965): \ suspended chords, \ no dominant anywhere", WHITE),
            (r"Indian music influenced Coltrane's modal playing \ (Part 34's drone and raga)", WHITE),
            (r"modal jazz led to rock and soul's one-chord vamps, \ and to fusion", TUNE),
            (r"chapter 6 returns to the other road: \ more changes, \ not fewer", GREY_A),
        ]
        rows_scene(self, r"after Kind of Blue", items,
                   "Modal jazz spread quickly. <bookmark mark='b'/> Coltrane's Impressions, from 1961, reuses the form of So "
                   "What at speed. <bookmark mark='c'/> Herbie Hancock's Maiden Voyage, from 1965, uses suspended chords with no "
                   "dominant anywhere. <bookmark mark='d'/> Indian music influenced Coltrane's modal playing, Part 34's drone and "
                   "raga meeting jazz. <bookmark mark='e'/> And modal jazz led to the one-chord vamps of rock and soul, and to "
                   "fusion. <bookmark mark='f'/> Chapter six returns to the other road: more changes, not fewer.", marks="cdef")
