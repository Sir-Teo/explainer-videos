from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    Plot, cfg, heat_image, label, model, model_tag, note, schematic_tag, show_chapter_card, source,
)
from videos.open_models.toys import sink_softmax, softmax

QUIET = np.array([0.1, -0.2, 0.0, 0.3, -0.1, 0.2])  # nothing in the window stands out
LOUD = np.array([0.1, -0.2, 4.0, 0.3, -0.1, 0.2])  # one token clearly matters
SINK = 2.0

# MiMo-V2-Flash Technical Report (Xiaomi, arXiv:2601.02780), Tables 2-3: a 32B dense test model.
ABLATION_ROWS = ["all global", r"window 128, no sink", r"window 128 + sink", r"window 512 + sink"]
ABLATION = {  # benchmark: values per row (None = not reported)
    "MMLU": [57.3, 54.9, 58.3, 58.3],
    "BBH": [54.7, 52.4, 56.1, 54.9],
    "NoLiMa": [49.7, None, 51.2, 38.5],
    "RULER-32k": [89.4, None, 89.4, 84.7],
    "MRCR": [32.5, None, 34.4, 19.6],
}


def weight_bars(vals, x0, color, width=0.45, gap=0.18, scale=3.0, y0=-1.6) -> VGroup:
    g = VGroup()
    for i, v in enumerate(vals):
        r = Rectangle(width=width, height=max(1e-3, scale * v), stroke_width=0, fill_color=color, fill_opacity=0.9)
        r.move_to([x0 + i * (width + gap), y0, 0], aligned_edge=DOWN)
        g.add(r)
    return g


