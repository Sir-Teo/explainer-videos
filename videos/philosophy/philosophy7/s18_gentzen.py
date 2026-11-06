from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class Gentzen(VoiceoverScene):
    def construct(self):
        card = chapter_card(17, r"Gentzen's answer", r"If not from within, how can we trust arithmetic?",
                            lit=(1935,), part=PART)
        with self.voiceover("Chapter seventeen. Gentzen's answer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.proof()
        self.analysis()
        self.reverse()
        self.lesson()

    def proof(self):
        hc = history_card(1936, r"Gerhard Gentzen", r"`The consistency of elementary number theory'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(label(r"assign every PA proof an ordinal below $\varepsilon_0$", font_size=26),
                      label(r"a step that simplifies a proof of $0 = 1$ \ gives a proof of $0 = 1$ with a smaller "
                            r"ordinal", font_size=26),
                      label(r"ordinals cannot fall for ever \ (Part 6): \ so there is no proof of $0 = 1$",
                            font_size=26, color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([0, 0.7, 0])
        uses = VGroup(label(r"it uses: \ finitary reasoning, \ plus induction along the ordinals up to "
                            r"$\varepsilon_0$", font_size=24, color=GOAL),
                      label(r"which PA cannot prove \ (Gentzen 1943): \ no contradiction with Gödel II", font_size=24,
                            color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Gödel's second theorem says that PA cannot prove its own consistency. It does not say that nothing "
            "can. <bookmark mark='a'/>In 1936 Gerhard Gentzen gave a proof. He assigned to every proof in PA an "
            "ordinal below epsilon zero, the ordinal of Part 6. <bookmark mark='b'/>Then he showed that any proof of "
            "zero equals one could be transformed into another proof of zero equals one, with a smaller ordinal. "
            "<bookmark mark='c'/>Since ordinals cannot decrease for ever, there is no proof of zero equals one. "
            "<bookmark mark='d'/>The proof is finitary, except for one principle: induction along the ordinals up "
            "to epsilon zero. That principle is not provable in PA, as Gentzen showed in 1943, so there is no "
            "conflict with Gödel. The consistency of arithmetic rests on something slightly beyond arithmetic."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(u) for u in uses], lag_ratio=0.4))
        self.clear_scene()

    def analysis(self):
        head = label(r"Ordinal analysis: \ the strength of a theory, \ as an ordinal", font_size=30,
                     color=CONN).to_edge(UP, buff=0.45)
        rows = VGroup()
        for i, (sysname, o) in enumerate(A.ORDINALS):
            y = 1.6 - 0.85 * i
            la = label(sysname, font_size=24)
            lo = MathTex(o, font_size=36, color=PROV)
            la.move_to([-6.2 + la.width / 2, y, 0])
            lo.move_to([3.6, y, 0])
            rows.add(VGroup(la, lo))
        rule = Line([-6.3, 2.1, 0], [5.4, 2.1, 0], color=GREY_D)
        hd = VGroup(label(r"theory", font_size=22, color=P.CLAIM).move_to([-5.8, 2.35, 0]),
                    label(r"proof-theoretic ordinal", font_size=22, color=P.CLAIM).move_to([3.6, 2.35, 0]))
        arrow = Arrow([5.9, 1.8, 0], [5.9, -1.8, 0], buff=0, color=GREY_B)
        al = label(r"stronger", font_size=20, color=GREY_B).next_to(arrow, RIGHT, buff=0.1).rotate(-PI / 2)
        note = label(r"Goodstein, \ the hydra, \ Paris--Harrington: \ each lives just above $\varepsilon_0$",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Gentzen's idea became a research program, ordinal analysis. <bookmark mark='a'/>Each theory is "
            "measured by the least ordinal along which it cannot prove induction. For weak systems it is omega to "
            "the omega; for PA, epsilon zero; for stronger systems, ordinals with names like Gamma zero, studied "
            "by Feferman and Schütte, and the Bachmann-Howard ordinal, and beyond, still being charted. "
            "<bookmark mark='b'/>The natural independent statements of Chapter 12 sit exactly here: Goodstein's "
            "theorem, the hydra, and Paris-Harrington all need induction up to epsilon zero, which is why PA "
            "cannot prove them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hd), Create(rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.35), GrowArrow(arrow),
                      FadeIn(al), run_time=5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.clear_scene()

    def reverse(self):
        hc = history_card(1975, r"Harvey Friedman; \ Stephen Simpson", r"reverse mathematics: \ \textit{Subsystems of "
                          r"Second Order Arithmetic} (1999)", width=7.2, color=HIST).to_corner(UL, buff=0.35)
        rows = [(r"$\mathrm{RCA}_0$", r"computable sets exist", r"the intermediate value theorem"),
                (r"$\mathrm{WKL}_0$", r"+ every infinite binary tree has a path",
                 r"Heine--Borel for $[0,1]$; \ completeness \ (Part 3)"),
                (r"$\mathrm{ACA}_0$", r"+ arithmetically definable sets exist",
                 r"Bolzano--Weierstrass"),
                (r"$\mathrm{ATR}_0$", r"+ transfinite recursion", r"any two well-orders are comparable"),
                (r"$\Pi^1_1\text{-}\mathrm{CA}_0$", r"+ $\Pi^1_1$-definable sets exist",
                 r"the Cantor--Bendixson theorem")]
        hd = VGroup(label(r"system", font_size=22, color=P.CLAIM).move_to([-5.9, 1.75, 0]),
                    label(r"its existence axiom", font_size=22, color=P.CLAIM).move_to([-4.5, 1.75, 0],
                                                                                       aligned_edge=LEFT),
                    label(r"a theorem \textit{equivalent} to it", font_size=22, color=P.CLAIM).move_to(
                        [0.7, 1.75, 0], aligned_edge=LEFT))
        rule = Line([-6.4, 1.5, 0], [6.6, 1.5, 0], color=GREY_D)
        tab = VGroup()
        for i, (a, b, c) in enumerate(rows):
            y = 1.05 - 0.72 * i
            tab.add(VGroup(label(a, font_size=26, color=PROV).move_to([-5.9, y, 0]),
                           label(b, font_size=21).move_to([-4.5, y, 0], aligned_edge=LEFT),
                           label(c, font_size=21, color=GOAL).move_to([0.7, y, 0], aligned_edge=LEFT)))
        moral = label(r"the Big Five: \ almost every classical theorem is provable in, \ or equivalent to, \ one of "
                      r"them", font_size=24, color=OK).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "There is a further twist, from Harvey Friedman in the 1970s, developed by Stephen Simpson. "
            "<bookmark mark='a'/>Instead of asking what follows from the axioms, ask which axioms a theorem needs. "
            "Work over a weak base, RCA zero, which says only that computable sets exist; it proves the "
            "intermediate value theorem. <bookmark mark='b'/>Add that every infinite binary tree has an infinite "
            "path, and you get WKL zero, which is equivalent, over the base, to the Heine-Borel theorem, and to "
            "Gödel's completeness theorem of Part 3. <bookmark mark='c'/>Arithmetical comprehension is equivalent "
            "to the Bolzano-Weierstrass theorem; transfinite recursion, to the comparability of well-orders; and "
            "the strongest of the five, to the Cantor-Bendixson theorem. <bookmark mark='d'/>The surprise is how "
            "few levels there are. Almost every theorem of classical mathematics is provable in one of these "
            "five systems, or equivalent to one: the theorem proves the axiom back."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(hd), Create(rule))
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            vo.wait_until("b")
            self.play(FadeIn(tab[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[2:]], lag_ratio=0.4), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(moral))
        self.clear_scene()

    def lesson(self):
        head = label(r"What became of Hilbert's program", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"completeness: \ impossible \ (Gödel I)", font_size=26, color=BAD),
            label(r"a finitary proof of consistency: \ impossible \ (Gödel II)", font_size=26, color=BAD),
            label(r"a decision procedure: \ impossible \ (Church, Turing)", font_size=26, color=BAD),
            label(r"relative consistency, \ ordinal analysis, \ and reverse mathematics: \ which axioms does a theorem "
                  r"need?", font_size=26, color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, 0.3, 0])
        moral = label(r"not a ruin: \ a map of what proof can reach", font_size=28, color=GOAL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "So what became of Hilbert's program? <bookmark mark='a'/>Completeness, a finitary consistency proof, "
            "and a decision procedure were all shown impossible. <bookmark mark='b'/>What survived is subtler and "
            "richer: proofs of consistency relative to other systems, ordinal analysis, and the program of reverse "
            "mathematics begun by Harvey Friedman and Stephen Simpson, which asks, for each ordinary theorem, "
            "exactly which axioms it needs. <bookmark mark='c'/>The limits of proof are not a ruin. They are a map "
            "of what proof can reach."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:3]], lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()
