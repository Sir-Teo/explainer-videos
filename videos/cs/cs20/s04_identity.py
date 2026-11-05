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
        with self.voiceover("Chapter three. Is this polynomial zero?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def lemma(self):
        head = label(r"The Schwartz--Zippel lemma", font_size=36).to_edge(UP, buff=0.35)
        stmt = MathTex(r"p \ne 0,\ \deg p = d,\quad r_1, \dots, r_n \in S \text{ at random}"
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
            "Freivalds' check is a special case of a more general fact. <bookmark mark='a'/> A polynomial that is "
            "not identically zero can't vanish at too many points: if p has degree d and each variable is chosen at "
            "random from a set S, p is zero there with probability at most d over the size of S. This is the "
            "Schwartz–Zippel lemma, found independently by Schwartz, Zippel, and DeMillo with Lipton, around 1980. "
            "<bookmark mark='b'/> With one variable, it is the fact that a degree-d polynomial has at most d roots. "
            "<bookmark mark='c'/> With more, write p as a polynomial in the first variable with top power k. Either "
            "its top coefficient vanishes, with probability at most d minus k over S by induction, or p becomes a "
            "nonzero polynomial of degree k in one variable, which vanishes with probability at most k over S. The "
            "two add up to d over S."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stmt))
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
            "Here is a claimed identity: the product x minus y, times y minus z, times z minus x, against an "
            "expansion. <bookmark mark='a'/> Instead of expanding, substitute random numbers and compare. We did "
            "this twenty thousand times for each size of S. <bookmark mark='b'/> The claim is false: one sign is "
            "wrong, so the two sides differ by two x z squared, a polynomial of degree three. It vanishes only when "
            "x or z is zero, which is why the agreement rates sit a little under the lemma's bound of three over S. "
            "With a thousand values, one test in five hundred is fooled; twenty tests are fooled with probability "
            "below ten to the minus fifty. <bookmark mark='c'/> The idea scales. The determinant of an eight by "
            "eight Vandermonde matrix equals a product of differences, a polynomial with forty thousand terms "
            "if you expand it. Evaluating both sides at fifty random points modulo a large prime took a "
            "fraction of a millisecond each, and they agreed every time."
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
            "A less obvious polynomial. <bookmark mark='a'/> Take a graph, and build its Tutte matrix: for each "
            "edge i j, put a variable x i j above the diagonal and minus x i j below it. <bookmark mark='b'/> For "
            "this graph the determinant is a perfect square, and each of its two terms is a perfect matching, a "
            "set of edges that covers every vertex exactly once. <bookmark mark='c'/> William Tutte proved in 1947 "
            "that the determinant is a nonzero polynomial exactly when the graph has a perfect matching. But it "
            "can have exponentially many terms. <bookmark mark='d'/> László Lovász saw in 1979 that we never need "
            "to expand it: substitute random numbers modulo a prime and compute one determinant by elimination, "
            "Schwartz–Zippel bounding the error. <bookmark mark='e'/> We tried it on forty-eight random graphs "
            f"near the threshold where matchings appear. {have} had one, and the determinant agreed with Edmonds' "
            "blossom algorithm every time. Determinants parallelize well, so this became the route to fast "
            "parallel matching algorithms."
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
            label(rf"$p$: \ a random 61-bit prime, \ {d['fp_prime']:,}".replace(",", "{,}"), font_size=20,
                  color=GREY_A),
            label(rf"$a \bmod p = {d['fp_a']}$ \quad against \quad $b \bmod p = {d['fp_b']}$", font_size=20,
                  color=YES),
            label(rf"computing it: \ {d['fp_seconds']:.2f} s", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 0.5)
        why = VGroup(
            label(r"a false match needs $p \mid (a - b)$, \ and $|a - b| < 2^{2 \times 10^8}$", font_size=20,
                  color=WHITE),
            label(rf"$a - b$ has at most $2 \times 10^8 / 60 \approx 3.3$ million prime factors above $2^{{60}}$; "
                  rf"\ there are $2.7 \times 10^{{16}}$ such primes", font_size=20, color=WHITE),
            MathTex(rf"\Pr[\text{{false match}}] \le 1.2 \times 10^{{-10}}", font_size=32, color=YES),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "One more use of the same idea. <bookmark mark='a'/> Alice has the novels, twenty-five megabytes, and "
            "Bob has a copy that may differ. Sending the whole file to compare is expensive. <bookmark mark='b'/> "
            "Instead, Alice treats her file as one enormous number a, picks a random sixty-one-bit prime p, and "
            "sends p and a modulo p: sixteen bytes. Bob compares with his own number modulo p. <bookmark mark='c'/> "
            "We flipped a single bit of Bob's copy. The two remainders differ completely, and computing one took "
            "about a seventh of a second. <bookmark mark='d'/> When could different files give the same "
            "remainder? Only if p divides their difference, a number with two hundred million bits. Such a number "
            "has at most a few million prime factors as large as p, out of tens of quadrillions of primes that "
            "size. So the chance of a false match is about one in ten billion, and a second prime squares it. "
            "Part 21 turns this into Rabin and Karp's string search, rolling the remainder along the text."
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
