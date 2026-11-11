from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs51.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load


def sci(x: float) -> str:
    """A positive number with two significant figures, in scientific notation when it is small."""
    m, e = f"{x:.1e}".split("e")
    e = int(e)
    if e == 0:
        return f"{x:.1f}"
    if e >= -2:
        return f"{x:.{1 - e}f}"
    return rf"${m} \times 10^{{{e}}}$"


class Projection(VoiceoverScene):
    def construct(self):
        self.card()
        self.similar()
        self.matrix()
        self.frustum()
        self.depth()
        self.precision()
        self.fighting()

    def card(self):
        card = chapter_card(2, r"Perspective projection", r"Why do far things look small, \ and what does it cost?",
                            lit=(1974, 1992), extra=((1974, r"Sutherland and Hodgman: \ clipping"),
                                                     (1992, r"OpenGL 1.0")), part=PART)
        with self.voiceover("Chapter two. Perspective projection."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def similar(self):
        head = label(r"Similar triangles", font_size=36).to_edge(UP, buff=0.3)
        E = np.array([-6.0, -0.9, 0])
        n = 1.6
        Y = 2.2
        d = ValueTracker(3.4)
        axis = Line(E, E + RIGHT * 6.6, color=GREY_C, stroke_width=1.5)
        screen = Line(E + RIGHT * n + DOWN * 0.5, E + RIGHT * n + UP * 2.6, color=DATA, stroke_width=4)
        eye = Dot(E, radius=0.1, color=WHITE)
        el = label(r"eye", font_size=19, color=GREY_A).next_to(eye, LEFT, buff=0.12)
        sl = label(r"screen", font_size=19, color=DATA).next_to(screen, UP, buff=0.1)

        def P():
            return E + RIGHT * d.get_value() + UP * Y

        def Q():
            return E + RIGHT * n + UP * (Y * n / d.get_value())
        big = always_redraw(lambda: Polygon(E, E + RIGHT * d.get_value(), P(), color=GREY_B, stroke_width=1.5,
                                            fill_color=GREY_B, fill_opacity=0.08))
        small = always_redraw(lambda: Polygon(E, E + RIGHT * n, Q(), color=HEAD, stroke_width=2, fill_color=HEAD,
                                              fill_opacity=0.25))
        ray = always_redraw(lambda: DashedLine(E, P(), color=GREY_A, stroke_width=2))
        obj = always_redraw(lambda: Line(E + RIGHT * d.get_value(), P(), color=YES, stroke_width=6))
        img = always_redraw(lambda: Line(E + RIGHT * n, Q(), color=HEAD, stroke_width=7))
        lab = always_redraw(lambda: VGroup(
            MathTex(r"y", font_size=30, color=YES).next_to(E + RIGHT * d.get_value() + UP * Y / 2, RIGHT, buff=0.1),
            MathTex(r"y'", font_size=30, color=HEAD).next_to(E + RIGHT * n + UP * Y * n / d.get_value() / 2, LEFT,
                                                             buff=0.1)))
        bn = BraceBetweenPoints(E, E + RIGHT * n, DOWN, color=GREY_B)
        bnl = MathTex(r"n", font_size=28, color=GREY_A).next_to(bn, DOWN, buff=0.05)
        bd = always_redraw(lambda: VGroup(b := BraceBetweenPoints(E + DOWN * 0.55, E + DOWN * 0.55 + RIGHT *
                                                                  d.get_value(), DOWN, color=GREY_B),
                                          MathTex(r"d", font_size=28, color=GREY_A).next_to(b, DOWN, buff=0.05)))
        rows = VGroup(
            MathTex(r"\frac{y'}{n}", r"=", r"\frac{y}{d}", font_size=44),
            MathTex(r"y'", r"=", r"\frac{n\,y}{d}", font_size=44),
            MathTex(r"x'", r"=", r"\frac{n\,x}{d}", r",\quad", r"y'", r"=", r"\frac{n\,y}{d}", font_size=44),
        ).arrange(DOWN, buff=0.5).move_to([4.0, 0.9, 0])
        for r in rows:
            r[0].set_color(HEAD)
        whys = VGroup(note(r"same angles, \ same ratios", font_size=18), note(r"multiply by $n$", font_size=18),
                      note(r"$d = -z$: \ distance in front of the eye", font_size=18))
        for r, w in zip(rows, whys):
            w.next_to(r, RIGHT, buff=0.25)
        for r, w in zip(rows, whys):
            g = VGroup(r, w)
            if g.get_right()[0] > 6.8:
                g.shift(LEFT * (g.get_right()[0] - 6.8))
        foot = wrapped_label(r"dividing by depth is not linear: \ no $4 \times 4$ matrix can do it alone", 4.8,
                             font_size=21, color=NO).next_to(rows, DOWN, buff=0.5).align_to(rows, RIGHT)
        with self.voiceover(
            "Why do far things look small? Leon Battista Alberti wrote down the painter's answer in 1435, and it is "
            "similar triangles. <bookmark mark='a'/> Put the eye at the origin and a screen at distance n. A point "
            "at height y and distance d is seen along this line, which crosses the screen at height "
            "y prime. <bookmark mark='b'/> The small triangle and the large one have the same angles, so y prime "
            "over n equals y over d. <bookmark mark='c'/> Multiply through: y prime is n y over d. "
            "<bookmark mark='d'/> Twice as far, half as tall. Every "
            "coordinate is divided by depth, and division is not linear, so no matrix can do it alone."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(eye), FadeIn(el))
            vo.wait_until("a")
            self.play(Create(screen), FadeIn(sl), FadeIn(big), FadeIn(obj), Create(ray), FadeIn(bn), FadeIn(bnl),
                      FadeIn(bd))
            self.play(FadeIn(small), FadeIn(img), FadeIn(lab))
            vo.wait_until("b")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("c")
            self.play(TransformMatchingTex(rows[0].copy(), rows[1]), FadeIn(whys[1]))
            self.play(TransformMatchingTex(rows[1].copy(), rows[2]), FadeIn(whys[2]))
            vo.wait_until("d")
            self.play(d.animate.set_value(6.4), run_time=3)
            self.play(FadeIn(foot), d.animate.set_value(3.2), run_time=2)
        self.wait(0.4)
        self.clear_scene()

    def matrix(self):
        fr = load("frustum")
        M = np.array(fr["matrix"])
        head = label(r"Put depth in $w$, \ divide once", font_size=36).to_edge(UP, buff=0.3)
        mat = MathTex(r"\begin{pmatrix} x_c \\ y_c \\ z_c \\ w_c \end{pmatrix}", r"=",
                      r"\begin{pmatrix} c/a & 0 & 0 & 0 \\ 0 & c & 0 & 0 \\ 0 & 0 & A & B \\ 0 & 0 & -1 & 0 "
                      r"\end{pmatrix}", r"\begin{pmatrix} x \\ y \\ z \\ 1 \end{pmatrix}", font_size=32)
        mat[2].set_color(HEAD)
        mat.move_to([-3.5, 1.6, 0])
        cnote = note(r"$c = \cot(\mathrm{fov}/2)$, \ $a$ = aspect ratio", font_size=17).next_to(mat, DOWN, buff=0.12)
        div = MathTex(r"x_{ndc} = \frac{x_c}{w_c} = \frac{c\,x}{a\,d}", r",\quad", r"w_c = -z = d", font_size=32,
                      color=WHITE).next_to(cnote, DOWN, buff=0.35)
        div[2].set_color(YES)
        num = MathTex(r"\begin{pmatrix} " + r" \\ ".join(" & ".join(f"{v:.3f}".rstrip("0").rstrip(".") if v else "0"
                                                                       for v in row) for row in M) +
                      r" \end{pmatrix}", font_size=26, color=GREY_A)
        numl = note(rf"ours: \ field of view ${fr['fovy_deg']:g}^\circ$, \ aspect 4:3, \ near {fr['near']:g}, \ "
                    rf"far {fr['far']:g}", font_size=17)
        VGroup(num, numl).arrange(DOWN, buff=0.1).next_to(div, DOWN, buff=0.3)
        rows = VGroup(
            MathTex(r"z_{ndc}", r"=", r"\frac{A z + B}{-z}", r"=", r"-A + \frac{B}{d}", font_size=34),
            MathTex(r"-A + \frac{B}{n} = -1", r",\quad", r"-A + \frac{B}{f} = +1", font_size=34),
            MathTex(r"A = \frac{f+n}{n-f}", r",\quad", r"B = \frac{2fn}{n-f}", font_size=34),
            MathTex(r"z_{ndc}", r"=", r"\frac{f+n}{f-n}", r"-", r"\frac{2fn}{f-n}\cdot\frac{1}{d}", font_size=34),
        ).arrange(DOWN, buff=0.42).move_to([3.6, 0.35, 0])
        rows[3][4].set_color(HEAD)
        whys = VGroup(note(r"the third row, \ after the division", font_size=17),
                      note(r"near plane to $-1$, \ far plane to $+1$", font_size=17),
                      note(r"subtract; \ solve", font_size=17),
                      note(r"affine in $1/d$, \ not in $d$", font_size=17, color=HEAD))
        for r, w in zip(rows, whys):
            w.next_to(r, DOWN, buff=0.08)
        with self.voiceover(
            "The fourth coordinate rescues us. <bookmark mark='a'/> The projection matrix scales x and y by the "
            "focal factor, and its last row copies the distance into w. Nothing has been divided yet: these are "
            "clip coordinates. <bookmark mark='b'/> The hardware then divides by w, once per vertex, and that one "
            "division is all of perspective. <bookmark mark='c'/> The third row must keep depth for the depth "
            "buffer. After the division it is minus A plus B over d. <bookmark mark='d'/> Ask that the near plane "
            "land at minus one and the far plane at plus one, <bookmark mark='e'/> and solve. "
            "<bookmark mark='f'/> Stored depth is affine in one over the distance, not in the distance, and that "
            "will cost us precision."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(mat), FadeIn(cnote))
            vo.wait_until("b")
            self.play(FadeIn(div), FadeIn(num), FadeIn(numl))
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(whys[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), FadeIn(whys[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]), FadeIn(whys[2]))
            vo.wait_until("f")
            self.play(TransformMatchingTex(rows[0].copy(), rows[3]), FadeIn(whys[3]))
        self.wait(0.4)
        self.clear_scene()

    def frustum(self):
        fr = load("frustum")
        P = np.array(fr["matrix"])
        C = np.array(fr["corners_eye"])
        edges = fr["edges"]
        near, far = fr["near"], fr["far"]
        flip = np.diag([1.0, 1.0, -1.0, 1.0])        # draw NDC depth so that near stays nearer the eye
        head = label(r"The frustum folds into a cube", font_size=36).to_edge(UP, buff=0.3)
        s, ox, oy = 0.85, -4.6, -0.4

        def scr(p):
            x, y, D = p
            return np.array([s * (D + 0.42 * x) + ox, s * (y + 0.25 * x) + oy, 0.0])

        def warp(pts, t):
            M = (1 - t) * np.eye(4) + t * (flip @ P)
            H = np.c_[pts, np.ones(len(pts))] @ M.T
            Q = H[:, :3] / H[:, 3:4]
            Q[:, 2] = -Q[:, 2]                        # display depth: distance in front of the eye
            return Q
        th = math.tan(math.radians(fr["fovy_deg"]) / 2)
        slices_d = [near + (far - near) * k / 4 for k in (1, 2, 3)]
        slices = [np.array([(sx * dd * th * fr["aspect"], sy * dd * th, -dd) for sx, sy in
                            ((-1, -1), (1, -1), (1, 1), (-1, 1))]) for dd in slices_d]
        t = ValueTracker(0.0)

        def draw():
            Q = [scr(q) for q in warp(C, t.get_value())]
            g = VGroup()
            for a, b in edges:
                col = DATA if a < 4 and b < 4 else (LAM if a >= 4 and b >= 4 else GREY_B)
                g.add(Line(Q[a], Q[b], color=col, stroke_width=3))
            for S in slices:
                R = [scr(q) for q in warp(S, t.get_value())]
                g.add(Polygon(*R, color=HEAD, stroke_width=1.8, fill_color=HEAD, fill_opacity=0.08))
            return g
        box = always_redraw(draw)
        eye = Dot(scr((0, 0, 0)), radius=0.08, color=WHITE)
        eyel = label(r"eye", font_size=17, color=GREY_A).next_to(eye, DOWN, buff=0.1)
        legend = VGroup(*[label(tx, font_size=18, color=c) for tx, c in
                          ((r"near face", DATA), (r"far face", LAM), (r"three equally spaced slices", HEAD))]).arrange(
            RIGHT, buff=0.4).to_edge(DOWN, buff=0.3).set_x(-3.2)
        zs = [float((P[2, 2] * (-dd) + P[2, 3]) / dd) for dd in slices_d]     # z_ndc = (A z + B) / d, z = -d
        notes = VGroup(
            wrapped_label(r"multiply by the projection matrix, \ divide by $w$: \ the viewing frustum becomes the "
                          r"cube $[-1, 1]^3$, \ \textbf{normalized device coordinates}", 5.6, font_size=19,
                          color=WHITE),
            wrapped_label(r"projective at every stage: \ straight lines stay straight, \ flat faces stay flat", 5.6,
                          font_size=19, color=YES),
            wrapped_label(r"equal steps in depth crowd towards the far face: \ $d$ = " +
                          ", ".join(f"{v:g}" for v in slices_d) + r" land at $z_{ndc}$ = " +
                          ", ".join(f"{v:.2f}" for v in zs), 5.6, font_size=19, color=HEAD),
            wrapped_label(r"clip triangles first, \ while it is all still linear \ ($-w \le x, y, z \le w$); \ then "
                          r"stretch the cube onto the screen's pixels", 5.6, font_size=19, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, -0.1, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here is what the matrix and the division do to space. This is the frustum, the "
            "truncated pyramid the camera sees between the near and far planes, with three equally spaced "
            "slices. <bookmark mark='b'/> Apply the map a little at a time. The far face "
            "shrinks and the near face grows, until the frustum is a cube from minus one to one in every "
            "coordinate. <bookmark mark='c'/> Straight lines stay straight all the way. <bookmark mark='d'/> But "
            "look at the slices: equally spaced in the world, they crowd towards the far face. "
            "<bookmark mark='e'/> Triangles are clipped before the division, while everything "
            "is still linear, and the cube is finally stretched onto the pixels."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eye), FadeIn(eyel))
            vo.wait_until("a")
            self.play(FadeIn(box), FadeIn(legend), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeOut(eye), FadeOut(eyel), t.animate.set_value(1.0), run_time=5, rate_func=smooth)
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
            vo.wait_until("e")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def depth(self):
        cv = load("depth")["curve"]
        dist, win = np.array(cv["distance"]), np.array(cv["window"])
        lg = np.log10(dist)
        head = label(r"Where the depth values go", font_size=36).to_edge(UP, buff=0.3)
        ax = axes([-1, 3, 1], [0, 1, 0.25], x_length=5.6, y_length=3.2, x_label=r"distance from the eye",
                  y_label=r"stored depth", xticks=[-1, 0, 1, 2, 3], yticks=[0, 0.5, 1],
                  fx=lambda v: {-1: "0.1", 0: "1", 1: "10", 2: "100", 3: "1000"}[int(v)])
        ax.move_to([-3.3, 0.3, 0])
        curve = ax.ax.plot_line_graph(lg.tolist(), win.tolist(), line_color=HEAD, add_vertex_dots=False,
                                      stroke_width=4)
        d50 = float(np.interp(0.5, win, dist))
        d90 = float(np.interp(0.9, win, dist))
        marks = VGroup()
        for dv, wv, txt in ((d50, 0.5, rf"half by {d50:.2f}"), (d90, 0.9, rf"90\% by {d90:.2f}")):
            p = ax.ax.c2p(math.log10(dv), wv)
            marks.add(VGroup(Dot(p, radius=0.07, color=NO), DashedLine(ax.ax.c2p(-1, wv), p, color=NO,
                                                                         stroke_width=1.5),
                             label(txt, font_size=18, color=NO).next_to(p, RIGHT, buff=0.15)))
        cap = note(rf"near {cv['near']:g}, \ far {cv['far']:g}; \ computed", font_size=16).next_to(ax, DOWN,
                                                                                                buff=0.05)
        # an illustrative 4-bit buffer, near 1, far 16: stored depth k / 15 sits at distance 16 / (16 - k)
        x0, x1, yb = 0.8, 6.6, -1.3
        ruler = Line([x0, yb, 0], [x1, yb, 0], color=GREY_C, stroke_width=2)

        def X(dv):
            return x0 + (x1 - x0) * (dv - 1) / 15
        ticks = VGroup(*[Line([X(16 / (16 - k)), yb - 0.18, 0], [X(16 / (16 - k)), yb + 0.18, 0], color=HEAD,
                              stroke_width=2.5) for k in range(16)])
        nums = VGroup(*[label(f"{v}", font_size=16, color=GREY_B).next_to([X(v), yb, 0], DOWN, buff=0.25)
                        for v in (1, 2, 4, 8, 16)])
        rt = label(r"a 4-bit depth buffer: \ its 16 values", font_size=20, color=HEAD).next_to(ruler, UP, buff=1.0)
        rn = note(r"illustrative: \ near 1, \ far 16; \ value $k$ sits at distance $16/(16-k)$", font_size=16).next_to(
            nums, DOWN, buff=0.15)
        gap = BraceBetweenPoints([X(8), yb + 0.25, 0], [X(16), yb + 0.25, 0], UP, color=NO)
        gl = label(r"one step", font_size=17, color=NO).next_to(gap, UP, buff=0.05)
        with self.voiceover(
            "How much does that crowding matter? <bookmark mark='a'/> Plot stored depth against distance, for a "
            "near plane at a tenth of a unit and a far plane at a thousand. "
            "<bookmark mark='b'/> Half of the whole range is used up before twice the near distance, and ninety "
            "percent before distance one. <bookmark mark='c'/> Depth buffers store integers. Picture one with only "
            "four bits: its sixteen values sit at sixteen over sixteen minus k. Half of them lie before distance "
            "two. <bookmark mark='d'/> And a single step covers the whole back half of the scene, from eight to "
            "sixteen."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ax), FadeIn(cap))
            self.play(Create(curve), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(marks[0]))
            self.play(FadeIn(marks[1]))
            vo.wait_until("c")
            self.play(Create(ruler), FadeIn(nums), FadeIn(rt), FadeIn(rn))
            self.play(LaggedStart(*[GrowFromCenter(tk) for tk in ticks], lag_ratio=0.15), run_time=2.5)
            vo.wait_until("d")
            self.play(GrowFromCenter(gap), FadeIn(gl))
        self.wait(0.4)
        self.clear_scene()

    def precision(self):
        tab_rows = load("depth")["table"]
        head = label(r"The smallest gap a 24-bit buffer can see", font_size=36).to_edge(UP, buff=0.3)
        nears = sorted({r["near"] for r in tab_rows})
        dists = sorted({r["distance"] for r in tab_rows})
        cell = {(r["near"], r["distance"]): r for r in tab_rows}
        rows = [[f"{nv:g}"] + [sci(cell[(nv, dv)]["resolvable"]) for dv in dists] for nv in nears]
        tab = grid_table([r"near plane"] + [rf"at {dv:g}" for dv in dists], rows, widths=[2.0, 2.1, 2.1, 2.1, 2.1],
                         row_h=0.55, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        for i in range(1, len(rows) + 1):
            tab.cells[i][0].set_color(DATA)
        for c in range(1, len(dists) + 1):
            tab.cells[1][c].set_color(NO)
            tab.cells[len(rows)][c].set_color(YES)
        sub = note(rf"far plane {tab_rows[0]['far']:g}; \ found by bisection on the depth mapping, \ and checked "
                   r"against the closed form", font_size=17).next_to(tab, DOWN, buff=0.2)
        form = MathTex(r"\Delta", r"\approx", r"\frac{d^2\,(f-n)}{f\,n\,(2^{b}-1)}", r"\approx",
                       r"\frac{d^2}{n\,2^{b}}", font_size=40).next_to(sub, DOWN, buff=0.4)
        form[4].set_color(HEAD)
        fn = note(r"for $f \gg n$: \ grows with distance squared; \ the near plane matters, \ the far plane hardly "
                  r"at all", font_size=19, color=HEAD).next_to(form, DOWN, buff=0.2)
        with self.voiceover(
            "How close can two surfaces be before the buffer cannot tell them apart? <bookmark mark='a'/> Our "
            "transform module finds the smallest resolvable gap for a twenty-four-bit buffer by bisection, "
            "and checks it against a closed form. <bookmark mark='b'/> With the near plane at a "
            "hundredth of a unit, two surfaces at distance a thousand must be about six units apart. With it at one, "
            "six hundredths will do. <bookmark mark='c'/> The closed form says why: the gap grows with the square "
            "of the distance and shrinks in proportion to the near distance, while the far plane hardly matters. "
            "So the cheapest fix is not more bits: it is pushing the near plane out."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(sub))
            vo.wait_until("b")
            self.play(Indicate(tab.cells[1][len(dists)], color=NO), Indicate(tab.cells[len(rows)][len(dists)],
                                                                             color=YES))
            vo.wait_until("c")
            self.play(Write(form))
            self.play(FadeIn(fn))
        self.wait(0.4)
        self.clear_scene()

    def fighting(self):
        zf = load("depth")["fighting"]
        head = label(r"Z-fighting", font_size=36).to_edge(UP, buff=0.3)
        r0 = zf[0]
        bars = VGroup()
        W = 5.4
        for r in zf:
            col = NO if r["share"] > 0.5 else (HEAD if r["share"] > 0 else YES)
            name = label(rf"near {r['near']:g}, \ {r['bits']} bits", font_size=20, color=WHITE)
            frame = Rectangle(width=W, height=0.42, stroke_color=GREY_C, stroke_width=1.2)
            fill = Rectangle(width=max(W * r["share"], 0.03), height=0.42, stroke_width=0, fill_color=col,
                             fill_opacity=0.85).align_to(frame, LEFT)
            val = label(rf"{100 * r['share']:.1f}\% wrong", font_size=19, color=col).next_to(frame, RIGHT, buff=0.15)
            name.next_to(frame, LEFT, buff=0.3)
            bars.add(VGroup(name, VGroup(frame, fill), val))
        bars.arrange(DOWN, buff=0.35)
        for b in bars:
            b[1].align_to(bars[0][1], LEFT)
            b[0].next_to(b[1], LEFT, buff=0.3)
            b[2].next_to(b[1], RIGHT, buff=0.15)
        bars.move_to([0, 0.7, 0])
        cap = note(rf"two planes {r0['gap']:g} apart at distance {r0['distance']:g}, \ far {r0['far']:g}, \ "
                   rf"{r0['pixels']:,} pixels: \ the share drawn with the farther plane on top".replace(",", "{,}"),
                   font_size=17).next_to(bars, DOWN, buff=0.3)
        notes = VGroup(
            wrapped_label(r"when two depths round to the same integer, \ draw order decides, \ and the surfaces "
                          r"flicker in stripes as the camera moves", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"modern engines also store depth \textbf{reversed} and in floating point: \ near at 1, \ "
                          r"far at 0, \ so Part 4's dense floats near zero meet the distant geometry that needs "
                          r"them", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "When two surfaces are closer than that gap, their depths round to the same integer, and drawing "
            "order decides which one shows. <bookmark mark='a'/> Our module draws two planes a "
            "hundredth of a unit apart at distance fifty. <bookmark mark='b'/> With a sixteen-bit buffer and the "
            "near plane at a hundredth, ninety-nine percent of the pixels show the wrong plane. Twenty-four bits "
            "cut it to about a third. <bookmark mark='c'/> Moving the near plane out to one helps less on "
            "its own, to about seventy percent; with both, every pixel is right. <bookmark mark='d'/> Modern engines also store depth "
            "reversed, in floating point, so that the dense floats near zero of Part 4 land on the distant "
            "geometry that needs them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(*[FadeIn(b[0]) for b in bars], *[FadeIn(b[1][0]) for b in bars], FadeIn(cap))
            vo.wait_until("b")
            for b in bars[:2]:
                self.play(GrowFromEdge(b[1][1], LEFT), FadeIn(b[2]))
            vo.wait_until("c")
            for b in bars[2:]:
                self.play(GrowFromEdge(b[1][1], LEFT), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
