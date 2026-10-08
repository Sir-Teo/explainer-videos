from __future__ import annotations

import json

import numpy as np

from explainer import *  # noqa: F403
from videos.frontier.common import Mono, bar_rows, label, load, note, page_card, source
from videos.frontier.compute import DATA_DIR

MIX = [  # Llama 3 pretraining mix (Llama 3 paper, Sec. 3.1.2)
    (r"general knowledge", 50, C.KEPT),
    (r"math and reasoning", 25, C.EDU),
    (r"code", 17, C.PARAMS),
    (r"multilingual", 8, C.MUON),
]
TOKENS = [  # pretraining tokens (trillions), from each model's report or card
    (r"Llama 3 (2024)", 15.6),
    (r"DeepSeek-V3 (2024)", 14.8),
    (r"Kimi K2 (2025)", 15.5),
    (r"GLM-5 (2026)", 28.5),
    (r"DeepSeek-V4 (2026)", 33.0),
    (r"Qwen3 (2025)", 36.0),
]


def edu_int(s: float) -> int:
    """FineWeb-Edu's integer score: round and clip the regression output to 0..5."""
    return int(round(max(0.0, min(5.0, s))))


class Quality(VoiceoverScene):
    def construct(self):
        self.e = load("edu")
        self.classifier_idea()
        self.our_scores()
        self.rewrite()
        self.mixture()
        self.tokens()

    # ------------------------------------------------------------------
    def classifier_idea(self):
        steps = VGroup(
            label(r"1. Llama 3 70B grades 500{,}000 pages: educational value 0--5", font_size=30),
            label(r"2. a small classifier learns to imitate those grades", font_size=30),
            label(r"3. it scores all 15 trillion tokens (6{,}000 H100 hours)", font_size=30),
            label(r"4. keep pages scoring 3 or more", font_size=30, color=C.EDU),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.1)
        head = label(r"Model-based filtering: FineWeb-Edu", font_size=38).to_edge(UP, buff=0.5)
        src = source(r"Penedo et al., \emph{The FineWeb Datasets} (2024)")
        with self.voiceover(
            "Hand-written rules catch obvious junk, but they can't tell whether a page is worth learning from. For "
            "that, labs use models. <bookmark mark='a'/> FineWeb-Edu asked Llama 3 70B to grade half a million pages "
            "for educational value, from zero to five, <bookmark mark='b'/> trained a small, fast classifier to "
            "imitate those grades, <bookmark mark='c'/> and ran it over all fifteen trillion tokens. "
            "<bookmark mark='d'/> Then it kept the pages scoring three or more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(steps[i], shift=RIGHT * 0.2), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def our_scores(self):
        scores = np.array(self.e["scores"], float)
        urls = self.e["urls"]
        ints = np.array([edu_int(s) for s in scores])
        counts = np.bincount(ints, minlength=6)
        n = len(ints)
        keep = (ints >= 3).mean()
        self.keep = keep
        bars = VGroup()
        maxc = counts.max()
        for k in range(6):
            col = C.EDU if k >= 3 else GREY_B
            b = Rectangle(width=0.8, height=max(0.02, 3.6 * counts[k] / maxc), stroke_width=0, fill_color=col, fill_opacity=0.85)
            bars.add(b)
        bars.arrange(RIGHT, buff=0.18, aligned_edge=DOWN).move_to(LEFT * 3.0 + DOWN * 0.6)
        xl = VGroup(*[MathTex(str(k), font_size=28, color=GREY_A).next_to(b, DOWN, buff=0.12) for k, b in enumerate(bars)])
        cl = VGroup(*[label(f"{c:,}".replace(",", "{,}"), font_size=22).next_to(b, UP, buff=0.08) for c, b in zip(counts, bars)])
        xt = label(r"educational score", font_size=24, color=GREY_A).next_to(xl, DOWN, buff=0.15)
        n_all = self.e["n_survivors"]
        assert n == 400 and n_all == 1363
        head = label(rf"FineWeb-Edu's classifier on {n} random pages of our {n_all:,} survivors".replace(",", "{,}"),
                     font_size=32).to_edge(UP, buff=0.4)
        kt = label(rf"score $\geq 3$: {100 * keep:.0f}\%", font_size=32, color=C.EDU).next_to(bars, UP, buff=0.5).align_to(bars, RIGHT)
        texts = {json.loads(ln)["url"]: json.loads(ln)["text"] for ln in open(DATA_DIR / "funnel_kept.jsonl")}
        order = np.argsort(-scores)
        top_url = urls[int(order[0])]
        low_url = urls[int(order[len(order) // 3])]
        top = page_card(texts[top_url], top_url, width=5.4, lines=6, chars=46, font_size=15, color=C.EDU)
        tops = label(rf"score {scores[order[0]]:.1f}", font_size=24, color=C.EDU)
        low = page_card(texts[low_url], low_url, width=5.4, lines=4, chars=46, font_size=15, color=GREY_B)
        lows = label(rf"score {scores[order[len(order) // 3]]:.1f}", font_size=24, color=GREY_B)
        right = VGroup(VGroup(tops, top).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
                       VGroup(lows, low).arrange(DOWN, aligned_edge=LEFT, buff=0.1)).arrange(DOWN, buff=0.35)
        right.move_to(RIGHT * 3.4 + DOWN * 0.4)
        if right.height > 6.2:
            right.scale_to_fit_height(6.2)
        with self.voiceover(
            "We ran that same classifier on four hundred random pages that survived our filters. "
            "<bookmark mark='h'/> Most score low: "
            "shops, services, local news. <bookmark mark='k'/> Keeping three and up, as FineWeb-Edu does, leaves "
            "EDUKEEP percent. <bookmark mark='t'/> The top scorer looks like this, and a typical low scorer like "
            "this."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("h")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), FadeIn(xl), FadeIn(cl), FadeIn(xt))
            vo.wait_until("k")
            self.play(FadeIn(kt))
            vo.wait_until("t")
            self.play(FadeIn(right[0]))
            self.play(FadeIn(right[1]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rewrite(self):
        items = VGroup(
            label(r"\textbf{FineWeb-Edu}: kept 8\% of FineWeb (1.3T tokens); matched older datasets'", font_size=28),
            label(r"knowledge-benchmark scores with 10$\times$ fewer tokens", font_size=28),
            label(r"\textbf{Nemotron-CC} (NVIDIA): rephrase pages with an LLM $\rightarrow$ 1.9T synthetic tokens", font_size=28),
            label(r"\textbf{Kimi K2}: rephrased knowledge data; SimpleQA 23.8\% $\rightarrow$ 28.9\%", font_size=28),
            label(r"\textbf{OLMo 3}: repeat the best data up to 7 times instead of a hard cut", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.1)
        items[1].shift(RIGHT * 0.4)
        head = label(r"Keep the best, and rewrite the rest", font_size=36).to_edge(UP, buff=0.5)
        src = source(r"FineWeb (2024); Su et al.\ 2024 (Nemotron-CC); Kimi K2 report (2025); OLMo 3 report (2025)")
        with self.voiceover(
            "The payoff is large. FineWeb-Edu kept only eight percent of FineWeb, 1.3 trillion tokens, and models "
            "trained on it matched older datasets on knowledge benchmarks with ten times fewer tokens. "
            "<bookmark mark='r'/> Since then, the trend is to rewrite rather than throw away. NVIDIA's Nemotron-CC "
            "used a language model to rephrase web pages, producing almost two trillion synthetic tokens. "
            "<bookmark mark='k'/> Moonshot rephrased Kimi K2's knowledge data, and a factual-recall score rose from "
            "24 to 29 percent. <bookmark mark='o'/> And AI2's OLMo 3 repeats its best data up to seven times, instead "
            "of drawing a hard line."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(items[0]), FadeIn(items[1]))
            vo.wait_until("r")
            self.play(FadeIn(items[2]))
            vo.wait_until("k")
            self.play(FadeIn(items[3]))
            vo.wait_until("o")
            self.play(FadeIn(items[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mixture(self):
        W = 11.0
        bar = VGroup()
        x = -W / 2
        labels = VGroup()
        for name, pct, col in MIX:
            w = W * pct / 100
            r = Rectangle(width=w, height=0.9, stroke_width=1, stroke_color=BACKGROUND, fill_color=col, fill_opacity=0.85)
            r.move_to([x + w / 2, 0.6, 0])
            bar.add(r)
            t = label(rf"{name}\\{pct}\%", font_size=24).next_to(r, DOWN, buff=0.2)
            labels.add(t)
            x += w
        head = label(r"Llama 3's pretraining mix", font_size=36).to_edge(UP, buff=0.6)
        anneal = VGroup(
            label(r"\textbf{Annealing}: in the final stretch, upweight the very best data", font_size=28),
            label(r"Llama 3 8B: +24\% on grade-school math (GSM8K)", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.9)
        src = source(r"Llama Team, Meta, \emph{The Llama 3 Herd of Models} (2024)")
        with self.voiceover(
            "Then the data is mixed. Llama 3's recipe was about half general knowledge, a quarter math and reasoning, "
            "seventeen percent code, and eight percent other languages. <bookmark mark='a'/> And in the last stretch "
            "of training, the mix shifts toward the very best data. Annealing Llama 3's 8-billion-parameter model "
            "this way raised its score on grade-school math problems by twenty-four percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in bar], lag_ratio=0.3), FadeIn(labels, lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(anneal))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tokens(self):
        rows = bar_rows([(name, t, C.DATA, rf"{t:g}T") for name, t in TOKENS], 6.0 / 36, font_size=26, buff=0.18)
        rows.move_to(LEFT * 1.0 + UP * 0.9)
        head = label(r"Pretraining tokens", font_size=34).to_edge(UP, buff=0.35)
        tk = load("tokenizer")
        toks = tk["example_tokens"]
        assert tk["vocab"] == 2048 and 160e6 < tk["train_tokens"] < 180e6
        boxes = VGroup()
        for t in toks:
            m = Mono(t.replace(" ", "␣"), font_size=20)
            bx = RoundedRectangle(width=m.width + 0.12, height=0.38, corner_radius=0.05, stroke_color=C.TOKEN,
                                  stroke_width=1.2, fill_color=C.TOKEN, fill_opacity=0.12)
            m.move_to(bx)
            boxes.add(VGroup(bx, m))
        boxes.arrange(RIGHT, buff=0.04)
        if boxes.width > 13.2:
            boxes.width = 13.2
        boxes.move_to(DOWN * 2.0)
        cap = label(rf"our tokenizer: {tk['vocab']:,} tokens; frontier tokenizers: 128{{,}}000--260{{,}}000".replace(",", "{,}", 1),
                    font_size=24, color=GREY_A).next_to(boxes, UP, buff=0.25)
        fuel = label(rf"our pretraining text: {tk['train_tokens'] / 1e6:.0f} million tokens of FineWeb-Edu", font_size=26,
                     color=C.DATA).next_to(boxes, DOWN, buff=0.3)
        src = source(r"each model's technical report or model card")
        with self.voiceover(
            "The finished datasets are enormous: around fifteen trillion tokens for Llama 3, DeepSeek-V3 and Kimi "
            "K2; twenty-eight and a half trillion for GLM-5; thirty-three trillion for DeepSeek-V4, released in April "
            "2026; thirty-six trillion for Qwen3. <bookmark mark='t'/> Last, the text becomes tokens. A tokenizer, "
            "trained with byte-pair encoding, breaks text into frequent pieces; frontier tokenizers have between 128 "
            "and 260 thousand of them. We trained a small one, with 2,048, <bookmark mark='f'/> and used it to encode "
            "168 million tokens of FineWeb-Edu: the fuel for the training runs in the next part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in rows],
                                  lag_ratio=0.25), run_time=3.0)
            vo.wait_until("t")
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in boxes], lag_ratio=0.04))
            vo.wait_until("f")
            self.play(FadeIn(fuel))
        self.wait(0.4)
        self.clear_scene()
