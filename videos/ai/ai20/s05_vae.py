from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (AR, DATA, KLC, LATENT, PART, RECON, VAE_C, Plane, band, curve, digit_sheet, load,
                                   rgb_of)

DIGIT_COLORS = ["#FF6B8B", "#FFB070", "#F7D154", "#9BE37B", "#5CD0B3", "#58A6FF", "#7C9CF0", "#B39DDB", "#E3A8F0",
                "#BBBBBB"]


class VAE(VoiceoverScene):
    def construct(self):
        self.card()
        self.replay()
        self.map()
        self.beta()
        self.collapse_plane()
        self.collapse_digits()
        self.blur()

    def card(self):
        card = chapter_card(4, r"Training a VAE: \ rate, distortion, collapse",
                            r"What does the code learn, and when does it learn nothing?", lit=(), part=PART)
        with self.voiceover("Chapter four. Training a VAE: rate, distortion, and collapse."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def replay(self):
        v = load("vae")
        cv = np.asarray(v["s0_curve"])  # step, examples, -elbo, rec, kl (nats per digit)
        ex = cv[:, 1]
        top = float(np.ceil(cv[:, 3].max() / 100) * 100)
        g = axes([0, ex[-1]], [0, top], x_length=5.6, y_length=3.4, xlabel=r"training digits seen",
                 ylabel=r"nats per digit \ (held-out)", xticks=[0, ex[-1]], yticks=[0, top],
                 xfmt=lambda v_: f"{v_ / 1e6:.1f}" + (r"\text{M}" if v_ else ""), center=[-3.2, -0.4, 0])
        rec = curve(g.ax, ex, cv[:, 3], RECON, 3)
        kl = curve(g.ax, ex, cv[:, 4], KLC, 3)
        lg = legend([(RECON, r"reconstruction: \ $-\mathbb E_q \log p(x \mid z)$"), (KLC, r"rate: \ "
                     r"$\mathrm{KL}(q \,\|\, p(z))$")], font_size=20).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        snaps = np.asarray(v["s0_snaps"])
        recs = np.asarray(v["s0_snap_recs"])
        src = np.asarray(v["s0_recon_src"])
        srow = digit_sheet(src, 1, 8, size=0.42, gap=0.04).move_to([3.4, 2.2, 0])
        srl = label(r"held-out digits", font_size=20, color=GREY_A).next_to(srow, UP, buff=0.08)
        rrows = [digit_sheet(r_, 1, 8, size=0.42, gap=0.04).next_to(srow, DOWN, buff=0.12) for r_ in recs]
        rrl = label(r"their reconstructions", font_size=20, color=RECON).next_to(rrows[0], DOWN, buff=0.06)
        sheets = [digit_sheet(s_, 2, 8, size=0.42, gap=0.04).move_to([3.4, -1.3, 0]) for s_ in snaps]
        shl = label(r"samples: \ $z \sim \mathcal N(0, I)$, \ the same $z$ each time", font_size=20,
                    color=VAE_C).next_to(sheets[0], UP, buff=0.08)
        r0, k0, r1, k1 = cv[0, 3], cv[0, 4], cv[-1, 3], cv[-1, 4]
        e_b = [float(v[f"s{s}_elbo_bpp"]) for s in (0, 1, 2)]
        iw = [float(v[f"s{s}_iwae_bpp"]) for s in (0, 1, 2)]
        act = int(v["s0_active"])
        tg = note(r"computed: \ seed $0$ replayed, \ three seeds measured").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Here is our VAE learning. The two terms of the bound, in nats per digit on held-out digits: "
            "reconstruction, and rate. <bookmark mark='a'/> At the start the decoder knows nothing, and "
            f"reconstruction costs {r0:.0f} nats per digit, while the rate is {k0:.1f}: the codes say nothing yet. "
            "<bookmark mark='b'/> Then the encoder starts to say something, the rate climbs, and the "
            "reconstructions sharpen: the model buys accuracy with information. <bookmark mark='c'/> By the end the "
            f"code carries {k1:.1f} nats about each digit, and the decoder needs {r1:.0f} nats to describe the rest. "
            f"In bits per pixel the bound is {e_b[0]:.2f}; a tighter estimate, averaging 64 codes per digit, gives "
            f"{iw[0]:.2f}. <bookmark mark='d'/> The samples, drawn from plain noise through the decoder, are "
            "digits, softly blurred. And only "
            f"{act} of the sixteen code numbers end up carrying information; the rest are switched off, a first "
            "hint of what comes later in this chapter."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), FadeIn(srow), FadeIn(srl), FadeIn(rrows[0]), FadeIn(rrl),
                      FadeIn(sheets[0]), FadeIn(shl), FadeIn(tg))
            vo.wait_until("a")
            dot_r, dot_k = Dot(g.ax.c2p(ex[0], cv[0, 3]), color=RECON), Dot(g.ax.c2p(ex[0], cv[0, 4]), color=KLC)
            self.play(FadeIn(dot_r), FadeIn(dot_k))
            vo.wait_until("b")
            cur_r, cur_s = rrows[0], sheets[0]
            per = max(0.4, vo.until("c") / max(1, len(snaps) - 1))
            for k in range(1, len(snaps)):
                self.play(dot_r.animate.move_to(g.ax.c2p(ex[k], cv[k, 3])),
                          dot_k.animate.move_to(g.ax.c2p(ex[k], cv[k, 4])), FadeTransform(cur_r, rrows[k]),
                          FadeTransform(cur_s, sheets[k]), run_time=0.6 * per)
                cur_r, cur_s = rrows[k], sheets[k]
                self.wait(0.4 * per)
            self.play(Create(rec), Create(kl), run_time=1.0)
            vo.wait_until("d")
            self.play(Indicate(cur_s, scale_factor=1.03))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def map(self):
        vm = load("vae_map")
        codes = np.asarray(vm["codes"])
        labs = np.asarray(vm["labels"])
        n = 700
        lim = 3.2
        pl = Plane(4.6, center=[-3.4, -0.2, 0], box=lim)
        clip = lambda P: np.clip(P, -lim * 0.97, lim * 0.97)
        dots = VGroup(*[Dot(q, radius=0.03, color=DIGIT_COLORS[labs[i]]) for i, q in
                        enumerate(pl.pts(clip(codes[0][:n])))])
        key = VGroup(*[VGroup(Dot(radius=0.06, color=DIGIT_COLORS[k]), label(str(k), font_size=20))
                       .arrange(RIGHT, buff=0.08) for k in range(10)]).arrange(RIGHT, buff=0.22)
        key.next_to(pl, UP, buff=0.15)
        grid = np.asarray(vm["grid"]).reshape(-1, 14, 14)
        sheet = digit_sheet(grid, 15, 15, size=0.27, gap=0.015).move_to([3.4, -0.2, 0])
        gl = label(r"decoding an even grid of codes", font_size=22, color=VAE_C).next_to(sheet, UP, buff=0.15)
        steps = list(vm["steps"])
        cnt = label(r"step $0$", font_size=22, color=GREY_A).next_to(pl, DOWN, buff=0.15)
        with self.voiceover(
            "What does the code learn? Give the VAE only two numbers per digit, and we can watch. Each dot is a "
            "held-out digit, placed at the mean of its code and coloured by which digit it is. <bookmark "
            "mark='a'/> At first every digit sits at the origin. As training goes on, the encoder spreads them "
            "out, and digits of the same kind gather together, though nobody told it the labels. The KL term keeps "
            "the whole cloud packed around the origin, roughly Gaussian. <bookmark mark='b'/> Decode an even grid "
            "of codes and you get the map of the model's digits: ones in one region, zeros in another, and "
            "smooth blends in between, a seven turning into a nine."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(dots), FadeIn(key), FadeIn(cnt))
            vo.wait_until("a")
            per = max(0.5, (vo.until("b") - 0.5) / max(1, len(codes) - 1))
            for k in range(1, len(codes)):
                new = label(rf"step ${steps[k]:,}$".replace(",", "{,}"), font_size=22, color=GREY_A).move_to(cnt)
                self.play(*[d.animate.move_to(q) for d, q in zip(dots, pl.pts(clip(codes[k][:n])))],
                          ReplacementTransform(cnt, new), run_time=per)
                cnt = new
            vo.wait_until("b")
            self.play(FadeIn(sheet), FadeIn(gl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def beta(self):
        b = load("beta")
        betas = list(b["betas"])
        R, Dd, A = np.asarray(b["kl_nats"]), np.asarray(b["rec_nats"]), np.asarray(b["active"])
        f = cmath(r"\mathcal L_\beta", r"=", r"\mathbb E_q[-\log p(x \mid z)]", r"+", r"\beta", r"\,",
                  r"\mathrm{KL}(q \,\|\, p)", font_size=36).to_edge(UP, buff=0.35)
        f[2].set_color(RECON)
        f[4].set_color(C.BITS)
        f[6].set_color(KLC)
        rmax = float(np.ceil(R.max() / 10) * 10 + 5)
        dlo, dhi = float(np.floor(Dd.min() / 20) * 20), float(np.ceil(Dd.max() / 20) * 20)
        g = axes([0, rmax], [dlo, dhi], x_length=5.2, y_length=3.6, xlabel=r"rate: \ KL (nats)",
                 ylabel=r"distortion: \ reconstruction (nats)", xticks=[0, rmax], yticks=[dlo, dhi],
                 center=[-3.4, -0.6, 0])
        pts = VGroup()
        labs = VGroup()
        for i, bb in enumerate(betas):
            for s in range(R.shape[1]):
                pts.add(Dot(g.ax.c2p(R[i, s], Dd[i, s]), radius=0.06, color=C.BITS).set_opacity(0.9))
            labs.add(MathTex(rf"\beta = {bb:g}", font_size=20, color=C.BITS).next_to(
                g.ax.c2p(R[i].mean(), Dd[i].mean()), UR, buff=0.06))
        path = curve(g.ax, R.mean(1), Dd.mean(1), C.BITS, 2)
        rows = Group()
        for i, bb in enumerate(betas):
            sh = digit_sheet(np.asarray(b["show"])[i][:8], 1, 8, size=0.36, gap=0.03)
            tl = MathTex(rf"\beta = {bb:g}", font_size=22, color=C.BITS)
            al = label(rf"${int(round(A[i].mean()))}$ active", font_size=18, color=GREY_B)
            rows.add(Group(tl, sh, al).arrange(RIGHT, buff=0.18))
        rows.arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([3.5, -0.5, 0])
        mono_r = all(R[i].mean() >= R[i + 1].mean() for i in range(len(betas) - 1))
        mono_d = all(Dd[i].mean() <= Dd[i + 1].mean() for i in range(len(betas) - 1))
        lo, hi = 0, len(betas) - 1
        trend = ("Every step up in beta lowers the rate and raises the distortion: the runs trace one curve, the "
                 "rate-distortion trade-off of information theory." if mono_r and mono_d else
                 "Overall, raising beta lowers the rate and raises the distortion, though not at every step: the "
                 "runs scatter around one curve, the rate-distortion trade-off of information theory.")
        cite_ = cite(r"Higgins et al., \textit{$\beta$-VAE} (2017); \ Alemi et al., \textit{Fixing a Broken ELBO} "
                     r"(2018)", corner=DR)
        with self.voiceover(
            "The two terms pull against each other, and one number sets the exchange rate. Weight the KL by beta: "
            "Irina Higgins and colleagues at DeepMind called it the beta-VAE. <bookmark mark='a'/> We trained it "
            f"at six values of beta, from {betas[lo]:g} to {betas[hi]:g}, two seeds each, on a quarter of the "
            "budget. Each dot is a run: how many nats the code carries, against how many the decoder still needs. "
            f"<bookmark mark='b'/> {trend} At beta {betas[lo]:g} the code carries {R[lo].mean():.0f} nats and "
            f"{int(round(A[lo].mean()))} code numbers are active; at beta {betas[hi]:g}, {R[hi].mean():.0f} nats "
            f"and {int(round(A[hi].mean()))}. <bookmark mark='c'/> The samples show the trade: a large beta gives "
            "smooth, generic digits, because the code no longer says enough to pin down the details. Higgins "
            "found that a large beta also pushes each code number to control one factor of the image, such as an "
            "object's position or a face's angle."
        ) as vo:
            self.play(Write(f), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(g), LaggedStart(*[FadeIn(p_, scale=1.5) for p_ in pts], lag_ratio=0.1), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(path), FadeIn(labs))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_, shift=LEFT * 0.1) for r_ in rows], lag_ratio=0.2), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def collapse_plane(self):
        c = load("collapse2d")
        S = np.asarray(c["fact_s0_curve"])[:, 0]
        F = np.array([np.asarray(c[f"fact_s{s}_curve"])[:, 3] for s in range(3)])
        Aa = np.array([np.asarray(c[f"ar_s{s}_curve"])[:, 3] for s in range(3)])
        top = float(np.ceil(max(F.max(), Aa.max()) * 2) / 2 + 0.5)
        g = axes([0, S[-1]], [0, top], x_length=5.4, y_length=3.4, xlabel=r"training step",
                 ylabel=r"rate: \ KL per point (nats)", xticks=[0, S[-1]], yticks=[0, top],
                 center=[-3.3, -0.5, 0])
        bf = band(g.ax, S, F.min(0), F.max(0), VAE_C, 0.25)
        ba = band(g.ax, S, Aa.min(0), Aa.max(0), AR, 0.25)
        lf, la = curve(g.ax, S, F.mean(0), VAE_C, 3), curve(g.ax, S, Aa.mean(0), AR, 3)
        lg = legend([(VAE_C, r"decoder: \ $p(x_1 \mid z)\, p(x_2 \mid z)$"),
                     (AR, r"decoder: \ $p(x_1 \mid z)\, p(x_2 \mid x_1, z)$")], font_size=20)
        lg.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        pf, pa = Plane(2.4, center=[2.4, -1.0, 0]), Plane(2.4, center=[5.2, -1.0, 0])
        cf, ca = np.asarray(c["fact_codes"]), np.asarray(c["ar_codes"])
        df, da = pf.dots(np.clip(cf, -2.9, 2.9), VAE_C, radius=0.02), pa.dots(np.clip(ca, -2.9, 2.9), AR, radius=0.02)
        tl = label(r"where held-out points land in the code", font_size=20, color=GREY_A).next_to(VGroup(pf, pa), UP,
                                                                                                 buff=0.12)
        fk, ak = float(F[:, -1].mean()), float(Aa[:, -1].mean())
        collapsed = ak < 0.1 * max(fk, 1e-9)
        verdict = (f"The autoregressive decoder's rate falls to {ak:.3f} nats, in every seed: the code has "
                   "collapsed. Every point is encoded as the same blob at the origin, and the decoder models the "
                   "moons alone." if collapsed else
                   f"The autoregressive decoder's rate falls to {ak:.2f} nats, against {fk:.2f}: the code is nearly "
                   "unused.")
        with self.voiceover(
            "Those switched-off code numbers have a name: posterior collapse, and we can make it happen on purpose. "
            "Take the two moons and a VAE with a two-number code. Give one version a decoder that predicts x one "
            "and x two separately, each from the code. <bookmark mark='a'/> To get the moons' shape, where x two "
            "depends on x one, it has to use the code, and it does: "
            f"its rate settles at {fk:.2f} nats per point, in all three seeds. <bookmark mark='b'/> Now give the "
            "decoder the power of chapter two: x two is predicted from the code and from x one. <bookmark "
            f"mark='c'/> {verdict}"
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg[0]))
            vo.wait_until("a")
            self.play(FadeIn(bf), Create(lf), FadeIn(pf), FadeIn(df), FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(lg[1]))
            vo.wait_until("c")
            self.play(FadeIn(ba), Create(la), FadeIn(pa), FadeIn(da))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def collapse_digits(self):
        c, v = load("collapse"), load("vae")
        Pc, Fc = np.asarray(c["plain_curve"]), np.asarray(c["free_curve"])  # step, examples, rec, kl
        top = float(np.ceil(max(Pc[:, 3].max(), Fc[:, 3].max(), float(v["s0_kl_nats"])) / 5) * 5 + 5)
        g = axes([0, Pc[-1, 1]], [0, top], x_length=5.4, y_length=3.4, xlabel=r"training digits seen",
                 ylabel=r"rate: \ KL per digit (nats)", xticks=[0, Pc[-1, 1]], yticks=[0, top],
                 xfmt=lambda v_: f"{v_ / 1000:.0f}" + (r"\text{k}" if v_ else ""), center=[-3.3, -0.4, 0])
        lp = curve(g.ax, Pc[:, 1], Pc[:, 3], AR, 3)
        lf = curve(g.ax, Fc[:, 1], Fc[:, 3], C.BITS, 3)
        ref = DashedLine(g.ax.c2p(0, float(v["s0_kl_nats"])), g.ax.c2p(Pc[-1, 1], float(v["s0_kl_nats"])), color=VAE_C,
                         stroke_width=2)
        rl = label(r"the plain VAE's rate", font_size=18, color=VAE_C).next_to(ref, UP, buff=0.05).align_to(ref, RIGHT)
        lg = legend([(AR, r"PixelCNN decoder"), (C.BITS, rf"PixelCNN decoder, \ free bits (${c['free_free_bits']:g}$ "
                                                         r"nats per code number)")], font_size=20)
        lg.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        rows = Group()
        for tag_, col in (("plain", AR), ("free", C.BITS)):
            src = np.asarray(c[f"{tag_}_src"])
            same = np.asarray(c[f"{tag_}_same_z"])
            r_ = Group()
            for i in range(4):
                r_.add(Group(digit_sheet(src[i:i + 1], 1, 1, size=0.42), MathTex(r"\to", font_size=26),
                             digit_sheet(same[4 * i:4 * i + 4], 1, 4, size=0.42, gap=0.03)).arrange(RIGHT, buff=0.12))
            r_.arrange(DOWN, buff=0.1)
            rows.add(Group(label(r"collapsed" if tag_ == "plain" else r"with free bits", font_size=20, color=col),
                           r_).arrange(DOWN, buff=0.1))
        rows.arrange(RIGHT, buff=0.4).move_to([3.6, -0.4, 0])
        cap = label(r"a digit, \ its code, \ four digits decoded from that code", font_size=20,
                    color=GREY_A).next_to(rows, UP, buff=0.15)
        kp, kf = float(Pc[-1, 3]), float(Fc[-1, 3])
        ap, af = float(c["plain_agree"]), float(c["free_agree"])
        kv = float(v["s0_kl_nats"])
        if kp < 0.25 * kv:
            first = (f"With a PixelCNN as its decoder, the VAE's rate climbs briefly, then sinks to {kp:.1f} nats "
                     f"per digit, against {kv:.1f} for the plain VAE. The decoder can draw a digit by itself, so "
                     "the code is mostly ignored.")
        else:
            first = (f"With a PixelCNN as its decoder, the VAE's rate ends at {kp:.1f} nats per digit, against "
                     f"{kv:.1f} for the plain VAE: the strong decoder leans on the code much less.")
        fbits = float(c["free_free_bits"])
        pa, pf = 100 * ap, 100 * af
        second = (f"Decode four digits from one code, and only {pa:.0f} percent are the same digit as the image that "
                  "was encoded." if ap < 0.6 else
                  f"Decode four digits from one code, and {pa:.0f} percent are still the same digit as the image that "
                  "was encoded.")
        third = (f"Free bits, a floor of {fbits:g} nats per code number below which the KL costs nothing, keep "
                 f"{kf:.1f} nats in the code, and {pf:.0f} percent of decoded digits match their source.")
        cite_ = cite(r"Bowman et al.\ (2016); \ Kingma et al., \textit{IAF}, free bits (2016); \ Chen et al., "
                     r"\textit{Variational Lossy Autoencoder} (2017)", corner=DR)
        with self.voiceover(
            "Why would a model give up its code? Because the code costs rate, and with a decoder that can model the "
            "data by itself, nothing pays for it. Samuel Bowman and colleagues hit this in 2016 with a VAE for "
            "sentences: the language-model decoder learned to ignore the code entirely. <bookmark mark='a'/> "
            f"{first} <bookmark mark='b'/> {second} <bookmark mark='c'/> {third} The cure is to make the code worth its cost: a weaker decoder, "
            "a floor on the rate, or a KL weight that is turned up slowly."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), Create(ref), FadeIn(rl), FadeIn(cite_))
            vo.wait_until("a")
            self.play(Create(lp), run_time=2.0)
            self.play(FadeIn(rows[0]), FadeIn(cap))
            vo.wait_until("b")
            self.play(Indicate(rows[0], scale_factor=1.03))
            vo.wait_until("c")
            self.play(Create(lf), FadeIn(rows[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blur(self):
        t, v2, e2 = load("toys"), load("vae2d"), load("eval2d")
        pt, pv = Plane(3.4, center=[-3.4, 0.1, 0]), Plane(3.4, center=[0.6, 0.1, 0])
        it = pt.image(t["ring_density"], DATA)
        iv = pv.scatter_image(np.asarray(v2["ring_s0"]), VAE_C, radius_px=1.5)
        tl = label(r"the ring", font_size=22, color=DATA).next_to(pt, UP, buff=0.12)
        vl = label(r"VAE samples", font_size=22, color=VAE_C).next_to(pv, UP, buff=0.12)
        q = np.mean([r["quality"] for r in e2["rows"]["vae"]])
        ql = label(rf"${100 * q:.0f}\%$ of samples within $3\sigma$ of a mode", font_size=22, color=VAE_C)
        ql.next_to(pv, DOWN, buff=0.15)
        nxt = VGroup(
            label(r"deeper codes: \ hierarchical VAEs (NVAE, 2020)", font_size=22, color=GREY_A),
            label(r"discrete codes: \ VQ-VAE (chapter 16)", font_size=22, color=VQ_COL),
            label(r"the autoencoder in front of \\ latent diffusion (Part 22)", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([5.0, 0.4, 0])
        tk = take_away(r"A VAE learns a code and a decoder with one bound: \ a trade between rate and distortion, "
                       r"\ whose samples blur where the data is sharp.", font_size=24)
        with self.voiceover(
            "One more thing to see. On the ring of eight narrow Gaussians, the VAE spreads its samples into the gaps "
            f"between the modes: averaged over three seeds, only {100 * q:.0f} percent land within three standard "
            "deviations of one. <bookmark mark='a'/> A Gaussian decoder plus a smooth code blurs whatever is "
            "sharp; on images, that's the VAE's famous softness. <bookmark mark='b'/> The fixes became whole "
            "lines of work: deeper hierarchies of codes, discrete codes that we'll meet at the end of this part, "
            "and the autoencoder that sits in front of every latent diffusion model."
        ) as vo:
            self.play(FadeIn(pt), FadeIn(it), FadeIn(tl), FadeIn(pv), FadeIn(iv), FadeIn(vl))
            self.play(FadeIn(ql))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(n_, shift=UP * 0.1) for n_ in nxt], lag_ratio=0.3), FadeIn(tk))
        self.wait(0.3)
        self.clear_scene()


VQ_COL = "#D4A5FF"
