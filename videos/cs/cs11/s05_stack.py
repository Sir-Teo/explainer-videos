from __future__ import annotations

from math import factorial

from explainer.cs import *  # noqa: F403
from videos.cs.cs11.common import (BG, CODE, CTRL, DATA, FUNC, HEAD, NO, PART, YES, code, frame_box, grid_table,
                                   load, region)


class Stack(VoiceoverScene):
    def construct(self):
        self.card()
        self.convention()
        self.frame()
        self.fact()
        self.debugger()

    def card(self):
        card = chapter_card(4, r"The call stack", r"How can separately written functions call each other?",
                            part=PART)
        with self.voiceover("Chapter four. The call stack."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def convention(self):
        head = label(r"A calling convention: \ Pebble's", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"\texttt{a0} -- \texttt{a5}", r"arguments; \ \texttt{a0} the result", r"the caller"],
                [r"\texttt{ra}", r"the return address \ (\texttt{call} sets it)", r"the caller"],
                [r"\texttt{t0} -- \texttt{t3}", r"temporaries", r"the caller \ (caller-saved)"],
                [r"\texttt{s0} -- \texttt{s2}", r"long-lived values", r"the callee \ (callee-saved)"],
                [r"\texttt{sp}", r"the stack pointer: \ 16-byte aligned, \ grows down", r"everyone"]]
        colors = [[CODE, GREY_A, DATA]] * 2 + [[CODE, GREY_A, CTRL], [CODE, GREY_A, YES], [CODE, GREY_A, HEAD]]
        t = grid_table([r"registers", r"hold", r"must save them"], rows, [2.6, 5.2, 3.6], row_h=0.55, font_size=21,
                       colors=colors, mono_cols=()).move_to(UP * 0.4)
        why = VGroup(
            label(r"a contract, \ not a law of the hardware: \ every function compiled anywhere obeys it", font_size=21,
                  color=GREY_A),
            label(r"real ones: \ the System V ABI \ (Linux, \ macOS), \ Microsoft x64, \ the RISC-V psABI",
                  font_size=21, color=FUNC),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "For functions written separately, perhaps by different people with different compilers, to call each "
            "other, they must agree on the rules: a calling convention. Here is Pebble's. <bookmark mark='a'/> "
            "Arguments go in a0 to a5, and the result comes back in a0. The call instruction puts the return "
            "address in ra. <bookmark mark='b'/> The registers are split in two. t0 to t3 are temporaries: a "
            "function may destroy them, so a caller that needs one after a call must save it itself. s0 to s2 "
            "are the opposite: a function that wants to use one must save the old value and restore it before "
            "returning, so callers can rely on them. And the stack pointer stays aligned to sixteen bytes. "
            "<bookmark mark='c'/> None of this is enforced by the hardware. It is a contract, and real systems "
            "write theirs down: the System V application binary interface for Linux and macOS, Microsoft's for "
            "Windows, the RISC-V psABI."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*t.cells[1])), FadeIn(VGroup(*t.cells[2])))
            vo.wait_until("b")
            for r in (3, 4, 5):
                self.play(FadeIn(VGroup(*t.cells[r])), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    def frame(self):
        head = label(r"A stack frame: \ \texttt{lookup}'s", font_size=34).to_edge(UP, buff=0.3)
        lst = code(["lookup: addi sp, sp, -16    # make room", "        sw   ra, 12(sp)     # save what we will change",
                    "        sw   s0, 8(sp)", "        sw   s1, 4(sp)", "        sw   s2, 0(sp)",
                    "        ...                 # the body: may call alloc",
                    "        lw   s2, 0(sp)      # restore", "        lw   s1, 4(sp)", "        lw   s0, 8(sp)",
                    "        lw   ra, 12(sp)", "        addi sp, sp, 16     # give the room back",
                    "        ret"], size=17).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        cells = VGroup(*[frame_box(t, c, w=2.4, h=0.5) for t, c in (("ra", NO), ("s0", YES), ("s1", YES),
                                                                     ("s2", YES))]).arrange(DOWN, buff=0)
        caller = frame_box(r"main's frame \ (its word buffer)", GREY_B, w=2.4, h=0.8)
        stack = VGroup(caller, cells).arrange(DOWN, buff=0).to_edge(RIGHT, buff=1.4).shift(UP * 0.3)
        spl = VGroup(Arrow(LEFT * 0.6, ORIGIN, color=HEAD, buff=0, stroke_width=3),
                     label(r"sp", font_size=20, color=HEAD)).arrange(LEFT, buff=0.1).next_to(cells, LEFT, buff=0.1)
        spl.align_to(cells, DOWN)
        offs = VGroup(*[label(rf"{o}(sp)", font_size=16, color=GREY_B).next_to(c, RIGHT, buff=0.15)
                        for o, c in zip((12, 8, 4, 0), cells)])
        down = label(r"addresses fall \\ as the stack grows", font_size=17, color=GREY_B).next_to(stack, DOWN,
                                                                                               buff=0.2)
        with self.voiceover(
            "Here is what a function does with that contract. <bookmark mark='a'/> lookup will use s0, s1 and s2, "
            "and it calls alloc, which overwrites ra. So on entry it moves the stack pointer down sixteen bytes and "
            "saves all four there. That block is its stack frame, or activation record. <bookmark mark='b'/> Above "
            "it sits the frame of the function that called it, main, holding main's word buffer. <bookmark "
            "mark='c'/> On the way out, lookup restores the four registers, moves the stack pointer back up, and "
            "returns. Every call pushes a frame and every return pops one, so the stack always mirrors the chain of "
            "calls in progress."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lst))
            vo.wait_until("a")
            self.play(*[Indicate(lst[k], color=YES) for k in range(5)], FadeIn(cells), FadeIn(offs), FadeIn(spl))
            vo.wait_until("b")
            self.play(FadeIn(caller), FadeIn(down))
            vo.wait_until("c")
            self.play(*[Indicate(lst[k], color=CTRL) for k in range(6, 12)])
        self.wait(0.3)
        self.clear_scene()

    def fact(self):
        st = load("stack")["fact"]
        head = label(r"\texttt{fact(10)}, \ frame by frame", font_size=34).to_edge(UP, buff=0.3)
        frames = VGroup()
        for n in range(10, 0, -1):
            frames.add(frame_box(rf"fact({n}): \ n = {n}, \ ra", DATA if n % 2 else CTRL, w=2.8, h=0.38,
                                 font_size=15))
        frames.arrange(DOWN, buff=0).to_edge(LEFT, buff=1.2).shift(UP * 0.1)
        ax = Axes(x_range=[0, st["steps"], 20], y_range=[0, 180, 40], x_length=6.2, y_length=3.2, tips=False,
                  axis_config={"color": GREY_C, "font_size": 15}).to_edge(RIGHT, buff=0.6).shift(UP * 0.3)
        depth = st["depth"]
        curve = VMobject(color=HEAD, stroke_width=3).set_points_as_corners(
            [ax.c2p(k, d) for k, d in enumerate(depth)])
        xl = label(r"instructions", font_size=16, color=GREY_B).next_to(ax, DOWN, buff=0.2)
        yl = label(r"stack depth \ (bytes)", font_size=16, color=GREY_B).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        res = label(rf"result {st['result']:,} $= 10!$; \ deepest {st['deepest']} bytes \ $= 10$ frames of 16",
                    font_size=22, color=YES).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Watch it on a recursive function, the factorial. <bookmark mark='a'/> fact of ten calls fact of nine, "
            "which calls fact of eight, and so on down to one, each call pushing a frame holding its own n and its "
            "return address. <bookmark mark='b'/> Here is the stack's depth, measured on Pebble's emulator "
            "instruction by instruction: it climbs to ten frames, then, as each call returns and multiplies, it "
            "unwinds to nothing. <bookmark mark='c'/> The result is ten factorial, and the deepest the stack went "
            "was a hundred and sixty bytes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.1) for f in frames], lag_ratio=0.15), run_time=3)
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            self.play(Create(curve), LaggedStart(*[FadeOut(f) for f in reversed(frames)], lag_ratio=0.15),
                      run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def debugger(self):
        import re

        bt = load("backtrace")
        head = label(r"A debugger walks the same frames \ (gdb, \ this machine)", font_size=32).to_edge(UP, buff=0.3)
        lines = ["(gdb) bt"] + [re.sub(r" at /\S+/", " at ", l) for l in bt["bt"]]
        lst = code(lines, size=14).to_edge(LEFT, buff=0.4).shift(UP * 1.6)
        names = []
        for l in bt["bt"]:
            m = re.search(r"in (\w+) \(([^)]*)\)|^#0\s+(\w+) \(([^)]*)\)", l)
            names.append((m.group(1) or m.group(3), (m.group(2) or m.group(4)).split(",")[0]))
        boxes = VGroup()
        for k, (fn, arg) in enumerate(names):
            c = (DATA, CTRL)[k % 2] if fn == "fact" else GREY_C
            boxes.add(frame_box(rf"\texttt{{{fn}}}({arg.replace('_', r'\_')})", c, w=2.6, h=0.5, font_size=16))
        boxes = VGroup(*reversed(boxes)).arrange(DOWN, buff=0).to_edge(DOWN, buff=0.5).shift(LEFT * 0.4)
        boxes = VGroup(*reversed(boxes))           # index k = frame #k again, #0 at the bottom
        sps = VGroup(*[label(rf"\texttt{{sp = {sp:#x}}}", font_size=14, color=HEAD).next_to(b, LEFT, buff=0.2)
                       for b, sp in zip(boxes, bt["sp"])])
        fact_ra = bt["ra"][0]
        ras = VGroup()
        for b, ra in zip(boxes, bt["ra"]):
            where = r"in \texttt{fact}" if ra == fact_ra else (r"in \texttt{main}" if ra == bt["ra"][-2] else
                                                               r"in the C library")
            ras.add(label(rf"returns to \texttt{{{ra:#x}}} \ {where}", font_size=14,
                          color=GREY_A if ra == fact_ra else FUNC).next_to(b, RIGHT, buff=0.2))
        size = label(rf"{bt['frame_bytes']} bytes apart: \ one frame each", font_size=18, color=YES).next_to(
            sps, UP, buff=0.25).align_to(sps, LEFT)
        with self.voiceover(
            "A debugger reads the same structure on a real machine. <bookmark mark='a'/> We compiled a C "
            "factorial on this computer, ran it under gdb, and stopped it at its deepest call, fact of one. "
            "<bookmark mark='b'/> Asked for a backtrace, gdb lists six frames: five calls of fact and main. "
            "<bookmark mark='c'/> It finds them by walking the stack. Each frame keeps its caller's frame address "
            "and its own return address, so from the stack pointer the debugger can step from frame to frame. The "
            "stack pointers it reports are thirty-two bytes apart, one frame of fact each. <bookmark mark='d'/> "
            "And the saved return addresses tell the story of the calls: four of them point to the same "
            "instruction in fact, the one just after the recursive call; the fifth returns into main, and main's "
            "into the C library that started it. That is all a backtrace is."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lst[0]), FadeIn(lst[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l) for l in lst[2:]], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(t) for t in sps], lag_ratio=0.15), FadeIn(size), run_time=2)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(t) for t in ras], lag_ratio=0.2), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
