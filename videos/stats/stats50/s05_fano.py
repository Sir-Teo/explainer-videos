from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class Fano(VoiceoverScene):
    def construct(self):
        self.card()
        self.inequality()
        self.proof()
        self.packing()
        self.vg()
        self.sparse()
        self.entropy()
        self.chart()

    def card(self):
        card = chapter_card(4, r"Fano's method", r"Many hypotheses, \ and how many bits the data carry", part=PART)
        with self.voiceover("Chapter four. Fano's method: many hypotheses, and how many bits the data carry."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def inequality(self):
        rows = [
            cmath(r"\theta_1, \dots, \theta_M", r":", r"\text{pairwise } \ge 2\delta \text{ apart}, \ \ \mathrm{KL}(P_j^n, P_0^n) \le \beta \ \ \forall j", font_size=32),
            cmath(r"\text{Fano (1952)}", r":", r"P(\text{wrong } j) \ge 1 - \frac{I(J; X) + \log 2}{\log M}, \ \ I \le \beta", font_size=32),
            cmath(r"\inf_{\hat\theta} \max_j E_j \|\hat\theta - \theta_j\|^2", r"\ge", r"\delta^2 \Big(1 - \frac{\beta + \log 2}{\log M}\Big)", font_size=34),
            cmath(r"\text{the game}", r":", r"\text{exponentially many hypotheses, \ each one costing little information}", font_size=30),
        ]
        rows[2][-1].set_color(LOWC)
        rows[3][-1].set_color(HYPC)
        whys = [why(r"a $2\delta$-separated packing"), why(r"information theory's inequality"), why(r"the lower bound"), why(r"$\log M \gg \beta$")]
        heading = label('A packing turns estimation into identification among many laws', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Two points give rates for one-dimensional features. For a whole function, or a long vector, "
            "use many hypotheses: M of them, pairwise at least two delta apart, each with Kullback–Leibler divergence at most "
            "beta from a centre. <bookmark mark='b'/> Robert Fano's inequality from information theory says that identifying "
            "which of M hypotheses is true fails with probability at least one minus the information the data carry, plus "
            "log two, over log M. The data can carry at most beta nats about which hypothesis holds. <bookmark mark='c'/> So "
            "every estimator's worst risk is at least delta squared times one minus beta plus log two over log M. <bookmark "
            "mark='d'/> The game is now to find exponentially many hypotheses, far apart, each costing little information."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"J \sim \text{uniform on } \{1..M\}, \ X \mid J \sim P_J", r":", r"\text{nature's coin}", font_size=34),
            cmath(r"I(J; X)", r"=", r"\tfrac1M \textstyle\sum_j \mathrm{KL}(P_j \| \bar P) \le \max_j \mathrm{KL}(P_j \| P_0)", font_size=32),
            cmath(r"H(J \mid X)", r"\ge", r"\log M - I(J; X): \ \text{the data leave most of the uncertainty}", font_size=32),
            cmath(r"\text{Fano}", r":", r"H(J \mid X) \le \log 2 + P(\hat J \ne J)\log M", font_size=34),
        ]
        rows[1][-1].set_color(HYPC)
        rows[3][-1].set_color(LOWC)
        whys = [why(r"a uniform prior on the packing"), why(r"mutual information, \ bounded by KL"), why(r"entropy accounting"), why(r"Fano (1952)")]
        heading = label('Mutual information limits how much a sample reveals', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Why Fano's inequality holds. Let nature pick the hypothesis index J uniformly, and then draw "
            "the data. <bookmark mark='b'/> The mutual information between J and the data is the average Kullback–Leibler "
            "divergence of each P j from their mixture, which is at most the largest divergence from any fixed centre. "
            "<bookmark mark='c'/> So the uncertainty about J left after seeing the data is at least log M minus that "
            "information: the data can only remove as many nats as they carry. <bookmark mark='d'/> And Fano's inequality, "
            "from information theory, says that any guess of J leaves uncertainty at most log two plus the error probability "
            "times log M. Combining the two gives the bound. Statistics borrows a theorem about communication channels."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def packing(self):
        W = LowerBoundPacking(center=(-2.6, -0.2, 0), scale=0.9)
        g = np.array([[0.9 * i + 0.45 * (j % 2), 0.8 * j] for i in range(-3, 3) for j in range(-2, 3)], float)
        pts = W.place(g, color=HYPC, radius=0.07)
        disc = W.separation(0.4, color=UPC, opacity=0.1)
        side = fit_rows(VGroup(
            label(r"gold: \ $M$ hypotheses, \ a packing", font_size=22, color=HYPC),
            label(r"blue: \ disjoint discs of radius $\delta$", font_size=22, color=UPC),
            label(r"the data's information: \ at most $\beta$ nats", font_size=22, color=LOWC),
            label(r"$\log M \gg \beta$: \ cannot tell which", font_size=22, color=LOWC),
            label(r"a packing of a ball in $d$ dims: \ $M \approx (R/\delta)^d$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the workbench: a packing, many hypotheses spread through the parameter set. <bookmark "
            "mark='b'/> Each has its own disc of radius delta, and the discs do not overlap. <bookmark mark='c'/> The data "
            "carry at most beta nats of information about which one is true, <bookmark mark='d'/> and when log M is much "
            "larger than beta, identification fails with high probability. <bookmark mark='e'/> In d dimensions a ball "
            "contains about R over delta to the d well-separated points, so log M grows linearly with the dimension, which is "
            "why Fano's method gives dimension-dependent rates."
        ) as vo:
            self.play(FadeIn(exact_tag(r"the lower-bound workbench")))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(disc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def vg(self):
        d = load("fano")
        rows = [
            cmath(r"\{0,1\}^d", r":", r"\text{the hypercube, \ Hamming distance}", font_size=34),
            cmath(r"\text{Varshamov--Gilbert}", r":", r"\exists\, M \ge 2^{d/8} \text{ points, \ pairwise } \ge d/8 \text{ apart}", font_size=32),
            cmath(rf"d = {d['d']}", r":", rf"\text{{guarantee }} {d['vg_guarantee']:.0f}; \ \text{{a greedy random search finds }} {d['vg_M']:,}", font_size=32),
            cmath(r"\Rightarrow", r"\;", r"\log M \asymp d: \ \text{as many bits as coordinates}", font_size=34),
        ]
        rows[2][-1].set_color(HYPC)
        rows[3][-1].set_color(LOWC)
        whys = [why(r"vertices as hypotheses"), why(r"Gilbert (1952); \ Varshamov (1957)"), why(r"the guarantee is loose"), why(r"the engine of Fano bounds")]
        heading = label('An existence theorem and a finite random search are distinct', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            f"<bookmark mark='a'/> The standard source of packings is the hypercube: binary strings of length d, with Hamming "
            f"distance. <bookmark mark='b'/> The Varshamov–Gilbert bound, from coding theory, guarantees at least two to the d "
            f"over eight strings that pairwise differ in at least d over eight places. <bookmark mark='c'/> For d equal to "
            f"{d['d']}, the guarantee is {d['vg_guarantee']:.0f} strings; a greedy random search finds {d['vg_M']:,}. The "
            f"guarantee is loose, but its exponent is what matters. <bookmark mark='d'/> Log M is of the order of d: a packing "
            f"with as many bits as there are coordinates."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def sparse(self):
        rows = [
            cmath(r"y = \theta + z, \ \theta \in \mathbb R^p, \ \|\theta\|_0 \le s", r":", r"\text{sparse normal means}", font_size=32),
            cmath(r"\text{pack } s\text{-sparse sign vectors}", r":", r"\log M \asymp s \log(ep/s)", font_size=34),
            cmath(r"\Rightarrow", r"\;", r"\inf_{\hat\theta} \sup_{\|\theta\|_0 \le s} E\|\hat\theta - \theta\|^2 \asymp s \log(ep/s)", font_size=34),
            cmath(r"\text{attained by}", r":", r"\text{soft thresholding at } \sqrt{2 \log(p/s)}, \ \text{the lasso, \ SLOPE}", font_size=32),
        ]
        rows[2][-1].set_color(LOWC)
        rows[3][-1].set_color(UPC)
        whys = [why(r"Part 32's sparsity"), why(r"choose the support: \ $\binom ps$ ways"), why(r"Donoho \& Johnstone (1994)"), why(r"Part 32's estimators, \ optimal")]
        heading = label('An unknown sparse support costs logarithmic complexity', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> The cleanest application: estimating a vector of p normal means of which at most s are non-zero, Part thirty-two's sparsity. <bookmark mark='b'/> Pack sign vectors with s non-zero coordinates: there are about p choose s supports, so log M is of order s log p over s. <bookmark mark='c'/> Fano's inequality then gives the minimax risk: of order s log of e p over s, the price of an unknown support; the e keeps the expression meaningful in the dense endpoint. <bookmark mark='d'/> And soft thresholding at the root of two log p over s attains it up to a constant, as do the lasso and SLOPE: Part thirty-two's estimators are minimax optimal."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def entropy(self):
        rows = [
            cmath(r"\text{Yang \& Barron (1999)}", r":", r"\text{a global-entropy rate bound can balance } \log N(\varepsilon_n) \asymp n\,\varepsilon_n^2", font_size=30),
            cmath(r"\log N(\varepsilon) \asymp \varepsilon^{-1/s}", r"\Rightarrow", r"\varepsilon_n^2 \asymp n^{-2s/(2s+1)}: \ \text{Hölder}", font_size=32),
            cmath(r"\log N(\varepsilon) \asymp d \log(1/\varepsilon)", r"\Rightarrow", r"\varepsilon_n^2 \asymp d\log n/n:\ \text{loose global bound; local theory gives }d/n", font_size=32),
            cmath(r"\text{the lesson}", r":", r"\text{Part 48's entropy decides the rate: \ size is difficulty}", font_size=32),
        ]
        rows[0][-1].set_color(HYPC)
        rows[3][-1].set_color(ADAPTC)
        whys = [why(r"a general recipe"), why(r"smooth functions"), why(r"finite dimensions"), why(r"complexity, \ measured")]
        heading = label('Global entropy bounds may need localization for a sharp rate', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Fano's method leads to a general recipe, due to Yuhong Yang and Andrew Barron in 1999. For density estimation in Hellinger distance, a global entropy balance can provide rate bounds when packing, covering and information conditions hold: the class's complexity balances the information in the sample. <bookmark mark='b'/> For Hölder classes, whose entropy is one over epsilon to the one over s, this gives the familiar n to the minus two s over two s plus one. <bookmark mark='c'/> For a d-parameter family, whose entropy is d log one over epsilon, this global calculation gives a generally loose d log n over n bound. Local entropy or local packings recover the sharp d over n rate in regular finite-dimensional models. <bookmark mark='d'/> So Part forty-eight's metric entropy, invented to make empirical processes behave, also decides how hard estimation is. The size of a class is its difficulty."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("fano")
        s = np.log10([r["s"] for r in d["rows"]])
        A = axes([-0.1, 2.1], [0, 3.2], x_length=7.4, y_length=4.4, xlabel=r"sparsity $s$ \ (log scale)", ylabel=r"$\log_{10}$ risk",
                 xticks=[0, 1, 2], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[0, 1, 2, 3], center=[-2.5, 0.2, 0])
        ax = A.ax
        rate = np.log10([r["rate"] for r in d["rows"]])
        soft = np.log10([r["soft"] for r in d["rows"]])
        cr = VGroup(polyline(ax, s, rate, LOWC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=LOWC) for a, b in zip(s, rate)])
        cs = VGroup(polyline(ax, s, soft, UPC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=UPC) for a, b in zip(s, soft)])
        mle = DashedLine(ax.c2p(-0.1, 3), ax.c2p(2.1, 3), color=GREY_B, stroke_width=2.5)
        ratio = float(np.mean(np.array([r["soft"] / r["rate"] for r in d["rows"]])))
        side = fit_rows(VGroup(
            label(rf"$p = {d['p']}$ means, \ $s$ of them large", font_size=22),
            label(r"grey: \ no thresholding: \ risk $p$", font_size=22, color=GREY_B),
            label(r"red: \ the rate $s \log(ep/s)$", font_size=22, color=LOWC),
            label(r"blue: \ soft thresholding, \ simulated", font_size=22, color=UPC),
            label(rf"about {ratio:.1f} times the rate, \ for every $s$", font_size=22, color=HYPC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> A thousand means, with s of them large. <bookmark mark='b'/> Using the data as they are costs a risk of p, a thousand. <bookmark mark='c'/> The minimax rate s log of e p over s is far smaller when the vector is sparse. <bookmark mark='d'/> Soft thresholding, simulated at the chosen large-signal vectors, rather than an independently verified supremum over all sparse vectors, <bookmark mark='e'/> tracks the rate at about {say(ratio, 1)} times it, for every sparsity level: the selected simulation tracks the rate proxy. The minimax upper theorem requires separate uniform risk control."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"blue simulated: \ 400 samples")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(mle), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cr), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cs), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
