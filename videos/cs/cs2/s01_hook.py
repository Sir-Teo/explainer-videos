from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import (COST, CTRL, DATA, HEAD, HIST, NO, PART, YES, cell_center, fmt, live_int, load, say,
                                  tile_board)


class Hook(VoiceoverScene):
    def construct(self):
        self.craze()
        self.slide()
        self.argument()
        self.computed()
        self.plan()

    # ------------------------------------------------------------------
    def craze(self):
        loyd = list(range(1, 14)) + [15, 14, 0]
        board = tile_board(loyd, 4, cell=1.15, font_size=46, hot=(14, 15)).move_to(RIGHT * 3.0 + DOWN * 0.2)
        hc = history_card(1880, r"the ``15 puzzle'' craze", r"fifteen numbered tiles in a box of sixteen squares; \ "
                          r"slide them, \ one at a time, \ into the empty square", width=5.4, font_size=24)
        hc.to_corner(UL, buff=0.5)
        ask = label(r"from here, \ slide back to \\ 1, 2, 3, \dots, 14, 15 \ in order?", font_size=30, color=HEAD)
        ask.next_to(hc, DOWN, buff=0.6).align_to(hc, LEFT)
        prize = label(r"\$1{,}000 \ for a solution", font_size=34, color=COST).next_to(ask, DOWN, buff=0.5).align_to(
            ask, LEFT)
        src = note(r"the prize as Sam Loyd later told it; \ the craze itself began in New England, 1879--80",
                   font_size=20).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In the winter of 1880, half of America and much of Europe was pushing little tiles around a box. "
            "<bookmark mark='a'/> Fifteen numbered tiles, sixteen squares, one of them empty. You slide a tile into the "
            "empty square, one move at a time, and try to put the numbers in order. <bookmark mark='b'/> The famous "
            "version starts with everything in place except the last two: fourteen and fifteen are swapped. "
            "<bookmark mark='c'/> The puzzle-maker Sam Loyd later claimed he had offered a thousand dollars to anyone "
            "who could put them right. Nobody collected. People spent weeks on it."
        ) as vo:
            self.play(FadeIn(hc, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(board, lag_ratio=0.05), run_time=1.6)
            vo.wait_until("b")
            self.play(Indicate(board.tile[14], color=HEAD), Indicate(board.tile[15], color=HEAD), FadeIn(ask))
            vo.wait_until("c")
            self.play(FadeIn(prize, shift=UP * 0.1), FadeIn(src))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def slide(self):
        d = load("puzzles")
        walk = d["walk"]
        par, dist = d["walk_parity"], d["walk_dist"]
        board = tile_board(walk[0], 4, cell=0.9, font_size=36).move_to(LEFT * 3.0 + DOWN * 0.2)
        # the two quantities, and their sum
        def row(txt, col):
            return label(txt, font_size=28, color=col)
        p_lab = row(r"swaps of the 16 squares so far:", GREY_A)
        p_val = label(r"even", font_size=30, color=CTRL)
        d_lab = row(r"blank's distance from its corner:", GREY_A)
        d_val = live_int(0, 32, DATA)
        s_lab = row(r"together:", GREY_A)
        s_val = label(r"even", font_size=30, color=YES)
        panel = VGroup(VGroup(p_lab, p_val), VGroup(d_lab, d_val), VGroup(s_lab, s_val))
        for r in panel:
            r.arrange(RIGHT, buff=0.3)
        panel.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 3.0 + UP * 0.6)
        d_val.add_updater(lambda m: m.next_to(d_lab, RIGHT, buff=0.3))
        moves = live_int(0, 30, COST)
        mv = VGroup(label(r"moves:", font_size=26, color=GREY_B), moves).arrange(RIGHT, buff=0.2)
        mv.next_to(board, DOWN, buff=0.35)
        moves.add_updater(lambda m: m.next_to(mv[0], RIGHT, buff=0.2))
        head = label(r"Watch two numbers while the tiles move", font_size=36).to_edge(UP, buff=0.4)
        cur = list(walk[0])

        def step_anims(k, rt):
            nonlocal cur, p_val, s_val
            nxt = walk[k]
            z_old = cur.index(0)
            v = cur[nxt.index(0)]  # the tile that moved into the old blank
            anims = [board.tile[v].animate(run_time=rt).move_to(cell_center(board, z_old)),
                     moves.tracker.animate(run_time=rt).set_value(k), d_val.tracker.animate(run_time=rt).set_value(dist[k])]
            new_p = label(r"odd" if par[k] else r"even", font_size=30, color=CTRL).move_to(p_val, aligned_edge=LEFT)
            anims.append(Transform(p_val, new_p, run_time=rt))
            cur = list(nxt)
            return anims

        with self.voiceover(
            "Instead of trying, watch two numbers while the tiles move. <bookmark mark='a'/> The first: think of the "
            "empty square as a sixteenth tile. Every move swaps it with a neighbour. Count the swaps: is the "
            "arrangement an even or an odd number of swaps away from where it started? <bookmark mark='b'/> The second: "
            "how far the empty square is from its home corner, counting steps along rows and columns. "
            "<bookmark mark='c'/> Now move at random. The first number flips between even and odd on every move. So "
            "does the second, because the blank moves exactly one square. They flip together, so their sum is always "
            "even. Always."
        ) as vo:
            self.play(FadeIn(head), FadeIn(board), FadeIn(mv))
            vo.wait_until("a")
            self.play(FadeIn(panel[0]))
            vo.wait_until("b")
            self.play(FadeIn(panel[1]))
            vo.wait_until("c")
            self.play(FadeIn(panel[2]))
            for k in range(1, len(walk)):
                rt = 0.5 if k < 8 else 0.18
                self.play(*step_anims(k, rt))
            self.play(Indicate(s_val, color=YES, scale_factor=1.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def argument(self):
        d = load("puzzles")
        loyd = list(range(1, 14)) + [15, 14, 0]
        board = tile_board(loyd, 4, cell=0.66, font_size=28, hot=(14, 15)).move_to(RIGHT * 5.2 + DOWN * 0.5)
        lines = VGroup(*[label(t, font_size=27, color=c) for t, c in (
            (r"each move swaps the blank with one tile: \ the swap parity flips", CTRL),
            (r"each move shifts the blank one square: \ its distance flips parity", DATA),
            (r"so \ (swap parity) + (distance) \ stays even, \ move after move", YES),
            (r"Loyd's position: \ one swap \ (odd), \ blank at home \ (distance 0)", HEAD),
            (r"odd $\ne$ even: \ no sequence of moves can reach it", NO),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(LEFT, buff=0.5).shift(UP * 0.4)
        word = definition_card(r"invariant", r"a quantity no allowed move can change", color=YES, width=5.6,
                               font_size=26).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        hc = history_card(1879, r"W. W. Johnson and W. E. Story", r"\textit{American Journal of Mathematics}: \ "
                          r"exactly half the arrangements are reachable", width=5.0, font_size=21)
        hc.to_corner(UR, buff=0.35)
        with self.voiceover(
            "That is the whole proof. <bookmark mark='a'/> Every move swaps the blank with one tile, so the parity of "
            "the swaps flips. <bookmark mark='b'/> Every move shifts the blank by one square, so the parity of its "
            "distance flips. <bookmark mark='c'/> So their sum is even at the start, and stays even forever. "
            "<bookmark mark='d'/> Now look at Loyd's position. It is one swap from the solved board: fourteen and "
            "fifteen. One is odd. And the blank is home, distance zero. Odd plus zero is odd. <bookmark mark='e'/> No "
            "sequence of moves, of any length, can get there. Weeks of sliding, settled in four lines. "
            "<bookmark mark='f'/> A quantity that no allowed move can change is called an invariant. William Johnson and "
            "William Story published this in 1879, and proved the converse too: every position with an even sum can be "
            "reached."
        ) as vo:
            self.play(FadeIn(board))
            for mk, l in zip("abcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=RIGHT * 0.15))
            vo.wait_until("f")
            self.play(FadeIn(word), FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def computed(self):
        d = load("puzzles")
        boards = Group()
        for s in d["sizes"]:
            r_, c_ = s["rows"], s["cols"]
            b = tile_board(list(range(1, r_ * c_)) + [0], c_, cell=0.55, font_size=24)
            cap = label(rf"${r_} \times {c_}$: \ ${fmt(s['reachable'])}$ of ${fmt(s['total'])}$", font_size=26,
                        color=YES)
            boards.add(Group(b, cap.next_to(b, DOWN, buff=0.25)))
        boards.arrange(RIGHT, buff=1.0, aligned_edge=DOWN).to_edge(UP, buff=0.6)
        s3 = d["sizes"][2]
        hist = np.array(s3["hist"], float)
        ax = Axes(x_range=[0, 32, 4], y_range=[0, 26000, 5000], x_length=8.4, y_length=2.6,
                  axis_config={"color": GREY_C, "include_tip": False, "font_size": 20},
                  x_axis_config={"numbers_to_include": list(range(0, 33, 4))},
                  y_axis_config={"numbers_to_include": [10000, 20000], "font_size": 18}).to_edge(DOWN, buff=0.75)
        bars = VGroup(*[Rectangle(width=ax.x_length / 33 * 0.85, height=max(ax.y_length * h / 26000, 0.005),
                                  stroke_width=0, fill_color=DATA, fill_opacity=0.9).move_to(
            ax.c2p(k, 0), aligned_edge=DOWN) for k, h in enumerate(hist)])
        xl = label(r"moves needed, \ $3 \times 3$ puzzle \ (every reachable position, \ by breadth-first search)",
                   font_size=22, color=GREY_B).next_to(ax, DOWN, buff=0.15)
        far = label(rf"the farthest: \ {s3['n_farthest']} positions, \ {s3['max_dist']} moves", font_size=24,
                    color=HEAD).next_to(ax, UP, buff=0.0).align_to(ax, RIGHT)
        big = math.factorial(16) // 2
        tag = note(rf"computed; \ for $4 \times 4$ the reachable half is ${fmt(big)}$ positions", font_size=22)
        tag.next_to(boards, DOWN, buff=0.3)
        with self.voiceover(
            "We can check the claim by brute force on smaller boards. <bookmark mark='a'/> Breadth-first search, which "
            "Part 18 builds properly, visits every position reachable from the solved one. On a two by two board, "
            f"twelve of the twenty-four arrangements. On two by three, three hundred and sixty of seven hundred and "
            f"twenty. On three by three, {say(s3['reachable'])} of {say(s3['total'])}: exactly half, every time, and "
            "exactly the half the invariant allows. <bookmark mark='b'/> Here is how far those positions are from "
            f"solved. The hardest need {s3['max_dist']} moves, and there are only {s3['n_farthest']} of them. "
            "<bookmark mark='c'/> For the real puzzle, the reachable half is more than ten trillion positions. A search "
            "would take a while. The proof took four lines."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in boards], lag_ratio=0.4), run_time=2.4)
            vo.wait_until("b")
            self.play(Create(ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.03),
                      FadeIn(xl), run_time=2.4)
            self.play(FadeIn(far))
            vo.wait_until("c")
            self.play(FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Proof and Counting", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"logic: \ propositions, \ connectives, \ quantifiers, \ and how to negate them",
            r"proof: \ direct, \ contrapositive, \ contradiction, \ cases; \ induction, \ on numbers and on structures",
            r"invariants and decreasing measures: \ the method that proves programs correct",
            r"sets, \ relations, \ functions, \ orders; \ countable and uncountable",
            r"counting: \ choices, \ Pascal's triangle, \ pigeonholes, \ inclusion--exclusion, \ Catalan numbers",
            r"numbers: \ Bezout, \ congruences, \ the Chinese remainder theorem; \ chance, \ expectation, \ graphs",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 1 used proofs without saying what a proof is. This is Part 2: proof and counting, the mathematics "
            "the rest of the series stands on. <bookmark mark='a'/> Logic, the grammar of precise statements. The "
            "standard ways to prove one, and induction, the proof that climbs. Invariants, like the one we just used, "
            "which is how we will prove circuits, algorithms and distributed systems correct. Sets, relations, "
            "functions and orders, and the sizes of infinite sets. Then counting: choices, Pascal's triangle, "
            "pigeonholes, inclusion and exclusion, and the Catalan numbers. And finally numbers, chance and graphs, "
            "which carry the cryptography, the algorithms and the networks of later acts."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
