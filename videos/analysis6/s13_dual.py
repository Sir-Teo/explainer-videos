from __future__ import annotations

import math

import numpy as np

from explainer.analysis import *  # noqa: F403
from videos.analysis6.common import area_under, dict_table, load, p_ball, plain_axes, pnorm, polyline, square_axes


class DualLp(VoiceoverScene):
    def construct(self):
        self.card()
        self.touch()
        self.theorem()
        self.probe()
        self.dictionary()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"The dual of $L^p$", r"Which linear functionals live on $L^p$?", lit=(), part=6)
        with self.voiceover("Chapter twelve: the functionals on L p, and on the continuous functions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def touch(self):
        d = load("dual")
        p, q, gq, best, g8 = float(d["p"]), float(d["q"]), float(d["gq"]), float(d["best"]), d["g"]
        ax = square_axes([-1.4, 1.4, 1], [-1.4, 1.4, 1], 1.8).move_to([-3.8, -0.6, 0])
        ax.set_opacity(0.35)
        ball = p_ball(ax, p, C.DIST)
        g = np.array([0.8, 0.5])
        nq = pnorm(g, q)
        xstar = np.sign(g) * np.abs(g) ** (q - 1)
        xstar /= pnorm(xstar, p)
        assert abs(g @ xstar - nq) < 1e-12 and abs(pnorm(xstar, p) - 1) < 1e-12
        th = np.linspace(0, 2 * np.pi, 7201)
        bd = np.stack([np.cos(th), np.sin(th)], 1)
        bd = bd / np.array([pnorm(v, p) for v in bd])[:, None]
        assert abs((bd @ g).max() - nq) < 1e-5
        cT = ValueTracker(0.2)
        gu = g / np.linalg.norm(g)
        tg = np.array([-gu[1], gu[0]])

        def level():
            c = cT.get_value()
            p0 = c / np.linalg.norm(g) * gu
            return Line(ax.c2p(*(p0 - 1.6 * tg)), ax.c2p(*(p0 + 1.6 * tg)), color=C.FUNCTIONAL, stroke_width=3)

        lv = always_redraw(level)
        # as in chapter 7: the functional is a stack of parallel level lines, with the vector g as their normal
        def faint(c_):  # the level line {g . x = c_}, cut to the axes' square
            ts_ = np.linspace(-3, 3, 1201)
            pts_ = c_ / np.linalg.norm(g) * gu[None, :] + ts_[:, None] * tg[None, :]
            ok_ = np.all(np.abs(pts_) <= 1.35, axis=1)
            return Line(ax.c2p(*pts_[ok_][0]), ax.c2p(*pts_[ok_][-1]), color=C.FUNCTIONAL, stroke_width=1.5).set_stroke(
                opacity=0.35)

        stack = VGroup(*[faint(c_) for c_ in (-0.8, -0.4, 0.4, 0.8)])
        garr = Arrow(ax.c2p(0, 0), ax.c2p(*g), buff=0, color=C.INNER, stroke_width=5, tip_length=0.18)
        g_l = MathTex("g", font_size=28, color=C.INNER).next_to(ax.c2p(*g), DOWN, buff=0.1).shift(RIGHT * 0.1)
        lv_l = always_redraw(lambda: MathTex(rf"\{{x : 0.8x_1 + 0.5x_2 = {cT.get_value():.4f}\}}", font_size=26,
                                             color=C.FUNCTIONAL).next_to(ax, DOWN, buff=0.15))
        xd = Dot(ax.c2p(*xstar), radius=0.09, color=C.EPS)
        x_l = MathTex(r"x^*", font_size=28, color=C.EPS).next_to(xd, UR, buff=0.05)
        b_l = MathTex(r"\|x\|_3 \le 1", font_size=28, color=C.DIST).move_to(ax.c2p(-0.5, -0.45))
        b_l.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.05)  # over the faint level lines
        b_l.set_z_index(2)
        side = VGroup(
            MathTex(r"\Lambda x = g \cdot x, \quad g = (0.8,\ 0.5)", font_size=30),
            MathTex(rf"\|\Lambda\| = \max_{{\|x\|_3 \le 1}} \Lambda x = \|g\|_{{3/2}} = {nq:.4f}", font_size=30,
                    color=C.EPS),
            label(r"attained at $x^* \propto \mathrm{sign}(g)\,|g|^{q-1}$ \ (H\"older's equality case)", font_size=24,
                  color=GREY_A),
            label(r"in $\R^8$, \ $g$ random, \ $p = 3$:", font_size=24),
            MathTex(rf"\|g\|_{{3/2}} = {gq:.4f}; \ \ 20{{,}}000 \text{{ random unit }} x: \ \max = {best:.4f}", font_size=26),
            MathTex(rf"x^*: \ \Lambda x^* = {gq:.4f}", font_size=26, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([3.2, -0.5, 0])
        side[3:].shift(DOWN * 0.2)
        for r_ in side:
            if r_.width > 6.4:
                r_.width = 6.4
        head = label(r"The norm of a functional: \ slide a level line out to the ball", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> How big is a functional on L p? Start in the plane with the three-norm. The "
            "functional zero point eight x one plus a half x two has level lines. <bookmark mark='b'/> Slide one "
            "outward until it last touches the unit ball. <bookmark mark='c'/> The value there is the norm of the "
            "functional, and it's the three-halves norm of the vector g. The exponent flips to the conjugate one, q. "
            "The touching point comes from Hölder's equality case. <bookmark mark='d'/> In eight dimensions: twenty "
            "thousand random unit vectors never beat the q-norm of g, and the extremal vector hits it exactly."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(ball), FadeIn(b_l), FadeIn(side[0]))
            self.play(FadeIn(stack), FadeIn(lv), FadeIn(lv_l), GrowArrow(garr), FadeIn(g_l))
            vo.wait_until("b")
            self.play(cT.animate.set_value(nq), run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(xd, scale=2), FadeIn(x_l), FadeIn(side[1]))
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3:]))
        for m in (lv, lv_l):
            m.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        head = label(r"The dual of $L^p$ is $L^q$", font_size=34).to_edge(UP, buff=0.3)
        thm = VGroup(
            label(r"\textbf{RCA 6.16} \ $1 \le p < \infty$, \ $\mu$ $\sigma$-finite, \ $\Phi$ a bounded linear functional "
                  r"on $L^p(\mu)$:", font_size=26),
            MathTex(r"\Phi(f) = \int f g\,d\mu \ \text{ for a unique } g \in L^q(\mu), \qquad \|\Phi\| = \|g\|_q",
                    font_size=30, color=C.EPS),
        ).arrange(DOWN, buff=0.12).next_to(head, DOWN, buff=0.15)
        pm = ProofMap([r"$\lambda(E) = \Phi(\mathbf 1_E)$ \ is a complex measure",
                       r"$\mu(E) = 0 \Rightarrow \lambda(E) = 0$: \ $\lambda \ll \mu$",
                       r"Radon--Nikodym: \ $d\lambda = g\,d\mu$",
                       r"$\Phi(f) = \int fg$ \ for simple $f$, \ then all $f$; \ $\|g\|_q = \|\Phi\|$"],
                      font_size=20, width=5.2, buff=0.22, direction=DOWN)
        pm.next_to([-6.4, thm.get_bottom()[1] - 0.35, 0], DR, buff=0)
        notes = VGroup(
            label(r"step 1 needs $p < \infty$:", font_size=24),
            MathTex(r"E_n \nearrow E \ \Rightarrow \ \|\mathbf 1_E - \mathbf 1_{E_n}\|_p = \mu(E \setminus E_n)^{1/p} \to 0",
                    font_size=26),
            label(r"so $\Phi(\mathbf 1_E)$ is countably additive", font_size=24, color=GREY_A),
            label(r"in $L^\infty$ that norm stays $1$: \ the step fails,", font_size=24, color=C.PATHOLOGY),
            label(r"and $(L^\infty)^*$ is bigger than $L^1$ \ (Part 8)", font_size=24, color=C.PATHOLOGY),
            label(r"$p = 2$: \ $q = 2$, \ chapter 7 again", font_size=24, color=C.INNER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        # the proof, run: a functional given only as a black box on L^3[0, 1]; feed it indicators of [0, x]
        xq = np.linspace(0, 1, 20001)
        w_hidden = 1 + 0.6 * np.cos(3 * np.pi * xq) + 0.8 * xq

        cum = np.concatenate([[0], np.cumsum((w_hidden[1:] + w_hidden[:-1]) / 2 * np.diff(xq))])

        def Phi_indicator(t_):  # the black box, applied to 1_[0, t]
            return float(np.interp(t_, xq, cum))

        xs_ = np.linspace(0, 1, 201)
        lam_ = np.array([Phi_indicator(t_) for t_ in xs_])
        g_ = np.gradient(lam_, xs_)
        w_at = 1 + 0.6 * np.cos(3 * np.pi * xs_) + 0.8 * xs_
        err_g = float(np.abs(g_[2:-2] - w_at[2:-2]).max())
        assert err_g < 5e-3  # central differences with step 0.005
        px = plain_axes([0, 1, 0.25], [0, 2.6, 1], 5.0, 1.75, numbers=True, font_size=16,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([3.7, -0.05, 0])
        gl_ = polyline(px, xs_, lam_, color=C.MEASURE, stroke_width=3)
        gg_ = polyline(px, xs_[2:-2], g_[2:-2], color=C.INNER, stroke_width=3)
        gw_ = DashedVMobject(polyline(px, xs_, w_at, color=WHITE, stroke_width=3), num_dashes=40).set_z_index(2)
        pl_ = VGroup(MathTex(r"\lambda([0, x]) = \Phi(\mathbf 1_{[0, x]})", font_size=24, color=C.MEASURE),
                     MathTex(rf"g = \tfrac{{d\lambda}}{{dx}}; \ w \text{{ dashed}}: \ \max|g - w| = {sci(err_g, 0)}",
                             font_size=24, color=C.INNER)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(px, UP, buff=0.1).align_to(px, LEFT)
        # notes: why p < infinity, under the plot; what fails in L^infinity, under the proof map
        nr = notes[:3].copy()
        nl = notes[3:].copy()
        nr.next_to([px.get_left()[0] - 0.35, px.get_bottom()[1] - 0.45, 0], DR, buff=0)
        nl.next_to([pm.get_left()[0], pm.get_bottom()[1] - 0.35, 0], DR, buff=0)
        notes = VGroup(*nr, *nl)
        assert pl_.get_top()[1] < thm.get_bottom()[1] - 0.1 and pl_.get_right()[0] < 6.6
        assert notes.get_bottom()[1] > -3.6 and max(m_.get_right()[0] for m_ in notes) < 6.6
        with self.voiceover(
            "<bookmark mark='a'/> The theorem: for finite p, every bounded functional on L p is integration against "
            "a function g in L q, and the norms match. <bookmark mark='b'/> The proof turns the functional into a "
            "measure. Feed it indicator functions of sets: that defines lambda of E. <bookmark mark='c'/> Lambda "
            "vanishes on null sets, <bookmark mark='d'/> so Radon-Nikodym gives a density g. "
            "<bookmark mark='e'/> Then phi of f is the integral of f g, first for simple functions, then for all. "
            "<bookmark mark='f'/> Countable additivity in step one is where p must be finite: the indicators of an "
            "increasing sequence of sets converge in L p, but not in L infinity. The dual of L infinity is bigger "
            "than L one, a story for Part 8."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(pm))
            self.play(*pm.light(0), Create(px), Create(gl_), FadeIn(pl_[0]))
            vo.wait_until("c")
            self.play(*pm.light(1))
            vo.wait_until("d")
            self.play(*pm.light(2), Create(gw_), Create(gg_), FadeIn(pl_[1]))
            vo.wait_until("e")
            self.play(*pm.light(3))
            self.play(*pm.done())
            vo.wait_until("f")
            self.play(FadeIn(notes[:3]))
            self.play(FadeIn(notes[3:5]))
            self.play(FadeIn(notes[5]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def probe(self):
        d = load("probe")
        a, rs, D, wa = d["a"], d["rs"], d["D"], d["wa"]
        ax = plain_axes([0, 1, 0.25], [0, 4, 1], 6.6, 3.8, numbers=True, font_size=18,
                        x_axis_config={"decimal_number_config": {"num_decimal_places": 2}},
                        y_axis_config={"decimal_number_config": {"num_decimal_places": 0}}).move_to([-2.7, -0.55, 0])
        cols = [C.SEQ, C.APPROX, C.EPS]
        curves = [runs(ax, a, D[i], cols[i], 3) for i in range(len(rs))]
        tops = [float(D[i].max()) for i in range(len(rs))]
        labels_ = [MathTex(rf"r = {r_}: \ \text{{peak }} {t_:.1f}", font_size=26, color=cols[i]).next_to(ax, DOWN, buff=0.15)
                   for i, (r_, t_) in enumerate(zip(rs, tops))]
        gw = polyline(ax, a, wa, color=C.MEASURE, stroke_width=5).set_stroke(opacity=0.5)
        atom = VGroup(Arrow(ax.c2p(0.3, 1.3), ax.c2p(0.3, 4.0), buff=0, color=C.PATHOLOGY, stroke_width=5,
                            tip_length=0.2),
                      MathTex(r"0.5\,\delta_{0.3}", font_size=28, color=C.PATHOLOGY).next_to(ax.c2p(0.45, 3.5), RIGHT,
                                                                                         buff=0.05))
        w_l = MathTex(r"w(x) = 1 + \tfrac12 \sin 2\pi x", font_size=26, color=C.MEASURE).next_to(ax.c2p(0.62, 1.55),
                                                                                              UR, buff=0.05)
        # 'a': we can only evaluate Phi; here it is on one continuous f
        xf_ = np.linspace(0, 1, 200001)
        f_a = 1.5 + np.cos(2 * math.pi * xf_)
        phi_f = 0.5 * (1.5 + math.cos(2 * math.pi * 0.3)) + float(np.trapezoid(f_a * (1 + 0.5 * np.sin(2 * math.pi * xf_)), xf_))
        assert abs(phi_f - (0.5 * (1.5 + math.cos(0.6 * math.pi)) + 1.5)) < 1e-9  # int (1.5 + cos)(1 + sin/2) = 1.5
        xg_ = np.linspace(0, 1, 300)
        gfa = polyline(ax, xg_, 1.5 + np.cos(2 * math.pi * xg_), color=C.FUNC, stroke_width=3.5)
        gfa_l = VGroup(MathTex(r"f(x) = \tfrac32 + \cos 2\pi x", font_size=26, color=C.FUNC),
                       MathTex(rf"\Phi(f) = {phi_f:.4f}", font_size=28)).arrange(RIGHT, buff=0.5).next_to(ax, DOWN, buff=0.15)
        # 'b': one probe, the tent of half-width r = 0.1 at a = 0.6
        tent = VGroup(Polygon(ax.c2p(0.5, 0), ax.c2p(0.6, 1), ax.c2p(0.7, 0), stroke_color=C.TEST_FN, stroke_width=3,
                              fill_color=C.TEST_FN, fill_opacity=0.3),
                      MathTex(r"\varphi_{0.6,\,0.1}", font_size=26, color=C.TEST_FN).next_to(ax.c2p(0.6, 1), UR, buff=0.05))
        side = VGroup(
            MathTex(r"\Phi(f) = \tfrac12 f(0.3) + \int_0^1 f\,w", font_size=30),
            label(r"probe: \ a tent $\varphi_{a,r}$ of half-width $r$ at $a$", font_size=24, color=GREY_A),
            MathTex(r"\frac{\Phi(\varphi_{a, r})}{\int \varphi_{a, r}} \ \text{ for every } a", font_size=28),
            label(r"away from $0.3$: \ $\to w(a)$ \ (to $2 \times 10^{-3}$)", font_size=24, color=C.MEASURE),
            label(r"at $0.3$: \ a spike of height $\approx \frac{0.5}{r}$: \ an atom", font_size=24, color=C.PATHOLOGY),
            label(r"\textbf{RCA 6.19} \ (Riesz) \ $C_0(X)^* = M(X)$:", font_size=24, color=C.EPS),
            MathTex(r"\Phi(f) = \int f\,d\mu, \quad \|\Phi\| = |\mu|(X) = 0.5 + 1 = 1.5", font_size=26, color=C.EPS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.3, -0.4, 0])
        for r_ in side:
            if r_.width > 4.9:
                r_.width = 4.9
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([4.1, -0.4, 0])
        xf = np.linspace(0, 1, 100001)
        wf = 1 + 0.5 * np.sin(2 * math.pi * xf)
        assert wf.min() > 0 and abs(float(np.sum((wf[1:] + wf[:-1]) / 2) * (xf[1] - xf[0])) - 1) < 1e-9
        far = np.abs(a - 0.3) > 0.12
        assert np.abs(D[-1][far] - wa[far]).max() < 2e-3 and tops[-1] > 40
        head = label(r"A functional on $C[0, 1]$, \ probed with narrowing bumps", font_size=34).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> On the continuous functions with the sup norm, functionals are something else. "
            "Here's one: half the value at 0.3, plus the integral of f against a weight w. Pretend we can only "
            "evaluate it. <bookmark mark='b'/> Probe it with a narrow tent at each point a, divided by the tent's "
            "area. <bookmark mark='c'/> As the tents narrow, the readings converge to the weight w, except at 0.3, "
            "where a spike grows like one over r: an atom of mass one half. <bookmark mark='d'/> That's the Riesz "
            "representation theorem: every bounded functional on the continuous functions is integration against a "
            "complex measure, and its norm is the total variation, here one and a half. The dual of C is a space of "
            "measures."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), Create(ax), FadeIn(side[0]), Create(gfa), FadeIn(gfa_l))
            vo.wait_until("b")
            self.play(FadeOut(gfa), FadeOut(gfa_l), FadeIn(tent), FadeIn(side[1:3]))
            self.play(tent.animate.set_opacity(0.35), Create(curves[0]), FadeIn(labels_[0]), run_time=1.5)
            vo.wait_until("c")
            for i in (1, 2):
                self.play(curves[i - 1].animate.set_stroke(opacity=0.3), Create(curves[i]),
                          FadeTransform(labels_[i - 1], labels_[i]), run_time=1.3)
            self.play(Create(gw), FadeIn(w_l), FadeIn(side[3]))
            self.play(GrowArrow(atom[0]), FadeIn(atom[1]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5:]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def dictionary(self):
        head = label(r"The dictionary: \ a functional is a vector, \ a function, \ or a measure", font_size=34).to_edge(UP,
                                                                                                                  buff=0.3)
        card = dict_table(r"the space", r"its bounded linear functionals", [
            (r"$\R^n$", r"vectors: \ $x \mapsto x \cdot y$"),
            (r"a Hilbert space $H$", r"vectors: \ $\langle \cdot, y\rangle$ \ (ch.~7)"),
            (r"$L^p(\mu)$, \ $1 \le p < \infty$", r"functions in $L^q$: \ $\int f g\,d\mu$"),
            (r"$C_0(X)$", r"complex measures: \ $\int f\,d\mu$"),
            (r"$L^\infty$", r"more than $L^1$ \ (Part 8)"),
        ], xs=(-4.1, -1.65, 1.55), widths=(3.3, 4.6), top=2.45, font_size=28, gap=0.6)
        assert card.get_bottom()[1] > -3.5
        # one small picture per row, in the column on the right
        tx_ = 5.35

        def frame_at(y_):
            return Rectangle(width=1.9, height=0.86, stroke_color=GREY_D, stroke_width=1.5).move_to([tx_, y_, 0])

        thumbs = VGroup()
        ys = [r_.get_y() for r_ in card.rows]
        # R^n: the vector y as the normal of a stack of level lines
        c0 = np.array([tx_ - 0.35, ys[0] - 0.15, 0])
        yv = np.array([0.55, 0.42, 0])
        tg = np.array([-yv[1], yv[0], 0]) / np.linalg.norm(yv)
        nv = yv / np.linalg.norm(yv)
        thumbs.add(VGroup(frame_at(ys[0]),
                          *[Line(c0 + k * 0.18 * nv - 0.26 * tg, c0 + k * 0.18 * nv + 0.26 * tg, color=C.FUNCTIONAL,
                                 stroke_width=1.5).set_stroke(opacity=0.7) for k in range(4)],
                          Arrow(c0, c0 + yv, buff=0, color=C.INNER, stroke_width=4, tip_length=0.13)))
        # H: the kernel and the unit normal z (chapter 7's proof)
        c1 = np.array([tx_, ys[1] - 0.2, 0])
        thumbs.add(VGroup(frame_at(ys[1]), Line(c1 + 0.75 * LEFT, c1 + 0.75 * RIGHT, color=C.EPS, stroke_width=3),
                          Arrow(c1, c1 + 0.5 * UP, buff=0, color=C.INNER, stroke_width=4, tip_length=0.13),
                          Line(c1 + 0.12 * RIGHT, c1 + 0.12 * RIGHT + 0.12 * UP, color=GREY_B, stroke_width=1.5),
                          Line(c1 + 0.12 * UP, c1 + 0.12 * RIGHT + 0.12 * UP, color=GREY_B, stroke_width=1.5)))
        # L^p: a function g (the hidden weight recovered in the proof above)
        mx = plain_axes([0, 1, 1], [0, 2.6, 1], 1.6, 0.66).move_to([tx_, ys[2], 0])
        mx.set_opacity(0.4)
        xq = np.linspace(0, 1, 120)
        thumbs.add(VGroup(frame_at(ys[2]), mx,
                          polyline(mx, xq, 1 + 0.6 * np.cos(3 * np.pi * xq) + 0.8 * xq, color=C.INNER, stroke_width=3)))
        # C_0: a density with an atom (the probe's measure)
        mx3 = plain_axes([0, 1, 1], [0, 3.0, 1], 1.6, 0.66).move_to([tx_, ys[3], 0])
        mx3.set_opacity(0.4)
        dens = 1 + 0.5 * np.sin(2 * np.pi * xq)
        thumbs.add(VGroup(frame_at(ys[3]), mx3, area_under(mx3, xq, dens, C.MEASURE, 0.35),
                          polyline(mx3, xq, dens, color=C.MEASURE, stroke_width=2.5),
                          Arrow(mx3.c2p(0.3, 0), mx3.c2p(0.3, 3.0), buff=0, color=C.PATHOLOGY, stroke_width=3.5,
                                tip_length=0.12)))
        # L^infinity: not drawn here
        thumbs.add(VGroup(frame_at(ys[4]), MathTex(r"?", font_size=40, color=C.PATHOLOGY).move_to([tx_, ys[4], 0])))
        assert max(t_.get_right()[0] for t_ in thumbs) < 6.6 and card.get_right()[0] < thumbs.get_left()[0] - 0.2
        for t_ in thumbs:  # every picture inside its frame
            assert t_[0].get_top()[1] + 0.02 >= t_.get_top()[1] and t_[0].get_bottom()[1] - 0.02 <= t_.get_bottom()[1]
        with self.voiceover(
            "<bookmark mark='a'/> So the dictionary grows a column. In the plane and in Hilbert space, a functional "
            "is a vector. <bookmark mark='b'/> On L p, it's a function in the conjugate space. On the continuous "
            "functions, it's a measure. <bookmark mark='c'/> And on L infinity, something stranger, which needs the "
            "Hahn-Banach theorem."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(head), FadeIn(card.titles))
            for i in range(2):
                self.play(FadeIn(card.rows[i]), FadeIn(card.arrows[i]), FadeIn(thumbs[i]), run_time=0.7)
            vo.wait_until("b")
            for i in range(2, 4):
                self.play(FadeIn(card.rows[i]), FadeIn(card.arrows[i]), FadeIn(thumbs[i]), run_time=0.7)
            vo.wait_until("c")
            self.play(FadeIn(card.rows[4]), FadeIn(card.arrows[4]), FadeIn(thumbs[4]))
        self.wait(0.4)
        self.clear_scene()
