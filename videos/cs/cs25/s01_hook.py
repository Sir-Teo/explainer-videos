from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs25.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, load, mono, wang, wang_grid, words)


class Hook(VoiceoverScene):
    def construct(self):
        self.three()
        self.plan()

    def three(self):
        t = load("tiles")
        h = load("hilbert")
        q = load("quines")
        head = label('Three questions, three connections', font_size=36).to_edge(UP, buff=0.35)
        tiles = VGroup(*[wang(tt, 0.42) for tt in t["tiles"]]).arrange(RIGHT, buff=0.1)
        grid = wang_grid(t["tiles"], next(r["grid"] for r in t["rects"] if r["n"] == 12), s=0.2)
        q1 = VGroup(label(r"\textbf{1.} \ Can copies of these 11 tiles cover the whole plane?", font_size=22,
                          color=DATA), tiles).arrange(DOWN, buff=0.2)
        p61 = next(r for r in h["rows"] if r["D"] == 61)
        b61 = next(b for b in h["brute"] if b["D"] == 61)
        q2 = VGroup(label('\\textbf{2.} \\ Is there an integer solution with $y>0$?', font_size=22,
                          color=HEAD), MathTex(r"x^2 - 61\,y^2 = 1", font_size=40, color=HEAD)).arrange(DOWN, buff=0.2)
        q3 = VGroup(label(r"\textbf{3.} \ Can a program print exactly its own source code?", font_size=22, color=LAM),
                    mono("s = 's = %r\\nprint(s %% s)'", 20, LAM), mono("print(s % s)", 20, LAM)).arrange(DOWN, buff=0.12)
        VGroup(q1, q2, q3).arrange(DOWN, buff=0.45, aligned_edge=LEFT).next_to(head, DOWN, buff=0.45).to_edge(
            LEFT, buff=0.6)
        grid.to_edge(RIGHT, buff=0.6).align_to(q1, UP)
        a1 = label(r"yes, \ but never periodically: \\ a 12$\times$12 patch, \ found by backtracking", font_size=19,
                   color=DATA).next_to(grid, DOWN, buff=0.15).align_to(grid, RIGHT)
        a2 = label(rf"brute force: \ {words(b61['tried'])} values of $y$ in {b61['seconds']:.2f} s, \ nothing; \\ "
                   rf"the answer: \ $x = {p61['x']}$, \ $y = {p61['y']}$", font_size=19, color=HEAD).next_to(a1, DOWN,
                                                                                                         buff=0.35).align_to(grid, RIGHT)
        a3 = label(rf"yes: \ and one in the Pebble language, \\ {q['pebble_lines']} lines, \ checked on the emulator",
                   font_size=19, color=LAM).next_to(a2, DOWN, buff=0.35).align_to(grid, RIGHT)
        moral = label('tiling and integer equations: undecidable in general; \\ quines: constructive self-reference',
                      font_size=24, color=NO).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here are three questions linking geometry, arithmetic and programs. <bookmark mark='a'/> Can these eleven fixed-orientation Wang tiles cover the whole plane? <bookmark mark='b'/> Our search constructs finite patches. The separate Jeandel and Rao theorem proves full-plane tilings exist and none is periodic. <bookmark mark='c'/> Does x squared minus sixty-one y squared equal one have a solution with positive y? <bookmark mark='d'/> A million attempted positive values find none. Continued fractions give the least solution, with x equal to one billion, seven hundred and sixty-six million, three hundred and nineteen thousand and forty-nine. <bookmark mark='e'/> Can a program print its own source without reading a file? <bookmark mark='f'/> Yes. Both our Python and Pebble quines do exactly that. <bookmark mark='g'/> Tiling and general integer equations lead to undecidability. The quine question has a constructive answer: self-reference supplies a technique used in the impossibility proofs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in grid], lag_ratio=0.004), FadeIn(a1), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(q2))
            vo.wait_until("d")
            self.play(FadeIn(a2))
            vo.wait_until("e")
            self.play(FadeIn(q3))
            vo.wait_until("f")
            self.play(FadeIn(a3))
            vo.wait_until("g")
            self.play(FadeIn(moral))
        self.wait(0.3)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Undecidable", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"decidable, \ recognizable, \ and reductions between undecidable problems",
            r"Rice's theorem; \ the recursion theorem and programs that print themselves",
            r"dominoes, \ tiles and Diophantine equations: \ halting in disguise",
            r"G\"odel's incompleteness, \ proved from halting; \ oracles and the arithmetic hierarchy",
            r"Kolmogorov complexity, \ Chaitin's $\Omega$, \ and busy beavers again",
            r"where decidability ends, \ undecidability in the wild, \ and the frontier",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "Part 25 of Computer Science, Built: Undecidable. Act Five begins: limits and secrets. <bookmark mark='a'/> We study decidability, recognition and reductions; Rice's theorem for nontrivial extensional program properties; constructive self-reference; dominoes, tiles and integer equations; effective arithmetic theories and incompleteness; oracles and the arithmetic hierarchy; plain program complexity, prefix-free Omega, and busy beavers. Each result has a model and assumptions, and our finite experiments will keep their limits explicit."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
