from __future__ import annotations

from explainer import *  # noqa: F403
from videos.open_models.common import KEYS, MCOLOR, NAMES, block, cfg, label, layer_strip, note


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.credits()

    # ------------------------------------------------------------------
    def recap(self):
        skel = VGroup(block("tokens $\\to$ vectors", C.EMBED, width=3.2, height=0.55, font_size=24),
                      block("attention", C.ATTN, width=3.2, height=0.55, font_size=24),
                      block("feed-forward $\\to$ experts", C.EXPERT, width=3.2, height=0.55, font_size=24),
                      block("next-token prediction", C.PROB, width=3.2, height=0.55, font_size=24))
        skel.arrange(UP, buff=0.15).to_edge(LEFT, buff=0.5).shift(DOWN * 0.3)
        sk_l = label(r"the same skeleton as GPT-2", font_size=26, color=GREY_A).next_to(skel, UP, buff=0.25)
        m, g, k = cfg("mimo"), cfg("glm"), cfg("kimi")
        strips = VGroup(
            layer_strip(m["layer_types"], {"swa": C.LOCAL, "global": C.GLOBAL}, cell=0.07, gap=0.016, height=0.4),
            layer_strip(["i" if t == "full" else "s" for t in g["indexer_types"]], {"i": C.INDEXER, "s": C.INDEXER},
                        cell=0.07, gap=0.016, height=0.4, outline_types=("s",)),
            layer_strip(k["layer_types"], {"kda": C.MEMORY, "mla": C.GLOBAL}, cell=0.07, gap=0.016, height=0.4),
        )
        lines = [
            r"looks nearby; a few global layers; learned sinks",
            r"compressed memory; reads only what the indexer picks",
            r"a running memory; global attention every 4th layer; attention across depth",
        ]
        rows = VGroup()
        for key, s, t in zip(KEYS, strips, lines):
            rows.add(VGroup(label(NAMES[key], font_size=28, color=MCOLOR[key]), s, label(t, font_size=22, color=GREY_A))
                     .arrange(DOWN, aligned_edge=LEFT, buff=0.1))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.1)
        width_l = label(r"width: all three turned the feed-forward network into a library of experts", font_size=26,
                        color=C.EXPERT).to_edge(UP, buff=0.4)
        with self.voiceover(
            "So that's the open frontier, as of October 2026. <bookmark mark='s'/> Underneath, the same skeleton GPT-2 "
            "had: tokens become vectors, attention and feed-forward layers refine them, and the last vector predicts the "
            "next token. <bookmark mark='w'/> On top of it, two kinds of bets. On width, all three turned the feed-forward "
            "network into a vast library of experts, with only a few percent of the model at work for any one token. "
            "<bookmark mark='l'/> On length, three different answers. <bookmark mark='m'/> MiMo looks nearby, and keeps a "
            "few global layers. <bookmark mark='g'/> GLM compresses its memory, and reads only what its indexer picks. "
            "<bookmark mark='k'/> Kimi keeps a running memory, attends globally only every fourth layer, and even uses "
            "attention across its own depth."
        ) as vo:
            vo.wait_until("s")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in skel], lag_ratio=0.2), FadeIn(sk_l))
            vo.wait_until("w")
            self.play(FadeIn(width_l), Indicate(skel[2], color=C.EXPERT))
            for i, mk in enumerate("mgk"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[i][0]), FadeIn(rows[i][1], lag_ratio=0.01), FadeIn(rows[i][2]), run_time=1.0)
        with self.voiceover(
            "<bookmark mark='n'/> What we haven't covered is where most of each technical report's pages actually go: "
            "training, and especially reinforcement learning on long, agentic tasks, which shapes what these models do with "
            "all this machinery. <bookmark mark='o'/> But because the weights are open, every number about these models "
            "that you've seen in this video can be checked by anyone, straight from the files. Thanks for watching."
        ) as vo:
            vo.wait_until("n")
            nc = label(r"not covered: data, training, and reinforcement learning on long agentic tasks", font_size=28,
                       color=GREY_A).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(nc))
            vo.wait_until("o")
            self.play(Indicate(rows, color=WHITE, scale_factor=1.02))
        self.clear_scene()

    # ------------------------------------------------------------------
    def credits(self):
        lines = VGroup(
            label(r"Inside the Open Frontier", font_size=48),
            label(r"Models: Xiaomi MiMo-V2.6-Pro (MIT license), Z.ai GLM-5.3, Moonshot AI Kimi K3", font_size=26),
            label(r"Ranking: Artificial Analysis Intelligence Index v4.3.2, October 8, 2026", font_size=26),
            label(r"Configs and weights: Hugging Face (read with range requests); technical reports cited on screen",
                  font_size=26),
            label(r"Animation: Manim Community \quad Voice: Kokoro-82M \quad Style: after 3Blue1Brown", font_size=26,
                  color=GREY_A),
            note(r"Not affiliated with Xiaomi, Z.ai, Moonshot AI or Artificial Analysis.", font_size=24),
        ).arrange(DOWN, buff=0.3)
        self.play(FadeIn(lines, lag_ratio=0.1), run_time=1.5)
        self.wait(4)
        self.play(FadeOut(lines))
