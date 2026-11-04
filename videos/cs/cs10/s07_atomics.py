from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs10.common import (BG, CODE, CORE_COLORS, CTRL, DATA, FUNC, HEAD, NO, PART, YES, bar_chart,
                                   grid_table, load, mono, timeline)


class Atomics(VoiceoverScene):
    def construct(self):
        self.card()
        self.lost()
        self.instructions()
        self.costs()
        self.consensus()

    def card(self):
        card = chapter_card(6, r"Atomic instructions", r"How do two cores agree on anything?", lit=(1964, 1991),
                            extra=((1964, r"test-and-set, \ IBM System/360"), (1991, r"Herlihy: \ wait-free "
                                                                                    r"synchronization")), part=PART)
        with self.voiceover("Chapter six. Atomic instructions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def lost(self):
        at = load("atomics")["rows"][0]["t4"]
        head = label(r"A lost update", font_size=36).to_edge(UP, buff=0.35)
        code = mono("count = count + 1;     // load, add, store", 22).next_to(head, DOWN, buff=0.35)
        t0 = timeline(["load 5", "add: 6", "store 6"], CORE_COLORS[0], -4.6, 0.6, dx=1.7)
        t1 = timeline(["load 5", "add: 6", "store 6"], CORE_COLORS[1], -2.9, -0.4, dx=1.7)
        n0 = label(r"thread 0", font_size=20, color=CORE_COLORS[0]).next_to(t0, LEFT, buff=0.3)
        n1 = label(r"thread 1", font_size=20, color=CORE_COLORS[1]).next_to(t1, LEFT, buff=0.3).align_to(n0, LEFT)
        tl = Arrow(LEFT * 5.8 + DOWN * 1.1, RIGHT * 3.2 + DOWN * 1.1, color=GREY_C, stroke_width=2, buff=0)
        tll = label(r"time", font_size=18, color=GREY_B).next_to(tl, RIGHT, buff=0.1)
        res = label(r"two increments, \ and the count went from 5 to 6", font_size=24, color=NO).next_to(tl, DOWN,
                                                                                                       buff=0.35)
        meas = label(rf"four threads, \ ten million increments each, \ on this computer: \ the count reaches "
                     rf"{min(at['count']):,} to {max(at['count']):,} \ of {at['expected']:,}", font_size=22,
                     color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Coherence keeps the caches in agreement about each line. It does not make a sequence of operations "
            "indivisible. <bookmark mark='a'/> Adding one to a shared counter is three steps: load it, add, store it "
            "back. <bookmark mark='b'/> Thread zero loads five. Before it stores, thread one also loads five. Both "
            "add one; both store six. <bookmark mark='c'/> Two increments, and the counter went up by one. <bookmark "
            "mark='d'/> On this computer, four threads each adding one to a shared counter ten million times end "
            f"with a count of between {min(at['count']) / 1e6:.0f} and {max(at['count']) / 1e6:.0f} million, out of "
            "forty. More than half of the updates simply vanish, and the result changes from run to run."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code))
            vo.wait_until("b")
            self.play(FadeIn(n0), FadeIn(n1), Create(tl), FadeIn(tll))
            for k in range(3):
                self.play(FadeIn(t0[k]), FadeIn(t1[k]), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(meas))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def instructions(self):
        head = label(r"Read, \ modify and write \ as one indivisible step", font_size=32).to_edge(UP, buff=0.3)
        items = [
            (r"test-and-set \ (IBM System/360, \ 1964)", "old = *p;  *p = 1;  return old;", DATA),
            (r"fetch-and-add \ (x86 \texttt{lock xadd})", "old = *p;  *p = old + v;  return old;", YES),
            (r"compare-and-swap \ (IBM System/370, \ x86 \texttt{cmpxchg})",
             "if (*p == expected) { *p = new; return 1; } return 0;", CTRL),
            (r"load-linked, \ store-conditional \ (Arm, \ POWER, \ RISC-V)",
             "v = LL(p);  ...;  ok = SC(p, v2);   // fails if p was written", FUNC),
        ]
        rows = VGroup()
        for t, c, col in items:
            rows.add(VGroup(label(t, font_size=22, color=col), mono(c, 18)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 0.15 + LEFT * 0.4)
        how = note(r"the core holds the line Modified for the whole step, \ refusing to give it up until it is done",
                   font_size=18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The fix needs the hardware's help: instructions that read, modify and write a location as a single step "
            "no other core can interrupt. <bookmark mark='a'/> The oldest is test-and-set, on IBM's System/360 in "
            "1964: set a word to one and return what it held. A lock is a word that test-and-set turns from zero to "
            "one; whoever got zero back holds the lock. <bookmark mark='b'/> Fetch-and-add adds to a word and returns "
            "the old value: exactly the counter, in one instruction. <bookmark mark='c'/> Compare-and-swap stores a "
            "new value only if the word still holds the value you expect, and reports whether it did. <bookmark "
            "mark='d'/> And load-linked and store-conditional split it in two: the store succeeds only if no one "
            "wrote the location since the load. <bookmark mark='e'/> Inside, they all work the same way: the core "
            "takes the line in the Modified state and refuses to give it up until the step is complete. Atomicity is "
            "built from coherence."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(how))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def costs(self):
        rows = load("atomics")["rows"]
        head = label(r"Counting correctly: \ the price, \ measured", font_size=34).to_edge(UP, buff=0.3)
        good = rows[1:]
        names = [r"fetch-and-add", r"CAS loop", r"mutex", r"spinlock \\ (test-and-set)"]
        v1 = [r["t1"]["ns"] for r in good]
        v4 = [r["t4"]["ns"] for r in good]
        c = bar_chart(v1 + v4, names + names, [YES, CTRL, DATA, FUNC] * 2, height=3.2, bar_w=0.62, gap=0.45,
                      fmt_=lambda v: f"{v:.0f}", font_size=17).move_to(DOWN * 0.4)
        for k in range(4, 8):
            c.bars[k].set_fill(opacity=0.95)
            c.bars[k - 4].set_fill(opacity=0.45)
        g1 = label(r"one thread", font_size=22, color=GREY_A).next_to(VGroup(*c.bars[:4]), UP, buff=1.0)
        g4 = label(r"four threads, \ one counter", font_size=22, color=GREY_A).next_to(VGroup(*c.bars[4:]), UP,
                                                                                         buff=0.2)
        yl = note(r"nanoseconds per increment \ (all four counts exact: \ 40,000,000)", font_size=18).to_edge(
            DOWN, buff=0.3)
        plain = rows[0]["t1"]["ns"]
        cmp_ = label(rf"a plain, \ wrong, \ increment: \ {plain:.1f} ns", font_size=20, color=NO).next_to(head, DOWN,
                                                                                                          buff=0.2)
        with self.voiceover(
            "What does correctness cost? Here are four correct counters, timed on this computer. <bookmark mark='a'/> "
            f"First with one thread, where there is no contention at all. A plain increment takes {plain:.0f} "
            "nanoseconds. Fetch-and-add takes about seven: the atomic step itself costs a few times a plain one. A "
            "compare-and-swap loop costs more, and a mutex, which is an atomic instruction plus bookkeeping, more "
            "again. <bookmark mark='b'/> Now four threads hammering the same counter. Everything slows, because the "
            "line must travel between cores for every increment, as in the last chapter. Fetch-and-add stays the "
            "cheapest, since each attempt always succeeds. The compare-and-swap loop retries whenever another core "
            "got in first. And the simple spinlock, where waiting cores hammer the lock with test-and-set, is the "
            "worst of all. The lesson is the Job's again: the fastest shared counter is one you do not share."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cmp_), FadeIn(yl), FadeIn(c[0]))
            vo.wait_until("a")
            self.play(FadeIn(g1), *[GrowFromEdge(c.bars[k], DOWN) for k in range(4)],
                      *[FadeIn(c.vals[k]) for k in range(4)], *[FadeIn(c.names[k]) for k in range(4)])
            vo.wait_until("b")
            self.play(FadeIn(g4), *[GrowFromEdge(c.bars[k], DOWN) for k in range(4, 8)],
                      *[FadeIn(c.vals[k]) for k in range(4, 8)], *[FadeIn(c.names[k]) for k in range(4, 8)])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def consensus(self):
        head = label(r"Not all atomics are equal \ (Herlihy, \ 1991)", font_size=34).to_edge(UP, buff=0.3)
        q = label(r"\textit{consensus}: \ $n$ threads each propose a value; \ all must decide the same one, \ "
                  r"and no thread may wait for another", font_size=22, color=GREY_A).next_to(head, DOWN, buff=0.35)
        rows = [[r"reads and writes", r"1"], [r"test-and-set, \ fetch-and-add, \ swap", r"2"],
                [r"compare-and-swap, \ LL/SC", r"$\infty$"]]
        colors = [[GREY_A, NO], [GREY_A, CTRL], [GREY_A, YES]]
        t = grid_table([r"primitive", r"consensus number"], rows, [5.6, 2.8], row_h=0.6, font_size=22, colors=colors,
                       mono_cols=()).next_to(q, DOWN, buff=0.45)
        univ = label(r"a primitive that solves consensus for $n$ threads \ can build \textit{any} shared data structure "
                     r"for $n$ threads, \ wait-free", font_size=22, color=HEAD).next_to(t, DOWN, buff=0.45)
        why = note(r"so every modern instruction set has compare-and-swap or LL/SC; \ Part 33 builds lock-free "
                   r"structures with them", font_size=18).next_to(univ, DOWN, buff=0.3)
        with self.voiceover(
            "There is a beautiful theory behind these instructions. <bookmark mark='a'/> In 1991 Maurice Herlihy asked "
            "which of them can solve consensus: several threads each propose a value, and all must agree on one of "
            "them, without any thread ever waiting for another, which might have stalled or crashed. <bookmark "
            "mark='b'/> With ordinary reads and writes, not even two threads can do it. Test-and-set, fetch-and-add "
            "and swap can do it for two threads, but provably not for three. Compare-and-swap, and load-linked with "
            "store-conditional, can do it for any number. <bookmark mark='c'/> And Herlihy showed that consensus is "
            "the key: a primitive that solves consensus for n threads can be used to build any shared data structure "
            "for n threads, in a wait-free way. <bookmark mark='d'/> That is why every modern instruction set has "
            "compare-and-swap or LL/SC, and Part 33 uses them to build data structures with no locks at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*t.cells[0])), FadeIn(t.rule))
            for r in (1, 2, 3):
                self.play(FadeIn(VGroup(*t.cells[r])), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(univ))
            vo.wait_until("d")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()
