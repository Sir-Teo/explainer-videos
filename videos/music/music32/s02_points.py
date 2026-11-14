from __future__ import annotations

import numpy as np

from videos.music.music32.common import *  # noqa: F403


class Points(SoundScene):
    def construct(self):
        chapter(self, 1, r"Chords as points", r"Where does a chord live?", extra=((2006, r"Tymoczko in \textit{Science}"),))
        self.plane()
        self.fold()
        self.why()
        self.history()

    # ------------------------------------------------------------------
    def plane(self):
        ax = Axes(x_range=[58, 74, 2], y_range=[58, 74, 2], x_length=5.6, y_length=5.6, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 16}).move_to(LEFT * 2.9 + DOWN * 0.3)
        grid = VGroup(*[Dot(ax.c2p(x, y), radius=0.025, color=DIM) for x in range(58, 75) for y in range(58, 75)])
        xl = label(r"voice 1 \ (key number)", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.3)
        yl = label(r"voice 2", font_size=18, color=GREY_A).next_to(ax, LEFT, buff=0.3).rotate(PI / 2)
        p = Dot(ax.c2p(60, 64), radius=0.1, color=TUNE)
        q = Dot(ax.c2p(64, 60), radius=0.1, color=BLUE)
        pl = label(r"(C4, \ E4)", font_size=18, color=TUNE).next_to(p, UL, buff=0.08)
        ql = label(r"(E4, \ C4)", font_size=18, color=BLUE).next_to(q, DR, buff=0.08)
        o = Dot(ax.c2p(72, 64), radius=0.1, color=EAR)
        ol = label(r"(C5, \ E4)", font_size=18, color=EAR).next_to(o, UP, buff=0.1)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"two voices: \ a point of the plane, \ one coordinate each", WHITE),
            (r"a voice leading: \ a path from point to point", WHITE),
            (r"but (C4, \ E4) and (E4, \ C4) are the same chord", BLUE),
            (r"and C5 with E4 is a C and an E too, \ an octave apart", EAR))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.0)).move_to(RIGHT * 3.4)
        with self.voiceover(
            "Write two voices as two numbers, the key number of each, and a chord becomes a point of the plane: C4 in the "
            "first voice and E4 in the second is this point. <bookmark mark='a'/> When the voices move, the point moves: a "
            "voice leading is a path. <bookmark mark='b'/> But the plane has too many points. E4 in the first voice and C4 "
            "in the second is a different point, yet the same chord. <bookmark mark='c'/> And if we care only which notes "
            "sound, not in which octave, then C5 with E4 is a C and an E as well."
        ) as vo:
            self.play(Create(ax), FadeIn(grid), FadeIn(xl), FadeIn(yl), FadeIn(p), FadeIn(pl), FadeIn(side[0]))
            vo.wait_until("a")
            path = Line(ax.c2p(60, 64), ax.c2p(60, 65), color=TUNE, stroke_width=4)
            self.play(FadeIn(side[1]), Create(path))
            vo.wait_until("b")
            self.play(FadeIn(q), FadeIn(ql), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(o), FadeIn(ol), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fold(self):
        ax = Axes(x_range=[0, 12, 2], y_range=[0, 12, 2], x_length=5.2, y_length=5.2, tips=False,
                  axis_config={"color": GREY_B, "include_numbers": True, "font_size": 16}).move_to(LEFT * 3.0 + DOWN * 0.3)
        sq = Polygon(ax.c2p(0, 0), ax.c2p(12, 0), ax.c2p(12, 12), ax.c2p(0, 12), color=GREY_B, stroke_width=2)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(12, 12), color=EAR, stroke_width=3)
        lower = Polygon(ax.c2p(0, 0), ax.c2p(12, 0), ax.c2p(12, 12), stroke_width=0, fill_color=BLACK, fill_opacity=0.75)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=TUNE if y > x else (EAR if x == y else BLUE)) for x in range(12) for y in range(12)])
        arrows = VGroup(Arrow(ax.c2p(-0.6, 3), ax.c2p(-0.6, 9), color=GREY_A, buff=0, stroke_width=3),
                        Arrow(ax.c2p(12.6, 3), ax.c2p(12.6, 9), color=GREY_A, buff=0, stroke_width=3))
        xl = label(r"voice 1, \ pitch class", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.3)
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"O, \ octaves: \ only pitch class counts; \ the plane wraps into a square whose edges are glued: \ a torus", WHITE),
            (r"P, \ permutations: \ (x, \ y) \ is (y, \ x): \ fold along the diagonal", EAR),
            (r"half the square is left, \ and its edges are glued with a twist", TUNE),
            (r"the diagonal itself, \ the unisons, \ becomes an edge: \ the space has a boundary", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        rows_.scale_to_fit_width(min(rows_.width, 6.1)).move_to(RIGHT * 3.5)
        with self.voiceover(
            "Two symmetries fold the plane. <bookmark mark='a'/> The first is the octave: keep only pitch classes and every "
            "coordinate lives on a circle of twelve semitones, so the plane becomes a square whose opposite edges are glued, "
            "a torus. <bookmark mark='b'/> The second is permutation: the point x, y is the same chord as y, x, so fold the "
            "square along its diagonal. <bookmark mark='c'/> Half the square is left, and when its edges are glued the "
            "gluing has a twist. <bookmark mark='d'/> The diagonal, where the two voices sound the same note, cannot be "
            "folded past: it becomes an edge. The next chapter shows the shape that results."
        ) as vo:
            self.play(Create(ax), FadeIn(sq), FadeIn(dots), FadeIn(xl), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(arrows))
            vo.wait_until("b")
            self.play(Create(diag), FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(FadeIn(lower), FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(diag.animate.set_stroke(width=7), FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why(self):
        items = [
            (r"in counterpoint the voices matter: \ Part 16 forbade them to cross", WHITE),
            (r"in harmony they do not: \ Part 13 named a chord by its notes, \ whoever sings them", WHITE),
            (r"the geometry keeps both: \ a path remembers the voices, \ a point forgets them", TUNE),
            (r"forgetting has a price: \ the space is curved, \ with edges and folds", WHITE),
            (r"and a reward: \ the same picture holds every chord of n notes, \ in any tuning", GREY_A),
        ]
        rows_scene(self, r"why fold at all?", items,
                   "Why fold at all? <bookmark mark='b'/> In counterpoint the voices matter: Part 16 forbade them to cross "
                   "carelessly. <bookmark mark='c'/> In harmony they do not: Part 13 named a chord by its notes, whoever "
                   "sings them. <bookmark mark='d'/> The geometry keeps both views: a path remembers which voice went where, "
                   "while a point forgets. <bookmark mark='e'/> Forgetting has a price, a space with edges and folds instead of "
                   "a flat plane. <bookmark mark='f'/> And a reward: one picture holds every chord of n notes, in any tuning, "
                   "including the notes between the piano's keys.", marks="cdef")

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Roeder \ (1984), \ Cohn \ (1990s): \ chords and voice leading on lattices and cycles", WHITE),
            (r"Callender \ (2004): \ continuous transformations between chords", WHITE),
            (r"Tymoczko \ (2006): \ the orbifolds; \ Callender, \ Quinn and Tymoczko \ (2008): \ the OPTIC family", TUNE),
            (r"the mathematics is older: \ quotient spaces and orbifolds \ (Thurston, \ 1970s)", WHITE),
            (r"what was new was the dictionary between musical words and geometric objects", GREY_A),
        ]
        rows_scene(self, r"a short history of chord space", items,
                   "The idea has a short history. <bookmark mark='b'/> John Roeder in the 1980s and Richard Cohn in the 1990s drew chords and voice leadings on lattices and cycles. <bookmark mark='c'/> Clifton Callender in 2004 described continuous transformations between chords. <bookmark mark='d'/> Tymoczko's paper of 2006 found the orbifolds, and the paper of 2008 with Callender and Quinn the whole family. <bookmark mark='e'/> The mathematics was older: quotient spaces and orbifolds, named by William Thurston in the 1970s. <bookmark mark='f'/> What was new was the dictionary between musical words and geometric objects.", marks="cdef")