class Sinks(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 6, "MiMo: permission to look at nothing")
        self.tag = model_tag("mimo")
        self.add(self.tag)
        self.must_sum()
        self.sink_trick()
        self.real_sinks()
        self.ablation()

    # ------------------------------------------------------------------
    def must_sum(self):
        p = softmax(QUIET)
        assert abs(p.sum() - 1) < 1e-9 and p.max() < 0.22
        toks = VGroup(*[Square(0.4, stroke_color=C.LOCAL, stroke_width=2, fill_color=C.LOCAL, fill_opacity=0.15)
                        for _ in QUIET]).arrange(RIGHT, buff=0.18).move_to(LEFT * 2.6 + DOWN * 2.2)
        t_l = label(r"the 6 tokens in this head's window", font_size=24, color=C.LOCAL).next_to(toks, DOWN, buff=0.15)
        bars = weight_bars(p, toks[0].get_x(), C.ATTN, width=0.4, gap=0.18, scale=6.0, y0=toks.get_top()[1] + 0.2)
        vals = VGroup(*[DecimalNumber(v, num_decimal_places=2, font_size=22).next_to(b, UP, buff=0.08) for v, b in zip(p, bars)])
        f = MathTex(r"w_j", "=", r"{e^{a_j} \over \sum_k e^{a_k}}", font_size=44).move_to(RIGHT * 3.6 + UP * 1.6)
        f[0].set_color(C.ATTN)
        s1 = MathTex(r"\sum_j w_j = 1", font_size=40, color=YELLOW).next_to(f, DOWN, buff=0.4)
        q = label(r"but what if nothing\\here is relevant?", font_size=30).next_to(s1, DOWN, buff=0.5)
        with self.voiceover(
            "But a window this small creates a problem, and to see it, we have to look closely at the softmax. "
            "<bookmark mark='f'/> Attention turns a head's scores into weights, and those weights always add up to exactly "
            "one. <bookmark mark='n'/> So what should a head do when nothing in its window is relevant? <bookmark mark='w'/> "
            "It can't attend to nothing. The weights still have to go somewhere, so the head ends up mixing in a little of "
            "everything: noise."
        ) as vo:
            self.play(FadeIn(toks), FadeIn(t_l))
            vo.wait_until("f")
            self.play(Write(f), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(vals))
            self.play(Write(s1))
            vo.wait_until("n")
            self.play(FadeIn(q))
            vo.wait_until("w")
            self.play(Wiggle(bars), run_time=1.5)
        self.toks, self.bars, self.vals, self.f, self.s1, self.q = toks, bars, vals, f, s1, q
        self.t_l = t_l

    # ------------------------------------------------------------------
    def sink_trick(self):
        w_quiet, s_quiet = sink_softmax(QUIET, SINK)
        w_loud, s_loud = sink_softmax(LOUD, SINK)
        assert round(s_quiet, 2) == 0.54 and round(w_quiet.sum(), 2) == 0.46
        assert s_loud < 0.11 and w_loud[2] > 0.8
        n = 24
        cell = 0.17
        grid = VGroup()
        for i in range(n):
            for j in range(i + 1):
                op = 0.9 if j == 0 else 0.15 + 0.2 * ((i * 7 + j * 3) % 5) / 5
                grid.add(Square(cell * 0.9, stroke_width=0, fill_color=C.ATTN, fill_opacity=op).move_to([j * cell, -i * cell, 0]))
        grid.scale(0.8).move_to(RIGHT * 3.6 + DOWN * 0.3)
        g_l = label(r"full attention: many heads park\\unwanted weight on token 1", font_size=24, color=GREY_A)
        g_l.next_to(grid, UP, buff=0.2)
        gone = label(r"in a window, token 1 is long gone", font_size=26, color=C.LOCAL).next_to(grid, DOWN, buff=0.25)
        with self.voiceover(
            "Full-attention models found their own workaround. Many heads dump their unwanted attention onto the very "
            "first token of the text, a so-called attention sink. <bookmark mark='w'/> But in a sliding window, the "
            "first token is long gone."
        ) as vo:
            self.play(FadeOut(self.q), FadeOut(self.f), FadeOut(self.s1))
            self.play(FadeIn(grid, lag_ratio=0.002), FadeIn(g_l), run_time=1.2)
            vo.wait_until("w")
            self.play(FadeIn(gone, shift=UP * 0.2))
        self.play(FadeOut(grid), FadeOut(g_l), FadeOut(gone))

        f2 = MathTex(r"w_j", "=", r"{e^{a_j} \over", r"e^{\,s}", r"+ \sum_k e^{a_k}}", font_size=46)
        f2.move_to(RIGHT * 3.4 + UP * 1.7)
        f2[0].set_color(C.ATTN)
        f2[3].set_color(C.SINK)
        s_l = label(r"$s$: one learned score per head,\\with no token behind it", font_size=26, color=C.SINK)
        s_l.next_to(f2, DOWN, buff=0.35)
        sink_bar = Rectangle(width=0.4, height=6.0 * s_quiet, stroke_width=0, fill_color=C.SINK, fill_opacity=0.9)
        sink_bar.next_to(self.bars[-1], RIGHT, buff=0.55).align_to(self.bars, DOWN)
        sink_box = Square(0.4, stroke_color=C.SINK, stroke_width=2).set_fill(C.SINK, 0.15)
        sink_box.next_to(self.toks[-1], RIGHT, buff=0.55)
        sink_t = label(r"sink", font_size=24, color=C.SINK).next_to(sink_box, DOWN, buff=0.15)
        sink_v = DecimalNumber(s_quiet, num_decimal_places=2, font_size=22, color=C.SINK).next_to(sink_bar, UP, buff=0.08)
        new_bars = weight_bars(w_quiet, self.toks[0].get_x(), C.ATTN, width=0.4, gap=0.18, scale=6.0,
                               y0=self.toks.get_top()[1] + 0.2)
        new_vals = VGroup(*[DecimalNumber(v, num_decimal_places=2, font_size=22).next_to(b, UP, buff=0.08)
                            for v, b in zip(w_quiet, new_bars)])
        total = MathTex(r"\sum_j w_j = 0.46", font_size=40, color=YELLOW).next_to(s_l, DOWN, buff=0.45)
        drop = label(r"the sink's share is simply thrown away", font_size=26, color=C.SINK).next_to(total, DOWN, buff=0.25)
        with self.voiceover(
            "MiMo's fix, borrowed from OpenAI's gpt-oss models, is to give every head a learnable sink: "
            "<bookmark mark='e'/> one extra score, with no token behind it, that sits in the softmax's denominator, "
            "<bookmark mark='p'/> like a phantom token with a learned score. <bookmark mark='a'/> When the real scores "
            "are unremarkable, the sink soaks up much of the weight, <bookmark mark='d'/> and that weight is simply thrown "
            "away. The head's real weights now add up to less than one. It's allowed to look at nothing."
        ) as vo:
            vo.wait_until("e")
            self.play(Write(f2), FadeIn(s_l))
            vo.wait_until("p")
            self.play(FadeIn(sink_box), FadeIn(sink_t))
            vo.wait_until("a")
            self.play(GrowFromEdge(sink_bar, DOWN), FadeIn(sink_v), Transform(self.bars, new_bars),
                      Transform(self.vals, new_vals), run_time=1.5)
            vo.wait_until("d")
            self.play(Write(total))
            self.play(FadeIn(drop), sink_bar.animate.set_fill(opacity=0.25))

        loud_bars = weight_bars(w_loud, self.toks[0].get_x(), C.ATTN, width=0.4, gap=0.18, scale=3.0,
                                y0=self.toks.get_top()[1] + 0.2)
        loud_vals = VGroup(*[DecimalNumber(v, num_decimal_places=2, font_size=22).next_to(b, UP, buff=0.08)
                             for v, b in zip(w_loud, loud_bars)])
        loud_sink = Rectangle(width=0.4, height=3.0 * s_loud, stroke_width=0, fill_color=C.SINK, fill_opacity=0.9)
        loud_sink.move_to(sink_bar, aligned_edge=DOWN)
        total2 = MathTex(rf"\sum_j w_j = {w_loud.sum():.2f}", font_size=40, color=YELLOW).move_to(total)
        with self.voiceover(
            "<bookmark mark='r'/> And when one token really does matter, its score beats the sink easily, and the head "
            "attends to it almost as if the sink weren't there."
        ) as vo:
            vo.wait_until("r")
            self.play(Indicate(self.toks[2], color=YELLOW), self.toks[2].animate.set_fill(YELLOW, 0.5))
            self.play(Transform(self.bars, loud_bars), Transform(self.vals, loud_vals), Transform(sink_bar, loud_sink),
                      sink_v.animate.set_value(s_loud).next_to(loud_sink, UP, buff=0.08), Transform(total, total2),
                      FadeOut(drop), run_time=1.5)
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def real_sinks(self):
        s = model("mimo")["sink_bias"]
        v = np.array(s["values"])
        assert v.shape == (60, 128)
        assert 0.96 < (v > 0).mean() < 0.98 and round(v.min()) == -6 and round(v.max()) == 3
        q25, q75 = np.percentile(v, [25, 75])
        assert 0.45 < q25 < 0.6 and 0.75 < q75 < 1.0
        img = heat_image(v.T, height=4.6, width=7.2, diverging=True, vmax=2.0, neg="#6FA8DC", pos="#FFB86B")
        img.move_to(LEFT * 1.4 + DOWN * 0.35)
        frame = SurroundingRectangle(img, buff=0.02, color=GREY_B, stroke_width=1.5)
        xl = label(r"the 60 sliding-window layers $\rightarrow$", font_size=24, color=GREY_A).next_to(frame, DOWN, 0.15)
        yl = label(r"128 heads", font_size=24, color=GREY_A).rotate(PI / 2).next_to(frame, LEFT, buff=0.15)
        bar = heat_image(np.linspace(2, -2, 64)[:, None], height=3.0, width=0.3, diverging=True, vmax=2.0, neg="#6FA8DC",
                         pos="#FFB86B", nearest=False).next_to(frame, RIGHT, buff=0.5).shift(UP * 0.3)
        bt = VGroup(MathTex(r"+2", font_size=24).next_to(bar, RIGHT, buff=0.1).align_to(bar, UP),
                    MathTex(r"0", font_size=24).next_to(bar, RIGHT, buff=0.1),
                    MathTex(r"-2", font_size=24).next_to(bar, RIGHT, buff=0.1).align_to(bar, DOWN))
        clip = note(r"color clipped at $\pm 2$; actual range $-6.2$ to $+3.0$", font_size=20)
        clip.next_to(xl, DOWN, buff=0.1)
        title = label(r"MiMo-V2.6-Pro's learned sink scores, read from the weights", font_size=32).to_edge(UP, buff=0.9)
        facts = VGroup(label(r"97\% positive", font_size=28, color="#FFB86B"),
                       label(r"a few deep heads strongly\\negative: they rarely look away", font_size=24, color="#6FA8DC"))
        facts.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(bar, DOWN, buff=0.45).align_to(bar, LEFT)
        with self.voiceover(
            "These are MiMo's actual learned sink scores: <bookmark mark='r'/> one for each of the 128 heads, in each of "
            "the 60 sliding-window layers. <bookmark mark='p'/> Almost all of them are positive, typically between about a "
            "half and one, so the phantom token is a serious competitor in nearly every head. <bookmark mark='n'/> In "
            "the deepest layers, a few heads have learned strongly negative values: for them, the sink almost never wins."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("r")
            self.play(FadeIn(img), Create(frame), FadeIn(xl), FadeIn(yl), run_time=1.5)
            self.play(FadeIn(bar), FadeIn(bt), FadeIn(clip))
            vo.wait_until("p")
            self.play(FadeIn(facts[0]))
            vo.wait_until("n")
            self.play(FadeIn(facts[1]))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def ablation(self):
        cols = list(ABLATION)
        table = VGroup()
        head = VGroup(label("", font_size=24), *[label(c, font_size=26, color=GREY_A) for c in cols])
        table.add(head)
        best = {c: max(v for v in vals if v is not None) for c, vals in ABLATION.items()}
        for r, name in enumerate(ABLATION_ROWS):
            cells = [label(name, font_size=26, color=C.LOCAL if "window" in name else C.GLOBAL)]
            for c in cols:
                v = ABLATION[c][r]
                txt = "--" if v is None else f"{v:.1f}"
                col = YELLOW if v is not None and v == best[c] else (RED if v is not None and v < best[c] - 5 else WHITE)
                cells.append(label(txt, font_size=26, color=col))
            table.add(VGroup(*cells))
        x0, xs = -5.4, [-1.3, 0.4, 2.1, 3.9, 5.6]
        for i, row in enumerate(table):
            y = 1.6 - 0.62 * i
            row[0].move_to([x0, y, 0], aligned_edge=LEFT)
            for j, cell in enumerate(row[1:]):
                cell.move_to([xs[j], y, 0])
        hl = Line([x0, 1.3, 0], [6.2, 1.3, 0], color=GREY_B, stroke_width=1.5)
        div = DashedLine([1.25, 1.85, 0], [1.25, -1.2, 0], color=GREY_D, stroke_width=1.5)
        gen = label(r"general", font_size=22, color=GREY_B).move_to([-0.45, 2.3, 0])
        lng = label(r"long context, after long-context training", font_size=22, color=GREY_B).move_to([3.9, 2.3, 0])
        title = label(r"A surprise: the tiny window wins", font_size=34).to_edge(UP, buff=0.9)
        src = source(r"MiMo-V2-Flash technical report (Xiaomi, 2026), Tables 2--3: 32B dense test models")
        why = label(r"small window $\Rightarrow$ local layers do local work, global layers do everything far away",
                    font_size=28, color=YELLOW).to_edge(DOWN, buff=0.8)
        assert ABLATION["MRCR"][2] > ABLATION["MRCR"][0] > ABLATION["MRCR"][3]
        with self.voiceover(
            "With sinks in place, Xiaomi found something surprising, in experiments on a 32-billion-parameter test model. "
            "<bookmark mark='n'/> Without sinks, a 128-token window hurt. <bookmark mark='s'/> With sinks, it matched "
            "or beat a model with global attention in every layer. <bookmark mark='l'/> And after training on long "
            "documents, the 128-token window beat a 512-token window on long-context tests, by a wide margin. "
            "<bookmark mark='h'/> Xiaomi's explanation is a division of labor: a small window forces the local layers to "
            "handle only local structure, and leaves everything far away to the global layers. A bigger window blurs "
            "that line."
        ) as vo:
            self.play(FadeIn(title), FadeIn(src), FadeIn(head), Create(hl), FadeIn(gen), FadeIn(lng), Create(div),
                      FadeIn(table[1]))
            vo.wait_until("n")
            self.play(FadeIn(table[2], shift=UP * 0.1))
            vo.wait_until("s")
            self.play(FadeIn(table[3], shift=UP * 0.1))
            vo.wait_until("l")
            self.play(FadeIn(table[4], shift=UP * 0.1))
            vo.wait_until("h")
            self.play(FadeIn(why, shift=UP * 0.2))
        self.clear_scene()
