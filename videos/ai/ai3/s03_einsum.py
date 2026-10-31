from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, HL, MONO, chapter, load

IDX = {"b": "#B39DDB", "h": "#F2A541", "t": "#4FD1C5", "q": "#4FD1C5", "k": "#58A6FF", "d": "#9BE37B",
       "e": "#FF6B8B", "i": "#58A6FF", "j": "#F7D154", "l": "#9BE37B"}


def cells(rows, cols, size=0.32, color=C.TRUE_P, opacity=0.35) -> VGroup:
    g = VGroup(*[Square(size, stroke_color=color, stroke_width=1.5, fill_color=color, fill_opacity=opacity)
                 .move_to([c * size, -r * size, 0]) for r in range(rows) for c in range(cols)])
    return g.move_to(ORIGIN)


def stack(depth, rows, cols, size=0.26, color=C.TRUE_P) -> VGroup:
    """A 3-axis array drawn as offset sheets."""
    g = VGroup()
    for k in range(depth):
        sh = cells(rows, cols, size, color, 0.25 + 0.5 * k / max(depth - 1, 1))
        sh.shift(np.array([0.22, 0.18, 0]) * (depth - 1 - k))
        g.add(sh)
    return g.move_to(ORIGIN)


def spec(s: str, font_size=34) -> Text:
    """An einsum string with each index letter in its colour (one Text, so the letters share a baseline)."""
    return data_text(s, font=MONO, font_size=font_size, color=GREY_A,
                     t2c={ch: IDX[ch] for ch in set(s) if ch in IDX})


def code_line(pre: str, idx: str, post: str, font_size=34) -> VGroup:
    """einsum('ij,jk->ik', A, B): the index string coloured, the rest grey."""
    a = data_text(pre, font=MONO, font_size=font_size, color=GREY_A)
    b = spec(idx, font_size)
    c = data_text(post, font=MONO, font_size=font_size, color=GREY_A)
    g = VGroup(a, b, c).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
    g.idx = b
    return g


