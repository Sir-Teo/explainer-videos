from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs31.common import (BG, COST, DATA, HEAD, KERN, LAM, NO, PART, YES, curve, fit_right, gantt,
                                   grid_table, load, time_axis)


class Mlfq(VoiceoverScene):
    def construct(self):
        self.card()
        self.rr()
        self.quantum()
        self.rules()
        self.gaming()

    def card(self):
        card = chapter_card(8, r"Round robin and the multi-level feedback queue",
                            r"How can a scheduler favour jobs it knows nothing about?",
                            lit=(1962,), extra=((1962, r"Corbat\'o: \ MLFQ"),), part=PART)
        with self.voiceover("Chapter eight. Round robin, and the multi-level feedback queue."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def rr(self):
        d = load("sched")
        head = label(r"Round robin: \ take turns", font_size=36).to_edge(UP, buff=0.3)
        g1 = gantt(d["rr_fcfs"]["segments"], 0, 90, width=9.0, h=0.55).move_to([-1.0, 1.6, 0])
        g2 = gantt(d["rr_rr"]["segments"], 0, 90, width=9.0, h=0.55).move_to([-1.0, 0.1, 0])
        ax = time_axis(g2, [0, 30, 60, 90], font=14)
        l1 = label(r"FCFS", font_size=21, color=WHITE).next_to(g1, UP, buff=0.12).align_to(g1, LEFT)
        l2 = label(r"round robin, \ quantum 5", font_size=21, color=YES).next_to(g2, UP, buff=0.12).align_to(g2, LEFT)
        f, r = d["rr_fcfs"]["metrics"]["mean"], d["rr_rr"]["metrics"]["mean"]
        m1 = label(rf"response {f['response']:.0f}, \ turnaround {f['turnaround']:.0f}", font_size=19,
                   color=GREY_A).next_to(g1, RIGHT, buff=0.25)
        m2 = label(rf"response {r['response']:.0f}, \ turnaround {r['turnaround']:.0f}", font_size=19,
                   color=GREY_A).next_to(g2, RIGHT, buff=0.25)
        fit_right(m1)
        fit_right(m2)
        lines = VGroup(
            label(r"three jobs of 30 ticks: \ round robin answers everyone within one round", font_size=21,
                  color=WHITE),
            label(r"but everyone finishes late: \ turnaround is \textbf{worse} than FCFS for equal jobs", font_size=21,
                  color=NO),
            label(r"CTSS's scheme: \ a timer interrupt every quantum, \ and the next ready job", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.16).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "For people at keyboards, response time is what matters, and the fix is to take turns. <bookmark "
            "mark='a'/> Three jobs of thirty ticks each. First come first served answers the third job only after "
            "sixty ticks. <bookmark mark='b'/> Round robin gives each job a quantum of five ticks, then moves to the "
            "next: every job starts within ten ticks, and the mean response time falls from thirty to five. "
            "<bookmark mark='c'/> But look at the finish times. Every job is still running near the end, so the mean "
            "turnaround rises from sixty to eighty-five. For jobs of equal length, round robin is the worst order "
            "for turnaround. <bookmark mark='d'/> This is the time-sharing of CTSS: a timer interrupt at the end of "
            "every quantum, and the next ready job."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(l1), LaggedStart(*[FadeIn(b) for b in g1.bars], lag_ratio=0.3), FadeIn(m1),
                      FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(l2), FadeIn(ax), LaggedStart(*[FadeIn(b) for b in g2.bars], lag_ratio=0.1),
                      FadeIn(m2))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def quantum(self):
        d = load("sched")
        head = label(r"How long a quantum?", font_size=36).to_edge(UP, buff=0.3)
        sw = d["sweep"]
        ax = Axes(x_range=[0, 2.0, 0.5], y_range=[0, 140, 20], x_length=6.2, y_length=3.8,
                  axis_config={"color": GREY_D, "include_numbers": False}).to_edge(LEFT, buff=1.0).shift(DOWN * 0.2)
        xs = [1, 3, 10, 30, 100]
        xt = VGroup(*[label(str(x), font_size=15, color=GREY_A).next_to(ax.c2p(math.log10(x), 0), DOWN, buff=0.08)
                      for x in xs])
        yt = VGroup(*[label(str(y), font_size=15, color=GREY_A).next_to(ax.c2p(0, y), LEFT, buff=0.08)
                      for y in range(0, 141, 20)])
        xl = label(r"quantum \ (ticks; \ a switch costs one tick)", font_size=17, color=GREY_A).next_to(xt, DOWN,
                                                                                                    buff=0.1)
        yl = label(r"mean response time", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        cv = curve(ax, [math.log10(s["q"]) for s in sw], [s["response"] for s in sw], YES)
        best = min(sw, key=lambda s: s["response"])
        bd = Dot(ax.c2p(math.log10(best["q"]), best["response"]), color=HEAD, radius=0.08)
        notes = VGroup(
            label(rf"quantum 1: \ half the processor goes on \\ switching \ ({sw[0]['overhead'] * 100:.0f}\%); \ the "
                  r"queue explodes", font_size=21, color=NO),
            label(rf"quantum {best['q']}: \ the best here, \ {best['response']:.0f} ticks", font_size=21, color=HEAD),
            label(r"quantum 80: \ nearly FCFS again", font_size=21, color=GREY_A),
            label(r"real kernels: \ quanta of milliseconds, \\ switches of microseconds: \\ under 1\% overhead",
                  font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(ax, RIGHT, buff=0.5).align_to(ax, UP)
        fit_right(notes)
        with self.voiceover(
            "How long should the quantum be? We ran round robin on the four hundred random jobs, charging one tick "
            "for every switch. <bookmark mark='a'/> With a quantum of one tick, half the processor's time goes on "
            "switching. The machine is effectively overloaded and the queue explodes. <bookmark mark='b'/> Around "
            "twelve ticks, the response time is lowest. <bookmark mark='c'/> And with a very long quantum, round "
            "robin turns back into first come first served. <bookmark mark='d'/> Real kernels choose quanta of a few "
            "milliseconds, a thousand times longer than a switch, so switching costs under one percent."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            self.play(Create(cv), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(bd), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.3)
        self.clear_scene()

    def rules(self):
        d = load("mlfq")
        b = d["basic"]
        head = label(r"The multi-level feedback queue", font_size=36).to_edge(UP, buff=0.3)
        rules = VGroup(*[label(t, font_size=23, color=c) for t, c in (
            (r"1. \ a higher queue always runs first; \ 2. \ within a queue, \ round robin", WHITE),
            (r"3. \ a new job starts at the top \ (quantum 10, \ then 20, \ then 40)", YES),
            (r"4. \ a job that uses up its allotment at a level moves down one", NO),
            (r"5. \ every so often, \ move every job back to the top", HEAD))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.14)
        rules.next_to(head, DOWN, buff=0.35).to_edge(LEFT, buff=0.7)
        segs = b["segments"]
        g = gantt(segs, 0, 101, width=10.0, h=0.42, lanes=["H1", "H2", "I"], font=18).move_to([0.6, -0.9, 0])
        ax = time_axis(g, [0, 25, 50, 75, 100], font=13)
        lines = VGroup(
            label(rf"I \ (1 tick of work, \ then 9 of I/O) \ runs the moment it is ready: \ response {b['resp_I']:.0f}"
                  rf"; \ finished at {b['turn_I']:.0f}, \ against {b['rr_turn_I']:.0f} under round robin",
                  font_size=20, color=YES),
            label(r"the hogs sink to the bottom queue and share what is left: \ no lengths needed, \ only behaviour",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Shortest first needs to know the future. Round robin ignores it. Corbató's multi-level feedback queue, "
            "from CTSS in 1962, learns it from behaviour. <bookmark mark='a'/> There are several queues, each with a "
            "priority. A higher queue always runs first, and within a queue jobs take turns. <bookmark mark='b'/> "
            "Every new job starts at the top, where the quantum is short. <bookmark mark='c'/> A job that uses up "
            "its allotted time at a level is demoted: it has shown that it computes for long stretches. <bookmark "
            "mark='d'/> And every so often, every job goes back to the top. We will see why. <bookmark mark='e'/> "
            "Here are two long computations, H1 and H2, and an interactive job, I, which computes for one tick and "
            "then waits nine for input. The hogs sink to the bottom. I never uses up its allotment, stays at the top, "
            "and runs the moment it is ready. <bookmark mark='f'/> It finishes at three hundred and forty-one ticks, "
            "against six hundred and forty-one under round robin, and nobody told the scheduler which job was which."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rules):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(g.lane_labels), FadeIn(ax), LaggedStart(*[FadeIn(x) for x in g.bars], lag_ratio=0.03),
                      run_time=2.5)
            vo.wait_until("f")
            self.play(FadeIn(lines))
        self.wait(0.3)
        self.clear_scene()

    def gaming(self):
        d = load("mlfq")
        head = label(r"Gaming the scheduler, \ and starving", font_size=36).to_edge(UP, buff=0.3)
        gm = d["game"]
        st = d["starve"]
        tab = grid_table([r"", r"the hog", r"the gamer", r"of 1000 ticks"], [
            [r"old rule: \ allotment resets on any I/O", str(gm["old"]["hog"]), str(gm["old"]["gamer"]), r""],
            [r"rule 4: \ allotment counted in total", str(gm["new"]["hog"]), str(gm["new"]["gamer"]), r""],
        ], widths=[5.6, 1.8, 1.8, 2.4], row_h=0.55, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        tab.cells[1][2].set_color(NO)
        tab.cells[2][1].set_color(YES)
        lines = VGroup(
            label(r"the gamer computes for 9 ticks, \ then does 1 tick of I/O, \ just inside the quantum of 10",
                  font_size=21, color=WHITE),
            label(r"under the old rule it stays on top for ever, \ and takes 89\% of the machine", font_size=21,
                  color=NO),
            label(rf"starvation: \ three interactive jobs keep the top queue busy; \ a long job gets "
                  rf"{st['none']['long']} ticks in 1500", font_size=21, color=NO),
            label(rf"the boost \ (rule 5, \ every 200 ticks) \ guarantees it {st['200']['long']}", font_size=21,
                  color=HEAD),
            label(r"MLFQ in practice: \ Solaris, \ the BSDs, \ and Windows NT's priority boosts", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.17).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Any rule based on behaviour can be gamed. The first version of rule four reset a job's allotment "
            "whenever it gave up the processor for input or output. <bookmark mark='a'/> So a clever program "
            "computes for nine ticks, does a token one-tick read, and computes again, always just inside its "
            "quantum of ten. <bookmark mark='b'/> It never looks like a hog, stays in the top queue, and takes "
            "eighty-nine percent of the machine. Counting each job's time at a level in total, however it is broken "
            "up, fixes this: the gamer drops to seventeen percent. <bookmark mark='c'/> The other danger is "
            "starvation. With three interactive jobs keeping the top queue busy, a long job at the bottom got ten "
            "ticks in fifteen hundred. <bookmark mark='d'/> Rule five, the periodic boost to the top, guarantees it a "
            "slice every two hundred ticks. <bookmark mark='e'/> Variants of this design scheduled Solaris and the "
            "BSD systems, and Windows still boosts the priority of threads that have just finished waiting."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[1])), FadeIn(lines[1]))
            self.play(FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
            vo.wait_until("e")
            self.play(FadeIn(lines[4]))
        self.wait(0.3)
        self.clear_scene()
