from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import (BG, DATA, EYE, HEAD, KERN, LAM, NO, PART, X1, Y0, Y1, YES, P,
                                   box2d, end_of, image, load, path_mob, random_path, to_display,
                                   to_linear)

class Equation(VoiceoverScene):
    def construct(self):
        self.card()
        self.balance()
        self.operator()
        self.paths()
        self.bounces()
        self.decay()

    def card(self):
        card = chapter_card(10, r"The rendering equation", r"Where does all the light in a picture come from?",
                            lit=(1984, 1986), extra=((1984, r"Goral et al.: \ radiosity, \ the Cornell box"),
                                                     (1986, r"Kajiya: \ the rendering equation")), part=PART)
        with self.voiceover("Chapter ten. The rendering equation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ energy balance
    def balance(self):
        head = label(r"Light arriving is light leaving somewhere else", font_size=36).to_edge(UP, buff=0.3)
        box = box2d(eye=False)
        x = np.array([X1, -0.2])
        nx = np.array([-1.0, 0.0])
        xd = Dot(P(x), radius=0.08, color=HEAD)
        xl = MathTex(r"x", font_size=28, color=HEAD).next_to(P(x), RIGHT, buff=0.1)

        def fan_at(p, n, angles, color, width):
            arrows, exits, hits = VGroup(), VGroup(), []
            t = np.array([n[1], -n[0]])
            for a in angles:
                d = math.cos(math.radians(a)) * n + math.sin(math.radians(a)) * t
                q, h = end_of(p + 1e-6 * n, d)
                if h is None:
                    exits.add(DashedLine(P(p), P(q), color=GREY_D, stroke_width=1.2, dash_length=0.06))
                else:
                    arrows.add(Arrow(P(q), P(p), buff=0.05, color=color, stroke_width=width,
                                     max_tip_length_to_length_ratio=0.05))
                    hits.append((q, h))
            return arrows, exits, hits
        fan, exits, srcs = fan_at(x, nx, np.linspace(-75, 75, 11), DATA, 2.5)
        sdots = VGroup(*[Dot(P(q), radius=0.06, color=DATA) for q, h in srcs])
        # the second generation: light arriving at one of those points, on the ceiling
        cq, ch = next((q, h) for q, h in srcs if h[1] == "ceiling")
        fan2, exits2, _ = fan_at(cq, ch[2], np.linspace(-70, 70, 9), LAM, 2)
        ill = note(r"a side view of our box, \ illustrative", font_size=16).move_to([-3.3, 2.65, 0])
        r0 = MathTex(r"L_o(x,\omega_o)", r"=", r"\int_\Omega f\, L_i(x,\omega_i)\cos\theta_i\, d\omega_i",
                     font_size=30)
        r1 = MathTex(r"L_o(x,\omega_o)", r"=", r"L_e(x,\omega_o)", r"+",
                     r"\int_\Omega f\, L_i(x,\omega_i)\cos\theta_i\, d\omega_i", font_size=30)
        r2 = MathTex(r"L_i(x,\omega_i)", r"=", r"L_o(r(x,\omega_i),\,-\omega_i)", font_size=30)
        r3 = MathTex(r"L(x,\omega_o)", r"=", r"L_e(x,\omega_o)", r"+",
                     r"\int_\Omega f\, L(r(x,\omega_i),-\omega_i)\cos\theta_i\, d\omega_i", font_size=30,
                     color=YES)
        notes = VGroup(note(r"chapter 9's reflection equation", font_size=17),
                       note(r"plus what the point itself emits", font_size=17),
                       note(r"$r(x,\omega)$: \ the first surface a ray from $x$ meets \ (chapters 7 and 8)",
                            font_size=17),
                       note(r"the unknown $L$ on both sides: \ Kajiya \ (1986)", font_size=17, color=YES))
        blocks = VGroup(*[VGroup(r, n).arrange(DOWN, aligned_edge=LEFT, buff=0.07) for r, n in
                          zip((r0, r1, r2, r3), notes)]).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
        blocks.to_edge(RIGHT, buff=0.3).set_y(-0.1)
        with self.voiceover(
            "Chapter nine's reflection equation needs the light arriving at a point. <bookmark mark='a'/> Take a "
            "point on the back wall. Light arrives from every direction in front of it. <bookmark mark='b'/> But "
            "each arrival is light leaving some other surface: the ceiling, the lamp, the two balls, or nothing at "
            "all through the open front. <bookmark mark='c'/> And what leaves that surface depends in turn on "
            "everything arriving there. <bookmark mark='d'/> Write it down. The light leaving a point is what it "
            "emits, plus what it reflects. <bookmark mark='e'/> The light arriving from a direction is the light "
            "leaving the first surface a ray meets that way, the job of chapters seven and eight. <bookmark "
            "mark='f'/> Substitute, and the unknown radiance appears on both sides. This is the rendering equation, "
            "published by James Kajiya in 1986: a balance of energy at every point and in every direction."
        ) as vo:
            self.play(FadeIn(head), FadeIn(box), FadeIn(ill), Write(r0), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(xd), FadeIn(xl), FadeIn(exits), LaggedStart(*[GrowArrow(a) for a in fan],
                                                                         lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(sdots))
            vo.wait_until("c")
            self.play(FadeIn(exits2), LaggedStart(*[GrowArrow(a) for a in fan2], lag_ratio=0.1))
            vo.wait_until("d")
            self.play(TransformMatchingTex(r0.copy(), r1), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(Write(r2), FadeIn(notes[2]))
            vo.wait_until("f")
            self.play(TransformMatchingTex(r1.copy(), r3), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ operator form and the Neumann series
    def operator(self):
        head = label(r"Solving it: \ the Neumann series", font_size=36).to_edge(UP, buff=0.3)
        r0 = MathTex(r"(TL)(x,\omega_o) = \int_\Omega f\, L(r(x,\omega_i),-\omega_i)\cos\theta_i\, d\omega_i",
                     font_size=32)
        n0 = note(r"$T$: \ cast a ray, \ look up the light there, \ weight, \ integrate", font_size=17)
        steps = [MathTex(r"L", r"=", r"L_e", r"+", r"T", r"L", font_size=40),
                 MathTex(r"(I", r"-", r"T)", r"L", r"=", r"L_e", font_size=40),
                 MathTex(r"L", r"=", r"(I", r"-", r"T)^{-1}", r"L_e", font_size=40),
                 MathTex(r"L", r"=", r"L_e", r"+", r"T L_e", r"+", r"T^2 L_e", r"+", r"T^3 L_e", r"+", r"\cdots",
                         font_size=40)]
        top = VGroup(r0, n0).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        top.move_to([-2.6, 2.1, 0])
        for s in steps:
            s.move_to([-2.6, 0.75, 0])
        steps[3].set_color_by_tex("T", YES)
        geo = MathTex(r"\frac{1}{1-x} = 1 + x + x^2 + x^3 + \cdots,\quad |x| < 1", font_size=32, color=GREY_A)
        geo.move_to([-2.6, -0.45, 0])
        rho = 0.73
        segs = VGroup()
        xcur, s = -6.3, 1.25
        cols = [HEAD, YES, DATA, LAM, KERN]
        for k in range(14):
            w = s * rho ** k
            segs.add(Rectangle(width=w, height=0.5, stroke_width=1, stroke_color=BG, fill_color=cols[k % 5],
                               fill_opacity=0.85).move_to([xcur + w / 2, -2.05, 0]))
            xcur += w
        segl = VGroup(*[label(t, font_size=16, color=BLACK).move_to(segs[k]) for k, t in
                        enumerate((r"$L_e$", r"$TL_e$", r"$T^2L_e$"))])
        total = 1 / (1 - rho)
        brace = Brace(segs, DOWN, buff=0.08, color=GREY_B)
        bl = label(rf"$1 + {rho} + {rho}^2 + \cdots = 1/(1 - {rho}) = {total:.2f}$", font_size=20,
                   color=WHITE).next_to(brace, DOWN, buff=0.1)
        notes = VGroup(
            wrapped_label(r"converges because $T$ shrinks every light field: \ each reflection keeps at most its "
                          r"albedo \ (chapter 9's furnace)", 4.9, font_size=19, color=WHITE),
            wrapped_label(rf"with albedo {rho}, \ our white walls, \ each bounce keeps {100 * rho:.0f}\%: \ the "
                          rf"bounces add up to {total:.2f} times the light emitted", 4.9, font_size=19, color=HEAD),
            wrapped_label(r"a closed room of such walls; \ a real scene loses light to black surfaces and open "
                          r"sides, \ so it converges faster", 4.9, font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).set_y(-0.6)
        with self.voiceover(
            "Name the integral as an operator. <bookmark mark='a'/> T takes a field of radiance and returns the "
            "light reflected once: cast a ray, look up the radiance there, weight it by the BRDF and the cosine, and"
            " integrate. The equation becomes L equals L e plus T L. <bookmark mark='b'/> Move T L across, and "
            "invert. <bookmark mark='c'/> Then expand as a geometric series, exactly as one over one minus x is one "
            "plus x plus x squared. <bookmark mark='d'/> This Neumann series converges when T shrinks every field, "
            "and chapter nine's furnace guarantees it: each reflection keeps at most its albedo. <bookmark "
            "mark='e'/> In a closed room with walls of albedo nought point seven three, our white walls, each bounce"
            " keeps seventy-three per cent, and the bounces add up to three point seven times the light emitted."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(r0), FadeIn(n0))
            self.play(Write(steps[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(steps[0], steps[1]))
            self.play(TransformMatchingTex(steps[1], steps[2]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(steps[2], steps[3]), FadeIn(geo))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(LaggedStart(*[GrowFromEdge(r, LEFT) for r in segs], lag_ratio=0.25), run_time=3)
            self.play(FadeIn(segl), GrowFromCenter(brace), FadeIn(bl), FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the terms as paths
    def paths(self):
        head = label(r"Each term is a set of paths", font_size=36).to_edge(UP, buff=0.3)
        box = box2d()
        lc = np.array([-3.3, Y1])
        p0 = [EYE, lc]
        p1 = [EYE, np.array([-4.8, Y0]), lc]
        d = np.array([-3.3, -1.45]) - EYE                    # aimed so the mirror reflects it into the light
        pm, _ = random_path(EYE, d / np.linalg.norm(d), np.random.default_rng(0), max_b=3)
        p2 = [EYE, np.array([X1, 1.2]), np.array([-5.4, Y0]), lc]
        m0 = path_mob(p0, HEAD)
        m1 = VGroup(path_mob(p1, YES), path_mob(pm, YES))
        m2 = path_mob(p2, DATA)
        ill = note(r"a side view of our box, \ illustrative", font_size=16).move_to([-3.3, 2.65, 0])
        terms = [(r"L_e", HEAD, r"light straight from the lamp into the eye"),
                 (r"T L_e", YES, r"one reflection: \ direct lighting, \ off the floor or via the mirror"),
                 (r"T^2 L_e", DATA, r"two reflections: \ back wall, \ then floor"),
                 (r"T^k L_e", LAM, r"$k$ reflections: \ an integral over all paths of that length")]
        rows = VGroup()
        for tex, col, txt in terms:
            m = MathTex(tex, font_size=36, color=col)
            n = wrapped_label(txt, 3.9, font_size=19, color=WHITE)
            rows.add(VGroup(m, n.next_to(m, RIGHT, buff=0.3, aligned_edge=UP)))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.4).set_y(0.5)
        left = rows.get_left()[0]
        for r in rows:
            r[1].set_x(left + 1.35, LEFT)
        rows.shift(LEFT * max(0.0, rows.get_right()[0] - 6.75))
        foot = wrapped_label(r"the picture is the sum over all path lengths: \ Veach \ (1997) \ wrote the whole "
                             r"equation as one integral over paths", 6.0, font_size=19, color=GREY_A).to_edge(
            DOWN, buff=0.35).set_x(3.6)
        with self.voiceover(
            "Each term of the series has a picture. <bookmark mark='a'/> L e alone is light that goes from the lamp "
            "straight into the eye. <bookmark mark='b'/> T L e is light that reflected once on its way to us: off "
            "the floor, or off the mirror ball. This is direct lighting. <bookmark mark='c'/> T squared L e is light "
            "that bounced twice, from the back wall onto the floor and then to the eye. <bookmark mark='d'/> Each "
            "term is an integral over every path with that many reflections, and the picture is the sum over all "
            "lengths. Eric Veach's thesis of 1997 wrote the whole equation as a single integral over paths, which "
            "is the form the next chapter samples."
        ) as vo:
            self.play(FadeIn(head), FadeIn(box), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(m0), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(m1), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(Create(m2), FadeIn(rows[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the bounce-by-bounce sum
    def bounces(self):
        p = load("path")
        lin = [to_linear(p[f"bounce{k}"]) for k in range(8)]
        partial = [to_display(sum(lin[:k + 1])) for k in range(8)]
        head = label(r"The series, \ summed on screen", font_size=36).to_edge(UP, buff=0.3)
        big_pos = np.array([-3.65, -0.25, 0])
        thumbs = Group()
        for k in range(8):
            t = image(p[f"bounce{k}"], height=1.45)
            cap = label(rf"bounce {k}" if k < 7 else r"bounce 7 and up", font_size=16, color=GREY_A).next_to(
                t, DOWN, buff=0.08)
            thumbs.add(Group(t, cap))
        thumbs.arrange_in_grid(rows=2, cols=4, buff=(0.2, 0.3)).move_to([3.55, 0.75, 0])
        caps = [label(rf"the sum so far: \ bounce 0" if k == 0 else rf"the sum so far: \ bounces 0 to {k}",
                      font_size=20, color=HEAD) for k in range(8)]
        series = MathTex(r"L", r"=", r"L_e", r"+", r"T L_e", r"+", r"T^2 L_e", r"+", r"T^3 L_e", r"+", r"\cdots",
                         font_size=36).move_to([3.55, -2.35, 0])
        hi = [series[2], series[4], series[6], series[8], series[10]]
        src = note(r"our path tracer, \ 128 $\times$ 128, \ 2048 paths per pixel, \ each path's light filed by "
                   r"its number of reflections", font_size=16).to_edge(DOWN, buff=0.2)
        cur = None
        marks = {0: "a", 1: "b", 2: "c", 3: "d"}
        with self.voiceover(
            "Our path tracer records each path's light by the number of reflections it took, so we can watch the "
            "series add up, term by term, in our own scene. <bookmark mark='a'/> Bounce zero: only the lamp. "
            "<bookmark mark='b'/> Add bounce one, direct lighting. The floor and walls are lit, the balls cast "
            "shadows, and the mirror shows the walls; but the ceiling is black, because no light reaches it "
            "directly. <bookmark mark='c'/> Add bounce two. The ceiling appears, the shadows soften, and red and "
            "green light spills onto the white surfaces. <bookmark mark='d'/> Three, four, five and beyond: each "
            "adds less, and the picture settles into the converged image. <bookmark mark='e'/> Nothing here was "
            "painted on. Soft shadows and colour bleeding are simply the later terms of the series."
        ) as vo:
            slots = VGroup(*[Rectangle(width=t[0].width, height=t[0].height, color=GREY_D, stroke_width=1.2)
                             .move_to(t[0]) for t in thumbs],
                           Rectangle(width=4.6, height=4.6, color=GREY_D, stroke_width=1.2).move_to(big_pos))
            self.play(FadeIn(head), FadeIn(series), FadeIn(src), FadeIn(slots))
            for k in range(8):
                if k in marks:
                    vo.wait_until(marks[k])
                new = image(partial[k], height=4.6).move_to(big_pos)
                cap = caps[k].next_to(new, DOWN, buff=0.15)
                anims = [FadeIn(thumbs[k]), FadeIn(new), FadeIn(cap)]
                if cur is not None:
                    anims += [FadeOut(cur[0]), FadeOut(cur[1])]
                hk = hi[min(k, 4)]
                anims.append(hk.animate.set_color(HEAD))
                self.play(*anims, run_time=1.0 if k < 3 else 0.6)
                self.play(hk.animate.set_color(WHITE), run_time=0.3)
                cur = (new, cap)
            vo.wait_until("e")
            self.play(Indicate(cur[0], scale_factor=1.03, color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ how fast the terms shrink
    def decay(self):
        p = load("path")
        bm = p["bounce_mean"]
        ref_mean = p["convergence"]["ref_mean"]
        head = label(r"Each bounce keeps about half", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 7, 1], y_range=[0, 3, 1], x_length=5.6, y_length=4.0, tips=False,
                  axis_config={"color": GREY_D, "include_ticks": True}).move_to([-3.3, 0.0, 0])
        xt = VGroup(*[label(f"{k}" if k < 7 else r"7+", font_size=17, color=GREY_B).next_to(
            ax.c2p(k, 0), DOWN, buff=0.1) for k in range(8)])
        yt = VGroup(*[label(t, font_size=17, color=GREY_B).next_to(ax.c2p(0, v + 3), LEFT, buff=0.1)
                      for v, t in ((-3, "0.001"), (-2, "0.01"), (-1, "0.1"), (0, "1"))])
        xl = label(r"number of reflections", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"mean radiance of the bounce image \ (log scale)", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT)
        pts = [ax.c2p(k, math.log10(v) + 3) for k, v in enumerate(bm)]
        line = VMobject(color=HEAD, stroke_width=3).set_points_as_corners(pts[:7])
        dots = VGroup(*[Dot(q, radius=0.07, color=HEAD if k < 7 else GREY_B) for k, q in enumerate(pts)])
        vals = VGroup(*[label(f"{v:.3f}", font_size=16, color=GREY_A).next_to(q, UR, buff=0.04)
                        for v, q in zip(bm[:4], pts[:4])])
        ratios = [b / a for a, b in zip(bm[1:6], bm[2:7])]
        indirect = (ref_mean - bm[0] - bm[1]) / (ref_mean - bm[0])
        bar_w = 5.0
        bx = 4.0
        b1 = Rectangle(width=bar_w * (1 - indirect), height=0.45, stroke_width=0, fill_color=YES, fill_opacity=0.85)
        b2 = Rectangle(width=bar_w * indirect, height=0.45, stroke_width=0, fill_color=DATA, fill_opacity=0.85)
        bars = VGroup(b1, b2).arrange(RIGHT, buff=0).move_to([bx, -1.35, 0])
        bl = VGroup(label(rf"direct {100 * (1 - indirect):.0f}\%", font_size=17, color=BLACK).move_to(b1),
                    label(rf"indirect {100 * indirect:.0f}\%", font_size=17, color=BLACK).move_to(b2))
        bcap = label(r"light reaching the eye from surfaces", font_size=17, color=GREY_A).next_to(bars, UP,
                                                                                                buff=0.1)
        notes = VGroup(
            wrapped_label(rf"from bounce 1 on, \ each term is {min(ratios):.2f} to {max(ratios):.2f} times the one "
                          r"before: \ a geometric series, \ as the operator predicts", 5.3, font_size=19,
                          color=HEAD),
            wrapped_label(rf"the eight bounce images add up to the reference's mean, \ {ref_mean:.4f}, \ "
                          rf"exactly", 5.3, font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([bx, 1.3, 0])
        foot = wrapped_label(r"stopping after direct light \ (Whitted, \ chapter 7) \ loses the indirect share; \ "
                             r"Goral et al. \ (1984) \ computed it for matte surfaces as radiosity", 5.3,
                             font_size=18, color=GREY_A).move_to([bx, -2.75, 0])
        with self.voiceover(
            "How fast do the terms shrink? <bookmark mark='a'/> On a logarithmic scale the mean brightness of each "
            "bounce image falls on a nearly straight line. <bookmark mark='b'/> From the first bounce on, each term "
            "is between nought point three eight and nought point five three times the one before: a geometric "
            "series, as the operator view predicted. The light lost at each bounce is absorbed by the coloured "
            "walls, or escapes through the open front. <bookmark mark='c'/> The eight images add up exactly to the "
            "converged image. <bookmark mark='d'/> And the later terms matter: of the light that reaches the eye "
            "from surfaces, forty-three per cent took two or more bounces. A renderer that stops at direct light "
            "loses all of it; the radiosity method of 1984 computed it for matte surfaces, and path tracing "
            "computes it for everything."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(dots), FadeIn(vals), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(bcap), GrowFromEdge(b1, LEFT), GrowFromEdge(b2, LEFT), FadeIn(bl), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
