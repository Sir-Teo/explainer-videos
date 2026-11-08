from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Foundations(VoiceoverScene):
    def construct(self):
        card = chapter_card(18, r"What sets are for", r"Must mathematics be built from sets?", lit=(1964,), part=PART)
        with self.voiceover("Chapter eighteen. What sets are for."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.foundation()
        self.junk()
        self.rivals()

    def foundation(self):
        layers = [(r"ZFC", SETC), (r"$\mathbb{N}$, \ $\mathbb{Z}$, \ $\mathbb{Q}$, \ $\mathbb{R}$", "#6FB7FF"),
                  (r"functions, \ spaces, \ groups", ORD), (r"analysis, \ algebra, \ topology", "#F28EC2"),
                  (r"almost all of mathematics", CARD)]
        stack = VGroup()
        for i, (t, c) in enumerate(layers):
            box = Rectangle(width=6.4 - 0.6 * i, height=0.75, stroke_color=c, stroke_width=2.5, fill_color=c,
                            fill_opacity=0.12)
            stack.add(VGroup(box, label(t, font_size=24, color=c).move_to(box)))
        stack.arrange(UP, buff=0.12).move_to([-2.4, -0.2, 0])
        side = VGroup(label(r"one language, \ one set of axioms", font_size=26, color=GOAL),
                      label(r"Bourbaki's \textit{Éléments}; \ the standard textbooks", font_size=22, color=GREY_A),
                      label(r"a common court of appeal: \ is this proof correct?", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.8, 0.0, 0])
        with self.voiceover(
            "Why does mathematics need sets at all? <bookmark mark='a'/>Because they give it one foundation. "
            "Starting from the axioms of ZFC, the number systems are built, then functions, spaces and groups, then "
            "analysis, algebra and topology: almost all of mathematics, in one language. <bookmark mark='b'/>That "
            "is what the Bourbaki group did in its Éléments, and what textbooks still assume. Its real value is a "
            "common court of appeal: when mathematicians disagree about whether a proof is correct, they can in "
            "principle reduce it to the axioms."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(s_, shift=UP * 0.15) for s_ in stack], lag_ratio=0.3), run_time=3)
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.4))
        self.clear_scene()

    def junk(self):
        head = label(r"Junk theorems: \ questions the coding answers, \ and mathematics never asked", font_size=28,
                     color=CONN).to_edge(UP, buff=0.5)
        vn, ze = S.von_neumann, S.zermelo_numeral
        facts = [(r"1 \in 3", vn(1) in vn(3), ze(1) in ze(3)), (r"2 \in 3", vn(2) in vn(3), ze(2) in ze(3)),
                 (r"0 \in 2", vn(0) in vn(2), ze(0) in ze(2)), (r"1 \subseteq 2", vn(1) <= vn(2), ze(1) <= ze(2))]
        hd = [label(r"`theorem'", font_size=22, color=P.CLAIM), label(r"von Neumann", font_size=22, color=P.CLAIM),
              label(r"Zermelo", font_size=22, color=P.CLAIM)]
        rows = [[MathTex(f, font_size=34), a, b] for f, a, b in facts]
        grid = ValueGrid(hd, rows, col_w=[2.6, 2.6, 2.2], cell_h=0.66, font_size=30).move_to([0, 0.3, 0])
        moral = label(r"the answers differ, \ and no mathematician cares: \ numbers have structure, not members",
                      font_size=24, color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "But the foundation has a strange side. <bookmark mark='a'/>Coded as von Neumann's sets, the number one "
            "is a member of three. Coded as Zermelo's, it is not. Two is a member of three in both codings; zero is "
            "a member of two only in von Neumann's. The Reasoner simply checks the sets. <bookmark mark='b'/>These "
            "are junk theorems: answers the coding gives to questions mathematics never asked. No number theorist "
            "cares whether one is a member of three. What matters about the numbers is their structure: their "
            "order, and their arithmetic."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(rows))], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(moral))
        self.clear_scene()

    def rivals(self):
        head = label(r"Rival foundations", font_size=34, color=CONN).to_edge(UP, buff=0.45)
        rows = [(r"categories", r"Lawvere (1964), ETCS: \ functions primitive, \ sets known only by their maps", ORD),
                (r"types", r"Martin-Löf (1972); \ univalent foundations, \ Voevodsky (2006--13)", "#6FB7FF"),
                (r"proof assistants", r"Lean's mathlib: \ type theory; \ Mizar: \ Tarski--Grothendieck sets", OK)]
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.3 - 1.0 * i
            l1 = label(a, font_size=28, color=c)
            l2 = label(b, font_size=24)
            l1.move_to([-6.0 + l1.width / 2, y, 0])
            l2.move_to([-2.6 + l2.width / 2, y, 0])
            tab.add(VGroup(l1, l2))
        nxt = label(r"Part 7: \ what any such foundation cannot prove; \ Part 9: \ what mathematics is about",
                    font_size=24, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Hence the rival foundations. <bookmark mark='a'/>In 1964 William Lawvere axiomatized sets through "
            "category theory, taking functions as primitive, so that a set is known only by its maps to other "
            "sets, and junk questions cannot even be asked. <bookmark mark='b'/>Type theories, from Per Martin-Löf "
            "to the univalent foundations of Vladimir Voevodsky, build mathematics from types and constructions, "
            "with proofs as programs. <bookmark mark='c'/>And the computers have taken sides: Lean's library of "
            "formal mathematics is built on type theory, Mizar's on a set theory with large cardinals. "
            "<bookmark mark='d'/>Part 7 asks what any foundation of this kind cannot prove, and Part 9 what "
            "mathematics is about."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(nxt))
        self.clear_scene()
