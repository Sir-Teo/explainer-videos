from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


class Donkey(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Donkeys and dynamics", r"What does `it' refer to?", lit=(1962, 1981, 1991),
                            part=PART)
        with self.voiceover("Chapter fourteen. Donkeys and dynamics."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.geach()
        self.dpl()
        self.discourse()
        self.dynamic()

    def geach(self):
        head = label(r"`Every farmer who owns a donkey beats it'", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        naive = MathTex(r"\forall x\,\big(\,(Fx \wedge \exists y\,(Dy \wedge Oxy)) \rightarrow B x", r"y", r"\big)",
                        font_size=34)
        naive[1].set_color(BAD)
        right = MathTex(r"\forall x\, \forall y\, \big(\,(Fx \wedge Dy \wedge Oxy) \rightarrow Bxy\big)", font_size=34,
                        color=OK)
        ind = MathTex(r"\text{`a farmer owns a donkey'}: \quad \exists x\, \exists y\,(Fx \wedge Dy \wedge Oxy)",
                      font_size=30, color=REF)
        VGroup(naive, right, ind).arrange(DOWN, buff=0.55).move_to([0, 0.9, 0])
        tags = VGroup(label(r"the $y$ in `beats $y$' is outside the scope of $\exists y$: \ unbound", font_size=19,
                            color=BAD).next_to(naive, DOWN, buff=0.12),
                      label(r"right truth conditions, \ but `a donkey' has become `every donkey'", font_size=19,
                            color=OK).next_to(right, DOWN, buff=0.12),
                      label(r"elsewhere, \ `a' is existential", font_size=19, color=REF).next_to(ind, DOWN, buff=0.12))
        foot = label(r"Geach \ (1962): \ an indefinite that binds a pronoun beyond its scope", font_size=21,
                     color=HIST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Peter Geach, in 1962, posed a puzzle with a farmer and a donkey. <bookmark mark='a'/>Translate every "
            "farmer who owns a donkey beats it into first-order logic in the obvious way, and the pronoun it becomes "
            "a variable outside the scope of the quantifier that should bind it. The formula does not say what the "
            "sentence says. <bookmark mark='b'/>The formula that gets the truth conditions right turns a donkey into "
            "a universal: for every farmer and every donkey he owns, he beats it. <bookmark mark='c'/>But elsewhere "
            "the indefinite a donkey is existential: a farmer owns a donkey means there is one. "
            "<bookmark mark='d'/>So the same word seems to mean some in one place and every in another, depending on "
            "a pronoun that comes later."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(naive), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(Write(right), FadeIn(tags[1]))
            vo.wait_until("c")
            self.play(Write(ind), FadeIn(tags[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def dpl(self):
        d = load("donkey")
        hc = history_card(1991, r"Jeroen Groenendijk and Martin Stokhof", r"`Dynamic Predicate Logic'", width=7.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = stack([(r"a formula's meaning: \ a relation between assignments, \ input to outputs", SENSE),
                      (r"$\exists x$: \ reset $x$ to anything, \ and pass it on", REF),
                      (r"conjunction: \ feed the outputs of the left into the right", NAME),
                      (r"`if \dots\ then': \ every output of the left must be extendable by the right", GOAL)],
                     font_size=21, aligned_edge=LEFT, width=7.8, buff=0.26).next_to(hc, DOWN, buff=0.35).align_to(
            hc, LEFT)
        assert d["trials"] == 400 and d["dpl_vs_fo"] == 400 and d["discourse"] == 400 and d["dpl_vs_naive"] == 352
        hd = [r"\text{DPL donkey sentence against}", r"\text{agree on}"]
        cells = [[label(r"$\forall x \forall y$ translation", font_size=20, color=OK),
                  MathTex(r"400 / 400", font_size=24, color=OK)],
                 [label(r"static translation, \ $y$ unbound", font_size=20, color=BAD),
                  MathTex(r"352 / 400", font_size=24, color=BAD)]]
        grid = ValueGrid(hd, cells, col_w=[4.4, 2.2], cell_h=0.5, font_size=20).move_to([3.4, -1.9, 0])
        gtag = label(r"400 random models", font_size=17, color=GREY_A).next_to(grid, UP, buff=0.12)
        with self.voiceover(
            "In 1991 Jeroen Groenendijk and Martin Stokhof proposed changing what a formula means. "
            "<bookmark mark='a'/>In dynamic predicate logic, a formula's meaning is not a set of assignments but a "
            "relation between them: given an input assignment of objects to variables, it returns the outputs. "
            "<bookmark mark='b'/>An existential resets its variable to any object and passes the result on. "
            "<bookmark mark='c'/>A conjunction feeds the outputs of its left side into its right side, so a variable "
            "set by an existential stays set to the right of it. <bookmark mark='d'/>And if-then requires every "
            "output of the antecedent to be extendable by the consequent, which is where the universal force comes "
            "from. <bookmark mark='e'/>The Reasoner implements it and tests the obvious translation of the donkey "
            "sentence, read dynamically, on four hundred random models. It agrees with the correct first-order "
            "formula every time. Read statically, with y left unbound, it is wrong on forty-eight of them."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(gtag), FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(x) for x in grid.cell[r]], run_time=0.5)
        self.clear_scene()

    def discourse(self):
        d = load("donkey")
        head = label(r"Across sentences", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        s = label(r"`A farmer owns a donkey. \ He beats it.'", font_size=28, color=TRUTH).move_to([0, 2.0, 0])
        box = RoundedRectangle(width=4.2, height=3.0, corner_radius=0.1, color=SENSE).move_to([-3.4, -0.4, 0])
        refs = MathTex(r"x \quad y", font_size=30, color=REF).move_to(box.get_top() + DOWN * 0.4)
        line = Line(box.get_left() + DOWN * 0.0 + UP * 0.9, box.get_right() + UP * 0.9, color=SENSE).shift(DOWN * 0.15)
        conds = VGroup(*[MathTex(t, font_size=26, color=WHITE) for t in (r"\textsc{farmer}(x)", r"\textsc{donkey}(y)",
                                                                          r"\textsc{owns}(x, y)", r"\textsc{beats}(x, y)")]
                       ).arrange(DOWN, buff=0.15).move_to(box.get_center() + DOWN * 0.35)
        dtag = label(r"a discourse representation structure \ (Kamp, \ 1981)", font_size=17, color=GREY_A).next_to(
            box, DOWN, buff=0.12)
        assert d["discourse"] == d["trials"]
        side = stack([(r"each sentence adds discourse referents and conditions to a growing box", SENSE),
                      (r"`he' and `it' pick up referents introduced earlier", NAME),
                      (r"DPL: \ $\exists x\,(Fx \wedge \exists y\,(Dy \wedge Oxy)) \wedge Bxy$ \ equals \ "
                       r"$\exists x \exists y\,(\dots \wedge Bxy)$", REF),
                      (r"checked on 400 random models: \ 400 agree", OK)], font_size=20, aligned_edge=LEFT, width=5.6,
                     buff=0.3).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "The same mechanism handles pronouns across sentences. <bookmark mark='a'/>A farmer owns a donkey. He "
            "beats it. <bookmark mark='b'/>Hans Kamp, in 1981, and Irene Heim, in 1982, represented a discourse as a "
            "growing box. Each sentence adds discourse referents, here x and y, and conditions on them. "
            "<bookmark mark='c'/>The pronouns he and it pick up referents introduced earlier, so the second sentence "
            "adds beats x y to the same box. <bookmark mark='d'/>In dynamic predicate logic, the conjunction of the "
            "two sentences, with the variables apparently free in the second, comes out equivalent to the single "
            "existential claim we want. <bookmark mark='e'/>The Reasoner checks it on the same four hundred models: "
            "they agree every time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(s))
            vo.wait_until("b")
            self.play(Create(box), FadeIn(refs), Create(line), FadeIn(conds[:3]), FadeIn(dtag), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(conds[3]), FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def dynamic(self):
        head = label(r"Meaning as context change", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"static", r"a sentence's meaning: \ its truth conditions, \ a set of worlds or assignments", SENSE),
            (r"dynamic", r"a sentence's meaning: \ how it changes the information of whoever accepts it", REF),
            (r"why it matters", r"pronouns, \ presuppositions \ (Strawson's, \ from chapter 4), \ and `might' all "
                                r"depend on the context built so far", NAME),
            (r"where it leads", r"meaning as something we do with words: \ Part 28, \ \textit{Meaning in Use}", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "This was a change in the idea of meaning itself. <bookmark mark='a'/>On the static view, from Frege to "
            "Montague, the meaning of a sentence is its truth conditions. <bookmark mark='b'/>On the dynamic view, "
            "its meaning is its context change potential: the way it changes the information state of whoever "
            "accepts it. <bookmark mark='c'/>That matters for pronouns, for presuppositions like Strawson's, which a "
            "context must already satisfy, and for words like might, which comment on the information gathered so "
            "far. <bookmark mark='d'/>It also points toward the idea that meaning is something we do with words, "
            "which Part 28 takes up."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
