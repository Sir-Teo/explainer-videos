from __future__ import annotations

import numpy as np
from scipy.special import ndtr, ndtri

from explainer.quant import *  # noqa: F403
from videos.quant.quant16.common import BAD, GOOD, OPT, PART, SPOT, illustration, load, predict


class Paths(VoiceoverScene):
    def construct(self):
        rng = load("rng")
        ed = load("effdim")
        self.card()
        self.inverse()
        self.cloud(rng)
        self.proof()
        self.lab(ed)
        self.streams(rng)

    def card(self):
        c = chapter_card(2, r"Random numbers and sample paths", r"Where do the normals come from, and can a rerun repeat "
                         r"them?", part=PART)
        with self.voiceover("Chapter two. Random numbers and sample paths."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def inverse(self):
        g = axes([-3.2, 3.2], [0, 1], x_length=7.0, y_length=4.2, xlabel=r"$x$", ylabel=r"$u = \Phi(x)$",
                 xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[0, 0.5, 1], font_size=16)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        ax = g.ax
        xs = np.linspace(-3.2, 3.2, 200)
        cdf = curve(ax, xs, ndtr(xs), SPOT, stroke_width=3)
        u = np.random.default_rng(3).random(160)
        x = ndtri(u)
        bins = np.linspace(-3.2, 3.2, 25)
        counts = np.zeros(len(bins) - 1)
        stacks = VGroup()
        drops = []
        for ui, xi in zip(u, x):
            if abs(xi) >= 3.2:
                continue
            b = int(np.searchsorted(bins, xi) - 1)
            counts[b] += 1
            x_c = 0.5 * (bins[b] + bins[b + 1])
            sq = Square(side_length=0.2, stroke_width=0, fill_color=OPT, fill_opacity=0.85)
            sq.move_to(ax.c2p(x_c, 0) + UP * (0.11 + 0.2 * (counts[b] - 1)) * 0.5)
            sq.scale(0.5)
            stacks.add(sq)
            drops.append((ui, xi, sq))
        side = wrapped_label(r"inverse transform: a uniform $u$ read across to the curve and down gives $x = \Phi^{-1}(u)$, "
                             r"and $P(\Phi^{-1}(U) \le x) = P(U \le \Phi(x)) = \Phi(x)$. The dots pile into the bell",
                             4.2, 19, GREY_A).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Every simulation starts from uniform random numbers, and a normal is made from them. The cleanest way is "
            "the inverse transform. Take a uniform u on the vertical axis, read across to the normal distribution "
            "function, and down. <bookmark mark='a'/> Do it again and again, and the points pile up into a bell, "
            "because the probability of landing below any x is exactly the area the curve gives it."
        ) as vo:
            self.play(FadeIn(g), Create(cdf), FadeIn(side))
            for ui, xi, sq in drops[:4]:
                p0, p1, p2 = ax.c2p(-3.2, ui), ax.c2p(xi, ui), ax.c2p(xi, 0)
                path = VGroup(Line(p0, p1, stroke_color=GREY_B, stroke_width=1.5),
                              Line(p1, p2, stroke_color=GREY_B, stroke_width=1.5))
                self.play(Create(path), run_time=0.6)
                self.play(FadeIn(sq), FadeOut(path), run_time=0.3)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(sq, shift=DOWN * 0.3) for _, _, sq in drops[4:]], lag_ratio=0.03,
                                  run_time=max(vo.remaining(0.5), 2)))
        self.wait(0.3)
        self.clear_scene()

    def cloud(self, rng):
        rho = rng["rho"]
        g = np.random.default_rng(8)
        u1, u2 = g.random(450), g.random(450)
        r = np.sqrt(-2 * np.log(u1))
        z1, z2 = r * np.cos(2 * np.pi * u2), r * np.sin(2 * np.pi * u2)
        plane = axes([-3.5, 3.5], [-3.5, 3.5], x_length=5.0, y_length=5.0, xlabel=r"$Z_1$", ylabel=r"$Z_2$",
                     xticks=[-3, 0, 3], yticks=[-3, 0, 3], font_size=15).to_edge(LEFT, buff=1.0).shift(DOWN * 0.1)
        ax = plane.ax
        t = ValueTracker(0.0)

        def pts():
            rr = t.get_value()
            y1, y2 = z1, rr * z1 + np.sqrt(1 - rr * rr) * z2
            return VGroup(*[Dot(ax.c2p(np.clip(a, -3.5, 3.5), np.clip(b, -3.5, 3.5)), radius=0.025, color=SPOT)
                            for a, b in zip(y1, y2)])

        cloud = always_redraw(pts)
        rd = readout(r"\rho =", lambda: t.get_value(), digits=2, font_size=34, color=OPT).next_to(plane, UP, buff=0.05)
        eq = VGroup(
            MathTex(r"R = \sqrt{-2\log U_1},\ \ \phi = 2\pi U_2", font_size=30),
            MathTex(r"(Z_1, Z_2) = (R\cos\phi,\ R\sin\phi)", font_size=30),
            MathTex(r"L = \begin{pmatrix}1 & 0\\ \rho & \sqrt{1-\rho^2}\end{pmatrix},\quad X = LZ", font_size=30, color=OPT),
            wrapped_label(rf"Box and Muller (1958): two uniforms, two independent normals. Then Cholesky: "
                          rf"$LL^\top = \Sigma$ gives $\operatorname{{Cov}}(LZ) = L I L^\top = \Sigma$. Here "
                          rf"$\rho = {rho}$, Heston's correlation between price and variance", 5.6, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "A second way, from George Box and Mervin Muller in 1958, makes two normals at once. One uniform sets a "
            "radius, the square root of minus twice its log; the other sets an angle. The result is a round cloud of "
            "independent pairs. <bookmark mark='a'/> Models need correlated noise: Heston's price and variance move "
            f"with correlation {rho}. Multiply the pair by a lower-triangular matrix L whose product with its "
            "transpose is the covariance, the Cholesky factor, and watch the round cloud shear into the tilted "
            "ellipse the model wants."
        ) as vo:
            self.play(FadeIn(plane), FadeIn(cloud), FadeIn(eq[0]), FadeIn(eq[1]))
            vo.wait_until("a")
            self.play(FadeIn(rd), FadeIn(eq[2]), FadeIn(eq[3]))
            self.play(t.animate.set_value(rho), run_time=max(vo.remaining(0.5), 2.5))
        cloud.clear_updaters()
        rd.clear_updaters()
        self.wait(0.3)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"P\big(F^{-1}(U) \le x\big)", r"=", r"P\big(U \le F(x)\big) = F(x)", font_size=36),
            cmath(r"\tfrac{1}{2\pi}e^{-(x^2+y^2)/2}\,dx\,dy", r"=", r"\tfrac{1}{2\pi}e^{-r^2/2}\,r\,dr\,d\phi,\qquad "
                  r"\tfrac{R^2}{2} \sim \text{Exp}(1) = -\log U_1", font_size=32),
            cmath(r"W_{t_k}", r"=", r"\sum_{j \le k}\sqrt{\Delta t}\,Z_j,\qquad W = L_{\text{step}}\,Z", font_size=34,
                  colors={r"W_{t_k}": SPOT}),
            cmath(r"L L^\top", r"=", r"C,\quad C_{ij} = \min(t_i, t_j)\ \Rightarrow\ LZ \overset{d}{=} W", font_size=34,
                  colors={r"L L^\top": OPT}),
        ]
        whys = [why(r"$F$ increasing: the event $F^{-1}(U) \le x$ is the event $U \le F(x)$"),
                why(r"polar coordinates: the Jacobian is $r$, so the angle is uniform and $R^2/2$ is exponential"),
                why(r"a random walk: Brownian motion at the grid is a cumulative sum of scaled normals"),
                why(r"any square root of Brownian motion's covariance gives the same law; which one we choose decides "
                    r"which normals matter (chapter 6)")]
        step = ladder(self, rows, whys, keep=4, top=2.8, x=-1.2, buff=0.6, edge=6.9)
        with self.voiceover(
            "In symbols. The inverse transform works because an increasing function preserves the event. "
            "<bookmark mark='a'/> Box–Muller works because in polar coordinates the Gaussian density factors: the "
            "angle is uniform and half the squared radius is exponential, which is minus the log of a uniform. "
            "<bookmark mark='b'/> A Brownian path on a grid is then a cumulative sum of scaled normals: a matrix "
            "times a vector of independent normals. <bookmark mark='c'/> And here is the hinge for chapter six. Any "
            "matrix whose product with its transpose is Brownian motion's covariance, the minimum of the two times, "
            "builds paths with exactly the same law. They differ only in which normal does which job."
        ) as vo:
            for i, mk in enumerate("abc"):
                step(i)
                vo.wait_until(mk)
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def lab(self, ed):
        card = lab_card(r"the Brownian bridge", [
            "W[:, n] = np.sqrt(T) * z[:, 0]      # first normal: the end",
            "used, h = 1, n",
            "while h > 1:",
            "    half = h // 2",
            "    for left in range(0, n, h):",
            "        right, mid = left + h, left + half",
            "        tl, tr, tm = left*T/n, right*T/n, mid*T/n",
            "        mean = W[:, left] + (tm-tl)/(tr-tl)*(W[:, right]-W[:, left])",
            "        sd = np.sqrt((tm-tl)*(tr-tm)/(tr-tl))",
            "        W[:, mid] = mean + sd * z[:, used]",
            "        used += 1",
            "    h = half",
        ], source="explainer/quant/house/engine.py  brownian_bridge", width=7.6).to_corner(UL, buff=0.35)
        txt = wrapped_label(r"fed the identity matrix, the function returns its own $L$; multiply out $LL^\top$ and "
                            r"compare with $\min(t_i, t_j)$", 4.6, 19, GREY_A).to_corner(UR, buff=0.5)
        with self.voiceover(
            "Here is the House's Brownian bridge, twelve lines. The first normal fixes where the path ends; each pass "
            "halves the gaps, placing every midpoint at its conditional mean given its two neighbours, plus its "
            "conditional standard deviation times the next normal. <bookmark mark='a'/> Feed it the identity "
            "matrix and it hands back its own L. Multiply L by its transpose and compare with the minimum of the "
            "times: they agree to the last bit of double precision, for eight steps and for sixty-four."
        ) as vo:
            self.play(FadeIn(card), FadeIn(txt))
            vo.wait_until("a")
            lab_run(self, card, [f"L = brownian_bridge(np.eye(8), 1).T", f"max |L L' - min(t_i,t_j)| = {ed['dev8']:.1e}",
                                 f"64 steps:                 {ed['dev64']:.1e}"])
        self.wait(0.5)
        self.clear_scene()

    def streams(self, rng):
        n = 12
        tiles = VGroup()
        for j in range(n * 4):
            z = np.random.Generator(np.random.Philox(key=[2026, j])).standard_normal(3)
            col = interpolate_color(ManimColor(QC.SPOT), ManimColor(QC.OPTION), float(ndtr(z[0])))
            tiles.add(VGroup(Square(side_length=0.48, stroke_color=GREY_D, stroke_width=1, fill_color=col,
                                    fill_opacity=0.9), Text(str(j), font_size=12, color=WHITE)))
        tiles.arrange_in_grid(rows=4, cols=n, buff=0.06).to_edge(UP, buff=0.9)
        order = list(np.random.default_rng(3).permutation(len(tiles)))
        head = label(r"path $j$ draws from Philox(key $= 2026$, counter from $j$): any order, the same numbers",
                     font_size=21, color=GREY_A).next_to(tiles, DOWN, buff=0.25)
        stats = VGroup(
            MathTex(rf"\text{{1{{,}}000 paths, shuffled order: identical bits}}\ ({'yes' if rng['philox_same'] else 'no'})",
                    font_size=28, color=GOOD),
            MathTex(rf"\text{{one sequential stream: path 7 alone reproduces it}}\ ({'yes' if rng['seq_same'] else 'no'})",
                    font_size=28, color=BAD),
            MathTex(rf"\text{{Kolmogorov--Smirnov on }}10^6:\ \text{{inverse}}\ {rng['ks_inv']:.4f}\ (p = {rng['ks_inv_p']:.2f}),"
                    rf"\ \ \text{{Box--Muller}}\ {rng['ks_bm']:.4f}\ (p = {rng['ks_bm_p']:.2f})", font_size=26),
            MathTex(rf"10^5\ \text{{payoffs: a Python loop is}}\ {rng['speedup']:,.0f}".replace(",", "{,}") +
                    r"\times\ \text{slower than one numpy line}", font_size=28, color=OPT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.4)
        q = predict(r"Two assets with $\rho = 0.9$. What is the second row of the Cholesky factor?", width=5.0,
                    font_size=21).to_corner(DR, buff=0.3)
        ans = MathTex(r"(0.9,\ \sqrt{0.19}) = (0.9,\ 0.436)", font_size=28, color=GOOD).next_to(q, UP, buff=0.2)
        with self.voiceover(
            "Last, where the uniforms come from on a real machine. numpy's default generator is a sequential "
            "stream: each number follows from the state the last one left. Which numbers a path gets then depends on "
            "how many were drawn before it, and a rerun of one trade's paths, or ten thousand GPU threads, need "
            "something else. <bookmark mark='a'/> Counter-based generators, "
            "like Philox from D. E. Shaw Research in 2011, make each number a pure function of a key and a counter. "
            "Give path j its own key and compute the paths in any order: the numbers are identical, bit for bit. "
            "<bookmark mark='b'/> Both normal recipes pass a Kolmogorov–Smirnov test on a million draws; and a Python "
            f"loop over payoffs is about {rng['speedup']:,.0f} times slower than one vectorised line. <bookmark mark='c'/> Pause and predict: the Cholesky factor for correlation 0.9. "
            "Its second row is 0.9 and the square root of 0.19."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(tiles[k]) for k in order], lag_ratio=0.03, run_time=3), FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(stats[0]), FadeIn(stats[1]))
            vo.wait_until("b")
            self.play(FadeIn(stats[2]), FadeIn(stats[3]))
            vo.wait_until("c")
            self.play(FadeIn(q), FadeIn(ans))
        self.wait(0.5)
        self.clear_scene()
