from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Reduction(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_variables()
        self.phase_plane()
        self.two_ways()

    def card(self):
        card = chapter_card(8, r"Two variables are enough", r"How much of the model can be thrown away?",
                            lit={1961: r"FitzHugh's two-variable model"}, part=PART, scale=("neuron",), marr=("how",))
        with self.voiceover(
            "Chapter eight. Two variables are enough."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two_variables(self):
        d = load("fhn")
        head = heading(r"From four variables to two")
        four = VGroup(*[label(t, font_size=40, color=c) for t, c in ((r"$V$", VOLT), (r"$m$", GATE["m"]),
                                                                    (r"$h$", GATE["h"]), (r"$n$", GATE["n"]))])
        four.arrange(RIGHT, buff=0.9).move_to([0, 2.0, 0])
        notes = VGroup(
            wrapped_label(r"$m$ is so fast that it is always where the voltage says it should be: \ fold it "
                          r"into $V$.", 5.6, 27, GATE["m"]),
            wrapped_label(r"$h$ and $n$ are both slow, and move together: \ one recovery variable will do for "
                          r"both.", 5.6, 27, GATE["n"]),
        ).arrange(RIGHT, buff=0.8, aligned_edge=UP).move_to([0, 0.5, 0])
        two = VGroup(
            MathTex(r"\frac{dv}{dt} \;=\; v - \frac{v^3}{3} - w + I", font_size=44, color=VOLT),
            MathTex(rf"\frac{{dw}}{{dt}} \;=\; \varepsilon\,(v + a - b\,w)", font_size=44, color=GATE["n"]),
        ).arrange(RIGHT, buff=1.2).move_to([0, -1.3, 0])
        names = VGroup(label(r"fast: \ the voltage, with sodium's self-feeding loop built in", font_size=24,
                             color=GREY_A).next_to(two[0], DOWN, buff=0.2),
                       label(rf"slow ($\varepsilon = {d['eps']}$): \ recovery", font_size=24, color=GREY_A).next_to(
                           two[1], DOWN, buff=0.2))
        keep_in_frame(VGroup(two, names))
        end = label(r"Not a model of any real membrane. \ A model of what the four equations are doing.", font_size=28,
                    color=P.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Four equations reproduce the nerve signal. A natural next question, and it's the question a "
            "theorist always asks, is whether you need all four. <bookmark mark='a'/> Look at the gates "
            "again. m is so much faster than everything else that it's effectively always at the value the "
            "voltage dictates. So it isn't an independent variable; fold it into the voltage. "
            "<bookmark mark='b'/> And h and n are both slow, with similar time constants, and through a "
            "signal they move together: as potassium turns on, sodium becomes unavailable. One variable can "
            "stand for both. Call it recovery. <bookmark mark='c'/> In 1961 Richard FitzHugh wrote down the "
            "simplest pair of equations with those two features, and Jinichi Nagumo built it as an electrical "
            "circuit the following year. A fast variable v, with a cubic term that makes it feed on itself. "
            "And a slow variable w that follows v and drags it back. <bookmark mark='d'/> This is no longer "
            "a model of the squid. The numbers aren't millivolts. It's a model of the model: the least "
            "machinery that behaves like a nerve. And two variables have a great advantage over four. You "
            "can draw them on a sheet of paper."
        ) as vo:
            self.play(FadeIn(head), FadeIn(four, lag_ratio=0.2))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), four[1].animate.set_opacity(0.3))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), four[2].animate.set_opacity(0.3))
            vo.wait_until("c")
            self.play(Write(two[0]), Write(two[1]), FadeIn(names), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def phase_plane(self):
        d = load("fhn")
        v = np.asarray(d["v"])
        head = heading(r"The whole behaviour of a nerve, on one sheet")
        A = axes([-2.4, 2.4], [-1.2, 1.8], x_length=7.0, y_length=4.4, xticks=[-2, -1, 0, 1, 2], yticks=[-1, 0, 1],
                 xlabel=r"$v$ (fast: the voltage)", ylabel=r"$w$ (slow: recovery)", center=[-2.9, -0.45, 0])
        ax = A.ax
        ok = (d["null_v_0"] > -1.2) & (d["null_v_0"] < 1.8)
        nv = curve(ax, v[ok], d["null_v_0"][ok], VOLT, stroke_width=3)
        ok2 = (d["null_w"] > -1.2) & (d["null_w"] < 1.8)
        nw = curve(ax, v[ok2], d["null_w"][ok2], GATE["n"], stroke_width=3)
        rest = Dot(ax.c2p(*d["rest"]), radius=0.11, color=THRESH)
        below = curve(ax, d["below_v"], d["below_w"], LEAK, stroke_width=3)
        above = curve(ax, d["above_v"], d["above_w"], MODEL, stroke_width=4)
        starts = VGroup(Dot(ax.c2p(d["below_v"][0], d["below_w"][0]), radius=0.08, color=LEAK),
                        Dot(ax.c2p(d["above_v"][0], d["above_w"][0]), radius=0.08, color=MODEL))
        leg = legend([(VOLT, r"where $v$ stops changing"), (GATE["n"], r"where $w$ stops changing")], font_size=22)
        leg.move_to(ax.c2p(1.5, 1.45))
        nv_l, nw_l = leg[0], leg[1]
        state = VGroup(Dot(ax.c2p(0.6, 0.2), radius=0.1, color=THRESH),
                       Arrow(ax.c2p(0.6, 0.2), ax.c2p(1.25, 0.32), color=THRESH, stroke_width=3, buff=0.08),
                       label(r"one state of the cell, and where it is heading", font_size=22, color=THRESH))
        state[2].next_to(state[0], DOWN, buff=0.2)
        rest_l = label(r"rest", font_size=24, color=THRESH).next_to(rest, LEFT, buff=0.12)
        side = VGroup(
            wrapped_label(r"The two curves cross at the resting state.", 4.5, 26, THRESH),
            wrapped_label(r"A small kick: \ straight back.", 4.5, 26, LEAK),
            wrapped_label(r"A kick past the middle of the N: \ the state is swept right, up, left and down. \ "
                          r"One full signal.", 4.5, 26, MODEL),
            wrapped_label(r"Threshold, fixed size and dead time are the shape of this picture.", 4.5, 26, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.8, -0.3, 0])
        keep_in_frame(side)
        tag = psyche_tag()
        with self.voiceover(
            "Put the fast variable across and the slow one up. Every possible state of the cell is a point "
            "on this sheet, and the equations say which way each point moves. <bookmark mark='a'/> Two curves "
            "organise everything. On the N-shaped one, the fast variable has stopped changing. On the straight "
            "one, the slow variable has. Where they cross, nothing changes: that's the resting state. "
            "<bookmark mark='b'/> Give the cell a small kick to the right. The state slides straight back to "
            "rest. <bookmark mark='c'/> Now a slightly bigger kick, past the middle branch of the N. This time "
            "the fast variable runs away to the right-hand branch: that's the upstroke. Then the slow variable "
            "climbs: recovery building. At the top of the N the state falls off and shoots to the left: the "
            "downstroke. And it creeps down the left branch back to rest: the undershoot and the dead time. "
            "<bookmark mark='d'/> Everything from chapter six is here as geometry. The threshold is the "
            "middle branch. The signal has one size because every path that crosses the threshold joins the "
            "same loop. The dead time is the trip home down the left side, when a new kick would have to "
            "reach much further to cross over. One picture, and no arithmetic."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            self.play(FadeIn(state[0], scale=1.5), FadeIn(state[2]))
            self.play(GrowArrow(state[1]))
            vo.wait_until("a")
            self.play(FadeOut(state), run_time=0.6)
            self.play(Create(nv), Create(nw), FadeIn(nv_l), FadeIn(nw_l), run_time=3.0)
            self.play(FadeIn(rest, scale=1.5), FadeIn(rest_l), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(starts[0]), Create(below), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(starts[1]), FadeIn(side[2]))
            self.play(Create(above), run_time=14.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def two_ways(self):
        d = load("fhn")
        head = heading(r"Two ways to start firing")
        A = axes([0, 20], [0, 105], x_length=5.3, y_length=3.5, xticks=[0, 5, 10, 15, 20], yticks=[0, 25, 50, 75, 100],
                 xlabel=r"steady current ($\mu$A/cm$^2$)", ylabel=r"signals per second", center=[-3.6, -0.55, 0],
                 font_size=20)
        B = axes([0, 4], [0, 160], x_length=5.3, y_length=3.5, xticks=[0, 1, 2, 3, 4], yticks=[0, 50, 100, 150],
                 xlabel=r"steady current (nA)", ylabel=r"signals per second", center=[3.5, -0.55, 0], font_size=20)
        on = d["r_hh"] > 0
        hh = VGroup(curve(A.ax, d["i_hh"][~on], d["r_hh"][~on], MODEL, stroke_width=4),
                    curve(A.ax, d["i_hh"][on], d["r_hh"][on], MODEL, stroke_width=4))
        jump = DashedLine(A.ax.c2p(d["hh_onset"], 0), A.ax.c2p(d["hh_onset"], d["hh_first_rate"]), color=THRESH, stroke_width=2)
        lif = curve(B.ax, d["i_lif"], d["r_lif"], GATE["n"], stroke_width=4)
        t1 = VGroup(label(r"the squid axon's four equations", font_size=26, color=MODEL),
                    label(rf"nothing, then at once {d['hh_first_rate']:.0f} a second", font_size=22, color=GREY_A)).arrange(
                        DOWN, buff=0.06).next_to(A, UP, buff=0.3)
        t2 = VGroup(label(r"an integrator with a threshold", font_size=26, color=GATE["n"]),
                    label(r"as slowly as you like, from zero", font_size=22, color=GREY_A)).arrange(
                        DOWN, buff=0.06).next_to(B, UP, buff=0.3)
        end = wrapped_label(r"A cell of the second kind can report a weak input as a low rate. \ A cell of the first "
                            r"kind cannot: \ it prefers a rhythm.", 9.4, 26, P.ACCENT)
        end.to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.5)
        tag = psyche_tag()
        with self.voiceover(
            "The picture also explains something the single signal couldn't. Feed the cell a steady current "
            "and it fires over and over. How does that begin? <bookmark mark='a'/> For the squid's equations "
            f"the answer is abrupt. Below about {d['hh_onset']:.0f} units of current, nothing. Just above it, "
            f"the cell fires at once at {d['hh_first_rate']:.0f} signals a second. It can't fire slowly. In the "
            "picture, the steady current lifts the N-shaped curve until the crossing point slides onto the "
            "middle branch and becomes unstable, and the state starts circling at a rate set by the loop "
            "itself. <bookmark mark='b'/> Other cells, and the simpler model of the next chapter, begin "
            "differently: at the threshold current they fire as slowly as you like, and the rate grows "
            "smoothly from zero. <bookmark mark='c'/> Hodgkin noticed both kinds in real axons in 1948 and "
            "called them classes. The difference matters for what a cell can say. A cell that starts from "
            "zero can signal a weak input with a low rate: its rate is a measure. A cell that jumps is "
            "better thought of as a resonator, tuned to a rhythm. Both kinds are in your head."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(t1), Create(hh[0]), run_time=1.5)
            self.play(Create(jump), Create(hh[1]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(t2), Create(lif), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
