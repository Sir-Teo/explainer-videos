from __future__ import annotations

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


class MatrixBernstein(VoiceoverScene):
    def construct(self):
        self.card()
        self.why_matrices()
        self.theorem()
        self.chart()
        self.dimension()
        self.uses()

    def card(self):
        card = chapter_card(5, r"Matrix concentration", r"Bernstein's inequality, \ for sums of random matrices", lit=(2012,), part=PART)
        with self.voiceover("Chapter five. Matrix concentration: Bernstein's inequality, for sums of random matrices."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def why_matrices(self):
        rows = fit_rows(VGroup(
            label(r"many estimators are sums of independent random matrices:", font_size=28, color=GREY_A),
            label(r"the sample covariance: \ $\hat\Sigma - \Sigma = \tfrac1n \sum_i (x_i x_i^\top - \Sigma)$", font_size=26, color=MATC),
            label(r"a random graph's adjacency matrix: \ $\sum_{i<j} A_{ij}(e_i e_j^\top + e_j e_i^\top)$", font_size=26, color=MATC),
            label(r"random sampling of a matrix's entries, \ columns, \ or rows", font_size=26, color=MATC),
            label(r"the question: \ how large is $\|\sum_i X_i\|_{op}$? \ \ a scalar Bernstein for matrices", font_size=26, color=BNDC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Why sums of random matrices? Because many statistical objects are sums of independent "
            "random matrices. <bookmark mark='b'/> The sample covariance minus the truth is an average of the independent "
            "matrices x x transpose minus sigma. <bookmark mark='c'/> A random graph's adjacency matrix is a sum of "
            "independent edges, each contributing a rank-two matrix. <bookmark mark='d'/> Sampling entries, rows or columns of "
            "a large matrix, as in matrix completion and randomized linear algebra, produces such sums too. <bookmark "
            "mark='e'/> In each case we want the operator norm of the sum: Bernstein's inequality, but for matrices."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def theorem(self):
        rows = [
            cmath(r"X_i \text{ independent, symmetric } p \times p", r":", r"E X_i = 0, \ \ \|X_i\| \le L", font_size=34),
            cmath(r"v", r"=", r"\big\|\textstyle\sum_i E X_i^2\big\|: \ \text{the matrix variance}", font_size=34),
            cmath(r"P\big(\|\textstyle\sum X_i\| \ge t\big)", r"\le", r"2p \exp\!\Big(\frac{-t^2/2}{v + Lt/3}\Big)", font_size=34),
            cmath(r"E\|\textstyle\sum X_i\|", r"\le", r"\sqrt{2v\log 2p} + \tfrac13 L\log 2p", font_size=34),
        ]
        rows[2][-1].set_color(BNDC)
        rows[3][-1].set_color(BNDC)
        whys = [why(r"bounded, \ centred"), why(r"variance in operator norm"), why(r"Tropp (2012); \ Ahlswede--Winter (2002)"), why(r"the price: \ $\log p$")]
        with self.voiceover(
            "<bookmark mark='a'/> The setting: independent, symmetric, p by p random matrices, each with mean zero and operator "
            "norm at most L. <bookmark mark='b'/> Their matrix variance, v, is the operator norm of the sum of the expected "
            "squares, the exact analogue of the sum of variances. <bookmark mark='c'/> Joel Tropp's matrix Bernstein "
            "inequality of 2012, sharpening Rudolf Ahlswede and Andreas Winter's of 2002, says that the norm of the sum "
            "exceeds t with probability at most two p times the scalar Bernstein bound. <bookmark mark='d'/> In expectation: "
            "the root of two v log two p, plus a third of L log two p. The only cost of moving from numbers to matrices is the "
            "dimension factor p in front, which becomes a log p in the bound. The proof replaces the moment generating "
            "function by a trace exponential, and uses Lieb's concavity theorem of 1973 where the scalar proof uses independence."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("bernstein")
        n = np.asarray([r["n"] for r in d["rows"]], float)
        ln = np.log10(n)
        lg = lambda key: np.log10([r[key] for r in d["rows"]])  # noqa: E731
        A = axes([1.9, 3.6], [-0.7, 0.55], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10} \|S - I\|_{op}$",
                 xticks=[2, np.log10(400), np.log10(3200)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[-0.5, 0, 0.5], center=[-2.5, 0.2, 0])
        ax = A.ax
        cb = VGroup(polyline(ax, ln, lg("bound"), BNDC, 4), *[Dot(ax.c2p(a, b), radius=0.07, color=BNDC) for a, b in zip(ln, lg("bound"))])
        cm = VGroup(polyline(ax, ln, lg("mp"), EXACTC, 3), *[Dot(ax.c2p(a, b), radius=0.06, color=EXACTC) for a, b in zip(ln, lg("mp"))])
        cs = VGroup(*[Dot(ax.c2p(a, b), radius=0.1, color=MATC) for a, b in zip(ln, lg("mean"))])
        r0, r1 = d["rows"][0], d["rows"][-1]
        side = fit_rows(VGroup(
            label(r"$S = \tfrac1n\sum x_i x_i^\top$, \ $x_i$ uniform on $\sqrt{p}\,S^{p-1}$, \ $p = 50$", font_size=22),
            label(r"purple: \ matrix Bernstein, \ $L = p/n$, \ $v = (p-1)/n$", font_size=22, color=BNDC),
            label(rf"teal: \ simulated, \ {r0['mean']:.2f} at $n = 100$, \ {r1['mean']:.2f} at 3,200", font_size=22, color=MATC),
            label(r"white: \ the Marchenko--Pastur edge, \ $2\sqrt\gamma + \gamma$", font_size=22, color=EXACTC),
            label(r"Bernstein is valid at every $n$; \ about $1.6\times$ too big", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        ratio = float(np.mean([r["bound"] / r["mean"] for r in d["rows"]]))
        with self.voiceover(
            f"<bookmark mark='a'/> A test: fifty-dimensional vectors drawn uniformly from the sphere of radius root fifty, "
            f"so each has identity covariance and is bounded, and the error of their sample covariance. <bookmark mark='b'/> "
            f"Matrix Bernstein's bound, in purple, with L equal to p over n and variance p minus one over n. <bookmark "
            f"mark='c'/> The simulated error, in teal: {say(r0['mean'], 2)} with a hundred observations, {say(r1['mean'], 2)} "
            f"with three thousand two hundred. <bookmark mark='d'/> The Marchenko–Pastur edge, in white, is the asymptotic "
            f"answer, and it is very close. <bookmark mark='e'/> The matrix Bernstein bound holds at every sample size and is "
            f"about {ratio:.1f} times too large here, a modest price for a bound that needed only a norm bound and a variance."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ bounds exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cs), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cm), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def dimension(self):
        rows = [
            cmath(r"\text{diagonal } X_i = \varepsilon_i\, e_{k_i} e_{k_i}^\top", r":", r"\|\textstyle\sum X_i\| = \max_k |\text{a sum of } n/p \text{ signs}|", font_size=30),
            cmath(r"\text{there}", r":", r"\text{the max of } p \text{ independent sums: \ } \sqrt{(n/p)\, 2\log p}: \ \log p \text{ is real}", font_size=30),
            cmath(r"\text{rotation-invariant } X_i", r":", r"\text{no } \log p: \ \text{Marchenko--Pastur's } 2\sqrt{p/n}", font_size=30),
            cmath(r"\text{closing the gap}", r":", r"\text{Bandeira, \ Boedihardjo \& van Handel (2023)}", font_size=30),
        ]
        rows[1][-1].set_color(BADC)
        rows[2][-1].set_color(GOODC)
        whys = [why(r"commuting matrices"), why(r"the bound is attained"), why(r"what we just simulated"), why(r"intrinsic freeness")]
        with self.voiceover(
            "<bookmark mark='a'/> Is the log p factor a weakness of the proof? Not in general. Take diagonal matrices, each a "
            "random sign in one random diagonal position. Their sum is diagonal, and its norm is the largest of p independent "
            "sums of signs. <bookmark mark='b'/> That is the maximum of p roughly Gaussian variables, of size the root of two "
            "log p: the log p factor is real. <bookmark mark='c'/> For matrices that are spread out in every direction, like "
            "the sphere's rank-one matrices we just simulated, the log p disappears, and the truth is Marchenko–Pastur's two "
            "root p over n. <bookmark mark='d'/> When the log p is and is not needed was settled only in 2023, by Afonso "
            "Bandeira, March Boedihardjo and Ramon van Handel, whose theory of intrinsic freeness says when a random matrix "
            "behaves like the free, rotation-invariant model."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def uses(self):
        rows = fit_rows(VGroup(
            label(r"what matrix Bernstein buys:", font_size=28, color=GREY_A),
            label(r"covariance estimation for bounded vectors: \ $n \gtrsim p\log p / \varepsilon^2$", font_size=26, color=MATC),
            label(r"spectral clustering: \ a random graph's adjacency is its mean plus a small matrix", font_size=26, color=MATC),
            label(r"matrix completion: \ sampled entries concentrate around the full matrix (Part 52)", font_size=26, color=MATC),
            label(r"randomized SVD and sketching: \ sampled columns preserve the spectrum", font_size=26, color=MATC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What it buys. <bookmark mark='b'/> Covariance estimation for any bounded vectors, not just "
            "Gaussian ones, with p log p over epsilon squared observations. <bookmark mark='c'/> Spectral clustering, because "
            "a random graph's adjacency matrix is its expected value plus a matrix whose norm the inequality controls, so the "
            "top eigenvectors reveal the communities. <bookmark mark='d'/> Matrix completion, in Part fifty-two, where a few "
            "observed entries concentrate around the full matrix. <bookmark mark='e'/> And randomized numerical linear "
            "algebra, where a sample of columns preserves a matrix's spectrum."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
