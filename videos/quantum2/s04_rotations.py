from __future__ import annotations

import math

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (Projector, corner_wheel, label, ladder, load, mtex, note, num_table, sphere_img, why)

FACE_COLORS = ["#E06C75", "#E5C07B", "#61AFEF", "#98C379", "#C678DD", "#56B6C2"]


def Rx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def Ry(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def book(proj: Projector, R, size=(1.5, 1.0, 0.32)) -> VGroup:
    """A shaded box (a 'book') rotated by R, faces depth-sorted and back faces culled; world z is up."""
    a, b, c = (s / 2 for s in size)
    # world (x, y, z_up) -> projector world (X right, Y up, Z toward viewer) = (x, z, -y)
    M = np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])
    faces = [((1, 0, 0), [(a, -b, -c), (a, b, -c), (a, b, c), (a, -b, c)]),
             ((-1, 0, 0), [(-a, -b, -c), (-a, -b, c), (-a, b, c), (-a, b, -c)]),
             ((0, 1, 0), [(-a, b, -c), (-a, b, c), (a, b, c), (a, b, -c)]),
             ((0, -1, 0), [(-a, -b, -c), (a, -b, -c), (a, -b, c), (-a, -b, c)]),
             ((0, 0, 1), [(-a, -b, c), (a, -b, c), (a, b, c), (-a, b, c)]),
             ((0, 0, -1), [(-a, -b, -c), (-a, b, -c), (a, b, -c), (a, -b, -c)])]
    Rv = proj._rot()
    light = np.array([-0.4, 0.6, 0.7])
    light /= np.linalg.norm(light)
    polys = []
    for k, (n, vs) in enumerate(faces):
        nw = M @ (R @ np.array(n, float))
        nv = Rv @ nw
        if nv[2] <= 1e-6:
            continue
        P = np.array([M @ (R @ np.array(v, float)) for v in vs])
        pts = proj(P)
        shade = 0.45 + 0.55 * max(0.0, float(nv @ light))
        col = ManimColor(FACE_COLORS[k]).interpolate(ManimColor(BACKGROUND), 1 - shade)
        poly = Polygon(*pts, fill_color=col, fill_opacity=1, stroke_color=WHITE, stroke_width=1.2)
        polys.append((float(proj.depth(P).mean()), poly))
    polys.sort(key=lambda t: t[0])
    return VGroup(*[p for _, p in polys])


