from __future__ import annotations

import numpy as np

from videos.stats.stats50.common import *  # noqa: F403


class LeCam(VoiceoverScene):
    def construct(self):
        self.card()
        self.reduction()
        self.proof()
        self.picture()
        self.divergences()
        self.density()
        self.functional()
        self.chart()

    def card(self):
        card = chapter_card(3, r"Le Cam's two-point method", r"If two answers look alike, \ no one can tell them apart", part=PART)
        with self.voiceover("Chapter three. Le Cam's two-point method: if two answers look alike, no one can tell them apart."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def reduction(self):
        rows = [
            cmath(r"\theta_0, \theta_1 \in \Theta, \ \ |\theta_0 - \theta_1| = 2\delta", r":", r"\text{two hypotheses}", font_size=34),
            cmath(r"\text{any } \hat\theta", r":", r"\text{test } \psi = \mathbf 1\{\hat\theta \text{ nearer } \theta_1\}; \ \text{ an error forces } |\hat\theta - \theta| \ge \delta", font_size=30),
            cmath(r"\max_{j} E_j (\hat\theta - \theta_j)^2", r"\ge", r"\frac{\delta^2}{2}\,\big(1 - \mathrm{TV}(P_0^n, P_1^n)\big)", font_size=34),
            cmath(r"\text{the game}", r":", r"\text{make } \delta \text{ large and TV small: \ far apart, \ hard to tell}", font_size=32),
        ]
        rows[2][-1].set_color(LOWC)
        rows[3][-1].set_color(HYPC)
        whys = [why(r"inside the parameter set"), why(r"estimation $\Rightarrow$ testing"), why(r"the best test's error: \ Part 46"), why(r"the trade-off")]
        with self.voiceover(
            "<bookmark mark='a'/> Lucien Le Cam's method needs only two hypotheses, two parameter values in the set, a "
            "distance two delta apart. <bookmark mark='b'/> Any estimator defines a test: decide for whichever hypothesis it "
            "lands nearer. Whenever that test errs, the estimator is at least delta from the truth. <bookmark mark='c'/> "
            "And the best possible test between two laws errs with total probability one minus their total variation "
            "distance, by Part forty-six. So the worst-case risk of any estimator is at least delta squared over two times "
            "one minus the total variation between the two samples' laws. <bookmark mark='d'/> The game is to choose the two "
            "hypotheses as far apart as possible while keeping their data nearly indistinguishable."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def proof(self):
        rows = [
            cmath(r"\max_j E_j \ell", r"\ge", r"\tfrac12 (E_0 \ell + E_1 \ell): \ \text{a max beats an average}", font_size=34),
            cmath(r"\phantom{\max}", r"\ge", r"\tfrac{\delta^2}{2}\,\big(P_0(\psi = 1) + P_1(\psi = 0)\big)", font_size=34),
            cmath(r"\inf_\psi \big(P_0(\psi = 1) + P_1(\psi = 0)\big)", r"=", r"1 - \mathrm{TV}(P_0, P_1)", font_size=34),
            cmath(r"\text{the best test}", r":", r"\text{Neyman--Pearson's likelihood ratio, \ Part 46}", font_size=34),
        ]
        rows[2][-1].set_color(LOWC)
        whys = [why(r"a two-point prior"), why(r"an error costs at least $\delta^2$"), why(r"the sum of errors"), why(r"reject when $p_1 > p_0$")]
        with self.voiceover(
            "<bookmark mark='a'/> The proof takes four lines. The worst of two risks is at least their average, which is the "
            "Bayes risk of a prior putting half its mass on each point. <bookmark mark='b'/> Whenever the induced test errs, "
            "the loss is at least delta squared, so the average risk is at least delta squared over two times the sum of the "
            "test's two error probabilities. <bookmark mark='c'/> The smallest possible sum of the two errors, over all tests, "
            "is one minus the total variation distance between the laws. <bookmark mark='d'/> It is attained by Part "
            "forty-six's likelihood-ratio test, rejecting when the second density is larger. The lower bound for estimation is "
            "the Neyman–Pearson lemma in disguise."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def picture(self):
        W = LowerBoundPacking(center=(-2.6, -0.2, 0), scale=1.6)
        pts = W.place([[-1.2, 0.0], [1.2, 0.0]], color=HYPC, radius=0.12)
        disc = W.separation(1.2, color=UPC, opacity=0.1)
        conf = W.confusion(0, 1, color=LOWC)
        est = Dot(W._p([0.15, 0.4]), radius=0.1, color=TRUTHC)
        side = fit_rows(VGroup(
            label(r"gold: \ $\theta_0$ and $\theta_1$, \ $2\delta$ apart", font_size=22, color=HYPC),
            label(r"blue discs: \ radius $\delta$, \ disjoint", font_size=22, color=UPC),
            label(r"white: \ an estimate: \ far from at least one", font_size=22, color=TRUTHC),
            label(r"red dashed: \ their data are nearly the same law", font_size=22, color=LOWC),
            label(r"so with real probability, \ it is far from the truth", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> On the workbench: two hypotheses, two delta apart. <bookmark mark='b'/> Around each, a disc "
            "of radius delta; the discs do not overlap. <bookmark mark='c'/> Wherever an estimate lands, it is outside at "
            "least one disc, at least delta from one of the two candidates. <bookmark mark='d'/> If the data cannot reliably "
            "say which candidate is true, <bookmark mark='e'/> then with probability bounded away from zero the estimate is "
            "far from the truth. That is the whole idea."
        ) as vo:
            self.play(FadeIn(exact_tag(r"the lower-bound workbench")))
            vo.wait_until("a")
            self.play(FadeIn(pts), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(disc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(est), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(conf), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def divergences(self):
        d = load("lecam")
        rows = [[r"$N(0,1)$ vs.\ $N(d,1)$", r"TV", r"Hellinger$^2$", r"KL", r"Pinsker's $\sqrt{\mathrm{KL}/2}$"]]
        for r in d["div"]:
            rows.append([f"$d = {r['d']:g}$", f"{r['tv']:.3f}", f"{r['h2']:.3f}", f"{r['kl']:.3f}", f"{r['pinsker']:.3f}"])
        tab = table_rows(rows, font_size=28, col_buff=0.8, row_buff=0.34, colors=[GREY_B] + [None] * 5)
        tab.move_to([0, 0.8, 0])
        for i in range(1, 6):
            tab[i][1].set_color(LOWC)
            tab[i][4].set_color(HYPC)
        foot = label(r"for $n$ observations: \ $\mathrm{KL}(P^n, Q^n) = n\,\mathrm{KL}(P, Q)$, \ $1 - H^2$ multiplies: \ products are easy", font_size=24, color=GREY_A).move_to([0, -1.6, 0])
        foot2 = label(r"$H^2 \le \mathrm{TV} \le \sqrt{2H^2}$, \ \ $\mathrm{TV} \le \sqrt{\mathrm{KL}/2}$: \ bound TV through the others", font_size=24, color=HYPC).move_to([0, -2.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Total variation is what the bound needs, but it is awkward for samples of n. Two other "
            "divergences behave well: the Kullback–Leibler divergence adds up over independent observations, and one minus "
            "the squared Hellinger distance multiplies. For two normals a distance d apart, the table compares them. "
            "<bookmark mark='b'/> Pinsker's inequality, total variation at most the root of half the Kullback–Leibler "
            "divergence, and Le Cam's inequalities between total variation and Hellinger, let us bound one through the "
            "other. In practice: keep n times the Kullback–Leibler divergence of order one, and the total variation stays "
            "bounded away from one."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(foot), FadeIn(exact_tag(r"exact")))
            vo.wait_until("b")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def density(self):
        rows = [
            cmath(r"f_0 = \text{a smooth density}", r",", r"f_1 = f_0 + h\, b\big(\tfrac{x - x_0}{w}\big) - h\, b\big(\tfrac{x - x_1}{w}\big)", font_size=30),
            cmath(r"f_1 \in \text{Hoelder}(s, L)", r"\Leftarrow", r"h = L\, w^s", font_size=34),
            cmath(r"|f_1(x_0) - f_0(x_0)| = h", r",", r"n\, \chi^2(f_1, f_0) \asymp n\, h^2 w = n\, w^{2s + 1}", font_size=32),
            cmath(r"w \asymp n^{-1/(2s+1)}", r"\Rightarrow", r"\text{risk} \gtrsim h^2 = w^{2s} \asymp n^{-2s/(2s + 1)}", font_size=34),
        ]
        rows[3][-1].set_color(LOWC)
        whys = [why(r"add a bump, \ remove one elsewhere"), why(r"thin bumps must be low"), why(r"separation vs.\ information"), why(r"Farrell's rate")]
        with self.voiceover(
            "<bookmark mark='a'/> Here is Farrell's lower bound by the two-point method. Take a smooth density and perturb it "
            "with a bump of height h and width w at the point of interest, removing the same mass elsewhere so it stays a "
            "density. <bookmark mark='b'/> For the perturbed density to stay in the Hölder class with s derivatives, a bump "
            "of width w can have height at most of order w to the s. <bookmark mark='c'/> The two densities differ by h at "
            "the point, while n times their chi-square distance, which controls the total variation of the samples, is of "
            "order n h squared w, that is n w to the two s plus one. <bookmark mark='d'/> Choose w so that this is of order "
            "one: w of order n to the minus one over two s plus one. Then the risk is at least h squared, of order n to the "
            "minus two s over two s plus one. For two derivatives, n to the minus four fifths: the kernel estimate's rate is "
            "the best possible."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def functional(self):
        rows = [
            cmath(r"\psi(P) \text{ smooth}, \ \text{a submodel } P_t", r":", r"|\psi(P_t) - \psi(P)| \approx t\,|\langle \phi^*, s\rangle|, \ \ n\,\mathrm{KL} \approx n t^2 \|s\|^2/2", font_size=30),
            cmath(r"t = 1/\sqrt n", r"\Rightarrow", r"\text{risk} \gtrsim 1/n: \ \text{root-}n \text{ is the best possible}", font_size=32),
            cmath(r"\text{the modulus of continuity}", r":", r"\omega(\epsilon) = \sup\{|\psi(P) - \psi(Q)| : H(P, Q) \le \epsilon\}", font_size=32),
            cmath(r"\text{Donoho \& Liu (1991)}", r":", r"\text{the minimax rate is } \omega(n^{-1/2})^2, \ \text{for linear functionals}", font_size=32),
        ]
        rows[1][-1].set_color(LOWC)
        rows[3][-1].set_color(HYPC)
        whys = [why(r"Part 49's pathwise derivative"), why(r"the two-point bound at root-$n$"), why(r"how fast $\psi$ can move"), why(r"one number decides the rate")]
        with self.voiceover(
            "<bookmark mark='a'/> The two-point method also explains root n. For a smooth functional, move the law a distance "
            "t along a submodel: the functional moves by about t times its pathwise derivative, while n times the "
            "Kullback–Leibler divergence grows like n t squared. <bookmark mark='b'/> With t of order one over root n the two "
            "laws are hard to tell apart, and the risk is at least of order one over n: root n is the best possible rate, the "
            "lower half of Part forty-nine's story. <bookmark mark='c'/> In general what matters is the modulus of continuity: "
            "how far the functional can move when the data's law moves by epsilon in Hellinger distance. <bookmark "
            "mark='d'/> David Donoho and Richard Liu showed in 1991 that for linear functionals the minimax rate is the modulus "
            "at one over root n, squared. A density at a point has a modulus that grows faster than linearly in epsilon, which "
            "is exactly why it cannot be estimated at root n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("lecam")
        ln = np.log10(d["ns"])
        A = axes([2.2, 5.0], [-6.2, -2.4], x_length=7.4, y_length=4.4, xlabel=r"$n$ \ (log scale)", ylabel=r"$\log_{10}$ MSE at a point",
                 xticks=[np.log10(250), 3, 4, np.log10(64000)], xfmt=lambda v: f"{10 ** v:,.0f}", yticks=[-6, -5, -4, -3], center=[-2.5, 0.2, 0])
        ax = A.ax
        up = VGroup(polyline(ax, ln, np.log10(d["upper"]), UPC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=UPC) for a, b in zip(ln, np.log10(d["upper"]))])
        lo = VGroup(polyline(ax, ln, np.log10(d["lower"]), LOWC, 4), *[Dot(ax.c2p(a, b), radius=0.08, color=LOWC) for a, b in zip(ln, np.log10(d["lower"]))])
        gap = float(np.mean(np.log10(d["upper"]) - np.log10(d["lower"])))
        side = fit_rows(VGroup(
            label(r"a smooth density at a point, \ $s = 2$", font_size=22),
            label(r"blue: \ a kernel estimate's simulated MSE", font_size=22, color=UPC),
            label(r"red: \ Le Cam's two-point lower bound", font_size=22, color=LOWC),
            label(r"nearly parallel: \ both $\asymp n^{-4/5}$", font_size=22, color=HYPC),
            label(rf"the gap: \ a constant, \ about $10^{{{gap:.1f}}}$", font_size=22, color=GREY_A),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Both halves on one chart. <bookmark mark='b'/> In blue, a kernel estimator's simulated mean "
            f"squared error at a point. <bookmark mark='c'/> In red, the two-point lower bound, optimized over the bump's "
            f"width. <bookmark mark='d'/> The lines are nearly parallel: the bound has slope exactly minus four fifths, and the "
            f"estimator's slope is approaching it, so the rate is pinned down. "
            f"<bookmark mark='e'/> The gap between them is a constant factor, about ten to the {say(gap, 1)}. Two-point bounds "
            f"are crude in their constants, and Pinsker's exact constant is the exception, not the rule."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"blue simulated; \ red exact")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(up), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lo), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
