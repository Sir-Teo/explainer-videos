from __future__ import annotations

from videos.philosophy.philosophy25.common import *  # noqa: F403


class Hole(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"The hole argument", r"Are spacetime points real things?", lit=(1913, 1987),
                            part=PART)
        with self.voiceover("Chapter eleven. The hole argument."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.gr()
        self.deform()
        self.dilemma()
        self.price()
        self.wall_brick()

    def gr(self):
        hc = history_card(1915, r"Albert Einstein", r"the field equations of general relativity", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        f = MathTex(r"G_{\mu\nu} = 8\pi G\, T_{\mu\nu}", font_size=48, color=CURVE).move_to([0, 1.2, 0])
        rows = stack([(r"left: \ the curvature of spacetime, \ from the metric $g$", CURVE),
                      (r"right: \ the matter and energy in it", MATTER),
                      (r"`matter tells spacetime how to curve; \ spacetime tells matter how to move' \ (Wheeler)",
                       WHITE),
                      (r"and the equations take the same form in every coordinate system: \ general covariance", ABS)],
                     font_size=22, aligned_edge=LEFT, width=11.4, buff=0.32).move_to([0, -1.2, 0])
        with self.voiceover(
            "General relativity, completed by Einstein in 1915, makes geometry dynamical. <bookmark mark='a'/>The "
            "field equations set the curvature of spacetime, built from a metric field g, <bookmark mark='b'/>equal "
            "to the matter and energy it contains. <bookmark mark='c'/>John Wheeler's summary: matter tells "
            "spacetime how to curve; spacetime tells matter how to move. <bookmark mark='d'/>And the equations take "
            "the same form in every coordinate system, a property called general covariance. Two years earlier, "
            "general covariance had made Einstein despair."
        ) as vo:
            self.play(FadeIn(hc), Write(f))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def deform(self):
        d = load("hole")
        head = label(r"A hole, \ and a smooth shuffle inside it", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        c = np.array([-3.0, -0.6, 0])
        sc = 1.6
        bump = ValueTracker(0.0)
        R = d["radius"]

        def phi(x, y, b):
            r = math.hypot(x, y)
            if r >= R:
                return x, y
            s = (1 - (r / R) ** 2) ** 3
            a = b * 2 * math.pi * s
            return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)

        def grid():
            b = bump.get_value()
            g = VGroup()
            ts = np.linspace(-1.5, 1.5, 61)
            for k in np.linspace(-1.5, 1.5, 11):
                for pts in ([phi(float(k), float(t), b) for t in ts], [phi(float(t), float(k), b) for t in ts]):
                    g.add(VMobject(stroke_color=SPACE, stroke_width=1.6).set_points_as_corners(
                        [c + sc * np.array([x, y, 0]) for x, y in pts]))
            return g

        mesh = always_redraw(grid)
        hole = Circle(radius=R * sc, color=CURVE, stroke_width=3).move_to(c)
        hl = label(r"the hole", font_size=19, color=CURVE).next_to(hole, UP, buff=0.1)
        star = always_redraw(lambda: Dot(c + sc * np.array(phi(0.35, 0.2, bump.get_value()) + (0,)), radius=0.1,
                                         color=MATTER))
        side = stack([(r"a solution: \ a metric and matter fields, \ laid out over the points", WHITE),
                      (r"push every field around inside the hole, \ smoothly; \ leave everything outside alone", CURVE),
                      (r"by general covariance, \ the result is also a solution", ABS),
                      (r"outside the hole, \ and before it, \ the two agree everywhere", OK),
                      (r"inside, \ the orange event's fields sit at a different point", MATTER)], font_size=20,
                     aligned_edge=LEFT, width=5.6, buff=0.28).move_to([3.6, -0.4, 0])
        assert d["outside_fixed"]
        with self.voiceover(
            "In 1913 Einstein gave an argument against general covariance, and two years later he found the flaw in "
            "it. John Earman and John Norton revived it in 1987 as an argument about what spacetime is. "
            "<bookmark mark='a'/>Take a solution of the equations: a metric and matter fields, laid out over the "
            "points of spacetime. Pick a region, the hole. <bookmark mark='b'/>Now push every field around inside "
            "the hole, smoothly, while leaving everything outside exactly where it was. <bookmark mark='c'/>Because "
            "the equations are generally covariant, the shuffled fields are also a solution. "
            "<bookmark mark='d'/>The two solutions agree everywhere outside the hole, and in particular at every time "
            "before it. <bookmark mark='e'/>But inside, they differ about which point has which field: the orange "
            "event's matter now sits at a different point."
        ) as vo:
            self.play(FadeIn(head), FadeIn(mesh), FadeIn(star))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Create(hole), FadeIn(hl))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), bump.animate.set_value(d["radius"] * 0.35), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Indicate(star, color=MATTER))
        mesh.clear_updaters()
        star.clear_updaters()
        self.clear_scene()

    def dilemma(self):
        head = label(r"Earman and Norton's dilemma", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = stack([(r"substantivalism: \ spacetime points exist in their own right, \ with their own identities",
                        SPACE),
                       (r"then the two solutions describe different possible worlds: \ which point has which field "
                        r"differs", CURVE),
                       (r"they agree up to the hole: \ so the past, \ with the laws, \ does not fix what happens in "
                        r"the hole", BAD),
                       (r"so substantivalism makes general relativity indeterministic, \ for a reason no experiment "
                        r"could detect", BAD),
                       (r"Earman and Norton: \ that is too high a price; \ give up substantivalism", ABS)],
                      font_size=22, aligned_edge=LEFT, width=11.6, buff=0.32).move_to([0, -0.2, 0])
        with self.voiceover(
            "Here is the dilemma. <bookmark mark='a'/>Substantivalism, Newton's heir, says that spacetime points "
            "exist in their own right and have their own identities. <bookmark mark='b'/>Then the two solutions "
            "describe different possible worlds, because they differ about which point has which field. "
            "<bookmark mark='c'/>But they agree everywhere up to the hole. So the whole past, together with the laws, "
            "fails to determine what happens in the hole. <bookmark mark='d'/>Substantivalism makes general "
            "relativity indeterministic, and for a reason no experiment could ever detect, since the two worlds look "
            "exactly alike. <bookmark mark='e'/>Earman and Norton concluded that this price is too high, and that we "
            "should give up substantivalism."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        d = load("holepl")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(d["mcs"]) == [["D"], ["M"], ["P"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.6, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ the hole")
        positions = [(("M",), r"sophisticated substantivalism", r"points are real, \ but diffeomorphic models "
                                                                 r"are one world \ (Leibniz equivalence)"),
                     (("P",), r"relationalism", r"no points in their own right; \ only the fields and their "
                                               r"relations"),
                     (("D",), r"accept indeterminism", r"the hole is open: \ a bullet few will bite")]
        with self.voiceover(
            "Make it a Price List. <bookmark mark='a'/>Spacetime points are real things with identities of their "
            "own. General relativity is deterministic. And diffeomorphic models, the shuffled and the unshuffled, "
            "represent different possible worlds. <bookmark mark='b'/>The hole argument shows the three cannot all "
            "hold. <bookmark mark='c'/>The most popular position gives up the third: sophisticated substantivalism. "
            "Points are real, but two models related by a diffeomorphism represent one and the same world; this is "
            "Leibniz equivalence, the shift argument's conclusion, turned into a principle. "
            "<bookmark mark='d'/>Relationalists give up the first: there are no points in their own right, only "
            "the fields and their relations. <bookmark mark='e'/>And almost no one gives up the second, accepting an "
            "undetectable indeterminism."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.2)
                self.play(*anims)
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=25, current=25).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(25, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the twenty-fifth brick in the Wall. <bookmark mark='a'/>The dream was spacetime points as real "
            "things in a deterministic theory. The hole argument blocks it. <bookmark mark='b'/>The way through is "
            "a choice: sophisticated substantivalism, which counts shuffled models as one world, or relationalism, "
            "which never had the points. The next chapter builds the relationalist's best attempt."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[25], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()
