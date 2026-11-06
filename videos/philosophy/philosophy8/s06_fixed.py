from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Fixed(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Grounded and paradoxical", r"What sets the liar apart from the truth-teller?",
                            lit=(1975,), part=PART)
        with self.voiceover("Chapter five. Grounded and paradoxical."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.many()
        self.classify()
        self.intrinsic()
        self.arithmetic()

    def many(self):
        d = load("fixed")
        head = label(r"Every fixed point, \ found by the Reasoner", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        show = ["s5", "s9", "L", "H", "s13", "s8", "A", "B"]
        hd = [label(r"sentence", font_size=22, color=P.CLAIM)] + [label(rf"fixed point {i + 1}", font_size=22,
                                                                         color=P.CLAIM) for i in range(len(d["fixed"]))]
        order = sorted(d["fixed"], key=lambda fp: "tfn".index(fp["H"]))
        rows = []
        for n in show:
            rows.append([label(rf"\textbf{{{n}}}: \ {Tr.GLOSS[n].replace('‘', '`').replace('’', chr(39))}",
                               font_size=21)] + [value_chip(fp[n], 22) for fp in order])
        grid = ValueGrid(hd, rows, col_w=[5.2, 2.0, 2.0, 2.0], cell_h=0.52, font_size=22).move_to([0, -0.3, 0])
        note = label(rf"the least fixed point is the third: \ it says only what it must", font_size=22,
                     color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The least fixed point is not the only one. <bookmark mark='a'/>The Reasoner searches every way of "
            "assigning true, false or neither to the sentences that the least fixed point leaves open, and keeps "
            "those that the construction would reproduce exactly. There are three. <bookmark mark='b'/>In all three, "
            "the grounded sentences keep their values, and the liar is neither. So is the liar cycle, A and B. "
            "<bookmark mark='c'/>The truth-teller differs. It can consistently be true, or false, or neither; and "
            "'the truth-teller is not true' follows along. <bookmark mark='d'/>The least fixed point, the third, "
            "is the one that says only what it must."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(len(rows))])
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid.head[c]) for c in range(1, 4)], lag_ratio=0.3))
            vo.wait_until("b")
            idx = [show.index(n) for n in ("s5", "s9", "L", "s8", "A", "B")]
            self.play(*[FadeIn(grid.cell[r][c], scale=0.7) for r in idx for c in range(1, 4)])
            vo.wait_until("c")
            idx2 = [show.index(n) for n in ("H", "s13")]
            self.play(*[FadeIn(grid.cell[r][c], scale=0.7) for r in idx2 for c in range(1, 4)])
            vo.wait_until("d")
            self.play(FadeIn(note), Indicate(grid.head[3], color=GOAL))
        self.clear_scene()

    def classify(self):
        d = load("fixed")
        head = label(r"Kripke's classification", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        kinds = [("grounded", r"a value in the least fixed point: \ settled by the facts", OK),
                 ("ungrounded", r"no value there, \ but a value in some fixed point", GOAL),
                 ("paradoxical", r"no value in any fixed point", SELF)]
        cols = VGroup()
        for k, desc, c in kinds:
            names = [n for n, v in d["classes"].items() if v == k]
            col = VGroup(label(k, font_size=30, color=c), label(desc, font_size=21, color=GREY_A),
                         label(", ".join(rf"\textbf{{{n}}}" for n in names), font_size=24)).arrange(DOWN, buff=0.25)
            cols.add(col)
        cols.arrange(RIGHT, buff=0.7, aligned_edge=UP).move_to([0, 0.6, 0])
        ex = VGroup(label(r"the truth-teller is ungrounded: \ nothing fixes its value, \ but nothing forbids one",
                          font_size=24, color=GOAL),
                    label(r"the liar is paradoxical: \ every value refutes itself", font_size=24, color=SELF),
                    label(r"`the liar is true or not true' \ is paradoxical too: \ in $K_3$ \ excluded middle fails",
                          font_size=24, color=BAD)).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "This gives Kripke's classification. <bookmark mark='a'/>A sentence is grounded if it has a value in "
            "the least fixed point: its truth traces back, in finitely or transfinitely many steps, to facts that "
            "do not mention truth. <bookmark mark='b'/>It is ungrounded if it has no value there, though some fixed "
            "point gives it one: the truth-teller, and the sentence about it. <bookmark mark='c'/>And it is "
            "paradoxical if no fixed point gives it a value at all: the liar, the cycle, the sentence that the liar "
            "is true or not, and 's2 or the liar is true'. <bookmark mark='d'/>Notice the third of those. In "
            "Kripke's logic, the law of excluded middle fails for the liar. That is the price of the gap."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cols):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=DOWN * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.4), run_time=3)
        self.clear_scene()

    def intrinsic(self):
        head = label(r"Which fixed point is \textit{the} truth?", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"the least: \ only what is forced \ (Kripke's favourite)", font_size=26),
            label(r"a maximal one: \ as much as consistency allows", font_size=26),
            label(r"the largest \textit{intrinsic} one: \ every value that no fixed point contradicts", font_size=26),
            label(r"here the intrinsic point is the least one: \ the truth-teller's three options cancel out",
                  font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.3, 0])
        lesson = label(r"truth is a fixed point of `true': \ applying the predicate changes nothing", font_size=26,
                       color=OK).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Which fixed point is truth? Kripke left the choice open. <bookmark mark='a'/>The least fixed point "
            "says only what is forced. <bookmark mark='b'/>A maximal fixed point says as much as consistency "
            "allows. <bookmark mark='c'/>And the largest intrinsic fixed point gives a sentence a value just when "
            "no fixed point gives it the opposite one. <bookmark mark='d'/>In our small world the Reasoner finds "
            "that the intrinsic point is the least one, because the truth-teller can go any way. "
            "<bookmark mark='e'/>In every case truth is a fixed point: adding 'is true' to a sentence never "
            "changes its value. That is the T-schema, rescued for every sentence that has a value."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(lesson))
        self.clear_scene()

    def arithmetic(self):
        head = label(r"Over arithmetic, \ the crystal grows transfinitely", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"with Gödel coding, \ PA's language can say `the sentence with code $n$ is true'", font_size=26),
            label(r"Kripke's stages: \ $0, 1, 2, \dots, \omega, \omega + 1, \dots$ \ until nothing new is added",
                  font_size=26),
            label(r"the closing stage: \ $\omega_1^{CK}$, \ the first ordinal no program can describe", font_size=26,
                  color=GOAL),
            label(r"the least fixed point is $\Pi^1_1$-complete \ (Burgess 1986): \ far beyond arithmetic", font_size=26,
                  color=BAD),
            label(r"so the theory of truth for arithmetic is not itself arithmetical: \ Tarski again", font_size=24,
                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, -0.2, 0])
        with self.voiceover(
            "Our small world closed after three stages. For the language of arithmetic it takes far longer. "
            "<bookmark mark='a'/>With Gödel's coding, arithmetic can say of the sentence with code n that it is true. "
            "<bookmark mark='b'/>Kripke's stages then run through the finite numbers, past omega, and on, adding "
            "truths at every stage. <bookmark mark='c'/>The process closes only at omega one Church-Kleene, the "
            "first ordinal that no program can describe. <bookmark mark='d'/>And John Burgess showed in 1986 that "
            "the least fixed point is pi one one complete: as a set of codes, it lies far beyond anything "
            "arithmetic can define. <bookmark mark='e'/>Which is Tarski's theorem again: truth for a language rich "
            "enough to talk about itself is not definable in that language."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
