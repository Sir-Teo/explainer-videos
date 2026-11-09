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
            label('a warm, correct BTB hit removes the modeled jump redirect; misses still cost', font_size=22,
                  color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Direction alone is not enough: fetch also needs a target. <bookmark mark='a'/> A branch target buffer, "
            "indexed by the program counter, remembers the kind and target of earlier control transfers. <bookmark "
            "mark='b'/> On a hit with a correct taken prediction and correct target, our ideal front end fetches from "
            "that target next cycle. On a miss it continues at pc plus four until a redirect. <bookmark mark='c'/> A "
            "warm, correct BTB hit can therefore remove the modeled unconditional-jump redirect cost. Cold misses, "
            "aliases, wrong indirect targets and real fetch-bandwidth constraints can still cost time. Free here is a "
            "condition of this model, not a universal property of jumps."
        ) as vo:
            self.play(FadeIn(head))
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
            label('push recognized calls, pop balanced returns; \\\\ a 16-entry stack helps here; overflow and recovery matter',
                  font_size=22, color=YES),
            label(r"the BTB alone remembers one target per return: \ the last one, \ usually wrong in recursion",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A return can have many targets. <bookmark mark='a'/> The same instruction returns to different callers, "
            "so remembering only its last target often fails in recursion. <bookmark mark='b'/> Recognized calls and "
            "returns normally nest: push the return address on a small front-end stack at each call and pop it at a "
            "return. <bookmark mark='c'/> A sixteen-entry stack works well on the balanced call patterns shown. Deeper "
            "nesting can discard entries; unusual control transfers, context switches and speculative repair also "
            "matter in real systems. Its residual misses must be measured rather than attributed to overflow from the "
            "count alone."
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
            "Run the same recursive Fibonacci program on three modeled front ends. <bookmark mark='a'/> With no target "
            "buffer, the table records redirects for jumps and returns. <bookmark mark='b'/> A BTB removes many jump "
            "redirects, but a last-target entry still misses many returns. <bookmark mark='c'/> Adding a sixteen-entry "
            "return stack cuts return misses to a few hundred and lowers CPI to about one point one two in this run. "
            "That comparison isolates the modeled front-end choices; it does not establish a universal return-miss "
            "rate or hardware speedup."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2]))
        self.wait(0.3)
        self.clear_scene()
