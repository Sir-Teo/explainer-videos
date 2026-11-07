from __future__ import annotations

import numpy as np

from videos.stats.stats48.common import *  # noqa: F403


class Concentration(VoiceoverScene):
    def construct(self):
        self.card()
        self.bernstein()
        self.talagrand()
        self.chart()
        self.lowvar()
        self.uses()

    def card(self):
        card = chapter_card(6, r"Maximal inequalities", r"How tightly the supremum sits around its mean", lit=(1996,), part=PART)
        with self.voiceover("Chapter six. Maximal inequalities: how tightly the supremum sits around its mean."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def bernstein(self):
        rows = [
            cmath(r"\text{one } f, \ |f - Pf| \le b, \ \mathrm{Var} f = \sigma^2", r":", r"P\big(\textstyle\sum (f(X_i) - Pf) \ge t\big) \le \exp\Big(-\dfrac{t^2}{2(n\sigma^2 + bt/3)}\Big)", font_size=28),
            cmath(r"Z = \sup_{f \in \mathcal F} \textstyle\sum_i (f(X_i) - Pf)", r":", r"\text{the expectation } EZ \text{ by chaining; \ the fluctuation?}", font_size=30),
            cmath(r"\text{McDiarmid (Part 44)}", r":", r"P(Z - EZ \ge t) \le e^{-2t^2/n}: \ \text{blind to the variance}", font_size=30),
            cmath(r"\text{wanted}", r":", r"\text{Bernstein's inequality, \ uniformly over the class}", font_size=32),
        ]
        rows[0][-1].set_color(EMPC)
        rows[2][-1].set_color(BADC)
        rows[3][-1].set_color(GOODC)
        whys = [why(r"Bernstein (1924)"), why(r"two problems: \ mean and spread"), why(r"bounded differences"), why(r"Talagrand's question")]
        with self.voiceover(
            "<bookmark mark='a'/> For a single bounded function, Bernstein's inequality bounds the tail of a centred sum: Gaussian with variance n sigma squared for moderate deviations, exponential for large ones. <bookmark mark='b'/> For the supremum over a class there are two separate problems: the size of its expectation, which chaining controls, and how far it fluctuates around that expectation. <bookmark mark='c'/> Part forty-four's McDiarmid inequality handles the fluctuation, for the indicator classes used here, since changing one observation moves the supremum of centred sums by at most one. But it cannot see the variance: it treats every function as if it had the largest possible spread. <bookmark mark='d'/> What one wants is Bernstein's inequality, holding uniformly over the class, with the largest variance in the class in place of sigma squared."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def talagrand(self):
        rows = [
            cmath(r"\sigma^2 \ge \sup_f \mathrm{Var} f, \ v = n\sigma^2 + 2b\,EZ", r":", r"P\big(Z \ge EZ + \sqrt{2xv} + bx/3\big) \le e^{-x}", font_size=30),
            cmath(r"\text{read it as}", r":", r"Z-EZ\le \sqrt{2x(n\sigma^2+2bEZ)}+bx/3\ \text{with probability }\ge1-e^{-x}", font_size=32),
            cmath(r"\text{the class enters only through}", r":", r"EZ \ \text{and} \ \sigma^2", font_size=34),
            cmath(r"\text{KS}", r":", r"P(\sqrt n D_n > t) \le 2 e^{-2t^2} \ \text{(DKW, \ Massart's constant)}", font_size=32),
        ]
        rows[0][-1].set_color(GOODC)
        rows[2][-1].set_color(CLASSC)
        whys = [why(r"Talagrand (1996); \ Bousquet's constants (2002)"), why(r"Bernstein, \ uniformly"), why(r"concentration is free"), why(r"Dvoretzky--Kiefer--Wolfowitz (1956); \ Massart (1990)")]
        heading = label('Bousquet bounds moderate and large deviations', font_size=34).move_to([0, 3.3, 0])
        if heading.width > 12.5: heading.width = 12.5
        self.add(heading)
        with self.voiceover(
            "<bookmark mark='a'/> Michel Talagrand proved exactly that in 1996, and Olivier Bousquet in 2002 found the sharp constants. With sigma squared the largest variance in the class, and v equal to n sigma squared plus twice b times the expected supremum, the supremum exceeds its mean by more than root two x v plus b x over three with probability at most e to the minus x. <bookmark mark='b'/> Read it as: the supremum is its expectation plus a fluctuation of the order of the largest single standard deviation, with Bernstein-type tails: a Gaussian moderate-deviation term and a linear large-deviation term. <bookmark mark='c'/> The class's complexity enters only through the expectation and the largest variance. The concentration around the mean comes for free. <bookmark mark='d'/> For the Kolmogorov statistic there is an even sharper special result, the Dvoretzky–Kiefer–Wolfowitz inequality, with the constant two found by Pascal Massart in 1990: the tail of root n D n is at most twice e to the minus two t squared, for every n."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def chart(self):
        d = load("conc")
        ts = np.asarray(d["ts"])
        A = axes([0, 16], [-4, 0.1], x_length=7.4, y_length=4.4, xlabel=r"$t$", ylabel=r"$\log_{10} P(nD_n - E\,nD_n \ge t)$",
                 xticks=[0, 4, 8, 12, 16], yticks=[-4, -3, -2, -1, 0], center=[-2.5, 0.2, 0])
        ax = A.ax
        lg = lambda v: np.log10(np.maximum(np.asarray(v, float), 1e-5))  # noqa: E731
        ok = np.asarray(d["sim"]) > 0
        cs = clip_curve(ax, ts[ok], lg(np.asarray(d["sim"])[ok]), EMPC, 4, ymin=-4, ymax=0.1)
        cb = clip_curve(ax, ts, lg(d["bous"]), BOUNDC, 3.5, ymin=-4, ymax=0.1)
        cm = clip_curve(ax, ts, lg(d["mcd"]), BADC, 3.5, ymin=-4, ymax=0.1)
        cd = clip_curve(ax, ts, lg(d["dkw"]), GOODC, 3.5, ymin=-4, ymax=0.1)
        side = fit_rows(VGroup(
            label(rf"$n = {d['n']}$, \ uniform data, \ $E\,nD_n$ = {d['ez']:.2f}", font_size=22),
            label(r"blue: \ simulated, \ 40,000 samples", font_size=22, color=EMPC),
            label(r"red: \ McDiarmid, \ $e^{-2t^2/n}$", font_size=22, color=BADC),
            label(r"purple: \ Bousquet, \ $\sigma^2 = 1/4$", font_size=22, color=BOUNDC),
            label(r"green: \ DKW, \ for the KS class alone", font_size=22, color=GOODC),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The tails for the Kolmogorov statistic, a hundred uniform observations, on a log scale. The estimated expected value of n D n is {say(d['ez'], 2)}. <bookmark mark='b'/> In blue, the simulated chance of exceeding that by t. <bookmark mark='c'/> McDiarmid's bound in red, <bookmark mark='d'/> Bousquet's in purple. For this class the largest variance is a quarter, as large as it can be, so Bousquet has nothing to exploit, and his bound is the weaker of the two here. <bookmark mark='e'/> And in green the Dvoretzky–Kiefer–Wolfowitz bound, which uses everything about this particular class, and is tightest here. We estimated the centring expectation from forty thousand samples; these plotted plug-in comparisons are not certified finite-sample bounds."
        ) as vo:
            self.play(FadeIn(A), FadeIn(simulated_tag(r"simulated; \ bounds evaluated at estimated $EZ$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cm), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cb), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(cd), FadeIn(side[4]))
        self.clear_scene()

    def lowvar(self):
        d = load("conc")
        lo, fu = d["low"], d["full"]
        rows = [[r"class", r"$\sigma^2$", r"simulated", r"Bousquet", r"McDiarmid"],
                [r"all half-lines", r"0.25", f"{fu['sim95']:.2f}", f"{fu['b95']:.2f}", f"{fu['m95']:.2f}"],
                [rf"half-lines with $t \le {d['q']}$", f"{d['q'] * (1 - d['q']):.4f}", f"{lo['sim95']:.2f}", f"{lo['b95']:.2f}", f"{lo['m95']:.2f}"]]
        tab = table_rows(rows, font_size=30, col_buff=0.8, row_buff=0.4, colors=[GREY_B, None, GOODC])
        if tab.width > 12.6:
            tab.width = 12.6
        tab.move_to([0, 0.9, 0])
        foot = label(r"95\% upper points of $Z - EZ$, \ $Z = n \sup_{\mathcal F} |P_n f - Pf|$, \ $n = 100$", font_size=24, color=GREY_A).move_to([0, -1.3, 0])
        foot2 = label(r"a small-variance class: \ Bousquet is twice as tight as McDiarmid; \ the localized classes of chapter 9 are like this", font_size=24, color=GOODC).move_to([0, -2.1, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Bousquet's bound earns its keep when the variances are small. Take the half-lines that end before two percent of the probability: every function in the class has variance below two percent. <bookmark mark='b'/> The table compares simulated fluctuation quantiles with bounds evaluated at estimated expectations. It illustrates the variance effect, with centring Monte Carlo error. For all half-lines, the simulated point is {say(fu['sim95'], 1)}; McDiarmid says {say(fu['m95'], 1)} and Bousquet {say(fu['b95'], 1)}. For the small-variance class the simulated point drops to {say(lo['sim95'], 1)}. McDiarmid cannot tell the difference and still says {say(lo['m95'], 1)}, but Bousquet drops to {say(lo['b95'], 1)}. <bookmark mark='c'/> Classes like this, functions near the truth with small variance, are exactly what the rate theorems of chapter nine and the oracle inequalities of learning theory need."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(simulated_tag(r"40,000 samples; \ plug-in expectation, Monte Carlo error")))
            vo.wait_until("b")
            self.play(FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(foot2))
        self.clear_scene()

    def uses(self):
        rows = fit_rows(VGroup(
            label(r"what concentration buys:", font_size=28, color=GREY_A),
            label(r"bounded measurable class: mean GC + concentration gives a.s. GC", font_size=26, color=GOODC),
            label(r"finite-sample bands: \ DKW gives $\pm\sqrt{\log(2/\alpha)/(2n)}$ for every $n$ \ (chapter 11)", font_size=26, color=EMPC),
            label(r"oracle inequalities for ERM and the lasso: \ risk $\le$ best in class $+$ complexity", font_size=26, color=CLASSC),
            label(r"the rest of the theory reduces to bounding $E\,\|P_n - P\|_{\mathcal F}$", font_size=26, color=S.ACCENT),
        ), 12.4, 0.55, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> What concentration buys. <bookmark mark='b'/> It turns statements about expectations into almost sure ones: for a measurable uniformly bounded class, convergence in mean combines with bounded-difference concentration and Borel–Cantelli to give almost sure convergence. <bookmark mark='c'/> It gives honest finite-sample bands, like the DKW band, valid separately at each fixed n, rather than simultaneously over all sampling times, which chapter eleven tests on the Coverage Board. <bookmark mark='d'/> And it underlies oracle inequalities for empirical risk minimization and the lasso. <bookmark mark='e'/> With concentration in hand, the whole theory comes down to bounding one number, the expected supremum, by symmetrization and chaining."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
