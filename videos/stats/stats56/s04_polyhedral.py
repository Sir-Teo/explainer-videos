from __future__ import annotations

import numpy as np

from videos.stats.stats56.common import *  # noqa: F403


class Polyhedral(VoiceoverScene):
    def construct(self):
        self.card()
        self.lemma()
        self.proof()
        self.pivot()
        self.screening()
        self.window()
        self.lasso_event()
        self.prostate()
        self.board()
        self.costs()
        self.asymptotic()

    def card(self):
        card = chapter_card(3, r"Conditional selective inference", r"The polyhedral lemma, \ proved", lit=(2016,), part=PART)
        with self.voiceover("Chapter three. Conditional selective inference, and the polyhedral lemma, proved."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def lemma(self):
        rows = [
            cmath(r"Y \sim N(\mu, \Sigma)", r",", r"\text{a selection event } \{AY \le b\}, \ \text{a target } \eta'\mu", font_size=34),
            cmath(r"c = \frac{\Sigma\eta}{\eta'\Sigma\eta}", r",", r"Z = Y - c\,\eta'Y: \ \text{independent of } \eta'Y", font_size=34),
            cmath(r"\{AY \le b\}", r"=", r"\{\mathcal V^-(Z) \le \eta'Y \le \mathcal V^+(Z)\}", font_size=36),
            cmath(r"\eta'Y \mid \{AY \le b\}, Z", r"\sim", r"N(\eta'\mu, \eta'\Sigma\eta) \text{ truncated to } [\mathcal V^-, \mathcal V^+]", font_size=32),
        ]
        rows[2][-1].set_color(SELC)
        rows[3][-1].set_color(CONDC)
        whys = [why(r"Lee, \ Sun, \ Sun \& Taylor (2016)"), why(r"Gaussian: \ uncorrelated is independent"), why(r"the lemma"), why(r"one dimension, \ exactly")]
        with self.voiceover(
            "<bookmark mark='a'/> The key result is due to Jason Lee, Dennis Sun, Yuekai Sun and Jonathan Taylor. Let Y be "
            "Gaussian, let the selection event be a polyhedron, A Y at most b, and let the target be a linear function, eta "
            "transpose mu. <bookmark mark='b'/> Split Y into its component along eta, and a remainder Z that is "
            "uncorrelated with it, hence independent. <bookmark mark='c'/> The lemma says the polyhedron, seen along that "
            "line, is an interval: the selection event equals V minus of Z at most eta transpose Y at most V plus of Z. "
            "<bookmark mark='d'/> So, given selection and Z, the statistic is a normal truncated to that interval: a "
            "one-dimensional law, known exactly."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"Y", r"=", r"c\,(\eta'Y) + Z", font_size=38),
            cmath(r"AY \le b", r"\iff", r"(Ac)_k\,\eta'Y \le b_k - (AZ)_k \ \text{ for every row } k", font_size=34),
            cmath(r"(Ac)_k > 0", r":", r"\eta'Y \le \frac{b_k - (AZ)_k}{(Ac)_k}; \ \ (Ac)_k < 0: \ \eta'Y \ge \frac{b_k - (AZ)_k}{(Ac)_k}", font_size=32),
            cmath(r"\mathcal V^+ = \min_{(Ac)_k > 0}(\cdot), \ \ \mathcal V^- = \max_{(Ac)_k < 0}(\cdot)", r":", r"\text{functions of } Z \text{ alone} \qquad \blacksquare", font_size=32),
        ]
        rows[3][-1].set_color(PROOFC)
        whys = [why(r"the decomposition"), why(r"substitute"), why(r"divide by the sign of $(Ac)_k$"), why(r"rows with $(Ac)_k = 0$ only constrain $Z$")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof is four lines. Write Y as c times eta transpose Y, plus Z. <bookmark mark='b'/> "
            "Substitute into the constraints: each row k says that A c, its k-th entry, times the statistic is at most b k "
            "minus the k-th entry of A Z. <bookmark mark='c'/> Where that coefficient is positive, the row is an upper bound "
            "on the statistic; where it is negative, dividing flips the inequality, and it is a lower bound. <bookmark "
            "mark='d'/> The tightest upper bound is V plus, the tightest lower bound V minus, and both depend on Z alone. "
            "Rows where the coefficient is zero constrain only Z, which we condition on anyway."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pivot(self):
        rows = [
            cmath(r"F_{\theta}^{[\mathcal V^-, \mathcal V^+]}(\eta'Y)", r"\sim", r"U(0, 1) \ \text{ given selection, \ at } \theta = \eta'\mu", font_size=34),
            cmath(r"\text{test}", r":", r"H_0: \eta'\mu = \theta_0 \text{ with the truncated pivot}", font_size=34),
            cmath(r"\text{interval}", r":", r"\{\theta: \ \tfrac\alpha2 \le F_\theta(\eta'Y) \le 1 - \tfrac\alpha2\}, \ \ F \text{ monotone in } \theta", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"P\big(\eta'\mu \in C \mid \text{selection}\big) = 1 - \alpha", font_size=36),
        ]
        rows[3][-1].set_color(CONDC)
        whys = [why(r"the probability integral transform"), why(r"exact, \ conditional"), why(r"invert the test"), why(r"conditional coverage")]
        with self.voiceover(
            "<bookmark mark='a'/> Then the truncated normal's distribution function, evaluated at the statistic, is uniform "
            "given selection: the probability integral transform. <bookmark mark='b'/> That gives an exact test of any "
            "value of the target, <bookmark mark='c'/> and inverting the test, which is monotone in theta, gives an interval, "
            "<bookmark mark='d'/> with exact conditional coverage: given that this question was selected, the interval "
            "covers its answer with probability one minus alpha."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def screening(self):
        rows = [
            cmath(r"\text{marginal screening}", r":", r"\text{select } j \text{ if } |Y_j| > t", font_size=36),
            cmath(r"\{|Y_j| > t\}", r"=", r"\{Y_j > t\} \cup \{Y_j < -t\}: \ \text{a union of two polyhedra}", font_size=34),
            cmath(r"\text{given } j \text{ selected}", r":", r"Y_j \sim N(\mu_j, 1) \text{ truncated to } (-\infty, -t) \cup (t, \infty)", font_size=32),
            cmath(r"\text{the lesson}", r":", r"\text{the lemma extends to unions: \ sum the truncated masses}", font_size=34),
        ]
        rows[2][-1].set_color(CONDC)
        whys = [why(r"the simplest selection"), why(r"one polyhedron per sign"), why(r"two pieces"), why(r"condition on less")]
        with self.voiceover(
            "<bookmark mark='a'/> The simplest example is marginal screening: report coordinate j if its absolute "
            "value exceeds a threshold t. <bookmark mark='b'/> That event is a union of two polyhedra, one for each "
            "sign. <bookmark mark='c'/> Given selection, Y j is a normal truncated to the two outer pieces of the "
            "line. <bookmark mark='d'/> The lemma extends to unions by summing the truncated masses over the pieces, "
            "and that is exactly how one conditions on less: on the selected set without its signs."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def window(self):
        A = axes([-2, 5], [0, 1.6], x_length=7.4, y_length=4.0, xlabel=r"$\eta'Y$", ylabel=r"density",
                 xticks=[-2, 0, 2, 4], yticks=[0, 0.5, 1, 1.5], center=[-2.5, 0.0, 0])
        ax = A.ax
        sw = SelectionWindow(ax, a=1.0, b=3.0, y=2.6, x_range=(-2, 5), trunc_color=CONDC, obs_color=SELC, region_color=SELC)
        mus = [0.0, 1.0, 2.2, 3.5]
        pics = [sw.at(m) for m in mus]
        lab = [label(rf"$\theta = {m:g}$: \ pivot $= {sw.pivot(m):.3f}$", font_size=22, color=CONDC) for m in mus]
        side = fit_rows(VGroup(
            label(r"truncation $[\mathcal V^-, \mathcal V^+] = [1, 3]$, \ observed 2.6", font_size=22, color=SELC),
            *lab,
            label(r"the interval: \ every $\theta$ with pivot in $[0.025, 0.975]$", font_size=22, color=GREY_A),
        ), 4.6, 0.38, [4.45, 0.2, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The selection window shows the inversion. The statistic was observed at two point six, "
            f"and the selection event confines it to between one and three. <bookmark mark='b'/> With theta zero, the "
            f"truncated law piles up at the left end, and the chance of exceeding two point six is only "
            f"{say(sw.pivot(0.0), 3)}. <bookmark mark='c'/> At theta one it is {say(sw.pivot(1.0), 3)}; <bookmark mark='d'/> "
            f"at two point two, {say(sw.pivot(2.2), 3)}; <bookmark mark='e'/> at three and a half, {say(sw.pivot(3.5), 3)}. "
            f"<bookmark mark='f'/> The interval collects every theta whose pivot lies between two and a half and ninety-seven "
            f"and a half percent."
        ) as vo:
            self.play(FadeIn(A), FadeIn(sw.region), FadeIn(sw.obs), FadeIn(exact_tag(r"exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            cur = None
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                if cur is None:
                    self.play(Create(pics[k][0]), Create(pics[k][1]), FadeIn(pics[k][2]), FadeIn(side[k + 1]))
                else:
                    self.play(Transform(cur, pics[k]), FadeIn(side[k + 1]))
                cur = pics[k] if cur is None else cur
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def lasso_event(self):
        rows = [
            cmath(r"\hat\beta", r"=", r"\arg\min \tfrac12\|y - X\beta\|^2 + \lambda\|\beta\|_1: \ \text{active set } E, \ \text{signs } s", font_size=32),
            cmath(r"\text{KKT}", r":", r"X_E'(y - X_E\hat\beta_E) = \lambda s, \ \ \|X_{-E}'(y - X_E\hat\beta_E)\|_\infty < \lambda", font_size=32),
            cmath(r"\{(\hat E, \hat s) = (E, s)\}", r"=", r"\{A_0 y \le b_0\} \cap \{A_1 y \le b_1\}: \ \text{a polyhedron}", font_size=32),
            cmath(r"\eta_j", r"=", r"(X_E^+)'e_j: \ \ \eta_j'\mu = \beta_{j\cdot E}, \ \text{the submodel coefficient}", font_size=34),
        ]
        rows[2][-1].set_color(SELC)
        rows[3][-1].set_color(CONDC)
        whys = [why(r"Part 32's lasso, \ this scaling"), why(r"the optimality conditions"), why(r"inactive: \ $A_0$; \ signs: \ $A_1$"), why(r"PoSI's target")]
        with self.voiceover(
            "<bookmark mark='a'/> The lemma's first application was the lasso. At a fixed lambda, the lasso picks an active "
            "set E with signs s. <bookmark mark='b'/> Its optimality conditions say that on E the correlations with the "
            "residual equal lambda times the signs, and off E they are smaller than lambda. <bookmark mark='c'/> Lee and "
            "colleagues wrote the event that the lasso picks exactly E with signs s as the intersection of two sets of linear "
            "inequalities in y: a polyhedron. <bookmark mark='d'/> Take eta to be the row of the pseudo-inverse of X E that "
            "gives coefficient j, so the target is PoSI's submodel coefficient, and the lemma gives exact selective "
            "intervals for every variable the lasso kept."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def prostate(self):
        d = load("lasso")
        f = d["fits"][0]
        hdr = [r"variable", r"estimate", r"naive 95\%", r"selective 95\%", r"truncation"]
        body = [[iv["name"], f"{iv['est']:.3f}", f"({iv['naive'][0]:.2f}, {iv['naive'][1]:.2f})", f"({iv['lo']:.2f}, {iv['hi']:.2f})",
                 f"[{iv['trunc'][0]:.2f}, {iv['trunc'][1]:.2f}]"] for iv in f["intervals"]]
        tab = table_rows([hdr] + body, font_size=24, col_buff=0.55, row_buff=0.25, colors=[GREY_B] + [WHITE] * len(body)).move_to([0, 0.4, 0])
        foot = fit_rows(VGroup(
            label(rf"Stamey's prostate data, \ $n = {d['n']}$, \ 8 standardized predictors, \ $\sigma = {d['sigma']:.3f}$ from the full fit", font_size=22, color=GREY_A),
            label(rf"the lasso at $\lambda = {f['lam']:.0f}$ keeps {', '.join(f['E'])}", font_size=24, color=SELC),
            label(r"lcavol is far inside its window: \ the intervals agree", font_size=24, color=CONDC),
            label(r"lweight and svi are near their windows' edges: \ the selective intervals stretch down", font_size=24, color=NAIVEC),
        ), 12.4, 0.25, [0, -2.2, 0])
        lw = f["intervals"][1]
        with self.voiceover(
            f"<bookmark mark='a'/> Stamey's prostate cancer data, ninety-seven men and eight standardized predictors of the "
            f"log PSA, with sigma taken from the full least-squares fit. <bookmark mark='b'/> The lasso at lambda twenty keeps "
            f"three: the log cancer volume, the log prostate weight, and seminal vesicle invasion. <bookmark mark='c'/> For "
            f"the log cancer volume, the statistic sits far inside its truncation window, and the selective interval agrees "
            f"with the naive one. <bookmark mark='d'/> For the log weight, the estimate {say(lw['est'], 3)} is close to its "
            f"window's lower edge, {say(lw['trunc'][0], 2)}: it was selected partly because it was large, and the selective "
            f"interval stretches down to {say(lw['lo'], 2)}, against the naive {say(lw['naive'][0], 2)}. The same happens "
            f"for seminal vesicle invasion."
        ) as vo:
            self.play(FadeIn(tab[0]), FadeIn(museum_tag(r"Stamey et al. (1989)")))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r) for r in tab[1:]], lag_ratio=0.3), FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(Indicate(tab[1], color=CONDC), FadeIn(foot[2]))
            vo.wait_until("d")
            self.play(Indicate(tab[2], color=NAIVEC), Indicate(tab[3], color=NAIVEC), FadeIn(foot[3]))
        self.clear_scene()

    def board(self):
        s = load("lasso")["sim"]
        show_board(self, board_rows("lasso", "polyhedral"),
                   f"<bookmark mark='a'/> The Board, with Stamey's design, a truth in which only the log cancer volume "
                   f"matters, and the lasso at lambda twelve, which lets noise variables in: {s['count']:,} selected "
                   f"coefficients over eight hundred data sets. The "
                   f"ordinary least-squares intervals after the lasso cover {100 * s['naive']:.1f} percent of them. <bookmark "
                   f"mark='b'/> The selective intervals cover {100 * s['selective']:.1f} percent: kept, at the cost of a median "
                   f"length {s['len_s'] / s['len_n']:.1f} times the naive one.", [("a", [0]), ("b", [1])])

    def asymptotic(self):
        rows = [
            cmath(r"\text{non-Gaussian errors}", r":", r"\text{the lemma needs exact normality of } \eta'Y", font_size=34),
            cmath(r"\text{asymptotically}", r":", r"\text{valid uniformly, \ under conditions}", font_size=32),
            cmath(r"\text{when it fails}", r":", r"\text{the edge amplifies departures}", font_size=34),
            cmath(r"\text{so}", r":", r"\text{randomize (chapter 4), \ or check the edge distance}", font_size=34),
        ]
        rows[1][-1].set_color(CONDC)
        rows[2][-1].set_color(NAIVEC)
        whys = [why(r"heavy tails, \ skewness"), why(r"Tibshirani, \ Rinaldo, \ Tibshirani \& Wasserman (2018)"), why(r"tails matter after truncation"), why(r"practical advice")]
        with self.voiceover(
            "<bookmark mark='a'/> What if the errors are not Gaussian? The lemma needs the statistic to be exactly "
            "normal. <bookmark mark='b'/> Ryan Tibshirani, Alessandro Rinaldo, Robert Tibshirani and Larry Wasserman "
            "showed that selective intervals remain asymptotically valid, uniformly over a class of error "
            "distributions, under conditions on the selection. <bookmark mark='c'/> The weak point is the edge: when "
            "the statistic sits near a truncation point, the truncated law is determined by the far tail of the error "
            "distribution, where the normal approximation is worst. <bookmark mark='d'/> So randomize, as in the next "
            "chapter, or at least report how close each statistic is to the edge of its window."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def costs(self):
        rows = [
            cmath(r"\text{near an edge}", r":", r"E\,|C| = \infty \ \ (\text{Kivaranovic \& Leeb 2021})", font_size=30),
            cmath(r"\text{condition on less}", r":", r"\text{on } E \text{ only, \ a union of } 2^{|E|} \text{ polyhedra: \ shorter}", font_size=32),
            cmath(r"\text{optimal}", r":", r"\text{condition on selection and the nuisance only}", font_size=32),
            cmath(r"\text{so}", r":", r"\text{conditioning discards what selected}", font_size=32),
        ]
        rows[0][-1].set_color(NAIVEC)
        rows[2][-1].set_color(CONDC)
        whys = [why(r"truncated normals' tails"), why(r"drop the signs"), why(r"Fithian, \ Sun \& Taylor (2014)"), why(r"the next chapter's fix")]
        with self.voiceover(
            "<bookmark mark='a'/> Two costs. When the statistic is near an edge of its window, the selective interval can be "
            "very long; Danijel Kivaranovic and Hannes Leeb proved its expected length is infinite. <bookmark mark='b'/> "
            "Conditioning on less helps: conditioning only on the active set, not the signs, means a union of polyhedra and "
            "shorter intervals. <bookmark mark='c'/> Fithian, Sun and Taylor showed the optimal recipe: condition on the "
            "selection event and the sufficient statistics for the nuisance parameters, and nothing else, as in Part "
            "forty-six's Neyman structure. <bookmark mark='d'/> The deeper cost is that conditioning throws away the "
            "information that was used to select. The next chapter keeps some of it."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
