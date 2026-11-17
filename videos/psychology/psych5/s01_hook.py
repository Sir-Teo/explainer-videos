from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.galvani()
        self.too_slow()
        self.four_equations()
        self.objectives()

    def galvani(self):
        head = heading(r"Bologna, the 1780s: \ a dead frog's leg kicks")
        hip = np.array([-3.4, 0.9, 0])
        thigh = Line(hip, hip + np.array([1.5, -1.3, 0]), color=VOLT, stroke_width=14)
        knee = thigh.get_end()
        shin = Line(knee, knee + np.array([-0.4, -1.7, 0]), color=VOLT, stroke_width=11)
        foot = Line(shin.get_end(), shin.get_end() + np.array([0.9, -0.15, 0]), color=VOLT, stroke_width=8)
        lower = VGroup(shin, foot)
        nerve = Line(hip + np.array([-0.2, 1.3, 0]), hip, color=DATA, stroke_width=5)
        nerve_l = label(r"nerve", font_size=24, color=DATA).next_to(nerve, LEFT, buff=0.15)
        muscle_l = label(r"muscle", font_size=24, color=GREY_A).next_to(thigh, DOWN, buff=0.3).shift(LEFT * 0.9)
        arc_a = ArcBetweenPoints(nerve.get_start() + UP * 0.02, nerve.get_start() + np.array([1.9, -0.9, 0]), angle=-PI / 2.4,
                                 color="#C98A4B", stroke_width=6)
        arc_b = ArcBetweenPoints(arc_a.get_end(), thigh.point_from_proportion(0.6), angle=-PI / 3, color="#9AA7B8",
                                 stroke_width=6)
        metals = VGroup(label(r"one metal", font_size=22, color="#C98A4B").next_to(arc_a, UP, buff=0.05).shift(RIGHT * 0.5),
                        label(r"another", font_size=22, color="#9AA7B8").next_to(arc_b, RIGHT, buff=0.1))
        side = VGroup(
            label(r"Galvani", font_size=36, color=DATA),
            wrapped_label(r"The animal carries its own electricity. \ Nerves conduct it to the muscles.", 5.6, 29,
                          WHITE),
            label(r"Volta", font_size=36, color="#9AA7B8"),
            wrapped_label(r"The two metals made the electricity. \ The leg only detected it.", 5.6, 29, WHITE),
            wrapped_label(r"Both were partly right. \ Neither could say what travels along the nerve.", 5.6, 27,
                          P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.5, -0.2, 0])
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "In the seventeen-eighties, in Bologna, the physician Luigi Galvani was dissecting frogs. "
            "<bookmark mark='a'/> He found that if he joined the nerve of a severed leg to its muscle with an "
            "arc made of two different metals, <bookmark mark='b'/> the leg kicked. The frog was dead, and the "
            "leg kicked every time. <bookmark mark='c'/> Galvani concluded that animals carry an electricity of "
            "their own, stored in the muscle and led about by the nerves. <bookmark mark='d'/> Alessandro "
            "Volta, a physicist, didn't believe it. He said the electricity came from the two metals, and the "
            "leg was only a sensitive detector. To prove it he stacked metals without any frog, and so "
            "invented the battery. <bookmark mark='e'/> Each of them was partly right. Metals do make a "
            "current. And nerves and muscles are electrical. But neither could say what it is that travels "
            "along a nerve when a leg is told to move."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(VGroup(thigh, lower, nerve, nerve_l, muscle_l)))
            vo.wait_until("a")
            self.play(Create(arc_a), Create(arc_b), FadeIn(metals), run_time=2.0)
            vo.wait_until("b")
            for _ in range(2):
                self.play(Rotate(lower, angle=1.1, about_point=knee), run_time=0.18)
                self.play(Rotate(lower, angle=-1.1, about_point=knee), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()

    def too_slow(self):
        h = archive.HELMHOLTZ_1850.data
        head = heading(r"1850: \ whatever it is, it is slow")
        lo, hi = h["speed_frog"]
        rows = [(r"light, and a current in a wire", 3e8, GREY_B, r"$300{,}000{,}000$ m/s"),
                (r"sound in air", 340.0, GREY_B, r"340 m/s"),
                (r"the signal in a frog's nerve", (lo + hi) / 2, DATA, rf"{lo:.0f} to {hi:.0f} m/s")]
        x0, unit = -1.2, 0.72  # bar length = unit * log10(speed)
        bars = VGroup()
        for i, (name, speed, color, text) in enumerate(rows):
            y = 1.2 - 1.15 * i
            w = unit * np.log10(speed)
            bar = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=color, fill_opacity=0.9)
            bar.move_to([x0 + w / 2, y, 0])
            nm = label(name, font_size=28, color=WHITE).next_to([x0, y, 0], LEFT, buff=0.25)
            val = label(text, font_size=28, color=color).next_to(bar, RIGHT, buff=0.15)
            bars.add(VGroup(nm, bar, val))
        keep_in_frame(bars)
        scale_note = label(r"each step along the bar is ten times faster", font_size=22, color=GREY_B)
        scale_note.next_to(bars, DOWN, buff=0.3)
        end = wrapped_label(r"A wire carries a signal ten million times faster. \ A nerve is not a wire.", 12.0, 30,
                            P.ACCENT).to_edge(DOWN, buff=0.7)
        src = historical_tag(archive.HELMHOLTZ_1850.cite)
        with self.voiceover(
            "Sixty years later Hermann von Helmholtz measured it, as you saw in Part 1. He stimulated a frog's "
            "nerve at two distances from the muscle and timed the difference. <bookmark mark='a'/> A current in "
            "a wire travels at close to the speed of light. <bookmark mark='b'/> Sound manages three hundred "
            f"and forty metres a second. <bookmark mark='c'/> The signal in the nerve moved at between {lo:.0f} "
            f"and {hi:.0f} metres a second. Slower than sound. You could outrun it on a motorcycle. "
            "<bookmark mark='d'/> That settles one thing. If a nerve were simply a wire carrying Galvani's "
            "electricity, the signal would arrive ten million times sooner. Something is happening along the "
            "way that takes time: something is being done at every point of the nerve, one point after the "
            "next. The question is what."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for mark, b_ in zip("abc", bars):
                vo.wait_until(mark)
                self.play(FadeIn(b_[0]), GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]), run_time=1.2)
            self.play(FadeIn(scale_note))
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.15))
        self.clear_scene()

    def four_equations(self):
        s, c = load("spike"), load("cable")
        head = heading(r"1952: \ four equations, and the signal comes out")
        A = axes([0, 8], [-90, 60], x_length=6.6, y_length=4.0, xticks=[0, 2, 4, 6, 8], yticks=[-80, -40, 0, 40],
                 xlabel=r"time (ms)", ylabel=r"membrane potential (mV)", center=[-3.2, -0.5, 0])
        ax = A.ax
        keep = s["t"] <= 8
        trace = curve(ax, s["t"][keep], s["v"][keep], MODEL, stroke_width=4)
        rest = DashedLine(ax.c2p(0, s["rest"]), ax.c2p(8, s["rest"]), color=GREY_B, stroke_width=2)
        side = VGroup(
            wrapped_label(r"Alan Hodgkin and Andrew Huxley measure the currents through the membrane of a squid's "
                          r"giant nerve fibre, and fit them with four equations.", 5.4, 27, WHITE),
            wrapped_label(r"Solved by hand, the equations produce this.", 5.4, 27, MODEL),
            VGroup(label(rf"computed speed: \ {c['published']} m/s", font_size=30, color=MODEL),
                   label(rf"measured: \ {c['observed']} m/s", font_size=30, color=DATA)).arrange(
                       DOWN, aligned_edge=LEFT, buff=0.1),
            wrapped_label(r"Psychology's best model of anything, and the pattern for every model in this "
                          r"series.", 5.4, 27, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.0, -0.2, 0])
        tag = psyche_tag()
        src = published_tag(archive.HODGKIN_HUXLEY_1952.cite)
        with self.voiceover(
            "The answer took another century, and it's the subject of this part. <bookmark mark='a'/> In "
            "1952 two physiologists in Cambridge, Alan Hodgkin and Andrew Huxley, published measurements of the "
            "electric currents that cross the membrane of a nerve fibre, a giant one, from a squid. They fitted "
            "those currents with four equations. Then they did the thing that makes this the best piece of "
            "science in our whole subject. <bookmark mark='b'/> They solved the equations, by hand, on a "
            "mechanical calculator, to see whether a nerve signal would come out. It did. This curve is that "
            "computation, done again by Psyche: the voltage across the membrane, rising by a tenth of a volt "
            "and falling back within two thousandths of a second. <bookmark mark='c'/> And the equations said "
            f"how fast the signal should travel along that fibre: {c['published']} metres a second. The "
            f"measured speed was {c['observed']}. <bookmark mark='d'/> Nothing in the equations had been told "
            "about speed. That is what a model is for. Measure, write equations, compute, and compare with "
            "something you didn't put in."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(A), Create(rest))
            vo.wait_until("b")
            self.play(Create(trace), FadeIn(side[1]), run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[2], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 5", font_size=34, color=GREY_B), label(r"The Neuron", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"what a neuron is, \ and why its membrane holds a voltage",
            r"the voltage clamp, \ and the four equations fitted to it",
            r"the action potential computed: \ threshold, all-or-none, refractory period",
            r"how it travels, \ and why its speed could be predicted",
            r"what can be thrown away: \ two variables, then one",
            r"what a spike train says, \ and what one cell can compute",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part five: the neuron. This opens the second act, in which we build the machine. "
            "<bookmark mark='a'/> We start with what a neuron is, and why its membrane sits at a voltage in "
            "the first place. <bookmark mark='b'/> Then the experiment that cracked it, the voltage clamp, and "
            "the four equations. <bookmark mark='c'/> We'll compute the nerve signal from those equations and "
            "find that its strangest properties, a threshold, a fixed size, a dead time afterwards, all fall "
            "out. <bookmark mark='d'/> We'll send it down a fibre and recover its speed. <bookmark mark='e'/> "
            "Then we'll throw most of the model away, twice, to see what's essential. <bookmark mark='f'/> And "
            "we'll ask what a train of these signals can say, and how much one cell can compute by itself."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
