from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


def unit(deg: float) -> np.ndarray:
    """A unit vector at ``deg`` degrees from the vertical, clockwise (towards +x)."""
    a = math.radians(deg)
    return np.array([math.sin(a), math.cos(a), 0.0])


def rows_with_notes(pairs, buff=0.34, note_size=17):
    """MathTex rows, each with a grey note under it; returns (rows, notes, group)."""
    rows = VGroup(*[r for r, _ in pairs])
    notes = VGroup(*[note(n, font_size=note_size) if isinstance(n, str) else n for _, n in pairs])
    blocks = VGroup(*[VGroup(r, n).arrange(DOWN, aligned_edge=LEFT, buff=0.07) for r, n in zip(rows, notes)])
    blocks.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return rows, notes, blocks


def lobe_points(O, fn, scale, n=91):
    """A polar plot in the plane above a surface point O: radius scale * fn(angle from the normal)."""
    pts = []
    for a in np.linspace(-90, 90, n):
        pts.append(O + scale * fn(a) * unit(a))
    return pts


class Radiometry(VoiceoverScene):
    def construct(self):
        self.card()
        self.solid_angle()
        self.radiance()
        self.invariance()
        self.brdf()
        self.microfacets()
        self.furnace()

    def card(self):
        card = chapter_card(9, r"Radiometry and BRDFs", r"How much light leaves a point, \ in one direction?",
                            lit=(1977, 1982, 2007), extra=((1977, r"Nicodemus et al.: \ the BRDF"),
                                                           (1982, r"Cook and Torrance"),
                                                           (2007, r"Walter et al.: \ GGX")), part=PART)
        with self.voiceover("Chapter nine. Radiometry and BRDFs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------ solid angle
    def solid_angle(self):
        head = label(r"Solid angle: \ area on a sphere", font_size=36).to_edge(UP, buff=0.3)
        S = np.array([-3.9, -0.7, 0])
        R = 2.1
        k = 0.28                                   # how flat the circles of latitude look
        sphere = Circle(radius=R, color=GREY_B, stroke_width=2.5).move_to(S)
        equator = Ellipse(width=2 * R, height=2 * R * k, color=GREY_D, stroke_width=1.5).move_to(S)
        cd = Dot(S, radius=0.05, color=GREY_A)
        # the 2D angle first: an arc of the outline
        a0, a1 = math.radians(-18), math.radians(18)
        arc = Arc(radius=R, start_angle=a0, angle=a1 - a0, arc_center=S, color=DATA, stroke_width=7)
        rad = VGroup(Line(S, S + R * np.array([math.cos(a0), math.sin(a0), 0]), color=DATA, stroke_width=2),
                     Line(S, S + R * np.array([math.cos(a1), math.sin(a1), 0]), color=DATA, stroke_width=2))
        arcl = VGroup(MathTex(r"s", font_size=30, color=DATA).next_to(S + RIGHT * R, RIGHT, buff=0.12),
                      MathTex(r"\theta", font_size=28, color=DATA).move_to(S + RIGHT * 0.55),
                      MathTex(r"r", font_size=28, color=GREY_A).move_to(S + R * 0.5 * np.array([0.95, -0.55, 0])))
        al = ValueTracker(25.0)

        def cap():
            a = math.radians(al.get_value())
            y = S[1] + R * math.cos(a)
            w = max(2 * R * math.sin(a), 0.02)
            rim = Ellipse(width=w, height=max(w * k, 0.01), color=YES, stroke_width=2.5, fill_color=YES,
                          fill_opacity=0.25).move_to([S[0], y, 0])
            top = Arc(radius=R, start_angle=PI / 2 - a, angle=2 * a, arc_center=S, color=YES, stroke_width=6)
            e1, e2 = rim.get_left(), rim.get_right()
            cone = VGroup(DashedLine(S, e1, color=YES, stroke_width=1.8), DashedLine(S, e2, color=YES,
                                                                                     stroke_width=1.8))
            ang = Arc(radius=0.6, start_angle=PI / 2, angle=a, arc_center=S, color=HEAD, stroke_width=2.5)
            axis = DashedLine(S, S + UP * (R + 0.35), color=GREY_C, stroke_width=1.5)
            return VGroup(axis, rim, top, cone, ang)
        capm = always_redraw(cap)
        rd = VGroup(MathTex(r"\alpha =", font_size=30, color=HEAD),
                    DecimalNumber(25, num_decimal_places=0, font_size=30, color=HEAD),
                    MathTex(r"^\circ", font_size=30, color=HEAD),
                    MathTex(r"\Omega =", font_size=30, color=YES),
                    DecimalNumber(2 * PI * (1 - math.cos(math.radians(25))), num_decimal_places=2, font_size=30,
                                  color=YES),
                    MathTex(r"\text{sr}", font_size=28, color=YES))
        rd.arrange(RIGHT, buff=0.12).move_to(S + DOWN * (R + 0.45))
        rd[1].add_updater(lambda m: m.set_value(al.get_value()).next_to(rd[0], RIGHT, buff=0.12))
        rd[2].add_updater(lambda m: m.next_to(rd[1], RIGHT, buff=0.04).align_to(rd[1], UP))
        rd[3].add_updater(lambda m: m.next_to(rd[2], RIGHT, buff=0.45).match_y(rd[0]))
        rd[4].add_updater(lambda m: m.set_value(2 * PI * (1 - math.cos(math.radians(al.get_value())))).next_to(
            rd[3], RIGHT, buff=0.12))
        rd[5].add_updater(lambda m: m.next_to(rd[4], RIGHT, buff=0.1).match_y(rd[0]))
        r0 = MathTex(r"\theta", r"=", r"{s", r"\over", r"r}", font_size=34)
        r1 = MathTex(r"\Omega", r"=", r"{A", r"\over", r"r^2}", font_size=34)
        r2 = MathTex(r"d\omega", r"=", r"\sin\theta\, d\theta\, d\phi", font_size=34)
        r3 = MathTex(r"\Omega_{\text{cap}}", r"=", r"\int_0^{2\pi}\!\!\int_0^{\alpha} \sin\theta\, d\theta\, d\phi",
                     r"=", r"2\pi\,(1-\cos\alpha)", font_size=34)
        r4 = MathTex(r"\Omega_{\text{hemisphere}} = 2\pi, \qquad \Omega_{\text{sphere}} = 4\pi", font_size=34,
                     color=YES)
        rows, notes, blk = rows_with_notes([
            (r0, r"an angle: \ arc over radius \ (radians)"),
            (r1, r"a solid angle: \ area over radius squared \ (steradians)"),
            (r2, r"a small patch of the unit sphere: \ latitude times longitude"),
            (r3, r"integrate over a cap of half-angle $\alpha$"),
            (r4, r"the directions above a surface: \ half the sphere")])
        blk.to_edge(RIGHT, buff=0.35).set_y(0.0)
        with self.voiceover(
            "First, directions. <bookmark mark='a'/> An angle in the "
            "plane is an arc length divided by the radius, in radians. <bookmark mark='b'/> A solid angle is the "
            "same idea one dimension up: the area a shape covers on a sphere, divided by the radius squared, in "
            "steradians. <bookmark mark='c'/> On the unit sphere a small patch of latitude and longitude has area "
            "sine theta d theta d phi. <bookmark mark='d'/> Integrate it over a cap of half-angle alpha: two pi "
            "times one minus cos alpha. <bookmark mark='e'/> Open the cap to ninety degrees and it covers every "
            "direction above a surface: two pi steradians, half the sphere's four pi."
        ) as vo:
            self.play(FadeIn(head), Create(sphere), FadeIn(equator), FadeIn(cd))
            vo.wait_until("a")
            self.play(Create(arc), Create(rad), FadeIn(arcl), Write(r0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeOut(arc), FadeOut(rad), FadeOut(arcl), FadeIn(capm),
                      TransformMatchingTex(r0.copy(), r1), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(r2), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Write(r3), FadeIn(notes[3]), FadeIn(rd))
            vo.wait_until("e")
            self.play(al.animate.set_value(90), run_time=3)
            self.play(FadeIn(r4), FadeIn(notes[4]))
        for m in rd:
            m.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ radiance
    def radiance(self):
        head = label(r"Flux, \ irradiance, \ radiance", font_size=36).to_edge(UP, buff=0.3)
        O = np.array([-4.2, -1.6, 0])
        surf = Line(O + LEFT * 2.4, O + RIGHT * 2.4, color=GREY_B, stroke_width=3)
        dA = Line(O + LEFT * 0.55, O + RIGHT * 0.55, color=DATA, stroke_width=9)
        dAl = MathTex(r"dA", font_size=28, color=DATA).next_to(dA, DOWN, buff=0.12)
        nrm = Arrow(O, O + UP * 1.7, buff=0, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.1)
        nl = MathTex(r"\mathbf{n}", font_size=28).next_to(nrm.get_end(), UP, buff=0.06)
        th = 42
        d = unit(th)
        half = 6
        beam = VGroup(*[Line(O + s * RIGHT * 0.5, O + s * RIGHT * 0.5 + 3.4 * unit(th + half * s), color=HEAD,
                             stroke_width=2) for s in (-1, 0, 1)])
        ang = Arc(radius=0.75, start_angle=PI / 2 - math.radians(th), angle=math.radians(th), arc_center=O,
                  color=HEAD, stroke_width=2)
        al = MathTex(r"\theta", font_size=26, color=HEAD).move_to(O + 1.0 * unit(th / 2))
        dw = Arc(radius=3.0, start_angle=PI / 2 - math.radians(th + half), angle=math.radians(2 * half),
                 arc_center=O, color=YES, stroke_width=5)
        dwl = MathTex(r"d\omega", font_size=28, color=YES).next_to(dw, UR, buff=0.05)
        perp = np.array([d[1], -d[0], 0])
        proj = Line(O + 1.6 * d - 0.55 * math.cos(math.radians(th)) * perp,
                    O + 1.6 * d + 0.55 * math.cos(math.radians(th)) * perp, color=NO, stroke_width=6)
        pl = MathTex(r"dA\cos\theta", font_size=26, color=NO).next_to(proj, DR, buff=0.02)
        r0 = MathTex(r"\Phi", font_size=34)
        r1 = MathTex(r"E", r"=", r"{d\Phi", r"\over", r"dA}", font_size=34)
        r2 = MathTex(r"L", r"=", r"{d^2\Phi", r"\over", r"dA\cos\theta\, d\omega}", font_size=34)
        r3 = MathTex(r"E", r"=", r"\int_\Omega L\cos\theta\, d\omega", font_size=34, color=YES)
        rows, notes, blk = rows_with_notes([
            (r0, r"flux: \ energy per second, \ watts"),
            (r1, r"irradiance: \ flux arriving per area, \ W\,m$^{-2}$"),
            (r2, r"radiance: \ per area across the beam, \ per steradian, \ W\,m$^{-2}$\,sr$^{-1}$"),
            (r3, r"irradiance gathered from radiance, \ with Lambert's cosine \ (chapter 4)")], buff=0.4)
        blk.to_edge(RIGHT, buff=0.4).set_y(0.1)
        pix = wrapped_label(r"a camera pixel is a small area looking along a narrow cone: \ it measures radiance",
                            5.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35).set_x(-3.6)
        with self.voiceover(
            "Now the quantities. <bookmark mark='a'/> Radiant flux, capital phi, is energy per second, in watts. "
            "<bookmark mark='b'/> Irradiance is flux arriving per unit area: how brightly a surface is lit. "
            "<bookmark mark='c'/> Radiance divides once more: flux per unit area across the beam, per unit solid "
            "angle. The cosine is there because a patch seen at a slant presents only cos theta of its area. "
            "<bookmark mark='d'/> Radiance is what a camera pixel measures: a small area looking along a narrow "
            "cone. <bookmark mark='e'/> Gathered over the hemisphere with the cosine, radiance gives back "
            "irradiance: Lambert's law of chapter four."
        ) as vo:
            self.play(FadeIn(head), Create(surf), FadeIn(nrm), FadeIn(nl))
            vo.wait_until("a")
            self.play(FadeIn(r0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(dA), FadeIn(dAl), Write(r1), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(beam), Create(ang), FadeIn(al), Create(dw), FadeIn(dwl))
            self.play(Create(proj), FadeIn(pl), Write(r2), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(pix))
            vo.wait_until("e")
            self.play(Write(r3), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ radiance along a ray
    def invariance(self):
        head = label(r"Radiance is constant along a ray", font_size=36).to_edge(UP, buff=0.3)
        E = np.array([-6.3, 0.2, 0])
        half = math.radians(9)
        dist = ValueTracker(1.6)
        eye = VGroup(Square(side_length=0.22, color=DATA, fill_color=DATA, fill_opacity=0.6).move_to(E),
                     label(r"pixel", font_size=17, color=DATA).next_to(E, UP, buff=0.2))

        def scene():
            dd = dist.get_value()
            x = E[0] + dd
            wall = Line([x, -1.8, 0], [x, 2.4, 0], color=GREY_B, stroke_width=4)
            h = dd * math.tan(half)
            cone = VGroup(Line(E, [x, E[1] + h, 0], color=HEAD, stroke_width=2),
                          Line(E, [x, E[1] - h, 0], color=HEAD, stroke_width=2))
            foot = Line([x, E[1] - h, 0], [x, E[1] + h, 0], color=YES, stroke_width=9)
            return VGroup(wall, cone, foot)
        sc = always_redraw(scene)
        d0 = 1.6

        def readout(tex, fn, col, y):
            t = MathTex(tex, font_size=28, color=col)
            v = DecimalNumber(fn(), num_decimal_places=2, font_size=28, color=col)
            VGroup(t, v).arrange(RIGHT, buff=0.15).move_to([-3.6, y, 0]).align_to([-6.4, 0, 0], LEFT)
            v.add_updater(lambda m: m.set_value(fn()).next_to(t, RIGHT, buff=0.15))
            return VGroup(t, v)
        rel = lambda: dist.get_value() / d0
        ro = VGroup(readout(r"\text{distance} \times", rel, WHITE, -2.25),
                    readout(r"\text{wall seen} \times", lambda: rel() ** 2, YES, -2.75),
                    readout(r"\text{light from each bit} \times", lambda: rel() ** -2, NO, -3.25))
        r0 = MathTex(r"A_{\text{seen}}", r"\propto", r"d^2", font_size=34, color=YES)
        r1 = MathTex(r"\omega_{\text{pixel, seen from the wall}}", r"\propto", r"1/d^2", font_size=34, color=NO)
        r2 = MathTex(r"\Phi_{\text{pixel}}", r"\propto", r"L\, d^2 \cdot \frac{1}{d^2}", r"=", r"L", font_size=34)
        r3 = MathTex(r"L_{\text{pixel}} = L_{\text{surface}}", font_size=36, color=HEAD)
        rows, notes, blk = rows_with_notes([
            (r0, r"the patch of wall inside the pixel's cone"),
            (r1, r"the share of each bit's light that enters the pixel"),
            (r2, r"the two cancel"),
            (r3, r"so a ray carries one number back to the eye")], buff=0.4)
        blk.to_edge(RIGHT, buff=0.4).set_y(0.3)
        ill = note(r"illustrative geometry", font_size=16).move_to([-3.6, 2.75, 0])
        with self.voiceover(
            "Radiance has one property that makes ray tracing possible. <bookmark mark='a'/> A pixel looks along a "
            "narrow cone. Move the wall away, and the patch of wall inside the cone grows with the square of the "
            "distance, <bookmark mark='b'/> while the share of each bit's light that enters the pixel falls with the"
            " inverse square. <bookmark mark='c'/> They cancel: in empty space, radiance is constant along a ray. "
            "That is why a wall does not darken as you walk away from it. <bookmark mark='d'/> And it is why a ray "
            "tracer can carry one number, the radiance, from the surface it hits straight back to the eye."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eye), FadeIn(sc), FadeIn(ill), FadeIn(ro))
            vo.wait_until("a")
            self.play(FadeIn(r0), FadeIn(notes[0]))
            self.play(dist.animate.set_value(4.8), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(r1), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(r2), FadeIn(notes[2]))
            self.play(dist.animate.set_value(2.6), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(r3), FadeIn(notes[3]))
        for g in ro:
            g[1].clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the BRDF
    def brdf(self):
        head = label(r"The BRDF: \ how a material reflects", font_size=36).to_edge(UP, buff=0.3)
        O = np.array([-4.0, -1.7, 0])
        surf = Line(O + LEFT * 2.6, O + RIGHT * 2.6, color=GREY_B, stroke_width=3)
        ti, to = -45, 28
        wi = Arrow(O + 2.6 * unit(ti), O, buff=0, color=HEAD, stroke_width=4, max_tip_length_to_length_ratio=0.08)
        wil = MathTex(r"\omega_i", font_size=30, color=HEAD).next_to(O + 2.6 * unit(ti), LEFT, buff=0.08)
        wo = Arrow(O, O + 2.6 * unit(to), buff=0, color=DATA, stroke_width=4, max_tip_length_to_length_ratio=0.08)
        wol = MathTex(r"\omega_o", font_size=30, color=DATA).next_to(wo.get_end(), RIGHT, buff=0.08)
        lam = VMobject(color=YES, stroke_width=3, fill_color=YES, fill_opacity=0.18).set_points_as_corners(
            lobe_points(O, lambda a: 1.0, 1.25))
        n = 20
        phong = VMobject(color=LAM, stroke_width=3, fill_color=LAM, fill_opacity=0.18).set_points_as_corners(
            lobe_points(O, lambda a: max(math.cos(math.radians(a + ti)), 0) ** n, 2.4, n=181))
        laml = label(r"matte: \ the same in every direction", font_size=18, color=YES).next_to(O, DOWN, buff=0.3)
        phl = label(r"glossy: \ a lobe about the mirror direction", font_size=18, color=LAM).next_to(O, DOWN,
                                                                                                    buff=0.3)
        r0 = MathTex(r"f(\omega_i,\omega_o)", r"=", r"{dL_o(\omega_o)", r"\over",
                     r"L_i(\omega_i)\cos\theta_i\, d\omega_i}", font_size=32)
        r1 = MathTex(r"L_o(\omega_o)", r"=", r"\int_\Omega f(\omega_i,\omega_o)\, L_i(\omega_i)\cos\theta_i\,"
                     r"d\omega_i", font_size=32)
        r2 = MathTex(r"f_{\text{Lambert}}", r"=", r"{\rho", r"\over", r"\pi}", font_size=32, color=YES)
        r3a = MathTex(r"\int_\Omega \cos\theta\, d\omega", r"=",
                      r"\int_0^{2\pi}\!\!\int_0^{\pi/2}\cos\theta\sin\theta\, d\theta\, d\phi", font_size=32)
        r3b = MathTex(r"\int_\Omega \cos\theta\, d\omega", r"=", r"2\pi \cdot \tfrac{1}{2}", r"=", r"\pi",
                      font_size=32)
        r4 = MathTex(r"L_i = 1", r"\ \Rightarrow\ ", r"L_o = \frac{\rho}{\pi}\cdot\pi = \rho", font_size=32,
                     color=YES)
        rows, notes, blk = rows_with_notes([
            (r0, r"radiance out per irradiance in; \ units sr$^{-1}$"),
            (r1, r"the reflection equation: \ sum over every incoming direction"),
            (r2, r"a matte surface of albedo $\rho$"),
            (r3a, r"why $\pi$: \ the cosine over the hemisphere"),
            (r4, r"under uniform light a matte surface returns its albedo")], buff=0.3)
        blk.to_edge(RIGHT, buff=0.3).set_y(-0.05)
        r3b.move_to(r3a, aligned_edge=LEFT)
        with self.voiceover(
            "How a material reflects is a function of two directions. <bookmark mark='a'/> The BRDF, the "
            "bidirectional reflectance distribution function named by Fred Nicodemus and colleagues in 1977, is the "
            "radiance going out in one direction per unit of irradiance arriving from another. <bookmark mark='b'/> "
            "Add up every incoming direction, and we have the reflection equation. <bookmark mark='c'/> A matte "
            "surface scatters equally everywhere, so its BRDF is a constant, rho over pi. <bookmark mark='d'/> Why "
            "pi? The cosine integrated over the hemisphere is two pi times one half: pi. <bookmark mark='e'/> So "
            "under uniform light of radiance one, a matte surface returns exactly its albedo. <bookmark mark='f'/> A"
            " glossy surface instead gathers its light into a lobe around the mirror direction."
        ) as vo:
            self.play(FadeIn(head), Create(surf))
            vo.wait_until("a")
            self.play(GrowArrow(wi), FadeIn(wil), GrowArrow(wo), FadeIn(wol), Write(r0), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(r1), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(lam), FadeIn(laml), FadeIn(r2), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Write(r3a), FadeIn(notes[3]))
            self.play(TransformMatchingTex(r3a, r3b))
            vo.wait_until("e")
            self.play(FadeIn(r4), FadeIn(notes[4]))
            vo.wait_until("f")
            self.play(ReplacementTransform(lam, phong), ReplacementTransform(laml, phl))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ microfacets
    def microfacets(self):
        head = label(r"Microfacets: \ Cook--Torrance and GGX", font_size=36).to_edge(UP, buff=0.3)
        rng = np.random.default_rng(5)
        xs = np.linspace(-6.4, -1.6, 25)
        u = rng.uniform(-1, 1, len(xs))
        y0 = -1.4
        rough = ValueTracker(0.16)
        ti, to = -40, 20
        hdeg = (ti + to) / 2

        def surface():
            ys = y0 + rough.get_value() * u
            g = VGroup()
            for k in range(len(xs) - 1):
                a, b = np.array([xs[k], ys[k], 0]), np.array([xs[k + 1], ys[k + 1], 0])
                t = b - a
                nrm = np.array([-t[1], t[0], 0]) / np.linalg.norm(t)
                tilt = math.degrees(math.atan2(nrm[0], nrm[1]))
                hit = abs(tilt - hdeg) < 7
                g.add(Line(a, b, color=HEAD if hit else GREY_B, stroke_width=6 if hit else 2.5))
                if hit:
                    m = (a + b) / 2
                    g.add(Arrow(m, m + 0.6 * nrm, buff=0, color=HEAD, stroke_width=2.5,
                                max_tip_length_to_length_ratio=0.25))
            return g
        surf = always_redraw(surface)
        C = np.array([-4.0, y0 + 0.5, 0])
        wi = Arrow(C + 2.4 * unit(ti), C, buff=0, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.08)
        wo = Arrow(C, C + 2.4 * unit(to), buff=0, color=DATA, stroke_width=3, max_tip_length_to_length_ratio=0.08)
        hv = Arrow(C, C + 1.9 * unit(hdeg), buff=0, color=HEAD, stroke_width=4, max_tip_length_to_length_ratio=0.1)
        lab = VGroup(MathTex(r"\omega_i", font_size=28).next_to(wi.get_start(), LEFT, buff=0.06),
                     MathTex(r"\omega_o", font_size=28, color=DATA).next_to(wo.get_end(), RIGHT, buff=0.06),
                     MathTex(r"\mathbf{h}", font_size=30, color=HEAD).next_to(hv.get_end(), UP, buff=0.06))
        ill = note(r"a rough surface, \ magnified \ (illustrative)", font_size=16).move_to([-4.0, -2.4, 0])
        r0 = MathTex(r"\mathbf{h}", r"=", r"{\omega_i + \omega_o", r"\over", r"\lVert\omega_i + \omega_o\rVert}",
                     font_size=32)
        r1 = MathTex(r"f", r"=", r"{D(\mathbf{h})\; G(\omega_i,\omega_o)\; F(\omega_i\cdot\mathbf{h})", r"\over",
                     r"4\cos\theta_i\cos\theta_o}", font_size=32)
        legend = VGroup(label(r"$D$: \ the density of facets facing $\mathbf{h}$", font_size=18, color=HEAD),
                        label(r"$G$: \ facets hidden or shadowed by others \ (Smith)", font_size=18, color=LAM),
                        label(r"$F$: \ Fresnel--Schlick \ (chapter 7)", font_size=18, color=DATA)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        r2 = MathTex(r"D_{\text{GGX}}(\mathbf{h})", r"=", r"{\alpha^2", r"\over",
                     r"\pi\left((\mathbf{n}\cdot\mathbf{h})^2(\alpha^2-1)+1\right)^2}", font_size=32)
        rows, notes, blk = rows_with_notes([
            (r0, r"only facets whose normal is $\mathbf{h}$ send $\omega_i$ to $\omega_o$"),
            (r1, legend),
            (r2, r"one parameter: \ roughness $\alpha$")], buff=0.4)
        blk.to_edge(RIGHT, buff=0.35).set_y(0.0)
        rr = label(r"rougher $\rightarrow$", font_size=19, color=HEAD).move_to([-4.0, 2.6, 0])
        with self.voiceover(
            "Glossy surfaces are rough at a scale far below a pixel. <bookmark mark='a'/> In 1982 Robert Cook and "
            "Kenneth Torrance modelled them as tiny mirrors, microfacets, tilted at random. <bookmark mark='b'/> A "
            "facet sends light from one direction to the other only if its normal is the half vector between them. "
            "<bookmark mark='c'/> So the BRDF is D, the density of facets facing the half vector; times G, the "
            "fraction not hidden or shadowed by their neighbours; times F, the Fresnel reflectance of chapter seven;"
            " over four cosines from the change of variables. <bookmark mark='d'/> The GGX distribution, brought to "
            "graphics by Bruce Walter and colleagues in 2007, has one parameter, the roughness alpha. <bookmark "
            "mark='e'/> Turn it up and the facets spread: the highlight widens and dims."
        ) as vo:
            self.play(FadeIn(head), FadeIn(surf), FadeIn(ill))
            vo.wait_until("a")
            self.play(GrowArrow(wi), GrowArrow(wo), FadeIn(lab[:2]))
            vo.wait_until("b")
            self.play(GrowArrow(hv), FadeIn(lab[2]), Write(r0), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Write(r1), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(Write(r2), FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(rr), rough.animate.set_value(0.42), run_time=3)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------ the white furnace
    def furnace(self):
        fu = load("furnace")
        rows = fu["rows"]
        rec = fu["reciprocity"]
        head = label(r"Reciprocity and the white furnace", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 80, 20], y_range=[0, 1.2, 0.2], x_length=5.6, y_length=4.2, tips=False,
                  axis_config={"color": GREY_D, "include_ticks": True}).move_to([-3.4, -0.05, 0])
        xt = VGroup(*[label(rf"{v}$^\circ$", font_size=17, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (0, 20, 40, 60, 80)])
        yt = VGroup(*[label(f"{v:.1f}", font_size=17, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2)])
        xl = label(r"viewing angle from the normal", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"reflected under uniform light of radiance 1 \ (albedo)", font_size=17, color=GREY_A).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT)
        one = DashedLine(ax.c2p(0, 1), ax.c2p(80, 1), color=GREY_A, stroke_width=1.5)

        def series(model, param, col):
            pts = [(r["theta_deg"], r["quad"]) for r in rows if r["model"] == model and r["param"] == param]
            P = [ax.c2p(x, y) for x, y in pts]
            return VGroup(VMobject(color=col, stroke_width=3).set_points_as_corners(P),
                          *[Dot(p, radius=0.055, color=col) for p in P]), pts
        lam, lp = series("lambert", 1.0, YES)
        pho, pp = series("phong", 10.0, DATA)
        bli, bp = series("blinn_phong", 10.0, NO)
        g1, g1p = series("ggx", 0.1, KERN)
        g5, g5p = series("ggx", 0.5, KERN)
        g10, g10p = series("ggx", 1.0, KERN)
        tags = VGroup(
            label(r"Lambert", font_size=17, color=YES).next_to(ax.c2p(40, 1.0), UP, buff=0.08),
            label(r"Phong, \ $n = 10$", font_size=17, color=DATA).next_to(pho[-1], RIGHT, buff=0.1),
            label(rf"Blinn--Phong, \ $n = 10$: \ {bp[0][1]:.3f}", font_size=17, color=NO).next_to(
                ax.c2p(0, bp[0][1]), UR, buff=0.08).shift(RIGHT * 0.15),
            label(r"GGX $\alpha = 0.1$", font_size=17, color=KERN).next_to(g1[-1], RIGHT, buff=0.1),
            label(r"$\alpha = 0.5$", font_size=17, color=KERN).next_to(g5[-1], RIGHT, buff=0.1),
            label(r"$\alpha = 1$", font_size=17, color=KERN).next_to(g10[-1], RIGHT, buff=0.1))
        names = [("lambert", r"Lambert"), ("phong", r"Phong"), ("blinn_phong", r"Blinn--Phong"), ("ggx", r"GGX")]

        def sci(v):
            if v == 0:
                return r"0"
            e = int(math.floor(math.log10(v)))
            return rf"${v / 10 ** e:.0f}\times10^{{{e}}}$"
        tab = grid_table([r"BRDF", r"$\max |f(a,b) - f(b,a)| / \max f$"],
                         [[n, sci(rec[k])] for k, n in names], widths=[1.8, 3.4], row_h=0.38, font_size=18,
                         mono_cols=())
        tcap = label(r"reciprocity on 10{,}000 random pairs of directions", font_size=17, color=GREY_A)
        tblk = VGroup(tcap, tab).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([4.15, 1.7, 0])
        ggx_lost = 1 - g10p[0][1]
        bsrow = next(r for r in rows if r["model"] == "blinn_phong" and r["param"] == 10.0 and r["theta_deg"] == 0)
        notes = VGroup(
            wrapped_label(r"the white furnace: \ lit equally from every direction, \ a surface may return at most "
                          r"what it receives", 5.2, font_size=18, color=WHITE),
            wrapped_label(rf"the usual Blinn--Phong normalization is approximate: \ at $n = 10$ it returns "
                          rf"{bsrow['quad']:.3f} \ (Monte Carlo: \ {bsrow['mc']:.3f} $\pm$ {bsrow['mc_se']:.3f})",
                          5.2, font_size=18, color=NO),
            wrapped_label(rf"GGX at $\alpha = 1$ loses {100 * ggx_lost:.0f}\% head-on: \ light bouncing between "
                          r"facets more than once is left out of the model", 5.2, font_size=18, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(tblk, DOWN, buff=0.35).align_to(tblk, LEFT)
        with self.voiceover(
            "Every physical BRDF obeys two rules, and our instruments check both. <bookmark mark='a'/> Reciprocity: "
            "swapping the two directions gives the same value. On ten thousand random pairs our four models agree to"
            " rounding. <bookmark mark='b'/> Energy conservation: lit equally from every direction, in a white "
            "furnace, a surface must return at most one. <bookmark mark='c'/> Lambert returns exactly one. "
            "Normalized Phong returns one head-on, and less at grazing angles, where its lobe dips below the "
            "horizon. <bookmark mark='d'/> The usual Blinn-Phong normalization is only approximate: at exponent ten "
            "it creates energy, one point nought seven five. <bookmark mark='e'/> GGX keeps nearly everything when "
            "smooth, but at roughness one it loses more than two thirds head-on, because the model leaves out light "
            "that bounces between facets more than once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tblk))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), Create(one), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Create(lam), FadeIn(tags[0]))
            self.play(Create(pho), FadeIn(tags[1]))
            vo.wait_until("d")
            self.play(Create(bli), FadeIn(tags[2]), FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(Create(g1), Create(g5), Create(g10), FadeIn(tags[3:]), FadeIn(notes[2]), run_time=2)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, grid_table)
