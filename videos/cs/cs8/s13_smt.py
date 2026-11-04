from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs8.common import (BG, CODE, COST, CTRL, DATA, FUNC, HEAD, HIST, INF, NO, PART, YES, bar_chart, box, fmt,
                                  load, mono)


def slots(counts, width=4, cw=0.42, ch=0.42, colors=(DATA,)):
    """Issue slots, cycles across and slots up: ``counts[c]`` is the number used in cycle c (or a list, one count per
    thread, stacked)."""
    g = VGroup()
    g.frame, g.used = VGroup(), VGroup()
    for c, n in enumerate(counts):
        ns = n if isinstance(n, list) else [n]
        k = 0
        for t, m in enumerate(ns):
            for _ in range(min(m, width - k)):
                g.used.add(Rectangle(width=cw * 0.88, height=ch * 0.84, stroke_width=0, fill_color=colors[t],
                                     fill_opacity=0.8).move_to([c * cw, k * ch, 0]))
                k += 1
        for w in range(width):
            g.frame.add(Rectangle(width=cw, height=ch, stroke_color=GREY_D, stroke_width=1).move_to([c * cw, w * ch, 0]))
    g.add(g.frame, g.used)
    return g


class Smt(VoiceoverScene):
    def construct(self):
        self.card()
        self.empty()
        self.share()
        self.numbers()

    def card(self):
        card = chapter_card(12, r"Simultaneous multithreading", r"Who uses the empty slots?", lit=(1995, 2002),
                            extra=((1995, r"Tullsen, \ Eggers, \ Levy"), (2002, r"Hyper-Threading")), part=PART)
        with self.voiceover("Chapter twelve. Simultaneous multithreading."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def empty(self):
        d = load("smt")
        h = load("hook")
        head = label(r"A four-wide machine, \ one program", font_size=36).to_edge(UP, buff=0.35)
        g = slots(d["slots_alone"], colors=(DATA,)).move_to(UP * 0.6)
        lab = note(r"issue slots: \ 4 per cycle, \ 24 cycles", font_size=20).next_to(g, UP, buff=0.2)
        used = sum(min(x, 4) for x in d["slots_alone"])
        facts = VGroup(
            label(rf"here {used} of {4 * len(d['slots_alone'])} slots are used", font_size=24, color=DATA),
            label(rf"our core on the Job: \ IPC {h['ooo']['ipc']:.2f} \ of 4: \ more than half the slots empty",
                  font_size=24, color=NO),
            label(r"the slots are there; \ one program cannot fill them", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Chapter six ended with a machine that has more width than one program can use. Here are a four-wide "
            "machine's issue slots, four per cycle, over twenty-four cycles of the Job. <bookmark mark='a'/> Filled "
            "squares are slots that started an instruction. Some cycles use all four; many use one or two; some none, "
            "while a misprediction is repaired. <bookmark mark='b'/> On our real core, the Job reaches one point nine "
            "instructions per cycle out of four: more than half the issue slots go unused, cycle after cycle. "
            "<bookmark mark='c'/> The hardware is built, powered and waiting. One program simply cannot fill it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.frame), FadeIn(lab))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(u) for u in g.used], lag_ratio=0.02), run_time=2.0)
            self.play(FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def share(self):
        d = load("smt")
        head = label(r"Two programs, \ one core", font_size=36).to_edge(UP, buff=0.35)
        g = slots(d["slots_both"], colors=(DATA, CTRL)).move_to(UP * 0.9)
        leg = VGroup(label(r"thread 1: \ the Job on \textit{Pride and Prejudice}", font_size=20, color=DATA),
                     label(r"thread 2: \ the Job on \textit{Moby-Dick}", font_size=20, color=CTRL)).arrange(
            RIGHT, buff=0.6).next_to(g, UP, buff=0.25)
        per = VGroup(
            label(r"per thread: \ its own program counter, \ alias table, \ branch history", font_size=23,
                  color=GREY_A),
            label(r"shared: \ the issue queue, \ the units, \ the caches; \ the ROB split in two", font_size=23,
                  color=GREY_A),
            label(r"a wrong guess in one thread squashes only that thread's work", font_size=23, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1995 Dean Tullsen, Susan Eggers and Henry Levy proposed the obvious, radical fix: let a second "
            "program use the same core at the same time. <bookmark mark='a'/> Here the Job runs on two different "
            "books, as two threads sharing one four-wide core. Their instructions mix freely in the issue slots, and "
            "the second thread fills many of the holes the first one leaves. <bookmark mark='b'/> Each thread needs "
            "only its own program counter, its own register alias table, and its own branch history. Everything "
            "expensive is shared: the issue queue, the functional units, the caches, and the reorder buffer, split "
            "between them. Because renaming keeps the threads' registers apart, the scheduler does not even need to "
            "know which instruction belongs to whom. <bookmark mark='c'/> And when one thread guesses a branch "
            "wrong, only its own instructions are thrown away; the other thread carries on."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.frame), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(u) for u in g.used], lag_ratio=0.015), run_time=2.0)
            for mk, p in zip("bc", (VGroup(per[0], per[1]), per[2])):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        d = load("smt")["configs"]
        head = label(r"Throughput, \ in the limit study", font_size=36).to_edge(UP, buff=0.35)
        groups = VGroup()
        for key, title in (("4/128", r"4 wide, \ window 128"), ("8/256", r"8 wide, \ window 256")):
            r = d[key]
            ch = bar_chart([r["one_a"], r["two"]], [r"one thread", r"two threads"], [DATA, YES], height=2.8,
                           bar_w=1.0, gap=0.9, font_size=22, vmax=6.5)
            t = label(title, font_size=24, color=GREY_A).next_to(ch, UP, buff=0.6)
            gain = label(rf"$+{r['two'] / r['one_a'] - 1:.0%}$".replace("%", r"\%"), font_size=28, color=HEAD).next_to(
                ch.bars[1], RIGHT, buff=0.25)
            groups.add(VGroup(t, ch, gain))
        groups.arrange(RIGHT, buff=1.6).move_to(DOWN * 0.1)
        yl = note(r"instructions per cycle, \ both threads together", font_size=20).next_to(groups, UP, buff=0.2)
        real = VGroup(
            label(r"Intel's Hyper-Threading (2002), \ IBM POWER5 (2004): \ two threads; \ POWER8 (2014): \ eight",
                  font_size=22, color=HIST),
            label(r"the price: \ each thread runs slower, \ and threads can time each other's use of the core",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How much does it help? The oracle scheduler with real branch prediction can answer. <bookmark mark='a'/> "
            "Four wide, with a window of a hundred twenty-eight: one thread manages two point seven instructions per "
            "cycle; two threads, each with half the window, three point seven together, forty percent more. "
            "<bookmark mark='b'/> Eight wide, with a window of two hundred fifty-six, the gain is eighty percent: "
            "the wider the machine, the more a single thread wastes, and the more a second thread recovers. "
            "<bookmark mark='c'/> Intel shipped two-thread SMT as Hyper-Threading in 2002, IBM in the POWER5 in "
            "2004, and IBM's POWER8 runs eight threads per core. The price is that each thread runs slower than it "
            "would alone, and that threads sharing a core can watch each other: one can time its own use of the "
            "units to learn what the other is doing. After 2018 some systems turned SMT off for exactly that reason."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl))
            for mk, gr in zip("ab", groups):
                vo.wait_until(mk)
                self.play(FadeIn(gr[0]), FadeIn(gr[1][0]), GrowFromEdge(gr[1].bars[0], DOWN),
                          GrowFromEdge(gr[1].bars[1], DOWN), FadeIn(gr[1].vals), FadeIn(gr[1].names))
                self.play(FadeIn(gr[2]))
            vo.wait_until("c")
            self.play(FadeIn(real))
        self.wait(0.3)
        self.clear_scene()
