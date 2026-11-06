from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (BG, COST, HEAD, KERN, LAM, NO, PART, T0C, T1C, YES, curve, fit_right,
                                   grid_table, load, mono)

KC = {"tas": NO, "ttas": COST, "backoff": LAM, "ticket": HEAD, "mcs": YES}


class Locks(VoiceoverScene):
    def construct(self):
        self.card()
        self.designs()
        self.mcs()
        self.sim()
        self.machine()

    def card(self):
        card = chapter_card(5, r"Hardware locks", r"What does a lock cost when many cores want it?",
                            lit=(1990, 1991), extra=((1990, r"Anderson: \ backoff"),
                                                     (1991, r"Mellor-Crummey and Scott: \ MCS")), part=PART)
        with self.voiceover("Chapter five. Hardware locks."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def designs(self):
        head = label(r"One atomic instruction, \ four locks", font_size=34).to_edge(UP, buff=0.3)
        rows = VGroup()
        for name, src, why, c in (
                (r"test-and-set", "while (tas(&lock)) ;", r"every try is a write: \ the line bounces between cores",
                 NO),
                (r"test and test-and-set", "while (lock || tas(&lock)) ;",
                 r"spin on a read in your own cache; \ a stampede at each release", COST),
                (r"ticket", "t = fai(&next); while (serving != t) ;",
                 r"first come, first served; \ each release wakes every waiter's cache", HEAD),
                (r"MCS queue", "swap(&tail, me); spin on me->locked",
                 r"each waiter spins on its own line; \ a release touches one", YES)):
            rows.add(VGroup(label(name, font_size=22, color=c), mono(src, 18, WHITE),
                            label(why, font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.9)
        side = VGroup(
            label(r"the instruction: \ \texttt{tas}, \ \texttt{xchg}, \ \texttt{lock cmpxchg}", font_size=20,
                  color=WHITE),
            label(r"atomic: \ the core holds the cache line \\ in \textbf{M} state for the whole step \\ (Part 10's "
                  r"MESI)", font_size=20, color=KERN),
            label(r"so contention is coherence traffic", font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rows, RIGHT, buff=0.6).align_to(rows, UP)
        fit_right(side)
        with self.voiceover(
            "Real locks use one atomic instruction, such as test-and-set, which writes a one and returns the old value "
            "in a single indivisible step. The core does it by holding the cache line in the modified state of Part "
            "10's coherence protocol. <bookmark mark='a'/> The simplest lock spins on test-and-set. But every attempt "
            "is a write, so the cache line bounces from core to core even while the lock is held. <bookmark "
            "mark='b'/> Test and test-and-set spins on an ordinary read instead, which hits in the core's own cache, "
            "and tries the atomic only when the lock looks free. But at each release, every waiter misses and rushes "
            "at once. <bookmark mark='c'/> The ticket lock is a bakery in hardware: take a ticket with fetch-and-add, "
            "and wait for your number. It is fair, but each release invalidates every waiter's copy. <bookmark "
            "mark='d'/> And the MCS lock, from Mellor-Crummey and Scott in 1991, puts the waiters in a queue, each "
            "spinning on a flag in its own cache line. <bookmark mark='e'/> In every case, what contention costs is "
            "coherence traffic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]), FadeIn(side[1]))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.wait(0.3)
        self.clear_scene()

    def mcs(self):
        head = label(r"The MCS lock: \ waiters in a queue", font_size=34).to_edge(UP, buff=0.3)
        nodes = VGroup()
        cols = (YES, T0C, T1C, LAM)
        names = (r"holder", r"waiter 1", r"waiter 2", r"waiter 3")
        for k, (nm, c) in enumerate(zip(names, cols)):
            r = RoundedRectangle(width=2.1, height=1.3, corner_radius=0.1, stroke_color=c, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            t = label(nm, font_size=19, color=c).next_to(r.get_top(), DOWN, buff=0.1)
            f = mono("locked = 0" if k == 0 else "locked = 1", 16, WHITE).move_to(r).shift(DOWN * 0.1)
            nx = mono("next ->", 16, GREY_B).next_to(f, DOWN, buff=0.08)
            nodes.add(VGroup(r, t, f, nx))
        nodes.arrange(RIGHT, buff=0.7).move_to([0, 0.8, 0])
        links = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), buff=0.05, color=GREY_B,
                               stroke_width=2) for i in range(3)])
        tail = VGroup(mono("tail", 20, HEAD))
        tail.next_to(nodes[3], UP, buff=0.6)
        ta = Arrow(tail.get_bottom(), nodes[3].get_top(), buff=0.05, color=HEAD, stroke_width=2)
        spins = VGroup(*[CurvedArrow(nodes[i].get_bottom() + LEFT * 0.4, nodes[i].get_bottom() + RIGHT * 0.4,
                                     angle=2.5, color=cols[i], stroke_width=2) for i in (1, 2, 3)])
        lines = VGroup(
            label(r"to wait: \ swap yourself into \texttt{tail}, \ link behind the old tail, \ spin on your own "
                  r"\texttt{locked}", font_size=21, color=WHITE),
            label(r"to release: \ write \texttt{locked = 0} in your successor's node: \ one line, \ one cache",
                  font_size=21, color=YES),
            label(r"used in Linux's queued spinlocks \ (qspinlock, \ 2015) \ and Java's locks", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is the MCS queue. <bookmark mark='a'/> Each thread brings its own little node, with a locked flag and "
            "a next pointer. To wait, it swaps its node into the shared tail pointer, with one atomic exchange, and "
            "links itself behind the thread that was the tail. <bookmark mark='b'/> Then it spins on its own flag, "
            "which lives in its own cache line, so the spinning makes no traffic at all. <bookmark mark='c'/> To "
            "release, the holder writes zero into its successor's flag: one line, moved to one cache. The waiters are "
            "served in order. <bookmark mark='d'/> Linux's queued spinlocks, since 2015, are built on this idea."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(n) for n in nodes[1:]], lag_ratio=0.3), Create(links), FadeIn(tail),
                      GrowArrow(ta), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(Create(spins))
            vo.wait_until("c")
            self.play(nodes[1][2].animate.become(mono("locked = 0", 16, YES).move_to(nodes[1][2])), FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def sim(self):
        d = load("lockssim")
        head = label(r"Coherence traffic per handoff, \ simulated", font_size=34).to_edge(UP, buff=0.3)
        rows = d["rows"]
        cores = sorted({r["cores"] for r in rows})
        ax = Axes(x_range=[1, 5.2, 1], y_range=[0, 2.0, 0.5], x_length=6.2, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.1).shift(DOWN * 0.3)
        xt = VGroup(*[label(str(c), font_size=16, color=GREY_A).next_to(ax.c2p(math.log2(c), 0), DOWN, buff=0.08)
                      for c in cores])
        yt = VGroup(*[label(str(v), font_size=15, color=GREY_A).next_to(ax.c2p(1, math.log10(v)), LEFT, buff=0.08)
                      for v in (1, 3, 10, 30, 100)])
        xl = label(r"cores", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"bus transactions per acquisition \ (log)", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.1).align_to(ax, LEFT)
        cvs = VGroup()
        keys = VGroup()
        for kind in ("tas", "ttas", "ticket", "mcs"):
            rr = [r for r in rows if r["kind"] == kind]
            cvs.add(curve(ax, [math.log2(r["cores"]) for r in rr], [math.log10(r["bus_per_acq"]) for r in rr],
                          KC[kind]))
            keys.add(label(kind.upper() if kind != "ticket" else r"ticket", font_size=17, color=KC[kind]).next_to(
                ax.c2p(math.log2(rr[-1]["cores"]), math.log10(rr[-1]["bus_per_acq"])), RIGHT, buff=0.1))
        at32 = {r["kind"]: r for r in rows if r["cores"] == 32}
        notes = VGroup(
            label(r"Part 10's MESI caches; \ one bus, \\ 8 cycles per transaction", font_size=19, color=WHITE),
            label(rf"32 cores: \ TAS {at32['tas']['bus_per_acq']:.0f}, \ TTAS {at32['ttas']['bus_per_acq']:.0f}, \\ "
                  rf"ticket {at32['ticket']['bus_per_acq']:.0f}, \ MCS {at32['mcs']['bus_per_acq']:.0f} \ "
                  rf"transactions", font_size=19, color=HEAD),
            label(rf"time per handoff: \ TAS {at32['tas']['cycles_per_acq']:.0f} cycles, \\ MCS "
                  rf"{at32['mcs']['cycles_per_acq']:.0f}", font_size=19, color=YES),
            label(rf"fairness \ (least / most served): \\ TAS {at32['tas']['fair']:.2f}, \ MCS "
                  rf"{at32['mcs']['fair']:.2f}", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(ax, RIGHT, buff=0.8).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "We put these locks on Part 10's simulated caches, with a single bus that each transaction occupies for "
            "eight cycles, and counted. <bookmark mark='a'/> With test-and-set, the traffic per handoff grows with the "
            "number of cores, about two transactions per waiting core. <bookmark mark='b'/> Test and test-and-set is "
            "a little better, and the ticket lock better again, but both still grow linearly. <bookmark mark='c'/> The "
            "MCS lock stays flat at about seven, whatever the number of cores. <bookmark mark='d'/> With thirty-two "
            "cores, a test-and-set handoff takes over five hundred cycles, and MCS under sixty. And MCS serves the "
            "waiters in order, while test-and-set lets some cores win far more often than others."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(cvs[0]), FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(Create(cvs[1]), FadeIn(keys[1]), Create(cvs[2]), FadeIn(keys[2]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(cvs[3]), FadeIn(keys[3]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]), FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def machine(self):
        d = load("locksc")
        head = label(rf"On this machine: \ {d['cores']} cores", font_size=36).to_edge(UP, buff=0.3)
        by = {(r["kind"], r["threads"]): r for r in d["rows"]}
        rows = []
        for kind, nm in (("tas", r"test-and-set"), ("ttas", r"test and test-and-set"), ("ticket", r"ticket"),
                         ("mcs", r"MCS"), ("mutex", r"\texttt{pthread\_mutex}")):
            rows.append([nm] + [f"{by[(kind, t)]['ns']:.0f}" for t in (1, 2, 4)] + [f"{by[(kind, 4)]['fair']:.2f}"])
        tab = grid_table([r"lock", r"1 thread", r"2 threads", r"4 threads", r"fairness, \ 4"], rows,
                         widths=[4.0, 1.8, 1.8, 1.8, 2.2], row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.45)
        sub = label(r"nanoseconds per acquisition, \ a one-line critical section, \ best of three half-second runs",
                    font_size=18, color=GREY_A).next_to(tab, UP, buff=0.12)
        lines = VGroup(
            label(r"alone, \ the simplest lock is fastest: \ 7 ns; \ MCS pays for its queue", font_size=21,
                  color=WHITE),
            label(r"contended, \ every lock is 10 to 30 times slower: \ the line must move between cores", font_size=21,
                  color=NO),
            label(r"\texttt{pthread\_mutex} spins briefly, \ then sleeps in the kernel \ (a futex): \ the best here "
                  r"at 4", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.15).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "And on this machine, which has four cores. <bookmark mark='a'/> Uncontended, the simplest lock is the "
            "fastest, seven nanoseconds, and MCS pays for its queue. <bookmark mark='b'/> With two or four threads "
            "fighting over one lock, everything is ten to thirty times slower, because the lock's cache line has to "
            "travel between cores on every handoff. With only four cores, MCS's advantage cannot show. <bookmark "
            "mark='c'/> The library mutex does best under contention here: it spins briefly, and then asks the kernel "
            "to put the thread to sleep, using Linux's fast user-space mutex, the futex."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule),
                      LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.2))
            for mk, ln in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()
