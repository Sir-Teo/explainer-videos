from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, OooChart, bar_chart,
                                  box, fmt, load, mono, phase_legend)


class Memory(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.queues()
        self.violation()
        self.histogram()
        self.job()

    def card(self):
        card = chapter_card(8, r"Loads, \ stores, \ and their order", r"When may a load overtake a store?",
                            lit=(1997, 1998), extra=((1997, r"Moshovos: \ dependence prediction"),
                                                     (1998, r"store sets; \ the Alpha 21264")), part=PART)
        with self.voiceover("Chapter eight. Loads, stores, and their order."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def problem(self):
        head = label(r"Registers are renamed early; \ memory addresses are known late", font_size=32).to_edge(
            UP, buff=0.4)
        code = VGroup(mono("sw   a4, 0(a3)     # where? a3 is still being computed", 22),
                      mono("lw   a5, 4(s0)     # s0 is known: the load could go now", 22)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to(UP * 1.0)
        q = VGroup(
            label(r"if \texttt{a3} $= $ \texttt{s0 + 4}: \ the load must wait for the store, \ and take its value",
                  font_size=24, color=NO),
            label(r"if not: \ the load is free to go first", font_size=24, color=YES),
            label(r"the machine cannot know which \ until the store's address is computed", font_size=24,
                  color=HEAD),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 0.9)
        with self.voiceover(
            "Renaming removed the false dependences between registers, because a register's name is right there in "
            "the instruction, and can be checked as soon as it is decoded. Memory is harder. <bookmark mark='a'/> "
            "Here a store writes to an address in a3, which is still being computed, and a load right after it "
            "reads from s0 plus four, which is already known. <bookmark mark='b'/> If the two addresses are the "
            "same, the load must wait for the store and take the store's value. <bookmark mark='c'/> If they are "
            "different, the load could go at once. <bookmark mark='d'/> And the machine cannot tell which, until "
            "the store's address is known. Dependences through memory are hidden behind arithmetic."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code))
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
            label(r"\textit{wait table} \ (Alpha 21264): \ speculate, \ except loads that were caught before",
                  font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So a core keeps its memory operations in two queues, in program order. <bookmark mark='a'/> Stores wait "
            "in the store queue until they commit; only then do they write memory, so a store on a wrong path never "
            "touches it. <bookmark mark='b'/> A load, when it executes, searches the older stores. If the youngest "
            "older store to the same address has its data, the load takes the value straight from the queue: "
            "store-to-load forwarding. <bookmark mark='c'/> The hard case is the first entry, a store whose address "
            "is unknown. There are three policies. Wait, conservatively, while any older store's address is unknown. "
            "Or speculate: go ahead, and check later. Or do what the Alpha 21264 did in 1998: speculate, but remember "
            "the loads that have been caught out before, and make only those wait."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sqg))
            vo.wait_until("b")
            self.play(FadeIn(ld), Create(arr), FadeIn(fw))
            vo.wait_until("c")
            self.play(Indicate(sq_t[0], color=NO))
            self.play(LaggedStart(*[FadeIn(m) for m in modes], lag_ratio=0.4))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def violation(self):
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
            "Here is speculation caught out, on our core. A divide produces the store's address offset, so the store "
            "cannot compute its address for sixteen cycles. <bookmark mark='a'/> The load after it, whose address "
            "is known, does not wait. It reads its word from memory at once, and gets zero. <bookmark mark='b'/> "
            "Sixteen cycles later the store's address arrives, and the store queue checks every younger load that "
            "has already run. One of them read the very word this store writes. <bookmark mark='c'/> That load's "
            "value is wrong, and so is anything computed from it. So the load and everything after it are squashed "
            "and fetched again, exactly as after a wrong branch. <bookmark mark='d'/> The second time, the store has "
            "committed, and the load reads seventy-seven. Here the gamble lost, and cost six cycles."
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
    def histogram(self):
        d = load("memory")["histogram"]
        m = d["modes"]
        head = label(r"Where it matters: \ counting samples that miss the cache", font_size=32).to_edge(UP, buff=0.3)
        code = VGroup(*[mono(s, 17) for s in (
            "loop: lbu  a0, 0(s0)     # a sample: a cache miss, 60 cycles",
            "      slli a0, a0, 2",
            "      add  a0, a0, s1",
            "      lw   t0, 0(a0)     # count[sample]",
            "      addi t0, t0, 1",
            "      sw   t0, 0(a0)     # its address waits for the miss",
            "      addi s0, s0, 64",
            "      bne  s0, s2, loop")]).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.4).shift(
            DOWN * 0.6)
        keys = ["conservative", "speculative", "wait-table"]
        vals = [m[k]["cycles"] / 1000 for k in keys]
        ch = bar_chart(vals, [r"conservative", r"speculative", r"wait table"], [NO, DATA, YES], height=3.0, bar_w=1.0,
                       gap=0.9, font_size=20, fmt_=lambda v: f"{v:.1f}K").to_corner(DR, buff=0.6).shift(UP * 0.4)
        yl = note(rf"cycles for {d['n']:,} samples", font_size=20).next_to(ch, UP, buff=0.3)
        viol = VGroup(*[label(rf"{m[k]['violations']} violations", font_size=18, color=GREY_B).next_to(
            ch.names[i], DOWN, buff=0.12) for i, k in enumerate(keys)])
        punch = label(rf"{m['conservative']['cycles'] / m['wait-table']['cycles']:.0f} times faster, \ by guessing "
                      r"that a load and a store do not collide", font_size=24, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "When does it matter? Here is a loop that counts samples into buckets, where every sample misses the "
            "cache. <bookmark mark='a'/> The store at the bottom writes a count whose address depends on the "
            "sample, so its address is unknown for sixty cycles. The next trip's sample load, which has nothing to do "
            "with the counts, comes right after it. <bookmark mark='b'/> A conservative machine makes every load wait "
            "for that store's address: each miss in turn, ninety-eight thousand cycles for fifteen hundred samples. "
            "<bookmark mark='c'/> A speculative machine lets the sample loads run ahead, so a dozen misses overlap: "
            "seven and a half thousand cycles. Twenty-three times, two count loads collided with stores to the same "
            "bucket, and had to be redone. <bookmark mark='d'/> The wait table learns, after one collision, that the "
            "count load is the risky one, and makes only it wait, while the sample loads still run ahead. Thirteen "
            "times faster than waiting. Real cores predict memory dependences in just this way; Intel's count each "
            "recovery from a wrong guess as a machine clear, a number any programmer can read from the performance "
            "counters."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("a")
            self.play(Indicate(code[5], color=INF), Indicate(code[0], color=INF))
            self.play(FadeIn(yl), FadeIn(ch[0]))
            for mk, k in (("b", 0), ("c", 1), ("d", 2)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(ch.bars[k], DOWN), FadeIn(ch.vals[k]), FadeIn(ch.names[k]), FadeIn(viol[k]))
            self.play(FadeIn(punch))
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
            label(r"the Job writes only when it counts a word: \ its loads almost never wait", font_size=26,
                  color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(lines, DOWN, buff=0.6)
        with self.voiceover(
            "And on the Job? <bookmark mark='a'/> All three policies give exactly the same cycle count. <bookmark "
            "mark='b'/> The Job does a hundred fifty-five thousand loads in its first chapter but only five thousand "
            "stores, one or two each time it counts a word, and their addresses are known early. There is nothing to "
            "wait for. A machine's features earn their keep on some programs and sit idle on others, which is why "
            "architects measure on many."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l) for l in lines], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()
