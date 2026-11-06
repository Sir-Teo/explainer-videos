from __future__ import annotations

import itertools

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Ersatz(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Ersatz worlds", r"Can worlds be representations instead?", lit=(1974, 1989),
                            part=PART)
        with self.voiceover("Chapter six. Ersatz worlds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.kinds()
        self.books()
        self.primitive()
        self.aliens()
        self.actualism()

    def kinds(self):
        head = label(r"Worlds without the plurality", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"linguistic", r"a world is a maximal consistent set of sentences: \ a complete book \ (Carnap, \ 1947; "
                            r"\ Jeffrey)", WORLD),
            (r"states of affairs", r"Plantinga \ (1974): \ a maximal possible state of affairs; \ the actual world is "
                                   r"the one that obtains", NAME),
            (r"ways", r"Stalnaker \ (1976): \ worlds are ways things might have been, \ properties the world might "
                      r"have had", CPT),
            (r"combinations", r"Armstrong \ (1989): \ recombinations of the actual particulars and universals", ABS),
            (r"what they share", r"worlds are actual, \ abstract representations; \ only one world is concrete: "
                                 r"ours", GOAL),
        ]
        g = rows_table(rows, top=1.8, gap=0.45, width=8.6, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Most philosophers who use possible worlds do not believe in Lewis's plurality. They take worlds to be "
            "ersatz: substitutes, representations of how things might have been. <bookmark mark='a'/>Linguistic "
            "ersatzism: a world is a maximal consistent set of sentences, a complete book about a world, in the "
            "tradition of Carnap's state descriptions. <bookmark mark='b'/>Alvin Plantinga: a world is a maximal "
            "possible state of affairs, and the actual world is the one that obtains. <bookmark mark='c'/>Robert "
            "Stalnaker: worlds are ways things might have been, properties the whole world might have had. "
            "<bookmark mark='d'/>David Armstrong: worlds are recombinations of the actual particulars and "
            "universals. <bookmark mark='e'/>What they share: worlds are actual things, abstract ones, and there is "
            "only one concrete world, ours."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def books(self):
        head = label(r"Carnap's state descriptions", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        atoms = [r"Fa", r"Fb", r"Ga", r"Gb"]
        W = list(itertools.product([1, 0], repeat=4))
        books = VGroup()
        for i, w in enumerate(W):
            c = np.array([-5.7 + 1.18 * (i % 8), 1.35 - 1.6 * (i // 8), 0])
            b = RoundedRectangle(width=1.0, height=1.3, corner_radius=0.08, color=WORLD, stroke_width=2,
                                 fill_opacity=0.08).move_to(c)
            t = VGroup(*[MathTex(a if v else r"\lnot " + a, font_size=17, color=WHITE if v else GREY_B)
                         for a, v in zip(atoms, w)]).arrange(DOWN, buff=0.05).move_to(c)
            books.add(VGroup(b, t))
        true_one = SurroundingRectangle(books[5], color=NAME, buff=0.06, stroke_width=4)
        tl = label(r"the true book", font_size=17, color=NAME).next_to(true_one, DOWN, buff=0.08)
        rows = stack([(r"two individuals, \ two predicates: \ $2^4 = 16$ complete, \ consistent descriptions", WHITE),
                      (r"necessary: \ in every book; \ \ possible: \ in some book", ABS),
                      (r"`$\forall x\, Fx$' is in 4 books; \ `$Fa \lor \lnot Fa$' in all 16", CPT),
                      (r"the actual world: \ the one book that is true", NAME)],
                     font_size=21, aligned_edge=LEFT, width=12.0).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The linguistic version is easy to build. <bookmark mark='a'/>Take a tiny language: two individuals, a "
            "and b, and two predicates, F and G. A state description says, of each atomic sentence, whether it or "
            "its negation holds. There are two to the fourth, sixteen of them. Each is a complete, consistent book "
            "about a possible world. <bookmark mark='b'/>Then necessary means: in every book; possible means: in some "
            "book. <bookmark mark='c'/>For all x, F x is in four of the books; F a or not F a is in all sixteen. "
            "<bookmark mark='d'/>And one book is special, not because it is concrete but because it is true. That "
            "book is the actual world. No talking donkeys are required, only sentences."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(b) for b in books], lag_ratio=0.05), FadeIn(rows[0]),
                      run_time=2.5)
            for mk, r in zip("bc", rows[1:3]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(Create(true_one), FadeIn(tl), FadeIn(rows[3]))
        self.clear_scene()

    def primitive(self):
        head = label(r"Lewis's first objection: \ primitive modality", font_size=30, color=CONN).to_edge(UP,
                                                                                                     buff=0.35)
        rows = stack([(r"which sets of sentences count as worlds? \ the \textit{consistent} ones", WHITE),
                      (r"consistent in the narrow sense, \ by logic alone? \ then `$a$ is red and green all over' "
                       r"gets a world", BAD),
                      (r"consistent in the broad sense: \ \textit{possibly} true together", GOAL),
                      (r"so the account uses possibility, \ and cannot reduce it", BAD),
                      (r"the ersatzer's reply: \ we wanted a semantics, \ not a reduction; \ modality may be "
                       r"primitive", OK)], font_size=22, aligned_edge=LEFT, width=12.0, buff=0.35).move_to([0, -0.2,
                                                                                                         0])
        with self.voiceover(
            "Lewis pressed two objections. <bookmark mark='a'/>First: which sets of sentences are worlds? The "
            "consistent ones. <bookmark mark='b'/>Consistent in the narrow sense, by logic alone? Then the sentence "
            "this patch is red all over and green all over gets a world, since logic alone does not rule it out. "
            "<bookmark mark='c'/>So it must be consistent in the broad sense: possibly true together. "
            "<bookmark mark='d'/>But then the account uses the notion of possibility in saying what a world is. It "
            "cannot reduce modality to anything else. Lewis's worlds explained possibility; ersatz worlds presuppose "
            "it. <bookmark mark='e'/>Most ersatzers accept the charge. They wanted a semantics that makes modal "
            "reasoning precise, not a reduction; and modality, they say, may simply be primitive."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def aliens(self):
        d = load("aliens")
        head = label(r"Lewis's second objection: \ alien properties", font_size=30, color=CONN).to_edge(UP,
                                                                                                    buff=0.3)
        w1 = island([-4.6, 1.1, 0], w=3.0, h=1.5, seed=140, color=WORLD, name=r"world 1")
        w2 = island([-0.6, 1.1, 0], w=3.0, h=1.5, seed=141, color=WORLD, name=r"world 2")
        t1 = VGroup(label(r"$a$: \ F, \ X", font_size=19, color=WHITE), label(r"$b$: \ G, \ Y", font_size=19,
                                                                              color=WHITE)).arrange(
            DOWN, buff=0.1).move_to(w1.shape)
        t2 = VGroup(label(r"$a$: \ F, \ Y", font_size=19, color=WHITE), label(r"$b$: \ G, \ X", font_size=19,
                                                                              color=WHITE)).arrange(
            DOWN, buff=0.1).move_to(w2.shape)
        book = RoundedRectangle(width=3.6, height=1.5, corner_radius=0.1, color=NAME, fill_opacity=0.08).move_to(
            [4.0, 1.1, 0])
        bt = VGroup(label(r"$Fa$, \ $Gb$", font_size=19, color=NAME),
                    label(r"some alien property holds of $a$ alone, \ and another of $b$ alone", font_size=15,
                          color=NAME)).arrange(DOWN, buff=0.1)
        if bt[1].width > 3.3:
            bt[1] = wrapped_label(r"some alien property holds of $a$ alone, \ and another of $b$ alone", 3.3, 15,
                                  NAME)
            bt.arrange(DOWN, buff=0.1)
        bt.move_to(book)
        a1 = Arrow(w1.shape.get_bottom(), book.get_bottom(), buff=0.1, color=GREY_B, stroke_width=2,
                   path_arc=0.6)
        a2 = Arrow(w2.shape.get_right(), book.get_left(), buff=0.15, color=GREY_B, stroke_width=2)
        hd = [r"", r"\text{count}"]
        rows = [[label(r"genuine worlds \ (F, \ G and two alien properties X, \ Y, \ over $a$, \ $b$)",
                       font_size=18), MathTex(str(d["genuine"]), font_size=24, color=WORLD)],
                [label(r"distinct descriptions in the actual vocabulary", font_size=18),
                 MathTex(str(d["ersatz"]), font_size=24, color=NAME)],
                [label(r"descriptions that stand for more than one world", font_size=18),
                 MathTex(str(d["collapsed_descriptions"]), font_size=24, color=BAD)],
                [label(r"worlds lost in those descriptions", font_size=18),
                 MathTex(str(d["worlds_in_collapsed"]), font_size=24, color=BAD)]]
        grid = ValueGrid(hd, rows, col_w=[8.4, 1.6], cell_h=0.48, font_size=19).move_to([-0.6, -1.85, 0])
        with self.voiceover(
            "The second objection is subtler. <bookmark mark='a'/>Suppose there could have been properties that "
            "nothing actual has and that nothing actual is made of: alien properties, X and Y. In world one, a has X "
            "and b has Y; in world two, the other way round. Two different possibilities. <bookmark mark='b'/>An "
            "ersatz book is written in our vocabulary, which has no names for X and Y. The best it can do is say "
            "that some alien property holds of a alone, and another of b alone. Both worlds get the same "
            "description. <bookmark mark='c'/>The Reasoner counts. Over two individuals, with our two properties and "
            "two alien ones, there are two hundred and fifty-six genuine possibilities. <bookmark mark='d'/>In the "
            "actual vocabulary only one hundred and sixty distinct descriptions are possible. "
            "<bookmark mark='e'/>Ninety-six of them each stand for two worlds that differ only by swapping the alien "
            "properties: a hundred and ninety-two worlds whose differences cannot be told apart. Linguistic "
            "ersatzism undercounts the possibilities, unless the language is enriched with names for things that do "
            "not exist."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(w1), FadeIn(t1), FadeIn(w2), FadeIn(t2))
            vo.wait_until("b")
            self.play(FadeIn(book), FadeIn(bt), GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(grid.cell[0][0]), FadeIn(grid.cell[0][1]))
            vo.wait_until("d")
            self.play(FadeIn(grid.cell[1][0]), FadeIn(grid.cell[1][1]))
            vo.wait_until("e")
            self.play(*[FadeIn(grid.cell[r][c]) for r in (2, 3) for c in (0, 1)])
        self.clear_scene()

    def actualism(self):
        head = label(r"Actualism, \ and the people who might have been", font_size=30, color=CONN).to_edge(UP,
                                                                                                       buff=0.35)
        rows = [
            (r"actualism", r"everything that exists actually exists: \ there are no merely possible things", NAME),
            (r"the problem", r"`there could have been someone distinct from everyone actual': \ how can an actual "
                             r"book describe \textit{that} person?", BAD),
            (r"Plantinga", r"by individual essences: \ uninstantiated properties that \textit{would} have made "
                           r"something that person", ABS),
            (r"the worry", r"properties of being a given possible person, \ which exist though nobody has them", GOAL),
            (r"next", r"perhaps the possible person exists after all, \ but not concretely", CPT),
        ]
        g = rows_table(rows, top=1.8, gap=0.45, width=8.6, x_text=-2.6, label_size=21)
        with self.voiceover(
            "Ersatz views are usually actualist. <bookmark mark='a'/>Everything that exists actually exists; there are "
            "no merely possible people or donkeys waiting in the wings. <bookmark mark='b'/>But there could have "
            "been someone distinct from everyone who actually exists: a child your grandparents never had. An "
            "actual book must somehow describe that very person, who is not there to be named. <bookmark mark='c'/>"
            "Plantinga's answer was individual essences: properties, existing though uninstantiated, that would "
            "have made something that particular person. <bookmark mark='d'/>Critics found them as mysterious as "
            "the possible people they replace. <bookmark mark='e'/>Which suggests a bolder thought: perhaps the "
            "possible person does exist, only not concretely. That is the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
