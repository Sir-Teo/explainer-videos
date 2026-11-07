from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, image, load

# A 2D slice through a scene like our Whitted scene (illustrative): a floor, a mirror ball, a glass ball, a red
# ball and a point light.  Positions are in scene units of the left part of the frame.
FLOOR = -2.45
BALLS = [(np.array([1.2, -1.2]), 1.25, "mirror"), (np.array([-2.4, -1.8]), 0.65, "glass"),
         (np.array([-0.55, -2.05]), 0.4, "diffuse")]
LIGHT = np.array([2.3, 2.4])
EYE = np.array([-6.3, 1.2])
X_MIN, X_MAX, Y_MAX = -6.7, 2.7, 2.5
IOR = 1.5
COL = {"primary": WHITE, "shadow": HEAD, "reflection": DATA, "refraction": LAM}


def nearest(o, d):
    """Nearest hit t > 0 of the ray o + t d (d unit) in the 2D slice: (t, kind, normal, index) or None."""
    best = None
    for k, (c, r, kind) in enumerate(BALLS):
        oc = o - c
        b = d @ oc
        disc = b * b - (oc @ oc - r * r)
        if disc < 0:
            continue
        for t in (-b - math.sqrt(disc), -b + math.sqrt(disc)):
            if t > 1e-6:
                if best is None or t < best[0]:
                    p = o + t * d
                    best = (t, kind, (p - c) / r, k)
                break
    if d[1] < 0:
        t = (FLOOR - o[1]) / d[1]
        if t > 1e-6 and (best is None or t < best[0]) and X_MIN <= (o + t * d)[0] <= X_MAX:
            best = (t, "floor", np.array([0.0, 1.0]), -1)
    return best


def exit_t(o, d):
    """Distance to the edge of the drawing along a ray that hits nothing."""
    ts = []
    for lim, comp in ((X_MIN, 0), (X_MAX, 0), (Y_MAX, 1)):
        if abs(d[comp]) > 1e-9:
            t = (lim - o[comp]) / d[comp]
            if t > 0:
                ts.append(t)
    return min(ts) if ts else 1.0


def trace2d(o, d, kind="primary", depth=0, inside=False, max_depth=4):
    """Whitted's recursion in the slice: segments (start, end, kind) and shadow-ray segments with their verdict."""
    segs = []
    h = nearest(o, d)
    if h is None:
        segs.append((o, o + exit_t(o, d) * d, kind))
        return segs
    t, what, n, _ = h
    p = o + t * d
    segs.append((o, p, kind))
    if depth >= max_depth:
        return segs
    if what in ("floor", "diffuse"):
        to_l = LIGHT - p
        dist = np.linalg.norm(to_l)
        s = nearest(p + 1e-6 * n, to_l / dist)
        blocked = s is not None and s[0] < dist
        end = p + (s[0] if blocked else dist) * to_l / dist
        segs.append((p, end, "shadow" if not blocked else "blocked"))
    elif what == "mirror":
        r = d - 2 * (d @ n) * n
        segs += trace2d(p + 1e-6 * n, r, "reflection", depth + 1, inside, max_depth)
    elif what == "glass":
        nn = -n if inside else n
        eta = IOR if inside else 1 / IOR
        ci = -(d @ nn)
        s2 = eta * eta * (1 - ci * ci)
        r = d + 2 * ci * nn
        if not inside:
            segs += trace2d(p + 1e-6 * nn, r, "reflection", depth + 1, inside, max_depth)
        if s2 <= 1:
            tdir = eta * d + (eta * ci - math.sqrt(1 - s2)) * nn
            segs += trace2d(p - 1e-6 * nn, tdir / np.linalg.norm(tdir), "refraction", depth + 1, not inside,
                            max_depth)
    return segs


def P(v):
    return np.array([v[0], v[1], 0.0])


