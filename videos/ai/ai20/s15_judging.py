from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (AR, DATA, EBM, FAM, FLOW, GAN_C, PART, VAE_C, WGAN_C, Plane, curve, digit_sheet,
                                   load)

FAM2D = {"ar": (r"autoregressive", AR), "vae": (r"VAE", VAE_C), "gan": (r"GAN", GAN_C), "wgan": (r"WGAN-GP", WGAN_C),
         "flow": (r"RealNVP", FLOW), "ebm": (r"energy model", EBM)}


class Judging(VoiceoverScene):
    def construct(self):
        self.card()
        self.likelihood()
        self.fid()
        self.checks()
        self.prec_rec()
        self.ring_table()
        self.memory()

    def card(self):
        card = chapter_card(14, r"Judging a generator", r"How do you score a model you can't ask for a probability?",
                            lit=(), part=PART)
        with self.voiceover("Chapter fourteen. Judging a generator."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def likelihood(self):
        rows = [
            cmath(r"q(x)", r"=", r"0.01\, p_{\text{good}}(x) + 0.99\, p_{\text{noise}}(x)", font_size=36),
            cmath(r"\log q(x)", r"\ge", r"\log p_{\text{good}}(x) - \log 100", font_size=36),
        ]
        rows[0][2].set_color(C.MODEL_Q)
        whys = [why(r"a good model, \ diluted with noise"), why(r"$\log 100 \approx 4.6$ nats: \ small, per image")]
        step = ladder(self, rows, whys, keep=2, top=2.8, x=-1.6, buff=0.6, edge=6.9)
        pts = VGroup(label(r"its likelihood: \ almost as good", font_size=26, color=C.INTERVAL),
                     label(r"its samples: \ $99\%$ noise", font_size=26, color=C.SURPRISE),
                     label(r"and a GAN has no likelihood at all", font_size=26, color=GAN_C)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.4, 0])
        cite_ = cite(r"Theis, van den Oord \& Bethge, \textit{A note on the evaluation of generative models} (2016)",
                     corner=DR)
        with self.voiceover(
            "How good is a generative model? The obvious answer is its likelihood on held-out data. Lucas Theis, "
            "Aaron van den Oord and Matthias Bethge showed in 2016 why that isn't enough. Take a good model and "
            "dilute it: one sample in a hundred from the good model, the rest pure noise. <bookmark mark='a'/> Its "
            "log-likelihood drops by at most log one hundred, four and a half nats, which on an image of thousands "
            "of pixels is a rounding error. <bookmark mark='b'/> Its likelihood is nearly as good; its samples are "
            "ninety-nine percent garbage. Likelihood and sample quality can disagree. <bookmark mark='c'/> And "
            "GANs give no likelihood at all. So the field learned to judge samples directly."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]), FadeIn(cite_))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fid(self):
        c = load("classifier")
        acc = 100 * float(c["accuracy"])
        rows = [
            cmath(r"W_2^2\big(\mathcal N(\mu_1, \sigma_1^2), \mathcal N(\mu_2, \sigma_2^2)\big)", r"=",
                  r"(\mu_1 - \mu_2)^2", r"+", r"(\sigma_1 - \sigma_2)^2", font_size=32),
            cmath(r"W_2^2\big(\mathcal N(\mu_1, \Sigma_1), \mathcal N(\mu_2, \Sigma_2)\big)", r"=",
                  r"\|\mu_1 - \mu_2\|^2", r"+", r"\mathrm{tr}\Big(\Sigma_1 + \Sigma_2 - 2\big(\Sigma_1^{1/2}\, "
                  r"\Sigma_2\, \Sigma_1^{1/2}\big)^{1/2}\Big)", font_size=30),
            cmath(r"\mathrm{FID}", r"=", r"W_2^2", r"\text{ between Gaussians fitted to the features of real and "
                  r"generated images}", font_size=30),
        ]
        rows[2][0].set_color(C.BITS)
        whys = [why(r"in one dimension: \ match the quantiles"), why(r"in $d$: \ Dowson \& Landau (1982)"),
                why(r"Heusel et al.\ (2017)")]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-0.5, buff=0.6, edge=6.9)
        oneD = label(r"in 1D the best plan maps quantile to quantile: \ $x_2 = \mu_2 + \tfrac{\sigma_2}{\sigma_1}"
                     r"(x_1 - \mu_1)$", font_size=20, color=GREY_A)
        feat = VGroup(
            label(r"Inception's features: \ $2{,}048$ numbers from an ImageNet classifier", font_size=22,
                  color=GREY_A),
            label(rf"ours: \ the last hidden layer ($128$ numbers) of a digit classifier, \ test accuracy "
                  rf"${100 * float(c['accuracy']):.2f}\%$", font_size=22, color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The standard measure since 2017 is the Fréchet Inception Distance. Its core is a distance between "
            "two Gaussians. In one dimension, the cheapest way to move one Gaussian onto another maps quantile to "
            "quantile, and the squared Wasserstein distance comes out as the squared difference of the means plus "
            "the squared difference of the spreads. <bookmark mark='a'/> In many dimensions, the spreads become "
            "covariance matrices and the difference of the spreads becomes this trace with matrix square roots, "
            "Dowson and Landau's formula of 1982. <bookmark mark='b'/> Martin Heusel and colleagues in Sepp "
            "Hochreiter's group applied it not to pixels but to the features a trained classifier sees: fit a "
            "Gaussian to the features of real images and one to the features of generated images, and compute "
            "the distance. <bookmark mark='c'/> They used Google's Inception network, trained on ImageNet. For "
            "digits, we use the same idea with a classifier trained on the digits, as papers that report FID on "
            f"MNIST do: its last hidden layer, 128 numbers; it reads the test digits with {acc:.2f} percent "
            "accuracy."
        ) as vo:
            step(0)
            oneD.next_to(rows[0], DOWN, buff=0.2)
            self.play(FadeIn(oneD))
            vo.wait_until("a")
            self.play(FadeOut(oneD))
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(feat, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def checks(self):
        c = load("classifier")
        sig = list(c["noise_sigmas"])
        nf = [r["fid"] for r in c["noise"]]
        g = axes([0, sig[-1]], [0, max(nf) * 1.1], x_length=4.6, y_length=3.0, xlabel=r"noise added (pixel scale)",
                 ylabel=r"FID", xticks=sig[::2], yticks=[0, round(max(nf))], center=[-3.4, 0.5, 0])
        nc = curve(g.ax, sig, nf, C.BITS, 3)
        nd = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.06, color=C.BITS) for a, b in zip(sig, nf)])
        ex = Group(digit_sheet(np.asarray(c["ex_clean"]), 1, 4, size=0.42, gap=0.04),
                   digit_sheet(np.asarray(c["ex_noisy"]), 1, 4, size=0.42, gap=0.04),
                   digit_sheet(np.asarray(c["ex_blur"]), 1, 4, size=0.42, gap=0.04)).arrange(DOWN, buff=0.12)
        ex.move_to([-3.4, -2.5, 0])
        exl = VGroup(label(r"clean", font_size=18), label(r"noise $0.2$", font_size=18),
                     label(r"blurred", font_size=18))
        for l_, e_ in zip(exl, ex):
            l_.next_to(e_, LEFT, buff=0.15)
        ns = np.asarray(c["ns"])
        fn = np.asarray(c["fid_n"])
        top = float(fn.mean(1).max() * 1.15)
        g2 = axes([math.log10(ns[0]), math.log10(ns[-1])], [0, top], x_length=4.8, y_length=3.0,
                  xlabel=r"real digits used, \ $n$", ylabel=r"FID of real digits against the test set",
                  xticks=[2, 3, 4], yticks=[0, round(top, 1)], xfmt=lambda v: f"10^{{{int(v)}}}", center=[3.3, 0.5, 0])
        bc = curve(g2.ax, np.log10(ns), fn.mean(1), DATA, 3)
        bd = VGroup(*[Dot(g2.ax.c2p(math.log10(n_), v), radius=0.06, color=DATA) for n_, v in zip(ns, fn.mean(1))])
        mono = all(b >= a for a, b in zip(nf, nf[1:]))
        blur = float(c["blur"]["fid"])
        i2k = int(np.argmin(np.abs(ns - 2000)))
        f0, f2k, fN = (float(fn[k].mean()) for k in (0, i2k, -1))
        n0, n2k, nN = int(ns[0]), int(ns[i2k]), int(ns[-1])
        nf0, nfN = nf[0], nf[-1]
        if mono:
            rise = f"Add noise to real digits, and our FID rises with every step up in noise, from {nf0:.2f} to {nfN:.1f}."
        else:
            rise = f"Add noise to real digits, and our FID rises, overall, with the noise, from {nf0:.2f} to {nfN:.1f}."
        with self.voiceover(
            f"First, a check that the measure measures something. {rise} A three-by-three blur gives {blur:.1f}. "
            "<bookmark mark='a'/> "
            "Second, a warning. FID compares estimated means and covariances, and estimates from a few samples "
            "are noisy, which biases the distance upward. Real digits against the test set give an FID of "
            f"{f0:.2f} with {n0} samples, {f2k:.2f} with {n2k:,}, and {fN:.2f} with {nN:,}. <bookmark mark='b'/> So "
            f"FIDs can only be compared at the same number of samples. Ours always use {n2k:,}, which puts the "
            f"floor, a perfect model, at about {f2k:.2f}."
        ) as vo:
            self.play(FadeIn(g), Create(nc), FadeIn(nd), FadeIn(ex), FadeIn(exl))
            vo.wait_until("a")
            self.play(FadeIn(g2), Create(bc), FadeIn(bd))
            vo.wait_until("b")
            self.play(Indicate(bd[i2k], color=DATA, scale_factor=1.8))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prec_rec(self):
        e2 = load("eval2d")
        real = np.asarray(e2["real"])[:120]
        g2 = load("gan2d")
        fake = np.asarray(g2["ring_ns_s0"])[:120]
        pl = Plane(4.8, center=[-3.3, -0.2, 0])
        k = 3
        dd = np.sqrt(((real[:, None] - real[None]) ** 2).sum(-1))
        rad = np.sort(dd, 1)[:, k]
        s = pl.side / (2 * pl.box)
        balls = VGroup(*[Circle(radius=r * s, stroke_width=0, fill_color=DATA, fill_opacity=0.18).move_to(pl.p(*p))
                         for p, r in zip(real, rad)])
        rd = pl.dots(real, DATA, radius=0.03)
        fd = pl.dots(np.clip(fake, -2.95, 2.95), GAN_C, radius=0.035)
        df = np.sqrt(((fake[:, None] - fake[None]) ** 2).sum(-1))
        frad = np.sort(df, 1)[:, k]
        fballs = VGroup(*[Circle(radius=r * s, stroke_width=0, fill_color=GAN_C, fill_opacity=0.18).move_to(pl.p(*p))
                          for p, r in zip(np.clip(fake, -2.95, 2.95), frad)])
        defs = VGroup(
            label(r"each real point's ball: \ out to its $3$rd nearest real neighbour", font_size=20, color=DATA),
            label(r"precision: \ the share of generated samples inside some real ball", font_size=22,
                  color=C.INTERVAL),
            label(r"recall: \ the share of real points inside some generated ball", font_size=22, color=C.SURPRISE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.2, 1.0, 0])
        r0 = e2["rows"]["gan"][0]
        num = label(rf"this GAN \ (non-saturating, seed $0$): \ precision ${r0['precision']:.2f}$, \ recall "
                    rf"${r0['recall']:.2f}$", font_size=22, color=GAN_C).move_to([3.2, -1.3, 0])
        cite_ = cite(r"Sajjadi et al.\ (2018); \ Kynk\"a\"anniemi et al.\ (2019)", corner=DR)
        verdict = ("High precision, low recall: what it makes is real-looking, but it covers only part of the data."
                   if r0["precision"] > r0["recall"] + 0.15 else
                   "The two numbers say different things, which is the point of having two.")
        with self.voiceover(
            "One number can't say whether a model's samples are good or whether they cover the data, and those are "
            "different failures. Mehdi Sajjadi and colleagues, and then Tuomas Kynkäänniemi and colleagues at NVIDIA, "
            "split it in two. <bookmark mark='a'/> Around each real point, draw a ball reaching out to its third "
            "nearest real neighbour: together, the balls estimate where the data lives. <bookmark mark='b'/> "
            "Precision is the share of generated samples that land inside the real balls: how many of the fakes "
            "look real. <bookmark mark='c'/> Recall is the reverse: draw balls around the generated samples, and "
            "count the real points they cover. <bookmark mark='d'/> Here is the non-saturating GAN of chapter "
            f"five, on the ring: precision {r0['precision']:.2f}, recall {r0['recall']:.2f}. {verdict}"
        ) as vo:
            self.play(FadeIn(pl), FadeIn(rd), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(balls), FadeIn(defs[0]))
            vo.wait_until("b")
            self.play(FadeIn(fd), FadeIn(defs[1]))
            vo.wait_until("c")
            self.play(FadeIn(fballs), FadeIn(defs[2]))
            vo.wait_until("d")
            self.play(FadeIn(num))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ring_table(self):
        e2 = load("eval2d")
        g = axes([0, 1], [0, 1], x_length=4.4, y_length=4.4, xlabel=r"precision", ylabel=r"recall",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-3.6, -0.3, 0])
        dots, keys = VGroup(), VGroup()
        for f in e2["families"]:
            nm, col = FAM2D[f]
            for r in e2["rows"][f]:
                dots.add(Dot(g.ax.c2p(r["precision"], r["recall"]), radius=0.07, color=col))
            keys.add(VGroup(Dot(radius=0.07, color=col), label(nm, font_size=20, color=col)).arrange(RIGHT, buff=0.12))
        keys.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(g, RIGHT, buff=0.25).shift(UP * 0.6)
        pl = Plane(3.0, center=[4.6, 1.3, 0])
        blob = pl.scatter_image(np.asarray(e2["blob"]), C.MODEL_Q, radius_px=1.3)
        bl = label(r"a single Gaussian with the ring's mean and covariance", font_size=18, color=C.MODEL_Q)
        bl.next_to(pl, DOWN, buff=0.1)
        if bl.width > 4.2:
            bl.width = 4.2
        nums = VGroup(
            label(rf"its Fr\'echet distance to the ring: \ ${float(e2['blob_fd']):.3f}$ \ (real vs real: "
                  rf"${float(e2['real_fd']):.3f}$)", font_size=20, color=C.MODEL_Q),
            label(rf"its precision: \ ${float(e2['blob_precision']):.2f}$", font_size=20, color=C.MODEL_Q),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(bl, DOWN, buff=0.15)
        if nums.width > 5.2:
            nums.width = 5.2
        nums.set_x(4.3)
        mean = {f: (float(np.mean([r["precision"] for r in e2["rows"][f]])),
                    float(np.mean([r["recall"] for r in e2["rows"][f]]))) for f in e2["families"]}
        best_p = max(mean, key=lambda f: mean[f][0])
        best_r = max(mean, key=lambda f: mean[f][1])
        worst_p = min(mean, key=lambda f: mean[f][0])
        spoken = {"ar": "the autoregressive model", "vae": "the VAE", "gan": "the GAN", "wgan": "WGAN-GP",
                  "flow": "the flow", "ebm": "the energy model"}
        n_bp, n_br, n_wp = spoken[best_p], spoken[best_r], spoken[worst_p]
        v_bp, v_br, v_wp = mean[best_p][0], mean[best_r][1], mean[worst_p][0]
        bfd, bprec = float(e2["blob_fd"]), float(e2["blob_precision"])
        with self.voiceover(
            "Now every family, on the ring, three seeds each, against two thousand fresh points of the data. "
            f"<bookmark mark='a'/> The highest precision belongs to {n_bp}, at {v_bp:.2f} on average; the highest "
            f"recall to {n_br}, at {v_br:.2f}; and the lowest precision to {n_wp}, at {v_wp:.2f}. "
            "<bookmark mark='b'/> And here is why FID alone is dangerous. Fit one Gaussian blob to the ring, with "
            "the same mean and covariance, and sample from it. Its Fréchet distance to the ring is "
            f"{bfd:.3f}, about as small as that between two samples of the ring itself, because the Fréchet "
            f"distance sees only means and covariances. Its precision is {bprec:.2f}. On images, features rich enough make this failure rarer, but "
            "never impossible."
        ) as vo:
            self.play(FadeIn(g), FadeIn(keys))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=1.5) for d_ in dots], lag_ratio=0.06), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(pl), FadeIn(blob), FadeIn(bl))
            self.play(FadeIn(nums))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def memory(self):
        e, c = load("evaluate"), load("classifier")
        fams = ["pixelcnn", "vae", "gan", "flow"]
        rows = Group()
        for f in fams:
            src = np.asarray(load(f)["s0_show"])[:6]
            near = np.asarray(e[f"mem_{f}_nearest"])[:6]
            pair = Group(digit_sheet(src, 1, 6, size=0.4, gap=0.03), MathTex(r"\to", font_size=24),
                         digit_sheet(near, 1, 6, size=0.4, gap=0.03)).arrange(RIGHT, buff=0.12)
            nm = label(r"PixelCNN" if f == "pixelcnn" else {"vae": r"VAE", "gan": r"GAN", "flow": r"RealNVP"}[f],
                       font_size=20, color=FAM[f])
            rows.add(Group(nm, pair).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.15).move_to([-2.4, 0.2, 0])
        hdr = label(r"samples \ $\to$ \ their nearest training digits", font_size=20, color=GREY_A).next_to(rows, UP,
                                                                                                         buff=0.15)
        real_d = float(np.median(e["mem_real_dist"]))
        med = {f: float(np.median(e[f"mem_{f}_dist"])) for f in fams}
        lo = min(med.values())
        bars = VGroup()
        for i, f in enumerate(fams + ["real"]):
            v = med[f] if f != "real" else real_d
            col = FAM[f]
            bars.add(VGroup(label(r"PixelCNN" if f == "pixelcnn" else {"vae": r"VAE", "gan": r"GAN",
                                                                         "flow": r"RealNVP",
                                                                         "real": r"real test digits"}[f],
                                  font_size=18, color=col),
                            MathTex(f"{v:.3f}", font_size=24, color=col)).arrange(RIGHT, buff=0.2))
        bars.arrange(DOWN, aligned_edge=RIGHT, buff=0.18).move_to([4.6, 0.0, 0])
        bh = label(r"median distance to the \\ nearest training digit \ (RMS per pixel)", font_size=18,
                   color=GREY_A).next_to(bars, UP, buff=0.2)
        floor = float(c["real"]["fid"])
        rp, rr = float(c["real"]["precision"]), float(c["real"]["recall"])
        copying = lo < 0.5 * real_d
        verdict = ("None of our models is copying: their samples are about as far from the training set as real "
                   "test digits are." if not copying else
                   "One of them sits suspiciously close to the training set: it may be copying.")
        with self.voiceover(
            "One failure no sample metric catches is memorization. A model that simply replayed its training "
            f"digits would score exactly like real data: an FID of {floor:.2f}, at the floor, precision {rp:.2f} "
            f"and recall {rr:.2f}. <bookmark mark='a'/> So we check "
            "directly: for each sample, find the nearest of the sixty thousand training digits. <bookmark "
            f"mark='b'/> Real test digits sit at a median distance of {real_d:.3f} from their nearest training "
            f"digit. {verdict} Measures of this kind, and features from stronger networks than Inception, such "
            "as DINOv2, are where evaluation research has gone since."
        ) as vo:
            self.play(FadeIn(hdr))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()
