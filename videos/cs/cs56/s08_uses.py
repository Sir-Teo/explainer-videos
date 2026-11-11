from __future__ import annotations

import math
import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs56.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, mono

# A toy Tanner graph: the twelve lines of the affine plane over Z_3 as bits, its nine points as checks (a bit is in
# the three checks on its line; two lines share at most one point).  Rows are checks.
TANNER = [[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
          [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
          [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0],
          [0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1],
          [0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1]]


def draw(pos, edges, center=ORIGIN, scale=1.0, r=0.1, color=WHITE, ecolor=GREY_C, sw=2.0):
    """A graph from vertex positions: VGroup(edges, dots) with .pts (scene coordinates)."""
    pts = [np.array(center) + scale * np.array([x, y, 0.0]) for x, y in pos]
    lines = VGroup(*[Line(pts[a], pts[b], color=ecolor, stroke_width=sw) for a, b in edges])
    dots = VGroup(*[Dot(p, radius=r, color=color) for p in pts])
    g = VGroup(lines, dots)
    g.pts = pts
    return g


def random_regular_edges(n, d, seed):
    """A random simple d-regular graph by pairing stubs, restarting on a loop or a repeated edge."""
    rng = random.Random(seed)
    while True:
        stubs = [v for v in range(n) for _ in range(d)]
        rng.shuffle(stubs)
        edges = set()
        ok = True
        for a, b in zip(stubs[::2], stubs[1::2]):
            if a == b or (min(a, b), max(a, b)) in edges:
                ok = False
                break
            edges.add((min(a, b), max(a, b)))
        if ok:
            return sorted(edges)


def ring(n, radius, start=math.pi / 2):
    return [(radius * math.cos(start - 2 * math.pi * k / n), radius * math.sin(start - 2 * math.pi * k / n))
            for k in range(n)]


def tanner(center, bit_dx=0.56, check_dx=0.72, height=1.9):
    """The toy Tanner graph: bits (circles) on top, checks (squares) below.  Returns (edges, bits, checks, pairs)."""
    H = np.array(TANNER)
    m, n = H.shape
    c = np.array(center, dtype=float)
    bp = [c + np.array([(i - (n - 1) / 2) * bit_dx, height / 2, 0]) for i in range(n)]
    cp = [c + np.array([(j - (m - 1) / 2) * check_dx, -height / 2, 0]) for j in range(m)]
    pairs = [(i, j) for j in range(m) for i in range(n) if H[j, i]]
    edges = VGroup(*[Line(bp[i], cp[j], color=GREY_D, stroke_width=1.6) for i, j in pairs])
    bits = VGroup(*[Circle(radius=0.15, stroke_color=GREY_A, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(p)
                    for p in bp])
    checks = VGroup(*[Square(side_length=0.3, stroke_color=GREY_A, stroke_width=2, fill_color=BG,
                             fill_opacity=1).move_to(p) for p in cp])
    return edges, bits, checks, pairs


def block(w, txt, col, h=0.42, size=17):
    r = Rectangle(width=w, height=h, stroke_color=col, stroke_width=1.5, fill_color=col, fill_opacity=0.25)
    g = VGroup(r)
    if txt:
        t = label(txt, font_size=size, color=col)
        if t.width < w - 0.05:
            g.add(t.move_to(r))
    return g


class Uses(VoiceoverScene):
    def construct(self):
        self.card()
        self.walk()
        self.hitting()
        self.savings()
        self.codes()
        self.decoding()
        self.dinur()
        self.practice()

    def card(self):
        card = chapter_card(7, r"Expanders at work", r"What can a graph that is impossible to cut do for us?",
                            lit=(1981, 1996), extra=((1981, r"Tanner: \ codes on graphs"),
                                                     (1996, r"Sipser and Spielman: \ expander codes")), part=PART)
        with self.voiceover("Chapter seven. Expanders at work: saving random bits, correcting errors, and proving "
                            "theorems."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ a walk instead of fresh coins
    def walk(self):
        head = label(r"Recycling random bits", font_size=36).to_edge(UP, buff=0.3)
        n = 16
        edges = random_regular_edges(n, 4, seed=2)
        center = LEFT * 4.4 + DOWN * 0.15
        g = draw(ring(n, 1.85), edges, center=center, r=0.11, sw=1.5, color=GREY_A)
        rng = random.Random(4)
        bad = set(rng.sample(range(n), n // 2))
        disc = VGroup(*[Circle(radius=0.2, stroke_width=0, fill_color=NO, fill_opacity=0.35).move_to(g.pts[v])
                        for v in sorted(bad)])
        bl = label(r"$B$: \ the bad strings", font_size=19, color=NO).next_to(g, DOWN, buff=0.3)
        nbr = {v: sorted({b for a, b in edges if a == v} | {a for a, b in edges if b == v}) for v in range(n)}
        path = [sorted(bad)[0]]
        for _ in range(6):
            path.append(rng.choice(nbr[path[-1]]))
        hits = sum(1 for v in path if v not in bad)
        walker = Dot(g.pts[path[0]], radius=0.14, color=HEAD)
        marks = VGroup(*[Circle(radius=0.2, stroke_color=HEAD, stroke_width=2.5).move_to(g.pts[v]) for v in path])
        cnt = label(rf"{len(path)} samples; \ {hits} outside $B$", font_size=19, color=HEAD).next_to(bl, DOWN,
                                                                                                    buff=0.12)
        setup = wrapped_label(r"an algorithm reads $r$ random bits and can be fooled only by strings in a bad set "
                              r"$B$, \ at most half of all $2^r$", 6.3, font_size=20, color=GREY_A)
        t1 = label(r"$t+1$ independent runs: \ $(t+1)\,r$ bits", font_size=20, color=NO)
        tape1 = VGroup(*[block(0.78, r"$r$", NO) for _ in range(7)]).arrange(RIGHT, buff=0.04)
        t2 = label(r"a walk on an expander of degree $D$: \ $r + t \log_2 D$ bits", font_size=20, color=YES)
        tape2 = VGroup(block(0.78, r"$r$", YES), *[block(0.2, "", YES) for _ in range(6)]).arrange(RIGHT, buff=0.04)
        right = VGroup(setup, t1, tape1, t2, tape2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right.move_to(RIGHT * 2.9 + UP * 0.35)
        ill = note(r"illustrative graph and walk", font_size=16).to_corner(DL, buff=0.2)
        with self.voiceover(
            "Parts 20 and 27 amplified randomized algorithms by rerunning them. <bookmark mark='a'/> Suppose an "
            "algorithm reads r random bits, and only a bad set, at most half of the strings, can fool it. <bookmark "
            "mark='b'/> Independent runs all fail with probability a half to the number of runs, but each run costs r"
            " new bits. <bookmark mark='c'/> Instead, put all two to the r strings on an explicit expander of "
            "constant degree. Pick a random start, then walk: <bookmark mark='d'/> each step costs only the logarithm"
            " of the degree. <bookmark mark='e'/> The samples are no longer independent. How likely is it that all "
            "land in B?"
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(setup), FadeIn(disc), FadeIn(bl))
            vo.wait_until("b")
            self.play(FadeIn(t1), LaggedStart(*[FadeIn(b) for b in tape1], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(t2), FadeIn(tape2[0]), FadeIn(walker), Create(marks[0]))
            vo.wait_until("d")
            for k, v in enumerate(path[1:], start=1):
                self.play(walker.animate.move_to(g.pts[v]), Create(marks[k]), FadeIn(tape2[k]), run_time=0.5)
            vo.wait_until("e")
            self.play(FadeIn(cnt))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the hitting bound
    def hitting(self):
        head = label(r"The hitting bound", font_size=36).to_edge(UP, buff=0.3)
        fs = 32
        steps = VGroup(
            cmath(r"\Pr[\text{all in } B]", r"=", r"\mathbf{1}^{\mathsf T} (PM)^t P\, u", font_size=fs),
            cmath(r"\|PMx\|", r"\le", r"\|P x_\parallel\|", r"+", r"\|M x_\perp\|", font_size=fs),
            cmath(r"\|PMx\|", r"\le", r"\mu\, \|x\|", r"+", r"\lambda\, \|x\|", font_size=fs),
            cmath(r"\Pr[\text{all in } B]", r"\le", r"\|P\mathbf{1}\|", r"\,(\mu + \lambda)^t\,", r"\|P u\|",
                  font_size=fs),
            cmath(r"\Pr[\text{all in } B]", r"\le", r"\mu", r"\,(\mu + \lambda)^t\,", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.55).to_edge(LEFT, buff=0.5).shift(DOWN * 0.2)
        steps[4][2:].set_color(YES)
        ww = 6.85 - (max(s.get_right()[0] for s in steps) + 0.45)
        whys = VGroup(
            wrapped_label(r"$u$: \ the uniform start; \ $M$: \ one step; \ $P$: \ keep only the mass on $B$, \ "
                          r"a fraction $\mu$ of the vertices", ww, font_size=20, color=GREY_B),
            wrapped_label(r"for $x$ living on $B$: \ split it along $\mathbf{1}$ and across; \ $M$ fixes the "
                          r"first part", ww, font_size=20, color=GREY_B),
            wrapped_label(r"Cauchy--Schwarz on $B$: \ $\langle \mathbf{1}, x\rangle \le \sqrt{\mu N}\,\|x\|$; "
                          r"\ $M$ shrinks the rest by $\lambda$", ww, font_size=20, color=GREY_B),
            wrapped_label(r"Cauchy--Schwarz once more, \ then the step $t$ times", ww, font_size=20, color=GREY_B),
            wrapped_label(r"$\|P\mathbf{1}\| = \sqrt{\mu N}$, \ $\|Pu\| = \sqrt{\mu N}/N$", ww, font_size=20,
                          color=GREY_B),
        )
        right = max(s.get_right()[0] for s in steps) + 0.45
        for w, s in zip(whys, steps):
            w.next_to([right, s.get_y(), 0], RIGHT, buff=0)
        punch = label(r"exponentially small in $t$, \ with $\lambda$ normalized by the degree; \ averages too: \ "
                      r"a Chernoff bound for expander walks \ (Gillman, \ 1998)", font_size=19,
                      color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Start uniform. Each step moves with the walk matrix M, then keeps only the mass on "
            "B, with the projection P; what is left is the chance that every sample was bad. <bookmark mark='b'/> "
            "Look at one step. Split a vector x living on B into its part along the all-ones vector and the rest; M "
            "leaves the first alone. <bookmark mark='c'/> The first is small because B is: Cauchy–Schwarz bounds it "
            "by mu times x. The rest shrinks by lambda. <bookmark mark='d'/> So each step costs a factor mu plus "
            "lambda, <bookmark mark='e'/> and all the samples land in B with probability at most mu times mu plus "
            "lambda to the t. Averages work too: David Gillman proved a Chernoff bound for such walks in 1998."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3], shift=DOWN * 0.1), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[3].copy(), steps[4]), FadeIn(whys[4]))
            self.play(FadeIn(punch))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ what it buys
    def savings(self):
        head = label(r"What the walk saves", font_size=36).to_edge(UP, buff=0.3)
        r, mu, lam, logd = 256, 0.5, 0.25, 10
        ks = (10, 20, 40)
        indep = [k * r for k in ks]
        walks = []
        for k in ks:
            t = math.ceil((k - 1) / math.log2(1 / (mu + lam)))   # mu (mu + lam)^t <= 2^-k
            walks.append((t, r + logd * t))
        vmax = max(indep)
        hscale = 4.2 / vmax
        base_y = -2.2
        bars = VGroup()
        for i, (k, a, (t, b)) in enumerate(zip(ks, indep, walks)):
            x = -4.6 + 2.0 * i
            ba = Rectangle(width=0.6, height=a * hscale, stroke_width=0, fill_color=NO, fill_opacity=0.85)
            ba.move_to([x - 0.33, base_y + a * hscale / 2, 0])
            bb = Rectangle(width=0.6, height=max(b * hscale, 0.03), stroke_width=0, fill_color=YES,
                           fill_opacity=0.85)
            bb.move_to([x + 0.33, base_y + b * hscale / 2, 0])
            la = label(rf"{a:,}", font_size=17, color=NO).next_to(ba, UP, buff=0.08)
            lb = label(rf"{b:,}", font_size=17, color=YES).next_to(bb, UP, buff=0.08)
            nm = label(rf"error $2^{{-{k}}}$", font_size=18, color=GREY_A).move_to([x, base_y - 0.3, 0])
            bars.add(VGroup(ba, bb, la, lb, nm))
        axis = Line([-5.6, base_y, 0], [-0.3, base_y, 0], color=GREY_C, stroke_width=1.5)
        yl = label(r"random bits needed", font_size=19, color=GREY_A).move_to([-3.2, 2.6, 0])
        key = VGroup(label(r"independent runs", font_size=19, color=NO),
                     label(r"one expander walk", font_size=19, color=YES)).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.1)
        key.next_to(yl, DOWN, buff=0.2)
        ex = MathTex(r"\tfrac12 \left(\tfrac12 + \tfrac14\right)^{t} \le 2^{-k}", font_size=32, color=YES)
        side = VGroup(
            wrapped_label(rf"illustrative: \ $r = {r}$ bits per run, \ bad set $\mu = \tfrac12$, \ an expander "
                          rf"with $\lambda \le \tfrac14$ and degree $2^{{{logd}}}$, \ so {logd} bits a step",
                          5.6, font_size=19, color=GREY_A),
            ex,
            wrapped_label(rf"error $2^{{-{ks[1]}}}$: \ {walks[1][0]} steps, \ {walks[1][1]:,} bits, \ against "
                          rf"{indep[1]:,} for {ks[1]} independent runs", 5.6, font_size=20, color=YES),
            wrapped_label(r"the walk's cost grows by a constant per halving of the error, \ not by $r$", 5.6,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.6 + DOWN * 0.1)
        with self.voiceover(
            "What does it buy? <bookmark mark='a'/> Take an illustrative algorithm with two hundred and fifty-six "
            "random bits and a bad half, and an expander with lambda a quarter and degree two to the ten: ten bits a "
            "step. <bookmark mark='b'/> Each step multiplies the failure bound by three quarters. <bookmark "
            "mark='c'/> For an error of two to the minus twenty, independent runs need five thousand one hundred and "
            "twenty bits; the walk needs forty-six steps, seven hundred and sixteen bits. <bookmark mark='d'/> The "
            "walk pays a constant for each halving of the error; fresh runs pay the full r."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(yl), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(ex))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(b[0], DOWN) for b in bars], *[GrowFromEdge(b[1], DOWN) for b in bars],
                      *[FadeIn(VGroup(b[2], b[3], b[4])) for b in bars], FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(bars[2][3], color=YES))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ expander codes: unique neighbours
    def codes(self):
        head = label(r"Expander codes: \ unique neighbours", font_size=36).to_edge(UP, buff=0.3)
        H = np.array(TANNER)
        edges, bits, checks, pairs = tanner(LEFT * 3.2 + UP * 1.35)
        bl = label(r"12 bits, \ each in 3 checks", font_size=18, color=GREY_A).next_to(bits, UP, buff=0.15)
        cl = label(r"9 parity checks", font_size=18, color=GREY_A).next_to(checks, DOWN, buff=0.15)
        S = [1, 2]
        c = 3
        hits = H[:, S].sum(axis=1)
        U = [j for j in range(len(H)) if hits[j] == 1]
        M = [j for j in range(len(H)) if hits[j] >= 2]
        sedges = [ln for ln, (i, j) in zip(edges, pairs) if i in S]
        counts = VGroup(
            label(rf"$S$: \ {len(S)} bits, \ $c\,|S| = {c * len(S)}$ edges", font_size=20, color=DATA),
            label(rf"unique neighbours $U$: \ {len(U)} checks", font_size=20, color=YES),
            label(rf"shared neighbours $M$: \ {len(M)} check", font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 4.6 + UP * 1.4)
        fs = 32
        steps = VGroup(
            cmath(r"c\,|S|", r"\ge", r"|U| + 2\,|M|", font_size=fs),
            cmath(r"|U| + |M|", r">", r"\tfrac34\, c\,|S|", font_size=fs),
            cmath(r"|U|", r">", r"\tfrac12\, c\,|S|", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=0.7).shift(DOWN * 1.75)
        steps[2].set_color(YES)
        whys = VGroup(
            label(r"count the edges out of $S$: \ one to each unique check, \ at least two to each shared one",
                  font_size=19, color=GREY_B),
            label(r"the graph expands: \ every set of at most $\alpha n$ bits reaches more than $\tfrac34 c|S|$ "
                  r"checks", font_size=19, color=GREY_B),
            label(r"subtract: \ more than half of $S$'s edges end at unique neighbours", font_size=19, color=YES),
        )
        for w, s in zip(whys, steps):
            w.next_to([-3.5, s.get_y(), 0], RIGHT, buff=0)
        dist = wrapped_label(r"a unique check sees exactly one 1 of a word living on $S$, \ so the word fails it: "
                             r"\ no codeword other than zero has $\alpha n$ or fewer ones", 12.6, font_size=20,
                             color=HEAD).to_edge(DOWN, buff=0.3)
        ill = note(r"illustrative code", font_size=16).next_to(checks, RIGHT, buff=0.3)
        with self.voiceover(
            "Part 28 drew parity-check codes as graphs of bits and checks, after Michael Tanner in 1981. <bookmark "
            "mark='a'/> Here is a toy: twelve bits, each in three checks. In 1996 Michael Sipser and Daniel Spielman "
            "asked what expansion buys. <bookmark mark='b'/> Take a small set S of bits. A check is a unique "
            "neighbour if exactly one edge from S reaches it. <bookmark mark='c'/> Each unique check takes one of S's"
            " edges, and each shared check at least two. <bookmark mark='d'/> If small sets reach more than three "
            "quarters of their edges' worth of checks, <bookmark mark='e'/> more than half of S's edges end at unique"
            " checks. <bookmark mark='f'/> So a nonzero word on a small set fails a check: it is not a codeword, and "
            "the distance is large."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(bits), FadeIn(checks), FadeIn(bl), FadeIn(cl),
                      FadeIn(ill))
            vo.wait_until("a")
            self.play(Indicate(bits, color=HEAD), Indicate(checks, color=HEAD))
            vo.wait_until("b")
            self.play(*[bits[i].animate.set_stroke(DATA, width=4).set_fill(DATA, opacity=0.6) for i in S],
                      *[ln.animate.set_stroke(DATA, width=3) for ln in sedges], FadeIn(counts[0]))
            self.play(*[checks[j].animate.set_stroke(YES, width=4).set_fill(YES, opacity=0.5) for j in U],
                      *[checks[j].animate.set_stroke(LAM, width=4).set_fill(LAM, opacity=0.5) for j in M],
                      FadeIn(counts[1]), FadeIn(counts[2]))
            vo.wait_until("c")
            self.play(Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(steps[1].copy(), steps[2]), FadeIn(whys[2]))
            vo.wait_until("f")
            self.play(FadeIn(dist))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ flip decoding
    def decoding(self):
        head = label(r"Decoding by flipping", font_size=36).to_edge(UP, buff=0.3)
        H = np.array(TANNER)
        m, n = H.shape
        edges, bits, checks, pairs = tanner(LEFT * 3.2 + UP * 1.35)
        word = np.zeros(n, dtype=int)
        errs = [1, 2]
        word[errs] = 1
        vals = VGroup(*[mono(str(int(v)), size=16, color=WHITE).move_to(b) for v, b in zip(word, bits)])

        def state(w):
            syn = H @ w % 2
            unsat = H.T @ syn
            return syn, unsat
        # the decoder: flip the bit with the most unsatisfied checks while that is more than half of its checks
        history = [word.copy()]
        flips = []
        w = word.copy()
        while True:
            syn, unsat = state(w)
            i = int(np.argmax(unsat))
            if syn.sum() == 0 or 2 * unsat[i] <= 3:
                break
            w[i] ^= 1
            flips.append(i)
            history.append(w.copy())

        def check_anims(w):
            syn, _ = state(w)
            return [ck.animate.set_stroke(NO if s else YES, width=4).set_fill(NO if s else YES, opacity=0.45)
                    for ck, s in zip(checks, syn)]

        def counter(w):
            syn, _ = state(w)
            return label(rf"unsatisfied checks: \ {int(syn.sum())}", font_size=22,
                         color=NO if syn.sum() else YES).move_to(RIGHT * 4.6 + UP * 1.9)
        cnt = counter(history[0])
        rule = wrapped_label(r"rule: \ flip a bit if more than half of its checks are unsatisfied", 4.0,
                             font_size=20, color=HEAD).next_to(cnt, DOWN, buff=0.3)
        rule.set_x(4.6)
        thm = VGroup(
            wrapped_label(r"Sipser and Spielman \ (1996): \ if every set of at most $\alpha n$ bits reaches more "
                          r"than $\tfrac34 c|S|$ checks, \ flipping corrects any $\alpha n / 2$ errors", 12.4,
                          font_size=21, color=YES),
            wrapped_label(r"why: \ the errors' unique checks are all unsatisfied, \ so some wrong bit has more than "
                          r"$c/2$ of them; \ every flip lowers the unsatisfied count, \ so there are at most $m$ "
                          r"flips: \ linear time", 12.4, font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(checks, DOWN, buff=1.0).to_edge(LEFT, buff=0.5)
        ill = note(r"the toy code; \ two errors, \ decoded by the rule", font_size=16).next_to(checks, RIGHT,
                                                                                             buff=0.3)
        with self.voiceover(
            "Expansion also gives a decoder. <bookmark mark='a'/> Send all zeros; two bits arrive flipped. <bookmark "
            "mark='b'/> Every check on an odd number of wrong bits is unsatisfied: four of them. <bookmark mark='c'/>"
            " The rule: flip any bit with more than half of its checks unsatisfied. <bookmark mark='d'/> The first "
            "wrong bit qualifies; flip it, and three unsatisfied checks remain. <bookmark mark='e'/> Now the second "
            "has all three of its checks unsatisfied; flip it, and every check is happy. <bookmark mark='f'/> On a "
            "good enough expander, Sipser and Spielman proved, this always works for errors up to a fixed fraction of"
            " the length: some wrong bit always qualifies, and each flip lowers the count: linear time."
        ) as vo:
            self.play(FadeIn(head), Create(edges), FadeIn(bits), FadeIn(checks), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(vals), *[bits[i].animate.set_stroke(NO, width=4) for i in errs])
            vo.wait_until("b")
            self.play(*check_anims(history[0]), FadeIn(cnt))
            vo.wait_until("c")
            self.play(FadeIn(rule))
            for k, i in enumerate(flips[:2]):
                vo.wait_until("de"[k])
                self.play(Indicate(bits[i], color=HEAD))
                self.play(Transform(vals[i], mono(str(int(history[k + 1][i])), size=16, color=WHITE).move_to(bits[i])),
                          bits[i].animate.set_stroke(YES, width=4), *check_anims(history[k + 1]),
                          Transform(cnt, counter(history[k + 1])))
            vo.wait_until("f")
            self.play(FadeIn(thm))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Dinur's gap amplification
    def dinur(self):
        head = label(r"The PCP theorem by gap amplification", font_size=36).to_edge(UP, buff=0.3)
        n = 8
        pos = ring(n, 1.45)
        edges = [(k, (k + 1) % n) for k in range(n)] + [(0, 4), (1, 5), (2, 6), (3, 7)]
        center = LEFT * 4.8 + UP * 0.55
        g = draw(pos, edges, center=center, r=0.15, sw=2)
        colours = [DATA, KERN, LAM, DATA, KERN, LAM, KERN, DATA]
        for dt, col in zip(g[1], colours):
            dt.set_color(col)
        bad = [k for k, (a, b) in enumerate(edges) if colours[a] == colours[b]]
        cap = label(rf"{len(bad)} of {len(edges)} constraints violated", font_size=19, color=NO).next_to(
            g, DOWN, buff=0.3)
        ill = note(r"illustrative: \ a 3-colouring as constraints", font_size=16).next_to(cap, DOWN, buff=0.1)
        names = [(r"make it an expander", r"gap $\div$ a constant", KERN),
                 (r"walks of length $t$", r"gap $\times$ a factor growing with $t$", YES),
                 (r"shrink the alphabet", r"gap $\div$ a constant", LAM)]
        boxes = VGroup()
        for nm, eff, col in names:
            b = RoundedRectangle(width=2.35, height=0.75, corner_radius=0.1, stroke_color=col, stroke_width=2,
                                 fill_color=BG, fill_opacity=1)
            t = label(nm, font_size=18, color=col).move_to(b)
            e = label(eff, font_size=17, color=GREY_A).next_to(b, DOWN, buff=0.1)
            boxes.add(VGroup(b, t, e))
        boxes.arrange(RIGHT, buff=0.35).move_to(RIGHT * 2.75 + UP * 2.2)
        arrows = VGroup(*[Arrow(boxes[k][0].get_right(), boxes[k + 1][0].get_left(), buff=0.05, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.3) for k in range(2)])
        fs = 30
        steps = VGroup(
            cmath(r"\mathrm{gap}_0", r"\ge", r"\tfrac{1}{m}", font_size=fs),
            cmath(r"\mathrm{gap}_{i+1}", r"\ge", r"\min(2\,\mathrm{gap}_i,\ \varepsilon_0)", font_size=fs),
            cmath(r"\mathrm{size}_{i+1}", r"\le", r"C \cdot \mathrm{size}_i", font_size=fs),
            cmath(r"\text{after } \log_2 m \text{ rounds:}", r"\quad", r"\mathrm{gap} \ge \varepsilon_0,",
                  r"\quad", r"\mathrm{size} \le m^{1 + \log_2 C}", font_size=fs),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(boxes, DOWN, buff=0.6).align_to(boxes, LEFT)
        steps[3].set_color(YES)
        whys = VGroup(
            label(r"unsatisfiable: \ at least one of $m$ constraints fails", font_size=18, color=GREY_B),
            label(r"one round of the three steps", font_size=18, color=GREY_B),
            label(r"each round grows the graph by a constant factor", font_size=18, color=GREY_B),
        )
        for w, s in zip(whys, steps[:3]):
            w.next_to(s, RIGHT, buff=0.4)
        why_exp = wrapped_label(r"on an expander a walk meets a set of bad edges nearly as often as independent "
                                r"samples would: \ the same fact as the hitting bound", 12.4, font_size=20,
                                color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Expanders also drive Irit Dinur's proof of the PCP theorem, from Part 27. <bookmark mark='a'/> Write a "
            "problem as constraints on a graph's edges, like a colouring. If it is unsatisfiable, at least one of the"
            " m constraints fails: a gap of one over m. <bookmark mark='b'/> Each round does three things: make the "
            "graph an expander, losing a constant factor; replace constraints by walks of length t, so the gap grows "
            "with t; and shrink the alphabet back, losing another constant. <bookmark mark='c'/> With t a large "
            "constant, each round at least doubles the gap, up to a ceiling, and grows the graph by a constant "
            "factor. <bookmark mark='d'/> After logarithmically many rounds the gap is constant and the size "
            "polynomial. <bookmark mark='e'/> Walks work because, on an expander, they meet bad edges about as often "
            "as independent samples."
        ) as vo:
            self.play(FadeIn(head), Create(g[0]), FadeIn(g[1]))
            vo.wait_until("a")
            self.play(*[g[0][k].animate.set_stroke(NO, width=5) for k in bad], FadeIn(cap), FadeIn(ill),
                      Write(steps[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.5), FadeIn(arrows), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(steps[1], shift=DOWN * 0.1), FadeIn(whys[1]))
            self.play(FadeIn(steps[2], shift=DOWN * 0.1), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(steps[3], shift=DOWN * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(why_exp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ in practice
    def practice(self):
        head = label(r"In practice: \ random wiring", font_size=36).to_edge(UP, buff=0.3)
        n = 12
        center = LEFT * 3.4 + DOWN * 0.2
        pos = ring(n, 2.2)
        edges = random_regular_edges(n, 3, seed=11)
        pts = [center + np.array([x, y, 0.0]) for x, y in pos]
        links = VGroup(*[Line(pts[a], pts[b], color=GREY_C, stroke_width=1.8) for a, b in edges])

        def switch(p, col=KERN):
            return RoundedRectangle(width=0.42, height=0.3, corner_radius=0.05, stroke_color=col, stroke_width=2,
                                    fill_color=BG, fill_opacity=1).move_to(p)
        sw = VGroup(*[switch(p) for p in pts])
        # Jellyfish's incremental growth: remove one link (a, b), wire both ends to the new switch
        a, b = edges[0]
        new_p = center + 0.45 * (pts[a] + pts[b] - 2 * center) / 2 + RIGHT * 0.0
        new_sw = switch(new_p, col=YES)
        old = links[0]
        l1 = Line(pts[a], new_p, color=YES, stroke_width=2.5)
        l2 = Line(pts[b], new_p, color=YES, stroke_width=2.5)
        reg = load("regular")["rows"][0]
        ill = note(r"illustrative: \ 12 switches, \ each with 3 links to others", font_size=16).to_corner(DL,
                                                                                                   buff=0.25)
        notes = VGroup(
            wrapped_label(r"Jellyfish \ (Singla, \ Hong, \ Popa and Godfrey, \ 2012): \ wire a data centre's "
                          r"top-of-rack switches as a random regular graph", 5.6, font_size=20, color=KERN),
            wrapped_label(rf"nearly Ramanujan: \ chapter 5's random 3-regular graph had "
                          rf"$\lambda = {reg['lambda']:.3f}$ against ${reg['ramanujan']:.3f}$; \ short paths, \ "
                          r"no bottleneck cut", 5.6, font_size=20, color=YES),
            wrapped_label(r"to grow, \ cut one link and wire both ends to the new switch", 5.6, font_size=20,
                          color=GREY_A),
            wrapped_label(r"Xpander \ (Valadarsky, \ Shahaf, \ Dinitz and Schapira, \ 2016): \ data-centre "
                          r"networks designed as expanders", 5.6, font_size=20, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 3.7 + DOWN * 0.1)
        with self.voiceover(
            "<bookmark mark='a'/> In 2012 Ankit Singla, Chi-Yao Hong, Lucian Popa and Brighten Godfrey proposed "
            "Jellyfish: wire a data centre's switches together at random. <bookmark mark='b'/> A random regular graph"
            " is nearly Ramanujan, as chapter five measured, so paths stay short and no cut is a bottleneck. "
            "<bookmark mark='c'/> And it grows gracefully: cut one link and wire both its ends to the new switch. "
            "<bookmark mark='d'/> Xpander, in 2016, designed such networks as expanders on purpose. Next, the "
            "Laplacian as a circuit."
        ) as vo:
            self.play(FadeIn(head), Create(links), FadeIn(sw), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), Indicate(links, color=YES))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), old.animate.set_stroke(NO, width=4))
            self.play(FadeOut(old), FadeIn(new_sw), Create(l1), Create(l2))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, LAM)
