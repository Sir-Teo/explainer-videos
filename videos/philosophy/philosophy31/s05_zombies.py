from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


def matrix(m, names, centre, title, col):
    """A 3 x 3 two-dimensional matrix of truth values: rows are scenarios considered as actual, columns worlds
    considered as counterfactual."""
    g = VGroup()
    cells = VGroup()
    size = 0.78
    x0, y0 = centre[0] - size, centre[1] + size
    for r in range(3):
        row = VGroup()
        for c in range(3):
            sq = Square(side_length=size, color=GREY_C, stroke_width=1.5).move_to([x0 + c * size, y0 - r * size, 0])
            row.add(VGroup(sq, mark(m[r][c], size=26).move_to(sq)))
        cells.add(row)
    short = {"Earth": r"Earth", "Twin Earth": r"Twin", "zombie world": r"zombie"}
    rl = VGroup(*[label(short[n], font_size=16, color=GREY_A).next_to(cells[r][0], LEFT, buff=0.15)
                  for r, n in enumerate(names)])
    cl = VGroup(*[label(short[n], font_size=16, color=GREY_A).next_to(cells[0][c], UP, buff=0.12)
                  for c, n in enumerate(names)])
    t = label(title, font_size=21, color=col).next_to(cl, UP, buff=0.25)
    g.add(cells, rl, cl, t)
    g.cells = cells
    return g


