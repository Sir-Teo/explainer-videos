from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import ADV, CODE, CTRL, DATA, HEAD, NO, PART, YES, truth_table

TF = [(True, True), (True, False), (False, True), (False, False)]


class Logic(VoiceoverScene):
    def construct(self):
        self.card()
        self.connectives()
        self.implication()
        self.equivalence()
        self.quantifiers()
        self.game()

    def card(self):
        card = chapter_card(1, r"The grammar of truth", r"What exactly does a statement say?", lit=(1854, 1879),
                            part=PART)
        with self.voiceover("Chapter one. The grammar of truth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def connectives(self):
        head = label(r"Propositions, \ and the ways to combine them", font_size=38).to_edge(UP, buff=0.4)
        ex = VGroup(*[label(t, font_size=28, color=c) for t, c in (
            (r"$P$: \ ``the blank is in its home corner''", DATA),
            (r"$Q$: \ ``the swap parity is even''", DATA),
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL, buff=0.5).shift(DOWN * 0.9)
        rows = [[p, q, not p, p and q, p or q] for p, q in TF]
        tt = truth_table([r"P", r"Q", r"\neg P", r"P \wedge Q", r"P \vee Q"], rows, font_size=34, col_w=1.55,
                         colors={0: DATA, 1: DATA, 2: CTRL, 3: CTRL, 4: CTRL}).move_to(RIGHT * 2.2 + DOWN * 0.6)
        names = VGroup(*[label(t, font_size=22, color=GREY_B) for t in (r"not", r"and", r"or")])
        for nm, j in zip(names, (2, 3, 4)):
            nm.next_to(tt.cells[0][j], UP, buff=0.25)
        foot = note(r"``or'' is inclusive: \ true when either, or both, are true", font_size=24)
        foot.next_to(tt, DOWN, buff=0.4)
        with self.voiceover(
            "A proposition is a statement that is either true or false: the blank is in its home corner; the swap "
            "parity is even. <bookmark mark='a'/> Logic builds bigger statements from smaller ones with a few "
            "connectives, and each one is defined completely by a truth table: one row for every way its parts can be "
            "true or false. <bookmark mark='b'/> Not P flips P. <bookmark mark='c'/> P and Q is true only when both are. "
            "<bookmark mark='d'/> P or Q is true when at least one is: in mathematics, or is inclusive. "
            "<bookmark mark='e'/> George Boole turned this into algebra in 1854. In Part 3 these tables become "
            "transistors."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ex))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tt.cells[0][:2])), FadeIn(tt.rule),
                      FadeIn(VGroup(*[VGroup(*r[:2]) for r in tt.rows])))
            for j, mk in zip((2, 3, 4), "bcd"):
                vo.wait_until(mk)
                self.play(FadeIn(tt.cells[0][j]), FadeIn(names[j - 2]),
                          LaggedStart(*[FadeIn(r[j]) for r in tt.rows], lag_ratio=0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def implication(self):
        head = label(r"If $P$, then $Q$", font_size=40).to_edge(UP, buff=0.4)
        rows = [[p, q, (not p) or q] for p, q in TF]
        tt = truth_table([r"P", r"Q", r"P \Rightarrow Q"], rows, font_size=36, col_w=1.8,
                         colors={0: DATA, 1: DATA, 2: CTRL}).move_to(LEFT * 3.2 + DOWN * 0.4)
        promise = label(r"a promise: \ broken only when \\ $P$ happens and $Q$ does not", font_size=28, color=HEAD)
        promise.move_to(RIGHT * 3.0 + UP * 1.4)
        vac = VGroup(
            label(r"vacuously true:", font_size=28, color=YES),
            label(r"``every unicorn in this room is purple''", font_size=28),
            label(r"no unicorn, \ so no broken promise", font_size=24, color=GREY_B),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.0 + DOWN * 0.9)
        hl = SurroundingRectangle(tt.rows[1], color=NO, buff=0.12, corner_radius=0.08)
        lows = VGroup(SurroundingRectangle(tt.rows[2], color=YES, buff=0.1, corner_radius=0.08),
                      SurroundingRectangle(tt.rows[3], color=YES, buff=0.1, corner_radius=0.08))
        with self.voiceover(
            "The connective that causes the most trouble is implication: if P, then Q. <bookmark mark='a'/> Read it as a "
            "promise. If it rains, the street will be wet. <bookmark mark='b'/> The promise is broken in exactly one "
            "case: it rained, and the street is dry. <bookmark mark='c'/> If it did not rain, the promise was not "
            "tested, and it was not broken, so the implication counts as true, whatever the street is like. "
            "<bookmark mark='d'/> That is vacuous truth. Every unicorn in this room is purple: true, because there are "
            "no unicorns to be anything else. It sounds like a trick, but programs rely on it constantly. A loop that "
            "runs zero times satisfies every promise about each of its iterations."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tt))
            vo.wait_until("a")
            self.play(FadeIn(promise))
            vo.wait_until("b")
            self.play(Create(hl))
            vo.wait_until("c")
            self.play(Create(lows))
            vo.wait_until("d")
            self.play(FadeIn(vac, lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def equivalence(self):
        head = label(r"Equivalent statements: \ the same truth table", font_size=38).to_edge(UP, buff=0.4)
        # P => Q, its contrapositive (not Q) => (not P), and its converse Q => P
        rows = [[p, q, (not p) or q, q or (not p), (not q) or p] for p, q in TF]
        tt = truth_table([r"P", r"Q", r"P \Rightarrow Q", r"\neg Q \Rightarrow \neg P", r"Q \Rightarrow P"],
                         rows, font_size=32, col_w=2.1,
                         colors={0: DATA, 1: DATA, 2: CTRL, 3: YES, 4: NO}).move_to(UP * 0.1)
        lab = VGroup(note(r"implication", font_size=22), note(r"contrapositive", font_size=22),
                     note(r"converse", font_size=22))
        for l_, j in zip(lab, (2, 3, 4)):
            l_.next_to(tt.cells[0][j], UP, buff=0.22)
        same = SurroundingRectangle(VGroup(*[tt.cells[i][j] for i in range(1, 5) for j in (2, 3)]), color=YES,
                                    buff=0.12, corner_radius=0.1)
        diff = VGroup(*[SurroundingRectangle(tt.cells[i][4], color=NO, buff=0.1) for i in (2, 3)])
        dm = VGroup(MathTex(r"\neg(P \wedge Q) \equiv \neg P \vee \neg Q", font_size=36, color=CODE),
                    MathTex(r"\neg(P \vee Q) \equiv \neg P \wedge \neg Q", font_size=36, color=CODE)).arrange(
            RIGHT, buff=1.0).to_edge(DOWN, buff=0.7)
        dml = note(r"De Morgan's laws, \ checked the same way", font_size=22).next_to(dm, UP, buff=0.18)
        with self.voiceover(
            "Two statements are equivalent when they have the same truth table: they say the same thing. "
            "<bookmark mark='a'/> If P then Q, and if not Q then not P, agree on all four rows. The second is the "
            "contrapositive. The hook's proof used it: if a position is reachable, its sum is even; so, if the sum is "
            "odd, the position is not reachable. <bookmark mark='b'/> But if Q then P, the converse, disagrees in two "
            "rows. Mixing up a statement and its converse is the most common error in all of reasoning. "
            "<bookmark mark='c'/> De Morgan's laws, which say how not passes through and and or, are checked the same "
            "way. With n variables a table has two to the n rows. Checking is easy; it is just long. Whether it can "
            "always be done quickly is Part 26."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*[VGroup(*c) for c in tt.cells[:1]])), FadeIn(tt.rule),
                      FadeIn(VGroup(*[VGroup(*r[:3]) for r in tt.rows])), FadeIn(lab[0]))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*[r[3] for r in tt.rows])), FadeIn(lab[1]))
            self.play(Create(same))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*[r[4] for r in tt.rows])), FadeIn(lab[2]))
            self.play(Create(diff))
            vo.wait_until("c")
            self.play(FadeIn(dml), FadeIn(dm))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quantifiers(self):
        head = label(r"Predicates and quantifiers", font_size=38).to_edge(UP, buff=0.4)
        defs = VGroup(*[label(t, font_size=30) for t in (
            r"$\forall x\ P(x)$: \ for every $x$, \ $P(x)$",
            r"$\exists x\ P(x)$: \ there is an $x$ with $P(x)$",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.45)
        a = MathTex(r"\forall x\ \exists y\quad y > x", font_size=46, color=YES)
        b = MathTex(r"\exists y\ \forall x\quad y > x", font_size=46, color=NO)
        a_t = label(r"every integer has a bigger one: \ true", font_size=26, color=YES)
        b_t = label(r"one integer bigger than all: \ false", font_size=26, color=NO)
        ga = VGroup(a, a_t).arrange(DOWN, buff=0.2)
        gb = VGroup(b, b_t).arrange(DOWN, buff=0.2)
        VGroup(ga, gb).arrange(RIGHT, buff=1.4).move_to(DOWN * 0.4)
        neg = VGroup(MathTex(r"\neg\,\forall x\ P(x) \;\equiv\; \exists x\ \neg P(x)", font_size=38, color=CODE),
                     MathTex(r"\neg\,\exists x\ P(x) \;\equiv\; \forall x\ \neg P(x)", font_size=38, color=CODE)
                     ).arrange(RIGHT, buff=1.0).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "A predicate is a statement with a blank in it: x is prime; y is bigger than x. Quantifiers fill the "
            "blanks. <bookmark mark='a'/> For all x, and there exists an x. <bookmark mark='b'/> Their order matters "
            "enormously. For every integer x there is a y bigger than x: true, take x plus one. "
            "<bookmark mark='c'/> There is a y that is bigger than every x: false, there is no largest integer. Same "
            "symbols, swapped, opposite meaning. <bookmark mark='d'/> To negate a quantified statement, push the not "
            "inward and flip each quantifier as it passes. Not everything is P means something is not P. Nothing is P "
            "means everything is not P."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(ga))
            vo.wait_until("c")
            self.play(FadeIn(gb))
            vo.wait_until("d")
            self.play(FadeIn(neg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def game(self):
        head = label(r"A statement as a game", font_size=38).to_edge(UP, buff=0.4)
        rule = VGroup(label(r"$\forall$: \ the skeptic chooses", font_size=30, color=ADV),
                      label(r"$\exists$: \ the prover chooses", font_size=30, color=YES)).arrange(RIGHT, buff=1.2)
        rule.next_to(head, DOWN, buff=0.4)
        cont = MathTex(r"\forall \varepsilon > 0\ \ \exists \delta > 0\ \ \forall x:\ \ |x - a| < \delta "
                       r"\Rightarrow |f(x) - f(a)| < \varepsilon", font_size=40, color=CODE).next_to(rule, DOWN, buff=0.5)
        ctag = note(r"$f$ is continuous at $a$ \ (\textit{Analysis, Built}, Part 2)", font_size=22).next_to(
            cont, DOWN, buff=0.15)
        # the number line game for "for all x exists y, y > x"
        nl = NumberLine(x_range=[-2, 12, 1], length=11, color=GREY_C, include_numbers=True, font_size=22)
        nl.to_edge(DOWN, buff=2.0)
        moves = [(3, 4), (7, 8), (10, 11)]
        dots = []
        for x, y in moves:
            dx = Dot(nl.n2p(x), color=ADV, radius=0.1)
            dy = Dot(nl.n2p(y), color=YES, radius=0.1)
            lx = MathTex("x", font_size=28, color=ADV).next_to(dx, UP, buff=0.15)
            ly = MathTex("y", font_size=28, color=YES).next_to(dy, UP, buff=0.15)
            dots.append((VGroup(dx, lx), VGroup(dy, ly)))
        gtag = label(r"$\forall x\ \exists y\ \ y > x$: \ \ the prover answers $y = x + 1$, \ every time", font_size=26,
                     color=GREY_A).next_to(nl, DOWN, buff=0.45)
        neg = MathTex(r"\exists \varepsilon > 0\ \ \forall \delta > 0\ \ \exists x:\ \ |x - a| < \delta "
                      r"\ \wedge\ |f(x) - f(a)| \ge \varepsilon", font_size=40, color=NO).next_to(rule, DOWN, buff=0.5)
        ntag = note(r"not continuous: \ the quantifiers flip, \ the implication becomes ``and not''", font_size=22)
        ntag.next_to(neg, DOWN, buff=0.15)
        with self.voiceover(
            "There is a way to read long chains of quantifiers without getting lost: play them as a game. "
            "<bookmark mark='a'/> A skeptic chooses every for-all; a prover chooses every there-exists; the prover wins "
            "if the final statement holds. The statement is true exactly when the prover has a strategy that always "
            "wins. <bookmark mark='b'/> For every x there is a bigger y. The skeptic picks three; the prover answers "
            "four. Seven; eight. Ten; eleven. The strategy, y equals x plus one, always wins, so the statement is true. "
            "<bookmark mark='c'/> The game handles statements that defeat intuition. Here is continuity, from Analysis, "
            "Built: for every epsilon, there is a delta, such that for every x. <bookmark mark='d'/> Its negation, "
            "flipping each quantifier, is a winning strategy for the skeptic. Every specification in this series, from "
            "a cache that is coherent to a protocol that is safe, is a statement of this shape, and we prove it by "
            "showing that the prover always has an answer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule, lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Create(nl), FadeIn(gtag))
            for dx, dy in dots:
                self.play(FadeIn(dx, shift=DOWN * 0.2), run_time=0.5)
                self.play(FadeIn(dy, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("c")
            self.play(FadeIn(cont), FadeIn(ctag))
            vo.wait_until("d")
            self.play(ReplacementTransform(cont, neg), FadeOut(ctag), FadeIn(ntag))
        self.wait(0.3)
        self.clear_scene()
