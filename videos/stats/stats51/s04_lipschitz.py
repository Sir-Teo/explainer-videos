from __future__ import annotations

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


class Lipschitz(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.herbst()
        self.chart()
        self.maxtable()
        self.sphere()
        self.talagrand()

    def card(self):
        card = chapter_card(3, r"Concentration of Lipschitz functions", r"Anything smooth of many independent pieces is nearly constant", lit=(1976,), part=PART)
        with self.voiceover("Chapter three. Concentration of Lipschitz functions: anything smooth of many independent pieces is nearly constant."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"f: \mathbb R^n \to \mathbb R, \ |f(x) - f(y)| \le L\|x - y\|", r":", r"L\text{-Lipschitz}", font_size=32),
            cmath(r"g \sim N(0, I_n)", r":", r"P\big(f(g) - E f(g) \ge t\big) \le e^{-t^2/(2L^2)}", font_size=34),
            cmath(r"\mathrm{Var}\, f(g)", r"\le", r"L^2: \ \text{the Gaussian Poincaré inequality}", font_size=34),
            cmath(r"\text{no dependence on } n", r":", r"\text{the norm, \ the maximum, \ the operator norm, \ any sup of linear forms}", font_size=30),
        ]
        rows[1][-1].set_color(GAUSSC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"changes by at most $L$ per unit move"), why(r"Tsirelson--Ibragimov--Sudakov (1976)"), why(r"Nash; \ Chernoff (1981)"), why(r"dimension-free")]
        with self.voiceover(
            "<bookmark mark='a'/> The general principle. A function of n variables is L-Lipschitz if moving the input a "
            "distance d moves the output at most L times d. <bookmark mark='b'/> Boris Tsirelson, Ildar Ibragimov and "
            "Vladimir Sudakov proved in 1976 that if the input is a standard Gaussian vector, the function exceeds its mean by "
            "t with probability at most e to the minus t squared over two L squared. <bookmark mark='c'/> Its variance is at "
            "most L squared, the Gaussian Poincaré inequality. <bookmark mark='d'/> What is remarkable is what is missing: the "
            "dimension n. The length of the vector, its largest coordinate, the operator norm of a random matrix, any "
            "supremum of linear forms: all are Lipschitz, and all concentrate around their means with Gaussian tails, in any "
            "dimension."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def herbst(self):
        rows = [
            cmath(r"\text{Gaussian log-Sobolev}", r":", r"\mathrm{Ent}(f^2) \le 2\,E\|\nabla f\|^2", font_size=34),
            cmath(r"\text{apply it to } e^{\lambda f/2}", r":", r"\tfrac{d}{d\lambda}\Big(\tfrac{1}{\lambda}\log E e^{\lambda(f - Ef)}\Big) \le \tfrac{L^2}{2}", font_size=32),
            cmath(r"\text{integrate}", r":", r"E e^{\lambda(f - Ef)} \le e^{\lambda^2 L^2/2}: \ f \text{ is sub-Gaussian}", font_size=32),
            cmath(r"\text{tensorization}", r":", r"\text{log-Sobolev for one coordinate} \Rightarrow \text{for } n, \ \text{same constant}", font_size=30),
        ]
        rows[2][-1].set_color(GAUSSC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Gross (1975)"), why(r"Herbst's argument"), why(r"chapter 1's definition"), why(r"why $n$ never appears")]
        with self.voiceover(
            "<bookmark mark='a'/> One proof, in outline, because it shows where the dimension goes. Leonard Gross's Gaussian "
            "log-Sobolev inequality of 1975 bounds the entropy of a squared function by twice its expected squared gradient. "
            "<bookmark mark='b'/> Applied to the exponential of lambda f over two, it becomes a differential inequality for "
            "the log moment generating function of f, Herbst's argument. <bookmark mark='c'/> Integrating it gives exactly the "
            "sub-Gaussian bound of chapter one, with variance proxy L squared. <bookmark mark='d'/> And the dimension never "
            "enters, because log-Sobolev inequalities tensorize: if each coordinate satisfies one, the product measure "
            "satisfies the same inequality with the same constant."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("lipschitz")
        t = np.asarray(d["t"])
        A = axes([0, 3], [-4.5, 0.1], x_length=7.4, y_length=4.4, xlabel=r"$t$", ylabel=r"$\log_{10} P(f - Ef \ge t)$",
                 xticks=[0, 1, 2, 3], yticks=[-4, -3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        lg = lambda v: np.log10(np.maximum(np.asarray(v, float), 1e-5))  # noqa: E731
        okm = np.asarray(d["tail_max"]) > 0
        okn = np.asarray(d["tail_norm"]) > 0
        cm = clip_curve(ax, t[okm], lg(np.asarray(d["tail_max"])[okm]), SPHC, 4, ymin=-4.5, ymax=0.1)
        cn = clip_curve(ax, t[okn], lg(np.asarray(d["tail_norm"])[okn]), GAUSSC, 4, ymin=-4.5, ymax=0.1)
        cb = clip_curve(ax, t, lg(d["bound"]), BNDC, 3.5, ymin=-4.5, ymax=0.1)
        side = fit_rows(VGroup(
            label(r"$g \sim N(0, I_{1000})$, \ 20,000 draws", font_size=22),
            label(r"purple: \ the bound $e^{-t^2/2}$, \ for every 1-Lipschitz $f$", font_size=22, color=BNDC),
            label(rf"blue: \ $f = \|g\|$: \ variance {d['var_norm']:.3f}", font_size=22, color=GAUSSC),
            label(rf"gold: \ $f = \max_i g_i$: \ variance {d['var_max']:.3f}", font_size=22, color=SPHC),
            label(r"both under the bound; \ the max far under", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A Gaussian vector in a thousand dimensions, twenty thousand times. <bookmark mark='b'/> The "
            f"purple curve is the concentration bound, valid for every one-Lipschitz function. <bookmark mark='c'/> The length "
            f"of the vector is one: its upper tail, in blue, sits under the bound, and its variance, {say(d['var_norm'], 2)}, "
            f"is half the Poincaré bound of one. <bookmark mark='d'/> The largest coordinate is another: its tail, in "
            f"gold, falls much faster, and its variance is only {say(d['var_max'], 2)}. <bookmark mark='e'/> The theorem is a "
            f"guarantee, not a prediction: some Lipschitz functions concentrate far more than it promises, and the maximum is "
            f"one of them, a phenomenon called superconcentration."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ bound exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cn), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cm), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def maxtable(self):
        d = load("lipschitz")
        rows = [[r"$n$", r"$E \max_i g_i$ \ (exact)", r"simulated", r"$\sqrt{2 \log n}$", r"SD of the max"]]
        for r in d["rows"]:
            rows.append([f"{r['n']:,}", f"{r['exact_mean']:.3f}", f"{r['mean']:.3f}", f"{r['sqrt2log']:.3f}", f"{r['sd']:.3f}"])
        tab = table_rows(rows, font_size=30, col_buff=0.8, row_buff=0.38, colors=[GREY_B] + [None] * 4)
        tab.move_to([0, 0.8, 0])
        for i in range(1, 5):
            tab[i][1].set_color(EXACTC)
            tab[i][4].set_color(SPHC)
        foot = label(r"the mean grows like $\sqrt{2\log n}$, \ slowly; \ the spread \emph{shrinks}, \ like $1/\sqrt{2 \log n}$", font_size=24, color=GREY_A).move_to([0, -1.5, 0])
        foot2 = label(r"the maximum of many Gaussians is a nearly deterministic number", font_size=24, color=SPHC).move_to([0, -2.3, 0])
        r = d["rows"]
        with self.voiceover(
            f"<bookmark mark='a'/> The maximum of n independent standard normals. Its mean grows like the root of two log n, "
            f"but slowly: {say(r[0]['exact_mean'], 2)} at ten, {say(r[-1]['exact_mean'], 2)} at ten thousand, always below the "
            f"root of two log n. <bookmark mark='b'/> And its standard deviation shrinks, from {say(r[0]['sd'], 2)} to "
            f"{say(r[-1]['sd'], 2)}. <bookmark mark='c'/> The maximum of ten thousand Gaussians is very nearly a fixed number, "
            f"which is why Part thirty-three's Bonferroni thresholds and Part fifty's universal thresholds work as well as they do."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated; \ exact by quadrature")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def sphere(self):
        rows = [
            cmath(r"x \text{ uniform on } \sqrt n\, S^{n-1}", r":", r"P(|f(x) - Ef| \ge t) \le 2e^{-c t^2/L^2}", font_size=32),
            cmath(r"f(x) = x_1", r":", r"\text{Lipschitz with } L = 1: \ \text{the hook's equator, \ explained}", font_size=32),
            cmath(r"\text{the isoperimetric inequality}", r":", r"\text{among sets of a given area, \ caps have the smallest boundary}", font_size=30),
            cmath(r"\text{Lévy's proof}", r":", r"\text{neighbourhoods of a half-sphere swallow almost everything}", font_size=32),
        ]
        rows[1][-1].set_color(SPHC)
        whys = [why(r"the same for the sphere"), why(r"scale: \ radius $\sqrt n$"), why(r"Lévy, \ Schmidt (1948)"), why(r"geometry behind the bound")]
        with self.voiceover(
            "<bookmark mark='a'/> The same concentration holds on the sphere of radius root n: Lipschitz functions of a "
            "uniform point concentrate with Gaussian tails, independent of the dimension. <bookmark mark='b'/> The first "
            "coordinate is one-Lipschitz, which explains the hook: on the unit sphere it is within a few over root n of zero. "
            "<bookmark mark='c'/> Lévy's proof rested on the spherical isoperimetric inequality: among all sets with a given "
            "area, spherical caps have the smallest boundary. <bookmark mark='d'/> So the set of points within a small "
            "distance of a half-sphere, the equatorial band thickened on one side, already contains almost all of the sphere, "
            "and any Lipschitz function, being nearly its median on that set, is nearly constant."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def talagrand(self):
        rows = fit_rows(VGroup(
            label(r"beyond Gaussians:", font_size=28, color=GREY_A),
            label(r"bounded independent coordinates: \ Talagrand's convex-distance inequality (1995)", font_size=26, color=GAUSSC),
            label(r"for \emph{convex} Lipschitz $f$ of independent $X_i \in [0, 1]$: \ $P(|f - Mf| \ge t) \le 4 e^{-t^2/4}$", font_size=26, color=GOODC),
            label(r"convexity is needed: \ without it, \ bounded coordinates can fail to concentrate", font_size=26, color=BADC),
            label(r"the same mechanism powers Part 48's Talagrand inequality for empirical processes", font_size=26, color=SPHC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Beyond Gaussian inputs. <bookmark mark='b'/> For independent bounded coordinates, Michel "
            "Talagrand's convex-distance inequality of 1995 does the same job, <bookmark mark='c'/> for convex Lipschitz "
            "functions: they are within t of their median except with probability four e to the minus t squared over four, "
            "whatever the dimension. <bookmark mark='d'/> Convexity cannot be dropped: there are non-convex Lipschitz "
            "functions of bounded coordinates that do not concentrate at this rate. <bookmark mark='e'/> And the same "
            "mechanism lies under Part forty-eight's Talagrand inequality for the supremum of an empirical process, which is "
            "a convex function of the sample."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
