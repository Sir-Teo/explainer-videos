from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403

NAMES3 = {(0, 4, 8): "augmented", (0, 3, 7): "major and minor", (0, 3, 6): "diminished", (0, 2, 7): "suspended", (0, 1, 2): "cluster",
          (0, 2, 4): "whole tones", (0, 2, 6): "", (0, 1, 6): "", (0, 1, 3): "", (0, 1, 4): "", (0, 1, 5): "", (0, 2, 5): ""}


def tri_frame(scale=3.0, center=ORIGIN):
    V = [np.array([0.0, 1.0, 0]), np.array([-np.sqrt(3) / 2, -0.5, 0]), np.array([np.sqrt(3) / 2, -0.5, 0])]
    pts = [center + scale * v for v in V]
    g = VGroup(Polygon(*pts, color=GREY_B, stroke_width=2))
    g.scale_ = scale
    g.center_ = center

    def p(x, y):
        return center + scale * np.array([x, y, 0])

    g.p = p
    return g


class Triangle(SoundScene):
    def construct(self):
        chapter(self, 3, r"Three notes: \ a triangle in a prism", r"Where do the triads live?", extra=((2008, r"Callender, \ Quinn \& Tymoczko"),))
        self.shapes()
        self.walk()
        self.glide()
        self.prism()
        self.neighbours()
        self.tetra()

    # ------------------------------------------------------------------
    def shapes(self):
        d = load("triangle")
        g = tri_frame(scale=3.1, center=LEFT * 2.6 + DOWN * 0.5)
        dots = VGroup()
        for pt in d["points"]:
            e = pt["even"]
            col = interpolate_color(ManimColor(TUNE), ManimColor(DIM), min(e / 6.0, 1.0))
            dots.add(Dot(g.p(pt["x"], pt["y"]), radius=0.055, color=col))
        def at(steps):
            for pt in d["points"]:
                if pt["steps"] == list(steps):
                    return g.p(pt["x"], pt["y"])
        marks = VGroup(
            label(r"augmented", font_size=18, color=EAR).next_to(at((4, 4, 4)), UP, buff=0.12),
            label(r"C E G", font_size=16, color=TUNE).next_to(at((4, 3, 5)), DOWN, buff=0.1),
            label(r"C E$\flat$ G", font_size=16, color=BLUE).next_to(at((3, 4, 5)), LEFT, buff=0.1),
            label(r"triple unisons", font_size=16, color=GREY_A).next_to(at((12, 0, 0)), UP, buff=0.1))
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"a three-note chord's shape: \ its three steps round the octave, \ summing to 12", WHITE),
            (r"C E G: \ steps 4, \ 3, \ 5; \ C E$\flat$ G: \ 3, \ 4, \ 5", TUNE),
            (r"the centre, \ 4, \ 4, \ 4: \ the augmented triad, \ perfectly even", EAR),
            (r"the corners: \ all 12 in one step: \ three voices on one note", GREY_A),
            (r"major and minor triads sit close to the centre, \ but not on it", WHITE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.6)).move_to(RIGHT * 3.6)
        with self.voiceover(
            "With three notes, forget transposition for a moment and keep only a chord's shape: the three steps that go "
            "round the octave, from note to note and back to the first, which always add up to twelve. <bookmark mark='a'/> "
            "C major's steps are four, three and five; C minor's are three, four and five. <bookmark mark='b'/> Every shape "
            "is a point of a triangle. At the centre, four, four, four: the augmented triad, perfectly even. "
            "<bookmark mark='c'/> At the corners, all twelve in one step: three voices on a single note. "
            "<bookmark mark='d'/> Major and minor triads sit close to the centre, but not on it. The brighter a dot, the more "
            "even the chord."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dots), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(marks[1]), FadeIn(marks[2]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(marks[0]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(marks[3]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def walk(self):
        d = load("triangle")
        c = clip("triangle.walk")
        g = tri_frame(scale=2.8, center=LEFT * 2.8 + DOWN * 0.4)
        base = VGroup(*[Dot(g.p(pt["x"], pt["y"]), radius=0.04, color=DIM) for pt in d["points"]])
        pts = [g.p(x, y) for x, y in d["walk_xy"]]
        wd = VGroup(*[Dot(p, radius=0.11, color=TUNE) for p in pts])
        path = VMobject(color=TUNE, stroke_width=3).set_points_as_corners(pts)
        names = [r"C C$\sharp$ D", r"C D E", r"C E$\flat$ G$\flat$", r"C E G", r"C E G$\sharp$"]
        rows_ = VGroup(*[VGroup(label(n, font_size=22, color=WHITE), label(k, font_size=18, color=GREY_A),
                                label(rf"{e:.2f}", font_size=20, color=TUNE)).arrange(RIGHT, buff=0.3)
                         for n, k, e in zip(names, d["names"], d["walk_even"])]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        rows_.move_to(RIGHT * 3.6 + DOWN * 0.2)
        hd = label(r"distance from the nearest even chord", font_size=18, color=GREY_A).next_to(rows_, UP, buff=0.35)
        head = label(r"from a corner to the centre", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Walk from near a corner to the centre and listen. A cluster, C, C sharp, D; then whole tones, C, D, E; the "
            "diminished triad; the major triad; and the augmented triad at the centre. Beside each, its distance from the "
            "nearest perfectly even chord, in semitones: four and a quarter for the cluster, falling to zero. The sound opens "
            "out as the chord spreads."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(base), FadeIn(path), FadeIn(wd), FadeIn(hd), FadeIn(rows_))
        with self.listen(c) as snd:
            window(snd, r"cluster to augmented", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i in range(5):
                pulse(snd, wd[i], i * d["unit"], (i + 1) * d["unit"] - 0.1, buff=0.06)
                pulse(snd, rows_[i], i * d["unit"], (i + 1) * d["unit"] - 0.1, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prism(self):
        items = [
            (r"put transposition back: \ every three-note chord is a point of a prism", WHITE),
            (r"along the prism: \ the chord's sum, \ transposing it; \ across: \ its shape, \ the triangle", WHITE),
            (r"the ends are glued with a third of a turn: \ twelve more semitones in the sum, \ the triangle turned", WHITE),
            (r"the augmented triads run straight down the middle; \ major and minor triads coil round them", TUNE),
            (r"a short voice leading between triads: \ a short path between neighbouring coils", GREY_A),
        ]
        rows_scene(self, r"the whole space: \ a twisted prism", items,
                   "Put transposition back and the whole space of three-note chords appears. <bookmark mark='b'/> It is a prism: "
                   "along it runs the sum of the chord's notes, which transposition changes; across it lies the triangle of "
                   "shapes. <bookmark mark='c'/> Its two ends are glued with a third of a turn: travel the length of the prism, adding "
                   "twelve semitones to the sum, and you are back among the same chords with the triangle turned. "
                   "<bookmark mark='d'/> The four augmented triads run straight down the middle, and the twenty-four major and "
                   "minor triads coil round them. <bookmark mark='e'/> A small voice leading between two triads is a short step "
                   "between neighbouring points on that coil.", marks="bcde")

    # ------------------------------------------------------------------
    def neighbours(self):
        d = load("vlsize")
        tri = d["triads"]
        order = sorted(tri, key=lambda k: (tri[k], k))
        bars = columns([tri[k] for k in order], [k.replace("b", r"$\flat$").replace("#", r"$\sharp$") for k in order], width=11.6, height=2.6,
                       color=TUNE, fmt="{:.0f}", font_size=14).move_to(DOWN * 0.6)
        head = label(r"how far is each triad from C major? \ semitones of the smallest voice leading", font_size=24, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"C minor and E minor: \ 1; \ five triads at 2; \ D, \ F$\sharp$ and B$\flat$ major: \ 6, \ the far side of the coil", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The coil can be measured. For each of the twenty-four triads, the smallest number of semitones C major's three "
            "voices must move to reach it. C minor and E minor are one semitone away; five triads are two away, among them A "
            "minor, E major and A flat major. The farthest, six semitones, are D, F sharp and B flat major: the far side of "
            "the coil. Part 31 counted P, L and R moves; this counts semitones, and the two rankings mostly agree."
        ):
            self.play(FadeIn(head), FadeIn(bars), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def glide(self):
        d = load("neutral")
        c = clip("neutral.glide")
        names = [r"C E G", r"E $-\tfrac14$", r"E $-\tfrac12$: \ neutral", r"E $-\tfrac34$", r"C E$\flat$ G"]
        cells = VGroup(*[VGroup(label(n, font_size=22, color=TUNE if i in (0, 4) else EAR), label(rf"{e:.2f}", font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2)
                         for i, (n, e) in enumerate(zip(names, d["even"]))]).arrange(RIGHT, buff=0.7).move_to(UP * 0.3)
        lab = label(r"distance from even", font_size=18, color=GREY_A).next_to(cells, LEFT, buff=0.3).shift(DOWN * 0.3)
        head = label(r"the space is continuous: \ from major to minor by quarters of a semitone", font_size=25, color=GREY_A).to_edge(UP, buff=0.4)
        cap = label(r"halfway is the neutral triad, \ heard in Arabic and Persian music \ (Part 35): \ the most even of the five", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Nothing in the geometry needs the piano's twelve keys. The space is continuous, and the chords between the keys "
            "are points too. Slide C major's third down a quarter of a semitone at a time until it becomes C minor. Halfway is "
            "the neutral triad, with a third exactly between major and minor, a sound at home in Arabic and Persian music, "
            "as Part 35 will show. On the triangle it lies on the straight line between major and minor, and it is the most "
            "even of the five. Listen to the third sink."
        ):
            self.play(FadeIn(head), FadeIn(cells), FadeIn(lab), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"major to minor, \ by quarters", detail=r"Part 7's piano, \ retuned", corner=DL, tag_corner=DR)
            for i in range(5):
                pulse(snd, cells[i], i * d["unit"], (i + 1) * d["unit"] - 0.1, buff=0.08)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tetra(self):
        items = [
            (r"four-note chords: \ the cross-section is a tetrahedron, \ the space a twisted prism over it", WHITE),
            (r"at the centre: \ the diminished seventh, \ perfectly even", WHITE),
            (r"close around it: \ the dominant seventh, \ the half-diminished; \ a little further, \ the minor seventh", TUNE),
            (r"the first two are a single semitone from a diminished seventh: \ the trapdoor of Part 19", WHITE),
            (r"in general: \ n notes, \ an (n--1)-simplex, \ the perfectly even chord at its centre", GREY_A),
        ]
        rows_scene(self, r"four notes: a tetrahedron", items,
                   "One more dimension. <bookmark mark='b'/> For four-note chords the cross-section is a tetrahedron, and the whole space a twisted prism over it. <bookmark mark='c'/> At the centre sits the diminished seventh, perfectly even. <bookmark mark='d'/> Close around it: the dominant seventh and the half-diminished seventh, with the minor seventh a little further out, the chords of tonal harmony and jazz. <bookmark mark='e'/> The first two are each one semitone from a diminished seventh, which is why Part 19's diminished seventh worked as a trapdoor into so many keys. <bookmark mark='f'/> In general, chords of n notes have a simplex for a cross-section, with the perfectly even chord at its centre.", marks="cdef")
