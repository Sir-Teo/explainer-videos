from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs15.common import (CODE, COST, CTRL, DATA, FUNC, HEAD, LAM, NO, PART, YES, code, grid_table, load,
                                   mono, words)


class Interpreters(VoiceoverScene):
    def construct(self):
        self.card()
        self.evalapply()
        self.metacircular()
        self.ladder()

    def card(self):
        card = chapter_card(1, r"Interpreters: \ eval and apply", r"What does it take to run a program?",
                            lit=(1960,), extra=((1960, r"McCarthy's LISP: \ \texttt{eval}"),), part=PART)
        with self.voiceover("Chapter one. Interpreters: eval and apply."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def evalapply(self):
        head = label(r"Two procedures that call each other", font_size=34).to_edge(UP, buff=0.3)
        ev = VGroup(Circle(radius=1.05, color=DATA, stroke_width=3),
                    label(r"\textbf{eval}", font_size=30, color=DATA))
        ap = VGroup(Circle(radius=1.05, color=LAM, stroke_width=3),
                    label(r"\textbf{apply}", font_size=30, color=LAM))
        ev[1].move_to(ev[0])
        ap[1].move_to(ap[0])
        VGroup(ev, ap).arrange(RIGHT, buff=3.2).move_to(LEFT * 2.6 + DOWN * 0.2)
        a1 = CurvedArrow(ev[0].get_top() + RIGHT * 0.3, ap[0].get_top() + LEFT * 0.3, angle=-1.0, color=GREY_B,
                         stroke_width=2.5, tip_length=0.18)
        a2 = CurvedArrow(ap[0].get_bottom() + LEFT * 0.3, ev[0].get_bottom() + RIGHT * 0.3, angle=-1.0,
                         color=GREY_B, stroke_width=2.5, tip_length=0.18)
        l1 = label(r"a function and its argument", font_size=19, color=GREY_A).next_to(a1, UP, buff=0.1)
        l2 = label(r"its body, \ in a new environment", font_size=19, color=GREY_A).next_to(a2, DOWN, buff=0.1)
        e_in = label(r"(expression, \ environment)", font_size=18, color=DATA).next_to(ev, DOWN, buff=0.15)
        src = code([
            "def ev(e, env):",
            "    if e is a variable:",
            "        return env[e.name]",
            "    if e is fun x -> body:",
            "        return Closure(x, body, env)",
            "    if e is f a:",
            "        c, v = ev(f, env), ev(a, env)",
            "        return ev(c.body,             # apply",
            "                  {**c.env, c.param: v})",
        ], size=16, color=CODE).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
        notes = VGroup(
            label(r"an \textbf{environment}: \ the values of the variables in scope", font_size=21, color=GREY_A),
            label(r"no substitution: \ a variable is looked up when it is used", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Every interpreter, from the first LISP to the JavaScript in your browser, has the same heart: two "
            "procedures that call each other. <bookmark mark='a'/> Eval takes an expression and an environment, "
            "the values of the variables in scope, and finds the expression's value. <bookmark mark='b'/> When "
            "the expression applies a function to an argument, eval evaluates both and hands them to apply. "
            "<bookmark mark='c'/> Apply runs the function's body, which means calling eval again, in a new "
            "environment where the parameter has the argument's value. <bookmark mark='d'/> Here is the core of "
            "our own interpreter for the lambda core, the one Part 14 used. Notice what it does not do: it never "
            "substitutes. Chapter one of Part 14 rewrote terms; a real interpreter keeps a table of values and "
            "looks a variable up only when it is used."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ev), FadeIn(e_in))
            vo.wait_until("a")
            self.play(Indicate(ev, color=DATA))
            vo.wait_until("b")
            self.play(Create(a1), FadeIn(l1), FadeIn(ap))
            vo.wait_until("c")
            self.play(Create(a2), FadeIn(l2))
            vo.wait_until("d")
            self.play(FadeIn(src), FadeIn(notes))
        self.wait(0.3)
        self.clear_scene()

    def metacircular(self):
        d = load("interp")
        head = label(r"A language, \ defined by a program", font_size=34).to_edge(UP, buff=0.3)
        quote = label(r"``the Maxwell's equations of software'' \ --- \ Alan Kay, \ on LISP's \texttt{eval}",
                      font_size=23, color=HEAD).next_to(head, DOWN, buff=0.4)
        pts = VGroup(
            label(r"McCarthy, \ 1960: \ \texttt{eval}, \ written in LISP, \ half a page long", font_size=22,
                  color=GREY_A),
            label(r"Steve Russell coded it by hand: \ the first LISP interpreter", font_size=22, color=GREY_A),
            label(r"an interpreter written in its own language is \textbf{metacircular} \ (SICP, \ 1985)",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(quote, DOWN, buff=0.5)
        tab = grid_table([r"the Job on Part 7's chapter", r"count"], [
            [r"applications (each one a new environment)", words(d["tree"]["apps"])],
            [r"values allocated (closures, pairs, cells)", words(d["tree"]["alloc"])],
        ], widths=[6.6, 2.4], row_h=0.5, font_size=21, mono_cols=(), colors=[[WHITE, COST], [WHITE, COST]]).next_to(
            pts, DOWN, buff=0.5)
        cost = label(r"every step pays for the interpretation: \ look up, \ copy the environment, \ dispatch on "
                     r"the kind of node", font_size=21, color=NO).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "This idea is older than almost anything else in programming languages. <bookmark mark='a'/> In 1960 "
            "John McCarthy defined LISP by writing eval in LISP itself: half a page. His student Steve Russell "
            "noticed that if he translated eval into machine code by hand, he would have a LISP interpreter, and "
            "he did. <bookmark mark='b'/> An interpreter written in the language it interprets is called "
            "metacircular, and Abelson and Sussman's textbook of 1985 built one in its fourth chapter. Alan Kay "
            "called that half page the Maxwell's equations of software. <bookmark "
            "mark='c'/> On the Job, our interpreter makes three hundred and fifty-eight thousand applications, and "
            "each one builds a new environment. <bookmark mark='d'/> That is the price of interpreting a tree: "
            "every step looks up names, copies tables and asks what kind of node it is looking at. The rest of "
            "the first half of this part removes those costs one by one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]))
            vo.wait_until("b")
            self.play(FadeIn(pts[2]), FadeIn(quote))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(cost))
        self.wait(0.3)
        self.clear_scene()

    def ladder(self):
        d = load("interp")
        head = label(rf"One function, \ every runtime on this machine: \ \texttt{{fib({d['fib_n']})}}", font_size=32
                     ).to_edge(UP, buff=0.3)
        rows = sorted(d["fib"], key=lambda r: r["seconds"])
        kc = {"aot": YES, "jit": DATA, "interp": NO}
        lo, hi = -3.0, 0.0
        W = 6.4
        x0 = -0.2
        bars = VGroup()
        for i, r in enumerate(rows):
            y = 1.9 - i * 0.62
            e = np.log10(r["seconds"])
            w = max((e - lo) / (hi - lo) * W, 0.05)
            bar = Rectangle(width=w, height=0.38, stroke_width=0, fill_color=kc[r["kind"]], fill_opacity=0.85)
            bar.move_to([x0 + w / 2, y, 0])
            name = label(r["runtime"].replace("--", "-{}-"), font_size=18, color=WHITE)
            if name.width > 6.0:
                name.scale_to_fit_width(6.0)
            name.move_to([x0 - 0.2 - name.width / 2, y, 0])
            val = label(human_time(r["seconds"]), font_size=18, color=kc[r["kind"]]).next_to(bar, RIGHT, buff=0.12)
            bars.add(VGroup(name, bar, val))
        key = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=c, fill_opacity=0.85),
                              label(t, font_size=18, color=c)).arrange(RIGHT, buff=0.12)
                       for t, c in ((r"compiled ahead of time", YES), (r"compiled just in time", DATA),
                                    (r"interpreted", NO))]).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=1.0)
        note = label(r"log scale; \ the best of three runs; \ the same recursion, \ 7 million calls, \ in each",
                     font_size=18, color=GREY_B).to_edge(DOWN, buff=0.45)
        fast = min(r["seconds"] for r in rows if r["kind"] != "interp")
        slow = max(r["seconds"] for r in rows if r["kind"] == "interp")
        with self.voiceover(
            "How much does interpretation cost? We can measure it on the runtimes this machine has, running the "
            "same doubly recursive Fibonacci function, seven million calls, in each. <bookmark mark='a'/> At the "
            "top, programs compiled ahead of time: C, and Go. <bookmark mark='b'/> Then the just-in-time compilers: "
            "Java's HotSpot, and V8, the JavaScript engine in Chrome and Node. <bookmark mark='c'/> And at the "
            "bottom, the interpreters: Java and V8 with their compilers switched off, and CPython, which only "
            "interprets. The gap between the ends is a factor of more than fifty. <bookmark mark='d'/> The same "
            "language can sit on either side. JavaScript with V8's compilers is about nine times faster than the "
            "same JavaScript on V8's interpreter alone. Chapter eleven explains how."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            for k in ("aot",):
                self.play(*[FadeIn(b) for b, r in zip(bars, rows) if r["kind"] == k])
            vo.wait_until("b")
            self.play(*[FadeIn(b) for b, r in zip(bars, rows) if r["kind"] == "jit"])
            vo.wait_until("c")
            self.play(*[FadeIn(b) for b, r in zip(bars, rows) if r["kind"] == "interp"], FadeIn(key))
            vo.wait_until("d")
            self.play(*[Indicate(b[0], color=HEAD) for b, r in zip(bars, rows) if "JavaScript" in r["runtime"]])
        self.wait(0.3)
        self.clear_scene()
