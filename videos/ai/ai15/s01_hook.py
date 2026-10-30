from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import HIST, K, MONO, PART, STATE, V, gib, grid_matrix, load, vec_column


class Hook(VoiceoverScene):
    def construct(self):
        self.grow()
        self.fixed()
        self.history()
        self.plan()

    # ------------------------------------------------------------------
    def grow(self):
        k = load("kvcache")
        per = float(k["per_token"]["llama"])
        n = ValueTracker(0)
        g = np.random.default_rng(12)
        cols = VGroup(*[VGroup(vec_column(g.normal(size=8), cell=0.16, color=K), vec_column(g.normal(size=8), cell=0.16, color=V))
                        .arrange(RIGHT, buff=0.03) for _ in range(24)]).arrange(RIGHT, buff=0.1).move_to(UP * 0.8)
        counter = VGroup(label(r"tokens read:", font_size=30, color=GREY_A), Integer(0, font_size=36, color=WHITE),
                         label(r"memory:", font_size=30, color=GREY_A), MathTex(r"0", font_size=36, color=C.SURPRISE))
        counter.arrange(RIGHT, buff=0.25).move_to(DOWN * 1.6)

        def upd_int(m):
            m.set_value(int(n.get_value()))
            counter[2].next_to(m, RIGHT, buff=0.4)  # the number grows wider: keep the next label clear of it

        def upd_mem(m):
            m.become(MathTex(gib(max(n.get_value(), 1) * per), font_size=36, color=C.SURPRISE).next_to(counter[2], RIGHT, buff=0.25))

        tag = note(r"Llama 3.1 70B's cache: \ $80$ layers, \ $8$ key and value heads of $128$ numbers, \ bf16: \ $16$ bits $= 2$ bytes a number").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Every token a transformer reads, it keeps: a key and a value, in every layer. <bookmark mark='a'/> For "
            "Llama 3.1 with seventy billion parameters, each number stored in bf16, sixteen bits or two bytes, "
            f"that's {per / 2**10:.0f} kilobytes a token. "
            "<bookmark mark='b'/> A long conversation, a hundred and twenty-eight thousand tokens, needs "
            f"{128e3 * per / 2**30:.0f} gigabytes of memory, just to remember what it has read."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_, shift=LEFT * 0.2) for c_ in cols], lag_ratio=0.08), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(counter), FadeIn(tag))
            counter[1].add_updater(upd_int)  # only once it is on screen: fading in a mobject that rebuilds itself fails
            counter[3].add_updater(upd_mem)
            vo.wait_until("b")
            self.play(n.animate.set_value(128_000), run_time=3.0, rate_func=rate_functions.ease_in_quad)
        counter[1].clear_updaters()
        counter[3].clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fixed(self):
        words = "Spade looked at the girl and said nothing".split()
        toks = VGroup(*[data_text(w, font=MONO, font_size=26, color=GREY_A) for w in words]).arrange(RIGHT, buff=0.3)
        toks.to_edge(UP, buff=0.6)
        g = np.random.default_rng(3)
        S = np.zeros((8, 8))
        grid = grid_matrix(np.full((8, 8), 1e-3), 3.0).move_to(DOWN * 0.4)
        gl = label(r"a memory of fixed size", font_size=26, color=STATE).next_to(grid, DOWN, buff=0.3)
        q = label(r"what must it keep, \ and what can it forget?", font_size=30, color=WHITE).to_edge(DOWN, buff=0.4)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        with self.voiceover(
            "The alternative is to read like we do: keep a memory of a fixed size, and update it as each word "
            "arrives. <bookmark mark='a'/> Then the question is what to keep, and what to forget."
        ) as vo:
            self.play(FadeIn(toks), FadeIn(grid), FadeIn(gl), FadeIn(tag))
            for i in range(len(words)):
                S = 0.9 * S + np.outer(g.normal(size=8), g.normal(size=8))
                new = grid_matrix(S, 3.0).move_to(grid)
                self.play(toks[i].animate.set_color(C.BITS), Transform(grid, new), run_time=0.3)
            vo.wait_until("a")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"How we got here", font_size=40).to_edge(UP, buff=0.3)
        w, fs = 4.3, 22
        cards = [
            history_card(1982, r"Hopfield networks", r"a memory you return to by its content \ (Part 20)", color=HIST,
                         width=w, font_size=fs),
            history_card(1992, r"fast weights", r"one network writes the weights of another \ (Schmidhuber)", color=HIST,
                         width=w, font_size=fs),
            history_card(1997, r"LSTM", r"a gated memory cell, \ read and written by gates \ (Part 10)", color=HIST,
                         width=w, font_size=fs),
            history_card(2014, r"Neural Turing machines, \ memory networks", r"a memory read and written by attention",
                         color=HIST, width=w, font_size=fs),
            history_card(2017, r"the transformer", r"keep every key and value \ (Part 13)", color=HIST, width=w,
                         font_size=fs),
            history_card(r"2019--20", r"Transformer-XL, \ Longformer, \ BigBird", r"reach further back; \ look at less of it",
                         color=HIST, width=w, font_size=fs),
            history_card(2020, r"linear attention, \ kNN-LM, \ RAG", r"a transformer as a recurrent network; \ a memory "
                         r"outside the model", color=HIST, width=w, font_size=fs),
            history_card(r"2021--23", r"S4, \ RETRO, \ Mamba", r"state-space models; \ retrieval at scale; \ a memory that "
                         r"chooses", color=HIST, width=w, font_size=fs),
            history_card(2026, r"hybrids in production", r"Qwen3.5, \ Kimi K3: \ three layers in four linear; \ "
                         r"million-token windows", color=HIST, width=w, font_size=fs),
        ]
        grid = VGroup(*cards).arrange_in_grid(rows=3, cols=3, buff=(0.22, 0.25), cell_alignment=UP)
        if grid.width > 13.4:
            grid.width = 13.4
        if grid.height > 6.5:
            grid.height = 6.5
        grid.next_to(head, DOWN, buff=0.25)
        with self.voiceover(
            "How we got here. In 1982 John Hopfield built a network that stores memories in its connections and "
            "returns to one when given a piece of it. <bookmark mark='a'/> In 1992 Jürgen Schmidhuber had one network "
            "write, token by token, the weights of another: fast weights, the idea at the heart of this part. "
            "<bookmark mark='b'/> In 1997 the LSTM gave a recurrent network a memory cell with gates, Part 10's story. "
            "<bookmark mark='c'/> In 2014 neural Turing machines and memory networks read and wrote a memory with "
            "attention. <bookmark mark='d'/> In 2017 the transformer simply kept everything. <bookmark mark='e'/> "
            "From 2019, Transformer-XL reached further back, and Longformer and BigBird looked at less of it. "
            "<bookmark mark='f'/> In 2020 linear attention turned a transformer back into a recurrent network, and "
            "retrieval put a memory outside the model. <bookmark mark='g'/> Then came state-space models, retrieval "
            "from trillions of tokens, and Mamba, a memory that chooses what to keep. <bookmark mark='h'/> And by "
            "2026, the frontier's open models make three of every four layers a fixed-size memory, and read a "
            "million tokens."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.1))
            for k, m in enumerate("abcdefgh"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k + 1], shift=UP * 0.1), run_time=0.8)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Memory", font_size=48).to_edge(UP, buff=0.35)
        obj = objectives_card([
            r"attention's memory: \ the cache, \ how it is shrunk, \ what can be thrown away",
            r"a matrix as a memory: \ from Hopfield and fast weights to linear attention",
            r"how to write to it: \ adding, \ decaying, \ the delta rule, \ and how to train it in parallel",
            r"state-space models: \ HiPPO, \ S4, \ Mamba; \ and memories that learn while they read",
            r"recall, measured: \ which memory can look things up, \ and hybrids that mix them",
            r"long contexts, \ how well they really work, \ and retrieval: \ a memory outside the model",
        ], title=r"In this part", font_size=28, width=12.6)
        obj.rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        obj.head.next_to(obj.rows, UP, buff=0.5).set_x(0)
        obj.next_to(title, DOWN, buff=0.3)
        if obj.height > 6.2:
            obj.height = 6.2
            obj.next_to(title, DOWN, buff=0.3)
        with self.voiceover(
            "This is Part 15 of AI, Built: memory. <bookmark mark='a'/> First, attention's own memory: the cache, how "
            "models shrink it, and what can be thrown away. <bookmark mark='b'/> Then a matrix as a memory, from "
            "Hopfield and fast weights to linear attention. <bookmark mark='c'/> How to write to it, and how to train "
            "such a memory on a whole text at once. <bookmark mark='d'/> State-space models, and memories that learn "
            "while they read. <bookmark mark='e'/> Then we measure which memories can look things up, and mix them. "
            "<bookmark mark='f'/> And last, long contexts, how well they really work, and memory outside the model. "
            "<bookmark mark='g'/> Every model in this part is trained here, and we'll watch each one learn."
        ) as vo:
            self.play(FadeIn(title), FadeIn(obj.head))
            for k, m in enumerate("abcdef"):
                vo.wait_until(m)
                self.play(FadeIn(obj.rows[k], shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("g")
            self.play(Indicate(title, color=STATE, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()
