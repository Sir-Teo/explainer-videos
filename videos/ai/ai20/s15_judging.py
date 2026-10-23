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
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([1.0, -1.4, 0])
        # a hundred draws from q: one from the good model (a PixelCNN sample), ninety-nine of noise
        mix = np.random.default_rng(14).integers(0, 16, (100, 14, 14)).astype(float)
        k_good = 37
        mix[k_good] = np.asarray(load("pixelcnn")["s0_show"])[0]
        sz, gp = 0.21, 0.02
        sheet = digit_sheet(mix, 10, 10, size=sz, gap=gp).move_to([-4.5, -1.1, 0])
        img = sheet[1]
        r_, c_ = divmod(k_good, 10)
        hit = Square(sz + 0.06, color=AR, stroke_width=2.5).move_to(
            [img.get_left()[0] + c_ * (sz + gp) + sz / 2, img.get_top()[1] - r_ * (sz + gp) - sz / 2, 0])
        mcap = label(r"$100$ draws from $q$: \\ one from the good model", font_size=20, color=GREY_A).next_to(
            sheet, DOWN, buff=0.15)
        cite_ = cite(r"Theis, van den Oord \& Bethge, \textit{A note on the evaluation of generative models} (2016)",
                     corner=DR)
        with self.voiceover(
            "How good is a generative model? Its held-out likelihood isn't enough, as Lucas Theis, Aaron van den "
            "Oord and Matthias Bethge showed in 2016: dilute a good model, one sample in a hundred from it, the rest "
            "noise. <bookmark mark='a'/> The log-likelihood drops by at most log one hundred, a rounding error on "
            "an image. <bookmark mark='b'/> The samples are ninety-nine percent garbage. <bookmark mark='c'/> And "
            "GANs have no likelihood at all. So the field judges samples directly."
        ) as vo:
            step(0)
            self.play(FadeIn(sheet), FadeIn(mcap))
            self.play(Create(hit))
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]), FadeIn(cite_), Indicate(sheet, scale_factor=1.04))
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
            cmath(r"\mathrm{FID}", r"=", r"W_2^2\big(\mathcal N(\mu_r, \Sigma_r), \mathcal N(\mu_g, \Sigma_g)\big)",
                  font_size=32),
        ]
        rows[2][0].set_color(C.BITS)
        whys = [why(r"in one dimension: \ match the quantiles"), why(r"in $d$: \ Dowson \& Landau (1982)"),
                why(r"Gaussians fitted to the features of real ($r$) and generated ($g$) images: \ Heusel et al.\ (2017)")]
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
            "The standard since 2017 is the Fréchet Inception Distance, a distance between Gaussians. In one "
            "dimension the cheapest move maps quantile to quantile, and the squared Wasserstein distance is the "
            "squared gap in means plus the squared gap in spreads. <bookmark mark='a'/> In many dimensions, "
            "covariances and a trace of matrix roots: Dowson and Landau, 1982. <bookmark mark='b'/> Martin Heusel "
            "and colleagues fitted those Gaussians to the features a trained classifier sees, real against "
            "generated. <bookmark mark='c'/> They used Inception, trained on ImageNet; for digits, we use a digit "
            f"classifier's last hidden layer, 128 numbers, {acc:.2f} percent accurate on the test digits."
        ) as vo:
            step(0)
            oneD.next_to(VGroup(rows[0], whys[0]), DOWN, buff=0.3)
            # one Gaussian carried onto another, quantile by quantile
            qa = axes([-3.5, 4.5], [0, 0.75], x_length=6.4, y_length=1.6, xticks=[], yticks=[], center=[-0.3, -2.3, 0])
            xg = np.linspace(-3.5, 4.5, 300)
            npdf = lambda x, m, s: np.exp(-0.5 * ((x - m) / s) ** 2) / (s * np.sqrt(2 * np.pi))
            g1 = curve(qa.ax, xg, npdf(xg, -1.2, 0.6), DATA, 3)
            g2_ = curve(qa.ax, xg, npdf(xg, 1.6, 1.0), C.MODEL_Q, 3)
            qs = [-1.28, -0.67, 0.0, 0.67, 1.28]
            qarr = VGroup(*[Arrow(qa.ax.c2p(-1.2 + 0.6 * z, 0.05), qa.ax.c2p(1.6 + 1.0 * z, 0.05), buff=0.02,
                                  color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.12,
                                  path_arc=-0.5) for z in qs])
            self.play(FadeIn(oneD), FadeIn(qa), Create(g1), Create(g2_))
            self.play(LaggedStart(*[Create(a_) for a_ in qarr], lag_ratio=0.2), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeOut(VGroup(oneD, qa, g1, g2_, qarr)))
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
            rise = f"noise added to real digits raises our FID at every step, from {nf0:.2f} to {nfN:.1f}."
        else:
            rise = f"noise added to real digits raises our FID overall, from {nf0:.2f} to {nfN:.1f}."
        with self.voiceover(
            f"A check: {rise} A three-by-three blur gives {blur:.1f}. <bookmark mark='a'/> A warning: few samples "
            "bias FID upward. Real digits against the test set score "
            f"{f0:.2f} with {n0} samples, {f2k:.2f} with {n2k:,}, {fN:.2f} with {nN:,}. <bookmark mark='b'/> So "
            f"compare at equal sample counts: ours use {n2k:,}, putting a perfect model at about {f2k:.2f}."
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
        pr0, rc0 = r0["precision"], r0["recall"]
        num = label(rf"this GAN \ (non-saturating, seed $0$): \ precision ${r0['precision']:.2f}$, \ recall "
                    rf"${r0['recall']:.2f}$", font_size=22, color=GAN_C).move_to([3.2, -1.3, 0])
        cite_ = cite(r"Sajjadi et al.\ (2018); \ Kynk\"a\"anniemi et al.\ (2019)", corner=DR)
        verdict = ("High precision, low recall: what it makes is real-looking, but it covers only part of the data."
                   if r0["precision"] > r0["recall"] + 0.15 else
                   "The two numbers say different things, which is the point of having two.")
        with self.voiceover(
            "One number can't separate good samples from good coverage. Mehdi Sajjadi and colleagues, then Tuomas "
            "Kynkäänniemi and colleagues at NVIDIA, split it in two. <bookmark mark='a'/> Around each real point, a "
            "ball out to its third nearest real neighbour: where the data lives. <bookmark mark='b'/> Precision: "
            "the share of generated samples inside real balls. <bookmark mark='c'/> Recall: the share of real "
            "points inside generated balls. <bookmark mark='d'/> Chapter five's non-saturating GAN, seed zero: "
            f"precision {pr0:.2f}, recall {rc0:.2f}. {verdict}"
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
        g = axes([0, 1], [0, 1], x_length=4.4, y_length=4.4, xlabel=r"precision{}", ylabel=r"recall",
                 xticks=[0, 0.5, 1], yticks=[0, 0.5, 1], center=[-3.6, -0.3, 0])  # "{}": a zh key of its own (the shared table has bare "precision" as 精度)
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
            "Every family on the ring, three seeds each. <bookmark mark='a'/> Highest precision: "
            f"{n_bp}, {v_bp:.2f}; highest recall: {n_br}, {v_br:.2f}; lowest precision: {n_wp}, {v_wp:.2f}. "
            "<bookmark mark='b'/> And why FID alone is dangerous: one Gaussian blob with the ring's mean and "
            f"covariance has a Fréchet distance of {bfd:.3f}, about that between two samples of the ring itself, "
            f"and a precision of {bprec:.2f}."
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
        train = np.concatenate([np.asarray(e[f"mem_{f}_nearest"])[:3] for f in fams])
        replay = Group(digit_sheet(train, 2, 6, size=0.55, gap=0.06),
                       label(rf"replaying training digits: \ FID ${floor:.2f}$, \ precision ${rp:.2f}$, \ recall ${rr:.2f}$",
                             font_size=26, color=GREY_A)).arrange(DOWN, buff=0.3).move_to([0, 0.2, 0])
        ws, wl = replay[0].width * 0.55, replay[1].width * 0.75  # then down to the bottom, side by side
        x0 = -(ws + 0.3 + wl) / 2
        with self.voiceover(
            "No sample metric catches memorization: replaying training digits scores exactly like real data, "
            f"an FID of {floor:.2f}, precision {rp:.2f}, recall {rr:.2f}. <bookmark mark='a'/> So we check: each "
            "sample's nearest training digit. <bookmark mark='b'/> Real test digits sit a median "
            f"{real_d:.3f} from theirs. {verdict}"
        ) as vo:
            self.play(FadeIn(replay[0]), FadeIn(replay[1]))
            vo.wait_until("a")
            self.play(replay[0].animate.scale(0.55).move_to([x0 + ws / 2, -2.6, 0]),
                      replay[1].animate.scale(0.75).move_to([x0 + ws + 0.3 + wl / 2, -2.6, 0]), run_time=1.0)
            self.play(FadeIn(hdr), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in rows], lag_ratio=0.3),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bh), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.2))
        self.wait(0.3)
        self.clear_scene()
