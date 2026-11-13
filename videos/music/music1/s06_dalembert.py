from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from videos.music.music1.common import (FREQ, GOOD, HIST, LEFT_C, PART, RATIO, RIGHT_C, STR, TIME, TUNE, clip, film,
                                        film_many, load, say, window)


class DAlembert(SoundScene):
    def construct(self):
        self.card()
        self.guess()
        self.from_rest()
        self.check()
        self.period()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(5, r"Two travelling waves", r"What does the equation say the string will do?",
                            lit=(1747,), part=PART)
        with self.voiceover("Chapter five. Two travelling waves."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def guess(self):
        d = load("pulse")
        rope = StringView(width=9.0, scale=0.9).move_to(UP * 2.75)
        tr = film(rope, d["right"])
        per = (len(d["right"]) - 1) / 2.0
        rows = [
            MathTex(r"u", r"=", r"f(x - ct)", font_size=46),
            MathTex(r"\frac{\partial^2 u}{\partial x^2}", r"=", r"f''(x - ct)", font_size=46),
            MathTex(r"\frac{\partial^2 u}{\partial t^2}", r"=", r"c^2", r"f''(x - ct)", font_size=46),
            MathTex(r"\frac{\partial^2 u}{\partial t^2}", r"=", r"c^2", r"\frac{\partial^2 u}{\partial x^2}", font_size=46),
        ]
        whys = [why(r"a shape $f$, \ sliding right at speed $c$"), why(r"two derivatives in $x$"),
                why(r"each derivative in $t$ brings out a factor $-c$"), why(r"the wave equation, \ for any shape $f$")]
        rows[0][2].set_color(RIGHT_C), rows[1][2].set_color(RIGHT_C), rows[2][3].set_color(RIGHT_C)
        step = ladder(self, rows, whys, keep=4, top=1.55, buff=0.4, x=-2.2)
        with self.voiceover(
            "We saw bumps slide along a rope at a steady speed without changing shape. So try that as a solution. "
            "<bookmark mark='a'/> Take any shape, call it f, and slide it to the right at speed c: f of x minus c t. "
            "<bookmark mark='b'/> Differentiate twice in x, and you get f double prime. <bookmark mark='c'/> "
            "Differentiate twice in time, and each derivative brings out a factor of minus c, so you get c squared "
            "times the same thing. <bookmark mark='d'/> The wave equation is satisfied, whatever the shape."
        ) as vo:
            self.play(FadeIn(rope), run_time=0.5)
            self.play(tr.animate.set_value(0.45 * per), run_time=vo.until("a"), rate_func=linear)
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        rope.clear_updaters()
        thm = theorem_card(r"d'Alembert's solution", MathTex(r"u(x, t) \;=\; f(x - ct) \;+\; g(x + ct)", font_size=44),
                           who=r"Jean le Rond d'Alembert, \ 1747", color=GOOD, width=8.6, kind=r"Theorem")
        thm.move_to(DOWN * 0.9)
        gloss_ = VGroup(label(r"any shape moving right", font_size=26, color=RIGHT_C),
                        label(r"plus any shape moving left", font_size=26, color=LEFT_C),
                        label(r"and nothing else", font_size=26, color=GREY_A)).arrange(RIGHT, buff=0.6)
        gloss_.next_to(thm, DOWN, buff=0.4)
        with self.voiceover(
            "A shape sliding left works just as well, and because waves add, so does the sum of the two. "
            "<bookmark mark='a'/> D'Alembert proved that this is everything. Every possible motion of the string is "
            "one shape moving right plus one shape moving left. <bookmark mark='b'/> So the constant c in the "
            "equation really is a speed: the square root of tension over mass, as promised."
        ) as vo:
            self.play(*[FadeOut(m) for m in rows[:3] + whys], rows[3].animate.scale(0.7).to_corner(UL, buff=0.5),
                      FadeOut(rope))
            both = StringView(width=9.0, scale=1.0).move_to(UP * 1.9)
            tb = film(both, d["cross"])
            self.play(FadeIn(both), run_time=0.4)
            self.play(tb.animate.set_value(0.5 * per), run_time=vo.until("a"), rate_func=linear)
            both.clear_updaters()
            self.play(FadeIn(thm, shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(g) for g in gloss_], lag_ratio=0.5), run_time=2.0)
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def from_rest(self):
        d = load("dalembert")
        n = d["frames"]
        top = StringView(width=9.6, scale=1.5).move_to(UP * 1.9)
        mid = StringView(width=9.6, scale=1.5, color=RIGHT_C, stroke_width=3, supports=False).move_to(DOWN * 0.6)
        bot = StringView(width=9.6, scale=1.5, color=LEFT_C, stroke_width=3, supports=False).move_to(DOWN * 2.5)
        tr = film_many([(top, d["b20"]), (mid, d["b20_right"]), (bot, d["b20_left"])], loop=True)
        tags = VGroup(label(r"the string", font_size=26, color=STR).next_to(top, LEFT, buff=0.2).shift(UP * 0.5),
                      label(r"half, \ going right", font_size=26, color=RIGHT_C).next_to(mid, LEFT, buff=0.2).shift(UP * 0.4),
                      label(r"half, \ going left", font_size=26, color=LEFT_C).next_to(bot, LEFT, buff=0.2).shift(UP * 0.4))
        for t in tags:
            t.to_edge(LEFT, buff=0.3)
        tags[2].shift(DOWN * 0.15)
        plus = MathTex(r"=", font_size=40, color=GREY_B).move_to(UP * 0.85 + LEFT * 6.1)
        plus2 = MathTex(r"+", font_size=40, color=GREY_B).move_to(DOWN * 1.2 + LEFT * 6.1)
        with self.voiceover(
            "Which two shapes? That depends on how the string starts. Pluck it: pull it aside and hold it still. "
            "<bookmark mark='a'/> A string let go from rest starts as two copies of its own shape, each half as "
            "tall, lying on top of each other. <bookmark mark='b'/> Let go, and one copy slides right and the other "
            "slides left. What you see is their sum."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(FadeIn(mid), FadeIn(bot), FadeIn(tags[1:]), FadeIn(plus), FadeIn(plus2))
            vo.wait_until("b")
            self.play(tr.animate.set_value(0.14 * n), run_time=max(vo.remaining(), 3.0), rate_func=linear)
        flat = label(r"between the two corners: \ flat", font_size=26, color=TUNE).next_to(top, UP, buff=0.35)
        with self.voiceover(
            "Look at the string itself. The corner you made with your finger has split into two corners, running "
            "apart, <bookmark mark='a'/> and between them the string is flat. When a corner reaches an end, it "
            "reflects, upside down, exactly like the bump on the rope. <bookmark mark='b'/> So a plucked string never "
            "looks like the smooth wobble people draw. It is three straight lines at most, with two corners chasing "
            "each other round and round."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(flat))
            self.play(tr.animate.set_value(0.5 * n), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeOut(flat), tr.animate.set_value(1.5 * n), run_time=max(vo.remaining(), 4.0),
                      rate_func=linear)
        for v in (top, mid, bot):
            v.clear_updaters()
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        d = load("dalembert")
        n = d["frames"]
        frames = d["b20"]
        s = StringView(width=10.4, scale=1.7).move_to(UP * 1.0)
        tr = film(s, frames, step=1, loop=True)
        idx = np.arange(8, frames.shape[1] - 1, 8)
        dots = VGroup(*[Dot(radius=0.055, color=TUNE) for _ in idx])

        def place(m):
            f = tr.get_value() % (n - 1)
            i = int(f)
            a = f - i
            row = (1 - a) * frames[i] + a * frames[i + 1]
            for dot, k in zip(m, idx):
                dot.move_to(s.p(k / (frames.shape[1] - 1), row[k]))

        place(dots)
        dots.add_updater(place)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, color=STR, stroke_width=4),
                            label(r"d'Alembert's formula", font_size=26, color=STR)).arrange(RIGHT, buff=0.2),
                     VGroup(Dot(radius=0.06, color=TUNE),
                            label(rf"the simulation: \ {d['beads']} beads and Newton's law", font_size=26, color=TUNE))
                     .arrange(RIGHT, buff=0.2)).arrange(RIGHT, buff=0.9).to_edge(UP, buff=0.5)
        e = d["b20_error"]
        expo = int(np.floor(np.log10(e)))
        err = VGroup(label(r"largest difference over a whole cycle", font_size=28, color=GREY_A),
                     MathTex(rf"{e / 10 ** expo:.1f} \times 10^{{{expo}}}", font_size=50, color=GOOD),
                     label(r"of the height of the pluck: \ the computer's rounding, and nothing else", font_size=26,
                           color=GREY_A)).arrange(DOWN, buff=0.2).move_to(DOWN * 2.3)
        with self.voiceover(
            "Is that really what our simulation does? The line is d'Alembert's formula. <bookmark mark='a'/> The dots "
            f"are {say(d['beads'])} beads, each obeying Newton's law and knowing nothing about any formula. "
            "<bookmark mark='b'/> Over a whole cycle the two never differ by more than about one part in "
            f"ten to the {abs(expo)}. That is the rounding error of the computer's arithmetic. The bead model and "
            "d'Alembert's solution are, at this step size, the same thing."
        ) as vo:
            self.play(FadeIn(s), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(FadeIn(dots), FadeIn(leg[1]))
            self.play(tr.animate.set_value(0.5 * n), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(err), tr.animate.set_value(1.2 * n), run_time=max(vo.remaining(), 4.0), rate_func=linear)
        s.clear_updaters()
        dots.clear_updaters()
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def period(self):
        d = load("dalembert")
        n = d["frames"]
        s = StringView(width=10.4, scale=1.6).move_to(UP * 1.7)
        tr = film(s, d["b20"], step=1, loop=True)
        eq = MathTex(r"\text{the shapes repeat every } 2L", r"\;\Longrightarrow\;", r"\text{the motion repeats every } \frac{2L}{c}",
                     font_size=38).move_to(DOWN * 0.5)
        law = MathTex(r"f", r"=", r"\frac{c}{2L}", r"=", r"\frac{1}{2L}\sqrt{\frac{T}{\mu}}", font_size=54).move_to(DOWN * 2.0)
        law[0].set_color(FREQ), law[4].set_color(GOOD)
        law.shift(UP * 0.3)
        tick = label(r"Mersenne's law, \ derived from Newton's", font_size=28, color=GOOD).next_to(law, DOWN, buff=0.3)
        with self.voiceover(
            "And now the pitch falls out. With both ends fixed, each travelling shape is the starting shape, "
            "reflected back and forth for ever: it repeats every two string lengths. <bookmark mark='a'/> A shape "
            "moving at speed c covers two lengths in a time of two L over c. So the whole motion repeats that often, "
            "<bookmark mark='b'/> and the frequency is c over two L. That is Mersenne's law, the one half included, "
            "derived from Newton's law and nothing else."
        ) as vo:
            self.play(FadeIn(s), run_time=0.5)
            self.play(tr.animate.set_value(0.6 * n), run_time=vo.until("a"), rate_func=linear)
            self.play(FadeIn(eq), tr.animate.set_value(1.0 * n), run_time=vo.until("b"), rate_func=linear)
            self.play(Write(law), run_time=1.5)
            self.play(FadeIn(tick), tr.animate.set_value(1.6 * n), run_time=max(vo.remaining(), 2.0), rate_func=linear)
        note_ = label(r"the period did not depend on the shape", font_size=32, color=TUNE).move_to(DOWN * 0.5)
        with self.voiceover(
            "Notice what we never used: the shape. <bookmark mark='a'/> Pluck the string in the middle or near the "
            "end, softly or hard, with a finger or a feather. The shape differs, and it comes back after exactly the "
            "same time. That is why a string has a pitch: one pitch, however you play it."
        ) as vo:
            self.play(FadeOut(eq), tr.animate.set_value(1.9 * n), run_time=vo.until("a"), rate_func=linear)
            self.play(FadeIn(note_), tr.animate.set_value(3.2 * n), run_time=max(vo.remaining(), 3.0),
                      rate_func=linear)
        s.clear_updaters()
        c = clip("pluck.b20")
        period = d["period"]
        slow = 1.6 / period
        cap = label(rf"the string, slowed {slow:.0f} times \quad $\cdot$ \quad its sound, at full speed", font_size=24,
                    color=GREY_A).next_to(s, DOWN, buff=0.9)
        self.play(FadeOut(note_), FadeOut(law), FadeOut(tick), FadeIn(cap), run_time=0.5)
        with self.listen(c) as snd:
            window(snd, r"plucked a fifth of the way along")
            snd.drive(s, s.film(d["b20"], d["dt"], slow=slow, loop=True))
        with self.voiceover(
            "Travelling waves explain the pitch. They do not explain something Mersenne noticed in 1636 and could "
            "not account for: that a single string seems to sound several notes at once. For that we need a second "
            "way to solve the same equation."
        ) as vo:
            tr2 = film(s, d["b20"], step=1, loop=True)
            self.play(tr2.animate.set_value(3.0 * n), run_time=max(vo.remaining(), 3.0), rate_func=linear)
        s.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
