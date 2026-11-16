from __future__ import annotations

import numpy as np

from videos.music.music51.common import *  # noqa: F403


class Circuit(SoundScene):
    def construct(self):
        chapter(self, 5, r"Running the circuit", r"How do you put a transistor ladder inside a computer?")
        self.equations()
        self.three_ways()
        self.convergence()
        self.quiz()
        self.harmonics()
        self.edge()
        self.sing()

    # ------------------------------------------------------------------
    def equations(self):
        lines = VGroup(
            MathTex(r"\frac{dV_1}{dt} = \omega_c\,\big(\tanh(x - kV_4) - \tanh V_1\big)", font_size=34),
            MathTex(r"\frac{dV_j}{dt} = \omega_c\,\big(\tanh V_{j-1} - \tanh V_j\big), \quad j = 2, 3, 4", font_size=34),
        ).arrange(DOWN, buff=0.5).move_to(UP * 0.6)
        notes = VGroup(label(r"a transistor pair passes current as the tanh of the voltage across it: \ linear when quiet, \ saturating when loud", font_size=18, color=WHITE),
                       label(r"so the ladder is four capacitors, \ each charged through a tanh: \ Antti Huovilainen's model \ (2004)", font_size=18, color=GREY_A),
                       label(r"turn the input up and the filter itself distorts, \ softly, \ in its own way", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.5)
        head = label(r"the circuit's equations", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The linear algebra is only the quiet half of the story. <bookmark mark='a'/> A transistor pair passes current as "
            "the hyperbolic tangent of the voltage across it: linear when quiet, saturating when loud. <bookmark mark='b'/> So "
            "the ladder is four capacitors, each charged through a tanh. These are the equations of Antti Huovilainen's 2004 "
            "model, derived from the circuit. <bookmark mark='c'/> Turn the input up, and the filter itself distorts, softly, "
            "in its own way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(lines, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three_ways(self):
        items = [
            (r"the reference: \ fourth-order Runge--Kutta, \ sixteen small steps per sample: \ slow, \ and very nearly exact", WHITE),
            (r"forward steps: \ each capacitor moves by its current slope, \ the feedback taken from the last sample's output", WHITE),
            (r"Huovilainen's correction: \ average the last two outputs in the loop, \ cancelling half a sample of delay", WHITE),
            (r"the trapezoidal rule with Newton's method: \ solve for the new voltages and the feedback together, \ at every sample", WHITE),
            (r"Vadim Zavalishin called the last `zero-delay feedback': \ the loop has no sample of delay in it", TUNE),
        ]
        rows_scene(self, r"three ways to step it, \ and a reference", items,
                   "A computer must step these equations from sample to sample, and there are better and worse ways. "
                   "<bookmark mark='b'/> First a reference: the fourth-order Runge-Kutta method with sixteen small steps per "
                   "sample, slow and very nearly exact. <bookmark mark='c'/> Then forward steps: each capacitor moves by its current "
                   "slope, with the feedback taken from the last sample's output. <bookmark mark='d'/> Huovilainen's correction "
                   "averages the last two outputs in the loop, cancelling half a sample of delay. <bookmark mark='e'/> And the "
                   "trapezoidal rule with Newton's method solves for the new voltages and the feedback together, at every sample. "
                   "<bookmark mark='f'/> Vadim Zavalishin called this zero-delay feedback: the loop has no sample of delay in it.",
                   marks="bcdef")

    # ------------------------------------------------------------------
    def convergence(self):
        d = load("ladder")
        cv = d["conv"]
        order = [("forward", r"forward steps", EAR), ("corrected", r"half-sample correction", BLUE), ("trapezoid", r"trapezoid and Newton", TUNE)]
        lp = line_plot([cv[k] for k, _, _ in order], width=6.4, height=3.8, ylo=-80, yhi=0, colors=[c for _, _, c in order],
                       yticks=(0, -20, -40, -60, -80), ylabel=r"error against the reference, \ dB", size=16).move_to(LEFT * 2.0 + DOWN * 0.2)
        xt = VGroup(*[label(f"{r}x", font_size=15, color=GREY_A).next_to(lp.to(i, -80), DOWN, buff=0.12) for i, r in enumerate(d["rates"])])
        xl = label(r"times 48 kHz", font_size=15, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        key = VGroup(*[label(t, font_size=17, color=c) for _, t, c in order]).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(lp, RIGHT, buff=0.6)
        sl = VGroup(label(r"6 dB per doubling: \ first order", font_size=16, color=GREY_A), label(r"12 dB per doubling: \ second order", font_size=16, color=TUNE)).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(key, DOWN, buff=0.5, aligned_edge=LEFT)
        cap = label(r"a 220 Hz sawtooth into the ladder at 1.5 kHz, \ $k = 3$, \ driven to full level", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.3)
        head = label(r"the ladder against its circuit equations", font_size=26, color=GREY_A).to_edge(UP, buff=0.3)
        f, c, t = cv["forward"], cv["corrected"], cv["trapezoid"]
        with self.voiceover(
            f"Here they are against the reference, driven hard with plenty of resonance, at one, two, four and eight times forty-eight kilohertz. <bookmark mark='a'/> Forward steps are only {say(-f[0], 1)} decibels from the oversampled numerical reference at the normal rate, and gain six decibels for each doubling: a first-order method. <bookmark mark='b'/> The half-sample correction starts {say(c[0] - f[0], 1)} decibels lower and keeps the same slope. <bookmark mark='c'/> The trapezoid with Newton starts at {say(-t[0], 1)} and gains twelve decibels a doubling, second order: at the normal rate it is already better than forward steps at eight times the rate. Each of its samples costs about {say(d['cost'], 1)} times as much on this computer: far less than eight times the samples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lp[0]), FadeIn(lp[2:]), FadeIn(xt), FadeIn(xl), FadeIn(cap), FadeIn(ghost(lp.lines, 0.25)))
            for mark, i in zip("abc", range(3)):
                vo.wait_until(mark)
                self.play(Create(lp.lines[i]), FadeIn(key[i]), run_time=1.0)
            self.play(FadeIn(sl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("drive")
        c = clip("drive.two")
        card = listen_card(r"The Tune's first phrase, \ a sawtooth driven hard into the ladder, \ twice, \ at the same loudness. \ One run "
                           r"uses the circuit's equations with every tanh removed; \ the other, \ the full circuit. \ Which is the circuit?", width=10.4)
        with self.voiceover(
            "Your turn. The Tune's first phrase on a sawtooth driven hard into the ladder, twice, at the same loudness. One run "
            "uses the circuit's equations with every tanh removed, a filter linear in its audio input for a fixed cutoff trajectory; the other, the full circuit. "
            "Which is the circuit?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"driven hard, \ twice", kind="synthesized", detail=r"sawtooth and ladder", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], c.duration, buff=0.08)
        with self.voiceover(
            "The second. A linear filter does not care how hard it is driven: it simply rings, a sharp, whistling resonance on "
            "every note. The circuit cannot do that. Its transistors saturate, so the resonance is tamed "
            "and the tone thickens and rounds off: the Moog's warmth is partly this."
        ):
            self.play(boxes[1][0].animate.set_stroke(TUNE, width=4))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harmonics(self):
        d = load("drive")
        hl = harm_bars(d["h_lin"], width=0.3, gap=0.5, floor=-50.0, height=2.6, color=GREY_A, x0=-5.2, y0=-1.6)
        hn = harm_bars(d["h_nl"], width=0.3, gap=0.5, floor=-50.0, height=2.6, color=TUNE, x0=1.2, y0=-1.6)
        tl = label(r"equations without tanh", font_size=18, color=GREY_A).next_to(hl, UP, buff=0.3)
        tn = label(r"the circuit", font_size=18, color=TUNE).next_to(hn, UP, buff=0.3)
        res = SurroundingRectangle(hl[3], color=EAR, buff=0.08)
        rl = label(rf"the 4th harmonic, \ near the cutoff: \ ${d['h_lin'][3]:+.1f}$ dB", font_size=16, color=EAR).next_to(hl, DOWN, buff=0.4)
        nl = label(rf"in the circuit: \ ${d['h_nl'][3]:.1f}$ dB", font_size=16, color=TUNE).next_to(hn, DOWN, buff=0.4)
        cap = label(r"a 220 Hz sawtooth, \ three times full level, \ into the ladder at 900 Hz with $k = 3.2$: \ harmonics in dB re the first", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"what saturation did", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The harmonics show it. <bookmark mark='a'/> In the linear filter, the fourth harmonic, at eight hundred and eighty "
            f"hertz, right on the resonant peak, comes out {say(d['h_lin'][3], 1)} decibels above the fundamental: the "
            "whistle. <bookmark mark='b'/> In the circuit the saturating rungs refuse to build that peak, and the fourth "
            f"harmonic sits {say(-d['h_nl'][3], 1)} decibels below it. The resonance is felt, not shouted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cap), FadeIn(ghost(VGroup(hl, hn), 0.3)))
            vo.wait_until("a")
            self.play(FadeIn(hl), FadeIn(tl), Create(res), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(hn), FadeIn(tn), FadeIn(nl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def edge(self):
        d = load("ladder")
        rows = VGroup(VGroup(label(r"cutoff", font_size=20, color=GREY_A), label(r"oscillates at", font_size=20, color=GREY_A), label(r"off by", font_size=20, color=GREY_A)))
        for fc in ("220", "440", "880"):
            f = d["osc"][fc]
            rows.add(VGroup(label(rf"{fc} Hz", font_size=22, color=WHITE), label(rf"{f:.1f} Hz", font_size=22, color=TUNE),
                            label(rf"{1200 * np.log2(f / float(fc)):+.0f} cents", font_size=22, color=WHITE)))
        rows.arrange(DOWN, buff=0.4)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-3.4 + 3.4 * i)
        rows.move_to(DOWN * 0.1)
        cap = label(r"$k = 4.3$, \ no input but one tiny click: \ the tanh holds the oscillation at a steady level", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.6)
        head = label(r"past the edge", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now push k past four. With no input but one tiny click, the filter starts to oscillate and does not stop: the "
            "tanh in each rung holds the swing at a steady level, as a real circuit's saturation does. <bookmark mark='a'/> It "
            "oscillates close to the cutoff, within about twenty cents at each of three settings: a filter that has become a "
            "nearly pure "
            "sine oscillator."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(cap), FadeIn(ghost(rows[1:], 0.3)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sing(self):
        d = load("sing")
        c = clip("sing.one")
        notes = [(m, a, dd) for m, a, dd in d["notes"]]
        r = mroll(notes, width=10.0, height=2.4, lo=58, hi=71, color=TUNE).move_to(DOWN * 0.2)
        cap = label(r"no oscillator: \ the ladder alone, \ $k = 4.3$, \ its cutoff stepped from note to note", font_size=18, color=GREY_A).to_edge(DOWN, buff=1.0)
        head = label(r"the filter sings", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "So play a tune on it. No oscillator at all: the ladder alone, oscillating, its cutoff stepped through the Tune's "
            "first phrase."
        ):
            self.play(FadeIn(head), FadeIn(r), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"the filter alone", kind="synthesized", detail=r"a self-oscillating ladder", corner=DL, tag_corner=DR)
            flash(snd, r.notes, [n[1] for n in notes], hot=WHITE, base=TUNE)
            cursor(snd, r, 0.0, 1.0)
        with self.voiceover(
            "A pure, slightly hollow whistle, gliding a little as each change of cutoff settles: the sound players called the "
            "filter singing. Chapter nine strikes the same filter instead of letting it run, and gets a drum."
        ):
            self.play(Indicate(r, color=TUNE, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()
