from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class RaoBlackwell(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.tanks()
        self.lehmann()
        self.table()
        self.absurd()
        self.lesson()

    def card(self):
        card = chapter_card(6, r"Rao--Blackwell and Lehmann--Scheff\'e", r"Averaging over what does not matter", lit=(1947, 1950), part=PART)
        with self.voiceover("Chapter six. Rao–Blackwell and Lehmann–Scheffé: averaging over what does not matter."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def theorem(self):
        rows = [
            cmath(r"\delta^*(T)", r"=", r"E[\delta(X) \mid T]: \ \text{free of } \theta, \text{ so a statistic}", font_size=32),
            cmath(r"E_\theta \delta^*", r"=", r"E_\theta \delta: \ \text{same bias}", font_size=34),
            cmath(r"\mathrm{Var}\, \delta", r"=", r"\mathrm{Var}\, \delta^* + E\,\mathrm{Var}(\delta \mid T) \ \ge \ \mathrm{Var}\, \delta^*", font_size=32),
            cmath(r"L(\theta, \cdot) \text{ convex}", r"\Rightarrow", r"R(\theta, \delta^*) \le R(\theta, \delta) \ \text{(Jensen)}", font_size=32),
        ]
        rows[0][-1].set_color(S.ACCENT)
        rows[2][-1].set_color(ADMC)
        rows[3][-1].set_color(ADMC)
        whys = [why(r"sufficiency is used here"), why(r"the tower property"), why(r"Part 44's variance decomposition"), why(r"Rao (1945), \ Blackwell (1947)")]
        with self.voiceover(
            "<bookmark mark='a'/> Take any estimator and average it over the data given a sufficient statistic. Because T "
            "is sufficient, that conditional expectation does not depend on theta, so it is a genuine estimator, computable "
            "from data. <bookmark mark='b'/> By the tower property it has the same expectation, hence the same bias. "
            "<bookmark mark='c'/> By the conditional variance decomposition its variance is smaller, by the average "
            "conditional variance that was thrown away. <bookmark mark='d'/> And for any convex loss, Jensen's inequality "
            "gives smaller risk at every theta. That is the theorem of C. R. Rao, 1945, and David Blackwell, 1947: under "
            "convex loss, only functions of a sufficient statistic are worth considering."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def tanks(self):
        d = load("suff")
        N, k = d["N"], d["k"]
        A = axes([0, 310], [0, 620], x_length=7.4, y_length=4.4, xlabel=r"$M$, \ the largest serial seen", ylabel=r"$2X_1 - 1$",
                 xticks=[0, 100, 200, 300], yticks=[0, 300, 600], center=[-2.5, 0.2, 0])
        ax = A.ax
        pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.035, color=MLEC, fill_opacity=0.6) for a, b in zip(d["scatter_M"], d["scatter_one"])])
        line = polyline(ax, d["line_m"], d["line"], ADMC, 5)
        truth = DashedLine(ax.c2p(0, N), ax.c2p(310, N), color=GREY_B, stroke_width=2)
        side = fit_rows(VGroup(
            label(rf"$N = {N}$ tanks, \ $k = {k}$ serials captured", font_size=22),
            label(r"blue: \ $2X_1 - 1$ from the first serial alone, \ unbiased", font_size=22, color=MLEC),
            label(r"given $M = m$: \ $X_1 = m$ w.p.\ $1/k$, \ else uniform below", font_size=22, color=GREY_A),
            label(r"green: \ $E[2X_1 - 1 \mid M] = M\,\tfrac{k + 1}{k} - 1$", font_size=22, color=ADMC),
            label(rf"SD: \ {d['sd']['one']:.0f} \ $\to$ \ {d['sd']['umvue']:.0f}", font_size=22, color=S.ACCENT),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Part nine's tanks, Rao–Blackwellized in a picture. There are {N} tanks and we capture "
            f"{k} serial numbers. <bookmark mark='b'/> A silly unbiased estimator uses only the first serial seen: twice it, "
            f"minus one. Each blue dot is one simulated capture, plotted against the largest serial in that capture. "
            f"<bookmark mark='c'/> The maximum is sufficient. Given that it equals m, the first serial is m itself with "
            f"probability one over k, and otherwise uniform below m. <bookmark mark='d'/> Averaging gives the green line, m "
            f"times k plus one over k, minus one: the vertical scatter at each m collapses onto its mean. <bookmark "
            f"mark='e'/> The standard deviation falls from {d['sd']['one']:.0f} to {d['sd']['umvue']:.0f}, and the "
            f"estimator is still unbiased."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 600 captures; \ the line exact")))
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.003), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(line), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def lehmann(self):
        rows = [
            cmath(r"T \text{ complete sufficient}", r",", r"\ g(T) \text{ unbiased for } \tau(\theta)", font_size=32),
            cmath(r"g_1(T), g_2(T) \text{ unbiased}", r"\Rightarrow", r"E_\theta(g_1 - g_2) = 0 \ \forall\theta \Rightarrow g_1 = g_2", font_size=30),
            cmath(r"\delta \text{ any unbiased}", r"\Rightarrow", r"E[\delta \mid T] \text{ unbiased, a function of } T, \text{ so } = g(T)", font_size=30),
            cmath(r"\Rightarrow", r"\;", r"R(\theta, g) \le R(\theta, \delta) \ \forall \theta, \delta: \ \text{the UMVUE, for every convex loss}", font_size=30),
        ]
        rows[3][-1].set_color(ADMC)
        whys = [why(r"the setting"), why(r"completeness: \ uniqueness"), why(r"Rao--Blackwell: \ improvement"), why(r"Lehmann--Scheff\'e (1950)")]
        with self.voiceover(
            "<bookmark mark='a'/> Lehmann and Scheffé's theorem adds completeness. Suppose T is complete and sufficient, "
            "and some function of T is unbiased for the quantity we want. <bookmark mark='b'/> Then it is the only one: two "
            "unbiased functions of T differ by a function with mean zero everywhere, which completeness forces to vanish. "
            "<bookmark mark='c'/> Now take any unbiased estimator at all. Rao–Blackwellizing it gives an unbiased function "
            "of T, which must be that same one. <bookmark mark='d'/> So the unbiased function of a complete sufficient "
            "statistic beats every unbiased estimator, at every theta, under every convex loss: the uniformly minimum-"
            "variance unbiased estimator. Part nine stated this; here it is proved."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def table(self):
        d = load("suff")
        sd, sim = d["sd"], d["sim_sd"]
        tab = table_rows([[r"unbiased estimator of $N$", r"exact SD", r"simulated SD", r"simulated mean"],
                          [r"$2X_1 - 1$ \ (one serial)", f"{sd['one']:.1f}", f"{sim['one']:.1f}", f"{d['sim_mean']['one']:.1f}"],
                          [r"$2\bar X - 1$ \ (moments)", f"{sd['mom']:.1f}", f"{sim['mom']:.1f}", f"{d['sim_mean']['mom']:.1f}"],
                          [r"$M(k + 1)/k - 1$ \ (UMVUE)", f"{sd['umvue']:.1f}", f"{sim['umvue']:.1f}", f"{d['sim_mean']['umvue']:.1f}"]],
                         font_size=28, col_buff=0.8, row_buff=0.3, colors=[GREY_A, MLEC, BAYESC, ADMC]).move_to([0, 1.5, 0])
        t = d["tanks"]
        hist = table_rows([[r"Ruggles \& Brodie (1947)", r"serial numbers", r"intelligence", r"German records"]] +
                          [[r["month"], f"{r['stat']:,}", f"{r['intel']:,}", f"{r['records']:,}"] for r in t],
                          font_size=24, col_buff=0.7, row_buff=0.2, colors=[GREY_A, None, None, None]).move_to([0, -1.6, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The three unbiased estimators side by side, for {d['N']} tanks and {d['k']} serials, with "
            f"exact and simulated standard deviations. <bookmark mark='b'/> One serial alone: about {sd['one']:.0f}. "
            f"<bookmark mark='c'/> The method of moments, twice the average serial minus one: {sd['mom']:.0f}. <bookmark "
            f"mark='d'/> The UMVUE: {sd['umvue']:.0f}, best among all unbiased estimators, by Lehmann–Scheffé. <bookmark "
            f"mark='e'/> And the real thing: Richard Ruggles and Henry Brodie's serial-number estimates of monthly German "
            f"tank production, against Allied intelligence and the German records found after the war. The statisticians "
            f"were far closer."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab[0]))
            for k, m_ in enumerate("bcd"):
                vo.wait_until(m_)
                self.play(FadeIn(tab[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(hist), FadeIn(museum_tag(r"Ruggles \& Brodie, \ \emph{JASA} (1947)")))
        self.clear_scene()

    def absurd(self):
        d = load("suff")
        lam = np.asarray(d["lam"])
        a = d["absurd"]
        A = axes([0, 3], [0, 1.05], x_length=7.4, y_length=4.4, xlabel=r"$\lambda$", ylabel=r"MSE for $e^{-2\lambda}$",
                 xticks=[0, 1, 2, 3], yticks=[0, 0.25, 0.5, 0.75, 1], center=[-2.5, 0.2, 0])
        ax = A.ax
        cu = polyline(ax, lam, a["umvue"], INADC, 4)
        ce = polyline(ax, lam, a["even"], MMC, 4)
        cm = polyline(ax, lam, a["mle"], MLEC, 4)
        side = fit_rows(VGroup(
            label(r"$X \sim$ Poisson$(\lambda)$: \ estimate $e^{-2\lambda}$", font_size=22),
            label(r"the only unbiased estimator: \ $(-1)^X$, \ i.e.\ $\pm 1$", font_size=22, color=INADC),
            label(r"the UMVUE, \ and it can say $-1$", font_size=22, color=INADC),
            label(r"gold: \ $\mathbf 1(X \text{ even})$ dominates it", font_size=22, color=MMC),
            label(r"blue: \ the MLE $e^{-2X}$, \ biased, \ far better", font_size=22, color=MLEC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            "<bookmark mark='a'/> But unbiasedness can be absurd. Observe one Poisson count with mean lambda and estimate e "
            "to the minus two lambda: the chance of no events in the next two periods. <bookmark mark='b'/> Expanding the "
            "Poisson probabilities shows that the only unbiased estimator is minus one to the power X: plus one for an even "
            "count, minus one for an odd count. <bookmark mark='c'/> The count is complete and sufficient, so this is the "
            "UMVUE, and it estimates a probability by minus one half of the time. <bookmark mark='d'/> Replacing minus one "
            "by zero, the indicator that X is even, is biased but dominates it everywhere. <bookmark mark='e'/> And the "
            "maximum likelihood estimate, e to the minus two X, is better still across this range. Best among unbiased "
            "estimators can mean best among bad ones."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ Poisson generating functions")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cu), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(ce), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(cm), FadeIn(side[4]))
        self.clear_scene()

    def lesson(self):
        rows = fit_rows(VGroup(
            label(r"Rao--Blackwell: \ always condition on a sufficient statistic \ (convex loss)", font_size=26, color=ADMC),
            label(r"Lehmann--Scheff\'e: \ with completeness, \ the best \emph{unbiased} estimator is unique", font_size=26, color=ADMC),
            label(r"but unbiasedness is a restriction, \ not a virtue: \ it can exclude every sensible rule", font_size=26, color=INADC),
            label(r"chapter 3's $s^2$ and this $(-1)^X$: \ unbiased, \ and inadmissible", font_size=26, color=S.ACCENT),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> The lessons. Rao–Blackwell is a universal improvement: whatever you do, condition on a "
            "sufficient statistic. <bookmark mark='b'/> Lehmann–Scheffé, with completeness, singles out the best unbiased "
            "estimator. <bookmark mark='c'/> But unbiasedness is a restriction on the competition, not a virtue in itself, "
            "and it can exclude every sensible rule. <bookmark mark='d'/> Chapter three's sample variance and this chapter's "
            "minus one to the X are both unbiased and both inadmissible."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
