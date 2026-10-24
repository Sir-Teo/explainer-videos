from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import HIST, LAT_C, PANEL, PART, PATCH, glyph_sheet, gray_image, load

SIDE_C = {10: C.TRUE_P, 5: C.BITS, 2: C.INTERVAL, 1: "#B39DDB"}


def latent_stack(side, ch, cell=0.2, color=LAT_C) -> VGroup:
    """A side x side x ch block of latent numbers, drawn as stacked sheets."""
    g = VGroup()
    for c in range(min(ch, 6)):
        sheet = VGroup(*[Square(cell, stroke_width=0.8, stroke_color=color, fill_color=color, fill_opacity=0.25)
                         for _ in range(side * side)]).arrange_in_grid(side, side, buff=0)
        g.add(sheet.shift(0.1 * c * (UP + RIGHT)))
    return g


class Latent(VoiceoverScene):
    def construct(self):
        self.card()
        self.why()
        self.sweep()
        self.generate()

    def card(self):
        card = chapter_card(3, r"A smaller space", r"Why denoise every pixel?", part=PART)
        with self.voiceover("Chapter three. A smaller space."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def why(self):
        d = load("latents")
        orig = np.asarray(d["orig"])
        rec = np.asarray(d["g5c4_rec"])
        a_in = gray_image(orig[0], 1.8).move_to([-5.2, 1.0, 0])
        enc = Polygon([-1.0, 0.9, 0], [1.0, 0.4, 0], [1.0, -0.4, 0], [-1.0, -0.9, 0], stroke_color=LAT_C, stroke_width=2.5,
                      fill_color=LAT_C, fill_opacity=0.1).move_to([-2.6, 1.0, 0])
        lat = latent_stack(5, 4).move_to([-0.2, 1.0, 0])
        dec = enc.copy().flip(UP).move_to([2.2, 1.0, 0])
        a_out = gray_image(rec[0], 1.8).move_to([4.8, 1.0, 0])
        labs = VGroup(label(r"$400$ pixels", font_size=20, color=GREY_A).next_to(a_in, DOWN, buff=0.15),
                      label(r"encoder", font_size=20, color=LAT_C).move_to(enc),
                      label(r"$5 \times 5 \times 4 = 100$ numbers", font_size=20, color=LAT_C).next_to(lat, DOWN, buff=0.2),
                      label(r"decoder", font_size=20, color=LAT_C).move_to(dec),
                      label(r"rebuilt", font_size=20, color=GREY_A).next_to(a_out, DOWN, buff=0.15))
        hc = history_card(2022, r"Rombach, Blattmann, Lorenz, Esser \& Ommer", r"latent diffusion: \ an autoencoder "
                          r"removes the detail nobody notices \ (\textit{perceptual} compression); \ diffusion learns "
                          r"what's left \ (\textit{semantic})", color=HIST, width=6.4, font_size=20).move_to([-3.2, -2.0, 0])
        kl8 = VGroup(label(r"Stable Diffusion's KL-f8:", font_size=22, color=PATCH),
                     MathTex(r"512 \times 512 \times 3 \;\to\; 64 \times 64 \times 4", font_size=30, color=WHITE),
                     label(r"$48\times$ fewer numbers; \ a whisper of KL \ (Part 20's VAE)", font_size=20, color=GREY_A)
                     ).arrange(DOWN, buff=0.15).move_to([3.6, -2.0, 0])
        with self.voiceover(
            "Real pictures have millions of pixels, and most of that detail is predictable texture. In 2022 Robin "
            "Rombach, Patrick Esser, Bjorn Ommer and colleagues split the work in two. <bookmark mark='a'/> An "
            "autoencoder squeezes the picture into a small grid of latent numbers and rebuilds it: that removes the "
            "detail nobody notices. <bookmark mark='b'/> Then the diffusion model only has to learn what's left, the "
            "meaning. <bookmark mark='c'/> Stable Diffusion's autoencoder, called KL-f8, shrinks each side eight "
            "times and keeps four channels: forty-eight times fewer numbers, with just a whisper of Part 20's KL "
            "penalty to keep the latents tame."
        ) as vo:
            self.play(FadeIn(a_in), FadeIn(labs[0]))
            vo.wait_until("a")
            self.play(FadeIn(enc), FadeIn(labs[1]), FadeIn(lat, lag_ratio=0.02), FadeIn(labs[2]), run_time=1.5)
            self.play(FadeIn(dec), FadeIn(labs[3]), FadeIn(a_out), FadeIn(labs[4]))
            vo.wait_until("b")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(kl8))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sweep(self):
        d = load("latents")
        cfgs = [tuple(int(x) for x in c) for c in d["configs"]]
        rm = {c: float(d[f"g{c[0]}c{c[1]}_rmse"]) for c in cfgs}
        num = {c: c[0] * c[0] * c[1] for c in cfgs}
        lx = lambda n_: math.log2(n_)  # noqa: E731
        top = max(rm.values()) * 1.15
        ax = axes([4, 7], [0, top], x_length=5.6, y_length=3.6, xlabel=r"numbers in the latent (log scale)",
                  ylabel=r"rebuild error, \ held-out fonts", xticks=[4, 5, 6, 6.64], yticks=[0, round(top / 2, 2)],
                  xfmt=lambda v: {4: "16", 5: "32", 6: "64", 6.64: "100"}[v], center=[-3.0, 0.2, 0], font_size=18)
        dots = VGroup(*[Dot(ax.ax.c2p(lx(num[c]), rm[c]), radius=0.08, color=SIDE_C[c[0]]) for c in cfgs])
        tags = VGroup(*[MathTex(rf"{c[0]}\!\times\!{c[0]}\!\times\!{c[1]}", font_size=18, color=SIDE_C[c[0]]) for c in cfgs])
        place_labels(list(dots), list(tags), buff=0.06)
        leg = legend([(SIDE_C[s], rf"grid ${s} \times {s}$") for s in (10, 5, 2, 1)], font_size=18).next_to(ax, RIGHT, buff=0.2)
        leg.align_to(ax, UP)
        # pictures: the held-out letters and three rebuilds
        orig = np.asarray(d["orig"])[:6]
        show = [(1, 16), (2, 16), (5, 4)]
        rows = Group(Group(label(r"letters", font_size=18, color=GREY_A), glyph_sheet(orig, 1, 6, size=0.5, gap=0.05)).arrange(RIGHT, buff=0.2))
        for c in show:
            rows.add(Group(MathTex(rf"{c[0]}\!\times\!{c[0]}\!\times\!{c[1]}", font_size=20, color=SIDE_C[c[0]]),
                           glyph_sheet(np.asarray(d[f"g{c[0]}c{c[1]}_rec"])[:6], 1, 6, size=0.5, gap=0.05)).arrange(RIGHT, buff=0.2))
        rows.arrange(DOWN, buff=0.2, aligned_edge=RIGHT).move_to([4.0, -1.6, 0])
        pairs = [((10, 1), (5, 4)), ((2, 4), (1, 16)), ((2, 16), (1, 64))]
        wins = [(a if rm[a] < rm[b] else b) for a, b in pairs]
        coarse_wins = sum(w[0] < max(a[0], b[0]) for w, (a, b) in zip(wins, pairs))
        best, worst = min(cfgs, key=lambda c: rm[c]), max(cfgs, key=lambda c: rm[c])
        trend = rm[(1, 16)] > rm[(1, 64)] and rm[(2, 4)] > rm[(2, 16)]
        same = ("More numbers rebuild better: within each grid, adding channels lowers the error. " if trend else
                "Adding channels doesn't steadily help here. ")
        coarse = (f"And at the same count, the coarser grid with more channels wins {coarse_wins} of 3 pairs: "
                  "squeezing space hard is fine, if each cell gets enough channels to describe its patch." if coarse_wins >= 2 else
                  f"At the same count, the finer grid wins {3 - coarse_wins} of 3 pairs: here, keeping the layout "
                  "matters more than deep channels.")
        with self.voiceover(
            "How small can the space be? We trained eight autoencoders on our letters, each squeezing a picture to a "
            "grid of cells with some channels each, from 16 numbers to 100. <bookmark mark='a'/> Here is each one's "
            f"rebuild error on fonts it never saw: from {rm[best]:.3f} for {best[0]} by {best[0]} by {best[1]} to "
            f"{rm[worst]:.3f} for {worst[0]} by {worst[0]} by {worst[1]}. <bookmark mark='b'/> " + same
            + "<bookmark mark='c'/> " + coarse
        ) as vo:
            self.play(Create(ax), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d_, scale=0.5), FadeIn(t_)) for d_, t_ in zip(dots, tags)],
                                  lag_ratio=0.15), run_time=2.0)
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows[1:]], lag_ratio=0.3), run_time=1.5)
            vo.wait_until("c")
            for a, b in pairs:
                ia, ib = cfgs.index(a), cfgs.index(b)
                self.play(Create(DashedLine(dots[ia].get_center(), dots[ib].get_center(), color=GREY_B,
                                            stroke_width=2, dash_length=0.06)), run_time=0.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def generate(self):
        d = load("latents")
        cfgs = [tuple(int(x) for x in c) for c in d["configs"]]
        rm = {c: float(d[f"g{c[0]}c{c[1]}_rmse"]) for c in cfgs}
        fd = {c: np.asarray(d[f"g{c[0]}c{c[1]}_fd"], float) for c in cfgs}
        top_fd = max(f.max() for f in fd.values()) * 1.1
        top_rm = max(rm.values()) * 1.1
        ax = axes([0, top_rm], [0, top_fd], x_length=5.4, y_length=3.6, xlabel=r"rebuild error \ (lower: \ a better autoencoder)",
                  ylabel=r"generated letters' distance from real ones (FD)", xticks=[0, round(top_rm / 2, 2)],
                  yticks=[0, round(top_fd / 2)], center=[-3.0, 0.3, 0], font_size=18)
        pts = VGroup()
        for c in cfgs:
            x, f = rm[c], fd[c]
            pts.add(VGroup(Line(ax.ax.c2p(x, f.min()), ax.ax.c2p(x, f.max()), color=SIDE_C[c[0]], stroke_width=2),
                           Dot(ax.ax.c2p(x, f.mean()), radius=0.08, color=SIDE_C[c[0]])))
        tags = VGroup(*[MathTex(rf"{c[0]}\!\times\!{c[0]}\!\times\!{c[1]}", font_size=18, color=SIDE_C[c[0]]) for c in cfgs])
        place_labels([p_[1] for p_ in pts], list(tags), buff=0.06)
        best_g = min(cfgs, key=lambda c: fd[c].mean())
        best_r = min(cfgs, key=lambda c: rm[c])
        smp = np.asarray(d[f"g{best_g[0]}c{best_g[1]}_samples"])
        other = best_r if best_r != best_g else max(cfgs, key=lambda c: fd[c].mean())
        smp_r = np.asarray(d[f"g{other[0]}c{other[1]}_samples"])
        sh = Group(label(rf"generated in ${best_g[0]}\times{best_g[0]}\times{best_g[1]}$", font_size=20, color=SIDE_C[best_g[0]]),
                   glyph_sheet(smp[:12], 2, 6, size=0.5, gap=0.05)).arrange(DOWN, buff=0.12).move_to([3.9, 1.4, 0])
        sr = Group(label(rf"generated in ${other[0]}\times{other[0]}\times{other[1]}$", font_size=20, color=SIDE_C[other[0]]),
                   glyph_sheet(smp_r[:12], 2, 6, size=0.5, gap=0.05)).arrange(DOWN, buff=0.12).move_to([3.9, -1.2, 0])
        cite_ = cite(r"Part 21's flow matching in each space: \ same network, \ same steps, \ two seeds (bars)", corner=DL)
        if best_g == best_r:
            verdict = (f"Here the best autoencoder, {best_r[0]} by {best_r[0]} by {best_r[1]}, is also the easiest to "
                       "generate in. On letters this simple the two goals agree.")
        else:
            verdict = (f"The space that rebuilds best, {best_r[0]} by {best_r[0]} by {best_r[1]}, is not the one that "
                       f"generates best: that's {best_g[0]} by {best_g[0]} by {best_g[1]}. A space can keep every detail "
                       "and still be hard to generate in.")
        with self.voiceover(
            "Now run Part 21's flow matching inside each space, the same small network for the same number of steps, "
            "two seeds, and measure how far the generated letters are from real ones. <bookmark mark='a'/> "
            + verdict + " <bookmark mark='b'/> This is the reconstruction against generation dilemma, and it shapes "
            "every image model: Stable Diffusion 3 and Flux widened their latents to sixteen channels; 2024's "
            "deep-compression autoencoders shrink each side thirty-two to a hundred and twenty-eight times, with "
            "many channels, to make high resolutions cheap. The next chapter is about shaping the space itself."
        ) as vo:
            self.play(Create(ax), FadeIn(cite_))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(p_), FadeIn(t_)) for p_, t_ in zip(pts, tags)], lag_ratio=0.12),
                      run_time=2.0)
            self.play(FadeIn(sh), FadeIn(sr))
            vo.wait_until("b")
            self.play(Indicate(sh[0], color=PATCH))
        self.wait(0.3)
        self.clear_scene()
