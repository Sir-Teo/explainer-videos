from __future__ import annotations

import numpy as np

from explainer.music.monochord import chromatic as X
from videos.music.music19.common import *  # noqa: F403

ORDER = [(0, "major"), (9, "minor"), (7, "major"), (4, "minor"), (2, "major"), (11, "minor"), (9, "major"), (6, "minor"),
         (4, "major"), (1, "minor"), (11, "major"), (8, "minor"), (6, "major"), (3, "minor"), (1, "major"), (10, "minor"),
         (8, "major"), (5, "minor"), (3, "major"), (0, "minor"), (10, "major"), (7, "minor"), (5, "major"), (2, "minor")]
HEAT = ["#F5C542", "#E8A23A", "#C77B3F", "#9A5A4A", "#6B4255", "#47365A", "#2E2B4F", "#1F2338"]


def vl_matrix():
    n = len(ORDER)
    m = np.zeros((n, n), dtype=int)
    for i, a in enumerate(ORDER):
        for j, b in enumerate(ORDER):
            m[i, j] = X.voice_leading(X.triad(*a), X.triad(*b))["cost"]
    return m


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 12, r"Frontier: \ extended tonality", r"Is chromatic harmony a geometry?", extra=((2006, r"Tymoczko's geometry of chords"),),
                spoken="Frontier: extended tonality")
        self.matrix()
        self.geometry()
        self.history()

    # ------------------------------------------------------------------
    def matrix(self):
        m = vl_matrix()
        n = len(ORDER)
        cell = 0.22
        grid = VGroup()
        for i in range(n):
            for j in range(n):
                sq = Square(side_length=cell * 0.92, stroke_width=0, fill_color=HEAT[min(m[i, j], len(HEAT) - 1)], fill_opacity=1.0)
                sq.move_to([(j - n / 2 + 0.5) * cell, (n / 2 - 0.5 - i) * cell, 0])
                grid.add(sq)
        grid.move_to(LEFT * 3.4 + DOWN * 0.3)
        nm = lambda t: X.CH.triad_name(t) if hasattr(X, "CH") else str(t)  # noqa: E731
        ticks = VGroup()
        for k in (0, 2, 12, 22):
            lab = label(tex(nm(ORDER[k])), font_size=16, color=GREY_B).next_to(grid[k], UP, buff=0.12)
            ticks.add(lab)
        cap = label(r"24 triads, \ in circle-of-fifths order: \ the least voice-leading motion between each pair", font_size=21, color=GREY_A).next_to(grid, UP, buff=0.45)
        cnt1 = int(((m == 1).sum()) // 2)
        cnt2 = int(((m == 2).sum()) // 2)
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"bright: \ one semitone of motion; \ dark: \ many", WHITE),
            (rf"{cnt1} pairs one semitone apart: \ P, \ L, \ and nothing else", WHITE),
            (rf"{cnt2} pairs two semitones apart: \ R, \ the mediants", WHITE),
            (r"near the diagonal: \ close in key", WHITE),
            (r"bright cells far from it: \ close in motion, \ far in key", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.2))
        rows_.move_to(RIGHT * 3.4 + DOWN * 0.1)
        with self.voiceover(
            "Measure every pair of the twenty-four major and minor triads by the least motion that carries one onto "
            "the other, and lay them out in circle-of-fifths order. <bookmark mark='a'/> Bright cells are close, dark "
            f"cells far. <bookmark mark='b'/> {say(cnt1)} pairs are a single semitone apart: exactly the P and L moves "
            f"of chapter eight. <bookmark mark='c'/> {say(cnt2)} more are two semitones apart. <bookmark mark='d'/> Near "
            "the diagonal, the chords are close in key. But there are bright cells far from the diagonal: chords "
            "from distant keys that are next to each other in motion. That is the space chromatic harmony explores."
        ) as vo:
            self.play(FadeIn(cap), FadeIn(grid), FadeIn(ticks))
            for mark, r in zip("abcd", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
            self.play(FadeIn(rows_[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def geometry(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"1853: \ Weitzmann: \ the augmented triad as a hub, \ six triads a semitone away", WHITE),
            (r"1880s: \ Riemann: \ harmony as transformations between triads", WHITE),
            (r"1996: \ Cohn: \ the hexatonic and octatonic cycles; \ 2012, \ \textit{Audacious Euphony}", WHITE),
            (r"2006: \ Tymoczko: \ chords as points in a space of voicings, \ an orbifold \ (\textit{Science})", TUNE),
            (r"nearly even chords sit near the centre, \ with the shortest moves to many others", WHITE),
            (r"the triad and the dominant seventh: \ nearly even, \ which is why they move so smoothly", GREY_A))]).arrange(DOWN, buff=0.33, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"harmony as a geometry of motion", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The idea is older than it looks. <bookmark mark='a'/> In 1853 Carl Friedrich Weitzmann noticed that the "
            "augmented triad sits a semitone from six different major and minor triads, a hub for chromatic moves. "
            "<bookmark mark='b'/> In the 1880s Hugo Riemann described harmony as transformations between triads. "
            "<bookmark mark='c'/> In 1996 Richard Cohn revived those transformations and found the hexatonic cycles, "
            "and his 2012 book Audacious Euphony applied them to Schubert, Liszt and Wagner. <bookmark mark='d'/> In "
            "2006 Dmitri Tymoczko, in the journal Science, placed every chord as a point in a geometric space of "
            "voicings, with voice leadings as paths. <bookmark mark='e'/> In that space, chords that divide the octave "
            "nearly evenly sit near the centre, with short paths to many others. <bookmark mark='f'/> The major triad "
            "and the dominant seventh are nearly even, which may be one reason why they became the chords of tonal "
            "music: they can always move smoothly somewhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcdef", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        rows_ = VGroup(*[label(t, font_size=24, color=c_) for t, c_ in (
            (r"corpus studies: \ measure how far the harmony strays from one key, \ piece by piece, \ century by century", WHITE),
            (r"the measure rises from the Baroque to the late nineteenth century \ (Part 27 measures it)", WHITE),
            (r"film scores: \ chromatic mediants for wonder, \ the hexatonic pole for menace \ (Lehman, \ 2018)", WHITE),
            (r"open: \ is extended tonality a grammar \ (Part 22), \ or a geometry, \ or both?", TUNE))]).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 12.6))
        rows_.move_to(DOWN * 0.1)
        head = label(r"what is still open", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "And the questions now. <bookmark mark='a'/> Corpus studies measure, piece by piece, how far the harmony "
            "strays from a single key. <bookmark mark='b'/> Across the Baroque, Classical and Romantic eras the measure "
            "rises, and Part 27 builds such an index itself. <bookmark mark='c'/> In film music, Frank Lehman's 2018 "
            "book Hollywood Harmony traces chromatic mediants used for wonder, and the hexatonic pole, a major chord "
            "and the minor chord a major third below, used for menace. <bookmark mark='d'/> And the open question: is "
            "this music best described as a grammar, the subject of Part 22, or as a geometry of smooth motion, or "
            "both at once?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcd", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
