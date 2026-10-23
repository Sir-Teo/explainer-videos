from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (BASE_C, BWD, COMM, DUP, EDU, F, FULL_C, FWD, GPU, KEPT, OPT, PAGE, PART, REMOVED,
                                   WEIGHTS, gantt, load, node_box)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        out = []
        # 1. the web, filtered
        W = load("web")
        vals = [W["n_pages"], W["n_pages"] - W["blocked"], dict(W["langs"])["en"], W["english"]]
        g = VGroup(*[Rectangle(width=0.45, height=1.7 * v / vals[0], stroke_width=0,
                               fill_color=PAGE if i == 0 else KEPT, fill_opacity=0.85).move_to([0.6 * i, 0, 0],
                                                                                              aligned_edge=DOWN)
                     for i, v in enumerate(vals)])
        out.append((g, rf"${W['n_pages']:,}$ pages $\to$ ${W['english']:,}$".replace(",", "{,}"), KEPT))
        # 2. MinHash's S-curve, measured
        D = load("dedup")
        ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=TW * 0.85, y_length=TH * 0.8, tips=False,
                  axis_config={"stroke_color": GREY_D, "include_ticks": False})
        ss = np.linspace(0, 1, 100)
        g2 = VGroup(ax, curve(ax, ss, 1 - (1 - ss ** D["rows"]) ** D["bands"], DUP, 3),
                    *[Dot(ax.c2p(b["s"], b["measured"]), radius=0.035, color=WHITE) for b in D["bins"]])
        out.append((g2, r"LSH's S-curve, \ measured", DUP))
        # 3. quality: our classifier against FineWeb-Edu's
        Q = load("quality")
        g3 = VGroup(*[Rectangle(width=0.7, height=1.7 * v, stroke_width=0, fill_color=c, fill_opacity=0.85)
                      .move_to([1.0 * i, 0, 0], aligned_edge=DOWN)
                      for i, (v, c) in enumerate(((F.FINEWEB_EDU["f1"] / 100, C.PROB), (Q["f1"], EDU)))])
        out.append((g3, r"a quality filter, \ F1", EDU))
        # 4. collapse: what a model can still say, replace against accumulate
        Cl = load("collapse")
        rep, acc = np.asarray(Cl["replace"]).mean(0), np.asarray(Cl["accumulate"]).mean(0)
        ax4 = Axes(x_range=[0, Cl["gens"], 10], y_range=[0, 3500, 1000], x_length=TW * 0.85, y_length=TH * 0.8,
                   tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})
        x = np.arange(Cl["gens"] + 1)
        g4 = VGroup(ax4, curve(ax4, x, rep[:, 0], REMOVED, 3), curve(ax4, x, acc[:, 0], KEPT, 3))
        out.append((g4, r"collapse, \ and its cure", REMOVED))
        # 5. the ring's bound
        g5 = VGroup(MathTex(r"T \ge 2\,\frac{p-1}{p}\,\frac{n}{B}", font_size=40, color=COMM),
                    label(r"and the ring attains it", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.2)
        out.append((g5, r"all-reduce, \ optimal", COMM))
        # 6. ZeRO's memory per GPU
        P = load("published")
        mem = P["zero_mem"]
        g6 = VGroup(*[Rectangle(width=0.45, height=max(1.7 * m / mem[0], 0.03), stroke_width=0, fill_color=OPT,
                                fill_opacity=0.85).move_to([0.6 * i, 0, 0], aligned_edge=DOWN)
                      for i, m in enumerate(mem)])
        out.append((g6, r"ZeRO: \ $120 \to 1.9$ GB", OPT))
        # 7. a pipeline, 1F1B
        Pp = load("pipeline")
        g7 = gantt(Pp["1f1b"]["ops"], Pp["p"], Pp["1f1b"]["total"], width=2.8, row_h=0.32, numbers=False)
        g7.names.set_opacity(0)
        out.append((g7, rf"the bubble: \ $\frac{{p-1}}{{m+p-1}}$", GPU))
        # 8. our two recipes
        b, f = load("recipe_base"), load("recipe_full")
        eb, ef = np.asarray(b["evals"]), np.asarray(f["evals"])
        lo = min(eb[:, 2].min(), ef[:, 2].min()) - 0.1
        ax8 = Axes(x_range=[0, b["spec"]["steps"], 200], y_range=[lo, lo + 2.5, 1], x_length=TW * 0.85,
                   y_length=TH * 0.8, tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})
        g8 = VGroup(ax8, curve(ax8, eb[:, 0], np.minimum(eb[:, 2], lo + 2.5), BASE_C, 3),
                    curve(ax8, ef[:, 0], np.minimum(ef[:, 2], lo + 2.5), FULL_C, 3))
        out.append((g8, r"2020 against 2026", FULL_C))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
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
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. A pretraining corpus starts as a crawl of the web, and most of it is thrown away: by "
            "address, by language, by quality. MinHash and locality-sensitive hashing find the near-duplicates "
            "without comparing every pair, and their S-curve came out as predicted. A small classifier, trained on a "
            "large model's grades, decides which pages teach. Mixtures are chosen for a target, and synthetic data "
            "helps only alongside real text. Then the arithmetic: six operations per parameter per token, sixteen "
            "bytes per parameter, and activations on top. Data parallelism needs an all-reduce, and the ring is "
            "optimal; ZeRO shards the copies away; tensor, pipeline, context and expert parallelism cut the rest. "
            "Fewer bits need scaling tricks, big runs need QK-norm and the z-loss, and sixteen thousand GPUs need "
            "checkpoints. And our own model, trained with the full recipe, took its place on the scoreboard."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"serving: \ KV caches, \ drafts, \ four-bit weights", [19]),
            (r"the same data pipeline for images, video, sound", [22, 23]),
            (r"post-training on our pretrained model", [27]),
            (r"reinforcement learning on top of pretraining", [28]),
            (r"what the pretrained model knows inside", [30]),
            (r"contamination, \ evaluation, \ trust", [31]),
        ], font_size=24)
        with self.voiceover(
            "All of this comes back. Serving the trained model, with its caches, drafts and four-bit weights, is "
            "Part 19. The same data pipelines feed images, video and sound in Parts 22 and 23. Post-training starts "
            "from a pretrained model in Part 27, and reinforcement learning builds reasoning on top of it in Part "
            "28. Part 30 opens a pretrained model up, and Part 31 asks how far its evaluations can be trusted."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"MinHash: \ show that for a random permutation, $\Pr[\min_A = \min_B] = J(A, B)$. \ With $b = 20$ bands "
            r"of $r = 5$, at what similarity is a pair caught half the time? \ How often at $s = 0.8$?",
            r"An all-reduce of $10$ GB of gradients over $p = 64$ GPUs with $50$ GB/s each: \ find the ring's "
            r"bandwidth time, \ and show that no algorithm can beat it.",
            r"A $70$B model in mixed-precision Adam ($K = 12$) on $512$ GPUs: \ bytes per GPU without ZeRO and with "
            r"stages $1$, $2$, $3$. \ How much more does stage $3$ communicate?",
            r"A pipeline of $p = 16$ stages and $m = 64$ micro-batches: \ the bubble for GPipe, \ for 1F1B, \ "
            r"interleaved with $v = 4$, \ and ZB-H1 when $t_F = t_B = t_W$.",
            r"Gradients of size $2^{-30}$ in FP16: \ which loss scale brings them to FP16's smallest normal number? \ "
            r"Why does BF16 need none?",
            r"Checkpoints cost $\delta = 60$ s and failures come every $M = 2$ h: \ find Young's interval and the "
            r"share of time it wastes, to first order.",
        ], font_size=21)
        with self.voiceover(
            "Here are six problems to try, from MinHash's probability to Young's checkpoint interval. Pause here and "
            "work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 19, \ Inference", font_size=40).to_edge(UP, buff=0.5)
        D = F.DSV3
        steps = VGroup(*[node_box(t, c, font_size=24) for t, c in (
            (r"prefill: \ the prompt at once, \ arithmetic-bound", C.COMPUTE),
            (r"decode: \ one token at a time, \ memory-bound", C.DRAM if hasattr(C, "DRAM") else GREY_B),
            (r"guess ahead, check at once: \ speculative decoding", C.PROB),
            (r"fewer bits per weight: \ GPTQ, rotations, NVFP4", C.QUANT))])
        steps.arrange(DOWN, buff=0.45).move_to(DOWN * 0.4)
        arrs = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.06, color=GREY_B, stroke_width=2.5,
                              max_tip_length_to_length_ratio=0.35) for a, b in zip(steps, steps[1:])])
        with self.voiceover(
            "Next time: inference. A trained model has to answer, quickly and cheaply, for millions of people. "
            "Reading a prompt is arithmetic; writing the answer, one token at a time, is moving memory. Drafts like "
            "DeepSeek-V3's second-token guesses let one pass check several tokens, and four-bit weights make every "
            "token cheaper. That is Part 19."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s_), *([GrowArrow(arrs[i - 1])] if i else []))
                                    for i, s_ in enumerate(steps)], lag_ratio=0.5), run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"S.~Rajbhandari, J.~Rasley et al., the ZeRO papers (2020--21), \ and the DeepSpeed and Megatron-LM docs",
             r"J.~Leskovec, A.~Rajaraman \& J.~D.~Ullman, \textit{Mining of Massive Datasets}, ch.~3 (MinHash, LSH)",
             r"Hugging Face, \textit{The Ultra-Scale Playbook} (2025); \ \textit{The Smol Training Playbook} (2025)"],
            [r"Broder (1997); \ Indyk \& Motwani (1998); \ Lee et al.\ (2022); \ Penedo et al., FineWeb (2024); \ Li et "
             r"al., DCLM (2024)",
             r"Xie et al., DoReMi (2023); \ Liu et al., RegMix (2024); \ Maini et al., WRAP (2024); \ Shumailov et al.\ "
             r"(2024); \ Gerstgrasser et al.\ (2024); \ Muennighoff et al.\ (2023)",
             r"Raffel et al.\ (2020); \ Bavarian et al., FIM (2022); \ Hu et al., MiniCPM (2024); \ Hägele et al.\ "
             r"(2024); \ Xiong et al.\ (2023)",
             r"Patarasuk \& Yuan (2009); \ Rajbhandari et al., ZeRO (2020); \ Zhao et al., FSDP (2023); \ Shoeybi et "
             r"al., Megatron-LM (2019); \ Korthikanti et al.\ (2022)",
             r"Huang et al., GPipe (2019); \ Narayanan et al.\ (2019, 2021); \ Qi et al., Zero Bubble (2024); \ Liu et "
             r"al., Ring Attention (2023); \ Chowdhery et al., PaLM (2022)",
             r"Micikevicius et al.\ (2018, 2022); \ Mishra et al., MXFP8 (2025); \ NVIDIA, NVFP4 (2025); \ Wortsman "
             r"et al.\ (2024); \ Dehghani et al.\ (2023); \ Liu et al., Moonlight (2025)",
             r"Gloeckle et al.\ (2024); \ Young (1974); \ Llama Team (2024); \ DeepSeek-AI, V3 (2024), V4 (2026); \ "
             r"Kimi Team, K2 (2025); \ Qwen Team (2025)",
             r"Team OLMo, OLMo 2 (2025), Olmo 3 (2025); \ Hugging Face, SmolLM3 (2025); \ NVIDIA, Nemotron 3 (2026); \ "
             r"Meta, Llama 4 (2025); \ GLM-4.5 Team (2025)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Most of this part's methods are written up openly, in the technical reports of the labs that use them, "
            "and they are well worth reading. Thanks for watching, and see you in Part 19."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
