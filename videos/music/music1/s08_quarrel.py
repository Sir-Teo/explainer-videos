from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music.monochord.physics import pluck_shape
from videos.music.music1.common import (BAD, FREQ, GOOD, HIST, LEFT_C, PART, RATIO, RIGHT_C, STR, TIME, TUNE, clip,
                                        film, load, say, window)

X = np.linspace(0, 1, 121)


def mini(shape, color=STR, width=2.4, scale=0.42) -> StringView:
    v = StringView(width=width, scale=scale, color=color, stroke_width=3, supports=False)
    v.set_shape(shape)
    return v


class Quarrel(SoundScene):
    def construct(self):
        self.card()
        self.cast()
        self.add_it_up()
        self.fourier()
        self.same_motion()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(7, r"The quarrel", r"Travelling shapes or standing modes: \ which is the string?",
                            lit=(1747, 1753, 1759, 1807), part=PART)
        with self.voiceover("Chapter seven. The quarrel."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def cast(self):
        tri = pluck_shape(X, 1.0, 0.3, 1.0)
        people = [
            (1747, r"d'Alembert", r"Paris", r"the string is two travelling shapes, \\ and a shape is a formula",
             mini(np.exp(-0.5 * ((X - 0.45) / 0.1) ** 2), RIGHT_C)),
            (1748, r"Euler", r"Berlin", r"any curve a hand can draw will do, \\ corners and all",
             mini(tri, STR)),
            (1753, r"Daniel Bernoulli", r"Basel", r"every motion is a sum of the simple modes: \\ a musician can "
             r"hear them", VGroup(*[mini(np.sin(n * np.pi * X) / n, harmonic_color(n), scale=0.3)
                                    for n in (1, 2, 3)]).arrange(DOWN, buff=0.12)),
            (1759, r"Lagrange", r"Turin, aged 23", r"start from beads, \ let them shrink: \\ one step from the answer",
             VGroup(mini(tri, GREY_B), VGroup(*[Dot(radius=0.045, color=STR) for _ in range(9)]))),
        ]
        rows = VGroup()
        for yr, who, where, claim, pic in people:
            y = label(str(yr), font_size=38, color=HIST)
            w = VGroup(label(who, font_size=30), label(where, font_size=22, color=GREY_B)).arrange(DOWN, buff=0.06,
                                                                                                aligned_edge=LEFT)
            cl = label(claim, font_size=26, color=GREY_A)
            rows.add(VGroup(y, w, cl, pic))
        xs = [-6.2, -4.9, -1.9, 4.6]
        for i, r in enumerate(rows):
            for cell, x in zip(r[:3], xs[:3]):
                cell.move_to([x, 2.5 - 1.55 * i, 0], aligned_edge=LEFT)
            r[3].move_to([xs[3], 2.5 - 1.55 * i, 0])
        lag = rows[3][3]
        for k, dot in enumerate(lag[1]):
            f = (k + 1) / 10
            dot.move_to(lag[0].p(f, float(np.interp(f, X, tri))))
        with self.voiceover(
            "D'Alembert published his travelling waves in 1747, and he was strict about what counted as a shape: "
            "it had to be given by one formula. <bookmark mark='a'/> The next year Leonhard Euler disagreed. A string "
            "can be pulled into any curve a hand can draw, corners included. A plucked string is two straight "
            "lines, and no single formula gives you that. <bookmark mark='b'/> Then, in 1753, Daniel Bernoulli made "
            "a bolder claim. Every motion of a string is a sum of the standing sine waves. He had no proof. He had "
            "his ears: a musician hears those tones sounding together."
        ) as vo:
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2))
        objection = label(r"``A sum of sines is smooth. \ How could it ever make a corner?''", font_size=30, color=BAD)
        objection.to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Euler would not have it, and his objection sounds unanswerable. <bookmark mark='a'/> Every sine wave is "
            "perfectly smooth. Add smooth curves together and you get a smooth curve. So how could a sum of sines "
            "ever be a triangle, with a corner? <bookmark mark='b'/> A young man in Turin, Joseph-Louis Lagrange, "
            "started from beads on a thread, let the beads shrink, and came within one step of the answer without "
            "taking it. The argument ran for fifty years."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(objection), Indicate(rows[1][3], color=BAD))
            vo.wait_until("b")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def add_it_up(self):
        d = load("fourier")
        c = clip("fourier.build")
        x = d["x"]
        s = StringView(width=10.4, scale=2.2).move_to(UP * 0.7)
        target = StringView(width=10.4, scale=2.2, color=GREY_C, stroke_width=2, supports=False).move_to(UP * 0.7)
        target.set_shape(d["target"])
        s.set_shape(np.zeros(len(x)))
        bars = partial_bars(np.abs(d["a"]), width=9.6, height=1.3, db=False, numbers=False)
        bars.move_to(DOWN * 2.55)
        for b in bars.bars:
            b.set_opacity(0.15)
        blab = label(r"how much of each mode", font_size=22, color=GREY_B).next_to(bars, UP, buff=0.12).align_to(bars, RIGHT)
        count = label(r"0 modes", font_size=40, color=TUNE).to_corner(UL, buff=0.5)
        errl = label(r"", font_size=28, color=GREY_A)
        with self.voiceover(
            "We can do what they could not. We can add it up, and listen while we do. Here is the plucked shape, "
            "in grey. <bookmark mark='a'/> We will build it from modes: one, then two, three, five, ten, thirty. "
            "Each time, you will hear the string as it would sound with only those modes in it."
        ) as vo:
            self.play(FadeIn(target), FadeIn(s))
            vo.wait_until("a")
            self.play(FadeIn(bars), FadeIn(blab), FadeIn(count))
        with self.listen(c) as snd:
            window(snd, r"1, 2, 3, 5, 10, 30 modes, \ then all")
            for N, row in zip(d["heard"], d["heard_sums"]):
                snd.wait_until(f"n{N}")
                s.set_shape(row)
                new = label(rf"{N} mode" + ("s" if N > 1 else ""), font_size=40, color=TUNE).to_corner(UL, buff=0.5)
                self.remove(count)
                count = new
                self.add(count)
                for b in bars.bars[:N]:
                    b.set_opacity(0.95)
                e = label(rf"largest gap: \ {100 * float(d['error'][N - 1]):.0f}\% of the height", font_size=28,
                          color=GREY_A).to_corner(UR, buff=0.5).shift(DOWN * 0.7)
                self.remove(errl)
                errl = e
                self.add(errl)
            snd.wait_until("all")
            s.set_shape(d["target"])
            new = label(r"all of them", font_size=40, color=TUNE).to_corner(UL, buff=0.5)
            self.remove(count, errl)
            count = new
            self.add(count)
        e100 = float(d["error"][99])
        verdict = VGroup(label(r"Bernoulli was right: \ the pluck is a sum of modes", font_size=30, color=GOOD),
                         label(r"Euler was right: \ the shape has a corner, \ and no one formula", font_size=30, color=GOOD)
                         ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.5)
        with self.voiceover(
            "With one mode it is a hum and a smooth arch. With thirty, the corner is nearly there and the sound has "
            f"its bite. With a hundred terms the sum is within {say(100 * e100, 1)} percent of the pluck everywhere, "
            f"and the gap goes on shrinking like one over the number of terms. <bookmark mark='a'/> No finite sum "
            "has a corner. The infinite sum does. So Bernoulli was right, <bookmark mark='b'/> and so was Euler. The "
            "plucked shape is not smooth, it is not one formula, and it is a sum of sines."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(bars), FadeOut(blab), FadeIn(verdict[0]))
            vo.wait_until("b")
            self.play(FadeIn(verdict[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fourier(self):
        card = history_card(1807, r"Joseph Fourier", r"studying heat, \ not strings, \ he claims that \emph{any} "
                            r"shape is a sum of sines, \ and gives the recipe for the amounts. \ The Paris Academy "
                            r"declines to print it.", width=6.0).move_to(LEFT * 3.4 + UP * 2.4)
        card2 = history_card(1829, r"Dirichlet", r"the first proof of when the sum converges. \ To write it he has "
                             r"to say what a function is.", width=5.2).move_to(RIGHT * 3.4 + UP * 2.4)
        # "any shape": a curve no one would call a formula, and its sum of sines growing term by term
        from explainer.music.monochord.physics import sine_coefficients
        xs = np.linspace(0, 1, 801)
        knots_x = [0.0, 0.14, 0.28, 0.42, 0.58, 0.60, 0.82, 1.0]
        knots_y = [0.0, 0.85, 0.2, 0.95, 0.9, -0.45, -0.65, 0.0]
        hand = np.interp(xs, knots_x, knots_y)
        co = sine_coefficients(hand, 60)
        basis = np.sin(np.pi * np.outer(np.arange(1, 61), xs))
        drawn = StringView(width=9.6, scale=1.0, color=GREY_C, stroke_width=2, supports=False).move_to(DOWN * 0.55)
        drawn.set_shape(hand)
        summed = StringView(width=9.6, scale=1.0).move_to(DOWN * 0.55)
        terms = ValueTracker(1)
        summed.add_updater(lambda m: m.set_shape(co[: max(1, int(terms.get_value()))] @ basis[: max(1, int(terms.get_value()))]))
        counter = Integer(1, font_size=36, color=TUNE).next_to(summed, RIGHT, buff=0.3)
        counter.add_updater(lambda m: m.set_value(max(1, int(terms.get_value()))))
        ctag = label(r"sines", font_size=24, color=TUNE).next_to(counter, DOWN, buff=0.1)
        back = VGroup(label(r"where this comes back", font_size=26, color=GREY_B),
                      label(r"Part 3, \ \textit{The Spectrum}: \ Fourier's recipe, \ for any sound", font_size=28, color=TUNE),
                      label(r"\textit{Analysis, Built}: \ what it means for such a sum to converge", font_size=28,
                            color=GREY_A)).arrange(DOWN, buff=0.15).move_to(DOWN * 2.85)
        with self.voiceover(
            "It was settled in 1807 by a man who was not thinking about music. Joseph Fourier was studying how "
            "heat spreads, and he claimed that any shape whatever is a sum of sines, and gave the recipe for how "
            "much of each. <bookmark mark='a'/> The old guard, Lagrange among them, would not print it. Making it "
            "rigorous took twenty more years, and mathematicians had to decide what a function is. "
            "<bookmark mark='b'/> A quarrel about a string ended up rebuilding the foundations of mathematics. We "
            "use Fourier's recipe in the next chapter, and Part 3 is built on it."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2), FadeIn(drawn), FadeIn(summed), FadeIn(counter), FadeIn(ctag))
            self.play(terms.animate.set_value(24), run_time=vo.until("a"), rate_func=linear)
            self.play(FadeIn(card2, shift=UP * 0.2))
            self.play(terms.animate.set_value(60), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(back))
        summed.clear_updaters()
        counter.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def same_motion(self):
        d = load("dalembert")
        f = load("fourier")
        frames = d["b20"]
        n = d["frames"]
        xs = d["x"]
        s = StringView(width=10.4, scale=1.7).move_to(UP * 1.2)
        tr = film(s, frames, step=1, loop=True)
        a = f["a"][:30]
        modes = np.sin(np.pi * np.outer(np.arange(1, 31), xs))
        idx = np.arange(6, len(xs) - 1, 6)
        dots = VGroup(*[Dot(radius=0.05, color=TUNE) for _ in idx])

        def place(m):
            tau = (tr.get_value() % (n - 1)) / n
            row = (a * np.cos(2 * np.pi * np.arange(1, 31) * tau)) @ modes
            for dot, k in zip(m, idx):
                dot.move_to(s.p(xs[k], row[k]))

        place(dots)
        dots.add_updater(place)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, color=STR, stroke_width=4),
                            label(r"two travelling shapes", font_size=26, color=STR)).arrange(RIGHT, buff=0.2),
                     VGroup(Dot(radius=0.06, color=TUNE),
                            label(r"thirty standing modes, \ each swinging at its own frequency", font_size=26,
                                  color=TUNE)).arrange(RIGHT, buff=0.2)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.5)
        end = label(r"one motion, \ two descriptions", font_size=36, color=GOOD).move_to(DOWN * 2.0)
        with self.voiceover(
            "So which is the string: travelling shapes, or standing modes? Both. <bookmark mark='a'/> The line is "
            "the plucked string as d'Alembert's two travelling shapes. The dots are thirty modes, each one doing "
            "nothing but swinging in place at its own frequency, added together. <bookmark mark='b'/> It is one "
            "motion, described twice. The travelling picture tells you why there is a pitch. The standing picture "
            "tells you what is in the sound. And that raises the practical question: for a given pluck, how much of "
            "each mode do you get?"
        ) as vo:
            self.play(FadeIn(s), FadeIn(leg[0]), run_time=0.5)
            self.play(tr.animate.set_value(0.35 * n), run_time=vo.until("a"), rate_func=linear)
            self.play(FadeIn(dots), FadeIn(leg[1]), run_time=0.5)
            self.play(tr.animate.set_value(1.0 * n), run_time=vo.until("b"), rate_func=linear)
            self.play(FadeIn(end), tr.animate.set_value(2.6 * n), run_time=max(vo.remaining(), 4.0), rate_func=linear)
        s.clear_updaters()
        dots.clear_updaters()
        self.wait(0.3)
        self.clear_scene()
