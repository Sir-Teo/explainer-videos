from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs9.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, fmt,
                                  load)


class Pebbles(VoiceoverScene):
    def construct(self):
        self.card()
        self.game()
        self.play_game()
        self.proof()
        self.against()

    def card(self):
        card = chapter_card(10, r"The red-blue pebble game", r"How much data must any matrix multiply move?",
                            lit=(1981,), extra=((1981, r"Hong and Kung"),), part=PART)
        with self.voiceover("Chapter ten. The red-blue pebble game."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def game(self):
        head = label(r"Hong and Kung, \ 1981", font_size=38).to_edge(UP, buff=0.35)
        rules = VGroup(
            label(r"a computation is a graph: \ inputs, \ operations, \ outputs", font_size=24, color=GREY_A),
            label(r"a red pebble on a node: \ the value is in fast memory \ (at most $M$ red pebbles)", font_size=24,
                  color=NO),
            label(r"a blue pebble: \ the value is in slow memory \ (as many as you like)", font_size=24, color=DATA),
            label(r"moves: \ load (blue $\to$ red), \ store (red $\to$ blue), \ compute (red on every input $\to$ red "
                  r"on the output)", font_size=24, color=GREY_A),
            label(r"the cost: \ the number of loads and stores", font_size=26, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.1)
        with self.voiceover(
            "Programming tricks raise a question: how good can they get? In 1981 Jia-Wei Hong and H. T. Kung turned it "
            "into a game. <bookmark mark='a'/> Draw the computation as a graph: each operation a node, with arrows from "
            "its inputs. <bookmark mark='b'/> A red pebble on a node means its value is in fast memory, and you may "
            "have at most M red pebbles. <bookmark mark='c'/> A blue pebble means the value is in slow memory, and "
            "blue pebbles are unlimited. <bookmark mark='d'/> You may load a value, turning blue into red; store one, "
            "red into blue; or compute a node, if all its inputs are red. <bookmark mark='e'/> The cost of a strategy "
            "is the number of loads and stores: the traffic between the levels. The question is the least cost of "
            "any strategy, for a given graph and a given M."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()

    def play_game(self):
        head = label(r"A tiny game: \ $y = (a + b)(a + c)$, \ with $M = 3$ red pebbles", font_size=32).to_edge(UP, buff=0.3)
        pos = {"a": LEFT * 3 + DOWN * 1.2, "b": LEFT * 1 + DOWN * 1.2, "c": RIGHT * 1 + DOWN * 1.2,
               "s": LEFT * 2 + UP * 0.2, "t": UP * 0.2, "y": LEFT * 1 + UP * 1.5}
        names = {"a": "a", "b": "b", "c": "c", "s": "a+b", "t": "a+c", "y": "y"}
        nodes = {k: VGroup(Circle(radius=0.38, color=GREY_C, stroke_width=2).move_to(v),
                           Text(names[k], font="DejaVu Sans Mono", font_size=18, color=WHITE).move_to(v))
                 for k, v in pos.items()}
        edges = VGroup(*[Arrow(nodes[a][0].get_center(), nodes[b][0].get_center(), buff=0.42, color=GREY_D,
                               stroke_width=2) for a, b in (("a", "s"), ("b", "s"), ("a", "t"), ("c", "t"),
                                                            ("s", "y"), ("t", "y"))])
        moves = [("load", "a"), ("load", "b"), ("compute", "s"), ("drop", "b"), ("load", "c"), ("compute", "t"),
                 ("drop", "a"), ("drop", "c"), ("compute", "y"), ("store", "y")]
        log = VGroup()
        cost = 0
        counter = label(r"loads + stores: \ 0", font_size=24, color=HEAD).to_corner(UR, buff=0.4).shift(DOWN * 0.6)
        red = {}
        blue = {k: Dot(nodes[k][0].get_right() + RIGHT * 0.12, radius=0.08, color=DATA) for k in "abc"}
        with self.voiceover(
            "Here is the game on a tiny computation: y equals a plus b, times a plus c, with room for three red "
            "pebbles. The inputs start in slow memory, blue. <bookmark mark='a'/> Load a and b, compute their sum, and "
            "drop b, which is no longer needed. Load c, compute a plus c, then drop a and c. Compute y from the two "
            "sums, and store it. <bookmark mark='b'/> Four transfers: three loads and a store, the least possible, "
            "since every input must be loaded once and the output stored once. With only two red pebbles, the same "
            "computation would need extra transfers; for matrix multiplication the extra traffic is exactly what the "
            "bound measures."
        ) as vo:
            self.play(FadeIn(head), Create(edges), *[FadeIn(n) for n in nodes.values()], *[FadeIn(b) for b in blue.values()],
                      FadeIn(counter))
            vo.wait_until("a")
            for kind, k in moves:
                anims = []
                if kind in ("load", "compute"):
                    red[k] = Dot(nodes[k][0].get_left() + LEFT * 0.12, radius=0.1, color=NO)
                    anims.append(FadeIn(red[k], scale=1.5))
                    anims.append(nodes[k][0].animate.set_stroke(NO))
                elif kind == "drop":
                    anims.append(FadeOut(red.pop(k)))
                    anims.append(nodes[k][0].animate.set_stroke(GREY_C))
                else:
                    blue[k] = Dot(nodes[k][0].get_right() + RIGHT * 0.12, radius=0.08, color=DATA)
                    anims.append(FadeIn(blue[k], scale=1.5))
                if kind in ("load", "store"):
                    cost += 1
                    anims.append(Transform(counter, label(rf"loads + stores: \ {cost}", font_size=24,
                                                          color=HEAD).move_to(counter)))
                self.play(*anims, run_time=0.6)
            vo.wait_until("b")
            self.play(Indicate(counter, color=YES))
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        head = label(r"Matrix multiply: \ the proof idea", font_size=36).to_edge(UP, buff=0.35)
        steps = VGroup(
            label(r"1. \ cut any schedule into segments of $M$ loads and stores", font_size=24, color=GREY_A),
            label(r"2. \ in one segment at most $2M$ values of $A$, \ $B$, \ $C$ are at hand", font_size=24,
                  color=GREY_A),
            label(r"3. \ the Loomis--Whitney inequality: \ with $a$, \ $b$, \ $c$ elements of the three, \ at most "
                  r"$\sqrt{abc}$ multiplications", font_size=24, color=DATA),
            label(r"4. \ so each segment does $O(M^{3/2})$ of the $n^3$ multiplications", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.4)
        bound = MathTex(r"Q \;\ge\; \frac{n^3}{O(M^{3/2})} \times M \;=\; \Omega\!\left(\frac{n^3}{\sqrt{M}}\right)",
                        font_size=44, color=HEAD).next_to(steps, DOWN, buff=0.4)
        tight = note(r"with the constant: \ $Q \ge 2n^3/\sqrt{M} - 2M$ \ (Smith, \ van de Geijn and others, \ 2019)",
                     font_size=20).next_to(bound, DOWN, buff=0.2)
        with self.voiceover(
            "For multiplying two n by n matrices, Hong and Kung proved a lower bound. The idea fits on one screen. "
            "<bookmark mark='a'/> Cut any schedule into segments, each containing M loads and stores. <bookmark "
            "mark='b'/> During one segment, at most two M values can be at hand: the M already in fast memory and the M "
            "loaded during it. <bookmark mark='c'/> Now a geometric fact, the Loomis-Whitney inequality: if you hold a "
            "elements of A, b of B and c of C, you can do at most the square root of a b c of the multiplications A i k "
            "times B k j. <bookmark mark='d'/> So one segment does at most on the order of M to the three halves "
            "multiplications, and there are n cubed to do. The number of segments, times M, gives the bound: any "
            "schedule moves at least on the order of n cubed over the square root of M words. In 2019 Tyler Smith, "
            "Robert van de Geijn and colleagues pinned down the constant: two n cubed over root M."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
            self.play(Write(bound), FadeIn(tight))
        self.wait(0.3)
        self.clear_scene()

    def against(self):
        d = load("pebbles")
        head = label(rf"Our multiplies against the bound: \ $n = {d['n']}$, \ $M = {d['M']}$ words \ (8 KB)",
                     font_size=32).to_edge(UP, buff=0.3)
        rows = d["rows"]
        names = [r"i-j-k", r"i-k-j", r"tiled, \ $T = 4$", r"tiled, \ $T = 8$", r"tiled, \ $T = 16$"]
        vals = [r["words"] / 1000 for r in rows]
        ch = bar_chart(vals, names, [NO, NO, DATA, DATA, YES], height=3.4, bar_w=1.0, gap=0.9, font_size=20,
                       fmt_=lambda v: f"{v:.0f}K").move_to(DOWN * 0.3)
        y0 = ch.bars[0].get_bottom()[1]
        h = 3.4 * d["bound"] / 1000 / max(vals)
        bl = DashedLine([ch.get_left()[0], y0 + h, 0], [ch.get_right()[0], y0 + h, 0], color=HEAD, stroke_width=3)
        blab = label(rf"the bound: \ {d['bound'] / 1000:.1f}K words", font_size=22, color=HEAD).next_to(bl, UP,
                                                                                                   buff=0.08).align_to(
            bl, RIGHT)
        yl = note(r"words moved \ (simulated, \ fully associative LRU)", font_size=18).next_to(ch, UP, buff=0.3).align_to(
            ch, LEFT)
        punch = label(rf"the best tile is within {rows[-1]['words'] / d['bound']:.1f} times of the bound; \ the "
                      r"untiled orders, \ 19 times", font_size=24, color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Our simulator can play the game for real. Take sixty-four by sixty-four matrices and a fast memory of a "
            "thousand and twenty-four words. <bookmark mark='a'/> The bound says any schedule must move at least "
            "fourteen thousand words. <bookmark mark='b'/> Both untiled orders move two hundred seventy thousand, "
            "nineteen times the bound. <bookmark mark='c'/> Tiles of four and eight move about seventy thousand; "
            "tiles of sixteen, forty-two thousand, within three times of the bound, with an ordinary LRU cache "
            "instead of an optimal one. <bookmark mark='d'/> The theorem says no cleverness can do better than the "
            "dashed line, and tiling gets close to it. The same bound, at scale, is why matrix multiplication on a "
            "GPU is limited by memory traffic as often as by arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(ch[0]))
            vo.wait_until("a")
            self.play(Create(bl), FadeIn(blab))
            for mk, ks in (("b", [0, 1]), ("c", [2, 3, 4])):
                vo.wait_until(mk)
                self.play(*[GrowFromEdge(ch.bars[k], DOWN) for k in ks], *[FadeIn(ch.vals[k]) for k in ks],
                          *[FadeIn(ch.names[k]) for k in ks])
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
