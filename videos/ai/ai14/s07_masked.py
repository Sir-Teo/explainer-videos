from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import MONO, load


class Masked(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.writing()

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

        def row(mask):
            return VGroup(*[Text("_" if (mk and ch != " ") else ch, font=MONO, font_size=34,
                                 color=GREY_D if (mk and ch != " ") else WHITE) for ch, mk in zip(s, mask)]).arrange(RIGHT, buff=0.06)

        full = row(np.zeros(len(s), bool)).move_to(UP * 1.6)
        half = row(m).move_to(UP * 0.4)
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
            "both sides, and guesses every blank. Weighted by one over t, that's a bound on the bits per character, "
            "the same quantity as on our scoreboard. LLaDA, in 2025, trained an eight-billion-parameter language "
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

        def cell(ch, i, fresh=False):  # fixed character cells, so that every round lines up with the next
            row, col = divmod(i, half)
            if ch == " ":
                m = Dot(radius=0.02, color=GREY_D)
            else:
                m = Text(ch, font=MONO, font_size=28, color=GREY_D if ch == "_" else C.BITS if fresh else WHITE)
            return m.move_to([-6.0 + step * (col + 0.5), 0.9 - 1.0 * row, 0])

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
            self.play(FadeIn(cur), FadeIn(counter), FadeIn(info))
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
