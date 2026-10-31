from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai4.common import GRAD, PART, VALUE, load


def warp(p):
    x, y = p[0], p[1]
    return np.array([x + 0.45 * math.sin(1.1 * y), y + 0.45 * math.sin(1.1 * x), 0.0])


def jac(x, y):
    return np.array([[1.0, 0.495 * math.cos(1.1 * y)], [0.495 * math.cos(1.1 * x), 1.0]])


def clip_segment_to_disk(a, b, center, radius):
    """Clip a sampled map segment to the lens, without moving its endpoints."""
    a, b, center = np.asarray(a, float), np.asarray(b, float), np.asarray(center, float)
    delta, offset = b - a, a - center
    aa = float(delta @ delta)
    if aa == 0:
        return (a, b) if float(offset @ offset) <= radius ** 2 else None
    bb = 2 * float(offset @ delta)
    cc = float(offset @ offset) - radius ** 2
    discriminant = bb ** 2 - 4 * aa * cc
    if discriminant < 0:
        return None
    root = math.sqrt(max(0.0, discriminant))
    first = max(0.0, (-bb - root) / (2 * aa))
    last = min(1.0, (-bb + root) / (2 * aa))
    return None if first > last else (a + first * delta, a + last * delta)


def grid_lines(lo, hi, n, f, steps=30, color=BLUE_C, width=2.0, clip_disk=None):
    """The lines x = const and y = const of a square [lo, hi]^2, n of each, mapped by f."""
    g = VGroup()
    for t in np.linspace(lo, hi, n):
        for horiz in (True, False):
            pts = [f(np.array([s, t]) if horiz else np.array([t, s])) for s in np.linspace(lo, hi, steps)]
            if clip_disk is None:
                g.add(VMobject(color=color, stroke_width=width).set_points_smoothly(pts))
            else:
                # Polyline pieces stay in the convex disk. Smoothing clipped
                # endpoints can overshoot the lens and imply a larger region.
                line = VMobject(color=color, stroke_width=width)
                for a, b in zip(pts, pts[1:]):
                    clipped = clip_segment_to_disk(a, b, *clip_disk)
                    if clipped is not None:
                        segment = VMobject().set_points_as_corners(clipped)
                        line.add_subpath(segment.points)
                g.add(line)
    return g


def depth_plot_range(data):
    """Show all measured log norms and seed extrema, without endpoint clamping."""
    values = np.concatenate([np.asarray(data[f"{name}{k}"], float).ravel()
                             for k in range(len(data["gains"])) for name in ("mean", "lo", "hi")])
    if not np.isfinite(values).all():
        raise ValueError("Depth plot requires finite recorded log norms")
    low = 6 * math.floor(min(float(values.min()) - 0.5, -0.5) / 6)
    high = 6 * math.ceil(max(float(values.max()) + 0.5, 0.5) / 6)
    return low, high


