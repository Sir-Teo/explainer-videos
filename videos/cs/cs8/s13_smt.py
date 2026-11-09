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
        head = label("Trace scheduler: one program, four start slots", font_size=36).to_edge(UP, buff=0.35)
        g = slots(d["slots_alone"], colors=(DATA,)).move_to(UP * 0.6)
        lab = note("oracle start slots: \\ 4 per cycle, \\ 24-cycle sample", font_size=20).next_to(g, UP, buff=0.2)
        used = sum(min(x, 4) for x in d["slots_alone"])
        facts = VGroup(
            label(rf"here {used} of {4 * len(d['slots_alone'])} slots are used", font_size=24, color=DATA),
            label(rf"functional core: retired IPC {h['ooo']['ipc']:.2f}; \ issue utilization is a different metric",
                  font_size=24, color=NO),
            label("sharing can improve aggregate throughput; \\ this is an oracle study", font_size=26, color=HEAD),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This grid shows starts in a twenty-four-cycle sample from the offline trace scheduler, with four start "
            "slots per cycle. It is not an issue-activity recording from the functional core. <bookmark mark='a'/> "
            "Fifty-eight of its ninety-six displayed slots contain scheduled instructions. The empty cells are "
            "directly counted in this particular sample. <bookmark mark='b'/> Separately, the functional core "
            "retires about one point nine instructions per cycle. Retired IPC cannot tell us how many issue slots "
            "were used: wrong-path and replayed operations may execute without retiring. Our implementation also "
            "has a different total execution-start limit from its four-wide front end. <bookmark mark='c'/> The "
            "useful question is whether another independent thread can share resources and improve aggregate "
            "throughput, under an explicitly stated scheduling model. Neither the grid nor retired IPC measures "
            "powered idle hardware or energy consumption."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.frame), FadeIn(lab))
            self.play(LaggedStart(*[FadeIn(u) for u in g.used], lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
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
            label("real SMT needs per-thread architectural, retirement and recovery state", font_size=23,
                  color=GREY_A),
            label("queue ownership, resource sharing and partitioning are design choices", font_size=23,
                  color=GREY_A),
            label("this scheduler gives each thread independent control barriers", font_size=23, color=YES),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Simultaneous multithreading lets operations from different threads share execution resources. Tullsen, "
            "Eggers and Levy's 1995 paper is an influential study of this approach. <bookmark mark='a'/> Here we "
            "interleave two known Job traces in an offline oracle scheduler, sharing four start slots and giving "
            "each thread its own dependency state, control barriers and half of the start-distance allowance. This "
            "is not a functionally verified SMT implementation of Pebble. <bookmark mark='b'/> Real SMT needs "
            "per-thread architectural, retirement, exception and recovery state, plus ownership information for "
            "shared queues. PCs, register mappings and branch history alone are not enough. Sharing and "
            "partitioning policies vary by design. <bookmark mark='c'/> The colored grid illustrates how one thread "
            "can use cycles where another lacks ready work. Actual fairness, cache contention, recovery and "
            "isolation require a fuller machine and workload analysis."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.frame), FadeIn(leg))
            self.play(LaggedStart(*[FadeIn(u) for u in g.used], lag_ratio=0.015), run_time=2.0)
            vo.wait_until("a")
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
            label("evaluate per-thread latency, fairness, energy and isolation separately",
                  font_size=22, color=NO),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "These bars report combined throughput in the same offline scheduling study. The traces are truncated "
            "to equal instruction counts, and both must finish. <bookmark mark='a'/> With four start slots and the "
            "stated lookahead allowance, one trace averages about two point seven instructions per cycle; the two "
            "together reach about three point seven. <bookmark mark='b'/> At eight slots, the aggregate improvement "
            "is larger for these particular traces and assumptions. This is not a universal scaling rule or a "
            "measurement of a production SMT processor. <bookmark mark='c'/> Real sharing can improve aggregate "
            "throughput while slowing an individual thread, and results depend on workload, partitioning and "
            "contention. Fairness, latency, energy and security are separate evaluation axes. Timing interactions "
            "between threads can also expose information, so throughput alone is not a complete design objective."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yl))
            for mk, gr in zip("ab", groups):
                if mk != "a":
                    vo.wait_until(mk)
                self.play(FadeIn(gr[0]), FadeIn(gr[1][0]), GrowFromEdge(gr[1].bars[0], DOWN),
                          GrowFromEdge(gr[1].bars[1], DOWN), FadeIn(gr[1].vals), FadeIn(gr[1].names))
                self.play(FadeIn(gr[2]))
                if mk == "a":
                    vo.wait_until(mk)
            vo.wait_until("c")
            self.play(FadeIn(real))
        self.wait(0.3)
        self.clear_scene()
