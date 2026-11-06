from __future__ import annotations

import numpy as np
from scipy import stats

from videos.stats.stats28.common import *  # noqa: F403


class Averaging(VoiceoverScene):
    def construct(self):
        self.card()
        self.bma()
        self.occam()
        self.closed_open()
        self.candidates()
        self.weights()
        self.scores()
        self.stacking()
        self.prostate_avg()

    def card(self):
        card = chapter_card(8, r"Averaging", r"Weight the models instead of choosing one", lit=(1999,), part=PART)
        with self.voiceover("Chapter eight. Averaging models."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bma(self):
        rows = [
            cmath(r"p(M_k \mid y)", r"\propto", r"p(y \mid M_k)\, p(M_k)", font_size=32),
            cmath(r"p(\tilde y \mid y)", r"=", r"\textstyle\sum_k p(\tilde y \mid y, M_k)\, p(M_k \mid y)", font_size=30),
            cmath(r"\text{uncertainty}", r":", r"\text{within models, \ and between them}", font_size=30),
            cmath(r"\text{optimal}", r":", r"\text{if one of the } M_k \text{ is true}", font_size=30),
        ]
        rows[1][2].set_color(AICC)
        whys = [why(r"each model's evidence, \ Part 26"), why(r"Bayesian model averaging"),
                why(r"Hoeting, Madigan, Raftery \& Volinsky (1999)"), why(r"the $\mathcal M$-closed view")]
        with self.voiceover(
            "<bookmark mark='a'/> Choosing one model throws away the uncertainty about which. Bayes's answer: give each model "
            "a prior probability, and its posterior probability is proportional to the prior times the evidence. "
            "<bookmark mark='b'/> Predict with the posterior-weighted mixture of the models' predictions. "
            "<bookmark mark='c'/> Its uncertainty includes both the uncertainty within each model and the uncertainty between "
            "them, the case Jennifer Hoeting, David Madigan, Adrian Raftery and Chris Volinsky made in 1999. "
            "<bookmark mark='d'/> If one of the candidates is true, nothing predicts better on average."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def closed_open(self):
        rows = fit_rows(VGroup(
            label(r"$\mathcal M$-closed: \ the truth is one of the candidates", font_size=26, color=BICC),
            label(r"$\mathcal M$-open: \ none of them is; \ we want the best combination", font_size=26, color=AICC),
            label(r"BMA's weights converge to the single candidate closest in KL", font_size=26, color=RES),
            label(r"a mixture of wrong models can beat each of them", font_size=26, color=HIT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> José Bernardo and Adrian Smith named the distinction. In the M-closed world the truth is one "
            "of the candidates. <bookmark mark='b'/> In the M-open world none is, and the honest goal is the best combination. "
            "<bookmark mark='c'/> In that world Bayesian model averaging behaves oddly: as data accumulate, its weights pile "
            "onto whichever single candidate is closest in Kullback–Leibler divergence, because the evidence of each model "
            "is a product over observations. <bookmark mark='d'/> Yet a weighted mixture of wrong models can be much closer "
            "to the truth than any one of them."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def candidates(self):
        d = load("averaging")
        xs, tr = np.asarray(d["xs"]), np.asarray(d["truth"])
        A = axes([-6, 6], [0, 0.45], x_length=7.6, y_length=4.2, xlabel=r"$y$", ylabel=r"density", xticks=[-4, -2, 0, 2, 4],
                 yticks=[0, 0.2, 0.4], center=[-2.0, 0.3, 0])
        ax = A.ax
        truth = curve(ax, xs, tr, TRUE, 4)
        m1 = curve(ax, xs, stats.norm.pdf(xs, -2, 1), AICC, 3)
        m2 = curve(ax, xs, stats.norm.pdf(xs, 2, 1), BICC, 3)
        mix = DashedVMobject(curve(ax, xs, 0.5 * stats.norm.pdf(xs, -2, 1) + 0.5 * stats.norm.pdf(xs, 2, 1), HIT, 3), num_dashes=60)
        rows = fit_rows(VGroup(
            label(r"gold: \ the truth, \ half $N(-2, 1)$, \ half $N(2, 1)$", font_size=22, color=TRUE),
            label(r"blue: \ model 1, \ $N(-2, 1)$", font_size=22, color=AICC),
            label(r"purple: \ model 2, \ $N(2, 1)$", font_size=22, color=BICC),
            label(r"green dashed: \ the 50/50 mixture of the two \ $=$ the truth", font_size=22, color=HIT),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A stark example. The truth is a fifty-fifty mixture of two normals, at minus two and plus "
            "two. <bookmark mark='b'/> Model one says every observation is normal around minus two. <bookmark mark='c'/> Model "
            "two says plus two. Both are wrong, and equally wrong. <bookmark mark='d'/> But an equal mixture of their "
            "predictions is exactly the truth. Which weights do the two methods find?"
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(m1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(m2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(mix), FadeIn(rows[3]))
        self.clear_scene()

    def weights(self):
        d = load("averaging")
        ns = np.log10(np.asarray(d["ns"], float))
        A = axes([1.1, 2.9], [0.4, 1.02], x_length=7.4, y_length=4.4, xlabel=r"sample size $n$ \ (log scale)",
                 ylabel=r"weight on the favoured model", xticks=[np.log10(20), 2, np.log10(500)], yticks=[0.5, 0.75, 1],
                 xfmt=lambda v: f"{10 ** v:.0f}", center=[-2.0, 0.3, 0])
        ax = A.ax
        half = DashedLine(ax.c2p(1.1, 0.5), ax.c2p(2.9, 0.5), color=HIT, stroke_width=2)
        lb = polyline(ax, ns, d["bma"], AICC, 3)
        ls = polyline(ax, ns, d["stack"], LOOC, 3)
        db = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=AICC) for a, b in zip(ns, d["bma"])])
        ds = VGroup(*[Dot(ax.c2p(a, b), radius=0.06, color=LOOC) for a, b in zip(ns, d["stack"])])
        rows = fit_rows(VGroup(
            label(r"100 data sets at each $n$", font_size=22),
            label(r"blue: \ BMA: \ all on one model, \ at random", font_size=22, color=AICC),
            label(r"orange: \ stacking: \ towards 50/50", font_size=22, color=LOOC),
            label(r"green dashed: \ the right answer", font_size=22, color=HIT),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A hundred data sets at each sample size, from twenty to five hundred. Plotted is the weight "
            "given to whichever model a method favours. <bookmark mark='b'/> Bayesian model averaging puts ninety-nine percent "
            "on one model, already at twenty observations: whichever happened to have slightly more data on its side, chosen "
            "essentially by coin toss. <bookmark mark='c'/> Stacking chooses the weights that maximize the leave-one-out log "
            "score of the mixture; it puts fifty-nine percent on the favourite at twenty and moves towards half and half as n "
            "grows, <bookmark mark='d'/> which is the right answer."
        ) as vo:
            self.add(seeded_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(lb), FadeIn(db), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ls), FadeIn(ds), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Create(half), FadeIn(rows[3]))
        self.clear_scene()

    def scores(self):
        d = load("averaging")
        hdr = [r"\textbf{$n$}", r"\textbf{best single model}", r"\textbf{BMA}", r"\textbf{stacking}"]
        body = [[f"{n}", f"{a:.2f}", f"{b:.2f}", f"{c:.2f}"] for n, a, b, c in zip(d["ns"], d["score_best"], d["score_bma"], d["score_stack"])]
        tb = table_rows([hdr] + body, font_size=26, col_buff=1.0, row_buff=0.3, colors=[GREY_A] + [None] * 5)
        for r in tb[1:]:
            r[1].set_color(RES)
            r[2].set_color(AICC)
            r[3].set_color(LOOC)
        tb.move_to([0, 0.8, 0])
        foot = fit_rows(VGroup(
            label(r"mean log density of 2{,}000 new draws \ (higher is better)", font_size=22),
            label(r"the truth itself scores $-2.05$: \ stacking is within a hundredth of it", font_size=22, color=HIT),
        ), 12.0, 0.22, [0, -2.0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Judge the predictions on two thousand new draws by their log score. "
            "<bookmark mark='b'/> The best single model scores about minus five point two: it assigns almost no probability to "
            "half of the data. <bookmark mark='c'/> Bayesian model averaging is no better, about minus five point one, because "
            "it has in effect chosen one model. <bookmark mark='d'/> Stacking scores minus two point oh six, within a hundredth "
            "of the truth's own minus two point oh five. In the M-open world, combining beats choosing, and Bayes's weights "
            "are not the ones to combine with."
        ) as vo:
            self.add(seeded_tag())
            vo.wait_until("a")
            self.play(FadeIn(tb[0]), LaggedStart(*[FadeIn(r[0]) for r in tb[1:]], lag_ratio=0.1), FadeIn(foot[0]))
            for j, m_ in zip((1, 2, 3), "bcd"):
                vo.wait_until(m_)
                self.play(LaggedStart(*[FadeIn(r[j]) for r in tb[1:]], lag_ratio=0.1))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def stacking(self):
        rows = [
            cmath(r"\hat w", r"=", r"\arg\max_{w \in \Delta} \textstyle\sum_i \log \sum_k w_k\, p(y_i \mid y_{-i}, M_k)", font_size=28),
            cmath(r"p(y_i \mid y_{-i}, M_k)", r":", r"\text{PSIS-LOO, \ chapter five}", font_size=30),
            cmath(r"\text{pseudo-BMA}", r":", r"w_k \propto \exp(\widehat{\text{elpd}}_k)", font_size=30),
            cmath(r"\text{point predictions}", r":", r"\text{Wolpert (1992), \ Breiman (1996)}", font_size=30),
        ]
        rows[0][2].set_color(LOOC)
        whys = [why(r"Yao, Vehtari, Simpson \& Gelman (2018)"), why(r"no refitting needed"),
                why(r"cheaper, \ but chooses like BMA"), why(r"stacked regressions, \ super learners")]
        with self.voiceover(
            "<bookmark mark='a'/> Stacking, in the Bayesian form of Yuling Yao, Aki Vehtari, Daniel Simpson and Andrew Gelman: "
            "choose weights on the simplex to maximize the summed log of the weighted leave-one-out predictive densities. "
            "<bookmark mark='b'/> Those densities come free from chapter five's PSIS-LOO. <bookmark mark='c'/> Weighting each "
            "model by its exponentiated elpd, pseudo-BMA, is cheaper but behaves like BMA, piling weight on one model. "
            "<bookmark mark='d'/> For point predictions the idea is older: David Wolpert's stacked generalization and Leo "
            "Breiman's stacked regressions, today's super learners."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def prostate_avg(self):
        d = load("prostate")
        crit = d["crit"]
        aic = np.array([c["aic"] for c in crit])
        bic = np.array([c["bic"] for c in crit])
        wa = np.exp(-0.5 * (aic - aic.min()))
        wa /= wa.sum()
        wb = np.exp(-0.5 * (bic - bic.min()))
        wb /= wb.sum()
        A = axes([-0.6, 8.6], [0, 0.4], x_length=7.4, y_length=4.2, xlabel=r"subset size \ (best subset of each size)",
                 ylabel=r"weight", xticks=list(range(9)), yticks=[0, 0.1, 0.2, 0.3, 0.4], yfmt=lambda v: f"{v:.1f}", center=[-2.0, 0.3, 0])
        ax = A.ax
        wid = ax.c2p(0.36, 0)[0] - ax.c2p(0, 0)[0]
        ba = VGroup(*[Rectangle(width=wid, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 1e-3), fill_color=AICC, fill_opacity=0.85,
                                stroke_width=1).move_to(ax.c2p(k - 0.19, v / 2)) for k, v in enumerate(wa)])
        bb = VGroup(*[Rectangle(width=wid, height=max(ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], 1e-3), fill_color=BICC, fill_opacity=0.85,
                                stroke_width=1).move_to(ax.c2p(k + 0.19, v / 2)) for k, v in enumerate(wb)])
        rows = fit_rows(VGroup(
            label(r"Akaike weights: \ $w_k \propto e^{-\text{AIC}_k/2}$", font_size=22, color=AICC),
            label(rf"no size above {100 * wa.max():.0f}\%: \ spread over sizes 4--8", font_size=22, color=AICC),
            label(r"BIC weights: \ approximate posterior probabilities", font_size=22, color=BICC),
            label(rf"sizes 2, 3, 4: \ {100 * wb[2]:.0f}\%, {100 * wb[3]:.0f}\%, {100 * wb[4]:.0f}\%", font_size=22, color=BICC),
            label(r"either way: \ no single subset deserves our confidence", font_size=22, color=RES),
        ), 4.3, 0.42, [4.5, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Back to the prostate data. Burnham and Anderson's Akaike weights turn AIC differences into "
            "weights. <bookmark mark='b'/> No subset size gets more than about a third of them; the weight spreads over four to "
            "eight predictors. <bookmark mark='c'/> BIC differences, exponentiated, approximate posterior model probabilities. "
            "<bookmark mark='d'/> They move the weight to smaller models, but split it almost evenly between two, three and four "
            "predictors. <bookmark mark='e'/> Either way the message is the "
            "same as chapter four's flat CV curve: the data do not single out one subset, and any report that pretends they do "
            "overstates what is known."
        ) as vo:
            self.add(prostate_tag())
            self.play(FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in ba], lag_ratio=0.1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bb], lag_ratio=0.1), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def occam(self):
        rows = [
            cmath(r"\text{models}", r":", r"2^p \text{ subsets: \ too many to sum}", font_size=30),
            cmath(r"\text{Occam's window}", r":", r"\text{drop } M_k \text{ if } \tfrac{p(M_k \mid y)}{\max_j p(M_j \mid y)} < \tfrac1{20}", font_size=28),
            cmath(r"\text{MC}^3", r":", r"\text{a Markov chain over models}", font_size=30),
            cmath(r"\text{prior on models}", r":", r"\text{uniform on subsets favours size } p/2", font_size=30),
        ]
        rows[1][2].set_color(AICC)
        whys = [why(r"BMA's computational problem"), why(r"Madigan \& Raftery (1994)"),
                why(r"Madigan \& York (1995): \ Part 27 on models"), why(r"Scott \& Berger (2010): \ beta-binomial instead")]
        with self.voiceover(
            "<bookmark mark='a'/> With p predictors there are two to the p subsets, too many to average over. "
            "<bookmark mark='b'/> David Madigan and Adrian Raftery's Occam's window keeps only the models within a factor of "
            "twenty of the best. <bookmark mark='c'/> Madigan and Jeremy York's MC cubed runs a Markov chain over the models "
            "themselves, Part 27's machinery on a discrete space. <bookmark mark='d'/> And the prior on models matters: a "
            "uniform prior on subsets piles its mass on models of half the size, so James Scott and James Berger recommend a "
            "beta-binomial prior on the number of predictors, which also corrects for multiplicity."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
