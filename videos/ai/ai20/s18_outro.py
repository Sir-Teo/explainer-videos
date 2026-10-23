from __future__ import annotations

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (AR, CNF_C, DATA, EBM, FLOW, GAN_C, KLC, PART, RECON, SCORE_C, VAE_C, VQ_C, WGAN_C,
                                   Plane, arrows, curve, digit_sheet, load, node_box, tile_frame)
from videos.ai.ai20.s10_flows import warp_lines
from videos.ai.ai20.s13_rbm import filter_sheet

DIFF = "#7FD3FF"


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
        p = load("pixelcnn")
        out.append((digit_sheet(np.asarray(p["s0_show"])[:8], 2, 4, size=0.42, gap=0.04),
                    r"one pixel at a time", AR))
        v = load("vae")
        cv = np.asarray(v["s0_curve"])
        ax = Axes(x_range=[0, cv[-1, 1], cv[-1, 1]], y_range=[0, cv[:, 3].max(), cv[:, 3].max()], x_length=TW * 0.9,
                  y_length=TH * 0.85, tips=False, axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out.append((VGroup(ax, curve(ax, cv[:, 1], cv[:, 3], RECON, 3), curve(ax, cv[:, 1], cv[:, 4], KLC, 3)),
                    r"the ELBO's two terms", VAE_C))
        gc = load("gan2d_collapse")  # the run chapter five replayed: the seed with the fewest modes
        pl = Plane(2.0)
        ring = VGroup(*[Circle(radius=3 * 0.1 * pl.side / 6, stroke_color=DATA, stroke_width=1.2).move_to(pl.p(*c))
                        for c in np.asarray(load("toys")["ring_centers"])])  # the data's eight modes
        out.append((Group(pl, pl.scatter_image(np.asarray(gc["frame_samples"])[-1], GAN_C, radius_px=1.6), ring),
                    r"mode collapse", GAN_C))
        b = load("bilinear")
        pl2 = Plane(2.0, box=1.9)
        sim = np.asarray(b["sim"])
        n_in = int(np.argmax(np.abs(sim).max(1) > 1.85)) or len(sim)
        out.append((VGroup(pl2, VMobject(stroke_color=GAN_C, stroke_width=2.5).set_points_as_corners(pl2.pts(sim[:n_in])),
                           VMobject(stroke_color=C.INTERVAL, stroke_width=2.5).set_points_as_corners(
                               pl2.pts(np.asarray(b["extra"])))), r"the spiral", C.INTERVAL))
        f2 = load("flow2d")
        pl3 = Plane(2.0)
        out.append((VGroup(pl3, warp_lines(pl3, np.asarray(f2["moons_warp"])[-1], stroke_width=1.0)),
                    r"a flow bends the plane", FLOW))
        c = load("cnf")
        pl4 = Plane(2.0)
        out.append((Group(pl4, pl4.image(np.asarray(c["dens_t"])[-1], CNF_C)), r"a continuous flow", CNF_C))
        r = load("rbm")
        out.append((filter_sheet(np.asarray(r["big_W"])[:15], 3, 5, size=0.36), r"a Boltzmann machine's filters",
                    EBM))
        L = load("langevin")
        pl5 = Plane(2.0, box=3.0)
        out.append((Group(pl5, pl5.scatter_image(np.asarray(L["annealed"])[:800], SCORE_C, radius_px=1.4)),
                    r"annealed Langevin", SCORE_C))
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
            "Let's take stock. An autoregressive model writes an image one piece at a time, with an exact "
            "likelihood and a slow sampler. A VAE learns a code and a decoder together with one bound, trading "
            "rate against distortion. A GAN learns from a critic, and the game can collapse onto a few modes and "
            "spiral around its equilibrium; a Wasserstein critic and gradient penalties tame it. A flow bends "
            "noise into data, invertibly, with an exact likelihood, and a neural ODE does it continuously, with a "
            "trace in place of a determinant. A Boltzmann machine is an energy, trained by contrasting the data "
            "with its own dreams; and Langevin dynamics samples any energy using only its score, given enough "
            "noise to cross between modes."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        """Where each idea comes back, each with a small picture from this part's own results."""
        TW, TH = 3.7, 1.5
        pics = []
        # the score, at every noise level: our energy model's score field on the ring
        e2 = load("ebm2d")
        pl1 = Plane(TH)
        pics.append(Group(pl1, pl1.scatter_image(np.asarray(load("toys")["ring_samples"])[:600], DATA, radius_px=1.2),
                          arrows(pl1, e2["ring_score_pts"], e2["ring_score"], color=SCORE_C, max_len=0.1,
                                 stroke_width=1.2)))
        # continuous flows: noise carried along the learned field
        cn = load("cnf")
        P = np.asarray(cn["paths"])
        pl2 = Plane(TH)
        paths = VGroup(*[VMobject(stroke_color=CNF_C, stroke_width=1.0, stroke_opacity=0.5).set_points_smoothly(
            pl2.pts(np.clip(P[:, i], -2.9, 2.9))) for i in range(0, P.shape[1], 50)])
        pics.append(Group(pl2, pl2.image(np.asarray(cn["dens_t"])[-1], CNF_C), paths,
                          pl2.dots(np.clip(P[-1, ::50], -2.9, 2.9), WHITE, radius=0.016)))
        # tokens: a digit, its 7 x 7 codes, the digit decoded from them
        vq = load("vq")
        codes = np.asarray(vq["codes"])[0]
        K = int(vq["K"])
        hue = [ManimColor.from_hsv(((7 * k) % K / K, 0.45, 0.9)) for k in range(K)]
        cells = VGroup(*[Square(0.15, stroke_width=0, fill_color=hue[int(c)], fill_opacity=0.9) for c in codes.ravel()])
        cells.arrange_in_grid(7, 7, buff=0.02)
        tok = Group(digit_sheet(np.asarray(vq["src"])[:1], 1, 1, size=0.95), MathTex(r"\to", font_size=26),
                    cells, MathTex(r"\to", font_size=26),
                    digit_sheet(np.asarray(vq["recon"])[:1], 1, 1, size=0.95)).arrange(RIGHT, buff=0.15)
        pics.append(tok)
        # next-scale: one digit at 2 x 2, 7 x 7 and 14 x 14
        d = np.asarray(vq["src"])[1].astype(float)
        scales = [np.kron(d.reshape(n, 14 // n, n, 14 // n).mean((1, 3)), np.ones((14 // n, 14 // n))) for n in (2, 7, 14)]
        scales = [15.0 * x / max(x.max(), 1e-9) for x in scales]  # each scale at full contrast
        pics.append(Group(*[x for k, im in enumerate(scales) for x in
                            ([digit_sheet(im[None], 1, 1, size=0.95)] + ([MathTex(r"\to", font_size=26)] if k < 2 else []))]
                          ).arrange(RIGHT, buff=0.15))
        # pull the data up, push the rest down: our energy model's density on the ring
        E = np.asarray(e2["ring_energy"], float)
        pl5 = Plane(TH)
        pics.append(Group(pl5, pl5.image(np.exp(-(E - E.min())), EBM)))
        # judging, and how metrics fail: a single Gaussian with the ring's mean and covariance
        ev = load("eval2d")
        pl6 = Plane(TH)
        under = pl6.scatter_image(np.asarray(ev["blob"])[:800], C.MODEL_Q, radius_px=1.2).pixel_array[..., :3] / 255.0
        pics.append(Group(pl6, pl6.scatter_image(np.asarray(ev["real"])[:800], DATA, radius_px=1.2, base=under)))
        ideas = [(r"the score at every noise level: \\ diffusion", r"$\to$ \ Part 21", SCORE_C),
                 (r"continuous flows, \\ trained by regression", r"$\to$ \ Part 21", CNF_C),
                 (r"autoencoders and tokens \\ for images, video and sound", r"$\to$ \ Parts 22 and 23", VQ_C),
                 (r"next-token and \\ next-scale image models", r"$\to$ \ Part 22", AR),
                 (r"pulling data together, \\ pushing the rest apart", r"$\to$ \ Part 24", EBM),
                 (r"judging models: \\ metrics and their failures", r"$\to$ \ Part 31", C.BITS)]
        tiles = Group()
        for pic, (idea, dest, col) in zip(pics, ideas):
            box = RoundedRectangle(width=TW + 0.3, height=TH + 1.3, corner_radius=0.15, stroke_color=GREY_D,
                                   stroke_width=1.5, fill_color="#121722", fill_opacity=1)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            pic.move_to(box.get_top() + DOWN * (0.15 + TH / 2))
            il = label(idea, font_size=20, color=col).move_to(box.get_bottom() + UP * 0.72)
            dl = label(dest, font_size=18, color=GREY_A).move_to(box.get_bottom() + UP * 0.24)
            tiles.add(Group(box, pic, il, dl))
        tiles.arrange_in_grid(rows=2, cols=3, buff=(0.25, 0.3)).move_to(DOWN * 0.35)
        head = label(r"Where this comes back", font_size=40).to_edge(UP, buff=0.3)
        with self.voiceover(
            "All of this comes back. The score, learned at every noise level, is diffusion, next time, <bookmark "
            "mark='p2'/> with flow matching training continuous flows by regression. <bookmark mark='p3'/> "
            "Autoencoders and their tokens are the front end of the image, video and audio models of Parts 22 and "
            "23, <bookmark mark='p4'/> and next-scale prediction returns in Part 22. <bookmark mark='p5'/> The "
            "contrastive idea, pull the data up and push everything else down, drives the self-supervised learning "
            "of Part 24. <bookmark mark='p6'/> And the question of how to judge a model, and how its metrics fail, "
            "closes the series."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tiles[0], shift=UP * 0.1))
            for k, mk in enumerate(["p2", "p3", "p4", "p5", "p6"], 1):
                vo.wait_until(mk)
                anims = [FadeIn(tiles[k], shift=UP * 0.1)]
                if k == 1:  # the paths draw themselves, noise to data
                    anims = [FadeIn(tiles[k][0]), FadeIn(tiles[k][2]), FadeIn(tiles[k][3]), FadeIn(pl2),
                             FadeIn(tiles[k][1][1]), Create(paths, lag_ratio=0.02), FadeIn(tiles[k][1][3])]
                self.play(*anims, run_time=1.2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"Show that for fixed $G$ the best discriminator is $D^* = p / (p + q)$, \ and that "
            r"$V(D^*, G) = -\log 4 + 2\, \mathrm{JS}(p \,\|\, q)$.",
            r"Show that $\log p(x) - \mathrm{ELBO} = \mathrm{KL}\big(q(z \mid x) \,\|\, p(z \mid x)\big)$. \ If a decoder "
            r"can model $p(x)$ without $z$, \ show that $q(z \mid x) = p(z)$ maximizes the ELBO.",
            r"For the coupling layer $y_b = x_b \odot e^{s(x_a)} + t(x_a)$, $y_a = x_a$, \ show that "
            r"$\log |\det J| = \sum_i s_i(x_a)$, \ and write down the inverse.",
            r"Show that $\mathbb E[\varepsilon^\top A \varepsilon] = \mathrm{tr}\, A$ when $\mathbb E[\varepsilon "
            r"\varepsilon^\top] = I$. \ For $\varepsilon_i = \pm 1$, \ show the variance is $2 \sum_{i \ne j} S_{ij}^2$ with "
            r"$S = (A + A^\top)/2$.",
            r"For a restricted Boltzmann machine, \ derive $p(h_j = 1 \mid v) = \sigma(c_j + W_{:j}^\top v)$ and the free "
            r"energy $F(v)$.",
            r"Show that the squared 2-Wasserstein distance between $\mathcal N(\mu_1, \sigma_1^2)$ and "
            r"$\mathcal N(\mu_2, \sigma_2^2)$ is $(\mu_1 - \mu_2)^2 + (\sigma_1 - \sigma_2)^2$.",
        ], font_size=22)
        with self.voiceover(
            "Here are six problems to try, from the optimal discriminator to the Fréchet distance. Pause here and "
            "work through them; full solutions are in this part's notes."
        ) as vo:
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        L = load("langevin")
        head = label(r"Next: \ Part 21, \ Diffusion and Flow", font_size=40).to_edge(UP, buff=0.5)
        pl = Plane(4.2, center=[-3.0, -0.4, 0], box=3.0)
        ar = arrows(pl, L["field_pts"], L["field_blur"], color=SCORE_C, max_len=0.3, stroke_width=1.8)
        dots = pl.dots(np.asarray(L["annealed_path"])[0][:200], WHITE, radius=0.025)
        steps = VGroup(node_box(r"add noise to the data, \ at every level", GREY_B, font_size=22),
                       node_box(r"learn to remove it: \ the score", SCORE_C, font_size=22),
                       node_box(r"walk back from pure noise", DIFF, font_size=22)).arrange(DOWN, buff=0.4)
        steps.move_to([3.6, -0.4, 0])
        arr = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.08, color=GREY_B, stroke_width=2.5)
                       for a, b in zip(steps, steps[1:])])
        P = np.asarray(L["annealed_path"])
        with self.voiceover(
            "Next time: diffusion. Add noise to the data at every level, from a whisper to a roar; learn the score "
            "at each level by learning to remove the noise; then walk back from pure noise, level by level, the "
            "annealed Langevin of chapter thirteen grown up. Part 21: diffusion and flow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pl), FadeIn(ar), FadeIn(dots))
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s_), *([GrowArrow(arr[i - 1])] if i else []))
                                    for i, s_ in enumerate(steps)], lag_ratio=0.5), run_time=2.5)
            self.play(*[d_.animate.move_to(q) for d_, q in zip(dots, pl.pts(np.clip(P[-1][:200], -2.9, 2.9)))],
                      run_time=max(2.0, vo.remaining() - 0.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"I.~Goodfellow, Y.~Bengio \& A.~Courville, \textit{Deep Learning} (2016), chapters 16--20",
             r"S.~J.~D.~Prince, \textit{Understanding Deep Learning} (2023), chapters 14--17",
             r"K.~P.~Murphy, \textit{Probabilistic Machine Learning: Advanced Topics} (2023), part IV",
             r"C.~Villani, \textit{Optimal Transport: Old and New} (2009)"],
            [r"Shannon (1948); \ Hopfield (1982); \ Amit, Gutfreund \& Sompolinsky (1985); \ Ackley, Hinton \& "
             r"Sejnowski (1985); \ Smolensky (1986); \ Hinton (2002); \ Tieleman (2008); \ Hinton, Osindero \& Teh "
             r"(2006); \ Krotov \& Hopfield (2016); \ Ramsauer et al.\ (2020)",
             r"Dayan, Hinton, Neal \& Zemel (1995); \ Hinton, Dayan, Frey \& Neal (1995); \ Kingma \& Welling (2013); "
             r"\ Rezende, Mohamed \& Wierstra (2014); \ Bowman et al.\ (2016); \ Higgins et al.\ (2017); \ Alemi et "
             r"al.\ (2018); \ Burda, Grosse \& Salakhutdinov (2016)",
             r"Larochelle \& Murray (2011); \ Germain et al.\ (2015); \ van den Oord et al.\ (2016a, b); \ Salimans "
             r"et al.\ (2017)",
             r"Goodfellow et al.\ (2014); \ Radford, Metz \& Chintala (2015); \ Arjovsky \& Bottou (2017); \ "
             r"Arjovsky, Chintala \& Bottou (2017); \ Gulrajani et al.\ (2017); \ Mescheder, Geiger \& Nowozin (2018); "
             r"\ Karras et al.\ (2018, 2019); \ Brock, Donahue \& Simonyan (2019); \ Zhu et al.\ (2016); \ Huang et "
             r"al.\ (2024)",
             r"Tabak \& Vanden-Eijnden (2010); \ Rezende \& Mohamed (2015); \ Dinh, Krueger \& Bengio (2014); \ "
             r"Dinh, Sohl-Dickstein \& Bengio (2017); \ Kingma \& Dhariwal (2018); \ Chen et al.\ (2018); \ "
             r"Grathwohl et al.\ (2019); \ Hutchinson (1989); \ Zhai et al.\ (2025)",
             r"LeCun et al.\ (2006); \ Hyv\"arinen (2005); \ Vincent (2011); \ Du \& Mordatch (2019); \ Song \& Ermon "
             r"(2019); \ Wang \& Du (2025)",
             r"Theis, van den Oord \& Bethge (2016); \ Salimans et al.\ (2016); \ Heusel et al.\ (2017); \ Dowson \& "
             r"Landau (1982); \ Sajjadi et al.\ (2018); \ Kynk\"a\"anniemi et al.\ (2019); \ Stein et al.\ (2023)",
             r"Dhariwal \& Nichol (2021); \ van den Oord, Vinyals \& Kavukcuoglu (2017); \ Esser, Rombach \& Ommer "
             r"(2021); \ Ramesh et al.\ (2021); \ Tian et al.\ (2024); \ Sauer et al.\ (2023, 2024); \ Yin et al.\ "
             r"(2024); \ Lu \& Song (2025); \ Deng et al.\ (2026)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "To go deeper, Simon Prince's Understanding Deep Learning covers GANs, flows and VAEs clearly, and for "
            "free; Kevin Murphy's second volume covers every family in this part, in depth. Thanks for watching, and see you in "
            "Part 21."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
