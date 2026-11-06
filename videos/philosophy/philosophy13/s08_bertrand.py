from __future__ import annotations

import math

from videos.philosophy.philosophy13.common import *  # noqa: F403

LONG, SHORT = "#FFD166", "#4A5A70"
METHODS = [("endpoints", r"random endpoints", r"$\tfrac13$"), ("radius", r"random radius", r"$\tfrac12$"),
           ("midpoint", r"random midpoint", r"$\tfrac14$")]


class Bertrand(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Bertrand's chords", r"Can ignorance fix a prior?", lit=(1889, 1921, 1957),
                            part=PART)
        with self.voiceover("Chapter seven. Bertrand's chords."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.indifference()
        self.question()
        self.chords()
        self.why()
        self.cubes()
        self.jaynes()
        self.brick()

    def indifference(self):
        head = label(r"The principle of indifference", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rule = MathTex(r"\text{no reason to favour any of } n \text{ possibilities} \ \Longrightarrow\ "
                       r"P(\text{each}) = \tfrac{1}{n}", font_size=36).next_to(head, DOWN, buff=0.6)
        rows = stack([(r"Laplace's `principle of insufficient reason'; \ named `indifference' by Keynes, \ 1921",
                       GREY_A),
                      (r"a die you know nothing about: \ $\tfrac16$ each", WHITE),
                      (r"the objective Bayesian's dream: \ ignorance itself fixes the prior", GOAL),
                      (r"for infinitely many possibilities: \ a uniform density", WHITE)], font_size=25).next_to(
            rule, DOWN, buff=0.5)
        with self.voiceover(
            "The simplest way to fix a prior is the principle of indifference. <bookmark mark='a'/>If you have no "
            "reason to favour any of n possibilities, give each one an nth. <bookmark mark='b'/>Laplace called it "
            "the principle of insufficient reason; John Maynard Keynes renamed it in 1921, and also catalogued its "
            "paradoxes. <bookmark mark='c'/>Knowing nothing about a die, give each face a sixth. "
            "<bookmark mark='d'/>If it worked, it would realize the objective Bayesian's dream: ignorance itself would "
            "fix the prior. <bookmark mark='e'/>With infinitely many possibilities, the principle says to use a "
            "uniform density. And there it breaks."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rule))
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def question(self):
        hc = history_card(1889, r"Joseph Bertrand", r"\textit{Calcul des probabilités}", width=4.8,
                          color=HIST).to_corner(UL, buff=0.35)
        R = 2.2
        c = Circle(radius=R, color=WHITE, stroke_width=3).move_to([-2.6, -0.6, 0])
        o = c.get_center()
        tri = Polygon(*[o + R * np.array([math.cos(PI / 2 + k * TAU / 3), math.sin(PI / 2 + k * TAU / 3), 0])
                        for k in range(3)], color=COH, stroke_width=3)
        side = label(r"side $\sqrt{3}$", font_size=22, color=COH).next_to(tri, DOWN, buff=0.1)
        chord = Line(o + R * np.array([math.cos(2.6), math.sin(2.6), 0]), o + R * np.array([math.cos(-0.2),
                                                                                             math.sin(-0.2), 0]),
                     color=LONG, stroke_width=4)
        q = stack([(r"a circle of radius 1, \ and its inscribed equilateral triangle", WHITE),
                   (r"draw a chord `at random'", LONG),
                   (r"what is the chance it is longer than the triangle's side?", BET),
                   (r"indifference: \ `use the uniform distribution'. \ \ Over \textit{what}?", BAD)], font_size=24,
                  aligned_edge=LEFT, width=6.4).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Joseph Bertrand's problem, from 1889. <bookmark mark='a'/>Take a circle of radius one and the "
            "equilateral triangle inscribed in it; the triangle's side is root three. <bookmark mark='b'/>Draw a "
            "chord of the circle at random. <bookmark mark='c'/>What is the chance that it is longer than the side "
            "of the triangle? <bookmark mark='d'/>Indifference says: choose the chord uniformly. But uniformly over "
            "what? There are several natural ways to pick a chord, and each is uniform over something."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(c), Create(tri), FadeIn(side), FadeIn(q[0]))
            vo.wait_until("b")
            self.play(Create(chord), FadeIn(q[1]))
            vo.wait_until("c")
            self.play(FadeIn(q[2]))
            vo.wait_until("d")
            self.play(FadeIn(q[3]))
        self.clear_scene()

    def chords(self):
        d = load("bertrand")["chords"]
        head = label(r"Three ways to be indifferent, \ simulated", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        R = 1.65
        panels = VGroup()
        for i, (key, name, exact) in enumerate(METHODS):
            o = np.array([-4.4 + 4.4 * i, -0.2, 0])
            circ = Circle(radius=R, color=WHITE, stroke_width=2.5).move_to(o)
            lines = VGroup()
            for x1, y1, x2, y2 in d[key]["sample"]:
                long = math.hypot(x1 - x2, y1 - y2) > math.sqrt(3)
                lines.add(Line(o + R * np.array([x1, y1, 0]), o + R * np.array([x2, y2, 0]),
                               color=LONG if long else SHORT, stroke_width=1.2, stroke_opacity=0.75 if long else 0.6))
            title = label(name, font_size=24, color=CRED).next_to(circ, UP, buff=0.25)
            freq = VGroup(label(r"100{,}000 chords:", font_size=20, color=GREY_A),
                          MathTex(rf"{d[key]['freq']:.3f}", font_size=30, color=LONG)).arrange(RIGHT, buff=0.15)
            freq.next_to(circ, DOWN, buff=0.3)
            ex = label(rf"exactly {exact}", font_size=24, color=GOAL).next_to(freq, DOWN, buff=0.15)
            p = VGroup(circ, title, lines, freq, ex)
            p.lines = lines
            panels.add(p)
        legend = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.4, color=LONG, stroke_width=3),
                               label(r"longer than $\sqrt{3}$", font_size=20, color=LONG)).arrange(RIGHT, buff=0.12),
                        VGroup(Line(ORIGIN, RIGHT * 0.4, color=SHORT, stroke_width=3),
                               label(r"shorter", font_size=20, color=GREY_B)).arrange(RIGHT, buff=0.12)).arrange(
            RIGHT, buff=0.6).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The Reasoner draws a hundred thousand chords each way, and shows two hundred and fifty of them. "
            "<bookmark mark='a'/>First: pick two points on the circle, uniformly and independently, and join them. "
            "<bookmark mark='b'/>About one third of these chords are long. <bookmark mark='c'/>Second: pick a "
            "radius at random, a point uniformly along it, and draw the chord through that point at right angles to "
            "the radius. <bookmark mark='d'/>Half are long. <bookmark mark='e'/>Third: pick a point uniformly in the "
            "disk, and draw the chord that has it as its midpoint. <bookmark mark='f'/>A quarter are long. "
            "<bookmark mark='g'/>One question, three uniform distributions, three answers: a third, a half, a quarter. "
            "Each simulation matches its exact value."
        ) as vo:
            self.play(FadeIn(head), FadeIn(legend))
            for k, (m1, m2) in enumerate((("a", "b"), ("c", "d"), ("e", "f"))):
                p = panels[k]
                vo.wait_until(m1)
                self.play(Create(p[0]), FadeIn(p[1]))
                self.play(LaggedStart(*[Create(ln) for ln in p.lines], lag_ratio=0.01), run_time=3)
                vo.wait_until(m2)
                self.play(FadeIn(p[3]))
            vo.wait_until("g")
            self.play(*[FadeIn(p[4]) for p in panels])
        self.clear_scene()

    def why(self):
        head = label(r"Why each answer is right, \ by its own lights", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        R = 1.5
        cols = VGroup()
        # endpoints: fix the first endpoint at the top; long iff the second lands in the opposite 120-degree arc
        o1 = np.array([-4.4, 0.2, 0])
        c1 = Circle(radius=R, color=WHITE, stroke_width=2.5).move_to(o1)
        arc = Arc(radius=R, start_angle=-PI / 2 - PI / 3, angle=2 * PI / 3, arc_center=o1, color=LONG, stroke_width=8)
        p0 = Dot(o1 + R * UP, color=CRED)
        t1 = label(r"fix one end: \ long iff the other lands in the far third", font_size=19, color=GREY_A)
        # radius: long iff the point lies within 1/2 of the centre
        o2 = np.array([0.0, 0.2, 0])
        c2 = Circle(radius=R, color=WHITE, stroke_width=2.5).move_to(o2)
        rad = Line(o2, o2 + R * RIGHT, color=GREY_B, stroke_width=3)
        half = Line(o2, o2 + 0.5 * R * RIGHT, color=LONG, stroke_width=8)
        t2 = label(r"on a radius: \ long iff within $\tfrac12$ of the centre", font_size=19, color=GREY_A)
        # midpoint: long iff the midpoint lies in the circle of radius 1/2
        o3 = np.array([4.4, 0.2, 0])
        c3 = Circle(radius=R, color=WHITE, stroke_width=2.5).move_to(o3)
        inner = Circle(radius=0.5 * R, color=LONG, fill_color=LONG, fill_opacity=0.5, stroke_width=3).move_to(o3)
        t3 = label(r"midpoint: \ long iff inside radius $\tfrac12$: \ area $\tfrac14$", font_size=19, color=GREY_A)
        for g, circ, t in ((VGroup(c1, arc, p0), c1, t1), (VGroup(c2, rad, half), c2, t2), (VGroup(c3, inner), c3, t3)):
            if t.width > 3.9:
                t.width = 3.9
            t.next_to(circ, DOWN, buff=0.35)
            cols.add(VGroup(g, t))
        foot = label(r"`at random' is not a property of chords: \ it is a choice of what to be uniform over",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Each answer is correct for its own way of choosing. <bookmark mark='a'/>With random endpoints, fix the "
            "first end; the chord is long exactly when the other end lands in the far third of the circle. One "
            "third. <bookmark mark='b'/>With a random point on a radius, the chord is long exactly when the point is "
            "within a half of the centre. One half. <bookmark mark='c'/>With a random midpoint, the chord is long "
            "exactly when the midpoint lies inside the circle of radius one half, which has a quarter of the area. "
            "One quarter. <bookmark mark='d'/>Being drawn at random is not a property of chords. It is a choice of "
            "what to be uniform over, and the principle of indifference cannot make it for us."
        ) as vo:
            self.play(FadeIn(head))
            for mk, col in zip("abc", cols):
                vo.wait_until(mk)
                self.play(FadeIn(col[0]), FadeIn(col[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def cubes(self):
        d = load("bertrand")["cubes"]
        head = label(r"Van Fraassen's cube factory", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sub = label(r"a factory makes cubes with sides up to 1 cm. \ Chance of a side of at most $\tfrac12$ cm?",
                    font_size=24, color=BET).next_to(head, DOWN, buff=0.3)
        rows = VGroup()
        for i, (what, cut, val, txt) in enumerate(((r"side", 0.5, d["side"], r"side $\leq \tfrac12$"),
                                                   (r"face area", 0.25, d["area"], r"area $\leq \tfrac14$"),
                                                   (r"volume", 0.125, d["volume"], r"volume $\leq \tfrac18$"))):
            y = 1.0 - i * 1.3
            line = Line([-3.0, y, 0], [3.0, y, 0], color=GREY_C, stroke_width=3)
            fill = Line([-3.0, y, 0], [-3.0 + 6.0 * cut, y, 0], color=LONG, stroke_width=10)
            nm = label(rf"uniform over {what}", font_size=22, color=CRED).next_to(line, LEFT, buff=0.3)
            lab = label(txt, font_size=20, color=LONG).next_to(fill, UP, buff=0.1)
            pv = MathTex(rf"P = {val:g}", font_size=30, color=LONG).next_to(line, RIGHT, buff=0.3)
            rows.add(VGroup(line, fill, nm, lab, pv))
        rows.next_to(sub, DOWN, buff=0.6)
        foot = label(r"the same event, \ three answers: \ $\tfrac12,\ \tfrac14,\ \tfrac18$", font_size=26,
                     color=BAD).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Bas van Fraassen's version needs no geometry. <bookmark mark='a'/>A factory makes cubes with sides of "
            "up to one centimetre. What is the chance that the next cube's side is at most half a centimetre? "
            "<bookmark mark='b'/>Be indifferent over side length, and the answer is one half. "
            "<bookmark mark='c'/>But a side of at most a half is a face of at most a quarter. Be indifferent over "
            "face area, and the answer is one quarter. <bookmark mark='d'/>And it is a volume of at most an eighth: "
            "be indifferent over volume, and the answer is one eighth. <bookmark mark='e'/>One event; three answers. "
            "Ignorance of side, of area and of volume are the same ignorance, yet indifference gives each a different "
            "prior."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(sub))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(Create(r[0]), FadeIn(r[2]))
                self.play(Create(r[1]), FadeIn(r[3]), FadeIn(r[4]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def jaynes(self):
        hc = history_card(1973, r"Edwin Jaynes", r"`The Well-Posed Problem'", width=4.8, color=HIST).to_corner(
            UL, buff=0.35)
        rows = stack([
            (r"demand that the answer not depend on where the circle is, \ how big, \ or how turned", WHITE),
            (r"invariance under translation, \ scaling, \ rotation", CRED),
            (r"only one ensemble survives: \ random radius, \ $\tfrac12$", OK),
            (r"and he checked it: \ straws tossed onto a circle land with a half", GREY_A),
            (r"but: \ which symmetries? \ that choice is not given by ignorance", BAD),
            (r"the cube factory has no symmetry that settles it", BAD),
        ], font_size=24, aligned_edge=LEFT, width=12.0).next_to(hc, DOWN, buff=0.5).set_x(0)
        with self.voiceover(
            "Jaynes fought back in 1973, in a paper called The Well-Posed Problem. <bookmark mark='a'/>If the problem "
            "states nothing about the circle's position, size or orientation, then the answer should not depend on "
            "them. <bookmark mark='b'/>So demand that the distribution of chords be invariant under translation, "
            "scaling and rotation. <bookmark mark='c'/>Only one of the three ensembles survives: the random radius, "
            "with its answer one half. <bookmark mark='d'/>Jaynes even reported tossing straws at a circle drawn on "
            "the floor, which agreed. <bookmark mark='e'/>But the reply has limits. Which symmetries to demand is "
            "itself a substantive choice; ignorance does not supply it. <bookmark mark='f'/>And many problems, like "
            "the cube factory, have no symmetry group that settles the answer."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def brick(self):
        w = wall(upto=13, current=13).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(13, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirteenth brick in the Wall. <bookmark mark='a'/>The dream: one rational prior, read off "
            "from ignorance alone. <bookmark mark='b'/>The wall: Bertrand's paradox, which shows that indifference "
            "gives incompatible answers depending on how the possibilities are described. <bookmark mark='c'/>What "
            "it forces: priors are choices. They can be argued for, with symmetry, with calibration, with track "
            "records, but they are not given free by ignorance. Every Bayesian, human or machine, starts from a bet."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[13], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]))
            vo.wait_until("b")
            self.play(FadeIn(card[1][1]))
            vo.wait_until("c")
            self.play(Indicate(card, color=P.WALL, scale_factor=1.02))
        self.clear_scene()
