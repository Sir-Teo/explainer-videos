from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403


class Adding(VoiceoverScene):
    def construct(self):
        self.card()
        self.one_input()
        self.in_time()
        self.less_than_sum()
        self.divide()

    def card(self):
        card = chapter_card(3, r"Adding up", r"How does a cell combine thousands of inputs?", lit=(), part=PART,
                            scale=("neuron",), marr=("how",))
        with self.voiceover(
            "Chapter three. Adding up."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def one_input(self):
        d = load("integration")
        head = heading(r"One synapse opens for a few milliseconds")
        A = axes([0, 60], [-3, 17], x_length=7.0, y_length=4.4, xticks=[0, 20, 40, 60], yticks=[0, 5, 10, 15],
                 xlabel=r"time (ms)", ylabel=r"change in voltage (mV)", center=[-3.1, -0.5, 0])
        ax = A.ax
        t = d["t"]
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(60, 0), color=GREY_D, stroke_width=2)
        thr = DashedLine(ax.c2p(0, d["to_threshold"]), ax.c2p(60, d["to_threshold"]), color=THRESH, stroke_width=3)
        thr_l = label(r"threshold", font_size=24, color=THRESH).next_to(ax.c2p(60, d["to_threshold"]), UP, buff=0.08)
        thr_l.shift(LEFT * 0.8)
        e = trace(ax, t, d["one"] - d["e_l"], EXC)
        i = trace(ax, t, d["ipsp"] - d["e_l"], INH)
        e_l = label(rf"EPSP: \ ${d['peak_one']:+.1f}$ mV", font_size=26, color=EXC).next_to(
            ax.c2p(14, d["peak_one"]), UR, buff=0.1)
        i_l = label(rf"IPSP: \ ${d['trough_ipsp']:+.1f}$ mV", font_size=26, color=INH).next_to(
            ax.c2p(14, d["trough_ipsp"]), DR, buff=0.1)
        side = VGroup(
            wrapped_label(r"excitatory postsynaptic potential: \ a small bump up, \ gone within the membrane's "
                          r"time constant", 5.0, 27, EXC),
            wrapped_label(r"inhibitory postsynaptic potential: \ a small dip", 5.0, 27, INH),
            wrapped_label(r"One input gets a sixth of the way to threshold. \ A cell in your cortex has "
                          r"thousands of synapses, and no single one can fire it.", 5.0, 27, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.2, -0.3, 0])
        tag = psyche_tag()
        with self.voiceover(
            "Take the membrane from Part 5, sitting at rest, and open one excitatory synapse on it for a few "
            "milliseconds. <bookmark mark='a'/> The voltage rises by "
            f"{d['peak_one']:.1f} millivolts, and then decays, over the membrane's time constant. This bump "
            "is an excitatory postsynaptic potential. Everyone says EPSP. <bookmark mark='b'/> An inhibitory "
            f"synapse does the opposite. An IPSP: here, {abs(d['trough_ipsp']):.1f} millivolts down. "
            "<bookmark mark='c'/> And up here is threshold, fifteen millivolts above rest. One input gets a "
            "sixth of the way. A neuron in your cortex receives thousands of synapses, and no single one of "
            "them can make it fire. What the cell does with them is add."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(Create(e), run_time=2.5, rate_func=linear)
            self.play(FadeIn(e_l), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(i), run_time=2.0, rate_func=linear)
            self.play(FadeIn(i_l), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(thr), FadeIn(thr_l), FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()

    def in_time(self):
        d = load("integration")
        head = heading(r"Adding in time: \ what counts as together?")
        A = axes([0, 70], [0, 5.6], x_length=6.2, y_length=4.2, xticks=[0, 20, 40, 60], yticks=[0, 2, 4],
                 xlabel=r"time (ms)", ylabel=r"change in voltage (mV)", center=[-3.6, -0.3, 0])
        ax = A.ax
        t = d["t"]
        keep = t <= 70
        cases = [("together", THRESH, rf"together: \ {d['peak_together']:.2f}"),
                 ("close", EXC, rf"3 ms apart: \ {d['peak_close']:.2f}"),
                 ("apart", INH, rf"30 ms apart: \ {d['peak_apart']:.2f}")]
        curves = VGroup(*[trace(ax, t[keep], d[k][keep] - d["e_l"], c) for k, c, _ in cases])
        one = trace(ax, t[keep], d["one"][keep] - d["e_l"], GREY_B, 2.5)
        lg = legend([(GREY_B, rf"one input: \ {d['peak_one']:.2f} mV")] + [(c, s) for _, c, s in cases], font_size=23)
        lg.next_to(ax.c2p(70, 5.6), DL, buff=0.1)
        B = axes([0, 40], [2, 5.2], x_length=4.6, y_length=3.6, xticks=[0, 10, 20, 30, 40], yticks=[2.5, 3.5, 4.5],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"gap between two inputs (ms)", ylabel=r"peak (mV)",
                 center=[3.9, -0.1, 0])
        bx = B.ax
        pk = trace(bx, d["gaps"], d["peak_gap"], MODEL)
        floor = DashedLine(bx.c2p(0, d["peak_one"]), bx.c2p(40, d["peak_one"]), color=GREY_B, stroke_width=2)
        floor_l = label(r"one alone", font_size=22, color=GREY_B).next_to(bx.c2p(0, d["peak_one"]), DR, buff=0.06)
        tau = DashedLine(bx.c2p(d["tau"], 2), bx.c2p(d["tau"], 5.2), color=THRESH, stroke_width=2)
        tau_l = label(rf"$\tau = {d['tau']:.0f}$ ms", font_size=24, color=THRESH).next_to(
            bx.c2p(d["tau"], 5.2), RIGHT, buff=0.1).shift(DOWN * 0.2)
        end = wrapped_label(r"A neuron detects what happens together, \ and together means within about ten "
                            r"milliseconds.", 12.6, 28, P.ACCENT).to_edge(DOWN, buff=0.62)
        tag = psyche_tag()
        with self.voiceover(
            "Two inputs, then. <bookmark mark='a'/> If they arrive at the same moment, the peak is "
            f"{d['peak_together']:.2f} millivolts. Not quite double, and I'll come back to that. "
            f"<bookmark mark='b'/> Three milliseconds apart: {d['peak_close']:.2f}. The second rides on what's "
            "left of the first. <bookmark mark='c'/> Thirty milliseconds apart, and there's almost nothing "
            f"left to ride on: {d['peak_apart']:.2f}, hardly more than one input alone. <bookmark mark='d'/> "
            "Here's the peak against the gap between the two. It falls away at a pace set by the membrane's "
            f"time constant, {d['tau']:.0f} milliseconds in this cell. <bookmark mark='e'/> So a neuron is a "
            "detector of things that happen together, and together means within about ten milliseconds. "
            "That's summation in time. Summation in space is the same arithmetic, for inputs arriving at "
            "different synapses on the same cell."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(one), FadeIn(lg[0]))
            for k, mark_ in enumerate("abc"):
                vo.wait_until(mark_)
                self.play(Create(curves[k]), FadeIn(lg[k + 1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(B), Create(floor), FadeIn(floor_l))
            self.play(Create(pk), run_time=2.5)
            self.play(Create(tau), FadeIn(tau_l))
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def less_than_sum(self):
        d = load("integration")
        head = heading(r"Many at once: \ less than the sum")
        A = axes([0, 12.5], [0, 32], x_length=6.6, y_length=4.4, xticks=[2, 4, 6, 8, 10, 12], yticks=[0, 10, 20, 30],
                 xlabel=r"inputs arriving together", ylabel=r"peak change in voltage (mV)", center=[-3.3, -0.5, 0])
        ax = A.ax
        n = d["counts"]
        line = DashedLine(ax.c2p(0, 0), ax.c2p(12, d["peak_one"] * 12), color=LEAK, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(k, v), radius=0.075, color=EXC) for k, v in zip(n, d["peak_n"])])
        cur = trace(ax, np.r_[0, n], np.r_[0, d["peak_n"]], EXC, 3)
        thr = DashedLine(ax.c2p(0, 15), ax.c2p(12.5, 15), color=THRESH, stroke_width=2.5)
        thr_l = label(r"threshold", font_size=22, color=THRESH).next_to(ax.c2p(0, 15), UR, buff=0.06)
        need = d["needed"]
        drop = DashedLine(ax.c2p(need, 0), ax.c2p(need, float(d["peak_n"][need - 1])), color=EXC, stroke_width=2)
        lg = legend([(LEAK, r"if inputs simply added"), (EXC, r"computed")], font_size=24)
        lg.next_to(ax.c2p(0, 32), DR, buff=0.25)
        side = VGroup(
            label(r"current through a synapse", font_size=26, color=GREY_A),
            label(r"$I = g\,(E_E - V)$", font_size=40, color=EXC),
            wrapped_label(r"The pull is proportional to the distance from the battery at 0 mV. \ As $V$ climbs, "
                          r"each new input has less distance to pull through.", 5.0, 27, WHITE),
            wrapped_label(rf"to reach threshold: \ {need} inputs, where simple addition says 6", 5.0, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, -0.3, 0])
        tag = psyche_tag()
        with self.voiceover(
            "Now many at once. <bookmark mark='a'/> If inputs simply added, twelve of them would give twelve "
            f"times {d['peak_one']:.1f}: this straight line. <bookmark mark='b'/> They don't quite. The "
            "computed peaks bend below it. <bookmark mark='c'/> The reason is in the last chapter. An open "
            "channel pulls the voltage toward its battery, and the pull is proportional to how far away the "
            "voltage is. As the voltage climbs toward zero, each new input has less distance to pull "
            f"through. <bookmark mark='d'/> For this cell it takes {need} inputs arriving together to reach "
            "threshold, where simple addition says six. It's a small effect here. But it's the first sign "
            "that a neuron's arithmetic isn't just a sum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(thr), FadeIn(thr_l))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(lg[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cur), LaggedStart(*[FadeIn(x, scale=1.5) for x in dots], lag_ratio=0.2), FadeIn(lg[1]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(drop), Indicate(dots[need - 1], color=WHITE, scale_factor=2.0),
                      FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def divide(self):
        d = load("integration")
        head = heading(r"An inhibition that divides")
        A = axes([0, 0.3], [-8, 52], x_length=6.2, y_length=4.4, xticks=[0, 0.1, 0.2, 0.3], yticks=[0, 20, 40],
                 xfmt=lambda v: f"{v:.1f}", xlabel=r"excitation $g_E$ (mS/cm$^2$)",
                 ylabel=r"steady change in voltage (mV)", center=[-3.5, -0.5, 0])
        ax = A.ax
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0.3, 0), color=GREY_D, stroke_width=2)
        alone = trace(ax, d["ge"], d["alone"], EXC)
        hyper = trace(ax, d["ge"], d["hyper"], RULE)
        shunt = trace(ax, d["ge"], d["shunt"], INH)
        lg = legend([(EXC, r"excitation alone"), (RULE, r"inhibition with its battery below rest"),
                     (INH, r"inhibition with its battery at rest")], font_size=23)
        lg.next_to(ax.c2p(0.3, -8), UL, buff=0.15).shift(UP * 0.6)
        side = VGroup(
            label(r"with the inhibitory battery at rest:", font_size=26, color=GREY_A),
            MathTex(r"V - E_L \;=\; \frac{g_E\,(E_E - E_L)}{g_L + g_E + g_I}", font_size=38, color=WHITE),
            wrapped_label(r"Excitation is on top. \ The inhibition appears only underneath. \ It divides.", 5.2, 28,
                          INH),
            wrapped_label(rf"a weak input's effect: \ cut to {pct(d['ratio_small'])}. \ With no input: \ no "
                          r"change at all", 5.2, 27, WHITE),
            wrapped_label(r"shunting inhibition: \ a volume control", 5.2, 30, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.0, -0.3, 0])
        tag = psyche_tag(r"computed: Psyche, a passive membrane")
        with self.voiceover(
            "And inhibition can do something stranger than subtract. <bookmark mark='a'/> Here's the steady "
            "voltage of the membrane as excitation is turned up. <bookmark mark='b'/> Add an inhibitory "
            "synapse whose battery sits below rest, and the whole curve moves down. That's subtraction, more "
            "or less. <bookmark mark='c'/> Now add one whose battery sits exactly at rest. With no excitation, "
            "it does nothing at all. The voltage doesn't move, and you'd never see this synapse in a "
            "recording. But it has opened a hole in the membrane, and whatever current excitation brings in "
            "leaks out through the hole. <bookmark mark='d'/> Look at the formula. Excitation is on top. The "
            "inhibition appears only underneath. It divides. <bookmark mark='e'/> Here it cuts the effect of "
            "a weak input in half. This is shunting inhibition, and it gives a neuron a volume control: the "
            "same pattern of input, scaled down. Division of one signal by another will turn up again and "
            "again, in vision and in attention."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(zero))
            vo.wait_until("a")
            self.play(Create(alone), FadeIn(lg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(hyper), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(shunt), FadeIn(lg[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]), FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()
