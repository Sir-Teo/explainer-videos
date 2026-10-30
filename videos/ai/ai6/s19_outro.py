from __future__ import annotations

import math

import numpy as np

from explainer import narration_credit
from explainer.ai import *  # noqa: F403
from videos.ai.ai6.common import AUSTEN, DICKENS, PART, author_color, load, mix


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.problems()
        self.next_time()
        self.references()

    # ------------------------------------------------------------------
    def tiles(self):
        """The part in twelve pictures, each drawn from its own computed result."""
        TW, TH = 2.05, 1.75
        mk = lambda xr, yr: Axes(x_range=xr, y_range=yr, x_length=TW * 0.9, y_length=TH * 0.85, tips=False,  # noqa: E731
                                 axis_config={"stroke_color": GREY_D, "include_ticks": False})
        out = []
        z = load("zipf")
        ax = mk([0, 3, 1], [1, 6, 1])
        b = np.asarray(z["beta"])
        out.append((VGroup(ax, *[Dot(ax.c2p(math.log10(r), math.log10(f)), radius=0.012, color=C.TRUE_P)
                                 for r, f in zip(np.asarray(z["r"])[::8], np.asarray(z["f"])[::8])],
                           Line(ax.c2p(0, b[0]), ax.c2p(3, b[0] + 3 * b[1]), color=C.MODEL_Q, stroke_width=2.5)),
                    r"least squares: \ Zipf", C.MODEL_Q))
        gm = load("gaussmarkov")
        bins = np.asarray(gm["hist_bins"])
        ho, he = np.asarray(gm["hist_ols"]), np.asarray(gm["hist_end"])
        ax = mk([bins[0], bins[-1], 0.1], [0, float(ho.max()) * 1.05, 1])
        hb = VGroup(ax)
        for h, col in ((he, "#B48EF0"), (ho, C.MODEL_Q)):
            for a_, b_, c_ in zip(bins[:-1], bins[1:], h):
                if c_ > 0:
                    p0, p1 = ax.c2p(a_, 0), ax.c2p(b_, c_)
                    hb.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=col,
                                     fill_opacity=0.6).move_to((p0 + p1) / 2))
        out.append((hb, r"Gauss--Markov", C.MODEL_Q))
        rd = load("ridge")
        d = np.asarray(rd["d"])
        ax = mk([0, len(d) + 1, 1], [0, 1, 1])
        out.append((VGroup(ax, *[curve(ax, np.arange(1, len(d) + 1), d ** 2 / (d ** 2 + l_), "#7FD3FF", 2.5)
                                 for l_ in (30.0, 300.0, 3000.0)]), r"ridge shrinks", "#7FD3FF"))
        la = load("lasso")
        path = np.asarray(la["path"])
        top = float(np.abs(path).max())
        ax = mk([0, len(path) - 1, 1], [-top, top, 1])
        out.append((VGroup(ax, *[curve(ax, np.arange(len(path)), path[:, j], C.BITS if j in np.argsort(-np.abs(path[-1]))[:6]
                                       else GREY_D, 1.5) for j in range(path.shape[1]) if np.any(path[:, j])]),
                    r"the lasso path", C.BITS))
        ir = load("irls")
        ax = mk([0, 4.3, 1], [-16, 0, 1])
        gd = np.asarray(ir["gd"])
        out.append((VGroup(ax, curve(ax, [math.log10(max(i, 1)) for i in range(1, len(ir["newton_gap"]))],
                                     [math.log10(max(v, 1e-16)) for v in ir["newton_gap"][1:]], C.REWARD, 2.5),
                           curve(ax, [math.log10(a_) for a_, v in gd if a_ >= 1 and v > 1e-16],
                                 [math.log10(v) for a_, v in gd if a_ >= 1 and v > 1e-16], C.MODEL_Q, 2.5)),
                    r"Newton vs.\ gradient", C.REWARD))
        nb = load("nbvslr")
        sz = [int(m) for m in nb["sizes"]]
        ax = mk([math.log10(sz[0]), math.log10(sz[-1]), 1], [0, 0.3, 1])
        out.append((VGroup(ax, *[curve(ax, np.log10(sz), [nb[k][str(m)]["mean"] for m in sz], c_, 2.5)
                                 for k, c_ in (("nb", "#4FD1C5"), ("lr", C.MODEL_Q))]), r"Bayes vs.\ logistic",
                    "#4FD1C5"))
        ch = load("coverhart")
        ns = [int(n) for n in ch["ns"]]
        ax = mk([1, 4, 1], [0.15, 0.4, 1])
        out.append((VGroup(ax, curve(ax, np.log10(ns), [ch["e1"][str(n)]["mean"] for n in ns], C.MODEL_Q, 2.5),
                           *[DashedLine(ax.c2p(1, v), ax.c2p(4, v), color=c_, stroke_width=1.5)
                             for v, c_ in ((ch["Rstar"], C.TRUE_P), (ch["bound"], C.PENALTY))]), r"Cover--Hart", C.MODEL_Q))
        ke = load("kernel")
        ev, es = np.asarray(ke["ev2"]), np.asarray(ke["ev_sig"])
        ax = mk([0, len(ev), 1], [float(es.min()), float(ev.max()), 1])
        out.append((VGroup(ax, curve(ax, np.arange(len(ev)), ev, C.REWARD, 2.5), curve(ax, np.arange(len(es)), es, C.PENALTY, 2)),
                    r"Mercer's test", C.REWARD))
        sv = load("svm")
        reg = np.asarray(sv["region_C1"]) > 0
        im = (np.stack([np.where(reg, 0x58, 0xE8), np.where(reg, 0xA6, 0x6F), np.where(reg, 0xFF, 0x8A),
                        np.full(reg.shape, 255)], -1)[::-1] * 0.45).astype(np.uint8)
        im[..., 3] = 255
        img = ImageMobject(im)
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img.stretch_to_fit_width(TW * 0.9).stretch_to_fit_height(TH * 0.85)
        out.append((Group(img), r"SVM, \ Gaussian kernel", C.BITS))
        bg = load("bagging")
        Bm = np.log10(np.asarray(bg["Bm"], float))
        topv = max(max(bg[k]["meas"]) for k in ("mf70", "mf8"))
        ax = mk([0, Bm[-1], 1], [0, topv, 1])
        out.append((VGroup(ax, *[curve(ax, Bm, bg[k]["meas"], c_, 2.5) for k, c_ in (("mf70", C.PENALTY), ("mf8", C.INTERVAL))]),
                    r"$\rho\sigma^2 + (1-\rho)\sigma^2/B$", C.INTERVAL))
        ab = load("adaboost")
        L = np.asarray(ab["exp_loss_70"])
        ax = mk([0, math.log10(len(L)), 1], [-4, 0, 1])
        out.append((VGroup(ax, curve(ax, np.log10(np.arange(1, len(L) + 1)), np.maximum(np.log10(np.maximum(L, 1e-12)), -4),
                                     "#B48EF0", 2.5)), r"exponential loss", "#B48EF0"))
        me = load("metrics")
        rc = np.asarray(me["roc_lr2"])
        ax = mk([0, 1, 1], [0, 1, 1])
        out.append((VGroup(ax, DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=GREY_D, stroke_width=1),
                           VMobject(color=C.MODEL_Q, stroke_width=2.5).set_points_as_corners([ax.c2p(a_, b_) for a_, b_ in rc])),
                    rf"ROC, \ area ${me['lr2']['auc']:.2f}$", C.MODEL_Q))
        tiles = Group()
        for pic, cap, col in out:
            box, c_ = tile_frame(cap, col, TW, TH)
            if c_.width > TW + 0.1:
                c_.width = TW + 0.1
            pic.move_to(box.get_center() + UP * 0.22)
            if pic.width > TW:
                pic.width = TW
            if pic.height > TH:
                pic.height = TH
            tiles.add(Group(box, pic, c_))
        tiles.arrange_in_grid(rows=2, cols=6, buff=(0.12, 0.3)).move_to(DOWN * 0.3)
        if tiles.width > 13.7:
            tiles.width = 13.7
        return tiles

    def recap(self):
        tiles = self.tiles()
        head = label(rf"Part {PART}, in twelve pictures", font_size=40).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Let's take stock. Least squares is a projection, and among linear unbiased estimates the best. Ridge "
            "shrinks the weak directions; the lasso's soft thresholds choose words. Logistic regression is a convex "
            "bowl, and Newton's method finds its bottom in a few steps. Naive Bayes learns fast but stays wrong, and "
            "overconfident. A single neighbour errs at most twice as often as the best rule, but neighbours drown in "
            "many dimensions. Kernels lift without lifting, and the support vector machine's dual needs only them. "
            "Averaging trees cuts variance down to a floor set by their correlation; boosting walks down the "
            "exponential loss, and XGBoost takes Newton steps. And an honest score needs the right curve and "
            "untouched test pages."
        ) as vo:
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t_, shift=UP * 0.15, scale=0.95) for t_ in tiles], lag_ratio=0.85),
                      run_time=max(4.0, vo.duration - 2.0))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        card = payoff_card([
            (r"cross-entropy, \ gradients \ and curvature", [9, 11]),
            (r"logistic regression for many classes: \ the softmax", [9, 13]),
            (r"PCA, \ mixtures and EM, \ Bayesian models", [7]),
            (r"penalties, \ validation, \ double descent", [8]),
            (r"kernels: \ the neural tangent kernel; \ attention as a kernel smoother", [8, 13]),
            (r"calibration and honest evaluation", [31]),
        ], font_size=24)
        with self.voiceover(
            "All of it comes back. Cross-entropy, gradients and curvature are how every network in Parts 9 and 11 "
            "is trained, and the softmax is logistic regression with many classes. Part 7 builds the statistical "
            "models: principal components, mixtures, Bayes. Part 8 asks why a model generalizes at all, and meets "
            "the neural tangent kernel, a network that behaves like a kernel machine. Part 13 reads attention as a "
            "kernel smoother, and Part 31 asks the same question of language models that we asked of naive Bayes: "
            "are its probabilities honest?"
        ) as vo:
            self.play(FadeIn(card.head))
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.1) for r_ in card.rows], lag_ratio=0.4),
                      run_time=max(3.0, vo.duration - 1.5))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"For $y_i = \beta_0 + \beta_1 x_i + \varepsilon_i$, \ show that the slope through the two end points is "
            r"unbiased with variance $2\sigma^2/(x_n - x_1)^2$, \ and that least squares' is $\sigma^2/\sum_i (x_i - \bar x)^2$; "
            r"\ which is smaller?",
            r"Show that ridge's fit is $\sum_j \mathbf{u}_j \frac{d_j^2}{d_j^2 + \lambda}\mathbf{u}_j^{\top}\mathbf{y}$, "
            r"\ and that its effective number of weights, \ $\operatorname{tr}\,Z(Z^{\top}Z + \lambda I)^{-1}Z^{\top}$, "
            r"\ is $\sum_j d_j^2/(d_j^2 + \lambda)$.",
            r"Derive the soft threshold from subgradients, \ and show that the lasso's weights are all zero exactly when "
            r"$\lambda \ge \max_j |\mathbf{z}_j^{\top}\mathbf{y}|/n$.",
            r"Show that the logistic loss's Hessian $X^{\top}SX/n$ is positive semidefinite, \ and that if a line "
            r"separates the training data, \ no finite weights minimize the loss.",
            r"Show that the Gram matrix of $K(\mathbf{x}, \mathbf{z}) = (\mathbf{x}\cdot\mathbf{z} + 1)^2$ is positive "
            r"semidefinite, \ and find a Gram matrix of $\tanh(\mathbf{x}\cdot\mathbf{z} - 1)$ with a negative eigenvalue.",
            r"Derive the dual of the soft-margin SVM, \ and use complementary slackness to show that $\alpha_i = C$ for "
            r"every training point strictly inside the street.",
            r"Derive $\operatorname{Var}\big(\frac1B\sum_b T_b\big) = \rho\sigma^2 + (1 - \rho)\sigma^2/B$, \ and AdaBoost's "
            r"$\alpha = \tfrac12\log\frac{1-\varepsilon}{\varepsilon}$ from the exponential loss.",
            r"For the logistic loss, \ derive XGBoost's leaf weight $-G/(H + \lambda)$ and split gain, \ and show that a "
            r"single leaf at $p = \tfrac12$ moves the log-odds by $-4G/(n + 4\lambda)$.",
        ], font_size=21)
        with self.voiceover(
            "Here are eight problems to try, from Gauss-Markov to XGBoost's gain. Pause here, and work through them; "
            "full solutions are in this part's notes."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows], lag_ratio=0.3),
                      run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_time(self):
        p = load("pages")
        X2, y = np.asarray(p["X2"]), np.asarray(p["y"])
        Z = (X2 - X2.mean(0)) / X2.std(0)
        Zj = Z + np.random.default_rng(6).uniform(-0.06, 0.06, Z.shape)  # the rates are whole numbers: a little jitter
        vals, vecs = np.linalg.eigh(np.cov(Z.T))
        head = label(r"Next: \ Part 7, \ Statistical ML", font_size=40).to_edge(UP, buff=0.35)
        U = 1.0
        dots = VGroup(*[Dot([U * z[0], U * z[1] - 0.4, 0], radius=0.035, color=author_color(int(l_)), fill_opacity=0.7)
                        for z, l_ in zip(Zj, y) if abs(z[0]) < 3.3 and abs(z[1]) < 2.9])
        arrows = VGroup(*[Arrow([0, -0.4, 0], [1.8 * math.sqrt(v) * e[0], 1.8 * math.sqrt(v) * e[1] - 0.4, 0], buff=0,
                                color=C.BITS if k == 1 else GREY_A, stroke_width=6) for k, (v, e) in enumerate(zip(vals, vecs.T))])
        tag = note(r"the pages, \ no labels used: \ the directions they spread along").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Next time: statistical machine learning. Every method in this part was told who wrote each training "
            "page. <bookmark mark='a'/> Part 7 takes the labels away and asks what structure is there anyway: the "
            "directions the pages spread along, the clusters they fall into, and the hidden causes behind them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dots), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(*[d.animate.set_color(GREY_B) for d in dots], run_time=1.0)
            self.play(GrowArrow(arrows[1]), GrowArrow(arrows[0]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def references(self):
        card = reference_card(
            [r"T.~Hastie, R.~Tibshirani \& J.~Friedman, \textit{The Elements of Statistical Learning}, 2nd ed.\ (2009); "
             r"\ C.~M.~Bishop, \textit{Pattern Recognition and Machine Learning} (2006)",
             r"K.~P.~Murphy, \textit{Probabilistic Machine Learning: An Introduction} (2022); \ B.~Sch\"olkopf \& A.~Smola, "
             r"\textit{Learning with Kernels} (2002)"],
            [r"Legendre (1805); \ Gauss (1809, 1821); \ Markov (1900); \ Moore (1920); \ Penrose (1955); \ Theil (1950); "
             r"\ Sen (1968); \ Hoerl \& Kennard (1970); \ Tibshirani (1996); \ Zou \& Hastie (2005); \ Friedman, Hastie \& "
             r"Tibshirani, \textit{glmnet} (2010)",
             r"Berkson (1944); \ Nelder \& Wedderburn (1972); \ Platt (1999); \ Ng \& Jordan (2002); \ Fisher (1936); \ "
             r"Mosteller \& Wallace (1963, 1964)",
             r"Fix \& Hodges (1951); \ Cover \& Hart (1967); \ Bellman (1957); \ Rosenblatt (1958); \ Novikoff (1962); \ "
             r"Minsky \& Papert (1969); \ Mercer (1909); \ Aizerman, Braverman \& Rozonoer (1964); \ Kimeldorf \& Wahba "
             r"(1971); \ Boser, Guyon \& Vapnik (1992); \ Cortes \& Vapnik (1995); \ Platt, \textit{SMO} (1998); \ "
             r"Sch\"olkopf, Herbrich \& Smola (2001)",
             r"Breiman, Friedman, Olshen \& Stone, \textit{CART} (1984); \ Quinlan (1986); \ Breiman (1996, 2001a, 2001b); "
             r"\ Ho (1995); \ Freund \& Schapire (1997); \ Schapire et al.\ (1998); \ Friedman, Hastie \& Tibshirani (2000); "
             r"\ Friedman (2001); \ Viola \& Jones (2001); \ Chen \& Guestrin, \textit{XGBoost} (2016)",
             r"Soudry et al.\ (2018); \ Grinsztajn, Oyallon \& Varoquaux (2022); \ Hollmann et al., \textit{TabPFN} "
             r"(\textit{Nature}, 2025); \ Prior Labs, \textit{TabPFN-2.5} (2025), \textit{TabPFN-3} (2026); \ Purucker et "
             r"al., \textit{Beyond IID} (2026)"])
        credit = note(narration_credit(), font_size=18).to_edge(DOWN, buff=0.15)
        if card.get_bottom()[1] < credit.get_top()[1] + 0.1:
            card.shift(UP * (credit.get_top()[1] + 0.1 - card.get_bottom()[1]))
        with self.voiceover(
            "For more, The Elements of Statistical Learning by Hastie, Tibshirani and Friedman covers every method "
            "here, by three of the people who built them; Bishop's Pattern Recognition and Machine Learning gives "
            "the probabilistic view; and Schölkopf and Smola's Learning with Kernels the kernels. Thanks for "
            "watching, and see you in Part 7."
        ):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(1.5)
        self.clear_scene()
