from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music.monochord.physics import pluck_shape
from videos.music.music1.common import (BAD, FORCE, FREQ, GOOD, HIST, MASS, PART, RATIO, STR, TIME, TUNE, clip, load,
                                        ring, say, window)


def beaded(view: StringView, u: np.ndarray, radius=0.08, color=STR) -> VGroup:
    """Beads at the interior points of a StringView set to the shape ``u``."""
    view.set_shape(u)
    n = len(u)
    return VGroup(*[Dot(view.p(i / (n - 1), u[i]), radius=radius, color=color) for i in range(1, n - 1)])


class Equation(SoundScene):
    def construct(self):
        self.card()
        self.beads()
        self.newton()
        self.hear()
        self.limit()
        self.meaning()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(4, r"The wave equation", r"What does Newton's law say about one small piece of string?",
                            lit=(1747, 1759), part=PART)
        with self.voiceover("Chapter four. The wave equation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def beads(self):
        x = np.linspace(0, 1, 13)
        u = 0.9 * np.sin(np.pi * x) * (0.6 + 0.4 * np.sin(2.3 * np.pi * x + 0.4))
        s = StringView(width=11.6, scale=2.0, stroke_width=2.5).shift(DOWN * 0.3)
        s.curve.set_stroke(color=GREY_B)
        dots = beaded(s, u)
        hbr = BraceBetweenPoints(s.p(5 / 12, 0) + DOWN * 0.9, s.p(6 / 12, 0) + DOWN * 0.9, DOWN, color=RATIO)
        hl = MathTex(r"h", font_size=34, color=RATIO).next_to(hbr, DOWN, buff=0.06)
        with self.voiceover(
            "How do you write Newton's law for a string? A string is not one object in one place. So chop it up. "
            "<bookmark mark='a'/> Picture a row of small beads on a weightless thread, each a distance h from the "
            "next. Each bead can move only up and down, and its height is called u. <bookmark mark='b'/> And each "
            "bead feels exactly two forces: the thread on its left and the thread on its right, both pulling with "
            "the tension of the string, T."
        ) as vo:
            self.play(FadeIn(s))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.08), FadeIn(hbr), FadeIn(hl),
                      run_time=1.6)
            vo.wait_until("b")
            self.play(Indicate(dots[5], color=TUNE, scale_factor=1.8))
        # one bead and its two neighbours, large, on the left; the algebra goes on the right
        H, X0 = 2.5, -3.6
        left, right = np.array([X0 - H, -1.6, 0]), np.array([X0 + H, -1.1, 0])
        y = ValueTracker(0.4)

        def mid():
            return np.array([X0, y.get_value(), 0.0])

        row = VGroup(s, dots)

        beads3 = VGroup(Dot(left, radius=0.13, color=STR), Dot(right, radius=0.13, color=STR))
        me = always_redraw(lambda: Dot(mid(), radius=0.15, color=TUNE))
        threads = always_redraw(lambda: VGroup(Line(left, mid(), color=GREY_B, stroke_width=2.5),
                                               Line(mid(), right, color=GREY_B, stroke_width=2.5)))

        def pull(target):
            d = target - mid()
            return Arrow(mid(), mid() + 1.5 * d / np.linalg.norm(d), buff=0.16, color=FORCE, stroke_width=5,
                         max_tip_length_to_length_ratio=0.18)

        pulls = always_redraw(lambda: VGroup(pull(left), pull(right)))
        names = VGroup(MathTex(r"u_{i-1}", font_size=36, color=STR).next_to(left, DOWN, buff=0.25),
                       MathTex(r"u_{i+1}", font_size=36, color=STR).next_to(right, DOWN, buff=0.25))
        myname = always_redraw(lambda: MathTex(r"u_i", font_size=38, color=TUNE).next_to(mid(), UP, buff=0.3))
        tl = always_redraw(lambda: VGroup(
            MathTex(r"T", font_size=34, color=FORCE).move_to(mid() + 0.95 * (left - mid()) / np.linalg.norm(left - mid())
                                                             + UP * 0.35),
            MathTex(r"T", font_size=34, color=FORCE).move_to(mid() + 0.95 * (right - mid()) / np.linalg.norm(right - mid())
                                                             + UP * 0.35)))
        hb = VGroup(BraceBetweenPoints([X0 - H, -2.5, 0], [X0, -2.5, 0], DOWN, color=RATIO),
                    BraceBetweenPoints([X0, -2.5, 0], [X0 + H, -2.5, 0], DOWN, color=RATIO))
        hbl = VGroup(*[MathTex(r"h", font_size=34, color=RATIO).next_to(b, DOWN, buff=0.06) for b in hb])
        self.play(FadeOut(hbr), FadeOut(hl), row.animate.scale(0.55).to_edge(UP, buff=0.35), run_time=0.8)
        self.play(FadeIn(beads3), FadeIn(me), FadeIn(threads), FadeIn(names), FadeIn(myname), FadeIn(hb), FadeIn(hbl),
                  run_time=0.6)
        force = MathTex(r"F_i", r"=", r"T\,\frac{u_{i+1} - u_i}{h}", r"-", r"T\,\frac{u_i - u_{i-1}}{h}", font_size=38)
        force.move_to(RIGHT * 3.3 + UP * 0.3)
        force[0].set_color(FORCE)
        tidy = MathTex(r"F_i", r"=", r"\frac{T}{h}\,\bigl(u_{i+1} - 2u_i + u_{i-1}\bigr)", font_size=42).move_to(force)
        tidy[0].set_color(FORCE)
        small = note(r"gentle slopes: \ the upward part of each pull \\ is $T$ times the slope", font_size=24)
        small.next_to(force, DOWN, buff=0.4)
        with self.voiceover(
            "Take one bead. The thread on its right pulls along the thread, with force T. "
            "<bookmark mark='a'/> Only the up-and-down part of that pull can move the bead, and for a gentle slope "
            "that part is T times the slope: the difference in height, over h. <bookmark mark='b'/> The left thread "
            "does the same with its own slope. <bookmark mark='c'/> Add them, and tidy up."
        ) as vo:
            self.play(FadeIn(pulls), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(force[:3]), FadeIn(small))
            vo.wait_until("b")
            self.play(FadeIn(force[3:]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(force, tidy), FadeOut(small))
        target = always_redraw(lambda: VGroup(
            DashedLine(left, right, color=GREY_C, stroke_width=1.5, dash_length=0.12),
            Dot((left + right) / 2, radius=0.07, color=GOOD)))
        sentence = label(r"each bead is pulled towards \\ the midpoint of its neighbours", font_size=30, color=GOOD)
        sentence.next_to(tidy, DOWN, buff=0.6)
        def net_arrow():
            ty = (left[1] + right[1]) / 2
            if abs(y.get_value() - ty) > 0.12:
                return Arrow(mid(), np.array([X0, ty, 0]), buff=0.0, color=GOOD, stroke_width=6,
                             max_tip_length_to_length_ratio=0.25)
            return Arrow(mid(), mid() + DOWN * 0.3, buff=0.0, color=GOOD, stroke_width=6).set_opacity(0)

        net = always_redraw(net_arrow)
        avg = sentence
        with self.voiceover(
            "Read that as a sentence. Add the two neighbours' heights and subtract twice your own. "
            "<bookmark mark='a'/> The bead is pulled towards the midpoint between its neighbours. If it sits above "
            "the midpoint, it is pulled down. <bookmark mark='b'/> Below, and it is pulled up. <bookmark mark='c'/> "
            "And if the three beads lie on one straight line, however steep, the two pulls cancel and there is no "
            "force at all."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeOut(pulls), FadeOut(tl), FadeOut(hb), FadeOut(hbl), FadeIn(target), FadeIn(net), FadeIn(avg))
            vo.wait_until("b")
            self.play(y.animate.set_value(-2.7), run_time=1.6)
            vo.wait_until("c")
            self.play(y.animate.set_value((left[1] + right[1]) / 2), run_time=1.4)
        self.wait(0.4)
        for m in (me, threads, myname, target, net):
            m.clear_updaters()
        self.tidy_eq = tidy
        self.clear_scene(tidy)

    # ------------------------------------------------------------------
    def newton(self):
        tidy = self.tidy_eq
        newton = MathTex(r"\mu h", r"\,\ddot u_i", r"=", r"\frac{T}{h}\,\bigl(u_{i+1} - 2u_i + u_{i-1}\bigr)", font_size=50)
        newton[0].set_color(MASS), newton[1].set_color(TIME)
        newton.move_to(UP * 2.3)
        tags = VGroup(label(r"mass of a bead", font_size=24, color=MASS).next_to(newton[0], UP, buff=0.3),
                      label(r"its acceleration", font_size=24, color=TIME).next_to(newton[1], DOWN, buff=0.35),
                      label(r"the pull of its neighbours", font_size=24, color=FORCE).next_to(newton[3], DOWN, buff=0.3))
        tags[0].shift(LEFT * 0.5)
        src = note(r"explainer/music/monochord/physics/string.py", font_size=22).move_to(UP * 0.1).to_edge(LEFT, buff=1.2)
        code = code_block([
            "dxx = u[2:] - 2.0 * u[1:-1] + u[:-2]",
            "new = 2.0 * u[1:-1] - up[1:-1] + lam2 * dxx",
        ], font_size=30, color=MC.CODE, buff=0.75).next_to(src, DOWN, buff=0.3, aligned_edge=LEFT)
        cm = VGroup(note(r"each bead against its two neighbours", font_size=24),
                    note(r"every bead, one small step of time later \ (the loss terms are left out here)", font_size=24))
        for c_, line in zip(cm, code):
            c_.next_to(line, DOWN, buff=0.12, aligned_edge=LEFT)
        none = VGroup(*[label(t, font_size=30, color=GREY_B) for t in
                        (r"no pitch", r"no ratios", r"no harmonics", r"no Mersenne")]).arrange(RIGHT, buff=0.8)
        none.to_edge(DOWN, buff=0.55)
        strikes = VGroup(*[Line(t.get_left() + LEFT * 0.05, t.get_right() + RIGHT * 0.05, color=BAD, stroke_width=2.5)
                           for t in none])
        with self.voiceover(
            "Now Newton. A bead's mass is mu, the mass of a metre of string, times h. <bookmark mark='a'/> Mass "
            "times acceleration equals force. That one line is all the physics in a string. <bookmark mark='b'/> It "
            "is also our whole simulation. These two lines are from the code that made every sound so far. "
            "<bookmark mark='c'/> The first compares each bead with its neighbours. The second moves every bead one "
            "small step forward in time. <bookmark mark='d'/> No pitch in there. No ratios, no harmonics, no "
            "Mersenne."
        ) as vo:
            self.play(tidy.animate.move_to(UP * 2.3), run_time=0.6)
            vo.wait_until("a")
            self.play(ReplacementTransform(tidy, newton), run_time=1.2)
            self.play(FadeIn(tags))
            vo.wait_until("b")
            self.play(FadeIn(src), FadeIn(code))
            vo.wait_until("c")
            self.play(Indicate(code[0], color=TUNE, scale_factor=1.03), FadeIn(cm[0]))
            self.play(Indicate(code[1], color=TUNE, scale_factor=1.03), FadeIn(cm[1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(t), Create(k)) for t, k in zip(none, strikes)],
                                  lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.newton_eq = newton
        self.clear_scene(newton)

    # ------------------------------------------------------------------
    def hear(self):
        d = load("beads")
        c = clip("beads.three")
        newton = self.newton_eq
        cols = VGroup()
        views = []
        for N in d["counts"]:
            row = d["rows"][str(N)]
            v = StringView(width=3.6, scale=0.55, stroke_width=2.5)
            x = np.linspace(0, 1, min(N, 60) + 1)
            shape = pluck_shape(x, 1.0, 0.11, 1.0)
            v.set_shape(shape)
            dots = VGroup(*[Dot(v.p(i / (len(x) - 1), shape[i]), radius=0.06 if N < 50 else 0.025, color=STR)
                            for i in range(1, len(x) - 1)])
            head = label(rf"{row['beads']} beads", font_size=30, color=GREY_B)
            flat = VGroup(label(r"its partials are flat by", font_size=20, color=GREY_B),
                          label(rf"2nd: \ {abs(row['flat_cents'][1]):.0f} cents", font_size=24, color=FREQ),
                          label(rf"3rd: \ {abs(row['flat_cents'][2]):.0f} cents", font_size=24, color=FREQ),
                          label(rf"4th: \ {abs(row['flat_cents'][3]):.0f} cents", font_size=24, color=FREQ)
                          ).arrange(DOWN, buff=0.12)
            col = VGroup(head, VGroup(v, dots), flat).arrange(DOWN, buff=0.45)
            col.head, col.view = head, v
            cols.add(col)
            views.append(v)
        cols.arrange(RIGHT, buff=0.7, aligned_edge=UP).move_to(DOWN * 0.9)
        with self.voiceover(
            "You can hear what the beads do. Here is our string chopped into six pieces, then sixteen, then two "
            "hundred, each plucked the same way. Listen to the first one's overtones."
        ):
            self.play(newton.animate.scale(0.7).to_edge(UP, buff=0.35), FadeIn(cols))
        with self.listen(c) as snd:
            window(snd, r"6 pieces, \ 16, \ 200")
            for N, col in zip(d["counts"], cols):
                snd.wait_until(f"n{N}")
                self.play(col.head.animate.set_color(TUNE), run_time=0.2)
                lens = Lens(col.view.p(0.0), col.view.p(1.0), amp=0.16, color=TUNE)
                snd.show(lens)
                nxt = snd.time_of(f"n{d['counts'][d['counts'].index(N) + 1]}") if N != d["counts"][-1] else None
                snd.drive(lens, ring(at=snd.time_of(f"n{N}"), rate=1.6, stop_at=nxt))
        r6 = d["rows"]["6"]
        with self.voiceover(
            f"With five beads the second partial is {say(abs(r6['flat_cents'][1]))} cents flat, most of a semitone, "
            "and the higher ones are worse. It rings like a toy. With two hundred pieces you cannot tell it from a "
            "string. So let the beads shrink to nothing."
        ):
            self.play(Indicate(cols[0][2], color=FREQ, scale_factor=1.08))
        self.wait(0.2)
        self.clear_scene(newton)

    # ------------------------------------------------------------------
    def limit(self):
        newton = self.newton_eq
        rows = [
            MathTex(r"\ddot u_i", r"=", r"\frac{T}{\mu}", r"\cdot", r"\frac{u_{i+1} - 2u_i + u_{i-1}}{h^2}", font_size=46),
            MathTex(r"\frac{\partial^2 u}{\partial t^2}", r"=", r"\frac{T}{\mu}", r"\cdot",
                    r"\frac{\partial^2 u}{\partial x^2}", font_size=46),
            MathTex(r"\frac{\partial^2 u}{\partial t^2}", r"=", r"c^2", r"\,", r"\frac{\partial^2 u}{\partial x^2}",
                    font_size=54),
        ]
        whys = [why(r"divide by the bead's mass, $\mu h$"),
                why(r"$h \to 0$: \ a second difference over $h^2$ is a second derivative"),
                why(r"name the constant: \ $c = \sqrt{T/\mu}$")]
        for r in rows:
            r[0].set_color(TIME)
            r[2].set_color(FORCE)
        step = ladder(self, rows, whys, keep=3, top=1.6, buff=0.55, x=-2.6)
        with self.voiceover(
            "Divide both sides by the bead's mass. <bookmark mark='a'/> On the right there is now a difference of "
            "differences, divided by h squared. As h goes to zero, that is the definition of a second derivative: "
            "the curvature of the string. <bookmark mark='b'/> On the left, the bead's acceleration becomes the "
            "second derivative in time. <bookmark mark='c'/> And the constant, tension over mass per metre, gets a "
            "name: c squared."
        ) as vo:
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        box = SurroundingRectangle(rows[2], color=GOOD, buff=0.22, corner_radius=0.12, stroke_width=2.5)
        name = label(r"the wave equation", font_size=34, color=GOOD).next_to(box, DOWN, buff=0.2)
        card = history_card(1747, r"Jean le Rond d'Alembert", r"writes down this equation for the vibrating string, "
                            r"and solves it: \ one of the first laws of physics stated as a partial differential "
                            r"equation", width=5.2).to_corner(DR, buff=0.4)
        with self.voiceover(
            "This is the wave equation. <bookmark mark='a'/> Jean d'Alembert wrote it down for the vibrating string "
            "in 1747: one of the first laws of physics stated as an equation between rates of change in space and "
            "in time."
        ) as vo:
            self.play(FadeOut(newton), *[FadeOut(m) for m in rows[:2] + whys])
            self.play(rows[2].animate.scale(1.25).move_to(LEFT * 3.2 + UP * 0.4), run_time=0.7)
            box = SurroundingRectangle(rows[2], color=GOOD, buff=0.25, corner_radius=0.12, stroke_width=2.5)
            name = label(r"the wave equation", font_size=36, color=GOOD).next_to(box, DOWN, buff=0.25)
            card.move_to(RIGHT * 3.4 + UP * 0.3)
            self.play(Create(box), FadeIn(name))
            vo.wait_until("a")
            self.play(FadeIn(card, shift=UP * 0.2))
        self.wait(0.3)
        self.eq = VGroup(rows[2], box)
        self.clear_scene(self.eq)

    # ------------------------------------------------------------------
    def meaning(self):
        eq = self.eq
        s = StringView(width=10.6, scale=1.5).shift(DOWN * 0.7)
        x = np.linspace(0, 1, 161)
        bump = np.exp(-0.5 * ((x - 0.33) / 0.07) ** 2) - 0.55 * np.exp(-0.5 * ((x - 0.7) / 0.09) ** 2)
        bump *= np.sin(np.pi * x) ** 0.2
        s.set_shape(bump)
        curv = np.gradient(np.gradient(bump, x), x)

        def arrows(shape, cv, idx, scale):
            g = VGroup()
            for i in idx:
                a = cv[i] * scale
                if abs(a) < 0.08:
                    continue
                p = s.p(x[i], shape[i])
                g.add(Arrow(p, p + UP * a, buff=0.0, color=TIME, stroke_width=4, max_tip_length_to_length_ratio=0.3))
            return g

        arr = arrows(bump, curv, range(6, 156, 6), 0.007)
        says = label(r"acceleration \ $=$ \ $c^2\,\times$ curvature", font_size=32, color=TIME).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Before solving it, read it. The left side is the acceleration of a point of the string. The right side "
            "is the string's curvature there. <bookmark mark='a'/> So a string accelerates wherever it is bent, "
            "towards the inside of the bend. A hump is pulled down. A dip is pulled up. <bookmark mark='b'/> And any "
            "straight stretch, however much it slopes, feels nothing."
        ) as vo:
            self.play(eq.animate.scale(0.75).to_edge(UP, buff=0.4), FadeIn(s))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.05), FadeIn(says), run_time=2.0)
            vo.wait_until("b")
        tri = pluck_shape(x, 1.0, 0.3, 1.0)
        k = int(np.argmax(tri))
        corner = Arrow(s.p(x[k], 1.0), s.p(x[k], 1.0) + DOWN * 1.3, buff=0.0, color=TIME, stroke_width=6,
                       max_tip_length_to_length_ratio=0.25)
        q = label(r"a plucked string is straight everywhere except at one corner", font_size=28, color=TUNE)
        q.next_to(s, DOWN, buff=1.3)
        assume = note(r"assumed: \ small slopes, \ a perfectly flexible string, \ no friction \ (chapters 11 and 12 "
                      r"take these back)", font_size=22).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Which makes a plucked string a strange case. <bookmark mark='a'/> Pull a string aside with one finger and "
            "it is two straight lines. Nothing is curved, so nothing wants to move, except at one point: the "
            "corner, <bookmark mark='b'/> where the curvature is enormous. When you let go, everything that happens "
            "has to start from that corner. The equation tells us where the string accelerates. It does not yet "
            "tell us what the string will do. For that, we have to solve it."
        ) as vo:
            self.play(FadeOut(arr), FadeOut(says))
            vo.wait_until("a")
            s.set_shape(tri)
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(GrowArrow(corner), FadeIn(assume))
        self.wait(0.4)
        self.clear_scene()
