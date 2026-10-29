from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai22.common import GS_C, HIST, NERF_C, PART, PATCH, fmt_int, load, rgb_image, spread_bars


def ellipse_of(cov, centre, scale=1.0, color=GS_C, opacity=0.35, stroke=1.5) -> Ellipse:
    """The one-sigma ellipse of a 2 x 2 covariance (in scene units)."""
    w, V = np.linalg.eigh(np.asarray(cov, float))
    w = np.sqrt(np.maximum(w, 1e-12)) * scale
    e = Ellipse(width=2 * w[1], height=2 * w[0], stroke_color=color, stroke_width=stroke, fill_color=color, fill_opacity=opacity)
    e.rotate(math.atan2(V[1, 1], V[0, 1]))
    return e.move_to(centre)


class Splat(VoiceoverScene):
    def construct(self):
        self.card()
        self.gaussians()
        self.derive()
        self.check()
        self.fit()
        self.frontier()

    def card(self):
        card = chapter_card(16, r"Gaussian splatting", r"Can 3D be fast enough to render in real time?", part=PART)
        with self.voiceover("Chapter sixteen. Gaussian splatting."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def gaussians(self):
        s = load("splat")
        res = int(s["res"])
        uv, cov, col, op = (np.asarray(s[k]) for k in ("ell_uv", "ell_cov", "ell_col", "ell_op"))
        S = 3.6
        k = S / res
        frame = Square(S, stroke_color=GREY_C, stroke_width=1.5, fill_color="#000000", fill_opacity=1).move_to([-3.4, 0.2, 0])
        o = frame.get_corner(UL)
        ells = VGroup(*[ellipse_of(c_ * k * k, o + np.array([u[0] * k, -u[1] * k, 0]), color=ManimColor.from_rgb(tuple(float(x) for x in np.clip(cl, 0, 1))),
                                   opacity=0.25 + 0.5 * float(a)) for u, c_, cl, a in zip(uv, cov, col, op)])
        for e in ells:  # image rows run down: flip each ellipse's tilt
            e.flip(RIGHT)
        el = label(r"the $150$ most opaque of our $500$ Gaussians, \ projected into a held-out view", font_size=18,
                   color=GREY_A).next_to(frame, DOWN, buff=0.15)
        each = VGroup(MathTex(r"\mu \in \mathbb R^3", font_size=30, color=GS_C), label(r"where it is", font_size=20, color=GREY_A),
                      MathTex(r"\Sigma = R\, S\, S^{\top} R^{\top}", font_size=30, color=GS_C),
                      label(r"its shape: \ a rotation $R$ (a quaternion) \\ and three scales $S$: \ always a valid covariance",
                            font_size=20, color=GREY_A),
                      MathTex(r"o \in (0, 1), \quad \mathbf c", font_size=30, color=GS_C),
                      label(r"its opacity and colour", font_size=20, color=GREY_A))
        each.arrange_in_grid(rows=3, cols=2, buff=(0.4, 0.35), col_alignments="rl").move_to([3.4, 0.6, 0])
        cite_ = cite(r"B.~Kerbl, G.~Kopanas, T.~Leimk\"uhler \& G.~Drettakis, \textit{3D Gaussian Splatting} (2023)", corner=DR)
        with self.voiceover(
            "NeRF's catch is speed: every pixel needs dozens of network evaluations along its ray. In 2023 Bernhard "
            "Kerbl, George Drettakis and colleagues replaced the network with a cloud of 3D Gaussians, millions of "
            "small soft blobs. <bookmark mark='a'/> Each has a position, <bookmark mark='b'/> a shape, a covariance "
            "built from a rotation and three scales so it always stays a valid one, <bookmark mark='c'/> an opacity "
            "and a colour. <bookmark mark='d'/> To render, project every blob onto the screen as a flat ellipse, and "
            "blend them front to back. No rays to march: the paper rendered at thirty frames a second or more, at "
            "1080p."
        ) as vo:
            self.play(FadeIn(frame), FadeIn(cite_))
            self.play(LaggedStart(*[GrowFromCenter(e) for e in ells], lag_ratio=0.01), FadeIn(el), run_time=2.5)
            for k_, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(each[2 * k_]), FadeIn(each[2 * k_ + 1]))
            vo.wait_until("d")
            self.play(Indicate(ells, color=GS_C, scale_factor=1.03), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        rows = [
            cmath(r"\mathbf t", r"=", r"W\,(\mu - \mathbf o)", font_size=32),
            cmath(r"(u, v)", r"=", r"\Big(f\,\frac{t_x}{t_z},\ f\,\frac{t_y}{t_z}\Big)", font_size=32),
            cmath(r"J", r"=", r"\frac{\partial (u, v)}{\partial \mathbf t} = \begin{pmatrix} f/t_z & 0 & -f t_x / t_z^2 \\ "
                  r"0 & f/t_z & -f t_y / t_z^2 \end{pmatrix}", font_size=30),
            cmath(r"\Sigma'", r"=", r"J\, W\, \Sigma\, W^{\top} J^{\top}", font_size=34),
        ]
        whys = [why(r"into the camera's frame: \ rotate by $W$"), why(r"perspective: \ divide by depth, \ not linear"),
                why(r"linearize at the mean"), why(r"a linear map of a Gaussian \ is a Gaussian")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-1.6, buff=0.5, edge=6.8)
        cite_ = cite(r"M.~Zwicker, H.~Pfister, J.~van Baar \& M.~Gross, \textit{EWA Splatting} (2001)", corner=DR)
        box = label(r"the $2 \times 2$ covariance of the ellipse on screen", font_size=22, color=GS_C).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "What ellipse does a 3D Gaussian make on the screen? Derive it. <bookmark mark='a'/> First rotate into "
            "the camera's frame. <bookmark mark='b'/> Then the perspective projection: divide by depth. That isn't "
            "linear, and a Gaussian pushed through a nonlinear map isn't Gaussian. <bookmark mark='c'/> So "
            "linearize: near the mean, the projection is approximately its Jacobian, J. <bookmark mark='d'/> A linear "
            "map of a Gaussian is Gaussian, with covariance J W Sigma W transpose J transpose. This is the 2001 "
            "EWA splatting of Matthias Zwicker and colleagues, the graphics idea at the heart of the method."
        ) as vo:
            self.play(FadeIn(cite_))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                step(k)
            self.play(FadeIn(box))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        s = load("splat")
        P_ = np.asarray(s["proj_samples"])
        mean, cov = np.asarray(s["proj_mean"]), np.asarray(s["proj_cov"])
        emp = np.asarray(s["proj_emp"])
        rel, errs = [float(r) for r in s["proj_rel"]], [float(e) for e in s["proj_errs"]]
        # left: the samples and the two ellipses, in pixels
        ctr = np.array([-3.6, 0.2, 0])
        sc = 3.4 / (6 * math.sqrt(max(np.linalg.eigvalsh(emp))))
        pts = VGroup(*[Dot(ctr + sc * np.array([p[0] - mean[0], -(p[1] - mean[1]), 0]), radius=0.012, color=GREY_B,
                           fill_opacity=0.6) for p in P_[:1500]])
        e_pred = ellipse_of(cov * sc * sc * 4, ctr, color=GS_C, opacity=0.0, stroke=3).flip(RIGHT)
        e_emp = ellipse_of(emp * sc * sc * 4, ctr + sc * np.array([float(s["proj_emp_mean"][0]) - mean[0],
                                                                   -(float(s["proj_emp_mean"][1]) - mean[1]), 0]),
                           color=C.TRUE_P, opacity=0.0, stroke=2).flip(RIGHT)
        leg = legend([(GS_C, r"$J W \Sigma W^{\top} J^{\top}$ \ (two sigmas)"), (C.TRUE_P, r"the samples' own covariance")],
                     font_size=18).next_to(VGroup(pts), DOWN, buff=0.3)
        pl = label(r"$200{,}000$ points from one 3D Gaussian, \ projected exactly", font_size=18, color=GREY_A).to_edge(UP, buff=0.35).shift(LEFT * 3.2)
        # right: the error against the Gaussian's size
        lx = [math.log10(r) for r in rel]
        ly = [math.log10(max(e, 1e-6)) for e in errs]
        ax = axes([lx[0] - 0.1, lx[-1] + 0.1], [min(ly) - 0.3, max(0.0, max(ly) + 0.3)], x_length=4.6, y_length=3.0,
                  xlabel=r"the Gaussian's size, \ over its depth", ylabel=r"relative error of the projected covariance",
                  xticks=[-2, -1], yticks=[int(np.floor(min(ly))), 0], xfmt=lambda x: rf"10^{{{int(x)}}}",
                  yfmt=lambda y: rf"10^{{{int(y)}}}", center=[3.3, 0.2, 0], font_size=17)
        ln = VGroup(curve(ax.ax, lx, ly, GS_C), *[Dot(ax.ax.c2p(a, b), radius=0.05, color=GS_C) for a, b in zip(lx, ly)])
        i10 = rel.index(0.1) if 0.1 in rel else len(rel) // 2
        slope = (ly[-1] - ly[0]) / (lx[-1] - lx[0])
        with self.voiceover(
            "Is the linearization good? Sample two hundred thousand points from a 3D Gaussian, project each one "
            "exactly, and compare their spread with the formula. <bookmark mark='a'/> For a Gaussian a tenth of its "
            f"depth across, the formula's covariance is off by {100 * errs[i10]:.1f} percent. <bookmark mark='b'/> "
            f"The error grows with the Gaussian's size: from {100 * errs[0]:.2f} percent at one hundredth of the depth "
            f"to {100 * errs[-1]:.0f} percent at {rel[-1]:g}, roughly as the size to the power {slope:.1f}. Splats are "
            "small, so the approximation holds where it's used."
        ) as vo:
            self.play(FadeIn(pl), LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.0005), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(e_pred), Create(e_emp), FadeIn(leg))
            vo.wait_until("b")
            self.play(Create(ax), Create(ln[0]), FadeIn(ln[1:]), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def fit(self):
        s, n = load("splat"), load("nerf")
        checks = [int(c) for c in s["checks"]]
        views = np.asarray(s["replay_views"])
        ps = [float(p) for p in s["replay_psnr"]]
        S = 2.2
        truth = rgb_image(np.asarray(s["test_view"]), S).move_to([-5.0, 1.4, 0])
        tl_ = label(r"the truth", font_size=18, color=GREY_A).next_to(truth, UP, buff=0.1)
        nv = rgb_image(np.asarray(n["replay_views"])[-1], S).move_to([-2.5, 1.4, 0])
        nl = label(r"NeRF", font_size=18, color=NERF_C).next_to(nv, UP, buff=0.1)

        def view(k):
            return rgb_image(views[k], S).move_to([0.0, 1.4, 0])

        cur = view(0)
        gl = label(r"Gaussians", font_size=18, color=GS_C).next_to(cur, UP, buff=0.1)
        t = ValueTracker(0)
        cnt = always_redraw(lambda: label(rf"step ${fmt_int(t.get_value())}$", font_size=20, color=GS_C).next_to(cur, DOWN, buff=0.1))
        gp, npp = np.asarray(s["test_psnr"], float), np.asarray(n["test_psnr"], float)
        gs_, ns_ = np.asarray(s["secs"], float), np.asarray(n["secs"], float)
        gr, nr = np.asarray(s["render_ms"], float), np.asarray(n["render_ms"], float)
        b1 = spread_bars([[npp, gp]], [NERF_C, GS_C], None, height=2.0, bar_w=0.55, gap=0.2, fmt=lambda v: f"{v:.1f}",
                         font_size=18).move_to([3.0, 1.2, 0])
        b2 = spread_bars([[nr, gr]], [NERF_C, GS_C], None, height=2.0, bar_w=0.55, gap=0.2, fmt=lambda v: f"{v:.0f}",
                         font_size=18).move_to([5.3, 1.2, 0])
        t1 = label(r"held-out \\ PSNR (dB)", font_size=16, color=GREY_A).next_to(b1, DOWN, buff=0.12)
        t2 = label(r"ms to render \\ one view", font_size=16, color=GREY_A).next_to(b2, DOWN, buff=0.12)
        hd = note(rf"the same $24$ photographs, \ ${fmt_int(s['steps'])}$ steps each, \ three seeds; \ on this CPU, "
                  rf"training took ${ns_.mean():.0f}$ s (NeRF) and ${gs_.mean():.0f}$ s (Gaussians)").to_edge(DOWN, buff=0.3)
        comp = ("the Gaussians match the photographs more closely" if gp.mean() > npp.mean() + 0.3 else
                "NeRF matches the photographs more closely" if npp.mean() > gp.mean() + 0.3 else
                "the two match the photographs about equally well")
        fast = gr.mean() < nr.mean()
        verdict = (f"After the same number of steps, {comp}: {gp.mean():.1f} decibels for the Gaussians and "
                   f"{npp.mean():.1f} for NeRF.")
        speed = (f"Rendering a view takes {gr.mean():.0f} milliseconds against NeRF's {nr.mean():.0f}, even with our "
                 "plain code; on a GPU, with the paper's tile rasterizer, it runs in real time." if fast else
                 f"Our plain code renders a view in {gr.mean():.0f} milliseconds against NeRF's {nr.mean():.0f}: we "
                 "evaluate every Gaussian at every pixel. The paper's GPU rasterizer sorts them into tiles and touches "
                 "only the few that cover each pixel, which is where real time comes from.")
        with self.voiceover(
            f"We fitted {int(s['N'])} Gaussians to the same twenty-four photographs, by gradient descent through the "
            "renderer, moving faded ones next to busy ones as we went. <bookmark mark='a'/> Here is the held-out "
            f"view as they settle: PSNR from {ps[0]:.1f} decibels to {ps[-1]:.1f}. <bookmark mark='b'/> " + verdict
            + " <bookmark mark='c'/> " + speed
        ) as vo:
            self.play(FadeIn(truth), FadeIn(tl_), FadeIn(nv), FadeIn(nl), FadeIn(cur), FadeIn(gl))
            self.add(cnt)
            vo.wait_until("a")
            for k in range(1, len(checks)):
                nxt = view(k)
                self.play(t.animate.set_value(checks[k]), FadeOut(cur), FadeIn(nxt), run_time=0.9)
                cur = nxt
            vo.wait_until("b")
            self.play(FadeIn(b1.base), FadeIn(b1.bars), FadeIn(t1), FadeIn(hd))
            vo.wait_until("c")
            self.play(FadeIn(b2.base), FadeIn(b2.bars), FadeIn(t2))
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def frontier(self):
        head = label(r"3D, \ 2020--2025", font_size=36).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(r"2022", r"Instant-NGP \ (M\"uller et al.)", r"a hash grid instead of a big MLP: \ a NeRF in "
                         r"seconds", color=HIST, width=11.0, font_size=25),
            history_card(r"2024", r"DUSt3R \ (Wang et al.)", r"a transformer turns two photographs \ into 3D points, \ "
                         r"no camera calibration", color=HIST, width=11.0, font_size=25),
            history_card(r"2025", r"VGGT \ (Wang et al., Oxford \& Meta)", r"cameras, depth and points \ from hundreds "
                         r"of views, \ in one pass under a second; \ CVPR best paper", color=HIST, width=11.0, font_size=25),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(head, DOWN, buff=0.4)
        if cards.height > 5.0:
            cards.height = 5.0
            cards.next_to(head, DOWN, buff=0.4)
        foot = label(r"from fitting one scene \ to a transformer that sees 3D: \ worlds you can walk through are Part 29",
                     font_size=22, color=PATCH).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "NeRF and splatting fit one scene at a time, from carefully calibrated photographs. <bookmark mark='a'/> "
            "Instant-NGP made the fitting take seconds. <bookmark mark='b'/> Then transformers learned to see 3D "
            "directly: DUSt3R turned two uncalibrated photographs into 3D points, <bookmark mark='c'/> and VGGT, the "
            "best paper at CVPR 2025, predicts cameras, depth and points from hundreds of views in one pass, in under "
            "a second. <bookmark mark='d'/> Generate those views, and you can generate worlds, the subject of Part 29."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()
