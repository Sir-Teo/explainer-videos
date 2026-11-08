from __future__ import annotations

from videos.philosophy.philosophy7.common import *  # noqa: F403


class First(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"The first incompleteness theorem", r"Is every truth of arithmetic provable?",
                            lit=(1931,), part=PART)
        with self.voiceover("Chapter seven. The first incompleteness theorem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sentence()
        self.proof()
        self.rosser()
        self.truth()
        self.polynomial()

    def sentence(self):
        hc = history_card(1931, r"Kurt Gödel", r"`On formally undecidable propositions of \textit{Principia "
                          r"Mathematica} and related systems I'", width=7.2, color=HIST).to_corner(UL, buff=0.35)
        step = MathTex(r"\varphi(x) := \lnot\,\mathrm{Prov}(x)", font_size=44, color=PROV).move_to([0, 1.0, 0])
        g = MathTex(r"\mathrm{PA} \vdash \ G \ \leftrightarrow\ \lnot\,\mathrm{Prov}(\ulcorner G \urcorner)",
                    font_size=54, color=SELF).next_to(step, DOWN, buff=0.6)
        cap = label(r"$G$ says: \ `I am not provable in PA'", font_size=30, color=GOAL).next_to(g, DOWN, buff=0.5)
        with self.voiceover(
            "Now the theorem. <bookmark mark='a'/>Apply the diagonal lemma to the property of not being provable. "
            "<bookmark mark='b'/>It gives a sentence G that PA proves equivalent to: G is not provable. "
            "<bookmark mark='c'/>G says, of itself, I am not provable. Not 'I am false', which would be the liar. "
            "Provability is a precise, arithmetical property, so G is a perfectly good sentence about numbers: in "
            "the end, a claim that a certain polynomial equation has no solution."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(step))
            vo.wait_until("b")
            self.play(Write(g))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.clear_scene()

    def proof(self):
        head = label(r"Suppose PA is consistent", font_size=32, color=CONN).to_edge(UP, buff=0.45)
        g = MathTex(r"G \leftrightarrow \lnot\,\mathrm{Prov}(\ulcorner G \urcorner)", font_size=40,
                    color=SELF).next_to(head, DOWN, buff=0.35)
        left = VGroup(label(r"if PA proved $G$", font_size=28, color=GOAL),
                      label(r"some number $m$ codes the proof", font_size=24),
                      label(r"$\mathrm{Prf}(\bar m, \ulcorner G \urcorner)$ is true and $\Sigma_1$, \ so PA proves it",
                            font_size=24),
                      label(r"so PA proves $\mathrm{Prov}(\ulcorner G \urcorner)$, \ that is, $\lnot G$", font_size=24),
                      label(r"PA proves $G$ and $\lnot G$: \ inconsistent", font_size=26, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25)
        right = VGroup(label(r"if PA proved $\lnot G$", font_size=28, color=GOAL),
                       label(r"then PA proves $\exists m\,\mathrm{Prf}(m, \ulcorner G \urcorner)$", font_size=24),
                       label(r"but by the left side, no actual $m$ is a proof:", font_size=24),
                       label(r"PA proves $\lnot\mathrm{Prf}(\bar 0, \cdot), \ \lnot\mathrm{Prf}(\bar 1, \cdot), "
                             r"\dots$", font_size=24),
                       label(r"$\omega$-inconsistent: \ `some $m$', \ yet `not 0, not 1, \dots'", font_size=26,
                             color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        cols = VGroup(left, right).arrange(RIGHT, buff=0.9, aligned_edge=UP).next_to(g, DOWN, buff=0.55)
        div = Line(cols.get_top() + UP * 0.1, cols.get_bottom() + DOWN * 0.1, color=GREY_D).move_to(
            [(left.get_right()[0] + right.get_left()[0]) / 2, cols.get_center()[1], 0])
        concl = label(r"so a consistent PA cannot prove $G$; \ an $\omega$-consistent PA cannot refute it",
                      font_size=26, color=OK).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Suppose PA is consistent. Could it prove G? <bookmark mark='a'/>If it did, some number m would code "
            "that proof. Checking that m codes a proof of G is a computation, a true sigma one fact, so PA proves "
            "it. So PA proves that G is provable, which is equivalent to not G. PA would prove both G and its "
            "negation. So a consistent PA does not prove G. <bookmark mark='b'/>Could it prove not G? Then PA "
            "proves that some number codes a proof of G. But we just saw that no number does, and PA can check each "
            "one: it proves 'zero is not a proof of G', 'one is not', and so on, for every number. A theory like "
            "that says 'there is one', and denies every candidate. Gödel called it omega-inconsistent. "
            "<bookmark mark='c'/>So if PA is consistent it cannot prove G, and if it is omega-consistent it cannot "
            "refute G. G is undecidable."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in left], lag_ratio=0.6), run_time=6)
            vo.wait_until("b")
            self.play(Create(div), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in right], lag_ratio=0.6),
                      run_time=6)
            vo.wait_until("c")
            self.play(FadeIn(concl))
        self.clear_scene()

    def rosser(self):
        hc = history_card(1936, r"J. Barkley Rosser", r"`Extensions of some theorems of Gödel and Church'",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        r = MathTex(r"R \ \leftrightarrow\ \forall m\,\bigl(\mathrm{Prf}(m, \ulcorner R \urcorner) \to \exists k < m"
                    r"\ \mathrm{Prf}(k, \ulcorner \lnot R \urcorner)\bigr)", font_size=38, color=SELF).move_to([0, 0.8, 0])
        cap = label(r"$R$ says: \ `for any proof of me, \ there is a shorter proof of my negation'", font_size=26,
                    color=GOAL).next_to(r, DOWN, buff=0.4)
        thm = theorem_card(r"Gödel--Rosser", r"any consistent, \ effectively axiomatized theory that contains $Q$ is "
                           r"incomplete: \ some sentence is neither provable nor refutable", width=10.6,
                           font_size=25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 1936 Barkley Rosser removed the need for omega-consistency, with a cleverer sentence. "
            "<bookmark mark='a'/>R says: for any proof of me, there is a shorter proof of my negation. A race "
            "between proofs, which a merely consistent theory can neither win nor lose. "
            "<bookmark mark='b'/>The result, in its modern form: any consistent theory that contains Q, and whose "
            "axioms can be listed by a program, is incomplete. Some sentence is neither provable nor refutable in "
            "it. Adding G as a new axiom does not help: the new theory has its own Gödel sentence."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(r), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(thm))
        self.clear_scene()

    def truth(self):
        head = label(r"But $G$ is true", font_size=34, color=OK).to_edge(UP, buff=0.5)
        rows = VGroup(label(r"$G$ says that $G$ is not provable", font_size=28),
                      label(r"and $G$ is not provable \ (if PA is consistent)", font_size=28),
                      label(r"so what $G$ says is so: \ $G$ is true in $\mathbb{N}$", font_size=30, color=OK)).arrange(
            DOWN, buff=0.4).move_to([0, 0.9, 0])
        venn = VGroup(Circle(radius=1.3, color=GOAL, fill_opacity=0.08).move_to([-0.6, -1.7, 0]),
                      Circle(radius=0.75, color=PROV, fill_opacity=0.15).move_to([-1.0, -1.7, 0]))
        vl = VGroup(label(r"true in $\mathbb{N}$", font_size=22, color=GOAL).next_to(venn[0], RIGHT, buff=0.2),
                    label(r"provable in PA", font_size=20, color=PROV).move_to(venn[1]),
                    Dot([0.3, -1.7, 0], color=SELF), label(r"$G$", font_size=24, color=SELF).move_to([0.52, -1.52, 0]))
        caveat = label(r"`true' assumes PA is consistent; \ and $G$ is false in some \textit{other} models of PA "
                       r"(Part 3)", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "And there is a twist. <bookmark mark='a'/>G says that G is not provable. <bookmark mark='b'/>If PA is "
            "consistent, G is not provable. <bookmark mark='c'/>So what G says is so: G is true, in the natural "
            "numbers. Truth in arithmetic outruns provability in PA, and in any system like it. "
            "<bookmark mark='d'/>Two cautions. The argument that G is true assumes that PA is consistent. And by "
            "the completeness theorem of Part 3, since PA does not prove G, there are other models of PA, with "
            "nonstandard numbers, in which G is false: in them, some nonstandard number codes a 'proof' of G."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=DOWN * 0.1))
            self.play(Create(venn), FadeIn(vl))
            vo.wait_until("d")
            self.play(FadeIn(caveat))
        self.clear_scene()

    def polynomial(self):
        hc = history_card(1970, r"Yuri Matiyasevich", r"after Martin Davis, Hilary Putnam and Julia Robinson: \ "
                          r"Hilbert's tenth problem is unsolvable", width=7.4, color=HIST).to_corner(UL, buff=0.35)
        h10 = VGroup(label(r"Hilbert's tenth problem \ (1900):", font_size=26, color=GOAL),
                     label(r"find a procedure that decides whether a polynomial equation with integer coefficients "
                           r"has a whole-number solution", font_size=24)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.15).move_to([0, 1.0, 0])
        ex = MathTex(r"x^2 - 2y^2 = 1 \ \ \text{(yes: } 3, 2\text{)} \qquad x^2 + y^2 = 3 \ \ \text{(no)}",
                     font_size=34, color=TAPE).next_to(h10, DOWN, buff=0.35)
        mrdp = VGroup(label(r"MRDP: \ every set a program can list is the solution set of a polynomial", font_size=25,
                            color=OK),
                      label(r"so \ $G$ \ is equivalent to: \ `a certain polynomial equation has no solution'",
                            font_size=25, color=SELF),
                      label(r"and no procedure decides such equations: \ halting would be decidable", font_size=25,
                            color=BAD)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "How ordinary is Gödel's sentence, in the end? <bookmark mark='a'/>Hilbert's tenth problem, of 1900, "
            "asked for a procedure to decide whether a polynomial equation with integer coefficients has a solution "
            "in whole numbers. x squared minus two y squared equals one has one: three and two. x squared plus y "
            "squared equals three has none. <bookmark mark='b'/>In 1970 Yuri Matiyasevich, completing work of "
            "Martin Davis, Hilary Putnam and Julia Robinson, proved that every set a program can list is the set of "
            "solutions of some polynomial. <bookmark mark='c'/>So Gödel's sentence is equivalent to the claim that a "
            "certain polynomial equation has no solution: a statement any number theorist can read. "
            "<bookmark mark='d'/>And Hilbert's tenth problem is unsolvable, since a procedure for polynomials would "
            "decide halting."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(h10), FadeIn(ex))
            vo.wait_until("b")
            self.play(FadeIn(mrdp[0]))
            vo.wait_until("c")
            self.play(FadeIn(mrdp[1]))
            vo.wait_until("d")
            self.play(FadeIn(mrdp[2]))
        self.clear_scene()
