from __future__ import annotations

import itertools

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart,
                                   grid_table, load, mono, timeline)


class Consistency(VoiceoverScene):
    def construct(self):
        self.card()
        self.sc()
        self.interleavings()
        self.buffer()
        self.measured()
        self.models()

    def card(self):
        card = chapter_card(5, r"Memory consistency", r"In what order do other cores see my writes?", lit=(1979,),
                            extra=((1979, r"Lamport: \ sequential consistency"),), part=PART)
        with self.voiceover("Chapter five. Memory consistency."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def sc(self):
        head = label(r"Sequential consistency \ (Lamport, \ 1979)", font_size=34).to_edge(UP, buff=0.35)
        quote = wrapped_label(r"``the result of any execution is the same as if the operations of all the processors "
                              r"were executed in some sequential order, \ and the operations of each individual "
                              r"processor appear in this sequence in the order specified by its program''", 11.0,
                              font_size=24, color=GREY_A).next_to(head, DOWN, buff=0.4)
        t0 = timeline(["x = 1", "r0 = y"], CORE_COLORS[0], -4.0, -0.4)
        t1 = timeline(["y = 1", "r1 = x"], CORE_COLORS[1], -4.0, -1.3)
        n0 = label(r"thread 0", font_size=20, color=CORE_COLORS[0]).next_to(t0, LEFT, buff=0.3)
        n1 = label(r"thread 1", font_size=20, color=CORE_COLORS[1]).next_to(t1, LEFT, buff=0.3)
        init = label(r"$x$ and $y$ start at 0", font_size=20, color=GREY_B).next_to(VGroup(t0, t1), RIGHT, buff=0.6)
        q = label(r"can both threads read 0?", font_size=28, color=HEAD).to_edge(DOWN, buff=0.6)
        coh = note(r"coherence is about one address; \ consistency is about the order of accesses to different "
                   r"addresses", font_size=18).next_to(q, DOWN, buff=0.15)
        with self.voiceover(
            "Coherence is about one address at a time. But programs communicate through several: write the data, then "
            "set a flag. In what order do other cores see those writes? <bookmark mark='a'/> In 1979 Leslie Lamport "
            "gave the answer programmers assume without thinking. A multiprocessor is sequentially consistent if "
            "every execution gives the same result as some single interleaving of all the threads' operations, with "
            "each thread's operations in its program order. <bookmark mark='b'/> Here is the test that probes it, "
            "called store buffering. Thread zero sets x to one, then reads y. Thread one sets y to one, then reads x. "
            "Both start at zero. <bookmark mark='c'/> Can both threads read zero?"
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(quote), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(t0), FadeIn(t1), FadeIn(n0), FadeIn(n1), FadeIn(init))
            vo.wait_until("c")
            self.play(FadeIn(q), FadeIn(coh))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def interleavings(self):
        head = label(r"Every interleaving \ that keeps program order", font_size=34).to_edge(UP, buff=0.3)
        ops0 = [("x = 1", 0), ("r0 = y", 0)]
        ops1 = [("y = 1", 1), ("r1 = x", 1)]
        rows = VGroup()
        for pick in itertools.combinations(range(4), 2):
            seq, a, b = [], 0, 0
            for k in range(4):
                if k in pick:
                    seq.append(ops0[a]); a += 1
                else:
                    seq.append(ops1[b]); b += 1
            mem, reg = {"x": 0, "y": 0}, {}
            for t, _ in seq:
                lhs, rhs = [s.strip() for s in t.split("=")]
                if rhs.isdigit():
                    mem[lhs] = int(rhs)
                else:
                    reg[lhs] = mem[rhs]
            row = VGroup(*[VGroup(RoundedRectangle(width=1.25, height=0.45, corner_radius=0.06,
                                                   stroke_color=CORE_COLORS[c], stroke_width=2, fill_color=BG,
                                                   fill_opacity=1),
                                  Text(t, font="DejaVu Sans Mono", font_size=16, color=WHITE)) for t, c in seq])
            for r in row:
                r[1].move_to(r[0])
            row.arrange(RIGHT, buff=0.12)
            res = label(rf"r0 = {reg['r0']}, \ r1 = {reg['r1']}", font_size=22,
                        color=YES if reg["r0"] or reg["r1"] else NO).next_to(row, RIGHT, buff=0.5)
            rows.add(VGroup(row, res))
        rows.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(DOWN * 0.2 + LEFT * 0.5)
        sim = load("litmus")["simulated"]["sc"]
        punch = label(r"six interleavings, \ and in every one some store comes first: \ never r0 = r1 = 0",
                      font_size=24, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Under sequential consistency we can simply list the possibilities. Each thread's two operations stay in "
            "order, and the four can be interleaved in six ways. <bookmark mark='a'/> Here they are, with what each "
            "thread reads. <bookmark mark='b'/> In every one of them, one of the two stores comes first, and the other "
            "thread's load comes after it, so at least one thread reads one. Both reading zero is impossible. Our "
            "simulator, running two hundred thousand random interleavings, agrees: it never happens."
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=0.6)
            vo.wait_until('a')
            vo.wait_until("b")
            self.play(FadeIn(punch))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def buffer(self):
        head = label(r"Store buffers break it", font_size=34).to_edge(UP, buff=0.3)
        cores = VGroup()
        bufs = []
        for k, x in ((0, -3.2), (1, 3.2)):
            c = VGroup(RoundedRectangle(width=2.4, height=0.8, corner_radius=0.1, stroke_color=CORE_COLORS[k],
                                        stroke_width=2.4),
                       label(rf"core {k}", font_size=22, color=CORE_COLORS[k])).move_to([x, 1.7, 0])
            c[1].move_to(c[0])
            b = VGroup(*[Rectangle(width=0.8, height=0.45, stroke_color=GREY_C, stroke_width=1.5) for _ in range(3)]
                       ).arrange(RIGHT, buff=0).move_to([x, 0.55, 0])
            bl = label(r"store buffer", font_size=17, color=GREY_B).next_to(b, LEFT, buff=0.15)
            cores.add(c, b, bl)
            bufs.append(b)
        mem = VGroup(RoundedRectangle(width=5.0, height=0.8, corner_radius=0.1, stroke_color=GREY_B),
                     Text("x = 0    y = 0", font="DejaVu Sans Mono", font_size=22, color=WHITE)).move_to(DOWN * 1.2)
        mem[1].move_to(mem[0])
        ml = label(r"caches and memory, \ coherent", font_size=18, color=GREY_B).next_to(mem, DOWN, buff=0.1)
        st0 = Text("x=1", font="DejaVu Sans Mono", font_size=18, color=DATA).move_to(cores[0])
        st1 = Text("y=1", font="DejaVu Sans Mono", font_size=18, color=CTRL).move_to(cores[3])
        r0 = label(r"r0 = 0", font_size=24, color=NO).next_to(cores[0], RIGHT, buff=0.2)
        r1 = label(r"r1 = 0", font_size=24, color=NO).next_to(cores[3], LEFT, buff=0.2)
        p0 = Arrow(mem.get_top() + LEFT * 1.2, cores[0].get_bottom() + RIGHT * 0.6, color=GREY_A, buff=0.05,
                   stroke_width=2.5)
        p1 = Arrow(mem.get_top() + RIGHT * 1.2, cores[3].get_bottom() + LEFT * 0.6, color=GREY_A, buff=0.05,
                   stroke_width=2.5)
        mem2 = Text("x = 1    y = 1", font="DejaVu Sans Mono", font_size=22, color=WHITE).move_to(mem[0])
        why = label(r"a store waits in the buffer for its line; \ the core's next loads go ahead", font_size=22,
                    color=GREY_A).to_edge(DOWN, buff=0.75)
        tso = label(r"\textit{total store order} \ (x86): \ stores leave in order, \ but a load may pass an earlier "
                    r"store", font_size=22, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            (
            "Real processors do not wait for stores. <bookmark mark='a'/> When a core executes a store, it puts "
            "the address and value in a small queue, the store buffer, and carries on; the store reaches the "
            "cache when its line arrives, perhaps a hundred cycles later. Part 8's teaching core also used "
            "buffered stores, without implementing a complete multicore TSO model. <bookmark mark='b'/> So thread "
            "zero's store of x sits in core zero's buffer, and thread one's store of y in core one's. <bookmark "
            "mark='c'/> Now each core loads the other variable. Neither store has reached memory, so both loads "
            "read zero. <bookmark mark='d'/> Then the buffers drain, and memory ends with both ones, too late. "
            "Each core still sees its own store, because its loads check its own buffer first. But other cores "
            "see it late. <bookmark mark='e'/> This is the memory model of x86, called total store order: stores "
            "become visible in program order, but a load can overtake an earlier store to a different address."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(cores), FadeIn(mem), FadeIn(ml))
            vo.wait_until("a")
            self.play(FadeIn(why))
            vo.wait_until("b")
            self.play(FadeIn(st0), FadeIn(st1))
            self.play(st0.animate.move_to(bufs[0][0]), st1.animate.move_to(bufs[1][0]))
            vo.wait_until("c")
            self.play(GrowArrow(p0), GrowArrow(p1))
            self.play(FadeIn(r0), FadeIn(r1))
            vo.wait_until("d")
            self.play(st0.animate.move_to(mem[0].get_left() + RIGHT * 1.0), st1.animate.move_to(
                mem[0].get_right() + LEFT * 1.0), FadeOut(p0), FadeOut(p1))
            self.play(FadeOut(st0), FadeOut(st1), Transform(mem[1], mem2))
            vo.wait_until("e")
            self.play(FadeOut(why), FadeIn(tso))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def measured(self):
        lt = load("litmus")
        n = lt["trials"]
        head = label(rf"The litmus test, \ run {n:,} times on this computer", font_size=32).to_edge(UP, buff=0.3)
        keys = ["r0=0, r1=0", "r0=0, r1=1", "r0=1, r1=0", "r0=1, r1=1"]
        names = [r"both 0", r"r0 = 0, \ r1 = 1", r"r0 = 1, \ r1 = 0", r"both 1"]
        plain = [lt["plain"][k] / n for k in keys]
        fence = [lt["mfence"][k] / n for k in keys]
        c1 = bar_chart(plain, names, [NO, GREY_B, GREY_B, GREY_B], height=2.6, bar_w=0.8, gap=0.5, vmax=1.0,
                       font_size=17, fmt_=lambda v: rf"{100 * v:.1f}\%")
        c2 = bar_chart(fence, names, [YES, GREY_B, GREY_B, GREY_B], height=2.6, bar_w=0.8, gap=0.5, vmax=1.0,
                       font_size=17, fmt_=lambda v: rf"{100 * v:.1f}\%")
        VGroup(c1, c2).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.4)
        t1 = label(r"relaxed atomic loads and stores", font_size=21, color=NO).next_to(c1, UP, buff=0.4)
        t2 = VGroup(label(r"with a fence between them", font_size=22, color=YES),
                    Text("x = 1;  mfence;  r0 = y;", font="DejaVu Sans Mono", font_size=16, color=CODE)).arrange(
            DOWN, buff=0.08).next_to(c2, UP, buff=0.25)
        both = lt["plain"]["r0=0, r1=0"]
        punch = label(rf"{both:,} times, \ both threads read 0: \ impossible under sequential consistency", font_size=23,
                      color=HEAD).to_edge(DOWN, buff=0.3)
        note_ = note(r"how often depends on timing: \ the threads start each trial together, \ so their loads race "
                     r"their stores", font_size=16).next_to(punch, UP, buff=0.1)
        with self.voiceover(
            f"We ran this test a million times with two worker threads. They are released each trial by an acquire-release handshake, without pinning them to particular cores. <bookmark mark='a'/> The shared x and y use separate relaxed atomic loads and stores: these are defined C operations, not volatile data races. Both reads were zero in {both:,} trials. The observed frequency depends on timing and scheduling; an allowed outcome need not appear in every run. <bookmark mark='b'/> The second run inserts x86 mfence after each worker's store. Under the stated ordinary-memory assumptions, that blocks this store-buffering outcome. The chart reports what was observed. A fence here orders these accesses; arbitrary fences do not automatically make a whole C or C++ program sequentially consistent."
        ) as vo:
            self.play(FadeIn(head), run_time=0.5)
            self.play(FadeIn(t1), FadeIn(c1[0]), FadeIn(c1.names), *[GrowFromEdge(b, DOWN) for b in c1.bars], FadeIn(c1.vals), run_time=0.6)
            vo.wait_until('a')
            self.play(FadeIn(punch), FadeIn(note_))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(c2[0]), FadeIn(c2.names), *[GrowFromEdge(b, DOWN) for b in c2.bars],
                      FadeIn(c2.vals))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def models(self):
        head = label(r"Which reorderings each machine allows", font_size=34).to_edge(UP, buff=0.3)
        hdr = [r"", r"load, \ load", r"load, \ store", r"store, \ store", r"store, \ load"]
        Y, N_ = r"kept", r"may swap"
        rows = [[r"sequential consistency", Y, Y, Y, Y], [r"x86 \ (TSO)", Y, Y, Y, N_],
                [r"Arm, \ POWER, \ RISC-V", N_, N_, N_, N_]]
        colors = [[GREY_A] + [YES if c == Y else NO for c in r[1:]] for r in rows]
        t = grid_table(hdr, rows, [3.8, 1.9, 1.9, 1.9, 1.9], row_h=0.6, font_size=22, colors=colors,
                       mono_cols=()).move_to(UP * 0.6)
        cap = note(r"an earlier access, \ then a later one, \ to different addresses: \ may the later one become "
                   r"visible first?", font_size=18).next_to(t, DOWN, buff=0.3)
        pts = VGroup(
            label(r"overview only: \ dependencies, same-address rules and architecture details still apply",
                  font_size=21, color=GREY_A),
            label(r"C and C++ (2011), \ Java (2004): \ one portable model, \ mapped to each machine's fences",
                  font_size=21, color=DATA),
            label(r"relaxed atomics can be race-free yet non-SC; \ use the language's synchronization rules \ (Part 33)",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(cap, DOWN, buff=0.35)
        with self.voiceover(
            (
            "This table is a first approximation for ordinary memory accesses to different addresses, without "
            "dependencies or ordering instructions. <bookmark mark='a'/> SC admits a program-order-preserving "
            "interleaving. x86 TSO permits a later load to pass an earlier store to a different address. Baseline "
            "Arm, POWER and RISC-V RVWMO permit more reorderings, with important dependency, same-address and "
            "architecture-specific constraints; the table is not a complete specification. <bookmark mark='b'/> "
            "Acquire, release and fences establish selected ordering relationships. Their meanings differ between "
            "language rules and machine instructions. <bookmark mark='c'/> C, C++ and Java define language memory "
            "models, and compilers must implement their guarantees on each target. <bookmark mark='d'/> Proper "
            "locking can give an SC-style reasoning discipline. But merely having no non-atomic data race does "
            "not make arbitrary C++ relaxed-atomic code SC: our store-buffering test is the counterexample. Part "
            "33 develops the precise conditions."
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule), FadeIn(cap))
            vo.wait_until("a")
            for r in (1, 2, 3):
                self.play(FadeIn(VGroup(*t.cells[r])), run_time=0.8)
            for mk, p in zip("bcd", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
