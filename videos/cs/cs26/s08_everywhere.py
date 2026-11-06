from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (BG, CODE, CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, mono)


def tetromino(cells, color, s=0.28):
    return VGroup(*[Square(side_length=s, stroke_color=BG, stroke_width=1.5, fill_color=color, fill_opacity=0.9)
                    .move_to([x * s, -y * s, 0]) for x, y in cells])


class Everywhere(VoiceoverScene):
    def construct(self):
        self.card()
        self.games()
        self.work()

    def card(self):
        card = chapter_card(7, r"NP-completeness everywhere", r"Where do NP-complete problems turn up?",
                            lit=(1979, 2003), extra=((1979, r"Garey and Johnson"), (2003, r"Tetris")), part=PART)
        with self.voiceover("Chapter seven. NP-completeness everywhere."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def games(self):
        head = label(r"Puzzles and games", font_size=34).to_edge(UP, buff=0.3)
        pics = [
            VGroup(tetromino([(0, 0), (1, 0), (2, 0), (1, 1)], LAM), tetromino([(0, 0), (0, 1), (1, 1), (1, 2)], NO)
                   .shift(RIGHT * 1.0), tetromino([(0, 0), (1, 0), (2, 0), (3, 0)], DATA).shift(DOWN * 0.7)),
            VGroup(*[VGroup(Square(side_length=0.34, stroke_color=GREY_B, stroke_width=1, fill_color=GREY_D
                                   if t == "#" else BG, fill_opacity=1).move_to([x * 0.34, -y * 0.34, 0]),
                            mono(t if t not in "#." else " ", 16, HEAD).move_to([x * 0.34, -y * 0.34, 0]))
                     for y, row in enumerate(["1##", "2#.", "1.."]) for x, t in enumerate(row)]),
            VGroup(*[Square(side_length=0.22, stroke_color=GREY_B, stroke_width=1 if (x % 3 and y % 3) else 2)
                     .move_to([x * 0.22, -y * 0.22, 0]) for x in range(9) for y in range(9)]),
            VGroup(*[Dot([np.cos(t) * 0.6, np.sin(t) * 0.45, 0], radius=0.07, color=HEAD if k % 2 else DATA)
                     for k, t in enumerate(np.linspace(0, 2 * PI, 9)[:-1])]),
        ]
        items = [
            (r"Tetris", r"given the pieces in advance, \\ can you clear the board? \\ Demaine, Hohenberger, \\ "
                        r"Liben-Nowell \ (2003)"),
            (r"Minesweeper", r"is this board consistent? \\ Kaye \ (2000)"),
            (r"Sudoku, $n^2 \times n^2$", r"can this grid be completed? \\ Yato and Seta \ (2003)"),
            (r"protein folding", r"lowest-energy fold, \\ HP model: \ Berger and \\ Leighton \ (1998)"),
        ]
        cards = VGroup()
        for pic, (t, d) in zip(pics, items):
            box_ = RoundedRectangle(width=3.0, height=3.4, corner_radius=0.12, stroke_color=GREY_D, fill_color=BG,
                                    fill_opacity=1)
            pic.move_to(box_.get_center() + UP * 0.75)
            if pic.height > 1.3:
                pic.height = 1.3
            tt = label(t, font_size=21, color=HEAD).move_to(box_.get_center() + DOWN * 0.25)
            dd = label(d, font_size=16, color=GREY_A).next_to(tt, DOWN, buff=0.12)
            cards.add(VGroup(box_, pic, tt, dd))
        cards.arrange(RIGHT, buff=0.25).next_to(head, DOWN, buff=0.4)
        notes = VGroup(
            label(r"each is in NP: \ a solution is easy to check", font_size=21, color=YES),
            label(r"each is NP-complete: \ a reduction builds gadgets out of pieces, \ mines or cells", font_size=21,
                  color=WHITE),
            label(r"games with two players and long play are harder still: \ chapter 10", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).next_to(cards, DOWN, buff=0.4)
        with self.voiceover(
            "NP-completeness turns up in unexpected places. <bookmark mark='a'/> In 2003 Erik Demaine, Susan "
            "Hohenberger and David Liben-Nowell proved that Tetris is NP-complete: knowing every piece in advance, "
            "can you clear the board? <bookmark mark='b'/> Richard Kaye showed in 2000 that deciding whether a "
            "Minesweeper board is consistent is NP-complete. <bookmark mark='c'/> Sudoku on an n squared grid is "
            "NP-complete, by Takayuki Yato and Takahiro Seta. <bookmark mark='d'/> So is finding the lowest-energy "
            "fold of a protein in the simplest lattice model. <bookmark mark='e'/> Each is in NP, because a solution "
            "is easy to check. Each is NP-complete because someone built gadgets, out of falling pieces, mines or "
            "cells, that simulate a formula. <bookmark mark='f'/> Two-player games with long play are harder still, "
            "as chapter ten shows."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            for mk, n_ in zip("ef", [VGroup(notes[0], notes[1]), notes[2]]):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()

    def work(self):
        head = label(r"At work: \ recognize it, \ then don't despair", font_size=32).to_edge(UP, buff=0.35)
        rows = VGroup(
            label(r"\textbf{scheduling} \ (exams, \ shifts, \ jobs on machines) \ $\to$ \ integer programming \ "
                  r"(Part 23), \ constraint solvers", font_size=21, color=WHITE),
            label(r"\textbf{packing} \ (bins, \ containers, \ VMs on hosts) \ $\to$ \ first-fit decreasing is "
                  r"within about $11/9$ of optimal", font_size=21, color=WHITE),
            label(r"\textbf{dependency resolution} \ (``install these packages'') \ is NP-complete \ (Mancinelli et "
                  r"al., 2006)", font_size=21, color=HEAD),
            label(r"$\to$ \ apt, \ pip, \ cargo and conda use SAT-style solvers \ (PubGrub; \ Part 41)", font_size=21,
                  color=DATA),
            label(r"\textbf{configuration}, \ routing, \ register allocation \ (Part 13: \ graph colouring)",
                  font_size=21, color=WHITE),
            label(r"NP-complete means \textbf{worst case} has no known fast algorithm: \ real instances are often "
                  r"easy", font_size=22, color=YES),
            label(r"the playbook: \ exact solver for small or structured inputs, \ approximation \ (Part 23), \ or "
                  r"a heuristic with a bound", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.45)
        fit_right(rows)
        if rows.get_left()[0] < -6.9:
            rows.width = 13.6
            rows.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Engineers meet NP-hard problems every week. <bookmark mark='a'/> Scheduling exams, shifts or jobs on "
            "machines. <bookmark mark='b'/> Packing items into bins, containers, or virtual machines onto servers. "
            "<bookmark mark='c'/> Even installing software: deciding whether a set of packages with version "
            "constraints can be installed together is NP-complete, as researchers studying Debian showed in 2006. "
            "<bookmark mark='d'/> That is why modern package managers resolve dependencies with SAT-style solvers; "
            "Part 41 builds one. <bookmark mark='e'/> Register allocation, back in Part 13, was graph colouring. "
            "<bookmark mark='f'/> NP-completeness is a statement about the worst case. The instances that arise in "
            "practice are often easy. <bookmark mark='g'/> The playbook: an exact solver when inputs are small or "
            "structured, an approximation algorithm with a guarantee, or a heuristic whose results you can bound."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdefg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
