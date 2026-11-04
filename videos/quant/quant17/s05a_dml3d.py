from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant17.common import BAD, GOOD, NET, OPT, PART, REF, ask, grid_fn, illustration, load, surf3d_axes

METH = [("plain", BAD, r"network, payoffs only"), ("diff", GOOD, r"network, payoffs and slopes"),
        ("gp", QC.Q, r"Gaussian process with gradients")]


class DML3D(VoiceoverScene, ThreeDScene):
    def construct(self):
        r = load("dml2d")
        self.card()
        self.planes(r)
        self.gp_derive()
        self.gp_shell(r)
        self.table(r)

    def card(self):
        c = chapter_card(7, r"Differential labels in three dimensions", r"What does a slope label look like, and who "
                         r"used it first?", part=PART)
        with self.voiceover("Chapter seven. Differential labels in three dimensions."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def _axes(self, r):
        g1, g2 = np.asarray(r["g1"]), np.asarray(r["g2"])
        zmax = float(np.asarray(r["exact"]).max()) * 1.1
        ax = surf3d_axes([g1[0], g1[-1], 20], [g2[0], g2[-1], 20], [0, zmax, 10], x_length=6.6, y_length=5.0,
                         z_length=3.2).shift(DOWN * 0.4)
        return ax, g1, g2, zmax

    def _surf(self, ax, g1, g2, Z, zmax, col, opacity=0.6, res=(18, 18)):
        f = grid_fn(g1, g2, np.clip(np.asarray(Z), 0, zmax))
        return Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(g1[0], g1[-1]), v_range=(g2[0], g2[-1]),
                       resolution=res, fill_color=col, fill_opacity=opacity, stroke_width=0.3, stroke_color=col,
                       checkerboard_colors=False)

    def planes(self, r):
        ax, g1, g2, zmax = self._axes(r)
        S = r["samples"]
        X, Y, dY = np.asarray(S["X"]), np.asarray(S["Y"]), np.asarray(S["dY"])
        m = (X[:, 0] > g1[0]) & (X[:, 0] < g1[-1]) & (X[:, 1] > g2[0]) & (X[:, 1] < g2[-1]) & (Y < zmax)
        dots = VGroup(*[Dot3D(ax.c2p(a, b, c), radius=0.05, color=OPT, resolution=(4, 4))
                        for (a, b), c in zip(X[m], Y[m])])
        h = 0.06 * (g1[-1] - g1[0])
        tiles = VGroup()
        for (a, b), c, (p, q) in zip(X[m], Y[m], dY[m]):
            corners = [(a + sa * h, b + sb * h, c + p * sa * h + q * sb * h) for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            if all(0 <= z <= zmax for _, _, z in corners):
                tiles.add(Polygon(*[ax.c2p(*cc) for cc in corners], stroke_color=GOOD, stroke_width=1,
                                  fill_color=GOOD, fill_opacity=0.35))
        ex = self._surf(ax, g1, g2, r["exact"], zmax, WHITE, opacity=0.08)
        pl = self._surf(ax, g1, g2, r["surfs"]["plain"], zmax, BAD)
        df = self._surf(ax, g1, g2, r["surfs"]["diff"], zmax, GOOD)
        s0 = r["seeds"]["0"]
        hint = VGroup(label(r"asset 1 (across), asset 2 (back), price (up)", font_size=19, color=GREY_A),
                      legend([(OPT, r"64 simulated payoffs"), (GOOD, r"their pathwise tangent planes"),
                              (WHITE, r"the exact price (faint)"), (BAD, r"fit to payoffs only"),
                              (GOOD, r"fit to payoffs and slopes")], font_size=16)).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.15).to_corner(UL, buff=0.3)
        errs = label(rf"grid error: {s0['plain']:.2f} without slopes, {s0['diff']:.2f} with", font_size=20,
                     color=GREY_A).to_corner(DR, buff=0.35)
        self.set_camera_orientation(phi=64 * DEGREES, theta=-50 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(hint, errs)
        self.remove(hint, errs)
        with self.voiceover(
            "Two assets now, so the price is a surface we can see. Sixty-four training states, each with one simulated "
            "payoff: the pink dots, hovering above and below the true price, which is the faint sheet. "
            "<bookmark mark='a'/> Now give each its pathwise gradient, drawn as a small tangent plane. Each plane is "
            "tilted the way the payoff moves when each asset moves, on that one path. <bookmark mark='b'/> Fit a "
            "network to the dots alone: with sixty-four noisy heights, the red surface wobbles between them. "
            "<bookmark mark='c'/> Fit it to the dots and the planes: the green surface hugs the true price, because "
            f"every sample also says which way it tilts. On a fine grid, the error falls from {s0['plain']:.2f} to "
            f"{s0['diff']:.2f}."
        ) as vo:
            self.play(Create(ax), FadeIn(hint[0]), FadeIn(ex))
            self.play(FadeIn(dots), FadeIn(hint[1][0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t_) for t_ in tiles], lag_ratio=0.03), FadeIn(hint[1][1]), FadeIn(hint[1][2]))
            vo.wait_until("b")
            self.play(Create(pl), FadeIn(hint[1][3]), run_time=2)
            self.move_camera(theta=-30 * DEGREES, run_time=2)
            vo.wait_until("c")
            self.play(FadeOut(pl), Create(df), FadeIn(hint[1][4]), FadeIn(errs), run_time=2)
            self.move_camera(theta=-70 * DEGREES, phi=70 * DEGREES, run_time=max(vo.remaining(0.3), 1.5))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, dots, tiles, ex, df)),
                                                                  FadeOut(hint), FadeOut(errs)], run_time=1.2)
        self.clear_scene()

    def gp_derive(self):
        rows = [cmath(r"f", r"\sim", r"\mathcal{GP}(m, k),\quad k(x, x') = s^2 e^{-\lVert x - x'\rVert^2 / 2\ell^2}",
                      font_size=38, colors={r"f": QC.Q}),
                cmath(r"\operatorname{Cov}\big(f(x), \partial_j f(x')\big)", r"=", r"\partial_{x'_j} k(x, x'),\quad "
                      r"\operatorname{Cov}\big(\partial_i f(x), \partial_j f(x')\big) = \partial_{x_i}\partial_{x'_j} k",
                      font_size=34, colors={r"=": WHITE}),
                cmath(r"\bar f(x_*)", r"=", r"m + k_*^\top \big(K + \Sigma\big)^{-1}\big[\,y - m;\ \partial y\,\big]",
                      font_size=38, colors={r"\bar f(x_*)": QC.Q}),
                cmath(r"\text{cost}", r"=", r"O\big((n(1 + d))^3\big)\ \ \text{vs}\ \ O(n)\ \text{per epoch}", font_size=38,
                      colors={r"\text{cost}": OPT})]
        whys = [why(r"Dixon, Halperin and Bilokon (ch.\ 3): a Gaussian process puts a prior on functions; its kernel "
                    r"says how alike two prices are, given how close their states are"),
                why(r"differentiation is linear, so derivatives of a Gaussian process are jointly Gaussian with it, with "
                    r"covariances that are derivatives of the kernel: slope observations enter exactly like price ones"),
                why(r"the posterior mean given the $n$ payoffs and the $n d$ slopes, stacked, with their noise $\Sigma$: the "
                    r"same information differential machine learning uses, combined exactly, with error bars"),
                why(r"but one linear solve on $n(1 + d)$ observations: cubic. At $n = 64$, $d = 2$ that is 192; at a "
                    r"desk's $n = 10^5$ and $d = 100$ it is ten million, and the network's linear cost is the reason to "
                    r"use one")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.4, buff=0.62, edge=6.9)
        with self.voiceover(
            "Using slopes as labels has a classical twin. A Gaussian process puts a probability distribution on "
            "functions: its kernel says how alike two prices are, given how close their states are. "
            "<bookmark mark='a'/> Differentiation is linear, so the derivative of a Gaussian process is Gaussian too, "
            "jointly with the process, and its covariances are simply derivatives of the kernel. A slope observation "
            "enters the model exactly the way a price observation does. <bookmark mark='b'/> Condition on both, and "
            "the posterior mean is one linear solve over the stacked payoffs and slopes: the same information "
            "differential machine learning uses, combined exactly, and with error bars. <bookmark mark='c'/> The catch "
            "is the cost: cubic in the number of observations. Fine for sixty-four samples on two assets; hopeless for "
            "a desk's hundred thousand on a hundred. The network is the scalable version."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
        self.wait(0.4)
        self.clear_scene()

    def gp_shell(self, r):
        ax, g1, g2, zmax = self._axes(r)
        mu = np.asarray(r["surfs"]["gp"])
        sd = np.asarray(r["gp_sd"])
        gp = self._surf(ax, g1, g2, mu, zmax, QC.Q, opacity=0.7)
        up = self._surf(ax, g1, g2, mu + 2 * sd, zmax, GREY_B, opacity=0.12, res=(14, 14))
        dn = self._surf(ax, g1, g2, mu - 2 * sd, zmax, GREY_B, opacity=0.12, res=(14, 14))
        S = r["samples"]
        X, Y = np.asarray(S["X"]), np.asarray(S["Y"])
        m = (X[:, 0] > g1[0]) & (X[:, 0] < g1[-1]) & (X[:, 1] > g2[0]) & (X[:, 1] < g2[-1]) & (Y < zmax)
        dots = VGroup(*[Dot3D(ax.c2p(a, b, c), radius=0.05, color=OPT, resolution=(4, 4)) for (a, b), c in zip(X[m], Y[m])])
        s0 = r["seeds"]["0"]
        hint = VGroup(legend([(QC.Q, r"posterior mean"), (GREY_B, r"plus and minus two standard deviations")],
                             font_size=17),
                      label(rf"length scale {s0['gp_ls']:.0f}, chosen by cross-validation on the payoffs; grid error "
                            rf"{s0['gp']:.2f}", font_size=18, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.15).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=66 * DEGREES, theta=-55 * DEGREES, zoom=0.9)
        self.add_fixed_in_frame_mobjects(hint)
        self.remove(hint)
        with self.voiceover(
            "Here is the Gaussian process on the same sixty-four payoffs and slopes: its mean, and a translucent shell "
            "two standard deviations above and below. <bookmark mark='a'/> The shell is thin where the samples are "
            "dense and opens up at the corners, where nothing was observed. A network gives you a number; the process "
            f"also tells you where not to believe it. Its grid error here is {s0['gp']:.2f}."
        ) as vo:
            self.play(Create(ax), FadeIn(dots), FadeIn(hint[0]))
            self.play(Create(gp), run_time=2)
            vo.wait_until("a")
            self.play(FadeIn(up), FadeIn(dn), FadeIn(hint[1]))
            self.move_camera(theta=-25 * DEGREES, run_time=max(vo.remaining(0.3), 2))
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, added_anims=[FadeOut(VGroup(ax, gp, up, dn, dots)),
                                                                  FadeOut(hint)], run_time=1.2)
        self.clear_scene()

    def table(self, r):
        seeds = r["seeds"]
        head = VGroup(label(r"", font_size=20), *[label(rf"seed {s}", font_size=20, color=GREY_A) for s in seeds],
                      label(r"mean", font_size=20, color=GREY_A))
        tab = VGroup(head)
        means = {}
        for k, col, t in METH:
            v = [seeds[s][k] for s in seeds]
            means[k] = float(np.mean(v))
            tab.add(VGroup(label(t, font_size=21, color=col), *[MathTex(f"{x:.2f}", font_size=30, color=col) for x in v],
                           MathTex(f"{means[k]:.2f}", font_size=30, color=col)))
        xs = [-4.0, -0.6, 1.2, 3.0, 5.0]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 1.6 - 0.8 * i, 0])
        ttl = label(r"Price error (RMSE) on a $41 \times 41$ grid, 64 samples, two assets", font_size=28).to_edge(UP, buff=0.6)
        best = min(means, key=means.get)
        names = {"plain": "the plain network", "diff": "the differential network", "gp": "the Gaussian process"}
        if means["diff"] < means["plain"] and means["gp"] < means["plain"]:
            slopes = "Both methods that use slopes beat the one that does not."
        else:
            slopes = "Here the slopes do not help every method, a reminder that sixty-four samples is very few."
        with self.voiceover(
            "Three seeds, three methods. <bookmark mark='a'/> On average the "
            f"plain network's error is {means['plain']:.2f}, the differential network's {means['diff']:.2f}, and the "
            f"Gaussian process's {means['gp']:.2f}: {names[best]} does best here. {slopes}"
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(tab[0]), FadeIn(tab[1]))
            vo.wait_until("a")
            self.play(FadeIn(tab[2]), FadeIn(tab[3]))
        q = ask(r"a digital pays 1 above the strike. Its pathwise derivative is zero on almost every path. What do "
                r"the slope labels teach the network?")
        with self.voiceover(
            "And the digital: its payoff is flat on both sides of the strike, so its pathwise derivative is zero on "
            "almost every path, and the slopes teach the network that the price is flat. Smooth the payoff, or use "
            "Part sixteen's likelihood-ratio derivatives."
            " Next: a hundred dimensions."
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
