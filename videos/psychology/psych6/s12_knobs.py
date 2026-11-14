from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403

from explainer.psychology.psyche import circuits  # isort: skip

SYSTEMS = [(r"dopamine", RULE), (r"serotonin", "#5BD18B"), (r"noradrenaline", THRESH), (r"acetylcholine", DATA)]


class Knobs(VoiceoverScene):
    def construct(self):
        self.card()
        self.broadcast()
        self.gain()
        self.rate()

    def card(self):
        card = chapter_card(11, r"Knobs: \ the neuromodulators", r"What can a broadcast chemical usefully say?",
                            lit=(), part=PART, scale=("circuit", "brain"), marr=("how",))
        with self.voiceover(
            "Chapter eleven. Knobs: the neuromodulators."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def broadcast(self):
        head = heading(r"A few cells, \ speaking to everything at once")
        hd = head_outline(5.6).move_to([-3.7, -0.4, 0])
        centre = hd.get_center() + np.array([-0.25, 0.75, 0])
        g = np.random.default_rng(11)
        fans, nuclei = VGroup(), VGroup()
        for k, (name, col) in enumerate(SYSTEMS):
            src = centre + np.array([-0.45 + 0.3 * k, -1.25 - 0.12 * (k % 2), 0])
            nuclei.add(Dot(src, radius=0.11, color=col))
            fan = VGroup()
            for a in np.linspace(0.25, PI - 0.25, 8) + 0.12 * g.standard_normal(8):
                end = centre + np.array([1.75 * np.cos(a), 1.3 * np.sin(a) - 0.1, 0])
                fan.add(Line(src, end, color=col, stroke_width=2, stroke_opacity=0.8))
            fans.add(fan)
        names = VGroup(*[label(n, font_size=28, color=col) for n, col in SYSTEMS]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.16)
        rows = VGroup(
            names,
            wrapped_label(r"each made by a small cluster of cells deep in the brain, \ with axons that reach "
                          r"almost everywhere", 5.6, 27, WHITE),
            wrapped_label(r"slow receptors (the second kind from chapter 1): \ seconds, not milliseconds", 5.6, 27,
                          GREY_A),
            wrapped_label(r"A signal that goes everywhere cannot say \emph{what}. \ It can say \emph{how}: \ how "
                          r"strongly to respond, \ how fast to learn.", 5.6, 28, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.5, -0.3, 0])
        keep_in_frame(rows)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Back in chapter two we set four transmitters to one side, as broadcasters. Here's what's "
            "different about them. <bookmark mark='a'/> Each is made by a small cluster of cells deep in the "
            "brain, and those cells send their axons almost everywhere. <bookmark mark='b'/> And they act "
            "mainly through the slow kind of receptor, the kind that changes how a cell behaves over seconds. "
            "<bookmark mark='c'/> Now think about what such a system could possibly be for. A signal that "
            "reaches everything at once can't carry content. It can't say, there's an edge here, or, choose "
            "the left one. What it can carry is something about the state of the whole animal, something "
            "every circuit ought to know. In a model, that means it turns a knob. There are two knobs we've "
            "already built, and I'll show you both."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hd), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(nuclei), LaggedStart(*[Create(f) for f in fans], lag_ratio=0.3), FadeIn(rows[1]),
                      run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def gain(self):
        k = load("knobs")
        head = heading(r"Knob one: \ gain")
        A = axes([-2, 8], [0, 1.05], x_length=6.6, y_length=4.2, xticks=[0, 2, 4, 6, 8], yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:.1f}", xlabel=r"input to a unit", ylabel=r"its response", center=[-3.2, -0.5, 0])
        ax = A.ax
        cols = [INH, VOLT, EXC]
        curves = VGroup(*[trace(ax, k["x"], c, col) for c, col in zip(k["curves"], cols)])
        lg = legend([(col, rf"gain {g_:g}") for g_, col in zip(k["gains"], cols)], font_size=24)
        lg.next_to(ax.c2p(-2, 1.05), DR, buff=0.2)
        xa, xb = 2.5, 3.5
        def gap(g_):
            return float(circuits.sigmoid(xb, g_, 3.0) - circuits.sigmoid(xa, g_, 3.0))

        marks = VGroup(*[DashedLine(ax.c2p(x, 0), ax.c2p(x, 1.05), color=GREY_C, stroke_width=1.5) for x in (xa, xb)])
        marks_l = label(r"two inputs, one unit apart", font_size=22, color=GREY_B).next_to(ax.c2p(3.0, 1.05), UP,
                                                                                         buff=0.06)
        side = VGroup(
            wrapped_label(rf"low gain: \ the two responses differ by {gap(k['gains'][0]):.2f}", 4.8, 27, INH),
            wrapped_label(rf"high gain: \ by {gap(k['gains'][2]):.2f}", 4.8, 27, EXC),
            wrapped_label(r"High gain: \ decisive, committed to the strongest input. \ Low gain: \ open to the "
                          r"alternatives.", 4.8, 27, WHITE),
            wrapped_label(r"a leading hypothesis for noradrenaline; \ tested in the parts on attention", 4.8, 26,
                          P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.2, -0.4, 0])
        keep_in_frame(side)
        tag = psyche_tag()
        with self.voiceover(
            "The first knob is gain. Every unit in the last four chapters had an S-shaped response curve. "
            "<bookmark mark='a'/> Gain is its steepness. <bookmark mark='b'/> Take two inputs a little way "
            "apart. With the gain low, the unit responds to them almost alike: a difference of "
            f"{gap(k['gains'][0]):.2f}. With the gain high, the same two inputs are driven far apart: "
            f"{gap(k['gains'][2]):.2f}. <bookmark mark='c'/> Now imagine that turned up across a whole "
            "brain. Every winner-take-all circuit decides faster and commits harder to whatever is strongest. "
            "Turned down, the circuits loosen, and weaker alternatives get a hearing. Exploit, or explore. "
            "<bookmark mark='d'/> That's a leading hypothesis for what noradrenaline does. It's a hypothesis, "
            "and we'll put it to the evidence when we get to attention."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(curves[1]), FadeIn(lg[1]))
            vo.wait_until("a")
            self.play(Create(curves[0]), Create(curves[2]), FadeIn(lg[0]), FadeIn(lg[2]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(marks), FadeIn(marks_l))
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def rate(self):
        k = load("knobs")
        head = heading(r"Knob two: \ the learning rate")
        A = axes([0, 300], [0.94, 1.005], x_length=6.6, y_length=4.0, xticks=[0, 100, 200, 300],
                 yticks=[0.95, 0.97, 0.99], yfmt=lambda v: f"{v:.2f}", xlabel=r"steps of learning",
                 ylabel=r"agreement with the right answer", center=[-3.2, -0.5, 0])
        ax = A.ax
        n = np.arange(301)
        slow = trace(ax, n, np.clip(k["slow"][:301], 0.94, 1.0), INH, 3)
        fast = trace(ax, n, np.clip(k["fast"][:301], 0.94, 1.0), EXC, 3)
        goal = DashedLine(ax.c2p(0, 0.99), ax.c2p(300, 0.99), color=GREY_C, stroke_width=1.5)
        lg = legend([(EXC, rf"fast, $\eta = {k['fast_eta']:g}$"), (INH, rf"slow, $\eta = {k['slow_eta']:g}$")],
                    font_size=24)
        lg.next_to(ax.c2p(300, 0.94), UL, buff=0.2)
        side = VGroup(
            wrapped_label(rf"fast: \ there in {k['fast_steps']} steps, \ then jerked about by every new sample",
                          4.8, 27, EXC),
            wrapped_label(rf"slow: \ {k['slow_steps']} steps, \ then steady", 4.8, 27, INH),
            MathTex(r"\Delta w \;=\; m \cdot \eta\, x\, y", font_size=44, color=RULE),
            wrapped_label(r"a third factor $m$, broadcast: \ learn now, this matters", 4.8, 27, WHITE),
            wrapped_label(r"dopamine as that signal: \ Part 17", 4.8, 27, P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([4.2, -0.4, 0])
        keep_in_frame(side)
        tag = psyche_tag()
        with self.voiceover(
            "The second knob is the learning rate. Go back to the cell learning by Oja's rule, and run it "
            "twice. <bookmark mark='a'/> With a large learning rate it finds the right direction in "
            f"{k['fast_steps']} steps. But it never settles. Every new sample jerks it about. "
            f"<bookmark mark='b'/> With a small learning rate it takes {k['slow_steps']} steps, ten times as "
            "long, and then it's steady. Fast and unstable, or slow and stable. No single setting is right. "
            "It depends on whether the world has just changed. <bookmark mark='c'/> So let a broadcast "
            "signal set it. Multiply Hebb's term by a third factor, delivered to every synapse at once, "
            "that says: something important just happened, learn from it now. <bookmark mark='d'/> A "
            "three-factor rule of this kind is a leading proposal for how learning is steered in a real "
            "brain. And the best-studied candidate for the third factor is dopamine. Part 17 is about "
            "exactly what it signals."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(goal))
            vo.wait_until("a")
            self.play(Create(fast), FadeIn(lg[0]), FadeIn(side[0]), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(Create(slow), FadeIn(lg[1]), FadeIn(side[1]), run_time=4.0, rate_func=linear)
            vo.wait_until("c")
            self.play(Write(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()
