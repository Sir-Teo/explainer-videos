from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import ADD, DECAY, DELTA, STATE, curve, grid_matrix, load


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        def plane(xr, yr):
            return Axes(x_range=xr, y_range=yr, x_length=TW, y_length=TH, tips=False, axis_config={"stroke_width": 0})

        out = []
        k = load("kvcache")
        pt = k["per_token"]
        vals = [pt["llama_mha"], pt["llama"], pt["mla"], pt["qwen"]]
        cols = [GREY_B, C.TRUE_P, C.BITS, C.INTERVAL]
        bars = VGroup(*[Rectangle(width=0.5, height=0.3 + 0.55 * (math.log10(v) - 4), stroke_width=0, fill_color=c_,
                                  fill_opacity=0.85) for v, c_ in zip(vals, cols)]).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        out.append((bars, r"shrinking the cache", C.BITS))
        out.append((VGroup(Rectangle(width=0.5, height=1.6, stroke_color=C.QUERY, fill_color=C.QUERY, fill_opacity=0.2),
                           Rectangle(width=0.5, height=0.5, stroke_color=STATE, fill_color=STATE, fill_opacity=0.3))
                    .arrange(RIGHT, buff=0.2), r"regrouping $Q(K^{\top}V)$", STATE))
        g = np.random.default_rng(1)
        out.append((grid_matrix(sum(np.outer(g.normal(size=6), g.normal(size=6)) for _ in range(4)), 1.8),
                    r"a matrix memory", STATE))
        c = load("capacity")
        a4 = plane([0, 256, 64], [0, 2.5, 1])
        out.append((VGroup(curve(a4, np.asarray(c["Ns"]), np.minimum(np.asarray(c["err_add"]), 2.5), ADD, 3)),
                    r"crosstalk", ADD))
        n = len(np.asarray(c["age_add"]))
        a5 = plane([0, n, 32], [0, 2.5, 1])
        out.append((VGroup(curve(a5, np.arange(n), np.minimum(np.asarray(c["age_add"]), 2.5), ADD, 2.5),
                           curve(a5, np.arange(n), np.minimum(np.asarray(c["age_decay"]), 2.5), DECAY, 3)), r"forgetting", DECAY))
        vals = [c["update_add"], c["update_decay"], c["update_delta"]]
        b6 = VGroup(*[Rectangle(width=0.6, height=0.2 + 0.6 * (math.log10(v / min(vals)) + 0.2), stroke_width=0, fill_color=c_,
                                fill_opacity=0.85) for v, c_ in zip(vals, (ADD, DECAY, DELTA))]).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        out.append((b6, r"the delta rule", DELTA))
        s = load("ssm")
        a7 = plane([0, len(s["u"]), 20], [-2.5, 2.5, 1])
        out.append((VGroup(curve(a7, np.arange(len(s["u"])), np.asarray(s["fixed"]), ADD, 2).set_stroke(opacity=0.5),
                           curve(a7, np.arange(len(s["u"])), np.asarray(s["selective"]), C.INTERVAL, 3)),
                    r"a selective state", C.INTERVAL))
        stk = VGroup(*[Rectangle(width=1.2, height=0.16, stroke_width=0, fill_color=(C.ATTN if i % 4 == 3 else C.INTERVAL),
                                 fill_opacity=0.85) for i in range(8)]).arrange(UP, buff=0.04)
        out.append((stk, r"hybrids", C.ATTN))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 12, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Attention's memory is its cache, and models shrink it by sharing keys and values, or "
            "squeezing them into a latent. Drop the softmax, regroup the product, and attention becomes a recurrence "
            "on a fixed matrix memory. Written by adding, that memory blurs; with decay, it forgets the old; with "
            "the delta rule, one step of gradient descent per token, it corrects itself. State-space models, made "
            "selective, turned out to be the same family. And the newest models mix a few attention layers with "
            "many fast ones."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"attending to only some of the cache", [13]),
            (r"long horizons for agents", [18]),
            (r"serving the cache: \ paging, \ quantizing", [19]),
            (r"memories inside a trained model", [20]),
        ], font_size=26)
        with self.voiceover(
            "Next comes sparsity: attending to only some of the past, and using only some of the model. Agents, in "
            "part eighteen, need memory over very long horizons. Part nineteen is about serving the cache fast, and "
            "part twenty looks for memories inside a trained model."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 13, \ Sparsity", font_size=40).to_edge(UP, buff=0.4)
        g = np.random.default_rng(13)
        experts = VGroup(*[RoundedRectangle(width=0.7, height=0.7, corner_radius=0.1, stroke_color=GREY_C, stroke_width=2)
                           for _ in range(16)]).arrange_in_grid(rows=2, cols=8, buff=0.25).move_to(DOWN * 0.6)
        tok = Text("Spade", font="DejaVu Sans Mono", font_size=30, color=C.BITS).move_to(UP * 1.4)
        chosen = sorted(g.choice(16, 2, replace=False))
        arrows = VGroup(*[Arrow(tok.get_bottom(), experts[i].get_top(), buff=0.1, color=C.BITS, stroke_width=3) for i in chosen])
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        ql = label(r"each token visits only a few experts", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Next time: sparsity. The biggest models today don't use all their weights for every token: a router "
            "sends each token to a few experts among hundreds. <bookmark mark='a'/> How do you route, and how do you "
            "keep every expert busy?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(experts), FadeIn(tok), FadeIn(tag))
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.3),
                      *[experts[i].animate.set_fill(C.BITS, opacity=0.4) for i in chosen])
            vo.wait_until("a")
            self.play(FadeIn(ql))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [
            r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapter 12",
        ]
        papers = [
            r"J.~Ainslie et al., \textit{GQA} (2023); \ DeepSeek-AI, \textit{DeepSeek-V2} (2024), \textit{DeepSeek-V3} (2024)",
            r"A.~Katharopoulos et al., \textit{Transformers are RNNs} (2020)",
            r"B.~Widrow \& M.~E.~Hoff (1960); \ I.~Schlag, K.~Irie \& J.~Schmidhuber (2021); \ S.~Yang et al., \textit{DeltaNet} (2024)",
            r"A.~Gu et al., \textit{S4} (2022); \ A.~Gu \& T.~Dao, \textit{Mamba} (2023); \ T.~Dao \& A.~Gu, \textit{Mamba-2} (2024)",
            r"S.~Yang, J.~Kautz \& A.~Hatamizadeh, \textit{Gated Delta Networks} (2025); \ Y.~Sun et al., \textit{Test-Time Training} (2024)",
            r"S.~Arora et al., \textit{Zoology} (2023); \ Qwen Team, \textit{Qwen3-Next} (2025); \ Kimi Team, \textit{Kimi Linear} (2025)",
        ]
        card = reference_card(books, papers)
        data = note(r"Cache sizes from each model's published configuration; \ every other number is computed here "
                    r"and checked; \ illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Songlin Yang's papers and blog on linear attention and the delta rule are the best way in. Thanks for "
            "watching, and see you in part thirteen."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
