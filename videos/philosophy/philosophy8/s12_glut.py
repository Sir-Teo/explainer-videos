from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Glut(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"True contradictions?", r"What if the liar is both true and false?", lit=(1979,),
                            part=PART)
        with self.voiceover("Chapter eleven. True contradictions?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.view()
        self.same_table()
        self.schema()
        self.prices()
        self.naive()

    def view(self):
        hc = history_card(1979, r"Graham Priest", r"`The logic of paradox'; \ \textit{In Contradiction} (1987)",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(label(r"dialetheism: \ some contradictions are true", font_size=30, color=GLUT),
                      label(r"the liar is both true and false; \ the argument of the hook was \textit{sound}",
                            font_size=26),
                      label(r"keep the T-schema, \ keep self-reference, \ keep excluded middle", font_size=26,
                            color=OK),
                      label(r"give up: \ `no contradiction is true', \ and with it explosion \ (LP, Part 5)",
                            font_size=26, color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.3, 0])
        with self.voiceover(
            "Graham Priest's answer, from 1979, is the boldest. <bookmark mark='a'/>Dialetheism: some contradictions "
            "are true. <bookmark mark='b'/>The liar is both true and false, and the argument at the start of this "
            "part was sound. <bookmark mark='c'/>Everything else is kept: the T-schema for every sentence, "
            "self-reference, even excluded middle. <bookmark mark='d'/>What goes is the principle that no "
            "contradiction is true, and with it the rule of explosion. The logic is LP, the logic of paradox from "
            "Part 5, in which a contradiction does not entail everything."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()

    def same_table(self):
        d = load("lp")
        k = load("fixed")["lfp"]
        head = label(r"The same construction, \ read the other way", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        names = ["s1", "s5", "s9", "L", "H", "A", "s8"]
        hd = [label(r"sentence", font_size=22, color=P.CLAIM), label(r"Kripke: \ a gap", font_size=22,
                                                                      color=P.CLAIM),
              label(r"Priest: \ a glut", font_size=22, color=P.CLAIM)]
        rows = [[label(rf"\textbf{{{n}}}: \ {Tr.GLOSS[n].replace('‘', '`').replace('’', chr(39))}", font_size=21),
                 value_chip(k[n], 22), value_chip(d["glut"][n], 22)] for n in names]
        grid = ValueGrid(hd, rows, col_w=[5.4, 2.4, 2.4], cell_h=0.52, font_size=22).move_to([0, -0.1, 0])
        note = label(r"$K_3$ and LP share their tables: \ the middle value read as `neither', \ or as `both' \ "
                     r"(the duality of Part 5)", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Here is a pleasing fact, which the Reasoner makes visible. <bookmark mark='a'/>Run Kripke's "
            "construction, but read the middle value not as 'neither' but as 'both'. Start with every sentence both "
            "true and false, and let the facts strip away what does not hold. <bookmark mark='b'/>The grounded "
            "sentences come out exactly as before. The liar, the truth-teller, the cycle: all both true and false. "
            "<bookmark mark='c'/>The tables of K3 and LP are the same; only the reading of the middle value "
            "differs. A gap and a glut are mirror images, the duality of Part 5."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(len(rows))])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][1]) for r in range(len(rows))], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][2], scale=0.7) for r in range(len(rows))], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.clear_scene()


    def schema(self):
        d = load("schema")
        head = label(r"Who keeps the whole T-schema?", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        names = ["s1", "s5", "L", "H", "A"]
        hd = [label(r"T-biconditional", font_size=22, color=P.CLAIM), label(r"its value", font_size=22,
                                                                             color=P.CLAIM),
              label(r"in $K_3$ (gap)", font_size=22, color=P.CLAIM), label(r"in LP (glut)", font_size=22,
                                                                           color=P.CLAIM)]
        rows = []
        for n in names:
            v = d["values"][n]
            rows.append([MathTex(rf"T\ulcorner {n} \urcorner \leftrightarrow {n}", font_size=28), value_chip(v, 22),
                         label(r"holds" if v == "t" else r"fails", font_size=22, color=OK if v == "t" else BAD),
                         label(r"holds", font_size=22, color=OK)])
        grid = ValueGrid(hd, rows, col_w=[3.6, 2.0, 2.6, 2.6], cell_h=0.55, font_size=22).move_to([0, -0.1, 0])
        note = label(r"designated values: \ only t in $K_3$; \ t and b in LP: \ so the middle value keeps every "
                     r"biconditional", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "There is a sharp difference between the gap and the glut. <bookmark mark='a'/>Compute the "
            "T-biconditional for each sentence: 'A' is true if and only if A. In the least fixed point, it has "
            "value true for the grounded sentences, and the middle value for the liar and its kin. "
            "<bookmark mark='b'/>In K3, only true counts as holding, so the T-schema fails for every ungrounded "
            "sentence. Kripke's theory satisfies the T-schema only where it is safe. <bookmark mark='c'/>In LP, the "
            "middle value means both true and false, and counts as holding. So the glut theorist keeps every "
            "T-biconditional, which is exactly what Priest claims as dialetheism's advantage."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(len(rows))])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][1]) for r in range(len(rows))], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][2]) for r in range(len(rows))], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(grid.cell[r][3]) for r in range(len(rows))], lag_ratio=0.2), FadeIn(note))
        self.clear_scene()

    def prices(self):
        head = label(r"The price of a glut", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            VGroup(label(r"modus ponens fails", font_size=26, color=BAD),
                   label(r"in LP, \ $A$ and $A \to B$ do not entail $B$ \ (take $A$ both, $B$ false); \ Priest adds a "
                         r"stronger conditional, \ and must then face Curry", font_size=22, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"`just true' is revenge", font_size=26, color=BAD),
                   label(r"`this sentence is false and not also true' \ pushes for a new glut", font_size=22,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"disagreement gets harder", font_size=26, color=BAD),
                   label(r"if asserting $\lnot A$ does not exclude $A$, \ how does one deny anything?", font_size=22,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"in return", font_size=26, color=OK),
                   label(r"one uniform solution to every paradox in the inclosure family", font_size=22,
                         color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.2, 0])
        with self.voiceover(
            "The price is real. <bookmark mark='a'/>In LP, modus ponens fails: if A is both true and false and B is "
            "false, then A and 'if A then B' are both true, yet B is not. Priest adds a stronger conditional, which "
            "must then be kept safe from Curry. <bookmark mark='b'/>Revenge returns as 'just true': a sentence that "
            "says it is false and not also true. <bookmark mark='c'/>And disagreement becomes harder to express: if "
            "asserting not A does not rule out A, how does anyone deny anything? Priest's answer is that denial is "
            "a speech act of its own. <bookmark mark='d'/>In return, dialetheism offers one solution for the whole "
            "inclosure family, sets and truth alike."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()

    def naive(self):
        hcs = VGroup(history_card(1989, r"Ross Brady", r"naive set theory in a relevant logic is non-trivial",
                                  width=5.6, color=HIST),
                     history_card(2010, r"Zach Weber", r"transfinite numbers in paraconsistent set theory",
                                  width=5.6, color=HIST)).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        rows = VGroup(
            label(r"if the liar may be both, \ why not Russell's set?", font_size=26),
            label(r"keep naive comprehension, \ every condition a set \ (Part 6's dream)", font_size=26, color=GOAL),
            label(r"in a suitable paraconsistent logic, \ Russell's set both belongs and does not, \ and nothing "
                  r"explodes", font_size=24),
            label(r"the work in progress: \ how much ordinary mathematics can be recovered?", font_size=24,
                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(hcs, DOWN, buff=0.5)
        with self.voiceover(
            "If the liar may be both true and false, why not Russell's set as well? <bookmark mark='a'/>Dialetheists "
            "have tried to keep Part 6's dream: naive comprehension, a set for every condition. "
            "<bookmark mark='b'/>Ross Brady proved in 1989 that naive set theory in a suitable relevant logic is not "
            "trivial: Russell's set both belongs to itself and does not, and the contradiction stays contained. "
            "<bookmark mark='c'/>Zach Weber has since developed ordinals and cardinals in such a theory. "
            "<bookmark mark='d'/>Whether enough of ordinary mathematics can be recovered to make the price "
            "worth paying is still being worked out."
        ) as vo:
            self.play(FadeIn(hcs))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
