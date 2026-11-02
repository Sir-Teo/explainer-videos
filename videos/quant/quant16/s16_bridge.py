from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from explainer.quant.house import engine as E
from videos.quant.quant16.common import (BAD, GOOD, METHOD_COL, OPT, PART, SPOT, fixed, illustration, load, loglog,
                                         polyline, predict)

KINDS = [("step", r"step by step", GREY_B), ("bridge", r"Brownian bridge", METHOD_COL["Sobol + bridge"]),
         ("pca", r"principal components", METHOD_COL["PCA"])]


class Bridge(VoiceoverScene, ThreeDScene):
    def construct(self):
        e = load("effdim")
        q = load("qmc")
        self.card()
        self.staircase(e)
        self.crystal()
        self.proof(e)
        self.measured(e, q)

    def card(self):
        c = chapter_card(6, r"QMC on paths: the bridge and effective dimension", r"Which of 64 dimensions matter?",
                         part=PART)
        with self.voiceover("Chapter six. Quasi-Monte Carlo on paths: the Brownian bridge, and effective dimension."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def staircase(self, e):
        ax = ThreeDAxes(x_range=[0, 1, 0.25], y_range=[0, 16, 4], z_range=[-0.5, 1.0, 0.5], x_length=6.5, y_length=6.0,
                        z_length=3.0, tips=False, axis_config={"stroke_color": GREY_C, "include_ticks": False,
                                                               "stroke_width": 2})
        ax.shift(DOWN * 0.3)
        t = np.linspace(1 / 16, 1, 16)

        def ribbons(kind):
            L = np.asarray(e["cols16"][kind])
            col = dict((k, c) for k, _, c in KINDS)[kind]
            g = VGroup()
            for k in range(16):
                pts = [ax.c2p(0, k + 0.5, 0)] + [ax.c2p(tt, k + 0.5, np.clip(L[j, k], -0.5, 1.0)) for j, tt in enumerate(t)]
                op = 1.0 if k < 4 else 0.55
                g.add(VMobject(stroke_color=col, stroke_width=3 if k < 4 else 2, stroke_opacity=op).set_points_as_corners(pts))
            return g

        rs = {k: ribbons(k) for k, _, _ in KINDS}
        hint = VGroup(label(r"across: time $t$", font_size=22, color=GREY_A),
                      label(r"back: which normal, $k = 1 \dots 16$", font_size=22, color=GREY_A),
                      label(r"up: what normal $k$ adds to $W_t$", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).to_corner(UL, buff=0.35)
        names = {k: label(nm, font_size=30, color=c).to_corner(UR, buff=0.4) for k, nm, c in KINDS}
        sh = {k: np.asarray(e["shares"][k]) for k, _, _ in KINDS}
        nums = {k: MathTex(rf"\text{{first normal: }}{100 * sh[k][0]:.1f}\%,\ \ \text{{first four: }}{100 * sh[k][3]:.1f}\%",
                           font_size=26, color=c).to_corner(DR, buff=0.4) for k, _, c in KINDS}
        src = illustration(r"16 steps drawn; the shares are for the average of a 64-step path", corner=DL)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-55 * DEGREES, zoom=0.85)
        fixed(self, hint, src, *names.values(), *nums.values())
        with self.voiceover(
            "Chapter two ended with a fact: any matrix whose product with its transpose is Brownian motion's "
            "covariance builds the same paths. Here is what each normal does under three such matrices. Across is "
            "time; going back, the sixteen normals in order; up, what each normal adds to the path. "
            "<bookmark mark='a'/> Step by step, every normal adds the same small step from its own moment on: "
            "a flat field, every coordinate equally important. <bookmark mark='b'/> The Brownian bridge spends the "
            "first normal on where the path ends, a ramp over the whole year; the second on the midpoint, a tent; "
            "then quarter points, smaller and smaller. <bookmark mark='c'/> Principal components go further: smooth "
            "waves, the first carrying almost everything. <bookmark mark='d'/> For the average of a sixty-four-step "
            f"path, the first normal carries {100 * sh['step'][0]:.1f} percent of the variance step by step, "
            f"{100 * sh['bridge'][0]:.1f} percent with the bridge and {100 * sh['pca'][0]:.1f} with principal "
            "components."
        ) as vo:
            self.play(Create(ax), FadeIn(hint), FadeIn(src), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(rs["step"]), FadeIn(names["step"]), FadeIn(nums["step"]), run_time=2)
            vo.wait_until("b")
            self.play(ReplacementTransform(rs["step"], rs["bridge"]), FadeOut(names["step"]), FadeIn(names["bridge"]),
                      FadeOut(nums["step"]), FadeIn(nums["bridge"]), run_time=2)
            self.move_camera(theta=-20 * DEGREES, phi=75 * DEGREES, run_time=2)
            vo.wait_until("c")
            self.play(ReplacementTransform(rs["bridge"], rs["pca"]), FadeOut(names["bridge"]), FadeIn(names["pca"]),
                      FadeOut(nums["bridge"]), FadeIn(nums["pca"]), run_time=2)
            vo.wait_until("d")
            self.move_camera(theta=-80 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(0.5), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, added_anims=[FadeOut(VGroup(ax, rs["pca"])), FadeOut(hint),
                                                                  FadeOut(names["pca"]), FadeOut(nums["pca"]),
                                                                  FadeOut(src)], run_time=1.5)
        self.clear_scene()

    def crystal(self):
        z = np.random.default_rng(4).standard_normal((1, 64))
        W = np.concatenate([[0.0], E.brownian_bridge(z, 1.0)[0]])
        t = np.linspace(0, 1, 65)
        g = axes([0, 1], [-1.6, 1.6], x_length=9.0, y_length=4.4, xlabel=r"time $t$", ylabel=r"$W_t$",
                 xticks=[0, 0.5, 1], yticks=[-1, 0, 1], font_size=16).shift(DOWN * 0.3)
        ax = g.ax
        stages = []
        for lev in range(0, 7):
            step = 64 // 2 ** lev
            idx = np.arange(0, 65, step)
            line = polyline(ax, t[idx], W[idx], METHOD_COL["Sobol + bridge"], stroke_width=2.5, dots=False)
            dots = VGroup(*[Dot(ax.c2p(t[i], W[i]), radius=0.05 if lev > 3 else 0.08, color=OPT) for i in idx[1:]])
            tag = MathTex(rf"\text{{normals used: }}{2 ** lev}", font_size=28, color=GREY_A).next_to(g, UP, buff=0.1)
            stages.append(VGroup(line, dots, tag))
        nums = VGroup()
        for k, i in enumerate([64, 32, 16, 48]):
            nums.add(MathTex(str(k + 1), font_size=24, color=OPT).next_to(ax.c2p(t[i], W[i]), UP, buff=0.12))
        with self.voiceover(
            "Watch the bridge build one path from sixty-four normals. The first fixes the end point. "
            "<bookmark mark='a'/> The second, the midpoint, given both ends. Then the quarter points, the eighths, "
            "and so on, each new point drawn around the straight line between its neighbours. After eight normals the "
            "shape is already there; the last thirty-two only add wiggles. That is the order quasi-random points "
            "want: their best coordinates, the first few, now decide the most."
        ) as vo:
            self.play(FadeIn(g), FadeIn(stages[0]), FadeIn(nums[0]))
            vo.wait_until("a")
            for k in range(1, 7):
                self.play(ReplacementTransform(stages[k - 1], stages[k]),
                          *({1: [FadeIn(nums[1])], 2: [FadeIn(nums[2]), FadeIn(nums[3])]}.get(k, [])), run_time=1.2)
                self.wait(0.3)
        self.wait(0.4)
        self.clear_scene()

    def proof(self, e):
        lam, kl = e["eig"], e["eig_kl"]
        rows = [
            cmath(r"f", r"=", r"\sum_{u \subseteq \{1..d\}} f_u,\qquad \sigma^2 = \sum_u \sigma_u^2", font_size=34),
            cmath(r"d_T", r"=", r"\min\Big\{s:\ \sum_{u \subseteq \{1..s\}} \sigma_u^2 \ge 0.99\,\sigma^2\Big\}", font_size=32,
                  colors={r"d_T": GOOD}),
            cmath(r"a^\top W = (a^\top L)\,Z", r"\Rightarrow", r"\text{share}_k = \frac{\sum_{j \le k}(a^\top L)_j^2}"
                  r"{\|a^\top L\|^2}", font_size=32),
            cmath(r"L_{\text{PCA}}", r"=", r"V\Lambda^{1/2},\qquad \lambda_j \approx \frac{T^2}{(j - \frac12)^2\pi^2}",
                  font_size=34, colors={r"L_{\text{PCA}}": METHOD_COL["PCA"]}),
        ]
        whys = [why(r"the ANOVA decomposition: orthogonal pieces depending on subsets $u$ of the coordinates"),
                why(r"truncation dimension (Caflisch, Morokoff and Owen 1997); the superposition dimension counts "
                    r"$|u| \le s$ instead"),
                why(r"for a linear payoff each normal's share is its squared weight: the heights in the 3D picture"),
                why(rf"Karhunen--Lo\`eve: the 64-step eigenvalues {lam[0]:.3f}, {lam[1]:.3f}, {lam[2]:.3f} (times $1/64$: "
                    rf"{lam[0] / 64:.3f}, {lam[1] / 64:.4f}, {lam[2] / 64:.4f}) against {kl[0]:.3f}, {kl[1]:.4f}, {kl[2]:.4f}; "
                    r"PCA front-loads the most variance of any $L$ (Eckart--Young)")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.8, buff=0.6, edge=6.9)
        with self.voiceover(
            "The idea has a name. Split any function of d inputs into pieces, each depending on one subset of the "
            "coordinates; the pieces are orthogonal, so their variances add. <bookmark mark='a'/> The truncation "
            "dimension is how many leading coordinates hold ninety-nine percent of the variance. Caflisch, Morokoff "
            "and Owen introduced it in 1997 to explain why quasi-Monte Carlo worked on mortgage securities at all. "
            "<bookmark mark='b'/> For a payoff linear in the path, each normal's share is just its squared weight: "
            "the heights you saw in three dimensions. <bookmark mark='c'/> Principal components use the covariance's "
            "eigenvectors, whose eigenvalues fall like one over j squared: no other matrix front-loads more."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def measured(self, e, q):
        ns = np.log10(np.asarray(q["ns"], float))
        g = loglog(2.2, 4.4, -4, 0, r"paths", r"spread of the price over 20 scrambles", x_length=5.8, y_length=4.0,
                   xt=[3, 4], yt=[-4, -3, -2, -1, 0])
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        series = [("pseudo-random", q["sd"]["pseudo-random"]), ("Sobol", q["sd"]["Sobol"]),
                  ("Sobol + bridge", q["sd"]["Sobol + bridge"]), ("PCA", e["pca_sd"])]
        lines = VGroup(*[polyline(ax, ns, np.clip(np.log10(v), -4, 0), METHOD_COL[k]) for k, v in series])
        names = {"pseudo-random": r"pseudo-random", "Sobol": r"Sobol, step by step", "Sobol + bridge": r"Sobol + bridge",
                 "PCA": r"Sobol + principal components"}
        leg = legend([(METHOD_COL[k], names[k]) for k, _ in series], font_size=16).next_to(g, UP, buff=0.1).align_to(g, LEFT)
        sd = {k: v[-1] for k, v in series}
        cards = VGroup(
            history_card(1995, r"Paskov and Traub", r"priced a 360-dimensional collateralised mortgage obligation with "
                         r"Sobol and Halton points faster than Monte Carlo, against the theory's warnings: the start "
                         r"of quasi-Monte Carlo in finance.", color=QC.IDEA, width=5.2, font_size=18),
            history_card(1997, r"Caflisch, Morokoff and Owen", r"explained it: the mortgage payoff's effective "
                         r"dimension is small, and the Brownian bridge makes a path's effective dimension small too.",
                         color=QC.IDEA, width=5.2, font_size=18),
        ).arrange(DOWN, buff=0.25).to_edge(RIGHT, buff=0.35)
        q2 = predict(r"Step by step, Sobol's spread stalls between 4{,}096 and 16{,}384 paths. Why?", width=5.2,
                     font_size=20).to_edge(RIGHT, buff=0.35).to_edge(DOWN, buff=0.3)
        src = illustration(r"arithmetic Asian call, 64 fixings; PCA costs $O(d^2)$ per path and needs a fixed grid",
                           corner=DL)
        with self.voiceover(
            "On the Asian option with sixty-four fixings, the spread over twenty scrambles. Pseudo-random points fall "
            "on their square-root line. Sobol fed step by step does better, then stalls: "
            f"{q['sd']['Sobol'][2]:.4f} at 4,096 paths and {q['sd']['Sobol'][3]:.4f} at 16,384. <bookmark mark='a'/> "
            f"The bridge reaches {sd['Sobol + bridge']:.4f}, and principal components {sd['PCA']:.5f}, "
            f"{sd['pseudo-random'] / sd['PCA']:.0f} times less spread than random paths. Principal components cost a "
            "dense matrix product per path and need a fixed grid, so desks usually take the bridge. "
            "<bookmark mark='b'/> History in two cards: Spassimir Paskov and Joseph Traub's mortgage obligation in "
            "1995, and the explanation two years later. <bookmark mark='c'/> And the stall? Step by step, the "
            f"variance is spread over all sixty-four coordinates: the first four carry only "
            f"{100 * e['shares']['step'][3]:.0f} percent, so the later, less even coordinates decide the answer."
            " Another way to spend less: take coarse steps on most paths. Next: multilevel Monte Carlo."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), Create(lines[0]), Create(lines[1]), FadeIn(leg[:2]), run_time=2)
            vo.wait_until("a")
            self.play(Create(lines[2]), Create(lines[3]), FadeIn(leg[2:]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(cards))
            vo.wait_until("c")
            self.play(FadeOut(cards[0]), FadeIn(q2))
        self.wait(0.5)
        self.clear_scene()
