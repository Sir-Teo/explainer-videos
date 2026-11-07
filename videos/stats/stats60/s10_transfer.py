from __future__ import annotations

import numpy as np

from videos.stats.stats60.common import *  # noqa: F403


class Transfer(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter nine. Transfer learning: borrowing from a related problem, and knowing when not to.", 9,
                            r"Transfer learning", r"How much is the source worth?", lit=(2010,))
        self.bound()
        self.exponent()
        self.translasso()
        self.chart()
        self.negative()
        self.domain()

    def bound(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Transfer learning combines source data with a smaller target sample. <bookmark mark='b'/> A classic binary-classification bound relates target risk to source risk. <bookmark mark='c'/> It adds one half of the hypothesis-disagreement divergence between covariate distributions. <bookmark mark='d'/> It also adds the minimum combined source and target error within the hypothesis class. A large joint error makes this bound uninformative; it does not prove that no source information can help any procedure.",
            [(r"\text{setting}", r":", r"n_S \text{ source points}, \ n_T \ll n_S \text{ target points}", 40),
             (r"R_T(h)", r"\le", r"R_S(h)", 40),
             (r"\text{the shift}", r"+", r"\tfrac12 d_{\mathcal H\Delta\mathcal H}(P_S, P_T)", 40),
             (r"\text{joint error}", r"+", r"\lambda^* = \min_h \big(R_S(h) + R_T(h)\big)", 40)],
            [r"few target labels", r"Ben-David et al. (2010)", r"the shift, \ as the class sees it", r"the joint optimum"],
            colors=[(3, NAIVEC)])

    def exponent(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Bounds like that are loose; minimax theory asks for exact rates. <bookmark mark='b'/> "
            "Samory Kpotufe and Guillaume Martinet, in 2021, measured covariate shift by a transfer exponent gamma: how much "
            "less mass the source puts on small balls of the target's support. <bookmark mark='c'/> Then a source point is "
            "worth a fractional power of a target point, and the minimax rate depends on the source size raised to a power "
            "that shrinks as gamma grows. <bookmark mark='d'/> Tony Cai and Hongji Wei found the analogous rates for "
            "posterior drift, where the regression function itself changes, with an adaptive classifier that needs no "
            "knowledge of how similar the problems are.",
            [(r"\text{bounds}", r"\to", r"\text{minimax rates}", 40),
             (r"\text{transfer exponent}", r":", r"P_S(B(x, r)) \gtrsim r^{\gamma}\,P_T(B(x, r))", 40),
             (r"\text{effective size}", r":", r"n_T + n_S^{\,\kappa(\gamma)}, \ \ \kappa \le 1 \text{ falling in } \gamma", 40),
             (r"\text{posterior drift}", r":", r"\text{adaptive minimax classifiers}", 40)],
            [r"Part 50's question", r"Kpotufe \& Martinet (2021)", r"a source point is worth less", r"Cai \& Wei (2021)"],
            colors=[(2, FIXC)])

    def translasso(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Li, Cai and Li study high-dimensional transfer under restricted coefficient contrasts. An l-one bound h describes the total contrast, rather than a single-coordinate shift. <bookmark mark='b'/> Our demonstration uses one chosen source: first fit a lasso on the pooled source and target. <bookmark mark='c'/> Then fit a sparse correction on target residuals. This is a simplified two-step core, without the paper's adaptive source aggregation. <bookmark mark='d'/> Theoretical gains depend on sparsity, design, sample sizes, contrast size and tuning. A source can pay for shared structure when target data can estimate the correction.",
            [(r"\text{model}", r":", r"w = \beta + \delta, \ \ \|\delta\|_1 \le h", 40),
             (r"\text{step 1}", r":", r"\hat w = \text{lasso on source} \cup \text{target}", 40),
             (r"\text{step 2}", r":", r"\hat\delta = \text{lasso of } y_T - X_T\hat w \text{ on } X_T", 40),
             (r"\text{rate}", r":", r"\frac{s\log p}{n_S + n_T} + \text{a term in } h \ \ \text{vs} \ \ \frac{s\log p}{n_T}", 40)],
            [r"Li, \ Cai \& Li (2022)", r"the shared part", r"the correction", r"the gain"],
            colors=[(3, FIXC)])

    def chart(self):
        d = load("transfer")
        nts = np.asarray(d["nts"], float)
        xs = np.log10(nts)
        yt = [0.1, 0.3, 1, 3]

        def panel(res, cx, title):
            A = axes([1.6, 2.7], [-1.15, 0.7], x_length=4.6, y_length=3.6, xlabel=r"target size $n_T$", ylabel=r"$\|\hat\beta - \beta\|^2$",
                     xticks=list(xs), xfmt=lambda v: f"{10 ** v:.0f}", yticks=list(np.log10(yt)), yfmt=lambda v: f"{10 ** v:g}",
                     center=[cx, 0.35, 0])
            ax = A.ax
            ls = {}
            for k, c, sw, op in (("target", NAIVEC, 3.5, 1.0), ("pooled", TGTC, 10, 0.55), ("transfer", FIXC, 3.5, 1.0)):
                ys = np.log10(res[k])
                ls[k] = VGroup(polyline(ax, xs, ys, c, sw, op), *[Dot(ax.c2p(a, b), radius=0.06, color=c) for a, b in zip(xs, ys)])
            t = label(title, font_size=24).next_to(A, UP, buff=0.25)
            return A, ls, t
        A1, L1, T1 = panel(d["h0.15"], -3.4, r"a similar source: \ 5 coefficients differ by 0.15")
        A2, L2, T2 = panel(d["h1"], 3.4, r"a dissimilar source: \ 5 differ by 1")
        a, b = d["h0.15"], d["h1"]
        key = fit_rows(VGroup(
            label(r"red: \ target-only lasso; \ gold band: \ pooled lasso; \ green: \ two-step transfer core", font_size=24),
            label(rf"similar, \ $n_T = 50$: \ target {a['target'][0]:.2f}, \ pooled {a['pooled'][0]:.2f}, \ transfer {a['transfer'][0]:.2f}", font_size=24, color=FIXC),
            label(rf"dissimilar, \ $n_T = 400$: \ pooled {b['pooled'][-1]:.2f}, \ target {b['target'][-1]:.2f}, \ transfer {b['transfer'][-1]:.2f}", font_size=24, color=GREY_A),
        ), 12.0, 0.22, [0, -2.85, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A simulation: two hundred predictors, ten of them active, a thousand source points, and "
            f"between fifty and four hundred target points. <bookmark mark='b'/> The total l-one contrasts are zero point seven five and five. With a similar source, the target-only lasso, "
            f"in red, needs many target points; with fifty its error is {say(a['target'][0], 2)}. Pooling everything, in gold, "
            f"and Trans-Lasso, in green, are both near {say(a['transfer'][0], 2)}: the source does almost all the work. "
            f"<bookmark mark='c'/> With a dissimilar source, pooling is a disaster: {say(b['pooled'][-1], 2)} even with four "
            f"hundred target points, worse than ignoring the source. <bookmark mark='d'/> Trans-Lasso's correction step "
            f"reduces the error in these repetitions: {say(b['transfer'][-1], 2)}, still better than the target alone at {say(b['target'][-1], 2)}."
        ) as vo:
            self.play(FadeIn(A1), FadeIn(T1), FadeIn(A2), FadeIn(T2), FadeIn(simulated_tag(r"simulated, \ 40 repetitions; \ Monte Carlo errors recorded")))
            vo.wait_until("a")
            self.play(FadeIn(key[0]))
            vo.wait_until("b")
            self.play(*[Create(L1[k]) for k in ("target", "pooled", "transfer")], FadeIn(key[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(L2["target"]), Create(L2["pooled"]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(L2["transfer"]), FadeIn(key[2]), run_time=1.5)
        self.clear_scene()

    def negative(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The failure of pooling has a name: negative transfer. Adding data can make an estimator "
            "worse, when the added data answer a different question. <bookmark mark='b'/> Guarding against it needs either "
            "knowledge of the similarity, or a way to estimate it. <bookmark mark='c'/> With several candidate sources, Li, "
            "Cai and Li aggregate the Trans-Lasso fits from each, with weights chosen on held-out target data, so that "
            "useless sources are ignored automatically. <bookmark mark='d'/> The principle generalizes: a transfer method "
            "should never do much worse than using the target alone.",
            [(r"\text{negative transfer}", r":", r"\text{more data, \ worse estimate}", 40),
             (r"\text{needs}", r":", r"\text{knowing or estimating the similarity}", 40),
             (r"\text{many sources}", r":", r"\text{aggregate with held-out target data}", 40),
             (r"\text{principle}", r":", r"\text{never much worse than target-only}", 40)],
            [r"the gold line", r"$h$, \ or its estimate", r"Trans-Lasso's aggregation", r"an objective requiring model and aggregation assumptions"],
            colors=[(0, NAIVEC), (3, FIXC)])

    def domain(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> In deep learning, domain adaptation learns a representation in which source and target "
            "look alike: Yaroslav Ganin and co-authors' domain-adversarial networks, in 2016, train a feature extractor to "
            "fool a classifier of domain membership. <bookmark mark='b'/> It shrinks the divergence term in Ben-David's bound. "
            "<bookmark mark='c'/> But matching the covariate distributions can hurt, when the label proportions also "
            "differ: aligning the features then misaligns the classes, as Han Zhao and co-authors showed in 2019. <bookmark "
            "mark='d'/> Every adaptation method encodes an assumption about what stays fixed; the statistics is in "
            "knowing which.",
            [(r"\text{DANN}", r":", r"\text{features that fool a domain classifier}", 40),
             (r"\text{aim}", r":", r"\text{shrink } d_{\mathcal H\Delta\mathcal H}", 40),
             (r"\text{but}", r":", r"\text{with label shift, \ alignment hurts}", 40),
             (r"\text{so}", r":", r"\text{each method assumes something fixed}", 40)],
            [r"Ganin et al. (2016)", r"Ben-David's bound", r"Zhao et al. (2019)", r"chapters 5, \ 6 and 8"],
            colors=[(2, NAIVEC)])
