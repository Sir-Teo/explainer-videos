from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music.monochord.physics import pluck_shape
from videos.music.music1.common import (BAD, EAR, FREQ, GOOD, HIST, NODE, PART, RATIO, STR, TIME, TUNE, clip, load,
                                        ring, say, window)

X = np.linspace(0, 1, 201)


def area(view: StringView, y: np.ndarray, color, opacity=0.45) -> VMobject:
    """The region between a curve and the string's rest line, filled."""
    pts = [view.p(x, v) for x, v in zip(X, y)]
    m = VMobject(stroke_width=0, fill_color=color, fill_opacity=opacity)
    m.set_points_as_corners([view.p(0.0), *pts, view.p(1.0), view.p(0.0)])
    return m


class Pluck(SoundScene):
    def construct(self):
        self.card()
        self.recipe()
        self.formula()
        self.compare()
        self.practice()
        self.quiz()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(8, r"The plucked string", r"Which modes are in a pluck, \ and how much of each?",
                            lit=(1807,), part=PART)
        with self.voiceover("Chapter eight. The plucked string."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def recipe(self):
        d = load("fourier")
        beta = d["beta"]
        shape = pluck_shape(X, 1.0, beta, 1.0)
        top = StringView(width=8.6, scale=1.1).move_to(LEFT * 2.2 + UP * 1.8)
        top.set_shape(shape)
        modev = StringView(width=8.6, scale=1.1, color=FREQ, stroke_width=2.5, supports=False).move_to(top.axis)
        prod = StringView(width=8.6, scale=1.1, color=GREY_A, stroke_width=2, supports=False).move_to(LEFT * 2.2 + DOWN * 1.7)
        rec = MathTex(r"a_n", r"=", r"\frac{2}{L}\int_0^L", r"f(x)", r"\,\sin\frac{n\pi x}{L}", r"\,dx", font_size=40)
        rec[0].set_color(TUNE), rec[3].set_color(STR), rec[4].set_color(FREQ)
        rec.to_corner(UR, buff=0.45)
        tags = VGroup(label(r"the shape", font_size=24, color=STR).next_to(top.p(beta, 1.0), UP, buff=0.15),
                      label(r"shape $\times$ mode, \ and the area under it", font_size=24, color=GREY_A))
        tags[1].move_to(prod.p(0.62) + UP * 1.25)
        with self.voiceover(
            "Fourier's recipe is a way of asking a shape a question: how much of mode n is in you? "
            "<bookmark mark='a'/> To answer, lay the mode over the shape, multiply the two together point by point, "
            "<bookmark mark='b'/> and add up the result along the whole string. Where shape and mode are on the same "
            "side, they contribute; where they are on opposite sides, they take away. What is left is the amount."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tags[0]))
            vo.wait_until("a")
            modev.set_shape(np.sin(np.pi * X))
            self.play(FadeIn(modev))
            vo.wait_until("b")
            p1 = shape * np.sin(np.pi * X)
            prod.set_shape(p1)
            self.play(FadeIn(prod), FadeIn(tags[1]), FadeIn(area(prod, np.maximum(p1, 0), GOOD)), FadeIn(rec))
        self.clear_scene(top, modev, rec, tags)
        readout = VGroup()
        pos = neg = None
        prod.set_shape(np.zeros(len(X)))
        self.add(prod)
        lines = {1: "Mode one fits the pluck well: a large amount.", 2: "Mode two: less.", 3: "Mode three: less again.",
                 4: "Mode four: a little.",
                 5: "And mode five: the part on the left of the node and the parts on the right cancel exactly. "
                    "There is no mode five in this pluck at all. Look where its node is: right under the finger."}
        for n in (1, 2, 3, 4, 5):
            m = np.sin(n * np.pi * X)
            p = shape * m
            new_pos, new_neg = area(prod, np.maximum(p, 0), GOOD), area(prod, np.minimum(p, 0), BAD)
            val = VGroup(MathTex(rf"n = {n}", font_size=44, color=harmonic_color(n)),
                         MathTex(rf"a_{n} = {d['a'][n - 1] + 0.0:.3f}", font_size=44, color=TUNE)).arrange(DOWN, buff=0.25)
            val.move_to(RIGHT * 4.6 + DOWN * 1.5)
            with self.voiceover(lines[n]):
                modev.set_shape(m)
                modev.curve.set_stroke(color=harmonic_color(n))
                prod.set_shape(p)
                anims = [FadeIn(new_pos), FadeIn(new_neg), FadeIn(val)]
                if pos is not None:
                    anims += [FadeOut(pos), FadeOut(neg), FadeOut(readout)]
                self.play(*anims, run_time=0.6)
                if n == 5:
                    node = Dot(top.p(beta), radius=0.09, color=NODE)
                    self.play(FadeIn(node, scale=2.0))
            pos, neg, readout = new_pos, new_neg, val
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def formula(self):
        thm = theorem_card(
            r"The plucked string", MathTex(
                r"a_n \;=\; \frac{2h}{\pi^2 \beta (1-\beta)} \cdot \frac{1}{n^2} \cdot \sin(n\pi\beta)", font_size=44),
            who=r"a string pulled aside by $h$ at the fraction $\beta$ of its length, and let go", color=GOOD,
            width=9.6, kind=r"Result").to_edge(UP, buff=0.45)
        a = VGroup(MathTex(r"\frac{1}{n^2}", font_size=54, color=TIME),
                   label(r"the higher the mode, \\ the less of it: \ fast", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.4)
        b = VGroup(MathTex(r"\sin(n\pi\beta)", font_size=46, color=NODE),
                   label(r"the mode's own height at the plucking point: \\ zero if it has a node there", font_size=26,
                         color=GREY_A)).arrange(RIGHT, buff=0.4)
        VGroup(a, b).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(DOWN * 0.6)
        bridge = VGroup(label(r"what the bridge feels is the string's slope, not its height:", font_size=26, color=GREY_B),
                        MathTex(r"\text{force on the bridge} \;\propto\; n\, a_n \;\propto\; \frac{\sin(n\pi\beta)}{n}",
                                font_size=38, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "For a pluck the sum can be done exactly, and here is the answer. <bookmark mark='a'/> It has two parts "
            "that matter. One over n squared: the higher the mode, the less of it there is, and the amounts fall "
            "quickly. <bookmark mark='b'/> And the sine of n pi beta, which is nothing but the height of mode n at "
            "the point where you plucked. If a mode has a node there, it gets nothing. You cannot start a mode by "
            "pulling on the one place where it does not move."
        ) as vo:
            self.play(FadeIn(thm, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b))
        with self.voiceover(
            "One correction before we listen. A string moves almost no air. What makes the sound is the force it "
            "puts on the bridge, and that goes with the string's slope at the end, not its height. "
            "<bookmark mark='a'/> Taking a slope multiplies mode n by n. So at the bridge the amounts fall as one "
            "over n, not one over n squared: brighter than the shape alone suggests."
        ) as vo:
            self.play(FadeIn(bridge[0]))
            vo.wait_until("a")
            self.play(FadeIn(bridge[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("pluck")
        keys = [("b50", r"\tfrac{1}{2}", "the middle"), ("b33", r"\tfrac{1}{3}", "one third"),
                ("b20", r"\tfrac{1}{5}", "one fifth"), ("b10", r"\tfrac{1}{10}", "one tenth")]
        panels = VGroup()
        for key, frac, _ in keys:
            r = d["rows"][key]
            v = StringView(width=2.7, scale=0.5, stroke_width=3)
            v.set_shape(pluck_shape(X, 1.0, r["beta"], 1.0))
            fingertip = Dot(v.p(r["beta"], 1.0), radius=0.07, color=HIST)
            head = VGroup(label(r"plucked at", font_size=24, color=GREY_B), MathTex(frac, font_size=34, color=RATIO)
                          ).arrange(RIGHT, buff=0.15)
            meas = 10 ** (np.array(r["measured_db"][:12]) / 20)
            pred = 10 ** (np.array(r["force_db"][:12]) / 20)
            bars = partial_bars(meas, width=2.9, height=1.7, db=False, font_size=14)
            ticks = VGroup(*[Line(LEFT * 0.1, RIGHT * 0.1, color=WHITE, stroke_width=2.5).move_to(
                [b.get_x(), bars.base.get_y() + pred[i] * 1.7, 0]) for i, b in enumerate(bars.bars)])
            panel = VGroup(head, VGroup(v, fingertip), VGroup(bars, ticks)).arrange(DOWN, buff=0.4)
            panel.head, panel.view, panel.bars = head, v, bars
            panels.add(panel)
        panels.arrange(RIGHT, buff=0.4).move_to(DOWN * 0.3)
        leg = VGroup(VGroup(Rectangle(width=0.22, height=0.3, stroke_width=0, fill_color=harmonic_color(1), fill_opacity=1),
                            label(r"simulated: \ the force on the bridge, \ partial by partial", font_size=24, color=GREY_A)
                            ).arrange(RIGHT, buff=0.15),
                     VGroup(Line(LEFT * 0.12, RIGHT * 0.12, color=WHITE, stroke_width=3),
                            label(r"predicted: \ $\sin(n\pi\beta)/n$", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.15)
                     ).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.4)
        worst = max(r["worst_db"] for r in d["rows"].values())
        with self.voiceover(
            "Here is the test. Four plucks of the same string at the same pitch: in the middle, at a third, at a "
            "fifth, and at a tenth of the way along. <bookmark mark='a'/> The bars are the partials of the force on "
            "the bridge, taken from the bead simulation. The white marks are the formula. They agree to within "
            f"{say(worst, 1)} decibels on every partial that matters. Now listen to the four."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p) for p in panels], lag_ratio=0.2), run_time=1.6)
            vo.wait_until("a")
            self.play(FadeIn(leg))
        for (key, frac, where), panel in zip(keys, panels):
            with self.listen(clip(f"pluck.{key}")) as snd:
                window(snd, rf"plucked at {where}")
                frame = SurroundingRectangle(panel, color=TUNE, buff=0.12, corner_radius=0.1, stroke_width=2)
                lens = Lens(panel.view.p(0), panel.view.p(1), amp=0.12, color=TUNE)
                snd.show(frame, lens)
                snd.drive(lens, ring(rate=1.5))
        with self.voiceover(
            "In the middle, every even partial is missing, and the sound is hollow. Hold on to that sound: a "
            "clarinet has the same gap, for a different reason, and we will meet it in Part 8. "
            "<bookmark mark='a'/> At a third, partials three, six and nine are gone. <bookmark mark='b'/> And near "
            "the end, the first ten partials are nearly equal: bright, thin and nasal."
        ) as vo:
            self.play(Indicate(panels[0].bars, color=TUNE, scale_factor=1.05))
            vo.wait_until("a")
            self.play(Indicate(panels[1].bars, color=TUNE, scale_factor=1.05))
            vo.wait_until("b")
            self.play(Indicate(panels[3].bars, color=TUNE, scale_factor=1.05))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def practice(self):
        d = load("pluck")
        c = clip("pluck.sweep")
        s = StringView(width=10.4, scale=0.9).move_to(UP * 1.6)
        s.set_shape(pluck_shape(X, 1.0, 0.5, 1.0))
        tasto = label(r"\textit{sul tasto}: \ over the fingerboard, \ soft", font_size=26, color=GREY_A).move_to(s.p(0.5) + UP * 1.5)
        pont = label(r"\textit{sul ponticello}: \ by the bridge, \ bright", font_size=26, color=GREY_A)
        pont.next_to(s.p(0.0), DOWN, buff=0.5).align_to(s.p(0.0), LEFT)
        n = np.arange(1, 17)

        def levels(beta):
            v = np.abs(np.sin(n * np.pi * beta)) / n
            return v / v.max()

        bars = partial_bars(levels(0.5), width=9.0, height=1.9, db=False).move_to(DOWN * 1.9)
        with self.voiceover(
            "Every player of a plucked or bowed instrument uses this, whether or not they know the formula. "
            "<bookmark mark='a'/> Guitarists and violinists have names for the two ends of the range: over the "
            "fingerboard for a soft, round tone, <bookmark mark='b'/> by the bridge for a bright, glassy one. A "
            "harpsichord maker chooses the plucking point for every string, and a piano's hammers strike about an "
            "eighth of the way along. Listen to one string as the plucking point walks from the middle to the end."
        ) as vo:
            self.play(FadeIn(s), FadeIn(bars))
            vo.wait_until("a")
            self.play(FadeIn(tasto))
            vo.wait_until("b")
            self.play(FadeIn(pont))
        with self.listen(c) as snd:
            window(snd, r"from the middle to the end")
            for i, beta in enumerate(d["sweep_betas"]):
                snd.wait_until(f"p{i}")
                s.set_shape(pluck_shape(X, 1.0, beta, 1.0))
                new = partial_bars(levels(beta), width=9.0, height=1.9, db=False).move_to(DOWN * 1.9)
                self.remove(bars)
                bars = new
                self.add(bars)
                self.wait(0.12)
                s.set_shape(np.zeros(len(X)))
                lens = Lens(s.p(0), s.p(1), amp=0.2, color=TUNE,
                            shape=np.minimum(X / beta, (1 - X) / (1 - beta)))
                snd.show(lens)
                nxt = snd.time_of(f"p{i + 1}") if i + 1 < len(d["sweep_betas"]) else None
                snd.drive(lens, ring(at=snd.time_of(f"p{i}") + 0.12, rate=2.0, stop_at=nxt))
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("pluck")
        q = listen_card(r"The same note, \ plucked twice: \ A and B. \\ Which one was plucked in the middle of the "
                        r"string?", width=9.4).to_edge(UP, buff=0.6)
        boxes = VGroup(*[VGroup(RoundedRectangle(width=2.6, height=1.6, corner_radius=0.15, stroke_color=GREY_C,
                                                 stroke_width=2), label(t, font_size=60, color=GREY_A))
                         for t in ("A", "B")]).arrange(RIGHT, buff=1.4).shift(DOWN * 0.6)
        with self.voiceover("A question for your ears. The same note, plucked twice. Which one was plucked in the "
                            "middle of the string?"):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(boxes))
        c = clip("pluck.quiz")
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", tag_corner=DR)
            for i, (key, box) in enumerate(zip("AB", boxes)):
                snd.wait_until(key)
                box[1].set_color(EAR)
                glow = box[0].copy().set_stroke(EAR, width=5)
                snd.show(glow)
                t0 = snd.time_of(key)
                t1 = snd.time_of("B") if i == 0 else c.duration
                # the box's edge fades with the note: no picture of the string, which would give the answer away
                snd.drive(glow, lambda m, t, t0=t0, t1=t1: m.set_stroke(
                    opacity=float(np.exp(-2.2 * max(t - t0, 0.0))) if t < t1 else 0.0))
                snd.wait_until(t1 - 0.05)
                box[1].set_color(GREY_A)
        v = [StringView(width=2.4, scale=0.4, stroke_width=3) for _ in range(2)]
        v[0].set_shape(pluck_shape(X, 1.0, 0.1, 1.0))
        v[1].set_shape(pluck_shape(X, 1.0, 0.5, 1.0))
        for view, box in zip(v, boxes):
            view.next_to(box, DOWN, buff=0.45)
        with self.voiceover(
            f"{d['quiz_answer']}. The hollow one, with its even partials missing. A was plucked a tenth of the way "
            "along. <bookmark mark='a'/> So one pluck sets a dozen modes going at once, in amounts we can "
            "calculate. The obvious question is whether we actually hear them."
        ) as vo:
            self.play(FadeIn(v[0]), FadeIn(v[1]), boxes[1][0].animate.set_stroke(GOOD, width=4))
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()
