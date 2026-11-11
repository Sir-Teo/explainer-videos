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
            (r"Tetris", 'known pieces: can you clear \\\\ at least $k$ rows? \\\\ Demaine, Hohenberger, \\\\ Liben-Nowell (2003)'),
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
            "Hardness appears in many generalized decision problems. <bookmark mark='a'/> Offline Tetris asks whether a specified board and known piece sequence can achieve a stated objective, such as enough cleared rows, under the chosen move rules. <bookmark mark='b'/> Minesweeper consistency asks whether a finite clue layout has a compatible mine placement. <bookmark mark='c'/> Generalized Sudoku completion lets board dimensions grow; a fixed nine-by-nine puzzle is a finite case. <bookmark mark='d'/> The folding example concerns a specified lattice hydrophobic-polar model and energy threshold, not unrestricted physical protein behaviour. <bookmark mark='e'/> Each named decision variant has a polynomially checkable witness and an appropriate hardness reduction. <bookmark mark='f'/> Different rules or objectives may change the classification. Long two-player games introduce another set of questions, considered in the space chapter."
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
            label('packing: first-fit decreasing uses at most $11\\,\\mathrm{OPT}/9+2/3$ bins (one-dimensional model)', font_size=21, color=WHITE),
            label(r"\textbf{dependency resolution} \ (``install these packages'') \ is NP-complete \ (Mancinelli et "
                  r"al., 2006)", font_size=21, color=HEAD),
            label('package managers differ: SAT, incompatibility learning, or backtracking (Part 41)', font_size=21,
                  color=DATA),
            label(r"\textbf{configuration}, \ routing, \ register allocation \ (Part 13: \ graph colouring)",
                  font_size=21, color=WHITE),
            label('NP-complete: a polynomial-time general algorithm would imply P = NP; many real instances are easy', font_size=22, color=YES),
            label(r"the playbook: \ exact solver for small or structured inputs, \ approximation \ (Part 23), \ or "
                  r"a heuristic with a bound", font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(head, DOWN, buff=0.45)
        fit_right(rows)
        if rows.get_left()[0] < -6.9:
            rows.width = 13.6
            rows.next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "Engineers meet these problems in general-purpose forms. <bookmark mark='a'/> Scheduling models often lead to integer programming or constraint programming. <bookmark mark='b'/> In one-dimensional bin packing, first-fit decreasing has an eleven-ninths asymptotic guarantee with an additive constant; it is not a pure eleven-ninths bound for every small instance. <bookmark mark='c'/> Expressive dependency constraints can make package installation NP-complete. <bookmark mark='d'/> Actual package managers use different techniques, including SAT, incompatibility learning and backtracking; PubGrub is not the algorithm of every manager. <bookmark mark='e'/> Configuration and register allocation also produce hard general models. <bookmark mark='f'/> NP-completeness describes worst-case reductions. A polynomial-time algorithm for all instances would imply P equals NP; many real instances remain easy. <bookmark mark='g'/> Match the model to the task, then consider exact solvers, structure, approximation guarantees or explicitly limited heuristics."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdefg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
