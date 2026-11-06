from __future__ import annotations

from videos.philosophy.philosophy10.common import *  # noqa: F403


class Aesthetic(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Space and time", r"Are space and time out there, \ or in us?", lit=(1781,), part=PART)
        with self.voiceover("Chapter ten. Space and time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.forms()
        self.examples()
        self.hands()
        self.triangle()

    def forms(self):
        head = label(r"The transcendental aesthetic", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"space and time are not things, \ nor relations between things", font_size=26),
            label(r"they are the \textit{forms of intuition}: \ the way anything must be given to us", font_size=26,
                  color=KANT),
            label(r"space: \ the form of outer sense; \ time: \ the form of inner sense", font_size=24, color=GREY_A),
            label(r"we can think space empty of objects, \ but never think away space itself", font_size=24,
                  color=GREY_A),
            label(r"so what is true of space \ is true of everything we can ever perceive", font_size=26,
                  color=GOAL)).arrange(DOWN, buff=0.38).move_to([0, -0.4, 0])
        with self.voiceover(
            "The first part of Kant's answer concerns space and time. <bookmark mark='a'/>Newton thought them real "
            "containers; Leibniz, relations between things. Kant said neither. <bookmark mark='b'/>They are the forms "
            "of intuition: the way anything at all must be given to us. <bookmark mark='c'/>Space is the form of "
            "outer sense, time the form of inner sense. <bookmark mark='d'/>We can imagine space with no objects in "
            "it, Kant observed, but we can never imagine away space itself. <bookmark mark='e'/>So whatever is true of "
            "space in general will be true of everything we can ever perceive, because perceiving is having things in "
            "space. That is why geometry can be known in advance."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def examples(self):
        head = label(r"Kant's two examples", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        left = VGroup(MathTex(r"7 + 5 = 12", font_size=46, color=GOAL),
                      label(r"not in the concept of $7 + 5$", font_size=22, color=GREY_A),
                      label(r"we must count on, \ five units, \ in time", font_size=22, color=GREY_A))
        dots = VGroup(*[Dot(radius=0.09, color=REASON) for _ in range(7)],
                      *[Dot(radius=0.09, color=SENSE) for _ in range(5)]).arrange(RIGHT, buff=0.18)
        left.add(dots)
        left.arrange(DOWN, buff=0.25)
        right = VGroup(MathTex(r"\alpha + \beta + \gamma = 180^\circ", font_size=40, color=GOAL),
                       label(r"not in the concept of a triangle", font_size=22, color=GREY_A),
                       label(r"we must draw, \ in space, \ a parallel through a corner", font_size=22,
                             color=GREY_A))
        A, B, C = np.array([-1.2, -0.5, 0]), np.array([1.2, -0.5, 0]), np.array([0.3, 0.9, 0])
        tri = VGroup(Polygon(A, B, C, stroke_color=KANT, stroke_width=3),
                     Line(C + LEFT * 1.6, C + RIGHT * 1.6, color=GREY_B, stroke_width=2))
        right.add(tri.scale(0.8))
        right.arrange(DOWN, buff=0.25)
        cols = VGroup(left, right).arrange(RIGHT, buff=1.4).move_to([0, -0.2, 0])
        with self.voiceover(
            "Kant gave two examples. <bookmark mark='a'/>Seven plus five equals twelve. The concept of the sum of "
            "seven and five contains only the union of the two numbers, not which number results. To get twelve, we "
            "must count on, five units, one after another, in time. So arithmetic is synthetic, and a priori because "
            "time is our form. <bookmark mark='b'/>And the angles of a triangle sum to two right angles. Nothing in "
            "the concept of a three-sided figure says so. We must construct: draw the triangle, and a line through one "
            "corner parallel to the opposite side, in space. So geometry is synthetic a priori, because space is our "
            "form, and every triangle we will ever meet is in it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left[:3]), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(right[:3]), Create(tri))
        self.clear_scene()

    def hands(self):
        d = load("hands")
        hc = history_card(1768, r"Immanuel Kant", r"`On the first ground of the distinction of regions in space'",
                          width=5.8, color=HIST).to_corner(UL, buff=0.35)
        u = 0.45

        def shape(cells, color, origin):
            return VGroup(*[Square(side_length=u, stroke_color=WHITE, stroke_width=1.5, fill_color=color,
                                   fill_opacity=0.7).move_to(origin + u * np.array([x, y, 0])) for x, y in cells])
        left = shape(d["cells"], SENSE, np.array([-4.6, -1.4, 0]))
        right = shape([(-x, y) for x, y in d["cells"]], REASON, np.array([-1.2, -1.4, 0]))
        ll = label(r"a left hand", font_size=20, color=SENSE).next_to(left, DOWN, buff=0.2)
        rl = label(r"its mirror image", font_size=20, color=REASON).next_to(right, DOWN, buff=0.2)
        ghost = left.copy().set_opacity(0.35)
        assert not any(d["rotations_match"]) and d["flip_matches"]
        rows = VGroup(
            label(r"the Reasoner tries all four rotations in the plane: \ none matches", font_size=22, color=BAD),
            label(r"a turn through the third dimension does", font_size=22, color=OK),
            VGroup(label(r"a left and a right hand: \ every internal relation the same,", font_size=22, color=GOAL),
                   label(r"yet they differ", font_size=22, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"Kant (1768): \ against Leibniz, \ space is more than relations", font_size=22,
                         color=KANT),
                   label(r"later (1783): \ evidence that space is a form of intuition", font_size=22,
                         color=KANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        for r in rows:
            if r.width > 6.6:
                r.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.next_to(right, RIGHT, buff=0.9).set_y(-0.9)
        if rows.get_right()[0] > 6.9:
            rows.shift(LEFT * (rows.get_right()[0] - 6.9))
        with self.voiceover(
            "Kant had a striking example about space, from 1768. <bookmark mark='a'/>Take a flat hand, and its mirror "
            "image. <bookmark mark='b'/>The Reasoner tries every rotation of one in the plane against the other: four "
            "rotations, and none matches. <bookmark mark='c'/>Only a turn through the third dimension, flipping it "
            "over, brings them together. <bookmark mark='d'/>A left and a right hand are alike in every internal "
            "relation, every length and every angle, yet they are different, and no amount of turning makes one the "
            "other. <bookmark mark='e'/>In 1768 Kant took this to show, against Leibniz, that space is more than "
            "relations between things. Later, in the Prolegomena, he took it as evidence that space is a form of our "
            "intuition, not a property of things in themselves."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(ll), FadeIn(right), FadeIn(rl))
            vo.wait_until("b")
            self.add(ghost)
            for _ in range(4):
                self.play(Rotate(ghost, PI / 2), run_time=0.7)
            self.play(ghost.animate.move_to(right.get_center()), run_time=0.8)
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(ghost.animate.stretch(-1, 0), run_time=1.2)
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def triangle(self):
        d = load("gauss")
        head = label(r"A triangle with three right angles", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        R = 2.0
        c0 = np.array([-3.6, -0.6, 0])
        sphere = Circle(radius=R, color=GREY_C, stroke_width=2).move_to(c0)
        eq = Ellipse(width=2 * R, height=0.7, color=GREY_D, stroke_width=1.5).move_to(c0)
        N = c0 + UP * R
        E1 = c0 + np.array([-R * 0.72, -0.24, 0])
        E2 = c0 + np.array([R * 0.72, -0.24, 0])
        arc1 = ArcBetweenPoints(N, E1, angle=0.55, color=GOAL, stroke_width=4)
        arc2 = ArcBetweenPoints(N, E2, angle=-0.55, color=GOAL, stroke_width=4)
        arc3 = ArcBetweenPoints(E1, E2, angle=0.5, color=GOAL, stroke_width=4)
        tri = VGroup(arc1, arc2, arc3)
        rows = VGroup(
            label(r"on a sphere, \ from the pole to the equator, \ a quarter turn along it, \ and back:", font_size=22),
            MathTex(r"90^\circ + 90^\circ + 90^\circ = 270^\circ", font_size=36, color=GOAL),
            label(r"the excess over $180^\circ$ \ = \ area $\div R^2$: \ bigger triangles, \ bigger excess",
                  font_size=22, color=GREY_A),
            label(r"Gauss's survey, \ 1820s: \ Brocken, \ Hohehagen, \ Inselsberg", font_size=22, color=HIST),
            label(rf"the Reasoner: \ on the earth's curved surface, \ excess "
                  rf"{d['excess_arcsec']:.1f}$''$ \ (about $1/240$ of a degree)", font_size=21, color=OK),
            label(r"too small to see, \ and a test of the surface, \ not of space: \ Kant's question was untouched",
                  font_size=21, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -0.4, 0])
        for x in rows:
            if x.width > 7.0:
                x.width = 7.0
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -0.4, 0])
        with self.voiceover(
            "Is the angle sum really fixed in advance? On a curved surface it is not. <bookmark mark='a'/>Walk on a "
            "sphere from the north pole down to the equator, turn a right angle, go a quarter of the way round, turn "
            "again, and walk back to the pole. <bookmark mark='b'/>The triangle has three right angles: two hundred "
            "and seventy degrees. <bookmark mark='c'/>The excess over a hundred and eighty is the triangle's area "
            "divided by the square of the radius, so bigger triangles show it more. <bookmark mark='d'/>Carl "
            "Friedrich Gauss, surveying Hanover in the 1820s, measured a great triangle between three mountain tops. "
            "<bookmark mark='e'/>The Reasoner works out its spherical excess on the curved surface of the earth: "
            "about fifteen seconds of arc, roughly a two-hundred-and-fortieth of a degree. <bookmark mark='f'/>That "
            "was close to the limit of his instruments, and it concerns the earth's surface, not space itself. "
            "Whether Gauss meant to test the geometry of space is debated; either way, Kant's question was untouched "
            "until Einstein."
        ) as vo:
            self.play(FadeIn(head), Create(sphere), Create(eq))
            vo.wait_until("a")
            self.play(Create(arc1), FadeIn(rows[0]))
            self.play(Create(arc3))
            self.play(Create(arc2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Indicate(tri, color=GOAL))
            for mk, r in zip("cdef", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