class Rotations(VoiceoverScene):
    def construct(self):
        self.noncommuting()
        self.algebra()
        self.ladder_derivation()
        self.spectrum()
        self.harmonics()

    # ------------------------------------------------------------------
    def noncommuting(self):
        pl = Projector(az=-0.55, el=0.38, scale=1.6, center=LEFT * 3.4 + DOWN * 0.3)
        pr = Projector(az=-0.55, el=0.38, scale=1.6, center=RIGHT * 3.4 + DOWN * 0.3)
        t = ValueTracker(0.0)

        def ang(tt, k):
            return PI / 2 * float(np.clip(2 * tt - k, 0, 1))

        bl = always_redraw(lambda: book(pl, Ry(ang(t.get_value(), 1)) @ Rx(ang(t.get_value(), 0))))
        br = always_redraw(lambda: book(pr, Rx(ang(t.get_value(), 1)) @ Ry(ang(t.get_value(), 0))))
        tl = MathTex(r"\text{first } x\text{, then } y", font_size=32).move_to(LEFT * 3.4 + UP * 2.6)
        tr = MathTex(r"\text{first } y\text{, then } x", font_size=32).move_to(RIGHT * 3.4 + UP * 2.6)
        q = label(r"$90^\circ$ turns about two axes", font_size=28, color=GREY_A).to_edge(UP, buff=0.3)
        neq = MathTex(r"\neq", font_size=72).move_to(DOWN * 0.3)
        axes_note = note(r"$x$ points right, $y$ into the screen, $z$ up").to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Rotations are the third symmetry, and the most interesting, because they don't commute. "
            "<bookmark mark='a'/> Turn a book a quarter turn about one axis and then about another; now do it in the "
            "opposite order. <bookmark mark='b'/> The book ends up facing a different way."
        ) as vo:
            self.add(bl, br)
            self.play(FadeIn(bl), FadeIn(br), FadeIn(tl), FadeIn(tr), FadeIn(q), FadeIn(axes_note))
            vo.wait_until("a")
            self.play(t.animate.set_value(1.0), run_time=4.0, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(neq))
        bl.clear_updaters()
        br.clear_updaters()
        self.clear_scene()
        e = load("symmetry")
        rows = [[f"{ep:g}", f"{ang:.5f}", f"{ang / ep**2:.4f}", f"{az:.4f}"]
                for ep, ang, az in zip(e["comm_eps"], e["comm_angle"], e["comm_axis_z"])]
        tab = num_table([r"\epsilon", r"\text{leftover angle}", r"\text{angle}/\epsilon^2", r"\text{axis}\cdot\hat z"], rows, font_size=32,
                        col_colors=[WHITE, C.ANGMOM, C.ANGMOM, WHITE]).move_to(DOWN * 0.9)
        loop = MathTex(r"R_x(\epsilon)\,R_y(\epsilon)\,R_x(-\epsilon)\,R_y(-\epsilon)", r"=", r"R_z(\epsilon^2) + O(\epsilon^3)", font_size=40)
        loop.to_edge(UP, buff=0.8)
        loop[2].set_color(C.ANGMOM)
        with self.voiceover(
            "Even for tiny turns: <bookmark mark='a'/> rotate by epsilon about x, then about y, then undo both, and "
            "you're left with a rotation about z by epsilon squared. <bookmark mark='b'/> Here are the numbers, for "
            "real rotation matrices: the leftover angle divided by epsilon squared goes to one, and its axis to z."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(loop))
            vo.wait_until("b")
            self.play(FadeIn(tab.header), Create(tab.rule), LaggedStart(*[FadeIn(r) for r in tab.rows], lag_ratio=0.3), run_time=2)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def algebra(self):
        r1 = MathTex(r"R_{\hat n}(\theta)", r"=", r"e^{-i\theta\,\hat n\cdot\hat{\mathbf J}/\hbar}", font_size=42)
        r1[2].set_color(C.ANGMOM)
        r2 = MathTex(r"e^{-i\epsilon \hat J_x/\hbar}e^{-i\epsilon \hat J_y/\hbar}e^{i\epsilon \hat J_x/\hbar}e^{i\epsilon \hat J_y/\hbar}",
                     r"=", r"1 - \frac{\epsilon^2}{\hbar^2}[\hat J_x, \hat J_y] + O(\epsilon^3)", font_size=36)
        r3 = MathTex(r"R_z(\epsilon^2)", r"=", r"1 - \frac{i\epsilon^2}{\hbar}\hat J_z + O(\epsilon^4)", font_size=36)
        r4 = MathTex(r"[\hat J_x, \hat J_y] = i\hbar\hat J_z", r",\quad", r"[\hat J_y, \hat J_z] = i\hbar\hat J_x", r",\quad",
                     r"[\hat J_z, \hat J_x] = i\hbar\hat J_y", font_size=38)
        r4.set_color(C.ANGMOM)
        g = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.55).move_to(UP * 0.4)
        w2 = why(r2, r"expand each exponential to second order", direction=DOWN, buff=0.08)
        box = SurroundingRectangle(r4, color=C.ANGMOM, buff=0.18, corner_radius=0.12)
        msg = label(r"one relation decides every possible value of angular momentum", font_size=28, color=GREY_A).next_to(box, DOWN, buff=0.35)
        with self.voiceover(
            "Each rotation is a unitary, <bookmark mark='a'/> e to the minus i theta J over h-bar, and the three "
            "generators are the components of angular momentum. <bookmark mark='b'/> Expand that loop of four rotations "
            "to second order, <bookmark mark='c'/> match it to the leftover rotation about z, <bookmark mark='d'/> and "
            "you get J x J y minus J y J x equals i h-bar J z, and the same for every cyclic pair. "
            "<bookmark mark='e'/> That one algebraic relation determines every possible value of angular momentum, "
            "without solving any equation."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(r1))
            vo.wait_until("b")
            self.play(Write(r2), FadeIn(w2))
            vo.wait_until("c")
            self.play(Write(r3))
            vo.wait_until("d")
            self.play(Write(r4), Create(box))
            vo.wait_until("e")
            self.play(FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ladder_derivation(self):
        rows = [
            MathTex(r"\hat J_\pm = \hat J_x \pm i\hat J_y", r",\quad", r"[\hat J_z, \hat J_\pm] = \pm\hbar\hat J_\pm", font_size=36),
            MathTex(r"\hat J_z\,(\hat J_\pm\ket{m})", r"=", r"(m \pm 1)\,\hbar\,(\hat J_\pm\ket{m})", font_size=36),
            MathTex(r"\hat J_\mp\hat J_\pm", r"=", r"\hat{\mathbf J}^2 - \hat J_z^2 \mp \hbar\hat J_z", font_size=36),
            MathTex(r"\hat J_+\ket{j} = 0", r"\;\Rightarrow\;", r"\hat{\mathbf J}^2 = \hbar^2 j(j + 1)", font_size=36),
            MathTex(r"\hat J_-\ket{j'} = 0", r"\;\Rightarrow\;", r"\hbar^2 j'(j' - 1) = \hbar^2 j(j + 1)\;\Rightarrow\; j' = -j", font_size=36),
            MathTex(r"-j \to j \text{ in whole steps}", r"\;\Rightarrow\;", r"2j \in \{0, 1, 2, 3, \dots\}", font_size=40),
        ]
        rows[5][2].set_color(C.ANGMOM)
        whys = [
            why(rows[0], r"from $[\hat J_x, \hat J_y] = i\hbar\hat J_z$ and its partners"),
            why(rows[1], r"$\hat J_+$ raises $m$ by one; $\hat J_-$ lowers it"),
            why(rows[2], r"multiply out"),
            why(rows[3], r"the top rung: the ladder must stop, since $\hat J_z^2 \le \hat{\mathbf J}^2$"),
            why(rows[4], r"the bottom rung, likewise"),
            None,
        ]
        step = ladder(self, rows, whys, keep=3, top=3.2, x=-3.0, buff=0.5)
        # the ladder picture, right side
        j = 3 / 2
        ms = [-1.5, -0.5, 0.5, 1.5]
        rungs = VGroup(*[Line(LEFT * 0.7, RIGHT * 0.7, color=C.ANGMOM, stroke_width=4).move_to(RIGHT * 4.2 + UP * (m * 0.72 - 2.15)) for m in ms])
        mtex_ = {-1.5: r"m = -\tfrac32", -0.5: r"m = -\tfrac12", 0.5: r"m = +\tfrac12", 1.5: r"m = +\tfrac32"}
        mlabs = VGroup(*[MathTex(mtex_[m], font_size=24, color=C.ANGMOM).next_to(r, RIGHT, buff=0.15) for m, r in zip(ms, rungs)])
        ups = VGroup(*[Arrow(rungs[i].get_left() + RIGHT * 0.15, rungs[i + 1].get_left() + RIGHT * 0.15, buff=0.05, color=C.RAISE,
                             stroke_width=4, tip_length=0.14) for i in range(3)])
        downs = VGroup(*[Arrow(rungs[i + 1].get_right() + LEFT * 0.15, rungs[i].get_right() + LEFT * 0.15, buff=0.05, color=C.LOWER,
                               stroke_width=4, tip_length=0.14) for i in range(3)])
        stop_t = MathTex(r"\hat J_+\ket{j} = 0", font_size=24, color=C.RAISE).next_to(rungs[-1], UP, buff=0.2)
        stop_b = MathTex(r"\hat J_-\ket{-j} = 0", font_size=24, color=C.LOWER).next_to(rungs[0], DOWN, buff=0.2)
        jl = MathTex(r"j = \tfrac32", font_size=28, color=C.ANGMOM).next_to(rungs, LEFT, buff=0.5)
        with self.voiceover(
            "Here's how. <bookmark mark='a'/> Combine J x and J y into J plus and J minus. Their commutator with J z is "
            "plus or minus h-bar times themselves, <bookmark mark='b'/> so J plus raises the z component by one unit of "
            "h-bar, and J minus lowers it. The total, J squared, commutes with all three components, so the whole ladder "
            "shares one value of J squared."
        ) as vo:
            vo.wait_until("a")
            step(0)
            self.play(LaggedStart(*[Create(r) for r in rungs], lag_ratio=0.15), FadeIn(mlabs), FadeIn(jl))
            vo.wait_until("b")
            step(1)
            self.play(LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.2), LaggedStart(*[GrowArrow(a) for a in downs], lag_ratio=0.2))
        with self.voiceover(
            "<bookmark mark='c'/> But J z squared can't exceed J squared, so the ladder has a top rung, where J plus gives "
            "zero, and a bottom rung. <bookmark mark='d'/> Multiply out J minus J plus, apply it to the top rung, and J "
            "squared equals h-bar squared, j times j plus one. <bookmark mark='e'/> Do the same at the bottom with J plus "
            "J minus, and the bottom rung must be at minus j. <bookmark mark='f'/> Getting from minus j to j takes a "
            "whole number of steps, so two j is a whole number."
        ) as vo:
            vo.wait_until("c")
            step(2)
            self.play(FadeIn(stop_t), FadeIn(stop_b))
            vo.wait_until("d")
            step(3)
            vo.wait_until("e")
            step(4)
            vo.wait_until("f")
            step(5)
            self.play(Create(SurroundingRectangle(rows[5], color=C.ANGMOM, buff=0.15, corner_radius=0.1)))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def spectrum(self):
        js = [0, 0.5, 1, 1.5, 2, 2.5]
        cols = VGroup()
        for k, j in enumerate(js):
            ms = np.arange(-j, j + 0.01, 1.0)
            half = abs(j - round(j)) > 0.1
            col = C.SPIN_UP if half else C.ANGMOM
            g = VGroup(*[Line(LEFT * 0.42, RIGHT * 0.42, color=col, stroke_width=4).move_to(UP * m * 0.55) for m in ms])
            jt = MathTex(r"j = " + ({0: "0", 0.5: r"\tfrac12", 1: "1", 1.5: r"\tfrac32", 2: "2", 2.5: r"\tfrac52"}[j]), font_size=30, color=col)
            jt.move_to(UP * 2.25)
            n = MathTex(f"{int(2 * j + 1)}" + (r"\text{ state}" if j == 0 else r"\text{ states}"), font_size=22, color=GREY_B).move_to(DOWN * 1.9)
            cols.add(VGroup(g, jt, n).shift(RIGHT * (k - 2.5) * 1.9 + DOWN * 0.1))
        orb = label(r"whole $j$: orbital, $\hat{\mathbf L} = \hat{\mathbf x}\times\hat{\mathbf p}$, phase $e^{im\varphi}$ must close up",
                    font_size=26, color=C.ANGMOM).to_edge(DOWN, buff=0.85)
        spin = label(r"half-integer $j$: spin; a $360^\circ$ turn gives $(-1)^{2j} = -1$", font_size=26, color=C.SPIN_UP).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "So j can be zero, one, two, <bookmark mark='a'/> but also one half, three halves. <bookmark mark='b'/> "
            "Orbital angular momentum, x cross p, only gives whole numbers, because the phase e to the i m phi has to "
            "come back to itself after a full turn. <bookmark mark='c'/> The half-integers are spin, and the algebra "
            "allowed them before anyone knew they were needed: a rotation by three hundred sixty degrees multiplies such "
            "a state by minus one, the sign Part 1 found for the electron."
        ) as vo:
            self.play(FadeIn(cols[0]), FadeIn(cols[2]), FadeIn(cols[4]))
            vo.wait_until("a")
            self.play(FadeIn(cols[1]), FadeIn(cols[3]), FadeIn(cols[5]))
            vo.wait_until("b")
            self.play(FadeIn(orb))
            vo.wait_until("c")
            self.play(FadeIn(spin))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def harmonics(self):
        e = load("symmetry")
        err = float(e["Lplus_err"].max())
        assert err < 1e-4
        spheres = Group(*[sphere_img(f"Y_2_{m}", height=1.85) for m in range(-2, 3)]).arrange(RIGHT, buff=0.75).move_to(UP * 0.9)
        mls = VGroup(*[MathTex(f"m = {m}".replace("-", "{-}"), font_size=28, color=C.ANGMOM).next_to(s, DOWN, buff=0.15)
                       for m, s in zip(range(-2, 3), spheres)])
        facs = [r"2", r"\sqrt6", r"\sqrt6", r"2"]
        arrs = VGroup()
        for i in range(4):
            a = CurvedArrow(spheres[i].get_top() + RIGHT * 0.25 + UP * 0.05, spheres[i + 1].get_top() + LEFT * 0.25 + UP * 0.05,
                            angle=-PI / 3, color=C.RAISE, stroke_width=3, tip_length=0.15)
            arrs.add(VGroup(a, MathTex(r"\hat L_+:\," + facs[i] + r"\hbar", font_size=22, color=C.RAISE).next_to(a, UP, buff=0.04)))
        title = MathTex(r"Y_2^m(\theta, \varphi)", font_size=36).to_edge(UP, buff=0.25).to_edge(LEFT, buff=0.6)
        form = MathTex(r"\hat L_+ Y_\ell^m = \hbar\sqrt{\ell(\ell + 1) - m(m + 1)}\;Y_\ell^{m+1}", font_size=32).next_to(mls, DOWN, buff=0.4)
        chk = note(r"checked on a $241 \times 720$ grid of $(\theta, \varphi)$: largest error $" + f"{err * 1e5:.1f}" + r"\times 10^{-5}$").next_to(form, DOWN, buff=0.15)
        cone_txt = MathTex(r"|\hat{\mathbf J}| = \hbar\sqrt{j(j + 1)} = \sqrt6\,\hbar", r"\;>\;", r"\max J_z = 2\hbar", font_size=32).to_edge(DOWN, buff=0.75)
        cone_n = label(r"so $\hat{\mathbf J}$ never points exactly along an axis: $\langle J_x^2 + J_y^2\rangle \ge j\hbar^2$", font_size=26,
                       color=GREY_A).to_edge(DOWN, buff=0.25)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.28)
        with self.voiceover(
            "Here's the ladder for j equals two, painted on spheres: <bookmark mark='a'/> the color is the phase of each "
            "spherical harmonic, the brightness its size. <bookmark mark='b'/> Going up, the phase winds once more "
            "around the vertical axis, <bookmark mark='c'/> and each step multiplies by exactly the square root of l "
            "times l plus one, minus m times m plus one, checked here on a grid to better than one part in ten thousand."
        ) as vo:
            self.play(FadeIn(title), FadeIn(wheel))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s) for s in spheres], lag_ratio=0.15), FadeIn(mls))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(a) for a in arrs], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(Write(form), FadeIn(chk))
        with self.voiceover(
            "And because J squared is j times j plus one, h-bar squared, while J z is at most j h-bar, "
            "<bookmark mark='a'/> angular momentum can never point exactly along an axis: the other two components can "
            "never both be zero."
        ) as vo:
            self.play(FadeOut(chk), FadeOut(form))
            self.play(Write(cone_txt))
            vo.wait_until("a")
            self.play(FadeIn(cone_n))
        self.wait(0.4)
        self.clear_scene()
