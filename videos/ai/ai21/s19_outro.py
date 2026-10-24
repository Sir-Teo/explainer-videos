from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import (CFG_C, DATA, DDIM_C, DDPM_C, FM_C, MDM_C, MONO, NOISE, PART, RF2_C, SCORE, SOLVER_C, Panel,
                                   glyph_sheet, load, panel_arrows, tile_frame)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        TW, TH = 3.0, 2.0
        out = []
        f = load("forward")
        fr = np.asarray(f["frames"])
        pn = Panel(TW, xlim=(-3.2, 3.4), ylim=(-2.4, 2.0), frame=False)
        under = pn.scatter(fr[-1][:400], NOISE, radius_px=1.2, res=260).pixel_array[..., :3] / 255.0
        mid = pn.scatter(fr[6][:400], interpolate_color(ManimColor(DATA), ManimColor(NOISE), 0.5), radius_px=1.2, res=260,
                         base=under).pixel_array[..., :3] / 255.0
        out.append((Group(pn, pn.scatter(fr[0][:400], DATA, radius_px=1.2, res=260, base=mid)), r"data into noise, \ slowly",
                    NOISE))
        d = load("denoiser")
        pn2 = Panel(TW, frame=False)
        out.append((VGroup(pn2, panel_arrows(pn2, np.asarray(d["grid"]), np.asarray(d["field0.25"]), max_len=0.2,
                                             stroke_width=1.3)), r"a learned score", SCORE))
        s = load("sde")
        pn3 = Panel(TW, xlim=(-3.2, 3.4), ylim=(-3.0, 2.6), frame=False)
        out.append((VGroup(pn3, pn3.paths(np.asarray(s["sde_paths"])[:, :6], DDPM_C, stroke_width=0.9, opacity=0.55),
                           pn3.paths(np.asarray(s["ode_paths"])[:, :24], DDIM_C, stroke_width=1.6, opacity=0.9)),
                    r"two ways back: \ SDE and ODE", DDIM_C))
        so = load("solvers")
        ax = CornerAxes(x_range=[0, 1.6], y_range=[-3, 0.2], x_length=TW * 0.9, y_length=TH * 0.85, tips=False,
                        axis_config={"stroke_color": GREY_D, "include_ticks": False})
        lines = VGroup(ax)
        for k in ("ddim", "heun", "dpmpp2m"):
            pts = [ax.c2p(math.log10(r["nfe"]) - 0.5, max(math.log10(max(r["err"], 1e-3)), -3)) for r in so[k]]
            lines.add(VMobject(color=SOLVER_C[k], stroke_width=2.5).set_points_as_corners(pts))
        out.append((lines, r"solvers: \ error by steps", SOLVER_C["dpmpp2m"]))
        fl = load("flow")
        pn4 = Panel(TW, frame=False)
        out.append((VGroup(pn4, pn4.paths(np.asarray(fl["rf2_path"])[:, ::3], RF2_C, stroke_width=1.0, opacity=0.8, smooth=True)),
                    r"reflow: \ straight paths", RF2_C))
        g = load("guidance")
        pn5 = Panel(TW, xlim=(-3.0, 3.0), ylim=(-1.6, 1.6), frame=False)
        j = [float(w) for w in g["w"]].index(4.0)
        out.append((Group(pn5, pn5.scatter(np.asarray(g["cfg_x"])[j], CFG_C, radius_px=1.3, res=260)), r"guidance, \ $w = 4$",
                    CFG_C))
        gl = load("glyphs")
        out.append((glyph_sheet(np.asarray(gl["samples"])[:12], 2, 6, size=0.42, gap=0.04, frame=False), r"letters from noise",
                    WHITE))
        m = load("textlm")
        frs = [str(x) for x in m["frames"][0]]
        n = len(frs)
        out.append((VGroup(*[data_text(frs[k][:22], font=MONO, font_size=16, color=GREY_A) for k in (n // 4, n // 2, n - 1)])
                    .arrange(DOWN, aligned_edge=LEFT, buff=0.1), r"text by unmasking", MDM_C))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
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
        head = label(rf"Part {PART}, in eight pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. A diffusion model destroys data slowly with noise, and learns to undo it. The bound "
            "that trains it is a sum of noise-guessing errors, and the best noise guess is the score, by Tweedie's "
            "formula; denoising score matching learns it by plain regression. Time can be run back with a "
            "stochastic equation or a deterministic one; DDPM and DDIM discretize them, and EDM and DPM-Solver "
            "solve them in ten to thirty steps. Flow matching learns straight-line velocities, reflow straightens "
            "the paths, and distillation or MeanFlow reaches a single step. Guidance turns a request into a push. "
            "The same machinery draws pictures, and, with blanks for noise, writes text."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"diffusion in latent spaces; \ transformers as denoisers; \ video", [22]),
            (r"generating speech and sound", [23]),
            (r"denoising as a way to learn features", [24]),
            (r"diffusion for molecules and proteins", [25]),
            (r"world models that imagine the next frame", [29]),
            (r"fewer steps, \ faster serving", [19]),
        ], font_size=24)
        with self.voiceover(
            "This machinery comes back. Next time it meets real images and video, in compressed latent spaces with "
            "transformers as the denoisers. Speech and sound generators use it, in Part 23; denoising as a way to "
            "learn features returns in Part 24; diffusion builds molecules and protein structures in Part 25; world "
            "models imagine the next frame with it in Part 29; and making it fast is part of Part 19's story."
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"For $q(x_t \mid x_{t-1}) = \mathcal N(\sqrt{1-\beta_t}\, x_{t-1}, \beta_t I)$, \ show that $q(x_t \mid x_0) = "
            r"\mathcal N(\sqrt{\bar\alpha_t}\, x_0, (1-\bar\alpha_t) I)$ with $\bar\alpha_t = \prod_{s \le t}(1-\beta_s)$.",
            r"For $x = \alpha x_0 + \sigma \varepsilon$, \ prove Tweedie's formula $\mathbb E[x_0 \mid x] = (x + \sigma^2 \nabla \log "
            r"p(x))/\alpha$, \ and deduce the best noise guess $-\sigma \nabla \log p(x)$.",
            r"Prove that denoising score matching and explicit score matching differ by a constant independent of $\theta$.",
            r"Show that DDIM's step $x_s = \alpha_s \hat x_0 + \sigma_s \hat\varepsilon$ solves $dx/d\sigma = (x - D)/\sigma$ "
            r"exactly, \ in $x/\alpha$ and $\sigma/\alpha$, \ when $D = \hat x_0$ is constant over the step.",
            r"Show that classifier-free guidance with weight $w$ follows the score of $p(x)\, p(c \mid x)^w$, \ and that "
            r"$w = 1$ gives the conditional model.",
            r"For masked diffusion on $n$ symbols, \ show $\binom{n}{k}\int_0^1 t^{k-1}(1-t)^{n-k}\, dt = 1/k$, \ and deduce "
            r"that the bound is the any-order autoregressive loss.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems, from the forward process's closed form to the masked bound. Pause here and work "
            "through them; full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        head = label(r"Next: \ Part 22, \ Images, Video and 3D", font_size=40).to_edge(UP, buff=0.4)
        gl = load("glyphs")
        im = np.asarray(gl["samples"])[0]
        from videos.ai.ai21.common import gray_image

        big = gray_image(im, 3.0).move_to(LEFT * 3)
        lines = VGroup(*[Line(big.get_corner(UL) + RIGHT * 3.0 * k / 4, big.get_corner(DL) + RIGHT * 3.0 * k / 4, color=C.BITS,
                              stroke_width=1.5) for k in range(1, 4)],
                       *[Line(big.get_corner(UL) + DOWN * 3.0 * k / 4, big.get_corner(UR) + DOWN * 3.0 * k / 4, color=C.BITS,
                              stroke_width=1.5) for k in range(1, 4)])
        toks = VGroup(*[Square(0.4, stroke_color=C.BITS, stroke_width=1.5, fill_color=C.BITS, fill_opacity=0.15) for _ in range(16)])
        toks.arrange(RIGHT, buff=0.06).scale(0.8).move_to(RIGHT * 2.6 + DOWN * 0.2)
        tl = label(r"a picture as a sequence of patches", font_size=26, color=GREY_A).next_to(toks, DOWN, buff=0.3)
        with self.voiceover(
            "Next time: images, video and 3D. A picture is cut into patches, and the patches become tokens, "
            "<bookmark mark='a'/> so the transformers of Part 13 can look at pictures, and denoise them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(big))
            self.play(Create(lines))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_, shift=RIGHT * 0.2) for t_ in toks], lag_ratio=0.05), FadeIn(tl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        books = [r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapter 18",
                 r"K.~P.~Murphy, \textit{Probabilistic Machine Learning: Advanced Topics} (2023), chapter 25",
                 r"C.~Villani, \textit{Optimal Transport: Old and New} (2009)"]
        papers = [
            r"Sohl-Dickstein et al.\ (2015); \ Ho, Jain \& Abbeel (2020); \ Song \& Ermon (2019); \ Song et al.\ (2021); \ "
            r"Anderson (1982); \ Robbins (1956); \ Efron (2011); \ Hyv\"arinen (2005); \ Vincent (2011)",
            r"Song, Meng \& Ermon (2021); \ Nichol \& Dhariwal (2021); \ Kingma et al.\ (2021); \ Lin et al.\ (2024); \ Karras et "
            r"al.\ (2022, 2024); \ Lu et al.\ (2022a, b)",
            r"Benamou \& Brenier (2000); \ Lipman et al.\ (2023); \ Liu, Gong \& Liu (2023); \ Albergo \& Vanden-Eijnden "
            r"(2023); \ Albergo, Boffi \& Vanden-Eijnden (2023); \ Tong et al.\ (2024); \ Pooladian et al.\ (2023)",
            r"Salimans \& Ho (2022); \ Song et al.\ (2023); \ Lu \& Song (2025); \ Yin et al.\ (2024a, b); \ Geng et al.\ (2025); \ "
            r"Frans et al.\ (2024); \ Liu et al.\ (2024)",
            r"Dhariwal \& Nichol (2021); \ Ho \& Salimans (2022); \ Rombach et al.\ (2022); \ Peebles \& Xie (2023); \ Esser et "
            r"al.\ (2024)",
            r"Austin et al.\ (2021); \ Uria et al.\ (2014); \ Hoogeboom et al.\ (2022); \ Lou, Meng \& Ermon (2024); \ Sahoo et "
            r"al.\ (2024); \ Shi et al.\ (2024); \ Ou et al.\ (2024); \ Nie et al.\ (2025); \ Arriola et al.\ (2025); \ Wu et "
            r"al.\ (2025); \ Prabhudesai et al.\ (2025); \ Inception Labs (2025); \ Ant Group et al.\ (2025)",
        ]
        card = reference_card(books, papers)
        data = note(r"Points: Part 5's ``AI'' as a mixture of $400$ Gaussians; \ letters from the system's fonts; \ text: "
                    r"Part 1's novels. \ Every model here is trained on this video's CPU.", font_size=19).to_edge(DOWN, buff=0.25)
        credit = note(rf"Animated with Manim Community; \ narrated by {narration_credit()}.", font_size=19)
        credit.next_to(data, UP, buff=0.1)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.15:
            card.shift(UP * (credit.get_top()[1] + 0.15 - card.get_bottom()[1]))
        if card.get_top()[1] > 3.9:
            card.scale((3.9 - credit.get_top()[1] - 0.15) / card.height).next_to(credit, UP, buff=0.15)
        with self.voiceover(
            "To go deeper, Simon Prince's Understanding Deep Learning covers diffusion clearly and for free, and "
            "Sander Dieleman's blog posts on diffusion are a wonderful companion. Thanks for watching, and see you in "
            "Part 22."
        ):
            self.play(LaggedStart(FadeIn(card), FadeIn(credit), FadeIn(data), lag_ratio=0.3), run_time=3)
        self.wait(2.0)
        self.play(FadeOut(Group(*self.mobjects)))
