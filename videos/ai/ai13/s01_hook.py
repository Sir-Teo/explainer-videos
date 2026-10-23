from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai13.common import A, HIST, PART, attention_arcs, char_row, framed, heat_image, load


class Hook(VoiceoverScene):
    def construct(self):
        self.reading()
        self.grid()
        self.era()
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
            "called attention, and it is the engine of every large language model today."
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
            f"Our model has {L * H} of these looks, called heads, each its own way of weighing the past: here are all "
            f"{L * H}, on the same sentence. <bookmark mark='a'/> This part is "
            "about the mathematics of that look: what it computes, how it knows where things are, and what it can "
            "learn to do."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(m, scale=0.9) for m in imgs], lag_ratio=0.04), FadeIn(rl), FadeIn(hl),
                      FadeIn(cap), run_time=2.5)
            vo.wait_until("a")
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def era(self):
        """How we got here: from a weighted average in 1964 to the hybrids of 2026, evenly spaced (not to scale)."""
        events = [
            (1964, r"Nadaraya, Watson: \\ a weighted average"),
            (1982, r"Hopfield: \\ a memory that recalls"),
            (2014, r"Bahdanau et al.: \\ attention, for translation"),
            (2017, r"Vaswani et al.: \\ attention is all you need"),
            (2021, r"rotary positions; \\ ALiBi"),
            (2022, r"induction heads; \\ FlashAttention"),
            (2023, r"attention sinks; \\ YaRN; \ grouped queries"),
            (2024, r"latent attention \\ (DeepSeek-V2)"),
            (2025, r"sparse and gated attention; \\ sink logits"),
            (2026, r"hybrids: \\ Qwen3.5, \ Kimi K3"),
        ]
        n = len(events)
        xs = np.linspace(-6.2, 6.2, n)
        y0 = -0.2
        axis = Line([-6.6, y0, 0], [6.6, y0, 0], color=GREY_C, stroke_width=3)
        marks = []
        for i, ((yr, txt), x) in enumerate(zip(events, xs)):
            up = i % 2 == 0
            stem = Line([x, y0, 0], [x, y0 + (0.9 if up else -0.9), 0], color=HIST, stroke_width=2.5)
            dot = Dot([x, y0, 0], radius=0.08, color=HIST)
            yl = label(rf"{yr}", font_size=28, color=HIST)
            t = label(txt, font_size=19, color=WHITE)
            words = VGroup(yl, t).arrange(DOWN, buff=0.05)
            words.next_to(stem.get_end(), UP if up else DOWN, buff=0.08)
            keep_in_frame(words, margin=0.1)
            marks.append(VGroup(stem, dot, words))
        head = label(r"How we got here", font_size=42).to_edge(UP, buff=0.3)
        tag = note(r"milestones evenly spaced, \ not to scale").to_corner(DR, buff=0.2)
        with self.voiceover(
            "The idea is older than it looks. In 1964 two statisticians, Elizbar Nadaraya and Geoffrey Watson, "
            "guessed a value by averaging its neighbours, weighted by how close they were. <bookmark mark='a'/> In "
            "1982 John Hopfield built a network that recalls a whole memory from a fragment. <bookmark mark='b'/> "
            "In 2014 a translation network learned where to look in the sentence it was translating, "
            "<bookmark mark='c'/> and in 2017 a team at Google built a network of nothing but that looking: the "
            "transformer. <bookmark mark='d'/> Then came better ways to give positions, <bookmark mark='e'/> the "
            "discovery of heads that copy, and kernels fast enough for long texts; <bookmark mark='f'/> strange "
            "heads that stare at the first token, and tricks to read far past the training length; "
            "<bookmark mark='g'/> smaller memories of the past, <bookmark mark='h'/> attention that looks at only "
            "some of it, and gates that let a head switch off; <bookmark mark='i'/> and in 2026, models that keep "
            "full attention in only a quarter of their layers."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(tag))
            self.play(FadeIn(marks[0], shift=UP * 0.2))
            for k, mk in enumerate("abcdefghi"):
                vo.wait_until(mk)
                self.play(FadeIn(marks[k + 1], shift=(UP if (k + 1) % 2 == 0 else DOWN) * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Attention as Geometry", font_size=48).to_edge(UP, buff=0.45)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"attention as a weighted average, \ as a memory, \ and why it divides by $\sqrt{d}$",
            r"heads as low-rank maps, \ masks, \ and what a block costs",
            r"our own transformer, \ trained here and replayed",
            r"positions: \ sinusoids, \ ALiBi, \ rotations, \ none at all; \ trained side by side, \ "
            r"and stretched past their training length",
            r"sinks, \ gates and caps: \ the fixes inside today's softmax",
            r"what heads learn: \ induction, \ learning in context, \ programs, \ and limits",
        ], font_size=24).move_to(DOWN * 0.35)
        with self.voiceover(
            "This is Part 13 of AI, Built, and the start of the third act: the transformer era. <bookmark mark='a'/> "
            "In it: what attention computes, as an average and as a memory; heads, masks and costs; our own "
            "transformer, trained and replayed; four ways to tell it where things are, and how to stretch them; "
            "the fixes inside today's softmax; and what heads learn to do, and what they cannot."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
