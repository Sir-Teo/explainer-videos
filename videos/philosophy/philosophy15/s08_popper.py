from __future__ import annotations

from videos.philosophy.philosophy15.common import *  # noqa: F403


def swan(color, size=0.28, neck_color=None, outline=GREY_B) -> VMobject:
    nc = neck_color or color
    body = Ellipse(width=size * 2.2, height=size * 1.0, stroke_color=outline, stroke_width=2, fill_color=color,
                   fill_opacity=1)
    neck = Line(body.get_right() + LEFT * size * 0.3, body.get_right() + LEFT * size * 0.2 + UP * size * 1.1,
                stroke_color=nc, stroke_width=4)
    head = Circle(radius=size * 0.18, stroke_width=0, fill_color=nc,
                  fill_opacity=1).move_to(neck.get_end())
    beak = Polygon(head.get_right(), head.get_right() + RIGHT * size * 0.3 + DOWN * size * 0.05,
                   head.get_right() + DOWN * size * 0.12, stroke_width=0, fill_color=BAD, fill_opacity=1)
    return VGroup(body, neck, head, beak)


class Popper(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Conjectures and refutations", r"Can science do without induction?",
                            lit=(1934, 1974), part=PART)
        with self.voiceover("Chapter seven. Conjectures and refutations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.falsify()
        self.duhem()
        self.verisim()
        self.corroboration()

    def falsify(self):
        hc = history_card(1934, r"Karl Popper", r"\textit{Logik der Forschung} \ (English 1959)", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        h = MathTex(r"H:\ \forall x\,(\text{Swan}(x) \to \text{White}(x))", font_size=34, color=FUT).next_to(
            hc, DOWN, buff=0.4).set_x(0)
        whites = VGroup(*[swan(WHITE, neck_color=GREY_A) for _ in range(9)]).arrange(RIGHT, buff=0.25).next_to(h, DOWN, buff=0.4)
        wl = label(r"any number of white swans: \ never a proof", font_size=21, color=GREY_A).next_to(whites, DOWN,
                                                                                                   buff=0.15)
        black = swan(RAVEN, 0.34, neck_color="#3A4050", outline=GREY_A).next_to(wl, DOWN, buff=0.35)
        bl = label(r"one black swan \ (Western Australia, \ 1697): \ a refutation", font_size=21,
                   color=BAD).next_to(black, RIGHT, buff=0.3)
        mt = MathTex(r"H \vdash E,\quad \lnot E \ \ \therefore\ \lnot H", font_size=34, color=BAD).next_to(
            VGroup(black, bl), DOWN, buff=0.3)
        side = stack([(r"science: \ bold conjectures, \ severe tests", OK),
                      (r"bold = high content = \textit{low} probability: \ $P(H \wedge G) \le P(H)$", GOAL)],
                     font_size=21).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Karl Popper's answer to Hume was radical: science does not use induction at all. "
            "<bookmark mark='a'/>Take the hypothesis that all swans are white. <bookmark mark='b'/>No number of "
            "white swans proves it. <bookmark mark='c'/>But one black swan, like those Willem de Vlamingh's crew saw "
            "in Western Australia in 1697, refutes it, <bookmark mark='d'/>by modus tollens, a purely deductive "
            "rule: H implies E; not E; so not H. <bookmark mark='e'/>So science, for Popper, is bold conjecture and "
            "severe attempted refutation. And bold means improbable: a theory that says more has more ways to be "
            "wrong. The probability of H and G together is never more than that of H alone. Science aims at "
            "content, not at probability."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(h))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in whites], lag_ratio=0.1), FadeIn(wl))
            vo.wait_until("c")
            self.play(FadeIn(black, scale=1.4), FadeIn(bl))
            vo.wait_until("d")
            self.play(Write(mt))
            vo.wait_until("e")
            self.play(FadeIn(side))
        self.clear_scene()

    def duhem(self):
        head = label(r"Duhem and Quine: \ which premise failed?", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        prem = [r"Newton's laws", r"the known planets are all there is", r"the observations are accurate"]
        boxes = VGroup()
        for t in prem:
            l_ = label(t, font_size=21)
            b = RoundedRectangle(width=l_.width + 0.4, height=0.6, corner_radius=0.1, stroke_color=GREY_B,
                                 stroke_width=2)
            boxes.add(VGroup(b, l_.move_to(b)))
        boxes.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.45)
        pred = label(r"predicted orbit", font_size=22, color=FUT).next_to(boxes, DOWN, buff=0.8)
        arrows = VGroup(*[Arrow(b.get_bottom(), pred.get_top() + RIGHT * 0.25 * (b.get_x() - pred.get_x()) / 3,
                                buff=0.12, color=GREY_C, stroke_width=2, max_tip_length_to_length_ratio=0.08)
                          for b in boxes])
        x = MathTex(r"\times", font_size=40, color=BAD).next_to(pred, RIGHT, buff=0.2)
        eq = MathTex(r"(H \wedge A_1 \wedge A_2) \vdash E,\ \ \lnot E\ \ \therefore\ \lnot(H \wedge A_1 \wedge A_2)",
                     font_size=30, color=BAD).next_to(pred, DOWN, buff=0.3)
        left = stack([(r"Uranus, \ 1840s", PAST), (r"blame $A_1$: \ another planet", WHITE),
                      (r"Neptune found, \ 1846: \ Newton saved", OK)], font_size=21).move_to([-3.4, -2.3, 0])
        right = stack([(r"Mercury, \ 1859", PAST), (r"blame $A_1$: \ the planet Vulcan", WHITE),
                       (r"no Vulcan: \ Newton was the culprit \ (1915)", BAD)], font_size=21).move_to([3.4, -2.3, 0])
        foot = label(r"logic alone cannot say which; \ Lakatos: \ judge whole research programmes", font_size=21,
                     color=GOAL).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Falsification is less simple than it looks, as Pierre Duhem saw in 1906 and Quine generalized. "
            "<bookmark mark='a'/>No theory predicts anything alone. A predicted orbit follows from Newton's laws, "
            "together with assumptions about which planets exist, and the reliability of the telescopes. "
            "<bookmark mark='b'/>When the prediction fails, modus tollens refutes only the conjunction. "
            "<bookmark mark='c'/>In the 1840s Uranus strayed from its predicted orbit. Le Verrier and Adams blamed "
            "the auxiliary assumption, predicted a new planet, and in 1846 Neptune was found where Le Verrier said. "
            "<bookmark mark='d'/>In 1859 Le Verrier tried the same move for Mercury, and predicted a planet "
            "called Vulcan. It was never found. This time the culprit was Newton, as Einstein showed. "
            "<bookmark mark='e'/>The logic was identical, and only later evidence told the two cases apart. Imre "
            "Lakatos concluded that we judge whole research programmes, progressive or degenerating, not single "
            "hypotheses."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.3), FadeIn(pred),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(x, scale=1.5), Write(eq))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in left], lag_ratio=0.5),
                      Indicate(boxes[1], color=PAST, scale_factor=1.05))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in right], lag_ratio=0.5),
                      Indicate(boxes[0], color=BAD, scale_factor=1.05))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def verisim(self):
        d = load("popper")
        mt, lg = d["mt"], d["lang"]
        head = label(r"Closer to the truth? \ Verisimilitude", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        defn = MathTex(r"A \succ B \iff \mathrm{Cn}_T(B) \subseteq \mathrm{Cn}_T(A)\ \text{ and }\ "
                       r"\mathrm{Cn}_F(A) \subseteq \mathrm{Cn}_F(B)", font_size=30, color=FUT).next_to(
            head, DOWN, buff=0.3)
        dl = label(r"Popper \ (1963): \ more truths among its consequences, \ fewer falsehoods \ (one strictly)",
                   font_size=20, color=GREY_A).next_to(defn, DOWN, buff=0.15)
        chk = stack([
            (r"the Reasoner: \ three atoms, \ " + str(mt["n_theories"]) + r" theories, \ " +
             f"{mt['pairs_checked']:,}".replace(",", "{,}") + r" pairs with a false theory first", WHITE),
            (r"false theories closer than another: \ " + str(mt["false_closer"]) + r" \ \ \ (Miller, \ Tichý, \ "
             r"1974)", BAD),
        ], font_size=21).next_to(dl, DOWN, buff=0.3)

        def w(t, names):
            return r"$" + r" \wedge ".join(n if v else r"\lnot " + n for n, v in zip(names, t)) + r"$"
        hrw, hma = ("h", "r", "w"), ("h", "m", "a")
        hd = [r"\text{theory}", r"\text{in } h, r, w", r"\text{wrong}", r"\text{in } h, m, a", r"\text{wrong}"]
        rows = [[MathTex(r"\text{truth}", font_size=24, color=OK), label(w(lg["truth"], hrw), font_size=22),
                 MathTex("0", font_size=24), label(w(lg["truth_m"], hma), font_size=22), MathTex("0", font_size=24)],
                [MathTex(r"T_1", font_size=24, color=A_C), label(w(lg["T1"], hrw), font_size=22),
                 MathTex(lg["d1"].replace("1/3", r"\tfrac13"), font_size=24, color=OK),
                 label(w(lg["T1_m"], hma), font_size=22),
                 MathTex(lg["d1_m"].replace("1/3", r"\tfrac13"), font_size=24, color=BAD)],
                [MathTex(r"T_2", font_size=24, color=B_C), label(w(lg["T2"], hrw), font_size=22),
                 MathTex(lg["d2"].replace("1/3", r"\tfrac13"), font_size=24, color=BAD),
                 label(w(lg["T2_m"], hma), font_size=22),
                 MathTex(lg["d2_m"].replace("1/3", r"\tfrac13"), font_size=24, color=OK)]]
        grid = ValueGrid(hd, rows, col_w=[1.4, 3.0, 1.2, 3.0, 1.2], cell_h=0.55, font_size=22).next_to(chk, DOWN,
                                                                                                      buff=0.35)
        key = label(r"$h$ hot, \ $r$ rainy, \ $w$ windy; \ \ $m$: \ $h \leftrightarrow r$, \ \ $a$: \ "
                    r"$h \leftrightarrow w$", font_size=19, color=GREY_B).next_to(grid, DOWN, buff=0.15)
        foot = label(r"likeness to the truth flips with the vocabulary: \ grue again", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "If no theory is ever proved, can one at least be closer to the truth than another? Popper defined "
            "verisimilitude. <bookmark mark='a'/>A is closer to the truth than B if A has all of B's true "
            "consequences and B has all of A's false ones, with at least one of these strict. "
            "<bookmark mark='b'/>David Miller and Pavel Tichý proved in 1974 that on this definition no false "
            "theory is ever closer to the truth than any other theory. The Reasoner checks every pair over three "
            "atoms: thirty-two thousand pairs, and not one. Since every interesting theory in science is false, the "
            "definition is useless. <bookmark mark='c'/>Tichý proposed likeness instead: count how many atoms a "
            "theory gets wrong. The weather is hot, rainy and windy. T one says it is not hot but rainy and windy: "
            "one wrong. T two says it is none of these: three wrong. T one is closer. <bookmark mark='d'/>Miller's "
            "reply was to translate. Call it Minnesotan when it is hot exactly when rainy, and Arizonan when hot "
            "exactly when windy. In hot, Minnesotan and Arizonan, T one gets all three wrong, and T two only one. "
            "<bookmark mark='e'/>Likeness to the truth depends on the vocabulary. It is grue again."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(defn), FadeIn(dl))
            vo.wait_until("b")
            self.play(FadeIn(chk[0]))
            self.play(FadeIn(chk[1], scale=1.1))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(key))
            self.play(*[FadeIn(grid.cell[r][c]) for r in range(3) for c in range(3)])
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[r][c]) for r in range(3) for c in (3, 4)])
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def corroboration(self):
        head = label(r"Salmon's question", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"Popper: \ prefer the theory that has best survived severe tests \ (`corroboration')", OK),
            (r"you must build a bridge tomorrow: \ which theory should you rely on?", WHITE),
            (r"`it has survived' is a report about the past", PAST),
            (r"`so rely on it' treats the past as a guide to the future", FUT),
            (r"Salmon \ (1981): \ either corroboration is idle for prediction, \ or it is induction", BAD),
        ], font_size=24, buff=0.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Wesley Salmon asked Popper a practical question. <bookmark mark='a'/>Popper tells us to prefer the "
            "theory that has best survived severe tests. <bookmark mark='b'/>Suppose you must build a bridge "
            "tomorrow. Which theory should you rely on? <bookmark mark='c'/>That a theory has survived is a report "
            "about the past. <bookmark mark='d'/>To rely on it tomorrow is to treat the past as a guide to the "
            "future. <bookmark mark='e'/>So either corroboration says nothing about what to predict, or it is "
            "induction under another name."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
