from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.open_models.common import (
    KEYS, MCOLOR, NAMES, Plot, cfg, label, model, note, show_chapter_card, source,
)
from videos.open_models.toys import cache_gb, kv_cache

FP4_VALUES = [0, 0.5, 1, 1.5, 2, 3, 4, 6]


class SideBySide(VoiceoverScene):
    def construct(self):
        show_chapter_card(self, 14, "Side by side")
        self.cache_chart()
        self.speculative()
        self.four_bits()
        self.table()

    # ------------------------------------------------------------------
    def cache_chart(self):
        kv = kv_cache()
        at = {k: cache_gb(kv[k], 1e6) for k in KEYS}
        assert [round(at[k]) for k in KEYS] == [51, 93, 28]
        pl = Plot((0, 1e6), (0, 100), width=8.6, height=4.6, x_ticks=[0, 250_000, 500_000, 750_000, 1_000_000],
                  x_fmt=lambda v: ["0", "250K", "500K", "750K", "1M"][int(v // 250_000)], y_ticks=[0, 25, 50, 75, 100],
                  font_size=24).move_to(LEFT * 1.3 + DOWN * 0.35)
        xl = label(r"tokens of context", font_size=24, color=GREY_A).next_to(pl, DOWN, buff=0.5)
        yl = label(r"cache memory (GB)", font_size=26, color=GREY_A).rotate(PI / 2).next_to(pl.y_labels, LEFT, buff=0.2)
        xs = np.linspace(0, 1e6, 60)
        lines, ends = VGroup(), VGroup()
        for k in KEYS:
            ys = [cache_gb(kv[k], x) for x in xs]
            lines.add(pl.line(xs, ys, MCOLOR[k], 5))
            t = label(rf"{NAMES[k]}: {at[k]:.0f} GB", font_size=26, color=MCOLOR[k])
            t.next_to(pl.c2p(1e6, at[k]), RIGHT, buff=0.2)
            ends.add(t)
        mha = kv["glm"]["mha_per_token"]
        x_exit = 100e9 / mha
        off1 = DashedLine(pl.c2p(0, 0), pl.c2p(x_exit, 100), color=GREY_B, stroke_width=2.5)
        off1_l = label(r"textbook attention at GLM's size: 5.1 TB at 1M", font_size=22, color=GREY_B)
        off1_l.next_to(pl.c2p(x_exit, 100), UP, buff=0.12, aligned_edge=LEFT)
        x_exit2 = 100e9 / kv["mimo"]["all_global_per_token"]
        off2 = DashedLine(pl.c2p(0, 0), pl.c2p(x_exit2, 100), color=GREY_B, stroke_width=2).set_stroke(opacity=0.6)
        off2_l = label(r"MiMo with every layer global: 358 GB", font_size=22, color=GREY_B)
        off2_l.next_to(pl.c2p(x_exit2, 100), RIGHT, buff=0.15).shift(DOWN * 0.2)
        src = note(r"computed from each config: 16-bit cache entries; KDA memories in 32 bits").to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Let's put the three side by side. <bookmark mark='c'/> Here's how much cache memory each one needs as the "
            "context grows to a million tokens, computed from their configurations. <bookmark mark='m'/> MiMo: about 51 "
            "gigabytes at a million, almost all of it from its 10 global layers. <bookmark mark='g'/> GLM: about 93. Its "
            "sparse attention saves compute, not memory: every token's latent has to be kept, in case the indexer picks "
            "it. <bookmark mark='k'/> Kimi: about 28, plus its fixed 0.4 gigabytes of KDA memories. "
            "<bookmark mark='x'/> For comparison, textbook attention at GLM's size would leave this chart almost "
            "immediately, on its way to 5 terabytes."
        ) as vo:
            vo.wait_until("c")
            self.play(Create(pl), FadeIn(xl), FadeIn(yl), FadeIn(src))
            for i, mk in enumerate("mgk"):
                vo.wait_until(mk)
                self.play(Create(lines[i]), run_time=1.5)
                self.play(FadeIn(ends[i]))
            vo.wait_until("x")
            self.play(Create(off2), FadeIn(off2_l))
            self.play(Create(off1), FadeIn(off1_l))
        self.clear_scene()

    # ------------------------------------------------------------------
    def speculative(self):
        words = ["The", "cache", "grows", "with", "every", "token", "you", "add"]
        boxes = VGroup()
        for i, w in enumerate(words):
            t = Text(w, font="DejaVu Sans Mono", font_size=24)
            b = RoundedRectangle(width=t.width + 0.3, height=0.55, corner_radius=0.08, stroke_width=2,
                                 stroke_color=C.TOKEN if i < 3 else C.PROB, fill_color=C.TOKEN, fill_opacity=0.1)
            if i >= 3:
                b = DashedVMobject(b, num_dashes=24)
            boxes.add(VGroup(b, t.move_to(b)))
        boxes.arrange(RIGHT, buff=0.15).move_to(UP * 1.6)
        d_l = label(r"draft: a small extra module guesses the next few tokens", font_size=26, color=C.PROB)
        d_l.next_to(boxes, UP, buff=0.3)
        marks = VGroup()
        ok = [True, True, True, False, False]
        for b, good in zip(boxes[3:], ok):
            m = MathTex(r"\checkmark" if good else r"\times", font_size=36, color=GREEN if good else RED)
            marks.add(m.next_to(b, DOWN, buff=0.15))
        v_l = label(r"verify: the full model checks all the guesses in one pass, keeps the ones it agrees with",
                    font_size=26).next_to(marks, DOWN, buff=0.3)
        facts = VGroup(
            label(r"\textbf{MiMo}: a 5-layer drafter that proposes 7 tokens per pass", font_size=26, color=C.MIMO),
            label(r"\textbf{GLM}: a drafter that reuses the indexer's choices and the main model's cache;", font_size=26,
                  color=C.GLM),
            label(r"\quad average accepted run $+20\%$, to 5.5 tokens (Z.ai's tests)", font_size=24, color=C.GLM),
            label(r"\textbf{Kimi K3}: a one-layer drafter (per its report)", font_size=26, color=C.KIMI),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "They also share a trick for speed: guessing several tokens at once. <bookmark mark='d'/> Each one has a "
            "small extra module that drafts the next few tokens cheaply. <bookmark mark='v'/> Then the full model checks "
            "all the guesses in a single pass, and keeps every guess it agrees with, up to the first mistake. "
            "<bookmark mark='m'/> MiMo's drafter is five layers deep, and proposes seven tokens at a time. "
            "<bookmark mark='g'/> GLM's reuses the indexer's choices and the main model's cache, which in Z.ai's tests "
            "raised the average number of accepted tokens by 20 percent. <bookmark mark='k'/> Kimi K3's report "
            "describes a single-layer drafter."
        ) as vo:
            self.play(FadeIn(boxes[:3]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.1) for b in boxes[3:]], lag_ratio=0.15), FadeIn(d_l))
            vo.wait_until("v")
            self.play(LaggedStart(*[FadeIn(m, scale=1.4) for m in marks], lag_ratio=0.2), FadeIn(v_l))
            self.play(*[boxes[i][0].animate.set_stroke(C.TOKEN) for i in (3, 4, 5)], boxes[6:].animate.set_opacity(0.25))
            vo.wait_until("m")
            self.play(FadeIn(facts[0]))
            vo.wait_until("g")
            self.play(FadeIn(facts[1]), FadeIn(facts[2]))
            vo.wait_until("k")
            self.play(FadeIn(facts[3]))
        self.clear_scene()

    # ------------------------------------------------------------------
    def four_bits(self):
        blk = model("kimi")["fp4_block"]
        el = np.array(blk["elements"])
        assert len(el) == 32 and blk["scale_exp"] == -6
        assert set(np.abs(el)).issubset(set(FP4_VALUES))
        grid = sorted(set(FP4_VALUES) | {-v for v in FP4_VALUES})
        assert len(grid) == 15
        nl = NumberLine(x_range=[-6.5, 6.5, 1], length=12.6, include_ticks=False, stroke_color=GREY_B).move_to(DOWN * 0.6)
        ticks = VGroup(*[Line(nl.n2p(v) + DOWN * 0.12, nl.n2p(v) + UP * 0.12, color=WHITE, stroke_width=2) for v in grid])
        tl = VGroup(*[MathTex(f"{v:g}", font_size=18, color=GREY_A).next_to(nl.n2p(v), DOWN, buff=0.2) for v in grid])
        counts: dict[float, int] = {}
        dots = VGroup()
        for v in el:
            v = float(abs(v) if v == 0 else v)
            c = counts.get(v, 0)
            counts[v] = c + 1
            dots.add(Dot(nl.n2p(v) + UP * (0.3 + 0.24 * c), radius=0.09, color=C.EXPERT))
        title = label(r"32 real weights from one of Kimi K3's experts, as stored", font_size=32).to_edge(UP, buff=0.5)
        sub = note(r"layer 13, expert 1, first row: one 32-number block, decoded from the weight file", font_size=22)
        sub.next_to(title, DOWN, buff=0.12)
        g_l = label(r"a 4-bit number can only be one of these 15 values", font_size=28).next_to(tl, DOWN, buff=0.3)
        scale = MathTex(r"\times\; 2^{-6}", r"\text{ shared by the whole block of 32}", font_size=34)
        scale[0].set_color(YELLOW)
        scale.next_to(g_l, DOWN, buff=0.3)
        st = {k: sum(model(k)["params"]["storage_bytes"].values()) / 1e12 for k in KEYS}
        assert abs(st["kimi"] - 1.56) < 0.01 and abs(st["mimo"] - 0.57) < 0.01 and abs(st["glm"] - 0.76) < 0.01
        disk = VGroup(
            label(r"on disk:", font_size=26, color=GREY_A),
            label(r"Kimi K3: 2.78 trillion parameters in 1.56 TB (experts in 4 bits)", font_size=26, color=C.KIMI),
            label(r"MiMo: 1.02 trillion in 0.57 TB (experts in 4 bits)", font_size=26, color=C.MIMO),
            label(r"GLM: 0.75 trillion in 0.76 TB (8 bits)", font_size=26, color=C.GLM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DL, buff=0.35)
        with self.voiceover(
            "And they store their numbers in remarkably few bits. <bookmark mark='w'/> Here are 32 real weights from one "
            "of Kimi K3's experts, exactly as stored in the file. <bookmark mark='f'/> Each one takes just four bits, and "
            "a four-bit number can only be one of these fifteen values, from minus six to six. <bookmark mark='s'/> Every "
            "block of 32 weights shares one scale factor, a power of two: here, two to the minus six. "
            "<bookmark mark='d'/> That's how Kimi K3's 2.8 trillion parameters fit in about one and a half terabytes. "
            "Moonshot trained with this format in the loop, so the model learned to live with it. MiMo stores its experts "
            "in four bits too; GLM uses eight."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("w")
            self.play(Create(nl))
            vo.wait_until("f")
            self.play(FadeIn(ticks), FadeIn(tl), FadeIn(g_l))
            self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in dots], lag_ratio=0.05), run_time=2)
            vo.wait_until("s")
            self.play(Write(scale))
            vo.wait_until("d")
            self.play(FadeOut(g_l), FadeOut(scale), FadeIn(disk))
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        tot = {k: model(k)["params"]["total"] for k in KEYS}
        act = {k: model(k)["active"] for k in KEYS}
        kv = kv_cache()
        rows = [
            ("parameters", [rf"{tot[k] / 1e12:.2f}T total, {act[k] / 1e9:.0f}B active" for k in KEYS]),
            ("layers", [str(cfg(k)["layers"]) for k in KEYS]),
            ("attention", [r"60 window (128) + 10 global", r"latent (MLA) + sparse (top 2{,}048)",
                           r"69 KDA memory + 24 global MLA"]),
            ("tricks", [r"learned sinks; grouped queries", r"indexer shared by 4 layers", r"no positions; depth attention"]),
            ("experts", [r"384, 8 per token", r"256 + 1 shared, 8 per token", r"896 + 2 shared, 16 per token, latent"]),
            ("cache at 1M tokens", [rf"{cache_gb(kv[k], 1e6):.0f} GB" for k in KEYS]),
        ]
        xs = [-2.1, 1.3, 4.8]
        table = VGroup()
        head = VGroup(*[label(NAMES[k], font_size=28, color=MCOLOR[k]).move_to([x, 2.7, 0]) for k, x in zip(KEYS, xs)])
        table.add(head)
        for i, (name, vals) in enumerate(rows):
            y = 1.9 - 0.78 * i
            r = VGroup(label(name, font_size=24, color=GREY_A).move_to([-6.6, y, 0], aligned_edge=LEFT))
            for v, x in zip(vals, xs):
                t = label(v, font_size=22)
                if t.width > 3.2:
                    t.width = 3.2
                r.add(t.move_to([x, y, 0]))
            table.add(r)
        lines = VGroup(*[Line([-6.7, 2.35 - 0.78 * i, 0], [7.0, 2.35 - 0.78 * i, 0], color=GREY_D, stroke_width=1)
                         for i in range(len(rows) + 1)])
        with self.voiceover(
            "Here's everything at once. <bookmark mark='a'/> Three models of broadly similar ambition, all mixtures of "
            "experts, all reading a million tokens, <bookmark mark='b'/> with three different answers to the cost of "
            "attention."
        ) as vo:
            self.play(FadeIn(head), Create(lines))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in table[1:]], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("b")
            self.play(*[Indicate(t, color=YELLOW, scale_factor=1.05) for t in table[3][1:]])
        self.wait(1.0)
        self.clear_scene()
