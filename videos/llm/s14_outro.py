from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.llm.common import (
    PROMPT, Plot, ProbBars, attention_grid, data, label, piece_text, random_values, token_row, vector_strip,
)


class Outro(VoiceoverScene):
    def construct(self):
        self.d = data()
        self.pipeline()
        self.learned()

    # ------------------------------------------------------------------
    def pipeline(self):
        d = self.d
        pieces = d["tokenize"][PROMPT + " Paris."]["pieces"][:-2]
        text = piece_text(pieces + [" Paris"], font_size=26).to_edge(UP, buff=0.45)
        n0 = len(pieces)
        prompt = VGroup(*text.pieces[:n0])
        row = token_row(pieces, font_size=20, buff=0.06).move_to(LEFT * 2.7 + DOWN * 3.2)
        strips = VGroup(*[vector_strip(random_values(6, seed=i), color=C.EMBED, cell=0.13, gap=0.025).next_to(t, UP, buff=0.2)
                          for i, t in enumerate(row)])
        pos = VGroup(*[vector_strip(random_values(6, seed=50 + i), color=C.POSITION, cell=0.09, gap=0.02)
                       .next_to(s, RIGHT, buff=0.02).align_to(s, DOWN) for i, s in enumerate(strips)])
        stack = VGroup(*[VGroup(
            Rectangle(width=row.width + 0.3, height=0.2, stroke_color=C.ATTN, stroke_width=1.5, fill_color=C.ATTN, fill_opacity=0.3),
            Rectangle(width=row.width + 0.3, height=0.2, stroke_color=C.MLP, stroke_width=1.5, fill_color=C.MLP, fill_opacity=0.3),
        ).arrange(UP, buff=0.04) for _ in range(4)]).arrange(UP, buff=0.1)
        stack.move_to([row.get_x(), 0, 0]).align_to(strips.get_top() + UP * 0.35, DOWN)
        times = MathTex(r"\times 12", font_size=34, color=GREY_A).next_to(stack, RIGHT, buff=0.2)
        stream = VGroup(*[Line(s.get_top(), [s.get_x(), stack.get_top()[1] + 0.25, 0], color=C.EMBED, stroke_width=1.5)
                          .set_opacity(0.5) for s in strips])
        top_vec = vector_strip(random_values(6, seed=99), color=C.EMBED, cell=0.15)
        top_vec.next_to(stack, UP, buff=0.3).set_x(strips[-1].get_x())
        f = d["final"]
        bars = ProbBars(f["tokens"][:5], f["probs"][:5], max_width=1.8, scale_max=0.1, font_size=22, highlight=" Paris")
        bars.move_to(RIGHT * 5.2).set_y(top_vec.get_y() - 0.4)
        sm = Arrow(top_vec.get_right(), bars.get_left(), buff=0.15, color=C.PROB, stroke_width=3)
        sm_l = label(r"unembed + softmax", font_size=24, color=C.PROB).next_to(sm, UP, buff=0.08)
        back = CurvedArrow(bars.get_top() + UP * 0.15, text.pieces[n0].get_bottom() + DOWN * 0.15, angle=PI / 3,
                           color=YELLOW, stroke_width=3)

        with self.voiceover(
            "Let's put it all together. <bookmark mark='t'/> Text is chopped into tokens. <bookmark mark='v'/> Each token "
            "becomes a vector, plus a vector for its position. <bookmark mark='s'/> Those vectors flow up through a stack of "
            "blocks, where attention lets them share information, the MLPs process what each one holds, and every step adds "
            "to the residual stream."
        ) as vo:
            self.play(FadeIn(prompt))
            vo.wait_until("t")
            self.play(*[TransformFromCopy(text.pieces[i], row[i]) for i in range(n0)], run_time=1.2)
            vo.wait_until("v")
            self.play(FadeIn(strips, shift=UP * 0.2), FadeIn(pos, shift=UP * 0.2))
            vo.wait_until("s")
            self.play(FadeIn(stream), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in stack], lag_ratio=0.15), FadeIn(times),
                      run_time=2)

        with self.voiceover(
            "At the top, <bookmark mark='u'/> the last vector is compared with every token in the vocabulary, and softmax "
            "turns the scores into probabilities. <bookmark mark='p'/> One token is chosen, <bookmark mark='a'/> appended, "
            "and the whole thing runs again."
        ) as vo:
            self.play(FadeIn(top_vec, shift=UP * 0.2))
            vo.wait_until("u")
            self.play(GrowArrow(sm), FadeIn(sm_l), FadeIn(bars))
            vo.wait_until("p")
            self.play(Indicate(bars.row(0), color=YELLOW))
            vo.wait_until("a")
            self.play(Create(back), ReplacementTransform(bars.labels[0].copy(), text.pieces[n0]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def learned(self):
        d = self.d
        bank = attention_grid(np.array(d["bank_head"]["pattern"]), d["bank_head"]["pieces"], cell=0.32, font_size=18,
                              col_labels=False)
        ind = attention_grid(np.array(d["induction_head"]["pattern"]), d["induction_head"]["pieces"], cell=0.17,
                             row_labels=False, col_labels=False)
        ranks = [r["target_rank"] for r in d["logit_lens"]]
        pl = Plot((0, 12), (0, 5), width=3.2, height=2.2, x_ticks=[0, 12], y_ticks=[])
        lens = VGroup(pl, pl.line(range(13), [4 - np.log10(r) for r in ranks], YELLOW, 3))
        panels = VGroup(bank, ind, lens).arrange(RIGHT, buff=1.0).move_to(UP * 0.4)
        caps = VGroup(label(r"``bank'' looks at ``river''", font_size=26, color=GREY_A),
                      label(r"an induction head", font_size=26, color=GREY_A),
                      label(r"``Paris'' rising through the layers", font_size=26, color=GREY_A))
        for c, p in zip(caps, panels):
            c.next_to(p, DOWN, buff=0.3)
        title = label(r"learned, not designed", font_size=44, color=YELLOW).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Here's the part I find most remarkable. None of what we found inside GPT-2, <bookmark mark='a'/> the head that "
            "links bank to river, <bookmark mark='b'/> the induction heads, <bookmark mark='c'/> Paris emerging layer by "
            "layer, was designed by anyone. <bookmark mark='t'/> The architecture fits in a few pages of code. Everything else "
            "was learned, from one simple objective: predict the next token."
        ) as vo:
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(panels[i], shift=UP * 0.2), FadeIn(caps[i]), run_time=0.8)
            vo.wait_until("t")
            self.play(FadeIn(title, shift=DOWN * 0.2))

        interp = label(r"What all those learned numbers are doing, in detail,\\is still an open question: \emph{interpretability}",
                       font_size=32).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Working out, in detail, what all those billions of learned numbers are actually doing is still an open "
            "scientific problem, and a very active one, called interpretability. You now know the machine they live in."
        ) as vo:
            self.play(FadeIn(interp, shift=UP * 0.2))
        self.clear_scene()

        thanks = label(r"Thanks for watching.", font_size=60)
        with self.voiceover("Thanks for watching.") as vo:
            self.play(FadeIn(thanks))
        self.wait(2.0)
        self.play(FadeOut(thanks))


