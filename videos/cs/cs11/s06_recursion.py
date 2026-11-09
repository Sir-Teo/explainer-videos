from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, grid_table, load, region)


class Recursion(VoiceoverScene):
    def construct(self):
        self.card()
        self.ackermann()
        self.tail()
        self.limits()

    def card(self):
        card = chapter_card(5, r"Recursion, \ depth and tail calls", r"How deep can the stack go?", lit=(1928,),
                            extra=((1928, r"Ackermann's function"),), part=PART)
        with self.voiceover("Chapter five. Recursion, depth, and tail calls."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ackermann(self):
        rows = load("ackermann")["rows"]
        head = label(r"Ackermann's function on Pebble", font_size=34).to_edge(UP, buff=0.3)
        defn = MathTex(r"A(0, n) = n + 1, \quad A(m, 0) = A(m-1, 1), \quad A(m, n) = A(m-1, A(m, n-1))",
                       font_size=32, color=HEAD).next_to(head, DOWN, buff=0.3)
        pick = [r for r in rows if (r["m"], r["n"]) in ((1, 5), (2, 3), (2, 5), (3, 1), (3, 3), (3, 4), (3, 5),
                                                        (3, 6))]
        body = [[rf"$A({r['m']}, {r['n']})$", f"{r['value']:,}", f"{r['calls']:,}", f"{r['frames']:,}"] for r in pick]
        colors = [[GREY_A, YES, CTRL, NO]] * len(body)
        t = grid_table([r"call", r"value", r"calls made", r"deepest stack \ (frames)"], body, [2.2, 1.8, 2.2, 3.2],
                       row_h=0.42, font_size=21, colors=colors, mono_cols=()).next_to(defn, DOWN, buff=0.4)
        cap = label(r"$A(4, 2)$ has 19,729 digits: \ no computer will ever finish it this way", font_size=21,
                    color=NO).to_edge(DOWN, buff=0.35)
        with self.voiceover("A small recursive definition can demand a large call tree. <bookmark mark='a'/> This two-argument Ackermann variant has three rules. As a function of both arguments it is computable but not primitive recursive: no fixed nesting of bounded loops computes all its values. That is a computability classification, not a ban on while-loop implementations. <bookmark mark='b'/> Our Pebble run for A of three, six returns 509 after 172,233 calls, with 511 frames at maximum depth. Work counts every call; depth counts only the longest active chain. <bookmark mark='c'/> A of four, two equals two to the 65,536 minus three, a value with 19,729 decimal digits. The experiment demonstrates both enormous work and stack demand; it does not compute that larger case by naive recursion.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(Write(defn), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule), LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.25), run_time=3)
            vo.wait_until('c')
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def tail(self):
        st = load("stack")
        a, b = st["sum"], st["sum_tail"]
        head = label("An eligible tail call can reuse a frame", font_size=34).to_edge(UP, buff=0.3)
        src = VGroup(code(["sum(n, acc):", "    if n == 0: return acc", "    return sum(n - 1, acc + n)"], size=19,
                          color=YES),
                     label(r"the recursive call is the last thing it does", font_size=19, color=GREY_A)).arrange(
            DOWN, buff=0.15, aligned_edge=LEFT).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.8)
        two = VGroup(code(["call sum      # push a frame", "...", "ret"], size=17),
                     code(["j    sum      # just jump", "", ""], size=17)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        two.next_to(src, RIGHT, buff=1.0).align_to(src, UP)
        ax = Axes(x_range=[0, a["steps"], 200], y_range=[0, 1800, 400], x_length=8.0, y_length=2.8, tips=False,
                  axis_config={"color": GREY_C, "font_size": 15}).to_edge(DOWN, buff=0.8)
        c1 = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax.c2p(k, d) for k, d in enumerate(a["depth"])])
        c2 = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(k, d) for k, d in enumerate(b["depth"])])
        l1 = label(rf"as a call: \ {a['deepest']:,} bytes of stack, \ {a['steps']:,} instructions", font_size=18,
                   color=NO).next_to(ax.c2p(a["steps"] * 0.5, 1650), UP, buff=0.05)
        l2 = label(rf"as a jump: \ {b['deepest']} bytes, \ {b['steps']:,} instructions", font_size=18,
                   color=YES).next_to(ax.c2p(b["steps"], 0), UR, buff=0.1)
        yl = label(r"stack depth, \ $n = 100$", font_size=16, color=GREY_B).next_to(ax, LEFT, buff=0.1).shift(UP * 0.9)
        with self.voiceover(f"A tail call can reuse a frame when nothing remains to do after it. <bookmark mark='a'/> This recursive call returns its result directly: no addition, cleanup or other pending operation follows it. <bookmark mark='b'/> In this Pebble example the arguments can be updated and control can jump back without saving another return address. General tail calls also have to respect calling conventions and language cleanup rules. <bookmark mark='c'/> Our ordinary sum uses {a['deepest']:,} bytes of stack and {a['steps']:,} instructions; this hand-written tail version uses no additional stack. Scheme requires proper tail recursion. C compilers may optimize eligible calls, but the language does not guarantee it. CPython does not generally eliminate Python tail-call frames.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(src), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(two))
            vo.wait_until('c')
            self.play(Create(ax), FadeIn(yl))
            self.play(Create(c1), FadeIn(l1), run_time=2)
            self.play(Create(c2), FadeIn(l2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    def limits(self):
        head = label(r"When the stack runs out", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label("stack size is configurable; \\\\ 8 MiB Linux main-stack and 1 MiB Windows defaults are common examples",
                  font_size=22, color=GREY_A),
            label(r"below it, \ an unmapped \textit{guard page}: \ touching it is a segmentation fault", font_size=22,
                  color=NO),
            label("CPython: configurable recursion limit, commonly near 1000; Java: StackOverflowError", font_size=22,
                  color=GREY_A),
            label(r"mutual recursion counts too: \ \texttt{even(n)} calls \texttt{odd(n-1)} calls \texttt{even(n-2)} "
                  r"\dots", font_size=22, color=DATA),
            label(r"the cure: \ an explicit stack on the heap, \ or a loop", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        if pts.width > 8.4:
            pts.scale_to_fit_width(8.4)
        pts.to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        # the address space around one thread's stack
        top = region(2.2, 0.6, r"caller frames", GREY_C, font_size=16, fill=0.08)
        stk = Rectangle(width=2.2, height=3.4, stroke_color=NO, stroke_width=2, fill_opacity=0)
        guard = region(2.2, 0.55, r"guard page", NO, font_size=16, fill=0.35)
        other = region(2.2, 0.8, r"other mappings", GREY_C, font_size=16, fill=0.08)
        col = VGroup(top, stk, guard, other).arrange(DOWN, buff=0).to_edge(RIGHT, buff=1.3).shift(DOWN * 0.2)
        size = label(r"8 MiB", font_size=20, color=NO).next_to(stk, LEFT, buff=0.15)
        nf = 10
        fh = stk.height / nf
        frames = VGroup(*[Rectangle(width=2.2, height=fh, stroke_color=GREY_D, stroke_width=1,
                                    fill_color=(DATA, CTRL)[k % 2], fill_opacity=0.45)
                          .move_to(stk.get_top() + DOWN * fh * (k + 0.5)) for k in range(nf)])
        extra = Rectangle(width=2.2, height=fh, stroke_color=NO, stroke_width=2, fill_color=NO,
                          fill_opacity=0.6).move_to(guard.get_top() + DOWN * fh / 2)
        boom = label(r"\texttt{SIGSEGV}", font_size=22, color=NO).next_to(guard, LEFT, buff=0.15)
        with self.voiceover(
            (
            "Stack limits depend on the process, thread and runtime. <bookmark mark='a'/> Eight megabytes is a "
            "common Linux soft limit for the main thread's stack, and one megabyte a common Windows executable "
            "default; neither is a universal constant, and thread stacks can be configured. <bookmark mark='b'/> "
            "Guard pages can make an access beyond a stack boundary fault. Large unchecked jumps can skip a "
            "guard, so stack probing and stack-clash protections matter too. <bookmark mark='c'/> CPython has a "
            "configurable recursion limit, commonly around a thousand. Java can report StackOverflowError; the "
            "available depth depends on stack size and frame sizes. <bookmark mark='d'/> Mutual recursion "
            "consumes frames just as direct recursion does. <bookmark mark='e'/> An explicit heap worklist or an "
            "iterative algorithm can control call-stack growth, but it still needs memory for pending work."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(col))
            vo.wait_until("a")
            self.play(FadeIn(pts[0], shift=RIGHT * 0.1), FadeIn(size))
            self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pts[1], shift=RIGHT * 0.1), FadeIn(extra))
            self.play(FadeIn(boom), Indicate(guard, color=NO))
            for mk, p in zip("cde", pts[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
