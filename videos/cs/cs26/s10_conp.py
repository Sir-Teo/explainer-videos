from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs26.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, fit_right, load, mono)


class CoNp(VoiceoverScene):
    def construct(self):
        self.card()
        self.conp()
        self.pratt()
        self.ph()

    def card(self):
        card = chapter_card(9, r"coNP and the polynomial hierarchy", r"Can a no-answer have a short proof?",
                            lit=(1975, 2002), extra=((1975, r"Pratt"), (2002, r"AKS")), part=PART)
        with self.voiceover("Chapter nine. coNP and the polynomial hierarchy."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def conp(self):
        head = label(r"coNP: \ problems whose \textbf{no}-answers have short proofs", font_size=32).to_edge(UP,
                                                                                                 buff=0.35)
        np_ = Ellipse(width=5.0, height=3.4, color=HEAD).set_fill(HEAD, 0.05).shift(LEFT * 4.2 + DOWN * 0.4)
        co = Ellipse(width=5.0, height=3.4, color=LAM).set_fill(LAM, 0.05).shift(LEFT * 1.6 + DOWN * 0.4)
        p_ = Ellipse(width=1.4, height=1.0, color=DATA).set_fill(DATA, 0.2).move_to(LEFT * 2.9 + DOWN * 0.4)
        labs = VGroup(label(r"NP", font_size=24, color=HEAD).move_to(np_.get_center() + LEFT * 1.6 + UP * 0.9),
                      label(r"coNP", font_size=24, color=LAM).move_to(co.get_center() + RIGHT * 1.4 + UP * 0.9),
                      label(r"P", font_size=22, color=DATA).move_to(p_))
        ex = VGroup(label(r"SAT", font_size=18, color=HEAD).move_to(np_.get_center() + LEFT * 1.4 + DOWN * 0.4),
                    label(r"TAUTOLOGY", font_size=18, color=LAM).move_to(co.get_center() + RIGHT * 1.2 + DOWN * 0.4),
                    label(r"factoring", font_size=18, color=YES).move_to(p_.get_center() + UP * 0.85))
        lines = VGroup(
            label(r"a tautology \ (true under every assignment): \\ a yes needs checking all $2^n$ rows", font_size=21,
                  color=WHITE),
            label(r"NP = coNP? \ Unknown; \ most believe not. \\ It would follow from P = NP", font_size=21,
                  color=NO),
            label(r"NP $\cap$ coNP: \ both answers have proofs. \\ Factoring lives here", font_size=21, color=YES),
            label(r"an NP-complete problem in coNP would give NP = coNP: \\ so factoring is probably \textbf{not} "
                  r"NP-complete", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        fit_right(lines)
        with self.voiceover(
            "NP is lopsided: a yes comes with a short proof, a no need not. <bookmark mark='a'/> Flip it and you get "
            "coNP, the problems whose no-answers have short proofs. Is a formula a tautology, true under every "
            "assignment? A no is easy to prove: show one assignment that makes it false. A yes seems to need all two "
            "to the n rows. <bookmark mark='b'/> Whether NP equals coNP is open. If P equalled NP they would be "
            "equal, so this is a second, weaker question. <bookmark mark='c'/> In the overlap sit problems where "
            "both answers have proofs. Factoring is the famous one. <bookmark mark='d'/> If any NP-complete problem "
            "were in coNP, the two classes would coincide. That is the main reason experts doubt factoring is "
            "NP-complete, even though nobody can factor quickly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(np_), FadeIn(co), FadeIn(p_), FadeIn(labs), FadeIn(ex[:2]))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(ex[2]), FadeIn(lines[2]))
            vo.wait_until("d")
            self.play(FadeIn(lines[3]))
        self.wait(0.3)
        self.clear_scene()

    def pratt(self):
        d = load("pratt")
        head = label(r"Why factoring is in NP $\cap$ coNP", font_size=32).to_edge(UP, buff=0.35)
        N = d["N"]
        a, b = d["N_factors"]
        yes = VGroup(
            label(r"``does $N$ have a factor $\le k$?''", font_size=22, color=WHITE),
            label(rf"$N$ = {N}", font_size=22, color=DATA),
            label(rf"certificate: \ the factorization {a} $\times$ {b}, \\ and proofs that both are prime",
                  font_size=21, color=YES),
            label(r"that one certificate answers yes \textbf{and} no, \\ for every $k$", font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(LEFT, buff=0.7).shift(UP * 0.8)
        tree = d["tree"]
        rows = VGroup()
        for t in tree[:14]:
            txt = rf"{t['p']}" + (rf"\ \ (witness $g$ = {t['g']})" if t["g"] else r"")
            rows.add(label(txt, font_size=17, color=[HEAD, DATA, LAM, GREY_A][min(t["depth"], 3)]).shift(
                RIGHT * 0.4 * t["depth"]))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        for r, t in zip(rows, tree[:14]):
            r.shift(RIGHT * 0.4 * t["depth"])
        more = label(r"\ldots", font_size=18, color=GREY_A).next_to(rows, DOWN, buff=0.05).align_to(rows, LEFT)
        right = VGroup(label(r"a \textbf{Pratt certificate} \ (1975) \ that $2^{61} - 1$ is prime", font_size=20,
                             color=WHITE), rows, more).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        right.to_edge(RIGHT, buff=0.6).align_to(yes, UP)
        fit_right(right)
        notes = VGroup(
            label(r"$p$ is prime iff some $g$ has order exactly $p - 1$: \ $g^{p-1} = 1$, \ and $g^{(p-1)/q} \ne 1$ "
                  r"for each prime $q \mid p - 1$", font_size=20, color=GREY_A),
            label(rf"the certificate lists $g$, \ the primes $q$, \ and certificates for each $q$: \ "
                  rf"{d['checks']} checks in all", font_size=20, color=YES),
            label(r"since 2002 primality is in P anyway \ (AKS); \ but the certificate is the idea behind NP "
                  r"$\cap$ coNP", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Why is factoring in both? <bookmark mark='a'/> Ask whether a number N has a factor no larger than k. "
            "<bookmark mark='b'/> A certificate for either answer is the complete factorization, together with "
            "proofs that each factor is prime. Given the prime factors, anyone can check the product and read off "
            "the answer, yes or no, for every k. <bookmark mark='c'/> But how do you prove a number prime briefly? "
            "Vaughan Pratt showed how in 1975. A number p is prime exactly when some g has multiplicative order p "
            "minus one, and that can be checked from the prime factors of p minus one, each with its own "
            "certificate. <bookmark mark='d'/> Here is the certificate for the Mersenne prime two to the sixty-one "
            "minus one: sixty checks in all, each a modular power. <bookmark mark='e'/> Since 2002 we know primality "
            "is in P outright. The certificate remains the clearest picture of what NP intersect coNP means."
        ) as vo:
            self.play(FadeIn(head), FadeIn(yes[0]), FadeIn(yes[1]))
            vo.wait_until("b")
            self.play(FadeIn(yes[2]), FadeIn(yes[3]))
            vo.wait_until("c")
            self.play(FadeIn(right[0]), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.1), FadeIn(more), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()

    def ph(self):
        head = label(r"The polynomial hierarchy", font_size=34).to_edge(UP, buff=0.3)
        rungs = [
            (r"P", r"no quantifier", DATA),
            (r"NP = $\Sigma_1^p$", r"$\exists c$: \ is there a colouring?", HEAD),
            (r"coNP = $\Pi_1^p$", r"$\forall c$: \ is every assignment satisfying?", LAM),
            (r"$\Sigma_2^p$", r"$\exists \forall$: \ is there a circuit of size $k$ equal to this one on all inputs?",
             NO),
            (r"$\Pi_2^p$", r"$\forall \exists$: \ does every input have a short witness?", NO),
        ]
        ladder = VGroup()
        for nm, ex, col in rungs:
            b = RoundedRectangle(width=2.6, height=0.6, corner_radius=0.08, color=col).set_fill(col, 0.15)
            t = label(nm, font_size=21, color=col).move_to(b)
            e = label(ex, font_size=19, color=WHITE).next_to(b, RIGHT, buff=0.3)
            ladder.add(VGroup(b, t, e))
        ladder.arrange(UP, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
        fit_right(ladder)
        notes = VGroup(
            label(r"the arithmetic hierarchy of Part 25, \ with every quantifier bounded by a polynomial \ "
                  r"(Meyer and Stockmeyer, 1972)", font_size=20, color=WHITE),
            label(r"P = NP would collapse it all to P; \ any $\Sigma_k^p = \Pi_k^p$ collapses everything above",
                  font_size=20, color=NO),
            label(r"so ``the hierarchy is infinite'' \ is a stronger bet than P $\ne$ NP, \ and theorists use it: \ "
                  r"Karp--Lipton \ (1980)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Alternate the quantifiers and you climb a ladder. <bookmark mark='a'/> P at the bottom. NP asks whether "
            "there exists a short certificate; coNP whether every candidate fails. <bookmark mark='b'/> One level "
            "up: does there exist a circuit of size k such that, for every input, it agrees with this one? That is "
            "an exists-forall question, sigma two. <bookmark mark='c'/> This is the arithmetic hierarchy of Part 25 "
            "with every quantifier limited to polynomial length, defined by Albert Meyer and Larry Stockmeyer in "
            "1972. <bookmark mark='d'/> If P equalled NP, the whole ladder would collapse to P. More generally, if "
            "any two neighbouring levels coincide, everything above them falls too. <bookmark mark='e'/> So the "
            "assumption that the hierarchy is infinite is a standard bet, a bit stronger than P not equal to NP, "
            "and many theorems, such as Karp and Lipton's, are stated relative to it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in ladder[:3]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(ladder[3]), FadeIn(ladder[4]))
            for mk, n_ in zip("cde", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_))
        self.wait(0.3)
        self.clear_scene()
