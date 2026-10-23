from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import (ALPHA27, PART, ZoomLadder, letter, letter_bars, letter_row, load, tt)


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
                            part=PART)
        with self.voiceover("Chapter one. Before we can score a guess, we need a way to write one down.") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def frequencies(self):
        d = load("letters")
        corpus = load("corpus")
        p = d["p"]
        n = int(d["n"])
        nb = int(corpus["n_books"])
        g = letter_bars(p, width=12.0, height=3.4, base=(0, -2.3))
        head = label(rf"${n:,}$ symbols from ${nb}$ novels".replace(",", "{,}"), font_size=34).to_edge(UP, buff=0.45)
        sub = label(r"$26$ letters and the space; \ capitals and punctuation dropped", font_size=24,
                    color=GREY_B).next_to(head, DOWN, buff=0.18)
        books = VGroup(*[label(rf"\textit{{{t}}}", font_size=24, color=GREY_A) for t in corpus["titles"][:10]])
        books.arrange_in_grid(rows=5, cols=2, buff=(0.6, 0.16), col_alignments="ll").move_to(DOWN * 0.4)
        more = label(rf"\ldots\ and ${nb - 10}$ more", font_size=24, color=GREY_B).next_to(books, DOWN, buff=0.3)
        order = [int(i) for i in d["order"]]
        first, second = order[0], order[1]
        sp_val = MathTex(f"{p[first]:.3f}", font_size=26, color=C.TRUE_P).next_to(g.bars[first], UP, buff=0.1)
        e_val = MathTex(f"{p[second]:.3f}", font_size=26, color=C.TRUE_P).next_to(g.bars[second], UP, buff=0.1)

        def sym_name(i):
            return "the space" if ALPHA27[i] == " " else ALPHA27[i]

        with self.voiceover(
            f"Take {nb} novels, from Pride and Prejudice to The Great Gatsby, and count every symbol: Shannon's "
            "alphabet of twenty-six letters and the space, capitals and punctuation dropped. That's "
            f"<bookmark mark='a'/> {n / 1e6:.1f} million symbols. <bookmark mark='b'/> The most common is "
            f"{sym_name(first)}, about one symbol in {round(1 / p[first])}. Then {sym_name(second)}, one in "
            f"{round(1 / p[second])}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), LaggedStart(*[FadeIn(b) for b in books], lag_ratio=0.1), FadeIn(more))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in g.bars], lag_ratio=0.05), FadeIn(g.labels),
                      FadeOut(books), FadeOut(more), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(sp_val), Indicate(g.bars[first], color=WHITE))
            self.play(FadeIn(e_val))
        # sort by frequency
        slot = g.slot
        anims = []
        for k, i in enumerate(order):
            x = g.x0 + (k + 0.5) * slot
            anims += [g.bars[i].animate.set_x(x), g.labels[i].animate.set_x(x)]
        top6 = ", ".join("space" if ALPHA27[i] == " " else ALPHA27[i] for i in order[:6])
        rarest = order[-1]
        with self.voiceover(
            f"Sorted, the familiar order appears: {top6}. <bookmark mark='z'/> The rarest, {ALPHA27[rarest]}, turns "
            f"up about once in {round(1 / p[rarest], -2):,.0f} symbols."
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
            "This is a probability distribution: a number for each possibility, <bookmark mark='a'/> none "
            "negative, adding up to one. <bookmark mark='b'/> Stack the bars end to end, and they fill a bar of "
            "length one, a sliver per symbol, as wide as its probability. A guess, written down, shares one unit "
            "of belief among the possibilities."
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
        cell = 0.2
        x0, y0 = -6.2, 2.45  # top-left corner of the grid
        grid = VGroup()
        for i in range(27):
            for j in range(27):
                v = float(np.sqrt(cond[i, j]))
                col = interpolate_color(ManimColor("#151B26"), ManimColor(C.TRUE_P), min(1.0, v * 1.6))
                if v > 0.75:
                    col = interpolate_color(ManimColor(C.TRUE_P), ManimColor(WHITE), (v - 0.75) * 4)
                grid.add(Square(side_length=cell, stroke_width=0, fill_color=col, fill_opacity=1)
                         .move_to([x0 + (j + 0.5) * cell, y0 - (i + 0.5) * cell, 0]))
        rows = VGroup(*[letter(ALPHA27[i], font_size=15, color=GREY_B).move_to([x0 - 0.15, y0 - (i + 0.5) * cell, 0])
                        for i in range(27)])
        cols = VGroup(*[letter(ALPHA27[j], font_size=15, color=GREY_B).move_to([x0 + (j + 0.5) * cell, y0 + 0.15, 0])
                        for j in range(27)])
        rl = label(r"previous", font_size=20, color=GREY_B)
        if not zh():  # Chinese reads top to bottom unrotated (the table sets it as a vertical stack)
            rl.rotate(PI / 2)
        rl.next_to(rows, LEFT, buff=0.12)
        cl = label(r"next", font_size=20, color=GREY_B).next_to(cols, UP, buff=0.1)
        qi, ui, ti, hi = (ALPHA27.index(c) for c in "quth")
        head = label(r"$P(\text{next} \mid \text{previous})$ \ for every pair of symbols", font_size=30)
        head.move_to([2.6, 3.3, 0])
        row_note = VGroup(label(r"each row: \ one distribution over the next symbol", font_size=26, color=GREY_A),
                          label(r"brighter $=$ more likely", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.2)
        row_note.move_to([3.6, 0.2, 0])
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
        b_w = brace_note(out, rf"$P(A) = P(\texttt{{t}}) = {p1[ti]:.3f}$", DOWN, color=C.CONTEXT, font_size=24)
        b_h = Brace(out[hi], RIGHT, buff=0.42, color=C.INTERVAL)
        b_h_l = label(rf"$P(B \mid A) = {cond[ti, hi]:.3f}$", font_size=24, color=C.INTERVAL).next_to(b_h, RIGHT,
                                                                                                    buff=0.1)
        area = label(r"area in the square: \ $P(A \text{ and } B)$", font_size=24, color=C.BITS)
        area.next_to(f_def, DOWN, buff=0.45)
        lit_cell = cells[ti * 27 + hi].copy().set_fill(C.BITS, opacity=1)
        with self.voiceover(
            "But we rarely guess from nothing. Once you know the previous letter, the odds change. <bookmark mark='a'/> "
            "Here is the whole table: each row is a previous symbol, each square how likely the next one is. "
            "<bookmark mark='d'/> This is conditional probability: B given A is the probability of both, divided "
            "by that of A."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(grid[i * 27:(i + 1) * 27]) for i in range(27)], lag_ratio=0.08),
                      FadeIn(rows), FadeIn(cols), FadeIn(rl), FadeIn(cl), run_time=2.5)
            self.play(FadeIn(row_note))
            vo.wait_until("d")
            self.play(*[ReplacementTransform(grid[k], cells[k]) for k in range(729)], FadeOut(rows), FadeOut(cols),
                      FadeOut(rl), FadeOut(cl), FadeOut(row_note), run_time=2.2)
            self.play(FadeIn(mlabs), FadeIn(mcap), FadeIn(lit_cell))
            self.show_pull(pt)
            self.play(Write(f_def), FadeIn(b_w), GrowFromCenter(b_h), FadeIn(b_h_l))
            self.play(FadeIn(area), Indicate(lit_cell, color=WHITE, scale_factor=2.5))
        n_q = int(load("letters")["counts"][qi])
        n_qu = int(round(float(joint[qi, ui]) * int(load("letters")["n"])))
        q_u = float(b["q_u"])
        f_qu = mtex(r"P(" + tt("u") + r" \mid " + tt("q") + rf") = \frac{{{n_qu:,}}}{{{n_q:,}}} = {q_u:.4f}"
                    .replace(",", "{,}"), font_size=36, color=WHITE).move_to([3.7, 1.9, 0])
        cap_q = label(r"after \texttt{q}, almost surely \texttt{u}", font_size=28, color=C.BITS).next_to(f_qu, DOWN,
                                                                                                    buff=0.4)
        cap_sp = label(r"after a space, almost anything:\\ a word is starting", font_size=28, color=C.CONTEXT)
        cap_sp.move_to([4.2, -1.0, 0])
        pq = self.pull(cells, qi, cond, lit=(ui,))
        q_col = VGroup(*cells[qi * 27:(qi + 1) * 27])
        q_arrow = Arrow(q_col.get_bottom() + DOWN * 0.9, q_col.get_bottom() + DOWN * 0.05, buff=0, color=C.CONTEXT,
                        stroke_width=3, max_tip_length_to_length_ratio=0.25)
        q_name = letter("q", font_size=26, color=C.CONTEXT).next_to(q_arrow, DOWN, buff=0.05)
        ps = self.pull(cells, 0, cond, min_label=0.2)
        with self.voiceover(
            f"In our books, q appears {n_q:,} times, and all but {n_q - n_qu:,} are followed by u. "
            f"<bookmark mark='a'/> So u given q is {q_u:.4f}. "
            "<bookmark mark='b'/> After a space, though, almost anything can come next: a new word is starting."
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
        assert abs(ch["p_the"] - pt_ * ph * pe) < 1e-12
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
            if e.width > 6.6:
                e.width = 6.6
            e.move_to([3.2, 3.2, 0])
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
        num = mtex(rf"P(\texttt{{the}}) = {pt_:.3f} \times {ph:.3f} \times {pe:.3f} = {ch['p_the']:.4f}", font_size=30)
        num.move_to([3.6, -2.7, 0])
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
            "And so on, one symbol at a time. <bookmark mark='a'/> A whole text's probability is a product of "
            "next-symbol guesses, each knowing everything before it. This is the chain rule, and it is exact: no "
            "assumption made. <bookmark mark='b'/> It's why a machine that only guesses the next symbol can score, "
            "or write, a whole text."
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
        ps = [s["p"] for s in steps[:3]]
        cx = [s["context"] for s in steps[:3]]
        lad = ZoomLadder(steps, W=8.8, x=-0.5)
        ys = [2.0, 0.55, -0.9]
        head = label(r"he said\ \ldots \quad $P(" + tt("the") + r")$ one letter at a time", font_size=32)
        head.to_edge(UP, buff=0.35)
        rows = [lad.row(k, ys[k]) for k in range(3)]
        funnels = [lad.funnel(k, ys[k], ys[k + 1]) for k in range(2)]
        tex = [r"P(" + tt(c) + r" \mid " + tt(x) + rf") = {v:.3f}" for c, x, v in zip("the", cx, ps)]
        reads = [mtex(t, font_size=26, color=C.INTERVAL) for t in tex]
        for r, y in zip(reads, ys):
            r.move_to([4.25, y, 0], aligned_edge=LEFT)
        ctxs = VGroup(*[label(tt(s["context"]), font_size=24, color=C.CONTEXT).move_to([-5.7, y, 0])
                        for s, y in zip(steps[:3], ys)])
        ctx_head = label(r"context", font_size=20, color=GREY_B).next_to(ctxs[0], UP, buff=0.3)
        pr = float(np.prod(ps))
        prod = mtex(r"P(" + tt("the") + r" \mid " + tt(cx[0]) + rf") = {ps[0]:.3f} \times {ps[1]:.3f} \times "
                    rf"{ps[2]:.3f} = {pr:.4f}", font_size=34, color=WHITE).move_to(DOWN * 2.35)
        note_ctx = note(r"context: the last three symbols (an order-3 counting model of the $30$ books)")
        note_ctx.to_edge(DOWN, buff=0.3)
        q_row = VGroup(letter_row("he said ", font_size=44),
                       *[VGroup(Square(0.62, stroke_color=C.INTERVAL, stroke_width=2.5),
                                letter(c, font_size=44, color=C.INTERVAL)) for c in "the"]).arrange(RIGHT, buff=0.12)
        for sq_ in q_row[1:]:
            sq_[1].move_to(sq_[0])
        q_row.move_to(UP * 0.4)
        q_cap = label(r"how likely are the next three letters to be \texttt{t}, \texttt{h}, \texttt{e}?", font_size=28,
                      color=GREY_A).next_to(q_row, DOWN, buff=0.45)
        with self.voiceover(
            "Here's the chain rule as a picture. Someone has written, he said, and we want the chance that the "
            "next three letters are t, h, e. <bookmark mark='a'/> The first bar shares the whole unit of belief "
            "among the 27 next symbols, given the last three: i, d, space. t gets a sliver "
            f"{ps[0]:.3f} wide."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note_ctx), FadeIn(q_row[0]))
            self.play(LaggedStart(*[FadeIn(sq_, shift=UP * 0.15) for sq_ in q_row[1:]], lag_ratio=0.3), FadeIn(q_cap))
            vo.wait_until("a")
            self.play(FadeOut(q_row), FadeOut(q_cap), run_time=0.5)
            self.play(FadeIn(rows[0][0]), Create(rows[0][2]), FadeIn(ctxs[0]), FadeIn(ctx_head))
            self.play(FadeIn(rows[0][1]), FadeIn(reads[0]))
        with self.voiceover(
            "Now zoom into that sliver and share it out again, <bookmark mark='a'/> by the probabilities after d, "
            f"space, t. h takes {100 * ps[1]:.0f} percent of it. <bookmark mark='b'/> Zoom again: after space, t, h, "
            f"e takes {100 * ps[2]:.0f} percent. <bookmark mark='c'/> The final sliver's width is the product, "
            f"{pr:.4f}: the probability of the whole string."
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
            "Keep this picture in mind: nested slivers, each one a guess. In chapter eight, it becomes a way to "
            "compress text."
        ) as vo:
            self.play(Indicate(prod, color=C.INTERVAL), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()
