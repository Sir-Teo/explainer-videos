from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import ATT, GATED, HIST, HYB, PART, RET, SSM_C, STATE, load, node_box


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.production()
        self.debate()
        self.context()
        self.open()

    def card(self):
        card = chapter_card(15, r"The frontier, late 2026", r"What do the newest models remember, and how?", part=PART)
        with self.voiceover("Chapter fifteen. The frontier, late 2026."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def production(self):
        head = label(r"Fixed-size memories in production, \ 2025--26", font_size=34).to_edge(UP, buff=0.3)
        items = [
            ("January 2025", r"MiniMax-01", r"lightning attention \\ in 7 layers of 8; \\ $456$B weights; \\ $4$M tokens", SSM_C),
            ("April 2025", r"Nemotron-H", r"NVIDIA: \\ Mamba-2, \\ $8\%$ attention; \\ up to $3\times$ faster", SSM_C),
            ("September 2025", r"Qwen3-Next", r"Gated DeltaNet \\ in 3 layers of 4; \\ $80$B, \\ $3$B active", GATED),
            ("October 2025", r"Kimi Linear", r"Kimi Delta Attention, \\ 3 of 4; \\ up to $6\times$ faster \\ decoding at $1$M", GATED),
            ("October 2025", r"MiniMax-M2", r"back to \\ full attention", ATT),
            ("December 2025", r"Nemotron 3", r"NVIDIA: \\ Mamba-2 hybrid \\ with experts; \\ $1$M tokens", SSM_C),
            ("February 2026", r"Qwen3.5", r"Gated DeltaNet, \\ 3 of 4; \\ $0.8$B to $397$B", GATED),
            ("March 2026", r"Mamba-3", r"complex states, \\ MIMO", SSM_C),
            ("April 2026", r"DeepSeek-V4", r"compressed sparse \\ attention; \\ $1$M tokens", ATT),
            ("July 2026", r"Kimi K3", r"Kimi Delta Attention \\ in 69 of 93 layers; \\ $2.8$T weights", GATED),
        ]
        cards = VGroup()
        for when, name, what, col in items:
            d = label(when, font_size=17, color=GREY_B)
            t = label(name, font_size=24, color=col)
            w = label(what, font_size=18, color=GREY_A)
            body = VGroup(d, t, w).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            box = RoundedRectangle(width=2.55, height=2.75, corner_radius=0.12, stroke_color=col, stroke_width=1.8,
                                   fill_color="#0B0F17", fill_opacity=0.95)
            if body.width > 2.3:
                body.width = 2.3
            body.move_to(box).align_to(box, UP).shift(DOWN * 0.18)
            cards.add(VGroup(box, body))
        cards.arrange_in_grid(rows=2, cols=5, buff=(0.12, 0.25)).next_to(head, DOWN, buff=0.35)
        foot = note(r"each from its maker's report or model card", font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Two years ago, a fixed-size memory in a frontier model was an experiment. <bookmark mark='a'/> In "
            "January 2025 MiniMax-01 shipped lightning attention in seven layers of every eight, and read up to four "
            "million tokens; in April, NVIDIA's Nemotron-H kept attention in a few layers of a Mamba-2 stack. "
            "<bookmark mark='b'/> That autumn came the gated delta rule: Qwen3-Next and Kimi Linear, three layers in "
            "four. <bookmark mark='c'/> Then MiniMax's next model went back to full attention, and we'll see why. "
            "<bookmark mark='d'/> NVIDIA's Nemotron 3 mixed Mamba-2 with experts and a million tokens; Qwen3.5 made "
            "the gated-delta hybrid the whole family's design, and Mamba-3 improved the state-space line. "
            "<bookmark mark='e'/> DeepSeek-V4 took another road, compressing the cache instead; and in July 2026 "
            "Kimi K3, two point eight trillion weights, put Kimi Delta Attention in sixty-nine of its ninety-three "
            "layers."
        ) as vo:
            veils = VGroup(*[Rectangle(width=c_[0].width + 0.04, height=c_[0].height + 0.04, stroke_width=0,
                                       fill_color=BACKGROUND, fill_opacity=0.82).move_to(c_[0]) for c_ in cards])
            self.play(FadeIn(head), FadeIn(foot), FadeIn(cards), FadeIn(veils))
            groups = [[0, 1], [2, 3], [4], [5, 6, 7], [8, 9]]
            for g_, m in zip(groups, "abcde"):
                vo.wait_until(m)
                self.play(*[FadeOut(veils[i]) for i in g_], run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def debate(self):
        head = label(r"Why MiniMax-M2 went back to full attention", font_size=32).to_edge(UP, buff=0.35)
        lines_ = [
            (r"its lightning-attention hybrid matched full attention on the usual benchmarks,",
             r"but showed ``clear deficits in complex, multi-hop reasoning'' at larger scale"),
            (r"``the real bottleneck is the limitations of evaluation'':",
             r"the tests that would show the gap are expensive, \ and may not hold at scale"),
            (r"the infrastructure is young: \ many linear layers are memory-bound,",
             r"and serving needs low-precision states, \ prefix caching, \ speculative decoding"),
            (r"a sliding-window hybrid lost quality as the context grew:",
             r"retrieval and induction heads form early in pretraining, \ and are hard to add later"),
        ]
        pts = VGroup(*[VGroup(label(a, font_size=24, color=WHITE), label(b, font_size=24, color=GREY_A))
                       .arrange(DOWN, aligned_edge=LEFT, buff=0.1) for a, b in lines_])
        pts.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.5).shift(RIGHT * 0.3)
        if pts.width > 12.6:
            pts.width = 12.6
        bullets = VGroup(*[Dot(radius=0.07, color=ATT).next_to(p_, LEFT, buff=0.25).align_to(p_, UP).shift(DOWN * 0.14)
                           for p_ in pts])
        src = cite(r"H.~Sun (MiniMax), \textit{Why did M2 end up as a full attention model?} \ (October 2025)", corner=DL,
                   font_size=17)
        tw = label(r"the recall test of chapter 11, \ at the scale of a frontier model", font_size=24, color=C.BITS)
        tw.to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "In October 2025 Haohai Sun, who led MiniMax-M2's pretraining, explained the reversal. "
            "<bookmark mark='a'/> Their hybrid matched full attention on the usual benchmarks, but at larger scale "
            "it showed clear deficits in complex, multi-hop reasoning. <bookmark mark='b'/> The deeper problem, he "
            "wrote, is evaluation: the tests that reveal such gaps are expensive, and small experiments may not "
            "predict large ones. <bookmark mark='c'/> And the tools are young: linear layers are often limited by "
            "memory bandwidth, and serving tricks built for caches, like prefix caching and speculative decoding, "
            "have to be rebuilt. <bookmark mark='d'/> A sliding-window hybrid fared worse as the context grew; "
            "the heads that retrieve and copy, they found, form early in pretraining and are hard to add later. "
            "<bookmark mark='e'/> It's our recall test, at a frontier lab's scale. Moonshot and Qwen bet the other "
            "way; both bets are in production."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(pts[k], shift=RIGHT * 0.1), FadeIn(bullets[k]))
            vo.wait_until("e")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def context(self):
        head = label(r"Context engineering", font_size=36).to_edge(UP, buff=0.35)
        win = RoundedRectangle(width=7.2, height=4.2, corner_radius=0.15, stroke_color=GREY_B, stroke_width=2).move_to([-2.6, -0.5, 0])
        wl = label(r"the context window", font_size=20, color=GREY_B).next_to(win, UP, buff=0.1)
        parts = [(r"instructions and tools", 0.5, GREY_B), (r"retrieved documents", 0.9, RET),
                 (r"the conversation so far, \ compacted into a summary", 0.7, STATE), (r"recent turns, \ in full", 1.2, HYB),
                 (r"the current task", 0.5, C.BITS)]
        blocks = VGroup()
        y = win.get_top()[1] - 0.15
        for t, h, c_ in parts:
            r_ = Rectangle(width=6.8, height=h, stroke_width=0, fill_color=c_, fill_opacity=0.22)
            r_.move_to([win.get_x(), y - h / 2, 0])
            blocks.add(VGroup(r_, label(t, font_size=18, color=c_).move_to(r_)))
            y -= h + 0.06
        notes_ = node_box(r"notes and memory files", HIST, font_size=20).move_to([4.2, 0.9, 0])
        subs = node_box(r"sub-agents, \ each with a clean window", SSM_C, font_size=20).move_to([4.2, -0.6, 0])
        arr = VGroup(Arrow(notes_.get_left(), win.get_right() + UP * 1.4, buff=0.1, color=HIST, stroke_width=2.5),
                     Arrow(subs.get_left(), win.get_right() + DOWN * 0.1, buff=0.1, color=SSM_C, stroke_width=2.5))
        src = cite(r"Anthropic, \textit{Effective context engineering for AI agents} (September 2025)", corner=DL, font_size=17)
        tw = label(r"the window is a budget: \\ what goes in it matters \\ more than how big it is", font_size=24,
                   color=WHITE).next_to(subs, DOWN, buff=0.7)
        with self.voiceover(
            "Meanwhile the people who build agents learned the lesson of the last two chapters the practical way. "
            "A model's window is a budget, and every token spent dilutes its attention; Anthropic's guide of "
            "September 2025 calls the decline context rot. <bookmark mark='a'/> So context engineering decides what "
            "goes in: instructions and tools, the documents retrieval finds, <bookmark mark='b'/> the conversation "
            "so far compacted into a summary when the window fills, and only the recent turns in full. "
            "<bookmark mark='c'/> What doesn't fit goes to notes the agent writes and reads back later, "
            "<bookmark mark='d'/> or to sub-agents that work in clean windows and report back a summary. It is "
            "this part's memory, managed by hand: a cache that is evicted, compressed, and retrieved."
        ) as vo:
            for b_ in blocks:
                b_.set_opacity(0.15)
            self.play(FadeIn(head), Create(win), FadeIn(wl), FadeIn(src), FadeIn(blocks))
            vo.wait_until("a")
            self.play(*[b_[0].animate.set_fill(opacity=0.22) for b_ in blocks[:2]], *[b_[1].animate.set_opacity(1) for b_ in blocks[:2]])
            vo.wait_until("b")
            self.play(*[b_[0].animate.set_fill(opacity=0.22) for b_ in blocks[2:]], *[b_[1].animate.set_opacity(1) for b_ in blocks[2:]])
            vo.wait_until("c")
            self.play(FadeIn(notes_), GrowArrow(arr[0]))
            vo.wait_until("d")
            self.play(FadeIn(subs), GrowArrow(arr[1]), FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        head = label(r"Open questions", font_size=36).to_edge(UP, buff=0.4)
        qs = VGroup(
            label(r"how much attention does a model need? \ one layer in four, \ in eight, \ or none at all?", font_size=30),
            label(r"how big must a fixed memory be, \ and how should it grow with the model?", font_size=30),
            label(r"can a memory learn what to keep \ as well as attention learns where to look?", font_size=30),
            label(r"how do we measure what a model can do with a million tokens?", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.7).next_to(head, DOWN, buff=0.6)
        nums = VGroup(*[label(rf"{i + 1}.", font_size=24, color=C.BITS).next_to(q_, LEFT, buff=0.25) for i, q_ in enumerate(qs)])
        with self.voiceover(
            "So the questions are open. <bookmark mark='a'/> How much attention does a model need: one layer in "
            "four, in eight, or none? <bookmark mark='b'/> How big must a fixed memory be, and how should it grow? "
            "<bookmark mark='c'/> Can a memory learn what to keep as well as attention learns where to look? "
            "<bookmark mark='d'/> And how do we even measure what a model does with a million tokens?"
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(qs[k], shift=RIGHT * 0.1), FadeIn(nums[k]))
        self.wait(0.3)
        self.clear_scene()
