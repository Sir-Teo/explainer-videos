from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


class Tarski(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Truth and meaning", r"Can a theory of truth be a theory of meaning?",
                            lit=(1933, 1967, 1976), part=PART)
        with self.voiceover("Chapter eight. Truth and meaning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.convention()
        self.derive()
        self.davidson()
        self.foster()

    def convention(self):
        hc = history_card(1933, r"Alfred Tarski", r"`The Concept of Truth in Formalized Languages'", width=6.8,
                          color=HIST).to_corner(UL, buff=0.3)
        t = MathTex(r"\text{`snow is white' is true} \iff \text{snow is white}", font_size=36, color=TRUTH).move_to(
            [0, 1.0, 0])
        gen = MathTex(r"\text{`}S\text{' is true} \iff p", font_size=34, color=SENSE).next_to(t, DOWN, buff=0.45)
        rows = stack([(r"Convention T: \ an adequate definition of truth must entail every such sentence", WHITE),
                      (r"quoted on the left: \ the object language; \ used on the right: \ the metalanguage", NAME),
                      (r"for a language with quantifiers, \ truth is defined through satisfaction by assignments", WORLD),
                      (r"and never inside the language itself: \ Part 8's liar forbids it", BAD)], font_size=21,
                     aligned_edge=LEFT, width=11.6, buff=0.26).move_to([0, -1.7, 0])
        with self.voiceover(
            "The tools for a theory of meaning came from the theory of truth. <bookmark mark='a'/>In 1933 Alfred "
            "Tarski set a condition on any definition of truth. Snow is white, in quotation marks, is true if and "
            "only if snow is white. <bookmark mark='b'/>In general: S is true if and only if p, where p translates S. "
            "Tarski's Convention T requires an adequate definition to entail every such sentence. "
            "<bookmark mark='c'/>On the left the sentence is mentioned, in the object language; on the right it is "
            "used, in the metalanguage. <bookmark mark='d'/>For a language with quantifiers, truth is defined by way "
            "of satisfaction, a relation between formulas and assignments of objects to variables: the same "
            "recursion the Reasoner's model checker runs. <bookmark mark='e'/>And, as Part 8 showed, the definition "
            "must be given in a richer metalanguage, never inside the language itself, or the liar returns."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(t))
            vo.wait_until("b")
            self.play(Write(gen), FadeIn(rows[0]))
            for mk, r in zip("cde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def derive(self):
        d = load("tarski")
        head = label(r"A T-sentence, \ derived", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        axioms = stack([(r"`snow is white' is true iff snow is white \ (and so for each atom)", NAME),
                        (r"`$A$ and $B$' is true iff $A$ is true and $B$ is true; \ likewise `or'", SENSE),
                        (r"`not $A$' is true iff it is not the case that $A$ is true", SENSE)], font_size=19,
                       aligned_edge=LEFT, width=12.0, buff=0.15).move_to([0, 2.2, 0])
        steps = d["steps"]
        assert "T(" not in steps[-1] and d["value"] is True and len(steps) == 4

        def fmt(s):
            return s.replace("T(", r"\textbf{T}(")

        lines = VGroup()
        for i, s in enumerate(steps):
            lab = wrapped_label((r"$\iff$ \ " if i else "") + fmt(s), 12.4, 19, TRUTH if i == len(steps) - 1 else
                                (REF if i == 0 else WHITE))
            lines.add(lab)
        lines.arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([0, -0.5, 0])
        val = label(r"evaluated in the actual world: \ true", font_size=21, color=OK).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Reasoner derives T-sentences for a small language. <bookmark mark='a'/>It has three atomic "
            "sentences, each with its own axiom, and one axiom for each connective. <bookmark mark='b'/>Start with a "
            "compound sentence: not snow is green, and, grass is green or snow is green. Ask when it is true. "
            "<bookmark mark='c'/>The axiom for and splits it in two. <bookmark mark='d'/>The axioms for not and or "
            "split the parts. <bookmark mark='e'/>The atomic axioms remove the last mention of truth, leaving a "
            "condition stated in the metalanguage: a T-sentence, derived from finitely many axioms. "
            "<bookmark mark='f'/>Evaluated in the actual world, it is true."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(axioms))
            for mk, l in zip("bcde", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l, shift=DOWN * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(val))
        self.clear_scene()

    def davidson(self):
        hc = history_card(1967, r"Donald Davidson", r"`Truth and Meaning'", width=5.2, color=HIST).to_corner(UL,
                                                                                                         buff=0.3)
        rows = [
            (r"the proposal", r"a theory of meaning for a language is a finite truth theory \ that entails a "
                              r"T-sentence for every sentence", SENSE),
            (r"learnability", r"finitely many axioms, \ infinitely many sentences: \ how a finite mind can understand "
                              r"a language", OK),
            (r"no meanings needed", r"`$S$ means that $p$' is replaced by `$S$ is true iff $p$'", NAME),
            (r"radical interpretation", r"a field linguist builds such a theory from which sentences speakers hold "
                                        r"true, \ assuming they are mostly right: \ charity", WORLD),
        ]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "In 1967 Donald Davidson turned Tarski's tool around. Tarski used meaning to define truth; Davidson used "
            "truth to explain meaning. <bookmark mark='a'/>A theory of meaning for a language, he proposed, is a "
            "finite truth theory that entails a T-sentence for every sentence of the language. "
            "<bookmark mark='b'/>Because the axioms are finite and the sentences infinite, such a theory shows how a "
            "finite mind can understand a language. <bookmark mark='c'/>And it needs no entities called meanings: "
            "S means that p is replaced by S is true if and only if p. <bookmark mark='d'/>How would we find such a "
            "theory for an unknown language? By radical interpretation: observe which sentences speakers hold true "
            "in which circumstances, and assume, by a principle of charity, that they are mostly right."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def foster(self):
        d = load("foster")
        head = label(r"Foster's problem", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        good = label(r"theory A: \ `snow is white' is true iff \textit{snow is white}", font_size=23, color=OK)
        bad = label(r"theory B: \ `snow is white' is true iff \textit{grass is green}", font_size=23, color=BAD)
        pair = VGroup(good, bad).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 1.6, 0])
        assert d["agree_actual"] == d["n"] == 99 and d["n"] - d["agree_other"] == 29
        hd = [r"\text{world}", r"\text{sentences}", r"\text{A and B agree on}"]
        cells = [[label(r"actual", font_size=21, color=WORLD), MathTex(str(d["n"]), font_size=24),
                  MathTex(str(d["agree_actual"]), font_size=24, color=OK)],
                 [label(r"grass is not green", font_size=21, color=WORLD), MathTex(str(d["n"]), font_size=24),
                  MathTex(str(d["agree_other"]), font_size=24, color=BAD)]]
        grid = ValueGrid(hd, cells, col_w=[3.6, 2.4, 3.4], cell_h=0.5, font_size=21).move_to([0, 0.0, 0])
        rows = stack([(r"theory B's T-sentences are all true: \ it fits every fact, \ yet gives the wrong meaning", BAD),
                      (r"Davidson's reply: \ the theory must hold as a law, \ across counterfactual circumstances", OK),
                      (r"truth conditions are not enough; \ modal facts must be added", GOAL)], font_size=21,
                     aligned_edge=LEFT, width=11.6, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1976 John Foster found a problem. <bookmark mark='a'/>Take the right theory, and a deviant one whose "
            "axiom says snow is white is true if and only if grass is green. <bookmark mark='b'/>Since snow is white "
            "and grass is green, the deviant theory's T-sentences are all true. The Reasoner compares the two theories "
            "on ninety-nine sentences of the small language: in the actual world they agree on every one. "
            "<bookmark mark='c'/>In a world where grass is not green, they disagree on twenty-nine. "
            "<bookmark mark='d'/>So a truth theory can fit all the facts and still give the wrong meanings. "
            "<bookmark mark='e'/>Davidson's reply was to require more: the theory must hold as a law, supporting "
            "counterfactuals, which brings back exactly the modal facts that truth conditions in one world leave "
            "out. The next chapters build those modal facts in."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pair[0]))
            self.play(FadeIn(pair[1]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for c in grid.cell[0]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[1]])
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
        self.clear_scene()
