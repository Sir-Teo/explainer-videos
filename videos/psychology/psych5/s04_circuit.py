from __future__ import annotations

import numpy as np

from videos.psychology.psych5.common import *  # noqa: F403


class Circuit(VoiceoverScene):
    def construct(self):
        self.card()
        self.parts()
        self.charging()

    def card(self):
        card = chapter_card(3, r"The membrane as a circuit", r"How fast can a cell's voltage change?", lit=(),
                            part=PART, scale=("neuron",), marr=("tissue",))
        with self.voiceover(
            "Chapter three. The membrane as a circuit."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _circuit(self, cx=0.0, cy=0.0):
        """Capacitor, leak resistor and battery between an outside rail (top) and an inside rail (bottom)."""
        top, bot = cy + 1.5, cy - 1.5
        rails = VGroup(Line([cx - 2.6, top, 0], [cx + 2.6, top, 0], color=VOLT, stroke_width=3),
                       Line([cx - 2.6, bot, 0], [cx + 2.6, bot, 0], color=VOLT, stroke_width=3))
        # capacitor on the left branch
        x = cx - 1.6
        cap = VGroup(Line([x, top, 0], [x, cy + 0.14, 0], color=VOLT, stroke_width=3),
                     Line([x - 0.45, cy + 0.14, 0], [x + 0.45, cy + 0.14, 0], color=LEAK, stroke_width=6),
                     Line([x - 0.45, cy - 0.14, 0], [x + 0.45, cy - 0.14, 0], color=LEAK, stroke_width=6),
                     Line([x, cy - 0.14, 0], [x, bot, 0], color=VOLT, stroke_width=3))
        # resistor (zigzag) and battery on the right branch
        x = cx + 1.2
        zig = [np.array([x + (0.22 if i % 2 else -0.22) * (0 < i < 7), top - 0.35 - 0.18 * i, 0]) for i in range(8)]
        res = VGroup(Line([x, top, 0], zig[0], color=VOLT, stroke_width=3),
                     VMobject(color=K, stroke_width=4).set_points_as_corners(zig),
                     Line(zig[-1], [x, cy - 0.55, 0], color=VOLT, stroke_width=3))
        bat = VGroup(Line([x - 0.42, cy - 0.55, 0], [x + 0.42, cy - 0.55, 0], color=THRESH, stroke_width=5),
                     Line([x - 0.2, cy - 0.8, 0], [x + 0.2, cy - 0.8, 0], color=THRESH, stroke_width=5),
                     Line([x, cy - 0.8, 0], [x, bot, 0], color=VOLT, stroke_width=3))
        ends = VGroup(label(r"outside", font_size=22, color=GREY_A).next_to(rails[0], UP, buff=0.1),
                      label(r"inside", font_size=22, color=GREY_A).next_to(rails[1], DOWN, buff=0.1))
        g = VGroup(rails, cap, res, bat, ends)
        g.cap, g.res, g.bat = cap, res, bat
        return g

    def parts(self):
        head = heading(r"Three parts, and each is a piece of the cell")
        c = self._circuit(-3.4, -0.3)
        rows = VGroup(
            VGroup(label(r"a capacitor", font_size=32, color=LEAK),
                   wrapped_label(r"the membrane itself: \ a film of fat two molecules thick, with salt water "
                                 r"on both sides, stores charge", 6.2, 26, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"a resistor", font_size=32, color=K),
                   wrapped_label(r"the channels: \ the more that are open, the more easily current leaks "
                                 r"through", 6.2, 26, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"a battery", font_size=32, color=THRESH),
                   wrapped_label(r"the concentration difference: \ the Nernst potential of whatever those "
                                 r"channels pass", 6.2, 26, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.3, -0.2, 0])
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "If you want to know how a voltage changes in time, you draw a circuit. This one has three parts, "
            "and each is something in the cell. <bookmark mark='a'/> The membrane is a film of fat, two "
            "molecules thick, with conducting salt water on either side. Two conductors separated by a thin "
            "insulator is a capacitor. It stores charge, and to change its voltage you have to move charge "
            "onto it, which takes time. <bookmark mark='b'/> The channels are holes in the insulator. Current "
            "leaks through them. That's a resistor, and its resistance falls as more channels open. "
            "<bookmark mark='c'/> And in series with the resistor sits the battery from the last chapter: the "
            "Nernst potential of whatever ion those channels pass. That's the whole membrane. A capacitor, "
            "with a leaky battery across it. Hodgkin and Huxley's model will be this circuit with two extra "
            "branches, and nothing else."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(c[0]), FadeIn(c[4]))
            vo.wait_until("a")
            self.play(Create(c.cap), FadeIn(rows[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(Create(c.res), FadeIn(rows[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(Create(c.bat), FadeIn(rows[2], shift=UP * 0.1))
        self.clear_scene()

    def charging(self):
        d = load("rc")
        head = heading(r"Push current in, and the voltage follows late")
        t = np.asarray(d["t"])
        top = float(d["family"].max()) * 1.12
        A = axes([0, 12], [0, top], x_length=7.0, y_length=3.9, xticks=[0, 2, 4, 6, 8, 10, 12],
                 yticks=[0, 0.5, 1.0, 1.5], xlabel=r"time since the current was switched on (ms)",
                 ylabel=r"change in voltage (mV)", center=[-2.8, -0.55, 0])
        ax = A.ax
        main = curve(ax, t, d["family"][1], VOLT, stroke_width=4)
        others = VGroup(curve(ax, t, d["family"][0], LEAK, stroke_width=2.5), curve(ax, t, d["family"][2], LEAK,
                                                                                    stroke_width=2.5))
        final = d["amp"] * d["r_rest"]
        asym = DashedLine(ax.c2p(0, final), ax.c2p(12, final), color=GREY_B, stroke_width=2)
        asym_l = label(r"$IR$", font_size=24, color=GREY_B).next_to(ax.c2p(12, final), RIGHT, buff=0.08)
        tau_x = d["tau"]
        tau_mark = VGroup(DashedLine(ax.c2p(tau_x, 0), ax.c2p(tau_x, final * 0.632), color=THRESH, stroke_width=2),
                          Dot(ax.c2p(tau_x, final * 0.632), radius=0.09, color=THRESH))
        tau_l = label(rf"$\tau = RC = {d['tau']:.1f}$ ms", font_size=26, color=THRESH).move_to(
            ax.c2p(tau_x + 0.25, 0.16), aligned_edge=LEFT)
        eq = MathTex(r"V(t) \;=\; IR\,\bigl(1 - e^{-t/RC}\bigr)", font_size=40).move_to([4.6, 1.7, 0])
        side = VGroup(
            wrapped_label(r"After one time constant the voltage has gone 63\% of the way.", 4.6, 27, THRESH),
            wrapped_label(r"More open channels: \ smaller $R$, a smaller and quicker response. \ Fewer: "
                          r"larger and slower.", 4.6, 27, LEAK),
            wrapped_label(r"So a membrane adds up what arrives within a few milliseconds, and forgets the rest.",
                          4.6, 27, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(eq, DOWN, buff=0.4)
        keep_in_frame(VGroup(eq, side))
        tag = note(r"computed: \ a leak equal to the model membrane's at rest, and 1 $\mu$F/cm$^2$").to_corner(
            DR, buff=0.2)
        with self.voiceover(
            "Here's what the circuit does. Switch on a small steady current, into the cell. "
            "<bookmark mark='a'/> The voltage doesn't jump. The current first has to charge the capacitor, and "
            "as the voltage rises, more and more of the current escapes through the leak. So the voltage "
            "climbs quickly at first, then more slowly, toward a ceiling set by the current times the "
            "resistance. <bookmark mark='b'/> The curve is an exponential, and it has one number that matters: "
            "the resistance times the capacitance. That's a time, called the time constant. After one time "
            "constant the voltage has covered sixty-three per cent of the distance. For this membrane it's "
            f"about {d['tau']:.1f} milliseconds. <bookmark mark='c'/> Open more channels and the resistance "
            "drops: the response is smaller and faster. Close some and it's larger and slower. "
            "<bookmark mark='d'/> That one number has a meaning for the mind. A membrane can't tell apart two "
            "inputs that arrive within a time constant of each other; it adds them. And it has mostly "
            "forgotten an input that came several time constants ago. So before there's any signalling at "
            "all, a neuron is already an adder with a memory a few milliseconds long."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(main), Create(asym), FadeIn(asym_l), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(tau_mark), FadeIn(tau_l), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(others), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[2], shift=UP * 0.1))
        self.clear_scene()
