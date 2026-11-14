from __future__ import annotations

import numpy as np

from videos.music.music39.common import *  # noqa: F403
from explainer.music.monochord import blues as BL

NN = ["C", r"D$\flat$", "D", r"E$\flat$", "E", "F", r"F$\sharp$", "G", r"A$\flat$", "A", r"B$\flat$", "B"]


def major_scale(r):
    return {(r + i) % 12 for i in (0, 2, 4, 5, 7, 9, 11)}


class Thirds(SoundScene):
    def construct(self):
        chapter(self, 6, r"Third cycles", r"Why are Coltrane's changes so hard?")
        self.circle()
        self.lattice()
        self.shared()
        self.substitute()
        self.hear()
        self.legacy()

    # ------------------------------------------------------------------
    def circle(self):
        d = load("hook")
        r = 2.0
        pts = [r * np.array([np.cos(PI / 2 - k * TAU / 12), np.sin(PI / 2 - k * TAU / 12), 0]) for k in range(12)]
        circ = Circle(radius=r, color=DIM, stroke_width=1.5)
        names = VGroup(*[label(NN[k], font_size=18, color=GREY_A).move_to(pts[k] * 1.18) for k in range(12)])
        tri = Polygon(*[pts[k] for k in (11, 7, 3)], color=TUNE, stroke_width=4, fill_color=TUNE, fill_opacity=0.15)
        dots = VGroup(*[Dot(pts[k], radius=0.13, color=TUNE) for k in (11, 7, 3)])
        g = VGroup(circ, names, tri, dots).move_to(LEFT * 3.0 + DOWN * 0.2)
        side = VGroup(label(r"the tonics of \textit{Giant Steps}: \ B, \ G, \ E$\flat$", font_size=21, color=WHITE),
                      label(r"each four semitones, \ a major third, \ from the next", font_size=21, color=WHITE),
                      label(r"three major thirds make an octave: \ the cycle closes after three keys", font_size=21, color=TUNE),
                      label(r"the octave cut in three equal parts: \ an augmented triad of keys", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 3.0)
        head = label(r"three keys, \ equally spaced", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Draw the three tonics of Giant Steps on the circle of pitch classes. <bookmark mark='a'/> B, G and E flat: each "
            "is four semitones, a major third, from the next. <bookmark mark='b'/> Three major thirds make exactly an octave, "
            "so the cycle closes after three keys, and the tonics divide the octave into three equal parts, an equilateral "
            "triangle. It is an augmented triad, built of keys instead of notes. The symmetry is the same one Part 28 found "
            "in the whole-tone and octatonic scales."
        ) as vo:
            self.play(FadeIn(head), FadeIn(circ), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(side[:2]))
            vo.wait_until("b")
            self.play(Create(tri), FadeIn(side[2:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lattice(self):
        tz = tonnetz(radius=0.42, cols=7, rows_=5, origin=(-5.6, -2.6))
        tris = VGroup()
        cols = {11: TUNE, 7: BLUE, 3: EAR}
        for pc, (i, j) in ((7, (1, 0)), (11, (1, 1)), (3, (1, 2))):      # G, B, E flat: up the major-third axis
            assert tz.pc[(i, j)] == pc
            p = [tz.pos[(i, j)], tz.pos[(i + 1, j)], tz.pos[(i, j + 1)]]
            tris.add(Polygon(*p, color=cols[pc], stroke_width=3, fill_color=cols[pc], fill_opacity=0.35))
        tz_g = VGroup(tz, tris)
        side = VGroup(label(r"on the Tonnetz \ (Part 31): \ fifths to the right, \ major thirds up and to the right", font_size=19, color=WHITE),
                      label(r"the three tonic triads lie in a line up the major-third axis", font_size=19, color=TUNE),
                      label(r"far apart in fifths: \ each key is four fifths from the next", font_size=19, color=WHITE),
                      label(r"in a ii--V--I the harmony steps to a neighbour; \ here it jumps across the lattice", font_size=19, color=EAR)).arrange(DOWN, buff=0.28, aligned_edge=LEFT).to_edge(RIGHT, buff=0.3).shift(UP * 0.6)
        head = label(r"the three tonic triads on the Tonnetz", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        with self.voiceover(
            "Now put the three tonic chords on Part 31's Tonnetz, where fifths run to the right and major thirds up and to the "
            "right. <bookmark mark='a'/> The B major, G major and E flat major triads lie in a line up the major-third axis. "
            "<bookmark mark='b'/> In fifths they are far apart: each key is four fifths from the next. A two-five-one steps "
            "from a chord to a neighbour on this lattice; Coltrane's changes jump across it, and the soloist must jump with "
            "them, every two beats."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tz), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t) for t in tris], lag_ratio=0.3), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2:]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shared(self):
        pairs = [("C", "G", 0, 7), ("C", "F", 0, 5), ("B", "G", 11, 7), ("G", r"E$\flat$", 7, 3), (r"E$\flat$", "B", 3, 11)]
        rows_ = VGroup()
        for a, b, ra, rb in pairs:
            n = len(major_scale(ra) & major_scale(rb))
            bar = Rectangle(width=0.9 * n, height=0.35, stroke_width=0, fill_color=TUNE if n >= 6 else EAR, fill_opacity=0.85)
            rows_.add(VGroup(label(rf"{a} major and {b} major", font_size=20, color=WHITE), bar, label(rf"{n} of 7 notes shared", font_size=19, color=WHITE)))
        for i, r in enumerate(rows_):
            y = 1.5 - 0.75 * i
            r[0].move_to([-3.0, y, 0], aligned_edge=RIGHT)
            r[1].move_to([-2.7, y, 0], aligned_edge=LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.25)
        cap = label(r"keys a fifth apart share six notes; \ keys a major third apart share three", font_size=21, color=TUNE).to_edge(DOWN, buff=0.8)
        head = label(r"how many notes do two keys share?", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Why does that make it hard? Count the notes two major scales share. <bookmark mark='a'/> C major and G major, a "
            "fifth apart, share six of their seven notes; C and F likewise. B major and G major share three. G and E flat, "
            "three. E flat and B, three. <bookmark mark='b'/> In Giant Steps every few beats the scale under the soloist "
            "loses more than half its notes. The fingers' habits, built on neighbouring keys, stop working."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_.copy().set_opacity(0.2)))   # a ghost of what is coming: never a bare title
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows_], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def substitute(self):
        d = load("thirds")
        plain = chart(d["plain"], cell_w=2.6, cell_h=0.7, size=20)
        colt = chart(d["coltrane"], cell_w=2.6, cell_h=0.7, size=20)
        g = VGroup(VGroup(label(r"ii--V--I in C", font_size=20, color=WHITE), plain).arrange(DOWN, buff=0.2),
                   VGroup(label(r"Coltrane's substitute: \ through A$\flat$ and E", font_size=20, color=TUNE), colt).arrange(DOWN, buff=0.2)).arrange(DOWN, buff=0.6).move_to(UP * 0.2)
        cap = label(r"the same start and goal; \ in between, \ three tonics a major third apart, \ each led in by its dominant", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Coltrane used the same cycle as a substitute for an ordinary two-five-one, as in his Countdown of 1959, built "
            "on the changes of a Miles Davis tune. <bookmark mark='a'/> Instead of D minor seven, G seven, C, play D minor "
            "seven, then E flat seven to A flat major, B seven to E major, G seven to C. The start and goal are the same; in "
            "between, three tonics a major third apart, each led in by its own dominant."
        ) as vo:
            self.play(FadeIn(g[0]))
            vo.wait_until("a")
            self.play(FadeIn(g[1]), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("thirds")
        c = clip("thirds.two")
        gp = line_over([tuple(x) for x in d["lines"]["plain"]], d["plain"] * 2, width=11.4, height=1.5, color=GREY_A, lo=56, hi=86, size=13).move_to(UP * 1.4)
        gc = line_over([tuple(x) for x in d["lines"]["coltrane"]], d["coltrane"] * 2, width=11.4, height=1.5, color=TUNE, lo=56, hi=86, size=12).move_to(DOWN * 1.4)
        with self.voiceover(
            "Hear both, twice each, with the improviser's line on the piano: first the plain two-five-one, then Coltrane's "
            "substitute. The improviser aims at each new chord's guide tones, so it has to leap when the keys do."
        ):
            self.play(FadeIn(gp), FadeIn(gc))
        with self.listen(c) as snd:
            window(snd, r"plain, \ then Coltrane's cycle", detail=r"piano, \ string and cymbal models", corner=DL, tag_corner=DR)
            for g, k, col in ((gp, "plain", GREY_A), (gc, "coltrane", TUNE)):
                L = d["lines"][k]
                flash(snd, g.roll.notes, list(BL.swing_times([e for _, e in L], d["bpm"]) + d["starts"][k]), hot=WHITE, base=col)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def legacy(self):
        items = [
            (r"`Coltrane changes' became a standard tool of reharmonisation", WHITE),
            (r"the cycle was not new: \ Nicolas Slonimsky's \textit{Thesaurus of Scales and Melodic Patterns} \ (1947) \ lists such divisions", WHITE),
            (r"nor the harmony: \ Romantic composers moved between keys a third apart \ (Part 27)", WHITE),
            (r"what was new was playing through it, \ improvising, \ at speed", TUNE),
            (r"chapter 7: \ reharmonisation in general", GREY_A),
        ]
        rows_scene(self, r"a cycle with a history", items,
                   "Coltrane changes became a standard tool of reharmonisation. <bookmark mark='b'/> The cycle itself was not "
                   "new: Nicolas Slonimsky's Thesaurus of Scales and Melodic Patterns, of 1947, which Coltrane studied, lists "
                   "such equal divisions of the octave. <bookmark mark='c'/> Nor was the harmony: Romantic composers moved between "
                   "keys a third apart, as Part 27 heard. <bookmark mark='d'/> What was new was improvising through it, at speed. "
                   "<bookmark mark='e'/> Chapter seven turns to reharmonisation in general.", marks="bcde")
