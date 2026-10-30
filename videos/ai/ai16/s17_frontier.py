from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai16.common import (BLOCKC, EXPERTC, F, FULLC, INDEXC, PART, ROUTER, SHAREDC, billions, load, take_away)

SHORT = {"switch": r"Switch-C", "glam": r"GLaM", "mixtral": r"Mixtral", "dsv2": r"DeepSeek-V2", "dsv3": r"DeepSeek-V3",
         "llama4": r"Llama 4 Maverick", "qwen3": r"Qwen3-235B", "kimik2": r"Kimi K2", "glm45": r"GLM-4.5",
         "gptoss": r"gpt-oss-120b", "qwen3next": r"Qwen3-Next", "minimax": r"MiniMax-M2", "glm5": r"GLM-5",
         "qwen35": r"Qwen3.5-397B", "dsv4": r"DeepSeek-V4-Pro", "kimik3": r"Kimi K3", "mistral4": r"Mistral Large 4"}


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.experts()
        self.share()
        self.attention()

    def card(self):
        card = chapter_card(16, r"The frontier, late 2026", r"How sparse are the biggest models now?", lit=(2025, 2026),
                            part=PART)
        with self.voiceover("Chapter sixteen. The frontier, late 2026."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def experts(self):
        c = load("configs")
        rows = [r for r in c["rows"] if r["year"] >= 2023]
        x0, x1 = 2023.4, 2026.95
        ax = Axes(x_range=[x0, x1, 1], y_range=[0.7, 3.1, 1], x_length=9.2, y_length=4.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-0.9, -0.3, 0])
        yt = VGroup(*[MathTex(str(v), font_size=20, color=GREY_B).next_to(ax.c2p(x0, math.log10(v)), LEFT, buff=0.1)
                      for v in (8, 32, 128, 512)])
        xt = VGroup(*[MathTex(str(y), font_size=20, color=GREY_B).next_to(ax.c2p(y + 0.5, 0.7), DOWN, buff=0.1)
                      for y in (2024, 2025, 2026)])
        yl = label(r"routed experts per layer \ (log scale); \ dot size: \ total parameters", font_size=20,
                   color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        dots, labs = VGroup(), VGroup()
        for r in rows:
            rad = 0.05 + 0.05 * (math.log10(r["total"]) - 10)
            dots.add(Dot(ax.c2p(r["year"], math.log10(r["experts"])), radius=max(rad, 0.05), color=EXPERTC if not r["shared"] else SHAREDC))
            labs.add(label(SHORT[r["key"]] + rf" \ ${r['k']}$" + (rf"$+{r['shared']}$" if r["shared"] else ""), font_size=16,
                           color=GREY_A))
        place_labels(list(dots), list(labs), bounds=(-6.8, 6.8, -3.0, 2.6))
        key = VGroup(label(r"purple: \ routed only", font_size=18, color=EXPERTC),
                     label(r"lilac: \ $+$ shared experts", font_size=18, color=SHAREDC),
                     label(r"label: \ chosen per token", font_size=18, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        key.to_corner(DR, buff=0.3)
        src = note(r"each maker's report or model card \ (checked October 2026)", font_size=16).to_corner(DL, buff=0.2)
        k3 = next(r for r in rows if r["key"] == "kimik3")
        mx = next(r for r in rows if r["key"] == "mixtral")
        with self.voiceover(
            "Where has all this led? Here are the large open mixtures of the last three years, by how many experts "
            "each layer holds. <bookmark mark='a'/> In December 2023 Mixtral had eight. A year later DeepSeek-V3 had "
            "two hundred and fifty-six, plus a shared one. <bookmark mark='b'/> In 2025 the field followed: Qwen3, "
            "Kimi K2 with three hundred and eighty-four, GLM-4.5, OpenAI's gpt-oss, MiniMax, and Qwen3-Next with "
            "five hundred and twelve. <bookmark mark='c'/> And in 2026, GLM-5, Qwen3.5, DeepSeek-V4, Mistral Large "
            f"4 released this week, and Kimi K3, with {k3['experts']} experts in a layer and {k3['k']} chosen. "
            "Almost all of them are fine-grained, and most keep a shared expert."
        ) as vo:
            self.play(Create(ax), FadeIn(yt), FadeIn(xt), FadeIn(yl), FadeIn(key), FadeIn(src))
            groups = [[i for i, r in enumerate(rows) if r["year"] < 2025],
                      [i for i, r in enumerate(rows) if 2025 <= r["year"] < 2026],
                      [i for i, r in enumerate(rows) if r["year"] >= 2026]]
            for mk, idx in zip("abc", groups):
                vo.wait_until(mk)
                self.play(LaggedStart(*[AnimationGroup(FadeIn(dots[i], scale=0.5), FadeIn(labs[i])) for i in idx],
                                      lag_ratio=0.2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def share(self):
        c = load("configs")
        rows = [r for r in c["rows"] if r["active"] and r["year"] >= 2023]
        rows.sort(key=lambda r: r["year"])
        lo, hi = 9.0, 12.6
        sc = 6.0 / (hi - lo)
        g = VGroup()
        for i, r in enumerate(rows):
            y = 3.0 - i * 0.39
            nm = label(SHORT[r["key"]] + rf" \ ({r['date'][:4]})", font_size=17, color=WHITE).move_to([-2.9, y, 0], aligned_edge=RIGHT)
            wt = (math.log10(r["total"]) - lo) * sc
            wa = (math.log10(r["active"]) - lo) * sc
            bt = Rectangle(width=wt, height=0.28, stroke_width=0, fill_color=GREY_D, fill_opacity=0.9).move_to([-2.6 + wt / 2, y, 0])
            ba = Rectangle(width=wa, height=0.28, stroke_width=0, fill_color=C.BITS, fill_opacity=0.9).move_to([-2.6 + wa / 2, y, 0])
            vt = label(rf"${billions(r['total'])}$ \ \ ${100 * r['frac']:.1f}\%$ used", font_size=16, color=GREY_B).next_to(bt, RIGHT, buff=0.1)
            g.add(VGroup(nm, bt, ba, vt))
        key = VGroup(label(r"all parameters", font_size=20, color=GREY_B), label(r"used per token", font_size=20, color=C.BITS),
                     label(r"(log scale)", font_size=18, color=GREY_C)).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.25)
        fr = {r["key"]: r["frac"] for r in rows}
        lowest = min(rows, key=lambda r: r["frac"])
        sparsest = SHORT_SPOKEN.get(lowest["key"], lowest["name"])
        with self.voiceover(
            "And by the share of the model each token uses. <bookmark mark='a'/> Mixtral used "
            f"{100 * fr['mixtral']:.0f} percent of its weights per token; DeepSeek-V3, {100 * fr['dsv3']:.1f}. "
            f"<bookmark mark='b'/> The newest use three to five percent: DeepSeek-V4-Pro {100 * fr['dsv4']:.1f}, "
            f"Kimi K3 {100 * fr['kimik3']:.1f}, and the sparsest here, {sparsest}, "
            f"{100 * lowest['frac']:.1f}. A trillion-parameter model that costs per token what a thirty- to fifty-billion "
            "dense model costs. <bookmark mark='c'/> Mixtures are also in the closed models: Google's Gemini 1.5 and "
            "2.5 reports describe sparse mixtures of experts, and OpenAI's open gpt-oss is one, though most labs "
            "don't publish their architecture."
        ) as vo:
            self.play(FadeIn(key), LaggedStart(*[FadeIn(VGroup(r_[0], r_[1], r_[3])) for r_ in g], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(r_[2], LEFT) for r_ in g], lag_ratio=0.1), run_time=2.5)
            vo.wait_until("b")
            lows = [i for i, r in enumerate(rows) if r["frac"] < 0.05]
            self.play(*[Indicate(g[i][2], color=C.BITS, scale_factor=1.05) for i in lows])
            vo.wait_until("c")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attention(self):
        rows = [
            (r"Feb 2025", r"NSA \ (DeepSeek)", r"compressed blocks, \ chosen blocks, \ a window; \ trained sparse from the start", BLOCKC),
            (r"Feb 2025", r"MoBA \ (Moonshot)", r"chooses blocks by their mean key; \ serves Kimi's long requests", BLOCKC),
            (r"Sep 2025", r"DSA \ (DeepSeek-V3.2)", r"a lightning indexer picks $2{,}048$ tokens", INDEXC),
            (r"Oct 2025", r"MiniMax-M2", r"full attention in every layer: \ its efficient hybrids fell short on multi-hop reasoning", FULLC),
            (r"Feb 2026", r"GLM-5", r"adopts DeepSeek's sparse attention", INDEXC),
            (r"Apr 2026", r"DeepSeek-V4", r"compress, \ then choose: \ CSA and HCA", INDEXC),
            (r"Jun 2026", r"MiniMax-M3", r"back to sparse: \ MiniMax Sparse Attention, \ a million tokens", INDEXC),
            (r"Jul 2026", r"Kimi K3", r"mostly linear attention (Part 15): \ $69$ KDA and $24$ MLA layers", C.MEMORY),
        ]
        tbl = VGroup()
        for d_, nm, what, col in rows:
            tbl.add(VGroup(label(d_, font_size=20, color=GREY_B), label(nm, font_size=22, color=col),
                           label(what, font_size=19, color=GREY_A)))
        w0, w1 = max(r[0].width for r in tbl), max(r[1].width for r in tbl)
        for i, r in enumerate(tbl):
            y = 2.4 - i * 0.62
            r[0].move_to([-6.4 + w0 / 2, y, 0])
            r[1].move_to([-6.4 + w0 + 0.4 + r[1].width / 2, y, 0])
            r[2].move_to([-6.4 + w0 + 0.8 + w1 + r[2].width / 2, y, 0])
        if tbl.get_right()[0] > 6.8:
            tbl.scale_to_fit_width(13.2).move_to([0, tbl.get_y(), 0])
        head = label(r"Sparse attention since 2025", font_size=32).to_edge(UP, buff=0.3)
        ta = take_away(r"the 2026 recipe: \ fine-grained experts, \ a shared one, \ loss-free balancing, \ and attention "
                       r"that compresses and chooses", color=ROUTER, font_size=22)
        with self.voiceover(
            "And attention. <bookmark mark='a'/> In February 2025, DeepSeek's native sparse attention and Moonshot's "
            "MoBA both chose blocks of the past, and MoBA was already serving Kimi's long requests. "
            "<bookmark mark='b'/> In September, DeepSeek-V3.2's indexer chose single tokens. <bookmark mark='c'/> Not "
            "everyone was convinced: MiniMax went back to full attention for M2, saying its efficient hybrids "
            "matched full attention on the usual benchmarks but fell short on multi-step reasoning. <bookmark mark='d'/> But in 2026 GLM-5 adopted DeepSeek's sparse "
            "attention, DeepSeek-V4 compressed before choosing, MiniMax came back to sparse attention for M3, and Kimi K3 went mostly linear, part fifteen's "
            "subject. <bookmark mark='e'/> The 2026 recipe, then: many fine experts, a shared one, balancing that "
            "steers instead of penalizing, and attention that compresses, then chooses."
        ) as vo:
            self.play(FadeIn(head))
            for mk, idx in zip("abcd", ([0, 1], [2], [3], [4, 5, 6, 7])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(tbl[i], shift=RIGHT * 0.15) for i in idx], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeIn(ta))
        self.wait(0.3)
        self.clear_scene()


SHORT_SPOKEN = {"gptoss": "gpt-oss", "qwen3next": "Qwen3-Next", "qwen35": "Qwen3.5", "minimax": "MiniMax-M2",
                "kimik3": "Kimi K3", "dsv4": "DeepSeek-V4-Pro", "llama4": "Llama 4 Maverick", "kimik2": "Kimi K2",
                "mistral4": "Mistral Large 4", "glm5": "GLM-5"}
