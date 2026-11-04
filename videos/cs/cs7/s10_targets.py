from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs7.common import (BG, CLOCK, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, box, fmt,
                                  load, mono)


class Targets(VoiceoverScene):
    def construct(self):
        self.card()
        self.btb()
        self.ras()
        self.measured()

    def card(self):
        card = chapter_card(9, r"Where the branch goes", r"Knowing it is taken is not enough", part=PART)
        with self.voiceover("Chapter nine. Where the branch goes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def btb(self):
        head = label(r"The branch target buffer", font_size=38).to_edge(UP, buff=0.35)
        rows = [("0x0094", "branch", "0x00b4"), ("0x00a8", "jal", "0x0090"), ("0x00c0", "return", "stack"),
                ("0x0170", "branch", "0x0128")]
        tab = VGroup()
        for k, r in enumerate([("pc", "kind", "target")] + rows):
            row = VGroup(*[Text(t, font="DejaVu Sans Mono", font_size=20, color=GREY_B if k == 0 else
                                [DATA, CTRL, HEAD][j]) for j, t in enumerate(r)]).arrange(RIGHT, buff=0.7)
            tab.add(row)
        tab.arrange(DOWN, buff=0.18).move_to(RIGHT * 2.8 + UP * 0.6)
        frame = SurroundingRectangle(tab[1:], buff=0.15, color=GREY_C)
        pc = mono("pc = 0x00a8", 22, DATA).move_to(LEFT * 4.0 + UP * 1.4)
        arr = Arrow(pc.get_right(), tab[2].get_left(), buff=0.2, color=HEAD)
        nx = mono("next pc = 0x0090", 22, YES).move_to(LEFT * 4.0 + DOWN * 0.2)
        notes = VGroup(
            label(r"in IF, \ before the instruction is even decoded: \ is this a branch or jump, \ and where to?",
                  font_size=22, color=GREY_A),
            label(r"a hit, \ predicted taken: \ fetch from the target next cycle; \ a miss: \ \texttt{pc} $+ 4$",
                  font_size=22, color=GREY_A),
            label(r"so even a \texttt{jal}, \ always taken, \ costs nothing once it is in the buffer", font_size=22,
                  color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A prediction of taken is useless without the target address, and the target is computed from the "
            "instruction's bits, which the fetch stage has not decoded yet. <bookmark mark='a'/> So the fetch stage "
            "consults a second small memory, the branch target buffer, indexed by the program counter. Each entry "
            "remembers that the instruction at this address was a branch or jump, of what kind, and where it went. "
            "<bookmark mark='b'/> On a hit, the predictor decides taken or not, and if taken, the next fetch comes from "
            "the stored target, in the very next cycle. On a miss, fetch simply continues at pc plus four. "
            "<bookmark mark='c'/> That makes unconditional jumps free too. A jal is always taken, but without the buffer "
            "even it would waste a cycle while decode works out the target."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(frame), FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(pc), GrowArrow(arr), Indicate(tab[2], color=HEAD))
            self.play(FadeIn(nx), FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ras(self):
        head = label(r"Returns go to different places", font_size=38).to_edge(UP, buff=0.35)
        code = VGroup(*[mono(t, 19) for t in ("main:  call fib      # returns to A", "A:     ...",
                                              "       call fib      # returns to B", "B:     ...",
                                              "fib:   ...", "       ret           # to A?  to B?  to fib itself?")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to(LEFT * 3.0 + UP * 0.8)
        stack = VGroup(*[Rectangle(width=1.8, height=0.45, stroke_color=HEAD, stroke_width=1.5) for _ in range(5)]
                       ).arrange(UP, buff=0.0).move_to(RIGHT * 3.4 + UP * 0.3)
        sl = label(r"return-address stack", font_size=22, color=HEAD).next_to(stack, UP, buff=0.15)
        vals = ["A", "fib+40", "fib+40"]
        items = VGroup(*[MathTex(rf"\texttt{{{v}}}", font_size=22, color=YES).move_to(stack[k]) for k, v in
                         enumerate(vals)])
        notes = VGroup(
            label(r"a return's target is the call's \texttt{pc} $+ 4$, \ and calls nest: \ last called, \ first returned",
                  font_size=22, color=GREY_A),
            label(r"push on every call, \ pop on every return: \ a 16-entry stack predicts nearly all of them",
                  font_size=22, color=YES),
            label(r"the BTB alone remembers one target per return: \ the last one, \ usually wrong in recursion",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One kind of jump defeats the target buffer: the return from a function. <bookmark mark='a'/> The same "
            "return instruction goes back to wherever the function was called from, a different place each time, and "
            "in a recursive function like Fibonacci, sometimes into the function itself. A buffer that remembers the "
            "last target is usually wrong. <bookmark mark='b'/> But calls and returns nest: the last function called is "
            "the first to return. So keep a small stack in the fetch stage. Every call pushes its return address; every "
            "return pops one and uses it as the prediction. <bookmark mark='c'/> A sixteen-entry stack predicts nearly "
            "every return, unless the recursion goes deeper than sixteen calls."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(FadeIn(notes[2]))
            vo.wait_until("b")
            self.play(FadeIn(stack), FadeIn(sl))
            for it in items:
                self.play(FadeIn(it, shift=DOWN * 0.3), run_time=0.5)
            self.play(FadeOut(items[-1], shift=UP * 0.3))
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        b = load("btbras")
        head = label(r"Fibonacci of 18, \ three front ends", font_size=36).to_edge(UP, buff=0.35)
        names = list(b)
        scale = 5.0 / max(v["cpi"] for v in b.values())
        rows = VGroup()
        for k, n in enumerate(names):
            v = b[n]
            y = 1.3 - 1.0 * k
            nl = label(n, font_size=22, color=GREY_A).move_to([-2.4, y, 0], aligned_edge=RIGHT)
            r = Rectangle(width=v["cpi"] * scale, height=0.45, stroke_width=0, fill_color=[NO, HEAD, YES][k],
                          fill_opacity=0.65).move_to([-2.2 + v["cpi"] * scale / 2, y, 0])
            vl = label(rf"CPI {v['cpi']:.2f}; \ returns mispredicted {fmt(v['jalr_miss'])} of {fmt(v['jalr'])}",
                       font_size=18, color=GREY_A).next_to(r, RIGHT, buff=0.15)
            rows.add(VGroup(nl, r, vl))
        note = label(r"the same program, \ the same predictor for conditional branches; \ only the front end differs",
                     font_size=22, color=GREY_B).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is recursive Fibonacci of eighteen, eighty-eight thousand instructions with eight thousand returns, "
            "on three front ends. <bookmark mark='a'/> With no target buffer, every taken jump and every return costs a "
            "redirect: CPI one point four eight. <bookmark mark='b'/> A target buffer fixes the jumps, but still "
            "mispredicts most returns. <bookmark mark='c'/> Add the return-address stack and only a few hundred returns "
            "go wrong, the ones deeper than its sixteen entries: CPI one point one two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
        self.wait(0.3)
        self.clear_scene()
