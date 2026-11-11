from __future__ import annotations

import random

from explainer.cs import *  # noqa: F403
from videos.cs.cs60.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load, module_box, mono

_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
        "seventeen eighteen nineteen".split()

# Illustrative operands (labelled on screen): a pruned weight vector and its inputs.
W_SPARSE = [0, 3, 0, 0, -2, 0, 0, 0, 1, 0, 0, 0, 0, 2, 0, -1]
X_IN = [2, 1, 4, 3, 1, 5, 2, 6, 3, 1, 2, 4, 7, 1, 3, 2]
# A small sparse matrix for the compressed format (illustrative).
M_SPARSE = [[0, 5, 0, 0, 2, 0], [3, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0], [0, 1, 0, 0, 0, 4]]
# Sixteen trained-looking weights for 2:4 pruning (illustrative).
W_24 = [0.8, -0.1, 0.05, -1.3, 0.2, 0.9, -0.6, 0.1, -0.05, 0.3, 1.1, -0.2, 0.7, 0.0, -0.4, 0.15]
SR_STEP, SR_STEPS, SR_SEED = 0.25, 24, 3     # the rounding demo: 24 updates of a quarter step, one random run


def box_num(v, color, size=0.62, fs=22, dim=False):
    sq = Square(size, stroke_color=GREY_D if dim else color, stroke_width=2, fill_color=BG, fill_opacity=1)
    t = label(rf"${v}$", font_size=fs, color=GREY_D if dim else color).move_to(sq)
    return VGroup(sq, t)


