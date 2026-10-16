from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import (ALPHA27, ZoomLadder, letter, letter_bars, load, tt)


class Probability(VoiceoverScene):
    def construct(self):
        self.card()
        self.frequencies()
        self.unit_bar()
        self.conditional()
        self.chain_rule()
        self.ladder()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(1, r"Probability, and the chain rule", r"How do you write a guess down?", lit=(1948,),
                            part=1)
        with self.voiceover("Chapter one. Before we can score a guess, we need a way to write one down.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def frequencies(self):
        d = load("letters")
        corpus = load("corpus")
        p = d["p"]
        n = int(d["n"])
        assert n == 22_788_042 and corpus["n_books"] == 30
        g = letter_bars(p, width=12.0, height=3.4, base=(0, -2.3))
        head = label(r"$22{,}788{,}042$ symbols from $30$ novels", font_size=34).to_edge(UP, buff=0.45)
        sub = label(r"$26$ letters and the space; \ capitals and punctuation dropped", font_size=24,
                    color=GREY_B).next_to(head, DOWN, buff=0.18)
        books = VGroup(*[label(rf"\textit{{{t}}}", font_size=24, color=GREY_A) for t in corpus["titles"][:10]])
        books.arrange_in_grid(rows=5, cols=2, buff=(0.6, 0.16), col_alignments="ll").move_to(DOWN * 0.4)
        more = label(r"\ldots\ and $20$ more", font_size=24, color=GREY_B).next_to(books, DOWN, buff=0.3)
        space_i, e_i = 0, ALPHA27.index("e")
        assert abs(p[space_i] - 0.191) < 0.001 and abs(p[e_i] - 0.0999) < 0.0005
        sp_val = MathTex(r"0.191", font_size=26, color=C.TRUE_P).next_to(g.bars[space_i], UP, buff=0.1)
        e_val = MathTex(r"0.100", font_size=26, color=C.TRUE_P).next_to(g.bars[e_i], UP, buff=0.1)
        with self.voiceover(
            "Take thirty novels, from Pride and Prejudice to The Great Gatsby, and count every symbol in them. We "
            "use Shannon's alphabet: twenty-six letters and the space, with capitals and punctuation dropped. That's "
            "<bookmark mark='a'/> twenty-two point eight million symbols. <bookmark mark='b'/> The space is the "
            "most common, about one symbol in five. Then e, one in ten."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), LaggedStart(*[FadeIn(b) for b in books], lag_ratio=0.1), FadeIn(more))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in g.bars], lag_ratio=0.05), FadeIn(g.labels),
                      FadeOut(books), FadeOut(more), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(sp_val), Indicate(g.bars[space_i], color=WHITE))
            self.play(FadeIn(e_val))
        # sort by frequency
        order = list(d["order"])
        assert "".join(ALPHA27[i] for i in order[:6]) == " etaon"
        slot = g.slot
        anims = []
        for k, i in enumerate(order):
            x = g.x0 + (k + 0.5) * slot
            anims += [g.bars[i].animate.set_x(x), g.labels[i].animate.set_x(x)]
        with self.voiceover(
            "Sorted, the familiar order appears: space, e, t, a, o, n. <bookmark mark='z'/> At the far end, x, j, q "
            "and z, each well under one symbol in a thousand."
        ) as vo:
            self.play(*anims, FadeOut(sp_val), FadeOut(e_val), run_time=2.0)
            vo.wait_until("z")
            self.play(*[Indicate(g.labels[i], color=C.SURPRISE, scale_factor=1.5) for i in order[-4:]])
        self.g, self.head, self.sub, self.p = g, head, sub, p

    # ------------------------------------------------------------------
    def unit_bar(self):
        g, p = self.g, self.p
        defn = mtex(r"p(x) \ge 0, \qquad \sum_x p(x) = 1", font_size=40).to_edge(UP, buff=0.5)
        W, y = 12.0, 0.4
        L = -W / 2
        slivers, cum = [], 0.0
        for i in range(27):
            w = W * p[i]
            r = Rectangle(width=w, height=0.6, stroke_width=1, stroke_color=BACKGROUND, fill_color=C.TRUE_P,
                          fill_opacity=0.55 + 0.4 * (i % 2)).move_to([L + (cum + p[i] / 2) * W, y, 0])
            slivers.append(r)
            cum += p[i]
        labs = VGroup(*[letter(ALPHA27[i], font_size=22, color=WHITE).move_to(slivers[i]) for i in range(27)
                        if W * p[i] > 0.22])
        ends = VGroup(MathTex("0", font_size=28, color=GREY_B).next_to(slivers[0], DOWN, buff=0.2).align_to(slivers[0], LEFT),
                      MathTex("1", font_size=28, color=GREY_B).next_to(slivers[-1], DOWN, buff=0.2).align_to(slivers[-1], RIGHT))
        cap = label(r"a guess $=$ a way of sharing one unit of belief among the possibilities", font_size=28,
                    color=GREY_A).move_to(DOWN * 1.6)
        with self.voiceover(
            "This is a probability distribution: a number for each possibility, <bookmark mark='a'/> none of them "
            "negative, and adding up to one. <bookmark mark='b'/> Stack the bars end to end, and they fill a bar of "
            "length exactly one, with a sliver for every symbol, as wide as its probability. A guess, written down "
            "properly, is a way of sharing one unit of belief among the possibilities."
        ) as vo:
            self.play(FadeOut(self.head), FadeOut(self.sub))
            vo.wait_until("a")
            self.play(Write(defn))
            vo.wait_until("b")
            self.play(*[ReplacementTransform(g.bars[i], slivers[i]) for i in range(27)], FadeOut(g.labels),
                      run_time=2.2)
            self.play(FadeIn(labs), FadeIn(ends))
            self.play(FadeIn(cap, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    MW, MH, MX, MY = 4.6, 4.6, -6.5, 2.3  # the mosaic: width, height, top-left corner
    PX, PW = -0.5, 1.5  # where a column is pulled out to, and how wide

    def mosaic_cells(self, joint, cond):
        """The unit square cut by the previous symbol (column widths P(A)) and then by the next (cell heights P(B|A)):
        cell areas are the joint probabilities."""
        p1 = joint.sum(1)
        cells, x = VGroup(), self.MX
        for i in range(27):
            w = self.MW * p1[i]
            y = self.MY
            for j in range(27):
                h = self.MH * cond[i, j]
                shade = 0.35 + 0.55 * ((j * 7) % 27) / 26
                col = interpolate_color(ManimColor("#1B2638"), ManimColor(C.TRUE_P), shade)
                cells.add(Rectangle(width=max(w, 1e-4), height=max(h, 1e-4), stroke_width=0.5,
                                    stroke_color=BACKGROUND, fill_color=col, fill_opacity=1)
                          .move_to([x + w / 2, y - h / 2, 0]))
                y -= h
            x += w
        return cells

    def pull(self, cells, i, cond, lit=(), min_label=0.26):
        """Column i of the mosaic, pulled out to the right and stretched: what follows symbol i."""
        col = VGroup(*[cells[i * 27 + j] for j in range(27)])
        out = col.copy()
        out.stretch_to_fit_width(self.PW).move_to([self.PX, self.MY - self.MH / 2, 0])
        for j in lit:
            out[j].set_fill(C.BITS, opacity=1)
        labs = VGroup(*[letter(ALPHA27[j], font_size=24, color=C.BITS if j in lit else WHITE)
                        .next_to(out[j], RIGHT, buff=0.12) for j in range(27) if self.MH * cond[i, j] > min_label])
        frame = SurroundingRectangle(col, buff=0.0, color=C.CONTEXT, stroke_width=2.5)
        rays = VGroup(*[Line(frame.get_corner(a), out.get_corner(b), color=C.CONTEXT, stroke_width=1.2,
                             stroke_opacity=0.6) for a, b in ((UR, UL), (DR, DL))])
        return VGroup(col, out, labs, frame, rays)

    def show_pull(self, pl, run_time=1.4):
        col, out, labs, frame, rays = pl
        self.play(Create(frame), run_time=0.5)
        self.play(TransformFromCopy(col, out), Create(rays), run_time=run_time)
        self.play(FadeIn(labs), run_time=0.5)

    def conditional(self):
        b = load("bigram")
        cond, joint = b["cond"], b["joint"]
        cell = 0.165
        x0, y0 = -6.3, 2.35  # top-left corner of the grid
        grid = VGroup()
        for i in range(27):
            for j in range(27):
                v = float(np.sqrt(cond[i, j]))
                col = interpolate_color(ManimColor("#151B26"), ManimColor(C.TRUE_P), min(1.0, v * 1.6))
                if v > 0.75:
                    col = interpolate_color(ManimColor(C.TRUE_P), ManimColor(WHITE), (v - 0.75) * 4)
                grid.add(Square(side_length=cell, stroke_width=0, fill_color=col, fill_opacity=1)
                         .move_to([x0 + (j + 0.5) * cell, y0 - (i + 0.5) * cell, 0]))
        rows = VGroup(*[letter(ALPHA27[i], font_size=13, color=GREY_B).move_to([x0 - 0.15, y0 - (i + 0.5) * cell, 0])
                        for i in range(27)])
        cols = VGroup(*[letter(ALPHA27[j], font_size=13, color=GREY_B).move_to([x0 + (j + 0.5) * cell, y0 + 0.15, 0])
                        for j in range(27)])
        rl = label(r"previous", font_size=20, color=GREY_B)
        if not zh():  # Chinese reads top to bottom unrotated (the table sets it as a vertical stack)
            rl.rotate(PI / 2)
        rl.next_to(rows, LEFT, buff=0.12)
        cl = label(r"next", font_size=20, color=GREY_B).next_to(cols, UP, buff=0.1)
        qi, ui, ti, hi = (ALPHA27.index(c) for c in "quth")
        assert b["q_u"] > 0.998
        head = label(r"$P(\text{next} \mid \text{previous})$ \ for every pair of symbols", font_size=30)
        head.move_to([2.6, 3.3, 0])
        # the same numbers as areas: the unit square, cut by the previous symbol, then by the next
        cells = self.mosaic_cells(joint, cond)
        p1 = joint.sum(1)
        mlabs = VGroup(*[letter(ALPHA27[i], font_size=20, color=GREY_A).next_to(VGroup(*cells[i * 27:(i + 1) * 27]),
                                                                              DOWN, buff=0.1)
                         for i in range(27) if self.MW * p1[i] > 0.2])
        mcap = label(r"previous symbol", font_size=22, color=GREY_B).next_to(mlabs, DOWN, buff=0.12)
        mcap.set_x(self.MX + self.MW / 2)
        f_def = mtex(r"P(B \mid A) = \frac{P(A \text{ and } B)}{P(A)}", font_size=40).move_to([3.7, 1.9, 0])
        pt = self.pull(cells, ti, cond, lit=(hi,))
        out = pt[1]
        b_w = brace_note(out, r"$P(A) = P(\texttt{t}) = 0.072$", DOWN, color=C.CONTEXT, font_size=24)
        b_h = Brace(out[hi], RIGHT, buff=0.42, color=C.INTERVAL)
        b_h_l = label(r"$P(B \mid A) = 0.314$", font_size=24, color=C.INTERVAL).next_to(b_h, RIGHT, buff=0.1)
        area = label(r"area in the square: \ $P(A \text{ and } B)$", font_size=24, color=C.BITS)
        area.next_to(f_def, DOWN, buff=0.45)
        assert abs(p1[ti] - 0.0724) < 0.0005 and abs(cond[ti, hi] - 0.314) < 0.001
        lit_cell = cells[ti * 27 + hi].copy().set_fill(C.BITS, opacity=1)
        with self.voiceover(
            "But we rarely guess from nothing. Once you know the previous letter, the odds change. <bookmark mark='a'/> "
            "Here is the whole table: each row is the previous symbol, and each square shows how likely each next "
            "symbol is, given that one. <bookmark mark='d'/> This is conditional probability: the probability of B "
            "given A is the probability of both, divided by the probability of A."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid[i * 27:(i + 1) * 27]) for i in range(27)], lag_ratio=0.08),
                      FadeIn(rows), FadeIn(cols), FadeIn(rl), FadeIn(cl), run_time=2.5)
            vo.wait_until("d")
            self.play(*[ReplacementTransform(grid[k], cells[k]) for k in range(729)], FadeOut(rows), FadeOut(cols),
                      FadeOut(rl), FadeOut(cl), run_time=2.2)
            self.play(FadeIn(mlabs), FadeIn(mcap), FadeIn(lit_cell))
            self.show_pull(pt)
            self.play(Write(f_def), FadeIn(b_w), GrowFromCenter(b_h), FadeIn(b_h_l))
            self.play(FadeIn(area), Indicate(lit_cell, color=WHITE, scale_factor=2.5))
        f_qu = mtex(r"P(" + tt("u") + r" \mid " + tt("q") + r") = \frac{18{,}469}{18{,}496} = 0.9985", font_size=36,
                    color=WHITE).move_to([3.7, 1.9, 0])
        n_q = int(load("letters")["counts"][qi])
        assert n_q == 18496 and round(float(joint[qi, ui]) * int(load("letters")["n"])) == 18469
        cap_q = label(r"after \texttt{q}, almost surely \texttt{u}", font_size=28, color=C.BITS).next_to(f_qu, DOWN,
                                                                                                    buff=0.4)
        cap_sp = label(r"after a space, almost anything: \ a word is starting", font_size=28, color=C.CONTEXT)
        cap_sp.move_to([3.7, -0.6, 0])
        pq = self.pull(cells, qi, cond, lit=(ui,))
        q_col = VGroup(*cells[qi * 27:(qi + 1) * 27])
        q_arrow = Arrow(q_col.get_bottom() + DOWN * 0.9, q_col.get_bottom() + DOWN * 0.05, buff=0, color=C.CONTEXT,
                        stroke_width=3, max_tip_length_to_length_ratio=0.25)
        q_name = letter("q", font_size=26, color=C.CONTEXT).next_to(q_arrow, DOWN, buff=0.05)
        ps = self.pull(cells, 0, cond, min_label=0.2)
        with self.voiceover(
            "In our books, q appears eighteen thousand, four hundred and ninety-six times, and all but twenty-seven "
            "of them are followed by u. <bookmark mark='a'/> So the probability of u, given q, is 0.9985. "
            "<bookmark mark='b'/> After a space, on the other hand, almost anything can come next: a new word is "
            "starting."
        ) as vo:
            self.play(FadeOut(VGroup(pt[1:], b_w, b_h, b_h_l, f_def, area, lit_cell)), FadeOut(mlabs), FadeOut(mcap))
            self.play(GrowArrow(q_arrow), FadeIn(q_name))
            self.show_pull(pq, run_time=1.2)
            vo.wait_until("a")
            self.play(Write(f_qu), FadeIn(cap_q))
            vo.wait_until("b")
            self.play(FadeOut(VGroup(pq[1:], q_arrow, q_name)))
            self.show_pull(ps, run_time=1.2)
            self.play(FadeIn(cap_sp))
        self.wait(0.3)
        self.play(FadeOut(VGroup(ps[1:], f_qu, cap_q, cap_sp, head)))
        self.cells, self.cond = cells, cond

    # ------------------------------------------------------------------
    def chain_rule(self):
        cells, cond = self.cells, self.cond
        ch = load("chain")
        ti, hi, ei = (ALPHA27.index(c) for c in "the")
        pt_, ph, pe = float(ch["p1"][ti]), float(ch["after_t"][hi]), float(ch["after_th"][ei])
        assert abs(pt_ - 0.0724) < 0.0005 and abs(ph - 0.314) < 0.001 and abs(pe - 0.613) < 0.001
        assert abs(ch["p_the"] - 0.0139) < 0.0001
        K1, K2, K3 = C.CONTEXT, C.INTERVAL, TEAL_C
        colors = {r"P(x_1)": K1, r"P(x_2 \mid x_1)": K2, r"P(x_1, x_2)": C.BITS, r"P(x_3 \mid x_1, x_2)": K3}
        steps = [
            [r"P(x_1, x_2)", "=", r"P(x_1)", r"P(x_2 \mid x_1)"],
            [r"P(x_1, x_2, x_3)", "=", r"P(x_1, x_2)", r"P(x_3 \mid x_1, x_2)"],
            [r"P(x_1, x_2, x_3)", "=", r"P(x_1)", r"P(x_2 \mid x_1)", r"P(x_3 \mid x_1, x_2)"],
            [r"P(x_1, \dots, x_n)", "=", r"\prod_{i=1}^{n}", r"P(x_i \mid x_1, \dots, x_{i-1})"],
        ]
        eqs = [cmath(*s, colors=colors, font_size=40) for s in steps]
        for e in eqs:
            e.move_to([3.4, 3.2, 0])
            if e.width > 7.0:
                e.width = 7.0
        eqs[3].scale(1.2).move_to(UP * 0.6)
        head = label(r"The chain rule", font_size=36).to_corner(UL, buff=0.35)
        pt = self.pull(cells, ti, cond, lit=(hi,))
        out = pt[1]
        b_w = brace_note(out, r"$P(x_1)$", DOWN, color=K1, font_size=30)
        b_h = Brace(out[hi], RIGHT, buff=0.42, color=K2)
        b_h_l = MathTex(r"P(x_2 \mid x_1)", font_size=30, color=K2).next_to(b_h, RIGHT, buff=0.1)
        lit_cell = cells[ti * 27 + hi].copy().set_fill(C.BITS, opacity=1)
        names = MathTex(r"x_1 = \texttt{t}, \ x_2 = \texttt{h}, \ x_3 = \texttt{e}", font_size=30, color=GREY_A)
        names.next_to(eqs[0], DOWN, buff=0.3)
        # the cell for "th", pulled out again and cut by the third letter
        h3 = 3.4
        cell3 = VGroup()
        y = 1.9
        for j in range(27):
            h = h3 * float(ch["after_th"][j])
            cell3.add(Rectangle(width=1.5, height=max(h, 1e-4), stroke_width=0.6, stroke_color=BACKGROUND,
                                fill_color=K3 if j == ei else C.BITS, fill_opacity=1 if j == ei else 0.55)
                      .move_to([3.0, y - h / 2, 0]))
            y -= h
        c3l = VGroup(*[letter(ALPHA27[j], font_size=24, color=K3 if j == ei else WHITE).next_to(cell3[j], RIGHT, buff=0.12)
                       for j in range(27) if h3 * ch["after_th"][j] > 0.25])
        rays3 = VGroup(*[Line(out[hi].get_corner(a), cell3.get_corner(b), color=C.BITS, stroke_width=1.2, stroke_opacity=0.6)
                         for a, b in ((UR, UL), (DR, DL))])
        b3 = Brace(cell3[ei], RIGHT, buff=0.42, color=K3)
        b3_l = MathTex(r"P(x_3 \mid x_1, x_2)", font_size=30, color=K3).next_to(b3, RIGHT, buff=0.1)
        num = mtex(r"P(\texttt{the}) = 0.072 \times 0.314 \times 0.613 = 0.0139", font_size=30).move_to([3.6, -2.7, 0])
        with self.voiceover(
            "Multiply that definition out, and you get a rule for whole strings. <bookmark mark='a'/> The "
            "probability of two symbols is the probability of the first, times the probability of the second given "
            "the first. <bookmark mark='b'/> For three, treat the first two as a single event, <bookmark mark='c'/> "
            "and substitute."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lit_cell))
            self.show_pull(pt, run_time=1.0)
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(names))
            self.play(FadeIn(b_w), GrowFromCenter(b_h), FadeIn(b_h_l), Indicate(lit_cell, color=WHITE, scale_factor=2.5))
            vo.wait_until("b")
            self.play(FadeOut(names), FadeOut(b_h), FadeOut(b_h_l))
            morph(self, eqs[0], eqs[1], run_time=1.2)
            self.play(TransformFromCopy(out[hi], cell3), Create(rays3), run_time=1.3)
            self.play(FadeIn(c3l), GrowFromCenter(b3), FadeIn(b3_l))
            vo.wait_until("c")
            morph(self, eqs[1], eqs[2], run_time=1.2)
            self.play(Write(num))
        cap = label(r"exact, for any distribution: \ no assumption has been made", font_size=30, color=C.BITS)
        cap2 = label(r"a text's probability $=$ a product of next-symbol guesses", font_size=30, color=GREY_A)
        box = SurroundingRectangle(eqs[3], color=C.BITS, buff=0.25, corner_radius=0.1)
        cap.next_to(box, DOWN, buff=0.4)
        cap2.next_to(cap, DOWN, buff=0.25)
        with self.voiceover(
            "And so on, one symbol at a time. <bookmark mark='a'/> The probability of a whole text is a product of "
            "next-symbol guesses, each made knowing everything before it. This is the chain rule, and it is exact: "
            "no assumption has been made. <bookmark mark='b'/> It is also why a machine that only ever guesses the "
            "next symbol can score, or write, an entire text."
        ) as vo:
            self.play(FadeOut(VGroup(cells, pt[1:], lit_cell, b_w, cell3, c3l, rays3, b3, b3_l, num, head)), run_time=0.8)
            morph(self, eqs[2], eqs[3], run_time=1.4)
            self.play(Create(box))
            vo.wait_until("a")
            self.play(FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(cap2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ladder(self):
        a = load("arith")
        steps = a["steps"]
        assert [s["symbol"] for s in steps[:3]] == ["t", "h", "e"]
        assert [s["context"] for s in steps[:3]] == ["id ", "d t", " th"]
        ps = [s["p"] for s in steps[:3]]
        assert abs(ps[0] - 0.155) < 0.001 and abs(ps[1] - 0.614) < 0.001 and abs(ps[2] - 0.700) < 0.001
        lad = ZoomLadder(steps, W=8.8, x=-0.5)
        ys = [2.0, 0.55, -0.9]
        head = label(r"he said\ \ldots \quad $P(" + tt("the") + r")$ one letter at a time", font_size=32)
        head.to_edge(UP, buff=0.35)
        rows = [lad.row(k, ys[k]) for k in range(3)]
        funnels = [lad.funnel(k, ys[k], ys[k + 1]) for k in range(2)]
        tex = [r"P(" + tt("t") + r" \mid " + tt("id ") + r") = 0.155",
               r"P(" + tt("h") + r" \mid " + tt("d t") + r") = 0.614",
               r"P(" + tt("e") + r" \mid " + tt(" th") + r") = 0.700"]
        reads = [mtex(t, font_size=26, color=C.INTERVAL) for t in tex]
        for r, y in zip(reads, ys):
            r.move_to([4.25, y, 0], aligned_edge=LEFT)
        ctxs = VGroup(*[label(tt(s["context"]), font_size=24, color=C.CONTEXT).move_to([-5.7, y, 0])
                        for s, y in zip(steps[:3], ys)])
        ctx_head = label(r"context", font_size=20, color=GREY_B).next_to(ctxs[0], UP, buff=0.3)
        prod = mtex(r"P(" + tt("the") + r" \mid " + tt("id ") + r") = 0.155 \times 0.614 \times 0.700 = 0.0666",
                    font_size=34, color=WHITE).move_to(DOWN * 2.35)
        assert abs(np.prod(ps) - 0.0666) < 0.0001
        note_ctx = note(r"context: the last three symbols (an order-3 counting model of the $30$ books)")
        note_ctx.to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here's the chain rule as a picture. Someone has just written, he said, and we want the probability "
            "that the next three letters are t, h, e. <bookmark mark='a'/> The first bar is the whole unit of "
            "belief, shared among the 27 possible next symbols, given the last three: d, i, space. t gets a sliver "
            "of width 0.155."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note_ctx))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][0]), Create(rows[0][2]), FadeIn(ctxs[0]), FadeIn(ctx_head))
            self.play(FadeIn(rows[0][1]), FadeIn(reads[0]))
        with self.voiceover(
            "Now zoom into that sliver and share it out again, <bookmark mark='a'/> this time by the probabilities "
            "of the next letter after d, space, t. h takes 61 percent of it. <bookmark mark='b'/> Zoom again: "
            "after space, t, h, the letter e takes 70 percent. <bookmark mark='c'/> The final sliver is as wide as "
            "the product: 0.0666, the probability of the whole string."
        ) as vo:
            self.play(FadeIn(funnels[0]), FadeIn(rows[1][0]), Create(rows[1][2]), FadeIn(ctxs[1]))
            vo.wait_until("a")
            self.play(FadeIn(rows[1][1]), FadeIn(reads[1]))
            vo.wait_until("b")
            self.play(FadeIn(funnels[1]), FadeIn(rows[2][0]), Create(rows[2][2]), FadeIn(ctxs[2]))
            self.play(FadeIn(rows[2][1]), FadeIn(reads[2]))
            vo.wait_until("c")
            self.play(Write(prod))
        with self.voiceover(
            "Keep this picture in mind: nested slivers, each one a guess. In chapter six, the very same picture "
            "will turn out to be a way of compressing text."
        ) as vo:
            self.play(Indicate(prod, color=C.INTERVAL), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
