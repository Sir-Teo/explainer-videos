from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (HEAD, KERN, NO, PART, YES, code, grid_table,
                                   load, mono, num)


class PebbleThreads(VoiceoverScene):
    def construct(self):
        self.card()
        self.isa()
        self.threads()
        self.results()
        self.sweep()

    def card(self):
        card = chapter_card(15, r"PebbleOS gains threads and CAS", r"What does our machine need?", lit=(), extra=(),
                            part=PART)
        with self.voiceover("Chapter fifteen. PebbleOS gains threads, and an atomic instruction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def isa(self):
        head = label(r"Two new instructions", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup()
        for name, op, sem, c in (("cas rd, rs1, rs2", 52, r"$t \leftarrow M[rs_1]$; \ if $t = rd$ then "
                                                          r"$M[rs_1] \leftarrow rs_2$; \ $rd \leftarrow t$", YES),
                                 ("amoadd rd, rs1, rs2", 53, r"$t \leftarrow M[rs_1]$; \ $M[rs_1] \leftarrow t + rs_2$; "
                                                             r"\ $rd \leftarrow t$", HEAD)):
            rows.add(VGroup(mono(name, 22, c), label(rf"opcode {op}, \ R format", font_size=19, color=GREY_A),
                            label(sem, font_size=22, color=WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.55)
        lines = VGroup(
            label(r"the two opcodes Part 6 left reserved; \ each is \textbf{one} step: \ nothing can come between its "
                  r"load and its store", font_size=21, color=WHITE),
            label(r"in a real core: \ hold the cache line in M state for both halves \ (chapter 5)", font_size=21,
                  color=KERN),
            label(r"under the MMU they translate and fault like any load and store \ (Part 32)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Our own machine needs two things to run this part's programs. The first is an atomic instruction. "
            "<bookmark mark='a'/> Compare-and-swap: load the word at the address, and if it equals the expected value "
            "in rd, store the new value; either way, rd receives what was there. <bookmark mark='b'/> And atomic add, "
            "for counters: load, add, store, and return the old value. <bookmark mark='c'/> They take the two "
            "opcodes that Part 6 left reserved, and each is a single step of the machine, so nothing can come between "
            "its load and its store. <bookmark mark='d'/> A real core does that by holding the cache line in the "
            "modified state for both halves. <bookmark mark='e'/> And under Part 32's memory-management unit, they "
            "translate and fault exactly like ordinary loads and stores."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("ab", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            for mk, ln in zip("cde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def threads(self):
        d = load("pebble")
        head = label(r"Threads: \ PCBs that share a page table", font_size=34).to_edge(UP, buff=0.3)
        lk = code([ln.split("#")[0].rstrip() for ln in d["src"]["lock"].splitlines()], size=16)
        box = SurroundingRectangle(lk, color=GREY_D, buff=0.15, corner_radius=0.08)
        cg = VGroup(box, lk).next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        items = VGroup(
            label(r"\texttt{threads\_vm}: \ $n$ PCBs, \\ one root table, \\ a stack each, \ 16 KiB apart", font_size=20,
                  color=WHITE),
            label(r"the kernel is unchanged: \\ a switch between threads \\ just reloads the same \texttt{ptbr}",
                  font_size=20, color=KERN),
            label(r"the lock: \ CAS 0 $\rightarrow$ 1; \\ on failure, \ count it and \\ \texttt{yield} instead of "
                  r"spinning", font_size=20, color=YES),
            label(r"unlock: \ an ordinary store of 0", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(cg, RIGHT, buff=0.5).align_to(cg, UP)
        with self.voiceover(
            "The second thing is threads. <bookmark mark='a'/> In PebbleOS a thread is simply another process control "
            "block whose page-table root is the same as its parent's, with its own stack pages. <bookmark mark='b'/> "
            "The kernel needed no change at all: switching between two threads just reloads the same page table. "
            "<bookmark mark='c'/> And here is a lock built on the new instruction. Compare-and-swap the lock from zero "
            "to one. If the old value was not zero, someone holds it: count the failure, and yield the processor "
            "instead of spinning, since on one core the holder cannot release it while we spin. <bookmark mark='d'/> "
            "Unlocking is an ordinary store of zero."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(items[0]))
            vo.wait_until("b")
            self.play(FadeIn(items[1]))
            vo.wait_until("c")
            self.play(Create(box), FadeIn(lk), FadeIn(items[2]))
            vo.wait_until("d")
            self.play(FadeIn(items[3]))
        self.wait(0.3)
        self.clear_scene()

    def results(self):
        d = load("pebble")
        head = label(rf"Two threads, \ {num(d['n'])} increments each", font_size=34).to_edge(UP, buff=0.3)
        by = {(r["kind"], r["quantum"]): r for r in d["rows"]}
        qs = sorted({r["quantum"] for r in d["rows"]})
        rows = []
        for kind, nm in (("race", r"load, \ add, \ store"), ("amoadd", r"\texttt{amoadd}"), ("lock", r"CAS lock")):
            rows.append([nm] + [by[(kind, q)]["output"] for q in qs])
        tab = grid_table([r"increment", *[rf"quantum {q}" for q in qs]], rows, widths=[3.4, 2.4, 2.4, 2.4],
                         row_h=0.55, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        for j, q in enumerate(qs):
            if by[("race", q)]["output"] != str(2 * d["n"]):
                tab.cells[1][j + 1].set_color(NO)
            for i in (2, 3):
                tab.cells[i][j + 1].set_color(YES)
        lk = by[("lock", 500)]
        am = by[("amoadd", 500)]
        lines = VGroup(
            label(r"the racy version loses updates whenever the timer lands between a load and its store; \ at quantum "
                  r"97 it happens never to", font_size=20, color=NO),
            label(rf"\texttt{{amoadd}} and the lock: \ always {num(2 * d['n'])}; \ at quantum 500 the lock costs "
                  rf"{num(lk['steps'])} instructions against {num(am['steps'])}, \ with {lk['spins']} failed CASes",
                  font_size=20, color=YES),
            label(r"so a test that passes says little: \ the race needs the right schedule \ (chapter 2)",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, buff=0.16).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Now the hook's experiment on our own machine: two threads, each adding one to a shared counter two "
            "thousand times, under three timer quanta. <bookmark mark='a'/> With load, add and store, the count comes "
            "out short at quanta of five hundred and three thousand, whenever the timer interrupt lands between a "
            "thread's load and its store. At ninety-seven instructions it happens, by luck of the arithmetic, never to "
            "land there, and the answer is right. <bookmark mark='b'/> With the atomic add, or with the "
            "compare-and-swap lock, the answer is always four thousand. The lock is not free: at quantum five hundred "
            "it costs nearly three times the instructions, with every failed attempt a yield. <bookmark mark='c'/> And "
            "notice the lucky quantum. A test that happens to pass proves very little; the race only needs the right "
            "schedule, which is why chapter two's checker tries them all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[1])), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[2])), FadeIn(VGroup(*tab.cells[3])), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def sweep(self):
        d = load("pebble")
        sw = d["sweep"]
        head = label(r"The racy counter, \ quantum by quantum", font_size=34).to_edge(UP, buff=0.3)
        full = 2 * d["n"]
        ax = Axes(x_range=[0, 3000, 500], y_range=[2400, 4100, 400], x_length=6.4, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.1).shift(DOWN * 0.3)
        xt = VGroup(*[label(f"{x:,}".replace(",", "{,}"), font_size=15, color=GREY_A).next_to(ax.c2p(x, 2400), DOWN,
                                                                                              buff=0.08)
                      for x in (0, 1000, 2000, 3000)])
        yt = VGroup(*[label(f"{y:,}".replace(",", "{,}"), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT,
                                                                                              buff=0.08)
                      for y in (2400, 3200, 4000)])
        xl = label(r"timer quantum, \ instructions", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        ok = DashedLine(ax.c2p(0, full), ax.c2p(3000, full), color=YES, stroke_width=2)
        okl = label(rf"{num(full)}: \ right", font_size=16, color=YES).next_to(ax.c2p(3000, full), UP, buff=0.05)
        okl.shift(LEFT * 0.6)
        dots = VGroup(*[Dot(ax.c2p(r["quantum"], r["count"]), radius=0.045, color=NO) for r in sw])
        lucky = Dot(ax.c2p(97, full), radius=0.07, color=YES)
        ll = label(r"97", font_size=15, color=YES).next_to(lucky, DOWN, buff=0.06)
        worst = min(sw, key=lambda r: r["count"])
        notes = VGroup(
            label(rf"75 quanta from 40 to 3{{,}}000: \\ every one loses updates; \\ the count ends between "
                  rf"{num(min(r['count'] for r in sw))} and {num(max(r['count'] for r in sw))}", font_size=20,
                  color=NO),
            label(r"one bad preemption loses \\ everything the other thread did \\ until the store", font_size=20,
                  color=WHITE),
            label(r"the sawtooth: \ where the timer lands \\ in the 5-instruction loop \\ shifts with the quantum",
                  font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax, RIGHT, buff=0.7).align_to(ax, UP)
        with self.voiceover(
            "How lucky was that quantum of ninety-seven? We ran the racy counter under seventy-five more quanta. "
            "<bookmark mark='a'/> Every one of them loses updates. The count ends between about two thousand six "
            "hundred and three thousand, never four thousand. <bookmark mark='b'/> The losses are large because one "
            "badly timed preemption loses everything the other thread did between the load and the store: a whole "
            "quantum's worth of increments, overwritten at once. <bookmark mark='c'/> And the sawtooth comes from "
            "where, inside the five-instruction loop, each timer interrupt happens to land, which shifts steadily as "
            "the quantum grows. Ninety-seven was a fluke of that arithmetic."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), Create(ok), FadeIn(okl))
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.02), FadeIn(lucky), FadeIn(ll),
                      run_time=2.0)
            for mk, n_ in zip("abc", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        del worst
        self.wait(0.3)
        self.clear_scene()
