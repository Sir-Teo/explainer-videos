from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs20.common import (CTRL, DATA, HEAD, LAM, NO, PART, YES, draw_graph, grid_table, load, mono, words)


class Identity(VoiceoverScene):
    def construct(self):
        self.card()
        self.lemma()
        self.claim()
        self.tutte()
        self.fingerprint()

    def card(self):
        card = chapter_card(3, r"Is this polynomial zero?", r"How do you test an identity you can't expand?",
                            lit=(1979, 1980), extra=((1979, r"Lov\'asz's matchings"), (1980, r"Schwartz--Zippel")),
                            part=PART)
        with self.voiceover((
            'Chapter three. Is this polynomial zero?'
        )):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lemma(self):
        head = label(r"The Schwartz--Zippel lemma", font_size=36).to_edge(UP, buff=0.35)
        stmt = MathTex(r"p\ne0\text{ over a field},\ \deg p=d,\quad r_i\overset{\rm iid}{\sim}\mathrm{Unif}(S)"
                       r"\quad\Longrightarrow\quad \Pr[\,p(r_1, \dots, r_n) = 0\,] \le \frac{d}{|S|}",
                       font_size=34, color=YES)
        stmt.next_to(head, DOWN, buff=0.5)
        ax = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=4.4, y_length=2.6,
                  axis_config={"color": GREY_D, "include_ticks": False}).to_edge(LEFT, buff=0.7).shift(DOWN * 1.3)
        curve = ax.plot(lambda x: 0.25 * (x + 2.2) * (x - 0.4) * (x - 2.0), x_range=[-2.9, 2.9], color=DATA)
        roots = VGroup(*[Dot(ax.c2p(r, 0), color=NO, radius=0.07) for r in (-2.2, 0.4, 2.0)])
        one = label(r"one variable: \ a nonzero polynomial of degree $d$ \\ has at most $d$ roots", font_size=20,
                    color=GREY_A).next_to(ax, UP, buff=0.2)
        induct = VGroup(
            label(r"$n$ variables, \ by induction:", font_size=22, color=WHITE),
            MathTex(r"p = \sum_{i=0}^{k} x_1^{\,i}\; q_i(x_2, \dots, x_n), \quad q_k \ne 0", font_size=30,
                    color=LAM),
            label(r"$q_k(r_2, \dots) = 0$: \ probability $\le (d - k)/|S|$", font_size=20, color=GREY_A),
            label(r"otherwise $p$ is a nonzero polynomial in $x_1$ of degree $k$: \ $\le k/|S|$", font_size=20,
                  color=GREY_A),
            label(r"total: \ $\le d/|S|$", font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(RIGHT, buff=0.5).shift(DOWN * 1.1)
        with self.voiceover(
            (
            "Freivalds' check is a special case of a general fact. <bookmark mark='a'/> Let p be a nonzero formal "
            'polynomial of total degree d over a field. Choose each variable independently and uniformly from the '
            'same finite subset S of that field. Then the probability that p evaluates to zero is at most d divided '
            'by the size of S, capped at one. This is the Schwartz–Zippel lemma, also associated with DeMillo and '
            "Lipton, around 1980. <bookmark mark='b'/> In one variable, a nonzero degree-d polynomial has at most d "
            "roots. <bookmark mark='c'/> In several variables, write p in the first variable, with highest power k. "
            'Its leading coefficient has total degree at most d minus k. Inductively that coefficient vanishes with '
            'probability at most d minus k over the size of S; otherwise the remaining univariate polynomial has at '
            'most k roots. Adding the two bounds proves the claim.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(stmt))
            vo.wait_until("a")
            self.play(Indicate(stmt, color=YES))
            vo.wait_until("b")
            self.play(Create(ax), Create(curve), FadeIn(one))
            self.play(LaggedStart(*[GrowFromCenter(r) for r in roots], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in induct], lag_ratio=0.5), run_time=6.0)
        self.wait(0.3)
        self.clear_scene()

    def claim(self):
        d = load("pit")
        head = label(r"Testing an identity without expanding it", font_size=34).to_edge(UP, buff=0.35)
        claim = MathTex(r"(x - y)(y - z)(z - x)", r"\overset{?}{=}",
                        r"x^2 z - x^2 y + y^2 x - y^2 z + z^2 y", r"+ z^2 x", font_size=34)
        claim[0].set_color(DATA)
        claim[2].set_color(LAM)
        claim[3].set_color(LAM)
        claim.next_to(head, DOWN, buff=0.45)
        rows = [[str(r["S"]), f"{r['agree']:.4f}", f"{min(r['bound'], 1):.4f}"] for r in d["sz"]]
        tab = grid_table([r"$|S|$", r"the sides agreed", r"bound $3/|S|$"], rows, widths=[1.6, 3.0, 2.4],
                         row_h=0.4, font_size=20, mono_cols=(), colors=[[GREY_A, YES, HEAD]] * len(rows))
        tab.next_to(claim, DOWN, buff=0.5).shift(LEFT * 3.0)
        v = d["vandermonde"]
        side = VGroup(
            label(r"20{,}000 random points per row", font_size=20, color=GREY_A),
            label(r"one sign is wrong: \ the difference is $2xz^2$", font_size=20, color=NO),
            label(r"it vanishes when $x = 0$ or $z = 0$", font_size=20, color=GREY_A),
            label(rf"Vandermonde, \ $n = {v['n']}$: \ $\det V = \prod_{{i<j}} (x_j - x_i)$", font_size=20,
                  color=WHITE),
            label(rf"{words(v['terms'])} terms if expanded; \ {v['ok']} of {v['trials']} random points agree",
                  font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, RIGHT, buff=0.6)
        with self.voiceover(
            (
            'Here is a claimed identity: the product x minus y, times y minus z, times z minus x, against an '
            "expansion. <bookmark mark='a'/> Instead of expanding, substitute random numbers and compare. We did "
            "this twenty thousand times for each size of S. <bookmark mark='b'/> The claim is false: one sign is "
            'wrong, so the two sides differ by two x z squared, a polynomial of degree three. It vanishes only when '
            "x or z is zero, which is why the agreement rates sit a little under the lemma's bound of three over S. "
            'With a thousand values, one test in five hundred is fooled; twenty tests are fooled with probability '
            "below ten to the minus fifty. <bookmark mark='c'/> The idea scales. The determinant of an eight by "
            'eight Vandermonde matrix equals a product of differences, a polynomial with forty thousand terms if you'
            ' expand it. Evaluating both sides at fifty random points modulo a large prime took a fraction of a '
            'millisecond each, and they agreed every time.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(claim))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule), FadeIn(side[0]))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(Indicate(claim[3], color=NO), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.3)
        self.clear_scene()

    def tutte(self):
        d = load("pit")
        head = label(r"Perfect matchings from a determinant", font_size=34).to_edge(UP, buff=0.35)
        pos = {1: (-5.6, 1.2), 2: (-3.8, 1.2), 3: (-3.8, -0.4), 4: (-5.6, -0.4)}
        g, nodes, es = draw_graph(pos, [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)], r=0.28)
        T = MathTex(r"T = \begin{pmatrix} 0 & x_{12} & x_{13} & x_{14} \\ -x_{12} & 0 & x_{23} & 0 \\ "
                    r"-x_{13} & -x_{23} & 0 & x_{34} \\ -x_{14} & 0 & -x_{34} & 0 \end{pmatrix}", font_size=30,
                    color=LAM).move_to(RIGHT * 0.4 + UP * 0.4)
        det = MathTex(r"\det T = (x_{12}x_{34} + x_{14}x_{23})^2", font_size=30, color=YES).next_to(T, RIGHT,
                                                                                                  buff=0.4)
        if det.get_right()[0] > 6.9:
            det.shift(LEFT * (det.get_right()[0] - 6.9))
            det.next_to(T, DOWN, buff=0.3)
        pm = VGroup(es[(1, 2)].copy().set_stroke(YES, 6), es[(3, 4)].copy().set_stroke(YES, 6))
        pm2 = VGroup(es[(4, 1)].copy().set_stroke(HEAD, 6), es[(2, 3)].copy().set_stroke(HEAD, 6))
        facts = VGroup(
            label(r"Tutte (1947): \ $\det T \ne 0$ exactly when a perfect matching exists", font_size=21,
                  color=WHITE),
            label(r"Lov\'asz (1979): \ put random numbers mod $p$ in for the $x_{ij}$; \ wrong with probability "
                  r"$\le n/p$", font_size=21, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=1.3)
        rows = d["tutte"]
        tot = sum(r["graphs"] for r in rows)
        agree = sum(r["agree"] for r in rows)
        have = sum(r["with_pm"] for r in rows)
        res = label(rf"{tot} random graphs, \ 40 to 100 vertices: \ {have} have a perfect matching; \ the "
                    rf"determinant agreed with Edmonds' algorithm on all {agree}", font_size=20, color=HEAD
                    ).to_edge(DOWN, buff=0.5)
        if res.width > 13:
            res.width = 13
        with self.voiceover(
            (
            f"A less obvious polynomial. <bookmark mark='a'/> Take a graph, and build its Tutte matrix: for each edge"
            f" i j, put a variable x i j above the diagonal and minus x i j below it. <bookmark mark='b'/> For this "
            f'graph the determinant is a perfect square. Inside that square, each of the two monomials corresponds to'
            f" a perfect matching, a set of edges that covers every vertex exactly once. <bookmark mark='c'/> William"
            f' Tutte proved in 1947 that the determinant is a nonzero polynomial exactly when the graph has a perfect'
            f" matching. But it can have exponentially many terms. <bookmark mark='d'/> László Lovász saw in 1979 "
            f'that we never need to expand it: substitute random numbers modulo a prime and compute one determinant '
            f"by elimination, Schwartz–Zippel bounding the error. <bookmark mark='e'/> We tried it on forty-eight "
            f'random graphs near the threshold where matchings appear. '
            f'{have}'
            f" had one, and the determinant agreed with Edmonds' blossom algorithm every time. Determinants "
            f'parallelize well, so this became the route to fast parallel matching algorithms.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(T))
            vo.wait_until("b")
            self.play(FadeIn(det), Create(pm))
            self.play(FadeOut(pm), Create(pm2))
            vo.wait_until("c")
            self.play(FadeIn(facts[0]))
            vo.wait_until("d")
            self.play(FadeIn(facts[1]))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    def fingerprint(self):
        d = load("pit")
        head = label(r"Fingerprints: \ are two files the same?", font_size=34).to_edge(UP, buff=0.35)
        alice = VGroup(Rectangle(width=2.6, height=1.5, stroke_color=DATA, fill_color=DATA, fill_opacity=0.1),
                       label(r"Alice: \ the novels", font_size=20, color=DATA),
                       label(rf"{d['bytes'] / 1e6:.0f} MB", font_size=18, color=GREY_A))
        alice[1].move_to(alice[0].get_center() + UP * 0.25)
        alice[2].move_to(alice[0].get_center() + DOWN * 0.3)
        bob = alice.copy()
        bob[0].set_stroke(LAM)
        bob[1].become(label(r"Bob: \ his copy", font_size=20, color=LAM).move_to(bob[1]))
        bob[2].become(label(r"one bit flipped", font_size=18, color=NO).move_to(bob[2]))
        VGroup(alice, bob).arrange(RIGHT, buff=5.0).shift(UP * 1.1)
        msg = VGroup(label(r"$p$, \ and $a \bmod p$", font_size=22, color=HEAD),
                     label(r"16 bytes", font_size=18, color=GREY_A)).arrange(DOWN, buff=0.1).move_to(UP * 1.4)
        arrow = Arrow(alice.get_right(), bob.get_left(), color=HEAD, buff=0.2).shift(UP * 0.0)
        res = VGroup(
            label(rf"$p$: \ fixed 61-bit prime, \ {d['fp_prime']:,}".replace(",", "{,}"), font_size=20,
                  color=GREY_A),
            label(rf"$a \bmod p = {d['fp_a']}$ \quad against \quad $b \bmod p = {d['fp_b']}$", font_size=20,
                  color=YES),
            label(rf"computing it: \ {d['fp_seconds']:.2f} s", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 0.5)
        why = VGroup(
            label(r"injective encoding: \ prepend byte 1; \ a collision needs $p\mid(a-b)$", font_size=20,
                  color=WHITE),
            MathTex(r"\Pr[\text{collision}]\le"
                    r"\frac{\lfloor L/60\rfloor}{\pi(2^{61})-\pi(2^{60})},\quad L=8\,\max(|A|,|B|)+1",
                    font_size=30, color=YES),
            label(rf"prime-count asymptotic estimate: \ {d['fp_false_estimate']:.2g}; \ not a certified finite bound",
                  font_size=19, color=HEAD),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            (
            "One more fingerprinting idea. <bookmark mark='a'/> Alice and Bob want to compare copies of the novel "
            "corpus without transmitting it all. <bookmark mark='b'/> Encode the byte string as a big-endian integer"
            ' with a leading one byte. The sentinel preserves leading zero bytes and makes the encoding injective. '
            'Alice sends a sixty-one-bit prime p and her residue in sixteen bytes; Bob compares his own residue. The'
            " displayed experiment uses one fixed prime. <bookmark mark='c'/> Our altered copy flips one bit. Both "
            'residues are checked against independent blockwise Horner evaluation; the displayed time is a local '
            "observation. <bookmark mark='d'/> Distinct encodings collide only when p divides their nonzero "
            'difference. For a uniformly sampled prime in the stated interval, count possible large prime divisors '
            'and divide by the number of eligible primes. The displayed prime-count approximation is an asymptotic '
            'heuristic, not a certified finite upper bound. Independent modulus choices multiply their actual '
            'collision probabilities. Part 21 develops rolling string fingerprints.'
        )
        ) as vo:
            self.play(FadeIn(head), FadeIn(alice), FadeIn(bob))
            vo.wait_until("a")
            self.play(Indicate(bob[2], color=NO))
            vo.wait_until("b")
            self.play(GrowArrow(arrow), FadeIn(msg))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in res], lag_ratio=0.3))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in why], lag_ratio=0.5), run_time=4.0)
        self.wait(0.3)
        self.clear_scene()
