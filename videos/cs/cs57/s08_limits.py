from __future__ import annotations

import itertools
import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box


def stacked(rows, whys, buff=0.2):
    """Derivation rows, each with its reason underneath in grey, as one left-aligned column."""
    pairs = VGroup()
    for r, w in zip(rows, whys):
        w.next_to(r, DOWN, buff=0.08, aligned_edge=LEFT)
        pairs.add(VGroup(r, w))
    pairs.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return pairs


def fit_x(g, lo=-6.85, hi=6.85):
    if g.get_right()[0] > hi:
        g.shift(LEFT * (g.get_right()[0] - hi))
    if g.get_left()[0] < lo:
        g.shift(RIGHT * (lo - g.get_left()[0]))
    return g


def arrow(a, b, color=GREY_B):
    return Arrow(a.get_right(), b.get_left(), buff=0.12, stroke_width=2.5, color=color,
                 max_tip_length_to_length_ratio=0.18)


class Limits(VoiceoverScene):
    def construct(self):
        self.card()
        self.proper()
        self.crypto()
        self.sq()
        self.parity()
        self.landscape()

    def card(self):
        card = chapter_card(7, r"What cannot be learned", r"When is enough data not enough?", lit=(1988, 1994),
                            extra=((1988, r"Pitt and Valiant: \ hardness of proper learning"),
                                   (1994, r"Kearns and Valiant: \ cryptographic limits")), part=PART)
        with self.voiceover("Chapter seven. What cannot be learned."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ data is not the problem; time is
    def proper(self):
        head = label(r"Enough data, \ not enough time", font_size=36).to_edge(UP, buff=0.3)
        top = VGroup(
            MathTex(r"|\mathcal H_s| \le 2^{O(s \log s)}", r"\ \Rightarrow\ ",
                    r"m = O\Big(\frac{s\log s + \ln(1/\delta)}{\epsilon}\Big)", font_size=28),
            label(r"circuits of size $s$, \ and chapter 1's finite-class bound: \ the examples are never the problem",
                  font_size=17, color=GREY_B),
        ).arrange(DOWN, buff=0.1).next_to(head, DOWN, buff=0.35)
        top[0][2].set_color(YES)
        c1, c2, c3 = DATA, LAM, KERN
        dnf = MathTex(r"(x_1", r"\wedge", r"x_2)", r"\ \vee\ ", r"x_3", r"\ \vee\ ", r"(x_4", r"\wedge", r"x_5)",
                      font_size=32)
        for k, c in ((0, c1), (2, c1), (4, c2), (6, c3), (8, c3)):
            dnf[k].set_color(c)
        cl, src = [], []
        for ia, a in ((0, "x_1"), (2, "x_2")):
            for ib, b in ((6, "x_4"), (8, "x_5")):
                m = MathTex(r"(", a, r"\vee", r"x_3", r"\vee", b, r")", font_size=28)
                m[1].set_color(c1)
                m[3].set_color(c2)
                m[5].set_color(c3)
                cl.append(m)
                src.append((ia, ib))
        cnf = VGroup(*cl).arrange(RIGHT, buff=0.12)
        eq = MathTex(r"=", font_size=32)
        block = VGroup(dnf, eq, cnf).arrange(DOWN, buff=0.25).next_to(top, DOWN, buff=0.45).to_edge(LEFT, buff=0.7)
        why = wrapped_label(r"distribute: \ one literal from each term, \ every way \ ($2 \times 1 \times 2 = 4$ "
                            r"clauses)", 6.0, font_size=18, color=GREY_B).next_to(block, DOWN, buff=0.2).align_to(
            block, LEFT)
        ill = note(r"illustrative formula", font_size=16).next_to(why, DOWN, buff=0.1).align_to(block, LEFT)
        bad = VGroup(RoundedRectangle(width=5.4, height=1.3, corner_radius=0.12, stroke_color=NO, stroke_width=2,
                                      fill_color=BG, fill_opacity=1))
        bad.add(wrapped_label(r"output a 3-term DNF: \ NP-hard, \ unless RP = NP \ (Pitt and Valiant 1988)", 5.0,
                              font_size=19, color=NO).move_to(bad[0]))
        good = VGroup(RoundedRectangle(width=5.4, height=1.6, corner_radius=0.12, stroke_color=YES, stroke_width=2,
                                       fill_color=BG, fill_opacity=1))
        good.add(wrapped_label(r"output a 3-CNF instead: \ start with all $(2n)^3$ clauses, \ delete each one a "
                               r"positive example falsifies \ (Valiant 1984): \ polynomial time", 5.0, font_size=19,
                               color=YES).move_to(good[0]))
        VGroup(bad, good).arrange(DOWN, buff=0.35).next_to(top, DOWN, buff=0.45).to_edge(RIGHT, buff=0.45)
        foot = wrapped_label(r"hardness that depends on the hypothesis we must output is not real hardness: \ we "
                             r"need limits that hold \textit{whatever} the learner outputs", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Data is rarely what limits learning. <bookmark mark='a'/> There are at most two to the order s "
            "log s circuits of size s, so chapter one's bound says polynomially many examples suffice. The "
            "trouble is time: finding a hypothesis that fits. <bookmark mark='b'/> Take formulas that are an "
            "or of three ands, like this one. Leonard Pitt and Valiant proved in 1988 that finding such a "
            "formula consistent with the data is NP-hard. <bookmark mark='c'/> But distribute the or over the "
            "ands: the same function is an and of clauses, each taking one literal from each term. "
            "<bookmark mark='d'/> Clauses of three literals are few, and Valiant's elimination learns them in "
            "polynomial time. The class is easy; its own representation was hard. <bookmark mark='e'/> So real "
            "limits must hold whatever the learner outputs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(top[0]), FadeIn(top[1]))
            vo.wait_until("b")
            self.play(Write(dnf), FadeIn(ill), FadeIn(bad))
            vo.wait_until("c")
            self.play(Write(eq))
            for m, (ia, ib) in zip(cnf, src):
                self.play(TransformFromCopy(VGroup(dnf[ia], dnf[4], dnf[ib]), m), run_time=0.7)
            self.play(FadeIn(why))
            vo.wait_until("d")
            self.play(FadeIn(good))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ cryptographic hardness
    def crypto(self):
        head = label(r"A learner would be a code-breaker", font_size=36).to_edge(UP, buff=0.3)
        pk = module_box(r"public key", KERN, w=1.9, h=0.75)
        ex = module_box(r"examples $(\mathrm{Enc}(b),\, b)$", DATA, w=2.8, h=0.75)
        ln = module_box(r"learner for $\mathcal C$", HEAD, w=2.3, h=0.75)
        hy = module_box(r"hypothesis $h$", YES, w=2.1, h=0.75)
        row1 = VGroup(pk, ex, ln, hy).arrange(RIGHT, buff=0.55).next_to(head, DOWN, buff=0.6)
        fit_x(row1)
        a1 = VGroup(arrow(pk, ex), arrow(ex, ln), arrow(ln, hy))
        ch = module_box(r"challenge $c = \mathrm{Enc}(b^*)$", NO, w=3.2, h=0.75)
        gs = module_box(r"$h(c) = b^*$\,?", NO, w=2.1, h=0.75)
        ch.next_to(hy, DOWN, buff=0.8).align_to(ex, LEFT)
        gs.next_to(hy, DOWN, buff=0.8).align_to(hy, LEFT)
        a2 = VGroup(Arrow(ch.get_right(), gs.get_left(), buff=0.12, stroke_width=2.5, color=GREY_B,
                          max_tip_length_to_length_ratio=0.1),
                    Arrow(hy.get_bottom(), gs.get_top(), buff=0.1, stroke_width=2.5, color=GREY_B,
                          max_tip_length_to_length_ratio=0.25))
        n1 = label(r"anyone can make these: \ encryption is public", font_size=17, color=GREY_B).next_to(
            ex, UP, buff=0.12)
        fs = 26
        rows = [
            MathTex(r"x = \mathrm{Enc}_{pk}(b)", r",\qquad", r"f(x) = \mathrm{Dec}_{sk}(x) = b", font_size=fs),
            MathTex(r"f \in \mathcal C", r"\ \Rightarrow\ ", r"\Pr\big[h(c) = b^*\big] \ge \tfrac12 + "
                    r"\tfrac{1}{\mathrm{poly}}", font_size=fs),
        ]
        whys = [
            label(r"the target concept is the decryption function, \ and the learner never sees $sk$", font_size=17,
                  color=GREY_B),
            label(r"even a \textit{weak} learner would beat the cryptosystem", font_size=17, color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.3).next_to(VGroup(ch, gs), DOWN, buff=0.55).to_edge(LEFT, buff=0.7)
        thm = wrapped_label(r"\textbf{Kearns and Valiant \ (1994)}: \ if RSA, \ or factoring Blum integers, \ is hard, "
                            r"\ no efficient algorithm learns small Boolean formulas or finite automata, \ whatever "
                            r"hypotheses it outputs", 5.6, font_size=19, color=HEAD)
        prf = wrapped_label(r"and if pseudorandom functions exist \ (Goldreich, \ Goldwasser and Micali 1986; \ "
                            r"Part 29), \ small circuits cannot be learned even with queries", 5.6, font_size=19,
                            color=LAM)
        right = VGroup(thm, prf).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(col, RIGHT, buff=0.5).align_to(
            col, UP)
        fit_x(right)
        with self.voiceover(
            "Michael Kearns and Leslie Valiant found such limits in cryptography; the journal version appeared "
            "in 1994. <bookmark mark='a'/> Take a public-key cryptosystem. Anyone with the public key can "
            "encrypt random bits, so anyone can make labelled examples: a ciphertext, and the bit inside it. "
            "<bookmark mark='b'/> The target concept is the decryption function. <bookmark mark='c'/> If some "
            "class of functions can compute decryption, a learner for that class, fed these examples, returns a "
            "hypothesis that decrypts a fresh challenge better than chance. That breaks the cryptosystem. "
            "<bookmark mark='d'/> So, if RSA or factoring is hard, no efficient algorithm learns small Boolean "
            "formulas or finite automata, whatever it outputs. <bookmark mark='e'/> And if pseudorandom functions "
            "exist, from Part 29, small circuits cannot be learned even by asking questions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pk), GrowArrow(a1[0]), FadeIn(ex), FadeIn(n1))
            vo.wait_until("b")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("c")
            self.play(GrowArrow(a1[1]), FadeIn(ln), GrowArrow(a1[2]), FadeIn(hy))
            self.play(FadeIn(ch), GrowArrow(a2[0]), GrowArrow(a2[1]), FadeIn(gs))
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("d")
            self.play(FadeIn(thm))
            vo.wait_until("e")
            self.play(FadeIn(prf))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ statistical queries and parity
    def sq(self):
        head = label(r"Statistical queries cannot find a parity", font_size=36).to_edge(UP, buff=0.3)
        n, k = 10, 3
        subsets = list(itertools.combinations(range(n), k))
        cols_, s = 12, 0.3
        cells = VGroup(*[Square(side_length=s * 0.82, stroke_width=0, fill_color=GREY_D, fill_opacity=1).move_to(
            [(j % cols_) * s, -(j // cols_) * s, 0]) for j in range(len(subsets))])
        cells.next_to(head, DOWN, buff=0.85).to_edge(LEFT, buff=0.8)
        ct = label(rf"the $\binom{{{n}}}{{{k}}} = {len(subsets)}$ candidate sets $S$, \ $n = {n}$, \ $k = {k}$",
                   font_size=18, color=GREY_A).next_to(cells, UP, buff=0.15).align_to(cells, LEFT)
        tau = 0.25
        per = int(1 / tau ** 2)
        rng = np.random.default_rng(8)
        qs = [rng.choice(len(subsets), per, replace=False) for _ in range(3)]
        qn = label(rf"each query, \ tolerance $\tau = {tau:g}$, \ rules out at most $1/\tau^2 = {per}$", font_size=18,
                   color=HEAD).next_to(cells, DOWN, buff=0.2).align_to(cells, LEFT)
        ill = note(r"illustrative", font_size=16).next_to(qn, DOWN, buff=0.1).align_to(cells, LEFT)
        fs = 25
        rows = [
            MathTex(r"\chi_S(x) = (-1)^{\sum_{i \in S} x_i}", r",\qquad", r"\mathbb E[\chi_S \chi_T] = 0 \ \ "
                    r"(S \ne T)", font_size=fs),
            MathTex(r"q(x, y) = q_0(x) + y\, q_1(x)", r"\ \Rightarrow\ ", r"\mathbb E\, q = \mathbb E\, q_0 + "
                    r"\langle q_1, \chi_S\rangle", font_size=fs),
            MathTex(r"\sum_S \langle q_1, \chi_S\rangle^2 \le 1", r"\ \Rightarrow\ ",
                    r"\#\big\{S : |\langle q_1, \chi_S\rangle| \ge \tau\big\} \le 1/\tau^2", font_size=fs),
            MathTex(r"\text{queries}", r"\ \ge\ ", r"\tau^2 \binom{n}{k}", font_size=fs + 2),
        ]
        rows[3][2].set_color(NO)
        whys = [
            label(r"the label is a parity of the bits in $S$; \ different parities are orthogonal", font_size=17,
                  color=GREY_B),
            label(r"any query splits so, \ since $y = \pm 1$; \ only the second term depends on $S$", font_size=17,
                  color=GREY_B),
            label(r"Bessel's inequality: \ a query is informative about very few $S$", font_size=17, color=GREY_B),
            label(r"the oracle answers $\mathbb E\, q_0$ and stays within $\tau$ for all the rest", font_size=17,
                  color=GREY_B),
        ]
        col = stacked(rows, whys, buff=0.22).next_to(cells, RIGHT, buff=0.6).align_to(ct, UP).shift(UP * 0.2)
        fit_x(col)
        model = wrapped_label(r"Kearns's \textbf{statistical query} model: \ ask for the average of any $q(x, y)$, \ "
                              r"get it to within $\tau$; \ such learners tolerate noise, \ and gradient descent on an "
                              r"average loss is one", 12.0, font_size=19, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Kearns also defined a gentler kind of learner. <bookmark mark='a'/> A statistical-query learner "
            "never looks at single examples; it asks for the average of some function of an example and its "
            "label, and gets it to within a tolerance tau. Such learners survive noisy labels, and gradient "
            "descent on an average loss is one. <bookmark mark='b'/> Now let the label be the parity of an "
            "unknown set of k bits. Different parities are orthogonal. <bookmark mark='c'/> Any query splits into"
            " a part that ignores the label and a part that correlates with it, and only the second depends on "
            "the set. <bookmark mark='d'/> By Bessel's inequality those correlations have squares summing to at "
            "most one, so each query is informative about at most one over tau squared sets. "
            "<bookmark mark='e'/> The rest look identical, so finding the set takes at least tau squared times n "
            "choose k queries."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(ct), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(model))
            vo.wait_until("b")
            self.play(Write(col[0][0]), FadeIn(col[0][1]))
            vo.wait_until("c")
            self.play(Write(col[1][0]), FadeIn(col[1][1]))
            vo.wait_until("d")
            self.play(Write(col[2][0]), FadeIn(col[2][1]), FadeIn(qn))
            for q in qs:
                self.play(*[cells[j].animate.set_fill(HEAD) for j in q], run_time=0.5)
                self.play(*[cells[j].animate.set_fill(GREY_E) for j in q], run_time=0.4)
            vo.wait_until("e")
            self.play(Write(col[3][0]), FadeIn(col[3][1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ parity, measured
    def parity(self):
        rows_ = load("parity")["rows"]
        k = rows_[0]["k"]
        head = label(r"Parity: \ easy for algebra, \ hard for statistics", font_size=36).to_edge(UP, buff=0.3)
        # bars: subsets to search against n
        vmax = max(r["subsets_total"] for r in rows_)
        H = 3.0
        bars = VGroup()
        for r in rows_:
            tot = Rectangle(width=0.7, height=H * r["subsets_total"] / vmax, stroke_color=GREY_B, stroke_width=1.5,
                            fill_opacity=0)
            tried = Rectangle(width=0.7, height=max(0.02, H * r["subsets_tried"] / vmax), stroke_width=0,
                              fill_color=NO, fill_opacity=0.7)
            tried.align_to(tot, DOWN)
            nl = label(rf"$n = {r['n']}$", font_size=17, color=GREY_A).next_to(tot, DOWN, buff=0.1)
            vl = label(rf"{r['subsets_total']:,}".replace(",", "{,}"), font_size=16, color=GREY_B).next_to(
                tot, UP, buff=0.06)
            bars.add(VGroup(tot, tried, nl, vl))
        bars.arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        for b in bars:
            b[2].next_to(b[0], DOWN, buff=0.1)
        bars.next_to(head, DOWN, buff=0.9).to_edge(LEFT, buff=0.9)
        bt = wrapped_label(rf"outline: \ all $\binom{{n}}{{{k}}}$ sets of {k} bits; \ red: \ how many a search "
                           r"tried before the right one", 4.6, font_size=17, color=GREY_A).next_to(
            bars, UP, buff=0.3).align_to(bars, LEFT)
        hdr = [r"$n$", r"best single bit", r"search", r"elimination"]
        trs = [[f"{r['n']}", f"{r['max_single_bit_correlation']:.3f}", rf"{1000 * r['search_seconds']:.1f} ms",
                rf"{1000 * r['gauss_seconds']:.2f} ms"] for r in rows_]
        tab = grid_table(hdr, trs, widths=[0.7, 1.9, 1.3, 1.6], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(bars, RIGHT, buff=0.8).align_to(bars, UP).shift(UP * 0.3)
        fit_x(tab)
        tnote = wrapped_label(r"400 random examples each; \ ``best single bit'': \ its largest correlation with the "
                              r"label, \ about the sampling noise of $1/\sqrt{400} = 0.05$", 5.4, font_size=17,
                              color=GREY_B).next_to(tab, DOWN, buff=0.2).align_to(tab, LEFT)
        ok = all(r["found"] and r["gauss_found"] for r in rows_)
        side = VGroup(
            wrapped_label(r"elimination over GF(2) \ (Part 28) \ solves the parity from $2n$ examples: \ parity is "
                          r"PAC-learnable, \ just not by statistics" + (r"; \ both found every set" if ok else ""),
                          5.4, font_size=18, color=YES),
            wrapped_label(r"flip a few labels and elimination breaks: \ \textbf{learning parity with noise} is "
                          r"believed hard; \ the best known algorithm takes $2^{O(n/\log n)}$ \ (Blum, \ Kalai and "
                          r"Wasserman 2003)", 5.4, font_size=18, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tnote, DOWN, buff=0.3).align_to(tab, LEFT)
        p7 = wrapped_label(r"Part 7's parity branch: \ no single history bit predicts it, \ and the perceptron "
                           r"predictor got 49\% right", 4.8, font_size=18, color=KERN).next_to(bars, DOWN, buff=0.6)
        p7.align_to(bars, LEFT)
        with self.voiceover(
            "Here are sparse parities of three bits among n, from four hundred random examples. "
            "<bookmark mark='a'/> No single bit correlates with the label beyond the sampling noise. "
            "<bookmark mark='b'/> A search over sets of three bits must try up to n choose three of them, and "
            "it did: fifteen hundred and eight of fifteen hundred and forty at n equal to twenty-two. "
            "<bookmark mark='c'/> Yet parity is easy for algebra. Each example is a linear equation over the "
            "field of two elements, and Gaussian elimination, from Part 28, solves it from about two n examples "
            "in under a millisecond. Parity is learnable, just not by statistics. <bookmark mark='d'/> Flip a "
            "few labels and elimination breaks. Learning parity with noise is believed hard; the best known "
            "algorithm, by Avrim Blum, Adam Kalai and Hal Wasserman, takes time two to the n over log n. "
            "<bookmark mark='e'/> It is Part 7's parity branch again: no single history bit predicts it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.cells[0][0]), *[FadeIn(c) for c in tab.cells[0][1:]], FadeIn(tab.rule))
            for r in range(1, len(rows_) + 1):
                self.play(*[FadeIn(c) for c in tab.cells[r]], run_time=0.3)
            vo.wait_until("a")
            self.play(Indicate(VGroup(*[tab.cells[r][1] for r in range(1, len(rows_) + 1)]), color=WHITE),
                      FadeIn(tnote))
            vo.wait_until("b")
            self.play(FadeIn(bt), LaggedStart(*[FadeIn(b[0]) for b in bars], lag_ratio=0.2),
                      *[FadeIn(b[2]) for b in bars], *[FadeIn(b[3]) for b in bars])
            self.play(LaggedStart(*[GrowFromEdge(b[1], DOWN) for b in bars], lag_ratio=0.2), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[0]), Indicate(VGroup(*[tab.cells[r][3] for r in range(1, len(rows_) + 1)]),
                                                color=WHITE))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(p7))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the landscape
    def landscape(self):
        head = label(r"The landscape", font_size=36).to_edge(UP, buff=0.3)
        specs = [
            (12.6, 6.0, GREY_B, r"finite VC dimension: \ learnable from enough data \ (chapter 2)"),
            (9.6, 4.4, HEAD, r"learnable in polynomial time"),
            (5.4, 2.6, YES, r"statistical queries: \ noise-tolerant"),
        ]
        boxes = VGroup()
        for w, h, c, t in specs:
            r = RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=c, stroke_width=2.5,
                                 fill_color=c, fill_opacity=0.05)
            boxes.add(r)
        boxes[0].next_to(head, DOWN, buff=0.35)
        boxes[1].align_to(boxes[0], DOWN).shift(UP * 0.3).align_to(boxes[0], LEFT).shift(RIGHT * 0.3)
        boxes[2].align_to(boxes[1], DOWN).shift(UP * 0.3).align_to(boxes[1], LEFT).shift(RIGHT * 0.3)
        titles = VGroup(*[label(t, font_size=20, color=c).next_to(b.get_corner(UL), DR, buff=0.15)
                          for (w, h, c, t), b in zip(specs, boxes)])
        items = VGroup(
            wrapped_label(r"conjunctions, \ $k$-CNF, \ halfspaces with a margin", 4.8, font_size=19, color=WHITE),
            wrapped_label(r"parities: \ Gaussian elimination", 3.0, font_size=19, color=WHITE),
            wrapped_label(r"small formulas, \ finite automata, \ small circuits: \ not, \ if cryptography is "
                          r"sound", 2.2, font_size=19, color=WHITE),
        )
        items[0].move_to(boxes[2]).shift(DOWN * 0.25)
        items[1].next_to(boxes[2], RIGHT, buff=0.35).shift(DOWN * 0.2)
        items[2].next_to(boxes[1], RIGHT, buff=0.3).shift(DOWN * 0.2)
        out = label(r"outside: \ infinite VC dimension, \ not learnable at all", font_size=19, color=NO).next_to(
            boxes[0], DOWN, buff=0.15)
        with self.voiceover(
            "So the map of what can be learned has three walls. <bookmark mark='a'/> The outer wall is "
            "statistical: a class with infinite VC dimension cannot be learned from any amount of data. "
            "<bookmark mark='b'/> Inside it, the computational wall. Small formulas, automata and circuits need "
            "few examples, but learning them would break cryptography. <bookmark mark='c'/> Inside that, the "
            "statistical-query wall. Conjunctions and halfspaces with a margin sit inside it and survive noise; "
            "<bookmark mark='d'/> parities sit between, learnable only by algebra that a single wrong label "
            "spoils. Avrim Blum and colleagues showed in 1994 that this wall is set by one number, the "
            "statistical-query dimension: how many nearly orthogonal functions a class contains."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(boxes[0]), FadeIn(titles[0]), FadeIn(out))
            vo.wait_until("b")
            self.play(Create(boxes[1]), FadeIn(titles[1]), FadeIn(items[2]))
            vo.wait_until("c")
            self.play(Create(boxes[2]), FadeIn(titles[2]), FadeIn(items[0]))
            vo.wait_until("d")
            self.play(FadeIn(items[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, LAM, math)
