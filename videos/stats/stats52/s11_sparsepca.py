from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class SparsePCA(VoiceoverScene):
    def construct(self):
        self.card()
        self.idea()
        self.chart()
        self.barrier()
        self.graphs()
        self.graph_chart()

    def card(self):
        card = chapter_card(10, r"Sparse PCA and graphical models", r"Structure beats the BBP threshold, \ at a price", lit=(2009,), part=PART)
        with self.voiceover("Chapter ten. Sparse PCA and graphical models: structure beats the BBP threshold, at a price."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def idea(self):
        rows = [
            cmath(r"v \text{ has } k \ll p \text{ non-zero entries}", r":", r"\text{the signal lives on a few variables}", font_size=32),
            cmath(r"\text{PCA}", r":", r"\text{inconsistent when } p/n \not\to 0, \ \text{and blind below } \sqrt{p/n}", font_size=32),
            cmath(r"\text{diagonal thresholding}", r":", r"\text{keep the } k \text{ largest variances, \ then PCA on them}", font_size=32),
            cmath(r"\text{minimax benchmark, not diagonal-thresholding guarantee}", r":", r"\sin^2\angle(\hat v, v) \lesssim 1\wedge\frac{(1+\ell)k\log(ep/k)}{n\ell^2}: \ p \text{ only in a log}", font_size=32),
        ]
        rows[2][-1].set_color(LASSOC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"interpretable components"), why(r"Johnstone \& Lu (2009)"), why(r"Johnstone \& Lu's estimator"), why(r"Vu \& Lei (2013), \ minimax")]
        heading = label('Diagonal thresholding and the sparse-PCA minimax benchmark differ', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> If the signal direction has only k non-zero entries, so that the signal lives on a few variables, structure can help. <bookmark mark='b'/> Iain Johnstone and Arthur Lu showed in 2009 that ordinary PCA is inconsistent whenever p over n does not go to zero, and blind below the BBP threshold. <bookmark mark='c'/> Their remedy, diagonal thresholding, is almost embarrassingly simple: the variables carrying the signal have larger variances, so keep the k with the largest sample variances and run PCA on those alone. <bookmark mark='d'/> The minimax squared-angle rate is capped at one and involves one plus ell over ell squared, times k log of p over k over n in the appropriate sparse-spike regime. This is a benchmark for suitable estimators; plain diagonal thresholding need not attain it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("spca")
        n = np.log10([r["n"] for r in d["rows"]])
        A = axes([1.6, 3.0], [0, 1.0], x_length=7.4, y_length=4.4, xlabel=rf"$n$ \ (log scale), \ $p = {d['p']:,}$", ylabel=r"$\langle\hat v, v\rangle^2$",
                 xticks=[np.log10(50), 2, np.log10(200), np.log10(400), np.log10(800)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cp = VGroup(polyline(ax, n, [r["pca"] for r in d["rows"]], BADC, 4), *[Dot(ax.c2p(a, r["pca"]), radius=0.08, color=BADC) for a, r in zip(n, d["rows"])])
        cd = VGroup(polyline(ax, n, [r["dt"] for r in d["rows"]], LASSOC, 4), *[Dot(ax.c2p(a, r["dt"]), radius=0.08, color=LASSOC) for a, r in zip(n, d["rows"])])
        cb = VGroup(polyline(ax, n, [r["bbp"] for r in d["rows"]], TRUEC, 2.5), *[Dot(ax.c2p(a, r["bbp"]), radius=0.05, color=TRUEC) for a, r in zip(n, d["rows"])])
        r = {x["n"]: x for x in d["rows"]}
        side = fit_rows(VGroup(
            label(rf"spike $\ell = {d['ell']:g}$ on $k = {d['k']}$ of {d['p']:,} variables", font_size=22),
            label(r"white: \ PCA's BBP limit: \ zero until $p/n < \ell^2 = 4$", font_size=22, color=TRUEC),
            label(rf"red: \ PCA, \ {r[200]['pca']:.2f} at $n = 200$", font_size=22, color=BADC),
            label(rf"blue: \ diagonal thresholding, \ {r[200]['dt']:.2f} at $n = 200$", font_size=22, color=LASSOC),
            label(rf"$n = 800$: \ {r[800]['pca']:.2f} against {r[800]['dt']:.2f}", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test: a spike of strength two on ten of a thousand variables. <bookmark mark='b'/> PCA's "
            f"BBP limit, in white, is zero until p over n falls below ell squared, four, at two hundred and fifty "
            f"observations. <bookmark mark='c'/> PCA, in red, follows it: at two hundred observations its squared overlap is "
            f"{say(r[200]['pca'], 2)}, nothing. <bookmark mark='d'/> Diagonal thresholding, in blue, already reaches "
            f"{say(r[200]['dt'], 2)} there, below the threshold that blinds PCA. <bookmark mark='e'/> With eight hundred "
            f"observations PCA reaches {say(r[800]['pca'], 2)} and diagonal thresholding {say(r[800]['dt'], 2)}: knowing the "
            f"signal is sparse doubles what can be recovered."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ BBP exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cb), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cp), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cd), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def barrier(self):
        rows = [
            cmath(r"\text{information}", r":", r"n \gtrsim k\log p/\ell^2 \text{ suffices for some estimator}", font_size=32),
            cmath(r"\text{diagonal thresholding}", r":", r"\text{needs } n \gtrsim k^2\log p/\ell^2 \text{ in the hardest cases}", font_size=32),
            cmath(r"\text{the gap}", r":", r"k\log p \text{ vs } k^2\log p: \ \text{conditional, regime-specific computational evidence}", font_size=32),
            cmath(r"\text{evidence}", r":", r"\text{reduction from planted clique \ (Part 50)}", font_size=32),
        ]
        rows[2][-1].set_color(BADC)
        whys = [why(r"exhaustive search"), why(r"and SDPs: \ d'Aspremont et al. (2007)"), why(r"a computational barrier"), why(r"Berthet \& Rigollet (2013)")]
        heading = label('Sparse-PCA computational gaps are conditional and regime dependent', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> But there is a catch, and Part fifty met it. In principle, k log p over ell squared observations suffice, for an estimator that searches over all supports of size k. <bookmark mark='b'/> For flat sparse spikes, diagonal thresholding typically needs order k squared log p over ell squared samples. Computational lower bounds are conditional and regime-specific; there is no single universal sample requirement for every polynomial-time algorithm. <bookmark mark='c'/> The gap between k and k squared is a statistical–computational gap. <bookmark mark='d'/> Quentin Berthet and Philippe Rigollet showed in 2013 that sufficiently strong improvements in their specified asymptotic detection regimes would yield fast planted-clique algorithms, contrary to a standard conjecture. This is conditional evidence, not an unconditional finite-sample lower bound. Sparse PCA is the standard example of a problem where the information is in the data but may not be extractable in reasonable time."       ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def graphs(self):
        rows = [
            cmath(r"x \sim N(0, \Sigma), \ \Theta = \Sigma^{-1}", r":", r"\Theta_{jk} = 0 \iff x_j \perp x_k \mid \text{rest}", font_size=32),
            cmath(r"\text{neighbourhood selection}", r":", r"\text{lasso of each } x_j \text{ on the others; \ edges where selected}", font_size=30),
            cmath(r"\text{the graphical lasso}", r":", r"\max_\Theta \log\det\Theta - \mathrm{tr}(S\Theta) - \lambda\|\Theta\|_1", font_size=32),
            cmath(r"\text{consistency}", r":", r"n \gtrsim d^2\log p, \ \ d = \text{max degree; beta-min, spectra and incoherence conditions}", font_size=30),
        ]
        rows[1][-1].set_color(LASSOC)
        rows[2][-1].set_color(BULKC)
        whys = [why(r"Part 31's graphs"), why(r"Meinshausen \& Bühlmann (2006)"), why(r"Friedman, \ Hastie \& Tibshirani (2008)"), why(r"Ravikumar et al. (2011)")]
        heading = label('Gaussian graph recovery needs signal, spectrum and incoherence conditions', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Sparsity in the inverse covariance means something different: a zero entry of the precision matrix says two variables are independent given all the others, an absent edge in a graphical model, as in Part thirty-one. <bookmark mark='b'/> Nicolai Meinshausen and Peter Bühlmann's neighbourhood selection of 2006 regresses each variable on all the others by the lasso, and draws an edge wherever a coefficient survives. <bookmark mark='c'/> The graphical lasso of Friedman, Hastie and Tibshirani penalizes the Gaussian likelihood directly. <bookmark mark='d'/> Graph recovery also requires minimum edge strength, controlled spectra and the method-specific incoherence conditions; a degree-squared-log-p sample order is a representative sufficient regime, as Pradeep Ravikumar and colleagues proved in 2011."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def graph_chart(self):
        d = load("spca")
        n = np.log10([r["n"] for r in d["graph"]])
        A = axes([1.3, 2.7], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=rf"$n$ \ (log scale), \ a chain on $p = {d['graph_p']}$ nodes", ylabel=r"rate",
                 xticks=[np.log10(25), np.log10(50), 2, np.log10(200), np.log10(400)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        ct = VGroup(polyline(ax, n, [r["tpr"] for r in d["graph"]], GOODC, 4), *[Dot(ax.c2p(a, r["tpr"]), radius=0.08, color=GOODC) for a, r in zip(n, d["graph"])])
        cf = VGroup(polyline(ax, n, [r["fpr"] for r in d["graph"]], BADC, 4), *[Dot(ax.c2p(a, r["fpr"]), radius=0.08, color=BADC) for a, r in zip(n, d["graph"])])
        g = {r["n"]: r for r in d["graph"]}
        side = fit_rows(VGroup(
            label(r"neighbourhood selection, \ the AND rule", font_size=22),
            label(r"the truth: \ a chain, \ $x_j$ linked to $x_{j \pm 1}$ only", font_size=22, color=TRUEC),
            label(rf"green: \ true edges found, \ {100 * g[25]['tpr']:.0f}\% at $n = 25$, \ {100 * g[100]['tpr']:.0f}\% at 100", font_size=22, color=GOODC),
            label(rf"red: \ fraction of absent edges selected, \ {100 * g[25]['fpr']:.1f}\% \ to {100 * g[400]['fpr']:.1f}\%", font_size=22, color=BADC),
            label(r"25 observations, \ 435 possible edges", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test of neighbourhood selection, keeping an edge only when both regressions select it. <bookmark mark='b'/> The truth is a chain of thirty variables, each linked only to its neighbours. <bookmark mark='c'/> With twenty-five observations it finds {100 * g[25]['tpr']:.0f} percent of the true edges, and the plotted average true-edge rate reaches one in the sampled replicates. This does not establish certain exact-graph recovery. <bookmark mark='d'/> The rate of false edges stays between {100 * g[400]['fpr']:.1f} and {100 * g[25]['fpr']:.1f} percent. <bookmark mark='e'/> That is with twenty-five observations and four hundred and thirty-five possible edges: sparsity makes the graph learnable from far fewer observations than parameters."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ct), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cf), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
