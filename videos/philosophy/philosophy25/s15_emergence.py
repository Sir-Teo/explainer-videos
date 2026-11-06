from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Emergence(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Spacetime from something else?", r"Could space and time be emergent?",
                            lit=(1997, 2013), part=PART)
        with self.voiceover("Chapter fourteen. Spacetime from something else?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.clash()
        self.holography()
        self.causets()
        self.philosophy()

    def clash(self):
        head = label(r"Two theories that do not fit", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"general relativity", r"spacetime is a smooth, \ dynamical field; \ no fixed background", CURVE),
            (r"quantum field theory", r"fields on a fixed spacetime stage; \ probabilities, \ superpositions", SPACE),
            (r"where they meet", r"black holes, \ and the first instant: \ a quantum superposition of geometries?",
             BAD),
            (r"the programmes", r"strings and holography; \ loop quantum gravity; \ causal sets; \ asymptotic "
                                r"safety", ABS),
            (r"a warning", r"everything in this chapter is speculative: \ there is no confirmed theory of quantum "
                           r"gravity", LIGHT),
        ]
        g = rows_table(rows, top=1.7, gap=0.48, width=8.4, x_text=-2.2, label_size=22, text_size=21)
        with self.voiceover(
            "This part's last question is about the frontier, and it comes with a warning. "
            "<bookmark mark='a'/>General relativity treats spacetime as a smooth, dynamical field, with no fixed "
            "background. <bookmark mark='b'/>Quantum field theory puts its fields on a fixed spacetime stage. "
            "<bookmark mark='c'/>Where both matter, at black holes and in the first instant, we would need a "
            "superposition of geometries, and neither theory tells us what that is. <bookmark mark='d'/>There are "
            "programmes: string theory and holography, loop quantum gravity, causal sets, asymptotic safety. "
            "<bookmark mark='e'/>Everything in this chapter is speculative. There is no confirmed theory of quantum "
            "gravity."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def holography(self):
        head = label(r"Geometry from entanglement \ (schematic, \ speculative)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        c = np.array([-3.0, -0.6, 0])
        R = 2.4
        rim = Circle(radius=R, color=SPACE, stroke_width=3).move_to(c)
        n = 16
        pts = [c + R * np.array([math.cos(2 * PI * k / n), math.sin(2 * PI * k / n), 0]) for k in range(n)]
        sites = VGroup(*[Dot(p, radius=0.07, color=SPACE) for p in pts])
        links = VGroup()
        for k in range(n):
            for j in (1, 2, 4, 8):
                a, b = pts[k], pts[(k + j) % n]
                if j == 8 and k >= n // 2:
                    continue
                mid = (a + b) / 2
                inward = c + (mid - c) * (0.25 if j == 8 else 0.7 - 0.08 * j)
                links.add(VMobject(stroke_color=LIGHT, stroke_width=1.2 + 0.3 * j, stroke_opacity=0.55
                                   ).set_points_smoothly([a, inward, b]))
        side = stack([(r"holography \ (Maldacena, \ 1997): \ a gravitational theory in a bulk space \ equals a "
                       r"quantum theory without gravity on its boundary", ABS),
                      (r"Ryu and Takayanagi \ (2006): \ entanglement between boundary regions \ measures areas of "
                       r"surfaces in the bulk", LIGHT),
                      (r"Van Raamsdonk \ (2010): \ remove the entanglement, \ and the bulk space comes apart", BAD),
                      (r"ER = EPR \ (Maldacena and Susskind, \ 2013): \ entangled particles, \ joined by tiny "
                       r"wormholes?", CURVE)], font_size=19, aligned_edge=LEFT, width=5.4, buff=0.28).move_to(
            [3.7, -0.4, 0])
        with self.voiceover(
            "One striking idea, drawn here only schematically. <bookmark mark='a'/>In 1997 Juan Maldacena found a "
            "duality: a theory with gravity in a region of space is equivalent to a quantum theory without gravity "
            "living on the region's boundary, like a hologram. <bookmark mark='b'/>In 2006 Shinsei Ryu and Tadashi "
            "Takayanagi showed that the entanglement between parts of the boundary measures the areas of surfaces "
            "deep in the interior. <bookmark mark='c'/>Mark Van Raamsdonk argued in 2010 that if you remove the "
            "entanglement, the interior space comes apart: connected geometry is built from entanglement. "
            "<bookmark mark='d'/>And Maldacena and Leonard Susskind conjectured in 2013 that every pair of entangled "
            "particles is joined by a microscopic wormhole, ER equals EPR. These results hold for model universes "
            "unlike ours; whether they apply to our world is unknown."
        ) as vo:
            self.play(FadeIn(head), Create(rim), FadeIn(sites))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.02), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(links.animate.set_stroke(opacity=0.12), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(links.animate.set_stroke(opacity=0.55), FadeIn(side[3]))
        self.clear_scene()

    def causets(self):
        d = load("causet")
        head = label(r"Order plus number", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        c, half = np.array([-3.6, -0.7, 0]), 2.4             # the diamond's centre and half-height on screen

        def to_screen(t, x):
            return c + np.array([x * 2 * half, (t - 0.5) * 2 * half, 0])

        diamond = Polygon(to_screen(0, 0), to_screen(0.5, 0.5), to_screen(1, 0), to_screen(0.5, -0.5),
                          color=GREY_C, stroke_width=2)
        pts = [to_screen(t, x) for t, x in d["points"]]
        dots = VGroup(*[Dot(p, radius=0.045, color=LIGHT) for p in pts])
        links = VGroup(*[Line(pts[i], pts[j], color=TIME, stroke_width=1.1, stroke_opacity=0.6)
                         for i, j in d["links"]])
        tags = VGroup(label(r"time", font_size=17, color=GREY_A).next_to(diamond, UP, buff=0.1),
                      label(r"%d events, \ %d links" % (len(pts), d["n_links"]), font_size=17,
                            color=GREY_A).next_to(diamond, DOWN, buff=0.12))
        f = MathTex(r"\frac{\#\,\text{related pairs}}{\binom{N}{2}} \;\approx\; \frac{\Gamma(d + 1)\,\Gamma(d/2)}"
                    r"{2\,\Gamma(3d/2)}", font_size=30, color=ABS).move_to([3.3, 1.8, 0])
        rows_d = d["rows"]
        assert [round(r["estimate"]) for r in rows_d] == [2, 3, 4] and d["n"] == 400
        hd = [r"d", r"\text{fraction related}", r"\text{theory}", r"\text{dimension recovered}"]
        rows = [[MathTex(str(r["d"]), font_size=24), MathTex(f"{r['fraction']:.3f}", font_size=24, color=LIGHT),
                 MathTex(f"{r['theory']:.3f}", font_size=24, color=ABS),
                 MathTex(f"{r['estimate']:.2f}", font_size=24, color=OK)] for r in rows_d]
        grid = ValueGrid(hd, rows, col_w=[0.7, 2.0, 1.3, 2.4], cell_h=0.45, font_size=19).move_to([3.3, 0.1, 0])
        gtag = label(r"%d events sprinkled in each dimension; \ coordinates forgotten" % d["n"], font_size=17,
                     color=GREY_A).next_to(grid, DOWN, buff=0.15)
        side = stack([(r"Hawking, \ King and McCarthy \ (1976); \ Malament \ (1977): \ causal order fixes geometry "
                       r"up to scale", HIST),
                      (r"Bombelli, \ Lee, \ Meyer and Sorkin \ (1987): \ at bottom, \ a discrete partial order; "
                       r"\ counting supplies the scale", ABS)], font_size=19, aligned_edge=LEFT, width=6.2,
                     buff=0.25).move_to([3.3, -2.3, 0])
        with self.voiceover(
            "Another programme on that list, causal set theory, makes the idea concrete enough to compute. "
            "<bookmark mark='a'/>In 1987 Luca Bombelli, Joohan Lee, David Meyer and Rafael Sorkin proposed that "
            "spacetime is, at bottom, a discrete set of events with only one relation: which events can influence "
            "which. <bookmark mark='b'/>Why might order be enough? Results by Stephen Hawking, Andrew King and "
            "Patrick McCarthy, and by David Malament, in 1976 and 1977, show that the causal order of a spacetime "
            "fixes its geometry up to a local scale. Counting events supplies the scale: order plus number equals "
            "geometry, in Sorkin's slogan. <bookmark mark='c'/>The Reasoner tests the slogan. It scatters events at "
            "random through a diamond of flat spacetime, keeps only who can signal to whom, and forgets every "
            "coordinate. <bookmark mark='d'/>From the order alone it counts the related pairs. In two dimensions "
            "about half of all pairs are related; in four, about a tenth. Inverting the formula recovers the "
            "dimension: about two, three and four. <bookmark mark='e'/>Dimension, a geometric fact, is read off a "
            "pattern of influence. Whether all of spacetime can be recovered this way, and what space would then "
            "be, is the philosophers' question."
        ) as vo:
            self.play(FadeIn(head), Create(diamond), FadeIn(tags[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.02), run_time=2)
            self.play(LaggedStart(*[Create(l) for l in links], lag_ratio=0.005), FadeIn(tags[1]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeOut(side), Write(f))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(x) for x in grid.cell[r]], run_time=0.5)
            self.play(FadeIn(gtag))
            vo.wait_until("e")
            self.play(Indicate(grid.cell[2][3], color=OK))
        self.clear_scene()

    def philosophy(self):
        head = label(r"What emergence would mean", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the substantivalist", r"the deepest level would have no points at all: \ substantivalism and "
                                     r"relationalism both outdated", SPACE),
            (r"empirical coherence", r"our evidence is observations at places and times: \ can a theory without "
                                     r"spacetime explain them? \ (Huggett and Wüthrich)", BAD),
            (r"functionalism", r"spacetime is whatever plays the spacetime role: \ like a gas's temperature, \ real "
                               r"but not fundamental", OK),
            (r"the old question", r"Leibniz's relations, \ revived at the bottom of physics?", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.4, x_text=-2.2, label_size=22, text_size=21)
        with self.voiceover(
            "If spacetime is emergent, what would that mean? <bookmark mark='a'/>At the deepest level there would be "
            "no points at all, and the old fight between substantivalism and relationalism would be about a "
            "derived, not a fundamental, structure. <bookmark mark='b'/>Nick Huggett and Christian Wüthrich have "
            "pressed a worry: all our evidence consists of observations at places and times. Can a theory without "
            "spacetime even explain the evidence for itself? <bookmark mark='c'/>The likeliest answer is "
            "functionalism: spacetime is whatever plays the spacetime role, as a gas's temperature is whatever plays "
            "the temperature role, real, but not fundamental. <bookmark mark='d'/>If so, Leibniz's idea that space "
            "is an order of relations may come back, at the very bottom of physics."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
