from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ Light and Pixels", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"x' = \tfrac{n\,x}{-z}", font_size=54, color=HEAD), r"perspective", HEAD),
            tile(MathTex(r"\tfrac{u/w}{1/w}", font_size=60, color=YES), r"perspective-correct", YES),
            tile(label(r"mipmaps, \ not moir\'e", font_size=36, color=DATA), r"sampling", DATA),
            tile(label(r"$O(\log n)$ per ray", font_size=40, color=KERN), r"BVHs", KERN),
            tile(MathTex(r"L_o = L_e + \int f\,L_i \cos\theta", font_size=40, color=LAM), r"the rendering equation",
                 LAM),
            tile(MathTex(r"1/\sqrt{N}", font_size=60, color=NO), r"path tracing", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Transforms as matrices, with quaternions to rotate smoothly; perspective "
            "as linear algebra plus one division, and the depth buffer that division distorts. A rasterizer with "
            "edge functions and perspective-correct interpolation, shading, and textures sampled without aliasing. "
            "A ray tracer, accelerated by bounding volume hierarchies to a logarithm per ray. Radiometry and the "
            "rendering equation, solved by a path tracer whose noise falls as one over the square root of the "
            "samples, made practical by importance sampling and denoising. And the Bézier curves that draw every "
            "letter on screen. One idea runs through it: a picture is an integral, and every technique is a way of "
            "estimating it."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"numerical integration and linear solvers", [52]),
            (r"hardware built for graphics and learning", [60]),
            (r"verified rendering pipelines and GPUs", [54]),
            (r"learning from images", [57]),
            (r"open problems as research", [61]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 52 treats integration and linear solvers with the care rounding demands. "
            "Part 54 proves programs correct, graphics drivers among them. Part 57 asks when learning from images "
            "can generalize. Part 60 builds hardware for one job, and the GPU is the first and most successful "
            "example. And Part 61 returns to this part's open problems as research."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"engines", r"Unreal, \ Unity and Godot: \ rasterization with ray-traced effects"),
            (r"APIs", r"Vulkan, \ Metal, \ Direct3D 12 and WebGPU: \ shaders and command buffers"),
            (r"film", r"production path tracers, \ with denoisers and render farms"),
            (r"interfaces", r"fonts, \ vector graphics and compositors draw every screen you use"),
            (r"debug", r"look at the image at one sample per pixel: \ noise tells you what is wrong"),
        ])
        with self.voiceover(
            "In practice. Game engines rasterize, and add ray-traced shadows and reflections where hardware allows. "
            "Graphics programming interfaces such as Vulkan, Metal and WebGPU expose shaders and command buffers. "
            "Film is rendered by production path tracers with denoisers, on render farms. Fonts, vector graphics "
            "and compositors draw every interface you use. And when a renderer is wrong, look at one sample per "
            "pixel: the noise tells you where the light is lost."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive the perspective matrix that maps the frustum to the cube $[-1, 1]^3$, \ and show depth is "
            r"affine in $1/z$.",
            r"Show that interpolating $u/w$ and $1/w$ linearly in screen space gives perspective-correct $u$.",
            r"Derive the M\"oller--Trumbore ray--triangle test with Cramer's rule.",
            r"Prove that Russian roulette leaves the path tracer unbiased, \ and compute its effect on variance.",
            r"\textit{Build.} \ Add next-event estimation for a second light to our path tracer, \ and measure the "
            r"noise at 16 spp.",
            r"$\bigstar$ \textit{Research.} \ Caustic paths with provably near-optimal variance.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: give our path tracer a second light and sample both, then measure the noise. The last, marked "
            "with a star, is a research problem: an estimator for caustics whose variance is provably close to the "
            "best possible."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 52, \ Computing with Real Numbers", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"conditioning against stability", HEAD),
            (r"elimination, \ QR and the SVD", YES),
            (r"conjugate gradients and multigrid", DATA),
            (r"stiff equations and symplectic orbits", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 52: computing with real numbers. With rounding in every operation, which answers can we "
            "trust? The answer separates how hard a problem is from how good an algorithm is, and leads to the "
            "algorithms that power all of scientific computing."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Pharr, \ Jakob and Humphreys, \ \textit{Physically Based Rendering} \ (4th ed.)",
             r"Marschner and Shirley, \ \textit{Fundamentals of Computer Graphics}; \ Akenine-M\"oller et al., \ "
             r"\textit{Real-Time Rendering}"],
            [r"Sutherland \ (1963); \ Catmull \ (1974); \ Whitted \ (1980); \ Williams \ (1983)",
             r"Kajiya \ (1986); \ Veach \ (1997); \ Cook and Torrance \ (1982); \ Walter et al. \ (2007)",
             r"M\"oller and Trumbore \ (1997); \ Shoemake \ (1985); \ Catmull and Clark \ (1978)",
             r"Bitterli et al. \ (2020); \ Mildenhall et al. \ (2020); \ Kerbl et al. \ (2023)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
