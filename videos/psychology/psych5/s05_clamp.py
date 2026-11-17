from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Clamp(VoiceoverScene):
    def construct(self):
        self.card()
        self.squid()
        self.the_clamp()
        self.measured()

    def card(self):
        card = chapter_card(4, r"The squid and the voltage clamp", r"How do you measure a thing that changes "
                            r"itself?", lit={1939: r"a record from inside a nerve fibre"}, part=PART,
                            scale=("molecule", "neuron"), marr=("tissue",))
        with self.voiceover(
            "Chapter four. The squid and the voltage clamp."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def squid(self):
        d, s = archive.HODGKIN_HUXLEY_1952.data, load("spike")
        cc = archive.COLE_CURTIS_1939.data
        head = heading(r"A nerve fibre wide enough to put a wire inside")
        big = Circle(radius=1.5, color=VOLT, stroke_width=4, fill_color="#111722", fill_opacity=1).move_to([-4.6, 0.3, 0])
        small = Circle(radius=0.05, color=DATA, stroke_width=0, fill_color=DATA, fill_opacity=1).move_to([-2.4, -0.9, 0])
        big_l = label(rf"squid giant axon: \ {2 * d['radius_um'] / 1000:.1f} mm across", font_size=24, color=VOLT)
        big_l.next_to(big, DOWN, buff=0.2)
        small_l = label(r"a typical axon of ours, to scale", font_size=22, color=DATA).next_to(small, RIGHT, buff=0.15)
        wire = Line(big.get_center() + UP * 2.4, big.get_center(), color=THRESH, stroke_width=4)
        A = axes([0, 8], [-90, 60], x_length=5.2, y_length=3.6, xticks=[0, 2, 4, 6, 8], yticks=[-80, -40, 0, 40],
                 xlabel=r"time (ms)", ylabel=r"inside, relative to outside (mV)", center=[3.4, -0.2, 0], font_size=20)
        ax = A.ax
        keep = s["t"] <= 8
        trace = curve(ax, s["t"][keep], s["v"][keep], MODEL, stroke_width=4)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(8, 0), color=GREY_B, stroke_width=2)
        over = VGroup(Arrow(ax.c2p(4.6, 25), ax.c2p(3.0, 32), color=THRESH, stroke_width=3, buff=0.05),
                      label(r"past zero: \ the overshoot", font_size=24, color=THRESH).next_to(ax.c2p(4.6, 25), RIGHT,
                                                                                         buff=0.05))
        found = VGroup(
            label(rf"1939, Hodgkin and Huxley: \ rest ${d['rest_1939_mv']:.0f}$ mV, \ peak ${d['peak_1939_mv']:+.0f}$ mV",
                  font_size=26, color=DATA),
            label(r"1939, Cole and Curtis: \ during the signal the membrane's conductance rises", font_size=26,
                  color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.75)
        src = published_tag(rf"{archive.HODGKIN_HUXLEY_1952.cite}; \ {archive.COLE_CURTIS_1939.cite}")
        tag = note(r"the curve is the model's, not their record").to_corner(DR, buff=0.2)
        with self.voiceover(
            "To find out what turns the dial, somebody had to get inside a nerve fibre, and ordinary nerve "
            "fibres are a few thousandths of a millimetre across. <bookmark mark='a'/> The squid solved the "
            f"problem. To escape predators it has an axon that is {2 * d['radius_um'] / 1000:.1f} millimetres "
            f"thick, found by the zoologist John Zachary Young in {cc['giant_axon']}. You can see it with the "
            "naked eye. <bookmark mark='b'/> And you can slide a fine wire down the inside of it. In 1939, "
            "in Plymouth, Hodgkin and Huxley did that, and recorded the voltage of a nerve signal from the "
            "inside for the first time. <bookmark mark='c'/> It held a surprise. The theory of the day said "
            "that during the signal the membrane simply breaks down, so the voltage should collapse to zero. "
            f"It didn't stop at zero. From about minus {abs(d['rest_1939_mv']):.0f} millivolts it shot up to "
            f"about plus {d['peak_1939_mv']:.0f}. <bookmark mark='d'/> The inside went positive. A membrane "
            "that had merely sprung a leak couldn't do that. Something was driving the voltage toward a "
            "positive battery, and you know from chapter two which ion has one. The same year, in America, "
            "Kenneth Cole and Howard Curtis showed that the membrane's conductance rises sharply during the "
            "signal, while its capacitance stays put. Doors were opening. Then the war came, and the work "
            "stopped for six years."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(small, scale=3.0), FadeIn(small_l))
            vo.wait_until("a")
            self.play(FadeIn(big), FadeIn(big_l))
            vo.wait_until("b")
            self.play(Create(wire))
            vo.wait_until("c")
            self.play(FadeIn(A), Create(zero), FadeIn(tag))
            self.play(Create(trace), run_time=4.0, rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(over), FadeIn(found[0]))
            self.play(FadeIn(found[1]))
        self.clear_scene()

    def the_clamp(self):
        head = heading(r"The trouble, and the trick")
        loop = VGroup(
            label(r"voltage", font_size=34, color=VOLT).move_to([-5.7, 0.35, 0]),
            label(r"channels", font_size=34, color=NA).move_to([-2.6, 0.35, 0]),
        )
        arcs = VGroup(CurvedArrow(loop[0].get_top() + UP * 0.1, loop[1].get_top() + UP * 0.1, angle=-PI / 2,
                                  color=GREY_B, stroke_width=4),
                      CurvedArrow(loop[1].get_bottom() + DOWN * 0.1, loop[0].get_bottom() + DOWN * 0.1, angle=-PI / 2,
                                  color=GREY_B, stroke_width=4))
        arc_l = VGroup(label(r"opens", font_size=24, color=GREY_A).next_to(arcs[0], UP, buff=0.1),
                       label(r"change", font_size=24, color=GREY_A).next_to(arcs[1], DOWN, buff=0.1))
        keep_in_frame(VGroup(loop, arcs, arc_l))
        # the clamp: axon, two wires, an amplifier that holds the voltage at a commanded value
        axon = RoundedRectangle(width=5.6, height=0.9, corner_radius=0.45, color=VOLT, stroke_width=3,
                                fill_color="#111722", fill_opacity=1).move_to([3.0, -1.6, 0])
        w_v = Line([1.6, -1.6, 0], [1.6, 0.2, 0], color=VOLT, stroke_width=3)
        w_i = Line([4.4, -1.6, 0], [4.4, 0.2, 0], color=THRESH, stroke_width=3)
        amp = Polygon([2.2, 1.6, 0], [2.2, 0.2, 0], [3.8, 0.9, 0], color=GREY_A, stroke_width=3,
                      fill_color="#111722", fill_opacity=1)
        to_amp = VGroup(Line([1.6, 0.2, 0], [1.6, 0.6, 0], color=VOLT, stroke_width=3),
                        Line([1.6, 0.6, 0], [2.2, 0.6, 0], color=VOLT, stroke_width=3))
        from_amp = VGroup(Line([3.8, 0.9, 0], [4.4, 0.9, 0], color=THRESH, stroke_width=3),
                          Line([4.4, 0.9, 0], [4.4, 0.2, 0], color=THRESH, stroke_width=3))
        cmd = VGroup(Line([1.0, 1.25, 0], [2.2, 1.25, 0], color=MODEL, stroke_width=3),
                     label(r"the voltage you want", font_size=22, color=MODEL).next_to([1.0, 1.25, 0], LEFT, buff=0.1))
        labs = VGroup(label(r"measures the voltage", font_size=22, color=VOLT).next_to(w_v, LEFT, buff=0.1),
                      label(r"injects current", font_size=22, color=THRESH).next_to(w_i, RIGHT, buff=0.1),
                      label(r"amplifier", font_size=22, color=GREY_A).next_to(amp, UP, buff=0.1))
        clamp = VGroup(axon, w_v, w_i, amp, to_amp, from_amp, cmd, labs)
        keep_in_frame(clamp)
        end = wrapped_label(r"Hold the voltage fixed. \ The current the amplifier has to supply is, moment by "
                            r"moment, the current the membrane is passing.", 12.2, 29, P.ACCENT).to_edge(DOWN, buff=0.5)
        tag = note(r"schematic").to_corner(UR, buff=0.2)
        with self.voiceover(
            "When they came back to it, they faced a problem that anyone who studies a living system "
            "eventually meets. <bookmark mark='a'/> The voltage opens channels. And open channels change the "
            "voltage. The two chase each other round, and the whole event is over in a millisecond. If you "
            "watch the voltage, you can't tell what the channels are doing, because you're looking at the "
            "result of a loop. <bookmark mark='b'/> The trick, developed by Cole and by George Marmont and then "
            "by Hodgkin, Huxley and Bernard Katz, is to break the loop by force. One wire inside the axon "
            "measures the voltage. A second wire injects current. Between them sits an amplifier, which is "
            "told what voltage you want and injects whatever current it takes to keep the membrane there. "
            "That's a voltage clamp. <bookmark mark='c'/> Now step the voltage to a new value and hold it. The "
            "channels respond, but they can no longer move the voltage, because the amplifier cancels "
            "whatever they do. And the current the amplifier supplies in order to do that is exactly the "
            "current flowing through the channels. You've turned a runaway into a measurement. It's the "
            "same idea as the blind in Part 2: when two things influence each other, pin one of them down."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(loop), Create(arcs), FadeIn(arc_l), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(FadeIn(axon), Create(w_v), FadeIn(labs[0]), FadeIn(amp), FadeIn(labs[2]), Create(to_amp),
                                  Create(from_amp), Create(w_i), FadeIn(labs[1]), FadeIn(cmd), lag_ratio=0.5),
                      run_time=12.0)
            vo.wait_until("c")
            self.play(FadeIn(end, shift=UP * 0.15))
        self.clear_scene()

    def measured(self):
        d = load("clamp")
        head = heading(r"What the clamp showed: \ two conductances with different habits")
        t = np.asarray(d["t"])
        steps = d["steps"]
        shade = {-40: 0.35, -20: 0.5, 0: 1.0, 20: 0.7, 40: 0.55}
        top_na = max(float(np.max(d[f"g_na_{int(v)}"])) for v in steps) * 1.1
        top_k = max(float(np.max(d[f"g_k_{int(v)}"])) for v in steps) * 1.1
        A1 = axes([0, 8], [0, top_na], x_length=5.4, y_length=3.2, xticks=[0, 2, 4, 6, 8], yticks=[0, 10, 20, 30],
                  xlabel=r"time after the step (ms)", ylabel=r"sodium conductance", center=[-3.5, -0.5, 0], font_size=20)
        A2 = axes([0, 8], [0, top_k], x_length=5.4, y_length=3.2, xticks=[0, 2, 4, 6, 8], yticks=[0, 10, 20, 30],
                  xlabel=r"time after the step (ms)", ylabel=r"potassium conductance", center=[3.6, -0.5, 0],
                  font_size=20)
        na = VGroup(*[curve(A1.ax, t, d[f"g_na_{int(v)}"], NA, stroke_width=4 if v == 0 else 2.5).set_stroke(
            opacity=shade[int(v)]) for v in steps])
        kk = VGroup(*[curve(A2.ax, t, d[f"g_k_{int(v)}"], K, stroke_width=4 if v == 0 else 2.5).set_stroke(
            opacity=shade[int(v)]) for v in steps])
        i0 = steps.index(0.0)
        cap1 = VGroup(label(r"fast on, then off by itself", font_size=28, color=NA),
                      label(rf"peak after {d['t_peak_na_0']:.1f} ms", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.06)
        cap2 = VGroup(label(r"slow on, after a delay, and it stays", font_size=28, color=K),
                      label(rf"half-way after {d['half_g_k_0']:.1f} ms", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.06)
        cap1.next_to(A1, UP, buff=0.3)
        cap2.next_to(A2, UP, buff=0.3)
        end = label(r"Larger steps: \ both come on faster, and larger. \ The doors are opened by voltage.", font_size=26,
                    color=P.ACCENT).to_edge(DOWN, buff=0.4).to_edge(LEFT, buff=0.5)
        cmd = label(r"the command: \ hold at rest, then step to 0 mV and hold", font_size=26, color=MODEL)
        cmd.next_to(head, DOWN, buff=0.25)
        tag = psyche_tag()
        with self.voiceover(
            "Here is what the clamp shows, in the form Hodgkin and Huxley reduced it to. They separated the "
            "current into the part carried by sodium and the part carried by potassium, by repeating each "
            "experiment with the sodium in the bath replaced, and subtracting. Then they divided each current "
            "by its driving force, to get a conductance: how open the doors are. <bookmark mark='a'/> Step "
            "the voltage from rest up to zero, and hold. The sodium conductance leaps up within half a "
            "millisecond. And then, with the voltage still held, it falls again, by itself. The sodium doors "
            "open, and then something shuts them. <bookmark mark='b'/> The potassium conductance behaves "
            "differently. It does nothing at first. Then it rises, along an S-shaped curve, taking a couple "
            "of milliseconds, and it stays up for as long as the voltage is held. <bookmark mark='c'/> Repeat "
            "with larger and smaller steps. The bigger the step, the faster and further both of them go. So "
            "these are doors opened by voltage. And there are three processes to describe: sodium turning on, "
            "sodium turning off, and potassium turning on, late. Everything else in this part follows from "
            "those three curves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A1), FadeIn(A2))
            vo.wait_until("a")
            self.play(FadeIn(cmd))
            self.play(Create(na[i0]), FadeIn(cap1), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(kk[i0]), FadeIn(cap2), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(c_) for i, c_ in enumerate(na) if i != i0], lag_ratio=0.3),
                      LaggedStart(*[Create(c_) for i, c_ in enumerate(kk) if i != i0], lag_ratio=0.3), run_time=4.0)
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
