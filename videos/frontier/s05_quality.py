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
        self.bpe_math()

    # ------------------------------------------------------------------
    def classifier_idea(self):
        def mini_page(badge=None, color=GREY_B):
            r = RoundedRectangle(width=0.5, height=0.66, corner_radius=0.05, stroke_color=GREY_B, stroke_width=1.5,
                                 fill_color="#1b1f27", fill_opacity=1)
            lines = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=1.5, color=GREY_C)
                             for w in (0.32, 0.3, 0.34, 0.2)]).arrange(DOWN, buff=0.1).move_to(r)
            g = VGroup(r, lines)
            if badge is not None:
                c = Circle(radius=0.15, stroke_width=0, fill_color=color, fill_opacity=1).move_to(r.get_corner(UR))
                g.add(c, MathTex(str(badge), font_size=22, color=BLACK).move_to(c))
            return g

        grades = [1, 4, 0, 3, 2, 1]  # illustrative grades
        unknown = VGroup(*[mini_page("?", GREY_B) for _ in grades]).arrange(RIGHT, buff=0.3).move_to(UP * 0.3)
        worth = label(r"worth learning from?", font_size=30, color=GREY_A).next_to(unknown, DOWN, buff=0.4)
        raw = VGroup(*[mini_page() for _ in grades]).arrange_in_grid(2, 3, buff=0.2).scale(1.2).move_to(LEFT * 5.0 + UP * 1.2)
        raw_t = label(r"500{,}000 pages", font_size=24).next_to(raw, DOWN, buff=0.15)
        llm = VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, stroke_color=C.EDU, fill_color=C.EDU,
                                      fill_opacity=0.15),
                     label(r"Llama 3 70B", font_size=30, color=C.EDU)).move_to(LEFT * 1.2 + UP * 1.2)
        llm[1].move_to(llm[0])
        llm_t = label(r"prompt: rate educational value, 0--5", font_size=20, color=GREY_A).next_to(llm, UP, buff=0.12)
        graded = VGroup(*[mini_page(g, C.EDU if g >= 3 else GREY_B) for g in grades]).arrange_in_grid(2, 3, buff=0.2).scale(1.2)
        graded.move_to(RIGHT * 2.8 + UP * 1.2)
        graded_t = label(r"graded pages", font_size=24).next_to(graded, DOWN, buff=0.15)
        a1 = Arrow(raw.get_right(), llm.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        a2 = Arrow(llm.get_right(), graded.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        clf = VGroup(RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, stroke_color=C.PARAMS, fill_color=C.PARAMS,
                                      fill_opacity=0.15),
                     label(r"small classifier", font_size=30, color=C.PARAMS)).move_to(LEFT * 1.2 + DOWN * 1.9)
        clf[1].move_to(clf[0])
        clf_t = label(r"$\approx$110M parameters: cheap enough for the whole web", font_size=20, color=GREY_A).next_to(clf, DOWN, buff=0.12)
        a3 = DashedLine(graded_t.get_bottom() + DOWN * 0.05, clf.get_corner(UR) + LEFT * 0.3 + UP * 0.05, color=C.PARAMS, stroke_width=2.5,
                        dash_length=0.1).add_tip(tip_length=0.2)
        a3_t = label(r"learns to imitate", font_size=24, color=C.PARAMS).next_to(a3.get_center(), LEFT, buff=0.55).shift(UP * 0.12)
        web = VGroup(*[mini_page() for _ in range(18)]).arrange_in_grid(3, 6, buff=0.12).scale(0.85)
        web.move_to(RIGHT * 4.0 + DOWN * 1.9)
        web_t = label(r"all 15 trillion tokens (6{,}000 H100 hours)", font_size=22).next_to(web, DOWN, buff=0.15)
        a4 = Arrow(clf.get_right(), web.get_left(), buff=0.15, color=GREY_B, stroke_width=3)
        rng = np.random.default_rng(3)
        web_scores = rng.choice([0, 1, 1, 1, 2, 2, 3, 4], size=len(web))
        keep_t = label(r"keep score $\geq 3$", font_size=26, color=C.EDU).next_to(web, UP, buff=0.15)
        head = label(r"Model-based filtering: FineWeb-Edu", font_size=38).to_edge(UP, buff=0.4)
        src = source(r"Penedo et al., \emph{The FineWeb Datasets} (2024); grades on screen are illustrative")
        with self.voiceover(
            "Hand-written rules catch obvious junk, but they can't tell whether a page is worth learning from. For "
            "that, labs use models. <bookmark mark='a'/> FineWeb-Edu asked Llama 3 70B to grade half a million pages "
            "for educational value, from zero to five, <bookmark mark='b'/> trained a small, fast classifier to "
            "imitate those grades, <bookmark mark='c'/> and ran it over all fifteen trillion tokens. "
            "<bookmark mark='d'/> Then it kept the pages scoring three or more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), LaggedStart(*[FadeIn(u, shift=UP * 0.2) for u in unknown], lag_ratio=0.15))
            self.play(FadeIn(worth))
            vo.wait_until("a")
            self.play(FadeOut(worth), ReplacementTransform(unknown, raw), FadeIn(raw_t), run_time=1.0)
            self.play(GrowArrow(a1), FadeIn(llm), FadeIn(llm_t), run_time=0.8)
            self.play(GrowArrow(a2), TransformFromCopy(raw, graded), FadeIn(graded_t), run_time=1.0)
            vo.wait_until("b")
            self.play(Create(a3), FadeIn(a3_t), FadeIn(clf), FadeIn(clf_t), run_time=1.0)
            vo.wait_until("c")
            self.play(GrowArrow(a4), LaggedStart(*[FadeIn(w, scale=0.6) for w in web], lag_ratio=0.04), FadeIn(web_t), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(keep_t), *[w.animate.set_opacity(1.0 if sc >= 3 else 0.2) for w, sc in zip(web, web_scores)],
                      *[w[0].animate.set_stroke(C.EDU, width=2.5) for w, sc in zip(web, web_scores) if sc >= 3])
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
        assert n == 400 and n_all == 1363 and round(100 * keep) == 7 and counts.argmax() == 1
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
            "just seven percent. <bookmark mark='t'/> The top scorer looks like this, and a typical low scorer like "
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
        head = label(r"Keep the best, and rewrite the rest", font_size=34).to_edge(UP, buff=0.35)
        src = source(r"FineWeb (2024); Su et al.\ 2024 (Nemotron-CC); Kimi K2 report (2025); OLMo 3 report (2025)")

        def page(color=GREY_B, fill=0.0, s=1.0):
            r = RoundedRectangle(width=0.36 * s, height=0.46 * s, corner_radius=0.04, stroke_color=color, stroke_width=1.5,
                                 fill_color=color, fill_opacity=fill)
            ln = VGroup(*[Line(LEFT * 0.1 * s, RIGHT * 0.1 * s, stroke_width=1.2, color=GREY_C) for _ in range(3)]).arrange(DOWN, buff=0.07 * s).move_to(r)
            return VGroup(r, ln)

        def titled(title, body, caption):
            return VGroup(label(title, font_size=26), body, label(caption, font_size=20, color=GREY_A)).arrange(DOWN, buff=0.2)
        # FineWeb-Edu: keep 8 in 100
        rng = np.random.default_rng(8)
        kept = set(rng.choice(100, 8, replace=False).tolist())
        grid = VGroup(*[Square(0.17, stroke_width=0, fill_color=C.EDU if i in kept else GREY_D, fill_opacity=1 if i in kept else 0.6)
                        for i in range(100)]).arrange_in_grid(10, 10, buff=0.04)
        pa = titled(r"\textbf{FineWeb-Edu}: keep 8\% (1.3T tokens)", grid, r"matched older datasets with 10$\times$ fewer tokens")
        # Nemotron-CC: rephrase pages with an LLM
        src_pg = page(GREY_B)
        llm = RoundedRectangle(width=1.0, height=0.6, corner_radius=0.1, stroke_color=C.PARAMS, fill_color=C.PARAMS, fill_opacity=0.15)
        llm.add(label(r"LLM", font_size=22).move_to(llm))
        outs = VGroup(*[page(c, 0.15) for c in (C.KEPT, C.EDU, C.USER)]).arrange(DOWN, buff=0.12)
        flow = VGroup(src_pg, llm, outs).arrange(RIGHT, buff=0.6)
        fa = VGroup(Arrow(src_pg.get_right(), llm.get_left(), buff=0.08, stroke_width=3, color=GREY_B),
                    *[Arrow(llm.get_right(), o.get_left(), buff=0.08, stroke_width=2.5, color=GREY_B) for o in outs])
        pb = titled(r"\textbf{Nemotron-CC} (NVIDIA): rephrase", VGroup(flow, fa), r"$\approx$1.9T synthetic tokens")
        # Kimi K2: SimpleQA before/after rephrasing
        qa = bar_rows([(r"original data", 23.8, GREY_B, r"23.8\%"), (r"rephrased", 28.9, C.KEPT, r"28.9\%")], 3.4 / 30,
                      font_size=22, bar_h=0.34, buff=0.16)
        pc = titled(r"\textbf{Kimi K2}: rephrased knowledge data", qa, r"SimpleQA (factual recall) accuracy")
        # OLMo 3: repeat the best data instead of a hard cut
        best = VGroup(*[page(C.EDU, 0.25, 1.4) for _ in range(7)])
        for i, b in enumerate(best):
            b.shift(RIGHT * 0.1 * i + UP * 0.1 * i)
        rest = VGroup(*[page(GREY_B, 0.0, 1.4) for _ in range(3)]).arrange(RIGHT, buff=0.15)
        rep = VGroup(VGroup(best, label(r"best: $\times$7", font_size=22, color=C.EDU)).arrange(DOWN, buff=0.12),
                     VGroup(rest, label(r"the rest: $\times$1", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12)).arrange(RIGHT, buff=0.8, aligned_edge=DOWN)
        pd = titled(r"\textbf{OLMo 3}: repeat the best data", rep, r"up to 7 times, instead of a hard cut")
        panels = VGroup(pa, pb, pc, pd)
        for g, (cx, cy) in zip(panels, [(-3.4, 1.0), (3.4, 1.0), (-3.4, -2.2), (3.4, -2.2)]):
            g.scale_to_fit_height(min(g.height, 2.9)).move_to([cx, cy, 0])
        with self.voiceover(
            "At full scale, FineWeb-Edu kept a similar eight percent of FineWeb, 1.3 trillion tokens, and models "
            "trained on it matched older datasets on knowledge benchmarks with ten times fewer tokens. "
            "<bookmark mark='r'/> Since then, the trend is to rewrite rather than throw away. NVIDIA's Nemotron-CC "
            "used a language model to rephrase web pages, producing almost two trillion synthetic tokens. "
            "<bookmark mark='k'/> Moonshot rephrased Kimi K2's knowledge data, and a factual-recall score rose from "
            "24 to 29 percent. <bookmark mark='o'/> And AI2's OLMo 3 repeats its best data up to seven times, instead "
            "of drawing a hard line."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), FadeIn(pa[0]), FadeIn(pa[2]), LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.01))
            vo.wait_until("r")
            self.play(FadeIn(pb[0]), FadeIn(pb[2]), FadeIn(src_pg), GrowArrow(fa[0]), FadeIn(llm))
            self.play(*[GrowArrow(a) for a in fa[1:]], LaggedStart(*[FadeIn(o, shift=RIGHT * 0.1) for o in outs], lag_ratio=0.2))
            vo.wait_until("k")
            self.play(FadeIn(pc[0]), FadeIn(pc[2]), *[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT), FadeIn(r[2])) for r in qa])
            vo.wait_until("o")
            self.play(FadeIn(pd[0]), FadeIn(pd[2]), FadeIn(rep[1]), LaggedStart(*[FadeIn(b, shift=UP * 0.05) for b in best], lag_ratio=0.12),
                      FadeIn(rep[0][1]))
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

    # ------------------------------------------------------------------
    def bpe_math(self):
        b = load("math")["bpe"]
        steps = b["steps"]
        assert [st["pair"] for st in steps] == b["trained_merges"]  # recounting reproduces the trained merges
        assert steps[0]["pair"] == ["Ġ", "t"] and steps[0]["count"] == 6_071_917 and steps[5]["pair"] == ["Ġt", "he"]
        assert b["sentence_tokens"] == ["the", "Ġc", "at", "Ġs", "at", "Ġon", "Ġthe", "Ġmat"] and len(b["sentence"]) == 22

        def tk(t, color=C.TOKEN, fs=24):
            m = Mono(t.replace("Ġ", "␣"), font_size=fs)
            bx = RoundedRectangle(width=m.width + 0.14, height=0.42, corner_radius=0.05, stroke_color=color,
                                  stroke_width=1.3, fill_color=color, fill_opacity=0.14)
            return VGroup(bx, m.move_to(bx))
        head = label(r"Byte-pair encoding, on our real training text", font_size=34).to_edge(UP, buff=0.35)
        sub = label(rf"{b['total_words'] / 1e6:.1f} million words ({b['unique_words']:,} distinct); ␣ marks a space".replace(",", "{,}"),
                    font_size=24, color=GREY_A).next_to(head, DOWN, buff=0.15)
        sub = VGroup(label(rf"{b['total_words'] / 1e6:.1f} million words ({b['unique_words']:,} distinct);".replace(",", "{,}"),
                           font_size=24, color=GREY_A), Mono("␣", font_size=22, color=GREY_A),
                     label(r"marks a space", font_size=24, color=GREY_A)).arrange(RIGHT, buff=0.12).next_to(head, DOWN, buff=0.15)
        # step 1: the ranking
        rank = VGroup()
        for x, y, n in steps[0]["top"][:3]:
            rank.add(VGroup(tk(x), Mono("+", font_size=22), tk(y),
                            label(rf"{n:,}".replace(",", "{,}"), font_size=26, color=C.DATA)).arrange(RIGHT, buff=0.15))
        rank.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rt = label(r"step 1: count every adjacent pair", font_size=26).next_to(rank, UP, buff=0.25).align_to(rank, LEFT)
        rgroup = VGroup(rt, rank).to_edge(LEFT, buff=0.6).shift(UP * 0.3)
        win = SurroundingRectangle(rank[0], buff=0.08, color=C.DATA, stroke_width=2)
        # the merge list
        rows = VGroup()
        for i, st in enumerate(steps):
            x, y = st["pair"]
            rows.add(VGroup(Mono(f"{i + 1}.", font_size=22, color=GREY_A), tk(x), Mono("+", font_size=22), tk(y),
                            MathTex(r"\rightarrow", font_size=28), tk(x + y, C.KEPT),
                            label(rf"{st['count']:,}".replace(",", "{,}"), font_size=24, color=C.DATA)).arrange(RIGHT, buff=0.14))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        mt = label(r"merge the most frequent pair, recount, repeat", font_size=26).next_to(rows, UP, buff=0.25).align_to(rows, LEFT)
        mgroup = VGroup(mt, rows).to_edge(RIGHT, buff=0.6).shift(UP * 0.1)
        if mgroup.height > 5.6:
            mgroup.scale_to_fit_height(5.6)
        # the sentence
        bytes_ = VGroup(*[tk(ch.replace(" ", "Ġ"), GREY_B, 20) for ch in b["sentence"]]).arrange(RIGHT, buff=0.04)
        final = VGroup(*[tk(t, C.KEPT, 24) for t in b["sentence_tokens"]]).arrange(RIGHT, buff=0.06)
        lb = label(r"22 bytes", font_size=24, color=GREY_A)
        lf = label(r"8 tokens", font_size=24, color=C.KEPT)
        sent = VGroup(VGroup(lb, bytes_).arrange(RIGHT, buff=0.3), VGroup(lf, final).arrange(RIGHT, buff=0.3)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "How does byte-pair encoding choose its pieces? Start from single bytes, and count every adjacent pair "
            "in the training text. <bookmark mark='c'/> In our 57 million words, the most common pair is a space "
            "followed by t: six million times. <bookmark mark='m'/> Merge it into one token, recount, and repeat: "
            "space-a, then h-e, i-n, r-e. <bookmark mark='t'/> At the sixth merge, space-t plus h-e makes space-the. "
            "Recounting the pairs ourselves gives exactly the merges our tokenizer learned. <bookmark mark='e'/> After "
            "two thousand merges, 'the cat sat on the mat', twenty-two bytes, becomes eight tokens."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("c")
            self.play(FadeIn(rt), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rank], lag_ratio=0.3))
            self.play(Create(win))
            vo.wait_until("m")
            self.play(FadeIn(mt), LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in rows[:5]], lag_ratio=0.4), run_time=3.0)
            vo.wait_until("t")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.1) for r in rows[5:]], lag_ratio=0.4), run_time=1.5)
            self.play(Indicate(rows[5], color=C.KEPT, scale_factor=1.05))
            vo.wait_until("e")
            self.play(FadeOut(rgroup), FadeOut(win), FadeIn(sent[0]))
            self.play(TransformFromCopy(sent[0][1], sent[1][1]), FadeIn(sent[1][0]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()
