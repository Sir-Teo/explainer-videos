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
    def conditional(self):
        b = load("bigram")
        cond = b["cond"]
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
        qi, ui = ALPHA27.index("q"), ALPHA27.index("u")
        assert b["q_u"] > 0.998
        q_row = SurroundingRectangle(VGroup(*grid[qi * 27:(qi + 1) * 27]), color=C.CONTEXT, buff=0.02, stroke_width=2.5)
        q_u = SurroundingRectangle(grid[qi * 27 + ui], color=C.BITS, buff=0.03, stroke_width=3)
        sp_row = SurroundingRectangle(VGroup(*grid[0:27]), color=C.CONTEXT, buff=0.02, stroke_width=2.5)
        head = label(r"$P(\text{next} \mid \text{previous})$ \ for every pair of symbols", font_size=30)
        head.move_to([2.6, 3.3, 0])
        f_def = mtex(r"P(B \mid A) = \frac{P(A \text{ and } B)}{P(A)}", font_size=40).move_to([2.6, 1.9, 0])
        f_qu = mtex(r"P(" + tt("u") + r" \mid " + tt("q") + r") = \frac{18{,}469}{18{,}496} = 0.9985", font_size=36,
                    color=WHITE).move_to([2.6, 0.4, 0])
        n_q = int(load("letters")["counts"][qi])
        assert n_q == 18496 and round(float(b["joint"][qi, ui]) * int(load("letters")["n"])) == 18469
        f_qu[0].set_color(WHITE)
        cap_q = label(r"after \texttt{q}, almost surely \texttt{u}", font_size=26, color=C.BITS).move_to([2.6, -0.5, 0])
        cap_sp = label(r"after a space, almost anything: \ a word is starting", font_size=26, color=C.CONTEXT)
        cap_sp.move_to([2.6, -1.5, 0])
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
            self.play(Write(f_def))
        with self.voiceover(
            "In our books, q appears eighteen thousand, four hundred and ninety-six times, and all but twenty-seven "
            "of them are followed by u. <bookmark mark='a'/> So the probability of u, given q, is 0.9985. "
            "<bookmark mark='b'/> After a space, on the other hand, almost anything can come next: a new word is "
            "starting."
        ) as vo:
            self.play(Create(q_row))
            vo.wait_until("a")
            self.play(Create(q_u), Write(f_qu), FadeIn(cap_q))
            vo.wait_until("b")
            self.play(ReplacementTransform(q_row, sp_row), FadeIn(cap_sp))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def chain_rule(self):
        rows = [
            mtex([r"P(x_1, x_2)", r"=", r"P(x_1)\,", r"P(x_2 \mid x_1)"]),
            mtex([r"P(x_1, x_2, x_3)", r"=", r"P(x_1, x_2)\,", r"P(x_3 \mid x_1, x_2)"]),
            mtex([r"P(x_1, x_2, x_3)", r"=", r"P(x_1)\, P(x_2 \mid x_1)\,", r"P(x_3 \mid x_1, x_2)"]),
            mtex([r"P(x_1, \dots, x_n)", r"=", r"\prod_{i=1}^{n}", r"P(x_i \mid x_1, \dots, x_{i-1})"],
                 font_size=44),
        ]
        whys = [why(r"the definition, multiplied out"), why(r"the same, with $(x_1, x_2)$ as $A$"),
                why(r"the first line, substituted"), why(r"and so on, one symbol at a time")]
        step = ladder(self, rows, whys, keep=4, top=2.6)
        head = label(r"The chain rule", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Multiply that definition out, and you get a rule for whole strings. <bookmark mark='a'/> The "
            "probability of two symbols is the probability of the first, times the probability of the second given "
            "the first. <bookmark mark='b'/> For three, treat the first two as a single event, <bookmark mark='c'/> "
            "and substitute."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
        cap = label(r"exact, for any distribution: \ no assumption has been made", font_size=28, color=C.BITS)
        cap2 = label(r"a text's probability $=$ a product of next-symbol guesses", font_size=28, color=GREY_A)
        with self.voiceover(
            "And so on, one symbol at a time. <bookmark mark='a'/> The probability of a whole text is a product of "
            "next-symbol guesses, each made knowing everything before it. This is the chain rule, and it is exact: "
            "no assumption has been made. <bookmark mark='b'/> It is also why a machine that only ever guesses the "
            "next symbol can score, or write, an entire text."
        ) as vo:
            step(3)
            box = SurroundingRectangle(rows[3], color=C.BITS, buff=0.2, corner_radius=0.1)
            cap.next_to(box, DOWN, buff=0.35)
            cap2.next_to(cap, DOWN, buff=0.25)
            self.play(FadeOut(whys[3]), Create(box))
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
