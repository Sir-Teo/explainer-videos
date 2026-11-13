from __future__ import annotations

import numpy as np

from videos.music.music6.common import *  # noqa: F403


class Piano(SoundScene):
    def construct(self):
        chapter(self, 8, r"The piano's stretched octaves", r"Is even the octave safe?", lit=(1883,), extra=((1938, r"Railsback's curve"),))
        self.stiff()
        self.curve()

    # ------------------------------------------------------------------
    def stiff(self):
        d = load("piano")
        c = clip("piano.octave")
        lo = d["lo"]
        base, unit = LEFT * 5.8 + UP * 0.9, 11.0 / (4.3 * lo)
        axis = Line(base, base + RIGHT * 11.3, color=GREY_C, stroke_width=2)
        ideal = VGroup(*[DashedLine(base + RIGHT * unit * lo * k, base + RIGHT * unit * lo * k + UP * 1.3, color=GREY_B, stroke_width=2, dash_length=0.07) for k in range(1, 5)])
        real = VGroup(*[Line(base + RIGHT * unit * f, base + RIGHT * unit * f + UP * 1.3, color=STR, stroke_width=5) for f in d["partials"]])
        il = VGroup(*[MathTex(str(k), font_size=24, color=GREY_B).next_to(base + RIGHT * unit * lo * k, DOWN, buff=0.12) for k in range(1, 5)])
        head = label(r"a stiff string: \ its partials run sharp, \ more and more", font_size=30, color=GREY_A).to_edge(UP, buff=0.4)
        note = listen_note(r"An octave on two very stiff strings. \ First exactly 2 to 1. \\ Then widened until the upper note sits on the lower note's second partial.", width=10.0, font_size=26).move_to(DOWN * 0.9)
        bx = boxes((r"exactly 2 : 1", rf"{d['stretch_cents']:.0f} cents wide"), buff=0.8, width=3.4, height=0.9, font_size=28).move_to(DOWN * 2.35)
        with self.voiceover(
            "Through all of this, one interval has been safe: the octave, two to one, pure in every system. On a "
            "piano, even that fails, and Part 5 has already told us why. <bookmark mark='a'/> A piano string is "
            "thick steel under great tension, and in Part 1 we found that a stiff string's partials are not "
            "whole multiples of its fundamental. They run sharp, more and more the higher they go. "
            "<bookmark mark='b'/> So the second partial of a piano note is a little above twice its frequency. "
            "And we know that an octave is smooth when the upper note lands on the lower note's second partial, "
            "wherever that happens to be. Listen: an octave on two very stiff strings, first tuned exactly two "
            "to one, and then stretched."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axis), FadeIn(ideal), FadeIn(il))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in real], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(real[1], color=WHITE, scale_factor=1.15), FadeIn(note), FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"an exact octave, \ then a stretched one", kind="synthesized", detail=r"stiff-string partials", corner=DL, tag_corner=DR)
            for ev, b in zip(("exact", "stretched"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 2.4)
        with self.voiceover(
            f"The exact octave beats, about {say(d['beat_exact'])} times a second on these exaggerated strings. "
            "The stretched one is still. On an instrument whose partials are stretched, the in-tune octave is a "
            "stretched octave. It is the lesson of the bent timbre, in an instrument found in every concert hall."
        ):
            self.play(Indicate(bx[1][0], color=GOOD))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curve(self):
        d = load("piano")
        keys, curve_ = d["keys"], d["curve"]
        g = axes([1, 88], [-30, 35], x_length=10.4, y_length=3.8, xlabel=r"key of the piano", ylabel=r"cents above or below equal temperament", xticks=[1, 13, 25, 37, 49, 61, 73, 88],
                 yticks=[-20, -10, 0, 10, 20, 30], xfmt=lambda v: {1: "A0", 13: "A1", 25: "A2", 37: "A3", 49: "A4", 61: "A5", 73: "A6", 88: "C8"}[int(v)], font_size=20)
        g.move_to(DOWN * 0.3 + LEFT * 0.5)
        zero = Line(g.ax.c2p(1, 0), g.ax.c2p(88, 0), color=GREY_D, stroke_width=1.5)
        cu = curve(g.ax, keys, curve_, STR)
        card = history_card(1938, r"O. L. Railsback", r"measures how pianos are actually tuned: flat in the bass, sharp in the treble, by tens of cents.", width=4.6, font_size=20).move_to(g.ax.c2p(29, 21))
        ends = VGroup(label(rf"{d['bottom']:.0f} cents", font_size=26, color=NARROW).next_to(g.ax.c2p(1, d["bottom"]), UP, buff=0.6).shift(RIGHT * 1.0),
                      label(rf"{d['top']:+.0f} cents", font_size=26, color=WIDE).next_to(g.ax.c2p(88, d["top"]), LEFT, buff=0.3))
        tag = label(r"Monochord's model: \ every octave beatless, \ on strings of typical stiffness; \ the A above middle C left where it is", font_size=20, color=GREY_C).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Do that across a whole keyboard and you get a curve. <bookmark mark='a'/> A tuner sets the middle "
            "of the keyboard to equal temperament, and then tunes octaves outward from it, each one beatless. "
            "Because every string is a little stiff, every octave comes out a little wide, and the widening "
            "adds up. <bookmark mark='b'/> This is Monochord's model, with strings of typical stiffness. By the "
            f"top of the keyboard the notes are about {say(d['top'])} cents sharp of where equal temperament puts "
            f"them, and at the bottom about {say(abs(d['bottom']))} cents flat. <bookmark mark='c'/> In 1938 "
            "O. L. Railsback measured real pianos, tuned by good tuners, and found this shape. So the "
            "instrument that stands for equal temperament is not in equal temperament. No formula on paper says "
            "how a piano should be tuned. Its own strings do. And every piano is different. A short string has "
            "to be thicker for its pitch, so it is stiffer, and its partials are further out of line. That is "
            "one reason a small upright never sounds like a concert grand, however well it is tuned: its "
            "octaves have to be stretched more, and its bass notes hardly agree with themselves."
        ) as vo:
            self.play(FadeIn(g), FadeIn(zero))
            vo.wait_until("a")
            self.play(Create(cu), run_time=4.0)
            vo.wait_until("b")
            self.play(FadeIn(tag), FadeIn(ends))
            vo.wait_until("c")
            self.play(FadeIn(card))
        self.wait(0.3)
        self.clear_scene()
