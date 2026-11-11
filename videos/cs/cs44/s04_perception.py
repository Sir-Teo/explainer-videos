from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


class Perception(VoiceoverScene):
    def construct(self):
        self.card()
        self.thresholds()
        self.latency()
        self.weber()
        self.popout()
        self.change()

    def card(self):
        card = chapter_card(3, r"Perception and its thresholds", r"What do people notice, \ and how fast?",
                            lit=(1860, 1968, 1980), extra=((1860, r"Fechner: \ psychophysics"),
                                                           (1968, r"Miller: \ response time"),
                                                           (1980, r"Treisman and Gelade")), part=PART)
        with self.voiceover("Chapter three. Perception and its thresholds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def thresholds(self):
        head = label(r"0.1, \ 1 and 10 seconds", font_size=36).to_edge(UP, buff=0.3)
        x0, dec, y = -5.6, 2.8, 0.9

        def X(t):
            return x0 + (math.log10(t) + 2) * dec
        axis = Line([X(0.01), y, 0], [X(100), y, 0], color=GREY_C, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([X(t), y - 0.1, 0], [X(t), y + 0.1, 0], color=GREY_C),
                                label(s, font_size=18, color=GREY_A).next_to([X(t), y + 0.1, 0], UP, buff=0.1))
                         for t, s in ((0.01, r"0.01 s"), (0.1, r"0.1 s"), (1, r"1 s"), (10, r"10 s"),
                                      (100, r"100 s"))])
        zones = [(0.01, 0.1, YES, r"feels \textbf{instantaneous}: \ the result is the only feedback needed"),
                 (0.1, 1, HEAD, r"the delay is noticed, \ but the \textbf{flow of thought} is kept"),
                 (1, 10, KERN, r"\textbf{attention} is kept, \ just: \ show that work is happening"),
                 (10, 100, NO, r"attention wanders: \ show progress, \ let people do something else")]
        bands = VGroup()
        for a, b, c, t in zones:
            band = Rectangle(width=X(b) - X(a), height=0.22, stroke_width=0, fill_color=c, fill_opacity=0.7)
            band.move_to([(X(a) + X(b)) / 2, y - 0.25, 0])
            txt = wrapped_label(t, dec - 0.2, font_size=21, color=c).next_to(band, DOWN, buff=0.3)
            bands.add(VGroup(band, txt))
        wait = Triangle(color=WHITE, fill_opacity=1).scale(0.12).rotate(PI).move_to([X(0.01), y + 0.95, 0])
        wl = label(r"waiting for a response", font_size=17, color=WHITE).next_to(wait, UP, buff=0.08)
        src = wrapped_label(r"Miller \ (1968); \ Card, \ Robertson and Mackinlay \ (1991); \ Nielsen, \ "
                            r"\textit{Usability Engineering} \ (1993)", 12.4, font_size=18, color=GREY_B)
        src.to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The first thresholds are in time. In 1968 Robert Miller, at IBM, asked how fast a computer must answer "
            "a person, and the answer has been restated ever since, by Card, Robertson and Mackinlay in 1991 and by "
            "Jakob Nielsen in 1993. <bookmark mark='a'/> Under a tenth of a second, a response feels instantaneous: "
            "the result itself is all the feedback needed. <bookmark mark='b'/> Under a second, the delay is "
            "noticed, but the user's flow of thought is not broken. <bookmark mark='c'/> Under ten seconds, "
            "attention holds, if the interface shows that work is happening. <bookmark mark='d'/> Beyond that, "
            "people turn away: show real progress, and let them do something else."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(ticks), FadeIn(wait), FadeIn(wl), FadeIn(src))
            for mk, (a, b, _, _), band in zip("abcd", zones, bands):
                vo.wait_until(mk)
                self.play(FadeIn(band), VGroup(wait, wl).animate.shift(RIGHT * (X(b) - wait.get_x())),
                          run_time=1.2)
        self.wait(0.4)
        self.clear_scene()

    def latency(self):
        head = label(r"Input latency", font_size=36).to_edge(UP, buff=0.3)
        x0, x1 = -6.2, -0.4
        t = ValueTracker(0.0)
        speed = 4.0                          # scene units per second of the animation

        def drag(y, lag, colour):
            track = Line([x0, y, 0], [x1, y, 0], color=GREY_D, stroke_width=2)
            obj = always_redraw(lambda: Square(0.36, stroke_width=0, fill_color=colour, fill_opacity=0.9).move_to(
                [min(x0 + speed * max(t.get_value() - lag, 0), x1 - 0.3), y, 0]))
            finger = always_redraw(lambda: Circle(0.24, stroke_color=WHITE, stroke_width=2.5).move_to(
                [min(x0 + speed * t.get_value(), x1 - 0.3), y, 0]))
            return track, obj, finger
        r1 = drag(1.5, 0.30, NO)
        r2 = drag(0.2, 0.03, YES)
        l1 = label(r"a long delay: \ the object trails the finger", font_size=18, color=NO).next_to(
            [x0, 1.5 + 0.35, 0], UP, buff=0.05, aligned_edge=LEFT)
        l2 = label(r"a short one: \ it stays under the finger", font_size=18, color=YES).next_to(
            [x0, 0.2 + 0.35, 0], UP, buff=0.05, aligned_edge=LEFT)
        tag = note(r"illustrative", font_size=16).next_to(r2[0], DOWN, buff=0.15).align_to(r2[0], LEFT)
        ng = wrapped_label(r"Ng et al. \ (Microsoft Research, \ 2012): \ people dragging on a touch screen "
                           r"notice delays of a few milliseconds, \ far below a tenth of a second", 5.6,
                           font_size=19, color=WHITE).move_to([3.6, 1.0, 0])
        stages = [r"sense", r"OS", r"app", r"render", r"compose", r"display"]
        fw = 1.9
        frames = VGroup(*[VGroup(Rectangle(width=fw, height=0.5, stroke_color=GREY_B, stroke_width=1.5,
                                           fill_color=[DATA, LAM, KERN, HEAD, YES, NO][k], fill_opacity=0.25),
                                 label(s, font_size=18, color=WHITE))
                          for k, s in enumerate(stages)]).arrange(RIGHT, buff=0.08).move_to([0, -1.55, 0])
        for f in frames:
            f[1].move_to(f[0])
        br = Brace(frames[0], DOWN, color=GREY_B)
        bl = label(r"one frame: \ $1000/60 \approx 16.7$ ms at 60 Hz \ (Part 42)", font_size=18, color=GREY_A).next_to(
            br, DOWN, buff=0.08).align_to(frames, LEFT)
        foot = wrapped_label(r"a key press or a touch travels through stages, \ and each one that waits for the next "
                             r"frame adds up to a frame; \ latencies add, \ so every stage must be budgeted", 6.6,
                             font_size=19, color=YES).next_to(bl, DOWN, buff=0.25).align_to(frames, RIGHT)
        ptag = note(r"stages illustrative", font_size=16).next_to(frames, UP, buff=0.1).align_to(frames, RIGHT)
        with self.voiceover(
            "Direct manipulation is stricter than a tenth of a second. <bookmark mark='a'/> When you drag something "
            "under your finger, any delay shows as a gap between the finger and the thing. In 2012 Albert Ng and "
            "colleagues at Microsoft Research built a touch screen with almost no delay, and found that people "
            "dragging on it could notice latencies of only a few milliseconds. <bookmark mark='b'/> Every input "
            "travels a pipeline: the sensor, the operating system, the application, rendering, compositing and the "
            "display. Each stage that waits for the next frame can add a whole frame, sixteen point seven "
            "milliseconds at sixty hertz, the frame budget of Part 42. Latencies add, so each stage must be "
            "budgeted."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(m) for m in (*r1, *r2)], FadeIn(l1), FadeIn(l2), FadeIn(tag))
            vo.wait_until("a")
            self.play(t.animate.set_value(1.2), run_time=3.0, rate_func=linear)
            self.play(FadeIn(ng))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in frames], lag_ratio=0.25), FadeIn(ptag))
            self.play(FadeIn(br), FadeIn(bl), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def weber(self):
        head = label(r"Weber and Fechner: \ differences are relative", font_size=36).to_edge(UP, buff=0.3)
        u, xl = 1.0, -6.3
        pairs = [(1.0, 1.1, r"$+0.1$: \ $+10\%$", YES), (4.0, 4.1, r"$+0.1$: \ $+2.5\%$", NO),
                 (4.0, 4.4, r"$+0.4$: \ $+10\%$", YES)]
        rows = VGroup()
        for k, (a, b, t, c) in enumerate(pairs):
            y = 1.7 - 1.15 * k
            ba = Rectangle(width=a * u, height=0.3, stroke_width=0, fill_color=GREY_A, fill_opacity=0.9)
            bb = Rectangle(width=b * u, height=0.3, stroke_width=0, fill_color=GREY_A, fill_opacity=0.9)
            ba.move_to([xl + a * u / 2, y + 0.2, 0])
            bb.move_to([xl + b * u / 2, y - 0.2, 0])
            tl = label(t, font_size=19, color=c).move_to([xl + 4.7 * u, y, 0], aligned_edge=LEFT)
            rows.add(VGroup(ba, bb, tl))
        tag = note(r"illustrative", font_size=16).next_to(rows, DOWN, buff=0.25).align_to(rows, LEFT)
        weber = MathTex(r"\frac{\Delta I}{I} = k", font_size=44, color=HEAD)
        fech = MathTex(r"S = c\,\log\frac{I}{I_0}", font_size=44, color=LAM)
        W = 5.0
        side = VGroup(
            VGroup(weber, label(r"Weber \ (1834)", font_size=19, color=HEAD)).arrange(RIGHT, buff=0.3),
            wrapped_label(r"the \textbf{just-noticeable difference} $\Delta I$ is a fixed fraction $k$ of the "
                          r"stimulus $I$: \ the Weber fraction", W, font_size=19, color=WHITE),
            VGroup(fech, label(r"Fechner \ (1860)", font_size=19, color=LAM)).arrange(RIGHT, buff=0.3),
            wrapped_label(r"count the noticeable steps and sensation grows with the logarithm of the stimulus: \ "
                          r"loudness in decibels, \ and screens spending more codes on dark tones \ (chapter 4)",
                          W, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.95, 0.0, 0])
        with self.voiceover(
            "The second kind of threshold is in size. <bookmark mark='a'/> Two short bars differ by a tenth of a "
            "unit, and the difference is easy to see. <bookmark mark='b'/> Add the same tenth to a long bar and it "
            "nearly vanishes. <bookmark mark='c'/> To be as visible, the difference must grow with the bar. "
            "<bookmark mark='d'/> Ernst Weber found this in the 1830s: the just-noticeable difference is a fixed "
            "fraction of the stimulus, a fraction that differs from one sense to another. <bookmark mark='e'/> "
            "Gustav Fechner, in 1860, counted those steps, and concluded that sensation grows with the logarithm of "
            "the stimulus. It is why loudness is measured in decibels, and, as the next chapter shows, why screens "
            "spend more codes on dark tones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), FadeIn(r[1]))
                self.play(FadeIn(r[2]), run_time=0.5)
            vo.wait_until("d")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()

    def popout(self):
        head = label(r"What pops out", font_size=36).to_edge(UP, buff=0.3)
        rng = random.Random(4)
        n, gap = 6, 0.55

        def grid(cx, kind):
            g, target = VGroup(), None
            ti = rng.randrange(n * n)
            for i in range(n * n):
                p = [cx + (i % n - (n - 1) / 2) * gap, 0.9 - (i // n - (n - 1) / 2) * gap, 0]
                if kind == "colour":
                    m = Dot(p, radius=0.11, color=NO if i == ti else DATA)
                elif kind == "orient":
                    m = Line(UP * 0.17, DOWN * 0.17, color=GREY_A, stroke_width=4).move_to(p)
                    if i == ti:
                        m.rotate(PI / 4)
                else:
                    red = (i == ti) or rng.random() < 0.5
                    tilt = (i == ti) or not red
                    m = Line(UP * 0.17, DOWN * 0.17, color=NO if red else DATA, stroke_width=4).move_to(p)
                    if tilt:
                        m.rotate(PI / 4)
                if i == ti:
                    target = m
                g.add(m)
            ring = Circle(0.26, color=HEAD, stroke_width=3).move_to(target)
            return g, ring
        g1, c1 = grid(-4.4, "colour")
        g2, c2 = grid(0.0, "orient")
        g3, c3 = grid(4.4, "conj")
        caps = VGroup(
            wrapped_label(r"colour: \ pops out", 3.6, font_size=19, color=YES).next_to(g1, DOWN, buff=0.3),
            wrapped_label(r"orientation: \ pops out", 3.6, font_size=19, color=YES).next_to(g2, DOWN, buff=0.3),
            wrapped_label(r"red \textit{and} tilted: \ search item by item", 3.6, font_size=19,
                          color=NO).next_to(g3, DOWN, buff=0.3))
        foot = wrapped_label(r"Treisman and Gelade \ (1980): \ simple features are seen in parallel, \ "
                             r"\textit{preattentively}; \ a conjunction needs attention, \ one place at a time. \ "
                             r"Mark the one thing that matters with one feature", 12.4, font_size=19,
                             color=WHITE).to_edge(DOWN, buff=0.4)
        tag = note(r"illustrative", font_size=16).to_corner(UR, buff=0.4).shift(DOWN * 0.55)
        with self.voiceover(
            "Some differences need no search at all. <bookmark mark='a'/> One red mark among blue ones is seen "
            "at once, however many blue ones there are. <bookmark mark='b'/> So is one tilted line among upright "
            "ones. Colour, size, orientation and motion are processed in parallel across the whole field of view, "
            "before attention arrives. <bookmark mark='c'/> But find the red tilted line here, among red upright "
            "lines and blue tilted ones. Each feature alone is everywhere, and the eye has to check the marks one "
            "by one. <bookmark mark='d'/> Anne Treisman and Garry Gelade made this the feature integration theory "
            "in 1980. For an interface: mark the one thing that matters with a single feature."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(g1))
            self.play(Create(c1), FadeIn(caps[0]), run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(g2))
            self.play(Create(c2), FadeIn(caps[1]), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(g3))
            self.wait(2.5)
            self.play(Create(c3), FadeIn(caps[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def change(self):
        head = label(r"Change blindness", font_size=36).to_edge(UP, buff=0.3)
        vals = [(r"users", r"1{,}204"), (r"errors", r"17"), (r"latency", r"212 ms"), (r"queue", r"38"),
                (r"disk", r"61\%"), (r"build", r"passing")]

        def tile(k, v, color=WHITE):
            b = RoundedRectangle(width=2.6, height=1.2, corner_radius=0.1, stroke_color=GREY_C, stroke_width=1.5,
                                 fill_color=BG, fill_opacity=1)
            t = VGroup(label(k, font_size=18, color=GREY_B), label(v, font_size=30, color=color)).arrange(
                DOWN, buff=0.12).move_to(b)
            return VGroup(b, t)
        before = VGroup(*[tile(k, v) for k, v in vals]).arrange_in_grid(rows=2, cols=3, buff=0.3).move_to(
            [-2.4, 0.6, 0])
        after = before.copy()
        new = tile(r"errors", r"71").move_to(before[1])
        after[1].become(new)
        cover = Rectangle(width=before.width + 0.4, height=before.height + 0.4, stroke_width=0, fill_color=GREY_E,
                          fill_opacity=1).move_to(before)
        tag = note(r"illustrative", font_size=16).next_to(before, DOWN, buff=0.15).align_to(before, LEFT)
        W = 3.6
        side = VGroup(
            wrapped_label(r"a change hidden by a flicker, \ a blink or a page reload often goes unseen \ (Rensink, "
                          r"\ O'Regan and Clark, \ 1997)", W, font_size=19, color=WHITE),
            wrapped_label(r"so draw the eye: \ animate the change, \ or highlight it briefly", W, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.8, 0.6, 0])
        shown = before
        with self.voiceover(
            "<bookmark mark='a'/> Watch these six numbers while the screen "
            "flickers. One of them changes each time. In 1997 Ronald Rensink, Kevin O'Regan and James Clark showed "
            "that when a brief blank separates two pictures, even large changes go unseen for many seconds. "
            "<bookmark mark='b'/> Here, the errors went from seventeen to seventy-one. A page that reloads, or a "
            "value that updates during a scroll, is exactly such a blank. <bookmark mark='c'/> So an interface "
            "should draw the eye to what changed: animate it, or highlight it briefly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(before), FadeIn(tag))
            vo.wait_until("a")
            for k in range(5):
                nxt = after if k % 2 == 0 else before
                self.add(cover)
                self.wait(0.15)
                self.remove(shown)
                self.add(nxt)
                self.remove(cover)
                shown = nxt
                self.wait(0.9)
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            if shown is not after:
                self.remove(shown)
                self.add(after)
                shown = after
            self.play(after[1][1][1].animate.set_color(NO), after[1][0].animate.set_stroke(NO, width=3))
            self.play(Indicate(after[1], color=NO, scale_factor=1.1))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, HEAD)
