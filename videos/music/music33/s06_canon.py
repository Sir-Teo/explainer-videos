from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403


def tile_grid(n, A, B, width=11.0, row_h=0.22, colors=None):
    """A canon as a grid: one row per voice (an entry offset in B), a filled cell at every pulse the voice strikes."""
    colors = colors or [TUNE, BLUE, EAR, "#A3E635", "#F59E0B", "#22D3EE"]
    w = width / n
    g = VGroup()
    g.cells = []
    for j, b in enumerate(B):
        row = VGroup()
        for a in A:
            t = (a + b) % n
            r = Rectangle(width=w * 0.9, height=row_h * 0.8, stroke_width=0, fill_color=colors[j % len(colors)], fill_opacity=0.95)
            r.move_to([-width / 2 + (t + 0.5) * w, -j * row_h, 0])
            row.add(r)
        g.add(row)
        g.cells.append(row)
    frame = Rectangle(width=width, height=row_h * len(B), stroke_color=DIM, stroke_width=1).move_to(g.get_center())
    g.add(frame)
    return g


class Canon(SoundScene):
    def construct(self):
        chapter(self, 5, r"Tiling the line", r"Can a canon fill every moment exactly once?", extra=((1991, r"Vuza's canons"),))
        self.small()
        self.vuza()
        self.why72()
        self.search()
        self.hajos()
        self.composers()

    # ------------------------------------------------------------------
    def small(self):
        d = load("canon")
        s = d["small"]
        g = tile_grid(s["n"], s["A"], s["B"], width=8.0, row_h=0.6, colors=[TUNE, BLUE]).move_to(UP * 0.4)
        lab = VGroup(label(r"voice 1: \ 0 1 4 5", font_size=20, color=TUNE), label(r"voice 2: \ the same, \ 2 pulses later", font_size=20, color=BLUE)).arrange(DOWN, buff=0.3).next_to(g, LEFT, buff=0.4)
        cap = label(r"every one of the 8 pulses struck exactly once: \ A $\oplus$ B \ = \ the whole cycle", font_size=22, color=GREY_A).to_edge(DOWN, buff=1.1)
        head = label(r"a rhythmic tiling canon", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A canon in time. One voice plays a rhythm, strokes on pulses zero, one, four and five of an eight-pulse cycle. "
            "A second voice plays the same rhythm two pulses later. Together they strike every pulse of the cycle exactly "
            "once, no gaps and no collisions: the rhythm tiles the cycle. Mathematicians write it as a direct sum: the "
            "rhythm A plus the entries B is the whole cycle. Listen to the two voices, high and low."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(lab), FadeIn(cap))
        c = clip("canon.small")
        with self.listen(c) as snd:
            window(snd, r"a small canon", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            p = d["pulse"]
            for cc in range(2):
                for j, b in enumerate(s["B"]):
                    for i, a in enumerate(s["A"]):
                        t0 = (cc * s["n"] + a + b) * p
                        pulse(snd, g.cells[j][i], t0, t0 + p * 0.9, buff=0.03)
        with self.voiceover(
            "But this canon has a weakness. The rhythm, zero one four five, repeats itself every four pulses: it is "
            "periodic, really a two-stroke rhythm played twice. The question Dan Tudor Vuza asked in 1991 was whether a canon "
            "can tile the cycle when neither the rhythm nor the entries repeat in this way."
        ):
            self.wait(0.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vuza(self):
        d = load("canon")
        v = d["vuza"]
        c = clip("canon.vuza")
        g = tile_grid(v["n"], v["A"], v["B"], width=11.6, row_h=0.26).move_to(DOWN * 0.3)
        info = VGroup(label(r"rhythm A \ = \ \{0, \ 8, \ 16, \ 18, \ 26, \ 34\}: \ not periodic", font_size=20, color=TUNE),
                      label(r"entries B \ = \ \{0, \ 1, \ 5, \ 24, \ 25, \ 29, \ 30, \ 36, \ 49, \ 53, \ 60, \ 66\}: \ not periodic", font_size=20, color=BLUE),
                      label(rf"checked: \ every one of the 72 pulses struck exactly once", font_size=20, color=WHITE)).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        cap = label(rf"the search found {v['n_tilings']:,} ways to tile with this rhythm; \ {v['n_aperiodic']} of them have aperiodic entries", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "Here is such a canon, of period seventy-two, found for this film by a program that tries to cover the cycle with "
            "copies of a rhythm, backtracking when it gets stuck. The rhythm has six strokes and repeats at no shift; twelve "
            "voices enter at twelve offsets that also repeat at no shift. Every one of the seventy-two pulses is struck by "
            f"exactly one voice, and the program checks it. With this rhythm there are {say(v['n_tilings'])} tilings in all, "
            f"and {say(v['n_aperiodic'])} of them have entries that never repeat. Listen: twelve voices on twelve pitches, "
            "one note on every pulse."
        ):
            self.play(FadeIn(info), FadeIn(g), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a Vuza canon, \ period 72", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            vp = d["vpulse"]
            for j, b in enumerate(v["B"]):
                for i, a in enumerate(v["A"]):
                    t = ((a + b) % v["n"]) * vp
                    pulse(snd, g.cells[j][i], t, t + vp * 1.5, buff=0.02)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def why72(self):
        items = [
            (r"a canon with neither part periodic exists only in some cycles", WHITE),
            (r"the smallest is 72: \ every tiling of a shorter cycle has a periodic part", WHITE),
            (r"72 \ = \ 2 $\times$ 2 $\times$ 2 $\times$ 3 $\times$ 3: \ room for two independent periodicities to be broken", WHITE),
            (r"the next lengths: \ 108, \ 120, \ 144, \ 168, \ 180 ...", TUNE),
            (r"Vuza \ (1991), \ building on Haj\'os \ (1941) \ and de Bruijn \ (1950s)", GREY_A),
        ]
        rows_scene(self, r"why period 72?", items,
                   "Why seventy-two? <bookmark mark='b'/> Canons with neither part periodic exist only for some lengths of cycle. "
                   "<bookmark mark='c'/> The smallest is seventy-two: in every shorter cycle, one of the two parts of any tiling "
                   "must repeat. <bookmark mark='d'/> Seventy-two is two times two times two times three times three, enough "
                   "room for two separate periodicities to be broken at once. <bookmark mark='e'/> After it come one hundred and "
                   "eight, one hundred and twenty, one hundred and forty-four and more. <bookmark mark='f'/> Vuza's result of 1991 "
                   "rests on work by Hajós in the 1940s and de Bruijn in the 1950s, about factoring groups.", marks="cdef")

    # ------------------------------------------------------------------
    def hajos(self):
        items = [
            (r"Haj\'os \ (1941) \ proved Minkowski's conjecture on lattice tilings of space by cubes", WHITE),
            (r"his key step: \ when must a factoring of a finite group have a periodic factor?", WHITE),
            (r"the cyclic groups where it must are the `good' ones: \ every length below 72", WHITE),
            (r"a question from geometry became a question about canons, \ sixty years later", TUNE),
            (r"chapter 10: \ the link to an open conjecture about tiling and Fourier series", GREY_A),
        ]
        rows_scene(self, r"from cubes to canons", items,
                   "The mathematics came from geometry. <bookmark mark='b'/> In 1941 György Hajós proved a conjecture of "
                   "Minkowski about filling space with cubes. <bookmark mark='c'/> His key step asked when a factoring of a finite "
                   "group must have a periodic factor. <bookmark mark='d'/> The cyclic groups where it must are called good, and "
                   "every cycle shorter than seventy-two is good. <bookmark mark='e'/> A question about cubes became, half a "
                   "century later, a question about canons. <bookmark mark='f'/> The frontier chapter follows it to an open "
                   "conjecture.", marks="cdef")

    # ------------------------------------------------------------------
    def search(self):
        items = [
            (r"cover the 72 pulses with copies of the rhythm, \ one at a time", WHITE),
            (r"always cover the earliest pulse still empty: \ six ways to place a copy over it", WHITE),
            (r"if a copy would strike a pulse already struck, \ undo and try the next: \ backtracking", WHITE),
            (r"every complete cover is a canon; \ keep those whose entries repeat at no shift", TUNE),
            (r"exact cover: \ the same search solves Sudoku and packs polyominoes", GREY_A),
        ]
        rows_scene(self, r"how the canon was found", items,
                   "How did the program find it? <bookmark mark='b'/> It covers the seventy-two pulses with copies of the rhythm, one copy at a time. <bookmark mark='c'/> It always works on the earliest pulse still empty: there are only six ways to place a copy so that one of its strokes lands there. <bookmark mark='d'/> If a copy would strike a pulse already struck, it undoes the last choice and tries the next: backtracking. <bookmark mark='e'/> Every complete cover is a canon; the program keeps those whose entries repeat at no shift. <bookmark mark='f'/> The same exact-cover search solves Sudoku puzzles and packs polyominoes.", marks="cdef")

    # ------------------------------------------------------------------
    def composers(self):
        items = [
            (r"Messiaen wrote rhythmic canons and was fascinated by symmetric rhythms \ (Part 28)", WHITE),
            (r"Tom Johnson's \textit{Tilework} \ (2003): \ pieces built from tiling canons", WHITE),
            (r"Moreno Andreatta and the IRCAM group: \ tiling canons as compositional tools", WHITE),
            (r"a Vuza canon is dense: \ one note on every pulse, \ every voice audible only by register or timbre", TUNE),
            (r"the mathematics invites the music; \ the ear decides whether it works", GREY_A),
        ]
        rows_scene(self, r"composers and canons", items,
                   "Composers have used these canons. <bookmark mark='b'/> Messiaen wrote rhythmic canons and loved symmetric rhythms, as Part 28 showed. <bookmark mark='c'/> Tom Johnson's Tilework, of 2003, builds pieces from tiling canons. <bookmark mark='d'/> Moreno Andreatta and colleagues at IRCAM made tiling canons a compositional tool. <bookmark mark='e'/> A Vuza canon is dense: one note on every pulse, each voice heard only by its register or timbre. <bookmark mark='f'/> The mathematics invites the music; the ear decides whether it works.", marks="cdef")
