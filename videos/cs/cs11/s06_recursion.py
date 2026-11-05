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
        with self.voiceover(
            "Recursion can make the stack enormous. <bookmark mark='a'/> Wilhelm Ackermann's function, from 1928, is "
            "defined by three short rules, and Part 25 explains why it matters: it is computable, but it grows "
            "faster than anything a fixed number of loops can compute. <bookmark mark='b'/> We ran it on Pebble. "
            "A of three, six is just five hundred and nine, but computing it takes a hundred and seventy-two "
            "thousand calls, and at its deepest the stack holds five hundred and eleven frames. Each step up in n "
            "roughly quadruples the calls and doubles the depth. <bookmark mark='c'/> A of four, two has nearly "
            "twenty thousand digits. Recursion like this is limited not by time alone but by the stack."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(defn))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule),
                      LaggedStart(*[FadeIn(VGroup(*t.cells[r])) for r in range(1, len(t.cells))], lag_ratio=0.25),
                      run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.3)
        self.clear_scene()

    def tail(self):
        st = load("stack")
        a, b = st["sum"], st["sum_tail"]
        head = label(r"A tail call needs no frame", font_size=34).to_edge(UP, buff=0.3)
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
        with self.voiceover(
            "Some recursion can be made free. <bookmark mark='a'/> Here the recursive call is the very last thing "
            "the function does; its result is returned unchanged. That is a tail call. <bookmark mark='b'/> There "
            "is then no reason to come back: the frame holds nothing anyone needs. So instead of calling, the "
            "function can simply jump to itself, and when the innermost one returns, it returns straight to the "
            "original caller. <bookmark mark='c'/> On Pebble, summing a hundred numbers the first way uses "
            f"{a['deepest']:,} bytes of stack and {a['steps']:,} instructions; the second, no stack at all and less than half "
            "the instructions. Scheme requires this optimization; C compilers do it when they can, as the jump "
            "table of the last chapter showed; Python, deliberately, never does."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(src))
            vo.wait_until("b")
            self.play(FadeIn(two))
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(yl))
            self.play(Create(c1), FadeIn(l1), run_time=2)
            self.play(Create(c2), FadeIn(l2), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    def limits(self):
        head = label(r"When the stack runs out", font_size=34).to_edge(UP, buff=0.35)
        pts = VGroup(
            label(r"a thread's stack is fixed when it starts: \ 8 MB by default on Linux, \ 1 MB on Windows",
                  font_size=22, color=GREY_A),
            label(r"below it, \ an unmapped \textit{guard page}: \ touching it is a segmentation fault", font_size=22,
                  color=NO),
            label(r"Python stops at 1000 frames by default; \ Java throws \texttt{StackOverflowError}", font_size=22,
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
        size = label(r"8 MB", font_size=20, color=NO).next_to(stk, LEFT, buff=0.15)
        nf = 10
        fh = stk.height / nf
        frames = VGroup(*[Rectangle(width=2.2, height=fh, stroke_color=GREY_D, stroke_width=1,
                                    fill_color=(DATA, CTRL)[k % 2], fill_opacity=0.45)
                          .move_to(stk.get_top() + DOWN * fh * (k + 0.5)) for k in range(nf)])
        extra = Rectangle(width=2.2, height=fh, stroke_color=NO, stroke_width=2, fill_color=NO,
                          fill_opacity=0.6).move_to(guard.get_top() + DOWN * fh / 2)
        boom = label(r"\texttt{SIGSEGV}", font_size=22, color=NO).next_to(guard, LEFT, buff=0.15)
        with self.voiceover(
            "What happens when the stack runs out? <bookmark mark='a'/> A thread's stack has a fixed size, chosen "
            "when it starts: eight megabytes by default on Linux, one on Windows. <bookmark mark='b'/> Below it the "
            "operating system leaves a guard page that is not mapped at all, so running past the end is caught as "
            "a segmentation fault rather than silently trampling other memory. <bookmark mark='c'/> Languages "
            "with their own runtimes catch it earlier: Python stops at a thousand frames, Java throws a stack "
            "overflow error. <bookmark mark='d'/> Two functions calling each other count just as much as one "
            "calling itself. <bookmark mark='e'/> The cure for deep recursion is to keep the pending work in an "
            "explicit stack on the heap, or to turn it into a loop."
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
