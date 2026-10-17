from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import LETTERS, PATCH, gray_image, load


class Latent(VoiceoverScene):
    def construct(self):
        self.card()
        self.squeeze()
        self.space()
        self.diffuse()
        self.vae()
        self.tradeoff()
        self.training()

    def card(self):
        card = chapter_card(2, r"A smaller space", r"Why denoise every pixel?", part=15)
        with self.voiceover("Chapter two. A smaller space."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def squeeze(self):
        d = load("latent")
        Z, n = int(d["Z"]), np.asarray(d["orig"]).shape[-1]
        orig, rec = np.asarray(d["orig"]), np.asarray(d["rec"])
        enc = Polygon([-1.2, 1.0, 0], [1.2, 0.4, 0], [1.2, -0.4, 0], [-1.2, -1.0, 0], stroke_color=PATCH, stroke_width=2.5,
                      fill_color=PATCH, fill_opacity=0.12).move_to([-1.6, 0.6, 0])
        dec = Polygon([-1.2, 0.4, 0], [1.2, 1.0, 0], [1.2, -1.0, 0], [-1.2, -0.4, 0], stroke_color=PATCH, stroke_width=2.5,
                      fill_color=PATCH, fill_opacity=0.12).move_to([2.6, 0.6, 0])
        el = label(r"encoder", font_size=22, color=PATCH).move_to(enc)
        dl = label(r"decoder", font_size=22, color=PATCH).move_to(dec)
        zc = VGroup(*[Square(0.18, stroke_width=0.6, stroke_color=GREY_D, fill_color=C.EMBED, fill_opacity=0.7) for _ in range(Z)])
        zc.arrange(DOWN, buff=0).scale_to_fit_height(1.6).move_to([0.5, 0.6, 0])
        zl = label(rf"${Z}$ numbers", font_size=22, color=C.EMBED).next_to(zc, DOWN, buff=0.15)
        a_in = gray_image(orig[0], 1.6).move_to([-4.6, 0.6, 0])
        a_out = gray_image(rec[0], 1.6).move_to([5.4, 0.6, 0])
        il = label(rf"${n * n}$ pixels", font_size=22, color=GREY_A).next_to(a_in, DOWN, buff=0.15)
        ol = label(r"rebuilt", font_size=22, color=GREY_A).next_to(a_out, DOWN, buff=0.15)
        pairs = Group(*[Group(gray_image(o, 0.6), gray_image(r, 0.6)).arrange(DOWN, buff=0.05) for o, r in zip(orig[:10], rec[:10])])
        pairs.arrange(RIGHT, buff=0.12).to_edge(DOWN, buff=0.5)
        pl = label(r"top: \ the pictures; \ bottom: \ rebuilt from $16$ numbers", font_size=20, color=GREY_A).next_to(pairs, UP, buff=0.1)
        cite_ = cite(r"R.~Rombach et al., \textit{Latent Diffusion Models} (2022)", corner=UR)
        with self.voiceover(
            f"Real pictures have millions of pixels, and most of that detail is predictable. So first, train an "
            f"autoencoder: an encoder squeezes each picture into a few numbers, here {Z} instead of {n * n}, and a "
            "decoder rebuilds the picture from them. <bookmark mark='a'/> The rebuilt letters are close to the "
            f"originals: {n * n // Z} times fewer numbers, little lost."
        ) as vo:
            self.play(FadeIn(a_in), FadeIn(il), FadeIn(enc), FadeIn(el), FadeIn(zc), FadeIn(zl), FadeIn(dec), FadeIn(dl),
                      FadeIn(a_out), FadeIn(ol), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.1), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def space(self):
        d = load("latent")
        Q, N = np.asarray(d["nn_query"]), np.asarray(d["nn_imgs"])
        ql, nl = [int(x) for x in d["nn_qlabels"]], np.asarray(d["nn_labels"])
        same, chance = float(d["nn_same"]), float(d["nn_chance"])
        S = 0.8
        rows = Group()
        for q, ns, lq, lns in zip(Q, N, ql, nl):
            qi = gray_image(q, S)
            box = SurroundingRectangle(qi, color=C.BITS, buff=0.03, stroke_width=2.5)
            arrow = MathTex(r"\rightarrow", font_size=36, color=GREY_B)
            nbrs = Group(*[Group(gray_image(n_, S), SurroundingRectangle(gray_image(n_, S), buff=0.03, stroke_width=2,
                                                                         color=C.INTERVAL if int(l_) == lq else C.SURPRISE))
                           for n_, l_ in zip(ns, lns)]).arrange(RIGHT, buff=0.12)
            rows.add(Group(Group(qi, box), arrow, nbrs).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-1.0, -0.4, 0])
        head = label(r"each picture, \ and the $6$ pictures nearest to it in the $16$ numbers", font_size=24, color=GREY_A)
        head.to_edge(UP, buff=0.4)
        key = VGroup(label(r"green: \ the same letter", font_size=22, color=C.INTERVAL),
                     label(r"red: \ a different one", font_size=22, color=C.SURPRISE)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        key.move_to([5.2, 1.2, 0])
        res = label(rf"over all the pictures: \\ ${100 * same:.0f}\%$ of neighbours \\ are the same letter \\ "
                    rf"(by chance: \ ${100 * chance:.0f}\%$)", font_size=24, color=C.INTERVAL).next_to(key, DOWN, buff=0.5)
        res.align_to(key, LEFT)
        good = same > 5 * chance
        with self.voiceover(
            "And the space of those few numbers has structure. <bookmark mark='a'/> Take a picture, and find the "
            "pictures whose sixteen numbers are closest to its own. "
            + (f"<bookmark mark='b'/> Mostly, they're the same letter, in other fonts: {100 * same:.0f} percent of the "
               f"time, against {100 * chance:.0f} by chance. "
               if good else
               f"<bookmark mark='b'/> Often they're the same letter, {100 * same:.0f} percent of the time against "
               f"{100 * chance:.0f} by chance, but just as often only something of a similar shape. ")
            + "Denoising in this space is cheaper, and each step is about shapes, not pixels."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_[0]) for r_ in rows], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(r_[1]), LaggedStart(*[FadeIn(n_, shift=RIGHT * 0.1) for n_ in r_[2]],
                                                                              lag_ratio=0.1)) for r_ in rows], lag_ratio=0.25),
                      FadeIn(key), run_time=2.5)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def diffuse(self):
        d = load("latent")
        S = np.asarray(d["samples"])
        grid = Group(*[gray_image(im, 0.7) for im in S[:24]]).arrange_in_grid(rows=3, cols=8, buff=0.08).move_to(DOWN * 0.3)
        head = label(r"Part 14's flow matching, \ run on the $16$ numbers, \ then decoded", font_size=26, color=GREY_A)
        head.to_edge(UP, buff=0.5)
        foot = label(r"Stable Diffusion, \ Flux, \ and every video model work this way", font_size=26, color=PATCH).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            f"Now run part fourteen's flow matching on those {int(d['Z'])} numbers instead of the pixels, and decode the "
            f"result. <bookmark mark='a'/> Letters again, with {int(d['ratio'])} times fewer numbers to "
            "denoise. That's latent diffusion, and it's how Stable Diffusion, Flux and every video model work."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(i_) for i_ in grid], lag_ratio=0.04), FadeIn(foot), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def vae(self):
        colors = {r"\mu": C.EMBED, r"\sigma": C.EMBED, r"\varepsilon": C.TRUE_P, r"\beta": C.SURPRISE}
        elbo = cmath(r"\log p(x) \;\ge\; \mathbb{E}_{z \sim q(z \mid x)}\big[\log p(x \mid z)\big]", r"\;-\;",
                     r"D_{\mathrm{KL}}\big(q(z \mid x)\,\|\,\mathcal{N}(0, I)\big)", font_size=34).to_edge(UP, buff=0.5)
        el = VGroup(label(r"rebuild well", font_size=22, color=PATCH), label(r"keep the codes near a plain Gaussian", font_size=22,
                                                                            color=C.SURPRISE))
        el[0].next_to(elbo[0], DOWN, buff=0.2)
        el[1].next_to(elbo[2], DOWN, buff=0.2)
        rep = cmath(r"z = ", r"\mu", r"(x) + ", r"\sigma", r"(x) \odot", r"\varepsilon", r", \quad", r"\varepsilon",
                    r"\sim \mathcal{N}(0, I)", colors=colors, font_size=34).move_to([0, 0.6, 0])
        rl = label(r"the encoder gives a cloud, \ not a point; \\ a sample from it is decoded", font_size=22,
                   color=GREY_A).next_to(rep, DOWN, buff=0.15)
        kl = cmath(r"D_{\mathrm{KL}} = \tfrac12 \sum_j \big(", r"\mu", r"_j^2 +", r"\sigma", r"_j^2 - \log", r"\sigma",
                   r"_j^2 - 1\big)", colors=colors, font_size=34).move_to([0, -1.0, 0])
        loss = cmath(r"\mathcal{L} = \|x - \hat x\|^2 \;+\;", r"\beta", r"\, D_{\mathrm{KL}}", colors=colors,
                     font_size=36).move_to([0, -2.4, 0])
        ll = label(r"$\beta$: \ how hard to pull toward the Gaussian", font_size=22, color=C.SURPRISE).next_to(loss, DOWN, buff=0.15)
        # one code cloud, drawn: a point for the plain autoencoder, a blob for the VAE
        cite_ = cite(r"D.~P.~Kingma \& M.~Welling, \textit{Auto-Encoding Variational Bayes} (2013)", corner=DR)
        with self.voiceover(
            "But a plain autoencoder's codes can sit anywhere, in any odd shape, and a generator has to learn that "
            "shape. The variational autoencoder, from Kingma and Welling, shapes the space on purpose. "
            "<bookmark mark='a'/> It maximizes a lower bound on the probability of the data: rebuild each picture "
            "well, while keeping its code close to a plain Gaussian. <bookmark mark='b'/> The encoder gives a small "
            "cloud instead of a point, mean mu and spread sigma, and the decoder must rebuild from any sample in it. "
            "Writing the sample as mu plus sigma times fresh noise lets the gradient flow through. "
            "<bookmark mark='c'/> For Gaussians, the KL term has a closed form. <bookmark mark='d'/> In practice, "
            "its weight, beta, sets the balance."
        ) as vo:
            self.play(FadeIn(cite_), Write(elbo), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(el[0]), Indicate(elbo[0], color=PATCH))
            self.play(FadeIn(el[1]), Indicate(elbo[2], color=C.SURPRISE))
            vo.wait_until("b")
            self.play(Write(rep), FadeIn(rl))
            vo.wait_until("c")
            self.play(Write(kl))
            vo.wait_until("d")
            self.play(Write(loss), FadeIn(ll))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tradeoff(self):
        v = load("vae")
        betas = [float(b) for b in v["betas"]]
        tags = [f"{b:g}" for b in betas]
        rm = {t: float(v[f"rmse_{t}"]) for t in tags}
        kl = {t: float(v[f"kl_{t}"]) for t in tags}
        cl = {t: float(v[f"clear_{t}"]) for t in tags}
        nz = [t for t in tags if t != "0"]
        # left: the rate-distortion picture, one dot per beta (the plain autoencoder as a dashed line)
        kmax = max(kl[t] for t in nz)
        rmax = max(rm.values())
        xt_ = 10 ** math.ceil(math.log10(kmax)) / 4
        ax = CornerAxes(x_range=[0, kmax * 1.1, xt_], y_range=[0, rmax * 1.15, rmax / 2], x_length=5.6, y_length=3.6, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([-3.4, -0.4, 0])
        xn = label(r"KL: \ how much the codes say, \ nats", font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        yn = label(r"rebuild error \ (held-out fonts)", font_size=20, color=GREY_A).next_to(ax, UP, buff=0.12).align_to(ax, LEFT)
        pts = [ax.c2p(kl[t], rm[t]) for t in nz]
        line = VMobject(color=C.SURPRISE, stroke_width=3).set_points_as_corners(pts)
        dots = VGroup(*[Dot(p, radius=0.07, color=C.SURPRISE) for p in pts])
        dl = VGroup(*[MathTex(rf"\beta = {t}", font_size=20, color=C.SURPRISE).next_to(p, UR, buff=0.06) for t, p in zip(nz, pts)])
        ae = DashedLine(ax.c2p(0, rm["0"]), ax.c2p(kmax * 1.1, rm["0"]), dash_length=0.08, stroke_width=2, color=GREY_B)
        ael = label(r"plain autoencoder", font_size=18, color=GREY_B).next_to(ae, UP, buff=0.05).align_to(ae, RIGHT)
        # right: how many generated letters the judge can read, for each beta
        bw, by, H = 0.5, -2.2, 3.0
        bars = VGroup()
        for i, t in enumerate(tags):
            h = H * cl[t]
            b = Rectangle(width=bw, height=max(h, 0.02), stroke_width=0, fill_color=PATCH if t != "0" else GREY_B,
                          fill_opacity=0.85).move_to([2.2 + i * 0.9, by + h / 2, 0])
            bars.add(VGroup(b, MathTex(rf"{100 * cl[t]:.0f}\%", font_size=20, color=WHITE).next_to(b, UP, buff=0.05),
                            MathTex(t, font_size=20, color=GREY_B).next_to(b, DOWN, buff=0.1)))
        bxl = MathTex(r"\beta", font_size=24, color=GREY_B).next_to(bars, DOWN, buff=0.5)
        bh = label(r"generated letters a judge reads \\ with confidence above $0.8$", font_size=20, color=GREY_A)
        bh.next_to(bars, UP, buff=0.35)
        best = max(tags, key=lambda t: cl[t])
        # pictures: rebuilds and samples at three betas
        show = ["0", best, tags[-1]] if best not in ("0", tags[-1]) else ["0", tags[2], tags[-1]]
        cite_ = cite(r"J.~Yao et al., \textit{Reconstruction vs.~Generation} (VA-VAE, 2025)", corner=UR)
        with self.voiceover(
            f"We trained the same small autoencoder with {len(betas)} values of beta, then ran flow matching in each "
            "code space and asked a judge, a classifier trained on the real letters, how many of the generated "
            "letters it can read. <bookmark mark='a'/> As beta grows, the codes carry less, fewer nats, and the "
            f"rebuilds get worse: from {rm[nz[0]]:.3f} to {rm[nz[-1]]:.3f}. <bookmark mark='b'/> But generation "
            + (f"peaks in between: at beta {best}, {100 * cl[best]:.0f} percent of the samples are readable, against "
               f"{100 * cl['0']:.0f} for the plain autoencoder. " if best != "0" else
               f"is best with no KL at all here: {100 * cl['0']:.0f} percent readable. ")
            + "A space that's easy to rebuild from isn't the same as one that's easy to generate in. That trade-off "
            "is one of the live questions in image models: 2025's VA-VAE aligns the codes with a vision model's "
            "features to get both."
        ) as vo:
            self.play(FadeIn(cite_), Create(ax), FadeIn(xn), FadeIn(yn), Create(ae), FadeIn(ael))
            vo.wait_until("a")
            self.play(Create(line), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.2), FadeIn(dl), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(bh), FadeIn(bxl), LaggedStart(*[AnimationGroup(GrowFromEdge(b_[0], DOWN), FadeIn(b_[1]), FadeIn(b_[2]))
                                                             for b_ in bars], lag_ratio=0.15), run_time=2.0)
            self.play(Indicate(bars[tags.index(best)], color=PATCH))
        self.wait(0.3)
        self.clear_scene()
        # the pictures behind the numbers
        rows = Group()
        orig = np.asarray(v["orig"])
        for t in show:
            rec = Group(*[gray_image(im, 0.62) for im in np.asarray(v[f"recon_{t}"])[:6]]).arrange(RIGHT, buff=0.05)
            smp = Group(*[gray_image(im, 0.62) for im in np.asarray(v[f"samples_{t}"])[:8]]).arrange(RIGHT, buff=0.05)
            rows.add(Group(MathTex(rf"\beta = {t}", font_size=26, color=C.SURPRISE), rec, smp).arrange(RIGHT, buff=0.5))
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(DOWN * 0.3)
        o_row = Group(*[gray_image(im, 0.62) for im in orig[:6]]).arrange(RIGHT, buff=0.05).next_to(rows[0][1], UP, buff=0.45)
        h1 = label(r"rebuilt \ (originals above)", font_size=20, color=GREY_A).next_to(o_row, UP, buff=0.1)
        h2 = label(r"generated", font_size=20, color=GREY_A).next_to(rows[0][2], UP, buff=0.55)
        with self.voiceover(
            "Here are the pictures behind those numbers: rebuilds on the left, generated letters on the right. "
            "<bookmark mark='a'/> Sharp rebuilds with muddled samples, blurry rebuilds with clean but plain "
            "samples, and in between, the balance."
        ) as vo:
            self.play(FadeIn(o_row), FadeIn(h1), FadeIn(h2))
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def training(self):
        """How a VAE trains: rebuilds of six held-out letters at checkpoints, and the two terms of the loss."""
        v = load("vae")
        tag = "0.01" if "curve_0.01" in v else [f"{float(b):g}" for b in v["betas"]][2]
        cv = np.asarray(v[f"curve_{tag}"])
        steps = [int(s_) for s_ in v[f"snap_steps_{tag}"]]
        snaps = np.asarray(v[f"snaps_{tag}"])
        orig = np.asarray(v["orig"])[:6]
        S = 0.62
        cols = Group(*[Group(*[gray_image(im, S) for im in snaps[k]]).arrange(DOWN, buff=0.05) for k in range(len(steps))])
        ocol = Group(*[gray_image(im, S) for im in orig]).arrange(DOWN, buff=0.05)
        Group(ocol, cols).arrange(RIGHT, buff=0.35).move_to([-2.6, 0.2, 0])
        cols.shift(RIGHT * 0.25)
        ol = label(r"the letters", font_size=18, color=GREY_A).next_to(ocol, UP, buff=0.12)
        sl = VGroup(*[MathTex(f"{s_:,}".replace(",", "{,}"), font_size=20, color=PATCH).next_to(c_, UP, buff=0.12)
                      for s_, c_ in zip(steps, cols)])
        hl = label(r"rebuilt after this many steps \ (held-out fonts)", font_size=20, color=GREY_A).next_to(sl, UP, buff=0.15)
        # the two terms of the loss as it trains
        total = float(cv[-1, 0])
        rmax, kmax = float(cv[:, 1].max()), float(cv[:, 2].max())
        ax = CornerAxes(x_range=[0, total, total / 2], y_range=[0, 1.05, 0.5], x_length=3.6, y_length=3.0, tips=False,
                        axis_config={"stroke_color": GREY_C, "include_ticks": False}).move_to([4.6, 0.0, 0])
        rc = VMobject(color=PATCH, stroke_width=3).set_points_as_corners([ax.c2p(a, b / rmax) for a, b, _ in cv])
        kc = VMobject(color=C.SURPRISE, stroke_width=3).set_points_as_corners([ax.c2p(a, c / kmax) for a, _, c in cv])
        kl = VGroup(label(r"rebuild error", font_size=18, color=PATCH), label(r"KL: \ what the codes say", font_size=18, color=C.SURPRISE))
        kl.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(ax, UP, buff=0.15)
        xn = label(r"training steps \ (each scaled to its peak)", font_size=18, color=GREY_A).next_to(ax, DOWN, buff=0.12)
        k_peak_at = float(cv[int(np.argmax(cv[:, 2])), 0])
        with self.voiceover(
            f"And here is one of them learning, the one with beta {tag}. <bookmark mark='a'/> These six letters are "
            "from fonts it never trains on, rebuilt from their codes at checkpoints. At first, every letter "
            "comes out as the same grey smudge: the average letter. <bookmark mark='b'/> Then the broad shape of "
            "each one appears, and the details last. <bookmark mark='c'/> The two terms of the loss pull against "
            "each other. The rebuild error falls fast; the KL, how much information the codes carry, "
            + (f"climbs as the encoder learns to say more, peaking around step {k_peak_at:,.0f}, then settles as the "
               "penalty trims what isn't worth its cost." if k_peak_at < 0.8 * total else
               "climbs all the way, as the encoder learns to say more about each letter.")
        ) as vo:
            self.play(FadeIn(ocol), FadeIn(ol), FadeIn(hl))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]), FadeIn(sl[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(c_, shift=RIGHT * 0.1), FadeIn(s_)) for c_, s_ in zip(cols[1:], sl[1:])],
                                  lag_ratio=0.5), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(ax), FadeIn(kl), FadeIn(xn))
            self.play(Create(rc), Create(kc), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()
