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
        VGroup(np_, co, p_, labs, ex).scale(0.8).move_to(LEFT * 3.7 + DOWN * 0.4)
        lines = VGroup(
            label('general-formula tautology: \\\\ falsifying assignments certify no; \\\\ brute force is one upper bound', font_size=21,
                  color=WHITE),
            label(r"NP = coNP? \ Unknown; \ most believe not. \\ It would follow from P = NP", font_size=21,
                  color=NO),
            label(r"NP $\cap$ coNP: \ both answers have proofs. \\ Factoring lives here", font_size=21, color=YES),
            label('NP-complete in coNP would give \\\\ NP = coNP; factoring is probably \\\\ not NP-complete', font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 3.5 + DOWN * 0.2)
        fit_right(lines)
        with self.voiceover(
            "NP requires short certificates for yes-instances. <bookmark mark='a'/> CoNP consists of languages whose complements are in NP, so their no-instances have short efficiently checkable certificates. <bookmark mark='b'/> Tautology for general Boolean formulas is a coNP-complete example: a falsifying assignment certifies a no-answer. Enumerating every assignment is one decision method, not a necessity for every yes-instance. CNF tautology has a different, easy structure. <bookmark mark='c'/> Whether NP equals coNP is open; equality would follow from P equals NP, but the converse is not known. <bookmark mark='d'/> Bounded nontrivial-factor decision lies in both classes. If an NP-complete language were also in coNP, then NP would equal coNP. The overlapping circles are a schematic, not a proof of strict separation."
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
            label('does $N\\ge2$ have a divisor $2\\le d\\le k<N$?', font_size=22, color=WHITE),
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
            label('modulo $p$: $g^{p-1}\\equiv1$ and $g^{(p-1)/q}\\not\\equiv1$ for every certified prime $q\\mid p-1$', font_size=20, color=GREY_A),
            label(rf"complete tree: {d['checks']} certificate nodes; \\ separate arithmetic check: {d['reference']['modular_powers']} modular powers", font_size=20, color=YES),
            label(r"since 2002 primality is in P anyway \ (AKS); \ but the certificate is the idea behind NP "
                  r"$\cap$ coNP", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Define the factor question carefully. <bookmark mark='a'/> For N at least two and k below N, ask whether N has a divisor d between two and k. Divisor one is excluded. <bookmark mark='b'/> The full prime factorization, with primality certificates, answers both yes and no: compare the smallest prime factor with k. Its total bit length is polynomial in log N. <bookmark mark='c'/> Pratt certificates recursively certify the prime factors of p minus one and exhibit an element of order p minus one modulo p. The order criterion then proves p prime. <bookmark mark='d'/> We retain the complete certificate for two to the sixty-first minus one and certificates for both displayed factors. One checker counts certificate nodes; a separate arithmetic checker records the modular powers. These are different counts. <bookmark mark='e'/> AKS later put primality decision itself in P. Factoring search still has no known classical polynomial-time algorithm."
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
            (r"P", r"polynomial-time predicate", DATA),
            (r"NP = $\Sigma_1^p$", r"$\exists c$: certificate", HEAD),
            (r"coNP = $\Pi_1^p$", r"$\forall c$: dual predicate", LAM),
            (r"$\Sigma_2^p$", r"$\exists u\,\forall v$: predicate", NO),
            (r"$\Pi_2^p$", r"$\forall u\,\exists v$: predicate", NO),
        ]
        positions = [(0,-0.7),(-3.4,0.7),(3.4,0.7),(-3.4,2.0),(3.4,2.0)]
        ladder = VGroup()
        for (nm,ex,col),(x,y) in zip(rungs,positions):
            box = RoundedRectangle(width=2.0,height=0.6,corner_radius=0.08,color=col).set_fill(col,0.15)
            title = label(nm,font_size=20,color=col).move_to(box)
            detail = label(ex,font_size=17,color=WHITE).next_to(box,DOWN,buff=0.12)
            item = VGroup(box,title,detail)
            if item.width > 6.1: item.width = 6.1
            ladder.add(item.move_to([x,y,0]))
        notes = VGroup(
            label('polynomially bounded BIT LENGTH for each quantified string; NP/coNP are duals on level 1', font_size=20, color=WHITE),
            label('$\\Sigma_k^p=\\Pi_k^p$ collapses PH to level $k$; P = NP collapses it to P',
                  font_size=20, color=NO),
            label(r"so ``the hierarchy is infinite'' \ is a stronger bet than P $\ne$ NP, \ and theorists use it: \ "
                  r"Karp--Lipton \ (1980)", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Alternation produces the polynomial hierarchy. <bookmark mark='a'/> An existential block of polynomially many bits followed by a polynomial-time predicate gives NP. <bookmark mark='b'/> A universal block gives coNP. They are duals at the same first level, not successive levels. <bookmark mark='c'/> An existential block followed by a universal block gives the second existential level, with its universal-existential dual beside it. <bookmark mark='d'/> Each quantified string has polynomial BIT LENGTH in the original input; the numerical values can therefore be exponentially large. <bookmark mark='e'/> If the existential and universal classes coincide at level k, the entire hierarchy collapses to that level. P equals NP would collapse it to P. None of the displayed separations is assumed proved."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ladder[0]),FadeIn(ladder[1]))
            vo.wait_until("b")
            self.play(FadeIn(ladder[2]))
            vo.wait_until("c")
            self.play(FadeIn(ladder[3]),FadeIn(ladder[4]),FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(FadeIn(notes[2]))
        self.wait(0.3)
        self.clear_scene()
