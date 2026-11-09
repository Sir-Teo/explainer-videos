from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, load)


class Control(VoiceoverScene):
    def construct(self):
        self.card()
        self.branches()
        self.switch()

    def card(self):
        card = chapter_card(3, r"Control flow in machine code", r"What do if, while and switch become?", part=PART)
        with self.voiceover("Chapter three. Control flow in machine code."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def branches(self):
        head = label(r"Ifs and loops are branches", font_size=34).to_edge(UP, buff=0.3)
        src = code(["if (c >= 'A' && c <= 'Z')", "    c = c + 32;",
                    "while (node != 0) {", "    ...", "    node = node->next;", "}"], size=19, color=YES)
        asm = code(["        addi t0, a0, -65     # c - 'A'", "        sltiu t1, t0, 26     # 0 <= c-'A' < 26 ?",
                    "        beqz t1, lower       # no: skip", "        addi a0, a0, 32", "lower:  ...",
                    "scan:   beqz t0, new         # node == 0: leave", "        ...",
                    "        lw   t0, 0(t0)       # node = node->next", "        j    scan"], size=17)
        VGroup(src, asm).arrange(RIGHT, buff=0.9, aligned_edge=UP).next_to(head, DOWN, buff=0.5)
        pts = VGroup(
            label(r"an \texttt{if}: \ a conditional branch around the body", font_size=21, color=GREY_A),
            label(r"a loop: \ a test at the top, \ a jump back at the bottom", font_size=21, color=GREY_A),
            label(r"a range test in two instructions: \ subtract, \ then compare unsigned", font_size=21,
                  color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover("Structured control flow disappears in machine code: everything becomes a branch. <bookmark mark='a'/> Here are two pieces of the Job, in C-like source on the left and Pebble on the right. <bookmark mark='b'/> An if becomes a conditional branch around its body. And notice the trick for the range test: subtract A, and then one unsigned comparison against 26 asks both questions at once, because anything below A wraps round to a huge unsigned number. Compilers do this routinely. <bookmark mark='c'/> A loop becomes a test at the top that leaves, and a jump back at the bottom.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(src), FadeIn(asm), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until('b')
            self.play(FadeIn(pts[0]), FadeIn(pts[2]), *[Indicate(asm[k], color=DATA) for k in range(4)])
            vo.wait_until('c')
            self.play(FadeIn(pts[1]), *[Indicate(asm[k], color=CTRL) for k in (5, 7, 8)])
        self.wait(0.3)
        self.clear_scene()

    def switch(self):
        sw = load("switch")
        head = label(r"A switch becomes a table of jumps \ (gcc -O2, \ this machine)", font_size=32).to_edge(
            UP, buff=0.3)
        import re
        lines = []
        for l in sw["source"].splitlines()[1:]:
            parts = [p.strip() for p in re.split(r"(?=case \d)", l) if p.strip()]
            ind = re.match(r"\s*", l).group(0)
            lines += [ind + p for p in parts] if len(parts) > 1 else [l]
        src = code(lines, size=16, color=YES)
        keep = [l for l in sw["asm"] if not l.strip().startswith((".section", ".align"))][:24]
        asm = code([l.replace("\t", "  ") for l in keep], size=15)
        if asm.height > 6.2:
            asm.scale_to_fit_height(6.2)
        asm.to_edge(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.3).to_edge(RIGHT, buff=0.6)
        src.to_edge(LEFT, buff=0.7).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.7)
        notes = VGroup(
            label(r"1. \ is \texttt{c} between 0 and 7? \ if not, \ return", font_size=19, color=GREY_A),
            label(r"2. \ load entry \texttt{c} of the table \texttt{.L4}", font_size=19, color=DATA),
            label("3. \\ in-range case: add base and offset, then one indirect jump", font_size=19,
                  color=CTRL),
            label(r"each case ends in \texttt{jmp}, \ not \texttt{call}: \ a tail call \ (chapter 5)", font_size=19,
                  color=FUNC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(src, DOWN, buff=0.5).align_to(src, LEFT)
        with self.voiceover("Dense switch cases can use a jump table. <bookmark mark='a'/> This is the actual gcc output for eight cases on our x86-64 host. Different targets, options and case patterns can produce a different lowering. <bookmark mark='b'/> One unsigned bounds comparison rejects values outside zero through seven. <bookmark mark='c'/> The code loads a signed relative offset from the table, then adds the table's base address. Computing an address with lea is not a second data-memory load. <bookmark mark='d'/> An indirect jump transfers control to the selected case. The instruction count alone does not determine latency: prediction and memory matter too. <bookmark mark='e'/> Each case ends with a jump to its function because that call is in tail position. Its result goes straight back to our caller; chapter five explains when this transformation is valid.") as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(src), FadeIn(asm), run_time=0.6)
            vo.wait_until('a')
            for mk, n in zip('bcde', notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.3)
        self.clear_scene()
