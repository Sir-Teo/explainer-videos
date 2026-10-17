from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai14.common import DATA, DDIM_C, DDPM_C, FM_C, NOISE, RF_C, arrows_field, cloud, curve, gray_image, load


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

        out = []
        t = load("toy")
        out.append((arrows_field(np.asarray(t["grid"]), t["field0.25"], unit=0.5, max_len=0.2, stroke_width=1.5),
                    r"a learned score", C.MODEL_Q))
        P = np.asarray(t["ddpm_path"])
        out.append((VGroup(*[VMobject(stroke_width=1, stroke_color=DDPM_C, stroke_opacity=0.6).set_points_as_corners(
            [[p[i, 0] * 0.5, p[i, 1] * 0.5, 0] for p in P]) for i in range(0, 300, 12)]), r"DDPM's wandering paths", DDPM_C))
        out.append((cloud(np.asarray(t["ddim20"])[:400], DDIM_C, radius=0.015, scale=0.5), r"DDIM, $20$ steps", DDIM_C))
        f = load("flow")
        F = np.asarray(f["fm_path"])
        out.append((VGroup(*[VMobject(stroke_width=1, stroke_color=FM_C, stroke_opacity=0.7).set_points_smoothly(
            [[p[i, 0] * 0.5, p[i, 1] * 0.5, 0] for p in F[::10]]) for i in range(0, 300, 12)]), r"flow matching", FM_C))
        R = np.asarray(f["rf_path"])
        out.append((VGroup(*[VMobject(stroke_width=1, stroke_color=RF_C, stroke_opacity=0.7).set_points_smoothly(
            [[p[i, 0] * 0.5, p[i, 1] * 0.5, 0] for p in R[::10]]) for i in range(0, 300, 12)]), r"reflow: straight", RF_C))
        g = load("guidance")
        out.append((cloud(np.asarray(g["w4"])[:400], FM_C, radius=0.015, scale=0.45), r"guidance, $w = 4$", C.BITS))
        gl = load("glyphs")
        out.append((Group(*[gray_image(im, 0.42) for im in np.asarray(gl["samples"])[:12]]).arrange_in_grid(rows=2, cols=6, buff=0.04),
                    r"letters from noise", WHITE))
        m = load("masked")
        fr = [str(x) for x in m["frames"][0]]
        out.append((VGroup(*[Text(fr[k][:22], font="DejaVu Sans Mono", font_size=16, color=GREY_A) for k in (4, 10, 16)])
                    .arrange(DOWN, aligned_edge=LEFT, buff=0.1), r"text by unmasking", C.BITS))
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
        head = label(r"Part 14, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. A diffusion model learns to guess the noise in a noisy example, and that guess is the "
            "score. DDPM walks back from noise with a little randomness at every step; DDIM walks a fixed path in "
            "far fewer. Flow matching learns straight-line velocities, and reflow straightens the paths until one "
            "step will do. Guidance turns a request into a push. The same machinery makes pictures, and, with "
            "blanks for noise, text."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"diffusion in a compressed latent space; \ transformers as denoisers", [15]),
            (r"generating speech and sound", [16]),
            (r"world models that imagine the next frame", [18]),
            (r"fewer steps, \ faster serving", [19]),
        ], font_size=26)
        with self.voiceover(
            "Next time this machinery meets real images and video, in a compressed space and with transformers as "
            "the denoisers. Speech generators use it too, in part sixteen; world models imagine the next frame with "
            "it, in part eighteen; and part nineteen is about making it fast."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 15, \ Images and Video", font_size=40).to_edge(UP, buff=0.4)
        gl = load("glyphs")
        im = np.asarray(gl["samples"])[0]
        big = gray_image(im, 3.0).move_to(LEFT * 3)
        n = im.shape[0]
        lines = VGroup(*[Line(big.get_corner(UL) + RIGHT * 3.0 * k / 4, big.get_corner(DL) + RIGHT * 3.0 * k / 4, color=C.BITS,
                              stroke_width=1.5) for k in range(1, 4)],
                       *[Line(big.get_corner(UL) + DOWN * 3.0 * k / 4, big.get_corner(UR) + DOWN * 3.0 * k / 4, color=C.BITS,
                              stroke_width=1.5) for k in range(1, 4)])
        toks = VGroup(*[Square(0.4, stroke_color=C.BITS, stroke_width=1.5, fill_color=C.BITS, fill_opacity=0.15) for _ in range(16)])
        toks.arrange(RIGHT, buff=0.06).scale(0.8).move_to(RIGHT * 2.6 + DOWN * 0.2)
        tl = label(r"an image as a sequence of patches", font_size=26, color=GREY_A).next_to(toks, DOWN, buff=0.3)
        with self.voiceover(
            "Next time: images and video. A picture is cut into patches, and the patches become tokens, "
            "<bookmark mark='a'/> so the transformers of part eleven can look at pictures, and denoise them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(big))
            self.play(Create(lines))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.2) for t_ in toks], lag_ratio=0.05), FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapter 18"]
        papers = [
            r"J.~Sohl-Dickstein et al.\ (2015); \ J.~Ho, A.~Jain \& P.~Abbeel, \textit{DDPM} (2020)",
            r"Y.~Song et al., \textit{Score-Based Generative Modeling through SDEs} (2021); \ J.~Song et al., \textit{DDIM} (2021)",
            r"Y.~Lipman et al., \textit{Flow Matching} (2023); \ X.~Liu et al., \textit{Rectified Flow} (2023)",
            r"J.~Ho \& T.~Salimans, \textit{Classifier-Free Guidance} (2022); \ P.~Esser et al., \textit{Stable Diffusion 3} (2024)",
            r"J.~Austin et al., \textit{D3PM} (2021); \ S.~Sahoo et al., \textit{MDLM} (2024); \ S.~Nie et al., \textit{LLaDA} (2025)",
        ]
        card = reference_card(books, papers)
        data = note(r"Points: Part 4's ``AI''; \ letters from the system's fonts; \ text: Part 1's novels. \ Every model "
                    r"here is trained on this video's CPU.", font_size=20).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=20)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        with self.voiceover(
            "Sander Dieleman's blog posts on diffusion are a wonderful companion. Thanks for watching, and see you in "
            "part fifteen."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
