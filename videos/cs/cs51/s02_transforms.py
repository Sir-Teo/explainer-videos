from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load


def view(p, az=0.0, el=15.0):
    """Orthographic view of a 3D point: (screen x, screen y, depth towards the viewer), az and el in degrees."""
    a, e = math.radians(az), math.radians(el)
    e3 = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    e1 = np.array([-math.sin(a), math.cos(a), 0.0])
    e2 = np.cross(e3, e1)
    p = np.asarray(p, float)
    return float(p @ e1), float(p @ e2), float(p @ e3)


class Transforms(VoiceoverScene):
    def construct(self):
        self.card()
        self.linear()
        self.homogeneous()
        self.order()
        self.gimbal()
        self.quaternions()
        self.slerp()

    def card(self):
        card = chapter_card(1, r"Transforms and rotations", r"How does one matrix move a whole scene?",
                            lit=(1827, 1843, 1985), extra=((1827, r"M\"obius: \ homogeneous coordinates"),
                                                           (1843, r"Hamilton: \ quaternions"),
                                                           (1985, r"Shoemake: \ slerp")), part=PART)
        with self.voiceover("Chapter one. Transforms and rotations."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def linear(self):
        head = label(r"A matrix moves every point at once", font_size=36).to_edge(UP, buff=0.3)
        plane = NumberPlane(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1], x_length=5.4, y_length=4.5,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1})
        plane.move_to([-3.4, -0.35, 0])
        o = plane.c2p(0, 0)
        house = Polygon(*[plane.c2p(x, y) for x, y in ((0, 0), (1, 0), (1, 1), (0.5, 1.6), (0, 1))],
                        color=HEAD, fill_color=HEAD, fill_opacity=0.35, stroke_width=3)
        ex = Arrow(o, plane.c2p(1, 0), buff=0, color=DATA, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        ey = Arrow(o, plane.c2p(0, 1), buff=0, color=LAM, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        moving = VGroup(plane.copy().set_opacity(0.0), house, ex, ey)
        M = np.array([[0.8, -0.9], [0.6, 0.7]])
        eq = MathTex(r"\begin{pmatrix} x' \\ y' \end{pmatrix}", r"=",
                     r"\begin{pmatrix} 0.8 & -0.9 \\ 0.6 & 0.7 \end{pmatrix}", r"\begin{pmatrix} x \\ y \end{pmatrix}",
                     font_size=36).move_to([3.3, 2.0, 0])
        eq[2].set_color(HEAD)
        notes = VGroup(
            wrapped_label(r"the columns are where the two axis arrows land; \ every other point follows, \ "
                          r"because the map is linear", 5.8, font_size=20, color=WHITE),
            wrapped_label(r"rotation, \ scaling and shear are all like this, \ and two of them in a row are one "
                          r"matrix: \ their product", 5.8, font_size=20, color=YES),
            wrapped_label(r"but a linear map always keeps the origin where it is, \ so \textbf{moving} an object, \ "
                          r"translation, \ is not a matrix of this size", 5.8, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(eq, DOWN, buff=0.5)
        ill = note(r"illustrative matrix", font_size=16).next_to(plane, DOWN, buff=0.12)
        ring = Circle(radius=0.16, color=NO, stroke_width=4).move_to(o)
        with self.voiceover(
            "A scene is made of points, and a renderer's first job is to move them: each object into the world, "
            "and the world in front of the camera. <bookmark mark='a'/> A matrix moves every point at once. Its "
            "columns say where the two axis arrows land, and because the map is linear, everything else follows. "
            "<bookmark mark='b'/> Rotations, scalings and shears all work this way, and one after another is a "
            "single matrix, their product. <bookmark mark='c'/> But a linear map never moves the origin, so the "
            "simplest motion of all, sliding sideways, is not a matrix of this size."
        ) as vo:
            self.play(FadeIn(head), Create(plane), FadeIn(house), GrowArrow(ex), GrowArrow(ey), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(notes[0]))
            self.play(ApplyMatrix(M, moving, about_point=o), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]), Create(ring))
            self.play(Indicate(ring, color=NO))
        self.wait(0.4)
        self.clear_scene()

    def homogeneous(self):
        head = label(r"Homogeneous coordinates: \ translation becomes linear", font_size=36).to_edge(UP, buff=0.3)
        plane = NumberPlane(x_range=[-3, 4, 1], y_range=[-0.5, 2.5, 1], x_length=5.6, y_length=2.4,
                            background_line_style={"stroke_color": GREY_D, "stroke_width": 1})
        plane.move_to([-3.4, -1.3, 0])
        o = plane.c2p(0, 0)
        xl = MathTex(r"x", font_size=26, color=GREY_A).next_to(plane.c2p(4, 0), DOWN, buff=0.1)
        wl = MathTex(r"w", font_size=26, color=GREY_A).next_to(plane.c2p(0, 2.5), LEFT, buff=0.1)
        line = Line(plane.c2p(-3, 1), plane.c2p(4, 1), color=HEAD, stroke_width=3)
        ll = MathTex(r"w = 1", font_size=26, color=HEAD).next_to(plane.c2p(-3, 1), UP, buff=0.08).shift(RIGHT * 0.4)
        pts = VGroup(*[Dot(plane.c2p(x, 1), radius=0.08, color=DATA) for x in (-2, -1, 0, 1)])
        sheet = VGroup(*[Line(plane.c2p(x, 0), plane.c2p(x, 2), color=DATA, stroke_width=2, stroke_opacity=0.6)
                         for x in range(-3, 3)])
        rows = VGroup(
            MathTex(r"\begin{pmatrix} x' \\ y' \end{pmatrix}", r"=", r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}",
                    r"\begin{pmatrix} x \\ y \end{pmatrix}", r"+", r"\begin{pmatrix} t_x \\ t_y \end{pmatrix}",
                    font_size=34),
            MathTex(r"\begin{pmatrix} x' \\ y' \\ 1 \end{pmatrix}", r"=",
                    r"\begin{pmatrix} a & b & t_x \\ c & d & t_y \\ 0 & 0 & 1 \end{pmatrix}",
                    r"\begin{pmatrix} x \\ y \\ 1 \end{pmatrix}", font_size=34),
        )
        rows[0].move_to([3.4, 1.6, 0])
        rows[1].move_to([3.4, -0.6, 0])
        arrow = Arrow(rows[0].get_bottom(), rows[1].get_top(), buff=0.15, color=GREY_B, stroke_width=2,
                      max_tip_length_to_length_ratio=0.15)
        why = note(r"add a coordinate $w = 1$", font_size=19).next_to(arrow, RIGHT, buff=0.15)
        rows[1][2].set_color(HEAD)
        foot = wrapped_label(r"points carry $w = 1$ and are translated; \ directions \ (normals, \ light "
                             r"directions) \ carry $w = 0$ and are not; \ in 3D the matrices are $4 \times 4$",
                             6.4, font_size=20, color=YES).next_to(rows[1], DOWN, buff=0.45)
        side = note(r"one dimension down: \ a shear of the $(x, w)$ plane", font_size=17).next_to(plane, DOWN,
                                                                                                  buff=0.15)
        with self.voiceover(
            "The fix is to add one coordinate. <bookmark mark='a'/> A general motion is a matrix times the point, "
            "plus a constant. <bookmark mark='b'/> Give every point an extra coordinate, w, equal to one, and put "
            "the constant in a new last column: the matrix multiplies that one and adds the translation for us. "
            "<bookmark mark='c'/> Here is the picture one dimension down. Points live on the line where w is one. "
            "A shear of the plane keeps the origin fixed, as linear maps must, yet slides the line along itself: "
            "a translation. <bookmark mark='d'/> These are August Möbius's homogeneous coordinates of 1827. "
            "Directions get w equal to zero, so they turn but never move."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(rows[0]))
            vo.wait_until("b")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), GrowArrow(arrow), FadeIn(why))
            vo.wait_until("c")
            self.play(Create(plane), FadeIn(xl), FadeIn(wl), Create(line), FadeIn(ll), FadeIn(pts), FadeIn(side),
                      Create(sheet))
            self.play(ApplyMatrix(np.array([[1.0, 1.0], [0.0, 1.0]]), sheet, about_point=o),
                      pts.animate.shift(plane.c2p(1, 0) - o), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def order(self):
        d = load("order")
        head = label(r"Order matters: \ matrices apply right to left", font_size=36).to_edge(UP, buff=0.3)

        def panel(title, color, tex):
            pl = NumberPlane(x_range=[-2, 4, 1], y_range=[-1, 4, 1], x_length=4.2, y_length=3.5,
                             background_line_style={"stroke_color": GREY_D, "stroke_width": 1})
            t = MathTex(tex, font_size=32, color=color)
            cap = label(title, font_size=19, color=color)
            return VGroup(VGroup(t, cap).arrange(DOWN, buff=0.12), pl).arrange(DOWN, buff=0.25)
        left = panel(r"rotate $90^\circ$, \ then translate by 2", YES, r"T(2,0,0)\,R_z(90^\circ)")
        right = panel(r"translate by 2, \ then rotate $90^\circ$", NO, r"R_z(90^\circ)\,T(2,0,0)")
        VGroup(left, right).arrange(RIGHT, buff=1.4).next_to(head, DOWN, buff=0.3)

        def square(pl, pts, col, op=0.5):
            return Polygon(*[pl.c2p(p[0], p[1]) for p in pts], color=col, fill_color=col, fill_opacity=op,
                           stroke_width=2.5)
        sq = d["square"]
        ghosts = VGroup(square(left[1], sq, GREY_B, 0.15), square(right[1], sq, GREY_B, 0.15))
        a = square(left[1], sq, YES)
        b = square(right[1], sq, NO)
        ends = VGroup(
            label(r"corners " + ", ".join(f"({p[0]:g}, {p[1]:g})" for p in d["rotate_then_translate"]),
                  font_size=17, color=YES).next_to(left[1], DOWN, buff=0.15),
            label(r"corners " + ", ".join(f"({p[0]:g}, {p[1]:g})" for p in d["translate_then_rotate"]),
                  font_size=17, color=NO).next_to(right[1], DOWN, buff=0.15),
        )
        foot = wrapped_label(r"a renderer chains them: \ $P\,V\,M\,\mathbf{x}$: \ model to world, \ world to eye, \ "
                             r"eye to clip; \ the rightmost acts first", 12.4, font_size=20, color=HEAD).to_edge(
            DOWN, buff=0.25)
        with self.voiceover(
            "Now a chain of motions multiplies into one matrix. But matrix products do not commute, and they act "
            "from right to left. <bookmark mark='a'/> On the left, the unit square is rotated a quarter turn, then "
            "moved two units right. <bookmark mark='b'/> On the right, the same two matrices in the other order: "
            "moved first, then swung around the origin. <bookmark mark='c'/> The corners, computed by our "
            "transform module, land in different places. <bookmark mark='d'/> A renderer multiplies three such "
            "matrices: the model matrix places an object in the world, the view matrix puts the world in front of "
            "the camera, and the projection matrix, next chapter, prepares perspective."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left), FadeIn(right), FadeIn(ghosts), FadeIn(a), FadeIn(b))
            vo.wait_until("a")
            self.play(Rotate(a, PI / 2, about_point=left[1].c2p(0, 0)), run_time=1.5)
            self.play(a.animate.shift(left[1].c2p(2, 0) - left[1].c2p(0, 0)), run_time=1.5)
            vo.wait_until("b")
            self.play(b.animate.shift(right[1].c2p(2, 0) - right[1].c2p(0, 0)), run_time=1.5)
            self.play(Rotate(b, PI / 2, about_point=right[1].c2p(0, 0)), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(ends))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def gimbal(self):
        g = load("gimbal")
        head = label(r"Euler angles and gimbal lock", font_size=36).to_edge(UP, buff=0.3)
        eq = MathTex(r"R", r"=", r"R_z(\text{yaw})", r"\,R_y(\text{pitch})", r"\,R_x(\text{roll})", font_size=34)
        eq[2].set_color(KERN)
        eq[3].set_color(HEAD)
        eq[4].set_color(LAM)
        eq.move_to([-3.4, 2.3, 0])
        c = np.array([-3.4, -0.6, 0])
        L = 1.7
        p = ValueTracker(0.0)
        yaw_ax = Arrow(c + DOWN * 0.2, c + UP * L, buff=0, color=KERN, stroke_width=6,
                       max_tip_length_to_length_ratio=0.12)
        yl = label(r"yaw axis", font_size=19, color=KERN).next_to(yaw_ax.get_end(), RIGHT, buff=0.12)
        roll_ax = always_redraw(lambda: Arrow(
            c, c + L * np.array([math.cos(math.radians(p.get_value())), -math.sin(math.radians(p.get_value())), 0]),
            buff=0, color=LAM, stroke_width=6, max_tip_length_to_length_ratio=0.12))
        rl = always_redraw(lambda: label(r"roll axis", font_size=19, color=LAM).next_to(
            c + L * np.array([math.cos(math.radians(p.get_value())), -math.sin(math.radians(p.get_value())), 0]),
            RIGHT, buff=0.12))
        readout = always_redraw(lambda: label(rf"pitch ${p.get_value():.0f}^\circ$", font_size=22,
                                              color=HEAD).move_to(c + np.array([-1.6, -1.9, 0])))
        side = note(r"side view, \ schematic", font_size=16).move_to(c + np.array([1.3, -2.45, 0]))
        rows = []
        for r in g["rows"]:
            sv = r["singular_values"]
            rows.append([f"{r['pitch']:g}" + r"$^\circ$", f"{sv[0]:.3f}", f"{sv[1]:.3f}", f"{sv[2]:.3f}",
                         f"{r['rank']}"])
        tab = grid_table([r"pitch", r"$\sigma_1$", r"$\sigma_2$", r"$\sigma_3$", r"rank"], rows,
                         widths=[1.2, 1.15, 1.15, 1.15, 0.9], row_h=0.46, font_size=20, mono_cols=())
        tab.move_to([3.3, 1.0, 0])
        for i in range(1, len(rows) + 1):
            tab.cells[i][3].set_color(NO if i == len(rows) else HEAD)
        tab.cells[len(rows)][4].set_color(NO)
        form = MathTex(r"\sigma = 1,\ \sqrt{1 + \sin p},\ \sqrt{1 - \sin p}", font_size=30, color=WHITE).next_to(
            tab, DOWN, buff=0.35)
        n1 = wrapped_label(r"singular values of the map from angle rates to spin, \ computed; \ at $90^\circ$ one "
                           r"direction of turning is simply missing", 6.0, font_size=19, color=GREY_A).next_to(
            form, DOWN, buff=0.3)
        with self.voiceover(
            "Rotations in three dimensions are usually described by three angles: yaw, pitch and roll. "
            "<bookmark mark='a'/> Watch the roll axis as the pitch rises. At ninety degrees it lies along the yaw "
            "axis: yaw and roll now spin about the same line, and one way of turning is gone. This is gimbal lock. "
            "<bookmark mark='b'/> Our transform module measures it: the singular values of the map from angle "
            "rates to spin are one, and the square roots of one plus and one minus the sine of the pitch. "
            "<bookmark mark='c'/> At eighty-nine degrees the smallest is about one hundredth; at ninety, zero, "
            "and the rank falls to two."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq), GrowArrow(yaw_ax), FadeIn(yl), FadeIn(side))
            self.add(roll_ax, rl, readout)
            vo.wait_until("a")
            self.play(p.animate.set_value(89.0), run_time=4.0)
            self.play(p.animate.set_value(90.0), run_time=0.8)
            vo.wait_until("b")
            self.play(FadeIn(tab.cells[0][0]), *[FadeIn(m) for m in tab.cells[0][1:]], FadeIn(tab.rule),
                      *[FadeIn(m) for row in tab.cells[1:3] for m in row], FadeIn(form))
            vo.wait_until("c")
            self.play(*[FadeIn(m) for row in tab.cells[3:] for m in row], FadeIn(n1))
            self.play(Indicate(tab.cells[len(rows)][3], color=NO))
        self.wait(0.4)
        self.clear_scene()

    def quaternions(self):
        head = label(r"Quaternions", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            MathTex(r"i^2 = j^2 = k^2 = ijk = -1", font_size=40, color=GREY_A),
            MathTex(r"q", r"=", r"\big(\cos\tfrac{\theta}{2},\ \sin\tfrac{\theta}{2}\,\mathbf{n}\big)", font_size=40),
            MathTex(r"\mathbf{v}'", r"=", r"q\,", r"\mathbf{v}", r"\,q^{*}", font_size=40),
        ).arrange(DOWN, buff=0.45).move_to([-3.2, 0.6, 0])
        rows[1][2].set_color(HEAD)
        rows[2][3].set_color(DATA)
        whys = VGroup(
            note(r"Hamilton, \ 1843", font_size=18),
            note(r"a turn by $\theta$ about the unit axis $\mathbf{n}$", font_size=18),
            note(r"rotate a vector: \ two products", font_size=18),
        )
        for r, w in zip(rows, whys):
            w.next_to(r, DOWN, buff=0.1)

        def card(title, body, col):
            t = label(title, font_size=21, color=col)
            b = wrapped_label(body, 4.6, font_size=19, color=GREY_A)
            g = VGroup(t, b).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            box = SurroundingRectangle(g, buff=0.18, color=col, stroke_width=1.5, corner_radius=0.1)
            return VGroup(box, g)
        cards = VGroup(
            card(r"3 Euler angles", r"compact, \ readable, \ but singular at gimbal lock", NO),
            card(r"9 matrix entries", r"no singularity, \ but rounding drifts them away from a rotation", KERN),
            card(r"4 quaternion numbers", r"no singularity; \ renormalize to stay a rotation; \ $q$ and $-q$ are "
                 r"the same turn", YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "The cure is older than computers. <bookmark mark='a'/> In 1843 William Rowan Hamilton found numbers "
            "with three imaginary units whose squares are all minus one. <bookmark mark='b'/> A turn by theta about "
            "an axis is the unit quaternion of cosine and sine of half the angle. <bookmark mark='c'/> To rotate a "
            "vector, multiply by q on one side and its conjugate on the other. <bookmark mark='d'/> Euler angles "
            "are compact but singular. A matrix has nine numbers, which Part 4's rounding slowly pushes away from a "
            "rotation. A quaternion has four, never locks, and is repaired by dividing by its length."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r, w in zip("abc", rows, whys):
                vo.wait_until(mk)
                self.play(Write(r), FadeIn(w))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(cd, shift=LEFT * 0.2) for cd in cards], lag_ratio=0.5), run_time=2.5)
        self.wait(0.4)
        self.clear_scene()

    def slerp(self):
        s = load("slerp")
        head = label(r"Slerp: \ the shortest way round", font_size=36).to_edge(UP, buff=0.3)
        R = 2.0
        c = np.array([-3.6, -0.55, 0])
        sphere = Circle(radius=R, color=GREY_C, stroke_width=1.5).move_to(c)
        eqt = VGroup(*[ParametricFunction(lambda t, lat=lat: c + R * np.array(view(
            (math.cos(lat) * math.cos(t), math.cos(lat) * math.sin(t), math.sin(lat)))[:2] + (0,)),
            t_range=[0, TAU], color=GREY_D, stroke_width=1) for lat in (0.0, -0.7)])

        def path(pts, col):
            g = VGroup()
            P = [c + R * np.array(view(p)[:2] + (0,)) for p in pts]
            D = [view(p)[2] for p in pts]
            for k in range(len(P) - 1):
                front = D[k] + D[k + 1] >= 0
                g.add(Line(P[k], P[k + 1], color=col, stroke_width=5 if front else 2.5,
                           stroke_opacity=1.0 if front else 0.45))
            return g
        pe = path(s["euler"]["path"], NO)
        ps = path(s["slerp"]["path"], YES)
        ends = VGroup(Dot(pe[0].get_start(), color=WHITE, radius=0.08), Dot(pe[-1].get_end(), color=WHITE,
                                                                             radius=0.08))
        sl = note(r"the nose's path, \ 40 steps each", font_size=17).next_to(sphere, DOWN, buff=0.12)
        form = MathTex(r"\mathrm{slerp}(a, b; t) = \frac{\sin\big((1-t)\theta\big)}{\sin\theta}\,a + "
                       r"\frac{\sin(t\theta)}{\sin\theta}\,b", font_size=30).move_to([3.3, 2.35, 0])
        fn = note(r"$\cos\theta = a \cdot b$; \ Shoemake, \ 1985", font_size=17).next_to(form, DOWN, buff=0.1)
        ax = axes([0, 40, 10], [0, 7, 1], x_length=5.2, y_length=2.6, x_label=r"step",
                  y_label=r"degrees turned in each step", xticks=[0, 10, 20, 30, 40], yticks=[0, 2, 4, 6])
        ax.next_to(fn, DOWN, buff=0.35)
        ce = ax.ax.plot_line_graph(list(range(1, 41)), s["euler"]["per_step_deg"], line_color=NO,
                                   add_vertex_dots=False, stroke_width=3)
        cs = ax.ax.plot_line_graph(list(range(1, 41)), s["slerp"]["per_step_deg"], line_color=YES,
                                   add_vertex_dots=False, stroke_width=3)
        lab = VGroup(
            label(rf"Euler angles in a straight line: \ {s['euler']['total_deg']:.1f}$^\circ$ in all, \ uneven",
                  font_size=19, color=NO),
            label(rf"slerp: \ {s['slerp']['total_deg']:.1f}$^\circ$, \ constant speed \ (shortest: \ "
                  rf"{s['geodesic_deg']:.1f}$^\circ$)", font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, DOWN, buff=0.2)
        a, b = s["a"], s["b"]
        src = note(rf"from (yaw, pitch, roll) = ({a[0]:g}, {a[1]:g}, {a[2]:g}) to ({b[0]:g}, {b[1]:g}, {b[2]:g}) "
                   r"degrees; \ computed", font_size=16).to_edge(DOWN, buff=0.12)
        with self.voiceover(
            "Quaternions also answer the animator's question: how do you turn smoothly between two orientations? "
            "<bookmark mark='a'/> The naive way slides the three Euler angles in straight lines, and the nose "
            "wanders along this red path. <bookmark mark='b'/> Ken Shoemake's slerp, from 1985, follows the great "
            "circle between the two quaternions, with these sine weights. <bookmark mark='c'/> The green path turns "
            "the same amount every step, and its total is exactly the single rotation between the ends, about one "
            "hundred and thirty-nine degrees. <bookmark mark='d'/> The Euler path turns about two hundred and "
            "thirty-seven, unevenly. That is why game engines interpolate rotations with quaternions."
        ) as vo:
            self.play(FadeIn(head), Create(sphere), Create(eqt), FadeIn(ends), FadeIn(sl), FadeIn(src))
            vo.wait_until("a")
            self.play(Create(pe), run_time=2.5)
            vo.wait_until("b")
            self.play(Write(form), FadeIn(fn))
            vo.wait_until("c")
            self.play(Create(ps), FadeIn(ax), run_time=2.0)
            self.play(Create(cs), FadeIn(lab[1]))
            vo.wait_until("d")
            self.play(Create(ce), FadeIn(lab[0]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
