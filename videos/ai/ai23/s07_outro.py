from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai23.common import IMG_C, SND_C, TEXT_C, gray_image, heat, load, token_chips


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0

        def frame(caption, color):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            return box, label(caption, font_size=22, color=color).move_to(box.get_bottom() + UP * 0.28)

        b, v, s, c = load("bpe"), load("vq"), load("sound"), load("clip")
        out = [
            (token_chips([str(x) for x in b["first"]][:8], font_size=18, height=0.36), r"byte-pair merges", TEXT_C),
            (token_chips([str(x) for x in b["cut8000"]], font_size=18, height=0.36), r"a sentence in tokens", TEXT_C),
            (Group(*[gray_image(x, 0.42) for x in np.asarray(v["codebook16"])]).arrange_in_grid(rows=2, cols=8, buff=0.04),
             r"a codebook", IMG_C),
            (Group(*[gray_image(np.asarray(v[f"img_rvq{k}"]), 0.7) for k in range(1, 5)]).arrange(RIGHT, buff=0.06),
             r"residual stages", IMG_C),
            (heat(np.asarray(s["spec"])[::-1], 2.9, 1.6, color=SND_C), r"a spectrogram", SND_C),
            (heat(np.asarray(s["rec4"])[::-1], 2.9, 1.6, color=SND_C), r"rebuilt from codes", SND_C),
            (heat(np.asarray(c["sim_clip"]), 1.8, 1.8, signed=True), r"matching pictures and words", C.TRUE_P),
            (VGroup(*[Square(0.26, stroke_width=1, stroke_color=col, fill_color=col, fill_opacity=0.35)
                      for col in [TEXT_C] * 3 + [IMG_C] * 4 + [SND_C] * 3]).arrange(RIGHT, buff=0.04), r"one sequence", WHITE),
        ]
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = frame(cap, col)
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.3)).move_to(DOWN * 0.3)
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(r"Part 23, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Text is cut into tokens by merging the commonest pairs, again and again. Pictures and "
            "sound become tokens through codebooks, refined in stages. Contrastive training puts pictures and words "
            "in one space, with a softmax or a sigmoid. And with everything as tokens, one model reads, sees, "
            "listens and speaks."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"thinking in tokens", [28]),
            (r"acting: \ robot actions as tokens", [29]),
            (r"fewer bits per number", [19]),
        ], font_size=26)
        with self.voiceover(
            "Act four begins next. Reasoning models think in tokens, in part twenty-eight. Robots read the world and "
            "write actions as tokens, in part twenty-nine. And part nineteen squeezes the numbers themselves into fewer "
            "bits."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 28, \ Reasoning \ (Act IV: Agency)", font_size=40).to_edge(UP, buff=0.4)
        lines = VGroup(Text("Q: 347 + 589 = ?", font="DejaVu Sans Mono", font_size=30, color=WHITE),
                       Text("7 + 9 = 16, write 6, carry 1", font="DejaVu Sans Mono", font_size=26, color=GREY_A),
                       Text("4 + 8 + 1 = 13, write 3, carry 1", font="DejaVu Sans Mono", font_size=26, color=GREY_A),
                       Text("3 + 5 + 1 = 9", font="DejaVu Sans Mono", font_size=26, color=GREY_A),
                       Text("A: 936", font="DejaVu Sans Mono", font_size=30, color=C.BITS)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        lines.move_to(DOWN * 0.3)
        tag = note(r"illustrative").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Next time, act four, agency, begins with reasoning: <bookmark mark='a'/> why writing the steps out "
            "makes a model smarter, and how models learn to do it by trial and error."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.2) for l_ in lines[1:]], lag_ratio=0.4), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"D.~Jurafsky \& J.~H.~Martin, \textit{Speech and Language Processing} (3rd ed.\ draft), chapters 2 and 16"]
        papers = [
            r"P.~Gage (1994); \ R.~Sennrich, B.~Haddow \& A.~Birch, \textit{Neural Machine Translation of Rare Words} (2016)",
            r"A.~van den Oord et al., \textit{VQ-VAE} (2017); \ F.~Mentzer et al., \textit{Finite Scalar Quantization} (2023)",
            r"N.~Zeghidour et al., \textit{SoundStream} (2021); \ A.~D\'efossez et al., \textit{EnCodec} (2022), \textit{Moshi} (2024)",
            r"A.~Radford et al., \textit{CLIP} (2021); \ X.~Zhai et al., \textit{SigLIP} (2023)",
            r"G.~E.~Peterson \& H.~L.~Barney, \textit{Control Methods Used in a Study of the Vowels} (1952); \ Qwen Team, "
            r"\textit{Qwen3-Omni} (2025)",
        ]
        card = reference_card(books, papers)
        data = note(r"Text: Part 1's novels; \ letters from the system's fonts; \ a synthesized voice. \ Every number "
                    r"here is computed and checked; \ illustrations are labeled.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover("Thanks for watching, and see you in part twenty-eight."):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
