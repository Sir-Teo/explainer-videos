from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs1.common import CTRL, DATA, HEAD, HIST, NO, PART, YES, load, pebble, pebble_pile


class Hook(VoiceoverScene):
    def construct(self):
        self.piles()
        self.calculus()
        self.hilbert()
        self.turing()
        self.plan()

    # ------------------------------------------------------------------
    def piles(self):
        d = load("pebbles")
        steps = d["steps"]
        L, R = np.array([-3.4, -2.9, 0]), np.array([3.4, -2.9, 0])
        left = pebble_pile(steps[0][0], L, cols=6, seed=1, radius=0.23)
        right = pebble_pile(steps[0][1], R, cols=6, seed=40, radius=0.23)
        cl = Integer(steps[0][0], font_size=60, color=DATA).move_to(L + UP * 2.6)
        cr = Integer(steps[0][1], font_size=60, color=DATA).move_to(R + UP * 2.6)
        rule = VGroup(
            label(r"The rule:", font_size=34, color=CTRL),
            label(r"if the piles differ, take from the bigger one \\ as many pebbles as the smaller one has", font_size=34),
            label(r"stop when they are equal", font_size=34),
        ).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Here is a game for someone who knows nothing about numbers. Two piles of pebbles. <bookmark mark='a'/> "
            "One rule. If the piles are different, take away from the bigger pile as many pebbles as there are in "
            "the smaller one. <bookmark mark='b'/> When the piles are equal, stop."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in left], lag_ratio=0.03),
                      LaggedStart(*[FadeIn(p, shift=DOWN * 0.3) for p in right], lag_ratio=0.03), run_time=2.2)
            self.play(FadeIn(cl), FadeIn(cr))
            vo.wait_until("a")
            self.play(FadeIn(rule[0]), FadeIn(rule[1]))
            vo.wait_until("b")
            self.play(FadeIn(rule[2]))
        with self.voiceover(
            "Twenty-four and eighteen. The left pile is bigger, so take eighteen pebbles from it. <bookmark mark='a'/> "
            "Six and eighteen: now the right is bigger; take six from it. <bookmark mark='b'/> Six and twelve: take six "
            "again. <bookmark mark='c'/> Six and six. The piles are equal, and the game is over."
        ) as vo:
            for k, mk in enumerate("abc"):
                (a0, b0), (a1, b1) = steps[k], steps[k + 1]
                if a0 > b0:
                    gone = left[a1:]
                    left = VGroup(*left[:a1])
                    tgt = cl
                    new = a1
                else:
                    gone = right[b1:]
                    right = VGroup(*right[:b1])
                    tgt = cr
                    new = b1
                moved = VGroup(*gone)
                self.play(moved.animate.set_color(HEAD), run_time=0.4)
                self.play(LaggedStart(*[FadeOut(q, shift=DOWN * 1.4) for q in moved], lag_ratio=0.02),
                          ChangeDecimalToValue(tgt, new), run_time=1.2)
                if mk != "c":
                    vo.wait_until(mk)
            self.play(Indicate(cl, color=HEAD), Indicate(cr, color=HEAD))
        ans = label(r"$6 = \gcd(24, 18)$", font_size=50, color=YES).move_to(UP * 2.6)
        euclid = note(r"Euclid, \textit{Elements}, Book VII, Proposition 2 \ (about 300 BC)", font_size=24)
        euclid.next_to(ans, DOWN, buff=0.3)
        with self.voiceover(
            "The player has computed something. <bookmark mark='a'/> Six is the greatest common divisor of twenty-four "
            "and eighteen: the largest number that divides both. <bookmark mark='b'/> This is Euclid's algorithm, written "
            "down about twenty-three hundred years ago. And the player needed no idea what a divisor is. They only "
            "had to follow the rule."
        ) as vo:
            self.play(FadeOut(rule))
            vo.wait_until("a")
            self.play(Write(ans))
            vo.wait_until("b")
            self.play(FadeIn(euclid, shift=UP * 0.1))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def calculus(self):
        word = label(r"\textit{calculus}", font_size=96, color=HEAD).move_to(UP * 1.6)
        gloss_ = label(r"Latin: \ a small stone, \ a pebble", font_size=36, color=GREY_A).next_to(word, DOWN, buff=0.35)
        stones = VGroup(*[pebble(0.2, seed=7 + i) for i in range(5)]).arrange(RIGHT, buff=0.25).next_to(gloss_, DOWN,
                                                                                                      buff=0.5)
        # a Roman counting board: lines for units, tens, hundreds; pebbles on the lines
        board = VGroup()
        lines = VGroup(*[Line(LEFT * 2.6, RIGHT * 2.6, color=GREY_C, stroke_width=2).shift(DOWN * (i * 0.55))
                         for i in range(4)])
        names = VGroup(*[label(n, font_size=22, color=GREY_B).next_to(lines[i], LEFT, buff=0.2)
                         for i, n in enumerate([r"thousands", r"hundreds", r"tens", r"units"])])
        counts = [1, 9, 2, 8]  # 1928
        pebs = VGroup()
        for i, c in enumerate(counts):
            for j in range(c):
                p = pebble(0.13, seed=30 + 10 * i + j).move_to(lines[i].get_left() + RIGHT * (0.5 + 0.42 * j))
                pebs.add(p)
        board.add(lines, names, pebs)
        board.move_to(DOWN * 1.9)
        value = label(r"$1928$", font_size=40, color=DATA).next_to(board, RIGHT, buff=0.5)
        words = VGroup(*[label(w, font_size=34, color=GREY_A) for w in
                         (r"calculate", r"calculus", r"calculator")]).arrange(RIGHT, buff=0.7).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Moving pebbles by rule is an old way of thinking. <bookmark mark='a'/> The Latin word for a pebble is "
            "calculus. Roman merchants reckoned with pebbles on lined counting boards: <bookmark mark='b'/> a pebble on "
            "the lowest line counts one, on the next line ten, then a hundred, then a thousand. <bookmark mark='c'/> To "
            "calculate was, literally, to move the stones."
        ) as vo:
            self.play(Write(word), LaggedStart(*[FadeIn(s, scale=0.5) for s in stones], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(gloss_))
            vo.wait_until("b")
            self.play(FadeOut(stones), Create(lines), FadeIn(names))
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for p in pebs], lag_ratio=0.05), run_time=2.0)
            self.play(FadeIn(value))
            vo.wait_until("c")
            self.play(FadeOut(board), FadeOut(value), FadeIn(words, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hilbert(self):
        yr = label(r"1928", font_size=60, color=HIST).to_corner(UL, buff=0.5)
        who = label(r"David Hilbert \ and \ Wilhelm Ackermann", font_size=30, color=GREY_A).next_to(yr, RIGHT, buff=0.4)
        box = RoundedRectangle(width=3.4, height=1.8, corner_radius=0.2, stroke_color=CTRL, stroke_width=3,
                               fill_color=CTRL, fill_opacity=0.08)
        q = label(r"?", font_size=90, color=CTRL).move_to(box)
        machine = VGroup(box, q).move_to(RIGHT * 0.6 + DOWN * 0.3)
        tag = label(r"a mechanical procedure", font_size=28, color=CTRL)
        stmts = [r"there are infinitely many \\ twin primes $p,\ p+2$",
                 r"every even number $> 2$ \\ is a sum of two primes",
                 r"$x^n + y^n = z^n$ has no solution \\ in positive integers for $n > 2$"]
        machine.move_to(RIGHT * 1.6 + DOWN * 0.2)
        ins = VGroup(*[label(s, font_size=28, color=DATA) for s in stmts]).arrange(DOWN, buff=0.5, aligned_edge=RIGHT)
        ins.next_to(box, LEFT, buff=0.9)
        arrows = VGroup(*[Arrow(s.get_right(), box.get_left(), buff=0.15, color=GREY_C, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.12) for s in ins])
        out_t = label(r"true", font_size=36, color=YES)
        out_f = label(r"false", font_size=36, color=NO)
        outs = VGroup(out_t, out_f).arrange(DOWN, buff=0.6).next_to(box, RIGHT, buff=0.9)
        tag.next_to(box, UP, buff=0.2)
        oarr = VGroup(*[Arrow(box.get_right(), o.get_left(), buff=0.15, color=GREY_C, stroke_width=2.5) for o in outs])
        name = label(r"the \textit{Entscheidungsproblem} \ (the decision problem)", font_size=30, color=HEAD)
        name.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1928 the mathematician David Hilbert, with Wilhelm Ackermann, asked whether all of mathematics could be "
            "done this way. <bookmark mark='a'/> Is there a mechanical procedure, a set of rules for moving symbols "
            "like pebbles, <bookmark mark='b'/> that takes any precisely stated mathematical claim and decides, in a "
            "finite number of steps, whether it is true? <bookmark mark='c'/> Such a procedure would settle every open "
            "problem at once, by turning the crank. <bookmark mark='d'/> Hilbert called it the decision problem, the "
            "Entscheidungsproblem, and he expected the answer to be yes."
        ) as vo:
            self.play(FadeIn(yr), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(machine), FadeIn(tag))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in ins], lag_ratio=0.3),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(a) for a in oarr], lag_ratio=0.2), FadeIn(outs))
            vo.wait_until("d")
            self.play(FadeIn(name, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def turing(self):
        yr = label(r"1936", font_size=60, color=HIST).to_corner(UL, buff=0.5)
        who = label(r"Alan Turing, \ aged 23", font_size=30, color=GREY_A).next_to(yr, RIGHT, buff=0.4)
        title = label(r"``On computable numbers, \ with an application to the \textit{Entscheidungsproblem}''",
                      font_size=28).next_to(VGroup(yr, who), DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        no = label(r"No.", font_size=110, color=NO).move_to(LEFT * 3.6 + DOWN * 0.9)
        tape = TapeView(list("_1101_1_"), head=3, state="A", cell=0.62).scale(0.95).move_to(RIGHT * 2.4 + DOWN * 0.4)
        rules = RuleTable([("A", "1", "0", "R", "B"), ("A", "0", "1", "L", "A"), ("B", "_", "1", "L", "H")],
                          font_size=22, header=False).scale(0.8).next_to(tape, DOWN, buff=0.5)
        cap = label(r"a tape, \ a head, \ a table of rules", font_size=28, color=CTRL).next_to(rules, DOWN, buff=0.35)
        with self.voiceover(
            "Eight years later, a twenty-three-year-old in Cambridge, Alan Turing, sent off his answer. "
            "<bookmark mark='a'/> The answer was no. No such procedure can exist. <bookmark mark='b'/> But to prove that, "
            "Turing first had to say exactly what a mechanical procedure is. His definition was a machine: a tape of "
            "symbols, a head that reads and writes one of them at a time, and a finite table of rules. "
            "<bookmark mark='c'/> He invented it to show what machines cannot do. It became the blueprint of every "
            "computer built since."
        ) as vo:
            self.play(FadeIn(yr), FadeIn(who), FadeIn(title))
            vo.wait_until("a")
            self.play(FadeIn(no, scale=1.4))
            vo.wait_until("b")
            self.play(FadeIn(tape), FadeIn(rules), FadeIn(cap))
            self.play(rules.light(0), run_time=0.4)
            self.play(tape.step("0", 1, "B"))
            vo.wait_until("c")
            self.play(Indicate(tape, color=HEAD, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ What Is a Computation?", font_size=46).to_edge(UP, buff=0.4)
        smap = series_map(current=PART).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"algorithms before machines: \ Euclid, \ Babbage's engines, \ Lovelace's program",
            r"Hilbert's question, \ and Turing's machine: \ tapes, \ heads, \ tables, \ and how to program them",
            r"why more tapes, \ nondeterminism and other models add no power, \ and the universal machine",
            r"$\lambda$-calculus, \ counter machines and cellular automata; \ the Church--Turing thesis",
            r"more problems than programs; \ the halting problem; \ reductions; \ busy beavers",
            r"and what this series will build: \ a real computer, \ from one gate up",
        ], font_size=26).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 1 of Computer Science, Built: fifty-five lectures that start here, with the question of what "
            "computing is, build a working computer from a single kind of gate, and climb all the way to the systems "
            "that run the internet. <bookmark mark='a'/> In this part: algorithms before there were machines, and the "
            "engines of Babbage and Lovelace; Hilbert's question, and Turing's machine, which we will program by hand; "
            "why extra tapes and other designs add no power, and the universal machine that can run any other; the "
            "lambda calculus, counter machines and cellular automata, and the Church-Turing thesis; why there are more "
            "problems than programs, the halting problem, and the busy beavers. And at the end, what this series will "
            "build."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.4)
        self.clear_scene()
