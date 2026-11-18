from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, OooChart, bar_chart,
                                  box, fmt, load, mono, phase_legend)


class Memory(WatchScene):
    def construct(self):
        self.card()
        self.problem()
        self.queues()
        self.violation()
        self.job()

    def card(self):
        self.chapter(8, r"Loads, \ stores, \ and their order", r"When may a load overtake a store?", lit=(1997, 1998), extra=((1997, r"Moshovos: \ dependence prediction"),
                                                     (1998, r"store sets; \ the Alpha 21264")), part=PART, said="Chapter eight. Loads, stores, and their order.")

    # ------------------------------------------------------------------
    def problem(self):
        head = label(r"Registers are renamed early; \ memory addresses are known late", font_size=32).to_edge(
            UP, buff=0.4)
        code = VGroup(mono("sw   a4, 0(a3)     # where? a3 is still being computed", 22),
                      mono("lw   a5, 4(s0)     # s0 is known: the load could go now", 22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to(UP * 1.0)
        q = VGroup(
            label("overlapping byte ranges: \\ preserve the older store value",
                  font_size=24, color=NO),
            label("disjoint byte ranges: \\ this dependency is absent; \\ other rules remain", font_size=24, color=YES),
            label(r"the machine cannot know which \ until the store's address is computed", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 0.9)
        with self.voiceover(
            "Register names are available at decode, but effective memory addresses may depend on unfinished "
            "arithmetic. <bookmark mark='a'/> Here an older store waits for its address in a3, while a younger load "
            "already knows s0 plus four. <bookmark mark='b'/> If their byte ranges overlap, the load must observe "
            "the correct older store's bytes, perhaps through forwarding or after waiting. Equal starting addresses "
            "are only one overlap case. <bookmark mark='c'/> Disjoint byte ranges remove this particular "
            "dependency, though resources and other ordering rules still apply. <bookmark mark='d'/> Until the "
            "store address is known, the core must either wait conservatively or speculate and later check. That is "
            "the memory-disambiguation problem in this single-core model."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(code))
            vo.wait_until("a")
            for mk, x in zip("bcd", q):
                vo.wait_until(mk)
                self.play(FadeIn(x, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def queues(self):
        head = label(r"The load and store queues", font_size=36).to_edge(UP, buff=0.35)
        sq = VGroup(*[Rectangle(width=3.8, height=0.48, stroke_color=INF, stroke_width=1.5) for _ in range(5)]).arrange(
            DOWN, buff=0.04)
        entries = [("sw a4, 0(a3)", "address ?", NO), ("sw t1, 8(t0)", "0x1018 = 5", YES),
                   ("sw a1, 4(s0)", "0x2004 = 9", YES)]
        sq_t = VGroup()
        for k, (ins, st, c) in enumerate(entries):
            sq_t.add(VGroup(Text(ins, font="DejaVu Sans Mono", font_size=14, color=CODE),
                            Text(st, font="DejaVu Sans Mono", font_size=14, color=c)).arrange(RIGHT, buff=0.2).move_to(
                sq[k]))
        sqg = VGroup(label(r"store queue \ (oldest at top)", font_size=20, color=INF).next_to(sq, UP, buff=0.12), sq,
                     sq_t).move_to(LEFT * 3.2 + DOWN * 0.1)
        ld = box(3.0, 0.7, r"\texttt{lw a5, 4(s0)} \ \to \ \texttt{0x2004}", DATA, 20).move_to(RIGHT * 2.8 + UP * 1.4)
        arr = CurvedArrow(ld.get_left(), sq[2].get_right(), angle=0.5, color=YES, stroke_width=3)
        fw = label(r"store-to-load forwarding: \ 9, \ without touching memory", font_size=22, color=YES).next_to(
            ld, DOWN, buff=0.9)
        modes = VGroup(
            label(r"\textit{conservative}: \ wait while any older store's address is unknown", font_size=22,
                  color=GREY_A),
            label(r"\textit{speculative}: \ go anyway; \ check when the store's address arrives", font_size=22,
                  color=GREY_A),
            label("load-PC wait table: \\ a simplified historical load-wait policy",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The load and store queues retain program-order relationships among memory operations. <bookmark "
            "mark='a'/> In this simulator, stores compute address and data early but write the byte array only at "
            "retirement. A squashed store does not commit that write. Real processors can have earlier "
            "store-related cache or coherence effects, which this rule does not model. <bookmark mark='b'/> A load "
            "searches for the youngest relevant older store. If that store covers all requested bytes and its data "
            "is ready, it can forward the value. This implementation waits on partial overlaps rather than merging "
            "several stores. <bookmark mark='c'/> Conservative disambiguation waits for unknown older store "
            "addresses. Speculative disambiguation proceeds and checks later. The load-PC wait table conservatively "
            "retrains previously violating loads; it is a simplified policy inspired by historical load-wait "
            "predictors, not a complete store-set predictor."
        ) as vo:
            self.play(FadeIn(head))
            self.play(FadeIn(sqg))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(ld), Create(arr), FadeIn(fw))
            vo.wait_until("c")
            self.play(Indicate(sq_t[0], color=NO))
            self.play(LaggedStart(*[FadeIn(m) for m in modes], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def violation(self):
        self.ask(r"A load runs before an older store \\ whose address isn't known yet. They turn out to match. Then...",
                 [r"the hardware had waited anyway", r"the load read stale data, and is squashed and replayed"], 1,
                 say="A load runs before an older store whose address isn't known yet. The addresses turn out to be the same. "
                     "What happens?",
                 reveal="The load read stale data. The core catches the conflict, squashes the load, and replays it.")
        d = load("memory")["demo"]
        head = label(r"Caught out: \ a memory-order violation", font_size=34).to_edge(UP, buff=0.25)
        tl = d["speculative"]["timeline"][6:]
        ch = OooChart(tl, cw=0.27, ch=0.38, label_width=2.6, label_size=15, c0=4).move_to(DOWN * 0.2 + LEFT * 0.4)
        leg = phase_legend(font_size=17).to_edge(DOWN, buff=0.15)
        notes = VGroup(
            label(r"the load runs early: \ reads 0 from memory", font_size=21, color=NO),
            label(r"the store's address arrives: \ \texttt{0x804}, \ the very word", font_size=21, color=INF),
            label(r"the load and everything after it: \ squashed, \ refetched", font_size=21, color=NO),
            label(r"run again: \ 77", font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UR, buff=0.3).shift(DOWN * 0.6)
        tot = label(rf"speculative: \ {d['speculative']['cycles']} cycles; \ conservative: \ "
                    rf"{d['conservative']['cycles']}", font_size=22, color=HEAD).next_to(notes, DOWN, buff=0.3).align_to(
            notes, LEFT)
        with self.voiceover(
            "This recorded example makes the ordering mistake visible. <bookmark mark='a'/> A younger load executes "
            "before the older store's address is ready and reads zero from memory. <bookmark mark='b'/> The delayed "
            "address resolves to the same word, which the older store must write with seventy-seven. <bookmark "
            "mark='c'/> The model detects the overlapping younger load, squashes it and its dependents, and "
            "refetches. The corrected load obtains seventy-seven after the required older-store ordering is "
            "respected. In this recording the store retires before the replayed load starts; forwarding can satisfy "
            "other valid cases before a store retires. <bookmark mark='d'/> The speculative run takes thirty-five "
            "cycles and the conservative one twenty-nine. Speculation is not always faster: a wrong guess can cost "
            "more than the waiting it avoided."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ch.heads), FadeIn(leg),
                      LaggedStart(*[FadeIn(VGroup(ch.rows[i], ch.bars[i], ch.commits[i])) for i in range(6)],
                                  lag_ratio=0.1))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(ch.rows[6], ch.bars[6], ch.rows[7], ch.bars[7], ch.rows[8], ch.bars[8])),
                      FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Indicate(ch.rows[5], color=INF), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(ch.rows[i], ch.bars[i], ch.commits[i])) for i in range(9, ch.n)],
                                  lag_ratio=0.2), FadeIn(notes[3]))
            self.play(FadeIn(tot))
        self.wait(0.3)
        self.clear_scene()


    # ------------------------------------------------------------------
    def job(self):
        d = load("memory")
        r = d["rows"]
        head = label(r"And on the Job?", font_size=38).to_edge(UP, buff=0.4)
        lines = VGroup(
            label(rf"conservative: \ {r['conservative']['cycles']:,} cycles", font_size=26, color=GREY_A),
            label(rf"speculative: \ {r['speculative']['cycles']:,} cycles", font_size=26, color=GREY_A),
            label(rf"wait table: \ {r['wait-table']['cycles']:,} cycles", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(UP * 0.6)
        why = VGroup(
            label(rf"{d['loads']:,} loads, \ but only {d['stores']:,} stores", font_size=26, color=INF),
            label("stores update counts, table metadata and letters; \\ no policy benefit here", font_size=26,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(lines, DOWN, buff=0.6)
        with self.voiceover(
            "The Job's first chapter behaves differently. <bookmark mark='a'/> All three tested disambiguation "
            "policies give the same four hundred thirty-seven thousand five hundred eighty model cycles. <bookmark "
            "mark='b'/> Its recorded trace has a hundred fifty-four thousand eight hundred thirty-five loads and "
            "five thousand two hundred seventy stores. Stores update counts, table metadata and the letter pool. "
            "These runs show no benefit from changing the tested policy; they do not prove that every load is "
            "independent or that memory disambiguation never matters. Different workloads expose different "
            "bottlenecks."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.3))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()