def scene2d():
    floor = Line(P((X_MIN, FLOOR)), P((X_MAX, FLOOR)), color=GREY_B, stroke_width=3)
    cols = {"mirror": GREY_A, "glass": TEAL_B, "diffuse": NO}
    balls = VGroup(*[Circle(radius=r, color=cols[k], stroke_width=3, fill_color=cols[k],
                            fill_opacity=0.12 if k != "diffuse" else 0.35).move_to(P(c)) for c, r, k in BALLS])
    names = VGroup(*[label(k, font_size=17, color=cols[k]).move_to(P(c)) for c, r, k in BALLS[:2]])
    light = Star(6, outer_radius=0.18, color=HEAD, fill_opacity=1).move_to(P(LIGHT))
    eye = Dot(P(EYE), radius=0.09, color=WHITE)
    el = label(r"eye", font_size=17, color=GREY_A).next_to(eye, UP, buff=0.1)
    ll = label(r"light", font_size=17, color=HEAD).next_to(light, UP, buff=0.1)
    return VGroup(floor, balls, names, light, eye, el, ll)


def segs_mob(segs):
    g = VGroup()
    for a, b, k in segs:
        if k == "blocked":
            g.add(DashedLine(P(a), P(b), color=NO, stroke_width=2.5, dash_length=0.08))
            g.add(Cross(scale_factor=0.09, stroke_color=NO, stroke_width=4).move_to(P(b)))
        elif k == "shadow":
            g.add(DashedLine(P(a), P(b), color=HEAD, stroke_width=2.5, dash_length=0.08))
        else:
            g.add(Line(P(a), P(b), color=COL[k], stroke_width=3))
    return g


