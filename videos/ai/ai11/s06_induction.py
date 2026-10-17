from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import A, K, MONO, Q, V, char_row, curve, heat_image, load


class Induction(VoiceoverScene):
    def construct(self):
        self.card()
        self.copying()
        self.mechanism()
        self.phase()

    def card(self):
        card = chapter_card(5, r"Induction heads", r"How does a model copy what it has just seen?", part=11)
        with self.voiceover("Chapter five. Induction heads."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def copying(self):
        t = load("tf")
        b1, b2 = np.asarray(t["copy_bits1"]), np.asarray(t["copy_bits2"])
        L = len(b1) + 1
        txt = str(t["ind_text"])
        half = len(txt) // 2
        row = char_row(txt, 12.4, font_size=22).move_to(UP * 2.7)
        for i in range(half, len(txt)):
            row[i].set_color(C.BITS)
        ax = Axes(x_range=[0, L, 10], y_range=[0, 6, 1], x_length=8.6, y_length=3.6, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-1.0, -0.9, 0])
        yt = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1) for v in (0, 2, 4, 6)])
        xn = label(r"position in the string", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yn = label(r"bits per character", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        c1 = curve(ax, np.arange(1, L), b1, GREY_B, 3)
        c2 = curve(ax, np.arange(1, L), b2, C.BITS, 3.5)
        lg = math.log2(26)
        ref = DashedLine(ax.c2p(0, lg), ax.c2p(L, lg), color=GREY_D, stroke_width=1.5)
        refl = MathTex(r"\log_2 26", font_size=24, color=GREY_B).next_to(ax.c2p(L, lg), RIGHT, buff=0.1)
        k1 = label(rf"first time: \ ${b1[5:].mean():.1f}$ bits", font_size=26, color=GREY_B).move_to([4.6, 0.4, 0])
        k2 = label(rf"second time: \ ${b2[5:].mean():.2f}$ bits", font_size=26, color=C.BITS).next_to(k1, DOWN, buff=0.3)
        k2.align_to(k1, LEFT)
        tag = note(rf"averaged over $24$ random strings of ${L}$ letters, \ each shown twice").to_edge(DOWN, buff=0.25)
        assert b1[5:].mean() > 3.5 and b2[5:].mean() < 0.5 * b1[5:].mean()
        with self.voiceover(
            "Here's a test no novel prepared our transformer for: random letters, then the same random letters "
            "again. <bookmark mark='a'/> The first time through, nothing can be predicted: about four point seven "
            "bits a letter, a guess among twenty-six. <bookmark mark='b'/> The second time, it predicts almost "
            f"every letter: {b2[5:].mean():.1f} bits. It has never seen these strings. It copies them from its own "
            "context, as it reads."
        ) as vo:
            self.play(FadeIn(row), Create(ax), FadeIn(yt), FadeIn(xn), FadeIn(yn), Create(ref), FadeIn(refl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(k1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(k2), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def mechanism(self):
        s = "the Falcon ... the Fal"
        row = char_row(s, 11.0, font_size=34).move_to(UP * 1.4)
        i_cur = len(s) - 1  # the 'l' being read
        j_prev = s.index("Fal") + 2  # the earlier 'l'
        j_next = j_prev + 1  # what came after it: 'c'
        box = SurroundingRectangle(row[i_cur], color=Q, buff=0.08)
        # head 1: every position notes the character before it
        prevs = VGroup(*[CurvedArrow(row[k - 1].get_bottom() + DOWN * 0.08, row[k].get_bottom() + DOWN * 0.08, angle=PI / 2,
                                     color=K, stroke_width=2.5, tip_length=0.12)
                         for k in range(1, len(s)) if s[k] != " " and s[k - 1] != " "])
        h1 = label(r"head 1, \ an earlier layer: \ each character notes the one before it", font_size=26, color=K)
        h1.move_to(DOWN * 0.4)
        # head 2: the query looks for a key whose previous character matches its own
        arc = ArcBetweenPoints(row[i_cur].get_top() + UP * 0.1, row[j_next].get_top() + UP * 0.1, angle=-PI / 3.2,
                               color=A, stroke_width=6)
        h2 = label(r"head 2: \ ``which earlier character came right after one like me?'' \\ attend there, \ copy it",
                   font_size=26, color=A).next_to(h1, DOWN, buff=0.4)
        guess = VGroup(label(r"next:", font_size=30, color=GREY_A), Text("c", font=MONO, font_size=40, color=C.BITS))
        guess.arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.6)
        rule = label(r"$[\,a\,][\,b\,] \;\dots\; [\,a\,] \;\to\; [\,b\,]$", font_size=34, color=WHITE).next_to(guess, UP, buff=0.3)
        tag = note(r"schematic").to_corner(DR, buff=0.3)
        cite_ = cite(r"C.~Olsson et al., \textit{In-context Learning and Induction Heads} (2022)", corner=UL)
        with self.voiceover(
            "How? Two heads, in two layers, working together. <bookmark mark='a'/> In an earlier layer, a head that "
            "only ever looks one step back: each character's vector now also says which character came before it. "
            "<bookmark mark='b'/> In a later layer, the second head. The character being read is an 'l'. Its query "
            "asks: which earlier character came right after an 'l'? The key of the 'c' in Falcon answers, because "
            "its note says: the one before me was an 'l'. <bookmark mark='c'/> So the head attends there and copies "
            "it: 'c'. Seen A followed by B? On seeing A again, predict B. Catherine Olsson and colleagues at "
            "Anthropic named these induction heads in 2022."
        ) as vo:
            self.play(FadeIn(row), Create(box), FadeIn(tag), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(p) for p in prevs], lag_ratio=0.05), FadeIn(h1), run_time=1.8)
            vo.wait_until("b")
            self.play(Create(arc), FadeIn(h2), Indicate(row[j_next], color=A))
            vo.wait_until("c")
            self.play(FadeIn(rule), FadeIn(guess, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def phase(self):
        d = load("induction")
        c1, c2 = np.asarray(d["curve1"]), np.asarray(d["curve2"])
        V_ = int(d["V"])
        top = math.ceil(math.log2(V_)) + 0.5
        ax = Axes(x_range=[0, c2[-1, 0], 1000], y_range=[0, top, 1], x_length=6.6, y_length=3.8, tips=False,
                  axis_config={"stroke_color": GREY_C, "include_ticks": True, "tick_size": 0.04}).move_to([-3.2, -0.3, 0])
        xt = VGroup(*[MathTex(f"{v:,}".replace(",", "{,}"), font_size=20, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in range(0, int(c2[-1, 0]) + 1, 1000)])
        xn = label(r"training steps", font_size=22, color=GREY_A).next_to(xt, DOWN, buff=0.12)
        yn = label(r"bits per token, \ on the repeated stretch", font_size=22, color=GREY_A).next_to(ax, UP, buff=0.12)
        yn.align_to(ax, LEFT)
        l1 = curve(ax, c1[:, 0], c1[:, 1], GREY_B, 3)
        l2 = curve(ax, c2[:, 0], c2[:, 1], A, 3.5)
        k1 = label(r"one layer", font_size=24, color=GREY_B).next_to(ax.c2p(c1[-1, 0], c1[-1, 1]), UP, buff=0.12).shift(LEFT * 0.6)
        k2 = label(r"two layers", font_size=24, color=A).next_to(ax.c2p(c2[-1, 0], c2[-1, 1]), UP, buff=0.12).shift(LEFT * 0.6)
        js = int(d["jump_step"])
        jl = DashedLine(ax.c2p(js, 0), ax.c2p(js, top), color=A, stroke_width=1.5)
        S = 2.6
        mp = heat_image(np.asarray(d["map_prev"]), S, S, color=K, mask_upper=True)
        mi = heat_image(np.asarray(d["map_ind"]), S, S, color=A, mask_upper=True)
        maps = Group(mp, mi).arrange(RIGHT, buff=0.35).move_to([3.6, -0.1, 0])
        frames = VGroup(*[SurroundingRectangle(m, buff=0, color=GREY_D, stroke_width=1.5) for m in maps])
        t1 = label(r"layer 1: \ one back", font_size=22, color=K).next_to(mp, UP, buff=0.12)
        t2 = label(r"layer 2: \ the induction head", font_size=22, color=A).next_to(mi, UP, buff=0.12)
        ax_l = label(r"each row: \ a position, \ looking back along it", font_size=20, color=GREY_B).next_to(maps, DOWN, buff=0.15)
        stripe = label(r"the stripe: \ the repeat looking at its source, \ one step ahead", font_size=22,
                       color=GREY_A).next_to(ax_l, DOWN, buff=0.12)
        head = label(rf"a small attention-only model, \ ${V_}$ random tokens with a repeated stretch", font_size=26)
        head.to_edge(UP, buff=0.35)
        with self.voiceover(
            "Induction heads can be watched as they form. Train a small model of attention alone on random tokens "
            "with a repeated stretch somewhere inside. <bookmark mark='a'/> With one layer, it can never copy: one "
            "head can't both note the previous token and search for it. <bookmark mark='b'/> With two layers, "
            "nothing happens for a while, and then, around step "
            f"{js:,}, the loss on the repeat falls off a cliff. <bookmark mark='c'/> Look inside: the first layer "
            "has a head that looks exactly one step back, and the second a head that looks at the earlier copy, one "
            "step ahead. In large models the same jump happens early in training, right when they get good at "
            "learning from their prompt."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(xn), FadeIn(yn))
            vo.wait_until("a")
            self.play(Create(l1), FadeIn(k1), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(l2), FadeIn(k2), run_time=2.5)
            self.play(Create(jl))
            vo.wait_until("c")
            self.play(FadeIn(maps), Create(frames), FadeIn(t1), FadeIn(t2), FadeIn(ax_l))
            self.play(FadeIn(stripe))
        self.wait(0.3)
        self.clear_scene()
