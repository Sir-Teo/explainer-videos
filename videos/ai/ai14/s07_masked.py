from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import MONO, load


class Masked(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.writing()
        self.blocks()

    def card(self):
        card = chapter_card(6, r"Diffusion for text", r"Can text be written all at once?", part=14)
        with self.voiceover("Chapter six. Diffusion for text."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        s = "Spade looked at the girl."
        g = np.random.default_rng(1)
        m = g.random(len(s)) < 0.5

        def row(mask):  # one monospace line: the blanks keep their columns and the letters their baseline
            t = data_text("".join("_" if (mk and ch != " ") else ch for ch, mk in zip(s, mask)), font=MONO, font_size=34,
                          color=WHITE)
            for glyph, mk in zip(t, [mk for ch, mk in zip(s, mask) if ch != " "]):  # Text has no glyph for a space
                if mk:
                    glyph.set_color(GREY_D)
            return t

        full, half = row(np.zeros(len(s), bool)), row(m)
        full.move_to(UP * 1.6)
        half.move_to(UP * 0.4).align_to(full, LEFT)
        a1 = Arrow(full.get_bottom(), half.get_top(), buff=0.1, color=GREY_B)
        noise = label(r"the noise: \ blank out characters, \ each with probability $t$", font_size=24, color=GREY_A)
        noise.next_to(a1, RIGHT, buff=0.3)
        colors = {r"t": C.BITS}
        f = cmath(r"\mathcal{L}", "=", r"\frac{1}{t}", r"\sum_{\text{blanked } i}", r"-\log q_\theta(x_i \mid \text{the rest})",
                  colors=colors, font_size=36).move_to(DOWN * 1.4)
        fl = label(r"guess every blank from everything else, \ both sides", font_size=24, color=GREY_A).next_to(f, DOWN, buff=0.2)
        cite_ = cite(r"S.~Nie et al., \textit{LLaDA: Large Language Diffusion Models} (2025)", corner=DR)
        with self.voiceover(
            "Text isn't made of continuous numbers, so what's the noise? Blanks. Blank out each character with "
            "probability t; at t equal to one, everything is blank. <bookmark mark='a'/> The model sees the rest, on "
            "both sides, and guesses every blank. Weighted by one over t, that's a bound on the bits per character: "
            "a guaranteed ceiling, so the true figure can only be lower. It's the same quantity as on our scoreboard. LLaDA, in 2025, trained an eight-billion-parameter language "
            "model this way."
        ) as vo:
            self.play(FadeIn(full), FadeIn(cite_))
            self.play(GrowArrow(a1), FadeIn(half), FadeIn(noise))
            vo.wait_until("a")
            self.play(Write(f), FadeIn(fl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def writing(self):
        d = load("masked")
        frames = [str(f_) for f_ in d["frames"][0]]
        T = len(frames[0])
        half = T // 2

        step = 12.0 / half

        def at(i):
            row, col = divmod(i, half)
            return np.array([-6.0 + step * (col + 0.5), 0.9 - 1.0 * row, 0])

        def cell(ch, i, fresh=False):  # fixed character cells, so that every round lines up with the next
            if ch == " ":
                m = Dot(radius=0.025, color=GREY_B)
            elif ch == "_":  # a blank: an empty slot, its line at the foot of the cell
                return Line(LEFT * step * 0.3, RIGHT * step * 0.3, color=GREY_B, stroke_width=2.5).move_to(at(i) + DOWN * 0.2)
            else:
                m = Text(ch, font=MONO, font_size=28, color=C.BITS if fresh else WHITE)
            return m.move_to(at(i))

        slots = VGroup(*[RoundedRectangle(width=step * 0.84, height=0.62, corner_radius=0.05, stroke_color=GREY_C, stroke_width=1.2,
                                          fill_color="#151B27", fill_opacity=1).move_to(at(i)) for i in range(T)])
        cur = VGroup(*[cell(ch, i) for i, ch in enumerate(frames[0])])
        counter = VGroup(label(r"round", font_size=26, color=GREY_A), Integer(0, font_size=30, color=C.BITS)).arrange(RIGHT, buff=0.2)
        counter.to_edge(UP, buff=0.5)
        info = label(rf"our model: \ ${d['n_params'] / 1e6:.1f}$ million numbers, \ two-way attention, \ "
                     rf"trained on the novels; \ bound on held-out text: \ ${d['bound']:.2f}$ bits per character",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.45)
        rule = label(r"each round: \ fill every blank, \ keep only the surest guesses", font_size=24, color=C.BITS)
        rule.next_to(info, UP, buff=0.3)
        with self.voiceover(
            f"Here's our own small text diffuser writing {T} characters. It starts with all blanks. "
            "<bookmark mark='a'/> Each round it guesses every blank, keeps only the guesses it's surest of, and "
            "blanks the rest again. <bookmark mark='b'/> Words appear in no particular order, wherever the model is "
            "confident first, and the rest fills in around them. It's a different way to write: all at once, "
            "then refined, rather than left to right."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(VGroup(b_, c_)) for b_, c_ in zip(slots, cur)], lag_ratio=0.01), FadeIn(counter),
                      FadeIn(info), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            fresh = []
            for r, fr in enumerate(frames[1:], start=1):  # only what this round reveals moves; it lights up, then settles
                prev = frames[r - 1]
                changed = [i for i in range(T) if prev[i] != fr[i]]
                anims = [Transform(cur[i], cell(fr[i], i, fresh=True)) for i in changed]
                anims += [cur[i].animate.set_color(WHITE) for i in fresh if i not in changed and fr[i] != " "]
                self.play(*anims, counter[1].animate.set_value(r), run_time=0.45)  # the counter keeps the list non-empty
                fresh = changed
            last = [cur[i].animate.set_color(WHITE) for i in fresh if frames[-1][i] != " "]
            if last:
                self.play(*last, run_time=0.3)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blocks(self):
        """Block diffusion: left to right across blocks, diffusion inside each one."""
        n, B = 24, 8
        cw = 0.42
        cells = VGroup(*[Square(cw, stroke_color=GREY_C, stroke_width=1.5, fill_color="#121722", fill_opacity=1) for _ in range(n)])
        cells.arrange(RIGHT, buff=0.06).move_to([0, 1.3, 0])
        for b in range(1, n // B):
            cells[b * B:].shift(RIGHT * 0.25)
        cells.move_to([0, 1.3, 0])
        masks = VGroup(*[MathTex(r"\cdot", font_size=30, color=GREY_B).move_to(c) for c in cells])
        g = np.random.default_rng(14)
        order = [list(g.permutation(B)) for _ in range(n // B)]
        braces = VGroup(*[Brace(VGroup(*cells[b * B:(b + 1) * B]), DOWN, buff=0.1, color=GREY_B) for b in range(n // B)])
        bl = VGroup(*[label(rf"block {b + 1}", font_size=18, color=GREY_B).next_to(braces[b], DOWN, buff=0.08) for b in range(n // B)])
        ar = VGroup(*[CurvedArrow(bl[b].get_bottom() + DOWN * 0.1, bl[b + 1].get_bottom() + DOWN * 0.1, angle=0.6,
                                  color=C.TRUE_P, stroke_width=2.5) for b in range(n // B - 1)])
        al = label(r"left to right, \ block by block \ (with a key-value cache)", font_size=20, color=C.TRUE_P).next_to(ar, DOWN, buff=0.15)
        f = MathTex(r"\log p(x) = \sum_{b} \log p\big(x^{(b)} \mid x^{(<b)}\big)", font_size=34).move_to([0, -1.6, 0])
        fl = label(r"each factor: \ masked diffusion inside the block, \ a few tokens per step", font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.15)
        ends = label(r"block size $1$: \ an ordinary language model; \ \ one block for everything: \ this chapter's model",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        tag = note(r"schematic").to_corner(UR, buff=0.3)
        cite_ = cite(r"M.~Arriola et al., \textit{Block Diffusion} (2025); \ S.~Nie et al., \textit{LLaDA} (2025)", corner=UL)
        with self.voiceover(
            "Writing everything at once has a cost: the length is fixed in advance, and nothing can be cached. "
            "Block diffusion splits the difference. <bookmark mark='a'/> The text is cut into blocks. Within a block, "
            "tokens are unmasked a few at a time, as here; <bookmark mark='b'/> across blocks, it goes left to right, "
            "like an ordinary language model, so finished blocks can be cached and the text can run as long as it "
            "likes. <bookmark mark='c'/> With blocks of one token, it is an ordinary language model; with a single "
            "block, it's this chapter's. Commercial diffusion language models, Google's Gemini Diffusion and "
            "Inception's Mercury, report writing over a thousand tokens a second."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cite_), FadeIn(cells), FadeIn(masks), LaggedStart(*[GrowFromCenter(b_) for b_ in braces], lag_ratio=0.2),
                      FadeIn(bl))
            vo.wait_until("a")
            for b in range(n // B):
                for step in range(0, B, 3):
                    idx = [b * B + i for i in order[b][step:step + 3]]
                    self.play(*[masks[i].animate.become(MathTex(r"\bullet", font_size=30, color=C.BITS).move_to(cells[i])) for i in idx],
                              *[cells[i].animate.set_fill(C.BITS, 0.3) for i in idx], run_time=0.35)
                if b == 0:
                    vo.wait_until("b")
                    self.play(Create(ar), FadeIn(al))
            vo.wait_until("c")
            self.play(Write(f), FadeIn(fl))
            self.play(FadeIn(ends))
        self.wait(0.3)
        self.clear_scene()
