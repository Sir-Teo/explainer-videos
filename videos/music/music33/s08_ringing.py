from __future__ import annotations

import numpy as np

from videos.music.music33.common import *  # noqa: F403

BELL_COL = {1: TUNE, 2: BLUE, 3: EAR, 4: "#A3E635"}


def rows_grid(rows, cell=0.32, line_bell=1, size=16):
    g = VGroup()
    g.rows = []
    for i, r in enumerate(rows):
        row = VGroup(*[label(str(b), font_size=size, color=BELL_COL[b] if b == line_bell else GREY_A).move_to([j * cell, -i * cell * 0.9, 0]) for j, b in enumerate(r)])
        g.add(row)
        g.rows.append(row)
    return g


class Ringing(SoundScene):
    def construct(self):
        chapter(self, 7, r"Change ringing", r"Can four bells ring every order without repeating?", extra=((1668, r"\textit{Tintinnalogia}"),))
        self.hunt()
        self.six()
        self.bob()
        self.groups()

    # ------------------------------------------------------------------
    def hunt(self):
        d = load("ringing")
        g = rows_grid(d["hunt"], cell=0.5, size=24).move_to(LEFT * 3.2 + DOWN * 0.1)
        path = VMobject(color=TUNE, stroke_width=3).set_points_as_corners([g.rows[i][r.index(1)].get_center() for i, r in enumerate(d["hunt"])])
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"English tower bells swing full circle: \ each can only move one place per change", WHITE),
            (r"a change: \ swap neighbouring bells in the order of striking", WHITE),
            (r"plain hunt: \ swap every pair, \ then every inner pair, \ alternately", WHITE),
            (r"each bell weaves from front to back and back: \ the gold line is bell 1", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.0)).move_to(RIGHT * 3.2)
        head = label(r"plain hunt on four bells", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "In seventeenth-century England, ringers found a way to make music from heavy church bells that swing full circle "
            "and cannot be hurried. <bookmark mark='a'/> A bell can only move one place earlier or later in the order of "
            "striking from one round to the next, so each change swaps neighbours. <bookmark mark='b'/> The simplest pattern "
            "is plain hunt: swap every pair, then every inner pair, and repeat. <bookmark mark='c'/> Each bell weaves from "
            "the front to the back and back again; the gold line follows bell one. After eight changes the bells are back in "
            "rounds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(side[0]))
            for mark, r in zip("abc", side[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
            self.play(Create(path))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bob(self):
        d = load("ringing")
        c = clip("ringing.bob")
        rows = d["bob"]
        cols = VGroup()
        for k in range(3):
            part = rows[8 * k: 8 * k + 9]
            gg = rows_grid(part, cell=0.3, size=15)
            cols.add(gg)
        cols.arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to(LEFT * 1.6 + DOWN * 0.2)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"Plain Bob Minimus: \ plain hunt, \ but every eighth change the bells in the first two places hold", WHITE),
            (rf"three leads of eight: \ {d['distinct']} different rows, \ then rounds again", TUNE),
            (r"every one of the 4! \ = \ 24 orders of four bells, \ each exactly once: \ an `extent'", WHITE))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 4.4)).move_to(RIGHT * 4.4)
        head = label(r"every order of four bells, \ once", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Plain hunt alone repeats after eight rows. Plain Bob Minimus changes one step: at the end of each lead of eight, "
            "the first two bells hold their places while the others swap. <bookmark mark='a'/> Three leads give twenty-four "
            "rows, and then the bells come back to rounds. <bookmark mark='b'/> The program checks that the twenty-four rows "
            "are all different: every one of the twenty-four orders of four bells, each exactly once. Ringers call it an "
            "extent. Listen to it on four bells tuned E, D, C and G."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols), FadeIn(side[0]))
            for mark, r in zip("ab", side[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        flat = [row for gg in cols for row in gg.rows]
        idx = [r for k in range(3) for r in range(8 * k, 8 * k + 9)]
        with self.listen(c) as snd:
            window(snd, r"Plain Bob Minimus", detail=r"Part 9's bells", corner=DL, tag_corner=DR)
            st = d["stroke"]
            t = 0.0
            seen = set()
            for i in range(len(rows)):
                pos = [j for j, x in enumerate(idx) if x == i]
                for j in pos:
                    pulse(snd, flat[j], t, t + 4 * st - 0.05, buff=0.03)
                t += 4 * st + (st if i % 2 == 1 else 0.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def groups(self):
        items = [
            (r"the orders of n bells are the permutations of n things: \ the symmetric group, \ n! of them", WHITE),
            (r"a method is a walk on its Cayley graph that visits every element once: \ a Hamiltonian cycle", WHITE),
            (r"Fabian Stedman's \textit{Campanalogia} \ (1677) \ worked with these structures by hand", WHITE),
            (r"ringers used cosets of subgroups before group theory had a name", TUNE),
            (r"an extent on eight bells: \ 40,320 changes, \ about 18 hours of ringing", GREY_A),
        ]
        rows_scene(self, r"bells and groups", items,
                   "Mathematicians later recognised what the ringers were doing. <bookmark mark='b'/> The orders of n bells are "
                   "the permutations of n things, the symmetric group, with n factorial elements. <bookmark mark='c'/> A method "
                   "is a walk on the group's Cayley graph that visits every element once, a Hamiltonian cycle, like Part 31's "
                   "tours of the triads. <bookmark mark='d'/> Fabian Stedman's Campanalogia of 1677 worked with these structures "
                   "by hand, <bookmark mark='e'/> using what would later be called cosets of subgroups, long before group theory "
                   "had a name. <bookmark mark='f'/> On eight bells an extent has forty thousand three hundred and twenty changes, "
                   "about eighteen hours of continuous ringing.", marks="cdef")

    # ------------------------------------------------------------------
    def six(self):
        d = load("hunt6")
        c = clip("hunt6.hunt")
        g = rows_grid(d["rows"] + [d["rows"][0]], cell=0.42, size=20).move_to(LEFT * 2.8 + DOWN * 0.3)
        side = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"six bells: \ the same rule, \ 12 changes before rounds return", WHITE),
            (r"bell 1, \ in gold, \ hunts down to last place and back up", TUNE),
            (r"every bell moves at most one place per change", WHITE),
            (r"12 rows of the 720 possible: \ methods must do much more", GREY_A))]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 5.4)).move_to(RIGHT * 3.6)
        head = label(r"plain hunt on six bells", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Six bells hunt by the same rule. <bookmark mark='a'/> Twelve changes and the bells are back in rounds. "
            "<bookmark mark='b'/> Each bell, like bell one in gold, works its way from the front to the back and up again. "
            "<bookmark mark='c'/> No bell ever moves more than one place at a change. <bookmark mark='d'/> But twelve rows are "
            "a tiny fraction of the seven hundred and twenty orders of six bells, and methods exist to reach them all. Listen "
            "to the plain hunt first."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(side[0]))
            for mark, r in zip("abcd", side[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        with self.listen(c) as snd:
            window(snd, r"plain hunt on six", detail=r"Part 9's bells", corner=DL, tag_corner=DR)
            st = d["stroke"]
            t = 0.0
            for i in range(len(d["rows"])):
                pulse(snd, g.rows[i], t, t + 6 * st - 0.05, buff=0.03)
                t += 6 * st + (st if i % 2 == 1 else 0.0)
        self.wait(0.3)
        self.clear_scene()
