from __future__ import annotations

import numpy as np

from videos.stats.stats54.common import *  # noqa: F403


class ERM(VoiceoverScene):
    def construct(self):
        self.card()
        self.setup_ladder()
        self.decomposition()
        self.chart()
        self.finite()
        self.pac()
        self.nfl()
        self.srm()

    def card(self):
        card = chapter_card(1, r"ERM and uniform convergence", r"Why the chosen rule's sample error lies", lit=(1971,), part=PART)
        with self.voiceover("Chapter one. Empirical risk minimization and uniform convergence: why the chosen rule's sample error lies."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def setup_ladder(self):
        rows = [
            cmath(r"(X_i, Y_i) \overset{iid}{\sim} P", r":", r"\text{a loss } \ell(h(x), y), \ \text{a class } \mathcal H", font_size=34),
            cmath(r"R(h) = E\,\ell(h(X), Y)", r",", r"\ R_n(h) = \tfrac1n\textstyle\sum_i \ell(h(X_i), Y_i)", font_size=34),
            cmath(r"\hat h", r"=", r"\arg\min_{h \in \mathcal H} R_n(h): \ \text{empirical risk minimization}", font_size=34),
            cmath(r"E\,R_n(\hat h)", r"\le", r"E\,R(\hat h) \text{ (in expectation): \ } \hat h \text{ was chosen to look good}", font_size=32),
        ]
        rows[2][-1].set_color(CLASSC)
        rows[3][-1].set_color(BADC)
        whys = [why(r"no model for $P$"), why(r"true and empirical risk"), why(r"ERM"), why(r"optimism")]
        heading = label('A fixed class and independent bounded losses define the learning problem', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Take an independent, identically distributed sample and a fixed measurable class of rules. For the classification bounds here, losses lie between zero and one. <bookmark mark='b'/> True risk is expected loss on a new observation; empirical risk averages the observed losses. <bookmark mark='c'/> Empirical risk minimization chooses a rule with the smallest sample risk. <bookmark mark='d'/> This creates optimism in expectation: the chosen rule tends to look better on its training sample. It is not a pointwise inequality on every dataset."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def decomposition(self):
        rows = [
            cmath(r"R(\hat h) - R^*", r"=", r"\underbrace{R(\hat h) - \inf_{\mathcal H} R}_{\text{estimation}} + \underbrace{\inf_{\mathcal H} R - R^*}_{\text{approximation}}", font_size=32),
            cmath(r"R(\hat h) - \inf_{\mathcal H} R", r"\le", r"2\sup_{h \in \mathcal H} |R_n(h) - R(h)|", font_size=34),
            cmath(r"\text{so}", r":", r"\text{control the uniform deviation, \ and ERM is safe}", font_size=34),
            cmath(r"\text{a bigger class}", r":", r"\text{less approximation error, \ more estimation error}", font_size=34),
        ]
        rows[1][-1].set_color(BOUNDC)
        rows[3][-1].set_color(CLASSC)
        whys = [why(r"$R^*$: \ the Bayes risk"), why(r"add and subtract"), why(r"Vapnik's programme"), why(r"Part 19's trade-off")]
        heading = label('ERM trades approximation error against a uniform estimation error', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The excess risk over the best possible, the Bayes risk, splits in two: estimation error, how "
            "far the chosen rule is from the best in the class, and approximation error, how far the class's best is from "
            "the best overall. <bookmark mark='b'/> Adding and subtracting empirical risks bounds the estimation error by "
            "twice the largest gap between empirical and true risk over the whole class. <bookmark mark='c'/> So the "
            "programme is to control that uniform deviation: then minimizing the empirical risk is safe. <bookmark "
            "mark='d'/> And class size trades the two errors off against each other, Part nineteen's bias–variance "
            "trade-off in its most general form."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("erm")
        ln = np.log10(d["ns"])
        g = d["by_eta"]["0.1"]
        A = axes([1.3, 3.3], [-3.4, 0.4], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$",
                 xticks=[np.log10(25), 2, np.log10(400), np.log10(1600)], xfmt=lambda v: f"{10 ** v:.0f}", yticks=[-3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax

        def line(v, c, w=4):
            return VGroup(polyline(ax, ln, np.log10(v), c, w), *[Dot(ax.c2p(a, b), radius=0.06, color=c) for a, b in zip(ln, np.log10(v))])

        cvc = line(d["vc"], BOUNDC)
        crad = line(d["rad"], BOUNDC, 2.5)
        cdev = line(g["dev"], TRAINC)
        cex = line(g["excess"], CLASSC)
        sd = float(np.polyfit(ln, np.log10(g["dev"]), 1)[0])
        se = float(np.polyfit(ln, np.log10(g["excess"]), 1)[0])
        side = fit_rows(VGroup(
            label(r"thresholds $1\{x > t\}$ on $[0, 1]$, \ 10\% label noise", font_size=22),
            label(r"purple: \ 95\% VC bound; \ thinner: expectation bound", font_size=22, color=BOUNDC),
            label(rf"teal: \ $\sup_t |R_n - R|$, \ slope {sd:.2f}", font_size=22, color=TRAINC),
            label(rf"gold: \ ERM's excess risk, \ slope {se:.2f}", font_size=22, color=CLASSC),
            label(r"probability bounds and expectations are different guarantees", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The simplest class: thresholds on the unit interval, with ten percent of labels flipped at random, two hundred data sets at each size. <bookmark mark='b'/> The VC bound in purple, and the thinner expectation bound below it. This is not another ninety-five percent confidence bound. <bookmark mark='c'/> The actual uniform deviation, in teal, falls with slope {say(sd, 2)}: one over root n, as the theory says. <bookmark mark='d'/> But ERM's excess risk, in gold, falls with slope {say(se, 2)}, much faster: one over n. The uniform deviation is a worst case over all thresholds, and the chosen one is not the worst; chapter four explains the gap. <bookmark mark='e'/> The VC bound is valid at every n, and about ten times too large."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ probability and expectation bounds")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cvc), Create(crad), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cdev), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cex), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def finite(self):
        rows = [
            cmath(r"|\mathcal H| = K", r":", r"P\big(\sup_h |R_n(h) - R(h)| > t\big) \le 2K e^{-2nt^2}", font_size=34),
            cmath(r"\text{so}", r":", r"\sup_h |R_n - R| \le \sqrt{\log(2K/\delta)/(2n)} \ \text{ w.p. } 1 - \delta", font_size=34),
            cmath(r"\log K", r":", r"\text{the class's size enters only through its logarithm}", font_size=34),
            cmath(r"\text{infinite classes}", r":", r"\text{symmetrize first; then count patterns on a ghost sample}", font_size=32),
        ]
        rows[1][-1].set_color(BOUNDC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Hoeffding $+$ union"), why(r"invert"), why(r"Occam's razor"), why(r"the VC idea, \ next")]
        heading = label('A union bound protects selection from a fixed finite class', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> For a class of K rules fixed before the data, bounded losses let Hoeffding control each rule. A union bound makes the failure probability at most two K times e to the minus two n t squared. <bookmark mark='b'/> Inverting gives the displayed simultaneous confidence bound. <bookmark mark='c'/> Only log K enters, a mathematical form of Occam's razor. <bookmark mark='d'/> Infinite classes require a ghost-sample symmetrization argument before counting label patterns. We cannot simply substitute the observed number of patterns into this finite-class formula."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def pac(self):
        rows = [
            cmath(r"\text{realizable PAC}", r":", r"\text{some } h \in \mathcal H \text{ has zero error}", font_size=34),
            cmath(r"n", r"\ge", r"\frac{c}{\varepsilon}\Big(d\log\frac1\varepsilon + \log\frac1\delta\Big) \Rightarrow R(\hat h) \le \varepsilon \text{ w.p. } 1 - \delta", font_size=32),
            cmath(r"\text{agnostic}", r":", r"n \asymp \frac{d + \log(1/\delta)}{\varepsilon^2}: \ \text{a whole power of } \varepsilon \text{ worse}", font_size=32),
            cmath(r"\text{Valiant (1984)}", r":", r"\text{probably approximately correct, \ in polynomial time}", font_size=32),
        ]
        rows[1][-1].set_color(GOODC)
        rows[2][-1].set_color(BADC)
        whys = [why(r"no label noise"), why(r"Blumer et al. (1989)"), why(r"noise costs $1/\varepsilon$"), why(r"the PAC framework")]
        heading = label('Realizable and agnostic learning have different sample complexities', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The same questions in the language of computer science. In the realizable case, some rule in the class makes no mistakes at all. <bookmark mark='b'/> Then about d over epsilon times log one over epsilon examples suffice for ERM's error to be below epsilon with high probability, as Anselm Blumer and colleagues proved in 1989. <bookmark mark='c'/> With label noise, the agnostic case, the number grows to d over epsilon squared: a whole power of epsilon worse, the slow rate of chapter one. <bookmark mark='d'/> Leslie Valiant's probably-approximately-correct framework of 1984 added the requirement that learning run in polynomial time, which makes it a theory of algorithms as well as of samples."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def srm(self):
        rows = [
            cmath(r"\mathcal H_1 \subset \mathcal H_2 \subset \cdots", r":", r"\text{nested classes of growing capacity}", font_size=34),
            cmath(r"\text{SRM}", r":", r"\hat h = \arg\min_{k, h \in \mathcal H_k} R_n(h) + \mathrm{pen}(k), \ \ \mathrm{pen}(k) \asymp \sqrt{d_k/n}", font_size=30),
            cmath(r"\text{oracle inequality}", r":", r"R(\hat h) \lesssim \min_k \big(\inf_{\mathcal H_k} R + \mathrm{pen}(k)\big)", font_size=34),
            cmath(r"\text{in practice}", r":", r"\text{the penalty is chosen by cross-validation \ (Part 28)}", font_size=34),
        ]
        rows[2][-1].set_color(GOODC)
        whys = [why(r"Vapnik's structure"), why(r"structural risk minimization"), why(r"adapts to the best $k$"), why(r"data-driven penalties")]
        heading = label('Selecting a class requires paying for complexity and the class index', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> When the right class size is unknown, Vapnik's structural risk minimization uses a nested sequence of classes of growing capacity. <bookmark mark='b'/> It minimizes the empirical risk plus a penalty for the class's complexity, of order the root of its VC dimension over n. <bookmark mark='c'/> The result satisfies an oracle inequality: it does almost as well as if the best class had been known in advance, trading approximation against estimation automatically. <bookmark mark='d'/> In practice the penalty is usually replaced by cross-validation, Part twenty-eight's method, which estimates the same trade-off from the data."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def nfl(self):
        rows = fit_rows(VGroup(
            label(r"and without a class, \ nothing:", font_size=28, color=GREY_A),
            label(r"no free lunch: \ for every learner, \ some distribution defeats it (Wolpert 1996)", font_size=26, color=BADC),
            label(r"a class of infinite VC dimension cannot be learned uniformly at any rate", font_size=26, color=BADC),
            label(r"the class is the prior of learning theory: \ what you are willing to assume", font_size=26, color=CLASSC),
            label(r"the fundamental theorem: \ learnable $\iff$ finite VC dimension", font_size=26, color=GOODC),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> And without restricting the class, nothing can be learned. <bookmark mark='b'/> The no-"
            "free-lunch theorems, in David Wolpert's form, say that for every learning algorithm there is a distribution on "
            "which it does badly. <bookmark mark='c'/> A class of infinite VC dimension cannot be learned uniformly over "
            "distributions at any rate. <bookmark mark='d'/> So the class plays the role a prior plays for a Bayesian: it is "
            "what you are willing to assume. <bookmark mark='e'/> The fundamental theorem of statistical learning says a "
            "binary class is learnable, in the distribution-free sense, exactly when its VC dimension is finite."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
