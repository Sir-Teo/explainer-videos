from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (crossfade, DATA, DISC, GAN_C, HIST, LATENT, PART, VAE_C, digit_sheet, load, node_box)


class Scale(VoiceoverScene):
    def construct(self):
        self.card()
        self.ours()
        self.road()
        self.style()
        self.truncation()
        self.inversion()

    def card(self):
        card = chapter_card(8, r"GANs at scale: \ BigGAN, StyleGAN, inversion", r"How did GANs get good, and what "
                            r"can you do with one?", lit=(2014,), part=PART)
        with self.voiceover("Chapter eight. GANs at scale: BigGAN, StyleGAN, and inversion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def ours(self):
        g = load("gan")
        L = np.asarray(g["s0_losses"])  # step, D loss, G loss
        snaps = np.asarray(g["s0_snaps"])
        marks = list(g["s0_marks"])
        steps = int(g["s0_steps"])
        k = max(1, len(L) // 40)
        sm = lambda v: np.convolve(v, np.ones(k) / k, mode="valid")
        xs = L[k - 1:, 0]
        top = float(math.ceil(max(sm(L[:, 1]).max(), sm(L[:, 2]).max()) + 0.5))
        ax = axes([0, steps], [0, top], x_length=5.6, y_length=3.2, xlabel=r"generator step",
                  ylabel=r"loss (running mean)", xticks=[0, steps], yticks=[0, round(2 * math.log(2), 2), top],
                  xfmt=lambda v: f"{int(v):,}".replace(",", "{,}"), center=[-3.3, -0.6, 0])
        dl, gl = curve(ax.ax, xs, sm(L[:, 1]), DISC, 2.5), curve(ax.ax, xs, sm(L[:, 2]), GAN_C, 2.5)
        eq = DashedLine(ax.ax.c2p(0, 2 * math.log(2)), ax.ax.c2p(steps, 2 * math.log(2)), color=GREY_C,
                        stroke_width=1.5)
        eql = label(r"$2 \log 2$: \ $D = \tfrac12$ everywhere", font_size=18, color=GREY_B).next_to(eq, UP, buff=0.05)
        eql.align_to(eq, RIGHT)
        lg = legend([(DISC, r"discriminator"), (GAN_C, r"generator")], font_size=20).next_to(ax, UP, buff=0.12)
        lg.align_to(ax, LEFT)
        sheets = [digit_sheet(s_, 4, 4, size=0.55, gap=0.05).move_to([3.5, 0.3, 0]) for s_ in snaps]
        cap = [label(rf"generator step ${m:,}$".replace(",", "{,}"), font_size=22, color=GAN_C)
               .next_to(sheets[0], DOWN, buff=0.2) for m in marks]
        head = label(r"our digit GAN, \ seed $0$: \ the same $16$ noise vectors at every checkpoint", font_size=22,
                     color=GREY_A).to_edge(UP, buff=0.35)
        dfin = float(sm(L[:, 1])[-1])
        bal = ("The discriminator's loss settles close to two log two, the value when it can do no better than a "
               "coin toss." if abs(dfin - 2 * math.log(2)) < 0.25 else
               f"The discriminator's loss ends at {dfin:.2f}, below two log two: it still tells most fakes from real "
               "digits.")
        with self.voiceover(
            "First, ours: two-layer networks on the digits, and what the generator draws from sixteen fixed noise "
            "vectors. <bookmark mark='a'/> Blobs, then strokes, then digits. <bookmark mark='b'/> The two losses "
            f"don't fall like a learning curve; they balance. {bal} Nothing here says when the generator is good, "
            "one reason GANs needed chapter fourteen's measuring sticks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sheets[0]), FadeIn(cap[0]))
            vo.wait_until("a")
            cur, cc = sheets[0], cap[0]
            per = max(0.4, vo.until("b") / max(1, len(sheets) - 1))
            for i in range(1, len(sheets)):
                self.play(crossfade(cur, sheets[i]), ReplacementTransform(cc, cap[i]), run_time=0.6 * per)
                cur, cc = sheets[i], cap[i]
                self.wait(0.4 * per)
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(lg), Create(eq), FadeIn(eql))
            self.play(Create(dl), Create(gl), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def road(self):
        cards = VGroup(
            history_card(2015, r"Radford, Metz \& Chintala: \ DCGAN", r"convolutions, batch norm; \ arithmetic on "
                         r"codes: \ smiling woman $-$ woman $+$ man", width=3.3, font_size=18),
            history_card(2017, r"Karras et al.: \ progressive growing", r"train at $4 \times 4$, \ then add layers, "
                         r"up to $1024 \times 1024$ faces", width=3.3, font_size=18),
            history_card(2018, r"Brock, Donahue \& Simonyan: \ BigGAN", r"ImageNet at $128^2$: \ IS $166.5$, \ FID "
                         r"$7.4$ \ (previous best $52.5$, \ $18.6$)", width=3.3, font_size=18),
            history_card(2018, r"Karras, Laine \& Aila: \ StyleGAN", r"a mapping network and per-layer styles", width=3.3,
                         font_size=18),
        ).arrange(RIGHT, buff=0.18).move_to(UP * 0.4)
        if cards.width > 13.6:
            cards.width = 13.6
        more = label(r"and: \ spectral normalization (Miyato et al., 2018), \ self-attention (Zhang et al., 2018), "
                     r"\ R1 (Mescheder et al., 2018)", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "From there to photographs took four years. <bookmark mark='a'/> In 2015 Alec Radford, Luke Metz and "
            "Soumith Chintala found convolutional GANs that trained reliably, whose noise vectors did arithmetic: a "
            "smiling woman, minus a woman, plus a man, gave a smiling man. <bookmark mark='b'/> In 2017 Tero Karras "
            "and colleagues at NVIDIA grew the networks during training, up to 1024 pixels. <bookmark mark='c'/> In "
            "2018 Andrew Brock, Jeff Donahue and Karen Simonyan scaled a GAN to ImageNet: an Inception score of "
            "166.5 and an FID of 7.4 at 128 pixels, against a previous best of 52.5 and 18.6. <bookmark mark='d'/> "
            "And Karras's group rebuilt the generator itself: StyleGAN."
        ) as vo:
            vo.wait_until("a")
            for k, mk in enumerate([None, "b", "c", "d"]):
                if mk:
                    vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.15))
            self.play(FadeIn(more))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def style(self):
        z = node_box(r"$z$", LATENT, font_size=30).move_to([-6.0, 1.6, 0])
        mp = node_box(r"mapping: \ $8$ layers", LATENT, font_size=22, height=0.9).move_to([-3.9, 1.6, 0])
        w = node_box(r"$w$", LATENT, font_size=30).move_to([-1.9, 1.6, 0])
        const = node_box(r"a learned constant, $4 \times 4$", GREY_B, font_size=20).move_to([1.7, 2.6, 0])
        blocks = VGroup(*[node_box(rf"${r} \times {r}$", GAN_C, font_size=22, width=2.0) for r in (4, 8, 16, "\\dots",
                                                                                                    1024)])
        for i, b in enumerate(blocks):
            b.move_to([1.7, 1.5 - 0.95 * i, 0])
        styles = VGroup(*[Arrow(w.get_right(), b.get_left(), buff=0.12, color=LATENT, stroke_width=2,
                                max_tip_length_to_length_ratio=0.06) for b in blocks])
        sl = label(r"a style per layer: \ scale and shift each channel", font_size=20, color=LATENT)
        sl.move_to([-2.0, -1.5, 0])
        noise = VGroup(*[label(r"$+$ noise", font_size=18, color=GREY_B).next_to(b, RIGHT, buff=0.15) for b in blocks])
        chain = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.04, color=GAN_C, stroke_width=2,
                               max_tip_length_to_length_ratio=0.25) for a, b in zip(blocks, blocks[1:])])
        c0 = Arrow(const.get_bottom(), blocks[0].get_top(), buff=0.04, color=GREY_B, stroke_width=2)
        A = lambda a, b: Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2.5)
        mix = VGroup(label(r"style mixing:", font_size=22, color=C.BITS),
                     label(r"coarse layers' styles from one $w$: \ pose, face shape", font_size=20),
                     label(r"fine layers' from another: \ colour, texture", font_size=20))
        mix.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([5.0, -0.4, 0])
        tg = note(r"schematic").to_corner(UR, buff=0.25)
        cite_ = cite(r"Karras, Laine \& Aila (2019); \ StyleGAN2 (2020), StyleGAN3 (2021)", corner=DR)
        with self.voiceover(
            "StyleGAN's generator starts not from the noise but from a learned four-pixel constant, upsampled block "
            "by block. <bookmark mark='a'/> The noise goes through an eight-layer mapping network to a code w, "
            "<bookmark mark='b'/> and w sets each block's style, a scale and shift per channel; fresh noise adds "
            "details like freckles. <bookmark mark='c'/> Styles can be mixed, coarse layers from one face, fine ones "
            "from another, and straight lines in w's space became meaningful edits."
        ) as vo:
            self.play(FadeIn(const), FadeIn(blocks[0]), Create(c0), FadeIn(tg), FadeIn(cite_))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(c), FadeIn(b)) for c, b in zip(chain, blocks[1:])],
                                  lag_ratio=0.3), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(z), GrowArrow(A(z, mp)), FadeIn(mp), GrowArrow(A(mp, w)), FadeIn(w))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(s_) for s_ in styles], lag_ratio=0.15), FadeIn(sl),
                      LaggedStart(*[FadeIn(n_) for n_ in noise], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(mix, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def truncation(self):
        e = load("evaluate")
        tr = [r for r in e["trunc"] if r["t"]]
        full = [r for r in e["trunc"] if not r["t"]][0]
        ts = [r["t"] for r in tr]
        g = axes([0, 2.1], [0, 1], x_length=5.4, y_length=3.4, xlabel=r"truncation $t$: \ resample $|z_i| > t$",
                 ylabel=r"precision, \ recall", xticks=[0.5, 1, 1.5, 2], yticks=[0, 0.5, 1], center=[-3.2, -0.4, 0])
        P = [r["precision"] for r in tr]
        R = [r["recall"] for r in tr]
        pc, rc = curve(g.ax, ts, P, C.INTERVAL, 3), curve(g.ax, ts, R, C.SURPRISE, 3)
        pd = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.06, color=C.INTERVAL) for a, b in zip(ts, P)])
        rd = VGroup(*[Dot(g.ax.c2p(a, b), radius=0.06, color=C.SURPRISE) for a, b in zip(ts, R)])
        lg = legend([(C.INTERVAL, r"precision: \ samples that look real"),
                     (C.SURPRISE, r"recall: \ real digits the samples cover")], font_size=20).next_to(g, UP, buff=0.12)
        lg.align_to(g, LEFT)
        rows = Group()
        for r in (tr[0], tr[2], full):
            nm = MathTex(rf"t = {r['t']:g}" if r["t"] else r"t = \infty", font_size=24, color=GAN_C)
            rows.add(Group(nm, digit_sheet(np.asarray(r["show"]), 1, 8, size=0.42, gap=0.04)).arrange(RIGHT,
                                                                                                    buff=0.25))
        rows.arrange(DOWN, buff=0.25, aligned_edge=RIGHT).move_to([3.6, 0.2, 0])
        t0, t1 = tr[0], full
        tt, p0, r0, p1, r1 = t0["t"], t0["precision"], t0["recall"], t1["precision"], t1["recall"]
        if t0["precision"] > t1["precision"] and t0["recall"] < t1["recall"]:
            verdict = (f"at t of {tt:g}, precision {p0:.2f} and recall {r0:.2f}; untruncated, {p1:.2f} and "
                       f"{r1:.2f}. Fidelity bought with variety.")
        else:
            verdict = (f"at t of {tt:g}, precision {p0:.2f} and recall {r0:.2f}; untruncated, {p1:.2f} and "
                       f"{r1:.2f}: a weaker trade than BigGAN's.")
        best = min(e["trunc"], key=lambda r: r["fid"])
        bt = best["t"]
        fid_s = (f"The FID, which mixes both, is best at t of {bt:g}." if bt else
                 "The FID, which mixes both, is best with no truncation at all.")
        with self.voiceover(
            "BigGAN's truncation trick: at sampling time, resample any noise coordinate larger than t, keeping the "
            "generator near the middle of what it learned. <bookmark mark='a'/> On our GAN, with chapter "
            "fourteen's precision and recall: <bookmark mark='b'/> " + verdict + " <bookmark mark='c'/> " + fid_s
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), FadeIn(rows))
            vo.wait_until("a")
            self.play(Create(pc), FadeIn(pd), Create(rc), FadeIn(rd), run_time=2.0)
            vo.wait_until("b")
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def inversion(self):
        e = load("evaluate")
        tgt = np.asarray(e["inv_targets"])
        frames = np.asarray(e["inv_frames"])
        steps = list(e["inv_steps"])
        top = digit_sheet(tgt, 1, 8, size=0.55, gap=0.05).move_to([0.4, 2.4, 0])
        tl = label(r"real test digits", font_size=22, color=DATA).next_to(top, LEFT, buff=0.3)
        rec = [digit_sheet(f, 1, 8, size=0.55, gap=0.05).next_to(top, DOWN, buff=0.25) for f in frames]
        rl = [label(rf"$G(z)$ after ${s}$ steps", font_size=22, color=GAN_C).next_to(rec[0], LEFT, buff=0.3)
              for s in steps]
        vr = digit_sheet(np.asarray(e["vae_recon"]), 1, 8, size=0.55, gap=0.05).next_to(rec[0], DOWN, buff=0.25)
        vl = label(r"the VAE's encoder, \ one pass", font_size=22, color=VAE_C).next_to(vr, LEFT, buff=0.3)
        it = digit_sheet(np.asarray(e["interp"]), 1, 9, size=0.55, gap=0.05).to_edge(DOWN, buff=0.6).shift(RIGHT * 0.4)
        il = label(r"a straight line in $z$ between the first two", font_size=22, color=GAN_C).next_to(it, UP,
                                                                                                     buff=0.12)
        ge, ve = float(np.mean(e["inv_err"])), float(np.mean(e["vae_err"]))
        n_st = int(steps[-1])
        f = cmath(r"z^* = \arg\min_z \, \|G(z) - x\|^2", font_size=30).to_corner(UR, buff=0.35)
        cmp_ = (f"Their average squared error per pixel is {ge:.3f}, against {ve:.3f} for the VAE's encoder, "
                f"which gets its answer in one pass but is a different model." if ge < ve else
                f"Their average squared error per pixel is {ge:.3f}, against {ve:.3f} for the VAE's encoder in one "
                "pass: the GAN's range doesn't quite contain these digits.")
        cite_ = cite(r"Zhu et al., \textit{iGAN} (2016); \ Abdal, Qin \& Wonka (2019); \ Pan et al., "
                     r"\textit{DragGAN} (2023)", corner=DL)
        with self.voiceover(
            "A GAN has no encoder: to edit a real photograph, first find the noise that would produce it, by "
            "gradient descent on the difference between G of z and the image. That's GAN inversion. <bookmark "
            f"mark='a'/> Eight unseen test digits, four random starts each, the best kept, {n_st} steps. <bookmark "
            f"mark='b'/> {cmp_} <bookmark mark='c'/> A line between two found codes morphs one digit into the "
            "other; in StyleGAN's w space this became photo editing, from iGAN in 2016 to DragGAN in 2023."
        ) as vo:
            self.play(FadeIn(top), FadeIn(tl), Write(f), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(rec[0]), FadeIn(rl[0]))
            cur, cl = rec[0], rl[0]
            for k in range(1, len(rec)):
                self.play(crossfade(cur, rec[k]), ReplacementTransform(cl, rl[k]), run_time=0.6)
                cur, cl = rec[k], rl[k]
            vo.wait_until("b")
            self.play(FadeIn(vr), FadeIn(vl))
            vo.wait_until("c")
            self.play(FadeIn(it), FadeIn(il))
        self.wait(0.3)
        self.clear_scene()
