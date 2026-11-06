from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (BG, HEAD, LAM, NO, PART, T0C, T1C, YES, load, mono)


class Sema(VoiceoverScene):
    def construct(self):
        self.card()
        self.def_()
        self.buffer()
        self.rw()

    def card(self):
        card = chapter_card(6, r"Semaphores", r"Can one primitive express every kind of waiting?", lit=(1965,),
                            extra=((1965, r"Dijkstra: \ P and V"),), part=PART)
        with self.voiceover("Chapter six. Semaphores."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def def_(self):
        head = label(r"Dijkstra's semaphore, \ 1965", font_size=36).to_edge(UP, buff=0.3)
        defs = VGroup(
            VGroup(mono("P(s):", 24, HEAD), label(r"wait until $s > 0$, \ then $s \leftarrow s - 1$ \ (atomically)",
                                                   font_size=24, color=WHITE)).arrange(RIGHT, buff=0.3),
            VGroup(mono("V(s):", 24, YES), label(r"$s \leftarrow s + 1$, \ waking a waiter if there is one",
                                                  font_size=24, color=WHITE)).arrange(RIGHT, buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.6)
        uses = VGroup(
            label(r"initial value 1: \ a \textbf{mutex} \ (P to lock, \ V to unlock)", font_size=22, color=WHITE),
            label(r"initial value $n$: \ $n$ identical resources \ (buffers, \ connections)", font_size=22,
                  color=WHITE),
            label(r"initial value 0: \ a \textbf{signal} \ (one thread waits with P until another does V)",
                  font_size=22, color=WHITE),
            label(r"P and V: \ Dutch \textit{proberen} and \textit{verhogen}, \ try and raise; \ the waiting is done by "
                  r"the kernel, \ not by spinning", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(defs, DOWN, buff=0.6)
        with self.voiceover(
            "Locks protect data. But threads also need to wait for each other: for an item to arrive, for space to "
            "free up. In 1965 Dijkstra proposed one primitive for all of it, the semaphore: a counter with two "
            "operations. <bookmark mark='a'/> P waits until the counter is positive, then decrements it, as one atomic "
            "step. <bookmark mark='b'/> V increments it, and wakes a waiting thread if there is one. <bookmark "
            "mark='c'/> Start it at one, and it is a mutex. <bookmark mark='d'/> Start it at n, and it counts n "
            "identical resources. <bookmark mark='e'/> Start it at zero, and it is a signal: one thread waits until "
            "another says go. <bookmark mark='f'/> The letters are Dutch, try and raise, and the waiting is done by the "
            "kernel, which puts the thread to sleep instead of letting it spin."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("ab", defs):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            for mk, it in zip("cdef", uses):
                vo.wait_until(mk)
                self.play(FadeIn(it))
        self.wait(0.3)
        self.clear_scene()

    def buffer(self):
        d = load("sema")
        head = label(r"The bounded buffer", font_size=36).to_edge(UP, buff=0.3)
        prod = VGroup(mono("producer:", 19, T0C), mono("  P(empty)", 19, WHITE), mono("  P(mutex)", 19, GREY_B),
                      mono("  put an item", 19, WHITE), mono("  V(mutex)", 19, GREY_B),
                      mono("  V(full)", 19, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        cons = VGroup(mono("consumer:", 19, T1C), mono("  P(full)", 19, WHITE), mono("  P(mutex)", 19, GREY_B),
                      mono("  take an item", 19, WHITE), mono("  V(mutex)", 19, GREY_B),
                      mono("  V(empty)", 19, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        slots = VGroup(*[Square(0.7, stroke_color=GREY_B, fill_color=BG, fill_opacity=1) for _ in range(4)]).arrange(
            RIGHT, buff=0)
        sl = label(r"$n$ slots: \ \texttt{empty} starts at $n$, \ \texttt{full} at 0", font_size=19,
                   color=GREY_A).next_to(slots, DOWN, buff=0.12)
        VGroup(prod, VGroup(slots, sl), cons).arrange(RIGHT, buff=0.8).next_to(head, DOWN, buff=0.45)
        corr = d["correct"]["finals"]
        brk = d["broken"]["finals"]
        chart_vals = [(k, v) for k, v in sorted(brk.items(), key=lambda kv: int(kv[0]))]
        bars = VGroup()
        mx = max(v for _, v in chart_vals)
        for k, v in chart_vals:
            r = Rectangle(width=0.55, height=1.4 * v / mx, stroke_width=0, fill_color=YES if k == "0" else NO,
                          fill_opacity=0.85)
            bars.add(VGroup(r, label(k, font_size=17, color=GREY_A)))
        for b in bars:
            b[1].next_to(b[0], DOWN, buff=0.06)
        bars.arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        bt = label(r"without the mutex: \ final counts \\ (should be 0)", font_size=18, color=NO).next_to(bars, UP,
                                                                                                    buff=0.15)
        bg = VGroup(bt, bars)
        lines = VGroup(
            label(rf"checked, \ one producer, \ one consumer, \ 3 items, \ 2 slots: \ the final count is always "
                  rf"{list(corr)[0]} \ ({d['correct']['states']} states)", font_size=20, color=YES),
            label(r"P(empty) and P(full) do the \textbf{waiting}; \ the mutex protects the \textbf{data}: \ drop it, "
                  r"and updates are lost", font_size=20, color=WHITE),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        bg.next_to(lines, UP, buff=0.3)
        with self.voiceover(
            "The classic use is the bounded buffer: producers put items into n slots, consumers take them out. "
            "<bookmark mark='a'/> Two counting semaphores do the waiting. Empty starts at n, and a producer does P on "
            "it before putting an item, so it waits when the buffer is full. <bookmark mark='b'/> Full starts at zero, "
            "and a consumer does P on it before taking, so it waits when the buffer is empty. Each side does V on the "
            "other's semaphore when it is done. <bookmark mark='c'/> A third semaphore, used as a mutex, protects the "
            "buffer itself. The checker confirms that the count of items always ends at zero. <bookmark mark='d'/> "
            "Remove the mutex, and the waiting still works, but the shared count is updated by load, add and store, "
            "and the checker finds final counts anywhere from minus two to two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(slots), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(prod))
            vo.wait_until("b")
            self.play(FadeIn(cons))
            vo.wait_until("c")
            self.play(FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(bt), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.15),
                      FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def rw(self):
        head = label(r"Readers and writers, \ and other puzzles", font_size=34).to_edge(UP, buff=0.3)
        items = VGroup(*[VGroup(label(t, font_size=24, color=c), label(s, font_size=20, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08) for t, s, c in (
            (r"readers--writers \ (Courtois, Heymans and Parnas, 1971)",
             r"many readers at once, \ or one writer alone; \ the first reader locks the writers out, \ the last lets "
             r"them in", HEAD),
            (r"\ldots{} and its catch", r"a steady stream of readers starves every writer; \ the fix, \ a turnstile, "
                                        r"\ starves nobody but reads less in parallel", NO),
            (r"the sleeping barber, \ the cigarette smokers, \ the dining savages",
             r"Downey's \textit{Little Book of Semaphores} \ (2005): \ each a pattern you will meet in real code", LAM),
            (r"why semaphores fell out of favour", r"P and V scattered through a program: \ forget one V and a thread "
                                                    r"sleeps forever; \ nothing ties the semaphore to the data", WHITE),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Semaphores can express almost any pattern of waiting. <bookmark mark='a'/> Readers and writers: many "
            "readers may share the data, but a writer needs it alone. The first reader to arrive locks the writers "
            "out, and the last to leave lets them in. <bookmark mark='b'/> But a steady stream of readers then starves "
            "the writers forever. Fixing that costs some of the readers' parallelism, and every real reader-writer lock "
            "chooses a point on that trade-off. <bookmark mark='c'/> Allen Downey's Little Book of Semaphores collects "
            "dozens of such puzzles, each a pattern that turns up in real systems. <bookmark mark='d'/> Yet semaphores "
            "fell out of favour. The P's and V's end up scattered across a program; forget one V and a thread sleeps "
            "forever; and nothing in the code says which data a semaphore protects."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
