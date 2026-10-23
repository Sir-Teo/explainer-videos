from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (AR, DATA, EBM, FAM, FAM_NAME, FLOW, GAN_C, PART, VAE_C, digit_sheet, load,
                                   node_box)


class Hook(VoiceoverScene):
    def construct(self):
        self.digits()
        self.question()
        self.plan()

    # ------------------------------------------------------------------
    def digits(self):
        fams = ["pixelcnn", "vae", "gan", "flow"]
        runs = {f: load(f) for f in fams}
        panels = Group()
        for f in fams:
            sheet = digit_sheet(np.asarray(runs[f]["s0_show"])[:16], 4, 4, size=0.6, gap=0.05)
            cap = label(FAM_NAME[f], font_size=26, color=FAM[f]).next_to(sheet, UP, buff=0.18)
            panels.add(Group(sheet, cap))
        panels.arrange(RIGHT, buff=0.42).move_to(UP * 0.35)
        mins = np.mean([runs[f]["s0_secs"] for f in fams]) / 60
        how = VGroup(
            label(r"one pixel at a time", font_size=22, color=AR),
            label(r"squeeze to $16$ numbers, \ expand again", font_size=22, color=VAE_C),
            label(r"a game against a critic", font_size=22, color=GAN_C),
            label(r"bend noise, \ invertibly", font_size=22, color=FLOW),
        )
        for h, p in zip(how, panels):
            h.next_to(p, DOWN, buff=0.22)
            if h.width > p.width + 0.3:
                h.width = p.width + 0.3
        tg = note(r"computed: \ trained on this computer, \ MNIST at $14 \times 14$").to_corner(DR, buff=0.25)
        with self.voiceover(
            "None of these sixty-four digits was written by a person. <bookmark mark='a'/> Each block was drawn by a "
            "different machine, trained on the computer making this video, for about "
            f"{mins:.0f} minutes each, on the same sixty thousand handwritten digits. <bookmark mark='b'/> The first "
            "writes a digit one pixel at a time. <bookmark mark='c'/> The second squeezes every digit into sixteen "
            "numbers and learns to expand them again. <bookmark mark='d'/> The third learned by playing a game "
            "against a critic. <bookmark mark='e'/> And the fourth bends random noise, smoothly and invertibly, into "
            "ink."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(p[0], scale=0.96) for p in panels], lag_ratio=0.25), run_time=2.2)
            vo.wait_until("a")
            self.play(*[FadeIn(p[1]) for p in panels], FadeIn(tg))
            for k, mk in enumerate("bcde"):
                vo.wait_until(mk)
                self.play(FadeIn(how[k], shift=UP * 0.1), Indicate(panels[k][1], color=FAM[fams[k]]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def question(self):
        real = load("classifier")
        sheet = digit_sheet(np.asarray(real["grid"])[:32], 4, 8, size=0.5, gap=0.04).move_to([-3.6, 0.9, 0])
        rl = label(r"real digits: \ samples from $p(x)$", font_size=24, color=DATA).next_to(sheet, UP, buff=0.15)
        q = label(r"From examples alone, \\ learn a distribution \\ you can draw new ones from.", font_size=38)
        q.move_to([3.4, 1.0, 0])
        ways = VGroup(
            node_box(r"one piece at a time", AR, font_size=22),
            node_box(r"compress and expand", VAE_C, font_size=22),
            node_box(r"a two-player game", GAN_C, font_size=22),
            node_box(r"an invertible map", FLOW, font_size=22),
            node_box(r"an energy landscape", EBM, font_size=22),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 2.2)
        if ways.width > 13.4:
            ways.width = 13.4
        yrs = VGroup(*[label(t, font_size=20, color=GREY_B).next_to(w, DOWN, buff=0.12) for t, w in
                       zip((r"Shannon, \ 1948", r"Kingma \& Welling, \ 2013", r"Goodfellow et al., \ 2014",
                            r"Dinh et al., \ 2014", r"Hopfield, \ 1982"), ways)])
        with self.voiceover(
            "Real handwriting looks like this: samples from some distribution p of x that nobody can write down. "
            "<bookmark mark='a'/> The question of this part: from examples alone, how do you learn a distribution "
            "you can draw new examples from? <bookmark mark='b'/> The field found four answers that work, and one "
            "older one that it keeps coming back to. Build the example one piece at a time. Compress it into a code "
            "and learn to expand the code. Set two networks against each other. Bend simple noise with an "
            "invertible map. <bookmark mark='c'/> Or carve an energy landscape that the data sits at the bottom of. "
            "Diffusion, next time, is built from these pieces."
        ) as vo:
            self.play(FadeIn(sheet), FadeIn(rl))
            vo.wait_until("a")
            self.play(Write(q), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.15) for w in ways[:4]], lag_ratio=0.5),
                      LaggedStart(*[FadeIn(y) for y in yrs[:4]], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("c")
            self.play(FadeIn(ways[4], shift=UP * 0.15), FadeIn(yrs[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Four Ways to Generate", font_size=44).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.5)
        obj = objectives_card([
            r"the generative problem, \ and how the field got here",
            r"autoregressive models: \ the chain rule, \ PixelCNN",
            r"latent variables: \ the Helmholtz machine, \ the VAE and its bound, \ posterior collapse",
            r"adversarial games: \ GANs, \ why they spiral, \ Wasserstein GANs, \ StyleGAN",
            r"invertible maps: \ coupling flows, \ neural ODEs, \ Hutchinson's trace",
            r"energy: \ Hopfield and Boltzmann, \ contrastive divergence, \ Langevin dynamics and the score",
            r"judging generators: \ FID, \ precision and recall; \ five models on one budget",
        ], font_size=25)
        with self.voiceover(
            "This is Part 20 of AI, Built, and the start of its fourth act: generation and perception. "
            "<bookmark mark='a'/> In this part: the generative problem and its history; autoregressive models; "
            "latent variables, from the Helmholtz machine to the variational autoencoder; adversarial games, why "
            "they spiral, and how Wasserstein distance and StyleGAN tamed them; invertible maps, from coupling "
            "layers to neural ODEs; energy, from Hopfield and Boltzmann to Langevin dynamics and the score; and how "
            "to judge a generator, with every family trained here and compared on one budget."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.3)
        self.clear_scene()
