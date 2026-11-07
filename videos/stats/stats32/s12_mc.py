from __future__ import annotations

import numpy as np

from videos.stats.stats32.common import *  # noqa: F403


class Completion(VoiceoverScene):
    def construct(self):
        self.card()
        self.netflix()
        self.lowrank()
        self.nuclear()
        self.softimpute()
        self.blocks()
        self.path()
        self.singular()
        self.theory()

    def card(self):
        card = chapter_card(11, r"Matrix completion", r"Sparsity in the singular values", lit=(2010,), part=PART)
        with self.voiceover("Chapter eleven. Matrix completion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def netflix(self):
        rows = fit_rows(VGroup(
            label(r"2006: \ Netflix offers \$1 million for a 10\% better film recommender", font_size=24),
            label(r"480{,}189 users $\times$ 17{,}770 films; \ about 1\% of the ratings known", font_size=24, color=LASSO),
            label(r"fill in the rest: \ which films would each user like?", font_size=24, color=SPIKE),
            label(r"won in 2009 by BellKor's Pragmatic Chaos: \ low-rank factor models at the core", font_size=24, color=GREY_A),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> In 2006 Netflix offered a million dollars to anyone who could improve its film "
            "recommendations by ten percent. <bookmark mark='b'/> The data were a matrix of four hundred and eighty thousand "
            "users by seventeen thousand seven hundred films, with about one percent of the entries known: the ratings users "
            "had actually given. <bookmark mark='c'/> The task was to fill in the rest. <bookmark mark='d'/> The prize was "
            "won in 2009 by a team whose methods had, at their core, low-rank factor models: the idea that tastes are "
            "described by a few hidden dimensions."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def lowrank(self):
        rows = [
            cmath(r"M", r"=", r"U V^\top, \ \ U \in \mathbb R^{m \times r}, \ V \in \mathbb R^{k \times r}, \ r \ll m, k", font_size=30),
            cmath(r"\text{parameters}", r":", r"r(m+k-r) \ \ll \ mk", font_size=32),
            cmath(r"\min \ \mathrm{rank}(Z)", r"\text{ s.t. }", r"Z_{ij} = M_{ij} \text{ on the observed } \Omega", font_size=28),
            cmath(r"\mathrm{rank}(Z)", r"=", r"\|\sigma(Z)\|_0: \ \text{the } \ell_0 \text{ norm of the singular values}", font_size=28),
        ]
        rows[3][-1].set_color(SPIKE)
        whys = [why(r"each user a mix of $r$ tastes"), why(r"subtract $r^2$ factorization redundancies"), why(r"NP-hard again"),
                why(r"the same problem as chapter three")]
        with self.voiceover(
            "<bookmark mark='a'/> Suppose the full matrix has low rank: each user's ratings a combination of a few "
            "taste profiles. <bookmark mark='b'/> Then its identifiable rank-r dimension is r times m plus k minus r,"
            " removing factorization redundancies, far fewer than its m times k entries, and a fraction of the "
            "entries might determine the rest. <bookmark mark='c'/> The direct problem, the matrix of smallest rank "
            "that agrees with the known entries, is NP-hard. <bookmark mark='d'/> And look at it this way: the rank "
            "is the number of nonzero singular values, the zero norm of the vector of singular values. It is chapter "
            "three's problem in disguise."
        ) as vo:
            intro=label('Low rank reduces the identifiable dimension of a matrix model',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nuclear(self):
        rows = [
            cmath(r"\|Z\|_*", r"=", r"\textstyle\sum_i \sigma_i(Z)", font_size=34),
            cmath(r"\|Z\|_*", r":", r"\text{the convex envelope of rank on } \{\|Z\|_{op} \le 1\}", font_size=30),
            cmath(r"\min_Z", r"", r"\tfrac12 \|P_\Omega(M - Z)\|_F^2 + \lambda\|Z\|_*", font_size=32),
            cmath(r"\text{prox}", r":", r"\text{soft-threshold the singular values}", font_size=30),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"the nuclear norm: \ $\ell_1$ of the singular values"), why(r"Fazel (2002), \ as chapter three"),
                why(r"the matrix lasso"), why(r"singular value thresholding")]
        with self.voiceover(
            "<bookmark mark='a'/> The same relaxation works. Replace the rank by the nuclear norm, the sum of the "
            "singular values, their one norm. <bookmark mark='b'/> Maryam Fazel showed in 2002 that it is the convex "
            "envelope of rank on the unit operator-norm ball, paralleling the bounded-box count relaxation. <bookmark"
            " mark='c'/> Fit the observed entries with a nuclear-norm penalty: a matrix lasso. <bookmark mark='d'/> "
            "Its proximal step is the matrix version of soft thresholding: take the SVD and soft-threshold the "
            "singular values."
        ) as vo:
            intro=label('The nuclear norm relaxes rank on an operator-norm ball',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def softimpute(self):
        rows = [
            cmath(r"W", r"=", r"P_\Omega(M) + P_\Omega^\perp(Z): \ \text{fill the gaps with the current guess}", font_size=28),
            cmath(r"W", r"=", r"U D V^\top", font_size=32),
            cmath(r"Z", r"\leftarrow", r"U (D - \lambda I)_+ V^\top", font_size=32),
            cmath(r"\text{repeat}", r":", r"\text{an EM-like fixed-point iteration, \ warm-started along } \lambda", font_size=28),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"impute"), why(r"decompose"), why(r"shrink"), why(r"Mazumder, \ Hastie \& Tibshirani (2010)")]
        with self.voiceover(
            "<bookmark mark='a'/> Rahul Mazumder, Trevor Hastie and Robert Tibshirani's SoftImpute is almost a one-line "
            "algorithm. Fill the missing entries with the current guess. <bookmark mark='b'/> Take the singular value "
            "decomposition. <bookmark mark='c'/> Soft-threshold the singular values to get the next guess. "
            "<bookmark mark='d'/> Repeat. It is like EM from Part 22, with imputation and shrinkage alternating, and like the "
            "lasso it is computed along a decreasing sequence of lambdas with warm starts."
        ) as vo:
            intro=label('SoftImpute alternates filling missing cells and spectral shrinkage',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def blocks(self):
        d = load("mc")
        T, O, F = (np.asarray(d[k], float) for k in ("truth_block", "obs_block", "fit_block"))
        missing=np.isnan(O)
        O = np.where(missing, -99, O)
        p1 = PhantomPanel(T, size=3.6, caption=r"truth \ (rank 4)", lo=-6, hi=6, tint=LASSO, center=[-4.4, 0.5, 0])
        p2 = PhantomPanel(O, size=3.6, caption=rf"observed: \ {100 * d['frac']:.0f}\%, \ with noise", lo=-6, hi=6, tint=LASSO,
                          center=[0, 0.5, 0])
        # A distinct hatch distinguishes missing cells from observed low intensities.
        corner=p2.image.get_corner(UL);dx=p2.image.width/O.shape[1];dy=p2.image.height/O.shape[0]
        hatch=VGroup()
        for i,j in np.argwhere(missing):
            center=corner+RIGHT*(j+.5)*dx+DOWN*(i+.5)*dy
            hatch.add(Line(center+LEFT*.32*dx+DOWN*.32*dy,
                           center+RIGHT*.32*dx+UP*.32*dy,color=GREY_A,stroke_width=1))
        p2.add(hatch)
        p3 = PhantomPanel(F, size=3.6, caption=rf"SoftImpute, \ $\lambda = {d['best']['lam']:g}$", lo=-6, hi=6, tint=LASSO,
                          center=[4.4, 0.5, 0], caption_color=HIT)
        foot = label(rf"a $24 \times 18$ corner of a ${d['m']} \times {d['k']}$ matrix; \ hatched cells unobserved; display clipped to $[-6,6]$; test error {100 * d['best']['test']:.0f}\%",
                     font_size=22, color=GREY_A).move_to([0, -2.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A simulated example: a hundred and twenty by ninety matrix of rank four, a corner "
            "of which is shown with brightness for the value. <bookmark mark='b'/> We observe thirty percent of the "
            "entries, each with noise; the hatched cells are missing. Brightness uses a common scale, clipped at plus"
            " and minus six. <bookmark mark='c'/> SoftImpute fills them in. The pattern returns, and the relative "
            "error against latent truth on untouched test cells is about twenty-seven percent. Lambda was selected by"
            " noisy validation-cell error, without using test cells or latent truth for tuning."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(p1))
            vo.wait_until("b")
            self.play(FadeIn(p2))
            vo.wait_until("c")
            self.play(FadeIn(p3), FadeIn(foot))
        self.clear_scene()

    def path(self):
        d = load("mc")
        P = d["path"]
        lam = np.array([o["lam"] for o in P])
        te = np.array([o["validation_mse"] for o in P])
        rk = np.array([o["rank"] for o in P])
        A = axes([-0.1, 1.9], [0, max(1.1,float(te.max())*1.08)], x_length=6.6, y_length=4.4, xlabel=r"$\log_{10}\lambda$",
                 ylabel=r"validation-cell mean squared error", xticks=[0, 0.5, 1, 1.5], yticks=[0, 1, 2, 3, 4], center=[-2.6, 0.3, 0])
        ax = A.ax
        x = np.log10(lam)
        l = VGroup(polyline(ax, x, te, LASSO, 3), *[Dot(ax.c2p(a, b), radius=0.07, color=LASSO) for a, b in zip(x, te)])
        rl = VGroup(*[label(rf"{r}", font_size=18, color=SPIKE).next_to(ax.c2p(a, b), UP, buff=0.12) for a, b, r in zip(x, te, rk)])
        rows = fit_rows(VGroup(
            label(r"the path, \ from large $\lambda$ \ (right) \ to small", font_size=22),
            label(r"gold numbers: \ the fitted rank", font_size=22, color=SPIKE),
            label(r"at $\lambda=15$: fitted rank 4, validation MSE 1.58", font_size=22),
            label(rf"validation chooses $\lambda = {d['best']['lam']:g}$; final test untouched", font_size=22, color=HIT),
            label(r"test relative error 27.4\%; fitted rank 23 with small extra singular values", font_size=22, color=HIT),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The SoftImpute path, from a large lambda on the right, where the answer is the zero"
            " matrix, to small. <bookmark mark='b'/> The gold numbers are the rank of each fit. <bookmark mark='c'/> "
            "The fitted rank is four at lambda fifteen, with validation mean squared error about one point five "
            "eight. <bookmark mark='d'/> The smallest validation error is about point five eight at lambda three, "
            "which keeps the four large singular values less shrunk and lets in a few tiny extra ones: the lasso's "
            "bias trade-off, again."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(l), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
        self.clear_scene()

    def singular(self):
        d = load("mc")
        st, sf = np.asarray(d["sv_truth"]), np.asarray(d["sv_fit"])
        hdr = [r"\textbf{singular value}", r"\textbf{1}", r"\textbf{2}", r"\textbf{3}", r"\textbf{4}", r"\textbf{5}", r"\textbf{6}"]
        body = [[r"truth"] + [f"{v:.0f}" for v in st[:6]], [rf"SoftImpute, \ $\lambda = {d['best']['lam']:g}$"] + [f"{v:.0f}" for v in sf[:6]]]
        tb = table_rows([hdr] + body, font_size=26, col_buff=0.7, row_buff=0.35, colors=[GREY_A, SPIKE, LASSO])
        tb.move_to([0, 0.9, 0])
        foot = fit_rows(VGroup(
            label(r"the top four are recovered, \ each shrunk by 15--20\%", font_size=22, color=LASSO),
            label(r"four dominant singular values; fitted rank 23, including many smaller ones", font_size=22),
            label(r"refit or reweight, \ as in chapter six, \ to remove the shrinkage", font_size=22, color=GREY_A),
        ), 12.0, 0.22, [0, -1.9, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The singular values tell the story. The four true ones are recovered, each shrunk "
            "by fifteen to twenty percent. <bookmark mark='b'/> The extra ones are an order of magnitude smaller, so "
            "the fit is nearly rank four. <bookmark mark='c'/> And as with the lasso, refitting or reweighting can "
            "reduce shrinkage at a possible variance cost, the matrix versions of chapter six's remedies."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb), FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def theory(self):
        rows = [
            cmath(r"|\Omega|", r"\ge", r"C\, \mu\, r\, (m + k) \log^2(m + k)", font_size=32),
            cmath(r"\mu", r":", r"\text{incoherence: \ singular vectors not concentrated on a few rows}", font_size=28),
            cmath(r"\Rightarrow", r"", r"\text{nuclear-norm minimization recovers } M \text{ exactly, \ w.h.p.}", font_size=30),
            cmath(r"\text{a spiky matrix}", r":", r"\text{one entry matters: \ no hope}", font_size=30),
        ]
        rows[2][-1].set_color(LASSO)
        whys = [why(r"Cand\`es \& Recht (2009); \ Cand\`es \& Tao (2010); \ Recht (2011)"), why(r"the analogue of RIP"),
                why(r"exact, \ without noise"), why(r"incoherence is necessary")]
        with self.voiceover(
            "<bookmark mark='a'/> The theory mirrors chapter nine. Emmanuel Candès and Benjamin Recht proved in 2009 "
            "that if the number of observed entries is a constant times the rank times the dimensions, up to "
            "logarithms, <bookmark mark='b'/> entries are sampled uniformly at random, and the matrix satisfies the "
            "theorem's incoherence conditions, with singular vectors spread over rows and columns, <bookmark "
            "mark='c'/> then nuclear-norm minimization recovers the matrix exactly with high probability. <bookmark "
            "mark='d'/> For uniform recovery from few randomly sampled entries, concentration can obstruct recovery: "
            "a matrix that is zero except for one entry cannot be recovered unless that entry is observed. Part 52 "
            "returns to low-rank recovery with noise."
        ) as vo:
            intro=label('Exact matrix completion requires sampling and incoherence conditions',font_size=36).move_to([0,3.3,0])
            if intro.width>12.5:intro.width=12.5
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
