from __future__ import annotations

import numpy as np

from videos.stats.stats2.common import *  # noqa: F403

METHODS = [("ends", r"two random endpoints", r"\tfrac13", 1 / 3),
           ("radius", r"a random point on a random radius", r"\tfrac12", 1 / 2),
           ("midpoint", r"a random midpoint in the disc", r"\tfrac14", 1 / 4)]
R = 1.8
XS = [-4.6, 0.0, 4.6]
Y0 = 0.35
LONG, SHORT = S.ACCENT, "#55657A"


class Bertrand(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_q()
        self.three()
        self.midpoints()
        self.resolution()

    def card(self):
        card = chapter_card(3, r"Bertrand's paradox", r"Draw a chord of a circle at random. How likely is it to be "
                            r"long?", lit=(1889,), part=PART)
        with self.voiceover("Chapter three. Bertrand's paradox."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_q(self):
        c = Circle(radius=2.4, stroke_color=GREY_A, stroke_width=3).move_to([-2.6, -0.2, 0])
        verts = [c.get_center() + 2.4 * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, PI / 2 + TAU / 3,
                                                                                      PI / 2 + 2 * TAU / 3)]
        tri = Polygon(*verts, stroke_color=EXACT, stroke_width=3)
        side = label(r"side $= \sqrt3\, r$", font_size=26, color=EXACT).next_to(tri, DOWN, buff=0.15)
        g = np.random.Generator(np.random.PCG64(5))
        demo = VGroup()
        for _ in range(6):
            t1, t2 = g.uniform(0, TAU, 2)
            p, q = [c.get_center() + 2.4 * np.array([np.cos(t), np.sin(t), 0]) for t in (t1, t2)]
            col = LONG if np.linalg.norm(p - q) > np.sqrt(3) * 2.4 else GREY_B
            demo.add(Line(p, q, color=col, stroke_width=2.5))
        hc = history_card(1889, r"Joseph Bertrand, \ \emph{Calcul des probabilit\'es}", r"a chord is drawn at random "
                          r"in a circle. \ What is the probability that it is longer than the side of the inscribed "
                          r"equilateral triangle?", color=S.MUSEUM, width=5.8, font_size=23).move_to([3.6, 0.6, 0])
        with self.voiceover(
            "Galileo had to choose which cases were equally likely. In 1889 Joseph Bertrand showed that sometimes "
            "the choice decides the answer. <bookmark mark='a'/> Take a circle, and draw the equilateral triangle "
            "inside it; its side is root three times the radius. <bookmark mark='b'/> Now draw a chord of the circle "
            "at random. <bookmark mark='c'/> What's the probability that the chord is longer than the triangle's "
            "side? It sounds like a question with one answer. Bertrand gave three, each argued correctly."
        ) as vo:
            self.play(Create(c))
            vo.wait_until("a")
            self.play(Create(tri), FadeIn(side))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l) for l in demo], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(hc, shift=LEFT * 0.2))
        self.clear_scene()

    def panel(self, k):
        key, title, ftex, _ = METHODS[k]
        ctr = np.array([XS[k], Y0, 0])
        circ = Circle(radius=R, stroke_color=GREY_A, stroke_width=2.5).move_to(ctr)
        head = label(title, font_size=22, color=GREY_A).next_to(circ, UP, buff=0.3)
        num = label(rf"method {k + 1}", font_size=20, color=GREY_B).next_to(head, UP, buff=0.08)
        return ctr, VGroup(circ, head, num)

    def three(self):
        d = load("bertrand")
        panels, chords, counters, whys_ = [], [], [], []
        for k, (key, title, ftex, exact) in enumerate(METHODS):
            ctr, pnl = self.panel(k)
            panels.append(pnl)
            P, Q, L = np.asarray(d[f"{key}_p"]), np.asarray(d[f"{key}_q"]), np.asarray(d[f"{key}_long"])
            ch = VGroup(*[Line(ctr + R * np.array([p[0], p[1], 0]), ctr + R * np.array([q[0], q[1], 0]),
                               color=LONG if l else SHORT, stroke_width=1.3, stroke_opacity=0.75)
                          for p, q, l in zip(P[:160], Q[:160], L[:160])])
            chords.append(ch)
            frac_ = d[f"{key}_frac"]
            cnt = VGroup(MathTex(r"\text{exact}\ ", ftex, font_size=32, color=EXACT),
                         MathTex(rf"\text{{simulated}}\ {frac_:.3f}", font_size=26, color=SIM)).arrange(DOWN, buff=0.12)
            cnt.move_to(ctr + DOWN * (R + 0.75))
            counters.append(cnt)
        # why each answer: the critical region
        c0 = np.array([XS[0], Y0, 0])
        arc = Arc(radius=R, start_angle=-PI / 2 - PI / 3, angle=TAU / 3, stroke_color=EXACT, stroke_width=7)
        arc.move_arc_center_to(c0)
        fixed = Dot(c0 + R * UP, radius=0.07, color=WHITE)
        tri0 = Polygon(*[c0 + R * np.array([np.cos(a), np.sin(a), 0]) for a in (PI / 2, PI / 2 + TAU / 3,
                                                                                 PI / 2 + 2 * TAU / 3)],
                       stroke_color=EXACT, stroke_width=1.5, stroke_opacity=0.6)
        c1 = np.array([XS[1], Y0, 0])
        rad = Line(c1, c1 + R * RIGHT, color=GREY_B, stroke_width=3)
        inner = Line(c1, c1 + R / 2 * RIGHT, color=EXACT, stroke_width=7)
        c2 = np.array([XS[2], Y0, 0])
        disc = Circle(radius=R / 2, stroke_width=0, fill_color=EXACT, fill_opacity=0.35).move_to(c2)
        whys = [label(r"far third of the circle", font_size=20, color=EXACT).move_to(c0 + DOWN * (R + 0.25)),
                label(r"inner half of the radius", font_size=20, color=EXACT).move_to(c1 + DOWN * (R + 0.25)),
                label(r"inner disc: \ a quarter of the area", font_size=20, color=EXACT).move_to(c2 + DOWN * (R + 0.25))]
        tag = note(rf"simulated: {fmt_int(d['n'])} chords by each method (160 drawn)").to_corner(DR, buff=0.25)
        for c in counters:
            c.shift(DOWN * 0.3)
        with self.voiceover(
            "Here they are, side by side. <bookmark mark='a'/> Method one: pick two points on the circle at random "
            "and join them. By symmetry, fix the first point at the top. The chord is long exactly when the second "
            "point lands on the far third of the circle, between the triangle's other two corners. "
            "<bookmark mark='b'/> Probability one third. <bookmark mark='c'/> Method two: pick a radius at random, "
            "then a point on it at random, and draw the chord through that point, at right angles to the radius. "
            "The chord is long exactly when the point is in the inner half of the radius. <bookmark mark='d'/> "
            "Probability one half. <bookmark mark='e'/> Method three: pick a point anywhere in the disc at random "
            "and draw the chord that has it as its midpoint. The chord is long exactly when the midpoint is inside "
            "the circle of half the radius, which has a quarter of the area. <bookmark mark='f'/> Probability one "
            f"quarter. <bookmark mark='g'/> And simulation agrees with all three: {fmt_int(d['n'])} chords each, "
            f"long in {d['ends_frac']:.3f}, {d['radius_frac']:.3f} and {d['midpoint_frac']:.3f} of cases. Three "
            "correct calculations, three different answers."
        ) as vo:
            self.play(*[FadeIn(p) for p in panels], FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(tri0), FadeIn(fixed), Create(arc), FadeIn(whys[0]))
            self.play(LaggedStart(*[Create(l) for l in chords[0]], lag_ratio=0.02), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeOut(whys[0]), FadeIn(counters[0][0]))
            vo.wait_until("c")
            self.play(Create(rad), Create(inner), FadeIn(whys[1]))
            self.play(LaggedStart(*[Create(l) for l in chords[1]], lag_ratio=0.02), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeOut(whys[1]), FadeIn(counters[1][0]))
            vo.wait_until("e")
            self.play(FadeIn(disc), FadeIn(whys[2]))
            self.play(LaggedStart(*[Create(l) for l in chords[2]], lag_ratio=0.02), run_time=3.0)
            vo.wait_until("f")
            self.play(FadeOut(whys[2]), FadeIn(counters[2][0]))
            vo.wait_until("g")
            self.play(*[FadeIn(c[1]) for c in counters])
        self.panels, self.chords, self.counters = panels, chords, counters
        self.extras = VGroup(arc, fixed, tri0, rad, inner, disc, tag)

    def midpoints(self):
        d = load("bertrand")
        dots = []
        for k, (key, *_r) in enumerate(METHODS):
            ctr = np.array([XS[k], Y0, 0])
            P, Q = np.asarray(d[f"{key}_p"]), np.asarray(d[f"{key}_q"])
            mids = (P + Q) / 2
            dots.append(VGroup(*[Dot(ctr + R * np.array([m[0], m[1], 0]), radius=0.03, color=SIM) for m in mids]))
        head = label(r"each chord is fixed by its midpoint: \ the same chords, \ three different clouds", font_size=28,
                     color=S.ACCENT).to_edge(UP, buff=0.25)
        with self.voiceover(
            "How can that be? Look at what each method actually does. <bookmark mark='a'/> A chord is determined by "
            "its midpoint, so shrink every chord to its midpoint. <bookmark mark='b'/> The three methods scatter "
            "the midpoints in three different ways. Two random endpoints put most midpoints near the rim. A random "
            "point on a random radius crowds them toward the centre. A random midpoint spreads them evenly. "
            "<bookmark mark='c'/> These are three different probability distributions on the same set of chords. "
            "Each method is a different meaning of the words at random, and the question, as asked, didn't say "
            "which."
        ) as vo:
            self.play(FadeOut(self.extras), *[FadeOut(c) for c in self.counters])
            vo.wait_until("a")
            self.play(FadeIn(head))
            anims = []
            for ch, ds in zip(self.chords, dots):
                anims += [ReplacementTransform(l, dt) for l, dt in zip(ch, ds[:len(ch)])]
            self.play(*anims, run_time=2.5)
            extra = [ds[len(ch):] for ch, ds in zip(self.chords, dots)]
            vo.wait_until("b")
            self.play(*[FadeIn(e, lag_ratio=0.01) for e in extra], run_time=1.5)
            vo.wait_until("c")
            self.play(*[Indicate(p[0], color=S.ACCENT, scale_factor=1.05) for p in self.panels])
        keep = VGroup(*self.panels, *dots)
        self.play(FadeOut(head), keep.animate.scale(0.5).move_to([0, -2.55, 0]))
        self.keep = keep

    def resolution(self):
        dfn = definition_card(r"A probability model", r"a set of outcomes $\Omega$, \ and a rule $P$ that gives "
                              r"each event a probability. \ ``At random'' means nothing until $P$ is chosen.",
                              color=EXACT, width=6.4, font_size=24).move_to([-3.3, 1.9, 0])
        hc = history_card(1973, r"E. T. Jaynes, \ ``The well-posed problem''", r"if the answer must not depend on the "
                          r"circle's position, size or orientation, \ only method 2 survives: \ $\tfrac12$. \ Straws "
                          r"thrown at a circle agree.", color=S.MUSEUM, width=5.8, font_size=22).move_to([3.5, 1.9, 0])
        take = label(r"on a continuum, \ ``equally likely'' is a \emph{choice of measure}", font_size=32,
                     color=S.ACCENT).move_to([0, -0.15, 0])
        nxt = label(r"next: \ Kolmogorov makes the measure the foundation", font_size=24, color=GREY_B)
        nxt.next_to(take, DOWN, buff=0.2)
        with self.voiceover(
            "The lesson is the reason modern probability is built the way it is. <bookmark mark='a'/> A probability "
            "model has two parts: a set of possible outcomes, and a rule that assigns each event a probability. "
            "Counting equally likely cases is one such rule, and it works for dice. On a continuum, like the set of "
            "all chords, there's no natural count, and at random means nothing until you've chosen the rule. "
            "<bookmark mark='b'/> Can a principle choose it for us? In 1973 the physicist Edwin Jaynes argued that "
            "if the answer mustn't change when the circle is moved, enlarged or turned, only the second method "
            "survives, giving one half, and that straws tossed onto a circle agree. It's an elegant argument, and "
            "it's an extra assumption, not a consequence of the words at random. <bookmark mark='c'/> On a "
            "continuum, equally likely is a choice of measure. <bookmark mark='d'/> So the measure itself must be "
            "part of the foundations. In 1933 Andrey Kolmogorov wrote those foundations down."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(dfn, shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=LEFT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(take, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(nxt))
        self.clear_scene()
