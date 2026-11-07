from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs53.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, tag_box


def dot(a: int, b: int) -> int:
    """The inner product of two bit strings mod 2: AND, then parity."""
    return bin(a & b).count("1") % 2


def amp_row(values, width=0.3, gap=0.1, scale=1.6):
    """Signed amplitude bars on one baseline (y = 0), coloured by sign: blue for +, red for -.  Zero bars are kept
    (invisible) so that a row can be transformed into the next."""
    bars = VGroup()
    for i, a in enumerate(values):
        h = max(abs(a) * scale, 0.002)
        r = Rectangle(width=width, height=h, stroke_width=0, fill_color=DATA if a >= 0 else NO,
                      fill_opacity=0.85 if abs(a) > 1e-6 else 0.0)
        r.move_to([i * (width + gap), 0, 0], aligned_edge=DOWN if a >= 0 else UP)
        bars.add(r)
    base = Line([-width, 0, 0], [(len(values) - 1) * (width + gap) + width, 0, 0], color=GREY_C, stroke_width=1.5)
    return VGroup(base, bars)


def reg_wire(x0, x1, y, k, ket):
    """A register of k qubits drawn as one wire with a slash and its width."""
    w = Line([x0, y, 0], [x1, y, 0], color=GREY_B, stroke_width=2.4)
    sl = Line([x0 + 0.35 - 0.08, y - 0.14, 0], [x0 + 0.35 + 0.08, y + 0.14, 0], color=GREY_B, stroke_width=2)
    kt = label(f"{k}", font_size=16, color=GREY_B).next_to(sl, UP, buff=0.04)
    kl = MathTex(ket, font_size=28, color=GREY_A).next_to(w, LEFT, buff=0.1)
    return VGroup(w, sl, kt, kl)


def gate_box(tex, x, y, color=HEAD, w=0.85, h=0.6, size=26):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.2, fill_color=BG, fill_opacity=1).move_to(
        [x, y, 0])
    return VGroup(r, MathTex(tex, font_size=size, color=color).move_to(r))


def meter(x, y, color=KERN, size=0.55):
    r = Rectangle(width=size + 0.1, height=size, stroke_color=color, stroke_width=2, fill_color=BG,
                  fill_opacity=1).move_to([x, y, 0])
    arc = Arc(radius=0.17, start_angle=PI / 6, angle=2 * PI / 3, color=color, stroke_width=2).move_to([x, y - 0.03, 0])
    return VGroup(r, arc, Line([x, y - 0.12, 0], [x + 0.15, y + 0.13, 0], color=color, stroke_width=2))


