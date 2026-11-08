from __future__ import annotations

from videos.philosophy.philosophy8.common import *  # noqa: F403


class Axioms(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Truth as an axiom", r"How strong is the concept of truth?", part=PART)
        with self.voiceover("Chapter thirteen. Truth as an axiom."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.table()
        self.kf()
        self.deflation()

    def idea(self):
        head = label(r"Instead of a model, \ axioms", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(label(r"take Peano arithmetic \ (Part 7), \ add a predicate $T$, \ and write down axioms for it",
                            font_size=26),
                      label(r"then ask the questions of Part 7: \ what does the new theory prove? \ how strong is it?",
                            font_size=26, color=GOAL),
                      label(r"truth becomes a measurable addition to mathematics", font_size=26, color=OK)).arrange(
            DOWN, buff=0.4).move_to([0, 0.2, 0])
        with self.voiceover(
            "There is another way to study truth, developed most fully by Volker Halbach. <bookmark mark='a'/>Do not "
            "build a model of a language with truth in it. Take Peano arithmetic, which, thanks to Gödel coding, "
            "can already talk about its own sentences; add a truth predicate; and write down axioms for it. "
            "<bookmark mark='b'/>Then ask the questions of Part 7. What does the new theory prove? How strong is "
            "it? <bookmark mark='c'/>The concept of truth becomes something whose strength can be measured."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=DOWN * 0.1))
        self.clear_scene()

    def table(self):
        head = label(r"Four theories of truth over PA", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        hd = [label(r"theory", font_size=22, color=P.CLAIM), label(r"its axioms", font_size=22, color=P.CLAIM),
              label(r"its strength", font_size=22, color=P.CLAIM), label(r"from", font_size=22, color=P.CLAIM)]
        rows = [[label(a, font_size=26, color=GOAL), label(b, font_size=20), label(c, font_size=20),
                 label(d_, font_size=19, color=GREY_B)] for a, b, c, d_ in Tr.THEORIES]
        grid = ValueGrid(hd, rows, col_w=[1.3, 4.9, 4.4, 2.4], cell_h=0.9, font_size=22).move_to([0, -0.2, 0])
        with self.voiceover(
            "Four theories stand out. <bookmark mark='a'/>TB takes just the T-biconditionals, for sentences that do "
            "not themselves contain the truth predicate. It is conservative: it proves nothing new about numbers. "
            "<bookmark mark='b'/>CT adds Tarski's compositional clauses, true of a conjunction if true of both "
            "parts, and so on, with induction for the new predicate. CT proves that PA is consistent: by induction, "
            "every theorem of PA is true, and zero equals one is not. So truth, used compositionally, is not "
            "conservative. <bookmark mark='c'/>KF, from Solomon Feferman in 1991, axiomatizes Kripke's fixed "
            "points, and is stronger still. <bookmark mark='d'/>FS, from Harvey Friedman and Michael Sheard in "
            "1987, follows revision theory: the truth predicate commutes with every connective. It is consistent, "
            "but, as Vann McGee showed, omega-inconsistent: it proves 'some sentence is not true' while proving each "
            "particular one true."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule))
            for mk, r in zip("abcd", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*grid.cell[r]), shift=RIGHT * 0.1))
        self.clear_scene()


    def kf(self):
        hc = history_card(1991, r"Solomon Feferman", r"`Reflecting on incompleteness'", width=5.6, color=HIST).to_corner(
            UL, buff=0.35)
        rows = [(r"T\ulcorner s = t \urcorner \leftrightarrow s = t", r"atoms: \ as arithmetic says"),
                (r"T\ulcorner \lnot\lnot A \urcorner \leftrightarrow T\ulcorner A \urcorner", r"double negation"),
                (r"T\ulcorner A \wedge B \urcorner \leftrightarrow T\ulcorner A \urcorner \wedge T\ulcorner B \urcorner",
                 r"conjunction"),
                (r"T\ulcorner \lnot(A \wedge B) \urcorner \leftrightarrow T\ulcorner \lnot A \urcorner \vee "
                 r"T\ulcorner \lnot B \urcorner", r"falsity of a conjunction"),
                (r"T\ulcorner T\ulcorner A \urcorner \urcorner \leftrightarrow T\ulcorner A \urcorner", r"truth of "
                 r"truth"),
                (r"T\ulcorner \lnot T\ulcorner A \urcorner \urcorner \leftrightarrow T\ulcorner \lnot A \urcorner",
                 r"falsity of truth")]
        tab = VGroup()
        for i, (f, why) in enumerate(rows):
            y = 1.6 - 0.62 * i
            tab.add(VGroup(MathTex(f, font_size=30).move_to([-5.8, y, 0], aligned_edge=LEFT),
                           label(why, font_size=21, color=GREY_A).move_to([2.6, y, 0], aligned_edge=LEFT)))
        note = VGroup(label(r"KF describes Kripke's fixed points from inside, \ in classical logic", font_size=24,
                            color=GOAL),
                      label(r"it proves the liar, \ and proves the liar not true: \ it asserts what it says is untrue",
                            font_size=24, color=BAD)).arrange(DOWN, buff=0.18).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here, more closely, is KF, the Kripke-Feferman theory. <bookmark mark='a'/>Its axioms describe a fixed "
            "point from the inside. An atomic sentence is true when arithmetic says so. A double negation is true "
            "when the sentence is. A conjunction is true when both parts are, and false when either part is false. "
            "And truth commutes with truth: 'A is true' is true exactly when A is, and 'A is true' is false exactly "
            "when A is false. <bookmark mark='b'/>KF uses classical logic for everything outside the truth "
            "predicate. The result is strange: it proves the liar, and it proves that the liar is not true. It "
            "asserts a sentence it calls untrue. That is the restriction's price from the Price List."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in tab], lag_ratio=0.5), run_time=8)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n_) for n_ in note], lag_ratio=0.4))
        self.clear_scene()

    def deflation(self):
        head = label(r"Is truth thin, \ or substantial?", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"deflationism: \ `true' is only a device of disquotation \ and generalization", font_size=26),
            label(r"so truth should add nothing new: \ a conservative theory, \ like TB", font_size=26, color=GOAL),
            label(r"but we use truth compositionally, \ and CT is \textit{not} conservative \ (Shapiro 1998; "
                  r"Ketland 1999)", font_size=26, color=BAD),
            label(r"reply: \ the extra strength comes from induction, \ not from truth \ (Field 1999)", font_size=26,
                  color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, -0.2, 0])
        with self.voiceover(
            "These results bear on a philosophical question. <bookmark mark='a'/>Deflationists hold that truth is "
            "thin: 'true' is just a device that lets us say 'everything he said is true' without repeating it all. "
            "<bookmark mark='b'/>If so, adding truth should teach us nothing new about the world, or about numbers: "
            "a thin truth should be conservative, like TB. <bookmark mark='c'/>But the truth we actually use is "
            "compositional, and CT is not conservative. Stewart Shapiro and Jeffrey Ketland argued in 1998 and "
            "1999 that deflationism is therefore false. <bookmark mark='d'/>Hartry Field replied that the extra "
            "strength comes from extending induction to the new vocabulary, not from truth itself. The debate "
            "continues, with theorems on both sides."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
        self.clear_scene()
