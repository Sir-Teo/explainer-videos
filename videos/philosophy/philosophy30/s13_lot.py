from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


class LOT(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"The language of thought", r"Do we think in sentences?", lit=(1975, 1988), part=PART)
        with self.voiceover("Chapter twelve. The language of thought."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lot()
        self.systematic()
        self.built()
        self.answers()

    def lot(self):
        hc = history_card(1975, r"Jerry Fodor", r"\textit{The Language of Thought}", width=5.4, color=HIST).to_corner(
            UL, buff=0.3)
        tree = VGroup(MathTex(r"\textsc{loves}(\textsc{john}, \textsc{mary})", font_size=36, color=SYM))
        tree.move_to([0, 1.0, 0])
        rows = stack([(r"thoughts are sentences in a mental language, \ `Mentalese'", SYM),
                      (r"with a compositional syntax: \ the meaning of the whole from the meanings of the parts", FUNC),
                      (r"thinking is computation: \ rules applied to symbols in virtue of their form", MIND),
                      (r"the computational theory of mind: \ the best account, \ Fodor said, \ because the only one",
                       GOAL)], font_size=21, aligned_edge=LEFT, width=12.0, buff=0.3).move_to([0, -1.2, 0])
        with self.voiceover(
            "Fodor's own theory of the mind was the language of thought, set out in 1975. "
            "<bookmark mark='a'/>Thoughts are sentences in a mental language, which he called Mentalese. "
            "<bookmark mark='b'/>Like any language it has a compositional syntax: the content of the thought that "
            "John loves Mary is built from the contents of John, loves and Mary. <bookmark mark='c'/>Thinking is "
            "computation: the application of rules to these mental sentences in virtue of their form, as a proof "
            "checker manipulates formulas. <bookmark mark='d'/>The computational theory of mind was, Fodor said, the "
            "best account we have, because it was the only one."
        ) as vo:
            self.play(FadeIn(hc), Write(tree))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def systematic(self):
        head = label(r"Systematicity \ (Fodor and Pylyshyn, \ 1988)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        a = MathTex(r"\textsc{loves}(\textsc{john}, \textsc{mary})", font_size=34, color=SYM).move_to([-3.0, 1.2, 0])
        b = MathTex(r"\textsc{loves}(\textsc{mary}, \textsc{john})", font_size=34, color=SYM).move_to([3.0, 1.2, 0])
        ar = DoubleArrow(a.get_right(), b.get_left(), buff=0.2, color=GREY_B)
        rows = stack([(r"whoever can think that John loves Mary can think that Mary loves John", MIND),
                      (r"a compositional system gets this for free: \ the same parts, \ recombined", OK),
                      (r"a network of associations need not: \ each capacity could be learned separately", BAD),
                      (r"so connectionism is either false, \ or a mere implementation of a language of thought", GOAL)],
                     font_size=21, aligned_edge=LEFT, width=12.0, buff=0.3).move_to([0, -0.9, 0])
        with self.voiceover(
            "In 1988 Fodor and Zenon Pylyshyn used the theory against neural networks. <bookmark mark='a'/>Thought is "
            "systematic: anyone who can think that John loves Mary can think that Mary loves John. "
            "<bookmark mark='b'/>A compositional system gets this for free: the same parts, recombined by the same "
            "rule. <bookmark mark='c'/>A network of learned associations need not: it could learn one capacity "
            "without the other. <bookmark mark='d'/>So, they argued, connectionism is either false as a theory of "
            "the mind, or a mere implementation of a language of thought."
        ) as vo:
            self.play(FadeIn(head), FadeIn(a), FadeIn(b), GrowArrow(ar))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def built(self):
        d = load("systematicity")
        head = label(r"A held-out word, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["train"] == 91 and d["test"] == 65 and d["table_right"] == 0 and d["comp_right"] == 65
        assert d["example"]["out"] == ["JUMP", "JUMP", "LOOK", "LOOK", "LOOK"]
        ex = VGroup(label(r"`jump twice and look thrice'", font_size=24, color=BEHAV), MathTex(r"\longrightarrow"),
                    MathTex(r"\textsc{jump}\;\textsc{jump}\;\textsc{look}\;\textsc{look}\;\textsc{look}", font_size=28,
                            color=FUNC)).arrange(RIGHT, buff=0.3).move_to([0, 1.8, 0])
        hd = [r"\text{learner}", r"\text{held-out commands with `jump', \ right}"]
        cells = [[label(r"a lookup table of the 91 training pairs", font_size=19, color=BAD),
                  MathTex(r"0 \text{ of } 65", font_size=24, color=BAD)],
                 [label(r"a compositional interpreter, \ told only what `jump' means", font_size=19, color=OK),
                  MathTex(r"65 \text{ of } 65", font_size=24, color=OK)]]
        grid = ValueGrid(hd, cells, col_w=[6.0, 4.6], cell_h=0.6, font_size=19).move_to([0, 0.1, 0])
        foot = stack([(r"commands: \ walk, \ run, \ look, \ jump; \ `twice', \ `thrice'; \ joined by `and'", GREY_A),
                      (r"in training, \ `jump' appears only alone: \ the `add a primitive' split of SCAN \ (Lake and "
                       r"Baroni, \ 2018)", SYM)], font_size=20, aligned_edge=LEFT, width=12.0, buff=0.2).to_edge(
            DOWN, buff=0.45)
        with self.voiceover(
            "The Reasoner sets up the test in a tiny command language, after Brenden Lake and Marco Baroni's SCAN. "
            "<bookmark mark='a'/>Commands like jump twice and look thrice mean sequences of actions: jump, jump, look, "
            "look, look. <bookmark mark='b'/>There are four verbs, two repeaters and the word and. In training, jump "
            "appears only on its own; ninety-one commands are seen, and sixty-five commands that combine jump with "
            "anything are held out. <bookmark mark='c'/>A lookup table of the training pairs gets none of the "
            "sixty-five right. A compositional interpreter, told only what jump means, gets all sixty-five. "
            "<bookmark mark='d'/>That is systematicity, in miniature: the capacity to use a part comes with the "
            "capacity to combine it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ex))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row])
            vo.wait_until("d")
            self.play(Indicate(grid.cell[1][1], color=OK))
        self.clear_scene()

    def answers(self):
        head = label(r"Networks answer back", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Lake and Baroni \ (2018)", r"standard sequence-to-sequence networks failed the held-out `jump' almost "
                                          r"completely", BAD),
            (r"Lake and Baroni \ (2023)", r"a network meta-trained on many such tasks generalized systematically, \ "
                                          r"and made human-like errors", OK),
            (r"large language models", r"strong on many compositional tasks, \ uneven on others: \ the question is "
                                       r"now empirical", FUNC),
            (r"the stakes", r"if networks can be systematic without explicit symbols, \ the language of thought is not "
                            r"the only game in town", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "The networks answered back, slowly. <bookmark mark='a'/>In 2018 Lake and Baroni found that standard "
            "sequence-to-sequence networks failed the held-out jump test almost completely. "
            "<bookmark mark='b'/>In 2023 the same authors showed that a network meta-trained on many such "
            "composition tasks generalized systematically, and even made the same kinds of errors people make. "
            "<bookmark mark='c'/>Large language models are strong on many compositional tasks and uneven on others. "
            "<bookmark mark='d'/>The question Fodor and Pylyshyn posed as a matter of principle has become an "
            "empirical one: if networks can be systematic without explicit symbols, the language of thought is not "
            "the only game in town."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