class Jacobian(VoiceoverScene):
    def construct(self):
        self.card()
        self.bend()
        self.det_and_chain()
        self.depth()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(3, r"Maps that bend: the Jacobian", r"What does a curved map look like up close?", part=PART)
        with self.voiceover("Chapter three. Maps that bend."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def bend(self):
        pl = NumberPlane(x_range=[-8, 8, 1], y_range=[-5, 5, 1], background_line_style={"stroke_color": BLUE_D,
                         "stroke_width": 1.5, "stroke_opacity": 0.7}, faded_line_ratio=1)
        pl.prepare_for_nonlinear_transform()
        p0 = np.array([1.2, 0.6])
        P = warp(p0)
        J = jac(*p0)
        c = np.array([4.0, -1.0, 0])
        R = 2.2
        lens = Circle(radius=R, color=WHITE, stroke_width=3).move_to(c)
        lens_bg = Circle(radius=R, stroke_width=0, fill_color=BACKGROUND, fill_opacity=1).move_to(c)
        r = ValueTracker(1.6)

        def inset():
            rr = r.get_value()
            k = R * 0.62 / rr

            def curved(q):
                return c + k * (warp(p0 + q) - P)

            def straight(q):
                return c + k * np.array([*(J @ q), 0])

            return VGroup(grid_lines(-rr, rr, 7, curved, color=BLUE_C, width=3, clip_disk=(c, R * 0.98)),
                          grid_lines(-rr, rr, 7, straight, color=GRAD, width=2,
                                     clip_disk=(c, R * 0.98)).set_opacity(0.8))

        ins = always_redraw(inset)
        spot = always_redraw(lambda: Circle(radius=r.get_value() * 1.25, color=WHITE, stroke_width=2).move_to(P))
        dot = glow_dot(P, color=WHITE, radius=0.07, layers=3)
        Jt = MathTex(r"J = \begin{bmatrix} \partial f_1/\partial x & \partial f_1/\partial y \\ \partial f_2/\partial x & "
                     r"\partial f_2/\partial y \end{bmatrix}", font_size=36, color=GRAD).to_corner(UL, buff=0.45)
        Jb = BackgroundRectangle(Jt, color=BACKGROUND, fill_opacity=0.9, buff=0.12)
        key = VGroup(label(r"the map", font_size=24, color=BLUE_C), label(r"its Jacobian", font_size=24, color=GRAD))
        key.arrange(RIGHT, buff=0.5).next_to(lens, DOWN, buff=0.15)
        tag = label(r"illustrative map", font_size=22, color=GREY_B).to_corner(DL, buff=0.35)
        with self.voiceover(
            "Now let a function take a whole vector to another vector, the way a layer of a network does. "
            "<bookmark mark='a'/> Here's one that bends the plane: the grid lines curve. <bookmark mark='b'/> But zoom "
            "in close to any point, and the curves straighten out. Up close, every smooth map looks like a matrix: "
            "its Jacobian, the table of all its partial derivatives."
        ) as vo:
            self.play(Create(pl, lag_ratio=0.05), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(pl.animate.apply_function(warp), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(dot), Create(spot), FadeIn(lens_bg), Create(lens), FadeIn(ins), FadeIn(key))
            self.play(r.animate.set_value(0.08), run_time=4.0, rate_func=smooth)
            self.play(FadeIn(Jb), Write(Jt))
        ins.clear_updaters()
        spot.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def det_and_chain(self):
        p0 = np.array([1.2, 0.6])
        J = jac(*p0)
        det = float(np.linalg.det(J))
        dc = definition_card(
            r"the Jacobian",
            r"For differentiable $f: \mathbb{R}^n \to \mathbb{R}^m$, the $m \times n$ matrix of partial derivatives, $J_{ij} = "
            r"\partial f_i / \partial x_j$: the one matrix with $f(x + h) = f(x) + J\,h + o(\|h\|)$. \ A gradient is the "
            r"Jacobian of a function with one output, stood up as a column.", width=12.6, font_size=26)
        dc.to_edge(UP, buff=0.3)
        sq = Square(side_length=1.4, stroke_width=0, fill_color=VALUE, fill_opacity=0.5).move_to([-5.0, -1.4, 0])
        par = Polygon(*[np.array([*(J @ v), 0]) * 1.4 + np.array([-1.9, -1.4, 0]) for v in
                        (np.array([-0.5, -0.5]), np.array([0.5, -0.5]), np.array([0.5, 0.5]), np.array([-0.5, 0.5]))],
                      stroke_width=0, fill_color=GRAD, fill_opacity=0.55)
        arrow_ = Arrow([-4.1, -1.4, 0], [-3.1, -1.4, 0], color=GREY_B, stroke_width=4)
        dl = MathTex(rf"\text{{area factor}} = |\det J| = {abs(det):.2f}", font_size=34, color=GRAD).move_to([-3.4, -3.0, 0])
        colors = {r"J_{f \circ g}(x)": WHITE, r"J_f(g(x))": GRAD, r"J_g(x)": VALUE}
        chain = cmath(r"J_{f \circ g}(x)", "=", r"J_f(g(x))", r"\,", r"J_g(x)", colors=colors, font_size=44)
        chain.move_to([3.4, -1.55, 0])
        cw = label(r"one map after another: \\ multiply their Jacobians", font_size=26, color=GREY_A).next_to(chain, DOWN, buff=0.3)
        shapes = label(r"$(m \times k)\,(k \times n)$: \ the shapes chain like the maps", font_size=22, color=GREY_B)
        shapes.next_to(cw, DOWN, buff=0.3)
        cells = VGroup(*[Square(side_length=0.36, stroke_color=GRAD, stroke_width=1.5, fill_color=GRAD, fill_opacity=0.15)
                         for _ in range(15)]).arrange_in_grid(rows=3, cols=5, buff=0)
        cells.move_to([3.2, 0.15, 0])
        rb = Brace(cells, LEFT, color=GREY_B)
        rl = label(r"$m$ outputs", font_size=22, color=GREY_A).next_to(rb, LEFT, buff=0.1)
        cb = Brace(cells, UP, color=GREY_B)
        cl_ = label(r"$n$ inputs", font_size=22, color=GREY_A).next_to(cb, UP, buff=0.08)
        jij = MathTex(r"J_{ij}", font_size=24, color=GRAD).move_to(cells[7])
        shape_pic = VGroup(cells, rb, rl, cb, cl_, jij)
        with self.voiceover(
            "In general, a map from n numbers to m numbers has an m by n Jacobian: one row per output, one column "
            "per input, the one matrix that makes the straight-line guess best. A gradient is the special case of a "
            "single output. <bookmark mark='a'/> For this two-dimensional map, the absolute value of the Jacobian's "
            "determinant, from part three, gives the local area factor. <bookmark mark='b'/> And the chain rule for maps is matrix "
            "multiplication: the Jacobian of one map after another is the product of their Jacobians, each taken "
            "where its input lands. Applying this chain rule backwards is the basis of backpropagation, as chapter five will show."
        ) as vo:
            self.play(FadeIn(dc, shift=UP * 0.2))
            self.play(FadeIn(shape_pic), FadeIn(sq), GrowArrow(arrow_))
            vo.wait_until("a")
            self.play(TransformFromCopy(sq, par), FadeIn(dl))
            vo.wait_until("b")
            self.play(Write(chain))
            self.play(FadeIn(cw), FadeIn(shapes))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def depth(self):
        d = load("depth")
        gains = [float(g) for g in d["gains"]]
        L = int(d["L"])
        cols = [C.SURPRISE, GRAD, WHITE, C.TRUE_P, C.BITS]
        ymin, ymax = depth_plot_range(d)
        g = axes([0, L, 10], [ymin, ymax, 6], x_length=7.2, y_length=4.8,
                 xlabel=r"depth: \ how many layers the gradient crosses",
                 ylabel=r"maximum stretch of $J_L \cdots J_1$: \ mean $\log_{10}\|\cdot\|_2$",
                 xticks=[0, 20, 40, 60], yticks=list(range(ymin, ymax + 1, 6)), center=[-2.0, -0.4, 0])
        ax = g.ax
        xs = np.arange(1, L + 1)
        curves, labs = VGroup(), VGroup()
        for k, gn in enumerate(gains):
            m = np.asarray(d[f"mean{k}"])
            curves.add(VGroup(band(ax, xs, d[f"lo{k}"], d[f"hi{k}"], cols[k], 0.15), curve(ax, xs, m, cols[k], 3)))
            labs.add(label(rf"gain ${gn:g}$", font_size=22, color=cols[k]).next_to(ax.c2p(L, float(m[-1])),
                                                                                RIGHT, buff=0.15))
        head = label(rf"${L}$ tanh layers, \ weights scaled by a gain \ (computed, ${int(d['seeds'])}$ seeds)", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.3)
        m0, m4, m2 = (float(np.asarray(d[f"mean{k}"])[-1]) for k in (0, 4, 2))
        steady = abs(m2) < 1
        verdict = ("At gain one, its mean log size stays within one power of ten of zero." if steady else
                   "Even at gain one, its mean log size ends more than one power of ten from zero.")
        bound = MathTex(r"\|J_L\cdots J_1\|_2 \le \prod_{\ell=1}^{L}\|J_\ell\|_2", font_size=28)
        if bound.width > 3.7:
            bound.scale_to_fit_width(3.7)
        bound.move_to([4.5, 1.45, 0])
        meaning = label(r"an upper bound, \ not equality \\ maximum stretch, \ not every direction", font_size=22,
                        color=GREY_A).next_to(bound, DOWN, buff=0.3)
        spread = label(r"curve: \ mean log norm \\ band: \ minimum--maximum over seeds", font_size=22,
                       color=GREY_B).move_to([4.5, -2.3, 0])
        with self.voiceover(
            "Chain many maps and their Jacobians multiply. The product's norm is at most the product of the "
            "individual norms; it need not equal it. Here is a deep stack of "
            f"tanh layers, {L} of them, with random weights scaled by a gain. We plot the mean log of the product's "
            "largest singular value, with the range across seeds. This is the maximum possible amplification, "
            "also for the transposed product in backpropagation, not what happens in every direction. "
            "A norm below one shrinks every direction; a norm above one allows growth in some direction. "
            f"<bookmark mark='a'/> At gain {gains[0]:g}, the mean log size ends at {m0:.1f}. "
            f"<bookmark mark='b'/> At gain {gains[4]:g}, it ends at {m4:.1f}. "
            f"<bookmark mark='c'/> {verdict} Such products help explain vanishing and exploding gradients. "
            "Parts 9 and 10 return to how initialization affects their scale."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(bound), FadeIn(meaning), FadeIn(spread))
            self.play(Create(curves[2][1]), FadeIn(labs[2]), run_time=1.2)
            vo.wait_until("a")
            self.play(FadeIn(curves[0]), FadeIn(curves[1]), FadeIn(labs[0]), FadeIn(labs[1]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(curves[3]), FadeIn(curves[4]), FadeIn(labs[3]), FadeIn(labs[4]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(curves[2][0]), Indicate(labs[2], color=WHITE, scale_factor=1.0))
        self.wait(0.3)
        self.clear_scene()
