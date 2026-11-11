from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, image, load


def unit(deg: float) -> np.ndarray:
    """A unit vector at ``deg`` degrees from the vertical, clockwise (towards +x)."""
    a = math.radians(deg)
    return np.array([math.sin(a), math.cos(a), 0.0])


def vec(o, deg, length, color, tex, side=RIGHT, width=5):
    """An arrow from o at ``deg`` from the vertical, with a MathTex name at its tip."""
    end = o + length * unit(deg)
    a = Arrow(o, end, buff=0, color=color, stroke_width=width, max_tip_length_to_length_ratio=0.12)
    t = MathTex(tex, font_size=30, color=color).next_to(end, side, buff=0.08)
    return VGroup(a, t)


class Shading(VoiceoverScene):
    def construct(self):
        self.card()
        self.cosine()
        self.phong()
        self.blinn()
        self.gouraud()
        self.normals()

    def card(self):
        card = chapter_card(4, r"Shading", r"How bright is a surface, \ seen from here?", lit=(1971, 1975, 1977),
                            extra=((1971, r"Gouraud shading"), (1975, r"Phong"), (1977, r"Blinn")), part=PART)
        with self.voiceover("Chapter four. Shading."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cosine(self):
        sh = load("shading")
        head = label(r"Lambert's cosine law", font_size=36).to_edge(UP, buff=0.3)
        C = np.array([-3.5, -1.1, 0])
        surf = Line(C + LEFT * 2.8, C + RIGHT * 2.8, color=GREY_B, stroke_width=4)
        nrm = vec(C, 0, 1.6, WHITE, r"\mathbf{N}", side=UP)
        th = ValueTracker(0.0)
        w, Lr = 1.2, 2.6

        def beam():
            t = th.get_value()
            c = math.cos(math.radians(t))
            Ld = unit(t)
            g = VGroup()
            for s in np.linspace(-w / 2, w / 2, 5):
                end = C + RIGHT * s / c
                g.add(Arrow(end + Lr * Ld, end, buff=0, color=HEAD, stroke_width=2.5,
                            max_tip_length_to_length_ratio=0.06))
            foot = Line(C + LEFT * w / 2 / c, C + RIGHT * w / 2 / c, color=NO, stroke_width=9)
            return VGroup(g, foot)
        bm = always_redraw(beam)
        rd = VGroup(MathTex(r"\theta =", font_size=30, color=HEAD), DecimalNumber(0, num_decimal_places=0,
                                                                                     font_size=30, color=HEAD),
                    MathTex(r"^\circ", font_size=30, color=HEAD), MathTex(r"\cos\theta =", font_size=30, color=NO),
                    DecimalNumber(1.0, num_decimal_places=2, font_size=30, color=NO))
        rd.arrange(RIGHT, buff=0.12).move_to(C + DOWN * 1.15)
        rd[1].add_updater(lambda m: m.set_value(th.get_value()).next_to(rd[0], RIGHT, buff=0.12))
        rd[2].add_updater(lambda m: m.next_to(rd[1], RIGHT, buff=0.04).align_to(rd[1], UP))
        rd[3].add_updater(lambda m: m.next_to(rd[2], RIGHT, buff=0.45).match_y(rd[0]))
        rd[4].add_updater(lambda m: m.set_value(math.cos(math.radians(th.get_value()))).next_to(rd[3], RIGHT,
                                                                                                buff=0.12))
        fl = label(r"the same beam, \ spread over $1/\cos\theta$ as much surface", font_size=18,
                   color=NO).next_to(rd, DOWN, buff=0.2)
        rows = VGroup(
            MathTex(r"E = \frac{\Phi}{A}", r",\quad", r"A = \frac{A_\perp}{\cos\theta}", font_size=34),
            MathTex(r"E = E_\perp \cos\theta = E_\perp\,(\mathbf{N}\cdot\mathbf{L})", font_size=34),
            MathTex(r"\text{diffuse} = k_d\,\max(0,\ \mathbf{N}\cdot\mathbf{L})", font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, 2.0, 0])
        rows[2].set_color(YES)
        img = image(sh["lambert"], height=2.1).next_to(rows, DOWN, buff=0.3).set_x(3.7)
        cap = label(r"our rasterizer: \ ambient + diffuse only", font_size=18, color=GREY_A).next_to(img, DOWN,
                                                                                                buff=0.12)
        with self.voiceover(
            "Now that we know which triangle a pixel sees, how bright should it be? <bookmark mark='a'/> Start with "
            "a beam of light falling straight onto a matte surface. <bookmark mark='b'/> Tilt the light. The same "
            "beam now spreads over a longer stretch of surface, one over the cosine of the angle as long, so each "
            "bit of surface receives less, in proportion to the cosine. Johann Heinrich Lambert wrote this down in "
            "1760. <bookmark mark='c'/> The power per unit area is the power over the area, and the area grows as "
            "one over the cosine. <bookmark mark='d'/> So brightness goes as the cosine, which is the dot product "
            "of the unit normal with the unit vector towards the light. <bookmark mark='e'/> A matte surface "
            "scatters that light equally in all directions, so it looks the same from anywhere: here is our sphere "
            "with diffuse light alone."
        ) as vo:
            self.play(FadeIn(head), Create(surf), FadeIn(nrm))
            vo.wait_until("a")
            self.play(FadeIn(bm), FadeIn(rd))
            vo.wait_until("b")
            self.play(th.animate.set_value(65), run_time=4)
            self.play(FadeIn(fl))
            vo.wait_until("c")
            self.play(Write(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]), FadeIn(img), FadeIn(cap))
        for m in rd:
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def phong(self):
        sh = load("shading")
        head = label(r"Phong: \ a highlight around the mirror direction", font_size=36).to_edge(UP, buff=0.3)
        O = np.array([-3.5, -1.4, 0])
        surf = Line(O + LEFT * 2.8, O + RIGHT * 2.8, color=GREY_B, stroke_width=4)
        tl = 45
        N = vec(O, 0, 2.2, WHITE, r"\mathbf{N}", side=UP)
        L = vec(O, -tl, 2.2, HEAD, r"\mathbf{L}", side=LEFT)
        R = vec(O, tl, 2.2, YES, r"\mathbf{R}", side=RIGHT)
        V = vec(O, 22, 2.4, DATA, r"\mathbf{V}", side=UP)
        proj = O + 2.2 * math.cos(math.radians(tl)) * UP
        dl = VGroup(DashedLine(O + 2.2 * unit(-tl), proj, color=GREY_B, stroke_width=1.5),
                    DashedLine(proj, O + 2.2 * unit(tl), color=GREY_B, stroke_width=1.5))
        pl = MathTex(r"(\mathbf{N}\cdot\mathbf{L})\,\mathbf{N}", font_size=24, color=GREY_A).next_to(proj, UL,
                                                                                                  buff=0.08)

        def lobe(s, col, length=2.4):
            pts = []
            for a in np.linspace(-math.pi / 2, math.pi / 2, 121):
                r = length * math.cos(a) ** s
                pts.append(O + r * unit(tl + math.degrees(a)))
            return VMobject(color=col, stroke_width=2.5, fill_color=col, fill_opacity=0.15).set_points_smoothly(pts)
        lobes = VGroup(lobe(8, GREY_B), lobe(32, YES))
        ll = VGroup(label(r"$s = 8$", font_size=17, color=GREY_B), label(r"$s = 32$", font_size=17, color=YES))
        ll.arrange(RIGHT, buff=0.3).next_to(surf, DOWN, buff=0.2)
        rows = VGroup(
            MathTex(r"\mathbf{R} = 2(\mathbf{N}\cdot\mathbf{L})\,\mathbf{N} - \mathbf{L}", font_size=32),
            MathTex(r"\text{specular} = k_s\,\max(0,\ \mathbf{R}\cdot\mathbf{V})^{s}", font_size=32),
            MathTex(r"I = k_a + k_d\,(\mathbf{N}\cdot\mathbf{L}) + k_s\,(\mathbf{R}\cdot\mathbf{V})^{s}",
                    font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 2.05, 0])
        rows[1].set_color(YES)
        img = image(sh["phong"], height=2.1).next_to(rows, DOWN, buff=0.3).set_x(3.6)
        cap = label(r"our rasterizer: \ $s = 32$, \ evaluated at every pixel", font_size=18, color=GREY_A).next_to(
            img, DOWN, buff=0.12)
        with self.voiceover(
            "Shiny surfaces add a highlight, and in 1975 Bui Tuong Phong, at Utah, gave the model still taught "
            "first. <bookmark mark='a'/> Reflect the light direction in the normal. Its projection onto the normal "
            "is N dot L times N; go there twice and step back by L, and you have the mirror direction R. "
            "<bookmark mark='b'/> The highlight is brightest when the eye looks straight down R, and falls off as "
            "the cosine between R and the view direction, raised to a power s. <bookmark mark='c'/> A larger "
            "power makes a tighter lobe and a smaller, sharper highlight, a shinier material. "
            "<bookmark mark='d'/> Add an ambient constant for light from everywhere else, the diffuse term and the "
            "highlight, and this is our rasterizer's sphere, with the power at thirty-two."
        ) as vo:
            self.play(FadeIn(head), Create(surf), FadeIn(N), FadeIn(L), FadeIn(V))
            vo.wait_until("a")
            self.play(Create(dl), FadeIn(pl))
            self.play(FadeIn(R), Write(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(lobes[0]), FadeIn(ll[0]))
            self.play(Create(lobes[1]), FadeIn(ll[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]), FadeIn(img), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def blinn(self):
        sh = load("shading")
        head = label(r"Blinn: \ the halfway vector", font_size=36).to_edge(UP, buff=0.3)
        O = np.array([-4.2, -0.4, 0])
        surf = Line(O + LEFT * 2.3, O + RIGHT * 2.3, color=GREY_B, stroke_width=4)
        tl, tv = -50, 30
        N = vec(O, 0, 2.0, WHITE, r"\mathbf{N}", side=UP)
        L = vec(O, tl, 2.0, HEAD, r"\mathbf{L}", side=LEFT)
        V = vec(O, tv, 2.0, DATA, r"\mathbf{V}", side=RIGHT)
        H = vec(O, (tl + tv) / 2, 2.0, LAM, r"\mathbf{H}", side=UP)
        arc = Arc(radius=1.0, start_angle=PI / 2 - math.radians((tl + tv) / 2), angle=math.radians((tl + tv) / 2),
                  arc_center=O, color=LAM, stroke_width=3)
        rows = VGroup(
            MathTex(r"\mathbf{H} = \frac{\mathbf{L} + \mathbf{V}}{\lVert \mathbf{L} + \mathbf{V} \rVert}", r",\quad",
                    r"\text{specular} = k_s\,(\mathbf{N}\cdot\mathbf{H})^{s'}", font_size=32),
            MathTex(r"\cos^{s}\alpha", r"\approx", r"e^{-s\alpha^2/2}", font_size=34),
            MathTex(r"\cos^{s'}\tfrac{\alpha}{2}", r"\approx", r"e^{-s'\alpha^2/8}", font_size=34),
            MathTex(r"s' = 4s", font_size=34, color=YES),
        )
        rows[0].move_to([2.6, 2.3, 0])
        VGroup(rows[1], rows[2], rows[3]).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(rows[0], DOWN,
                                                                                             buff=0.35).set_x(1.3)
        whys = VGroup(note(r"Phong, \ with $\alpha$ the angle between $\mathbf{R}$ and $\mathbf{V}$", font_size=16),
                      note(r"Blinn: \ $\mathbf{H}$ is $\alpha/2$ from $\mathbf{N}$", font_size=16),
                      note(r"same highlight width", font_size=16, color=YES))
        for r, w in zip(rows[1:], whys):
            w.next_to(r, RIGHT, buff=0.25)
        imgs = Group(image(sh["phong"], height=2.0), image(sh["blinn_phong"], height=2.0)).arrange(RIGHT, buff=0.3)
        imgs.to_corner(DR, buff=0.5).shift(UP * 0.15)
        caps = VGroup(label(r"Phong, \ $s = 32$", font_size=17, color=GREY_A),
                      label(r"Blinn--Phong, \ $s' = 128$", font_size=17, color=LAM))
        for c, im in zip(caps, imgs):
            c.next_to(im, DOWN, buff=0.1)
        foot = wrapped_label(r"with a distant light and viewer, \ $\mathbf{H}$ is the same at every pixel: \ no "
                             r"reflection vector to compute; \ the fixed-function lighting of OpenGL and Direct3D",
                             5.6, font_size=19, color=WHITE).move_to([-3.6, -2.6, 0])
        with self.voiceover(
            "In 1977 Jim Blinn proposed a cheaper highlight. <bookmark mark='a'/> Instead of reflecting the light, "
            "take the vector halfway between the light and the eye, H, and measure how close the normal is to "
            "it. When the normal is exactly H, the eye sits in the mirror direction. <bookmark mark='b'/> The two "
            "highlights are not the same width with the same power. Near the peak, Phong's cosine to the power s "
            "behaves like a Gaussian in the angle alpha. <bookmark mark='c'/> The angle to H is about half of alpha, "
            "<bookmark mark='d'/> so Blinn's power must be four times larger to match. <bookmark mark='e'/> With a "
            "distant light and viewer, H is the same at every pixel, which made this the fixed-function lighting "
            "of OpenGL and Direct3D."
        ) as vo:
            self.play(FadeIn(head), Create(surf), FadeIn(N), FadeIn(L), FadeIn(V))
            vo.wait_until("a")
            self.play(FadeIn(H), Create(arc), Write(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[2]), FadeIn(imgs), FadeIn(caps))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def gouraud(self):
        sh = load("shading")
        head = label(r"Gouraud against Phong shading", font_size=36).to_edge(UP, buff=0.3)
        names = (("gouraud", r"Gouraud: \ light the vertices, \ blend colours", NO),
                 ("phong", r"Phong: \ blend normals, \ light every pixel", YES),
                 ("truth", r"the exact sphere, \ ray cast", GREY_A))
        imgs = Group(*[image(sh[k], height=2.7) for k, _, _ in names]).arrange(RIGHT, buff=0.3).next_to(
            head, DOWN, buff=0.4)
        caps = VGroup(*[label(t, font_size=18, color=c).next_to(im, DOWN, buff=0.12)
                        for (_, t, c), im in zip(names, imgs)])
        x, y = sh["max_diff_at"]
        H, W = sh["gouraud"].shape[:2]
        x0, x1, y0, y1 = x - 20, x + 20, y - 15, y + 15
        boxes = VGroup()
        for im in imgs:
            pic = im[0]
            ul = pic.get_corner(UL)
            sx, sy = pic.width / W, pic.height / H
            boxes.add(Rectangle(width=(x1 - x0) * sx, height=(y1 - y0) * sy, color=HEAD, stroke_width=2).move_to(
                ul + np.array([(x0 + x1) / 2 * sx, -(y0 + y1) / 2 * sy, 0])))
        crops = Group(*[image(sh[k][y0:y1, x0:x1], height=2.7) for k, _, _ in names]).arrange(RIGHT, buff=0.3)
        crops.move_to(imgs)
        zl = note(rf"zoomed: \ 40 $\times$ 30 pixels around pixel ({x}, {y})", font_size=17).next_to(caps, DOWN,
                                                                                                    buff=0.15)
        notes = VGroup(
            wrapped_label(rf"{sh['triangles']} triangles; \ Gouraud \ (1971) \ evaluates the lighting only at "
                          r"vertices, \ so a highlight that falls between them is smeared into a star, \ or missed",
                          12.4, font_size=20, color=WHITE),
            wrapped_label(rf"largest per-pixel difference: \ {sh['max_diff_gouraud_phong']:.2f} of full brightness; "
                          rf"\ error against the exact sphere: \ Gouraud {sh['rmse_gouraud']:.3f}, \ Phong "
                          rf"{sh['rmse_phong']:.4f}, \ {sh['rmse_gouraud'] / sh['rmse_phong']:.0f} times smaller",
                          12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Where should the lighting be computed? <bookmark mark='a'/> Henri Gouraud, in 1971, evaluated it once "
            "per vertex and let the rasterizer blend the colours, which is cheap. Phong's paper of 1975 also "
            "proposed the alternative: blend the normals, renormalize, and light every pixel. "
            "<bookmark mark='b'/> On a sphere of three hundred and sixty triangles the difference is in the "
            "highlight. <bookmark mark='c'/> Zoom in. Gouraud's highlight is a star of straight-edged blends, "
            "because a peak between vertices cannot be made by blending the values at the vertices. Phong's is "
            "round. <bookmark mark='d'/> Our rasterizer measures it: against the exact sphere, Gouraud's error is "
            "five times larger. Diffuse light varies slowly and survives vertex lighting; highlights do not, which "
            "is why every modern renderer lights per pixel."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(imgs[0]), FadeIn(caps[0]), FadeIn(notes[0]))
            self.play(FadeIn(imgs[1]), FadeIn(caps[1]))
            vo.wait_until("b")
            self.play(FadeIn(imgs[2]), FadeIn(caps[2]), Create(boxes))
            vo.wait_until("c")
            self.play(FadeOut(boxes), FadeOut(imgs), FadeIn(crops), FadeIn(zl))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def normals(self):
        head = label(r"Normals need the inverse transpose", font_size=36).to_edge(UP, buff=0.3)
        M = np.diag([1.8, 0.6])
        Mit = np.linalg.inv(M).T
        c = np.array([-3.4, -0.3, 0])
        r0, ln = 1.1, 0.6
        angs = np.linspace(0, TAU, 9)[:-1] + 0.35
        circ = Circle(radius=r0, color=GREY_B, stroke_width=2.5).move_to(c)
        cn = VGroup(*[Arrow(c + r0 * np.r_[math.cos(a), math.sin(a), 0], c + (r0 + ln) * np.r_[math.cos(a),
                                                                                             math.sin(a), 0],
                            buff=0, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.25) for a in angs])
        shape = VGroup(circ, cn)
        good = VGroup()
        for a in angs:
            p = np.array([math.cos(a), math.sin(a)])
            q = c + np.r_[r0 * (M @ p), 0]
            n = Mit @ p
            n = ln * n / np.linalg.norm(n)
            good.add(Arrow(q, q + np.r_[n, 0], buff=0, color=YES, stroke_width=3,
                           max_tip_length_to_length_ratio=0.25))
        ml = MathTex(r"M = \begin{pmatrix} 1.8 & 0 \\ 0 & 0.6 \end{pmatrix}", font_size=30).move_to(c + UP * 2.4)
        ill = note(r"illustrative", font_size=16).next_to(ml, RIGHT, buff=0.3)
        leg = VGroup(label(r"normals times $M$: \ tilted", font_size=19, color=NO),
                     label(r"times $M^{-\top}$: \ perpendicular", font_size=19, color=YES)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to(c + DOWN * 2.3)
        rows = VGroup(
            MathTex(r"\mathbf{n}^{\top}", r"\mathbf{t}", r"= 0", font_size=36),
            MathTex(r"\mathbf{n}^{\top}", r"M^{-1}", r"M", r"\mathbf{t}", r"= 0", font_size=36),
            MathTex(r"(M^{-\top}\mathbf{n})^{\top}", r"(M\mathbf{t})", r"= 0", font_size=36),
            MathTex(r"\mathbf{n}'", r"=", r"M^{-\top}\mathbf{n}", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 1.0, 0]).align_to([1.6, 0, 0], LEFT)
        rows[3].set_color(YES)
        whys = VGroup(note(r"a normal is perpendicular to every tangent", font_size=16),
                      note(r"insert $M^{-1}M = I$", font_size=16),
                      note(r"regroup: \ tangents move by $M$", font_size=16),
                      note(r"so normals move by this", font_size=16, color=YES))
        for r, w in zip(rows, whys):
            w.next_to(r, DOWN, buff=0.06).align_to(r, LEFT)
        foot = wrapped_label(r"for a rotation $M^{-\top} = M$, \ which is why the mistake hides until something is "
                             r"squashed; \ engines pass a separate normal matrix to their shaders", 5.0, font_size=19,
                             color=WHITE).next_to(whys[3], DOWN, buff=0.35).align_to(rows, LEFT)
        with self.voiceover(
            "One last trap, back in chapter one's matrices. <bookmark mark='a'/> Normals are directions, so they "
            "are not translated. But squash a circle into an ellipse and move its normals with the same matrix, "
            "and they tilt: they are no longer perpendicular to the surface, and the lighting is wrong. "
            "<bookmark mark='b'/> Why? A normal is defined by being perpendicular to every tangent. "
            "<bookmark mark='c'/> Slip the identity, M inverse times M, between them. <bookmark mark='d'/> The "
            "tangents move by M, so to keep the product zero, normals must move by the inverse transpose. "
            "<bookmark mark='e'/> For rotations the two are the same matrix, which is why the mistake hides until "
            "an object is stretched, and why engines hand their shaders a separate normal matrix."
        ) as vo:
            self.play(FadeIn(head), FadeIn(shape), FadeIn(ml), FadeIn(ill))
            vo.wait_until("a")
            self.play(ApplyMatrix(M, shape, about_point=c), cn.animate.set_color(NO), run_time=2.5)
            self.play(FadeIn(leg[0]))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("d")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            self.play(TransformMatchingTex(rows[2].copy(), rows[3]), FadeIn(whys[3]), FadeIn(good), FadeIn(leg[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
