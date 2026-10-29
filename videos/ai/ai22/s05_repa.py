from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import CFG_C, HIST, PART, PATCH, fmt_int, gray_image, load, mean_band, take_away

REPA_C, BASE_C = CFG_C["repa"], CFG_C["zero"]


def repa_picture() -> VGroup:
    """REPA: the denoiser's tokens after an early block, through a small projector, compared (cosine) with a frozen
    vision encoder's tokens of the clean picture."""
    blocks = VGroup(*[RoundedRectangle(width=2.6, height=0.42, corner_radius=0.08, stroke_color=GREY_B, stroke_width=2)
                      for _ in range(4)]).arrange(UP, buff=0.14)
    bl = VGroup(*[label(rf"block {k + 1}", font_size=16, color=GREY_A).move_to(b) for k, b in enumerate(blocks)])
    noisy = label(r"noisy patches", font_size=18, color=PATCH).next_to(blocks, DOWN, buff=0.2)
    out = label(r"velocity", font_size=18, color=GREY_A).next_to(blocks, UP, buff=0.2)
    proj = node_box_(r"projector", REPA_C).next_to(blocks[1], RIGHT, buff=0.7)
    a1 = Arrow(blocks[1].get_right(), proj.get_left(), buff=0.06, color=REPA_C, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
    enc = node_box_(r"frozen encoder", C.TRUE_P).next_to(proj, RIGHT, buff=1.5)
    clean = label(r"the clean picture", font_size=18, color=C.TRUE_P).next_to(enc, DOWN, buff=0.35)
    a2 = Arrow(clean.get_top(), enc.get_bottom(), buff=0.06, color=C.TRUE_P, stroke_width=2.5, max_tip_length_to_length_ratio=0.2)
    cos = MathTex(r"\cos", font_size=30, color=REPA_C).move_to((proj.get_right() + enc.get_left()) / 2 + UP * 0.45)
    link = DoubleArrow(proj.get_right(), enc.get_left(), buff=0.08, color=REPA_C, stroke_width=2.5, tip_length=0.15)
    return VGroup(blocks, bl, noisy, out, proj, a1, enc, clean, a2, cos, link)


def node_box_(text, color, font_size=20):
    t = label(text, font_size=font_size, color=color)
    box = RoundedRectangle(width=t.width + 0.4, height=0.55, corner_radius=0.1, stroke_color=color, stroke_width=2,
                           fill_color=color, fill_opacity=0.1)
    return VGroup(box, t.move_to(box))


class REPA(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.experiment()
        self.frontier()

    def card(self):
        card = chapter_card(4, r"Borrowed eyes", r"Must a denoiser learn to see from scratch?", part=PART)
        with self.voiceover("Chapter four. Borrowed eyes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def idea(self):
        pic = repa_picture().scale(1.05).move_to([-1.2, 0.9, 0])
        f = MathTex(r"\mathcal{L} = \mathcal{L}_{\text{flow}} \;+\; \lambda \cdot \frac{1}{N}\sum_{n=1}^{N}"
                    r"\Big(1 - \cos\big(h_\phi(z_n),\ y_n\big)\Big)", font_size=32).move_to([0, -2.1, 0])
        fl = label(r"$z_n$: \ the denoiser's token $n$ after an early block; \ $y_n$: \ the frozen encoder's token $n$; \ "
                   r"$h_\phi$: \ a small MLP", font_size=20, color=GREY_A).next_to(f, DOWN, buff=0.2)
        cite_ = cite(r"S.~Yu, \dots, S.~Xie, \textit{Representation Alignment for Generation} (REPA, 2024)", corner=UR)
        res = label(r"SiT-XL: \ the same quality \\ $17.5\times$ sooner \ (as published)", font_size=22, color=REPA_C)
        res.move_to([4.9, 1.6, 0])
        jobs = VGroup(label(r"two jobs at once:", font_size=26, color=WHITE),
                      label(r"1. \ what pictures are made of", font_size=24, color=C.TRUE_P),
                      label(r"2. \ how to remove noise", font_size=24, color=PATCH)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        jobs.move_to([2.4, 1.7, 0])
        dino = node_box_(r"a vision encoder, \ e.g.\ DINOv2 (Part 24): \ already knows 1", C.TRUE_P, font_size=22)
        dino.move_to([2.4, -0.2, 0])
        probe = label(r"probe the denoiser's middle layers: \ it learns 1 too, \ but slowly, \ far behind", font_size=22,
                      color=GREY_A).move_to([2.4, -1.5, 0])
        with self.voiceover(
            "A diffusion transformer has to learn two things at once: what pictures are made of, and how to remove "
            "noise. <bookmark mark='p'/> But vision encoders trained on millions of images, like Part 24's DINOv2, "
            "already know the first. <bookmark mark='q'/> Probe a diffusion transformer's middle layers, and you find "
            "it does learn what pictures show, and slowly comes to resemble such an encoder, but it lags far behind. "
            "<bookmark mark='a'/> In October 2024 Sihyun Yu, Saining Xie and colleagues added one term to "
            "the loss. Take the denoiser's tokens after an early block, pass them through a small projector, "
            "<bookmark mark='b'/> and pull them toward the frozen encoder's tokens for the clean picture, by cosine "
            "similarity. <bookmark mark='c'/> They called it REPA, representation alignment. A large diffusion "
            "transformer reached the same quality seventeen and a half times sooner."
        ) as vo:
            self.play(FadeIn(cite_), FadeIn(pic[0]), FadeIn(pic[1]), FadeIn(pic[2]), FadeIn(pic[3]))
            self.play(LaggedStart(*[FadeIn(j_, shift=RIGHT * 0.1) for j_ in jobs], lag_ratio=0.4), run_time=1.6)
            vo.wait_until("p")
            self.play(FadeIn(dino, shift=UP * 0.1))
            vo.wait_until("q")
            self.play(FadeIn(probe))
            vo.wait_until("a")
            self.play(FadeOut(jobs), FadeOut(dino), FadeOut(probe))
            self.play(GrowArrow(pic[5]), FadeIn(pic[4]))
            vo.wait_until("b")
            self.play(FadeIn(pic[7]), GrowArrow(pic[8]), FadeIn(pic[6]), GrowFromCenter(pic[10]), FadeIn(pic[9]))
            self.play(Write(f), FadeIn(fl))
            vo.wait_until("c")
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        d = load("denoisers")
        ev = np.asarray(d["eval_at"], float)
        za, ra = np.asarray(d["zero_acc"]), np.asarray(d["repa_acc"])
        zf, rf = np.asarray(d["zero_fd"]), np.asarray(d["repa_fd"])
        rc = np.asarray(d["repa_curve"])  # (seeds, points, [step, loss, align])
        top_fd = float(max(zf.max(), rf.max())) * 1.08
        ax1 = axes([0, ev[-1]], [0, 1], x_length=4.2, y_length=2.6, xlabel=r"training step",
                   ylabel=r"generated letters read as requested", xticks=[0, ev[-1]], yticks=[0, 0.5, 1],
                   center=[-4.45, 0.2, 0], font_size=17, xfmt=lambda x: fmt_int(x))
        ax2 = axes([0, ev[-1]], [0, top_fd], x_length=4.2, y_length=2.6, xlabel=r"training step",
                   ylabel=r"distance from real letters (FD)", xticks=[0, ev[-1]], yticks=[0, round(top_fd / 2)],
                   center=[1.0, 0.2, 0], font_size=17, xfmt=lambda x: fmt_int(x))
        ax3 = axes([0, rc[0, -1, 0]], [0, 1], x_length=3.0, y_length=2.6, xlabel=r"training step",
                   ylabel=r"alignment \ (cosine)", xticks=[0, rc[0, -1, 0]], yticks=[0, 0.5, 1], center=[5.35, 0.2, 0],
                   font_size=17, xfmt=lambda x: fmt_int(x))
        l1 = VGroup(mean_band(ax1.ax, ev, za, BASE_C), mean_band(ax1.ax, ev, ra, REPA_C))
        l2 = VGroup(mean_band(ax2.ax, ev, zf, BASE_C), mean_band(ax2.ax, ev, rf, REPA_C))
        l3 = mean_band(ax3.ax, rc[0, :, 0], rc[:, :, 2], REPA_C)
        leg = legend([(BASE_C, r"adaLN-Zero"), (REPA_C, r"the same, plus REPA")], font_size=20).to_edge(UP, buff=0.35)
        head = note(rf"teacher: \ chapter 1's vision transformer, \ frozen; \ REPA after block ${int(d['repa_layer'])}$ "
                    rf"of ${int(d['L'])}$, \ $\lambda = {float(d['repa_w']):g}$; \ three seeds each, \ bands: \ min to max").to_edge(DOWN, buff=0.35)
        z_end, r_end = float(zf[:, -1].mean()), float(rf[:, -1].mean())
        reach = next((int(s) for s, v in zip(ev, rf.mean(0)) if v <= z_end), None)
        za_end, ra_end = float(za[:, -1].mean()), float(ra[:, -1].mean())
        if reach is not None and reach < ev[-1] and r_end < z_end:
            verdict = (f"With REPA, the generated letters reach the plain model's final distance by step {reach:,}, "
                       f"{ev[-1] / reach:.1f} times sooner, and end closer still: {r_end:.0f} against {z_end:.0f}.")
        elif r_end < z_end:
            verdict = (f"With REPA the generated letters end closer to real ones, {r_end:.0f} against {z_end:.0f}, "
                       "though not by much.")
        else:
            verdict = (f"Here REPA doesn't help: the distance ends at {r_end:.0f} with it and {z_end:.0f} without. Our "
                       "teacher only learned to name letters, and the letters are easy to see; REPA's gains came from "
                       "encoders trained on millions of varied images.")
        ends = VGroup(label(rf"${100 * ra_end:.0f}\%$", font_size=18, color=REPA_C).next_to(ax1.ax.c2p(ev[-1], ra_end), RIGHT, buff=0.1),
                      label(rf"${100 * za_end:.0f}\%$", font_size=18, color=BASE_C).next_to(ax1.ax.c2p(ev[-1], za_end), RIGHT, buff=0.1))
        if abs(ends[0].get_y() - ends[1].get_y()) < 0.3:
            hi_, lo_ = (ends[0], ends[1]) if ra_end >= za_end else (ends[1], ends[0])
            hi_.shift(UP * 0.15)
            lo_.shift(DOWN * 0.15)
        a0, a1 = float(rc[:, 0, 2].mean()), float(rc[:, -1, 2].mean())
        align = (f"And the alignment itself climbs, from {a0:.2f} to {a1:.2f}, as the denoiser's tokens come to "
                 "resemble the teacher's." if a1 > a0 + 0.05 else
                 f"The alignment itself barely moves, from {a0:.2f} to {a1:.2f}.")
        with self.voiceover(
            "We tried it on our letters, with chapter 1's vision transformer as the frozen teacher: the same "
            "diffusion transformer, the same data, steps and seeds, with and without the extra term. "
            f"<bookmark mark='a'/> The share of generated letters the judge reads as requested ends at "
            f"{100 * ra_end:.0f} percent with REPA and {100 * za_end:.0f} without. <bookmark mark='b'/> "
            + verdict + " <bookmark mark='c'/> " + align
        ) as vo:
            self.play(FadeIn(leg), Create(ax1), Create(ax2), FadeIn(head))
            self.play(*[FadeIn(l_[0]) for l_ in l1], *[Create(l_[1]) for l_ in l1], run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(ends, shift=LEFT * 0.1))
            vo.wait_until("b")
            self.play(*[FadeIn(l_[0]) for l_ in l2], *[Create(l_[1]) for l_ in l2], run_time=2.0)
            vo.wait_until("c")
            self.play(Create(ax3), FadeIn(l3[0]), Create(l3[1]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        head = label(r"Shaping the space itself", font_size=36).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(r"Jan 2025", r"VA-VAE \ (Yao, Yang \& Wang)", r"align the autoencoder's latents with a vision "
                         r"model's features: \ FID $1.35$ on ImageNet $256^2$, \ $21\times$ faster to train",
                         color=HIST, width=11.0, font_size=25),
            history_card(r"Apr 2025", r"REPA-E \ (Leng et al.)", r"train the autoencoder and the denoiser together, \ "
                         r"held in place by REPA: \ FID $1.12$", color=HIST, width=11.0, font_size=25),
            history_card(r"Oct 2025", r"representation autoencoders \ (Zheng, Ma, Tong \& Xie)", r"no VAE at all: \ a "
                         r"frozen DINOv2 encoder and a trained decoder; \ FID $1.51$ without guidance, \ $1.13$ with",
                         color=HIST, width=11.0, font_size=25),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(head, DOWN, buff=0.4)
        if cards.height > 5.0:
            cards.height = 5.0
            cards.next_to(head, DOWN, buff=0.4)
        tk = take_away(r"the space a model generates in should already mean something: \ borrow a vision model's eyes")
        with self.voiceover(
            "The same idea then moved into the latent space itself. <bookmark mark='a'/> VA-VAE aligned an "
            "autoencoder's latents with a vision model's features, so the space is easy to rebuild from and easy to "
            "generate in. <bookmark mark='b'/> REPA-E trained the autoencoder and the denoiser together, with "
            "REPA keeping the space from collapsing. <bookmark mark='c'/> And in October 2025 representation "
            "autoencoders dropped the VAE altogether: keep DINOv2 frozen as the encoder, train only a decoder, and "
            "diffuse in the encoder's own features. <bookmark mark='d'/> The space a model generates in should "
            "already mean something."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(tk, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
