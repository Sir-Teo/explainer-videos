from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, COST, DATA, HEAD, KERN, LAM, NO, PART, YES, curve, fit_right, gantt, load,
                                   time_axis)

TC = {"T1": DATA, "T2": HEAD}


def tagged(segs):
    return [(a, b, f"T{k + 1}") for a, b, k in segs]


class RealTime(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_tasks()
        self.bound()
        self.pathfinder()

    def card(self):
        card = chapter_card(11, r"Real time", r"How do you promise a deadline?", lit=(1973, 1997),
                            extra=((1973, r"Liu and Layland"), (1997, r"Mars Pathfinder")), part=PART)
        with self.voiceover("Chapter eleven. Real time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def two_tasks(self):
        d = load("realtime")
        head = label(r"Two periodic tasks, \ 97\% busy", font_size=36).to_edge(UP, buff=0.3)
        (c1, t1), (c2, t2) = d["tasks"]
        spec = label(rf"T1: \ {c1} ticks of work every {t1}; \ \ T2: \ {c2} every {t2}; \ \ each due before its next "
                     rf"release; \ \ $U = {c1}/{t1} + {c2}/{t2} = {d['U']:.3f}$", font_size=21, color=WHITE).next_to(
            head, DOWN, buff=0.35)
        H = 35
        g1 = gantt(tagged(d["rms"]["segments"]), 0, H, width=10.5, h=0.42, lanes=["T1", "T2"],
                   colors=TC, font=18).move_to([0.4, 1.0, 0])
        g2 = gantt(tagged(d["edf"]["segments"]), 0, H, width=10.5, h=0.42, lanes=["T1", "T2"],
                   colors=TC, font=18).move_to([0.4, -1.1, 0])
        a1 = time_axis(g1, list(range(0, 36, 5)), font=13)
        a2 = time_axis(g2, list(range(0, 36, 5)), font=13)
        l1 = label(r"rate monotonic: \ shorter period, \ higher priority, \ fixed", font_size=20, color=GREY_A).next_to(
            g1, UP, buff=0.12).align_to(g1, LEFT)
        l2 = label(r"earliest deadline first: \ priorities change as deadlines approach", font_size=20,
                   color=YES).next_to(g2, UP, buff=0.12).align_to(g2, LEFT)
        mt, md = d["rms"]["misses"][0]
        miss = VGroup(Cross(scale_factor=0.16, stroke_color=NO, stroke_width=4).move_to(
            [g1.x(md), g1.lane_labels[1].get_center()[1], 0]),
            label(rf"T2 misses its deadline at {md}", font_size=18, color=NO))
        miss[1].next_to(miss[0], RIGHT, buff=0.2).shift(DOWN * 0.42)
        lines = VGroup(
            label(r"EDF meets every deadline whenever $U \le 1$: \ it is \textbf{optimal} on one processor \ (Liu and "
                  r"Layland, \ 1973)", font_size=21, color=YES),
            label(r"so why fixed priorities? \ simpler, \ and when overloaded they fail predictably: \ the lowest "
                  r"priority first", font_size=21, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In a car's brakes or an aircraft's controls, a late answer is a wrong answer. Real-time systems run "
            "periodic tasks, each needing some work every period, finished before the next one starts. <bookmark "
            "mark='a'/> Task one needs two ticks every five, and task two four ticks every seven. Together they keep "
            "the processor ninety-seven percent busy. <bookmark mark='b'/> The classic scheme gives fixed priorities "
            "by rate: the shorter the period, the higher the priority. That is rate-monotonic scheduling. <bookmark "
            "mark='c'/> At tick seven, task two has had only three of its four ticks, because task one keeps "
            "preempting it. It misses its deadline. <bookmark mark='d'/> Earliest deadline first instead runs "
            "whichever task's deadline is nearest, so priorities change from moment to moment. It meets every "
            "deadline. <bookmark mark='e'/> Liu and Layland proved in 1973 that on one processor, earliest deadline "
            "first succeeds whenever the total utilisation is at most one, which nothing can beat. <bookmark "
            "mark='f'/> Fixed priorities are still the common choice: they are simple, and when the system is "
            "overloaded, it is always the lowest-priority task that suffers, which engineers can plan for."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(spec))
            vo.wait_until("b")
            self.play(FadeIn(l1), FadeIn(g1.lane_labels), FadeIn(a1),
                      LaggedStart(*[FadeIn(b) for b in g1.bars], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(miss))
            vo.wait_until("d")
            self.play(FadeIn(l2), FadeIn(g2.lane_labels), FadeIn(a2),
                      LaggedStart(*[FadeIn(b) for b in g2.bars], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(lines[0]))
            vo.wait_until("f")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()

    def bound(self):
        d = load("realtime")
        head = label(r"How busy can rate monotonic be?", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0.5, 1.0, 0.1], y_range=[0, 1.0, 0.25], x_length=6.2, y_length=3.6,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.4)
        xt = VGroup(*[label(f"{x:.1f}", font_size=15, color=GREY_A).next_to(ax.c2p(x, 0), DOWN, buff=0.08)
                      for x in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0)])
        yt = VGroup(*[label(f"{int(y * 100)}\\%", font_size=15, color=GREY_A).next_to(ax.c2p(0.5, y), LEFT,
                                                                                    buff=0.08)
                      for y in (0, 0.25, 0.5, 0.75, 1.0)])
        xl = label(r"utilisation $U$ \ (4 random tasks)", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"task sets that meet every deadline", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(
            ax, LEFT)
        cv = d["curve"]
        c_edf = curve(ax, [c["U"] for c in cv], [c["edf"] for c in cv], YES)
        c_rms = curve(ax, [c["U"] for c in cv], [c["rms"] for c in cv], DATA)
        c_ll = curve(ax, [c["U"] for c in cv], [c["ll"] for c in cv], GREY_B)
        ll4 = d["bounds"][3][1]
        vline = DashedLine(ax.c2p(ll4, 0), ax.c2p(ll4, 1.0), color=HEAD, stroke_width=1.5)
        keys = VGroup(label(r"EDF", font_size=18, color=YES), label(r"RMS, \ exact test", font_size=18, color=DATA),
                      label(r"the Liu--Layland test", font_size=18, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.08)
        keys.move_to(ax.c2p(0.62, 0.3))
        bl = ", \\ ".join(f"{b:.3f}" for _, b in d["bounds"][:4])
        h = d["harmonic"]
        notes = VGroup(
            label(r"Liu and Layland: \ RMS meets every deadline if", font_size=20, color=WHITE),
            MathTex(r"U \le n\,(2^{1/n} - 1) \;\to\; \ln 2 \approx 0.693", font_size=32, color=HEAD),
            label(rf"$n = 1, 2, 3, 4$: \ {bl}", font_size=19, color=GREY_A),
            label(r"the worst case: \ all tasks released together, \\ periods within a factor of two, \ each just "
                  r"filling the gap", font_size=19, color=GREY_A),
            label(r"sufficient, \ not necessary: \ the exact test \\ (response-time analysis) \ accepts far more",
                  font_size=19, color=DATA),
            label(rf"harmonic periods 10, 20, 40 at $U = 0.875$: \ fine \\ (worst responses {h[0]}, {h[1]}, {h[2]})",
                  font_size=19, color=YES),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP).shift(UP * 0.4)
        fit_right(notes)
        with self.voiceover(
            "For rate-monotonic scheduling, Liu and Layland found a simple sufficient test. <bookmark mark='a'/> If "
            "the utilisation is at most n times two to the one over n, minus one, every deadline is met. For one "
            "task that is a hundred percent; for two, eighty-three; for four, seventy-six; and as n grows it falls to "
            "the natural logarithm of two, about sixty-nine percent. <bookmark mark='b'/> The proof sketch: the worst "
            "moment is when all tasks are released together, and the worst task set has periods within a factor of "
            "two, each task's work just filling the gap between the next two periods. <bookmark mark='c'/> But the "
            "test is only sufficient. We generated random sets of four tasks at each utilisation. <bookmark "
            "mark='d'/> The Liu-Layland test accepts almost nothing above seventy-six percent. The exact test, which "
            "computes each task's worst response time, accepts every set up to eighty percent, and most up to ninety. "
            "<bookmark mark='e'/> Earliest deadline first meets them all, up to a hundred. <bookmark mark='f'/> And "
            "when the periods divide one another, rate monotonic can use the whole processor: periods of ten, twenty "
            "and forty, at eighty-seven and a half percent, are comfortably on time."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(notes[1]), FadeIn(notes[2]))
            vo.wait_until("b")
            self.play(FadeIn(notes[3]))
            vo.wait_until("c")
            self.play(FadeIn(notes[4]))
            vo.wait_until("d")
            self.play(Create(c_ll), Create(c_rms), Create(vline), FadeIn(keys[1:]), run_time=2.0)
            vo.wait_until("e")
            self.play(Create(c_edf), FadeIn(keys[0]))
            vo.wait_until("f")
            self.play(FadeIn(notes[5]))
        self.wait(0.3)
        self.clear_scene()

    def pathfinder(self):
        d = load("realtime")
        head = label(r"Mars, \ July 1997: \ the lander keeps resetting", font_size=34).to_edge(UP, buff=0.3)
        lanes = ["bus", "comms", "meteo"]
        g1 = gantt(d["pf_no"]["segments"], 0, 46, width=10.0, h=0.36, lanes=lanes, font=17).move_to([0.6, 1.5, 0])
        g2 = gantt(d["pf_pi"]["segments"], 0, 46, width=10.0, h=0.36, lanes=lanes, font=17).move_to([0.6, -0.9, 0])
        a2 = time_axis(g2, [0, 10, 20, 30, 40], font=13)
        t1 = label(r"without priority inheritance", font_size=20, color=NO).next_to(g1, UP, buff=0.12).align_to(g1,
                                                                                                             LEFT)
        t2 = label(r"with priority inheritance", font_size=20, color=YES).next_to(g2, UP, buff=0.12).align_to(g2,
                                                                                                         LEFT)
        dl = d["pf_no"]["deadline"]
        dead1 = DashedLine([g1.x(dl), g1.get_top()[1], 0], [g1.x(dl), g1.get_bottom()[1], 0], color=NO)
        dead2 = DashedLine([g2.x(dl), g2.get_top()[1], 0], [g2.x(dl), g2.get_bottom()[1], 0], color=GREY_B)
        r1 = label(rf"bus finishes at {d['pf_no']['bus_done']}: \ past its deadline \ ({dl}): \ the watchdog resets",
                   font_size=18, color=NO).next_to(g1, DOWN, buff=0.15).align_to(g1, LEFT)
        r2 = label(rf"bus finishes at {d['pf_pi']['bus_done']}", font_size=18, color=YES).next_to(a2, DOWN,
                                                                                               buff=0.1).align_to(g2,
                                                                                                                  LEFT)
        lines = VGroup(
            label(r"meteo \ (low) \ holds the bus mutex; \ bus \ (high) \ waits for it; \ comms \ (medium) \ preempts "
                  r"meteo: \ \textbf{priority inversion}", font_size=19, color=WHITE),
            label(r"the fix: \ a mutex holder runs at the priority of its most urgent waiter \ (Sha, Rajkumar and "
                  r"Lehoczky, 1990)", font_size=19, color=YES),
            label(r"JPL reproduced it on a ground copy, \ and uploaded one changed setting in VxWorks", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Days after Mars Pathfinder landed in July 1997, its computer started resetting itself. <bookmark "
            "mark='a'/> Three tasks matter. A low-priority meteorological task takes a lock on the information bus. "
            "The high-priority bus manager arrives and waits for the lock. Then a medium-priority communications "
            "task, which needs no lock, preempts the meteorological task, and runs for a long time. <bookmark "
            "mark='b'/> The high-priority task is now stuck behind a medium-priority one: priority inversion. It "
            "misses its deadline, and a watchdog concludes that something is badly wrong and resets the system. "
            "<bookmark mark='c'/> The cure is priority inheritance: while a task holds a lock that a higher-priority "
            "task wants, it runs at that higher priority. <bookmark mark='d'/> Now the meteorological task finishes "
            "with the lock quickly, and the bus manager is done at tick thirteen. <bookmark mark='e'/> Engineers at "
            "the Jet Propulsion Laboratory reproduced the fault on a copy of the spacecraft on Earth, and fixed it by "
            "uploading a change to one setting of the VxWorks operating system, turning inheritance on."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(g1.lane_labels), LaggedStart(*[FadeIn(b) for b in g1.bars], lag_ratio=0.3),
                      FadeIn(lines[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(dead1), FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(t2), FadeIn(g2.lane_labels), FadeIn(a2),
                      LaggedStart(*[FadeIn(b) for b in g2.bars], lag_ratio=0.3), Create(dead2), FadeIn(r2),
                      run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()
