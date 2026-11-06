from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, gantt, grid_table, load, time_axis)


def mean_tag(m, color, g):
    return label(rf"mean turnaround {m['turnaround']:.0f}", font_size=20, color=color).next_to(g, RIGHT, buff=0.3)


class Scheduling(VoiceoverScene):
    def construct(self):
        self.card()
        self.metrics()
        self.convoy()
        self.exchange()
        self.preempt()

    def card(self):
        card = chapter_card(7, r"Scheduling: \ FCFS, \ SJF, \ SRTF", r"Which job should run next?",
                            lit=(1968,), extra=((1968, r"Schrage: \ SRPT is optimal"),), part=PART)
        with self.voiceover("Chapter seven. Scheduling: first come first served, shortest job first, and shortest "
                            "remaining time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def metrics(self):
        head = label(r"What should a scheduler optimise?", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"measure", r"definition", r"who cares"], [
            [r"turnaround", r"finish $-$ arrival", r"batch jobs"],
            [r"response", r"first run $-$ arrival", r"people at keyboards"],
            [r"waiting", r"time ready but not running", r"everyone"],
            [r"throughput", r"jobs finished per second", r"the owner of the machine"],
            [r"fairness", r"similar jobs, \ similar treatment", r"the users"],
        ], widths=[2.6, 4.6, 4.2], row_h=0.52, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        line = label(r"they conflict: \ the best order for turnaround is unfair to long jobs, \ and switching for "
                     r"response costs throughput", font_size=21, color=HEAD).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A scheduler decides which ready process runs next. What should it optimise? <bookmark mark='a'/> For a "
            "batch job, the turnaround time: from arrival to finish. For a person at a keyboard, the response time: "
            "how long until the program first does something. The waiting time: how long a job sat ready but not "
            "running. The throughput: how many jobs finish per second. And fairness. <bookmark mark='b'/> These "
            "conflict. We will see that the best order for turnaround starves long jobs, and that switching often "
            "for good response time costs throughput."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(line))
        self.wait(0.3)
        self.clear_scene()

    def convoy(self):
        d = load("sched")
        head = label(r"First come, \ first served, \ and the convoy", font_size=34).to_edge(UP, buff=0.3)
        g1 = gantt(d["convoy_fcfs"]["segments"], 0, 120, width=9.0, h=0.6).move_to([-1.2, 1.3, 0])
        a1 = time_axis(g1, [0, 20, 40, 60, 80, 100, 120], font=14)
        g2 = gantt(d["convoy_sjf"]["segments"], 0, 120, width=9.0, h=0.6).move_to([-1.2, -0.7, 0])
        a2 = time_axis(g2, [0, 20, 40, 60, 80, 100, 120], font=14)
        l1 = label(r"FCFS", font_size=22, color=WHITE).next_to(g1, UP, buff=0.15).align_to(g1, LEFT)
        l2 = label(r"shortest job first", font_size=22, color=YES).next_to(g2, UP, buff=0.15).align_to(g2, LEFT)
        m1 = mean_tag(d["convoy_fcfs"]["metrics"]["mean"], NO, g1)
        m2 = mean_tag(d["convoy_sjf"]["metrics"]["mean"], YES, g2)
        lines = VGroup(
            label(r"A needs 100 ticks; \ B and C need 10 each; \ all arrive at once", font_size=21, color=WHITE),
            label(r"FCFS: \ B and C wait behind A \ (the \textbf{convoy effect}): \ finish times 100, \ 110, \ 120",
                  font_size=21, color=NO),
            label(r"run the short ones first: \ 10, \ 20, \ 120: \ the mean drops from 110 to 50", font_size=21,
                  color=YES),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The simplest scheduler runs jobs in the order they arrive, to completion: first come, first served. "
            "<bookmark mark='a'/> Three jobs arrive together. A needs a hundred ticks of processor time, B and C need "
            "ten each. <bookmark mark='b'/> If A happens to be first, B and C wait behind it, like cars behind a "
            "truck on a mountain road. The finish times are a hundred, a hundred and ten, and a hundred and twenty: a "
            "mean turnaround of a hundred and ten. This is the convoy effect. <bookmark mark='c'/> Run the short "
            "jobs first instead, and they finish at ten and twenty, and A still finishes at a hundred and twenty. "
            "The mean falls to fifty."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(l1), FadeIn(a1), LaggedStart(*[FadeIn(b) for b in g1.bars], lag_ratio=0.4), FadeIn(m1),
                      FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(l2), FadeIn(a2), LaggedStart(*[FadeIn(b) for b in g2.bars], lag_ratio=0.4), FadeIn(m2),
                      FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def exchange(self):
        head = label(r"Shortest first is optimal: \ the exchange argument", font_size=34).to_edge(UP, buff=0.3)
        W = 10.0
        sc = W / 60

        def bars(order):
            g = VGroup()
            x = -W / 2
            for name, L, c in order:
                r = Rectangle(width=L * sc, height=0.6, stroke_color=BG, stroke_width=1, fill_color=c,
                              fill_opacity=0.85).move_to([x + L * sc / 2, 0, 0])
                g.add(VGroup(r, label(name, font_size=20, color=GREY_A if c is GREY_D else BG).move_to(r)))
                x += L * sc
            return g
        before = bars([("earlier jobs", 14, GREY_D), ("long", 24, NO), ("short", 8, YES), ("later", 14, GREY_D)])
        after = bars([("earlier jobs", 14, GREY_D), ("short", 8, YES), ("long", 24, NO), ("later", 14, GREY_D)])
        before.move_to([0, 1.3, 0])
        after.move_to([0, -0.2, 0])
        tb = label(r"a long job $L$ just before a short one $S$", font_size=20, color=GREY_A).next_to(before, UP,
                                                                                                    buff=0.15)
        ta = label(r"swap them", font_size=20, color=GREY_A).next_to(after, UP, buff=0.15)
        math_ = VGroup(
            label(r"the short job now finishes $L$ earlier; \ the long one $S$ later; \ nobody else moves", font_size=21,
                  color=WHITE),
            label(r"total completion time changes by $S - L < 0$: \ the swap helps", font_size=21, color=YES),
            label(r"so in an optimal order no long job precedes a short one: \ \textbf{shortest first minimises the mean}",
                  font_size=21, color=HEAD),
            label(r"the same argument, \ run at every arrival, \ proves SRPT optimal \ (Schrage, 1968)", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Shortest first is not just better here: for jobs that are all present at the start, it is the best "
            "possible order, and the proof is a single swap. <bookmark mark='a'/> Take any order in which a long job, "
            "of length L, runs immediately before a short one, of length S. <bookmark mark='b'/> Swap them. <bookmark "
            "mark='c'/> The short job now finishes L earlier, the long one finishes S later, and every other job "
            "finishes at the same time as before. <bookmark mark='d'/> So the total of the completion times changes "
            "by S minus L, which is negative. <bookmark mark='e'/> An order with a long job before a short one can "
            "always be improved, so the best order has none: shortest first. <bookmark mark='f'/> The same exchange, "
            "made whenever a new job arrives, shows that shortest remaining processing time first is optimal even "
            "when jobs arrive over time. Linus Schrage proved it in 1968."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(before), FadeIn(tb))
            vo.wait_until("b")
            self.play(FadeIn(ta), TransformFromCopy(before, after), run_time=1.5)
            for mk, ln in zip("cdef", math_):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()

    def preempt(self):
        d = load("sched")
        head = label(r"Preemption: \ shortest remaining time first", font_size=34).to_edge(UP, buff=0.3)
        g1 = gantt(d["late_sjf"]["segments"], 0, 120, width=8.4, h=0.55).move_to([-1.5, 2.0, 0])
        g2 = gantt(d["late_srtf"]["segments"], 0, 120, width=8.4, h=0.55).move_to([-1.5, 0.75, 0])
        l1 = label(r"SJF", font_size=21, color=WHITE).next_to(g1, LEFT, buff=0.2)
        l2 = label(r"SRTF", font_size=21, color=YES).next_to(g2, LEFT, buff=0.2)
        m1 = mean_tag(d["late_sjf"]["metrics"]["mean"], NO, g1)
        m2 = mean_tag(d["late_srtf"]["metrics"]["mean"], YES, g2)
        ax = time_axis(g2, [0, 10, 40, 80, 120], font=14)
        r = d["random"]
        tab = grid_table([r"400 random jobs, \ load 0.8", r"FCFS", r"SJF", r"SRTF", r"RR"], [
            [r"mean turnaround"] + [f"{r[p]['turnaround']:.1f}" for p in ("fcfs", "sjf", "srtf", "rr")],
            [r"mean response"] + [f"{r[p]['response']:.1f}" for p in ("fcfs", "sjf", "srtf", "rr")],
        ], widths=[4.0, 1.6, 1.6, 1.6, 1.6], row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(ax, DOWN, buff=0.45)
        line = label(r"the catch: \ the scheduler must \textbf{know} the lengths; \ real ones guess from each "
                     r"process's past bursts", font_size=21, color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Jobs do not all arrive at the start. <bookmark mark='a'/> Here A starts alone, and B and C arrive ten "
            "ticks later. Shortest job first never interrupts a running job, so B and C wait for all of A: a mean "
            "turnaround of a hundred and three. <bookmark mark='b'/> Shortest remaining time first preempts: when B "
            "arrives needing ten ticks, and A still needs ninety, A is set aside. The mean falls to fifty. <bookmark "
            "mark='c'/> On four hundred random jobs arriving at eighty percent load, shortest remaining time first "
            "has the best mean turnaround, half that of first come first served. Round robin, the next chapter, has "
            "the best response time. <bookmark mark='d'/> But all of this assumes the scheduler knows how long each "
            "job will run, and it does not. Real schedulers guess, from how long each process ran the last few "
            "times."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(l1), LaggedStart(*[FadeIn(b) for b in g1.bars], lag_ratio=0.3), FadeIn(m1))
            vo.wait_until("b")
            self.play(FadeIn(l2), FadeIn(ax), LaggedStart(*[FadeIn(b) for b in g2.bars], lag_ratio=0.3), FadeIn(m2))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(line))
        self.wait(0.3)
        self.clear_scene()
