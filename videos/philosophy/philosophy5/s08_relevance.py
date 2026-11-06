from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Relevance(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Relevance", r"Must the premises of an argument be about its conclusion?",
                            lit=(1972,), part=PART)
        with self.voiceover("Chapter seven. Relevance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.problem()
        self.matrix_()
        self.ternary()
        self.uses()

    def problem(self):
        ex = VGroup(label(r"`if the moon is made of cheese, \ then $2 + 2 = 4$'", font_size=28),
                    label(r"`if $2 + 2 = 5$, \ then Paris is in Peru'", font_size=28),
                    label(r"true for Philo (Part 2), \ and strictly true for Lewis (Part 4)", font_size=24,
                          color=GREY_A)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.6)
        hc = history_card(1975, r"Alan Ross Anderson \& Nuel Belnap", r"\textit{Entailment: The Logic of Relevance "
                          r"and Necessity}, vol.\ I", width=7.6, color=HIST).next_to(ex, DOWN, buff=0.5)
        vs = theorem_card(r"variable sharing", r"if $A \to B$ is a theorem of a relevant logic, \ $A$ and $B$ share "
                          r"an atom", who=r"Belnap 1960", width=8.4, font_size=24).next_to(hc, DOWN, buff=0.4)
        with self.voiceover(
            "Part 4 left a problem unsolved. <bookmark mark='a'/>Material implication makes 'if the moon is made "
            "of cheese, then two plus two is four' true, and Lewis's strict implication makes it necessarily true, "
            "because anything implies a necessary truth and an impossibility implies anything. "
            "<bookmark mark='b'/>Alan Anderson and Nuel Belnap set out to build a logic of real entailment, in "
            "which the premises must be relevant to the conclusion. <bookmark mark='c'/>Their test is a simple "
            "syntactic one, proved by Belnap in 1960: in a relevant logic, if A implies B is a theorem, then A and B "
            "share at least one atom. The moon and arithmetic share nothing."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(hc))
            vo.wait_until("c")
            self.play(FadeIn(vs))
        self.clear_scene()

    def matrix_(self):
        d = load("relevance")
        T = load("tables")["RM3"]
        tab = VGroup(label(r"Sobociński's RM3 (1952)", font_size=26, color=P.CLAIM),
                     ConnTable("imp", T["values"], T["imp"], designated=T["designated"], size=0.66, font_size=28)
                     ).arrange(DOWN, buff=0.4).move_to([-4.2, 0.2, 0])
        hd = [label(r"formula", font_size=22, color=P.CLAIM), label(r"classical", font_size=22, color=P.CLAIM),
              label(r"RM3", font_size=22, color=P.CLAIM), label(r"countermodel", font_size=22, color=P.CLAIM)]
        explicit = {"p -> (q -> p)": r"p \to (q \to p)", "(p & ~p) -> q": r"(p \land \lnot p) \to q",
                    "p -> (q | ~q)": r"p \to (q \lor \lnot q)", "(p & (p -> q)) -> q": r"(p \land (p \to q)) \to q",
                    "(p -> q) -> (~q -> ~p)": r"(p \to q) \to (\lnot q \to \lnot p)"}
        rows = [[MathTex(explicit.get(r["f"], mx_tex(r["f"])), font_size=28), r["cl"], r["rm3"], MathTex(cm_tex(r["cm"]) if r["cm"] else r"\cdot",
                                                              font_size=24, color=GREY_A)] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[3.8, 1.5, 1.1, 2.4], cell_h=0.6, font_size=26).move_to([2.4, 0.4, 0])
        mingle = label(r"but RM3 still proves $(p \land \lnot p) \to (q \lor \lnot q)$: \ only semi-relevant; \ the "
                       r"logic R needs a richer semantics", font_size=22, color=BAD).to_edge(DOWN, buff=0.35)
        assert d["mingle"] and d["mp"]
        with self.voiceover(
            "A first taste comes from a three-valued matrix that Bolesław Sobociński found in 1952. "
            "<bookmark mark='a'/>It designates one and one half, like LP, but its conditional is stricter: a "
            "conditional whose antecedent is truer than its consequent is false outright. "
            "<bookmark mark='b'/>The Reasoner checks the paradoxes. 'If p, then if q then p': refuted. "
            "'A contradiction implies q': refuted. 'p implies q or not q': refuted. <bookmark mark='c'/>Yet the "
            "laws we want survive: if p then p; modus ponens; contraposition. <bookmark mark='d'/>RM3 is only a "
            "first approximation. It still proves that a contradiction implies a tautology about something else "
            "entirely. Anderson and Belnap's logic R needs a richer semantics, and it took more than a decade to find."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][c]) for r in range(len(rows)) for c in (0, 1)])
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[r][c]) for r in (1, 2, 3) for c in (2, 3)])
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[r][c]) for r in (0, 4, 5) for c in (2, 3)])
            vo.wait_until("d")
            self.play(FadeIn(mingle))
        self.clear_scene()

    def ternary(self):
        hc = history_card(r"1972--73", r"Richard Routley \& Robert K.\ Meyer", r"the ternary relation semantics",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        x, y, z = [-2.6, -1.6, 0], [0.0, 1.0, 0], [2.6, -1.6, 0]
        pts = VGroup(*[VGroup(Circle(radius=0.42, color=P.WORLD, stroke_width=3, fill_color="#0B0F17", fill_opacity=1),
                              MathTex(n, font_size=36)).move_to(p) for n, p in (("x", x), ("y", y), ("z", z))])
        for g in pts:
            g[1].move_to(g[0])
        tri = VGroup(Line(x, y, color=CONN, stroke_width=2.5), Line(y, z, color=CONN, stroke_width=2.5),
                     Line(x, z, color=CONN, stroke_width=2.5)).set_z_index(-1)
        rl = MathTex(r"Rxyz", font_size=34, color=CONN).move_to([0, -0.6, 0])
        ay = MathTex(r"A", font_size=34, color=P.CLAIM).next_to(pts[1], UP, buff=0.15)
        bz = MathTex(r"B", font_size=34, color=GOAL).next_to(pts[2], DOWN, buff=0.15)
        clause = MathTex(r"x \models A \to B \iff \text{for all } y, z \text{ with } Rxyz:\ "
                         r"y \models A \Rightarrow z \models B", font_size=32).to_edge(DOWN, buff=1.05)
        read = label(r"read: \ the information in $x$, applied to the information in $y$, \ yields at most $z$",
                     font_size=24, color=GREY_A).to_edge(DOWN, buff=0.45)
        star = label(r"negation: \ $x \models \lnot A$ iff $x^{*} \not\models A$ \ (the Routley star)", font_size=24,
                     color=GOAL).to_corner(UR, buff=0.5).shift(DOWN * 1.2)
        with self.voiceover(
            "The richer semantics came from Richard Routley and Robert Meyer in 1972 and 1973. "
            "<bookmark mark='a'/>Its points are not possible worlds but situations, bodies of information that may "
            "be incomplete or inconsistent. And it relates them three at a time. <bookmark mark='b'/>'If A then B' "
            "holds at x when, whenever x relates y to z, A at y gives B at z. <bookmark mark='c'/>Read it this way: "
            "x is a rule; applied to the information in y, it yields the information in z. A conditional is "
            "information that, combined with A, produces B. <bookmark mark='d'/>Negation uses a second device, the "
            "Routley star: not A holds at a situation when A fails at its mirror image. With these two, the "
            "relevant logic R is sound and complete."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(pts), Create(tri), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(ay), FadeIn(bz), Write(clause))
            vo.wait_until("c")
            self.play(FadeIn(read))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.clear_scene()

    def uses(self):
        head = label(r"What relevance buys", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(label(r"a conditional that means `follows from', \ not `is not a counterexample to'",
                            font_size=26),
                      label(r"naive set theory, every condition defining a set, \ kept consistent in weak relevant "
                            r"logics \ (Brady 2006)", font_size=26),
                      label(r"theories that tolerate a contradiction without trivializing \ (Mortensen, "
                            r"\textit{Inconsistent Mathematics} 1995)", font_size=26),
                      label(r"the price: \ disjunctive syllogism is lost again \ (Chapter 6), \ and the semantics is "
                            r"hard to interpret", font_size=26, color=BAD)).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "What does relevance buy? <bookmark mark='a'/>First, a conditional that means 'follows from', rather "
            "than 'is not a counterexample to'. <bookmark mark='b'/>Second, a home for naive set theory. Part 6 "
            "will show that the rule 'every condition defines a set' is inconsistent in classical logic. Ross Brady "
            "proved that, in a weak enough relevant logic, it is not even trivial. <bookmark mark='c'/>Third, "
            "mathematics with inconsistent theories that do not collapse. <bookmark mark='d'/>The price is high: "
            "the relevant logics lose disjunctive syllogism, like LP, and the ternary relation has resisted an "
            "intuitive reading. That debate is still open."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