class Einsum(VoiceoverScene):
    def construct(self):
        chapter(self, 2, r"Tensors and einsum", r"How do we write products of arrays with many axes?",
                "Chapter two. Tensors, and the notation attention is written in.", lit=(2017,))
        self.tensors()
        self.convention()
        self.examples()
        self.attention()
        self.order()

    # ------------------------------------------------------------------
    def tensors(self):
        e = load("einsum")
        sc = cells(1, 1, 0.5)
        ve = cells(1, 5, 0.42)
        ma = cells(4, 5, 0.36)
        cu = stack(4, 4, 5, 0.3)
        objs = VGroup(sc, ve, ma, cu).arrange(RIGHT, buff=1.0).move_to(UP * 0.6)
        names = [r"a number", r"a vector \\ one axis: $i$", r"a matrix \\ two axes: $i, j$",
                 r"a tensor \\ three axes: $b, t, d$"]
        labs = VGroup(*[label(n, font_size=26, color=GREY_A).next_to(o, DOWN, buff=0.35) for n, o in zip(names, objs)])
        for lb in labs:
            lb.set_y(-1.0)
        shapes = VGroup(
            label(r"a batch of text in GPT-2: \ $b \times 1024$ tokens $\times\ 768$ numbers", font_size=28),
            label(rf"inside attention: \ $b \times {e['heads']}$ heads $\times\ 1024 \times {e['dh']}$", font_size=28),
        ).arrange(DOWN, buff=0.25).to_edge(DOWN, buff=0.6)
        head = label(r"Tensors: \ arrays with any number of axes", font_size=40).to_edge(UP, buff=0.4)
        with self.voiceover(
            "A number, a vector, a matrix: zero, one and two axes. <bookmark mark='a'/> A batch of text is a list of "
            "sentences, each a list of tokens, each a list of numbers: three axes, what machine learning calls a "
            f"tensor. <bookmark mark='b'/> Attention splits the numbers among {e['heads']} heads: four. Products of such "
            "arrays need a notation that names the axes."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(o, scale=0.8), FadeIn(lb)) for o, lb in
                                    zip(objs[:3], labs[:3])], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(cu, scale=0.8), FadeIn(labs[3]))
            self.play(FadeIn(shapes[0]))
            vo.wait_until("b")
            self.play(FadeIn(shapes[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def convention(self):
        rows = [
            cmath(r"c_{ik}", "=", r"\sum_{j} a_{ij}\, b_{jk}", font_size=44),
            cmath(r"c_{ik}", "=", r"a_{ij}\, b_{jk}", font_size=44),
        ]
        whys = [why(r"row $i$ of $A$ against column $k$ of $B$"),
                why(r"Einstein (1916): \ an index repeated on the right is summed")]
        step = ladder(self, rows, whys, keep=2, top=3.1, x=-2.2, buff=0.45, edge=6.9)
        code = code_line("einsum('", "ij,jk->ik", "', A, B)", 36).move_to([0, 0.2, 0])
        A = cells(3, 4, 0.36, C.TRUE_P)
        B = cells(4, 3, 0.36, C.MODEL_Q)
        Cm = cells(3, 3, 0.36, C.BITS)
        grp = VGroup(A, MathTex(r"\times", font_size=36), B, MathTex("=", font_size=36), Cm).arrange(RIGHT, buff=0.35)
        grp.move_to([-2.0, -2.2, 0])
        row_hl = SurroundingRectangle(VGroup(*A[4:8]), color=IDX["i"], buff=0.04, stroke_width=3)
        col_hl = SurroundingRectangle(VGroup(*[B[3 * r + 1] for r in range(4)]), color=IDX["k"], buff=0.04,
                                      stroke_width=3)
        out_hl = SurroundingRectangle(Cm[4], color=WHITE, buff=0.03, stroke_width=3)
        rule = VGroup(label(r"an index in the output: \ kept", font_size=28, color=GREY_A),
                      label(r"an index only in the inputs: \ summed over", font_size=28, color=IDX["j"]),
                      label(r"cost: \ the product of all the index sizes", font_size=28, color=GREY_A))
        rule.arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.7, -2.2, 0])
        hist = note(r"A.~Einstein (1916); \ \texttt{numpy.einsum} (2011)").to_corner(DR, buff=0.4)
        with self.voiceover(
            "Multiplying two matrices: entry i k is row i of A against column k of B, summed over j. "
            "<bookmark mark='a'/> In 1916, writing general relativity, Einstein tired of summation signs and dropped "
            "them: an index that appears twice is summed. <bookmark mark='b'/> Programs adopted the idea as einsum, "
            "with a letter for each axis. <bookmark mark='c'/> A letter in the output is kept; a letter only in the "
            "inputs is summed away. And the cost is one multiply-add for every combination of the letters: i times j "
            "times k."
        ) as vo:
            step(0)
            self.play(FadeIn(grp))
            self.play(Create(row_hl), Create(col_hl), Create(out_hl))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(Write(code), FadeIn(hist))
            vo.wait_until("c")
            self.play(Indicate(code.idx[1], color=IDX["j"], scale_factor=1.5),
                      Indicate(code.idx[3], color=IDX["j"], scale_factor=1.5))
            self.play(LaggedStart(*[FadeIn(r_, shift=LEFT * 0.2) for r_ in rule], lag_ratio=0.5), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def examples(self):
        table = [
            ("i,i->", r"dot product: \ $\sum_i a_i b_i$"),
            ("i,j->ij", r"outer product: \ rank at most one"),
            ("ij,j->i", r"matrix times vector"),
            ("ij->ji", r"transpose"),
            ("ii->", r"trace: \ the diagonal, summed"),
            ("bij,bjk->bik", r"a batch of matrix products"),
        ]
        head = label(r"Six operations, \ one notation", font_size=40).to_edge(UP, buff=0.4)
        subtitle = note("colours name indices; output indices stay; input-only indices are summed",
                        font_size=22).next_to(head, DOWN, buff=0.25)
        rows = VGroup()
        for s, t in table:
            rows.add(VGroup(spec(s, 34), label(t, font_size=30, color=GREY_A)))
        for r in rows:
            r[0].move_to([-2.2, 0, 0], aligned_edge=RIGHT)
            r[1].move_to([-1.4, 0, 0], aligned_edge=LEFT)
        for k, r in enumerate(rows):
            r.shift(UP * (2.0 - 0.78 * k))
        with self.voiceover(
            "One function does all of these. <bookmark mark='a'/> The dot product: multiply, and sum everything. "
            "<bookmark mark='b'/> The outer product: nothing summed, a matrix of rank at most one. <bookmark mark='c'/> Matrix "
            "times vector. <bookmark mark='d'/> The transpose, which only reorders. <bookmark mark='e'/> The trace. "
            "<bookmark mark='f'/> And a batch of matrix products, the letter b carried along."
        ) as vo:
            self.play(FadeIn(head), FadeIn(subtitle), FadeIn(rows.copy().set_opacity(0.2)))
            for k, mk in enumerate("abcdef"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]), run_time=0.7)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attention(self):
        e = load("einsum")
        lines = [
            ("btd,dhe->bhte", r"$Q$, $K$, $V$: \ each token's vector, split into heads"),
            ("bhqe,bhke->bhqk", r"scores: \ every query against every key"),
            ("bhqk,bhke->bhqe", r"weights times values (after a softmax over $k$)"),
            ("bhqe,hed->bqd", r"heads merged back into one vector"),
        ]
        head = label(r"Attention, \ in four contractions", font_size=40).to_edge(UP, buff=0.4)
        rows = VGroup()
        for s, t in lines:
            rows.add(VGroup(spec(s, 30), label(t, font_size=26, color=GREY_A)))
        for k, r in enumerate(rows):
            r[0].move_to([-1.9, 2.3 - 0.72 * k, 0], aligned_edge=RIGHT)
            r[1].move_to([-1.5, 2.3 - 0.72 * k, 0], aligned_edge=LEFT)
        n, h, dh = int(e["n"]), int(e["heads"]), int(e["dh"])
        ms, mv, mp = float(e["macs_scores"]), float(e["macs_values"]), float(e["macs_proj"])
        top = max(ms, mv, mp)
        items = [(r"scores \ $h\,q\,k\,e$", ms, C.ATTN), (r"weighted values", mv, C.VALUE),
                 (r"$Q,K,V$ and output \ ($4 \times 1024 \times 768^2$)", mp, C.EMBED)]
        bars = VGroup()
        for k, (t, v, col) in enumerate(items):
            w = 6.0 * v / top
            y = -1.0 - 0.7 * k
            b = Rectangle(width=w, height=0.42, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([-1.4, y, 0], aligned_edge=LEFT)
            nm = label(t, font_size=24, color=GREY_A).move_to([-1.6, y, 0], aligned_edge=RIGHT)
            val = MathTex(rf"{v / 1e6:,.0f}".replace(",", "{,}") + r"\ \text{million}", font_size=26, color=col)
            val.next_to(b, RIGHT, buff=0.15)
            bars.add(VGroup(nm, b, val))
        cap = note(rf"multiply-adds per layer, \ one sequence of ${n:,}$ tokens, \ GPT-2 small \ (computed from the "
                   r"index sizes)".replace(",", "{,}")).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Here is attention, Part 13's subject, in this notation. <bookmark mark='a'/> Each token's vector is "
            "projected into queries, keys and values, split among heads. <bookmark mark='b'/> Every query is dotted with "
            "every key: e is summed away. <bookmark mark='c'/> A softmax turns scores into weights, which average the "
            "values. <bookmark mark='d'/> The heads are merged back. <bookmark mark='e'/> Read the costs off the "
            f"letters. For {n:,} tokens, the scores take about {ms / 1e6:,.0f} million multiply-adds per layer, and the "
            f"projections {mp / 1e6:,.0f} million. The scores grow with the square of the length: that is why long "
            "contexts are expensive."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows.copy().set_opacity(0.25)))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k]), run_time=0.8)
            vo.wait_until("e")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(b_[0]), GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]))
                                    for b_ in bars], lag_ratio=0.4), FadeIn(cap), run_time=2.4)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def order(self):
        e = load("einsum")
        a, b, c, d = (int(x) for x in e["shapes"])
        L, R = int(e["macs_left"]), int(e["macs_right"])
        s = 2.2 / a  # drawing scale: 1,000 rows -> 2.2 units
        thin = 20 * s * 6  # the 20-wide side, exaggerated 6x so it is visible

        def rect(h, w, col, txt):
            r = Rectangle(width=w, height=h, stroke_color=col, stroke_width=2, fill_color=col, fill_opacity=0.3)
            return VGroup(r, MathTex(txt, font_size=24, color=col).next_to(r, DOWN, buff=0.1))

        A = rect(2.2, thin, C.TRUE_P, rf"{a:,}\times{b}".replace(",", "{,}"))
        B = rect(thin, 2.2, C.MODEL_Q, rf"{b}\times{c:,}".replace(",", "{,}"))
        Cm = rect(2.2, thin, C.BITS, rf"{c:,}\times{d}".replace(",", "{,}"))
        names = VGroup(MathTex("A", color=C.TRUE_P), MathTex("B", color=C.MODEL_Q), MathTex("C", color=C.BITS))
        top = VGroup(A, B, Cm).arrange(RIGHT, buff=0.6, aligned_edge=UP).move_to([0, 1.35, 0])
        for nm, m in zip(names, (A, B, Cm)):
            nm.next_to(m[0], UP, buff=0.1)
        AB = rect(2.2, 2.2, C.PENALTY, rf"AB:\ {a:,}\times{c:,}".replace(",", "{,}")).move_to([-3.6, -1.4, 0])
        BC = rect(thin, thin, C.REWARD, rf"BC:\ {b}\times{d}").move_to([3.6, -1.0, 0])
        lt = label(r"$(AB)\,C$: \ $" + fmt_int(L) + r"$ multiply-adds", font_size=28, color=C.PENALTY)
        rt = label(r"$A\,(BC)$: \ $" + fmt_int(R) + "$", font_size=28, color=C.REWARD)
        lt.next_to(AB, DOWN, buff=0.15)
        rt.next_to(BC, DOWN, buff=0.5).set_y(lt.get_y())
        fac = L / R
        path = e["path"]
        first = "B and C" if sorted(path[0]) == [1, 2] else ("A and B" if sorted(path[0]) == [0, 1] else "A and C")
        tag = note(r"\texttt{einsum('ij,jk,kl->il', A, B, C, optimize=True)} \ picks the order").to_edge(DOWN, buff=0.3)
        head = label(r"The order of a product changes its cost", font_size=38).to_edge(UP, buff=0.3)
        with self.voiceover(
            f"The letters also show that order matters. <bookmark mark='a'/> A is {a:,} by {b}, B is {b} by {c:,}, C is "
            f"{c:,} by {d}. <bookmark mark='b'/> Multiply A and B first, and you build a {a:,} by {c:,} matrix on the "
            f"way: {L:,} multiply-adds. <bookmark mark='c'/> B and C first: {R:,}. The same answer, {fac:.0f} times "
            f"cheaper. <bookmark mark='d'/> einsum can find the cheap order itself; here it multiplies {first} first."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in (A, B, Cm)], lag_ratio=0.3), FadeIn(names))
            vo.wait_until("b")
            self.play(FadeIn(AB, shift=DOWN * 0.2), FadeIn(lt))
            vo.wait_until("c")
            self.play(FadeIn(BC, shift=DOWN * 0.2), FadeIn(rt))
            vo.wait_until("d")
            self.play(FadeIn(tag))
        self.wait(0.3)
        self.clear_scene()