class Simon(VoiceoverScene):
    def construct(self):
        self.card()
        self.bv()
        self.problem()
        self.circuit()
        self.solve()
        self.separation()

    def card(self):
        card = chapter_card(6, r"Bernstein--Vazirani and Simon", r"Can a quantum computer be exponentially faster?",
                            lit=(1993, 1994),
                            extra=((1993, r"Bernstein and Vazirani: \ quantum complexity theory"),
                                   (1994, r"Simon: \ an exponential separation")), part=PART)
        with self.voiceover("Chapter six. Bernstein–Vazirani and Simon. Can a quantum computer be exponentially "
                            "faster?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ Bernstein-Vazirani
    def bv(self):
        b = load("bv")
        n, s = b["n"], b["secret"]
        N = 2 ** n
        sbits = format(s, f"0{n}b")
        head = label(r"Bernstein--Vazirani: \ a hidden string", font_size=36).to_edge(UP, buff=0.3)
        stmt = label(r"$f(x) = s \cdot x \bmod 2$ \ for a hidden $n$-bit string $s$: \ find $s$", font_size=22,
                     color=WHITE).next_to(head, DOWN, buff=0.3)
        # classical: one bit per query
        ct = label(r"classically: \ one bit per query", font_size=20, color=GREY_A).move_to([-4.1, 1.85, 0])
        boxes = VGroup(*[VGroup(Square(side_length=0.55, stroke_color=GREY_B, stroke_width=1.8),
                                label(r"?", font_size=24, color=GREY_B)) for _ in range(n)]).arrange(RIGHT, buff=0.12)
        for bx in boxes:
            bx[1].move_to(bx[0])
        boxes.move_to([-4.1, 1.15, 0])
        reveal = VGroup(*[mono(c, size=22, color=HEAD).move_to(boxes[i][0]) for i, c in enumerate(sbits)])
        qs = VGroup()
        for i in range(n):
            e = format(1 << (n - 1 - i), f"0{n}b")
            qs.add(VGroup(mono(f"f({e})", size=18, color=DATA), mono(f"= {sbits[i]}", size=18, color=HEAD)).arrange(
                RIGHT, buff=0.15))
        qs.arrange(DOWN, aligned_edge=LEFT, buff=0.16).next_to(boxes, DOWN, buff=0.35)
        cnt = label(rf"{b['classical_queries']} queries for {n} bits: \ each answer is a single bit", font_size=19,
                    color=GREY_A).next_to(qs, DOWN, buff=0.3)
        cnt.set_x(-4.1)
        # quantum: the amplitudes
        qt = label(r"quantum: \ one query", font_size=20, color=GREY_A).move_to([3.6, 1.85, 0])
        uni = [1 / math.sqrt(N)] * N
        signed = [(-1) ** dot(x, s) / math.sqrt(N) for x in range(N)]
        final = [1.0 if x == b["measured"] else 0.0 for x in range(N)]
        anchor = np.array([1.05, -0.2, 0])
        rows_ = [amp_row(v, width=0.24, gap=0.1, scale=1.5).shift(anchor) for v in (uni, signed, final)]
        xs = [r.get_x() for r in rows_[0][1]]
        ticks = VGroup(*[mono(format(i, f"0{n}b"), size=16, color=HEAD if i == s else GREY_A).move_to(
            [xs[i], -0.75, 0]) for i in (0, s, N - 1)])
        caps = [label(t, font_size=18, color=GREY_B).move_to([3.6, -1.1, 0]) for t in
                (r"$H$ on every qubit", r"after the oracle: \ sign $(-1)^{s \cdot x}$", r"after $H$ again")]
        rows = VGroup(
            MathTex(r"\frac{1}{\sqrt N}\sum_x (-1)^{s \cdot x}|x\rangle", r"=", r"H^{\otimes n}|s\rangle", font_size=28),
            MathTex(r"H^{\otimes n}", r"H^{\otimes n}|s\rangle", r"=", r"|s\rangle", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, -2.15, 0])
        rows.shift(RIGHT * (-0.3 - rows.get_left()[0]))
        rows[1][3].set_color(HEAD)
        whys = VGroup(label(r"chapter 5's formula, \ backwards", font_size=18, color=GREY_B),
                      label(r"$H$ undoes itself", font_size=18, color=GREY_B))
        for wl, r in zip(whys, rows):
            wl.next_to(r, RIGHT, buff=0.3)
        res = label(rf"our simulator: \ measured \texttt{{{format(b['measured'], f'0{n}b')}}} with probability "
                    rf"{b['p']:.3f}", font_size=20, color=YES).to_edge(DOWN, buff=0.3).set_x(-3.4)
        div = DashedLine([-0.6, 2.1, 0], [-0.6, -2.7, 0], color=GREY_D, dash_length=0.08)
        with self.voiceover(
            "Ethan Bernstein and Umesh Vazirani, in 1993, hid a whole string in a function. <bookmark mark='a'/> "
            "The function takes x to the parity of the bits that x shares with a secret string s. "
            "<bookmark mark='b'/> Classically each query returns one bit, so the best you can do is ask about one "
            "position at a time: four queries for four bits, n for n. <bookmark mark='c'/> Quantumly, run the same "
            "circuit as Deutsch–Jozsa. The oracle stamps the sign minus one to the s dot x on every input. "
            "<bookmark mark='d'/> But that pattern of signs is exactly what Hadamards make from the string s, by "
            "chapter five's formula read backwards. <bookmark mark='e'/> Hadamard undoes itself, so the final "
            "Hadamards return s. <bookmark mark='f'/> Our simulator measures one zero one one, the secret, with probability one, from a "
            "single query."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stmt))
            vo.wait_until("b")
            self.play(FadeIn(ct), FadeIn(boxes), Create(div))
            for i in range(n):
                self.play(FadeIn(qs[i]), ReplacementTransform(boxes[i][1], reveal[i]), run_time=0.7)
            self.play(FadeIn(cnt))
            vo.wait_until("c")
            self.play(FadeIn(qt), FadeIn(rows_[0]), FadeIn(caps[0]), FadeIn(ticks))
            self.play(ReplacementTransform(rows_[0], rows_[1]), ReplacementTransform(caps[0], caps[1]))
            vo.wait_until("d")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("e")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            self.play(ReplacementTransform(rows_[1], rows_[2]), ReplacementTransform(caps[1], caps[2]))
            vo.wait_until("f")
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Simon's problem
    def problem(self):
        sm = load("simon")
        n, s = sm["n"], sm["secret"]
        N = 2 ** n
        head = label(r"Simon's problem", font_size=36).to_edge(UP, buff=0.3)
        stmt = label(r"$f$ is two-to-one: \ $f(x) = f(y)$ exactly when $y = x \oplus s$; \ find $s \ne 0$",
                     font_size=22).next_to(head, DOWN, buff=0.3)
        lab, f = {}, {}
        for x in range(N):                       # the same labelling as the instrument's oracle
            key = min(x, x ^ s)
            lab.setdefault(key, len(lab))
            f[x] = lab[key]
        cols = [DATA, LAM, KERN, YES]
        xs = [-5.25 + 1.5 * i for i in range(N)]
        ins = VGroup(*[tag_box(format(x, f"0{n}b"), color=GREY_A, size=18).move_to([xs[x], 1.45, 0])
                       for x in range(N)])
        outs = VGroup(*[tag_box(format(f[x], f"0{n}b"), color=cols[f[x]], size=18).move_to([xs[x], 0.45, 0])
                        for x in range(N)])
        arrows = VGroup(*[Arrow(ins[x].get_bottom(), outs[x].get_top(), buff=0.05, color=GREY_C, stroke_width=2,
                                max_tip_length_to_length_ratio=0.25) for x in range(N)])
        xl = label(r"$x$", font_size=22, color=GREY_A).next_to(ins, LEFT, buff=0.2)
        fl = label(r"$f(x)$", font_size=22, color=GREY_A).next_to(outs, LEFT, buff=0.2)
        arcs = VGroup()
        for x in range(N):
            if x < x ^ s:
                arcs.add(ArcBetweenPoints(outs[x].get_bottom() + DOWN * 0.04, outs[x ^ s].get_bottom() + DOWN * 0.04,
                                          angle=PI * 0.15, color=cols[f[x]], stroke_width=2.4))
        sl = label(rf"each colour is a pair $\{{x, \ x \oplus s\}}$; \ here $s = $ \texttt{{{format(s, f'0{n}b')}}} "
                   r"\ (hidden)", font_size=19, color=GREY_B).move_to([0, -0.75, 0])
        rows = VGroup(
            MathTex(r"q \text{ queries}:", r"\binom{q}{2} \text{ pairs},", r"\text{ each a collision w.p. }",
                    r"\frac{1}{2^n - 1}", font_size=28),
            MathTex(r"\mathbb{E}[\text{collisions}]", r"\approx", r"\frac{q^2}{2^{n+1}}", font_size=28),
            MathTex(r"q", r"\approx", r"2^{n/2}", r"\text{ before the first collision}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(sl, DOWN, buff=0.35)
        rows[2][2].set_color(NO)
        why = wrapped_label(r"Part 17's birthday bound; \ Simon proved that no classical algorithm, \ even a "
                            r"randomized one, \ does much better", 3.6, font_size=18, color=HEAD)
        why.next_to(rows, RIGHT, buff=0.4)
        if why.get_right()[0] > 6.85:
            VGroup(rows, why).shift(LEFT * (why.get_right()[0] - 6.85))
        with self.voiceover(
            "In 1994 Daniel Simon found a problem with an exponential gap. <bookmark mark='a'/> A function on n-bit "
            "strings is promised to be two-to-one in a special way: two inputs collide exactly when they differ by "
            "a hidden string s, under exclusive-or. Find s. <bookmark mark='b'/> Here are the eight inputs for three "
            "bits. Each colour is a pair, x and x exclusive-or s. <bookmark mark='c'/> Classically the only clue is a "
            "collision, two inputs with the same output; their exclusive-or is s. With q queries there are about q "
            "squared over two pairs, each a collision with probability one in two to the n minus one. "
            "<bookmark mark='d'/> So the first collision needs about two to the n over two queries. That is Part "
            "17's birthday bound, and Simon proved that no classical algorithm, even a randomized one, does much "
            "better."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stmt))
            vo.wait_until("b")
            self.play(FadeIn(ins), FadeIn(xl))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), FadeIn(outs), FadeIn(fl))
            self.play(Create(arcs), FadeIn(sl))
            vo.wait_until("c")
            self.play(Write(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]), FadeIn(why))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the circuit
    def circuit(self):
        sm = load("simon")
        n, s = sm["n"], sm["secret"]
        N = 2 ** n
        head = label(r"One run, \ one equation", font_size=36).to_edge(UP, buff=0.3)
        y1, y2 = 2.25, 1.25
        x0, x1 = -5.7, -0.9
        w1 = reg_wire(x0, x1, y1, n, r"|0\rangle^{\otimes n}")
        w2 = reg_wire(x0, x1, y2, n, r"|0\rangle^{\otimes n}")
        hb1 = gate_box(r"H^{\otimes n}", -4.55, y1)
        orc = Rectangle(width=0.9, height=y1 - y2 + 0.7, stroke_color=KERN, stroke_width=2.2, fill_color=BG,
                        fill_opacity=1).move_to([-3.3, (y1 + y2) / 2, 0])
        orc = VGroup(orc, MathTex(r"U_f", font_size=30, color=KERN).move_to(orc))
        hb2 = gate_box(r"H^{\otimes n}", -2.05, y1)
        m1, m2 = meter(-1.1, y1), meter(-1.1, y2)
        x0v = 1                                   # the example: the second register reads f(001)
        amps = [(-1) ** dot(x0v, y) * (1 + (-1) ** dot(s, y)) / math.sqrt(2 * N) for y in range(N)]
        bars = amp_row(amps, width=0.42, gap=0.2, scale=1.5).shift([0.9, 1.75, 0])
        bx = [b.get_x() for b in bars[1]]
        names = VGroup(*[mono(format(y, f"0{n}b"), size=16, color=YES if dot(s, y) == 0 else GREY_B).move_to(
            [bx[y], 0.8, 0]) for y in range(N)])
        bl = label(r"first register after the last $H$: \ amplitudes", font_size=18, color=GREY_B).next_to(
            bars, UP, buff=0.3)
        ill = note(rf"example: \ the second register read $f(\texttt{{{format(x0v, f'0{n}b')}}})$; \ "
                   rf"$s = $ \texttt{{{format(s, f'0{n}b')}}}", font_size=16).move_to([-3.3, 0.55, 0])
        rows = VGroup(
            MathTex(r"\frac{1}{\sqrt N}\sum_x |x\rangle|f(x)\rangle", font_size=28),
            MathTex(r"\text{second register reads } f(x_0):", r"\quad", r"\tfrac{1}{\sqrt2}\big(|x_0\rangle + "
                    r"|x_0 \oplus s\rangle\big)", font_size=28),
            MathTex(r"\xrightarrow{H^{\otimes n}}", r"\frac{1}{\sqrt{2N}}\sum_y", r"\big((-1)^{x_0 \cdot y} + "
                    r"(-1)^{(x_0 \oplus s) \cdot y}\big)", r"|y\rangle", font_size=28),
            MathTex(r"\text{only } y \text{ with }", r"y \cdot s = 0", r"\text{ survive}", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-0.6, -1.5, 0])
        rows.shift(RIGHT * (-6.3 - rows.get_left()[0]))
        r2b = MathTex(r"\xrightarrow{H^{\otimes n}}", r"\frac{1}{\sqrt{2N}}\sum_y", r"(-1)^{x_0 \cdot y}\big(1 + "
                      r"(-1)^{s \cdot y}\big)", r"|y\rangle", font_size=28)
        r2b.move_to(rows[2], aligned_edge=LEFT)
        rows[3][1].set_color(YES)
        whys = VGroup(label(r"one query, \ on all inputs at once", font_size=18, color=GREY_B),
                      label(r"the two inputs with that value", font_size=18, color=GREY_B),
                      label(r"$(x_0 \oplus s) \cdot y = x_0 \cdot y \oplus s \cdot y$", font_size=18, color=GREY_B),
                      label(r"$1 + (-1) = 0$ for the rest", font_size=18, color=HEAD))
        wx = 3.9
        for wl, r in zip(whys, rows):
            wl.move_to([max(wx, r.get_right()[0] + 0.3) + wl.width / 2, r.get_y(), 0])
        over = max(wl.get_right()[0] for wl in whys) - 6.85
        if over > 0:
            for wl in whys:
                wl.shift(LEFT * over)
        foot = label(r"reading the second register is optional: \ it only makes the picture simpler", font_size=18,
                     color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Simon's circuit has two registers. <bookmark mark='a'/> Hadamards spread the first over every input, "
            "and one query writes f of x into the second. <bookmark mark='b'/> Suppose the second register reads "
            "some value. Two inputs give that value, x nought and x nought exclusive-or s, so the first register is "
            "left in an equal superposition of exactly those two. <bookmark mark='c'/> Apply Hadamards again. Each "
            "output y receives two contributions, with signs that agree when y dot s is zero and are opposite when "
            "it is one. <bookmark mark='d'/> So every y with y dot s equal to one cancels. <bookmark mark='e'/> What "
            "survives, all with equal probability, are the y orthogonal to s. One run gives one random linear "
            "equation that s must satisfy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w1), FadeIn(w2))
            vo.wait_until("a")
            self.play(FadeIn(hb1), FadeIn(orc), Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(m2), FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(hb2), FadeIn(m1), FadeIn(rows[2]))
            self.play(TransformMatchingTex(rows[2], r2b), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            self.play(FadeIn(bl), FadeIn(bars), FadeIn(names), FadeIn(ill))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ solving
    def solve(self):
        sm = load("simon")
        n, s = sm["n"], sm["secret"]
        N = 2 ** n
        ys = sm["ys"]
        head = label(r"Solving for $s$", font_size=36).to_edge(UP, buff=0.3)
        runs = VGroup()
        for k, y in enumerate(ys):
            bits = format(y, f"0{n}b")
            terms = [f"s_{i}" for i in range(n) if bits[i] == "1"]
            eq = r" \oplus ".join(terms) + r" = 0"
            runs.add(VGroup(label(rf"run {k + 1}:", font_size=20, color=GREY_A),
                            tag_box(bits, color=DATA, size=20),
                            MathTex(r"\Rightarrow\;", eq, font_size=30, color=WHITE)).arrange(RIGHT, buff=0.3))
        runs.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.45).set_x(-3.2)
        rl = wrapped_label(r"each run yields a $y$ with $y \cdot s = 0$: \ one linear equation over the bits, \ "
                           r"arithmetic mod 2", 5.4, font_size=19, color=GREY_A).next_to(runs, RIGHT, buff=0.7)
        cands = VGroup(*[tag_box(format(c, f"0{n}b"), color=GREY_A, size=20, w=1.1) for c in range(1, N)])
        cands.arrange(RIGHT, buff=0.3).move_to([0, -0.25, 0])
        cl = label(r"every candidate $s \ne 0$", font_size=19, color=GREY_B).next_to(cands, UP, buff=0.2)
        crosses = []
        alive = set(range(1, N))
        for y in ys:
            out = [c for c in sorted(alive) if dot(c, y) == 1]
            crosses.append(VGroup(*[Cross(cands[c - 1], stroke_color=NO, stroke_width=4, scale_factor=0.7)
                                    for c in out]))
            alive -= set(out)
        winner = cands[sm["found"] - 1]
        ok = r"\ (it is the hidden $s$)" if sm["found"] == s and sm["dot_zero"] else ""
        res = label(rf"our simulator: \ $s = $ \texttt{{{format(sm['found'], f'0{n}b')}}} after {sm['runs']} runs "
                    + ok, font_size=21, color=YES).next_to(cands, DOWN, buff=0.45)
        notes = VGroup(
            wrapped_label(r"in general: \ $n - 1$ independent equations pin down $s$; \ each run adds a new one with "
                          r"probability at least $\tfrac12$, \ so on average a little over $n$ runs suffice", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"then Gaussian elimination mod 2: \ $O(n^3)$ classical steps; \ in all, \ polynomial in "
                          r"$n$ against the classical $2^{n/2}$", 12.4, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Now collect equations. <bookmark mark='a'/> Our simulator's first run gave one one zero: so the first "
            "two bits of s are equal. The second gave nought nought one: the last bit of s is zero. "
            "<bookmark mark='b'/> Watch the candidates. Seven nonzero strings could be s. The first equation rules "
            "out four of them, the second rules out two more. <bookmark mark='c'/> One is left, one one zero, and it "
            "is the hidden string. <bookmark mark='d'/> In general n minus one independent equations determine s. "
            "Each run gives a new independent equation with probability at least a half, and on average a little "
            "over n runs are enough, <bookmark mark='e'/> and Gaussian elimination, modulo two, finishes the job: "
            "polynomial in n, against the classical two to the n over two."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(runs[0]), FadeIn(rl))
            self.play(FadeIn(runs[1]))
            vo.wait_until("b")
            self.play(FadeIn(cands), FadeIn(cl))
            for cr in crosses:
                self.play(Create(cr), run_time=1.0)
                self.wait(0.3)
            vo.wait_until("c")
            self.play(winner[0].animate.set_stroke(YES), winner[1].animate.set_color(YES), Circumscribe(winner, color=YES),
                      FadeIn(res))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ separation, and Shor
    def separation(self):
        head = label(r"An oracle separation, \ and the seed of Shor", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 64, 16], y_range=[0, 10, 3], x_length=4.2, y_length=3.2,
                  axis_config={"color": GREY_D, "include_numbers": False, "include_ticks": True})
        ax.move_to([-4.2, 0.2, 0])
        xt = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (16, 32, 48, 64)])
        yt = VGroup(*[MathTex(rf"10^{{{v}}}", font_size=20, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (3, 6, 9)])
        xl = label(r"$n$ \ (bits)", font_size=18, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = label(r"queries \ (log scale)", font_size=18, color=GREY_B).next_to(ax, UP, buff=0.15).align_to(ax, LEFT)
        cl = ax.plot(lambda v: v / 2 * math.log10(2), x_range=[1, 64], color=NO, stroke_width=3)
        ql = ax.plot(lambda v: math.log10(v), x_range=[1, 64], color=YES, stroke_width=3)
        cll = label(r"classical: \ $2^{n/2}$", font_size=19, color=NO).next_to(ax.c2p(64, 64 / 2 * math.log10(2)),
                                                                             UP, buff=0.1).shift(LEFT * 0.6)
        qll = label(r"Simon: \ about $n$", font_size=19, color=YES).next_to(ax.c2p(64, math.log10(64)), UP,
                                                                         buff=0.15).shift(LEFT * 0.6)
        sh = note(r"the shapes of the two bounds; \ constants omitted", font_size=16).next_to(xl, DOWN, buff=0.1)
        tab = grid_table(
            [r"", r"Simon", r"Shor \ (chapter 9)"],
            [[r"promise", r"$f(x) = f(x \oplus s)$", r"$f(x) = f(x + r)$"],
             [r"group", r"bit strings, \ XOR", r"integers, \ addition"],
             [r"transform", r"$H^{\otimes n}$", r"the QFT \ (chapter 7)"],
             [r"one run gives", r"$y$ with $y \cdot s = 0$", r"$y \approx k \cdot 2^t / r$"],
             [r"classical finish", r"elimination mod 2", r"continued fractions"]],
            widths=[1.9, 2.5, 2.6], row_h=0.52, font_size=19, mono_cols=())
        tab.move_to([3.15, 0.55, 0])
        for r in range(1, 6):
            tab.cells[r][0].set_color(GREY_A)
            tab.cells[r][1].set_color(DATA)
            tab.cells[r][2].set_color(LAM)
        foot = VGroup(
            wrapped_label(r"both find a hidden period of a function on a group: \ the \textbf{hidden subgroup "
                          r"problem}, \ solved efficiently for abelian groups by the same recipe", 12.4, font_size=19,
                          color=WHITE),
            wrapped_label(r"the separation is relative to an oracle, \ a black box: \ it does not prove that quantum "
                          r"computers beat classical ones on problems with no box \ (chapter 11)", 12.4,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Simon's result was the first exponential separation between quantum and randomized classical "
            "computation. <bookmark mark='a'/> On a logarithmic scale the gap is plain: the classical cost is two to "
            "the n over two, a straight line climbing steeply, while the quantum cost grows like n. "
            "<bookmark mark='b'/> And Simon's algorithm has exactly the shape of the one Peter Shor published the same "
            "year. Replace exclusive-or by ordinary addition, and the hidden string by a hidden period r; replace "
            "the Hadamards by the quantum Fourier transform, and linear algebra by continued fractions. "
            "<bookmark mark='c'/> Both find a hidden period of a function on a group, and the same recipe solves that "
            "for every abelian group. <bookmark mark='d'/> One caution. The separation is relative to a black box. "
            "It does not prove that quantum computers beat classical ones on any problem stated without one, as "
            "chapter eleven explains."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(sh))
            self.play(Create(cl), Create(ql), FadeIn(cll), FadeIn(qll), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(tab.cells[0][0]), FadeIn(tab.cells[0][1]), FadeIn(tab.cells[0][2]), Create(tab.rule))
            for r in range(1, 6):
                self.play(*[FadeIn(c) for c in tab.cells[r]], run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM, NO, YES, BG, DATA, HEAD)
