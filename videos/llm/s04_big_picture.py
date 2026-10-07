from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.llm.common import (
    Plot, TokenBox, attention_arcs, block, data, label, random_values, show_chapter_card, token_row, vector_strip,
)

N_CELLS = 6


def words(s: str) -> list[str]:
    w = s.split(" ")
    return [w[0]] + [" " + x for x in w[1:]]


def strip(seed, color=C.EMBED, cell=0.17):
    return vector_strip(random_values(N_CELLS, seed=seed), color=color, cell=cell, gap=0.03)


class BigPicture(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 3, "The plan: refine every vector with context")
        self.d = data()
        self.same_vector()
        self.architecture()
        self.drift()

    # ------------------------------------------------------------------
    def same_vector(self):
        river, _, money = self.d["bank"]["sentences"]
        rows = VGroup(token_row(words(river), font_size=30, buff=0.1), token_row(words(money), font_size=30, buff=0.1))
        # GPT-2 tokenizes both sentences into exactly these words, with "bank" at the same position.
        assert self.d["bank_head"]["pieces"] == words(river)
        rows.arrange(DOWN, buff=2.2, aligned_edge=RIGHT).move_to(LEFT * 1.0 + DOWN * 0.6)
        banks = VGroup(rows[0][-1], rows[1][-1])
        vecs = VGroup(*[strip(7, cell=0.2).next_to(b, UP, buff=0.25) for b in banks])
        eq = MathTex(r"=", font_size=60).move_to(VGroup(*vecs).get_center() + RIGHT * 1.6)
        same = label(r"identical vectors", font_size=32, color=YELLOW).next_to(eq, RIGHT, buff=0.3)

        with self.voiceover(
            "But there's a problem. In <bookmark mark='a'/> 'we walked along the river bank', and <bookmark mark='b'/> "
            "'we deposited cash at the bank', <bookmark mark='c'/> the token bank gets exactly the same vector, because "
            "there's only one entry for it in the table."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows[0], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], lag_ratio=0.1))
            vo.wait_until("c")
            self.play(banks.animate.set_color(YELLOW), *[FadeIn(v, shift=UP * 0.2) for v in vecs])
            self.play(Write(eq), FadeIn(same))

        mean = VGroup(label(r"land beside water", font_size=30, color=GREY_A), label(r"a place for money", font_size=30, color=GREY_A))
        for m, r in zip(mean, rows):
            m.next_to(r, DOWN, buff=0.3).align_to(r, RIGHT)
        with self.voiceover(
            "Its meaning, though, depends on the words around it: <bookmark mark='r'/> river in one case, "
            "<bookmark mark='m'/> cash in the other. The same is true of nearly every word. The vector from the lookup "
            "table is only a starting point."
        ) as vo:
            vo.wait_until("r")
            self.play(Indicate(rows[0][4], color=YELLOW), FadeIn(mean[0]))
            vo.wait_until("m")
            self.play(Indicate(rows[1][2], color=YELLOW), FadeIn(mean[1]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def architecture(self):
        pieces = self.d["bank_head"]["pieces"]
        row = token_row(pieces, font_size=26, buff=0.35).to_edge(DOWN, buff=0.35).set_x(-2.6)
        xs = [t.get_x() for t in row]
        y_layers = [-2.15, 0.15, 2.45]
        stacks = [VGroup(*[strip(10 * k + i).move_to([x, y, 0]) for i, x in enumerate(xs)]) for k, y in enumerate(y_layers)]
        bw = row.width + 0.8
        attn = block("", C.ATTN, width=bw, height=0.62).move_to([row.get_x(), -1.0, 0])
        mlp_boxes = VGroup(*[RoundedRectangle(width=0.62, height=0.62, corner_radius=0.1, stroke_color=C.MLP, stroke_width=2,
                                              fill_color=C.MLP, fill_opacity=0.18).move_to([x, 1.3, 0]) for x in xs])
        attn_l = label(r"attention", font_size=32, color=C.ATTN).next_to(attn, RIGHT, buff=0.3)
        mlp_l = label(r"MLP", font_size=32, color=C.MLP).next_to(mlp_boxes, RIGHT, buff=0.3)
        mlp_l.set_x(attn_l.get_x(), direction=LEFT)
        attn_note = label(r"vectors exchange information", font_size=26, color=GREY_A).next_to(attn_l, DOWN, buff=0.12)
        attn_note.align_to(attn_l, LEFT)
        mlp_note = label(r"each vector processed on its own", font_size=26, color=GREY_A).next_to(mlp_l, DOWN, buff=0.12)
        mlp_note.align_to(mlp_l, LEFT)
        up = VGroup(*[Arrow(row[i].get_top(), stacks[0][i].get_bottom(), buff=0.05, color=GREY_B, stroke_width=2,
                            max_tip_length_to_length_ratio=0.3) for i in range(len(xs))])

        with self.voiceover(
            "That's what the rest of the network is for. Start with each token's vector. <bookmark mark='a'/> In a transformer, "
            "these vectors flow upward through a stack of layers. In each layer, there's first an attention step, "
            "<bookmark mark='x'/> where the vectors exchange information with each other."
        ) as vo:
            self.play(FadeIn(row), *[GrowArrow(a) for a in up], FadeIn(stacks[0], shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(attn), FadeIn(attn_l))
            vo.wait_until("x")
            arcs = VGroup(*[attention_arcs(stacks[0], t, np.r_[np.ones(t), 0] / max(t, 1) * 0.6, min_weight=0.01)
                            for t in range(1, len(xs))])
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.15), FadeIn(attn_note), run_time=1.5)
            self.play(FadeOut(arcs), *[TransformFromCopy(stacks[0][i], stacks[1][i], path_arc=0) for i in range(len(xs))],
                      run_time=1.3)

        with self.voiceover(
            "Then comes a step called an MLP, <bookmark mark='m'/> which processes each vector on its own, without looking at "
            "the others."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(mlp_boxes, lag_ratio=0.1), FadeIn(mlp_l), FadeIn(mlp_note))
            self.play(*[TransformFromCopy(stacks[1][i], stacks[2][i]) for i in range(len(xs))], run_time=1.3)

        # Residual: zoom on the last column.
        k = len(xs) - 1
        before = stacks[0][k]
        plus = VGroup(MathTex(r"\vec x", r"+", r"\Delta", font_size=44))
        plus[0][0].set_color(C.EMBED)
        plus[0][2].set_color(C.ATTN)
        plus.move_to(RIGHT * 5.0 + DOWN * 2.6)
        res_l = label(r"the residual stream", font_size=34, color=C.EMBED)
        res_lines = VGroup(*[Line([x, -2.8, 0], [x, 3.2, 0], color=C.EMBED, stroke_width=2).set_opacity(0.35) for x in xs])
        with self.voiceover(
            "Crucially, neither step replaces a vector. Each one computes a small adjustment, <bookmark mark='d'/> and adds it "
            "to the vector that's already there. Because of this, the column of vectors running up through the network is "
            "called <bookmark mark='r'/> the residual stream. Think of it as a shared workspace that every layer reads from "
            "and writes to."
        ) as vo:
            self.play(FadeOut(VGroup(attn_note, mlp_note)))
            vo.wait_until("d")
            self.play(Indicate(before, color=YELLOW), Write(plus))
            vo.wait_until("r")
            res_l.next_to(plus, UP, buff=0.4)
            self.play(FadeIn(res_lines), FadeIn(res_l))

        dots = MathTex(r"\vdots", font_size=48, color=GREY_A).next_to(stacks[2], UP, buff=0.05)
        times = label(r"$\times\,12$ layers in GPT-2 small", font_size=32, color=GREY_A)
        times.next_to(VGroup(attn_l, mlp_l), UP, buff=0.4).align_to(attn_l, LEFT)
        nxt = TokenBox(" ?", font_size=26, color=C.PROB).move_to([xs[-1] + 1.6, 3.5, 0])
        out_arrow = Arrow(stacks[2][-1].get_top(), nxt.get_left(), buff=0.12, color=C.PROB, stroke_width=4)
        with self.voiceover(
            "GPT-2 small repeats this pair of steps <bookmark mark='t'/> 12 times, each layer with its own learned weights. "
            "<bookmark mark='o'/> At the very top, the vector at the last position is used to predict the next token."
        ) as vo:
            vo.wait_until("t")
            self.play(FadeIn(times), FadeIn(dots))
            vo.wait_until("o")
            self.play(GrowArrow(out_arrow), FadeIn(nxt))

        k = 2
        ok = VGroup(*[Line(stacks[0][j].get_top(), stacks[1][k].get_bottom(), color=YELLOW, stroke_width=3)
                      for j in range(k + 1)])
        bad = VGroup(*[DashedLine(stacks[0][j].get_top(), stacks[1][k].get_bottom(), color=RED, stroke_width=2.5)
                       for j in range(k + 1, len(xs))])
        crosses = VGroup(*[MathTex(r"\times", color=RED, font_size=44).move_to(
            interpolate(stacks[0][j].get_top(), stacks[1][k].get_bottom(), 0.35)) for j in range(k + 1, len(xs))])
        rule = label(r"each position may only look at\\itself and earlier positions", font_size=28, color=YELLOW)
        rule.next_to(attn_l, DOWN, buff=0.2).align_to(attn_l, LEFT)
        with self.voiceover(
            "One more rule. When the vectors exchange information, <bookmark mark='c'/> each position may only look at "
            "itself and at positions before it, <bookmark mark='n'/> never after. We'll see why when we get to training."
        ) as vo:
            self.play(FadeOut(VGroup(times, dots, out_arrow, nxt, res_l, plus)),
                      VGroup(stacks[2], mlp_boxes, res_lines).animate.set_opacity(0.25))
            vo.wait_until("c")
            self.play(Create(ok), FadeIn(rule), stacks[1][k].animate.set_stroke(YELLOW, 3))
            vo.wait_until("n")
            self.play(Create(bad), FadeIn(crosses))
        self.clear_scene()

    # ------------------------------------------------------------------
    def drift(self):
        b = self.d["bank"]
        diff, same = b["different"], b["same"]
        assert diff[0] > 0.999 and min(diff) < 0.4 and min(same) > 0.85
        n = len(diff)
        ax = Plot((0, n - 1), (-0.2, 1.0), width=9.0, height=4.6, x_ticks=range(0, n, 2),
                  y_ticks=[0, 0.2, 0.4, 0.6, 0.8, 1.0], y_fmt=lambda v: f"{v:.1f}")
        ax.move_to(LEFT * 0.6 + DOWN * 0.75)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(n - 1, 0), color=GREY_D, stroke_width=1.5)
        xl = label(r"layer", font_size=30, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.55)
        yl = label(r"similarity of the two ``bank'' vectors", font_size=28, color=GREY_A)
        yl.next_to(ax.y_axis, UP, buff=0.2).align_to(ax.y_axis, LEFT).shift(LEFT * 0.4)
        method = label(r"(cosine similarity, after subtracting each layer's average vector)", font_size=22, color=GREY_B)
        method.to_edge(DOWN, buff=0.12).to_edge(RIGHT, buff=0.3)
        p_diff = ax.line(range(n), diff, YELLOW, 5)
        p_same = ax.line(range(n), same, C.EMBED, 5)
        d_diff = ax.dots(range(n), diff, YELLOW)
        d_same = ax.dots(range(n), same, C.EMBED)
        l_diff = label(r"river bank vs.\ cash at the bank", font_size=28, color=YELLOW)
        l_same = label(r"river bank vs.\ another river bank", font_size=28, color=C.EMBED)
        l_same.move_to(ax.c2p(7.5, 1.1))
        l_diff.move_to(ax.c2p(4.6, 0.3))
        title = label(r"Inside GPT-2: the vector at ``bank'', layer by layer", font_size=34).to_edge(UP, buff=0.4)
        sents = label(r"``We walked along the river bank''\quad vs.\quad ``We deposited cash at the bank''", font_size=26,
                      color=GREY_A).next_to(title, DOWN, buff=0.15)

        with self.voiceover(
            "We can watch this happen inside GPT-2. Take the vector at the bank position in each of our two sentences, and "
            "measure how similar they are, using cosine similarity, after each layer. <bookmark mark='s'/> Before the first "
            "layer, they're identical. <bookmark mark='d'/> Then, layer by layer, they drift apart, as each one absorbs its "
            "own context."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sents), Create(ax), FadeIn(zero), FadeIn(xl), FadeIn(yl), FadeIn(method))
            vo.wait_until("s")
            self.play(FadeIn(d_diff[0], scale=2))
            vo.wait_until("d")
            self.play(Create(p_diff), LaggedStart(*[FadeIn(dt) for dt in d_diff[1:]], lag_ratio=0.15), run_time=3,
                      rate_func=linear)
            self.play(FadeIn(l_diff))

        with self.voiceover(
            "For comparison, here's bank in a different sentence that also talks about a river. "
            "<bookmark mark='s'/> Those two stay almost identical all the way up. The network has pulled the two meanings "
            "of bank apart."
        ) as vo:
            vo.wait_until("s")
            self.play(Create(p_same), LaggedStart(*[FadeIn(dt) for dt in d_same], lag_ratio=0.1), run_time=2.5,
                      rate_func=linear)
            self.play(FadeIn(l_same))

        q = label(r"How does ``bank'' know to listen to ``river''?", font_size=44, color=YELLOW).to_edge(UP, buff=0.5)
        with self.voiceover(
            "So the heart of a transformer is this mixing step. How does bank know to pull information from river, "
            "and not from walked? That's the job of attention."
        ) as vo:
            self.play(FadeOut(VGroup(title, sents)), FadeIn(q, shift=DOWN * 0.2))
        self.clear_scene()
