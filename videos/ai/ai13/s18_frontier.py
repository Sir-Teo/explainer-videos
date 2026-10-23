from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, K, PART, Q, V

MEM, SPARSE, LIN, INSIDE = C.LATENT, C.INDEXER, C.MEMORY, C.BITS


def panel(title, color, items, width=6.4, part=None):
    head = label(title, font_size=26, color=color)
    rows = VGroup(*[label(t, font_size=20, color=GREY_A) for t in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    if body.width > width - 0.5:
        body.scale_to_fit_width(width - 0.5)
    if part:
        tag = label(part, font_size=20, color=color).next_to(head, RIGHT, buff=0.3)
        body.add(tag)
    box = RoundedRectangle(width=width, height=body.height + 0.4, corner_radius=0.12, stroke_color=color,
                           stroke_width=1.5, fill_color="#0B0F17", fill_opacity=0.9)
    body.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
    return VGroup(box, body)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.map()
        self.hybrids()

    def card(self):
        card = chapter_card(17, r"Attention in 2026", r"What are the newest models changing, and why?", part=PART)
        with self.voiceover("Chapter seventeen. Attention in 2026."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def map(self):
        f = cmath(r"\operatorname{softmax}\!\Big(", r"\frac{Q K^\top}{\sqrt{d}}", r"+", r"M", r"\Big)", r"\,V",
                  font_size=44, colors={r"\frac{Q K^\top}{\sqrt{d}}": A, r"\,V": V, r"M": GREY_A}).move_to([0, 0.2, 0])
        p_in = panel(r"inside the softmax", INSIDE, [
            r"sink logits \ (gpt-oss, 2025)", r"output gates \ (Qwen3-Next 2025, \ Kimi K3 2026)",
            r"QK-norm \ (Qwen3, \ Gemma 3, \ 2025)", r"layers without positions \ (Llama 4, 2025)"],
            width=6.3, part=r"this part").move_to([-3.4, 2.55, 0])
        p_mem = panel(r"a smaller memory of keys and values", MEM, [
            r"grouped queries share keys and values \ (GQA, 2023)",
            r"keys and values from a low-rank latent \ (MLA: \ DeepSeek-V2, 2024)"], width=6.3,
            part=r"Part 15").move_to([3.4, 2.55, 0])
        p_sp = panel(r"look at only some of the past", SPARSE, [
            r"sliding windows \ (Mistral 2023; \ gpt-oss: $128$ tokens)", r"natively sparse attention \ (NSA, DeepSeek, 2025)",
            r"an indexer picks the keys \ (DSA: \ DeepSeek-V3.2, 2025)",
            r"compressed sparse attention, \ $1$M tokens \ (DeepSeek-V4, 2026)"], width=6.3,
            part=r"Part 16").move_to([-3.4, -2.35, 0])
        p_lin = panel(r"replace most of it with a fixed-size memory", LIN, [
            r"gated DeltaNet, \ $3$ layers to $1$ \ (Qwen3-Next 2025, \ Qwen3.5 2026)",
            r"Kimi Delta Attention \ (Kimi Linear 2025; \ Kimi K3 2026)"], width=6.3,
            part=r"Part 15").move_to([3.4, -2.35, 0])
        arrows = VGroup(*[Arrow(f.get_center(), p.get_center(), buff=1.25, color=GREY_D, stroke_width=2,
                                max_tip_length_to_length_ratio=0.08) for p in (p_in, p_mem, p_sp, p_lin)])
        cite_ = note(r"each from its paper or model card").to_corner(DR, buff=0.15)
        with self.voiceover(
            "Every model in 2026 still computes this formula somewhere. What has changed is where, and how much. "
            "<bookmark mark='a'/> Inside the softmax, the fixes of the last few chapters: sink logits in gpt-oss, "
            "output gates in Qwen3-Next and Kimi K3, QK-norm in Qwen3 and Gemma 3, and in Llama 4, layers with no "
            "positions at all. <bookmark mark='b'/> The keys and values every past token leaves behind have been "
            "shrunk: grouped-query attention shares them between heads, and DeepSeek's multi-head latent attention "
            "rebuilds them from a small latent vector, the low-rank idea of chapter four applied to memory. "
            "<bookmark mark='c'/> Many models look at only part of the past: a sliding window in most layers, or a "
            "learned choice of which keys matter. DeepSeek's sparse attention lets a small, fast indexer pick a few "
            "thousand past tokens for each query, and DeepSeek-V4 compresses and selects to read a million tokens. "
            "<bookmark mark='d'/> And some models replace most of their attention layers with a fixed-size memory "
            "that is updated as they read: three such layers for every attention layer in Qwen3-Next and Qwen3.5, "
            "Kimi Delta Attention in Kimi Linear and Kimi K3."
        ) as vo:
            self.play(FadeIn(f))
            vo.wait_until("a")
            self.play(GrowArrow(arrows[0]), FadeIn(p_in))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[1]), FadeIn(p_mem))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[2]), FadeIn(p_sp))
            vo.wait_until("d")
            self.play(GrowArrow(arrows[3]), FadeIn(p_lin), FadeIn(cite_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hybrids(self):
        n_kda, n_mla = 69, 24  # Kimi K3 model card (2026): 93 layers, 69 KDA + 24 gated MLA
        cells = VGroup()
        for i in range(n_kda + n_mla):
            full = (i + 1) % 4 == 0 or i == n_kda + n_mla - 1
            cells.add(Rectangle(width=0.12, height=0.7, stroke_width=0, fill_color=A if full else LIN, fill_opacity=0.9))
        cells.arrange(RIGHT, buff=0.015).move_to([0, 1.6, 0])
        if cells.width > 13.0:
            cells.scale_to_fit_width(13.0)
        cl = VGroup(label(rf"Kimi K3 (2026): \ ${n_kda + n_mla}$ layers \ --- \ ${n_kda}$ of Kimi Delta Attention, "
                          rf"\ ${n_mla}$ of gated attention", font_size=26, color=GREY_A).next_to(cells, UP, buff=0.3),
                    note(r"layer order schematic; \ counts from the Kimi K3 model card", font_size=18).next_to(cells, DOWN, buff=0.15))
        keys = VGroup(VGroup(Square(0.25, fill_color=LIN, fill_opacity=0.9, stroke_width=0),
                             label(r"a fixed-size memory, \ updated as it reads", font_size=24, color=LIN)).arrange(RIGHT, buff=0.15),
                      VGroup(Square(0.25, fill_color=A, fill_opacity=0.9, stroke_width=0),
                             label(r"full attention, \ to recall exactly", font_size=24, color=A)).arrange(RIGHT, buff=0.15))
        keys.arrange(RIGHT, buff=0.8).move_to([0, -0.2, 0])
        why_ = VGroup(
            label(r"attention: \ exact recall of anything in context, \ cost growing with every token", font_size=26,
                  color=A),
            label(r"a fixed memory: \ constant cost per token, \ but it must decide what to forget", font_size=26,
                  color=LIN),
            label(r"a few attention layers keep the recall; \ the rest keep the cost down", font_size=26, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([0, -2.2, 0])
        with self.voiceover(
            "Here is what such a hybrid looks like: Kimi K3, released in 2026, has 93 layers, and only 24 of them "
            "are full attention. <bookmark mark='a'/> The rest keep a fixed-size memory, updated as they read. "
            "<bookmark mark='b'/> Why keep any attention at all? Because attention can recall anything in its "
            "context exactly, as the induction heads of chapter fourteen did, while a fixed memory has to decide what to forget. A few "
            "attention layers keep the recall, the rest keep the cost down. <bookmark mark='c'/> How that memory "
            "works, and why it is attention in disguise, is where we go next, through the lineage of the models "
            "themselves in Part 14, to memory in Part 15."
        ) as vo:
            self.play(FadeIn(cl[0]), LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.01), FadeIn(cl[1]),
                      run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(keys))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(w_, shift=UP * 0.1) for w_ in why_], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("c")
            self.play(Indicate(why_[2]))
        self.wait(0.3)
        self.clear_scene()
