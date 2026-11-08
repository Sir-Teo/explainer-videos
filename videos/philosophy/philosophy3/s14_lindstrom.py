from __future__ import annotations

from videos.philosophy.philosophy3.common import *  # noqa: F403


class Lindstrom(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Why first-order logic?", r"Is there a stronger logic with the same virtues?",
                            lit=(1969,), part=PART)
        with self.voiceover("Chapter thirteen. Why first-order logic?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.abstract()
        self.map_()
        self.theorem()
        self.games()
        self.debate()

    def abstract(self):
        head = label(r"What is a logic? \ Abstractly:", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        items = VGroup(
            label(r"a set of sentences, \ and a relation $\mathcal{M} \models \varphi$ between structures and sentences",
                  font_size=26),
            label(r"closed under $\lnot$, $\land$, $\exists$, \ and at least as strong as first-order logic",
                  font_size=26),
            label(r"isomorphic structures satisfy the same sentences: \ only form matters, not which objects",
                  font_size=26, color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.6)
        ex = label(r"first-order, \ second-order, \ `there are infinitely many', \ infinitely long conjunctions, "
                   r"\dots", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "First-order logic gives up a lot. Why is it the logic in every textbook, rather than something "
            "stronger? <bookmark mark='a'/>To answer, logicians in the 1960s stepped back and asked what a logic is, "
            "abstractly. It has sentences, and a relation of truth between structures and sentences. "
            "<bookmark mark='b'/>It can negate, conjoin, and say 'there exists', and it can say at least what "
            "first-order logic says. <bookmark mark='c'/>And it cares only about form: two structures with the same "
            "shape make the same sentences true. <bookmark mark='d'/>Second-order logic is one such logic. So are "
            "first-order logic with a new quantifier 'there are infinitely many', and logics with infinitely long "
            "conjunctions."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(ex))
        self.clear_scene()

    def map_(self):
        ax = VGroup(Arrow([-5.0, -2.6, 0], [4.8, -2.6, 0], buff=0, color=GREY_B, stroke_width=3),
                    Arrow([-5.0, -2.6, 0], [-5.0, 2.6, 0], buff=0, color=GREY_B, stroke_width=3))
        xl = label(r"expressive power", font_size=24, color=GREY_A).next_to(ax[0], DOWN, buff=0.15)
        yl = label(r"good behaviour", font_size=24, color=GREY_A).rotate(PI / 2).next_to(ax[1], LEFT, buff=0.15)
        pts = [((-3.6, 1.9), r"first-order", r"compact, \ L\"owenheim--Skolem, \ complete", OK),
               ((-0.6, 0.3), r"$+$ `infinitely many'", r"loses compactness", GOAL),
               ((0.9, 1.0), r"$+$ `uncountably many'", r"compact (Keisler 1970), \ loses L\"owenheim--Skolem", GOAL),
               ((1.8, -1.0), r"infinitary $\mathcal{L}_{\omega_1\omega}$", r"keeps L\"owenheim--Skolem, \ loses "
                                                                          r"compactness", GOAL),
               ((3.6, -2.0), r"second-order", r"loses all three", BAD)]
        dots = VGroup()
        for (x, y), nm, why, c in pts:
            d = Dot([x, y, 0], radius=0.1, color=c)
            t = VGroup(label(nm, font_size=24, color=c), label(why, font_size=18, color=GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.06).next_to(d, RIGHT, buff=0.18)
            dots.add(VGroup(d, t))
        with self.voiceover(
            "Here is a rough map. <bookmark mark='a'/>First-order logic sits at the top left: limited power, "
            "excellent behaviour. <bookmark mark='b'/>Add the quantifier 'there are infinitely many', and "
            "compactness fails. <bookmark mark='c'/>Add 'there are uncountably many' instead, and, as Jerome Keisler "
            "showed, compactness survives, but the Löwenheim-Skolem theorem fails. <bookmark mark='d'/>Allow "
            "infinitely long conjunctions, and Löwenheim-Skolem survives, but compactness fails. "
            "<bookmark mark='e'/>Second-order logic loses everything. Every step to the right seems to cost a step "
            "down. Is that an accident?"
        ) as vo:
            self.play(GrowArrow(ax[0]), GrowArrow(ax[1]), FadeIn(xl), FadeIn(yl))
            for mk, d in zip("abcde", dots):
                vo.wait_until(mk)
                self.play(FadeIn(d, scale=0.9))
        self.clear_scene()

    def theorem(self):
        hc = history_card(1969, r"Per Lindström", r"`On extensions of elementary logic', \textit{Theoria}", width=6.0,
                          color=HIST).to_corner(UL, buff=0.4)
        thm = theorem_card(r"Lindström's theorem", r"a logic that extends first-order logic and has both compactness "
                           r"and the downward Löwenheim--Skolem property \ \textit{is} first-order logic: it can "
                           r"say nothing more", width=9.6, font_size=24).move_to([0, 0.2, 0])
        also = label(r"also: \ semi-decidable validity plus Löwenheim--Skolem pins it down", font_size=24,
                     color=GREY_A).next_to(thm, DOWN, buff=0.4)
        moral = label(r"first-order logic is the strongest logic that keeps its good behaviour", font_size=28,
                      color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "It is not an accident. <bookmark mark='a'/>In 1969 the Swedish logician Per Lindström proved that any "
            "logic extending first-order logic that has both compactness and the downward Löwenheim-Skolem property "
            "can say nothing more than first-order logic. <bookmark mark='b'/>He also proved a version with "
            "semi-decidable validity in place of compactness. <bookmark mark='c'/>So the trade-off on the map is a "
            "theorem: first-order logic is the strongest logic with those properties. The weaknesses we found in "
            "Chapters eight and nine are the price of its strengths. You cannot have the strengths without them."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(thm, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(also))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()

    def games(self):
        d = load("ef")
        g3 = d["grids"]["3"]
        hc = history_card(r"1954, \ 1961", r"Roland Fraïssé; \ Andrzej Ehrenfeucht", r"a game that measures what "
                          r"first-order sentences can tell apart", width=6.4, color=HIST).to_corner(UL, buff=0.35)
        A = VGroup(*[Dot(radius=0.08, color=OBJ) for _ in range(8)]).arrange(RIGHT, buff=0.42)
        B = VGroup(*[Dot(radius=0.08, color=OBJ) for _ in range(9)]).arrange(RIGHT, buff=0.42)
        rows = VGroup(VGroup(label(r"length 8", font_size=22, color=GREY_A), A).arrange(RIGHT, buff=0.4),
                      VGroup(label(r"length 9", font_size=22, color=GREY_A), B).arrange(RIGHT, buff=0.4)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.5).move_to([-3.0, 0.2, 0])
        rules = VGroup(label(r"each round: \ the spoiler picks a point in either order;", font_size=22),
                       label(r"the duplicator answers in the other, keeping the same pattern of $<$ and $=$",
                             font_size=22),
                       label(r"the duplicator survives $k$ rounds \ $\iff$", font_size=22, color=GOAL),
                       label(r"no sentence with $k$ nested quantifiers tells them apart", font_size=22,
                             color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).next_to(rows, DOWN, buff=0.45).align_to(rows, LEFT)
        picks = [(0, 3, 3), (1, 8, 7), (0, 0, 0)]       # (side, spoiler's point, duplicator's answer)
        marks = VGroup()
        for i, (side, e, f) in enumerate(picks):
            col = [P.CLAIM, P.AGENT, GOAL][i]
            a, b = (A[e], B[f]) if side == 0 else (A[f], B[e])
            marks.add(VGroup(Circle(radius=0.16, color=col, stroke_width=3).move_to(a),
                             Circle(radius=0.16, color=col, stroke_width=3).move_to(b)))
        hd = [MathTex(r"m \backslash n", font_size=20, color=GREY_B)] + [MathTex(str(n), font_size=20, color=OBJ)
                                                                         for n in d["sizes"]]
        body = [[MathTex(str(m), font_size=20, color=OBJ)] + [
            Square(0.26, stroke_width=0, fill_color=OK if w else GREY_E, fill_opacity=0.85 if w else 0.4)
            for w in row] for m, row in zip(d["sizes"], g3)]
        grid = ValueGrid(hd, body, col_w=[0.6] + [0.36] * len(d["sizes"]), cell_h=0.34, font_size=20)
        grid.move_to([4.7, -0.2, 0])
        gl = wrapped_label(r"3 rounds: \ the duplicator wins (green) when $m = n$ or both $\geq 7$", 4.3,
                           font_size=20, color=GREY_A).next_to(grid, DOWN, buff=0.25)
        moral = label(r"so no first-order sentence says `even length': \ 8 and 9 agree on every sentence of depth 3, "
                      r"$2^k$ and $2^k + 1$ at depth $k$", font_size=22, color=BAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How do logicians prove that something cannot be said? The sharpest tool is a game, due to Roland Fraïssé "
            "and Andrzej Ehrenfeucht. <bookmark mark='a'/>Take two structures, here two orderings of points, of "
            "length eight and length nine. <bookmark mark='b'/>In each round a spoiler picks a point in either "
            "ordering, and a duplicator must answer with a point in the other, so that the points chosen so far are "
            "arranged the same way in both. <bookmark mark='c'/>The theorem: the duplicator can survive k rounds "
            "exactly when no sentence with k nested quantifiers tells the two structures apart. "
            "<bookmark mark='d'/>The Reasoner played every three-round game on orderings of lengths one to nine. "
            "The duplicator wins whenever the lengths are equal, or both are at least seven. "
            "<bookmark mark='e'/>So eight and nine agree on every sentence of depth three, and in general two to the "
            "k and two to the k plus one agree at depth k. No first-order sentence says 'the length is even'. The "
            "same games show that a database query language without recursion cannot ask whether one node can reach "
            "another."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows))
            vo.wait_until("b")
            self.play(FadeIn(rules[:2]))
            for m_ in marks:
                self.play(Create(m_[0]), run_time=0.5)
                self.play(Create(m_[1]), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(rules[2:]))
            vo.wait_until("d")
            self.play(FadeIn(grid), FadeIn(gl))
            vo.wait_until("e")
            self.play(FadeIn(moral))
        self.clear_scene()

    def debate(self):
        head = label(r"So is first-order logic \textit{the} logic?", font_size=32, color=CONN).to_edge(UP, buff=0.4)
        cols = VGroup(
            VGroup(label(r"yes", font_size=28, color=OK),
                   label(r"Quine: \ the rest is mathematics", font_size=22),
                   label(r"Lindström: \ its limits are its virtues", font_size=22),
                   label(r"it has a complete proof theory", font_size=22)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.2),
            VGroup(label(r"no", font_size=28, color=BAD),
                   label(r"Shapiro (1991): \ mathematics needs categorical theories", font_size=22),
                   label(r"Boolos: \ plurals are logic too", font_size=22),
                   label(r"Tarski (1966): \ logic is what no permutation can change", font_size=22)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.2)).arrange(RIGHT, buff=1.4, aligned_edge=UP).next_to(head, DOWN,
                                                                                                    buff=0.6)
        perm = VGroup(label(r"Tarski's test: \ a notion is logical if every permutation of the objects leaves it "
                            r"unchanged", font_size=24, color=GOAL),
                      label(r"`at least two things' passes; \ `is red' fails; \ second-order `every property' "
                            r"passes too", font_size=22, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                 buff=0.12).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So is first-order logic the true logic? Philosophers disagree. <bookmark mark='a'/>Quine said yes: what "
            "goes beyond it is mathematics, not logic, and Lindström's theorem gives the boundary a precise shape. "
            "<bookmark mark='b'/>Stewart Shapiro argued in 1991 that mathematics needs second-order logic, because "
            "only categorical theories capture what mathematicians mean by the natural numbers or the reals. "
            "Boolos argued that plural quantifiers are as logical as 'some'. <bookmark mark='c'/>And Tarski proposed "
            "a test in 1966: a notion is logical if no permutation of the objects can change it. 'There are at "
            "least two things' passes; 'is red' fails. Second-order quantifiers pass the test too, so the test alone "
            "does not settle the question. We meet it again in Part 9."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(perm))
        self.clear_scene()
