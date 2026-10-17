from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai12.common import K, MONO, STATE, V, gib, grid_matrix, load, vec_column


class Hook(VoiceoverScene):
    def construct(self):
        self.grow()
        self.fixed()
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

        def upd_mem(m):
            m.become(MathTex(gib(max(n.get_value(), 1) * per), font_size=36, color=C.SURPRISE).next_to(counter[2], RIGHT, buff=0.25))

        tag = note(r"Llama 3.1 70B's cache: \ $80$ layers, \ $8$ key and value heads of $128$ numbers, \ bf16").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Every token a transformer reads, it keeps: a key and a value, in every layer. <bookmark mark='a'/> For "
            f"Llama 3.1 with seventy billion parameters, that's {per / 2**10:.0f} kilobytes a token. "
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
        toks = VGroup(*[Text(w, font=MONO, font_size=26, color=GREY_A) for w in words]).arrange(RIGHT, buff=0.3)
        toks.to_edge(UP, buff=0.6)
        g = np.random.default_rng(3)
        S = np.zeros((8, 8))
        grid = grid_matrix(np.full((8, 8), 1e-3), 3.0).move_to(DOWN * 0.4)
        gl = label(r"a memory of fixed size", font_size=26, color=STATE).next_to(grid, DOWN, buff=0.3)
        q = label(r"what must it keep, \ and what can it forget?", font_size=30, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The alternative is to read like we do: keep a memory of a fixed size, and update it as each word "
            "arrives. <bookmark mark='a'/> Then the question is what to keep, and what to forget."
        ) as vo:
            self.play(FadeIn(toks), FadeIn(grid), FadeIn(gl))
            for i in range(len(words)):
                S = 0.9 * S + np.outer(g.normal(size=8), g.normal(size=8))
                new = grid_matrix(S, 3.0).move_to(grid)
                self.play(toks[i].animate.set_color(C.BITS), Transform(grid, new), run_time=0.3)
            vo.wait_until("a")
            self.play(FadeIn(q))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 12: \ Memory", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"KV caches, \ latent attention, \ linear attention, \ the delta rule, \ state-space models, "
                    r"\ hybrids", font_size=28, color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=12, done=11).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "This part is about memory: how attention's cache is shrunk, how a fixed memory can stand in for it, "
            "<bookmark mark='a'/> and why the newest models use both."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
