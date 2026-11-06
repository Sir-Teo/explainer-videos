from __future__ import annotations

from videos.philosophy.philosophy13.common import *  # noqa: F403


class Ramsey(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"From belief to degrees", r"What is a degree of belief?", lit=(1926, 1937, 1933),
                            part=PART)
        with self.voiceover("Chapter one. From belief to degrees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.betting()
        self.axioms()
        self.simplex()

    def betting(self):
        hcs = VGroup(history_card(1926, r"Frank Ramsey", r"`Truth and Probability'", width=4.4, color=HIST),
                     history_card(1937, r"Bruno de Finetti", r"`La prévision'", width=4.0, color=HIST)).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        ticket = VGroup(RoundedRectangle(width=4.2, height=1.4, corner_radius=0.15, color=BET, stroke_width=3),
                        label(r"pays \$1 \ if it rains tomorrow", font_size=24, color=BET)).move_to([-3.2, 0.2, 0])
        ticket[1].move_to(ticket[0])
        rows = VGroup(
            label(r"your credence in rain: \ the price at which you'd buy \textit{or} sell this ticket", font_size=23),
            label(r"pay 70 cents for it, \ or take 70 cents to issue it: \ credence 0.7", font_size=23, color=CRED),
            label(r"Ramsey: \ measure belief by betting behaviour; \ de Finetti: \ `probability does not exist'",
                  font_size=21, color=GREY_A),
            label(r"only degrees of belief, \ which must cohere", font_size=23, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.0, -1.6, 0])
        for r in rows:
            if r.width > 7.6:
                r.width = 7.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([1.6, -1.7, 0])
        with self.voiceover(
            "How can a degree of belief be measured? <bookmark mark='a'/>Frank Ramsey in 1926, and Bruno de Finetti "
            "independently, proposed: by betting. Picture a ticket that pays one dollar if it rains tomorrow. "
            "<bookmark mark='b'/>Your credence in rain is the price at which you would be equally willing to buy the "
            "ticket or to sell it. <bookmark mark='c'/>If you would pay seventy cents for it, and also take seventy "
            "cents to issue one, your credence is point seven. <bookmark mark='d'/>De Finetti went further: "
            "probability does not exist, he wrote, meaning that there is no probability out in the world, "
            "<bookmark mark='e'/>only degrees of belief, constrained by one requirement, coherence, which we come to "
            "next."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("a")
            self.play(Create(ticket[0]), FadeIn(ticket[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def axioms(self):
        hc = history_card(1933, r"Andrey Kolmogorov", r"\textit{Grundbegriffe der Wahrscheinlichkeitsrechnung}",
                          width=6.4, color=HIST).to_corner(UL, buff=0.35)
        ax = VGroup(MathTex(r"1.\ \ c(A) \geq 0", font_size=36),
                    MathTex(r"2.\ \ c(\top) = 1", font_size=36),
                    MathTex(r"3.\ \ c(A \lor B) = c(A) + c(B) \quad \text{if } A, B \text{ are incompatible}",
                            font_size=36)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.3, 0])
        cons = VGroup(MathTex(r"c(\lnot A) = 1 - c(A)", font_size=30, color=CRED),
                      MathTex(r"c(A \lor B) = c(A) + c(B) - c(A \land B)", font_size=30, color=CRED),
                      MathTex(r"A \vDash B \ \Rightarrow\ c(A) \leq c(B)", font_size=30, color=CRED)).arrange(
            RIGHT, buff=0.6).next_to(ax, DOWN, buff=0.6)
        foot = label(r"probabilism: \ rational credences obey these laws", font_size=26, color=GOAL).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "The laws themselves were set down by Andrey Kolmogorov in 1933, for probability in mathematics. "
            "<bookmark mark='a'/>Three axioms. Credences are never negative. A tautology gets credence one. And the "
            "credence in a disjunction of incompatible propositions is the sum of their credences. "
            "<bookmark mark='b'/>Everything else follows: the credence of not A is one minus that of A; the general "
            "rule for disjunctions; and if A entails B, A can be no more credible than B. <bookmark mark='c'/>The "
            "claim that rational credences must obey these laws is called probabilism. The next two chapters give "
            "the two main arguments for it."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(a) for a in ax], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c) for c in cons], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def simplex(self):
        head = label(r"Credences as points", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        pl = Plane2(center=[-3.6, -0.4, 0], size=3.6)
        good = Dot(pl.p(0.7, 0.3), color=COH, radius=0.09)
        gl = MathTex(r"(0.7, 0.3)", font_size=22, color=COH).next_to(good, UR, buff=0.05)
        bad = Dot(pl.p(0.6, 0.6), color=INC, radius=0.09)
        bl = MathTex(r"(0.6, 0.6)", font_size=22, color=INC).next_to(bad, UR, buff=0.05)
        sx = Simplex3(origin=[2.6, -1.6, 0], scale=2.4)
        sl = label(r"three worlds: \ the coherent credences form a triangle", font_size=21, color=COH).move_to(
            [3.0, 2.3, 0])
        foot = label(r"coherent \ = \ on the simplex; \ incoherent \ = \ anywhere else", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Geometry makes this vivid. <bookmark mark='a'/>With one proposition A, a credence function is a pair "
            "of numbers: your credence in A, and in not A. Plot it as a point. The coherent pairs, which add to "
            "one, lie on the diagonal line. <bookmark mark='b'/>Point seven and point three is on the line. Point six "
            "and point six is off it: it gives more total credence than there is. <bookmark mark='c'/>With three "
            "possible worlds, a credence function is a point in space, and the coherent ones form a triangle, the "
            "probability simplex, with a world at each corner. <bookmark mark='d'/>Coherence means being on the "
            "simplex. Now, why should we be?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(good), FadeIn(gl))
            self.play(FadeIn(bad), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeIn(sx), FadeIn(sl))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
