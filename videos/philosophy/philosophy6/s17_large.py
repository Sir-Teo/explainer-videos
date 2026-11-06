from __future__ import annotations

from videos.philosophy.philosophy6.common import *  # noqa: F403


class Large(VoiceoverScene):
    def construct(self):
        card = chapter_card(16, r"Beyond the axioms", r"What new axioms could settle the open questions?",
                            lit=(1989,), part=PART)
        with self.voiceover("Chapter sixteen. Beyond the axioms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.inaccessible()
        self.ladder()
        self.games()
        self.determinacy()

    def inaccessible(self):
        hc = history_card(1930, r"Sierpiński \& Tarski; \ Zermelo", r"inaccessible cardinals", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(label(r"$\kappa$ is \textit{inaccessible}: \ uncountable, \ and not reachable from below by "
                            r"power sets or unions of fewer than $\kappa$ sets", font_size=24),
                      label(r"then $V_\kappa$ is itself a model of ZFC", font_size=26, color=GOAL),
                      label(r"so ZFC cannot prove that one exists: \ it would prove its own consistency \ (Gödel, Part 7)",
                            font_size=24, color=BAD)).arrange(DOWN, buff=0.35).move_to([0, -0.2, 0])
        with self.voiceover(
            "If the axioms cannot settle the continuum hypothesis, perhaps new axioms can. The most studied "
            "candidates assert the existence of very large infinite numbers. <bookmark mark='a'/>A cardinal is "
            "inaccessible if it is uncountable and cannot be reached from below, by power sets or by unions of "
            "fewer sets. <bookmark mark='b'/>Then the stage of the hierarchy at that cardinal is itself a complete "
            "model of ZFC. <bookmark mark='c'/>So ZFC cannot prove that an inaccessible exists, because then it "
            "would prove its own consistency, which Gödel's second theorem, in Part 7, forbids."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def ladder(self):
        head = label(r"The ladder of consistency strength", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        rungs = [(r"ZFC", GREY_A), (r"inaccessible", SETC), (r"Mahlo", SETC), (r"weakly compact", "#6FB7FF"),
                 (r"measurable \ (Ulam 1930)", ORD), (r"Woodin", "#F28EC2"), (r"supercompact", CARD),
                 (r"$\vdots$", GREY_B)]
        lad = VGroup()
        for i, (t, c) in enumerate(rungs):
            y = -2.8 + 0.78 * i
            bar = Line([-1.6, y, 0], [1.6, y, 0], color=c, stroke_width=4)
            lab = label(t, font_size=24, color=c).next_to(bar, RIGHT, buff=0.3)
            lad.add(VGroup(bar, lab))
        rails = VGroup(Line([-1.6, -3.0, 0], [-1.6, 2.9, 0], color=GREY_C), Line([1.6, -3.0, 0], [1.6, 2.9, 0],
                                                                                 color=GREY_C))
        lad.shift(LEFT * 4.1)
        rails.shift(LEFT * 4.1)
        notes = VGroup(label(r"each rung proves the consistency of those below", font_size=22, color=GREY_A),
                       label(r"Scott (1961): \ a measurable cardinal implies $V \neq L$", font_size=22, color=GOAL),
                       label(r"but none of them settles CH \ (Lévy and Solovay 1967)", font_size=22, color=BAD)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        notes.next_to([0.8, -0.3, 0], RIGHT, buff=0)
        with self.voiceover(
            "Large cardinals form a ladder. <bookmark mark='a'/>Above ZFC come the inaccessibles, then Mahlo and "
            "weakly compact cardinals, then the measurable cardinals that Stanisław Ulam introduced in 1930, then "
            "Woodin and supercompact cardinals, and more. Remarkably, the many proposals that set theorists have "
            "made fall into a single line: each rung proves the consistency of those below. "
            "<bookmark mark='b'/>Dana Scott showed in 1961 that a measurable cardinal is incompatible with Gödel's "
            "L: the universe must be wider. <bookmark mark='c'/>But Azriel Lévy and Robert Solovay proved that no "
            "large cardinal of this kind settles the continuum hypothesis. Forcing with small sets leaves them "
            "untouched."
        ) as vo:
            self.play(FadeIn(head), Create(rails))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in lad], lag_ratio=0.25), run_time=4)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.clear_scene()

    def games(self):
        d = load("game")
        hc = history_card(1913, r"Ernst Zermelo", r"every finite game of perfect information is determined", width=6.4,
                          color=HIST).to_corner(UL, buff=0.35)
        board = VGroup()
        for i in range(3):
            for j in range(3):
                board.add(Square(side_length=0.9, stroke_color=GREY_B).move_to([-3.4 + 0.9 * j, 0.5 - 0.9 * i, 0]))
        marks = VGroup(MathTex(r"\times", font_size=56, color=P.CLAIM).move_to(board[4]),
                       MathTex(r"\circ", font_size=56, color=GOAL).move_to(board[0]),
                       MathTex(r"\times", font_size=56, color=P.CLAIM).move_to(board[8]))
        res = VGroup(label(rf"backward induction over all {d['positions']:,} positions".replace(",", "{,}"),
                           font_size=26),
                     label(r"with best play: \ a draw" if d["value"] == 0 else r"?", font_size=30, color=GOAL),
                     label(r"one player always has a strategy that guarantees their best outcome", font_size=22,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([2.6, 0.0, 0])
        with self.voiceover(
            "A different kind of axiom comes from games. <bookmark mark='a'/>In 1913 Zermelo proved that every "
            "finite game of perfect information, chess for example, is determined: either one player has a winning "
            "strategy, or both can force a draw. <bookmark mark='b'/>The Reasoner checks the idea on noughts and "
            "crosses. Working backwards from every finished board, it values all five thousand, four hundred and "
            "seventy-eight positions. With best play from both sides, the game is a draw."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(board), LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.4))
        self.clear_scene()

    def determinacy(self):
        head = label(r"Infinite games", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        seq = MathTex(r"\text{I: } x_0 \quad \text{II: } x_1 \quad \text{I: } x_2 \quad \text{II: } x_3 \quad \cdots",
                      font_size=36).next_to(head, DOWN, buff=0.5)
        rule = label(r"I wins if the infinite sequence lies in a given set $A$ of reals", font_size=26,
                     color=GREY_A).next_to(seq, DOWN, buff=0.3)
        facts = VGroup(label(r"Gale and Stewart (1953): \ open games are determined", font_size=24),
                       label(r"with choice, \ some games have no winning strategy for either player", font_size=24,
                             color=BAD),
                       label(r"projective determinacy: \ every definable game is determined", font_size=26, color=GOAL),
                       label(r"Martin and Steel (1989): \ it follows from Woodin cardinals", font_size=24, color=OK),
                       label(r"and it settles the classical questions about definable sets of reals", font_size=24,
                             color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rule, DOWN, buff=0.55)
        with self.voiceover(
            "Now let the game go on forever. <bookmark mark='a'/>Two players take turns writing digits. Player one "
            "wins if the infinite sequence they produce lands in a given set of reals. <bookmark mark='b'/>David "
            "Gale and Frank Stewart showed in 1953 that simple, open games are determined. "
            "<bookmark mark='c'/>But with the axiom of choice one can build games that are not: neither player has "
            "a winning strategy. <bookmark mark='d'/>The hypothesis that every definable game is determined, "
            "projective determinacy, was found to settle the old open questions about definable sets of real "
            "numbers. <bookmark mark='e'/>In 1989 Donald Martin and John Steel proved that it follows from the "
            "existence of Woodin cardinals. Two independent lines of thought, games and large cardinals, met. "
            "Many set theorists take that convergence as evidence that both are true."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(seq), FadeIn(rule))
            for mk, i in zip("bcde", range(4)):
                vo.wait_until(mk)
                self.play(FadeIn(facts[i], shift=RIGHT * 0.15))
            self.play(FadeIn(facts[4]))
        self.clear_scene()
