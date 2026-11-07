from __future__ import annotations

import numpy as np

from videos.stats.stats51.common import *  # noqa: F403


class RandomMatrices(VoiceoverScene):
    def construct(self):
        self.card()
        self.nets()
        self.singular()
        self.mp()
        self.covariance()
        self.cancer()
        self.shuffle()

    def card(self):
        card = chapter_card(4, r"Random matrices, \ non-asymptotically", r"$\sqrt n \pm \sqrt p$, \ and what it says about covariances", lit=(1985,), part=PART)
        with self.voiceover("Chapter four. Random matrices, non-asymptotically: root n plus or minus root p, and what it says about covariances."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def nets(self):
        rows = [
            cmath(r"\|A\|_{op}", r"=", r"\sup_{\|u\| = \|v\| = 1} u^\top A v: \ \text{a supremum of linear forms}", font_size=32),
            cmath(r"\varepsilon\text{-net } \mathcal N \text{ of } S^{p-1}", r":", r"|\mathcal N| \le (1 + 2/\varepsilon)^p, \ \ \|A\| \le \tfrac{1}{1 - \varepsilon}\max_{v \in \mathcal N} \|Av\|", font_size=30),
            cmath(r"\text{each } \|Av\|", r":", r"\text{concentrates (chapter 3); \ a union bound over } e^{O(p)} \text{ points}", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"\|A\| \le C(\sqrt n + \sqrt p + t) \ \text{w.p. } 1 - 2e^{-t^2}, \ \text{independent centred entries, uniformly bounded }\psi_2", font_size=30),
        ]
        rows[3][-1].set_color(MATC)
        whys = [why(r"a Lipschitz function of $A$"), why(r"a volume argument"), why(r"concentration $\times$ counting"), why(r"Vershynin's Theorem 4.4.5")]
        heading = label('A finite net controls a centered sub-Gaussian matrix norm', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The operator norm of a matrix is the supremum of u transpose A v over unit vectors: a supremum of linear forms, so the methods of chapter three apply. <bookmark mark='b'/> The standard argument replaces the sphere by a finite epsilon-net, a set of points within epsilon of every unit vector. A volume argument shows one exists with at most one plus two over epsilon, to the p, points, and the norm on the net controls the norm everywhere. <bookmark mark='c'/> Each A v has a concentrated length, and a union bound over the exponentially many net points costs only a term of order p in the exponent. <bookmark mark='d'/> The result: for an n by p matrix with independent, mean-zero sub-Gaussian entries with a common norm bound, the operator norm is at most a constant times root n plus root p, with overwhelming probability."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def singular(self):
        d = load("matrices")
        p = np.asarray([r["p"] for r in d["rows"]], float)
        A = axes([0, 420], [0, 42], x_length=7.4, y_length=4.4, xlabel=rf"$p$ \ (columns), \ $n = {d['n']}$ rows", ylabel=r"singular value",
                 xticks=[0, 100, 200, 300, 400], yticks=[0, 10, 20, 30, 40], center=[-2.5, 0.2, 0])
        ax = A.ax
        u = np.linspace(0, 400, 200)
        gmax = polyline(ax, u, np.sqrt(d["n"]) + np.sqrt(u), EXACTC, 3)
        gmin = polyline(ax, u, np.sqrt(d["n"]) - np.sqrt(u), EXACTC, 3)
        smax = VGroup(*[Dot(ax.c2p(a, r["max"]), radius=0.08, color=MATC) for a, r in zip(p, d["rows"])])
        smin = VGroup(*[Dot(ax.c2p(a, r["min"]), radius=0.08, color=SPHC) for a, r in zip(p, d["rows"])])
        r100 = [r for r in d["rows"] if r["p"] == 100][0]
        side = fit_rows(VGroup(
            label(r"Gaussian $n \times p$ matrices, \ 20 per $p$", font_size=22),
            label(r"white: \ $\sqrt n + \sqrt p$ \ and \ $\sqrt n - \sqrt p$", font_size=22, color=EXACTC),
            label(rf"teal: \ the largest: \ {r100['max']:.2f} at $p = 100$ \ (30)", font_size=22, color=MATC),
            label(rf"gold: \ the smallest: \ {r100['min']:.2f} \ (10)", font_size=22, color=SPHC),
            label(r"$p=n$: \ smallest positive a.s.; \ tends to zero with size", font_size=22, color=BADC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Gaussian matrices with four hundred rows and a varying number of columns. <bookmark mark='b'/> Yehoram Gordon's inequality, from chapter seven, gives the white curves: the expected largest singular value is at most root n plus root p, and the smallest at least root n minus root p. <bookmark mark='c'/> The simulated largest values sit just under the upper curve: {say(r100['max'], 1)} at a hundred columns, against thirty. <bookmark mark='d'/> The smallest sit just above the lower one: {say(r100['min'], 1)} against ten. <bookmark mark='e'/> As square Gaussian matrices grow, their smallest singular value tends to zero; at a fixed size it is positive almost surely, and the matrix becomes nearly singular, which is why least squares fails when p approaches n."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ curves exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(gmax), Create(gmin), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(smax), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(smin), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def mp(self):
        d = load("matrices")
        e = np.asarray(d["edges"])
        A = axes([0, 2.6], [0, 1.4], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue of $S = X^\top X / n$, \ $\Sigma = I$", ylabel=r"density",
                 xticks=[0, 0.25, 1, 2.25], yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        hb = hist_bars(ax, e, d["hist"], color=MATC, opacity=0.55)
        mpc = polyline(ax, d["mp_x"], d["mp_pdf"], EXACTC, 4)
        one = DashedLine(ax.c2p(1, 0), ax.c2p(1, 1.4), color=SPHC, stroke_width=2.5)
        side = fit_rows(VGroup(
            label(r"$n = 2{,}000$, \ $p = 500$: \ $\gamma = p/n = 1/4$", font_size=22),
            label(r"the truth: \ every eigenvalue is 1 \ (gold)", font_size=22, color=SPHC),
            label(rf"teal: \ the sample's, \ from {d['ev_min']:.2f} to {d['ev_max']:.2f}", font_size=22, color=MATC),
            label(r"white: \ Marchenko--Pastur, \ edges $(1 \pm \sqrt\gamma)^2$", font_size=22, color=EXACTC),
            label(r"2,000 observations, \ and the spectrum is badly spread", font_size=22, color=BADC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> What this means for covariance estimation. Two thousand observations of five hundred "
            f"variables, all independent with variance one. <bookmark mark='b'/> The true covariance is the identity: every "
            f"eigenvalue is one. <bookmark mark='c'/> The sample covariance's eigenvalues spread from {say(d['ev_min'], 2)} to "
            f"{say(d['ev_max'], 2)}. <bookmark mark='d'/> They follow the Marchenko–Pastur law of 1967, whose support runs "
            f"from one minus root gamma, squared, to one plus root gamma, squared, with gamma the ratio of variables to "
            f"observations. <bookmark mark='e'/> Two thousand observations sounds like a lot, but with five hundred variables "
            f"the sample covariance badly distorts the spectrum, inflating the largest eigenvalues and shrinking the smallest, "
            f"with no signal at all."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ the law exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(one), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(hb), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(mpc), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def covariance(self):
        d = load("matrices")
        rows = [[r"$n$"] + [f"{r['n']:,}" for r in d["cov"]],
                [r"$E\|S - I\|_{op}$, \ simulated"] + [f"{r['err']:.3f}" for r in d["cov"]],
                [r"MP edge $(1 + \sqrt\gamma)^2 - 1$"] + [f"{r['limit']:.3f}" for r in d["cov"]],
                [r"$\sqrt{p/n}$"] + [f"{r['sqrt']:.3f}" for r in d["cov"]]]
        tab = table_rows(rows, font_size=28, col_buff=0.6, row_buff=0.4, colors=[GREY_B, MATC, EXACTC, GREY_A])
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.8, 0])
        foot = label(rf"$p = {d['cov_p']}$: \ the operator-norm error is about $2\sqrt{{p/n}} + p/n$", font_size=24, color=GREY_A).move_to([0, -1.3, 0])
        foot2 = label(r"to estimate a $p \times p$ covariance to accuracy $\varepsilon$ \ needs $n \gtrsim p/\varepsilon^2$: \ linear in $p$, \ not $p^2$", font_size=24, color=GOODC).move_to([0, -2.1, 0])
        c = d["cov"]
        with self.voiceover(
            f"<bookmark mark='a'/> The operator-norm error of the sample covariance, for a hundred variables. With a hundred "
            f"observations it is {say(c[0]['err'], 1)}, useless; with three thousand two hundred, {say(c[-1]['err'], 2)}. The "
            f"simulation tracks the edge of the Marchenko–Pastur law, two root gamma plus gamma. <bookmark mark='b'/> The "
            f"error is of order the root of p over n. <bookmark mark='c'/> So estimating a p by p covariance matrix to "
            f"accuracy epsilon in operator norm needs about p over epsilon squared observations: linear in the dimension, "
            f"even though the matrix has p squared entries. The non-asymptotic theory gives the same answer at every n."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def cancer(self):
        d = load("cancer")
        k = np.arange(1, d["p"] + 1)
        A = axes([0, 31], [-4.3, 1.4], x_length=7.4, y_length=4.4, xlabel=r"eigenvalue rank", ylabel=r"$\log_{10}$ eigenvalue of the correlation matrix",
                 xticks=[1, 5, 10, 20, 30], yticks=[-4, -3, -2, -1, 0, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        ev = np.log10(np.maximum(d["ev"], 1e-3))
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.08, color=SPHC if b > np.log10(d["mp_hi"]) else GREY_B) for a, b in zip(k, ev)])
        band = Rectangle(width=ax.c2p(31, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, np.log10(d["mp_hi"]))[1] - ax.c2p(0, np.log10(d["mp_lo"]))[1],
                         fill_color=MATC, fill_opacity=0.2, stroke_width=0).move_to(ax.c2p(15.5, (np.log10(d["mp_hi"]) + np.log10(d["mp_lo"])) / 2))
        side = fit_rows(VGroup(
            label(rf"Wisconsin breast cancer: \ $n = {d['n']}$, \ $p = {d['p']}$", font_size=22),
            label(rf"teal band: \ Marchenko--Pastur, \ $[{d['mp_lo']:.2f}, {d['mp_hi']:.2f}]$", font_size=22, color=MATC),
            label(rf"gold: \ {d['above']} above an asymptotic reference edge", font_size=22, color=SPHC),
            label(rf"the top one: \ {100 * d['share_top']:.0f}\% of the variance; \ top five: \ {100 * d['share_top5']:.0f}\%", font_size=22, color=SPHC),
            label(r"below the band: \ near-collinear features", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Real data: the Wisconsin breast cancer measurements of Part thirty-four, five hundred and sixty-nine biopsies and thirty features of the cell nuclei. <bookmark mark='b'/> The Marchenko–Pastur band is an asymptotic reference for standardized independent noise, not a finite-sample confidence band. Its edges here are {say(d['mp_lo'], 2)} to {say(d['mp_hi'], 2)}. <bookmark mark='c'/> {d['above']} eigenvalues stand clearly above it. This suggests strong dependence, but crossing an asymptotic edge alone is not a calibrated test. <bookmark mark='d'/> The largest alone carries {100 * d['share_top']:.0f} percent of the total variance, and the top five {100 * d['share_top5']:.0f} percent. <bookmark mark='e'/> Many eigenvalues fall below the band, because several features are nearly linear combinations of others, radius, perimeter and area, for instance. Random matrix theory supplies the null against which a spectrum is judged."       ) as vo:
            self.play(FadeIn(A), FadeIn(museum_tag(r"Wolberg, \ Street \& Mangasarian (1995)")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dots), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def shuffle(self):
        d = load("cancer")
        rows = [
            cmath(r"\text{shuffle each column independently}", r":", r"\text{the margins kept, \ every dependence destroyed}", font_size=32),
            cmath(r"\text{the shuffled spectrum}", r":", rf"\text{{largest }} {d['ev_shuffled'][0]:.2f}, \ \text{{inside the band's edge }} {d['mp_hi']:.2f}", font_size=32),
            cmath(r"\text{the real spectrum}", r":", rf"\text{{largest }} {d['ev'][0]:.2f}: \ \text{{{d['ev'][0] / d['mp_hi']:.0f} times the edge}}", font_size=32),
            cmath(r"\text{399 column permutations}", r":", rf"\text{{95\% max threshold }} {d['top_threshold95']:.2f},\ \text{{top-eigenvalue }} p={d['top_pvalue']:.4f}", font_size=30),
        ]
        rows[1][-1].set_color(MATC)
        rows[2][-1].set_color(SPHC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Part 16's permutations"), why(r"one shuffled realization, not a calibrated test"), why(r"signal does not"), why(r"Horn's parallel analysis (1965)")]
        heading = label('Repeated column permutations calibrate a global independence null', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> A check that needs no theory: shuffle each feature's values independently, keeping every empirical margin and breaking the rowwise associations, under an independent-column null. <bookmark mark='b'/> The shuffled data's largest eigenvalue is {say(d['ev_shuffled'][0], 2)}, inside the Marchenko–Pastur edge of {say(d['mp_hi'], 2)}, in this one shuffle. A single shuffle does not calibrate a test. <bookmark mark='c'/> The real largest eigenvalue is {say(d['ev'][0], 1)}, about {d['ev'][0] / d['mp_hi']:.0f} times the edge. <bookmark mark='d'/> To calibrate the comparison we also use three hundred ninety-nine independent column permutations. Their largest-eigenvalue distribution gives a global independence-null reference. This is related to Horn's parallel analysis; it does not prove a count of latent factors."     ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
