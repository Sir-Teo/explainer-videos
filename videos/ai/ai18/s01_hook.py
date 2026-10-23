from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai18.common import (COMM, C_COL, D_COL, F, GPU, PART, REMOVED, human, load, spoken_int, stat)


class Hook(VoiceoverScene):
    def construct(self):
        self.era()
        self.run()
        self.question()
        self.ours()
        self.plan()

    # ------------------------------------------------------------------
    def era(self):
        g = axes([2017.8, 2026.2], [0, 5], x_length=10.0, y_length=4.6, xlabel=r"year",
                 ylabel=r"chips working on one training run \ (log scale)", center=[0.4, -0.3, 0],
                 xticks=[2018, 2020, 2022, 2024, 2026], yticks=[0, 1, 2, 3, 4, 5],
                 xfmt=lambda v: f"{int(v)}", yfmt=lambda v: rf"10^{{{int(v)}}}")
        ax = g.ax
        pts = VGroup()
        tags = VGroup()
        sides = [UR, DR, UL, DR, DR, UL]
        for (yr, name, n, kind, src), side in zip(F.ERA, sides):
            d = Dot(ax.c2p(yr, math.log10(n)), radius=0.09, color=GPU)
            pts.add(d)
            tags.add(label(rf"{name}: \ ${n:,}$ {kind}".replace(",", "{,}"), font_size=20, color=GREY_A)
                     .next_to(d, side, buff=0.1))
        line = VMobject(color=GPU, stroke_width=2, stroke_opacity=0.5).set_points_as_corners([p.get_center() for p in pts])
        hc = history_card(2018, r"OpenAI's GPT-1", r"pretrained for a month on eight GPUs", width=5.0,
                          color=GPU).move_to(ax.c2p(2020.4, 4.1))
        src = cite(r"OpenAI (2018); \ Shoeybi et al.\ (2019); \ Narayanan et al.\ (2021, a throughput test); \ "
                   r"Chowdhery et al.\ (2022); \ Llama Team (2024); \ Meta (2025)", font_size=17)
        first, last = F.ERA[0], F.ERA[-1]
        with self.voiceover(
            "June 2018. OpenAI's first GPT is pretrained for about a month on eight graphics cards. "
            "<bookmark mark='a'/> Here is how many chips have worked together on one training run since then, on a "
            "scale where each step up is ten times more. <bookmark mark='b'/> In 2019, Megatron-LM spreads one model "
            "over 512 GPUs. In 2022, Google's PaLM trains on 6,144 TPU chips. In 2024, Meta's Llama 3 uses 16,384 "
            f"GPUs, and in 2025 Llama 4 Behemoth is pretrained on {spoken_int(last[2])} of them. <bookmark mark='c'/> In seven "
            f"years, a training run went from {first[2]} chips to {round(last[2] / first[2], -2):,.0f} times as many. "
            "This part is about how that is done."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(pts[0], scale=1.5), FadeIn(tags[0]), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(hc), Indicate(g.ax, color=GPU, scale_factor=1.0))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(p, scale=1.5), FadeIn(t)) for p, t in zip(pts[1:], tags[1:])],
                                  lag_ratio=0.5), Create(line), run_time=4.0)
            vo.wait_until("c")
            self.play(Indicate(pts[-1], color=YELLOW, scale_factor=1.8))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def run(self):
        L, P = F.LLAMA3, load("published")
        k = 128  # 128 x 128 = 16,384 GPUs, one pixel-dot each (an image: sixteen thousand mobjects would crawl)
        px = np.zeros((3 * k, 3 * k, 4), np.uint8)
        col = np.array(ManimColor(GPU).to_rgb()) * 255
        for i in range(k):
            for j in range(k):
                px[3 * i:3 * i + 2, 3 * j:3 * j + 2, :3] = col
                px[3 * i:3 * i + 2, 3 * j:3 * j + 2, 3] = 255
        dots = ImageMobject(px).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        dots.height = 5.1
        dots.move_to([-3.2, -0.2, 0])
        sp = dots.height / k

        def at(i):
            return dots.get_corner(UL) + np.array([(i % k + 0.33) * sp, -(i // k + 0.33) * sp, 0])

        frame = SurroundingRectangle(dots, color=GREY_D, buff=0.12, corner_radius=0.06, stroke_width=1.5)
        cap = label(rf"${L['gpus']:,}$ H100 GPUs, \ one dot each".replace(",", "{,}"), font_size=22, color=GPU)
        cap.next_to(frame, UP, buff=0.15)
        stats = VGroup(
            stat(rf"${sci(L['flops'], 1)}$", r"operations \ (FLOP)", color=C_COL, font_size=38),
            stat(rf"${L['tokens'] / 1e12:.1f}$ trillion", r"tokens of text", color=D_COL, font_size=38),
            stat(rf"${L['interruptions']}$ \ in \ ${L['days']}$ days", r"interruptions, \ $419$ unplanned",
                 color=REMOVED, font_size=38),
            stat(rf"one every ${P['llama_mtbf_h']:.1f}$ hours", r"on average", color=REMOVED, font_size=34),
        ).arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to([3.6, -0.1, 0])
        src = cite(r"Llama Team, \textit{The Llama 3 Herd of Models} (2024), \ Secs.\ 3.3--3.4")
        g = np.random.default_rng(3)
        fails = g.choice(k * k, 24, replace=False)
        boom = [Dot(at(i), radius=0.07, color=REMOVED) for i in fails]
        sch = note(r"which dots fail: \ illustrative").next_to(frame, DOWN, buff=0.15)
        with self.voiceover(
            f"Take that run of Llama 3. {spoken_int(L['gpus'])} H100 GPUs, one dot each. <bookmark mark='a'/> "
            "Together they did about four times ten to the twenty-five operations, on fifteen point six trillion "
            "tokens of text. <bookmark mark='b'/> And they kept breaking. In one fifty-four-day stretch the job "
            f"stopped {L['interruptions']} times, {L['unexpected']} of them unplanned: a faulty GPU, a memory chip, a "
            f"network cable. <bookmark mark='c'/> That is one failure every {P['llama_mtbf_h']:.0f} hours or so, and "
            "every one of them stops all sixteen thousand GPUs, because they are all working on the same model."
        ) as vo:
            self.play(FadeIn(frame), FadeIn(cap), FadeIn(src), FadeIn(dots), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(stats[0], shift=UP * 0.1), FadeIn(stats[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(stats[2], shift=UP * 0.1), FadeIn(sch))
            for b in boom[:12]:
                self.play(FadeIn(b, scale=3), run_time=0.15)
            vo.wait_until("c")
            self.play(FadeIn(stats[3], shift=UP * 0.1), *[FadeIn(b, scale=3) for b in boom[12:]])
            self.play(dots.animate.set_opacity(0.3), run_time=0.6)
            self.play(dots.animate.set_opacity(1.0), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        q = label(r"How do you turn fifteen trillion tokens of the web \\ into one model, \ on sixteen thousand "
                  r"GPUs, \\ without the run falling apart?", font_size=40).move_to(UP * 1.4)
        steps = [(r"data", C.KEPT), (r"objectives", C.PROB), (r"FLOPs and bytes", C_COL), (r"parallelism", GPU),
                 (r"precision", C.QUANT), (r"stability", C.LOSS), (r"failures", REMOVED)]
        path = VGroup()
        for i, (t, c) in enumerate(steps):
            if i:
                path.add(MathTex(r"\to", font_size=30, color=GREY_C))
            path.add(label(t, font_size=28, color=c))
        path.arrange(RIGHT, buff=0.2).move_to(DOWN * 1.2)
        if path.width > 13.0:
            path.width = 13.0
        with self.voiceover(
            "So the question of this part: how do you turn fifteen trillion tokens of the web into one model, on "
            "sixteen thousand GPUs, without the run falling apart? <bookmark mark='a'/> The answer comes in layers: the "
            "data, the objective, the arithmetic, the cuts across devices, the bits, the stability, and the failures."
        ) as vo:
            self.play(FadeIn(q), FadeIn(path.copy().set_opacity(0.15)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.1) for m in path], lag_ratio=0.25), run_time=5.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ours(self):
        W, D = load("web"), load("dedup")
        items = VGroup(
            label(rf"${W['n_pages']:,}$ real web pages from Common Crawl's September 2026 crawl: \ filtered, "
                  r"deduplicated, scored".replace(",", "{,}"), font_size=26, color=C.KEPT),
            label(r"four processes of this computer as a small cluster: \ data, ZeRO, tensor and ring parallelism, "
                  r"\ checked exactly", font_size=26, color=GPU),
            label(r"pipeline schedules simulated, \ failures simulated", font_size=26, color=COMM),
            label(r"training runs pushed to the edge: \ FP16, FP8, high learning rates, \ two-token prediction",
                  font_size=26, color=C.QUANT),
            label(r"and a model trained with the full 2026 recipe, \ against the 2020 one, \ on the scoreboard",
                  font_size=26, color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.2)
        for it in items:
            if it.width > 12.8:
                it.width = 12.8
        head = label(r"In miniature, \ on the computer making this video", font_size=36).to_edge(UP, buff=0.6)
        with self.voiceover(
            "We'll build every layer in miniature, on the computer making this video. <bookmark mark='a'/> "
            f"{spoken_int(W['n_pages'])} real web pages from Common Crawl, filtered, deduplicated and scored. "
            "<bookmark mark='b'/> Four processes as a tiny cluster, to check each kind of parallelism exactly. "
            "<bookmark mark='c'/> Pipelines and failures, simulated. <bookmark mark='d'/> Training pushed to the edge, in "
            "fewer bits and at high learning rates. <bookmark mark='e'/> And the 2026 recipe against the 2020 one, on the "
            "series' scoreboard."
        ) as vo:
            self.play(FadeIn(head), FadeIn(items[0], shift=UP * 0.1), FadeIn(items[1:].copy().set_opacity(0.18)))
            for k, mk in enumerate("bcde", 1):
                vo.wait_until(mk)
                self.play(FadeIn(items[k], shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Pretraining at Scale", font_size=44).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"the data: \ extraction, \ language, \ deduplication by MinHash, \ quality, \ contamination, \ mixtures",
            r"objectives, \ annealing, \ mid-training and long context",
            r"the arithmetic: \ $6ND$, \ and the bytes of weights, gradients, optimizer and activations",
            r"parallelism: \ data, ZeRO and FSDP, \ tensor, pipeline, context, expert",
            r"precision and stability: \ BF16, FP16, FP8 and FP4, \ z-loss, QK-norm, \ Muon at scale",
            r"two-token prediction, \ failures at 16,000 GPUs, \ and our own full-recipe model",
        ], font_size=25)
        with self.voiceover(
            "This is Part 18 of AI, Built, in its third act, the transformer era. <bookmark mark='a'/> In this part: the "
            "data, from raw web pages to a clean mixture; the objective, and the stages of training; the arithmetic of a "
            "run, in operations and bytes; the five ways to cut a model across devices; fewer bits, and stability; "
            "predicting two tokens at once; surviving failures; and our own model, trained with the full recipe."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
