from __future__ import annotations

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, image, load, module_box


def edge_fn(a, b, p):
    """The edge function of Part 22: twice the signed area of (a, b, p)."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


class Raster(VoiceoverScene):
    def construct(self):
        self.card()
        self.edges()
        self.bary()
        self.whyw()
        self.persp()
        self.zbuffer()
        self.ours()

    def card(self):
        card = chapter_card(3, r"Rasterization and the z-buffer", r"Which pixels does a triangle cover, \ and which "
                            r"triangle wins?", lit=(1974, 1988), extra=((1974, r"Catmull: \ the z-buffer"),
                                                                       (1988, r"Pineda: \ edge functions")),
                            part=PART)
        with self.voiceover("Chapter three. Rasterization and the z-buffer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def edges(self):
        b = load("bary")
        ctr = b["counters"]
        head = label(r"Edge functions: \ inside is three signs", font_size=36).to_edge(UP, buff=0.3)
        cols, rows, cell = 20, 15, 0.3
        x0, y0 = -6.4, 1.9

        def S(x, y):
            return np.array([x0 + x * cell, y0 - y * cell, 0.0])
        grid = VGroup(*[Square(cell, stroke_color=GREY_D, stroke_width=0.8).move_to(S(i + 0.5, j + 0.5))
                        for j in range(rows) for i in range(cols)])
        V = [np.array(v) / 8 for v in b["vertices"]]            # our triangle, at one eighth of the resolution
        tri = Polygon(*[S(*v) for v in V], color=WHITE, stroke_width=2.5)
        sgn = np.sign(edge_fn(V[0], V[1], V[2]))
        centres = [(i + 0.5, j + 0.5) for j in range(rows) for i in range(cols)]
        dots = VGroup(*[Dot(S(*c), radius=0.035, color=GREY_B) for c in centres])
        inside = np.ones(len(centres), bool)
        steps = []
        for k, (p, q) in enumerate(((V[1], V[2]), (V[2], V[0]), (V[0], V[1]))):
            ok = np.array([sgn * edge_fn(p, q, c) > 0 for c in centres])
            newly = inside & ~ok
            inside &= ok
            steps.append((Line(S(*p), S(*q), color=(DATA, LAM, KERN)[k], stroke_width=6), np.where(newly)[0]))
        fill = VGroup(*[grid[i].copy().set_fill(HEAD, 0.55).set_stroke(width=0) for i in np.where(inside)[0]])
        ill = note(r"the triangle of the next slide, \ at one eighth of the resolution", font_size=16).next_to(
            grid, DOWN, buff=0.12)
        form = MathTex(r"E_{ab}(p)", r"=", r"(b - a) \times (p - a)", font_size=36).move_to([3.5, 2.2, 0])
        form[0].set_color(HEAD)
        notes = VGroup(
            wrapped_label(r"twice the signed area of the triangle $a, b, p$: \ Part 22's orientation test", 5.6,
                          font_size=19, color=WHITE),
            wrapped_label(r"a pixel centre is inside when all three edge functions have the triangle's sign; \ "
                          r"centres exactly on an edge go to one triangle only \ (the top-left rule)", 5.6,
                          font_size=19, color=YES),
            wrapped_label(r"$E$ is affine in $p$: \ one step right adds a constant, \ so hardware tests many pixels "
                          r"in parallel \ (Pineda 1988)", 5.6, font_size=19, color=HEAD),
            wrapped_label(rf"our rasterizer at 160 $\times$ 120: \ {ctr['tested']:,} pixels of the bounding box "
                          rf"tested, \ {ctr['covered']:,} inside".replace(",", "{,}"), 5.6, font_size=19,
                          color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(form, DOWN, buff=0.4)
        with self.voiceover(
            "Which pixels does a triangle cover? <bookmark mark='a'/> For an edge from a to b, take the cross "
            "product of the edge with the vector to a point p: twice the signed area of the triangle a, b, p, "
            "Part 22's orientation test, telling which side of the edge p is on. <bookmark mark='b'/> Test every "
            "pixel centre against the three edges in turn. A centre on the wrong side of any edge is out; the rest "
            "are in, and a tie-breaking rule gives a centre exactly on a shared edge to one triangle only. "
            "<bookmark mark='c'/> Each edge function is affine, so one pixel to the right adds a constant, and "
            "hardware tests whole blocks at once. <bookmark mark='d'/> About half the bounding box was inside."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid), FadeIn(dots), Create(tri), FadeIn(ill))
            vo.wait_until("a")
            self.play(Write(form), FadeIn(notes[0]))
            vo.wait_until("b")
            for ln, out in steps:
                self.play(Create(ln), *[dots[i].animate.set_color(NO) for i in out], run_time=1.2)
            self.play(FadeIn(fill), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def bary(self):
        b = load("bary")
        head = label(r"Barycentric coordinates", font_size=36).to_edge(UP, buff=0.3)
        sc = 0.042
        V = [np.array([-6.4 + x * sc, 1.9 - y * sc, 0.0]) for x, y in b["vertices"]]
        cols = (NO, YES, DATA)
        tri = Polygon(*V, color=WHITE, stroke_width=2.5)
        names = VGroup(*[MathTex(n, font_size=32, color=c) for n, c in zip("abc", cols)])
        names[0].next_to(V[0], DL, buff=0.08)
        names[1].next_to(V[1], DR, buff=0.08)
        names[2].next_to(V[2], UP, buff=0.08)
        way = [(1 / 3, 1 / 3, 1 / 3), (0.7, 0.18, 0.12), (0.15, 0.7, 0.15), (0.12, 0.18, 0.7), (1 / 3, 1 / 3, 1 / 3)]
        u = ValueTracker(0.0)

        def lam():
            v = u.get_value() * (len(way) - 1)
            k = min(int(v), len(way) - 2)
            f = v - k
            return (1 - f) * np.array(way[k]) + f * np.array(way[k + 1])

        def P():
            lm = lam()
            return lm[0] * V[0] + lm[1] * V[1] + lm[2] * V[2]
        subs = always_redraw(lambda: VGroup(
            Polygon(P(), V[1], V[2], stroke_width=1, stroke_color=GREY_B, fill_color=NO, fill_opacity=0.3),
            Polygon(V[0], P(), V[2], stroke_width=1, stroke_color=GREY_B, fill_color=YES, fill_opacity=0.3),
            Polygon(V[0], V[1], P(), stroke_width=1, stroke_color=GREY_B, fill_color=DATA, fill_opacity=0.3)))
        dot = always_redraw(lambda: Dot(P(), radius=0.11, color=ManimColor.from_rgb(tuple(lam()))).set_stroke(
            WHITE, 1.5))
        pl = always_redraw(lambda: MathTex(r"p", font_size=30).next_to(P(), UR, buff=0.05))
        reads = VGroup()
        for k, (n, c) in enumerate(zip("abc", cols)):
            t = MathTex(rf"\lambda_{n} =", font_size=30, color=c)
            num = DecimalNumber(0.333, num_decimal_places=2, font_size=30, color=c)
            num.add_updater(lambda m, k=k: m.set_value(lam()[k]))
            reads.add(VGroup(t, num).arrange(RIGHT, buff=0.12))
        reads.arrange(RIGHT, buff=0.5).move_to([-3.6, -2.95, 0])
        for g in reads:
            g[1].add_updater(lambda m, g=g: m.next_to(g[0], RIGHT, buff=0.12))
        rows = VGroup(
            MathTex(r"\lambda_a = \frac{E_{bc}(p)}{E_{ab}(c)}", r",\ ", r"\lambda_a + \lambda_b + \lambda_c = 1",
                    font_size=32),
            MathTex(r"p = \lambda_a a + \lambda_b b + \lambda_c c", font_size=32),
            MathTex(r"\text{colour}(p) = \lambda_a\,\text{red} + \lambda_b\,\text{green} + \lambda_c\,\text{blue}",
                    font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, 2.0, 0])
        img = image(b["image"], height=2.4).next_to(rows, DOWN, buff=0.35)
        cap = wrapped_label(rf"our rasterizer: \ {b['counters']['covered']:,} pixels, \ each coloured by its "
                            r"barycentric coordinates".replace(",", "{,}"), 5.4, font_size=18,
                            color=GREY_A).next_to(img, DOWN, buff=0.12)
        with self.voiceover(
            "Once a pixel is inside, we need its colour, its depth, its texture position: values given only at the "
            "three corners. <bookmark mark='a'/> A point p splits the triangle into three smaller ones. The share of "
            "the area opposite each corner is that corner's weight, lambda, and the three weights add to one. "
            "<bookmark mark='b'/> Move p around and watch: near a corner, that corner's weight approaches one. "
            "These are barycentric coordinates, from August Möbius in 1827 again, and they come free from the edge "
            "functions we already computed. <bookmark mark='c'/> Any value at the corners is blended with the same "
            "weights. <bookmark mark='d'/> Give the corners pure red, green and blue, and our rasterizer paints "
            "the weights themselves."
        ) as vo:
            self.play(FadeIn(head), Create(tri), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(subs), FadeIn(dot), FadeIn(pl), FadeIn(reads), Write(rows[0]))
            vo.wait_until("b")
            self.play(u.animate.set_value(1.0), run_time=7, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(img), FadeIn(cap))
        for g in reads:
            g[1].clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def whyw(self):
        head = label(r"Why interpolate $1/w$", font_size=36).to_edge(UP, buff=0.3)
        E = np.array([-6.3, 1.4, 0])
        H, n = 3.2, 1.6
        fy = E[1] - H
        floor = Line([-6.6, fy, 0], [0.5, fy, 0], color=GREY_C, stroke_width=2)
        screen = Line(E + RIGHT * n + DOWN * 2.4, E + RIGHT * n + UP * 0.2, color=DATA, stroke_width=4)
        eye = Dot(E, radius=0.09, color=WHITE)
        hs = np.linspace(2.2, 0.8, 5)
        sp = [E + RIGHT * n + DOWN * h for h in hs]
        fp = [np.array([E[0] + n * H / h, fy, 0]) for h in hs]
        rays = VGroup(*[DashedLine(E, f, color=GREY_B, stroke_width=1.5) for f in fp])
        sdots = VGroup(*[Dot(p, radius=0.06, color=HEAD) for p in sp])
        fdots = VGroup(*[Dot(p, radius=0.07, color=HEAD) for p in fp])
        mid_true = Dot((fp[0] + fp[-1]) / 2, radius=0.1, color=YES)
        mt = label(r"halfway along the floor", font_size=17, color=YES).next_to(mid_true, DOWN, buff=0.2).align_to(
            mid_true, LEFT)
        ring = Circle(radius=0.14, color=NO, stroke_width=3).move_to(fp[2])
        mr = label(r"halfway on screen", font_size=17, color=NO).next_to(ring, DOWN, buff=0.2).align_to(ring, RIGHT)
        lab = VGroup(label(r"screen", font_size=18, color=DATA).next_to(screen, UP, buff=0.1),
                     label(r"floor", font_size=18, color=GREY_A).next_to(floor, DOWN, buff=0.1).align_to(floor, RIGHT))
        cap = note(r"equal steps on the screen, \ growing steps on the floor", font_size=17).move_to([-3.2, -3.0, 0])
        rows = VGroup(
            MathTex(r"u", r"=", r"(1-s)\,u_0 + s\,u_1", font_size=34),
            MathTex(r"\frac{u}{w}", r"=", r"(1-s)\,\frac{u_0}{w_0} + s\,\frac{u_1}{w_1}", font_size=34),
            MathTex(r"\frac{1}{w}", r"=", r"(1-s)\,\frac{1}{w_0} + s\,\frac{1}{w_1}", font_size=34),
            MathTex(r"u", r"=", r"\frac{\sum_i \lambda_i\, u_i / w_i}{\sum_i \lambda_i / w_i}", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([4.0, 0.3, 0])
        cross = Line(rows[0].get_left() + LEFT * 0.1, rows[0].get_right() + RIGHT * 0.1, color=NO, stroke_width=4)
        whys = VGroup(note(r"wrong: \ $s$ is a fraction of the screen", font_size=17, color=NO),
                      note(r"affine in screen position", font_size=17),
                      note(r"so is this: \ divide the plane's equation by depth", font_size=17),
                      note(r"divide; \ $\lambda_i$ are the barycentrics", font_size=17, color=YES))
        for r, w in zip(rows, whys):
            w.next_to(r, DOWN, buff=0.06).align_to(r, LEFT)
        with self.voiceover(
            "There is a catch, and it is perspective. <bookmark mark='a'/> Equal steps across the screen are not "
            "equal steps across a floor that recedes from the eye. The point halfway between two vertices on the "
            "screen is much nearer than the point halfway along the floor. <bookmark mark='b'/> So blending a "
            "texture coordinate by screen fractions is wrong. <bookmark mark='c'/> What is right? On a flat "
            "triangle, one over the depth is an affine function of screen position: divide the plane's equation by "
            "depth to see it. So is any attribute divided by depth. <bookmark mark='d'/> So interpolate u over w "
            "and one over w, both linearly, <bookmark mark='e'/> and divide one by the other at every pixel. That "
            "division is perspective-correct interpolation."
        ) as vo:
            self.play(FadeIn(head), Create(floor), Create(screen), FadeIn(eye), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(sdots), Create(rays), FadeIn(fdots), FadeIn(cap), run_time=2)
            self.play(FadeIn(mid_true), FadeIn(mt), Create(ring), FadeIn(mr))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            self.play(Create(cross))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            self.play(Circumscribe(rows[3], color=YES))
        self.wait(0.4)
        self.clear_scene()

    def persp(self):
        p = load("persp")
        head = label(r"A floor, \ three ways", font_size=36).to_edge(UP, buff=0.3)
        imgs = Group(*[image(p[k], height=2.9) for k in ("affine", "perspective", "truth")]).arrange(RIGHT, buff=0.3)
        imgs.next_to(head, DOWN, buff=0.45)
        caps = VGroup(
            label(rf"affine: \ {100 * p['wrong_affine']:.1f}\% of pixels wrong", font_size=20, color=NO),
            label(rf"with $1/w$: \ {100 * p['wrong_perspective']:.1f}\% wrong", font_size=20, color=YES),
            label(r"ray cast: \ the truth", font_size=20, color=GREY_A),
        )
        for c, im in zip(caps, imgs):
            c.next_to(im, DOWN, buff=0.15)
        e = p["uv_error_max"]
        m, ex = f"{e:.1e}".split("e")
        notes = VGroup(
            wrapped_label(rf"two triangles, \ {p['floor_pixels']:,} floor pixels; \ our rasterizer's texture "
                          rf"coordinates agree with the ray cast to ${m} \times 10^{{{int(ex)}}}$, \ rounding error "
                          r"\ (Part 4)".replace(",", "{,}", 1), 12.4, font_size=20, color=WHITE),
            wrapped_label(r"the original PlayStation \ (1994) \ interpolated textures affinely: \ its textures bent "
                          r"and swam as the camera moved", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Here is the difference, from our own rasterizer. <bookmark mark='a'/> A checkered floor made of two "
            "triangles, with texture coordinates interpolated affinely: the squares bend along the diagonal where "
            "the triangles meet, and almost half of the floor's pixels get the wrong colour. "
            "<bookmark mark='b'/> With one over w, every pixel is right. <bookmark mark='c'/> And against a ray "
            "cast of the true floor, the texture coordinates agree to rounding error. <bookmark mark='d'/> The "
            "original PlayStation, in 1994, skipped this division, and its textures famously wobbled."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(imgs[0]), FadeIn(caps[0]))
            vo.wait_until("b")
            self.play(FadeIn(imgs[1]), FadeIn(caps[1]))
            vo.wait_until("c")
            self.play(FadeIn(imgs[2]), FadeIn(caps[2]), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def zbuffer(self):
        z = load("zbuffer")
        cz = z["counters_zbuffer"]
        head = label(r"The z-buffer", font_size=36).to_edge(UP, buff=0.3)
        a = image(z["painter"], height=2.8)
        b = image(z["zbuffer"], height=2.8)
        Group(a, b).arrange(RIGHT, buff=0.35).to_edge(LEFT, buff=0.4).shift(UP * 0.6)
        ca = label(rf"painter's order: \ {z['painter_wrong']} pixels wrong", font_size=19, color=NO).next_to(
            a, DOWN, buff=0.15)
        cb = label(rf"z-buffer: \ {z['zbuffer_wrong']} pixel{'' if z['zbuffer_wrong'] == 1 else 's'} wrong", font_size=19, color=YES).next_to(b, DOWN,
                                                                                                      buff=0.15)
        code = code_block(["for each fragment (x, y, z, c):", "  if z < depth[y][x]:", "    depth[y][x] = z",
                           "    colour[y][x] = c"], size=17).to_edge(RIGHT, buff=0.45).shift(UP * 1.6)
        cl = note(r"cleared to 1, \ the far plane", font_size=17).next_to(code, DOWN, buff=0.15).align_to(code, LEFT)
        notes = VGroup(
            wrapped_label(rf"two triangles that pass through each other: \ in the {z['overlap']:,} pixels where both "
                          rf"are drawn, \ the orange one is in front in {z['a_in_front']} and the blue one in "
                          rf"{z['b_in_front']}".replace(",", "{,}", 1), 12.4, font_size=20, color=WHITE),
            wrapped_label(r"sorting whole triangles by depth puts the blue one behind and paints over it everywhere; "
                          r"\ no order is right, \ but a depth per pixel is", 12.4, font_size=20, color=NO),
            wrapped_label(rf"z-buffer: \ {cz['depth_pass']:,} fragments passed the test, \ {cz['depth_fail']:,} "
                          r"failed; \ its one disagreement with the ray cast is a pixel on a triangle's outer edge, \ a "
                          r"coverage tie, \ not a visibility error"
                          .replace(",", "{,}"), 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now visibility: which of two overlapping triangles do we see? <bookmark mark='a'/> These two pass "
            "through each other, so each is in front over part of the overlap. <bookmark mark='b'/> The painter's "
            "algorithm sorts whole triangles from back to front. The blue one is farther on average, so it is "
            "painted first and covered everywhere: four hundred and seventy-two pixels wrong. No order of whole "
            "triangles can be right. <bookmark mark='c'/> Ed Catmull's answer, in 1974, was a depth for every "
            "pixel: a fragment is written only if it is nearer than what is there. <bookmark mark='d'/> The result "
            "is right in any drawing order, for one number per pixel, a price steep in 1974 and trivial today."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(b))
            vo.wait_until("b")
            self.play(FadeIn(a), FadeIn(ca), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(code), FadeIn(cl))
            vo.wait_until("d")
            self.play(FadeIn(cb), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def ours(self):
        head = label(r"Our rasterizer, \ end to end", font_size=36).to_edge(UP, buff=0.3)
        steps = [(r"clip coordinates", DATA), (r"clip near plane", KERN), (r"divide by $w$", HEAD),
                 (r"viewport", DATA), (r"edge functions", KERN), (r"depth test", YES),
                 (r"interpolate $a/w$, \ $1/w$", HEAD), (r"write pixel", DATA)]
        boxes = VGroup(*[module_box(t, c, w=2.6, h=0.7, font=19) for t, c in steps])
        top, bot = boxes[:4], VGroup(*boxes[4:][::-1])          # a snake: the second row runs right to left
        top.arrange(RIGHT, buff=0.55)
        bot.arrange(RIGHT, buff=0.55)
        VGroup(top, bot).arrange(DOWN, buff=0.9).next_to(head, DOWN, buff=0.6)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.05, stroke_width=2,
                                color=GREY_B, max_tip_length_to_length_ratio=0.25) for i in (0, 1, 2)],
                        *[Arrow(boxes[i].get_left(), boxes[i + 1].get_right(), buff=0.05, stroke_width=2,
                                color=GREY_B, max_tip_length_to_length_ratio=0.25) for i in (4, 5, 6)])
        arrows.add(Arrow(boxes[3].get_bottom(), boxes[4].get_top(), buff=0.05, stroke_width=2, color=GREY_B,
                         max_tip_length_to_length_ratio=0.12))
        notes = VGroup(
            wrapped_label(r"clipping happens in homogeneous space, \ before the division, \ so nothing behind the eye "
                          r"is ever divided by a negative $w$ \ (Sutherland and Hodgman, \ 1974)", 12.4,
                          font_size=20, color=KERN),
            wrapped_label(r"vertices are snapped to $1/256$ of a pixel, \ as GPUs do, \ so the edge functions are "
                          r"computed exactly and two triangles sharing an edge never both own, \ or both miss, \ a "
                          r"pixel on it", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"every image in this chapter, \ and the next two, \ came out of this pipeline", 12.4,
                          font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(VGroup(top, bot), DOWN, buff=0.7)
        with self.voiceover(
            "Put together, this is our rasterizer. <bookmark mark='a'/> Vertices arrive in clip coordinates. "
            "Triangles are clipped against the near plane while still homogeneous, so nothing behind the eye is "
            "ever divided by a negative w. Then the division, the viewport, the edge functions, the depth test, "
            "and the perspective-correct blend. <bookmark mark='b'/> One detail matters more than it looks: "
            "vertices are snapped to a two-hundred-and-fifty-sixth of a pixel, as GPUs do, so the edge tests are "
            "exact, and two triangles sharing an edge never leave a crack between them. <bookmark mark='c'/> "
            "Every image in this chapter, and the next two, came out of this pipeline."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(bx) for bx in boxes], lag_ratio=0.25), Create(arrows), FadeIn(notes[0]),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
