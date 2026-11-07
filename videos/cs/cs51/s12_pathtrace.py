from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block
from videos.cs.cs51.common import EYE, SPH, X1, Y0, Y1, P, box2d, cos_dir, end_of, path_mob, random_path

WORDS = ["none", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def blocks_of(pairs, buff=0.36, size=17):
    """MathTex rows each with a grey note under it: (rows, notes, group)."""
    rows = VGroup(*[r for r, _ in pairs])
    notes = VGroup(*[note(n, font_size=size) if isinstance(n, str) else n for _, n in pairs])
    g = VGroup(*[VGroup(r, n).arrange(DOWN, aligned_edge=LEFT, buff=0.07) for r, n in zip(rows, notes)])
    g.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return rows, notes, g


def hemi(p, n, r=0.42, color=GREY_B):
    """A small semicircle of directions above a vertex with normal n."""
    a = math.atan2(n[1], n[0])
    return Arc(radius=r, start_angle=a - PI / 2, angle=PI, arc_center=P(p), color=color, stroke_width=1.8)


class Pathtrace(VoiceoverScene):
    def construct(self):
        self.card()
        self.estimator()
        self.cosine()
        self.roulette()
        self.nee()
        self.mis()

    def card(self):
        card = chapter_card(11, r"Path tracing", r"How do we sample an infinite sum of integrals?",
                            lit=(1986, 1990, 1997), extra=((1986, r"Kajiya: \ path tracing"),
                                                           (1990, r"Arvo and Kirk: \ Russian roulette"),
                                                           (1997, r"Veach: \ multiple importance sampling")),
                            part=PART)
        with self.voiceover("Chapter eleven. Path tracing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ the estimator
    def estimator(self):
        head = label(r"One sample per bounce: \ a path", font_size=36).to_edge(UP, buff=0.3)
        box = box2d()
        d = np.array([X1, 0.8]) - EYE
        pts, kinds = random_path(EYE, d / np.linalg.norm(d), np.random.default_rng(42))
        segs = [path_mob([a, b], WHITE if k != "light" else HEAD, dots=False) for a, b, k in
                zip(pts, pts[1:], kinds)]
        normals = {"back": np.array([-1.0, 0]), "ceiling": np.array([0, -1.0]), "floor": np.array([0, 1.0])}
        normals["diffuse"] = None
        hemis = [VGroup(hemi(p, normals[k] if k != "diffuse" else (p - SPH[1][0]) / SPH[1][1]),
                        Dot(P(p), radius=0.06, color=WHITE)) for p, k in zip(pts[1:], kinds) if k in normals]
        ill = note(r"a side view of our box; \ directions drawn at random \ (illustrative)", font_size=16).move_to(
            [-3.3, 2.65, 0])
        r0 = MathTex(r"\int_\Omega g(\omega)\,d\omega", r"\approx",
                     r"\frac{1}{N}\sum_{k=1}^{N}\frac{g(\omega_k)}{p(\omega_k)}", font_size=32)
        r1 = MathTex(r"E\!\left[\frac{g(\omega)}{p(\omega)}\right]", r"=",
                     r"\int_\Omega \frac{g(\omega)}{p(\omega)}\,p(\omega)\,d\omega", r"=",
                     r"\int_\Omega g(\omega)\,d\omega", font_size=32)
        r2 = MathTex(r"\beta", r"\leftarrow", r"\beta\cdot\frac{f\,\cos\theta}{p}", font_size=32)
        r3 = MathTex(r"\hat L", r"=", r"\sum_{\text{vertices } j} \beta_j\, L_e(x_j)", font_size=32, color=YES)
        rows, notes, blk = blocks_of([
            (r0, r"Monte Carlo \ (Part 20): \ any density $p$ that is positive where $g$ is"),
            (r1, r"unbiased: \ right on average"),
            (r2, r"the throughput $\beta$ carries the weights from bounce to bounce"),
            (r3, r"one path, \ one estimate; \ average many per pixel")], buff=0.4)
        blk.to_edge(RIGHT, buff=0.35).set_y(-0.1)
        with self.voiceover(
            "The rendering equation is an integral inside an integral, with no end, and Monte Carlo handles that. "
            "<bookmark mark='a'/> To estimate an integral, draw directions from any density p, and average the "
            "integrand divided by p: Part twenty's method. <bookmark mark='b'/> It is unbiased: under p, the "
            "expected value of g over p is exactly the integral. <bookmark mark='c'/> Now take a single sample at "
            "each bounce. From the eye the ray meets the back wall; choose one direction at random; it meets the "
            "ceiling; again, the matte ball; again, and it reaches the lamp. That is a path. <bookmark mark='d'/> A "
            "running weight, the throughput, is multiplied at each bounce by f cos theta over p, <bookmark "
            "mark='e'/> and the light the path finds, times its throughput, is one estimate of the pixel. This is "
            "path tracing, Kajiya's own algorithm."
        ) as vo:
            self.play(FadeIn(head), FadeIn(box), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(r0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(r1), FadeIn(notes[1]))
            vo.wait_until("c")
            for k, s in enumerate(segs):
                self.play(Create(s), run_time=0.8)
                if k < len(hemis):
                    self.play(FadeIn(hemis[k]), run_time=0.4)
            vo.wait_until("d")
            self.play(Write(r2), FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(Write(r3), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ cosine-weighted sampling
    def cosine(self):
        head = label(r"Importance sampling: \ follow the cosine", font_size=36).to_edge(UP, buff=0.3)
        C = np.array([-4.9, 1.0, 0])
        R = 1.3
        disk = Circle(radius=R, color=GREY_B, stroke_width=2).move_to(C)
        rng = np.random.default_rng(2)
        n = 170
        rr, ph = np.sqrt(rng.random(n)), 2 * PI * rng.random(n)
        xs, ys = rr * np.cos(ph), rr * np.sin(ph)
        dots = VGroup(*[Dot(C + R * np.array([x, y, 0]), radius=0.03, color=DATA) for x, y in zip(xs, ys)])
        B = np.array([-4.9, -2.75, 0])
        base = Line(B + LEFT * (R + 0.2), B + RIGHT * (R + 0.2), color=GREY_B, stroke_width=2.5)
        dome = Arc(radius=R, start_angle=0, angle=PI, arc_center=B, color=GREY_B, stroke_width=2)
        lifted = [B + R * np.array([x, math.sqrt(max(0.0, 1 - x * x - y * y)), 0]) for x, y in zip(xs, ys)]
        nrm = DashedLine(B, B + UP * (R + 0.3), color=GREY_C, stroke_width=1.5)
        tl = wrapped_label(r"top view: \ uniform on the disk", 1.5, font_size=17, color=GREY_A).next_to(
            disk, RIGHT, buff=0.2)
        sl = wrapped_label(r"side view: \ lifted onto the hemisphere", 1.5, font_size=17, color=GREY_A).next_to(
            dome, RIGHT, buff=0.35).align_to(dome, DOWN)
        r0 = MathTex(r"p(\omega)", r"\propto", r"\cos\theta", font_size=32)
        r1 = MathTex(r"p_{\text{disk}}", r"=", r"\frac{1}{\pi}", font_size=32)
        r2 = MathTex(r"dA", r"=", r"\cos\theta\, d\omega", font_size=32)
        r3 = MathTex(r"p(\omega)", r"=", r"\frac{\cos\theta}{\pi}", font_size=32)
        r4 = MathTex(r"\frac{f\cos\theta}{p}", r"=", r"\frac{(\rho/\pi)\cos\theta}{\cos\theta/\pi}", r"=",
                     r"\rho", font_size=32, color=YES)
        rows, notes, blk = blocks_of([
            (r0, r"sample more where the integrand is large"),
            (r1, r"Malley's method: \ uniform points on the unit disk, \ per unit area"),
            (r2, r"the disk is the hemisphere seen from above: \ a patch $d\omega$ projects to "
                 r"$\cos\theta\, d\omega$"),
            (r3, r"so the lifted directions have density $\cos\theta/\pi$"),
            (r4, r"each bounce multiplies the throughput by the albedo")], buff=0.3)
        blk.to_edge(RIGHT, buff=0.35).set_y(-0.15)
        with self.voiceover(
            "Which density should we sample? Any works, but the noise depends on the choice. "
            "<bookmark mark='a'/> The integrand contains a cosine, so sample more often where the cosine is large, "
            "near the normal. <bookmark mark='b'/> Malley's method does this without any trigonometry. Pick points "
            "uniformly on a disk, <bookmark mark='c'/> then lift each one straight up onto the hemisphere above it. "
            "They crowd towards the top. <bookmark mark='d'/> The disk is the hemisphere seen from above, and a "
            "patch of directions d omega appears on it with area cos theta d omega. So the lifted directions have "
            "density cos theta over pi. <bookmark mark='e'/> For a matte surface, f cos theta over p is then just "
            "the albedo. Every bounce multiplies the throughput by the same number, and the cosine adds no noise "
            "at all."
        ) as vo:
            self.play(FadeIn(head), Create(disk), Create(base), Create(dome), FadeIn(nrm))
            vo.wait_until("a")
            self.play(FadeIn(r0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.01), FadeIn(tl), Write(r1),
                      FadeIn(notes[1]), run_time=2)
            vo.wait_until("c")
            moved = dots.copy()
            self.play(*[m.animate.move_to(q) for m, q in zip(moved, lifted)], FadeIn(sl), run_time=2.5)
            vo.wait_until("d")
            self.play(Write(r2), FadeIn(notes[2]))
            self.play(TransformMatchingTex(r1.copy(), r3), FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(Write(r4), FadeIn(notes[4]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ Russian roulette
    def roulette(self):
        head = label(r"Russian roulette: \ stop at random, \ stay unbiased", font_size=36).to_edge(UP, buff=0.3)
        rho = 0.73
        beta = [rho ** k for k in range(4)]
        q = beta[3]
        bw, gap, H = 0.55, 0.3, 2.0
        x0, yb = -6.0, 0.15
        bars = VGroup(*[Rectangle(width=bw, height=H * b, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
                        .move_to([x0 + k * (bw + gap), yb + H * b / 2, 0]) for k, b in enumerate(beta)])
        blab = VGroup(*[label(f"{b:.2f}", font_size=16, color=DATA).next_to(r, UP, buff=0.06) for b, r in
                        zip(beta, bars)])
        klab = VGroup(*[label(rf"{k}", font_size=16, color=GREY_B).next_to([x0 + k * (bw + gap), yb, 0], DOWN,
                                                                           buff=0.1) for k in range(6)])
        axis = Line([x0 - 0.4, yb, 0], [x0 + 5 * (bw + gap) + 0.4, yb, 0], color=GREY_C, stroke_width=1.5)
        xl = label(r"bounce", font_size=16, color=GREY_A).next_to(klab, DOWN, buff=0.08)
        surv = Rectangle(width=bw, height=H, stroke_width=0, fill_color=YES, fill_opacity=0.85).move_to(
            [x0 + 4 * (bw + gap), yb + H / 2, 0])
        sl = label(rf"$\beta/q = 1$", font_size=16, color=YES).next_to(surv, UP, buff=0.06)
        dead = Cross(scale_factor=0.22, stroke_color=NO, stroke_width=5).move_to([x0 + 4 * (bw + gap), yb + 0.3,
                                                                                    0])
        coin = wrapped_label(rf"after bounce 3: \ survive with probability $q = \beta = {q:.2f}$", 4.6,
                             font_size=18, color=HEAD).next_to(axis, UP, buff=2.35).align_to(axis, LEFT)
        outcome = VGroup(label(r"survives: \ full weight again", font_size=17, color=YES),
                         label(r"or ends", font_size=17, color=NO)).arrange(RIGHT, buff=0.4).next_to(
            xl, DOWN, buff=0.15).align_to(axis, LEFT)
        ill = note(r"throughput of one path, \ walls of albedo 0.73 \ (illustrative)", font_size=16).next_to(
            coin, UP, buff=0.12).align_to(axis, LEFT)
        code = code_block([
            "if rr and depth >= rr_start:      # 3",
            "    q = min(max(tr, tg, tb), 0.95)",
            "    if np.random.random() >= q:",
            "        break",
            "    tr, tg, tb = tr / q, tg / q, tb / q",
        ], size=14)
        ctitle = label(r"our tracer \ (\texttt{explainer/cs/graphics/path.py})", font_size=17, color=KERN)
        cblk = VGroup(ctitle, code).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(DL, buff=0.4)
        r0 = MathTex(r"X'", r"=", r"\begin{cases} X/q & \text{with probability } q \\ 0 & \text{otherwise}"
                     r"\end{cases}", font_size=32)
        r1 = MathTex(r"E[X']", r"=", r"q\cdot\frac{X}{q} + (1-q)\cdot 0", r"=", r"X", font_size=32, color=YES)
        r2 = MathTex(r"\operatorname{Var}[X']", r"=", r"\operatorname{Var}[X] + \left(\frac{1}{q}-1\right)E[X^2]",
                     font_size=32)
        rows, notes, blk = blocks_of([
            (r0, r"Arvo and Kirk \ (1990)"),
            (r1, r"unbiased: \ no term of the series is dropped"),
            (r2, r"the price: \ a little more variance per path, \ for far fewer rays")], buff=0.45)
        blk.to_edge(RIGHT, buff=0.4).set_y(0.3)
        with self.voiceover(
            "When should a path stop? Cutting every path at a fixed length drops the later terms of the series: a "
            "bias. <bookmark mark='a'/> A path's throughput shrinks at each bounce, so its later terms matter less "
            "and less. <bookmark mark='b'/> Russian roulette, brought to graphics by James Arvo and David Kirk in "
            "1990, stops paths at random instead: keep the path with probability q, and if it survives, divide its "
            "weight by q. <bookmark mark='c'/> The proof is one line. The expected contribution is q times X over q,"
            " plus one minus q times zero: X. <bookmark mark='d'/> The price is some extra variance, growing as q "
            "falls. <bookmark mark='e'/> Our tracer plays from the third bounce, with q equal to the throughput, "
            "capped at nought point nine five: dim paths usually die, and survivors return to full weight."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(klab), FadeIn(xl), FadeIn(ill))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.3), FadeIn(blab))
            vo.wait_until("b")
            self.play(FadeIn(coin), Write(r0), FadeIn(notes[0]))
            self.play(GrowFromEdge(surv, DOWN), FadeIn(sl), FadeIn(dead), FadeIn(outcome))
            vo.wait_until("c")
            self.play(Write(r1), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Write(r2), FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(cblk))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ next-event estimation
    def nee(self):
        head = label(r"Next-event estimation: \ aim at the light", font_size=36).to_edge(UP, buff=0.3)
        box = box2d(eye=False)
        x = np.array([-4.8, Y0])
        xd = Dot(P(x), radius=0.08, color=WHITE)
        xl = MathTex(r"x", font_size=28).next_to(P(x), DOWN, buff=0.1)
        rng = np.random.default_rng(3)
        rays, found = VGroup(), 0
        for _ in range(9):
            d = cos_dir(np.array([0.0, 1.0]), rng.random())
            q, h = end_of(x + np.array([0, 1e-6]), d)
            ok = h is not None and h[1] == "light"
            found += ok
            rays.add(Line(P(x), P(q), color=HEAD if ok else GREY_B, stroke_width=3 if ok else 1.8))
        lp = np.array([-3.05, Y1])
        shadow = DashedLine(P(x), P(lp), color=HEAD, stroke_width=3.5, dash_length=0.1)
        ld = Dot(P(lp), radius=0.07, color=HEAD)
        th = VGroup(MathTex(r"\theta", font_size=24, color=GREY_A).move_to(P(x) + np.array([0.15, 0.55, 0])),
                    MathTex(r"\theta'", font_size=24, color=GREY_A).move_to(P(lp) + np.array([0.3, -0.45, 0])),
                    MathTex(r"d", font_size=26, color=HEAD).next_to(shadow.get_center(), RIGHT, buff=0.12))
        cnt = label(rf"{found} of 9 random bounces found the light", font_size=18, color=GREY_A).move_to(
            [-3.3, -3.2, 0])
        ill = note(r"a side view of our box \ (illustrative); \ in 3D the light is $1/16$ of the ceiling",
                   font_size=16).move_to([-3.3, 2.65, 0])
        r0 = MathTex(r"p_A", r"=", r"\frac{1}{A}", font_size=32)
        r1 = MathTex(r"d\omega", r"=", r"\frac{\cos\theta'\, dA}{d^2}", font_size=32)
        r2 = MathTex(r"L_{\text{direct}}", r"\approx", r"f\, L_e\, \frac{\cos\theta\,\cos\theta'}{d^2}\, A\, V",
                     font_size=32, color=YES)
        rows, notes, blk = blocks_of([
            (r0, r"pick a point uniformly on the light, \ area $A$"),
            (r1, r"area on the light, \ seen from $x$, \ as solid angle"),
            (r2, r"$V$: \ 1 if the shadow ray is clear, \ else 0")], buff=0.45)
        twice = wrapped_label(r"then a later bounce that reaches the light by chance adds nothing, \ or that light "
                              r"would be counted twice; \ except after a mirror, \ which a shadow ray cannot aim "
                              r"through", 5.6, font_size=18, color=KERN)
        VGroup(blk, twice).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35).set_y(-0.1)
        n_word = WORDS[found] if found < len(WORDS) else str(found)
        with self.voiceover(
            "Our light is small, a sixteenth of the ceiling. <bookmark mark='a'/> A path that leaves the floor in a "
            f"random direction rarely hits it: here, {n_word} of nine. The paths that do find it are rare and "
            "bright: that is noise. <bookmark mark='b'/> Next-event estimation "
            "aims at the light directly. At every matte vertex, pick a point on the lamp and send a shadow ray "
            "towards it. <bookmark mark='c'/> Converting area on the light to solid angle at the point gives two "
            "cosines over the distance squared. <bookmark mark='d'/> If the shadow ray is clear, add the direct "
            "light. <bookmark mark='e'/> Then, so nothing is counted twice, light that a later bounce reaches by "
            "chance is ignored, except after a mirror, which a shadow ray cannot aim through."
        ) as vo:
            self.play(FadeIn(head), FadeIn(box), FadeIn(ill), FadeIn(xd), FadeIn(xl))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.15), run_time=2)
            self.play(FadeIn(cnt))
            vo.wait_until("b")
            self.play(Create(shadow), FadeIn(ld), FadeIn(r0), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(th), Write(r1), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Write(r2), FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(twice))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ multiple importance sampling
    def mis(self):
        head = label(r"Multiple importance sampling", font_size=36).to_edge(UP, buff=0.3)

        def panel(a, sigma, caption, y):
            ax = Axes(x_range=[-40, 40, 20], y_range=[0, 1.1, 0.5], x_length=5.6, y_length=1.75, tips=False,
                      axis_config={"color": GREY_D, "include_ticks": True}).move_to([-3.5, y, 0])
            th = np.linspace(-40, 40, 321)
            pl = np.where(np.abs(th) <= a, 1 / (2 * a), 0.0)
            pb = np.exp(-th ** 2 / (2 * sigma ** 2)) / (sigma * math.sqrt(2 * PI))
            g = (np.abs(th) <= a) * pb
            top = max(pl.max(), pb.max())
            wl = np.where(pl + pb > 0, pl / (pl + pb + 1e-30), 0)
            curve = lambda v, col, w=3: VMobject(color=col, stroke_width=w).set_points_as_corners(
                [ax.c2p(t, y_) for t, y_ in zip(th, v)])
            area = ax.get_area(ax.plot(lambda t: (abs(t) <= a) * math.exp(-t * t / (2 * sigma * sigma)) /
                                       (sigma * math.sqrt(2 * PI)) / top, x_range=[-40, 40, 0.25]),
                               x_range=[-a, a], color=GREY_B, opacity=0.35)
            ws = VGroup(*[DashedLine(ax.c2p(t0, w0), ax.c2p(t1, w1), color=HEAD, stroke_width=1.6)
                          for t0, t1, w0, w1 in zip(th[::8], th[8::8], wl[::8], wl[8::8]) if w0 > 0 or w1 > 0])
            cap = wrapped_label(caption, 5.6, font_size=18, color=WHITE).next_to(ax, UP, buff=0.08).align_to(
                ax, LEFT)
            return VGroup(ax, area, curve(pl / top, HEAD), curve(pb / top, DATA), ws, cap), g
        A, _ = panel(4, 16, r"small light, \ broad lobe: \ light sampling wins", 1.25)
        Bp, _ = panel(25, 3, r"large light, \ narrow lobe: \ BRDF sampling wins", -1.65)
        leg = VGroup(label(r"light pdf", font_size=16, color=HEAD), label(r"BRDF pdf", font_size=16, color=DATA),
                     label(r"integrand", font_size=16, color=GREY_B),
                     label(r"dashed: \ balance weight of light samples", font_size=16, color=HEAD)).arrange(
            RIGHT, buff=0.3).to_edge(DOWN, buff=0.25).set_x(-3.5)
        ill = note(r"one dimension, \ illustrative", font_size=16).next_to(leg, UP, buff=0.08).set_x(-3.5)
        r0 = MathTex(r"F", r"=", r"\sum_{s} \frac{1}{n_s}\sum_{k=1}^{n_s} w_s(\omega_{s,k})\,"
                     r"\frac{g(\omega_{s,k})}{p_s(\omega_{s,k})}", font_size=30)
        r1 = MathTex(r"\sum_s w_s(\omega) = 1", r"\ \Rightarrow\ ", r"E[F] = \int g\,d\omega", font_size=30)
        r2 = MathTex(r"w_s", r"=", r"\frac{n_s\,p_s}{\sum_t n_t\,p_t}", font_size=30, color=YES)
        rows, notes, blk = blocks_of([
            (r0, r"samples from each strategy $s$: \ the light, \ and the BRDF"),
            (r1, r"unbiased for any weights that sum to one"),
            (r2, r"the balance heuristic; \ the power heuristic squares each term")], buff=0.42)
        veach = wrapped_label(r"Veach and Guibas \ (1995): \ never much worse than the best single strategy \ "
                              r"(measured in chapter 12)", 5.0, font_size=18, color=YES)
        VGroup(blk, veach).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35).set_y(0.0)
        with self.voiceover(
            "Light sampling is not always best. <bookmark mark='a'/> With a small light and a broad lobe it is "
            "ideal: every sample lands where the integrand lives. <bookmark mark='b'/> But with a large light and a "
            "narrow, shiny lobe, most light samples land where the BRDF is nearly zero, and sampling the BRDF is far"
            " better. <bookmark mark='c'/> Eric Veach and Leonidas Guibas showed in 1995 how to use both: draw "
            "samples from each strategy, and weight every sample. <bookmark mark='d'/> If the weights sum to one in "
            "every direction, the combination is unbiased, whatever they are. <bookmark mark='e'/> The balance "
            "heuristic weights a sample by its own strategy's density over the sum of all of them, so each region is"
            " handled mostly by the strategy that samples it best, and Veach proved it is never much worse than the "
            "best single strategy."
        ) as vo:
            self.play(FadeIn(head), FadeIn(leg), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(A[0]), FadeIn(A[5]), Create(A[2]), Create(A[3]), FadeIn(A[1]))
            vo.wait_until("b")
            self.play(FadeIn(Bp[0]), FadeIn(Bp[5]), Create(Bp[2]), Create(Bp[3]), FadeIn(Bp[1]))
            vo.wait_until("c")
            self.play(Write(r0), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(Write(r1), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(Write(r2), FadeIn(notes[2]), Create(A[4]), Create(Bp[4]))
            self.play(FadeIn(veach))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