class Zombies(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Zombies", r"Could there be a world just like ours, \ with no one home?", lit=(1974,
                                                                                                            1996),
                            part=PART)
        with self.voiceover("Chapter four. Zombies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.twod()
        self.modal()
        self.price()

    def idea(self):
        hc = history_card(1996, r"David Chalmers", r"\textit{The Conscious Mind}", width=5.4, color=HIST).to_corner(
            UL, buff=0.3)
        def person(x, lit):
            body = VGroup(Circle(radius=0.35, color=PHYS), Line([0, -0.35, 0], [0, -1.5, 0], color=PHYS),
                          Line([-0.6, -0.8, 0], [0.6, -0.8, 0], color=PHYS),
                          Line([0, -1.5, 0], [-0.45, -2.3, 0], color=PHYS),
                          Line([0, -1.5, 0], [0.45, -2.3, 0], color=PHYS)).move_to([x, 0.0, 0])
            glow = Circle(radius=0.32, color=FEEL, fill_opacity=0.7 if lit else 0, stroke_width=0).move_to(
                body[0].get_center())
            return VGroup(body, glow)
        me, z = person(-3.3, True), person(3.3, False)
        ml = wrapped_label(r"you: \ every atom, \ every word, \ and experience", 4.2, 19, FEEL).next_to(
            me, DOWN, buff=0.3)
        zl = wrapped_label(r"your zombie twin: \ every atom, \ every word, \ and nothing", 4.2, 19,
                           GREY_A).next_to(z, DOWN, buff=0.3)
        rows = stack([(r"Kirk \ (1974): \ the philosophical zombie", HIST),
                      (r"it says `I see red' \ and means nothing by it, \ feels nothing", GREY_A)], font_size=20,
                     buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The sharpest form of the hard problem is a thought experiment. <bookmark mark='a'/>Imagine a being "
            "physically identical to you, atom for atom, in a world physically identical to ours. "
            "<bookmark mark='b'/>It walks, talks, and writes papers about consciousness, just as you do, and for "
            "the same physical reasons. But there is nothing it is like to be it. The lights are on, and no one is "
            "home. <bookmark mark='c'/>Robert Kirk named it a zombie in 1974; Chalmers made it famous in 1996. "
            "<bookmark mark='d'/>Its words about red are produced by the same mechanisms as yours. It simply has no "
            "experience of red at all. The question is whether such a world is even coherent."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(me), FadeIn(ml))
            vo.wait_until("b")
            self.play(TransformFromCopy(me[0], z[0]), FadeIn(zl))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), Indicate(z, color=GREY_B))
        self.clear_scene()

    def twod(self):
        d = load("twod")
        head = label(r"Two dimensions, \ computed \ (Part 22)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        names = d["scenarios"]
        W, Pn = d["sentences"]["water is H2O"], d["sentences"]["pain is C-fibre firing"]
        assert names == ["Earth", "Twin Earth", "zombie world"]
        assert W["necessary"] and not W["a_priori"] and not Pn["necessary"] and Pn["primary"] == Pn["secondary"]
        mw = matrix(W["matrix"], names, (-3.4, 0.4), r"`water is H$_2$O'", SIG)
        mp = matrix(Pn["matrix"], names, (3.4, 0.4), r"`pain is C-fibre firing'", FEEL)
        axl = VGroup(label(r"rows: \ a scenario taken as actual", font_size=17, color=GREY_A),
                     label(r"columns: \ a world taken as counterfactual", font_size=17, color=GREY_A)).arrange(
            DOWN, buff=0.1).move_to([0, -1.75, 0])
        diag_w = VGroup(*[SurroundingRectangle(mw.cells[k][k], color=SIG, buff=0.03) for k in range(3)])
        row_w = SurroundingRectangle(mw.cells[0], color=OK, buff=0.05)
        diag_p = VGroup(*[SurroundingRectangle(mp.cells[k][k], color=FEEL, buff=0.03) for k in range(3)])
        row_p = SurroundingRectangle(mp.cells[0], color=BAD, buff=0.05)
        foot = stack([(r"water: \ diagonal has a $\times$, \ Earth's row is all $\checkmark$: \ necessary, \ but "
                       r"not a priori", SIG),
                      (r"pain: \ `pain' names the feeling in every row, \ so diagonal and row agree: \ the zombie "
                       r"$\times$ carries over", FEEL)], font_size=19, buff=0.15).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Part 22 built two-dimensional semantics; here it earns its keep. <bookmark mark='a'/>Three scenarios: "
            "Earth; Twin Earth, where the watery stuff is XYZ; and the zombie world, physically like Earth, with no "
            "experience. Each row takes a scenario as actual; each column considers a world as counterfactual. "
            "<bookmark mark='b'/>Water is H two O. Take Earth as actual, and water is H two O in every column: "
            "the statement is necessary. But take Twin Earth as actual, and the watery stuff there is XYZ: the "
            "diagonal has a false entry, so it is not knowable a priori. A posteriori necessity opens a gap between "
            "the diagonal and the row. <bookmark mark='c'/>Now pain is C-fibre firing. The word pain picks out the "
            "feeling itself, whichever scenario is actual, so every row is the same, and the diagonal and the row "
            "agree. In the zombie world the C-fibres fire and nothing hurts: false. <bookmark mark='d'/>So if the "
            "zombie scenario is coherent, the falsity on the diagonal carries straight over to a world: the "
            "identity is not necessary, and physicalism, which needs it, fails. The physicalist's way out for "
            "water, a gap between the two dimensions, is not available for pain, Chalmers argues, because pain has "
            "no hidden essence that only its appearance picks out: for pain, the appearance is the essence, as "
            "Kripke said."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(mw[1:]), FadeIn(mp[1:]), FadeIn(axl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for row in mw.cells for c in row], lag_ratio=0.08))
            self.play(Create(row_w))
            self.play(Create(diag_w), FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(c) for row in mp.cells for c in row], lag_ratio=0.08))
            self.play(Create(diag_p), Create(row_p))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]), Indicate(mp.cells[2][2], color=BAD, scale_factor=1.2))
        self.clear_scene()

    def modal(self):
        d = load("modal")
        head = label(r"Which physicalism the argument refutes", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["strong_any"] and d["strong_s5"] and d["weak_worlds"] == 2 and d["weak_Q"] == [0]
        defs = VGroup(label(r"$P$: \ every physical truth \quad $Q$: \ someone feels pain", font_size=21,
                            color=GREY_A)).move_to([0, 2.3, 0])
        f1 = MathTex(r"\Box(P \rightarrow Q) \;\;\wedge\;\; \Diamond(P \wedge \neg Q)", font_size=36, color=FEEL)
        r1 = label(r"no model, \ on any frame up to three worlds \ (and none in $K$)", font_size=20, color=BAD)
        g1 = VGroup(f1, r1).arrange(DOWN, buff=0.25).move_to([-3.3, 0.6, 0])
        f2 = MathTex(r"(P \rightarrow Q) \;\wedge\; P \;\wedge\; \Diamond(P \wedge \neg Q)", font_size=36, color=PHYS)
        r2 = label(r"a model: \ two worlds, \ $Q$ only in ours", font_size=20, color=OK)
        g2 = VGroup(f2, r2).arrange(DOWN, buff=0.25).move_to([3.3, 0.6, 0])
        w0 = VGroup(Circle(radius=0.5, color=OK), MathTex(r"P,\,Q", font_size=22)).move_to([2.3, -1.2, 0])
        w1 = VGroup(Circle(radius=0.5, color=GREY_B), MathTex(r"P,\,\neg Q", font_size=22)).move_to([4.3, -1.2, 0])
        link = DoubleArrow(w0.get_right(), w1.get_left(), buff=0.05, color=GREY_B, stroke_width=2)
        foot = stack([(r"physicalism needs necessitation: \ the physical truths must fix the phenomenal ones in every "
                       r"possible world", GOAL),
                      (r"so everything turns on the step from conceivable to possible \ (the 2D matrix, \ above)",
                       GREY_A)], font_size=19, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Reasoner's modal logic from Part 4 makes the argument's target exact. <bookmark mark='a'/>Let P "
            "be the conjunction of all the physical truths, and Q a phenomenal truth, say that someone feels pain. "
            "<bookmark mark='b'/>Physicalism, as the argument understands it, says that P necessitates Q: box, P "
            "implies Q. Zombies say it is possible to have P without Q. The Reasoner searches every frame up to "
            "three worlds for a model of both, and finds none; in fact none exists in any normal modal logic. "
            "<bookmark mark='c'/>A weaker claim, that P implies Q merely here in our world, is consistent with "
            "zombies: two worlds, Q only in ours. <bookmark mark='d'/>So the zombie argument refutes only a "
            "physicalism of necessitation, which is the physicalism nearly everyone holds, since supervenience in "
            "Part 30 was a modal claim. And everything turns on the step from conceivable to possible, the step "
            "the two-dimensional matrix examined."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs))
            vo.wait_until("b")
            self.play(Write(f1))
            self.play(FadeIn(r1))
            vo.wait_until("c")
            self.play(Write(f2), FadeIn(r2))
            self.play(FadeIn(w0), FadeIn(w1), GrowFromCenter(link))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def price(self):
        d = load("zombie")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(d["mcs"]) == [["CP"], ["E"], ["P"], ["Z"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.4, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ the zombie argument")
        positions = [(("Z",), r"type-A physicalism", r"we only think we can conceive them: \ Dennett"),
                     (("CP",), r"type-B physicalism", r"conceivable, \ yet impossible: \ Loar, \ Papineau, \ "
                                                       r"Hill and McLaughlin"),
                     (("E",), r"Russellian monism", r"a world without the intrinsic natures is not a full "
                                                    r"physical duplicate"),
                     (("P",), r"property dualism", r"experience is a further fact: \ Chalmers")]
        with self.voiceover(
            "Four claims cannot all be true. <bookmark mark='a'/>A zombie world is conceivable. Whatever is ideally "
            "conceivable is possible. If a zombie world is possible, physicalism is false. And physicalism is true. "
            "<bookmark mark='b'/>One has to go. <bookmark mark='c'/>The type-A physicalist denies the first: we only "
            "think we can conceive zombies, Dennett says, because we have not really imagined all the physical "
            "facts. <bookmark mark='d'/>The type-B physicalist denies the second: zombies are conceivable, as water "
            "without H two O is, and impossible all the same. <bookmark mark='e'/>The Russellian monist denies the "
            "third: what we conceive is a world with the same structure, but if experience is the intrinsic nature "
            "of matter, that world is not a full physical duplicate. <bookmark mark='f'/>And the property dualist "
            "denies the last. Experience is a further fact about our world, over and above the physical: "
            "Chalmers's own conclusion."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()
