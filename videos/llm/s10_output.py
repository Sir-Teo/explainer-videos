from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.llm.common import (
    PROMPT, Mono, Plot, ProbBars, data, display_token, label, load_arrays, random_values, show_chapter_card, softmax,
    token_row, vector_strip, wrap_text,
)


class NextToken(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 9, "From a vector to a prediction")
        self.d = data()
        self.arrays = load_arrays("gpt2_small")
        self.unembed()
        self.logit_lens()
        self.temperature()
        self.samples()

    # ------------------------------------------------------------------
    def unembed(self):
        f = self.d["final"]
        toks, logits, probs = f["tokens"][:8], f["logits"][:8], f["probs"][:8]
        assert toks[0] == " Paris" and -100 < logits[0] < -90
        pieces = self.d["tokenize"][PROMPT + " Paris."]["pieces"][:-2]
        row = token_row(pieces, font_size=24, buff=0.08).to_edge(UP, buff=0.35)
        last = row[-1]
        vec = vector_strip(random_values(10, seed=4), color=C.EMBED, cell=0.22).move_to(LEFT * 6.2 + DOWN * 0.6)
        vlab = label(r"final vector\\at ``of''", font_size=28, color=C.EMBED).next_to(vec, DOWN, buff=0.2)
        after = label(r"(after all 12 blocks and a final layer norm)", font_size=24, color=GREY_A)
        after.next_to(row, DOWN, buff=0.2).align_to(row, RIGHT)

        with self.voiceover(
            "At the top of the stack, take the vector at the last position, the one for 'of'. <bookmark mark='v'/> By now, "
            "it has absorbed information from the whole prompt. After one last layer norm, it's time to turn it into a "
            "prediction."
        ) as vo:
            self.play(FadeIn(row), last.animate.set_color(YELLOW))
            vo.wait_until("v")
            self.play(TransformFromCopy(last, vec), FadeIn(vlab), FadeIn(after))

        # Unembedding matrix: one row per vocabulary token.
        rows = VGroup()
        for t in toks[:5] + ["..."] + [" zebra", " the"]:
            if t == "...":
                rows.add(MathTex(r"\vdots", font_size=30, color=GREY_B))
            else:
                rows.add(Mono(display_token(t), font_size=24))
        cells = VGroup()
        rng = np.random.default_rng(1)
        for r in rows:
            if isinstance(r, MathTex):
                cells.add(VectorizedPoint())
                continue
            cells.add(VGroup(*[Square(0.18, stroke_width=0, fill_color=C.PROB,
                                      fill_opacity=min(0.95, 0.1 + abs(rng.normal(0, 0.45)))) for _ in range(10)])
                      .arrange(RIGHT, buff=0.03))
        rows.arrange(DOWN, buff=0.22, aligned_edge=RIGHT).move_to(LEFT * 4.3 + DOWN * 0.6)
        for r, c in zip(rows, cells):
            c.next_to(r, RIGHT, buff=0.2).set_y(r.get_y())
        cells.align_to(cells[0], LEFT)
        mframe = SurroundingRectangle(VGroup(*[c for c in cells if len(c)]), color=C.PROB, buff=0.08, stroke_width=2)
        wl = MathTex(r"W_U", font_size=40, color=C.PROB).next_to(mframe, UP, buff=0.15)
        tied = label(r"one row per token: 50{,}257 rows\\(GPT-2 reuses the embedding table)", font_size=24, color=GREY_A)
        tied.next_to(mframe, DOWN, buff=0.2).shift(LEFT * 0.4)
        lg = VGroup()
        shown = list(logits[:5]) + [None, None, None]
        for r, z in zip(rows, shown):
            if z is None:
                m = MathTex(r"\vdots" if isinstance(r, MathTex) else r"\cdots", font_size=30, color=GREY_B)
            else:
                m = DecimalNumber(z, num_decimal_places=2, font_size=28, color=C.PROB)
            m.move_to([mframe.get_right()[0] + 0.9, r.get_y(), 0])
            lg.add(m)
        lg_l = label(r"logits", font_size=30, color=C.PROB).next_to(lg, UP, buff=0.3).set_y(wl.get_y())
        with self.voiceover(
            "The vector is compared, by dot product, <bookmark mark='m'/> with a vector for every token in the vocabulary. "
            "GPT-2 simply reuses its embedding table for this. <bookmark mark='l'/> The result is 50,257 scores, called "
            "logits, one for each possible next token."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(rows), FadeIn(cells, lag_ratio=0.02), Create(mframe), FadeIn(wl), FadeIn(tied))
            vo.wait_until("l")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in lg], lag_ratio=0.1), FadeIn(lg_l))

        bars = ProbBars(toks, probs, max_width=2.4, scale_max=0.1, font_size=26, highlight=" Paris")
        bars.move_to(RIGHT * 4.5 + DOWN * 0.6)
        sm_arrow = Arrow(lg.get_right() + RIGHT * 0.15, bars.get_left() + LEFT * 0.1, buff=0.05, color=C.ATTN)
        sm = label(r"softmax", font_size=30, color=C.ATTN).next_to(sm_arrow, UP, buff=0.1)
        shift = MathTex(r"\softmax(\vec z + c) = \softmax(\vec z)", font_size=32, color=GREY_A)
        shift.move_to(RIGHT * 3.8 + DOWN * 3.35)
        with self.voiceover(
            "Here, GPT-2's raw logits all happen to sit around minus 95. <bookmark mark='d'/> That doesn't matter: adding the same "
            "number to every score doesn't change softmax, so only the differences count. <bookmark mark='s'/> Softmax turns "
            "them into probabilities, and Paris comes out on top, at about six percent."
        ) as vo:
            vo.wait_until("d")
            self.play(Write(shift))
            vo.wait_until("s")
            self.play(GrowArrow(sm_arrow), FadeIn(sm))
            self.play(FadeIn(bars.labels), LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars.bars], lag_ratio=0.08),
                      FadeIn(bars.pcts))

        every = label(r"(every position makes a prediction like this, for the token after it)", font_size=26, color=GREY_A)
        every.to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In fact, every position in the sequence makes a prediction like this, for the token that follows it. To "
            "generate text we only need the last one; during training, as we'll see, all of them are used."
        ) as vo:
            self.play(FadeOut(VGroup(shift, tied)), FadeIn(every))
            self.play(*[Indicate(t, color=C.PROB, scale_factor=1.1) for t in row], run_time=1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def logit_lens(self):
        lens = self.d["logit_lens"]
        ranks = [r["target_rank"] for r in lens]
        assert ranks[0] > 10000 and ranks[9] < 20 and ranks[10] == 2 and ranks[11] == 1 and ranks[12] == 1
        title = label(r"The logit lens: decode the residual stream after every layer", font_size=34).to_edge(UP, buff=0.35)
        head = VGroup(label(r"after layer", font_size=26, color=GREY_A), label(r"top guess", font_size=26, color=GREY_A),
                      label(r"rank of Paris", font_size=26, color=GREY_A))
        xs = [-5.6, -3.6, -1.1]
        y0, dy = 2.35, 0.43
        for h, x in zip(head, xs):
            h.move_to([x, y0, 0])
        table = VGroup()
        for i, r in enumerate(lens):
            y = y0 - (i + 1) * dy
            top = r["top"][0][0]
            hit = top == " Paris"
            cells = VGroup(
                MathTex(str(r["layer"]) if r["layer"] else r"0\ (\text{embedding})", font_size=26).move_to([xs[0], y, 0]),
                Mono(display_token(top), font_size=24, color=YELLOW if hit else WHITE).move_to([xs[1], y, 0]),
                MathTex(f"{r['target_rank']:,}".replace(",", "{,}"), font_size=26,
                        color=YELLOW if r["target_rank"] == 1 else WHITE).move_to([xs[2], y, 0]),
            )
            table.add(cells)
        pl = Plot((0, 12), (0, 5), width=5.0, height=4.6, x_ticks=[0, 3, 6, 9, 12], y_ticks=[0, 1, 2, 3, 4],
                  y_fmt=lambda v: {0: "10{,}000", 1: "1{,}000", 2: "100", 3: "10", 4: "1"}[v]).move_to(RIGHT * 3.7 + DOWN * 0.3)
        yv = [4 - np.log10(r) for r in ranks]
        curve = pl.line(range(13), yv, YELLOW, 4)
        dots = pl.dots(range(13), yv, YELLOW)
        pll = label(r"rank of ``Paris''", font_size=28, color=YELLOW).next_to(pl, UP, buff=0.25)
        xl = label(r"layer", font_size=26, color=GREY_A).next_to(pl, DOWN, buff=0.5)

        with self.voiceover(
            "Here's a fun trick, called the logit lens. Nothing stops us from applying this final step early, to the "
            "residual stream after any layer, and asking: what would the model predict right now? <bookmark mark='e'/> After "
            "the embedding alone, Paris sits at rank 22,947. <bookmark mark='t'/> The early layers mostly guess 'the'."
        ) as vo:
            self.play(FadeIn(title), FadeIn(head), Create(pl), FadeIn(pll), FadeIn(xl))
            vo.wait_until("e")
            self.play(FadeIn(table[0]), FadeIn(dots[0]))
            vo.wait_until("t")
            self.play(LaggedStart(*[FadeIn(table[i]) for i in range(1, 6)], lag_ratio=0.3),
                      Create(pl.line(range(6), yv[:6], YELLOW, 4)), FadeIn(dots[1:6]), run_time=2)

        with self.voiceover(
            "Around the middle, <bookmark mark='p'/> place names start to appear: England, Rome. <bookmark mark='a'/> After "
            "layer 9, Paris is 13th; <bookmark mark='b'/> after layer 10, second; <bookmark mark='c'/> after layer 11, first. "
            "You can watch the answer take shape, layer by layer."
        ) as vo:
            vo.wait_until("p")
            self.play(LaggedStart(*[FadeIn(table[i]) for i in range(6, 9)], lag_ratio=0.3), FadeIn(dots[6:9]), run_time=1.5)
            for i, m in zip(range(9, 12), "abc"):
                vo.wait_until(m)
                self.play(FadeIn(table[i]), FadeIn(dots[i]), run_time=0.6)
            self.play(FadeIn(table[12]), FadeIn(dots[12]), Create(curve), run_time=1.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def temperature(self):
        z = self.arrays["temp_logits"].astype(np.float64)
        top = self.d["temp_tokens"]
        ids, pieces = top["ids"][:10], top["pieces"][:10]
        T = ValueTracker(1.0)

        def probs():
            return softmax(z, T.get_value())[ids]

        prompt = Mono(self.d["temp_prompt"] + " ...", font_size=30).to_edge(UP, buff=0.5)
        bars = ProbBars(pieces, probs(), max_width=4.6, scale_max=0.4, font_size=26).move_to(LEFT * 3.2 + DOWN * 0.5)
        bars.add_updater(lambda b: b.set_probs(probs()))
        tr = VGroup(MathTex("T =", font_size=48), DecimalNumber(1.0, num_decimal_places=2, font_size=48))
        tr.arrange(RIGHT, buff=0.2).move_to(RIGHT * 4.4 + UP * 1.2)
        tr[1].add_updater(lambda d: d.set_value(T.get_value()))
        form = MathTex(r"p_i", "=", r"{e^{\,z_i / T} \over \sum_j e^{\,z_j / T}}", font_size=44).next_to(tr, DOWN, buff=0.5)
        form[0].set_color(C.PROB)
        note = label(r"top 10 of 50{,}257 tokens", font_size=24, color=GREY_A).next_to(bars, DOWN, buff=0.3)
        with self.voiceover(
            "To generate text, we have to pick a token from these probabilities. <bookmark mark='p'/> Here's GPT-2's "
            "distribution after a more open-ended prompt: once upon a time, there was a... <bookmark mark='g'/> Always "
            "picking the top choice is called greedy decoding."
        ) as vo:
            vo.wait_until("p")
            self.play(FadeIn(prompt), FadeIn(bars), FadeIn(note))
            vo.wait_until("g")
            self.play(Indicate(bars.row(0), color=YELLOW))

        greedy = wrap_text(self.d["sampling"]["greedy"], width=26, font_size=24, max_lines=6)
        assert "great wealth and power. He was a man of great wealth" in self.d["sampling"]["greedy"]
        gl = label(r"greedy decoding:", font_size=30, color=YELLOW)
        gg = VGroup(gl, greedy).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to(RIGHT * 4.3 + DOWN * 0.4)
        with self.voiceover(
            "But greedy decoding tends to get stuck in loops: <bookmark mark='l'/> a man who was a man of great wealth and "
            "power. He was a man of great wealth and power. He was a man of great wealth and power..."
        ) as vo:
            self.play(FadeOut(note))
            vo.wait_until("l")
            self.play(FadeIn(gg, shift=UP * 0.2))
        self.play(FadeOut(gg))

        with self.voiceover(
            "So instead, we usually sample at random, in proportion to the probabilities, after first dividing every logit "
            "by a number called the temperature. <bookmark mark='c'/> A temperature below one sharpens the distribution "
            "toward the top choices. <bookmark mark='h'/> Above one, it flattens it out, giving unlikely tokens more of a "
            "chance."
        ) as vo:
            self.play(FadeIn(tr), Write(form))
            vo.wait_until("c")
            self.play(T.animate.set_value(0.5), run_time=2.5)
            vo.wait_until("h")
            self.play(T.animate.set_value(2.0), run_time=3)
            self.play(T.animate.set_value(1.0), run_time=1.5)
        bars.clear_updaters()
        tr[1].clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def samples(self):
        s = self.d["sampling"]["samples"]
        prompt = Mono(self.d["temp_prompt"] + " ...", font_size=30).to_edge(UP, buff=0.5)
        blocks = VGroup()
        for t, col in (("0.7", C.PROB), ("1.0", YELLOW), ("1.6", RED)):
            lab = MathTex(rf"T = {t}", font_size=36, color=col)
            body = wrap_text(s[t], width=60, font_size=24, max_lines=3)
            blocks.add(VGroup(lab, body).arrange(RIGHT, buff=0.4, aligned_edge=UP))
        blocks.arrange(DOWN, buff=0.55, aligned_edge=LEFT).move_to(DOWN * 0.3)
        tag = label(r"real samples from GPT-2 small (same random seed)", font_size=24, color=GREY_B).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here are real samples from GPT-2. <bookmark mark='a'/> At a temperature of 0.7, it writes about a bright star in "
            "the sky. <bookmark mark='b'/> At 1, it gets more surprising. <bookmark mark='c'/> At 1.6, the long tail of "
            "unlikely tokens takes over, and it dissolves into word salad. Many applications use temperatures somewhere "
            "between about 0.7 and 1."
        ) as vo:
            self.play(FadeIn(prompt), FadeIn(tag))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(blocks[i][0]), AddTextLetterByLetter(VGroup(*[g for ln in blocks[i][1] for g in ln.glyphs]),
                                                                      time_per_char=0.01), run_time=1.5)
        self.clear_scene()
