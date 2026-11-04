from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant1.common import GAUSS, LARGE, PART, REAL, SMALL, TAIL, VOL, load

MODELS = (("iid", r"iid normal", GAUSS), ("garch", r"GARCH(1,1), normal shocks", VOL),
          ("garch_t5", r"GARCH(1,1), $t_5$ shocks", TAIL))


class Research(VoiceoverScene):
    def construct(self):
        t = load("vr_theory")
        self.card()
        self.iid()
        self.hetero(t)
        self.size(t)
        self.shape(t)
        self.power(t)
        self.data(load("vr"))
        self.open_problems()
        self.question()

    def card(self):
        c = research_card(r"The variance ratio's law", r"How far can VR$(q)$ stray from one when the walk is true?",
                          part=PART)
        with self.voiceover("For the researcher: the theorem behind Chapter 4's test. How far can a variance ratio "
                            "stray from one when prices really are a random walk, and what changes when volatility "
                            "clusters?"):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def iid(self):
        rows = [cmath(r"\operatorname{VR}(q) - 1", r"\approx", r"2\textstyle\sum_{k=1}^{q-1}\big(1 - \tfrac kq\big)\,\hat\rho_k",
                      font_size=32, colors={r"\operatorname{VR}(q) - 1": REAL}),
                cmath(r"\sqrt n\,(\hat\rho_1, \dots, \hat\rho_{q-1})", r"\Rightarrow", r"N(0, I)", font_size=32,
                      colors={r"\sqrt n\,(\hat\rho_1, \dots, \hat\rho_{q-1})": QC.IDEA}),
                cmath(r"\sqrt n\,\big(\operatorname{VR}(q) - 1\big)", r"\Rightarrow",
                      r"N\Big(0,\ 4\textstyle\sum_{k=1}^{q-1}\big(1 - \tfrac kq\big)^2\Big)", font_size=32,
                      colors={r"\sqrt n\,\big(\operatorname{VR}(q) - 1\big)": REAL}),
                cmath(r"4\textstyle\sum_{k=1}^{q-1}\big(1 - \tfrac kq\big)^2", r"=", r"\frac{2(2q - 1)(q - 1)}{3q}",
                      font_size=32, colors={r"4\textstyle\sum_{k=1}^{q-1}\big(1 - \tfrac kq\big)^2": QC.GAIN})]
        whys = [why(r"Chapter 4: the variance ratio is a weighted sum of sample autocorrelations (exactly, up to "
                    r"$O_p(1/n)$ terms from the means)"),
                why(r"Bartlett (1946): for iid increments with a finite fourth moment, the scaled sample autocorrelations "
                    r"are asymptotically independent standard normals"),
                why(r"a fixed linear combination of independent normals is normal, with the sum of the squared weights "
                    r"as its variance"),
                why(r"$\sum_{j=1}^{q-1} j^2 = (q-1)q(2q-1)/6$ with $j = q - k$: Lo and MacKinlay's (1988) iid variance; "
                    r"for $q = 2$, 1; for $q = 16$, about 9.7")]
        step = ladder(self, rows, whys, keep=4, top=2.9, x=-0.3, buff=0.42, edge=6.9)
        with self.voiceover(
            "The proof takes four lines. <bookmark mark='a'/> Chapter 4 showed the variance ratio minus one is a "
            "weighted sum of sample autocorrelations, with weights falling from the first lag to the last. <bookmark "
            "mark='b'/> If increments are independent and identically distributed, with a finite fourth moment, "
            "Bartlett's theorem says the sample autocorrelations, scaled by root n, behave like independent standard "
            "normals. <bookmark mark='c'/> So the variance ratio is asymptotically normal, with variance the sum of "
            "its squared weights. <bookmark mark='d'/> That sum has a closed form: two times two q minus one, times q "
            "minus one, over three q. One for q of two; almost ten for q of sixteen. Divide by the sample size, take "
            "the square root, and that is the standard error Lo and MacKinlay used."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
        self.wait(0.5)
        self.clear_scene()

    def hetero(self, t):
        rows = [cmath(r"\mathbb E[\varepsilon_t \mid \mathcal F_{t-1}]", r"=", r"0,\quad \mathbb E[\varepsilon_t^2 \mid "
                      r"\mathcal F_{t-1}] = \sigma_t^2\ \text{varies}", font_size=30,
                      colors={r"\mathbb E[\varepsilon_t \mid \mathcal F_{t-1}]": VOL}),
                cmath(r"\sqrt n\,\hat\rho_k", r"\Rightarrow", r"N(0, \delta_k),\quad \delta_k = \frac{\mathbb E[\varepsilon_t^2"
                      r"\varepsilon_{t-k}^2]}{\sigma^4}", font_size=30, colors={r"\sqrt n\,\hat\rho_k": QC.IDEA}),
                cmath(r"z^*", r"=", r"\sqrt n\,\big(\operatorname{VR}(q) - 1\big)\Big/\sqrt{\textstyle\sum_k \big(2(1 - "
                      r"\tfrac kq)\big)^2\hat\delta_k}", font_size=30, colors={r"z^*": REAL})]
        whys = [why(r"a martingale difference: unpredictable in mean, but its size may be predictable, as Chapter 6 "
                    r"measured"),
                why(r"the martingale-difference central limit theorem: each autocorrelation is still centred at zero, but "
                    r"its variance is $\delta_k$, which exceeds one when large moves follow large moves"),
                why(r"Lo and MacKinlay's heteroskedasticity-robust statistic: estimate each $\delta_k$ from the data "
                    r"(the House's \texttt{stats.variance\_ratio}, \texttt{z\_star})")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-0.3, buff=0.45, edge=6.9)
        delta = np.asarray(t["delta"])
        w_, a_, b_ = t["params"]
        kap = 3 * (1 - (a_ + b_) ** 2) / (1 - (a_ + b_) ** 2 - 2 * a_ ** 2)
        rho1 = a_ * (1 - a_ * b_ - b_ ** 2) / (1 - 2 * a_ * b_ - b_ ** 2)
        ks = np.arange(1, len(delta) + 1)
        th = 1 + (kap - 1) * rho1 * (a_ + b_) ** (ks - 1)
        g = axes([0.5, len(delta) + 0.5], [0.8, max(th.max(), delta.max()) * 1.15], x_length=4.6, y_length=2.2,
                 xlabel=r"lag $k$", ylabel=r"$\delta_k$, GARCH", xticks=[1, 5, 10, 15], yticks=[1, 2, 3, 4],
                 font_size=12).to_corner(DR, buff=0.4)
        ax = g.ax
        one = DashedLine(ax.c2p(0.5, 1), ax.c2p(len(delta) + 0.5, 1), color=GAUSS, stroke_width=1.5)
        thl = curve(ax, ks, th, WHITE, stroke_width=2)
        thlab = note(r"white: theory, $1 + (\kappa - 1)\rho_1(\alpha + \beta)^{k-1}$; dots: 400{,}000 simulated "
                     r"returns", font_size=13, color=GREY_B).next_to(g, UP, buff=0.1)
        dots = VGroup(*[Dot(ax.c2p(k + 1, v), radius=0.05, color=VOL) for k, v in enumerate(delta)])

        with self.voiceover(
            "But Chapter 6 showed that returns are not independent: their size clusters. <bookmark mark='a'/> "
            "Weaken the assumption to a martingale difference, unpredictable in direction but with a size that can "
            "be forecast. <bookmark mark='b'/> Each sample autocorrelation is still centred at zero, but its variance "
            "is now delta k, the correlation of squared moves k periods apart, scaled. With clustering, delta k is "
            "above one: in the House's GARCH model the theory gives four and a half at the first lag, decaying "
            "slowly. Even four hundred thousand simulated returns estimate it at only three, because that estimate's "
            "own variance needs an eighth moment this model does not have. "
            "<bookmark mark='c'/> So Lo and MacKinlay built a second statistic, z star, that estimates every delta "
            "from the data and divides by the right variance."
        ) as vo:
            step(0)
            vo.wait_until("a")
            self.wait(0.1)
            vo.wait_until("b")
            step(1)
            self.play(FadeIn(g), Create(one), Create(thl), FadeIn(thlab), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.1))
            vo.wait_until("c")
            step(2)
        self.wait(0.5)
        self.clear_scene()

    def size(self, t):
        qs = t["q"]
        n_q = len(qs)
        g = axes([-0.6, 3 * n_q - 0.4], [0, 0.4], x_length=10.0, y_length=4.0, xlabel=r"",
                 ylabel=r"rejection rate of a nominal 5\% test, random walk true", xticks=[],
                 yticks=[0, 0.05, 0.1, 0.2, 0.3, 0.4], yfmt=lambda v: rf"{100 * v:.0f}\%", font_size=13).move_to(
            DOWN * 0.3 + LEFT * 0.6)
        ax = g.ax
        nominal = DashedLine(ax.c2p(-0.6, 0.05), ax.c2p(3 * n_q - 0.4, 0.05), color=WHITE, stroke_width=1.5)
        groups, labs = VGroup(), VGroup()
        for i, (m, nm, col) in enumerate(MODELS):
            for j, q in enumerate(qs):
                x0 = i * n_q + j
                for k_, (stat, op) in enumerate((("z", 0.95), ("z_star", 0.45))):
                    v = min(t["size"][m][str(q)][stat], 0.4)
                    y0, y1 = ax.c2p(0, 0)[1], ax.c2p(0, v)[1]
                    groups.add(Rectangle(width=0.34 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]),
                                         height=max(y1 - y0, 0.01), stroke_width=0, fill_color=col,
                                         fill_opacity=op).move_to([ax.c2p(x0 + (k_ - 0.5) * 0.38, 0)[0], (y0 + y1) / 2, 0]))
                labs.add(MathTex(rf"{q}", font_size=18, color=GREY_B).next_to(ax.c2p(x0, 0), DOWN, buff=0.1))
            labs.add(label(nm, font_size=16, color=col).next_to(ax.c2p(i * n_q + (n_q - 1) / 2, 0), DOWN, buff=0.45))
        leg = VGroup(label(r"solid: iid $z$", font_size=17), label(r"pale: robust $z^*$", font_size=17)).arrange(
            RIGHT, buff=0.4).to_edge(UP, buff=0.4)
        foot = note(rf"{t['M']} simulated paths of {t['n']} returns each; GARCH $(\omega, \alpha, \beta) = "
                    rf"({t['params'][0]}, {t['params'][1]}, {t['params'][2]})$; bars at $q$ = " + ", ".join(map(str, qs)),
                    font_size=15, color=GREY_B).to_edge(DOWN, buff=0.2)
        g_s, gt_s = t["size"]["garch"], t["size"]["garch_t5"]
        with self.voiceover(
            "Does it matter? Simulate. <bookmark mark='a'/> Two thousand paths of fifteen hundred returns each, the "
            "length of thirty years of weekly data, with the walk true. For independent normal returns, both tests "
            "reject at their nominal five percent. <bookmark mark='b'/> With clustered volatility, the iid test rejects a true "
            "random walk about one time in six, and with fat-tailed shocks one time in four, at every horizon. The "
            "robust test stays at five or six percent."
        ) as vo:
            self.play(FadeIn(g), Create(nominal), FadeIn(leg), FadeIn(foot))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in groups[:2 * n_q]], lag_ratio=0.05),
                      FadeIn(labs[:n_q + 1]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in groups[2 * n_q:]], lag_ratio=0.05),
                      FadeIn(labs[n_q + 1:]))
        self.wait(0.4)
        self.clear_scene()

    def shape(self, t):
        e = np.linspace(-6, 6, 41)
        c = (e[:-1] + e[1:]) / 2
        g = axes([-6, 6], [0, 0.45], x_length=8.0, y_length=3.8, xlabel=r"test statistic, $q = 4$",
                 ylabel=r"density", xticks=[-4, -2, 0, 2, 4], yticks=[], font_size=13).move_to(LEFT * 1.2 + DOWN * 0.3)
        ax = g.ax
        xs = np.linspace(-6, 6, 300)
        nrm = curve(ax, xs, np.exp(-xs ** 2 / 2) / np.sqrt(2 * np.pi), WHITE, stroke_width=2.5)
        lines = VGroup()
        for key, col in (("z", VOL), ("z_star", QC.IDEA)):
            h = np.asarray(t["z_q4"]["garch"][key], float)
            h = h / h.sum() / (e[1] - e[0])
            lines.add(curve(ax, c, h, col, stroke_width=3))
        leg = legend([(WHITE, r"$N(0, 1)$"), (VOL, rf"iid $z$ under GARCH, sd {t['z_q4']['garch']['sd_z']:.2f}"),
                      (QC.IDEA, rf"robust $z^*$, sd {t['z_q4']['garch']['sd_z_star']:.2f}")], font_size=17).to_edge(
            RIGHT, buff=0.35).shift(UP * 1.2)
        with self.voiceover(
            "The reason, in one picture. <bookmark mark='a'/> Under clustering, the iid statistic is still centred at "
            "zero, but it is too wide: its standard deviation is about one and a half, so its tails cross plus or minus two far "
            "more often than a standard normal's. <bookmark mark='b'/> The robust statistic, divided by the right "
            "variance, lies almost on the normal curve."
        ) as vo:
            self.play(FadeIn(g), Create(nrm), FadeIn(leg))
            vo.wait_until("a")
            self.play(Create(lines[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(lines[1]), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def power(self, t):
        pw = t["power_q4"]
        rows = VGroup(*[MathTex(rf"\rho = {r}:\ \ {100 * v:.0f}\%", font_size=32, color=REAL) for r, v in pw.items()]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3).move_to(LEFT * 2.5 + UP * 0.3)
        side = wrapped_label(r"share of paths in which the robust $z^*$ at $q = 4$ rejects the walk, when returns follow "
                             r"an AR(1) with autocorrelation $\rho$ and GARCH shocks; 1{,}500 weekly returns. Chapter 4's "
                             r"small stocks of 1962--85 had $\rho_1$ near 0.3", 5.0, 18, GREY_A).move_to(RIGHT * 3.0 + UP * 0.3)
        with self.voiceover(
            "And the robustness does not cost much power. <bookmark mark='a'/> Against a weekly autocorrelation of "
            "point zero five, fifteen hundred returns reject the walk about one time in five; at point one, two times "
            "in three; at point two, almost always. Chapter 4's small stocks of 1962 to 85, at about point three, "
            "could not have hidden."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def data(self, v):
        hx = [-3.6, -0.6, 1.4, 3.4, 5.2]
        head = VGroup(label(r"weekly, $q = 4$", font_size=18, color=GREY_B), label(r"1962--85: $z$", font_size=18),
                      label(r"$z^*$", font_size=18), label(r"1986--2020: $z$", font_size=18), label(r"$z^*$", font_size=18))
        k4 = v["q"].index(4)
        names = {"small": (r"smallest 10\%", SMALL), "large": (r"largest 10\%", LARGE), "market": (r"whole market", REAL)}
        tab = VGroup()
        for j, row in enumerate([head] + [VGroup(label(nm, font_size=18, color=col),
                                                 *[MathTex(rf"{v[era][key]['vr'][k4][s]:.1f}", font_size=24)
                                                   for era in ("lm", "after") for s in ("z", "z_star")])
                                          for key, (nm, col) in names.items()]):
            for i, cell in enumerate(row):
                cell.move_to([hx[i], 1.4 - 0.7 * j, 0])
            row[0].align_to(np.array([hx[0] - 1.8, 0, 0]), LEFT)
            tab.add(row)
        foot = wrapped_label(r"Chapter 4's replication, both statistics. Where $z$ and $z^*$ part, the volatility of the "
                             r"sample did; where both exceed two, the walk is rejected whatever the clustering", 11.0, 17,
                             GREY_A).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Back to Chapter 4's data, with both statistics. <bookmark mark='a'/> From 1962 to 1985 the smallest "
            "stocks reject the walk overwhelmingly either way, a z of fifteen and a z star of eleven, and the whole "
            "market rejects too. After 1986 the smallest stocks still reject, but the robust statistic is less than "
            "half the iid one, three point seven against eight and a half: much of the later evidence was volatility, "
            "not memory. The market and the large stocks show nothing either way."
        ) as vo:
            self.play(FadeIn(tab[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[1:]], lag_ratio=0.3), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open_problems(self):
        cards = VGroup(
            desk_question(r"open: infinite fourth moments", r"Chapter 5's tails have an exponent near three, so $\delta_k$ "
                          r"may not exist: sample autocorrelations of heavy-tailed GARCH converge more slowly, to "
                          r"non-normal limits (Davis and Mikosch 1998). Valid variance-ratio inference there is unsettled",
                          width=12.4, font_size=18),
            desk_question(r"open: long horizons", r"when $q$ grows with $n$ the normal limit fails and overlapping sums "
                          r"have non-standard laws (Richardson and Stock 1989); what to report at horizons of years is "
                          r"debated", width=12.4, font_size=18),
            desk_question(r"open: which $q$?", r"testing many $q$ at once is a multiple test (Chow and Denning 1993); "
                          r"data-chosen $q$ (Choi 1999) and the wild bootstrap (Kim 2006) are partial answers", width=12.4,
                          font_size=18),
        ).arrange(DOWN, buff=0.22)
        with self.voiceover(
            "Three open questions. <bookmark mark='a'/> Chapter 5 found tail exponents near three, so the fourth "
            "moment the theorem needs may not exist. Sample autocorrelations of heavy-tailed processes then converge "
            "more slowly, to limits that are not normal, and valid inference for the variance ratio there is "
            "unsettled. <bookmark mark='b'/> When the horizon grows with the sample, the normal limit fails, and the "
            "laws of long overlapping sums are non-standard. <bookmark mark='c'/> And testing many horizons at once is "
            "a multiple test: which q to report is itself a choice the counter of Part 26 should see."
        ) as vo:
            for k, mk in enumerate(("a", "b", "c")):
                vo.wait_until(mk)
                self.play(FadeIn(cards[k], shift=UP * 0.2))
        self.wait(0.4)
        self.clear_scene()

    def question(self):
        q = ask(r"a weekly series of 1{,}500 returns gives $\operatorname{VR}(4) = 1.10$. Compute the iid $z$. If $\delta_1 "
                r"= \delta_2 = \delta_3 = 2$, what is $z^*$?")
        with self.voiceover(
            "Pause and predict. Fifteen hundred weekly returns give a variance ratio at four of one point one. "
            "Compute the iid z. If the first three deltas are all two, what is z star?"
        ):
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()
