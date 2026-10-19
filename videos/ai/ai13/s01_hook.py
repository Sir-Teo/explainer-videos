from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, attention_arcs, char_row, heat_image, load


class Hook(VoiceoverScene):
    def construct(self):
        self.reading()
        self.grid()
        self.plan()

    # ------------------------------------------------------------------
    def reading(self):
        t = load("tf")
        snip = str(t["snip"])
        maps = np.asarray(t["maps"])  # layer, head, query, key
        L, H, n, _ = maps.shape
        # the head that looks furthest back on average, in the last layer: the most interesting arcs
        dist = np.array([[(maps[l_, h] * np.abs(np.arange(n)[:, None] - np.arange(n)[None])).sum(1)[16:].mean()
                          for h in range(H)] for l_ in range(L)])
        li = L - 1
        hi = int(np.argmax(dist[li]))
        cut = snip.rfind(" ", 0, 33) + 1 or 32  # break the line at a space
        first, second = snip[:cut], snip[cut:]
        r1 = char_row(first, 12.6, font_size=30).move_to(UP * 0.9)
        r2 = char_row(second, 12.6, font_size=30).move_to(DOWN * 1.6)
        row = VGroup(*r1, *r2)
        tag = note(rf"our transformer, \ layer {li + 1}, head {hi + 1}, \ reading the scoreboard's passage "
                   r"\ (computed weights)").to_edge(DOWN, buff=0.3)
        picks = [i for i in (14, 22, 30, 41, 50, 58, 63) if i < n and snip[i] != " "]
        with self.voiceover(
            "This is a transformer reading. It's ours: we trained it on this series' thirty novels, and it's "
            "reading a sentence from the scoreboard's passage, which it has never seen. <bookmark mark='a'/> To "
            "guess each next character, every character looks back at the characters before it and decides how "
            "much each one matters. The thicker the arc, the more it looks. <bookmark mark='b'/> That look is "
            "called attention, and it is the engine of every large model today."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in row], lag_ratio=0.01), run_time=1.5)
            self.play(FadeIn(tag))
            vo.wait_until("a")
            prev = None
            for i in picks:
                rr = r1 if i < cut else r2
                if i >= cut:  # second line: arcs reach back over the line break, drawn on the second line only
                    w = maps[li, hi, i, cut:]
                    arcs = attention_arcs(r2, i - cut, w, color=A)
                else:
                    arcs = attention_arcs(r1, i, maps[li, hi, i], color=A)
                hl = SurroundingRectangle(rr[i if i < cut else i - cut], color=C.QUERY, buff=0.06)
                anims = [Create(arcs), Create(hl)]
                if prev is not None:
                    anims += [FadeOut(prev)]
                self.play(*anims, run_time=0.8)
                prev = VGroup(arcs, hl)
            vo.wait_until("b")
            self.play(FadeOut(prev))
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def grid(self):
        t = load("tf")
        maps = np.asarray(t["maps"])
        L, H = maps.shape[:2]
        S = 1.25
        imgs = Group(*[heat_image(maps[l_, h], S, S, color=A, mask_upper=True) for l_ in range(L) for h in range(H)])
        imgs.arrange_in_grid(rows=L, cols=H, buff=0.18).move_to(DOWN * 0.2)
        rl = VGroup(*[label(rf"layer {l_ + 1}", font_size=20, color=GREY_B).next_to(imgs[l_ * H], LEFT, buff=0.2) for l_ in range(L)])
        hl = VGroup(*[label(rf"head {h + 1}", font_size=20, color=GREY_B).next_to(imgs[h], UP, buff=0.12) for h in range(H)])
        cap = label(rf"all ${L * H}$ heads, \ on the same ${maps.shape[-1]}$ characters", font_size=26, color=GREY_A)
        cap.to_edge(UP, buff=0.25)
        with self.voiceover(
            f"Our model has {L * H} of these looks, called heads, each its own way of weighing the past. Some look "
            "one character back, some at the start of the word, some spread out. <bookmark mark='a'/> This part is "
            "about the mathematics of that look: what it computes, how it knows where things are, and what it can "
            "learn to do."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m, scale=0.9) for m in imgs], lag_ratio=0.04), FadeIn(rl), FadeIn(hl),
                      FadeIn(cap), run_time=2.5)
            vo.wait_until("a")
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(r"Part 13: \ Attention as Geometry", font_size=52).to_edge(UP, buff=0.6)
        sub = label(r"kernel smoothers, \ queries and keys, \ rotations, \ induction heads, \ learning in context",
                    font_size=28, color=C.BITS).next_to(title, DOWN, buff=0.25)
        smap = series_map(current=13, done=12).scale(0.85).move_to(DOWN * 0.9)
        with self.voiceover(
            "Act three begins: the engines inside today's models. First, attention: a weighted average, built from "
            "geometry, <bookmark mark='a'/> and the strange abilities it learns on its own."
        ) as vo:
            self.play(FadeIn(title), FadeIn(sub))
            vo.wait_until("a")
            self.play(FadeIn(smap))
        self.wait(0.5)
        self.clear_scene()
