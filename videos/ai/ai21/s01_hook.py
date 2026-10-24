from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import DATA, HIST, NOISE, PART, Panel, load


class Hook(VoiceoverScene):
    def construct(self):
        self.reverse()
        self.history()
        self.plan()

    # ------------------------------------------------------------------
    def reverse(self):
        d = load("denoiser")
        P = np.asarray(d["ddim_path"])[::1]  # the deterministic sampler: each point's path is a smooth curve
        pn = Panel(9.6, center=[0, -0.25, 0])
        pn.frame.set_stroke(opacity=0)
        dots = pn.dots(P[0], NOISE, radius=0.035)
        tag = note(r"a network trained on this computer, \ walking $300$ points from noise; \ computed").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Noise: three hundred random points. <bookmark mark='a'/> A network, trained on this computer, nudges "
            "each one a little, fifty times. <bookmark mark='b'/> Part 20 ended with Langevin dynamics: walk uphill "
            "on the score, the slope of the data's log-density, with noise turned down level by level. Here the "
            "network has learned that slope at every noise level, from examples alone."
        ) as vo:
            self.play(FadeIn(dots), FadeIn(tag))
            vo.wait_until("a")
            for k in range(1, len(P), 2):  # each point walks, and warms from the noise colour to the data colour
                col = interpolate_color(ManimColor(NOISE), ManimColor(DATA), k / (len(P) - 1))
                self.play(*[dot.animate.move_to(q).set_color(col) for dot, q in zip(dots, pn.pts(P[k]))],
                          run_time=0.16, rate_func=linear)
            vo.wait_until("b")
            idx = np.linspace(0, P.shape[1] - 1, 18).astype(int)

            def path(i):  # short segments warming from the noise colour to the data colour along the way
                Q = pn.pts(P[:, i])
                return VGroup(*[Line(Q[k], Q[k + 1], stroke_width=1.8, stroke_opacity=0.75,
                                     color=interpolate_color(ManimColor(NOISE), ManimColor(DATA), k / (len(Q) - 2)))
                                for k in range(len(Q) - 1)])

            paths = VGroup(*[path(i) for i in idx])
            self.play(LaggedStart(*[Create(pa) for pa in paths], lag_ratio=0.08), run_time=2.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        head = label(r"How we got here", font_size=40).to_edge(UP, buff=0.35)
        cards = VGroup(
            history_card(2015, r"Sohl-Dickstein, Weiss, Maheswaranathan \& Ganguli",
                         r"destroy the data's structure slowly, \ then learn to run it backwards", color=HIST, width=4.3,
                         font_size=22),
            history_card(2019, r"Song \& Ermon", r"one network, \ the score at many noise levels", color=HIST,
                         width=4.3, font_size=22),
            history_card(2020, r"Ho, Jain \& Abbeel: \ DDPM", r"guess the noise; \ CIFAR-10 at FID $3.17$", color=HIST,
                         width=4.3, font_size=22),
            history_card(2021, r"Song et al.: \ score SDEs; \ Dhariwal \& Nichol", r"one framework; \ diffusion beats "
                         r"GANs on ImageNet", color=HIST, width=4.3, font_size=22),
            history_card(2022, r"Rombach et al.: \ latent diffusion", r"Stable Diffusion, \ open weights; \ DALL$\cdot$E 2, "
                         r"Imagen", color=HIST, width=4.3, font_size=22),
            history_card(2023, r"Peebles \& Xie: \ DiT; \ Song et al.", r"transformers as denoisers; \ consistency "
                         r"models", color=HIST, width=4.3, font_size=22),
            history_card(2024, r"Esser et al.: \ SD3; \ Sora; \ FLUX.1", r"rectified flow transformers; \ video",
                         color=HIST, width=4.3, font_size=22),
            history_card(2025, r"Veo 3; \ LLaDA; \ Gemini Diffusion", r"video with sound; \ diffusion language models",
                         color=HIST, width=4.3, font_size=22),
            history_card(2026, r"Google: \ DiffusionGemma", r"an open diffusion language model, \ 256 tokens at a time",
                         color=HIST, width=4.3, font_size=22),
        )
        cards.arrange_in_grid(rows=3, cols=3, buff=(0.22, 0.2)).next_to(head, DOWN, buff=0.3)
        if cards.height > 6.2:
            cards.height = 6.2
        if cards.width > 13.4:
            cards.width = 13.4
        cards.next_to(head, DOWN, buff=0.25)
        cite_ = cite(r"Part 22 opens up the architectures", corner=DR)
        with self.voiceover(
            "How we got here. In 2015 Jascha Sohl-Dickstein and colleagues borrowed an idea from physics: destroy "
            "the structure in data slowly, with noise, and learn to run the destruction backwards. <bookmark mark='a'/> "
            "In 2019 Yang Song and Stefano Ermon learned the score at many noise levels; <bookmark mark='b'/> in 2020 "
            "Jonathan Ho, Ajay Jain and Pieter Abbeel made the recipe simple: just guess the noise. <bookmark mark='c'/> "
            "In 2021 one framework joined them, and diffusion overtook GANs. <bookmark mark='d'/> In 2022 latent "
            "diffusion became Stable Diffusion, released with open weights; <bookmark mark='e'/> then transformers "
            "became the denoisers, <bookmark mark='f'/> straight-line flows trained the image models of 2024, and video "
            "followed; <bookmark mark='g'/> by 2025 the same idea was writing text, <bookmark mark='h'/> and in 2026 "
            "Google released an open diffusion language model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards[0], shift=UP * 0.1), FadeIn(cite_))
            for k, mk in enumerate("abcdefgh", 1):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.1), run_time=0.7)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Diffusion and Flow", font_size=48).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"the forward process, \ the bound, \ and why guessing the noise is learning the score",
            r"time reversed: \ the reverse SDE, \ the probability-flow ODE, \ and the samplers that solve them",
            r"design: \ noise schedules, \ EDM's preconditioning, \ DPM-Solver",
            r"flows: \ optimal transport, \ flow matching, \ rectified flow",
            r"fewer steps: \ distillation, \ consistency, \ MeanFlow; \ and guidance",
            r"discrete diffusion, \ and a diffusion language model on our scoreboard",
        ], font_size=26)
        with self.voiceover(
            "This is Part 21 of AI, Built: diffusion and flow. <bookmark mark='a'/> In this part: the forward "
            "process and the bound that trains the reverse; why guessing the noise is learning the score; "
            "<bookmark mark='b'/> running time backwards, with a stochastic equation or a deterministic one, and the "
            "samplers that solve them; <bookmark mark='c'/> the design choices, from noise schedules to EDM and "
            "DPM-Solver; <bookmark mark='d'/> flow matching and optimal transport; <bookmark mark='e'/> how to get "
            "from fifty steps to one; how to ask for something specific; <bookmark mark='f'/> and diffusion for text, "
            "with a language model of our own on the scoreboard. <bookmark mark='g'/> Every model here is trained on "
            "this computer."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            rows = obj.rows
            self.play(FadeOut(smap), FadeIn(obj.head), FadeIn(rows[0], shift=RIGHT * 0.1))
            for k, mk in enumerate("bcdef", 1):
                vo.wait_until(mk)
                self.play(*[r_[1].animate.set_opacity(0.45) for r_ in rows[:k]], FadeIn(rows[k], shift=RIGHT * 0.1),
                          run_time=0.6)
            vo.wait_until("g")
            self.play(*[r_[1].animate.set_opacity(1) for r_ in rows], run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
