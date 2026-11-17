from __future__ import annotations

import numpy as np

from videos.psychology.psych8.common import *  # noqa: F403


class Units(VoiceoverScene):
    def construct(self):
        self.card()
        self.method()
        self.tuning()
        self.limits()

    def card(self):
        card = chapter_card(1, r"Listening to one neuron", r"What does a single cell tell you?",
                            lit={1959: r"Hubel \& Wiesel"}, part=PART, scale=("neuron",), marr=("what", "tissue"))
        with self.voiceover(
            "Chapter one. Listening to one neuron."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def _bar(self, center, angle_deg, length=1.5, color=VOLT):
        a = np.deg2rad(angle_deg)
        d = np.array([np.cos(a), np.sin(a), 0]) * length / 2
        return Line(np.asarray(center) - d, np.asarray(center) + d, color=color, stroke_width=8)

    def method(self):
        head = heading(r"1959: \ a wire next to one cell, \ and a line of light")
        screen = RoundedRectangle(width=4.4, height=3.0, corner_radius=0.1, color=GREY_B, stroke_width=3,
                                  fill_color="#05070B", fill_opacity=1).move_to([-4.3, 0.55, 0])
        bar = self._bar(screen.get_center(), 0, 2.2)
        screen_l = label(r"what the cat sees", font_size=28, color=GREY_A).next_to(screen, UP, buff=0.1)
        speaker = VGroup(Line([-6.5, -2.6, 0], [-2.1, -2.6, 0], color=GREY_D, stroke_width=2))
        g = np.random.default_rng(3)
        quiet = VGroup(*[Line([x, -2.6, 0], [x, -1.85, 0], color=SPIKE, stroke_width=3.5) for x in
                         np.sort(g.uniform(-6.4, -2.2, 3))])
        loud = VGroup(*[Line([x, -2.6, 0], [x, -1.85, 0], color=SPIKE, stroke_width=3.5) for x in
                        np.sort(g.uniform(-6.4, -2.2, 30))])
        sp_l = label(r"the cell's impulses, \ one second", font_size=28, color=SPIKE).next_to(speaker, DOWN, buff=0.12)
        rows = rows_of([
            (r"a fine wire, \ next to one cell in the visual cortex of an anaesthetized cat", WHITE),
            (r"spots of light, \ which had worked in the eye: \ almost nothing", GREY_A),
            (r"a line at the right angle: \ a burst of impulses", SPIKE),
            (r"turn the line a little, \ and the cell goes quiet", WHITE),
        ], 5.9, 31).move_to([3.75, -0.2, 0])
        keep_in_frame(rows)
        src = historical_tag(archive.HUBEL_WIESEL_1959.cite)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The first link of the chain is one cell. In Part 5 we put a wire inside a giant axon. A finer "
            "wire can be parked next to a cell in a living brain, close enough to pick up each of its "
            "impulses, and you can listen to them through a loudspeaker. <bookmark mark='a'/> In the late "
            "nineteen-fifties David Hubel and Torsten Wiesel did that in the visual cortex of anaesthetized "
            "cats, and showed the cat patterns of light. <bookmark mark='b'/> They began with spots, "
            "because spots were what excited cells in the eye. The cortical cells mostly ignored them. "
            "<bookmark mark='c'/> Then, by their own account, a cell went off like a machine gun when the "
            "edge of a glass slide slid across the projector, throwing a line onto the screen. The cell "
            "wanted a line. <bookmark mark='d'/> And a line at one particular angle. Turn it, and the cell "
            "fell quiet. So here was a cell in a brain whose activity meant something you could state: "
            "there's an edge, here, tilted this way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(tag), FadeIn(screen), FadeIn(screen_l), FadeIn(speaker),
                      FadeIn(sp_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            spot = Dot(screen.get_center(), radius=0.18, color=VOLT)
            self.play(FadeIn(spot), FadeIn(quiet), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeOut(spot), FadeOut(quiet), run_time=0.3)
            self.play(FadeIn(bar), FadeIn(loud, lag_ratio=0.05), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Rotate(bar, angle=PI / 3), FadeOut(loud), FadeIn(quiet), FadeIn(rows[3]))
        self.clear_scene()

    def tuning(self):
        t = load("tuning")
        head = heading(r"A tuning curve: \ the cell's answer to every angle")
        # three rasters
        ras = VGroup()
        for i, ang in enumerate((45, 75, 135)):
            y = 1.9 - 1.5 * i
            line = Line([-6.4, y - 0.3, 0], [-2.9, y - 0.3, 0], color=GREY_D, stroke_width=2)
            ticks = VGroup(*[Line([-6.4 + 3.5 * x, y - 0.3, 0], [-6.4 + 3.5 * x, y + 0.2, 0], color=SPIKE, stroke_width=2.5)
                             for x in t[f"raster_{ang}"]])
            icon = self._bar([-6.75, y - 0.05, 0], ang, 0.5, VOLT)
            cap = label(rf"{t[f'rate_{ang}']:.0f} a second", font_size=27, color=SPIKE).next_to(line, DOWN, buff=0.08)
            ras.add(VGroup(line, ticks, icon, cap))
        A = axes([0, 180], [0, 50], x_length=5.6, y_length=3.7, xticks=[0, 45, 90, 135, 180], yticks=[0, 20, 40],
                 xlabel=r"angle of the line (degrees)", ylabel=r"impulses a second", center=[3.1, -0.05, 0])
        ax = A.ax
        c = curve(ax, t["fine"], t["curve"], MODEL, stroke_width=4)
        dots = VGroup(*[VGroup(Line(ax.c2p(x, m - s), ax.c2p(x, m + s), color=SPIKE, stroke_width=2),
                               Dot(ax.c2p(x, m), radius=0.07, color=SPIKE))
                        for x, m, s in zip(t["theta"], t["mean_rate"], t["sem_rate"])])
        lg = legend([(SPIKE, r"counted: 8 showings at each angle"), (MODEL, r"the cell's tuning curve")], font_size=26)
        lg.next_to(A, UP, buff=0.12)
        end = wrapped_label(r"A tuning curve is a cell's whole vocabulary on one axis: \ what it says, about what.",
                            12.6, 30, P.ACCENT).to_edge(DOWN, buff=0.85)
        tag = psyche_tag(r"computed: a model cell (Psyche)")
        with self.voiceover(
            "Make that a measurement. Here's a model cell of the same kind. <bookmark mark='a'/> Show it a "
            f"line at its favourite angle, and in one second it fires about {t['rate_45']:.0f} impulses. "
            f"Thirty degrees off, about {t['rate_75']:.0f}. At right angles to its favourite, "
            f"{t['rate_135']:.0f}, which is what it does with no stimulus at all. <bookmark mark='b'/> Now "
            "do it properly: every angle, several times each, count the impulses, and plot the average "
            "against the angle. The counts scatter, because a cell's firing is noisy, as Part 5 showed. "
            "<bookmark mark='c'/> Through them runs a smooth hill. That's the cell's tuning curve. "
            "<bookmark mark='d'/> It's the basic description of a sensory neuron, and it answers two "
            "questions at once. What is this cell about? The angle of an edge. And how does it say it? With "
            "its rate. Every cell in the first visual area has such a curve, each with its own favourite "
            "angle, and together they cover all of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in ras], lag_ratio=0.9), run_time=9.0)
            vo.wait_until("b")
            self.play(FadeIn(A), FadeIn(dots, lag_ratio=0.1), FadeIn(lg[0]), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(c), FadeIn(lg[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def limits(self):
        head = heading(r"What one cell can and cannot tell you")
        rows = VGroup(
            VGroup(label(r"what it gives", font_size=36, color=MODEL),
                   wrapped_label(r"the real signal, impulse by impulse, to the millisecond, \ from a cell you can "
                                 r"point to", 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"what it costs", font_size=36, color=BAD),
                   wrapped_label(r"a hole in the skull: \ so, animals, \ and people only when surgery is already "
                                 r"needed", 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"what it misses", font_size=36, color=THRESH),
                   wrapped_label(r"one cell of 86 billion, \ or today a few thousand at once: \ a keyhole",
                                 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(label(r"so the rest of this part", font_size=36, color=P.ACCENT),
                   wrapped_label(r"is about instruments that stay outside the head, \ and what they give up to "
                                 r"do so", 12.4, 31, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, -0.35, 0])
        with self.voiceover(
            "Keep this as the standard everything else is measured against. <bookmark mark='a'/> A wire "
            "next to a cell gives you the real signal. Each impulse, to the millisecond, from a cell whose "
            "place you know. <bookmark mark='b'/> The cost is a hole in the skull. So nearly all of this "
            "work is in animals, and in people only when surgery is needed anyway. <bookmark mark='c'/> "
            "And it's a keyhole. One cell out of eighty-six billion, or, with today's probes, a few "
            "thousand at once. You learn a great deal about very little. <bookmark mark='d'/> So the rest "
            "of this part is about instruments that stay outside the head. Each of them pays for that "
            "politeness. The question to ask of every one is the same: what does it measure, how far is "
            "that from an impulse, and what was given up on the way?"
        ) as vo:
            self.play(FadeIn(head))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
        self.clear_scene()
