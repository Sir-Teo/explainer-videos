from __future__ import annotations

from datetime import date

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant12.common import BAD, IV, LV, OPT, PART, RV, SPOT, illustration, load, real_data


class Learning(VoiceoverScene):
    def construct(self):
        v = load("vae")
        h = load("history")
        self.card()
        self.latent(v, h)
        self.walk(v, h)

    def card(self):
        c = chapter_card(7, r"Learning surfaces", r"How many numbers describe a day's surface?", part=PART)
        with self.voiceover("Chapter seven. Learning surfaces."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def latent(self, v, h):
        z = np.asarray(v["latent"])
        atm = np.asarray(v["atm"])
        g = axes([-3, 3], [-3, 3], x_length=4.8, y_length=4.8, xlabel=r"$z_1$", ylabel=r"$z_2$", xticks=[-2, 0, 2],
                 yticks=[-2, 0, 2], font_size=17).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        lo, hi = atm.min(), atm.max()
        dots = VGroup(*[Dot(ax.c2p(*np.clip(p, -3, 3)), radius=0.06,
                            color=interpolate_color(ManimColor(QC.SPOT), ManimColor(BAD), float((a - lo) / (hi - lo))))
                        for p, a in zip(z, atm)])
        cbar = VGroup(label(rf"colour: 30-day ATM vol, {100 * lo:.0f}\% (blue) to {100 * hi:.0f}\% (red)", font_size=17,
                            color=GREY_B)).next_to(g, DOWN, buff=0.15)
        side = VGroup(
            wrapped_label(r"each week's surface: implied vol on a grid of 17 moneyness by 6 maturity points, 102 numbers", 4.6,
                          20, GREY_A),
            wrapped_label(r"a variational autoencoder (Kingma and Welling 2014) squeezes them through two numbers and "
                          r"rebuilds the surface (Bergeron, Fung, Hull and Poulos 2022 did this for FX and equity "
                          r"surfaces)", 4.6, 20, LV),
            MathTex(rf"\text{{rebuilt to }} {v['recon_rmse_volpts']:.1f}\ \text{{vol points}}", font_size=30, color=OPT),
            MathTex(rf"\text{{corr}}(z_1, \text{{ATM level}}) = {v['corr_atm'][0]:.2f}", font_size=28, color=IV),
            MathTex(rf"\text{{corr}}(z_2, \text{{skew}}) = {v['corr_skew'][1]:.2f}", font_size=28, color=BAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.4)
        src = real_data(rf"{len(z)} weekly surfaces, 2024--2025; trained here on a CPU")
        with self.voiceover(
            "A whole surface is a lot of numbers: here, a hundred and two implied volatilities on a grid. How many "
            "does it really take? A variational autoencoder, a neural network trained to squeeze its input through a "
            "narrow middle and rebuild it, was trained on the hundred weekly surfaces. <bookmark mark='a'/> With only "
            f"two numbers in the middle, it rebuilds the surfaces to {v['recon_rmse_volpts']:.1f} volatility points. "
            "Each dot is a week, coloured by its at-the-money volatility. <bookmark mark='b'/> The network found the "
            f"level on its own: the first number tracks at-the-money volatility with a correlation of "
            f"{v['corr_atm'][0]:.2f}. The second carries part of the skew."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01, run_time=2), FadeIn(cbar), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]), FadeIn(side[4]))
        self.wait(0.4)
        self.clear_scene()

    def walk(self, v, h):
        kg = np.asarray(h["grid_k"])
        g1 = axes([-0.4, 0.4], [0.3, 0.8], x_length=5.4, y_length=3.4, xlabel=r"log-moneyness (30 days)",
                  ylabel=r"implied vol", xticks=[-0.4, 0, 0.4], yticks=[0.4, 0.6, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%",
                  font_size=16)
        g2 = axes([-0.4, 0.4], [0.3, 0.8], x_length=5.4, y_length=3.4, xlabel=r"log-moneyness (30 days)",
                  ylabel=r"implied vol", xticks=[-0.4, 0, 0.4], yticks=[0.4, 0.6, 0.8], yfmt=lambda u: f"{100 * u:.0f}\\%",
                  font_size=16)
        VGroup(g1, g2).arrange(RIGHT, buff=1.0).to_edge(UP, buff=1.0)
        t1 = label(r"move $z_1$ from $-2$ to $+2$", font_size=21, color=IV).next_to(g1, UP, buff=0.1)
        t2 = label(r"move $z_2$ from $-2$ to $+2$", font_size=21, color=BAD).next_to(g2, UP, buff=0.1)
        w1, w2 = np.asarray(v["walk"]["z1"]), np.asarray(v["walk"]["z2"])
        cols = [QC.SPOT, LV, GREY_A, IV, BAD]
        l1 = VGroup(*[curve(g1.ax, kg, np.clip(w1[i, 2], 0.3, 0.8), c, stroke_width=2.5) for i, c in enumerate(cols)])
        l2 = VGroup(*[curve(g2.ax, kg, np.clip(w2[i, 2], 0.3, 0.8), c, stroke_width=2.5) for i, c in enumerate(cols)])
        foot = wrapped_label(r"walking the latent space generates plausible surfaces that never happened: scenarios for "
                             r"risk (Part 40), and a smooth way to fill in missing quotes. But it knows nothing about "
                             r"arbitrage unless it is taught: the House checks every generated surface with Part 9's "
                             r"checker", 11.0, 20, GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Now walk through the space the network learned. Moving the first number from minus two to plus two "
            "lifts the whole smile: a calm market becomes a frightened one. <bookmark mark='a'/> Moving the second "
            "tilts it, from a put skew toward a call skew. <bookmark mark='b'/> A walk like this generates surfaces that "
            "never happened but could have: scenarios for risk management, and a smooth way to fill in missing "
            "quotes. One caution. The network knows nothing about arbitrage unless it is taught, so every surface it "
            "generates goes through the checker of Part nine."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(t1), LaggedStart(*[Create(l_) for l_ in l1], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(g2), FadeIn(t2), LaggedStart(*[Create(l_) for l_ in l2], lag_ratio=0.2), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()
