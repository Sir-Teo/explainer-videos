from __future__ import annotations

from videos.philosophy.philosophy9.common import *  # noqa: F403


def poly(pts, origin, u, color, op=0.55, width=2):
    return Polygon(*[origin + u * np.array([x, y, 0]) for x, y in pts], stroke_color=WHITE, stroke_width=width,
                   fill_color=color, fill_opacity=op)


def cells(cs, origin, u, color):
    return VGroup(*[poly([(x, y), (x + 1, y), (x + 1, y + 1), (x, y + 1)], origin, u, color, 0.7, 1) for x, y in cs])


class Pictures(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Pictures that prove, \ pictures that lie", r"Can a picture be a proof?", lit=(263,),
                            part=PART)
        with self.voiceover("Chapter fifteen. Pictures that prove, and pictures that lie."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.gougu()
        self.explain()
        self.missing()
        self.euclid()

    def gougu(self):
        a, b = 1.2, 2.0
        s = a + b
        u = 1.1
        o = np.array([-6.0, -2.0, 0])
        frame = poly([(0, 0), (s, 0), (s, s), (0, s)], o, u, BLACK, 0.0, 2.5)
        t1 = [[(0, 0), (a, 0), (0, b)], [(s, 0), (s, a), (a, 0)], [(s, s), (b, s), (s, a)], [(0, s), (0, b), (b, s)]]
        t2 = [[(a, 0), (s, 0), (s, a)], [(a, 0), (s, a), (a, a)], [(0, a), (a, s), (0, s)], [(0, a), (a, a), (a, s)]]
        cols = [CONCRETE, OK, ABSTRACT, PROOF]
        tris = VGroup(*[poly(t, o, u, c) for t, c in zip(t1, cols)])
        tris2 = VGroup(*[poly(t, o, u, c) for t, c in zip(t2, cols)])
        csq = poly([(a, 0), (s, a), (b, s), (0, b)], o, u, NUM, 0.25, 0)
        asq = poly([(0, 0), (a, 0), (a, a), (0, a)], o, u, NUM, 0.25, 0)
        bsq = poly([(a, a), (s, a), (s, s), (a, s)], o, u, NUM, 0.25, 0)
        lc = MathTex("c^2", font_size=34, color=NUM).move_to(csq)
        la = MathTex("a^2", font_size=30, color=NUM).move_to(asq)
        lb = MathTex("b^2", font_size=34, color=NUM).move_to(bsq)
        hc = history_card(263, r"Liu Hui", r"commentary on the \textit{Nine Chapters}: \ `out and in complement each "
                          r"other'", width=6.0, color=HIST).to_corner(UR, buff=0.35)
        rows = VGroup(label(r"the \textit{Zhoubi suanjing}'s hypotenuse diagram; \ Bhāskara's `Behold!'", font_size=22,
                            color=GREY_A),
                      label(r"four copies of one right triangle, \ inside a square of side $a + b$", font_size=22),
                      label(r"what is left: \ the square on the hypotenuse", font_size=22, color=NUM),
                      label(r"move the triangles: \ what is left is $a^2 + b^2$", font_size=22, color=NUM),
                      MathTex(r"a^2 + b^2 = c^2", font_size=40, color=OK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.3).move_to([2.9, -0.8, 0])
        with self.voiceover(
            "Can a picture prove something? Mathematicians in China and India thought so. <bookmark mark='a'/>The "
            "Chinese classic Zhoubi suanjing has a diagram for the hypotenuse, and in 263 Liu Hui, commenting on "
            "the Nine Chapters, stated the principle behind it: what goes out and what comes in complement each "
            "other. Cut a figure up and move the pieces, and the area stays the same. <bookmark mark='b'/>Take four "
            "copies of a right triangle with sides a and b, inside a square of side a plus b. <bookmark mark='c'/>"
            "What is left over is the square on the hypotenuse, c squared. <bookmark mark='d'/>Now move the "
            "triangles. The same square, the same four triangles, and what is left over is a square of side a and a "
            "square of side b. <bookmark mark='e'/>So a squared plus b squared is c squared. The story goes that "
            "Bhāskara, in twelfth-century India, gave a proof like this with a picture and a single word: Behold."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(frame), FadeIn(tris), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(csq), FadeIn(lc), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeOut(csq), FadeOut(lc))
            self.play(LaggedStart(*[Transform(x, y) for x, y in zip(tris, tris2)], lag_ratio=0.4), run_time=4)
            self.play(FadeIn(asq), FadeIn(bsq), FadeIn(la), FadeIn(lb), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(Write(rows[4]))
        self.clear_scene()

    def explain(self):
        d = M.odd_squares(5)
        head = label(r"Proofs that verify, \ and proofs that explain", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        u = 0.42
        o = np.array([-5.6, -2.4, 0])
        layers = VGroup()
        cols = [NUM, OK, ABSTRACT, PROOF, CONCRETE]
        for k in range(1, 6):
            cs = [(x, k - 1) for x in range(k)] + [(k - 1, y) for y in range(k - 1)]
            layers.add(cells(cs, o, u, cols[k - 1]))
        eq = MathTex(r"1 + 3 + 5 + 7 + 9 = 25 = 5^2", font_size=32, color=NUM).next_to(layers, UP, buff=0.35).align_to(
            layers, LEFT)
        assert d[-1] == (5, 25)
        ind = VGroup(label(r"by induction: \ if $1 + \dots + (2k - 1) = k^2$, \ add $2k + 1$ \ to get $(k + 1)^2$",
                           font_size=22, color=GREY_A),
                     label(r"correct, \ but it does not say \textit{why}", font_size=22, color=BAD),
                     label(r"the picture: \ each odd number is one more L around the last square", font_size=22,
                           color=OK),
                     VGroup(label(r"Steiner (1978); \ Lange, \textit{Because Without Cause} (2017):", font_size=21,
                                  color=GREY_B),
                            label(r"some proofs explain, \ some only verify", font_size=21, color=GREY_B)).arrange(
                         DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        for x in ind:
            if x.width > 6.6:
                x.width = 6.6
        ind.arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0.0, -1.0, 0], aligned_edge=LEFT)
        with self.voiceover(
            "Pictures can do something proofs by symbols often do not: explain. <bookmark mark='a'/>The odd numbers "
            "add up to squares: one plus three plus five plus seven plus nine is twenty-five. <bookmark mark='b'/>"
            "Induction proves it: if the first k odd numbers make k squared, adding the next gives k plus one "
            "squared. <bookmark mark='c'/>Correct, but it does not show why. <bookmark mark='d'/>The picture does: "
            "each odd number is one more L-shaped layer wrapped around the last square. <bookmark mark='e'/>Mark "
            "Steiner in 1978, and Marc Lange more recently, have studied what makes some proofs explain why a "
            "theorem is true, while others only make sure that it is."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(L) for L in layers], lag_ratio=0.5), FadeIn(eq), run_time=4)
            for mk, r in zip("bcde", ind):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def missing(self):
        d = load("missing")
        head = label(r"Curry's missing square", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        u = 0.44
        o1 = np.array([-6.4, 0.3, 0])
        o2 = np.array([0.6, 0.3, 0])
        red, blue, orange, green = BAD, ABSTRACT, CONCRETE, OK
        orange_c = [(x, 0) for x in range(5)] + [(0, 1), (1, 1)]
        green_c = [(2, 0), (3, 0), (4, 0)] + [(x, 1) for x in range(5)]

        def arrangement(o, which):
            grid = VGroup(*[Line(o + u * np.array([x, 0, 0]), o + u * np.array([x, 5, 0]), color=GREY_D,
                                 stroke_width=1) for x in range(14)],
                          *[Line(o + u * np.array([0, y, 0]), o + u * np.array([13, y, 0]), color=GREY_D,
                                 stroke_width=1) for y in range(6)])
            if which == 1:
                pieces = VGroup(poly([(0, 0), (8, 0), (8, 3)], o, u, red), poly([(8, 3), (13, 3), (13, 5)], o, u, blue),
                                cells([(8 + x, y) for x, y in orange_c], o, u, orange),
                                cells([(8 + x, 1 + y) for x, y in green_c], o, u, green))
            else:
                pieces = VGroup(poly([(5, 2), (13, 2), (13, 5)], o, u, red), poly([(0, 0), (5, 0), (5, 2)], o, u, blue),
                                cells([(5 + x, y) for x, y in orange_c], o, u, orange),
                                cells([(8 + x, y) for x, y in green_c], o, u, green))
            return grid, pieces
        g1, p1 = arrangement(o1, 1)
        g2, p2 = arrangement(o2, 2)
        hole = Square(side_length=u, stroke_color=GOAL, stroke_width=4).move_to(o2 + u * np.array([7.5, 1.5, 0]))
        diag1 = DashedLine(o1, o1 + u * np.array([13, 5, 0]), color=WHITE, stroke_width=2)
        diag2 = DashedLine(o2, o2 + u * np.array([13, 5, 0]), color=WHITE, stroke_width=2)
        assert d["figure2"] == "33" and d["pieces"] == "32" and not d["equal"]
        rows = VGroup(
            label(r"the same four pieces, \ in two `13 by 5 triangles'; \ the second has a hole", font_size=22),
            label(rf"slopes: \ red ${d['slopes'][0]} = 0.375$, \ blue ${d['slopes'][1]} = 0.4$, \ the diagonal "
                  rf"${d['slopes'][2]} \approx 0.385$", font_size=22, color=GOAL),
            label(r"neither `hypotenuse' is straight: \ one sags, \ one bulges, \ by half a square each", font_size=22,
                  color=BAD),
            label(rf"areas: \ pieces {d['pieces']}, \ outlines {d['figure1']} and {d['figure2']}, \ the true triangle "
                  rf"$32\tfrac{{1}}{{2}}$", font_size=22, color=OK),
            label(r"Paul Curry, \ an amateur magician, \ 1953 \ (no relation to Haskell)", font_size=20,
                  color=GREY_B)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Pictures can also lie. <bookmark mark='a'/>Here are four pieces: a red triangle, a blue triangle, and two "
            "L-shaped pieces. Arranged one way, they make a triangle thirteen squares wide and five high. "
            "<bookmark mark='b'/>Arranged the other way, the same pieces make the same triangle, with one square "
            "missing. Where did it go? <bookmark mark='c'/>The Reasoner computes the slopes. The red triangle rises "
            "three in eight; the blue one, two in five; the true diagonal, five in thirteen. They are all different, "
            "so neither long side is straight. <bookmark mark='d'/>Draw the true diagonal: the first figure sags "
            "below it, the second bulges above it, each by half a square. <bookmark mark='e'/>The pieces have area "
            "thirty-two; the outlines thirty-two and thirty-three; the true triangle thirty-two and a half. The eye "
            "cannot see a bend of a few hundredths. <bookmark mark='f'/>The puzzle was invented in 1953 by Paul "
            "Curry, an amateur magician, no relation to Haskell."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g1), LaggedStart(*[FadeIn(p) for p in p1], lag_ratio=0.3), FadeIn(rows[0]), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(g2), LaggedStart(*[FadeIn(p) for p in p2], lag_ratio=0.3), run_time=3)
            self.play(Create(hole))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(Create(diag1), Create(diag2), FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def euclid(self):
        head = label(r"Euclid's first proposition", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        A, B = np.array([-5.2, -0.8, 0]), np.array([-3.6, -0.8, 0])
        r = 1.6
        c1 = Circle(radius=r, color=ABSTRACT, stroke_width=2.5).move_to(A)
        c2 = Circle(radius=r, color=CONCRETE, stroke_width=2.5).move_to(B)
        C = (A + B) / 2 + UP * r * np.sqrt(3) / 2
        tri = Polygon(A, B, C, stroke_color=NUM, stroke_width=3)
        dots = VGroup(*[Dot(p, radius=0.07, color=WHITE) for p in (A, B, C)])
        ls = VGroup(MathTex("A", font_size=28).next_to(A, DL, buff=0.1), MathTex("B", font_size=28).next_to(B, DR,
                                                                                                          buff=0.1),
                    MathTex("C", font_size=28, color=GOAL).next_to(C, UP, buff=0.12))
        rows = VGroup(
            label(r"on segment $AB$, \ draw two circles; \ where they meet, \ $C$", font_size=22),
            label(r"the picture shows that they meet; \ the axioms never say so", font_size=22, color=GOAL),
            label(r"in the plane of rational points, \ every postulate holds, \ and they miss:", font_size=22),
            label(r"$C = (\tfrac{1}{2}, \tfrac{\sqrt{3}}{2})$ \ for $A = (0, 0)$, $B = (1, 0)$, \ and $\sqrt{3}$ is "
                  r"irrational", font_size=22, color=BAD),
            label(r"Pasch (1882), \ Hilbert (1899): \ add axioms of order and continuity", font_size=22, color=OK),
            VGroup(label(r"Manders: \ Euclid reads off a figure only what survives small errors", font_size=21,
                         color=GREY_A),
                   label(r"(which regions meet), \ never exact sizes", font_size=21, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.08)).arrange(DOWN, aligned_edge=LEFT,
                                                                            buff=0.25)
        for x in rows:
            if x.width > 7.0:
                x.width = 7.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.8, -0.4, 0])
        with self.voiceover(
            "Even Euclid leaned on a picture. <bookmark mark='a'/>His very first proposition builds an equilateral "
            "triangle: on a segment A B, draw the circle about A through B, and the circle about B through A. Where "
            "they meet is the third corner, C. <bookmark mark='b'/>The picture shows that the circles meet, but none "
            "of Euclid's axioms says so. <bookmark mark='c'/>In fact, take the plane of points with rational "
            "coordinates. Every one of Euclid's postulates holds there, and the circles miss each other, because the "
            "point where they should meet has a coordinate of root three over two, which is irrational. "
            "<bookmark mark='d'/>Moritz Pasch in 1882 and Hilbert in 1899 added the missing axioms of order and "
            "continuity. <bookmark mark='e'/>And Kenneth Manders showed that Euclid's use of diagrams was "
            "disciplined: he read off a figure only what survives small errors of drawing, such as which regions "
            "meet or contain each other, never exact sizes. A formal system built on that idea now checks Euclid's "
            "proofs, diagrams and all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(dots[:2]), FadeIn(ls[:2]), Create(c1), Create(c2), FadeIn(rows[0]))
            self.play(FadeIn(dots[2]), FadeIn(ls[2]), Create(tri))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
        self.clear_scene()
