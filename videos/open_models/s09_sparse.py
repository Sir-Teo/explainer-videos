from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    cfg, label, layer_strip, model_tag, note, schematic_tag, show_chapter_card, source,
)

# GLM-5 technical report (arXiv:2602.15763), Table 3: base models after DSA continued pre-training.
DSA_TABLE = {"MQ-NIAH-128k": (100.0, 100.0), "MV-NIAH-128k": (95.5, 97.0), "SQuAD-128k": (79.7, 86.0),
             "HotpotQA-128k": (66.3, 63.0)}


class SparseAttention(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 8, "GLM: read only what matters")
        self.c = cfg("glm")
        self.tag = model_tag("glm")
        self.add(self.tag)
        self.select()
        self.indexer()
        self.index_share()
        self.training()

    # ------------------------------------------------------------------
    def select(self):
        c = self.c
        assert c["index_topk"] == 2048
        n, k = 96, 12
        rng = np.random.default_rng(11)
        score = rng.gamma(1.2, 0.18, n)
        for p in (4, 5, 31, 52, 53, 54, 77, 88, 93, 94, 95):
            score[p] += rng.uniform(0.9, 1.4)
        top = np.argsort(-score)[:k]
        assert 4 in top and 31 in top
        cw = 0.1
        toks = VGroup(*[Rectangle(width=cw, height=0.42, stroke_width=0, fill_color=C.LATENT, fill_opacity=0.45)
                        for _ in range(n)]).arrange(RIGHT, buff=0.015).move_to(DOWN * 0.9 + LEFT * 0.7)
        cur = Rectangle(width=cw * 2.2, height=0.6, stroke_width=0, fill_color=C.QUERY, fill_opacity=0.95)
        cur.next_to(toks, RIGHT, buff=0.25)
        cur_l = label(r"new\\token", font_size=22, color=C.QUERY).next_to(cur, DOWN, buff=0.12)
        toks_l = label(r"every earlier token's cached latent (a million of them; 96 drawn)", font_size=24, color=C.LATENT)
        toks_l.next_to(toks, DOWN, buff=1.75)
        bars = VGroup()
        for i, s in enumerate(score):
            b = Rectangle(width=cw, height=1.6 * s / score.max(), stroke_width=0, fill_color=C.INDEXER, fill_opacity=0.75)
            b.next_to(toks[i], UP, buff=0.08)
            bars.add(b)
        bars_l = label(r"lightning indexer: a relevance score for every earlier token", font_size=26, color=C.INDEXER)
        bars_l.next_to(bars, UP, buff=0.35).align_to(toks, LEFT)
        thr = np.sort(score)[::-1][k - 1]
        cut = DashedLine(toks.get_left() + UP * (0.29 + 1.6 * thr / score.max()) + LEFT * 0.1,
                         toks.get_right() + UP * (0.29 + 1.6 * thr / score.max()) + RIGHT * 0.1, color=WHITE, stroke_width=2)
        cut.set_y(toks.get_top()[1] + 0.08 + 1.6 * thr / score.max() - 0.01)
        cut_l = label(r"keep the top 2{,}048 (here: 12)", font_size=24).next_to(cut, UP, buff=0.1).align_to(cut, RIGHT)
        arcs = VGroup(*[ArcBetweenPoints(toks[i].get_bottom() + DOWN * 0.02, cur.get_bottom(), angle=0.9, color=C.ATTN,
                                         stroke_width=2.5) for i in sorted(top)])
        far = label(r"chosen by content, not position: the start of the text can be selected", font_size=26,
                    color=YELLOW).to_edge(UP, buff=0.95)
        with self.voiceover(
            "So GLM adds a second idea, DeepSeek Sparse Attention. <bookmark mark='i'/> Before the real attention runs, "
            "a tiny scorer called the lightning indexer looks at every earlier token, and gives each one a relevance "
            "score. <bookmark mark='k'/> Then each token keeps just its top 2,048, <bookmark mark='a'/> and the real "
            "attention runs only over those. <bookmark mark='c'/> Unlike a sliding window, which decides by position, "
            "this decides by content: a token from the very beginning of a long document can still be picked, if it "
            "matters."
        ) as vo:
            self.play(FadeIn(toks, lag_ratio=0.005), FadeIn(toks_l), FadeIn(cur), FadeIn(cur_l), run_time=1.2)
            vo.wait_until("i")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.01), FadeIn(bars_l), run_time=1.8)
            vo.wait_until("k")
            self.play(Create(cut), FadeIn(cut_l))
            self.play(*[bars[i].animate.set_fill(opacity=0.15) for i in range(n) if i not in top],
                      *[toks[i].animate.set_fill(C.INDEXER, opacity=0.95) for i in top],
                      *[toks[i].animate.set_fill(opacity=0.12) for i in range(n) if i not in top])
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.08), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(far), Indicate(toks[4], color=YELLOW, scale_factor=1.8), Indicate(toks[5], color=YELLOW,
                                                                                                  scale_factor=1.8))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def indexer(self):
        c = self.c
        assert c["index_heads"] == 32 and c["index_head_dim"] == 128
        f = MathTex(r"I_{t,s}", "=", r"\sum_{j=1}^{32}", r"w_{t,j}", r"\cdot", r"\mathrm{ReLU}", r"(", r"\vec q^{\,I}_{t,j}",
                    r"\cdot", r"\vec k^{\,I}_s", r")", font_size=48).move_to(UP * 1.6)
        f[0].set_color(C.INDEXER)
        f[3].set_color(C.INDEXER)
        f[7].set_color(C.QUERY)
        f[9].set_color(C.KEY)
        notes = VGroup(
            label(r"32 small heads, 128 dimensions each, one shared key per token", font_size=28),
            label(r"keep only the positive part of each match (ReLU), add the heads with learned weights", font_size=28),
            label(r"computed in 8-bit arithmetic; caches just 128 numbers per token", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(f, DOWN, buff=0.6)
        save = VGroup(MathTex(r"2{,}048", r"\text{ instead of }", r"1{,}000{,}000", font_size=42),
                      label(r"$\approx 500\times$ fewer entries for the real attention to read", font_size=30, color=YELLOW))
        save[0][0].set_color(C.INDEXER)
        save.arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.75)
        src = note(r"indexer formula: DeepSeek-V3.2 (DeepSeek-AI, 2025)").to_corner(DR, buff=0.25)
        with self.voiceover(
            "The indexer is like attention's cheap little cousin. <bookmark mark='f'/> It has 32 small heads, of 128 "
            "dimensions each. Each head compares the current token's indexer query with a past token's indexer key, "
            "<bookmark mark='r'/> keeps only the positive part, and the heads' results are added up with learned weights. "
            "<bookmark mark='c'/> It runs in 8-bit arithmetic, and needs only a small cache of its own. "
            "<bookmark mark='s'/> The savings: with a million tokens of context, the real attention reads 2,048 entries "
            "instead of a million, about five hundred times fewer. The indexer still has to scan everything, but each of "
            "its comparisons is far cheaper."
        ) as vo:
            vo.wait_until("f")
            self.play(Write(f), FadeIn(src), FadeIn(notes[0]))
            vo.wait_until("r")
            self.play(FadeIn(notes[1]), Indicate(f[5], color=YELLOW))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("s")
            self.play(FadeIn(save, shift=UP * 0.2))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def index_share(self):
        c = self.c
        types = c["indexer_types"]
        assert len(types) == 78 and types.count("full") == 21
        strip = layer_strip(["idx" if t == "full" else "sh" for t in types], {"idx": C.INDEXER, "sh": C.INDEXER},
                            cell=0.13, gap=0.035, height=0.8, outline_types=("sh",)).move_to(DOWN * 0.3)
        arrows = VGroup()
        last = 0
        for i, t in enumerate(types):
            if t == "full":
                last = i
            else:
                arrows.add(CurvedArrow(strip[last].get_top() + UP * 0.05, strip[i].get_top() + UP * 0.05, angle=-1.2,
                                       color=C.INDEXER, stroke_width=1.2, tip_length=0.08))
        leg = VGroup(
            VGroup(Rectangle(width=0.2, height=0.35, stroke_width=0, fill_color=C.INDEXER, fill_opacity=0.9),
                   label(r"runs its own indexer (21 layers)", font_size=26, color=C.INDEXER)).arrange(RIGHT, buff=0.15),
            VGroup(Rectangle(width=0.2, height=0.35, stroke_width=1.2, stroke_color=C.INDEXER, fill_opacity=0.1),
                   label(r"reuses the choices from below (57 layers)", font_size=26)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(strip, DOWN, buff=0.6)
        title = label(r"IndexShare: GLM-5.3's 78 layers, from its config", font_size=32).to_edge(UP, buff=0.9)
        obs = label(r"neighboring layers pick 70--100\% of the same tokens", font_size=28, color=YELLOW)
        obs.next_to(title, DOWN, buff=0.35)
        res = label(r"$2.9\times$ less compute per token at a million tokens (Z.ai)", font_size=28, color=YELLOW)
        res.to_edge(DOWN, buff=0.6)
        src = note(r"overlap: IndexCache (Bai et al., Tsinghua \& Z.ai, 2026), measured on a 30B sparse-attention model",
                   font_size=20).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "GLM-5.2, the base model GLM-5.3 is built on, noticed something about the indexer's choices. "
            "<bookmark mark='o'/> Neighboring layers pick almost the same tokens. In Z.ai's measurements on a smaller "
            "model, adjacent layers shared 70 to 100 percent of their selections. <bookmark mark='s'/> So in GLM-5.3, "
            "only about one layer in four runs the indexer, <bookmark mark='r'/> and the layers above it reuse its "
            "choices. Here's the real layout: 21 of the 78 layers have an indexer of their own. <bookmark mark='f'/> Z.ai "
            "reports that this cuts the compute per token by 2.9 times, at a million tokens of context."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("o")
            self.play(FadeIn(obs), FadeIn(src))
            vo.wait_until("s")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in strip], lag_ratio=0.015), run_time=1.6)
            vo.wait_until("r")
            self.play(Create(arrows, lag_ratio=0.02), FadeIn(leg), run_time=2)
            vo.wait_until("f")
            self.play(FadeIn(res, shift=UP * 0.2))
        self.clear_scene(self.tag)

    # ------------------------------------------------------------------
    def training(self):
        steps = VGroup(
            block_text(r"start: a trained model\\with dense attention", GREY_B),
            block_text(r"warm-up: train only the\\indexer, to imitate where\\dense attention looks", C.INDEXER),
            block_text(r"then: let the whole model\\adapt to sparse attention", C.GLM),
        ).arrange(RIGHT, buff=0.7).move_to(UP * 1.3)
        arrows = VGroup(*[Arrow(steps[i].get_right(), steps[i + 1].get_left(), buff=0.1, color=WHITE) for i in range(2)])
        rows = VGroup()
        head = VGroup(label("", font_size=24), label(r"dense (MLA)", font_size=26, color=GREY_A),
                      label(r"sparse (DSA)", font_size=26, color=C.INDEXER))
        rows.add(head)
        for name, (a, b) in DSA_TABLE.items():
            rows.add(VGroup(label(name, font_size=26), label(f"{a:.1f}", font_size=26), label(f"{b:.1f}", font_size=26)))
        for i, r in enumerate(rows):
            y = -0.7 - 0.5 * i
            r[0].move_to([-2.2, y, 0], aligned_edge=RIGHT)
            r[1].move_to([0.6, y, 0])
            r[2].move_to([2.8, y, 0])
        src = source(r"GLM-5 technical report, Section 2.1.1 and Table 3 (base models)")
        with self.voiceover(
            "How do you train a scorer like this? Not from scratch. <bookmark mark='a'/> GLM-5 started from a model with "
            "ordinary dense attention, <bookmark mark='b'/> first trained the indexer alone, to imitate where dense "
            "attention was looking, <bookmark mark='c'/> and then let the whole model adapt to reading sparsely. "
            "<bookmark mark='t'/> On long-context tests at 128 thousand tokens, the sparse model came out about even with "
            "the dense one: a little better on some, a little worse on others."
        ) as vo:
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                anims = [FadeIn(steps[i], shift=RIGHT * 0.2)]
                if i:
                    anims.append(GrowArrow(arrows[i - 1]))
                self.play(*anims)
            vo.wait_until("t")
            self.play(FadeIn(rows, lag_ratio=0.1), FadeIn(src), run_time=1.5)
        self.clear_scene()


def block_text(text, color) -> VGroup:
    t = label(text, font_size=24)
    box = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.35, corner_radius=0.1, stroke_color=color,
                           stroke_width=2, fill_color=color, fill_opacity=0.15)
    return VGroup(box, t.move_to(box))