class Sparsity(VoiceoverScene):
    def construct(self):
        self.card()
        self.skip()
        self.formats()
        self.structured()
        self.rounding()
        self.drift()
        self.approximate()

    def card(self):
        card = chapter_card(9, r"Sparsity and approximation", r"What if most numbers are zero, \ or need not be "
                            r"exact?", lit=(2015, 2016, 2020),
                            extra=((2015, r"Gupta et al.: \ stochastic rounding"),
                                   (2016, r"Han et al.: \ EIE, \ a sparse engine"),
                                   (2020, r"NVIDIA A100: \ 2:4 sparsity")), part=PART)
        with self.voiceover("Chapter nine. Sparsity and approximation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def skip(self):
        head = label(r"Zero times anything is zero", font_size=36).to_edge(UP, buff=0.3)
        n = len(W_SPARSE)
        ws = VGroup(*[box_num(v, LAM, dim=(v == 0)) for v in W_SPARSE]).arrange(RIGHT, buff=0.12)
        xs = VGroup(*[box_num(v, DATA) for v in X_IN]).arrange(RIGHT, buff=0.12)
        prods = VGroup(*[box_num(w * x, HEAD) for w, x in zip(W_SPARSE, X_IN)]).arrange(RIGHT, buff=0.12)
        VGroup(ws, xs, prods).arrange(DOWN, buff=0.42).next_to(head, DOWN, buff=0.7).shift(RIGHT * 0.4)
        names = VGroup(label(r"$w$", font_size=24, color=LAM).next_to(ws, LEFT, buff=0.2),
                       label(r"$x$", font_size=24, color=DATA).next_to(xs, LEFT, buff=0.2),
                       label(r"$w\,x$", font_size=24, color=HEAD).next_to(prods, LEFT, buff=0.2))
        nz = [k for k in range(n) if W_SPARSE[k]]
        total = sum(w * x for w, x in zip(W_SPARSE, X_IN))
        dense = label(rf"dense: \ {n} multiplies, \ {n - len(nz)} of them by zero", font_size=22, color=NO)
        dense.next_to(prods, DOWN, buff=0.5).align_to(prods, LEFT)
        pairs = VGroup(*[tag_pair(W_SPARSE[k], X_IN[k]) for k in nz]).arrange(RIGHT, buff=0.18)
        res = label(rf"$= {total}$", font_size=26, color=WHITE)
        packed = VGroup(pairs, res).arrange(RIGHT, buff=0.3)
        packed.next_to(dense, DOWN, buff=0.6).align_to(prods, LEFT)
        sparse = label(rf"skipped: \ {len(nz)} multiplies, \ same answer", font_size=22, color=YES)
        sparse.next_to(packed, RIGHT, buff=0.5)
        gate = label(r"gating: \ a zero holds the multiplier still \ (energy saved, \ not time)", font_size=19,
                     color=GREY_A).next_to(dense, RIGHT, buff=0.5)
        foot = wrapped_label(r"pruning: \ Han, \ Pool, \ Tran and Dally \ (2015) \ removed about 9 in 10 of AlexNet's "
                             r"weights without losing accuracy; \ ReLU zeros many inputs", 12.6,
                             font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        ill = note(r"illustrative values", font_size=16).next_to(foot, UP, buff=0.15).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "A trained network is full of zeros. <bookmark mark='a'/> Here is one row of weights after pruning, "
            "and the inputs it meets. <bookmark mark='b'/> A dense engine multiplies every pair: sixteen "
            "multiplies, eleven of them by zero. <bookmark mark='c'/> The cheap fix is to notice a zero and hold "
            "the multiplier still, which saves energy but not time. <bookmark mark='d'/> The better fix is to "
            "skip: feed only the five pairs that matter, and get the same sum in five steps. <bookmark mark='e'/>"
            " The zeros are real. In 2015 Song Han and colleagues pruned nine in ten of AlexNet's weights without"
            " losing accuracy, and then built an engine, EIE, to run such networks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(ws), FadeIn(xs), FadeIn(names[:2]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p, shift=DOWN * 0.15) for p in prods], lag_ratio=0.08), FadeIn(names[2]),
                      run_time=1.6)
            self.play(FadeIn(dense))
            vo.wait_until("c")
            zeros = [k for k in range(n) if not W_SPARSE[k]]
            self.play(*[prods[k].animate.set_opacity(0.25) for k in zeros], *[xs[k].animate.set_opacity(0.35)
                                                                             for k in zeros], FadeIn(gate))
            vo.wait_until("d")
            self.play(*[TransformFromCopy(VGroup(ws[k], xs[k]), pairs[i]) for i, k in enumerate(nz)], run_time=1.4)
            self.play(FadeIn(res), FadeIn(sparse))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def formats(self):
        head = label(r"Storing only what is there", font_size=36).to_edge(UP, buff=0.3)
        m, n = len(M_SPARSE), len(M_SPARSE[0])
        cells = VGroup(*[box_num(v, HEAD if v else GREY_D, size=0.56, fs=20, dim=not v) for row in M_SPARSE
                         for v in row]).arrange_in_grid(m, n, buff=0.06)
        cells.to_edge(LEFT, buff=0.8).shift(UP * 1.1)
        cl = VGroup(*[label(f"{j}", font_size=16, color=GREY_B).next_to(cells[j], UP, buff=0.08) for j in range(n)])
        rl = VGroup(*[label(f"{i}", font_size=16, color=GREY_B).next_to(cells[i * n], LEFT, buff=0.1)
                      for i in range(m)])
        vals = [v for row in M_SPARSE for v in row if v]
        cols = [j for row in M_SPARSE for j, v in enumerate(row) if v]
        ptr = [0]
        for row in M_SPARSE:
            ptr.append(ptr[-1] + sum(1 for v in row if v))

        def strip(items, color):
            return VGroup(*[box_num(v, color, size=0.5, fs=19) for v in items]).arrange(RIGHT, buff=0.06)
        sv, sc, sp = strip(vals, HEAD), strip(cols, DATA), strip(ptr, KERN)
        VGroup(sv, sc, sp).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([2.6, 1.5, 0])
        an = VGroup(label(r"values", font_size=19, color=HEAD).next_to(sv, LEFT, buff=0.2),
                    label(r"columns", font_size=19, color=DATA).next_to(sc, LEFT, buff=0.2),
                    label(r"row starts", font_size=19, color=KERN).next_to(sp, LEFT, buff=0.2))
        nnz = len(vals)
        b, c = 1, 2
        dense_b, csr_b = m * n * b, nnz * (b + c) + (m + 1) * c
        sizes = VGroup(label(rf"dense, \ 8-bit: \ {dense_b} bytes", font_size=20, color=GREY_A),
                       label(rf"compressed rows, \ 16-bit indices: \ {csr_b} bytes", font_size=20, color=NO)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(cells, DOWN, buff=0.35).align_to(rl, LEFT)
        rows = VGroup(
            MathTex(r"\text{dense}", r"=", r"m\,n\,b", font_size=32),
            MathTex(r"\text{compressed}", r"=", r"z\,(b + c)", r"+", r"(m+1)\,c", font_size=32),
            MathTex(r"z\,(b + c)", r"<", r"m\,n\,b", font_size=32),
            MathTex(r"\frac{z}{m\,n}", r"<", r"\frac{b}{b + c}", font_size=32),
            MathTex(r"\frac{z}{m\,n}", r"<", r"\frac{1}{1 + 2}", r"=", r"\frac13", font_size=32),
        )
        rows[:2].arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows[2:].arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows[:2].next_to(sizes, DOWN, buff=0.45).align_to(rl, LEFT)
        rows[2:].next_to([-0.5, -1.75, 0], RIGHT, buff=0)
        rows[4][-1].set_color(HEAD)
        whys = VGroup(label(r"$z$ nonzeros, \ $b$ bytes a value, \ $c$ bytes an index", font_size=18, color=GREY_B)
                      .next_to(rows[1], DOWN, buff=0.15).align_to(rows[1], LEFT),
                      label(r"ignoring the row starts", font_size=18, color=GREY_B).next_to(rows[2], RIGHT, buff=0.3),
                      label(r"the density must be below", font_size=18, color=GREY_B).next_to(rows[3], RIGHT, buff=0.3),
                      label(r"8-bit values, \ 16-bit indices", font_size=18, color=HEAD).next_to(rows[4], RIGHT,
                                                                                                 buff=0.3))
        ill = note(r"illustrative matrix", font_size=16).to_corner(DR, buff=0.2)
        with self.voiceover(
            "To skip zeros, the hardware must not store them. <bookmark mark='a'/> The commonest format is "
            "compressed sparse rows: the nonzero values, row by row; <bookmark mark='b'/> beside each, its "
            "column; <bookmark mark='c'/> and where each row starts. <bookmark mark='d'/> But indices cost bytes "
            "too. Here the dense matrix takes twenty-four bytes, the compressed one twenty-eight. "
            "<bookmark mark='e'/> With z nonzeros, compression wins only if z times b plus c is less than m n b: "
            "the density must be below b over b plus c. <bookmark mark='f'/> For eight-bit values and sixteen-bit"
            " indices, below a third. And every lookup by column is a read from a scattered address."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cells), FadeIn(cl), FadeIn(rl), FadeIn(ill))
            vo.wait_until("a")
            nzc = [cells[i * n + j] for i in range(m) for j in range(n) if M_SPARSE[i][j]]
            self.play(*[TransformFromCopy(c_, s_) for c_, s_ in zip(nzc, sv)], FadeIn(an[0]), run_time=1.2)
            vo.wait_until("b")
            self.play(*[TransformFromCopy(cl[j], s_) for j, s_ in zip(cols, sc)], FadeIn(an[1]), run_time=1.2)
            vo.wait_until("c")
            self.play(FadeIn(sp, shift=RIGHT * 0.2), FadeIn(an[2]))
            vo.wait_until("d")
            self.play(FadeIn(sizes))
            self.play(Write(rows[0]))
            self.play(FadeIn(rows[1], shift=DOWN * 0.2), FadeIn(whys[0]))
            vo.wait_until("e")
            self.play(Write(rows[2]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[2]))
            vo.wait_until("f")
            self.play(TransformMatchingTex(rows[3].copy(), rows[4]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def structured(self):
        head = label(r"Structured sparsity: \ two in every four", font_size=36).to_edge(UP, buff=0.3)
        keep = []
        for g in range(4):
            grp = W_24[4 * g:4 * g + 4]
            best = sorted(range(4), key=lambda k: -abs(grp[k]))[:2]
            keep.append(sorted(best))

        def wbox(v, dim=False, w=0.66):
            r = Rectangle(width=w, height=0.5, stroke_color=GREY_D if dim else LAM, stroke_width=2, fill_color=BG,
                          fill_opacity=1)
            return VGroup(r, label(rf"${v:g}$", font_size=19, color=GREY_D if dim else LAM).move_to(r))
        groups = VGroup(*[VGroup(*[wbox(W_24[4 * g + k]) for k in range(4)]).arrange(RIGHT, buff=0.05)
                          for g in range(4)]).arrange(RIGHT, buff=0.35).next_to(head, DOWN, buff=0.6)
        pruned = VGroup(*[VGroup(*[wbox(W_24[4 * g + k] if k in keep[g] else 0, dim=k not in keep[g])
                                   for k in range(4)]).arrange(RIGHT, buff=0.05) for g in range(4)])
        for p, g in zip(pruned, groups):
            p.move_to(g)
        braces = VGroup(*[Brace(g, UP, buff=0.05, color=GREY_C) for g in groups])
        gl = label(r"groups of four: \ keep the two largest, \ zero the rest", font_size=19, color=GREY_A)
        gl.next_to(braces, UP, buff=0.05)
        kv = VGroup(*[wbox(W_24[4 * g + k], w=0.66) for g in range(4) for k in keep[g]]).arrange(RIGHT, buff=0.05)
        ki = VGroup(*[VGroup(Rectangle(width=0.66, height=0.42, stroke_color=KERN, stroke_width=1.5),
                             mono(f"{k:02b}", size=16, color=KERN)) for g in range(4) for k in keep[g]])
        for b_ in ki:
            b_[1].move_to(b_[0])
        ki.arrange(RIGHT, buff=0.05)
        VGroup(kv, ki).arrange(DOWN, buff=0.08).next_to(groups, DOWN, buff=0.55).align_to(groups, LEFT)
        cn = VGroup(label(r"8 values", font_size=18, color=LAM).next_to(kv, RIGHT, buff=0.2),
                    label(r"8 two-bit positions", font_size=18, color=KERN).next_to(ki, RIGHT, buff=0.2))
        # the hardware for group 0: two 4-to-1 selectors pick the matching inputs
        xs = VGroup(*[box_num(rf"x_{k}", DATA, size=0.55, fs=20) for k in range(4)]).arrange(RIGHT, buff=0.1)
        xs.move_to([-4.6, -0.35, 0])

        def mux(sel):
            p = Polygon([-0.45, 0.25, 0], [0.45, 0.25, 0], [0.25, -0.25, 0], [-0.25, -0.25, 0], color=KERN,
                        stroke_width=2, fill_color=KERN, fill_opacity=0.15)
            return VGroup(p, mono(sel, size=14, color=KERN).move_to(p))
        m0, m1 = mux(f"{keep[0][0]:02b}"), mux(f"{keep[0][1]:02b}")
        VGroup(m0, m1).arrange(RIGHT, buff=0.7).next_to(xs, DOWN, buff=0.45)
        mul = VGroup(*[module_box(rf"$\times\,{W_24[k]:g}$", HEAD, w=1.0, h=0.42, font=17) for k in keep[0]])
        for mm, mx in zip(mul, (m0, m1)):
            mm.next_to(mx, DOWN, buff=0.3)
        add = module_box(r"$+$", YES, w=0.6, h=0.42, font=20).next_to(mul, DOWN, buff=0.35)
        wires = VGroup(*[Line(xs[k].get_bottom(), m.get_top(), color=DATA, stroke_width=1.2, stroke_opacity=0.5)
                         for m in (m0, m1) for k in range(4)],
                       *[Line(m.get_bottom(), mm.get_top(), color=KERN, stroke_width=2)
                         for m, mm in zip((m0, m1), mul)],
                       Line(mul[0].get_bottom(), add.get_top(), color=YES, stroke_width=2),
                       Line(mul[1].get_bottom(), add.get_top(), color=YES, stroke_width=2))
        hw = VGroup(xs, m0, m1, mul, add, wires)
        rows = VGroup(
            MathTex(r"\text{dense: }", r"4 \times 8", r"=", r"32 \text{ bits}", font_size=30),
            MathTex(r"\text{2:4: }", r"2 \times 8 + 2 \times 2", r"=", r"20 \text{ bits}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.6, -1.4, 0])
        rows[1][-1].set_color(YES)
        facts = VGroup(label(r"half the multiplies, \ every time: \ no irregular gathers", font_size=19, color=YES),
                       label(r"NVIDIA A100 \ (2020): \ up to twice the tensor-core rate; \ the network is "
                             r"retrained after pruning", font_size=18, color=GREY_A)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(rows, DOWN, buff=0.35).align_to(rows,
                                                                                                           LEFT)
        if facts.get_right()[0] > 6.8:
            facts.shift(LEFT * (facts.get_right()[0] - 6.8))
        ill = note(r"illustrative weights", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Arbitrary zeros make the work unpredictable, so in 2020 NVIDIA's A100 asked for a pattern. "
            "<bookmark mark='a'/> Cut the weights into groups of four, <bookmark mark='b'/> and in each group "
            "keep the two largest and zero the rest. <bookmark mark='c'/> Store the eight survivors, each with a "
            "two-bit position in its group. <bookmark mark='d'/> In hardware, each position drives a selector "
            "that picks the matching input, so two multipliers do the work of four. <bookmark mark='e'/> Exactly "
            "half the multiplies, every time, and thirty-two bits a group become twenty. The network is retrained"
            " after pruning to recover its accuracy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(groups), FadeIn(braces), FadeIn(gl))
            vo.wait_until("b")
            self.play(*[Transform(g, p) for g, p in zip(groups, pruned)], run_time=1.2)
            vo.wait_until("c")
            src = VGroup(*[groups[g][k] for g in range(4) for k in keep[g]])
            self.play(TransformFromCopy(src, kv), run_time=1.2)
            self.play(FadeIn(ki, shift=DOWN * 0.1), FadeIn(cn))
            vo.wait_until("d")
            self.play(FadeIn(xs), Create(wires[:8]), FadeIn(m0), FadeIn(m1))
            self.play(Create(wires[8:]), FadeIn(mul), FadeIn(add))
            self.play(Indicate(VGroup(xs[keep[0][0]], xs[keep[0][1]]), color=HEAD), Indicate(ki[:2], color=KERN))
            vo.wait_until("e")
            self.play(Write(rows[0]))
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            self.play(FadeIn(facts))
        _ = hw
        self.wait(0.4)
        self.clear_scene()

    def rounding(self):
        head = label(r"Stochastic rounding: \ right on average", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"x", r"=", r"L", r"+", r"p\,\Delta", r",\quad 0 \le p < 1", font_size=34),
            MathTex(r"\mathbb{E}[\operatorname{r}(x)]", r"=", r"(1-p)\,L", r"+", r"p\,(L + \Delta)", font_size=34),
            MathTex(r"\mathbb{E}[\operatorname{r}(x)]", r"=", r"L", r"+", r"p\,\Delta", font_size=34),
            MathTex(r"\mathbb{E}[\operatorname{r}(x)]", r"=", r"x", font_size=34),
            MathTex(r"\operatorname{Var}[\operatorname{r}(x)]", r"=", r"p\,(1-p)\,\Delta^2", r"\le",
                    r"\tfrac14\,\Delta^2", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        rows[3][-1].set_color(YES)
        whys = VGroup(label(r"between two levels a step $\Delta$ apart", font_size=18, color=GREY_B),
                      label(r"round up with probability $p$", font_size=18, color=GREY_B),
                      label(r"expand", font_size=18, color=GREY_B),
                      label(r"unbiased: \ exact in expectation", font_size=18, color=YES),
                      label(r"the price: \ noise, \ at most half a step", font_size=18, color=KERN))
        for w, r in zip(whys, rows):
            w.next_to(r, RIGHT, buff=0.35)
        p = 0.3
        nl = NumberLine(x_range=[0, 1, 0.1], length=4.0, include_ticks=False, color=GREY_B).move_to([4.3, 1.9, 0])
        ends = VGroup(Line(nl.n2p(0) + UP * 0.15, nl.n2p(0) + DOWN * 0.15, color=WHITE),
                      Line(nl.n2p(1) + UP * 0.15, nl.n2p(1) + DOWN * 0.15, color=WHITE))
        el = VGroup(label(r"$L$", font_size=24).next_to(nl.n2p(0), DOWN, buff=0.25),
                    label(r"$L + \Delta$", font_size=24).next_to(nl.n2p(1), DOWN, buff=0.25))
        xd = Dot(nl.n2p(p), color=HEAD, radius=0.08)
        xl = label(r"$x$", font_size=24, color=HEAD).next_to(xd, DOWN, buff=0.2)
        down = CurvedArrow(nl.n2p(p) + UP * 0.15, nl.n2p(0) + UP * 0.15, angle=0.9, color=DATA, stroke_width=3)
        up = CurvedArrow(nl.n2p(p) + UP * 0.15, nl.n2p(1) + UP * 0.15, angle=-0.9, color=LAM, stroke_width=3)
        dl = label(r"$1 - p$", font_size=22, color=DATA).next_to(down, UP, buff=0.08)
        ul = label(r"$p$", font_size=22, color=LAM).next_to(up, UP, buff=0.08)
        near = label(r"round to nearest: \ always $L$, \ off by $p\,\Delta$", font_size=18, color=NO)
        near.next_to(el, DOWN, buff=0.3).set_x(nl.get_x())
        with self.voiceover(
            "Part 4 rounded to the nearest number. That is the best single answer, but it is biased. "
            "<bookmark mark='a'/> Put x a fraction p of the way from one level, L, to the next, L plus delta. "
            "Round to nearest always gives L, off by p delta. <bookmark mark='b'/> Stochastic rounding flips a "
            "biased coin: up with probability p, down with probability one minus p. <bookmark mark='c'/> The "
            "expected result is one minus p times L, plus p times L plus delta. <bookmark mark='d'/> Expand it: L"
            " plus p delta. <bookmark mark='e'/> That is x: the rounding is exact on average. "
            "<bookmark mark='f'/> The price is noise, a variance of p times one minus p times delta squared, at "
            "most a quarter of delta squared."
        ) as vo:
            self.play(FadeIn(head), Create(nl), FadeIn(ends), FadeIn(el))
            vo.wait_until("a")
            self.play(FadeIn(xd, scale=1.5), FadeIn(xl), Write(rows[0]), FadeIn(whys[0]))
            self.play(FadeIn(near))
            vo.wait_until("b")
            self.play(Create(down), Create(up), FadeIn(dl), FadeIn(ul), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(Write(rows[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("e")
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]))
            vo.wait_until("f")
            self.play(FadeIn(rows[4], shift=DOWN * 0.2), FadeIn(whys[4]))
        self.wait(0.4)
        self.clear_scene()

    def drift(self):
        head = label(r"Many small updates", font_size=36).to_edge(UP, buff=0.3)
        T = SR_STEPS
        top = int(SR_STEP * T) + 2
        ax = Axes(x_range=[0, T, 4], y_range=[0, top, 2], x_length=7.0, y_length=4.2, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 20})
        ax.to_edge(LEFT, buff=0.9).shift(DOWN * 0.3)
        xl = label(r"updates of a quarter step", font_size=19, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yl = label(r"stored value \ (in steps)", font_size=19, color=GREY_A).next_to(ax, UP, buff=0.15).align_to(
            ax, LEFT)
        rng = random.Random(SR_SEED)
        s, path = 0, [0]
        for _ in range(T):
            v = s + SR_STEP
            s = int(v) + (1 if rng.random() < v - int(v) else 0)
            path.append(s)
        exact = DashedLine(ax.c2p(0, 0), ax.c2p(T, SR_STEP * T), color=GREY_A, stroke_width=2.5)
        pts = [ax.c2p(0, 0)]
        for t in range(1, T + 1):
            pts += [ax.c2p(t, path[t - 1]), ax.c2p(t, path[t])]
        sr = VMobject(color=YES, stroke_width=4).set_points_as_corners(pts)
        rn = Line(ax.c2p(0, 0), ax.c2p(T, 0), color=NO, stroke_width=5)
        keys = VGroup(label(r"exact sum", font_size=20, color=GREY_A),
                      label(r"round to nearest: \ stuck at 0", font_size=20, color=NO),
                      label(rf"stochastic: \ one random run, \ ends at {path[-1]}", font_size=20, color=YES)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(ax, RIGHT, buff=0.45).shift(UP * 1.2)
        why = wrapped_label(r"a quarter step rounds back down every time; \ Part 23's gradient descent makes exactly "
                            r"such tiny updates", 4.9, font_size=19, color=GREY_A).next_to(keys, DOWN, buff=0.45
                                                                                          ).align_to(keys, LEFT)
        cite = wrapped_label(r"Gupta, \ Agrawal, \ Gopalakrishnan and Narayanan \ (2015): \ networks trained in "
                             r"16-bit fixed point with stochastic rounding matched 32-bit floats", 4.9, font_size=18,
                             color=HEAD).next_to(why, DOWN, buff=0.3).align_to(keys, LEFT)
        ill = note(r"illustrative: \ one seeded random run", font_size=16).to_corner(DL, buff=0.2)
        with self.voiceover(
            "Why want noise? <bookmark mark='a'/> Add a quarter of a step, again and again, to a number stored on"
            " a coarse grid. The exact sum climbs steadily. <bookmark mark='b'/> Round to nearest sends every "
            "quarter step back down, so the stored value never moves. <bookmark mark='c'/> Stochastic rounding "
            "moves up one time in four, on average, and follows the sum. <bookmark mark='d'/> This is Part 23's "
            "gradient descent in low precision: millions of tiny updates. In 2015 Suyog Gupta and colleagues "
            "trained networks in sixteen-bit fixed point, and with stochastic rounding they matched thirty-two-"
            "bit floats."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(exact), FadeIn(keys[0]))
            vo.wait_until("b")
            self.play(Create(rn), FadeIn(keys[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(sr), run_time=3.5, rate_func=linear)
            self.play(FadeIn(keys[2]))
            vo.wait_until("d")
            self.play(FadeIn(why))
            self.play(FadeIn(cite))
        self.wait(0.4)
        self.clear_scene()

    def approximate(self):
        q = load("quant")
        mm, cl = q["matmul"], q["classifier"]
        head = label(r"Approximate computing", font_size=36).to_edge(UP, buff=0.3)
        n, k = 8, 4
        dot = 0.3
        dots = VGroup()
        for i in range(n):
            for j in range(n):
                c = i + j                      # the column (weight 2^c) of partial product a_j b_i
                d = Dot([-(c * dot), -i * dot, 0], radius=0.075, color=HEAD)
                d.col = c
                dots.add(d)
        dots.move_to([-3.6, 0.2, 0])
        dropped = VGroup(*[d for d in dots if d.col < k])
        cx, cy = dots[0].get_x() - (k - 0.5) * dot, dots[0].get_y()
        cut = DashedLine([cx, cy + 0.3, 0], [cx, cy - n * dot, 0], color=NO, stroke_width=2)
        dl = label(r"$8 \times 8$ partial products: \ 64 AND gates, \ then adders", font_size=19, color=GREY_A)
        dl.next_to(dots, UP, buff=0.35)
        cw = label(r"columns of weight $1, 2, 4, 8$", font_size=18, color=NO).next_to(dots, DOWN, buff=0.3).align_to(
            dots, RIGHT)
        nd = len(dropped)
        bound = sum((c + 1) * 2 ** c for c in range(k))
        top = (2 ** n - 1) ** 2
        rows = VGroup(
            MathTex(r"\text{error}", r"\le", r"\sum_{c=0}^{3} (c+1)\,2^c", font_size=32),
            MathTex(r"\text{error}", r"\le", r"1 + 4 + 12 + 32", r"=", rf"{bound}", font_size=32),
            MathTex(r"\frac{\text{error}}{255^2}", r"\le", rf"\frac{{{bound}}}{{{top:,}}}".replace(",", "{,}"),
                    r"<", rf"{100 * bound / top:.2f}\%", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 1.0, 0])
        rows[2][-1].set_color(YES)
        why = label(rf"drop the {nd} smallest partial products", font_size=19, color=NO).next_to(rows, UP, buff=0.3
                                                                                                 ).align_to(rows, LEFT)
        meas = VGroup(
            label(rf"measured \ (chapter 5's int8 classifier): \ scores off by {100 * cl['score_rel_error']:.1f}\%, "
                  rf"\ answers changed on {100 * (1 - cl['agreement']):.1f}\% of points", font_size=19, color=HEAD),
            label(r"error in the numbers is not error in the answer: \ images, \ sound, \ learning tolerate it",
                  font_size=19, color=WHITE),
            label(r"never addresses, \ branches, \ or the Job's counts", font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.35)
        cite = label(r"also: \ skipping loop iterations \ (loop perforation, \ Rinard's group, \ 2011)", font_size=18,
                     color=GREY_A).next_to(meas, UP, buff=0.3).align_to(meas, LEFT)
        with self.voiceover(
            "Approximate computing gives up accuracy on purpose. <bookmark mark='a'/> An eight-bit multiplier "
            "forms sixty-four partial products, one AND gate each, and adds them up by column. "
            "<bookmark mark='b'/> Drop the ten in the four lowest columns, and their adders with them. "
            f"<bookmark mark='c'/> The answer is off by at most {say(bound)}, <bookmark mark='d'/> under a tenth "
            "of a percent of the largest product. <bookmark mark='e'/> Is that acceptable? It depends on who "
            "reads the answer. Chapter five's eight-bit classifier had its scores off by about one percent, yet "
            f"changed its answer on only {say_dec(100*(1-cl['agreement']))} percent of the points. Images, sound "
            "and learning tolerate error; addresses, branches and the Job's word counts do not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.01), FadeIn(dl), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cut), FadeIn(cw), FadeIn(why), dropped.animate.set_color(NO).set_opacity(0.3))
            self.play(Write(rows[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(meas[0]))
            self.play(FadeIn(meas[1]), FadeIn(cite))
            self.play(FadeIn(meas[2]))
        _ = mm
        self.wait(0.4)
        self.clear_scene()


def tag_pair(w, x):
    t = label(rf"${w} \cdot {x}$", font_size=20, color=WHITE)
    r = RoundedRectangle(width=t.width + 0.3, height=0.48, corner_radius=0.08, stroke_color=YES, stroke_width=1.6,
                         fill_color=BG, fill_opacity=1)
    t.move_to(r)
    return VGroup(r, t)


def say(n: int) -> str:
    """A small integer as a speaker says it."""
    tens = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
    if n < 20:
        return _ONES[n]
    return tens[n // 10] + ("" if n % 10 == 0 else "-" + _ONES[n % 10])


def say_dec(x: float, digits: int = 1) -> str:
    whole, frac = f"{x:.{digits}f}".split(".")
    return say(int(whole)) + " point " + " ".join(_ONES[int(c)] for c in frac)


_ = (BG, KERN, LAM, PART)
