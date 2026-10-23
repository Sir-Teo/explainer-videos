from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai20.common import (DATA, DISC, GAN_C, PART, Plane, arrows, load, rgb_of, take_away, to_image)

SIM, ALT, EXTRA, OPT = GAN_C, C.BITS, C.INTERVAL, "#7FD3FF"


def traced(scene, plane, P, color, run_time, dot_r=0.07):
    """A point moving along a computed trajectory, leaving its path behind."""
    P = np.asarray(P)
    t = ValueTracker(0.0)
    pts = plane.pts(P)
    dot = Dot(pts[0], radius=dot_r, color=color)
    path = VMobject(stroke_color=color, stroke_width=2.5)
    path.set_points_as_corners([pts[0], pts[0]])

    def upd(m):
        k = int(t.get_value())
        m.set_points_as_corners(pts[:max(2, k + 1)])

    path.add_updater(upd)
    dot.add_updater(lambda d: d.move_to(pts[min(int(t.get_value()), len(pts) - 1)]))
    scene.add(path, dot)
    return t, dot, path


class Dynamics(VoiceoverScene):
    def construct(self):
        self.card()
        self.field()
        self.steps()
        self.dirac()
        self.hopping()

    def card(self):
        card = chapter_card(6, r"Why GANs spiral", r"What happens when two players follow their gradients?",
                            lit=(), part=PART)
        with self.voiceover("Chapter six. Why GANs spiral."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def field(self):
        b = load("bilinear")
        pl = Plane(5.2, center=[-3.2, -0.2, 0], box=1.9, axes_lines=True)
        ar = arrows(pl, b["field_pts"], b["field_vec"], color=GREY_B, max_len=0.42)
        xl = MathTex(r"x", font_size=30, color=GAN_C).next_to(pl, DOWN, buff=0.1)
        yl = MathTex(r"y", font_size=30, color=DISC).next_to(pl, LEFT, buff=0.1)
        rows = VGroup(
            cmath(r"\min_x \max_y \; f(x, y) = x\, y", font_size=36),
            cmath(r"\dot x = -\partial_x f = -y, \qquad \dot y = +\partial_y f = x", font_size=32),
            cmath(r"J = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}, \qquad \lambda = \pm i", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.3, 1.0, 0])
        note_ = label(r"no downhill anywhere: \ the field only turns", font_size=24, color=C.BITS)
        note_.next_to(rows, DOWN, buff=0.5)
        with self.voiceover(
            "The smallest game: one player picks x and wants x times y small, the other picks y and wants it "
            "large. <bookmark mark='a'/> Each follows its own gradient: x moves by minus y, y by plus x. <bookmark "
            "mark='b'/> Draw those velocities: no downhill anywhere, only turning. <bookmark mark='c'/> The "
            "Jacobian's eigenvalues are plus and minus i, pure rotation. Gradient descent was built for valleys; a "
            "game can be a whirlpool."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(xl), FadeIn(yl), Write(rows[0]))
            vo.wait_until("a")
            self.play(Write(rows[1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in ar], lag_ratio=0.01), run_time=2.0)
            vo.wait_until("c")
            self.play(Write(rows[2]), FadeIn(note_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def steps(self):
        b = load("bilinear")
        eta, T = float(b["eta"]), int(b["steps"])
        pl = Plane(5.4, center=[-3.1, -0.2, 0], box=1.9, axes_lines=True)
        ar = arrows(pl, b["field_pts"], b["field_vec"], color=GREY_D, max_len=0.35)
        M = cmath(r"\begin{pmatrix} x \\ y \end{pmatrix}_{t+1}", r"=",
                  r"\begin{pmatrix} 1 & -\eta \\ \eta & 1 \end{pmatrix}", r"\begin{pmatrix} x \\ y \end{pmatrix}_t",
                  font_size=32).move_to([3.4, 2.6, 0])
        lam = cmath(r"|\lambda|", r"=", r"|1 \pm i \eta|", r"=", r"\sqrt{1 + \eta^2}", r"> 1", font_size=32)
        lam.next_to(M, DOWN, buff=0.35)
        rs = np.asarray(b["sim_radius"])
        grow = label(rf"$\eta = {eta:g}$: \ after ${T}$ steps the radius is ${rs[-1]:.1f}\times$ the start",
                     font_size=22, color=SIM).next_to(lam, DOWN, buff=0.3)
        lg = legend([(SIM, r"simultaneous steps"), (ALT, r"alternating steps"),
                     (EXTRA, r"extragradient (Korpelevich, 1976)"),
                     (OPT, r"optimistic (Daskalakis et al., 2018)")], font_size=20).move_to([3.4, -1.3, 0])
        ra, re_, ro = (float(np.asarray(b[f"{k}_radius"])[-1]) for k in ("alt", "extra", "opt"))
        rs_end = float(rs[-1])
        with self.voiceover(
            "Take real steps, both players at once, step size eta: each step multiplies by this matrix. <bookmark "
            "mark='a'/> Its eigenvalues have size root one plus eta squared, more than one. <bookmark mark='b'/> "
            f"So simultaneous steps spiral out: after {T} steps the radius has grown {rs_end:.1f} times. <bookmark "
            f"mark='c'/> Taking turns closes the spiral into an orbit; its radius ends at {ra:.2f}. <bookmark "
            "mark='d'/> To converge, look ahead: extragradient steps with the gradient at a trial point, optimistic "
            f"descent extrapolates the last one. Both spiral in, to {re_:.2f} and {ro:.2f}."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(ar), Write(M))
            vo.wait_until("a")
            self.play(Write(lam))
            vo.wait_until("b")
            self.play(FadeIn(lg[0]))
            sim = np.asarray(b["sim"])
            n_in = int(np.argmax(np.abs(sim).max(1) > 1.85)) or len(sim)  # until it leaves the picture
            t1, d1, p1 = traced(self, pl, sim[:n_in], SIM, 1)
            self.play(t1.animate.set_value(n_in - 1), run_time=max(2.0, vo.until("c") - 1.0), rate_func=linear)
            self.play(FadeIn(grow))
            vo.wait_until("c")
            self.play(FadeIn(lg[1]))
            t2, d2, p2 = traced(self, pl, b["alt"], ALT, 1)
            self.play(t2.animate.set_value(T), run_time=max(2.0, vo.until("d") - 0.5), rate_func=linear)
            vo.wait_until("d")
            self.play(FadeIn(lg[2]), FadeIn(lg[3]))
            t3, d3, p3 = traced(self, pl, b["extra"], EXTRA, 1)
            t4, d4, p4 = traced(self, pl, b["opt"], OPT, 1)
            self.play(t3.animate.set_value(T), t4.animate.set_value(T), run_time=4.0, rate_func=linear)
        for m in (d1, p1, d2, p2, d3, p3, d4, p4):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dirac(self):
        b = load("bilinear")
        pl = Plane(5.0, center=[-3.3, -0.3, 0], box=1.6, axes_lines=True)
        th = MathTex(r"\theta", font_size=30, color=GAN_C).next_to(pl, DOWN, buff=0.1)
        ps = MathTex(r"\psi", font_size=30, color=DISC).next_to(pl, LEFT, buff=0.1)
        setup = VGroup(
            label(r"data: \ a single point at $0$", font_size=22, color=DATA),
            label(r"generator: \ a single point at $\theta$", font_size=22, color=GAN_C),
            label(r"discriminator: \ $D_\psi(x) = \psi\, x$", font_size=22, color=DISC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, 2.4, 0])
        r1 = cmath(r"\max_\psi \; V(\theta, \psi)", r"-", r"\tfrac{\gamma}{2}\, \psi^2", font_size=32)
        r1[2].set_color(C.BITS)
        r1.move_to([3.4, 0.7, 0])
        r1l = label(r"R1: \ penalize the discriminator's gradient on real data", font_size=20, color=C.BITS)
        r1l.next_to(r1, DOWN, buff=0.12)
        lg = legend([(SIM, r"simultaneous steps"), (ALT, r"alternating steps"),
                     (C.BITS, rf"with R1, \ $\gamma = {b['dirac_gamma']:g}$")], font_size=20).move_to([3.4, -1.0, 0])
        cite_ = cite(r"Mescheder, Geiger \& Nowozin, \textit{Which Training Methods for GANs do actually Converge?} "
                     r"(2018)", corner=DR)
        # the Dirac-GAN's own field: V = f(psi theta) + f(0), f(t) = -log(1 + e^-t); theta descends, psi ascends
        tt, pp = np.meshgrid(np.linspace(-1.4, 1.4, 11), np.linspace(-1.4, 1.4, 11))
        fp = 1 / (1 + np.exp(tt * pp))
        fld = arrows(pl, np.c_[tt.ravel(), pp.ravel()], np.c_[(-pp * fp).ravel(), (tt * fp).ravel()], color=GREY_B,
                     max_len=0.36).set_opacity(0.55)
        Ps = np.clip(b["dirac_sim"], -1.55, 1.55)
        n_out = int(np.argmax(np.abs(np.asarray(b["dirac_sim"])).max(1) > 1.55)) or len(Ps)
        with self.voiceover(
            "Real GANs do this. Lars Mescheder, Andreas Geiger and Sebastian Nowozin boiled one down to two "
            "numbers: data at zero, the generator at theta, a discriminator with slope psi. <bookmark mark='a'/> "
            "Around the equilibrium, the same rotation. <bookmark mark='b'/> Simultaneous steps spiral out; "
            "<bookmark mark='c'/> alternating steps circle. <bookmark mark='d'/> Their fix penalizes the "
            "discriminator's gradient on real data, here gamma over two psi squared: friction, and the spiral winds "
            "in. StyleGAN trains with this penalty, R1."
        ) as vo:
            self.play(FadeIn(pl), FadeIn(th), FadeIn(ps), FadeIn(setup), FadeIn(cite_))
            self.play(LaggedStart(*[GrowArrow(a_) for a_ in fld], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("a")
            self.play(Indicate(fld, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(FadeIn(lg[0]))
            t1, d1, p1 = traced(self, pl, Ps[:n_out], SIM, 1)
            self.play(t1.animate.set_value(n_out - 1), run_time=max(2.0, vo.until("c") - 0.3), rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(lg[1]))
            t2, d2, p2 = traced(self, pl, b["dirac_alt"], ALT, 1)
            self.play(t2.animate.set_value(len(b["dirac_alt"]) - 1), run_time=max(2.0, vo.until("d") - 0.3),
                      rate_func=linear)
            vo.wait_until("d")
            self.play(Write(r1), FadeIn(r1l), FadeIn(lg[2]))
            t3, d3, p3 = traced(self, pl, b["dirac_r1"], C.BITS, 1)
            self.play(t3.animate.set_value(len(b["dirac_r1"]) - 1), run_time=4.0, rate_func=linear)
        for m in (d1, p1, d2, p2, d3, p3):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hopping(self):
        g = load("gan2d_collapse")
        counts = np.asarray(g["frame_counts"], float)  # frames x 8 modes
        steps = np.asarray(g["frame_steps"])
        seed = int(g["seed"])
        A = counts.T / max(counts.max(), 1)
        rgb = rgb_of("#0B0F17")[None, None] * (1 - A[..., None]) + rgb_of(GAN_C)[None, None] * A[..., None]
        H = 4.2
        img = to_image(rgb, 10.0, H)
        img.move_to([0.4, 0.45, 0])
        box = SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1.2)
        ml = VGroup(*[label(rf"mode {k + 1}", font_size=18, color=GREY_B).next_to(
            img.get_corner(UL) + DOWN * (k + 0.5) * H / 8, LEFT, buff=0.15) for k in range(8)])
        xl = label(r"training step $\to$", font_size=20, color=GREY_A).next_to(img, DOWN, buff=0.15)
        x0 = MathTex(r"0", font_size=20, color=GREY_B).next_to(img.get_corner(DL), DOWN, buff=0.1)
        x1 = MathTex(rf"{int(steps[-1]):,}".replace(",", "{,}"), font_size=20, color=GREY_B)
        x1.next_to(img.get_corner(DR), DOWN, buff=0.1)
        head = label(rf"where the generator's samples are, \ checkpoint by checkpoint \ (non-saturating GAN, seed "
                     rf"${seed}$)", font_size=22, color=GREY_A).next_to(img, UP, buff=0.2)
        held = counts > 0.01 * np.maximum(counts.sum(1, keepdims=True), 1)
        visited, best, last = int(held.any(0).sum()), int(held.sum(1).max()), int(held[-1].sum())
        tour = (f"Over training the generator visits {visited} of the modes, but never more than {best} at once; at "
                f"the end it covers {last}." if best < 8 else
                f"Over training the generator visits all eight modes, and at times holds them all at once, but not "
                f"for long; at the end it covers {last}.")
        tk = take_away(r"GAN training is a dynamical system, not a descent: \ penalties (R1), \ look-ahead steps, "
                       r"\ two learning rates (TTUR), \ spectral normalization", font_size=24)
        with self.voiceover(
            "Back to the ring: each row a mode, each column a checkpoint, brightness the generator's samples there. "
            f"<bookmark mark='a'/> {tour} The bands wander from mode to mode: the toy game's rotation, in a space of "
            "distributions. <bookmark mark='b'/> The field fought it with penalties, look-ahead steps, separate "
            "learning rates, and spectral normalization."
        ) as vo:
            self.play(FadeIn(img), FadeIn(box), FadeIn(ml), FadeIn(xl), FadeIn(x0), FadeIn(x1), FadeIn(head))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(tk, shift=UP * 0.1))
        self.wait(0.3)
        self.clear_scene()
