from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


def node(tex, col, at):
    t = MathTex(tex, font_size=26, color=col)
    box = SurroundingRectangle(t, color=col, buff=0.1, corner_radius=0.08, stroke_width=1.5)
    return VGroup(box, t).move_to(at)


def edge(a, b):
    return Line(a.get_bottom(), b.get_top(), color=GREY_C, stroke_width=2)


class Russell(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Russell's descriptions", r"What is `the present king of France' about?",
                            lit=(1905,), part=PART)
        with self.voiceover("Chapter three. Russell's theory of descriptions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.puzzles()
        self.theory()
        self.scope()
        self.legacy()

    def puzzles(self):
        hc = history_card(1905, r"Bertrand Russell", r"`On Denoting'", width=5.4, color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"excluded middle", r"`the present king of France is bald' or `\dots is not bald': \ one should be true; "
                                 r"\ but he is on neither list", REF),
            (r"negative existence", r"`the present king of France does not exist': \ what is it about?", NAME),
            (r"substitution", r"George IV wished to know whether Scott was the author of \textit{Waverley}; \ "
                              r"Scott was; \ yet George IV did not wish to know whether Scott was Scott", SPEAK),
        ]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        foot = label(r"Russell: \ `the Hegelians, \ who love a synthesis, \ will probably conclude that he wears a "
                     r"wig'", font_size=20, color=HIST).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1905 Bertrand Russell published On Denoting, about phrases like the present king of France. It "
            "solves three puzzles. <bookmark mark='a'/>Excluded middle: either the present king of France is bald, "
            "or he is not. But list the bald things and the things that are not bald, and he is on neither list. "
            "<bookmark mark='b'/>Negative existence: the present king of France does not exist. What is that "
            "sentence about, if there is nothing for it to be about? <bookmark mark='c'/>Substitution: George the "
            "Fourth wished to know whether Scott was the author of Waverley. Scott was the author of Waverley. Yet "
            "George the Fourth did not wish to know whether Scott was Scott. <bookmark mark='d'/>Of the first "
            "puzzle, Russell remarked that the Hegelians, who love a synthesis, will probably conclude that he wears "
            "a wig."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def theory(self):
        head = label(r"The theory", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        s = label(r"`the present king of France is bald'", font_size=30, color=TRUTH).move_to([0, 2.0, 0])
        f = MathTex(r"\exists x\, \big(", r"Kx", r"\;\wedge\;", r"\forall y\, (Ky \rightarrow y = x)", r"\;\wedge\;",
                    r"Bx", r"\big)", font_size=40).move_to([0, 0.8, 0])
        f[1].set_color(REF)
        f[3].set_color(NAME)
        f[5].set_color(SENSE)
        braces = VGroup(Brace(f[1], DOWN, color=REF), Brace(f[3], DOWN, color=NAME), Brace(f[5], DOWN, color=SENSE))
        btxt = VGroup(label(r"there is a king", font_size=19, color=REF).next_to(braces[0], DOWN, buff=0.1),
                      label(r"at most one", font_size=19, color=NAME).next_to(braces[1], DOWN, buff=0.1),
                      label(r"and he is bald", font_size=19, color=SENSE).next_to(braces[2], DOWN, buff=0.1))
        rows = stack([(r"`the K' is not a name: \ it has no meaning in isolation, \ and disappears on analysis", WHITE),
                      (r"with no king, \ the first conjunct is false, \ so the sentence is simply false", OK),
                      (r"`the K does not exist' becomes $\neg \exists x\,(Kx \wedge \forall y\,(Ky \rightarrow y = x))$: "
                       r"\ true, \ and about nothing", GOAL)], font_size=21, aligned_edge=LEFT, width=12.0,
                     buff=0.26).move_to([0, -1.9, 0])
        with self.voiceover(
            "Russell's answer is that the phrase is not a name at all. <bookmark mark='a'/>The present king of "
            "France is bald says three things at once. <bookmark mark='b'/>There is a king of France; "
            "<bookmark mark='c'/>there is at most one; <bookmark mark='d'/>and he is bald. "
            "<bookmark mark='e'/>The description has no meaning in isolation. It is an incomplete symbol: it "
            "disappears when the sentence is analysed, and leaves only quantifiers, a predicate and a variable. "
            "<bookmark mark='f'/>With no king, the first part is false, so the whole sentence is simply false. "
            "<bookmark mark='g'/>And the present king of France does not exist becomes: it is not the case that "
            "there is exactly one king. That is true, and it is about nothing at all, which solves the second "
            "puzzle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(s))
            vo.wait_until("a")
            self.play(Write(f))
            for mk, i in zip("bcd", range(3)):
                vo.wait_until(mk)
                self.play(GrowFromCenter(braces[i]), FadeIn(btxt[i]))
            for mk, r in zip("efg", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def scope(self):
        d = load("russell")
        head = label(r"Two scopes for `not'", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        # wide scope tree
        xL, xR = -3.7, -0.6
        w = [node(r"\neg", BAD, [xL, 2.0, 0]), node(r"\exists x", REF, [xL, 1.2, 0]), node(r"\wedge", GREY_A,
                                                                                         [xL, 0.4, 0]),
             node(r"Kx \wedge \forall y\,(Ky \rightarrow y = x)", NAME, [xL - 1.2, -0.5, 0]),
             node(r"Bx", SENSE, [xL + 1.4, -0.5, 0])]
        we = VGroup(edge(w[0], w[1]), edge(w[1], w[2]), edge(w[2], w[3]), edge(w[2], w[4]))
        wl = label(r"wide: \ it is not the case that the K is B", font_size=19, color=BAD).next_to(w[0], UP, buff=0.15)
        n = [node(r"\exists x", REF, [xR + 4.6, 2.0, 0]), node(r"\wedge", GREY_A, [xR + 4.6, 1.2, 0]),
             node(r"Kx \wedge \forall y\,(Ky \rightarrow y = x)", NAME, [xR + 3.4, 0.3, 0]),
             node(r"\neg", BAD, [xR + 6.0, 0.3, 0]), node(r"Bx", SENSE, [xR + 6.0, -0.5, 0])]
        ne = VGroup(edge(n[0], n[1]), edge(n[1], n[2]), edge(n[1], n[3]), edge(n[3], n[4]))
        nl = label(r"narrow: \ the K is not-B", font_size=19, color=OK).next_to(n[0], UP, buff=0.15)
        rows_d = d["rows"]
        keys = ["the K is B", "wide: not (the K is B)", "narrow: the K is not B"]
        hd = [r"\text{model}", r"\text{the K is B}", r"\text{wide } \neg", r"\text{narrow } \neg"]
        rows = [[label(r["model"], font_size=20, color=WORLD)] + [tv(r["values"][k], 22) for k in keys]
                for r in rows_d]
        grid = ValueGrid(hd, rows, col_w=[3.6, 2.2, 1.8, 2.0], cell_h=0.4, font_size=20).move_to([0, -2.3, 0])
        nk = next(r for r in rows_d if r["model"] == "no king")["values"]
        assert nk == {"the K is B": False, "wide: not (the K is B)": True, "narrow: the K is not B": False}
        with self.voiceover(
            "Now the first puzzle. The present king of France is not bald can be analysed in two ways, because the "
            "negation can go in two places. <bookmark mark='a'/>Wide scope: it is not the case that there is exactly "
            "one king who is bald. <bookmark mark='b'/>Narrow scope: there is exactly one king, and he is not bald. "
            "<bookmark mark='c'/>The Reasoner evaluates all three sentences in four models: no king, one bald king, "
            "one king with hair, and two kings. <bookmark mark='d'/>With no king, the plain sentence is false, the "
            "narrow negation is false too, and the wide negation is true. Excluded middle holds where it should, "
            "between a sentence and its wide negation, and the king needs no wig."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in w], lag_ratio=0.2), Create(we), FadeIn(wl))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(x) for x in n], lag_ratio=0.2), Create(ne), FadeIn(nl))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.4)
            vo.wait_until("d")
            self.play(*[Indicate(c, color=TRUTH) for c in grid.cell[0]])
        self.clear_scene()

    def legacy(self):
        head = label(r"A paradigm of philosophy", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the third puzzle", r"`George IV wished to know whether $\exists x\,(Wx \wedge \forall y\,(Wy \rightarrow "
                                  r"y = x) \wedge x = s)$': \ no name to substitute for", SPEAK),
            (r"Ramsey", r"called the theory `that paradigm of philosophy': \ grammar misleads, \ logic reveals",
             HIST),
            (r"names", r"Russell: \ ordinary names are disguised descriptions; \ `Homer' means `the author of the "
                       r"\textit{Iliad}'", NAME),
            (r"the target", r"descriptivism about names, \ shared by Frege and Russell: \ Kripke's target in "
                            r"chapter 5", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "The third puzzle dissolves the same way. <bookmark mark='a'/>Analysed, George the Fourth's wish "
            "contains no name for the author of Waverley, only quantifiers and a predicate, so there is nothing to "
            "substitute Scott for. <bookmark mark='b'/>Frank Ramsey called the theory that paradigm of philosophy: "
            "the grammar of a sentence can mislead about its logical form, and analysis reveals it. "
            "<bookmark mark='c'/>Russell went further. He held that ordinary proper names are disguised "
            "descriptions: Homer means something like the author of the Iliad. <bookmark mark='d'/>This view of "
            "names, shared in different forms by Frege and Russell, is called descriptivism. It was the received "
            "view for sixty years, until Saul Kripke attacked it, in chapter five."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
