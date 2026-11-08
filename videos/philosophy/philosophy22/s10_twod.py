from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


def matrix_mob(M, size=0.9, font_size=22, center=ORIGIN) -> VGroup:
    """Squares with T or F; ``.cells[i][j]`` is (square, text)."""
    n = len(M)
    g = VGroup()
    g.cells = []
    c0 = np.array(center, float)
    for i in range(n):
        row = []
        for j in range(n):
            p = c0 + np.array([(j - (n - 1) / 2) * size, ((n - 1) / 2 - i) * size, 0])
            sq = Square(side_length=size * 0.94, stroke_color=GREY_B, stroke_width=1.5,
                        fill_color=OK if M[i][j] else BAD, fill_opacity=0.18).move_to(p)
            t = MathTex(r"\text{T}" if M[i][j] else r"\text{F}", font_size=font_size, color=OK if M[i][j] else BAD
                        ).move_to(p)
            row.append(VGroup(sq, t))
            g.add(row[-1])
        g.cells.append(row)
    return g


class TwoD(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Two dimensions", r"Can one sentence have two intensions?", lit=(1978, 2006),
                            part=PART)
        with self.voiceover("Chapter nine. Two dimensions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.fill()
        self.classes()
        self.zombies()
        self.brick()

    def idea(self):
        head = label(r"Two roles for a world", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"[\![\, S \,]\!]\,(\,", r"w", r",\;", r"v", r"\,)", font_size=56)
        f[1].set_color(DESC)
        f[3].set_color(WORLD)
        f.move_to([0, 1.5, 0])
        lw = wrapped_label(r"the world considered as actual: \ fixes what `water' picks out", 5.2, 22,
                           DESC).move_to([-3.7, 0.0, 0])
        lv = wrapped_label(r"the world considered as counterfactual: \ where we check", 5.2, 22,
                           WORLD).move_to([3.7, 0.0, 0])
        aw = Arrow(lw.get_top(), f[1].get_bottom(), buff=0.1, color=DESC, stroke_width=2.5)
        av = Arrow(lv.get_top(), f[3].get_bottom(), buff=0.1, color=WORLD, stroke_width=2.5)
        rows = stack([(r"primary intension: \ the diagonal, \ $w \mapsto [\![S]\!](w, w)$: \ how $S$ fares if $w$ "
                       r"turns out to be actual", DESC),
                      (r"secondary intension: \ the actual row, \ $v \mapsto [\![S]\!](@, v)$: \ Kripke's "
                       r"counterfactual truth conditions", WORLD),
                      (r"Stalnaker \ (1978): \ the diagonal proposition; \ Davies and Humberstone \ (1980); \ "
                       r"Chalmers and Jackson \ (2001)", GREY_A)], font_size=21, aligned_edge=LEFT,
                     width=12.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Two-dimensional semantics starts from an observation. A world can play two different roles in "
            "evaluating a sentence. <bookmark mark='a'/>Write the truth value of a sentence S as depending on two "
            "worlds. <bookmark mark='b'/>The first, w, is the world considered as actual: it settles what our words "
            "pick out. If Twin Earth turned out to be our world, water would pick out XYZ. <bookmark mark='c'/>The "
            "second, v, is the world considered as counterfactual: the one at which we then check whether S is "
            "true. <bookmark mark='d'/>Fix both worlds to be the same and you get the primary intension: how S fares "
            "if w turns out to be actual. <bookmark mark='e'/>Fix the first to be our actual world and you get the "
            "secondary intension: Kripke's counterfactual truth conditions. <bookmark mark='f'/>The idea goes back "
            "to Robert Stalnaker's diagonal propositions, and to Martin Davies and Lloyd Humberstone; Chalmers and "
            "Frank Jackson made it a theory of meaning."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(lw), GrowArrow(aw))
            vo.wait_until("c")
            self.play(FadeIn(lv), GrowArrow(av))
            for mk, r in zip("def", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def fill(self):
        d = load("twod")
        W = d["worlds"]
        s = d["sentences"][0]
        head = label(r"Filling the matrix: \ `water $=$ H$_2$O'", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        facts = d["facts"]
        hd = [r"\text{world}", r"\text{watery stuff}", r"\text{evening star}", r"\text{morning star}",
              r"\text{stick S}"]
        frows = [[MathTex(r"\text{" + w + "}", font_size=19, color=NAME if w == d["actual"] else WHITE)] +
                 [MathTex(r"\text{" + str(facts[w][k]).replace("H2O", "H$_2$O") + "}", font_size=19)
                  for k in ("watery", "evening", "morning")] +
                 [MathTex(rf"{facts[w]['stick']:.2f}\,\text{{m}}", font_size=19)] for w in W]
        ftab = ValueGrid(hd, frows, col_w=[1.8, 1.5, 1.5, 1.5, 1.1], cell_h=0.42, font_size=17).move_to(
            [3.25, 1.8, 0])
        M = matrix_mob(s["matrix"], size=1.0, font_size=26, center=[-3.0, -0.9, 0])
        rl = VGroup(*[label(w, font_size=17, color=NAME if w == d["actual"] else DESC).next_to(
            M.cells[i][0], LEFT, buff=0.15) for i, w in enumerate(W)])
        cl = VGroup(*[label(w, font_size=17, color=WORLD).next_to(M.cells[0][j], UP, buff=0.12).rotate(0.0)
                      for j, w in enumerate(W)])
        rt = label(r"considered as actual", font_size=18, color=DESC).next_to(rl, LEFT, buff=0.2).rotate(PI / 2)
        ct = label(r"considered as counterfactual", font_size=18, color=WORLD).next_to(cl, UP, buff=0.12)
        diag = VGroup(*[SurroundingRectangle(M.cells[i][i], color=DESC, buff=0.02, stroke_width=4)
                        for i in range(3)])
        arow = SurroundingRectangle(VGroup(*M.cells[0]), color=WORLD, buff=0.05, stroke_width=4)
        rows = stack([(r"row Twin Earth: \ `water' picks out XYZ, \ which is never H$_2$O", DESC),
                      (r"diagonal: \ T, \ F, \ T: \ not \textit{a priori}", DESC),
                      (r"actual row: \ T, \ T, \ T: \ necessary", WORLD),
                      (r"so: \ necessary \textit{a posteriori}, \ computed", OK)], font_size=20, aligned_edge=LEFT,
                     width=5.4).move_to([3.6, -1.3, 0])
        with self.voiceover(
            "The Reasoner builds it for three worlds. <bookmark mark='a'/>Earth: the watery stuff is H two O. Twin "
            "Earth: the watery stuff is XYZ. And a third world, Dusk, which differs in the evening sky and will "
            "matter for other sentences. <bookmark mark='b'/>The matrix for water is H two O. Row by row, a world "
            "is considered as actual; column by column, a world is considered as counterfactual. In the Earth row, "
            "water picks out H two O, and H two O is H two O wherever we check: true, true, true. "
            "<bookmark mark='c'/>In the Twin Earth row, water picks out XYZ, which is never H two O: false all "
            "along. The Dusk row is like Earth's. <bookmark mark='d'/>Read the diagonal: true, false, true. If Twin "
            "Earth had turned out to be actual, the sentence would have been false; so it cannot be known a "
            "priori. <bookmark mark='e'/>Read the actual row: true everywhere. So it is necessary. "
            "<bookmark mark='f'/>Necessary a posteriori, computed from the matrix."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ftab.head), Create(ftab.rule), *[FadeIn(c) for r in ftab.cell for c in r])
            vo.wait_until("b")
            self.play(FadeIn(rl), FadeIn(cl), FadeIn(rt), FadeIn(ct))
            for j in range(3):
                self.play(FadeIn(M.cells[0][j]), run_time=0.45)
            vo.wait_until("c")
            for i in (1, 2):
                for j in range(3):
                    self.play(FadeIn(M.cells[i][j]), run_time=0.35)
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(LaggedStart(*[Create(x) for x in diag], lag_ratio=0.3), FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(Create(arow), FadeIn(rows[2]))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def classes(self):
        d = load("twod")
        head = label(r"Six sentences, \ four classes", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        mats = VGroup()
        for k, s in enumerate(d["sentences"]):
            c = np.array([-4.6 + 4.6 * (k % 3), 1.0 - 2.55 * (k // 3), 0])
            M = matrix_mob(s["matrix"], size=0.5, font_size=16, center=c + LEFT * 0.75)
            diag = VGroup(*[SurroundingRectangle(M.cells[i][i], color=DESC, buff=0.01, stroke_width=2.5)
                            for i in range(3)])
            arow = SurroundingRectangle(VGroup(*M.cells[0]), color=WORLD, buff=0.03, stroke_width=2.5)
            t = label(s["sentence"].replace("H2O", "H$_2$O"), font_size=17, color=WHITE).next_to(M, UP, buff=0.12)
            t.set_x(c[0])
            cls = s["class"].replace("a priori", r"\textit{a priori}").replace("a posteriori", r"\textit{a posteriori}")
            col = {"necessary a priori": OK, "necessary a posteriori": NAME, "contingent a priori": DESC,
                   "contingent a posteriori": GREY_A}[s["class"]]
            cl = wrapped_label(cls, 1.7, 16, col).next_to(M, RIGHT, buff=0.25)
            mats.add(VGroup(M, diag, arow, t, cl))
        key = VGroup(VGroup(Square(side_length=0.22, color=DESC, stroke_width=3), label(r"diagonal: \ \textit{a "
                                                                                          r"priori} iff all T",
                                                                                          font_size=17, color=DESC)
                            ).arrange(RIGHT, buff=0.12),
                     VGroup(Rectangle(width=0.5, height=0.22, color=WORLD, stroke_width=3),
                            label(r"actual row: \ necessary iff all T", font_size=17, color=WORLD)).arrange(
                         RIGHT, buff=0.12)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now six sentences. <bookmark mark='a'/>Water is H two O, and Hesperus is Phosphorus: actual row all "
            "true, diagonal not. Necessary a posteriori. <bookmark mark='b'/>Water is the watery stuff, and the "
            "length of stick S is one metre: the diagonal is all true, since whatever world is actual, water and "
            "the metre are fixed by that world's watery stuff and that world's stick. But the actual row has a "
            "false: in Twin Earth the watery stuff is not water, and S is longer than a metre. Contingent a priori, "
            "Kripke's strange box, computed. <bookmark mark='c'/>The evening star is Venus: false at Dusk, on "
            "both readings. Contingent a posteriori. <bookmark mark='d'/>And H two O is H two O: true everywhere. "
            "Necessary a priori. <bookmark mark='e'/>The two notions that Kant fused, and Kripke split, are two "
            "readings of one matrix: the a priori is the diagonal, the necessary is the actual row."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            order = [("a", (0, 1)), ("b", (2, 3)), ("c", (4,)), ("d", (5,))]
            for mk, ks in order:
                vo.wait_until(mk)
                self.play(*[FadeIn(mats[k]) for k in ks])
            vo.wait_until("e")
            self.play(*[Indicate(mats[k][1], color=DESC) for k in range(6)])
        self.clear_scene()

    def zombies(self):
        head = label(r"The bridge to Part 31", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        steps = stack([(r"1. \ $P \land \lnot Q$ is ideally conceivable, \ in the primary sense", WHITE),
                       (r"\ \ \ \ ($P$: \ all the physical truths; \ $Q$: \ some truth about consciousness)", GREY_A),
                       (r"2. \ so it is primarily possible: \ true on the diagonal at some world", DESC),
                       (r"3. \ for consciousness the primary and secondary intensions coincide: \ no Twin Earth "
                        r"for pain", GOAL),
                       (r"4. \ so it is secondarily possible: \ a world physically like ours, \ without "
                        r"consciousness", WORLD),
                       (r"5. \ so the physical truths do not necessitate all the truths: \ materialism is false",
                        BAD)], font_size=22, aligned_edge=LEFT, width=12.0, buff=0.28).move_to([0, -0.1, 0])
        with self.voiceover(
            "The machinery was built for a purpose, and here it is in outline, to be examined in Part 31. "
            "<bookmark mark='a'/>Let P be all the physical truths, and Q a truth about consciousness, say that "
            "someone is in pain. Chalmers argues that P and not Q is ideally conceivable in the primary sense: a "
            "zombie world. <bookmark mark='b'/>Then, by the defensible bridge, it is primarily possible. "
            "<bookmark mark='c'/>For consciousness, the two intensions coincide; there is no Twin Earth for pain, "
            "because what fixes the reference of pain is how it feels. <bookmark mark='d'/>So the zombie world is "
            "possible in the ordinary, counterfactual sense. <bookmark mark='e'/>And then the physical truths do not "
            "necessitate all the truths, and materialism is false. Each step can be resisted, and each has been."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]))
            for mk, r in zip("bcde", steps[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def brick(self):
        w = wall(upto=22, current=22).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(22, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        rows = card[1][1]
        with self.voiceover(
            "This is the twenty-second brick in the Wall. <bookmark mark='a'/>The dream: conceivability as a "
            "straightforward guide to possibility, a way to learn what could be from the armchair. "
            "<bookmark mark='b'/>The wall: Kripke's necessary a posteriori. Some things that seem conceivable, like "
            "water not being H two O, are impossible, and we learn which only by experience. "
            "<bookmark mark='c'/>What it forces: either two dimensions of meaning, with the bridge rebuilt on the "
            "diagonal, or no general bridge at all."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[22], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