class Rays(VoiceoverScene):
    def construct(self):
        self.card()
        self.primary()
        self.sphere()
        self.triangle()
        self.tree()
        self.snell()
        self.fresnel()

    def card(self):
        card = chapter_card(7, r"Ray tracing", r"What does the eye see along one line?", lit=(1968, 1980, 1997),
                            extra=((1968, r"Appel: \ ray casting"), (1980, r"Whitted: \ recursive rays"),
                                   (1997, r"M\"oller and Trumbore")), part=PART)
        with self.voiceover("Chapter seven. Ray tracing."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def primary(self):
        w = load("whitted")
        head = label(r"One ray through every pixel", font_size=36).to_edge(UP, buff=0.3)
        sc = scene2d()
        plane_x = -5.3
        ys = np.linspace(0.95, -0.55, 8)
        plane = Line(P((plane_x, 1.15)), P((plane_x, -0.75)), color=DATA, stroke_width=4)
        ticks = VGroup(*[Line(P((plane_x - 0.08, y)), P((plane_x + 0.08, y)), color=DATA, stroke_width=2)
                         for y in ys])
        pl = label(r"pixels", font_size=17, color=DATA).next_to(plane, DOWN, buff=0.1)
        rays, hits = VGroup(), VGroup()
        for y in ys:
            d = np.array([plane_x, y]) - EYE
            d = d / np.linalg.norm(d)
            h = nearest(EYE, d)
            end = EYE + (h[0] if h else exit_t(EYE, d)) * d
            rays.add(Line(P(EYE), P(end), color=WHITE, stroke_width=2))
            if h:
                hits.add(Dot(P(end), radius=0.07, color=HEAD))
        rows = VGroup(MathTex(r"\mathbf{r}(t) = \mathbf{o} + t\,\mathbf{d}", font_size=34),
                      MathTex(r"t_{\text{hit}} = \min_{\text{objects}}\ t_k > 0", font_size=34)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.8, 2.2, 0])
        img = image(w["image"], height=2.5).next_to(rows, DOWN, buff=0.4).set_x(4.8)
        cap = wrapped_label(rf"our Whitted ray tracer: \ {w['W']} $\times$ {w['H']} pixels, \ "
                            rf"{w['counts']['primary']:,} primary rays".replace(",", "{,}"), 3.9, font_size=18,
                            color=GREY_A).next_to(img, DOWN, buff=0.12)
        ill = note(r"a 2D slice, \ illustrative", font_size=16).move_to([-3.5, 2.65, 0])
        foot = wrapped_label(r"the z-buffer asks each triangle which pixels it covers; \ a ray asks each object "
                             r"where it is hit, \ and keeps the nearest", 9.0, font_size=19, color=WHITE).to_edge(
            DOWN, buff=0.3).set_x(-2.0)
        with self.voiceover(
            "Rasterization starts from the triangles; ray tracing starts from the eye. <bookmark mark='a'/> For "
            "every pixel, shoot a ray through the pixel's centre: a point o plus t times a direction d. "
            "<bookmark mark='b'/> Intersect it with every object and keep the nearest hit with t positive: that is "
            "what the pixel sees. Arthur Appel did this in 1968, for hidden surfaces and shadows. "
            "<bookmark mark='c'/> It is the z-buffer turned around: instead of each triangle asking which pixels it "
            "covers, each pixel asks which object it meets first. <bookmark mark='d'/> Our tracer sends nineteen "
            "thousand two hundred such rays for a small image, then, following Turner Whitted, keeps going."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sc), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(plane), FadeIn(ticks), FadeIn(pl), Write(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(r) for r in rays], lag_ratio=0.2), run_time=2)
            self.play(FadeIn(hits), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
            vo.wait_until("d")
            self.play(FadeIn(img), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def sphere(self):
        head = label(r"Ray meets sphere: \ a quadratic", font_size=36).to_edge(UP, buff=0.3)
        C = np.array([-3.8, 0.3, 0])
        R = 1.5
        circ = Circle(radius=R, color=TEAL_B, stroke_width=3).move_to(C)
        cd = Dot(C, radius=0.05, color=GREY_A)
        cl = MathTex(r"\mathbf{c}", font_size=28, color=GREY_A).next_to(cd, DR, buff=0.05)
        h = ValueTracker(0.4)

        def ray():
            y = C[1] + h.get_value()
            return Arrow([-6.6, y, 0], [-0.9, y, 0], buff=0, color=WHITE, stroke_width=3,
                         max_tip_length_to_length_ratio=0.04)

        def hits():
            g = VGroup()
            disc = R * R - h.get_value() ** 2
            if disc >= -1e-9:
                s = math.sqrt(max(disc, 0))
                for x in ((-s, s) if s > 1e-3 else (0,)):
                    g.add(Dot(C + np.array([x, h.get_value(), 0]), radius=0.09, color=HEAD))
            return g
        rm = always_redraw(ray)
        hm = always_redraw(hits)

        def verdict():
            disc = R * R - h.get_value() ** 2
            txt, c = ((r"$\Delta > 0$: \ two hits", YES) if disc > 0.02 else
                      (r"$\Delta = 0$: \ grazing", HEAD) if disc > -0.02 else (r"$\Delta < 0$: \ miss", NO))
            return label(txt, font_size=22, color=c).move_to(C + DOWN * 2.2)
        vm = always_redraw(verdict)
        rows = VGroup(
            MathTex(r"\lVert \mathbf{o} + t\,\mathbf{d} - \mathbf{c} \rVert^2", r"=", r"r^2", font_size=32),
            MathTex(r"(\mathbf{d}\cdot\mathbf{d})", r"\,t^2", r"+ 2\,", r"(\mathbf{d}\cdot(\mathbf{o}-\mathbf{c}))",
                    r"\,t", r"+", r"\lVert\mathbf{o}-\mathbf{c}\rVert^2 - r^2", r"= 0", font_size=28),
            MathTex(r"A", r"\,t^2", r"+ 2\,", r"B", r"\,t", r"+", r"C", r"= 0", font_size=32),
            MathTex(r"t = \frac{-B \pm \sqrt{\Delta}}{A}", r",\quad", r"\Delta = B^2 - AC", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.35).set_y(0.9)
        whys = VGroup(note(r"a point on the ray, \ at distance $r$ from the centre", font_size=17),
                      note(r"expand the dot product", font_size=17),
                      note(r"name the coefficients", font_size=17),
                      note(r"the smaller positive root is the visible hit", font_size=17, color=YES))
        for r, wy in zip(rows, whys):
            wy.next_to(r, DOWN, buff=0.06).align_to(r, LEFT)
        p4 = wrapped_label(r"in code, \ $q = -(B + \mathrm{sign}(B)\sqrt{\Delta})$, \ $t = q/A$ and $C/q$: \ no "
                           r"cancellation \ (Part 4)", 6.2, font_size=19, color=KERN).to_edge(DOWN, buff=0.4).set_x(3.3)
        with self.voiceover(
            "The simplest object is a sphere. <bookmark mark='a'/> A point on the ray is on the sphere when its "
            "distance from the centre is the radius. <bookmark mark='b'/> Expand the squared length as a dot "
            "product, and it is a quadratic in t. <bookmark mark='c'/> Name the coefficients A, B and C, "
            "<bookmark mark='d'/> and the roots follow. The discriminant decides everything. "
            "<bookmark mark='e'/> Slide the ray: positive, two hits, in and out; zero, the ray grazes the sphere; "
            "negative, it misses. The smaller positive root is the hit we see. <bookmark mark='f'/> And "
            "from Part 4: the textbook formula can subtract nearly equal numbers, so our code computes one root "
            "safely and the other from their product."
        ) as vo:
            self.play(FadeIn(head), Create(circ), FadeIn(cd), FadeIn(cl), FadeIn(rm), FadeIn(hm))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(vm))
            self.play(h.animate.set_value(R), run_time=2)
            self.wait(0.5)
            self.play(h.animate.set_value(R + 0.45), run_time=1.5)
            self.play(h.animate.set_value(0.4), run_time=1.5)
            vo.wait_until("f")
            self.play(FadeIn(p4))
        self.wait(0.4)
        self.clear_scene()

    def triangle(self):
        head = label(r"Ray meets triangle: \ M\"oller--Trumbore", font_size=36).to_edge(UP, buff=0.3)
        V0, V1, V2 = np.array([-6.0, -1.6, 0]), np.array([-1.6, -1.2, 0]), np.array([-4.2, 1.6, 0])
        tri = Polygon(V0, V1, V2, color=WHITE, stroke_width=2.5, fill_color=DATA, fill_opacity=0.15)
        vl = VGroup(MathTex(r"\mathbf{v}_0", font_size=28).next_to(V0, DL, buff=0.05),
                    MathTex(r"\mathbf{v}_1", font_size=28).next_to(V1, DR, buff=0.05),
                    MathTex(r"\mathbf{v}_2", font_size=28).next_to(V2, UP, buff=0.05))
        e1 = Arrow(V0, V1, buff=0, color=YES, stroke_width=4, max_tip_length_to_length_ratio=0.06)
        e2 = Arrow(V0, V2, buff=0, color=LAM, stroke_width=4, max_tip_length_to_length_ratio=0.06)
        el = VGroup(MathTex(r"\mathbf{e}_1", font_size=28, color=YES).next_to(e1, DOWN, buff=0.08),
                    MathTex(r"\mathbf{e}_2", font_size=28, color=LAM).next_to(e2.get_center(), LEFT, buff=0.15))
        u, v = 0.35, 0.3
        Q = V0 + u * (V1 - V0) + v * (V2 - V0)
        du = DashedLine(V0, V0 + u * (V1 - V0), color=YES, stroke_width=5)
        dv = DashedLine(V0 + u * (V1 - V0), Q, color=LAM, stroke_width=5)
        O = np.array([-5.9, 3.0, 0])
        ray = Arrow(O, Q + (Q - O) * 0.02, buff=0, color=HEAD, stroke_width=3, max_tip_length_to_length_ratio=0.06)
        ol = MathTex(r"\mathbf{o}", font_size=28, color=HEAD).next_to(O, LEFT, buff=0.08)
        hit = Dot(Q, radius=0.08, color=HEAD)
        rows = VGroup(
            MathTex(r"\mathbf{o} + t\,\mathbf{d}", r"=", r"(1-u-v)\,\mathbf{v}_0 + u\,\mathbf{v}_1 + v\,\mathbf{v}_2",
                    font_size=30),
            MathTex(r"-t\,\mathbf{d} + u\,\mathbf{e}_1 + v\,\mathbf{e}_2", r"=", r"\mathbf{s}", font_size=30),
            MathTex(r"\begin{pmatrix} -\mathbf{d} & \mathbf{e}_1 & \mathbf{e}_2 \end{pmatrix}"
                    r"\begin{pmatrix} t \\ u \\ v \end{pmatrix}", r"=", r"\mathbf{s}", font_size=30),
            MathTex(r"u = \frac{\mathbf{s}\cdot\mathbf{p}}{\mathbf{e}_1\cdot\mathbf{p}},\ \ "
                    r"v = \frac{\mathbf{d}\cdot\mathbf{q}}{\mathbf{e}_1\cdot\mathbf{p}},\ \ "
                    r"t = \frac{\mathbf{e}_2\cdot\mathbf{q}}{\mathbf{e}_1\cdot\mathbf{p}}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.35).set_y(0.8)
        rows[3].set_color(YES)
        whys = VGroup(note(r"the hit is a barycentric blend of the corners \ (chapter 3)", font_size=17),
                      note(r"$\mathbf{e}_1 = \mathbf{v}_1 - \mathbf{v}_0$, \ $\mathbf{e}_2 = \mathbf{v}_2 - "
                           r"\mathbf{v}_0$, \ $\mathbf{s} = \mathbf{o} - \mathbf{v}_0$", font_size=17),
                      note(r"three equations, \ three unknowns", font_size=17),
                      note(r"Cramer's rule with triple products: \ $\mathbf{p} = \mathbf{d}\times\mathbf{e}_2$, \ "
                           r"$\mathbf{q} = \mathbf{s}\times\mathbf{e}_1$", font_size=17, color=YES))
        for r, wy in zip(rows, whys):
            wy.next_to(r, DOWN, buff=0.06).align_to(r, LEFT)
        test = wrapped_label(r"hit when $u \ge 0$, \ $v \ge 0$, \ $u + v \le 1$ and $t > 0$: \ two cross products, "
                             r"\ four dot products, \ one division, \ and $u, v$ come out as texture weights for free",
                             6.4, font_size=19, color=HEAD).to_edge(DOWN, buff=0.35).set_x(2.9)
        with self.voiceover(
            "Most scenes are triangles. In 1997 Tomas Möller and Ben Trumbore published the test most ray tracers "
            "still use. <bookmark mark='a'/> A point of the triangle is a blend of its corners with barycentric "
            "weights, chapter three's again; the ray hits it when the two points agree. <bookmark mark='b'/> "
            "Measure everything from the first corner, along the two edges. <bookmark mark='c'/> That is a three by "
            "three linear system for t, u and v. <bookmark mark='d'/> Solve it by Cramer's rule: each determinant "
            "is a triple product, and they share two cross products, p and q. <bookmark mark='e'/> It is a hit when "
            "u and v are non-negative, sum to at most one, and t is positive; and u and v come out free, ready for "
            "texturing."
        ) as vo:
            self.play(FadeIn(head), Create(tri), FadeIn(vl))
            vo.wait_until("a")
            self.play(GrowArrow(ray), FadeIn(ol), FadeIn(hit), Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(GrowArrow(e1), GrowArrow(e2), FadeIn(el), TransformMatchingTex(rows[0].copy(), rows[1]),
                      FadeIn(whys[1]))
            self.play(Create(du), Create(dv))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(whys[3]))
            vo.wait_until("e")
            self.play(FadeIn(test))
        self.wait(0.4)
        self.clear_scene()

    def tree(self):
        w = load("whitted")
        c = w["counts"]
        head = label(r"Whitted: \ follow the light backwards", font_size=36).to_edge(UP, buff=0.3)
        sc = scene2d()
        aims = [(-4.6, -2.45), (0.0, -1.35), (-2.8, -1.4)]           # the floor, the mirror, the glass
        paths = []
        for a in aims:
            d = np.array(a) - EYE
            paths.append(segs_mob(trace2d(EYE, d / np.linalg.norm(d))))
        leg = VGroup(*[label(t, font_size=17, color=col) for t, col in (
            (r"primary", WHITE), (r"reflection", DATA), (r"refraction", LAM), (r"shadow ray", HEAD),
            (r"blocked: \ in shadow", NO))]).arrange(RIGHT, buff=0.35).to_edge(DOWN, buff=0.3).set_x(-2.0)
        ill = note(r"a 2D slice, \ illustrative", font_size=16).move_to([-3.5, 2.65, 0])
        names = [r"primary", r"shadow", r"reflection", r"refraction"]
        vals = [c[k] for k in names]
        chart = bar_chart(vals, names, [GREY_A, HEAD, DATA, LAM], height=2.3, bar_w=0.5, gap=0.5,
                          fmt_=lambda v: f"{v:,}".replace(",", "{,}"), font_size=17)
        chart.move_to([4.95, 0.9, 0])
        ct = label(rf"our tracer's rays, \ {w['W']} $\times$ {w['H']}", font_size=18, color=GREY_A).next_to(
            chart, UP, buff=0.2)
        tot = wrapped_label(rf"{c['total']:,} rays in all: \ {c['total'] / c['primary']:.2f} per "
                            r"pixel".replace(",", "{,}", 1), 3.6, font_size=19, color=WHITE).next_to(chart, DOWN,
                                                                                                buff=0.25)
        with self.voiceover(
            "Turner Whitted's paper of 1980 asked what happens after the first hit. <bookmark mark='a'/> At a matte "
            "surface, cast a shadow ray towards the light; if something is in the way, the point is in shadow. "
            "<bookmark mark='b'/> At a mirror, trace the reflected ray by the same procedure. Here it finds the red "
            "ball, at a point the mirror itself hides from the light. <bookmark mark='c'/> At glass, trace two: a "
            "reflected ray, and a refracted one that bends into the ball and out again. Each pixel grows a tree. "
            "<bookmark mark='d'/> Our tracer counts them: nineteen thousand two hundred primary rays, thirteen and a "
            "half thousand shadow rays, over four thousand each reflected and refracted: about two per pixel."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sc), FadeIn(ill))
            vo.wait_until("a")
            self.play(Create(paths[0]), FadeIn(leg[0]), FadeIn(leg[3]), run_time=2)
            vo.wait_until("b")
            self.play(Create(paths[1]), FadeIn(leg[1]), FadeIn(leg[4]), run_time=2)
            vo.wait_until("c")
            self.play(Create(paths[2]), FadeIn(leg[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(ct), FadeIn(chart), FadeIn(tot))
        self.wait(0.4)
        self.clear_scene()

    def snell(self):
        w = load("whitted")
        head = label(r"Refraction: \ Snell's law", font_size=36).to_edge(UP, buff=0.3)
        O = np.array([-3.6, 0.2, 0])
        surf = Line(O + LEFT * 3.0, O + RIGHT * 3.0, color=GREY_B, stroke_width=3)
        glass = Rectangle(width=6.0, height=2.4, stroke_width=0, fill_color=TEAL_B, fill_opacity=0.12).next_to(
            surf, DOWN, buff=0)
        gl = VGroup(label(r"glass, \ $n = 1.5$", font_size=18, color=TEAL_B).move_to(O + np.array([2.0, -2.0, 0])),
                    label(r"air, \ $n = 1$", font_size=18, color=GREY_A).move_to(O + np.array([2.2, 1.9, 0])))
        nrm = DashedLine(O + DOWN * 2.2, O + UP * 2.2, color=GREY_C, stroke_width=1.5)
        th = ValueTracker(20.0)
        crit = math.degrees(math.asin(1 / IOR))

        def rays():
            a = math.radians(th.get_value())
            inc = O + 2.1 * np.array([-math.sin(a), -math.cos(a), 0])
            g = VGroup(Arrow(inc, O, buff=0, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.08))
            s = IOR * math.sin(a)
            refl = O + 2.1 * np.array([math.sin(a), -math.cos(a), 0])
            if s <= 1:
                b = math.asin(s)
                g.add(Arrow(O, O + 2.1 * np.array([math.sin(b), math.cos(b), 0]), buff=0, color=LAM,
                            stroke_width=3, max_tip_length_to_length_ratio=0.08))
                g.add(Arrow(O, refl, buff=0, color=DATA, stroke_width=2, max_tip_length_to_length_ratio=0.08,
                            stroke_opacity=0.5))
            else:
                g.add(Arrow(O, refl, buff=0, color=DATA, stroke_width=4, max_tip_length_to_length_ratio=0.08))
            return g
        rm = always_redraw(rays)

        def readout():
            a = th.get_value()
            s = IOR * math.sin(math.radians(a))
            t2 = rf"$\theta_2 = {math.degrees(math.asin(s)):.0f}^\circ$" if s <= 1 else r"total internal reflection"
            return label(rf"inside the glass: \ $\theta_1 = {a:.0f}^\circ$, \ " + t2, font_size=20,
                         color=NO if s > 1 else WHITE).move_to(O + DOWN * 2.85)
        ro = always_redraw(readout)
        rows = VGroup(
            MathTex(r"n_1 \sin\theta_1 = n_2 \sin\theta_2", font_size=32),
            MathTex(r"\mathbf{t} = \eta\,\mathbf{d} + (\eta\cos\theta_1 - \cos\theta_2)\,\mathbf{n}", font_size=30),
            MathTex(r"\cos\theta_2 = \sqrt{1 - \eta^2 (1 - \cos^2\theta_1)}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.5, 1.5, 0])
        whys = VGroup(note(r"Snell; \ $\eta = n_1/n_2$", font_size=17),
                      note(r"the same law in vectors: \ no angles, \ no trigonometry", font_size=17),
                      note(r"no real root: \ total internal reflection", font_size=17, color=NO))
        for r, wy in zip(rows, whys):
            wy.next_to(r, DOWN, buff=0.06).align_to(r, LEFT)
        Cs = np.array([5.6, -1.8, 0])
        Rs = 0.95
        ball = Circle(radius=Rs, color=TEAL_B, stroke_width=2.5).move_to(Cs)
        a1, a2 = math.radians(160), math.radians(35)
        A = Cs + Rs * np.array([math.cos(a1), math.sin(a1), 0])
        B = Cs + Rs * np.array([math.cos(a2), math.sin(a2), 0])
        tri = VGroup(Line(Cs, A, color=GREY_B, stroke_width=1.5), Line(Cs, B, color=GREY_B, stroke_width=1.5),
                     Line(A, B, color=LAM, stroke_width=3))
        ang = VGroup(Angle(Line(A, Cs), Line(A, B), radius=0.3, color=HEAD),
                     Angle(Line(B, A), Line(B, Cs), radius=0.3, color=HEAD))
        sph = wrapped_label(rf"inside a ball the two radii make an isosceles triangle: \ a ray leaves at the angle it "
                            rf"entered, \ below ${crit:.1f}^\circ$; \ our tracer counted {w['tir']} total internal "
                            r"reflections", 3.4, font_size=17, color=HEAD).next_to(ball, LEFT, buff=0.3)
        with self.voiceover(
            "Glass bends light. <bookmark mark='a'/> Snell's law: the index of refraction times the sine of the "
            "angle is the same on both sides. <bookmark mark='b'/> A ray tracer wants it in vectors: the bent "
            "direction is a blend of the incoming direction and the normal, no angles needed. <bookmark mark='c'/> "
            "Going from glass into air, the square root can fail. <bookmark mark='d'/> Tilt the ray inside the "
            "glass: beyond about forty-two degrees there is no refracted ray, and all the light reflects. "
            "<bookmark mark='e'/> In a ball this never happens: the radii to entry "
            "and exit make an isosceles triangle, so a ray leaves at the angle it entered. Our tracer counted zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(glass), Create(surf), Create(nrm), FadeIn(gl), FadeIn(rm), FadeIn(ro))
            vo.wait_until("a")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(th.animate.set_value(60), run_time=4, rate_func=linear)
            vo.wait_until("e")
            self.play(Create(ball), Create(tri), Create(ang), FadeIn(sph))
        self.wait(0.4)
        self.clear_scene()

    def fresnel(self):
        w = load("whitted")
        head = label(r"How much reflects? \ Fresnel and Schlick", font_size=36).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 90, 15], y_range=[0, 1, 0.25], x_length=5.6, y_length=3.0,
                  axis_config={"color": GREY_D, "include_ticks": True}).move_to([-3.4, 0.4, 0])
        xt = VGroup(*[label(rf"{v}$^\circ$", font_size=16, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.1)
                      for v in (0, 30, 60, 90)])
        yt = VGroup(*[label(rf"{v:g}", font_size=16, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                      for v in (0, 0.5, 1)])
        xl = label(r"angle of incidence, \ air into glass", font_size=17, color=GREY_A).next_to(xt, DOWN, buff=0.1)
        yl = label(r"reflected fraction $R$", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.1).align_to(ax,
                                                                                                         LEFT)
        n1, n2 = 1.0, IOR
        r0 = ((n1 - n2) / (n1 + n2)) ** 2

        def exact(deg):
            ci = math.cos(math.radians(deg))
            st = n1 / n2 * math.sqrt(max(0.0, 1 - ci * ci))
            ct = math.sqrt(max(0.0, 1 - st * st))
            rs = ((n1 * ci - n2 * ct) / (n1 * ci + n2 * ct)) ** 2
            rp = ((n1 * ct - n2 * ci) / (n1 * ct + n2 * ci)) ** 2
            return (rs + rp) / 2

        def schlick(deg):
            return r0 + (1 - r0) * (1 - math.cos(math.radians(deg))) ** 5
        ce = ax.plot(exact, x_range=[0, 89.9, 0.5], color=GREY_A, stroke_width=3)
        cs = DashedVMobject(ax.plot(schlick, x_range=[0, 90, 0.5], color=YES, stroke_width=3), num_dashes=40)
        leg = VGroup(label(r"exact Fresnel", font_size=17, color=GREY_A),
                     label(r"Schlick", font_size=17, color=YES)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        leg.move_to(ax.c2p(22, 0.72))
        rows = VGroup(
            MathTex(r"R(\theta) = R_0 + (1 - R_0)(1 - \cos\theta)^5", font_size=32),
            MathTex(r"R_0 = \Big(\frac{n_1 - n_2}{n_1 + n_2}\Big)^2", r"= \Big(\frac{1 - 1.5}{1 + 1.5}\Big)^2",
                    rf"= {r0:.2f}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, 2.0, 0])
        rows[1][2].set_color(HEAD)
        img = image(w["image"], height=2.55).next_to(rows, DOWN, buff=0.35).set_x(3.4)
        cap = wrapped_label(r"our glass ball: \ reflected rays weighted $R$, \ refracted rays $1 - R$; \ its rim "
                            r"is a mirror", 5.4, font_size=18, color=GREY_A).next_to(img, DOWN, buff=0.12)
        with self.voiceover(
            "How much light reflects, and how much goes through? <bookmark mark='a'/> Fresnel's equations answer "
            "exactly: head on, glass reflects four per cent, climbing to all of it at grazing angles. "
            "<bookmark mark='b'/> In 1994 Christophe Schlick fitted this with one fifth power, <bookmark mark='c'/> "
            "anchored at the head-on value, four hundredths for glass. <bookmark mark='d'/> Our tracer gives each "
            "glass hit a reflected ray weighted by R and a refracted ray weighted by one minus R, and drops branches "
            "whose weight is negligible. So the rim of our glass ball mirrors the floor and the sky, while its middle "
            "shows the scene behind it, bent by refraction."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(Create(ce), FadeIn(leg[0]), run_time=2)
            vo.wait_until("b")
            self.play(Write(rows[0]), Create(cs), FadeIn(leg[1]), run_time=2)
            vo.wait_until("c")
            self.play(Write(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(img), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
