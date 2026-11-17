from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Integrate(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.rate()
        self.kept_and_lost()

    def card(self):
        card = chapter_card(9, r"Integrate and fire", r"What is the least a neuron can be?",
                            lit={1907: r"Lapicque's model"}, part=PART, scale=("neuron", "circuit"), marr=("how",))
        with self.voiceover(
            "Chapter nine. Integrate and fire."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def model(self):
        d = load("lif")
        head = heading(r"A leaky capacitor and a rule")
        t, v = np.asarray(d["t"]), np.asarray(d["v"])
        keep = t <= 80
        A = axes([0, 80], [-70, -35], x_length=7.2, y_length=3.7, xticks=[0, 20, 40, 60, 80], yticks=[-65, -50],
                 xlabel=r"time (ms)", ylabel=r"membrane potential (mV)", center=[-2.8, -0.5, 0])
        ax = A.ax
        trace = curve(ax, t[keep], v[keep], VOLT, stroke_width=3.5)
        thr = DashedLine(ax.c2p(0, d["v_th"]), ax.c2p(80, d["v_th"]), color=THRESH, stroke_width=2)
        thr_l = label(r"threshold", font_size=22, color=THRESH).move_to(ax.c2p(6, d["v_th"] + 2.2), aligned_edge=LEFT)
        sp = load("spike")
        st, sv = np.asarray(sp["t"]), np.asarray(sp["v"])
        win = (st > 1.0) & (st < 7.0)
        same = VGroup()
        for i in range(3):
            pts = [np.array([3.0 + 1.25 * i + 0.16 * (a_ - 1.0), -0.6 + 0.014 * (b_ + 65), 0]) for a_, b_ in zip(st[win][::6], sv[win][::6])]
            same.add(VMobject(color=MODEL, stroke_width=3).set_points_smoothly(pts))
        same_l = wrapped_label(r"Every signal has the same shape. \ Only the moment it happens carries news.", 4.4, 26,
                               GREY_A).next_to(same, DOWN, buff=0.35)
        opening = VGroup(same, same_l)
        keep_in_frame(opening)
        ticks = VGroup(*[Line(ax.c2p(s_, d["v_th"]), ax.c2p(s_, -38), color=MODEL, stroke_width=4)
                         for s_ in d["spikes"] if s_ <= 80])
        rules = VGroup(
            MathTex(r"\tau\,\frac{dV}{dt} \;=\; -(V - E_L) + R\,I", font_size=38),
            wrapped_label(r"1. \ Below threshold: \ the charging curve of chapter three.", 4.6, 26, VOLT),
            wrapped_label(r"2. \ At threshold: \ write down ``a signal'', and reset the voltage.", 4.6, 26, MODEL),
            wrapped_label(rf"3. \ Wait {d['t_ref']:.0f} ms, and begin again.", 4.6, 26, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.75, -0.2, 0])
        keep_in_frame(rules)
        tag = psyche_tag()
        with self.voiceover(
            "Now throw away even more. The signal always has the same shape, so its shape carries no "
            "information. All that matters to the next cell is when it happened. So don't compute the signal "
            "at all. <bookmark mark='a'/> Keep the membrane of chapter three, the capacitor with a leak. Let "
            "the input current charge it. <bookmark mark='b'/> Add a rule: when the voltage reaches a "
            "threshold, record that a signal occurred, and put the voltage back where it started. "
            "<bookmark mark='c'/> Wait a moment, for the dead time, and carry on. That's the leaky "
            "integrate-and-fire neuron. The idea goes back to the French physiologist Louis Lapicque in 1907, "
            "before anyone knew what a nerve signal was. It has one equation and it's the charging curve. "
            "There are no gates, no sodium, no potassium. And for a great many purposes it's all the neuron "
            "you need."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(thr), FadeIn(thr_l))
            self.play(LaggedStart(*[Create(s_) for s_ in same], lag_ratio=0.4), FadeIn(same_l), run_time=4.0)
            vo.wait_until("a")
            self.play(FadeOut(opening), run_time=0.6)
            self.play(Write(rules[0]), FadeIn(rules[1]))
            self.play(Create(trace), run_time=6.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(ticks, lag_ratio=0.2), FadeIn(rules[2]))
            vo.wait_until("c")
            self.play(FadeIn(rules[3]))
        self.clear_scene()

    def rate(self):
        d = load("lif")
        head = heading(r"Its firing rate can be written down")
        A = axes([0, 8.5], [0, 270], x_length=6.6, y_length=3.9, xticks=[0, 2, 4, 6, 8], yticks=[0, 50, 100, 150, 200, 250],
                 xlabel=r"steady input current (nA)", ylabel=r"signals per second", center=[-3.1, -0.5, 0])
        ax = A.ax
        line = curve(ax, d["fine"], d["curve"], GATE["n"], stroke_width=4)
        pts = VGroup(*[Dot(ax.c2p(x, y), radius=0.09, color=MODEL) for x, y in zip(d["currents"], d["simulated"])])
        rheo = VGroup(DashedLine(ax.c2p(d["rheobase"], 0), ax.c2p(d["rheobase"], 150), color=THRESH, stroke_width=2),
                      wrapped_label(r"the least current that ever fires it", 2.3, 22, THRESH))
        rheo[1].move_to(ax.c2p(0.15, 205), aligned_edge=LEFT)
        eq = VGroup(
            wrapped_label(r"Time to charge from reset to threshold $\theta$:", 5.0, 26, WHITE),
            MathTex(r"T \;=\; \tau\,\ln\frac{R I}{R I - \theta}", font_size=40),
            wrapped_label(r"so the rate is", 5.0, 26, WHITE),
            MathTex(r"f \;=\; \frac{1}{t_{\text{ref}} + T}", font_size=40),
            wrapped_label(r"curve: \ the formula. \ dots: \ the simulation.", 5.0, 24, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.5, -0.2, 0])
        keep_in_frame(eq)
        tag = psyche_tag()
        with self.voiceover(
            "The reward for simplicity is that you can do mathematics on it. With the squid's equations, the "
            "firing rate under a steady current had to be found by simulation. Here it can be written down. "
            "<bookmark mark='a'/> The charging curve is an exponential, so you can solve for the moment it "
            "crosses the threshold. That time is the time constant multiplied by a logarithm. Add the dead "
            "time, turn it upside down, and that's the rate. <bookmark mark='b'/> Below a certain current the "
            "voltage levels off under the threshold and the cell never fires. Just above it, the cell fires "
            "very slowly, because the voltage only just creeps over. Then the rate climbs, and eventually "
            "bends over toward the ceiling set by the dead time. <bookmark mark='c'/> The dots are the "
            "simulation and the curve is the formula. They agree to a fraction of a per cent, which is how "
            "the code is tested. This curve, the rate as a function of the input, is the single most used "
            "summary of a neuron. In the artificial networks of the companion series, AI, Built, each unit "
            "is just such a curve with the spikes left out."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            self.play(FadeIn(eq[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e_) for e_ in eq[1:4]], lag_ratio=0.6), run_time=6.0)
            vo.wait_until("b")
            self.play(Create(line), FadeIn(rheo), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(pts, lag_ratio=0.15), FadeIn(eq[4]), run_time=2.0)
        self.clear_scene()

    def kept_and_lost(self):
        d = load("lif")
        head = heading(r"What was kept, and what was lost")
        kept = VGroup(
            label(r"kept", font_size=36, color=MODEL),
            label(r"adding up inputs over a few milliseconds", font_size=28, color=WHITE),
            label(r"a threshold", font_size=28, color=WHITE),
            label(r"a rate that grows with the input", font_size=28, color=WHITE),
            label(r"a formula", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        lost = VGroup(
            label(r"lost", font_size=36, color=BAD),
            label(r"the shape of the signal, and its ions", font_size=28, color=WHITE),
            label(r"why there is a threshold at all", font_size=28, color=WHITE),
            label(r"the squid's abrupt start, and its rhythms", font_size=28, color=WHITE),
            label(r"any way to be wrong about a membrane", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cols = VGroup(kept, lost).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 0.9, 0])
        t, v = np.asarray(d["noisy_t"]), np.asarray(d["noisy_v"])
        A = axes([0, 400], [-70, -44], x_length=11.0, y_length=1.6, xticks=[0, 100, 200, 300, 400], yticks=[],
                 xlabel=r"time (ms): \ a steady input just too weak to fire the cell, with noise", center=[0, -2.25, 0],
                 font_size=19)
        noisy = curve(A.ax, t, v, VOLT, stroke_width=2)
        thr = DashedLine(A.ax.c2p(0, d["v_th"]), A.ax.c2p(400, d["v_th"]), color=THRESH, stroke_width=2)
        ticks = VGroup(*[Line(A.ax.c2p(s_, d["v_th"]), A.ax.c2p(s_, -45), color=MODEL, stroke_width=3)
                         for s_ in d["noisy_spikes"]])
        tag = psyche_tag()
        with self.voiceover(
            "It's worth being exact about the trade. <bookmark mark='a'/> Kept: the membrane's habit of "
            "adding up what arrives within a few milliseconds. A threshold. A firing rate that grows with "
            "the input. And a formula. <bookmark mark='b'/> Lost: the signal itself, and any mention of ions. "
            "The reason there's a threshold; here it's simply decreed. The squid's way of starting abruptly. "
            "And one more thing, the most important. This model can't be wrong about a membrane, because it "
            "says nothing about one. Hodgkin and Huxley's model can be refuted by a measurement on an axon. "
            "This one can only be more or less useful. <bookmark mark='c'/> Used honestly, it's very useful. "
            "Give it an input just too weak to fire it, and add noise, and it fires now and then, at "
            "irregular moments, like a real cortical cell. Put ten thousand of them together and you can "
            "study a network, which is Part 6. And notice its outline: something accumulates toward a "
            "threshold, and an event happens when it gets there. You'll meet that shape again in Part 25, "
            "as a model of how a person makes up their mind."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in kept], lag_ratio=0.5), run_time=5.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in lost], lag_ratio=0.8), run_time=14.0)
            vo.wait_until("c")
            self.play(FadeIn(A), Create(thr))
            self.play(Create(noisy), FadeIn(ticks, lag_ratio=0.3), run_time=6.0, rate_func=linear)
        self.clear_scene()
