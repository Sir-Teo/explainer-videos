from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Geometry(VoiceoverScene):
    R = 2.6

    def construct(self):
        card = chapter_card(4, r"Geometries other than Euclid's", r"Is space flat?", lit=(1829, 1854), part=PART)
        with self.voiceover("Chapter four. Geometries other than Euclid's."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.postulate()
        self.disk()
        self.triangles()
        self.gauss()

    def to_screen(self, p, c=(-3.2, -0.5)):
        return np.array([c[0] + self.R * p[0], c[1] + self.R * p[1], 0])

    def postulate(self):
        head = label(r"The fifth postulate", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        line = Line([-4.5, -0.8, 0], [4.5, -0.8, 0], color=SPACE, stroke_width=4)
        P = Dot([0, 1.0, 0], radius=0.1, color=LIGHT)
        Pl = MathTex(r"P", font_size=30, color=LIGHT).next_to(P, UP, buff=0.12)
        par = Line([-4.5, 1.0, 0], [4.5, 1.0, 0], color=OK, stroke_width=3)
        many = VGroup(*[Line([-4.5, 1.0 - 4.5 * s, 0], [4.5, 1.0 + 4.5 * s, 0], color=CURVE, stroke_width=2,
                             stroke_opacity=0.7) for s in (-0.12, -0.06, 0.06, 0.12)])
        rows = stack([(r"Euclid: \ through a point off a line, \ exactly one parallel", OK),
                       (r"for two thousand years, \ geometers tried to prove it from the other axioms", HIST),
                       (r"Lobachevsky \ (1829), \ Bolyai \ (1832), \ and Gauss in private: \ deny it, \ and no "
                        r"contradiction follows", CURVE),
                       (r"hyperbolic geometry: \ through $P$, \ infinitely many lines that never meet the line", ABS)],
                     font_size=21, aligned_edge=LEFT, width=11.4, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Euclid's fifth postulate is the odd one out. <bookmark mark='a'/>In the form we learn it: through a "
            "point off a line there is exactly one line that never meets it, the parallel. <bookmark mark='b'/>For "
            "two thousand years geometers tried to prove it from the other, simpler axioms, and failed. "
            "<bookmark mark='c'/>Then Nikolai Lobachevsky in 1829, János Bolyai in 1832, and Gauss privately before "
            "both, tried denying it, and found no contradiction, only a new geometry. <bookmark mark='d'/>In "
            "hyperbolic geometry, through the point there are infinitely many lines that never meet the given line. "
            "And Part 7's lesson applies: the parallel postulate is independent of the other axioms."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(P), FadeIn(Pl))
            vo.wait_until("a")
            self.play(Create(par), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(m) for m in many], lag_ratio=0.2), FadeIn(rows[3]))
        self.clear_scene()

    def disk(self):
        head = label(r"The Poincaré disk", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        c = (-3.2, -0.5)
        bound = Circle(radius=self.R, color=GREY_B, stroke_width=2.5).move_to(self.to_screen((0, 0)))
        pairs = [((-0.9, 0.2), (0.85, 0.35)), ((-0.5, -0.8), (0.6, -0.7)), ((-0.2, 0.9), (0.1, -0.95)),
                 ((-0.85, -0.3), (0.3, 0.88))]
        geos = VGroup()
        for u, v in pairs:
            pts = S.geodesic(u, v, n=80)
            geos.add(VMobject(stroke_color=SPACE, stroke_width=3).set_points_smoothly([self.to_screen(p, c)
                                                                                       for p in pts]))
        line = S.geodesic((-0.95, -0.2), (0.95, -0.2), n=80)
        base = VMobject(stroke_color=CURVE, stroke_width=4).set_points_smoothly([self.to_screen(p, c) for p in line])
        P = (0.0, 0.45)
        pz = complex(*P)
        par = VGroup()
        # the disk automorphism z -> (z + p) / (1 + conj(p) z) carries diameters to the lines through P
        for phi in (-0.3, 0.0, 0.3):
            zs = [(r * np.exp(1j * phi) + pz) / (1 + np.conj(pz) * r * np.exp(1j * phi))
                  for r in np.linspace(-0.995, 0.995, 80)]
            par.add(VMobject(stroke_color=OK, stroke_width=2.5).set_points_smoothly(
                [self.to_screen((z.real, z.imag), c) for z in zs]))
        Pd = Dot(self.to_screen(P, c), radius=0.09, color=LIGHT)
        rows = stack([(r"the whole infinite hyperbolic plane, \ drawn inside a circle", WHITE),
                      (r"straight lines: \ arcs that meet the rim at right angles", SPACE),
                      (r"distances grow without bound toward the rim: \ $d = \operatorname{arcosh}\!\left(1 + "
                       r"\frac{2|u-v|^2}{(1-|u|^2)(1-|v|^2)}\right)$", ABS),
                      (r"through a point, \ many lines missing the pink one", OK)], font_size=20,
                     aligned_edge=LEFT, width=5.6, buff=0.3).move_to([3.6, -0.3, 0])
        with self.voiceover(
            "Henri Poincaré found a way to draw it. <bookmark mark='a'/>The whole infinite hyperbolic plane fits "
            "inside a circle. <bookmark mark='b'/>Its straight lines, the geodesics, are arcs of circles that meet "
            "the rim at right angles, and diameters. <bookmark mark='c'/>Distances are measured by this formula, "
            "which grows without bound as you approach the rim, so the rim is infinitely far away and never reached. "
            "<bookmark mark='d'/>And through a point off a line, many lines miss it: here the pink line and three "
            "green ones through the gold point, none of which meets it."
        ) as vo:
            self.play(FadeIn(head), Create(bound))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(g) for g in geos], lag_ratio=0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeOut(geos), Create(base), FadeIn(Pd), LaggedStart(*[Create(p) for p in par],
                                                                          lag_ratio=0.3), FadeIn(rows[3]))
        self.clear_scene()

    def triangles(self):
        d = load("disk")
        head = label(r"Triangles in the disk", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        c = (-3.2, -0.5)
        bound = Circle(radius=self.R, color=GREY_B, stroke_width=2.5).move_to(self.to_screen((0, 0), c))
        cols = [OK, SPACE, LIGHT, MATTER, CURVE]
        tris = VGroup()
        for r, col in zip(d["rows"], cols):
            g = VGroup()
            for side in r["sides"].values():
                g.add(VMobject(stroke_color=col, stroke_width=3).set_points_smoothly([self.to_screen(p, c)
                                                                                      for p in side]))
            tris.add(g)
        hd = [r"\text{size}", r"\text{angle sum}", r"\text{area} = \pi - \text{sum}"]
        rows = [[MathTex(f"{r['rho']:.1f}", font_size=22, color=col), MathTex(rf"{r['sum_deg']:.1f}^\circ",
                                                                             font_size=22),
                 MathTex(f"{r['area']:.3f}", font_size=22, color=ABS)] for r, col in zip(d["rows"], cols)]
        grid = ValueGrid(hd, rows, col_w=[1.4, 2.0, 2.8], cell_h=0.46, font_size=20).move_to([3.6, 0.6, 0])
        f = MathTex(r"\text{Area} = \frac{\pi - (\alpha + \beta + \gamma)}{|K|}", font_size=30,
                    color=ABS).next_to(grid, DOWN, buff=0.45)
        note = label(r"large triangles are thin; \ no triangle has area above $\pi$", font_size=20,
                     color=GOAL).next_to(f, DOWN, buff=0.3)
        with self.voiceover(
            "Now draw triangles. <bookmark mark='a'/>The Reasoner places five equilateral triangles at the centre "
            "of the disk, each larger than the last, and measures their angles; the disk is conformal, so angles "
            "can be read off the drawing. <bookmark mark='b'/>The smallest has angles summing to just under a "
            "hundred and eighty degrees. As they grow, the sum falls: a hundred and fifty-five, a hundred and "
            "sixteen, sixty-nine, twenty-three. <bookmark mark='c'/>And the area is exactly the shortfall, pi minus "
            "the angle sum, in units set by the curvature. <bookmark mark='d'/>So no hyperbolic triangle, however "
            "large, has area greater than pi. In a curved space, measuring the angles of a big enough triangle "
            "reveals the curvature."
        ) as vo:
            self.play(FadeIn(head), Create(bound))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("b")
            for i in range(len(rows)):
                self.play(Create(tris[i]), *[FadeIn(x) for x in grid.cell[i]], run_time=0.8)
            vo.wait_until("c")
            self.play(Write(f))
            vo.wait_until("d")
            self.play(FadeIn(note))
        self.clear_scene()

    def gauss(self):
        g = load("gauss")
        head = label(r"Did Gauss measure space?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        A, B, C = np.array([-5.6, 1.0, 0]), np.array([-1.4, 1.4, 0]), np.array([-3.4, -1.6, 0])
        tri = Polygon(A, B, C, color=LIGHT, stroke_width=3, fill_opacity=0.08, fill_color=LIGHT)
        names = VGroup(label(r"Brocken", font_size=19, color=WHITE).next_to(A, LEFT, buff=0.15),
                       label(r"Inselsberg", font_size=19, color=WHITE).next_to(B, RIGHT, buff=0.15),
                       label(r"Hohenhagen", font_size=19, color=WHITE).next_to(C, DOWN, buff=0.15))
        rows = stack([(r"the Hanover survey, \ 1820s: \ sides of about 69, \ 85 and 107 km", WHITE),
                      (rf"on the curved Earth the angles must exceed $180^\circ$ by area$/R^2$: \ "
                       rf"{g['excess_arcsec']:.1f} arcseconds", ABS),
                      (r"the famous story: \ Gauss tested the geometry of space itself, \ and found it Euclidean", HIST),
                      (r"probably a legend: \ the survey was geodesy; \ but Riemann \ (1854) \ made the question "
                       r"real", BAD)], font_size=21, aligned_edge=LEFT, width=6.2, buff=0.3).move_to([3.6, -0.2, 0])
        with self.voiceover(
            "Did anyone ever check space itself? <bookmark mark='a'/>In the 1820s Gauss led a survey of the kingdom "
            "of Hanover, with a great triangle between three mountain tops, the Brocken, the Inselsberg and the "
            "Hohenhagen, with sides of roughly seventy, eighty-five and a hundred and seven kilometres. "
            "<bookmark mark='b'/>Because the survey follows the curved surface of the Earth, the angles must add to "
            "more than a hundred and eighty degrees, by the area over the Earth's radius squared: the Reasoner gets "
            "about fifteen arcseconds. <bookmark mark='c'/>The famous story says Gauss was testing whether space "
            "itself is curved, and found it Euclidean within his errors. <bookmark mark='d'/>Historians think that "
            "story is mostly legend: the survey was geodesy. But in 1854 Bernhard Riemann, Gauss's student, made the "
            "question real: the geometry of space is a matter of fact, to be settled by measurement and by physics. "
            "Sixty years later, Einstein made curvature part of physics."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(tri), FadeIn(names), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
