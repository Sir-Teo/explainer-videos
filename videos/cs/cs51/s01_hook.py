from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, image, load


class Hook(VoiceoverScene):
    def construct(self):
        self.samples()
        self.two_ways()
        self.plan()

    def samples(self):
        p = load("path")
        c = {r["spp"]: r for r in p["convergence"]["rows"]}
        head = label(r"Every pixel is an average of light", font_size=36).to_edge(UP, buff=0.3)
        imgs = Group()
        for k in (1, 4, 16, 256):
            g = image(p[f"spp{k}"], height=2.7)
            cap = label(rf"{k} path{'s' if k > 1 else ''} per pixel", font_size=19, color=GREY_A).next_to(g, DOWN,
                                                                                                    buff=0.15)
            err = label(rf"error {c[k]['rmse_surfaces']:.3f}", font_size=17, color=HEAD).next_to(cap, DOWN, buff=0.08)
            imgs.add(Group(g, cap, err))
        imgs.arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(rf"our own path tracer, \ 128 $\times$ 128 pixels; \ the error falls like "
                             rf"$N^{{{p['convergence']['slope_surfaces']:.2f}}}$, \ close to the "
                             r"$1/\sqrt{N}$ of Part 20's Monte Carlo", 12.4, font_size=20, color=WHITE).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "This picture was made by the program we build in this part. <bookmark mark='a'/> With one path of "
            "light per pixel it is mostly noise. Each pixel's colour is a random estimate of how much light reaches "
            "it, bounced around a box with a red wall, a green wall, a mirror ball and a light in the ceiling. "
            "<bookmark mark='b'/> With four paths the shapes appear; with sixteen the colours; "
            "<bookmark mark='c'/> with two hundred and fifty-six it is nearly clean, and the soft shadows and the red "
            "light spilling onto the white ball are not painted on: they come out of the physics. "
            "<bookmark mark='d'/> The error falls like one over the square root of the number of paths, the "
            "Monte Carlo rate of Part 20, so four times the work halves the noise."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(imgs[0]))
            vo.wait_until("b")
            self.play(FadeIn(imgs[1]))
            self.play(FadeIn(imgs[2]))
            vo.wait_until("c")
            self.play(FadeIn(imgs[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def two_ways(self):
        w = load("whitted")
        b = load("bary")
        head = label(r"Two ways to make a picture", font_size=36).to_edge(UP, buff=0.3)
        left = image(b["image"], height=3.0)
        right = image(w["image"], height=3.0)
        Group(left, right).arrange(RIGHT, buff=1.6).next_to(head, DOWN, buff=0.5)
        l1 = wrapped_label(r"\textbf{rasterization}: \ project each triangle onto the screen, \ then fill the pixels "
                           r"it covers \ (games, \ interfaces, \ this video's own text)", 4.6, font_size=19,
                           color=DATA).next_to(left, DOWN, buff=0.3)
        r1 = wrapped_label(rf"\textbf{{ray tracing}}: \ follow light backward from the eye into the scene \ "
                           rf"({w['counts']['total']:,} rays for this {w['W']} $\times$ {w['H']} image)", 4.6,
                           font_size=19, color=HEAD).next_to(right, DOWN, buff=0.3)
        hist = note(r"Sutherland's Sketchpad drew lines on a screen in 1963; \ Whitted traced recursive rays in 1980",
                    font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "There are two ways to turn a scene into pixels, and this part builds both. <bookmark mark='a'/> "
            "Rasterization takes each triangle, projects its corners onto the screen with linear algebra and one "
            "division, and fills in the pixels it covers, here blending three colours across one triangle. Games and "
            "user interfaces work this way, sixty or more times a second. <bookmark mark='b'/> Ray tracing works "
            "backwards: from the eye, through each pixel, into the scene, bouncing off mirrors and through glass. "
            f"This small image took {w['counts']['total']:,} rays. <bookmark mark='c'/> Ivan Sutherland's Sketchpad "
            "drew lines on a screen in 1963. Turner Whitted traced recursive rays in 1980. The mathematics between "
            "them is the subject of this part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(r1))
            vo.wait_until("c")
            self.play(FadeIn(hist))
        self.wait(0.4)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Light and Pixels", font_size=36).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"transforms, \ quaternions, \ and perspective as one division",
            r"rasterization, \ the z-buffer and why $1/w$",
            r"shading, \ textures and sampling without aliasing",
            r"ray tracing and bounding volume hierarchies",
            r"radiometry, \ the rendering equation and path tracing",
            r"curves and surfaces, \ including the letters on this screen",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 51 of Computer Science, Built, and the first part of Act Ten, Horizons and Trust. "
            "<bookmark mark='a'/> We will transform and project geometry; rasterize it with a depth buffer and "
            "perspective-correct interpolation; shade it and texture it without aliasing; trace rays through a "
            "bounding volume hierarchy; derive the rendering equation and solve it by path tracing; and finish with "
            "the curves that draw every letter you have read in this series."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM, NO, YES)
