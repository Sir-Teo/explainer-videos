from __future__ import annotations

from videos.philosophy.philosophy13.common import *  # noqa: F403


def proj2(x: float, y: float) -> tuple[float, float]:
    """The closest point to (x, y) on the segment x + y = 1, 0 <= x <= 1."""
    a = min(max(x - (x + y - 1) / 2, 0.0), 1.0)
    return a, 1 - a


def brier2(x, y, world_a: bool) -> float:
    return (x - 1) ** 2 + y ** 2 if world_a else x ** 2 + (y - 1) ** 2


class Accuracy(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Closer to the truth", r"Can incoherence be faulted without a bookie?",
                            lit=(1950, 1998), part=PART)
        with self.voiceover("Chapter three. Closer to the truth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.inaccuracy()
        self.dominance()
        self.three()
        self.theorem()

    def inaccuracy(self):
        hc = history_card(1998, r"James Joyce", r"`A Nonpragmatic Vindication of Probabilism'", width=6.6,
                          color=HIST).to_corner(UL, buff=0.35)
        goal = label(r"the aim of belief is truth: \ credence 1 in truths, \ 0 in falsehoods", font_size=25,
                     color=GOAL).next_to(hc, DOWN, buff=0.4).set_x(0)
        brier = MathTex(r"\mathcal{I}(c, w) \;=\; \sum_{X} \bigl(c(X) - \mathbf{1}_X(w)\bigr)^2", font_size=40)
        brier.next_to(goal, DOWN, buff=0.45)
        bl = label(r"the Brier score \ (Glenn Brier, \ 1950, \ for weather forecasts)", font_size=22,
                   color=GREY_A).next_to(brier, DOWN, buff=0.25)
        ex = VGroup(MathTex(r"c(\text{rain}) = 0.7:", font_size=30, color=CRED),
                    MathTex(r"\text{rain: } (0.7-1)^2 + (0.3-0)^2 = 0.18", font_size=28, color=OK),
                    MathTex(r"\text{dry: } (0.7-0)^2 + (0.3-1)^2 = 0.98", font_size=28, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2).next_to(bl, DOWN, buff=0.4)
        foot = label(r"geometrically: \ squared distance from your point to the corner of the true world",
                     font_size=23, color=COH).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1998 James Joyce gave an argument for probabilism with no bets in it. <bookmark mark='a'/>Belief aims "
            "at truth. The ideal credence gives one to every truth and zero to every falsehood; the closer you are to "
            "that, the more accurate. <bookmark mark='b'/>Measure inaccuracy by the Brier score: the sum, over the "
            "propositions, of the squared gap between your credence and the truth value. <bookmark mark='c'/>Glenn "
            "Brier introduced it in 1950 to score weather forecasters. <bookmark mark='d'/>With credence point seven "
            "in rain, and point three in dry: if it rains, your inaccuracy is point one eight; if it stays dry, point "
            "nine eight. <bookmark mark='e'/>Geometrically, it is the squared distance from your credence point to "
            "the corner of the true world."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(goal))
            vo.wait_until("b")
            self.play(Write(brier))
            vo.wait_until("c")
            self.play(FadeIn(bl))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.4))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def dominance(self):
        d = load("accuracy")
        head = label(r"Accuracy dominance", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        pl = Plane2(center=[-3.7, -0.5, 0], size=3.5)
        vA, vN = pl.p(1, 0), pl.p(0, 1)
        tx, ty = ValueTracker(d["two"]["incoherent"][0]), ValueTracker(d["two"]["incoherent"][1])

        def cpt():
            return pl.p(tx.get_value(), ty.get_value())

        def ppt():
            return pl.p(*proj2(tx.get_value(), ty.get_value()))

        dot_c = always_redraw(lambda: Dot(cpt(), color=INC, radius=0.09))
        dot_p = always_redraw(lambda: Dot(ppt(), color=COH, radius=0.09))
        link = always_redraw(lambda: DashedLine(cpt(), ppt(), color=GREY_B, stroke_width=2))
        circA = always_redraw(lambda: Arc(radius=np.linalg.norm(cpt() - vA), start_angle=PI / 2, angle=PI / 2,
                                          arc_center=vA, color=WORLD_C[0], stroke_width=2.5))
        circN = always_redraw(lambda: Arc(radius=np.linalg.norm(cpt() - vN), start_angle=-PI / 2, angle=PI / 2,
                                          arc_center=vN, color=WORLD_C[1], stroke_width=2.5))
        lc = always_redraw(lambda: MathTex(r"c", font_size=26, color=INC).next_to(dot_c, UR, buff=0.04))
        lp = always_redraw(lambda: MathTex(r"c^{*}", font_size=26, color=COH).next_to(dot_p, DL, buff=0.04))

        def tbl_pos(m, r, col):
            return m.move_to([2.1 + col * 2.0, 1.0 - r * 0.6, 0])

        hdr = VGroup(label(r"inaccuracy", font_size=22, color=GREY_A).move_to([0.6, 1.6, 0]),
                     label(r"if $A$", font_size=24, color=WORLD_C[0]).move_to([2.1, 1.6, 0]),
                     label(r"if $\lnot A$", font_size=24, color=WORLD_C[1]).move_to([4.1, 1.6, 0]))
        names = VGroup(label(r"$c$ \ (incoherent)", font_size=22, color=INC).move_to([0.6, 1.0, 0]),
                       label(r"$c^{*}$ \ (projected)", font_size=22, color=COH).move_to([0.6, 0.4, 0]))
        vals = VGroup(
            always_redraw(lambda: tbl_pos(DecimalNumber(brier2(tx.get_value(), ty.get_value(), True),
                                                        num_decimal_places=3, font_size=28, color=INC), 0, 0)),
            always_redraw(lambda: tbl_pos(DecimalNumber(brier2(tx.get_value(), ty.get_value(), False),
                                                        num_decimal_places=3, font_size=28, color=INC), 0, 1)),
            always_redraw(lambda: tbl_pos(DecimalNumber(brier2(*proj2(tx.get_value(), ty.get_value()), True),
                                                        num_decimal_places=3, font_size=28, color=COH), 1, 0)),
            always_redraw(lambda: tbl_pos(DecimalNumber(brier2(*proj2(tx.get_value(), ty.get_value()), False),
                                                        num_decimal_places=3, font_size=28, color=COH), 1, 1)))
        notes = stack([(r"$c^{*}$ lies inside both arcs: \ closer to \textit{both} corners", COH),
                       (r"Pythagoras: \ $|c - v|^2 \geq |c - c^{*}|^2 + |c^{*} - v|^2$", WHITE),
                       (r"so $c^{*}$ is more accurate than $c$ \ in every world", GOAL)], font_size=23,
                      aligned_edge=LEFT).move_to([2.8, -1.4, 0])
        with self.voiceover(
            "Now the theorem. <bookmark mark='a'/>Take the incoherent credences from the Dutch book: point six and "
            "point six. Its inaccuracy in each world is the squared distance to that world's corner. Draw a circle "
            "around each corner, through the point. <bookmark mark='b'/>Now project the point onto the coherent line: "
            "one half, one half. The projection lies inside both circles. It is closer to both corners. "
            "<bookmark mark='c'/>Point five two becomes point five, in each world. Whatever the truth turns out to "
            "be, the coherent credence is more accurate. <bookmark mark='d'/>Move the incoherent point anywhere. "
            "Point eight and point five: the projection is point six five, point three five, and again it wins in "
            "both worlds. <bookmark mark='e'/>Anywhere off the line, the same thing happens. The reason is "
            "Pythagoras: the angle at the projection, between the point and any corner, is right or obtuse, so the "
            "corner is closer to the projection than to the point. <bookmark mark='f'/>An incoherent credence is "
            "accuracy-dominated: some coherent credence is more accurate in every possible world."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pl))
            vo.wait_until("a")
            self.play(FadeIn(dot_c), FadeIn(lc), Create(circA), Create(circN), FadeIn(hdr), FadeIn(names[0]),
                      FadeIn(vals[0]), FadeIn(vals[1]))
            vo.wait_until("b")
            self.play(Create(link), FadeIn(dot_p), FadeIn(lp))
            vo.wait_until("c")
            self.play(FadeIn(names[1]), FadeIn(vals[2]), FadeIn(vals[3]))
            vo.wait_until("d")
            self.play(tx.animate.set_value(d["two_b"]["incoherent"][0]), ty.animate.set_value(
                d["two_b"]["incoherent"][1]), run_time=2.5)
            vo.wait_until("e")
            for x, y in ((0.3, 0.25), (0.15, 0.6), (0.9, 0.85), (0.6, 0.6)):
                self.play(tx.animate.set_value(x), ty.animate.set_value(y), run_time=1.6)
            self.play(FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("f")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def three(self):
        d = load("accuracy")
        head = label(r"Three worlds: \ project onto the triangle", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sx = Simplex3(origin=[-3.6, -1.4, 0], scale=2.6)
        examples = [("three", r"(0.5,\,0.4,\,0.3)", r"1.2"), ("three_b", r"(0.2,\,0.2,\,0.3)", r"0.7")]
        dots = VGroup()
        for key, _, _ in examples:
            c, p = d[key]["incoherent"], d[key]["projection"]
            dots.add(VGroup(Dot(sx.p(c), color=INC, radius=0.08), Dot(sx.p(p), color=COH, radius=0.08),
                            DashedLine(sx.p(c), sx.p(p), color=GREY_B, stroke_width=2)))
        rows = []
        for key, name, s in examples:
            e = d[key]
            pr = ",\\,".join(f"{v:.2f}" for v in e["projection"])
            rows.append([MathTex(name, font_size=22, color=INC), MathTex(s, font_size=20, color=GREY_A)] +
                        [MathTex(rf"{a:.3f} \to {b:.3f}", font_size=22) for a, b in zip(e["brier_c"], e["brier_p"])])
            rows.append([MathTex(rf"\to ({pr})", font_size=22, color=COH)] + [VGroup() for _ in range(4)])
        hd = [r"c", r"\text{sum}", r"w_1", r"w_2", r"w_3"]
        grid = ValueGrid(hd, rows, col_w=[2.2, 1.3, 1.7, 1.7, 1.7], cell_h=0.5, font_size=22).move_to([2.6, 0.6, 0])
        for r in (0, 2):
            for c in (2, 3, 4):
                grid.cell[r][c].set_color(OK)
        foot = label(r"every incoherent point: \ its projection is closer to every corner", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "With three worlds, the coherent credences form a triangle in space. <bookmark mark='a'/>Credences point "
            "five, point four, point three add to one point two: the point floats above the triangle. Project it "
            "down, and the inaccuracy falls in every world: point five to point four eight seven, point seven to "
            "point six eight seven, point nine to point eight eight seven. <bookmark mark='b'/>Credences that add to "
            "only point seven sit below the triangle; projected up, to point three, point three, point four, again "
            "they improve in all three worlds. <bookmark mark='c'/>The geometry is the same in every dimension. The "
            "simplex is convex, and the projection onto a convex set is closer to every point of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sx), FadeIn(grid.head), Create(grid.rule))
            for mk, k in zip("ab", range(2)):
                vo.wait_until(mk)
                self.play(FadeIn(dots[k]))
                for r in (2 * k, 2 * k + 1):
                    self.play(*[FadeIn(m) for m in grid.cell[r]], run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def theorem(self):
        head = label(r"The accuracy theorem, \ and its fine print", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        thm = VGroup(
            label(r"for any strictly proper inaccuracy measure \ (a Bregman divergence):", font_size=24),
            label(r"incoherent \ $\Rightarrow$ \ strictly dominated by a coherent credence", font_size=24, color=BAD),
            label(r"coherent \ $\Rightarrow$ \ never even weakly dominated", font_size=24, color=OK),
            label(r"de Finetti \ (1974); \ Joyce \ (1998); \ Predd et al.\ \ (2009); \ Pettigrew \ (2016)",
                  font_size=21, color=GREY_A)).arrange(DOWN, buff=0.22).next_to(head, DOWN, buff=0.35)
        fine = [
            (r"why squared error?", r"absolute error is not proper: \ it can favour incoherence (next chapter)"),
            (r"dominance needs care", r"if your credences affect the world, \ dominance can mislead (Caie, \ 2013)"),
            (r"trade-offs", r"epistemic consequentialism: \ accept one falsehood to gain many truths? \ (Greaves)"),
            (r"the same tool, \ again", r"projection = the nearest coherent repair; \ updating as minimal change: \ Ch.\ 5"),
        ]
        g = VGroup()
        for i, (a, b) in enumerate(fine):
            x = label(a, font_size=22, color=INC)
            y = label(b, font_size=21, color=GREY_A)
            if y.width > 8.6:
                y.width = 8.6
            x.move_to([-6.6 + x.width / 2, -0.9 - i * 0.72, 0])
            y.move_to([-3.2 + y.width / 2, -0.9 - i * 0.72, 0])
            g.add(VGroup(x, y))
        with self.voiceover(
            "This is the accuracy argument for probabilism. <bookmark mark='a'/>For any strictly proper measure of "
            "inaccuracy, the mathematicians' Bregman divergences, of which the Brier score is one, "
            "<bookmark mark='b'/>incoherent credences are strictly dominated by coherent ones, "
            "<bookmark mark='c'/>and coherent credences are never dominated, not even weakly. <bookmark mark='d'/>The "
            "result goes back to de Finetti, was made a philosophical argument by Joyce, was proved in this "
            "generality by Joel Predd and colleagues, and is the subject of Richard Pettigrew's book. "
            "<bookmark mark='e'/>The fine print. Why squared error? With absolute error the theorem fails; the next "
            "chapter shows why. <bookmark mark='f'/>Dominance reasoning can mislead when your credences affect the "
            "world, as Michael Caie showed with self-referential propositions. <bookmark mark='g'/>Hilary Greaves "
            "asked whether accuracy licenses trade-offs, accepting one falsehood to gain many truths. "
            "<bookmark mark='h'/>And note the projection itself: it is the nearest coherent repair, and a close "
            "cousin of it returns when we update on evidence."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abcd", thm):
                vo.wait_until(mk)
                self.play(FadeIn(t))
            for mk, r in zip("efgh", g):
                vo.wait_until(mk)
                self.play(FadeIn(r[0]), FadeIn(r[1], shift=LEFT * 0.1))
        self.clear_scene()
