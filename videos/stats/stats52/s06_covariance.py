from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class Covariance(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.methods()
        self.chart()
        self.table()
        self.shrinkage()

    def card(self):
        card = chapter_card(5, r"Covariance estimation", r"When the sample covariance is the wrong answer", lit=(2008,), part=PART)
        with self.voiceover("Chapter five. Covariance estimation: when the sample covariance is the wrong answer."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"S = \tfrac1n\textstyle\sum x_i x_i^\top", r":", r"\|S - \Sigma\|_{op} \asymp \|\Sigma\|\sqrt{p/n}: \ \text{useless when } p \gtrsim n", font_size=30),
            cmath(r"p > n", r":", r"S \text{ is singular: \ no inverse, \ no Mahalanobis, \ no LDA}", font_size=32),
            cmath(r"\text{the way out}", r":", r"\text{structure: \ banded, \ sparse, \ or shrink towards a target}", font_size=32),
            cmath(r"\text{the price}", r":", r"\text{a wrong structure gives a confident wrong answer}", font_size=32),
        ]
        rows[0][-1].set_color(BADC)
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Part 51, \ chapter 4"), why(r"Part 31's methods break"), why(r"as sparsity rescued regression"), why(r"no free lunch")]
        with self.voiceover(
            "<bookmark mark='a'/> Part fifty-one found that the sample covariance's operator-norm error is of order the root "
            "of p over n: useless once the dimension is comparable to the sample size. <bookmark mark='b'/> With more variables "
            "than observations it is singular, so everything in Part thirty-one that needs its inverse, the Mahalanobis "
            "distance, discriminant analysis, Hotelling's test, breaks. <bookmark mark='c'/> The way out, as for regression, is "
            "structure: covariances that are banded, sparse, or close to a simple target. <bookmark mark='d'/> And the price, "
            "as always, is that an assumed structure that is wrong gives a confident wrong answer."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def methods(self):
        rows = [
            cmath(r"\text{banding}", r":", r"B_k(S)_{ij} = S_{ij}\,1\{|i - j| \le k\}: \ \text{for ordered variables}", font_size=32),
            cmath(r"\text{thresholding}", r":", r"T_t(S)_{ij} = S_{ij}\,1\{|S_{ij}| \ge t\}, \ t \asymp \sqrt{\log p/n}", font_size=32),
            cmath(r"\text{rate, \ banded class}", r":", r"\|B_k(S) - \Sigma\| \lesssim (\log p/n)^{\alpha/(2\alpha + 2)}", font_size=32),
            cmath(r"\text{Ledoit--Wolf}", r":", r"\hat\Sigma = \rho\,\mu I + (1 - \rho) S, \ \ \rho \text{ estimated in closed form}", font_size=32),
        ]
        rows[0][-1].set_color(LASSOC)
        rows[1][-1].set_color(BULKC)
        rows[3][-1].set_color(SPIKEC)
        whys = [why(r"Bickel \& Levina (2008a)"), why(r"Bickel \& Levina (2008b)"), why(r"decay $|i - j|^{-\alpha - 1}$"), why(r"Ledoit \& Wolf (2004)")]
        with self.voiceover(
            "<bookmark mark='a'/> Three remedies. For variables with a natural order, like times or positions on a genome, "
            "Peter Bickel and Elizaveta Levina's banding of 2008 keeps only the entries near the diagonal. <bookmark "
            "mark='b'/> For variables with no order, their thresholding keeps only the entries larger than a constant times "
            "the root of log p over n, the size of a pure-noise entry. <bookmark mark='c'/> Over classes of covariances whose "
            "entries decay away from the diagonal, both achieve rates that depend on p only through log p. <bookmark "
            "mark='d'/> And Olivier Ledoit and Michael Wolf's shrinkage of 2004 pulls the sample covariance towards a multiple "
            "of the identity, with the amount estimated in closed form; it needs no structure at all, and is always invertible."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("cov")
        n = np.log10([r["n"] for r in d["rows"]])
        A = axes([1.6, 3.0], [-0.3, 1.15], x_length=7.4, y_length=4.4, xlabel=rf"$n$ \ (log scale), \ $p = {d['p']}$", ylabel=r"$\log_{10}\|\hat\Sigma - \Sigma\|_{op}$",
                 xticks=[np.log10(50), 2, np.log10(200), np.log10(400), np.log10(800)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[0, 0.5, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cols = {"sample": BADC, "lw": SPIKEC, "thresh": BULKC, "band": LASSOC}
        cs = {k: VGroup(polyline(ax, n, np.log10([r[k] for r in d["rows"]]), c, 4),
                        *[Dot(ax.c2p(a, b), radius=0.07, color=c) for a, b in zip(n, np.log10([r[k] for r in d["rows"]]))]) for k, c in cols.items()}
        r0 = d["rows"][0]
        side = fit_rows(VGroup(
            label(rf"AR(1), \ $\Sigma_{{ij}} = {d['rho']}^{{|i-j|}}$, \ $\|\Sigma\| = {d['sig_norm']:.2f}$", font_size=22),
            label(rf"red: \ sample covariance, \ {r0['sample']:.1f} at $n = 50$", font_size=22, color=BADC),
            label(rf"gold: \ Ledoit--Wolf, \ {r0['lw']:.1f}", font_size=22, color=SPIKEC),
            label(rf"teal: \ thresholding, \ {r0['thresh']:.1f}; \ blue: \ banding, \ {r0['band']:.1f}", font_size=22, color=LASSOC),
            label(r"the more structure assumed, \ the smaller the error", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test: two hundred variables with autoregressive correlation {d['rho']}, whose covariance "
            f"has operator norm {say(d['sig_norm'], 2)}. <bookmark mark='b'/> The sample covariance's error with fifty "
            f"observations is {say(r0['sample'], 1)}, twice the size of the matrix itself. <bookmark mark='c'/> Ledoit–Wolf "
            f"shrinkage, which assumes nothing about structure, cuts it to {say(r0['lw'], 1)}. <bookmark mark='d'/> "
            f"Thresholding, which assumes sparsity, gets {say(r0['thresh'], 1)}, and banding, which assumes the order matters, "
            f"{say(r0['band'], 1)}. The banding and thresholding levels were chosen by an oracle here; in practice, by "
            f"cross-validation or a risk estimate. <bookmark mark='e'/> The more correct structure an estimator assumes, the "
            f"smaller its error."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ oracle tuning")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs["sample"]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cs["lw"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs["thresh"]), Create(cs["band"]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def table(self):
        d = load("cov")
        rows = [[r"$n$"] + [str(r["n"]) for r in d["rows"]],
                [r"sample"] + [f"{r['sample']:.2f}" for r in d["rows"]],
                [r"Ledoit--Wolf"] + [f"{r['lw']:.2f}" for r in d["rows"]],
                [r"thresholding"] + [f"{r['thresh']:.2f}" for r in d["rows"]],
                [r"banding"] + [f"{r['band']:.2f}" for r in d["rows"]]]
        tab = table_rows(rows, font_size=28, col_buff=0.7, row_buff=0.4, colors=[GREY_B, BADC, SPIKEC, BULKC, LASSOC])
        tab.move_to([0, 0.9, 0])
        rr = d["rows"]
        foot = label(rf"at $n = 800 = 4p$, \ the sample covariance still errs by {rr[-1]['sample']:.2f}; \ banding by {rr[-1]['band']:.2f}", font_size=24, color=GREY_A).move_to([0, -1.5, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The numbers. Every method improves with n, but the order never changes. <bookmark "
            f"mark='b'/> Even with eight hundred observations, four for every variable, the sample covariance errs by "
            f"{say(rr[-1]['sample'], 2)} in operator norm, while banding errs by {say(rr[-1]['band'], 2)}, almost three times "
            f"less."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def shrinkage(self):
        rows = [
            cmath(r"\text{the eigenvalues}", r":", r"S \text{ spreads them (Marchenko--Pastur); \ shrinkage pulls them back}", font_size=30),
            cmath(r"\text{linear shrinkage}", r":", r"\text{one } \rho \text{ for all: \ Ledoit--Wolf}", font_size=32),
            cmath(r"\text{nonlinear shrinkage}", r":", r"\text{each eigenvalue moved by inverting the MP map}", font_size=32),
            cmath(r"\text{the precision } \Sigma^{-1}", r":", r"\text{sparse: \ the graphical lasso (Part 31), \ chapter 10}", font_size=32),
        ]
        rows[2][-1].set_color(SPIKEC)
        whys = [why(r"chapter 7's laws"), why(r"Stein (1975)"), why(r"Ledoit \& Wolf (2012, 2020)"), why(r"conditional independence")]
        with self.voiceover(
            "<bookmark mark='a'/> Why shrinkage works. The sample covariance spreads the eigenvalues out, as the hook showed, "
            "the large ones too large and the small ones too small. Shrinkage pulls them back together. <bookmark mark='b'/> "
            "Ledoit–Wolf moves them all by the same proportion. <bookmark mark='c'/> Their later nonlinear shrinkage moves each "
            "eigenvalue by its own amount, by inverting the Marchenko–Pastur map, which chapter seven derives, an idea that "
            "goes back to Charles Stein in 1975. <bookmark mark='d'/> And when the inverse covariance is the object of "
            "interest, sparsity there means conditional independence, the graphical models of chapter ten."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
