from __future__ import annotations

import numpy as np

from videos.stats.stats52.common import *  # noqa: F403


class LowRank(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.incoherence()
        self.chart()
        self.picture()
        self.noisy()

    def card(self):
        card = chapter_card(4, r"Low-rank recovery and matrix completion", r"Filling in a table from a few of its entries", lit=(2009,), part=PART)
        with self.voiceover("Chapter four. Low-rank recovery and matrix completion: filling in a table from a few of its entries."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        rows = [
            cmath(r"M \in \mathbb R^{n_1 \times n_2}, \ \mathrm{rank}\, r", r":", r"\text{observe a random set } \Omega \text{ of entries}", font_size=32),
            cmath(r"\text{rank minimization}", r":", r"\min \mathrm{rank}(Z) \text{ s.t. } Z_\Omega = M_\Omega: \ \text{NP-hard}", font_size=32),
            cmath(r"\text{the convex relaxation}", r":", r"\min \|Z\|_* = \textstyle\sum_k \sigma_k(Z) \ \text{ s.t. } Z_\Omega = M_\Omega", font_size=32),
            cmath(r"\text{the analogy}", r":", r"\text{rank : nuclear norm} \ = \ \|\cdot\|_0 : \|\cdot\|_1", font_size=34),
        ]
        rows[2][-1].set_color(BULKC)
        whys = [why(r"a ratings table, \ a sensor array"), why(r"combinatorial"), why(r"Fazel (2002); \ Candès \& Recht (2009)"), why(r"sparsity of the spectrum")]
        heading = label('The estimator, loss, sampling law and target must be specified', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> A matrix of low rank, like a table of ratings that depends on a few tastes, of which we "
            "observe a random set of entries. <bookmark mark='b'/> Finding the matrix of smallest rank that agrees with the "
            "observed entries is computationally hopeless in general. <bookmark mark='c'/> Maryam Fazel's relaxation replaces "
            "the rank by the nuclear norm, the sum of the singular values, which is convex. <bookmark mark='d'/> The analogy "
            "is exact: the rank counts the non-zero singular values, as the l-zero norm counts non-zero coefficients, and the "
            "nuclear norm adds their sizes, as the l-one norm does. Low rank is sparsity of the spectrum."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def incoherence(self):
        rows = [
            cmath(r"\text{a bad matrix}", r":", r"M = e_1 e_1^\top: \ \text{one nonzero entry; \ missed with probability $1-f$ at sampling rate $f$}", font_size=30),
            cmath(r"\text{incoherence}", r":", r"\max_i\|U^\top e_i\|^2,\ \max_j\|V^\top e_j\|^2\le\mu r/n: \ \text{singular vectors spread out}", font_size=30),
            cmath(r"|\Omega|", r"\gtrsim", r"\mu\, r\, n \log^2 n \ \Rightarrow \ \text{exact recovery, \ w.h.p.}", font_size=34),
            cmath(r"\text{degrees of freedom}", r":", r"r(n_1 + n_2 - r): \ \text{only a } \log^2 \text{ factor more}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"no method can see it"), why(r"Candès \& Recht (2009)"), why(r"Candès \& Tao (2010); \ Gross, \ Recht (2011)"), why(r"the information limit")]
        heading = label('Both singular spaces must be spread across the sampled coordinates', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Not every low-rank matrix can be completed. A matrix with a single non-zero entry has rank one, but unless that entry is observed, no method can find it. <bookmark mark='b'/> Emmanuel Candès and Benjamin Recht's condition of 2009 rules this out: both row and column singular spaces must be incoherent, spread across the coordinates rather than concentrated on a few. <bookmark mark='c'/> For square matrices under the theorem's incoherence conditions and uniform independent sampling, as later sharpened by Candès and Terence Tao, David Gross and Recht, observing about mu r n log squared n entries at random suffices for the nuclear-norm solution to be exactly the matrix, with high probability. <bookmark mark='d'/> A rank-r matrix has r times n one plus n two minus r free parameters, so this is only a log-squared factor more than counting allows. The proof's key step is matrix Bernstein, from Part fifty-one."     ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("complete")
        f = np.asarray([r["frac"] for r in d["rows"]])
        e = np.log10(np.maximum([r["err"] for r in d["rows"]], 1e-4))
        A = axes([0, 0.52], [-3, 0.2], x_length=7.4, y_length=4.4, xlabel=r"fraction of entries observed", ylabel=r"$\log_{10}$ relative error",
                 xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[-3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        c = VGroup(polyline(ax, f, e, BULKC, 4), *[Dot(ax.c2p(a, b), radius=0.1, color=BULKC) for a, b in zip(f, e)])
        dof = DashedLine(ax.c2p(d["dof_frac"], -3), ax.c2p(d["dof_frac"], 0.2), color=SPIKEC, stroke_width=2.5)
        r = {x["frac"]: x["err"] for x in d["rows"]}
        side = fit_rows(VGroup(
            label(rf"${d['n']} \times {d['n']}$, \ rank {d['r']}; \ final $\lambda=0.05$; \ checked fixed-point residual; \ 4 trials", font_size=22),
            label(rf"gold: \ degrees of freedom, \ {d['dof']} = {100 * d['dof_frac']:.1f}\% of entries", font_size=22, color=SPIKEC),
            label(rf"teal: \ error {r[0.06]:.2f} at 6\%, \ {r[0.15]:.2f} at 15\%", font_size=22, color=BULKC),
            label(rf"from 30\%: \ {r[0.3]:.4f}, \ finite-penalty relative error", font_size=22, color=GOODC),
            label(r"finite-run illustration; \ not a recovery guarantee", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A test: a hundred by hundred matrix of rank three, completed by SoftImpute from Part thirty-two, with a fixed decreasing penalty schedule ending at point oh five and an accelerated proximal solver checked to a normalized fixed-point residual below two times ten to the minus seven. Four trials contribute each plotted median. <bookmark mark='b'/> The gold line marks the degrees of freedom, {d['dof']} parameters, {100 * d['dof_frac']:.1f} percent of the entries: a generic parameter-counting benchmark, not an exact universal finite-matrix recovery threshold. <bookmark mark='c'/> With six percent observed the relative error is {say(r[0.06], 2)}; with fifteen, {say(r[0.15], 2)}. <bookmark mark='d'/> At thirty percent the reported finite-penalty relative error is small. It is not exact equality or a convergence certificate. <bookmark mark='e'/> This realization is compatible with substantial recovery above the parameter count; four finite runs do not verify a high-probability recovery theorem."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(dof), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def picture(self):
        N = 16
        r = np.random.default_rng(11)
        M = np.outer(r.standard_normal(N), r.standard_normal(N)) + 0.6 * np.outer(r.standard_normal(N), r.standard_normal(N))
        obs = r.random((N, N)) < 0.45
        frac = float(obs.mean())
        lo, hi = M.min(), M.max()
        from explainer.stats.kit import sparse as SPK

        Z = None
        for lam in (2.0, 1.0, 0.3, 0.05, 0.01, 0.001):
            Z = SPK.soft_impute(M, obs, lam, iters=2000, Z0=Z)["Z"]
        rel = float(np.linalg.norm(Z - M) / np.linalg.norm(M))

        def grid(show_all: bool, A=M):
            g = VGroup()
            for i in range(N):
                for j in range(N):
                    t = min(max((A[i, j] - lo) / (hi - lo), 0.0), 1.0)
                    col = interpolate_color(ManimColor(BULKC), ManimColor(SPIKEC), t)
                    vis = show_all or obs[i, j]
                    g.add(Square(side_length=0.24, fill_color=col if vis else GREY_E, fill_opacity=0.9 if vis else 0.4, stroke_width=0.5,
                                 stroke_color=GREY_D).move_to([j * 0.26, -i * 0.26, 0]))
            return g

        left = grid(False).move_to([-3.3, 0.2, 0])
        right = grid(True, Z).move_to([3.3, 0.2, 0])
        arr = Arrow([-1.0, 0.2, 0], [1.0, 0.2, 0], color=GREY_B, buff=0.1)
        l1 = label(rf"{100 * frac:.0f}\% observed, \ rank 2", font_size=24, color=GREY_A).next_to(left, DOWN, buff=0.3)
        l2 = label(rf"SoftImpute's completion: \ relative error {rel:.4f}", font_size=24, color=GOODC).next_to(right, DOWN, buff=0.3)
        with self.voiceover(
            f"<bookmark mark='a'/> What it looks like: a sixteen by sixteen table of rank two with {100 * frac:.0f} percent of its entries seen, the rest grey. <bookmark mark='b'/> The low-rank structure lets the algorithm infer a candidate completion in this realization: SoftImpute fills the table with a relative error of {say(rel, 4)}, finite-penalty relative errorly. This was the idea behind the Netflix Prize of 2006 to 2009, where most of a matrix of users' ratings of films was missing."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(l1))
            vo.wait_until("b")
            self.play(GrowArrow(arr), FadeIn(right), FadeIn(l2))
        self.wait(1.0)
        self.clear_scene()

    def noisy(self):
        rows = [
            cmath(r"Y_\Omega = M_\Omega + E_\Omega", r":", r"\text{uniform sampling, controlled noise and entry/spikiness bounds}", font_size=34),
            cmath(r"\hat M", r"=", r"\arg\min_{\|Z\|_\infty\le a}\tfrac12\|Y_\Omega-Z_\Omega\|_F^2+\lambda\|Z\|_*", font_size=32),
            cmath(r"\tfrac{\|\hat M - M\|_F^2}{n_1 n_2}", r"\lesssim", r"(\sigma^2+a^2)\frac{r(n_1+n_2)\log n}{|\Omega|}\quad (\|M\|_\infty\le a)", font_size=34),
            cmath(r"\text{bounded-entry class, sampling/noise/RSC conditions}", r":", r"\text{up to the log; \ Part 50's lower bounds for matrices}", font_size=32),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"real data are noisy"), why(r"Mazumder, \ Hastie \& Tibshirani (2010)"), why(r"Koltchinskii, \ Lounici \& Tsybakov (2011)"), why(r"the theorem of chapter 3")]
        heading = label('Class-wide completion rates require matrix, sampling and noise bounds', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Real entries are noisy. <bookmark mark='b'/> Then the equality constraint becomes a squared-error loss, and a nuclear-norm penalty yields a SoftImpute-style estimator. The displayed bounded variant also constrains the entry magnitudes, as required for the stated class-wide rate. <bookmark mark='c'/> Vladimir Koltchinskii, Karim Lounici and Alexandre Tsybakov proved in 2011 that under suitable sampling, noise and matrix-class bounds, a nuclear-penalized estimator achieves a per-entry error rate involving the rank, dimensions and a logarithm over the observed sample size. Bounded-entry or spikiness terms and the precise estimator matter; this is not a noise-only guarantee for every low-rank matrix. <bookmark mark='d'/> That is minimax up to the log, and it is the decomposable-regularizer theorem of chapter three again, with the nuclear norm in place of the l-one norm."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
