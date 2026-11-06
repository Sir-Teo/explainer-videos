from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, image, load


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.realtime()
        self.neural()
        self.open()

    def card(self):
        card = chapter_card(14, r"Frontier: \ real time, \ and neural rendering",
                            r"Can a path tracer run at sixty frames a second?", lit=(2018, 2023),
                            extra=((2018, r"ray-tracing hardware in consumer GPUs"),
                                   (2023, r"3D Gaussian splatting")), part=PART)
        with self.voiceover("Chapter fourteen, the frontier. Can a path tracer run at sixty frames a second?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def realtime(self):
        d = load("denoise")
        p = load("path")
        c = {r["spp"]: r for r in p["convergence"]["rows"]}
        head = label(r"A few samples, \ then clean up", font_size=36).to_edge(UP, buff=0.3)
        a = image(d["noisy"], height=3.0)
        b = image(d["denoised"], height=3.0)
        r = image(p["reference"], height=3.0)
        Group(a, b, r).arrange(RIGHT, buff=0.4).next_to(head, DOWN, buff=0.45)
        ca = label(rf"16 paths: \ error {d['rmse_surfaces_before']:.3f}", font_size=18, color=NO).next_to(a, DOWN,
                                                                                                    buff=0.15)
        cb = label(rf"denoised: \ {d['rmse_surfaces_after']:.3f}", font_size=18, color=YES).next_to(b, DOWN,
                                                                                               buff=0.15)
        cr = label(rf"reference \ (256 paths: \ {c[256]['rmse_surfaces']:.3f})", font_size=18, color=GREY_A).next_to(
            r, DOWN, buff=0.15)
        notes = wrapped_label(r"real time adds three ideas: \ ray-tracing hardware that walks the BVH \ (2018); \ "
                              r"reusing samples across pixels and frames \ (ReSTIR, \ Bitterli et al. \ 2020); \ "
                              r"and learned denoisers and upscalers", 12.4, font_size=19, color=WHITE).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "A film frame can take hours. A game has sixteen milliseconds. <bookmark mark='a'/> The gap is closed "
            "first by taking very few samples: here our own image at sixteen paths a pixel, still noisy. "
            f"<bookmark mark='b'/> Then a denoiser, the edge-aware filter of chapter twelve, smooths the noise "
            f"guided by each pixel's normal and colour, and its error drops from {d['rmse_surfaces_before']:.3f} to "
            f"{d['rmse_surfaces_after']:.3f}, below that of two hundred and fifty-six paths. <bookmark mark='c'/> "
            "Real-time renderers add three more ideas: hardware since 2018 that walks bounding volume hierarchies "
            "in silicon; algorithms such as ReSTIR, from 2020, that reuse good light samples across neighbouring "
            "pixels and frames; and neural networks trained to denoise and upscale."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(ca))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(cb), FadeIn(r), FadeIn(cr))
            vo.wait_until("c")
            self.play(FadeIn(notes))
        self.wait(0.4)
        self.clear_scene()

    def neural(self):
        head = label(r"Scenes learned from photographs", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"neural radiance fields", r"Mildenhall et al. \ (2020): \ a network maps a point and a direction to "
                 r"colour and density; \ volume rendering along each ray, \ trained on photographs", DATA),
            tile(r"Gaussian splatting", r"Kerbl et al. \ (2023): \ millions of small 3D Gaussians, \ projected and "
                 r"blended by a rasterizer, \ fitted to photos; \ real time", HEAD),
            tile(r"what is lost", r"no explicit materials or lights: \ hard to edit, \ relight or verify; \ physics "
                 r"enters only through the training data", NO),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"both are the rendering of this part run in reverse: \ given pictures, \ find the scene "
                             r"\ (\textit{AI, Built} \ 22)", 12.4, font_size=21, color=WHITE).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The newest idea turns rendering around. <bookmark mark='a'/> In 2020 Ben Mildenhall and colleagues "
            "trained a small network that maps a point and a viewing direction to a colour and a density, and "
            "rendered it by integrating along each ray, fitted to a few dozen photographs of a real scene. "
            "<bookmark mark='b'/> In 2023 Bernhard Kerbl and colleagues replaced the network with millions of "
            "small three-dimensional Gaussians, projected and blended by a rasterizer, which runs in real time. "
            "<bookmark mark='c'/> What is lost is the physics: there are no explicit materials or lights, so these "
            "scenes are hard to edit or relight. <bookmark mark='d'/> Both run this part backwards: given pictures, "
            "find the scene, the inverse problem of AI, Built part twenty-two."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Caustics}: \ light through glass onto a diffuse floor converges slowly for "
                          r"every known unbiased method.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Denoisers with guarantees}: \ bounds on the bias a filter introduces.", 12.4,
                          font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Inverse rendering}: \ recovering materials and lights, \ not just "
                          r"appearance, \ from photographs.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Perceptual error}: \ a measure of image error that matches what people "
                          r"see.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ an unbiased estimator for "
                             r"specular--diffuse--specular paths \ (caustics seen in a mirror) \ whose variance is "
                             r"within a constant factor of the best possible, \ with a proof", 12.4, font_size=23,
                             color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Caustics: light focused through glass onto a floor and seen in a "
            "mirror is still slow to converge for every known unbiased method. <bookmark mark='b'/> Denoisers with "
            "guarantees on the bias they introduce. <bookmark mark='c'/> Inverse rendering that recovers materials "
            "and lights, and not just appearance. <bookmark mark='d'/> And a measure of image error that matches "
            "what people actually see. <bookmark mark='e'/> This part's research problem asks for an unbiased "
            "estimator for those caustic paths whose variance is provably within a constant factor of the best "
            "possible."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
