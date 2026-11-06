from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Quine(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"On what there is", r"What does a theory say there is?", lit=(1948, 1984),
                            part=PART)
        with self.voiceover("Chapter one. On what there is."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.beard()
        self.criterion()
        self.plurals()
        self.razor()
        self.gavagai()

    def beard(self):
        hc = history_card(1948, r"W. V. O. Quine", r"`On What There Is'", width=5.0, color=HIST).to_corner(
            UL, buff=0.35)
        rows = stack([(r"`Pegasus does not exist' \ seems to be about Pegasus", WHITE),
                      (r"so Pegasus must \textit{be}, \ in some sense, \ to be denied: \ `Plato's beard'", BAD),
                      (r"McX: \ Pegasus is an idea in the mind; \ \ Wyman: \ Pegasus is an unactualized possible", NOM),
                      (r"Quine: \ the name is a disguised predicate: \ $\lnot \exists x \, \mathit{Pegasizes}(x)$",
                       OK),
                      (r"denying existence commits you to nothing", GOAL)], font_size=21, aligned_edge=LEFT,
                     width=9.0).move_to([0.4, -0.5, 0])
        with self.voiceover(
            "Quine begins with an old riddle, which he called Plato's beard, because it had dulled the edge of "
            "Ockham's razor. <bookmark mark='a'/>The sentence Pegasus does not exist seems to be about Pegasus. "
            "<bookmark mark='b'/>Then Pegasus must in some sense be, or there would be nothing for the sentence to "
            "deny. <bookmark mark='c'/>Quine's imaginary opponents offer homes: McX says Pegasus is an idea in our "
            "minds; Wyman says he is an unactualized possible. <bookmark mark='d'/>Quine's answer follows Russell: "
            "treat the name as a disguised predicate, being Pegasus, or pegasizing, and say that nothing pegasizes. "
            "<bookmark mark='e'/>Then denying that Pegasus exists commits you to nothing at all."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def criterion(self):
        head = label(r"`To be is to be the value of a variable'", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{sentence}", r"\text{regimented}", r"\text{commits to}"]
        data = [
            (r"\text{some dogs are white}", r"\exists x \, (Dx \land Wx)", r"\text{dogs}"),
            (r"\text{there is a prime between 10 and 20}", r"\exists n \, (Pn \land 10 < n < 20)",
             r"\text{numbers}"),
            (r"\text{Pegasus does not exist}", r"\lnot \exists x \, \mathit{Peg}(x)", r"\text{nothing}"),
            (r"\text{the average family has 2.3 children}", r"\text{(paraphrase it away)}", r"\text{no families}"),
            (r"\text{some species are cross-fertile}", r"\exists x \exists y \, (Sx \land Sy \land Cxy)",
             r"\text{species}"),
        ]
        rows = [[MathTex(a, font_size=22), MathTex(b, font_size=24, color=PARTC), MathTex(c, font_size=22,
                                                                                         color=WHOLE)]
                for a, b, c in data]
        grid = ValueGrid(hd, rows, col_w=[5.4, 4.2, 2.6], cell_h=0.62, font_size=20).move_to([0, 0.3, 0])
        notes = stack([(r"a theory is committed to whatever its bound variables must range over to make it true",
                        GOAL),
                       (r"commitment is a property of theories, \ not of the world: \ it says what a theory "
                        r"\textit{says} there is", GREY_A)], font_size=19, width=12.0).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Quine's criterion: to be is to be the value of a variable. <bookmark mark='a'/>Translate a theory into "
            "first-order logic. Some dogs are white becomes: there is an x that is a dog and white. The theory is "
            "committed to dogs. <bookmark mark='b'/>There is a prime between ten and twenty commits us to numbers. "
            "<bookmark mark='c'/>Pegasus does not exist commits us to nothing. <bookmark mark='d'/>Some sentences "
            "can be paraphrased away: the average family has two point three children does not commit us to an "
            "average family. <bookmark mark='e'/>Others resist: some species are cross-fertile quantifies over "
            "species. <bookmark mark='f'/>The criterion does not tell us what there is. It tells us what a theory "
            "says there is, so that ontological disputes become disputes about which theory to accept."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*grid.cell[r])))
            vo.wait_until("f")
            self.play(FadeIn(notes))
        self.clear_scene()

    def plurals(self):
        d = load("gk")
        head = label(r"`Some critics admire only one another'", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"\exists X \, \big( \exists x \, Xx \;\land\; \forall x \forall y \, ((Xx \land Axy) \to "
                    r"(x \ne y \land Xy)) \big)", font_size=32, color=UNIV).next_to(head, DOWN, buff=0.3)
        graphs = VGroup()
        names = list(d)
        for k, nm in enumerate(names):
            g = d[nm]
            c = np.array([-4.4 + 4.4 * k, -0.8, 0])
            pos = [c + 1.05 * np.array([np.cos(PI / 2 + 2 * PI * i / 5), np.sin(PI / 2 + 2 * PI * i / 5), 0])
                   for i in range(5)]
            wit = set(g["witnesses"][0]) if g["witnesses"] else set()
            dots = VGroup(*[Dot(p, radius=0.13, color=OK if i in wit else GREY_B) for i, p in enumerate(pos)])
            arrows = VGroup()
            for a, b in g["edges"]:
                if a == b:
                    arrows.add(Circle(radius=0.16, color=BAD, stroke_width=2.5).move_to(pos[a] + UP * 0.25))
                else:
                    arrows.add(Arrow(pos[a], pos[b], buff=0.16, color=GREY_A, stroke_width=2.5,
                                     max_tip_length_to_length_ratio=0.18))
            verdict = label((r"true: \ e.g. \ $\{" + ", ".join(str(i) for i in sorted(wit)) + r"\}$") if g["true"]
                            else r"false", font_size=18, color=OK if g["true"] else BAD).next_to(dots, DOWN,
                                                                                                buff=0.35)
            title = label(nm, font_size=17, color=GREY_A).next_to(dots, UP, buff=0.45)
            graphs.add(VGroup(arrows, dots, verdict, title))
        rows = stack([(r"Geach and Kaplan: \ no first-order sentence says this; \ it quantifies over pluralities", BAD),
                      (r"the Reasoner checks all " + f"{d[names[0]]['checked']}" + r" nonempty groups of five critics",
                       GREY_A),
                      (r"Boolos \ (1984): \ plural quantification is innocent: \ `some critics' commits only to "
                       r"critics, \ not to sets", GOAL)], font_size=19, width=12.4).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Peter Geach offered a sentence that tests the criterion: some critics admire only one another. "
            "<bookmark mark='a'/>It says there is a group of critics such that whenever one of them admires someone, "
            "that someone is another member of the group. David Kaplan proved that no first-order sentence about "
            "critics expresses this: the quantifier ranges over groups. <bookmark mark='b'/>The Reasoner checks it "
            "on three admiration networks among five critics, trying all thirty-one nonempty groups. "
            "<bookmark mark='c'/>In the first, a closed circle of mutual admirers makes it true. In the second, "
            "everyone's admiration leads to a self-admirer, so it is false. In the third, a ring, only the whole "
            "community will do. <bookmark mark='d'/>So does the sentence commit us to groups, or sets, as entities? "
            "George Boolos argued no: plural quantification, some critics, is ontologically innocent; it commits us "
            "only to critics, taken many at a time."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(VGroup(g[0], g[1], g[3])) for g in graphs], lag_ratio=0.3),
                      FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(g[2]) for g in graphs], lag_ratio=0.6), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def razor(self):
        head = label(r"Desert landscapes", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Ockham's razor", r"entities are not to be multiplied beyond necessity", GOAL),
            (r"`no entity without identity'", r"Quine: \ admit only things with clear identity conditions: \ "
                                              r"possible fat men in doorways have none", BAD),
            (r"a taste", r"Quine's `taste for desert landscapes': \ physical objects and sets, \ nothing more", PARTC),
            (r"indispensability", r"Quine and Putnam: \ science quantifies over numbers, \ so we must accept them "
                                  r"\ (Part 9)", UNIV),
            (r"the question left", r"commitment tells us what a theory says; \ which theory to believe is still open",
             GREY_A),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Quine paired his criterion with a strict standard of admission. <bookmark mark='a'/>Ockham's razor: do "
            "not multiply entities beyond necessity. <bookmark mark='b'/>And: no entity without identity. Consider "
            "the possible fat man in that doorway, and the possible bald man in it. Are they the same possible man, "
            "or two? There is no fact of the matter, Quine said, so possibilia are not respectable entities. "
            "<bookmark mark='c'/>He confessed a taste for desert landscapes: physical objects and sets, and nothing "
            "else. <bookmark mark='d'/>Sets stay because science needs mathematics, the indispensability argument of "
            "Part 9. <bookmark mark='e'/>The criterion settles what a theory says there is. It does not settle which "
            "theory to believe, and the rest of this part is the argument."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def gavagai(self):
        hc = history_card(1968, r"W. V. O. Quine", r"`Ontological Relativity'", width=5.2, color=HIST).to_corner(
            UL, buff=0.35)
        rabbit = VGroup(Ellipse(width=1.6, height=0.9, color=GREY_A, fill_opacity=0.35),
                        Circle(radius=0.32, color=GREY_A, fill_opacity=0.35).shift(RIGHT * 0.85 + UP * 0.35),
                        Ellipse(width=0.16, height=0.6, color=GREY_A, fill_opacity=0.35).shift(RIGHT * 0.9 + UP * 0.85))
        rabbit.move_to([-4.6, -0.2, 0])
        word = label(r"`Gavagai!'", font_size=26, color=GOAL).next_to(rabbit, UP, buff=0.4)
        rows = [
            (r"rabbit", r"an enduring animal", OK),
            (r"undetached rabbit part", r"wherever there is one, \ there is the other", PARTC),
            (r"rabbit stage", r"a temporal slice: \ the topic of Part 21", WHOLE),
            (r"rabbithood", r"a universal, \ manifested here \ (chapter 3)", UNIV),
        ]
        g = rows_table(rows, x_label=-1.6, x_text=1.8, top=1.2, gap=0.42, width=4.8, label_size=20, text_size=19)
        moral = stack([(r"every observation fits every translation: \ reference is inscrutable", BAD),
                       (r"ontology is relative to a background language: \ `what is there?' \ needs a framework to "
                        r"be asked in", GREY_A)], font_size=19, width=12.0).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Quine later found that his own criterion has a limit. <bookmark mark='a'/>A linguist in the field hears a "
            "speaker say gavagai whenever a rabbit runs past. Does gavagai mean rabbit? <bookmark mark='b'/>It might "
            "mean undetached rabbit part, since wherever there is a rabbit there are its parts. Or rabbit stage, a "
            "brief temporal slice of a rabbit. Or rabbithood, the universal manifested here. "
            "<bookmark mark='c'/>Every possible observation fits every one of these translations. Quine concluded that "
            "reference is inscrutable. <bookmark mark='d'/>And so ontology is relative: what a theory says there is "
            "can only be asked against a background language, a theme that returns in chapter ten."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(rabbit))
            vo.wait_until("a")
            self.play(FadeIn(word))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.5), run_time=3)
            for mk, r in zip("cd", moral):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
