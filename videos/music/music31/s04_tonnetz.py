from __future__ import annotations

import numpy as np

from videos.music.music31.common import *  # noqa: F403


class Tonnetz(SoundScene):
    def construct(self):
        chapter(self, 3, r"The Tonnetz", r"Can every triad be drawn on one map?", extra=((1739, r"Euler's \textit{Tentamen}"),))
        self.lattice()
        self.moves()
        self.torus()
        self.spheres()
        self.walk()
        self.history()
        self.comma()
        self.keyboards()

    # ------------------------------------------------------------------
    def lattice(self):
        g = tonnetz()
        head = label(r"the Tonnetz: \ fifths to the right, \ major thirds up and to the right", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        cmaj = triangle(g, [(0, 0), (1, 0), (0, 1)], TUNE)
        cmin = triangle(g, [(0, 0), (1, 0), (1, -1)], BLUE) if (1, -1) in g.pos else None
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"each node a pitch class; \ neighbours a fifth, \ a major third or a minor third apart", WHITE),
            (r"a triangle pointing up: \ a major triad; \ pointing down: \ a minor triad", TUNE))]).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Euler drew the first version of this map in 1739. Each node is a pitch class. Moving right goes up a perfect "
            "fifth; moving up and to the right goes up a major third; and so moving up and to the left goes up a minor third. "
            "<bookmark mark='a'/> Every small triangle is a triad: those pointing up are major, like C, E, G here, and those "
            "pointing down are minor."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(rows_[0]))
            vo.wait_until("a")
            self.play(FadeIn(cmaj), FadeIn(rows_[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def moves(self):
        g = tonnetz()
        c = triangle(g, [(0, 0), (1, 0), (0, 1)], TUNE)
        # C at (0,0), G at (1,0), E at (0,1): the neighbours across each edge
        p = triangle(g, [(0, 0), (1, 0), (1, -1)], BLUE) if (1, -1) in g.pos else triangle(g, [(1, 0), (0, 1), (1, 1)], BLUE)
        lt = triangle(g, [(1, 0), (0, 1), (1, 1)], EAR)
        r = triangle(g, [(0, 0), (0, 1), (-1, 1)], GREY_A) if (-1, 1) in g.pos else None
        g2 = tonnetz()
        c = triangle(g2, [(1, 1), (2, 1), (1, 2)], TUNE)
        L_ = triangle(g2, [(2, 1), (1, 2), (2, 2)], EAR)
        P_ = triangle(g2, [(1, 1), (2, 1), (2, 0)], BLUE)
        R_ = triangle(g2, [(1, 1), (1, 2), (0, 2)], GREY_A)
        head = label(r"P, \ L and R: \ flip the triangle across one of its edges", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        key = VGroup(*[label(t, font_size=20, color=c_) for t, c_ in (
            (r"gold: \ a major triad", TUNE), (r"pink: \ L, \ across the edge of its third and fifth", EAR),
            (r"blue: \ P, \ across root and fifth", BLUE), (r"grey: \ R, \ across root and third", GREY_A))]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_corner(DR, buff=0.4)
        with self.voiceover(
            "On the map, the three moves become flips. <bookmark mark='a'/> A major triad shares an edge with three minor "
            "triads. Flip it across the edge of its third and fifth and you get L. <bookmark mark='b'/> Flip across the edge "
            "of its root and fifth, the horizontal one, and you get P. <bookmark mark='c'/> Flip across the edge of its root "
            "and third and you get R. Two notes stay, because the edge stays; the third note jumps to the other side."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g2), FadeIn(c), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(FadeIn(L_), FadeIn(key[1]))
            vo.wait_until("b")
            self.play(FadeIn(P_), FadeIn(key[2]))
            vo.wait_until("c")
            self.play(FadeIn(R_), FadeIn(key[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def torus(self):
        rows_ = text_rows([
            (r"going right twelve fifths returns to the same pitch class", WHITE),
            (r"going up three major thirds returns too: \ C, \ E, \ G$\sharp$, \ C", WHITE),
            (r"identify all equal pitch classes, including diagonal equivalents:\\a torus with 12 nodes and 24 triangles", TUNE),
            (r"12 pitch classes, \ 24 triangles: \ exactly the 24 major and minor triads", WHITE),
            (r"chapter two's distance is a walk across triangles on this torus", GREY_A),
        ], font_size=24)
        head = label(r"the map closes up", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "The map does not go on for ever. <bookmark mark='a'/> Twelve steps to the right, twelve fifths, bring you back to the same pitch class. <bookmark mark='b'/> Three steps up, three major thirds, C, E, G sharp, C, also bring you back. <bookmark mark='c'/> Identifying every lattice point with the same twelve-tone pitch class, including diagonal equivalences, gives a torus, the surface of a doughnut. The two periods alone would leave repeated pitch classes. <bookmark mark='d'/> On it there are twelve nodes and twenty-four triangles: exactly the twenty-four major and minor triads. <bookmark mark='e'/> Chapter two's distance is the number of triangles you cross on this surface."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows_[0]))
            for mark, r in zip("bcde", rows_[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Leonhard Euler, \ 1739: \ a lattice of fifths and thirds for just intonation \ (Part 6)", WHITE),
            (r"Arthur von Oettingen, \ Hugo Riemann \ (1866--1880s): \ the \textit{Tonnetz}, \ `tone network'", WHITE),
            (r"in just intonation the map does not close: \ four fifths are not a major third plus two octaves \ (the comma)", WHITE),
            (r"equal temperament closes it into a torus", TUNE),
            (r"Part 32 builds a larger geometry, \ for chords of any size", GREY_A),
        ]
        rows_scene(self, r"a history of the map", items,
                   "The map is old. <bookmark mark='b'/> Euler drew a lattice of fifths and thirds in 1739 to describe just "
                   "intonation, as Part 6 did. <bookmark mark='c'/> Arthur von Oettingen and Hugo Riemann developed it in the "
                   "nineteenth century as the Tonnetz, the tone network. <bookmark mark='d'/> In just intonation the map never "
                   "closes: four pure fifths overshoot two octaves and a pure third by a comma. <bookmark mark='e'/> Equal "
                   "temperament makes the comma vanish and closes the map into a torus. <bookmark mark='f'/> Part 32 builds a "
                   "larger geometry, for chords of any size.", marks="cdef")

    # ------------------------------------------------------------------
    def walk(self):
        d = load("walk")
        c = clip("walk.random")
        names = VGroup(*[label(tex_triad(n), font_size=30, color=TUNE if not n.endswith("m") else BLUE) for n in d["chain"]]).arrange(RIGHT, buff=0.5).move_to(UP * 0.8)
        word = VGroup(*[label(k, font_size=20, color=GREY_A).move_to((names[i].get_center() + names[i + 1].get_center()) / 2 + DOWN * 0.55) for i, k in enumerate(d["word"])])
        head = label(r"a random walk: \ eight moves, \ never the same twice running", font_size=25, color=GREY_A).to_edge(UP, buff=0.45)
        cap = label(rf"after eight steps the walk is {d['end_dist']} steps from home: \ random walks on the torus drift", font_size=21, color=GREY_A).to_edge(DOWN, buff=1.1)
        with self.voiceover(
            "Here is a walk on the torus chosen by chance: eight moves, each P, L or R, never the same one twice in a row, "
            "starting from C major. Every step is smooth, yet after eight of them the walk has wandered to D major, four "
            f"steps from home by the shortest route. Listen to how each chord follows naturally from the last, and how far "
            "the whole thing drifts."
        ):
            self.play(FadeIn(head), FadeIn(names), FadeIn(word), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a random walk", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for i in range(len(names)):
                pulse(snd, names[i], i * d["unit"], (i + 1) * d["unit"] - 0.05, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def keyboards(self):
        items = [
            (r"isomorphic keyboards: \ every chord shape the same in every key", WHITE),
            (r"the Wicki--Hayden layout \ (concertinas, \ 1896); \ the `harmonic table' of hexagonal pads", WHITE),
            (r"on a harmonic table a major triad is always the same triangle of three buttons", WHITE),
            (r"P, \ L and R become one finger moving to a neighbouring button", TUNE),
            (r"some electronic instruments are built on exactly this map", GREY_A),
        ]
        rows_scene(self, r"the Tonnetz under the fingers", items,
                   "The map has also been built into instruments. <bookmark mark='b'/> On an isomorphic keyboard every chord has the same shape in every key. <bookmark mark='c'/> The Wicki-Hayden layout, used on concertinas from the 1890s, is one; the harmonic table, a grid of hexagonal buttons, is another. <bookmark mark='d'/> On a harmonic table a major triad is always the same small triangle of three buttons, <bookmark mark='e'/> and P, L and R become a single finger moving to a neighbouring button. <bookmark mark='f'/> Several electronic instruments are laid out on exactly this map.", marks="cdef")

    # ------------------------------------------------------------------
    def spheres(self):
        d = load("spheres")
        ks = sorted(d["hist"], key=int)
        vals = [d["hist"][k] for k in ks]
        bars = columns(vals, ks, width=6.0, height=3.0, color=TUNE, fmt="{:.0f}", font_size=20, hot=(5,), hot_color=EAR).move_to(LEFT * 3.0 + DOWN * 0.4)
        xl = label(r"steps from C major", font_size=20, color=GREY_A).next_to(bars, DOWN, buff=0.4)
        side = VGroup()
        for k in ks:
            nm = r", \ ".join(tex_triad(n) for n in d["by"][k])
            side.add(label(rf"{k}: \ {nm}", font_size=19, color=EAR if k == "5" else WHITE))
        side.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.6)).move_to(RIGHT * 3.6 + DOWN * 0.2)
        head = label(r"how far is every triad from C major?", font_size=28, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "How far is each triad from C major? A breadth-first search across the triangles answers it. "
            "<bookmark mark='a'/> One step: C minor, E minor and A minor. Two steps: six triads, the major chords a third "
            "away and the neighbouring fifths, G and F. Three steps: eight minor triads. Four: five major triads, including "
            "F sharp and the remote B and C sharp. <bookmark mark='b'/> And five steps: only B flat minor, the single "
            "farthest triad on the torus, the one chapter two found. On average a triad is two and two thirds steps from C."
        ) as vo:
            self.play(FadeIn(head), FadeIn(bars), FadeIn(xl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in side[1:5]], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(side[5]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def comma(self):
        d = load("comma")
        c = clip("comma.two")
        rows_ = VGroup(*[label(s, font_size=23, color=c_) for s, c_ in (
            (rf"a pure major third, \ 5:4: \ {d['just_cents']:.1f} cents above C", TUNE),
            (rf"four pure fifths, \ less two octaves: \ {d['fifths_cents']:.1f} cents", BLUE),
            (rf"the gap: \ {d['comma_cents']:.1f} cents, \ the syntonic comma", EAR),
            (r"in just intonation the Tonnetz is an infinite plane, \ not a torus", GREY_A))]).arrange(DOWN, buff=0.4)
        rows_.move_to(UP * 0.4)
        head = label(r"why Euler's map does not close", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Hear the comma that keeps Euler's map open. Go up a major third from C on the lattice, and the E is a pure "
            f"third, five to four, {say(round(d['just_cents']))} cents above C. Go four fifths to the right instead, pure "
            f"fifths, and come down two octaves: that E is {say(round(d['fifths_cents']))} cents up. The two Es differ by "
            f"{say(d['comma_cents'], 1)} cents, the syntonic comma. First C with each E; then the two Es alone, "
            "alternating."
        ):
            self.play(FadeIn(head), FadeIn(rows_[0]), FadeIn(rows_[1]), FadeIn(rows_[2]))
        with self.listen(c) as snd:
            window(snd, r"pure third, \ then four fifths", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            pulse(snd, rows_[0], 0.0, 2.5, buff=0.08)
            pulse(snd, rows_[1], 2.6, 5.5, buff=0.08)
            pulse(snd, rows_[2], 5.6, c.duration, buff=0.08)
        with self.voiceover(
            'In just intonation those are different notes, so the lattice never wraps round: it is an infinite plane. Twelve-tone equal temperament identifies both routes with the same E. Identifying all equivalent pitch classes gives the finite torus used here; other finite temperaments can give other quotients.'
        ):
            self.play(FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()
