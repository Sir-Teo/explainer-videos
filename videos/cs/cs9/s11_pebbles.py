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
        card = chapter_card(10, r"The red-blue pebble game", "How much data must this computation move?",
                            lit=(1981,), extra=((1981, r"Hong and Kung"),), part=PART)
        with self.voiceover(
            "Chapter ten. The red-blue pebble game."
        ):
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
            "The pebble game asks about a specified computation graph. Hong and Kung introduced this framework in "
            "1981. <bookmark mark='a'/> Nodes hold inputs or computed values; arrows identify required operands. "
            "<bookmark mark='b'/> Red pebbles represent values in fast memory, with a limit of M. <bookmark "
            "mark='c'/> Blue pebbles represent stored slow-memory values. A value may have both colors at once. "
            "<bookmark mark='d'/> Loading adds a red copy, storing adds a blue copy, and computing places a new red "
            "pebble when all predecessor values are red. Removing a red pebble is free; our illustration does not "
            "overwrite an input pebble during a compute move. <bookmark mark='e'/> Count loads and stores. The "
            "graph, initial/output conditions and recomputation rules are part of the problem, so changing them can "
            "change its optimum."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rules):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
        self.wait(0.3)
        self.clear_scene()

    def play_game(self):
        head = label(r"A tiny game: \ $y = (a + b)(a + c)$, \ with $M = 4$ red pebbles", font_size=32).to_edge(UP, buff=0.3)
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
        occupancy = label("red pebbles: \\ 0 / 4", font_size=22, color=NO).next_to(counter, DOWN, buff=0.2)
        red = {}
        blue = {k: Dot(nodes[k][0].get_right() + RIGHT * 0.12, radius=0.08, color=DATA) for k in "abc"}
        with self.voiceover(
            "Compute y equals a plus b, times a plus c, under the place-new-pebble rules with four red slots. Inputs "
            "begin in slow memory and y must finish there. <bookmark mark='a'/> Load a and b, compute their sum, "
            "drop b, then load c. Computing the second sum temporarily needs four red pebbles: a, c and both sums. "
            "The occupancy counter makes that peak explicit. Drop a and c, compute y and store it. <bookmark "
            "mark='b'/> Three input loads and one output store give four transfers, the minimum possible. "
            "Independent shortest-path search confirms it. With three red slots the same graph needs six transfers, "
            "spilling and reloading a partial result. Two slots cannot execute a binary compute move under these "
            "non-overwrite rules."
        ) as vo:
            self.play(FadeIn(head), Create(edges), *[FadeIn(n) for n in nodes.values()], *[FadeIn(b) for b in blue.values()],
                      FadeIn(counter), FadeIn(occupancy))
            vo.wait_until("a")
            for kind, k in moves:
                anims = []
                if kind in ("load", "compute"):
                    if kind == "compute":
                        inputs = {"s": {"a", "b"}, "t": {"a", "c"}, "y": {"s", "t"}}[k]
                        assert inputs <= red.keys()
                    red[k] = Dot(nodes[k][0].get_left() + LEFT * 0.12, radius=0.1, color=NO)
                    assert len(red) <= 4
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
                anims.append(Transform(occupancy, label(rf"red pebbles: \ {len(red)} / 4", font_size=22,
                                                        color=NO).move_to(occupancy)))
                self.play(*anims, run_time=0.6)
            vo.wait_until("b")
            self.play(Indicate(counter, color=YES))
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        head = label("Classical multiplication: \\ two-level movement proof sketch", font_size=36).to_edge(UP, buff=0.35)
        steps = VGroup(
            label(r"1. \ cut any schedule into segments of $M$ loads and stores", font_size=24, color=GREY_A),
            label("2. \\ boundary values and transfers constrain supported index projections", font_size=24,
                  color=GREY_A),
            label(r"3. \ the Loomis--Whitney inequality: \ with $a$, \ $b$, \ $c$ elements of the three, \ at most "
                  r"$\sqrt{abc}$ multiplications", font_size=24, color=DATA),
            label(r"4. \ so each segment does $O(M^{3/2})$ of the $n^3$ multiplications", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 0.4)
        bound = MathTex(r"Q \;\ge\; \frac{n^3}{O(M^{3/2})} \times M \;=\; \Omega\!\left(\frac{n^3}{\sqrt{M}}\right)",
                        font_size=44, color=HEAD).next_to(steps, DOWN, buff=0.4)
        tight = note("sharp total-I/O bound: \\ classical, no recomputation, all outputs in slow memory",
                     font_size=20).next_to(bound, DOWN, buff=0.2)
        with self.voiceover(
            "Consider classical matrix multiplication with its n-cubed scalar products, distinct matrices and the "
            "stated no-recomputation model. This is not a bound on every possible multiplication algorithm. "
            "<bookmark mark='a'/> Divide a valid schedule into segments with a limited number of transfers. "
            "<bookmark mark='b'/> Values already in fast memory and values brought in constrain what one segment can "
            "use. <bookmark mark='c'/> The Loomis-Whitney argument bounds how many distinct index triples can be "
            "supported by the available A, B and partial-output values. <bookmark mark='d'/> That yields the leading "
            "movement scale n cubed over square root M. A sharper argument gives the displayed constant and "
            "lower-order term when all outputs must end in slow memory. Read-only bounds and total read-plus-write "
            "bounds have different lower-order terms; the short sketch does not derive the sharp constant by itself."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(s, shift=RIGHT * 0.1))
                if mk == 'a':
                    vo.wait_until(mk)
            self.play(Write(bound), FadeIn(tight))
        self.wait(0.3)
        self.clear_scene()

    def against(self):
        d = load("pebbles")
        head = label(rf"Classical multiply: \ $n={d['n']}$, \ $M={d['M']}$ words total \ ({d['cache_words']} cache + {d['scalar_words']} scalar)",
                     font_size=32).to_edge(UP, buff=0.3)
        rows = d["rows"]
        names = [r"i-j-k", r"i-k-j", r"tiled, \ $T = 4$", r"tiled, \ $T = 8$", r"tiled, \ $T = 16$"]
        vals = [r["words"] / 1000 for r in rows]
        ch = bar_chart(vals, names, [NO, NO, DATA, DATA, YES], height=3.4, bar_w=1.0, gap=0.9, font_size=20,
                       fmt_=lambda v: f"{v:.0f}K").move_to(DOWN * 0.3)
        y0 = ch.bars[0].get_bottom()[1]
        h = 3.4 * d["bound"] / 1000 / max(vals)
        bl = DashedLine([ch.get_left()[0], y0 + h, 0], [ch.get_right()[0], y0 + h, 0], color=HEAD, stroke_width=3)
        blab = label(rf"the bound: \\ {d['bound'] / 1000:.1f}K words", font_size=22, color=HEAD).next_to(bl, RIGHT,
                                                                                                     buff=0.15)
        yl = note("read-fill words + dirty-write words; \\ final output drain included", font_size=18).next_to(ch, UP, buff=0.3).align_to(
            ch, LEFT)
        punch = label(rf"best shown tile: \ {min(r['words'] for r in rows[2:]) / d['bound']:.1f} times bound; \ "
                      rf"untiled: \ {rows[0]['words'] / d['bound']:.1f} times", font_size=24, color=YES).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Compare classical sixty-four-by-sixty-four address traces with a total fast-data budget of one thousand "
            "twenty-four words. Eight slots are reserved for scalar operands and accumulators; the rest form a fully "
            "associative LRU cache. <bookmark mark='a'/> The displayed lower bound counts both reads and writes and "
            "requires outputs in slow memory. <bookmark mark='b'/> The untiled bars now count line fills, dirty "
            "evictions and a final dirty-line drain. Counting fills alone would understate movement. <bookmark "
            "mark='c'/> The tile sizes give the other bars; their ratios are calculated from these counters. This is "
            "a specified trace-and-cache experiment, with zero-initialization setup excluded. <bookmark mark='d'/> "
            "It illustrates how blocking can approach the movement scale. Registers, physical write protocols, "
            "vectorization, arithmetic throughput and different algorithms require additional analysis before "
            "predicting actual GPU or CPU runtime."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl), FadeIn(ch[0]))
            self.play(Create(bl), FadeIn(blab))
            vo.wait_until("a")
            for mk, ks in (("b", [0, 1]), ("c", [2, 3, 4])):
                vo.wait_until(mk)
                self.play(*[GrowFromEdge(ch.bars[k], DOWN) for k in ks], *[FadeIn(ch.vals[k]) for k in ks],
                          *[FadeIn(ch.names[k]) for k in ks])
            vo.wait_until("d")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()
